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

## FAL.AI

- **API key:** stored in `~/.config/qi/fal_api_key`
- **Account:** Quantum (quantumneurocreations@gmail.com)
- **Pricing:** pay-per-use, no subscription
- **SDK:** `pip install fal-client` (Python) · `npm install @fal-ai/client` (Node)
- **Env var:** `FAL_KEY`
- **Primary models:**
  - Images: `fal-ai/nano-banana-2` ($0.08/img, Gemini 3.1 Flash) · `fal-ai/nano-banana-pro` ($0.15/img, Gemini 3 Pro) · `fal-ai/flux-pro/v1.1` (diffusion alternative)
  - Video: `fal-ai/kling-video/v3.0/pro` ($0.112/sec, cinematic) · `fal-ai/veo3` ($0.40/sec, Google, native audio)
  - Budget video: `fal-ai/seedance-2-0` (~$0.03/sec)
- **Used for:** Head-of-Design sub-agent image generation · QI marketing agent media creation
- **Access:** One API key → 1000+ models. Swap model by changing endpoint string only.
- **Added:** 2026-05-15

## QI GMAIL

- **QI email:** `qi@qncacademy.com`
- **Google Workspace domain:** `qncacademy.com`
- **Sending name:** QI — Quantum Integrator
- **OAuth client name:** QI Email Agent (Desktop app type)
- **Client secret location:** `~/.config/qi/gmail_client_secret.json` (download from Google Cloud → Credentials)
- **Token location:** `~/.config/qi/gmail_token.pickle` (auto-created on first auth)
- **Gmail API scopes:** `https://mail.google.com/` (full access)
- **Google Cloud project:** `quantum-cube-494914` (add Gmail API + new OAuth client here)
- **Setup script:** `python3 scripts/qi-gmail.py auth` (run once, opens browser)
- **Voice triggers:** "send email to X about Y" → composes + sends · "check my email" → reads inbox aloud
- **Status:** ⏳ AWAITING SETUP — needs Google Admin user creation + OAuth credential download

### One-time setup steps (user must complete):
1. `admin.google.com` → Users → Add user → `qi@qncacademy.com` · name: QI Integrator
2. `console.cloud.google.com` → project `quantum-cube-494914` → APIs & Services → Library → Enable **Gmail API**
3. Credentials → Create → OAuth client ID → **Desktop app** → name: "QI Email Agent" → Download JSON
4. Rename downloaded file to `gmail_client_secret.json` → move to `~/.config/qi/`
5. Run: `python3 scripts/qi-gmail.py auth`  ← browser opens, sign in as qi@qncacademy.com
6. Test: `python3 scripts/qi-gmail.py test quantumneurocreations@gmail.com`

## QI BRAND

- **Theme:** Purple → pink gradient (NOT Quantum Cube cyan)
- **Gradient:** `linear-gradient(135deg, #5B64F9 0%, #9A6DE8 50%, #FF60CB 100%)`
- **Purple:** `#5B64F9` (start) · `#9A6DE8` (mid/primary)
- **Pink:** `#FF60CB` (end)
- **Background:** `#05000F` (very dark purple-black)
- **Text:** `#FFFFFF`
- **Logo file:** `assets/qi-logo.png` (transparent PNG, purple→pink QUANTUM + white script "integrator")
- **Logo use:** dashboard header, email, all QI surfaces
- **Name:** QI (short for Quantum Integrator) — never "QI Integrator"

## QI GOOGLE CLOUD PROJECT

- **Status:** ⏳ NEEDS CREATION — separate from quantum-cube-494914
- **Why separate:** QI is its own entity, not a sub-system of Quantum Cube
- **Steps to create (user):**
  1. console.cloud.google.com → New Project → name: "Quantum Integrator" → note project ID
  2. Enable Gmail API in new project
  3. Credentials → OAuth client ID → Desktop app → name "QI Email Agent"
  4. Download JSON → `~/.config/qi/gmail_client_secret.json`
- **Update this file** with the new project ID once created

## QI GOOGLE CLOUD PROJECT (confirmed)

- **Project name:** QI - Quantum Integrator
- **Project ID:** `qi-quantum-integrator`
- **Organisation:** quantumneurocreations-org
- **Billing:** My Billing Account
- **Status:** ⏳ Created — awaiting Gmail API enable + OAuth credentials

### Next steps after project created:
1. APIs & Services → Library → search "Gmail API" → Enable
2. APIs & Services → Credentials → Create → OAuth client ID → **Desktop app** → name "QI Email Agent"
3. Download JSON → rename `gmail_client_secret.json` → move to `~/.config/qi/`
4. `python3 scripts/qi-gmail.py auth`  ← one-time browser auth as qi@qncacademy.com

## QI GMAIL OAUTH (confirmed credentials)

- **Client ID:** `351155276338-fhvir238110b8h51g4mbjagqc2fmannm.apps.googleusercontent.com`
- **Client secret:** stored in `~/.config/qi/gmail_client_secret.json` (chmod 600) — DO NOT commit
- **Credential name:** QI Email Agent (Desktop app)
- **Project:** qi-quantum-integrator
- **Status:** ⏳ Awaiting Gmail API enable + first auth run
- **Next:** GCP Console → Library → enable Gmail API → then run qi-gmail.py auth

## QI GMAIL STATUS (updated 2026-05-15)

- **Authenticated as:** quantumneurocreations@gmail.com (temporary — until qi@qncacademy.com created)
- **Token:** `~/.config/qi/gmail_token.pickle` ✅ saved
- **Auth flow:** External + Testing mode, test users: quantumneurocreations@gmail.com + admin@qncacademy.com
- **TODO:** Create qi@qncacademy.com in Google Admin → add as test user → re-auth as qi@qncacademy.com → delete old token → that becomes QI's permanent sending address

