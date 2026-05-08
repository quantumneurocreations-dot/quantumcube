# Session Log

Live working narrative across chats. Append-only. Each session adds a new entry **early** in the work (after the first non-trivial action), then updates it incrementally. This survives tools-drops, Mac permission prompts, browser crashes — anything that wipes the chat without wiping git.

Format per entry: date stamp, one-line goal, bulleted actions, open questions, what's next. Terse. This is for the next-chat-Claude, not a journal.

For older completed-and-committed history, see `BRIEF_ARCHIVE.md`.

---

## 2026-05-08 evening/night — Chrome audit sweep + Claude Code setup

**Goal:** Chrome tabs safety/efficiency audit + Claude Code installation + full tool setup.

**Done in this chat:**
- ✅ `docs/manifest.json` TWA audit — added `id: "/app"` for stable PWA identity (commit `4b69936`)
- ✅ **Claude.ai settings audit** — Instructions for Claude field populated (persistent prefs across all chats), Discovery toggle OFF, Cloudflare Developer Platform disconnected (redundant), Privacy verified (training OFF, location OFF)
- ✅ **Supabase audit** — advisors clean (0 performance, 1 known false-positive re: password auth), RLS verified on both public tables, 6 edge functions confirmed ACTIVE. Stale unconfirmed auth user `admin@qncacademy.com` deleted (created Apr 21, never confirmed). auth.users: 8, all confirmed.
- ✅ **Sentry/Clarity CSP fix** (commit `da02bc3`, qc-v212) — Previous chat wired Clarity but only whitelisted `www.clarity.ms` in script-src. Clarity CDN (`scripts.clarity.ms`) was blocked → Sentry `JAVASCRIPT-6`. Fixed: `*.clarity.ms` wildcard across all 10 pages with CSP meta tags. JAVASCRIPT-6 resolved.
- ✅ **PostHog audit** — SDK doctor healthy, 3 insights configured, ingestion alive (6 events/2 days). No action needed.
- ✅ **Claude Code installed** — v2.1.133 via native installer, Opus 4.7 (1M context), Claude Max plan, `~/Projects/quantumcube`
- ✅ **Claude Code configured** (commits `347afb6`, `55f72fc`, `efc4a66`, `2ab95a0`):
  - `~/.claude/CLAUDE.md` — global prefs (buddy tone, autonomy, upgrading mindset)
  - `.claude/commands/` — `/project:health-check`, `/project:pre-ship`, `/project:narration-fix`
  - `.claude/settings.json` — PostToolUse hook warns on SW/APP version mismatch
  - `.mcp.json` cleared (project-level remote SSE MCPs conflict with claude.ai connectors)
- ✅ **User MCPs added to Claude Code** (global scope): ElevenLabs (24 tools), Context7 (2 tools), Tavily (5 tools)
- ✅ **20 MCP servers total** in Claude Code: 3 user MCPs + 17 claude.ai connectors (GitHub 41, Supabase 29, Sentry 22, Resend 32, Linear 33, etc.)
- ✅ Extra usage enabled on Claude.ai ($20/month limit)

**Key architectural insight (ADR-020):** Remote SSE MCPs (Supabase/Sentry/PostHog hosted URLs) cannot run from local Claude Code — Anthropic policy blocks persistent SSE from local machines. Solution: claude.ai connectors auto-sync to Claude Code when authenticated with Max plan. No project-level MCP config needed for cloud services.

**Division of labour going forward:**
- **Claude Code (terminal):** file edits, git, bash, deploys, narration regeneration via ElevenLabs MCP
- **Claude Chat (web):** planning, PostHog analytics, Sentry investigation, browser automation

**In progress:**
- _(nothing uncommitted — all shipped)_

**Open questions / decisions pending:**
- _(none)_

