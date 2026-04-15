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
**YouTube:** Quantum Neuro Creations Academy (quantumneurocreations@gmail.com)

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
| **YouTube Studio** | studio.youtube.com | quantumneurocreations@gmail.com | Manage videos |
| **PayFast** | payfast.co.za | TBD | Payment gateway |
| **ElevenLabs** | elevenlabs.io | ElevenCreative | Future voice |

> Note: Vercel and Supabase are Academy-only. Do NOT open them for Quantum Cube work.

---

## HOW TO WORK ON THE FILE
1. Upload `quantum-cube-v10.html` to a new chat
2. Paste this full document
3. All edits via Python string replacement — **never rewrite from scratch**
4. File is ~13MB (audio base64 embedded)
5. After edits: drop updated file into `/Users/madcarl/Projects/quantumcube` and push

---

## TECH STACK
- Single HTML file — no framework, no backend, no database
- Vanilla JavaScript — all calculations client-side
- CSS3 — 3D transforms, glassmorphism, custom animations
- Fonts: Cinzel Decorative (logo), Cinzel (labels/UI), Cormorant Garamond (body text)
- Payment: PayFast (sandbox credentials active)
- Videos: YouTube embed (unlisted)
- Audio: Base64 embedded (currently disabled)
- Hosting: GitHub Pages
- PWA: Web manifest, service worker (cache: qc-v11)

---

## APP STRUCTURE — 7 FACES
| Face | Name | Status | Videos |
|------|------|--------|--------|
| Face 0 | Entry / Sign Up Form | ✅ Complete | None |
| Face 1 | Introduction | ✅ Complete | Introduction + Numerology Explained |
| Face 2 | Results Explained | ✅ Complete | Results Explained + Astrology |
| Face 3 | Numerology Results | ✅ Complete | None |
| Face 4 | Astrology & Horoscope | ✅ Complete | None |
| Face 5 | Combined Results | ✅ Complete | None |
| Face 6 | Complete / Outro | ✅ Complete | Your Journey Complete |
| Face 7 | Settings / Launch Guide | ✅ Complete | None |

---

## YOUTUBE VIDEOS
| Face | Title | YouTube ID | Status |
|------|-------|------------|--------|
| Face 1 | Introduction | ZNzo2731VPU | ✅ New upload — verify embedding enabled |
| Face 1 | Numerology Explained | eORl2jWAvfs | ✅ Active |
| Face 2 | Results Explained | Xb6bH09Ggzs | ⚠️ Copyright flag — monitor |
| Face 2 | Astrology & Horoscope | QHdxiHTiLoY | ✅ Active |
| Face 6 | Your Journey Complete | lJp2eFZUz_U | ✅ New upload — verify embedding enabled |

> **Important:** All videos must have **Allow Embedding = ON** in YouTube Studio.
> Videos uploaded as YouTube Shorts may not embed — re-upload as regular videos if embedding fails.
> Always test from live URL, NOT from local file (local = Error 153 always).

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
- Day default: 1, Year default: 1999, max year: 2025

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
  4. Update price display in app from R88 to $8
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

### 🔴 Priority 3 — Videos
- [ ] Update Introduction video ID (ZNzo2731VPU) — confirm embedding works
- [ ] Update Complete video ID (lJp2eFZUz_U) — confirm embedding works
- [ ] Enable embedding in YouTube Studio for all 5 videos
- [ ] Re-record all videos at lower volume if needed

### 🟡 Priority 4 — Audio
- [ ] Re-enable audio (uncomment ~2 lines in JS)
- [ ] Test all 6 sounds on device
- [ ] Test music pause/resume on video play

### 🟡 Priority 5 — Payments
- [ ] Register PayFast merchant account
- [ ] Swap sandbox → live credentials
- [ ] Set sandbox: false
- [ ] Test live R88 payment

### 🟢 Priority 6 — App Stores
- [ ] Google Play: PWABuilder.com → .aab → $25 USD dev account
- [ ] Apple App Store: Capacitor → Xcode → $99/yr dev account

### 🟢 Priority 7 — Final Polish
- [ ] Final QA pass all 6 faces on device
- [ ] Update legal documents if needed
- [ ] Review lock screen content

---

## PENDING FIXES FROM LAST SESSION
- [x] **FIXED** — payOverlay CSS bug: #payOverlay styles were merged into .legal-link selector, causing "Unlock Your Complete Reading" and "R88" bars to show on Face 0. Split into separate CSS rules. (Fixed April 15, 2026)
- [ ] Spike star CSS still in file (JS generates round stars but CSS classes remain — harmless but can clean up)
- [ ] Audio re-enable (3 lines to uncomment)


---


---

## STRATEGIC NOTES — WHAT NEEDS ATTENTION

These points came out of a product review. Address before full launch:

### 🔴 Critical
- **Content variations incomplete** — same text repeating on every load kills user trust. Life Path has 3 variations done. All other 8 categories still need 2 more variations each. This is the single biggest content priority.
- **YouTube dependency is fragile** — videos can break, get copyright flagged, or fail to embed. Plan: host MP4s directly on GitHub as backup, or move to self-hosted video.

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
