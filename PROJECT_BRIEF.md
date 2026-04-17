# QUANTUM CUBE — MASTER PROJECT DOCUMENT
**Version: v10 | Last Updated: April 17, 2026**

---

## ⚠️ CRITICAL RULE — ALWAYS READ FIRST
**Quantum Cube and QNC Academy are COMPLETELY SEPARATE projects.**
- Never mix code or files between them
- Quantum Cube currently lives on GitHub Pages
- If creating new Vercel or Supabase projects, create them FOR Quantum Cube — never modify or touch the Academy project
- Always confirm which project you are working on before making any changes
- Vercel, Supabase, and all platforms are allowed — just make sure you are working on the Quantum Cube project, not the Academy

---

## ⚠️ FIRST THING EVERY SESSION — RUN THIS BEFORE TOUCHING ANYTHING:
```bash
grep -n "function runCalculation" /Users/qnc/Projects/quantumcube/quantum-cube-v10.html
```
If it returns empty — restore from git before proceeding:
```bash
git show HEAD~1:quantum-cube-v10.html > /tmp/good-version.html
cp /tmp/good-version.html /Users/qnc/Projects/quantumcube/quantum-cube-v10.html
```

---

## FILE LOCATIONS

/Users/qnc/Projects/quantumcube/              <- MAIN PROJECT FOLDER
|- quantum-cube-v10.html                      <- THE APP (single file, ~12MB)
|- PROJECT_BRIEF.md                           <- This document
|- cube-background.jpg                        <- Milky Way background image (in repo)
|- Cube Sides/                                <- Cube face images (gitignored - embedded in HTML)
|  |- Side 1.png + Side 1.webp
|  |- Side 2.png + Side 2.webp
|  |- Side 3.png + Side 3.webp
|  |- Side 4.png + Side 4.webp
|  |- Side 5.png + Side 5.webp
|  |- Side 6.png + Side 6.webp
|- Videos/                                    <- Video local backups (gitignored)
|- audio/
   |- ES_Dream_Focus_Beta_Waves.mp3
   |- Opening_app.wav
   |- Cube_Side_Selection.wav
   |- rotate_cube.wav
   |- Pop1.mp3
   |- Pop_2.mp3

**GitHub Repo:** https://github.com/quantumneurocreations-dot/quantumcube
**Live URL:** https://quantumneurocreations-dot.github.io/quantumcube/quantum-cube-v10.html
**Gitignored:** Videos/, Music/, Sounds/, Video Thumbnails/, Backup/, .DS_Store, More backgrounds/, Cube Sides/

---

## DEV ENVIRONMENT
| Item | Detail |
|------|--------|
| Machine | Mac Mini M4 |
| Username | qnc |
| Project path | /Users/qnc/Projects/quantumcube |
| Editor | Cursor + Terminal |
| GitHub Desktop | Not installed - using GitHub CLI instead |
| GitHub CLI | gh v2.89.0 - authenticated as quantumneurocreations-dot |
| SSH Key | ED25519 ~/.ssh/id_ed25519 - "Quantum's Mac mini" - verified |
| Node.js | v24.15.0 (LTS) via nvm, npm v11.12.1 |
| cwebp | v1.6.0 via Homebrew |
| Homebrew | Installed, PATH set in ~/.zprofile |
| .cursorignore | In place - excludes quantum-cube-v10.html from indexing |
| Cursor | Installed, signed in, Vercel plugin installed |
| code command | Installed - use "code ." to open projects in Cursor |

**Terminal push command:**
```bash
cd /Users/qnc/Projects/quantumcube
git add .
git commit -m "description"
git push
```

---

## WORKFLOW RULES - CRITICAL
- **Use Mac Terminal + sed/python3** for CSS and HTML structure changes
- **JavaScript changes only** via Cursor Claude Code
- **Never use sed for JavaScript functions** - silently corrupts code
- **Python3 for multi-line replacements** - safer than sed for complex changes
- **Always verify runCalculation** before and after any edit
- **Cursor:** Start every chat with "Never read the full file. Use Grep to find line numbers, then Read only specific lines, then StrReplace."
- **.cursorignore** - already in place, prevents indexing of large files

