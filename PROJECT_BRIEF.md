# QUANTUM CUBE — MASTER PROJECT DOCUMENT
**Version: v14 | Last Updated: April 18, 2026 (evening)**

---

## ⚠️ CRITICAL RULE — ALWAYS READ FIRST
**Quantum Cube and QNC Academy are COMPLETELY SEPARATE projects.**
- Never mix code or files between them
- Quantum Cube lives on GitHub Pages
- Quantum Cube has its own Supabase project (Frankfurt) — never touch the Academy one (Ireland)
- Always confirm which project you are working on before making any changes

---

## 🚦 NEW CHAT? READ CHAT_KICKOFF.md FIRST
The kickoff doc handles session startup, role split between Chat Claude and Cursor Claude, and the golden rules. Read it first, then read this brief for project-specific context.

---

## TEAM
- **Ronnie (Willem Pretorius)** — creator, design, programming, tech lead
- **Michelle** — admin, content review, QA
- **Keyzer** — marketing, finance, payments
- Equal 3-way partnership
- Faceless brand: public only sees `admin@qncacademy.com` and `info@qncacademy.com`

---

## FILE LOCATIONS
/Users/qnc/Projects/quantumcube/              <- MAIN PROJECT FOLDER
|- quantum-cube-v10.html                      <- THE APP (~11 MiB, ~2870 lines)
|- PROJECT_BRIEF.md                           <- This document
|- CHAT_KICKOFF.md                            <- Chat operating protocol
|- cube-background.jpg                        <- Milky Way background (in repo)
|- .supabase-env                              <- Supabase + Resend creds (gitignored)
|- .cursorignore                              <- Cursor indexing rules (committed)
|- .gitignore                                 <- Git ignore rules (committed)
|- supabase/                                  <- Supabase CLI linked project (.temp gitignored)
|- Sounds/                                    <- Audio assets (committed now — see below)
|- Cube Sides/                                <- Cube face images (gitignored - embedded in HTML)
|- Videos/                                    <- Video local backups (gitignored)
|- audio/                                     <- Audio files
|- screenshots/                               <- Audit screenshots (gitignored)
|- .bak-                                    <- Rewrite script backups (gitignored)

**GitHub Repo:** https://github.com/quantumneurocreations-dot/quantumcube
**Live URL:** https://quantumneurocreations-dot.github.io/quantumcube/quantum-cube-v10.html
**Custom domain (registered, not yet pointed):** https://quantumcube.app

---

## DEV ENVIRONMENT (M4 Mac Mini)
| Item | Detail |
|------|--------|
| Machine | Mac Mini M4 |
| Username | qnc |
| Project path | /Users/qnc/Projects/quantumcube |
| Editor | Cursor (Claude agent) + Terminal |
| GitHub CLI | gh v2.89.0 — authenticated as quantumneurocreations-dot |
| SSH Key | ED25519 ~/.ssh/id_ed25519 |
| Node.js | v24.15.0 (LTS) via nvm, npm v11.12.1 |
| Python | 3.9.6 (system) |
| cwebp | v1.6.0 via Homebrew |
| Supabase CLI | v2.90.0 — logged in, repo linked to quantum-cube |
| Vercel CLI | v51.5.0 — logged in as quantumneurocreations-5422 |
| Cursor settings | File-Deletion Protection ON; External-File Protection ON; Auto-Run in Sandbox |

---

## TECH STACK
- **Frontend:** Single HTML file, vanilla JavaScript, CSS3 3D transforms, glassmorphism
- **Fonts:** Cinzel Decorative (logo), Cinzel (labels/UI), Cormorant Garamond (body text)
- **Auth:** Supabase magic-link (email OTP), SDK v2.45.4 via UMD CDN
- **Database:** Supabase Postgres (Frankfurt) — `public.profiles` with RLS
- **Email:** Resend via custom SMTP on Supabase (unlimited)
- **Payment:** PayFast sandbox currently wired — Paddle swap Monday April 20
- **Videos:** Vimeo Player API — native real fullscreen only
- **Audio:** 5 base64 embedded (currently disabled) + 2 lightsaber MP3s extracted to Sounds/ (cube touch FX, silenced)
- **Haptics:** window.haptic('light'|'medium'|'success') — wired on all major interactions
- **Hosting:** GitHub Pages
- **PWA:** Web manifest, service worker (cache: qc-v41)

