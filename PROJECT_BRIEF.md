# QUANTUM CUBE — MASTER PROJECT DOCUMENT
**Version: v15 | Last Updated: April 19, 2026 (evening)**

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
|- quantum-cube-v10.html                      <- THE APP (~11 MiB, ~2978 lines)
|- PROJECT_BRIEF.md                           <- This document
|- CHAT_KICKOFF.md                            <- Chat operating protocol
|- cube-background.jpg                        <- Milky Way background (in repo)
|- .supabase-env                              <- Supabase + Resend creds (gitignored)
|- .cursorignore                              <- Cursor indexing rules (committed)
|- .gitignore                                 <- Git ignore rules (committed)
|- supabase/                                  <- Supabase CLI linked project (.temp gitignored)
|- Sounds/                                    <- Audio assets (committed)
|- Cube Sides/                                <- Cube face images (gitignored — cube faces are now text + lines ONLY, no images)
|- Videos/                                    <- Video local backups (gitignored)
|- audio/                                     <- Audio files
|- screenshots/                               <- Audit screenshots (gitignored)
|- .bak-                                      <- Rewrite script backups (gitignored)

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
- **Audio:** 5 base64 embedded (currently disabled) + 2 lightsaber MP3s extracted to Sounds/ (cube touch FX, silenced). ElevenLabs narrator NOT yet wired.
- **Haptics:** window.haptic('light'|'medium'|'success') — wired on all major interactions
- **Hosting:** GitHub Pages
- **PWA:** Web manifest, service worker (**cache: qc-v99**)

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
| faceCheckEmail | Interstitial — "Check Your Email" | 3 form-title lines inside glass-card. Resend button (60s cooldown) + Back to Sign Up card button |
| Face 1 | Introduction video | Auto-advance destination after magic-link SIGNED_IN |
| Face 2 | Results Explained videos | |
| Face 3 | Numerology Results | Locked until has_paid. Voice button below matrix grid. |
| Face 4 | Astrology & Horoscope | Locked until has_paid. Voice button below astro-grid. |
| Face 5 | Combined Results | Locked until has_paid. Voice button above "Your Complete Portrait" header. |
| Face 6 | Complete / Outro video | |
| Face 7 | Settings (Sign Out + Back) | Reached via Settings link in Face 0 legal footer |

---

## VIMEO VIDEOS
Privacy: Hide from Vimeo. Downloads OFF. Comments OFF.

| Face | Title | Vimeo ID | Shape |
|------|-------|----------|-------|
| Face 1 | 1 - Introduction | 1183086210 | Portrait (9:16) — container 75% wide |
| Face 2 | 2 - Numerology Explained | 1183086853 | Landscape (16:9) |
| Face 2 | 3 - Results Explanation | 1183087269 | Landscape (16:9) |
| Face 2 | 4 - Astrology | 1183087951 | Landscape (16:9) |
| Face 6 | 5 - Cube Outro | 1183103519 | Portrait (9:16) — container 75% wide |

**Video behaviour:**
- Real fullscreen only (Vimeo native) — no fake CSS fullscreen
- On play: unlock orientation, enter fullscreen, lock to landscape (landscape videos) or portrait (portrait videos)
- On exit fullscreen: re-lock portrait
- Exit via Vimeo's own controls (built-in). No custom × button.
- 2px black border on video containers
- iframes use `allow="autoplay; fullscreen; ..."` — redundant `allowfullscreen` attribute removed

**Fullscreen toast (Android Chrome):** Android OS shows a non-suppressible toast with URL on fullscreen entry. This is an OS-level security feature, not fixable from code. Behaviour may be cleaner in installed PWA — test post-launch.

---

