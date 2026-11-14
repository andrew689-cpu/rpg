# Mendvale: game-design and technical spec

Status: **draft, partly open.** Assembled on 2026-11-14 from the 23 resolved tickets of the [Mendvale map](map.md), with every amendment applied. Areas still in the map's **Not yet specified** are marked **Open** here and listed in [§7](#7-still-open). Update this file as they close.

**What this is.** The current truth for Mendvale, an original 2D pixel-art Creature-collecting RPG for Android and iOS, released free as a hobby project. It is the hand-off for slicing into implementation tickets. Each subsection links the ticket it comes from. The ticket holds the reasoning and the alternatives; this file holds only the decision as it stands.

**How to read it.**
- Terms follow [`GLOSSARY.md`](../../GLOSSARY.md). Code and data use the generic terms (Creature, Trainer, Lure, Sanctuary, Collection log). The in-world names (Verdling, Mender, Offering, Haven, Almanac) are display strings only.
- Decisions that are hard to reverse are ADRs in [`docs/adr/`](../../docs/adr/).
- **Every count, level, price and rate is data with a starting value**, tuned in playtesting, unless it's stated as a closed list in code.
- **Scale:** built for **Medium** (1 region, 100 species, 15–25 h, 8 Bosses), and designed to grow to **Large** (several regions, 150+ species) with no rewrites, because content is data, not code.