---

## 🔁 PAYMENT PROCESSOR CHANGE — MONDAY APRIL 20
- **Old:** PayFast, $8, SA-only
- **New:** Paddle, $17, global (Merchant of Record — handles VAT/GST internationally)
- **Why $17:** Paddle minimum rules out $8. 1+7=8 in numerology (wealth number)
- **Status:** All visible UI prices show $17. `launchPayFast()` function still wired under the hood — Monday rewrites its body to call Paddle
- **Monday tasks:** Paddle account (team meeting), webhook Edge Function, rewrite `launchPayFast()`, update legal docs, remove PayFast refs, E2E test

---

## 📧 EMAIL INFRASTRUCTURE — Resend
Custom SMTP replaces Supabase's 2/hour free-tier limit.

- **Resend account:** admin@qncacademy.com (Google SSO)
- **Domain:** quantumcube.app — verified
- **API key:** domain-restricted, sending-only, stored in `.supabase-env` as `RESEND_API_KEY`
- **Region:** eu-west-1 (Ireland)
- **Free tier:** 3000 emails/month, 100/day

**DNS records on quantumcube.app (Cloudflare):**
- TXT `resend._domainkey` — DKIM
- MX `send` priority 10 → `feedback-smtp.eu-west-1.amazonses.com`
- TXT `send` — SPF (`v=spf1 include:amazonses.com ~all`)
- TXT `_dmarc` — DMARC monitor (`v=DMARC1; p=none;`)

Coexist cleanly with existing Cloudflare Email Routing at root `@`.

**Supabase SMTP config:**
- Sender: `noreply@quantumcube.app` (display name "Quantum Cube")
- Host: `smtp.resend.com:465`, user `resend`, password = RESEND_API_KEY
- Min interval between emails: 60 seconds

**Known cosmetic issue:** magic-link emails technically route via `send.quantumcube.app` subdomain. Fix post-launch: configure Resend return-path.

---

## APP STRUCTURE — 7 FACES + INTERSTITIAL
| Face | Name | Notes |
|------|------|-------|
| Face 0 | Entry / Sign Up Form | |
| faceCheckEmail | Interstitial — "Check Your Email" | 3 lines (Check Your Email / A Sign-In Link Was Sent / Click On The Link To Verify Your Email) inside glass-card, all form-title style. Resend button (60s cooldown) + Back to Sign Up card button |
| Face 1 | Introduction video | Auto-advance destination after magic-link SIGNED_IN |
| Face 2 | Results Explained videos | |
| Face 3 | Numerology Results | Locked until has_paid |
| Face 4 | Astrology & Horoscope | Locked until has_paid |
| Face 5 | Combined Results | Locked until has_paid |
| Face 6 | Complete / Outro video | |
| Face 7 | Settings (Sign Out + Back) | Reached via Settings link in Face 0 legal footer |

---

## VIMEO VIDEOS
Privacy: Hide from Vimeo. Downloads OFF. Comments OFF.

| Face | Title | Vimeo ID | Shape |
|------|-------|----------|-------|
| Face 1 | 1 - Introduction | 1183086210 | Portrait (9:16) |
| Face 2 | 2 - Numerology Explained | 1183086853 | Landscape (16:9) |
| Face 2 | 3 - Results Explanation | 1183087269 | Landscape (16:9) |
| Face 2 | 4 - Astrology | 1183087951 | Landscape (16:9) |
| Face 6 | 5 - Cube Outro | 1183103519 | Portrait (9:16) |

