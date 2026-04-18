# QUANTUM CUBE — MASTER PROJECT DOCUMENT
**Version: v11 | Last Updated: April 18, 2026**

---

## ⚠️ CRITICAL RULE — ALWAYS READ FIRST
**Quantum Cube and QNC Academy are COMPLETELY SEPARATE projects.**
- Never mix code or files between them
- Quantum Cube currently lives on GitHub Pages
- Quantum Cube has its own Supabase project (Frankfurt) — never touch the Academy one (Ireland)
- If creating new Vercel or Supabase resources, create them FOR Quantum Cube only
- Always confirm which project you are working on before making any changes

---

## ⚠️ FIRST THING EVERY SESSION — RUN THIS BEFORE TOUCHING ANYTHING:
```bash
grep -n "function runCalculation" /Users/qnc/Projects/quantumcube/quantum-cube-v10.html
```
Expected: line 2197 (or close — will drift as the file grows).
If it returns empty — restore from git before proceeding:
```bash
git show HEAD~1:quantum-cube-v10.html > /tmp/good-version.html
cp /tmp/good-version.html /Users/qnc/Projects/quantumcube/quantum-cube-v10.html
```

---

## TEAM
- **Ronnie (Willem Pretorius)** — design, programming, tech lead
- **Michelle** — admin, content review
- **Keyzer** — marketing + finance/payments
- Equal 3-way partnership
- Faceless brand philosophy: public communication only uses `admin@qncacademy.com` and `info@qncacademy.com`

---

## FILE LOCATIONS

```
/Users/qnc/Projects/quantumcube/              <- MAIN PROJECT FOLDER
|- quantum-cube-v10.html                      <- THE APP (single file, ~11.2 MiB, 2754 lines)
|- PROJECT_BRIEF.md                           <- This document
|- cube-background.jpg                        <- Milky Way background image (in repo)
|- .supabase-env                              <- Supabase credentials (gitignored)
|- .cursorignore                              <- Cursor indexing rules (committed)
|- .gitignore                                 <- Git ignore rules (committed)
|- supabase/                                  <- Supabase CLI linked project (.temp gitignored)
|- Cube Sides/                                <- Cube face images (gitignored - embedded in HTML)
|- Videos/                                    <- Video local backups (gitignored)
|- audio/                                     <- Audio files
|  |- ES_Dream_Focus_Beta_Waves.mp3
|  |- Opening_app.wav
|  |- Cube_Side_Selection.wav
|  |- rotate_cube.wav
|  |- Pop1.mp3
|  |- Pop_2.mp3
|- *.bak-*                                    <- Rewrite script backups (gitignored)
|- write_brief.py                             <- Ad-hoc script (gitignored)
|- rewrite_legal.py                           <- Legal section rewrite tool (committed)
|- rewrite_terms.py                           <- Terms rewrite tool (committed)
```

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
| Editor | Cursor (with Claude agent) + Terminal |
| GitHub CLI | gh v2.89.0 — authenticated as quantumneurocreations-dot |
| SSH Key | ED25519 ~/.ssh/id_ed25519 — "Quantum's Mac mini" |
| Node.js | v24.15.0 (LTS) via nvm, npm v11.12.1 |
| Python | 3.9.6 (system) |
| cwebp | v1.6.0 via Homebrew |
| Supabase CLI | v2.90.0 — logged in, repo linked to quantum-cube project |
| Vercel CLI | v51.5.0 — logged in as quantumneurocreations-5422 |
| .cursorignore | In place — excludes quantum-cube-v10.html from indexing |
| Cursor settings | File-deletion protection ON; external-file protection ON; allowlist for safe read-only commands |

**Terminal push command:**
```bash
cd /Users/qnc/Projects/quantumcube
git add .
git commit -m "description"
git push
```

---

## WORKFLOW RULES — CRITICAL
- **Use Mac Terminal + sed/python3** for CSS and HTML structure changes
- **JavaScript changes only** via Cursor Claude
- **Never use sed for JavaScript functions** — silently corrupts code
- **Python3 for multi-line replacements** — safer than sed for complex changes
- **Always verify runCalculation** before and after any edit
- **Cursor:** Start every chat with "Never read the full file. Use Grep to find line numbers, then Read only specific lines, then StrReplace."
- **.cursorignore** already in place, prevents indexing of large files
- **One commit per logical change** — makes `git revert` safe

