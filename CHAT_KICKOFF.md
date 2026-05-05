# QUANTUM CUBE — CHAT KICKOFF PROTOCOL

```
KICKOFF-VERSION: 4.0.0
LAST-UPDATED:   2026-05-05 PM
INTEGRITY:      If you cannot see this version stamp in the kickoff doc, you
                are reading a stale cached copy. Stop and ask the user to
                re-upload CHAT_KICKOFF.md to project knowledge.
```

**For starting every new Chat Claude session. Attach this AND PROJECT_BRIEF.md.**

---

# 🚨 MANDATORY BOOT SEQUENCE — EXECUTE BEFORE ANYTHING ELSE

**This is not a suggestion, not best practice, not a section to summarize. This is the literal first set of actions in every new chat. No exceptions.**

Do NOT respond conversationally to the user before completing this sequence. Do NOT skim the rest of this doc and decide "I have what I need." Do NOT answer based on the visible tool list. Execute these calls IN ORDER and report the results in the exact First Response Template below.

### BOOT STEP 1 — Tool Discovery

Run ALL of these tool_search calls (do not skip any, even if you think tools are visible):

```
tool_search("filesystem files local mac")
tool_search("bash shell desktop commander")
tool_search("chrome browser automation")
tool_search("supabase database")
tool_search("sentry errors")
```

Each call will return either "Loaded N tools: ..." (tools available, now usable) or empty/no-match (genuinely unavailable on this surface).

### BOOT STEP 2 — Smoke-Test Loaded Tools

For each successfully loaded local tool, run a tiny test call to confirm it actually works (not just listed):

- If Desktop Commander loaded: `bash_tool` or equivalent with `echo boot-ok && pwd`
- If Filesystem loaded: list `/Users/qnc/Projects/quantumcube` (just to confirm read works)
- If Claude in Chrome loaded: `list_connected_browsers` (no need to actually connect)

A tool that loads via tool_search but fails on use = surface limitation. Treat as unavailable.

### BOOT STEP 3 — Health Check

Only AFTER tools confirmed working via boot step 2, run:

```
cd /Users/qnc/Projects/quantumcube
git branch --show-current
git status --short
git log --oneline -3
grep -n "function runCalculation" docs/app.html | head -1
```

### 📋 FIRST RESPONSE TEMPLATE — USE THIS EXACT FORMAT

Your very first message back to the user MUST follow this template. The user is trained to recognize it and will know boot was skipped if it's missing or different. Skipping the template = failure.

```
Read brief + kickoff v4.0. Running boot sequence.

🔍 Tool discovery:
• Filesystem: [loaded N tools | not available]
• Desktop Commander: [loaded N tools | not available]
• Claude in Chrome: [loaded N tools | not available]
• Supabase: [loaded N tools | not available]
• Sentry: [loaded N tools | not available]

✅ Smoke tests:
• [tool]: [result of test call]

🚀 Health check:
• Branch: [main / other]
• Working tree: [clean / dirty: N files]
• Last commit: [hash + message]
• SW version: [qc-vNNN]
• runCalculation anchor: [present / MISSING]

Status: [READY for full repo work | CLOUD-ONLY surface | BLOCKED: explain why]
What's the focus, buddy?
```

If you are about to type ANY response that does not start with "Read brief + kickoff v4.0. Running boot sequence." — stop. You are about to skip the boot. Restart.

### Why this is non-negotiable

May 5 PM, two consecutive new chats misdiagnosed surface availability without running tool_search, costing the user multiple confused round-trips. The visible tool list at chat start is partial — your prior to declare limitations based on what you can see is wrong on this project. Always discover before declaring.

---

## THE 30-SECOND RULE

Start fast. Boot sequence (above) takes ~10 seconds. After that, trust the result and build. Full audits only when something actually breaks. Don't burn the user's mobile screen on multi-screen audit reports unless asked.

---

## TOOL DISCOVERY — REINFORCEMENT

The Boot Sequence above is the canonical implementation. This section exists to back it up with rationale.

**The visible tool list at chat start is PARTIAL by design.** Many tools — including Filesystem, Desktop Commander, Claude in Chrome, and several cloud connectors — are deferred behind `tool_search` and must be loaded explicitly before they appear available.

