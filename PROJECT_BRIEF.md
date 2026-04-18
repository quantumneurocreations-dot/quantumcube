# QUANTUM CUBE — MASTER PROJECT DOCUMENT
**Version: v13 | Last Updated: April 18, 2026 (end of day)**

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

```
/Users/qnc/Projects/quantumcube/              <- MAIN PROJECT FOLDER
|- quantum-cube-v10.html                      <- THE APP (~11 MiB, ~2823 lines)
|- PROJECT_BRIEF.md                           <- This document
|- CHAT_KICKOFF.md                            <- Chat operating protocol
|- cube-background.jpg                        <- Milky Way background (in repo)
|- .supabase-env                              <- Supabase + Resend creds (gitignored)
|- .cursorignore                              <- Cursor indexing rules (committed)
|- .gitignore                                 <- Git ignore rules (committed)
|- supabase/                                  <- Supabase CLI linked project (.temp gitignored)
|- Cube Sides/                                <- Cube face images (gitignored - embedded in HTML)
|- Videos/                                    <- Video local backups (gitignored)
|- audio/                                     <- Audio files
|- screenshots/                               <- Audit screenshots (gitignored)
|- *.bak-*                                    <- Rewrite script backups (gitignored)
|- wire_supabase_*.py, rewrite_*.py           <- Historical edit scripts (committed, no longer used)
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
- **Videos:** Vimeo Player API
- **Audio:** Base64 embedded (currently disabled)
- **Hosting:** GitHub Pages
- **PWA:** Web manifest, service worker (cache: qc-v11)

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
| faceCheckEmail | Interstitial — "Check Your Email" (NEW Chunk 5b) | Shown after Reveal My Cube submit; has Resend button (60s cooldown) + Back to Sign Up |
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

Video behaviour: fake fullscreen via CSS on play. Portrait videos stay portrait. Landscape videos rotate via Screen Orientation API.

---

## VISUAL DESIGN — KEY DECISIONS (DO NOT CHANGE)
- Background: Milky Way image + CSS starfield (220 stars)
- Cube: Glass effect, cyan-white glowing edges 2px, clean glass faces (no images)
- Logo: QUANTUM top, CUBE right-aligned inline-block, CUBE cyan with glow + float
- All cards: glass style, margin 0 16px 20px 32px
- Lock screens: "Complete Quantum Cube Unlock" title, stacked bullets (9 Numerology / 5 Western Astrology / 5 Chinese Horoscope / & / Combined Interpretation), $17.00, cyan-glow UNLOCK button
- Payment overlay: matched `#globalLogo` at top, two-line title, same bullets as lock card, $17 + stacked meta (One-Time Fee / No Subscription / Yours Forever), permanent cyan-glow Pay $17 button
- Three fixed buttons bottom-right: narrator / music / mute
- Legal footer on Face 0: Terms + Disclaimer + Settings (Settings signed-in only)
- Month dropdown: numbers 1-12
- PWA orientation: portrait locked, unlocks during landscape video play

---

## SUPABASE BACKEND
- **Project:** quantum-cube (ref `fqqdldvnxupzxvvbyvjm`)
- **Region:** Central EU (Frankfurt) — POPIA/GDPR aligned
- **Org:** Quantum Neuro Creations (`ybhwpcakkaveapdztnrs`)
- **Credentials:** `.supabase-env` (gitignored) — contains SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_PROJECT_ID, RESEND_API_KEY

### Schema — `public.profiles`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK, references `auth.users.id` |
| email | text | |
| has_paid | boolean | Immutable from client — only service role can flip |
| marketing_consent | boolean | From user_metadata at signup |
| created_at | timestamptz | |

### RLS Policies (VERIFIED April 18)
- RLS enabled
- `users_select_own_profile` — SELECT where `auth.uid() = id`
- `users_insert_own_profile` — INSERT backup (trigger does the real work)
- `users_update_own_profile` — UPDATE with `has_paid` locked to existing value
- No DELETE policy — profile deletion requires service-role Edge Function

### Trigger
- `on_auth_user_created` → `handle_new_user()` (SECURITY DEFINER) → inserts profile with email + marketing_consent from user_metadata

### Auth Config
- Site URL: GitHub Pages URL
- Redirect URLs: GitHub Pages + quantumcube.app
- Magic-link only, session persists until explicit sign-out
- Custom SMTP via Resend (see EMAIL INFRASTRUCTURE)

### Edge Functions
None deployed. Paddle webhook is Monday's work.

