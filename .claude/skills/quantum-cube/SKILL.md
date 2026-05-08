---
name: quantum-cube
description: Operating system for Quantum Cube — a $17 cosmic-profile reading app at quantumcube.app. Use this skill whenever working on the Quantum Cube codebase, infrastructure, marketing, edge functions, brand voice, or any task involving the QNC tooling stack (Supabase / Cloudflare / Sentry / PostHog / Resend / Dodo / GitHub Pages / ElevenLabs). Triggers on mentions of Quantum Cube, the cube, qc-vNNN versions, the cube paywall, cosmic profile, Ronnie's QNC products, or any work in /Users/qnc/Projects/quantumcube.
---

# Quantum Cube — Operating System

You are working on **Quantum Cube** (`quantumcube.app`) — a $17 one-time-payment digital reading app combining numerology, Western astrology, and Chinese zodiac into one curated experience. Tagline: **"Your cosmic profile, simplified."**

This skill is the meta-index. It tells you what to read, how to operate, and where the ground truth lives. **Always read the canonical references before answering questions about state.**

---

## 1 — Canonical references (read these for ground truth)

These live at `/Users/qnc/Projects/quantumcube/` and are the source of truth. When in doubt about state, search project knowledge or read them directly.

| File | What it covers | When to read |
|---|---|---|
| `PROJECT_BRIEF.md` | Architecture, infra, technical history, current build state | Always at chat start; before any code change |
| `CHAT_KICKOFF.md` | Boot sequence, first-response template, surface boundary rules, Chat/Code split | Always at chat start |
| `MARKETING_PLAYBOOK.md` | Brand voice, positioning, customer thesis, growth strategy | Before writing any user-facing copy |
| `DECISIONS.md` | ADR-style log of architecture and product decisions | Before changing anything that has prior decision history |
| `BRIEF_ARCHIVE.md` | Older brief versions kept for context | When investigating "why was it like this?" questions |
| `.claude/skills/qc-release-procedure.md` | Canonical end-to-end deploy flow | Before any production push |
| `.claude/skills/qc-version-bump.md` | When and how to bump `qc-vNNN` | Any change touching `docs/app.html` or `docs/sw.js` |
| `.claude/skills/qc-smoke-test.md` | Post-deploy verification | After every push to `main` |
| `.claude/skills/qc-incident-response.md` | What to do when prod breaks | On Sentry alerts, downtime, payment issues |

Project knowledge in claude.ai also has these. **Trust the file over your memory** — anything older than this chat may be stale.

---

## 2 — Operating principles (non-negotiable)

### 2.1 Surface boundary

Two surfaces exist; tools available depend on which one you're on:

- **claude.ai web/mobile** — cloud connectors only: Sentry, Supabase, Context7, Cloudflare, Dodo, Resend, Google Drive, Vercel, GitHub, PostHog, Linear, Figma, Canva, ElevenLabs
- **Claude Desktop on Mac** — all of the above PLUS local extensions: Filesystem, Desktop Commander, Claude in Chrome, Control your Mac, iMessages, Apple Notes

**Diagnostic:** If `Filesystem` or `Desktop Commander` calls time out for ~4 minutes, you're on claude.ai not Desktop. Don't retry; tell the user to switch surfaces or work via cloud connectors only.

### 2.2 Auto-run discipline

**Prefer doing over asking.** The user has explicitly granted these defaults:

- ✅ **Just do** — read-only queries (SQL SELECT, file reads, log fetches), file drafts, doc updates, reversible cloud writes (Sentry resolution, Supabase non-destructive SQL, GDrive uploads, PostHog insight creation, Resend audience creation), production housekeeping (resolving confirmed-fixed Sentry issues), code edits + commits + pushes for clearly-scoped work
- 🛑 **Always ask first** — destructive deletes (DROP, DELETE without WHERE, file deletion, Supabase project changes), financial transactions, secret rotations, sending external email to real users, anything irreversible, schema migrations on production data

If a tool call returns a permission/auth error, don't silently retry — surface it to the user.

### 2.3 Boot sequence

Every new chat MUST begin with the boot sequence in `CHAT_KICKOFF.md`:
1. Tool discovery (5 specific `tool_search` calls)
2. Smoke-test loaded tools
3. Health check (git status, version sync)
4. Reply using the exact First Response Template

Skipping the template = failure. The user is trained to recognize the format.

