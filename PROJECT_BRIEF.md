---
tags: [core, brief]
---
# QUANTUM CUBE — PROJECT BRIEF
---
tags: [core, brief]
---
# QUANTUM CUBE — PROJECT BRIEF
---
tags: [core, brief]
---
# QUANTUM CUBE — PROJECT BRIEF

**Version: v48 | Last Updated: May 15, 2026**

> **v48 update note (May 15, 2026 — Play Console audit + OTP fixes v300–v305, Chat Claude):** Full Play Console credential policy audit completed — all 10 declarations in Actioned tab, Need attention empty. App Access instructions updated to explain name/DOB/OTP flow + bypass URL. v300 recovery bump (Claude Code used --no-verify on Sentry filter — NEVER allowed, rule added to OPERATING_RULES). v301: OTP timeout recovery + cyan full-screen spinner overlay. v302: session restore fixed (15 users affected, JAVASCRIPT-7) — validates profile name+dob before runCalculation, _qcSessionRestored guard. v303: spinner was visible by default on OTP load + button showed "Verifying" before anything typed — both fixed, spinner resets on face entry. v304: ROOT FIX for stuck spinner — stopped racing slow Supabase SDK Promise (30s+), now races SIGNED_IN event (~1s) instead; _qcOtpVerifying flag prevents double-processing; finally block guarantees spinner always hidden. v305: Paste Code button added — clipboard API reads copied code, strips non-digits, fills + auto-verifies if 6 digits found. **Sentry:** 3 stale issues resolved, OTP rate-limit filter broadened. **DB:** rkelbrickmail@gmail.com confirmed. **Next session:** SMS OTP via Twilio + sign-up flow restructure (Name/DOB only → Reveal → SMS or Email choice → OTP). **Post-launch backlog:** Play Integrity API, Huawei AppGallery. **HEAD: `d9aeb58`, SW: qc-v305, APP: qc-v305 ✅ in sync.**

