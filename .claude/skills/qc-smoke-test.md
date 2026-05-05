# qc-smoke-test

**When to use:** After every push to `main`, ~60-180 seconds after GitHub Pages would have rebuilt. Also use when something feels off and you want a quick all-clear.

## What it checks

`scripts/smoke.sh` runs four checks:

1. **SW version sync** — repo `docs/sw.js` `qc-vNNN` matches what GitHub Pages is serving at `quantumcube.app/sw.js`. Confirms Pages rebuilt.
2. **Sentry release tag in live HTML** — confirms the Sentry init block is present in the served HTML and tagged with the same `qc-vNNN`. Doubles as "Sentry block intact" — accidentally removing it would also fail this check.
3. **HTTP 200 sweep** — all 10 public pages (`/`, `/app`, `/privacy`, `/terms`, `/refund`, `/disclaimer`, `/ip`, `/popia`, `/security`, `/contact`) return 200.
4. **Supabase reachable** — `https://fqqdldvnxupzxvvbyvjm.supabase.co/auth/v1/health` returns any HTTP code (timeout/refused = down).

## How to run

```bash
cd /Users/qnc/Projects/quantumcube
scripts/smoke.sh           # full check
scripts/smoke.sh --quick   # skip the 10-page sweep (faster, less thorough)
```

## Important: Mac-only

**This script must run from a residential IP (your Mac).** Some sandboxed agent environments may be blocked by edge protections; if you see 403 across the board from a CI/sandbox environment, that's not a real deploy issue — switch surfaces.

The pre-deploy check `.github/workflows/verify-versions.yml` does in-repo version sync (no live URLs), and the post-deploy check `.github/workflows/daily-health-check.yml` runs from GitHub Actions and currently succeeds against the live URLs. If that workflow starts failing with 403s, the cause is likely edge filtering rather than a real outage.

## Failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| SW version mismatch (repo > live) | GitHub Pages still rebuilding | Wait 60-180s, re-run |
| SW version mismatch (live > repo) | Push didn't land | Check `git log origin/main..HEAD` |
| Sentry release mismatch but SW matches | Version drift in repo | New commit fixing the drifting file |
| HTTP 200 fails on `/app` | Pages build broke or HTML invalid | Check repo Actions → "pages build and deployment" run logs |
| HTTP 200 fails on multiple pages | Edge or DNS issue | Check Cloudflare DNS dashboard + GitHub Pages status |
| Supabase unreachable | Supabase outage or project paused | Check Supabase dashboard |
| All checks pass | ✅ Deploy is healthy | Move on |

## After smoke passes

Update `BRIEF_ARCHIVE.md` with the deploy entry if the change was meaningful. Otherwise, just note the commit hash + smoke pass and move on.