---

## HOW TO WORK ON THE FILE
**IMPORTANT: Simple CSS/HTML = Mac Terminal. JavaScript = Cursor Claude only.**

If in Cursor with Claude:
1. File is at /Users/qnc/Projects/quantumcube/quantum-cube-v10.html
2. Do NOT read the full file — Grep first, then read specific lines
3. File is ~11 MiB — do NOT upload to chat
4. Use live URL for visual checks (via Browser MCP)
5. After edits: git add, commit, push

---

## TECH STACK
- **Frontend:** Single HTML file, vanilla JavaScript, CSS3 3D transforms, glassmorphism
- **Fonts:** Cinzel Decorative (logo), Cinzel (labels/UI), Cormorant Garamond (body text)
- **Auth:** Supabase magic-link (email OTP) — no passwords, SDK v2.45.4 via UMD CDN
- **Database:** Supabase Postgres in Frankfurt — `public.profiles` table with RLS
- **Payment:** PayFast sandbox currently wired (being replaced — see "PAYMENT PROCESSOR CHANGE")
- **Videos:** Vimeo — Player API active, fake fullscreen on play, portrait videos stay portrait
- **Audio:** Base64 embedded (currently disabled)
- **Hosting:** GitHub Pages
- **PWA:** Web manifest, service worker (cache: qc-v11)
- **Background:** Milky Way image (cube-background.jpg) behind CSS starfield
- **Cube faces:** Clean glass look — no face images (finalised April 16)

---

## 🔁 PAYMENT PROCESSOR CHANGE — IN PROGRESS
**Decided April 18, 2026. Full implementation Monday April 20 with team.**

- **Old:** PayFast, $8 USD, SA-only, sandbox active in code
- **New:** Paddle, $17 USD, global (Merchant of Record handles VAT/GST for us)
- **Why $17:** Paddle minimum rules out $8. 1+7=8 in numerology (wealth number) — on-brand.
- **Why Paddle:** Global reach, MoR handles international tax, allows SA-based sellers
- **Status:**
  - Team meeting Monday April 20 for Paddle account setup (Ronnie + Michelle + Keyzer)
  - Account application, domain verification, bank + tax details required
  - All PayFast code still in place until Paddle is live — do not rip out early
  - Webhook Edge Function is a Monday+ task

---

## APP STRUCTURE — 7 FACES
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

## VIMEO VIDEOS
All videos on Vimeo. Privacy: Hide from Vimeo. Downloads OFF. Comments OFF.

| Face | Title | Vimeo ID | Shape |
|------|-------|----------|-------|
| Face 1 | 1 - Introduction | 1183086210 | Portrait (9:16) |
| Face 2 | 2 - Numerology Explained | 1183086853 | Landscape (16:9) |
| Face 2 | 3 - Results Explanation | 1183087269 | Landscape (16:9) |
| Face 2 | 4 - Astrology | 1183087951 | Landscape (16:9) |
| Face 6 | 5 - Cube Outro | 1183103519 | Portrait (9:16) |

Video behaviour: fake fullscreen via CSS on play. Portrait videos stay portrait. Landscape videos allow phone rotation via Screen Orientation API unlock on play, relock to portrait on pause/end.

**Known warning:** Line 559 has an iframe with both `allow="... fullscreen ..."` and `allowfullscreen` attributes. Chrome logs "Allow attribute will take precedence over 'allowfullscreen'" — cosmetic, not a bug. Fix planned for weekend.

---