---

## HOW TO WORK ON THE FILE
**IMPORTANT: Simple CSS/HTML = Mac Terminal. JavaScript = Cursor Claude Code only.**

If in Cursor with Claude Code:
1. File is at /Users/qnc/Projects/quantumcube/quantum-cube-v10.html
2. Do NOT read the full file - Grep first, then read specific lines
3. File is ~12MB - do NOT upload to chat
4. Use live URL for visual checks
5. After edits: git add, commit, push

---

## TECH STACK
- Single HTML file - no framework, no backend, no database
- Vanilla JavaScript - all calculations client-side
- CSS3 - 3D transforms, glassmorphism, custom animations
- Fonts: Cinzel Decorative (logo), Cinzel (labels/UI), Cormorant Garamond (body text)
- Payment: PayFast (sandbox credentials active)
- Videos: Vimeo - Player API active, fake fullscreen on play, portrait videos stay portrait
- Audio: Base64 embedded (currently disabled)
- Hosting: GitHub Pages
- PWA: Web manifest, service worker (cache: qc-v11)
- Background: Milky Way image (cube-background.jpg) behind CSS starfield
- Cube faces: 6 WebP images base64 embedded, 160x160px locked - clean glass look preferred (no face textures)

---

## APP STRUCTURE - 7 FACES
| Face | Name | Status | Videos |
|------|------|--------|--------|
| Face 0 | Entry / Sign Up Form | Complete | None |
| Face 1 | Introduction | Complete | Introduction (portrait 9:16) |
| Face 2 | Results Explained | Complete | Numerology + Results Explained + Astrology (landscape 16:9) |
| Face 3 | Numerology Results | Complete | None |
| Face 4 | Astrology & Horoscope | Complete | None |
| Face 5 | Combined Results | Complete | None |
| Face 6 | Complete / Outro | Complete | Cube Outro (portrait 9:16) |
| Face 7 | Settings / Launch Guide | Complete | None |

---

## VIMEO VIDEOS - CURRENT STATE
All videos on Vimeo. Privacy: Hide from Vimeo. Downloads OFF. Comments OFF.

| Face | Title | Vimeo ID | Shape |
|------|-------|----------|-------|
| Face 1 | 1 - Introduction | 1183086210 | Portrait (9:16) |
| Face 2 | 2 - Numerology Explained | 1183086853 | Landscape (16:9) |
| Face 2 | 3 - Results Explanation | 1183087269 | Landscape (16:9) |
| Face 2 | 4 - Astrology | 1183087951 | Landscape (16:9) |
| Face 6 | 5 - Cube Outro | 1183103519 | Portrait (9:16) |

Video behaviour: fake fullscreen via CSS on play. Portrait videos stay portrait. Landscape videos allow phone rotation via Screen Orientation API unlock on play, relock to portrait on pause/end.

---

## VISUAL DESIGN - KEY DECISIONS (DO NOT CHANGE)
- Background: Milky Way image (cube-background.jpg) + CSS starfield on top
- Starfield: 220 stars, round glowing dots
- Cube: Glass effect, cyan-white glowing edges 2px - clean glass faces (no face images)
- Logo: QUANTUM top, CUBE right-aligned, CUBE in cyan with glow + float animation
- All cards: glass style, margin 0 16px 20px 32px (breathing room left/right)
- Lock screens: same margins as sign-up card
- Scoreboard, matrix, card-stack, astro-grid, combo-full: all have matching side margins
- Video-face: margin 0 16px 16px 32px on Face 2 landscape videos
- Lock screen: "Complete Quantum Cube Unlock", & between Chinese Horoscope and Combined Interpretation, $8.00
- Unlock button: text "Unlock", narrow width (auto/160px min), centered
- Three fixed buttons bottom-right: narrator (top), music (middle), mute (bottom)
- Combined portrait: no drop cap, starts "You are someone..."
- Face 6 outro: removed icon/title/text, only "Your Journey Complete" heading + video
- Legal footer: Terms of Use + Disclaimer outside lock cards, hidden on unlock via .lock-footer class, restored on reset
- "Period Cycles" changed to "Life Phases" everywhere
- Month dropdown: numbers 1-12
- PWA orientation: portrait locked, unlocks during landscape video play

