// supabase/functions/dodo-create-session/index.ts
//
// Mints a Dodo Payments Checkout Session URL for the authenticated user.
// Frontend calls this endpoint, gets back { checkout_url, session_id },
// then opens the overlay via DodoPayments.Checkout.open({ checkoutUrl }).
//
// Required Supabase secrets (already set):
//   DODO_PAYMENTS_API_KEY      (test or live API key)
//
// supabase/config.toml must include:
//   [functions.dodo-create-session]
//   verify_jwt = false   (we manually verify via apikey header)

import { serve } from "https://deno.land/std@0.208.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.4";

const API_KEY = Deno.env.get("DODO_PAYMENTS_API_KEY") ?? "";
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const ANON_KEY = Deno.env.get("SUPABASE_ANON_KEY")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

const sb = createClient(SUPABASE_URL, SERVICE_ROLE, {
  auth: { autoRefreshToken: false, persistSession: false },
});

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

// Mode + product config — kept in sync with frontend DODO_MODE
const MODE = "live"; // flip to "live" for production
const CONFIG = {
  test: {
    apiBase: "https://test.dodopayments.com",
    productId: "pdt_0NdwjT5U975nxTzpogS68",
  },
  live: {
    apiBase: "https://live.dodopayments.com",
    productId: "pdt_0Ndx7o41zFEREpoPTyvR2",
  },
};

serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405, headers: CORS });
  }

  // v354: authenticate the USER via their access-token JWT, NOT the public anon key.
  // The anon key ships in the client bundle and proves nothing about identity. We now
  // validate the bearer token via auth.getUser() and derive user_id/email from it —
  // the request body is never trusted for identity. (Frontend sends the apikey header
  // for the gateway and the user's access_token as Authorization: Bearer.)
  const _authToken = req.headers.get("authorization")?.replace(/^Bearer\s+/i, "") ?? "";
  if (!_authToken || _authToken === ANON_KEY) {
    return new Response(JSON.stringify({ error: "unauthorized" }), {
      status: 401,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }
  const { data: { user: _authUser }, error: _authErr } = await sb.auth.getUser(_authToken);
  if (_authErr || !_authUser) {
    return new Response(JSON.stringify({ error: "unauthorized" }), {
      status: 401,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }

  const _ip = req.headers.get("x-forwarded-for")?.split(",")[0]?.trim() ||
    req.headers.get("cf-connecting-ip") ||
    "unknown";

  // ── Rate limit (reuses narrate's general-purpose RPC) ──
  const _now = Date.now();
  const _minEnd = new Date(Math.floor(_now / 60000) * 60000 + 60000).toISOString();
  const _hourEnd = new Date(Math.floor(_now / 3600000) * 3600000 + 3600000).toISOString();
  const { data: _rl, error: _rlErr } = await sb.rpc("narrate_rate_limit_try", {
    p_min_key: `dodo-session:${_ip}:m`,
    p_hour_key: `dodo-session:${_ip}:h`,
    p_min_cap: 5,
    p_hour_cap: 20,
    p_min_window_end: _minEnd,
    p_hour_window_end: _hourEnd,
  });
  if (_rlErr) {
    console.error(`dodo-create-session rate_limit error:`, _rlErr);
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

  try {
    const body = await req.json().catch(() => ({}));
    const { fullName } = body || {};
    // v354: identity is server-derived from the verified JWT — never the body.
    const user_id = _authUser.id;
    const email = _authUser.email ?? "";

    if (!email) {
      return new Response(JSON.stringify({ error: "verified user has no email" }), {
        status: 400,
        headers: { ...CORS, "Content-Type": "application/json" },
      });
    }

    // Verify the user_id exists in profiles (defence-in-depth; user_id is a verified
    // UUID from auth.users, so this URL interpolation is now injection-safe)
    const profileCheck = await fetch(
      `${SUPABASE_URL}/rest/v1/profiles?id=eq.${user_id}&select=id`,
      {
        headers: {
          apikey: SERVICE_ROLE,
          Authorization: `Bearer ${SERVICE_ROLE}`,
        },
      },
    );
    const rows = await profileCheck.json();
    if (!Array.isArray(rows) || rows.length === 0) {
      return new Response(JSON.stringify({ error: "profile not found" }), {
        status: 404,
        headers: { ...CORS, "Content-Type": "application/json" },
      });
    }

    const cfg = CONFIG[MODE as "test" | "live"];
    if (!cfg || cfg.productId.startsWith("PLACEHOLDER")) {
      return new Response(JSON.stringify({ error: "product not configured for mode: " + MODE }), {
        status: 500,
        headers: { ...CORS, "Content-Type": "application/json" },
      });
    }

    // Create a checkout session via Dodo's API
    // Per Dodo docs: POST /checkouts (Checkout Sessions endpoint)
    const sessionRes = await fetch(`${cfg.apiBase}/checkouts`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        product_cart: [
          { product_id: cfg.productId, quantity: 1 },
        ],
        customer: {
          email: email,
          name: fullName || email,
        },
        return_url: "https://quantumcube.app/app",
        metadata: {
          user_id: user_id,
          email: email,
        },
      }),
    });

    if (!sessionRes.ok) {
      const errText = await sessionRes.text();
      console.error("Dodo session creation failed:", sessionRes.status, errText);
      return new Response(
        JSON.stringify({ error: "session_creation_failed" }),
        {
          status: 502,
          headers: { ...CORS, "Content-Type": "application/json" },
        },
      );
    }

    const session = await sessionRes.json();

    // Dodo returns { checkout_url, session_id } per their docs
    return new Response(
      JSON.stringify({
        checkout_url: session.checkout_url,
        session_id: session.session_id,
      }),
      {
        status: 200,
        headers: { ...CORS, "Content-Type": "application/json" },
      },
    );
  } catch (e) {
    console.error("dodo-create-session error:", e);
    return new Response(JSON.stringify({ error: "internal_error" }), {
      status: 500,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }
});
