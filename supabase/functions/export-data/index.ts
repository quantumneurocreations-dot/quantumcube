import { serve } from "https://deno.land/std@0.192.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.4";

// POPIA / GDPR right of access — returns the user's profile data as JSON.
// User-scoped via JWT verification; cannot return another user's data.

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

  const authHeader = req.headers.get("authorization") || "";
  const jwt = authHeader.replace(/^Bearer\s+/i, "");
  if (!jwt) {
    return new Response(JSON.stringify({ error: "missing_auth" }), {
      status: 401,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }

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

  const { data: profile, error: profileErr } = await sb
    .from("profiles")
    .select("id, email, has_paid, marketing_consent, created_at")
    .eq("id", user.id)
    .single();

  if (profileErr) {
    console.error(`export-data: query failed for ${user.id}:`, profileErr);
    return new Response(JSON.stringify({ error: "query_failed" }), {
      status: 500,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }

  const exportPayload = {
    export_generated_at: new Date().toISOString(),
    account: {
      user_id: profile.id,
      email: profile.email,
      account_created_at: profile.created_at,
      has_paid: profile.has_paid,
      marketing_consent: profile.marketing_consent,
    },
    note:
      "This export contains all personal data Quantum Cube stores about your account. Reading content (numerology, astrology, zodiac) is generated deterministically from your name and date of birth at runtime and is not stored on our servers.",
  };

  return new Response(JSON.stringify(exportPayload, null, 2), {
    status: 200,
    headers: {
      ...CORS,
      "Content-Type": "application/json",
      "Content-Disposition": `attachment; filename="quantum-cube-data-${user.id}.json"`,
    },
  });
});
