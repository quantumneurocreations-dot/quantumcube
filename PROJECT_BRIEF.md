# QUANTUM CUBE — MASTER PROJECT DOCUMENT
**Version: v12 | Last Updated: April 18, 2026 (Saturday afternoon)**

---

## ⚠️ CRITICAL RULE — ALWAYS READ FIRST
**Quantum Cube and QNC Academy are COMPLETELY SEPARATE projects.**
- Never mix code or files between them
- Quantum Cube currently lives on GitHub Pages
- Quantum Cube has its own Supabase project (Frankfurt) — never touch the Academy one (Ireland)
- If creating new Vercel or Supabase resources, create them FOR Quantum Cube only
- Always confirm which project you are working on before making any changes

---

## 🚦 SESSION STARTUP — ALWAYS RUN FIRST

**At the start of every new chat, paste this block into Cursor Claude. Cursor Claude runs the full health check and reports status. Chat Claude reads status, flags anything needing attention, and only then starts real work.**

```
Session startup health check. Read-only. No edits, no commits.

cd /Users/qnc/Projects/quantumcube

echo "=== A. Working tree state ==="
grep -n "function runCalculation" quantum-cube-v10.html
wc -l quantum-cube-v10.html
git status
git log --oneline -5

echo ""
echo "=== B. Supabase CLI ==="
supabase --version
supabase projects list 2>&1 | head -5

echo ""
echo "=== C. Resend DNS records (all 4 must resolve) ==="
dig +short TXT resend._domainkey.quantumcube.app | head -1
dig +short MX send.quantumcube.app
dig +short TXT send.quantumcube.app
dig +short TXT _dmarc.quantumcube.app

echo ""
echo "=== D. Supabase env file ==="
grep -c "=" /Users/qnc/Projects/quantumcube/.supabase-env
grep -o "^[A-Z_]*" /Users/qnc/Projects/quantumcube/.supabase-env | sort

echo ""
echo "=== E. Supabase profiles table state ==="
echo "Query via Supabase SQL Editor if Browser MCP available:"
echo "SELECT email, has_paid, marketing_consent, created_at FROM profiles ORDER BY created_at DESC;"

echo ""
echo "=== F. Key line refs (sanity check) ==="
grep -n "supabase-js" quantum-cube-v10.html | head -1
grep -n "signInWithOtp" quantum-cube-v10.html
grep -n "launchPayFast" quantum-cube-v10.html
grep -c "</body>" quantum-cube-v10.html
grep -c "</html>" quantum-cube-v10.html

Report all output verbatim. Do NOT proceed to any other work until status is reviewed.
```

**Expected clean state:**
- runCalculation present (line number will drift — ballpark 2200)
- Working tree clean, branch main, up to date with origin
- Supabase CLI logged in, `quantum-cube` project linked (● marker)
- All 4 DNS records return non-empty values
- `.supabase-env` has 4 variables: SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_PROJECT_ID, RESEND_API_KEY
- `</body>` and `</html>` each count 1 (file closes properly)
- launchPayFast appears 2x (button onclick + function definition)

**If anything is off:** Chat Claude will flag which item failed and give you the specific fix block before starting real work.

---

## TEAM
- **Ronnie (Willem Pretorius)** — creator, design, programming, tech lead
- **Michelle** — admin, content review, QA
- **Keyzer** — marketing, finance, payments
- Equal 3-way partnership
- Faceless brand philosophy: public communication only uses `admin@qncacademy.com` and `info@qncacademy.com`

---

## FILE LOCATIONS

