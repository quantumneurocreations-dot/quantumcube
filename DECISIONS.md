# Quantum Cube — Architecture Decision Records (ADRs)

Append-only log of significant decisions during development. When you find
yourself wondering "why did we do X this way?" — grep here first.

Format adapted from Michael Nygard's ADR template. Each entry is a snapshot
of context + decision + consequences AT THE TIME, not a moving target.
Don't edit old entries — add new ones that supersede if the call changes.

When to add an ADR:
- A decision that took >15 minutes of consideration
- A choice between two real alternatives where defaults wouldn't apply
- Anything that constrains future work (tech, vendor, design pattern)
- Anything you'd want to re-explain to a new team member in 6 months

When NOT to add an ADR:
- Bug fixes, small refactors, dependency bumps
- "We picked X because it was the obvious choice"

---

## ADR-001 — Dodo Payments as MoR processor

**Date:** 2026-04-29
**Status:** Accepted
**Supersedes:** N/A

### Context
Quantum Cube needs payment processing globally. Pre-launch we considered:
- Stripe: needs us to handle Merchant of Record (VAT/GST, fraud, chargebacks per region)
- Paddle: ruled out April 29 — see BRIEF_ARCHIVE.md "Why Paddle was ruled out"
- LemonSqueezy / FastSpring: viable MoR alternatives but less momentum
- Dodo Payments: full MoR, JS overlay SDK, webhook signature verification

### Decision
Use Dodo Payments. Full MoR — they handle global tax + fraud + chargebacks.

### Consequences
- Zero per-region compliance work for us
- Slightly higher fees vs raw Stripe, offset by zero compliance overhead
- We're on Dodo's allow-list of accepted business categories
- One-time payment model for v1 (no subscription)
- DODO_MODE constant in `docs/app.html` + matching MODE in `dodo-create-session/index.ts` + Supabase secrets must all flip together (fragile area, see brief)

---

## ADR-002 — GitHub Pages for hosting

**Date:** 2026-04-17
**Status:** Accepted

### Context
Static HTML + service worker site. Options: GitHub Pages, Vercel, Cloudflare Pages, Netlify.

### Decision
GitHub Pages serving from `/docs` on `main` branch, custom domain `quantumcube.app` via Cloudflare DNS.

### Consequences
- Free forever, unlimited bandwidth
- Auto-deploy on every push to `main` (~60s rebuild)
- HTTPS via Let's Encrypt, auto-renewed
- No serverless functions on the static host (which is fine — Supabase Edge Functions handle that)
- Can't add CI gates on the deploy itself (Pages just builds; no pre-deploy test step). Mitigate via pre-commit hook (`00a6314`) + smoke test (`fc479a0`) + GitHub Actions daily health check.

### Note (May 5, 2026)
Vercel project also exists at `prj_WKo5JwtJ02CGBVsyqbDAORQbQpDy` and has been auto-deploying every commit as a parallel chain. Decision deferred — may use as Academy site or backup deploy target.

---

## ADR-003 — Single-HTML-file architecture for app.html

**Date:** 2026-04 (pre-launch refactor)
**Status:** Accepted

### Context
The Quantum Cube app is small enough to fit in one HTML file (~350 KB after asset cleanup). Two approaches:
- Monolithic single file with inline JS + CSS
- Split into many files with module loader

### Decision
Single `docs/app.html` with inline JS + CSS.

### Consequences
- One HTTP request for the whole app (good for PWA cache priming)
- No build step required
- Edits use `str_replace` against precise anchors — see kickoff doc for HTML editing rules
- No tree-shaking — every byte gets shipped to every user
- File is too big to read whole-file in one tool call; greppy edits are mandatory
- Must NEVER reintroduce base64 assets (10.8MB cleanup reduced from 11MB to ~350KB)

---

## ADR-004 — RLS column-level guard on profiles.has_paid

**Date:** 2026-04 (locked) / 2026-05-05 (re-affirmed)
**Status:** Accepted

### Context
The paywall is the entire revenue model. Need to prevent client-side mutation of `has_paid` even if the JWT is somehow exfiltrated and used for unauthorized PATCH attempts.

### Decision
RLS UPDATE policy on `public.profiles` includes a column-level guard:

```sql
WITH CHECK (
  (SELECT auth.uid()) = id
  AND has_paid = (SELECT has_paid FROM public.profiles WHERE id = (SELECT auth.uid()))
)
```

The new row's `has_paid` must equal the existing value — clients cannot flip it. Only service role (Edge Functions invoked by webhooks) can mutate.

### Consequences
- If a customer's JWT leaks, attacker can read their profile (per SELECT policy) but cannot grant themselves paid access
- `dodo-webhook` Edge Function uses service-role key (bypasses RLS) to flip `has_paid = true` after payment confirmed
- Any future schema change touching `profiles` UPDATE policy must preserve this guard — flagged in brief as fragile area
- Re-verified May 5, 2026 via Supabase advisor + manual SQL inspection

---

## ADR-005 — Magic-link + Google OAuth, no passwords

**Date:** 2026-04
**Status:** Accepted

### Context
Auth method choice for a consumer app. Options: passwords, magic links, OAuth, passkeys, mix.

