#!/usr/bin/env node
/**
 * QI — Quantum Integrator Server
 * Runs on localhost:3001, serves the dashboard + proxies API calls.
 * Launch: node scripts/qi-server.js
 */

const http  = require('http');
const https = require('https');
const fs    = require('fs');
const path  = require('path');
const url   = require('url');

const PORT    = 3001;
let QI_SPEAKING = false;  // set by voice script via POST /api/speaking
const DASH    = path.join(__dirname, 'qi-dashboard.html');

// ── Keys (loaded from ~/.config/qi/) ─────────────────────────────────────────
const readKey = f => { try { return fs.readFileSync(path.join(process.env.HOME,'.config','qi',f),'utf8').trim(); } catch{ return ''; } };

const SUPABASE_URL  = 'https://auth.quantumcube.app';
const SUPABASE_KEY  = readKey('supabase_service_role') || process.env.SUPABASE_SERVICE_ROLE_KEY;
const POSTHOG_KEY   = readKey('posthog_api_key')       || process.env.POSTHOG_API_KEY;
const SENTRY_TOKEN  = readKey('sentry_auth_token')     || process.env.SENTRY_AUTH_TOKEN;

const GOAL_DATE     = new Date('2026-08-15');
const GOAL_CUST     = 500;
const PRICE         = 17;

// ── Fetch helpers ─────────────────────────────────────────────────────────────
function fetchJson(reqUrl, opts = {}) {
  return new Promise((resolve) => {
    const parsed = new URL(reqUrl);
    const options = {
      hostname: parsed.hostname,
      path: parsed.pathname + parsed.search,
      method: opts.method || 'GET',
      headers: opts.headers || {},
    };
    const req = https.request(options, res => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => { try { resolve(JSON.parse(data)); } catch { resolve({ error: data }); } });
    });
    req.on('error', e => resolve({ error: e.message }));
    if (opts.body) req.write(JSON.stringify(opts.body));
    req.end();
  });
}

// ── Data sources ──────────────────────────────────────────────────────────────
async function getCustomers() {
  if (!SUPABASE_KEY) return { total: null, today: null, week: null };
  const now      = new Date();
  const dayAgo   = new Date(now - 864e5).toISOString();
  const weekAgo  = new Date(now - 6048e5).toISOString();
  const rows = await fetchJson(
    `${SUPABASE_URL}/rest/v1/profiles?select=created_at&has_paid=eq.true`,
    { headers: { apikey: SUPABASE_KEY, Authorization: `Bearer ${SUPABASE_KEY}` } }
  );
  if (!Array.isArray(rows)) return { total: null, today: null, week: null };
  return {
    total: rows.length,
    today: rows.filter(r => r.created_at >= dayAgo).length,
    week:  rows.filter(r => r.created_at >= weekAgo).length,
  };
}

async function getSessions() {
  if (!POSTHOG_KEY) return { sessions: null, pageviews: null };
  const body = {
    query: {
      kind: 'HogQLQuery',
      query: `SELECT count(DISTINCT properties.$session_id) as s, count() as pv
              FROM events
              WHERE event = '$pageview'
                AND properties.$current_url LIKE '%quantumcube.app/app%'
                AND timestamp >= now() - INTERVAL 1 DAY`
    }
  };
  const r = await fetchJson('https://eu.posthog.com/api/projects/172921/query/', {
    method: 'POST',
    headers: { Authorization: `Bearer ${POSTHOG_KEY}`, 'Content-Type': 'application/json' },
    body
  });
  try { return { sessions: r.results[0][0], pageviews: r.results[0][1] }; }
  catch { return { sessions: null, pageviews: null }; }
}

async function getSentry() {
  if (!SENTRY_TOKEN) return { count: null, top: null };
  const since = new Date(Date.now() - 864e5).toISOString();
  const r = await fetchJson(
    `https://sentry.io/api/0/projects/quantum-neuro-creations/javascript/issues/?query=firstSeen:>${since}&limit=5`,
    { headers: { Authorization: `Bearer ${SENTRY_TOKEN}` } }
  );
  if (!Array.isArray(r)) return { count: null, top: null };
  return { count: r.length, top: r[0]?.title || null };
}

