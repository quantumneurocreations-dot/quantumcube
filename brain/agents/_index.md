---
tags: [core, agents]
---
# QNC AGENT IDENTITY REGISTRY

## AGENT NAMING CONVENTION

Agents are referred to by their function, not by person names. Simple, clean, unambiguous. When you say it in conversation — to QI or in this chat — there's no confusion about who's who.

| Call name | Full agent | Script |
|-----------|-----------|--------|
| **QI** | QI Voice — main agent | `scripts/qi-voice.py` |
| **CoS** | Chief of Staff (mode within QI) | `scripts/morning-briefing.py` |
| **Design** | Head of Design | `scripts/head_of_design.py` |
| **Upgrade** | Stack Intelligence Agent | `scripts/qi-stack-intel.py` (pending) |
| **Marketing** | Marketing Agent | `scripts/qi-marketing.py` (pending) |
| **Revenue** | Revenue Agent | `scripts/qi-revenue.py` (pending) |
| **Security** | Security Agent (3am cron) | `scripts/qi-security.py` |
| **Calendar** | Google Calendar (wired into CoS) | `scripts/qi-calendar.py` |
| **Memory** | Session Memory | `scripts/qi_memory.py` |

Usage: "How's security looking?" = Security agent + its logs. "Run upgrade" = trigger Upgrade's scan. "Ask design to..." = Head of Design brief.


Every QI agent loads a vault identity document at runtime as its system context.
No hardcoded worldviews in scripts — the vault is the brain for agents too.

---

## WHAT AN IDENTITY DOCUMENT IS

Each agent has a `brain/agents/<name>/identity.md` file that provides:
- Who the agent is and its personality/voice
- Its one specific job (narrow mandate, not general AI)
- The QNC world it operates in — business context, current state
- Its capabilities and tool access
- Its constraints and escalation path
- Where to find more detail (links to TECH_STACK, CONNECTORS, NORTH_STAR, PROJECT_BRIEF)

Scripts load this at startup via `read_vault_file("brain/agents/<name>/identity.md")` and inject it as the system prompt or the first block of context.

---

## AGENT REGISTRY

| Agent | Identity doc | Script | Status |
|-------|-------------|--------|--------|
| QI Voice (main) | `brain/agents/qi-voice/identity.md` | `scripts/qi-voice.py` | ✅ Live |
| Chief of Staff | `brain/agents/chief-of-staff/identity.md` | `scripts/morning-briefing.py` | ✅ Live |
| Head of Design | `brain/agents/head-of-design/identity.md` | `scripts/head_of_design.py` | ✅ Live |
| Stack Intel | `brain/agents/stack-intel/identity.md` | `scripts/qi-stack-intel.py` | 🔴 Pending |
| Marketing Agent | `brain/agents/marketing/identity.md` | `scripts/qi-marketing.py` | 🔴 Pending |
| Revenue Agent | `brain/agents/revenue/identity.md` | `scripts/qi-revenue.py` | 🔴 Pending |

---

## HOW TO LOAD IN A SCRIPT

Add this helper to any QI agent script:

```python
from pathlib import Path

VAULT_ROOT = Path("/Users/qnc/Projects/quantum-integrator")

def load_agent_identity(agent_name: str) -> str:
    """Load agent identity document from vault as system context."""
    path = VAULT_ROOT / f"brain/agents/{agent_name}/identity.md"
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"You are QI, an AI operating system for Quantum Neuro Creations."

# Usage:
SYSTEM_PROMPT = load_agent_identity("chief-of-staff")
```

---

## IDENTITY DOCUMENT TEMPLATE

Copy for each new agent:

```markdown
---
agent: [agent-name]
version: 1.0.0
updated: YYYY-MM-DD
---
# [Agent Name] — Identity & World Context

## Who I am
[1-2 sentences: role, personality, voice style]

## My one job
[Narrow mandate — what I do and what I explicitly don't do]

## The world I operate in

**Organisation:** Quantum Neuro Creations (QNC) — South Africa
**Products:** Quantum Cube (quantumcube.app) — live, 4 paying customers | QI — this system
**Goal:** 500 paying customers by Aug 15, 2026 at $17 one-time = $8,500 gross
**Infrastructure:** Mac Mini M4 · Supabase (EU) · Cloudflare · GitHub Pages · ElevenLabs TTS · PostHog · Sentry
**Human:** Ronnie — founder, voice/STT input, direct tone preferred

## My capabilities
- [What tools/APIs I can call]
- [What data I have access to]

## My constraints
- [What I don't do]
- [When to escalate to Ronnie]
- Never store sensitive keys in memory or logs

## Reference docs (read when needed)
- NORTH_STAR.md — 500 customer goal, milestones
- PROJECT_BRIEF.md — current QC + QI state
- CONNECTORS.md — all service IDs and API key locations
- TECH_STACK.md — full tool inventory
- DECISIONS.md — why things were built the way they were
```

---

> **Related:** [[TECH_STACK]] · [[CONNECTORS]] · [[OPERATING_RULES]] · [[NORTH_STAR]]

---

## FINAL AGENT ROSTER — LOCKED 2026-05-16

QI is the OS — overseer, delegator, voice, feedback loop. Seven agents do the heavy lifting. QI reads their outputs, speaks summaries, routes commands. QI handles nothing that an agent can handle.

| Agent | Core mandate | Primary tools | Status |
|-------|-------------|---------------|--------|
| **QI** | OS, voice, delegator, overseer | Claude Haiku · ElevenLabs · Deepgram | ✅ Live |
| **Upgrade** | Tech radar — stack + agent evolution | Firecrawl · Tavily · Claude Sonnet | 🔴 Build pending |
| **Design** | Brand, visual, image, video — QNC's face | Claude Sonnet · Fal.ai | ✅ Live |
| **Marketing** | Social, ads, trends, analytics, conversion | Tavily · PostHog · Fal.ai · Claude Sonnet | 🔴 Build pending |
| **Security** | All security + QC app health + Sentry | File audit · Sentry API · osascript | ✅ Live |
| **Mind** | Vault, memory, documents, knowledge graph | Obsidian · QMD · Claude Haiku | 🔴 Build pending |
| **Admin** | Calendar, email, finance, ops | Google Calendar · Gmail · Dodo · Supabase | 🔴 Build pending |

**Architecture:** QI is the interface. Agents run on crons and write reports to `research-notes/` or vault. QI reads reports and speaks summaries on demand or at 7am briefing.

**No Sales agent** — QC is B2C. Marketing *is* the sales engine. Analytics fold into Marketing (data and action are inseparable).

**No Dev agent** — Security watches QC app health and Sentry. Code changes are handled by Claude Code in terminal, not an autonomous agent.