## VISUAL DESIGN — KEY DECISIONS (DO NOT CHANGE)
- Background: Milky Way image (cube-background.jpg) + CSS starfield on top
- Starfield: 220 stars, round glowing dots
- Cube: Glass effect, cyan-white glowing edges 2px — clean glass faces (no face images)
- Logo: QUANTUM top, CUBE right-aligned, CUBE in cyan with glow + float animation
- All cards: glass style, margin 0 16px 20px 32px (breathing room left/right)
- Lock screens: same margins as sign-up card
- Scoreboard, matrix, card-stack, astro-grid, combo-full: all have matching side margins
- Video-face: margin 0 16px 16px 32px on Face 2 landscape videos
- Lock screen: "Complete Quantum Cube Unlock", & between Chinese Horoscope and Combined Interpretation, price to update from $8 → $17 on Paddle switch
- Unlock button: narrow width (auto/160px min), centered, 2px white border, 60% width matching divider, cyan glow on hover/active
- Three fixed buttons bottom-right: narrator (top), music (middle), mute (bottom)
- Combined portrait: no drop cap, starts "You are someone..."
- Face 6 outro: only "Your Journey Complete" heading + video
- Legal footer: Terms of Use + Disclaimer outside lock cards, hidden on unlock via .lock-footer class, restored on reset
- "Period Cycles" renamed to "Life Phases" everywhere
- Month dropdown: numbers 1-12
- PWA orientation: portrait locked, unlocks during landscape video play

---

## CUBE BEHAVIOUR
- Hidden on Face 0, visible on all other faces
- Idle auto-rotation after 1 second (clockwise from top)
- Drag rotates cube, no snap-back on release
- Cube faces: clean glass look — no face images
- Face mapping: Front=Face1, Right=Face2, Back=Face3, Left=Face4, Top=Face5, Bottom=Face6

---

## SUPABASE BACKEND
**Project:** quantum-cube (ref `fqqdldvnxupzxvvbyvjm`)
**Region:** Central EU (Frankfurt) — POPIA/GDPR aligned
**Organisation:** Quantum Neuro Creations (`ybhwpcakkaveapdztnrs`)
**Credentials:** `/Users/qnc/Projects/quantumcube/.supabase-env` (gitignored)

### Schema — `public.profiles`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK, references `auth.users.id` |
| email | text | |
| has_paid | boolean | Immutable from client — only service role can flip |
| marketing_consent | boolean | Set at signup from user metadata |
| created_at | timestamptz | |

### RLS Policies (VERIFIED April 18)
- **RLS enabled** on `public.profiles`
- `users_select_own_profile` — SELECT where `auth.uid() = id`
- `users_insert_own_profile` — INSERT with `auth.uid() = id` (backup for the trigger)
- `users_update_own_profile` — UPDATE where `auth.uid() = id` AND `has_paid` locked to existing value (users cannot self-grant paid status)
- No DELETE policy — profile deletion requires service-role Edge Function

### Trigger
- `on_auth_user_created` — AFTER INSERT on `auth.users` → calls `public.handle_new_user()` (SECURITY DEFINER) → inserts row into `public.profiles` with `id`, `email`, `marketing_consent` from user_metadata

### Auth Configuration
- Site URL: `https://quantumneurocreations-dot.github.io/quantumcube/quantum-cube-v10.html`
- Redirect URLs: GitHub Pages URL, `https://quantumcube.app/quantum-cube-v10.html`
- Magic-link / OTP auth only (no passwords)
- Session: free-tier default (persists until explicit sign-out)
- Single-session-per-user: OFF (user can sign in from multiple devices)

### Edge Functions
None deployed. Paddle webhook Edge Function is the Monday+ work.

---

## FRONTEND WIRING — CURRENT STATE (April 18, 2026)

All Supabase frontend wiring is shipped across 8 chunks (commits `90ff35c` through `32c59ae`):

- ✅ Chunk 1: Supabase SDK loaded (line 443) + client init (`const sb`, line 447)
- ✅ Chunk 2: Email field + marketing consent checkbox on Face 0
- ✅ Chunk 2b: Cyan-glow custom styling for consent checkbox
- ✅ Chunk 3: Magic-link signup wired (`signInWithOtp` line 2130), session restore on page load (`onAuthStateChange` line 2181)
- ✅ Chunk 4: `has_paid` is source of truth (line 1880), `STORE_KEY` ("qc_unlocked_v1") as cache only
- ✅ Chunk 5: Banner countdown + mirrored marketing consent across lock cards
- ✅ Chunk 6: Two-stage banner flow replaces countdown
- ✅ Chunk 7: Inline message slot replaces banner card, 3s SENDING + 3s EMAIL SENT
- ✅ Chunk 8: Choreography starts immediately, dead banner calls removed, center fix

