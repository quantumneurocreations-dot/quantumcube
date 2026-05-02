# QUANTUM CUBE — MARKETING PLAYBOOK
**Version: v1 | Last Updated: May 2, 2026 (Saturday, evening — launch day)**

---

## 🎯 PURPOSE

This playbook lives separate from PROJECT_BRIEF.md to keep build context and marketing context cleanly separated. The brief is for code, infra, architecture. This is for distribution, growth, and getting the cube in front of real customers.

**For new chats:** attach this playbook + CHAT_KICKOFF.md when working on marketing/growth tasks. Attach PROJECT_BRIEF.md + CHAT_KICKOFF.md when working on build/code tasks.

---

## 🔮 BRAND FUNDAMENTALS

### Product
Quantum Cube — a $17 one-time digital reading app combining personalized numerology, Western astrology, and Chinese zodiac into a single curated experience with AI-narrated voice. Web (PWA) at quantumcube.app, Android via Google Play, iOS deferred.

### Tagline
**"Your cosmic profile, simplified."**

Distills the curation differentiator (one beautiful, easy reading vs. the overwhelm of generic horoscope apps).

### Positioning
- **Premium, ornate, mystical** — not the scrappy free-horoscope-app aesthetic
- **Curated, simplified** — not "drown the user in raw chart data"
- **Entertainment & self-reflection** — never positioned as predictive science
- **One-time payment, lifetime access** — not subscription fatigue

