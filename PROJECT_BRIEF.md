# QUANTUM CUBE — MASTER PROJECT DOCUMENT
**Version: v25.1 | Last Updated: April 29, 2026 (Wednesday, evening)**

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

## 🎉 BIGGEST WINS SINCE v24

**1. Payment processor decision FINAL: Dodo Payments.** Application submitted April 29, in 24-72hr review. Dodo actively markets to astrology brands (dedicated blog post on it). LemonSqueezy and FastSpring parked as fallbacks. Paddle definitively ruled out (their AUP explicitly prohibits "fortune-telling/horoscopes/clairvoyance").

**2. Account deletion + data export shipped and VERIFIED end-to-end.** Two new Edge Functions, two-tap confirmation pattern with 5-second arm window, full localStorage wipe, signOut Promise.race timeout, cascade FK from auth.users → public.profiles. Smoke-tested Apr 29 — deletion fully works, fresh signup with same email works, no orphan state.

**3. narrate Edge Function rate-limited.** Postgres RPC-based (5/min, 20/hr per IP). Closes the ElevenLabs credit-burn vulnerability that was a launch-blocker.

**4. Static manifest.json replaces blob URL.** Google Play submission prerequisite met. Real PNG icons still pending (cube icon design work).

**5. Magic-link email rebranded.** Dark cosmic Quantum Cube template applied via Supabase dashboard, preview confirmed.

**6. Brand wordmark pack committed.** White/gold Cinzel Decorative wordmark in 3 PNG variants + Cinzel/Cinzel Decorative woff2 fonts (self-hosted backup).

**7. Database migration history reconciled.** The `profiles` table + RLS + handle_new_user trigger migration that had been applied directly to remote without a committed file is now properly tracked. `db push` works again.

---

## 🌐 LIVE SITE

`quantumcube.app` is LIVE. Domain pointed at GitHub Pages, SSL active, public landing page + 8 legal pages all responding HTTP 200.

**Live URLs:**
- `https://quantumcube.app/` — public landing page (hero, features, $17 pricing, entertainment disclaimer, "Begin" CTA)
- `https://quantumcube.app/app` — the cube app
- `https://quantumcube.app/privacy` — privacy policy
- `https://quantumcube.app/terms` — terms of use
- `https://quantumcube.app/refund` — refund policy (currently Paddle MoR — needs swap to Dodo entity)
- `https://quantumcube.app/disclaimer` — disclaimer
- `https://quantumcube.app/ip` — IP notice
- `https://quantumcube.app/popia` — POPIA / data
- `https://quantumcube.app/security` — security
- `https://quantumcube.app/contact` — contact info with full company details from CIPC

---

## 📅 SESSION TIMELINE

### April 19, 2026 (Saturday, marathon — SW qc-v42 → qc-v99)
56 commits. Auth/unlock architecture fixes, cube orientation, music/voice redesign, card widening, square matrix, marketing consent, mobile lock-screen width fix, payment button parity. ElevenLabs narrator foundation wired.

### April 20, 2026 (Monday, launch-prep — SW qc-v107 → qc-v114)
- `57dd972` Remove 10.8MB base64 AUDIO (11MB → 356KB)
- `fd41b68` **CRITICAL paywall fix #1: STORE_KEY user-scoped**
- `2403ca7` **CRITICAL paywall fix #2: unconditional lock enforcement**
- `94af122` Legal additions: entertainment opener + Original Works + AI-Assisted

### April 21, 2026 (Tuesday, Mac + Cursor hardening)
- `e1070fb` FileVault enabled, Cursor allowlist tightened, `.cursorrules` at repo root, `.cursorignore` deleted.

### April 21-22, 2026 (Tuesday evening → Wednesday morning — narration phase 1 struggle)
Scaffolded pipeline, generated 256 numerology MP3s. Hash-based lookup failed on Android Chrome. Multiple debug rounds.

### April 22, 2026 (Wednesday — narration phase 1 lock + phase 2 ship + SW rebuild)
- `c2e3c80`, `4d51c0d`, `639bd09`, `2ba2a1e`, `e83b152`, `37f19fd`, `b0b87c5` (morning, SW v127→v136)
- `636e3d8`, `be9f385`, `0546755` (afternoon, 129 new MP3s, ~$13 overage)

### April 23, 2026 (Thursday — polish pass + CRITICAL paywall fix #3)
- `0bd5a54` Paywall fix #3 — gate face-reveal blocks on isUnlocked
- `231803e` UX: face-name label card + auto-scroll
- `2d38560` Audio: music refresh + randomisation + cube-touch SFX ripped
- `546363b` Welcome greeting auto-plays first 2 Face 1 entries
- (revert + reset back to `546363b` due to Cursor display glitch)

SW: qc-v138 → qc-v142.

Non-code: refund policy drafted+approved, magic-link email HTML drafted, Paddle + Google Play full requirements audits.

### April 24, 2026 (Friday — public site SHIPPED)

**Massive day.** Public site went live.

- `2e888d2` **Public site: landing page + 9 legal pages + /app route.** Restructured app into `/docs/`. Created landing page, 8 standalone legal pages, shared CSS, CNAME, .nojekyll. Deployed.
- `e8bfbc4` `/docs` restructure for Pages source
- `32a23f0` `.nojekyll` + `/privacy/` redirect
- `cc63d90` `/app/` trailing-slash redirect

GitHub Pages source switched. Cloudflare CNAME propagated. Cloudflare email routing set up. `quantumcube.app` LIVE.

### April 24-27, 2026 (additional fix)
- `7a9b7ac` Music randomisation per session + user-scope welcome counter

### April 28, 2026 (Tuesday — sync + brief update)

Cross-chat sync. Identified gap between Claude chat A (April 23 polish) and Claude chat B (April 24 public site). Re-aligned context. v24 brief generated. Identified untracked `brand/` folder.

### April 29, 2026 (Wednesday — single-day sprint, 12 commits)

The biggest single-day technical sprint of the project. 12 commits shipped:

| Commit | What |
|---|---|
| `7016cb1` | feat(narrate): per-IP rate limiting (Postgres RPC, 5/min + 20/hr) |
| `f9a3df3` | chore(db): commit existing remote migration to repo (profiles + RLS + trigger) |
| `43e397e` | feat(pwa): static manifest.json replaces blob URL |
| `0fcbdb9` | feat(account): data export + account deletion (POPIA/GDPR) |
| `dddb84e` | debug(delete): diagnostic logs + signOut timeout race |
| `21b9c99` | fix(delete): rip diagnostic logs, keep timeout race |
| `9c35570` | feat(brand): commit Quantum Cube wordmark pack |
| `49ea172` | docs: brief v25 (subsequently expanded to v25.1) |

SW: qc-v142 → qc-v147.

**Non-code outcomes Apr 29:**
- Paddle definitively ruled out (verified directly against their AUP)
- LemonSqueezy: SA tax form delay, application paused
- FastSpring: Michelle started KYB, account dormant as fallback
- Dodo Payments signup submitted, in 24-72hr review
- Magic-link email HTML pasted to Supabase dashboard, preview confirmed
- Security audit complete: 3 items checked (rate limit, input validation, key handling) — only narrate rate limit needed fixing
- Paddle/PayFast 26-line punch list captured for post-Dodo cleanup
- Cube icon priority surfaced (needed for app icons + social profile pics — single dependency for two work items)
- Lesson on JWT-handling: tokens never go through Cursor or chat; debug via DevTools Console + Promise.race timeouts instead

