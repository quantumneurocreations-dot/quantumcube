---
tags: [core, session]
---
# Session Log

## 2026-05-14 Night — Full Play Console audit + auth rebuild wrap-up (v283–v299)

**Goal:** Complete Play Console audit, ensure everything is in order for 14-day testing window, fix all outstanding UI/UX issues flagged by testers.

**Done — Code (v283–v299):**
- ✅ **v283** — OTP flow fully restored: email field back on face0, `signInWithOtp` (no redirect), `_qcOtpVerify` saves profile via direct REST PATCH (bypasses JS client deadlock), `qc_otp_email` stored in localStorage before OTP screen, ~250 lines of magic-link dead code removed
- ✅ **v284** — OTP UI: 3+3 box layout, email truncation, paste support (`distributePaste` helper)
- ✅ **v285** — Music: silent on face0 and faceOtpEntry, stops on `visibilitychange`
- ✅ **v286** — Google GSI One Tap added: `signInWithIdToken`, `_qcGsiInProgress` flag, hash recovery IIFE
- ✅ **v287** — GSI post-login face0 bounce fixed: always calls `runCalculation()` after GSI regardless of DOB state
- ✅ **v288** — Back to Sign Up: ALL paths (face0/faceOtpEntry/face1) call `handleBackToSignUp()` → `signOut()` + clear all keys + reset form
- ✅ **v289** — Sentry `beforeSend`: OTP rate-limit errors and `AuthRetryableFetchError` dropped; alert throttle 5min → 60min
- ✅ **v290** — OTP paste improved: `type="tel"`, input event multi-char detection; GSI DOB always calls `runCalculation()`
- ✅ **v291** — face1 Back to Sign Up unified. GSI DOB simplified: always `runCalculation()`, fallback `showFace(1)` if DOB missing
- ✅ **v292** — CRITICAL: `_qcOtpVerify` 15s `Promise.race` timeout, `resetVerifyUI(msg)` on any error, "Code expired — tap Resend" message, Sentry breadcrumbs at every verify step
- ✅ **v293** — Google Sign-In STRIPPED ENTIRELY: removed all GSI code, script tag, CSP entries for `accounts.google.com`
- ✅ **v294** — Play Store reviewer bypass: `?review=qncreview2026` triggers `_qcReviewMode=true`, skips auth, full paid access auto-granted. DB: `qnc.review@gmail.com` DOB set to 1990-01-15
- ✅ **v295** — DOB date validation: impossible dates blocked (dynamic max day per month, leap year handling, form submit guard)
- ✅ **v296** — OTP autofill: single hidden input (`autocomplete="one-time-code"`, `type="tel"`, `maxlength="6"`) overlaid on 6 visual display divs. Standard Stripe/WhatsApp pattern
- ✅ **v297** — Button glass: `.calc-btn` and `.reset-btn` get `background: rgba(4,15,30,0.55)` + `backdrop-filter: blur(12px)` for text legibility
- ✅ **v298** — Button glass matched to glass-card: switched to `var(--glass)` + `backdrop-filter: blur(16px)`. OTP boxes also use `var(--glass)` + `var(--border)`. Consistent glass language throughout
- ✅ **v299** — OTP screen: "Back to\nSign Up" → single-line "Back to Sign Up" (`white-space: nowrap`), `padding-bottom: 32px` added to OTP container

**Done — Play Console audit (comprehensive):**
- ✅ **Policy status** — No issues found
- ✅ **App content** — 0 items needing attention; all 10 declarations complete (Content ratings, App access, Advertising ID, Data safety, Target audience, Privacy policy, Financial features, Health apps, Government apps, Ads)
- ✅ **App Access updated** — Instruction renamed from "Google Sign-In" to "Reviewer Access". Instructions now explain OTP is normal auth method + provide bypass URL: *"Note: Normal sign-up requires a 6-digit OTP sent to the user's email. For review, use this bypass URL instead — no OTP or sign-in needed: Open https://quantumcube.app/app?review=qncreview2026 in Chrome. Full paid access is granted automatically."* Username: `qnc.review@gmail.com`, Password: `QNC@Reviewer2026!`
- ✅ **Data Safety updated** — OAuth checkbox UNCHECKED (Google sign-in removed in v293). Only "Username and other authentication" (OTP) remains. Saved and submitted for review
- ✅ **Store listing** — Live: name, short description (71/80), full description (859/4000), icon, feature graphic, 6 phone screenshots, 5 tablet screenshots
- ✅ **Store settings** — Category: Lifestyle, Tags: Horoscope + Self-help, Email: support@quantumcube.app, Website: https://quantumcube.app, External marketing: ON
- ✅ **App Integrity** — Automatic protection: ON, App signing: Google Play, Play Integrity API: not started (post-launch task)
- ✅ **Closed testing — Alpha** — Active, 2 releases, last updated 12 May 2026
- ✅ **Expert Approved** — Not eligible (18+ app) — correct, no action needed
- ✅ **Publishing overview** — Changes sent for review (App Access + Data Safety)
- ✅ **Inline installations** — Leave unchecked (not applicable for QC TWA)

**Done — DB verification:**
- ✅ `madjadex@gmail.com` (Jade Crystal) confirmed went through full OTP flow correctly — `confirmed_at` set, 3-minute gap between create and last sign-in = normal OTP check time

**Decisions:**
- 🔵 **DEFERRED: Play Integrity API** — prevents cracked APK sideloads bypassing `has_paid`. Free up to 10K calls/month. One Claude Code session post-launch. Can only be properly tested after production release
- 🔵 **DEFERRED: Huawei AppGallery** — 400M+ active users, 3rd largest store globally. Huawei phones (post-2019) have no Google Play access. Honor phones are fine (full GMS since 2021). AppGallery submission is simple: register HUAWEI ID, upload existing APK, fill store details (same assets as Play Store). Half-day task post-launch
- 🔵 **DEFERRED: OTP autofill (`autocomplete="one-time-code"`)** — code is in place (v296) but autofill suggestion not appearing on user's Samsung device. May be Samsung keyboard limitation or TWA context. Needs investigation next session

**Critical dates:**
- May 14 = Day 1 (14-day testing clock started)
- May 27 = Day 14 → APPLY FOR PRODUCTION
- May 28 = Expected approval = birthday 🎂

**Current HEAD:** `5f0e75e` | **SW:** qc-v299 | **APP:** qc-v299 ✅ in sync


## 2026-05-11 Morning/Afternoon — Google Play Console setup (Chat Claude)

**Goal:** Create app in Play Console, upload AAB, work through all store listing requirements.

**Done:**
- ✅ **assetlinks.json updated** — Play App Signing SHA-256 added (`9D:72:AD:7C:6D:00:BE:62:F2:F4:F6:21:F3:72:53:A8:C5:95:85:D4:41:DC:D4:67:81:47:AD:3B:3E:B4:C0:17`). Both fingerprints now in file. Commit `b44ecaa`. TWA verification will work correctly.
- ✅ **App created in Play Console** — App ID `4973211872239545786`, package `app.quantumcube.twa`, Free, en-US
- ✅ **AAB uploaded** — `app-release-bundle.aab` (1.66MB), Version 2(y), Target SDK 35, API 21+, uploaded to Closed testing - Alpha track
- ✅ **Financial features** — declared "no financial features"
- ✅ **Privacy policy** — `https://quantumcube.app/privacy` submitted
- ✅ **App access** — "restricted", temp credentials: `quantumneurocreations@gmail.com`, magic link instructions added
- ✅ **Content rating** — IARC questionnaire completed: All other app types, online content Yes, no violence/sexuality/language, purchase digital goods Yes (no loot boxes), 18+ only, minor restriction enabled
- ✅ **Target audience** — 18+ selected, minor restriction ticked
- ✅ **Data safety** — fully completed: Name/Email/UserIDs/Purchase history/App interactions/Crash logs/Diagnostics/Device IDs all declared with correct collection/sharing/purpose answers. Delete account URL: `https://quantumcube.app/account/delete`
- ✅ **App category** — Lifestyle, tags: Horoscope + Self-help
- ✅ **Store listing contact** — support@quantumcube.app, https://quantumcube.app
- ✅ **External marketing** — ON
- ✅ **Store listing descriptions** — short (≤80 chars) + full (≤4000 chars) drafted and entered
- ✅ **App icon** — `docs/qc-icon-512.png` uploaded
- ✅ **Feature graphic** — designed in Claude + Canva (star background, QUANTUM white + CUBE cyan, phone mockups with app screenshots). Uploaded 1024×500.
- ✅ **Phone screenshots** — 6 portrait screenshots taken and uploaded
- ✅ **Tablet screenshots** — in progress (APK sideloaded on tablet, Play Protect warning = expected, tap Install anyway)

**Still pending (Play Console):**
- 🔲 Tablet screenshots (7-inch + 10-inch) — sideload APK, take screenshots
- 🔲 Ads declaration
- 🔲 Government apps declaration
- 🔲 Health declaration
- 🔲 Re-upload AAB and submit closed testing release (was blocked by errors — all now cleared except store listing)
- 🔲 Select countries (United States)
- 🔲 Add 12 testers → 14-day clock starts
- 🔲 Create dedicated reviewer Gmail → sign in once → Claude sets has_paid=true → update App access credentials
- 🔲 Enroll External Content Links Program (Play Console → Settings)
- 🔲 Supabase Pro upgrade ($25/mo)

**Code fixes needed (new chat):**
- 🔲 Video spacing issues on phone
- 🔲 "Reveal My Cube" button spacing issue
- 🔲 Email page buttons (Continue/Google) shift left on larger screens — need centering fix

**Current HEAD:** `b44ecaa` | **SW:** qc-v227 | **Sentry:** quantum-cube@qc-v227

---

## 2026-05-10 Night — Play Store final pre-Monday checks (Chat Claude)

**Goal:** Audit all remaining Play Store requirements, ship outstanding code items, lock in the payment path decision.

**Done:**
- ✅ **Entertainment disclaimer confirmed already shipped** — CSS `::before` pseudo-element on every `.legal-footer` and `#legalFooter` reads "For entertainment purposes only" in small uppercase Cinzel. Added in `ca863c2`. No action needed.
- ✅ **PostHog SDK confirmed v3+** — self-loading CDN snippet always loads latest; Android ID policy (April 2025) handled correctly. No action needed.
- ✅ **192×192 maskable icon created + committed** — `docs/qc-icon-192-maskable.png` generated from 512 maskable (17KB), added to `docs/manifest.json` icons array. Committed in `ca863c2` alongside SW bump qc-v225 → **qc-v226**. Pushed.
- ✅ **Delete account requirement confirmed covered** — `delete-account` Edge Function live since May 4, accessible from Face 7 (Settings). Required by Play since 2024. Already in PLAY_STORE_PREP.md Section 10 with ✓.
- ✅ **Comprehensive Play Store gap audit completed** — full list of remaining items catalogued (see NEXT-CHAT LEAD-IN).

**🔴 CRITICAL DECISION — PAYMENT PATH (do not lose this):**
- **Decision: US-only launch, Dodo Payments on Android, no Google Play Billing.**
- **Legal basis:** Epic Games vs Google court ruling — US court ordered Google to allow third-party payment processors in the Play Store for US users. This is the legitimate path; no Play Billing required for US launch.
- **Play Console fee confirmation:** "Quantum Neuro Creations" account group enrolled at **15% service fee** (standard reduced rate for first $1M/year in earnings — applies to all small developers since 2021). Screenshot saved.
- **Current code state:** Commit `0cd3f9c` has IS_TWA detection that redirects Android unlock to `window.open('https://quantumcube.app/app?ref=android-unlock')`. This works as a fallback but **needs review Monday**: if Dodo overlay renders cleanly inside a TWA Chrome instance, we can show it directly instead of redirecting to the browser — better UX. If not, the redirect stays.
- **Do NOT touch payments code until Monday UX test on device.**

**Current HEAD:** `3049a13` (vault backup) | **SW:** `qc-v226` | **Sentry:** `quantum-cube@qc-v226`

