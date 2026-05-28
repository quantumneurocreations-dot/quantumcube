---
tags: [core, state]
---
# CURRENT STATE — overwrite this every session end

**Updated:** 2026-05-28 (session 16 — production access day)
**HEAD (QC):** `f3ef9c9` — fix: clear _qcSavedName/Dob on sign-out (v332 profile lock gap)
**QC SW:** qc-v332 | **QI server:** localhost:3001 | **has_paid=true:** 6 (real paying = 2)
**Android versionCode:** 5 | **AAB:** versionCode 5 uploaded to Play Console ✅

---

## Play Store — PRODUCTION ACCESS TONIGHT

**14-day testing window completes ~6-7pm TODAY (May 28).**

### What to do tonight
1. 🔴 **Click "Apply for production access"** — button unlocks on Play Console Dashboard at ~6-7pm. Submit immediately.
2. 🔴 **Fill questionnaire** — Parts 1, 2, 3. Use prepared copy-paste answers.
3. 🔴 **DO NOT click Publish** after Google approval. Managed Publishing is ON — won't auto-release.

### Review credentials (Part 3)
- **Email:** `qnc.review@gmail.com`
- **Password:** Ronnie's Gmail password
- **Instructions:** "Enter email, tap Continue, check Gmail for 6-digit OTP, enter in app. Account pre-unlocked — enter any name and date of birth, then tap Reveal My Cube to explore all 4 faces."
- **Note:** Profile lock is live (qc-v332). Reviewer's first-entered name/DOB saves to their account. They can tap "Edit Details" to change if needed.

### Before Publishing (after Google approval — DO NOT skip)
- 🔴 External Content Links enrollment in Play Console (PLAY_STORE_PREP §15a)
- 🔴 External content links disclosure modal in IS_TWA unlock flow (PLAY_STORE_PREP §15b)
- 🔴 TWA payment path confirmed as web redirect (ADR-026)

---

## Sentry (updated 2026-05-23 — CLEAN)
- ✅ JAVASCRIPT-8 resolved
- ✅ JAVASCRIPT-16 resolved
- ✅ JAVASCRIPT-18 resolved
- 🟡 JAVASCRIPT-3 — CSP blocking Clarity img `c.clarity.ms/c.gif` — low priority, backlog

---

## Recent commits
- `f3ef9c9` — fix: clear _qcSavedName/Dob on sign-out (v332 profile lock gap)
- `ae84677` — feat: lock profile name/dob to account — one profile per user (qc-v332)
- `ee5b2a0` — feat: dodo getSession 4s timeout guard (qc-v331)
- `819a13d` — fix: adaptive auth loader timeout (qc-v319)

---

## Agents (all 12 complete as of 2026-05-17)
- ✅ quantum · security · upgrade · mind · cleaner · project
- ✅ design · marketing · admin · truth · coder · audit

---

## Full backlog (priority order)
1. 🔴 Submit production access form tonight (~6-7pm)
2. 🔴 External Content Links enrollment + disclosure modal (before publishing)
3. 🟡 Supabase Pro upgrade — auto-pause risk (ADR-028, deferred)
4. 🟡 JAVASCRIPT-3 — CSP img-src add `c.clarity.ms`
5. 🟡 Dodo refund webhook → auto-flip has_paid on refund ✅ (edge function exists, needs verification)
6. 🟡 qi-voice.py CoS briefing: read all briefing snippets
7. 🟡 CSP: Report-Only → Enforcing
8. 🟡 Truth adversarial test
9. 🟡 Marketing full `all` mode live test
10. 🟡 Canva MCP + ElevenLabs narration — Design v3.1
11. 🟡 Wake word training
12. 🟡 ElevenLabs cancel after Valory migration
13. 🟡 Agent handshake pairs (Upgrade→Truth, Coder→Truth) — ADR-033
14. 🟡 Claude Code 401 — run `/login`

---

## Key facts
- **QC DB:** Supabase `fqqdldvnxupzxvvbyvjm` | **QI DB:** `zhvcmxtgvrogxnvqauus`
- **Real paying customers:** 2 (keyzer.pretorius + booyens.michelle)
- **Review account:** `qnc.review@gmail.com` — `has_paid=true` confirmed (created 2026-05-12)
- **Tester account:** `noel92.nh@gmail.com` — `has_paid=true` (manual, not real customer)
- **Voice:** ElevenLabs `uju3wxzG5OhpWcoi3SMy` | model: `eleven_turbo_v2_5`
- **Play Console:** Developer `9099327495444765719` | App `4973211872239545786`
- **Keystore:** `android/quantumcube.keystore` · alias `quantumcube` · pw in Apple Passwords
- **Managed Publishing:** ON — Google approval will NOT auto-publish
- **Obsidian vault:** `/Users/qnc/Projects/quantum-integrator`

<!-- topic-linker:start -->
---
## See Also
- [[Claude Code]]
- [[ElevenLabs]]
- [[Play Store]]
- [[Sentry]]
- [[Supabase]]
<!-- topic-linker:end -->