---

## 💳 PAYMENT PROCESSOR — Dodo Payments

### Why Dodo

| Factor | Dodo | LemonSqueezy | FastSpring | Paddle |
|---|---|---|---|---|
| Astrology/esoteric content | **Actively markets to it** | Allowed (silent) | Allowed (silent) | **PROHIBITED** |
| Pricing | 4% + 40¢ (+1.5% non-US ~= 5.5% + 40¢) | 5% + 50¢ | ~8.9% | 5% + 50¢ |
| MoR + global tax | ✓ | ✓ | ✓ | ✓ |
| Founded | 2023 | 2021 | 2005 | 2012 |
| SA seller accepted | ✓ | ✓ | ✓ | N/A |
| Current status | **Application pending 24-72hr** | Parked (SA tax form delay) | Parked (account dormant) | Out (AUP exclusion) |

### Dodo AUP — relevant categories for Quantum Cube

- **Spiritual & Astrology services** → "Categories That Often Require Review" (entertainment only, no claims/predictions). We comply ✓ (entertainment opener live since `94af122`)
- **Religious/spiritual *services*** → prohibited, but this targets paid prayer/ritual/spiritual-authority access, not personalized digital readings ✓
- **AI Content Generation tools** → review category if we sold the tool itself; we use AI voice as part of product, not selling generation. Disclosed as "AI-Assisted" in IP page ✓

### Account details
- **Account name:** Quantum Neuro Creations (registering as business, CIPC Pty Ltd)
- **Account owner (operator):** Michelle Booyens
- **Status (Apr 29):** Submitted via dodopayments.com/login, awaiting review (24-72hr)

### Fallback chain (if Dodo rejects)
1. **Dodo** ← we are here
2. **FastSpring** — Michelle has registered, account dormant, can be reactivated. Subdomain `quantumneurocreations_store` already provisioned.
3. **LemonSqueezy** — application open from Apr 28, on SA tax form hold. Stripe-acquired, stable.
4. **Polar.sh** — open-source MoR, Stripe-backed, developer-first
5. **Creem** — newer (2024), indie-hacker focus, lowest fees, less proven
6. **Gumroad** — last resort, 10% flat fee, accepts almost anything digital

All support international payouts to FNB via SWIFT/wire.

### Dodo MoR legal entity name
**TBD** — confirm exact entity name from Dodo dashboard once approved. Likely "Dodo Payments, Inc." but verify before swapping legal copy in 26 places.

### Why Paddle was ruled out (verified Apr 29)
Paddle's AUP explicitly prohibits: *"Digital services associated with pseudo-science, including but not limited to clairvoyance, horoscopes, fortune-telling"*. Quantum Cube includes Western astrology + Chinese zodiac + numerology = textbook fortune-telling per their own definition. Also prohibits products *"where there is no bona fide software or service sold"* — covers our one-time digital reading model. Paddle's signup form errors out at the product-category step if you select anything other than SaaS or digital download. Don't waste time reapplying.

---

## 📋 PADDLE/PAYFAST PUNCH LIST — 26 lines to swap when Dodo approves

### `docs/app.html` — 17 lines
- L2178-2188: PayFast integration block + sandbox credentials
- L2306-2347: `launchPayFast()` function definition
- L2348-2350: `checkPayFastReturn()` function definition
- L2964-2967: page-load handler calling `checkPayFastReturn()`
- L3223: button onclick="launchPayFast()"
- L3027, 3038, 3128, 3153, 3180: 5 in-app legal copy mentions

### `docs/*.html` (8 public pages, 9 occurrences)
- contact.html:31 — billing contact line
- index.html:54 — landing page price note
- ip.html:45 — third-party attribution list
- popia.html:26 — POPIA disclosure
- privacy.html:21 + privacy.html:42 — privacy policy (2 mentions)
- refund.html:48 — refund policy MoR disclosure
- security.html:27 — security page
- terms.html:34 — terms of use

### Migrations
- `supabase/migrations/20260417104424_create_profiles_table_and_rls.sql:31` — `has_paid` column comment mentions PayFast

### Code rename
- `launchPayFast()` → `launchDodo()`
- `checkPayFastReturn()` → `checkDodoReturn()` (or remove entirely if Dodo handles return differently)
- New: Dodo webhook Edge Function at `supabase/functions/dodo-webhook/`

### MoR text swap
- "PayFast (Pty) Ltd" → "Dodo Payments, Inc." (or actual entity name once confirmed)
- "Paddle.com Market Limited" → "Dodo Payments, Inc."

---

## 📜 REFUND POLICY (LIVE — needs Dodo MoR swap)

Currently published at `quantumcube.app/refund` with **Paddle wording**. Update conditions when Dodo approved:
- Replace: "Paddle.com Market Limited" → Dodo legal entity
- Replace: "contact Paddle support" → "contact Dodo Payments support"
- Effective date: bump to swap day

Otherwise wording stands as approved by Ronnie on April 23.

**Full approved wording (kept inline so this brief stays self-contained):**

> # Refund Policy
>
> **Effective date: [TO INSERT]**
>
> Quantum Cube provides instant access to digital content. Because your personalized reading, numerology calculations, astrological interpretations, and voice narrations are delivered immediately upon payment and cannot be returned or un-accessed, **all sales are final and non-refundable.**
>
> Before purchasing, please make sure you understand what Quantum Cube offers:
>
> - A personalized numerology, Western astrology, and Chinese zodiac reading based on the name and date of birth you provide
> - Written interpretations and AI-assisted voice narration (Valory) for each category
> - Content provided for **entertainment and self-reflection purposes only** — Quantum Cube makes no claims of accuracy, predictive power, or scientific validity
> - One-time payment of $17 USD for lifetime access to your personal reading
>
> **No refunds will be issued** for any of the following:
>
> - Change of mind after purchase
> - Dissatisfaction with the content or interpretations
> - Technical issues on your device that did not prevent delivery
> - Accidental purchases (please review carefully before confirming)
> - Failure to read or listen to content after purchase
>
> **Limited exceptions.** We may, at our sole discretion, consider a refund in the following cases:
>
> - Duplicate charges for the same account caused by a technical error on our side
> - Proven inability to access the product due to a verified fault in our systems that we cannot resolve within a reasonable time
> - Any refund required under applicable consumer protection law in your jurisdiction
>
> To request a refund under one of the limited exceptions above, contact **admin@qncacademy.com** within **7 days** of purchase with your email address, date of purchase, and a description of the issue. We will respond within 5 business days.
>
> **Chargebacks.** Initiating a chargeback without first contacting us may result in suspension of your account. We prefer to resolve issues directly with customers.
>
> **Changes to this policy.** We may update this refund policy from time to time. The version in effect on the date of your purchase governs your transaction.
>
> Payments are processed by [Dodo Payments / Sold Through Link, LLC / FastSpring entity — confirm at swap], who acts as the Merchant of Record for all purchases. For payment-related questions, contact support directly or us.