**🚀 NEXT-CHAT LEAD-IN:**
1. **Boot as usual** per CHAT_KICKOFF.md v4.3.0. Read this SESSION_LOG after PROJECT_BRIEF v43.
2. **Narration fix is the immediate coding task** — start in Claude Code terminal: `/project:narration-fix`. This loads context and reads the Edge Function. The audit tool at `/audit-narration.html` needs a bug fix first (user reported it's not working well). Fix the audit tool → user flags bad MP3s → Claude Code regenerates flagged files via ElevenLabs MCP with corrected phonetics → replace files.
3. **Play Store TWA** — target was Sunday May 10. Steps: generate Android keystore via Bubblewrap, get real SHA-256 for `/.well-known/assetlinks.json`, build `.aab`, submit to Play Console.

**Pre-existing operational notes:**
- HEAD: `2ab95a0` → will update after handoff commit
- SW: `qc-v212`. Pre-commit hook validates sync.
- Sentry: 0 unresolved issues.
- auth.users: 8 (all confirmed, no stale records).
- Claude Code: active at v2.1.133. Run `claude` from `~/Projects/quantumcube`.


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
- ✅ **PostHog insight "Narrate — API latency (p50 / p95 / p99)" created and favorited** — https://eu.posthog.com/project/172921/insights/AHB7Ci6u (short_id `AHB7Ci6u`, id 4114617). 14-day Trends line graph of latency_ms percentiles from `narrate_api_succeeded`. Tagged `narrate`, `latency`, `qc-v211`.
- ✅ **Project annotation marking qc-v211 deploy** at 2026-05-08T12:00:00Z — marker will appear on every PostHog chart so the before/narration-fix-after split is visible.

*(Briefly created a "Quantum Cube — Narrate Health" dashboard to group both insights, then deleted it: the available PostHog MCP tools don't support attaching insights to a dashboard programmatically (no `insight-update` exposed via tool_search), and an empty pinned dashboard is worse UX than two favorited insights. Both insights are findable via the PostHog Insights menu's Favorites filter.)*

**In progress:**
- _(none — all live work for this chat is shipped and pushed; HEAD at `e26d591`)_

**Skipped (user agreed to defer):**
- Weekly digest email (user prefers daily review)
- PostHog feature flags + first A/B test (later)
- "First 1000 customers" Resend templates playbook (later)
- Vercel preview deploys (Claude reconsidered — architecture mismatch, see ADR-018)
- UptimeRobot CNAME (`status.quantumcube.app`) — paid-only on UptimeRobot, default `stats.uptimerobot.com/azO4bPUJJQ` URL is fine
- Custom "Narrate Health" PostHog dashboard — PostHog MCP doesn't expose `insight-update` cleanly; two favorited insights are sufficient (see ADR-018)

**Open questions / decisions pending:**
- _(none — all questions from earlier in the session resolved before doc-update commit)_

**Doc-update transition pack (committed at end of this chat):**
- `PROJECT_BRIEF.md` v41 → v42 — added v42 update note, bumped Edge Functions count 5 → 6, added `resend-events` subsection, added webhook → Sentry paragraph in Email Infrastructure
- `DECISIONS.md` — added ADR-018 covering all PM work (Resend webhook, narrate analytics, Vercel skip, skill v1.1.0)
- `CHAT_KICKOFF.md` v4.1.0 → v4.2.0 — added `SESSION_LOG.md` to the read-in-order doc system, updated boot footer to read brief THEN session log
- `SESSION_LOG.md` (this file) — final polish for clean handoff

**🚀 NEXT-CHAT LEAD-IN (start here):**

1. **Boot sequence as usual** — run `tool_search` calls per `CHAT_KICKOFF.md` v4.2.0 BOOT STEP 1, smoke-test loaded tools (BOOT STEP 2), health-check (BOOT STEP 3). Then read `PROJECT_BRIEF.md` v42 and this file.

2. **First proactive task: 60-second `docs/manifest.json` audit against Google Play TWA requirements.** Target: Google Play submission Sunday May 10 (~2 days out). Specifically grep for / verify:
   - 512×512 `maskable` icon entry (`purpose: "any maskable"` or `purpose: "maskable"` separate entry)
   - `display: "standalone"` or `"fullscreen"` (TWA requires this; `"browser"` would block Play approval)
   - `start_url` is a valid same-origin path
   - `theme_color` and `background_color` set (Play uses these for splash)
   - `name` (full ≤ 45 chars for Play listing) and `short_name` (≤ 12 chars for Android home screen)
   - `scope` set to `/` or app-root
   - `id` field present (recommended for stable PWA identity)

   Report findings back inline, then ship a single commit if anything's missing. Existing `/.well-known/assetlinks.json` placeholder still needs the real keystore SHA-256 — that's a separate step user needs to do at signing time, not chat-side.

3. **Then onto the narration-fix workstream.** Telemetry is now waiting (qc-v211 instrumentation + 2 PostHog insights + project annotation). Whatever the fix turns out to be, the before/after will be measurable on `https://eu.posthog.com/project/172921/insights/buiaXjHa` and `/AHB7Ci6u`.

**Pre-existing operational notes for next-chat-Claude:**
- HEAD: `e26d591` (post doc-update commit will bump this)
- Live SW: `qc-v211`. Sentry release: `quantum-cube@qc-v211`. Pre-commit hook validates this sync — don't bypass.
- Resend webhook deployment status: live, signing secret set, tested 400 + 401 paths
- Welcome email pipeline live on `dodo-webhook` Edge Function (ADR-017) — first paying customer post-`RESEND_API_KEY` setup gets brand-voiced welcome automatically
- Skill is at v1.1.0 — process changes already encoded (no option pickers, proactive close, this log file)