### Key line references (current, April 18)
| What | Line |
|---|---|
| Supabase UMD script tag | 443 |
| SUPABASE_URL const | 445 |
| SUPABASE_ANON_KEY const | 446 |
| `const sb` createClient | 447 |
| `detectSessionInUrl: true` | 451 |
| Face 0 div open | 520 |
| Email input | 528 |
| Marketing consent checkbox | 535–538 |
| "Reveal My Cube" button | 540 |
| STORE_KEY const | 1865 |
| `has_paid` check | 1880 |
| PayFast notify URL placeholder | 1956 |
| `runCalculation` function | 2197 |
| `signInWithOtp` call | 2130 |
| `sb.from("profiles")` calls | 2173, 2184 |
| `onAuthStateChange` listener | 2181 |
| Face 0 signup button label | "Reveal My Cube" (not "Send magic link" — on-brand) |

---

## WHAT STILL NEEDS TO BE DONE

### 🚀 LAUNCH-BLOCKING — Monday / Tuesday with team
- [ ] Paddle account application (Ronnie + Michelle + Keyzer, Monday)
- [ ] Paddle webhook Edge Function (`supabase/functions/paddle-webhook/`)
- [ ] Swap PayFast code → Paddle checkout in HTML
- [ ] Update price $8 → $17 (line 2590 legal, 2728 pay-price-big, 2735 pay button)
- [ ] Replace placeholder `https://YOUR-SERVER.com/payfast-notify` (line 1956) with real Paddle webhook URL
- [ ] Remove "Try Demo (test mode)" buttons (lines 645, 686, 725, 762, 2740)
- [ ] Remove `unlockDemo()` function (line 2035)
- [ ] End-to-end test: signup → magic link → Paddle payment → has_paid flips → unlock persists across devices
- [ ] Update legal docs: replace all PayFast references with Paddle (Privacy line ~2338, Terms ~2375, IP ~2428, POPIA section)
- [ ] Age gate on signup (DOB ≥ 18) — Privacy Policy promises 18+, currently unenforced

### ⚙️ Weekend housekeeping (April 18–19)
- [ ] Sign-out flow — `sb.auth.signOut()` button somewhere in Settings (Face 7)
- [ ] Age gate on signup (above — could ship this weekend, no payment dep)
- [ ] Fix line 559 iframe `allow`/`allowfullscreen` warning (applies to all 5 video iframes)
- [ ] Fix truncated `<but` at end of file + add missing `</body></html>` (historical — present since first commit)
- [ ] Paddle prep document for Monday team meeting
- [ ] Expose `window.sb` for DevTools debugging (`window.sb = sb;` one-liner)

### 📝 After-launch follow-ups
- [ ] Narrator button → ElevenLabs API (male/female voice toggle, API key reuse from Academy)
- [ ] Re-enable audio (uncomment ~2 lines in JS), test all 6 sounds on device, test music pause/resume on video play
- [ ] Marketing email pipeline + unsubscribe endpoint (Privacy Policy promises this — must exist before first campaign)
- [ ] App stores — Google Play (PWABuilder.com → .aab → $25 dev account); Apple (Capacitor → Xcode → $99/yr)
- [ ] Social proof / testimonials section
- [ ] Sharing mechanism for readings
- [ ] Analytics — track usage
- [ ] Profile deletion Edge Function (privacy policy promises 30-day deletion on request)
- [ ] Gmail aliases propagation check (info, privacy, keyzer, michelle, ronnie @ qncacademy.com)
- [ ] 2FA on all 3 partner Workspace accounts
- [ ] DMARC tightening from p=none → p=quarantine after 1-2 weeks clean reports
- [ ] Duplicate `.DS_Store` line in .gitignore (line 6 and lines 17–18 — cosmetic)

### 📦 Content complete (no action needed)
- [x] PRIORITY 1 — Content Variations (all 9 categories, 3 variations each)
- [x] PRIORITY 2 — Content Accuracy Review (numerology + Western + Chinese zodiac all verified)

---