**Rationale notes:**
- "No refunds ever, period" sometimes fails MoR review and is unenforceable under EU/SA/CA consumer law. Limited exceptions clause is narrow but legally sound.
- Chargebacks language is industry-recommended for MoR products.
- Merchant-of-Record disclosure is required under all major MoR ToS.

---

## 📧 MAGIC-LINK EMAIL TEMPLATE (APPLIED Apr 29)

Pasted to Supabase dashboard (Authentication → Email Templates → Magic Link). Preview confirmed.

**Config:**
- Subject: `Verify Your Email`
- Sender name: `Quantum Cube` ✓
- Sender email: `noreply@quantumcube.app` ✓

**Full HTML body (kept inline for re-paste if needed):**

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Verify Your Email</title>
</head>
<body style="margin:0;padding:0;background:#0a0e1a;font-family:Georgia,'Times New Roman',serif;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#0a0e1a;">
    <tr>
      <td align="center" style="padding:60px 20px;">
        <table role="presentation" width="480" cellpadding="0" cellspacing="0" border="0" style="max-width:480px;width:100%;">
          <tr>
            <td align="center" style="padding:0 0 40px 0;">
              <div style="font-family:Georgia,'Times New Roman',serif;font-size:24px;letter-spacing:6px;color:#ffffff;text-transform:uppercase;font-weight:normal;">
                Quantum Cube
              </div>
            </td>
          </tr>
          <tr>
            <td align="center" style="padding:0 20px 40px 20px;">
              <p style="margin:0;font-family:Georgia,'Times New Roman',serif;font-size:15px;line-height:1.6;color:#c8d0e0;letter-spacing:1px;">
                Tap below to sign in.
              </p>
            </td>
          </tr>
          <tr>
            <td align="center" style="padding:0 0 40px 0;">
              <a href="{{ .ConfirmationURL }}" style="display:inline-block;padding:16px 48px;background:#0f1829;border:1px solid #7dd4fc;border-radius:999px;color:#ffffff;text-decoration:none;font-family:Georgia,'Times New Roman',serif;font-size:14px;letter-spacing:4px;text-transform:uppercase;box-shadow:0 0 20px rgba(125,212,252,0.25);">
                Verify
              </a>
            </td>
          </tr>
          <tr>
            <td align="center" style="padding:0 20px;">
              <p style="margin:0;font-family:Georgia,'Times New Roman',serif;font-size:11px;line-height:1.6;color:#6a7388;letter-spacing:1px;">
                Didn't request this? You can safely ignore this email.
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
```

Leave `{{ .ConfirmationURL }}` exactly as written — Supabase replaces it at send time.

**Visual:** dark navy background, "QUANTUM CUBE" wordmark in spaced caps (system font fallback — see note below), single rounded-pill "VERIFY" button with sky-blue glow border, small grey "didn't request this?" footer.

**Pending upgrade:** swap inline text wordmark for hosted PNG from `brand/quantum-cube-logo-1400.png` once brand folder is publicly served. Email clients don't render Cinzel Decorative reliably (no web fonts in email), so PNG is the only way to get true on-brand wordmark.

---

## 🎨 BRAND IDENTITY

### Existing assets — committed Apr 29 in `brand/` folder

- `quantum-cube-logo-1400.png` — wordmark, 1400px wide
- `quantum-cube-logo-2800.png` — wordmark, 2800px wide (high-res print)
- `quantum-cube-logo.svg` — wordmark vector
- `quantum-cube-tiktok-1080.png` — TikTok profile variant, 1080×1080 square
- `quantum-cube-tiktok-profile.svg` — TikTok variant vector
- `cinzel-decorative-bold.woff2` + `cinzel-regular.woff2` — self-hosted fonts (backup if Google Fonts CDN fails)

### Visual language — locked

- **Primary typeface:** Cinzel Decorative (wordmarks)
- **Secondary typeface:** Cinzel (subtitles, smaller text)
- **Tertiary typeface:** Cormorant Garamond (body, italic)
- **Colour pattern:** white-as-base + ONE gold/orange accent word as keyword highlight
- **Background:** dark cosmic / black (#05050f primary, #071b2e secondary)
- **Accent glow:** cyan (#7dd4fc) for cube and interactive elements
- **Style:** ornate serif, premium, mystical-but-clean

### Logo work still needed

| Asset | Purpose | Status |
|---|---|---|
| **Cyan cube icon (square)** | App icon, favicon, social profile pic | **Needed — Canva Pro attempt then Fiverr if needed** |
| Real PNG icons at 192/512/maskable | manifest.json, Google Play submission | **Needed (depends on cube icon)** |
| Apple touch icon (180×180 PNG) | iOS home screen | **Needed (depends on cube icon)** |
| Favicon (32×32 PNG) | Browser tab | **Needed (depends on cube icon)** |
| Brain + CPU chip half/half icon | Brand family conceptual badge | Optional, post-launch |

**Tool decision:** Canva Pro for cube icon attempt (Ronnie has access). 30-min Canva attempt; if illustration doesn't land well, $30-50 Fiverr designer for square icons matching the in-app cyan cube vibe. Don't sink hours into Canva trying to make illustration work — wordmarks are trivial in Canva (text), icons are illustration.

The cube icon is **the single dependency** for two outstanding work items (manifest PNGs + social profile pics). Knock it out, both unblock.

---

## 📱 SOCIAL MEDIA — handles to claim (NOT YET CREATED)

Decided April 28, confirmed April 29. Claim now, **post nothing until launch announcement.**

| Platform | Preferred | Fallback |
|---|---|---|
| YouTube | @quantumcube | @quantumcubeapp |
| Facebook | /quantumcube | /quantumcubeapp |
| X / Twitter | @quantumcube | @quantumcubeapp |
| Instagram | @quantumcube | @quantumcubeapp |
| TikTok | @quantumcube | @quantumcubeapp |
| Threads | @quantumcube | @quantumcubeapp |

**Steps:**
1. namechk.com to verify availability across all 6
2. If `@quantumcube` not available everywhere → fall back to a single consistent alternative across all
3. Set up profiles with consistent display name "Quantum Cube" + same bio + same logo + same banner
4. **Don't post anything** until launch — prevents impersonation, locks brand consistency

**Blocker:** social media setup needs the cube icon for profile pics. Sequence: cube icon → social claiming.

---

## 📂 FILE LOCATIONS
/Users/qnc/Projects/quantumcube/              <- MAIN PROJECT FOLDER
|- docs/                                       <- GITHUB PAGES SOURCE
|   |- index.html                              <- public landing page
|   |- app.html                                <- THE CUBE APP
|   |- styles.css                              <- shared Cinzel + Cormorant dark cosmic styling
|   |- manifest.json                           <- static PWA manifest (committed Apr 29)
|   |- privacy.html / terms.html / refund.html
|   |- disclaimer.html / ip.html / popia.html
|   |- security.html / contact.html
|   |- sw.js                                   <- Service worker (qc-v147 + qc-narration-v2)
|   |- CNAME                                   <- quantumcube.app
|   |- .nojekyll
|   |- Sounds/                                 <- audio assets (385 narration MP3s + 5 music tracks)
|   - cube-background.jpg                     <- Milky Way background
|- brand/                                      <- Wordmark PNGs + SVGs + Cinzel fonts (committed Apr 29)
|- supabase/
|   |- config.toml                             <- function-level flags (3 functions: narrate, delete-account, export-data)
|   |- migrations/
|   |   |- 20260417104424_create_profiles_table_and_rls.sql
|   |   - 20250429140000_narrate_rate_limit.sql
|   - functions/
|       |- narrate/index.ts                    <- ElevenLabs proxy with rate limit
|       |- delete-account/index.ts             <- Auth admin delete (Apr 29)
|       - export-data/index.ts                <- Profile JSON export (Apr 29)
|- scripts/                                    <- Narration pipeline scripts
|- narration-manifest.json                     <- 385 entries
|- PROJECT_BRIEF.md                            <- This document (v25.1)
|- CHAT_KICKOFF.md                             <- Chat operating protocol
|- .supabase-env                               <- creds (gitignored)
|- .cursorrules                                <- Cursor project rules
- .gitignore

**GitHub Repo:** https://github.com/quantumneurocreations-dot/quantumcube
**Live URLs:** see "LIVE SITE" section above
**Pages source:** `/docs` directory on `main` branch

---

## 🧭 CANONICAL SAFE ROLLBACK POINTS

**Do not revert past these without conscious decision.**

| Commit | Why you don't revert past it |
|---|---|
| `21b9c99` | **Account deletion + export production-ready.** Reverting = stuck "Deleting..." bug returns + Google Play hard-requirement fails. CRITICAL |
| `0fcbdb9` | Account deletion + export shipped. Reverting = no in-app deletion, Google Play submission blocked. CRITICAL |
| `43e397e` | Static manifest.json. Reverting = blob URL returns, PWABuilder broken, Google Play submission blocked |
| `f9a3df3` | Migration reconciliation. Reverting = `db push` fails, unable to deploy new migrations |
| `7016cb1` | narrate rate limit. Reverting = ElevenLabs credit-burn vulnerability returns |
| `cc63d90` | `/app/` trailing-slash redirect — without this `quantumcube.app/app/` 404s |
| `32a23f0` | `.nojekyll` for static HTML + privacy redirect — without this Pages mangles HTML |
| `e8bfbc4` | `/docs` restructure — reverting breaks Pages deployment |
| `2e888d2` | **Public site landing + legal pages.** Reverting kills MoR/Google Play readiness. CRITICAL. |
| `7a9b7ac` | Music randomisation per session + user-scoped welcome counter |
| `546363b` | Welcome greeting auto-play from local MP3. Reverting re-adds button + live-TTS credit burn |
| `2d38560` | Music refresh + randomisation + cube-touch SFX rip |
| `231803e` | Face-name label card + auto-scroll. Reverting removes "you are here" UX |
| `0bd5a54` | **Paywall fix #3 — renderAllContent gating.** Reverting = unpaid users see full content on page refresh. CRITICAL |
| `0546755` | Narration phase 2 wiring — Life Phases sequential + Face 4 astro/chinese narration + SW cleanup |
| `be9f385` | 129 phase 2 MP3s committed to repo |
| `636e3d8` | Narration phase 2 prep — strip dead 11/22 from NUM.pc |
| `b0b87c5` | SW diagnostics rip + ASSETS fix |
| `37f19fd` | Real sw.js file replaces blob URL — Android Chrome 117+ fix |
| `4d51c0d` | data-variant alignment — voice matches text |
| `c2e3c80` | Numerology direct MP3 path — ripped sha256 manifest |
| `e1070fb` | Cursor hardening — `.cursorrules` + allowlist + gitignore |
| `94af122` | Legal additions — entertainment opener, Original Works, AI-Assisted |
| `2403ca7` | **Paywall fix #2** — unconditional lock enforcement in `syncUnlockFromProfile` |
| `fd41b68` | **Paywall fix #1** — STORE_KEY user-scoped |
| `57dd972` | 10.8MB cleanup — reverting blows file back up to 11MB |

When in doubt, `git revert <commit>` a specific bad change rather than resetting through these anchors.

---

## ✅ PAYWALL VERIFICATION PROTOCOL — 4-LAYER DEFENCE

**Four-layer defence:**
1. `STORE_KEY` is user-scoped (fix #1 — `fd41b68`)
2. `syncUnlockFromProfile` unconditionally enforces lock branch for unpaid (fix #2 — `2403ca7`)
3. `renderAllContent` gates all 4 face-reveal blocks on `isUnlocked` (fix #3 — `0bd5a54`)
4. **Database-level RLS lock on `has_paid` column** (in migration `20260417104424` — `with check` clause prevents user from updating their own `has_paid`. Surfaced to brief Apr 29 — was always there but undocumented)

### Test sequence (run on live `quantumcube.app/app`)

- Two test profiles in `public.profiles`:
  - `quantumneurocreations@gmail.com` — `has_paid=true`
  - `carlkelbrick@gmail.com` — `has_paid=false`
- Use **regular Chrome** (not PWA) with **DevTools open** for storage inspection

1. **Clean start:** Chrome DevTools → Application → Storage → Clear site data. Hard-refresh.
2. **Unpaid test:** Sign in as carl. Face 3 must show Lock card with $17 button, NO numerology visible. **Refresh page — lock card must STAY** (this is the fix #3 check).
3. **Switch to paid:** Sign Out → sign in as quantumneurocreations. Full content visible, Valory narrates.
4. **Tab close + reopen (paid):** Should auto-advance, unlocked, no magic link re-verify.
5. **Switch back to unpaid:** Sign Out → sign in as carl. Lock card must appear again.

**Paywall verified working both directions on April 23.**

---

## 🏁 DEFINITION OF DONE — LAUNCH GATE

### ✅ DONE
- [x] Narration phase 1 verified (256 numerology MP3s, offline-capable)
- [x] Narration phase 2 shipped (9 Life Phases + 60 Western Astro + 60 Chinese MP3s, offline-capable)
- [x] Service worker rebuilt (qc-v147, two-cache architecture)
- [x] Paywall fix #3 (renderAllContent gated)
- [x] Music refresh + randomisation
- [x] Welcome greeting auto-plays
- [x] Face name label card + auto-scroll
- [x] Public landing page + 8 legal pages live
- [x] quantumcube.app domain HTTPS verified
- [x] Paywall verified both directions (Apr 23)
- [x] Accessibility trio (user-scalable=no removed, labels on 12 inputs)
- [x] Legal copy final (entertainment opener, Original Works, AI-Assisted)
- [x] **narrate Edge Function rate-limited (5/min + 20/hr per IP)** ← Apr 29
- [x] **Static manifest.json (replaces blob URL)** ← Apr 29
- [x] **Account deletion mechanism (in-app, working, end-to-end verified)** ← Apr 29
- [x] **Data export mechanism (POPIA/GDPR right of access)** ← Apr 29
- [x] **Magic-link email redesigned + applied** ← Apr 29
- [x] **Migration history reconciled** ← Apr 29
- [x] **Brand wordmark pack committed** ← Apr 29

### ⏳ TO DO — pre-launch

**Code:**
- [ ] **Google OAuth 2.0** (~2-3 hrs) — Google Cloud Console OAuth credentials, Supabase provider config, frontend "Continue with Google" button + callback handling, DOB-only follow-up form. Reasoning: removes magic-link-on-mobile fragility (Gmail internal browser issue), brand trust signal.
- [ ] **Dodo webhook Edge Function** (~1 hr after Dodo approval) — receives payment confirmation, sets `has_paid=true`
- [ ] **`launchDodo()` swap** (~30 min after Dodo approval) — replaces `launchPayFast()`
- [ ] **26-line Paddle/PayFast wording swap** (after Dodo approved + entity name confirmed)
- [ ] **E2E payment test** → refund to self
- [ ] **Real PNG icons in manifest** (192/512/maskable, plus apple-touch-icon, favicon) — needs cube icon designed first

**Non-code (Ronnie solo):**
- [ ] **Cube icon designed in Canva Pro** (~30 min attempt; if doesn't land, Fiverr ~$50)
- [ ] **Social media handles claimed** across 6 platforms (~30 min, after cube icon done)
- [ ] **Magic-link email PNG wordmark upgrade** (post brand-folder-deployed, swap inline text for hosted PNG)

**Backend cleanup:**
- [ ] **Delete 9+ test profile rows** from Supabase profiles table before launch (re-snapshot pending)
- [ ] **Resend deliverability tested** to fresh Gmail, Outlook, Yahoo accounts

### ⏳ TO DO — UX polish (not launch-blocker)
- [ ] **Settings discoverability** — currently the Settings link is only on the signup screen. Add a settings gear ⚙️ icon visible to signed-in users so they can reach Delete Account / Sign Out without first signing out. ~30 min, slot into Google OAuth session or post-launch.
- [ ] Sentry error monitoring (~20 min)
- [ ] At least 5 smoke tests against live site

### Not required for launch but strongly recommended
- [ ] Quantum Cube wordmark refinement (already have base, may want crisper export)
- [ ] Brain + CPU chip icon (designer, post-launch)

---

## 💰 SUBSCRIPTION AUDIT — OUTCOMES (carried forward from v23/v24)

### ✅ Keep as-is
Claude Max, Claude Console (API), Cursor Pro, Epidemic Sound, CapCut Pro, ElevenLabs Creator (usage-based enabled April 22), Google Workspace, GitHub, Canva Pro (added Apr 29).

### ⬇️ Downgrade / switch (parked pending team discussion)
- Vercel Pro → Hobby (~$20/mo savings)
- Vimeo Starter → annual billing (~$65/yr savings)

### ❌ Confirmed deprecated
- HeyGen — canceled. Academy codebase cleanup pending (not a Cube task).
- PayFast — replaced by Dodo Payments (pending approval). Code references to be removed via 26-line punch list.
- Paddle — never used, definitively excluded by AUP.

---

## 📜 CONTENT LICENSING — RESOLVED

Numerology/astrology concepts public domain; written interpretations original expression. Three legal additions shipped April 20 (commit `94af122`). Content licensing not a launch-blocker.

Third-party attributions in IP tab + public IP page: Epidemic Sound, Google Fonts. **PayFast reference must be swapped to Dodo entity post-approval** (part of the 26-line punch list).

---

## 💻 DEV ENVIRONMENT (M4 Mac Mini)

Hardware + OS unchanged. Native ARM64 dev tools confirmed (Node v24.15.0, Supabase CLI v2.90.0). Cursor setup unchanged (Privacy Mode ON, `.cursorignore` deleted, Browser MCP verified working).

**CLI version note:** Supabase CLI v2.95+ has `functions logs` subcommand we don't have at v2.90.0. For Edge Function logs, use the dashboard (Project → Edge Functions → function name → Logs). Worth upgrading the CLI when convenient.

---

## TECH STACK (LOCKED)

- **Frontend:** Single HTML file at `docs/app.html`, vanilla JS, CSS3 3D transforms, glassmorphism. **File size: ~349 KB, ~3194 lines.** `runCalculation` at line 2745 (Apr 29 reference; will drift)
- **Public site:** static HTML pages at `docs/index.html` + 8 legal pages, shared `docs/styles.css`
- **PWA Manifest:** static file at `docs/manifest.json` (Apr 29). SVG data-URI icon for now; PNG icons pending cube icon design.
- **Fonts:** Cinzel Decorative, Cinzel, Cormorant Garamond (Google Fonts CDN; self-hosted backup in `brand/`)
- **Auth:** Supabase magic-link (email OTP), SDK v2.45.4 UMD. Google OAuth pending.
- **Database:** Supabase Postgres (Frankfurt) — `public.profiles` with RLS, `public.narrate_rate_counters` (Apr 29)
- **Email:** Resend via custom SMTP on Supabase. Magic-link template applied Apr 29.
- **Payment:** PayFast sandbox currently wired — **Dodo Payments swap pending approval** (Paddle ruled out, LemonSqueezy + FastSpring as fallbacks)
- **Videos:** Vimeo Player API
- **Audio:**
  - **Music:** 5 tracks in `Sounds/Music/` — randomised playback, no-immediate-repeat
  - **SFX:** 5 active (reveal_my_cube, select_side, reveal_result ×3, payment, back_to_signup). cube_touch removed April 23.
  - **Narration:** 385 pre-recorded Valory MP3s — all Face 3/4 narration + welcome greeting; live Edge Function fallback for Face 5 ONLY
- **Haptics:** 3× strength
- **Hosting:** GitHub Pages (source: `/docs` directory on `main`)
- **Custom domain:** `quantumcube.app` via Cloudflare CNAME → `quantumneurocreations-dot.github.io`
- **Email routing:** Cloudflare `*@quantumcube.app` → `admin@qncacademy.com` (incl. `support@quantumcube.app`)
- **PWA:** Real `sw.js` file + static `manifest.json`. Two-cache architecture:
  - `qc-v147` — HTML + root assets
  - `qc-narration-v2` — 385 MP3s (precached on install + on-demand fallback)

---

## 🎙️ ELEVENLABS NARRATOR

- **Voice:** Valory (voice ID `VhxAIIZM8IRmnl5fyeyk`)
- **Model:** `eleven_turbo_v2_5` — `{stability:0.5, similarity_boost:0.75, speed:1.15}`
- **Edge Function:** `supabase/functions/narrate/index.ts` (now ~100 lines with rate limit, `verify_jwt=false`, manual apikey-header check, Postgres RPC for rate counter)
- **Rate limit:** 5/min + 20/hr per IP (Apr 29). Returns HTTP 429 with `Retry-After` header.
- **Narration inventory on disk:** 385 MP3s
- **Frontend narration paths:**
  - Welcome: `playWelcomeGreeting()` → `startNarrationFromUrl('Sounds/Narration/welcome.mp3')` on first 2 Face 1 entries (counter `qc_greet_count_<uid>`)
  - Face 3 numerology categories → `startNarrationFromUrl` → `Sounds/Narration/num_<cat>_<num>_v<variant>.mp3`
  - Face 3 Life Phases → `playSequence` → 3× `Sounds/Narration/num_pc_<n>_v1.mp3` sequential
  - Face 4 western → `Sounds/Narration/west_<sign>_<slot>.mp3`
  - Face 4 chinese → `Sounds/Narration/chin_<animal>_<slot>.mp3`
  - Face 5 combined → `fetchNarration` → live Edge Function (ONLY credit-burn path at runtime)

---

## 🔧 EDGE FUNCTIONS — current state (Apr 29)

### `narrate` (rate-limited Apr 29)
- Voice: Valory, model `eleven_turbo_v2_5`
- Rate limit: per-IP via Postgres RPC (`narrate_rate_limit_try`), 5/min + 20/hr, atomic check-and-increment with `FOR UPDATE` row lock
- 2500-char input cap, JWT validation (manual via apikey header check)
- ONLY credit-burn path at runtime (Face 5 only)
- Returns 503 + `rate_limit_unavailable` if RPC fails (fail-closed)

### `delete-account` (NEW Apr 29)
- Verifies user JWT via `getUser(jwt)` — never trusts client-supplied user id
- Calls `auth.admin.deleteUser(userId)` server-side using service-role key
- Cascades to `public.profiles` via `on delete cascade` FK
- Logs deletion server-side (id + timestamp, no email)
- Frontend wraps signOut in `Promise.race([signOut, 3000ms])` to prevent hang

### `export-data` (NEW Apr 29)
- Verifies user JWT
- Returns profile JSON with `Content-Disposition: attachment` header for browser download
- POPIA Section 23 / GDPR Article 15 compliance (right of access)
- Includes explanatory note: "Reading content is generated deterministically from your inputs at runtime and is not stored."

**All three:** `verify_jwt = false` in `supabase/config.toml` + manual JWT handling + CORS headers + service-role key from Edge Function env vars.

**Pending:** `dodo-webhook` Edge Function (after Dodo approval) — receives payment confirmation, sets `has_paid=true`.

---

## 🔊 AUDIO SYSTEM — QC_AUDIO

**Music:** 5-track rotation in `docs/Sounds/Music/`:
- `ES_Across the Meadow - Hanna Lindgren.mp3`
- `ES_Subterranean Room - Hanna Lindgren.mp3`
- `ES_Tranquil Dawn - Amber Glow.mp3`
- `ambient.mp3`
- `bgMusic.mp3`

Playback: randomised on first play AND on each track-end, avoiding immediate repeat. 0.20 volume, first-tap auto-start, fades, Vimeo pause-on-play. Index persisted in `localStorage.qc_musicIdx`.

**SFX:** 5 files at 0.30 vol, wired to 5 triggers:
- `reveal_my_cube` (`Reveal my cube.mp3`)
- `select_side` (`Select cube side.mp3`)
- `reveal_result` (`Reveal Result 1/2/3.mp3` — random per call)
- `payment` (`Payment.mp3`)
- `back_to_signup` (`Back to signup.wav`)

**Haptics:** 3× strength.

---

## 📧 EMAIL INFRASTRUCTURE — Resend

- Resend admin@qncacademy.com, domain `quantumcube.app` verified
- eu-west-1, free tier 3000/mo, 100/day
- DNS: DKIM, SPF, DMARC (p=none), MX send subdomain
- Supabase SMTP: `noreply@quantumcube.app`, `smtp.resend.com:465`, 60s min interval
- **Magic-link HTML applied Apr 29** ✓

`support@quantumcube.app` → `admin@qncacademy.com` via Cloudflare email routing. Used in all public legal pages.

**Pending:** PNG wordmark upgrade for magic-link email (post brand-folder-deployed).

---

## APP STRUCTURE — 7 FACES + INTERSTITIAL

| Face | Name | Card label | Notes |
|------|------|---|-------|
| Face 0 | Entry / Sign Up Form | — | Settings link visible here in legal footer |
| faceCheckEmail | "Check Your Email" interstitial | — | |
| Face 1 | Introduction video + Welcome greeting | **Introduction** | Welcome auto-plays first 2 entries |
| Face 2 | Results Explained videos | **Videos** | |
| Face 3 | Numerology Results | **Your Numbers** | Locked unless paid |
| Face 4 | Astrology & Horoscope | **Stars and Signs** | Locked unless paid |
| Face 5 | Combined Results | **Combination** | Locked unless paid. ONLY live TTS path |
| Face 6 | Complete / Outro video | **Complete** | |
| Face 7 | Settings | — | Sign Out, Download My Data, Delete Account, Back |

**Settings discoverability gap:** the Settings link is currently only visible from Face 0 (signup screen) via the legal footer. Once a user is signed in and using the cube, there is no obvious in-app navigation to Face 7 — they'd need to sign out first to find Settings, OR call `openFace(7)` from DevTools console. Not a Google Play violation (deletion *exists in-app*) but a real UX gap. Fix is ~30 min — add a gear ⚙️ icon visible on signed-in faces, or surface the Settings link in the legal footer of every face. Slot into Google OAuth session or post-launch.

---

## SUPABASE BACKEND

- **Project:** quantum-cube (ref `fqqdldvnxupzxvvbyvjm`)
- **Region:** Central EU (Frankfurt)
- **Schema (migrated and committed):**
  - `public.profiles` (id, email, has_paid, marketing_consent, created_at) — migration `20260417104424_create_profiles_table_and_rls.sql`
  - `public.narrate_rate_counters` + `narrate_rate_limit_try` RPC — migration `20250429140000_narrate_rate_limit.sql`
- **RLS:** Enabled. 3 profiles policies, `has_paid` locked from client via column-level `with check` clause
- **Trigger:** `on_auth_user_created` → `handle_new_user()` auto-creates profile on auth signup
- **Cascade FK:** `profiles.id` → `auth.users.id` `on delete cascade` (powers account deletion)
- **Edge Functions (deployed):** `narrate` ✓, `delete-account` ✓, `export-data` ✓
- **Pending:** `dodo-webhook` (after Dodo approval)

### Test / team data in profiles (DELETE BEFORE LAUNCH)
Snapshot from April 23 sweep. **Re-snapshot in next session** in case list has drifted:
- `admin@qncacademy.com` (team, unpaid)
- `charlheyns1@gmail.com` (unpaid)
- `booyens.michelle@gmail.com` (Michelle, unpaid)
- `keyzer@xtremeprop24.com` (Keyzer, unpaid)
- `quantumneurocreations@gmail.comcom` ← **typo, delete anytime**
- `test+chunk5b@qncacademy.com` (unpaid)
- `carlkelbrick+test@gmail.com` (unpaid)
- `rkelbrickmail@gmail.com` (unpaid)
- `carlkelbrick@gmail.com` (paywall test profile — keep until E2E payment test done)
- `quantumneurocreations@gmail.com` (paid test — keep for paywall testing)

---

## FRONTEND WIRING — KEY LINE REFS

**Numbers float — use grep, anchor by function/const name not line number.** Snapshot from Apr 29:

| What | Approx line in `docs/app.html` |
|---|---|
| const sb = window.supabase.createClient | ~499 |
| Static manifest link | ~17 |
| Apple touch icon | ~29 |
| `#faceLabelCard` HTML | ~569 |
| `.face-label-card` CSS | ~418 |
| `.export-btn` / `.delete-btn` CSS | ~289-296 |
| `updateFaceLabel` + `FACE_NAMES` + MutationObserver | ~1310+ |
| `scrollBelowCube()` | ~1300+ |
| `openFace()` (calls scrollBelowCube) | ~1290+ |
| window.haptic + QC_AUDIO init | ~1004 / ~1007 |
| `_musicTracks` array (5 entries, randomised) | ~1011 |
| `fetchNarration` (Edge Function, Face 5 only) | ~1349 |
| `startNarration` | ~1380 |
| `startNarrationFromUrl` | ~1388 |
| `playSequence` (Life Phases sequential) | ~1404 |
| `window.qcNarrateCard` (Face 3 + Face 4 dispatch) | ~1420 |
| `playWelcomeGreeting` | ~1501 |
| voiceState defaults | ~1361 |
| `showFace(n){` | ~1534 |
| `onFaceShown` (Face 1 counter-based auto-play) | ~1510 |
| NUM data | ~1550+ |
| STORE_KEY const | ~2161 |
| `async function checkStoredUnlock` | ~2165 |
| `syncUnlockFromProfile` | ~2187 |
| applyUnlockedState | ~2218 |
| handleRevealClick | ~2323 |
| signInWithOtp paths | ~2378, ~2444 |
| sb.auth.onAuthStateChange | ~2471 |
| signOut | ~2621 |
| **`function runCalculation`** | **~2745** (STABLE ANCHOR — verified Apr 29) |
| `_wipeAllLocalState` | ~2630 |
| `exportMyData` | ~2640 |
| `armDeleteAccount` | ~2680 |
| `confirmDeleteAccount` | ~2700 |
| `renderAllContent` + 4× `if(isUnlocked){}` reveal gates | ~2800+ |
| SW registration | ~2995 |

