Generate the QI morning briefing for Quantum Cube. Pull live data from all sources, then deliver it as a spoken briefing followed by one action recommendation.

## Step 1 — Paying customers (Supabase)
Run this SQL via the Supabase MCP (project: fqqdldvnxupzxvvbyvjm):
```sql
SELECT
  COUNT(*) AS total_paid,
  COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '24 hours') AS new_today,
  COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '7 days') AS new_this_week
FROM public.profiles
WHERE has_paid = true;
```

## Step 2 — Revenue calculation
- Revenue to date: total_paid × $17
- Daily run rate needed: (500 - total_paid) ÷ days_remaining_to_aug_15
- Days remaining to August 15 2026: calculate from today's date

## Step 3 — Sessions (PostHog)
Query PostHog project 172921 (EU, https://eu.i.posthog.com) for:
- Unique sessions on quantumcube.app/app in the last 24h
- Pageview count on /app in the last 24h
Use the PostHog MCP insight query or HogQL:
```sql
SELECT count(DISTINCT session_id) as sessions, count() as pageviews
FROM events
WHERE event = '$pageview'
  AND properties.$current_url LIKE '%quantumcube.app/app%'
  AND timestamp >= now() - INTERVAL 1 DAY
```

## Step 4 — Errors (Sentry)
Query Sentry org: quantum-neuro-creations, project: javascript
- Count of NEW unresolved issues in last 24h
- If any new issues exist, name the top one

## Step 5 — Play Store tester status
Read SESSION_LOG.md from the Obsidian vault and report:
- Current tester opt-in count (target: 12)
- Days until production access is eligible (14 days after 12 opt in)

## Step 6 — Compose and deliver the briefing
Format as a QI spoken briefing. Terse, direct, no fluff:

---
**QI MORNING BRIEFING — [DATE]**

Revenue: $[X] total · [N] paying customers · [N] new today · [N] this week
Goal tracker: [N] of 500 · [N] days to Aug 15 · need [X]/day to hit target
Sessions: [N] unique sessions on /app yesterday
Errors: [N] new Sentry issues — [name top one or "all clear"]
Play Store: [N]/12 testers opted in · [status of 14-day clock]

**Today's one action:** [single highest-leverage task based on the data]
---

The one action must be chosen from this priority order:
1. If testers < 12 → "Chase [N] more tester opt-ins — this is the only thing that starts the 14-day clock"
2. If Sentry has new blocking errors → "Fix [error name] — it's costing conversions right now"
3. If daily conversion rate is below target → "Review the funnel — [sessions] sessions but only [N] conversions yesterday"
4. If everything is healthy → "Run one paid ad test — you're on track, now scale"
