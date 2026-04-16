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
grep -n "function runCalculation" /Users/madcarl/Projects/quantumcube/quantum-cube-v10.html
If it returns empty — restore from git before proceeding.

---

## FILE LOCATIONS
/Users/madcarl/Projects/quantumcube/
├── quantum-cube-v10.html                   ← THE APP (single file, ~12MB)
├── PROJECT_BRIEF.md                        ← This document
├── cube-background.jpg                     ← Milky Way background (in repo)
├── Cube Sides/                             ← Cube face images (gitignored — embedded in HTML)
├── Videos/                                 ← Video local backups (gitignored)
└── audio/                                  ← All audio files (gitignored)

**GitHub Repo:** https://github.com/quantumneurocreations-dot/quantumcube
**Live URL:** https://quantumneurocreations-dot.github.io/quantumcube/quantum-cube-v10.html
**Gitignored:** Videos/, Music/, Sounds/, Video Thumbnails/, Backup/, .DS_Store, More backgrounds/, Cube Sides/

---

## DEV ENVIRONMENT
Machine: Mac Mini (madcarl)
Project path: /Users/madcarl/Projects/quantumcube
Editor: Cursor + Terminal
Node.js: v25.9.0
cwebp: Installed via Homebrew
SSH Key: Authenticated to GitHub

Terminal push command:
cd /Users/madcarl/Projects/quantumcube
git add .
git commit -m "description"
git push

---

## WORKFLOW RULES — CRITICAL
- Use Mac Terminal + sed/python3 for CSS and HTML structure changes
- JavaScript changes only via Cursor Claude Code
- Never use sed for JavaScript functions — silently corrupts code
- Python3 for multi-line replacements — safer than sed
- Always verify runCalculation before and after any edit
- Cursor: Start every chat with "Never read the full file. Use Grep to find line numbers, then Read only specific lines, then StrReplace."
- .cursorignore already in place — prevents indexing of large files
- Always run git log --oneline -5 before making changes

---

## HOW TO WORK ON THE FILE
Simple CSS/HTML = Mac Terminal. JavaScript = Cursor Claude Code only.

If in Cursor with Claude Code:
1. File is at /Users/madcarl/Projects/quantumcube/quantum-cube-v10.html
2. Do NOT read the full file — Grep first, then read specific lines
3. File is ~12MB — do NOT upload to chat
4. Use live URL for visual checks
5. After edits: git add, commit, push

---

## TECH STACK
- Single HTML file — no framework, no backend, no database
- Vanilla JavaScript — all calculations client-side
- CSS3 — 3D transforms, glassmorphism, custom animations
- Fonts: Cinzel Decorative (logo), Cinzel (labels/UI), Cormorant Garamond (body text)
- Payment: PayFast (sandbox credentials active)
- Videos: Vimeo — Player API active, fake fullscreen on play
- Audio: Base64 embedded (currently disabled)
- Hosting: GitHub Pages
- PWA: Web manifest, service worker (cache: qc-v11)
- Background: Milky Way image (cube-background.jpg) behind CSS starfield
- Cube faces: 6 WebP images base64 embedded, 160x160px locked, 50% transparency overlay

---

## APP STRUCTURE — 7 FACES
Face 0 | Entry / Sign Up Form       | Complete | No video
Face 1 | Introduction               | Complete | Portrait 9:16
Face 2 | Results Explained          | Complete | 3x Landscape 16:9
Face 3 | Numerology Results         | Complete | No video
Face 4 | Astrology & Horoscope      | Complete | No video
Face 5 | Combined Results           | Complete | No video
Face 6 | Complete / Outro           | Complete | Portrait 9:16
Face 7 | Settings / Launch Guide    | Complete | No video

---

## VIMEO VIDEOS
All videos: Hide from Vimeo, embeddable anywhere, Downloads OFF, Comments OFF.

Face 1 | Introduction         | 1183086210 | Portrait 9:16
Face 2 | Numerology Explained | 1183086853 | Landscape 16:9
Face 2 | Results Explanation  | 1183087269 | Landscape 16:9
Face 2 | Astrology            | 1183087951 | Landscape 16:9
Face 6 | Cube Outro           | 1183103519 | Portrait 9:16

Video behaviour: fake fullscreen via CSS on play. Portrait videos stay portrait always.
Landscape videos unlock phone rotation on play via Screen Orientation API, relock to portrait on pause/end.

---

## VISUAL DESIGN — KEY DECISIONS (DO NOT CHANGE)
- Background: Milky Way image (cube-background.jpg) + CSS starfield on top
- Starfield: 220 stars, round glowing dots
- Cube: Glass effect, cyan-white glowing edges 2px border
- Cube face images: 6 WebP base64 embedded, 160x160px locked, background-blend-mode multiply rgba(0,0,20,0.5)
- Cube face mapping: Front=Face1 Introduction, Right=Face2 Results, Back=Face3 Numerology, Left=Face4 Astrology, Top=Face5 Combined, Bottom=Face6 Outro
- Logo: QUANTUM top, CUBE right-aligned, cyan glow + float animation
- All cards: glass style, margin 0 16px 20px 32px
- Lock screens: same margins as sign-up card
- Scoreboard, matrix, card-stack, astro-grid, combo-full: all have matching side margins (32px left, 16px right)
- Video-face on Face 2: margin 0 16px 16px 32px
- Lock card content: "Complete Quantum Cube Unlock", & between Chinese Horoscope and Combined Interpretation, $ 8.00, Unlock button (narrow, centered)
- Three fixed buttons bottom-right: 👄 narrator (top, 108px), 🎵 music (middle, 64px), 🔇 mute (bottom, 20px)
- Combined portrait: no drop cap, starts with "You are someone..."
- Face 6 outro: only "Your Journey Complete" heading + video (icon/title/text removed)
- Legal footer: Terms of Use + Disclaimer, class=lock-footer, hidden on unlock, restored on reset
- PWA orientation: portrait, unlocks during landscape video play

