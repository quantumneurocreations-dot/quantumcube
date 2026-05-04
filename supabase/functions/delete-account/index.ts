import { serve } from "https://deno.land/std@0.192.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.4";

// Service-role client — used ONLY to verify JWT and perform admin delete.
// This key is in the Edge Function env vars, NEVER exposed to client.
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405, headers: CORS });
  }

  // Extract user JWT from Authorization header
  const authHeader = req.headers.get("authorization") || "";
  const jwt = authHeader.replace(/^Bearer\s+/i, "");
  if (!jwt) {
    return new Response(JSON.stringify({ error: "missing_auth" }), {
      status: 401,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }

  // Verify JWT and extract user id — never trust client-supplied user id
  const sb = createClient(SUPABASE_URL, SERVICE_KEY, {
    auth: { autoRefreshToken: false, persistSession: false },
  });

  const { data: { user }, error: userErr } = await sb.auth.getUser(jwt);
  if (userErr || !user) {
    return new Response(JSON.stringify({ error: "invalid_token" }), {
      status: 401,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }

  const userId = user.id;

  // ── Rate limit (reuses narrate's general-purpose RPC) ──
  const _now = Date.now();
  const _minEnd = new Date(Math.floor(_now / 60000) * 60000 + 60000).toISOString();
  const _hourEnd = new Date(Math.floor(_now / 3600000) * 3600000 + 3600000).toISOString();
  const { data: _rl, error: _rlErr } = await sb.rpc("narrate_rate_limit_try", {
    p_min_key: `delete:${user.id}:m`,
    p_hour_key: `delete:${user.id}:h`,
    p_min_cap: 2,
    p_hour_cap: 5,
    p_min_window_end: _minEnd,
    p_hour_window_end: _hourEnd,
  });
  if (_rlErr) {
    console.error(`delete-account rate_limit error:`, _rlErr);
    return new Response(JSON.stringify({ error: "rate_limit_unavailable" }), {
      status: 503,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }
  if (!_rl?.ok) {
    return new Response(
      JSON.stringify({ error: "rate_limited", retry_after_seconds: _rl?.retry_after ?? 60 }),
      {
        status: 429,
        headers: {
          ...CORS,
          "Content-Type": "application/json",
          "Retry-After": String(_rl?.retry_after ?? 60),
        },
      },
    );
  }

  console.log(`delete-account: deleting user_id=${userId} at ${new Date().toISOString()}`);

  // Admin delete — cascades to public.profiles via on-delete-cascade FK
  const { error: deleteErr } = await sb.auth.admin.deleteUser(userId);
  if (deleteErr) {
    console.error(`delete-account: admin delete failed for ${userId}:`, deleteErr);
    return new Response(
      JSON.stringify({ error: "delete_failed" }),
      { status: 500, headers: { ...CORS, "Content-Type": "application/json" } },
    );
  }

  console.log(`delete-account: success user_id=${userId}`);
  return new Response(JSON.stringify({ success: true }), {
    status: 200,
    headers: { ...CORS, "Content-Type": "application/json" },
  });
});