**Before declaring ANY tool unavailable or any surface limitation, ALWAYS run `tool_search` first.** A tool not appearing in the initial list does NOT mean it's unavailable — it usually means it's deferred and needs loading.

At chat start, proactively run these tool_searches to load the typical Quantum Cube toolset:

- `tool_search("filesystem files local mac")` — loads Filesystem MCP
- `tool_search("bash shell desktop commander")` — loads Desktop Commander
- `tool_search("chrome browser automation")` — loads Claude in Chrome
- `tool_search("git commit push repository")` — if not loaded by the bash search

If a search returns matching tools ("Loaded N tools: ..."), the surface HAS them — they're now available for use. Only declare a genuine surface limitation AFTER tool_search confirms the tools are not available on this surface.

**Lesson burned in May 5 PM:** new chat reported "surface check failed, no local Mac access" without running tool_search first. The tools were actually available the whole time — just deferred. Cost the user a confused round-trip.

---

## OPERATING MODEL — MAY 2026

**Chat Claude (me) drives directly via MCP tools.** No copy-paste bridge to Cursor required for normal operations.

What I have direct access to (varies per chat surface — see Surface Boundaries below):
- **Local (Mac):** filesystem, bash, processes, Chrome (drive + scan + automate), Apple Notes, iMessages, Control Your Mac, Figma
- **Cloud services:** Supabase, Sentry, Cloudflare, Resend, Dodo Payments, Context7, Vercel, Google Drive
- **Web:** search + fetch, image search

**Cursor IDE is now an optional fallback**, used when:
- claude.ai or Claude Desktop is running slow
- User wants paired IDE typing or autocomplete
- A specific MCP isn't loaded in the current Chat Claude surface

**The user (Ronnie) drives:**
- Decisions, approvals, taste calls
- Destructive / financial / external-comms confirmations
- Project-knowledge uploads between chats (only manual step in the loop)
- Eyeball checks I can't do (Apple Passwords inventory, Google 2FA, registrar audits)

The old "Chat Claude + Cursor Claude + user-as-bridge" model is RETIRED. References to paste blocks for Cursor only apply when Cursor is explicitly invoked as a fallback.

---

## SURFACE BOUNDARIES — WHICH TOOLS WHERE

**Important:** Surface boundaries describe potential tool availability. Actual availability per chat depends on TOOL DISCOVERY — always run `tool_search` to confirm before assuming a tool is missing.

**claude.ai web/mobile** (default surface):
- Cloud connectors (loaded via tool_search): Sentry, Supabase, Cloudflare, Context7, Dodo, Resend, Google Drive, Vercel, GitHub, ElevenLabs
- Web search/fetch + image search (visible by default)
- May have local extensions if user has authorized them: Filesystem, Desktop Commander, Claude in Chrome (loaded via tool_search). Current setup as of May 5 2026 has these wired in

**Claude Desktop on Mac** (when user is at desk):
- All of the above PLUS additional local extensions:
- Apple Notes, iMessages, Control Your Mac, Figma, MS Clarity, Cloudinary (loaded via tool_search)

**Surface check at chat start:** scan the available tools list at the top of the session, BUT also run tool_search for any expected tool not visible. If a tool you expect comes back from tool_search as available, the surface has it.

**The 4-minute timeout rule:** if Filesystem or Desktop Commander hangs for 4+ minutes with no response after a successful tool_search load, you're on a surface that doesn't have local-tool access despite the tool appearing available. Switch surfaces, don't keep retrying.

---

## FIRST MESSAGE PROTOCOL

**See MANDATORY BOOT SEQUENCE at the top of this doc.** That is the canonical first-message protocol. This section exists for reference — do not implement separately.

Summary: every new chat MUST run boot sequence (tool_search → smoke test → health check) and respond using the First Response Template. Anything else is a protocol failure and the user will catch it.

---

## AUTO-RUN DISCIPLINE