---

## 🔐 AUTH + UNLOCK FLOW

### Session handling
- `persistSession: true`, `detectSessionInUrl: true`, `flowType: "implicit"`
- Session persists in localStorage until explicit signOut
- Closing tab + reopening → auto-advances into app
- Magic-link short-circuit: if session email matches form email → skip magic link
- Mismatched email → signs out session first, fires new magic link

### Unlock state — 4-layer defence
1. **STORE_KEY user-scoped** — stores `session.user.id`
2. **checkStoredUnlock** — only applies unlocked state if stored id matches session user id
3. **syncUnlockFromProfile** — authoritative from DB. Unpaid branch unconditionally enforces locks.
4. **renderAllContent** — 4× face-reveal blocks gated on `if(isUnlocked){}`
5. **DB-level RLS** prevents user from updating own `has_paid` (in migration `20260417104424`)

`applyUnlockedState` hides .lock-screen, reveals face-content — only callable after paid confirmed.

### Account deletion (NEW Apr 29)
- Two-tap confirmation pattern (5-second arm window)
- Edge Function admin-deletes user via service-role key
- Cascade FK wipes profile row automatically
- Frontend wipes 6 localStorage keys (STORE_KEY, QC_PENDING_KEY, qc_musicIdx, qc_rotIdx, qc_greet_count, qc_greet_count_<uid>)
- `Promise.race(signOut, 3000ms)` prevents hang from post-deletion signOut
- Redirects to `/` (landing) on completion
- Verified working end-to-end Apr 29

