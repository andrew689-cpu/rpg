# How is the region laid out?

Type: grilling
Status: resolved
Blocked by: none

## Question

Specify the Medium region's map as a list of Areas (see `GLOSSARY.md` and the answers to tickets 05, 10, 12, 14 and 15):
- **The Area list per Chapter:** how many towns, routes and dungeons; their rough size in screens (portrait, about 11 × 12 tiles visible); and their connections, adding up to the ~19 h critical path in ticket 15.
- **Boss home Areas:** where each of the 8 Bosses stands, matched to its theme Type (a Tide Boss by water), and which 1–2 routes its flag restores.
- **Blight barriers:** where each one stands, which flag clears it, and the story-beat flags that restore Areas no Boss covers (including the first route after the starter pick).
- **The Habitat kinds list:** the terrain kinds Creatures belong to. This sets the Habitat Lures (ticket 14) and Habitat patches (ticket 08).
- **Per-Area furniture:** Rest points (reachable in Blighted Areas too), one shop per town, focal points, and which Areas have 0 stages (interiors, untouched towns).
- **Optional paths** that only stages 2+ open, and where Area challenges and hidden sites sit, at the level bands from ticket 15.
- How the layout leaves room for a second region (the Large scale) without moving anything.

Already fixed:
- **Ticket 15:** 5 Chapters of 1 / 2 / 3 / 1 / 1 Bosses with ace levels 12 / 22 / 34 / 44 / 52. Each Chapter's Bosses are reachable without beating each other. Gates are Blight barriers only. Boss order comes from reachability (ADR 0003). The Areas before each Boss must offer at least 2 catchable species that hit its Type for 2×.
- **Ticket 12:** each restorable Area has a focal point, a tile-swap layer per stage, 3–6 native species, its trainers, at most one Area challenge, hidden sites, and optional paths that only stages 2+ open.
- **Ticket 14:** item-spot and Forage-spot markers. Blighted Areas have few Forage spots, and stages 2+ add more.

Placing each species in Areas waits for this ticket and the roster ticket (16). The tool used to draw Areas is ticket 19.