// ── Play Store stats ──────────────────────────────────────────────────────────
const { execSync } = require('child_process');
function getPlayStats() {
  try {
    const out = execSync(
      'python3 /Users/qnc/Projects/quantumcube/scripts/qi-play-stats.py',
      { timeout: 10000, encoding: 'utf8' }
    );
    return JSON.parse(out);
  } catch (e) {
    return { installs: null, testers: null, error: 'unavailable' };
  }
}

// ── Briefing builder ──────────────────────────────────────────────────────────
async function buildBriefing() {
  const [cust, sessions, sentry] = await Promise.all([getCustomers(), getSessions(), getSentry()]);
  const play = getPlayStats();
  const daysLeft  = Math.max(0, Math.ceil((GOAL_DATE - new Date()) / 864e5));
  const remaining = GOAL_CUST - (cust.total || 0);
  const runRate   = daysLeft > 0 ? (remaining / daysLeft).toFixed(1) : '0';
  const revenue   = cust.total != null ? cust.total * PRICE : null;
  const pct       = cust.total != null ? Math.round((cust.total / GOAL_CUST) * 100) : 0;

  let action = '';
  if (cust.total != null && cust.total < 12) action = 'Chase tester opt-ins — nothing else matters until the 14-day clock starts.';
  else if (sentry.count) action = `Fix Sentry: ${sentry.top}`;
  else if (sessions.sessions != null && sessions.sessions < 50) action = 'Traffic is low — push one organic post or activate an ad today.';
  else action = 'Everything healthy — run a paid ad test and measure the ROAS.';

  return {
    date: new Date().toLocaleDateString('en-ZA', { weekday:'long', day:'numeric', month:'long' }),
    customers: cust,
    revenue,
    goal: { target: GOAL_CUST, pct, daysLeft, runRate },
    sessions,
    sentry,
    play,
    action,
    keys: {
      supabase: !!SUPABASE_KEY,
      posthog:  !!POSTHOG_KEY,
      sentry:   !!SENTRY_TOKEN,
    }
  };
}

// ── HTTP server ───────────────────────────────────────────────────────────────
const server = http.createServer(async (req, res) => {
  const { pathname } = url.parse(req.url);

  if (pathname === '/api/briefing') {
    try {
      const data = await buildBriefing();
    data.speaking = QI_SPEAKING;
      res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
      res.end(JSON.stringify(data));
    } catch(e) {
      res.writeHead(500); res.end(JSON.stringify({ error: e.message }));
    }
    return;
  }

  if (pathname === '/api/speaking') {
    if (req.method === 'POST') {
      const u = new URL(req.url, 'http://localhost');
      QI_SPEAKING = u.searchParams.get('state') === 'true';
      res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
      res.end(JSON.stringify({ speaking: QI_SPEAKING }));
    } else {
      res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
      res.end(JSON.stringify({ speaking: QI_SPEAKING }));
    }
    return;
  }

  // Serve dashboard
  fs.readFile(DASH, (err, data) => {
    if (err) { res.writeHead(404); res.end('qi-dashboard.html not found'); return; }
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(data);
  });
});

server.listen(PORT, () => {
  console.log(`\n  ██████╗ ██╗`);
  console.log(`  ██╔═══██╗██║`);
  console.log(`  ██║   ██║██║`);
  console.log(`  ██║▄▄ ██║██║`);
  console.log(`  ╚██████╔╝██║`);
  console.log(`   ╚══▀▀═╝ ╚═╝  QUANTUM INTEGRATOR\n`);
  console.log(`  Dashboard →  http://localhost:${PORT}`);
  console.log(`  API       →  http://localhost:${PORT}/api/briefing`);
  console.log(`  Keys:  Supabase ${SUPABASE_KEY?'✓':'✗'}  PostHog ${POSTHOG_KEY?'✓':'✗'}  Sentry ${SENTRY_TOKEN?'✓':'✗'}\n`);
});
