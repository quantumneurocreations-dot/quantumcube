# QUANTUM CUBE — PROJECT BRIEF

**Version: v34 | Last Updated: May 4, 2026 (Monday, evening)**

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

Single `DODO_MODE` constant in `docs/app.html` (~line 2290) and matching `MODE` constant in `dodo-create-session/index.ts` (~line 28). Both must flip together. Supabase secrets (`DODO_PAYMENTS_API_KEY`, `DODO_PAYMENTS_WEBHOOK_KEY`) must also be swapped to match.

**Live + Test product IDs (in Apple Passwords + in code):**

- Test Mode: `pdt_0NdwjT5U975nxTzpogS68`
- Live Mode: `pdt_0Ndx7o41zFEREpoPTyvR2`

**Business ID:** `bus_0NdjpSYtT1ZAbRN6l15dg`

**MoR legal entity:** `Dodo Payments, Inc.` (Delaware-incorporated). Trade name on customer credit card statements: `Dodo Payments`.

**Key files:**

- `docs/app.html` — `launchDodo()`, `checkDodoReturn()`, `attemptPaymentUnlock()`, `_readSessionFromStorage()`, `handleDodoEvent()`, `_resolveDodoSdk()`
- `supabase/functions/dodo-webhook/index.ts` — webhook receiver
- `supabase/functions/dodo-create-session/index.ts` — session minter (rate-limited per-IP since May 4 PM)

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
|   |- index.html                              <- public landing page (CSP applied)
|   |- app.html                                <- THE CUBE APP (~350KB, ~3197 line for runCalculation)
|   |- styles.css                              <- shared Cinzel + Cormorant dark cosmic styling
|   |- manifest.json                           <- static PWA manifest
|   |- privacy.html / terms.html / refund.html         (CSP applied)
|   |- disclaimer.html / ip.html / popia.html          (CSP applied)
|   |- security.html / contact.html                    (CSP applied)
|   |- sw.js                                   <- Service worker (current: qc-v201)
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
|   |   |- 20250429140000_narrate_rate_limit.sql
|   |   - 20260430164143_add_dob_name_to_profiles.sql
|   - functions/
|       |- narrate/index.ts                    <- ElevenLabs proxy with rate limit
|       |- delete-account/index.ts             <- Auth admin delete (rate-limited per-user)
|       |- export-data/index.ts                <- Profile JSON export (rate-limited per-user)
|       |- dodo-create-session/index.ts        <- Dodo session minter (rate-limited per-IP)
|       - dodo-webhook/index.ts                <- Dodo webhook receiver
|- scripts/                                    <- Narration pipeline scripts
|- narration-manifest.json                     <- 385 entries
|- PROJECT_BRIEF.md                            <- This document (v34, lean active brief)
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

| Commit    | Why you don't revert past it                                                    |
| --------- | ------------------------------------------------------------------------------- |
| `1324784` | mobile-web-app-capable meta tag added (iOS deprecation fix). SW qc-v201.        |
| `00d1c6c` | CSP fix-up: Sentry CDN connect + Vimeo thumbnail img-src.                       |
| `f6a7db5` | **CSP baseline shipped** — 10 pages, securitypolicyviolation listener → Sentry. |
| `35331bf` | **Edge Function rate limits** — delete-account, export-data, dodo-create-session + tightened error responses across all 5. |
| `1b15ece` | Live Mode active after magic-link E2E test pass (May 4 PM).                     |
| `4b6bdf9` | Multi-number narration shipped (Hidden Passion + Karmic Lessons).               |
| `b99b807` | SW skips caching 206 partial-content responses — Sentry's first real catch.    |
| `730d4d8` | **Sentry error monitoring shipped** — production-only, EU region.               |
| `3f7f297` | Brand cyan refresh across logo variants.                                        |
| `e804ab4` | Brief v32 + new BRIEF_ARCHIVE.md — lossless history split.                      |
| `e85ca5c` | **Post-payment auto-runCalculation** — bounce-bug fix. Verified May 4 PM for both auth paths. |
| `7ff5db8` | 17-line Paddle/PayFast → Dodo legal copy swap.                                  |
| `b3386ea` | dodo-webhook Edge Function source.                                              |

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