### Decision
Email magic-link via Supabase Auth (custom Resend SMTP) + Google OAuth. No passwords at all.

### Consequences
- Zero password-related security surface — no leaks, no resets, no rotation, no HaveIBeenPwned worry
- Supabase advisor's "Leaked Password Protection Disabled" warning is moot for us
- Higher delivery sensitivity to email — magic links must arrive promptly (mitigated by Resend custom SMTP)
- Magic-link UX has a known quirk: opening from Gmail's internal browser breaks session continuity. Documented in kickoff PWA stickiness section.
- May add Sign in with Apple later for iOS App Store compliance (Phase 8)

---

## ADR-006 — Sentry on EU region, free tier, error monitoring only

**Date:** 2026-05-04
**Status:** Accepted

### Context
Need production error monitoring. Sentry vs Honeybadger vs Bugsnag vs Datadog vs Rollbar.

### Decision
Sentry, EU region (`o4511330222604288.ingest.de.sentry.io`), free Developer tier.
Error monitoring only — Session Replay, Performance Tracing, Application Metrics all DISABLED to stay within 5k errors/month free quota.

### Consequences
- 5k errors/month free is plenty at our scale (averaging ~2 per release based on May 4 data)
- Will revisit upgrade path if we hit 80% of quota in any 30-day window
- Sentry release tag (`quantum-cube@qc-vNNN`) MUST stay synced with SW version — pre-commit hook enforces this
- CSP violation listener forwards as Sentry warnings — paid for itself within hours by catching 2 CSP gaps
- Business trial expires May 18, 2026 — must verify no surprise billing post-downgrade

---

## ADR-007 — Brief / Archive / Kickoff three-doc structure

**Date:** 2026-05-04 (formalized)
**Status:** Accepted

### Context
Long-running project + multiple Claude sessions + human stakeholders means context preservation across chats is critical.

### Decision
Three-doc system:
- `PROJECT_BRIEF.md` — current operational state (what's live, current line refs, fragile areas, what's next). Versioned vNN.
- `BRIEF_ARCHIVE.md` — lossless append-only history. Every session entry, every lesson, every decision context.
- `CHAT_KICKOFF.md` — protocol for starting any new chat. How Chat Claude operates, role split with Cursor, golden rules.

Plus this `DECISIONS.md` for ADR-style "why we chose X" snapshots.

### Consequences
- Brief + archive must update in the SAME commit (caught as near-miss May 4 PM)
- Brief stays lean by moving condensed-out content to archive, never to git history alone
- Kickoff is small and stable — only changes when the protocol genuinely shifts (e.g., v36 → v37 added auto-run discipline + handoff protocol)
- New Claude sessions read brief + kickoff at start, archive only when they need historical context

---

## ADR-008 — Email-only alerting (defer Telegram/Slack)

**Date:** 2026-05-05
**Status:** Accepted

### Context
Pre-launch we considered Telegram, Slack, Discord, or SMS for routing Sentry + UptimeRobot alerts. Telegram had best phone-first UX but required a Cloudflare Worker translator (Sentry has no native Telegram). Discord had native Slack-compatible webhooks but adds another app for the user. Email is built-in to all alerting platforms.

### Decision
Email-only alerting. Default Sentry email alerts + UptimeRobot email contact + GitHub Actions built-in failure email.

### Consequences
- Zero new infrastructure to maintain
- Gmail mobile app push gives effectively-instant phone notifications
- No webhooks to debug, no Workers to deploy, no rate limit risk
- Re-evaluate when alert volume exceeds ~20/month (current rate is ~2/month)
- Cloudflare Worker code for Sentry → Telegram already drafted (`sentry-telegram-worker.js`) and parked for future use

---

## ADR-009 — Cloudflare orange cloud OFF for apex + www

**Date:** 2026-05-05
**Status:** Accepted

### Context
Cloudflare DNS for `quantumcube.app` shows apex + www CNAMEs to `quantumneurocreations-dot.github.io` with the proxy disabled (DNS-only, gray cloud). User asked whether this is wrong and should be fixed. Considered enabling proxy for CDN, WAF, bot fight mode, hidden origin IP, and analytics.

### Decision
Keep orange cloud OFF (proxy disabled). Apex + www remain DNS-only on the GitHub Pages CNAME chain.

### Consequences
- GitHub Pages handles HTTPS via Let's Encrypt with HTTP-01 challenge against the live CNAME target. With Cloudflare proxy ON, that challenge would be intercepted by Cloudflare's edge, breaking auto-renewal of the GH Pages cert.
- We get zero CDN/WAF/bot-mgmt benefit from Cloudflare at the runtime layer for the website itself — GH Pages already provides global CDN free.
- Cloudflare still provides DNS resolution, email routing, and DNSSEC for the zone.
- Revisit triggers: (a) sustained traffic where GH Pages CDN insufficient, (b) actual abuse/attack where WAF would help, (c) need to hide origin IP for security reasons. None apply at current scale (~9 users).
- If we enable proxy later, must migrate cert handling to Cloudflare Universal SSL with proper DNS-01 challenge OR reconcile GH Pages cert renewal flow first.

