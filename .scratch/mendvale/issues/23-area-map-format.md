# What exactly does an Area's `.tmj` contain?

Type: grilling
Status: resolved
Blocked by: none

## Question

Pin down Mendvale's Area map format, so agents can draw Areas and the bake, linter and shell can be written against it (see `GLOSSARY.md`, the answers to tickets 09, 12, 18, 19 and 20, and ADRs 0001 and 0002):
- **Layers:** the fixed list of layer names and their order. How a `restore_N` layer swaps tiles: which layer each swap lands on, and how a stage changes or removes **detail** tiles, such as a dead tree becoming a living one. Ticket 20 found that a `restore_N` layer drawn above `detail` hides it, and ticket 12 has the shell swap cells outward in rings anyway.
- **Logic tiles:** the closed set of logic kinds (walls, the 8 Habitat patch kinds from ticket 18, ledges, water, anything else), and whether Habitat patches are logic tiles, rectangle markers, or both.
- **Marker classes:** for every kind (Rest point, shop, item spot, Forage spot, hidden site, trainer, NPC, Area challenge, Blight barrier, Area exit and internal warp, focal point, Habitat patch), the shape (point or rectangle), the fields and their types, and how `stage_from` / `stage_until` work. Avoid Tiled 1.12 list properties (ticket 19).
- **Class defaults:** the linter requires every field to be set, or the bake merges project defaults in, or maps are exported with `--resolve-types-and-properties` (ticket 20).
- **Tilesets and files:** one external `.tsj` per Ninja Adventure sheet, the folder layout, and committed `.import` sidecars (ticket 20).
- **What the shell takes from the YATI import:** the import options per map, and whether the `markers` layer is dropped by a YATI post-processor. Ticket 20 found that rectangle markers import as `StaticBody2D` physics bodies, while the core owns markers through the bake (ADR 0002).

## Answer

Resolved by grilling with the human (2026-11-14). Builds on ticket 08 (catching), ticket 09 (architecture), ticket 11 (controls), ticket 12 (Restoration), ticket 14 (economy), ticket 18 (region layout), ticket 19 (map authoring), ticket 20 (YATI check) and ticket 22 (story), and on ADRs 0001 and 0002. Terms are defined in `GLOSSARY.md`. Tuning numbers (ring width, `sight` default, wander radius) are data with a starting value.

### Layers
The map has these layers, in draw order:

| Layer | Kind | Drawn | Holds |
|---|---|---|---|
| `ground` | tile | yes | floor, paths, water surfaces |
| `detail` | tile | yes | trees, rocks, fences, tall-grass looks, barrier drawings |
| *(actors)* | — | — | the shell draws the player, follower, NPCs, trainers and wild Creatures here; not a Tiled layer |
| `overhead` | tile | yes, above actors | tree tops and roofs the player walks behind |
| `logic` | tile | no (50% opacity in Tiled) | one logic kind per cell (see below) |
| `stage_1`, `stage_2` … | group | no | one per Restoration stage, each holding sub-layers `ground`, `detail`, `overhead`, `logic` |
| `markers` | object | no | every marker object |