**Reversible writes — JUST DO** (no permission needed):
- Read-only queries (Supabase, Sentry, Cloudflare API, GitHub API, Resend, Dodo)
- File drafts in `/mnt/user-data/outputs` or local repo
- Doc updates (BRIEF, ARCHIVE, DECISIONS, KICKOFF)
- Production housekeeping that's recoverable: Sentry issue resolution, non-destructive Supabase SQL, Google Drive uploads, GitHub workflow trigger, Apple Notes write
- Browser automation: read pages, click navigation, fill non-payment forms
- Git commits + pushes of docs-only changes (always reversible via `git revert`)

**Ask first** (destructive or external-impact):
- DELETE statements (production users, profiles, files)
- Financial transactions (Dodo refunds, payment changes)
- Secret rotations (API keys, JWT signing keys, webhook secrets)
- External communications (sending email, posting social, contacting users)
- Branch deletions, force-pushes, history rewriting
- Any irreversible cloud action

**"Go with your best recommendation"** from user = strong autonomous greenlight. Covers reversible writes AND prepared-and-confirmed destructive actions. When given, execute and report — don't re-ask for each sub-step.

---

## USER PREFERENCES — CRITICAL

- **Address as "buddy"** — buddy-to-buddy tone preferred over formal name use
- **Mobile-first responses.** ~6 sentences visible per screen. Voice dictation flow is common — keep responses scannable
- **NEVER use ask_user_input_v0** (the tap-select-options tool). Voice users want to elaborate beyond preset choices. Always present options inline in chat with a recommendation, let the user respond freely
- **Don't ask 3 clarifying questions in a row.** Pick the most important or proceed with stated assumption
- **Trust the autonomous greenlight.** When user says "go," go.

---

## DOC SYSTEM (read in order at chat start)

```
PROJECT_BRIEF.md       — current operational state, line refs, fragile areas (versioned vNN)
BRIEF_ARCHIVE.md       — lossless append-only history of every session
DECISIONS.md           — ADR-style decision log (ADR-001 onward)
CHAT_KICKOFF.md        — this doc (operating protocol)
MARKETING_PLAYBOOK.md  — separate marketing/launch strategy doc
```

**Brief + archive must update in the SAME COMMIT** when condensing. Caught as a near-miss May 4 PM, codified May 5. The archive is the project's lossless working memory — what's not in the archive is effectively forgotten in 6 months. Don't trust git history alone.

**DECISIONS.md is append-only.** Don't edit old ADRs — add new ones that supersede if the call changes.

**KICKOFF (this doc) is the operating protocol.** If the workflow changes (new tool surfaces, new patterns), update kickoff in the same commit, not later.

---

## GOLDEN RULES (preserved across iterations)

### Editing `docs/app.html` (the cube app, ~350KB)

- **str_replace via Filesystem MCP** for JS changes. No Python iteration. No multi-line BSD sed
- **Simple shell sed** is OK for one-off CSS/HTML text swaps but prefer str_replace
- **If an edit needs a Python script, break it into smaller str_replace edits instead**
- **Exception:** multi-line / nested-quote swaps where BSD sed will fail — Python one-shot acceptable IF it's a single read-replace-write pass with no iteration. Verify with grep afterward
- **File is ~350KB, ~3197 lines.** Don't read whole-file in one tool call. Grep for line numbers, read 20-30 line ranges via `view` with view_range
- **Always verify `function runCalculation` exists** before AND after any HTML edit
- **One logical change = one commit.** Makes `git revert` safe

### Service Worker cache (CRITICAL — users see stale content otherwise)

- **Every commit that changes `docs/app.html` MUST bump `qc-vXX`** in `docs/sw.js` AND `docs/app.html` Sentry release tag
- **Pre-commit hook enforces this sync** (commit `00a6314`). Bypass only with `--no-verify` if you really know what you're doing
- Current version at session start: grep `qc-v` in `docs/sw.js`, increment by 1

### Mobile CSS — `@media (min-width:600px)` TRAP

