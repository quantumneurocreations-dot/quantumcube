# Graph Report - .  (2026-05-12)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 175 nodes · 249 edges · 14 communities (13 shown, 1 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `036bc881`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]

## God Nodes (most connected - your core abstractions)
1. `Architecture Decision Records` - 17 edges
2. `Quantum Cube Product` - 15 edges
3. `Session Log` - 14 edges
4. `Chat Kickoff Protocol` - 12 edges
5. `Play Store Prep Checklist` - 11 edges
6. `Connectors & Service Registry` - 11 edges
7. `check_run_calc()` - 10 edges
8. `Project Brief` - 9 edges
9. `CLAUDE.md Context Pointer` - 9 edges
10. `Dodo Payments` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Play Store Screenshot: 10-inch Tablet Intro` --conceptually_related_to--> `Quantum Cube Product`  [INFERRED]
  Playstore Screenshots/10 Inch Tablet Screenshots/Tablet - Intro page.jpg → MARKETING_PLAYBOOK.md
- `Background Image: pexels-haseeb-syed` --conceptually_related_to--> `Quantum Cube Product`  [INFERRED]
  More backgrounds/pexels-haseeb-syed-2150151139-35198179.jpg → MARKETING_PLAYBOOK.md
- `Background Image: pexels-kate-holovacheva` --conceptually_related_to--> `Quantum Cube Product`  [INFERRED]
  More backgrounds/pexels-kate-holovacheva-1824230-5726190.jpg → MARKETING_PLAYBOOK.md
- `Background Image: olena-bohovyk-unsplash` --conceptually_related_to--> `Quantum Cube Product`  [INFERRED]
  More backgrounds/olena-bohovyk-Cq5NaI0yKBE-unsplash.jpg → MARKETING_PLAYBOOK.md
- `Play Store Screenshot: 10-inch Tablet Intro` --conceptually_related_to--> `Google Play Store`  [EXTRACTED]
  Playstore Screenshots/10 Inch Tablet Screenshots/Tablet - Intro page.jpg → PLAY_STORE_PREP.md

## Communities (14 total, 1 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (24): CONFIG, dodoClient, sendWelcomeEmail(), webhookHeaders, welcomeHtml(), welcomeText(), exportPayload, _hourEnd (+16 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (19): ASTRO_SLOTS, CAT_LABELS, clean, counts, data, extractAstroObject(), extractBalancedLiteral(), manifest (+11 more)

### Community 2 - "Community 2"
Cohesion: 0.14
Nodes (27): ADR-001: Dodo Payments as MoR, ADR-003: Single-HTML-file Architecture, ADR-004: RLS Column-Level Guard on has_paid, Android TWA (Trusted Web Activity), app.html (PWA Core), assetlinks.json (TWA Verification), Connectors & Service Registry, delete-account Edge Function (+19 more)

### Community 3 - "Community 3"
Cohesion: 0.17
Nodes (16): ADR-002: GitHub Pages Hosting, ADR-005: Magic-link + Google OAuth, ADR-006: Sentry EU Free Tier, ADR-008: Email-Only Alerting, ADR-009: Cloudflare Orange Cloud OFF, ADR-010: DMARC p=none Observation Period, ADR-011: Microsoft Clarity Deferred, ADR-012: DMARC Ramped to p=quarantine (+8 more)

### Community 4 - "Community 4"
Cohesion: 0.13
Nodes (15): Background Image: olena-bohovyk-unsplash, Background Image: pexels-haseeb-syed, Background Image: pexels-kate-holovacheva, Proprietary License, 500 Paying Customers by Aug 15 2026, Quantum Compatibility, Quantum Cube Product, Quantum Family (+7 more)

### Community 5 - "Community 5"
Cohesion: 0.31
Nodes (14): ADR-007: Brief/Archive/Kickoff Three-Doc Structure, Brief Archive, Chat Kickoff Protocol, CLAUDE.md Context Pointer, Instagram Channel (@quantumcubeapp), Marketing Playbook, mcp-obsidian MCP Tool, Michelle (Social Media Owner from May 4) (+6 more)

### Community 7 - "Community 7"
Cohesion: 0.2
Nodes (9): { ConsoleLog }, generator, KEYSTORE_PATH, log, require, TWA_MANIFEST_PATH, { TwaGenerator }, { TwaManifest } (+1 more)

### Community 8 - "Community 8"
Cohesion: 0.36
Nodes (6): die(), load_manifest(), main(), Apply per-filename script tweaks before TTS., transform(), tts()

### Community 9 - "Community 9"
Cohesion: 0.29
Nodes (3): Application, DelegationService, LauncherActivity

### Community 10 - "Community 10"
Cohesion: 0.5
Nodes (3): batch, u, urls

## Knowledge Gaps
- **61 isolated node(s):** `urls`, `batch`, `u`, `CORS`, `ip` (+56 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Quantum Cube Product` connect `Community 4` to `Community 2`, `Community 3`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `Architecture Decision Records` connect `Community 3` to `Community 2`, `Community 5`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `Dodo Payments` connect `Community 2` to `Community 4`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `Quantum Cube Product` (e.g. with `Play Store Screenshot: 10-inch Tablet Intro` and `Background Image: pexels-haseeb-syed`) actually correct?**
  _`Quantum Cube Product` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `urls`, `batch`, `u` to the rest of the system?**
  _61 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._