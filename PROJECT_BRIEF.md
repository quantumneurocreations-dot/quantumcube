# QUANTUM CUBE — MASTER PROJECT DOCUMENT
**Version: v10 | Last Updated: April 16, 2026**

---

## ⚠️ CRITICAL RULE — ALWAYS READ FIRST
**Quantum Cube and QNC Academy are COMPLETELY SEPARATE projects.**
- Never mix code, files, credentials, or platforms between them
- Quantum Cube lives on **GitHub Pages only** — no Vercel, no Supabase
- Academy lives on Vercel + Supabase — never touches Quantum Cube
- Always confirm which project you are working on before making any changes

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
