// supabase/functions/dodo-webhook/index.ts
//
// Receives Dodo Payments webhook events and updates user profile
// has_paid status. Verified via Standard Webhooks signature.
//
// On payment.succeeded transition (unpaid -> paid):
//   - adds customer to Resend audience "Quantum Cube Customers"
//   - sends welcome email via Resend (best-effort, non-blocking on failure)
//
// Subscribed events:
//   payment.succeeded -> has_paid = true (+ welcome email on transition)
//   refund.succeeded  -> has_paid = false
//   dispute.lost      -> has_paid = false  (merchant fought + lost; funds taken)
//   dispute.accepted  -> has_paid = false  (merchant accepted; refund issued)
//   (dispute.opened / dispute.won are intentionally ignored — not terminal losses)
//
// Required Supabase secrets (set via dashboard or `supabase secrets set`):
//   DODO_PAYMENTS_WEBHOOK_KEY  (signing secret from Dodo webhook config)
//   DODO_PAYMENTS_API_KEY      (API key from Dodo dashboard)
//   RESEND_API_KEY             (API key from Resend dashboard) - optional;
//                              if absent, Resend integration is skipped
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
const RESEND_API_KEY = Deno.env.get("RESEND_API_KEY") ?? "";
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

const RESEND_AUDIENCE_ID = "d9ba37bf-57f3-4e9b-929c-2bac5c2e856d"; // "Quantum Cube Customers"
const RESEND_FROM = "Quantum Cube <welcome@quantumcube.app>";
const RESEND_REPLY_TO = "quantumneurocreations@gmail.com";

const dodoClient = new DodoPayments({
  bearerToken: API_KEY,
  webhookKey: WEBHOOK_KEY,
});

// ── Profile helpers ─────────────────────────────────────────────────────────

async function getProfile(
  target: { user_id?: string; email?: string },
): Promise<{ id?: string; email?: string; name?: string; has_paid?: boolean } | null> {
  const url = target.user_id
    ? `${SUPABASE_URL}/rest/v1/profiles?id=eq.${target.user_id}&select=id,email,name,has_paid`
    : `${SUPABASE_URL}/rest/v1/profiles?email=eq.${encodeURIComponent(target.email!)}&select=id,email,name,has_paid`;

  const res = await fetch(url, {
    headers: {
      apikey: SERVICE_ROLE,
      Authorization: `Bearer ${SERVICE_ROLE}`,
    },
  });

  if (!res.ok) {
    console.warn(`profile fetch failed ${res.status}`);
    return null;
  }

  const rows = (await res.json()) as Array<Record<string, unknown>>;
  return (rows[0] as any) ?? null;
}

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

// v358: dispute (and as a safety net, refund) events originate outside our
// checkout flow — they come from the card network/bank — so they may omit our
// metadata.user_id and, depending on payload shape, the customer block. When we
// have no usable identifier but the event references a payment, recover identity
// from the originating payment (which carries our create-session metadata.user_id
// and the customer email).
async function recoverIdentityFromPayment(
  paymentId: string,
): Promise<{ user_id?: string; email?: string } | null> {
  try {
    const payment = (await dodoClient.payments.retrieve(paymentId)) as any;
    const uid = payment?.metadata?.user_id;
    const email = payment?.customer?.email;
    if (typeof uid === "string" && uid) return { user_id: uid, email };
    if (typeof email === "string" && email) return { email };
    return null;
  } catch (e) {
    console.error(`payment lookup failed for ${paymentId}:`, String(e));
    return null;
  }
}

// ── Resend helpers (best-effort; never throw) ───────────────────────────────

async function addContactToAudience(email: string, firstName?: string): Promise<void> {
  if (!RESEND_API_KEY) {
    console.log("resend: skipping audience add (no RESEND_API_KEY)");
    return;
  }
  try {
    const res = await fetch(
      `https://api.resend.com/audiences/${RESEND_AUDIENCE_ID}/contacts`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${RESEND_API_KEY}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          first_name: firstName ?? "",
          unsubscribed: false,
        }),
      },
    );
    if (!res.ok) {
      const detail = await res.text();
      console.error(`resend audience add failed ${res.status}: ${detail}`);
    } else {
      console.log(`resend audience: added ${email}`);
    }
  } catch (e) {
    console.error("resend audience add error:", String(e));
  }
}