### Visual identity
- Cinzel Decorative serif typography
- Cosmic dark backgrounds (#05050f, #071b2e)
- Cyan accent glow (#7dd4fc)
- White-as-base + ONE cyan accent word/letter (CUBE, the C in QC)

### Voice (when writing copy)
- Premium but warm, not aloof
- Mystical but grounded, not woo-woo or scammy
- Confident in the curation, humble about the "entertainment only" disclaimer
- Avoid the indie-hacker-bro voice ("just shipped...", "tired of...", "I built...")
- Avoid generic spiritual platitudes ("manifest your truth", "align your energy")

### Customer profile
- Primary: 22-50, mostly female-skewing, interested in astrology / numerology / self-discovery
- Secondary: gift-givers (cosmic-themed gift for partner, sister, friend)
- Geographic: global from launch (Adaptive Currency on Dodo enables this)
- Discovers via: TikTok scrolling, Instagram Reels, friend recommendation, search ("numerology reading", "astrology app")
- NOT: enterprise B2B buyers, dev-tool comparison shoppers, AppSumo deal hunters

---

## 📊 CHANNEL STRATEGY — RANKED

For a B2C visual/lifestyle product in the spirituality/self-discovery niche, the channel hierarchy is:

### Tier 1 — Highest leverage, must-do
1. **TikTok organic** — single biggest opportunity. WitchTok / AstroTok / NumerologyTok are massive engaged niches. The cube rotation + reading reveal is native short-video content. Free organic reach.
2. **Instagram Reels** — same content as TikTok, repurposed. Cosmic aesthetic = pure Instagram feed material.
3. **Google Play Store organic (ASO)** — once live, the store itself sends qualified buyers. App Store Optimization compounds forever.
4. **Pinterest** — underrated for spiritual content. Visuals + searchable + sustained slow traffic. Cosmic-aesthetic graphics are pure Pinterest material.

### Tier 2 — One-shot launches, high-value spikes
5. **Product Hunt** — single launch event, ~1000-5000 visits, ~20-200 first-day sales. Plan for ~2-3 weeks AFTER Play Store goes live so funnel is complete.
6. **Indie Hackers** — community-friendly, post launch journey + revenue updates. Low effort, supportive audience.
7. **Hacker News (Show HN)** — technical-angle only ("I built a $17 PWA with AI-narrated content using ElevenLabs + Supabase"). Audience hostile to spiritual framing — never lead with that.

### Tier 3 — Slow-burn organic
8. **Reddit** — r/numerology, r/astrology, r/Chinese_Astrology, r/spirituality. PARTICIPATE first, post your "I built this" story only after you've earned credibility. Never automate Reddit posting — accounts get banned.
9. **YouTube long-form** — your existing channel. "What your Life Path number means" type videos that subtly demonstrate the app. Compounds over years.

### Tier 4 — Influencer + paid (later)
10. **Influencer affiliates** — partner with astrology/numerology Instagram or YouTube creators. Affiliate model: $5/sale to creator, $12 net to you. Even 10k-50k follower creators move real units.
11. **Meta Ads (Facebook + Instagram)** — only AFTER organic validates funnel. ~3 months post-launch, $10-20/day test budgets. Connect Meta Ads MCP to Claude when ready (`mcp.facebook.com/ads`).
12. **Google Ads** — same timing as Meta. Search ads on "numerology reading", "astrology app" keywords.

### Channels REJECTED for Quantum Cube

- **AppSumo** — built for SaaS lifetime deals (80-95% off). Wrong audience (B2B founders), wrong economics ($3-5 sales destroy unit economics on $17 product).
- **G2 / Capterra** — B2B software review platforms. Salesforce, HubSpot, Notion. Wrong audience entirely.
- **Vloxo** — AI launch automation tool. Built for B2B indie-dev / SaaS founder bubble (Twitter/X, LinkedIn, Reddit, PH, IH, HN). Channel mix wrong for B2C spiritual product. Voice wrong for our brand. Reddit auto-posting risky.

---

## 📅 LAUNCH SEQUENCING

### Phase 1 — Pre-Play-Store (now → ~2 weeks)
- Web (quantumcube.app) is LIVE since Apr 24, accepting payments since May 2
- Brand identity locked
- All 6 social handles claimed (`@quantumcubeapp`)
- NO posts yet across any platform — claim-and-hold mode
- Cover photos for Facebook + Twitter still to do (820×312 + 1500×500 in Canva)

### Phase 2 — Play Store submission (~2-3 weeks)
- Google Play Developer account ($25)
- Implement Play Billing in Capacitor wrap (~3-4 hours dev work)
- Build `play-billing-webhook` Edge Function in Supabase
- Generate .aab via PWABuilder/Bubblewrap
- Store listing: feature graphic (1024×500), phone screenshots, description, content rating, Data Safety form
- Internal Testing track first (1-2 weeks with rkelbrick + carl + michelle as testers)
- Submit to Production (review takes 7-14 days)
- See PROJECT_BRIEF.md Phase 5 section for technical detail

### Phase 3 — Soft launch (Play Store live → +1 week)
- Verify Play Store listing live and discoverable
- First real users from organic Play Store search
- Monitor: crashes, payment edge cases, user reviews
- Address any urgent fixes before pushing harder

### Phase 4 — Social launch (Play Store +1 to +4 weeks)
- Cover photos shipped on FB + Twitter
- TikTok: start posting 3x/week (cube rotation, reading reveals, narration plays)
- Instagram Reels: same content repurposed
- Pinterest: start pinning cosmic-aesthetic graphics
- YouTube: first video on the channel ("What is Quantum Cube?")
- Reddit: BEGIN PARTICIPATING (don't post the app yet)

### Phase 5 — Product Hunt + Indie Hackers (Play Store +2 to +3 weeks)
- Launch on Product Hunt mid-week (Tuesday/Wednesday/Thursday US time)
- Cross-post to Indie Hackers same day
- Coordinate Twitter/X push for PH votes
- Have website + Play Store listing rock-solid that day (traffic spike incoming)

### Phase 6 — Slow-burn organic growth (months 1-3)
- TikTok consistency 3-5x/week
- Instagram Reels 3-5x/week
- Pinterest weekly batch pinning
- Reddit posts after credibility built (~2 months in)
- Hacker News Show HN with technical angle
- YouTube monthly long-form
- Track: organic Play Store rankings, conversion rate per channel, top-performing content

### Phase 7 — Paid ads + influencer affiliates (months 3-6)
- Connect Meta Ads MCP to Claude (`mcp.facebook.com/ads`)
- Test Meta ads at $10-20/day (Reels-format video ads)
- Test Google Ads on intent keywords
- Reach out to 5-10 astrology/numerology Instagram or YouTube creators for affiliate partnerships
- Scale only what works

---

## 🎬 CHANNEL PLAYBOOKS

### TikTok organic
- **Account:** `@quantumcubeapp` (claimed Apr 30 PM)
- **Posting cadence:** 3-5x/week
- **Content formats that work:**
  - Cube rotation + reading reveal (15-30 sec)
  - "POV: you finally found out what your numerology means"
  - "Reading the [zodiac sign]'s combined cosmic profile"
  - Trending audio + voiceover pointing at app
  - User-generated reaction content (when reviews start coming in)
- **Hashtags:** mix of niche (#numerology #astrology #chinesezodiac) + broad (#fyp #foryou) + brand (#quantumcube)
- **DO:** native vertical filming, trending audio, hook in first 2 sec, end with subtle "link in bio"
- **DON'T:** polished long-form ads, pure product walkthroughs without entertainment value, paid-feeling content

### Instagram Reels
- **Account:** `@quantumcubeapp`
- **Same content as TikTok, repurposed with platform-native hashtags**
- **Cross-post Reels → Threads automatically (handles linked)**
- **Use Stories for behind-the-scenes / build journey content**

### Pinterest
- **Account:** `@quantumcubeapp`
- **Content types:**
  - Cosmic-aesthetic quote graphics ("Your Life Path is your soul's blueprint")
  - Numerology "cheat sheet" infographics
  - Zodiac compatibility charts
  - Cube screenshots with cosmic backgrounds
- **Cadence:** weekly batch pin sessions (10-20 pins at a time, scheduled out)
- **Drives:** sustained 6-12 month traffic per pin (Pinterest is evergreen)

### Product Hunt (one-shot)
- **Timing:** ~2-3 weeks after Play Store goes live (so funnel is complete: PH → website → Play Store)
- **Day:** Tuesday, Wednesday, or Thursday US time. Avoid Mondays + Fridays.
- **Pre-launch:** build a small group of supporters (friends, ex-colleagues, IH community) who'll vote in first 2 hours
- **Post copy:** short, visual-first, lead with the cube, the tagline, the $17 price, the lifetime-access angle
- **Tagline for PH:** "Your cosmic profile, simplified — numerology, astrology & Chinese zodiac in one $17 reading"
- **Maker comment:** longer, share build story, mention bounce-bug debug as engineering anecdote
- **Coordinate:** Twitter/X push, Indie Hackers crosspost, email any existing list

### Indie Hackers
- **Account:** create when posting (or use existing if Ronnie has one)
- **First post:** "After 8 days of waiting for Dodo Payments approval, Quantum Cube is live — here's what shipping a $17 PWA actually looks like"
- **Tone:** transparent, story-driven, share commits + revenue + lessons
- **Ongoing:** monthly revenue updates, build journey continuation, lessons from organic growth

### Hacker News (Show HN)
- **Timing:** ~1 month post-launch, after Product Hunt
- **Title:** "Show HN: I built a $17 PWA with AI-narrated personalized content (Supabase + ElevenLabs + Dodo)"
- **Lead with:** technical architecture, the bounce-bug debug saga, the overlay SDK migration, the offline narration cache strategy
- **Don't lead with:** "your cosmic profile" or anything spiritual-sounding (HN is hostile)
- **Be ready for:** harsh comments about astrology being pseudoscience. Take feedback gracefully, don't argue, learn what you can.

### Reddit
- **Subs:** r/numerology (~100k), r/astrology (~700k), r/Chinese_Astrology (smaller), r/spirituality, r/witchcraft, r/IndieDev (when posting build story)
- **Phase 1 (months 1-2):** PARTICIPATE only. Comment helpfully on others' posts. Build karma + recognition. Do NOT promote Quantum Cube.
- **Phase 2 (months 2+):** post once per sub max, "I built an app that..." format, transparent that you're the maker, focus on the journey not the sale.
- **CRITICAL:** never use AI tools to automate Reddit. Accounts get banned fast. Manual only.

### YouTube long-form
- **Channel:** Quantum Cube (existing, renamed Apr 30 PM from "Quantum Neuro Creations Academy")
- **Content angles:**
  - "What your Life Path Number means" (numerology educational)
  - "Western vs Chinese astrology — which is more accurate?" (comparison)
  - "I built an astrology app — here's what 1000 readings taught me" (story-based, post-traction)
- **Cadence:** monthly is fine. Quality > volume.
- **Cross-promote:** in Cube app's Face 7, on website, in TikTok bios

### Influencer affiliates
- **Target:** 10k-100k follower astrology/numerology Instagram + TikTok + YouTube creators
- **Pitch:** $5 per sale to creator, custom discount code for tracking
- **Math at $17 sale:** creator gets $5, Dodo takes ~$1 fee, you net ~$11 vs ~$16 organic. Worth it for the reach.
- **Tools:** start manual (DM creators), explore affiliate platforms (Impact, Refersion) when scaling
- **Outreach template:** keep it personal, mention specific videos of theirs you liked, offer free reading code as a no-pressure intro

### Meta Ads (Phase 7+)
- **Connector:** Meta Ads AI Connector via MCP at `mcp.facebook.com/ads` (launched Apr 29, 2026 — open beta)
- **Setup:** paste URL as custom connector in Claude, OAuth with Meta Business
- **Capabilities:** create campaigns, edit budgets, analyze performance, run signal diagnostics, all via natural language
- **Includes:** Instagram Ads automatically (Meta Marketing API treats FB+IG as one)
- **Safety rules:**
  - Keep human in loop — review every Claude-proposed campaign before approving
  - Never let Claude make autonomous budget changes
  - Use chat-based MCP, not Claude Code's CLI (lower ban risk)
  - Run from verified Business Manager account
  - Avoid burst API traffic / rapid budget changes
- **Starting budget:** $10-20/day on Reels-format video ads (cube rotation + reading reveal)
- **Test timeline:** 2-week test cycle minimum before scaling. Kill what doesn't work, scale what does.

### Google Ads (Phase 7+)
- **Connector:** Google Ads MCP (open-source, released Oct 7, 2025)
- **Keywords to test:** "numerology reading", "astrology app", "personalized horoscope", "Chinese zodiac reading"
- **Budget:** $10-20/day to start, parallel with Meta tests
- **Landing page:** quantumcube.app/ (existing landing page) — may build dedicated landing pages per ad group later

---

## 🛠 TOOLS EVALUATED

### ✅ Recommended
- **Canva Pro** — already subscribed. For Pinterest pins, Instagram graphics, FB cover photos, ad creative.
- **Native phone camera** — for TikTok/Reels filming. Don't overthink production.
- **Buffer free tier** or **Twitter/X native scheduler** — for Twitter post scheduling. No paid tool needed.
- **Later (paid)** — if scheduling Instagram + TikTok at scale becomes painful.
- **Meta Ads MCP** (Phase 7) — official, free.
- **Google Ads MCP** (Phase 7) — open-source, free.
- **Apple Passwords / 1Password** — for ad account credentials, never paste in chat.

### ❌ Rejected
- **Vloxo** — wrong audience focus (B2B indie-dev), missing key channels (TikTok, Instagram Reels, Pinterest), AI-generated voice clashes with brand, Reddit auto-posting risky, platform itself very early-stage.
- **AppSumo** — built for SaaS lifetime deals. Wrong audience, destroys $17 unit economics.
- **G2 / Capterra** — B2B software review platforms. Wrong audience.

### 🔬 Bookmarked for later evaluation
- **Sensor Tower / AppFollow / Appfigures** — for ASO tracking once Play Store is live.
- **Refersion / Impact** — affiliate platforms when influencer program scales beyond manual.

---

## 📐 METRICS TO TRACK

### Per-channel
- **Sales attributed** (use UTM codes on website links + custom Dodo metadata)
- **Organic reach** (TikTok views, Instagram impressions, Pinterest impressions)
- **Click-through to Play Store / website**
- **Install-to-purchase conversion**
- **Cost per acquisition** (paid channels only)

### Aggregate
- **Daily active users** (Play Store dashboard + Supabase profile counts)
- **Total paid users** (Supabase profiles where has_paid=true)
- **Revenue per channel**
- **Average revenue per user** (likely just $17 since one-time, but post-launch analytics useful)
- **Lifetime value vs CAC ratio** (target 3:1+)

### Top-performing content
- **Best-performing TikToks** (replicate the format)
- **Best-performing Pinterest pins** (re-pin variations)
- **Best-converting paid ads** (kill underperformers within 7-14 days)

---

## 🧠 LESSONS LEARNED

(Will grow as launch progresses. Add learnings as we ship.)

### Pre-launch lessons (May 2, 2026)
- **Channel mix matters more than channel count.** A bad-fit channel (Vloxo for B2B SaaS bubble) is worse than no channel — wastes time + money.
- **Brand voice consistency > content volume.** Better to post 3 well-crafted TikToks than 10 AI-generated ones that feel off-brand.
- **Tools optimised for the wrong audience are still wrong tools.** Vloxo is well-built for indie-dev SaaS marketing — and wrong for Quantum Cube specifically.
- **The voice IS the product for premium B2C.** AI-generated launch posts feel hollow when the brand is "ornate, mystical, premium." Hand-craft these.
- **Discovery > margin in early days.** Eating 15% Play Billing fee for Play Store presence beats keeping 94% margin on web-only obscurity.
- **Sequence by funnel completeness.** Don't launch on Product Hunt while still web-only. Wait until Play Store is live so the funnel is whole.

---

## 🔗 RELATED DOCS

- **PROJECT_BRIEF.md** — build, infra, architecture, technical history. Update as code ships.
- **CHAT_KICKOFF.md** — how Chat Claude + Cursor Claude collaborate. Update as workflow evolves.
- **MARKETING_PLAYBOOK.md** (this doc) — distribution, growth, channel strategy. Update as launch progresses.

---

**End of marketing playbook v1.**
