// supabase/functions/dodo-webhook/index.ts
//
// Receives Dodo Payments webhook events and updates user profile
// has_paid status. Verified via Standard Webhooks signature.
//
// Subscribed events:
//   payment.succeeded -> has_paid = true
//   refund.succeeded  -> has_paid = false
//
// Required Supabase secrets (set via dashboard or `supabase secrets set`):
//   DODO_PAYMENTS_WEBHOOK_KEY  (signing secret from Dodo webhook config)
//   DODO_PAYMENTS_API_KEY      (API key from Dodo dashboard)
//   SUPABASE_URL               (auto-injected)
//   SUPABASE_SERVICE_ROLE_KEY  (auto-injected)
//
// supabase/config.toml must include:
//   [functions.dodo-webhook]
//   verify_jwt = false

import { serve } from "https://deno.land/std@0.208.0/http/server.ts";
import DodoPayments from "https://esm.sh/dodopayments@2.4.1";

const WEBHOOK_KEY = Deno.env.get("DODO_PAYMENTS_WEBHOOK_KEY") ?? "";
const API_KEY = Deno.env.get("DODO_PAYMENTS_API_KEY") ?? "";
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

const dodoClient = new DodoPayments({
  bearerToken: API_KEY,
  webhookKey: WEBHOOK_KEY,
});

async function setHasPaid(
  target: { user_id?: string; email?: string },
  value: boolean,
): Promise<number> {
  const url = target.user_id
    ? `${SUPABASE_URL}/rest/v1/profiles?id=eq.${target.user_id}`
    : `${SUPABASE_URL}/rest/v1/profiles?email=eq.${encodeURIComponent(target.email!)}`;

  const res = await fetch(url, {
    method: "PATCH",
    headers: {
      apikey: SERVICE_ROLE,
      Authorization: `Bearer ${SERVICE_ROLE}`,
      "Content-Type": "application/json",
      "Prefer": "return=representation",
    },
    body: JSON.stringify({ has_paid: value }),
  });

  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`profile update failed ${res.status}: ${detail}`);
  }

  const rows = (await res.json()) as unknown[];
  return rows.length;
}

serve(async (req) => {
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  const rawBody = await req.text();
  const webhookHeaders = {
    "webhook-id": req.headers.get("webhook-id") ?? "",
    "webhook-signature": req.headers.get("webhook-signature") ?? "",
    "webhook-timestamp": req.headers.get("webhook-timestamp") ?? "",
  };

  // Verify signature (Standard Webhooks spec)
  let event: any;
  try {
    event = await dodoClient.webhooks.unwrap(rawBody, webhookHeaders);
  } catch (e) {
    console.error("webhook signature verification failed:", String(e));
    return new Response(JSON.stringify({ error: "invalid signature" }), {
      status: 401,
      headers: { "Content-Type": "application/json" },
    });
  }

  console.log(`dodo webhook: type=${event.type} business_id=${event.business_id ?? "?"}`);

  try {
    const data = event.data ?? {};
    const metadata = data.metadata ?? {};
    const customerEmail = data.customer?.email;
    const userId = metadata.user_id;

    if (!userId && !customerEmail) {
      console.error("no user identifier in event:", JSON.stringify(event));
      // Acknowledge with 200 to prevent retry storm — unrecoverable on our side
      return new Response(JSON.stringify({ ok: true, warning: "no user identifier" }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      });
    }

    const target = userId ? { user_id: userId } : { email: customerEmail };

    if (event.type === "payment.succeeded") {
      const updated = await setHasPaid(target, true);
      console.log(`payment.succeeded -> has_paid=true target=${JSON.stringify(target)} rows=${updated}`);
    } else if (event.type === "refund.succeeded") {
      const updated = await setHasPaid(target, false);
      console.log(`refund.succeeded -> has_paid=false target=${JSON.stringify(target)} rows=${updated}`);
    } else {
      console.log(`ignoring event type: ${event.type}`);
    }

    return new Response(JSON.stringify({ ok: true }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  } catch (e) {
    console.error("webhook handler error:", String(e));
    return new Response(JSON.stringify({ error: String(e) }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
});