**Pending before Play Store submission:**
- ⏳ Google identity verification — main gate, check email Monday morning
- ⏳ 12 testers + 14-day closed test
- 🔲 Monday: test Dodo overlay inside TWA on device → decide redirect vs direct overlay
- 🔲 **Create review Gmail account** — dedicated account for Google Play reviewers. Sign in once at quantumcube.app/app via magic link to create Supabase profile → then ping Claude to set has_paid=true. Share credentials in Play Console App Access → Any other instructions. (Magic link flow: enter email, check Gmail, click link.)
- 🔲 Privacy policy: verify Supabase + Dodo Payments are explicitly named by name (PostHog + Sentry already confirmed added)
- 🔲 Supabase Pro upgrade ($25/mo) — do before Android traffic hits
- 🔲 4–6 portrait screenshots on phone
- 🔲 Feature graphic: user approval → commit to `docs/`
- 🔲 Store listing copy: short description (≤80 chars) + full description (≤4000 chars) — not drafted yet
- 🔲 **External Content Links Program** — enroll in Play Console → Settings before going live. Also integrate Google API for pre-redirect info screen in IS_TWA unlock flow (code change in app.html).
- 🔲 **Pre-redirect disclosure modal** — add to IS_TWA unlock flow: "You'll be taken to your browser to complete this purchase outside Google Play." (code change)
- 🔲 **Public account-deletion URL** — static page at quantumcube.app/account/delete. Play Console Data Safety form requires web URL alongside in-app deletion.
- 🔲 **USPTO trademark check** — run "Quantum Cube" on tmsearch.uspto.gov in Class 9 + Class 41. 5 min check.
- 🔲 **Prominent in-flow privacy disclosure** — small visible line before DOB/email entry on Face 0, not just footer.
- 🔲 **ElevenLabs commercial license** — verify current tier permits paid-app distribution.
- 🔲 **AI declaration: NO** — ElevenLabs TTS of pre-written scripts = not AI-generated content per Google's definition. Declare NO in App Content.
- 🔲 **Play Console form work** (all require app entry created first — post-identity-verification):
  - Health Apps Declaration (all apps, even non-health — declare "no health functionality")
  - AI-generated content declaration (tick YES — ElevenLabs narration)
  - Target audience: 18+ (avoids Families Policy)
  - Content rating questionnaire (IARC — likely Everyone/Everyone 10+)
  - Data safety form (email, name, DOB, purchase history, PostHog, Sentry)
  - App content declarations (ads: no, news: no, financial: no, COVID: no, government: no)
  - Privacy policy URL input
  - Test credentials for Google review team (app requires sign-in — need to provide test email)
- 🔲 **Post-AAB-upload:**
  - Play App Signing second SHA-256 from Play Console → add to `assetlinks.json` → redeploy
  - Deep Link Verification tool (Play Console → Android Vitals)
  - Pre-launch report review before promoting to closed test

**🚀 MONDAY PLAN:**
1. Check email for identity verification approval
2. Once approved → Create app in Play Console → upload AAB
3. Test Dodo overlay on device inside TWA → lock payment UX
4. Recruit 12 testers → 14-day clock starts
5. Fill all Play Console forms while waiting on 14 days
6. Take screenshots on phone
7. Draft store listing copy (can do in parallel)

---


## 2026-05-10 Evening — Obsidian graph maximised (Chat Claude)

**Goal:** Build out the Obsidian second brain graph to full visual density.

**Done:**
- ✅ **550+ atomic vault nodes created** — numerology numbers 1-31, alphabet A-Z, challenge/pinnacle/karmic-debt/personal-month numbers, astrology houses 1-12, aspects, ruling planets per sign, Chinese zodiac yin/yang + elements, PostHog events, Supabase table/column detail, Sentry detail, edge function internals, business/legal nodes, marketing channels, Play Store requirements, ADR sub-decisions, operating rule sub-items, colors/fonts/sounds
- ✅ **Graph color fixed** — switched from tag-based to path-based color groups. White=core docs, Cyan=vault/numerology+cube-faces+app-sections, Purple=vault/tech+features, Pink=vault/decisions+marketing+play-store+operating+brief-archive
- ✅ **All 8 core docs now white** — MARKETING_PLAYBOOK, BRIEF_ARCHIVE, PLAY_STORE_PREP, OPERATING_RULES all tagged #core
- ✅ **Tags toggle OFF recommended** — tag nodes (green dots) are visual clutter, file nodes with colors look far cleaner

**Current HEAD:** `d1118bb` | **SW:** `qc-v225`

**Pending (unchanged):**
- ⏳ Google identity verification email — check first thing next chat
- ⏳ 12 Android testers recruited
- 🔲 In-app entertainment disclaimer (quick commit)
- 🔲 Supabase Pro upgrade ($25/mo)
- 🔲 4–6 portrait screenshots for Play Store

**🚀 NEXT-CHAT LEAD-IN:**
1. Boot per CHAT_KICKOFF v5.0.0 — Obsidian must be open
2. Check email for Google identity verification approval
3. First task: entertainment disclaimer commit, then tester recruitment message

---


## 2026-05-10 PM — Obsidian second brain setup (Chat Claude)

**Goal:** Wire Obsidian as the live knowledge base for the project. Obsidian-first boot architecture replacing manual project file uploads.

**Done:**
- ✅ **mcp-obsidian installed** — `uvx mcp-obsidian` via Local REST API plugin (HTTP port 27123, API key stored in config). Full read/write access to vault from Claude Desktop.
- ✅ **Vault pointed at `/Users/qnc/Projects/quantumcube`** — all project markdown files now browsable in Obsidian with graph view.
- ✅ **Obsidian Git plugin installed + configured** — auto commit-and-sync every 10 min, push on sync, pull on startup.
- ✅ **CHAT_KICKOFF.md rewritten to v5.0.0** — lean Obsidian-first boot doc. SESSION_LOG + PROJECT_BRIEF read live from vault every chat. No more manual project file uploads ever.
- ✅ **OPERATING_RULES.md created** — all detailed golden rules, command templates, failure recovery, Cursor fallback moved here from old CHAT_KICKOFF.
- ✅ **31 atomic vault notes created** — 18 ADR notes, 6 tech nodes (supabase, sentry, posthog, elevenlabs, android, cloudflare, resend), 5 feature nodes (narrate, dodo-webhook, resend-events, unlock-flow, service-worker), 4 marketing nodes. All tagged + wiki-linked to hub docs.
- ✅ **Obsidian graph configured** — dark mode, AnuPpuccin theme, 3D Graph plugin, color groups (white=core, purple=tech/features, pink=decisions/reference), filters exclude non-markdown folders.
- ✅ **Vercel downgraded** — Pro → Hobby (free). Was billing ~$47/cycle for unused Academy project. Stopped.
- ✅ **Google Play email clarified** — generic onboarding email, NOT identity verification approval. Still waiting on that.

**Current HEAD:** `c26ea4e` | **SW:** `qc-v225`

**Pending (unchanged from morning session):**
- ⏳ Google identity verification email
- ⏳ 12 Android testers recruited
- 🔲 In-app entertainment disclaimer
- 🔲 Supabase Pro upgrade ($25/mo)
- 🔲 4–6 portrait screenshots for Play Store

**🚀 NEXT-CHAT LEAD-IN:**
1. Boot per CHAT_KICKOFF v5.0.0 — Obsidian must be open.
2. Waiting on Google identity verification — check email first.
3. First real task: entertainment disclaimer (quick commit) or tester recruitment message.

---


Live working narrative across chats. Append-only. Each session adds a new entry **early** in the work (after the first non-trivial action), then updates it incrementally. This survives tools-drops, Mac permission prompts, browser crashes — anything that wipes the chat without wiping git.

Format per entry: date stamp, one-line goal, bulleted actions, open questions, what's next. Terse. This is for the next-chat-Claude, not a journal.

For older completed-and-committed history, see `BRIEF_ARCHIVE.md`.

---

## 2026-05-10 — Brand polish + Google Play Store setup (Chat Claude)

**Goal:** Pre-Play-Store app polish, full Play Store submission preparation, Google Play developer account creation, Android TWA build + assetlinks wired.

**Done in this chat:**

- ✅ **Brand cyan updated #7dd4fc → #0cc0df** across entire `app.html` — 75 replacements covering hover states, glows, box-shadows, cube face borders, face label cards, all interactive button hovers, and all 5 Vimeo `color=` params (commit `af5a3f3`, qc-v223 → qc-v224). CSS `--glow` variable now points to the new cyan so all referencing selectors inherit automatically.
- ✅ **Privacy policy updated** — added PostHog (EU, anonymous usage events) and Sentry (EU, error/crash data) to service providers list; effective date updated 24 Apr → 9 May 2026 (commit `0db433f`). Live at `https://quantumcube.app/privacy` — Play Store ready.
- ✅ **TWA detection + Android payment redirect** (commit `0cd3f9c`, qc-v224 → qc-v225): `IS_TWA` const (triple detection: `document.referrer` startsWith `android-app://`, `sessionStorage`, URL param `utm_source=android-twa`). `unlock()` now short-circuits to `window.open('https://quantumcube.app/app?ref=android-unlock')` on Android — zero Play Billing required, zero policy risk. Web unlock flow completely unchanged. Supabase `has_paid` flag means existing paid web users open the Android app already unlocked.
- ✅ **`assetlinks.json` wired with real SHA-256** (commit `d298804`): `app.quantumcube.twa` + keystore fingerprint `14:01:92:A5:20:FC:99:8F:03:07:2C:0E:69:3B:EC:04:18:5F:30:DA:14:07:BF:61:6E:C8:E1:12:F9:F7:9B:3D`. Verified live on `https://quantumcube.app/.well-known/assetlinks.json`.
- ✅ **PLAY_STORE_PREP.md / PLAY_STORE_CHECKLIST.md created** (commit `9ed130b`, Claude Code) — comprehensive Play Store submission checklist with 2026 Google policies cited, ~80 yes/no items, payment strategy analysis, all risks documented.
- ✅ **AAB + APK built by Claude Code** — `android/app-release-bundle.aab` (1.66 MB), `android/app-release-signed.apk` (1.62 MB). Keystore: `android/quantumcube.keystore` (2.7 KB), validity 10,000 days (~27 years). Target SDK 35, compile SDK 36. Keystore password saved to Apple Passwords ("Quantum Cube Android Keystore"). `.gitignore` protects keystore + build outputs; `twa-manifest.json` + `scripts/build-twa.mjs` committed for rebuild.
- ✅ **Google Play developer account created** — Quantum Neuro Creations, personal account, Account ID `9099327495444765719`, `quantumneurocreations@gmail.com`. $25 fee paid. Identity documents + bank statement uploaded for verification. 14-day closed testing gate clock started May 10 → production access request eligible ~May 24.
- ✅ **Play Console configured** — developer name "Quantum Neuro Creations", website `https://quantumcube.app`, payments profile: Computer Software, "QUANTUM CUBE" statement name, in-app purchases (not paid apps).
- ✅ **Feature graphic created** — 1024×500 PNG (Play Store spec), Milky Way space photo background, Cinzel Decorative font (real Google Fonts via Puppeteer), wireframe neon cyan cube (multi-pass glow), tagline + descriptor. File: `quantum-cube-feature-graphic.png`.

**Commits (this session):**
- `af5a3f3` — style: update brand cyan #7dd4fc → #0cc0df across app (buttons, glows, cube, Vimeo); bump qc-v224
- `0db433f` — legal: privacy policy — add PostHog + Sentry to service providers, update effective date
- `0cd3f9c` — feat(android): TWA detection — redirect unlock to website on Android, no Play Billing required; bump qc-v225
- `d298804` — feat(android): assetlinks.json — real SHA-256 fingerprint from production keystore (app.quantumcube.twa)
- `9ed130b` — docs: add PLAY_STORE_PREP.md — strict first-try-approval checklist with 2026 policies cited (Claude Code)

**Current HEAD:** `d298804` | **SW:** `qc-v225` | **Sentry:** `quantum-cube@qc-v225`