**Video behaviour (UPDATED April 18):**
- Real fullscreen only (Vimeo native) — no more fake CSS fullscreen
- On play: unlock orientation, enter fullscreen, lock to landscape (landscape videos) or portrait (portrait videos)
- On exit fullscreen: re-lock portrait
- Exit via Vimeo's own controls (built-in). No custom × button needed.
- 2px black border on video containers, cyan top-gradient removed

---

## VISUAL DESIGN — KEY DECISIONS (DO NOT CHANGE)
- Background: Milky Way image + CSS starfield (220 stars)
- Cube: Glass effect, cyan-white glowing edges 2px, clean glass faces
- Cube faces (NEW): No giant center number. 4 small corner numbers per face (13px Cinzel Decorative, matches label) + 4 thin cyan edge lines inset 28px from corners so they never touch the numbers.
- Cube hint text: "rotate the cube / tap a side to open" — 10px Cinzel, 2px letter-spacing, two lines
- Logo: QUANTUM top, CUBE right-aligned inline-block, CUBE cyan with glow + float
- All cards: glass style, NO margin overrides (centered via face-container padding — see Layout below)
- Lock screens: "Complete Quantum Cube Unlock" title, stacked bullets (9 Numerology / 5 Western Astrology / 5 Chinese Horoscope / & / Combined Interpretation), $17.00, cyan-glow UNLOCK button. Margin normalized to 0 — centered by parent.
- Payment overlay: matched `#globalLogo` at top (32px 0 8px padding), two-line title, same bullets as lock card, $17 + stacked meta, cyan-glow Pay $17 button, white-outline Back to Cube button (exact size match to Pay). Bottom padding trimmed to 20px.
- Audio buttons: Music bottom-right, Voice bottom-LEFT (moved from right). Pill shape, reveal label on scroll, 30% idle opacity. **⚠ Architecture being reconsidered — see Tomorrow's starting point.**
- Legal footer on Face 0: Terms + Disclaimer + Settings (Settings signed-in only)
- Month dropdown: numbers 1-12
- PWA orientation: portrait locked, unlocks during landscape video play

**LAYOUT — CRITICAL (added April 18):**
- `.face` padding is now symmetric `24px 18px 0 18px` (was `24px 18px 0 0` — the 0 on left caused everything to drift left visually vs truly-centered elements like the logo).
- `.video-face` margin normalized to `0 0 16px 0` (was `0 16px 16px 32px` — old compensation trick, no longer needed).
- `.lock-screen` margin normalized to `0 0 20px 0` (was `0 16px 20px 32px` — same reason).
- If a future element looks off-center, check its own margins BEFORE touching face padding.

**BUTTON SIZES (bumped April 18):**
- `.calc-btn`, `.unlock-btn`, `.reset-btn`, `.pay-back` all use `font-size:clamp(11px,3vw,13px)` and `letter-spacing:clamp(3px,1.5vw,5px)` (previously 9-11 / 2-4).
- `.pay-overlay-btn` no longer has a `letter-spacing:6px` override — inherits clamp so Pay $17 matches other CTAs.

---

## 🪨 HAPTIC MAP — shipped April 18
Global helper: `window.haptic(type)` where type = `'light'` (25ms), `'medium'` (40ms), `'success'` ([30, 80, 30]).

| Trigger | Type |
|---|---|
| Cube touch (drag start) | light |
| Category card open (icard toggle) | light |
| Reveal My Cube button | medium |
| Resend Email button | medium |
| Back to Sign Up buttons (both) | medium |
| All Unlock buttons (4) | medium |
| Pay $17 button | medium |
| Back to Cube button | medium |
| Payment success (applyUnlockedState animate path) | success |