---

## CUBE BEHAVIOUR
- Hidden on Face 0, visible on all other faces
- Idle auto-rotation after 1 second
- Drag rotates cube, no snap-back on release
- Cube faces: clean glass look - no face images
- Face mapping: Front=Face1, Right=Face2, Back=Face3, Left=Face4, Top=Face5, Bottom=Face6

---

## PAYMENT SYSTEM
- Gateway: PayFast (SA only) - needs Stripe/Paddle for global
- Price: $8 USD once-off
- Status: Sandbox active, not live
- "Try Demo (test mode)" button - DELETE before going live

---

## WHAT STILL NEEDS TO BE DONE

### PRIORITY 1 - Content Variations (BIGGEST LAUNCH BLOCKER)
Write 2 additional variations (total 3 per number) for:
- [ ] Birthday Number (11 numbers)
- [ ] Expression (13 numbers)
- [ ] Soul Urge (13 numbers)
- [ ] Personality (11 numbers)
- [ ] Hidden Passion (9 numbers)
- [ ] Karmic Lessons (9 numbers)
- [ ] Life Phases (11 numbers)
- [ ] Personal Year (11 numbers)

### PRIORITY 2 - Content Accuracy Review
- [x] Verify all numerology interpretations - DONE
- [x] Verify all Western astrology content - DONE
- [x] Verify all Chinese zodiac content - DONE
- [ ] Verify all 144 combination readings
- [ ] Review combined portrait quality and flow

### PRIORITY 3 - Narrator Voice (ElevenLabs)
- [ ] Wire narrator button to ElevenLabs API
- [ ] Male/female voice toggle
- [ ] API key already set up in Academy - reuse same key
- [ ] Play reading text when result card opens, stop button available

### PRIORITY 4 - Audio
- [ ] Re-enable audio (uncomment ~2 lines in JS)
- [ ] Test all 6 sounds on device
- [ ] Test music pause/resume on video play

### PRIORITY 5 - Payments
- [ ] Switch from PayFast to Stripe or Paddle for global
- [ ] Remove "Try Demo (test mode)" button before go-live
- [ ] Test live $8 payment end-to-end

### PRIORITY 6 - App Stores
- [ ] Google Play: PWABuilder.com -> .aab -> $25 USD dev account
- [ ] Apple App Store: Capacitor -> Xcode -> $99/yr dev account

### PRIORITY 7 - Final Polish
- [ ] Remove cube face images - clean glass look (PENDING - decided April 16)
- [ ] Final QA pass all faces on device
- [ ] Add social proof / testimonials section
- [ ] Add sharing mechanism for readings
- [ ] Email capture or PWA push notification opt-in
- [ ] Mouse mousedown/mouseup cube glow (desktop)
- [ ] Spike star CSS cleanup (harmless but messy)

---

## STRATEGIC NOTES
- Content variations are the biggest priority before launch
- PayFast is SA only - need Stripe/Paddle for international
- No user accounts - consider email + localStorage for now
- No sharing mechanism yet - users should be able to share their reading

---

## SEPARATE PROJECT - QNC ACADEMY
Path:    /Users/qnc/Projects/qnc-academy/
Stack:   Vercel + Supabase + ElevenLabs + GitHub
URL:     qnc-academy.vercel.app
Status:  Active development - COMPLETELY SEPARATE CHAT

**Never bring Academy work into Quantum Cube chats and vice versa.**

---

## NEXT SESSION STARTING POINT
- Machine migrated to M4 Mac Mini - all tools installed and verified
- runCalculation confirmed at line 1983
- Remove cube face images - preference is clean glass look - PENDING
- Narrator button is in place but not wired up - next big feature
- Content variations are the #1 priority for launch readiness
- "Try Demo (test mode)" button needs removing before go-live
- Consider removing stars entirely and replacing with a different effect over the Milky Way background

---

## SESSION LOG

