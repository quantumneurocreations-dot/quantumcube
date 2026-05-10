# QUANTUM CUBE — PROJECT BRIEF

**Version: v45 | Last Updated: May 10, 2026 (Sunday)**

> **v45 update note (May 10, 2026 — brand polish + Play Store setup, Chat Claude):** Four commits shipped (`af5a3f3` → `d298804`), SW qc-v223 → **qc-v225**. **Brand cyan sweep** — 75 colour replacements in `app.html`: #7dd4fc → #0cc0df + rgba(125,212,252,) → rgba(12,192,223,) including all 5 Vimeo `color=` params (ADR-025). **Privacy policy updated** — PostHog + Sentry added as service providers, effective date updated; live at `quantumcube.app/privacy`. **TWA payment redirect** (ADR-026) — `IS_TWA` detection (triple-method: referrer / sessionStorage / URL param); `unlock()` redirects Android users to `quantumcube.app/app?ref=android-unlock` instead of Dodo overlay; web flow unchanged; existing paid users auto-unlocked via Supabase `has_paid`. **`assetlinks.json` wired** with real SHA-256 from production keystore (`app.quantumcube.twa`, fingerprint `14:01:92:A5...9B:3D`), verified live. **AAB built by Claude Code** — `android/app-release-bundle.aab` (1.66MB), signed keystore 10,000-day validity, target SDK 35, compile SDK 36; keystore password in Apple Passwords. **Google Play developer account created** (ADR-027) — Quantum Neuro Creations personal account, Account ID `9099327495444765719`; identity docs uploaded, verification 1-3 days; 14-day testing gate clock started May 10. **Supabase Pro flagged** (ADR-028) — free tier auto-pause is a production risk for live paying-customer app; $25/month upgrade deferred to next session. **Feature graphic created** — 1024×500 PNG, Milky Way background, Cinzel Decorative font, neon wireframe cube; awaiting user approval then commit. **PLAY_STORE_PREP.md** committed (Claude Code, `9ed130b`) — 80-item checklist, 2026 policies cited. **Pending before Play Store submission:** Google identity verification, 12 closed-track testers (14-day gate), Play App Signing SHA-256 (after first AAB upload), in-app entertainment disclaimer, data safety form + content rating (in Play Console), 4-6 screenshots. **HEAD: `d298804`.**

> **v44 update note (May 9, 2026 — narration audit + full re-record pass, Claude Code surface):** Single full-day session in Claude Code terminal closing the narration-fix workstream queued from May 8. **Audit tool fixed first** — `docs/audit-narration.html` had silent HTML parse failure on every browser caused by an unescaped single quote in a textarea `placeholder` (`ed04840`); SW bypass for the audit page added so debug iterations don't fight stale cache (`9aec413`). **Narration audit completed** — 98 of 385 MP3s flagged. **Three rerecord passes to find the correct ElevenLabs settings**: pass 1 used speed 0.85 (from the dashboard's saved voice profile — wrong); pass 2 used speed 1.0 (closer but still off); pass 3 used **speed 1.15 with similarity_boost 0.75** — found in git history at `f7854ee` and `be9f385` where the `narrate` Edge Function had these hard-coded at the time the originals were generated. **ElevenLabs voice settings now LOCKED** (ADR-021): `eleven_turbo_v2_5`, stability 0.5, similarity_boost 0.75, speed 1.15 (welcome.mp3 exception: speed 1.0). The dashboard-stored voice profile is no longer authoritative — `scripts/rerecord.py` carries the canonical values. **Per-category TTS text transforms** (manifest text + UI text unchanged — TTS payload only): Life Phase 2-9 opening rewritten to "A Life Phase governed by the N marks…" (kills pause-before-number); Karmic Lesson digits 1-9 spelled as words ("One", "Two", …); Hidden Passion 4 & 6 digits spelled out + em-dash padded to break phonetic merge with "Passion"; chin_ox uses phonetic respelling "Ocks" because "Ox" rendered as just a sibilant. **`scripts/rerecord.py` shipped** as the canonical re-record tool — reads manifest, applies named transforms per filename, POSTs ElevenLabs, writes MP3s, emits SHA256 JSON. **Numerology Matrix description card added to `app.html`** — non-interactive `.matrix-desc` card directly below the 3×3 grid, same border/glass/inset-glow as the icard pattern. **claudewatch MCP installed surgically** (binary at `~/.local/bin/claudewatch`, MCP entry only — no global rule files; ADR-024). **11 commits this session** (`e0f3c79` → `29eece7`), SW qc-v213 → **qc-v223** (10 cache bumps for the rerecord/transform iterations + matrix card + audit fixes). Both manifests (`narration-manifest.json` + embedded `<script id="manifest-data">` in `audit-narration.html`) updated for every batch. **HEAD: `29eece7` → updated by handoff commit.** **Next session:** listen-pass on hp_6 v223 first thing — em-dash padding may still drop the digit; if so, fall back to "The Hidden Passion of Six" preposition-bridge.

> **v43 update note (May 8, 2026 evening/night — Chrome audit sweep + Claude Code setup):** Full-evening sprint, two major tracks. **Track 1 — Chrome pages audit:** Claude.ai settings hardened (Instructions for Claude populated, Discovery OFF, Cloudflare Dev Platform disconnected). Supabase: advisors clean, RLS verified, 6 Edge Functions confirmed, stale unconfirmed user `admin@qncacademy.com` deleted (auth.users now 8, all confirmed). Sentry: diagnosed + fixed `JAVASCRIPT-6` — previous chat had wired Clarity but only whitelisted `www.clarity.ms` in script-src; Clarity CDN (`scripts.clarity.ms`) blocked. Fixed: `*.clarity.ms` wildcard across all 10 pages with CSP meta tags (`da02bc3`), SW bumped qc-v211 → qc-v212, JAVASCRIPT-6 resolved. PostHog: healthy, 3 insights configured, SDK doctor clean. **Track 2 — Claude Code setup (NOW ACTIVE):** Installed v2.1.133 via native installer (`curl -fsSL https://claude.ai/install.sh | bash`), authenticated via Max OAuth, runs Opus 4.7 (1M context) in `~/Projects/quantumcube`. User MCPs (global stdio): ElevenLabs 24 tools, Context7 2 tools, Tavily 5 tools. Total 20 MCP servers (3 user + 17 claude.ai connectors auto-synced via Max plan — GitHub 41, Supabase 29, Sentry 22, Resend 32, Linear 33, etc.). Project files added: `.claude/commands/` (3 slash commands: health-check, pre-ship, narration-fix), `.claude/settings.json` (PostToolUse hook for SW version mismatch), `~/.claude/CLAUDE.md` (global prefs, not committed). `.mcp.json` cleared — project-level remote SSE MCPs conflict with claude.ai connectors (key insight ADR-020). Division of labour: Claude Code for file/git/bash/deploy, Claude Chat for analytics/monitoring/planning. Extra usage enabled ($20/month). Commits: `4b69936` (manifest id), `da02bc3` (CSP fix), `347afb6`–`2ab95a0` (Claude Code config). **HEAD: `2ab95a0` → updated by handoff commit.**

> **v42 update note (May 8 PM, stack-hardening sweep — second half of the May 8 day):** AM half (commits up to `cd89c27`) covered by ADR-017 in chat titled "System upgrade" — crashed mid-session by a Mac permission prompt + Claude Desktop restart, but all work was safely committed before the drop. PM half (this entry, ADR-018) shipped seven commits (`094cb78` → `e26d591`). **6th Edge Function deployed: `resend-events`** — receives Resend webhooks, forwards `email.bounced` / `email.complained` / `email.delivery_delayed` to Sentry as warnings/errors with full context (recipient, bounce type, email_id, subject). Standard Webhooks signature verification via `standardwebhooks@1.0.0`, hard-fails 503 if `RESEND_WEBHOOK_SECRET` unset (never accepts unverified). Webhook id `2a5c62b4-7e5c-42eb-bdeb-fbe56bcdc8f9`. **Resend dedicated key** `quantum-cube-dodo-webhook` (id `5b36c8df-645e-4a77-bc25-a060ad22b161`) created and `RESEND_API_KEY` set in Supabase secrets — unblocks the welcome email pipeline from ADR-017. **UptimeRobot Narrate monitor `803021425`** keyword check on `Method not allowed`. **Status page rebranded** as "Quantum Cube — Status" at `https://stats.uptimerobot.com/azO4bPUJJQ` with QC logo (qc-icon-192) + favicon (qc-favicon-32); homepage URL set to https://quantumcube.app; auto-add-monitors stays ON; custom CNAME `status.quantumcube.app` deferred (paid-only on UptimeRobot). **PostHog narrate instrumentation** (qc-v210 → qc-v211): four new events — `narrate_api_requested` (text_length only, never content), `narrate_api_succeeded` (latency_ms + size_bytes), `narrate_api_failed` (status, error <=200 chars, latency_ms, reason: `http_error` or `network_error`), `narrate_audio_played` (filename basename, source: prerecorded). Two saved+favorited insights: **"Narrate — API health"** (`buiaXjHa`, all four events 14-day Trends) and **"Narrate — API latency p50/p95/p99"** (`AHB7Ci6u`, latency_ms percentiles). Project annotation marks the qc-v211 deploy on every chart — before/after split visible for the upcoming narration fix. **Vercel preview deploys reconsidered and skipped** — single-HTML PWA on GitHub Pages doesn't earn what Vercel costs in workflow change; better future move is a one-line `python3 -m http.server 8000 -d docs/` local serve script. **Canonical skill bumped 1.0.0 → 1.1.0**: §2.6 no-option-pickers (verbal/speech-to-text user, never use `ask_user_input_v0` even with options), §2.7 proactive inline suggestions (assistant brings ideas, ends every session with one explicit "I noticed X, worth doing Y" suggestion), §2.8 `SESSION_LOG.md` end-of-session protocol — live working narrative appended EARLY in each chat and incrementally, designed to survive chat drops. **`SESSION_LOG.md` lives at repo root and is now part of the boot sequence** — read it at the start of every chat alongside this brief and `CHAT_KICKOFF.md`. Pre-commit hook passed at `qc-v211`, smoke test 13/13 PASS post-deploy. **HEAD at `e26d591`. Now-cookin'-with-oil moment, high-five vibes.** **Next chat lead-in (per §2.7 proactive close):** 60-second `docs/manifest.json` audit against Google Play TWA requirements (target: Google Play submission by Sunday May 10 — two days out). Then onto the narration-fix workstream which now has live before/after telemetry waiting for it.