- **A stage group is a change set, not a drawn layer.** It holds only the cells that change at that stage. An empty cell means "no change", and the reserved **`erase`** tile (from `logic.tsj`) removes the base tile. This is how a dead tree becomes a living one, or brambles disappear.
- **Stages stack:** stage 2's changes apply on top of stage 1's. Stage 0 is the base layers alone. There is one group per stage the Area has (ticket 12), and the linter checks the count.
- **The shell plays the swap** (ticket 12's "tiles swap outward in rings"): it copies the changed cells onto the base layers in rings by **Chebyshev distance** from the focal point, with the ring width as tuning data. On entering an Area already at stage S, it applies stages 1…S at once.
- **The bake precomputes the grid per stage.** It folds `logic` and each `stage_N/logic` into the walkable cells, logic kinds and patches for every stage, so the core never replays layers.

### Logic kinds
A closed list, carried as a `kind` property on each tile of `logic.tsj`. An empty cell is plain walkable floor. A new kind needs code; a new map doesn't.

| Kind | Rule |
|---|---|
| `wall` | blocks everything |
| `water` | blocks walking (no surfing in v1: there are no field moves) |
| `counter` | blocks walking; interaction passes through it by one cell |
| `ledge_s`, `ledge_e`, `ledge_w` | one-way hop in that direction. No north ledge: the region reads bottom to top, so ledges only speed up the trip home |
| `meadow` … `ruins` | the 8 Habitat kinds from ticket 18; walkable Habitat-patch cells |
| `erase` | only in stage groups: removes the base cell |

### Habitat patches
- **Patches are logic tiles only.** There is no `habitat_patch` marker.
- **A patch is a 4-connected run of cells of one Habitat kind**, found by the bake for each stage. Its ID is assigned by the bake and isn't permanent, which is fine because spawn state is never saved (ticket 09).
- A stage's `logic` sub-layer adds or removes patches (a refilled pond), with no extra machinery.
- Spawn-table conditions key on the Habitat kind (ticket 08). Two patches of the same kind in one Area share a spawn table; an Area that needs two different mixes uses two Habitat kinds.
- Ticket 08's "up to 4 per Habitat patch" applies to each connected run.
- **Wild Creatures stay on their patch's cells.** A `curious` one approaches the player only up to the patch's edge, and a `shy` one flees within it. A patch's edge is where the danger stops.
- The look (tall grass, shallows) is drawn separately on `ground`/`detail`. A lint **warning** fires on a patch cell with nothing drawn on it.

### Markers

**Identity.** A marker's local name is the Tiled object's built-in **Name**. The bake forms its ID as **`<area_id>.<name>`**. Names are snake_case and unique within the Area. Saves refer to marker IDs (item spots taken, hidden sites found, the Rest point last used), so they're **permanent once released**, and a rename goes through `content/aliases.json`.

**Shared fields** on every class except `focal_point` and `blight_barrier`, where the linter forbids them:

| Field | Type | Default | Meaning |
|---|---|---|---|
| `stage_from` | int | 0 | active from this Restoration stage |
| `stage_until` | int | 0 | inactive from this stage on; **0 means no end** |
| `flag_on` | string | `""` | active only once this story flag is set |
| `flag_off` | string | `""` | inactive once this story flag is set |

A marker is active when all four hold. An NPC that moves between stages is two markers with the same `npc_id` and non-overlapping stage ranges. Per-stage dialogue lives in the NPC record, not on the map. Story placement uses the flags (the rival stands outside the inn until `starter_chosen`, via `flag_off`).

**Classes**, a closed list. A new class needs code. `Dir` is a Tiled string enum: `up`, `down`, `left`, `right`. No Tiled 1.12 list properties are used.

| Class | Shape | Fields | Notes |
|---|---|---|---|
| `player_start` | point | `facing: Dir` | Exactly one per region, in `home_town`. |
| `exit` | rect, 1 tile thick | `to_area: string`, `to_exit: string` (the local name there), `facing: Dir`, `dormant: bool` | Area exits, doors, map-edge roads and internal warps (`to_area` = own Area). |
| `rest_point` | point | `facing: Dir` | Is the Lantern-keeper: the shell draws them, talking to them rests, and after a loss the player returns to the cell they face. |
| `shop` | point | `facing: Dir` | The clerk. Stock comes from the town record (for an interior, its `parent`). |
| `trainer` | point | `trainer_id: string`, `facing: Dir`, `sight: int` (default 3; 0 = talk only), `movement` (`still`/`turn`) | Counts toward `defeat_trainers`. |
| `npc` | point | `npc_id: string`, `facing: Dir`, `movement` (`still`/`turn`/`wander`, within 2 tiles) | The NPC record holds the sprite and per-stage dialogue event. |
| `encounter` | point | `encounter_id: string`, `facing: Dir` | Any set encounter that's touched or talked to: the Area challenge, a Boss, a rare one-off. No sight line. The shell draws the lead's sprite. |
| `item_spot` | point | `item_id: string`, `count: int` (default 1) | Visible, taken once (ticket 14). There are no invisible items. |
| `forage_spot` | point | `forage_table: string` | Regrows each in-game day. Restoration adds more through `stage_from` (ticket 14). |
| `hidden_site` | point | `requires_species: string` (default `""`) | Its ID is the `find_site` ID (ticket 12). Flavour comes from the string `site.<id>`. Flag conditions use `flag_on`. |
| `blight_barrier` | rect | none | Blocks its cells while the Area is below stage 1, and clears at stage 1; a `stage_1` erase removes its drawing. Text comes from `barrier.<id>`. |
| `focal_point` | point | none | Sits on the drawn spring or shrine. Exactly one per Area with stages, none otherwise. Interacting opens the Mending checklist (ticket 12). |
| `trigger` | rect | `event_id: string` | Runs an event when the player steps in. "Once only" is a `flag_off` the event sets. |
| `interact` | point | `event_id: string` | Signs, bookshelves, statues: runs an event when faced and interacted with. |
| `camera_zone` | rect | none | The camera clamps to the zone holding the player. |

Weather, music, spawn tables, native species and shop stock stay in the Area JSON, never on the map.

### Exits and warps
- **An exit fires when the player steps into** one of its cells.
- **Arrival:** the player lands on the paired exit at the **same offset along it** (clamped), then is placed **one cell inward** in that exit's `facing` direction, facing that way. Standing on an arrival cell never fires anything, and wide exits line up.
- **Map-edge roads** are a 1-tile-thick `exit` along the edge row, not a special "off the edge" rule.
- **Internal warps** (stairs between dungeon floor sections) are exits within one Area. They cut to the new `camera_zone` with a short fade.
- **The dormant ferry:** a `dormant: true` exit is drawn, shows "not running yet" text and never fires. Only dormant exits may leave `to_area` empty. A second region gives it a target and a `flag_on` that its event sets, and drops `dormant`, in that content patch.

### Blocking and interaction
- **Occupants block their cell while active:** `rest_point`, `shop`, `trainer`, `npc`, `encounter`, `item_spot` (until taken) and `forage_spot` (always, even when picked). **Beaten trainers keep blocking:** they stay standing. Wild Creatures and the follower also block, but they're runtime state, not markers.
- **Not blocking:** `exit`, `trigger`, `camera_zone`, `focal_point`, `hidden_site`, `interact` (the last three usually sit on drawn `wall` cells).
- Occupancy that depends on stages is baked per stage. Occupancy that depends on flags is resolved by the core at runtime, since flags aren't known at bake time.
- **Interaction (`confirm`)** is with the occupant, `interact`, `hidden_site` or `focal_point` on the cell the player faces. A `counter` cell passes interaction through to the next cell, so a clerk behind a counter can be reached.
- **Tap-to-move** (ticket 11) paths to the nearest walkable cell facing the target, then interacts.

### Camera zones
- Zones may not overlap, and every walkable cell must sit in one. **A map with no zones** uses the whole map as one zone.
- A zone smaller than the screen (an interior about 8 × 6 tiles in an 11 × 12 view) is centred, with black around it.
- Zones are camera-only and carry no gameplay. The Region map stays one panel per Area.

### Class defaults
- **The bake merges class defaults** from the committed `.tiled-project`, as YATI already does on import. Maps stay as Tiled saves them, without default values.
- Required reference fields (`to_area`, `to_exit`, `trainer_id`, `npc_id`, `encounter_id`, `item_id`, `forage_table`, `event_id`) default to `""`, and the linter rejects them empty. The one exception is `to_area` on a dormant exit.
- **The `.tiled-project` is the one schema** for marker classes and enums. A unit test pins it to the classes and fields the bake expects, so the two can't drift.

### Files and IDs
- **One `.tmj` per Area, interiors included:** `content/maps/<area_id>.tmj`. The file name *is* the link to the Area record, which needs no map field (this replaces ticket 09's "Area JSON refers to its map by ID" with a naming convention, like art). Dungeon floors stay sections of one file (ticket 18).
- `content/maps/mendvale.tiled-project` holds the classes and enums.
- `content/maps/tilesets/`: one external `.tsj` per Ninja Adventure sheet, plus `logic.tsj`.
- `assets/tiles/<sheet>.png`, each with a committed `.import` sidecar (ticket 20) and a `LICENCES.csv` row. Swapping art means replacing a PNG on the same grid.
- **Map settings the linter checks:** orthogonal, 16 × 16 tiles, not infinite, CSV encoding, at most 64 × 64 (ticket 18), and tilesets only from `content/maps/tilesets/`.

### What the shell takes from the YATI import
- **One shared import preset for every map:** `add_class_as_metadata=false`, `add_id_as_metadata=false`, `tiled_project_file` set to the committed project, and `post_processor` set to `src/game/overworld/map_import_post.gd`. The linter checks every `.tmj.import` against the preset.
- **The post-processor, run on import:**
  - deletes the `markers` object layer, so no `StaticBody2D`s or `Marker2D`s reach the scene; the core owns markers through the bake (ADR 0002)
  - deletes `logic` and every `stage_N/logic`, since the bundle holds the grid
  - keeps each `stage_N` group's drawn sub-layers, hidden, as cell sources for the swap
  - sets `overhead` to draw above the actor layer
  - strips any physics, navigation and occlusion from the TileSets
- **At runtime, the shell:**
  - instances the imported scene for the Area
  - draws actors itself from the bundle's markers and `GameSession` state
  - plays stage swaps by copying cells (source, atlas coords, alternative/flip) from the hidden `stage_N` layers onto the base layers
- **A gdUnit test** imports a fixture map and asserts the output contains only these nodes, so a YATI upgrade that changes the import fails loudly.

### What the bake emits
For each Area, the `AreaGrid` in `content.bundle.json` holds:
- the size
- for each stage: the logic kind per cell, the walkable cells and the patches (kind plus cells)
- every marker with its ID, class, cells (a point is one cell; a rect is its cells), resolved fields and the shared activity fields
- the camera zones

Tile art is never in the bundle. The bake decodes GIDs and flip bits itself.

### Agents editing maps
Agents may hand-edit a `.tmj` as JSON, adding markers or changing CSV cells. The bake and linter are the safety net. Nothing has to re-save through Tiled's CLI, since CI has no Tiled. An optional `tools/tiled_resave.sh` (`--export-map json`) normalises formatting locally. **`AGENTS.md` gains:**
- CSV encoding only, with "minimize output" off
- never renumber `firstgid`
- every marker uses a class from the project file
- bump the map's `nextobjectid` when adding an object

### Linter checks added
1. Map settings (above), and the `.tmj.import` matches the shared preset.
2. Layer names and order match the table. There is one `stage_N` group per stage the Area has, each with only the four known sub-layers. `erase` appears only inside stage groups.
3. Every `logic` tile is one of the closed kinds.
4. Marker classes are from the closed list, names are snake_case and unique within the Area, and IDs are unique across the region.
5. Required reference fields are set and resolve: trainers, NPCs, set encounters, items, Forage tables, events, Areas and exits.
6. The shared activity fields are absent on `focal_point` and `blight_barrier`. Markers sharing an `npc_id` have non-overlapping stage ranges.
7. Exits pair up both ways, paired exits have the same length, and every arrival cell is walkable at every stage where the exit is active. There is exactly one dormant exit per region (ticket 18), and only it may leave `to_area` empty.
8. Exactly one `player_start` per region. Exactly one `focal_point` per Area with stages, and none in 0-stage Areas.
9. No two blocking occupants share a cell at any stage, and no occupant stands on `wall` or `water`.
10. Camera zones don't overlap and cover every walkable cell.
11. The Restoration rules from tickets 12 and 18 are run against the baked grid: flood-fill reachability treats every occupant (beaten trainers included) and every uncleared barrier as blocking; barriers clear only at stage 1; only stage 1 opens critical-path routes; Mendings are completable at the previous stage; and the Rest-point distance rule holds.
12. **Warning:** a Habitat-patch cell with nothing drawn on it.

### Follow-ups
- **Ticket 09** amended (Maps): patches are logic tiles, IDs come from object Names, the post-processor and preset, map files are named by Area ID, and the bake merges class defaults (replacing "every field set explicitly").
- **Ticket 08** amended: a patch is a connected run of one Habitat kind, and wild Creatures never leave it.
- **Ticket 12** amended: the tile-swap layer is a stacked change set per stage.
- **`GLOSSARY.md`:** Habitat patch sharpened.
- No new tickets. Drawing the Areas is implementation work for the slices.
