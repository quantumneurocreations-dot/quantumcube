#!/usr/bin/env bash
# Quantum Cube smoke test — verify live deploy state after git push.
#
# Run after every push to confirm:
#   1. SW version on Pages matches what's in repo (Pages rebuilt successfully)
#   2. Sentry release tag on live HTML matches SW version (no version drift)
#   3. Sentry DSN present in live app.html (Sentry block intact)
#   4. All 10 public pages return HTTP 200
#   5. Supabase reachable (any HTTP response = up; timeout/refused = down)
#
# Usage:
#   ./scripts/smoke.sh              # full check
#   ./scripts/smoke.sh --quick      # skip the 10-page HTTP 200 sweep
#
# If Pages hasn't rebuilt yet (~60s after push), the SW version check will
# show a mismatch — wait and re-run.
#
# NOTE: Run this from your Mac (residential IP). Cloudflare blocks
# datacenter curl with HTTP 403; if running from a sandboxed agent, expect
# 403 across the board — that's not a real deploy issue.
set -uo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

QUICK=0
[ "${1:-}" = "--quick" ] && QUICK=1

PASS=0
FAIL=0
WARN=0

ok()   { echo "  ✓ $1"; PASS=$((PASS+1)); }
bad()  { echo "  ✗ $1"; FAIL=$((FAIL+1)); }
warn() { echo "  ⚠ $1"; WARN=$((WARN+1)); }

echo "=== Quantum Cube smoke test ==="
echo ""

# Buffer live responses ONCE — avoids SIGPIPE issues with grep -q on pipes
# under set -o pipefail. Re-used by checks 1, 2, 3.
LIVE_APP_HTML=$(curl -fsS --max-time 15 https://quantumcube.app/app 2>/dev/null || echo "")
LIVE_SW_JS=$(curl -fsS --max-time 15 https://quantumcube.app/sw.js 2>/dev/null || echo "")

# === 1. SW version sync (repo vs live) ===
echo "[1/5] SW version sync (repo vs Pages)..."
REPO_SW=$(grep -oE "qc-v[0-9]+" docs/sw.js | head -1 || echo "MISSING")
LIVE_SW=$(echo "$LIVE_SW_JS" | grep -oE "qc-v[0-9]+" | head -1 || echo "MISSING")
if [ "$REPO_SW" = "$LIVE_SW" ] && [ "$REPO_SW" != "MISSING" ]; then
  ok "repo $REPO_SW = live $LIVE_SW"
else
  bad "repo=$REPO_SW  live=$LIVE_SW (Pages may still be rebuilding — wait 60s and re-run)"
fi
echo ""

# === 2. Sentry release tag in live app.html matches SW version ===
echo "[2/5] Sentry release tag in live app.html..."
LIVE_RELEASE=$(echo "$LIVE_APP_HTML" | grep -oE 'release: "quantum-cube@qc-v[0-9]+"' | head -1 | grep -oE 'qc-v[0-9]+' || echo "MISSING")
if [ "$LIVE_RELEASE" = "$LIVE_SW" ] && [ "$LIVE_RELEASE" != "MISSING" ]; then
  ok "Sentry release $LIVE_RELEASE matches SW $LIVE_SW"
else
  bad "Sentry release=$LIVE_RELEASE  SW=$LIVE_SW (version drift — bad deploy?)"
fi
echo ""

# === 3. Sentry DSN present (confirms Sentry block intact) ===
# Greps for the DSN host — uniquely identifies the Sentry init block.
# More reliable than grepping a console.log string that might or might
# not exist depending on production guards. If the Sentry block is
# accidentally removed, the DSN goes with it.
echo "[3/5] Sentry DSN present in live app.html..."
if echo "$LIVE_APP_HTML" | grep -qF "o4511330222604288.ingest.de.sentry.io"; then
  ok "Sentry DSN found"
else
  bad "Sentry DSN not found — Sentry block may have been accidentally removed"
fi
echo ""

# === 4. Public pages all return 200 (skip in --quick mode) ===
if [ "$QUICK" = "0" ]; then
  echo "[4/5] Public pages HTTP 200 sweep..."
  for path in / /app /privacy /terms /refund /disclaimer /ip /popia /security /contact; do
    CODE=$(curl -sS -o /dev/null -w "%{http_code}" --max-time 10 "https://quantumcube.app${path}" 2>/dev/null || echo "ERR")
    if [ "$CODE" = "200" ]; then
      ok "${path} → 200"
    else
      bad "${path} → ${CODE}"
    fi
  done
else
  warn "[4/5] HTTP 200 sweep skipped (--quick)"
fi
echo ""

# === 5. Supabase reachable (any HTTP response = up) ===
# /auth/v1/health requires apikey header to return 200; without it returns
# 401. Either way, the server is up. Only timeout / connection refused /
# DNS failure (curl returns empty body, exit non-zero) means it's down.
echo "[5/5] Supabase reachable..."
SB_CODE=$(curl -sS -o /dev/null -w "%{http_code}" --max-time 10 \
  https://fqqdldvnxupzxvvbyvjm.supabase.co/auth/v1/health 2>/dev/null || echo "")
if [ -n "$SB_CODE" ] && [ "$SB_CODE" != "000" ]; then
  ok "Supabase reachable (HTTP $SB_CODE)"
else
  bad "Supabase unreachable (timeout, DNS, or connection refused)"
fi
echo ""

# === Summary ===
echo "=== summary ==="
echo "  passed: $PASS"
echo "  failed: $FAIL"
[ "$WARN" -gt 0 ] && echo "  warnings: $WARN"
echo ""

if [ "$FAIL" -gt 0 ]; then
  echo "✗ smoke test FAILED — $FAIL check(s) failing. Investigate before declaring deploy good."
  exit 1
else
  echo "✓ smoke test PASSED — live deploy looks healthy."
  exit 0
fi
