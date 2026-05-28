---
tags: [core, reference, android]
---
# Quantum Cube — Google Play Store Submission Checklist

**Last updated:** 2026-05-09
**Goal:** First-try approval. Zero rejections.
**Submission target:** Trusted Web Activity (TWA) wrapping `https://quantumcube.app` via Bubblewrap, packaged as AAB, distributed on Google Play.

**Legend:** 🔴 hard blocker (rejection if missed) · 🟡 likely-question / friction · 🟢 polish · `[ ]` not done · `[✓]` verified in repo · `[?]` needs user verification

---

## ⚠️ THE BIG RISK — Payments Policy (read first)

The Quantum Cube product is **digital content sold inside the app for $17**. Google Play Payments Policy [§2](https://support.google.com/googleplay/android-developer/answer/9858738) explicitly requires **Google Play Billing for "in-app purchases of digital content"** — defined as "items, subscription services, app functionality or content (such as ad-free version or new features not available in the free version), and cloud software."

Section 3 exemptions do not apply (we are not physical goods, physical services, regulated finance, P2P, or donations).

Section 4 explicitly **prohibits** leading users to external payment via "in-app webviews, buttons, links" — which is exactly what the Dodo Payments overlay does inside a TWA.

**Three viable paths to approval:**

| Path | Description | Effort | Verdict |
|---|---|---|---|
| **A. Implement Play Billing inside the TWA** | Detect TWA context (`document.referrer === 'android-app://...'`), use the [Digital Goods API + Payment Request API](https://developer.chrome.com/docs/android/trusted-web-activity/play-billing) to bill via Play. Continue using Dodo for web users. | Medium — 1-2 days of frontend + a `dodo-or-play` branch in unlock flow + Play Console product setup | ✅ Recommended for first-try approval |
| **B. Enroll in External Offers Program** (EEA only — does not cover US/UK/RoW) and US Alternative Billing | Eligible regions only; still pays Google 5-10% revenue share for 2 years; specific UI/disclosure rules; required enrollment + agreement. US enrollment deadline was Jan 28, 2026. | High — multi-program enrollment, geo-aware billing flow, ongoing revenue share | ❌ Not viable as the *only* path; partial coverage |
| **C. Ship as a free "viewer" app** | The Play app is free / read-only; users go to web to buy. Must not have any "buy now" CTA inside the TWA — would be flagged as deceptive cross-funneling. | Low code — just hide the unlock flow when running inside TWA | 🟡 Possible but limits monetization severely; users on Android can't buy in-app at all |

🔴 **You must pick one before submission.** Path A is the path to first-try approval if monetization-on-Android matters. Treat this as the gating decision for the whole TWA project — not a polish item.

**Sources:**
- [Payments policy (Section 2 mandates Play Billing)](https://support.google.com/googleplay/android-developer/answer/9858738)
- [Use Play Billing in your TWA (Chrome dev docs)](https://developer.chrome.com/docs/android/trusted-web-activity/play-billing)
- [External Offers Program — EEA](https://support.google.com/googleplay/android-developer/answer/14372887)
- [User Choice Billing pilot](https://support.google.com/googleplay/android-developer/answer/12570971)

---

## 1. Developer Account Readiness

| | Item | Notes |
|---|---|---|
| 🔴 [?] | Personal Google Play developer account active and $25 fee paid | Verify in Play Console |
| 🔴 [?] | Identity verification complete (legal name, address, email, phone — government ID may be requested) | [Verify your developer identity](https://support.google.com/googleplay/android-developer/answer/10841920) |
| 🔴 [?] | Device verification done via Play Console mobile app on a real Android device | [Device verification for new accounts](https://support.google.com/googleplay/android-developer/answer/14316361) |
| 🔴 [?] | If account created **after Nov 13, 2023**: closed test of ≥12 testers, opted in for ≥14 consecutive days, completed before requesting production access | [Closed testing requirement](https://support.google.com/googleplay/android-developer/answer/14151465) — biggest single calendar item, plan accordingly |
| 🟡 [?] | Production access request submitted via Play Console Dashboard | Required for first app on personal account, separate from app review |
| 🟢 [?] | Contact information current (legal entity, support email, phone, physical address — required to be public on store listing) | [Contact info requirements](https://support.google.com/googleplay/android-developer/answer/10840893) |

**Critical timeline note:** The 14-day closed-testing window is the single longest fixed-time gate. If the account was created after Nov 13, 2023 and you haven't started the closed test, **you cannot submit to production for at least 14 days from the day you enroll your 12th tester**.

---

## 2. Target API + Build

| | Item | Notes |
|---|---|---|
| 🔴 [ ] | App targets **API level 35 (Android 15) minimum** today | [Target API requirements](https://developer.android.com/google/play/requirements/target-sdk) |
| 🟡 [ ] | Plan to bump to **API level 36 (Android 16)** before **Aug 31, 2026** | New apps and updates submitted after that date must target 36 |
| 🔴 [ ] | Bubblewrap CLI installed (latest from `@bubblewrap/cli` on npm), JDK + Android SDK present | [Bubblewrap repo](https://github.com/GoogleChromeLabs/bubblewrap) |
| 🔴 [ ] | Built as **AAB (Android App Bundle)**, not APK — Play has required AAB for new apps since Aug 2021 | `bubblewrap build` produces both; upload the `.aab` |
| 🔴 [ ] | App signed with a real production keystore (NOT the Bubblewrap-generated debug key) | Generate via `keytool -genkey -v -keystore quantumcube.keystore -alias quantumcube -keyalg RSA -keysize 2048 -validity 10000` |
| 🔴 [ ] | Keystore backed up in **multiple secure locations** (Apple Passwords + 1Password + offline backup) | Lose this and you can never update the app again |
| 🔴 [ ] | Play App Signing **enabled** (Google manages the upload key, you keep the original; recommended) | [Play App Signing](https://support.google.com/googleplay/android-developer/answer/9842756) |

---

## 3. Digital Asset Links (TWA verification)

| | Item | Notes |
|---|---|---|
| 🔴 [ ] | `assetlinks.json` at `https://quantumcube.app/.well-known/assetlinks.json` returns 200 with `Content-Type: application/json` | Currently 200 with placeholder values |
| 🔴 [ ] | `package_name` in assetlinks.json **matches** the Bubblewrap-generated Android package name | Currently placeholder: `app.quantumcube.twa` — confirm or change before signing |
| 🔴 [ ] | `sha256_cert_fingerprints` array contains the **exact SHA-256 of your production signing key** (from `keytool -list -v -keystore`) | Currently `REPLACE_WITH_KEYSTORE_SHA256_FINGERPRINT` |
| 🔴 [ ] | If Play App Signing is enabled, also include the **Google-managed upload key SHA-256** in the same array (Play Console → App signing → both fingerprints) | TWA verification fails if either is missing |
| 🔴 [ ] | Verified live via [Statement List Tester](https://developers.google.com/digital-asset-links/tools/generator) before submission | One-click verifier; must pass green |
| 🟢 [ ] | `assetlinks.json` cache headers allow updates within ~24h | Cloudflare default is fine |

**Source:** [Digital Asset Links getting started](https://developers.google.com/digital-asset-links/v1/getting-started)

---

## 4. Manifest.json (PWA → TWA prep)

Current `docs/manifest.json` reviewed. Status:

| | Item | Status |
|---|---|---|
| 🔴 [✓] | `name`, `short_name`, `id`, `start_url`, `scope` all present | ✓ |
| 🔴 [✓] | `display: "standalone"` (TWA requirement; `"browser"` would block) | ✓ |
| 🔴 [✓] | `theme_color` and `background_color` set (Play uses these for splash) | ✓ #05050f |
| 🔴 [✓] | 192×192 and 512×512 PNG icons present | ✓ |
| 🔴 [✓] | 512×512 maskable icon present (`purpose: "maskable"`) | ✓ |
| 🟡 [ ] | **Add 192×192 maskable variant** — Android home-screen icon quality is better with both sizes | Currently only 512 maskable |
| 🟡 [ ] | **Add `screenshots` array to manifest** with 1-8 entries (helps TWA + PWA install prompts on Chrome desktop too) | Missing |
| 🟢 [✓] | `categories: ["lifestyle", "entertainment"]` set | ✓ — note: should NOT be miscategorized as "medical" or "health" |
| 🟢 [✓] | `description` field present | ✓ |

---

## 5. Store Listing Assets (per [Play Console asset specs](https://support.google.com/googleplay/android-developer/answer/9866151))

| | Asset | Spec | Status |
|---|---|---|---|
| 🔴 [ ] | High-res app icon | 512 × 512 PNG, 32-bit (with alpha), max 1 MB | Have `qc-icon-512.png` — verify it's the right one and has no transparency issues at the edges |
| 🔴 [ ] | Feature graphic | **1024 × 500** PNG/JPG, max 1 MB, no alpha | **Missing — must create** |
| 🔴 [ ] | Phone screenshots | Min 2, max 8. 16:9 or 9:16. JPEG or 24-bit PNG. 320–3840 px on the long side. | **Missing — must create** |
| 🟡 [ ] | 7-inch tablet screenshots | Min 1, max 8 | Optional but improves listing |
| 🟡 [ ] | 10-inch tablet screenshots | Min 1, max 8 | Optional but improves listing |
| 🟢 [ ] | Promo video (YouTube URL) | 30 sec recommended | Optional |
| 🔴 [ ] | App title | ≤ **30 chars** (was 50; tightened in 2021) | "Quantum Cube" = 12 ✓ |
| 🔴 [ ] | Short description | ≤ **80 chars** | Need to draft |
| 🔴 [ ] | Full description | ≤ **4000 chars**, no all-caps, no excessive emojis, no "free" / "best" / "top" filler | Need to draft |

---

## 6. Privacy Policy + Data Safety Form (highest-friction non-payment area)

### 6a. Privacy policy

| | Item | Notes |
|---|---|---|
| 🔴 [?] | Public URL hosting a privacy policy (e.g., `https://quantumcube.app/privacy.html`) | **Verify this exists and is current** |
| 🔴 [ ] | Policy explicitly names **every data collector** in the stack: **Supabase** (auth, account info), **Dodo Payments** (purchase metadata), **PostHog** (product analytics, EU), **Sentry** (error monitoring, EU), **Microsoft Clarity** (session replay) | Each must be listed by name with a link to their privacy policy |
| 🔴 [ ] | States data retention period, deletion mechanism, and right-to-be-forgotten contact | We have `delete-account` Edge Function — link it from policy |
| 🔴 [ ] | Lists **all data types** collected (email, IP, device info, app interactions, purchase history) | Must match Data Safety form exactly — discrepancies are a top rejection reason |
| 🟡 [ ] | Effective date and last-updated date on the page | Required by GDPR + Play |
| 🟡 [ ] | Contact email (must work) | `admin@qncacademy.com` already configured |
| 🟢 [ ] | Multi-language? | Optional but recommended for global reach |

### 6b. Data Safety form (in Play Console — declares to users what you collect)

[Source: Data Safety form requirements](https://support.google.com/googleplay/android-developer/answer/10787469) — Google explicitly requires you to declare **third-party SDK data collection**, not just first-party.

| | Declaration | Recommended answer for Quantum Cube |
|---|---|---|
| 🔴 [ ] | **Personal info → Email address** | Collected (Supabase magic-link auth). Required. Encrypted in transit. User can delete. |
| 🔴 [ ] | **Personal info → Name** | Collected (full birth name from form input — used for numerology calculation). Required. Encrypted in transit. User can delete. |
| 🔴 [ ] | **Personal info → Other info → DOB** | Collected (used for chart calculations). Required. Encrypted in transit. User can delete. |
| 🔴 [ ] | **Financial info → Purchase history** | Collected via Dodo Payments. Required. Encrypted in transit. User can delete. |
| 🔴 [ ] | **App activity → App interactions** | Collected via PostHog + Microsoft Clarity. Required. Encrypted in transit. User can delete. |
| 🔴 [ ] | **App info & performance → Crash logs / Diagnostics** | Collected via Sentry. Required. Encrypted in transit. User can delete. |
| 🔴 [ ] | **Device or other IDs** | Collected (PostHog distinct ID, Sentry session ID). Required. Encrypted in transit. User can delete. |
| 🔴 [ ] | **Security practices → Encrypted in transit** | YES (HTTPS everywhere) |
| 🔴 [ ] | **Security practices → User can request deletion** | YES (`delete-account` Edge Function + in-app settings) |
| 🟡 [ ] | **Data shared with third parties** | Yes — declare each SDK that **transmits data off-device** (PostHog, Sentry, Clarity, Supabase, Dodo). Specify purpose. |

**Trap to avoid:** the form auto-flags if your declared collection types don't match the SDKs Google detects in your AAB. PostHog, Sentry, and Clarity will all be detected. Declare them. Do not check "no data collected".

---

## 7. App Content Declarations (Play Console → Policy → App content)

| | Section | Action |
|---|---|---|
| 🔴 [ ] | **Privacy policy URL** | Paste the public URL from §6a |
| 🔴 [ ] | **App access** | "All functionality is available without special access" if free tier works without login. If purchase is required to see anything, provide test credentials for Google review team. |
| 🔴 [ ] | **Ads** | "No, my app does not contain ads" (assuming we don't add Google AdSense / AdMob) |
| 🔴 [ ] | **Content rating** (IARC questionnaire) | Astrology/numerology likely → **Everyone / Everyone 10+** depending on whether romantic-relationship narration is rated mild |
| 🔴 [ ] | **Target audience and content** | Adults (18+) recommended — keeps you out of [Families Policy](https://support.google.com/googleplay/android-developer/answer/9893335) which has stricter rules |
| 🔴 [ ] | **News app declaration** | NO |
| 🔴 [ ] | **COVID-19 contact tracing** | NO |
| 🔴 [ ] | **Data safety** | Linked from §6b |
| 🔴 [ ] | **Government apps** | NO |
| 🔴 [ ] | **Financial features** | NO (not a finance app, even though we collect payment) |
| 🔴 [ ] | **Health content** | NO — and **explicitly avoid health/medical claims** in store listing or in-app copy. Numerology/astrology are entertainment. |
| 🟡 [ ] | **AI-generated content** declaration | YES — narration is AI-generated (ElevenLabs Valory). Disclose this somewhere in the listing (Play started enforcing AI disclosures in 2024). |

---

## 8. Deceptive Behavior Compliance (astrology = entertainment)

[Source: Deceptive Behavior policy](https://support.google.com/googleplay/android-developer/answer/9888077)

| | Item | Notes |
|---|---|---|
| 🔴 [ ] | App description **explicitly frames numerology + astrology as entertainment**, not factual prediction | Required to avoid "impossible functionality" rejection — same bucket as fortune-telling, palm reading, etc. |
| 🔴 [ ] | In-app disclaimer visible (e.g., footer or onboarding screen): "For entertainment purposes only" or similar | Add to app.html if not present |
| 🔴 [ ] | No claims of medical, psychological, or financial benefit | Currently clean — verify all marketing copy + Face 5 narration doesn't slip |
| 🔴 [ ] | App description matches actual functionality (no overpromising features) | Do a copy-vs-app audit before submission |
| 🟢 [ ] | Marketing pages (landing, terms, FAQ) consistent with the in-app entertainment framing | We control quantumcube.app — easy to align |

---

## 9. Pre-launch Report (automated tests, runs on every internal-track upload)

| | Item | Notes |
|---|---|---|
| 🔴 [ ] | App launches on stock Android emulators without crashes | Pre-launch report runs on real devices in Google's farm |
| 🔴 [ ] | No accessibility blockers (large tap targets, contrast, screen-reader labels) | We've done two a11y audits already — should pass |
| 🔴 [ ] | No security warnings (cleartext traffic, exposed secrets, vulnerable libs) | TWA is HTTPS-only — should pass |
| 🟡 [ ] | Performance acceptable (no ANRs, no excessive memory) | TWA is just a Chrome instance — bottleneck is the web app, which is fine |
| 🟢 [ ] | Pre-launch warnings reviewed and addressed before promoting from internal/closed to production | Soft block; only critical issues stop publication |

---

## 10. Existing Quantum Cube Repo Items Already in Place

| | Item | Notes |
|---|---|---|
| 🟢 [✓] | `manifest.json` with `id`, `start_url`, `scope`, `display`, theme/bg colors, 192/512 icons + 512 maskable | `docs/manifest.json` |
| 🟢 [✓] | `assetlinks.json` placeholder at `/.well-known/` | Needs real values pre-build |
| 🟢 [✓] | Service worker registered, HTTPS via GitHub Pages + Cloudflare DNS | qc-v224 |
| 🟢 [✓] | In-app account deletion (Edge Function `delete-account`) | Required for Play since 2024 |
| 🟢 [✓] | In-app data export (Edge Function `export-data`) | GDPR/POPIA helper |
| 🟢 [✓] | Sentry error monitoring (so pre-launch crashes are visible to us before Google flags them) | Live |
| 🟢 [✓] | Privacy/Terms/Disclaimer in-app modals | Linked from app.html footer |

---

## 11. Submission Sequence (recommended order)

1. **Decide payment path** (A / B / C from the top of this doc) — **this is the gate; do not start anything else until decided**
2. **If Path A (Play Billing inside TWA):** wire Digital Goods API + Payment Request API; create `quantum_cube_unlock` managed product in Play Console at $17 USD; test in internal track
3. **Generate production keystore** + back up immediately; compute SHA-256
4. **Update `assetlinks.json`** with real `package_name` + SHA-256(s); deploy; verify with [statement list tester](https://developers.google.com/digital-asset-links/tools/generator)
5. **Build AAB** via Bubblewrap targeting API 35+; sign with production key
6. **Upload to Internal Testing track** in Play Console; run pre-launch report; fix any flagged issues
7. **Create store listing**: title, short/full description, screenshots, feature graphic, icon
8. **Complete Data Safety form** (match privacy policy exactly)
9. **Complete App Content declarations** (rating, target audience, ads, financial, etc.)
10. **Promote internal track build to closed test track**; enroll 12+ testers (friends + community); wait the 14-consecutive-day window if account is post-Nov-2023
11. **Request production access** (personal account — separate from app review)
12. **Promote to production**; submission goes to review (typical: 1-7 days for first apps, longer if anything triggers manual review)

---

## 12. Red-Flag Items We Are Most Likely to Get Rejected For (ordered by probability)

1. **Payments policy violation** — selling digital content via Dodo overlay inside the TWA. **MUST be addressed pre-submission.** (See §0.)
2. **Data Safety form mismatch** — declared types don't match the SDKs Google scans in the AAB. Mitigation: be exhaustive in declarations.
3. **Privacy policy doesn't list all SDKs by name** — top reason for "Privacy violation" rejection. Mitigation: name PostHog, Sentry, Clarity, Supabase, Dodo individually.
4. **assetlinks.json fingerprint mismatch** — TWA fails verification, app shows browser URL bar (auto-rejection on TWA listing). Mitigation: include both upload + Play-managed signing keys.
5. **Astrology framed as factual prediction** in store description or in-app — "impossible functionality". Mitigation: entertainment framing throughout.
6. **Closed-testing requirement not satisfied** for personal accounts created after Nov 13, 2023 — production access denied silently. Mitigation: start the 14-day clock NOW if applicable.
7. **AI-generated content not disclosed** — silent flag, can trigger manual review. Mitigation: tick the AI box in App Content.
8. **Health/medical claims** in marketing copy — cosmic profile readings often slip into "wellness" language. Mitigation: copy audit pre-submission.

---

## Sources Cited

- [Target API level requirements (Android Developers)](https://developer.android.com/google/play/requirements/target-sdk)
- [Closed testing requirements (Play Console Help)](https://support.google.com/googleplay/android-developer/answer/14151465)
- [Payments policy (Play Console Help)](https://support.google.com/googleplay/android-developer/answer/9858738)
- [Deceptive Behavior policy (Play Console Help)](https://support.google.com/googleplay/android-developer/answer/9888077)
- [Data Safety form (Play Console Help)](https://support.google.com/googleplay/android-developer/answer/10787469)
- [Use Play Billing in your TWA (Chrome dev docs)](https://developer.chrome.com/docs/android/trusted-web-activity/play-billing)
- [Digital Asset Links — getting started (Google Developers)](https://developers.google.com/digital-asset-links/v1/getting-started)
- [Verify your developer identity (Play Console Help)](https://support.google.com/googleplay/android-developer/answer/10841920)
- [Device verification for new accounts (Play Console Help)](https://support.google.com/googleplay/android-developer/answer/14316361)
- [External Offers Program — EEA (Play Console Help)](https://support.google.com/googleplay/android-developer/answer/14372887)
- [User Choice Billing pilot (Play Console Help)](https://support.google.com/googleplay/android-developer/answer/12570971)
- [Bubblewrap CLI (GoogleChromeLabs)](https://github.com/GoogleChromeLabs/bubblewrap)
- [Trusted Web Activities Quick Start Guide (Android Developers)](https://developer.android.com/develop/ui/views/layout/webapps/guide-trusted-web-activities-version2)
- [Statement List Tester (verify assetlinks.json)](https://developers.google.com/digital-asset-links/tools/generator)
- [Play App Signing (Play Console Help)](https://support.google.com/googleplay/android-developer/answer/9842756)
- [Families Policy (Play Console Help)](https://support.google.com/googleplay/android-developer/answer/9893335)
- [Play Console asset specs (icon, screenshots, feature graphic)](https://support.google.com/googleplay/android-developer/answer/9866151)

---
**Sub-topics:** [[data-safety-form]] · [[content-rating]] · [[store-listing]] · [[screenshots-prep]] · [[feature-graphic]] · [[closed-testing-track]] · [[production-rollout]] · [[app-review-checklist]] · [[target-audience]] · [[app-category]] · [[twa-asset-links]] · [[aab-upload]] · [[identity-verification]] · [[android]] · [[PROJECT_BRIEF]]

---

## 13. Recent Policy Updates — May 2026 Audit

Checked against all Play Policy Center categories May 10, 2026. Three additions:

### 13a. Health Apps Declaration Form (ALL developers must complete)
🔴 [ ] Even non-health apps must complete the Health Apps declaration on App content page in Play Console. Declare "This app does not provide health or medical functionality." Required field — don't skip it.

### 13b. AI-Generated Content Disclosure
🔴 [ ] Google started enforcing AI-generated content disclosures in 2024. ElevenLabs narration = AI-generated audio. Must tick the AI-generated content declaration in App Content page in Play Console. Missing this = silent flag during review.

### 13c. External Content Links Program (payments-relevant)
🟡 [ ] The deadline to enroll in Google's External Content Links Program was January 28, 2026. If we go Path C (free viewer, link to web for payment), we need to verify whether our specific use case (linking OUT of app to website, not inside TWA) is covered under the post-deadline rules. May require enrollment or may be exempt as a TWA. **Confirm before choosing Path C.**

### 13d. Android ID No Longer a Persistent Identifier (April 2025)
🟢 [ ] Android ID is no longer treated as a persistent device identifier per Google policy from April 2025. PostHog SDK v3+ handles this correctly. Verify our PostHog SDK version in app.html is current — if it is, no action needed.

### Everything Else — CLEAN ✅
Restricted Content, IP, Impersonation, Malware, MUS, Families, Store Listing, Spam/UX — all verified clean against current policy. No additional gaps found.

---

## 14. Play Console Tools — Pre-Launch Checklist

### 14a. Deep Link Verification (Play Console tool)
🔴 [ ] After uploading AAB to internal track → Play Console → Android Vitals → Deep links → run verification. Separate from assetlinks.json check. Takes 2 minutes. Must pass green before promoting to closed test.

### 14b. Crash Stack Trace Deobfuscation
🟡 [ ] Upload ProGuard/R8 mapping file to Play Console so Google's own crash reporter shows readable stack traces (separate from Sentry). TWA may not generate a mapping file — check after AAB build. If no mapping file exists, skip this step.

---

## 15. Claude Code Policy Audit — May 10, 2026

Full crawl of Google Play Policy Center completed by Claude Code (3 parallel agents, 195 tool uses). New findings below.

### 15a. External Content Links Program — ENROLL BEFORE SUBMISSION
🔴 [ ] Enroll in Play Console → Settings → External content links BEFORE using external payment redirect.
- Jan 28 2026 deadline was for EXISTING apps already using external links. New apps must enroll prior to going live — not past the deadline.
- Integrate Google's external content links API in IS_TWA unlock flow so Google's own info screen renders before redirect fires.
- Currently $0 fees. Future fee structure ~20% (subject to ongoing Epic v Google proceedings).
- Source: https://support.google.com/googleplay/android-developer/answer/16470497

### 15b. Pre-Redirect Disclosure — CODE CHANGE NEEDED
🔴 [ ] Add disclosure modal/screen before IS_TWA unlock redirect fires. Must show: "You'll be taken to your browser to complete this purchase outside Google Play. Refunds handled by Dodo Payments." Required by External Content Links Program terms.

### 15c. Public Account-Deletion URL
🔴 [ ] Add static page at `quantumcube.app/account/delete` (or similar) documenting the in-app deletion process. Play Console Data Safety form requires a public web URL in addition to in-app deletion. Quick new HTML page.

### 15d. USPTO Trademark Clearance
🟡 [ ] Run "Quantum Cube" on TESS at tmsearch.uspto.gov — check Class 9 (software) and Class 41 (entertainment/education). Quick check before submission. No direct conflicts found via web search but TESS is the authoritative source.

### 15e. Prominent In-Flow Privacy Disclosure
🟡 [ ] Add visible privacy disclosure before first DOB/email entry on Face 0 — not buried in footer. Common rejection trigger. E.g. small line: "Your data is used only for your personal reading. See our Privacy Policy." with a link.

### 15f. ElevenLabs Commercial License
🟡 [ ] Confirm current ElevenLabs tier explicitly permits distribution in paid apps. Check ElevenLabs dashboard → plan details.

### 15g. AI-Generated Content Declaration — DECISION: Declare NO
🟡 [ ] Recommend Path A: declare NO in App Content. ElevenLabs TTS of pre-written deterministic scripts = TTS productivity feature, not runtime AI generation. Document rationale. Avoids needing "Report content" link.
- If declaring YES: must add "Report content" link in legal footer (mailto:support@quantumcube.app?subject=Report%20content)

### 15h. Review Gmail Account for Play Store Reviewers
🟢 [✓] **DONE.** `qnc.review@gmail.com` created, `has_paid=true` set in Supabase (2026-05-12). OTP auth (NOT magic link).

**Credentials to enter in Play Console → App content → App access:**
- Email: `qnc.review@gmail.com`
- Password: Ronnie's Gmail password
- Instructions: "Enter email, tap Continue, check Gmail for 6-digit OTP (check spam), enter in app. Account pre-unlocked — enter any name and date of birth when prompted, then tap Reveal My Cube to explore all 4 reading faces."

**Note on profile lock (qc-v332, live):** The reviewer's first-entered name/DOB will be saved to the account. An "Edit Details" button appears if they want to change it — it shows a confirmation dialog before unlocking the form. This is expected behaviour, not a bug.

### Confirmed PASS from audit
- Ads policy ✅ (no ads, no AAID)
- Permissions ✅ (INTERNET only — no SMS/Location/Camera — no Permissions Declaration Form needed)
- Restricted Content ✅ (astrology/numerology not in restricted list)
- Real-Money Gambling ✅ (no prize element)
- Financial Services ✅
- Health Content ✅ (just need declaration form in Console)
- User Generated Content ✅ (none)
- Children/Families ✅ (18+, out of scope)
- Spam/Webview wrapping ✅ (owned site + Digital Asset Links = supported TWA path)
- Minimum Functionality ✅
- Mobile Unwanted Software ✅
- Deceptive Behavior ✅ (entertainment disclaimer in place)
- SDKs ✅ (PostHog, Sentry, Supabase, Dodo, ElevenLabs all clean)
- Target SDK 35 ✅
- Account deletion + data export ✅
- Cube visual ✅ (face labels, not Rubik's Cube coloured grid — no Spin Master IP conflict)
- Subscriptions ✅ (one-time purchase, not subscription)
