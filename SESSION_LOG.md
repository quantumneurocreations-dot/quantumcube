# Session Log

Live working narrative across chats. Append-only. Each session adds a new entry **early** in the work (after the first non-trivial action), then updates it incrementally. This survives tools-drops, Mac permission prompts, browser crashes — anything that wipes the chat without wiping git.

Format per entry: date stamp, one-line goal, bulleted actions, open questions, what's next. Terse. This is for the next-chat-Claude, not a journal.

For older completed-and-committed history, see `BRIEF_ARCHIVE.md`.

---

## 2026-05-08 PM — Stack-upgrade sweep + process hardening

**Goal:** Continue the May 8 stack audit. User flagged: previous chat (titled "System upgrade") got disrupted by a Mac permission prompt + Claude Desktop restart. Recovered context from git commits + DECISIONS.md (ADR-017). Then user asked Claude to bring its own ideas for further upgrades instead of always being the recipient of his.

**Done in this chat:**
- ✅ Resend dedicated key created (`quantum-cube-dodo-webhook`, id `5b36c8df-645e-4a77-bc25-a060ad22b161`) — saved in user's Apple Passwords
- ✅ `RESEND_API_KEY` set as Supabase Edge Function secret (digest `02d1cd31...`) — unblocks welcome email pipeline shipped this morning in commit `14e4210`
- ✅ Key validated: domain `quantumcube.app` reachable, "Quantum Cube Customers" audience reachable
- ✅ UptimeRobot monitor `803021425` "QC — Narrate (Edge Function)" — keyword check on `Method not allowed`, alerts when missing
- ✅ Memory edit added: user prefers verbal/speech-to-text — never use `ask_user_input_v0` option pickers
- ✅ Canonical skill `.claude/skills/quantum-cube/SKILL.md` bumped 1.0.0 → 1.1.0 — added §2.6 no-option-pickers, §2.7 proactive inline suggestions, §2.8 SESSION_LOG protocol (commit `094cb78`)
- ✅ `SESSION_LOG.md` created (this file)
- ✅ **Resend bounce/complaint → Sentry pipeline shipped** (commit `723b2d5`) — new Edge Function `resend-events`, webhook `2a5c62b4-7e5c-42eb-bdeb-fbe56bcdc8f9`, signing secret stored as `RESEND_WEBHOOK_SECRET`. Closes the Resend-webhooks-NONE-configured gap from PROJECT_BRIEF.md.
- ✅ **Status page rebranded as "Quantum Cube — Status"** at `https://stats.uptimerobot.com/azO4bPUJJQ` — logo (qc-icon-192.png) + favicon (qc-favicon-32.png) uploaded, homepage URL set to https://quantumcube.app, auto-add-monitors stays ON
- ✅ **PostHog narrate instrumentation shipped** (commit `e5467d5`, qc-v210→v211) — `narrate_api_requested`, `narrate_api_succeeded`, `narrate_api_failed`, `narrate_audio_played` events added to `fetchNarration()` and `startNarrationFromUrl()`. Now we can measure narration success rate, API latency, and validate the upcoming narration fix against real before/after metrics.
- ✅ **PostHog insight "Narrate — API health" created and favorited** — https://eu.posthog.com/project/172921/insights/buiaXjHa (short_id `buiaXjHa`, id 4114564). 14-day Trends line graph of all four narrate_* events. Tagged `narrate`, `api-health`, `qc-v211`.
- ✅ **Project annotation marking qc-v211 deploy** at 2026-05-08T12:00:00Z — marker will appear on every PostHog chart so the before/narration-fix-after split is visible.

**In progress:**
- ~~Vercel preview deploys~~ — reconsidered, **decided to skip** (single-HTML PWA on GitHub Pages doesn't earn what Vercel costs in workflow change; better to set up a one-line `python3 -m http.server` dev script in the future)
- ~~Public status page on UptimeRobot~~ — ✅ **shipped**: existing page at `https://stats.uptimerobot.com/azO4bPUJJQ` renamed to "Quantum Cube — Status", homepage URL set to https://quantumcube.app, logo (qc-icon-192.png) + favicon (qc-favicon-32.png) uploaded. Custom CNAME `status.quantumcube.app` is paid-only on UptimeRobot — deferred. Auto-add new monitors stays ON (per user)

**Skipped (user agreed to defer):**
- Weekly digest email (user prefers daily review)
- PostHog feature flags + first A/B test (later)
- "First 1000 customers" Resend templates playbook (later)
- Vercel preview deploys (Claude reconsidered — architecture mismatch)
- UptimeRobot CNAME (`status.quantumcube.app`) — paid-only on UptimeRobot, default `stats.uptimerobot.com/azO4bPUJJQ` URL is fine

**Open questions / decisions pending:**
- Vercel preview deploy: confirm whether existing parked Vercel project can be reused or needs fresh setup
- Status page: keep at UptimeRobot subdomain (`stats.uptimerobot.com/...`) or set up CNAME `status.quantumcube.app`?

**What's next (this chat):**
1. Build + deploy `resend-events` Edge Function
2. Wire Resend webhook in dashboard
3. Smoke test by sending a known-bad email
4. Vercel preview deploys recon
5. Status page configuration

**For the next chat (if this one drops):**
- Read this entry + the latest commits in `git log --since="2026-05-08"` to know where we are
- Resend webhook deployment status: check `supabase functions list` for `resend-events`
- Skill is at v1.1.0 — process changes already encoded, no need to re-derive
