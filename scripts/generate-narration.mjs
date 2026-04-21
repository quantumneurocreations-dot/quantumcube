// scripts/generate-narration.mjs
// Reads narration-manifest.json, POSTs each entry to the narrate Edge Function,
// saves response as MP3 to Sounds/Narration/.
// Sequential, 500ms throttle between requests, resumable (skips existing files).
//
// Usage:
//   node scripts/generate-narration.mjs                 # generate all missing
//   node scripts/generate-narration.mjs --limit 15      # first 15 from manifest
//   node scripts/generate-narration.mjs --longest 15    # 15 longest clips
//   node scripts/generate-narration.mjs --dry           # list planned work, no calls

import fs from 'node:fs';
import path from 'node:path';

const MANIFEST_PATH = 'narration-manifest.json';
const OUTPUT_DIR = 'Sounds/Narration';
const ENV_PATH = '.supabase-env';
const VOICE_ID = 'VhxAIIZM8IRmnl5fyeyk'; // Valory
const THROTTLE_MS = 500;

function parseArgs() {
  const args = process.argv.slice(2);
  const out = { limit: null, longest: null, dry: false };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--limit') out.limit = parseInt(args[++i], 10);
    else if (args[i] === '--longest') out.longest = parseInt(args[++i], 10);
    else if (args[i] === '--dry') out.dry = true;
  }
  return out;
}

function loadEnv() {
  const raw = fs.readFileSync(ENV_PATH, 'utf8');
  const env = {};
  for (const line of raw.split('\n')) {
    const m = line.match(/^\s*([A-Z_][A-Z0-9_]*)\s*=\s*(.*)\s*$/);
    if (m) env[m[1]] = m[2].replace(/^["']|["']$/g, '');
  }
  if (!env.SUPABASE_URL || !env.SUPABASE_ANON_KEY) {
    throw new Error('.supabase-env missing SUPABASE_URL or SUPABASE_ANON_KEY');
  }
  return env;
}

async function generateOne(url, apikey, row) {
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'apikey': apikey,
      'Authorization': `Bearer ${apikey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text: row.text, voice_id: VOICE_ID }),
  });
  if (!res.ok) {
    const errBody = await res.text();
    throw new Error(`HTTP ${res.status}: ${errBody.slice(0, 300)}`);
  }
  const buf = Buffer.from(await res.arrayBuffer());
  if (buf.length < 1000) {
    throw new Error(`suspiciously small response: ${buf.length} bytes`);
  }
  return buf;
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

(async () => {
  const args = parseArgs();
  const env = loadEnv();
  const NARRATE_URL = `${env.SUPABASE_URL.replace(/\/$/, '')}/functions/v1/narrate`;

  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  let manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
  if (args.longest) {
    manifest = [...manifest].sort((a, b) => b.text.length - a.text.length).slice(0, args.longest);
  } else if (args.limit) {
    manifest = manifest.slice(0, args.limit);
  }

  const todo = manifest.filter(r => !fs.existsSync(path.join(OUTPUT_DIR, r.filename)));
  const skipped = manifest.length - todo.length;
  const totalChars = todo.reduce((n, r) => n + r.text.length, 0);

  console.log(`Endpoint: ${NARRATE_URL}`);
  console.log(`Output:   ${OUTPUT_DIR}/`);
  console.log(`Planned:  ${todo.length} clips  (${totalChars} chars ≈ ${totalChars} credits)`);
  if (skipped) console.log(`Skipped:  ${skipped} already on disk`);
  if (args.dry) { console.log('\nDry mode — no requests made. Planned files:');
    todo.forEach(r => console.log(`  ${r.text.length}  ${r.filename}`));
    return;
  }

  let ok = 0, fail = 0;
  const failures = [];
  for (let i = 0; i < todo.length; i++) {
    const row = todo[i];
    const outPath = path.join(OUTPUT_DIR, row.filename);
    const tag = `[${i + 1}/${todo.length}]`;
    process.stdout.write(`${tag} ${row.filename}  (${row.text.length} chars) ... `);
    try {
      const buf = await generateOne(NARRATE_URL, env.SUPABASE_ANON_KEY, row);
      fs.writeFileSync(outPath, buf);
      console.log(`OK ${(buf.length/1024).toFixed(1)}KB`);
      ok++;
    } catch (e) {
      console.log(`FAIL — ${e.message}`);
      fail++;
      failures.push({ filename: row.filename, error: e.message });
    }
    if (i < todo.length - 1) await sleep(THROTTLE_MS);
  }

  console.log(`\nDone. OK: ${ok}  FAIL: ${fail}`);
  if (failures.length) {
    console.log('Failures:');
    failures.forEach(f => console.log(`  ${f.filename} — ${f.error}`));
  }
})().catch(e => { console.error('Fatal:', e.message); process.exit(1); });
