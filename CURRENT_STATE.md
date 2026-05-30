---
tags: [core, state]
---
# CURRENT STATE — overwrite this every session end

**Updated:** 2026-05-30 (session 27 — auth/payment deep audit)
**HEAD (QC):** `39ab4b3` — qc-v354 (NOT YET PUSHED — deploy runbook below)
**QC SW:** qc-v354 | **QI server:** localhost:3001 | **has_paid=true:** 7 (real paying: 2)
**Android versionCode:** 5 | **AAB:** versionCode 5 uploaded to Play Console ✅

---

## ⚠️ DEPLOY PENDING — DO IN LOW-TRAFFIC WINDOW (tonight)

8 commits ahead of origin/main. Nothing pushed yet.

### Deploy order (MUST follow — breaking window if out of order)
```bash
# Step 1 — functions FIRST
supabase functions deploy dodo-create-session dodo-webhook --project-ref fqqdldvnxupzxvvbyvjm

# Step 2 — frontend immediately after
git push origin main
```

### After deploy
1. Verify version badge reads `qc-v354 · dodo✓`
2. Do real $17 round-trip test — confirm `profiles.has_paid = true` in Supabase
3. Watch Sentry ~30 min for 401/400s on dodo-create-session
4. Check welcome email arrived via Resend

### Rollback refs
- Pre-v354 function commit: `3822656`
- Frontend revert: `git revert 39ab4b3`

---

## What landed this session (qc-v348–v354)

### Auth/payment fixes (Claude Code audit)
| Version | Severity | Fix |
|---------|----------|-----|
| v348 | CRITICAL | visibilitychange guards — add `_qcOtpVerifying` + `_qcSessionRestored` checks, remove `saveProfileFromForm()` (was writing autofill garbage to DB) |
| v349 | HIGH | Drop `\|\| _emailBlank` from `_isLateRestore` — was re-running full restore on every token refresh |
| v350 | HIGH | Dodo SDK `onload`/`onerror` on script tag — SDK now initialises on arrival, not lazily on first Pay tap |
| v351 | MEDIUM | Fix version badge — `window.Dodo` → `_resolveDodoSdk()` (badge was always showing dodo✗ even when loaded) |
| v352 | MEDIUM | `_qcPostCheckoutHandled` guard — prevent double-fire of post-checkout sync |
| v353 | MEDIUM | `_qcDodoInFlight` 90s safety timeout — prevents permanent latch if overlay closes without emitting terminal event |
| v354 | HIGH (security) | Server-side identity verification — dodo-create-session now verifies JWT via `auth.getUser()`, derives user_id+email server-side, stops trusting request body. Frontend sends real access token instead of anon key. Webhook email fallback hardened. |

### Root cause identified (not yet fixed — tracked)
Three duplicated session-restore paths (initSupabaseSession / onAuthStateChange / visibilitychange) with boolean-flag coordination and no mutex. This is why auth keeps breaking. **Permanent fix = consolidate to one idempotent `_qcRestoreAndNavigate()` function.** Tracked as qc-v355+ task.

---

## Pending — next sessions

### qc-v355 — dispute/chargeback handler (MEDIUM revenue leak)
- `dispute.lost` + `dispute.accepted` → `has_paid = false`
- Dodo event names confirmed: dispute.lost, dispute.accepted (terminal, lost-funds states)
- **Blocked on:** confirm dispute payload shape (where `user_id`/`email` sit) before wiring
- Action: pull real dispute payload from Dodo sandbox or docs, then implement

### Path A/B/C consolidation (permanent auth fix)
- Collapse three duplicated restore paths into one `_qcRestoreAndNavigate()` function
- Replace boolean soup with single `_qcAuthPhase` state variable
- Higher risk, dedicated session — do after deploy confirmed stable

### External Content Links (before publishing to production)
- Enrollment in Play Console
- Disclosure modal in IS_TWA unlock flow (PLAY_STORE_PREP §15a + §15b)

---

## Sentry
- ✅ JAVASCRIPT-8, 16, 18 resolved
- 🟡 JAVASCRIPT-3 — CSP blocking Clarity img — low priority backlog

---

## Recent commits
- `39ab4b3` — qc-v354: server-side identity verification (security)
- `3822656` — qc-v353: _qcDodoInFlight 90s safety timeout
- `14478a3` — qc-v352: dedupe post-checkout double-fire
- `60ea1f8` — qc-v351: version badge fix
- `4eb8d83` — qc-v350: Dodo SDK onload/onerror
- `8820622` — qc-v349: drop _emailBlank from _isLateRestore
- `bb62ec1` — qc-v348: visibilitychange auth race (CRITICAL)
