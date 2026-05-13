---
tags: [core, reference, rules]
---
# QUANTUM CUBE — OPERATING RULES

Detailed reference doc. Read from Obsidian on demand — not needed at every boot.
Contains everything from CHAT_KICKOFF v4.x that isn't in the lean v5.0.0 boot doc.

---

## EDITING `docs/app.html` (the cube app, ~350KB)

- **str_replace via Filesystem MCP** for JS changes. No Python iteration. No multi-line BSD sed
- **Simple shell sed** is OK for one-off CSS/HTML text swaps but prefer str_replace
- **File is ~350KB, ~3197 lines.** Don't read whole-file in one tool call. Grep for line numbers, read 20-30 line ranges
- **Always verify `function runCalculation` exists** before AND after any HTML edit
- **One logical change = one commit.** Makes `git revert` safe

## SERVICE WORKER CACHE (CRITICAL)

- **Every commit that changes `docs/app.html` MUST bump `qc-vXX`** in `docs/sw.js` AND `docs/app.html` Sentry release tag
- **Pre-commit hook enforces this sync.** Bypass only with `--no-verify` if you really know what you're doing

## MOBILE CSS TRAP — `@media (min-width:600px)`

- **Any rule inside `@media (min-width:600px)` is desktop-only.** On mobile those rules don't fire
- For mobile-affecting changes, modify the BASE rule (outside the media query)

## BSD SED / GREP / SHELL SAFETY ON macOS

- **BSD sed** doesn't handle embedded newlines → multi-line swaps use Python one-shot
- **`grep -c` returns exit 1 on zero matches** → kills pipelines. Use `|| true`
- **`head -N` after `git log` can SIGPIPE (exit 141)** on macOS. Append `|| true`
- **`grep` with `\|` alternation unreliable** on BSD grep. Use `grep -E` with `|`

## SUPABASE MCP vs CLI

