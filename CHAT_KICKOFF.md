---
tags: [core, kickoff]
---
# QUANTUM CUBE — CHAT KICKOFF PROTOCOL

```
KICKOFF-VERSION: 6.0.0
LAST-UPDATED:   2026-05-15
VAULT:          /Users/qnc/Projects/quantumcube
ARCHITECTURE:   Obsidian-first. Single file in project knowledge. Vault = source of truth.
```

---

## 🚨 BOOT SEQUENCE — EXECUTE BEFORE ANYTHING ELSE

### STEP 1 — Load tools (minimum — do NOT over-load)

```
tool_search("obsidian vault notes")          → mcp-obsidian  ← always needed
tool_search("bash shell desktop commander")  → Desktop Commander  ← always needed
```

Load additional tools only when the session task requires them:
- `tool_search("github repository")`   → only when committing / reviewing PRs
- `tool_search("supabase database")`   → only when querying DB directly
- `tool_search("sentry errors")`       → only when investigating errors
- `tool_search("posthog analytics")`   → only when running analytics queries

**DO NOT speculatively load all tools. Every tool_search = ~500 tokens wasted.**

### STEP 2 — Read live docs (lean reads only)

```
mcp-obsidian: get SESSION_LOG.md    → TOP ENTRY ONLY — stop at the second --- separator
mcp-obsidian: get CONNECTORS.md     → service IDs, key locations, MCP map
```

Read on demand (not every boot):
- `PROJECT_BRIEF.md` → only when doing code work or needing line refs
- `NORTH_STAR.md`    → only when discussing strategy or goal tracking
- `DECISIONS.md`     → only when reviewing or logging an ADR

⚠️ SESSION_LOG is a long append-only file — read the TOP ENTRY ONLY.
If vault reads fail → Obsidian is closed → tell user to open Obsidian and retry.

### STEP 3 — Health check

```bash
cd /Users/qnc/Projects/quantumcube && git log --oneline -3 && git status --short
SW_VER=$(grep -oE "qc-v[0-9]+" docs/sw.js | head -1)
APP_VER=$(grep -oE "quantum-cube@qc-v[0-9]+" docs/app.html | head -1 | sed 's/quantum-cube@//')
echo "SW: $SW_VER | APP: $APP_VER $([ "$SW_VER" = "$APP_VER" ] && echo OK || echo MISMATCH)"
```

### 📋 FIRST RESPONSE TEMPLATE

```
Read QC kickoff v6.0.0.

🔍 Tools: mcp-obsidian ✅ | Desktop Commander ✅
📖 SESSION_LOG: [date — one-line goal]
🔗 CONNECTORS: confirmed

🚀 Health:
• Branch: [main/other] | Tree: [clean/dirty N files]
• Last commit: [hash message]
• SW: [qc-vNNN ✅ | MISMATCH ⚠️]

What's the focus, buddy?
```

---

## CONTEXT DISCIPLINE — MANDATORY

| Rule | Reason |
|------|--------|
| SESSION_LOG: top entry only, stop at second `---` | File is 1000+ lines |
| Never read `app.html` whole | 350KB = ~90K tokens |
| `app.html` edits: str_replace with anchor verification only | Always check `runCalculation` before + after |
| Load tool_search lazily — only what the task needs | Each call costs context |
| When chat runs long → wrap, commit, start fresh | Better than hitting the wall mid-task |
| One task per chat when possible | Prevents context bleed between concerns |

---

## SURFACE & CONNECTIVITY

**Always Claude Desktop** — user uses speech-to-text mic (Desktop-only).
**Obsidian** must be running. Vault = `/Users/qnc/Projects/quantumcube`.
**Obsidian Git** auto-commits + pushes every 10 min — no manual git for doc edits.

---

## USER PREFERENCES

- **"buddy"** — informal peer tone, never formal name
- **Voice/speech-to-text** — never use `ask_user_input_v0` option pickers; ask inline or assume + flag
- **Mobile-first** — ~6 sentences per screen
- **Autonomous greenlight** — reversible writes (file edits, commits, Sentry resolves, non-destructive SQL) = just do it and report
- **Ask before** — destructive deletes, financial, secret rotations, external email, irreversible

---

## KEY FACTS (inline — no extra file reads needed)

- **App:** `https://quantumcube.app` | PWA + Android TWA `app.quantumcube.twa`
- **Supabase:** `fqqdldvnxupzxvvbyvjm`, eu-central-1, Postgres 17.6
- **Sentry:** org `quantum-neuro-creations`, project `javascript`, EU
- **PostHog:** project 172921, EU, `https://eu.i.posthog.com`
- **ElevenLabs:** `eleven_turbo_v2_5`, stability 0.5, similarity_boost 0.75, speed 1.15
- **North Star:** 500 paying customers by Aug 15 2026 — currently in 14-day Play Store testing window (started May 14, apply production ~May 28)
- **app.html:** ~3200 lines — str_replace only, anchor = `runCalculation`
- **SW + Sentry release must stay in sync** — pre-commit hook enforces, never `--no-verify`
- **Android keystore:** `android/quantumcube.keystore` — pw in Apple Passwords

---

## VAULT DOC MAP

| File | Purpose | Read when |
|------|---------|-----------|
| `SESSION_LOG.md` | Session history — **TOP ENTRY ONLY** | Every boot |
| `CONNECTORS.md` | All service IDs, MCP map, golden rules | Every boot |
| `PROJECT_BRIEF.md` | App state, line refs, fragile areas | Code work only |
| `NORTH_STAR.md` | Goal, milestones, guardrails | Strategy only |
| `DECISIONS.md` | ADR log, append-only | On demand |
| `OPERATING_RULES.md` | Golden rules, command templates, recovery | On demand |
| `MARKETING_PLAYBOOK.md` | Launch strategy | On demand |

---

## END OF SESSION

1. Commit all changes + push to origin/main
2. Prepend new entry to SESSION_LOG.md (Obsidian Git syncs automatically)
3. Only re-upload this file to project knowledge if KICKOFF-VERSION changes