**Pending / waiting:**
- ⏳ Google identity verification (1–3 business days — unlocks "Create app" in Play Console)
- ⏳ 12 testers needed for closed testing track — recruit friends/family with Android phones, 14-day gate
- ⏳ Play App Signing SHA-256 — Google generates their own upload key after first AAB upload; add as second fingerprint in `assetlinks.json`
- ⏳ Data safety form + content rating questionnaire (in Play Console once app entry created)
- 🔲 In-app entertainment disclaimer — short "for entertainment purposes only" note somewhere visible (Google "impossible functionality" risk for astrology/numerology)
- 🔲 Supabase Pro plan upgrade — flagged: free tier auto-pauses projects with no traffic for 7 days. Live paying-customer app = production blocker risk at $25/month. Also unlocks custom auth domain (`auth.quantumcube.app` → fixes ugly OAuth sign-in URL).
- 🔲 4–6 portrait screenshots of live app (user's phone) for Play Store listing
- 🔲 Feature graphic: user to approve final version, then copy to `docs/` + commit

**🚀 NEXT-CHAT LEAD-IN:**
1. Boot per `CHAT_KICKOFF.md`. Check `d298804` is still HEAD.
2. **Check email** — Google identity verification approval unblocks everything. When approved: go to Play Console → Create app → walk through setup.
3. **Tester recruitment** — if 12 testers not yet recruited, draft message and send today. Counter visible in Play Console → Testing → Closed testing.
4. **In-app entertainment disclaimer** — add a small line to the app. Suggest: add to the profile form page or settings area. Quick commit.
5. **Supabase Pro upgrade** — do this before any significant traffic. One-click in Supabase dashboard.
6. **Screenshots** — take 4–6 portrait screenshots on phone, have ready for Play Console store listing.

**Pre-existing operational notes:**
- Android keystore: `~/Projects/quantumcube/android/quantumcube.keystore` — password in Apple Passwords
- Package name: `app.quantumcube.twa` — permanent, never changes
- SHA-1: `B4:AB:EA:5B:C2:23:41:45:E4:11:0E:AD:06:D8:7C:16:C3:ED:9C:76` (some tools need this)
- ElevenLabs: `eleven_turbo_v2_5`, stability 0.5, similarity_boost 0.75, speed 1.15 (welcome.mp3: speed 1.0)
- Claude Code at `~/Projects/quantumcube`, `scripts/build-twa.mjs` is the AAB rebuild script

---

## 2026-05-09 — Narration audit & full re-record pass (Claude Code)

**Goal:** Finish the narration-fix workstream queued from May 8: fix the audit tool, audit all 385 MP3s for issues, regenerate every flagged file at the correct ElevenLabs settings, ship.

**Done in this chat (Claude Code, terminal):**

- ✅ **claudewatch MCP installed** (surgical — MCP entry only, no global rule files; binary at `~/.local/bin/claudewatch`). Cache bumped qc-v212 → qc-v213 in the same commit chain. Tools-list now shows ~30 claudewatch.* analytics tools alongside the prior 20 servers.
- ✅ **`docs/audit-narration.html` actually working.** Root cause: an unescaped single quote inside the textarea `placeholder` attribute was silently breaking HTML parsing on every browser, leaving the page blank with no console error. Fixed via `&apos;` escapes (commit `ed04840`). Added a SW bypass for `audit-narration.html` so a fresh copy is always served (commit `9aec413`) — needed because debugging cached failures was burning time.
- ✅ **Audit completed end-to-end.** Of 385 MP3s, **98 flagged** for re-record (Life Phase pause-before-number, Birthday prefix, Karmic Lesson awkward digits, etc.).
- ✅ **Three rerecord passes to find the correct ElevenLabs settings** (story preserved here because it cost real credits):
  1. **Pass 1 — speed 0.85.** Source: ElevenLabs dashboard's saved voice profile (`/v1/voices/<id>` returned `speed: 0.85`). Wrong — too slow vs the untouched 287 originals.
  2. **Pass 2 — speed 1.0.** Closer but still noticeably slower than the rest of the library.
  3. **Pass 3 — speed 1.15.** Found by `git log -p --pickaxe-regex -S speed -- supabase/functions/narrate/`: commits `f7854ee` (256 MP3 bulk gen) and `be9f385` (phase 2 generation) both had the narrate Edge Function hard-coded at `speed: 1.15` at the time the originals were recorded. **This is the correct production setting.** `similarity_boost` was also wrong on disk (0.51 vs original 0.75) — corrected in the same pass.
- ✅ **Script transformations for stubborn TTS.** Ran each fix as a TTS-payload-only rewrite (manifest text untouched, app UI unchanged):
  - **Life Phase 2-9** (`num_pc_<n>_v1.mp3`): "A 2 Life Phase marks…" → "A Life Phase governed by the 2 marks…" (kills the awkward pause before the number).
  - **Birthday 1-9, 11, 22**: scripts already had "Birthday Number" prefix. Confirmed and shipped as-is.
  - **Karmic Lesson 1-9** (`num_kl_*`): digit spelled out — "A Karmic Lesson 1" → "A Karmic Lesson One". Same pattern for 2/3/4/5/6/7/9.
  - **Hidden Passion 4 & 6** (`num_hp_4_v3`, `num_hp_6_v3`): digit was being swallowed entirely. Spelled out + comma-padded + finally em-dash-padded for hp_6 ("The Hidden Passion — Six —"). Three passes to crack hp_6 specifically.
  - **chin_ox_core**: "Ox" rendered as just "ssss". TTS payload now uses phonetic respelling "Ocks" for all three occurrences. Manifest text stays "Ox".
- ✅ **`scripts/rerecord.py` shipped** — single-purpose Python script that reads the manifest from `audit-narration.html`, applies the named transforms, POSTs to ElevenLabs direct, writes MP3s + emits SHA256 JSON for manifest update. Lives at `scripts/rerecord.py` for any future per-file re-records.
- ✅ **Numerology Matrix description card added to `docs/app.html`** — non-interactive `.matrix-desc` static card sits directly below the 3×3 matrix grid, explains what the matrix is. Same border/glass/inset-glow as the icard pattern, no cursor or click handler.
- ✅ **Per-key ElevenLabs quota raised twice** mid-session (200K → 400K) when the rerecord burned through the per-key character cap. Account-level pool was fine; the `Quantum Cube` key's own limit needed lifting in the dashboard.

**Commits (chronological, this session, after `ed04840`):**

- `e0f3c79` — feat(narration): regenerate 98 MP3s; Life Phase pause fix, Birthday prefix
- `b78bf86` — chore: bump cache qc-v213 → qc-v214
- `6d8af3b` — feat(narration): regenerate 98 MP3s at speed 1.0; bump qc-v214 → v215
- `3161400` — feat(matrix): add static description card below numerology matrix; bump v215 → v216
- `cec69b0` — feat(narration): regenerate 98 MP3s at original settings (sb 0.75, speed 1.15); bump v216 → v217
- `4bc30f3` — feat(narration): re-record 20 MP3s; spell out Karmic Lesson digit; bump v217 → v218
- `c19d19f` — feat(narration): re-record 3 MP3s (hp_4, hp_6, ox); bump v218 → v219
- `cb1628e` — feat(narration): re-record same 3 MP3s again; bump v219 → v220
- `4064ae4` — fix(narration): phonetic fixes for hp_4/hp_6 (digit→word) and ox (Ox→Ocks); bump v220 → v221
- `46f7994` — fix(narration): hp_6 comma-pad 'Six'; bump v221 → v222
- `29eece7` — fix(narration): hp_6 em-dash 'Six' to break Passion-Six phonetic merge; bump v222 → v223

**In progress:**
- _(Listening pass on hp_6 v223 outstanding from user — em-dash fix may still drop the digit. Fallback plan: "The Hidden Passion of Six" or "Number Six".)_

**Open questions / decisions pending:**
- _(none beyond hp_6 confirmation above)_

**🚀 NEXT-CHAT LEAD-IN:**
1. Boot per `CHAT_KICKOFF.md` v4.3.0.
2. **Listen to hp_6 at qc-v223 first thing.** If the digit is still swallowed, tweak `rerecord.py` Hidden Passion transform to "The Hidden Passion of Six" (preposition-bridge), regenerate, ship.
3. **Narration pipeline is otherwise complete** — all 385 MP3s at the correct production settings, manifests in sync, audit tool live for any future regression.
4. **App polish + Play Store TWA still pending** (target was Sunday May 10 — slipping; keystore + assetlinks SHA-256 still need real values).

**Pre-existing operational notes:**
- HEAD: `29eece7` → will update after this handoff commit
- SW: `qc-v223`. Sentry release: `quantum-cube@qc-v223`. Pre-commit hook validates sync.
- ElevenLabs key (`Quantum Cube`) per-key cap now 400K; account pool healthy.
- `scripts/rerecord.py` is the canonical re-record tool — edit `FILES` + transforms, dry-run, generate.


## 2026-05-08 evening/night — Chrome audit sweep + Claude Code setup

**Goal:** Chrome tabs safety/efficiency audit + Claude Code installation + full tool setup.

**Done in this chat:**
- ✅ `docs/manifest.json` TWA audit — added `id: "/app"` for stable PWA identity (commit `4b69936`)
- ✅ **Claude.ai settings audit** — Instructions for Claude field populated (persistent prefs across all chats), Discovery toggle OFF, Cloudflare Developer Platform disconnected (redundant), Privacy verified (training OFF, location OFF)
- ✅ **Supabase audit** — advisors clean (0 performance, 1 known false-positive re: password auth), RLS verified on both public tables, 6 edge functions confirmed ACTIVE. Stale unconfirmed auth user `admin@qncacademy.com` deleted (created Apr 21, never confirmed). auth.users: 8, all confirmed.
- ✅ **Sentry/Clarity CSP fix** (commit `da02bc3`, qc-v212) — Previous chat wired Clarity but only whitelisted `www.clarity.ms` in script-src. Clarity CDN (`scripts.clarity.ms`) was blocked → Sentry `JAVASCRIPT-6`. Fixed: `*.clarity.ms` wildcard across all 10 pages with CSP meta tags. JAVASCRIPT-6 resolved.
- ✅ **PostHog audit** — SDK doctor healthy, 3 insights configured, ingestion alive (6 events/2 days). No action needed.
- ✅ **Claude Code installed** — v2.1.133 via native installer, Opus 4.7 (1M context), Claude Max plan, `~/Projects/quantumcube`
- ✅ **Claude Code configured** (commits `347afb6`, `55f72fc`, `efc4a66`, `2ab95a0`):
  - `~/.claude/CLAUDE.md` — global prefs (buddy tone, autonomy, upgrading mindset)
  - `.claude/commands/` — `/project:health-check`, `/project:pre-ship`, `/project:narration-fix`
  - `.claude/settings.json` — PostToolUse hook warns on SW/APP version mismatch
  - `.mcp.json` cleared (project-level remote SSE MCPs conflict with claude.ai connectors)
- ✅ **User MCPs added to Claude Code** (global scope): ElevenLabs (24 tools), Context7 (2 tools), Tavily (5 tools)
- ✅ **20 MCP servers total** in Claude Code: 3 user MCPs + 17 claude.ai connectors (GitHub 41, Supabase 29, Sentry 22, Resend 32, Linear 33, etc.)
- ✅ Extra usage enabled on Claude.ai ($20/month limit)

**Key architectural insight (ADR-020):** Remote SSE MCPs (Supabase/Sentry/PostHog hosted URLs) cannot run from local Claude Code — Anthropic policy blocks persistent SSE from local machines. Solution: claude.ai connectors auto-sync to Claude Code when authenticated with Max plan. No project-level MCP config needed for cloud services.

**Division of labour going forward:**
- **Claude Code (terminal):** file edits, git, bash, deploys, narration regeneration via ElevenLabs MCP
- **Claude Chat (web):** planning, PostHog analytics, Sentry investigation, browser automation

**In progress:**
- _(nothing uncommitted — all shipped)_

**Open questions / decisions pending:**
- _(none)_

**🚀 NEXT-CHAT LEAD-IN:**
1. **Boot as usual** per CHAT_KICKOFF.md v4.3.0. Read this SESSION_LOG after PROJECT_BRIEF v43.
2. **Narration fix is the immediate coding task** — start in Claude Code terminal: `/project:narration-fix`. This loads context and reads the Edge Function. The audit tool at `/audit-narration.html` needs a bug fix first (user reported it's not working well). Fix the audit tool → user flags bad MP3s → Claude Code regenerates flagged files via ElevenLabs MCP with corrected phonetics → replace files.
3. **Play Store TWA** — target was Sunday May 10. Steps: generate Android keystore via Bubblewrap, get real SHA-256 for `/.well-known/assetlinks.json`, build `.aab`, submit to Play Console.

**Pre-existing operational notes:**
- HEAD: `2ab95a0` → will update after handoff commit
- SW: `qc-v212`. Pre-commit hook validates sync.
- Sentry: 0 unresolved issues.
- auth.users: 8 (all confirmed, no stale records).
- Claude Code: active at v2.1.133. Run `claude` from `~/Projects/quantumcube`.


## 2026-05-08 PM — Stack-upgrade sweep + process hardening

**Goal:** Continue the May 8 stack audit. User flagged: previous chat (titled "System upgrade") got disrupted by a Mac permission prompt + Claude Desktop restart. Recovered context from git commits + DECISIONS.md (ADR-017). Then user asked Claude to bring its own ideas for further upgrades instead of always being the recipient of his.

**Done in this chat:**
- ✅ Resend dedicated key created (`quantum-cube-dodo-webhook`, id `5b36c8df-645e-4a77-bc25-a060ad22b161`) — saved in user's Apple Passwords
- ✅ `RESEND_API_KEY` set as Supabase Edge Function secret (digest `02d1cd31...`) — unblocks welcome email pipeline shipped this morning in commit `14e4210`
- ✅ Key validated: domain `quantumcube.app` reachable, "Quantum Cube Customers" audience reachable
- ✅ UptimeRobot monitor `803021425` "QC — Narrate (Edge Function)" — keyword check on `Method not allowed`, alerts when missing
- ✅ Memory edit added: user prefers verbal/speech-to-text — never use `ask_user_input_v0` option pickers
- ✅ Canonical skill `.claude/skills/quantum-cube/SKILL.md` bumped 1.0.0 → 1.1.0 — added §2.6 no-option-pickers, §2.7 proactive inline suggestions, §2.8 SESSION_LOG protocol (commit `094cb78`)
- ✅ `SESSION_LOG.md` created (this file)
- ✅ **Resend bounce/complaint → Sentry pipeline shipped** (commit `723b2d5`) — new Edge Function `resend-events`, webhook `2a5c62b4-7e5c-42eb-bdeb-fbe56bcdc8f9`, signing secret stored as `RESEND_WEBHOOK_SECRET`. Closes the Resend-webhooks-NONE-configured gap from PROJECT_BRIEF.md.
- ✅ **Status page rebranded as "Quantum Cube — Status"** at `https://stats.uptimerobot.com/azO4bPUJJQ` — logo (qc-icon-192.png) + favicon (qc-favicon-32.png) uploaded, homepage URL set to https://quantumcube.app, auto-add-monitors stays ON
- ✅ **PostHog narrate instrumentation shipped** (commit `e5467d5`, qc-v210→v211) — `narrate_api_requested`, `narrate_api_succeeded`, `narrate_api_failed`, `narrate_audio_played` events added to `fetchNarration()` and `startNarrationFromUrl()`. Now we can measure narration success rate, API latency, and validate the upcoming narration fix against real before/after metrics.
- ✅ **PostHog insight "Narrate — API health" created and favorited** — https://eu.posthog.com/project/172921/insights/buiaXjHa (short_id `buiaXjHa`, id 4114564). 14-day Trends line graph of all four narrate_* events. Tagged `narrate`, `api-health`, `qc-v211`.
- ✅ **PostHog insight "Narrate — API latency (p50 / p95 / p99)" created and favorited** — https://eu.posthog.com/project/172921/insights/AHB7Ci6u (short_id `AHB7Ci6u`, id 4114617). 14-day Trends line graph of latency_ms percentiles from `narrate_api_succeeded`. Tagged `narrate`, `latency`, `qc-v211`.
- ✅ **Project annotation marking qc-v211 deploy** at 2026-05-08T12:00:00Z — marker will appear on every PostHog chart so the before/narration-fix-after split is visible.

*(Briefly created a "Quantum Cube — Narrate Health" dashboard to group both insights, then deleted it: the available PostHog MCP tools don't support attaching insights to a dashboard programmatically (no `insight-update` exposed via tool_search), and an empty pinned dashboard is worse UX than two favorited insights. Both insights are findable via the PostHog Insights menu's Favorites filter.)*

**In progress:**
- _(none — all live work for this chat is shipped and pushed; HEAD at `e26d591`)_

**Skipped (user agreed to defer):**
- Weekly digest email (user prefers daily review)
- PostHog feature flags + first A/B test (later)
- "First 1000 customers" Resend templates playbook (later)
- Vercel preview deploys (Claude reconsidered — architecture mismatch, see ADR-018)
- UptimeRobot CNAME (`status.quantumcube.app`) — paid-only on UptimeRobot, default `stats.uptimerobot.com/azO4bPUJJQ` URL is fine
- Custom "Narrate Health" PostHog dashboard — PostHog MCP doesn't expose `insight-update` cleanly; two favorited insights are sufficient (see ADR-018)

**Open questions / decisions pending:**
- _(none — all questions from earlier in the session resolved before doc-update commit)_

**Doc-update transition pack (committed at end of this chat):**
- `PROJECT_BRIEF.md` v41 → v42 — added v42 update note, bumped Edge Functions count 5 → 6, added `resend-events` subsection, added webhook → Sentry paragraph in Email Infrastructure
- `DECISIONS.md` — added ADR-018 covering all PM work (Resend webhook, narrate analytics, Vercel skip, skill v1.1.0)
- `CHAT_KICKOFF.md` v4.1.0 → v4.2.0 — added `SESSION_LOG.md` to the read-in-order doc system, updated boot footer to read brief THEN session log
- `SESSION_LOG.md` (this file) — final polish for clean handoff

**🚀 NEXT-CHAT LEAD-IN (start here):**

1. **Boot sequence as usual** — run `tool_search` calls per `CHAT_KICKOFF.md` v4.2.0 BOOT STEP 1, smoke-test loaded tools (BOOT STEP 2), health-check (BOOT STEP 3). Then read `PROJECT_BRIEF.md` v42 and this file.

2. **First proactive task: 60-second `docs/manifest.json` audit against Google Play TWA requirements.** Target: Google Play submission Sunday May 10 (~2 days out). Specifically grep for / verify:
   - 512×512 `maskable` icon entry (`purpose: "any maskable"` or `purpose: "maskable"` separate entry)
   - `display: "standalone"` or `"fullscreen"` (TWA requires this; `"browser"` would block Play approval)
   - `start_url` is a valid same-origin path
   - `theme_color` and `background_color` set (Play uses these for splash)
   - `name` (full ≤ 45 chars for Play listing) and `short_name` (≤ 12 chars for Android home screen)
   - `scope` set to `/` or app-root
   - `id` field present (recommended for stable PWA identity)

   Report findings back inline, then ship a single commit if anything's missing. Existing `/.well-known/assetlinks.json` placeholder still needs the real keystore SHA-256 — that's a separate step user needs to do at signing time, not chat-side.

3. **Then onto the narration-fix workstream.** Telemetry is now waiting (qc-v211 instrumentation + 2 PostHog insights + project annotation). Whatever the fix turns out to be, the before/after will be measurable on `https://eu.posthog.com/project/172921/insights/buiaXjHa` and `/AHB7Ci6u`.

**Pre-existing operational notes for next-chat-Claude:**
- HEAD: `e26d591` (post doc-update commit will bump this)
- Live SW: `qc-v211`. Sentry release: `quantum-cube@qc-v211`. Pre-commit hook validates this sync — don't bypass.
- Resend webhook deployment status: live, signing secret set, tested 400 + 401 paths
- Welcome email pipeline live on `dodo-webhook` Edge Function (ADR-017) — first paying customer post-`RESEND_API_KEY` setup gets brand-voiced welcome automatically
- Skill is at v1.1.0 — process changes already encoded (no option pickers, proactive close, this log file)

> **Related:** [[PROJECT_BRIEF]] · [[DECISIONS]] · [[BRIEF_ARCHIVE]] · [[CHAT_KICKOFF]] · [[OPERATING_RULES]]


**Google Play onboarding email content (received May 10, 4:47PM SAST):**
From: Google Play | Apps & Games — "Quantum Neuro Creations, your launch journey starts here"
Three steps outlined:
1. Test early and often — internal tests + 14-day closed test with min 12 users
2. Build secure + transparent — Play Integrity API + complete data safety form
3. Comply and stay in control — follow Play Developer policy, use managed publishing
⚠️ Warning in email: "Don't forget to verify your account to maintain your Console access" — identity verification still pending, this is the main blocker for everything.

**End of session additions:**
- PLAY_STORE_PREP.md updated with Section 13 (policy audit) + Section 14 (Play Console tools)
- Full Google Play Policy Center audit completed — all categories checked, 4 small gaps added to checklist
- Deep link verification + crash deobfuscation added as pre-launch steps
- Vault has everything. All committed and pushed.

**🚀 MONDAY PLAN:**
1. Boot — check email for Google identity verification
2. Once verified → Create app in Play Console → upload AAB → internal test track live within minutes
3. Team meeting → recruit 12 testers → share opt-in link → 14-day closed test clock starts
4. While waiting on 14 days → entertainment disclaimer commit → store listing copy → screenshots → data safety form → app content declarations (health, AI, ads, no news)
5. After 14 days → request production access → submit

---

## 2026-05-10 Late Night — Final wrap-up (Chat Claude)

**Done this session:**
- ✅ Entertainment disclaimer — already in CSS on every face, confirmed
- ✅ PostHog SDK v3+ — Android ID policy fine
- ✅ 192×192 maskable icon — created + committed ca863c2, qc-v226, pushed
- ✅ ElevenLabs commercial license — confirmed, all paid plans cover app distribution
- ✅ Account type — stay personal. Read-only after signup. Developer name "Quantum Neuro Creations" already set and shows prominently on Play Store. Not a blocker.
- ✅ CIPC docs confirmed — QNC (PTY) Ltd reg 2019/559151/07, In Business
- ✅ Claude Code full policy audit — 3 agents, 195 tool uses. PLAY_STORE_PREP.md Section 15 added.
- ✅ External Content Links Program — Jan 28 deadline for existing apps only. New apps enroll before going live. Still open.
- ✅ All docs updated (SESSION_LOG + PLAY_STORE_PREP.md)

**Monday plan:**
1. Check email — identity verification approval
2. Run Claude Code audit list — implement code-side items (pre-redirect disclosure, account/delete page, in-flow privacy disclosure)
3. USPTO trademark check via Claude Code (tmsearch.uspto.gov — "Quantum Cube" Class 9 + 41)
4. Once verified → Create app → upload AAB → enroll External Content Links Program
5. Recruit 12 testers → 14-day clock starts
6. Use 14 days: Play Console forms + store listing copy + screenshots

**HEAD:** `3049a13` | **SW:** qc-v226 | **Sentry:** quantum-cube@qc-v226

---

## 2026-05-11 Morning — Claude Code compliance fixes (qc-v227)

**Commit:** `2244dfe` — pushed to origin/main

**Done:**
- ✅ Pre-redirect disclosure modal (TWA only) — "Leaving Quantum Cube / You'll be taken to your browser to complete your purchase outside Google Play." Continue/Cancel buttons. Only fires when IS_TWA=true. Lines 430–445 (CSS), 2860 (escape key), 2952–2975 (unlock logic), 4032–4040 (HTML).
- ✅ In-flow privacy disclosure — line below Face 0 form inputs, above submit button: "Your details are used only to generate your personal reading. See our Privacy Policy." Line 704.
- ✅ AI narration disclosure — Settings face (Face 7), below Delete Account button: "Narration is AI-generated using ElevenLabs." Line 985.
- ✅ Account deletion page — `docs/account/delete/index.html` + `docs/account-delete.html` both created. URL: quantumcube.app/account/delete. Dark theme, Cinzel font, full deletion instructions + fallback email.
- ✅ SW bumped qc-v226 → qc-v227. Sentry release in sync. runCalculation anchor intact at line 3437.
- ⚠️ USPTO trademark search — partial. No exact "QUANTUM CUBE" found in Class 9 or 41 via web mirrors (Justia, Trademarkia). Similar marks noted (Q.U.B.E., Quantum Conundrum, QUBE) but none identical. Manual pass still needed at tmsearch.uspto.gov — 5 min human task.

**Google bank account verified** (email 05:32 AM) — payments unblocked ✅
**Identity verification** — submitted Saturday May 9, expected today/tomorrow.

**Still pending:**
- 🔲 Identity verification email → create app in Play Console
- 🔲 USPTO manual trademark check (tmsearch.uspto.gov — "Quantum Cube" Class 9 + 41)
- 🔲 Create review Gmail account → sign in once → ping Claude to set has_paid=true
- 🔲 External Content Links Program enrollment (Play Console → Settings, after app created)
- 🔲 Supabase Pro upgrade ($25/mo) before Android traffic hits
- 🔲 assetlinks.json second SHA-256 (Play App Signing key — after AAB upload)
- 🔲 12 testers recruited → 14-day clock
- 🔲 4–6 portrait screenshots on phone
- 🔲 Store listing: short description (≤80 chars) + full description (≤4000 chars)
- 🔲 Play Console forms (all after app created): Health Apps, AI content, target audience 18+, content rating, data safety, app access (review Gmail credentials), privacy policy URL

---

## 2026-05-11 Morning — IDENTITY VERIFIED + Full session wrap (Chat Claude)

**🚨 IDENTITY VERIFIED 6:45 AM — GO TO PLAY CONSOLE NOW**
**🚨 BANK ACCOUNT VERIFIED 5:32 AM — payments unblocked**

Both gates cleared. App creation is unblocked. Start new chat immediately — will be sending screenshots through Play Console setup.

---

### WHAT WAS COMPLETED THIS SESSION (full record)

**Code commits:**
- `ca863c2` — qc-v226: entertainment disclaimer confirmed in CSS, 192×192 maskable icon created + added to manifest.json
- `2244dfe` — qc-v227: pre-redirect disclosure modal (IS_TWA only), Face 0 in-flow privacy disclosure, AI narration label in Settings (Face 7), `/account/delete` page created. All pushed to origin/main.
- Current HEAD: `2244dfe` | SW: qc-v227 | Sentry: quantum-cube@qc-v227

**Trademark search — CLEAR ✅**
- Full USPTO export (500 live marks) scanned programmatically
- NO federal registration or pending application for "QUANTUM CUBE" in Class 9 (software/apps) or Class 41 (entertainment)
- Quantum Cube LLC exists (speed cubing timer app) — common law rights only, completely different goods/services, coexistence defensible
- Name is clear to use

**Claude Code policy audit — 3 agents, 195 tool uses:**
All findings captured in PLAY_STORE_PREP.md Section 15. Key items:
- External Content Links Program: must enroll in Play Console → Settings BEFORE going live (Jan 28 deadline was for existing apps only — new apps enroll pre-launch)
- Pre-redirect disclosure modal: ✅ DONE in qc-v227
- Public account/delete URL: ✅ DONE (quantumcube.app/account/delete)
- In-flow privacy disclosure Face 0: ✅ DONE in qc-v227
- AI narration label: ✅ DONE in qc-v227
- Health Apps Declaration: do in Play Console (declare no health functionality)
- AI-generated content declaration: declare NO (ElevenLabs TTS of pre-written scripts ≠ runtime AI generation)
- Data Safety form: email, name, DOB, purchase history, PostHog, Sentry, device IDs
- ElevenLabs commercial license: ✅ CONFIRMED — all paid plans permit app distribution
- USPTO trademark: ✅ CLEAR

**Payment path — DECIDED AND LOCKED:**
- US-only launch, Dodo Payments on Android, NO Google Play Billing
- Legal basis: Epic Games v Google US court ruling
- IS_TWA redirect code already live — redirects to quantumcube.app/app?ref=android-unlock
- Pre-redirect disclosure modal now shows before redirect fires (qc-v227)

**Account type — personal, staying personal:**
- Cannot convert to organization (read-only after creation)
- Developer name "Quantum Neuro Creations" shows prominently — fine
- 14-day closed testing required (personal account post-Nov 2023)
- Company: Quantum Neuro Creations (PTY) Ltd, reg 2019/559151/07, South Africa

---

### IMMEDIATE NEXT STEPS (new chat picks up here)

**Step 1 — CREATE APP in Play Console (doing now)**
- App name: Quantum Cube (12 chars — under 30 limit ✅)
- Type: App (not game)
- Free (NOT paid — irreversible if set wrong)
- Support email: quantumneurocreations@gmail.com (or support@quantumcube.app)
- Tick: Developer Program Policies + US export laws
- Tick: Accept Play App Signing Terms of Service
- Click Create app

**Step 2 — CRITICAL immediately after creation:**
Play Console → Release → Setup → App signing → copy "App signing key certificate" SHA-256 fingerprint → paste to Claude in new chat → Claude updates assetlinks.json + redeploys. TWA verification BREAKS without this second fingerprint.

**Step 3 — Upload AAB**
File: `android/app-release-bundle.aab` (1.66MB, already built and signed)
Go to: Testing → Closed testing → Create new release → Upload AAB

**Step 4 — Enroll External Content Links Program**
Play Console → Settings → External content links → Enroll → register quantumcube.app/app as destination

**Step 5 — Recruit 12 testers → 14-day clock starts**

**Step 6 — Fill Play Console forms (App content page)**
All in Policy and programs → App content:
- Privacy policy URL: https://quantumcube.app/privacy
- Ads: NO
- App access: "App uses magic-link auth. Enter [review email], open Gmail at gmail.com with [password], click link." (Need to CREATE review Gmail first — set has_paid=true via Claude after first sign-in)
- Target audience: 18+
- Content rating: complete IARC questionnaire (likely Everyone/Everyone 10+)
- COVID-19: NO
- News/Magazine: NO
- Health Apps Declaration: NO health functionality
- AI-generated content: NO (ElevenLabs TTS of pre-written deterministic scripts)
- Data safety form: declare email, name, DOB, purchase history (Dodo), app interactions (PostHog), crash logs (Sentry), device IDs (PostHog)

**Step 7 — Store listing**
- Short description (≤80 chars): NOT YET DRAFTED — do in new chat
- Full description (≤4000 chars): NOT YET DRAFTED — do in new chat
- Feature graphic: needs approval + commit to docs/
- Screenshots: 4–6 portrait on phone

**Step 8 — Infrastructure before go-live**
- Supabase Pro upgrade ($25/mo) — before any Android traffic
- Verify Privacy Policy explicitly names Supabase + Dodo Payments by name (PostHog + Sentry already confirmed)

---

### PLAY STORE CHECKLIST REFERENCE
Full detailed checklist with policy citations: PLAY_STORE_PREP.md (Sections 1–15)
Claude Code audit findings: PLAY_STORE_PREP.md Section 15

---

### KEY FACTS FOR NEW CHAT

| Item | Value |
|------|-------|
| Package name | app.quantumcube.twa |
| Keystore | android/quantumcube.keystore (pw in Apple Passwords) |
| AAB location | android/app-release-bundle.aab (1.66MB) |
| Live domain | quantumcube.app |
| Support email | quantumneurocreations@gmail.com |
| Supabase project | fqqdldvnxupzxvvbyvjm, eu-central-1 |
| Sentry org | quantum-neuro-creations, project: javascript, EU |
| PostHog project | 172921, EU, https://eu.i.posthog.com |
| Current SW version | qc-v227 |
| Company reg | Quantum Neuro Creations (PTY) Ltd, 2019/559151/07 |
| Payment processor | Dodo Payments (MoR) — US only launch |
| ElevenLabs voice | eleven_turbo_v2_5, stability 0.5, similarity_boost 0.75, speed 1.15 |
| account/delete URL | quantumcube.app/account/delete ✅ live |
| Trademark status | CLEAR — no USPTO registration for Quantum Cube Class 9/41 |


## 2026-05-11 Full Day — App polish, auth fixes, Supabase Pro + custom domain (Chat Claude)

**Goal:** Ship all outstanding UI/UX fixes, lock down auth, upgrade infrastructure, progress Play Store submission.

**Code commits shipped:**
- `f9f80cb` qc-v228 — fix(ui): center buttons on wide screens — `!important` override on `.calc-btn`, `.reset-btn`, `#googleSignInBtn` inside `@media (min-width:600px)`
- `5aff6fe` qc-v229 — fix(auth): CheckEmail dead end + session poller for in-app browser magic link. `_qcMagicPoller` polls getSession() every 2s on CheckEmail; `showFace(0)` fallback only when `profileRow` is null
- `9d93440` qc-v230 — fix(ui): widen Dodo checkout overlay on tablet/desktop. `_qcScaleDodoOverlay()` MutationObserver targets `#dodo-checkout-inner-div`, forces `min(520px,92vw) × min(700px,92vh)`, centred
- `da21783` qc-v231 — fix(ui): vertically centre lock paywall on tablet. `:has(> .lock-screen:not([style*="none"]))` scoped flexbox — self-disables on unlock, no impact on paid content faces
- `2324080` qc-v234 — fix(ux): clicking new numerology card immediately stops previous. Root cause: `_narrateInflight` held true for entire `playSequence` duration, silently aborting all other card taps
- `686f998` qc-v237 — fix(media): stop video + narration on face change; suppress music resume during video-to-video switches. `_qcVideoActive` flag, `pauseAllVideos()` in `showFace()`, `resumeAfterVideo` guard
- `5aff6fe→686f998` also includes qc-v233 (cancellation token `_qcNarrateGen` on all narration paths — old `finally` was clobbering new audio)
- `5626c8e` qc-v236 — fix(auth): prevent showFace(0) regression for returning users + scope poller to requested magic links only. `_qcMagicLinkRequested` flag; `profileRow` null guard
- `61fda7f` qc-v238 — fix(auth): switch Supabase client URL to custom domain `auth.quantumcube.app` (3 refs: CSP, SUPABASE_URL, NARRATE_URL)
- `715067f` qc-v239 — fix(auth): Android stuck-on-CheckEmail — visibilitychange guard (unconditional on CheckEmail), "Already verified?" escape hatch button, OTP metadata fallback (`pending_first_name/last_name/dob_*`) for Gmail CCT storage isolation

**Infrastructure done:**
- ✅ Supabase Pro upgraded — $34.62/month (quantum-cube Micro + credit offset). No more auto-pausing.
- ✅ qnc-academy Supabase project deleted — was empty (3 rows), saves $10/month
- ✅ Custom domain `auth.quantumcube.app` — Cloudflare CNAME + TXT via MCP, Supabase activated, app.html updated, Google OAuth redirect URI added (via Claude in Chrome automation)
- ✅ Supabase health check completed — RLS ✓, 6 edge functions ✓, profiles structure ✓, 38 stale rate-counter rows cleared, test account deleted, leaked-password protection enabled, URL config verified
- ✅ CONNECTORS.md created — full service registry (Cloudflare zone ID, Supabase IDs, Sentry, PostHog, GitHub, Resend, Dodo, ElevenLabs, Google OAuth)
- ✅ OPERATING_RULES.md — Golden Rules section added (5 rules: Automation First, Permanent Fixes, Proactive Improvement, Update Connectors in Real Time, One Question Max)
- ✅ CHAT_KICKOFF.md v5.1.0 — CONNECTORS.md added to mandatory boot sequence

**Play Store progress:**
- ✅ Countries/regions — South Africa + United States added to Alpha track
- ✅ 7-inch tablet screenshots — reuse 10-inch (Google doesn't validate device origin)
- ✅ Chromebook + Android XR screenshot slots — confirmed optional, skipped
- ⏳ Testers — still gathering 12 Gmail addresses
- 🔲 Preview and confirm release
- 🔲 Send to Google for review → 14-day clock

**Pending:**
- 🔲 Test Android auth fixes on device (qc-v239) — verify magic link no longer opens stuck second tab
- 🔲 Add Google OAuth client ID to CONNECTORS.md (client ID: `886533964656-j8d17l8ij6u3q0i3bc8hgusr8od28c2h.apps.googleusercontent.com`)
- 🔲 12 testers opted in → submit closed testing release
- 🔲 Create review Gmail → set has_paid=true (Supabase)

**Current HEAD:** `715067f` | **SW:** qc-v239 | **Sentry:** quantum-cube@qc-v239

## 2026-05-12 — Google Play testers + reviewer Gmail (recovered from deleted chat)

**Context:** Chat was accidentally deleted. Recovered via Supabase query + user recall.

**Done (confirmed):**
- ✅ **~15 tester emails sent** — closed testing Alpha track invites dispatched
- ✅ **Reviewer Gmail created** — `qnc.review@gmail.com` / `QNC@Reviewer2026!`
- ✅ **has_paid=true confirmed in Supabase** — profile row exists, created 2026-05-12 06:29 UTC, has_paid=true. Verified via SQL query.
- ✅ **14-day tester clock** — check Play Console for exact start date

**Still pending:**
- 🔲 Confirm reviewer credentials added to Play Console → App content → App access → "Any other instructions"
- 🔲 Confirm 12+ testers have opted in (not just invited) — Play Console shows opt-in count
- 🔲 Preview and confirm closed testing release in Play Console
- 🔲 Supabase SESSION_LOG updated (this entry)

**Current HEAD:** `715067f` | **SW:** qc-v239 | **Sentry:** quantum-cube@qc-v239

## 2026-05-12 Update — App access credentials confirmed

- ✅ **Play Console → App content → App access** updated with reviewer Gmail credentials (`qnc.review@gmail.com` / `QNC@Reviewer2026!`). Instruction name: "Google Sign-In". Confirmed via screenshot.

## 2026-05-12 — Lock screen text fix + bad push recovery (qc-v242)

**What happened:**
- Attempted to split `No Subscription · Yours Forever` onto two `white-space:nowrap` lines across all 4 lock screens (faces 3–6)
- GitHub `push_files` MCP tool silently accepted `"PLACEHOLDER"` as file content — pushed an empty app.html to production (4,373 lines → 0 lines)
- Site was broken for ~13 minutes
- Claude Code recovered: `git revert 7970b92` (restores app.html) + clean fix commit `d21c799`

**Commits:**
- `9cb79bc` — revert destructive push, restore app.html
- `d21c799` — fix(ui): split lock screen divs onto two nowrap lines; bump qc-v241 → qc-v242

**Current HEAD:** `d21c799` | **SW:** qc-v242 | **Sentry:** quantum-cube@qc-v242

**⚠️ PERMANENT RULE: Never use GitHub `push_files` or `create_or_update_file` MCP tools for files >10KB. Use Claude Code or Terminal only.**

## 2026-05-12 Afternoon — TWA payment fix, Vimeo ratings, payment strategy locked (Chat Claude)

**Goal:** Fix TWA payment flow, debug tester video issues, lock payment strategy.

### Commits this session
- `7970b92` — ⚠️ BAD PUSH (PLACEHOLDER content) — reverted immediately
- `9cb79bc` — revert: restore app.html from PLACEHOLDER
- `d21c799` — fix(ui): split lock screen "No Subscription · Yours Forever" onto two separate white-space:nowrap divs; bump qc-v241→qc-v242 (4 occurrences, faces 3/4/5/6)
- `e2ae942` — fix(twa): remove IS_TWA payment block; Dodo opens inline on TWA; bump qc-v242→qc-v243

**Current HEAD:** `e2ae942` | **SW:** qc-v243 | **Sentry:** quantum-cube@qc-v243

---

### Done

**Lock screen text fix ✅**
- Split `No Subscription · Yours Forever` into two `white-space:nowrap` divs on all 4 lock faces
- Bad push incident (PLACEHOLDER) occurred during this fix — ~13 min downtime, recovered via Claude Code revert

**TWA payment fix ✅**
- Root cause: `IS_TWA` block in `unlock()` opened external Chrome browser for payment; browser has separate session from TWA → user sees Face 0 (not signed in)
- Fix: removed entire `if(IS_TWA){...}` block — Dodo checkout now opens inline on both PWA and TWA
- Orphaned code left in place (confirmTwaRedirect, cancelTwaRedirect, twaRedirectOverlay) — cleanup deferred to pre-production pass
- IS_TWA const still defined (used at line 1092 for sessionStorage flag)
- Payment confirmed working on both PWA and TWA ✅

**Vimeo content ratings ✅**
- All 5 videos had no content rating set — Vimeo warning: "Videos without a content rating can't be watched by some viewers"
- Set all 5 to "All audiences" via Vimeo Share panel:
  - 1183086210 — Introduction ✅
  - 1183086853 — Numerology ✅
  - 1183087269 — Results Explained ✅ (auto-applied via default)
  - 1183087951 — Astrology & Horoscope ✅
  - 1183103519 — Journey Complete ✅
- Set "All audiences" as default for future videos

**Tester status**
- 16 testers invited, opt-in links sent
- Waiting for 12 to opt in → 14-day clock starts
- Videos confirmed playing on both PWA and TWA for majority of testers
- Payment working on both PWA and TWA

**ECLP investigation — decided NOT to pursue**
- External Content Links Program: US-only, 2-week review, requires API integration code changes
- Fees coming (20% on one-time purchases when Google starts charging)
- Not worth the effort given 15% Play Billing alternative

---

### 🔴 PAYMENT STRATEGY — LOCKED

| Platform | Payment method | Fee | Notes |
|---|---|---|---|
| Web app (PWA) | Dodo Payments | ~2.5% | Keep as-is, no Google involvement |
| Google Play (TWA) | Google Play Billing | 15% | Implement pre-production |

**Key facts:**
- QNC enrolled in 15% reduced service fee (confirmed Play Console notification, 9 May 2026)
- Standard rate is 30%; QNC qualifies at 15% on first $1M/year
- $17 × 15% = $2.55 to Google → developer keeps $14.45 per Play Store sale
- Google Play Billing implementation is a pre-production task — NOT needed for closed testing
- ECLP not needed — Go global from day one via Play Billing

---

### Known issues / non-blocking

**Gerda's music on TWA** — music doesn't play even when tapping music button directly
- Music files confirmed accessible (200 OK on both ambient.mp3 and bgMusic.mp3)
- Videos work for her now ✅
- Likely TWA audio policy or device-specific issue
- Non-blocking — 3 other testers confirmed everything working on regular app
- Defer investigation unless more testers report it

**CI failure email (7970b92)** — "Verify versions in sync: All jobs have failed"
- This is from the bad PLACEHOLDER commit, not current state
- Current HEAD e2ae942 at qc-v243 is correct — ignore this email

**Multi-account session clash**
- Having PWA and TWA open simultaneously causes session conflicts
- Not a code bug — just test one at a time, clear cache between switches

---

### Pending (updated)

- 🔲 **12 testers opt in** → 14-day clock starts (CRITICAL PATH — links sent, chasing)
- 🔲 **Google Play Billing implementation** (pre-production, not urgent)
- 🔲 **assetlinks.json second SHA-256** from Play App Signing (after AAB upload confirmed)
- 🔲 **Orphaned TWA code cleanup** (confirmTwaRedirect, cancelTwaRedirect, twaRedirectOverlay) — pre-production
- 🔲 **Music on TWA** (Gerda) — investigate if more testers report it
- 🔲 **ECLP** — deprioritised, Google Play Billing is the better path
- 🔲 **System upgrade + integrations** — next chat

## 2026-05-12 Evening — QI System build (Chat Claude)

**Goal:** Build the Quantum Integrator (QI) — personal Jarvis system.

**Done:**
- ✅ **Graphify installed** — knowledge graph of codebase, 175 nodes 249 edges 14 communities. `graphify update .` after code changes (no API cost).
- ✅ **NORTH_STAR.md created** — 500 customers by Aug 15, $8,500 gross, milestones, guardrails. Wired into CLAUDE.md + CHAT_KICKOFF v5.2.0.
- ✅ **ANTHROPIC_API_KEY secured** — stored in `~/.config/anthropic/key`, never hardcoded.
- ✅ **QI keys vault** — `~/.config/qi/` with chmod 700. All 4 keys stored securely via `read -rs` pattern.
- ✅ **Morning briefing** — `scripts/morning-briefing.py` + `/morning-briefing` Claude Code command. Pulls Supabase/PostHog/Sentry, gives one daily action.
- ✅ **QI Dashboard live** — `scripts/qi-server.js` + `scripts/qi-dashboard.html`. Dark sci-fi mission control at localhost:3001. Animated particle orb, live data, 30s auto-refresh.
- ✅ **All 4 keys wired:** PostHog ✓ Sentry ✓ ElevenLabs ✓ Supabase ✓
- ✅ **First real briefing:** 3 paying customers · $51 revenue · 24 sessions · 0 errors

**Current HEAD:** `a743ff6` | **SW:** qc-v243 | **Sentry:** quantum-cube@qc-v243

**QI naming convention locked:**
- QI = Quantum Integrator (the Jarvis/personal agent)
- Code = Claude Code (terminal coder)
- Claude = this chat (strategy + MCPs)

**To start QI:** `cd ~/Projects/quantumcube && node scripts/qi-server.js &` → open localhost:3001

**Pending (QI phase 2):**
- 🔲 Deepgram voice input (real-time STT so QI can hear you)
- 🔲 Overnight cron tasks (Mac Mini stays on, runs scheduled jobs)
- 🔲 War Room multi-agent dashboard
- 🔲 gstack (Garry Tan's 23-tool Claude Code setup)

## 2026-05-12 Evening — QI Voice Loop LIVE

**🎙️ QI is fully operational:**
- Owen (voice ID `giAoKpl5weRTCJK7uB9b`) speaking via ElevenLabs ✅
- Deepgram listening live via mic ✅  
- Claude processing responses ✅
- Full two-way voice conversation working ✅
- `qi` alias launches full loop from any terminal window
- `qi-dash` launches dashboard at localhost:3001
- `qi-brief` fires spoken morning briefing

**First words from QI:**
"I'm here to help drive Quantum Cube to 500 paying customers by August 2026 — we're at 3 now, so we've got work to do."

**Pending QI upgrades:**
- 🔲 Web search tool (QI can't browse internet yet)
- 🔲 gstack — Garry Tan's 23-tool Claude Code setup
- 🔲 Overnight cron tasks (cron installed, needs task definitions)
- 🔲 War Room multi-agent dashboard
- 🔲 Security layer (prompt injection protection)

## 2026-05-12 Night — QI system completion

**Done:**
- ✅ gstack wired into quantumcube project — /office-hours /review /ship /qa /cso all active
- ✅ Overnight cron (2am): qi-overnight.py — pulls Supabase/PostHog/Sentry, saves report
- ✅ Security cron (3am): qi-security.py — secrets scan, key permissions, prompt injection check
- ✅ Security score: 100/100 — all key files chmod 600, .gitignore hardened
- ✅ QI v4 voice loop: streaming sentence-by-sentence, filler words, 1.5s Deepgram endpointing
- ✅ Tavily web search wired — QI answers live questions
- ✅ All keys secured: Anthropic, Deepgram, ElevenLabs, PostHog, Sentry, Supabase, Tavily

**Cron schedule:**
- 2am: qi-overnight.py (data pull + report)
- 3am: qi-security.py (security audit)
- 7am: qi-morning-auto.sh (spoken briefing via Owen)

**Note:** QI voice has echo feedback issue — fixed with headphones (mic picks up speakers). Code cooldown + min-words + streaming all in place.

**Current HEAD:** `62ebb36` | **SW:** qc-v243

## 2026-05-12 Full Day — QI System Build (Complete Record)

**This was the biggest single session. Full QI system built from scratch.**

---

### WHAT WAS BUILT TODAY

**Infrastructure:**
- ✅ ANTHROPIC_API_KEY — secured in `~/.config/anthropic/key`
- ✅ All 7 API keys in `~/.config/qi/` chmod 600: anthropic, deepgram, elevenlabs, posthog, sentry, supabase_service_role, tavily
- ✅ Mac Mini energy: prevent sleep ON, wake for network ON, restart after power failure ON
- ✅ Bun installed (`~/.bun/bin/bun`)
- ✅ Python 3.12 installed via Homebrew (`/opt/homebrew/opt/python@3.12`)

**Graphify:**
- ✅ Installed: `pip install graphifyy` (double y)
- ✅ Wired into Claude Code via `graphify claude install`
- ✅ Graph built: 175 nodes, 249 edges, 14 communities
- ✅ God nodes: Architecture Decision Records (17), Quantum Cube Product (15), check_run_calc() (10), Dodo Payments (8)
- ✅ CLAUDE.md updated to read GRAPH_REPORT.md before file searches
- ✅ `/graphify` command in `.claude/commands/graphify.md`
- ⚠️ API key needed for full semantic extraction. Code files extracted via tree-sitter (free). Docs need ANTHROPIC_API_KEY env var.

**North Star:**
- ✅ `NORTH_STAR.md` created — 500 customers by Aug 15 2026, $8,500 gross, milestones, guardrails
- ✅ Wired into CLAUDE.md boot checklist (step 3)
- ✅ CHAT_KICKOFF v5.2.0 — NORTH_STAR.md added to mandatory boot reads

**QI Dashboard (`scripts/qi-server.js` + `scripts/qi-dashboard.html`):**
- ✅ Node.js server on localhost:3001
- ✅ `/api/briefing` — pulls Supabase customers, PostHog sessions, Sentry errors
- ✅ `/api/speaking` — POST state=true/false, dashboard polls every 500ms
- ✅ Dark sci-fi UI: Cinzel font, cyan (#0cc0df) glows, particle orb
- ✅ v2 dashboard: wider panels (330px), bigger text, revenue+days moved to right panel bottom
- ✅ Orb flares when QI speaks: faster particles, bigger glow, 3 pulsing rings, "SPEAKING" label
- ✅ Launch: `qi-dash` alias OR `node scripts/qi-server.js &` then open localhost:3001

**Morning Briefing:**
- ✅ `scripts/morning-briefing.py` — pulls all 3 sources, gives one action
- ✅ `/morning-briefing` Claude Code command
- ✅ Cron: `0 7 * * *` — auto-runs daily at 7am, speaks via Owen
- ✅ `qi-brief` alias for manual trigger

**QI Voice Loop (`scripts/qi-voice.py` — currently v4):**
- ✅ Owen voice: ElevenLabs voice ID `giAoKpl5weRTCJK7uB9b`
- ✅ Deepgram STT: nova-3, endpointing 2500ms
- ✅ Claude Haiku 4.5 for fast voice responses
- ✅ Streaming pipeline: sentence-by-sentence, first word ~1.5s after you stop talking
- ✅ Filler words: "Hmm," "Got it," "Right," mask remaining latency
- ✅ Hard mic mute via osascript: `set volume input volume 0` when Owen speaks, 100 when done
- ✅ Response buffer: 1.2s timer after last transcript — waits for full sentence
- ✅ Tavily web search: triggered on news/current events keywords
- ✅ DIXON UM-20 external USB mic confirmed as system input
- ⚠️ Voice still being refined — echo/feedback work in progress. Mic mute + buffer should resolve it.
- 🔑 Launch: `qi` alias (new terminal window after `source ~/.zshrc`)

**Overnight Automation:**
- ✅ `scripts/qi-overnight.py` — 2am cron, pulls all data, saves to `/tmp/qi-overnight-report.json`
- ✅ `scripts/qi-security.py` — 3am cron, secrets scan + key permissions + prompt injection check
- ✅ Security score: 100/100
- ✅ Cron schedule: `0 2 * * *` overnight, `0 3 * * *` security, `0 7 * * *` briefing

**gstack (Garry Tan's 23-tool Claude Code setup):**
- ✅ Installed: `git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && ./setup`
- ✅ Wired into quantumcube project via `gstack-team-init required`
- ✅ Available slash commands in Claude Code: /office-hours /plan-ceo-review /plan-eng-review /review /ship /qa /cso /retro /autoplan /browse /investigate /document-release /codex
- ✅ Playwright browser installed (~91MB, headless Chrome)

**Shell aliases (in `~/.zshrc`):**
```bash
qi          # launch QI voice loop
qi-dash     # launch dashboard + open browser
qi-brief    # speak morning briefing now
```

---

### STILL TO BUILD (from chat discussion)

- 🔲 **War Room multi-agent dashboard** — 7 named agents (Content, Analytics, Revenue, Developer etc) with task board. Start one agent at a time.
- 🔲 **Ad performance in morning briefing** — Google/Meta Ads ROAS, spend, downloads. No API integration yet.
- 🔲 **Play Store download count** — Play Console API not integrated.
- 🔲 **Overnight task instructions** — way to tell QI before bed "run X at 3am tonight"
- 🔲 **Auto-start QI server on login** — launchd plist so localhost:3001 always running
- 🔲 **NotebookLM + GWS CLI** — research layer (from hexagon image in videos)
- 🔲 **hellotrilion.ai Chief of Staff skill** — daily 3-priority briefing format
- 🔲 **Google Play Billing** — pre-production Android task
- 🔲 **12 testers opted in** — critical path to production

---

### KEY FACTS FOR NEXT CHAT

| Item | Value |
|------|-------|
| QI dashboard | localhost:3001 (run: `node scripts/qi-server.js &`) |
| QI voice | run: `qi` in new terminal |
| Owen voice ID | giAoKpl5weRTCJK7uB9b |
| Current SW | qc-v243 |
| Paying customers | 3 (as of May 12) |
| Days to goal | 95 (Aug 15) |
| Security score | 100/100 |
| Mic device | DIXON UM-20 USB external mic |
| CHAT_KICKOFF | v5.2.0 |

---

### BOOT NOTE FOR NEXT CHAT

Boot sequence is now CHAT_KICKOFF v5.2.0:
1. SESSION_LOG.md (this file, top entry)
2. PROJECT_BRIEF.md
3. CONNECTORS.md
4. NORTH_STAR.md ← NEW mandatory read

First task next chat: test QI voice with the mic mute + buffer fixes. Then War Room agent planning.

## 2026-05-13 — QI System Upgrade Session (Chat Claude)

**Goal:** Complete QI system upgrades: auto-start, security layer, Chief of Staff briefing, research layer, Play Store stats integration.

### ✅ DONE THIS SESSION

- ✅ **#6 QI auto-start on login** — launchd plist created at `~/Library/LaunchAgents/com.quantumcube.qi-server.plist`. Node path `/Users/qnc/.nvm/versions/node/v24.15.0/bin/node`. KeepAlive=true. Verified running via `launchctl list | grep qi-server`. localhost:3001 survives reboots.
- ✅ **#9 Prompt injection security layer** — `sanitize_input()` in `scripts/qi-voice.py`: 12 injection pattern classes blocked, Unicode abuse detection (>40% non-ASCII), 500-char cap, security events logged to `~/.config/qi/security.log`. Blocked inputs speak "That input was flagged and blocked." Commit `59f68f5`.
- ✅ **#8 Chief of Staff morning briefing skill** — `run_cos_briefing()` in `scripts/qi-voice.py`. 15 trigger phrases ("morning briefing", "top priorities", "start my day", etc.). Fetches live data from `/api/briefing`. Delivers exactly 3 voiced priorities. Starts "First," ends "That is your focus. Go." Commit `4b413c8`.
- ✅ **#7 Research layer** — `scripts/qi-research.py` (executable). Voice triggers: "save note", "note this down", "log this", etc. Saves to `~/.config/qi/research-notes/` as markdown. `export` command generates `~/Desktop/qi-research-export.md` for NotebookLM. Optional GDrive upload (needs `~/.config/qi/gdrive-token.json`). Wired into `respond_now()` routing. Commit `4b413c8`.
- ⏳ **#4 Play Store install count** — `scripts/qi-play-stats.py` + `qi-server.js` updated. Service account `qi-play-reporting@quantum-cube-494914.iam.gserviceaccount.com`. Key at `~/.config/qi/play-service-account.json`. Both APIs enabled: `androidpublisher.googleapis.com` + `playdeveloperreporting.googleapis.com`. Play Console invite sent with "View app information and download bulk reports" permission. Still returning 404 — permission propagation in progress (15–60 min window). Run `python3 scripts/qi-play-stats.py` to confirm when ready. Commits `2ae007b`, `896c5f5`.

**Commits this session:** `59f68f5` · `4b413c8` · `2ae007b` · `896c5f5`

**Current HEAD:** `896c5f5` | **SW:** qc-v243 | **Sentry:** quantum-cube@qc-v243 | **Paying customers:** 3 | **Days to goal:** ~94

---

### 🔴 FULL REMAINING TODO LIST

**QI System**
- 🔲 **#1** Test QI voice live — mic mute + buffer fixes committed (`9aed0ae`, `5e5736b`), needs live test
- 🔲 **#2** War Room dashboard — 7 named agents (Content, Analytics, Revenue, Developer, etc.), task board
- 🔲 **#3** Ad performance in morning briefing — Google/Meta ROAS, spend, downloads (no API yet, parked)
- ⏳ **#4** Play Store install count — run `python3 scripts/qi-play-stats.py` to confirm when Play Console permission propagates
- 🔲 **#5** Overnight task instructions — tell QI before bed what to run at 3am

**Google Play — critical path to 500 customers**
- 🔲 **#10** Confirm 12+ testers opted in — check Play Console opt-in count (not just invited)
- 🔲 **#11** Preview + confirm closed testing release in Play Console
- 🔲 **#12** Google Play Billing implementation — required before production
- 🔲 **#13** assetlinks.json second SHA-256 from Play App Signing tab
- 🔲 **#14** Test Android auth on device — qc-v239 magic link fix
- 🔲 **#15** Music on TWA (Gerda) — defer unless more testers report
- 🔲 **#16** Orphaned TWA code cleanup (confirmTwaRedirect / cancelTwaRedirect / twaRedirectOverlay)

**App / Code fixes (tester-reported)**
- 🔲 **#17** Video spacing on phone
- 🔲 **#18** "Reveal My Cube" button spacing
- 🔲 **#19** Email page buttons (Continue/Google) shift left on wide screens — centering fix

**⚠️ Infrastructure — time-sensitive**
- 🔴 **#20** Sentry trial → free tier verify — **MAY 18 DEADLINE (5 days)**
- 🔲 **#21** Google OAuth verification — still in Testing mode (only 3 users allowed)
- 🔲 **#22** Privacy Policy — verify Supabase + Dodo Payments named explicitly

**Post-launch cleanup**
- 🔲 **#23** Dedupe `.scoreboard` duplicate CSS
- 🔲 **#24** `git gc --aggressive` (repo 1.2GB)
- 🔲 **#25** Delete test profile rows from Supabase
- 🔲 **#26** Rotate leaked Dodo Test API + webhook secrets
- 🔲 **#27** Refund second Live test payment
- 🔲 **#28** DMARC `p=none` → `p=quarantine`
- 🔲 **#29** Gmail 2FA on all 3 partner accounts

**25 items remaining. Biggest urgencies: #20 Sentry (May 18), #10/#11 Play Store tester clock, #1 QI voice live test.**

---

### KEY FILE PATHS (QI system)
- QI voice: `scripts/qi-voice.py`
- QI server: `scripts/qi-server.js`
- QI dashboard: `scripts/qi-dashboard.html`
- Play stats: `scripts/qi-play-stats.py`
- Research layer: `scripts/qi-research.py`
- LaunchAgent: `~/Library/LaunchAgents/com.quantumcube.qi-server.plist`
- Keys vault: `~/.config/qi/` (all chmod 600)
- Play key: `~/.config/qi/play-service-account.json`
- Security log: `~/.config/qi/security.log`
- Research notes: `~/.config/qi/research-notes/`

### 🚀 NEXT CHAT LEAD-IN
1. Boot per CHAT_KICKOFF v5.2.0 — read SESSION_LOG → PROJECT_BRIEF → CONNECTORS → NORTH_STAR
2. **Immediate: tester-reported app issues** (new chat for this)
3. **After app fixes:** Continue upgrade list — #1 QI voice live test, #10 tester opt-in count, #20 Sentry deadline May 18


## 2026-05-13 — Session cont.

**Shipped qc-v244:**
- Bug 1: magic link / TWA poller — `_qcCheckSessionOnce` helper, 1s×15 retry burst, "I've Verified — Continue" primary btn
- Bug 2: delete button — Sentry breadcrumbs + captureMessage on silent failure paths  
- Bug 3: Clarity CSP — `blob:` added to `worker-src`, richer violation reporting
- UptimeRobot API key stored + CONNECTORS.md updated

**Pending:**
- UptimeRobot MCP connector (next session)
- Play Store link monitor (Claude Code)
- Isolated storage / Gmail CCT edge case — OTP or assetlinks deep-link (future sprint)
- Sentry trial → free tier deadline: May 18 ⚠️


## 2026-05-13 Evening — Auth flow overhaul + Anthropic billing crisis (Chat Claude + Claude Code)

**Goal:** Fix all sign-up/auth bugs discovered by real TikTok users. Also resolved Anthropic billing crisis.

---

### 🚨 ANTHROPIC BILLING CRISIS — RESOLVED

**Root cause:** `ANTHROPIC_API_KEY` in `~/.zshrc` pointed to "Codex's Individual Org". Claude Code read this env var and bypassed Max plan OAuth, billing per-token on Opus all day. ~$57 charged.

**Fixes:**
- ✅ Removed key from `~/.zshrc` + deleted `~/.config/anthropic/key`
- ✅ `claude logout` + `claude login` via OAuth — now shows "Claude Max"
- ✅ Auto-recharge OFF, $20 cap, old keys deleted
- ✅ Partial refund $24.64 received — ~$38 outstanding, resets June 1
- ✅ QI voice key moved to `~/.config/qi/anthropic_api_key` (qi-voice.py line 58 fixed)
- ✅ Claude Code set back to Opus 4.7 via `~/.claude/settings.json`
- ✅ `qc` alias added to `~/.zshrc` → `cd ~/Projects/quantumcube && claude`

---

### AUTH BUGS FIXED (qc-v264 through qc-v269)

**v264** — Email-match check in reveal short-circuit  
`if(_revealSession && _revealSession.user)` → added `.email === em` check. Prevented foreign session bypassing OTP for new emails.

**v265** — CCT guard blocking new emails (Claude Code)  
`if(qcLastMagicEmail && !_revealSession)` → added email match check. CCT guard was firing for ANY previous email, blocking new emails from reaching signInWithOtp.

**v266** — Three auth flow bugs (Claude Code)  
1. CCT isolation recovery: visibilitychange now handles Face 0 (not just CheckEmail)  
2. Email lock on sign-out: sign-out now clears qcLastMagicEmail, resets readOnly=false + opacity  
3. Profile persistence: SIGNED_IN handler now awaits saveProfileFromForm() before runCalculation()

**v267** — Email cleanliness audit (Claude Code)  
Found QC_PENDING_KEY in localStorage was persisting indefinitely → 1-hour TTL added. Was the real source of email leaking between users on shared devices.

**v268** — CheckEmail buttons all white (Chat Claude)  
Swapped both calc-btn elements on CheckEmail face to reset-btn. Prevents cyan .ready bleed from sign-up form validation affecting CheckEmail buttons.

**v269** — CCT retry loop (Claude Code)  
visibilitychange handler now retries up to 5× over 2 seconds. Fixes race condition where CCT session hadn't landed in storage by first check. Also adds restorePendingProfile() + truncated email in all Sentry breadcrumbs.

---

### SUPABASE FIX — RLS INFINITE RECURSION

**Dropped** `users_update_own_profile` UPDATE policy (had recursive subquery on `profiles` inside `profiles` update).  
**Replaced** with clean `auth.uid() = id` policy + `lock_has_paid` BEFORE UPDATE trigger.  
Has_paid column is now protected via trigger (no recursion). All profile saves working.

---

### REAL USERS TODAY

| Email | Status |
|-------|--------|
| tjaart51@gmail.com | TikTok ad user — OTP sent, never confirmed. Likely CCT bug. Magic link may be expired. |
| keyzer.pretorius@gmail.com | **PAID customer** — name=null, dob=null (profile never saved due to RLS bug). |
| madjadex@gmail.com (Jade) | Working ✅ after v269 |
| codexsorcerer@gmail.com | Test account — working after all fixes |

**All confirmed users had name=null, dob=null** — RLS recursion bug silently ate every profile save since launch. Fixed in v269.

---

### CURRENT HEAD: `052c701` | SW: qc-v269 | Sentry: quantum-cube@qc-v269

**Pending:**
- 🔲 Test v269 CCT flow on device — magic link → Gmail → return to app → should auto-advance in 1-2s
- 🔲 Follow up tjaart51@gmail.com (TikTok user) — draft recovery email
- 🔲 keyzer.pretorius@gmail.com (paid user) — profile incomplete, may need support
- 🔲 Anthropic org rename: "Codex's Individual Org" → "Quantum Neuro Creations"
- 🔲 $38.29 refund outstanding from Anthropic — resets June 1


## 2026-05-14 — Install gate polish + PWA fixes + strategic review (Chat Claude)

**Goal:** Polish the install experience — splash screen, spinner, loading states. Fix PWA splash color mismatch. Strategic review before going wide on ads.

---

### INSTALL GATE OVERHAUL (v270–v272 + manifest fix)

**v270** — Install splash + spinner  
- `#qcSplash` full-screen black overlay with QUANTUM CUBE text logo, shows for 2s on page load  
- Spinner `#qcInstallSpinner` (.install-spin) replaces Install button on tap — cyan rotating arc, "INSTALLING" label  
- 3.5s delay after `accepted` before `_qcShowInstalledState()` fires — buys time for icon to land on home screen  
- If user dismisses Chrome prompt, button is restored and spinner hidden

**v271** — Polish  
- Splash now shows `qc-icon-512.png` (120px, border-radius 24px, floating animation) instead of text logo  
- `#installGate` now has `opacity:0` by default + `.visible` class triggered via double-rAF for smooth fade-in  
- Splash and gate cross-fade together (splash fades out as gate fades in) — no hard cut  
- Spinner delay doubled to 7s (was 3.5s)

**v272 — CRITICAL BUG FIX**  
- `#qcSplash` had `display:flex` in CSS so it showed for ALL users including already-installed standalone users  
- Installed users were stuck on black icon screen forever (couldn't access the app)  
- Fix: added `if(sp) sp.style.display='none'` to the standalone/desktop early-return path in the IIFE

**manifest.json — PWA splash color**  
- `background_color` and `theme_color` changed from `#05050f` to `#000000` (pure black)  
- Eliminates the visible blue-black mismatch on the native Android PWA launch splash  
- New installs get this immediately; existing installs get it on Chrome's own manifest refresh cycle (days/weeks)

---

### STRATEGIC DISCUSSION

**Android market:** Global Android ~72%, SA ~78%. US is the exception (~43% Android, ~57% iOS). For SA + global campaigns, Android-first is correct. Plenty of addressable market.

**PWA real cons (beyond Play Store):**  
- iOS: No `beforeinstallprompt`, manual A2HS, limited push notifications pre-iOS 16.4. iPhone-heavy US market partially unreachable  
- Zero organic discovery — 100% dependent on paid/referral traffic  
- Trust gap with less tech-savvy users vs native app store listing  
- Storage can be evicted by browser; cache fragility  
- TWA audio/media restrictions  

**Readiness assessment:** Infrastructure solid enough to run paid ads now. Sentry catches issues, PostHog tracks sessions, SW handles updates silently. Auth bugs nailed (v264–v272 combined). The one risk mid-campaign is auth — now addressed.

**Upcoming focus (tomorrow):**  
- Wide + deep upgrade: AI agents/assistants, skill expansion, marketing system  
- Financial backing confirmed — ads budget available, will find best channels and go all-in  
- 12 Play Store tester opt-ins (critical path for production)  
- Google Play Billing implementation

---

### CURRENT HEAD: `ce4eb4f` | SW/Sentry: `qc-v272` | manifest: #000000

**Pending carried forward:**
- 🔴 **Sentry trial → free tier — MAY 18 DEADLINE (4 days!)**
- 🔲 Test v269 CCT flow on device (magic link → Gmail → auto-advance without close/reopen)
- 🔲 Recovery email to tjaart51@gmail.com (TikTok user, never confirmed)
- 🔲 keyzer.pretorius@gmail.com (paid user, profile empty — RLS bug pre-fix)
- 🔲 Anthropic org rename: "Codex's Individual Org" → "Quantum Neuro Creations"
- 🔲 $38.29 Anthropic refund outstanding — resets June 1
- 🔲 12 Play Store testers opted in
- 🔲 Google Play Billing implementation

## 2026-05-14 Morning — Auth confirmed + small polish queue (Chat Claude)

**Auth verdict from user:** Magic link flow confirmed working on two devices, multiple emails. Third email on same device goes stale — expected + acceptable behaviour. No fix needed.

**Polish queue (deferred — no urgency):**
- 🔲 Loading screen — user considering adding one
- 🔲 Breathing space between pages — 1-2 spots need padding/margin review


## 2026-05-14 Morning — Critical: Reveal button broken for all users (Chat + Claude Code)

**Symptom:** Reveal My Cube fires audio + haptic but app stays on Face 0. Affects all users post-reinstall. Multiple users reported.

**Investigation (Chat Claude):**
- Sentry: no JS errors in last 4h
- Supabase: operational, RLS fine
- Profiles check: 8+ users with name=null/dob=null from old RLS bug — root cause for earlier "grey button" issue, not this new one
- v273 deployed: "Welcome back" hint for users with empty profiles — email unlocked
- Identified silent throw risk in showFace() — cubeScene null-check missing

**Root cause confirmed (Claude Code):**
`showFace()` line ~2131: `cs.classList.remove('visible')` threw uncaught TypeError when `cubeScene` element was null/not-yet-rendered. Audio + haptic fire before this line — so it felt responsive — then execution stopped silently before face navigation happened.

**v274 fixes (Claude Code):**
1. Null-guard: `if(cs) cs.classList.remove/add(...)` — showFace never throws on missing elements
2. try-catch around both showCheckEmailScreen() calls in handleRevealClick
3. Sentry breadcrumbs: reveal:form-valid, reveal:show-check-email-called, reveal:otp-dispatched
4. sw.js + Sentry release synced at qc-v274

**CURRENT HEAD:** qc-v274 | All users should now be able to reveal

**Affected users still needing follow-up (name=null/dob=null):**
- rkelbrick@icloud.com
- tjaart51@gmail.com
- quinton.edwards@gmail.com
- clinton.pretorius@gmail.com
- l88040124@gmail.com
- leochrisdt26@gmail.com
- crichter12@gmail.com
- agenyaclinton6@gmail.com / agenyaclinton@gmail.com
→ All need to fill name + DOB on next open. v273 shows "Welcome back" hint.

## 2026-05-14 Full Day — Auth root cause resolved, v275–v282, Play Store milestone, DB wipe, Claude Max upgrade

**Goal:** Find and permanently fix auth root cause for closed-testing testers, get Google Play 14-day clock running, ship auth-stripped v282 for day-one tester access.

---

### 🔴 ROOT CAUSE: CCT Isolated Storage (confirmed)

Chrome Custom Tab (CCT) — the in-app browser Gmail uses to open magic links — has **completely isolated localStorage** from the main Chrome session. `getSession()` was calling into Supabase's token-refresh path, which tried to write/read `localStorage`, but the CCT session could not see the localStorage written by the main Chrome tab. Result: deadlock / silent failure. OTP emails were arriving fine; the app just couldn't recover the session after the link was clicked.

**Secondary problem:** 6 of 12 testers had stale `qc_last_magic` localStorage from previous test sessions. Old email in that key was triggering the CCT guard incorrectly.

---

### Auth overhaul — v275 through v281 (all committed + deployed)

| Version | Commit | What changed |
|---------|--------|--------------|
| v275 | `d7bb68f` | Remove email readOnly (was blocking Android input); clear stale cross-account sessions; scroll validation errors into view |
| v276 | `d1dcb2` | Add diagnostic Sentry captureMessages throughout reveal flow; add null-guards for rotateTo/applyRot; wrap showFace in try-catch |
| v277 | `6d1dcb2` | Remove stale-session guard that was clearing form via SIGNED_OUT; add pre-validation diag breadcrumb |
| v278 | `7d0e7c0` | Fix getSession() deadlock on token refresh — removed from hot path, replaced with localStorage direct-read |
| v279 | `4af11e4` | Remove getSession() from reveal hot path entirely; persist qcLastMagicEmail for cross-session continuity |
| v280 | `5ded698` | OTP code entry screen added; install gate auth bypass for direct app loads |
| v281 | `b34b8ed` | Remove emailRedirectTo from signInWithOtp — OTP-only flow (no magic link redirect that opens CCT) |
| v282 | `58c25a9` | **STRIP AUTH ENTIRELY from reveal** — name + DOB form only, no email input, no OTP, no Supabase session. runCalculation() runs immediately on Reveal tap. Payment gate blocks naturally (no session = has_paid false). |

**v282 is the right call for day-one testing.** 14-day clock started May 14; testers can use the full app (minus paid content) without any auth friction. Google Play Billing implementation is pre-production, not needed for closed testing.

---

### 🗄️ Database wipe — completed

All non-paid auth.users deleted from Supabase `fqqdldvnxupzxvvbyvjm`. Only `has_paid = true` accounts kept:

| Email | has_paid | Name |
|-------|----------|------|
| quantumneurocreations@gmail.com | true | ronnie carl kelbrick |
| booyens.michelle@gmail.com | true | Jaeger Tjaart Booyens |
| qnc.review@gmail.com | true | QNC ReviewAccount |
| keyzer.pretorius@gmail.com | true | Willem Keyzer Pretorius |

Total: 4 records. Profiles cascade-deleted automatically on auth.users delete. DB is clean.

---

### 📋 Tester CSV created

File: `/mnt/user-data/outputs/qnc_testers_emails.csv`  
12 Gmail addresses for Google Play Console closed testing import:

```
gerda.jacobs21@gmail.com
rkelbrickmail@gmail.com
carlkelbrick@gmail.com
madjadex@gmail.com
charlheyns1@gmail.com
charlheyns4@gmail.com
keyzer.pretorius@gmail.com
deswardt.ronelle@gmail.com
crichter12@gmail.com
l88040124@gmail.com
xtremeproperties24@gmail.com
noel92.nh@gmail.com
```

---

### 🎯 Google Play milestone — screenshot confirmed May 14 ~18:45 SAST

Play Console `quantumneurocreations@gmail.com` shows:

- ✅ **Publish a closed testing release** — DONE (strikethrough)
- ✅ **Have at least 12 testers opted-in to your closed test** — DONE (strikethrough)
- ⭕ **Run your closed test with at least 12 testers, for at least 14 days** — IN PROGRESS

**14-day clock started May 14, 2026. Apply for production access ~May 28.**

No tester needs to do anything daily. Nobody opts out unless they deliberately go back to the invite link and tap "Leave the program." Uninstalling does NOT opt out.

---

### 💳 Claude Max $200/month plan upgrade

Upgraded to Max $200 plan = **20× usage**. No token constraints on any future chat. This session is the first fully unconstrained session.

---

### 🩺 Health check — May 14 evening

**Sentry (23 unresolved issues):**
- Most are `reveal-diag:*` breadcrumbs (JAVASCRIPT-E/F/G/H/J/K etc.) — intentional diagnostic captureMessages added in v276 to trace the auth flow. These are NOT real errors; they're telemetry of the OTP/CCT flow that was active in v275–v281. Will resolve once breadcrumbs are cleaned from v283+.
- JAVASCRIPT-A: "profile save error: infinite recursion" — 1 user, 22 hours ago. This was the RLS recursion bug fixed in v269. The event predates the fix; not a regression.
- JAVASCRIPT-B: "For security purposes, you can only request this after 15 seconds" — Supabase OTP rate-limit hit by some testers rapidly re-tapping Reveal. Non-blocking; v282 removes auth entirely so this stops.
- JAVASCRIPT-X: "launchDodo: no session at checkout" — 1 user, 1 hour ago. Expected: v282 has no auth session, so attempting payment correctly blocks. This is intended behavior for the 14-day test period.
- JAVASCRIPT-3: "CSP violation: img-src blocked c.clarity.ms" — Microsoft Clarity beacon. Known; Clarity was deferred (ADR-011). Non-blocking.
- JAVASCRIPT-7 + JAVASCRIPT-8: Session-restore nav breadcrumbs — diagnostic messages from restore flow. Not errors.

**Action:** After v282 stabilises, resolve all `reveal-diag:*` issues as noise. Keep JAVASCRIPT-A and JAVASCRIPT-X for documentation.

**Supabase:** ✅ 4 auth.users, all has_paid=true. RLS intact. DB clean.

**UptimeRobot (24h):** ✅ 2 UP, 3 paused, 0 DOWN, 0 incidents. 100% uptime.

---

### 📋 Pending — ordered by urgency

| # | Item | Urgency |
|---|------|---------|
| 1 | 🔴 Sentry free tier verify — **MAY 18 DEADLINE (4 days)** | CRITICAL |
| 2 | Monitor tester engagement — ensure 12 stay opted in through May 28 | CRITICAL |
| 3 | Push ≥1 update during 14-day window to show active development | HIGH |
| 4 | Clean up reveal-diag Sentry breadcrumbs from code (v283+) | MEDIUM |
| 5 | Resolve JAVASCRIPT-A, JAVASCRIPT-B, JAVASCRIPT-X in Sentry | MEDIUM |
| 6 | Google Play Billing implementation (pre-production, not urgent) | MEDIUM |
| 7 | Anthropic org rename: "Codex's Individual Org" → "Quantum Neuro Creations" | LOW |
| 8 | $38.29 Anthropic refund outstanding — resets June 1 | LOW |
| 9 | Follow up: tjaart51@gmail.com (TikTok user, OTP never confirmed) | LOW |
| 10 | Follow up: keyzer.pretorius@gmail.com (paid, profile was empty pre-RLS fix — now has name) | LOW |

---

**Current HEAD:** `58c25a9` | **SW:** qc-v282 | **Sentry:** quantum-cube@qc-v282 | **Paying customers:** 4 | **DB:** 4 auth.users (all has_paid=true) | **Play Store:** 14-day clock running since May 14 → apply production May 28

> **Related:** [[PROJECT_BRIEF]] · [[DECISIONS]] · [[CONNECTORS]] · [[NORTH_STAR]]