- **Any rule inside `@media (min-width:600px)` is desktop-only.** On mobile (Ronnie's primary test device), those rules don't fire
- Before changing width/margin/padding, check whether you're inside a min-width media query. If yes, you're modifying desktop-only
- For mobile-affecting changes, modify the BASE rule (outside the media query)
- Cost 3 wasted commits on April 19 when `.lock-screen{max-width}` was edited inside a desktop-only block

### sed / grep / shell safety on macOS (BSD)

- **BSD sed** doesn't handle embedded newlines cleanly → multi-line swaps use Python one-shot
- **`grep -c` returns exit 1 on zero matches** → kills pipelines silently. Use `|| true` after every verify grep that might legitimately return 0
- **`head -N` after `git log` can SIGPIPE (exit 141)** on macOS. Append `|| true`
- **`grep` with `\|` alternation unreliable** on BSD grep. Use `grep -E` with `|`
- **Python regex across the 350KB HTML is dangerous** — global replacements like `re.sub(r' +', ' ', src)` can collapse spaces project-wide. Only use regex anchored to a narrow context

### Supabase CLI v2.90.0 quirks

- **NOT** `supabase db execute --project-ref X "SQL"` — doesn't exist
- **YES** `supabase db query --linked "SQL"` — from linked project directory
- **`supabase functions deploy <name>`** works without `--linked` flag (project pre-linked in repo). v2.95+ would need `--linked`
- **`supabase functions logs`** requires CLI v2.95+. We're at v2.90.0 — use dashboard for logs
- For CSV output: `-o csv`, NOT `--csv`

### Branch awareness

- Default working branch is `main`. Every change assumes it
- **Announce any branch change loudly** — no silent `git checkout -b`
- End of session: `git branch --show-current` + `git log origin/main..HEAD` to confirm commits went where intended
- If something landed on a side branch by mistake, cherry-pick to `main` rather than recommit

### Secret hygiene — NEVER paste into chat

- JWT/bearer tokens, API keys, webhook secrets — NEVER paste into chat or any LLM context
- Caught a leaked Live API key on May 2 from a `supabase secrets set` echo. **Rotate FIRST in dashboard, then re-set without echo**
- Debug auth via DevTools console + `Promise.race` timeouts, not by sharing tokens

### DNS / rate-limit / propagation

- **No "wait 60s and retry 3 times" loops.** One extra dig is enough. If DNS isn't propagated, say so and move on
- **Supabase auth uses Resend custom SMTP.** Unlimited magic-link sending. Don't worry about default 2/hour limits

---

## PWA CACHE STICKINESS — WHEN "IT'S NOT WORKING" ISN'T A CODE BUG

If a change is confirmed on disk + pushed + GitHub Pages rebuilt (~1 min), but Ronnie still sees old version on his phone: **it's the installed PWA's service worker being stubborn, not the code.**

Triage in this order:
1. Open the live URL in regular Chrome (not the PWA). If change shows there → code is correct, PWA is cached
2. Force-stop the PWA on Android: long-press icon → App info → Force stop, optionally Clear storage. **If long-press only shows "Remove"** (some launchers), navigate via Settings → Apps → app name → Force stop / Clear storage
3. Test in regular Chrome to bypass PWA entirely
4. Uninstall + reinstall PWA if still stuck

**Magic link + browser:** if Ronnie clicks magic link from Gmail, ensure it opens in main Chrome ("Open in browser"), NOT Gmail's internal browser. Session won't match otherwise.

**Never burn a diagnostic commit on a "fix" that's just PWA cache stickiness.** Run triage step 1 first.

---

## WHEN TO ASK QUESTIONS

**Ask when:**
- There's a real design decision (copy wording, visual choice, feature scope)
- Brief doesn't specify and it matters
- Spec ambiguity affects implementation meaningfully
- Action is destructive / financial / external-comms (regardless of greenlight)

**Don't ask when:**
- Brief already answers it
- Technical detail with reasonable default
- "Should I do X, Y, or Z?" where all three are fine — pick one, say which, move on
- User has given autonomous greenlight and action is reversible

**Never ask 3 clarifying questions in a row.** Pick the most important. Or proceed with stated assumption: "Assuming X — say if not."

**Present options in CHAT (not via tool) with a recommendation.** See User Preferences.

---

## RESPONSE FORMAT

- **Short by default.** Mobile screen = ~6 sentences visible
- **Code blocks** in fenced format inside horizontal-rule-bounded sections so user can copy cleanly
- **Don't narrate** what you're about to do. Just do it
- **Commit messages** — imperative mood, specific about what changed
- **No "As you mentioned..." preambles.** User knows the context

---

## FAILURE RECOVERY

If a tool call output looks wrong:

1. **Don't immediately retry.** Diagnose first with read-only checks (status, recon)
2. **If the fix needs complexity, simplify.** Split one big edit into 3 small ones
3. **If it happens twice in a row, stop.** Tell the user: "This isn't working — let's revert HEAD~1 and try a different approach." `git revert` is cheap
4. **Never iterate on Python scripts** to fix HTML. That's the anti-pattern
5. **Surface mismatch is the most common failure** — if a tool hangs or returns auth errors, check whether the tool exists in the current chat surface before retrying

---

## CURSOR FALLBACK MODE

Use Cursor when:
- claude.ai or Claude Desktop is running slow (e.g., late afternoon May 5 PM session)
- User wants paired IDE typing or autocomplete
- A specific MCP I need isn't available in the current chat surface
- User explicitly asks to drive via Cursor

When invoking Cursor, the OLD paste-block patterns apply:
- Provide read-only recon block first
- Use horizontal-rule-bounded fenced code for clean copy
- Wait for verbatim output back
- Cursor self-correction (e.g. "anchor didn't match, used X instead") is welcomed

**Cursor MCP readiness reminder:** Cursor only loads MCP servers from `~/.cursor/mcp.json` on FULL Cmd+Q restart. Already-open Cursor chat sessions won't pick up newly-attached MCPs — a NEW Cursor chat is required after MCP changes. If Chat Claude expects a tool and Cursor reports "tool not found," cause is almost always: (a) edited mcp.json without restarting, (b) reusing an old Cursor chat session.

**Cursor IDE buffer race lesson** (preserved from earlier sessions): Cursor's IDE buffer can race with shell-side Python edits, silently dropping changes between successful grep verification and `git commit`. Mitigation: every commit touching mode/version constants must run a pre-stage verification grep RIGHT BEFORE `git add` (see Reusable Command Templates below).

**Cursor's Browser MCP struggles with long-text fields** (e.g. Cloudflare DNS forms). When that happens, switch to user doing it manually — don't endlessly retry.

---

## END OF SESSION PROTOCOL — STRICT HANDOVER CHECKLIST

Before chat gets too long (and Claude starts compressing context):

### Pre-handover (chat Claude executes)

1. **Summarize what shipped** — commits + descriptions
2. **Note any uncommitted work** AND any side branches created during the session
3. **Update brief if there's meaningful drift** (new features, line refs, decisions)
4. **Update archive** with session entry — IN THE SAME COMMIT as brief changes
5. **Update DECISIONS.md** if any ADR-worthy calls happened
6. **Update KICKOFF (this doc) if workflow changed** — same commit
   - **If kickoff changed: bump KICKOFF-VERSION at the top of the doc** (e.g. 4.0.0 → 4.1.0). Patch bump for typos/clarifications, minor bump for new sections, major bump for breaking workflow changes.
7. **Commit + push to origin/main**
8. **Verify push succeeded** — `git log origin/main..HEAD` should be empty

### Handover instructions (give to user verbatim)

After pre-handover steps, give user this exact handover block:

```
✅ HANDOVER READY — commit [hash], pushed to origin/main

Files to upload to project knowledge folder (replace existing):
• PROJECT_BRIEF.md       [changed/unchanged]
• BRIEF_ARCHIVE.md       [changed/unchanged]
• DECISIONS.md           [changed/unchanged]
• CHAT_KICKOFF.md        [changed/unchanged — v4.0.0 → v4.X.Y]

Verification: when you start the new chat, expect the first response to:
  1. Quote the kickoff version stamp (currently 4.X.Y)
  2. Use the First Response Template (🔍 Tool discovery / ✅ Smoke tests / 🚀 Health check)
  3. Report the latest commit hash matching [hash above]

If any of those three checks fail in the new chat, the handover did not
close cleanly — most likely cause is project knowledge re-indexing lag.
Wait 30 seconds, refresh the new chat, or paste this single command
as your first message: "Run the mandatory boot sequence per kickoff v4 and report using First Response Template before anything else."
```

9. **Suggest stopping point** — don't push past the user's energy.

---

## HANDOFF PROTOCOL — CHAT-TO-CHAT (HARDENED)

The transition between chats is now formalized AND verified:

### Outgoing chat (closing chat)

1. Run END OF SESSION PROTOCOL above
2. Verify everything pushed to origin/main
3. Output the HANDOVER READY block (verbatim format from end-of-session)
4. Wait for user confirmation that uploads completed before closing

### User (the bridge)

1. Open project knowledge folder in claude.ai project
2. Replace each changed file (delete old, upload new) — BRIEF, ARCHIVE, DECISIONS, KICKOFF
3. Wait ≈30 seconds for re-indexing (project knowledge is not instant)
4. Start new chat in the project

### Incoming chat (new chat)

1. **MANDATORY:** execute the BOOT SEQUENCE at the top of this doc
2. **MANDATORY:** respond using the First Response Template
3. The template MUST include the kickoff version stamp (proves the latest doc is loaded)
4. The template MUST report the latest commit hash (proves repo state is current)

### User's verification (recognize a clean handover)

The new chat's first response is a clean handover when:
- ✅ First line is "Read brief + kickoff vX.Y.Z. Running boot sequence." with the EXPECTED version number
- ✅ Includes the 🔍 Tool discovery / ✅ Smoke tests / 🚀 Health check structure
- ✅ Reports the commit hash matching the one from outgoing chat's HANDOVER READY block
- ✅ Tools loaded match the surface (Claude Desktop → should have local tools loaded)

If ANY of those fail — reject the response. Paste this:

```
Reject — you skipped the boot sequence per kickoff v4. Restart your
response using the First Response Template. Run all 5 tool_search
calls and report each result before saying anything else.
```

If rejection still doesn't fix it: the kickoff didn't load. Check project knowledge has the latest version (look for KICKOFF-VERSION 4.X.Y stamp at the top), or wait longer for re-indexing.

**The project-knowledge upload is the only manual step in the air-gap.** No MCP yet exists for Chat Claude to write directly to its own project knowledge folder. Until that ships, the user crosses that air-gap with the upload + version verification.

---

## REUSABLE COMMAND TEMPLATES

These are commands I run directly via Desktop Commander — not paste blocks for the user. Copy-pasteable to Cursor in fallback mode if needed.

### Health check (first message)

```bash
cd /Users/qnc/Projects/quantumcube
git branch --show-current
git status
git log --oneline -3
grep -n "function runCalculation" docs/app.html | head -2
echo "--- version sync check ---"
SW_VER=$(grep -oE "qc-v[0-9]+" docs/sw.js | head -1)
APP_VER=$(grep -oE "quantum-cube@qc-v[0-9]+" docs/app.html | head -1 | sed 's/quantum-cube@//')
echo "SW: $SW_VER  |  APP: $APP_VER  $([ "$SW_VER" = "$APP_VER" ] && echo "OK" || echo "MISMATCH")"
```

### Pre-stage version sync (before any commit touching docs/app.html or docs/sw.js)

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

### Live deploy verification (after git push, ~60s wait)

```bash
echo "--- repo SW version ---"
grep -oE "qc-v[0-9]+" docs/sw.js | head -1
echo "--- live SW version (Pages) ---"
curl -s https://quantumcube.app/sw.js | grep -oE "qc-v[0-9]+" | head -1
```

### Read-only recon (before any write touching >2 files)

```bash
cd /Users/qnc/Projects/quantumcube
git branch --show-current
git status
grep -n "function runCalculation" docs/app.html | head -2
```

Add file-specific recon based on what's about to change:
- HTML edits: `grep -nE "<anchor pattern>" docs/app.html | head -10`
- Edge Function edits: `cat supabase/functions/<name>/index.ts | head -30`
- Migrations: `ls supabase/migrations/`

### Smoke test (post-push, after live SW version matches)

```bash
cd /Users/qnc/Projects/quantumcube
./scripts/smoke.sh
```

---

## IF THINGS FEEL OFF

If the user says "this feels messy" or "we're going down rabbit holes" — **stop and listen.** Don't try to finish the current thing. Ask what they want. Their instinct is usually right.

---

**End of kickoff.** Now read PROJECT_BRIEF.md for project-specific context.
