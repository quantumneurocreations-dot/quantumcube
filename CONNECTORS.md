# QUANTUM CUBE — CONNECTORS & SERVICE REGISTRY

```
VERSION: 1.0.0
CREATED: 2026-05-11
PURPOSE: Single source of truth for all connected services, IDs, and operational
         details. Read at every boot alongside SESSION_LOG + PROJECT_BRIEF.
         UPDATE THIS FILE immediately when new service details are discovered.
```

---

## GOLDEN RULE — AUTOMATION FIRST

> Before asking the user to do ANYTHING in an external service, check if a
> connected MCP can do it. DNS change? Use Cloudflare MCP. Database query?
> Use Supabase MCP. If the MCP exists and the action is reversible — just do it.
> Never walk the user through manual steps when automation is available.

---

## CLOUDFLARE

- **Account ID:** `52dcfe9cdb207bed6ccc2321946b678c`
- **Account email:** quantumneurocreations@gmail.com
- **MCP:** `Cloudflare:execute` (load via tool_search "Cloudflare DNS")
- **Zone:** `quantumcube.app`
  - Zone ID: `837ceb26db877564cf5355e37b1cc316`
  - Nameservers: kelly.ns.cloudflare.com / thomas.ns.cloudflare.com
  - Plan: Free
- **Key DNS records (as of 2026-05-11):**
  - `quantumcube.app` → GitHub Pages (A records)
  - `auth.quantumcube.app` → CNAME → `fqqdldvnxupzxvvbyvjm.supabase.co` (proxied: OFF)
  - `_acme-challenge.auth.quantumcube.app` → TXT (Supabase domain verification)
  - `send.quantumcube.app` → Resend email sending subdomain
  - `resend._domainkey.quantumcube.app` → TXT (DKIM)
  - `_dmarc.quantumcube.app` → TXT (DMARC)
- **Proxy rule:** Auth/Supabase subdomains MUST be grey cloud (proxied: false)

---

## SUPABASE

- **Org ID:** `ybhwpcakkaveapdztnrs`
- **Org email:** quantumneurocreations@gmail.com
- **Plan:** Pro ($25/month base)
- **MCP:** `Supabase:execute_sql` + other tools (load via tool_search "supabase database")

### quantum-cube (PRODUCTION)
- **Project ID:** `fqqdldvnxupzxvvbyvjm`
- **Region:** eu-central-1 (Frankfurt)
- **Postgres:** 17.6
- **Status:** ACTIVE_HEALTHY
- **Custom domain:** `auth.quantumcube.app` (configured 2026-05-11)
- **Tables:** `profiles` (RLS on), `narrate_rate_counters` (RLS on, deny-all)
- **Edge Functions (6):** narrate · delete-account · export-data · dodo-webhook · dodo-create-session · resend-events
- **All functions:** verify_jwt=false (manual JWT handling)
- **Auth providers:** email (magic link) + Google OAuth
- **Site URL:** https://quantumcube.app/app
- **Redirect URLs:** https://quantumcube.app/app · https://quantumcube.app/app.html · https://quantumcube.app/**

### qnc-academy
- **Status:** DELETED 2026-05-11 (was bevaepokvavzmykjmhda, eu-west-1)
- When rebuilding Academy: create new project in same org

---

## SENTRY

- **Org slug:** `quantum-neuro-creations`
- **Project slug:** `javascript`
- **Region:** EU
- **Release tag format:** `quantum-cube@qc-vNNN` (must match sw.js cache version)
- **MCP:** load via tool_search "sentry errors"

---

## POSTHOG

- **Project ID:** `172921`
- **Region:** EU
- **Host:** `https://eu.i.posthog.com`
- **Asset host:** `eu-assets.i.posthog.com`
- **Public client API key:** `phc_sXjrkSUy6SAFddX69V53HGEegVKPUpRjpUEsERF6wcVk` (safe to commit — client-side)
- **MCP:** available in connectors

---

## GITHUB

