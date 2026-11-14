# What are the game's title and the in-world name for Creatures?

Type: grilling
Status: resolved
Blocked by: none

## Question

Choose the real title (replacing "Project Wildling") and the in-world term for Creatures (and for the player role, e.g. "tamer"), checking that candidates don't collide with existing trademarks or store listings. Decide whether the repo folder should be renamed.

## Answer

Resolved by grilling with the human (2026-11-14). Terms are defined in `GLOSSARY.md` (Creature, Trainer, Lure, Sanctuary, Collection log, Mending). The name check is in [`research/name-clearance.md`](../../../research/name-clearance.md): a hobby-level check, not legal advice.

### Names
| Concept (glossary / code term) | In-world name |
|---|---|
| Game title | **Mendvale** |
| Creature | **Verdling** (plural Verdlings) |
| Trainer (anyone who raises Creatures, player and rivals alike) | **Mender** |
| Lure | **Offering** (variants such as "Honey Offering") |
| Sanctuary | **Haven** |
| Collection log | **Almanac** |
| Mending | **Mending** (no longer a placeholder) |

"Project Wildling" is retired: "Wildlings" is a *Game of Thrones* term. Lure (Pokémon GO), Sanctuary and Keeper (Monster Sanctuary), Tamer (Digimon) and Warden (Pokémon Legends: Arceus) were rejected as signature terms of other franchises.

**Not decided here:** the currency name belongs to ticket 14 (What items exist, and how does the economy work?), and the region's name to the Story & world fog.

### Codename and identifiers
- **Codename `mendvale`**, which is permanent: repo folder, Godot project name, and app ID **`io.github.andrew689cpu.mendvale`** on both stores. Android package names can't contain hyphens, so the ID drops the one in the GitHub handle. The ID never changes; the title is free to change.
- The **GitHub repo stays `rpg`**.
- **Code and data use generic identifiers** (`creature`, `trainer`, `lure`, `sanctuary`, `collection_log`, `mending`). In-world words appear only in localisation strings, so renaming anything later touches only strings. `GLOSSARY.md` keeps the generic term as each heading, with an "In-world name" line.

### Store listing
- App name on both stores: **"Mendvale"** (no keyword stuffing).
- App Store subtitle, and the start of the Play short description: **"A creature-collecting RPG"** (25/30 characters).
- The description body leads with "creatures who grow from how you raise them" and the turn-based RPG structure, not with "restore the region" alone. *Pokémon Pokopia* (2026) also restores a withered region habitat by habitat.

### Known risks, accepted
- **Mendvale** collides with no game, but a Shopify accessibility app (*Mendvale - Accessibility*, launched August 2026) uses the same name and owns mendvale.com. A legal clash is unlikely given the different market; search results are shared. No domain is needed.
- **Mending** is also a Minecraft enchantment: an ordinary English word, unrelated use.
- The check couldn't query the USPTO, EUIPO or WIPO registers directly (aggregator sites only).

### Before release (human checklist)
- Manually search USPTO (classes 9, 28 and 41), EUIPO, WIPO, both app stores and itch.io for exact matches of "Mendvale" and "Verdling", and recheck the Shopify app's trademark status. If either name fails, rename it: only strings and the listing change.

### Renames (human, after this ticket merges)
1. Rename the repo folder `pokemongame` to `mendvale`.
2. Rename the effort folder `.scratch/project-wildling` to `.scratch/mendvale`. Links inside the map and tickets are relative, so they survive.
3. Start a fresh Claude Code session from the new folder. Per-folder memory and history don't carry over.

**Follow-ups:** tickets 09 (technical architecture) and 14 (items and economy) were amended. The map's Notes and its Quality & release fog were updated.
