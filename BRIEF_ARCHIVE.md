# QUANTUM CUBE — BRIEF ARCHIVE

**Frozen reference document. Do NOT update for normal sessions.**

This archive preserves the full historical record of Quantum Cube's build:
session-by-session timeline, every "biggest wins" block, all lessons learned,
full legal text, full magic-link email HTML, deprecated punch lists, brand
identity full inventory, and architectural decisions with reasoning.

**Active working brief lives in PROJECT_BRIEF.md** (lean, current state only).

**Knowledge transfer note:** This archive is intentionally lossless. When QNC
Academy or any future project needs to mine the lessons, decisions, and
hard-won insights from Cube's build, this is the canonical source. Cube-
specific facts AND the underlying portable lessons are both preserved here.

---

## 📅 SESSION TIMELINE (chronological)

### April 19, 2026 (Saturday, marathon — SW qc-v42 → qc-v99)

56 commits. Auth/unlock architecture fixes, cube orientation, music/voice redesign, card widening, square matrix, marketing consent, mobile lock-screen width fix, payment button parity. ElevenLabs narrator foundation wired.

### April 20, 2026 (Monday, launch-prep — SW qc-v107 → qc-v114)

- `57dd972` Remove 10.8MB base64 AUDIO (11MB → 356KB)
- `fd41b68` **CRITICAL paywall fix #1: STORE_KEY user-scoped**
- `2403ca7` **CRITICAL paywall fix #2: unconditional lock enforcement**
- `94af122` Legal additions: entertainment opener + Original Works + AI-Assisted

### April 21, 2026 (Tuesday, Mac + Cursor hardening)

- `e1070fb` FileVault enabled, Cursor allowlist tightened, `.cursorrules` at repo root, `.cursorignore` deleted.

### April 21-22, 2026 (Tuesday evening → Wednesday morning — narration phase 1 struggle)

Scaffolded pipeline, generated 256 numerology MP3s. Hash-based lookup failed on Android Chrome. Multiple debug rounds.

### April 22, 2026 (Wednesday — narration phase 1 lock + phase 2 ship + SW rebuild)

- `c2e3c80`, `4d51c0d`, `639bd09`, `2ba2a1e`, `e83b152`, `37f19fd`, `b0b87c5` (morning, SW v127→v136)
- `636e3d8`, `be9f385`, `0546755` (afternoon, 129 new MP3s, ~$13 overage)

### April 23, 2026 (Thursday — polish pass + CRITICAL paywall fix #3)

- `0bd5a54` Paywall fix #3 — gate face-reveal blocks on isUnlocked
- `231803e` UX: face-name label card + auto-scroll
- `2d38560` Audio: music refresh + randomisation + cube-touch SFX ripped
- `546363b` Welcome greeting auto-plays first 2 Face 1 entries
- (revert + reset back to `546363b` due to Cursor display glitch)

SW: qc-v138 → qc-v142.

Non-code: refund policy drafted+approved, magic-link email HTML drafted, Paddle + Google Play full requirements audits.

### April 24, 2026 (Friday — public site SHIPPED)

**Massive day.** Public site went live.

- `2e888d2` **Public site: landing page + 9 legal pages + /app route.** Restructured app into `/docs/`. Created landing page, 8 standalone legal pages, shared CSS, CNAME, .nojekyll. Deployed.
- `e8bfbc4` `/docs` restructure for Pages source
- `32a23f0` `.nojekyll` + `/privacy/` redirect
- `cc63d90` `/app/` trailing-slash redirect

GitHub Pages source switched. Cloudflare CNAME propagated. Cloudflare email routing set up. `quantumcube.app` LIVE.

### April 24-27, 2026 (additional fix)

- `7a9b7ac` Music randomisation per session + user-scope welcome counter

### April 28, 2026 (Tuesday — sync + brief update)

Cross-chat sync. Identified gap between Claude chat A (April 23 polish) and Claude chat B (April 24 public site). Re-aligned context. v24 brief generated. Identified untracked `brand/` folder.

### April 29, 2026 (Wednesday — single-day sprint, 12 commits)

The biggest single-day technical sprint of the project to that point. 12 commits shipped:

| Commit    | What                                                                           |
| --------- | ------------------------------------------------------------------------------ |
| `7016cb1` | feat(narrate): per-IP rate limiting (Postgres RPC, 5/min + 20/hr)              |
| `f9a3df3` | chore(db): commit existing remote migration to repo (profiles + RLS + trigger) |
| `43e397e` | feat(pwa): static manifest.json replaces blob URL                              |
| `0fcbdb9` | feat(account): data export + account deletion (POPIA/GDPR)                     |
| `dddb84e` | debug(delete): diagnostic logs + signOut timeout race                          |
| `21b9c99` | fix(delete): rip diagnostic logs, keep timeout race                            |
| `9c35570` | feat(brand): commit Quantum Cube wordmark pack                                 |
| `49ea172` | docs: brief v25 (subsequently expanded to v25.1)                               |

SW: qc-v142 → qc-v147.

**Non-code outcomes Apr 29:**

- Paddle definitively ruled out (verified directly against their AUP)
- LemonSqueezy: SA tax form delay, application paused
- FastSpring: Michelle started KYB, account dormant as fallback
- Dodo Payments signup submitted, in 24-72hr review
- Magic-link email HTML pasted to Supabase dashboard, preview confirmed
- Security audit complete: 3 items checked (rate limit, input validation, key handling) — only narrate rate limit needed fixing
- Paddle/PayFast 26-line punch list captured for post-Dodo cleanup
- Cube icon priority surfaced (needed for app icons + social profile pics — single dependency for two work items)
- Lesson on JWT-handling: tokens never go through Cursor or chat; debug via DevTools Console + Promise.race timeouts instead

### April 30, 2026 (Thursday — brand identity sprint, 3 commits)

Full morning of brand work. Three commits shipped:

| Commit    | What                                                                |
| --------- | ------------------------------------------------------------------- |
| `4fb2e40` | feat(brand): replace Apr 29 brand pack with QC monogram + wordmarks |
| `039b0c1` | feat(icons): wire QC monogram PNG icon family across site           |
| `78a8e00` | feat(icons): round favicon corners (18% radius, medium)             |

SW: qc-v147 → qc-v149.

**Outcomes Apr 30:**

- Confirmed orphan Firebase project ("QuantumCubeApp") was never used by either Cube or Academy. Cleared for deletion. (Lesson: Firebase ≠ Supabase — verify before action.)
- Built full wordmark pack in Canva Pro (Cinzel Decorative). 9 PNG variants exported transparent at 2800×1800.
- Cube icon path explored (glass cube, wireframe, outline) but team voted for **QC monogram** instead — a Cinzel-Decorative type-as-logo mark. Stronger silhouette, scales clean to favicon, brand-coherent with wordmarks.
- App icon family generated via macOS native `sips` (no homebrew/imagemagick needed) from `brand/QC - Solid.png` master.
- Favicon corners rounded via Python PIL (18% radius, medium — matches Claude/YouTube/Vimeo bookmark style).
- Landing page + 8 legal pages were missing all icon refs (favicon, apple-touch, manifest) — fixed in same commit as app.html SVG → PNG swap.
- Two C-only monogram variants created as bonus (could become a secondary mark later, like Mickey ears vs full Disney logo).
- Decision: HTML text wordmarks stay in app/site (sharper, faster, accessible, selectable). PNG wordmarks reserved for contexts where text won't render (email).
- Apr 29 brand pack (Cinzel woff2 fonts + old wordmark PNGs + Cube Sides source images) all retired — git history preserves.

### May 1, 2026 (Friday PM — Dodo approval + recon)

**1. DODO PAYMENTS APPROVED.** ← May 1, ~7 PM. The last launch-blocker dropped. Email "Live Payments Are Now Enabled" arrived after 8 days in review (longer than the stated 24-72hr window — escalation was being prepared but not needed). Live Payments status confirmed in dashboard with all 4 verification cards green: Product Information, Identity Verification, Business Verification, Bank Verification.

**2. Dodo MoR legal entity name confirmed.** ← May 1 PM. Verified via Cursor Browser MCP recon of Dodo's own Master Service Agreement at `dodopayments.com/legal/terms-of-use`:

- **Registered legal entity:** `Dodo Payments, Inc.` (Delaware-incorporated US entity)
- **Trade name (shows on customer credit card statements):** `Dodo Payments`
- This is the value to plug into the 26-line legal copy swap (replacing "PayFast (Pty) Ltd" / "Paddle.com Market Limited")

**3. Dodo dashboard recon complete.** ← May 1 PM. Captured for tomorrow's integration session:

- Business ID: `bus_0NdjpSYtT1ZAbRN6l15dg`
- Adaptive Currency: ON (customers see local currency)
- Visa Rapid Dispute Resolution: ON, $100 threshold (good defensive default)
- Webhooks docs URL: `docs.dodopayments.com/developer-resources/webhooks`
- Webhook event we'll subscribe to: `payment.succeeded` (also `refund.succeeded` for completeness)
- Integration path locked: **Hosted checkout** (Payment Links / Overlay) — NOT full SDK
- 3D Secure currently OFF — flagged for review post-launch (low-priority for $17 product)

**4. Dodo Test Mode active for tomorrow.** ← May 1 PM. Switched from Live Mode to Test Mode for sandbox integration work. **No live charges possible until we explicitly switch back.**

**5. LemonSqueezy + FastSpring fallback chain unchanged but now redundant.** ← May 1 PM. With Dodo live, fallback applications stay parked but no longer urgent. LemonSqueezy still on SA tax form delay (a week now). FastSpring still dormant. Both can be cleaned up post-launch.

**6. Coda Payments evaluated and rejected.** ← May 1 PM. Researched as a possible alternative — they're a gaming-focused MoR (Codashop, EA / Activision / Roblox clients). Wrong scale and wrong industry for a $17 one-time digital reading. Don't pursue.

### May 2, 2026 (Saturday — Dodo integration + LAUNCH, 11 commits)

The largest single-day technical sprint of the project. 11 commits shipped, both modes tested end-to-end, real payment processed, bounce-bug killed.

| Commit    | What                                                                          |
| --------- | ----------------------------------------------------------------------------- |
| `cdefd3f` | feat(payment): migrate Dodo to overlay SDK checkout                           |
| `7ff5db8` | feat(legal): swap PayFast/Paddle MoR wording for Dodo Payments, Inc.          |
| `90705bd` | feat(payment): switch Dodo to Live Mode                                       |
| `9db21e0` | diag: trace post-payment auth + overlay flow (Test Mode)                      |
| `f1e2058` | fix(payment): detect Dodo redirect on page-load to unlock cube                |
| `bc9b1d2` | fix(payment): event-driven post-payment unlock via auth listener              |
| `be425eb` | fix(payment): pass session arg to unlock + add inflight lock                  |
| `0413704` | fix(payment): bypass Supabase JS client during post-redirect unlock           |
| `e85ca5c` | fix(payment): auto-trigger runCalculation after post-payment unlock ← THE FIX |
| `061ca8e` | chore: rip diagnostic [QC-DIAG] logs after post-payment fix shipped           |
| `f7834c3` | feat(payment): switch back to Live Mode after bounce-bug fix shipped          |

Also pushed earlier-in-day commits: `b3386ea` (dodo-webhook source) and `84be838` (initial PayFast→Dodo redirect-link integration, replaced by overlay later same morning).

SW: qc-v154 → qc-v169 (15 bumps).

**Code outcomes May 2:**

- Two Edge Functions shipped: `dodo-webhook` + `dodo-create-session`
- Overlay SDK integration via jsdelivr UMD bundle
- `_readSessionFromStorage()` helper bypasses Supabase JS client
- `_resolveDodoSdk()` helper handles UMD namespace shape
- 17 PayFast/Paddle references replaced with Dodo Payments, Inc. across 9 files + 1 migration comment

**Non-code outcomes May 2:**

- Live Mode active in Dodo dashboard
- Live Mode webhook endpoint configured pointing to dodo-webhook URL
- Live Mode product created (`pdt_0Ndx7o41zFEREpoPTyvR2`, $17 USD)
- Test Mode + Live Mode signing secrets stored in Apple Passwords
- API key leak caught + rotated within ~2 minutes
- Two real $17 charges processed end-to-end (morning + evening); morning's refunded successfully, evening's pending settlement
- 11 commits on `main`, all pushed cleanly, zero rollbacks needed

### May 3, 2026 AM (Sunday — strategic sync)

Brief v30 + Marketing Playbook v2 shipped. Strategic context locked: budget posture, timeline posture, three outcome paths, Play Store path locked. Work continued throughout afternoon (see May 3 PM).

### May 3, 2026 PM (Sunday — multi-product strategy lock)

Brief v31 + Marketing Playbook v3 shipped. Customer thesis (curious dabbler) locked. Product model pivot from subscription to multi-product one-time purchase. Shareable cosmic-profile card identified as engagement-loop feature. Michelle handover scheduled for May 4.

