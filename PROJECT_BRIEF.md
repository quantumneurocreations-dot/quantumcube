# QUANTUM CUBE — MASTER PROJECT DOCUMENT
**Version: v20 | Last Updated: April 22, 2026 (Wednesday, morning)**

---

## ⚠️ CRITICAL RULE — ALWAYS READ FIRST
**Quantum Cube and QNC Academy are COMPLETELY SEPARATE projects — at the backend/tooling/profile level.**
- Never mix backend code, Supabase projects, API keys, or tool configs between them
- Quantum Cube has its own Supabase project (Frankfurt) — never touch the Academy one (Ireland)
- Quantum Cube has its own ElevenLabs API key — never share or cross-use

**Asset sharing is fine when explicit.** Music/audio files copies across projects permitted when Ronnie approves. The rule targets backend cross-contamination, not file assets.

### 🚫 NOT Quantum Cube's job — do not touch from a Cube chat
- The Academy website (Next.js codebase at `/Users/qnc/Projects/qnc-academy/`)
- The Quantum Integrator (QI) — Academy's branded AI
- HeyGen cleanup (Academy's own cleanup task)
- Academy's Vercel deployment
- The Academy Supabase project (Ireland)
- Any `.env.local`, config, or secret from the Academy side

If a Cube chat drifts into Academy territory, stop and ask.

---

## 🚦 NEW CHAT? READ CHAT_KICKOFF.md FIRST
The kickoff doc handles session startup, role split between Chat Claude and Cursor Claude, and the golden rules. Read it first, then read this brief for project-specific context.

---

## ⚠️ OPEN ISSUE AT START OF NEXT SESSION — NARRATION PIPELINE NOT VERIFIED

**Status: pipeline shipped but NOT verified working on Ronnie's phone.**

What's live on `origin/main` as of commit `1381917`:
- 256 MP3s committed at `Sounds/Narration/` (phase 1 numerology + welcome)
- `narration-manifest.json` committed (256 entries with sha256 drift hashes)
- `scripts/extract-narration.mjs` extractor
- `scripts/generate-narration.mjs` generator (not committed/pushed, lives locally only as `d3451f7` unpushed)
- Frontend rewire: `fetchNarration` tries local MP3 first via sha256 lookup, falls back to live Edge Function TTS
- Fixes applied: `innerText` (not `textContent`), `normText` normalizer for dynamic Personal Year, bd/kl label fixes
- SW currently: `qc-v122`

**The problem:**
- Valory plays fine when network is ON (either local MP3 or live TTS fallback — can't tell which from ear alone)
- On airplane mode: SILENT. Which means local MP3 path is NOT serving.
- Debug overlay showed `manifest size=0` on every card tap from Ronnie's phone — manifest is not loading into memory on his device
- Cursor's Browser MCP diagnostic (from a fresh desktop Chrome session) showed the pipeline works there
- Multiple nocache URL attempts, full "All time" Chrome cache wipe, no cookies/site data — none of it fixed it on Ronnie's phone

**Hypotheses (not tested):**
1. Some Chrome mobile setting persists across data wipes (service worker registrations, background fetch permissions)
2. Regular Chrome on Android is actually being hijacked by the installed PWA context
3. Real bug in `_loadNarrationManifest` that only surfaces on Android Chrome (not desktop)
4. GitHub Pages serving manifest with CORS/MIME that Android Chrome rejects

**Next session MUST resolve this before touching anything else narration-related.** Start by:
1. Uninstall the Quantum Cube PWA completely from the phone
2. Reinstall only after testing pure browser access first
3. If that fails, set up USB remote debugging (Chrome on Mac → USB → Chrome on phone → real DevTools console)
4. USB debug reveals the actual failure mode of `_loadNarrationManifest` on Android Chrome
5. Fix whatever it reveals

Do NOT start music/SFX refresh, auth loop fix, or any other work until narration is verified end-to-end on Ronnie's phone with airplane mode ON.

---

## ⚠️ NEW PROCESS RULE — CURSOR SCOPE CREEP

**April 22 morning: Cursor Claude made an unauthorized commit (`c5e61bd`) without approval from Chat Claude or Ronnie.** He made extractor label changes (bd, kl), added a `normText` normalizer for Personal Year, regenerated the manifest, bumped SW — all without being asked. The changes happened to be correct (fixed real bugs), but the process broke.

**Rule going forward: Cursor Claude does NOT make substantive edits beyond what Chat Claude's paste block explicitly asks for.** Self-correcting verbatim paste anchors (indentation, quote escaping) is welcomed. Fixing different bugs, adding normalizers, regenerating data files, bumping SW versions beyond what was requested — NOT permitted without an explicit ask. If Cursor thinks additional work is needed, he surfaces it in his output so Ronnie and Chat Claude can decide, and waits.

Add to CHAT_KICKOFF.md next update.

---

## 🔬 DIAGNOSTIC-FIRST DISCIPLINE

**Before any patch, always do these three first. No exceptions.**

```bash
git status                          # what's dirty, what branch
git log --oneline -10               # recent history, what's the rollback anchor
grep -n "<symptom>" <likely-file>   # locate, don't guess
```

**Rules of engagement:**
- Never patch blind. If you can't point to the line/function causing the problem, you don't understand it yet.
- Never iterate Python scripts to fix HTML — one-shot only (single read-replace-write, no loops). If it fails, break into smaller `str_replace` edits instead.
- Never assume Cursor Claude got the indentation or quote-escaping right in your first anchor. Expect and welcome self-correction on verbatim output.
- When adding diagnostics, use a temporary on-screen `#qcDebug` overlay + `window.qcLog()` — always remove in the next commit after the fix lands.

**When "it's not working on my phone" — triage order, in this exact order:**
1. Regular Chrome tab (not PWA) at the GitHub Pages URL. If it works there → it's cache, not code.
2. Uninstall + reinstall the PWA
3. Clear Chrome "All time" browsing data
4. USB remote debugging Chrome → phone (actual console access)
5. Only then consider a code change

**Never burn a diagnostic commit on what's just PWA cache stickiness.**

---

## 👤 BUILDER CONTEXT

**Ronnie:**
- First-time developer, ~2.5 weeks into real building
- Mobile-primary: Android Chrome + PWA on phone, Mac mini M4 for dev + Cursor
- AI-directed workflow: 100% code by AI (Claude chat + Claude Cursor agent)
- Contributes: product vision, UX taste, bug catching, QA, project management, team comms
- Marathon-capable but energy-aware pacing matters

**How help should work:**
- Bias toward **verification over assumption** — grep/read before edit, expected-state checks after edit
- **Pace matches energy level** — short confirmable steps when tired, bigger moves when fresh
- **Prefer concise + confirmable changes** over large blind rewrites
- **Respect locked decisions** — do not relitigate

**Avoid:**
- Over-recommending tools or subscriptions speculatively
- Emotional-whiplash audits right after breakthrough moments
- Assuming code literacy — explain the "why" in plain terms
- Silent rewrites of user paste blocks or Cursor scope creep (see rule above)

---

## 👥 TEAM CADENCE

- **Ronnie** — daily driver, all hands-on building
- **Michelle** — admin/support. Needs clear asks, not open-ended. Paddle requirements email ready — she has the M1 company + bank details now.
- **Keyzer** — marketing + finance + payments. On-demand.
- **Team decisions locked when agreed, not relitigated.**

**Currently locked team decisions:**
- Pre-recorded TTS strategy (full pre-record for static content, Face 5 stays live)
- HeyGen avatar approach deprecated for Academy
- $17 USD payment point
- Paddle replaces PayFast globally (Merchant of Record)
- Faceless brand — public contacts admin@qncacademy.com + info@qncacademy.com
- Narrator UX = Option 3 (auto-read on category open, Voice button = mute/stop only)
- **Launch is not time-pressured** — ship when quality is right
- **Music + SFX refresh** — team wants fresh tracks and new SFX before launch (scoped, not started)

---

## 🎯 APRIL 21-22 SESSION SUMMARY

### Shipped (commits on origin/main)
- Accessibility: `user-scalable=no` removed, 7 form labels linked → qc-v115, qc-v116
- Narration scripts scaffolded: `ee32f06`
- Extractor with sha256 drift hashes: `908d495`
- 256 MP3s committed + served from repo: `f7854ee`
- Frontend rewire for local MP3s with live fallback: `cd64914`
- `innerText` fix for hash matching: `2b420d0`
- bd/kl label fixes + normText py normalizer + manifest regen: `c5e61bd` (unauthorized but correct)
- Final debug revert: `1381917`

### ElevenLabs infrastructure
- Usage-based billing enabled on Creator plan ($22/mo base)
- Cap: 250k credits (~$75 max overage ceiling)
- Turbo v2.5 model (0.5 credits/char)
- Budget for phase 1 batch: ~$16 + tax
- `.supabase-env` backed up to `~/Documents/qnc-secrets-backup/`

### Unresolved
- **Narration NOT verified on phone** (see "Open Issue" above)
- `scripts/generate-narration.mjs` committed locally as `d3451f7` but NOT pushed to origin
- Login loop: signing out + back in same session re-fires magic link (known issue, post-launch polish)

---

## 🎵 MUSIC + SFX REFRESH — PLANNED NEXT PROJECT

Ronnie requested full music + SFX refresh. Not started. Scope to define before execution:

**Music:**
- Current: 5 Academy ambient tracks rotating
- Source: Epidemic Sound subscription
- Ronnie wants different tracks — taste decision, needs sourcing session

**SFX:**
- Current: 8 files in `Sounds/` (reveal_my_cube, select_side, reveal_result, back_to_signup, payment, touch_cube, plus 2 others)
- Ronnie wants to change these — source TBD (Epidemic Sound SFX? Custom?)

**Execution path (when narration verified and cleared):**
1. Source new tracks + SFX in a dedicated session (with Keyzer input recommended)
2. Drop into `Sounds/Music/` and `Sounds/`
3. Update `QC_AUDIO` references
4. SW bump, commit
5. Test playback order + volume balance on phone

Not launch-blocking if narration stays on current tracks temporarily.

---

## 🧭 CANONICAL SAFE ROLLBACK POINTS

**Do not revert past these commits without a conscious decision.**

| Commit | Why you don't revert past it |
|---|---|
| `1381917` | Clean narration state — debug removed, innerText + normText + labels + MP3 wiring intact |
| `c5e61bd` | Label fixes bd/kl + normText normalizer — reverting re-breaks Birthday and Karmic Lessons cards |
| `2b420d0` | innerText fix — reverting breaks ALL numerology sha256 matching |
| `cd64914` | Frontend rewire for local MP3s — reverting removes the whole local-first pipeline |
| `f7854ee` | 256 MP3s committed — reverting removes the MP3s from repo |
| `908d495` | Extractor + manifest with sha256 — reverting loses manifest |
| `e1070fb` | Cursor hardening + .cursorrules |
| `94af122` | Legal additions — required for launch defensibility |
| `2403ca7` | Paywall fix #2 |
| `fd41b68` | Paywall fix #1 |
| `57dd972` | 10.8MB base64 cleanup |

---

## ✅ PAYWALL VERIFICATION PROTOCOL

(Unchanged from v19 — see previous brief for full protocol. Still holds. Key rows to remember: `quantumneurocreations@gmail.com` has_paid=true, `carlkelbrick@gmail.com` has_paid=false, use regular Chrome with DevTools, verify STORE_KEY scoped to user.id not "1".)

---

## 🏁 DEFINITION OF DONE — LAUNCH GATE

**All must be true before charging a single real user:**

- [ ] **Narration pipeline verified end-to-end on Ronnie's phone** — airplane mode test passes (NEW, blocking)
- [ ] **Music + SFX refresh complete** — team has signed off (NEW, locked decision)
- [ ] **Paywall verified both directions** — paid unlocks, unpaid stays locked, sign-out re-locks, same-device different-user doesn't inherit unlock
- [ ] **Paddle E2E** — signup → verify → checkout → webhook → `has_paid=true` → unlock persists
- [ ] **All test profile rows deleted** from Supabase `public.profiles`
- [ ] **Rate-limit narrate Edge Function** per-IP (deferred from earlier sessions, still required)
- [ ] **Legal copy final** — entertainment opener, Original Works clause, AI-Assisted disclosure (commit 94af122 present)
- [ ] **SW version bumped + force-cache-tested** on Ronnie's phone
- [ ] **quantumcube.app domain pointed to GitHub Pages** with HTTPS verified
- [ ] **Zero PayFast references** remaining after Paddle swap
- [ ] **Resend deliverability tested** to fresh Gmail, Outlook, Yahoo

---

## 💰 SUBSCRIPTION AUDIT — OUTCOMES
(Unchanged from v19)

---

## 📜 CONTENT LICENSING — RESOLVED
(Unchanged from v19)

---

## DEV ENVIRONMENT (M4 Mac Mini)
(Unchanged from v19)

---

## TECH STACK (LOCKED)
- Frontend: Single HTML file, vanilla JS, CSS3, glassmorphism. ~356KB post-cleanup.
- Fonts: Cinzel Decorative, Cinzel, Cormorant Garamond
- Auth: Supabase magic-link, SDK v2.45.4 via UMD CDN
- Database: Supabase Postgres (Frankfurt), `public.profiles` with RLS
- Email: Resend via custom SMTP on Supabase
- Payment: PayFast sandbox wired, Paddle swap pending
- Videos: Vimeo Player API
- Audio:
  - Music: 5 ambient tracks (slated for replacement)
  - SFX: 8 files (slated for replacement)
  - Narration: 256 pre-recorded Valory MP3s + live TTS fallback for astro/chinese/Face5
- Haptics: 3× strength
- Hosting: GitHub Pages
- PWA: Web manifest + service worker (cache: **qc-v122**)

---

## 🎙️ ELEVENLABS NARRATOR
- Voice: Valory (`VhxAIIZM8IRmnl5fyeyk`)
- Model: `eleven_turbo_v2_5` (0.5 credits/char)
- Edge Function: `supabase/functions/narrate/index.ts` deployed with `--no-verify-jwt` + inline apikey check
- Pre-record phase 1 complete (numerology + welcome, 256 clips)
- Phase 2 pending: astro/chinese pre-record (requires variations authoring decision first)

---

## 🔁 PAYMENT PROCESSOR — PADDLE (UNBLOCKED)

Michelle has M1 data (company registration, bank details, tax IDs). Ready to send Paddle requirements email when Ronnie wants to initiate.

**Execution queue (post narration verification):**
- Email Michelle Paddle requirements
- Paddle team application
- Paddle webhook Edge Function
- Rewrite `launchPayFast()` → Paddle checkout
- Remove PayFast refs, update legal
- E2E test
- Delete test rows

---

## APP STRUCTURE — 7 FACES + INTERSTITIAL
(Unchanged from v19)

---

## SUPABASE BACKEND
(Unchanged from v19)

---

## FRONTEND WIRING — KEY LINE REFS (April 22 — grep, numbers drift)

| What | Approx line |
|---|---|
| const sb = window.supabase.createClient | ~499 |
| Face 0 div open | ~531 |
| #welcomeBtn | ~613 |
| NARRATE_URL + NARRATION_DIR + MANIFEST_URL | ~1312-1315 |
| _sha256Hex + _loadNarrationManifest | ~1322-1345 |
| fetchNarration (local-MP3 + live fallback) | ~1349 |
| normText py normalizer | ~1353 |
| qcNarrateCard | ~1425 |
| startNarration | ~1400 |
| showFace | ~1510 |
| STORE_KEY + checkStoredUnlock + syncUnlockFromProfile | ~2099-2138 |
| **function runCalculation** | **~2562** |
| renderAllContent | ~2575 |
| numCards render | ~2676 |
| astroCards render | ~2705 |
| SW code string | ~2908 (**qc-v122**) |

---

## 🔐 AUTH + UNLOCK FLOW
(Unchanged from v19 — known issue: sign out + back in same email same device re-fires magic link, post-launch polish)

---

## 🪨 FRAGILE AREAS
(Unchanged from v19 — plus ADD:)
- **Narration pipeline unverified on Android Chrome mobile** — desktop Chrome works, Android shows `manifest size=0` via debug overlay. Cache wipe did not resolve. USB debug required next session.
- **Cursor's unauthorized commits** — see process rule above

---

## WHAT'S LEFT — ORDERED BY PRIORITY

### 🚨 LAUNCH-BLOCKING (current blockers)
1. **Narration verification on Ronnie's phone** — USB debug, identify actual failure, fix, verify
2. **Music + SFX refresh** — team scope + source + integrate
3. **Paddle setup** — Michelle has data, ready to initiate
4. **Rate-limit narrate Edge Function** (~30 min)
5. **Delete test profile rows**
6. **Final paywall E2E test** after Paddle lands

### ⚠️ HIGH-VALUE
7. Accessibility h1/h2 structure (heading tags) — h1/h2 deferred post-launch per earlier decision
8. Static `manifest.json` + `sw.js` — replace blob URLs
9. Sentry error monitoring
10. Astro/Chinese pre-record phase 2

### 🧹 POST-LAUNCH CLEANUP
11. Split HTML into .js + .css files
12. `git gc --aggressive` — clean large .git folder (currently ~1.2GB after MP3 commit)
13. Login loop fix (same-email resign triggers new magic link)
14. HeyGen cleanup (Academy side, not Cube)

---

## INFRASTRUCTURE LIVE
| System | State |
|---|---|
| GitHub Pages | Live (SW **qc-v122**) |
| quantumcube.app | Registered, not yet pointed |
| Resend | Verified |
| ElevenLabs | Usage-based billing enabled, 250k cap |
| Supabase | Frankfurt, RLS verified, narrate deployed |

---

## SESSION LOG

### April 21, 2026 (Tuesday, Mac + Cursor hardening)
See v19 brief.

### April 21-22, 2026 (Tuesday evening → Wednesday morning — narration pipeline + verification struggle)

Started the pre-record TTS pipeline from scratch. Full execution:
- Extractor: reads NUM object from HTML, emits 256-entry manifest with sha256 drift hashes
- Generator: loops manifest, POSTs to narrate Edge Function, saves MP3s to Sounds/Narration/
- Dry-run 15 longest clips — all OK, Valory approved
- Full batch 241 remaining clips — all OK, ~$16 overage on Creator tier
- Frontend rewire: `fetchNarration` tries local MP3 via sha256 lookup, falls back to live Edge Function
- Multiple hash-mismatch debug rounds: textContent→innerText, bd/kl labels, normText for Personal Year
- On-screen debug overlay revealed `manifest size=0` on Ronnie's phone
- Cache wipe did not resolve
- Cursor made one unauthorized substantive commit (c5e61bd) — correct but off-process
- Session ended with pipeline shipped but unverified on mobile

### Lessons learned (running, updated)
- **Cursor Browser MCP diagnosis is not the same as phone diagnosis** — desktop Chrome session worked, Android didn't. Always verify on actual user device.
- **PWA + Chrome cache stickiness can be deeper than "clear all time"** — SW registrations persist, USB debug is the ironclad path.
- **When Cursor produces "evidence it works," check whether the evidence came from his action or from Ronnie's tap** — on the April 22 session, Ronnie manually tapped the card Cursor thought he had tapped.
- **Cursor unprompted commits must stop** — see process rule, update kickoff doc.
- **Chat compression risk is real at multi-hour sessions** — respect stop signals, update brief, start fresh.

---

## NEXT SESSION STARTING POINT

1. Attach PROJECT_BRIEF.md + CHAT_KICKOFF.md to new chat
2. Minimal health check: confirm `1381917` is HEAD on `origin/main`, SW = qc-v122, runCalculation at line ~2562
3. **Priority: narration phone verification via USB debug.** Don't start anything else until this is resolved.
4. Then: music + SFX refresh OR Paddle initiation — Ronnie's call

---

**End of brief v20.**
