# QUANTUM CUBE — MASTER PROJECT DOCUMENT
**Version: v10 | Last Updated: April 15, 2026**

---

## ⚠️ CRITICAL RULE — ALWAYS READ FIRST
**Quantum Cube and QNC Academy are COMPLETELY SEPARATE projects.**
- Never mix code, files, credentials, or platforms between them
- Quantum Cube lives on **GitHub Pages only** — no Vercel, no Supabase
- Academy lives on Vercel + Supabase — never touches Quantum Cube
- Always confirm which project you are working on before making any changes

---

## FILE LOCATIONS
```
/Users/madcarl/Projects/quantumcube/        ← MAIN PROJECT FOLDER
├── quantum-cube-v10.html                   ← THE APP (single file, ~11.5MB)
├── PROJECT_BRIEF.md                        ← This document
├── Videos/                                 ← Video local backups (gitignored)
└── audio/
    ├── ES_Dream_Focus_Beta_Waves.mp3       ← Background binaural music
    ├── Opening_app.wav                     ← App open sound
    ├── Cube_Side_Selection.wav             ← Cube tap sound
    ├── rotate_cube.wav                     ← Cube rotation sound
    ├── Pop1.mp3                            ← Result card expand sound
    └── Pop_2.mp3                           ← Result card expand sound alt
```

**GitHub Repo:** https://github.com/quantumneurocreations-dot/quantumcube
**Live URL:** https://quantumneurocreations-dot.github.io/quantumcube/quantum-cube-v10.html
**Note:** Git history was cleaned and fresh repo pushed on April 15, 2026 (videos removed from tracking).
**Gitignored:** Videos/, Music/, Sounds/, Video Thumbnails/, Backup/ — never pushed to repo.


---

## DEV ENVIRONMENT
| Item | Detail |
|------|--------|
| Machine | Mac Mini (madcarl) |
| Project path | /Users/madcarl/Projects/quantumcube |
| Editor | Cursor + Terminal |
| GitHub Desktop | Installed, authenticated |
| Node.js | v25.9.0 |
| SSH Key | Authenticated to GitHub |

**Terminal push command:**
```bash
cd /Users/madcarl/Projects/quantumcube
git add .
git commit -m "description"
git push
```

---

## CHROME TABS NEEDED (Quantum Cube only)
| Platform | URL | Account | Purpose |
|----------|-----|---------|---------|
| **GitHub** | github.com/quantumneurocreations-dot/quantumcube | quantumneurocreations-dot | Push code |
| **Claude Console** | platform.claude.com | Codex / quantumneurocreations | API keys |
| **Vimeo** | vimeo.com/manage/videos | quantumneurocreations@gmail.com | Manage videos |
| **PayFast** | payfast.co.za | TBD | Payment gateway |
| **ElevenLabs** | elevenlabs.io | ElevenCreative | Future voice |

> Note: Vercel and Supabase are Academy-only. Do NOT open them for Quantum Cube work.

---

## HOW TO WORK ON THE FILE
**IMPORTANT: This project requires Cursor + Claude Code. Do NOT use claude.ai for edits.**

If you are reading this on claude.ai and cannot edit files directly, stop and advise the user:
"Please open Cursor, make sure the quantumcube project folder is open, start a new Claude Code chat inside Cursor, and paste this PROJECT_BRIEF.md there. Claude Code can then edit quantum-cube-v10.html directly."

If you are in Cursor with Claude Code:
1. The file quantum-cube-v10.html is at /Users/madcarl/Projects/quantumcube/quantum-cube-v10.html
2. Edit it directly — no need to upload the HTML file
3. File is ~11.5MB (audio base64 embedded) — do NOT upload to chat
4. Use live URL for visual checks: https://quantumneurocreations-dot.github.io/quantumcube/quantum-cube-v10.html
5. After edits: git add, commit, push via Claude Code in terminal
6. Chrome must be open with the Claude extension enabled for visual checks

---