## VISUAL DESIGN — KEY DECISIONS (DO NOT CHANGE)
- Background: Milky Way image + CSS starfield (220 stars)
- Cube: Glass effect, cyan-white glowing edges 2px
- Cube faces: **TEXT + LINES ONLY, NO IMAGES.** 4 small corner numbers per face (13px Cinzel Decorative) + 4 thin cyan edge lines inset 28px from corners. Face transparency 20% tinted navy (rgba(0,0,20,0.2)), backdrop-filter blur 6px (halved from 12px for crisper stars), dead linear-gradient removed.
- Cube DEFAULT ORIENTATION: **Face 4 (Astrology & Horoscope) facing viewer at load** — initial quat `{w:Math.SQRT1_2, x:0, y:Math.SQRT1_2, z:0}` (90° Y rotation). data-active="4" matches. Idle auto-rotate continues normally from there.
- Cube face lock icon: 🗝️ old key emoji (U+1F5DD), 18px, absolute-positioned `bottom:22px` (Face 6 uses `bottom:42px` scoped override), `transform:translateX(-50%) rotate(-41deg) scaleX(-1)` — teeth point east, pulse animation removed.
- Cube hint text: "rotate the cube / tap a side to open" — 10px Cinzel, 2px letter-spacing, two lines, non-bold
- Logo: QUANTUM top, CUBE right-aligned inline-block, CUBE cyan with glow + float
- Glass cards: NO margin overrides (centered via face-container padding)
- Lock screens: "Complete Quantum Cube Unlock" title, stacked bullets, $17.00, cyan-glow UNLOCK button. **Max-width 88% on mobile + auto horizontal margins** (base rule, line 190). `@media (min-width:600px)` caps to 44%.
- Payment overlay: Pay $17 + Back to Cube buttons NOW BOTH INSIDE the lock card — identical width automatically via shared `.unlock-btn` class. Back to Cube is `unlock-btn pay-overlay-btn` with transparent background + white border.
- Audio buttons:
  - **Music**: permanent inline-centered below #cubeHint. White border, white "MUSIC" label, cyan emoji + glow. Shown on faces 1-5 ONLY. `showFace()` hides on 0/CheckEmail/6/7. Extra 10px top margin on Faces 1 & 2 (22px vs 12px) to avoid crowding.
  - **Voice**: 3 instances via `.voice-btn` class. Face 3 inside face3-content below matrix. Face 4 inside face4-content below astro-grid (+10px top margin scoped `#face4-content .voice-btn{margin-top:30px}`). Face 5 inside face5-content above "Your Complete Portrait" header. Same white-border/white-label/cyan-emoji styling as Music. **NOT yet wired to ElevenLabs — UI only.**
  - Old scroll-reveal IIFE REMOVED.
- Legal footer on Face 0: Terms + Disclaimer + Settings (Settings signed-in only)
- Month dropdown: numbers 1-12
- PWA orientation: portrait locked, unlocks during landscape video play

**LAYOUT — CRITICAL:**
- `.face` padding symmetric `24px 18px 0 18px`
- All 5 result containers (`.scoreboard`, `.matrix-wrap`, `.astro-grid`, `.card-stack`, `.combo-full`) now have ZERO side margins — they fill `.face` padding for symmetric 18px breathing room matching videos
- `.icard-body` horizontal margin REMOVED (was stacking with padding for 36px inset) — now 18px padding only, matches `.combo-full`'s 20px feel
- Numerology matrix cells (`.mc`): **square via `aspect-ratio:1/1`** with flex centering. Multiply count (`mc-c`) REMOVED — just number + dots.
- Astrology cells (`.astro-item`): **square via `aspect-ratio:1/1`** with flex centering. (Note: duplicate `.astro-item` selector — harmless but flag for next audit.)
- Combined teaser paragraph (combo-box on Face 4) REMOVED — already covered in full Face 5 narrative.
- Face 4 combo-txt summary line + Face 3 matLeg line (hidden passion / karmic lessons summary) REMOVED.

**BUTTON SIZES:**
- `.calc-btn`, `.unlock-btn`, `.reset-btn`, `.pay-back` all use `font-size:clamp(11px,3vw,13px)` and `letter-spacing:clamp(3px,1.5vw,5px)`
- `.err-msg` styling matches `.consent-main` — Cormorant Garamond 15px, no uppercase, no letter-spacing, red-pink color + subtle glow

---

## 🪨 HAPTIC MAP
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

## 🔊 AUDIO ASSETS
**Extracted from base64 into `Sounds/` folder (committed):**
- `bgMusic.mp3`, `openSound.wav`, `selectSound.wav`, `pop1.mp3`, `pop2.mp3`
- Two lightsaber cube-touch FX (wired but silenced)

