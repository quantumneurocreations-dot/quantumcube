Load context for the narration fix workstream and report current state.

Background: Quantum Cube uses ElevenLabs for audio narration. The narrate Edge Function at 
https://fqqdldvnxupzxvvbyvjm.supabase.co/functions/v1/narrate is version 27, actively monitored 
by UptimeRobot (keyword: "Method not allowed" on GET → confirms function is alive).

PostHog telemetry was added in qc-v211 to measure the fix:
- narrate_api_requested — fired when fetchNarration() is called
- narrate_api_succeeded — fired on successful blob creation (includes latency_ms)
- narrate_api_failed — fired on error (includes error detail)
- narrate_audio_played — fired when audio actually plays

Two PostHog insights waiting for before/after data:
- https://eu.posthog.com/project/172921/insights/buiaXjHa (API health)
- https://eu.posthog.com/project/172921/insights/AHB7Ci6u (latency p50/p95/p99)

Current state: read the narrate Edge Function source to understand the issue:
```bash
cat /Users/qnc/Projects/quantumcube/supabase/functions/narrate/index.ts
```

Then report: what the function does, what might be causing failures, and proposed fix approach.
Ask the user to confirm before making any changes to the Edge Function.