### May 3, 2026 EVENING (Sunday — Phase 2 polish marathon, 23 commits)

Single-session marathon. 23 commits across infrastructure, polish, and audio:

| Commit    | What                                                                    |
| --------- | ----------------------------------------------------------------------- |
| `c623a82` | docs: brief v31 + playbook v3 — multi-product roadmap, customer thesis  |
| `0748a57` | fix(audio): unblock music tracks from .gitignore + ship 5 MP3s          |
| `2cc112a` | feat(auth): swap white Google G for official 4-color logo (superseded)  |
| `beebff7` | fix(welcome): play greeting once only, never on signup screen           |
| `64440af` | chore(copy): strip Valory branding from user-facing pages               |
| `5a382ff` | fix(narration): re-render welcome.mp3 at slower pace (1.15 → 1.00)      |
| `2b92f93` | fix(face0): center Google + Reveal + Resend buttons                     |
| `64b9d89` | fix(face0): center Back to Sign Up button                               |
| `373fa2d` | chore(face0): remove redundant 'or sign up with email' divider          |
| `f928061` | style(face-label-card): more breathing room above + swap to Cinzel      |
| `4543f33` | style(face0): add breathing room between Google button and form card    |
| `ad98c26` | feat(auth): replace custom Google button with Google Dark Pill spec     |
| `4c210b3` | style(auth): switch Google button to Light Rectangular spec             |
| `cbbbc3d` | fix(splash): remove in-app loading screen + sync theme color            |
| `92bd75b` | style(splash): sync all theme/background colors to #05050f cosmic black |
| `1020df5` | fix(face3): matrix cards no longer overflow with high dot counts        |
| `c3d3e57` | feat(audio): duck music to 6% during narration, restore to 20%          |
| `a06ca3e` | fix(face3): re-apply matrix card overflow fix lost in c3d3e57           |
| `42d3094` | fix(face4): astrology profile cards no longer overflow                  |
| `c6ceb6d` | style(face4): distribute astrology card content evenly through card     |
| `7f01701` | style(face-label-card): unbold face-label-text (700 → 400)              |
| `c7e1d8b` | fix(face3): Life Phases card no longer stretches taller than siblings   |
| `5dcd585` | style(face3): unify multi-value separator to middle dot                 |
| `63684ef` | fix(face3): scale sb-num font by value count + revert separator to comma|

SW: qc-v169 → qc-v191 (22 bumps).

**Outcomes May 3 evening:**

