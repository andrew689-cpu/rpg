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
- **Tracker:** local markdown (see `docs/agents/issue-tracker.md`). Tickets live in `issues/`; research findings live on `research/<name>` branches, pushed to `origin` (github.com/andrew689-cpu/rpg) and never merged.

## Decisions so far

<!-- one line per resolved ticket: [title](issues/NN-slug.md): gist -->

- [What do Google Play and the Apple App Store require for a free hobby game?](issues/04-store-requirements.md): Play $25 + 12-tester/14-day closed test; Apple $99/yr + Mac/Xcode; API 36, AAB, 16 KB pages; privacy policy required; no bundled analytics; watch Families-policy risk from cute art.
- [Which 2D engine fits an agent-built pixel-art game for Android + iOS?](issues/01-engine-choice.md): Godot 4.7.x stable with typed GDScript (Defold is the runner-up; Unity and libGDX rejected). CI must not trust Godot's headless exit code.
- [Where can original or licensable pixel art come from, and at what cost?](issues/02-art-sources.md): use only CC0, OGA-BY or commercial licences (CC-BY conflicts with the App Store). Ninja Adventure (CC0, 16×16) for the world; placeholder Creatures from *50+ Monsters Pack 2D*; final Creatures self-drawn. Keep a licence ledger.
- [What stat, damage and type-chart systems do creature-collector games use?](issues/03-battle-mechanics-reference.md): a menu of genre mechanics with signature mechanics flagged to avoid. Mobile levers: visible randomness, 8–12 types, one energy bar, shown capture %, XP that helps lower levels catch up.
- [What is the core game loop, and what makes Project Wildling different?](issues/05-core-loop-and-pillars.md): for 13+ nostalgic players; Restoration hook (a broken region healed Area by Area, forward-only), backed by Habitat/time of day and visible Bond-shaped growth; 5 ranked pillars; 5–15 min sessions; string-of-pearls Boss order; light postgame.
- [How does a battle work?](issues/07-battle-system.md): 1v1, plus 2v2 in set encounters; 10 Types, no immunities, dual types capped 2×/0.5×; 7 stats (Power/Guard vs Focus/Will); Traits set by where and when caught; one Energy bar + free Basic move; ratio damage with a preview, no random crits; 6 Statuses with countdowns; 3 AI tiers; whole-party XP scaled by level gap; Pokémon-style money loss on defeat, capped at 50%.
- [How do catching, the party, and storage work?](issues/08-catching-and-party.md): visible wild Creatures with per-species behaviour; weighted spawn tables per Area × Restoration stage (Common/Uncommon/Rare/Very rare); Lure offering with a shown 1–95% chance and no fleeing on failure; random starter trio picked by a per-save seed, every starter also wild; Party of 6 with the lead following; unlimited Sanctuary (menu in v1); Collection log doubles as a hunting guide.
- [What should Project Wildling's pixel art look like?](issues/10-art-direction.md): 180 pixels wide internally with integer scaling; 16×16 tiles, player character and Creature map sprites; 64×64 front and back battle sprites animated by code; locked 53-colour palette; Public Pixel and Tiny5 fonts; Restoration shown as tile swaps spreading out from a focal point, muted rather than burnt.
- [How does the game feel on a touchscreen?](issues/11-controls-and-orientation.md): portrait first; floating pad plus tap-to-move; map above a control deck; battle info strip, Area-drawn scene and a thumb-arc command deck; tap to preview, tap again to confirm; 2v2 targeting by tapping a foe sprite; left-handed mirroring; gamepad and keyboard through five input actions.

## Not yet specified

- **Story & world:** setting, tone, protagonist, rival(s), antagonist faction, how the story paces against progression. Premise is now fixed as a broken region the player restores; tone is cozy-to-adventurous for 13+. Needs a framing for the randomly picked starter trio.
- **Creature roster & evolution:** how many types, how Creatures are designed and named, rarity/distribution across Areas. Every Creature needs a Habitat and Time of day; many need two Bond-selected evolution branches. Each species also needs base stats, moves, 2–3 Traits, a behaviour (wander/curious/shy), a Rarity tier, and a 16×16 map sprite; 4–5 starter trios form type triangles. Hangs on Bond design.
- **Creature art production:** no free source covers ~100 Creatures in one style. Who draws them, in what order, and how placeholders get replaced (commissioning would cost about $6k–$12k). Each species needs 64×64 front and back battle sprites (still frames) plus a 16×16 map sheet (4 directions × 2 frames), all within the locked 53-colour palette. Hangs on the roster.
- **Progression & bosses:** the ~8 Bosses, level curve, gating of Areas, postgame rematches. Shape is fixed as a string of pearls (choose 2–3 Bosses at a time, no level scaling), and each Boss drives a big Restoration stage. Hangs on battle and Restoration.
- **World structure & maps:** towns, routes, dungeons, tile-map authoring workflow, Habitat patches, Restoration tile-swap layers (each with a focal point). 16×16 tiles, about 11 × 12 tiles visible in portrait. Hangs on Restoration.
- **Audio & music:** sourcing ($0 budget), style, SFX list.
- **Save, settings & accessibility:** beyond the architecture skeleton. Settings so far: movement scheme (floating or fixed pad), left-handed mirroring, run toggle, follower toggle, battle text auto-advance, one-tap moves, simple-list battle commands, battle animations off. Still open: colour-blind support (type colours need icons or labels too), a large-text mode, localisation (Public Pixel covers 98 languages).
- **Quality & release:** testing strategy for agent-built code, build pipeline for Android + iOS (Mac/Xcode, AAB, 16 KB pages), licence ledger for every asset (including the Public Pixel and Tiny5 fonts), store listings (avoid child-directed look unless targeting Families), privacy-policy hosting, recruiting ≥12 Play closed testers early, trader-status declaration.

## Out of scope

- **Online features** (trading, PvP, leaderboards, accounts, servers): offline single-player first; save format should merely not preclude them.
- **Monetisation** (ads, IAP, paid release): hobby/free release.
- **Platforms beyond Android + iOS** (PC, web, consoles).
- **Use of Pokémon IP or ripped assets** in any form.