## INFRASTRUCTURE LIVE (end of April 17)

| System | State |
|---|---|
| GitHub Pages | Live, serving commit 32c59ae (last HTML deploy) |
| quantumcube.app domain | Registered at Cloudflare, DNS managed, not yet pointed at Pages |
| qncacademy.com domain | Registered at Cloudflare, DNS managed, MX + SPF + DKIM + DMARC all live |
| Google Workspace | admin@qncacademy.com active, 5 aliases created |
| Gmail inbox filters | 5 rules auto-label incoming mail by recipient alias |
| Cloudflare Email Routing | *@quantumcube.app → admin@qncacademy.com (active) |
| Email auth qncacademy.com | SPF (soft fail) + DKIM + DMARC (p=none) all live |
| Supabase project | quantum-cube in Frankfurt, ACTIVE_HEALTHY, free tier |
| Supabase schema | profiles table with RLS + auto-create trigger (all verified) |
| Supabase auth config | Site URL + 2 redirect URLs set, magic-link ready |
| Legal docs | Privacy + POPIA + Security + Terms all align with Supabase account model |
| Legal docs pending | All PayFast references need PayFast → Paddle swap |

---

## ANNUAL RUNNING COST SUMMARY
- 1× Google Workspace seat: ~R1,340/year
- qncacademy.com renewal: ~R200/year
- quantumcube.app renewal: ~R275/year
- **TOTAL: ~R1,815/year (~R150/month)**

Excludes: Paddle transaction fees (~5% + 50c per transaction, global), Supabase paid tier if free limits exceeded, ElevenLabs narrator API usage.

---

## SEPARATE PROJECT — QNC ACADEMY
| Detail | Value |
|---|---|
| Path | /Users/qnc/Projects/qnc-academy/ |
| Stack | Next.js + Vercel + Supabase + ElevenLabs + GitHub |
| URL | qnc-academy.vercel.app |
| Supabase | SEPARATE project in West EU (Ireland) — ref `bevaepokvavzmykjmhda` |
| Status | Active development — COMPLETELY SEPARATE CHAT |

**Never bring Academy work into Quantum Cube chats and vice versa.**

---

## SESSION LOG — April 18, 2026 — Saturday morning audit + housekeeping

### Discovery & re-orientation
- [x] Ran full connectivity audit (git, GitHub, SSH, Supabase CLI, Vercel CLI, Node, npm, Python, cwebp, browser MCP, Pages deploy status) — all green
- [x] Supabase CLI logged in + repo linked to quantum-cube project
- [x] Verified RLS policies on profiles table — all 4 policies correct, has_paid is truly immutable from client
- [x] Verified `on_auth_user_created` trigger exists and calls `handle_new_user()` (SECURITY DEFINER)
- [x] Repo hygiene: .DS_Store untracked, .cursorignore committed, *.bak-* + supabase/.temp/ + write_brief.py gitignored — commit 71f3a1a
- [x] Full audit of HTML confirms Chunks 1–8 of Supabase wiring all shipped (previous session undocumented in brief)
- [x] Discovered file tail truncated at `<but` fragment — historical (176 commits back, present in first commit). Harmless. Scheduled for weekend fix.

### Decisions locked in
- Payment processor: PayFast → Paddle (Monday team meeting to set up account)
- Price: $8 → $17 USD (Paddle minimum + numerology 1+7=8)
- Brief to reflect reality going forward — this document replaces v10

### Weekend plan (April 18–19, no Paddle dependency)
1. Update PROJECT_BRIEF.md (this commit)
2. Sign-out flow
3. Age gate on signup
4. Fix iframe allow/allowfullscreen console warning
5. Fix truncated `<but` + add proper `</body></html>`
6. Paddle prep doc for Monday team meeting

### Monday+
- Paddle account setup
- Webhook Edge Function
- Full PayFast → Paddle code swap
- Remove Try Demo buttons
- Launch readiness QA

---

## NEXT SESSION STARTING POINT
- Check runCalculation still at ~line 2197
- Continue weekend housekeeping items from the list above
- Review any new items in "AFTER-LAUNCH FOLLOW-UPS"
- On Monday: Paddle team meeting, then webhook Edge Function work
