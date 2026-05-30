---
tags: [core, state]
---
# CURRENT STATE — overwrite this every session end

**Updated:** 2026-05-30 (session 27 — auth/payment deep audit + deploy)
**HEAD (QC):** `2a339fd` — qc-v355 cold-start blank page rescue ✅ PUSHED
**QC SW:** qc-v355 | **QI server:** localhost:3001 | **has_paid=true:** 7 (real paying: 2)
**Android versionCode:** 5 | **AAB:** versionCode 5 uploaded to Play Console ✅

---

## ✅ DEPLOYED — qc-v348 → qc-v355

Both edge functions + frontend live. $17 round-trip test passed — has_paid flipped ✅

---

## What shipped this session

| Version | Severity | Fix |
|---------|----------|-----|
| v348 | CRITICAL | visibilitychange guards — `_qcOtpVerifying` + `_qcSessionRestored`, removed `saveProfileFromForm()` (DB corruption vector) |
| v349 | HIGH | Drop `\|\| _emailBlank` from `_isLateRestore` — was re-running full restore on every token refresh |
| v350 | HIGH | Dodo SDK `onload`/`onerror` — SDK initialises on arrival, not lazily on first Pay tap |
| v351 | MEDIUM | Version badge fix — `window.Dodo` → `_resolveDodoSdk()` (badge was always lying) |
| v352 | MEDIUM | `_qcPostCheckoutHandled` — prevent double-fire of post-checkout sync |
| v353 | MEDIUM | `_qcDodoInFlight` 90s safety timeout — prevents permanent latch |
| v354 | HIGH security | Server-side identity verification — dodo-create-session now verifies JWT, derives identity server-side. Frontend sends real access token. Webhook email fallback hardened. |
| v355 | HIGH | Cold-start blank page rescue (Sentry JAVASCRIPT-8, since v324) — stranded face-0 now re-runs force-populate + runCalculation instead of giving up |

---

## Root cause identified — NOT YET FIXED (tracked)

Three duplicated session-restore paths (initSupabaseSession / onAuthStateChange / visibilitychange) with boolean-flag coordination and no mutex. `_qcSessionRestored` set optimistically before nav confirmed. **Permanent fix = Path A/B/C consolidation into one `_qcRestoreAndNavigate()` function.** Dedicated session needed — higher risk, do when stable.

---

## Pending — next sessions

### qc-v356 — dispute/chargeback handler (MEDIUM revenue leak)
- `dispute.lost` + `dispute.accepted` → `has_paid = false`
- Dodo event names confirmed: `dispute.lost`, `dispute.accepted`
- **Blocked on:** confirm dispute payload shape (where `user_id`/`email` sit)
- Action: pull real dispute payload from Dodo sandbox/docs first

### Path A/B/C consolidation (permanent auth fix)
- Collapse three restore paths into one `_qcRestoreAndNavigate()` function
- Replace boolean soup with single `_qcAuthPhase` state variable
- Do after v355 confirmed stable in Sentry

### External Content Links (before publishing to production)
- Enrollment in Play Console (PLAY_STORE_PREP §15a)
- Disclosure modal in IS_TWA unlock flow (§15b)

---

## Sentry to watch
- JAVASCRIPT-8 — cold-start blank page — should drop after v355 rolls out
- JAVASCRIPT-1B — 401 anon-key-mismatch — was one-off from v347 cache during deploy, should not recur
- JAVASCRIPT-3 — CSP Clarity — low priority backlog
- JAVASCRIPT-1A — clientAppUnavailable — monitor, should reduce with v350 SDK fix

---

## Recent commits
- `2a339fd` — qc-v355: cold-start blank page rescue (JAVASCRIPT-8)
- `39ab4b3` — qc-v354: server-side identity verification (security)
- `3822656` — qc-v353: _qcDodoInFlight 90s safety timeout
- `14478a3` — qc-v352: dedupe post-checkout double-fire
- `60ea1f8` — qc-v351: version badge fix
- `4eb8d83` — qc-v350: Dodo SDK onload/onerror
- `8820622` — qc-v349: drop _emailBlank from _isLateRestore
- `bb62ec1` — qc-v348: visibilitychange auth race (CRITICAL)
