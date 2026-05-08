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
- ✅ Canonical skill `.claude/skills/quantum-cube/SKILL.md` bumped 1.0.0 → 1.1.0 — added §2.6 no-option-pickers, §2.7 proactive inline suggestions, §2.8 SESSION_LOG protocol
- ✅ `SESSION_LOG.md` created (this file)

**In progress:**
- Resend bounce/complaint → Sentry webhook: new Edge Function `resend-events`, signature verification via Standard Webhooks SDK, posts to Sentry as warning. Closes the carry-forward gap noted in PROJECT_BRIEF.md (Resend webhooks NONE configured).
- Vercel preview deploys for `docs/` folder per branch
- Public status page on UptimeRobot

**Skipped (user agreed to defer):**
- Weekly digest email (user prefers daily review)
- PostHog feature flags + first A/B test (later)
- "First 1000 customers" Resend templates playbook (later)

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
