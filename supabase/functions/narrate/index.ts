import { serve } from "https://deno.land/std@0.192.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.4";

const KEY = Deno.env.get("ELEVENLABS_API_KEY")!;
const ANON_KEY = Deno.env.get("SUPABASE_ANON_KEY")!;
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const MODEL = "eleven_turbo_v2_5";

// Service-role client — used ONLY to verify the user's JWT (auth.getUser).
const sb = createClient(SUPABASE_URL, SERVICE_ROLE, {
  auth: { autoRefreshToken: false, persistSession: false },
});

// ── GLOBAL DAILY CHARACTER CEILING ─────────────────────────
// Hard cap on total characters synthesised across ALL users per UTC day so
// total ElevenLabs spend is bounded even under distributed abuse. Tune to taste.
const DAILY_CHAR_CAP = 500_000;

// Atomically reserve `chars` against today's global budget. Returns ok=false
// (without counting) when the request would breach the ceiling.
async function reserveDailyChars(chars: number): Promise<{ ok: boolean; remaining?: number }> {
  const day = new Date().toISOString().slice(0, 10); // UTC YYYY-MM-DD
  const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/narrate_daily_chars_try`, {
    method: "POST",
    headers: {
      apikey: SERVICE_ROLE,
      Authorization: `Bearer ${SERVICE_ROLE}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ p_day: day, p_chars: chars, p_cap: DAILY_CHAR_CAP }),
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`daily_cap_rpc ${res.status}: ${detail}`);
  }
  const j = (await res.json()) as { ok: boolean; remaining?: number };
  return { ok: j.ok, remaining: j.remaining };
}

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

// `scope` is the identity the limit keys on. We call this once per user_id
// (primary limit) and once per IP (defence-in-depth) so abuse is bounded by
// both authenticated identity and network origin.
async function checkRateLimit(
  scopeKind: "user" | "ip",
  scope: string,
): Promise<{ ok: true } | { ok: false; retryAfter: number; reason: string }> {
  const now = Date.now();
  const minuteBucket = Math.floor(now / 60_000);
  const hourBucket = Math.floor(now / 3_600_000);
  const minKey = `narrate:${scopeKind}:min:${scope}:${minuteBucket}`;
  const hrKey = `narrate:${scopeKind}:hr:${scope}:${hourBucket}`;
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

  // Lazy janitor: prune counters older than 10 min so the table never grows unbounded.
  // Awaited per spec; .catch() swallows failures so a transient delete error never kills a narration.
  const cutoff = new Date(Date.now() - 10 * 60 * 1000).toISOString();
  await fetch(
    `${SUPABASE_URL}/rest/v1/narrate_rate_counters?window_end=lt.${encodeURIComponent(cutoff)}`,
    {
      method: "DELETE",
      headers: {
        apikey: SERVICE_ROLE,
        Authorization: `Bearer ${SERVICE_ROLE}`,
        Prefer: "return=minimal",
      },
    },
  ).catch((e) => { console.warn("narrate cleanup failed:", e); });

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
// DEPLOY COORDINATION (v359): this function now REQUIRES a real user JWT. The
// client (docs/app.html `_qcFetchNarrationChunk`) currently sends the public
// SUPABASE_ANON_KEY as the Authorization bearer, which is now rejected. Before
// (or with) deploying this function, update the client to send the user's
// session.access_token as `Authorization: Bearer <access_token>` — otherwise
// narration will 401 for all users. Edge-function-only PR by design; the
// app.html change is a separate, coordinated human step.
serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return new Response("Method not allowed", { status: 405, headers: CORS });

  // v359: require a real user JWT (mirrors delete-account/export-data). The anon
  // key is public in the client bundle and proves nothing — rate limits now key
  // on the authenticated user_id, not just IP.
  const jwt = req.headers.get("authorization")?.replace(/^Bearer\s+/i, "") ?? "";
  if (!jwt || jwt === ANON_KEY) {
    return new Response(JSON.stringify({ error: "unauthorized" }), {
      status: 401,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }
  const { data: { user }, error: userErr } = await sb.auth.getUser(jwt);
  if (userErr || !user) {
    return new Response(JSON.stringify({ error: "unauthorized" }), {
      status: 401,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }

  const ip = getClientIp(req);
  // Primary limit keyed on user_id; per-IP limit kept as defence-in-depth.
  let rl: Awaited<ReturnType<typeof checkRateLimit>>;
  try {
    rl = await checkRateLimit("user", user.id);
    if (rl.ok) rl = await checkRateLimit("ip", ip);
  } catch (e) {
    console.error("narrate rate_limit error:", e);
    return new Response(JSON.stringify({ error: "rate_limit_unavailable" }), {
      status: 503,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }

  if (!rl.ok) {
    console.log(`narrate rate-limit hit: user=${user.id} ip=${ip} window=${rl.reason} retryAfter=${rl.retryAfter}s`);
    return new Response(
      JSON.stringify({ error: "rate_limited", retry_after_seconds: rl.retryAfter }),
      {
        status: 429,
        headers: { ...CORS, "Content-Type": "application/json", "Retry-After": String(rl.retryAfter) },
      },
    );
  }

  try {
    const body = await req.json() as { text?: string; voice_id?: string; speed?: number };
    const { text, voice_id, speed: speedRaw } = body;
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

    // Global daily character ceiling — bounds total ElevenLabs spend across all
    // users. Reserve before billing; refuse (without counting) past the cap.
    let cap: { ok: boolean; remaining?: number };
    try {
      cap = await reserveDailyChars(text.length);
    } catch (e) {
      console.error("narrate daily_cap error:", e);
      return new Response(JSON.stringify({ error: "rate_limit_unavailable" }), {
        status: 503,
        headers: { ...CORS, "Content-Type": "application/json" },
      });
    }
    if (!cap.ok) {
      console.warn(`narrate daily-cap hit: user=${user.id} requested=${text.length} remaining=${cap.remaining ?? 0}`);
      return new Response(JSON.stringify({ error: "daily_capacity_reached" }), {
        status: 429,
        headers: { ...CORS, "Content-Type": "application/json", "Retry-After": "3600" },
      });
    }

    let speed = 1.15;
    if (typeof speedRaw === "number" && Number.isFinite(speedRaw)) {
      speed = Math.min(1.5, Math.max(0.25, speedRaw));
    }

    const r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voice_id}`, {
      method: "POST",
      headers: { "xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg" },
      body: JSON.stringify({
        text,
        model_id: MODEL,
        voice_settings: { stability: 0.5, similarity_boost: 0.75, speed },
      }),
    });
    if (!r.ok) {
      const err = await r.text();
      console.error("narrate elevenlabs error:", r.status, err);
      return new Response(JSON.stringify({ error: "elevenlabs_failed" }), {
        status: r.status,
        headers: { ...CORS, "Content-Type": "application/json" },
      });
    }
    return new Response(r.body, { status: 200, headers: { ...CORS, "Content-Type": "audio/mpeg" } });
  } catch (e) {
    console.error("narrate handler error:", e);
    return new Response(JSON.stringify({ error: "internal_error" }), {
      status: 500,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }
});
