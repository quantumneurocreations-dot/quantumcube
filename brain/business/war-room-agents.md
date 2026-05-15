# War Room — Agent Map

The War Room is QI's multi-agent command centre. 7 named agents, each with a specific domain. CoS runs first each morning and sets priorities — all other agents operate within that frame.

## The 7 Agents

| # | Agent | Domain | Status |
|---|-------|--------|--------|
| 0 | **Chief of Staff (CoS)** | Daily priorities, morning briefing, strategic frame | ✅ Live |
| 1 | **Head of Design** | UI mockups, component generation, brand enforcement | 🔲 Building next |
| 2 | **Revenue Agent** | Customer growth, pricing, conversion optimisation | 🔲 Planned |
| 3 | **Code Agent** | Bug triage, Claude Code orchestration, shipping queue | 🔲 Planned |
| 4 | **Marketing Agent** | Ad creatives, video generation, campaign launch (fal.ai + Creatify) | 🔲 Planned |
| 5 | **Analytics Agent** | PostHog insights, session review, funnel analysis | 🔲 Planned |
| 6 | **Ops Agent** | Sentry errors, infra health, cron monitoring, UptimeRobot | 🔲 Planned |

## Agent architecture (standard pattern)

Each agent follows the same pattern:
```
SKILL.md (knowledge + rules)
  ↓
Claude Code command (/agent-name)
  ↓
brain/ context files (domain knowledge)
  ↓
Live data (API calls relevant to domain)
  ↓
Output (voice via Owen / dashboard tile / file output)
```

## Dashboard layout (War Room tiles)
```
┌──────────────────────────────────────────────────────┐
│  ☀️ CHIEF OF STAFF    │  🎨 HEAD OF DESIGN           │
│  3 priorities · 7am  │  Last mockup: —               │
├──────────────────────┼──────────────────────────────-│
│  💰 REVENUE          │  💻 CODE                      │
│  4 customers / 500   │  0 Sentry errors              │
├──────────────────────┼───────────────────────────────│
│  📣 MARKETING        │  📊 ANALYTICS                 │
│  fal.ai ready        │  24 sessions today            │
├──────────────────────┴───────────────────────────────│
│  ⚙️ OPS · All systems UP · 100% uptime               │
└──────────────────────────────────────────────────────┘
```

## Build order
1. ✅ CoS (Agent 0) — live
2. 🔲 Head of Design (Agent 1) — building this sprint
3. 🔲 Marketing Agent (Agent 4) — fal.ai key ready, build after Head of Design
4. 🔲 Others — sequentially after

## Cross-references
- [[chief-of-staff]] — Agent 0 detail
- [[../../CONNECTORS]] — fal.ai, Creatify, HeyGen keys