### April 16, 2026 - M1 Session (final session on old machine)
- [x] FIXED - Landscape videos rotate 90deg in fake fullscreen via CSS transform
- [x] FIXED - Portrait videos excluded from rotation via .portrait-video class
- [x] FIXED - Outro video (Face 6) portrait-video class duplicate attribute fixed
- [x] FIXED - Back to Sign Up button: arrow removed, two lines, width matches portrait video
- [x] FIXED - Loading screen added with QUANTUM CUBE logo, fades out after 3.5s
- [x] FIXED - Background image compressed 5.6MB to 327KB, preload hint added
- [x] FIXED - Cube face images: broken local file references removed, base64 WebP now loads correctly
- [x] FIXED - Cube face transparency changed to 80% (rgba 0,0,20,0.2)
- [x] CONTENT - Michelle tested all numerology and astrology outcomes, all accurate
- [x] UPDATE - Priority 2 Content Accuracy Review: numerology, astrology, Chinese zodiac all verified

### April 16, 2026 - M4 Mac Mini Migration
- [x] Homebrew installed, PATH set in ~/.zprofile, brew doctor confirmed ready
- [x] Git installed via Homebrew
- [x] nvm installed + Node.js v24.15.0 (LTS) + npm v11.12.1
- [x] cwebp v1.6.0 installed via Homebrew
- [x] GitHub CLI gh v2.89.0 installed and authenticated via browser
- [x] ED25519 SSH key generated at ~/.ssh/id_ed25519
- [x] SSH key added to GitHub account as "Quantum's Mac mini"
- [x] SSH connection tested and verified as quantumneurocreations-dot
- [x] Cursor IDE downloaded, installed and signed in
- [x] Vercel plugin installed in Cursor
- [x] code command installed - open projects with "code ." in terminal
- [x] ~/Projects folder created
- [x] quantumcube repo cloned to /Users/qnc/Projects/quantumcube via SSH
- [x] .cursorignore created - excludes quantum-cube-v10.html from Cursor indexing
- [x] runCalculation verified present at line 1983
- [x] qnc-academy repo cloned to /Users/qnc/Projects/qnc-academy via SSH
- [x] Vercel CLI installed globally via npm
- [x] Vercel CLI logged in and project linked via vercel link
- [x] Supabase CLI v2.90.0 installed
- [x] npm install completed in qnc-academy - 407 packages, 0 vulnerabilities
- [x] .env.local created by pulling environment variables from Vercel
- [x] Dev server tested - Next.js 16.2.3 running at localhost:3000 in 161ms

---

## SESSION LOG — April 16, 2026 — Afternoon Session

### Fixes & Features
- [x] Cube face images fully removed — clean glass look live
- [x] Video pause now exits fullscreen and returns to app
- [x] Double tap on video toggles play/pause + fullscreen
- [x] Unlock button — 2px white border, 60% width matching divider line
- [x] Unlock button — cyan glow on hover/active matching other buttons
- [x] Loading screen — CUBE text right-aligned to match main logo

### Content Written (not yet inserted into file — do in next session)
- [x] Birthday Number — 2 additional variations written for all 11 numbers
- [x] Expression — 2 additional variations written for all 12 numbers
- [x] Soul Urge — 2 additional variations written for all 12 numbers

### Still To Write (next session)
- [ ] Personality — 2 additional variations for 11 numbers
- [ ] Hidden Passion — 2 additional variations for 9 numbers
- [ ] Karmic Lessons — 2 additional variations for 9 numbers
- [ ] Life Phases — 2 additional variations for 11 numbers
- [ ] Personal Year — 2 additional variations for 11 numbers

### Next Session Starting Point
- Insert Birthday, Expression, Soul Urge variations into HTML file
- Continue writing remaining category variations
- Life Path confirmed complete — 12 numbers, 3 variations each
- All other categories confirmed as single variation only — system ready for arrays
- "Period Cycles" already removed from file — no fix needed