function welcomeHtml(firstName?: string): string {
  const greeting = firstName ? `Welcome, ${firstName}.` : "Welcome.";
  return `<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Your cosmic profile is unlocked</title></head>
<body style="margin:0;padding:0;background:#05050f;font-family:Georgia,'Times New Roman',serif;color:#ffffff;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#05050f;">
<tr><td align="center" style="padding:48px 20px;">
<table role="presentation" width="560" cellpadding="0" cellspacing="0" style="max-width:560px;width:100%;">
<tr><td align="center" style="padding-bottom:32px;">
<span style="font-family:Georgia,'Times New Roman',serif;font-size:30px;letter-spacing:0.12em;color:#ffffff;">QUANTUM <span style="color:#7dd4fc;">C</span>UBE</span>
</td></tr>
<tr><td style="padding-bottom:24px;">
<h1 style="margin:0;font-family:Georgia,'Times New Roman',serif;font-size:26px;font-weight:normal;color:#ffffff;line-height:1.3;text-align:center;">Your cosmic profile is unlocked.</h1>
</td></tr>
<tr><td style="padding-bottom:8px;font-family:Georgia,'Times New Roman',serif;font-size:17px;line-height:1.7;color:#e5e5e5;">
<p style="margin:0 0 18px 0;">${greeting}</p>
<p style="margin:0 0 18px 0;">All four sides of your reading — your numerology, your Western zodiac, your Chinese zodiac, and how they weave together — are yours to revisit whenever you like.</p>
<p style="margin:0 0 18px 0;">There's no subscription. No daily push. No homework.</p>
<p style="margin:0;">Just one carefully curated reading, designed to be read once and returned to often.</p>
</td></tr>
<tr><td align="center" style="padding:36px 0;">
<a href="https://quantumcube.app/app.html" style="display:inline-block;padding:14px 36px;font-family:Georgia,'Times New Roman',serif;font-size:16px;color:#05050f;background:#7dd4fc;text-decoration:none;letter-spacing:0.06em;">Open my Cube  &#10022;</a>
</td></tr>
<tr><td style="padding-top:20px;border-top:1px solid #1a1a2e;font-family:Georgia,'Times New Roman',serif;font-size:14px;line-height:1.7;color:#a8a8b8;">
<p style="margin:0;">If anything's ever unclear — payment, access, the reading itself — reply to this email. A real person reads everything that comes in.</p>
</td></tr>
<tr><td align="center" style="padding-top:36px;font-family:Georgia,'Times New Roman',serif;font-size:12px;line-height:1.6;color:#7a7a8a;">
<p style="margin:0 0 4px 0;">Quantum Cube — Your cosmic profile, simplified.</p>
<p style="margin:0;">Lifetime access. No subscription, ever.</p>
</td></tr>
</table>
</td></tr>
</table>
</body></html>`;
}

function welcomeText(firstName?: string): string {
  const greeting = firstName ? `Welcome, ${firstName}.` : "Welcome.";
  return [
    "QUANTUM CUBE",
    "",
    "Your cosmic profile is unlocked.",
    "",
    greeting,
    "",
    "All four sides of your reading — your numerology, your Western zodiac, your Chinese zodiac, and how they weave together — are yours to revisit whenever you like.",
    "",
    "There's no subscription. No daily push. No homework.",
    "",
    "Just one carefully curated reading, designed to be read once and returned to often.",
    "",
    "Open your Cube: https://quantumcube.app/app.html",
    "",
    "If anything's ever unclear — payment, access, the reading itself — reply to this email. A real person reads everything that comes in.",
    "",
    "—",
    "Quantum Cube — Your cosmic profile, simplified.",
    "Lifetime access. No subscription, ever.",
  ].join("\n");
}

async function sendWelcomeEmail(email: string, firstName?: string): Promise<void> {
  if (!RESEND_API_KEY) {
    console.log("resend: skipping welcome email (no RESEND_API_KEY)");
    return;
  }
  try {
    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: RESEND_FROM,
        to: [email],
        reply_to: RESEND_REPLY_TO,
        subject: "Your cosmic profile is unlocked \u2726",
        html: welcomeHtml(firstName),
        text: welcomeText(firstName),
        tags: [{ name: "type", value: "welcome" }],
      }),
    });
    if (!res.ok) {
      const detail = await res.text();
      console.error(`resend send failed ${res.status}: ${detail}`);
    } else {
      console.log(`resend welcome: sent to ${email}`);
    }
  } catch (e) {
    console.error("resend send error:", String(e));
  }
}