## Contents
1. [Game, story and naming](#1-game-story-and-naming)
2. [Battle and moves](#2-battle-and-moves)
3. [Creatures: catching, party, Bond and roster](#3-creatures-catching-party-bond-and-roster)
4. [World: Restoration, region, Bosses and economy](#4-world-restoration-region-bosses-and-economy)
5. [Look and feel: art, controls and screens](#5-look-and-feel-art-controls-and-screens)
6. [Technology and release](#6-technology-and-release)
7. [Still open](#7-still-open)
8. [Out of scope](#8-out-of-scope)

## 1. Game, story and naming

### Audience and pillars
*Source: [What is the core game loop, and what makes Project Wildling different?](issues/05-core-loop-and-pillars.md)*

- **Player:** teens and adults who grew up on handheld Creature collectors. 13+ in spirit, deliberately **not child-directed** (avoids the Families-policy risk; see §6).
- **Pitch:** *"Heal a broken region with Creatures who grow from how you raise them."*
- **Nothing is monetised.**

**Pillars, ranked.** When two conflict, the higher one wins.

| Rank | Pillar | Meaning |
|---|---|---|
| 1 | **A World That Heals** | Progress is visible in the world itself, not just in menus. |
| 2 | **Raised, Not Rolled** | Your Creatures become what you made them; growth is visible and earned, not random. |
| 3 | **Belongs Somewhere** | Every Creature has a Habitat, a Time of day and a reason to be where it is. |
| 4 | **Respect the Player's Time** | Short sessions, suspend anywhere, no grinding, nothing permanently missable. |
| 5 | **Depth on Demand** | Easy to pick up, rewarding to master; randomness is always visible. |

### The hook
*Source: [What is the core game loop, and what makes Project Wildling different?](issues/05-core-loop-and-pillars.md)*

**Restoration** leads; **Habitat** and **Bond** support it.

- **Restoration:** each Area starts Blighted and has a few Restoration stages. The first stage always comes from the critical path (a story or Boss flag), so nobody is soft-locked; later stages come from optional local Mendings (registering the Area's native Creatures in the Collection log, beating its trainers and Area challenge, finding Hidden sites). Each stage is data that changes the Area's spawns, tiles, NPCs and optional paths. Restoration **only moves forward**: no decay, no punishment for being away. The story may *show* an Area under threat as a scripted beat, but saved progress never drops. Stage counts, Mending rules and what a stage changes: see §4.
- **Bond:** always visible on the Creature's page, never hidden. It may steer the **evolution branch** and unlocks **extra moves** beyond the level-up list. It never adds hidden stat growth. Rules: see §3.
- **Habitat and time:** an **in-game clock**, not the device clock. One in-game day ≈ **24 minutes** of play, in four times of day (morning, day, evening, night). Resting at a Rest point jumps to a chosen time of day. Weather rolls per Area per in-game day. Creatures that appear only at certain times are always reachable by resting, so nothing is permanently missable. Spawn rules: see §3.

### Loops and session length
*Source: [What is the core game loop, and what makes Project Wildling different?](issues/05-core-loop-and-pillars.md)*

- **Moment-to-moment (seconds to minutes):** explore an Area → meet a Creature or trainer → battle and/or catch → Creatures gain XP and Bond.
- **Session (5–15 min):** every session ends with at least one meaningful beat (a catch, a level-up or Bond milestone, a route cleared, a Restoration stage, a story step). Twenty such beats chained over an hour should flow too.
  - **Suspend anywhere, resume instantly**; autosave at safe points (after battles, on Area changes, after the Restoration sequence). Save mechanics: see §6.
- **Long-term (hours):** build a team → beat a Boss → a big Restoration stage → new Areas, Habitats and Creatures open → take on the next Boss.
  - A mostly linear **"string of pearls"** in **5 Chapters of 1 / 2 / 3 / 1 / 1 Bosses**: Bosses within a Chapter can be taken in any order, and the next Chapter opens once every Boss in the current one is beaten. **No level scaling.** Chapters, gating and levels: see §4.
- **Scale:** Medium (1 region, ~100 Creatures, 15–25 h, 8 Bosses), designed to grow to Large without rewrites.

### Difficulty
*Source: [What is the core game loop, and what makes Project Wildling different?](issues/05-core-loop-and-pillars.md)*

- **Default:** approachable but never brainless. **Grinding is never required** (catch-up XP that helps lower levels, §2). Bosses reward Type choice and switching.
- **Challenge mode:** an optional mode chosen at new game (tougher AI, level caps). The design keeps room for it now: AI one tier up and level-cap data (see §2 and §4). v1 ships the data with no menu option.

### Postgame
*Source: [What is the core game loop, and what makes Project Wildling different?](issues/05-core-loop-and-pillars.md), [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

- **Shape:** finish the Collection log, fully restore the region, Boss rematches at higher difficulty, the rival's daily friendly battle and the postgame one-off at `source`. Same data and systems, **no new mechanics**.
- Rematch levels, frequency and prizes, and the 100%-Restoration acknowledgement and cosmetic: see §4.
- No rematch ladders in v1. A bigger postgame (e.g. a second rematch set) waits for the Large scale.
- Postgame story lines are under [Postgame lines, one-offs and the ferry](#postgame-lines-one-offs-and-the-ferry).

### Title, codename and identifiers
*Source: [What are the game's title and the in-world name for Creatures?](issues/06-naming-and-branding.md)*

- **Title:** **Mendvale**. "Project Wildling" is retired ("Wildlings" is a *Game of Thrones* term).
- **Codename `mendvale`**, permanent: repo folder, effort folder `.scratch/mendvale/`, Godot project name, and app ID **`io.github.andrew689cpu.mendvale`** on **both** stores. Android package names can't contain hyphens, so the ID drops the one in the GitHub handle. The ID never changes; the title is free to change.
- The **GitHub repo stays `rpg`** (github.com/andrew689-cpu/rpg).

### In-world names and the strings rule
*Source: [What are the game's title and the in-world name for Creatures?](issues/06-naming-and-branding.md), [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

- **Code and data use the generic glossary identifiers** (`creature`, `trainer`, `lure`, `sanctuary`, `collection_log`, `mending`, `money` …). In-world words appear **only in localisation strings**, so renaming anything later touches only strings.
- **Every name is a display string** in `strings/en.csv`: in-world terms, the region, every Area and every character. In-world terms are keys too (`term.creature` → "Verdling"), so a rename is one CSV edit. `tr()`, key derivation and English-only v1: see §6.
- `GLOSSARY.md` keeps the generic term as each heading, with an "In-world name" line.
- **Every level and count in the story is data** with a starting value.

| Concept (glossary / code term) | Display string |
|---|---|
| Game title | **Mendvale** |
| Region (the Medium game's one region) | **Mendvale** |
| Creature | **Verdling** (plural Verdlings) |
| Trainer (anyone who raises Creatures: player, rival, everyone) | **Mender** |
| Lure | **Offering** (variants read "<X> Offering", e.g. "Honey Offering") |
| Sanctuary | **Haven** |
| Collection log | **Almanac** |
| Mending | **Mending** |
| Boss | **Steward** (plural Stewards) |
| Faction | **the Yield** (members: **Yield hands**) |
| Money | **Marks** (see §4) |

- **Rejected as other franchises' signature terms:** Lure (Pokémon GO), Sanctuary and Keeper (Monster Sanctuary), Tamer (Digimon), Warden (Pokémon Legends: Arceus).
- No Area or character name may use "haven" (the Sanctuary's string).

### Store listing and name clearance
*Source: [What are the game's title and the in-world name for Creatures?](issues/06-naming-and-branding.md)*

- **App name on both stores:** "Mendvale" (no keyword stuffing).
- **App Store subtitle, and the start of the Play short description:** "A creature-collecting RPG" (25 of 30 characters).
- **Description body** leads with "creatures who grow from how you raise them" and the turn-based RPG structure, not with "restore the region" alone: *Pokémon Pokopia* (2026) also restores a withered region habitat by habitat.
- **Known risks, accepted:**
  - A Shopify accessibility app (*Mendvale - Accessibility*, launched August 2026) uses the name and owns mendvale.com. A legal clash is unlikely in a different market; search results are shared. No domain is needed.
  - "Mending" is also a Minecraft enchantment: an ordinary English word, unrelated use.
  - The hobby-level check ([`research/name-clearance.md`](../../research/name-clearance.md), not legal advice) could not query the USPTO, EUIPO or WIPO registers directly.
- **Before release (human checklist):** manually search USPTO (classes 9, 28 and 41), EUIPO, WIPO, both app stores and itch.io for exact matches of "Mendvale" and "Verdling", and recheck the Shopify app's trademark status. If a name fails, rename it: only strings and the listing change.
- **Open:** the rest of the store listing (full description, screenshots, keeping a non-child-directed look) is still fog; see §6.

### How the story is told
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

- **Medium weight:** short beats at each flag, plus one running thread (the Rival and the Faction) through the Chapter transitions. Most of the story is told by the world: NPC lines that change with each Restoration stage, and Hidden-site flavour (pillar 1).
- **Budget:** a flag beat is **≤ 60 seconds** of reading (about **8–12 `say` lines**). Story text can be **fast-forwarded but not skipped**.
- Every beat is an event built from the closed command list (`say`, `move_actor`, `set_flag` …, see §6) on existing sprites. **No cutscene art.**
- **Tone:** cozy to adventurous, for 13+. The antagonists are **misguided, not evil**.
- **Open:** writing every event script and each Area's per-stage NPC lines is implementation work for the slices.

### Setting
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

- **The region is Mendvale:** a long vale with a river running south from **the Wellspring** at its northern heart (`source`). The Region map reads bottom to top.
- **The Blight.** About **30 years ago**, in a drought year, the Wellspring's own Boss (Weller) tapped it to make Creatures grow faster and stronger: forced, not raised. The spring soured, and the Blight has crept south ever since. It leaves Areas and their Creatures **muted and quiet, never monstrous**. This is pillar 2 as the villain's mistake.
- **The roots.** Each landmark holds a **root**, one of the springs the Wellspring once fed; the landmark's focal point is its root. When the Blight came, each Boss put their root to sleep so the Blight couldn't drink from it, and has guarded it since. A Boss won't wake it until a Trainer's team proves its Bond. **Beating the Boss is that proof:** afterwards the Boss and the player wake the root together, and the spoke heals outward (the Restoration ring animation, §4/§5).
- **The home town (`home_town`) was never Blighted** because the Blight hasn't reached it yet. It reached `route_1` this spring. Young Creatures fleeing south shelter in the home town. All creeping happens before the game starts: during play **nothing ever re-Blights**.
- **No "Blight" Type.** The Faction uses Shade.

### Cast
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

| Role | Display name | Where / record | Who |
|---|---|---|---|
| Protagonist | player-named | – | A young Trainer who grew up in the home town, set on going north. Mostly silent: occasional choice lines that change nothing. **2 looks** in v1 (data). |
| Mentor | **Hollis** | `home_town` inn | The home town's innkeeper, a retired Trainer who sends the player north. Their old field notebook becomes the Collection log. Not a professor: no lab and no handout speech. |
| Rival | **Bryn** | trainer records | A home-town friend who leaves the same morning, too impatient to wait for a Starter. |
| Boss 1 (Wild) | **Pip** | `warren` | Young; inherited the root from a parent last year. Nervous and earnest. |
| Boss 2 (Grove) | **Hazel** | `elder_tree` | An old forester, slow-spoken. The Faction asked for this root and was refused. |
| Boss 3 (Tide) | **Marlow** | `tide_shrine` | A cove fisher, blunt and warm. |
| Boss 4 (Stone) | **Slate** | `quarry` | The quarry boss, proud of the work. |
| Boss 5 (Volt, 2v2) | **Sparrow and Kit** | `storm_tower` | Siblings who rebuilt the tower. They bicker constantly and fight as one (**one Boss record**, §4). |
| Boss 6 (Frost) | **Tarn** | `glacier` | A mountain guide, laconic. |
| Boss 7 (Lumen) | **Morrow** | `lighthouse` | Weller's oldest friend, who carries the guilt of not stopping them. |
| Boss 8 (mixed) | **Weller** | `source` | Founder of the Faction and the Wellspring's own Boss 30 years ago. |
| Faction | **the Yield** / **Yield hands** | trainer records | See [The Faction](#the-faction). |
| Rest-point NPC | **Lantern-keeper** | one NPC record at every inn and camp | Tends the Rest point (it is the `rest_point` marker, §6) and gives the Lure safety net. |
| Ferry | **Ferry operator** | `harbour`'s dormant exit | See [the ferry](#postgame-lines-one-offs-and-the-ferry). |

- **All text is pronoun-free** for the protagonist and every named character. **All names are gender-neutral.**
- Names were checked against well-known Pokémon character names (Rowan, Oak, Alder, Birch, Elm, Willow, Flint and Ash were dropped) and avoid "haven".
- **Name entry:** a free text field of **up to 10 characters**, plus a **dice (🎲) button** that suggests a name from a short gender-neutral list (data).

### The Faction
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

- A misguided group that believes the tap failed only because it was too timid. It wants to tap the Wellspring "properly" and give the vale strong Creatures overnight. Motto (string): *"the vale needs strength, not patience."*
- **Teams:** Shade-led, with some Flame.
- **Forced Creatures are flavour only:** ordinary species records within the level bands, with quiet, tired idle lines. **No** special Status, Trait or rule.
- **Yield hands are ordinary trainer records** and count toward their Area's "beat the trainers here" Mending. **No separate faction system.**
  - Chapters 2–4: **2–3 per Chapter**.
  - Chapter 5: they hold `blight_heart`, filling its 3–5 trainers.

### Starters, the gift and the Lure safety net
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

- **Why the trio is random:** which three young Creatures are sheltering in the home town this season varies; that is the per-save seed (§3). The player picks one, and **the other two slip off north**, which is why every Starter turns up Rare in Chapter 2–3 Areas (§3).
- **The gift:** Hollis hands over the Collection log and the **starting kit, unchanged** (1,000 money, 5 basic Lures, 3 small heals; §4).
- **The Lure safety net** (§4) is given by the **Lantern-keeper** at whatever Rest point it fires: *"Hollis asked us to keep a few spare for you."*

### Beat sheet
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

What each flag restores is in §4; this table is the story beat behind it.

| Flag or moment | Where | Beat |
|---|---|---|
| New game | `home_town` inn | Hollis: the Blight reached `route_1` this spring, and Creatures are sheltering here. Name and look are chosen. Bryn bursts in and leaves to "fix it first", with no Starter. |
| `starter_chosen` | `home_town` → `route_1`'s edge | Pick 1 of the 3 sheltering Creatures; the others slip off north. Hollis gives the Collection log and the kit. Player and Starter tend the dried spring (the route's focal point), the tutorial Restoration plays, and the barrier clears. |
| `boss_1` | `warren` | Pip wakes the first root with the player and explains the Wellspring, the Bosses and the sleeping roots, then points north. The win event sets `chapter_2_open` (`route_3` heals). |
| Rival battle 1 | `route_3` | Bryn, on Gale and Flame, is proud of a team caught on the road. |
| First Faction sighting | `route_4` / `deepwood` | Yield hands stripping Forage. |
| `boss_2` | `elder_tree` | Hazel wakes the root. Lore: the Faction asked for it. |
| `boss_3` | `tide_shrine` | Marlow wakes the root. Lore: the Wellspring soured about 30 years ago. |
| `chapter_3_open` (combined) | wherever the second Chapter-2 Boss falls | That Boss: *"Both roots awake; Millbrook will feel it."* `hub_2` heals through the pending-presentation queue the next time the player enters. The `route_6` barrier clears. |
| Rival battle 2 | `route_6` | Bryn now has a forced Shade Creature from the Faction and is winning fast. Loses anyway and leaves rattled. |
| The Faction in Chapter 3 | `sunken_works` | Restarting old pumps that once piped water north toward the Wellspring. |
| `boss_4`, `boss_5`, `boss_6` | `quarry`, `storm_tower`, `glacier` | Each wakes its root. Tarn has seen Yield hands heading for the coast. |
| `chapter_4_open` (combined) | wherever the third Chapter-3 Boss falls | That Boss sends the player to the coast. `hub_3` heals; the `route_10` barrier clears. |
| Rival battle 3 | `route_10` | Bryn's Shade Creature is struggling. After the loss, Bryn sees it, turns from the Faction, and starts raising it properly. |
| Optional reveal | `observatory` | Old notes show the Faction's founder was the Wellspring's own Boss, who tapped it in a drought year. |
| `boss_7` | `lighthouse` | Morrow tells Weller's story outright, whether or not the notes were found. The win event sets `chapter_5_open` (`harbour` and `route_12` heal). |
| Tag battle | `blight_heart` entrance | Bryn joins the player against a Yield pair in a 2v2. Afterwards Bryn stays at `outpost`. |
| `boss_8` | `source` | Weller fights to finish the tap. After the loss, Weller and the player wake the Wellspring together, and Weller stays to tend it. `blight_heart`, `source` and `outpost` heal. **Credits.** |

- A **combined flag's beat** (`chapter_3_open`, `chapter_4_open`) plays right after the Boss win that completes it, at that landmark. The hub's Restoration then plays the next time the player enters it (the pending-presentation queue, §4).

### Rival
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

- **Gale and Flame** from Chapter 1, plus the forced **Shade** Creature from rival battle 2 on.
- Bryn **never uses a Starter line**, so "no Starter line on a trainer team before Chapter 3" (§3) holds trivially, and the counter-pick cliché (awkward with a random trio) is skipped.
- **Levels:** rival battles 1–3 sit where a Chapter opens, so the ace is **the previous Chapter's ace + 1**, with the rest 1–2 levels below. All fit the trainer ceilings in §4.

| Battle | Where | Team size | Ace | AI tier |
|---|---|---|---|---|
| 1 | `route_3` | 2 | 13 | Trainer |
| 2 | `route_6` | 3 | 23 | Trainer |
| 3 | `route_10` | 4 | 35 | Boss |
| Tag (ally) | `blight_heart` | Bryn's own | 46 | Boss |
| Postgame friendly | `outpost` | 6 | 60 | Boss |

- The **Yield pair** in the tag battle is at **≤ 50**.

### Tag battle
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

- **Slot `controller` rule:** each slot on a set encounter's side has an optional `controller`, `player` (the default) or an AI tier; a side with an AI-controlled slot has exactly one `player` slot. Field and AI wiring: see §6; battle rules: see §2.
- In the tag battle, Bryn's slot sends Creatures from Bryn's team and the player's slot sends from the Party, one at a time.
- **The player loses when the Party is out.** If only Bryn's team is out, the player fights on alone.
- Bryn's Creatures gain **no XP or Bond**. The ally's slot shows its own HP and Energy bars but takes no player input.
- Reusable later (e.g. a pair of Trainers joining the player).

### Postgame lines, one-offs and the ferry
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

- **Bosses:** one new line each when their rematch is ready (e.g. *"The root's strong now. Want to see what it's grown?"*).
- **NPCs:** each Area's final-stage lines, written with that Area.
- **Weller** tends the Wellspring at `source`.
- **Bryn** stays at `outpost` raising the Shade Creature and offers a friendly battle **once per in-game day**, shown by the rematch idle cue. Bryn is a **trainer record** with a rematch-style team, **not a Boss**: no Bosses-beaten count, and the prize is the rematch formula (**50 × the highest level**, §4).
- **Rare one-offs** (placement in §4):
  - **`observatory` (stage 3):** the Creature young Weller was studying, seen in the notes. It returns once the observatory is fully restored.
  - **`source` (stage 2):** the Wellspring's own Creature, which wakes once the spring is healed.
- **The ferry at `harbour`:** the operator says boats stopped when the Blight came. After the finale they add: *"Word from across the water: their shore's gone quiet too."* A hook with no promise. A second region wakes the dormant exit with an event (§4, §6).

### Display names: Areas
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

- The region displays as **Mendvale**. **Interiors** are named after their parent ("Lowfold Inn").
- **Area IDs stay as they are:** IDs are permanent, names are strings (§6).

| ID | Name | ID | Name | ID | Name |
|---|---|---|---|---|---|
| `home_town` | Lowfold | `tide_shrine` | Tide Shrine | `ice_cave` | Rimefall Cave |
| `route_1` | Wellside Lane | `route_6` | Ridgeback Road | `glacier` | Frostcrown Glacier |
| `route_2` | Reedwood Trail | `hub_3` | Threeways | `route_10` | Seawind Road |
| `warren` | Burrow Hill | `route_7` | Shale Trail | `harbour` | Saltharbour |
| `route_3` | Dryford Road | `old_mine` | Tinmouth Mine | `route_11` | Cliffside Path |
| `hub_2` | Millbrook | `quarry` | Greystone Quarry | `observatory` | Starwatch |
| `route_4` | Mossway | `route_8` | Old Works Road | `lighthouse` | Lastlight |
| `deepwood` | The Deepwood | `sunken_works` | The Sunken Works | `route_12` | Coldstep Road |
| `elder_tree` | The Elder Tree | `storm_tower` | Storm Tower | `outpost` | Highwatch |
| `route_5` | Saltmarsh Path | `route_9` | Highpass Trail | `blight_heart` | The Hushed Halls |
| `cove_town` | Gullcove | `peak_village` | Cloudrest | `source` | The Wellspring |

### Display names: cast
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

| Character | Name |
|---|---|
| Protagonist | player-named (≤ 10 characters, or a suggestion from the gender-neutral list) |
| Mentor | Hollis |
| Rival | Bryn |
| Boss 1 … 8 | Pip, Hazel, Marlow, Slate, Sparrow and Kit, Tarn, Morrow, Weller |
| Faction / members | the Yield / Yield hands |
| Rest-point NPC | Lantern-keeper |
| Ferry NPC | Ferry operator |

### Linter checks
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

1. No Starter line on Bryn's teams.
2. Rival battles 1–3 sit at the previous Chapter's ace + 1. Every rival and Faction team fits the derived Chapter's trainer ceiling.
3. A set encounter with an AI-controlled slot on the player's side has exactly one `player` slot.

## 2. Battle and moves

Every number here is data with a starting value, tuned in playtesting. The battle screen layout and command deck are in §5. The battle core's interface, the seeded `Rng`, battle events and mid-battle resume are in §6.

### Constraints from the genre survey
*Source: [What stat, damage and type-chart systems do creature-collector games use?](issues/03-battle-mechanics-reference.md)*

- **Signature mechanics not to copy:** Temtem's ally synergy bonus and stamina overspend; Coromon's forced rest and Potential grades; Cassette Beasts' fusion and type reactions; SMT's Press Turn; Monster Sanctuary's combo meter.
- **Decompiled code is reference only:** never copy its code or data tables.
- **Mobile levers adopted below:** visible randomness, a capped dual-type multiplier, one Energy bar instead of per-move counters, a shown catch %, XP that helps lower levels catch up, and Statuses with visible countdowns.

### Formats and slots
*Source: [How does a battle work?](issues/07-battle-system.md) · [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md) · [How does the game feel on a touchscreen?](issues/11-controls-and-orientation.md)*

- **1v1** is the default. Wild battles are always 1v1.
- **2v2** happens only in **set encounters** (some trainers, some Bosses, tag fights, Area-challenge pairs), never wild battles. The data model allows **N Creatures per side**.
- **Targeting in 2v2:** the player picks both Creatures' actions in turn, then taps a foe sprite to target. A move with only one valid target picks it automatically.
- **Per-slot controller:** each slot on a set encounter's side has an optional `controller`, `player` (default) or an AI tier. `BattleAI.choose` takes a side and tier, narrowed to a slot.
- **AI ally slot (tag battle):** the ally's slot sends Creatures from the ally's own team, and the player's slot sends from the Party, one at a time. **The player loses only when the Party is out**; if only the ally's team is out, the player fights on alone. The ally's slot shows its own HP and Energy bars but takes no player input. **The ally's Creatures gain no XP or Bond.** The tag battle itself is in §1.
- **Lint:** a set encounter with an AI-controlled slot on the player's side has exactly one `player` slot.

### Types
*Source: [How does a battle work?](issues/07-battle-system.md) · [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

- **10 Types:** Flame, Tide, Grove, Gale, Stone, Volt, Frost, Shade, Lumen, Wild (lowercase in data, e.g. `"type": "flame"`). There is no Blight Type; the antagonist faction uses Shade.
- Every Creature has **1–2 Types**; every move has exactly 1.
- **Multipliers:** 2× / 1× / 0.5×, with **no immunities**. A dual-type target's combined multiplier is **capped at 2× and floored at 0.5×**.
- **Same-type bonus:** 1.25×.
- The chart is a global tuning file (§6).

| Attacker | 2× vs | 0.5× vs |
|---|---|---|
| Flame | Grove, Frost, Wild | Tide, Stone, Flame |
| Tide | Flame, Stone | Tide, Grove, Frost |
| Grove | Tide, Stone | Flame, Gale, Grove |
| Gale | Grove, Wild | Stone, Volt |
| Stone | Flame, Gale, Volt | Grove, Wild |
| Volt | Tide, Gale | Stone, Grove, Volt |
| Frost | Grove, Gale | Flame, Frost |
| Shade | Lumen, Wild | Shade |
| Lumen | Shade, Frost | Lumen, Grove |
| Wild | Volt, Stone | Gale, Shade |

Every pairing not listed is 1×.

- **Open:** colour-blind support (Type colours need icons or labels too); see §7.

### Stats and levels
*Source: [How does a battle work?](issues/07-battle-system.md) · [How is the move list structured?](issues/21-move-list.md)*

- **7 stats:** **HP, Power, Guard, Focus, Will, Speed, Energy.**
- **Power moves** (fist icon) use Power vs Guard. **Focus moves** (spark icon) use Focus vs Will.
- **Levels 1–100.** The Medium credits roll around level 50–55.
- **Stat formula:** species base × level, with **no random component**: no IVs, natures or grades. Bond never touches stats (§3).
- **Energy is the exception:** max Energy is a **flat species value, not scaled by level**, and changes only when the Creature evolves. Typical max is about **100**; Casters and Wardens about **120–140**, Bruisers about **80**. Stat archetypes and stat totals are in §3.
- **Readability:** colour-paired horizontal bars with numbers (Power and Guard warm, Focus and Will cool).
- **Open:** each species' actual stats (per-species design; see §7).

### Traits
*Source: [How does a battle work?](issues/07-battle-system.md) · [How does Bond shape a Creature?](issues/13-bond.md) · [What items exist, and how does the economy work?](issues/14-items-and-economy.md)*

- Each species has **2–3 Traits**. Each Trait has a **condition** (Habitat, time of day or weather), plus **one default Trait** used when no condition matches. If several match, **the first listed in data wins**.
- The Trait is **fixed at the catch** and **shown before offering the Lure**. **No Trait swapping in v1** (§3).
- A Trait is a **passive effect built from a fixed set of effect types** (e.g. "+20% Tide damage in rain", "starts battle with +1 Guard"). There are no held items; Traits fill the passive slot.
- A Trait icon sits in the battle info strip (§5).
- **Open:** the closed list of Trait effect types is not yet written.
- **Open:** each species' Trait list (per-species design; see §7).

### Energy and the Basic move
*Source: [How does a battle work?](issues/07-battle-system.md) · [How is the move list structured?](issues/21-move-list.md)*

- **4 equipped moves plus the free Basic move.** Learned moves are kept forever and swapped freely outside battle.
- **One Energy bar per Creature.** It regains **20% of the Creature's own max per turn** and refills after battle. Move costs are **absolute numbers** (15 weak to 60 finisher; see Bands), so a high-Energy Creature really does fire more big moves.
- Moves the Creature can't afford are greyed out. **No overspend penalty and no forced rest.**
- **The Basic move:** 30 power, 100 accuracy, costs no Energy, uses the Creature's **first Type**, gets **no same-type bonus**, and uses **whichever of the user's Power and Focus is higher**, against the matching defence (Guard or Will). It takes about 10% of an equal-level neutral foe's HP. It **never moves a Leaning** (§3).
- An Energy tonic (+50% of max Energy, battle only) is in §4.

### Damage, accuracy and crits
*Source: [How does a battle work?](issues/07-battle-system.md) · [How is the move list structured?](issues/21-move-list.md)*

- **Formula:** `power × attacker level × attack ÷ defence × k × modifiers`.
  - Attack ÷ defence is Power ÷ Guard for a Power move, Focus ÷ Will for a Focus move.
  - **Modifiers:** Type multiplier, same-type bonus (1.25×), stat stages, Trait, plus the effects below where they apply: crit (1.5×), spread (0.75×), `empower_ally` (×1.5), `condition_boost` (×1.3 power).
- **The level term** means a move of a given power takes the same share of an equal-level foe's HP all game long, because stats and HP both grow with level. Power bands never creep; later moves get better through tiers and side effects.
- **`k`** is set so a move of power P takes about **P ÷ 3 % of HP** from an equal-level, neutral target, with a mid roll and no same-type bonus. `k` lives in `content/tuning/move_bands.json`.
- **Roll:** 90–100%.
- **Crits:** no random crits. Only a move whose card shows a `crit_pct` can crit, and a crit does **1.5×**.
- **Accuracy** is fixed per move and shown. **No accuracy or evasion stages.**
- **Spread:** a move that hits all foes does **75% to each, only when it actually hits 2 or more targets**. In 1v1 an all-foes move does full damage.

### Preview and turn order
*Source: [How does a battle work?](issues/07-battle-system.md) · [How does the game feel on a touchscreen?](issues/11-controls-and-orientation.md)*

- **Pick, then resolve.** Every side picks its actions, then the turn resolves.
- **Order:** priority, then Speed; **ties go to the player's side**. Priority is only −1, 0 or +1.
- **Before confirming,** the player sees:
  - the **damage range as a % of the target's HP, plus effectiveness**
  - the **%** of any chance to inflict a Status
  - the **turn-order indicator** (portraits in order)
  - the catch % on the Catch command
- Tap a move once to preview it, tap again to confirm; a "one-tap moves" setting skips the preview (§5).

### Statuses and stat stages
*Source: [How does a battle work?](issues/07-battle-system.md)*

- **6 Statuses.** Each has a **visible turn countdown**. A Creature has **at most 1** at a time, and **all clear after battle**. No random "may skip a turn" effects.

| Status | Effect |
|---|---|
| **Burn** | loses 1/12 max HP per turn; Power lowered |
| **Poison** | loses HP each turn, increasing each turn |
| **Chill** | Speed halved |
| **Fatigue** | regains no Energy |
| **Snare** | can't switch out (fleeing a wild battle still works) |
| **Drowsy** | skips its next turn, then immune to Drowsy for 3 turns |

- **Stat stages** run from **−2 to +2 at ±25% per step** (×0.5 to ×1.5). They show as arrows on the HP bar and **reset on switching or at battle end**.
- **Open:** starting values for each Status's countdown length, Poison's per-turn damage and ramp, and Burn's Power cut are not set.

### Switching, items and fleeing
*Source: [How does a battle work?](issues/07-battle-system.md) · [How do catching, the party, and storage work?](issues/08-catching-and-party.md) · [What items exist, and how does the economy work?](issues/14-items-and-economy.md)*

- **Switching** uses up the turn; the incoming Creature arrives **before the opponent's move**. Snare blocks it.
- **Items** use up the Creature's turn. Lures and Energy tonics work only in battle; the item list is in §4.
- **Fleeing** from wild battles always works, even while Snared. Trainers and Bosses can't be fled. A **trainer battle can be forfeited**, losing only the reward.
- **Open:** whether a Boss battle can be forfeited is not stated (ticket 07 names only trainer battles).

### Catching in battle
*Source: [How do catching, the party, and storage work?](issues/08-catching-and-party.md)*

- The player **offers a Lure** from the Catch command, which shows the catch % (clamped 1–95%) before offering.
- Offering **uses up the turn**. On failure the Lure is used up and the Creature refuses; **it never runs away because of a failed catch**.
- **Trainer and Boss Creatures can never be caught.**
- The catch formula, Lure modifiers and what happens after a catch are in §3.

### Wild and set-encounter battles
*Source: [How does a battle work?](issues/07-battle-system.md) · [How is the move list structured?](issues/21-move-list.md) · [What items exist, and how does the economy work?](issues/14-items-and-economy.md) · [How does Bond shape a Creature?](issues/13-bond.md)*

| | Wild | Trainer | Boss |
|---|---|---|---|
| Format | 1v1 | 1v1 or 2v2 (set encounter) | 1v1 or 2v2 (set encounter) |
| Start | touching a visible wild Creature (§3) | set encounter | set encounter |
| Catchable | yes | no | no |
| Flee | always works | no; forfeit loses only the reward | no |
| AI tier | Wild | from its data (§1, §4) | from its data (§4) |
| Moves | the **4 most recent level-up moves** it could have learned by its level (line list plus the form's extras); no Bond moves (wild Creatures are Bond rank 0); a new catch keeps that loadout | 4 per Creature, listed in data; may include Bond moves up to a rank set in that data | same as trainer |
| Items | none | Care items only, from a per-battle list in its data (separate from the player's bag), with a fixed number of uses | same as trainer |
| Bond points | 1 | 2 | 5 (§3) |

- The battle's **Habitat** (for Traits, `condition_boost` and Leanings) is the Habitat patch for wild battles; outside a patch each Area names a default Habitat, which a set encounter may override (§3). Time of day comes from the in-game clock and weather from the Area's daily roll (§4).
- Every trainer or Boss item use is **announced** in battle text.

### AI
*Source: [How does a battle work?](issues/07-battle-system.md) · [What items exist, and how does the economy work?](issues/14-items-and-economy.md) · [What is the technical architecture?](issues/09-technical-architecture.md)*

- A **separate module** behind a fixed interface, testable on its own. It sees only a read-only view with the same information the player has (§6).

| Tier | Behaviour |
|---|---|
| **Wild** | weighted-random |
| **Trainer** | best expected damage, with type awareness |
| **Boss** | Trainer, plus thinks one turn ahead, switches out of bad matchups, and uses Statuses on purpose |

- **One shared item rule for every tier:** heal a Creature below 30% HP if its expected damage this turn won't KO the foe.
- Each Boss's tier is in §4.

### Challenge-mode hooks
*Source: [How does a battle work?](issues/07-battle-system.md) · [How do the Bosses and Area gating sequence the region?](issues/15-bosses-and-gating.md)*

- **Challenge mode** is an option chosen at new game. **v1 ships its data and fields filled in, with no menu option.**
- It **raises every AI one tier** and gives Bosses a **fourth tier**.
- Each Boss record has an optional **`challenge_team`**; when absent, the normal team runs with the AI one tier up.
- A **level cap** keyed to Bosses beaten (cap = the ace level of the lowest Chapter with a Boss still unbeaten); **XP stops at the cap**. The cap table and its linter check are in §4.
- **Open:** what the fourth (challenge-mode Boss) AI tier does is not specified.

### After battle: HP, XP and defeat
*Source: [How does a battle work?](issues/07-battle-system.md) · [How is the move list structured?](issues/21-move-list.md) · [How do the Bosses and Area gating sequence the region?](issues/15-bosses-and-gating.md)*

- **HP persists** between battles. Energy, Statuses and stat stages reset. **Rest points** heal for free, revive fainted Creatures and skip the in-game clock (§4).
- **XP** goes to the **whole Party**, scaled by level gap: Creatures below the enemy's level get more, those far above get much less. An AI ally's Creatures get none.
- The XP constants are tuned so a player who fights only what's on the way reaches the **expected party level** (each Chapter's ace level − 2; §4) with no grinding.
- One after-battle step computes XP split, level-ups, newly learnable moves, Bond points, Leaning nudges and evolution offers (§6; Bond and evolution in §3).
- **A newly learned move fills an empty slot automatically** if there is one. Otherwise a "Learned X" card appears and the move waits in the learned list. There's no "forget a move" prompt.
- **Losing** (whole Party fainted): return to the last Rest point used, healed, and lose **8 × the Party's highest level × (Bosses beaten + 1)** in money, **capped at 50% of the money carried**. The same applies to Boss losses. Items, catches and XP are kept, and Bosses can be retried straight away. This is v1's only money sink (§4).
- **Open:** the XP curve and the level-gap XP formula and constants are not set (the XP curve is a global tuning file, §6).

### Move list: size and per-Type grid
*Source: [How is the move list structured?](issues/21-move-list.md)*

- **144 moves:** **110 level-up** (11 per Type), **20 Bond-only** (2 per Type), **14 signature**.
- Each Type has the same **11 level-up moves**:

| Slot | Power | Focus |
|---|---|---|
| Weak, single target | 1 | 1 |
| Mid, single target | 1 | 1 |
| Strong, single target | 1 | 1 |
| Finisher, single target | 1 | 1 |
| All-foes damage (mid tier) | 1, either category | |
| Moves with no damage (stat, Status, support) | 2, either category | |

- **3 of each Type's 8 single-target damage moves** carry a side effect.
- **Bond-only:** per Type, 1 damaging with a side effect and 1 with no damage.
- Overall about **42% pure damage, 37% damage with a side effect, 21% with no damage**.
- **Every move is a Power or a Focus move**, including moves that deal no damage, chosen by flavour (a war-cry is Power, a ward is Focus). So Style Leaning counts every move use (§3), and the roster's "a Power and a Focus move before the first evolution" rule may be met by a move with no damage. Every Type has a Power and a Focus move at every tier, so that rule can always be met with a line's own Type.
- **The grid is a floor** the linter checks, not a ceiling. Large adds moves freely.

### Bond-only and signature moves
*Source: [How is the move list structured?](issues/21-move-list.md)*

- **Bond-only** (`pool: bond_only`, 20) never appear on a level-up list. They give off-type coverage and stronger side effects. A form's Bond list may use Bond-only moves and ordinary level-up moves.
- **Signature** (`pool: signature`, 14): one per Starter line, at **Bond rank 5 on both** of its final branch forms (12), plus one for each rare one-off (2). Each belongs to **exactly one line**, and is written with that line.
- **Open:** no power/cost/accuracy band is given for the `signature` tier.

### Effect kinds (closed list)
*Source: [How is the move list structured?](issues/21-move-list.md)*

A new effect kind needs code and joins this list; a new move is data only.

| Kind | Parameters |
|---|---|
| `inflict_status` | Status, chance % |
| `stat_stage` | self, target or ally; stat; ±1 or ±2; chance % |
| `heal` | self or ally; % of max HP |
| `drain` | % of the damage dealt, healed by the user |
| `recoil` | % of the damage dealt, lost by the user |
| `energy` | add to self or ally, or drain from a foe; a fixed amount |
| `cure` | clears the Status of self or an ally |
| `reset_stages` | clears the target's stat stages |
| `empower_ally` | the ally's move this turn does ×1.5 |
| `redirect` | this turn, single-target foe moves hit the user |
| `condition_boost` | ×1.3 power when the battle's time of day, weather or Habitat matches |

- **Readability limit:** a damaging move has **at most one side effect**; a move with no damage has **at most two effects**, so every card fits in one line.
- **Left out of v1:** setting weather or terrain (weather belongs to the world and Restoration), Protect-style full-block turns, one-hit KOs, multi-hit, two-turn charge or recharge, forced or self switching, Type changes, copying moves, fixed damage, field hazards, and bonuses based on the ally's Type.

### Multi-target and 2v2 support
*Source: [How is the move list structured?](issues/21-move-list.md)*

- **1 all-foes damage move per Type** (10).
- Heal, `energy` and `cure` are written as "self or one ally", so they work in 1v1. **Only `empower_ally` and `redirect` moves are 2v2-only**; in 1v1 they are greyed out, like a move you can't afford.
- **At most 8 moves are 2v2-only**, and none appears on a line's level-up list before level 20.
- **Boss 5's Volt kit** (the 2v2 Boss, §4): the two Volt moves with no damage are `empower_ally` (the "charge") and a self-or-ally `energy` move, so "one charges while the other strikes" is built from data, not special code.

### Bands and pricing
*Source: [How is the move list structured?](issues/21-move-list.md)*

All in one global tuning file, **`content/tuning/move_bands.json`** (`k`, the bands and the reference %). Assumes a typical max Energy of 100 and regen of 20 per turn.

| Tier | Power | Cost | Accuracy | ≈ % HP, same-type, neutral |
|---|---|---|---|---|
| Basic | 30 | 0 | 100 | 10 |
| Weak | 50 | 15 | 100 | 21 |
| Mid | 75 | 30 | 100 | 31 |
| Strong | 100 | 45 | 95 | 42 |
| Finisher | 130 | 60 | 90 | 54 |

- Each extra point of Energy over the Basic move buys a flat **about 2.1–2.2 power** across tiers. Finishers trade that efficiency for tempo, with a miss risk.
- A weak move every turn can be kept up forever. A typical fight lasts **3–5 turns**. A same-type, super-effective finisher takes about **100%** of an equal-level foe's HP.
- **Moves with no damage and all-foes moves** take the tier nearest their cost.
- **Pricing:** each side effect or special costs **one step** of power at the same Energy cost, unless noted. A step is about 20% of the tier's power: weak 50 → 40, mid 75 → 60, strong 100 → 80, finisher 130 → 105.

| Effect | Band |
|---|---|
| Status on hit | 20% / 30% / 50% chance; never 100% on a damaging move |
| Status-only move | 100% chance, 90% accuracy, cost 30 (Drowsy: 45) |
| Stat stage on hit | +1 self or −1 foe, at 30% or 100%; ±2 only on moves with no damage |
| Stat-only move | ±1 for cost 20, ±2 for cost 35 |
| Priority +1 | power 40, cost 20; about 5 in total |
| Priority −1 | only a few strong Stone and Wild moves, one step **higher** |
| Crit | `crit_pct` 25 on the card, one step lower; about 6 in total |
| Drain | heals 50% of the damage dealt, one step lower |
| Recoil | 25% of the damage dealt, one step **higher** |
| Heal | 25% (cost 30) or 50% (cost 50) of max HP, never more |
| `empower_ally` | cost 20 |
| `redirect` | cost 25, priority +1 |
| `condition_boost` | ×1.3, no power cost; about 1 per Type |

- **Open:** the linter's tolerance around each band is not set.

### When each tier becomes available
*Source: [How is the move list structured?](issues/21-move-list.md)*

Every stage of the game gets fresh options through *when* moves are learned, not power creep.

| Tier | Earliest level on a level-up list | Earliest Bond rank |
|---|---|---|
| Weak | 1 | 1 |
| Mid | 12 | 2 |
| Strong | 25 (Chapter 3) | 3 |
| Finisher | 36 (Chapter 4) | 4 |
| Signature | n/a | 5 only |

This puts finishers before Bosses 6–8.

### Type identity
*Source: [How is the move list structured?](issues/21-move-list.md)*

A design guide: a Type's side effects and moves with no damage come mostly from what it "owns".

| Type | Statuses | Leans on |
|---|---|---|
| Flame | Burn | recoil, Power up |
| Tide | – | heal, cure, Guard up |
| Grove | Poison, Snare | drain, heal |
| Gale | – | priority, Speed up/down |
| Stone | – | Guard up, recoil, redirect, −1 priority |
| Volt | Fatigue | `energy`, `empower_ally`, crit |
| Frost | Chill | Speed down, Will up |
| Shade | Snare, Drowsy | drain, `energy` drain, crit |
| Lumen | Drowsy | cure, `reset_stages`, Will up |
| Wild | – | Power up, recoil, priority |

The linter checks only one rule from this table: a Status sits on its 1–2 home Types, and each other Type borrows **at most 1 move per Status**.

### The move record
*Source: [How is the move list structured?](issues/21-move-list.md)*

One JSON file per move, `content/moves/<id>.json`:

```json
{
  "id": "cinder_nip",
  "type": "flame",
  "category": "power",
  "tier": "weak",
  "pool": "level_up",
  "power": 40,
  "cost": 15,
  "accuracy": 100,
  "target": "one_foe",
  "priority": 0,
  "crit_pct": 0,
  "effects": [{ "kind": "inflict_status", "status": "burn", "chance": 20 }],
  "anim": "bite"
}
```

| Field | Values |
|---|---|
| `id` | permanent snake_case ID |
| `type` | one of the 10 Types |
| `category` | `power` or `focus` |
| `tier` | `weak`, `mid`, `strong`, `finisher` or `signature`; explicit so the linter knows which band to check |
| `pool` | `level_up`, `bond_only` or `signature` |
| `power` | 0 for a move with no damage |
| `cost` | absolute Energy cost |
| `accuracy` | fixed %, shown |
| `target` | `one_foe`, `all_foes`, `one_ally`, `self`, `self_or_ally` or `all`; `all` (both sides) only for moves with no damage in v1, so no damaging move hits its own ally |
| `priority` | −1, 0 or +1 |
| `crit_pct` | 0 unless shown on the card |
| `effects[]` | from the closed list of 11 effect kinds |
| `anim` | one of ~12 code effects, tinted by the Type's colour: `strike`, `slash`, `bite`, `burst`, `beam`, `orb`, `wave`, `rain`, `quake`, `gust`, `aura`, `shield`. Move visuals need no art. |

### Card text, strings and names
*Source: [How is the move list structured?](issues/21-move-list.md)*

- **The rules line on a card** ("20% Burn", "+1 Guard to self", "Heals 50% of damage dealt") is **generated from `effects[]`**, so it can never disagree with what the move does.
- **Strings** hold only `move.<id>.name` and an optional one-line `move.<id>.flavour`. Flavour shows on the Creature's page, not on the battle deck. The deck shows name, cost, Power/Focus icon, Type colour and accuracy (§5).
- **Names:** 1–2 plain-English words in the register of Mendvale, Verdling and Mender (craft, nature and material words). At most **12 characters** including spaces, title case, unique. The limit is re-checked against the real button width when the battle UI is built.
- Names are checked against the same franchise **blocklist file** as species names (§3), extended with the genre's well-known move names ("Thunderbolt", "Ember", "Tackle", "Flamethrower" …). Generic English words are fine unless they're a famous move name.

### Permanence and patches
*Source: [How is the move list structured?](issues/21-move-list.md)*

- Moves keep **permanent snake_case IDs** and are only ever added, never removed or renumbered.
- A move's **Type and category never change**. Power, cost, accuracy and effect values may be retuned in a content patch; a paused battle whose moves changed falls back to the pre-battle autosave (§6).
- A new effect kind is a code change and joins the closed list.

### Move lint rules
*Source: [How is the move list structured?](issues/21-move-list.md) · [How do the Bosses and Area gating sequence the region?](issues/15-bosses-and-gating.md)*

1. The schema, the closed effect-kind list, the `anim` list and the readability limit (≤ 1 side effect on a damaging move, ≤ 2 effects on a move with no damage).
2. Each move within its tier band and side-effect pricing, within a tolerance.
3. The per-Type grid floor: 11 level-up moves in their slots, 2 Bond-only moves.
4. A Status sits on its home Types, plus at most 1 borrow per other Type.
5. Tier floors: by level on level-up lists, by Bond rank on Bond lists; signature moves only at rank 5.
6. `bond_only` moves on no level-up list; each signature move on exactly one line.
7. 2v2-only moves: at most 8, and none on a level-up list before level 20.
8. Damaging moves never use the `all` target.
9. Trainer and Boss loadouts learnable by that species at that level and Bond rank.
10. Move names: at most 12 characters, unique, absent from the blocklist.

### Order of work
*Source: [How is the move list structured?](issues/21-move-list.md)*

- The **110 level-up moves and 20 Bond-only moves are one content slice, done before roster batch 1** (§3), because every line picks from them. The slice is done when every move lints clean.
- **Signature moves are written with their own line.**
- **Open:** choosing each species' actual level-up and Bond moves is per-species design (§7).

## 3. Creatures: catching, party, Bond and roster

**Every number in this section is data or a design budget with a starting value, tuned in playtesting.** Code and data use the generic terms (`creature`, `lure`, `sanctuary`, `collection_log`); the in-world names (Verdling, Offering, Haven, Almanac) live only in strings (see §1).

### Wild Creatures and spawning
*Source: [How do catching, the party, and storage work?](issues/08-catching-and-party.md) · [What exactly does an Area's `.tmj` contain?](issues/23-area-map-format.md) · [How is the Creature roster structured?](issues/16-roster-structure.md) · [How is the move list structured?](issues/21-move-list.md)*

- **Visible, no random encounters.** Wild Creatures are drawn on the map; touching one starts a 1v1 wild battle (fleeing always works, see §2). There are no hidden random encounters.
- **Habitat patches.** A patch is a **4-connected run of map cells of one Habitat kind** (logic tiles `meadow` … `ruins`, found by the bake per Restoration stage; see §6 for the map format). Patch IDs are bake-assigned and not permanent; spawn state is never saved.
- **Up to 4 wild Creatures per patch** (per connected run). A caught or defeated Creature is replaced after a short delay. The whole patch re-rolls when the time of day or weather changes, or when the player re-enters the Area.
- **Wild Creatures never leave their patch's cells.** A patch's edge is where the danger stops.
- **Behaviour**, one per species in its data:

  | Behaviour | Rule |
  |---|---|
  | `wander` | drifts around within its patch |
  | `curious` | approaches the player, but only up to the patch's edge |
  | `shy` | flees within its patch if the player runs nearby; walking slowly lets you approach |

- **Shimmer:** Rare and Very rare Creatures have a subtle shimmer on the map. No sound alert.
- **Spawn tables** are per **Area × Restoration stage**. Each entry has species, Rarity tier, level range and conditions (Habitat kind, times of day, weather). The game rolls only among entries whose conditions match right now. Two patches of the same Habitat kind in one Area share a spawn table; an Area that needs two different mixes uses two Habitat kinds.
- **Rarity tier weights** (global tuning): Common **50**, Uncommon **30**, Rare **15**, Very rare **5**. Any entry may override its weight.
- **Rarity lives on spawn entries, never on the species record.**
- **No level scaling.** Levels are fixed per Area (later Restoration stages may add +1–2 at the top of a band; Chapter bands are in §4).
- **Wild loadout:** a wild Creature equips the **4 most recent level-up moves** it could have learned by its level (line list plus its form's extras) and has no Bond moves (rank 0). A new catch keeps that loadout (see §2).
- Spawn rolls are seeded from the per-save seed, and the core owns wild movement on ticks (see §6).

### Catching
*Source: [How do catching, the party, and storage work?](issues/08-catching-and-party.md) · [How is the Creature roster structured?](issues/16-roster-structure.md) · [What items exist, and how does the economy work?](issues/14-items-and-economy.md)*

- **The player offers a Lure** in battle. The Creature may accept and *choose* to join. There is no container.
- **Catch %** is shown before offering (on the Catch command, see §5), **clamped to 1–95%**, with **no hidden factors**. It is made from:
  - the species' base catch %
  - remaining HP (lower HP raises it a lot)
  - a flat bonus if the target has any Status
  - the Lure's modifier
  - a level factor (harder if the target is far above the Party's highest level)
- **Base catch %** per species (full HP, basic Lure, before the other factors), within **±5** of its band:

  | Base | Middle | Final | Wild starters | Rare one-offs |
  |---|---|---|---|---|
  | 40 | 25 | 12 | 12 | 5 |

- **Lure modifiers:** Basic ×1, Better ×1.5, Best ×2, Habitat Lure ×2.5 when the target's home Habitat matches (×1 otherwise). No guaranteed catch: the 1–95% clamp holds for every Lure. Prices, shop unlocks and the zero-Lure safety net are in §4.
- **Offering uses up the turn.** On failure the Lure is used up and the Creature refuses; **it never runs away because of a failed catch**.
- **Trainer and Boss Creatures can never be caught.**
- **Trait:** fixed at the catch by the Habitat, time of day and weather, and shown before offering (rules in §2).
- **Open:** the exact catch % formula: how the factors combine, the HP curve, the Status bonus and the level factor's numbers.
- **Open:** the respawn delay after a patch Creature is caught or defeated.

### Rare one-off Creatures
*Source: [How do catching, the party, and storage work?](issues/08-catching-and-party.md) · [How is the Creature roster structured?](issues/16-roster-structure.md) · [How is the region laid out?](issues/18-region-layout.md)*

- **2 in Medium.** Each is a **single set encounter** placed in the world's data, never in a spawn table. Each is a single-stage line.
- They sit at **final-stage focal points**: one in Chapter 4 (`observatory`, stage 3, Ruins) and one postgame (`source`, stage 2, after the finale). **Neither is Shade or Lumen.** Their story reasons are in §1.
- If one is fainted or the player flees, it comes back after the player rests at a Rest point, so nothing is permanently missable.
- Caught with the normal Lure rules, with a low base rate (5%) shown as %.
- Never starters. Each has one signature move at Bond rank 5 (see Bond moves).

### Starters and Starter trios
*Source: [How do catching, the party, and storage work?](issues/08-catching-and-party.md) · [How is the Creature roster structured?](issues/16-roster-structure.md) · [How do the Bosses and Area gating sequence the region?](issues/15-bosses-and-gating.md)*

- **The player picks 1 of 3** from a Starter trio. A new game picks one of **4 trios** at random (a 5th trio is Large content).
- A **per-save seed**, rolled at new game and stored in the save, picks the trio. It's reproducible and can't be beaten by reloading; it is also the root of all seeded randomness (see §6).
- Story framing: the three sheltering in the home town, and the two not picked slip off north (see §1).
- **The trios** use 4 of the 7 type triangles in the type chart (see §2). Each of the 12 starter lines is a distinct species line:

  | Trio | Triangle | Vs Boss 1 (Wild) |
  |---|---|---|
  | T1 | Flame › Grove › Tide | Flame strong, others neutral |
  | T3 | Flame › Wild › Stone | Flame strong, Stone weak |
  | T5 | Grove › Stone › Gale | Gale strong, Stone weak |
  | T7 | Gale › Wild › Volt | Gale strong, Volt weak |

- Flame, Grove, Wild, Stone and Gale have 2 starters each; Tide and Volt have 1 each. **Frost, Shade and Lumen are never starters.** The 2 Stone starters are the hardest cases for the Boss 1 gate; Chapter 1's Common Flame and Gale lines carry them.
- **Boss 1 must be beatable with every starter in every trio:** a bot party (the starter plus the two most Common species before Boss 1, at level 10) must win at least 70% of 200 seeded runs, or the content tests fail (see §4).
- **No echoing genre icons:** no fire lizard, grass toad or water turtle.
- **Single-type** at base and middle stage. **All 12 branch at the final evolution**; the axis is chosen per line, with **each axis used by at least 2 starter lines**. A Type-axis branch may give each final form a different second Type.
- **Starter level 5.** Starters evolve at **16 and 34**, so the final form and its branch arrive in Chapter 3, after about 10 hours of Leaning.
- **Every starter is also wild:** all 12 starter base forms appear **Rare in Chapter 2–3 Areas**, each in an Area matching its Habitat, at most 2 per Area, the player's own trio included. So every starter is catchable in every playthrough.
- **No starter line is on a trainer or Boss team before Chapter 3** (the rival never uses one, see §1).

### Party
*Source: [How do catching, the party, and storage work?](issues/08-catching-and-party.md)*

- **6 Creatures.** The first one leads in battle.
- **The lead follows the player on the map** (settings toggle to turn it off), reusing the species' 16×16 map sprite. At Bond rank 3+ the follower uses a happier idle animation or emote (cosmetic only).
- The player can't release their last Creature.

### Sanctuary
*Source: [How do catching, the party, and storage work?](issues/08-catching-and-party.md)*

- Holds every Creature not in the Party. **No size limit.** Reachable from any **Rest point**.
- New catches go there automatically when the Party is full.
- **Version 1 is a menu**, with sorting and filters by Type, Trait, level and species.
- **The data model treats it as a place**: a stored Creature can have a spot on a map, so a walkable Sanctuary Area can come later without a rewrite. Sanctuary decor as a money sink is out of scope for v1.
- Display string: **Haven**.

### Nicknames, releasing and duplicates
*Source: [How do catching, the party, and storage work?](issues/08-catching-and-party.md) · [How does Restoration change an Area?](issues/12-restoration.md)*

- **Nickname:** offered right after the catch (skippable), changeable anytime from the Creature's page. Only a length limit; no profanity filter (offline, single-player).
- **Open:** the nickname length limit's value.
- **Releasing** needs a **"This can't be undone"** confirmation. The Creature returns to the wild. It gives **no reward**, does **not count toward Restoration**, and doesn't undo an Area registration already made. The Collection log keeps it as Caught. Its Bond is lost.
- **Duplicates** are unlimited and meaningful, because Traits, Bond and evolution branches differ per individual.

### Collection log
*Source: [How do catching, the party, and storage work?](issues/08-catching-and-party.md) · [How does Bond shape a Creature?](issues/13-bond.md) · [How is the Creature roster structured?](issues/16-roster-structure.md)*

- **Per species it records:**
  - Seen or Caught
  - where and when it can be found (Habitat, time of day, weather), filled in as discovered
  - Rarity tier **per where-found entry** (a species can have different tiers in different places), derived from content at display time and never saved
  - Traits discovered
  - evolution branches discovered (evolving records the branch)
- **Every form is its own entry** with its own display number, a separate field from the permanent ID (see §6), so species can be inserted when growing to Large. A line's forms sit together in display order: base, then middle, then the two branch forms side by side.
- Each form has a 1–2 sentence log entry (string).
- **Branch forms** show as silhouettes until discovered; seeing one on a trainer's or Boss's team counts as Seen. Since branch forms never spawn wild, completing the log means raising both branches of every line.
- **Native species registration** (caught inside that Area) is a Restoration Mending; rules in §4.
- **Completing the log is a postgame goal.**
- Display string: **Almanac**.

### Bond: what it is
*Source: [How does Bond shape a Creature?](issues/13-bond.md)*

- **Bond = a Bond rank + Leanings.** Rank is *how much* the Creature has been raised and unlocks Bond moves; a Leaning is *which way* and picks the evolution branch.
- Bond **never touches stats**. **No item affects Bond rank, Leanings or Traits** (no Bond treats, re-centring or branch-forcing items). Bond is earned only by raising the Creature.
- **No Trait swapping in v1.** The Trait stays a permanent record of where and when the Creature was caught; the data doesn't rule out a later "re-meet the condition" swap.
- Nothing is rolled or graded at the catch: every Creature starts at zero and becomes what the player made it (never copy Coromon's Potential grades).
- Bond is always visible on the Creature's page, never hidden.

### Bond rank
*Source: [How does Bond shape a Creature?](issues/13-bond.md)*

- **Ranks 0–5.** A Creature earns Bond points only for battles in which it **acted**: used a move, or a Lure was offered while it was out. Being in the Party, or out without acting, earns nothing.
- **Points per battle:** **1** wild, **2** set encounter, **5** Boss.
- **Rank thresholds:** **5 / 15 / 30 / 50 / 80** points. Rank 5 takes roughly 40–60 battles of real use: a core team member gets there within the Medium campaign, and a benched Creature catches up in a few hours.
- **Rank only grows**; nothing is ever lost.
- Beyond moves, rank has **no battle, catch or economy effect**. The only other effect is the cosmetic follower emote at rank 3+.

### Leanings
*Source: [How does Bond shape a Creature?](issues/13-bond.md)*

- **Four axes, a closed list in code** (`style`, `type`, `habitat`, `time`):

  | Axis | Ends | Counted per |
  |---|---|---|
  | Style | Power moves vs Focus moves used | each move use |
  | Type | which of two named move Types it uses (e.g. Flame vs Gale) | each move use |
  | Habitat | which of two Habitat kinds it battles in | each battle it acted in |
  | Time | day-side (morning/day) vs night-side (evening/night) battles | each battle it acted in |

- "Role" (damaging vs Status/stat moves) is deliberately not an axis: many moves are both.
- **Every Creature tracks all four**; a two-branch species' data names **one axis** and its two ends.
- **Needles run −10 to +10.** Each counted action nudges the needle one step toward that end. The **Basic move doesn't count**. A move of a Type that is neither end doesn't move the Type needle.
- A full swing takes about 10 battles, so the player can always steer it back.
- **Battles outside a patch:** each Area names a **`default_habitat`** for battles outside a Habitat patch (trainers, Bosses); a set encounter may override it. If the battle's Habitat is neither end, the needle doesn't move.

### Evolution and branches
*Source: [How does Bond shape a Creature?](issues/13-bond.md) · [How is the Creature roster structured?](issues/16-roster-structure.md)*

- **Trigger: a level threshold per species.** On reaching it, evolution is offered and the player may choose **"Not yet"**; afterwards it can evolve at any time from its page. No evolution items exist.
- **Branch pick:** for a two-branch species, the **needle's side at that moment picks the branch**. A needle at exactly the centre lets the **player choose**.
- Once evolved, the **branch is locked**. Single-form evolutions work the same way without a branch.
- **At most one branch point per evolution line in v1** (it may sit at either evolution). The data allows more; the linter enforces the limit.
- **On the Creature's page**, for a two-branch species:
  - the axis needle with both ends labelled, always visible: `Power ◀──●──▶ Focus`
  - the two branch forms at its ends, as **silhouettes until discovered** (Seen or Caught), then named
  - the end the needle currently favours, highlighted
  - from **5 levels before** the evolution level: "Evolves at Lv 24 · leaning toward [silhouette/name]"
- Species with one form or no branch show **no needle**, only the Bond rank.
- **Branch forms never spawn wild** in Medium; they are only obtainable by evolving.
- **Evolution levels:**

  | Line | Bands |
  |---|---|
  | Starters | 16 and 34 |
  | Other three-stage | first 14–22, second 30–40 |
  | Two-stage | 12–32 (some early Common lines at about 12, so Chapter 1 has an evolution) |

- **No evolution above level 44**, so every final form is usable before Boss 8.

### Bond moves
*Source: [How does Bond shape a Creature?](issues/13-bond.md) · [How is the move list structured?](issues/21-move-list.md)*

- **Each form lists 2–4 Bond moves, each keyed to a rank (1–5)**, with no Leaning condition. The branch gives the flavour: **each evolved form has its own Bond-move list**.
- A Bond list may use Bond-only moves and ordinary level-up moves. Tier floors by rank (weak 1, mid 2, strong 3, finisher 4, signature 5 only) and the move pools are in §2.
- **Signature moves:** each Starter line has one, at Bond rank 5 on **both** its final branch forms; each rare one-off has one. Each belongs to exactly one line.
- **On evolving,** the Creature **immediately learns every Bond move of its new form up to its current rank**. Moves learned before are kept forever.
- A short card appears at each rank-up: "Rank 3 — learned <move name>".
- Bond moves join the learned list and use the normal loadout (4 equipped plus the Basic move). A newly learned move fills an empty slot automatically if there is one (see §2).
- Trainer and Boss Creatures may carry Bond moves up to a rank set in their data; wild Creatures have none.

### Bond lifecycle
*Source: [How does Bond shape a Creature?](issues/13-bond.md)*

- **Bond belongs to the individual Creature.**
- **Sanctuary:** kept unchanged, **no decay**.
- **Evolution:** rank and needles carry over. A Type or Habitat needle **re-centres** only if the new form's ends for that axis differ from the ones it was measured against.
- **Release:** Bond is lost, with no refund or transfer.
- **New catches, duplicates and gift Creatures** start at rank 0 with every needle centred; nothing is inherited.
- Trading is out of scope (offline single-player).

### Bond data and save fields
*Source: [How does Bond shape a Creature?](issues/13-bond.md)*

**Species record:**
```yaml
evolution:
  level: 24
  # either a single form:
  into: species_id
  # or two branches:
  branch:
    axis: style | type | time | habitat
    ends: [power, focus]          # or two Types, [day, night], or two Habitat kinds
    into: [species_a, species_b]  # matching the ends' order
bond_moves:
  - { rank: 1, move: move_id }    # 2–4 entries, ranks 1–5
```

- **Area record:** a `default_habitat`; a set encounter may override it.
- **Global tuning:** rank thresholds, points per battle kind, needle range and step, the 5-level warning window, the follower-emote rank.
- **Save, per Creature:** `bond_points` and `needles` as `{axis: {ends, value}}`. **Rank is derived** from points, and a postponed evolution is derived (level ≥ evolution level, not yet evolved), so neither is stored. Retuning thresholds in a content patch can never take a rank away. The full per-Creature save record (instance id, species, level, XP, moves, Trait, HP, nickname, place) is in §6.

### Roster budget
*Source: [How is the Creature roster structured?](issues/16-roster-structure.md)*

- **The Medium roster is 100 species records** in **34 evolution lines**. Every evolved form and every branch form is one species with its own Collection log number.

  | | Lines | Three-stage | Two-stage | Single-stage | Branching | Species |
  |---|---|---|---|---|---|---|
  | Starters | 12 | 12 | – | – | 12 | 36 + 12 = **48** |
  | Others | 22 | 6 | 12 | 4 (2 ordinary, 2 rare one-offs) | 6 (2 three-stage, 4 two-stage) | 46 + 6 = **52** |
  | **Total** | **34** | 18 | 12 | 4 | **18 of 30 evolving lines** | **100** |

- **Area payoff Creatures** (§4) reuse existing species, as Very rare entries or evolved forms at level L. They add nothing to draw.
- Every species needs a Habitat, times of day, behaviour, 16×16 map sprite and 64×64 front and back battle sprites (art specs in §5).

### Branching
*Source: [How is the Creature roster structured?](issues/16-roster-structure.md)*

- **18 branching lines.** **Each of the four axes is used by at least 4 lines.**
- All 12 starter lines branch at the final evolution (each axis on at least 2 of them).
- The 6 non-starter branches lean on **Habitat and Time** (about 2 + 2, plus 1 Style and 1 Type), for pillar 3 ("Belongs Somewhere").
- A non-starter three-stage line may branch at either evolution. At most one branch point per line.
- The two branch forms of a line share one stat total, so neither is strictly better.

### Types across the roster
*Source: [How is the Creature roster structured?](issues/16-roster-structure.md)*

Counting each Type of a dual-type species once:
- Each Type is on **12–20 of the 100 species**.
- Each Type is the **primary Type of at least 2 non-starter lines**. Starters put none on Frost, Shade or Lumen, so the other lines carry them (about 3 lines each in practice).
- **Boss teams:** the theme Types (Wild, Grove, Tide, Stone, Volt, Frost, Lumen; Boss 8 mixed) each need enough species, evolved forms included, for a team of 2–6 at the Boss's level (12 / 22 / 34 / 44) and a rematch team of 6 at 58–66 (see §4). Each theme Type has **at least 4 distinct final forms**, branch and dual-type forms included, so a rematch team (4 on theme plus 2 coverage) never repeats a species. Flame, Gale and Shade have no Boss; they serve Area challenges, the rival and the antagonist.
- **Counter rule:** the Areas before each Boss offer at least 2 catchable species that hit its theme Type for 2× (see §4). Lumen is hit 2× only by Shade, so **at least 2 Shade lines are catchable before Chapter 4**.
- **About 40% of species are dual-type.** Base forms are mostly single-type; the second Type usually comes at evolution. **No dual-type pair is used by more than 2 lines.**

### Traits through evolution
*Source: [How is the Creature roster structured?](issues/16-roster-structure.md)*

- **2–3 Traits per species:** 1 **default** plus 1–2 with a condition (Habitat, time of day or weather). Trait effects and matching order are in §2.
- Trait **conditions are defined per line**. Each form may give each Trait a different or stronger effect.
- A Creature keeps **which Trait it got** through evolution and branching (its "night Trait" stays its night Trait). A wild-caught evolved form uses the same condition list.

### Habitat and time of day
*Source: [How is the Creature roster structured?](issues/16-roster-structure.md) · [How is the region laid out?](issues/18-region-layout.md)*

- Each species has exactly **one home Habitat kind** (the one the Habitat Lure checks) and a **set of 1–4 times of day**. Its spawn entries must fit both.
- **Habitat kinds** (8, global): Meadow, Woodland, Wetland, Coast, Cavern, Crag, Snowfield, Ruins (region detail in §4).
- The forms in a line share their Habitat. In a Habitat-axis branch, each branch form takes the Habitat of its own end.

### Look
*Source: [How is the Creature roster structured?](issues/16-roster-structure.md)*

- Each species is based on a **real animal, plant or fungus that fits its Habitat**, plus one visible element of its Type.
- **Time of day shows in its colouring:** night species use the cool half of the palette and have larger eyes.
- Every form reads as a **clear silhouette with 2 key colours at 16×16**, within the locked palette (§5).
- A **"do not echo" list** of iconic genre designs (an electric yellow rodent, a fire-tailed lizard, a pink blob, a gas ghost) is checked by eye in review, not by the linter.

### Stat archetypes
*Source: [How is the Creature roster structured?](issues/16-roster-structure.md)*

- A **closed list of 6 Stat archetypes**, used as data templates that a species adjusts slightly:

  | Archetype | Leans on |
  |---|---|
  | Bruiser | HP, Power |
  | Bulwark | Guard, Will |
  | Caster | Focus, Energy |
  | Skirmisher | Speed, Power |
  | Balanced | even spread |
  | Warden | Will, Energy (Status-focused) |

- **Stat totals by stage:**

  | Stage | Total |
  |---|---|
  | Base | ≈ 300 |
  | Middle | ≈ 400 |
  | Final | ≈ 500 |
  | Single-stage | 420–480 |
  | Rare one-off | ≈ 520 |

- Energy is a flat species value (typical max ≈ 100; Casters and Wardens ≈ 120–140, Bruisers ≈ 80), changing only on evolution (see §2).

### Level-up moves
*Source: [How is the Creature roster structured?](issues/16-roster-structure.md)*

- **The level-up list is shared across the line:** **8–12 line moves** across levels 1–55, plus **1–3 moves for each form**.
- A Creature learns the line's list whatever its form, plus its current form's extras. On evolving, it immediately learns any of the new form's extras at or below its level. **Postponing evolution never costs a move, and evolving never skips one.**
- Every line has **1 Power and 1 Focus move before its first evolution**, and moves of **at least 2 Types besides its own** by the final form.
- The move list itself (144 moves, pools, tiers) is in §2.
- **Open:** where the line-shared level-up list and the per-line Trait conditions live in data. The content kinds (§6) have a species record but no line record.

### Rarity across the roster
*Source: [How is the Creature roster structured?](issues/16-roster-structure.md)*

- The roster plan only aims for a spread. Best tier for each line's base form:

  | Best tier | Lines |
  |---|---|
  | Common | 10 |
  | Uncommon | 7 |
  | Rare | 3, plus all 12 starters |
  | Rare one-off | 2 |

- The 17 Common and Uncommon lines, plus middle forms from stage 1, supply the Areas' native-species lists (Common or Uncommon only, see §4).
- **Wild evolved forms, by form:**
  - **Middle forms:** Uncommon or rarer, from stage 1; may be native species.
  - **Final forms:** Rare or Very rare only, from stage 2; never native.
  - **Branch forms:** never wild.

### Debut Chapters
*Source: [How is the Creature roster structured?](issues/16-roster-structure.md)*

- Three-stage lines debut only in Chapters 1–2; a later debut would meet the line already past its first evolution level.
- **Non-starter lines by debut** (wild levels from §4):

  | Debut | Three-stage | Two-stage | Single-stage | Lines |
  |---|---|---|---|---|
  | Ch 1 (wild 4–8) | 4 | 3 | – | 7 |
  | Ch 2 (11–18) | 2 | 3 | – | 5 |
  | Ch 3 (21–30) | – | 4 | 1 ordinary | 5 |
  | Ch 4 (33–40) | – | 2 | 1 ordinary + 1 one-off | 4 |
  | Ch 5 / postgame | – | – | 1 one-off | 1 |

- **Type timing follows the Bosses:** Shade lines debut in Ch 2–3 (Lumen's only counter), Lumen lines in Ch 3–4, Frost lines by Ch 3.
- **Chapter 1** (Meadow, Woodland and Wetland on offer) includes:
  - at least 1 **Gale** and at least 1 **Flame** line, which are the **two most Common species before Boss 1**, so the Boss 1 gate's bot party always carries both Wild counters
  - at least 2 **Wild** lines, for Boss 1's team of 2
- Wild starters, rare one-offs and the no-starter-on-teams rule: see Starters and Rare one-off Creatures above.

### Names
*Source: [How is the Creature roster structured?](issues/16-roster-structure.md)*

- Display names are **4–9 letters, 2–3 syllables**, in the plain-English register of Mendvale, Verdling, Mender and Haven: blends of English roots (plant, animal, craft or material words).
- A **blocklist file** of names from other creature franchises is checked by the linter (the same file also covers move names, §2).
- The forms in a line don't need to share a prefix. IDs stay separate, snake_case and permanent (§6).

### Growing to Large
*Source: [How is the Creature roster structured?](issues/16-roster-structure.md)*

- Medium species are **never removed, renumbered or retyped**.
- Large adds new lines with later numbers. It may add a new **final stage** to an existing Medium line, as a new species, without changing the existing forms. Regional variants are their own species in their own lines. A 5th Starter trio is Large content.

### Unit of work, placeholders and order
*Source: [How is the Creature roster structured?](issues/16-roster-structure.md) · [How is the move list structured?](issues/21-move-list.md)*

- **The design unit is one evolution line**, because Traits, level-up moves, branches and evolution levels all span the line. An agent drafts each line; the human approves silhouettes and names.
- **A line is designed** when:
  - its records lint clean
  - each form has a 1–2 sentence Collection log entry
  - the line has a short design sheet: what it's based on, its silhouette, its 2 key colours, and its archetype per form
- **A line is drawn** when every form's front, back and map sprites are final, within the palette, with licence-ledger rows.
- **Placeholders:** a **dev-only mapping** gives every species a placeholder: one of the 56 sprites from *50+ Monsters Pack 2D*, or a generated silhouette in the palette (shape from its archetype, colour from its Type). The licence ledger has a `placeholder` column. Internal and closed-testing exports allow placeholders; a **production** export fails if any reachable species still uses one (§6). A final replaces its placeholder by dropping files at the conventional paths, with no data change.
- **Order of work:**
  0. The **move-list slice** (110 level-up and 20 Bond-only moves) comes first, because every line picks from it. Signature moves are written with their own line.
  1. **Batch 1 data:** all **12 starter lines** (the Boss 1 gate runs every starter in every trio), plus the **7 Chapter-1 lines** and Boss 1's team.
  2. **Batch 1 art, the vertical slice:** trio **T1** plus the 7 Chapter-1 lines as finals. Everything else stays a placeholder.
  3. **Batches 2–5:** data and art follow the **Chapter where each form is first seen**. Starter middle forms and the other three trios' base forms come with Chapter 2. Starter final and branch forms come with Chapter 3.
  4. **Rare one-offs last.**

  Each batch is a set of line-sized slices, and data may run a batch ahead of the art.
- **Open:** the per-species design itself (each line's species, stats, moves, Traits, names, placement in Areas). It no longer waits on any ticket. It is also undecided whether per-species design belongs in this spec or is later content work done in the batches above.
- **Open:** who draws the final Creature art, and the per-sprite workflow and review (see §5).

### Content-linter rules
*Source: [How does Bond shape a Creature?](issues/13-bond.md) · [How is the Creature roster structured?](issues/16-roster-structure.md)*

**Bond, for each branching species:**
- **Type axis:** both ends are Types the Creature can learn moves of (level-up or Bond) before its evolution level.
- **Habitat axis:** both ends exist in Areas reachable before the line's usual evolution level.
- **Time axis:** always valid (resting skips the clock).
- **Style axis:** the species can learn at least one Power and one Focus move before evolving.
- **Bond moves:** 2–4 per species, ranks 1–5, no duplicates (tier floors by rank and signature rules in §2).
- **At most one branch point per line.**

**Roster:**
- Total species count against the budget, and the forms per line.
- Evolution levels within their bands, and none above 44.
- At most one branch point per line; branch forms in no spawn table.
- Type counts: 12–20 per Type; at least 2 non-starter primary lines per Type; at least 4 final forms per Boss theme Type; no dual-type pair on more than 2 lines.
- Base catch % within ±5 of its stage band.
- Spawn entries fit the species' home Habitat and times of day; every home Habitat is one of the 8 kinds.
- Every line has a Power and a Focus move before its first evolution, and 2 extra move Types by its final form.
- Display names are 4–9 letters and absent from the blocklist.
- Production exports have no placeholders.

## 4. World: Restoration, region, Bosses and economy

**Every number in this section is data with a starting value, tuned in playtesting.** Map-file details (layers, logic kinds, marker classes and fields, the bake) belong to §6; this section points there.

### Restoration stages and triggers
*Source: [How does Restoration change an Area?](issues/12-restoration.md)*
*Source: [How is the region laid out?](issues/18-region-layout.md)*

- **Blighted start.** Every restorable Area starts **Blighted** (stage 0). Stage counts are set per Area in data (1–4) and follow the Area's kind (see Area kinds): routes and dungeons 3, landmarks 2, towns 1–2.
- **0 stages:** only `home_town` (never Blighted, part of the story) and interiors. A 0-stage Area is never Blighted. The Sanctuary is a menu in v1 (§3), not an Area.
- **Order:** stages always apply **in order** and only move forward. Nothing ever re-Blights during play.
- **Stage 1 comes only from the critical path:** a story flag (a Boss beaten, a story beat). One flag may restore **one or more Areas at once**. Which flags restore which Areas is in Flags and Blight barriers below.
- **Stages 2+ come only from Mendings.** Each stage lists its own Mendings and needs **K of M** of them (e.g. 3 of 5); the player picks which.
- **Mendings count early.** A Mending finished while the Area is still Blighted is saved and applies the moment stage 1 lands.
- **Counted Mendings** carry their own mini-progress, so a stage stays a short checklist: "Register 3 of 4 native species", "Beat the 4 trainers here", "Beat the Area challenge", "Find the hidden spring".
- **Never blocks the critical path:** only stage 1 opens critical-path routes (see What a stage changes).

### Mending kinds
*Source: [How does Restoration change an Area?](issues/12-restoration.md)*
*Source: [How is the region laid out?](issues/18-region-layout.md)*
*Source: [What exactly does an Area's `.tmj` contain?](issues/23-area-map-format.md)*

A **closed list** in code: `register_natives(n)`, `defeat_trainers(ids)`, `defeat_challenge(id)`, `find_site(id)`. A new *kind* needs code; a new Area or region doesn't.

- **Registering native species (`register_natives`).**
  - Only **Areas with Habitat patches** list native species: **3–6**, Common or Uncommon only, never Very rare. Areas without patches (every town) list none and have no `register_natives` Mending.
  - A species is registered for an Area when it is **caught inside that Area**, at the moment of the catch, once per species per Area. Catches elsewhere don't count, and evolved forms don't stand in for the listed species.
  - Registration is **permanent**: releasing the Creature later doesn't undo it. Released Creatures never count toward Restoration, and a release earns nothing.
- **Beating local trainers (`defeat_trainers`).** One counted Mending per group of trainers. Trainer counts per Area are in Optional content.
- **The Area challenge (`defeat_challenge`).** At most **one per Area** (in practice one in every route and dungeon, none in towns or landmarks). A stronger set encounter (a veteran trainer, a strong wild Creature, or a 2v2 pair), **visible on the map from the start**, showing a recommended level, retryable, never on the critical path. Postgame repeats go through the Boss-rematch system, not here.
- **Hidden sites (`find_site`).** Interactable spots (a choked spring, a buried seed cache, a cracked shrine), found by exploring with what the player already has. The site's marker ID is its `find_site` ID (§6). **No field-move or ability gates in v1**; the data has an optional condition (a story flag or a Party species) for later. A path opened by one stage may lead to a site that counts toward the next. Sites give no money or items (see Money and income).
- **Linter rule:** every Mending for stage N must be completable while the Area is at stage N−1 (e.g. a species to register must spawn in an earlier stage's table). The pipeline checks this, so designers don't have to remember it.

### What a stage changes
*Source: [How does Restoration change an Area?](issues/12-restoration.md)*
*Source: [What exactly does an Area's `.tmj` contain?](issues/23-area-map-format.md)*

A stage is a data bundle that may change any of:
1. **the spawn table** (one per Area × stage; entry format in §3)
2. **the tiles**, spreading out from the Area's **focal point**: each stage is a hidden change set of only the cells that change (on the ground, detail, overhead and logic layers), stacking on the stages before it; rings are measured by **Chebyshev distance** from the focal point, with the ring width as tuning data (format in §6)
3. **Habitat patches** added or removed (e.g. a pond refills and a water patch appears), including the Forage spots that come with them
4. **NPCs** added, removed, or given new dialogue
5. **paths opened**
6. **shop stock additions**
7. **the weather table**
8. **the music and ambient track**

Rules:
- **Only stage 1 may open critical-path routes**, by clearing Blight barriers. Stages 2+ open only optional paths: shortcuts, side pockets, hidden sites.
- **Restoration never changes battle rules.** Blighted Areas have no buffs or debuffs; only the battle backdrop follows Restoration (§5).
- Later stages may add **+1–2 levels at the top** of an Area's wild band (see Level curve).

### Payoffs
*Source: [How does Restoration change an Area?](issues/12-restoration.md)*
*Source: [How do the Bosses and Area gating sequence the region?](issues/15-bosses-and-gating.md)*
*Source: [How is the region laid out?](issues/18-region-layout.md)*

- **Each Area with Habitat patches gets a payoff Creature at its final stage**: either a rare one-off set encounter at the focal point, or a Very rare entry in that stage's spawn table. Payoff Creatures sit at the current Chapter's ace level **L**. They reuse existing species (§3).
- **The 2 rare one-offs** are at `observatory` (stage 3) and `source` (stage 2, postgame); see Landmarks and the rare one-offs.
- **Towns get no payoff Creature.** A town's final stage pays off through its own changes (NPCs, shop stock, music).
- **100% region Restoration** earns a postgame acknowledgement and a cosmetic (e.g. a flower crown on the following Creature).
- **Restoration rewards are never money or items**; the economy stays separate.

### Showing progress and stage changes
*Source: [How does Restoration change an Area?](issues/12-restoration.md)*
*Source: [How do the Bosses and Area gating sequence the region?](issues/15-bosses-and-gating.md)*
*Source: [How is the region laid out?](issues/18-region-layout.md)*

**In the world:**
- The **focal point changes visibly at every stage** (a dry spring trickles, then flows, then blooms). On a landmark, the focal point is its root (§1). Interacting with it opens the Area's Mending checklist.
- Hidden sites get **no marker**. Unbeaten trainers and the Area challenge keep their usual idle cue.

**In the menu, the Region map** (one per region; interiors get no panel). A panel per Area shows:
- stage pips (●●○)
- **only the next stage's** Mendings with K/M, plus "1 more stage after this"
- native species as silhouettes until Seen, then named
- hidden sites as "Hidden site — ?" with no location
- the Area challenge with its recommended level
- for a Blighted Area, what restores it ("Restored when Boss X is beaten"); Mendings done early show as "✓ — counts once restored"
- in the header, a **region-wide Restoration %** (per region)
- Bosses: every **reachable** unbeaten Boss shows its theme Type icon and ace level ("Grove · Lv 22"); Bosses in Locked Areas show as "?"; a beaten Boss's **crest** lights up (cosmetic only).

**The stage-change sequence:**
- If it triggers **while the player is in the Area**, it plays as soon as the current battle or dialogue ends: the camera pans to the focal point, tiles swap outward in rings over about **3 seconds** with a chime, then a banner ("<Area> — Restored: Stage 2") and a card listing what changed (new Creatures nearby, a path opened, new shop stock).
- **Skippable** with a tap; **instant** with battle animations off.
- If it triggers **elsewhere**, it's queued and plays on the next entry to that Area.
- **Several stages at once** (stage 1 landing with enough saved Mendings for stage 2) play as **one sequence** with one combined card.
- **Autosave** right after.
- On entering an Area already at stage S, the shell applies stages 1…S at once (§6).

### Restoration data and save
*Source: [How does Restoration change an Area?](issues/12-restoration.md)*
*Source: [What exactly does an Area's `.tmj` contain?](issues/23-area-map-format.md)*

- **Area JSON:** `native_species[]` and `stages[]`. Each stage has:
  - a trigger: `story_flag` (stage 1) or `mendings_required: K` (stages 2+)
  - `mendings[]`
  - a spawn-table reference
  - shop additions, the weather table and music
  - an optional payoff Creature
- **In the Area's `.tmj`** (§6): the per-stage tile change sets (which also add or remove Habitat patches and open paths), the one `focal_point` marker, Blight barriers, and markers that switch on or off by stage (NPCs, Forage spots, item spots). Weather, music, spawn tables, native species and shop stock stay in the Area JSON, never on the map.
- **The save stores raw facts:** species registered per Area, trainers beaten, sites found, story flags. It also stores **the highest stage reached per Area** and a **pending-presentation queue** per Area. The current stage itself is derived (§6).
- **On load**, an Area's stage is the **higher** of its stored stage and the stage computed from the facts, so a content patch that changes requirements can never move an Area backwards.

### Chapters and gating
*Source: [How do the Bosses and Area gating sequence the region?](issues/15-bosses-and-gating.md)*
*Source: [Boss order comes from reachability, not a list](../../docs/adr/0003-boss-order-comes-from-reachability.md)*

- **5 Chapters** of **1 / 2 / 3 / 1 / 1** Bosses (a string of pearls):
  - Chapter 1: Boss 1.
  - Chapter 2: Bosses 2 and 3, in either order.
  - Chapter 3: Bosses 4, 5 and 6, in any order.
  - Chapter 4: Boss 7.
  - Chapter 5: Boss 8, the finale. The credits roll after it.
- **The next Chapter opens only when every Boss in the current one is beaten.**
- Bosses in the same Chapter share one level. Whichever the player takes later feels a little easier; the catch-up XP (§2) keeps that gap small. **No level scaling.**
- **The only critical-path gate is a Blight barrier** (brambles, a dried ford, a rockfall), cleared by an Area's **stage-1** bundle. No NPC roadblocks, badge checks or field moves.
- **Area states:** every Area is **Locked** (not reachable yet), **Blighted** (reachable, stage 0) or **Restored 1+**. Players walk into the next Chapter's Areas while they are still Blighted, catch and train there, and restore them by beating that Chapter's Bosses.
- **"Beat every Boss in the Chapter" gates:** a stage-1 trigger stays a single flag. After each Boss win, an event checks the others and sets a combined flag, e.g. `if_flag boss_2 and boss_3 → set_flag chapter_3_open`, with a short story beat. Chapter 4's gate needs all three Chapter-3 flags the same way. Gates and story beats are events from the closed command list (§6).
- **Reachability is the order (ADR 0003).** There is **no progression record and no Boss-order list.** Which Bosses are on offer follows only from which Areas are reachable, and reachability comes from the stage-1 flags that clear Blight barriers. "Chapter" is a design convention the linter checks, never a field the game reads; a different shape means changing barriers and events, not a list.
- **Progress-keyed things use the Bosses-beaten count**, never which Bosses (shop stock, the level cap), so any order the map allows works.

### Bosses
*Source: [How do the Bosses and Area gating sequence the region?](issues/15-bosses-and-gating.md)*
*Source: [How is the region laid out?](issues/18-region-layout.md)*
*Source: [How is the move list structured?](issues/21-move-list.md)*

| Boss | Chapter | Theme Type | Home landmark | Ace level | Team | AI tier | Care-item uses | Format |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | Wild | `warren` | 12 | 2 | Trainer | 1 | 1v1 |
| 2 | 2 | Grove | `elder_tree` | 22 | 3 | Boss | 1 | 1v1 |
| 3 | 2 | Tide | `tide_shrine` | 22 | 3 | Boss | 1 | 1v1 |
| 4 | 3 | Stone | `quarry` | 34 | 4 | Boss | 2 | 1v1 |
| 5 | 3 | Volt | `storm_tower` | 34 | 4 | Boss | 2 | **2v2** |
| 6 | 3 | Frost | `glacier` | 34 | 4 | Boss | 2 | 1v1 |
| 7 | 4 | Lumen | `lighthouse` | 44 | 5 | Boss | 2 | 1v1 |
| 8 | 5 | mixed | `source` | 52 | 6 | Boss | 3 | 1v1 |

- **Ace level** is the highest level on the team; the others sit 1–3 levels below.
- **Type identity:** most of each team shares the Boss's theme Type. **From Chapter 3 on**, each team adds **one off-type "coverage" Creature**, so a single counter-pick can't sweep it and switching pays. Boss 8 has a mixed team.
- **Unthemed Types: Flame, Gale, Shade.** They are left for Area challenges, the rival and the antagonist faction (Shade-led; §1).
- **Boss 5** is a pair of Trainers sharing **one Boss record**: one flag, one prize, one +1 to Bosses beaten. Its Volt kit is the `empower_ally` move plus a self-or-ally `energy` move, built from data, not special code (§2).
- Each landmark is shaped by its Boss's Type. Boss names and story beats are in §1.
- The player's **whole Party of 6** is always allowed, whatever the Boss's team size.
- **Losing to a Boss** follows the normal defeat rule (money loss, immediate retry; §2). Each landmark has a camp at its entrance, so the retry is a few steps away.
- **Beating a Boss gives:** its flag (`boss_1` … `boss_8`: Restoration stage 1 and the opened routes); the Marks prize (**100 × the ace level**); **+1 to Bosses beaten** (drives shop stock and the challenge-mode cap); a crest on the Region map. **Nothing else:** no badges with stat effects, no move-teaching items, no gift Creature. Prizes come from the formulas, never hand-set.
- **Boss records** (JSON, permanent IDs): team and format; AI tier and Care-item uses; its flag; its home Area; `rematch_team`; optional `challenge_team`.

### Level curve
*Source: [How do the Bosses and Area gating sequence the region?](issues/15-bosses-and-gating.md)*
*Source: [How is the region laid out?](issues/18-region-layout.md)*

With **L** the current Chapter's ace level and **P** the previous Chapter's (P = 5 for Chapter 1, the starter level, which stays 5):

| Chapter | Ace level L | Expected party level | Wild levels (P − 1 to L − 4) | Trainers | Area challenges | Play time to reach (cumulative) |
|---|---|---|---|---|---|---|
| 1 | 12 | 10 | 4–8 | ≤ 10 | 14 | ~1.5 h |
| 2 | 22 | 20 | 11–18 | ≤ 20 | 24 | ~5 h |
| 3 | 34 | 32 | 21–30 | ≤ 32 | 36 | ~12 h |
| 4 | 44 | 42 | 33–40 | ≤ 42 | 46 | ~16 h |
| 5 | 52 | 50 | 43–48 | ≤ 50 | 54 | ~19 h |

- **Expected party level = L − 2**: what a player reaches by fighting only what's on the way, with no grinding. The XP constants (§2) are tuned to it, and the simulation gates use it.
- Later Restoration stages may add **+1–2 at the top** of an Area's wild band. **Payoff Creatures** sit at L.
- The strongest trainers stand nearest the Boss. Area challenges are optional and deliberately above the Boss.
- **Each Area's Chapter is derived by the linter:** an Area belongs to the Chapter in which it first becomes reachable on the walk from the new-game state. Connector routes therefore take the new Chapter's band (`route_3` is Chapter 2, wild levels 11–18). Spawn tables, trainers and Area challenges are checked against that band, with the +1–2 allowance. **The Chapter is never written on the Area.**
- Rival and faction team levels are in §1; they fit these trainer ceilings.

### Boss 1 is beatable with every starter
*Source: [How do the Bosses and Area gating sequence the region?](issues/15-bosses-and-gating.md)*

A **test, not a Type restriction**, so the Starter trios stay free (§3):
- A headless scenario on the seeded core runs, for **every starter in every trio**, a bot party: the starter plus the **two most Common species from the Areas before Boss 1**, all at the expected level (**10**).
- The bot must win **at least 70% of 200 seeded runs**, or the content tests fail. It runs in CI (§6).
- Boss 1 runs on **Trainer-tier AI** with 2 Creatures.
- The same harness can later run every Boss against an "expected party" as a balance report.

### Postgame rematches
*Source: [How do the Bosses and Area gating sequence the region?](issues/15-bosses-and-gating.md)*

- Each Boss has **one rematch team** (`rematch_team`): a full 6 with Boss-tier AI, keeping the theme with two coverage picks.
- **Fixed levels:** **58** (Bosses 1–3), **61** (Bosses 4–6), **63** (Boss 7), **66** (Boss 8).
- Fought at the Boss's own landmark, **once per in-game day**, shown by an idle cue when ready.
- **Prize: 50 × the highest level** (about 3,000 Marks), a token amount because money already piles up late. The rival's postgame friendly battle uses the same prize formula (§1).
- **No rematch ladders in v1.** A second rematch set can come with the Large scale.
- **Open:** how the save records when each rematch was last fought (the "once per in-game day" fact) isn't specified.

### Challenge mode (data only in v1)
*Source: [How do the Bosses and Area gating sequence the region?](issues/15-bosses-and-gating.md)*

- **Level-cap table keyed to the number of Bosses beaten.** Rule: cap = the ace level of the lowest Chapter with a Boss still unbeaten.

  | Bosses beaten | 0 | 1–2 | 3–5 | 6 | 7 | 8 |
  |---|---|---|---|---|---|---|
  | Cap | 12 | 22 | 34 | 44 | 52 | 100 |

- In challenge mode, **XP stops at the cap**. A Creature over the cap can't occur, because the linter checks that no reachable wild Creature or gift is above it.
- Each Boss record has an optional **`challenge_team`**. When it's absent, the normal team runs with the AI one tier up (§2).
- **v1 ships the table and fields filled in, with no menu option.**

### Region record
*Source: [How do the Bosses and Area gating sequence the region?](issues/15-bosses-and-gating.md)*
*Source: [How is the region laid out?](issues/18-region-layout.md)*
*Source: [Boss order comes from reachability, not a list](../../docs/adr/0003-boss-order-comes-from-reachability.md)*

- The region record holds its **Boss list** (for the Bosses-beaten count and the Region map) and the **level-cap table**, and the **unordered set of its Areas** (for the per-region Region map, Restoration % and the dormant-exit check). It holds no order list.
- A second region is content only: Areas, barriers, Bosses and events.

### Region shape
*Source: [How is the region laid out?](issues/18-region-layout.md)*
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

- **A hub per Chapter.** Each Chapter has one **hub town**. One **spoke** leads from it to each of that Chapter's Bosses: a chain of 1–3 Areas ending at the Boss's **landmark**.
- A **connector route** leads on from the hub to the next Chapter's hub, and a **Blight barrier** blocks it.
- Chapters 4 and 5 are each one spoke off their own hub. The home town sits before Chapter 1's single path, and is Chapter 1's hub.
- **Spokes can't reach each other on the critical path**, so "each Boss in a Chapter is reachable without the others" holds by construction. Stages 2+ add optional shortcuts so the region doesn't feel like a tree (see Optional content).
- The Region map reads **bottom to top** in portrait: home in the southern vale, the finale at its northern heart. The region's display name is **Mendvale** (§1).
- **Room for a second region:** Area IDs are **flat and globally unique**, with no region prefix; a region record lists its Areas; `harbour` has the one **dormant exit** (a ferry, visible but "not running yet"); a second region adds its Areas and wakes that exit with an event, moving nothing. The Region map and Restoration % are per region.
- **Open:** exits between Areas beyond the spoke and connector chains (for example where `route_3` leaves Chapter 1) aren't listed; drawing each Area's map is implementation work.

### Area kinds
*Source: [How is the region laid out?](issues/18-region-layout.md)*

The Area record has a closed `kind` field:

| Kind | What it is | Screens (≈ 11 × 12 tiles each) | Stages |
|---|---|---|---|
| `town` | shop, inn and houses | 1–2 | 1–2 (`home_town` has 0) |
| `route` | outdoor ground between places | 3–5 | 3 |
| `dungeon` | cave, deep forest or ruin; its 1–3 floors are sections of **one `.tmj`** joined by internal warps, with one Restoration track | 4–8 | 3 |
| `landmark` | the small site where a Boss (or a one-off) waits, shaped by its Type | 1–2 | 2 |
| `interior` | a house, shop or inn: 0 stages, a `parent` Area, no Region-map panel, the parent's music | < 1 | 0 |

- **Hard cap: 64 × 64 tiles per `.tmj`**, checked by the linter. Longer stretches split into two Areas.
- **Towns** have 1–2 stages. Stage 1 comes from a flag (see Flags and Blight barriers). Stage 2, where present, comes from town-style Mendings: local trainers or a hidden site. Towns have no Habitat patches and no native species.
- Interiors are named after their parent ("Lowfold Inn").

### Habitat kinds
*Source: [How is the region laid out?](issues/18-region-layout.md)*

**8 kinds**, a global list that a later region may extend:

| Kind | Terrain |
|---|---|
| Meadow | grass, fields |
| Woodland | forest |
| Wetland | rivers, ponds, marsh |
| Coast | beach, shallow sea |
| Cavern | caves, mines |
| Crag | rocky hills, badlands |
| Snowfield | alpine, ice |
| Ruins | old structures, overgrown towns, shrines |

- Each kind has one **Habitat Lure**, so there are 8 (see Items). Each species' home Habitat is one of these (§3).
- Habitat patches are logic tiles on the map, and wild Creatures never leave their patch (§6).
- Time of day and weather stay separate spawn conditions.

### The 33 Areas
*Source: [How is the region laid out?](issues/18-region-layout.md)*
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

**33 Areas plus interiors: 7 towns, 12 routes, 6 dungeons, 8 landmarks** — about 35 minutes of critical path per Area against the ~19 h total. IDs are permanent; display names are strings (§1).

| Ch | Area ID | Display name | Kind | Habitat kinds | Screens | Stages |
|---|---|---|---|---|---|---|
| 1 | `home_town` | Lowfold | town | – | 2 | 0 |
| 1 | `route_1` | Wellside Lane | route | Meadow | 3 | 3 |
| 1 | `route_2` | Reedwood Trail | route | Woodland, Wetland | 4 | 3 |
| 1 | `warren` (Boss 1, Wild) | Burrow Hill | landmark | Meadow | 2 | 2 |
| 2 | `route_3` (connector) | Dryford Road | route | Meadow, Wetland | 4 | 3 |
| 2 | `hub_2` | Millbrook | town | – | 2 | 2 |
| 2 | `route_4` | Mossway | route | Woodland | 4 | 3 |
| 2 | `deepwood` | The Deepwood | dungeon | Woodland | 6 | 3 |
| 2 | `elder_tree` (Boss 2, Grove) | The Elder Tree | landmark | Woodland | 2 | 2 |
| 2 | `route_5` | Saltmarsh Path | route | Wetland, Coast | 4 | 3 |
| 2 | `cove_town` | Gullcove | town | – | 1 | 2 |
| 2 | `tide_shrine` (Boss 3, Tide) | Tide Shrine | landmark | Coast | 2 | 2 |
| 3 | `route_6` (connector) | Ridgeback Road | route | Meadow, Crag | 5 | 3 |
| 3 | `hub_3` | Threeways | town | – | 2 | 2 |
| 3 | `route_7` | Shale Trail | route | Crag | 4 | 3 |
| 3 | `old_mine` | Tinmouth Mine | dungeon | Cavern | 7 | 3 |
| 3 | `quarry` (Boss 4, Stone) | Greystone Quarry | landmark | Crag | 2 | 2 |
| 3 | `route_8` | Old Works Road | route | Meadow, Ruins | 4 | 3 |
| 3 | `sunken_works` | The Sunken Works | dungeon | Ruins | 6 | 3 |
| 3 | `storm_tower` (Boss 5, Volt, 2v2) | Storm Tower | landmark | Ruins | 2 | 2 |
| 3 | `route_9` | Highpass Trail | route | Crag, Snowfield | 5 | 3 |
| 3 | `peak_village` | Cloudrest | town | – | 1 | 2 |
| 3 | `ice_cave` | Rimefall Cave | dungeon | Cavern, Snowfield | 5 | 3 |
| 3 | `glacier` (Boss 6, Frost) | Frostcrown Glacier | landmark | Snowfield | 2 | 2 |
| 4 | `route_10` (connector) | Seawind Road | route | Coast, Meadow | 5 | 3 |
| 4 | `harbour` (hub 4) | Saltharbour | town | – | 2 | 2 |
| 4 | `route_11` | Cliffside Path | route | Coast, Crag | 4 | 3 |
| 4 | `observatory` | Starwatch | dungeon | Ruins | 6 | 3 |
| 4 | `lighthouse` (Boss 7, Lumen) | Lastlight | landmark | Coast | 2 | 2 |
| 5 | `route_12` (connector) | Coldstep Road | route | Crag, Snowfield | 5 | 3 |
| 5 | `outpost` (hub 5) | Highwatch | town | – | 1 | 2 |
| 5 | `blight_heart` | The Hushed Halls | dungeon | Ruins, Cavern | 8 | 3 |
| 5 | `source` (Boss 8, finale) | The Wellspring | landmark | Ruins | 2 | 2 |

The Ch column is what the linter derives (see Level curve); it is never stored on the Area.

- **Spokes:**
  - Chapter 1: `route_2` → `warren`.
  - Chapter 2: `route_4` → `deepwood` → `elder_tree`; `route_5` → `cove_town` → `tide_shrine`.
  - Chapter 3: `route_7` → `old_mine` → `quarry`; `route_8` → `sunken_works` → `storm_tower`; `route_9` → `peak_village` → `ice_cave` → `glacier`.
  - Chapter 4: `route_11` → `observatory` → `lighthouse`.
  - Chapter 5: `blight_heart` → `source`.
- **Spoke towns:** `cove_town` and `peak_village` give long spokes a shop.
- **Habitat coverage:** every Habitat kind is reachable by Chapter 3. Chapters 2–3 hold 11 routes and dungeons with Habitat patches, which at 2 wild starters per Area is room for 22 against the 12 needed (§3). Chapter 1 offers Meadow, Woodland and Wetland for its 7 lines.
- Species placement rules that touch Areas (Chapter 1's two most Common species, wild starters, lines by debut Chapter, the counter rule) are in §3.

### Flags and Blight barriers
*Source: [How is the region laid out?](issues/18-region-layout.md)*
*Source: [How do the Bosses and Area gating sequence the region?](issues/15-bosses-and-gating.md)*
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

- **`starter_chosen`** restores `route_1` and clears its barrier at the home town's edge. It's the first Restoration the player sees, so it doubles as the tutorial.
- **A Boss flag** restores **its whole spoke**: the landmark plus every Area between it and the hub (at most 4), spoke towns included.
- **`chapter_N_open`** restores **the hub being left and the connector route out of it**, clearing that connector's barrier. Each hub is lived in Blighted and heals as its Chapter closes.
- **`boss_8`** restores its spoke plus `outpost`.
- There are exactly **5 critical-path barriers**: on `route_1`, `route_3`, `route_6`, `route_10` and `route_12`. Spokes have none. A barrier blocks its cells while its Area is below stage 1 and clears at stage 1 (marker format in §6).

| Flag | Set by | Restores to stage 1 | Barrier cleared |
|---|---|---|---|
| `starter_chosen` | the starter pick | `route_1` | `route_1` |
| `boss_1` | Boss 1 win | `route_2`, `warren` | – |
| `chapter_2_open` | the `boss_1` win event | `route_3` only (`home_town` has 0 stages) | `route_3` |
| `boss_2` | Boss 2 win | `route_4`, `deepwood`, `elder_tree` | – |
| `boss_3` | Boss 3 win | `route_5`, `cove_town`, `tide_shrine` | – |
| `chapter_3_open` | combined event once `boss_2` and `boss_3` are set | `hub_2`, `route_6` | `route_6` |
| `boss_4` | Boss 4 win | `route_7`, `old_mine`, `quarry` | – |
| `boss_5` | Boss 5 win | `route_8`, `sunken_works`, `storm_tower` | – |
| `boss_6` | Boss 6 win | `route_9`, `peak_village`, `ice_cave`, `glacier` | – |
| `chapter_4_open` | combined event once `boss_4`, `boss_5` and `boss_6` are set | `hub_3`, `route_10` | `route_10` |
| `boss_7` | Boss 7 win | `route_11`, `observatory`, `lighthouse` | – |
| `chapter_5_open` | the `boss_7` win event | `harbour`, `route_12` | `route_12` |
| `boss_8` | Boss 8 win (finale) | `blight_heart`, `source`, `outpost` | – |

- A combined flag's beat plays right after the Boss win that completes it, at that landmark; the hub's Restoration then plays the next time the player enters it (the pending-presentation queue). The story beat behind each flag is in §1.

### Furniture
*Source: [How is the region laid out?](issues/18-region-layout.md)*
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

- **Rest points** (heal, revive and skip the clock for free, §2; staffed by the **Lantern-keeper**, one NPC record used at every inn and camp):
  - **every town:** an inn interior holding the Rest point
  - **every dungeon:** a camp at its entrance, plus one deeper in if it has 3 floor sections
  - **every landmark:** a camp at its entrance, so a lost Boss fight retries a few steps away
  - **routes of 4+ screens:** a mid-route camp
  - camps work while Blighted (a lantern, a tent)
  - linter: **no critical-path cell is more than one Area exit from a Rest point**
- **Interiors per town:** an inn, a shop and 1–3 houses.
- **Shops:** one per town, so **7** in all. Camps sell nothing.
- **Focal points:** exactly one in every Area with stages (towns included); none in `home_town` or interiors.
- **0-stage Areas:** `home_town` and every interior.

### Landmarks and the rare one-offs
*Source: [How is the region laid out?](issues/18-region-layout.md)*
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

- **Landmarks have 2 stages.** Stage 1 comes from the Boss flag. Stage 2 comes from Mendings: a small Habitat patch with 3 native species, and a hidden site.
- A Boss's **rematch** is fought at its landmark.
- **The 2 rare one-offs** sit at final-stage focal points; neither is Shade or Lumen (their story reasons are in §1):
  - the Chapter 4 one at `observatory` (stage 3, Ruins)
  - the postgame one at `source` (stage 2, after the finale)

### Optional content
*Source: [How is the region laid out?](issues/18-region-layout.md)*
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

- **Area challenges:** one in **every route and dungeon** (**18** in all), none in towns or landmarks. Each sits at its Chapter's challenge level (**14 / 24 / 36 / 46 / 54**).
- **Hidden sites:** **1–2 per route, town and landmark; 2–3 per dungeon.**
- **Optional paths (stages 2+ only):**
  - every spoke gets **one stage-2 shortcut** back to its hub, or between neighbouring spokes in Chapter 3
  - every dungeon gets **one stage-2+ side pocket** holding a hidden site or an item spot
- **Trainers:** about **3–5 per route and dungeon**, **1–2 per town**. They make up each Area's "beat the trainers here" Mending. Faction trainers are ordinary trainer records and count toward it; in Chapter 5 they fill `blight_heart`'s 3–5 trainers (§1).

### Money and income
*Source: [What items exist, and how does the economy work?](issues/14-items-and-economy.md)*
*Source: [How do the Bosses and Area gating sequence the region?](issues/15-bosses-and-gating.md)*

- **One currency.** Code and data call it `money`; it displays as **Marks** (a string, so a rename is one edit). No second tokens, crafting materials or premium currency. **Display cap 9,999,999.**
- **Income is one-off:**

  | Source | Prize |
  |---|---|
  | Trainer | class base (16 for a casual trainer, up to 48 for a veteran) × the highest level on their team |
  | Area challenge | 60 × level |
  | Boss | 100 × its highest (ace) level |
  | Boss rematch (postgame, daily) | 50 × the highest level |
  | Visible item spot | the item, taken once; **there are no invisible items** |
  | Selling | 50% of the buy price; Key items can't be sold; Forage has its own low sell price |

- **Wild battles pay no money**, so battling wild Creatures over and over is never a money strategy.
- **Hidden sites give no money or items.** Their reward is the Mending plus Collection log or story flavour.
- **The only money sink in v1** is the defeat loss: 8 × the Party's highest level × (Bosses beaten + 1), capped at 50% of money carried (§2). Late-game money piling up is accepted; money sinks are out of scope.

### Forage and the Lure safety net
*Source: [What items exist, and how does the economy work?](issues/14-items-and-economy.md)*
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

- **Forage spots** are map markers with an ID and a small item table filtered by Habitat and time of day (marker format in §6). Each shows as a plant sprite that looks empty once picked.
- A spot **regrows one in-game day** (~24 min of play) after picking. Its yield is rolled from the seeded `Rng`.
- **Yields are Care items:** a small heal herb, a cure berry for one Status, and occasionally a rare Energy fruit. They sell for about **20–40 Marks**.
- **Restoration adds Forage spots:** a Blighted Area has few or none, and stages 2+ add more (part of each stage's Habitat-patch changes).
- **Lure safety net:** resting at any Rest point while holding **zero Lures of any kind** gives **3 basic Lures**. No cooldown, since it only fires at zero. The Lantern-keeper there gives them, with the display line *"Hollis asked us to keep a few spare for you."*

### Items
*Source: [What items exist, and how does the economy work?](issues/14-items-and-economy.md)*
*Source: [How is the region laid out?](issues/18-region-layout.md)*

- Each item is a JSON record with a permanent ID (file layout and icon convention in §6). Its effect is built from a **closed list of effect kinds** in code: `heal_hp`, `cure_status`, `revive`, `restore_energy`, `lure`, `key`. New items are data only.
- Lures display as "<X> Offering" (§1); data keeps the generic `lure` kind.

| Item | Price | Effect | Use |
|---|---|---|---|
| Basic Lure | 200 | catch ×1 | battle |
| Better Lure | 600 | catch ×1.5; in shops after 2 Bosses | battle |
| Best Lure | 1,200 | catch ×2; in shops after 5 Bosses | battle |
| Habitat Lure (one per Habitat kind, 8) | 1,000 | catch ×2.5 if the target's Habitat matches, ×1 otherwise | battle |
| Small / medium / full heal | 150 / 450 / 1,000 | 30% / 60% / 100% of max HP | anywhere |
| Single-Status cure (one per Status) | 150 | clears that Status | anywhere |
| All-cure | 500 | clears any Status | anywhere |
| Revive | 1,200 | revives at 50% HP | anywhere |
| Energy tonic | 400 | +50% of max Energy | battle |
| Forage items | n/a (20–40 sell) | Care effects as above | anywhere |
| Key items | n/a | story and progression; never consumed or sold | through the world |

- **Heals are percentages**, so they never go stale as levels rise.
- **No guaranteed catch.** The 1–95% catch clamp (§3) holds for every Lure; rare one-off Creatures keep their low base rate.
- **Deliberately absent from v1:** held items (Traits fill the passive slot), stat-stage boosters, move-teaching items, evolution items, repels, escape items, and anything affecting Bond rank, Leanings or Traits.

### Shops and bag
*Source: [What items exist, and how does the economy work?](issues/14-items-and-economy.md)*
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*

- **One shop per town.** Camps and route Rest points sell nothing; no wandering vendors in v1.
- **Stock** = a base list + **global additions by number of Bosses beaten** (better Lure tiers, stronger heals) + **local additions by that Area's Restoration stage** (Habitat Lures from stage 2, local Forage goods). Stock is data on the town record; a shop in an interior uses its `parent`'s.
- **The same prices everywhere.**
- **Bag:** **no capacity limit**, **99 per stack**. At 99 a pickup is refused and the spot stays full, and buying stops at 99.
- **Three pockets:** Care, Lures, Key.
- **Use:** Care items are usable from the bag outside battle. Lures only work in battle. Key items are used through interaction or the story, never from a menu "use" button. Using an item in battle takes the Creature's turn (§2).
- **Starting kit** (given by the mentor at `starter_chosen`, §1): **1,000 Marks, 5 basic Lures, 3 small heals.**

### Trainers' items
*Source: [What items exist, and how does the economy work?](issues/14-items-and-economy.md)*

- Trainers and Bosses use **Care items only** (never Lures or Energy tonics), from a per-battle list in their data, separate from the player's bag. Use counts are set per trainer or Boss (Boss counts in the Bosses table).
- **One shared rule for every AI tier:** heal a Creature below **30% HP** if its expected damage this turn won't KO the foe.
- Every use is **announced** in battle text.

### Economy data and save
*Source: [What items exist, and how does the economy work?](issues/14-items-and-economy.md)*

- **The save stores only:** the **bag** (item ID → count), **money**, item spots taken, and each Forage spot's last-picked in-game day. Forage regrowth and shop stock are derived (stock from Bosses beaten and Restoration stages).
- **Balance check:** critical-path income up to each Boss (trainers, challenges and item spots on the way) must cover a target shopping list for that point. It runs on the same Area-graph walk as the gating checks.
- **Open:** the contents of each Boss's target shopping list aren't specified.

### World linter checks
*Source: [How does Restoration change an Area?](issues/12-restoration.md)*
*Source: [How do the Bosses and Area gating sequence the region?](issues/15-bosses-and-gating.md)*
*Source: [How is the region laid out?](issues/18-region-layout.md)*
*Source: [What items exist, and how does the economy work?](issues/14-items-and-economy.md)*

All run in the content linter, the build gate (§6). The gating checks walk the Area graph from the new-game state, following flags. The map-level versions (flood-fill against the baked grid, barriers clear only at stage 1) are in §6.

**Restoration:**
1. Every Mending for stage N is completable while the Area is at stage N−1.
2. Only stage 1 opens critical-path routes.

**Gating and Bosses:**
1. Every barrier's flag is set somewhere reachable before the barrier.
2. Each Boss becomes reachable, and **each Boss in a Chapter can be reached without beating the others** in it.
3. Every Area with stages gets its stage 1 from a reachable flag, **the finale's own `boss_8` flag included** (it restores `blight_heart`, `source` and `outpost`), so 100% region Restoration is always possible in the postgame.
4. **At least 2 catchable species with a 2× edge over each Boss's theme Type** are reachable before that Boss.
5. Wild, trainer and Area-challenge levels fit the bands of each Area's derived Chapter, with the +1–2 allowance for later stages.
6. No reachable wild Creature or gift is above the challenge-mode cap for the Bosses-beaten count at that point.
7. The Boss 1 simulation gate passes for every starter in every trio.

**Region layout:**
1. `kind` is one of the 5 kinds. Interiors have 0 stages and a `parent`. Only `home_town` and interiors have 0 stages.
2. No `.tmj` is over 64 × 64 tiles.
3. Areas with Habitat patches list 3–6 native species (Common or Uncommon only); Areas without patches list none.
4. Every Habitat patch and every species' home Habitat uses one of the 8 kinds.
5. No critical-path cell is more than one Area exit from a Rest point.
6. Level bands come from each Area's derived Chapter.
7. Exactly one dormant exit per region.

**Economy:**
1. Critical-path income up to each Boss covers that point's target shopping list.

## 5. Look and feel: art, controls and screens

Reference prototypes (mock-ups to react to, not specs; where they differ from this section, this section wins):
- **Art direction:** [`prototypes/art-direction/`](../../prototypes/art-direction/) (artifact https://claude.ai/artifact/BF3KpShuSLG8qRX7wtW2m8). Its asset licences are in [`LICENCES.md`](../../prototypes/art-direction/LICENCES.md).
- **Controls and screens:** [`prototypes/controls/`](../../prototypes/controls/) (artifact https://claude.ai/artifact/X4zuWpD2Ddb7Y7J1cXPpc2).
- Survey behind the art-source rules: branch `research/art-sources`, file `research/art-sources.md`.

### 5.1 Art sources and licences
*Source: [Where can original or licensable pixel art come from, and at what cost?](issues/02-art-sources.md)*
*Source: [How is the Creature roster structured?](issues/16-roster-structure.md)*
*Source: [What is the technical architecture?](issues/09-technical-architecture.md)*

#### Licence rules
- **Allowed:** **CC0**, **OGA-BY**, and **paid or commissioned licences that grant commercial app-store rights**. **SIL OFL is allowed for fonts only**: unmodified, with the licence text on an in-game Credits screen.
- **CC-BY:** usable only with **written permission from the artist**. CC-BY, CC-BY-SA and GPL conflict with the iOS App Store's terms (anti-DRM clauses).
- **Paid assets never go in a public repo.** The repo is public (see §6).
- **Commission contracts** must explicitly grant app-store rights.
- **AI art:** neither store bans AI art bundled with the game (Apple requires only owned or licensed content). Art made from prompts alone isn't copyrightable. Use AI **for ideas, or as a base that gets substantially redrawn**, never as final art.

#### Never use
Pokémon IP and ripped assets are out of scope in any form. Specifically avoid:

| Source | Why (where known) |
|---|---|
| The Spriters Resource | — |
| PokéAPI sprites | labelled CC0, but the licence file says "Copyright The Pokémon Company" |
| Pokémon Essentials | DMCA'd in 2018 |
| "Pokemon DS Style" tileset, and other "Pokémon-like" or "fakemon" packs on itch.io | — |
| Tuxemon art | CC-BY-SA, some of unclear origin |
| LPC art | except the Sharm and Redshrike pieces that are also OGA-BY |

- **Verify before use** (terms not confirmed): OpenAI and Midjourney terms (seen only in search snippets), Retro Diffusion's terms (not found), and two effects/icon packs seen only in an itch.io CC0 listing.

#### Chosen packs and tools
| Use | Source | Licence | Notes |
|---|---|---|---|
| World tiles, characters, UI, effects | **Ninja Adventure** | CC0 | 16×16, one consistent style; also the master palette (§5.2) |
| Placeholder Creature battle sprites | ***50+ Monsters Pack 2D*** | CC0 | 56 monsters, 64×64, front and back; the only CC0 front/back battle set found |
| Dialogue and menu font | **Public Pixel** | CC0 | 8×8, covers 98 languages |
| Dense battle-label font | **Tiny5** | OFL | allowed for fonts (see Allowed above) |
| Final Creatures | **self-drawn** in **LibreSprite** or **Pixelorama** | own work | both free; Aseprite costs $19.99 |

- **No free source covers ~100 Creatures in one style**, so final Creatures are self-drawn unless the budget changes. Commissions run about **$30–$60 per 64×64 sprite**, so 100 Creatures with front and back sprites would cost roughly **$6k–$12k** before animation.
- **Open:** Creature art production: who draws, and the per-sprite workflow and review. (What each species needs is in §5.2; the drawing order is in §3.)

#### Placeholder policy
- A **dev-only mapping** gives every species a placeholder: one of the 56 *50+ Monsters Pack 2D* sprites, or a **generated silhouette in the palette** (shape from its Stat archetype, colour from its Type).
- A missing sprite falls back to a built-in placeholder and is a lint **warning**, not an error. A final replaces its placeholder by **dropping files at the conventional paths**, with no data change (paths in §5.2; mechanism in §6).
- **Internal and closed-testing exports** may use placeholder Creature sprites. A **production** export **fails if any reachable species still uses a placeholder** (Build channels: see §6).

#### Licence ledger
- **File:** `assets/LICENCES.csv`, one row per asset file.
- **Columns:** `source`, `licence`, `author`, `URL`, plus `placeholder` (marks placeholder art; drives the production gate).
- **Bake and lint checks:** every asset file has a ledger row; every sprite uses only the locked palette and is the right size (64×64 battle, 16×16 map). Details of the gate: §6.
- Fonts (Public Pixel, Tiny5) get rows too.
- **Open:** filling the ledger.

### 5.2 Art direction
*Source: [What should Project Wildling's pixel art look like?](issues/10-art-direction.md)*
*Source: [How is the Creature roster structured?](issues/16-roster-structure.md)*
*Source: [What is the technical architecture?](issues/09-technical-architecture.md)*

#### Render resolution and scaling
- **180 pixels wide internally**, scaled up by **whole numbers only**: **×4** on 720p Android, **×6** on 1080p and iPhone.
- **Height extends to fill the screen**, with no black bars. In Godot: viewport stretch, aspect expand, integer scale.
- The map shows **about 11 × 12 tiles** above the control deck (§5.4). Camera zones smaller than the screen are centred with black around them (see §6, Area map format).

#### Sizes and frames
| Asset | Size | Frames | Notes |
|---|---|---|---|
| Tile | **16×16** | — | Ninja Adventure tiles; files `assets/tiles/<sheet>.png` (§6) |
| Player character | **16×16** | **4-frame walk × 4 directions** | |
| Creature map sprite | **16×16** | **2 walk frames × 4 directions** | `assets/creatures/<id>/map.png`; used for wild Creatures and the following lead Creature |
| Creature battle sprite | **64×64**, front and back | **1 still frame each** | `assets/creatures/<id>/front.png`, `back.png`; **never scaled up** |
| Item icon | — | — | `assets/items/<id>.png` |

- **Battle animations are code effects on still sprites:** an **idle bob**, a **lunge** when attacking, a **flash** when hit, a **fade** when fainting. The battle scene plays core events as text, bar animations and these effects, and skips the visuals when battle animations are off (§5.6).
- **Drawn idle animations** can be added per species later **without code changes**.
- **Open:** sizes for item icons, NPC and Trainer art, Type icons and UI panels are not specified.

#### Palette
- **Ninja Adventure's 53 colours are locked as the master palette.** New colours are added only deliberately.
- Self-drawn Creatures are drawn **within the palette**; the bake rejects sprites with colours outside it.
- Creature design rules that use the palette (a clear silhouette with **2 key colours at 16×16**; night species use the **cool half** of the palette and have larger eyes): see §3.

#### Fonts and text
- **Public Pixel** (CC0) for dialogue and menus.
- **Tiny5** (OFL) for dense battle labels.
- **No text smaller than 8 internal pixels** (about 2.3 mm at ×4).
- Only the movement scheme and Run defaults are stated in tickets. The other defaults follow from how each setting is described (a toggle that "turns off" or "skips" something defaults to on, or to the preview), and are **Open** to confirm in the settings ticket.
- **No UI-scale setting in v1.**
- **Open:** a large-text mode.
- **Open:** localisation (only English ships in v1; Public Pixel covers 98 languages; strings: see §6).

#### How Restoration and Blight look
- **Restoration is shown as tile swaps** at each Restoration stage, **spreading out from the Area's Focal point** (a spring, a shrine), using the pack's dead and abandoned tiles for the Blighted look. The ring timing, change-set layers and stage-change sequence are in §4 and §6.
- **The Blighted state is muted grey-green and quiet, not burnt:** "broken but hopeful".
- **The battle backdrop is drawn from the current Area**, so it follows Restoration (the only battle-side thing Restoration changes; see §4).
- **Open:** smooth transition edges between healed and Blighted ground (may be drawn later).

#### Other visual cues (owned elsewhere)
- Rare and Very rare Creatures shimmer on the map (§3).
- At Bond rank 3+ the following Creature uses a happier idle animation or emote (§3).
- The Focal point changes visibly at every stage (§4).
- Store art and listing must not look child-directed, to avoid Play's Families Policy (§6).

### 5.3 Orientation and input
*Source: [How does the game feel on a touchscreen?](issues/11-controls-and-orientation.md)*
*Source: [What is the technical architecture?](issues/09-technical-architecture.md)*
*Source: [What exactly does an Area's `.tmj` contain?](issues/23-area-map-format.md)*

#### Orientation
- **Portrait first.** Screen layouts are data: each screen is a controller script plus layout scenes, and only `portrait` is built in v1, with `landscape` as a reserved slot (§6).

#### Movement
- **Default: floating D-pad plus tap-to-move, together.**
  - **Tap-to-move** works anywhere on the map. Tapping an NPC or sign walks you to it and interacts: the path goes to the nearest walkable cell facing the target, then interacts.
- **Option: a fixed pad.**
- **Swipe-and-hold is dropped.**
- **Grid movement.** A quick press only **turns** you.
- **Run is on by default**, with a toggle.
- **The pad hides in battles and menus**, where you tap buttons directly.

#### The five input actions
- Touch, gamepad and keyboard all reduce to **five actions**, mapped to Godot input actions, before reaching a screen controller:

| Action | Meaning |
|---|---|
| `move(dir)` | one grid step or turn in a direction; menu focus navigation |
| `walkTo(tile)` | tap-to-move to a cell |
| `confirm` | interact (A), select |
| `back` | cancel (B) |
| `menu` | open the menu |

- **Gamepad and keyboard** are secondary input in v1.
- **Every menu has a focus cursor** with direction-based navigation.
- Headless tests drive the game only through these five actions (§6).

#### Left-handed mirroring
- **Ships at launch** as a layout setting. It flips horizontal anchors and the command-deck order: the A/B buttons and the battle thumb arc move to the other side.

### 5.4 Overworld screen
*Source: [How does the game feel on a touchscreen?](issues/11-controls-and-orientation.md)*

- **Map:** the top **~60%** of the screen.
- **Control deck:** the bottom **~40%**: the floating-pad zone, **A (interact)** and **B (back)** on the main-thumb side, and a small **Menu** button.
- **Dialogue boxes** cover the bottom of the map, just above the deck.
- The layout **respects notches and gesture bars** (safe areas).
- **No page scrolling or zooming** on the game surface.

### 5.5 Battle screen
*Source: [How does the game feel on a touchscreen?](issues/11-controls-and-orientation.md)*
*Source: [How does a battle work?](issues/07-battle-system.md)*
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*
*Source: [How is the move list structured?](issues/21-move-list.md)*

Battle rules (what is previewed, Status countdowns, stat stages, targeting rules): see §2. Layout, top to bottom:

| # | Band | Contents |
|---|---|---|
| 1 | **Info strip** | For each side: name, level, **HP bar**, **Energy bar**, **Status with its countdown**, **stat-stage arrows** (on the HP bar), and a **Trait icon**. Plus the **turn-order indicator**: small portraits in order, shown before confirming. |
| 2 | **Scene** | The Area-drawn backdrop, the **foe's front sprite** and the **player's back sprite** (64×64). |
| 3 | **Message line** | Battle text. It **advances on tap**, with a fast auto-advance setting. |
| 4 | **Command deck** | The same area as the overworld control deck. |

#### Command deck
- **Thumb arc** on the main-thumb side, in this order: **Fight** (under the thumb), **Catch** (shows the catch %), **Team**, **Run** (furthest).
- A **simple list** layout is available as a setting. Left-handed mode mirrors the arc.
- **Move list:** the **4 equipped moves plus the Basic move**. Each shows **name, Energy cost, Power/Focus icon, Type colour and accuracy**. Moves you can't afford are **greyed out**.
- A move's rules line is generated from its effects, and its flavour text shows on the Creature's page, not the battle deck (§2).

#### Preview and confirm
- **Tap a move once to preview it** on the target: damage as **% of HP**, **effectiveness**, and any **status chance**.
- **Tap it again to confirm.**
- **Tapping elsewhere cancels.**
- The **"one-tap moves"** setting skips the preview.

#### 2v2
- 2v2 happens only in set encounters; wild battles are always 1v1 (§2).
- **Two foes side by side at the top, the player's two at the bottom.** The info strip grows to **two rows**.
- **Actions are chosen for each player-controlled Creature in turn**; the active one is highlighted.
- **Targeting:** after picking a move, **tap a foe sprite**. **Valid targets glow.** A move with **a single valid target picks it automatically**.
- **AI ally slot** (the tag battle): the ally's slot shows **its own HP and Energy bars but takes no player input** (§2).

### 5.6 Menu and settings
*Source: [How does the game feel on a touchscreen?](issues/11-controls-and-orientation.md)*
*Source: [What should Project Wildling's pixel art look like?](issues/10-art-direction.md)*
*Source: [How do catching, the party, and storage work?](issues/08-catching-and-party.md)*
*Source: [How does Restoration change an Area?](issues/12-restoration.md)*

#### Menu
- **Team / Bag / Save.** The Region map (§4) and the Sanctuary (§3) are also reached from menus.
- An **"Autosaved"** notice appears after battles and Area changes (autosave points: §6).

#### Settings
Settings live in a separate `settings.json`, read through the `Settings` autoload (§6).

| Setting | Default | Effect |
|---|---|---|
| Movement scheme | **floating pad** (+ tap-to-move) | or a **fixed pad** |
| Left-handed mirroring | off | flips horizontal anchors and the command-deck order |
| Run | **on** | toggle |
| Follower | **on** | turns off the lead Creature following on the map (§3) |
| Battle text auto-advance | off (advance on tap) | fast auto-advance |
| One-tap moves | off (tap to preview, tap again to confirm) | skips the preview |
| Battle commands | **thumb arc** | or a **simple list** |
| Battle animations | **on** | off skips the code effects; also makes the Restoration sequence instant (§4) |

- Only the movement scheme and Run defaults are stated in tickets. The other defaults follow from how each setting is described (a toggle that "turns off" or "skips" something defaults to on, or to the preview), and are **Open** to confirm in the settings ticket.
- **No UI-scale setting in v1.**
- **Open:** colour-blind support (Type colours need icons or labels too).
- **Open:** a large-text mode.

### 5.7 Audio
*Source: [How does Restoration change an Area?](issues/12-restoration.md)*
*Source: [What is the technical architecture?](issues/09-technical-architecture.md)*

- An `Audio` autoload exists (§6), and Restoration stages can change an Area's music and ambient track (§4).
- **Open:** audio and music sourcing ($0 budget), style, and the SFX list.

## 6. Technology and release

### Engine and pins
*Source: [Which 2D engine fits an agent-built pixel-art game for Android + iOS?](issues/01-engine-choice.md)*
*Source: [How are Mendvale's Android and iOS builds made and released?](issues/17-builds-and-release-pipeline.md)*

- **Engine: Godot 4.7.x stable, typed GDScript only.** C# on mobile is still experimental, so it is never used.
- **Why Godot:** MIT licence, $0 fees; text scene and resource files agents can edit and diff; a full CLI (import, export, headless) with no login; gdUnit4 for tests; built-in pixel-perfect scaling.
- **Single pin:** `.godot-version` at the repo root holds `4.7.2-stable`. CI and the local setup notes both read it.
- **Known engine traps** every agent and CI step must respect:
  - **Headless runs can exit 0 even when scripts failed** (reproduced up to 4.7.2). CI never trusts Godot's exit code; it parses results and logs.
  - **`.uid` sidecar files** move and delete together with their scripts.
  - The base export is about 25 MB of engine.
- **iOS builds need a Mac with Xcode** (true of every engine).
- **Project identity (permanent, both stores):** Godot project name `mendvale`, app ID `io.github.andrew689cpu.mendvale`. Naming and store subtitle: see §1.

### Core and shell
*Source: [What is the technical architecture?](issues/09-technical-architecture.md)*
*Source: [A pure core owns every rule, including the overworld grid](../../docs/adr/0002-pure-core-owns-the-rules.md)*

- **Every game rule lives in a pure core** under `src/core/`: typed GDScript classes extending `RefCounted`, with no `Node`, scene tree, `Input` or autoload access. Content, the RNG and the clock are passed in. This covers battle, catch %, spawn rolls, XP, Bond, Restoration, the clock and the overworld grid.
- **Core purity lint:** CI fails if `src/core/` mentions `Node`, `get_tree`, `Input` or an autoload.
- **The presentation shell** under `src/game/` reads core state, sends player intent and plays the events the core returns. It holds no rules.
- **The core owns the overworld simulation.** Grid positions and movement of the player, follower, NPCs and visible wild Creatures (`wander`, `curious`, `shy`) advance on discrete ticks against the `AreaGrid`. The overworld scene only interpolates sprites between cells and plays effects. **Tick rate** and **in-game clock speed** are tuning data.
- **Overworld feel** (easing, bump and run animations) is built in presentation on top of cell-to-cell moves; nothing comes from physics.
- **Illegal intents never crash.** A move with too little Energy, a switch while Snared or a step into a wall returns `Rejected{reason}` and leaves state unchanged. `assert` is only for invariants in debug builds.

### Core modules
*Source: [What is the technical architecture?](issues/09-technical-architecture.md)*

Each module has a small interface, a `README.md` stating it, and its own tests through that interface.

| Module | Interface (gist) | Hides |
|---|---|---|
| `content` | `ContentDB.load(bundle) -> db`; typed read-only lookups by ID; `ContentLinter.check(db) -> Array[Issue]` | parsing, schemas, cross-references, aliases |
| `battle` | `Battle.create(setup, content, rng)`, `legal_actions(slot)`, `preview(action)` (damage range % of HP, effectiveness, catch %, status %, turn order), `resolve_turn(actions) -> Array[BattleEvent]`, `outcome()` | damage, Types, Statuses, Energy, stat stages, turn order, catch roll, N-per-side targeting |
| `ai` | `BattleAI.choose(view, side, tier, rng) -> actions` | the Wild, Trainer and Boss tiers (and challenge mode's fourth); sees only a read-only `BattleView` with the same information the player has |
| `growth` | `Growth.after_battle(creatures, result, content) -> Array[GrowthEvent]` | XP split by level gap, level-ups, newly learnable moves, Bond points, needle nudges, evolution offers |
| `world` | `Restoration.stage(area, facts, content)`, `Spawner.roll(patch, conditions, rng)`, `Clock` | K-of-M Mendings, "higher of stored and computed", weighted spawn tables, time of day |
| `events` | `EventRunner.start(event_id)`, `step(input) -> requests` | the closed command list, flags, branching |
| `save` | `SaveCodec.encode(state)`, `SaveCodec.decode(json) -> state`; `SaveStore` seam | the migration chain, `.bak` fallback, unknown IDs |
| `session` | `GameSession` intent methods (`step(dir)`, `walk_to(cell)`, `tick()`, `interact()`, `start_battle(...)`, `submit_turn(...)`, `rest()`, menu intents …), each returning events | coordinates everything above; the **only writer** of save state |

- **Presentation calls only `GameSession`**, plus `ContentDB` for display lookups. It never reaches the other core modules directly.
- **`SaveStore` is the only external seam**, with two adapters: a file adapter (`user://`) and an in-memory adapter for tests. Other seams stay internal until a second adapter appears.
- `GameSession.step(dir)` returns events such as `Moved`, `Bumped`, `EncounterStarted`, `TrainerSpotted` and `Warp`. `tick()` advances wild and NPC movement and the clock.
- Flag-dependent marker activity and occupancy are resolved by the core at runtime (flags aren't known at bake time); stage-dependent ones are baked (see Area maps).

### Battle events
*Source: [What is the technical architecture?](issues/09-technical-architecture.md)*

- **One turn in, an event list out.** Events are plain data: `MoveUsed`, `Damage{amount, effectiveness}`, `StatusApplied`, `Fainted`, `CatchAttempt{accepted}`, `XpGained` ….
- The battle scene plays them as text, bar animations and code effects, and **skips the visuals when battle animations are off**.
- **The player's side and the AI submit through the same `resolve_turn`.** Each slot on a set encounter's side has an optional `controller` (`player` by default, or an AI tier), so an AI ally can fight beside the player in a tag battle. Battle rules: see §2.

### Determinism
*Source: [What is the technical architecture?](issues/09-technical-architecture.md)*
*Source: [A pure core owns every rule, including the overworld grid](../../docs/adr/0002-pure-core-owns-the-rules.md)*

- **All randomness comes from an injected, seeded `Rng` wrapper.** CI fails on `randf`, `randi` or `randomize` anywhere outside it.
- **Each battle gets its own seed**, so **setup + seed + the actions submitted** reproduce it exactly. Each spawn roll is also seeded.
- **The per-save seed** (rolled at new game, stored in the save; it picks the starter trio, §3) is the root.
- This record is what makes mid-battle resume by replay and exact bug-report replays possible. Changing a battle rule can invalidate a stored replay; resume then falls back to the pre-battle autosave (see Save).

### Content: format, IDs and bake
*Source: [What is the technical architecture?](issues/09-technical-architecture.md)*
*Source: [Content is JSON baked into one bundle, not Godot Resources](../../docs/adr/0001-json-content-bundle.md)*
*Source: [How is the move list structured?](issues/21-move-list.md)*

- **JSON, one file per record**, cross-referenced by permanent string IDs: `content/species/<id>.json`, `content/moves/<id>.json`, `content/items/<id>.json`, and likewise for Traits, Areas, spawn tables, trainers, set encounters and events. Later tickets add NPC records, Forage tables, Boss records, town records and the region record (owned by §3 and §4). Each kind has a **JSON Schema**.
- **Not Godot `.tres` Resources:** they cross-reference by `ext_resource` path and uid, which is fragile to hand-write. Content isn't editable in the inspector; `ContentDB` turns the bundle into typed GDScript classes at load, and the schemas plus the linter do the inspector's job.
- **Global tuning tables are one JSON file each:** type chart, rarity weights, Bond tuning (rank thresholds, points per battle kind, needle range and step, the 5-level warning window, the follower-emote rank), XP curve, clock speed, tick rate, and `content/tuning/move_bands.json` (the damage constant `k` and the tier bands). Map tuning (ring width, `sight` default, wander radius) is data too.
- **Permanent snake_case IDs** (`grove_sprout`, `cinder_nip`), separate from display names, **never reused or changed after a release**. The save, spawn tables, evolutions, Mendings and map markers refer to records by ID. A rare rename goes through **`content/aliases.json`**, never an edit of the ID. The Collection log's display number is a separate field.
- **Generic identifiers only** in code and data (`creature`, `trainer`, `lure`, `sanctuary`, `collection_log`, `mending`). Every in-world name lives only in strings.
- **Closed lists in code** (a new entry needs code; a new record doesn't): Mending kinds (`register_natives`, `defeat_trainers`, `defeat_challenge`, `find_site`); Leaning axes (`style`, `type`, `habitat`, `time`); move effect kinds (11) and `anim` code effects (`strike`, `slash`, `bite`, `burst`, `beam`, `orb`, `wave`, `rain`, `quake`, `gust`, `aura`, `shield`); event commands; logic kinds; marker classes. Record fields for each kind: see §2 (moves), §3 (species, Bond), §4 (Areas, stages, items, Bosses).
- **Baked at build time.** `tools/bake_content` (a headless Godot script) merges `content/**/*.json` and every `content/maps/*.tmj` into one **`content.bundle.json`**, running the full linter and **failing the build on any lint error** (warnings don't fail). The bake also avoids opening about 1,000 small files on phone startup.
- **The game and the tests read only a bundle** (the real one or a fixture). The bake runs in CI before tests and export.
- **The bundle has no version of its own.** The bake stamps it with the app version and git commit, for bug reports only.

### Content linter
*Source: [What is the technical architecture?](issues/09-technical-architecture.md)*
*Source: [How does Restoration change an Area?](issues/12-restoration.md)*
*Source: [How does Bond shape a Creature?](issues/13-bond.md)*
*Source: [What items exist, and how does the economy work?](issues/14-items-and-economy.md)*
*Source: [How do the Bosses and Area gating sequence the region?](issues/15-bosses-and-gating.md)*
*Source: [Boss order comes from reachability, not a list](../../docs/adr/0003-boss-order-comes-from-reachability.md)*
*Source: [How is the Creature roster structured?](issues/16-roster-structure.md)*
*Source: [How is the region laid out?](issues/18-region-layout.md)*
*Source: [How is the move list structured?](issues/21-move-list.md)*
*Source: [What is Mendvale's story, and which beat sets each flag?](issues/22-story.md)*
*Source: [What exactly does an Area's `.tmj` contain?](issues/23-area-map-format.md)*

`ContentLinter.check(db)` runs inside the bake and as a test. Every rule is an **error** unless marked **warning**. The source ticket is in brackets. Rules that walk the region use one shared **walk of the Area graph from the new-game state, following flags**; Chapters and Area Chapters are derived by that walk, never written in content (ADR 0003).

#### A. Schemas, references, strings and events
1. Every record matches its kind's JSON Schema [09].
2. Every ID resolves, through `content/aliases.json` where renamed [09].
3. Events: no flag is read but never set; no battle points at a missing trainer [09].
4. No missing and no orphaned string keys [09].

#### B. Assets and licences
5. Every asset file has a row in `assets/LICENCES.csv` [09].
6. Every sprite uses only the locked 53-colour palette and is the right size: 64×64 battle, 16×16 map [09].
7. **Warning:** a sprite missing at its conventional path (the built-in placeholder is used) [09].
8. A **production** export fails if any reachable species still uses a placeholder (licence-ledger `placeholder` column) [16, 17].

#### C. Map files and layers
9. Map settings: orthogonal, 16 × 16 tiles, not infinite, CSV encoding, at most **64 × 64 tiles**, tilesets only from `content/maps/tilesets/` [23, 18].
10. Every `.tmj.import` matches the shared YATI preset [23].
11. Layer names and order match the layer table. One `stage_N` group per stage the Area has, each with only the four known sub-layers. `erase` appears only inside stage groups [23].
12. Every `logic` tile is one of the closed logic kinds [23].
13. **Warning:** a Habitat-patch cell with nothing drawn on it [23].

#### D. Map markers
14. Marker classes are from the closed list; names are snake_case and unique within the Area; marker IDs are unique across the region [23].
15. Required reference fields (`to_area`, `to_exit`, `trainer_id`, `npc_id`, `encounter_id`, `item_id`, `forage_table`, `event_id`) are set and resolve: trainers, NPCs, set encounters, items, Forage tables, events, Areas and exits. Only a dormant exit may leave `to_area` empty [23].
16. The shared activity fields are absent on `focal_point` and `blight_barrier`. Markers sharing an `npc_id` have non-overlapping stage ranges [23].
17. Exits pair up both ways; paired exits have the same length; every arrival cell is walkable at every stage where the exit is active [23].
18. Exactly **one dormant exit per region**, and only it may leave `to_area` empty [18, 23].
19. Exactly one `player_start` per region. Exactly one `focal_point` per Area with stages, and none in 0-stage Areas [23, 18].
20. No two blocking occupants share a cell at any stage, and no occupant stands on `wall` or `water` [23].
21. Camera zones don't overlap and cover every walkable cell [23].

#### E. Areas and region layout
22. Area `kind` is one of `town`, `route`, `dungeon`, `landmark`, `interior`. Interiors have 0 stages and a `parent`. Only `home_town` and interiors have 0 stages [18].
23. Areas with Habitat patches list 3–6 native species; Areas without patches list none [18, 12].
24. Every Habitat patch and every species' home Habitat uses one of the 8 Habitat kinds [18].
25. **Rest-point distance:** no critical-path cell is more than one Area exit from a Rest point, checked on the baked grid [18, 23].
26. Level bands come from each Area's **derived Chapter** (the Chapter in which it first becomes reachable): spawn tables, trainers and Area challenges fit that band, with the +1–2 top allowance for later stages. Band values: see §4 [18, 15].

#### F. Restoration
27. Every Mending for stage N is completable while the Area is at stage N−1 (e.g. a species to register spawns in an earlier stage's table) [12, 23].
28. **Only stage 1 opens critical-path routes**; stages 2+ open only optional paths [12, 23].
29. Blight barriers clear only at stage 1 [09, 23].
30. **Flood-fill reachability** on the baked grid per stage treats every occupant (beaten trainers included) and every uncleared barrier as blocking [23].

#### G. Gating, Bosses and economy (on the region walk)
31. Every barrier's flag is set somewhere reachable before the barrier [15, ADR 0003].
32. Each Boss becomes reachable, and each Boss in a Chapter can be reached without beating the others in it [15, ADR 0003].
33. Every Area with stages gets its stage 1 from a reachable flag, the finale's `boss_8` flag included [15, 25, ADR 0003].
34. At least 2 catchable species with a 2× edge over each Boss's theme Type are reachable before that Boss [15].
35. Wild, trainer and Area-challenge levels fit the Chapter bands [15] (see 26).
36. No reachable wild Creature or gift is above the challenge-mode level cap for the Bosses-beaten count at that point [15].
37. **Balance check:** critical-path income up to each Boss (trainers, challenges and item spots on the way) covers a target shopping list for that point [14].
38. The **Boss 1 simulation gate** passes for every starter in every trio (see Tests) [15].

#### H. Bond and evolution
39. For each branching species: **Type axis** ends are Types the Creature can learn moves of (level-up or Bond) before its evolution level; **Habitat axis** ends exist in Areas reachable before the line's usual evolution level; **Time axis** is always valid; **Style axis**: it can learn at least one Power and one Focus move before evolving [13].
40. Bond moves: 2–4 per species, ranks 1–5, no duplicates [13].
41. At most one branch point per evolution line [13, 16].

#### I. Roster
42. Total species count against the budget, and the forms per line [16].
43. Evolution levels within their bands, and none above level 44 [16].
44. Branch forms are in no spawn table [16].
45. Type counts: 12–20 species per Type; at least 2 non-starter primary lines per Type; at least 4 final forms per Boss theme Type; no dual-type pair on more than 2 lines [16].
46. Base catch % within ±5 of its stage band [16].
47. Spawn entries fit the species' home Habitat and its times of day [16].
48. Every line has a Power and a Focus move before its first evolution, and 2 extra move Types by its final form [16].
49. Species display names are 4–9 letters and absent from the franchise **blocklist file** [16].

#### J. Moves
50. The move schema, the closed effect-kind list, the `anim` list, and the readability limit: ≤1 side effect on a damaging move, ≤2 effects on a move with no damage [21].
51. Each move within its tier band and side-effect pricing, within a tolerance [21].
52. The per-Type grid floor: 11 level-up moves in their slots and 2 Bond-only moves [21].
53. A Status sits on its 1–2 home Types, and each other Type borrows at most 1 move per Status [21].
54. Tier floors: by level on level-up lists, by Bond rank on Bond lists; signature moves only at rank 5 [21].
55. `bond_only` moves are on no level-up list; each signature move is on exactly one line [21].
56. 2v2-only moves: at most 8, and none on a level-up list before level 20 [21].
57. Damaging moves never use the `all` target [21].
58. Trainer and Boss loadouts are learnable by that species at that level and Bond rank [21].
59. Move names: at most 12 characters, unique, and absent from the blocklist (extended with the genre's well-known move names) [21].

#### K. Story and set encounters
60. No Starter line on the rival's teams [22].
61. Rival battles 1–3 sit at the previous Chapter's ace + 1; every rival and Faction team fits the derived Chapter's trainer ceiling [22].
62. A set encounter with an AI-controlled slot on the player's side has exactly one `player` slot [22].

- The "do not echo" list of iconic genre designs is checked by eye in review, not by the linter (§3).

### Area maps
*Source: [What exactly does an Area's `.tmj` contain?](issues/23-area-map-format.md)*
*Source: [Which tool authors Area maps, and how do they become content data?](issues/19-map-authoring.md)*

- **An Area's map is a Tiled 1.12 `.tmj` file, the source of truth.** Tiled writes one map row per line, so a one-tile change is a one-line diff. The core and linter never read a Godot scene or an importer.
- Not Godot `TileMapLayer` scenes (each layer's tiles are one base64 string agents can't read or diff); not LDtk (stalled); not Tiled's built-in Godot exporter (writes the deprecated `TileMap` node).
- **Tiled 1.12 list properties are not used** until tested.

#### Layers
In draw order:

| Layer | Kind | Drawn | Holds |
|---|---|---|---|
| `ground` | tile | yes | floor, paths, water surfaces |
| `detail` | tile | yes | trees, rocks, fences, tall-grass looks, barrier drawings |
| *(actors)* | — | — | the shell draws the player, follower, NPCs, trainers and wild Creatures here; not a Tiled layer |
| `overhead` | tile | yes, above actors | tree tops and roofs the player walks behind |
| `logic` | tile | no (50% opacity in Tiled) | one logic kind per cell |
| `stage_1`, `stage_2` … | group | no | one per Restoration stage, each holding sub-layers `ground`, `detail`, `overhead`, `logic` |
| `markers` | object | no | every marker object |

- **A stage group is a change set, not a drawn layer.** It holds only the cells that change at that stage. An empty cell means "no change"; the reserved **`erase`** tile (from `logic.tsj`) removes the base tile (a dead tree becomes a living one, brambles disappear).
- **Stages stack:** stage 2's changes apply on top of stage 1's. Stage 0 is the base layers alone. One group per stage the Area has.
- **The shell plays the swap:** it copies the changed cells onto the base layers in rings by **Chebyshev distance** from the focal point, with the ring width as tuning data. On entering an Area already at stage S, it applies stages 1…S at once. Presentation timing: see §4.
- **The bake precomputes the grid per stage**, folding `logic` and each `stage_N/logic` into walkable cells, logic kinds and patches, so the core never replays layers.
- **Open:** the starting value for the swap ring width is not set.

#### Logic kinds
A closed list, carried as a `kind` property on each tile of `logic.tsj`. An empty cell is plain walkable floor.

| Kind | Rule |
|---|---|
| `wall` | blocks everything |
| `water` | blocks walking (no surfing in v1: there are no field moves) |
| `counter` | blocks walking; interaction passes through it by one cell |
| `ledge_s`, `ledge_e`, `ledge_w` | one-way hop in that direction; no north ledge (the region reads bottom to top, so ledges only speed up the trip home) |
| `meadow` … `ruins` | the 8 Habitat kinds (Meadow, Woodland, Wetland, Coast, Cavern, Crag, Snowfield, Ruins; §4); walkable Habitat-patch cells |
| `erase` | only in stage groups: removes the base cell |

#### Habitat patches
- **Patches are logic tiles only;** there is no patch marker.
- **A patch is a 4-connected run of cells of one Habitat kind**, found by the bake for each stage. Its ID is bake-assigned and not permanent (spawn state is never saved).
- A stage's `logic` sub-layer adds or removes patches (a refilled pond).
- Spawn-table conditions key on the Habitat kind. Two patches of one kind in an Area share a spawn table; an Area needing two mixes uses two kinds. "Up to 4 per Habitat patch" applies per connected run (§3).
- **Wild Creatures stay on their patch's cells:** `curious` approaches only up to the edge, `shy` flees within it.
- The look (tall grass, shallows) is drawn separately on `ground`/`detail`.

#### Markers: identity and shared fields
- **Identity:** a marker's local name is the Tiled object's built-in **Name** (snake_case, unique within the Area). Its ID is **`<area_id>.<name>`**. Saves refer to marker IDs, so they are **permanent once released**; a rename goes through `content/aliases.json`.
- **Shared fields** on every class except `focal_point` and `blight_barrier`:

| Field | Type | Default | Meaning |
|---|---|---|---|
| `stage_from` | int | 0 | active from this Restoration stage |
| `stage_until` | int | 0 | inactive from this stage on; **0 means no end** |
| `flag_on` | string | `""` | active only once this story flag is set |
| `flag_off` | string | `""` | inactive once this story flag is set |

- A marker is active when all four hold. An NPC that moves between stages is two markers with the same `npc_id` and non-overlapping stage ranges. Per-stage dialogue lives in the NPC record. Story placement uses the flags (the rival stands outside the inn until `starter_chosen`, via `flag_off`).

#### Marker classes
A closed list of **15 classes**. `Dir` is a Tiled string enum: `up`, `down`, `left`, `right`.

| Class | Shape | Fields | Notes |
|---|---|---|---|
| `player_start` | point | `facing: Dir` | exactly one per region, in `home_town` |
| `exit` | rect, 1 tile thick | `to_area: string`, `to_exit: string` (local name there), `facing: Dir`, `dormant: bool` | Area exits, doors, map-edge roads and internal warps (`to_area` = own Area) |
| `rest_point` | point | `facing: Dir` | the Lantern-keeper: the shell draws them, talking rests, and after a loss the player returns to the cell they face |
| `shop` | point | `facing: Dir` | the clerk; stock comes from the town record (for an interior, its `parent`) |
| `trainer` | point | `trainer_id: string`, `facing: Dir`, `sight: int` (default 3; 0 = talk only), `movement` (`still`/`turn`) | counts toward `defeat_trainers` |
| `npc` | point | `npc_id: string`, `facing: Dir`, `movement` (`still`/`turn`/`wander`, within 2 tiles) | the NPC record holds the sprite and per-stage dialogue event |
| `encounter` | point | `encounter_id: string`, `facing: Dir` | any set encounter touched or talked to: Area challenge, Boss, rare one-off; no sight line; the shell draws the lead's sprite |
| `item_spot` | point | `item_id: string`, `count: int` (default 1) | visible, taken once; no invisible items |
| `forage_spot` | point | `forage_table: string` | regrows each in-game day; Restoration adds more through `stage_from` |
| `hidden_site` | point | `requires_species: string` (default `""`) | its ID is the `find_site` ID; flavour from string `site.<id>`; flag conditions use `flag_on` |
| `blight_barrier` | rect | none | blocks its cells while the Area is below stage 1, clears at stage 1; a `stage_1` erase removes its drawing; text from `barrier.<id>` |
| `focal_point` | point | none | on the drawn spring or shrine; one per Area with stages, none otherwise; interacting opens the Mending checklist |
| `trigger` | rect | `event_id: string` | runs an event when the player steps in; "once only" is a `flag_off` the event sets |
| `interact` | point | `event_id: string` | signs, bookshelves, statues: runs an event when faced and interacted with |
| `camera_zone` | rect | none | the camera clamps to the zone holding the player |

- **Never on the map:** weather, music, spawn tables, native species and shop stock stay in the Area JSON.

#### Exits and warps
- **An exit fires when the player steps into** one of its cells.
- **Arrival:** the player lands on the paired exit at the **same offset along it** (clamped), then is placed **one cell inward** in that exit's `facing` direction, facing that way. Standing on an arrival cell never fires anything.
- **Map-edge roads** are a 1-tile-thick `exit` along the edge row.
- **Internal warps** (stairs between dungeon floor sections) are exits within one Area; they cut to the new `camera_zone` with a short fade.
- **The dormant ferry:** a `dormant: true` exit is drawn, shows "not running yet" text and never fires. A second region gives it a target and a `flag_on` set by its event, and drops `dormant`, in that content patch.

#### Blocking and interaction
- **Occupants block their cell while active:** `rest_point`, `shop`, `trainer`, `npc`, `encounter`, `item_spot` (until taken), `forage_spot` (always, even when picked). **Beaten trainers keep blocking.** Wild Creatures and the follower also block, as runtime state.
- **Not blocking:** `exit`, `trigger`, `camera_zone`, `focal_point`, `hidden_site`, `interact` (the last three usually sit on drawn `wall` cells).
- Stage-dependent occupancy is baked per stage; flag-dependent occupancy is resolved by the core at runtime.
- **Interaction (`confirm`)** is with the occupant, `interact`, `hidden_site` or `focal_point` on the faced cell. A `counter` cell passes interaction to the next cell.
- **Tap-to-move** paths to the nearest walkable cell facing the target, then interacts.

#### Camera zones
- Zones may not overlap, and every walkable cell sits in one. **A map with no zones** uses the whole map as one zone.
- A zone smaller than the screen (an interior about 8 × 6 tiles in an 11 × 12 view) is centred, with black around it.
- Zones are camera-only and carry no gameplay. The Region map stays one panel per Area.

#### Class defaults
- **The bake merges class defaults** from the committed `.tiled-project` (as YATI does on import). Maps stay as Tiled saves them, without default values.
- Required reference fields default to `""`, and the linter rejects them empty, except `to_area` on a dormant exit.
- **The `.tiled-project` is the one schema** for marker classes and enums. A unit test pins it to the classes and fields the bake expects.

#### Files
- **One `.tmj` per Area, interiors included:** `content/maps/<area_id>.tmj`. The file name is the link to the Area record, which has no map field. Dungeon floors are sections of one file.
- `content/maps/mendvale.tiled-project`: marker classes and enums.
- `content/maps/tilesets/`: one external `.tsj` per Ninja Adventure sheet, plus `logic.tsj`.
- `assets/tiles/<sheet>.png`, each with a committed `.import` sidecar and a `LICENCES.csv` row. Swapping art means replacing a PNG on the same grid.
- An Area's per-stage tile changes live in its map's `stage_N` group and its focal point is a map marker; the rest of each stage's data stays in the Area JSON (§4).

#### What the bake emits
For each Area, the `AreaGrid` in `content.bundle.json` holds:
- the size
- for each stage: the logic kind per cell, the walkable cells, and the patches (kind plus cells)
- every marker with its ID, class, cells (a point is one cell; a rect is its cells), resolved fields and the shared activity fields
- the camera zones

Tile art is never in the bundle. The bake decodes GIDs and flip bits itself.

#### Agents editing maps
- Agents may hand-edit a `.tmj` as JSON (adding markers, changing CSV cells). The bake and linter are the safety net. Nothing has to re-save through Tiled, since CI has no Tiled.
- Optional `tools/tiled_resave.sh` (`--export-map json`, which keeps external tilesets) normalises formatting locally.
- **`AGENTS.md` map rules:** CSV encoding only, with "minimize output" off; never renumber `firstgid`; every marker uses a class from the project file; bump the map's `nextobjectid` when adding an object.
- **Tiled tooling facts:** the CLI can draw and save maps headless (`--evaluate`), but its script API can't open a tileset there ("Editor not available"); `--resolve-types-and-properties` writes class defaults into an exported map; Tiled escapes `/` as `\/` in JSON.

### Map import (YATI)
*Source: [What exactly does an Area's `.tmj` contain?](issues/23-area-map-format.md)*
*Source: [Does the YATI importer turn a Tiled Area into Godot tile maps on the Mac, the same way every time?](issues/20-yati-import-check.md)*
*Source: [Which tool authors Area maps, and how do they become content data?](issues/19-map-authoring.md)*

- **YATI 2.2.9** (MIT, GDScript build), vendored in `addons/`, generates the `TileMapLayer`s from the same `.tmj` on import. It is checked on macOS with Godot 4.7.2 and Tiled 1.12.2: every cell matches (tile, atlas coords, flip, transpose), logic tile properties become a TileSet custom-data layer, markers keep position, class, id and typed properties, and a Godot render matches Tiled's with 0 differing pixels.
- **Multi-threaded import off** (`editor/import/use_multiple_threads=false`; YATI has no thread option).
- **Not byte-reproducible:** two clean imports differ only in per-node `unique_id=` values, which Godot 4.7 randomises on every save.
- **Fallback (contingency only):** a small script paints the layers at runtime with `set_cell`; the bake still reads the `.tmj`.
- **One shared import preset for every map:** `add_class_as_metadata=false`, `add_id_as_metadata=false`, `tiled_project_file` set to the committed project, `post_processor` set to `src/game/overworld/map_import_post.gd`.
- **The post-processor, on import:**
  - deletes the `markers` layer, so no `StaticBody2D` (rect markers) or `Marker2D` (point markers) reach the scene
  - deletes `logic` and every `stage_N/logic`
  - keeps each `stage_N` group's drawn sub-layers, hidden, as cell sources for the swap
  - sets `overhead` to draw above the actor layer
  - strips any physics, navigation and occlusion from the TileSets
- **At runtime the shell** instances the imported scene for the Area, draws actors itself from the bundle's markers and `GameSession` state, and plays stage swaps by copying cells (source, atlas coords, alternative/flip) from the hidden `stage_N` layers onto the base layers.
- **Import traps the CI gates exist for:**
  - **Embedded textures:** if a tileset PNG has no `.import` sidecar yet when a map imports, YATI embeds the raw pixels (2.1 MB instead of 20 KB), and the bloated scene stays cached until the map's content changes.
  - **Failures exit 0.** Broken `.tmj` JSON logs `SCRIPT ERROR` and `ERROR: Error importing`, then Godot writes **`valid=false`** into the `.tmj.import` and never re-imports that map, even after a fix and a `.godot/` wipe; only restoring the `.import` recovers. A missing `.tsj` logs `ERROR: Tileset file … not found` and `Import finished with 1 error.` with no `SCRIPT ERROR`, and still writes a partial scene.
  - Leaked-RID errors at exit are noise.
- **Import gates in the `check` job:**
  1. Every asset has a committed `.import` sidecar, and none contains `valid=false`.
  2. The import log is scanned for `Error importing` and `Import finished with`, as well as `SCRIPT ERROR`.
  3. Every `.tmj` has an imported scene, and no imported map scene contains an `Image` sub-resource.
- **A gdUnit test** imports a fixture map and asserts the output contains only the expected nodes, so a YATI upgrade that changes the import fails loudly.

### Events and dialogue
*Source: [What is the technical architecture?](issues/09-technical-architecture.md)*

- NPC talk, story beats, gifts, cutscenes, gates and Boss rewards are **JSON arrays of steps from a closed command list** (`say`, `choice`, `set_flag`, `if_flag`, `give_item`, `give_creature`, `battle`, `move_actor`, `wait`, `heal` …), run by `EventRunner`. They emit presentation requests the same way battles emit events.
- A new kind of step is a code change; a new event is content only. Map `trigger` and `interact` markers and NPC records point at events by `event_id`.
- **Open:** the full closed command list is given only as "…"; the complete set is not specified.

### Art and strings
*Source: [What is the technical architecture?](issues/09-technical-architecture.md)*
*Source: [How is the Creature roster structured?](issues/16-roster-structure.md)*

- **Content records hold no asset paths.** Art is found by convention from the ID: `assets/creatures/<id>/front.png`, `back.png`, `map.png`; `assets/items/<id>.png`; `assets/tiles/<sheet>.png`; and so on. A built-in placeholder is used when a file is missing, so swapping art means dropping in a file. Sizes and palette: see §5.
- **Licence ledger `assets/LICENCES.csv`:** one row per asset with source, licence, author, URL and a `placeholder` column. Allowed licences: see §5.
- **Placeholder mapping (dev-only):** every species maps to one of the 56 *50+ Monsters Pack 2D* sprites or a generated palette silhouette. Test-channel exports allow placeholders; production exports fail on any reachable one.
- **Every player-facing string goes through `tr()`.** Keys derive from IDs (`species.grove_sprout.name`, `move.cinder_nip.name`, optional `move.<id>.flavour`, `site.<id>`, `barrier.<id>`); text lives in **`strings/en.csv`** (Godot's CSV translation import). In-world terms are keys too (`term.creature` → "Verdling"), so a rename is one CSV edit. A move's card text is generated from its `effects[]`, not stored.
- **Only English ships in v1.**
- **Open:** languages beyond English, colour-blind support and a large-text mode (map fog: Save, settings & accessibility).
- **Open:** whether a sprite missing at its conventional path (built-in placeholder) also fails the production no-placeholder gate is not stated.

### Scenes and screens
*Source: [What is the technical architecture?](issues/09-technical-architecture.md)*

- **One persistent `Main` scene** owns a single `GameSession` and a **screen stack**: Title → Overworld, with Battle, menus and the Restoration sequence pushed on top. The overworld stays loaded under a battle; Areas swap as child scenes of the overworld.
- **Autoloads hold no game state:** only `Content` (read-only, loaded once), `Settings` and `Audio`.
- **Every screen is a controller script plus one or more layout scenes.** The controller handles behaviour and the five input actions; layouts are Control nodes with anchors. Only `portrait` is built in v1; `landscape` is a reserved slot. Left-handed mirroring is a layout flag that flips horizontal anchors and the command-deck order.
- **Input:** touch, gamepad and keyboard all reduce to five actions (`move(dir)`, `walkTo(tile)`, `confirm`, `back`, `menu`) before reaching a controller.
- **Render:** 180 px wide internally, integer scaling, height extended to fill (viewport stretch, aspect expand, integer scale). Screen layouts, controls and settings: see §5.

### Save
*Source: [What is the technical architecture?](issues/09-technical-architecture.md)*
*Source: [How are Mendvale's Android and iOS builds made and released?](issues/17-builds-and-release-pipeline.md)*

- **One slot**, JSON in `user://` with a top-level integer `version`. **`settings.json` is separate.**
- **`version` is independent of the app version:** a plain integer bumped only when the save's shape changes. Every bump ships with a migration and a migration test. Content changes never need one (IDs are permanent).
- **Migrations:** loading runs a chain of pure functions (`v1→v2`, `v2→v3` …), each tested on its own.
- **Downgrades are refused:** a save with a newer `version` than the app understands shows a message and isn't loaded or overwritten.
- **Atomic writes:** write `save.tmp`, then rename. The previous save is kept as `save.bak` and used if the main one fails to parse.
- **The save holds facts only:**
  - seed, clock, current Area, cell and facing
  - Creature instances, each with a permanent instance id: species, level, XP, learned and equipped moves, Trait, current HP, nickname, `bond_points`, `needles` (`{axis: {ends, value}}`), and its place (Party slot or Sanctuary)
  - bag (item ID → count), money, story flags
  - item spots taken, each Forage spot's last-picked in-game day, the Rest point last used (by marker ID)
  - Restoration facts (species registered per Area, trainers beaten, sites found), highest stage reached per Area, and the pending-presentation queue per Area
  - rare one-off Creature state, Collection log entries (seen, caught, Traits and branches discovered, where-found facts)
- **Derived values are never stored:** stats, Bond rank, current Restoration stage (the higher of stored and computed), pending evolution offers, Forage regrowth, shop stock and spawn state are recomputed. A test fails if any `SaveCodec` field can be computed from the others.
- **Unknown IDs** (content removed in a patch) are kept but ignored and never crash a load.
- **When it writes:** on OS pause (`NOTIFICATION_APPLICATION_PAUSED`), at autosave points (after battles, on Area changes, after the Restoration sequence) and on manual Save.
- **Mid-battle resume:** a pause during battle also stores an `in_battle` record (setup + seed + actions so far); resume replays it silently to the same turn. A replay that no longer matches (a patch changed a move) falls back to the pre-battle autosave.
- **Open:** the save field for a Boss rematch's once-per-in-game-day readiness (§4) is not specified.

### Tests and developer tools
*Source: [What is the technical architecture?](issues/09-technical-architecture.md)*
*Source: [How do the Bosses and Area gating sequence the region?](issues/15-bosses-and-gating.md)*

- **gdUnit4.** CI gates on its JUnit XML plus a log scan for `SCRIPT ERROR`, never on Godot's exit code.
- **Three layers:**
  1. **Core unit tests** through each module's interface: most of the suite, fast, no scenes.
  2. **Content lint** as a test (the bake's linter).
  3. **Headless scenario tests** that boot `Main` with a fixture save, drive it only through the five input actions, and assert on `GameSession` state. Many scenarios instead run directly on `GameSession`.
- **Named tests:** each save migration on its own; no derivable `SaveCodec` field; the `.tiled-project` pinned to the bake's classes and fields; the YATI fixture-map import shape.
- **Boss 1 simulation gate** (part of the content tests): for **every starter in every trio**, a bot party of the starter plus the two most Common species from the Areas before Boss 1, all at level 10, fights Boss 1 (Trainer-tier AI, 2 Creatures) in **200 seeded headless runs** and must win **≥70%**, or the build fails. With 12 starters (§3) that is 2,400 battles; the CI budget allows up to 15 starters (3,000). The same harness can later run every Boss against an "expected party" as a balance report.
- **No screenshot or golden-image tests in v1.**
- **Debug menu (dev-only):** sends debug intents through `GameSession`: warp, give a Creature or item, set a flag, set the clock, add Restoration facts, start any set encounter. Left out of test and production exports by a Godot feature tag.
- **Named fixture saves** in `tests/fixtures/saves/` ("before Boss 3", "Area X at stage 2") serve scenario tests and manual playtesting. Debug channel only.

### Repo layout and agent rules
*Source: [What is the technical architecture?](issues/09-technical-architecture.md)*
*Source: [What exactly does an Area's `.tmj` contain?](issues/23-area-map-format.md)*
*Source: [How are Mendvale's Android and iOS builds made and released?](issues/17-builds-and-release-pipeline.md)*

- **Layout:** the Godot project (`project.godot`) at the repo root; `src/core/<module>/`, `src/game/<screen>/`, `content/` (incl. `content/maps/`, `content/tuning/`, `content/aliases.json`), `strings/`, `assets/` (incl. `LICENCES.csv`), `tests/` (mirroring `src/`, plus `tests/fixtures/saves/`), `tools/` (`bake_content`, `ci/install_godot.sh`, optional `tiled_resave.sh`), `addons/` (YATI), `.godot-version`.
- **Committed:** `export_presets.cfg`, every `.import` sidecar, `.uid` files. **Never committed:** `.godot/`, `.godot/export_credentials.cfg`, `android/build/` (gitignored), paid assets.
- **`AGENTS.md` rules:**
  - Godot pinned to **4.7.x** (`.godot-version`); upgrades only as a deliberate PR
  - typed GDScript only, with the `untyped_declaration` and `unsafe_*` warnings set to **error** in project settings
  - `.uid` files move and delete together with their scripts
  - `.godot/` is never committed
  - `src/core/` stays pure
  - randomness only through `Rng`
  - display text only through `tr()`
  - maps: CSV encoding only with "minimize output" off; never renumber `firstgid`; every marker uses a project-file class; bump `nextobjectid` when adding an object
- **Agents work through PRs;** only the human pushes version tags.

### CI: GitHub Actions
*Source: [How are Mendvale's Android and iOS builds made and released?](issues/17-builds-and-release-pipeline.md)*

- The repo (`andrew689-cpu/rpg`) is **public**, so standard GitHub-hosted runners, macOS included, are **free and unlimited**. At most 5 macOS jobs run at once on the Free plan; larger runners are never used.
- **`check` workflow**, on every PR and every push to `main`, on `ubuntu-latest`:
  1. `bake_content` with the full linter (Area-graph gating, map markers, roster checks).
  2. The Boss 1 simulation gate and the three gdUnit4 layers.
  3. Gate on the gdUnit4 JUnit XML plus a `SCRIPT ERROR` log scan, **never on Godot's exit code**.
  - The `godot --headless --import` step (multi-threaded import off) carries the three import gates (see Map import).
  - Time budget **10 minutes**. The job prints its slowest gates.
- **On pushes to `main` only**, two extra jobs:
  - a **debug APK** (Godot's debug keystore, debug menu included), kept as a workflow artifact for **14 days**, for sideloading onto the human's Android phone
  - an **unsigned iOS build** on `macos-26` (`xcodebuild build` with `CODE_SIGNING_ALLOWED=NO`), so the iOS path can't rot before the Apple membership exists
- **`release` workflow**, on a `v*` tag: checks the tag's commit is on `main`, runs `check`, then builds, signs and uploads both platforms. Signing secrets live in a GitHub **`release` environment** used only by this workflow; fork PRs never see secrets.
- **A GitHub tag ruleset** limits creating `v*` tags to repo admins. The ruleset is the guard, so the environment needs no extra approval click.
- A GitHub Release with auto-generated notes is created for each tag; no binaries are attached.

### Godot in CI, upgrades and build size
*Source: [How are Mendvale's Android and iOS builds made and released?](issues/17-builds-and-release-pipeline.md)*

- **`tools/ci/install_godot.sh`** (our own script; no third-party setup action in workflows holding signing secrets) downloads the official Linux x86_64 editor from the `godotengine/godot` GitHub release, checks it against the published `SHA512-SUMS.txt`, and caches it by version. Only export jobs fetch the ~1.28 GB export templates, cached the same way.
- **`.godot/` import cache** is keyed on the Godot version plus a hash of `assets/` and `content/`.
- **Third-party actions** are pinned to a commit SHA; Dependabot proposes updates.
- **Upgrades are deliberate:** a Godot upgrade is a PR that bumps `.godot-version`, passes `check`, and has a test build installed on both phones. Patch releases are taken when they fix something we hit; minor versions (4.8+) only when a store rule needs them. Xcode is bumped the same way.
- **Annual July check:** a recurring issue reviews store rules ahead of Play's 31 August target-SDK deadline and Apple's April SDK deadline. The first moves to **Xcode 27 and the iOS 27 SDK before April 2027**.
- **Test devices:** one Android phone and one iPhone. Each Godot upgrade and each release candidate is installed on both.
- **Official export templates in v1, no custom template.** Godot 4.7.2's arm64 Android engine library is about 24 MB compressed (71 MB installed, since 16 KB alignment keeps native libraries uncompressed), so the download should be roughly 25 MB plus assets.
- Each release job **reports the AAB size and estimated per-device download**, and **fails above 150 MB** (headroom under Play's 200 MB base-module limit).
- A custom template (`disable_3d`, `optimize=size`; about 15% smaller) becomes a separate task only if the report shows more than **60 MB** to download.

### Build channels and versions
*Source: [How are Mendvale's Android and iOS builds made and released?](issues/17-builds-and-release-pipeline.md)*

| Build channel | Made from | Contains |
|---|---|---|
| **debug** | `main` pushes and local runs only, never a tag | debug menu and named fixture saves |
| **test** | tag **`vX.Y.Z-beta.N`** | a release export; placeholder Creature sprites allowed |
| **production** | tag **`vX.Y.Z`** | store-ready; must pass the no-placeholder gate |

- Everything before launch is a beta, starting at **`v0.1.0-beta.1`**.
- The debug menu and fixture saves are left out of test and production exports by Godot feature tags.
- **`version_name`** (Android): the tag without the `v` (`0.4.0-beta.2`). **`CFBundleShortVersionString`** (iOS): the bare `X.Y.Z`, since Apple rejects suffixes.
- **`version_code`** (Android) and **`CFBundleVersion`** (iOS) are the same integer: **`X·1,000,000 + Y·10,000 + Z·100 + B`**, where B is the beta number (1–98) and **99** for production. `0.4.0-beta.2` → 40,002; `1.0.0` → 1,000,099. It always increases, a beta sorts before its release, and nothing is stored.
- **Limits:** Y, Z ≤ 99; at most 98 betas per version. The release workflow refuses a tag that breaks them, or whose code isn't higher than the last uploaded build.
- Save `version` and the content bundle are independent of the app version (see Save; Content).

### Android pipeline
*Source: [How are Mendvale's Android and iOS builds made and released?](issues/17-builds-and-release-pipeline.md)*

- Export **AAB**, which in Godot 4.7 requires **Use Gradle Build**. CI installs the Android build template fresh each build; `android/build/` is gitignored (no Java plugins).
- **Toolchain** (as Godot 4.7.2's source expects): **Java 17, compile and target SDK 36, build-tools 36.1.0, NDK 29**, via `setup-java` and `sdkmanager`.
- **Min SDK 24**; **arm64-v8a only**; **16 KB page size** is built in since Godot 4.5.
- **Play App Signing:** Google holds the app signing key. One **upload keystore**, generated once, lives in the `release` environment (base64 keystore, alias, passwords), with an offline backup in the human's password manager. A lost upload key can be reset in Play Console.
- `export_presets.cfg` is committed; Godot's secret fields live in `.godot/export_credentials.cfg` (never committed), and CI supplies them through `GODOT_ANDROID_KEYSTORE_RELEASE_*` env vars.
- **Upload:** every tag, beta or production, uploads its AAB to the **Play internal track** via the Play Developer Publishing API, using `r0adkll/upload-google-play` pinned to a commit SHA and a service-account JSON secret. The AAB is also kept as a workflow artifact.
- **Promotion is manual** in Play Console: internal → closed testing → production. Only production builds are ever promoted to production. The first closed test starts from a beta of the **Vertical slice**.
- **Store order:** Android's pipeline runs first; both stores launch together.

### iOS pipeline
*Source: [How are Mendvale's Android and iOS builds made and released?](issues/17-builds-and-release-pipeline.md)*

- The pipeline is written and tested from day one (the unsigned `main` build), but the **$99/yr Apple membership is bought at the Vertical slice**.
- **Built in CI** on a pinned **`macos-26`** runner with an explicit `xcode-select` to **Xcode 26.6** (Xcode 26 and the iOS 26 SDK are required for uploads since 2026-04-28).
- **Godot exports the Xcode project only** (`application/export_project_only=true`). Our script then runs `xcodebuild archive` and `xcodebuild -exportArchive -allowProvisioningUpdates` with the `-authenticationKey*` flags and `destination=upload` in the export-options plist. This **cloud-signs with an App Store Connect API key** and uploads to TestFlight in one step.
  - Not Godot's own `.ipa` export: it never passes an API key (CI would need a certificate and profile in a temporary keychain), its env-var names differ from the docs (`GODOT_APPLE_PLATFORM_PROVISIONING_PROFILE_UUID_*`), and in 4.7.2 the release one reads the debug variable.
- The API key (issuer ID, key ID, `.p8`) lives in the `release` environment. The team ID and signing identity aren't secret and stay in `export_presets.cfg`.
- **Minimum iOS 15.0** (Godot's default; meets Apple's April 2027 floor).
- **Upload:** every tag goes to **TestFlight** for internal testers. Submitting for App Store review is **manual** in App Store Connect.
- **The human's Mac** installs full Xcode only for debugging on their iPhone: a free personal team before the membership (7-day provisioning), then test builds through TestFlight, with debug builds still through Xcode.
- **Open:** whether cloud signing needs an **Admin**-role API key (forum reports say so); confirm when the key is created.

### One-time setup (the human's steps)
*Source: [How are Mendvale's Android and iOS builds made and released?](issues/17-builds-and-release-pipeline.md)*

Done in this order, as a HITL checklist (a `wizard` script) once the pipeline code exists:
1. Create the GitHub `release` environment and the `v*` tag ruleset (admins only).
2. Generate the Android upload keystore; store it in the `release` environment and back it up in the password manager.
3. Register the Play developer account ($25), create the app (`io.github.andrew689cpu.mendvale`), and **upload the first AAB by hand** from a release run's artifacts (the Publishing API can't create an app or make the first upload).
4. Create a Google Cloud service account, enable the Play Developer API, invite the service account in Play Console (Users & permissions), and store its JSON in the `release` environment.
5. Install full Xcode on the Mac.
6. At the Vertical slice: buy the Apple Developer membership ($99/yr), create the App Store Connect app, create an API key (check the role needed for cloud signing), and store it in the `release` environment.

### Store requirements
*Source: [What do Google Play and the Apple App Store require for a free hobby game?](issues/04-store-requirements.md)*

- **Costs:** Play US$25 once; Apple US$99/yr (no individual waiver). Both stores show the developer's legal name publicly.
- **Android:** new apps target API 36; AAB uploads; 16 KB page-size support required for updates from 2027-02-01.
- **iOS:** Xcode 26 now; Xcode 27 / iOS 27 SDK from April 2027; practical minimum iOS 15.
- **Play testing gate (new personal account):** a closed test with **≥12 testers opted in for 14 consecutive days** before production access. Budget about 3–4 weeks.
- **TestFlight:** the first external build needs review; builds expire after 90 days.
- **Privacy:** a privacy-policy URL is mandatory on both stores even with zero data collection. "No data collected" holds only if the build ships **no analytics or crash SDKs**, so none are bundled.
- **Ratings:** the IARC and Apple questionnaires are mandatory; fantasy violence → Apple 9+ (infrequent) or 13+ (frequent).
- **Families risk:** Play may treat a cute-creature game with youthful art as child-directed, which would require Families Policy compliance; store art and listing must be deliberate.
- **IP:** copycat and impersonation bans make the original-IP rule a store requirement (no Pokémon names, creatures, sprites, music or look).
- **EU trader status** must be declared on both stores; a free hobby game points to non-trader.
- **Open:** whether the Play testing gate applies per app or per account; the exact age rating; whether Xcode Cloud works with no Mac at all.

### Release work still open
*Source: [How are Mendvale's Android and iOS builds made and released?](issues/17-builds-and-release-pipeline.md)*
*Source: [What are the game's title and the in-world name for Creatures?](issues/06-naming-and-branding.md)*

- **Open:** filling the licence ledger (`assets/LICENCES.csv`), including the Public Pixel and Tiny5 fonts.
- **Open:** store listings (avoid a child-directed look unless targeting Families; the listing leads with "raised, not rolled"; subtitle in §1).
- **Open:** privacy-policy hosting.
- **Open:** recruiting ≥12 Play closed testers, lined up before the first Vertical-slice beta.
- **Open:** the EU trader-status declaration (the human's call).
- **Open:** a manual trademark search for "Mendvale" and "Verdling" (USPTO classes 9, 28 and 41, EUIPO, WIPO, both app stores and itch.io) before release; a failed name is a strings-and-listing change only.
- **Out of scope:** online features, monetisation, platforms beyond Android and iOS.

## 7. Still open

These areas need deciding before the spec is complete. Each is now an open ticket on the [map](map.md); [Reassemble the spec](issues/36-reassemble-spec.md) folds their answers in.

| Area | What's settled | What's open |
|---|---|---|
| **Per-species design** | The roster's structure (§3): 34 lines, budgets, Type spread, archetypes, batch order. The 144-move list (§2). | The **method** each line is designed by: [How is one evolution line designed and reviewed?](issues/28-line-design-method.md) (including the Trait effect list and stat numbers per archetype). Authoring the 34 lines themselves is content work against the spec (§8). |
| **Creature art production** | Sizes, frames, palette, drawing order, the placeholder mapping and the ledger's `placeholder` column (§5). | Who draws the Creatures, the tools, the per-sprite workflow and review. |
| **Audio and music** | Each Restoration stage may change an Area's music and ambient track (§4). | Where $0 audio comes from (licences as strict as art's), musical style, the track list and the SFX list. |
| **Settings and accessibility** | The save skeleton and the separate `settings.json` (§6). The settings named so far (§5). English-only `tr()` strings. | Colour-blind support (Type colours need icons or labels too), a large-text mode, localisation (Public Pixel covers 98 languages), and the final settings list. |
| **Quality and release** | The test strategy and the build pipeline (§6). | Filling the licence ledger (fonts included), store listings (avoiding a look aimed at young children unless targeting Families), privacy-policy hosting, recruiting 12+ Play closed testers before the vertical-slice beta, the trader-status declaration, and a manual trademark and store search for "Mendvale" and "Verdling". The listing leads with "raised, not rolled". |
| **Tuning gaps** | The tuning tables exist as data (§6). | Starting values no ticket gives: Status countdown lengths, Poison's damage and how it ramps, how much Burn lowers Power; the XP curve and level-gap split constants; the catch % formula's factors and HP curve; the respawn delay for wild Creatures; the nickname length limit; the `signature` move band and the band lint tolerance; the stage-swap ring width; what challenge mode's fourth Boss AI tier does; the Trait effect list. Most can be set while building their module. Trait effects need a decision. |
| **Data gaps** | — | Where a line's shared level-up list and per-line Trait conditions live (there's a species record but no line record); the save field for a Boss rematch's once-per-day readiness; each Boss's target shopping list for the economy balance check; the full event command list; whether a missing sprite counts as a placeholder for the production gate; exits between Areas beyond the spoke and connector chains (left to map drawing). |
| **Store facts** | Settled by [What exactly do Google Play and Apple require of Mendvale's accounts and rating?](issues/27-store-facts.md): the Play closed test applies to every app, Apple 13+, Play 13+ age groups, non-trader on both, an Admin-role API key, privacy policy on GitHub Pages. | The listing itself: [How is Mendvale listed on the stores, and who tests it?](issues/34-store-listing-and-testers.md) |

### Conflicts settled
The 7 conflicts found while assembling this spec were settled by [Which way do the spec's seven conflicts go?](issues/25-spec-conflicts.md) and are written above as current rules: Snare vs fleeing (§2), Collection log Rarity (§3), wild evolved forms (§3), town payoffs (§4), the region record (§4), the finale's flag (§4) and OFL fonts (§5).

## 8. Out of scope

- **Online features** (trading, PvP, leaderboards, accounts, servers): offline single-player first; save format should merely not preclude them.
- **Monetisation** (ads, IAP, paid release): hobby/free release.
- **Platforms beyond Android + iOS** (PC, web, consoles).
- **Use of Pokémon IP or ripped assets** in any form.
- **Money sinks** (cosmetics, Sanctuary decor): v1 accepts that late-game money piles up, per [What items exist, and how does the economy work?](issues/14-items-and-economy.md); a fit for a later walkable Sanctuary.

**Content work, not spec.** These are implementation slices, built against this spec, not decisions left open in it:
- drawing each Area's map ([How is the region laid out?](issues/18-region-layout.md))
- writing every event and each Area's per-stage NPC lines ([What is Mendvale's story, and which beat sets each flag?](issues/22-story.md))
