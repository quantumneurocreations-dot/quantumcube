// verify-play-purchase — Google Play Billing server-side verification
// Called from TWA after a successful Digital Goods API purchase.
//
// Flow:
//   1. Client sends { purchaseToken, userId }
//   2. We call Google Play Developer API to verify the token
//   3. Confirm productId === 'quantum_cube_unlock' and purchaseState === 0 (purchased)
//   4. Call setHasPaid(userId, true)
//   5. Acknowledge the purchase (REQUIRED — unacknowledged purchases auto-refund after 3 days)
//
// Required Supabase secrets:
//   PLAY_SERVICE_ACCOUNT_JSON  (contents of ~/.config/qi/play-service-account.json)
//   SUPABASE_URL               (auto-injected)
//   SUPABASE_SERVICE_ROLE_KEY  (auto-injected)

import { serve } from "https://deno.land/std@0.208.0/http/server.ts";
import { create, getNumericDate } from "https://deno.land/x/djwt@v3.0.2/mod.ts";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const PLAY_SA_JSON = Deno.env.get("PLAY_SERVICE_ACCOUNT_JSON")!;

const PACKAGE_NAME = "app.quantumcube.twa";
const PRODUCT_ID = "quantum_cube_unlock";

async function getGoogleAccessToken(): Promise<string> {
  const sa = JSON.parse(PLAY_SA_JSON);
  const pemBody = sa.private_key
    .replace("-----BEGIN PRIVATE KEY-----", "")
    .replace("-----END PRIVATE KEY-----", "")
    .replace(/\s/g, "");
  const keyBytes = Uint8Array.from(atob(pemBody), (c) => c.charCodeAt(0));
  const cryptoKey = await crypto.subtle.importKey(
    "pkcs8", keyBytes,
    { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" },
    false, ["sign"],
  );
  const jwt = await create(
    { alg: "RS256", typ: "JWT" },
    {
      iss: sa.client_email,
      scope: "https://www.googleapis.com/auth/androidpublisher",
      aud: "https://oauth2.googleapis.com/token",
      exp: getNumericDate(3600),
      iat: getNumericDate(0),
    },
    cryptoKey,
  );
  const tokenRes = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion=${jwt}`,
  });
  if (!tokenRes.ok) throw new Error(`Google token ${tokenRes.status}: ${await tokenRes.text()}`);
  const { access_token } = await tokenRes.json();
  return access_token;
}

async function verifyPurchaseToken(accessToken: string, purchaseToken: string) {
  const url = `https://androidpublisher.googleapis.com/androidpublisher/v3/applications/${PACKAGE_NAME}/purchases/products/${PRODUCT_ID}/tokens/${purchaseToken}`;
  const res = await fetch(url, { headers: { Authorization: `Bearer ${accessToken}` } });
  if (!res.ok) throw new Error(`Play verify ${res.status}: ${await res.text()}`);
  const data = await res.json();
  return {
    valid: data.purchaseState === 0,
    alreadyAcknowledged: data.acknowledgementState === 1,
  };
}

async function acknowledgePurchase(accessToken: string, purchaseToken: string) {
  const url = `https://androidpublisher.googleapis.com/androidpublisher/v3/applications/${PACKAGE_NAME}/purchases/products/${PRODUCT_ID}/tokens/${purchaseToken}:acknowledge`;
  const res = await fetch(url, {
    method: "POST",
    headers: { Authorization: `Bearer ${accessToken}`, "Content-Type": "application/json" },
    body: JSON.stringify({}),
  });
  if (!res.ok && res.status !== 204) throw new Error(`Play ack ${res.status}: ${await res.text()}`);
}

async function setHasPaid(userId: string, value: boolean): Promise<number> {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/profiles?id=eq.${userId}`, {
    method: "PATCH",
    headers: {
      apikey: SERVICE_ROLE,
      Authorization: `Bearer ${SERVICE_ROLE}`,
      "Content-Type": "application/json",
      "Prefer": "return=representation",
    },
    body: JSON.stringify({ has_paid: value }),
  });
  if (!res.ok) throw new Error(`profile update ${res.status}: ${await res.text()}`);
  return (await res.json()).length;
}

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "authorization, content-type" } });
  }
  const cors = { "Access-Control-Allow-Origin": "*", "Content-Type": "application/json" };
  try {
    const { purchaseToken, userId } = await req.json();
    if (!purchaseToken || !userId) {
      return new Response(JSON.stringify({ error: "purchaseToken and userId required" }), { status: 400, headers: cors });
    }
    const accessToken = await getGoogleAccessToken();
    const { valid, alreadyAcknowledged } = await verifyPurchaseToken(accessToken, purchaseToken);
    if (!valid) {
      console.warn(`verify-play-purchase: invalid purchase userId=${userId}`);
      return new Response(JSON.stringify({ error: "purchase_invalid" }), { status: 400, headers: cors });
    }
    const updated = await setHasPaid(userId, true);
    console.log(`verify-play-purchase: has_paid=true userId=${userId} rows=${updated}`);
    if (!alreadyAcknowledged) {
      await acknowledgePurchase(accessToken, purchaseToken);
      console.log(`verify-play-purchase: acknowledged userId=${userId}`);
    }
    return new Response(JSON.stringify({ ok: true, updated }), { status: 200, headers: cors });
  } catch (e) {
    console.error("verify-play-purchase error:", String(e));
    return new Response(JSON.stringify({ error: "internal_error", detail: String(e) }), { status: 500, headers: cors });
  }
});
