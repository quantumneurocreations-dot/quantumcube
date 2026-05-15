# Chief of Staff

QI's daily briefing agent. Owen's voice + Claude's reasoning + live data = 3 daily priorities.

## What it does

Every morning at 7am (or on demand), the CoS reads strategic context from brain/ + pulls live metrics, then delivers exactly 3 voiced priorities. Ends with: **"That is your focus. Go."**

## Architecture

```
brain/business/north-star.md  ─┐
brain/projects/qi-system.md    ├─► build_cos_prompt() ─► Claude Haiku ─► Owen
localhost:3001/api/briefing   ─┘         (qi-voice.py)
```

## Trigger phrases
"morning briefing" · "top priorities" · "chief of staff" · "start my day" · "run my day" · "priorities for today" — 15 total in qi-voice.py

## Output format
```
First, [one punchy sentence grounded in data].
Second, [one punchy sentence].
Third, [one punchy sentence].
That is your focus. Go.
```

## Status
- ✅ Live in qi-voice.py
- ✅ Brain/ integration (north-star.md + qi-system.md injected into prompt)
- ✅ SKILL.md at .claude/skills/chief-of-staff/
- ✅ Claude Code /cos command
- ✅ 7am cron via qi-morning-auto.sh
- 🔲 War Room agent card (dashboard tile)

## Agent role in War Room
CoS = **Agent 0 — The Orchestrator**. Runs every morning. Sets the daily frame. All other agents (Head of Design, Revenue, Code, etc.) execute within the priorities CoS defines.

## Cross-references
- [[north-star]] — what CoS reads for strategic context
- [[qi-system]] — system status CoS reads
- [[../../scripts/qi-voice.py]] — implementation