- **Frontend:** Single HTML file at `docs/app.html`, vanilla JS, CSS3 3D transforms, glassmorphism. **File size: ~350 KB, ~3197 line for runCalculation.**
- **Public site:** static HTML pages at `docs/index.html` + 8 legal pages, shared `docs/styles.css`. All 9 public pages have strict CSP applied.
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
- **Error monitoring:** Sentry browser SDK 8.50.0, EU region (`o4511330222604288.ingest.de.sentry.io`), production-only gate, error monitoring only (no Session Replay/Tracing/Application Metrics), JWT/email scrubbing in `beforeSend`, release tagged per SW version. Free tier (5k errors/month). CSP violation listener wired to forward as Sentry warnings.
- **Content Security Policy:** applied to all 10 HTML pages via `<meta http-equiv>`. App page allows inline scripts (existing inline handlers); public pages strict (no inline, no external scripts). Allow-list covers Vimeo, jsdelivr, Sentry CDN + ingest, Supabase, Dodo, Google Fonts.
- **PWA:** Real `sw.js` file + static `manifest.json` with PNG icons. Two-cache architecture:
  - `qc-v201` — HTML + root assets (skips caching of HTTP 206 partial-content responses since `b99b807`)
  - `qc-narration-v3` — 385 MP3s

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

All 5 deployed, all use `verify_jwt = false` in `supabase/config.toml` + manual JWT/signature handling + CORS headers + service-role key from Edge Function env vars. **All 5 return generic error codes only — full errors stay in `console.error` for log access.**

### `narrate` (rate-limited)

- ElevenLabs proxy, Postgres-RPC rate limit (5/min + 20/hr per IP)
- Returns 503 + `rate_limit_unavailable` if RPC fails (fail-closed)
- ONLY credit-burn path at runtime (Face 5 only)

### `delete-account` (rate-limited per-user, May 4 PM)

- Verifies user JWT via `getUser(jwt)` — never trusts client-supplied user id
- **Per-user rate limit: 2/min, 5/hr** via `narrate_rate_limit_try` RPC with `delete:USER_ID` bucket key
- Calls `auth.admin.deleteUser(userId)` server-side
- Cascades to `public.profiles` via `on delete cascade` FK
- Frontend wraps signOut in `Promise.race([signOut, 3000ms])` to prevent hang

### `export-data` (rate-limited per-user, May 4 PM)

- Verifies user JWT
- **Per-user rate limit: 5/min, 20/hr** via `narrate_rate_limit_try` RPC with `export:USER_ID` bucket key
- Returns profile JSON with `Content-Disposition: attachment` header
- POPIA Section 23 / GDPR Article 15 compliance

### `dodo-create-session` (rate-limited per-IP, May 4 PM)

- Mints Dodo Checkout Session URLs (`cks_xxx`) server-side
- Embeds `metadata.user_id` for webhook profile matching
- Defence-in-depth check: confirms user exists in profiles before minting
- **Per-IP rate limit: 5/min, 20/hr** via `narrate_rate_limit_try` RPC with `dodo-session:IP` bucket key. IP read from `x-forwarded-for` then `cf-connecting-ip`.

### `dodo-webhook`

- Receives `payment.succeeded` and `refund.succeeded` events
- Verifies signature via Standard Webhooks SDK
- Updates `has_paid` in profiles

### Pattern for adding new rate-limited Edge Functions

Reuse the existing `narrate_rate_limit_try` RPC. No new migration needed. Pick a unique bucket key prefix (e.g. `<function-name>:USER_ID` for per-user, `<function-name>:IP` for per-IP). The RPC returns `{ ok: true }` or `{ ok: false, reason, retry_after }`.

---

## 🛡️ SENTRY ERROR MONITORING (live since May 4)

### Account + project

- **Org:** `quantum-neuro-creations`
- **Project:** Browser JavaScript (Sentry slug `javascript-1`)
- **Region:** EU (Frankfurt-aligned with Supabase + Resend for GDPR consistency)
- **DSN** (public, safe — embedded in code): `https://fc0733d091a210fe80f9213b64fafa8e@o4511330222604288.ingest.de.sentry.io/4511330235908176`
- **Trial:** Auto-started 14-day Business trial on signup (May 4). **Set calendar reminder for May 18** to verify auto-downgrade to free tier landed without surprise billing. Free tier covers 5k errors/month — plenty for early launch.

