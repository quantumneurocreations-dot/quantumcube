---
tags: [core, state]
---
# CURRENT STATE — overwrite this every session end

**Updated:** 2026-05-23 (session 15 — FINAL)
**HEAD (QC):** `819a13d` — fix: adaptive auth loader timeout (v319)
**QC SW:** qc-v319 | **QI server:** localhost:3001 | **has_paid=true:** 6 (real paying = 2)
**Android versionCode:** 5 | **AAB:** versionCode 5 uploaded to Play Console ✅

---

## Play Store — PRODUCTION READY DAY ~MAY 29 (day 14)

### What YOU must do before May 29
1. 🔴 **Message all 12 testers** — tell them to actively OPEN + USE the app. Google checks engagement, not just opt-in. A few sessions each before May 29 is enough.
2. 🔴 **Push one more QC release** before May 29 — shows active development to Google. Even a small UX fix counts.

### What happens on May 29 (day 14)
3. 🔴 **Submit production form** — ~10 questions, 250-300+ chars each. Key talking points:
   - How testers were recruited (SA market, personal network)
   - Feedback gathered and incorporated each release
   - Changes made: sign-in flow, category card layout, Dodo payment button, auth loader (v318/v319)
   - 12 testers opted in, active testing window completed
   - Why app is ready for production
4. 🔴 **"Apply for production" button** — only unlocks on day 14. Submit immediately.

### After submission
- Google review: ~7 days
- Pre-launch report: already generating from versionCode 5 upload (~30 min after upload)
- Check: https://play.google.com/console/u/0/developers/9099327495444765719/app/4973211872239545786/pre-launch-report/overview

---

## Sentry (updated 2026-05-23 — CLEAN)
- ✅ JAVASCRIPT-8 resolved — info breadcrumb
- ✅ JAVASCRIPT-16 resolved — info breadcrumb (happy path)
- ✅ JAVASCRIPT-18 resolved — tester incomplete profile, expected behaviour
- 🟡 JAVASCRIPT-3 — CSP blocking Clarity img `c.clarity.ms/c.gif` — low priority, backlog

---

## Recent commits (this session)
- `819a13d` — fix: adaptive auth loader timeout v319 (fixes rapid re-open race condition)
- `41fff03` — chore: bump versionCode 5, versionName z2
- `acbc04d` — feat: auth loading overlay qc-v318

---

## Agents (all 12 complete as of 2026-05-17)
- ✅ quantum · security · upgrade · mind · cleaner · project
- ✅ design · marketing · admin · truth · coder · audit

---

## Full backlog (priority order)
1. 🔴 Message 12 testers — nudge active usage before May 29
2. 🔴 Push one more QC release before May 29
3. 🔴 Production form answers + submit on day 14 (~May 29)
4. 🟡 JAVASCRIPT-3 — CSP img-src add `c.clarity.ms`
5. 🟡 Dodo refund webhook → auto-flip has_paid on refund
6. 🟡 qi-voice.py CoS briefing: read all briefing snippets
7. 🟡 CSP: Report-Only → Enforcing
8. 🟡 Truth adversarial test
9. 🟡 Marketing full `all` mode live test (first Monday)
10. 🟡 Canva MCP + ElevenLabs narration — Design v3.1
11. 🟡 Wake word training
12. 🟡 ElevenLabs cancel after Valory migration
13. 🟡 Agent handshake pairs (Upgrade→Truth, Coder→Truth) — ADR-033

---

## Key facts
- **QC DB:** Supabase `fqqdldvnxupzxvvbyvjm` | **QI DB:** `zhvcmxtgvrogxnvqauus`
- **Real paying customers:** 2 (keyzer.pretorius + booyens.michelle)
- **Voice:** ElevenLabs `uju3wxzG5OhpWcoi3SMy` | model: `eleven_turbo_v2_5`
- **Play Console:** Developer `9099327495444765719` | App `4973211872239545786`
- **Keystore:** `android/quantumcube.keystore` · alias `quantumcube` · pw in Apple Passwords
- **Bubblewrap JDK:** `/Users/qnc/.bubblewrap/jdk/jdk-17.0.11+9`
- **Bubblewrap Android SDK:** `/Users/qnc/.bubblewrap/android_sdk`
- **Sentry:** `quantum-neuro-creations` · EU `de.sentry.io`
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