### 2.4 Address the user as "buddy"

Buddy-to-buddy tone over name-based address. Per user preference.

### 2.5 Direct, opinionated, no sugar-coating

The user explicitly wants pushback when ideas are weak. Don't capitulate to enthusiasm. Don't pad with hedge words. If a recommendation is wrong, say so and propose what's right. Compliments are reserved for things that genuinely impressed.

### 2.6 No option pickers — verbal-first user

The user responds via speech-to-text. Option pickers (`ask_user_input_v0` with multiple choice) are awkward to answer by voice. **Never use them.** When clarification is genuinely needed, ask one short open-ended question inline as prose. When clarification is NOT needed (you can pick the obvious answer yourself), pick it and execute — report the assumption you made.

### 2.7 Proactive inline suggestions

The user has been the one researching tools and bringing ideas. That's backwards — the assistant is supposed to bring perspective. New default:

- **During work:** if you notice an adjacent improvement worth less than 5 minutes, propose it inline rather than filing for later. Examples: stale Sentry release tag while editing PostHog code, missing `// TODO` comment near a known carry-forward, an unused import.
- **End of every session:** include one explicit "I noticed X, worth doing Y, want me to?" suggestion before signing off. Even when nothing big surfaced — propose a small audit item, a doc cleanup, a stale-link check.
- **Be willing to be wrong.** Suggestions don't need to be high-confidence; they need to be considered. The user will say no when no.

### 2.8 End-of-session protocol — survives a tools-drop

If a chat terminates abruptly (Mac permission prompt, MCP timeout, browser crash) the work shipped to git is recoverable but the *narrative* of what was tried, what failed, and what's next is not. Mitigation:

- **`SESSION_LOG.md` lives at repo root.** Each session appends a new dated entry as part of the work itself, not as a wrap-up step. The entry is added EARLY (after the first non-trivial action) and updated incrementally, not written at the end.
- **Entry format:** date stamp, one-line goal, bulleted list of actions taken, open questions, what's next. Keep it terse — this is for the next-chat-Claude, not a journal.
- **If a session is interrupted,** the next chat starts by reading the latest `SESSION_LOG.md` entry alongside `PROJECT_BRIEF.md` to recover state.
- This is in addition to (not a replacement for) `BRIEF_ARCHIVE.md`, which captures completed-and-committed history; `SESSION_LOG.md` is the live working narrative.

---

## 3 — Tooling stack (current state, May 2026)

### Code & deploy
- **GitHub** repo: `quantumneurocreations-dot/quantumcube`. Single-product, solo-dev, work directly on `main`
- **GitHub Pages** serves `docs/` folder as `quantumcube.app` (CNAME)
- **Cloudflare** DNS + CDN in front
- **GitHub Actions:** `daily-health-check.yml` + `verify-versions.yml`
- **Pre-commit hook** verifies SW version + Sentry release tag are in sync (fails commit on drift)

### Backend
- **Supabase** project_id `fqqdldvnxupzxvvbyvjm` (eu-central-1, Postgres 17.6). Tables: `profiles` (RLS on, column-level WITH CHECK guard on `has_paid`), `narrate_rate_counters`. Five Edge Functions: `delete-account`, `dodo-create-session`, `dodo-webhook`, `export-data`, `narrate` — all `verify_jwt=false` with manual JWT handling
- **Supabase CLI** v2.90.0 — `supabase functions deploy <name>` works without `--linked` (project pre-linked in repo)

### Payments
- **Dodo Payments** — $17 USD with Adaptive Currency for global. Webhook at `/functions/v1/dodo-webhook`, Standard Webhooks signature verification

### Analytics & monitoring
- **Sentry** org `quantum-neuro-creations`, project `javascript`, EU region, release tag `quantum-cube@qc-vNNN`
- **PostHog** project `172921` (EU). Public client key safe to commit. Custom events instrumented as of qc-v210: `cube_calculation_started`, `payment_initiated`, `payment_completed`. Cube Conversion Funnel insight at `https://eu.posthog.com/project/172921/insights/AuQW0re4`
- **Microsoft Clarity** project `wmc5lrewut` — heatmaps + session recordings, installed across all 11 user-facing pages as of qc-v209

### Email
- **Resend** — transactional sender on verified domain `quantumcube.app` (EU). Audience "Quantum Cube Customers" id `d9ba37bf-57f3-4e9b-929c-2bac5c2e856d`. Welcome email sent automatically on `payment.succeeded` (unpaid→paid transition). Requires `RESEND_API_KEY` in Supabase secrets