### Data export (NEW Apr 29)
- Single-tap from Settings (Face 7)
- Returns JSON with email, has_paid, marketing_consent, timestamps
- Browser downloads as `quantum-cube-data.json`
- POPIA right of access compliance

### Known remaining UX issues (not launch-blocker)
- Sign out + sign back in as same email same device still fires magic-link. Post-launch polish.
- Settings link only visible from Face 0 footer. Need gear icon in cube UI for signed-in users.

---

## 🪨 FRAGILE AREAS — DO NOT TOUCH CASUALLY

- **Service worker is a real file** (`sw.js`). Do NOT revert to blob URL — Android Chrome 117+ rejects blob SW silently.
- **Static manifest.json is a real file** (`docs/manifest.json`). Do NOT revert to blob URL — PWABuilder cannot read blob URLs.
- **`@media (min-width:600px)` rules** are desktop-only on mobile — any CSS change inside those media queries is invisible on Ronnie's phone. Base rules apply to mobile.
- **BSD sed can't do multi-line replacements** — use Python one-shot. Never iterate.
- **`grep -c` returns exit 1 on zero matches** — kills pipelines silently. Use `|| true`.
- **`head -N` piped after `git log` can trigger SIGPIPE (exit 141)** on macOS. Use `|| true`.
- **Service worker cache bump is mandatory** every commit that changes `docs/app.html` or `docs/manifest.json`.
- **PWA cache stickiness:** "it's not working on my phone" is usually cache or SW install timing, not code. Triage in this order: (1) regular Chrome tab not PWA, (2) Force-stop PWA / Clear storage on Android, (3) Test in regular Chrome to bypass PWA, (4) Uninstall + reinstall PWA.
- **Magic-link must open in main Chrome**, not Gmail's internal browser. Session won't match otherwise.
- **Never reintroduce base64 assets** — 10.8MB cleanup reduced file from 11MB to ~349KB.
- **Life Phases is sequential playback** via `playSequence`. Do not convert to 3 separate cards without product approval.
- **Master numbers in NUM.pc are stripped** (commit `636e3d8`). Do not re-add.
- **renderAllContent reveal blocks MUST stay gated on `if(isUnlocked){}`** — removing the gate re-introduces paywall bypass.
- **GitHub Pages source is `/docs` directory.** Do NOT add HTML to repo root expecting it to be served.
- **`docs/CNAME` binds the custom domain.** Removing it breaks `quantumcube.app`.
- **Cursor's verbatim grep output can occasionally glitch.** Verify via fresh `grep` OR `git cat-file` before reverting.
- **Cursor sessions can stall mid-output when context is full.** Start fresh Cursor chat alongside fresh Claude chat for clean cross-tool sync.
- **JWTs / bearer tokens NEVER paste into Cursor or chat** — debug via DevTools console + Promise.race timeout patterns instead. Cursor's refusal on Apr 29 was correct.
- **`auth.admin.deleteUser` can hang the calling session's `signOut`** — always wrap signOut in `Promise.race(signOut, 3000ms)` when calling delete from the user's own session.
- **Edge Functions need `verify_jwt = false` in `supabase/config.toml`** if they handle JWT manually — otherwise Supabase returns 401 before the function runs.
- **Supabase Edge Functions don't expose `Deno.openKv()`.** Use Postgres RPC for state instead.

