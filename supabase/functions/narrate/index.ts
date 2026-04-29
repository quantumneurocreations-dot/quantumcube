import { serve } from "https://deno.land/std@0.192.0/http/server.ts";

const KEY = Deno.env.get("ELEVENLABS_API_KEY")!;
const EXPECTED_APIKEY = Deno.env.get("SUPABASE_ANON_KEY")!;
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const MODEL = "eleven_turbo_v2_5";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

// ── RATE LIMITING ──────────────────────────────────────────
// Per-IP limits via Postgres RPC (Deno KV is not available on Supabase Edge).
// Two windows: burst (5/min) + sustained (20/hr).
const LIMIT_PER_MINUTE = 5;
const LIMIT_PER_HOUR = 20;

async function checkRateLimit(ip: string): Promise<{ ok: true } | { ok: false; retryAfter: number; reason: string }> {
  const now = Date.now();
  const minuteBucket = Math.floor(now / 60_000);
  const hourBucket = Math.floor(now / 3_600_000);
  const minKey = `narrate:min:${ip}:${minuteBucket}`;
  const hrKey = `narrate:hr:${ip}:${hourBucket}`;
  const minEndIso = new Date((minuteBucket + 1) * 60_000).toISOString();
  const hrEndIso = new Date((hourBucket + 1) * 3_600_000).toISOString();

  const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/narrate_rate_limit_try`, {
    method: "POST",
    headers: {
      apikey: SERVICE_ROLE,
      Authorization: `Bearer ${SERVICE_ROLE}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      p_min_key: minKey,
      p_hour_key: hrKey,
      p_min_cap: LIMIT_PER_MINUTE,
      p_hour_cap: LIMIT_PER_HOUR,
      p_min_window_end: minEndIso,
      p_hour_window_end: hrEndIso,
    }),
  });

  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`rate_limit_rpc ${res.status}: ${detail}`);
  }

  const j = (await res.json()) as { ok: boolean; reason?: string; retry_after?: number };
  if (j.ok === false) {
    return {
      ok: false,
      retryAfter: j.retry_after ?? 60,
      reason: j.reason ?? "minute",
    };
  }
  return { ok: true };
}

function getClientIp(req: Request): string {
  return req.headers.get("x-forwarded-for")?.split(",")?.[0]?.trim()
    || req.headers.get("cf-connecting-ip")
    || "unknown";
}

// ── HANDLER ─────────────────────────────────────────────────
serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return new Response("Method not allowed", { status: 405, headers: CORS });

  const apikey = req.headers.get("apikey") || req.headers.get("authorization")?.replace(/^Bearer\s+/i, "");
  if (!apikey || apikey !== EXPECTED_APIKEY) {
    return new Response(JSON.stringify({ error: "unauthorized" }), {
      status: 401,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }

  const ip = getClientIp(req);
  let rl: Awaited<ReturnType<typeof checkRateLimit>>;
  try {
    rl = await checkRateLimit(ip);
  } catch (e) {
    console.error("narrate rate_limit error:", e);
    return new Response(JSON.stringify({ error: "rate_limit_unavailable", detail: String(e) }), {
      status: 503,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }

  if (!rl.ok) {
    console.log(`narrate rate-limit hit: ip=${ip} window=${rl.reason} retryAfter=${rl.retryAfter}s`);
    return new Response(
      JSON.stringify({ error: "rate_limited", retry_after_seconds: rl.retryAfter }),
      {
        status: 429,
        headers: { ...CORS, "Content-Type": "application/json", "Retry-After": String(rl.retryAfter) },
      },
    );
  }

  try {
    const { text, voice_id } = await req.json();
    if (!text || !voice_id) {
      return new Response(JSON.stringify({ error: "missing text or voice_id" }), {
        status: 400,
        headers: { ...CORS, "Content-Type": "application/json" },
      });
    }
    if (text.length > 2500) {
      return new Response(JSON.stringify({ error: "text too long" }), {
        status: 400,
        headers: { ...CORS, "Content-Type": "application/json" },
      });
    }

    const r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voice_id}`, {
      method: "POST",
      headers: { "xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg" },
      body: JSON.stringify({
        text,
        model_id: MODEL,
        voice_settings: { stability: 0.5, similarity_boost: 0.75, speed: 1.15 },
      }),
    });
    if (!r.ok) {
      const err = await r.text();
      return new Response(JSON.stringify({ error: "elevenlabs failed", detail: err }), {
        status: r.status,
        headers: { ...CORS, "Content-Type": "application/json" },
      });
    }
    return new Response(r.body, { status: 200, headers: { ...CORS, "Content-Type": "audio/mpeg" } });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e) }), {
      status: 500,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }
});