### Configuration (in `docs/app.html` ~line 500)

- **Production gate:** Only initialises on `quantumcube.app` hostname. Local dev / test environments produce zero Sentry traffic.
- **Error monitoring ONLY:** `tracesSampleRate: 0`, `replaysSessionSampleRate: 0`, `replaysOnErrorSampleRate: 0`. No Session Replay (privacy + quota burn). No Tracing. No Application Metrics.
- **Release tag:** Set to current SW version (`quantum-cube@qc-vNNN`). MUST be bumped together with SW version on every commit that touches `app.html`.
- **PII scrubbing:** `sendDefaultPii: false` + `beforeSend` filter regex-scrubs anything resembling JWT or email address before payload leaves browser.
- **Noise filters in `beforeSend`:** drops common browser-extension errors, `ResizeObserver loop limit exceeded`, generic cross-origin "Script error.", and "Non-Error promise rejection captured".
- **CSP violation listener** (added May 4 PM): `securitypolicyviolation` event handler forwards directive + blocked URI to Sentry as a warning. Surfaces silently-blocked external dependencies.

### Email alerts

Default Sentry rule sends an email to the account owner on first occurrence of any new issue class. Confirmed working May 4.

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

**Resend API key local backup:** intentionally not held locally — Resend hides values after creation, and rotating to capture is a 5-minute job if ever needed. Documented decision May 4 PM.

---

## APP STRUCTURE — 7 FACES + INTERSTITIAL

| Face           | Name                                  | Card label          | Notes                                            |
| -------------- | ------------------------------------- | ------------------- | ------------------------------------------------ |
| Face 0         | Entry / Sign Up Form                  | —                   | Settings gear visible bottom-left here too       |
| faceCheckEmail | "Check Your Email" interstitial       | —                   |                                                  |
| Face 1         | Introduction video + Welcome greeting | **Introduction**    | Welcome plays once on first signed-in entry      |
| Face 2         | Results Explained videos              | **Videos**          |                                                  |
| Face 3         | Numerology Results                    | **Your Numbers**    | Locked unless paid                               |
| Face 4         | Astrology & Horoscope                 | **Stars and Signs** | Locked unless paid                               |
| Face 5         | Combined Results                      | **Combination**     | Locked unless paid. ONLY live TTS path           |
| Face 6         | Complete / Outro video                | **Complete**        |                                                  |
| Face 7         | Settings                              | —                   | Sign Out, Download My Data, Delete Account, Back |

**Settings discoverability:** ✅ gear icon present bottom-left, locked across every face including Face 0. Click → Face 7. Verified May 4 PM by Ronnie.

---

## SUPABASE BACKEND

- **Project:** quantum-cube (ref `fqqdldvnxupzxvvbyvjm`)
- **Region:** Central EU (Frankfurt)
- **Schema:**
  - `public.profiles` (id, email, name, dob, has_paid, marketing_consent, created_at)
  - `public.narrate_rate_counters` + `narrate_rate_limit_try` RPC (now used by 4 functions, not just narrate)
- **RLS:** Enabled. 3 profiles policies, `has_paid` locked from client via column-level `with check` clause
- **Trigger:** `on_auth_user_created` → `handle_new_user()` auto-creates profile on auth signup, captures dob + name from `raw_user_meta_data`
- **Cascade FK:** `profiles.id` → `auth.users.id` `on delete cascade`
- **Edge Functions deployed:** narrate ✓, delete-account ✓, export-data ✓, dodo-create-session ✓, dodo-webhook ✓
- **Secrets configured (10):** DODO_PAYMENTS_API_KEY, DODO_PAYMENTS_WEBHOOK_KEY, ELEVENLABS_API_KEY, SUPABASE_ANON_KEY, SUPABASE_DB_URL, SUPABASE_JWKS, SUPABASE_PUBLISHABLE_KEYS, SUPABASE_SECRET_KEYS, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_URL. CLI `supabase secrets list` shows SHA-256 digests, never values.