### Supabase CLI gotchas
- `supabase db execute --project-ref` does not exist. Use `supabase db query --linked "SQL"` from linked project directory.
- `supabase functions logs` requires CLI v2.95+. We have v2.90.0 — use dashboard for logs.
- For CSV output: `-o csv`, NOT `--csv`.

---

## WHAT'S LEFT — ORDERED BY PRIORITY (Apr 29 update)

### 🚨 LAUNCH-BLOCKING

1. **Dodo Payments approval** (24-72hr pending — submitted Apr 29)
2. **Cube icon design** (Canva Pro attempt, then Fiverr if needed) — single dependency for items 3 + 4
3. **Real PNG icons in manifest** (192/512/maskable) — needs #2
4. **Social media handles claimed** across 6 platforms — needs #2
5. **Google OAuth 2.0** (~2-3 hrs)
6. **Dodo wiring + 26-line MoR swap** — needs #1 first
7. **E2E payment test** → refund to self — needs #6
8. **Delete 9+ test profile rows**

### ⚠️ HIGH-VALUE (not launch-blocker)
- Settings discoverability fix (gear icon, ~30 min)
- Sentry error monitoring (~20 min)
- Email re-verification UX — same-email resubmit detection
- Magic-link email PNG wordmark upgrade

### 🧹 POST-LAUNCH CLEANUP
- Split `docs/app.html` into .js + .css files
- `git gc --aggressive` — .git folder is 1.2 GB
- Login loop fix (same-email resign triggers new magic link)
- HeyGen cleanup (Academy side)
- Fine-comb audit pass — duplicate CSS selectors, dead code
- Brain + CPU chip icon (designer)

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
- **Google Play:** $25 one-time, PWABuilder → .aab (after Dodo live + cube icon designed + account deletion ✓)
- **Apple App Store:** $99/year, Capacitor wrap, Xcode archive (DEFERRED — revisit post-Google-Play launch, tackle iOS payment politics then)