---

## CUBE BEHAVIOUR
- Hidden on Face 0, visible on all other faces
- Idle auto-rotation after 1 second of no touch
- Drag rotates cube, no snap-back on release
- Snap only on face tap or showFace()
- Touch glow: frames light up to 100% when touched
- Permanent 30% frame glow at rest

---

## PAYMENT SYSTEM
- Gateway: PayFast (SA only) — needs Stripe/Paddle for global
- Price: $8 USD once-off
- Status: Sandbox active, not live
- "Try Demo (test mode)" button — DELETE before going live

---

## CONTENT LOCATIONS IN HTML
Numerology content: const NUM = { ... }   // Search: // ═══ CONTENT DATA ═══
NUM.lp = Life Path        // 3 variations per number DONE
NUM.bd = Birthday Number  // needs 3 variations
NUM.ex = Expression       // needs 3 variations
NUM.su = Soul Urge        // needs 3 variations
NUM.pe = Personality      // needs 3 variations
NUM.hp = Hidden Passion   // needs 3 variations
NUM.kl = Karmic Lessons   // needs 3 variations
NUM.pc = Life Phases      // needs 3 variations
NUM.py = Personal Year    // needs 3 variations

Western Zodiac: const WSIGN  // Search: // ═══ WESTERN SIGN DATA ═══
Chinese Zodiac: const CSIGN  // Search: // ═══ CHINESE SIGN DATA ═══
144 Combinations: const COMBOS // Search: // ═══ COMBINATION DATA ═══
Combined Portrait: function buildCombinationNarrative(data)

---

## WHAT STILL NEEDS TO BE DONE

### PRIORITY 1 — Content Variations (BIGGEST PRIORITY)
- [ ] Birthday Number (11 numbers) — 2 more variations each
- [ ] Expression (13 numbers) — 2 more variations each
- [ ] Soul Urge (13 numbers) — 2 more variations each
- [ ] Personality (11 numbers) — 2 more variations each
- [ ] Hidden Passion (9 numbers) — 2 more variations each
- [ ] Karmic Lessons (9 numbers) — 2 more variations each
- [ ] Life Phases (11 numbers) — 2 more variations each
- [ ] Personal Year (11 numbers) — 2 more variations each

### PRIORITY 2 — Content Accuracy Review
- [ ] Verify all numerology interpretations
- [ ] Verify all Western astrology content
- [ ] Verify all Chinese zodiac content
- [ ] Verify all 144 combination readings
- [ ] Review combined portrait quality

### PRIORITY 3 — Narrator Voice (ElevenLabs)
- [ ] Wire 👄 button to ElevenLabs API
- [ ] Male/female voice toggle
- [ ] API key already set up in Academy — reuse same key
- [ ] Auto-play reading when result card opens

### PRIORITY 4 — Audio
- [ ] Re-enable audio (uncomment ~2 lines in JS)
- [ ] Test all 6 sounds on device

### PRIORITY 5 — Payments
- [ ] Switch PayFast to Stripe or Paddle for global
- [ ] Remove Try Demo button before go-live
- [ ] Test live $8 payment

### PRIORITY 6 — App Stores
- [ ] Google Play: PWABuilder.com → .aab → $25 USD dev account
- [ ] Apple App Store: Capacitor → Xcode → $99/yr dev account

### PRIORITY 7 — Final Polish
- [ ] Final QA pass all faces on device
- [ ] Add testimonials/social proof section
- [ ] Add sharing mechanism for readings
- [ ] Email capture or PWA push notification opt-in
- [ ] Mouse glow on desktop (mousedown/mouseup)
- [ ] Spike star CSS cleanup (harmless but present)

---

## STRATEGIC NOTES
- Content variations are the single biggest priority before launch
- PayFast is SA only — need Stripe/Paddle for international sales
- No user accounts yet — consider email + localStorage
- No sharing mechanism — users should be able to share readings

---

## SEPARATE PROJECT — QNC ACADEMY
Path:  /Users/madcarl/Projects/qnc-academy/
Stack: Vercel + Supabase + ElevenLabs + GitHub
URL:   qnc-academy.vercel.app
Status: Active development — COMPLETELY SEPARATE CHAT
Never bring Academy work into Quantum Cube chats and vice versa.

---

## NEXT SESSION STARTING POINT
1. Run: grep -n "function runCalculation" quantum-cube-v10.html — must return a line number
2. Check cube face image transparency — currently 50% via rgba(0,0,20,0.5), adjust if needed
3. Narrator button 👄 is in place but not wired up — next big feature to build
4. Content variations are #1 priority for launch readiness
5. Try Demo button needs removing before go-live