### April 16, 2026 — Evening Session
- [x] All 9 numerology categories now have 3 variations each — COMPLETE
- [x] Birthday Number — 11 numbers, 3 variations each
- [x] Expression — 12 numbers, 3 variations each
- [x] Soul Urge — 12 numbers, 3 variations each
- [x] Personality — 11 numbers, 3 variations each
- [x] Hidden Passion — 9 numbers, 3 variations each
- [x] Karmic Lessons — 9 numbers, 3 variations each
- [x] Life Phases — 11 numbers, 3 variations each
- [x] Personal Year — 9 numbers, 3 variations each
- [x] PRIORITY 1 CONTENT VARIATIONS — COMPLETE

---

## SESSION LOG — April 17, 2026 — Morning Update

### Status Update
- [x] PRIORITY 1 — Content Variations — COMPLETE
- [x] PRIORITY 2 — Content Accuracy Review — COMPLETE
  - Numerology interpretations verified by Michelle
  - Western astrology verified
  - Chinese zodiac verified
  - 144 combination readings reviewed — consistent and accurate
  - Combined portrait quality confirmed good
- [x] M4 Mac Mini fully set up and verified
- [x] SSH permanently configured
- [x] Cursor workflow established and working

### What Still Needs To Be Done

#### PRIORITY 3 — Narrator Voice (ElevenLabs)
- [ ] Wire narrator button to ElevenLabs API
- [ ] Male/female voice toggle
- [ ] API key already set up in Academy — reuse same key
- [ ] Play reading text when result card opens, stop button available

#### PRIORITY 4 — Audio
- [ ] Re-enable audio (uncomment ~2 lines in JS)
- [ ] Test all 6 sounds on device
- [ ] Test music pause/resume on video play

#### PRIORITY 5 — Payments
- [ ] Switch from PayFast to Stripe or Paddle for global
- [ ] Remove "Try Demo (test mode)" button before go-live
- [ ] Test live $8 payment end-to-end

#### PRIORITY 6 — User Accounts & Leads (NEW — decision needed)
- [ ] Decision: simple email capture vs full Supabase accounts
- [ ] Email + password + PIN for returning users
- [ ] Save profile to database for leads
- [ ] Supabase already set up for Academy — can reuse

#### PRIORITY 7 — Legal & Credits
- [ ] Add Epidemic Sound music credit to Terms/Disclaimer
- [ ] Privacy Policy — collecting names and birthdates requires one
- [ ] Cookie/GDPR notice for international users

#### PRIORITY 8 — App Stores
- [ ] Google Play: PWABuilder.com -> .aab -> $25 USD dev account
- [ ] Apple App Store: Capacitor -> Xcode -> $99/yr dev account

#### PRIORITY 9 — Final Polish
- [ ] Final QA pass all faces on device
- [ ] Add social proof / testimonials section
- [ ] Add sharing mechanism for readings
- [ ] Email capture or PWA push notification opt-in
- [ ] Mouse mousedown/mouseup cube glow (desktop)
- [ ] Analytics — track usage
- [ ] Remove "Try Demo (test mode)" button before go-live

### Next Session Starting Point
- Decide on user accounts approach (simple email capture vs full Supabase)
- Wire narrator button to ElevenLabs
- Add Epidemic Sound credit to legal footer
- Re-enable audio

---

## SESSION LOG — April 17, 2026 — Infrastructure Day

### Team Structure (documented for future context)
- **Ronnie (Willem)** — design, programming, tech lead
- **Michelle** — admin
- **Keyzer** — marketing + finance/payments
- Equal 3-way partnership
- Faceless brand philosophy: public only sees `admin@` and `info@`, never individual names

### Priority 1 — Epidemic Sound Credit — COMPLETE
- Added "Third-Party Credits" section to Intellectual Property tab in legal docs modal
- Credits cover music (Epidemic Sound subscription), fonts (Google Fonts SIL Open Font), payments (PayFast)
- Generic wording — covers all tracks present and future, no track-by-track listing
- Committed and pushed: commit 3b8428e
- runCalculation verified at line 1983 before and after — no JS corruption

### Priority 2 — Domain & Email Infrastructure — PARTIALLY COMPLETE

