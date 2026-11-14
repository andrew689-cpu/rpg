# Map: Mendvale

Label: wayfinder:map

## Destination

A complete game-design + technical spec for **Mendvale**, an original 2D pixel-art Creature-collecting RPG for Android and iOS, released free as a hobby project. It must be detailed enough to hand to agents for slicing into implementation tickets, with no design decisions left open.

## Notes

- **Domain:** game design + mobile game engineering. Original IP only: no Pokémon names, creatures, sprites, music or look. Genre mechanics (catching, turn-based battles, types, evolution, parties) are fair game.
- **Scale:** target **Medium** (1 region, ~100 Creatures, 15–25h, ~8 boss challenges), but every system must be designed so the game can **grow to Large** (multiple regions, 150+ Creatures) without rewrites: content is data, not code.
- **Platforms:** Android and iOS. Offline single-player first.
- **Builder:** mostly Claude agents, with the human reviewing. Specs should break into small, independently testable modules.
- **Art budget:** $0 for now (CC0 packs, self-drawn, generated placeholders). Art must be swappable without code changes. Revisit budget later.
- **Vocabulary:** see `GLOSSARY.md` at the repo root. Specs and code use the generic glossary terms (Creature, Trainer, Lure, Sanctuary, Collection log); the in-world names (Verdling, Mender, Offering, Haven, Almanac) are display strings only.
- **Names:** the title and codename are both **Mendvale** (`io.github.andrew689cpu.mendvale`). The GitHub repo stays `rpg`. The effort lives in `.scratch/mendvale/`; the local repo folder `pokemongame` is due to be renamed to `mendvale` (see [What are the game's title and the in-world name for Creatures?](issues/06-naming-and-branding.md)).
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
- [How does Restoration change an Area?](issues/12-restoration.md): Areas start Blighted with 3 stages; stage 1 only from story flags (one may restore several Areas), stages 2+ from K-of-M Mendings (native species caught in the Area, trainers, one Area challenge, hidden sites) that count early; stages change spawns, tiles, patches, NPCs, optional paths, shops, weather, music, never battle rules; focal point shows progress, Region map lists the next stage; save keeps facts plus highest stage, never regresses.
- [How does Bond shape a Creature?](issues/13-bond.md): Bond = a Bond rank (0–5, earned by acting in battles, unlocks 2–4 Bond moves per form) + Leaning needles on four axes (Style, Type, Habitat, Time) the player can steer; evolution at a species level, postponable, the needle picks one of two branches, shown as silhouettes until discovered; no stat effects, no Trait swaps, no Bond items; at most one branch per line in v1.
- [What are the game's title and the in-world name for Creatures?](issues/06-naming-and-branding.md): the title and codename are **Mendvale** (app ID `io.github.andrew689cpu.mendvale`). Creatures are **Verdlings**, players **Menders**; Offering, Haven, Almanac and Mending replace the placeholders. Code keeps generic identifiers; names live only in strings. The store subtitle is "A creature-collecting RPG". The currency and region names are left to other tickets.

## Not yet specified

- **Story & world:** setting, tone, protagonist, rival(s), antagonist faction, how the story paces against progression. Premise is now fixed as a broken region the player restores; tone is cozy-to-adventurous for 13+. Needs a framing for the randomly picked starter trio.
- **Creature roster & evolution:** the roster's *structure* is now [How is the Creature roster structured?](issues/16-roster-structure.md). Still fog: the per-species design work itself (each species' stats, movesets, Traits, Bond moves and evolution data), which hangs on that ticket, and spreading species across Areas, which hangs on the World structure.
- **Creature art production:** no free source covers ~100 Creatures in one style. Who draws them, in what order, and how placeholders get replaced (commissioning would cost about $6k–$12k). Each species needs 64×64 front and back battle sprites (still frames) plus a 16×16 map sheet (4 directions × 2 frames), all within the locked 53-colour palette. Each branching line adds one extra form, and branch forms show as silhouettes until discovered. Hangs on [How is the Creature roster structured?](issues/16-roster-structure.md).
- **World structure & maps:** towns, routes, dungeons, tile-map authoring workflow, Habitat patches. 16×16 tiles, about 11 × 12 tiles visible in portrait. From Restoration: each restorable Area needs a focal point, a tile-swap layer per stage spreading from it, 3–6 native species, its trainers, at most one Area challenge, hidden sites, and optional paths that only stages 2+ open; Rest points must be reachable in Blighted Areas too. Hangs on the Bosses and gating ticket.
- **Audio & music:** sourcing ($0 budget), style, SFX list.
- **Save, settings & accessibility:** beyond the architecture skeleton. Settings so far: movement scheme (floating or fixed pad), left-handed mirroring, run toggle, follower toggle, battle text auto-advance, one-tap moves, simple-list battle commands, battle animations off. Still open: colour-blind support (type colours need icons or labels too), a large-text mode, localisation (Public Pixel covers 98 languages).
- **Quality & release:** testing strategy for agent-built code, build pipeline for Android + iOS (Mac/Xcode, AAB, 16 KB pages), licence ledger for every asset (including the Public Pixel and Tiny5 fonts), store listings (avoid child-directed look unless targeting Families), privacy-policy hosting, recruiting ≥12 Play closed testers early, trader-status declaration. From naming: a manual USPTO, EUIPO, WIPO and store search for "Mendvale" and "Verdling" before release; the listing leads with "raised, not rolled" to stand apart from *Pokémon Pokopia*'s restore-the-habitat pitch.

## Out of scope

- **Online features** (trading, PvP, leaderboards, accounts, servers): offline single-player first; save format should merely not preclude them.
- **Monetisation** (ads, IAP, paid release): hobby/free release.
- **Platforms beyond Android + iOS** (PC, web, consoles).
- **Use of Pokémon IP or ripped assets** in any form.