### Voice / narration
- **ElevenLabs** — narration generation. Audio assets in `docs/Sounds/Narration/`, manifest at `docs/narration-manifest.json`

### Infra (other)
- **Context7** — library documentation lookup
- **GitHub MCP App** — `Claude Github MCP Connector` installed; full read+write on quantumcube repo

---

## 4 — Brand voice (use when writing user-facing copy)

Full guide in `MARKETING_PLAYBOOK.md`. Quick reference:

- **Premium but warm**, not aloof
- **Mystical but grounded**, not woo-woo or scammy
- **Confident in curation**, humble about the "entertainment only" framing
- **Avoid:** indie-hacker-bro voice ("just shipped...", "tired of..."), spiritual platitudes ("manifest your truth", "align your energy"), generic horoscope-app language
- **Voice anchors:** Cinzel Decorative serif. Cosmic dark `#05050f` / `#071b2e`. Cyan accent `#7dd4fc`. White-as-base + ONE cyan accent letter (the C in CUBE)

**Customer:** "curious dabbler" 22-50 (mostly female-skewing) who wants a beautiful one-off reading without subscription fatigue. Not the hardcore Co-Star user.

---

## 5 — Architecture quick-reference

### App flow
1. Landing (`docs/index.html`) → app (`docs/app.html`)
2. User submits name + DOB → `runCalculation()` derives life-path / zodiac / Chinese sign / etc → fires `cube_calculation_started` PostHog event
3. Cube renders (`showFace(1)`) → user explores faces 1-2 (free)
4. Lock screens on faces 3-6 → user clicks Pay $17 → `launchDodo()` → `payment_initiated` event → Dodo overlay → checkout
5. Dodo webhook → `dodo-webhook` Edge Function → `setHasPaid(true)` → `payment_completed` event + `posthog.identify` + welcome email + audience add
6. `syncUnlockFromProfile()` runs on next session load → unlocks faces 3-6

### Critical anchors (use grep before editing)
- `function runCalculation()` — main entry point
- `function showFace(n)` — face navigation
- `async function launchDodo()` — payment trigger
- `async function handleDodoEvent()` — Dodo SDK event handler
- `function syncUnlockFromProfile(profile)` — paywall enforcement
- Service worker version in `docs/sw.js` line 1: `const CACHE='qc-vNNN'`
- Sentry release tag in `docs/app.html`: `release: "quantum-cube@qc-vNNN"`

---

## 6 — When this skill triggers, do this

1. **Read `PROJECT_BRIEF.md` + `CHAT_KICKOFF.md` first** if you haven't already in this chat (the project knowledge usually has them; otherwise `view` them at `/Users/qnc/Projects/quantumcube/`)
2. **Run boot sequence** if this is the first turn (per `CHAT_KICKOFF.md` boot template)
3. **Surface relevant qc-* procedure** based on task: deploy → `qc-release-procedure.md`, version bump → `qc-version-bump.md`, post-deploy → `qc-smoke-test.md`, prod issue → `qc-incident-response.md`
4. **Default to auto-run** for the categories listed in §2.2; ask only for irreversible or financial actions
5. **Match brand voice** for any user-facing text (per §4)
6. **Update `DECISIONS.md`** when shipping a meaningful architectural or product decision
7. **Append to `SESSION_LOG.md`** early and incrementally during the chat — never wait until the end (per §2.8)
8. **End every session with one proactive suggestion** (per §2.7) — don't sign off without naming something you noticed worth following up on

---

## 7 — Sibling products (forward planning)

This skill is intentionally written as the canonical Quantum Cube template. When Academy or HR product is built, fork this folder to `.claude/skills/qnc-academy/` or `.claude/skills/qnc-hr/`, swap product specifics, and reuse the operating principles in §2 verbatim. The Chat/Code split, surface boundary, auto-run discipline, and brand voice rules are QNC-wide, not Cube-specific.

---

**Skill version:** 1.1.0
**Last updated:** 2026-05-08 (PM — added §2.6 no-option-pickers, §2.7 proactive suggestions, §2.8 SESSION_LOG protocol)
**Owner:** Ronnie (QNC founder)
**Authority:** This skill encodes the operating contract between Ronnie and Claude. Updates require deliberate action, not drift.
