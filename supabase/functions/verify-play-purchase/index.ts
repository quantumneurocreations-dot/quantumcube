// verify-play-purchase — Google Play Billing server-side verification
// Called from TWA after a successful Digital Goods API purchase.
//
// Flow:
//   1. Client sends { purchaseToken } and a Supabase user access-token (Bearer).
//      The userId is NEVER taken from the body — it is derived from the verified JWT.
//   2. We call Google Play Developer API to verify the token
//   3. Confirm productId === 'quantum_cube_unlock' and purchaseState === 0 (purchased)
//   4. Replay guard: claim the purchaseToken in play_consumed_tokens (UNIQUE PK).
//      An already-consumed token is refused — a token can grant entitlement once.
//   5. Call setHasPaid(userId, true)
//   6. Acknowledge the purchase (REQUIRED — unacknowledged purchases auto-refund after 3 days)
//
// IDOR / replay hardening (v359):
//   - Identity is server-derived from the verified Supabase JWT (mirrors
//     dodo-create-session), so a caller can only grant entitlement to themselves.
//   - Consumed purchaseTokens are persisted with a UNIQUE constraint and rejected
//     on reuse, blocking replay of a captured token.
//   - CLIENT TODO: at purchase launch the TWA should set Google Play's
//     `obfuscatedExternalAccountId` = the Supabase user_id. When Google's verify
//     response includes `obfuscatedExternalAccountId`, we assert it matches the
//     JWT user_id below (defence against cross-account token use). If it is absent
//     (older purchases / not yet wired client-side) we proceed on JWT identity.
//
// supabase/config.toml must include:
//   [functions.verify-play-purchase]
//   verify_jwt = false   (we manually verify the user JWT below)
//
// Required Supabase secrets:
//   PLAY_SERVICE_ACCOUNT_JSON  (contents of ~/.config/qi/play-service-account.json)
//   SUPABASE_URL               (auto-injected)
//   SUPABASE_ANON_KEY          (auto-injected)
//   SUPABASE_SERVICE_ROLE_KEY  (auto-injected)

import { serve } from "https://deno.land/std@0.208.0/http/server.ts";
import { create, getNumericDate } from "https://deno.land/x/djwt@v3.0.2/mod.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.4";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const ANON_KEY = Deno.env.get("SUPABASE_ANON_KEY")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const PLAY_SA_JSON = Deno.env.get("PLAY_SERVICE_ACCOUNT_JSON")!;

const sb = createClient(SUPABASE_URL, SERVICE_ROLE, {
  auth: { autoRefreshToken: false, persistSession: false },
});

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
    // Set client-side via BillingFlowParams.setObfuscatedAccountId(user_id) at
    // purchase launch. May be undefined for purchases made before that was wired.
    obfuscatedExternalAccountId: data.obfuscatedExternalAccountId as string | undefined,
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

// Replay guard: atomically claim a purchaseToken. Returns true if this call
// claimed it (first use), false if it was already consumed (PK conflict → 409).
// The UNIQUE primary key on purchase_token makes the claim race-safe.
async function claimPurchaseToken(
  purchaseToken: string,
  userId: string,
  productId: string,
): Promise<boolean> {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/play_consumed_tokens`, {
    method: "POST",
    headers: {
      apikey: SERVICE_ROLE,
      Authorization: `Bearer ${SERVICE_ROLE}`,
      "Content-Type": "application/json",
      "Prefer": "return=minimal",
    },
    body: JSON.stringify({
      purchase_token: purchaseToken,
      user_id: userId,
      product_id: productId,
    }),
  });
  if (res.status === 409) {
    // Duplicate primary key — token already consumed. Drain body for keep-alive.
    await res.text();
    return false;
  }
  if (!res.ok) throw new Error(`token claim ${res.status}: ${await res.text()}`);
  return true;
}

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "authorization, content-type" } });
  }
  const cors = { "Access-Control-Allow-Origin": "*", "Content-Type": "application/json" };

  // v359: authenticate the USER via their access-token JWT, NOT the request body.
  // Identity (userId) is derived from the verified token; the body cannot grant
  // entitlement to an arbitrary account (IDOR fix). Mirrors dodo-create-session.
  const authToken = req.headers.get("authorization")?.replace(/^Bearer\s+/i, "") ?? "";
  if (!authToken || authToken === ANON_KEY) {
    return new Response(JSON.stringify({ error: "unauthorized" }), { status: 401, headers: cors });
  }
  const { data: { user: authUser }, error: authErr } = await sb.auth.getUser(authToken);
  if (authErr || !authUser) {
    return new Response(JSON.stringify({ error: "unauthorized" }), { status: 401, headers: cors });
  }
  const userId = authUser.id;

  try {
    const body = await req.json().catch(() => ({}));
    const { purchaseToken } = body || {};
    if (!purchaseToken) {
      return new Response(JSON.stringify({ error: "purchaseToken required" }), { status: 400, headers: cors });
    }
    const accessToken = await getGoogleAccessToken();
    const { valid, alreadyAcknowledged, obfuscatedExternalAccountId } = await verifyPurchaseToken(accessToken, purchaseToken);
    if (!valid) {
      console.warn(`verify-play-purchase: invalid purchase userId=${userId}`);
      return new Response(JSON.stringify({ error: "purchase_invalid" }), { status: 400, headers: cors });
    }

    // Assert the purchase was launched for THIS user when Google echoes it back.
    // Client sets obfuscatedExternalAccountId = user_id at purchase launch.
    if (obfuscatedExternalAccountId && obfuscatedExternalAccountId !== userId) {
      console.warn(`verify-play-purchase: account mismatch userId=${userId} obfuscated=${obfuscatedExternalAccountId}`);
      return new Response(JSON.stringify({ error: "account_mismatch" }), { status: 403, headers: cors });
    }

    // Replay guard: a purchaseToken may grant entitlement exactly once.
    const claimed = await claimPurchaseToken(purchaseToken, userId, PRODUCT_ID);
    if (!claimed) {
      console.warn(`verify-play-purchase: token already consumed userId=${userId}`);
      return new Response(JSON.stringify({ error: "token_already_consumed" }), { status: 409, headers: cors });
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