### Alternatives considered
- Enable proxy with SSL mode "Full (strict)" — risks breaking cert auto-renewal as above
- Selective proxy (e.g., only `cdn.quantumcube.app` subdomain) — adds complexity, no real benefit yet
- Move off GitHub Pages to Cloudflare Pages or Vercel — unnecessary churn for non-issue

---

## ADR-010 — DMARC stays `p=none` for 30-60 day observation period

**Date:** 2026-05-05
**Status:** Accepted
**Supersedes:** N/A

### Context
DMARC TXT record at `_dmarc.quantumcube.app` is currently set to `v=DMARC1; p=none;` (created Apr 18). User asked whether this should be strengthened to `p=quarantine` or `p=reject`. Resend domain is verified, DKIM/SPF aligned and verified, but Cloudflare email routing forwards `*@quantumcube.app` to `admin@qncacademy.com` — forwarded mail can fail SPF alignment in some receiver implementations.

### Decision
Stay at `p=none` (observation only) for 30-60 days post-launch. Re-evaluate based on Resend delivery logs + any quarantine/bounce signals.

### Consequences
- Receivers report DMARC alignment failures via aggregate (`rua=`) reports if we add an aggregate address — currently no `rua=` set, so we get no observation data. **Optional improvement:** add `rua=mailto:admin@qncacademy.com` to the existing record to start collecting reports without changing the policy.
- Risk of phishing impersonation is low at our scale (zero brand recognition yet) but increases as we grow.
- Bumping to `p=quarantine` prematurely could quarantine legit mail forwarded through Cloudflare email routing if SPF doesn't align cleanly.
- Re-evaluate triggers: (a) 30-60 days post-launch with clean delivery, (b) any phishing attempt against the brand, (c) sufficient mail volume for aggregate reports to be statistically meaningful.

### Alternatives considered
- `p=quarantine` immediately — risk of false-quarantining legit forwards, no observation data first
- `p=reject` — too aggressive for a domain with zero reputation history
- Keep `p=none` indefinitely — leaves us permanently unprotected against impersonation

---

## ADR-011 — Microsoft Clarity deferred (project type mismatch)

**Date:** 2026-05-05
**Status:** Accepted

### Context
User signed up for Microsoft Clarity to add session-replay-style analytics to `quantumcube.app`. May 5 PM browser audit revealed the existing Clarity project (`wmb8y97pls`) was created with platform type "Mobile" — the Setup page only offers install instructions for iOS, Android, Flutter, React Native, Cordova, and Ionic. There is no Website install option for this project type. The dashboard's filters use Tablet/Mobile device classes, confirming Mobile-only flavor.

Quantum Cube is a PWA running in a web browser, not a native mobile app. Empirical test confirmed (`curl -s https://www.clarity.ms/tag/wmb8y97pls` on May 5 PM): Microsoft Clarity's backend serves a tag that explicitly logs `console.warn('Data from this session is not being collected by Microsoft Clarity because the provided project id is not a Clarity Web project')`. Web data is REJECTED at the Clarity backend for Mobile-typed projects — the project type lock is a hard restriction, not just a UI hint.

### Decision
Defer Clarity entirely until post-launch traffic justifies the analytics spend. When justified, create a NEW Clarity project with platform type "Website" and wire the standard web JS snippet into `docs/app.html` `<head>`.

### Consequences
- No session replay or heatmap analytics available pre-launch.
- At current scale (~9 users), Clarity provides no meaningful signal anyway.
- The existing Mobile project ID `wmb8y97pls` can be retained for future native app shipping (Phase 5a/5b/5c) when we wrap the PWA via Bubblewrap or PWABuilder.
- Wire-up plan when triggered: (1) create Website Clarity project, (2) add CSP allow-list for `https://www.clarity.ms https://*.clarity.ms` to script-src + connect-src in `docs/app.html` CSP meta, (3) inject the snippet AFTER Sentry init (so Sentry catches Clarity errors), (4) bump SW version, (5) gate behind cookie-consent before EU push (Phase 5b).

### Alternatives considered
- Use the Mobile project ID with the web snippet anyway — EMPIRICALLY DISPROVEN May 5 PM, Clarity backend explicitly rejects web data for Mobile projects (see Context above).
- Wire Clarity now even at minimal traffic — noise > signal at <100 sessions
- Use a different analytics tool (Posthog, Plausible, Fathom) — deferred along with Clarity decision; revisit together at scale

---

## ADR-012 — DMARC ramped to `p=quarantine; pct=25` with aggregate reporting

**Date:** 2026-05-05
**Status:** Accepted
**Supersedes:** ADR-010

### Context
ADR-010 (May 5 morning) decided to keep DMARC at `p=none` for 30-60 days observation post-launch. By May 5 evening, however, the Tier 1 security audit revealed:
- ADR-010's noted optional improvement ("add `rua=` to start collecting reports") was not yet done, so we'd been getting zero observation data despite being in observation mode.
- We can ramp via `pct=25` (partial enforcement) without committing to full enforcement, getting most of the benefit while preserving safety net.
- Cloudflare email routing catch-all (`*@quantumcube.app` → `admin@qncacademy.com`) means a `dmarc@quantumcube.app` rua address requires no new mailbox — reports will route to admin@ automatically.

Receivers report DMARC alignment failures via aggregate reports if `rua=` is set. Without a rua, we'd be enforcing blind.