**Test/team data to delete pre-public-launch:** snapshot list in BRIEF_ARCHIVE.md (re-snapshot before deletion).

---

## FRONTEND WIRING — KEY LINE REFS

**Numbers float — anchor by function/const name not line number when possible.** Snapshot from May 4 PM (post-CSP + meta-tag commits):

| What                                                    | Approx line in `docs/app.html`                |
| ------------------------------------------------------- | --------------------------------------------- |
| `function runCalculation`                               | **~3197** (STABLE ANCHOR — verified May 4 PM) |
| const sb = window.supabase.createClient                 | ~514                                          |
| Sentry init                                             | ~520                                          |
| `securitypolicyviolation` listener                      | ~551                                          |
| Static manifest link                                    | ~17                                           |
| Favicon link (qc-favicon-32.png)                        | ~25                                           |
| Apple touch icon (qc-apple-touch-180.png)               | ~26                                           |
| `apple-mobile-web-app-capable` + `mobile-web-app-capable` | ~9-10                                       |
| `Content-Security-Policy` meta tag                      | ~6 (right after charset)                      |
| `#faceLabelCard` HTML                                   | ~570                                          |
| `.face-label-text` CSS (Cinzel, weight 400)             | ~426                                          |
| `.export-btn` / `.delete-btn` CSS                       | ~290-297                                      |
| `.scoreboard` / `.sb-grid` / `.sb-item` / `.sb-num` CSS | ~202-213 (DUPLICATE blocks — see Fragile)     |
| `.sb-num.sb-num-count-N` CSS scaling rules              | ~210-215                                      |
| `.astro-grid` / `.astro-item` / `.astro-sign` CSS       | ~221-226                                      |
| `.mc` / `.mc-d` matrix card CSS                         | ~212-216                                      |
| QC_AUDIO with duckMusic / unduckMusic                   | ~1008+                                        |
| `_musicTracks` array (5 entries, randomised)            | ~1012                                         |
| `fetchNarration` (Edge Function, Face 5 only)           | ~1438+                                        |
| `startNarration` / `startNarrationFromUrl`              | ~1455+ / ~1463+                               |
| `playSequence` (Life Phases + multi-num cards)          | ~1480+                                        |
| `qcNarrateCard` (Face 3 + Face 4 dispatch)              | ~1498+                                        |
| `playWelcomeGreeting`                                   | ~1580+                                        |
| `showFace(n)`                                           | ~1610+                                        |
| NUM data                                                | ~1620+                                        |
| STORE_KEY const                                         | ~2240+                                        |
| `async function checkStoredUnlock`                      | ~2250+                                        |
| `syncUnlockFromProfile`                                 | ~2270+                                        |
| applyUnlockedState                                      | ~2300+                                        |
| Dodo overlay SDK constants (`DODO_MODE` etc)            | ~2290                                         |
| handleRevealClick                                       | ~2400+                                        |
| signInWithOtp paths                                     | ~2940 / ~3008                                 |
| signInWithOAuth (Google)                                | ~2867                                         |
| sb.auth.onAuthStateChange                               | ~2550+                                        |
| signOut                                                 | ~2700+                                        |
| `_wipeAllLocalState`                                    | ~2710+                                        |
| `exportMyData` / `armDeleteAccount` / `confirmDeleteAccount` | ~2720+ / ~2760+ / ~2780+               |
| `renderAllContent` + 4× `if(isUnlocked){}` reveal gates | ~2880+                                        |
| SW registration                                         | ~3070+                                        |

Lines drift +1-2 per added meta tag / listener. `runCalculation` and named functions are the reliable anchors.

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
- Edge Function admin-deletes user via service-role key (rate-limited per-user since May 4 PM)
- Cascade FK wipes profile row automatically
- Frontend wipes 6 localStorage keys (STORE_KEY, QC_PENDING_KEY, qc_musicIdx, qc_rotIdx, qc_greet_count, qc_greet_count_)
- `Promise.race(signOut, 3000ms)` prevents hang
- Redirects to `/` (landing) on completion

### Data export

