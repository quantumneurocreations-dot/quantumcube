---
tags: [core, kickoff]
---
# Quantum Cube — context for Claude

This file is auto-loaded by Claude Code, Cursor, and other Claude surfaces opening this repo. It's a **pointer doc** — the substance lives in the docs below.

## Where the rules live

- **`CHAT_KICKOFF.md`** — lean boot doc for Chat Claude (v5 Obsidian-first). Boot sequence only — full rules in `OPERATING_RULES.md`.
- **`OPERATING_RULES.md`** — golden rules, command templates, Cursor fallback, failure recovery, PWA debugging.
- **`PROJECT_BRIEF.md`** — what Quantum Cube is, current state, line refs, decisions.
- **`DECISIONS.md`** — ADR-style decisions. Append when a call is worth preserving.
- **`BRIEF_ARCHIVE.md`** — historical session log. Don't read in full; grep for context.
- **`.cursorrules`** — code style, conventions, safety rules. Authoritative on technical conventions. *Note: refers to `quantum-cube-v10.html` — that's stale, current canonical file is `docs/app.html`.*

## Where the code lives

- **App:** `docs/app.html` (~3.5k lines, vanilla HTML+JS, single page)
- **Service worker:** `docs/sw.js`
- **Edge functions:** `supabase/functions/*/index.ts` (Deno, 6 functions, all `verify_jwt=false` with manual JWT)
- **Migrations:** `supabase/migrations/`
- **Smoke test:** `scripts/smoke.sh` (Mac-only — Cloudflare blocks datacenter IPs)
- **Skills:** `.claude/skills/` — codified workflows. Read the relevant skill before executing the matching task.

## Stack one-liner

Static HTML on GitHub Pages (built from `main:/docs`, custom domain via Cloudflare DNS only — not proxied), Supabase (Postgres + Edge Functions, EU project `fqqdldvnxupzxvvbyvjm`), Sentry (org `quantum-neuro-creations`, project `javascript`, EU), Dodo Payments, ElevenLabs narration, Resend transactional email, PostHog product analytics (EU). No build step. No framework. Single deployable artifact: `docs/`.

## First-time-here checklist

1. Read `CHAT_KICKOFF.md` end to end.
2. Run the boot sequence at the top of that doc.
3. Skim `PROJECT_BRIEF.md` for current state.
4. Read the relevant `.claude/skills/*.md` for the task at hand.
5. Then start work.

## Critical invariants

- `docs/sw.js` cache version (`qc-vNNN`) **must equal** the Sentry release tag in `docs/app.html` (`release: "quantum-cube@qc-vNNN"`). CI catches drift via `.github/workflows/verify-versions.yml`.
- Edge functions all use `verify_jwt=false` with manual JWT validation — never flip this without reading the function's auth flow first.
- `.supabase-env` and any `service_role` key never get committed. Anon key in HTML is expected and public.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- ALWAYS read graphify-out/GRAPH_REPORT.md before reading any source files, running grep/glob searches, or answering codebase questions. The graph is your primary map of the codebase.
- IF graphify-out/wiki/index.md EXISTS, navigate it instead of reading raw files
- For cross-module "how does X relate to Y" questions, prefer `graphify query "<question>"`, `graphify path "<A>" "<B>"`, or `graphify explain "<concept>"` over grep — these traverse the graph's EXTRACTED + INFERRED edges instead of scanning files
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