```
/Users/qnc/Projects/quantumcube/              <- MAIN PROJECT FOLDER
|- quantum-cube-v10.html                      <- THE APP (single file, ~11 MiB, ~2750 lines)
|- PROJECT_BRIEF.md                           <- This document
|- cube-background.jpg                        <- Milky Way background image (in repo)
|- .supabase-env                              <- Supabase + Resend credentials (gitignored)
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
| Supabase CLI | v2.90.0 — logged in, repo linked to quantum-cube |
| Vercel CLI | v51.5.0 — logged in as quantumneurocreations-5422 |
| Cursor settings | File-Deletion Protection ON; External-File Protection ON; command allowlist includes read-only tools (grep, git status, ls, cat, wc, tail, head, supabase, gh, dig, python3); Auto-Run in Sandbox |

**Terminal push command:**
```bash
cd /Users/qnc/Projects/quantumcube
git add .
git commit -m "description"
git push
```

---

## WORKFLOW RULES

### Two-agent split
- **Chat Claude** (claude.ai, this doc) — strategy, code review, proposal-writing, briefing
- **Cursor Claude** (IDE agent) — drives Terminal + Browser MCP + file edits on your Mac
- Chat Claude gives you paste blocks. You paste to Cursor Claude. Cursor Claude runs. You paste output back. Repeat.

### Editing rules (apply to both agents)
- **Always verify `runCalculation` exists** before and after any HTML edit
- **One commit per logical change** — makes `git revert` safe
- **Prefer grep + line ranges** over reading full file (file is ~11 MiB)
- **Python3 for multi-line replacements** — safer than sed for complex changes
- **Never use sed for JavaScript functions** — silently corrupts code
- **StrReplace for targeted HTML edits** — exact anchor match required
- **`.cursorignore`** already in place; it excludes quantum-cube-v10.html from Cursor's search indexer (improves agent speed). Cursor Claude can still read/edit the file via explicit path — the ignore only affects the indexer.

### Rate limits and retries
- DNS propagation: one extra `dig` is plenty. Do NOT use "wait 60s and retry 3 times" loops — wastes time.
- Supabase auth rate limits: project has custom SMTP via Resend now — no email rate limit concerns.

---

## TECH STACK
- **Frontend:** Single HTML file, vanilla JavaScript, CSS3 3D transforms, glassmorphism
- **Fonts:** Cinzel Decorative (logo), Cinzel (labels/UI), Cormorant Garamond (body text)
- **Auth:** Supabase magic-link (email OTP) — no passwords, SDK v2.45.4 via UMD CDN
- **Database:** Supabase Postgres in Frankfurt — `public.profiles` table with RLS
- **Email sending:** Resend via custom SMTP on Supabase (unlimited — replaces the 2/hour free-tier Supabase default)
- **Payment:** PayFast sandbox currently wired (being replaced Monday — see "PAYMENT PROCESSOR CHANGE")
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
  - All visible UI prices updated to $17 (payment overlay + 4 lock cards + legal copy)
  - `launchPayFast()` function still wired under the hood — Monday's work renames/rewrites this function to call Paddle instead
  - Webhook Edge Function is a Monday+ task

---

## 📧 EMAIL INFRASTRUCTURE (NEW — April 18)

**Custom SMTP via Resend replaces Supabase's 2/hour free-tier limit.**

### Resend
- Account: `admin@qncacademy.com` (login via Google SSO)
- Domain: `quantumcube.app` — **verified**
- API key: `quantum-cube-supabase-smtp` (sending access only, domain-restricted)
- API key stored in `/Users/qnc/Projects/quantumcube/.supabase-env` as `RESEND_API_KEY` (gitignored)
- Region: eu-west-1 (Ireland — closest Resend offers to our Frankfurt Supabase)
- Free tier: 3000 emails/month, 100/day — ample for launch

### DNS records on quantumcube.app (Cloudflare)
| Type | Name | Content (abbreviated) | Purpose |
|---|---|---|---|
| TXT | `resend._domainkey` | `p=MIGfMA...QIDAQAB` | DKIM signing |
| MX | `send` | `feedback-smtp.eu-west-1.amazonses.com` (priority 10) | Bounce handling |
| TXT | `send` | `v=spf1 include:amazonses.com ~all` | SPF for send subdomain |
| TXT | `_dmarc` | `v=DMARC1; p=none;` | DMARC monitoring |

These coexist with existing Cloudflare Email Routing records at root `@` — no conflicts.

### Supabase SMTP config
- Enable Custom SMTP: ON
- Sender email: `noreply@quantumcube.app`
- Sender name: `Quantum Cube`
- Host: `smtp.resend.com`, Port: 465
- Username: `resend`
- Password: `RESEND_API_KEY` value
- Minimum interval between emails: 60 seconds (per-user rate limit)

### Known cosmetic issue
Magic-link emails technically route via `@send.quantumcube.app` subdomain (how Resend is set up). Some email clients may display this raw subdomain. Fix post-launch: configure Resend custom return-path to display as `@quantumcube.app`.

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
| Face 7 | Settings (Sign Out + Back) | Complete | None |

**Face 7 navigation:** Signed-in users see a "Settings" link in Face 0's legal footer (hidden for signed-out users). Face 7 has a Sign Out button + Back button to return to Face 0.

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

**Known warning:** Line ~559 has an iframe with both `allow="... fullscreen ..."` and `allowfullscreen` attributes. Chrome logs "Allow attribute will take precedence over 'allowfullscreen'" — cosmetic only. Fix deferred to cleanup pass.

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
- Lock screen: "Complete Quantum Cube Unlock" title, stacked bullets (9 Numerology / 5 Western Astrology / 5 Chinese Horoscope / & / Combined Interpretation), "$17.00", cyan-glow UNLOCK button
- Payment overlay: matched `#globalLogo` at top, "Complete Quantum / Cube Unlock" title (two lines), same bullets as lock card, `$17` + stacked meta (One-Time Fee / No Subscription / Yours Forever), permanent cyan-glow "Pay $17" button
- Three fixed buttons bottom-right: narrator (top), music (middle), mute (bottom)
- Combined portrait: no drop cap, starts "You are someone..."
- Face 6 outro: only "Your Journey Complete" heading + video
- Legal footer on Face 0: Terms of Use + Disclaimer + Settings (Settings shown only when signed in)
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
- Face 7 (Settings) is not mapped to a cube side — reached via Settings link on Face 0 legal footer

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
- RLS enabled on `public.profiles`
- `users_select_own_profile` — SELECT where `auth.uid() = id`
- `users_insert_own_profile` — INSERT with `auth.uid() = id` (backup for trigger)
- `users_update_own_profile` — UPDATE where `auth.uid() = id` AND `has_paid` locked to existing value
- No DELETE policy — profile deletion requires service-role Edge Function