Prefer MCP:
- `Supabase:deploy_edge_function` — preferred over CLI deploy
- `Supabase:get_logs` — preferred over `supabase functions logs` (CLI v2.90.0 doesn't support it)
- `Supabase:execute_sql`, `apply_migration`, `list_migrations` — always available

CLI quirks (v2.90.0):
- `supabase db query --linked "SQL"` — correct syntax
- `supabase functions deploy <name>` — works without `--linked` flag at v2.90.0

## SECRET HYGIENE

- JWT/bearer tokens, API keys, webhook secrets — NEVER paste into chat or LLM context
- Debug auth via DevTools console, not by sharing tokens

## BRANCH AWARENESS

- Default working branch is `main`
- **Announce any branch change loudly** — no silent `git checkout -b`
- End of session: `git branch --show-current` + `git log origin/main..HEAD` to confirm

## PWA CACHE STICKINESS

If change confirmed on disk + pushed but user still sees old version on phone:

1. Open live URL in regular Chrome (not PWA) — if change shows there → code correct, PWA cached
2. Force-stop PWA on Android: long-press icon → App info → Force stop / Clear storage
3. Test in regular Chrome to bypass PWA
4. Uninstall + reinstall PWA if still stuck

## FAILURE RECOVERY

1. Don't immediately retry — diagnose first with read-only checks
2. If fix needs complexity, simplify — split one big edit into 3 small ones
3. If it fails twice in a row: tell user, revert HEAD~1, try different approach
4. Never iterate on Python scripts to fix HTML
5. Surface mismatch is the most common failure — check tool availability before retrying

## REUSABLE COMMAND TEMPLATES

### Health check
```bash
cd /Users/qnc/Projects/quantumcube
git branch --show-current && git status && git log --oneline -3
SW_VER=$(grep -oE "qc-v[0-9]+" docs/sw.js | head -1)
APP_VER=$(grep -oE "quantum-cube@qc-v[0-9]+" docs/app.html | head -1 | sed 's/quantum-cube@//')
echo "SW: $SW_VER  |  APP: $APP_VER  $([ "$SW_VER" = "$APP_VER" ] && echo OK || echo MISMATCH)"
```

### Pre-stage version sync
```bash
EXPECTED=qc-vNNN
SW_VER=$(grep -oE "qc-v[0-9]+" docs/sw.js | head -1)
APP_VER=$(grep -oE "quantum-cube@qc-v[0-9]+" docs/app.html | head -1 | sed 's/quantum-cube@//')
if [ "$SW_VER" = "$EXPECTED" ] && [ "$APP_VER" = "$EXPECTED" ]; then
  echo "in sync at $EXPECTED — safe to ship"
else
  echo "MISMATCH: SW=$SW_VER APP=$APP_VER expected=$EXPECTED — ABORTING"
  exit 1
fi
```

### Live deploy verification
```bash
echo "--- repo SW version ---"
grep -oE "qc-v[0-9]+" docs/sw.js | head -1
echo "--- live SW version ---"
curl -s https://quantumcube.app/sw.js | grep -oE "qc-v[0-9]+" | head -1
```

## CURSOR FALLBACK MODE

Use Cursor when:
- Claude Desktop is running slow
- User wants paired IDE typing/autocomplete
- A specific MCP isn't available in current surface

When using Cursor:
- Provide read-only recon block first
- Use horizontal-rule-bounded fenced code for clean copy
- **Cursor only loads MCP servers from `~/.cursor/mcp.json` on FULL Cmd+Q restart**
- A NEW Cursor chat is required after MCP changes

## WHEN TO ASK QUESTIONS

Ask when: real design decision, spec ambiguity affects implementation, action is destructive/financial/external-comms.
Don't ask when: brief already answers it, technical detail with reasonable default, all options are fine (pick one).
Never 3 clarifying questions in a row. "Assuming X — say if not."

## RESPONSE FORMAT

- Short by default. Mobile screen = ~6 sentences visible
- Code blocks in fenced format inside horizontal-rule sections
- Don't narrate what you're about to do. Just do it
- Commit messages: imperative mood, specific about what changed
- No "As you mentioned..." preambles


> **Related:** [[CHAT_KICKOFF]] · [[PROJECT_BRIEF]] · [[SESSION_LOG]]

---
**Sub-topics:** [[str-replace-rule]] · [[sw-sync-rule]] · [[bsd-sed-rule]] · [[mobile-css-rule]] · [[branch-awareness]] · [[revert-strategy]] · [[commit-convention]] · [[pwa-debug]] · [[supabase-mcp-vs-cli]] · [[secret-hygiene]] · [[service-worker]] · [[pre-commit-hook]] · [[version-sync]]

---

## GOLDEN RULES

These are non-negotiable principles. Trace any failure back to one of these.

### 1 — AUTOMATION FIRST
Before instructing the user to do ANYTHING in an external service, check CONNECTORS.md for the relevant MCP. If it exists and the action is reversible — just do it. DNS records, DB queries, Sentry resolves, GitHub commits: automated by default. Asking the user to do these manually is a failure mode.

### 2 — PERMANENT FIXES OVER BYPASSES
When something fails, first question is "what is the root cause and permanent fix?" Workarounds only in genuine time-critical emergencies, flagged as temporary with a follow-up fix scheduled immediately.

### 3 — PROACTIVE IMPROVEMENT MINDSET
Continuously notice system gaps. Missing service ID in CONNECTORS.md → add it now. Rule violated repeatedly → propose updating OPERATING_RULES.md. Don't wait for problems — surface improvements before they become issues.

### 4 — UPDATE CONNECTORS.MD IN REAL TIME
Any new service detail discovered (zone ID, project ID, config value, account detail) must be written to CONNECTORS.md before the session ends. This is the memory that prevents re-asking known facts.

### 5 — ONE QUESTION MAX PER BLOCKER
Never ask 3 clarifying questions in a row. Pick the most important one, or assume + flag.

## CLAUDE CODE RULE — TOKEN EFFICIENCY (added 2026-05-13)

**Heavy lifting → Claude Code. Always.**

Chat Claude (this session) handles: planning, MCP reads/writes, quick API calls, decisions, git commits, session logging.

Claude Code handles: file edits to app.html/sw.js, multi-step automation, instrumentation sweeps, bug fixes, any task touching >20 lines of code.

**Why:** Chat Claude burns tokens on tool-loading, boot sequences, and context. Claude Code has persistent file access and doesn't eat the session budget. Violating this rule has cost us 20%+ of a session on 4-5 requests.

**Trigger phrase:** "Hand to Claude Code" = write a tight brief and stop. Don't attempt the work in Chat Claude first.

## BOOT — SENTRY CHECK (added 2026-05-13)

Add this to every session boot after health check:

```
https://mcp.sentry.dev/mcp: search_events
  org: quantum-neuro-creations
  project: javascript
  dataset: errors
  statsPeriod: 24h
  sort: -count()
```

Report: "🔴 N new Sentry issues since last session" or "✅ Sentry clean."
If issues found → list title + count before asking what's the focus.