**Domains registered via Cloudflare Registrar:**
- qncacademy.com — primary product URL + email home
- quantumcube.app — Cube app URL
- Both registered Apr 17, 2026 → expire Apr 17, 2027, auto-renew ON
- Total domain cost: ~R475/year

**Google Workspace setup:**
- Business Starter (annual commitment, 10% off for 12 months) — €6.12/user/month
- 14-day free trial active (billing starts ~May 1, 2026)
- Organisation: "Quantum Neuro Creations"
- Domain qncacademy.com verified via Cloudflare OAuth
- MX records + SPF TXT added via Cloudflare DomainConnect
- Gmail active on qncacademy.com
- Admin user: admin@qncacademy.com (WK Pretorius)
- Alias created: info@qncacademy.com

**Team Structure Decision — LOCKED IN:**
- 1 paid seat only: admin@qncacademy.com
- All three partners share admin login (trusted team)
- Personal emails are free aliases, used only for internal team-to-team communication
- Public face is strictly admin@ and info@

**Still to set up (next session):**
- [ ] Add 4 remaining aliases: privacy@, michelle@, keyzer@, ronnie@qncacademy.com
- [ ] "Send As" setup for each named alias (verification code from admin inbox)
- [ ] Gmail filters to auto-label emails by recipient alias
- [ ] Cloudflare Email Routing on quantumcube.app → forward to admin@qncacademy.com
- [ ] DKIM authentication (for email deliverability)
- [ ] Optional: cancel old quantumneurocreations.co.za Workspace once cutover verified

### Priority 3 — Privacy Policy / POPIA / Security Rewrite — NOT STARTED

**Context:** Current legal docs claim "zero data collection, no backend, no user accounts." Supabase Auth + email storage + marketing consent will make those claims false. Must rewrite BEFORE Supabase goes live.

**Decisions locked in:**
- Supabase region: Frankfurt (eu-central-1) — GDPR-strong
- Data deletion timeline: 30 days
- Support email for legal docs: privacy@qncacademy.com
- Marketing consent: unchecked checkbox on signup (not pre-ticked, per GDPR/POPIA)

**Still to do:**
- [ ] Draft replacement Privacy Policy section
- [ ] Draft replacement POPIA & Data Compliance section
- [ ] Draft replacement Security section
- [ ] Python replacement command (same pattern as Epidemic Sound insert)
- [ ] Deploy at same moment Supabase Auth goes live

### Priority 4 — Supabase Auth (ORIGINAL ITEM 1) — NOT STARTED

**Decisions locked in:**
- Magic link / OTP auth, no passwords
- Session persists 30–90 days
- No readings history saved (readings deterministic from name + birthdate)
- Minimal DB: email, has_paid, marketing_consent, created_at
- Signup form: one checkbox "Email me updates" — UNCHECKED by default
- Separate Supabase project from Academy (per project isolation rule)

### Annual Running Cost Summary
- 1× Google Workspace seat: ~R1,340/year
- qncacademy.com renewal: ~R200/year
- quantumcube.app renewal: ~R275/year
- **TOTAL: ~R1,815/year (~R150/month)**

(Excludes: PayFast transaction fees, Supabase paid tier if free limits exceeded, ElevenLabs narrator API usage)

### Next Session Starting Point
1. Finish aliases (privacy, michelle, keyzer, ronnie) + Send As setup — 15 min
2. Cloudflare Email Routing on quantumcube.app — 10 min
3. Draft privacy rewrite (Privacy / POPIA / Security) — Claude drafts, you review
4. After privacy drafts approved → begin Supabase Auth wiring
5. Then: narrator button → ElevenLabs, re-enable audio, DKIM, payments switch


---

## SESSION LOG — April 17, 2026 — Infrastructure Day Part 2

### Shipped to production
- [x] Privacy Policy section rewritten for Supabase-era data handling
- [x] POPIA & Data Compliance section rewritten (adds Information Officer, cross-border transfer, breach notification)
- [x] Security section rewritten (magic-link auth, Supabase at-rest, no readings history, 72hr incident response)
- [x] Commit 7a6a23e pushed to main — live on GitHub Pages
- [x] rewrite_legal.py committed (Python replacement script with runCalculation safety check)

