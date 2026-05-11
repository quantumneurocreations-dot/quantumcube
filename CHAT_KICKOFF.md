---
tags: [core, kickoff]
---
# QUANTUM CUBE — CHAT KICKOFF PROTOCOL

```
KICKOFF-VERSION: 5.0.0
LAST-UPDATED:   2026-05-10
ARCHITECTURE:   Obsidian-first. All live docs read from vault via mcp-obsidian each boot.
                This is the ONLY file needed in Claude Project knowledge.
```

---

## 🚨 MANDATORY BOOT SEQUENCE — EXECUTE BEFORE ANYTHING ELSE

### STEP 1 — Load tools

```
tool_search("obsidian vault notes")          → mcp-obsidian (must load — vault is source of truth)
tool_search("bash shell desktop commander")  → Desktop Commander
tool_search("supabase database")             → Supabase MCP
tool_search("sentry errors")                 → Sentry MCP
tool_search("github repository")             → GitHub MCP
```

### STEP 2 — Read live docs from Obsidian vault

```
mcp-obsidian: get SESSION_LOG.md    → read top entry only (current session state)
mcp-obsidian: get PROJECT_BRIEF.md  → current app state, line refs, fragile areas
```

These files are ALWAYS current — no project-knowledge lag. No re-uploading needed.
If vault reads fail → Obsidian app is closed → tell user to open Obsidian and retry.

### STEP 3 — Health check (Desktop Commander)

```bash
cd /Users/qnc/Projects/quantumcube && git log --oneline -3 && git status --short
SW_VER=$(grep -oE "qc-v[0-9]+" docs/sw.js | head -1)
APP_VER=$(grep -oE "quantum-cube@qc-v[0-9]+" docs/app.html | head -1 | sed 's/quantum-cube@//')
echo "SW: $SW_VER | APP: $APP_VER $([ "$SW_VER" = "$APP_VER" ] && echo OK || echo MISMATCH)"
```

### 📋 FIRST RESPONSE TEMPLATE

```
Read kickoff v5.0.0. Running Obsidian-first boot.

🔍 Tools loaded:
• mcp-obsidian: [loaded N tools | MISSING — Obsidian may be closed]
• Desktop Commander: [loaded / not available]
• Supabase: [loaded / not available]
• Sentry: [loaded / not available]
• GitHub: [loaded / not available]

📖 Docs read from Obsidian:
• SESSION_LOG: [last entry date + one-line goal]
• PROJECT_BRIEF: [version vNN]

🚀 Health check:
• Branch: [main / other]
• Working tree: [clean / dirty: N files]
• Last commit: [hash + message]
• SW version: [qc-vNNN | MISMATCH ⚠️]

Status: [READY | BLOCKED: explain]
What's the focus, buddy?
```

---

## SURFACE & CONNECTIVITY

**Always Claude Desktop** — user uses speech-to-text microphone (Desktop-only feature).
**Obsidian** must be running for mcp-obsidian to work. Vault = `/Users/qnc/Projects/quantumcube`.
**Obsidian Git plugin** auto-commits + pushes vault changes every 10 min — no manual git needed for doc edits.

---

## USER PREFERENCES — CRITICAL

- **Address as "buddy"** — buddy-to-buddy tone, never formal name
- **Mobile-first responses** — ~6 sentences per screen, speech-to-text flow
- **NEVER use ask_user_input_v0** — voice users can't tap options; ask inline or assume + flag
- **No 3 clarifying questions in a row** — pick one or proceed with stated assumption
- **Autonomous greenlight:** reversible writes (file edits, commits, Sentry resolves, Supabase reads) = just do it and report. Ask before: deletes, financial, secret rotations, external email, irreversible actions

---

## KEY OPERATIONAL FACTS

- **Android package:** `app.quantumcube.twa` | Keystore: `android/quantumcube.keystore` (pw in Apple Passwords)
- **Supabase:** project `fqqdldvnxupzxvvbyvjm`, eu-central-1, Postgres 17.6
- **Sentry:** org `quantum-neuro-creations`, project `javascript`, EU region
- **PostHog:** project 172921, EU, `https://eu.i.posthog.com`
- **app.html:** ~350KB / ~3197 lines — use str_replace only, never read whole file, always verify `runCalculation` anchor before + after edits
- **SW + Sentry release must stay in sync** — pre-commit hook enforces. Never `--no-verify`
- **ElevenLabs voice:** `eleven_turbo_v2_5`, stability 0.5, similarity_boost 0.75, speed 1.15 (welcome.mp3: speed 1.0)

---

## OBSIDIAN VAULT — DOC MAP

All docs live in `/Users/qnc/Projects/quantumcube` and are readable via mcp-obsidian:

| File | Purpose | Read when |
|------|---------|-----------|
| `SESSION_LOG.md` | Live session narrative | Every boot |
| `PROJECT_BRIEF.md` | App state, line refs, fragile areas | Every boot |
| `DECISIONS.md` | ADR log, append-only | On demand |
| `BRIEF_ARCHIVE.md` | Lossless session history | On demand |
| `OPERATING_RULES.md` | Golden rules, command templates, failure recovery | On demand |
| `MARKETING_PLAYBOOK.md` | Launch strategy | On demand |

---

## END OF SESSION (simplified)

1. Commit all changes + push to origin/main
2. Update SESSION_LOG.md with session entry (Obsidian Git will sync it)
3. **No project knowledge upload needed** — Obsidian reads live files every boot
4. Only re-upload this CHAT_KICKOFF.md to project knowledge if KICKOFF-VERSION changes

---

**Full golden rules, command templates, Cursor fallback, failure recovery, PWA cache debugging:**
→ read `OPERATING_RULES.md` from Obsidian vault on demand.

<!-- KICKOFF-VERSION: 5.1.0 — added CONNECTORS.md to boot + golden rules ref -->

---

## BOOT SEQUENCE UPDATE (v5.1.0)

CONNECTORS.md is now a mandatory boot read alongside SESSION_LOG + PROJECT_BRIEF.

**Updated Step 2:**
```
mcp-obsidian: get SESSION_LOG.md    → read top entry only
mcp-obsidian: get PROJECT_BRIEF.md  → app state, line refs, fragile areas
mcp-obsidian: get CONNECTORS.md     → ALL service IDs, MCP map, golden rules ← NEW
```

**Updated First Response Template — add this line under Docs read:**
```
• CONNECTORS: [confirmed — Cloudflare/Supabase/Sentry/PostHog/GitHub loaded]
```

**KICKOFF-VERSION: 5.1.0** — previous 5.0.0 lacked CONNECTORS.md in boot.
Re-upload this file to Claude Project knowledge to activate the v5.1.0 boot.