## TECH STACK
- Single HTML file — no framework, no backend, no database
- Vanilla JavaScript — all calculations client-side
- CSS3 — 3D transforms, glassmorphism, custom animations
- Fonts: Cinzel Decorative (logo), Cinzel (labels/UI), Cormorant Garamond (body text)
- Payment: PayFast (sandbox credentials active)
- Videos: Vimeo (Hide from Vimeo, embeddable anywhere) — Player API active, fake fullscreen on play
- Audio: Base64 embedded (currently disabled)
- Hosting: GitHub Pages
- PWA: Web manifest, service worker (cache: qc-v11)

---

## APP STRUCTURE — 7 FACES
| Face | Name | Status | Videos |
|------|------|--------|--------|
| Face 0 | Entry / Sign Up Form | ✅ Complete | None |
| Face 1 | Introduction | ✅ Complete | Introduction (portrait 9:16) |
| Face 2 | Results Explained | ✅ Complete | Numerology + Results Explained + Astrology (landscape 16:9) |
| Face 3 | Numerology Results | ✅ Complete | None |
| Face 4 | Astrology & Horoscope | ✅ Complete | None |
| Face 5 | Combined Results | ✅ Complete | None |
| Face 6 | Complete / Outro | ✅ Complete | Cube Outro (portrait 9:16) |
| Face 7 | Settings / Launch Guide | ✅ Complete | None |

---

## VIMEO VIDEOS — CURRENT STATE
All videos on Vimeo. Privacy: Hide from Vimeo (embeddable anywhere). Downloads OFF. Comments OFF.

| Face | Title | Vimeo ID | Shape |
|------|-------|----------|-------|
| Face 1 | 1 - Introduction | 1183086210 | Portrait (9:16) |
| Face 2 | 2 - Numerology Explained | 1183086853 | Landscape (16:9) |
| Face 2 | 3 - Results Explanation | 1183087269 | Landscape (16:9) |
| Face 2 | 4 - Astrology | 1183087951 | Landscape (16:9) |
| Face 6 | 5 - Cube Outro | 1183103519 | Portrait (9:16) |

Embed URL format: `https://player.vimeo.com/video/ID?badge=0&autopause=0&player_id=0&app_id=58479&title=0&byline=0&portrait=0&dnt=1&color=7dd4fc&api=1&playsinline=1`

Video playback: fake fullscreen via CSS fixed positioning on play event. Auto-collapses on pause/end. Vimeo Player API loaded via player.js.

---

## VISUAL DESIGN — KEY DECISIONS (DO NOT CHANGE)
- Background: Deep space black `#05050f`
- Starfield: 220 stars, all round glowing dots (spike/plus stars removed)
- Cube: Glass effect, cyan-white glowing edges `#7dd4fc`, transparent faces, backdrop-filter blur
- Logo: QUANTUM top, CUBE right-aligned (E under M), CUBE in cyan with glow + float animation
- QUANTUM CUBE words float with subtle x/y drift animation (quantumFloat + quantumFloatB)
- Global logo (header): fixed above cube on all pages — Quantum Neuro Creations / QUANTUM CUBE / Your Cosmic Profile
- Fonts forced with !important — Cinzel Decorative for QUANTUM/CUBE
- All text: White, no text-shadows (removed globally — black background does the work)
- "Period Cycles" → "Life Phases" everywhere
- Combined portrait: drop cap "Y" in "You are..." — no name displayed
- Result card text: centered, 18px body
- Month dropdown: numbers 1–12 (not names)
- Day and year fields: empty by default, max year 2025
- Mute button (sound FX): fixed bottom-right. Music toggle: fixed bottom-right next to mute
- Logo float: continuous elliptical path, linear timing, QUANTUM 6s, CUBE 11s, no stops
- Sign-up form: glass card transparent with backdrop blur, black input backgrounds
- cubeHint hidden on Face 0, visible on all other faces
- Watermark numbers 1-6 on each cube face, Cinzel Decorative 120px, opacity 0.07
- cubeScene height 220px
- Reveal My Cube button: outside glass card, below it, max-width 56.25% centered
- Form input fields: cyan rgba(125,212,252,0.1) background, white border when filled

