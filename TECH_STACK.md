---
tags: [core, reference, stack]
---
# QNC — FULL TECH STACK & OPERATING SYSTEMS

Living document. Update whenever a new tool, service, or surface is added.
Companion to CONNECTORS.md (which holds service IDs, API key paths, golden rules).

---

## HARDWARE

| Item | Detail |
|------|--------|
| **Primary machine** | Mac Mini M4 |
| **Internet** | Axxess WiFi Router — Uncapped, ~120 Mbps avg ([speedtest.net](https://www.speedtest.net/)) |

---

## CLAUDE SURFACES & MODELS

QNC runs three distinct Claude surfaces. Each has a different model, quota, and job.

| Surface | Where | Model | Primary job |
|---------|-------|-------|------------|
| **Claude Desktop / claude.ai** | This chat | Sonnet 4.6 | Buddy ↔ Claude main conversation. Speech-to-text via mic. Planning, MCP queries, decisions, session management. |
| **Claude Code** | Terminal (Mac Mini) | Opus 4 | Heavy file edits, git, bash, deployments. Separate quota from Desktop. |
| **QI Voice** | Local Python (`qi-voice.py`) | Haiku 4.5 | Fast voice responses inside QI. Low latency, low cost. |

**Plan:** Claude Max — covers both Desktop + Code on the same subscription.
**Note:** Voice/STT is Ronnie's primary input for Claude Desktop. Spelling errors are expected. Always keep that in mind.

---

## SECOND BRAIN — OBSIDIAN

| Item | Detail |
|------|--------|
| **App** | Obsidian (must be running for mcp-obsidian to work) |
| **Vault path** | `/Users/qnc/Projects/quantum-integrator` |
| **Auto-sync** | Obsidian Git plugin — commits + pushes every 10 min, no manual git needed for doc edits |
| **MCP** | mcp-obsidian (local stdio, 5 tools) |
| **Role** | Source of truth for all live docs. Claude reads from vault on every boot. |

**Core vault docs:**

| File | Purpose |
|------|---------|
| `SESSION_LOG.md` | Live session narrative (top entry only per boot) |
| `PROJECT_BRIEF.md` | QI + QC system state |
| `CONNECTORS.md` | All service IDs, API key locations, golden rules |
| `DECISIONS.md` | ADR log (append-only) |
| `OPERATING_RULES.md` | Golden rules, patterns, failure recovery |
| `NORTH_STAR.md` | 500 customers by Aug 15, 2026 goal |
| `TECH_STACK.md` | **This file** — full tool inventory |
| `CHAT_KICKOFF.md` | Boot protocol for every new Claude chat |

---

## MCPs & CONNECTORS

### Claude Desktop (claude.ai) — Connected MCP Servers

These are the live connectors shown in the Claude Console sidebar:

| Connector | MCP URL | Tools |
|-----------|---------|-------|
| **GitHub** | api.githubcopilot.com/mcp | 41 tools — commits, PRs, issues, code search |
| **ElevenLabs** | (Agents MCP App) | Agent creator, voice search, config |
| **Vercel** | mcp.vercel.com | 18 tools — deployments, logs, previews |
| **Supabase** | mcp.supabase.com/mcp | 29 tools — SQL, migrations, edge functions |
| **Vimeo** | — | Video hosting for Quantum Cube app embeds |
| **Dodo Payments** | mcp.mcpbundles.com/bundle/dodo-payments-mcp | Payments, orders, customers |
| **Canva** | mcp.canva.com/mcp | 32 tools — design generation, brand kits |
| **Quantum Cube / PostHog** | mcp.posthog.com/mcp | Analytics, funnels, insights, cohorts |
| **Cloudflare** | mcp.cloudflare.com/mcp | DNS, Workers, KV, R2 |
| **Cloudflare Dev Platform** | bindings.mcp.cloudflare.com/mcp | D1, KV, R2, Workers code |
| **Gmail** | gmailmcp.googleapis.com/mcp/v1 | 12 tools — threads, labels, drafts |
| **Google Drive** | drivemcp.googleapis.com/mcp/v1 | 8 tools — file search, read, upload |
| **Sentry** | mcp.sentry.dev/mcp | 22 tools — issues, events, replays |
| **Resend** | mcp.mcpbundles.com/bundle/resend | 31 tools — email send, audiences, templates |
| **Context7** | mcp.context7.com/mcp | Live library docs |
| **Linear** | mcp.linear.app/mcp | 35 tools — issues, projects (available, not active) |
| **Figma** | mcp.figma.com/mcp | Design context, assets (available, not active) |
| **Play Console** | — | Google Play Developer Console |
| **Desktop Commander** | Local stdio | Bash, file ops, process control on Mac Mini |
| **mcp-obsidian** | Local stdio | Vault read/write (requires Obsidian running) |

### Claude Code — Local stdio MCPs (Terminal)
| MCP | Install | Role |
|-----|---------|------|
| **ElevenLabs** | `uvx` | Re-generate narration MP3s from terminal |
| **Context7** | `npx` | Live docs for exact library versions in use |
| **Tavily** | `npx` | Web search from terminal (Claude Code has no default internet) |

---

## QNC PRODUCTS

| Product | URL | Status |
|---------|-----|--------|
| **Quantum Cube** | quantumcube.app | Live — 4 paying customers, SW qc-v305 |
| **Quantum Integrator (QI)** | localhost:3001 | Active development — AI OS for QNC |

---

## DATA & AUTH

| Service | Detail |
|---------|--------|
| **Supabase** | QNC org: ybhwpcakkaveapdztnrs |
| QC project | `fqqdldvnxupzxvvbyvjm` (eu-west-1) — Quantum Cube app database |
| QI project | `zhvcmxtgvrogxnvqauus` (eu-west-1) — QI system database ($10/mo) |
| Auth method | Magic-link (Resend SMTP) + Google OAuth. No passwords. |

---

## PAYMENTS

| Service | Detail |
|---------|--------|
| **Dodo Payments** | EU MoR — handles global tax, fraud, chargebacks. $17 one-time price. |
| **Google Play** | Personal account, "Quantum Neuro Creations". 15% reduced fee confirmed. 14-day closed testing gate. |

---

## INFRASTRUCTURE & CDN

| Service | Detail |
|---------|--------|
| **Cloudflare** | Account 52dcfe9cdb207bed6ccc2321946b678c · Zone 837ceb26db877564cf5355e37b1cc316 |
| DNS | quantumcube.app apex + www → GitHub Pages (DNS-only, orange cloud OFF per ADR-009) |
| Email routing | `*@quantumcube.app` → admin@qncacademy.com (catch-all) |
| **GitHub Pages** | Serves `quantumcube.app` from `/docs` on `main` branch. Auto-deploys on every push (~60s). |
| **Vercel** | prj_WKo5JwtJ02CGBVsyqbDAORQbQpDy (parked — potential Academy site) |

---

## MONITORING & ANALYTICS

| Service | Detail |
|---------|--------|
| **PostHog** | Project 172921, EU (`eu.i.posthog.com`). Autocapture + product funnel events. |
| **Sentry** | Org `quantum-neuro-creations`, EU. Error monitoring only (5k/mo free tier). |
| **UptimeRobot** | Status page: stats.uptimerobot.com/azO4bPUJJQ. Narrate + site monitors. |
| **Microsoft Clarity** | Project `wmc5lrewut`. Heatmaps + session recordings on 11 pages. |

---

## EMAIL & COMMUNICATIONS

| Service | Detail |
|---------|--------|
| **Resend** | Domain `send.quantumcube.app`, eu-west-1. Transactional email (welcome, magic links). |
| **Gmail** | QI alias: qi@qncacademy.com (routes via admin@qncacademy.com) |
| **Google Workspace** | Domain: qncacademy.com. Admin: admin@qncacademy.com. |

---

## VOICE & AUDIO

| Service | Detail |
|---------|--------|
| **ElevenLabs** | QI voice ID: `giAoKpl5weRTCJK7uB9b`, model `eleven_turbo_v2_5` — stability 0.5, similarity 0.75, speed 1.0 |
| Narration (Valory) | Voice ID: `VhxAIIZM8IRmnl5fyeyk` — same model, speed 1.15 (welcome.mp3 = 1.0) |
| **Deepgram** | STT for QI wake word + voice recognition. Key at `~/.config/qi/` |
| **Epidemic Sound** | Creator plan — background music + sound effects for QNC content |

---

## CONTENT, MEDIA & AI TOOLS

| Service | Detail |
|---------|--------|
| **Vimeo** | Video hosting — embeds inside Quantum Cube app |
| **Canva** | Design assets, brand kit, social media |
| **Fal.ai** | Image generation pipeline for QI marketing. Key at `~/.config/qi/` |
| **Firecrawl** | Web scraping for QI research. Script: `scripts/qi_firecrawl.py` |
| **Tavily** | Web search API for QI agents. Key at `~/.config/qi/` |

---

## API KEYS VAULT

All sensitive credentials stored at `~/.config/qi/` (chmod 600). Never in git.

| Key file | Service |
|----------|---------|
| `anthropic_api_key` | Claude API (direct calls from QI scripts) |
| `elevenlabs_api_key` | ElevenLabs TTS |
| `deepgram_api_key` | Deepgram STT |
| `tavily_api_key` | Tavily web search |
| `firecrawl_api_key` | Firecrawl scraping |
| `fal_api_key` | Fal.ai image gen |
| `calendar_token.pickle` | Google Calendar OAuth token |
| `supabase_qi_db_url` | QI Supabase direct DB connection |

---

## ANTHROPIC BILLING — JUNE 15, 2026 NOTE

All QI Anthropic calls use **direct `api.anthropic.com` + API key** — metered against API balance, not subscription credit pool. QI is unaffected by Anthropic's June 15 programmatic billing change. See ADR-029 + OPERATING_RULES.md Golden Rule #6.

Claim monthly Agent SDK credit on June 8 when Anthropic emails — free $20–$200 for interactive use.

---

> **Related:** [[CONNECTORS]] · [[OPERATING_RULES]] · [[PROJECT_BRIEF]] · [[DECISIONS]]
> **Last updated:** 2026-05-16

---

## SKILLS & SUPERPOWERS

Claude's capabilities are extended via skills — loaded automatically by trigger or called explicitly. Three tiers across two surfaces.

---

### TIER 1 — CLAUDE DESKTOP (claude.ai) PROJECT SKILLS
Available in this chat right now. Auto-triggered by context or read on demand.

**Document creation:**
| Skill | What it does |
|-------|-------------|
| `docx` | Create/edit/read Word documents |
| `pdf` | Create, merge, split, fill, watermark PDFs |
| `pptx` | Create/read/edit PowerPoint presentations |
| `xlsx` | Create/edit Excel spreadsheets |

**Design & UI:**
| Skill | What it does |
|-------|-------------|
| `frontend-design` | Production-grade web components, pages, artifacts |
| `canvas-design` | Visual art, posters, static designs → PNG/PDF |
| `theme-factory` | 10 preset themes for artifacts |
| `web-artifacts-builder` | Complex multi-component HTML artifacts (React, Tailwind, shadcn) |
| `brand-guidelines` | Brand colors + typography applied to artifacts |

**File handling:**
| Skill | What it does |
|-------|-------------|
| `file-reading` | Route any uploaded file to correct reading strategy |
| `pdf-reading` | Extract text, tables, images from PDFs |

**Writing & docs:**
| Skill | What it does |
|-------|-------------|
| `doc-coauthoring` | Structured co-author workflow for documentation |
| `internal-comms` | Status reports, leadership updates, newsletters, FAQs |

**Build tools:**
| Skill | What it does |
|-------|-------------|
| `mcp-builder` | Guide for building MCP servers |
| `skill-creator` | Create, modify, eval, and benchmark skills |
| `product-self-knowledge` | Look up current Anthropic product facts |

---

### TIER 2 — QI + QC CUSTOM SKILLS
Project-specific skills baked into the QNC operating system.

**QI vault skills** (`quantum-integrator/.claude/skills/`):

| Skill | What it does |
|-------|-------------|
| `chief-of-staff` | Morning briefing mode — 3 spoken priorities from strategic goals + live data. "That is your focus. Go." |
| `head-of-design` | Design sub-agent — plain English brief → dark sci-fi HTML mockup in QC brand, auto-opens in browser |
| `qmd` | Semantic vault search — search before reading files, proactively triggered for past decisions + architecture |

**QC project skills** (`quantumcube/.claude/skills/`):

| Skill | What it does |
|-------|-------------|
| `quantum-cube` | Full operating system for QC codebase — stack, brand, architecture, deploy rules |
| `qc-release-procedure` | Canonical end-to-end deploy flow for any production change |
| `qc-version-bump` | Version bump before any `app.html`/`sw.js` change |
| `qc-smoke-test` | Post-deploy 13-point verification check |
| `qc-incident-response` | Sentry alert triage → fix → verify flow |

---

### TIER 3 — GLOBAL CLAUDE CODE SKILLS (`~/.claude/skills/`)
Available as `/skill-name` slash commands in the Claude Code terminal. 48 skills total.

**Browser automation (flagship suite):**
| Skill | What it does |
|-------|-------------|
| `gstack` | Full headless browser framework — QA, screenshots, forms, responsive, bug evidence. Multi-agent compatible: Cursor, OpenClaw, Slate, Factory, Kiro, Hermes (101-file suite) |
| `browse` | Fast headless browser — navigate, interact, verify, diff |
| `benchmark` | Performance regression detection |
| `scrape` | Pull structured data from web pages; first call prototypes, reruns reuse |
| `skillify` | Codify scrape flows into permanent reusable skills |
| `pair-agent` | Pair a remote AI agent (OpenClaw compatible) with your browser |

**Dev workflow:**
| Skill | What it does |
|-------|-------------|
| `ship` | Full ship: merge base branch → tests → diff review → version bump → deploy |
| `land-and-deploy` | Merge PR, wait for CI + deploy, verify |
| `qa` / `qa-only` | QA test a web app + fix bugs found |
| `retro` | Weekly engineering retro — analyzes commit history + work patterns |
| `health` | Code quality dashboard — linter, type checker, project tools |
| `investigate` | Systematic debugging — 4 phases: investigate, hypothesize, test, resolve |
| `review` | Code review |
| `codex` | OpenAI Codex CLI wrapper (3 modes: code review, independent diff, direct) |

**Context management:**
| Skill | What it does |
|-------|-------------|
| `context-save` / `context-restore` | Save + restore working context (git state, decisions, remaining work) across sessions |
| `freeze` / `unfreeze` | Lock file edits to a specific directory for a session |
| `guard` | Full safety mode: destructive command warnings + directory-scoped edits |
| `careful` | Warns before `rm -rf`, `DROP TABLE`, force-push, destructive commands |

**Design & planning:**
| Skill | What it does |
|-------|-------------|
| `design-html` | Design finalization → production-quality HTML/CSS |
| `design-review` / `design-consultation` / `design-shotgun` | Design workflow modes |
| `autoplan` | Runs CEO / design / eng / DX reviews sequentially |
| `plan-ceo-review` / `plan-design-review` / `plan-devex-review` / `plan-eng-review` / `plan-tune` | Individual planning review modes |

**Strategy & operations:**
| Skill | What it does |
|-------|-------------|
| `office-hours` | YC Office Hours — 6 forcing questions that expose startup weaknesses |
| `cso` | Chief Security Officer mode — infrastructure-first security audit |
| `graphify` | Convert any input (code, docs, images) to a knowledge graph |
| `make-pdf` | Markdown → publication-quality PDF |
| `learn` | Manage project learnings from gstack |
| `benchmark-models` | Compare AI model outputs on tasks |
| `canary` | Canary deploy / feature flag pattern |

**Setup & utilities:**
| Skill | What it does |
|-------|-------------|
| `setup-deploy` / `setup-gbrain` / `setup-browser-cookies` | Environment setup helpers |
| `sync-gbrain` / `connect-chrome` / `open-gstack-browser` | Sync + browser helpers |
| `document-release` / `landing-report` | Release notes + landing page reporting |

---

> **"Super powers"** = this full skills suite. Chief-of-staff, gstack, cso, office-hours, investigate are the heavy hitters.
> Skills are loaded on-trigger — they cost no tokens unless actively used.
> Add new skills: `skill-creator` in Claude Desktop, or `/skillify` in Claude Code terminal.

---

## QI AGENTS

QI sub-agents are Python scripts in `scripts/qi-*.py`. Each has a matching SKILL.md in `.claude/skills/<name>/` per Golden Rule #7.

| Agent | Script | Skill | Status |
|-------|--------|-------|--------|
| Chief of Staff | `scripts/morning-briefing.py` | `.claude/skills/chief-of-staff/` | ✅ Live |
| Head of Design | `scripts/head_of_design.py` | `.claude/skills/head-of-design/` | ✅ Live |
| Voice | `scripts/qi-voice.py` | — (core loop, not a sub-agent) | ✅ Live |
| Calendar | `scripts/qi-calendar.py` | — | ✅ Live |
| Memory | `scripts/qi_memory.py` | — | ✅ Live |
| Firecrawl | `scripts/qi_firecrawl.py` | — | ✅ Live |
| Marketing Agent | `scripts/qi-marketing.py` | `.claude/skills/qi-marketing/` (create at build time) | 🔴 Pending |
| Revenue Agent | `scripts/qi-revenue.py` | `.claude/skills/qi-revenue/` (create at build time) | 🔴 Pending |

> Each new agent added here + matching SKILL.md written same session. See Golden Rule #7.

---

## QI STACK INTELLIGENCE AGENT — SPEC

> **Status:** 🔴 Pending build — spec complete, ready for next dedicated session.
> **Script target:** `scripts/qi-stack-intel.py`
> **Skill target:** `.claude/skills/qi-stack-intel/SKILL.md`
> **Cron slot:** 6am daily (runs BEFORE 7am morning briefing so QI can speak a summary)

### What it does
Automated tech radar. Runs daily, scans the web for new tools/upgrades/connectors, compares against QNC's current stack, surfaces only genuine signal. QI speaks a brief at 7am. Full report saved to vault.

### Architecture

```
6am cron → qi-stack-intel.py
    │
    ├── Layer 1: Firecrawl (scripts/qi_firecrawl.py)
    │   Scrape specific monitored pages:
    │   - Anthropic blog / changelog
    │   - ElevenLabs releases
    │   - Supabase changelog
    │   - Cloudflare blog
    │   - PostHog changelog
    │   - Dodo Payments updates
    │   - ModelContextProtocol.io (new MCPs)
    │   - GitHub trending (AI/voice/agents filter)
    │
    ├── Layer 2: Tavily (web search)
    │   Search queries (rotate weekly):
    │   - "new Claude MCP connectors [month year]"
    │   - "best AI voice tools 2026"
    │   - "new AI agent frameworks [month year]"
    │   - "Supabase new features [month year]"
    │   - "ElevenLabs new models [month year]"
    │   - "new developer tools for indie hackers [month year]"
    │
    ├── Layer 3: Claude Sonnet (api.anthropic.com direct)
    │   System prompt includes full TECH_STACK.md
    │   Task: rate each finding 1-5 on genuine upgrade value for QNC:
    │     5 = must evaluate immediately
    │     4 = worth testing this week
    │     3 = note for future consideration
    │     2 = interesting but not relevant to QNC
    │     1 = noise / marketing fluff
    │   Only output findings rated 3+
    │   Flag cost if any paid tier required
    │   Flag risk level (safe / low / medium / high)
    │
    └── Layer 4: Output
        Write to: vault/research-notes/stack-intel-YYYY-MM-DD.md
        Format: structured markdown (rating, tool name, what changed, why relevant, action)
        Trigger flag: if any rating 5 found → write ~/.config/qi/stack-intel-alert.flag
        QI 7am briefing reads flag → speaks summary of top findings
```

### Output format (per finding)
```markdown
## [Tool Name] — Rating: 4/5
**What changed:** [one sentence]
**Why relevant to QNC:** [one sentence]
**Cost impact:** [free / $X/mo / none]
**Risk:** [safe / low / medium]
**Action:** [evaluate / test / note / skip]
```

### Filtering philosophy
- **Include:** genuine new capabilities, version upgrades with meaningful features, new MCPs that extend what we do, tools that replace something we're already paying for at lower cost or better performance
- **Exclude:** hype articles with no substance, tools that duplicate what we have without clear upside, anything that adds complexity without proportional benefit, beta/alpha tools not production-ready

### Vault output location
`research-notes/stack-intel-YYYY-MM-DD.md` — auto-created daily.
QI brain index (`brain/_index.md`) should eventually reference this folder for semantic search.

### Build checklist (for next session)
- [ ] Create `scripts/qi-stack-intel.py` with 4-layer architecture above
- [ ] Wire monitored URLs list as config at top of script (easy to add/remove sources)
- [ ] Wire Tavily search queries as config list (easy to tune)
- [ ] Load TECH_STACK.md from vault path for Claude context
- [ ] Write output to `research-notes/` folder (create if not exists)
- [ ] Write alert flag file if rating-5 found
- [ ] Update `scripts/qi-morning-auto.sh` to check flag and include summary in briefing
- [ ] Add 6am cron entry
- [ ] Write `.claude/skills/qi-stack-intel/SKILL.md`
- [ ] Update QI AGENTS table in TECH_STACK.md
- [ ] Test run: `python3 scripts/qi-stack-intel.py --dry-run` (no cron, just output to terminal)