### Gmail admin@qncacademy.com hardened
- [x] 5 filters created with labels: Info, Privacy stay in inbox; Michelle, Keyzer, Ronnie skip inbox
- [x] Chat turned off (shared inbox cleanliness)
- [x] Smart features off (across all 3 Google popups)
- [x] Undo Send: 5s → 30s
- [x] Images: "Ask before displaying" (blocks tracking pixels)
- [x] Forwarding/POP/IMAP verified secure, Offline disabled at admin level
- [x] Conversation view on, Out-of-Office off, Dynamic email off

### Cloudflare Email Routing
- [x] Enabled on quantumcube.app (MX, DKIM, SPF records auto-added)
- [x] admin@qncacademy.com verified as destination
- [x] Catch-all rule ACTIVE: *@quantumcube.app → admin@qncacademy.com

### Supabase backend created (Priority 4 — backend phase)
- [x] Project "quantum-cube" created — project_id fqqdldvnxupzxvvbyvjm
- [x] Region: eu-central-1 (Frankfurt) — matches POPIA policy
- [x] Schema: public.profiles (id, email, has_paid, marketing_consent, created_at) — RLS enabled
- [x] Trigger: auth.users INSERT → public.profiles INSERT (auto-profile creation)
- [x] RLS policies: users read/update own row; has_paid immutable from client (must be set server-side after payment webhook)
- [x] Security advisor: 0 issues
- [x] Credentials saved to /Users/qnc/Projects/quantumcube/.supabase-env (gitignored)
- [x] SUPABASE_URL=https://fqqdldvnxupzxvvbyvjm.supabase.co
- [x] SUPABASE_ANON_KEY=sb_publishable_wp2cRcjgyJcarRVuq_Q1zw_Vd68AEcZ

---

## ITEMS CARRIED FORWARD — NOT done today, on radar

### Gmail / Workspace
- [ ] Send As aliases (info, privacy, keyzer, michelle, ronnie) — check propagation tomorrow; manual add via popup if needed
- [ ] "Reply from same address the message was sent to" setting — enable after Send As has 2+ addresses
- [ ] Gmail signature (per-alias) — needs brand wording decision
- [ ] Decide: hide Meet in sidebar or keep visible for client calls?
- [ ] IMAP disable at Admin Console level (if unused)
- [ ] Investigate "Turn on Gmail — Required" banner in admin inbox
- [ ] 2FA on all 3 partner Google Workspace accounts — verify enabled (Security section asserts "strong account security controls")
- [ ] Cancel old quantumneurocreations.co.za Workspace once cutover confirmed
- [ ] DKIM authentication for qncacademy.com (deliverability)

### Legal & content
- [ ] **LAUNCH BLOCKER: Rewrite Terms of Use section** — currently (line 2375–2376) says "unlock is tied to the device ... stored in local storage ... not responsible for unlocks lost due to clearing browser data or changing devices." This is FACTUALLY INCONSISTENT with the new account-based Privacy Policy once Supabase Auth goes live.
- [ ] Consider cookie banner for international users (likely optional since only one auth cookie is used, but worth a decision)
- [ ] If/when payment processor changes from PayFast, update all PayFast references (Privacy line 2338, Terms line 2375, IP line 2428, POPIA section)

