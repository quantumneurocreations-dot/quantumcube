---
tags: [core, state]
---
# CURRENT STATE — overwrite this every session end

**Updated:** 2026-05-31 (session 28 — auth consolidation v356 + Dodo CSP fix v357, both deployed)
**HEAD (QC):** `2c86eb6` — qc-v357 Dodo CSP fix (on top of v356 auth consolidation) ✅ DEPLOYED (live, verified)
**QC SW:** qc-v357 | **QI server:** localhost:3001 | **has_paid=true:** 7 (real paying: 2)
**Android versionCode:** 5 | **AAB:** versionCode 5 uploaded to Play Console ✅

---

## ✅ DEPLOYED — qc-v348 → qc-v357

**qc-v357** (2026-05-31): CSP `script-src` now allows `https://*.dodopayments.com` — fixes the
recurring JAVASCRIPT-6 CSP violation (Dodo SDK's `sdk.hs.dodopayments.com` sub-script was blocked
on every Pay tap). Standalone, not auth-related. Live + verified on quantumcube.app.


Frontend + both edge functions live. $17 round-trip passed (v354). v356 device-tested on the real
Chrome engine (cloudflared tunnel → Android Chrome) — cold-start restore recovers (loader holds, brief
form, then navigates in; **no hard blank-signup lock like v355**), console clean. Merged **fast-forward**
(main requires linear history — `--no-ff` is rejected), `deploy-pages.yml` green, quantumcube.app confirmed
serving qc-v356.

---

## What shipped — v356 (auth session-restore consolidation)

The "keeps breaking for 10+ versions" root cause fixed at the source. Three duplicated restore paths +
the overloaded `_qcSessionRestored` flag → ONE idempotent `_qcResolveAuth(session, source)` driven by a
`_qcAuthPhase` state machine (`idle → restoring → restored | awaiting-input`) + a separate `_qcAuthSettled`
loader-dismiss signal. All three triggers (init / onAuthStateChange / visibilitychange) are now thin
callers. Three Codex review rounds caught **7 real auth/payment bugs** before ship:

| Fix | Severity | What |
|-----|----------|------|
| resurrection race | HIGH | `_qcAuthGen` bumped on SIGNED_OUT; restore aborts post-await on gen mismatch |
| fetch stranding | HIGH | `_qcFetchProfile` 8s timeout + Supabase `{error}` → `_QC_FETCH_FAILED` sentinel; one bounded retry |
| payment downgrade | HIGH | `_qcResolveAuth` bails while `_qcPendingPaymentUnlock` (no stale re-lock of a paid user) |
| payment-giveup strand | MEDIUM | `attemptPaymentUnlock` give-up exits hand back to `_qcResolveAuth` |
| retry double-fire | MEDIUM | retry guarded against `restoring` (won't clobber an event-driven restore) |
| loader hang | MEDIUM | force-settle when runCalc fails twice (no 12s spin) |
| OAuth prefill | MEDIUM | no-profile branch restores email/name prefill |

Plan: `plans/2026-05-30-auth-restore-consolidation.md` · Runbooks:
`brain/agents/coder/knowledge/08-device-test-runbook-v356.md` + `…/08-merge-deploy-runbook-v356.md`.

### Earlier this run — qc-v348 → qc-v355
| Version | Severity | Fix |
|---------|----------|-----|
| v348 | CRITICAL | visibilitychange guards + removed `saveProfileFromForm()` (DB corruption vector) |
| v349 | HIGH | Drop `\|\| _emailBlank` from `_isLateRestore` |
| v350 | HIGH | Dodo SDK `onload`/`onerror` — SDK inits on arrival, not lazily on first Pay tap |
| v351 | MEDIUM | Version badge `window.Dodo` → `_resolveDodoSdk()` (badge was always lying) |
| v352 | MEDIUM | `_qcPostCheckoutHandled` post-checkout double-fire guard |
| v353 | MEDIUM | `_qcDodoInFlight` 90s safety timeout |
| v354 | HIGH security | Server-side JWT identity verification (dodo-create-session + webhook hardening) |
| v355 | HIGH | Cold-start blank-page rescue (JAVASCRIPT-8) — now superseded by v356's root fix |

---

## Pending — next sessions

### qc-v358 — dispute/chargeback handler (MEDIUM revenue leak)  ← bumped again (v356 = consolidation, v357 = Dodo CSP fix)
- `dispute.lost` + `dispute.accepted` → `has_paid = false`
- Dodo event names confirmed: `dispute.lost`, `dispute.accepted` (do NOT revert on `dispute.opened`)
- **Blocked on:** confirm the dispute payload shape (where `user_id`/`email` sit) — pull a real dispute payload from Dodo sandbox/docs first; do not wire blind

### runCalculation autofill root cause (the deeper one)
- v356 makes a stranded restore RECOVERABLE but does not eliminate WHY `runCalculation` silently returns
  early after `_qcForcePopulateFromProfile` (Android autofill DOM corruption — v314/v343).
- Prioritise via the `v356: restore retry still on face 0` Sentry volume. Its own effort.

### Deferred from Codex review (low)
- Codex #3: reset `_qcAuthSettled` on re-entry (cosmetic, no live impact)
- Codex #5: visibility-restore localStorage-token expiry validation (pre-existing minor)

### External Content Links (before publishing to production)
- Enrollment in Play Console (PLAY_STORE_PREP §15a)
- Disclosure modal in IS_TWA unlock flow (§15b)

---

## Sentry to watch (post-v356)
- **JAVASCRIPT-8** — cold-start blank page — should drop toward zero as v356 rolls out (PRIMARY signal)
- `v356: restore retry still on face 0` — NEW; a few are expected (retry path working), a SPIKE = autofill root cause biting
- new exceptions tagged `area: resolve-auth-runcalc` or `area: fetch-profile` = v356 regression, investigate
- JAVASCRIPT-1A — clientAppUnavailable — monitor, should reduce with v350 SDK fix
- JAVASCRIPT-3 — CSP Clarity — low priority backlog

---

## Recent commits (qc-v356 tip)
- `c0c9cc8` — qc-v356: restore on payment-unlock give-up (Codex pass #3)
- `0a5cf44` — qc-v356: Supabase `{error}` handling + retry double-fire (Codex re-review)
- `d73233d` — qc-v356: guard profile-apply on transient fetch failure
- `4c20020` — qc-v356: 4 Codex fixes (#1/#2/#4/#6)
- `7da383d` — qc-v356: onAuthStateChange rewrite + 8s fetch timeout
- `c86e1f5` — qc-v356: `_qcResolveAuth` single restore fn + helpers
- `933572f` — qc-v356: `_qcAuthPhase` state machine
- `2a339fd` — qc-v355: cold-start blank page rescue (prior session)