- Single-tap from Settings (Face 7)
- Returns JSON with email, has_paid, marketing_consent, timestamps (rate-limited per-user since May 4 PM)
- Browser downloads as `quantum-cube-data.json`
- POPIA right of access compliance

### Known remaining UX issues (not launch-blocker)

- Sign out + sign back in as same email same device still fires magic-link. Post-launch polish.
- **Magic-link from Gmail opens in user's default Chrome profile, not the same incognito/window session.** Real-user behavior — doesn't break the flow (verified May 4 PM E2E test) but worth documenting. Both OAuth and magic-link auth paths confirmed working through the post-payment unlock flow.

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
- **Service worker cache bump is mandatory** every commit that changes `docs/app.html` or `docs/manifest.json`. Sentry release tag in `Sentry.init()` MUST stay synced with SW cache version.
- **PWA cache stickiness:** "it's not working on my phone" is usually cache or SW install timing, not code. Triage: (1) regular Chrome tab not PWA, (2) Force-stop PWA / Clear storage on Android, (3) Test in regular Chrome to bypass PWA, (4) Uninstall + reinstall PWA.
- **Magic-link must open in main Chrome**, not Gmail's internal browser. Session won't match.
- **Never reintroduce base64 assets** — 10.8MB cleanup reduced file from 11MB to ~350KB.
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
- **Cursor IDE buffer can race with shell-side Python edits, silently dropping changes between successful grep verification and `git commit`.** Mitigation: every commit touching mode/version constants must run a pre-stage verification grep RIGHT BEFORE `git add` — use the pattern from `9062eef`'s commit block (`if both in sync → ship; else → exit 1`).
- **Three-place mode flips (`DODO_MODE` + Edge `MODE` + Supabase secrets) MUST stay in sync.** Mismatch causes confusing 401 errors and can leave Live Mode broken for real customers.
- **Incognito Chrome localStorage persists across same-session windows.** Only quitting all incognito windows clears it. Mitigation for testing: quit ALL incognito windows + reopen fresh, OR verify `localStorage` keys are empty before starting auth tests.
- **HTTP 206 partial-content responses cannot be cached via Cache API.** SW must guard `cache.put()` with `if (resp.ok && resp.status !== 206)` (fixed in `b99b807`). Don't reintroduce.
- **Don't paste literal multi-line shell commands from chat.** Newlines can render as `\n` characters → zsh parse error → `secrets set` silently fails. Type commands manually OR confirm clean paste before hitting Enter.
- **CSP allow-list extension required when adding new external dependencies.** Two CSP meta tags exist: a permissive one in `docs/app.html` (allows Vimeo, jsdelivr, Sentry CDN, Sentry ingest, Supabase, Dodo, Google Fonts) and a strict one in the 9 public pages (Google Fonts only). Adding any new CDN script, font host, fetch endpoint, or iframe source means updating the right CSP. Violations forward to Sentry as warnings via the `securitypolicyviolation` listener — check Sentry inbox after introducing any new external dep.
- **Edge Function error responses MUST stay generic.** Pattern: `console.error("function-name error:", e)` server-side, return `{ error: "specific_code" }` to client. Never leak raw error strings, stack traces, or upstream service errors back to the browser.

### Supabase CLI gotchas

- `supabase db execute --project-ref` does not exist. Use `supabase db query --linked "SQL"` from linked project directory.
- `supabase functions logs` requires CLI v2.95+. We have v2.90.0 — use dashboard for logs.
- For CSV output: `-o csv`, NOT `--csv`.

---

## 🛡️ PRE-LAUNCH SECURITY AUDIT — ✅ COMPLETED May 4, 2026 PM

Four commits shipped today closed the audit:

| Commit    | Bucket                                                                    |
| --------- | ------------------------------------------------------------------------- |
| `35331bf` | **Auth + abuse:** rate limits added to delete-account (per-user 2/min, 5/hr), export-data (per-user 5/min, 20/hr), dodo-create-session (per-IP 5/min, 20/hr). All 5 Edge Functions now return generic error codes only — full errors in `console.error` server-side. |
| `f6a7db5` | **Frontend security:** CSP applied to all 10 HTML pages. App.html permissive (allows existing inline handlers); 9 public pages strict (no inline, no external scripts). `securitypolicyviolation` listener forwards CSP violations to Sentry. |
| `00d1c6c` | CSP fix-up: Sentry CDN connect + Vimeo thumbnail img-src (caught on first deploy by the listener it set up). |
| `1324784` | `mobile-web-app-capable` meta tag added alongside the deprecated apple-prefixed form (iOS 16+ compliance). |

