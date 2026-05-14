---
tags: [core, brief]
---
# QUANTUM CUBE — PROJECT BRIEF
---
tags: [core, brief]
---
# QUANTUM CUBE — PROJECT BRIEF

**Version: v47 | Last Updated: May 14, 2026 (Wednesday night)**

> **v47 update note (May 14, 2026 night — auth rebuild v283–v299 + full Play Console audit, Chat Claude):** Full auth rebuilt from scratch across v283–v294. Root cause of v282 strip confirmed: CCT localStorage isolation + `getSession()` deadlock. New flow: OTP-only (no Google OAuth, no magic links). Email → 6-digit code → direct REST PATCH to save profile (bypasses JS client). v293 stripped Google Sign-In entirely (GSI, hash recovery, CSP entries all removed). v294 added Play Store reviewer bypass: `?review=qncreview2026` skips auth, grants full paid access. v295 fixed impossible DOB dates (Feb 31, etc.). v296 replaced 6 individual OTP boxes with single hidden input (`autocomplete="one-time-code"`, type=tel) + 6 visual display divs — standard Stripe/WhatsApp autofill pattern. v297–v298 added glass backdrop to all buttons matching `var(--glass)` from `.glass-card`. v299 fixed "Back to Sign Up" single-line + OTP screen bottom padding. **Play Console full audit completed:** Policy status clean, all 10 App Content declarations complete, App Access updated (OTP explained + bypass URL for reviewers), Data Safety updated (OAuth unchecked — Google sign-in removed), Store listing Live with all assets, Store settings complete, App Integrity auto-protection ON + Google signing ON. **DB check:** `madjadex@gmail.com` (Jade Crystal) confirmed successful OTP flow tonight. **14-day clock:** Started May 14 (Day 1) → apply for production May 27 → approval target May 28 (birthday). **Post-launch backlog added:** Play Integrity API (cracked APK prevention, 1 Claude Code session), Huawei AppGallery (400M users, half-day task, same APK). **HEAD: `5f0e75e`, SW: qc-v299, APP: qc-v299 ✅ in sync.**

