# Map: Project Wildling

Label: wayfinder:map

## Destination

A complete game-design + technical spec for **Project Wildling**, an original 2D pixel-art Creature-collecting RPG for Android and iOS, released free as a hobby project. It must be detailed enough to hand to agents for slicing into implementation tickets, with no design decisions left open.

## Notes

- **Domain:** game design + mobile game engineering. Original IP only: no Pokémon names, creatures, sprites, music or look. Genre mechanics (catching, turn-based battles, types, evolution, parties) are fair game.
- **Scale:** target **Medium** (1 region, ~100 Creatures, 15–25h, ~8 boss challenges), but every system must be designed so the game can **grow to Large** (multiple regions, 150+ Creatures) without rewrites: content is data, not code.
- **Platforms:** Android and iOS. Offline single-player first.
- **Builder:** mostly Claude agents, with the human reviewing. Specs should break into small, independently testable modules.
- **Art budget:** $0 for now (CC0 packs, self-drawn, generated placeholders). Art must be swappable without code changes. Revisit budget later.
- **Vocabulary:** see `GLOSSARY.md` at the repo root. "Creature" and "Project Wildling" are placeholders until naming is decided.
- **Skills every session should consult:** `grilling` + `domain-modeling` for grilling tickets; `prototype` for prototype tickets; `research` for research tickets; `codebase-design` for architecture tickets.
- **Tracker:** local markdown (see `docs/agents/issue-tracker.md`). Tickets live in `issues/`; research findings live on local `research/<name>` branches (no remote yet).

## Decisions so far

<!-- one line per resolved ticket: [title](issues/NN-slug.md): gist -->

- [What do Google Play and the Apple App Store require for a free hobby game?](issues/04-store-requirements.md): Play $25 + 12-tester/14-day closed test; Apple $99/yr + Mac/Xcode; API 36, AAB, 16 KB pages; privacy policy required; no bundled analytics; watch Families-policy risk from cute art.

- [Which 2D engine fits an agent-built pixel-art game for Android + iOS?](issues/01-engine-choice.md): Godot 4.7.x stable with typed GDScript (Defold is the runner-up; Unity and libGDX rejected). CI must not trust Godot's headless exit code.

## Not yet specified

- **Story & world:** setting, tone, protagonist, rival(s), antagonist faction, how the story paces against progression. Hangs on the core loop & pillars.
- **Creature roster & evolution:** how many types, how Creatures are designed and named, evolution rules, rarity/distribution across routes. Hangs on battle and catching design.
- **Progression & bosses:** the ~8 boss challenges, level curve, gating of areas, postgame. Hangs on core loop and battle.
- **Items & economy:** currency, shops, healing, capture tools, held items. Hangs on battle and catching.
- **World structure & maps:** towns, routes, dungeons, tile-map authoring workflow, encounter zones. Hangs on art direction and engine.
- **Audio & music:** sourcing ($0 budget), style, SFX list.
- **Save, settings & accessibility:** beyond the architecture skeleton: text speed, battle animations toggle, colour-blind support, localisation.
- **Quality & release:** testing strategy for agent-built code, build pipeline for Android + iOS (Mac/Xcode, AAB, 16 KB pages), store listings (avoid child-directed look unless targeting Families), privacy-policy hosting, recruiting ≥12 Play closed testers early, trader-status declaration.

## Out of scope

- **Online features** (trading, PvP, leaderboards, accounts, servers): offline single-player first; save format should merely not preclude them.
- **Monetisation** (ads, IAP, paid release): hobby/free release.
- **Platforms beyond Android + iOS** (PC, web, consoles).
- **Use of Pokémon IP or ripped assets** in any form.