Added from ticket 16 (How is the Creature roster structured?):
- **Lines by debut Chapter:** 7 lines first appear in Ch 1, 5 in Ch 2, 5 in Ch 3, 4 in Ch 4 and 1 in Ch 5 or postgame. Three-stage lines debut only in Ch 1–2. Shade lines debut in Ch 2–3, Lumen in Ch 3–4, and Frost by Ch 3.
- **Before Boss 1:** a **Gale** line and a **Flame** line must be the **two most Common species** in the Areas before Boss 1 (the Boss 1 gate's bot party uses them), and at least 2 Wild lines live there for Boss 1's team.
- **Wild starters:** all 12 starter base forms appear **Rare in Chapter 2–3 Areas**, each matching its Habitat, at most 2 per Area.
- **Rare one-offs:** 2 set encounters at **final-stage focal points**, one in Chapter 4 and one postgame.
- Each species has one home Habitat kind, so the Habitat kinds list sets every species' Habitat field as well as the Habitat Lures.
- No starter line is on a trainer or Boss team before Chapter 3, and branch forms are in no spawn table.

## Answer

Resolved by grilling with the human (2026-11-14). Builds on ticket 05 (pillars), ticket 08 (catching), ticket 10 (art direction), ticket 12 (Restoration), ticket 14 (economy), ticket 15 (Bosses and gating), ticket 16 (roster) and ticket 19 (map authoring). Terms are defined in `GLOSSARY.md`: Area, Hub town, Spoke, Landmark, Interior, Habitat kind, Blight barrier, Rest point, Focal point. **Every count and size is data with a starting value, tuned in playtesting.** Area IDs below are working IDs. Display names, and the region's own name, belong to the Story & world fog.

### Shape: a hub per Chapter
- Each Chapter has one **hub town**. One **spoke** leads from it to each of that Chapter's Bosses. A spoke is a chain of 1–3 Areas ending at the Boss's **landmark**.
- A **connector route** leads on from the hub to the next Chapter's hub, and a **Blight barrier** blocks it.
- Chapters 4 and 5 are each one spoke off their own hub. The home town sits before Chapter 1's single path.
- Spokes can't reach each other on the critical path, so ADR 0003's rule that "each Boss in a Chapter is reachable without the others" holds by construction. Stages 2+ add optional shortcuts so the region doesn't feel like a tree (see Optional paths).
- The Region map reads **bottom to top** in portrait: home in the southern vale, the finale at its northern heart.

### Area kinds
The Area record has a closed `kind` field:

| Kind | What it is | Screens (≈ 11 × 12 tiles each) | Stages |
|---|---|---|---|
| town | shop, inn and houses | 1–2 | 1–2 (the home town has 0) |
| route | outdoor ground between places | 3–5 | 3 |
| dungeon | cave, deep forest or ruin; its 1–3 floors are sections of **one `.tmj`** joined by internal warps, with one Restoration track | 4–8 | 3 |
| landmark | the small site where a Boss (or a one-off) waits, shaped by its Type | 1–2 | 2 |
| interior | a house, shop or inn: 0 stages, a `parent` Area, no Region-map panel, the parent's music | < 1 | 0 |

- **A hard cap of 64 × 64 tiles per `.tmj`**, checked by the linter. Longer stretches split into two Areas.

### Towns and Restoration
- **Towns have 1–2 stages.** Stage 1 comes from a flag (see Flags). Stage 2, where present, comes from town-style Mendings: local trainers or a hidden site.
- **This amends ticket 12:** an Area needs 3–6 native species **only if it has Habitat patches**. Towns have none, so they list no native species and no `register_natives` Mending.
- **The home town has 0 stages.** It was never Blighted, which is part of the story.

### Habitat kinds
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

- Each kind has one **Habitat Lure** (ticket 14), so there are 8. Each species' home Habitat (ticket 16) is one of these.
- Time of day and weather stay separate spawn conditions.

### The region
**33 Areas** plus interiors: **7 towns, 12 routes, 6 dungeons, 8 landmarks**. That's about 35 minutes of critical path per Area against ticket 15's ~19 h.

| Ch | Area | Kind | Habitat kinds | Screens | Stages |
|---|---|---|---|---|---|
| 1 | `home_town` | town | – | 2 | 0 |
| 1 | `route_1` | route | Meadow | 3 | 3 |
| 1 | `route_2` | route | Woodland, Wetland | 4 | 3 |
| 1 | `warren` (Boss 1, Wild) | landmark | Meadow | 2 | 2 |
| 2 | `route_3` (connector) | route | Meadow, Wetland | 4 | 3 |
| 2 | `hub_2` | town | – | 2 | 2 |
| 2 | `route_4` | route | Woodland | 4 | 3 |
| 2 | `deepwood` | dungeon | Woodland | 6 | 3 |
| 2 | `elder_tree` (Boss 2, Grove) | landmark | Woodland | 2 | 2 |
| 2 | `route_5` | route | Wetland, Coast | 4 | 3 |
| 2 | `cove_town` | town | – | 1 | 2 |
| 2 | `tide_shrine` (Boss 3, Tide) | landmark | Coast | 2 | 2 |
| 3 | `route_6` (connector) | route | Meadow, Crag | 5 | 3 |
| 3 | `hub_3` | town | – | 2 | 2 |
| 3 | `route_7` | route | Crag | 4 | 3 |
| 3 | `old_mine` | dungeon | Cavern | 7 | 3 |
| 3 | `quarry` (Boss 4, Stone) | landmark | Crag | 2 | 2 |
| 3 | `route_8` | route | Meadow, Ruins | 4 | 3 |
| 3 | `sunken_works` | dungeon | Ruins | 6 | 3 |
| 3 | `storm_tower` (Boss 5, Volt, 2v2) | landmark | Ruins | 2 | 2 |
| 3 | `route_9` | route | Crag, Snowfield | 5 | 3 |
| 3 | `peak_village` | town | – | 1 | 2 |
| 3 | `ice_cave` | dungeon | Cavern, Snowfield | 5 | 3 |
| 3 | `glacier` (Boss 6, Frost) | landmark | Snowfield | 2 | 2 |
| 4 | `route_10` (connector) | route | Coast, Meadow | 5 | 3 |
| 4 | `harbour` (hub 4) | town | – | 2 | 2 |
| 4 | `route_11` | route | Coast, Crag | 4 | 3 |
| 4 | `observatory` | dungeon | Ruins | 6 | 3 |
| 4 | `lighthouse` (Boss 7, Lumen) | landmark | Coast | 2 | 2 |
| 5 | `route_12` (connector) | route | Crag, Snowfield | 5 | 3 |
| 5 | `outpost` (hub 5) | town | – | 1 | 2 |
| 5 | `blight_heart` | dungeon | Ruins, Cavern | 8 | 3 |
| 5 | `source` (Boss 8, finale) | landmark | Ruins | 2 | 2 |

- **Spokes:**
  - Chapter 1: `route_2` → `warren`.
  - Chapter 2: `route_4` → `deepwood` → `elder_tree`, and `route_5` → `cove_town` → `tide_shrine`.
  - Chapter 3: `route_7` → `old_mine` → `quarry`; `route_8` → `sunken_works` → `storm_tower`; and `route_9` → `peak_village` → `ice_cave` → `glacier`.
  - Chapter 4: `route_11` → `observatory` → `lighthouse`.
  - Chapter 5: `blight_heart` → `source`.
- **Spoke towns:** `cove_town` and `peak_village` give long spokes a shop.
- **Habitat coverage:** every Habitat kind is reachable by Chapter 3. Chapters 2–3 hold 11 Areas with Habitat patches, which at 2 per Area is room for 22 wild starters against the 12 needed (ticket 16). Chapter 1 offers Meadow, Woodland and Wetland for its 7 lines.
- **Room for a second region:**
  - Area IDs are **flat and globally unique**, with no region prefix.
  - A **region record** lists its Areas.
  - `harbour` has the one **dormant exit**: a ferry, visible but "not running yet". A second region adds its Areas and wakes that exit with an event, moving nothing.
  - The Region map and the Restoration % are per region.

### Flags and Blight barriers
- **`starter_chosen`** restores `route_1` and clears its barrier at the home town's edge. It's the first Restoration the player sees, so it doubles as the tutorial.
- **A Boss flag** restores **its whole spoke**: the landmark plus every Area between it and the hub (at most 4), spoke towns included. **This amends ticket 15's "plus the 1–2 routes that led to it".**
- **`chapter_N_open`** restores **the hub being left and the connector route out of it**, which clears that connector's barrier. Each hub is lived in Blighted and heals as its Chapter closes. The flag is set:
  - for `chapter_2_open`: by the `boss_1` win event. Chapter 1's hub is `home_town`, which has 0 stages, so this flag restores only `route_3`.
  - for `chapter_3_open`: by the combined event once `boss_2` and `boss_3` are both set
  - for `chapter_4_open`: by the combined event once `boss_4`, `boss_5` and `boss_6` are all set
  - for `chapter_5_open`: by the `boss_7` win event
- **`boss_8`** restores its spoke plus `outpost`.
- There are exactly **5 critical-path barriers**: on `route_1`, `route_3`, `route_6`, `route_10` and `route_12`. Spokes have none. Players walk into each new Chapter's Areas while they're still Blighted (ticket 15).

### Level bands
- **The linter derives each Area's Chapter:** an Area belongs to the Chapter in which it first becomes reachable on the walk from the new-game state. Connector routes therefore take the new Chapter's band (`route_3` is Chapter 2, wild levels 11–18).
- Spawn tables, trainers and Area challenges are checked against that band (ticket 15), with the +1–2 allowance at the top for later stages. **The Chapter is never written on the Area** (ADR 0003).

### Furniture
- **Rest points:**
  - **Every town:** an inn interior holding the Rest point.
  - **Every dungeon:** a camp at its entrance, plus one deeper in if it has 3 floor sections.
  - **Every landmark:** a camp at its entrance, so a lost Boss fight retries a few steps away.
  - **Routes of 4+ screens:** a mid-route camp.
  - Camps work while Blighted (a lantern, a tent).
  - The linter checks that **no critical-path cell is more than one Area exit from a Rest point**.
- **Interiors per town:** an inn, a shop and 1–3 houses.
- **Shops:** one per town (ticket 14), so 7 in all. Camps sell nothing.
- **Focal points:** one in every Area with stages (towns included). None in the home town or interiors.
- **0-stage Areas:** `home_town` and every interior.

### Landmarks
- **2 stages.** Stage 1 comes from the Boss flag. Stage 2 comes from Mendings: a small Habitat patch with 3 native species, and a hidden site.
- A Boss's **rematch** (ticket 15) is fought at its landmark.
- **The 2 rare one-offs** (ticket 16) sit at final-stage focal points:
  - the Chapter 4 one at `observatory` (stage 3, Ruins)
  - the postgame one at `source` (stage 2, after the finale)

  Neither is Shade or Lumen.

### Optional content
- **Area challenges:** one in **every route and dungeon** (18 in all), and none in towns or landmarks. Each sits at its Chapter's challenge level (14 / 24 / 36 / 46 / 54, ticket 15).
- **Hidden sites:** **1–2 per route, town and landmark; 2–3 per dungeon.**
- **Optional paths (stages 2+ only):**
  - every spoke gets **one stage-2 shortcut** back to its hub, or between neighbouring spokes in Chapter 3
  - every dungeon gets **one stage-2+ side pocket** holding a hidden site or an item spot
- **Trainers:** about 3–5 per route and dungeon, and 1–2 per town. They make up each Area's "beat the trainers here" Mending.

### Linter checks added
1. `kind` is one of the 5 kinds. Interiors have 0 stages and a `parent`. Only `home_town` and interiors have 0 stages.
2. No `.tmj` is over 64 × 64 tiles.
3. Areas with Habitat patches list 3–6 native species. Areas without patches list none.
4. Every Habitat patch and every species' home Habitat uses one of the 8 kinds.
5. The Rest-point distance rule.
6. Level bands come from each Area's derived Chapter.
7. Exactly one dormant exit per region.

### Follow-ups
- **Ticket 12** amended: native species are required only on Areas with Habitat patches.
- **Ticket 15** amended: a Boss flag restores its whole spoke.
- **Ticket 16:** the 8 Habitat kinds now set each species' home Habitat. Species placement in Areas can go ahead with the per-line design work.
- **New ticket 22**, "What is Mendvale's story, and which beat sets each flag?", graduated from the Story & world fog.
- **Display names** for the region and its Areas move to ticket 22. Drawing each Area's map is implementation work for the slices, past this map's destination.