### Frontend wiring (tomorrow's main work — launch blocker for Priority 4)
- [ ] Supabase dashboard: set Site URL to https://quantumneurocreations-dot.github.io/quantumcube/quantum-cube-v10.html
- [ ] Supabase dashboard: add redirect URLs (GitHub Pages + quantumcube.app)
- [ ] Supabase dashboard: configure session duration 30-90 days per brief
- [ ] Add @supabase/supabase-js via CDN to quantum-cube-v10.html
- [ ] Replace Face 0 sign-up form with email + marketing_consent checkbox (unchecked default)
- [ ] Wire signup → supabase.auth.signInWithOtp() with marketing_consent in user_metadata
- [ ] Handle magic-link callback on page load (detect #access_token= hash)
- [ ] Profile fetch on page load via supabase.from('profiles').select().single()
- [ ] Replace localStorage STORE_KEY="qc_unlocked_v1" (line 1813) gate with profiles.has_paid as source of truth (keep localStorage as cache)
- [ ] Supabase Edge Function for PayFast ITN webhook → updates has_paid server-side
- [ ] Replace placeholder https://YOUR-SERVER.com/payfast-notify (line 1877) with Edge Function URL
- [ ] Sign-out flow
- [ ] Age gate on signup (DOB check) — currently privacy policy says "not intended for under 18" without enforcement
- [ ] E2E test: signup → magic link → unlock payment → has_paid flips → locked content opens

### Pre-launch removal checklist
- [ ] Remove "Try Demo (test mode)" buttons at lines 608, 644, 678, 710
- [ ] Remove unlockDemo() JS function
- [ ] Switch PayFast from sandbox to live credentials
- [ ] Test live $8 payment end-to-end

### Code repo cleanup (noticed in git status)
- [ ] Decide fate of write_brief.py (untracked) — delete or commit
- [ ] Commit .cursorignore changes
- [ ] Stop tracking .DS_Store

---

## Next Session Starting Point (Saturday April 18, 2026)

**5-minute warm-up (Supabase dashboard + Gmail, no code)**
1. Set Site URL + Redirect URLs in Supabase Authentication settings
2. Configure session duration 30-90 days
3. Check Gmail Send As — aliases should have auto-propagated overnight; finish "Reply from same address" setting

**Launch-blocker content fix (15 min)**
4. Rewrite Terms of Use section to match new account-based unlock model (use same rewrite_legal.py pattern)

**Main work — Frontend wiring (1-2 hours focused)**
5. Add supabase-js CDN → Face 0 signup form → magic-link flow → profile fetch
6. Replace localStorage unlock gate with profiles.has_paid
7. Supabase Edge Function for PayFast ITN → replace placeholder notify URL at line 1877
8. E2E test full signup → payment → unlock flow

**Then (if time / fresh head)**
9. DKIM for qncacademy.com
10. Investigate "Turn on Gmail — Required" banner

### April 17, 2026 — late session — Terms of Use rewrite (launch-blocker closed)
- [x] Terms of Use section rewritten for account-based unlock model
- [x] New section 2 "Your Account" — magic-link, no passwords
- [x] New section 4 "Payment and Unlock" — account-tied, survives device changes
- [x] New section 5 "Cooling-off Waiver and Refunds" — explicit CPA/EU waiver language
- [x] New section 6 "Account Deletion" — 30-day deletion, unlock dies with account
- [x] Contact aligned to privacy@qncacademy.com
- [x] rewrite_terms.py committed (same safety pattern as rewrite_legal.py)
- [x] Commit 983cc5a pushed — live on GitHub Pages
- [x] runCalculation verified at line 1983 before and after (unchanged)

### Legal docs now fully aligned
All five modified tabs (Privacy Policy, Terms of Use, POPIA & Data, Security, Intellectual Property) reflect the Supabase/account-era reality. Disclaimer tab untouched (no account-model claims in it — still accurate).

### April 17, 2026 — late session — Terms of Use rewrite (launch-blocker closed)
- [x] Terms of Use section rewritten for account-based unlock model
- [x] New section 2 "Your Account" — magic-link, no passwords
- [x] New section 4 "Payment and Unlock" — account-tied, survives device changes
- [x] New section 5 "Cooling-off Waiver and Refunds" — explicit CPA/EU waiver language
- [x] New section 6 "Account Deletion" — 30-day deletion, unlock dies with account
- [x] Contact aligned to privacy@qncacademy.com
- [x] rewrite_terms.py committed (same safety pattern as rewrite_legal.py)
- [x] Commit 983cc5a pushed — live on GitHub Pages
- [x] runCalculation verified at line 1983 before and after (unchanged)

### Legal docs now fully aligned
All five modified tabs (Privacy Policy, Terms of Use, POPIA & Data, Security, Intellectual Property) reflect the Supabase/account-era reality. Disclaimer tab untouched (no account-model claims in it — still accurate).