## OPENAI

- **API key:** stored in `~/.config/qi/openai_api_key` (chmod 600)
- **Project:** Quantum Cube (only project on account)
- **Note:** Previous key was exposed in Cloudflare Worker `holy-leaf-e567` — revoked 2026-05-15, worker deleted
- **Usage in QI:** Not currently active — QI voice uses Anthropic (Claude). Key stored for future use.

## QNCACADEMY.COM EMAIL (clarified 2026-05-15)

- **Email provider:** Google Workspace (MX records point to aspmx.l.google.com)
- **DNS:** Cloudflare zone `d8d3fbb1bfd538f3012cfa6d14a76042`
- **Cloudflare Email Routing:** Started April 2026 but NEVER completed — disabled, MX conflict with Google. Do not use.
- **Team emails:** Google Workspace aliases under each user in Google Admin
- **qi@qncacademy.com:** Needs to be created as Google Group or alias in admin.google.com

## QI GMAIL ALIAS CLARIFICATION (updated 2026-05-15)

- `qi@qncacademy.com` is an **alias** on `admin@qncacademy.com` — NOT a separate seat
- All team emails are aliases: info · privacy · keyzer · michelle · ronnie · qi (all @qncacademy.com)
- Up to 30 aliases, zero extra cost. Set in Google Admin → User → Alternative email addresses.
- OAuth authenticates as `admin@qncacademy.com`, sends FROM `qi@qncacademy.com` as alias
- `qi@` cannot be added as GCP OAuth test user (aliases have no standalone Google Account) — doesn't matter, admin@ covers it
- **Status: ✅ FULLY OPERATIONAL — no further setup needed**

## QNC UMBRELLA ARCHITECTURE (locked 2026-05-15)

```
Quantum Neuro Creations (QNC)
├── Quantum Integrator (QI) — the OS layer for all QNC
│   ├── Supabase: currently fqqdldvnxupzxvvbyvjm (QC) — migrate when 2nd product live
│   ├── GCP project: qi-quantum-integrator ✅
│   ├── GitHub: quantum-integrator ✅
│   └── Reads all QNC projects via service role keys in ~/.config/qi/
│
├── Quantum Cube (QC) — live app, paying customers
│   ├── Supabase: fqqdldvnxupzxvvbyvjm ✅
│   └── GitHub: quantumcube ✅
│
├── QNC Academy — website built, on hold
│   └── Own Supabase when activated
│
└── Future QNC products → QI connects to each
```

**QI's role:** Central intelligence OS. Manages, monitors, and connects all QNC products.
Not a sub-system of QC — it's the umbrella layer above all of them.

**Supabase migration trigger:** When Academy activates OR a second product connects to QI
→ create dedicated QI Supabase project
→ rename keys: supabase_qc_service_role / supabase_qi_service_role / supabase_academy_service_role
→ migrate qi_memory table out of QC project

**Current technical debt:** qi_memory lives in QC Supabase. Acceptable until 2nd product.

## QI SUPABASE (own project — confirmed 2026-05-15)

- **Org:** QNC Internal (FREE) — `wumshcmyhsylcpugtshb`
- **Project name:** Quantum Integrator
- **Project ID:** `bzuvrynrjuysdgehnygh`
- **Project URL:** `https://bzuvrynrjuysdgehnygh.supabase.co`
- **Region:** eu-west-1
- **Secret key:** stored at `~/.config/qi/supabase_qi_secret_key` (chmod 600)
- **Tables:** `qi_memory` (session memory, created 2026-05-15)
- **MCP connector:** Claude.ai Supabase connector now points HERE (QI project)
- **Status:** ✅ ACTIVE_HEALTHY — writing confirmed

### QC Supabase access from QI scripts
- QI scripts still read QC data via `~/.config/qi/supabase_service_role` (direct REST, no MCP)
- Claude Code (terminal) handles any QC database queries
- MCP connector = QI only going forward

### Cleanup TODO
- `qi_memory` table still exists in QC Supabase (fqqdldvnxupzxvvbyvjm) — 1 test row, harmless
- Drop it next time QC Supabase is accessible: `DROP TABLE IF EXISTS qi_memory;`

---

## QI SUPABASE — UPDATED 2026-05-15 (supersedes old entry above)

> Old free org `wumshcmyhsylcpugtshb` (bzuvrynrjuysdgehnygh) DELETED. Everything now under QNC org.

- **Org:** Quantum Neuro Creations — `ybhwpcakkaveapdztnrs` (SAME org as quantum-cube)
- **Project:** Quantum Integrator — `zhvcmxtgvrogxnvqauus`
- **URL:** `https://zhvcmxtgvrogxnvqauus.supabase.co`
- **Region:** eu-west-1
- **Anon key:** stored at `~/.config/qi/supabase_qi_secret_key` (chmod 600)
- **DB connection string:** `~/.config/qi/supabase_qi_db_url` (transaction pooler + IPv4, psycopg2)
- **Tables:** `qi_memory`
- **MCP connector:** points to QNC org — covers BOTH quantum-cube AND quantum-integrator forever. No more org switching.
- **Cost:** $10/month (separate project under QNC Pro org)
- **Status:** ✅ ACTIVE_HEALTHY — full chain tested 2026-05-15

### QNC Supabase final architecture
```
QNC org (ybhwpcakkaveapdztnrs) — one MCP connection
├── quantum-cube       fqqdldvnxupzxvvbyvjm  (eu-central-1) ← QC app data
└── quantum-integrator zhvcmxtgvrogxnvqauus  (eu-west-1)    ← QI OS data
    └── Tables: qi_memory
    └── Future: revenue_events, marketing_tasks, agent_logs...
```
Academy → add as 3rd project in same org when ready.