**Current state:**
- Cube touch sound is wired but silenced at `/* a.play().catch(...) */`
- The 5 original sounds are still base64-embedded in HTML (~lines 828-832). Not yet rewired to load from Sounds/ folder.
- Base64 → file references cleanup: significantly shrinks HTML when done. **HIGH PRIORITY post-launch** — biggest perf win available.

---

## SUPABASE BACKEND
- **Project:** quantum-cube (ref `fqqdldvnxupzxvvbyvjm`)
- **Region:** Central EU (Frankfurt) — POPIA/GDPR aligned
- **Org:** Quantum Neuro Creations (`ybhwpcakkaveapdztnrs`)
- **Credentials:** `.supabase-env` (gitignored) — SUPABASE_URL, SUPABASE_ANON_KEY (new sb_publishable_... format), SUPABASE_PROJECT_ID, RESEND_API_KEY

### Schema — `public.profiles`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK, references `auth.users.id` |
| email | text | |
| has_paid | boolean | Immutable from client — only service role can flip |
| marketing_consent | boolean | From user_metadata at signup |
| created_at | timestamptz | |

### RLS Policies
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
- `persistSession: true, autoRefreshToken: true, detectSessionInUrl: true, flowType: "implicit"`
- `window.sb = sb` exposed for debugging

### Edge Functions
None deployed. Paddle webhook is Monday's work.

