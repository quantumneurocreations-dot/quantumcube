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

### April 17, 2026 — Evening session (post-Terms rewrite)

#### Shipped
- [x] Terms of Use section rewritten for account-based unlock model (commit 983cc5a)
- [x] rewrite_terms.py committed alongside rewrite_legal.py (same safety pattern)
- [x] Session log dedupe (commit 17879e4)

#### Supabase URL Configuration
- [x] Site URL set: https://quantumneurocreations-dot.github.io/quantumcube/quantum-cube-v10.html
- [x] Redirect URL #1: GitHub Pages URL
- [x] Redirect URL #2: https://quantumcube.app/quantum-cube-v10.html
- [x] Single-session-per-user: OFF (matches Terms "sign in from any device")
- [x] Session duration: Pro-plan-gated; free tier defaults (never/user-logout-only) acceptable for launch

#### Email authentication stack for qncacademy.com — COMPLETE
- [x] "Turn on Gmail — Required" banner diagnosed — it was DKIM
- [x] DKIM generated via Google Workspace (2048-bit)
- [x] DKIM TXT record added to Cloudflare at google._domainkey.qncacademy.com
- [x] DKIM verified live: dig +short TXT google._domainkey.qncacademy.com returns v=DKIM1;...
- [x] DMARC Management enabled on Cloudflare (Beta feature, aggregates reports)
- [x] DMARC policy: p=none (monitor-only starter, tighten to quarantine/reject later)
- [x] SPF: soft fail (~all) — Google Workspace standard, already in place
- [x] All three email auth pillars (SPF + DKIM + DMARC) now live

#### Still outstanding (carried forward)
- [ ] Re-check DMARC dashboard in ~24h for first reports
- [ ] Consider tightening DMARC from p=none to p=quarantine after 1-2 weeks of clean reports
- [ ] Send As aliases propagation (still pending)
- [ ] 2FA on all 3 partner Workspace accounts
- [ ] All frontend wiring items (unchanged from earlier log)

#### Commits this session
- 983cc5a — Rewrite Terms of Use for account-based unlock model
- 17879e4 — Dedupe accidentally-doubled Terms rewrite session log block
- (plus the session log append itself, committed next)

---

## CONSOLIDATED HANDOFF — End of April 17, 2026

This section consolidates everything the next session needs to know. If you read only one section, read this one.

### Authentication model — LOCKED IN, awaiting frontend wiring

**Method:** Supabase magic-link (email OTP). No passwords, ever.

**Flow end-to-end:**
1. User opens the app. Face 0 shows a sign-up form.
2. User enters email address + optionally ticks "Email me updates" checkbox (unchecked by default).
3. App calls `supabase.auth.signInWithOtp({ email, options: { data: { marketing_consent: true|false } } })`.
4. Supabase sends a one-time sign-in link to the user's email (from Supabase's default sender; can be customised later via custom SMTP).
5. User clicks the link in their email. Link opens `https://quantumneurocreations-dot.github.io/quantumcube/quantum-cube-v10.html#access_token=...`.
6. Frontend detects the `#access_token=` hash fragment on page load and swaps the user into "signed in" state.
7. Frontend fetches the user's profile row: `supabase.from('profiles').select().single()`.
8. UI gates locked content on `profiles.has_paid` (not on localStorage anymore).

**Backend is already done:**
- `auth.users` INSERT trigger auto-creates a `public.profiles` row with `email` + `marketing_consent` from user_metadata
- RLS: users can read/update their own row only
- `has_paid` is immutable from client — only server-side code (PayFast webhook Edge Function) can flip it to true

**Session duration:** Free-tier Supabase default = sessions persist until explicit sign-out (no inactivity or absolute timeout). This is more user-friendly than the 30-90 days mentioned in earlier planning and is acceptable for launch. Revisit if we upgrade to Pro or if security posture tightens.