### Manual checks completed May 4 PM

- **zsh history scan:** 3969 lines, 0 matches across 5 secret-shape patterns. No leaked tokens lingering.
- **Apple Passwords inventory:** Dodo Test+Live API keys, Test+Live webhook signing secrets, Test+Live product IDs, Google account credentials, Mac recovery key all backed up.
- **Supabase secrets confirmed (10):** DODO_PAYMENTS_API_KEY, DODO_PAYMENTS_WEBHOOK_KEY, ELEVENLABS_API_KEY, SUPABASE_ANON_KEY, SUPABASE_DB_URL, SUPABASE_JWKS, SUPABASE_PUBLISHABLE_KEYS, SUPABASE_SECRET_KEYS, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_URL.
- **Resend API key:** intentionally not held locally (Resend hides values after creation, rotate-to-capture is 5 min if ever needed). Documented in Email Infrastructure section.

### Items intentionally deferred

- **dodo-create-session JWT verification:** currently trusts body-supplied `user_id`. Theoretical risk: attacker could pay $17 and unlock someone else's account — financially they'd lose $17, target gets free access. Real-world risk near zero. Defer until we have a reason.
- **innerHTML refactor (7 spots in app.html):** all 7 source from internal data tables (NUM, WSIGN, CSIGN) or computed numbers — never raw form input. `fullName` always goes via `textContent`. Verified no user-input → innerHTML flow. No refactor needed.
- **Inline script removal in app.html:** would require multi-hour refactor. CSP allows `'unsafe-inline'` for app.html only; 9 public pages stay strict.

---

## WHAT'S LEFT — ORDERED BY PRIORITY

### ✅ LAUNCH ACHIEVED — May 2, 2026

Quantum Cube is live and accepting real payments. Phase 2 polish substantially complete.

### 🟥 PRE-MARKETING-PUSH

- **Full app walkthrough QA pass** — every face, every state, OAuth + magic-link, paid + unpaid. Casual ongoing as you use the app.

(Security audit, Sentry, multi-narration, magic-link E2E, settings gear icon, mobile-web-app-capable — all shipped.)

### ⚠️ HIGH-VALUE (not launch-blocker, ideally before Phase 5a Play Store)

- Email re-verification UX — same-email resubmit detection
- Magic-link email PNG wordmark upgrade (~10 min — copy file + update template img tag)
- **Burner / warmup domain for marketing emails** (~30 min setup + 4-6 weeks warmup) — register `mail.quantumcube.app` or separate domain. Not needed until marketing email list grows.
- **Verify Sentry trial → free auto-downgrade (May 18, 2026)** — calendar reminder. After 14-day Business trial ends, account drops to free tier (5k errors/month). Confirm no surprise billing landed.

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
- **Delete 9+ test profile rows** from Supabase profiles table before public launch (re-snapshot first; `rkelbrickmail+e2etest@gmail.com` was added via May 4 E2E test, has_paid reset to false at end)
- **Submit Google OAuth for Verification** (currently Testing mode — only 3 test users)
- **Replace white Google G with original colour Google logo** on sign-up button (now using Light Rectangular spec — verify final visual)

### 📝 POST-LAUNCH FOLLOW-UPS (weeks-months)

- Astrology/Chinese 3-variant versions (currently single-string)
- Face 5 narrative opener variations for remaining 6 paragraphs
- Additional music tracks
- `info@quantumcube.app` via Cloudflare routing (already have `support@`)
- Marketing email pipeline + unsubscribe endpoint
- DMARC `p=none` → `p=quarantine` after 2 weeks clean
- Gmail 2FA on all 3 partner accounts
- Analytics, social proof, sharing, smoke tests
- Optional: tighten dodo-create-session to verify caller JWT matches body's `user_id`

### 🏪 APP STORE SUBMISSIONS

