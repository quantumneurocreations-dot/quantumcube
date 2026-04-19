import { serve } from "https://deno.land/std@0.192.0/http/server.ts";

const KEY = Deno.env.get("ELEVENLABS_API_KEY")!;
const EXPECTED_APIKEY = Deno.env.get("SUPABASE_ANON_KEY")!;
const MODEL = "eleven_turbo_v2_5";
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return new Response("Method not allowed", { status: 405, headers: CORS });

  const apikey = req.headers.get("apikey") || req.headers.get("authorization")?.replace(/^Bearer\s+/i, "");
  if (!apikey || apikey !== EXPECTED_APIKEY) {
    return new Response(JSON.stringify({error:"unauthorized"}), { status: 401, headers: {...CORS,"Content-Type":"application/json"} });
  }

  try {
    const { text, voice_id } = await req.json();
    if (!text || !voice_id) return new Response(JSON.stringify({error:"missing text or voice_id"}), { status: 400, headers: {...CORS,"Content-Type":"application/json"} });
    if (text.length > 2500) return new Response(JSON.stringify({error:"text too long"}), { status: 400, headers: {...CORS,"Content-Type":"application/json"} });
    const r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voice_id}`, {
      method: "POST",
      headers: { "xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg" },
      body: JSON.stringify({ text, model_id: MODEL, voice_settings: { stability: 0.5, similarity_boost: 0.75 } }),
    });
    if (!r.ok) {
      const err = await r.text();
      return new Response(JSON.stringify({error:"elevenlabs failed",detail:err}), { status: r.status, headers: {...CORS,"Content-Type":"application/json"} });
    }
    return new Response(r.body, { status: 200, headers: {...CORS,"Content-Type":"audio/mpeg"} });
  } catch (e) {
    return new Response(JSON.stringify({error:String(e)}), { status: 500, headers: {...CORS,"Content-Type":"application/json"} });
  }
});