---

## INFRASTRUCTURE LIVE

| System | State |
|---|---|
| GitHub Pages | Live (source: `/docs` on `main`. SW **qc-v147**, narration **qc-narration-v2**) |
| **quantumcube.app** | **LIVE** — landing + 8 legal + /app, all HTTP 200 ✓ |
| qncacademy.com | Full email stack live |
| Google Workspace | admin@qncacademy.com + 5 aliases |
| Cloudflare Email Routing | *@quantumcube.app → admin@qncacademy.com (incl. support@) |
| Cloudflare DNS | CNAME quantumcube.app → quantumneurocreations-dot.github.io ✓ |
| Resend | Verified, SMTP in Supabase, magic-link template applied |
| ElevenLabs | Valory, narrate deployed + rate-limited, usage-based billing enabled (250k cap) |
| Supabase | Frankfurt, free tier, RLS verified, 3 Edge Functions deployed (narrate / delete-account / export-data), 2 migrations synced |
| **Dodo Payments** | **Application pending — 24-72hr review (submitted Apr 29)** |
| FastSpring | Account dormant (registered Apr 29, no products live) |
| LemonSqueezy | Application paused (SA tax form delay) |

---

## ANNUAL RUNNING COST — unchanged from v23

Same subscription footprint plus Canva Pro added Apr 29. No major changes to running costs.