### Trigger
- `on_auth_user_created` — AFTER INSERT on `auth.users` → calls `public.handle_new_user()` (SECURITY DEFINER) → inserts profile row with `id`, `email`, `marketing_consent` from user_metadata

### Auth Configuration
- Site URL: `https://quantumneurocreations-dot.github.io/quantumcube/quantum-cube-v10.html`
- Redirect URLs: GitHub Pages URL, `https://quantumcube.app/quantum-cube-v10.html`
- Magic-link / OTP auth only (no passwords)
- Session persists until explicit sign-out
- Custom SMTP via Resend — see "EMAIL INFRASTRUCTURE" section above

### Edge Functions
None deployed. Paddle webhook Edge Function is the Monday+ work.

### Test data in profiles table (April 18)
Three test rows from today's testing — all need deleting before launch:
- `quantumneurocreations@gmail.com` (Ronnie's primary test account)
- `rkelbrickmail@gmail.com`
- `carlkelbrick@gmail.com`

---

## FRONTEND WIRING — CURRENT STATE (April 18 afternoon)

All Supabase magic-link wiring shipped across 8 chunks (commits `90ff35c` through `32c59ae` — April 17).

Today's work (April 18) added:
- Sign-out flow + Face 7 Settings page
- Face 7 reachable via Settings link on Face 0
- Payment overlay complete redesign ($17, matched branding, cyan button)
- File truncation fix (proper `</body></html>`)
- Demo mode fully removed

### Key line references (April 18 afternoon — will drift with edits)
| What | Line (approx) |
|---|---|
| Supabase UMD script tag | ~443 |
| SUPABASE_URL const | ~445 |
| SUPABASE_ANON_KEY const | ~446 |
| `const sb` createClient | ~447 |
| Face 0 div open | ~520 |
| Email input | ~528 |
| Marketing consent checkbox (Face 0) | ~535 |
| "Reveal My Cube" button | ~540 |
| Settings link (#settingsLink) | ~545 |
| Face 7 Sign Out button | ~800 |
| STORE_KEY const | ~1865 |
| `has_paid` check | ~1880 |
| launchPayFast notify placeholder | ~1956 |
| `function runCalculation` | **~2201** |
| `signInWithOtp` call | ~2130 |
| `onAuthStateChange` | ~2181 |
| `signOut` function | ~2201 |
| `updateSettingsLinkVisibility` | ~2206 |
| `#payOverlay` block | ~2723–2750 |

**Use grep to find current positions — line numbers drift.**

---

## WHAT STILL NEEDS TO BE DONE

### 🚀 LAUNCH-BLOCKING — Monday / Tuesday with team
- [ ] Paddle account application (Ronnie + Michelle + Keyzer, Monday)
- [ ] Paddle webhook Edge Function (`supabase/functions/paddle-webhook/`)
- [ ] Rewrite `launchPayFast()` function body → call Paddle checkout
- [ ] Replace placeholder notify URL (~line 1956) with Paddle webhook URL
- [ ] Update `PF_CONFIG.amount = "88.00"` (ZAR) → remove/repurpose for Paddle
- [ ] Update legal docs: replace all PayFast references with Paddle (Privacy, Terms, IP, POPIA sections)
- [ ] End-to-end test: signup → magic link → Paddle payment → has_paid flips → unlock persists across devices
- [ ] Delete 3 test rows from profiles table before launch

### ⚙️ Weekend remaining (April 18–19)
- [ ] **Chunk 5** — Face 0 form cleanup:
  - Simplify details block (remove extra text, keep "Please complete all fields" error only)
  - Block entry on errors (can't proceed until all fields valid)
  - Remove inline banner messaging from Chunks 5–8 (if redundant with interstitial)
  - New interstitial screen between Reveal My Cube and Face 1
  - Interstitial: "Check your email, click the link" — persistent (no timer)
  - Auto-advance to Face 1 only when magic link clicked + user actually signs in
  - Resend button on interstitial with 60s cooldown
  - Marketing checkbox label: lock cards = "Email me updates" (short), Face 0 = keep full "Email me updates about Quantum Cube"
- [ ] Loading page logo — shift "CUBE" further left to match main app logo alignment
- [ ] "Back to Sign Up" button — two lines ("Back to" on top, "Sign Up" below)
- [ ] Age gate on signup (DOB ≥ 18) — Privacy Policy promises 18+, currently unenforced
- [ ] Paddle prep document for Monday team meeting (Paddle application checklist — business entity, bank, tax ID, product URL, sample checkout flow)

### 📝 After-launch follow-ups
- [ ] Narrator button → ElevenLabs API (male/female voice toggle, API key reuse from Academy)
- [ ] Re-enable audio (uncomment ~2 lines in JS), test all 6 sounds on device, test music pause/resume on video play
- [ ] Marketing email pipeline + unsubscribe endpoint (Privacy Policy promises this — must exist before first campaign)
- [ ] Brand the Supabase magic-link email (currently plain "Confirm your signup" default template)
- [ ] Fix Resend return-path cosmetic: "@send.quantumcube.app" → display "@quantumcube.app"
- [ ] App stores — Google Play (PWABuilder.com → .aab → $25 dev account); Apple (Capacitor → Xcode → $99/yr)
- [ ] Social proof / testimonials section
- [ ] Sharing mechanism for readings
- [ ] Analytics — track usage
- [ ] Profile deletion Edge Function (privacy policy promises 30-day deletion on request)
- [ ] Dead CSS cleanup: `.pay-btn`, `.pay-btn-alt`, `.pay-price-lines span`, `.demo-btn` (left in place from today's cleanup)
- [ ] Fix iframe `allow`/`allowfullscreen` warning on line ~559 (5 iframes total)
- [ ] Gmail aliases propagation check (info, privacy, keyzer, michelle, ronnie @ qncacademy.com)
- [ ] 2FA on all 3 partner Workspace accounts
- [ ] DMARC tightening from p=none → p=quarantine after 1-2 weeks clean reports
- [ ] Migrate business services from `quantumneurocreations@gmail.com` → `admin@qncacademy.com` (audit all service logins)
- [ ] Duplicate `.DS_Store` line in .gitignore (cosmetic)

### 📦 Content complete (no action needed)
- [x] PRIORITY 1 — Content Variations (all 9 categories, 3 variations each)
- [x] PRIORITY 2 — Content Accuracy Review (numerology + Western + Chinese zodiac all verified)

---

## INFRASTRUCTURE LIVE (end of April 18)

| System | State |
|---|---|
| GitHub Pages | Live, serving commit 7ecfae6 (last HTML deploy) |
| quantumcube.app domain | Registered at Cloudflare, DNS managed, not yet pointed at Pages |
| qncacademy.com domain | Registered at Cloudflare, DNS managed, MX + SPF + DKIM + DMARC all live |
| Google Workspace | admin@qncacademy.com active, 5 aliases created |
| Gmail inbox filters | 5 rules auto-label incoming mail by recipient alias |
| Cloudflare Email Routing | *@quantumcube.app → admin@qncacademy.com (active) |
| Email auth qncacademy.com | SPF (soft fail) + DKIM + DMARC (p=none) all live |
| **Resend (NEW)** | **Domain quantumcube.app verified, API key live, SMTP configured in Supabase** |
| **Resend DNS records (NEW)** | **DKIM + MX + SPF + DMARC all propagated** |
| Supabase project | quantum-cube in Frankfurt, ACTIVE_HEALTHY, free tier |
| Supabase schema | profiles table with RLS + auto-create trigger (all verified) |
| Supabase auth config | Site URL + 2 redirect URLs set, custom SMTP via Resend, magic-link live |
| Legal docs | Privacy + POPIA + Security + Terms all align with Supabase account model |
| Legal docs pending | All PayFast references need PayFast → Paddle swap; Resend should be added as sub-processor |

---

## ANNUAL RUNNING COST SUMMARY
- 1× Google Workspace seat: ~R1,340/year
- qncacademy.com renewal: ~R200/year
- quantumcube.app renewal: ~R275/year
- Resend: Free tier (3000 emails/month) — $0 until we scale past that
- **TOTAL: ~R1,815/year (~R150/month)**

Excludes: Paddle transaction fees (~5% + $0.50 per transaction, global), Supabase paid tier if free limits exceeded, ElevenLabs narrator API usage, Resend paid tier when scaled.

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

## SESSION LOG — April 18, 2026 — Saturday

### Morning — audit, hygiene, infrastructure
- [x] Full connectivity audit (git, GitHub, SSH, Supabase CLI, Vercel CLI, Node, npm, Python, cwebp, browser MCP, Pages deploy status) — all green
- [x] Supabase CLI logged in + repo linked to quantum-cube project
- [x] Verified RLS policies on profiles — all 4 correct, has_paid truly immutable from client
- [x] Verified `on_auth_user_created` trigger
- [x] Repo hygiene commit 71f3a1a — gitignore .DS_Store, supabase/.temp, backup files
- [x] Discovery: file tail historically truncated at `<but` fragment (176 commits back) — scheduled for fix
- [x] Discovery: all 8 Supabase wiring chunks already shipped (brief was out of date)

### Afternoon — app fixes + Resend infrastructure
- [x] Commit c0b420d — Brief v11 sync (reflected Supabase chunks shipped, Paddle decision, $17 price)
- [x] Commit 773d85a — Sign-out flow: Face 7 Settings with Sign Out button, signOut() clears cache keys, SIGNED_OUT event also clears localStorage
- [x] Commit 316f6a3 — Make Face 7 reachable: Settings link on Face 0 (signed-in only) + Back button on Face 7
- [x] Resend account created, domain quantumcube.app verified, API key generated and stored in .supabase-env
- [x] 4 DNS records added to Cloudflare (DKIM, MX, SPF, DMARC) — all propagated
- [x] Supabase custom SMTP configured — Resend plugged in, tested, unlimited magic-link emails
- [x] Commit 4871fa7 — Payment overlay cleanup: matched logo, lock-card bullets, $17 price, demo removal, truncation fix (missing `</body></html>` added)
- [x] Commit cb1c3b2 — Payment overlay polish: two-line title, stacked price block, cyan button, fixed corrupted .pay-price-big CSS
- [x] Commit 7ecfae6 — Pay button permanent cyan glow (primary CTA always-on)

### Decisions locked in
- Payment processor: PayFast → Paddle (Monday team meeting for account)
- Price: $8 → $17 USD (all visible copy updated)
- Email: Resend as custom SMTP (unlimited sending)
- Business service logins: prefer `admin@qncacademy.com` going forward
- Session-startup protocol added to brief for consistent chat kickoff

### Weekend plan (April 18–19, no Paddle dependency)
1. Update PROJECT_BRIEF.md to v12 (this commit)
2. Chunk 5 — Face 0 form cleanup + interstitial screen + resend button
3. Loading page logo alignment fix
4. Back to Sign Up button two-line fix
5. Age gate on signup
6. Paddle prep doc for Monday team meeting

### Monday+
- Paddle account setup
- Webhook Edge Function
- Full PayFast → Paddle code swap
- Delete test rows from profiles table
- Launch readiness QA

---

## NEXT SESSION STARTING POINT
1. **Run the SESSION STARTUP block** at the top of this document first
2. Continue weekend items: Chunk 5 (Face 0 form + interstitial), loading logo, Back button, age gate
3. On Monday: Paddle team meeting, then webhook Edge Function work