// ── Webhook entrypoint ──────────────────────────────────────────────────────

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
    // unwrap(body, { headers }) — the 2nd arg MUST be an options object. Passing the
    // headers map directly leaves `headers` undefined inside the SDK, which SKIPS
    // signature verification entirely (silent forgery-accept). See SDK webhooks.unwrap.
    event = await dodoClient.webhooks.unwrap(rawBody, { headers: webhookHeaders });
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
    let customerEmail: string | undefined = data.customer?.email;
    const customerName = data.customer?.name;
    const userId = metadata.user_id;

    // v354: validate user_id is a real UUID before trusting it (defence-in-depth +
    // injection-safety for the PostgREST URL interpolation in getProfile/setHasPaid).
    const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
    let validUserId = (typeof userId === "string" && UUID_RE.test(userId)) ? userId : null;
    if (userId && !validUserId) {
      console.warn(`webhook: metadata.user_id present but not a valid UUID: ${JSON.stringify(userId)}`);
    }

    // v358: last-resort identity recovery for events that reference a payment but
    // carry no usable identifier of their own (dispute.* especially). Resolves via
    // the originating payment's metadata.user_id / customer.email.
    if (!validUserId && !customerEmail && typeof data.payment_id === "string") {
      const recovered = await recoverIdentityFromPayment(data.payment_id);
      if (recovered) {
        if (typeof recovered.user_id === "string" && UUID_RE.test(recovered.user_id)) {
          validUserId = recovered.user_id;
        }
        if (!customerEmail && recovered.email) customerEmail = recovered.email;
        console.log(
          `webhook: recovered identity from payment ${data.payment_id} ` +
            `(user_id=${validUserId ? "yes" : "no"} email=${customerEmail ? "yes" : "no"})`,
        );
      }
    }

    if (!validUserId && !customerEmail) {
      console.error("no usable user identifier in event:", JSON.stringify(event));
      // Acknowledge with 200 to prevent retry storm — unrecoverable on our side
      return new Response(JSON.stringify({ ok: true, warning: "no user identifier" }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      });
    }

    // v354: prefer the verified user_id (create-session now sets metadata.user_id from
    // the user's JWT). Email is a secondary fallback only — authentic post-v354 since
    // create-session derives it from the JWT too — but log when relied upon so the
    // fallback path is observable (it should be rare once all sessions carry user_id).
    const target = validUserId ? { user_id: validUserId } : { email: customerEmail };
    if (!validUserId) {
      console.warn(`webhook: falling back to email match for ${customerEmail} (no valid user_id in metadata)`);
    }

    if (event.type === "payment.succeeded") {
      // Capture previous state for idempotency (only welcome on unpaid->paid transition)
      const prevProfile = await getProfile(target);
      const wasUnpaid = !prevProfile?.has_paid;

      const updated = await setHasPaid(target, true);
      console.log(`payment.succeeded -> has_paid=true target=${JSON.stringify(target)} rows=${updated} wasUnpaid=${wasUnpaid}`);

      if (wasUnpaid && customerEmail) {
        const firstName =
          (typeof prevProfile?.name === "string" && prevProfile.name.split(" ")[0]) ||
          (typeof customerName === "string" && customerName.split(" ")[0]) ||
          undefined;
        // Run both in parallel; Promise.allSettled so one failure doesn't block the other
        await Promise.allSettled([
          addContactToAudience(customerEmail, firstName || undefined),
          sendWelcomeEmail(customerEmail, firstName || undefined),
        ]);
      }
    } else if (
      event.type === "refund.succeeded" ||
      event.type === "dispute.lost" ||
      event.type === "dispute.accepted"
    ) {
      // Revenue-leak guard (v358): a lost/accepted dispute means the funds are gone,
      // so revoke access. dispute.opened / dispute.won are NOT terminal — ignore them.
      const updated = await setHasPaid(target, false);
      console.log(`${event.type} -> has_paid=false target=${JSON.stringify(target)} rows=${updated}`);
    } else {
      console.log(`ignoring event type: ${event.type}`);
    }

    return new Response(JSON.stringify({ ok: true }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  } catch (e) {
    console.error("webhook handler error:", String(e));
    return new Response(JSON.stringify({ error: "internal_error" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
});
