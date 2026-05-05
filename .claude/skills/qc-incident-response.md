# qc-incident-response

**When to use:** Sentry alert fires. Daily-health-check workflow fails. User reports a bug. Smoke test fails. Anything where production might be broken.

## Triage flow

### Step 1 — Confirm scope

Before touching code, answer:

1. **Is it actually broken?** Pull up `quantumcube.app/app` in a browser. Reproduce the issue. If you can't reproduce, the alert may be noise — see "Noise patterns" below.
2. **How many users?** Sentry → search the issue → check event count. 1 event in 24h is usually noise; 10+ events in an hour is real.
3. **What's the blast radius?** All users? Specific browser? Specific journey step? Narrow it.

```bash
# Quick check — is the cube even loading?
curl -fsS https://quantumcube.app/app | grep -oE "qc-v[0-9]+" | head -1
```

### Step 2 — Look at what changed

```bash
cd /Users/qnc/Projects/quantumcube
git log --oneline -10
git log --since="24 hours ago" --stat
```

Did anything ship recently that could cause this? If yes, suspect that commit first. Bisect if needed.

### Step 3 — Get the Sentry context

Use the Sentry MCP:
- `search_issues` for recent unresolved issues
- `get_sentry_resource` with `resourceType=issue` for full issue details (stack trace, breadcrumbs, affected users)
- `analyze_issue_with_seer` ONLY if the root cause isn't obvious — burns tokens, takes 2-5 min, but gives a code-level fix proposal

### Step 4 — Decide: roll forward or hotfix

**Roll forward** (fix in next commit) if:
- The fix is small and clear
- The bug isn't blocking the critical path (form submission, paywall, narration playback)
- Affected user count is low

**Hotfix immediately** if:
- Form submission is broken (revenue impact)
- Paywall is bypassable (revenue + IP impact)
- Narration is broken site-wide (core feature)
- Critical legal page (`/terms`, `/privacy`) returns 5xx
- Cube doesn't render at all

For hotfix path, follow `qc-release-procedure.md` but skip the "is this risky" deliberation — ship the smallest possible fix and verify with smoke test.

### Step 5 — Resolve in Sentry

After the fix is live and smoke test passes:
- Verify in Sentry that no new events have come in for the issue (wait 10-15 min minimum)
- Mark the issue as resolved with the fixing commit referenced (Sentry can auto-resolve via release if Sentry release tracking is wired up)

The auto-run discipline in `CHAT_KICKOFF.md` says reversible cloud writes are fair game — resolving a confirmed-fixed Sentry issue counts. Just do it and report.

### Step 6 — Document

If the incident was non-trivial (>10 min to diagnose, or affected >10 users):
- Append a `## Incident: <date> — <one-line>` entry to `BRIEF_ARCHIVE.md`
- Capture: what broke, how it was detected, what fixed it, what could prevent recurrence

If the recurrence-prevention is something architectural (new test, new monitoring, new invariant), add it to `DECISIONS.md` as an ADR.

## Noise patterns to suppress, not chase

These should be filtered/grouped/ignored in Sentry rather than treated as bugs:

- `Network Error` / `Failed to fetch` from offline users — real, but unactionable
- Browser extension noise (ad blockers injecting errors)
- Old browser (`SecurityError` from <iOS 15 / pre-2020 Chrome)
- `ResizeObserver loop limit exceeded` — known-benign Chrome bug

If you see one of these as the top alert, tune the Sentry rule rather than touching code.

## When NOT to act

- **Single event, never reoccurs.** Ignore.
- **Affected user is you on a test machine.** Mark as test event in Sentry.
- **You can't reproduce after 15 min of trying.** Document the symptom in BRIEF_ARCHIVE, set a Sentry watch (notify-if-recurs), move on.

## Escalation

You're solo. There's no one to escalate to. The escalation IS the documentation — write down what you tried so future-you (or future-Claude) can pick up where you left off.