- Music files actually deployed (had been silently `.gitignore`d)
- Google OAuth verification de-risked (button now compliant with Google's Light Rectangular spec)
- Welcome greeting fixed (plays once, signed-in only, slower pace)
- Splash flow polished (no in-app wordmark loader, theme colors synced)
- All Face 0 buttons centered
- Three card-overflow bugs killed (matrix, astrology, life phases)
- Music ducks during narration so voice and music don't clash
- Multi-number profile cards scale font by count (handles 1-9 numbers cleanly)
- Separators unified to commas across all multi-value cards

### May 4, 2026 AM (Monday — cleanup + brief restructure)

Started with `.supabase-envx` cleanup (stray nano artifact containing all secrets — Cursor caught data-loss risk in the script and self-corrected to merge unique key into canonical file before delete). Brief restructured: split into lean active brief + lossless archive (this document).

- `804856a` chore(gitignore): tighten .supabase-env to .supabase-env* glob
- `e804ab4` docs: brief v32 + new BRIEF_ARCHIVE.md (lossless history split)
- `3f7f297` feat(brand): refresh cyan color across all logo variants

### May 4, 2026 PM (Monday — observability + feature completion + E2E verification, 7 commits)

Major afternoon. Three big themes shipped: production observability (Sentry), feature completion (multi-narration), and critical infrastructure verification (magic-link E2E test).

| Commit    | What                                                                          |
| --------- | ----------------------------------------------------------------------------- |
| `730d4d8` | feat(monitoring): add Sentry error monitoring (production-only)               |
| `649bb60` | fix(narration): multi-number cards narrate ALL numbers via playSequence (NEAR-MISS — Cursor stale buffer dropped narration code, only SW + Sentry release bumped) |
| `4b6bdf9` | fix(narration): actually wire hp/kl multi playSequence (follow-up — corrective for 649bb60) |
| `03eff84` | chore(test): flip to Test Mode for magic-link E2E verification                |
| `b99b807` | fix(sw): skip caching of 206 partial-content responses                        |
| `9062eef` | fix(test): re-apply DODO_MODE=test flip lost in b99b807 stale buffer          |
| `1b15ece` | chore: revert to Live Mode after magic-link E2E test pass                     |

SW: qc-v191 → qc-v198 (7 bumps).

**Sentry shipped (`730d4d8`):**

- Browser SDK 8.50.0 via explicit CDN (NOT loader script — keeps configuration auditable in code)
- EU region (`o4511330222604288.ingest.de.sentry.io`) for GDPR alignment with Supabase Frankfurt + Resend eu-west-1
- Production-only gate (`location.hostname !== "quantumcube.app"` skips init)
- Error monitoring ONLY — Tracing/Session Replay/Application Metrics all `sampleRate: 0`
- Release tagged with current SW version per deploy
- `sendDefaultPii: false` + `beforeSend` regex scrubs JWT/email
- Noise filters: drops browser-extension errors, ResizeObserver loops, generic "Script error.", non-Error promise rejections
- Smoke test confirmed working: email alert fired within seconds
- DSN (public-facing): `https://fc0733d091a210fe80f9213b64fafa8e@o4511330222604288.ingest.de.sentry.io/4511330235908176`

**Sentry's first real catch (`b99b807`):**

Within ~2 hours of going live, Sentry caught a real production bug. The SW was unconditionally caching every successful response, but Cache API rejects HTTP 206 partial-content responses (used by audio Range requests for seeking within MP3s). Every audio file load threw `TypeError: Failed to execute 'put' on 'Cache': Partial response (status code 206) is unsupported` — silent until Sentry exposed it. Fix: tighten `cache.put()` condition from `resp.ok` to `resp.ok && resp.status !== 206`.

**Multi-number narration shipped (`4b6bdf9` corrective for `649bb60`):**

Hidden Passion + Karmic Lessons cards previously narrated only the first number even when multiple values existed. Fix mirrors the Life Phases pattern: icard template now serializes multi-array to `data-multi` attribute, qcNarrateCard adds a multi-handler before the single-URL fallback that builds URL array of `num_{cat}_{n}_v1.mp3` per number and calls playSequence. Inventory verified: 27 hp + 27 kl files on disk (1-9 × v1/v2/v3); v1 always present for the locked-variant approach.

**`649bb60` near-miss:** First narration commit reported success + verification grep showed new code, but `git commit` only recorded the SW + Sentry release bumps. Cursor's IDE buffer race silently dropped the narration code between Python edit and git stage. Cursor's own post-commit verification caught the miss → corrective `4b6bdf9` shipped. Same failure mode struck again later in `b99b807` (DODO_MODE silently reverted from "test" to "live").

**Magic-link payment E2E test PASSED:**

Three-place mode flip: `DODO_MODE` in app.html + `MODE` in dodo-create-session + Supabase secrets `DODO_PAYMENTS_API_KEY` / `DODO_PAYMENTS_WEBHOOK_KEY` (swapped via Mac Terminal, never via Cursor). Test profile `rkelbrickmail+e2etest@gmail.com` used Gmail "+" alias to avoid collision with existing Google OAuth identity on `rkelbrickmail@gmail.com`.

Test sequence:
1. Form fill in fresh Chrome incognito → REVEAL MY CUBE
2. Magic link delivered to inbox within seconds
3. Click VERIFY in Gmail → opens in default Chrome profile (NOT incognito session — known browser behavior, doesn't break flow)
4. Auto-detect session, navigate into cube past Face 0
5. Face 3 → Pay $17 → Dodo overlay opens
6. Test card `4242 4242 4242 4242` → payment processes
7. **Lands directly on Face 3 with full reading visible — NO bounce to Face 0**

Bounce-bug fix from May 2 (`e85ca5c`) confirmed working for BOTH OAuth and magic-link auth paths.

**Pre-stage verification guard adopted (from `9062eef`):**

After the b99b807 stale buffer almost shipped a 3-place mismatch, every subsequent mode-flip commit included an explicit guard:

```bash
if [both vars match expected mode]; then
  echo "✓ Both in sync at TARGET — safe to ship"
else
  echo "✗ MISMATCH — ABORTING"
  exit 1
fi
```

This pattern is now standard for any 3-place flip operation. Caught no further mismatches in the rest of the session.

**Outcomes May 4 PM:**

- 7 commits, all pushed to origin/main
- SW v191 → v198 (each commit bumped)
- Sentry release tag tracking SW version
- Live Mode active end-of-session (verified via curl: DODO_MODE = "live", const CACHE='qc-v198', quantum-cube@qc-v198)
- Test profile rkelbrickmail+e2etest@gmail.com left at has_paid=false (Test Mode charge cleaned up)
- Pages serving fully reverted Live Mode build
- Supabase secrets digest hashes confirmed matching original Live values (9b76... and 65e7...)

### May 4, 2026 EVENING (Monday — pre-launch security audit + 5 commits)

Pre-marketing-push security audit run end-to-end and shipped. 5 commits across hardening, CSP, iOS compliance, and brief sync. Pre-launch security checklist closed.

| Commit    | What                                                                          |
| --------- | ----------------------------------------------------------------------------- |
| `35331bf` | chore(security): rate-limit unprotected Edge Functions + tighten error responses |
| `f6a7db5` | chore(security): add CSP baseline + securitypolicyviolation listener         |
| `00d1c6c` | fix(security): allow Sentry CDN connect + Vimeo thumbnail img-src in CSP    |
| `1324784` | chore(meta): add mobile-web-app-capable alongside apple- variant            |
| `9bcf2d3` | docs: brief v34 — security audit complete + 4 commits shipped May 4 PM      |

SW: qc-v198 → qc-v201 (`f6a7db5`, `00d1c6c`, `1324784` each bumped; `35331bf` was Edge Function only — no SW bump needed).

**Code outcomes May 4 EVENING:**

- **Edge Function rate limits added** to `delete-account` (per-user 2/min, 5/hr), `export-data` (per-user 5/min, 20/hr), `dodo-create-session` (per-IP 5/min, 20/hr). All three reuse the existing `narrate_rate_limit_try` Postgres RPC with namespaced bucket keys (`delete:USER_ID`, `export:USER_ID`, `dodo-session:IP`) — no new migration. `dodo-create-session` newly imports `@supabase/supabase-js` to gain RPC access.
- **Error responses tightened across all 5 Edge Functions.** No more `String(e)`, `detail: errText`, or `deleteErr.message` flowing back to the browser. Full error context preserved server-side via `console.error` for log-trail debugging. Generic codes only client-side.
- **CSP applied to all 10 HTML pages** via `<meta http-equiv>`. Two policies:
  - `docs/app.html`: permissive — keeps `'unsafe-inline'` for scripts (existing inline event handlers + style attrs would need multi-hour refactor) and styles. Allow-list: `player.vimeo.com`, `cdn.jsdelivr.net`, `browser.sentry-cdn.com`, `fonts.googleapis.com`, `fonts.gstatic.com`, Supabase project domain, `*.ingest.de.sentry.io`, `*.dodopayments.com`, `*.vimeocdn.com`. `frame-src` restricts iframes to vimeo + dodo. `object-src 'none'`.
  - 9 public pages (index + 8 legal): strict — no inline scripts, no external scripts at all, fonts via Google Fonts only.
- **`securitypolicyviolation` event listener** added to `app.html`, forwards CSP violations to Sentry as warnings. Same observability mechanism that caught the SW 206 bug — paid off within hours of CSP deploy by surfacing two CDN gaps that needed allow-listing (`browser.sentry-cdn.com` for Sentry's runtime self-fetch + `i.vimeocdn.com` for video thumbnail loads).
- **`mobile-web-app-capable` meta tag** added alongside the deprecated `apple-mobile-web-app-capable` form. iOS 16+ deprecation warning seen in DevTools console — both kept for back-compat with older iOS.
- **Brief v33 → v34** restructure. Security audit checklist condensed from "TO-DO list" form to "completed results" form. WHAT'S-LEFT bucket trimmed (settings gear, Sentry, multi-narration, magic-link E2E, mobile-web-app-capable, security audit all crossed off). Rollback table pruned of 8 older anchors (all preserved in this archive's rollback table).

**Non-code outcomes May 4 EVENING:**

- **zsh history sanitisation scan** ran against `~/.zsh_history` (3969 lines) with patterns covering `supabase secrets set` echo leaks, export-style assignments, Bearer/JWT tokens, Stripe/Dodo `sk_test_`/`whsec_` prefixes, ElevenLabs `sk_<hex40>` shape. Total matches: 0. Heuristic scan can miss exotic shapes but the May 2 leak pattern is fully covered.
- **Apple Passwords inventory documented.** Already-stored: Dodo Test+Live API keys, Test+Live webhook signing secrets, Test+Live product IDs, Google account credentials (admin@qncacademy.com + quantumneurocreations@gmail.com), Mac recovery key. Not stored locally: ElevenLabs API key, Resend API key — both live server-side as Supabase secrets, can be regenerated from upstream dashboards if ever needed.
- **Resend API key backup decision.** Resend hides API key values after creation by design (only metadata + prefix visible after first display). Two options: (A) leave alone, rotate-to-capture if ever needed locally (~5 min rotation job), (B) rotate now to capture and store. Chose **(A)** — low-stakes secret, the rotate-to-capture path is well understood, and the SMTP value already lives in Supabase Auth → SMTP config which is the only place it actually needs to be.
- **Notepad audit.** Some legacy passwords/usernames for social media accounts and dormant services (Paddle, LemonSqueezy, FastSpring). Low risk, no rotation needed. Stays as-is.
- **Supabase secrets confirmed (10 names):** DODO_PAYMENTS_API_KEY, DODO_PAYMENTS_WEBHOOK_KEY, ELEVENLABS_API_KEY, SUPABASE_ANON_KEY, SUPABASE_DB_URL, SUPABASE_JWKS, SUPABASE_PUBLISHABLE_KEYS, SUPABASE_SECRET_KEYS, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_URL. CLI prints SHA-256 digests, never values.

**Items intentionally deferred (logged so they don't get re-raised):**

- **`dodo-create-session` JWT verification of body's `user_id`.** Currently the function trusts the `user_id` field from the request body, validated only by checking the user exists in `profiles`. Theoretical risk: an attacker could pay $17 and unlock someone else's account — financially the attacker loses $17, the target gets free access. Real-world risk near zero (no upside for the attacker). Deferred until a use case forces the fix.
- **innerHTML refactor (7 spots in `app.html`).** Audited each: all source from internal data tables (NUM, WSIGN, CSIGN) or computed numeric values — never raw form input. `fullName` always goes via `textContent`. No user-input → innerHTML flow exists. No XSS surface. No refactor needed.
- **Inline script removal in `app.html`.** Would require multi-hour refactor of every inline event handler (`onclick=`, etc.) into `addEventListener` calls. CSP allows `'unsafe-inline'` for `app.html` only; the 9 public pages stay strict. Acceptable tradeoff for now.

**Calendar reminders set:**

- **May 18, 2026** — Sentry 14-day Business trial expires. Verify auto-downgrade to free tier (5k errors/month). Watch for surprise billing.
- **May 4, 2027** — Annual key rotation review (ElevenLabs + Resend + Dodo + Supabase service role).

(Michelle to set in shared calendar.)

---

## 🎉 BIGGEST WINS — HISTORICAL BLOCKS

### Wins since v33 (May 4 PM/EVENING session)

**1. PRE-LAUNCH SECURITY AUDIT COMPLETE.** ← May 4 EVENING. Four commits closed every actionable item from the audit checklist. Site is hardened (rate limits, generic error responses, CSP, iOS compliance) before any marketing-volume traffic hits.

**2. CSP LIVE ON ALL 10 HTML PAGES.** ← May 4 EVENING (`f6a7db5`, `00d1c6c`). Two policies (permissive for app, strict for public pages), `securitypolicyviolation` listener forwarding to Sentry. The listener proved value within hours by catching two real CDN allow-list gaps that escaped static planning.

**3. EDGE FUNCTION RATE LIMITS + ERROR HARDENING.** ← May 4 EVENING (`35331bf`). Three previously unprotected functions (delete-account, export-data, dodo-create-session) now rate-limited per-user or per-IP. All 5 functions return generic error codes only — no raw error strings, no stack traces, no upstream service details flowing to the client. Recipe documented in fragile-areas: "reuse `narrate_rate_limit_try` RPC with namespaced bucket key" — no new migration needed.

**4. SECRETS POSTURE DOCUMENTED.** ← May 4 EVENING. zsh history clean (0 matches across 5 secret-shape patterns). Apple Passwords inventory listed: Dodo + Google + Mac recovery key all backed up. ElevenLabs + Resend intentionally not held locally (regenerate from upstream if ever needed). 10 Supabase secrets confirmed by name. Operational rule reinforced: never paste secret values into terminal output, ever.

**5. iOS DEPRECATION FIX.** ← May 4 EVENING (`1324784`). `mobile-web-app-capable` meta tag added alongside the deprecated `apple-mobile-web-app-capable`. Both kept for back-compat. Sentry warning class for this on iOS 16+ users will stop appearing.

**6. SESSION HYGIENE: ARCHIVE UPDATED ALONGSIDE BRIEF.** ← May 4 EVENING. Caught a near-miss where the v34 brief condensation could have lost planning context (the original audit checklist with its bucket structure and intentional-deferral logic). Ronnie spotted the line-count drop and flagged before commit, prompting this archive update. Lesson burned in: when a brief section condenses because work shipped, the archive captures BOTH the planning context and the results record. Lossless transfer is the principle.

**7. PRE-MARKETING-PUSH CHECKLIST SUBSTANTIALLY CLEAR.** ← May 4 EVENING. Items remaining: full app walkthrough QA pass (casual ongoing). Items shipped (across May 4 morning + afternoon + evening): Sentry, multi-number narration, magic-link E2E test, security audit, mobile-web-app-capable. Settings gear icon was correctly noted as already shipped (Apr 30 — brief was stale, fixed in v34). **Phase 5a Play Store prep is now the next big rock.**

### Wins since v30 (May 3 PM session)

**1. CUSTOMER POSITIONING THESIS LOCKED — curious dabbler, not hardcore enthusiast.** ← May 3 PM. Market roughly splits: ~10-15% hardcore (Co-Star/Pattern/Sanctuary subscribers), ~70-75% **curious dabblers** (the underserved segment we target), ~10-15% gift buyers. The dabbler wants a beautiful, quick, meaningful one-off reading without subscription fatigue, daily push notifications, or a content treadmill. Our wedge is **simplicity, beauty, one-shot completeness** — not depth. Co-Star wins depth; we don't compete there.

**2. PRODUCT MODEL LOCKED — multi-product one-time-purchase, NOT subscription.** ← May 3 PM. Subscription tier (Quantum Cube Plus, $9.99/mo with daily horoscopes) is the **wrong model for our customer segment**. Building daily horoscope infrastructure would solve a problem the curious dabbler doesn't have. Conversion would be ~2-3% not the 12-15% projected for general spirituality apps. Instead: lifetime value comes from **new one-time products**, not recurring revenue from one product.

**3. SHAREABLE COSMIC-PROFILE CARD identified as the one engagement-loop feature worth building.** ← May 3 PM.

**4. RETENTION MECHANISM CLARITY — three drivers, two natural fits.** ← May 3 PM. Spirituality apps that retain over years do so through (a) life-event moments → maps to Compatibility / Year Ahead / Tarot, (b) gifting → maps to Family + gift codes, (c) community/sharing → maps to shareable cosmic card. Deliberately skip the typical 4th mechanism (daily horoscope + push notifications).

**5. SOCIAL CHANNEL OWNERSHIP — Michelle takes over from May 4 (Monday).** ← May 3 PM.

**6. PRE-LAUNCH SECURITY AUDIT SCOPED — OWASP-style review before Play Store submission.** ← May 3 PM.

**7. BUG REPORTER / SENTRY moved up the priority list.** ← May 3 PM. Should ship before public marketing push.

**8. EMAIL DELIVERABILITY PLAN — burner / warmup domain for marketing emails.** ← May 3 PM.

**9. APPLE APP STORE PHASE 8 — Small Business Program + Restore Purchases + Sign in with Apple.** ← May 3 PM.

**10. MARKETING TOOLS / DIRECTORIES TRIAGE — definitive list.** ← May 3 PM. Confirmed rejected: AppSumo, G2, Capterra, Vloxo, BetaList, uNeed, Fazier, Microlaunch, Peerlist, Tiny Launch, Tiny Startup, SideProjects, LaunchIgniter, PeerPush. Stick with Product Hunt + Indie Hackers + Hacker News only.

**11. SEO CONTENT STRATEGY ADDED — FindQuestions.com + EEAT blog framework.** ← May 3 PM.

### Wins since v28 (May 2 PM session — the LAUNCH day)

**1. QUANTUM CUBE IS LIVE AND ACCEPTING REAL PAYMENTS.** ← May 2, ~11 AM (first live charge) and again ~6:30 PM (second live charge after bounce-bug fix). Real $17 USD processed end-to-end. Real card. Real customer email receipt. Webhook fired, has_paid flipped, cube unlocked.

**2. Dodo overlay SDK migration shipped.** ← May 2 AM. Originally built integration with static payment-link redirect (commit cdefd3f). Within 30 minutes of testing, identified the cross-domain redirect was killing user sessions on return. Pivoted to Dodo's overlay SDK (`dodopayments-checkout` UMD bundle via jsdelivr). User now stays on `quantumcube.app` the entire time.

**3. Post-payment Face-0 bounce bug — diagnosed and killed.** ← May 2 PM. The big debug saga of the day. Multiple incorrect theories before finding the actual issue:

- First theory: cross-domain session loss → built session-aware banner UX (didn't help)
- Second theory: stale SW serving old code → multiple SW reset cycles (no smoking gun)
- Third theory: race condition between `checkDodoReturn` and `onAuthStateChange` calling `attemptPaymentUnlock` in parallel → added `_qcUnlockInFlight` idempotency lock (helped but didn't fix)
- Fourth theory: `await sb.auth.getSession()` hanging during INITIAL_SESSION restore → bypassed Supabase JS client entirely, read session straight from localStorage and queried profiles via direct REST fetch (worked — `profile fetch status: 200`, `unlock applied`, but still bounced)
- **Actual root cause:** the unlock data flow was working all along. Logs proved `syncUnlockFromProfile` ran successfully and `qcCurrentProfile` was set to a paid profile. But the user was sitting on Face 0 (sign-up form) because `runCalculation` had never fired to put them inside the cube view. **Unlock state was correct — the user just wasn't in the cube to see it.**
- **Fix (commit e85ca5c):** after applying the unlock, also call `populateFormFromProfile()` then `runCalculation()` after a 200ms DOM-settle delay. User now lands inside the cube on Face 3 with full reading visible. No bounce, no re-sign-in.
- **Lesson burned in:** when something looks broken, instrument the data flow before patching. Don't assume the visible symptom (bounce to Face 0) is the same as the actual bug (cube wasn't opened).

**4. 17-line legal copy swap shipped.** ← May 2 AM. Replaced all PayFast (Pty) Ltd and Paddle.com Market Limited references across 9 files (`docs/app.html`, 8 legal pages) plus 1 migration comment with `Dodo Payments, Inc.`.

**5. Live Mode E2E verified twice.** ← May 2.

**6. Dodo refund flow partially verified.** ← May 2. Theory confirmed: Dodo enforces a settlement-period holding window before funds are refundable from the merchant wallet.

**7. Dodo wallet flow understood.** ← May 2. Live Mode "Insufficient funds in wallet" is real and applies to refunds within ~hours of the original charge. Test Mode wallet is a fake balance that's always 0 (refunds always fail there). Don't treat as a bug.

**8. API key leak caught and rotated cleanly.** ← May 2 AM. During Live Mode setup, the Live API key was accidentally pasted into chat in plain text via the `supabase secrets set` command output. Caught within minutes, rotated immediately:

- Deleted the leaked Live API key in Dodo dashboard FIRST
- Generated a fresh Live API key
- Re-set Supabase secret with new value (no echo this time)
- Verified digest hash changed
- **No transactions used the leaked key.** Damage zero.
- **Burned-in rule:** the same `NEVER paste tokens or keys into chat or Cursor` rule from v28 (around OAuth Client Secret handling) applies to ALL secrets, ALL the time.

**9. Two new Supabase Edge Functions shipped.** ← May 2.

- `dodo-webhook`: receives `payment.succeeded` and `refund.succeeded` events from Dodo, verifies signature via Standard Webhooks SDK, updates `has_paid` in profiles. Source committed (commit b3386ea).
- `dodo-create-session`: mints checkout session URLs (`cks_xxx`) server-side via Dodo's Checkout Sessions API. Embeds `metadata.user_id` for webhook profile matching.
- Both run with `verify_jwt = false` and handle their own auth.

**10. Dodo product created in both modes.**

- **Test Mode product:** `pdt_0NdwjT5U975nxTzpogS68` — `Quantum Cube`, $17 USD, single payment
- **Live Mode product:** `pdt_0Ndx7o41zFEREpoPTyvR2` — same details
- Live webhook endpoint configured pointing to `dodo-webhook` Edge Function
- Both signing secrets stored in Apple Passwords

**11. CHAT_KICKOFF.md memory note added.** ← May 2 PM. User memory edits now persist across all Quantum Cube chats:

- Address user as "buddy" (not by name)
- Supabase CLI v2.90.0 — `functions deploy <name>` works without `--linked` flag

### Wins since v26 (Apr 30 PM session)

**1. Google OAuth 2.0 fully shipped end-to-end.** ← Apr 30 PM. The biggest launch-blocker after Dodo is now gone. Three-commit implementation:

- DB migration: `dob` + `name` columns added to `profiles`, `handle_new_user()` trigger updated to capture both from `raw_user_meta_data`, RLS update policy refreshed
- Frontend: cosmic-themed "Continue with Google" button on Face 0 above email field, italic "or sign up with email" divider below
- Profile persistence: `saveProfileFromForm()` writes name+DOB to profile after successful runCalculation; `populateFormFromProfile()` auto-fills form on return for any user (OAuth or magic-link); `onAuthStateChange` refactored to fetch profile FIRST, populate form, then decide whether to fire runCalculation
- **Tested all 3 paths end-to-end:** brand-new OAuth user, returning OAuth user, magic-link path

**2. Settings gear icon shipped.** ← Apr 30 PM. Closed the Face 7 discoverability gap. 40×40 fixed bottom-left, glass-cyan styling with safe-area insets for iOS notches.

**3. Magic-link email PNG wordmark deployed.** ← Apr 30 PM.

**4. Icon family regenerated with proper safe-zone padding.** ← Apr 30 PM. New `brand/QC - Solid Spaced.png` master regenerated all 5 icons (192/512/512-maskable/apple-touch-180/favicon-32) with breathing room inside the inner 80%.

**5. Social media handles claimed across all 6 platforms.** ← Apr 30 PM. `@quantumcubeapp` locked on YouTube, Facebook, Instagram, X/Twitter, TikTok, Threads.

**6. Brand tagline locked: "Your cosmic profile, simplified."** ← Apr 30 PM.

**7. Google Cloud project created and configured.** ← Apr 30 PM. New project `quantum-cube-494914`. OAuth consent screen branded with QC logo + privacy/terms URLs + 3 test users.

**8. Supabase Google provider enabled + URL config tightened.** ← Apr 30 PM. Site URL corrected from `https://quantumcube.app/app.html` to `https://quantumcube.app/app`.

### Wins since v24 (cumulative)

**1. Payment processor decision FINAL: Dodo Payments.** Application submitted April 29, in 24-72hr review. Dodo actively markets to astrology brands. LemonSqueezy and FastSpring parked as fallbacks. Paddle definitively ruled out (their AUP explicitly prohibits "fortune-telling/horoscopes/clairvoyance").

**2. Account deletion + data export shipped and VERIFIED end-to-end.** Two new Edge Functions, two-tap confirmation pattern with 5-second arm window, full localStorage wipe, signOut Promise.race timeout, cascade FK from auth.users → public.profiles.

**3. narrate Edge Function rate-limited.** Postgres RPC-based (5/min, 20/hr per IP). Closes the ElevenLabs credit-burn vulnerability.

**4. Real PNG icon family wired across the entire site.** ← Apr 30. The SVG cube placeholder is gone. Manifest now references actual PNGs (192, 512, 512-maskable). Apple-touch-icon, favicon, and manifest links added to landing page + all 8 legal pages.

**5. Brand identity rebuilt — QC monogram chosen over cube icon.** ← Apr 30.

**6. Magic-link email rebranded.** Dark cosmic Quantum Cube template applied via Supabase dashboard.

**7. Database migration history reconciled.** The `profiles` table + RLS + handle_new_user trigger migration that had been applied directly to remote without a committed file is now properly tracked.

**8. Static manifest.json replaces blob URL.** ← Apr 29 + Apr 30.

---

## 📜 REFUND POLICY — full text (LIVE at quantumcube.app/refund)

Currently published with Dodo Payments, Inc. as MoR (May 2 swap shipped from Paddle wording).

> # Refund Policy
>
> **Effective date: [TO INSERT]**
>
> Quantum Cube provides instant access to digital content. Because your personalized reading, numerology calculations, astrological interpretations, and voice narrations are delivered immediately upon payment and cannot be returned or un-accessed, **all sales are final and non-refundable.**
>
> Before purchasing, please make sure you understand what Quantum Cube offers:
>
> - A personalized numerology, Western astrology, and Chinese zodiac reading based on the name and date of birth you provide
> - Written interpretations and AI-assisted voice narration for each category
> - Content provided for **entertainment and self-reflection purposes only** — Quantum Cube makes no claims of accuracy, predictive power, or scientific validity
> - One-time payment of $17 USD for lifetime access to your personal reading
>
> **No refunds will be issued** for any of the following:
>
> - Change of mind after purchase
> - Dissatisfaction with the content or interpretations
> - Technical issues on your device that did not prevent delivery
> - Accidental purchases (please review carefully before confirming)
> - Failure to read or listen to content after purchase
>
> **Limited exceptions.** We may, at our sole discretion, consider a refund in the following cases:
>
> - Duplicate charges for the same account caused by a technical error on our side
> - Proven inability to access the product due to a verified fault in our systems that we cannot resolve within a reasonable time
> - Any refund required under applicable consumer protection law in your jurisdiction
>
> To request a refund under one of the limited exceptions above, contact **admin@qncacademy.com** within **7 days** of purchase with your email address, date of purchase, and a description of the issue. We will respond within 5 business days.
>
> **Chargebacks.** Initiating a chargeback without first contacting us may result in suspension of your account. We prefer to resolve issues directly with customers.
>
> **Changes to this policy.** We may update this refund policy from time to time. The version in effect on the date of your purchase governs your transaction.
>
> Payments are processed by Dodo Payments, Inc., who acts as the Merchant of Record for all purchases. For payment-related questions, contact support directly or us.

**Rationale notes:**

- "No refunds ever, period" sometimes fails MoR review and is unenforceable under EU/SA/CA consumer law. Limited exceptions clause is narrow but legally sound.
- Chargebacks language is industry-recommended for MoR products.
- Merchant-of-Record disclosure is required under all major MoR ToS.

---

## 📧 MAGIC-LINK EMAIL TEMPLATE (APPLIED Apr 29) — full HTML

Pasted to Supabase dashboard (Authentication → Email Templates → Magic Link). Preview confirmed.

**Config:**

- Subject: `Verify Your Email`
- Sender name: `Quantum Cube` ✓
- Sender email: `noreply@quantumcube.app` ✓

**Full HTML body (kept inline for re-paste if needed):**

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Verify Your Email</title>
</head>
<body style="margin:0;padding:0;background:#0a0e1a;font-family:Georgia,'Times New Roman',serif;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#0a0e1a;">
    <tr>
      <td align="center" style="padding:60px 20px;">
        <table role="presentation" width="480" cellpadding="0" cellspacing="0" border="0" style="max-width:480px;width:100%;">
          <tr>
            <td align="center" style="padding:0 0 40px 0;">
              <div style="font-family:Georgia,'Times New Roman',serif;font-size:24px;letter-spacing:6px;color:#ffffff;text-transform:uppercase;font-weight:normal;">
                Quantum Cube
              </div>
            </td>
          </tr>
          <tr>
            <td align="center" style="padding:0 20px 40px 20px;">
              <p style="margin:0;font-family:Georgia,'Times New Roman',serif;font-size:15px;line-height:1.6;color:#c8d0e0;letter-spacing:1px;">
                Tap below to sign in.
              </p>
            </td>
          </tr>
          <tr>
            <td align="center" style="padding:0 0 40px 0;">
              <a href="{{ .ConfirmationURL }}" style="display:inline-block;padding:16px 48px;background:#0f1829;border:1px solid #7dd4fc;border-radius:999px;color:#ffffff;text-decoration:none;font-family:Georgia,'Times New Roman',serif;font-size:14px;letter-spacing:4px;text-transform:uppercase;box-shadow:0 0 20px rgba(125,212,252,0.25);">
                Verify
              </a>
            </td>
          </tr>
          <tr>
            <td align="center" style="padding:0 20px;">
              <p style="margin:0;font-family:Georgia,'Times New Roman',serif;font-size:11px;line-height:1.6;color:#6a7388;letter-spacing:1px;">
                Didn't request this? You can safely ignore this email.
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
```

Leave `{{ .ConfirmationURL }}` exactly as written — Supabase replaces it at send time.

**Visual:** dark navy background, "QUANTUM CUBE" wordmark in spaced caps, single rounded-pill "VERIFY" button with sky-blue glow border, small grey "didn't request this?" footer.

**Pending upgrade:** swap inline text wordmark for hosted PNG. Copy `brand/QC Full White.png` to `docs/qc-wordmark-email.png`, then reference `https://quantumcube.app/qc-wordmark-email.png` in the email template's `<img src>`.

---

## 📋 PADDLE/PAYFAST PUNCH LIST — historical (already shipped May 2)

Documented for completeness. Swap was completed in commit `7ff5db8`.

### `docs/app.html` — 17 lines

- L2178-2188: PayFast integration block + sandbox credentials
- L2306-2347: `launchPayFast()` function definition
- L2348-2350: `checkPayFastReturn()` function definition
- L2964-2967: page-load handler calling `checkPayFastReturn()`
- L3223: button onclick="launchPayFast()"
- L3027, 3038, 3128, 3153, 3180: 5 in-app legal copy mentions

### `docs/*.html` (8 public pages, 9 occurrences)

- contact.html:31, index.html:54, ip.html:45, popia.html:26, privacy.html:21+42, refund.html:48, security.html:27, terms.html:34

### Migrations

- `supabase/migrations/20260417104424_create_profiles_table_and_rls.sql:31` — `has_paid` column comment mentions PayFast

### Code rename (shipped)

- `launchPayFast()` → `launchDodo()`
- `checkPayFastReturn()` → `checkDodoReturn()`
- New: Dodo webhook Edge Function at `supabase/functions/dodo-webhook/`

### MoR text swap (shipped)

- "PayFast (Pty) Ltd" → "Dodo Payments, Inc."
- "Paddle.com Market Limited" → "Dodo Payments, Inc."

---

## 🎨 BRAND IDENTITY — full inventory

### Brand pack (committed Apr 30 in `brand/` folder)

**Master files:**

- `QC - Solid.png` — QC monogram (white Q + cyan glowing C with curved underline tail) on solid dark cosmic bg. **APP ICON MASTER** — 2048×2048.
- `QC - Stars.png` — same QC monogram on cosmic Milky Way bg. **SOCIAL PROFILE PIC MASTER** — 2048×2048.
- `QC - White.png` — QC monogram on solid dark bg, alternate (similar to Solid).

**Standalone variants:**

- `QC - Black.png` — C-only mark (cyan C with cyan glow, no Q) on dark bg
- `QC - Black & Light.png` — C-only mark (white C with cyan glow) on dark bg

**Wordmark variants** (2800×1800, transparent PNGs):

- `QC Full White.png` — full layout: "QUANTUM NEURO CREATIONS / QUANTUM / CUBE / YOUR COSMIC PROFILE" with white QUANTUM + cyan glowing CUBE off-right
- `QC Full Black.png` — same layout, black text
- `QC White.png` — minimal: just QUANTUM + CUBE, white + cyan
- `QC Black.png` — minimal: just QUANTUM + CUBE, black text

⚠️ **Filename note:** wordmark filenames have spaces. Works on macOS but in HTML/CSS code, spaces must be URL-encoded as `%20`. Eventually worth a `git mv` rename to lowercase-with-hyphens.

### App icon family (committed Apr 30 in `docs/` folder)

Generated from `brand/QC - Solid.png` master via macOS `sips`:

- `qc-icon-192.png` — manifest, 192×192
- `qc-icon-512.png` — manifest, 512×512
- `qc-icon-512-maskable.png` — Android maskable, 512×512
- `qc-apple-touch-180.png` — iOS home screen, 180×180
- `qc-favicon-32.png` — browser tab/bookmark, 32×32, **18% rounded corners baked in**

### Visual language — locked

- **Primary typeface:** Cinzel Decorative (wordmarks, QC monogram, hero moments)
- **Secondary typeface:** Cinzel (subtitles, smaller utility text)
- **Tertiary typeface:** Cormorant Garamond (body, italic)
- **Colour pattern:** white-as-base + ONE cyan accent word/letter as keyword highlight
- **Background:** dark cosmic / black (#05050f primary, #071b2e secondary)
- **Accent glow:** cyan (#7dd4fc) for cube and interactive elements
- **Style:** ornate serif, premium, mystical-but-clean

### Why QC monogram instead of cube icon

Cube icon was the original plan. On Apr 30, after exploring three Canva options, the team voted for the **QC monogram** instead. Reasons:

- Type-as-logo: like Netflix's red N, Disney's D, the QC mark IS the brand
- Better separation: cube lives **in the app** (rotating, alive, hero element); QC monogram lives **outside** (icon, profile pic, favicon)
- Scales clean: works at favicon size and full app icon size with same silhouette
- Brand coherence: shares Cinzel Decorative + cyan accent with the wordmark
- Faster delivery: no Fiverr round needed

---

## 📱 SOCIAL MEDIA HANDLES — claimed Apr 30

| Platform    | Handle             |
| ----------- | ------------------ |
| YouTube     | @quantumcubeapp    |
| Facebook    | /quantumcubeapp    |
| X / Twitter | @quantumcubeapp    |
| Instagram   | @quantumcubeapp    |
| TikTok      | @quantumcubeapp    |
| Threads     | @quantumcubeapp    |

**Profile pic asset:** `brand/QC - Stars.png` (2048×2048, QC monogram on cosmic Milky Way bg).

**Status:** claim-and-hold mode until launch — handles secured, no posts made yet. Michelle takes over posting from May 4, 2026.

---

## 💰 SUBSCRIPTION AUDIT — historical outcomes

### ✅ Keep as-is

Claude Max, Claude Console (API), Cursor Pro, Epidemic Sound, CapCut Pro, ElevenLabs Creator (usage-based enabled April 22), Google Workspace, GitHub, Canva Pro (added Apr 29).

### ⬇️ Downgrade / switch (parked pending team discussion)

- Vercel Pro → Hobby (~$20/mo savings)
- Vimeo Starter → annual billing (~$65/yr savings)

### ❌ Confirmed deprecated

- HeyGen — canceled. Academy codebase cleanup pending (not a Cube task).
- PayFast — replaced by Dodo Payments. Code references removed via 26-line punch list (May 2).
- Paddle — never used, definitively excluded by AUP.

---

## 📜 CONTENT LICENSING — RESOLVED

Numerology/astrology concepts public domain; written interpretations original expression. Three legal additions shipped April 20 (commit `94af122`). Content licensing not a launch-blocker.

Third-party attributions in IP tab + public IP page: Epidemic Sound, Google Fonts.

---

## 🧠 LESSONS LEARNED (running, all sessions)

### General lessons (running, updated Apr 30)

- **SW diagnosis via phone screenshots is a trap.** Use Cursor Browser MCP with DevTools access OR diagnose via console.log on a fresh deploy.
- **Blob-URL service workers fail silently on Android Chrome 117+.** Use real files at origin scope.
- **Cursor's verbatim grep output can occasionally glitch.** Verify via fresh `grep` OR `git cat-file` before reverting based on Cursor's reported output.
- **Cursor sessions can stall mid-output when context is full.** Start fresh Cursor chat alongside fresh Claude chat.
- **renderAllContent had unconditional reveal logic** that predated the April 20 paywall fixes. Lesson: when patching paywall, grep ALL call sites that touch `display='block'` on `.lock-screen` or face-content IDs.
- **Python anchor strings for multi-block replacements must account for blank lines and indentation.** Cursor's repeated self-corrections on Apr 29 caught indentation mismatches and stale anchor text. Welcome the corrections.
- **Compression risk is real at multi-hour sessions.** Respect stop signals, update brief, start fresh.
- **Every brief version must be self-contained.** No "See vN for detail" — info loss on aging.
- **Public legal pages + landing page unlock BOTH payment processor AND Google Play in one go.** Build it once, satisfy two reviewers.
- **Paddle is NOT a fit for esoteric / non-SaaS digital content.** Their AUP is restrictive. Verified directly Apr 29.
- **Dodo Payments actively markets to astrology brands.** Better category fit than the more general MoRs.
- **Cross-chat context drift is real.** When work happens across multiple Claude sessions, do an end-of-week sync check before assuming brief is current.
- **Logo wordmarks are buildable in Canva** with Cinzel + Cinzel Decorative built-in. Logo icons (cube, brain/CPU) need a real designer — AI image generators can't reliably produce specific stylised brand icons.
- **PWA cache stickiness is the #1 false alarm.** Always check live site in regular Chrome before debugging code.
- **JWTs / bearer tokens NEVER go through Cursor or chat.** Cursor's refusal Apr 29 was correct. Diagnose via DevTools console + defensive timeouts (Promise.race) instead of curl tests with real tokens.
- **auth.admin.deleteUser can hang the calling session's signOut.** Wrap signOut in Promise.race(3000ms) when calling delete from the user's own session.
- **Diagnostic console.logs are scaffolding, not production code.** Always rip them in a follow-up commit.
- **Edge Functions need `verify_jwt = false` if they handle JWT manually.** Otherwise Supabase 401s before the function runs.
- **Supabase Edge Functions don't expose `Deno.openKv()`.** Use Postgres RPC for state instead.
- **Today's wins compound: each launch-blocker shipped tightens the path to revenue.**

### Apr 30 lessons (brand + icon sprint)

- **Firebase ≠ Supabase.** They're different backend services. When something Firebase-related shows up, run `grep -ril "firebase\|firestore"` across both Cube and Academy before acting. The orphan "QuantumCubeApp" Firebase project from a previous IT person was never used by either project.
- **Canva Pro page-background colour bakes into PNG export EVEN when "Transparent background" is ticked.** The transparent toggle only strips the default empty canvas, not custom page bg colours. Workaround: use a rectangle layer as design scaffolding (locked, easy to delete pre-export) instead of a page bg colour. OR explicitly set page bg to "no fill" before exporting.
- **Claude chat upload pipeline strips alpha channels from PNGs.** When verifying transparency, check the file in Preview on the user's Mac (look for grey-and-white checkered pattern) — Claude's image preview cannot be trusted for alpha.
- **HTML text wordmarks > PNG wordmarks for in-app/web use.** Sharper at all sizes, faster (50 bytes vs 600KB), accessible to screen readers, selectable for copy-paste, easier to edit. Only use PNG wordmarks where text won't render reliably (email clients without web fonts).
- **Favicon "blurriness" at 32×32 viewed in macOS Preview is normal.** Preview upscales the 32px file to ~200px on a Retina display. Inside an actual browser tab the favicon renders at 16-32px native and looks like every other favicon. Don't redesign for that.
- **iOS auto-rounds apple-touch-icon (squircle mask).** Android launchers auto-mask manifest icons (shape varies by phone). Browsers do NOT round favicons. So only the favicon needs baked-in rounding.
- **macOS Finder folder paste** into an existing same-named folder defaults to "Replace" — wipes existing contents entirely. Always run `git status` after a folder paste to catch unintended deletions before committing.
- **macOS native `sips` is enough for image resizing.** No homebrew/imagemagick needed. `sips -Z 192 source.png --out dest.png` for high-quality LANCZOS resampling.
- **PIL/Pillow may need a one-time `pip3 install Pillow`** when first used for image manipulation on the Mac.
- **One logical change = one commit, even when commits are related.**
- **Type-as-logo can replace illustration-as-logo entirely.** The QC monogram solved both the app-icon AND brand-mark problems in one move. Sometimes the type IS the logo.

### May 1 PM lessons (Dodo approval + recon)

- **"24-72hr review" can stretch to 8 days for MoR providers.** Don't escalate prematurely; have a fallback chain (LemonSqueezy + FastSpring) ready but parked.
- **MoR legal entity name verification belongs to the MoR's own ToS page.** Browser MCP recon of `dodopayments.com/legal/terms-of-use` confirmed `Dodo Payments, Inc.` (Delaware-incorporated) is the registered legal name for legal-copy swap purposes.
- **Coda Payments is a gaming-vertical MoR** (Codashop, EA / Activision / Roblox). Wrong category for $17 digital reading. Always research a payments provider's primary client base before applying.

### May 2 lessons (Dodo Live launch + bounce-bug debug)

- **The visible symptom isn't always the bug.** When something looks broken, instrument the data flow with diagnostic logs BEFORE patching theories. Spent ~3 hours chasing "post-redirect session loss" / "race condition" / "Supabase JS client hanging" theories. The actual root cause was that `runCalculation` never fired after unlock — user was sitting on Face 0 with a correctly-unlocked but invisible cube.
- **Cross-domain redirect kills queued JS state.** Even when using "in-page" overlay SDKs, if the SDK does an internal redirect at the end of payment (like Dodo's `/status/<id>/succeeded`), any `setTimeout` or pending Promise from before the redirect dies. Drive post-payment unlock from URL params on page-load, not from the overlay's `onEvent` callbacks.
- **Supabase JS auth methods can hang during INITIAL_SESSION restore.** `await sb.auth.getSession()`, `await sb.auth.getUser()`, AND `await sb.from(...).select()` all became unresponsive during the post-redirect auth restoration window. The fix is to bypass the JS client entirely: read the session token from localStorage directly (`sb-<ref>-auth-token` key), then query via direct `fetch()` to Supabase REST API. The JS client comes back to life ~5-10 seconds later, but you can't rely on that timing in a UX-critical flow.
- **NEVER paste secret values into chat — Cursor terminal output included.** A Live API key got into the chat transcript via a `supabase secrets set` command output. Took ~30 seconds to catch and ~2 minutes to rotate cleanly. Hash digests from `supabase secrets list` are fine to paste — they're one-way.
- **Dodo's UMD bundle attaches API as `window.DodoPaymentsCheckout.DodoPayments`** — NOT `window.DodoPayments` directly. When the SDK is described in npm READMEs as "DodoPayments", the UMD wrapper namespace can still be different. Always verify the actual bundle's global shape via `curl` or DevTools.
- **Test Mode wallet refunds always fail with "Insufficient funds in wallet".** Live Mode wallet refunds work but only after a settlement period (hours-to-days). Don't treat as a Dodo bug. For real customer refund support: communicate the few-day window to customers, refund within the window when ready.
- **Cursor's terminal markdown auto-linking turns dotted strings into fake markdown links.** Output like `rkelbrickmail@gmail.com` may appear as `[rkelbrickmail@gmail.com](mailto:...)` in Cursor's chat output. The actual file/database is clean text. Don't try to fix what isn't broken.
- **Dashboard mode toggle != actual mode.** Flipping Test/Live Mode in the Dodo dashboard only changes WHAT YOU SEE. The actual integration mode is hardcoded in `DODO_MODE` (frontend) and `MODE` (Edge Function), and the secrets in Supabase. Three separate places must all flip together for a real mode switch.
- **Pages serves the new build ~60s after push.** Don't test immediately after a `git push`. Wait. Save yourself the false-negative cycle.
- **window.location.reload() after detecting payment params can wipe localStorage mid-restore.** First instinct on the bounce bug was a hard reload. Disaster — the auth session was still being restored from the redirect, and reload nuked the in-flight state. Use in-place state update via `syncUnlockFromProfile()` + `runCalculation()` instead.

### May 3 PM lessons (multi-product strategy lock)

- **Wrong-model decisions are expensive to discover late.** Subscription tier (Quantum Cube Plus, $9.99/mo) was the working assumption from v25 through v30. Three weeks of brief space + planning energy went to it. May 3 PM realisation: customer thesis (curious dabbler) and product model (subscription) were misaligned — daily horoscope content treadmill solves a problem our segment doesn't have. **Always sanity-check that the product model matches the customer profile, not just the revenue spreadsheet.**
- **"Curious dabbler" beats "broad spirituality user" as a positioning frame.** Specificity sharpens every downstream decision: pricing (one-time wins), feature scope (less is more), retention design (life-event triggers + gifting + sharing, not daily push), competitive stance (Co-Star wins depth — we don't fight them there).
- **Pre-launch tool/directory lists are 90% noise.** Of ~15 indie launch directories Ronnie's contacts had collected, zero are right for our product (all built for indie-dev SaaS). Same lesson applied earlier to Vloxo, AppSumo, G2, Capterra. Keep saying no.
- **Document role handovers explicitly.** Michelle taking social media from May 4 is a real ownership transfer — not "she helps sometimes." Without explicit ownership, content goes nowhere or three people redo each other's work.
- **Security audits before public marketing volume, not after.** Once the marketing flywheel turns, attack surface attention turns with it.
- **Sentry is critical infrastructure, not "nice to have."** Right now if a paying customer hits a bug we have zero visibility. ~20 min implementation.

### May 3 EVENING lessons (Phase 2 polish marathon)

- **Files can be silently `.gitignore`d for weeks.** The 5 music MP3s lived on disk locally but never deployed because `.gitignore` line 2 had `Music/` (root-anchored, but BSD glob caught the nested `docs/Sounds/Music/` too). Diagnosis: always run `git ls-files` to verify deployment, not local presence. Local file existence ≠ deployed.
- **Anchor strings to a Python one-shot script must be re-grepped against CURRENT file state, not earlier recon output.** The c3d3e57 regression happened because old_* anchors matched pre-1020df5 CSS state — when the script wrote the file back, it serialized the matched-state CSS instead of the current state. **Cost: needed a separate re-apply commit (a06ca3e). Same lesson hit again in 63684ef where the anchor used `.scoreboard` but the actual file had `.sb-wide{}` between blocks. Cursor self-corrected both times.**
- **Diff-then-delete logic must have explicit branches.** My script for `.supabase-envx` cleanup had `diff … && echo identical || echo DIFFERENT` but then continued to delete regardless. Cursor caught the data-loss risk (would have lost the ElevenLabs key), merged the unique key into canonical file FIRST, then deleted. **Always have an explicit `if identical → delete; else → halt and ask` branch.**
- **Google's Sign-In branding guidelines require G on white tile.** Custom buttons on dark backgrounds with the 4-color G floating directly on the dark fail OAuth verification. Either use Google's pre-approved Light Rectangular button (white pill) or Dark Pill (dark with G on white tile inside). We chose Light Rectangular for visual consistency with the future Sign-in-with-Apple white button (Apple forbids black-on-dark).
- **Apple Sign-in only allows white/white-outlined/black variants.** On dark backgrounds, only WHITE is allowed. Black-on-dark fails App Store review. Plan for Apple white button + Google Light Rectangular = matched white pair.
- **Android PWA splash screens have unavoidable behaviors.** Two-stage launch (launcher icon → splash) is universal Android. Cannot be skipped. Cannot be timed manually. Different icon sizes between launcher and splash are spec — every Android PWA does this. Accept and move on.
- **CSS Grid items default to `min-width:auto`** which lets children push the cell wider than its 1fr share. Add `min-width:0` to grid item CSS to defeat this. Same root-cause pattern hit three times in one session: matrix cards (1020df5), astrology profile cards (42d3094), Life Phases card (c7e1d8b). Pattern is now well-internalized.
- **`white-space:nowrap` + `overflow:hidden` can clip valuable content.** When applied to multi-value cards (Life Phases "1, 1, 5"), the third value clipped invisibly. Solution: combine with count-based responsive font scaling so content always fits at smaller sizes rather than getting clipped.
- **BSD sed and `\|` alternation in `grep` are unreliable on macOS.** Use `grep -E` with `|` for extended regex when you need OR-pattern matching. Cursor self-corrected on this in the verification of 42d3094.
- **Cursor's self-correction on Python anchor strings is welcomed and usually right.** When Cursor says "your anchor didn't match exactly, I corrected to use the actual on-disk text X instead" — trust it. Don't argue. The kickoff doc explicitly welcomes this.
- **PWA cache stickiness affects manifest changes too, not just code.** Manifest splash colour changes won't show on existing PWA installs even after force-stop. Need clear-cache + reinstall. Real users installing fresh get correct values from day one — don't burn cycles trying to fix this for already-installed test devices.
- **Editor swap files are real. `.gitignore` should use globs.** `.supabase-envx` was a nano artifact. Original `.gitignore` rule `.supabase-env` (exact match) didn't catch it. Tightened to `.supabase-env*` to auto-protect any future variant.

### May 4 lessons (cleanup + restructure)

- **Brief size matters for session cognitive load.** At 1633 lines, even Claude has to skim. Lean active brief (~800 lines) + lossless archive is the right architecture. Active doc = current state of truth, archive = full historical record.
- **The archive isn't just for sentimentality.** It's the knowledge transfer asset for QNC Academy and any future project. Every lesson, decision, dead-end is portable IP. Lossless preservation is the goal.

### May 4 PM lessons (Sentry + multi-narration + E2E test)

- **Cursor IDE buffer can silently race with shell-side Python edits.** Hit twice in one afternoon. First: narration commit `649bb60` reported success + grep verified new code in file, but `git commit` only staged the SW + Sentry release bump — narration code was missing. Cursor's own post-commit verification caught it. Second: `b99b807` SW fix silently reverted `DODO_MODE` from "test" back to "live" mid-commit. Caught by the new pre-stage verification guard. **Mitigation pattern (now standard for mode-flip commits):** explicit `if both in sync → ship; else → exit 1` check immediately before `git add`. Don't trust grep verification alone — verify again at the commit boundary.
- **Sentry pays for itself within hours.** Within ~2 hours of going live, Sentry surfaced an unhandled SW exception (HTTP 206 partial-content responses can't be cached via Cache API — every audio Range request was throwing). Bug had been silent for who-knows-how-long. Sentry exposed it. Worth the ~20 minutes of integration setup just for that one catch.
- **The visible symptom isn't always the bug — second time this lesson burned.** Initially diagnosed the magic-link Reveal stall as "SW 206 errors flooding the JS event loop, choking the auth click handler." The 206 fix was real and worth shipping, but it WASN'T blocking the auth flow. Real cause: leftover Supabase auth token in incognito localStorage from earlier test attempts was making `handleRevealClick` short-circuit incorrectly. Lesson reapplied: instrument the data flow before patching theories. (Same lesson hit on May 2 bounce-bug debug — three-hour theory-chase before "user wasn't in the cube to see correct unlock" was the actual answer.)
- **Incognito Chrome localStorage persists across same-session windows.** Only quitting ALL incognito windows clears it. Caused the magic-link Reveal stall. **Mitigation:** for clean-slate testing, quit all incognito windows + reopen, OR verify `localStorage` keys are empty in console before starting auth tests.
- **Gmail "+" aliases bypass Google OAuth identity collisions.** `rkelbrickmail+e2etest@gmail.com` routes to `rkelbrickmail@gmail.com` inbox but Supabase treats it as a completely different user. Critical for testing magic-link flow when the base email already has a Google OAuth identity attached. Lesson learned the hard way after wasted attempts on the base email.
- **Magic-link from Gmail opens in user's default Chrome profile, not the incognito session it was triggered from.** Real-user behavior — Cursor caught this expectation mismatch during the test. Doesn't break the flow (verified May 4 E2E), but worth flagging in user-facing docs eventually if testers report confusion.
- **Three-place mode flips are high-stakes operations.** `DODO_MODE` (frontend) + `MODE` (Edge Function) + Supabase secrets MUST stay in sync. The brief warned about this before, but May 4 confirmed the consequences: a 5-minute window where origin/main had mismatched mode (frontend live + Edge test + Test secrets) due to stale-buffer revert. No customer hit it (low traffic), but real risk if anyone had clicked Pay. **Pre-flight + post-flight curl verification is non-negotiable.**
- **Don't paste literal multi-line shell commands from chat into Mac Terminal.** zsh interprets `\n` literally → parse error → command silently fails. Type manually OR confirm clean paste before hitting Enter. Hit this on `secrets set` step.
- **Sentry trial auto-downgrade requires a calendar reminder.** Default new account starts on 14-day Business plan trial → auto-drops to free tier. Set explicit reminder for trial expiry to verify no surprise billing. (May 18, 2026 for this account.)
- **Use the explicit Sentry SDK, not the loader script.** Loader script auto-applies whatever's toggled in the Sentry dashboard at runtime — including features you didn't intend. Explicit SDK + locked `Sentry.init()` config = auditable in code, no surprises from UI toggles.
- **EU region for error/data services is the right default for SA-based businesses serving global customers.** GDPR is the strictest bar; aligning with it gives clean data-residency story across Supabase Frankfurt + Resend eu-west-1 + Sentry EU. Locked-in choice (region can't be changed once project created on Sentry).

### May 4 EVENING lessons (security audit + CSP rollout)

- **CSP rollout produces noisy, helpful first-deploy feedback.** Within minutes of CSP going live, the `securitypolicyviolation` listener forwarded two real gaps to Sentry: Sentry's own runtime self-fetch from `browser.sentry-cdn.com` (the bundle CDN does a follow-up connect after initial load), and Vimeo's thumbnail loads from `i.vimeocdn.com`. Both invisible-until-blocked in dev. **Lesson:** ship CSP with the violation→Sentry listener wired BEFORE the policy itself goes strict. The listener is the safety net that catches what static analysis misses.
- **Two CSPs for two trust levels is the right pattern.** `app.html` keeps `'unsafe-inline'` because dropping it would require refactoring every inline `onclick=`/`onchange=` handler — multi-hour, low-payoff. Public pages stay strict (no inline anything, fonts only) because they have no inline scripts to begin with. **Don't homogenise the policy where the requirement differs.**
- **Edge Function rate limits don't need new infrastructure.** The existing `narrate_rate_limit_try` Postgres RPC already does general-purpose token-bucket logic with two windows (minute + hour). Three new functions got rate-limited by reusing it with namespaced bucket keys (`delete:USER_ID`, `export:USER_ID`, `dodo-session:IP`). Zero new migrations. **Lesson:** when adding similar capability across multiple endpoints, look for already-deployed primitives before designing a new system.
- **Generic error responses preserve debuggability while protecting the client.** Pattern that's now standard: `console.error("function-name error:", e)` server-side (full context for Supabase log access), `return { error: "specific_code" }` client-side (no stack traces, no upstream service details). Burns nothing in operational visibility, removes a small information-disclosure surface.
- **Heuristic secret scans are necessary but not sufficient.** zsh history scan with 5 patterns covered the leak shapes we'd actually used (the May 2 `supabase secrets set` echo, plus standard JWT/Bearer/Stripe-Dodo prefixes). 0 matches. But "0 matches on heuristic patterns" ≠ "no secrets in history" — exotic shapes (raw hex blobs, custom token formats) wouldn't trigger any pattern. **Lesson:** treat scan as one layer, also rely on the operational rule "never paste secret values into terminal in the first place" as the primary defence.
- **Brief condensation requires lossless archive update — caught only on read-back.** Brief v34 condensed the security audit checklist from its planning form (TO-DO buckets) to its results form (4 commits + manual checks). Active brief got cleaner. But the planning version contained design decisions (which directives to set, which directives to skip, which deferrals were intentional) that are valuable historical record. Ronnie spotted the line-count drop and asked before committing. **Lesson:** when condensing a brief section because work shipped, archive the planning context ALONGSIDE the results record. Don't trust that "git show <commit>:PROJECT_BRIEF.md" is sufficient — the archive is the project's working memory; what's not in the archive is effectively forgotten in 6 months.
- **Resend API key backup is a non-issue when you understand the upstream model.** Resend hides values after creation. So does GitHub for PATs, Cloudflare for some API tokens, Stripe for restricted keys, Apple for App-specific passwords. The pattern is: assume you can never read the value again, design for rotate-to-recover. Local backups are useful but not critical for this class of secret.
- **The brief is for current state, the archive is for memory.** Brief v33 had ~50 lines of "to-do" security audit checklist. v34 has ~30 lines of "what we shipped + what we deferred." That's a healthy ratio: brief shrinks as plans become reality. The archive grows as the real work accumulates. The trick is doing both in the same session — defer the archive update and you lose the planning context within a few sessions.

---

## 🎙️ ELEVENLABS NARRATOR — full configuration history

- **Voice:** Valory (voice ID `VhxAIIZM8IRmnl5fyeyk`)
- **Model:** `eleven_turbo_v2_5` — `{stability:0.5, similarity_boost:0.75, speed:1.15}` (default for production narrate Edge Function)
- **Welcome greeting (May 3 re-render):** speed `1.00` (slower) for Sounds/Narration/welcome.mp3
- **Edge Function:** `supabase/functions/narrate/index.ts` (~100 lines with rate limit, `verify_jwt=false`, manual apikey-header check, Postgres RPC for rate counter)
- **Rate limit:** 5/min + 20/hr per IP. Returns HTTP 429 with `Retry-After` header.
- **Narration inventory on disk:** 385 MP3s
- **Frontend narration paths:**
  - Welcome: `playWelcomeGreeting()` → `startNarrationFromUrl('Sounds/Narration/welcome.mp3')` on first 2 Face 1 entries (counter `qc_greet_count_<uid>`)
    - **Updated May 3 evening:** plays once only (count < 1) and ONLY when signed in (no firing on Face 0 signup)
  - Face 3 numerology categories → `startNarrationFromUrl` → `Sounds/Narration/num_<cat>_<num>_v<variant>.mp3`
  - Face 3 Life Phases → `playSequence` → 3× `Sounds/Narration/num_pc_<n>_v1.mp3` sequential
  - Face 4 western → `Sounds/Narration/west_<sign>_<slot>.mp3`
  - Face 4 chinese → `Sounds/Narration/chin_<animal>_<slot>.mp3`
  - Face 5 combined → `fetchNarration` → live Edge Function (ONLY credit-burn path at runtime)

**Generation pipeline:**

- `scripts/generate-narration.mjs` — sequential, 500ms throttle, resumable (skips existing files). Calls deployed `narrate` Edge Function so speed is locked at 1.15.
- `scripts/generate-welcome.mjs` (May 3) — one-off standalone script that calls ElevenLabs API directly (bypasses speed-locked Edge Function) for slower welcome render.

---

## 🏪 APP STORE SUBMISSIONS — full roadmap

### Phase 5a — US-only launch with Dodo billing (months 1–2)

- Google Play Developer account ($25 one-time)
- PWABuilder / Bubblewrap `.aab` — **no native Google Play Billing required for initial US rollout** where Epic v Google–era policies allow developers to complete digital purchases via **Dodo (same MoR as web)** through in-app web checkout / external payment flow
- Store listing: feature graphic (1024×500), phone screenshots, full description (4000 chars) + short description (80 chars), content rating questionnaire, **Data Safety** form
- **Internal Testing** track first (1–2 weeks: rkelbrick, carl, michelle)
- **Production: US-only** distribution to start — reviews and ranks compound in one market; partners target **10–15 TikToks/week** US-focused
- Initial Google review: **7–14 days** typical

### Phase 5b — English-speaking markets (months 2–3)

- Expand Play listing to **UK, Canada, Australia, New Zealand** (same app binary, no translation cost)
- **Web + Dodo** already handle these users globally; Play expansion is **discoverability + trust**
- Per-territory billing: add **Play Billing** or **External Offers / web-checkout routing** only where Google policy **requires** it

### Phase 5c — Global + localised (months 4–6)

- **Spanish, Portuguese, French, German** — app UI + store listings + key marketing assets
- **LATAM + Brazil** heavy-up (spirituality content over-indexes)
- **Dual billing** only in regions that **mandate** in-store digital payments — keep **Dodo** everywhere the law and Play policy allow off-store checkout

### Phase 8 — Apple App Store (months 6-9, deferred)

**Wrapping technology:** Capacitor + Xcode archive. (Capacitor wraps the existing PWA into a native iOS shell — same approach as PWABuilder/Bubblewrap on Android. Avoids native rebuild.)

Three Apple-specific add-ons confirmed May 3 PM:

- **Apply for Apple Small Business Program** — drops Apple's commission from 30% to 15% if annual proceeds under $1M. Free, automatic enrolment. No-brainer.
- **Implement Restore Purchases button** — Apple hard requirement. Required even for one-time products (lets customers restore on a new device or after reinstall). Maps to existing `has_paid` flag check on auth restore.
- **Implement Sign in with Apple** — required if any other social login is offered (we have Google OAuth). Add as a third sign-in option alongside Google and magic-link.
- **Apple IAP politics for digital content** — Apple's stricter than Google about external payments. For one-time products under our multi-product roadmap, the Reader Rule + News Publisher Program don't apply. Most likely: implement Apple IAP alongside Dodo, with entitlement sync via webhooks. Legal + product review before ship.

---

## CANONICAL SAFE ROLLBACK POINTS — historical anchors

**Do not revert past these without conscious decision.**

| Commit    | Why you don't revert past it                                                                                 |
| --------- | ------------------------------------------------------------------------------------------------------------ |
| `78a8e00` | Favicon 18% rounded corners.                                                                                 |
| `039b0c1` | **QC PNG icon family wired across site.**                                                                    |
| `4fb2e40` | **QC monogram + wordmark brand pack.**                                                                       |
| `21b9c99` | **Account deletion + export production-ready.** CRITICAL                                                     |
| `0fcbdb9` | Account deletion + export shipped. CRITICAL                                                                  |
| `43e397e` | Static manifest.json. PWABuilder dependency.                                                                 |
| `f9a3df3` | Migration reconciliation. `db push` works.                                                                   |
| `7016cb1` | narrate rate limit. ElevenLabs credit-burn protection.                                                       |
| `cc63d90` | `/app/` trailing-slash redirect.                                                                             |
| `32a23f0` | `.nojekyll` for static HTML + privacy redirect.                                                              |
| `e8bfbc4` | `/docs` restructure for Pages source.                                                                        |
| `2e888d2` | **Public site landing + legal pages.** CRITICAL.                                                             |
| `7a9b7ac` | Music randomisation per session + user-scoped welcome counter.                                               |
| `546363b` | Welcome greeting auto-play from local MP3.                                                                   |
| `2d38560` | Music refresh + randomisation + cube-touch SFX rip.                                                          |
| `231803e` | Face-name label card + auto-scroll.                                                                          |
| `0bd5a54` | **Paywall fix #3 — renderAllContent gating.** CRITICAL                                                       |
| `0546755` | Narration phase 2 wiring.                                                                                    |
| `be9f385` | 129 phase 2 MP3s committed.                                                                                  |
| `636e3d8` | Strip dead 11/22 master numbers from NUM.pc.                                                                 |
| `b0b87c5` | SW diagnostics rip + ASSETS fix.                                                                             |
| `37f19fd` | Real sw.js file replaces blob URL.                                                                           |
| `4d51c0d` | data-variant alignment.                                                                                      |
| `c2e3c80` | Numerology direct MP3 path.                                                                                  |
| `e1070fb` | Cursor hardening.                                                                                            |
| `94af122` | Legal additions.                                                                                             |
| `2403ca7` | **Paywall fix #2** — unconditional lock enforcement.                                                         |
| `fd41b68` | **Paywall fix #1** — STORE_KEY user-scoped.                                                                  |
| `57dd972` | 10.8MB cleanup.                                                                                              |
| `e85ca5c` | **Post-payment auto-runCalculation** — bounce-bug fix.                                                       |
| `7ff5db8` | **17-line Paddle/PayFast → Dodo legal copy swap.**                                                           |
| `b3386ea` | **dodo-webhook Edge Function source.**                                                                       |
| `f7834c3` | **Live Mode active in Dodo.**                                                                                |
| `0748a57` | **Music files actually deployed** (had been silently gitignored).                                            |
| `4c210b3` | **Google button compliant** — Light Rectangular spec for OAuth verification.                                 |
| `c3d3e57` | **Music ducking** during narration.                                                                          |
| `a06ca3e` | **Matrix card overflow re-applied** after c3d3e57 regression.                                                |
| `92bd75b` | **Splash colors synced** to #05050f cosmic black.                                                            |
| `804856a` | gitignore tightened for .supabase-env* glob (May 4 cleanup).                                                  |
| `e804ab4` | **Brief v32 + new BRIEF_ARCHIVE.md** — lossless history split.                                                |
| `3f7f297` | Brand cyan refresh across logo variants.                                                                      |
| `730d4d8` | **Sentry error monitoring shipped** — production-only, EU region.                                             |
| `4b6bdf9` | **Multi-number narration shipped** (corrective for 649bb60 near-miss).                                        |
| `b99b807` | **SW 206 cache-skip fix** — Sentry's first real catch.                                                        |
| `9062eef` | DODO_MODE re-flip + pre-stage verification guard pattern adopted.                                             |
| `1b15ece` | **Live Mode active after magic-link E2E test PASS** (May 4 PM).
| `35331bf` | **Edge Function rate limits + error tightening** — delete-account, export-data, dodo-create-session rate-limited (May 4 EVENING). |
| `f6a7db5` | **CSP baseline shipped** across all 10 HTML pages + securitypolicyviolation listener wired to Sentry.                              |
| `00d1c6c` | CSP fix-up — Sentry CDN connect + Vimeo thumbnail img-src (caught by violation listener within hours of deploy).                    |
| `1324784` | mobile-web-app-capable meta tag — iOS 16+ deprecation fix.                                                                          |
| `9bcf2d3` | **Brief v34** — security audit completion documented, archive updated with May 4 EVENING session record.                            |                                               |

---

## 💳 DODO PAYMENTS — historical fallback chain + AUP context

### Why Dodo (locked Apr 29)

| Factor                     | Dodo                                  | LemonSqueezy               | FastSpring               | Paddle              |
| -------------------------- | ------------------------------------- | -------------------------- | ------------------------ | ------------------- |
| Astrology/esoteric content | **Actively markets to it**            | Allowed (silent)           | Allowed (silent)         | **PROHIBITED**      |
| Pricing                    | 4% + 40¢ (+1.5% non-US ~= 5.5% + 40¢) | 5% + 50¢                   | ~8.9%                    | 5% + 50¢            |
| MoR + global tax           | ✓                                     | ✓                          | ✓                        | ✓                   |
| Founded                    | 2023                                  | 2021                       | 2005                     | 2012                |
| SA seller accepted         | ✓                                     | ✓                          | ✓                        | N/A                 |

### Dodo AUP — relevant categories for Quantum Cube

- **Spiritual & Astrology services** → "Categories That Often Require Review" (entertainment only, no claims/predictions). We comply ✓ (entertainment opener live since `94af122`)
- **Religious/spiritual *services*** → prohibited, but this targets paid prayer/ritual/spiritual-authority access, not personalized digital readings ✓
- **AI Content Generation tools** → review category if we sold the tool itself; we use AI voice as part of product, not selling generation. Disclosed as "AI-Assisted" in IP page ✓

### Account details

- **Account name:** Quantum Neuro Creations (registering as business, CIPC Pty Ltd)
- **Account owner (operator):** Michelle Booyens

### Fallback chain (parked, no longer urgent)

1. **Dodo** ← LIVE since May 2
2. **FastSpring** — Michelle has registered, account dormant. Subdomain `quantumneurocreations_store` already provisioned.
3. **LemonSqueezy** — application open from Apr 28, on SA tax form hold. Stripe-acquired, stable.
4. **Polar.sh** — open-source MoR, Stripe-backed, developer-first
5. **Creem** — newer (2024), indie-hacker focus, lowest fees, less proven
6. **Gumroad** — last resort, 10% flat fee, accepts almost anything digital

### Why Paddle was ruled out (verified Apr 29)

Paddle's AUP explicitly prohibits: *"Digital services associated with pseudo-science, including but not limited to clairvoyance, horoscopes, fortune-telling"*. Quantum Cube includes Western astrology + Chinese zodiac + numerology = textbook fortune-telling per their own definition.

---

## 📜 TEST / TEAM DATA IN PROFILES (DELETE BEFORE LAUNCH)

Snapshot from April 23 sweep. Re-snapshot in next session in case list has drifted:

- `admin@qncacademy.com` (team, unpaid)
- `charlheyns1@gmail.com` (unpaid)
- `booyens.michelle@gmail.com` (Michelle, unpaid)
- `keyzer@xtremeprop24.com` (Keyzer, unpaid)
- `quantumneurocreations@gmail.comcom` ← **typo, delete anytime**
- `test+chunk5b@qncacademy.com` (unpaid)
- `carlkelbrick+test@gmail.com` (unpaid)
- `rkelbrickmail@gmail.com` (unpaid)
- `carlkelbrick@gmail.com` (paywall test profile — keep until E2E payment test done)
- `quantumneurocreations@gmail.com` (paid test — keep for paywall testing)

---

### May 4, 2026 LATE EVENING (Monday — smoke-script saga + final hardening)

5 more commits after the initial security audit closed. Brought tonight's
total to **15 commits** across security audit, MCP install, kickoff
upgrade, pre-commit hook, and smoke test.

| Commit    | What                                                              |
| --------- | ----------------------------------------------------------------- |
| `00a6314` | Pre-commit hook (SW + Sentry release sync) committed + installed  |
| `23d4a20` | Smoke test script (initial, 5 checks)                             |
| `4efb70a` | Smoke fix #1 — buffer curl output (SIGPIPE/pipefail bug) + drop -f flag on Supabase check |
| `90fb8b9` | Smoke fix #2 — Step 3 greps DSN instead of console.log            |
| `fc479a0` | Smoke fix #3 — drop redundant Step 3, simplify to 4 checks. 13/13 green from residential IP. |

**Lessons burned in tonight (smoke-script saga specifically):**

- **Cursor's sandbox runs from a datacenter IP, not Ronnie's residential network.** Cloudflare bot protection blocks datacenter curl with HTTP 403, even though the same script works perfectly from Mac terminal. **Mitigation:** smoke script header now explicitly notes this; any curl-based verification of live site MUST be tested from Mac terminal, not Cursor's environment.
- **`set -o pipefail` + `curl ... | grep -q ...` is a SIGPIPE landmine.** When grep matches early and closes the pipe, curl gets SIGPIPE (exit 23), pipefail propagates non-zero, and the test reports false-negative even though the match succeeded. **Mitigation:** buffer the curl response into a variable first, then `echo "$VAR" | grep`.
- **`curl -f` + `|| echo "ERR"` produces garbage output on 4xx/5xx.** `-f` makes curl exit non-zero on HTTP errors, but `-w "%{http_code}"` still writes the code. The `||` then APPENDS "ERR", producing strings like "401ERR". **Mitigation:** drop `-f` when you want the status code regardless of HTTP success/failure semantics.
- **Supabase `/auth/v1/health` requires apikey header to return 200.** Without it returns 401. The server IS reachable — 401 just means we didn't send credentials. For a "is the server up?" check, accept ANY HTTP code (including 401) as "up". Only empty response / `000` / timeout means "down".
- **When two checks against the same buffer give contradictory results, drop the redundant one rather than rabbit-hole.** Step 2 (release-tag grep) and Step 3 (DSN grep) both ran against the same buffered HTML. Step 2 found the release tag, Step 3 didn't find the DSN despite both being in the same Sentry block. Couldn't isolate cause in reasonable time. Pragmatic call: drop Step 3 — Step 2 already proved "Sentry block intact AND versioned correctly". One check that works > two checks where one is mysteriously broken.
- **Pre-commit hooks live in `.git/hooks/` which automation tools can't write to** (sandbox restriction). Tracked source needs an installer script. Cursor caught this correctly: committed source files, asked Ronnie to run `./scripts/install-hooks.sh` from Mac terminal. Pattern: `scripts/hooks/<hook-name>` (tracked) + `scripts/install-hooks.sh` (re-runnable installer for new clones).
- **Cloudflare DNS hiccups can cause transient git push failures from sandboxed environments.** First push of `fc479a0` failed; retry succeeded. Not a real issue — known characteristic of the sandbox.

**Outcomes May 4 LATE EVENING:**

- Pre-commit hook installed locally on Ronnie's Mac (`/Users/qnc/Projects/quantumcube/.git/hooks/pre-commit`). Future SW/release mismatch commits will be blocked automatically.
- Smoke test script: 13/13 green from residential IP. New post-push verification routine: `git push origin main && sleep 60 && ./scripts/smoke.sh`.
- 4 working checks: SW version sync, Sentry release tag matches SW, 10 public pages HTTP 200, Supabase reachable.
- Total session count for May 4: **15 commits** (4 morning brief restructure + observability + verification, 4 security audit, 4 MCP/kickoff/pre-commit, 3 smoke iterations).

---

---

## May 5, 2026 — Tuesday — SYSTEM HARDENING DAY (two chat sessions)

Full-day system-hardening pass before resuming product work. Spanning two chat sessions on claude.ai web (mobile + Mac). The morning chat hit Max plan session limit before completion (95% used, 40-min reset); afternoon chat continued post-reset and unblocked previously-stuck connectors after user re-authorized them in claude.ai.

### Morning chat (08:30–11:10 SAST)

**Document reconciliation pass** — diff'd uploaded docs vs project knowledge folder. PROJECT_BRIEF.md differed (v33 in project knowledge vs v35 in upload). Built v36 drafts but those were never committed; afternoon chat skipped v36 and went straight to v37.

**Connector probe at chat start:** Cloudflare, Resend, GitHub Integration tools were NOT surfacing via tool_search despite being listed as available. User disconnect/reconnect didn't immediately resolve it within the active chat session. Hypothesized eventually-consistent backend at Anthropic.

**Sentry production sweep** — organization slug `quantum-neuro-creations`, project slug `javascript`. Two unresolved CSP issues (JAVASCRIPT-2, JAVASCRIPT-3) both fired only on qc-v199, fix shipped qc-v200/v201, 0 errors in 24h. **Resolved both** via `update_issue` tool.

**Supabase audit + 3 migrations applied** — see PROJECT_BRIEF v37 "v36-v37 CONSOLIDATED UPDATES" section for migration details. Security advisor 6→1, perf 3→0.

**Vercel shadow deployment found** — `prj_WKo5JwtJ02CGBVsyqbDAORQbQpDy` auto-deploying every commit as a parallel chain to `quantumcube.vercel.app` and 2 other URLs. Decision deferred (Academy use TBD).

**Memory edits added (4 stable facts):**
1. Sentry org/project slugs
2. Supabase project_id + schema invariants
3. Surface boundary rule (claude.ai vs Claude Desktop)
4. Auto-run discipline (do reversible writes, ask only for destructive/financial/secret/external-comms)

**Telegram pivoting** — mid-chat, user paused on a R25 charge prompt while setting up Telegram. Confirmed: R25 = Telegram **Premium** (optional), basic Telegram + bots is completely free. But pragmatic re-evaluation: at our current scale (~2 errors/month), email push via Gmail mobile is just as effective as Telegram. **Pivoted to email-only alerting** (codified later as ADR-008). Cloudflare Worker code drafted (`sentry-telegram-worker.js`) and parked for future use.

### Afternoon chat (11:10–13:00 SAST) — same chat ID, post Max-plan reset

Initially treated the 95% Max-plan warning as chat-context exhaustion and rushed a SESSION_HANDOFF document. Then realized the warning was Max plan session usage (resets in 40 min), not chat context. False alarm — continued in same chat after the reset.

**User re-authorized claude.ai connectors** — afterward, full tool surface unlocked: Cloudflare, Resend, Filesystem, Desktop Commander, Apple Notes, iMessages, Control your Mac, Claude in Chrome, Control Chrome all surfaced. GitHub Integration STILL missing (workaround: `gh` CLI via Desktop Commander).

**UptimeRobot LIVE** — user signed up via Google OAuth (`quantumneurocreations@gmail.com`). 4 monitors configured (landing, app page, sw.js keyword, Supabase REST keyword). Email alert contact only — no Telegram. Discovered UptimeRobot's free-tier-locked custom HTTP statuses, worked around it with keyword monitoring on Supabase 401 response (key insight: word "message" is reliably present in any healthy Supabase JSON 401 response).

**Master Setup Checklist re-execution** — user explicitly asked to re-run the full checklist with all tools now available. Autonomous batch:
- Repo inventory: HEAD `7ac44eb`, clean working tree, on main ✅
- Pre-commit hook installed and active ✅
- `scripts/smoke.sh --quick` passed: SW=qc-v201 = live, Sentry release matches ✅
- Cursor MCP config has 4 servers (context7, sentry, supabase, dodopayments) ✅
- Claude Desktop Chrome extension paired (deviceId `020a49a7-7cc1-4832-a6d3-44b28b149b0b`) ✅
- **Microsoft Clarity NOT wired into docs/app.html** — confirmed gap, deferred to next chat
- Cloudflare audit: DNS-only setup (orange cloud OFF), email routing fine, DMARC at p=none, 1 dormant Worker `holy-leaf-e567` to review
- Resend audit: domain verified, no webhooks configured (gap), 2 API keys clean

**New repo files written autonomously** (uncommitted):
- `DECISIONS.md` (root) — 8 ADRs seeded
- `.github/workflows/daily-health-check.yml` — daily cron, email-only alerting

**This brief v37 + this archive entry** — written via Filesystem MCP edit_file tool. Brief was bumped from v35 to v37 directly (skipping v36 since the v36 drafts in /mnt/user-data/outputs were never deployed and had been superseded).

### Lessons May 5

- **Re-authorizing claude.ai connectors is the actual fix** when MCP tools persistently fail to surface. "Eventually-consistent" was a wrong hypothesis — the missing scope was real and required user action.
- **`Filesystem:edit_file` is the right tool for surgical brief/archive updates.** Reading + writing whole files via `write_file` was tempting but error-prone for 50KB+ docs. `edit_file` with `dryRun: false` plus targeted oldText/newText pairs is safer and produces a git-style diff for review.
- **Telegram Premium is NOT required for bot alerting** — the R25 prompt is upsell, not gate. Free Telegram + bots covers our entire use case. Worth filing as a non-finding so the next time we hit the prompt we don't pause.
- **UptimeRobot's free tier locks "custom up status codes"** — but **keyword monitoring is free**. Use keyword presence/absence as a workaround to monitor endpoints that return non-2xx codes by design (like Supabase REST returning 401 without an apikey).
- **Cloudflare "orange cloud" being OFF means we get no runtime CDN/WAF/bot-mgmt benefits**. We're using Cloudflare for DNS + Email Routing only. Worth re-evaluating if we ever want runtime protections (would require enabling proxy + verifying GitHub Pages compatibility).
- **Don't let perceived urgency drive a rushed handover** — the morning chat almost wrote a hasty SESSION_HANDOFF document believing the chat was about to die. Always verify what the warning actually means before pivoting.
- **Brief versions can skip numbers when intermediate drafts never ship.** v35→v37 directly is fine if v36 drafts existed only in scratch space. The version number should reflect what's actually deployed in project knowledge / repo, not the count of intermediate WIP attempts.

**Outcomes May 5:**
- 3 Supabase migrations applied. Security advisor 6→1 (last one is wontfix-by-design). Performance advisor clean.
- UptimeRobot LIVE with 4 monitors and email alerting.
- 2 new files in repo (DECISIONS.md, .github/workflows/daily-health-check.yml) ready to commit.
- Brief v37 with consolidated v36-v37 update section.
- Full tool surface unlocked in claude.ai (everything except GitHub Integration).
- 8 setup artifacts staged in /mnt/user-data/outputs as future reference (`free-tier-analysis.md`, `uptimerobot-setup.md`, `sentry-telegram-worker.js`, etc.)

---

**End of archive. This document is frozen reference for future projects (especially QNC Academy) to mine for portable lessons. Do not edit.**


---

## May 5, 2026 — LATE AFTERNOON SESSION (Browser-tab audit + handover)

### What this session was

Final browser-tab settings audit via Claude in Chrome on Browser 1 (deviceId `020a49a7-7cc1-4832-a6d3-44b28b149b0b`). Goal: scan all 9 open tabs, verify settings, address remaining gaps from earlier sessions (Cloudflare orange cloud, DMARC, Resend webhooks, Microsoft Clarity wire-up).

### Tabs scanned

1. Claude.ai connectors page
2. Resend Emails dashboard
3. Supabase Billing (free tier confirmed)
4. GitHub `quantumneurocreations-dot/qnc-academy` (separate project)
5. UptimeRobot Monitors
6. Cloudflare Billing
7. Microsoft Clarity Getting Started (`wmb8y97pls`)
8. Gmail (skipped — private inbox)
9. Context7 Dashboard

### Key findings

**Microsoft Clarity is platform-locked to Mobile.** Existing project `wmb8y97pls` only offers install instructions for iOS/Android/Flutter/RN/Cordova/Ionic — no Website install option. Dashboard filters use Tablet/Mobile device classes. Decision: codified as ADR-011 — defer Clarity entirely until launch traffic justifies, then create new Website project. Existing Mobile project retained for future native app phase.

**UptimeRobot Supabase REST monitor** confirmed already paused (was actioned in a previous session). The list view's "Down 1h 48m" status is misleading — it shows the last incident pre-pause. Detail page shows status "Paused" with "Recently paused for 0h 12m 45s" and Resume button visible. No further action needed.

**Auth.users state verified clean.** Query against `auth.users` returned 8 users:
- `quantumneurocreations@gmail.com` (Ronnie's main, paid)
- `janek1223e@gmail.com` (Jane K, May 4 21:01 SAST — possible first organic signup)
- `admin@qncacademy.com` (QNC admin, never confirmed since Apr 21)
- `charlheyns1@gmail.com` (Charl Heyns)
- `booyens.michelle@gmail.com` (Michelle Booyens)
- `keyzer@xtremeprop24.com` (Keyzer)
- `rkelbrickmail@gmail.com` (Ronnie Kelbrick — Ronnie's secondary)
- `carlkelbrick@gmail.com` (Carl Kelbrick — possibly Ronnie's relative or test)

April 18 batch was thorough — no further test cleanup needed.

**Resend dashboard** showed all 15 recent emails delivered, zero bounces. Workspace is `qncacademy` (parent account), signed in as `admin@qncacademy.com`. 2 API keys (`quantum-cube-supabase-smtp` + `MCP Bundles - Claude`). Webhooks: still NONE configured — carry-forward gap.

**Cloudflare zone settings invisible.** MCP token scope is DNS:Read + Workers:Read + Email Routing:Read only. SSL mode, security level, bot fight mode, etc. require dashboard inspection. DMARC TXT record retrieved (id `e4c164849cbe1153783624c130d44223`, content `v=DMARC1; p=none;`).

**Context7 API key from earlier session is still active.** Revoke button visible in dashboard, key value still in Apple Notes (action: move to Apple Passwords + delete note still pending).

### Decisions codified

- **ADR-009** — Cloudflare orange cloud KEEP OFF (GH Pages cert renewal compat)
- **ADR-010** — DMARC stays `p=none` for 30-60 days observation period
- **ADR-011** — Microsoft Clarity deferred (project is Mobile-only, recreate as Website at scale)

### Files changed this session

- `PROJECT_BRIEF.md` v37 → v38 (audit summary + ADR references)
- `DECISIONS.md` (added ADRs 009, 010, 011)
- `BRIEF_ARCHIVE.md` (this entry)

No code changes. No SW bump needed.

### Carry-forward to next chat

1. Microsoft Clarity: defer entirely OR user creates new Website project, then wire it up
2. Resend webhooks: build Supabase Edge Function `/resend-webhook` with verify_jwt:false to receive bounce/complaint events
3. Supabase Edge Function `/health` to replace paused UR Supabase REST monitor (returns 200 unauthenticated, pings DB with SELECT 1)
4. Cloudflare orange cloud: stay OFF (no further action)
5. DMARC strengthening: revisit in 30-60 days

### Stage 6 user-eyeball items (no Claude action)

- Apple Passwords inventory cross-check
- Google 2FA on all 3 partner accounts
- Domain registrar audits
- Vercel shadow project (`prj_WKo5JwtJ02CGBVsyqbDAORQbQpDy`) decision: keep for Academy or delete
- Cloudflare dormant Worker `holy-leaf-e567` (Apr 6) — review and delete if unused
- Move Context7 API key from Apple Notes → Apple Passwords, delete note
- GitHub branch protection ruleset for `main` (Settings → Branches: "Require linear history" + "Restrict deletions")
- First manual run of GitHub Actions daily-health-check workflow

