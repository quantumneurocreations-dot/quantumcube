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

const API_KEY = Deno.env.get("DODO_PAYMENTS_API_KEY") ?? "";
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const ANON_KEY = Deno.env.get("SUPABASE_ANON_KEY")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

// Mode + product config — kept in sync with frontend DODO_MODE
const MODE = "test"; // flip to "live" for production
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

  // Manual JWT-style auth via apikey header (consistent with narrate function)
  const apikey = req.headers.get("apikey") || req.headers.get("authorization")?.replace(/^Bearer\s+/i, "");
  if (!apikey || apikey !== ANON_KEY) {
    return new Response(JSON.stringify({ error: "unauthorized" }), {
      status: 401,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }

  try {
    const body = await req.json();
    const { user_id, email, fullName } = body || {};

    if (!user_id || !email) {
      return new Response(JSON.stringify({ error: "missing user_id or email" }), {
        status: 400,
        headers: { ...CORS, "Content-Type": "application/json" },
      });
    }

    // Verify the user_id actually exists in profiles (defence-in-depth)
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
        JSON.stringify({ error: "session creation failed", status: sessionRes.status, detail: errText }),
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
    return new Response(JSON.stringify({ error: String(e) }), {
      status: 500,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }
});
