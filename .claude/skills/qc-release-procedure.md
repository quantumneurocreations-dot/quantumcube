# qc-release-procedure

**When to use:** Any time you're shipping a change to production (`docs/` or edge functions). This is the canonical end-to-end deploy flow.

## Pre-flight

1. **Boot sequence run?** Confirm tools loaded, repo clean, versions in sync (per `CHAT_KICKOFF.md`).
2. **Working tree clean?** `git status --short` — empty.
3. **Read recon for the area you're touching.** Grep for the function/section first; never edit blind.

## The flow

### 1. Branch policy

Solo dev, single product — work directly on `main`. No feature branches unless the change is multi-day or risky (auth, paywall, schema migration). For risky changes, branch + PR + let CI run.

### 2. Make the edit

- Read the section first (`grep -n` for the anchor function or marker).
- Match existing code style — comment density, naming, indentation.
- If the change touches `docs/app.html` or `docs/sw.js` and alters served output → see `qc-version-bump.md` and bump the version in the same commit.

### 3. Pre-commit verification

For changes touching `docs/app.html` or `docs/sw.js`:
```bash
cd /Users/qnc/Projects/quantumcube
SW_VER=$(grep -oE "qc-v[0-9]+" docs/sw.js | head -1)
APP_VER=$(grep -oE "quantum-cube@qc-v[0-9]+" docs/app.html | head -1 | sed 's/quantum-cube@//')
[ "$SW_VER" = "$APP_VER" ] && echo "✓ in sync at $SW_VER" || { echo "✗ DRIFT — abort"; exit 1; }
```

For edge function changes:
```bash
deno check supabase/functions/<name>/index.ts
```

### 4. Commit + push

```bash
git add -A
git diff --cached --stat   # eyeball — anything unexpected?
git diff --cached | grep -iE "sk_|service_role|xoxb-|bearer " || echo "✓ no obvious secrets"
git commit -m "<type>(<scope>): <imperative summary>"
git push origin main
```

Conventional commits: `feat`, `fix`, `chore`, `docs`, `refactor`, `style`, `perf`. Scope = file/area (e.g. `narrate`, `paywall`, `cube`, `version`).

### 5. Verify deploy

GitHub Pages picks up commits to `main`'s `/docs` folder automatically (typically ~60-180s for the build workflow to complete). Then:

```bash
scripts/smoke.sh
```

If smoke fails on SW version mismatch → wait another 60s and re-run. Pages can take up to ~3min on slow days.

If smoke fails on Sentry release mismatch after SW matches → version drift in repo. Roll forward with a fix commit, don't roll back.

If smoke fails on HTTP 200 sweep → real breakage. See `qc-incident-response.md`.

### 6. Edge function deploy (if applicable)

Edge functions don't auto-deploy from git. Deploy explicitly:

```bash
cd /Users/qnc/Projects/quantumcube
supabase functions deploy <function-name>
```

(Project is pre-linked — no `--linked` flag needed on CLI v2.90. v2.95+ requires it.)

Verify via Supabase MCP `execute_sql` or by hitting the function URL directly with a test payload.

### 7. Document

If the change is meaningful (new feature, bugfix, config change):
- Append a one-line entry to `BRIEF_ARCHIVE.md` under today's session.
- If it's an architectural decision, add an ADR entry to `DECISIONS.md`.
- If it changes how you work in chat, update `CHAT_KICKOFF.md` (and bump its version).

These doc updates can ride in the same commit as the code change OR be a follow-up commit — both are fine.

## What NOT to do

- Never `git push --force` to `main`.
- Never deploy with a dirty working tree (uncommitted changes).
- Never deploy edge functions without checking they compile locally first.
- Never bump SW version "to be safe" if served output didn't change — wastes user bandwidth.
- Never skip the smoke test "because it's a small change."
