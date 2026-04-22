# QUANTUM CUBE — MASTER PROJECT DOCUMENT
**Version: v22 | Last Updated: April 22, 2026 (Wednesday, evening)**

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
- HeyGen cleanup (Academy's own cleanup task)
- Academy's Vercel deployment investigation
- The Academy Supabase project (Ireland, ref `bevaepokvavzmykjmhda`)
- Any `.env.local`, config, or secret from the Academy side

If a Cube chat drifts into any of the above, stop and ask.

---

## 🚦 NEW CHAT? READ CHAT_KICKOFF.md FIRST
The kickoff doc handles session startup, role split between Chat Claude and Cursor Claude, and the golden rules. Read it first, then read this brief for project-specific context.

---

## 🎯 APRIL 22 HEADLINE WINS — NARRATION FULLY SHIPPED

**Today closed the entire narration pipeline. Credit burn for normal user sessions: ZERO.**

Four major outcomes:

1. **Phase 1 narration locked end-to-end** — 256 numerology MP3s play offline-capable. Text and voice aligned via `data-variant`. No sha256 manifest lookup. Direct filename playback.

2. **Phase 2 narration shipped** — 129 new MP3s generated:
   - 9 Life Phases (single variant, 1-9, no masters per calculation rule)
   - 60 Western Astrology (12 signs × 5 fields)
   - 60 Chinese Horoscope (12 animals × 5 fields)
   - Total repo narration inventory: **385 MP3s, 187 MB**
   - ElevenLabs phase 2 overage: ~$13

3. **Service worker rebuilt** — real `sw.js` file replaces blob URL (Android Chrome 117+ rejects blob-SW silently). Two-cache architecture (`qc-v138` HTML + `qc-narration-v2` narration). Precache on install + cache-on-demand fallback. ASSETS bug fixed.

4. **Life Phases sequential player added** — new `playSequence` helper plays 3 phase clips back-to-back (Early → Middle → Later Years) inside single card UX.

**Credit burn audit for the full user journey:**
- Face 0 (signup): zero
- Face 1 (welcome video): zero
- Face 2 (results explained): zero
- Face 3 (numerology, including Life Phases): zero — all local MP3s
- Face 4 (astrology + Chinese): zero — all local MP3s
- Face 5 (combined results): ~1 credit per auto-narrate on entry (live TTS, intentionally kept)
- Face 6 (outro): zero
- Face 7 (settings): zero

Phase 5 is the ONLY credit-consuming surface at runtime.

---

## ⚠️ NEW PROCESS RULE — CURSOR SCOPE CREEP (v21 carry-forward)

Cursor Claude does NOT make substantive edits beyond what Chat Claude's paste block explicitly asks for. Self-correcting verbatim paste anchors (indentation, quote escaping) is welcomed. Fixing different bugs, adding normalizers, regenerating data files, bumping SW versions beyond what was requested — NOT permitted without explicit ask. If Cursor thinks additional work is needed, he surfaces it in output and waits.

**Add to CHAT_KICKOFF.md next update (still pending from v20).**

---

## 🔬 DIAGNOSTIC-FIRST DISCIPLINE

**Before any patch, always do these three first. No exceptions.**

```bash
git status                          # what's dirty, what branch
git log --oneline -10               # recent history, rollback anchor
grep -n "<symptom>" <likely-file>   # locate, don't guess
```

**Rules of engagement:**
- Never patch blind. If you can't point to the line/function causing the problem, you don't understand it yet.
- Never iterate Python scripts to fix HTML — one-shot only. If it fails, break into smaller `str_replace` edits instead.
- Never assume Cursor got the indentation or quote-escaping right in your first anchor. Expect and welcome self-correction on verbatim output.
- **Prefer Cursor's Browser MCP for live SW/cache/DevTools diagnosis over user phone screenshots.** April 22 lesson: 7 SW diagnostic commits traded vs Cursor diagnosing `ASSETS=['./']` 404 exception in one Browser MCP session.
- When adding diagnostics, use a temporary on-screen `#qcDebug` overlay + `window.qcLog()` — always remove in the next commit after fix lands.

**When "it's not working on my phone" — triage in this exact order:**
1. Regular Chrome tab (not PWA) at the GitHub Pages URL. If it works there → cache, not code.
2. Fully close Chrome (all tabs), wait 10s, reopen
3. Clear Chrome "All time" browsing data
4. Hand to Cursor with Browser MCP (real DevTools access via Mac Chrome)
5. Only then consider a code change

**Never burn a diagnostic commit on what's just PWA cache stickiness or SW install timing.**

---

## 👤 BUILDER CONTEXT

**Ronnie:**
- First-time developer, ~2.5 weeks into real building, no prior programming/coding/design experience.
- Mobile-primary: Android Chrome + PWA on phone, Mac mini M4 for dev + Cursor
- AI-directed workflow: 100% code by AI (Claude chat + Claude Cursor agent)
- Contributes: product vision, UX taste, bug catching, QA, project management, team comms
- Marathon-capable but energy-aware pacing matters

**How help should work:**
- Bias toward **verification over assumption** — grep/read before edit, expected-state checks after edit
- **Pace matches energy level** — short confirmable steps when tired, bigger moves when fresh
- **Prefer concise + confirmable changes** over large blind rewrites
- **Respect locked decisions** — do not relitigate
- **Use Cursor Browser MCP for live diagnosis** — don't force Ronnie to run repeated phone screenshot loops when DevTools access can solve it directly

**Avoid:**
- Over-recommending tools or subscriptions speculatively
- Emotional-whiplash audits right after breakthrough moments
- Assuming code literacy — explain the "why" in plain terms
- Silent rewrites of user paste blocks or Cursor scope creep
- Diagnostic loops that should have been one Browser MCP session

---

## 👥 TEAM CADENCE

- **Ronnie** — daily driver, all hands-on building. Every decision routes through here.
- **Michelle** — admin/support. Works async. **Needs clear asks, not open-ended.** Paddle requirements email ready — she has the M1 company + bank details.
- **Keyzer** — marketing + finance + payments. On-demand and strategic check-ins. Not daily.
- **Team decisions are made together and then LOCKED.** Once locked, Claude should not relitigate or re-open.

**Currently locked team decisions (do not re-open unprompted):**
- Pre-recorded TTS strategy (full pre-record for static content, Face 5 stays live) — **COMPLETE**
- HeyGen avatar approach deprecated for Academy — sine wave visualization instead
- $17 USD payment point (numerology: 1+7 = 8, wealth number)
- Paddle replaces PayFast globally (Merchant of Record for VAT/GST)
- Faceless brand — public contacts only `admin@qncacademy.com` and `info@qncacademy.com`
- Narrator UX = Option 3 (auto-read on category open; Voice button = mute/stop only)
- **Launch is not time-pressured** — ship when quality is right
- **Music + SFX refresh** — team wants fresh tracks and new SFX before launch
- **Master numbers** — ONLY apply to Life Path, Birthday, Expression, Soul Urge, Personality. All other categories reduce to single digits. (Life Phases calc uses `reduceH` which enforces this.)

---

## FILE LOCATIONS
```
/Users/qnc/Projects/quantumcube/              <- MAIN PROJECT FOLDER
|- quantum-cube-v10.html                      <- THE APP (~3194 lines, ~356 KB)
|- PROJECT_BRIEF.md                           <- This document (v22)
|- CHAT_KICKOFF.md                            <- Chat operating protocol (v3, due v4)
|- sw.js                                      <- Service worker (real file, 53 lines) — REPLACED BLOB URL April 22
|- cube-background.jpg                        <- Milky Way background (in repo)
|- .supabase-env                              <- Supabase + Resend + ElevenLabs creds (gitignored)
|- .cursorrules                               <- Cursor project rules
|- .gitignore                                 <- Committed; covers node_modules, .DS_Store, and *.html.bak-*
|- supabase/                                  <- Supabase CLI linked project
|   |- config.toml                            <- function-level flags (narrate verify_jwt=false)
|   \- functions/narrate/index.ts             <- ElevenLabs proxy Edge Function (38 lines)
|- Sounds/                                    <- Audio assets
|   |- Music/                                 <- 5 Academy ambient tracks (slated for replacement)
|   \- Narration/                             <- 385 pre-recorded Valory MP3s (187 MB)
|       |- num_{lp,bd,ex,su,pe,hp,kl,py}_*.mp3 <- Numerology (256 files, 3 variants each)
|       |- num_pc_{1-9}_v1.mp3                <- Life Phases (9 files, single variant)
|       |- west_<sign>_<slot>.mp3             <- Western Astrology (60 files)
|       |- chin_<animal>_<slot>.mp3           <- Chinese Horoscope (60 files)
|       \- welcome.mp3                        <- Welcome greeting
|- scripts/                                   <- Narration pipeline scripts
|   |- extract-narration.mjs                  <- Builds narration-manifest.json (179 lines, handles pc/west/chin)
|   \- generate-narration.mjs                 <- Loops manifest, POSTs to narrate Edge Function, skip-existing guard
\- narration-manifest.json                    <- 385 entries
```

**GitHub Repo:** https://github.com/quantumneurocreations-dot/quantumcube
**Live URL:** https://quantumneurocreations-dot.github.io/quantumcube/quantum-cube-v10.html
**Custom domain (registered, not yet pointed):** https://quantumcube.app

---

## 🧭 CANONICAL SAFE ROLLBACK POINTS

**Do not revert past these commits without a conscious decision.**

| Commit | Why you don't revert past it |
|---|---|
| `0546755` | Narration phase 2 wiring — Life Phases sequential + Face 4 astro/chinese narration + SW cleanup. Reverting breaks Face 4 narration + Life Phases. |
| `be9f385` | 129 phase 2 MP3s committed to repo. Reverting loses ~3MB of MP3s. |
| `636e3d8` | Narration phase 2 prep — strip dead 11/22 from NUM.pc, extend extractor. Reverting re-adds unreachable data. |
| `b0b87c5` | SW diagnostics rip + ASSETS fix — the install-time precache bug that blocked offline. Reverting re-breaks SW install. |
| `37f19fd` | Real sw.js file replaces blob URL — Android Chrome 117+ fix. Reverting re-breaks SW registration on Android. |
| `4d51c0d` | data-variant alignment — voice matches text. Reverting re-introduces random voice mismatch. |
| `c2e3c80` | Numerology direct MP3 path — ripped sha256 manifest/hash pipeline. Reverting breaks all numerology narration. |
| `e1070fb` | Cursor hardening — `.cursorrules` + allowlist tightening + gitignore update. |
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

**1. Clean start:** Chrome DevTools → Application → Storage → Clear site data. Hard-refresh.

**2. Unpaid test — carlkelbrick:** Form → submit → verify magic link → Face 3 should show Lock card "Complete Quantum Cube Unlock" with $17 button, NO numerology visible. DevTools → Local Storage → `STORE_KEY` absent/cleared (NOT "1", NOT user id).

**3. Switch to paid — quantumneurocreations:** Sign Out (Face 7) → clear `STORE_KEY` in DevTools → new email form → Face 3 should show full content, Valory narrates category taps. `STORE_KEY` = session.user.id (UUID).

**4. Tab close + reopen (paid):** Close tab. Wait 10s. Reopen live URL. Should auto-advance into app, unlocked, no magic-link re-verify.

**5. Switch back to unpaid (same device):** Sign Out → fill form with `carlkelbrick@gmail.com`. **Lock card MUST appear again. Previous unlock does NOT leak.** This is the test that failed before fix #1 + fix #2.

### Expected DOM states
| State | `.lock-screen` display | `#face3-content` display | `#lock3` icon | `.cube-face[data-idx=2]` class |
|---|---|---|---|---|
| Unpaid | `block` | `none` | visible | `.locked` |
| Paid | `none` | `block` | hidden | no `.locked` |

---

## 🏁 DEFINITION OF DONE — LAUNCH GATE

**All must be true before charging a real user:**

- [x] **Narration phase 1 verified** — 256 numerology MP3s, offline-capable
- [x] **Narration phase 2 shipped** — 9 Life Phases + 60 Western Astro + 60 Chinese MP3s, offline-capable
- [x] **Service worker rebuilt** — real sw.js file, two-cache architecture
- [ ] **Music + SFX refresh complete** — team has signed off
- [ ] **Paywall verified both directions** — paid unlocks, unpaid stays locked, sign-out re-locks, same-device different-user doesn't inherit unlock
- [ ] **Paddle E2E** — signup → verify → Paddle checkout → webhook → `has_paid=true` in DB → unlock persists across session + reload
- [ ] **All test profile rows deleted** from Supabase `public.profiles` (5 listed in backend section)
- [x] **Accessibility trio shipped** — remove `user-scalable=no` ✓, `<label>` to all 12 form inputs ✓ (7 done via for= attributes, 5 already implicit). `<h1>`/`<h2>` structure deferred post-launch.
- [ ] **narrate Edge Function rate-limited** per-IP (Deno KV or simple in-memory cap) to prevent apikey abuse from DevTools scraping
- [x] **Legal copy final** — entertainment opener, Original Works clause, AI-Assisted disclosure all present (commit 94af122)
- [ ] **SW version bumped + force-cache-tested** on Ronnie's phone — current qc-v138, qc-narration-v2
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
| Claude Console (API) | Academy's QI uses Claude Haiku 4.5 | Keep |
| Cursor Pro | Code editor with Claude agent | Keep |
| Epidemic Sound | Music licensing | Keep |
| CapCut Pro | Video production | Keep |
| ElevenLabs Creator | TTS for Cube narration + Academy QI voice | Keep — usage-based billing enabled April 22, phase 2 overage ~$13 |
| Google Workspace | Email infrastructure | Keep |
| GitHub | Code hosting, Pages hosting | Free tier |

### ⬇️ Downgrade / switch (parked pending team discussion)
| Service | Action | Savings |
|---|---|---|
| Vercel Pro | Downgrade to Hobby until Academy goes live | ~$20/month |
| Vimeo Starter | Switch from monthly to annual billing | ~$65/year |

### ❌ Confirmed deprecated
- **HeyGen** — subscription canceled. Academy codebase cleanup pending (not a Cube task).

---

## 📜 CONTENT LICENSING — RESOLVED

### Verified outcome
- Numerology, astrology, Chinese zodiac **concepts** are public domain
- **Written interpretations are original expression** — distinctive phrasing, narrative framing, 3 genuine rotation variations per number (numerology) or single authored version (astro/chinese)
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

## DEV ENVIRONMENT (M4 Mac Mini)

### Hardware + OS
| Item | Detail |
|------|--------|
| Machine | Mac Mini M4 |
| Username | qnc |
| FileVault | ON (enabled April 21) |
| Terminal arch | arm64 (native, not Rosetta) |
| Homebrew prefix | /opt/homebrew |

### Native ARM64 dev tools
| Tool | Version / Notes |
|---|---|
| Node.js | v24.15.0 native ARM via nvm |
| Python | 3.9.6 universal2 |
| git | universal2 |
| gh | v2.89.0 native ARM |
| Supabase CLI | v2.90.0 native ARM |
| cwebp | v1.6.0 native ARM |
| Vercel CLI | v51.5.0 |

### Cursor setup
| Setting | Value |
|---|---|
| Default Composer model | claude-4.5-sonnet |
| Privacy Mode | ON |
| `yoloCommandAllowlist` | 40 entries — `bash -c` and `git push` removed |
| `diffTabDefaultAction` | `commit` |
| `autoApplyFilesOutsideContext` | false |
| `autoAcceptWebSearchTool` | false |
| `.cursorrules` | tracked at repo root |
| `.cursorignore` | DELETED — `quantum-cube-v10.html` fully indexable |
| **Browser MCP** | Verified working April 22 — DevTools access via Mac Chrome. USE FOR LIVE DIAGNOSIS. |

---

## TECH STACK (LOCKED)
- **Frontend:** Single HTML file, vanilla JavaScript, CSS3 3D transforms, glassmorphism. **File size: ~356 KB, 3194 lines**
- **Fonts:** Cinzel Decorative, Cinzel, Cormorant Garamond
- **Auth:** Supabase magic-link (email OTP), SDK v2.45.4 UMD
- **Database:** Supabase Postgres (Frankfurt) — `public.profiles` with RLS
- **Email:** Resend via custom SMTP on Supabase
- **Payment:** PayFast sandbox currently wired — Paddle swap pending
- **Videos:** Vimeo Player API
- **Audio:**
  - **Music:** 5 Academy ambient tracks (slated for replacement)
  - **SFX:** 8 files (slated for replacement)
  - **Narration:** 385 pre-recorded Valory MP3s in `Sounds/Narration/` — Face 3 numerology (incl. Life Phases), Face 4 western + chinese; live Edge Function fallback for Face 5 ONLY
- **Haptics:** 3× strength
- **Hosting:** GitHub Pages
- **PWA:** Real `sw.js` file + dynamic web manifest via blob URL. Two-cache architecture:
  - `qc-v138` — HTML + root assets
  - `qc-narration-v2` — 385 MP3s (precached on install + on-demand fallback)

---

## 🎙️ ELEVENLABS NARRATOR

### Architecture (phase 2 complete April 22)
- **Voice:** Valory (voice ID `VhxAIIZM8IRmnl5fyeyk`)
- **Model:** `eleven_turbo_v2_5` with `{stability:0.5, similarity_boost:0.75, speed:1.15}` — 0.5 credits/char
- **Key storage:** `ELEVENLABS_API_KEY` as Supabase secret only
- **Edge Function:** `supabase/functions/narrate/index.ts`, deployed with `--no-verify-jwt` + inline apikey-header check
- **Narration inventory on disk: 385 MP3s**
  - 256 numerology (lp/bd/ex/su/pe/hp/kl/py, 3 variants each)
  - 9 Life Phases (pc, single variant 1-9)
  - 60 Western Astrology (12 signs × 5 slots)
  - 60 Chinese Horoscope (12 animals × 5 slots)
- **Frontend narration paths:**
  - Face 3 numerology categories → `startNarrationFromUrl` → `Sounds/Narration/num_<cat>_<num>_v<variant>.mp3`
  - Face 3 Life Phases → `playSequence` → 3× `Sounds/Narration/num_pc_<n>_v1.mp3` sequential
  - Face 4 western → `startNarrationFromUrl` → `Sounds/Narration/west_<sign>_<slot>.mp3`
  - Face 4 chinese → `startNarrationFromUrl` → `Sounds/Narration/chin_<animal>_<slot>.mp3`
  - Face 5 combined → `fetchNarration` → live Edge Function (ONLY credit-burn path at runtime)

### Edge Function source (for reference)

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

**Gap flagged for launch:** no rate limiting. Anyone who scrapes the apikey from DevTools can burn ElevenLabs credits. Fix: per-IP rate limit in Deno KV or simple in-memory token bucket. ~30 min work.

### ElevenLabs billing configuration (April 22)
- Plan: Creator ($22/mo base)
- **Usage-based billing ENABLED** — overage $0.30 per 1,000 credits
- Cap: 250,000 credits max (~$75 ceiling)
- Phase 1 batch: ~60k credits (~$16 + tax), already incurred
- Phase 2 batch: ~43k credits (~$13 + tax), already incurred
- **Total April 22 overage: ~$33**
- Legacy feature warning: usage-based billing not available on new subscriptions — we're grandfathered in. Do not cancel/resubscribe.

### Frontend UX — Option 3 (auto-read on open)
Voice defaults ON, Voice button = mute/stop only.
- Face 1: "▶ Welcome" button (once-per-user localStorage `qc_greeted`) — Valory greets on tap. **(Earmarked for rework — Ronnie wants auto-play, not button.)**
- Faces 3/4: Tap category → opens AND narrates. Voice toggles future narration.
- Face 5: Auto-narrates on entry ~500ms, token-gated + visibility-checked

### 🔒 LOCKED DECISION — Pre-recorded TTS strategy (COMPLETE)
- Welcome greeting: 1 file ✓
- Numerology: 256 files ✓
- Life Phases: 9 files ✓
- Western Astrology: 60 files ✓
- Chinese Horoscope: 60 files ✓
- Combined Face 5: stays on live TTS (chunk-and-stitch too combinatorial to pre-record) ✓

**Benefits realized:** instant playback, offline via PWA cache, consistent quality, no API failure risk at runtime, near-zero credit burn per user session.

---

## 🔊 AUDIO SYSTEM — QC_AUDIO
Music: 5-track rotation, 0.20 vol, first-tap auto-start, fades, Vimeo pause-on-play. **Slated for replacement.**
SFX: 0.30 vol, wired to 6 triggers. **Slated for replacement.**
Haptics: 3× strength.

---

## 🔁 PAYMENT PROCESSOR — PADDLE (UNBLOCKED)

Michelle has M1 data. Ready to send Paddle requirements email when Ronnie wants to initiate.

**Execution queue (post launch prep polish):**
- Email Michelle Paddle requirements
- Paddle team application
- Paddle webhook Edge Function (server-side `has_paid` flip)
- Rewrite `launchPayFast()` → Paddle checkout
- Remove PayFast refs
- Update legal docs (remove PayFast, update IP tab to Paddle)
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
| Face 1 | Introduction video + Welcome greeting button | Welcome button earmarked for rework |
| Face 2 | Results Explained videos | |
| Face 3 | Numerology Results | Locked unless paid. Voice. All categories incl. Life Phases narrate from local MP3s. |
| Face 4 | Astrology & Horoscope | Locked unless paid. Voice. Western + Chinese narrate from local MP3s. |
| Face 5 | Combined Results | Locked unless paid. Auto-narrates on entry. **ONLY live TTS path.** |
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
- `quantumneurocreations@gmail.com` — has_paid=true
- `carlkelbrick@gmail.com` — has_paid=false
- `rkelbrickmail@gmail.com` — has_paid=false
- `test+chunk5b@qncacademy.com` — has_paid=false
- `carlkelbrick+test@gmail.com` — has_paid=false

---

## FRONTEND WIRING — KEY LINE REFS (April 22 v22 — use grep, numbers drift)

| What | Approx line |
|---|---|
| const sb = window.supabase.createClient | ~499 |
| Face 0 / 1 / welcomeBtn | ~531 / ~609 / ~613 |
| window.haptic + _cubeTouchSounds | ~1142 |
| QC_AUDIO + music auto-start | ~1142+ / ~1214 |
| NARRATE_URL + NARRATION_DIR constants | ~1312-1314 |
| fetchNarration (Edge Function, Face 5 only) | ~1349 |
| startNarration | ~1380 |
| startNarrationFromUrl | ~1388 |
| **playSequence (Life Phases sequential)** | **~1404** |
| window.qcNarrateCard (Face 3 + Face 4 dispatch) | ~1420 |
| voiceState defaults | ~1361 |
| showFace(n){ | ~1510 |
| NUM data (incl. pc with keys 1-9 only post-strip) | ~1550+ |
| STORE_KEY const | ~2095 |
| **async function checkStoredUnlock (user-scoped)** | **~2099** |
| **syncUnlockFromProfile (unconditional lock enforcement)** | **~2109** |
| applyUnlockedState | ~2138 |
| handleRevealClick | ~2323 |
| signInWithOtp paths | ~2378, ~2444 |
| sb.auth.onAuthStateChange | ~2471 |
| signOut | ~2501 |
| **function runCalculation** | **~2589** (STABLE ANCHOR) |
| renderAllContent | ~2602 |
| getNumIdx + getNumText | ~2598 / ~2612 |
| numSecs construction (incl. pc phases array) | ~2654 |
| numCards render (data-cat/num/first/variant/phases) | ~2714 |
| astroSecs + astroCards render (data-prefix/key/slot) | ~2683 / ~2745 |
| Legal overlay functions | ~2695-2716 |
| SW registration (navigator.serviceWorker.register('sw.js')) | ~2900 |

---

## 🔐 AUTH + UNLOCK FLOW — POST-FIX STATE (unchanged from v21)

### Session handling
- `persistSession: true`, `detectSessionInUrl: true`, `flowType: "implicit"`
- Session persists in localStorage until explicit signOut
- Closing tab + reopening → auto-advances into app
- Magic-link short-circuit: if session email matches form email → skip magic link
- Mismatched email → signs out session first, fires magic link for new email

### Unlock state
- **STORE_KEY = user-scoped** — stores `session.user.id`
- **checkStoredUnlock** — only applies unlocked state if stored id matches current session user id
- **syncUnlockFromProfile** — authoritative from DB. Unpaid branch unconditionally enforces locks.
- **applyUnlockedState** hides .lock-screen, reveals face-content

### Known remaining UX issue (not launch-blocker)
- Sign out + sign back in as same email same device still fires magic-link. Post-launch polish.

---

## 🪨 FRAGILE AREAS — DO NOT TOUCH CASUALLY

- **Service worker is a real file now** (`sw.js`, 53 lines). Do NOT revert to blob URL — Android Chrome 117+ rejects blob SW silently.
- **`@media (min-width:600px)` rules** are desktop-only on mobile — any CSS change inside those media queries is invisible on Ronnie's phone. Base rules apply to mobile.
- **BSD sed can't do multi-line replacements** — use Python one-shot (single read-replace-write, no iteration) for multi-line JS edits. Never iterate.
- **`grep -c` returns exit 1 on zero matches** — kills pipelines silently. Use `|| true` after verify greps.
- **`head -N` piped after `git log` can trigger SIGPIPE (exit 141)** on macOS. Use `|| true`.
- **Service worker cache bump is mandatory** every commit that changes the HTML. Narration cache only bumps when MP3s change.
- **PWA cache stickiness:** "it's not working on my phone" is usually cache or SW install timing, not code. Follow triage order in Diagnostic-First Discipline.
- **Magic-link must open in main Chrome**, not Gmail's internal browser — otherwise session won't land in correct context.
- **Never reintroduce base64 assets** — 10.8MB cleanup on April 20 reduced file from 11MB to 356KB.
- **Cursor's unauthorized commits** — see process rule.
- **Life Phases is sequential playback** — 3 MP3s stitched via `playSequence` inside one card. Do not convert to 3 separate cards without product approval.
- **Master numbers in NUM.pc are stripped** (commit 636e3d8). Do not re-add — `calcCyc` uses `reduceH` enforcing single-digit phases.

### Supabase CLI gotcha
- `supabase db execute --project-ref` does not exist
- Use `supabase db query --linked "SQL"` from linked project directory

---

## WHAT'S LEFT — ORDERED BY PRIORITY

### 🚨 LAUNCH-BLOCKING
1. **App polish pass** — Ronnie noted various in-app corrections and fixes needed. Scope to define this session.
2. **Music + SFX refresh** — team scope + source + integrate
3. **Paddle setup** — Michelle has data, ready to initiate
4. **Rate-limit narrate Edge Function** (~30 min)
5. **Delete test profile rows**
6. **Final paywall E2E test** after Paddle lands
7. **Welcome greeting rework** — auto-play instead of button (per Ronnie note April 22)

### ⚠️ HIGH-VALUE
8. Accessibility h1/h2 structure — deferred post-launch
9. Static `manifest.json` — replace blob URL (sw.js already done)
10. Sentry error monitoring — ~20 min
11. Email re-verification UX — same-email resubmit detection

### 🧹 POST-LAUNCH CLEANUP
12. Split HTML into .js + .css files
13. `git gc --aggressive` — clean large .git folder (currently ~1.2GB)
14. Login loop fix (same-email resign triggers new magic link)
15. HeyGen cleanup (Academy side)
16. Fine-comb audit pass — duplicate CSS selectors, dead code
17. Brand Supabase magic-link email

### 📝 POST-LAUNCH FOLLOW-UPS (weeks-months)
- Astrology/Chinese variations (currently single-string, might author 3-variant versions like numerology)
- Face 5 narrative opener variations for remaining 6 paragraphs
- Additional music tracks
- info@quantumcube.app via Cloudflare routing
- Marketing email pipeline + unsubscribe endpoint
- DMARC p=none → p=quarantine after 2 weeks clean
- Gmail 2FA on all 3 partner accounts
- Analytics, social proof, sharing, profile deletion, smoke tests

### 🏪 APP STORE SUBMISSIONS
- Google Play: $25 one-time, PWABuilder → .aab
- Apple App Store: $99/year, Capacitor wrap, Xcode archive

---

## INFRASTRUCTURE LIVE
| System | State |
|---|---|
| GitHub Pages | Live (SW **qc-v138**, narration **qc-narration-v2**) |
| quantumcube.app | Registered, DNS Cloudflare, not yet pointed |
| qncacademy.com | Full email stack live |
| Google Workspace | admin@qncacademy.com + 5 aliases |
| Cloudflare Email Routing | *@quantumcube.app → admin@qncacademy.com |
| Resend | Verified, SMTP in Supabase |
| ElevenLabs | Valory, narrate deployed, usage-based billing enabled (250k cap) |
| Supabase | Frankfurt, free tier, RLS verified, narrate deployed |

---

## ANNUAL RUNNING COST

### Current monthly subscriptions
- Claude Max: ~$200/mo
- Claude Console: variable (Academy runtime)
- Cursor Pro: ~$20/mo
- Vercel Pro: $20/mo → downgrade parked
- Vimeo Starter: $20/mo → annual switch parked
- Epidemic Sound: ~$15/mo
- CapCut Pro: ~$8/mo
- ElevenLabs Creator: $22/mo (usage-based enabled, ~$33 one-time April 22 phase 1+2 overage)
- Google Workspace: ~R112/mo

### Domains + hosting (annual)
- qncacademy.com: ~R200/yr
- quantumcube.app: ~R275/yr
- Google Workspace annual: ~R1,340/yr

### One-time / upcoming
- Google Play: $25
- Apple Developer: $99/yr (when App Store ready)

---

## SEPARATE PROJECT — QNC ACADEMY (context only)

- Path: /Users/qnc/Projects/qnc-academy/
- Stack: Next.js + Vercel + Supabase (Ireland) + Anthropic (Claude Haiku 4.5) + ElevenLabs + GitHub
- URL: qnc-academy.vercel.app (dev)
- Supabase ref `bevaepokvavzmykjmhda`
- **Quantum Integrator (QI)** = Academy's branded AI — Academy's cognitive framework, sine-wave visualized, ElevenLabs-voiced, Claude Haiku 4.5 brained
- **HeyGen avatar approach DEPRECATED** — subscription canceled, code cleanup pending
- **Never mix backend/tooling with Quantum Cube. Asset copies with consent permitted.**

---

## SESSION LOG

### April 19, 2026 (Saturday, marathon session — SW qc-v42 → qc-v99)
56 commits. Auth/unlock architecture fixes, cube orientation, music/voice button redesign, card widening, square matrix/astro cells, marketing consent copy, mobile lock-screen width fix, payment button parity. ElevenLabs narrator foundation wired.

### April 20, 2026 (Monday, launch-prep — SW qc-v107 → qc-v114)
- `57dd972` Remove 10.8MB base64 AUDIO (11MB → 356KB)
- `fd41b68` CRITICAL paywall fix #1: STORE_KEY user-scoped
- `2403ca7` CRITICAL paywall fix #2: unconditional lock enforcement
- `94af122` Legal additions: entertainment opener + Original Works + AI-Assisted

Three audits completed. Pre-recorded TTS strategy locked. Keyzer saw app — stars in eyes. Subscription audit done. Content licensing resolved.

### April 21, 2026 (Tuesday, Mac + Cursor hardening)
- `e1070fb` FileVault enabled, Cursor allowlist tightened, `.cursorrules` at repo root, `.cursorignore` deleted, Privacy Mode confirmed ON.

### April 21-22, 2026 (Tuesday evening → Wednesday morning — narration phase 1 struggle)
Scaffolded pre-record pipeline, generated 256 numerology MP3s. Hash-based lookup initially failed on Android Chrome. Multiple debug rounds. Session ended with phase 1 shipped but unverified on mobile.

### April 22, 2026 (Wednesday, narration phase 1 lock + phase 2 ship + SW rebuild)

**Morning — narration pipeline rip + rebuild (SW qc-v122 → qc-v138):**
- `c2e3c80` Rip sha256 manifest/hash pipeline, direct MP3 playback for numerology
- `4d51c0d` data-variant alignment — voice matches displayed text
- `639bd09` SW two-cache architecture (HTML + narration separate)
- `2ba2a1e` Fix blob-scope URL resolution
- `e83b152` Batch narration precache in groups of 8
- `37f19fd` **Replace blob-URL SW with real sw.js file** — fixes Android Chrome 117+ silent registration failure
- Seven SW diagnostic commits (v127 → v136) as we hunted offline mode bug blind. Lesson: should have used Cursor Browser MCP 5 commits earlier.
- `b0b87c5` Cursor diagnosed via Browser MCP — `ASSETS=['./']` 404 exception in SW install. Ripped diagnostics, fixed root cause.

**Afternoon — narration phase 2 (SW v137 → v138, narration v1 → v2):**
- `636e3d8` Strip dead 11/22 keys from NUM.pc, extend extractor for pc/west/chin (manifest 256 → 385 entries)
- `be9f385` Generate 129 phase 2 MP3s (9 Life Phases + 60 Western + 60 Chinese), ~$13 overage
- `0546755` Frontend wiring — Life Phases sequential playback + Face 4 astro/chinese narration + SW activate cleanup for old narration caches

**Evening outcome:** Full narration inventory complete. Every user-facing narration path runs on local MP3s except Face 5 combined results. Credit burn for average user session: near zero.

### Lessons learned (running, updated April 22)
- **SW diagnosis via phone screenshots is a trap.** Use Cursor Browser MCP with DevTools access. Saves hours.
- **Blob-URL service workers fail silently on Android Chrome 117+.** Use real files at origin scope.
- **`ASSETS=['./']` in SW install breaks if no root index.** Always verify actual fetch responses when `cache.addAll` throws.
- **Chrome HTTP cache masks broken SW installs** — user taps a card online, Chrome caches it via HTTP disk cache, airplane mode plays it. Looks like SW works. It doesn't.
- **Cursor self-correction on verbatim anchors is welcomed.** Cursor unprompted feature additions are not.
- **Text-voice alignment matters** — rotation must be deterministic (data-variant), not random (Math.random) — else user reads variant A but hears variant B.
- **Master numbers are category-specific** — only lp/bd/ex/su/pe keep 11/22/33. All other categories reduce to single digits. Enforced in data AND calc.
- **Sequential playback is cleaner than card-split** for Life Phases — preserves UX, adds one helper function.
- **Compression risk is real at multi-hour sessions.** Respect stop signals, update brief, start fresh.
- **Every brief version must be self-contained.** No "See v20 for detail" — info loss on aging.

---

## NEXT SESSION STARTING POINT

1. Attach PROJECT_BRIEF.md (v22) + CHAT_KICKOFF.md to new chat
2. Minimal health check: confirm HEAD is `0546755` on `origin/main`, SW = qc-v138, narration = qc-narration-v2, runCalculation at line ~2589
3. **Ronnie has in-app corrections + fixes to walk through.** Scope that work session first.
4. Then by priority: music + SFX refresh → Paddle initiation → narrate Edge Function rate limit → test profile row cleanup.

---

**End of brief v22.**
