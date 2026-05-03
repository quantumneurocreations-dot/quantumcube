// One-off: re-render welcome.mp3 at slower pace.
// 1) If ELEVENLABS_API_KEY is in .supabase-env or process.env — calls ElevenLabs directly (speed param).
// 2) Else POSTs to the narrate Edge Function with speed: 1.0 (requires deployed narrate that honors `speed`).
import fs from 'node:fs';
const ENV_PATH = '.supabase-env';
const VOICE_ID = 'VhxAIIZM8IRmnl5fyeyk'; // Valory
const MODEL = 'eleven_turbo_v2_5';
const SPEED = 1.0;
const TEXT = 'Welcome to the Quantum Cube, where numbers meet the stars. Enjoy your exploration.';
const OUT_PATH = 'docs/Sounds/Narration/welcome.mp3';

function loadEnv() {
  const raw = fs.readFileSync(ENV_PATH, 'utf8');
  const env = {};
  for (const line of raw.split('\n')) {
    const m = line.match(/^\s*([A-Z_][A-Z0-9_]*)\s*=\s*(.*)\s*$/);
    if (m) env[m[1]] = m[2].replace(/^["']|["']$/g, '');
  }
  if (process.env.ELEVENLABS_API_KEY) env.ELEVENLABS_API_KEY = process.env.ELEVENLABS_API_KEY;
  return env;
}

async function viaElevenLabsDirect(apiKey) {
  const url = `https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}?output_format=mp3_44100_128`;
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'xi-api-key': apiKey, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: TEXT,
      model_id: MODEL,
      voice_settings: { stability: 0.5, similarity_boost: 0.75, speed: SPEED },
    }),
  });
  if (!res.ok) {
    console.error(`HTTP ${res.status}: ${(await res.text()).slice(0, 300)}`);
    process.exit(1);
  }
  return Buffer.from(await res.arrayBuffer());
}

async function viaNarrateEdge(env) {
  if (!env.SUPABASE_URL || !env.SUPABASE_ANON_KEY) {
    throw new Error('.supabase-env missing SUPABASE_URL or SUPABASE_ANON_KEY');
  }
  const url = `${env.SUPABASE_URL.replace(/\/$/, '')}/functions/v1/narrate`;
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      apikey: env.SUPABASE_ANON_KEY,
      Authorization: `Bearer ${env.SUPABASE_ANON_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text: TEXT, voice_id: VOICE_ID, speed: SPEED }),
  });
  if (!res.ok) {
    const errBody = await res.text();
    throw new Error(`narrate HTTP ${res.status}: ${errBody.slice(0, 400)}`);
  }
  return Buffer.from(await res.arrayBuffer());
}

const env = loadEnv();
let buf;
if (env.ELEVENLABS_API_KEY) {
  console.log(`Rendering welcome.mp3 via ElevenLabs API (speed=${SPEED}, ${TEXT.length} chars)...`);
  buf = await viaElevenLabsDirect(env.ELEVENLABS_API_KEY);
} else {
  console.log(`Rendering welcome.mp3 via narrate Edge Function (speed=${SPEED}, ${TEXT.length} chars)...`);
  try {
    buf = await viaNarrateEdge(env);
  } catch (e) {
    console.error(String(e.message || e));
    console.error(
      '\nTip: add ELEVENLABS_API_KEY to .supabase-env, or export it, or deploy narrate with optional speed support then retry.',
    );
    process.exit(1);
  }
}

if (buf.length < 1000) {
  console.error(`Suspiciously small: ${buf.length} bytes`);
  process.exit(1);
}
fs.writeFileSync(OUT_PATH, buf);
console.log(`OK — wrote ${(buf.length / 1024).toFixed(1)} KB to ${OUT_PATH}`);