### Supabase CLI commands (v2.90.0) — CORRECT SYNTAX
- **NOT** `supabase db execute --project-ref X "SQL"` (doesn't exist)
- **YES** `supabase db query --linked "SQL"` (from linked project directory)
- Example: `supabase db query --linked -o table "SELECT id, email, has_paid FROM public.profiles WHERE email = 'X';"`

### Test data in profiles (delete before launch)
- `quantumneurocreations@gmail.com` — **currently flipped to has_paid=true for testing**
- `rkelbrickmail@gmail.com`
- `carlkelbrick@gmail.com`
- Any `test+*@qncacademy.com`

---

## FRONTEND WIRING — SHIPPED

### Key line refs (April 19 evening — use grep, numbers drift)
| What | Approx line |
|---|---|
| const sb = createClient | ~499 |
| Loading screen | ~463 |
| Face 0 div open | ~531 |
| faceCheckEmail interstitial | ~547 (3 form-title lines inside glass-card) |
| Resend Email button | ~601 |
| Face 1 Back to Sign Up (reset-btn) | ~626 |
| #musicBtn (inline after cubeHint) | ~536 |
| #cubeHint | ~535 |
| window.haptic definition | ~1141 |
| _cubeTouchSounds array | ~1141 |
| playCubeTouchFX function | ~1141 |
| Two-finger twist block | ~1195 |
| let quat (init to Face 4 orientation) | ~1091 |
| function showFace | ~1341 |
| function pickRotation (narrative variations) | ~1905 |
| function buildCombinationNarrative | ~1917 |
| STORE_KEY const | ~1994 |
| function checkStoredUnlock | ~1998 |
| function syncUnlockFromProfile | ~2008 |
| function applyUnlockedState | ~2038 |
| launchPayFast notify placeholder | ~2080 |
| QC_PENDING_KEY const | ~2185 |
| async function handleRevealClick | ~2222 |
| signInWithOtp (handleRevealClick path) | ~2276 |
| signInWithOtp (resend path) | ~2341 |
| sb.auth.onAuthStateChange | ~2368 |
| **function runCalculation** | **~2407** |
| function textToParas (array-safe) | ~2449 |
| function getNumText (rotation-based) | ~2459 |
| function renderAllContent | ~2475 |
| NUM.pc reference (Life Phases render) | ~2517 |
| SW code string | **~2734** (currently `qc-v99`) |

**Always grep before editing — these drift.**

---

## 🔐 AUTH + UNLOCK FLOW — SHIPPED ARCHITECTURE

### Entry paths that populate profileData + render results
1. **Fresh first-time signup** → form submit → magic link → redirect → `onAuthStateChange` SIGNED_IN → calls `restorePendingProfile()` then `runCalculation()` → profileData built → `renderAllContent()` called at end of runCalculation
2. **Returning verified user (session exists)** → form submit → `handleRevealClick` short-circuits via `sb.auth.getSession()` email match → skips magic link → calls `runCalculation()` → same flow
3. **Already-paid user page reload** → `initSupabaseSession` → `restorePendingProfile()` → if session exists, `runCalculation()` fires with populated form

### Key fixes shipped April 19:
- `applyUnlockedState` now hides `.lock-screen` and reveals face3-6 content (previously only hid keys — returning paid users saw empty cards)
- `onAuthStateChange` SIGNED_IN now calls `restorePendingProfile()` BEFORE `runCalculation` (was empty-form bailing)
- `handleRevealClick` short-circuits when session email matches entered email (no magic-link loop for verified users)
- `runCalculation` now ALWAYS calls `renderAllContent()` at the end (previously only on payment success — returning paid users saw blank faces)
- `textToParas` made array-safe (was crashing on NUM array entries → killed renderAllContent partway → Face 3 interpretations + Face 4 astro + Face 5 combined were blank)

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
- [ ] Delete test rows from profiles (INCLUDING the one currently flipped to paid for testing)

### ⚙️ Sunday/early week
- [ ] **ElevenLabs narrator wiring** — Voice buttons on Faces 3/4/5 are UI only. Reuse Academy API key. Decide: toggle on/off per face vs per-card click trigger. Ronnie's preference: clean + practical, default toggle model.
- [ ] **Fine-comb audit/debug pass** — dead code, date bugs, duplicate CSS selectors (e.g. `.astro-item` duplicate, `.err-msg` duplicate at line 189). Do AFTER Paddle ships.
- [ ] **Base64 asset extraction** — biggest perf win: HTML is 11.6MB. Extracting the 5 base64-embedded sounds will shrink meaningfully + reduce cold-load jank. Rewire to load from Sounds/ folder, test playback, music pause/resume on video play.
- [ ] Paddle prep doc for team meeting (business entity, bank, tax ID, product URL, checkout flow)

### 📝 Post-launch follow-ups
- [ ] **Astrology / Horoscope / Combined content variations** — currently single-string by design. Combined = Western × Chinese only (144 combos). Rotation helper is reusable if/when variations are authored. NOT confirmed, deferred.
- [ ] **Face 5 narrative opener variations** — 3 variations shipped for p1/p7/p9. Other 6 paragraphs unchanged.
- [ ] **Music library** — source 4 more ambient tracks similar to Dream-Focus-Beta-Waves, rotate through, persist index between sessions.
- [ ] **Numerology sequential rotation** — SHIPPED April 19. Per-user persisted via `qc_rotIdx` localStorage key.
- [ ] **Contact info + email address creation** — `info@quantumcube.app` via Cloudflare routing
- [ ] Marketing email pipeline + unsubscribe endpoint (Privacy Policy promises this)
- [ ] Brand the Supabase magic-link email
- [ ] Fix Resend return-path: `@send.quantumcube.app` → display `@quantumcube.app`
- [ ] App stores — Google Play (PWABuilder → .aab → $25); Apple (Capacitor → Xcode → $99/yr). Note: native wrappers don't make web code run faster — just distribution + native permissions.
- [ ] Social proof / testimonials
- [ ] Sharing mechanism for readings
- [ ] Analytics
- [ ] Profile deletion Edge Function
- [ ] Gmail aliases propagation check + 2FA on all 3 partner accounts
- [ ] DMARC tighten p=none → p=quarantine after 2 weeks clean reports
- [ ] Migrate business services: `quantumneurocreations@gmail.com` → `admin@qncacademy.com`

---

## INFRASTRUCTURE LIVE
| System | State |
|---|---|
| GitHub Pages | Live, serving latest HTML commit (**SW qc-v99**) |
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

---

## SEPARATE PROJECT — QNC ACADEMY
- Path: /Users/qnc/Projects/qnc-academy/
- Stack: Next.js + Vercel + Supabase + ElevenLabs + GitHub
- URL: qnc-academy.vercel.app
- Supabase: SEPARATE project (Ireland) ref `bevaepokvavzmykjmhda`
- **Never mix with Quantum Cube chats or code.**

---

## SESSION LOG — April 19, 2026 (marathon session, 56 commits, SW qc-v42 → qc-v99)

### Content / data
- Numerology variation picker: random → per-user persisted sequential rotation (`qc_rotIdx` localStorage)
- Face 5 narrative: 3 variations each for paragraph 1 (life-path opener), 7 (astrology transition), 9 (closing) via `pickRotation` helper
- `textToParas` made array-safe (critical bug fix — was crashing renderAllContent for paid users)
- Combo teaser on Face 4 removed (redundant with Face 5 full narrative)
- Hidden Passion / Karmic Lessons summary line on Face 3 (matLeg) removed

### Auth / unlock (BIG ARCHITECTURE FIXES)
- Age gate on signup (18+)
- `applyUnlockedState` now reveals face content (was only hiding keys)
- `onAuthStateChange` SIGNED_IN calls `restorePendingProfile` before runCalculation
- `handleRevealClick` short-circuits when session matches entered email (no redundant magic-link loop)
- `runCalculation` always calls `renderAllContent` at end

### Cube
- Default orientation: Face 4 facing viewer (quat + data-active synced)
- Dead zero-alpha background gradient removed
- Backdrop-filter blur halved 12px → 6px (crisper stars)
- Inset edge lines glow tried + reverted

### Cube face key icon overhaul (many iterations)
- 🔒 padlock emoji → 🗝️ old key emoji
- Size tuned (11px → 18px)
- Position tuned (bottom:22px; Face 6 scoped bottom:42px)
- Rotation tuned through scaleX(-1) + rotate(-41deg) so teeth point east with bit on east side
- lockPulse flashing animation removed

### Layout / cards
- All 5 result containers side margins zeroed → fill face padding (symmetric 18px)
- `.icard-body` 18px horizontal margin removed (was stacking with padding for 36px inset)
- Numerology matrix cells: square via aspect-ratio, multiply count removed
- Astrology cards: square via aspect-ratio (duplicate selector to flag in audit)
- Portrait videos widened 56.25% → 75%
- Payment lock cards: base max-width:88% added (mobile was uncapped because cap was in `@media (min-width:600px)`)
- Back to Cube button: moved INSIDE lock card below Pay $17 → both share parent, identical width
- err-msg typography matched to consent-main (Cormorant Garamond 15px, no uppercase)

### Audio buttons
- Music: permanent inline-centered, white border, white label, cyan emoji+glow, shown on faces 1-5 only. Extra 10px top margin on Faces 1 & 2.
- Voice: 3 instances via `.voice-btn` class on Faces 3/4/5. NOT wired to ElevenLabs yet.
- Scroll-reveal IIFE removed.

### Marketing consent
- "Email me updates" × 5 locations → "Add Me To The Quantum" + "News And Insights From The Cube" subtitle (POPIA/GDPR specificity, brand voice)

### Iframe + cleanup
- `allowfullscreen` attribute removed from 5 Vimeo iframes (redundant with `allow="fullscreen"`)
- `_updateMuteBtn` inert helper removed (mute button already deleted)
- 4 dead CSS blocks removed

### Process lessons
- **@media (min-width:600px) is desktop-only on mobile viewports.** Changes inside that media query are invisible on phones. Always check whether a rule is wrapped in a min-width media query before assuming it'll affect mobile.
- **`grep -c` with 0 matches exits 1** — use `|| true` on verify greps.
- **BSD sed can't do multi-line replacements** — Cursor correctly shifts to Python one-shots.
- **Never iterate on Python scripts to fix HTML** — break into smaller str_replace edits instead.
- **Cursor self-corrects verbatim output** when a Python script's anchor string doesn't match disk — this is welcomed and the correct behaviour.
- **`supabase db query --linked "SQL"`** is the correct CLI command for Supabase 2.90.0 — NOT `db execute --project-ref`.
- **`sb_publishable_...` key format** works with SDK 2.45.4 for auth. Session persists correctly in regular Chrome tabs.
- **Magic link opening "in browser"** (not Gmail's internal browser) is critical for session to land in main Chrome context where user tests.

---

## NEXT SESSION STARTING POINT

1. **Paddle prep doc** — biggest priority for Monday team meeting
2. **ElevenLabs narrator wiring** — Voice button UI exists on Faces 3/4/5, needs backend integration
3. **Base64 audio extraction** — perf win, shrinks HTML meaningfully
4. **Fine-comb audit pass** — duplicate CSS selectors (`.astro-item`, `.err-msg`), dead CSS cleanup, date bugs

**First action of next chat:** attach this brief + CHAT_KICKOFF.md, run the minimal health check (see kickoff), then pick from the list above.
