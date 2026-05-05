# qc-version-bump

**When to use:** Before any commit that touches `docs/app.html` or `docs/sw.js` in a way that changes served HTML/JS or cached assets.

**Why this exists:** Two values must stay in lockstep:
1. `docs/sw.js` line 1: `const CACHE='qc-vNNN'`
2. `docs/app.html` Sentry init: `release: "quantum-cube@qc-vNNN"`

If they drift, two bad things happen:
- Users keep seeing the old cached HTML (SW won't activate new cache)
- Sentry tags errors with the wrong release (debugging nightmare)

The CI workflow `.github/workflows/verify-versions.yml` blocks drift before deploy. The daily-health-check workflow catches drift after deploy as a second line of defense. Both should pass green.

## Procedure

1. **Pre-stage check** — confirm current sync:
   ```bash
   cd /Users/qnc/Projects/quantumcube
   SW_VER=$(grep -oE "qc-v[0-9]+" docs/sw.js | head -1)
   APP_VER=$(grep -oE "quantum-cube@qc-v[0-9]+" docs/app.html | head -1 | sed 's/quantum-cube@//')
   echo "SW: $SW_VER  |  APP: $APP_VER"
   ```
   They must be equal before you change anything. If they're not, fix the drift first as a separate commit.

2. **Decide the new version** — increment the integer: `qc-v201` → `qc-v202`. No skipping. No semver — single integer.

3. **Update both files in the same commit:**
   - `docs/sw.js`: `const CACHE='qc-vNEW'`
   - `docs/app.html`: `release: "quantum-cube@qc-vNEW"` (find via `grep -n "quantum-cube@qc-v" docs/app.html`)

4. **Re-verify before commit:**
   ```bash
   SW_VER=$(grep -oE "qc-v[0-9]+" docs/sw.js | head -1)
   APP_VER=$(grep -oE "quantum-cube@qc-v[0-9]+" docs/app.html | head -1 | sed 's/quantum-cube@//')
   [ "$SW_VER" = "$APP_VER" ] && echo "✓ in sync at $SW_VER" || echo "✗ DRIFT — abort"
   ```

5. **Commit message format:** `chore(version): bump to qc-vNEW — <reason>`. Example: `chore(version): bump to qc-v202 — wire PostHog product analytics`.

6. **Post-push:** wait ~60s, run `scripts/smoke.sh` to confirm Pages picked up the new version and live SW matches repo SW.

## When NOT to bump

- Pure backend changes (edge functions, migrations) — they don't touch served HTML/JS, no bump needed.
- Doc-only changes (README, kickoff, briefs) — no bump.
- `.github/workflows/*` changes — no bump.
- `scripts/*` changes — no bump.

## Common mistakes

- Bumping one file but not the other (CI will catch this, but it wastes a push).
- Skipping numbers (`qc-v201` → `qc-v203`) — keep it sequential for grep simplicity.
- Bumping without a real reason — every bump invalidates user caches and forces re-download. Don't bump cosmetically.
