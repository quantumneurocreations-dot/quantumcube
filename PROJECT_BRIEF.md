# QUANTUM CUBE — PROJECT BRIEF

**Version: v32 | Last Updated: May 4, 2026 (Monday, morning)**

📁 **Archived history → see BRIEF_ARCHIVE.md** — full session timeline, all "biggest wins" history blocks, complete legal text, lessons from every session, and Paddle/PayFast punch list (already shipped) live in the archive. This brief stays focused on current working context.

---

## ⚠️ CRITICAL RULE — ALWAYS READ FIRST

**Quantum Cube and QNC Academy are COMPLETELY SEPARATE projects — at the backend/tooling/profile level.**

- Never mix backend code, Supabase projects, API keys, or tool configs between them
- Quantum Cube has its own Supabase project (Frankfurt) — never touch the Academy one (Ireland)
- Quantum Cube has its own ElevenLabs API key — never share or cross-use

**Asset sharing is fine when explicit.** Copying logos/music/audio across projects is permitted when the user approves. The rule targets backend cross-contamination, not file assets.

### 🚫 NOT Quantum Cube's job — do not touch from a Cube chat

- The Academy website (Next.js codebase at `/Users/qnc/Projects/qnc-academy/`)
- The Quantum Integrator (QI) — Academy's branded AI built on Claude Haiku 4.5
- HeyGen cleanup (Academy's own cleanup task)
- Academy's Vercel deployment
- The Academy Supabase project (Ireland, ref `bevaepokvavzmykjmhda`)
- Any `.env.local`, config, or secret from the Academy side

If a Cube chat drifts into any of the above, stop and ask.

---

## 🚦 NEW CHAT? READ CHAT_KICKOFF.md FIRST

The kickoff doc handles session startup, role split between Chat Claude and Cursor Claude, and the golden rules. Read it first, then read this brief for project-specific context.

---

## 📣 MARKETING — see MARKETING_PLAYBOOK.md

Marketing strategy, launch sequencing, channel playbooks, customer positioning thesis (curious dabbler), shareable cosmic-profile card concept, SEO content strategy, email deliverability plan, tools evaluated, and growth metrics live in the separate marketing playbook.

**Social channel ownership:** Michelle owns all social media posting and interaction from May 4, 2026 (Monday). Brief stays code-focused; Michelle's content workflow lives in the playbook.

---

## STRATEGIC CONTEXT (locked May 3, 2026)

**Team capacity:** 3 full-time partners. Quantum Cube is one of three QNC projects — a launched byproduct with real revenue that can scale on its own, while QNC Academy stays the primary focus and the HR-screening product stays secondary.

**Customer thesis (locked):** Target is the **curious dabbler** (~70-75% of market), not the hardcore astrology enthusiast (~10-15%) or pure gift buyer (~10-15%). The wedge is **simplicity, beauty, one-shot completeness** — not depth. Co-Star wins depth; we don't compete there.

**Product model (locked — supersedes subscription tier plan):** **Multi-product one-time-purchase**. Each new product is its own Dodo product + own `has_paid`-style flag, $17 (Family $25). Planned product line: Quantum Cube (live) → Compatibility → Year Ahead → Tarot → Family. Subscription tier (Quantum Cube Plus, $9.99/mo) is **demoted to "evaluate at month 6 if data supports"**.

**Budget posture:** Money is **not** the limiting factor.

**Timeline posture:** **Aggressive** — meaningful traction on the order of months, not quarters.

**Three legitimate outcome paths** — revisit at month 6 with real channel + revenue data:

1. **Build big** — scale Quantum Cube + sibling products as durable revenue line inside QNC.
2. **Build to flippable** — package documented growth + multi-product portfolio for acquisition.
3. **Build modestly** — sustain on lighter touch + organic while partner capacity stays on Academy + HR.

---

## 🌐 LIVE SITE

`quantumcube.app` is LIVE and accepting real payments since May 2, 2026. Domain pointed at GitHub Pages, SSL active, public landing page + 8 legal pages all responding HTTP 200.

**Live URLs:**

- `https://quantumcube.app/` — public landing page
- `https://quantumcube.app/app` — the cube app
- `https://quantumcube.app/privacy` — privacy policy
- `https://quantumcube.app/terms` — terms of use
- `https://quantumcube.app/refund` — refund policy
- `https://quantumcube.app/disclaimer` — disclaimer
- `https://quantumcube.app/ip` — IP notice
- `https://quantumcube.app/popia` — POPIA / data
- `https://quantumcube.app/security` — security
- `https://quantumcube.app/contact` — contact info

---

## 💳 PAYMENT PROCESSOR — Dodo Payments (LIVE since May 2, 2026)

### Architecture

End-to-end overlay checkout integration. User stays on `quantumcube.app` for the entire payment flow.

1. User taps Pay $17 button on Face 3 lock card
2. Frontend `launchDodo()` calls `dodo-create-session` Edge Function with auth user_id, email, name
3. Edge Function creates Dodo Checkout Session via Dodo's API with `metadata.user_id` embedded
4. Frontend opens overlay via `DodoPaymentsCheckout.DodoPayments.Checkout.open({ checkoutUrl: cks_xxx })`
5. Customer pays inside the overlay (overlay redirects through Dodo's `/status/<id>/succeeded` page)
6. Customer returns to `quantumcube.app/app?payment_id=...&status=succeeded&email=...`
7. `checkDodoReturn()` detects redirect params, strips them, flags `_qcPendingPaymentUnlock = true`, calls `attemptPaymentUnlock()`
8. `attemptPaymentUnlock()` reads session from localStorage directly (Supabase JS client hangs during auth restore), polls profiles via direct REST fetch up to 8x at 1.5s intervals
9. When `has_paid=true` lands (webhook flipped it), `syncUnlockFromProfile()` runs, then `populateFormFromProfile()` + `runCalculation()` fires to land user inside the cube on Face 3
10. Webhook (`dodo-webhook` Edge Function) verifies Standard Webhooks signature via `dodopayments@2.4.1` SDK, updates `has_paid` server-side

### Mode switching

Single `DODO_MODE` constant in `docs/app.html` (~line 2200) and matching `MODE` constant in `dodo-create-session/index.ts` (~line 28). Both must flip together. Supabase secrets (`DODO_PAYMENTS_API_KEY`, `DODO_PAYMENTS_WEBHOOK_KEY`) must also be swapped to match.

**Live + Test product IDs (in Apple Passwords + in code):**

- Test Mode: `pdt_0NdwjT5U975nxTzpogS68`
- Live Mode: `pdt_0Ndx7o41zFEREpoPTyvR2`

**Business ID:** `bus_0NdjpSYtT1ZAbRN6l15dg`

**MoR legal entity:** `Dodo Payments, Inc.` (Delaware-incorporated). Trade name on customer credit card statements: `Dodo Payments`.

**Key files:**

- `docs/app.html` — `launchDodo()`, `checkDodoReturn()`, `attemptPaymentUnlock()`, `_readSessionFromStorage()`, `handleDodoEvent()`, `_resolveDodoSdk()`
- `supabase/functions/dodo-webhook/index.ts` — webhook receiver
- `supabase/functions/dodo-create-session/index.ts` — session minter

### Dodo's permanent strategic role

**Dodo stays the Merchant of Record across surfaces** (web + Android + future iOS where policy allows external checkout). Multi-product expansion: each new product is its own Dodo product, sharing the same Edge Function infrastructure.

---

## 💰 PRODUCT EXPANSION ROADMAP

**Live product:** Quantum Cube — $17 USD, one-time, lifetime access. Numerology + Western astrology + Chinese zodiac + premium AI-narrated content. **Existing buyers retain lifetime access permanently.**

**Planned product line:**

| Product                  | Price | Hook                                                            | Build complexity                                |
| ------------------------ | ----- | --------------------------------------------------------------- | ----------------------------------------------- |
| **Quantum Compatibility**| $17  | You + partner reading. "Send to your S/O" angle.                 | Medium — needs second profile capture + diff logic |
| **Quantum Year Ahead**   | $17  | Annual personalised forecast. Refreshable yearly = revisit hook | Medium — needs date-anchored content generation |
| **Quantum Tarot**        | $17  | One-off tarot session. Standalone, no birth data dependency     | Low-medium — card draw + interpretation logic    |
| **Quantum Family**       | $25  | Family/parent/child compatibility. Gifting angle.               | Medium-high — multi-profile capture, relationship logic |

**Math check:** 50,000 base Cube users × 30% Compatibility attach + 20% Year Ahead attach = ~$1.275M gross vs ~$850k Cube-only.

### Implementation phasing

- **Months 1–3 post-launch:** Focus on growing Quantum Cube. Validate funnel.
- **Month 3–4:** Build Quantum Compatibility (highest attach potential). Soft launch to existing Cube customers.
- **Month 4–5:** Soft-launch Quantum Year Ahead and Quantum Tarot in parallel.
- **Month 5–6:** Quantum Family for gifting season. Re-evaluate full portfolio at month 6.

### Engagement-loop feature: shareable cosmic-profile card

Beautiful single-image PNG summary of the user's reading they can save to phone or share. Drives viral moment + returning-user moment + gifting trigger. Tentative placement: extension of Face 6 with "Save your cosmic card" button. **Slot decision pending** — Phase 2 polish or Phase 6 (months 3-4). Detailed spec lives in MARKETING_PLAYBOOK.md.

### Migration safety

**Existing Cube customers keep lifetime access forever.** Sibling products are purely additive.

### Subscription tier (reserve option, evaluate at month 6)

Quantum Cube Plus ($9.99/mo with daily horoscope generation) is **deferred and demoted**. Reasons: curious-dabbler segment doesn't want a content treadmill; conversion would likely be ~2-3% not 12-15%; daily AI narration scales costs quickly; multi-product approach hits similar revenue without churn.

---

## 📂 FILE LOCATIONS

```
/Users/qnc/Projects/quantumcube/              <- MAIN PROJECT FOLDER
|- docs/                                       <- GITHUB PAGES SOURCE
|   |- index.html                              <- public landing page
|   |- app.html                                <- THE CUBE APP (~349KB, ~3138 lines)
|   |- styles.css                              <- shared Cinzel + Cormorant dark cosmic styling
|   |- manifest.json                           <- static PWA manifest
|   |- privacy.html / terms.html / refund.html
|   |- disclaimer.html / ip.html / popia.html
|   |- security.html / contact.html
|   |- sw.js                                   <- Service worker (current: qc-v191)
|   |- CNAME                                   <- quantumcube.app
|   |- .nojekyll
|   |- qc-icon-192.png / qc-icon-512.png / qc-icon-512-maskable.png
|   |- qc-apple-touch-180.png / qc-favicon-32.png
|   |- Sounds/                                 <- 385 narration MP3s + 5 music tracks
|   - cube-background.jpg                      <- Milky Way background
|- brand/                                      <- QC monogram + wordmark pack
|- supabase/
|   |- config.toml                             <- 5 functions: narrate, delete-account, export-data, dodo-create-session, dodo-webhook
|   |- migrations/
|   |   |- 20260417104424_create_profiles_table_and_rls.sql
|   |   - 20250429140000_narrate_rate_limit.sql
|   - functions/
|       |- narrate/index.ts                    <- ElevenLabs proxy with rate limit
|       |- delete-account/index.ts             <- Auth admin delete
|       |- export-data/index.ts                <- Profile JSON export
|       |- dodo-create-session/index.ts        <- Dodo session minter
|       - dodo-webhook/index.ts                <- Dodo webhook receiver
|- scripts/                                    <- Narration pipeline scripts
|- narration-manifest.json                     <- 385 entries
|- PROJECT_BRIEF.md                            <- This document (v32, lean active brief)
|- BRIEF_ARCHIVE.md                            <- Lossless reference archive
|- MARKETING_PLAYBOOK.md                       <- Marketing strategy + Michelle's playbook
|- CHAT_KICKOFF.md                             <- Chat operating protocol
|- .supabase-env                               <- creds (gitignored, glob pattern .supabase-env*)
|- .cursorrules                                <- Cursor project rules
- .gitignore
```

**GitHub Repo:** `https://github.com/quantumneurocreations-dot/quantumcube`
**Pages source:** `/docs` directory on `main` branch

---

## 🧭 RECENT SAFE ROLLBACK POINTS

(Older anchors live in BRIEF_ARCHIVE.md.)

| Commit    | Why you don't revert past it                                                  |
| --------- | ----------------------------------------------------------------------------- |
| `804856a` | gitignore tightening for .supabase-env* glob (May 4 cleanup).                  |
| `63684ef` | sb-num font scales by value count — multi-number cards lock in size.          |
| `42d3094` | Astrology profile cards lock to grid columns regardless of sign name length. |
| `a06ca3e` | **Re-applied matrix card overflow fix** lost in c3d3e57 — DO NOT lose again. |
| `c3d3e57` | Music ducks during narration.                                                 |
| `1020df5` | Matrix card overflow fix (original).                                          |
| `4c210b3` | Google sign-in button compliant with verification spec.                       |
| `0748a57` | Music files actually deployed (had been silently `.gitignore`d).              |
| `e85ca5c` | **Post-payment auto-runCalculation** — bounce-bug fix. CRITICAL.              |
| `7ff5db8` | **17-line Paddle/PayFast → Dodo legal copy swap.**                            |
| `b3386ea` | **dodo-webhook Edge Function source.**                                        |

When in doubt, `git revert <commit>` a specific bad change rather than resetting through these anchors.

---

## ✅ PAYWALL VERIFICATION PROTOCOL — 4-LAYER DEFENCE

1. `STORE_KEY` is user-scoped (commit `fd41b68`)
2. `syncUnlockFromProfile` unconditionally enforces lock branch for unpaid (commit `2403ca7`)
3. `renderAllContent` gates all 4 face-reveal blocks on `isUnlocked` (commit `0bd5a54`)
4. **Database-level RLS lock on `has_paid` column** (in migration `20260417104424` — `with check` clause prevents user from updating their own `has_paid`)

### Test sequence (run on live `quantumcube.app/app`)

Two test profiles in `public.profiles`:
- `quantumneurocreations@gmail.com` — `has_paid=true`
- `carlkelbrick@gmail.com` — `has_paid=false`

Use **regular Chrome** (not PWA) with **DevTools open**.

1. Clean start: Application → Storage → Clear site data. Hard-refresh.
2. Unpaid test: Sign in as carl. Face 3 must show Lock card with $17 button. Refresh — lock card must STAY.
3. Switch to paid: Sign Out → sign in as quantumneurocreations. Full content visible.
4. Tab close + reopen (paid): Should auto-advance, unlocked.
5. Switch back to unpaid: Lock card must appear again.

---

## TECH STACK (LOCKED)

- **Frontend:** Single HTML file at `docs/app.html`, vanilla JS, CSS3 3D transforms, glassmorphism. **File size: ~349 KB, ~3138 lines.** `runCalculation` at line ~3138.
- **Public site:** static HTML pages at `docs/index.html` + 8 legal pages, shared `docs/styles.css`
- **PWA Manifest:** static file at `docs/manifest.json`. Real PNG icons (192/512/512-maskable). Background + theme color: `#05050f`.
- **Fonts:** Cinzel Decorative, Cinzel, Cormorant Garamond — Google Fonts CDN only
- **Auth:** Supabase magic-link (email OTP) + Google OAuth, SDK v2.45.4 UMD
- **Database:** Supabase Postgres (Frankfurt) — `public.profiles` with RLS, `public.narrate_rate_counters`
- **Email:** Resend via custom SMTP on Supabase
- **Payment:** Dodo Payments overlay SDK (LIVE). MoR. Adaptive Currency ON. Visa Rapid Dispute Resolution ON.
- **Videos:** Vimeo Player API
- **Audio:**
  - **Music:** 5 tracks in `Sounds/Music/` — randomised playback, no-immediate-repeat, ducks to 6% during narration
  - **SFX:** 5 active (reveal_my_cube, select_side, reveal_result ×3, payment, back_to_signup)
  - **Narration:** 385 pre-recorded Valory MP3s — all Face 3/4 narration + welcome greeting; live Edge Function fallback for Face 5 ONLY
- **Haptics:** 3× strength
- **Hosting:** GitHub Pages (source: `/docs` directory on `main`)
- **Custom domain:** `quantumcube.app` via Cloudflare CNAME → `quantumneurocreations-dot.github.io`
- **Email routing:** Cloudflare `*@quantumcube.app` → `admin@qncacademy.com`
- **PWA:** Real `sw.js` file + static `manifest.json` with PNG icons. Two-cache architecture:
  - `qc-v191` — HTML + root assets
  - `qc-narration-v2` — 385 MP3s

---

## 🎙️ ELEVENLABS NARRATOR

- **Voice:** Valory (voice ID `VhxAIIZM8IRmnl5fyeyk`)
- **Production model:** `eleven_turbo_v2_5`, speed 1.15
- **Welcome greeting:** speed 1.00 (slower) — re-rendered May 3
- **Edge Function:** `supabase/functions/narrate/index.ts` (rate-limited, `verify_jwt=false`)
- **Rate limit:** 5/min + 20/hr per IP. Returns HTTP 429 with `Retry-After`.
- **Inventory:** 385 MP3s on disk
- **Live Edge Function only fires for Face 5** (combined results) — ONLY credit-burn path at runtime

Full narration paths + generation pipeline detail in BRIEF_ARCHIVE.md.

---

## 🔧 EDGE FUNCTIONS — current state

### `narrate` (rate-limited)

- ElevenLabs proxy, Postgres-RPC rate limit (5/min + 20/hr per IP)
- Returns 503 + `rate_limit_unavailable` if RPC fails (fail-closed)
- ONLY credit-burn path at runtime (Face 5 only)

### `delete-account`

- Verifies user JWT via `getUser(jwt)` — never trusts client-supplied user id
- Calls `auth.admin.deleteUser(userId)` server-side
- Cascades to `public.profiles` via `on delete cascade` FK
- Frontend wraps signOut in `Promise.race([signOut, 3000ms])` to prevent hang

### `export-data`

- Verifies user JWT
- Returns profile JSON with `Content-Disposition: attachment` header
- POPIA Section 23 / GDPR Article 15 compliance

### `dodo-create-session`

- Mints Dodo Checkout Session URLs (`cks_xxx`) server-side
- Embeds `metadata.user_id` for webhook profile matching
- Defence-in-depth check: confirms user exists in profiles before minting

### `dodo-webhook`

- Receives `payment.succeeded` and `refund.succeeded` events
- Verifies signature via Standard Webhooks SDK
- Updates `has_paid` in profiles

**All five:** `verify_jwt = false` in `supabase/config.toml` + manual JWT/signature handling + CORS headers + service-role key from Edge Function env vars.

---

## 🔊 AUDIO SYSTEM — QC_AUDIO

**Music:** 5-track rotation in `docs/Sounds/Music/`. Randomised on first play AND on each track-end, avoiding immediate repeat. **0.20 baseline volume, ducks to 0.06 during narration** (commit c3d3e57). 300ms duck-down, 600ms duck-up. First-tap auto-start, fades, Vimeo pause-on-play.

**SFX:** 5 files at 0.30 vol, wired to 5 triggers: `reveal_my_cube`, `select_side`, `reveal_result` (random per call), `payment`, `back_to_signup`.

**Haptics:** 3× strength.

---

## 📧 EMAIL INFRASTRUCTURE — Resend

- Resend `admin@qncacademy.com`, domain `quantumcube.app` verified
- eu-west-1, free tier 3000/mo, 100/day
- DNS: DKIM, SPF, DMARC (p=none), MX send subdomain
- Supabase SMTP: `noreply@quantumcube.app`, `smtp.resend.com:465`, 60s min interval
- Magic-link HTML template applied. Full template in BRIEF_ARCHIVE.md.

`support@quantumcube.app` → `admin@qncacademy.com` via Cloudflare email routing.

---

## APP STRUCTURE — 7 FACES + INTERSTITIAL

| Face           | Name                                  | Card label          | Notes                                            |
| -------------- | ------------------------------------- | ------------------- | ------------------------------------------------ |
| Face 0         | Entry / Sign Up Form                  | —                   | Settings link visible here in legal footer       |
| faceCheckEmail | "Check Your Email" interstitial       | —                   |                                                  |
| Face 1         | Introduction video + Welcome greeting | **Introduction**    | Welcome plays once on first signed-in entry      |
| Face 2         | Results Explained videos              | **Videos**          |                                                  |
| Face 3         | Numerology Results                    | **Your Numbers**    | Locked unless paid                               |
| Face 4         | Astrology & Horoscope                 | **Stars and Signs** | Locked unless paid                               |
| Face 5         | Combined Results                      | **Combination**     | Locked unless paid. ONLY live TTS path           |
| Face 6         | Complete / Outro video                | **Complete**        |                                                  |
| Face 7         | Settings                              | —                   | Sign Out, Download My Data, Delete Account, Back |

**Settings discoverability gap:** Settings link currently visible only from Face 0 footer. Once signed in, no obvious in-app navigation to Face 7. Fix is ~30 min — add a gear icon visible on signed-in faces. Slot post-launch.

---

## SUPABASE BACKEND

- **Project:** quantum-cube (ref `fqqdldvnxupzxvvbyvjm`)
- **Region:** Central EU (Frankfurt)
- **Schema:**
  - `public.profiles` (id, email, name, dob, has_paid, marketing_consent, created_at)
  - `public.narrate_rate_counters` + `narrate_rate_limit_try` RPC
- **RLS:** Enabled. 3 profiles policies, `has_paid` locked from client via column-level `with check` clause
- **Trigger:** `on_auth_user_created` → `handle_new_user()` auto-creates profile on auth signup, captures dob + name from `raw_user_meta_data`
- **Cascade FK:** `profiles.id` → `auth.users.id` `on delete cascade`
- **Edge Functions deployed:** narrate ✓, delete-account ✓, export-data ✓, dodo-create-session ✓, dodo-webhook ✓

**Test/team data to delete pre-public-launch:** snapshot list in BRIEF_ARCHIVE.md (re-snapshot before deletion).

---

## FRONTEND WIRING — KEY LINE REFS

**Numbers float — anchor by function/const name not line number when possible.** Snapshot from May 4:

| What                                                    | Approx line in `docs/app.html`                |
| ------------------------------------------------------- | --------------------------------------------- |
| `function runCalculation`                               | **~3138** (STABLE ANCHOR — verified May 4)    |
| const sb = window.supabase.createClient                 | ~500                                          |
| Static manifest link                                    | ~18                                           |
| Favicon link (qc-favicon-32.png)                        | ~25                                           |
| Apple touch icon (qc-apple-touch-180.png)               | ~26                                           |
| `#faceLabelCard` HTML                                   | ~570                                          |
| `.face-label-text` CSS (Cinzel, weight 400)             | ~426                                          |
| `.export-btn` / `.delete-btn` CSS                       | ~290-297                                      |
| `.scoreboard` / `.sb-grid` / `.sb-item` / `.sb-num` CSS | ~202-213 (DUPLICATE blocks — see Fragile)     |
| `.sb-num.sb-num-count-N` CSS scaling rules              | ~210-215                                      |
| `.astro-grid` / `.astro-item` / `.astro-sign` CSS       | ~221-226                                      |
| `.mc` / `.mc-d` matrix card CSS                         | ~212-216                                      |
| QC_AUDIO with duckMusic / unduckMusic                   | ~1008+                                        |
| `_musicTracks` array (5 entries, randomised)            | ~1012                                         |
| `fetchNarration` (Edge Function, Face 5 only)           | ~1350                                         |
| `startNarration` / `startNarrationFromUrl`              | ~1381 / ~1389                                 |
| `playSequence` (Life Phases sequential)                 | ~1405                                         |
| `qcNarrateCard` (Face 3 + Face 4 dispatch)              | ~1421                                         |
| `playWelcomeGreeting`                                   | ~1502                                         |
| voiceState defaults                                     | ~1362                                         |
| `showFace(n)`                                           | ~1535                                         |
| NUM data                                                | ~1551+                                        |
| STORE_KEY const                                         | ~2162                                         |
| `async function checkStoredUnlock`                      | ~2166                                         |
| `syncUnlockFromProfile`                                 | ~2188                                         |
| applyUnlockedState                                      | ~2219                                         |
| Dodo overlay SDK constants (`DODO_MODE` etc)            | ~2200                                         |
| handleRevealClick                                       | ~2324                                         |
| signInWithOtp paths                                     | ~2379, ~2445                                  |
| sb.auth.onAuthStateChange                               | ~2472                                         |
| signOut                                                 | ~2622                                         |
| `_wipeAllLocalState`                                    | ~2631                                         |
| `exportMyData` / `armDeleteAccount` / `confirmDeleteAccount` | ~2641 / ~2681 / ~2701                    |
| `renderAllContent` + 4× `if(isUnlocked){}` reveal gates | ~2801+                                        |
| SW registration                                         | ~2996                                         |

---

## 🔐 AUTH + UNLOCK FLOW

### Session handling

- `persistSession: true`, `detectSessionInUrl: true`, `flowType: "implicit"`
- Session persists in localStorage until explicit signOut
- Closing tab + reopening → auto-advances into app
- Magic-link short-circuit: if session email matches form email → skip magic link
- Mismatched email → signs out session first, fires new magic link
- **Google OAuth path:** brand-new user has email pre-filled+locked + name pre-filled, fills DOB. Returning user auto-fills + runs into cube directly.

### Unlock state — 4-layer defence

(See PAYWALL VERIFICATION PROTOCOL above.)

`applyUnlockedState` hides .lock-screen, reveals face-content — only callable after paid confirmed.

### Account deletion

- Two-tap confirmation pattern (5-second arm window)
- Edge Function admin-deletes user via service-role key
- Cascade FK wipes profile row automatically
- Frontend wipes 6 localStorage keys (STORE_KEY, QC_PENDING_KEY, qc_musicIdx, qc_rotIdx, qc_greet_count, qc_greet_count_)
- `Promise.race(signOut, 3000ms)` prevents hang
- Redirects to `/` (landing) on completion

### Data export

- Single-tap from Settings (Face 7)
- Returns JSON with email, has_paid, marketing_consent, timestamps
- Browser downloads as `quantum-cube-data.json`
- POPIA right of access compliance

### Known remaining UX issues (not launch-blocker)

- Sign out + sign back in as same email same device still fires magic-link. Post-launch polish.
- Settings link only visible from Face 0 footer.
- **Multi-number narration** (Hidden Passion + Karmic Lessons) currently narrates only first number — needs `playSequence` refactor like Life Phases. ~30-45 min.

---

## 🪨 FRAGILE AREAS — DO NOT TOUCH CASUALLY

- **Service worker is a real file** (`sw.js`). Do NOT revert to blob URL — Android Chrome 117+ rejects blob SW silently.
- **Static manifest.json is a real file** (`docs/manifest.json`). Do NOT revert to blob URL — PWABuilder cannot read blob URLs.
- **`@media (min-width:600px)` rules** are desktop-only on mobile — any CSS change inside those media queries is invisible on Ronnie's phone. Base rules apply to mobile.
- **CSS Grid items default to `min-width:auto`** — children can blow out the cell. Add `min-width:0` on grid item CSS to defeat. Recipe burned in: `.mc`, `.astro-item`, `.sb-item` all use this pattern.
- **`.scoreboard` / `.sb-item` / `.sb-num` CSS is DUPLICATED** at lines ~202-207 AND ~208-213 in app.html. Any edit to these rules MUST hit both copies (or use a Python script that counts both). Phase 3 cleanup target.
- **BSD sed can't do multi-line replacements** — use Python one-shot. Never iterate.
- **Python anchor strings MUST be re-grepped against current file state** before each script run — never reuse anchors from earlier recon output. Cost both `c3d3e57` and `63684ef` corrections. Cursor self-correction welcomed.
- **Diff-then-delete logic must have explicit branches** — `if identical → delete; else → halt and ask`. Never let "diff returned different" fall through to delete (would have lost ElevenLabs key in May 4 cleanup).
- **`grep -c` returns exit 1 on zero matches** — kills pipelines silently. Use `|| true`.
- **`head -N` piped after `git log` can trigger SIGPIPE (exit 141)** on macOS. Use `|| true`.
- **`grep` with `\|` alternation unreliable on BSD grep.** Use `grep -E` with `|` for extended regex.
- **Service worker cache bump is mandatory** every commit that changes `docs/app.html` or `docs/manifest.json`.
- **PWA cache stickiness:** "it's not working on my phone" is usually cache or SW install timing, not code. Triage: (1) regular Chrome tab not PWA, (2) Force-stop PWA / Clear storage on Android, (3) Test in regular Chrome to bypass PWA, (4) Uninstall + reinstall PWA.
- **Magic-link must open in main Chrome**, not Gmail's internal browser. Session won't match.
- **Never reintroduce base64 assets** — 10.8MB cleanup reduced file from 11MB to ~349KB.
- **Life Phases is sequential playback** via `playSequence`. Do not convert to 3 separate cards without product approval.
- **Master numbers in NUM.pc are stripped** (commit `636e3d8`). Do not re-add.
- **renderAllContent reveal blocks MUST stay gated on `if(isUnlocked){}`** — removing the gate re-introduces paywall bypass.
- **GitHub Pages source is `/docs` directory.** Do NOT add HTML to repo root expecting it to be served.
- **`docs/CNAME` binds the custom domain.** Removing it breaks `quantumcube.app`.
- **Files can be silently `.gitignore`d for weeks.** Run `git ls-files <path>` to verify deployment, not local presence.
- **JWTs / bearer tokens NEVER paste into Cursor or chat** — debug via DevTools console + Promise.race timeouts. Cursor's refusals on this are correct.
- **NEVER paste secret values into chat — Cursor terminal output included.** A `supabase secrets set` echo leaked the Live API key on May 2. Rotate FIRST in dashboard, then re-set without echo.
- **Edge Functions need `verify_jwt = false` in `supabase/config.toml`** if they handle JWT manually — otherwise Supabase returns 401 before the function runs.
- **Supabase Edge Functions don't expose `Deno.openKv()`.** Use Postgres RPC for state instead.
- **Supabase JS auth methods can hang during INITIAL_SESSION restore.** For UX-critical post-redirect flows, bypass the JS client: read session from localStorage directly + query via REST fetch.
- **Cross-domain redirect kills queued JS state.** Drive post-payment unlock from URL params on page-load, not from overlay callbacks.
- **`window.location.reload()` after detecting payment params can wipe localStorage mid-restore.** Use in-place state update instead.

### Supabase CLI gotchas

- `supabase db execute --project-ref` does not exist. Use `supabase db query --linked "SQL"` from linked project directory.
- `supabase functions logs` requires CLI v2.95+. We have v2.90.0 — use dashboard for logs.
- For CSV output: `-o csv`, NOT `--csv`.

---

## 🛡️ PRE-LAUNCH SECURITY AUDIT (OWASP-style)

**Status:** Scoped May 3 PM. **Run time:** ~1-2 hours focused. **Slot between Phase 2 polish and Phase 5a Play Store submission.**

### Audit checklist

**Authentication + authorization:**
- [ ] Confirm `verify_jwt = false` Edge Functions all manually validate auth correctly. `delete-account` and `export-data` should never trust a client-supplied user_id — both already use `getUser(jwt)`. Re-verify.
- [ ] RLS audit: confirm all 3 `profiles` policies still in place. Confirm `narrate_rate_counters` has appropriate RLS.
- [ ] Confirm column-level `with check` clause on `has_paid` still prevents user-side mutation. Test with malicious-user PATCH attempt.
- [ ] Webhook signature verification: re-confirm `dodo-webhook` Standard Webhooks signature check is non-bypassable (replay attack resistance).

**Rate limiting + abuse:**
- [ ] `narrate`: already rate-limited (5/min, 20/hr per IP) ✓
- [ ] `delete-account`: NOT currently rate-limited — add per-user rate limit (e.g. 1/hour per user).
- [ ] `export-data`: NOT currently rate-limited — add (e.g. 5/hour per user).
- [ ] `dodo-create-session`: NOT currently rate-limited — add per-user cap (e.g. 10/hour per user).

**Information disclosure:**
- [ ] Error message verbosity audit: grep all Edge Functions and frontend for error responses that leak stack traces, table names, internal IDs, or JWT contents.
- [ ] Confirm no debug mode on in production.
- [ ] Open endpoint check: any unauthenticated endpoint that takes user input — confirm input validation is strict.

**Frontend security:**
- [ ] CSP audit: do we have one set on the Pages-served HTML? If not, add a baseline.
- [ ] XSS audit: any place we render user-supplied data into the DOM — confirm `textContent` not `innerHTML`.
- [ ] Magic-link redirect audit: confirm Supabase redirect allow-list is tight enough.

**Operational hygiene:**
- [ ] Sentry shipped (~20 min — see WHAT'S LEFT)
- [ ] Confirm zsh history sanitised of any leaked secrets
- [ ] Apple Passwords / 1Password contains: Dodo Live + Test API keys, webhook secrets, Supabase service role key, Resend API key, ElevenLabs API key. No plaintext anywhere else.

**Supply chain:**
- [ ] CDN-loaded scripts inventory: Supabase JS UMD, Dodo overlay SDK UMD, Cinzel/Cinzel Decorative/Cormorant fonts. Optionally pin SRI hashes for Supabase + Dodo SDKs.

### Output

A single follow-up commit: `chore(security): pre-launch hardening pass`. Expected diff: rate-limit additions to 3 Edge Functions, error message tightening, CSP header if missing. Probably <100 LOC across 5-6 files.

---

## WHAT'S LEFT — ORDERED BY PRIORITY

### ✅ LAUNCH ACHIEVED — May 2, 2026

Quantum Cube is live and accepting real payments. From the v28 Definition of Done list, every required-for-launch item is shipped. Phase 2 polish substantially advanced May 3 evening (23 commits — see archive).

### 🟥 PRE-MARKETING-PUSH (must ship before Phase 4 social launch)

- **Multi-number narration** (~30-45 min) — Hidden Passion + Karmic Lessons should narrate ALL their numbers via `playSequence`, not just the first. Same pattern as Life Phases. Refactor `qcNarrateCard` dispatch logic.
- **Magic-link payment E2E test** — bounce-bug fix from May 2 was tested with OAuth path only. Magic-link path through `attemptPaymentUnlock` untested.
- **Full app walkthrough** — every face, every state, OAuth + magic-link, paid + unpaid.
- **Sentry error monitoring** (~20 min) — pre-marketing-push priority. Right now zero production error visibility.
- **OWASP-style pre-launch security audit** (~1-2 hours) — see PRE-LAUNCH SECURITY AUDIT section above.

### ⚠️ HIGH-VALUE (not launch-blocker, ideally before Phase 5a Play Store)

- Settings discoverability fix (gear icon, ~30 min)
- Email re-verification UX — same-email resubmit detection
- Magic-link email PNG wordmark upgrade (~10 min — copy file + update template img tag)
- **Burner / warmup domain for marketing emails** (~30 min setup + 4-6 weeks warmup) — register `mail.quantumcube.app` or separate domain. Not needed until marketing email list grows.

### 🧹 POST-LAUNCH CLEANUP

- **Dedupe `.scoreboard` / `.sb-item` / `.sb-num` duplicate CSS blocks** in app.html — currently lines ~202-207 AND ~208-213 are identical. Single-source.
- Split `docs/app.html` into .js + .css files
- `git gc --aggressive` — .git folder is 1.2 GB
- Login loop fix (same-email resign triggers new magic link)
- HeyGen cleanup (Academy side)
- Fine-comb audit pass — duplicate CSS selectors, dead code
- Brain + CPU chip icon (designer)
- `git mv` rename brand wordmark filenames to lowercase-with-hyphens
- **Refund the second Live test payment** once Dodo settlement clears
- **Rotate leaked Test API + Test webhook secrets** in Dodo dashboard
- **Delete 9+ test profile rows** from Supabase profiles table before public launch (re-snapshot first)
- **Submit Google OAuth for Verification** (currently Testing mode — only 3 test users)
- **Replace white Google G with original colour Google logo** on sign-up button (now using Light Rectangular spec — verify final visual)
- **Clean zsh history** of leaked secrets

### 📝 POST-LAUNCH FOLLOW-UPS (weeks-months)

- Astrology/Chinese 3-variant versions (currently single-string)
- Face 5 narrative opener variations for remaining 6 paragraphs
- Additional music tracks
- `info@quantumcube.app` via Cloudflare routing (already have `support@`)
- Marketing email pipeline + unsubscribe endpoint
- DMARC `p=none` → `p=quarantine` after 2 weeks clean
- Gmail 2FA on all 3 partner accounts
- Analytics, social proof, sharing, smoke tests

### 🏪 APP STORE SUBMISSIONS

Phase 5a (US-only with Dodo billing, months 1-2) → Phase 5b (English markets, months 2-3) → Phase 5c (global+localised, months 4-6) → Phase 8 (Apple, months 6-9). Full roadmap detail in BRIEF_ARCHIVE.md.

---

## INFRASTRUCTURE LIVE

| System                   | State                                                                                                                       |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| GitHub Pages             | Live (source: `/docs` on `main`. SW **qc-v191**, narration **qc-narration-v2**)                                             |
| **quantumcube.app**      | **LIVE** — landing + 8 legal + /app, all HTTP 200 ✓                                                                         |
| qncacademy.com           | Full email stack live                                                                                                       |
| Google Workspace         | admin@qncacademy.com + 5 aliases                                                                                            |
| Cloudflare Email Routing | *@quantumcube.app → admin@qncacademy.com (incl. support@)                                                                   |
| Cloudflare DNS           | CNAME quantumcube.app → quantumneurocreations-dot.github.io ✓                                                               |
| Resend                   | Verified, SMTP in Supabase, magic-link template applied                                                                     |
| ElevenLabs               | Valory, narrate deployed + rate-limited, usage-based billing enabled (250k cap)                                             |
| Supabase                 | Frankfurt, free tier, RLS verified, 5 Edge Functions deployed, 2 migrations synced                                          |
| **Dodo Payments**        | **LIVE — accepting real payments since May 2, 2026**                                                                        |
| FastSpring               | Account dormant (registered Apr 29, no products live)                                                                       |
| LemonSqueezy             | Application paused (SA tax form delay)                                                                                      |

---

## 💻 DEV ENVIRONMENT (M4 Mac Mini)

Hardware + OS unchanged. Native ARM64 dev tools confirmed (Node v24.15.0, Supabase CLI v2.90.0). Cursor setup unchanged (Privacy Mode ON, `.cursorignore` deleted, Browser MCP verified working).

**CLI version note:** Supabase CLI v2.95+ has `functions logs` subcommand we don't have at v2.90.0. For Edge Function logs, use the dashboard.

---

## SEPARATE PROJECT — QNC ACADEMY (context only)

Path `/Users/qnc/Projects/qnc-academy/`. Stack: Next.js + Vercel + Supabase (Ireland, ref `bevaepokvavzmykjmhda`) + Anthropic (Claude Haiku 4.5) + ElevenLabs + GitHub. QI = Academy's branded AI. HeyGen deprecated — Academy has its own cleanup task. **Never mix backends.**

---

## NEXT SESSION STARTING POINT (May 4, 2026 morning)

23-commit Phase 2 polish marathon shipped May 3 evening. Brief restructured May 4 morning into lean active brief (this doc) + lossless `BRIEF_ARCHIVE.md` for Academy knowledge transfer.

### Remaining Phase 2 polish

- **Multi-number narration** (Hidden Passion + Karmic Lessons via `playSequence`)
- **Magic-link payment E2E test** (architecture is auth-method-agnostic but untested for non-OAuth flow)
- **Full app walkthrough** — every face, every state

### Phase 3 — Cleanup (~30 min)

- Refund the second Live test payment once Dodo settlement clears
- Rotate leaked Test API + Test webhook secrets in Dodo dashboard
- Delete test profile rows from Supabase
- Resend deliverability tested to fresh Gmail / Outlook / Yahoo accounts
- Submit Google OAuth for Verification
- Sentry error monitoring (~20 min)

### Phase 4 — Marketing channel-by-channel attack planning

(New chat, marketing playbook attached. Michelle leads from May 4.)

### Phase 5 — Play Store submission (US-only with Dodo billing, ~2-3 weeks)

### Phase 6 — Multi-product expansion (parallel, months 3-6)

### Phase 7 — Geographic expansion (months 2-6)

### Phase 8 — Apple App Store (months 6-9, deferred)

### Recommended order at start of next coding session

1. Run minimal health check (per CHAT_KICKOFF.md)
2. Multi-number narration fix (Hidden Passion + Karmic Lessons)
3. Magic-link payment E2E test
4. Sentry shipping (~20 min)
5. OWASP-style pre-launch security audit (~1-2 hours, before Phase 5a Play Store)

---

**End of brief v32.** Archived history → `BRIEF_ARCHIVE.md`. Marketing strategy → `MARKETING_PLAYBOOK.md`. Session protocol → `CHAT_KICKOFF.md`.
