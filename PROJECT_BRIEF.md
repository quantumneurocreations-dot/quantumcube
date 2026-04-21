# QUANTUM CUBE — MASTER PROJECT DOCUMENT
**Version: v19 | Last Updated: April 21, 2026 (Tuesday)**

---

## ⚠️ CRITICAL RULE — ALWAYS READ FIRST
**Quantum Cube and QNC Academy are COMPLETELY SEPARATE projects — at the backend/tooling/profile level.**
- Never mix backend code, Supabase projects, API keys, or tool configs between them
- Quantum Cube has its own Supabase project (Frankfurt) — never touch the Academy one (Ireland)
- Quantum Cube has its own ElevenLabs API key — never share or cross-use

**Asset sharing is fine when explicit.** Copying music/audio files across projects is permitted when the user approves. The rule targets backend cross-contamination, not file assets.

### 🚫 NOT Quantum Cube's job — do not touch from a Cube chat
- The Academy website (Next.js codebase at `/Users/qnc/Projects/qnc-academy/`)
- The Quantum Integrator (QI) — Academy's branded AI built on Claude Haiku 4.5
- HeyGen cleanup (Academy's own cleanup task — `StreamingAvatar.tsx`, heygen routes, package.json deps)
- Academy's Vercel deployment investigation
- The Academy Supabase project (Ireland, ref `bevaepokvavzmykjmhda`)
- Any `.env.local`, config, or secret from the Academy side

If a Cube chat drifts into any of the above, stop and ask.

---

## 🚦 NEW CHAT? READ CHAT_KICKOFF.md FIRST
The kickoff doc handles session startup, role split between Chat Claude and Cursor Claude, and the golden rules. Read it first, then read this brief for project-specific context.

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
2. Force-stop the PWA (long-press icon → App info → Force stop + Clear storage)
3. Uninstall + reinstall the PWA
4. **Only then** consider a code change

**Never burn a diagnostic commit on what's just PWA cache stickiness.**

---

## 👤 BUILDER CONTEXT

**Ronnie:**
- First-time developer. ~2 weeks into real building, no prior programming/coding/design experience.
- Mobile-primary: testing on phone (Android Chrome + PWA). Mac mini M4 for dev + Cursor.
- AI-directed workflow: 100% of code written by AI (Claude via chat + Claude via Cursor agent).
- Ronnie contributes: product vision, UX taste, bug catching, project management, team comms, all architecture and feature decisions.
- Marathon sessions are common. Energy-aware pacing matters.

**How help should work:**
- Bias toward **verification over assumption** — grep/read before edit, expected-state checks after edit
- **Pace matches energy level** — short confirmable steps when tired, bigger moves when fresh
- **Prefer concise + confirmable changes** over large blind rewrites
- **Respect locked decisions** — do not relitigate (see Team Cadence section)

**Avoid:**
- Over-recommending tools or subscriptions speculatively
- Emotional-whiplash audits right after breakthrough moments
- Assuming code literacy — explain the "why" in plain terms, not just the "what"
- Silent rewrites of the user's paste blocks (self-corrections OK, silent scope creep not OK)

---

## 👥 TEAM CADENCE

- **Ronnie** — daily driver, all hands-on building. Every decision routes through here.
- **Michelle** — admin/support. Works async. **Needs clear asks, not open-ended.** Paddle requirements email will be one such ask.
- **Keyzer** — marketing + finance + payments. On-demand and strategic check-ins. Not daily.
- **Team decisions are made together and then LOCKED.** Once locked, Claude should not relitigate or re-open.

**Currently locked team decisions (do not re-open unprompted):**
- Pre-recorded TTS strategy (full pre-record, not hybrid) — see ElevenLabs Narrator section
- HeyGen avatar approach deprecated for Academy — sine wave visualization instead
- $17 USD payment point (numerology: 1+7 = 8, wealth number)
- Paddle replaces PayFast globally (Merchant of Record for VAT/GST)
- Faceless brand — public contacts only `admin@qncacademy.com` and `info@qncacademy.com`
- Narrator UX = Option 3 (auto-read on category open; Voice button = mute/stop only)

---

## TEAM
- **Ronnie** — creator, design, programming, tech lead
- **Michelle** — admin/support
- **Keyzer** — marketing & finance, payments
- Equal 3-way partnership
- Faceless brand: public only sees `admin@qncacademy.com` and `info@qncacademy.com`

---

## FILE LOCATIONS
```
/Users/qnc/Projects/quantumcube/              <- MAIN PROJECT FOLDER
|- quantum-cube-v10.html                      <- THE APP (~356 KB post-cleanup, ~2900 lines)
|- PROJECT_BRIEF.md                           <- This document
|- CHAT_KICKOFF.md                            <- Chat operating protocol
|- cube-background.jpg                        <- Milky Way background (in repo)
|- .supabase-env                              <- Supabase + Resend creds (gitignored)
|- .cursorrules                               <- Cursor project rules (committed e1070fb)
|- .cursorignore                              <- REMOVED (commit e1070fb, April 21) — main HTML now fully indexable by Cursor
|- .gitignore                                 <- Committed; covers node_modules, .DS_Store, and *.html.bak-*
|- supabase/                                  <- Supabase CLI linked project
|   |- config.toml                            <- function-level flags (narrate verify_jwt=false)
|   \- functions/narrate/index.ts             <- ElevenLabs proxy Edge Function (38 lines — see inline source below)
|- Sounds/                                    <- SFX audio assets (committed)
|   \- Music/                                 <- 5 Academy ambient tracks (force-added despite Music/ in .gitignore)
```

**GitHub Repo:** https://github.com/quantumneurocreations-dot/quantumcube
**Live URL:** https://quantumneurocreations-dot.github.io/quantumcube/quantum-cube-v10.html
**Custom domain (registered, not yet pointed):** https://quantumcube.app

---

## 🎯 APRIL 20 HEADLINE WINS

Six shippable outcomes from Monday:

1. **10.8 MB removed from HTML** (57dd972) — legacy base64 AUDIO object gone. File: 11.2MB → 346KB. 97% reduction.
2. **Paywall bypass fixed** (fd41b68 + 2403ca7) — two separate bugs, both patched. Verified holding.
3. **Three independent audits completed** — internal (Claude fresh chat), external (Claude in Chrome), security (RLS verification). Honest, actionable, no hype.
4. **Subscription audit** — identified trims and saves before scaling further.
5. **Pre-recorded TTS strategy locked** — team decision made, execution plan documented.
6. **Legal additions** (94af122) — three phrases added to cover entertainment, original-works synthesis, and AI disclosure. Content licensing concern resolved.

## 🔧 APRIL 21 FOLLOW-UP

- Mac + Cursor hardening pass (see Dev Environment section)
- `.cursorignore` removed → HTML now indexable by Cursor (str_replace works directly — old shell-sed workaround no longer needed)
- `.cursorrules` created at repo root
- Cursor yoloCommandAllowlist tightened (bash -c + git push removed)
- FileVault enabled
- Backup files cleaned from repo, `.gitignore` updated

---

## 🧭 CANONICAL SAFE ROLLBACK POINTS

**Do not revert past these commits without a conscious decision — each one contains essential state.**

| Commit | Why you don't revert past it |
|---|---|
| `e1070fb` | Cursor hardening — lose `.cursorrules` + allowlist tightening + gitignore update |
| `94af122` | Legal additions — entertainment opener, Original Works, AI-Assisted disclosure. Required for launch defensibility. |
| `2403ca7` | **Paywall fix #2** — unconditional lock enforcement. Reverting = paywall bypass returns. |
| `fd41b68` | **Paywall fix #1** — STORE_KEY user-scoped. Reverting = shared-device unlock inheritance. |
| `57dd972` | 10.8MB cleanup — reverting blows file back up to 11MB. |

When in doubt, `git revert <commit>` a specific bad change rather than resetting through these anchors.

---

## ✅ PAYWALL VERIFICATION PROTOCOL

**How to test paid + unpaid in one session without cross-contamination.**

### Setup
- Two test profiles in `public.profiles`:
  - `quantumneurocreations@gmail.com` — `has_paid=true`
  - `carlkelbrick@gmail.com` — `has_paid=false`
- Use **regular Chrome** (not PWA) with **DevTools open** for storage inspection

### Test sequence

**1. Clean start:**
- Chrome DevTools → Application → Storage → Clear site data (full wipe)
- Hard-refresh

**2. Unpaid test — carlkelbrick:**
- Fill form → submit → verify magic link → land in app
- Navigate Face 3 → **expected: Lock card "Complete Quantum Cube Unlock" with $17 button, NO numerology content visible**
- DevTools → Application → Local Storage → verify:
  - `STORE_KEY` = absent OR cleared (NOT "1", NOT a user id)
  - `qc_pending_profile_v1` = contains form data
- Face 4, 5, 6 → same lock card behavior

**3. Switch to paid — quantumneurocreations:**
- Sign Out (Face 7 button) — clears Supabase session
- Manually clear `STORE_KEY` in DevTools (belt-and-braces)
- Fill form with different email → verify magic link → land in app
- Navigate Face 3 → **expected: full numerology content, no lock card, Valory narrates category taps**
- DevTools → Local Storage → verify:
  - `STORE_KEY` = current session.user.id (a UUID, NOT "1")

**4. Tab close + reopen (paid):**
- Close tab. Wait 10s. Reopen live URL.
- Expected: auto-advances into app, still unlocked, no magic-link re-verify

**5. Switch back to unpaid (same device):**
- Sign Out
- Fill form with `carlkelbrick@gmail.com`
- **Expected: Lock card appears again. Previous user's unlock does NOT leak.**
- This is the test that failed before fix #1 + fix #2.

### Expected DOM states
| State | `.lock-screen` display | `#face3-content` display | `#lock3` icon | `.cube-face[data-idx=2]` class |
|---|---|---|---|---|
| Unpaid | `block` | `none` | visible | `.locked` |
| Paid | `none` | `block` | hidden | no `.locked` |

### Red flags during testing
- Lock card visible but content also visible behind it → z-index bug, different issue
- Lock card absent for unpaid user → `syncUnlockFromProfile` unpaid branch didn't fire
- Paid user sees lock card → `applyUnlockedState` not running, or `has_paid` read wrong from DB

---

## 🏁 DEFINITION OF DONE — LAUNCH GATE

**All must be true before charging a single real user:**

- [ ] **Paywall verified both directions** — paid unlocks, unpaid stays locked, sign-out re-locks, same-device different-user doesn't inherit unlock
- [ ] **Paddle E2E** — signup → verify → Paddle checkout → webhook → `has_paid=true` in DB → unlock persists across session + reload
- [ ] **All test profile rows deleted** from Supabase `public.profiles` (5 listed in backend section)
- [ ] **Accessibility trio shipped** — remove `user-scalable=no`, add `<h1>` + `<h2>` structure, add `<label>` to all 12 form inputs
- [ ] **narrate Edge Function rate-limited** per-IP (Deno KV or simple in-memory cap) to prevent apikey abuse from DevTools scraping
- [ ] **Legal copy final** — entertainment opener, Original Works clause, AI-Assisted disclosure all present (check commit 94af122 is in HEAD)
- [ ] **SW version bumped + force-cache-tested** on Ronnie's phone (regular Chrome + PWA both verified)
- [ ] **quantumcube.app domain pointed to GitHub Pages** with HTTPS verified
- [ ] **Zero PayFast references** remaining in code, legal copy, or Edge Functions after Paddle swap
- [ ] **Resend deliverability tested** to fresh Gmail, Outlook, Yahoo accounts

Not required but strongly recommended:
- [ ] Sentry error monitoring wired
- [ ] At least 5 smoke tests against live site

---

## 💰 SUBSCRIPTION AUDIT — OUTCOMES

### ✅ Keep as-is
| Service | Purpose | Status |
|---|---|---|
| Claude Max | Building both Cube + Academy | Keep |
| Claude Console (API) | **Necessary** — Academy's QI uses Claude Haiku 4.5 via `api.anthropic.com/v1/messages` from `src/app/api/avatar-chat/route.ts` | Keep — confirmed by Cursor recon |
| Cursor Pro | Code editor with Claude agent | Keep |
| Epidemic Sound | Music licensing (5 Cube tracks + future Academy) | Keep |
| CapCut Pro | Video production | Keep |
| ElevenLabs Creator | TTS for Cube narration + Academy QI voice | Keep (downgrade after Cube pre-record migration; Academy keeps live) |
| Google Workspace | Email infrastructure | Keep |
| GitHub | Code hosting, Pages hosting | Verify free tier (likely fine) |

### ⬇️ Downgrade / switch
| Service | Action | Savings |
|---|---|---|
| Vercel Pro | Downgrade to Hobby until Academy goes live + monetizes | ~$20/month |
| Vimeo Starter | Switch from monthly to annual billing | ~$65/year |

### ❌ Confirmed deprecated
- **HeyGen** — subscription already canceled. Academy codebase cleanup pending (not a Cube task).

### 🧠 About the Quantum Integrator (QI) — Academy only, not Cube
- Brain: Claude Haiku 4.5 via Anthropic Messages API
- Voice: ElevenLabs TTS (female + male voice IDs)
- Visualization: Sine wave (previously planned avatar via HeyGen — deprecated)

---

## 📜 CONTENT LICENSING — RESOLVED

### Verified outcome
- Numerology, astrology, Chinese zodiac **concepts** are public domain
- **Written interpretations are original expression** — voice inspection confirms distinctive phrasing, narrative framing, 3 genuine rotation variations per number
- Legal coverage already strong (6 legal tabs)

### Three additions shipped April 20 (commit 94af122)
1. Disclaimer opener: "All interpretations, narrations, and reading content provided in Quantum Cube are for entertainment and self-reflection purposes only."
2. IP tab — Original Works & Synthesized Expression: public domain traditions + original works by Quantum Neuro Creations
3. IP tab — AI-Assisted Content & Voice Narration: discloses AI-assisted writing + ElevenLabs TTS under editorial control

**Verdict: content licensing is NOT a launch-blocker.**

### Third-party attributions already in IP tab
- Epidemic Sound (licensed subscription)
- Google Fonts (SIL OFL — Cinzel, Cinzel Decorative, Cormorant Garamond)
- PayFast (will swap to Paddle reference post-integration)

---

## 📊 AUDIT FINDINGS — APRIL 20

Three independent audits completed. Summary:

### Internal evidence audit (fresh Claude chat)
Calibrated to "2-weeks-in, non-developer, self-taught, AI-directed" baseline.
- 11MB HTML → **fixed (97% reduction)**
- 327 commits in 5 days git, ~2 weeks real timeline → heavy iteration, normal for AI-loop dev
- Claude writes 100% of code; Ronnie contributes product/UX/QA/direction
- Right calls: server-side ElevenLabs key, RLS with immutable has_paid, Frankfurt region
- Comparison: freelancer 80–160 billable hours ($5k–$19k). Small agency $20k–$50k. "Team of 6 / 6 months" hero numbers are false — don't repeat them.

### External browser audit (Claude in Chrome)
Pre-cleanup: 7.9MB gzipped, ~5s load. **Post-cleanup: ~350KB gzipped.**
- No trackers, HTTPS + HSTS, no console errors
- Accessibility fails: `user-scalable=no`, 0 heading structure, 12 unlabeled inputs
- PWA registration via blob URLs (non-standard but working)

### Security audit (RLS verified)
- `profiles`: rowsecurity=true ✅
- SELECT + UPDATE: `auth.uid() = id`, has_paid locked
- INSERT: with_check enforced
- Anon key is safe sb_publishable_. Service role never in HTML. ElevenLabs key only as Supabase secret.

---

## DEV ENVIRONMENT (M4 Mac Mini)

### Hardware + OS
| Item | Detail |
|------|--------|
| Machine | Mac Mini M4 |
| Username | qnc |
| FileVault | **ON (enabled April 21, 2026)** |
| Terminal arch | arm64 (native, not Rosetta) |
| Homebrew prefix | /opt/homebrew (native ARM) |

### Native ARM64 dev tools — verified April 20
| Tool | Version / Notes |
|---|---|
| Node.js | v24.15.0 native ARM via nvm |
| Python | 3.9.6 universal2 (Apple native) |
| git | universal2 (Apple native) |
| gh | v2.89.0 native ARM |
| Supabase CLI | v2.90.0 native ARM |
| cwebp | v1.6.0 native ARM |
| Vercel CLI | v51.5.0 (node script on native node) |

### Cursor setup (current as of April 21)
| Setting | Value |
|---|---|
| Default Composer model | claude-4.5-sonnet |
| Privacy Mode | ON (`PRIVACY_MODE_NO_TRAINING`) |
| settings.json location | on disk at `~/Library/Application Support/Cursor/User/settings.json` (not DB only) |
| `yoloCommandAllowlist` | 40 entries — `bash -c` and `git push` removed |
| `diffTabDefaultAction` | `commit` (was `commitAndPush`) |
| `autoApplyFilesOutsideContext` | false |
| `autoAcceptWebSearchTool` | false (`isWebSearchToolEnabled: true`) |
| `.cursorrules` | tracked at repo root, committed e1070fb |
| `.cursorignore` | **DELETED** — `quantum-cube-v10.html` is now fully indexable by Cursor. `str_replace` works directly. (Pre–April 21 note: file was `.cursorignore`-blocked, required shell-sed/Python workaround. That workaround is OBSOLETE.) |

### Outstanding environment task
Ronnie has important files on M1 that need migrating to M4 — including email client setup for admin@qncacademy.com, required before sending Michelle the Paddle requirements list.

---

## TECH STACK (LOCKED)
- **Frontend:** Single HTML file, vanilla JavaScript, CSS3 3D transforms, glassmorphism. **File size: 356 KB** (down from 11.2 MB)
- **Fonts:** Cinzel Decorative (logo), Cinzel (labels/UI), Cormorant Garamond (body text)
- **Auth:** Supabase magic-link (email OTP), SDK v2.45.4 via UMD CDN
- **Database:** Supabase Postgres (Frankfurt) — `public.profiles` with RLS
- **Email:** Resend via custom SMTP on Supabase (3000/month, 100/day)
- **Payment:** PayFast sandbox currently wired — Paddle swap pending (ON PAUSE)
- **Videos:** Vimeo Player API — native real fullscreen only
- **Audio:**
  - **Music:** 5 Academy ambient tracks in Sounds/Music/, QC_AUDIO rotation
  - **SFX:** 8 files in Sounds/ (Touch Cube 2 removed Apr 20)
  - **Narration:** ElevenLabs Valory voice via Supabase Edge Function (Deno runtime)
- **Haptics:** 3× strength (75ms / 120ms / [90,240,90])
- **Hosting:** GitHub Pages
- **PWA:** Web manifest + service worker (cache: **qc-v114**)

---

## 🎙️ ELEVENLABS NARRATOR

### Architecture (shipped April 19)
- **Voice:** Valory (voice ID `VhxAIIZM8IRmnl5fyeyk`)
- **Model:** `eleven_turbo_v2_5` with `{stability:0.5, similarity_boost:0.75, speed:1.15}`
- **Key storage:** `ELEVENLABS_API_KEY` as Supabase secret only (never in HTML)
- **Edge Function:** `supabase/functions/narrate/index.ts`, deployed with `--no-verify-jwt` + inline apikey-header check
- **config.toml:** `[functions.narrate] verify_jwt = false`

### Edge Function source (for reference, not the active doc)

```typescript
import { serve } from "https://deno.land/std@0.192.0/http/server.ts";

const KEY = Deno.env.get("ELEVENLABS_API_KEY")!;
const EXPECTED_APIKEY = Deno.env.get("SUPABASE_ANON_KEY")!;
const MODEL = "eleven_turbo_v2_5";
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return new Response("Method not allowed", { status: 405, headers: CORS });

  const apikey = req.headers.get("apikey") || req.headers.get("authorization")?.replace(/^Bearer\s+/i, "");
  if (!apikey || apikey !== EXPECTED_APIKEY) {
    return new Response(JSON.stringify({error:"unauthorized"}), { status: 401, headers: {...CORS,"Content-Type":"application/json"} });
  }

  try {
    const { text, voice_id } = await req.json();
    if (!text || !voice_id) return new Response(JSON.stringify({error:"missing text or voice_id"}), { status: 400, headers: {...CORS,"Content-Type":"application/json"} });
    if (text.length > 2500) return new Response(JSON.stringify({error:"text too long"}), { status: 400, headers: {...CORS,"Content-Type":"application/json"} });
    const r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voice_id}`, {
      method: "POST",
      headers: { "xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg" },
      body: JSON.stringify({ text, model_id: MODEL, voice_settings: { stability: 0.5, similarity_boost: 0.75, speed: 1.15 } }),
    });
    if (!r.ok) {
      const err = await r.text();
      return new Response(JSON.stringify({error:"elevenlabs failed",detail:err}), { status: r.status, headers: {...CORS,"Content-Type":"application/json"} });
    }
    return new Response(r.body, { status: 200, headers: {...CORS,"Content-Type":"audio/mpeg"} });
  } catch (e) {
    return new Response(JSON.stringify({error:String(e)}), { status: 500, headers: {...CORS,"Content-Type":"application/json"} });
  }
});
```

**Gap flagged for launch:** no rate limiting. Anyone who scrapes the apikey header from DevTools can burn ElevenLabs credits. Fix: per-IP rate limit in Deno KV or simple in-memory token bucket. ~30 min work.

### Frontend UX — Option 3 (auto-read on open)
Voice defaults ON, Voice button = mute/stop only.
- Face 1: "▶ Welcome" button (once-per-user localStorage `qc_greeted`) — Valory greets on tap
- Faces 3/4: Tap category → opens AND narrates. Voice toggles future narration.
- Face 5: Auto-narrates on entry ~500ms, token-gated + visibility-checked

### 🔒 LOCKED DECISION — Pre-recorded TTS strategy
**Team aligned April 20: pre-record all narration one-time instead of live per-tap.**

**Execution (after Paddle ships + copy freeze):**
1. Upgrade ElevenLabs to Pro ($99 one month) → 500k credits
2. Generate all ~500–550 MP3s via script calling Edge Function in a loop
3. File structure: `Sounds/Narration/num_lifepath_7_v1.mp3`, etc.
4. Frontend rewired: filename-lookup → play local MP3 → Edge Function as fallback
5. Downgrade back to Creator ($22/mo)
6. **Total upfront: ~$99. Ongoing: $0 forever.**

**Scope:**
- Welcome greeting: 1 file
- Numerology: 9 categories × ~10 numbers × 3 variations = ~270 files
- Western Astrology: 5 categories × 12 signs = 60 files
- Chinese Horoscope: 5 categories × 12 animals = 60 files
- Combined Face 5: chunk-and-stitch ~225 files (openers × 3, fixed paras, 144 Western×Chinese combos, transitions, closers)

**Benefits:** instant playback, offline via PWA cache, consistent quality, no API failure risk, no rate-limit risk.
**Trade-off:** copy lock-in. Accept since content is stable post-launch.

---

## 🔊 AUDIO SYSTEM — QC_AUDIO
Music: 5-track rotation, 0.20 vol, first-tap auto-start, fades, Vimeo pause-on-play.
SFX: 0.30 vol, wired to 6 triggers (reveal_my_cube, select_side, reveal_result, back_to_signup, payment, touch_cube).
Haptics: 3× strength.

---

## 🔁 PAYMENT PROCESSOR — PADDLE (ON PAUSE)

**Blocker:** Ronnie needs M1 powered on to retrieve company registration numbers, business entity details, bank account info, tax IDs. Plus needs email setup on M4 to send Michelle the Paddle requirements list.

**Once unblocked:**
- Email Michelle Paddle requirements
- Paddle team application
- Paddle webhook Edge Function (server-side `has_paid` flip)
- Rewrite `launchPayFast()` → Paddle checkout
- Remove PayFast refs
- Update legal docs (remove PayFast, update IP tab third-party credits to Paddle)
- E2E test: signup → verify → Paddle → webhook → `has_paid=true` → unlock persists
- Delete test rows from profiles

---

## 📧 EMAIL INFRASTRUCTURE — Resend

- Resend admin@qncacademy.com, domain quantumcube.app verified
- eu-west-1, free tier 3000/mo, 100/day
- DNS: DKIM, SPF, DMARC (p=none), MX send subdomain
- Supabase SMTP: noreply@quantumcube.app, smtp.resend.com:465, 60s min interval

**Flagged UX polish:** resend caps (3/session), duplicate-link dedupe, better throttle messaging.

---

## APP STRUCTURE — 7 FACES + INTERSTITIAL

| Face | Name | Notes |
|------|------|-------|
| Face 0 | Entry / Sign Up Form | |
| faceCheckEmail | "Check Your Email" interstitial | |
| Face 1 | Introduction video + Welcome greeting button | |
| Face 2 | Results Explained videos | |
| Face 3 | Numerology Results | Locked unless paid. Voice. Auto-narrates category taps. |
| Face 4 | Astrology & Horoscope | Locked unless paid. Voice. Auto-narrates category taps. |
| Face 5 | Combined Results | Locked unless paid. Auto-narrates on entry. |
| Face 6 | Complete / Outro video | |
| Face 7 | Settings (Sign Out + Back) | |

---

## SUPABASE BACKEND
- **Project:** quantum-cube (ref `fqqdldvnxupzxvvbyvjm`)
- **Region:** Central EU (Frankfurt)
- **Schema:** `public.profiles` (id, email, has_paid, marketing_consent, created_at)
- **RLS:** Enabled. 3 policies, has_paid locked from client.
- **Edge Functions:** `narrate` deployed. `paddle-webhook` pending.

### Test data in profiles (DELETE BEFORE LAUNCH)
- `quantumneurocreations@gmail.com` — has_paid=true (manually flipped)
- `carlkelbrick@gmail.com` — has_paid=false (paywall testing)
- `rkelbrickmail@gmail.com` — has_paid=false
- `test+chunk5b@qncacademy.com` — has_paid=false
- `carlkelbrick+test@gmail.com` — has_paid=false

---

## FRONTEND WIRING — KEY LINE REFS (April 21 — use grep, numbers drift)

| What | Approx line |
|---|---|
| const sb = window.supabase.createClient | ~499 |
| window.sb = sb | ~507 |
| Face 0 div open | ~531 |
| #welcomeBtnWrap + #welcomeBtn | ~612 |
| Face 1 div open | ~609 |
| #musicBtn | ~569 |
| Sign Out button | ~851 |
| window.haptic (3× tuned) | ~1142 |
| _cubeTouchSounds | ~1142 |
| QC_AUDIO object | after ~1142 |
| Music auto-start IIFE | ~1214 |
| Vimeo music-pause bootstrap | (after QC_AUDIO block) |
| NUM.lp data (Life Path interpretations, variations) | ~1514+ |
| Quantum Cube Narrator block | ~1342 |
| voiceState defaults | ~1361 |
| showFace(n){ | ~1451 |
| STORE_KEY const | ~2095 |
| **async function checkStoredUnlock (user-scoped)** | **~2099** |
| **syncUnlockFromProfile (unconditional lock enforcement)** | **~2109** |
| applyUnlockedState | ~2138 |
| async function handleRevealClick | ~2323 |
| signInWithOtp paths | ~2378, ~2444 |
| sb.auth.onAuthStateChange | ~2471 |
| async function signOut | ~2501 |
| **function runCalculation** | **~2407** (STABLE ANCHOR) |
| function renderAllContent | ~2475 |
| numCards render (inline qcNarrateCard) | ~2668 |
| astroCards render (inline qcNarrateCard) | ~2697 |
| Legal overlay functions | ~2695-2716 |
| Legal doc HTML blocks (6 tabs) | ~2893-3056 |
| SW code string | ~2870 (**qc-v114**) |

---

## 🔐 AUTH + UNLOCK FLOW — POST-FIX STATE

### Session handling
- `persistSession: true`, `detectSessionInUrl: true`, `flowType: "implicit"`
- Session persists in localStorage until explicit signOut
- Closing tab + reopening → auto-advances into app ✅
- Magic-link short-circuit: if session email matches form email → skip magic link ✅
- Mismatched email → signs out session first, fires magic link for new email

### Unlock state (post-fix April 20)
- **STORE_KEY = user-scoped** — stores `session.user.id`, not literal "1"
- **checkStoredUnlock** async, only applies unlocked state if stored id matches current session user id
- **syncUnlockFromProfile** authoritative from DB. Unpaid branch UNCONDITIONALLY enforces locks (was previously guarded by `if(isUnlocked)` which skipped fresh-load unpaid users = the paywall bypass)
- **applyUnlockedState** hides .lock-screen, reveals face-content, stores user id

### Known remaining UX issue (not launch-blocker)
- Sign out + sign back in as **same email** same device still fires magic-link. Post-launch polish.

---

## 🪨 FRAGILE AREAS — DO NOT TOUCH CASUALLY

- **`@media (min-width:600px)` rules** are desktop-only on mobile — any CSS change inside those media queries is invisible on Ronnie's phone. Base rules apply to mobile. Cost 3 wasted commits on Apr 19.
- **BSD sed can't do multi-line replacements** — use Python one-shot (single read-replace-write, no iteration) for multi-line JS edits. Never iterate Python scripts to fix HTML.
- **`grep -c` returns exit 1 on zero matches** — kills pipelines silently. Use `|| true` after verify greps.
- **`head -N` piped after `git log` can trigger SIGPIPE (exit 141)** on macOS. Use `|| true`.
- **`.cursorignore` is no longer blocking** (removed April 21 in commit e1070fb) — Cursor can `str_replace` directly on `quantum-cube-v10.html`. Pre-April 21 the file was blocked and required shell-sed/Python workaround. That workaround is OBSOLETE. Old sessions or briefs referring to it are out of date.
- **Service worker cache bump is mandatory** every commit that changes the HTML, or users see stale content.
- **PWA cache stickiness:** "it's not working on my phone" is usually cache, not code. Follow the triage order in Diagnostic-First Discipline.
- **Magic-link must open in main Chrome**, not Gmail's internal browser — otherwise session won't land in correct context.
- **Single 11MB file was the norm, now 356KB after Apr 20 cleanup** — don't reintroduce base64 assets, always use file references from `Sounds/`.

### Supabase CLI gotcha
- `supabase db execute --project-ref` does not exist
- Use `supabase db query --linked "SQL"` from linked project directory

---

## WHAT'S LEFT — ORDERED BY PRIORITY

### 🚨 LAUNCH-BLOCKING

1. **Paddle setup** (ON PAUSE — needs M1 data + email Michelle)
2. **Accessibility trio** (~2 hours)
   - Remove `user-scalable=no` from viewport meta
   - Add `<h1>` + `<h2>` heading structure
   - Add `<label>` tags to 12 form inputs
3. **Rate limit narrate Edge Function** (~30 min) — per-IP limit in Deno
4. **Delete test profile rows**
5. **Final E2E paywall test** after Paddle lands (see Paywall Verification Protocol above)

### ⚠️ HIGH-VALUE THIS WEEK

6. **Vercel + Vimeo + GitHub subscription downgrades** (~10 min total)
7. **Email re-verification UX** — same-email resubmit detection
8. **Static `manifest.json` + `sw.js`** — replace blob URLs
9. **Sentry error monitoring** — ~20 min

### 🧹 POST-LAUNCH CLEANUP

10. **Split HTML into .js + .css files** — the big structural fix
11. **Pre-recorded TTS execution** (see locked decision above)
12. **Academy HeyGen cleanup** — NOT a Cube task, flagged separately for Academy sprint
13. **`git gc --aggressive`** — clean 1GB .git folder
14. **Fine-comb audit pass** — duplicate CSS selectors, dead code
15. **Resend return-path cosmetic**
16. **Brand Supabase magic-link email**

### 📝 POST-LAUNCH FOLLOW-UPS (weeks-months)

- Astrology/Chinese/Combined content variations (currently single-string)
- Face 5 narrative opener variations for remaining 6 paragraphs
- Additional music tracks (source 4 more ambient)
- info@quantumcube.app via Cloudflare routing
- Marketing email pipeline + unsubscribe endpoint
- DMARC p=none → p=quarantine after 2 weeks clean
- Business services migration quantumneurocreations@gmail.com → admin@qncacademy.com
- Gmail 2FA on all 3 partner accounts
- Analytics, social proof, sharing, profile deletion, smoke tests

### 🏪 APP STORE SUBMISSIONS

- Google Play: $25 one-time, PWABuilder → .aab
- Apple App Store: $99/year, Capacitor wrap, Xcode archive

---

## INFRASTRUCTURE LIVE
| System | State |
|---|---|
| GitHub Pages | Live (SW **qc-v114**) |
| quantumcube.app | Registered, DNS Cloudflare, not yet pointed |
| qncacademy.com | Full email stack live |
| Google Workspace | admin@qncacademy.com + 5 aliases |
| Cloudflare Email Routing | *@quantumcube.app → admin@qncacademy.com |
| Resend | Verified, SMTP in Supabase |
| ElevenLabs | Cube API key (TTS + Models perms only), Valory, narrate deployed |
| Supabase | Frankfurt, free tier, RLS verified, narrate deployed |

---

## ANNUAL RUNNING COST (APRIL 20)

### Current monthly subscriptions
- Claude Max: ~$200/mo (confirm actual tier)
- Claude Console: variable (Academy runtime Haiku 4.5 usage)
- Cursor Pro: ~$20/mo
- Vercel Pro: $20/mo → **downgrading to Hobby (free) while Academy in dev**
- Vimeo Starter: $20/mo monthly → **switching to annual (~$65/yr savings)**
- Epidemic Sound: ~$15/mo
- CapCut Pro: ~$8/mo
- ElevenLabs Creator: $22/mo
- Google Workspace: ~R112/mo

### Domains + hosting (annual)
- qncacademy.com: ~R200/yr
- quantumcube.app: ~R275/yr
- Google Workspace annual: ~R1,340/yr

### One-time / upcoming
- Google Play: $25 one-time
- Apple Developer: $99/yr (when App Store ready)
- ElevenLabs Pro one-month: $99 one-time (for pre-record migration)

**Post-subscription-trim monthly savings: ~$20/month + ~$65/year on Vimeo**

---

## SEPARATE PROJECT — QNC ACADEMY (context only, not this project's work)

- Path: /Users/qnc/Projects/qnc-academy/
- Stack: Next.js + Vercel + Supabase (Ireland) + Anthropic (Claude Haiku 4.5) + ElevenLabs + GitHub
- URL: qnc-academy.vercel.app (dev)
- Supabase ref `bevaepokvavzmykjmhda`
- **Quantum Integrator (QI)** = Academy's branded AI — scoped to Academy's cognitive framework, sine-wave visualized, ElevenLabs-voiced, Claude Haiku 4.5 brained
- **HeyGen avatar approach DEPRECATED** — subscription canceled, code cleanup pending (Academy sprint task)
- **Recent production deploys show Error status** — Academy sprint task
- **Never mix backend/tooling with Quantum Cube. Asset copies with consent permitted.**

---

## SESSION LOG

### April 19, 2026 (Saturday, marathon session — SW qc-v42 → qc-v99)
- 56 commits. Auth/unlock architecture fixes, cube default orientation, cube face key icon overhaul, music/voice button redesign, card widening, square matrix/astro cells, marketing consent copy, mobile lock-screen width fix (@media trap), payment button parity. ElevenLabs narrator foundation wired.

### April 20, 2026 (Monday, launch-prep day) — SW qc-v107 → qc-v114
**Commits:**
- `57dd972` — Remove 10.8MB base64 AUDIO object (97% file reduction)
- `22c67d7` — Remove Touch Cube 2.mp3 (sound not liked)
- `b96604d` — TEMP debug: reveal short-circuit diagnostics
- `fd41b68` — **CRITICAL paywall fix #1:** STORE_KEY user-scoped
- `41c2b49` — Remove TEMP debug after fix #1
- `a8d78c2` — TEMP paywall diagnostics (fix #1 was incomplete)
- `2403ca7` — **CRITICAL paywall fix #2:** unconditional lock enforcement for unpaid
- `b374fe5` — chore: ignore node_modules and .DS_Store
- `94af122` — **Legal additions:** entertainment opener + Original Works + AI-Assisted Content

**Context wins:**
- Three audits completed — internal/external/security — balanced, actionable
- Pre-recorded TTS strategy locked as team decision
- Paywall verified holding for unpaid + paid users
- Keyzer saw app over coffee — stars in eyes, team trust intact
- Subscription audit done — Vercel/Vimeo savings identified
- HeyGen deprecation clarified (canceled, cleanup pending)
- Content licensing resolved — original expression verified, 3 legal phrases added

### April 21, 2026 (Tuesday, Mac + Cursor hardening)
**Commit:**
- `e1070fb` — Mac + Cursor hardening: FileVault enabled, Cursor allowlist tightened (`bash -c` + `git push` removed), `diffTabDefaultAction` → `commit` (not `commitAndPush`), `autoApplyFilesOutsideContext` false, `.cursorrules` created at repo root, `.cursorignore` deleted (HTML now indexable by Cursor), backup files cleaned, `.gitignore` updated for `*.html.bak-*`, Cursor settings moved from DB-only to on-disk `settings.json`, Default Composer model locked to Claude Sonnet 4.5, Privacy Mode confirmed ON.

### Lessons learned (running)
- **checkStoredUnlock shared-device bug:** localStorage unlock flag was device-scoped, letting second user inherit first user's unlock. Fix: scope to user.id.
- **isUnlocked init + guard bug:** fresh-load unpaid users skipped lock enforcement because guard was "was previously unlocked, now re-lock" logic. Fix: unconditional enforcement.
- **Audit timing:** asking for audit at peak excitement after breakthrough produces emotional whiplash. Better to audit rested, separated from build work.
- **"Claude advised me to subscribe to X":** Claude (including AI assistants) tends to over-recommend tools when user is starting out. Rule: only subscribe when concrete wall is hit, not speculatively.
- **Content licensing reality:** "publicly available" ≠ "public domain." Heavy rewriting through AI iteration produces legally defensible original expression. Three small phrase additions make coverage airtight.
- **Cursor self-correction welcomed:** when verbatim-paste anchors fail due to indentation/escaping, Cursor correctly adjusting is the right behavior (per kickoff).

---

## NEXT SESSION STARTING POINT

1. **Confirm M1 data migration status** — Paddle requirements need to go to Michelle
2. **Accessibility trio** — 2 hours, launch-blocker
3. **Rate limiting on narrate Edge Function** — 30 min
4. **Subscription downgrades** — ~10 min (Vercel to Hobby, Vimeo to annual, verify GitHub free)
5. Then Paddle once Michelle has what she needs

**First action of next chat:** attach this brief v19 + CHAT_KICKOFF.md. Run the minimal health check. Confirm qc-v114 is serving live, paywall fix is holding (use Paywall Verification Protocol). Then pick from the priority list above.

---

**End of brief v19.**