---

## SEPARATE PROJECT — QNC ACADEMY (context only)

Path `/Users/qnc/Projects/qnc-academy/`. Stack: Next.js + Vercel + Supabase (Ireland, ref `bevaepokvavzmykjmhda`) + Anthropic (Claude Haiku 4.5) + ElevenLabs + GitHub. QI = Academy's branded AI (cognitive framework, sine-wave, Claude Haiku 4.5). HeyGen deprecated — Academy has its own cleanup task. **Never mix backends.**

---

## Lessons learned (running, updated Apr 29)

- **SW diagnosis via phone screenshots is a trap.** Use Cursor Browser MCP with DevTools access OR diagnose via console.log on a fresh deploy.
- **Blob-URL service workers fail silently on Android Chrome 117+.** Use real files at origin scope.
- **Cursor's verbatim grep output can occasionally glitch.** Verify via fresh `grep` OR `git cat-file` before reverting based on Cursor's reported output.
- **Cursor sessions can stall mid-output when context is full.** Start fresh Cursor chat alongside fresh Claude chat.
- **`renderAllContent` had unconditional reveal logic** that predated the April 20 paywall fixes. Lesson: when patching paywall, grep ALL call sites that touch `display='block'` on `.lock-screen` or face-content IDs.
- **Python anchor strings for multi-block replacements must account for blank lines and indentation.** Cursor's repeated self-corrections on Apr 29 caught indentation mismatches and stale anchor text. Welcome the corrections.
- **Compression risk is real at multi-hour sessions.** Respect stop signals, update brief, start fresh.
- **Every brief version must be self-contained.** No "See vN for detail" — info loss on aging. v25 violated this; v25.1 fixes.
- **Public legal pages + landing page unlock BOTH payment processor AND Google Play in one go.** Build it once, satisfy two reviewers.
- **Paddle is NOT a fit for esoteric / non-SaaS digital content.** Their AUP is restrictive. Verified directly Apr 29.
- **Dodo Payments actively markets to astrology brands.** Better category fit than the more general MoRs.
- **Cross-chat context drift is real.** When work happens across multiple Claude sessions, do an end-of-week sync check before assuming brief is current.
- **Logo wordmarks are buildable in Canva** with Cinzel + Cinzel Decorative built-in. Logo icons (cube, brain/CPU) need a real designer — AI image generators can't reliably produce specific stylised brand icons.
- **PWA cache stickiness is the #1 false alarm.** Always check live site in regular Chrome before debugging code.
- **JWTs / bearer tokens NEVER go through Cursor or chat.** Cursor's refusal Apr 29 was correct. Diagnose via DevTools console + defensive timeouts (Promise.race) instead of curl tests with real tokens.
- **`auth.admin.deleteUser` can hang the calling session's `signOut`.** Wrap signOut in Promise.race(3000ms) when calling delete from the user's own session.
- **Diagnostic console.logs are scaffolding, not production code.** Always rip them in a follow-up commit.
- **Edge Functions need `verify_jwt = false` if they handle JWT manually.** Otherwise Supabase 401s before the function runs.
- **Supabase Edge Functions don't expose `Deno.openKv()`.** Use Postgres RPC for state instead.
- **Today's wins compound: each launch-blocker shipped tightens the path to revenue.** April 29 took us from 4 hard blockers to 2 (Dodo + cube icon).

---

## NEXT SESSION STARTING POINT

1. Attach PROJECT_BRIEF.md (v25.1) + CHAT_KICKOFF.md to new chat
2. Start a fresh Cursor chat alongside (or continue current if context clean)
3. **Minimal health check:** confirm HEAD on `origin/main`, SW = qc-v147, all 4 live URLs return 200
4. **Check Dodo Payments approval status** — has Michelle heard back?
5. **If Dodo approved:** start payment integration session (webhook + launchDodo + 26-line MoR swap + E2E test)
6. **If Dodo still pending:** parallel work options:
   - Google OAuth 2.0 implementation (~2-3 hrs code)
   - Cube icon in Canva Pro (Ronnie solo, ~30 min attempt)
   - Settings discoverability fix (~30 min code)
7. Re-snapshot test profile rows in case list has drifted
8. Update brief at end of session if meaningful drift

---

**End of brief v25.1.**
