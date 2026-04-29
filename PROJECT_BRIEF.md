# QUANTUM CUBE — MASTER PROJECT DOCUMENT
**Version: v25 | Last Updated: April 29, 2026 (Wednesday, evening)**

---

## ⚠️ CRITICAL RULE — ALWAYS READ FIRST
**Quantum Cube and QNC Academy are COMPLETELY SEPARATE projects — at the backend/tooling/profile level.**
- Never mix backend code, Supabase projects, API keys, or tool configs between them
- Quantum Cube has its own Supabase project (Frankfurt) — never touch the Academy one (Ireland)
- Quantum Cube has its own ElevenLabs API key — never share or cross-use

**Asset sharing is fine when explicit.** Copying logos/music/audio across projects is permitted when the user approves. The rule targets backend cross-contamination, not file assets.

### 🚫 NOT Quantum Cube's job
- The Academy website (Next.js codebase at `/Users/qnc/Projects/qnc-academy/`)
- The Quantum Integrator (QI) — Academy's branded AI built on Claude Haiku 4.5
- HeyGen cleanup (Academy's own task)
- Academy's Vercel deployment
- The Academy Supabase project (Ireland, ref `bevaepokvavzmykjmhda`)
- Any `.env.local`, config, or secret from the Academy side

If a Cube chat drifts into any of the above, stop and ask.

---

## 🚦 NEW CHAT? READ CHAT_KICKOFF.md FIRST
The kickoff doc handles session startup, role split between Chat Claude and Cursor Claude, and the golden rules. Read it first, then read this brief.

---

## 🎉 BIGGEST WINS SINCE v24

**1. Payment processor decision FINAL: Dodo Payments.** Application submitted April 29, in 24-72hr review. They actively market to astrology brands (have a dedicated blog post on it). LemonSqueezy parked, FastSpring parked, Paddle definitively ruled out (their AUP explicitly prohibits "fortune-telling/horoscopes/clairvoyance").

**2. Account deletion + data export shipped and VERIFIED.** Two new Edge Functions, two-tap confirmation pattern, full localStorage wipe, signOut timeout race. Smoke-tested end-to-end on Apr 29 — deletion cascades cleanly, fresh signup with same email works.

**3. narrate Edge Function rate-limited.** Postgres RPC-based (5/min, 20/hr per IP). Closed the credit-burn vulnerability.

**4. Static manifest.json replaces blob URL.** Google Play submission prerequisite met. Real PNG icons still pending (designer/Canva work).

**5. Magic-link email rebranded.** Dark cosmic Quantum Cube template applied via Supabase dashboard.

**6. Brand wordmark pack committed.** White/gold Cinzel Decorative wordmark in 3 PNG variants + fonts.

---

## 📅 SESSION TIMELINE (April 29, 2026 — single-day sprint)

10 commits shipped this day:

| Commit | What |
|---|---|
| `7016cb1` | feat(narrate): per-IP rate limiting (Postgres RPC, 5/min + 20/hr) |
| `f9a3df3` | chore(db): commit existing remote migration to repo (profiles + RLS + handle_new_user trigger) |
| `43e397e` | feat(pwa): static manifest.json replaces blob URL |
| `0fcbdb9` | feat(account): data export + account deletion (POPIA/GDPR rights) |
| `dddb84e` | debug(delete): diagnostic logs + signOut timeout race |
| `21b9c99` | fix(delete): rip diagnostic logs, keep timeout race |
| (next) | feat(brand): commit Quantum Cube wordmark pack |
| (next) | docs: brief v25 rewrite |

**Non-code outcomes Apr 29:**
- Paddle definitively ruled out (verified directly from AUP — fortune-telling prohibition)
- FastSpring KYB started by Michelle then parked (no products live, returnable as fallback)
- Dodo Payments signup submitted, in 24-72hr review
- Magic-link email HTML pasted to Supabase dashboard, preview confirmed
- Security audit complete: 3 items checked, only narrate rate limit needed fixing
- Paddle/PayFast 26-line punch list captured for post-Dodo cleanup
- Brand identity locked: Cinzel Decorative + white/gold accent
- Logo strategy: Canva Pro for wordmarks (already have), designer for cube icon (post-launch acceptable)
- Social media handle plan: 6 platforms, claim only after launch (no posts yet)

---

## 💳 PAYMENT PROCESSOR — Dodo Payments

### Why Dodo

| Factor | Dodo | LemonSqueezy | FastSpring | Paddle |
|---|---|---|---|---|
| Astrology/esoteric content | **Actively markets to it** | Allowed (silent) | Allowed (silent) | **PROHIBITED** |
| Pricing | 4% + 40¢ (+1.5% non-US) | 5% + 50¢ | 8.9% | 5% + 50¢ |
| MoR + global tax | ✓ | ✓ | ✓ | ✓ |
| Founded | 2023 | 2021 | 2005 | 2012 |
| SA seller | ✓ | ✓ (pending) | ✓ | N/A |

**Dodo AUP relevant categories:**
- Spiritual & Astrology services → "Categories That Often Require Review" (entertainment only, no claims/predictions) — we comply ✓
- Religious/spiritual *services* → prohibited, but this is for prayer/ritual/spiritual-authority access, not us ✓
- AI Content Generation tools → review category if we sold the tool; we use AI voice as part of product, not selling generation ✓

### Account details
- **Account name:** Quantum Neuro Creations (registering as business)
- **Account owner (operator):** Michelle Booyens
- **Subdomain:** `quantumcube_store.onfastspring.com` was for FastSpring; Dodo uses different URL structure (TBD on approval)
- **Status (Apr 29):** Submitted, awaiting review (24-72hr)

### Fallback chain (if Dodo rejects)
1. **Dodo** ← we are here
2. **FastSpring** — already registered, account dormant, can be reactivated
3. **LemonSqueezy** — application open from earlier in week, on SA tax form hold
4. **Polar.sh** — open-source MoR, Stripe-backed
5. **Creem** — newer, indie-hacker focus
6. **Gumroad** — last resort, 10% flat fee

### Dodo MoR legal entity name
**TBD** — confirm exact entity name from Dodo dashboard once approved. Likely "Dodo Payments, Inc." but verify before swapping legal copy.

---

## 📋 PADDLE/PAYFAST PUNCH LIST — 26 lines to swap when Dodo approves

### `docs/app.html` — 17 lines
- L2178-2188: PayFast integration block + sandbox credentials
- L2306-2347: `launchPayFast()` function definition
- L2348-2350: `checkPayFastReturn()` function definition
- L2964-2967: page-load handler calling `checkPayFastReturn()`
- L3223: button onclick="launchPayFast()"
- L3027, 3038, 3128, 3153, 3180: 5 in-app legal copy mentions

### `docs/*.html` (8 public pages, 9 occurrences)
- contact.html:31 — billing contact line
- index.html:54 — landing page price note
- ip.html:45 — third-party attribution list
- popia.html:26 — POPIA disclosure
- privacy.html:21 + privacy.html:42 — privacy policy (2 mentions)
- refund.html:48 — refund policy MoR disclosure
- security.html:27 — security page
- terms.html:34 — terms of use

### Migrations
- `supabase/migrations/20260417104424_create_profiles_table_and_rls.sql:31` — `has_paid` column comment mentions PayFast

### Code rename
- `launchPayFast()` → `launchDodo()`
- `checkPayFastReturn()` → `checkDodoReturn()` (or remove entirely if Dodo handles return differently)
- New: Dodo webhook Edge Function at `supabase/functions/dodo-webhook/`

### MoR text swap
- "PayFast (Pty) Ltd" → "Dodo Payments, Inc." (or actual entity name once confirmed)
- "Paddle.com Market Limited" → "Dodo Payments, Inc."

---

## 📜 REFUND POLICY — needs Dodo MoR swap when approved

Currently published at `quantumcube.app/refund` with **Paddle wording**. Update conditions:
- "Paddle.com Market Limited" → Dodo legal entity name
- "contact Paddle support" → "contact Dodo Payments support"

Otherwise refund policy wording stands as approved by Ronnie on April 23: no refunds + limited exceptions + chargebacks clause + Merchant of Record disclosure.

---

## 🎨 BRAND IDENTITY

### Existing assets (committed Apr 29 in `brand/` folder)
- `quantum-cube-logo-1400.png` — wordmark, 1400×?
- `quantum-cube-logo-2800.png` — wordmark, 2800×? (high-res)
- `quantum-cube-logo.svg` — wordmark vector
- `quantum-cube-tiktok-1080.png` — TikTok profile variant
- `quantum-cube-tiktok-profile.svg` — TikTok variant vector
- `cinzel-decorative-bold.woff2` + `cinzel-regular.woff2` — self-hosted fonts (backup if Google Fonts fail)

### Visual language (locked)
- Primary typeface: Cinzel Decorative (wordmarks)
- Secondary typeface: Cinzel (subtitles, smaller text)
- Colour pattern: white-as-base + ONE gold/orange accent word
- Background: dark cosmic / black
- Style: ornate serif, premium, mystical-but-clean

### Logo work still needed (pre-launch acceptable)
| Asset | Purpose | Status |
|---|---|---|
| Cyan cube icon (square) | App icon, favicon, social profile pic | **Needed** |
| Brain + CPU chip half/half icon | Brand family conceptual badge | Optional, post-launch |
| Real PNG icons at 192/512/maskable | manifest.json, Google Play submission | **Needed** |

**Tool decision:** Canva Pro for cube icon attempt (Ronnie has access). 30-min Canva attempt; if it doesn't land well, $30-50 Fiverr designer for square icons matching the in-app cyan cube vibe. Don't sink hours into Canva trying to make illustration work.

---

## 📱 SOCIAL MEDIA — Handles to claim (NOT YET CREATED)

Decided Apr 28, confirmed Apr 29. Claim now, **post nothing until launch announcement.**

| Platform | Preferred | Fallback |
|---|---|---|
| YouTube | @quantumcube | @quantumcubeapp |
| Facebook | /quantumcube | /quantumcubeapp |
| X / Twitter | @quantumcube | @quantumcubeapp |
| Instagram | @quantumcube | @quantumcubeapp |
| TikTok | @quantumcube | @quantumcubeapp |
| Threads | @quantumcube | @quantumcubeapp |

**Steps:**
1. namechk.com to verify availability across all 6
2. If `@quantumcube` not available everywhere → fall back to a single consistent alternative
3. Set up profiles with consistent display name "Quantum Cube" + same bio + same logo + same banner
4. **Don't post anything** until launch — prevents impersonation, locks brand consistency

**Blocker:** social media setup needs the cube icon for profile pics. Sequence: logo work → social claiming.

---

## 📂 FILE LOCATIONS
/Users/qnc/Projects/quantumcube/              <- MAIN PROJECT FOLDER
|- docs/                                       <- GITHUB PAGES SOURCE
|   |- index.html                              <- public landing page
|   |- app.html                                <- THE CUBE APP
|   |- styles.css                              <- shared Cinzel + Cormorant dark cosmic styling
|   |- manifest.json                           <- static PWA manifest (qc-v147 era)
|   |- privacy.html / terms.html / refund.html
|   |- disclaimer.html / ip.html / popia.html
|   |- security.html / contact.html
|   |- sw.js                                   <- Service worker (qc-v147 + qc-narration-v2)
|   |- CNAME                                   <- quantumcube.app
|   |- .nojekyll
|   |- Sounds/                                 <- audio assets
|   - cube-background.jpg                     <- Milky Way background
|- brand/                                      <- Wordmark PNGs + Cinzel fonts (committed Apr 29)
|- supabase/
|   |- config.toml                             <- function-level flags (3 functions: narrate, delete-account, export-data)
|   |- migrations/
|   |   |- 20260417104424_create_profiles_table_and_rls.sql
|   |   - 20250429140000_narrate_rate_limit.sql
|   - functions/
|       |- narrate/index.ts                    <- ElevenLabs proxy with rate limit
|       |- delete-account/index.ts             <- Auth admin delete (Apr 29)
|       - export-data/index.ts                <- Profile JSON export (Apr 29)
|- scripts/                                    <- Narration pipeline scripts
|- narration-manifest.json                     <- 385 entries
|- PROJECT_BRIEF.md                            <- This document (v25)
|- CHAT_KICKOFF.md                             <- Chat operating protocol
|- .supabase-env                               <- creds (gitignored)
|- .cursorrules                                <- Cursor project rules
- .gitignore

**GitHub Repo:** https://github.com/quantumneurocreations-dot/quantumcube
**Live URLs:** quantumcube.app + /app + 8 legal pages (all 200 OK)
**Pages source:** `/docs` directory on `main` branch

---

## 🧭 CANONICAL SAFE ROLLBACK POINTS

**Do not revert past these without conscious decision.**

| Commit | Why you don't revert past it |
|---|---|
| `21b9c99` | **Account deletion + export production-ready.** Reverting = stuck "Deleting..." bug returns + Google Play hard-requirement fails. CRITICAL |
| `0fcbdb9` | Account deletion + export shipped. Reverting = no in-app deletion. CRITICAL for Google Play |
| `43e397e` | Static manifest.json. Reverting = blob URL returns, PWABuilder broken |
| `f9a3df3` | Migration reconciliation. Reverting = `db push` fails |
| `7016cb1` | narrate rate limit. Reverting = ElevenLabs credit-burn vulnerability returns |
| `cc63d90` | `/app/` trailing-slash redirect — without this `quantumcube.app/app/` 404s |
| `32a23f0` | `.nojekyll` for static HTML + privacy redirect |
| `e8bfbc4` | `/docs` restructure — reverting breaks Pages deployment |
| `2e888d2` | **Public site landing + legal pages.** Reverting kills MoR/Google Play readiness. CRITICAL |
| `7a9b7ac` | Music randomisation per session + user-scoped welcome counter |
| `546363b` | Welcome greeting auto-play from local MP3 |
| `2d38560` | Music refresh + randomisation + cube-touch SFX rip |
| `231803e` | Face-name label card + auto-scroll |
| `0bd5a54` | **Paywall fix #3 — renderAllContent gating.** CRITICAL |
| `0546755` | Narration phase 2 wiring |
| `be9f385` | 129 phase 2 MP3s committed |
| `636e3d8` | Narration phase 2 prep |
| `b0b87c5` | SW diagnostics rip + ASSETS fix |
| `37f19fd` | Real sw.js file replaces blob URL — Android Chrome 117+ fix |
| `4d51c0d` | data-variant alignment |
| `c2e3c80` | Numerology direct MP3 path |
| `e1070fb` | Cursor hardening |
| `94af122` | Legal additions |
| `2403ca7` | **Paywall fix #2.** CRITICAL |
| `fd41b68` | **Paywall fix #1.** CRITICAL |
| `57dd972` | 10.8MB cleanup |

When in doubt, `git revert <commit>` a specific bad change rather than resetting through these anchors.

---

## ✅ PAYWALL VERIFICATION PROTOCOL — 4-layer defence

1. `STORE_KEY` user-scoped (`fd41b68`)
2. `syncUnlockFromProfile` unconditional lock branch (`2403ca7`)
3. `renderAllContent` gates on `isUnlocked` (`0bd5a54`)
4. **Database-level lock on `has_paid` column** (RLS policy in `20260417104424` migration — `with check` clause prevents user from updating their own `has_paid`)

**Paywall verified working both directions on April 23.** Test sequence in v24 still applies. Use `quantumneurocreations@gmail.com` (paid) and `carlkelbrick@gmail.com` (unpaid) profiles.

---

## 🏁 DEFINITION OF DONE — LAUNCH GATE

### ✅ DONE
- Narration phase 1 + 2 verified (385 MP3s, offline-capable)
- Service worker rebuilt (qc-v147, two-cache architecture)
- Paywall fix #3 (renderAllContent gated)
- Music refresh + randomisation
- Welcome greeting auto-plays
- Face name label card + auto-scroll
- Public landing page + 8 legal pages live
- quantumcube.app domain HTTPS verified
- Paywall verified both directions
- Accessibility trio (user-scalable, labels)
- Legal copy final (entertainment opener, Original Works, AI-Assisted)
- **narrate Edge Function rate-limited (5/min + 20/hr per IP)** ← Apr 29
- **Static manifest.json (replaces blob URL)** ← Apr 29
- **Account deletion mechanism (in-app, working)** ← Apr 29
- **Data export mechanism (POPIA/GDPR right of access)** ← Apr 29
- **Magic-link email redesigned + applied** ← Apr 29
- **Migration history reconciled (profiles table now committed)** ← Apr 29

### ⏳ TO DO — pre-launch

**Code:**
- [ ] **Google OAuth 2.0** (~2-3 hrs) — Google Cloud Console OAuth credentials, Supabase provider config, frontend "Continue with Google" button + callback handling, DOB-only follow-up form. Reasoning: removes magic-link-on-mobile fragility (Gmail internal browser issue), brand trust signal.
- [ ] **Dodo webhook Edge Function** (~1 hr after Dodo approval) — receives payment confirmation, sets `has_paid=true`
- [ ] **`launchDodo()` swap** (~30 min after Dodo approval) — replaces `launchPayFast()`
- [ ] **26-line MoR wording swap** (after Dodo approved + entity name confirmed)
- [ ] **E2E payment test** → refund to self
- [ ] **Real PNG icons in manifest** (192/512/maskable, plus apple-touch-icon, favicon) — needs cube icon designed first

**Non-code (Ronnie solo):**
- [ ] **Cube icon designed in Canva Pro** (~30 min attempt; if doesn't land, Fiverr ~$50, post-launch acceptable)
- [ ] **Social media handles claimed** across 6 platforms (~30 min, after logo done)
- [ ] **Magic-link email PNG wordmark upgrade** (post brand-folder-deployed, swap inline text for hosted PNG)

**Backend cleanup:**
- [ ] **Delete 9+ test profile rows** from Supabase profiles table before launch
- [ ] **Resend deliverability tested** to fresh Gmail, Outlook, Yahoo accounts

### ⏳ TO DO — UX polish (not launch-blocker)
- [ ] **Settings discoverability** — currently the Settings link is only on the signup screen. Add a settings gear ⚙️ icon visible to signed-in users so they can reach Delete Account / Sign Out without first signing out. ~30 min, slot into Google OAuth session or post-launch.
- [ ] Sentry error monitoring (~20 min)
- [ ] At least 5 smoke tests against live site

---

## 🪨 FRAGILE AREAS — DO NOT TOUCH CASUALLY

- **Service worker is a real file now** (`sw.js`). Do NOT revert to blob URL — Android Chrome 117+ rejects blob SW silently.
- **Static manifest.json is a real file now** (`docs/manifest.json`). Do NOT revert to blob URL — PWABuilder cannot read blob URLs.
- **`@media (min-width:600px)` rules** are desktop-only on mobile — any CSS change inside those media queries is invisible on Ronnie's phone. Base rules apply to mobile.
- **BSD sed can't do multi-line replacements** — use Python one-shot. Never iterate.
- **`grep -c` returns exit 1 on zero matches** — kills pipelines silently. Use `|| true`.
- **`head -N` piped after `git log` can trigger SIGPIPE (exit 141)** on macOS. Use `|| true`.
- **Service worker cache bump is mandatory** every commit that changes `docs/app.html`.
- **PWA cache stickiness:** "it's not working on my phone" is usually cache or SW install timing, not code.
- **Magic-link must open in main Chrome**, not Gmail's internal browser.
- **Never reintroduce base64 assets** — 10.8MB cleanup reduced file from 11MB to ~349KB.
- **Life Phases is sequential playback** via `playSequence`. Do not convert to 3 separate cards.
- **Master numbers in NUM.pc are stripped** (commit `636e3d8`). Do not re-add.
- **renderAllContent reveal blocks MUST stay gated on `if(isUnlocked){}`** — removing the gate re-introduces paywall bypass.
- **GitHub Pages source is `/docs` directory.** Do NOT add HTML to repo root expecting it to be served.
- **`docs/CNAME` binds the custom domain.** Removing it breaks `quantumcube.app`.
- **Cursor's verbatim grep output can occasionally glitch.** Verify via fresh `grep` OR `git cat-file` before reverting.
- **JWTs / bearer tokens NEVER paste into Cursor or chat** — debug via DevTools console + Promise.race timeout patterns instead. Cursor's refusal on Apr 29 was correct.
- **`auth.admin.deleteUser` can hang the calling session's `signOut`** — always wrap signOut in Promise.race(signOut, 3000ms) when calling delete from the user's own session.
- **Edge Functions need `verify_jwt = false` in `supabase/config.toml`** if they handle JWT manually — otherwise Supabase returns 401 before the function runs.

### Supabase CLI gotcha
- `supabase db execute --project-ref` does not exist
- Use `supabase db query --linked "SQL"` from linked project directory
- `supabase functions logs` requires CLI v2.95+ (we have v2.90.0). Use dashboard for logs.
- For CSV output: `-o csv`, NOT `--csv`

---

## WHAT'S LEFT — ORDERED BY PRIORITY (Apr 29 update)

### 🚨 LAUNCH-BLOCKING

1. **Dodo Payments approval** (24-72hr pending)
2. **Cube icon design** (Canva Pro, then if needed Fiverr) — needed for both manifest icons + social media
3. **Real PNG icons in manifest** (192/512/maskable) — needs #2 first
4. **Social media handles claimed** — needs #2 first
5. **Google OAuth 2.0** (~2-3 hrs)
6. **Dodo wiring + 26-line MoR swap** — needs #1 first
7. **E2E payment test** — needs #6 first
8. **Delete 9 test profile rows**

### ⚠️ HIGH-VALUE (not launch-blocker)
- Settings discoverability fix
- Sentry error monitoring
- Email re-verification UX

### 🧹 POST-LAUNCH CLEANUP
- Split `docs/app.html` into .js + .css files
- `git gc --aggressive` — .git folder is 1.2 GB
- Login loop fix (same-email resign triggers new magic link)
- HeyGen cleanup (Academy side)
- Brain + CPU chip icon (designer)

### 📝 POST-LAUNCH FOLLOW-UPS
- Astrology/Chinese 3-variant versions
- Face 5 narrative opener variations
- Additional music tracks
- Marketing email pipeline + unsubscribe endpoint
- DMARC `p=none` → `p=quarantine` after 2 weeks clean
- Gmail 2FA on all 3 partner accounts
- Analytics, social proof, sharing

### 🏪 APP STORE SUBMISSIONS
- **Google Play:** $25 one-time, PWABuilder → .aab (after Dodo live + cube icon designed)
- **Apple App Store:** $99/year, Capacitor wrap, Xcode archive (deferred — revisit post-Google-Play launch)

---

## INFRASTRUCTURE LIVE
| System | State |
|---|---|
| GitHub Pages | Live (source: `/docs` on `main`. SW **qc-v147**, narration **qc-narration-v2**) |
| **quantumcube.app** | LIVE — landing + 8 legal + /app, all HTTP 200 ✓ |
| qncacademy.com | Full email stack live |
| Google Workspace | admin@qncacademy.com + 5 aliases |
| Cloudflare Email Routing | *@quantumcube.app → admin@qncacademy.com |
| Cloudflare DNS | CNAME quantumcube.app → quantumneurocreations-dot.github.io ✓ |
| Resend | Verified, SMTP in Supabase |
| ElevenLabs | Valory, narrate deployed, usage-based billing enabled |
| Supabase | Frankfurt, free tier, RLS verified, 3 Edge Functions deployed (narrate / delete-account / export-data) |
| **Dodo Payments** | **Application pending — 24-72hr review** |

---

## 🎙️ EDGE FUNCTIONS — current state

### `narrate` (rate-limited Apr 29)
- Voice: Valory (`VhxAIIZM8IRmnl5fyeyk`), model `eleven_turbo_v2_5`
- Rate limit: per-IP via Postgres RPC (`narrate_rate_limit_try`), 5/min + 20/hr
- 2500-char input cap, JWT validation (manual via apikey header check)
- ONLY credit-burn path at runtime (Face 5 only)

### `delete-account` (Apr 29)
- Verifies user JWT via `getUser(jwt)`
- Calls `auth.admin.deleteUser(userId)` server-side using service-role key
- Cascades to `public.profiles` via `on delete cascade` FK
- Logs deletion server-side (id + timestamp, no email)
- Frontend wraps signOut in Promise.race(3000ms) to prevent hang

### `export-data` (Apr 29)
- Verifies user JWT
- Returns profile JSON with Content-Disposition attachment header
- POPIA Section 23 / GDPR Article 15 compliance (right of access)

All three: `verify_jwt = false` in config.toml + manual JWT handling + CORS headers + service-role key from Edge Function env vars.

---

## 🔊 AUDIO + TECH STACK — unchanged from v24
See v24 sections (LOCKED). No changes Apr 29.

---

## 📧 EMAIL INFRASTRUCTURE — unchanged from v24 except magic-link template applied

- Resend admin@qncacademy.com, domain `quantumcube.app` verified
- eu-west-1, free tier 3000/mo, 100/day
- DNS: DKIM, SPF, DMARC (p=none), MX send subdomain
- Supabase SMTP: `noreply@quantumcube.app`, `smtp.resend.com:465`, 60s min interval
- **Magic-link HTML applied Apr 29** ← preview confirmed in Supabase dashboard

Pending: PNG wordmark upgrade for magic-link email (post brand-folder-deployed).

---

## 🧪 SUPABASE BACKEND
- **Project:** quantum-cube (ref `fqqdldvnxupzxvvbyvjm`)
- **Region:** Central EU (Frankfurt)
- **Schema:** `public.profiles` (committed migration: `20260417104424_create_profiles_table_and_rls.sql`)
  - id, email, has_paid, marketing_consent, created_at
  - 3 RLS policies: select_own, update_own (with `has_paid` column lock), insert_own
  - `handle_new_user` trigger auto-creates profile on auth signup
- **Schema (Apr 29):** `public.narrate_rate_counters` + `narrate_rate_limit_try` RPC
- **Edge Functions:** narrate ✓, delete-account ✓, export-data ✓. Dodo webhook pending.

### Test / team data in profiles (DELETE BEFORE LAUNCH)
Snapshot from Apr 23 sweep. Re-snapshot in next session — may have drifted:
- `admin@qncacademy.com` (team, unpaid)
- `charlheyns1@gmail.com` (unpaid)
- `booyens.michelle@gmail.com` (Michelle, unpaid)
- `keyzer@xtremeprop24.com` (Keyzer, unpaid)
- `quantumneurocreations@gmail.comcom` ← typo, delete anytime
- `test+chunk5b@qncacademy.com` (unpaid)
- `carlkelbrick+test@gmail.com` (unpaid)
- `rkelbrickmail@gmail.com` (unpaid)
- `carlkelbrick@gmail.com` (paywall test profile — keep until E2E payment test done)
- `quantumneurocreations@gmail.com` (paid test — keep for testing)

---

## 🔐 AUTH + UNLOCK FLOW

### Session handling — unchanged from v24

### Unlock state — 4-layer defence (added DB layer Apr 29)
1. STORE_KEY user-scoped
2. checkStoredUnlock matches stored id to session id
3. syncUnlockFromProfile unconditionally enforces lock for unpaid
4. renderAllContent gates on `isUnlocked`
5. **DB-level RLS prevents user from updating own `has_paid`** ← surfaced to brief Apr 29 (was always there in migration `20260417104424`, just not documented)

### Account deletion (NEW Apr 29)
- Two-tap confirmation pattern (5-second arm window)
- Edge Function admin-deletes user via service-role key
- Cascade FK wipes profile row automatically
- Frontend wipes 6 localStorage keys
- Promise.race signOut(3000ms) prevents hang
- Redirects to `/` (landing) on completion
- Verified working end-to-end Apr 29

### Data export (NEW Apr 29)
- Single-tap from Settings (Face 7)
- Returns JSON with email, has_paid, marketing_consent, timestamps
- Browser downloads as `quantum-cube-data.json`
- POPIA right of access compliance

---

## NEXT SESSION STARTING POINT

1. Attach PROJECT_BRIEF.md (v25) + CHAT_KICKOFF.md to new chat
2. Start a fresh Cursor chat alongside (or continue current if context clean)
3. **Minimal health check:** confirm HEAD on `origin/main`, SW = qc-v147, all 4 live URLs return 200
4. **Check Dodo Payments approval status** — has Michelle heard back?
5. **If Dodo approved:** start payment integration session (webhook + launchDodo + MoR swap + E2E test)
6. **If Dodo still pending:** parallel work options:
   - Google OAuth 2.0 implementation (~2-3 hrs code)
   - Cube icon in Canva Pro (Ronnie solo)
   - Settings discoverability fix (~30 min code)
7. Re-snapshot test profile rows in case list has drifted
8. Update brief at end of session if meaningful drift

---

### Lessons learned (running, updated Apr 29)
- **PWA cache stickiness is the #1 false alarm.** Always check live site in regular Chrome before debugging code.
- **JWTs never go through Cursor/chat.** Cursor's refusal Apr 29 was correct. Diagnose via DevTools console + defensive timeouts (Promise.race) instead of curl tests with real tokens.
- **`auth.admin.deleteUser` can hang the calling session's `signOut`.** Wrap signOut in Promise.race(3000ms) when calling delete from the user's own session.
- **Diagnostic console.logs are scaffolding, not production code.** Always rip them in a follow-up commit. Don't ship debug noise.
- **Cursor's anchor mismatches are common.** Cursor self-corrects against actual file content. Welcome the corrections — they catch real bugs in our paste blocks.
- **Edge Functions need `verify_jwt = false` if they handle JWT manually.** Otherwise Supabase 401s before the function runs.
- **Supabase Edge Functions don't expose `Deno.openKv()`.** Use Postgres RPC for state instead.
- **Paddle is definitively out for esoteric content.** AUP explicitly prohibits "fortune-telling/horoscopes/clairvoyance".
- **Dodo Payments actively markets to astrology brands.** Better category fit than the more general MoRs.
- **Today's wins compound: each launch-blocker shipped tightens the path to revenue.** April 29 took us from 4 hard blockers to 2 (Dodo + cube icon).
