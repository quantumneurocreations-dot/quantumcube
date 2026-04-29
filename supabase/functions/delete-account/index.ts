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
  console.log(`delete-account: deleting user_id=${userId} at ${new Date().toISOString()}`);

  // Admin delete — cascades to public.profiles via on-delete-cascade FK
  const { error: deleteErr } = await sb.auth.admin.deleteUser(userId);
  if (deleteErr) {
    console.error(`delete-account: admin delete failed for ${userId}:`, deleteErr);
    return new Response(
      JSON.stringify({ error: "delete_failed", detail: deleteErr.message }),
      { status: 500, headers: { ...CORS, "Content-Type": "application/json" } },
    );
  }

  console.log(`delete-account: success user_id=${userId}`);
  return new Response(JSON.stringify({ success: true }), {
    status: 200,
    headers: { ...CORS, "Content-Type": "application/json" },
  });
});