### Credentials reference (already saved to gitignored .supabase-env)
- SUPABASE_URL = https://fqqdldvnxupzxvvbyvjm.supabase.co
- SUPABASE_ANON_KEY = sb_publishable_wp2cRcjgyJcarRVuq_Q1zw_Vd68AEcZ
- SUPABASE_PROJECT_ID = fqqdldvnxupzxvvbyvjm
- Organization: Quantum Neuro Creations (ybhwpcakkaveapdztnrs)
- Region: eu-central-1 (Frankfurt) — matches POPIA policy
- Academy's project remains in eu-west-1 — SEPARATE, do not touch

### Frontend wiring checklist (tomorrow's main launch-blocker work)

Do these in order, commit between each bullet, verify runCalculation at line 1983 before/after each HTML change.

**1. Add supabase-js SDK to the HTML**
- Import via CDN inside `<head>` or just before closing `</body>`
- Initialise `const sb = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY)`

**2. Replace Face 0 signup form**
- Email input (type=email, required)
- Marketing consent checkbox, UNCHECKED by default, label "Email me updates about Quantum Cube"
- "Send magic link" button (rename from current Unlock/Submit button)
- Loading state ("Check your email for a sign-in link")
- Error state ("Something went wrong, try again")

**3. Wire signup action**
- Button onclick → `sb.auth.signInWithOtp({ email, options: { data: { marketing_consent } } })`
- Handle promise: success → show "Check your email", error → show message

**4. Handle magic-link callback on page load**
- On page load, check `window.location.hash` for `#access_token=`
- If present, Supabase SDK auto-handles session persistence; we just clean the URL and flip UI to signed-in state

**5. Fetch profile on sign-in**
- `const { data: profile } = await sb.from('profiles').select().single()`
- Read `profile.has_paid` → gate unlock UI

**6. Replace localStorage unlock gate**
- Current code at line 1813: `const STORE_KEY = "qc_unlocked_v1"`
- Keep localStorage as a CACHE (fast first paint), but source of truth is `profile.has_paid`
- On sign-in: if `profile.has_paid === true`, set localStorage AND unlock UI. If false, clear localStorage.

