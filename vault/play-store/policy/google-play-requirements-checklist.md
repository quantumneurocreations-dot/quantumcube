---
tags: [play-store, reference, android]
---
# Google Play — Full Requirements Checklist for Quantum Cube

Last reviewed: 2026-05-10. Source: Google Play Help Center docs provided in chat.

---

## TESTING TRACKS — STATUS

### Key rule for accounts created after Nov 13, 2023:
⚠️ Must complete testing requirements before production access. This applies to us.

| Track | Testers needed | Data Safety form needed? | Status |
|-------|--------------|--------------------------|--------|
| Internal test | Up to 100, available within minutes, FREE for testers | NOT required | 🔲 Not started |
| Closed test | Min 12 testers, 14-day gate | REQUIRED | 🔲 Waiting on identity verification |
| Production | After 14-day closed test | REQUIRED | 🔲 Blocked |

**Recommended path:** Start internal test first (no data safety form needed, instant) → then closed test with 12 testers → then production.

---

## DATA SAFETY FORM — What Quantum Cube collects/shares

### Data we COLLECT (must declare):
| Data type | Purpose | Required/Optional |
|-----------|---------|-------------------|
| Email address | Magic link auth, welcome email | Required |
| User IDs (Supabase UUID) | Account management | Required |
| Name (first name) | Numerology calculation + narration | Required |
| Date of birth | Numerology calculation | Required |
| App interactions (PostHog events) | Analytics, app functionality | Required |
| Crash logs (Sentry) | Diagnostics/crash reporting | Required |

### Data we SHARE (must declare):
| Third party | Data shared | Counts as "sharing"? |
|-------------|------------|----------------------|
| PostHog (EU) | App interactions/analytics | No — service provider |
| Sentry (EU) | Crash logs, device info | No — service provider |
| ElevenLabs | Name + numerology text for narration | Yes — third party processing |
| Resend | Email address for welcome email | No — service provider |

### Security practices to declare:
- ✅ Data encrypted in transit (HTTPS/Supabase)
- 🔲 Account deletion mechanism — **MAY BE MISSING from app** — users must be able to request account deletion from WITHIN the app AND via website

---

## APP CONTENT PAGE — Action items

| Item | Status | Notes |
|------|--------|-------|
| Privacy policy URL | ✅ Done | https://quantumcube.app/privacy |
| Ads declaration | ✅ Easy | Declare "No ads" |
| App access instructions | 🔲 Todo | Provide test login credentials for Google reviewers |
| Target audience | 🔲 Todo | Adults only — no children |
| Content rating questionnaire | 🔲 Todo | Numerology/astrology app — must complete IARC questionnaire |
| Data safety form | 🔲 Todo | Complete after identity verification |
| Entertainment disclaimer | 🔲 Todo | "For entertainment purposes only" text in-app |

---

## 🚨 CRITICAL GAPS IDENTIFIED

### 1. Account Deletion Mechanism (REQUIRED)
Google requires apps that let users CREATE accounts to also let users REQUEST DELETION.
- Must be accessible from within the app
- Must be accessible outside the app (website)
- Must delete associated user data from Supabase
- **Action:** Add "Delete my account" option in profile/settings area + add deletion request form/link at quantumcube.app

### 2. Data Safety Form
Required before closed testing track goes live. Must declare email, name, DOB, app interactions, crash logs.

### 3. Test Credentials for Reviewers
Google reviewers need login credentials to access app. Must provide in App Access section of Play Console.

### 4. Content Rating
Must complete IARC questionnaire. Numerology/astrology likely gets a "Everyone" or "Teen" rating — no violence, no mature content.

---

## TESTING STRATEGY RECOMMENDATION

**Start internal test NOW** (doesn't need data safety form):
1. Once identity verified → Play Console → Create app → Testing → Internal testing
2. Add up to 100 testers via email list
3. Upload AAB → publish to internal track (live within minutes)
4. Share opt-in link with testers

**Then closed test** (14-day gate):
- Needs data safety form completed first
- Need 12+ testers opted in
- 14-day clock starts when first tester installs

→ [[PLAY_STORE_PREP]] · [[android]] · [[PROJECT_BRIEF]] · [[data-safety-form]] · [[closed-testing-track]] · [[identity-verification]]
