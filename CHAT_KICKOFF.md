# QUANTUM CUBE — CHAT KICKOFF PROTOCOL
**For starting every new Chat Claude session. Attach this AND PROJECT_BRIEF.md.**

> **Updated May 5, 2026 PM — full rewrite for direct-MCP operating model.** Cursor demoted from primary driver to optional fallback. New sections: surface boundaries, auto-run discipline, handoff protocol. Old paste-to-Cursor patterns preserved in Cursor Fallback Mode section.

---

## THE 30-SECOND RULE

Start fast. One minimal health check, trust the result, build. Full audits only when something actually breaks. Don't burn the user's mobile screen on multi-screen audit reports unless asked.

---

## TOOL DISCOVERY — CRITICAL FIRST STEP

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

When user opens a new chat with brief + kickoff attached:

1. **Acknowledge briefly** — "Read the brief + kickoff, ready to go." That's enough.
2. **Run TOOL DISCOVERY first** (see Tool Discovery section above). Load Filesystem, Desktop Commander, Chrome via tool_search. This is non-optional — skip it and you will misdiagnose surface availability.
3. **THEN run minimal health check directly** (no paste block to user):
   - `git status` + `git branch --show-current` + `git log --oneline -3`
   - Grep `runCalculation` in `docs/app.html` (fragile-area canary)
   - Confirm `docs/sw.js` cache version matches Sentry release tag in `docs/app.html`
   - Optional: DNS check only if today's work touches email/domain
   - Optional: connector ping only if relying on a specific cloud service
4. **Report 1-2 sentences** of status — "On main, clean tree, qc-v201 synced, ready" — and ask what's needed.

**No multi-screen audit at startup.** Trust the result. Burn time only when something looks suspect.

If tool_search confirms a surface genuinely lacks local tools (e.g. running on an unauthenticated mobile session), say so and ask user to either switch to Claude Desktop or paste a recon block via Cursor.

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

## END OF SESSION PROTOCOL

Before chat gets too long (and Claude starts compressing context):

1. **Summarize what shipped** — commits + descriptions
2. **Note any uncommitted work** AND any side branches created during the session
3. **Update brief if there's meaningful drift** (new features, line refs, decisions)
4. **Update archive** with session entry — IN THE SAME COMMIT as brief changes
5. **Update DECISIONS.md** if any ADR-worthy calls happened
6. **Update KICKOFF (this doc) if workflow changed** — same commit
7. **Commit + push to origin/main**
8. **Tell user what to upload to project knowledge folder** (BRIEF, ARCHIVE, DECISIONS, KICKOFF if changed)
9. **Suggest stopping point** — don't push past their energy

---

## HANDOFF PROTOCOL — CHAT-TO-CHAT

The transition between chats is now formalized:

1. **End of chat A:** I commit + push doc updates to `origin/main`
2. **User uploads** updated MD files to the Quantum Cube project knowledge folder in claude.ai (replaces existing). Files to upload when changed:
   - `PROJECT_BRIEF.md`
   - `BRIEF_ARCHIVE.md`
   - `DECISIONS.md`
   - `CHAT_KICKOFF.md` (this file, only when itself changed)
3. **User starts new chat** in the Quantum Cube project
4. **New Chat Claude reads project knowledge automatically** at startup
5. **First message can be casual** — "ready, run health check" — Chat Claude follows First Message Protocol above

**The project-knowledge upload is the only manual step.** No MCP yet exists for Chat Claude to write to its own project knowledge folder. Until that ships, the user crosses that air-gap.

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