### Decision
Update `_dmarc.quantumcube.app` TXT record from `v=DMARC1; p=none;` to:

```
v=DMARC1; p=quarantine; pct=25; rua=mailto:dmarc@quantumcube.app
```

Applied via Cloudflare DNS PATCH on record id `e4c164849cbe1153783624c130d44223` on May 5 evening.

### Consequences
- **Partial enforcement live:** 25% of failing mail will be quarantined by receivers. 75% still gets a pass while we monitor.
- **Aggregate reports flow:** receivers now send daily XML reports to `dmarc@quantumcube.app`, which the Cloudflare catch-all forwards to `admin@qncacademy.com`. Reports show legit senders + alignment failures.
- **Ramp path:** after 2 weeks of clean reports, bump `pct=100`. After another 2 weeks clean at `p=quarantine; pct=100`, evaluate `p=reject`.
- **Risk:** if a legit forwarder has SPF misalignment, 25% of forwarded mail gets quarantined at receiver. Mitigated by partial pct.
- **Supersedes ADR-010:** the 30-60 day observation timeline is shortened because we're using partial-pct enforcement as the observation mode rather than zero-enforcement.

### Alternatives considered
- Add `rua=` only, keep `p=none` — collects reports but provides no actual protection. Rejected: we have data + low risk.
- Jump straight to `p=quarantine; pct=100` — risk of quarantining legit forwarded mail at scale. Rejected: pct=25 is safer.
- Jump to `p=reject` — too aggressive for a domain still building reputation. Rejected.

---

## ADR-013 — PostHog adopted as product analytics layer

**Date:** 2026-05-05
**Status:** Accepted