---

## CUBE BEHAVIOUR
- Hidden on Face 0 (sign-up), visible on all other faces
- Idle auto-rotation after **1 second** of no touch
- Idle rotation only pauses when cube itself is touched (not rest of page)
- Drag rotates cube — no snap-back on release
- Snap only occurs when tapping a face or navigating via showFace()
- Touch glow: frames light up to 100% when touched (JS .touching class)
- Permanent 30% frame glow at rest (::before pseudo-element)
- Cube face labels: Cinzel Decorative, 13px, stacked two-word labels, no icons
- Backdrop-filter: blur(12px) on all faces, gradient opacity = 0 (fully transparent)

---

## SCROLL BEHAVIOUR
- Body scrolls (not #app) — correct for iOS Safari
- Logo area scrolls page via touch relay
- Cube sides/hint area scrolls page via touch relay
- Only cubeWrapper captures rotation touches
- Face content scrolls within body flow

---

## AUDIO SYSTEM (CURRENTLY DISABLED)
All audio is base64 embedded in the HTML file.

**To re-enable, uncomment these lines in the JS:**
```javascript
// Line ~819:
AUDIO.init();

// Line ~822 (interaction listeners):
['pointerdown','touchstart','click'].forEach(ev =>
  document.addEventListener(ev, ()=>AUDIO.startOnInteraction(), {once:true})
);
```

**Audio details:**
- Background music: ES Dream Focus Beta Waves, volume 0.10, loops
- Opening sound: plays on app load
- Cube selection sound: plays on face tap
- Cube rotation sound: plays on drag end
- Pop 1 & Pop 2: alternate on result card expand
- Music pauses on video play, resumes after
- Mute toggle: bottom right 🔊/🔇, persists via localStorage

---

## PAYMENT SYSTEM
- Gateway: PayFast (South Africa) — **needs global alternative, see Strategic Notes**
- Price: **$8 USD once-off unlock** (changed from R88 — going global)
- Status: **Sandbox credentials active** (not live yet)
- To go live:
  1. Register at payfast.co.za (SA only) OR integrate Stripe/Paddle for global
  2. Swap Merchant ID + Merchant Key in `PF_CONFIG` block
  3. Set `sandbox: false`
  4. ~~Update price display in app from R88 to $8~~ ✅ Done
  5. Test payment end-to-end

---

## CONTENT LOCATIONS IN HTML
```javascript
// Numerology content:
const NUM = { ... }          // Search: // ═══ CONTENT DATA ═══
NUM.lp  = Life Path          // 3 variations per number ✅ DONE
NUM.bd  = Birthday Number    // Single string — needs 3 variations
NUM.ex  = Expression         // Single string — needs 3 variations
NUM.su  = Soul Urge          // Single string — needs 3 variations
NUM.pe  = Personality        // Single string — needs 3 variations
NUM.hp  = Hidden Passion     // Single string — needs 3 variations
NUM.kl  = Karmic Lessons     // Single string — needs 3 variations
NUM.pc  = Life Phases        // Single string — needs 3 variations
NUM.py  = Personal Year      // Single string — needs 3 variations

// Variation picker:
function getNumText(cat, num)  // Random pick from array, fallback to string

// Western Zodiac:
const WSIGN = { ... }        // Search: // ═══ WESTERN SIGN DATA ═══

// Chinese Zodiac:
const CSIGN = { ... }        // Search: // ═══ CHINESE SIGN DATA ═══

// 144 Combinations:
const COMBOS = { ... }       // Search: // ═══ COMBINATION DATA ═══

// Combined Portrait:
function buildCombinationNarrative(data)
```

---

## WHAT STILL NEEDS TO BE DONE

### 🔴 Priority 1 — Content Variations
Write 2 additional variations (total 3 per number) for:
- [ ] Birthday Number (11 numbers)
- [ ] Expression (13 numbers)
- [ ] Soul Urge (13 numbers)
- [ ] Personality (11 numbers)
- [ ] Hidden Passion (9 numbers)
- [ ] Karmic Lessons (9 numbers)
- [ ] Life Phases (11 numbers)
- [ ] Personal Year (11 numbers)

### 🔴 Priority 2 — Content Accuracy Review
- [ ] Verify all numerology interpretations are accurate
- [ ] Verify all Western astrology content
- [ ] Verify all Chinese zodiac content
- [ ] Verify all 144 combination readings
- [ ] Review combined portrait quality and flow

### 🟡 Priority 3 — Audio
- [ ] Re-enable audio (uncomment ~2 lines in JS)
- [ ] Test all 6 sounds on device
- [ ] Test music pause/resume on video play

### 🟡 Priority 4 — Payments
- [ ] Register PayFast merchant account
- [ ] Swap sandbox → live credentials
- [ ] Set sandbox: false
- [ ] Test live $8 payment

### 🟢 Priority 5 — App Stores
- [ ] Google Play: PWABuilder.com → .aab → $25 USD dev account
- [ ] Apple App Store: Capacitor → Xcode → $99/yr dev account

### 🟢 Priority 6 — Final Polish
- [ ] Final QA pass all 6 faces on device
- [ ] Update legal documents if needed
- [ ] Review lock screen content

---

## PENDING FIXES FROM LAST SESSION
- [x] **FIXED** — payOverlay CSS bug: R88/Unlock bars showing on Face 0 (April 15)
- [x] **FIXED** — Cube rotation: quaternion system, full 360 freedom, clockwise idle spin
- [x] **FIXED** — Gimbal lock on top/bottom faces
- [x] **FIXED** — Idle timer not restarting after long drag
- [x] **FIXED** — Price updated from R88 to $8 everywhere including legal text
- [x] **FIXED** — Vimeo player: fake fullscreen on play, auto-exit on pause/end (April 15)
- [x] **FIXED** — Auto scroll to top on every face change including iOS Safari
- [x] **FIXED** — Month dropdown default set to 1
- [x] **FIXED** — Responsive glass-card and lock-screen full width on mobile
- [x] **FIXED** — Legal footer added to all faces
- [x] **FIXED** — Description card removed from Face 2
- [x] **FIXED** — Music toggle button added above mute button, both fixed bottom-right
- [x] **FIXED** — Form inputs cyan 10% background
- [x] **FIXED** — Reveal My Cube moved outside glass card
- [x] **FIXED** — Vimeo player color set to cyan 7dd4fc
- [ ] Spike star CSS still in file (JS generates round stars but CSS classes remain — harmless but can clean up)
- [ ] Audio re-enable (3 lines to uncomment)

---

## STRATEGIC NOTES — WHAT NEEDS ATTENTION

These points came out of a product review. Address before full launch:

### 🔴 Critical
- **Content variations incomplete** — same text repeating on every load kills user trust. Life Path has 3 variations done. All other 8 categories still need 2 more variations each. This is the single biggest content priority.


### 🟡 Important
- **No push notifications** — zero retention mechanism once user leaves. Consider adding a "Save your reading" email capture or PWA push notification opt-in.
- **No user accounts** — no personalisation over time, users can't return to their reading. Consider lightweight account system (email + localStorage for now, Supabase later if needed).
- **Price changed to $8 USD** — going global, not SA-only. PayFast is SA only — need Stripe or Paddle for international payments.

### 🟢 Nice to Have
- **No reviews or social proof** — add a testimonial section or star rating prompt after unlock.
- **No referral or sharing mechanism** — users should be able to share their reading or refer friends.

## SEPARATE PROJECT — QNC ACADEMY
```
Path:    /Users/madcarl/Projects/qnc-academy/
Stack:   Vercel + Supabase + ElevenLabs + GitHub
URL:     qnc-academy.vercel.app
Status:  Active development — COMPLETELY SEPARATE CHAT
```
**Never bring Academy work into Quantum Cube chats and vice versa.**

---

*Paste this entire document at the start of every new Quantum Cube chat session.*
