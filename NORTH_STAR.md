---
tags: [core, north-star]
---
# QUANTUM CUBE — NORTH STAR

```
CREATED:  2026-05-12
OWNER:    Ronnie / Quantum Neuro Creations
HORIZON:  August 15, 2026 (95 days from creation)
```

---

## 🎯 THE PRIMARY GOAL

> **500 paying customers by August 15, 2026.**

- Price: $17 one-time, lifetime access
- Gross at goal: $8,500
- Current paying customers: check Supabase `profiles` WHERE `has_paid = true`
- Platform split: Web (Dodo Payments) + Android TWA (Google Play Billing — pre-production)

This is a realistic, honest target. It could go faster. It won't go slower if we stay focused.
The goal is NOT a vanity metric — it's 500 real humans who paid real money for a real product.

---

## 📍 WHERE WE ARE RIGHT NOW (May 12, 2026)

| Item | Status |
|------|--------|
| Web app live | ✅ quantumcube.app |
| Payments live | ✅ Dodo Payments, $17 one-time |
| Android APK built | ✅ app-release-bundle.aab ready |
| Play Store identity verified | ✅ |
| Closed testing (Alpha) | ⏳ 16 invited, need 12 opted in |
| 14-day testing clock | ⏳ starts when 12 opt in |
| Google Play Billing | 🔲 pre-production task |
| Marketing push | 🔲 blocked until Play Store live |

**Critical path to 500:** Play Store live → marketing push → first 500.
**Current bottleneck:** 12 testers opting in → 14-day clock → production access.

---

## 🔢 THE MATH

| Scenario | Customers | Revenue |
|----------|-----------|---------|
| Conservative | 500 | $8,500 |
| Optimistic | 1,000 | $17,000 |
| Moonshot | 5,000 | $85,000 |

**Daily run rate needed to hit 500 by Aug 15:** ~5–6 new paying customers/day
(assumes marketing kicks in post-Play Store launch, mid-June at earliest)

**Acquisition cost assumption:** if ads cost $3–5 per conversion, 500 customers = $1,500–$2,500 ad spend.
Fully covered by revenue. Profitable from day one.

---

## 🧭 WHAT MATTERS MOST — IN ORDER

1. **Unblock Play Store launch** — every day of delay is a day without Android traffic
2. **Get 12 testers opted in** — this starts the 14-day clock, nothing else does
3. **Marketing content running** — Michelle's organic social + first paid ad test
4. **Monitor and react** — PostHog conversions, Sentry errors, Dodo revenue daily
5. **Fix anything that causes drop-off** — auth bugs, UI issues, payment failures

---

## ❌ WHAT DOES NOT MATTER RIGHT NOW

- New product features (Compatibility, Year Ahead, Tarot) — post-500
- Subscription tier — post-month-6 review
- Rebuilding or refactoring anything that works — only fix what's actively broken
- Academy or HR product — separate project, separate context
- Vanity metrics (impressions, likes) — only conversions count

If a task doesn't move the needle on 500 customers by Aug 15, it goes to the backlog.

---

## 📊 DAILY INTELLIGENCE (what the morning briefing should surface)

Every morning, the AI assistant should report:
1. **Revenue last 24h** — Dodo Payments webhook data / Supabase `has_paid` count delta
2. **New sessions** — PostHog: unique visitors to `/app` in last 24h
3. **Conversion rate** — sessions → paying (PostHog funnel)
4. **Sentry errors** — any new issues blocking users
5. **Play Store status** — tester opt-in count, days until production access
6. **One recommendation** — the single highest-leverage action for today

---

## 🔒 GUARDRAILS FOR THE AI ASSISTANT

These rules apply in every session, every suggestion, every plan:

1. **Always ask: does this help get to 500 by Aug 15?** If no, flag it as post-goal work.
2. **Play Store is the unlock** — prioritise anything that unblocks Android launch.
3. **Don't suggest features** unless an existing customer specifically requested it.
4. **Don't suggest rebuilds** of things that work. Ship fixes, not rewrites.
5. **Revenue data beats gut feel** — always pull actual numbers before making recommendations.
6. **One thing at a time** — never give more than 3 action items. Force prioritisation.

---

## 🗓️ MILESTONES

| Date | Target |
|------|--------|
| May 26 | 12 testers opted in, 14-day clock started |
| June 9 | 14-day clock complete, production access request submitted |
| June 16 | Play Store live (Android) |
| June 30 | First 50 paying customers |
| July 15 | 150 paying customers |
| August 1 | 350 paying customers |
| **August 15** | **500 paying customers** ✅ |

---

## 🚀 THE DAILY QUESTION

> *"What is the single most important thing I can do today to get closer to 500 customers by August 15?"*

The AI assistant's job is to answer this question every morning with real data, not guesswork.

---

> **Related:** [[SESSION_LOG]] · [[PROJECT_BRIEF]] · [[MARKETING_PLAYBOOK]] · [[CONNECTORS]]
