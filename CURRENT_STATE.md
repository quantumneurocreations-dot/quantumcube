---
tags: [core, state]
---
# CURRENT STATE — overwrite this every session end

**Updated:** 2026-05-23 (session 15)
**HEAD (QC):** `41fff03` — chore(android): bump versionCode 5, versionName z2
**QC SW:** qc-v318 | **QI server:** localhost:3001 | **has_paid=true:** 6 (real paying = 2)
**Android versionCode:** 5 | **AAB:** uploaded to Play Console ✅

---

## Play Store status (updated 2026-05-23)
- ✅ Closed testing release published — versionCode 5 (z2) uploaded today
- ✅ 12 testers opted-in and on the list
- ⏳ ~Day 9 of 14 — hit 14 days ~May 29
- 🔴 Testers need to actively USE the app (not just be opted-in) — engagement matters for Google approval
- 🎯 Apply for production: ~May 29 (day 14)
- 🎯 Google review after submission: ~7 days
- ℹ️ Google checks: tester engagement + updates pushed during testing period ✅

## Sentry (updated 2026-05-23)
- ✅ JAVASCRIPT-8 resolved — info breadcrumb, expected nav behavior
- ✅ JAVASCRIPT-16 resolved — happy path breadcrumb, not an error
- 🟢 Zero open issues

## Recent commits
- `41fff03` — chore(android): bump versionCode 5, versionName z2
- `acbc04d` — feat: auth loading overlay qc-v318 (eliminates sign-up flash for returning users)

## Agents built (all 12 complete as of 2026-05-17)
- ✅ quantum (voice) · security · upgrade · mind · cleaner · project
- ✅ design · marketing · admin · truth · coder · audit
- All at v3.0.0+ · All crons wired · All briefing snippets active

## Obsidian Second Brain (installed 2026-05-19)
- ✅ claude-vault watcher · topic-linker v4.2.8 · Claude Memory mirror
- ✅ Session hooks · Auto Note Mover · Smart Connections
- ✅ CLAUDE.md auto-archive protocol — global, all Claude Code sessions

## What's next
1. 🔴 Message testers — nudge them to actively USE the app before May 29
2. 🔴 Draft + submit production form answers (~May 29, day 14)
3. 🟡 Push one more QC release before May 29 (shows active dev to Google)
4. 🟡 Dodo refund webhook → auto-flip has_paid on refund
5. 🟡 qi-voice.py CoS briefing: read all briefing snippets
6. 🟡 CSP: Report-Only → Enforcing
7. 🟡 Truth adversarial test
8. 🟡 Marketing full `all` mode live test (first Monday)
9. 🟡 Canva MCP + ElevenLabs narration — Design v3.1
10. 🟡 Wake word training
11. 🟡 ElevenLabs cancel after Valory migration
12. 🟡 Agent handshake pairs (Upgrade→Truth, Coder→Truth) — ADR-033

## Obsidian Copilot
- ✅ Copilot v3.3.2 · claude-sonnet-4-6 · gemini-2.5-flash · llama3.2 (Ollama)
- ✅ Semantic search ON · text-embedding-3-small (OpenAI)

<!-- topic-linker:start -->
---
## See Also
- [[Claude Code]]
- [[ElevenLabs]]
- [[Obsidian]]
- [[Play Store]]
- [[Sentry]]
- [[Supabase]]
<!-- topic-linker:end -->