Silent on iOS (Safari doesn't expose navigator.vibrate) — graceful fallback.

---

## 🔊 AUDIO ASSETS — status April 18
**Extracted from base64 into `Sounds/` folder (committed):**
- `bgMusic.mp3` — ambient music (Dream Focus Beta Waves)
- `openSound.wav` — face open sound
- `selectSound.wav` — selection
- `pop1.mp3`, `pop2.mp3` — UI pops
- `ES_Lightsaber, Swing, Electronic Hum 04 - Epidemic Sound.mp3` — cube touch FX
- `ES_Scifi, Weapon, Lightsaber, Swing, Electronic Hum - Epidemic Sound.mp3` — cube touch FX

**Current state:**
- Cube touch sound (random between 2 lightsaber MP3s) is **wired but silenced** at `/* a.play().catch(...) */`
- The 5 original sounds are still base64-embedded in HTML at lines ~828-832 (`this._bgMusic`, `this._openSound`, `this._selectSound`, `this._pop1`, `this._pop2`). Not yet rewired to load from Sounds/ folder.
- Cleanup pending: base64 → file references (will significantly shrink HTML).

---

## SUPABASE BACKEND
- **Project:** quantum-cube (ref `fqqdldvnxupzxvvbyvjm`)
- **Region:** Central EU (Frankfurt) — POPIA/GDPR aligned
- **Org:** Quantum Neuro Creations (`ybhwpcakkaveapdztnrs`)
- **Credentials:** `.supabase-env` (gitignored) — SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_PROJECT_ID, RESEND_API_KEY

### Schema — `public.profiles`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK, references `auth.users.id` |
| email | text | |
| has_paid | boolean | Immutable from client — only service role can flip |
| marketing_consent | boolean | From user_metadata at signup |
| created_at | timestamptz | |

### RLS Policies (verified April 18)
- RLS enabled
- `users_select_own_profile` — SELECT where `auth.uid() = id`
- `users_insert_own_profile` — INSERT backup
- `users_update_own_profile` — UPDATE with `has_paid` locked
- No DELETE policy

### Trigger
- `on_auth_user_created` → `handle_new_user()` (SECURITY DEFINER)

### Auth Config
- Site URL: GitHub Pages URL
- Redirect URLs: GitHub Pages + quantumcube.app
- Magic-link only, session persists until explicit sign-out
- Custom SMTP via Resend

### Edge Functions
None deployed. Paddle webhook is Monday's work.

### Test data in profiles (delete before launch)
- `quantumneurocreations@gmail.com`
- `rkelbrickmail@gmail.com`
- `carlkelbrick@gmail.com`
- Any `test+*@qncacademy.com`

---

## FRONTEND WIRING — SHIPPED

### Key line refs (April 18 evening — use grep, numbers drift)
| What | Approx line |
|---|---|
| Supabase UMD script tag | ~443 |
| SUPABASE_URL / ANON_KEY / client | ~445–447 |
| Loading screen (#loadingScreen) | ~463 |
| Face 0 div open | ~531 |
| faceCheckEmail interstitial | ~549 (3 form-title lines inside glass-card) |
| Resend Email button | ~560 |
| Face 1 Back to Sign Up (reset-btn) | ~586 |
| window.haptic definition | ~1100 |
| _cubeTouchSounds array | ~1100 (same line as haptic) |
| playCubeTouchFX function | ~1100 |
| Two-finger twist block | ~1154 |
| Audio button scroll-reveal IIFE | ~1134 |
| DOMContentLoaded cube-corner injector | before onDragStart |
| STORE_KEY const | ~1890 |
| has_paid check | ~1905 |
| applyUnlockedState | ~1975 |
| launchPayFast notify placeholder | ~1981 |
| signInWithOtp | ~2155 |
| handleBackToSignUp | ~2230 |
| **function runCalculation** | **~2333** |
| onAuthStateChange | ~2206 |
| Vimeo fullscreen block | ~2505 |
| #payOverlay | ~2825 |
| SW code string | ~2643 |

**Always grep before editing — these drift.**

---

## WHAT STILL NEEDS TO BE DONE

### 🚀 Monday / Tuesday (launch-blocking, needs team)
- [ ] Paddle account application
- [ ] Paddle webhook Edge Function
- [ ] Rewrite `launchPayFast()` body → call Paddle checkout
- [ ] Replace placeholder notify URL
- [ ] Remove `PF_CONFIG.amount = "88.00"` or repurpose
- [ ] Update legal docs: remove all PayFast refs, add Paddle + Resend
- [ ] E2E test: signup → magic link → Paddle payment → has_paid flips → unlock persists
- [ ] Delete test rows from profiles table

### ⚙️ Sunday (remaining weekend work)
- [ ] User re-test of signup → interstitial → magic link flow with fresh emails
- [ ] Age gate on signup (DOB ≥ 18)
- [ ] Paddle prep doc for Monday team meeting (business entity, bank, tax ID, product URL, checkout flow)
- [ ] **Audio button architecture redesign** — see "Next Session" below

### 📝 After-launch follow-ups
- [ ] Narrator button → ElevenLabs (reuse Academy API key) — triggered from Voice button inline on Faces 3/4/5
- [ ] Re-enable audio: rewire base64-embedded sounds to load from Sounds/ folder, test playback, music pause/resume on video play
- [ ] Marketing email pipeline + unsubscribe endpoint (Privacy Policy promises this)
- [ ] Brand the Supabase magic-link email (currently plain default)
- [ ] Fix Resend return-path: `@send.quantumcube.app` → display `@quantumcube.app`
- [ ] App stores — Google Play (PWABuilder → .aab → $25); Apple (Capacitor → Xcode → $99/yr)
- [ ] Social proof / testimonials section
- [ ] Sharing mechanism for readings
- [ ] Analytics
- [ ] Profile deletion Edge Function
- [ ] Dead CSS cleanup: `.pay-btn`, `.pay-btn-alt`, `.pay-price-lines span`, `.demo-btn`, `.pay-back` (still used by Continue button on success screen — rename for clarity?)
- [ ] Remove inert `AUDIO._updateMuteBtn` helper (mute button deleted)
- [ ] Fix iframe `allow`/`allowfullscreen` console warning (5 iframes)
- [ ] Gmail aliases propagation check + 2FA on all 3 partner accounts
- [ ] DMARC tighten p=none → p=quarantine after 2 weeks clean reports
- [ ] Migrate business services: `quantumneurocreations@gmail.com` → `admin@qncacademy.com`

### 📦 Content complete
- [x] Content variations (all 9 numerology categories, 3 variations each)
- [x] Content accuracy review (numerology + Western + Chinese zodiac verified)

---

## INFRASTRUCTURE LIVE (end of April 18)

| System | State |
|---|---|
| GitHub Pages | Live, serving latest HTML commit (SW v41) |
| quantumcube.app | Registered (Cloudflare), DNS managed, not yet pointed at Pages |
| qncacademy.com | Registered (Cloudflare), full email auth stack live |
| Google Workspace | admin@qncacademy.com active, 5 aliases |
| Gmail filters | 5 rules auto-label by recipient |
| Cloudflare Email Routing | *@quantumcube.app → admin@qncacademy.com |
| Resend | Domain verified, API key live, SMTP in Supabase, DNS propagated |
| Supabase | quantum-cube (Frankfurt), free tier, profiles RLS verified |

---

## ANNUAL RUNNING COST
- Google Workspace: ~R1,340/year
- qncacademy.com renewal: ~R200/year
- quantumcube.app renewal: ~R275/year
- Resend: free tier
- **Total: ~R1,815/year (~R150/month)**

Excludes Paddle fees (~5% + $0.50/tx), Supabase paid tier if scaled, ElevenLabs narrator.

---

## SEPARATE PROJECT — QNC ACADEMY
- Path: /Users/qnc/Projects/qnc-academy/
- Stack: Next.js + Vercel + Supabase + ElevenLabs + GitHub
- URL: qnc-academy.vercel.app
- Supabase: SEPARATE project (Ireland) ref `bevaepokvavzmykjmhda`
- **Never mix with Quantum Cube chats or code.**

---

## SESSION LOG — April 18, 2026 (second session, evening)

41 commits shipped in this session. Headlines by theme:

**Videos — settled on native Vimeo real fullscreen:**
- Removed real-fullscreen trigger, then re-added it (native-only)
- Added × overlay, then removed it (Vimeo's own controls are enough)
- Forced landscape orientation lock on landscape videos, portrait on portrait
- 2px black border, removed cyan top-gradient
- Fixed `Video-container` typo on Face 6 outro

**Cube interactions:**
- Two-finger twist → Z-axis rotation (one-finger drag unchanged)
- Haptic system (`window.haptic`) wired across all major CTAs
- Cube touch random lightsaber sound FX (wired, silenced)
- Extracted 5 base64 audio files to Sounds/ folder

**Cube visual:**
- Deleted giant center number
- Added 4 small corner numbers per face (matches label size)
- Added 4 thin cyan edge lines inset from corners
- Cube hint text: two lines, non-bold, 10px

**Audio buttons (provisional — to revisit):**
- Removed mute button entirely
- Music + Voice as pill buttons with scroll-reveal labels
- Voice moved bottom-left, Music bottom-right
- **User feedback: scroll-reveal is distracting during reading. Plan for tomorrow: relocate Voice inline with Faces 3/4/5 results, Music stays bottom-right at 30% always.**

**Layout / centering — the big fix:**
- Root cause identified: `.face` padding was `24px 18px 0 0` (0 left, 18 right)
- Workarounds on `.video-face` and `.lock-screen` used asymmetric margins to compensate
- Fixed at root: face padding now symmetric 18/18, video/lock-screen margins normalized to 0
- Everything now truly centered

**Pay overlay polish:**
- Logo gap matched to Face 0 (32px 0 8px)
- Legal footer matches other faces (Terms + Disclaimer, `.legal-footer` class)
- Back to Cube → white-outline card exactly matching Pay $17 size
- Bottom padding trimmed 60px → 20px
- Pay button letter-spacing override removed (inherits clamp)

**Buttons global:**
- Font-size bumped `clamp(9px,2.5vw,11px)` → `clamp(11px,3vw,13px)`
- Letter-spacing bumped `clamp(2px,1.2vw,4px)` → `clamp(3px,1.5vw,5px)`

**Interstitial:**
- Back to Sign Up upgraded to white-outline reset-btn card
- "Check Your Email" moved inside glass-card
- Two body lines replaced with "A Sign-In Link Was Sent To Your Email" and "Click On The Link To Verify Your Email", all three form-title style

### Lessons learned this session
- BSD sed on macOS doesn't handle multi-line replacements cleanly — Cursor Claude correctly shifted to Python one-shots when needed, which was the right call.
- `grep -c` with 0 matches exits 1 and kills pipelines — use `|| true` on verify greps.
- When elements look "off center", check each element's own margins BEFORE touching the root container. Workarounds stack and eventually collide.

---

## NEXT SESSION STARTING POINT

**Hot item — audio button architecture redesign:**
User proposed (and we agreed) to scrap the scroll-reveal approach. New plan:
- **Voice button**: appears INLINE with content only on Faces 3/4/5 (where there's interpretation text to narrate). Alongside the "Your Interpretations" section header on each. Scrolls naturally with content.
- **Music button**: one persistent spot, fixed bottom-right, always at 30% opacity, no reveal behaviour. Toggle once per session.
- Remove the current fixed bottom-left/bottom-right buttons and scroll-reveal IIFE. Remove pill styling.

**Other Sunday work:**
1. User re-test with fresh emails (signup → interstitial → magic link flow)
2. Age gate on signup (DOB ≥ 18)
3. Paddle prep doc for Monday team meeting

**Monday:** Paddle team meeting, then webhook Edge Function.

**First action of next chat:** attach this brief + CHAT_KICKOFF.md, run the minimal health check (see kickoff), then jump into the audio button redesign.