Phase 5a (US-only with Dodo billing, months 1-2) → Phase 5b (English markets, months 2-3) → Phase 5c (global+localised, months 4-6) → Phase 8 (Apple, months 6-9). Full roadmap detail in BRIEF_ARCHIVE.md.

---

## INFRASTRUCTURE LIVE

| System                   | State                                                                                                                       |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| GitHub Pages             | Live (source: `/docs` on `main`. SW **qc-v201**, narration **qc-narration-v3**)                                             |
| **quantumcube.app**      | **LIVE** — landing + 8 legal + /app, all HTTP 200, all CSP-protected ✓                                                      |
| qncacademy.com           | Full email stack live                                                                                                       |
| Google Workspace         | admin@qncacademy.com + 5 aliases                                                                                            |
| Cloudflare Email Routing | *@quantumcube.app → admin@qncacademy.com (incl. support@)                                                                   |
| Cloudflare DNS           | CNAME quantumcube.app → quantumneurocreations-dot.github.io ✓                                                               |
| Resend                   | Verified, SMTP in Supabase, magic-link template applied                                                                     |
| ElevenLabs               | Valory, narrate deployed + rate-limited, usage-based billing enabled (250k cap)                                             |
| Supabase                 | Frankfurt, free tier, RLS verified, 5 Edge Functions deployed (4 rate-limited, 1 webhook-signed), 3 migrations synced       |
| **Dodo Payments**        | **LIVE — accepting real payments since May 2, 2026**                                                                        |
| Sentry                   | Live, EU region, error monitoring only, CSP violations forwarded                                                            |
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

## NEXT SESSION STARTING POINT (May 4, 2026 evening snapshot)

Massive May 4 — 14 commits across morning + afternoon + evening. Pre-marketing-push checklist substantially complete: error monitoring live, multi-number narration shipped, magic-link payment E2E verified, security audit passed, settings gear shipped (Apr 30, brief was stale), apple-mobile-web-app-capable deprecation closed.

### What shipped May 4

**Morning:**
- `.supabase-envx` cleanup (Cursor caught data-loss risk in script + self-corrected)
- Brief restructured: lean v32 active brief + lossless `BRIEF_ARCHIVE.md`
- Brand cyan refresh

**Afternoon:**
- Sentry error monitoring shipped (production-only, EU region, error-only)
- Multi-number narration shipped (Hidden Passion + Karmic Lessons via playSequence)
- SW 206 cache-skip fix (Sentry's first real catch within hours of deploy)
- Magic-link payment E2E test PASSED — bounce-bug fix verified for both auth paths
- Live Mode flip cycle clean (Test → Live with pre-stage verification guards)

**Evening (this session):**
- Edge Function rate limits added to delete-account, export-data, dodo-create-session
- Edge Function error responses tightened across all 5 (no more raw error strings to client)
- CSP baseline applied to all 10 HTML pages + securitypolicyviolation → Sentry listener
- CSP fix-up for Sentry CDN connect + Vimeo thumbnail img-src
- mobile-web-app-capable meta tag (iOS deprecation fix)
- Manual: zsh history clean, Apple Passwords inventory documented, Resend backup decision logged

### Recommended order at start of next coding session

1. Run minimal health check (per CHAT_KICKOFF.md)
2. **Phase 5a Play Store prep** — biggest remaining lift before launch traction work. PWABuilder/Bubblewrap to generate `.aab`, store listing assets (feature graphic, phone screenshots, description), content rating questionnaire, Data Safety form, Internal Testing track setup with rkelbrick + carl + michelle as testers.
3. (In parallel) Marketing channel-by-channel attack planning — new chat with marketing playbook attached. Michelle leads social from May 4.

### Calendar reminders

- **May 18, 2026** — Sentry 14-day Business trial expires. Verify auto-downgrade to free tier (5k errors/month). No surprise billing.
- **May 4, 2027** — Annual key rotation review (ElevenLabs + Resend + Dodo + Supabase service role).

---

**End of brief v34.** Archived history → `BRIEF_ARCHIVE.md`. Marketing strategy → `MARKETING_PLAYBOOK.md`. Session protocol → `CHAT_KICKOFF.md`.
