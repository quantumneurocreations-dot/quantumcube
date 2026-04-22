// scripts/extract-narration.mjs
// Extracts numerology narration text from quantum-cube-v10.html into a manifest.
// Phase 1: numerology (lp, bd, ex, su, pe, hp, kl, py) + welcome greeting.
// Each entry carries a sha256 of the exact text sent for TTS — runtime can
// verify MP3 matches current card text and fall back to live TTS on mismatch.

import fs from 'node:fs';
import crypto from 'node:crypto';

const HTML_PATH = 'quantum-cube-v10.html';
const MANIFEST_PATH = 'narration-manifest.json';

const CAT_LABELS = {
  lp: 'Life Path',
  bd: 'Birthday Number',
  ex: 'Expression',
  su: 'Soul Urge',
  pe: 'Personality',
  hp: 'Hidden Passion',
  kl: 'Karmic Lessons',
  py: 'Personal Year',
};

function extractBalancedLiteral(src, startPattern) {
  const m = src.match(startPattern);
  if (!m) throw new Error(`start pattern not found: ${startPattern}`);
  const openIdx = m.index + m[0].lastIndexOf('{');
  let depth = 0, inStr = false, strCh = '';
  for (let i = openIdx; i < src.length; i++) {
    const ch = src[i];
    if (inStr) {
      if (ch === '\\') { i++; continue; }
      if (ch === strCh) inStr = false;
      continue;
    }
    if (ch === '"' || ch === "'" || ch === '`') { inStr = true; strCh = ch; continue; }
    if (ch === '/' && src[i+1] === '/') { while (i < src.length && src[i] !== '\n') i++; continue; }
    if (ch === '/' && src[i+1] === '*') {
      i += 2;
      while (i < src.length - 1 && !(src[i] === '*' && src[i+1] === '/')) i++;
      i++;
      continue;
    }
    if (ch === '{') depth++;
    else if (ch === '}') { depth--; if (depth === 0) return src.slice(openIdx, i + 1); }
  }
  throw new Error('unbalanced braces — parser failed');
}

function buildNarration(label, body) {
  const clean = String(body || '').replace(/\s+/g, ' ').trim();
  return `${label}. ${clean}`.replace(/\s+/g, ' ').trim();
}

function sha256(s) {
  return crypto.createHash('sha256').update(s, 'utf8').digest('hex');
}

const src = fs.readFileSync(HTML_PATH, 'utf8');
const numLit = extractBalancedLiteral(src, /const\s+NUM\s*=\s*\{/);
const NUM = new Function(`return ${numLit};`)();

const manifest = [];

const welcomeText = 'Welcome to the Quantum Cube, where numbers meet the stars. Enjoy your exploration.';
manifest.push({
  filename: 'welcome.mp3',
  group: 'welcome',
  text: welcomeText,
  sha256: sha256(welcomeText),
});

const counts = { welcome: 1 };
let skipped = 0;

for (const [cat, label] of Object.entries(CAT_LABELS)) {
  const data = NUM[cat];
  if (!data) { console.warn(`NUM.${cat} missing - skipped`); continue; }
  counts[cat] = 0;
  for (const [num, variants] of Object.entries(data)) {
    if (!Array.isArray(variants)) { skipped++; continue; }
    variants.forEach((body, i) => {
      const text = buildNarration(label, body);
      manifest.push({
        filename: `num_${cat}_${num}_v${i + 1}.mp3`,
        group: cat,
        num,
        variant: i + 1,
        text,
        sha256: sha256(text),
      });
      counts[cat]++;
    });
  }
}

fs.writeFileSync(MANIFEST_PATH, JSON.stringify(manifest, null, 2));

const totalChars = manifest.reduce((n, r) => n + r.text.length, 0);
console.log(`Manifest: ${MANIFEST_PATH}`);
console.log(`Total clips: ${manifest.length}`);
console.log(`Total chars: ${totalChars}`);
console.log(`By group:`);
for (const [g, n] of Object.entries(counts)) console.log(`  ${g}: ${n}`);
if (skipped) console.log(`Skipped (non-array entries): ${skipped}`);

// Top-15 longest — use this list to pick the dry-run candidates
console.log(`\nTop 15 longest clips (dry-run candidates):`);
[...manifest]
  .sort((a, b) => b.text.length - a.text.length)
  .slice(0, 15)
  .forEach(r => console.log(`  ${r.text.length}  ${r.filename}`));
