# Quantum Cube — context for Claude

This file is auto-loaded by Claude Code, Cursor, and other Claude surfaces opening this repo. It's a **pointer doc** — the substance lives in the docs below.

## Where the rules live

- **`CHAT_KICKOFF.md`** — operating model for chat sessions: mandatory boot sequence, surface boundaries, auto-run discipline, end-of-session protocol. **Read this first on every new chat.**
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