> **v41 update note (May 7 evening — GitHub MCP unlocked + repo hygiene sweep):** Cleared the GitHub access blockade after extended troubleshooting. Custom connector now live at `https://api.githubcopilot.com/mcp/` with full read+write on `quantumcube` — first MCP-driven commit landed (`072f636`, docs(meta): README + LICENSE-PROPRIETARY + SECURITY). **Two-step setup gotcha** (memory #8): OAuth alone is insufficient — the "Claude Github MCP Connector" GitHub App must ALSO be installed at `github.com/apps/claude-github-mcp-connector/installations/new` (pick `quantumcube` only, Contents/Issues/PRs Read+Write). Without step 2, OAuth completes and tools load but every write 403s with "Resource not accessible by integration". GitHub doesn't re-prompt OAuth scopes after first auth, so disconnect/reconnect on Claude.ai does NOT trigger fresh consent — the install step happens entirely on GitHub's settings. Disambiguation: the directory "GitHub Integration" connector is file-sync only, exposes ZERO MCP tools — do NOT confuse with this custom connector setup. Authed as `qncacademy@icloud.com`. **Repo hygiene sweep (post-MCP):** CodeQL default config enabled (all 3 langs, push/PR + weekly), private vulnerability reporting ON, Dependabot malware alerts ON, automatic dependency submission ON, Actions permissions tightened from "Allow all" to "GitHub-only allowlist" (covers `actions/checkout@v4`, the only external action used). Browser toggles: Wikis OFF, Forking OFF, Web commit signoff REQUIRED, Topics added (`pwa`, `quantum-neuro-creations`). Repo home page now renders a README for the first time — Community Standards score should jump from 0%. **Verified secure & untouched**: main branch protection (force-push BLOCKED, deletion BLOCKED, linear history REQUIRED, no admin bypass, fork PR approval for first-timers), Push protection + Secret Protection active, workflow permissions read-only, Actions can't create/approve PRs, no secrets referenced in workflows. **MCP inventory delta since v40 (5 new):** PostHog (project 172921, EU host, dashboard 662076), Linear (Quantum Cube team `8024de1c-d53d-4a2c-baea-0a640f5c47e5`), Figma (view-only seat — read files, no edits), Canva (brand kit `kAHHOGJi4RI`), GitHub MCP (above). **Chrome agent on github.com:** read-only — Anthropic policy hard-blocks navigate/click. github.com IS in the extension's approved-sites list (read works fine). GitHub MCP makes the limitation largely irrelevant. **Operating note:** Repo writes now go through GitHub MCP (silent API — no visible Chrome activity, unlike on other sites). Branch protection still guards `main` even with write access. Auto-run discipline (memory #6) extends naturally: read freely, write when obvious, ask before destructive. Settings/admin actions (wikis, branch rules, secrets, transfer/delete repo) are NOT in MCP scope and remain manual on purpose. **Loose Python migration scripts at root** (`wire_supabase_01-08.py`, `cleanup_duplicate_fn.py`, `rewrite_legal.py`, `rewrite_terms.py`) — flagged for cleanup decision next session: delete or move to `archive/`. **Repo state vs v40:** Last commit `072f636` (was `e40ff08`) — three commits ahead: `4e605bd` (brief v40 commit), `634f29d` (feat: narration audit page at `/audit-narration.html`, live at `https://quantumcube.app/audit-narration.html`, localStorage key `qc_narr_audit_v1`, noindex/nofollow, unlinked), `072f636` (this docs(meta) commit). **OPERATIONAL LESSON from this session (saved later in same chat):** GitHub MCP `create_or_update_file` chokes silently on ~79K-char payloads — tool call gets stuck with no error. For big-file edits to PROJECT_BRIEF.md / BRIEF_ARCHIVE.md / app.html (anything > ~30K chars), use **Desktop Commander → local Python splice → `git push`** (worked tonight, commit `96c442b`). GitHub MCP `push_files` is fine for small edits and multi-file new creates (the README/LICENSE/SECURITY trio at `072f636` was a clean 3-file `push_files` call). Rule of thumb: small/new files → GitHub MCP, big rewrites → Desktop Commander local.

> **v40 update note (May 6, full-day audit-close + SEO sprint):** Long single-chat day, 7 commits shipped (`d5fdc79` → `e40ff08`), SW qc-v202 → qc-v208 (six version bumps). Three audits closed back-to-back: (1) May-5 evening Chrome audit (13 fixes incl. Dodo `@latest` → `@1.8.0`, DOB year dynamic, OG/Twitter on `/app`, icard ARIA accordion), (2) unpaid-user Chrome audit (18 a11y fixes — paywall content gate via `aria-hidden`+`inert`, full dialog a11y via new `QC_DIALOG` helper covering `payOverlay`/`legalOverlay`/`paySuccess` with focus trap + Esc + focus return, form `aria-live` + `aria-invalid`), (3) my own independent 17-pass audit. Brand polish: removed "Quantum Neuro Creations" tagline from header, CUBE word colour `#7dd4fc` → `#0cc0df` with layered neon drop-shadow (3 stacked halos), `.logo-sub` resized 7px→11px / letter-spacing 5px→2px. Focus-outline regression introduced and fixed: replaced programmatic `target.focus()` with `aria-live` announcement on `#faceLabelCard` (zero visual artifact, same SR experience). SEO + distribution gap closed: 9 marketing pages got 10-tag meta block (description, robots, canonical, og:5, twitter:card 1) sharing `/qc-icon-512.png` as OG image; new `/robots.txt`, `/sitemap.xml` (10 URLs), `/.well-known/assetlinks.json` placeholder for Trusted Web Activity. Landing CTAs `/app.html` → `/app` cleanup. **Sentry: 0 unresolved issues at qc-v208 (verified live).** New ADRs: 015 (ElevenLabs UI semantics — Key ID *is* working credential), 016 (SEO meta-tag minimalism). Audit scores now: 6/8 areas at ⭐⭐⭐⭐⭐, Performance ⭐⭐⭐⭐, Play Store readiness ⭐⭐⭐⭐ (only blocker: real keystore SHA-256 for assetlinks). User triggered the no-`!` zsh history-expansion gotcha mid-session — single-quote message bodies for any commit referencing CSS `!important`.

> **v39 update note (May 5 evening, DevX + analytics + security sprint):** 5 commits shipped (b0d2d92 → d70255b). PostHog product analytics wired (EU project 172921, host `eu.i.posthog.com`, production-only gate, post-Sentry init in app.html). CSP extended: vimeo.com (frame-src), blob: (media-src), eu.posthog.com + eu-assets.i.posthog.com (script-src + connect-src). New DevX foundation: `CLAUDE.md` root pointer, `.claude/skills/` codified workflows (4 skills), `.github/workflows/verify-versions.yml` pre-deploy CI. Tier 1 security audit auto-fixes shipped: GitHub vulnerability-alerts + automated-security-fixes ENABLED; DMARC ramped from `p=none` to `p=quarantine; pct=25; rua=mailto:dmarc@quantumcube.app` (see ADR-012, supersedes ADR-010); branch protection on `main` ENFORCED via gh API (see ADR-014). Doc drift fixed (Cloudflare Pages → GitHub Pages everywhere). Sentry issues JAVASCRIPT-2/4/5 resolved. Supabase MCP capability expanded mid-session: `deploy_edge_function`, `get_logs`, `get_edge_function`, `list_edge_functions`, `merge_branch` now available — chat-side edge function deploys possible without `supabase functions deploy` CLI. Confirmed via app.html audit: app uses passwordless auth exclusively (magic-link + Google OAuth, zero `<input type="password">` exists), so Supabase advisor's leaked-password warning is moot — re-affirms ADR-005. SW: qc-v201 → qc-v202.

> **v38 update note (May 5 PM):** Browser-tab audit pass confirmed system is clean. No new code changes — decisions codified as ADR-009 (Cloudflare orange cloud KEEP OFF, GH Pages cert renewal compat), ADR-010 (DMARC p=none for 30-60 days observation), ADR-011 (Microsoft Clarity project found to be Mobile-platform-only — needs new Website project, deferred to post-launch). UR Supabase REST monitor confirmed paused (free-tier keyword monitoring still requires HTTP 2xx). Auth.users state verified clean (8 legitimate users, no test cleanup needed). See "v37-v38 CONSOLIDATED UPDATES" section.

> **v37 update note (May 5 AM):** Major system-hardening pass spanning two chat sessions. Three Supabase migrations applied (security + perf advisors now clean). UptimeRobot LIVE with 4 monitors + email alerts. Cloudflare and Resend audited via MCP. Email-only alerting confirmed (Telegram deferred). New files added: `DECISIONS.md`, `.github/workflows/daily-health-check.yml`.

📁 **Archived history → see BRIEF_ARCHIVE.md** — full session timeline, all "biggest wins" history blocks, complete legal text, lessons from every session, and Paddle/PayFast punch list (already shipped) live in the archive. This brief stays focused on current working context.

---

## ⚠️ CRITICAL RULE — ALWAYS READ FIRST

**Quantum Cube and QNC Academy are COMPLETELY SEPARATE projects — at the backend/tooling/profile level.**

- Never mix backend code, Supabase projects, API keys, or tool configs between them
- Quantum Cube has its own Supabase project (Frankfurt) — never touch the Academy one (Ireland)
- Quantum Cube has its own ElevenLabs API key — never share or cross-use

**Asset sharing is fine when explicit.** Copying logos/music/audio across projects is permitted when the user approves. The rule targets backend cross-contamination, not file assets.

### 🚫 NOT Quantum Cube's job — do not touch from a Cube chat

- The Academy website (Next.js codebase at `/Users/qnc/Projects/qnc-academy/`)
- The Quantum Integrator (QI) — Academy's branded AI built on Claude Haiku 4.5
- HeyGen cleanup (Academy's own cleanup task)
- Academy's Vercel deployment
- The Academy Supabase project (Ireland, ref `bevaepokvavzmykjmhda`)
- Any `.env.local`, config, or secret from the Academy side

If a Cube chat drifts into any of the above, stop and ask.

---

## 🚦 NEW CHAT? READ CHAT_KICKOFF.md FIRST

The kickoff doc handles session startup, role split between Chat Claude and Cursor Claude, and the golden rules. Read it first, then read this brief for project-specific context.

---

## 🤖 CLAUDE CHAT (you, right now) vs CLAUDE CODE (separate, additive — coming next chat)

**You are Claude Chat — the in-app Claude (web/mobile/Desktop Mac).** This is the surface Ronnie works in. Your capabilities are defined by the connected MCPs and (on Desktop) local extensions. Operate confidently within this scope — do NOT waste time looking for "other ways" or alternative routes; the integrations below are the routes.

**Cloud MCPs (work on every surface — claude.ai web, mobile, Desktop):**
GitHub (`api.githubcopilot.com/mcp/`, custom connector — see v41 note for setup), Supabase, Sentry, PostHog, Linear, Figma (view-only seat), Canva, Resend, Cloudflare, Cloudflare Developer Platform, Dodo Payments, Google Drive, Vercel, Context7, ElevenLabs Agents, Gmail, pdf-viewer.

**Local extensions (Claude Desktop on Mac ONLY — NOT available on claude.ai web/mobile):**
Filesystem, Desktop Commander, Claude in Chrome, Control Chrome, Control your Mac, Read and Send iMessages, Read and Write Apple Notes, Figma (Plugin API write), MS Clarity, Cloudinary.

**Surface check (memory #5):** if Filesystem/Desktop Commander times out for ~4 minutes on a tool call, you are on claude.ai web (not Desktop) — switch surfaces, do NOT retry.

**Claude Code is a separate, additive capability layer being set up in a future chat — NOT YET ACTIVE.** When set up, Claude Code will run in a different operating context (terminal/CLI on the Mac, agentic loop) with its own toolset for deep coding work that's awkward in chat: long-running build/test cycles, multi-file refactors across the codebase, autonomous codebase exploration, agentic debugging. Claude Chat (you) and Claude Code are **complementary, not interchangeable** — like two different team members with different strengths.

**Right now (Claude Chat operating model):**
- Stay within MCP + local-extension scope above
- For big-file edits (>~30K chars), use Desktop Commander → local git push (NOT GitHub MCP `create_or_update_file` — it chokes silently, lesson learned May 7)
- Do NOT assume Claude Code capabilities exist yet
- If a task feels like it needs deep agentic coding (multi-hour refactor, autonomous build/test loop, full-codebase rewrite), flag it as **"Claude Code territory — defer until that's set up"** rather than trying to bash it through chat
- Otherwise: proceed. Read freely, write when obvious, ask before destructive (memory #6, auto-run discipline)

**When Claude Code IS set up (future):**
- This section will be updated to document Claude Code's scope and where the split lands
- A new doc may also be added (e.g., `CLAUDE_CODE.md` or expanded `CLAUDE.md`) covering its own operating model
- Until that update lands, all coding work is Claude Chat's job within current MCPs

---

## 📣 MARKETING — see MARKETING_PLAYBOOK.md

Marketing strategy, launch sequencing, channel playbooks, customer positioning thesis (curious dabbler), shareable cosmic-profile card concept, SEO content strategy, email deliverability plan, tools evaluated, and growth metrics live in the separate marketing playbook.

**Social channel ownership:** Michelle owns all social media posting and interaction from May 4, 2026 (Monday). Brief stays code-focused; Michelle's content workflow lives in the playbook.

---

## STRATEGIC CONTEXT (locked May 3, 2026)

**Team capacity:** 3 full-time partners. Quantum Cube is one of three QNC projects — a launched byproduct with real revenue that can scale on its own, while QNC Academy stays the primary focus and the HR-screening product stays secondary.

**Customer thesis (locked):** Target is the **curious dabbler** (~70-75% of market), not the hardcore astrology enthusiast (~10-15%) or pure gift buyer (~10-15%). The wedge is **simplicity, beauty, one-shot completeness** — not depth. Co-Star wins depth; we don't compete there.

**Product model (locked — supersedes subscription tier plan):** **Multi-product one-time-purchase**. Each new product is its own Dodo product + own `has_paid`-style flag, $17 (Family $25). Planned product line: Quantum Cube (live) → Compatibility → Year Ahead → Tarot → Family. Subscription tier (Quantum Cube Plus, $9.99/mo) is **demoted to "evaluate at month 6 if data supports"**.

**Budget posture:** Money is **not** the limiting factor.

**Timeline posture:** **Aggressive** — meaningful traction on the order of months, not quarters.

**Three legitimate outcome paths** — revisit at month 6 with real channel + revenue data:

1. **Build big** — scale Quantum Cube + sibling products as durable revenue line inside QNC.
2. **Build to flippable** — package documented growth + multi-product portfolio for acquisition.
3. **Build modestly** — sustain on lighter touch + organic while partner capacity stays on Academy + HR.

---

## 🌐 LIVE SITE

`quantumcube.app` is LIVE and accepting real payments since May 2, 2026. Domain pointed at GitHub Pages, SSL active, public landing page + 8 legal pages all responding HTTP 200.

**Live URLs:**

- `https://quantumcube.app/` — public landing page
- `https://quantumcube.app/app` — the cube app
- `https://quantumcube.app/privacy` — privacy policy
- `https://quantumcube.app/terms` — terms of use
- `https://quantumcube.app/refund` — refund policy
- `https://quantumcube.app/disclaimer` — disclaimer
- `https://quantumcube.app/ip` — IP notice
- `https://quantumcube.app/popia` — POPIA / data
- `https://quantumcube.app/security` — security
- `https://quantumcube.app/contact` — contact info

---

## 💳 PAYMENT PROCESSOR — Dodo Payments (LIVE since May 2, 2026)

### Architecture

End-to-end overlay checkout integration. User stays on `quantumcube.app` for the entire payment flow.

1. User taps Pay $17 button on Face 3 lock card
2. Frontend `launchDodo()` calls `dodo-create-session` Edge Function with auth user_id, email, name
3. Edge Function creates Dodo Checkout Session via Dodo's API with `metadata.user_id` embedded
4. Frontend opens overlay via `DodoPaymentsCheckout.DodoPayments.Checkout.open({ checkoutUrl: cks_xxx })`
5. Customer pays inside the overlay (overlay redirects through Dodo's `/status/<id>/succeeded` page)
6. Customer returns to `quantumcube.app/app?payment_id=...&status=succeeded&email=...`
7. `checkDodoReturn()` detects redirect params, strips them, flags `_qcPendingPaymentUnlock = true`, calls `attemptPaymentUnlock()`
8. `attemptPaymentUnlock()` reads session from localStorage directly (Supabase JS client hangs during auth restore), polls profiles via direct REST fetch up to 8x at 1.5s intervals
9. When `has_paid=true` lands (webhook flipped it), `syncUnlockFromProfile()` runs, then `populateFormFromProfile()` + `runCalculation()` fires to land user inside the cube on Face 3
10. Webhook (`dodo-webhook` Edge Function) verifies Standard Webhooks signature via `dodopayments@2.4.1` SDK, updates `has_paid` server-side

### Mode switching

Single `DODO_MODE` constant in `docs/app.html` (~line 2290) and matching `MODE` constant in `dodo-create-session/index.ts` (~line 28). Both must flip together. Supabase secrets (`DODO_PAYMENTS_API_KEY`, `DODO_PAYMENTS_WEBHOOK_KEY`) must also be swapped to match.

**Live + Test product IDs (in Apple Passwords + in code):**

- Test Mode: `pdt_0NdwjT5U975nxTzpogS68`
- Live Mode: `pdt_0Ndx7o41zFEREpoPTyvR2`

**Business ID:** `bus_0NdjpSYtT1ZAbRN6l15dg`

**MoR legal entity:** `Dodo Payments, Inc.` (Delaware-incorporated). Trade name on customer credit card statements: `Dodo Payments`.

**Key files:**

- `docs/app.html` — `launchDodo()`, `checkDodoReturn()`, `attemptPaymentUnlock()`, `_readSessionFromStorage()`, `handleDodoEvent()`, `_resolveDodoSdk()`
- `supabase/functions/dodo-webhook/index.ts` — webhook receiver
- `supabase/functions/dodo-create-session/index.ts` — session minter (rate-limited per-IP since May 4 PM)

### Dodo's permanent strategic role

**Dodo stays the Merchant of Record across surfaces** (web + Android + future iOS where policy allows external checkout). Multi-product expansion: each new product is its own Dodo product, sharing the same Edge Function infrastructure.

---

## 💰 PRODUCT EXPANSION ROADMAP

**Live product:** Quantum Cube — $17 USD, one-time, lifetime access. Numerology + Western astrology + Chinese zodiac + premium AI-narrated content. **Existing buyers retain lifetime access permanently.**

**Planned product line:**

| Product                  | Price | Hook                                                            | Build complexity                                |
| ------------------------ | ----- | --------------------------------------------------------------- | ----------------------------------------------- |
| **Quantum Compatibility**| $17  | You + partner reading. "Send to your S/O" angle.                 | Medium — needs second profile capture + diff logic |
| **Quantum Year Ahead**   | $17  | Annual personalised forecast. Refreshable yearly = revisit hook | Medium — needs date-anchored content generation |
| **Quantum Tarot**        | $17  | One-off tarot session. Standalone, no birth data dependency     | Low-medium — card draw + interpretation logic    |
| **Quantum Family**       | $25  | Family/parent/child compatibility. Gifting angle.               | Medium-high — multi-profile capture, relationship logic |

**Math check:** 50,000 base Cube users × 30% Compatibility attach + 20% Year Ahead attach = ~$1.275M gross vs ~$850k Cube-only.

### Implementation phasing

- **Months 1–3 post-launch:** Focus on growing Quantum Cube. Validate funnel.
- **Month 3–4:** Build Quantum Compatibility (highest attach potential). Soft launch to existing Cube customers.
- **Month 4–5:** Soft-launch Quantum Year Ahead and Quantum Tarot in parallel.
- **Month 5–6:** Quantum Family for gifting season. Re-evaluate full portfolio at month 6.

### Engagement-loop feature: shareable cosmic-profile card

Beautiful single-image PNG summary of the user's reading they can save to phone or share. Drives viral moment + returning-user moment + gifting trigger. Tentative placement: extension of Face 6 with "Save your cosmic card" button. **Slot decision pending** — Phase 2 polish or Phase 6 (months 3-4). Detailed spec lives in MARKETING_PLAYBOOK.md.

### Migration safety

**Existing Cube customers keep lifetime access forever.** Sibling products are purely additive.

### Subscription tier (reserve option, evaluate at month 6)

Quantum Cube Plus ($9.99/mo with daily horoscope generation) is **deferred and demoted**. Reasons: curious-dabbler segment doesn't want a content treadmill; conversion would likely be ~2-3% not 12-15%; daily AI narration scales costs quickly; multi-product approach hits similar revenue without churn.

---

## 📂 FILE LOCATIONS

```
/Users/qnc/Projects/quantumcube/              <- MAIN PROJECT FOLDER
|- docs/                                       <- GITHUB PAGES SOURCE
|   |- index.html                              <- public landing page (CSP applied)
|   |- app.html                                <- THE CUBE APP (~350KB, ~3197 line for runCalculation)
|   |- styles.css                              <- shared Cinzel + Cormorant dark cosmic styling
|   |- manifest.json                           <- static PWA manifest
|   |- privacy.html / terms.html / refund.html         (CSP applied)
|   |- disclaimer.html / ip.html / popia.html          (CSP applied)
|   |- security.html / contact.html                    (CSP applied)
|   |- sw.js                                   <- Service worker (current: qc-v223)
|   |- CNAME                                   <- quantumcube.app
|   |- .nojekyll
|   |- qc-icon-192.png / qc-icon-512.png / qc-icon-512-maskable.png
|   |- qc-apple-touch-180.png / qc-favicon-32.png
|   |- Sounds/                                 <- 385 narration MP3s + 5 music tracks
|   - cube-background.jpg                      <- Milky Way background
|- brand/                                      <- QC monogram + wordmark pack
|- supabase/
|   |- config.toml                             <- 6 functions: narrate, delete-account, export-data, dodo-create-session, dodo-webhook, resend-events
|   |- migrations/
|   |   |- 20260417104424_create_profiles_table_and_rls.sql
|   |   |- 20250429140000_narrate_rate_limit.sql
|   |   - 20260430164143_add_dob_name_to_profiles.sql
|   - functions/
|       |- narrate/index.ts                    <- ElevenLabs proxy with rate limit
|       |- delete-account/index.ts             <- Auth admin delete (rate-limited per-user)
|       |- export-data/index.ts                <- Profile JSON export (rate-limited per-user)
|       |- dodo-create-session/index.ts        <- Dodo session minter (rate-limited per-IP)
|       - dodo-webhook/index.ts                <- Dodo webhook receiver
|- scripts/                                    <- Narration pipeline scripts
|- narration-manifest.json                     <- 385 entries
|- PROJECT_BRIEF.md                            <- This document (v39, lean active brief)
|- BRIEF_ARCHIVE.md                            <- Lossless reference archive
|- MARKETING_PLAYBOOK.md                       <- Marketing strategy + Michelle's playbook
|- CHAT_KICKOFF.md                             <- Chat operating protocol
|- .supabase-env                               <- creds (gitignored, glob pattern .supabase-env*)
|- .cursorrules                                <- Cursor project rules
- .gitignore
```

**GitHub Repo:** `https://github.com/quantumneurocreations-dot/quantumcube`
**Pages source:** `/docs` directory on `main` branch

---

## 🧭 RECENT SAFE ROLLBACK POINTS

(Older anchors live in BRIEF_ARCHIVE.md.)

| Commit    | Why you don't revert past it                                                    |
| --------- | ------------------------------------------------------------------------------- |
| `d70255b` | smoke.sh exec bit restored after doc commit lost it.                              |
| `d7ee696` | **Doc drift fix** — "Cloudflare Pages" → "GitHub Pages" across CLAUDE.md, skills, verify-versions.yml, smoke.sh. |
| `059542c` | **PostHog wired + CSP fixes** (qc-v202). Vimeo, blob: media, PostHog hosts added to CSP. |
| `b0d2d92` | **DevX foundation** — CLAUDE.md, .claude/skills/, pre-deploy verify-versions.yml CI. |
| `7fb5a73` | **CHAT_KICKOFF v4.0.0** — mandatory boot sequence + First Response Template + hardened handoff (now v4.1 with expanded MCP). |
| `fc479a0` | **Smoke test simplified to 4 checks** — Step 2 release-tag check covers Sentry block + version. Reliable green run. |
| `00a6314` | **Pre-commit hook** — SW + Sentry release sync; blocks `app.html` without SW bump. Run `./scripts/install-hooks.sh` on new clone. |
| `23d4a20` | Smoke test script landed (refined in 4efb70a, 90fb8b9, fc479a0).                 |
| `6c3cdf7` | **CHAT_KICKOFF.md** — MCP readiness, brief/archive sync rule, reusable paste blocks. |
| `5f8670f` | `.cursorrules` — Context7 MCP auto-fire for library/SDK docs.                   |
| `3027a87` | `BRIEF_ARCHIVE.md` — May 4 EVENING session record (lossless).                    |
| `9bcf2d3` | **Brief v34** — security audit complete (4 commits: rate limits, CSP, CSP fix-up, mobile-web-app-capable). |
| `1324784` | mobile-web-app-capable meta tag added (iOS deprecation fix). SW qc-v201.        |
| `00d1c6c` | CSP fix-up: Sentry CDN connect + Vimeo thumbnail img-src.                       |
| `f6a7db5` | **CSP baseline shipped** — 10 pages, securitypolicyviolation listener → Sentry. |
| `35331bf` | **Edge Function rate limits** — delete-account, export-data, dodo-create-session + tightened error responses across all 5. |
| `1b15ece` | Live Mode active after magic-link E2E test pass (May 4 PM).                     |
| `4b6bdf9` | Multi-number narration shipped (Hidden Passion + Karmic Lessons).               |
| `b99b807` | SW skips caching 206 partial-content responses — Sentry's first real catch.    |
| `730d4d8` | **Sentry error monitoring shipped** — production-only, EU region.               |
| `3f7f297` | Brand cyan refresh across logo variants.                                        |
| `e804ab4` | Brief v32 + new BRIEF_ARCHIVE.md — lossless history split.                      |
| `e85ca5c` | **Post-payment auto-runCalculation** — bounce-bug fix. Verified May 4 PM for both auth paths. |
| `7ff5db8` | 17-line Paddle/PayFast → Dodo legal copy swap.                                  |
| `b3386ea` | dodo-webhook Edge Function source.                                              |

When in doubt, `git revert <commit>` a specific bad change rather than resetting through these anchors.

---

## ✅ PAYWALL VERIFICATION PROTOCOL — 4-LAYER DEFENCE

1. `STORE_KEY` is user-scoped (commit `fd41b68`)
2. `syncUnlockFromProfile` unconditionally enforces lock branch for unpaid (commit `2403ca7`)
3. `renderAllContent` gates all 4 face-reveal blocks on `isUnlocked` (commit `0bd5a54`)
4. **Database-level RLS lock on `has_paid` column** (in migration `20260417104424` — `with check` clause prevents user from updating their own `has_paid`)

### Test sequence (run on live `quantumcube.app/app`)

Two test profiles in `public.profiles`:
- `quantumneurocreations@gmail.com` — `has_paid=true`
- `carlkelbrick@gmail.com` — `has_paid=false`

Use **regular Chrome** (not PWA) with **DevTools open**.

1. Clean start: Application → Storage → Clear site data. Hard-refresh.
2. Unpaid test: Sign in as carl. Face 3 must show Lock card with $17 button. Refresh — lock card must STAY.
3. Switch to paid: Sign Out → sign in as quantumneurocreations. Full content visible.
4. Tab close + reopen (paid): Should auto-advance, unlocked.
5. Switch back to unpaid: Lock card must appear again.

---

## TECH STACK (LOCKED)

- **Frontend:** Single HTML file at `docs/app.html`, vanilla JS, CSS3 3D transforms, glassmorphism. **File size: ~350 KB, ~3197 line for runCalculation.**
- **Public site:** static HTML pages at `docs/index.html` + 8 legal pages, shared `docs/styles.css`. All 9 public pages have strict CSP applied.
- **PWA Manifest:** static file at `docs/manifest.json`. Real PNG icons (192/512/512-maskable). Background + theme color: `#05050f`.
- **Fonts:** Cinzel Decorative, Cinzel, Cormorant Garamond — Google Fonts CDN only
- **Auth:** Supabase magic-link (email OTP) + Google OAuth, SDK v2.45.4 UMD
- **Database:** Supabase Postgres (Frankfurt) — `public.profiles` with RLS, `public.narrate_rate_counters`
- **Email:** Resend via custom SMTP on Supabase
- **Payment:** Dodo Payments overlay SDK (LIVE). MoR. Adaptive Currency ON. Visa Rapid Dispute Resolution ON.
- **Videos:** Vimeo Player API
- **Audio:**
  - **Music:** 5 tracks in `Sounds/Music/` — randomised playback, no-immediate-repeat, ducks to 6% during narration
  - **SFX:** 5 active (reveal_my_cube, select_side, reveal_result ×3, payment, back_to_signup)
  - **Narration:** 385 pre-recorded Valory MP3s — all Face 3/4 narration + welcome greeting; live Edge Function fallback for Face 5 ONLY
- **Haptics:** 3× strength
- **Hosting:** GitHub Pages (source: `/docs` directory on `main`)
- **Custom domain:** `quantumcube.app` via Cloudflare CNAME → `quantumneurocreations-dot.github.io`
- **Email routing:** Cloudflare `*@quantumcube.app` → `admin@qncacademy.com`
- **Error monitoring:** Sentry browser SDK 8.50.0, EU region (`o4511330222604288.ingest.de.sentry.io`), production-only gate, error monitoring only (no Session Replay/Tracing/Application Metrics), JWT/email scrubbing in `beforeSend`, release tagged per SW version. Free tier (5k errors/month). CSP violation listener wired to forward as Sentry warnings.
- **Product analytics:** PostHog EU (project 172921, host `https://eu.i.posthog.com`, asset host `eu-assets.i.posthog.com`). Production-only gate (`location.hostname !== "quantumcube.app"` short-circuits init). Wired in `app.html` AFTER Sentry init, BEFORE Supabase client. Public client API key (safe to commit, by design): `phc_sXjrkSUy6SAFddX69V53HGEegVKPUpRjpUEsERF6wcVk`. Autocapture ON. Person ID anonymized until `posthog.identify(user_id)` wired (deferred — paid users only).
- **Content Security Policy:** applied to all 10 HTML pages via `<meta http-equiv>`. App page allows inline scripts (existing inline handlers); public pages strict (no inline, no external scripts). Allow-list covers Vimeo (player.vimeo.com + vimeo.com), jsdelivr, Sentry CDN + ingest, Supabase, Dodo, Google Fonts, PostHog (eu.i.posthog.com + eu-assets.i.posthog.com), blob: (media-src for narration).
- **PWA:** Real `sw.js` file + static `manifest.json` with PNG icons. Two-cache architecture:
  - `qc-v223` — HTML + root assets (skips caching of HTTP 206 partial-content responses since `b99b807`; bypasses `audit-narration.html` per ADR-022)
  - `qc-narration-v3` — 385 MP3s

---

## 🎙️ ELEVENLABS NARRATOR

- **Voice:** Valory (voice ID `VhxAIIZM8IRmnl5fyeyk`)
- **Production voice settings (LOCKED, ADR-021):** model `eleven_turbo_v2_5`, stability 0.5, similarity_boost 0.75, speed 1.15
- **Welcome greeting exception:** speed 1.00 (slower) — re-rendered May 3 (`5a382ff`)
- **Dashboard voice profile is NOT authoritative** — `scripts/rerecord.py` carries the canonical settings; the dashboard has been edited and may drift
- **Re-record tooling:** `scripts/rerecord.py` reads the manifest, applies per-category TTS-payload transforms (Karmic Lesson digit→word, Hidden Passion em-dash padding, chin_ox phonetic Ox→Ocks, Life Phase opening rephrase — see ADR-023), POSTs ElevenLabs direct, emits SHA256 JSON for manifest update. Edit `FILES`, dry-run, run.
- **Edge Function:** `supabase/functions/narrate/index.ts` (rate-limited, `verify_jwt=false`)
- **Rate limit:** 5/min + 20/hr per IP. Returns HTTP 429 with `Retry-After`.
- **Inventory:** 385 MP3s on disk — full library at production settings as of May 9, 2026 (qc-v223). 98 re-recorded this session, 287 untouched originals match.
- **Live Edge Function only fires for Face 5** (combined results) — ONLY credit-burn path at runtime
- **Audit tool:** `https://quantumcube.app/audit-narration.html` — embeds the full manifest, lets you flag bad files for re-record. Always served network-only (SW bypassed per ADR-022).

Full narration paths + generation pipeline detail in BRIEF_ARCHIVE.md.

---

## 🔧 EDGE FUNCTIONS — current state

All 5 deployed, all use `verify_jwt = false` in `supabase/config.toml` + manual JWT/signature handling + CORS headers + service-role key from Edge Function env vars. **All 5 return generic error codes only — full errors stay in `console.error` for log access.**

### `narrate` (rate-limited)

- ElevenLabs proxy, Postgres-RPC rate limit (5/min + 20/hr per IP)
- Returns 503 + `rate_limit_unavailable` if RPC fails (fail-closed)
- ONLY credit-burn path at runtime (Face 5 only)

### `delete-account` (rate-limited per-user, May 4 PM)

- Verifies user JWT via `getUser(jwt)` — never trusts client-supplied user id
- **Per-user rate limit: 2/min, 5/hr** via `narrate_rate_limit_try` RPC with `delete:USER_ID` bucket key
- Calls `auth.admin.deleteUser(userId)` server-side
- Cascades to `public.profiles` via `on delete cascade` FK
- Frontend wraps signOut in `Promise.race([signOut, 3000ms])` to prevent hang

### `export-data` (rate-limited per-user, May 4 PM)

- Verifies user JWT
- **Per-user rate limit: 5/min, 20/hr** via `narrate_rate_limit_try` RPC with `export:USER_ID` bucket key
- Returns profile JSON with `Content-Disposition: attachment` header
- POPIA Section 23 / GDPR Article 15 compliance

### `dodo-create-session` (rate-limited per-IP, May 4 PM)

- Mints Dodo Checkout Session URLs (`cks_xxx`) server-side
- Embeds `metadata.user_id` for webhook profile matching
- Defence-in-depth check: confirms user exists in profiles before minting
- **Per-IP rate limit: 5/min, 20/hr** via `narrate_rate_limit_try` RPC with `dodo-session:IP` bucket key. IP read from `x-forwarded-for` then `cf-connecting-ip`.

### `dodo-webhook`

- Receives `payment.succeeded` and `refund.succeeded` events
- Verifies signature via Standard Webhooks SDK
- Updates `has_paid` in profiles

### `resend-events` (added May 8 PM)

- Receives Resend webhook events. Subscribed: `email.bounced`, `email.complained`, `email.delivery_delayed`. All other event types (delivered/opened/clicked) are 200-acked but not forwarded — they would burn Sentry quota with no actionable signal.
- Verifies Standard Webhooks signature via `standardwebhooks@1.0.0` (svix-id / svix-timestamp / svix-signature). Hard-fails 503 if `RESEND_WEBHOOK_SECRET` unset — never accepts unverified webhooks.
- Forwards critical events to Sentry as JSON via Store API: `email.bounced` → warning, `email.complained` → error, `email.delivery_delayed` → info. Includes recipient, bounce type, email_id, subject in `extra` payload. Sentry forwarding is best-effort; webhook always 200-acks so Resend doesn't retry.
- Webhook id in Resend dashboard: `2a5c62b4-7e5c-42eb-bdeb-fbe56bcdc8f9`. Endpoint: `https://fqqdldvnxupzxvvbyvjm.supabase.co/functions/v1/resend-events`.
- No rate limit needed — Standard Webhooks signature verification is the rate limit (attackers can't generate valid signatures).

### Pattern for adding new rate-limited Edge Functions

Reuse the existing `narrate_rate_limit_try` RPC. No new migration needed. Pick a unique bucket key prefix (e.g. `<function-name>:USER_ID` for per-user, `<function-name>:IP` for per-IP). The RPC returns `{ ok: true }` or `{ ok: false, reason, retry_after }`.

---

## 🛡️ SENTRY ERROR MONITORING (live since May 4)

### Account + project

- **Org:** `quantum-neuro-creations`
- **Project:** Browser JavaScript (Sentry slug `javascript-1`)
- **Region:** EU (Frankfurt-aligned with Supabase + Resend for GDPR consistency)
- **DSN** (public, safe — embedded in code): `https://fc0733d091a210fe80f9213b64fafa8e@o4511330222604288.ingest.de.sentry.io/4511330235908176`
- **Trial:** Auto-started 14-day Business trial on signup (May 4). **Set calendar reminder for May 18** to verify auto-downgrade to free tier landed without surprise billing. Free tier covers 5k errors/month — plenty for early launch.

### Configuration (in `docs/app.html` ~line 500)

- **Production gate:** Only initialises on `quantumcube.app` hostname. Local dev / test environments produce zero Sentry traffic.
- **Error monitoring ONLY:** `tracesSampleRate: 0`, `replaysSessionSampleRate: 0`, `replaysOnErrorSampleRate: 0`. No Session Replay (privacy + quota burn). No Tracing. No Application Metrics.
- **Release tag:** Set to current SW version (`quantum-cube@qc-vNNN`). MUST be bumped together with SW version on every commit that touches `app.html`.
- **PII scrubbing:** `sendDefaultPii: false` + `beforeSend` filter regex-scrubs anything resembling JWT or email address before payload leaves browser.
- **Noise filters in `beforeSend`:** drops common browser-extension errors, `ResizeObserver loop limit exceeded`, generic cross-origin "Script error.", and "Non-Error promise rejection captured".
- **CSP violation listener** (added May 4 PM): `securitypolicyviolation` event handler forwards directive + blocked URI to Sentry as a warning. Surfaces silently-blocked external dependencies.

### Email alerts

Default Sentry rule sends an email to the account owner on first occurrence of any new issue class. Confirmed working May 4.

---

## 🔊 AUDIO SYSTEM — QC_AUDIO

**Music:** 5-track rotation in `docs/Sounds/Music/`. Randomised on first play AND on each track-end, avoiding immediate repeat. **0.20 baseline volume, ducks to 0.06 during narration** (commit c3d3e57). 300ms duck-down, 600ms duck-up. First-tap auto-start, fades, Vimeo pause-on-play.

**SFX:** 5 files at 0.30 vol, wired to 5 triggers: `reveal_my_cube`, `select_side`, `reveal_result` (random per call), `payment`, `back_to_signup`.

**Haptics:** 3× strength.

---

## 📧 EMAIL INFRASTRUCTURE — Resend

- Resend `admin@qncacademy.com`, domain `quantumcube.app` verified
- eu-west-1, free tier 3000/mo, 100/day
- DNS: DKIM, SPF, DMARC (p=none), MX send subdomain
- Supabase SMTP: `noreply@quantumcube.app`, `smtp.resend.com:465`, 60s min interval
- Magic-link HTML template applied. Full template in BRIEF_ARCHIVE.md.

`support@quantumcube.app` → `admin@qncacademy.com` via Cloudflare email routing.

**Resend webhook → Sentry (added May 8 PM, ADR-018):** Edge Function `resend-events` subscribed to `email.bounced` / `email.complained` / `email.delivery_delayed`. Bounce/complaint events post to Sentry as warnings/errors with full context. Webhook id `2a5c62b4-7e5c-42eb-bdeb-fbe56bcdc8f9`, signing secret in Supabase as `RESEND_WEBHOOK_SECRET`. Closes the "Webhooks: NONE configured" gap from earlier audits.

**Resend API key local backup:** intentionally not held locally — Resend hides values after creation, and rotating to capture is a 5-minute job if ever needed. Documented decision May 4 PM. Dedicated key `quantum-cube-dodo-webhook` (id `5b36c8df-645e-4a77-bc25-a060ad22b161`) created May 8 PM and stored in user's Apple Passwords — see SESSION_LOG.md and ADR-018.

---

## APP STRUCTURE — 7 FACES + INTERSTITIAL

| Face           | Name                                  | Card label          | Notes                                            |
| -------------- | ------------------------------------- | ------------------- | ------------------------------------------------ |
| Face 0         | Entry / Sign Up Form                  | —                   | Settings gear visible bottom-left here too       |
| faceCheckEmail | "Check Your Email" interstitial       | —                   |                                                  |
| Face 1         | Introduction video + Welcome greeting | **Introduction**    | Welcome plays once on first signed-in entry      |
| Face 2         | Results Explained videos              | **Videos**          |                                                  |
| Face 3         | Numerology Results                    | **Your Numbers**    | Locked unless paid                               |
| Face 4         | Astrology & Horoscope                 | **Stars and Signs** | Locked unless paid                               |
| Face 5         | Combined Results                      | **Combination**     | Locked unless paid. ONLY live TTS path           |
| Face 6         | Complete / Outro video                | **Complete**        |                                                  |
| Face 7         | Settings                              | —                   | Sign Out, Download My Data, Delete Account, Back |

**Settings discoverability:** ✅ gear icon present bottom-left, locked across every face including Face 0. Click → Face 7. Verified May 4 PM by Ronnie.

---

## SUPABASE BACKEND

- **Project:** quantum-cube (ref `fqqdldvnxupzxvvbyvjm`)
- **Region:** Central EU (Frankfurt)
- **Schema:**
  - `public.profiles` (id, email, name, dob, has_paid, marketing_consent, created_at)
  - `public.narrate_rate_counters` + `narrate_rate_limit_try` RPC (now used by 4 functions, not just narrate)
- **RLS:** Enabled. 3 profiles policies, `has_paid` locked from client via column-level `with check` clause
- **Trigger:** `on_auth_user_created` → `handle_new_user()` auto-creates profile on auth signup, captures dob + name from `raw_user_meta_data`
- **Cascade FK:** `profiles.id` → `auth.users.id` `on delete cascade`
- **Edge Functions deployed:** narrate ✓, delete-account ✓, export-data ✓, dodo-create-session ✓, dodo-webhook ✓, resend-events ✓
- **Secrets configured (10):** DODO_PAYMENTS_API_KEY, DODO_PAYMENTS_WEBHOOK_KEY, ELEVENLABS_API_KEY, SUPABASE_ANON_KEY, SUPABASE_DB_URL, SUPABASE_JWKS, SUPABASE_PUBLISHABLE_KEYS, SUPABASE_SECRET_KEYS, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_URL. CLI `supabase secrets list` shows SHA-256 digests, never values.

**Test/team data cleanup:** ✅ COMPLETE as of May 5. auth.users state verified: 8 legitimate users remaining (1 paid: Ronnie's main; 5 real-looking; 2 Kelbrick-pattern accounts that may be Ronnie's dev/test — kept). No further test cleanup needed pre-launch.

---

## FRONTEND WIRING — KEY LINE REFS

**Numbers float — anchor by function/const name not line number when possible.** Snapshot from May 4 PM (post-CSP + meta-tag commits):

| What                                                    | Approx line in `docs/app.html`                |
| ------------------------------------------------------- | --------------------------------------------- |
| `function runCalculation`                               | **~3197** (STABLE ANCHOR — verified May 4 PM) |
| const sb = window.supabase.createClient                 | ~514                                          |
| Sentry init                                             | ~520                                          |
| `securitypolicyviolation` listener                      | ~551                                          |
| Static manifest link                                    | ~17                                           |
| Favicon link (qc-favicon-32.png)                        | ~25                                           |
| Apple touch icon (qc-apple-touch-180.png)               | ~26                                           |
| `apple-mobile-web-app-capable` + `mobile-web-app-capable` | ~9-10                                       |
| `Content-Security-Policy` meta tag                      | ~6 (right after charset)                      |
| `#faceLabelCard` HTML                                   | ~570                                          |
| `.face-label-text` CSS (Cinzel, weight 400)             | ~426                                          |
| `.export-btn` / `.delete-btn` CSS                       | ~290-297                                      |
| `.scoreboard` / `.sb-grid` / `.sb-item` / `.sb-num` CSS | ~202-213 (DUPLICATE blocks — see Fragile)     |
| `.sb-num.sb-num-count-N` CSS scaling rules              | ~210-215                                      |
| `.astro-grid` / `.astro-item` / `.astro-sign` CSS       | ~221-226                                      |
| `.mc` / `.mc-d` matrix card CSS                         | ~212-216                                      |
| QC_AUDIO with duckMusic / unduckMusic                   | ~1008+                                        |
| `_musicTracks` array (5 entries, randomised)            | ~1012                                         |
| `fetchNarration` (Edge Function, Face 5 only)           | ~1438+                                        |
| `startNarration` / `startNarrationFromUrl`              | ~1455+ / ~1463+                               |
| `playSequence` (Life Phases + multi-num cards)          | ~1480+                                        |
| `qcNarrateCard` (Face 3 + Face 4 dispatch)              | ~1498+                                        |
| `playWelcomeGreeting`                                   | ~1580+                                        |
| `showFace(n)`                                           | ~1610+                                        |
| NUM data                                                | ~1620+                                        |
| STORE_KEY const                                         | ~2240+                                        |
| `async function checkStoredUnlock`                      | ~2250+                                        |
| `syncUnlockFromProfile`                                 | ~2270+                                        |
| applyUnlockedState                                      | ~2300+                                        |
| Dodo overlay SDK constants (`DODO_MODE` etc)            | ~2290                                         |
| handleRevealClick                                       | ~2400+                                        |
| signInWithOtp paths                                     | ~2940 / ~3008                                 |
| signInWithOAuth (Google)                                | ~2867                                         |
| sb.auth.onAuthStateChange                               | ~2550+                                        |
| signOut                                                 | ~2700+                                        |
| `_wipeAllLocalState`                                    | ~2710+                                        |
| `exportMyData` / `armDeleteAccount` / `confirmDeleteAccount` | ~2720+ / ~2760+ / ~2780+               |
| `renderAllContent` + 4× `if(isUnlocked){}` reveal gates | ~2880+                                        |
| SW registration                                         | ~3070+                                        |

Lines drift +1-2 per added meta tag / listener. `runCalculation` and named functions are the reliable anchors.

---

## 🔐 AUTH + UNLOCK FLOW

### Session handling

- `persistSession: true`, `detectSessionInUrl: true`, `flowType: "implicit"`
- Session persists in localStorage until explicit signOut
- Closing tab + reopening → auto-advances into app
- Magic-link short-circuit: if session email matches form email → skip magic link
- Mismatched email → signs out session first, fires new magic link
- **Google OAuth path:** brand-new user has email pre-filled+locked + name pre-filled, fills DOB. Returning user auto-fills + runs into cube directly.

### Unlock state — 4-layer defence

(See PAYWALL VERIFICATION PROTOCOL above.)

`applyUnlockedState` hides .lock-screen, reveals face-content — only callable after paid confirmed.

### Account deletion

- Two-tap confirmation pattern (5-second arm window)
- Edge Function admin-deletes user via service-role key (rate-limited per-user since May 4 PM)
- Cascade FK wipes profile row automatically
- Frontend wipes 6 localStorage keys (STORE_KEY, QC_PENDING_KEY, qc_musicIdx, qc_rotIdx, qc_greet_count, qc_greet_count_)
- `Promise.race(signOut, 3000ms)` prevents hang
- Redirects to `/` (landing) on completion

### Data export

- Single-tap from Settings (Face 7)
- Returns JSON with email, has_paid, marketing_consent, timestamps (rate-limited per-user since May 4 PM)
- Browser downloads as `quantum-cube-data.json`
- POPIA right of access compliance

### Known remaining UX issues (not launch-blocker)

- Sign out + sign back in as same email same device still fires magic-link. Post-launch polish.
- **Magic-link from Gmail opens in user's default Chrome profile, not the same incognito/window session.** Real-user behavior — doesn't break the flow (verified May 4 PM E2E test) but worth documenting. Both OAuth and magic-link auth paths confirmed working through the post-payment unlock flow.

---

## 🪨 FRAGILE AREAS — DO NOT TOUCH CASUALLY

- **Service worker is a real file** (`sw.js`). Do NOT revert to blob URL — Android Chrome 117+ rejects blob SW silently.
- **Static manifest.json is a real file** (`docs/manifest.json`). Do NOT revert to blob URL — PWABuilder cannot read blob URLs.
- **`@media (min-width:600px)` rules** are desktop-only on mobile — any CSS change inside those media queries is invisible on Ronnie's phone. Base rules apply to mobile.
- **CSS Grid items default to `min-width:auto`** — children can blow out the cell. Add `min-width:0` on grid item CSS to defeat. Recipe burned in: `.mc`, `.astro-item`, `.sb-item` all use this pattern.
- **`.scoreboard` / `.sb-item` / `.sb-num` CSS is DUPLICATED** at lines ~202-207 AND ~208-213 in app.html. Any edit to these rules MUST hit both copies (or use a Python script that counts both). Phase 3 cleanup target.
- **BSD sed can't do multi-line replacements** — use Python one-shot. Never iterate.
- **Python anchor strings MUST be re-grepped against current file state** before each script run — never reuse anchors from earlier recon output. Cost both `c3d3e57` and `63684ef` corrections. Cursor self-correction welcomed.
- **Diff-then-delete logic must have explicit branches** — `if identical → delete; else → halt and ask`. Never let "diff returned different" fall through to delete (would have lost ElevenLabs key in May 4 cleanup).
- **`grep -c` returns exit 1 on zero matches** — kills pipelines silently. Use `|| true`.
- **`head -N` piped after `git log` can trigger SIGPIPE (exit 141)** on macOS. Use `|| true`.
- **`grep` with `\|` alternation unreliable on BSD grep.** Use `grep -E` with `|` for extended regex.
- **Service worker cache bump is mandatory** every commit that changes `docs/app.html` or `docs/manifest.json`. Sentry release tag in `Sentry.init()` MUST stay synced with SW cache version.
- **PWA cache stickiness:** "it's not working on my phone" is usually cache or SW install timing, not code. Triage: (1) regular Chrome tab not PWA, (2) Force-stop PWA / Clear storage on Android, (3) Test in regular Chrome to bypass PWA, (4) Uninstall + reinstall PWA.
- **Magic-link must open in main Chrome**, not Gmail's internal browser. Session won't match.
- **Never reintroduce base64 assets** — 10.8MB cleanup reduced file from 11MB to ~350KB.
- **Life Phases is sequential playback** via `playSequence`. Do not convert to 3 separate cards without product approval.
- **Master numbers in NUM.pc are stripped** (commit `636e3d8`). Do not re-add.
- **renderAllContent reveal blocks MUST stay gated on `if(isUnlocked){}`** — removing the gate re-introduces paywall bypass.
- **GitHub Pages source is `/docs` directory.** Do NOT add HTML to repo root expecting it to be served.
- **`docs/CNAME` binds the custom domain.** Removing it breaks `quantumcube.app`.
- **Files can be silently `.gitignore`d for weeks.** Run `git ls-files <path>` to verify deployment, not local presence.
- **JWTs / bearer tokens NEVER paste into Cursor or chat** — debug via DevTools console + Promise.race timeouts. Cursor's refusals on this are correct.
- **NEVER paste secret values into chat — Cursor terminal output included.** A `supabase secrets set` echo leaked the Live API key on May 2. Rotate FIRST in dashboard, then re-set without echo.
- **Edge Functions need `verify_jwt = false` in `supabase/config.toml`** if they handle JWT manually — otherwise Supabase returns 401 before the function runs.
- **Supabase Edge Functions don't expose `Deno.openKv()`.** Use Postgres RPC for state instead.
- **Supabase JS auth methods can hang during INITIAL_SESSION restore.** For UX-critical post-redirect flows, bypass the JS client: read session from localStorage directly + query via REST fetch.
- **Cross-domain redirect kills queued JS state.** Drive post-payment unlock from URL params on page-load, not from overlay callbacks.
- **`window.location.reload()` after detecting payment params can wipe localStorage mid-restore.** Use in-place state update instead.
- **Cursor IDE buffer can race with shell-side Python edits, silently dropping changes between successful grep verification and `git commit`.** Mitigation: every commit touching mode/version constants must run a pre-stage verification grep RIGHT BEFORE `git add` — use the pattern from `9062eef`'s commit block (`if both in sync → ship; else → exit 1`).
- **Three-place mode flips (`DODO_MODE` + Edge `MODE` + Supabase secrets) MUST stay in sync.** Mismatch causes confusing 401 errors and can leave Live Mode broken for real customers.
- **Incognito Chrome localStorage persists across same-session windows.** Only quitting all incognito windows clears it. Mitigation for testing: quit ALL incognito windows + reopen fresh, OR verify `localStorage` keys are empty before starting auth tests.
- **HTTP 206 partial-content responses cannot be cached via Cache API.** SW must guard `cache.put()` with `if (resp.ok && resp.status !== 206)` (fixed in `b99b807`). Don't reintroduce.
- **Don't paste literal multi-line shell commands from chat.** Newlines can render as `\n` characters → zsh parse error → `secrets set` silently fails. Type commands manually OR confirm clean paste before hitting Enter.
- **CSP allow-list extension required when adding new external dependencies.** Two CSP meta tags exist: a permissive one in `docs/app.html` (allows Vimeo, jsdelivr, Sentry CDN, Sentry ingest, Supabase, Dodo, Google Fonts) and a strict one in the 9 public pages (Google Fonts only). Adding any new CDN script, font host, fetch endpoint, or iframe source means updating the right CSP. Violations forward to Sentry as warnings via the `securitypolicyviolation` listener — check Sentry inbox after introducing any new external dep.
- **Edge Function error responses MUST stay generic.** Pattern: `console.error("function-name error:", e)` server-side, return `{ error: "specific_code" }` to client. Never leak raw error strings, stack traces, or upstream service errors back to the browser.

### Supabase CLI gotchas

- `supabase db execute --project-ref` does not exist. Use `supabase db query --linked "SQL"` from linked project directory.
- `supabase functions logs` requires CLI v2.95+. We have v2.90.0 — use dashboard for logs.
- For CSV output: `-o csv`, NOT `--csv`.

---

## 🛡️ PRE-LAUNCH SECURITY AUDIT — ✅ COMPLETED May 4, 2026 PM

Four commits shipped today closed the audit:

| Commit    | Bucket                                                                    |
| --------- | ------------------------------------------------------------------------- |
| `35331bf` | **Auth + abuse:** rate limits added to delete-account (per-user 2/min, 5/hr), export-data (per-user 5/min, 20/hr), dodo-create-session (per-IP 5/min, 20/hr). All 5 Edge Functions now return generic error codes only — full errors in `console.error` server-side. |
| `f6a7db5` | **Frontend security:** CSP applied to all 10 HTML pages. App.html permissive (allows existing inline handlers); 9 public pages strict (no inline, no external scripts). `securitypolicyviolation` listener forwards CSP violations to Sentry. |
| `00d1c6c` | CSP fix-up: Sentry CDN connect + Vimeo thumbnail img-src (caught on first deploy by the listener it set up). |
| `1324784` | `mobile-web-app-capable` meta tag added alongside the deprecated apple-prefixed form (iOS 16+ compliance). |

### Manual checks completed May 4 PM

- **zsh history scan:** 3969 lines, 0 matches across 5 secret-shape patterns. No leaked tokens lingering.
- **Apple Passwords inventory:** Dodo Test+Live API keys, Test+Live webhook signing secrets, Test+Live product IDs, Google account credentials, Mac recovery key all backed up.
- **Supabase secrets confirmed (10):** DODO_PAYMENTS_API_KEY, DODO_PAYMENTS_WEBHOOK_KEY, ELEVENLABS_API_KEY, SUPABASE_ANON_KEY, SUPABASE_DB_URL, SUPABASE_JWKS, SUPABASE_PUBLISHABLE_KEYS, SUPABASE_SECRET_KEYS, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_URL.
- **Resend API key:** intentionally not held locally (Resend hides values after creation, rotate-to-capture is 5 min if ever needed). Documented in Email Infrastructure section.

### Items intentionally deferred

- **dodo-create-session JWT verification:** currently trusts body-supplied `user_id`. Theoretical risk: attacker could pay $17 and unlock someone else's account — financially they'd lose $17, target gets free access. Real-world risk near zero. Defer until we have a reason.
- **innerHTML refactor (7 spots in app.html):** all 7 source from internal data tables (NUM, WSIGN, CSIGN) or computed numbers — never raw form input. `fullName` always goes via `textContent`. Verified no user-input → innerHTML flow. No refactor needed.
- **Inline script removal in app.html:** would require multi-hour refactor. CSP allows `'unsafe-inline'` for app.html only; 9 public pages stay strict.

---

## WHAT'S LEFT — ORDERED BY PRIORITY

### ✅ LAUNCH ACHIEVED — May 2, 2026

Quantum Cube is live and accepting real payments. Phase 2 polish substantially complete.

### 🟥 PRE-MARKETING-PUSH

- ✅ ~~OWASP-style pre-launch security audit~~ **COMPLETED May 4 EVENING** (4 commits: `35331bf` rate limits + error tightening, `f6a7db5` CSP baseline, `00d1c6c` CSP fix-up, `1324784` mobile-web-app-capable). Sentry caught two real CSP gaps within hours of deploy.
- ✅ ~~Pre-commit hook (SW + Sentry release sync)~~ **SHIPPED `00a6314`** May 4 EVENING. Self-tested + installed locally on Mac.
- ✅ ~~Post-deploy smoke test script~~ **SHIPPED `fc479a0`** May 4 EVENING. 13/13 green from residential IP. Run `./scripts/smoke.sh` after every push.

- **Full app walkthrough QA pass** — every face, every state, OAuth + magic-link, paid + unpaid. Casual ongoing as you use the app.

(Security audit, Sentry, multi-narration, magic-link E2E, settings gear icon, mobile-web-app-capable — all shipped.)

### ⚠️ HIGH-VALUE (not launch-blocker, ideally before Phase 5a Play Store)

- Email re-verification UX — same-email resubmit detection
- Magic-link email PNG wordmark upgrade (~10 min — copy file + update template img tag)
- **Burner / warmup domain for marketing emails** (~30 min setup + 4-6 weeks warmup) — register `mail.quantumcube.app` or separate domain. Not needed until marketing email list grows.
- **Verify Sentry trial → free auto-downgrade (May 18, 2026)** — calendar reminder. After 14-day Business trial ends, account drops to free tier (5k errors/month). Confirm no surprise billing landed.

### 🧹 POST-LAUNCH CLEANUP

- **Dedupe `.scoreboard` / `.sb-item` / `.sb-num` duplicate CSS blocks** in app.html — currently lines ~202-207 AND ~208-213 are identical. Single-source.
- Split `docs/app.html` into .js + .css files
- `git gc --aggressive` — .git folder is 1.2 GB
- Login loop fix (same-email resign triggers new magic link)
- HeyGen cleanup (Academy side)
- Fine-comb audit pass — duplicate CSS selectors, dead code
- Brain + CPU chip icon (designer)
- `git mv` rename brand wordmark filenames to lowercase-with-hyphens
- **Refund the second Live test payment** once Dodo settlement clears
- **Rotate leaked Test API + Test webhook secrets** in Dodo dashboard
- **Delete 9+ test profile rows** from Supabase profiles table before public launch (re-snapshot first; `rkelbrickmail+e2etest@gmail.com` was added via May 4 E2E test, has_paid reset to false at end)
- **Submit Google OAuth for Verification** (currently Testing mode — only 3 test users)
- **Replace white Google G with original colour Google logo** on sign-up button (now using Light Rectangular spec — verify final visual)

### 📝 POST-LAUNCH FOLLOW-UPS (weeks-months)

- Astrology/Chinese 3-variant versions (currently single-string)
- Face 5 narrative opener variations for remaining 6 paragraphs
- Additional music tracks
- `info@quantumcube.app` via Cloudflare routing (already have `support@`)
- Marketing email pipeline + unsubscribe endpoint
- DMARC `p=none` → `p=quarantine` after 2 weeks clean
- Gmail 2FA on all 3 partner accounts
- Analytics, social proof, sharing, smoke tests
- Optional: tighten dodo-create-session to verify caller JWT matches body's `user_id`

### 🏪 APP STORE SUBMISSIONS

Phase 5a (US-only with Dodo billing, months 1-2) → Phase 5b (English markets, months 2-3) → Phase 5c (global+localised, months 4-6) → Phase 8 (Apple, months 6-9). Full roadmap detail in BRIEF_ARCHIVE.md.

---

## INFRASTRUCTURE LIVE

| System                   | State                                                                                                                       |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| GitHub Pages             | Live (source: `/docs` on `main`. SW **qc-v223**, narration **qc-narration-v3**)                                             |
| **quantumcube.app**      | **LIVE** — landing + 8 legal + /app, all HTTP 200, all CSP-protected ✓                                                      |
| qncacademy.com           | Full email stack live                                                                                                       |
| Google Workspace         | admin@qncacademy.com + 5 aliases                                                                                            |
| Cloudflare Email Routing | *@quantumcube.app → admin@qncacademy.com (incl. support@)                                                                   |
| Cloudflare DNS           | CNAME quantumcube.app → quantumneurocreations-dot.github.io ✓                                                               |
| Resend                   | Verified, SMTP in Supabase, magic-link template applied                                                                     |
| ElevenLabs               | Valory, narrate deployed + rate-limited, usage-based billing enabled (250k cap)                                             |
| Supabase                 | Frankfurt, free tier, RLS verified, 5 Edge Functions deployed (4 rate-limited, 1 webhook-signed), 3 migrations synced       |
| **Dodo Payments**        | **LIVE — accepting real payments since May 2, 2026**                                                                        |
| Sentry                   | Live, EU region, error monitoring only, CSP violations forwarded                                                            |
| FastSpring               | Account dormant (registered Apr 29, no products live)                                                                       |
| LemonSqueezy             | Application paused (SA tax form delay)                                                                                      |

---

## 💻 DEV ENVIRONMENT (M4 Mac Mini)

Hardware + OS unchanged. Native ARM64 dev tools confirmed (Node v24.15.0, Supabase CLI v2.90.0). Cursor setup unchanged (Privacy Mode ON, `.cursorignore` deleted, Browser MCP verified working).

**CLI version note:** Supabase CLI v2.95+ has `functions logs` subcommand we don't have at v2.90.0. For Edge Function logs, use the dashboard.

---

## SEPARATE PROJECT — QNC ACADEMY (context only)

Path `/Users/qnc/Projects/qnc-academy/`. Stack: Next.js + Vercel + Supabase (Ireland, ref `bevaepokvavzmykjmhda`) + Anthropic (Claude Haiku 4.5) + ElevenLabs + GitHub. QI = Academy's branded AI. HeyGen deprecated — Academy has its own cleanup task. **Never mix backends.**

---

## NEXT SESSION STARTING POINT (May 4, 2026 evening snapshot)

Massive May 4 — **15 commits** across morning + afternoon + evening + late evening. Pre-marketing-push checklist substantially complete: error monitoring live, multi-number narration shipped, magic-link payment E2E verified, security audit passed, settings gear shipped (Apr 30, brief was stale), apple-mobile-web-app-capable deprecation closed, **MCP/kickoff upgrade**, **pre-commit hook**, **post-deploy smoke test** (`fc479a0`, 4 checks, 13/13 green from Mac).

### What shipped May 4

**Morning:**
- `.supabase-envx` cleanup (Cursor caught data-loss risk in script + self-corrected)
- Brief restructured: lean v32 active brief + lossless `BRIEF_ARCHIVE.md`
- Brand cyan refresh

**Afternoon:**
- Sentry error monitoring shipped (production-only, EU region, error-only)
- Multi-number narration shipped (Hidden Passion + Karmic Lessons via playSequence)
- SW 206 cache-skip fix (Sentry's first real catch within hours of deploy)
- Magic-link payment E2E test PASSED — bounce-bug fix verified for both auth paths
- Live Mode flip cycle clean (Test → Live with pre-stage verification guards)

**Evening (this session):**
- Edge Function rate limits added to delete-account, export-data, dodo-create-session
- Edge Function error responses tightened across all 5 (no more raw error strings to client)
- CSP baseline applied to all 10 HTML pages + securitypolicyviolation → Sentry listener
- CSP fix-up for Sentry CDN connect + Vimeo thumbnail img-src
- mobile-web-app-capable meta tag (iOS deprecation fix)
- Manual: zsh history clean, Apple Passwords inventory documented, Resend backup decision logged

**Late evening (smoke + hooks + kickoff):**
- `.cursorrules` — Context7 MCP auto-fire (`5f8670f`)
- `CHAT_KICKOFF.md` — MCP readiness, brief/archive sync discipline, reusable paste blocks (`6c3cdf7`)
- Pre-commit hook enforcing SW + Sentry release sync (`00a6314`)
- Post-deploy smoke test (`23d4a20` → `4efb70a` → `90fb8b9` → `fc479a0`); lessons in `BRIEF_ARCHIVE.md` May 4 LATE EVENING

### Recommended order at start of next coding session

1. Run minimal health check (per CHAT_KICKOFF.md)
2. **Phase 5a Play Store prep** — biggest remaining lift before launch traction work. PWABuilder/Bubblewrap to generate `.aab`, store listing assets (feature graphic, phone screenshots, description), content rating questionnaire, Data Safety form, Internal Testing track setup with rkelbrick + carl + michelle as testers.
3. (In parallel) Marketing channel-by-channel attack planning — new chat with marketing playbook attached. Michelle leads social from May 4.

### Calendar reminders

- **May 18, 2026** — Sentry 14-day Business trial expires. Verify auto-downgrade to free tier (5k errors/month). No surprise billing.
- **May 4, 2027** — Annual key rotation review (ElevenLabs + Resend + Dodo + Supabase service role).

---

---

## v37-v39 CONSOLIDATED UPDATES (May 5, 2026)

### v39 — DevX foundation + PostHog + Tier 1 audit fixes (evening, May 5)

Long session, 5 commits shipped to `origin/main`:

| Commit    | What                                                                                                |
| --------- | --------------------------------------------------------------------------------------------------- |
| `b0d2d92` | **DevX foundation** — root `CLAUDE.md` (Anthropic standard pointer doc), `.claude/skills/` folder with 4 codified workflows (qc-version-bump, qc-release-procedure, qc-smoke-test, qc-incident-response), `.github/workflows/verify-versions.yml` pre-deploy CI gate. |
| `059542c` | **PostHog wired + CSP fixes** (qc-v201 → qc-v202). PostHog snippet inserted in app.html after Sentry IIFE close, before Supabase client. Production-only gate. CSP additions: vimeo.com to frame-src (fixed JAVASCRIPT-4 from Sentry), `blob:` to media-src (fixed JAVASCRIPT-5), eu.posthog.com + eu-assets.i.posthog.com to script-src + connect-src. Smoke test 13/13 post-deploy. |
| `d7ee696` | **Doc drift fix** — today's earlier docs (CLAUDE.md, skills, verify-versions.yml, smoke.sh) all said "Cloudflare Pages" but DNS reality is GitHub Pages (CNAME → quantumneurocreations-dot.github.io, no orange cloud, traffic bypasses Cloudflare proxy entirely). Fixed everywhere. DECISIONS.md line 227 confirms historical decision was always GitHub Pages — drift was self-introduced today. |
| `d70255b` | smoke.sh executable bit restored (lost in d7ee696's mode change).                                    |

### PostHog setup detail (live, capturing events)

- Project 172921, EU region, host `https://eu.i.posthog.com`, asset host `eu-assets.i.posthog.com`.
- Public client API key (safe in code, by design): `phc_sXjrkSUy6SAFddX69V53HGEegVKPUpRjpUEsERF6wcVk`.
- 11+ events captured live during setup verification — pageviews + autocapture click events from `/app`. Person ID anonymized as `019df970-22b0-...` until we wire `posthog.identify(user_id)` for paid users.
- Defaults version: `'2025-05-24'`.
- Identify-call wiring deferred to next session — want clean attribution but not blocking.

### Sentry issues resolved this session

- **JAVASCRIPT-2** (CSP block of vimeo.com) — resolved via frame-src extension in 059542c.
- **JAVASCRIPT-4** (CSP block of vimeo.com frame) — resolved same.
- **JAVASCRIPT-5** (CSP block of blob: media for narration) — resolved via media-src extension.
- **JAVASCRIPT-1** (Ronnie's manual smoke test "Sentry test") — was already resolved earlier today.

### Tier 1 security audit — actions completed

Auto-fixed in session via gh API + Cloudflare API + Supabase MCP:

- ✅ **GitHub vulnerability alerts + Dependabot automated security updates ENABLED.** Two PUT calls to `/repos/.../vulnerability-alerts` and `/repos/.../automated-security-fixes`. Now auto-PRs for vulnerable dependencies will appear.
- ✅ **DMARC ramped from `p=none` to `p=quarantine; pct=25; rua=mailto:dmarc@quantumcube.app`** via Cloudflare DNS PATCH on record `e4c164849cbe1153783624c130d44223`. Aggregate reports flow to admin@ via catch-all. Conservative ramp — next step is pct=100 then consider p=reject after 2 weeks of clean reports. **Supersedes ADR-010 — see new ADR-012.**
- ✅ **Branch protection on `main` ENFORCED via gh API.** Block force-push, block deletion, require linear history, enforce_admins=true. Solo-dev workflow preserved (no PR requirement). **See new ADR-014.**
- ✅ **Doc drift fix shipped** (commit d7ee696) — 5 files corrected. The Pages reality everywhere now reads "GitHub Pages".
- ✅ **smoke.sh executable bit restored** (commit d70255b).

Deferred / N/A items:

- ⚫ **Supabase leaked password protection** — N/A. Confirmed via app.html grep: app uses `signInWithOtp` + `signInWithOAuth` exclusively. Zero `<input type="password">` exists. Feature is also Pro-plan only. Not needed regardless of plan tier. Re-affirms ADR-005.
- ⏭ **Resend webhooks** — still none configured. Carry-forward to next session if/when bounce/complaint signals matter (will at scale).
- ⏭ **Cloudflare zone settings audit** (SSL mode, HSTS, Bot Fight Mode) — MCP token scope (DNS:Read + Email Routing:Read) doesn't expose these. Deferred to dashboard walkthrough.
- ⏭ **Dodo Payments audit** (webhook signing config, test/live mode) — Dodo MCP exposes only `sleep` tool. Browser walkthrough required.

### Supabase MCP capability expansion

Mid-session, Ronnie activated additional MCP feature groups in Supabase dashboard (URL `?showConnect=true&connectTab=mcp`). New tools confirmed available now:

- `Supabase:get_logs` (services: api, branch-action, postgres, edge-function, auth, storage, realtime — 24hr window)
- `Supabase:get_edge_function` (read deployed function source remotely)
- `Supabase:deploy_edge_function` (deploy from chat without `supabase functions deploy` CLI)
- `Supabase:list_edge_functions`
- `Supabase:merge_branch`

**Workflow implication:** previous edge function deploys required Mac surface; now end-to-end from chat. Kickoff updated to v4.1 to reflect.

### Big realization: passwordless auth confirmed (re-affirms ADR-005)

While preparing to implement client-side HaveIBeenPwned check (option B for the Pro-tier-locked Supabase leaked password feature), grepped app.html and discovered: **no `signUp()` calls anywhere, no `<input type="password">` field, only `signInWithOtp` (magic link) and `signInWithOAuth` (Google).** Quantum Cube has zero passwords. The audit was about to ship a feature with no relevance. Caught and skipped. ADR-005 already documented this; just re-affirmed.

### Calibration / lessons May 5 evening

- **Always grep for actual code patterns before implementing security features triggered by advisor warnings.** The Supabase advisor flags features that may not apply to your auth model. ADR-005 was already in DECISIONS.md but I almost shipped a 15-line HIBP check that would have done nothing.
- **Self-introduced doc drift is sneaky.** Today's CLAUDE.md and skill files were written before I confirmed Pages reality — used "Cloudflare Pages" as natural framing. Caught only when DNS audit forced a check.
- **Solo-dev branch protection means: block force-push + delete + linear history, NO PR/checks requirement.** Anything stricter blocks the solo direct-push workflow that's the core operating mode. Documented as ADR-014.
- **DMARC ramp to `pct=25` first** before pct=100 lets you observe failures at lower stakes. Reports flowing to dmarc@ via catch-all = no new mailbox needed.
- **Compaction during a long session is real** — the user explicitly flagged it on wrap-up. Always factor it into end-of-session protocol; don't trust visible chat as the full record. Read transcript if any doubt.

### v38 — Browser-tab audit (afternoon, May 5)

Final browser-tab settings audit via Claude in Chrome. Scanned 9 open tabs across Cloudflare, Resend, Supabase, UR, Clarity, Context7, GitHub, Gmail (skipped — private), Claude.ai connectors. Findings:

**System confirmed clean:**
- UR Supabase REST monitor: ALREADY PAUSED (was actioned earlier session). List view's misleading "Down 1h 48m" is just the last incident pre-pause.
- auth.users: 8 legitimate users, NO test cleanup needed (April 18 batch was thorough).
- Resend: zero bounces, all delivered, workspace `qncacademy` healthy, 2 API keys (Supabase SMTP + MCP).
- Context7: API key from earlier session still active (revoke button visible in dashboard).
- Cloudflare/Supabase billing: both Free tier, no surprise charges.

**Issues codified as ADRs (no immediate action):**
- **ADR-009 — Cloudflare orange cloud KEEP OFF.** GitHub Pages + CF proxy has documented Let's Encrypt HTTP-01 challenge interception risk. No CDN/WAF benefit at our scale yet. Revisit at scale or under attack.
- **ADR-010 — DMARC stays `p=none`.** 30-60 day observation period via Resend logs before considering bump to `p=quarantine`. Premature strengthening can quarantine legit forwards through CF email routing.
- **ADR-011 — Microsoft Clarity deferred.** Existing project `wmb8y97pls` was created as Mobile-platform (iOS/Android/Flutter/RN/Cordova/Ionic install options only — no Website install). Quantum Cube is a PWA (web). Cannot use existing project. Action: create new Clarity Website project at scale OR defer entirely until launch traffic justifies. Currently leaning DEFER.

**Cloudflare zone settings (SSL mode, security level, bot fight) NOT readable via current MCP token** (DNS:Read + Workers:Read + Email Routing:Read only). For audits at that level, dashboard is required.

**Resend webhooks: still NONE configured.** Carry-forward to next chat. Needs an endpoint (Supabase Edge Function `/resend-webhook` with verify_jwt:false → log to a table) before we can wire it up.

### v36-v37 (May 5, 2026)

Major system-hardening pass across two chat sessions. Documented inline below until they get folded into the appropriate sections of the next major brief refactor.

### Database security + performance — RESOLVED

3 Supabase migrations applied to production (project `fqqdldvnxupzxvvbyvjm`):

1. **`20260505_security_perf_hardening`** — REVOKE EXECUTE on `handle_new_user` and `narrate_rate_limit_try` from anon/authenticated. Wrapped `auth.uid()` in `(SELECT ...)` on all 3 profiles RLS policies.
2. **`20260505_security_perf_hardening_followup`** — REVOKE EXECUTE on `handle_new_user` from PUBLIC (the prior revoke didn't touch PUBLIC grant). Added explicit USING clause to UPDATE policy.
3. **`20260505_narrate_rate_counters_explicit_deny`** — Explicit deny-all RLS policy on `narrate_rate_counters` for self-documentation.

Advisor state after migrations:
- **Performance advisor:** 3 → 0 (completely clean)
- **Security advisor:** 6 → 1 — only `auth_leaked_password_protection` remains, which is **Pro-only AND moot** for our setup (magic-link + Google OAuth, no passwords). Documented as wontfix-by-design.

Final UPDATE policy on `public.profiles` (verbatim, fragile):
```sql
FOR UPDATE
  USING ((SELECT auth.uid()) = id)
  WITH CHECK (
    (SELECT auth.uid()) = id
    AND has_paid = (SELECT has_paid FROM public.profiles WHERE id = (SELECT auth.uid()))
  );
```

### Monitoring — UptimeRobot LIVE

Free tier (50 monitors / 5-min interval). Account: `quantumneurocreations@gmail.com` via Google OAuth. Email-only alert contact (no Telegram). 4 monitors:

| # | Name | Type | URL | Logic |
|---|------|------|-----|-------|
| 1 | QC — Landing | HTTP | `https://quantumcube.app` | HTTP 2xx/3xx, HEAD method, follow redirects |
| 2 | QC — App page | HTTP | `https://quantumcube.app/app` | HTTP 2xx/3xx |
| 3 | QC — Service worker | Keyword | `https://quantumcube.app/sw.js` | Alert when `qc-v` is **NOT** present in body |
| 4 | Supabase — REST | Keyword | `https://fqqdldvnxupzxvvbyvjm.supabase.co/rest/v1/` | Alert when `message` is **NOT** present in body (clever 401 workaround for free-tier-locked custom status codes) |

### Alerting — email-only path locked in (ADR-008)

Decision: skip Telegram/Slack/Discord alerting at current scale (~2 errors/month). Relying on:
- Sentry default email alerts (existing)
- UptimeRobot email contact (just configured)
- GitHub Actions built-in failure email (auto-emails repo owner)

Revisit when alert volume hits ~20/month and email triage gets noisy. Cloudflare Worker code for Sentry → Telegram drafted and parked at `/mnt/user-data/outputs/sentry-telegram-worker.js` for future use (filed in chat artifacts, not committed to repo).

### Cloudflare audit findings (MCP, May 5)

Account: `52dcfe9cdb207bed6ccc2321946b678c` (`Quantumneurocreations@gmail.com`'s Account). Two zones, both Free Website plan:
- `qncacademy.com` (zone `d8d3fbb1bfd538f3012cfa6d14a76042`)
- `quantumcube.app` (zone `837ceb26db877564cf5355e37b1cc316`)

DNS for `quantumcube.app` (11 records):
- Apex + www CNAME → `quantumneurocreations-dot.github.io` — **NOT proxied** (orange cloud OFF), so Cloudflare is DNS-only here, not in the runtime path. No CDN/WAF/bot-mgmt benefits from CF for the website itself.
- Cloudflare Email Routing MX (route1/2/3.mx.cloudflare.net) for inbound
- Resend MX (`feedback-smtp.eu-west-1.amazonses.com`) on `send.quantumcube.app` for outbound
- DKIM keys for both Cloudflare and Resend in TXT records
- SPF on root and on `send` subdomain
- DMARC was `p=none`, **bumped May 5 evening to `p=quarantine; pct=25; rua=mailto:dmarc@quantumcube.app`** (partial enforcement + aggregate reports flowing to admin@ via catch-all). Ramp to pct=100 / consider p=reject after 2-week monitoring window. **See ADR-012 (supersedes ADR-010).**

Email Routing rules (both enabled):
- `support@quantumcube.app` → forward to `admin@qncacademy.com`
- catch-all → forward to `admin@qncacademy.com`

Destinations: `admin@qncacademy.com` (verified)

Workers in account: 1 — `holy-leaf-e567` (modified Apr 6, predates QC launch). **Action: review and likely delete** if unused.

MCP token scope limited to DNS:Read + Workers:Read + Email Routing:Read. Zone Settings (security level, bot fight mode, SSL/TLS config) are NOT readable via current token — use dashboard for those audits.

### Resend audit findings (MCP, May 5)

Domain `quantumcube.app`:
- Status: `verified`
- Region: `eu-west-1` (EU residency, aligns with Supabase EU + Sentry EU)
- Sending: enabled. Receiving: disabled (Cloudflare Email Routing handles inbound)
- DKIM, SPF MX, SPF TXT all `verified`
- Open tracking: OFF. Click tracking: OFF (good — magic-links shouldn't be wrapped)

API keys (2):
- `quantum-cube-supabase-smtp` (created Apr 18, last used May 4) — used by Supabase for magic-link delivery
- `MCP Bundles - Claude` (created May 5, last used May 5) — for chat-based admin operations

**Webhooks: NONE configured.** This is a real gap — we have no signal on bounces, complaints, or delivery failures. Recommended addition (post-launch): wire a webhook that catches `email.bounced` and `email.complained` events, posts to Sentry as a warning. Defer to next chat unless we see complaints.

### New repo files (uncommitted, ready for review)

Written this session via Filesystem MCP, NOT yet committed:
- `DECISIONS.md` (root) — 8 ADRs seeded (Dodo, GH Pages, single-HTML, has_paid guard, magic-link auth, Sentry tier, three-doc system, email-only alerting)
- `.github/workflows/daily-health-check.yml` — daily cron at 06:00 UTC, email-only alerting via GitHub's built-in failure notification

User action required:
1. Review file contents
2. `git add . && git commit -m "chore: brief v37 + DECISIONS + GH Actions health check"`
3. `git push`
4. First manual run of the GitHub Action via Actions tab to confirm green

### Site instrumentation gap

**Microsoft Clarity is NOT wired into `docs/app.html`.** May 5 PM audit revealed why: existing Clarity project `wmb8y97pls` was created as Mobile-platform-only (iOS/Android/Flutter/RN/Cordova/Ionic install paths only). Quantum Cube is a PWA, needs Website-type Clarity project. **Codified as ADR-011 — DEFERRED.** Re-evaluate when launch traffic justifies (currently ~9 users; Clarity is overkill at this scale).

### Pending action items (carry forward)

**User-side (you click):**
1. ✅ ~~**Branch protection**~~ — **DONE May 5 evening**. See ADR-014.
2. **Old test user delete approval** — auth user `a72a753e-90a3-48d7-a75b-422b8b9512bf` (April 18, never confirmed, 18 days stale). Pending yes/no.
3. **Anthropic API key** — defer until we ship Claude-in-loop scheduled tasks (we currently don't).
4. **Apple Passwords inventory + Google 2FA + domain registrar audits** — eyeball checks for Stage 6.
5. **Vercel shadow deployment decision** — `prj_WKo5JwtJ02CGBVsyqbDAORQbQpDy` still auto-deploying every commit. Decide whether to keep as Academy/backup or delete.
6. **Context7 free API key** — sign up at context7.com (free tier gives higher limits than the unauthenticated quota we hit twice).
7. **Submit `sitemap.xml` to Google Search Console** — once you've added the property at `quantumcube.app`, Submit → `https://quantumcube.app/sitemap.xml`. ~5 min.

**Next-chat to-do (Android/Play Store sprint — NEXT MAJOR PHASE):**

🎯 **Primary objective: Google Play Store submission as TWA (Trusted Web Activity)**
- Generate Android keystore (Bubblewrap recommended, or PWABuilder web UI)
- Replace placeholders in `/.well-known/assetlinks.json`:
  - `package_name: "app.quantumcube.twa"` → real value
  - `sha256_cert_fingerprints: ["REPLACE_WITH..."]` → keystore SHA-256
- Generate `.aab` (Android App Bundle) via Bubblewrap
- Google Play Console: create app entry, upload bundle, fill in store listing, declare data-safety form (uses Supabase auth, Dodo Payments, etc.), pricing ($17 one-time IAP or external billing — research Google's policy on external billing for one-time digital goods)
- Submit for review (typical 3-7 day turnaround)

🎯 **Pre-Android user-requested item: narration change**
- User mentioned "one more thing I would like to do regarding narration" at end of May 6 session. Specifics to be defined in next chat. Probable scope: voice/script/timing tweak.

🎯 **Other carry-forward (lower priority):**
- Wire Microsoft Clarity into `docs/app.html` (still requires Website-type project per ADR-011)
- Configure Resend webhook for bounce/complaint → Sentry
- Cookie consent solution (deferred to pre-EU push)
- TWA submission may surface fresh items not anticipated (Google Play data-safety form requires reviewing PostHog/Sentry/Supabase data flows)

### Tooling status (all loaded as of May 5 afternoon)

Finally surfaced after user re-authorization in claude.ai:
- Cloudflare (execute + search) — full API access via JS code
- Resend (32 tools — full CRUD)
- Filesystem — full access to user's Mac (`/`)
- Desktop Commander — full bash, processes
- Apple Notes, iMessages, Control your Mac, Claude in Chrome, Control Chrome
- ElevenLabs Agents, pdf-viewer, Google Drive, Sentry, Supabase, Vercel, Context7, Dodo Payments — already worked

Still missing in claude.ai surface: GitHub Integration (use `gh` CLI via Desktop Commander as workaround when needed).

---

**End of brief v41.** Archived history → `BRIEF_ARCHIVE.md`. Marketing strategy → `MARKETING_PLAYBOOK.md`. Session protocol → `CHAT_KICKOFF.md`. Decision log → `DECISIONS.md`.