**7. Supabase Edge Function: PayFast ITN webhook**
- Create Edge Function `payfast-webhook` in Supabase project
- Function receives POST from PayFast on successful payment
- Validates PayFast ITN signature (security-critical — use PayFast's documented verification)
- Looks up user by email or passed m_payment_id
- Flips `profiles.has_paid = true` via service-role key
- Replace placeholder URL at line 1877: `https://YOUR-SERVER.com/payfast-notify` → actual Edge Function URL

**8. Sign-out flow**
- Add sign-out button (in settings/Face 7, or a small "sign out" link)
- `await sb.auth.signOut()` → clear localStorage cache, return to Face 0

**9. End-to-end test (use PayFast sandbox)**
- Fresh incognito window
- Sign up with test email
- Open email, click magic link
- Verify signed-in state, has_paid=false, unlock UI locked
- Click Unlock → complete PayFast sandbox payment → return to app
- Verify has_paid=true, unlock UI open
- Sign out, sign back in on a different device/browser → verify unlock persists

### Other outstanding items

**Gmail / Workspace (quick tomorrow AM check, ~5 min):**
- Send As aliases — should have auto-propagated overnight; finish in Gmail Settings → Accounts
- "Reply from the same address" — enable once Send As has 2+ addresses
- Check DMARC Management dashboard for first reports (24h after enable)
- 2FA on all 3 partner Workspace accounts — verify enabled (Security section claim in legal docs)

**Pre-launch removal checklist (do these last, right before going live):**
- Remove "Try Demo (test mode)" buttons at lines 608, 644, 678, 710
- Remove `unlockDemo()` JS function entirely
- Switch PayFast from sandbox to live credentials in the process action at lines 1871-1872

**Code repo cleanup (low priority):**
- Decide fate of write_brief.py (untracked) — delete or commit
- Commit .cursorignore changes
- Stop tracking .DS_Store

### Systems live at end of today

| System | State |
|---|---|
| GitHub Pages | Live, serving latest commit 799bf0c |
| quantumcube.app domain | Registered, DNS managed by Cloudflare |
| qncacademy.com domain | Registered, DNS managed by Cloudflare |
| Google Workspace | admin@qncacademy.com active, 5 aliases created |
| Gmail inbox filters | 5 rules auto-label incoming mail by recipient alias |
| Cloudflare Email Routing | *@quantumcube.app → admin@qncacademy.com (active) |
| Email auth qncacademy.com | SPF (soft fail) + DKIM + DMARC (p=none) all live |
| Supabase project | quantum-cube in Frankfurt, ACTIVE_HEALTHY, free tier |
| Supabase schema | profiles table with RLS + auto-create trigger |
| Supabase auth config | Site URL + 2 redirect URLs set, magic-link ready |
| Legal docs | Privacy + POPIA + Security + Terms all align with account model |
| Legal docs | Disclaimer + IP + Epidemic Sound credits unchanged (still accurate) |
| runCalculation | Stable at line 1983 throughout all HTML rewrites today |

### First 3 things to run at start of next session

```bash
# 1. Sanity check runCalculation hasn't moved
grep -n "function runCalculation" /Users/qnc/Projects/quantumcube/quantum-cube-v10.html

# 2. Verify Supabase credentials are still in place
cat /Users/qnc/Projects/quantumcube/.supabase-env

# 3. Confirm email auth still resolves
dig +short TXT google._domainkey.qncacademy.com
```

All three should return non-empty. If any returns empty, STOP and diagnose before continuing.

### Audit catch — flagged before close of April 17 session

**Marketing email path — must build before first campaign goes out:**
Privacy Policy and POPIA sections currently promise users can "withdraw consent at any time from a link in any marketing email" and that "marketing emails are sent only on the basis of affirmative, opt-in consent." Backend records `marketing_consent` correctly on signup. What's NOT yet built: the actual marketing email sending pipeline, the unsubscribe link in those emails, and the endpoint that flips `profiles.marketing_consent=false` when someone unsubscribes. No urgency (zero marketing emails being sent today), but before the first campaign this path must exist or the legal docs become false.

**Cross-project note — confirm Academy chat was updated:**
Academy project chat needed a sync covering: shared Workspace status, separate Supabase projects in different regions, shared legal decisions (privacy@ as Information Officer, 30-day deletion, age 18+), no new shared recurring costs. If this wasn't pasted into the Academy chat yet, find the paste in the April 17 chat history before closing that chat.

---

## SESSION LOG — April 17, 2026 — Frontend Wiring Day (Supabase Auth)

### Shipped to production (5 commits, all live)

- **90ff35c** — Chunk 1: Supabase JS SDK v2.45.4 loaded via cdn.jsdelivr.net, `sb` client initialised just before </head>. Stray `>` on line 11 fixed.
- **b82a157** — Cleanup: Removed two duplicate copies of `updateCalcBtnReady` (was at lines 24, 429, 2323 — kept only line 24). Pre-existing structural issue, not introduced by today's chunks. The line-429 copy was glued inside `<script src="https://player.vimeo.com/api/player.js">` (dead code — browsers ignore inline content when src is set). The line-2323 copy was a runtime duplicate that double-registered input listeners. File is now structurally clean.
- **fc5fc5a** — Chunk 2: Email field added to Face 0 form (between Last Name and Day). Marketing consent checkbox added (unchecked default, "Email me updates about Quantum Cube"). `updateCalcBtnReady` extended to require valid email format before "Reveal My Cube" lights up.
- **(2b shipped in same workflow)** — Custom cyan-glow styling for marketing consent checkbox to match cube aesthetic. Native checkbox hidden, custom 20×20 box with cyan glow on check, clickable label, hover state.
- **1108396** — Chunk 3: Magic-link signup flow wired end-to-end. `handleRevealClick()` validates → saves to localStorage `qc_pending_profile_v1` → calls `sb.auth.signInWithOtp` with `marketing_consent` in user_metadata → shows cyan banner → calls `runCalculation()` so user sees reading immediately without waiting for email. `initSupabaseSession()` runs on page load to detect existing sessions and fetch profile. `onAuthStateChange` listener handles SIGNED_IN/SIGNED_OUT events. `restorePendingProfile()` refills form after magic-link return.
- **c476a5f** — Chunk 4: `profiles.has_paid` is now source of truth for unlock state. Added `syncUnlockFromProfile()` — called from `initSupabaseSession` and `onAuthStateChange`. localStorage `qc_unlocked_v1` retained as a fast-path cache for first paint, but if backend says `has_paid=false` and local cache says unlocked, local cache is cleared and UI re-locks (handles unlock revocation). PayFast flow itself unchanged in this chunk — still sets localStorage on success client-side. Server-side flip happens in Chunk 5.

### Verified live end-to-end

Chunk 3 tested via real magic-link round trip (Claude in Chrome assisted with browser-side verification):
- Reveal button transitions through "Sending sign-in link..." state
- Cyan banner appears on Face 0 with correct success message
- Magic-link email arrives in inbox within ~2s (sender: Supabase default)
- Clicking link returns user to app in signed-in state
- Cube rotates to Face 1, reading calculates normally
- No console errors. HTTP 200 from Supabase OTP endpoint, ~1.7s response time.
- Profile auto-created via auth.users INSERT trigger, has_paid=false (correct — no payment yet, so Faces 3-6 still locked, which is expected behaviour)

### Python replacement scripts committed (same safety pattern as rewrite_legal.py / rewrite_terms.py)

- wire_supabase_01_setup.py
- cleanup_duplicate_fn.py
- wire_supabase_02_form.py
- wire_supabase_02b_consent_style.py
- wire_supabase_03_submit.py
- wire_supabase_04_unlock_gate.py

Each script asserts exact-match anchors before writing and verifies `runCalculation` line is still present before/after. Backup files generated by cleanup script: `quantum-cube-v10.html.bak-cleanup-20260417-151711`.

### Carried forward — known UX paper-cut

- **Magic-link banner flashes too briefly.** Banner appears on Face 0 but face-rotation to Face 1 hides it within ~100ms — user effectively never sees the confirmation. Two fix options for next session: (a) delay face transition by 1.5-2s after banner appears, or (b) move banner to render as a toast on Face 1 instead. Identified in live test, not blocking, polish item.

### Major blocker raised — payment processor + pricing decision

Pre-Chunk 5 (PayFast Edge Function) work paused pending team decision. Real findings:

**Decision context: PayFast is SA-only. Need global processor for $8 USD product.**

**Paddle (initial preference):** 5% + $0.50 per transaction. Acts as merchant of record (handles VAT/sales tax in 100+ jurisdictions). However: (a) Paddle's standard pricing is designed for $10+ products — sub-$10 requires negotiated bespoke pricing via sales team, not self-serve signup, (b) approval process can take days to weeks, (c) on $8 the standard fee = $0.90 = ~11% effective rate.

**Lemon Squeezy (alternative checked):** Same headline fees as Paddle (5% + $0.50, +1.5% intl). No explicit sub-$10 minimum. **However: acquired by Stripe July 2024, currently being absorbed into "Stripe Managed Payments" (Stripe's new MoR). Lemon Squeezy team has openly admitted slower support / less frequent updates during transition. Existing users will be migrated to Stripe Managed Payments in 12-24 months. Not worth signing up only to face a forced platform migration.**

**Stripe direct (non-MoR option):** ~3.4% + $0.30 = $0.57 on $8 = ~7% effective. Would need to handle international tax compliance ourselves (Stripe Tax adds ~0.5%). Cheaper but pushes operational burden onto the team.

**The real issue:** $8 is below the price point where MoR economics work cleanly. The fixed $0.50 portion of MoR fees is designed for $20+ products. Any MoR will charge ~11-13% on $8.

**Three live options pending team conversation:**
1. **Bump Cube price** to $11 or higher to fit standard MoR pricing tiers (Paddle/LS becomes ~9.5% effective at $11). The number 8 numerology can be preserved via different presentation ($18, $28, $88).
2. **Stripe direct for Cube + Paddle for Academy** — different processors per product. Cube ships fast at lower fees but team handles tax. Academy gets MoR treatment because higher pricing makes the math work.
3. **Accept ~12% on Cube** if expected volume justifies it.

**Decision owner:** Keyzer (marketing/finance partner) + Ronnie + Michelle. Decision needs to happen before Chunk 5 work resumes.

### What was confirmed in this session about cross-product separation

If Cube and Academy use the same payment processor account, products are kept distinct via:
- Separate Product/Price records in the processor dashboard (Cube vs Academy)
- Custom `metadata: { app: "quantum_cube" | "qnc_academy" }` on every checkout
- Separate Supabase Edge Function webhooks per project (Cube webhook validates app=quantum_cube, Academy webhook validates app=qnc_academy, refuses cross-contamination)
- Separate `has_paid` columns in each project's database (Cube in eu-central-1, Academy in eu-west-1, never shared rows)

One processor account, two products is the recommended pattern. Cleaner accounting, single login, recognises customers who buy both.

### Next session starting point

**Pre-work (team conversation, not coding):**
- Decide: Cube price (stay $8 / bump to $11 / use $18 or $88 numerology variant)
- Decide: payment processor (Paddle / Stripe direct / Stripe + Paddle hybrid / something else)
- These two decisions unblock Chunk 5

**Once decisions made, in order:**
1. Sign up with chosen processor (Paddle approval may take days — start early)
2. Get sandbox/test credentials, store in gitignored env file
3. Update HTML pricing if changed (line ~671, ~707, ~741, ~773, ~792 — all five lock-screen "$ 8.00" instances)
4. Update Privacy/Terms references to PayFast (Privacy line 2338, Terms line 2375, IP line 2428, POPIA section)
5. Chunk 5: Supabase Edge Function for webhook (signature validation per processor's docs)
6. Replace placeholder URL at line ~1877 in HTML with deployed Edge Function URL
7. E2E test: signup → magic link → checkout → webhook flips has_paid → unlock UI opens

**Then post-payment polish:**
- Fix magic-link banner flash (2-second delay or toast on Face 1)
- Pre-launch removal: Try Demo buttons (lines 608, 644, 678, 710, 2528) + unlockDemo() function
- DKIM dashboard re-check (24h after enable)
- Send As aliases propagation check
- 2FA verification on all 3 partner Workspace accounts

### Backup files cleanup needed

- `quantum-cube-v10.html.bak-20260417-123829` (untracked)
- `quantum-cube-v10.html.bak-20260417-132006` (untracked)
- `quantum-cube-v10.html.bak-cleanup-20260417-151711` (created today)
- Add `*.bak-*` to `.gitignore`, then delete locally


---

## SESSION LOG — April 17, 2026 — Night Session (Banner + Timing Polish)

### Shipped (4 more commits on top of morning/afternoon work)

- **7783718** — Chunk 5: Added countdown banner ("Continuing in 3..." ticker) and mirrored marketing consent checkbox added to all 4 lock cards. Visual/timing felt wrong in testing.
- **487f48e** — Chunk 6: Replaced countdown with two-stage banner flow (Verify your email / Check your inbox). Still felt off visually.
- **90c9756** — Chunk 7: Major UX rework. Killed the separate glass banner card entirely. Reused the existing `#errMsg` slot below Day/Month/Year to show either "Please complete all fields" (red validation) or "Verify your email" (cyan success) via a new `.err-msg.success` class. Added Cinzel caps + glow + bigger font. Button cycles SENDING → EMAIL SENT.
- **32c59ae** — Chunk 8: Critical timing + dead-code fix. The choreography now starts IMMEDIATELY on click (not after Supabase API returns), so users see the full 3s SENDING + 3s EMAIL SENT regardless of API latency. Stripped leftover `showMagicLinkBanner()` calls from init + onAuthStateChange (banner element was deleted in Chunk 7, calls were throwing silent ReferenceErrors). Strengthened errMsg centering with margin auto.

### Live-verified

- Fresh incognito + unused email → full 6-second sequence plays correctly: button SENDING (3s) → EMAIL SENT (3s) → face rotate. Magic link arrives in inbox.
- Rate-limited email → handler correctly aborts rotate, shows "Could not send: EMAIL RATE LIMIT EXCEEDED" in red styling, stays on Face 0.
- Both happy path and error path working as designed.

### Open decisions / paused items

**1. Payment processor + pricing.** Still unresolved after team call. Options discussed: Paddle (under-$10 gotcha), Lemon Squeezy (being absorbed into Stripe Managed Payments — avoid), Stripe direct (cheaper, team handles tax). Price bump from $8 decided in principle; specific number TBD (candidates: $11, $18, $28, $88). Decision owner: Ronnie/Michelle/Keyzer. Paddle registration confirmed to NOT require going live — sandbox works indefinitely — so we can build Chunk 5 (webhook Edge Function) without commitment.

**2. Lock-card marketing consent checkbox — STILL BROKEN.** Chunk 5 inserted the checkboxes into all 4 lock cards (Face 3/4/5/6) but the `.consent-box` CSS styling isn't applying in those contexts. Checkbox appears as a small cyan arrow artifact instead of the proper styled box (per user screenshot). Not reverted. Diagnosis needed: CSS specificity inside `.lock-screen` likely overrides the base `.marketing-consent` rules. Next session: either fix the CSS or move the checkbox out of the lock-screen block entirely.

**3. Error message copy.** Supabase errors surface as raw uppercase strings ("EMAIL RATE LIMIT EXCEEDED"). Not urgent but worth a friendly rewrite before launch — map common Supabase error codes to human-readable English.

**4. Email template branding.** Supabase's default "Confirm Your Signup" email from `noreply@mail.app.supabase.io` is not brand-aligned. Three levels of fix available:
   - L1 (free, 10 min): edit the template copy in Supabase dashboard
   - L2 (moderate): custom SMTP via Resend/Postmark/Google Workspace → sender becomes `hello@qncacademy.com` or similar
   - L3: full HTML branded template
   Recommended: L1 before launch; L2 when ready. NOT urgent.

**5. Face 7 (Settings) and cube tweaks.** User flagged there are specific changes wanted on Face 7 and elsewhere on the cube. List not yet captured. Ask for it at start of next session.

### Python replacement scripts committed tonight
- wire_supabase_05_banner_mirror.py (superseded)
- wire_supabase_06_banner_v2.py (superseded)
- wire_supabase_07_inline_msg.py (current approach)
- wire_supabase_08_timing_fix.py (current timing)

### Next session starting point

**Warm-up (2 min terminal checks):**
```bash
grep -n "function runCalculation" /Users/qnc/Projects/quantumcube/quantum-cube-v10.html
cat /Users/qnc/Projects/quantumcube/.supabase-env
```

**Then in order of proposed priority:**
1. Capture the Face 7 + cube change list from the user
2. Fix the broken lock-card checkbox (Chunk 5 tail)
3. Decide pricing + payment processor (team decision needed)
4. Once decided: register sandbox account with chosen processor
5. Chunk 9 (or equivalent): Supabase Edge Function for payment webhook
6. Level 1 email template branding in Supabase dashboard (10 min task)
7. Friendly error message mapping for handleRevealClick

### Everything still working at end of session
- runCalculation at line 2197 (moved 16 lines across the night's work)
- Supabase magic-link signup: functional end-to-end
- Magic-link email delivery: confirmed working via quantumneurocreations@gmail.com
- profiles.has_paid is source of truth for unlock state
- Chrome + Safari tested
- No regressions in runCalculation, resetAll, showFace, or the cube rotation

