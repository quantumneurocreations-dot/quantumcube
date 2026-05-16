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
