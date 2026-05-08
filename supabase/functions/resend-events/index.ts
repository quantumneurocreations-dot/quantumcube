// supabase/functions/resend-events/index.ts
//
// Receives Resend webhook events and forwards critical email-delivery
// failures (bounce, complaint, delayed) to Sentry as warnings/errors.
// Closes the Resend-monitoring gap noted in PROJECT_BRIEF.md (carry-forward
// from the May 5 Resend audit: "Webhooks: NONE configured").
//
// Subscribed events (set in Resend dashboard → Webhooks):
//   email.bounced            → Sentry warning  (hard fail, user can't get magic link)
//   email.complained         → Sentry error    (marked as spam, reputation hit)
//   email.delivery_delayed   → Sentry info     (transient, may resolve on its own)
// All other event types (delivered, opened, clicked, etc.) are ack'd 200 but
// not forwarded — they would burn Sentry quota with no actionable signal.
//
// Required Supabase secrets:
//   RESEND_WEBHOOK_SECRET    (signing secret from Resend webhook config — starts with whsec_)
//   SENTRY_DSN               (optional — defaults to the Quantum Cube project DSN below)
//
// supabase/config.toml must include:
//   [functions.resend-events]
//   verify_jwt = false
//
// Resend uses the Standard Webhooks spec (svix-id / svix-timestamp / svix-signature
// headers). Verification via the standardwebhooks SDK.

import { serve } from "https://deno.land/std@0.208.0/http/server.ts";
import { Webhook } from "https://esm.sh/standardwebhooks@1.0.0";

const WEBHOOK_SECRET = Deno.env.get("RESEND_WEBHOOK_SECRET") ?? "";
const SENTRY_DSN = Deno.env.get("SENTRY_DSN") ??
  "https://fc0733d091a210fe80f9213b64fafa8e@o4511330222604288.ingest.de.sentry.io/4511330235908176";

// ── Resend event shape (per https://resend.com/docs/dashboard/webhooks/event-types) ──

interface ResendEvent {
  type: string;
  created_at: string;
  data: {
    email_id?: string;
    from?: string;
    to?: string[];
    subject?: string;
    bounce?: {
      type?: string;     // "Permanent" | "Transient" | "Undetermined"
      message?: string;
      subType?: string;
    };
    complaint?: {
      complainedRecipients?: Array<{ emailAddress: string }>;
      complaintFeedbackType?: string;
    };
    [key: string]: unknown;
  };
}

// ── Sentry forwarding (direct HTTP to /api/<projectId>/store/) ────────────

interface ParsedDsn {
  publicKey: string;
  host: string;
  projectId: string;
}

function parseDsn(dsn: string): ParsedDsn | null {
  // Format: https://<publicKey>@<host>/<projectId>
  const m = dsn.match(/^https:\/\/([^@]+)@([^/]+)\/(\d+)$/);
  if (!m) return null;
  return { publicKey: m[1], host: m[2], projectId: m[3] };
}

function levelFor(eventType: string): "info" | "warning" | "error" {
  if (eventType === "email.complained") return "error";
  if (eventType === "email.bounced") return "warning";
  if (eventType === "email.delivery_delayed") return "info";
  return "info";
}

async function sendToSentry(event: ResendEvent): Promise<void> {
  const dsn = parseDsn(SENTRY_DSN);
  if (!dsn) {
    console.error(`resend-events: invalid SENTRY_DSN format`);
    return;
  }

  const recipient = event.data.to?.[0]
    ?? event.data.complaint?.complainedRecipients?.[0]?.emailAddress
    ?? "unknown";

  const level = levelFor(event.type);

  const payload = {
    timestamp: new Date().toISOString(),
    level,
    logger: "resend-webhook",
    platform: "javascript",
    environment: "production",
    release: "resend-events@1.0.0",
    message: `Resend ${event.type}: ${recipient}`,
    tags: {
      event_type: event.type,
      service: "resend",
      recipient_domain: recipient.includes("@") ? recipient.split("@")[1] : "unknown",
      bounce_type: event.data.bounce?.type ?? "n/a",
    },
    extra: {
      email_id: event.data.email_id,
      subject: event.data.subject,
      from: event.data.from,
      to: event.data.to,
      bounce: event.data.bounce,
      complaint: event.data.complaint,
      created_at: event.created_at,
    },
    fingerprint: ["resend", event.type, recipient.split("@")[1] ?? "unknown"],
  };

  const url = `https://${dsn.host}/api/${dsn.projectId}/store/`;
  const auth = `Sentry sentry_version=7, sentry_key=${dsn.publicKey}, sentry_client=resend-webhook/1.0.0`;

  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Sentry-Auth": auth,
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const body = await res.text();
    console.error(`resend-events: sentry post failed ${res.status}: ${body}`);
  }
}

// ── Webhook handler ────────────────────────────────────────────────────────

const FORWARDED_EVENTS = new Set([
  "email.bounced",
  "email.complained",
  "email.delivery_delayed",
]);

serve(async (req: Request) => {
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  // Read raw body BEFORE any parsing — Standard Webhooks signature verifies
  // exact bytes including whitespace, ordering, etc.
  const rawBody = await req.text();

  const svixId = req.headers.get("svix-id");
  const svixTimestamp = req.headers.get("svix-timestamp");
  const svixSignature = req.headers.get("svix-signature");

  if (!svixId || !svixTimestamp || !svixSignature) {
    console.warn("resend-events: missing svix headers");
    return new Response(
      JSON.stringify({ error: "missing signature headers" }),
      { status: 400, headers: { "content-type": "application/json" } },
    );
  }

  if (!WEBHOOK_SECRET) {
    // Hard fail — never accept unverified webhooks in production.
    console.error("resend-events: RESEND_WEBHOOK_SECRET not set — refusing event");
    return new Response(
      JSON.stringify({ error: "server not configured" }),
      { status: 503, headers: { "content-type": "application/json" } },
    );
  }

  try {
    const wh = new Webhook(WEBHOOK_SECRET);
    wh.verify(rawBody, {
      "svix-id": svixId,
      "svix-timestamp": svixTimestamp,
      "svix-signature": svixSignature,
    });
  } catch (err) {
    console.warn(`resend-events: signature verification failed: ${err}`);
    return new Response(
      JSON.stringify({ error: "invalid signature" }),
      { status: 401, headers: { "content-type": "application/json" } },
    );
  }

  let event: ResendEvent;
  try {
    event = JSON.parse(rawBody) as ResendEvent;
  } catch {
    return new Response(
      JSON.stringify({ error: "invalid json" }),
      { status: 400, headers: { "content-type": "application/json" } },
    );
  }

  console.log(`resend-events: ${event.type} svix-id=${svixId}`);

  // Forward critical events to Sentry; ack everything 200 so Resend doesn't retry.
  if (FORWARDED_EVENTS.has(event.type)) {
    try {
      await sendToSentry(event);
    } catch (err) {
      // Never block the webhook ack on Sentry availability.
      console.error(`resend-events: sentry send threw: ${err}`);
    }
  }

  return new Response(
    JSON.stringify({ ok: true, type: event.type }),
    { status: 200, headers: { "content-type": "application/json" } },
  );
});