### Context
ADR-011 (May 5 PM) deferred Microsoft Clarity due to project-type mismatch (Mobile-only, can't use for web), and noted "deferred along with Clarity decision; revisit together at scale" for PostHog/Plausible/Fathom alternatives. By May 5 evening, the deferred decision was revisited and resolved.

The team needs **product analytics** (funnel + autocapture click events + person-level identification) separately from **error monitoring** (Sentry, already live) and **uptime monitoring** (UptimeRobot, already live). Without product analytics, we have zero data on user behavior (face-by-face dropoff, button clicks, payment funnel friction).

Options reconsidered:
- **PostHog:** open-core, EU residency available, free tier 1M events/month, autocapture + custom events + funnels + session replay (paid), API rich enough to identify paid users by Supabase user_id.
- **Plausible:** privacy-first, pageviews + UTM only, no person-level events, no funnels.
- **Fathom:** similar to Plausible.
- **Microsoft Clarity (for web):** session replay strong, but requires creating a new Website-typed Clarity project (existing Mobile project locked).
- **Mixpanel / Amplitude:** mature but heavier integration, more expensive past free tier.

### Decision
Adopt **PostHog EU** (project 172921, host `https://eu.i.posthog.com`). Wire client-side snippet into `docs/app.html` AFTER Sentry init, BEFORE Supabase client. Production-only gate (`location.hostname !== "quantumcube.app"` short-circuits init). Public client API key embedded in code (safe by design — client-side token).

### Consequences
- Free tier: 1M events/month, easily covers our scale for 12+ months.
- EU residency keeps data co-located with Supabase EU + Sentry EU + Resend EU — simpler GDPR/POPIA story.
- Autocapture is on — click events on every interactive element captured automatically without per-element instrumentation.
- Person ID currently anonymized (e.g., `019df970-22b0-...`). `posthog.identify(user_id)` wiring deferred to next session — will gate on `has_paid=true` to focus signal on real customers.
- CSP allow-list updated: `eu.posthog.com` and `eu-assets.i.posthog.com` added to script-src + connect-src.
- Re-evaluation: at scale or if we want session replay, evaluate PostHog Cloud paid tier vs Microsoft Clarity Website project (would need to create a new one per ADR-011).

### Alternatives considered
- **Plausible / Fathom:** rejected — no person-level events, no funnels.
- **Microsoft Clarity Website project:** deferred (ADR-011 keeps Clarity on the back burner; if we want session replay, revisit then).
- **No analytics layer:** rejected — we need behavior data before scaling spend.

---

## ADR-014 — GitHub branch protection on `main` (solo-dev tier)

**Date:** 2026-05-05
**Status:** Accepted

### Context
Until May 5 evening, `main` had zero branch protection. GitHub UI confirmed via `gh api repos/.../branches/main/protection` returning HTTP 404 ("Branch not protected"). Risks:
- Accidental `git push --force` rewriting history (most realistic threat for solo dev pushing on a tired Friday).
- Accidental branch deletion via UI fat-finger.
- Non-linear merges introducing merge commits we'd have to chase down.

Standard branch-protection "best practices" assume team workflows with PRs and required status checks. Our workflow is **direct push to main, multiple times per day, solo**. Requiring PRs would break the operating model.

### Decision
Apply minimum-viable branch protection via gh API `PUT /repos/.../branches/main/protection`:

```json
{
  "required_status_checks": null,
  "enforce_admins": true,
  "required_pull_request_reviews": null,
  "restrictions": null,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false
}
```

### Consequences
- **Force-push to main: BLOCKED.** Even by repo owner. The forcing function is the feature.
- **Branch deletion of main: BLOCKED.** Even by repo owner.
- **Linear history required.** Direct pushes are inherently linear, so no friction added.
- **`enforce_admins=true`:** rules apply to Ronnie too. If a real emergency requires force-push, the path is: temporarily disable protection in repo Settings → Branches, do the force-push, re-enable. Friction is intentional.
- **No PR requirement:** direct `git push origin main` continues to work exactly as before.
- **No required status checks:** these enforce only on PR merges anyway, and we don't use PRs. CI workflows still run on every push and email on failure.
- Verified post-application: `git push origin main` from this session worked without any change in flow.

### Alternatives considered
- **Heavy protection (require PR + reviews + status checks):** would block direct push to main, breaking solo workflow. Rejected.
- **Light protection (only block force-push, no enforce_admins):** owner can still force-push. Rejected — the forcing function applies to owner too or it's theatre.
- **Use GitHub Rulesets (newer mechanism):** more flexibility but classic branch protection covers what we need with simpler API. Defer rulesets until we need their extra features.
- **No protection (status quo):** rejected — no cost to enabling force-push block, real downside to leaving it off.

---

## ADR-015 — ElevenLabs API key UI semantics (Key ID = working credential)

**Date:** 2026-05-05
**Status:** Accepted

### Context
During the May 5 evening secrets-leak audit, `.supabase-env` was suspected to contain a wrong value for `ELEVENLABS_API_KEY` (a 64-char hex string starting `18b...`, ending `3d2e`) because:
1. ElevenLabs UI shows the key value masked as `••••••d3be` — a different last-4 from what the "Copy Key ID" button produces.
2. The 64-char raw-hex format resembles a SHA-256 hash, not the typical `sk_<hex>` pattern used by similar APIs (Resend, Stripe, Anthropic, etc.).
3. There appeared to be a paste-mismatch story plausible from zsh history (a verification hash possibly substituted for the real key during setup).

This led to an investigation under the false assumption that "Copy Key ID" returns a public identifier and that the real secret was different and probably lost.

### Decision
The 64-char hex value labeled "Key ID" in the ElevenLabs settings UI **IS** the working API credential. The masked `••••••d3be` display in the UI is a different visual representation (likely a public account-tied portion or a JWT subset) of the same logical credential. Production narrate has been authenticating correctly using this value all along — present in both `.supabase-env` (local) and the Supabase Edge Function secret (prod).

**Going forward:** when investigating ElevenLabs key issues, do NOT assume the UI's "Key ID" wording implies it's just an identifier. It IS the credential. Verify by empirical signal (does the function authenticate against ElevenLabs?) before assuming the stored value is wrong based on format-pattern intuition.

### Consequences
- No `.supabase-env` change needed; existing value is correct.
- No Supabase Edge Function secret change needed; production already has the working value.
- No key rotation needed for ElevenLabs (the leak audit's target was Dodo — that rotation IS done, see brief v40).
- Future audits: format-pattern intuition (`sk_` prefixes, fixed-length hex looks suspicious) is a weak signal for ElevenLabs specifically. Trust the production-works check first.
- The 64-hex value is still sensitive — treat as any API key: gitignored, scrubbed from shell history, rotated if exposed.

### Alternatives considered
- **Regenerate key to get a "proper" `sk_<hex>` format:** rejected — ElevenLabs doesn't let you choose key format, regeneration would invalidate the working prod credential, and would force re-configuring the per-key permission scope list (model access, voice cloning, etc.) for no functional gain.
- **Continue investigating the UI for a hidden "real" key:** rejected — empirical evidence (narrate works in prod) outweighs format-pattern hypotheses.

---

## ADR-016 — SEO meta-tag strategy (10-tag minimum, single shared OG image)

**Date:** 2026-05-06
**Status:** Accepted

### Context
Independent audit on May 6 found that 9 marketing pages (`/`, `/privacy`, `/terms`, `/disclaimer`, `/popia`, `/ip`, `/security`, `/refund`, `/contact`) had only `<title>` tags. Adding meta tags raises a real question: which ones? Open Graph protocol has 30+ optional fields, Twitter Cards has its own set, schema.org JSON-LD has many more. Adding everything bloats every page and creates a maintenance burden when titles/descriptions change.

User explicitly asked: "We're obviously not gonna add all of them. There's just too many, and some of them not even relevant. So let's just discuss the specifics."

### Decision
Adopt a **10-tag minimum** that covers all major social/search platforms via Open Graph as the primary source plus a single Twitter declaration for the `summary_large_image` card layout. Use a **single shared OG image** (`/qc-icon-512.png`, the white CUBE logo on starfield) across all pages.

The 10 tags per page:

1. `<title>` — already present
2. `<meta name="description">` — search snippet + social fallback
3. `<meta name="robots" content="index,follow">` — was ambiguous before
4. `<link rel="canonical">` — duplicate-content prevention
5. `<meta property="og:title">` — primary social headline
6. `<meta property="og:description">` — primary social subtext
7. `<meta property="og:url">` — canonical URL the share resolves to
8. `<meta property="og:image">` — preview image (shared, see below)
9. `<meta property="og:type">` — `website` for landing, `article` for legal pages
10. `<meta name="twitter:card" content="summary_large_image">` — Twitter falls back to og:* values for everything else

Per-page customization is **only**: title, description, og:type, canonical URL. Implemented as a Python list of tuples in the deploy script — adding a new page is one row.

### Tags deliberately skipped

| Tag | Why skipped |
|---|---|
| `og:image:width` / `og:image:height` / `og:image:alt` | Optional, not required. Most scrapers measure the image themselves. |
| `og:site_name` | Title already says "Quantum Cube". |
| `og:locale` | Defaults to `en_US`, which is correct. |
| `twitter:title` / `twitter:description` / `twitter:image` | Twitter falls back to og:* values when absent (saves 3 tags per page). |
| Schema.org JSON-LD (Organization, Product, etc.) | Overkill for a 9-page site. Could revisit if rich-snippet visibility becomes a marketing priority. |

### Single shared OG image rationale

When a user shares 3 different links to the site in one chat (e.g., the landing, the refund policy, the contact page), all 3 previews look unified rather than mismatched — visual consistency reinforces brand identity. Easier to maintain (one asset to update). Per-page hero images would be ~9× more work for marginal gain.

If a future blog post or marketing page needs its own preview image, override is one line in the deploy script's PAGES list.

### Consequences

- All 9 pages now share-preview cleanly on WhatsApp, iMessage, Twitter/X, LinkedIn, Facebook, Slack, Discord
- Search engines have unambiguous signals (robots, canonical, description on every page)
- Bloat avoided: no per-page maintenance burden when title/description change
- Per-page override path is open if a specific page needs different metadata in future

### Alternatives considered

- **Add full OG block (15-20 tags) on every page:** rejected — image dimensions and alt text are inferred by scrapers, and `twitter:*` tags duplicate the og:* values when both are present. Bloat for marginal gain.
- **Per-page custom OG images:** rejected — visual inconsistency in shared chats, ~9× the asset maintenance, no measurable share-rate uplift expected at current traffic.
- **Schema.org JSON-LD for rich snippets:** rejected — premature for current traffic. Revisit if Google Search Console shows organic traffic growth that justifies the optimization work.

---

## ADR-017 — Stack sweep (May 8 audit): analytics depth + email pipeline + canonical skill

**Date:** 2026-05-08
**Status:** Accepted

### Context

After the May 5–7 GitHub MCP integration and Chat/Code split, Ronnie asked for a proactive audit of what else could improve the QNC operating stack. Audit identified one major instrumentation gap, several connected-but-underutilized tools, and one missing alerting layer. This ADR captures the full sweep as one decision because the actions are interlinked (each ships within hours of the others, all from the same audit).

### Decision

**SHIPPED today (May 8):**

1. **Microsoft Clarity installed across all 11 user-facing pages.** Project `wmc5lrewut`. CSP extended on each page for `https://*.clarity.ms`. Bumped `qc-v208` → `qc-v209`. Commit `f52fcb6`. Heatmaps + session recordings now flowing.

2. **PostHog deeply instrumented.** Diagnosed: 30-day data showed only `$pageview` / `$autocapture` / `$pageleave` firing (zero custom product events). Added three funnel events with `try`/`catch` guards: `cube_calculation_started` (after `showFace(1)` in `runCalculation`), `payment_initiated` (in `launchDodo` after session check), `payment_completed` (in `syncUnlockFromProfile` on `unpaid → paid` transition, which also calls `posthog.identify(user.id)` for retention analysis). Created **Cube Conversion Funnel** insight (`AuQW0re4`) attached to existing dashboard `662076`. Bumped to `qc-v210`. Commit `6fb6b26`.

3. **Resend welcome email pipeline wired.** Created audience "Quantum Cube Customers" (id `d9ba37bf-57f3-4e9b-929c-2bac5c2e856d`). Updated `dodo-webhook` Edge Function to: capture `has_paid` before update (idempotency guard), update `has_paid = true` (existing), only on unpaid → paid transition add customer to audience and send welcome email via Resend API. Welcome email matches brand voice (premium / mystical-grounded), HTML + plain text, from `welcome@quantumcube.app`, reply-to `quantumneurocreations@gmail.com`. Graceful failure: missing `RESEND_API_KEY` logs and skips, never breaks the webhook. Deployed. Commit `14e4210`. **User action pending:** add `RESEND_API_KEY` to Supabase Edge Function secrets.

4. **Canonical Quantum Cube skill created.** New `.claude/skills/quantum-cube/SKILL.md` with proper frontmatter (`name`, `description`) for skill auto-discovery. Indexes the existing canonical docs (`PROJECT_BRIEF`, `CHAT_KICKOFF`, `MARKETING_PLAYBOOK`, `DECISIONS`, `BRIEF_ARCHIVE`, the existing `.claude/skills/qc-*.md` playbooks). Encodes operating principles: surface boundary, auto-run discipline, boot sequence reference, "buddy" address, direct/opinionated voice. Captures full May-2026 tooling stack snapshot (every connected service with IDs and current state). Brand voice condensed reference. Architecture quick-reference (app flow + critical anchors). Forward note that this is the QNC template — fork for Academy / HR product. Commit `1f71cb3`.

**FORMALLY DEFERRED (with triggers to revisit):**

| Item | Trigger to revisit |
|---|---|
| **Linear migration** from `BRIEF.md`-based work tracking | Post-launch + start of second QNC product (Academy or HR), where multi-product backlog overhead justifies the migration cost |
| **Vercel** — keep MCP connection but do not migrate Cube. Audit unused Cube project on Vercel dashboard | Start of second product if it's React/Next.js with edge runtime needs |
| **Cloudinary** — image hosting + transforms | Start of Nano Banana asset pipeline when image volume justifies the CDN+transform layer |
| **Resend reactivation / birthday / broadcast campaigns** | When Michelle is set up on the email-marketing tooling and has copy strategy |
| **PostHog post-purchase survey** | Once `payment_completed` event is verified flowing from real users (week-1 post-launch) |
| **UptimeRobot** monitors at `/`, `/sw.js`, `/functions/v1/narrate` | Immediate (Ronnie to log in, then driven via Chrome) — same-week followup |

### Consequences

- **Conversion funnel now measurable.** Drop-off between any two of the four steps tells us where to focus. Before today: blind from `$pageview` to revenue.
- **Welcome email unblocked.** First paying customer post-`RESEND_API_KEY` setup gets the brand-voiced welcome automatically. Audience starts populating for future broadcasts.
- **Canonical skill establishes the pattern** for QNC's multi-product operating system. Sibling products inherit operating principles + tooling conventions for free.
- **Idempotency is now part of the webhook contract.** Welcome email won't dupe on Dodo retries — guarded by previous `has_paid` lookup.
- **Three observability layers active:** Sentry (errors), PostHog (product), Clarity (UX). Sufficient for launch. UptimeRobot adds the fourth (uptime) when Ronnie completes setup.
- **Three formal defers stay parked** with explicit triggers — no risk of them rotting on a list.

### Alternatives considered

- **Build all the surveys, broadcasts, and reactivation emails today:** rejected — needs copy strategy from Michelle; today's foundation is the right scope.
- **Migrate to Vercel for Cube:** rejected — current GH Pages + Cloudflare stack is fine for static; Vercel earns its slot only when an upcoming product needs serverless edge runtime.
- **Add Stripe alongside Dodo as backup payment processor:** rejected — Dodo handles global Adaptive Currency, no incident has justified the migration overhead.
- **Cursor / Codex / Obsidian / 21st.dev / Stitch / Remotion / Nano Banana now:** all rejected or parked in earlier audits this week. Today's sweep stayed focused on extracting value from already-connected tools rather than adding new ones.

---

## ADR-018 — Stack hardening sweep (May 8 PM): Resend webhook → Sentry, narrate analytics, skill v1.1.0

**Date:** 2026-05-08
**Status:** Accepted

### Context

ADR-017 (May 8 AM) shipped the welcome-email pipeline but left two adjacent gaps: (1) no observability on what happens AFTER Resend sends the email — bounces, complaints, and delivery delays were going unmonitored, and (2) the existing narrate path (the only credit-burn surface in the app) had zero product analytics, so an upcoming narration fix would have no before/after telemetry. Same chat day also surfaced a recurring process pattern worth codifying: the user is a verbal/speech-to-text user, and option pickers (`ask_user_input_v0` widgets) create friction that simple inline questions don't. Vercel preview deploys were on the audit list and worth a real look. Crash recovery: the AM chat was killed mid-session by a Mac permission prompt, exposing that there's no live working narrative file the next chat can pick up from.

### Decision

**SHIPPED today (May 8 PM, seven commits `094cb78` → `e26d591`):**

1. **Resend dedicated key + welcome pipeline unblocked** (`094cb78`). Created Resend API key `quantum-cube-dodo-webhook` (id `5b36c8df-645e-4a77-bc25-a060ad22b161`) scoped to the welcome-email flow. Stored in Apple Passwords + set as Supabase secret `RESEND_API_KEY`. Closes the "User action pending" line from ADR-017.

2. **6th Edge Function deployed: `resend-events`** (`723b2d5`). Receives Resend webhooks via Standard Webhooks signature verification (`standardwebhooks@1.0.0`). Subscribed to `email.bounced`, `email.complained`, `email.delivery_delayed`. Forwards each to Sentry as JSON via the Store API: bounced → warning, complained → error, delayed → info. Other event types (delivered/opened/clicked) get 200-acked but never forwarded — they'd burn Sentry quota with zero actionable signal. **Fail-closed on missing secret:** if `RESEND_WEBHOOK_SECRET` is unset, the function returns 503 rather than accepting unverified webhooks. Webhook id `2a5c62b4-7e5c-42eb-bdeb-fbe56bcdc8f9`. Tested 400 (missing headers) + 401 (bad signature) before going live.

3. **UptimeRobot Narrate monitor** (`803021425`). Keyword check on the live narrate Edge Function URL, looking for the `Method not allowed` string that GET requests should produce. Status page at `https://stats.uptimerobot.com/azO4bPUJJQ` rebranded "Quantum Cube — Status" with QC logo (qc-icon-192) + favicon (qc-favicon-32) + homepage URL `https://quantumcube.app`. Custom CNAME `status.quantumcube.app` deferred (paid tier on UptimeRobot — not worth $5.50/mo for the cosmetic).

4. **PostHog narrate instrumentation** (`e5467d5`, qc-v210 → qc-v211). Four new events instrumented in `fetchNarration()` and `startNarrationFromUrl()`:
   - `narrate_api_requested` — `text_length` only, never the actual narration content (privacy)
   - `narrate_api_succeeded` — `latency_ms` + `size_bytes` of the audio blob
   - `narrate_api_failed` — `status` (HTTP), `error` truncated to <=200 chars, `latency_ms`, `reason` (`http_error` or `network_error`)
   - `narrate_audio_played` — filename basename, `source: prerecorded`

   Two saved+favorited PostHog insights created via MCP: "Narrate — API health" (`buiaXjHa`, all four events 14-day Trends) and "Narrate — API latency p50/p95/p99" (`AHB7Ci6u`, latency_ms percentiles). Project annotation marks the qc-v211 deploy on every chart so before/after for the upcoming narration fix is a vertical line on the timeline. Pre-commit hook validated SW + Sentry release sync, smoke test 13/13 PASS post-deploy.

5. **Vercel preview deploys reconsidered — SKIPPED.** Audit conclusion: single-HTML PWA on GitHub Pages doesn't earn what Vercel costs in workflow change. Vercel's value proposition (preview URLs per branch, edge runtime, framework conventions) all assume a build step, multi-page architecture, or serverless functions. Cube has none of those — it's one HTML file plus a service worker, deployed via `git push`. Better future move when local-dev friction shows up: a one-line `python3 -m http.server 8000 -d docs/` script. Vercel MCP connection stays available for sibling QNC products that may earn the slot.

6. **Canonical skill bumped 1.0.0 → 1.1.0** (`094cb78`, three new sections):
   - **§2.6 No option pickers.** User is a verbal/speech-to-text user; selecting between buttons is harder than answering a single inline open-ended question. Never use `ask_user_input_v0` even when clarification is genuinely needed — either ask one short question inline, or decide-and-execute and report back.
   - **§2.7 Proactive inline suggestions.** Assistant brings ideas, doesn't just respond. Every session ends with one explicit "I noticed X, worth doing Y — want me to?" suggestion before signing off.
   - **§2.8 SESSION_LOG.md protocol.** Live working narrative at repo root, appended EARLY in each chat (not at the end), updated incrementally, designed to survive chat drops. Read at start of every chat alongside `PROJECT_BRIEF.md` and `CHAT_KICKOFF.md`.

### Consequences

- **Email pipeline now end-to-end observable.** Welcome email leaves Resend → if it bounces, Sentry alerts. Hard bounces and complaints become first-class incidents instead of silent deliverability decay. Closes the "Webhooks: NONE configured" gap from earlier audits.
- **Narration fix gets real before/after telemetry.** The upcoming fix can be measured against actual user latency and failure rate. The qc-v211 annotation makes the split visible on every chart.
- **Fail-closed webhook is the right default.** A misconfigured `RESEND_WEBHOOK_SECRET` is a deployment bug; better to surface it as a 503 (Resend will retry, eventually a human notices) than to silently accept unverified payloads.
- **Process changes in skill v1.1.0 are durable.** The no-option-pickers rule is in user memory AND in the skill, so it survives memory drops AND tool changes.
- **`SESSION_LOG.md` is now the chat-drop recovery primitive.** Future chat crashes (like the May 8 AM permission-prompt incident) don't lose session context — the log is committed locally and incrementally.
- **Six functions on the rate-limit pattern, one new exception.** `resend-events` doesn't use `narrate_rate_limit_try` because Standard Webhooks signature verification is the rate limit (attackers can't forge valid signatures). Pattern note added to PROJECT_BRIEF.md.

### Alternatives considered

- **Keep webhooks on the deferred list:** rejected — the welcome-email work in ADR-017 made the gap actively concerning (we'd be sending mail with no way to know if it bounces). 90 minutes of work is worth it.
- **Forward all Resend events (delivered/opened/clicked) to Sentry:** rejected — those are not errors and would create noise that obscures the actual bounces. PostHog or a marketing-events table is the right home for engagement signal, not error monitoring.
- **Instrument PostHog narrate events as `$capture` with no privacy filter:** rejected — the source text could include personal birth-data context. `text_length` is enough to detect malformed inputs without ever shipping content.
- **Build a custom Narrate Health dashboard with both insights pinned:** attempted, deleted. The PostHog MCP doesn't expose `insight-update` cleanly via tool_search, so the insights couldn't be attached programmatically. Empty pinned dashboard is worse UX than two favorited insights findable via Insights → Favorites filter.
- **Migrate to Vercel for preview deploys:** rejected — see decision section #5.
- **Use `ask_user_input_v0` for clarification:** rejected by skill §2.6 (user is speech-to-text; option pickers are friction).

---

## ADR template — copy this for new entries

```markdown
## ADR-NNN — [short title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXX

### Context
What's the situation that requires a decision?

### Decision
What did we choose?

### Consequences
What changes because of this? Both upsides and constraints.

### Alternatives considered
What else was on the table and why we didn't pick it.
```