- **Org:** `quantumneurocreations-dot`
- **Repo:** `quantumcube`
- **Auth:** qncacademy@icloud.com
- **MCP:** GitHub (custom connector at https://api.githubcopilot.com/mcp/)
- **Note:** Requires 'Claude Github MCP Connector' GitHub App installed

---

## RESEND

- **Domain:** `quantumcube.app`
- **Sending subdomain:** `send.quantumcube.app`
- **Region:** eu-west-1 (data residency)
- **MCP:** load via tool_search "resend email"
- **DNS records already in Cloudflare:** DKIM + SPF + DMARC all configured

---

## DODO PAYMENTS

- **Region:** EU
- **Webhook handler:** `dodo-webhook` Edge Function (Supabase)
- **Session creator:** `dodo-create-session` Edge Function (Supabase)
- **Payment amount:** $17 one-time
- **MCP:** load via tool_search "dodo payments"

---

## GOOGLE CLOUD CONSOLE

- **OAuth client:** configured for quantumcube.app
- **⚠️ ACTION NEEDED:** When Supabase custom domain (auth.quantumcube.app) is fully
  active, update Google OAuth authorized redirect URIs to include the new domain.
  Current redirect still points to fqqdldvnxupzxvvbyvjm.supabase.co — update to
  auth.quantumcube.app/auth/v1/callback

---

## ELEVENLABS

- **Voice model:** `eleven_turbo_v2_5`
- **Settings:** stability 0.5, similarity_boost 0.75, speed 1.15
- **Exception:** welcome.mp3 uses speed 1.0
- **MCP:** ElevenLabs Agents MCP App

---

## CONNECTOR UPDATE PROTOCOL

When any new service detail is discovered (zone ID, project ID, API key, config
value), update this file immediately in the same session. Do not wait.
This file is the memory that prevents asking the user things we already know.

---

## GOOGLE CLOUD CONSOLE (updated 2026-05-11)

- **Project:** Quantum Cube (`quantum-cube-494914`)
- **OAuth client name:** `Quantum Cube Web Client`
- **Client ID:** `886533964656-j8d17l8ij6u3q0i3bc8hgusr8od28c2h.apps.googleusercontent.com`
- **Authorised JS origins:** `https://quantumcube.app`
- **Authorised redirect URIs:**
  - `https://fqqdldvnxupzxvvbyvjm.supabase.co/auth/v1/callback` (keep as fallback)
  - `https://auth.quantumcube.app/auth/v1/callback` (custom domain, added 2026-05-11)
- **MCP:** No direct MCP — use Claude in Chrome (`tabs_context_mcp` → navigate → `computer`) to automate dashboard changes


## GOOGLE PLAY BILLING

- **Service fee:** 15% (enrolled in reduced fee program, confirmed 9 May 2026)
- Standard rate is 30%; QNC qualifies for 15% on first $1M/year
- **Strategy:** Web app uses Dodo Payments; Google Play TWA will use Google Play Billing at 15% (pre-production task)
- ECLP not needed — Play Billing covers global distribution cleanly

## QI VOICE

- **QI Voice:** Owen · voice ID `giAoKpl5weRTCJK7uB9b` · model `eleven_turbo_v2_5` · stability 0.5 · similarity_boost 0.75 · speed 1.0
- **Narration Voice:** Valory · voice ID `VhxAIIZM8IRmnl5fyeyk` — Quantum Cube app narration only, never use for QI

## TAVILY

- **API key:** stored in `~/.config/qi/tavily_api_key`
- **Free tier:** 1,000 searches/month
- **Used for:** QI web search (live news, prices, current events)

## DEEPGRAM

- **API key:** stored in `~/.config/qi/deepgram_api_key`
- **Model:** nova-3, endpointing 2500ms
- **Used for:** QI voice input (speech-to-text)

## QI SYSTEM

- **Dashboard:** localhost:3001 (`node scripts/qi-server.js &`)
- **Voice:** `qi` alias in terminal
- **Briefing:** `qi-brief` alias
- **Owen voice ID:** giAoKpl5weRTCJK7uB9b (ElevenLabs)
- **Mic device:** DIXON UM-20 USB (system default input)
- **Keys vault:** `~/.config/qi/` (chmod 600 all files)
- **Crons:** 2am overnight / 3am security / 7am briefing

## UPTIMEROBOT

- **Account:** quantumneurocreations@gmail.com
- **Main API key:** `u3481167-eff9708257dbdf0694cc4cb3` (stored in `~/.config/qi/uptimerobot_api_key`)
- **Status page:** https://stats.uptimerobot.com/azO4bPUJJQ
- **MCP:** available in UptimeRobot dashboard (Integrations & API → MCP) — wire up next session