### Test data in profiles (delete before launch)
- `quantumneurocreations@gmail.com` (Ronnie's primary test, has_paid toggleable)
- `rkelbrickmail@gmail.com`
- `carlkelbrick@gmail.com`
- Any `test+*@qncacademy.com` from Chunk 5b testing

---

## FRONTEND WIRING — SHIPPED

All Supabase magic-link wiring done. All payment UI done to $17. Sign-out works. Face 7 reachable. Interstitial works.

### Key line refs (April 18 end-of-day — use grep, numbers drift)
| What | Approx line |
|---|---|
| Supabase UMD script tag | ~443 |
| SUPABASE_URL / ANON_KEY / client | ~445–447 |
| Loading screen (#loadingScreen) | 455 |
| Face 0 div open | ~520 |
| Email input on Face 0 | ~528 |
| Marketing consent on Face 0 | ~535 |
| Reveal My Cube button | ~540 |
| faceCheckEmail interstitial | ~545 |
| Resend Email button | ~552 |
| Settings link (#settingsLink) | ~545 (in Face 0 legal footer — different area) |
| Face 7 Sign Out button | ~800 |
| STORE_KEY const | ~1865 |
| has_paid check | ~1880 |
| launchPayFast notify placeholder | ~1956 |
| `function runCalculation` | **~2257** |
| signInWithOtp | ~2130 + handleResendMagicLink |
| onAuthStateChange | ~2181 |
| signOut | ~2201 |
| #payOverlay | ~2779 |

**Use grep before editing — these drift.**

---

## WHAT STILL NEEDS TO BE DONE

### 🚀 Monday / Tuesday (launch-blocking, needs team)
- [ ] Paddle account application
- [ ] Paddle webhook Edge Function
- [ ] Rewrite `launchPayFast()` body → call Paddle checkout
- [ ] Replace placeholder notify URL (~1956)
- [ ] Remove `PF_CONFIG.amount = "88.00"` or repurpose
- [ ] Update legal docs: remove all PayFast refs, add Paddle + Resend
- [ ] E2E test: signup → magic link → Paddle payment → has_paid flips → unlock persists
- [ ] Delete test rows from profiles table

### ⚙️ Sunday (remaining weekend work)
- [ ] User re-test of signup → interstitial → magic link flow with fresh emails (Ronnie's own visual QA)
- [ ] "Back to Sign Up" button — render as two lines ("Back to" / "Sign Up")
- [ ] Age gate on signup (DOB ≥ 18)
- [ ] Paddle prep doc for Monday team meeting (business entity, bank, tax ID, product URL, checkout flow)

### 📝 After-launch follow-ups
- [ ] Narrator button → ElevenLabs (reuse Academy API key)
- [ ] Re-enable audio, test 6 sounds, test music pause/resume on video play
- [ ] Marketing email pipeline + unsubscribe endpoint (Privacy Policy promises this)
- [ ] Brand the Supabase magic-link email (currently plain default)
- [ ] Fix Resend return-path: `@send.quantumcube.app` → display `@quantumcube.app`
- [ ] App stores — Google Play (PWABuilder → .aab → $25); Apple (Capacitor → Xcode → $99/yr)
- [ ] Social proof / testimonials section
- [ ] Sharing mechanism for readings
- [ ] Analytics
- [ ] Profile deletion Edge Function
- [ ] Dead CSS cleanup: `.pay-btn`, `.pay-btn-alt`, `.pay-price-lines span`, `.demo-btn`
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
| GitHub Pages | Live, serving latest HTML commit |
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

## SESSION LOG — April 18, 2026 — Saturday (12 commits)

| # | Commit | Summary |
|---|---|---|
| 1 | 71f3a1a | Repo hygiene — gitignore .DS_Store, supabase/.temp, backup files |
| 2 | c0b420d | Brief v11 sync |
| 3 | 773d85a | Sign-out flow + Face 7 Settings |
| 4 | 316f6a3 | Face 7 reachable (Settings link + Back button) |
| 5 | 4871fa7 | Payment overlay cleanup + demo removal + file truncation fix |
| 6 | cb1c3b2 | Payment overlay polish (2-line title, stacked price, cyan button) |
| 7 | 7ecfae6 | Pay button permanent cyan glow |
| 8 | 1a921e4 | Brief v12 (session-startup protocol + Resend infrastructure) |
| 9 | 1f0e82e | Repo hygiene — move audit screenshots to gitignored folder |
| 10 | 4be0431 | Chunk 5a — Face 0 form cleanup + lock-card label shortening |
| 11 | e78cadf | Chunk 5b — interstitial check-email face + resend button 60s cooldown + fix page-load re-send loop |
| 12 | f94fe4d | Loading logo — CUBE left-shift to match Face 0 structure |

### Infrastructure milestones today
- Supabase CLI authenticated + repo linked
- RLS policies verified
- Resend account + domain + DNS + API key + Supabase SMTP all live
- File truncation (historical) fixed
- Demo mode fully removed
- Brief refactored twice (v11 → v12 → v13) as understanding of actual state improved

### Lessons learned (added to CHAT_KICKOFF.md)
- Python scripts on HTML are an anti-pattern — str_replace or shell sed only
- New chats need both PROJECT_BRIEF.md AND CHAT_KICKOFF.md to behave consistently
- Long audits at chat-start waste time; a 4-line health check is enough

---

## NEXT SESSION STARTING POINT
1. Attach PROJECT_BRIEF.md + CHAT_KICKOFF.md to new chat's first message
2. Run minimal health check (see kickoff doc)
3. Sunday work: user re-test with fresh emails, Back to Sign Up two-line fix, age gate, Paddle prep doc
4. Monday: Paddle team meeting, then webhook Edge Function
