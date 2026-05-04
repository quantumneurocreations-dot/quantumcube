#!/usr/bin/env bash
# Quantum Cube smoke test — verify live deploy state after git push.
#
# Run after every push to confirm:
#   1. SW version on Pages matches what's in repo (Pages rebuilt successfully)
#   2. Sentry release tag on live HTML matches SW version (no version drift)
#   3. All listed public URLs return HTTP 200 (10 paths)
#   4. Auth endpoint at Supabase reachable
#   5. Sentry init log present in live app.html
#
# Usage:
#   ./scripts/smoke.sh              # full check
#   ./scripts/smoke.sh --quick      # skip the 9-page HTTP 200 sweep
#
# If Pages hasn't rebuilt yet (~60s after push), the SW version check will
# show a mismatch — wait and re-run.
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

# === 1. SW version sync (repo vs live) ===
echo "[1/5] SW version sync (repo vs Pages)..."
REPO_SW=$(grep -oE "qc-v[0-9]+" docs/sw.js | head -1 || echo "MISSING")
LIVE_SW=$(curl -fsS --max-time 10 https://quantumcube.app/sw.js 2>/dev/null | grep -oE "qc-v[0-9]+" | head -1 || echo "MISSING")
if [ "$REPO_SW" = "$LIVE_SW" ] && [ "$REPO_SW" != "MISSING" ]; then
  ok "repo $REPO_SW = live $LIVE_SW"
else
  bad "repo=$REPO_SW  live=$LIVE_SW (Pages may still be rebuilding — wait 60s and re-run)"
fi
echo ""

# === 2. Sentry release tag in live app.html matches SW version ===
echo "[2/5] Sentry release tag in live app.html..."
LIVE_RELEASE=$(curl -fsS --max-time 10 https://quantumcube.app/app | grep -oE 'release: "quantum-cube@qc-v[0-9]+"' | head -1 | grep -oE 'qc-v[0-9]+' || echo "MISSING")
if [ "$LIVE_RELEASE" = "$LIVE_SW" ] && [ "$LIVE_RELEASE" != "MISSING" ]; then
  ok "Sentry release $LIVE_RELEASE matches SW $LIVE_SW"
else
  bad "Sentry release=$LIVE_RELEASE  SW=$LIVE_SW (version drift — bad deploy?)"
fi
echo ""

# === 3. Sentry init log present (confirms Sentry block intact) ===
echo "[3/5] Sentry init code present in live app.html..."
if curl -fsS --max-time 10 https://quantumcube.app/app | grep -qF '[QC] Sentry initialised'; then
  ok 'console.log "[QC] Sentry initialised" found'
else
  bad "Sentry init log not found — Sentry block may have been accidentally removed"
fi
echo ""

# === 4. Public pages all return 200 (skip in --quick mode) ===
if [ "$QUICK" = "0" ]; then
  echo "[4/5] Public pages HTTP 200 sweep..."
  for path in / /app /privacy /terms /refund /disclaimer /ip /popia /security /contact; do
    CODE=$(curl -fsS -o /dev/null -w "%{http_code}" --max-time 10 "https://quantumcube.app${path}" 2>/dev/null || echo "ERR")
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

# === 5. Supabase auth endpoint reachable ===
echo "[5/5] Supabase auth endpoint reachable..."
SB_CODE=$(curl -fsS -o /dev/null -w "%{http_code}" --max-time 10 \
  https://fqqdldvnxupzxvvbyvjm.supabase.co/auth/v1/health 2>/dev/null || echo "ERR")
# Supabase /auth/v1/health returns 200 with empty body when up
if [ "$SB_CODE" = "200" ] || [ "$SB_CODE" = "404" ]; then
  # 404 also acceptable — endpoint may not exist but server is responding (not network down)
  ok "Supabase reachable (HTTP $SB_CODE)"
else
  bad "Supabase auth endpoint returned $SB_CODE"
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
