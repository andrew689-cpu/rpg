# What is the technical architecture?

Type: grilling
Status: resolved
Blocked by: 01, 07, 08

## Question

Given the chosen engine and battle/catching rules: module boundaries (overworld, battle, party, content, save, UI), the data-driven content format for Creatures/moves/items/maps (so Medium → Large needs no code changes), save-file format and versioning, scene/state flow, and the test strategy that lets agents build modules independently.

Added from tickets 10 and 11:
- Input reduces to five actions (`move(dir)`, `walkTo(tile)`, `confirm`, `back`, `menu`), shared by touch, gamepad and keyboard.
- Screen layouts are data (portrait now, landscape later; left-handed mirroring is a layout setting).
- Render is 180 pixels wide internally, with integer scaling and the height extended to fill the screen.
- Battle animations are code effects on still sprites, with an off setting.
- Art is swapped through data: tiles, 16×16 map sprites, and 64×64 front and back battle sprites, all within a locked 53-colour palette.

Added from ticket 12 (How does Restoration change an Area?):
- Area data holds `native_species[]` and `stages[]`. Each stage has a trigger (`story_flag` or `mendings_required: K`), `mendings[]`, a spawn table, a tile layer and focal point, and Habitat-patch, NPC, path, shop, weather and music changes, plus an optional payoff Creature.
- Mending kinds are a closed list in code (`register_natives`, `defeat_trainers`, `defeat_challenge`, `find_site`); new Areas need no code.
- The save stores raw facts (registrations per Area, trainers beaten, sites found, story flags), the highest stage reached per Area, and a pending-presentation queue. On load the stage is the higher of stored and computed, so a content patch never moves it backwards.
- A content linter must check that every Mending for stage N is completable at stage N−1, and that only stage 1 opens critical-path routes.

Added from ticket 13 (How does Bond shape a Creature?):
- Species data holds `evolution` (a `level`, plus either `into` or a `branch` with `axis`, `ends` and `into[]`) and `bond_moves[]` (`{rank, move}`). Areas hold a `default_habitat`; set encounters may override it.
- Leaning axes are a closed list in code (`style`, `type`, `habitat`, `time`); new species need no code.
- The save stores `bond_points` and `needles` (`{axis: {ends, value}}`) per Creature. Bond rank and a pending evolution offer are derived, never stored, so retuning thresholds can't take a rank away.
- Bond tuning (rank thresholds, points per battle kind, needle range and step, warning window) is global data.
- The content linter must check that every branch is reachable (Type ends learnable, Habitat ends reachable, Style has both a Power and a Focus move before evolving), 2–4 Bond moves per species at ranks 1–5, and at most one branch point per line.

Added from ticket 06 (What are the game's title and the in-world name for Creatures?):
- Godot project name and app ID: `mendvale`, `io.github.andrew689cpu.mendvale` (permanent, the same on both stores).
- Code and data use generic identifiers (`creature`, `trainer`, `lure`, `sanctuary`, `collection_log`, `mending`). Every in-world name (Verdling, Mender, Offering, Haven, Almanac) lives only in localisation strings, so a rename is a string change.

## Answer

Resolved by grilling with the human (2026-11-14). Builds on ticket 01 (Godot 4.7.x, typed GDScript), tickets 07, 08, 12 and 13 (rules and their data and save notes above), ticket 10 (render and art) and ticket 11 (input and layouts). Uses the generic glossary terms from `GLOSSARY.md`; in-world names live only in strings. Two decisions are recorded as ADRs: [`docs/adr/0001-json-content-bundle.md`](../../../docs/adr/0001-json-content-bundle.md) and [`docs/adr/0002-pure-core-owns-the-rules.md`](../../../docs/adr/0002-pure-core-owns-the-rules.md).

### Core and shell
- **Every game rule lives in a pure core** under `src/core/`: typed GDScript classes extending `RefCounted`, with no `Node`, scene tree, `Input` or autoload access. Content, the RNG and the clock are passed in. A lint rule fails CI if `src/core/` mentions `Node`, `get_tree`, `Input` or an autoload.
- The **presentation shell** under `src/game/` reads core state, sends player intent, and plays the events the core returns. It holds no rules.
- **The core owns the overworld simulation.** Grid positions and movement of the player, follower, NPCs and visible wild Creatures (wander, curious, shy) advance on discrete ticks against the `AreaGrid`. The overworld scene only interpolates sprites between cells and plays effects. Tick rate and in-game clock speed are tuning data.
- **Illegal intents never crash.** A move with too little Energy, a switch while Snared or a step into a wall returns `Rejected{reason}` and leaves state unchanged. `assert` is reserved for invariants in debug builds.

### Core modules

Each module has a small interface, a `README.md` stating it, and its own tests through that interface.

| Module | Interface (gist) | Hides |
|---|---|---|
| `content` | `ContentDB.load(bundle) -> db`; typed read-only lookups by ID; `ContentLinter.check(db) -> Array[Issue]` | parsing, schemas, cross-references, aliases |
| `battle` | `Battle.create(setup, content, rng)`, `legal_actions(slot)`, `preview(action)` (damage range % of HP, effectiveness, catch %, status %, turn order), `resolve_turn(actions) -> Array[BattleEvent]`, `outcome()` | damage, Types, Statuses, Energy, stat stages, turn order, catch roll, N-per-side targeting |
| `ai` | `BattleAI.choose(view, side, tier, rng) -> actions` | the Wild, Trainer and Boss tiers (and challenge mode's fourth); it sees only a read-only `BattleView` with the same information the player has |
| `growth` | `Growth.after_battle(creatures, result, content) -> Array[GrowthEvent]` | XP split by level gap, level-ups, newly learnable moves, Bond points, needle nudges, evolution offers |
| `world` | `Restoration.stage(area, facts, content)`, `Spawner.roll(patch, conditions, rng)`, `Clock` | K-of-M Mendings, "higher of stored and computed", weighted spawn tables, time of day |
| `events` | `EventRunner.start(event_id)`, `step(input) -> requests` | the closed command list, flags, branching |
| `save` | `SaveCodec.encode(state)`, `SaveCodec.decode(json) -> state`; `SaveStore` seam | the migration chain, `.bak` fallback, unknown IDs |
| `session` | `GameSession` intent methods (`step(dir)`, `walk_to(cell)`, `tick()`, `interact()`, `start_battle(...)`, `submit_turn(...)`, `rest()`, menu intents …), each returning events | coordinates everything above; the **only writer** of save state |

- **Presentation calls only `GameSession`**, plus `ContentDB` for display lookups. It never reaches the other core modules directly.
- **`SaveStore` is the only external seam** with two adapters: a file adapter (`user://`) and an in-memory adapter for tests. Other seams stay internal until a second adapter appears.
- `GameSession.step(dir)` returns events such as `Moved`, `Bumped`, `EncounterStarted`, `TrainerSpotted` and `Warp`. `tick()` advances wild and NPC movement and the clock.

### Battle
- **One turn in, an event list out.** Events are plain data (`MoveUsed`, `Damage{amount, effectiveness}`, `StatusApplied`, `Fainted`, `CatchAttempt{accepted}`, `XpGained` …). The battle scene plays them as text, bar animations and code effects, and skips the visuals when battle animations are off.
- The player's side and the AI submit through the same `resolve_turn`.

### Determinism
- **All randomness comes from an injected, seeded `Rng` wrapper.** A lint rule fails CI on `randf`, `randi` or `randomize` anywhere else.
- Each battle gets its own seed, so **setup + seed + the actions submitted** reproduce it exactly. Each spawn roll is also seeded. The per-save seed from ticket 08 stays the root.

### Content
- **JSON, one file per record**: `content/species/<id>.json`, `content/moves/<id>.json`, and likewise for Traits, items, Areas, spawn tables, trainers, set encounters and events. Each kind has a **JSON Schema**. Global tuning tables (type chart, rarity weights, Bond thresholds, XP curve, clock speed, move bands) are one JSON file each.
- **Permanent snake_case IDs** (`grove_sprout`, `cinder_nip`), separate from display names and never reused or changed after a release. The save, spawn tables, evolutions and Mendings all refer to records by ID. A rare rename goes through `content/aliases.json`. The Collection log's display number is a separate field.
- **Baked at build time.** `tools/bake_content` (a headless Godot script) merges `content/**/*.json` into one `content.bundle.json`, running the full linter and **failing the build on any lint error**. The game and the tests read only a bundle (the real one or a fixture). The bake runs in CI before tests and export.
- *Added 2026-11-14 by ticket 21 ("How is the move list structured?"):* a move record holds `type`, `category`, `tier`, `pool`, `power`, `cost`, `accuracy`, `target`, `priority`, `crit_pct`, `effects[]` (from a closed list of 11 effect kinds) and `anim` (from a closed list of code effects). `content/tuning/move_bands.json` holds the damage constant `k` and the tier bands. A move's card text is generated from its effects; strings hold only `move.<id>.name` and an optional `move.<id>.flavour`. The move lint rules are listed in ticket 21.
- **Lint covers:** schemas; every ID resolves; the Restoration rules from ticket 12, the Bond rules from ticket 13 and the move rules from ticket 21; events (flags read but never set, battles that point at missing trainers); missing or orphaned string keys; the licence ledger; sprite palette and size.

### Maps
*Amended 2026-11-14 by ticket 19 ("Which tool authors Area maps, and how do they become content data?"); the original said maps were Godot scenes.*
- An Area's map is a **Tiled 1.12 `.tmj` file**, the source of truth. It has CSV-encoded tile layers (ground, detail, a logic layer for collision and Habitat patches, and one `restore_N` tile-swap layer per Restoration stage). **Typed marker objects**, one custom class per kind in the Tiled project file, carry IDs for exits, Habitat patches, trainers, NPCs, item and Forage spots, hidden sites, Blight barriers, the focal point, Rest points and shops.
- The core never reads a scene. `tools/bake_content` parses the `.tmj` as plain JSON into a plain **`AreaGrid`** (walkable cells, patch cells, marker positions by ID) inside `content.bundle.json`, for the core and the scenario tests.
- For drawing, the **YATI** importer (MIT, vendored in `addons/`) generates the `TileMapLayer`s from the same `.tmj` on import. CI runs `godot --headless --import`, with multi-threaded import off. If YATI fails, a small script paints the layers at runtime with `set_cell`.
- **Lint covers markers:** only allowed kinds; **every field set explicitly** (Tiled keeps class defaults outside the map); every ID resolves; exits pair up; one focal point; barriers clear only at stage 1; flood-fill reachability; level bands. Avoid Tiled 1.12 list properties until tested.
- Area JSON refers to its map by ID.
- *Added 2026-11-14 by ticket 20 ("Does the YATI importer turn a Tiled Area into Godot tile maps on the Mac, the same way every time?"):* YATI 2.2.9 imports correctly on macOS (pixel-identical to Tiled), so the `set_cell` fallback stays a contingency only. Imports are deterministic apart from Godot's random node `unique_id`s, and failures exit 0. The `check` job therefore adds three import gates:
  1. Every asset has a committed `.import` sidecar, and none contains `valid=false`. A missing sidecar makes YATI embed the tileset pixels; a `valid=false` one silently stops the map ever re-importing.
  2. The import log is scanned for `Error importing` and YATI's `Import finished with`, as well as `SCRIPT ERROR`.
  3. Every `.tmj` has an imported scene, and no imported map scene contains an `Image` sub-resource.
  The exact map format is ticket 23, "What exactly does an Area's `.tmj` contain?".
- *Amended 2026-11-14 by ticket 23 ("What exactly does an Area's `.tmj` contain?"), which holds the full format:*
  - **Layers:** `ground`, `detail`, `overhead` (drawn above actors) and `logic`, plus one hidden `stage_N` group per Restoration stage holding only the changed cells (an `erase` tile removes one). The shell copies them onto the base layers in rings; the bake precomputes the grid per stage.
  - **Habitat patches are logic tiles, not markers:** a patch is a 4-connected run of one Habitat kind, with a bake-assigned ID.
  - **15 marker classes**, each identified as `<area_id>.<object Name>`, permanent once released, with shared `stage_from` / `stage_until` / `flag_on` / `flag_off` fields.
  - **Class defaults are merged by the bake** from the committed `content/maps/mendvale.tiled-project`, replacing "every field set explicitly" above; empty reference fields are lint errors.
  - **Files:** `content/maps/<area_id>.tmj`, so the Area JSON needs no map field (replacing "Area JSON refers to its map by ID" above); tilesets in `content/maps/tilesets/`.
  - **Import:** one shared YATI preset with a post-processor (`src/game/overworld/map_import_post.gd`) that deletes the `markers` and `logic` layers, hides the stage groups and strips physics. The shell draws actors from the bundle.

### Events and dialogue
- NPC talk, story beats, gifts and cutscenes are **JSON arrays of steps from a closed command list** (`say`, `choice`, `set_flag`, `if_flag`, `give_item`, `give_creature`, `battle`, `move_actor`, `wait`, `heal` …), run by `EventRunner`. They emit presentation requests the same way battles emit events.
- A new kind of step means adding a command in code. A new event is content only.
- *Amended 2026-11-14 by ticket 22 ("What is Mendvale's story, and which beat sets each flag?"): each slot on a set encounter's side has an optional `controller` (`player` by default, or an AI tier), so an AI ally can fight beside the player in a tag battle. The linter checks that such a side has exactly one `player` slot.*

### Art and strings
- **Content records hold no asset paths.** Art is found by convention from the ID: `assets/creatures/<id>/front.png`, `back.png` and `map.png`; `assets/items/<id>.png`; and so on. A built-in placeholder is used when a file is missing, so swapping art means dropping in a file. A missing sprite is a lint **warning**, not an error.
- The bake checks that every asset file has a row in **`assets/LICENCES.csv`** (source, licence, author, URL), and that every sprite uses only the locked 53-colour palette at the right size (64×64 battle, 16×16 map).
- **Every player-facing string goes through `tr()`.** Keys are derived from IDs (`species.grove_sprout.name`, `move.cinder_nip.name`), and the text lives in `strings/en.csv` (Godot's CSV translation import). In-world terms are keys too (`term.creature` → "Verdling"), so a rename is a single CSV edit. Only English ships in v1.

### Scenes and screens
- **One persistent `Main` scene** owns a single `GameSession` and a **screen stack**: Title → Overworld, with Battle, menus and the Restoration sequence pushed on top. The overworld stays loaded underneath a battle, and Areas swap as child scenes of the overworld.
- **Autoloads hold no game state:** only `Content` (read-only, loaded once), `Settings` and `Audio`.
- **Every screen is a controller script plus one or more layout scenes.** The controller handles behaviour and the five input actions; layouts are Control nodes with anchors. Only `portrait` is built in v1; `landscape` is a reserved slot. Left-handed mirroring is a layout flag that flips horizontal anchors and the command-deck order.
- Touch, gamepad and keyboard all reduce to the five input actions (`move(dir)`, `walkTo(tile)`, `confirm`, `back`, `menu`) before reaching a controller.

### Save
- **One slot**, as JSON in `user://` with a top-level integer `version`. **`settings.json` is separate.**
- **Migrations:** loading runs a chain of pure functions (`v1→v2`, `v2→v3` …), each tested on its own.
- **Atomic writes:** write `save.tmp`, then rename. The previous save is kept as `save.bak` and used if the main one fails to parse.
- **The save holds facts only:**
  - seed, clock, current Area, cell and facing
  - Creature instances, each with a permanent instance id: species, level, XP, learned and equipped moves, Trait, current HP, nickname, `bond_points`, `needles`, and its place (Party slot or Sanctuary)
  - bag, money, story flags
  - Restoration facts, highest stage per Area, and the pending-presentation queue
  - trainers beaten, rare one-off Creature state, Collection log entries (seen, caught, Traits and branches discovered, where-found facts)
- **Derived values are never stored:** stats, Bond rank, current Restoration stage, pending evolution offers and spawn state are always recomputed. A test fails if any `SaveCodec` field can be computed from the others.
- **Unknown IDs** (content removed in a patch) are kept but ignored and never crash a load.
- **When it writes:** on OS pause (`NOTIFICATION_APPLICATION_PAUSED`), at autosave points (after battles, on Area changes, after the Restoration sequence) and on manual Save.
- **Mid-battle resume:** a pause during battle also stores an `in_battle` record (setup + seed + actions so far), and resume replays it silently to the same turn. A replay that no longer matches (a patch changed a move) falls back to the pre-battle autosave.

### Tests
- **gdUnit4.** CI gates on its JUnit XML plus a scan of the log for `SCRIPT ERROR`, never on Godot's headless exit code.
- **Three layers:**
  1. **Core unit tests** through each module's interface: most of the suite, fast, with no scenes.
  2. **Content lint** as a test (the bake's linter).
  3. **Headless scenario tests** that boot `Main` with a fixture save, drive it only through the five input actions, and assert on `GameSession` state. Many scenarios can instead run directly on `GameSession`.
- No screenshot or golden-image tests in v1.
- **Developer tools:** a dev-only debug menu, left out of release exports by a Godot feature tag. It sends debug intents through `GameSession`: warp, give a Creature or item, set a flag, set the clock, add Restoration facts, start any set encounter. **Named fixture saves** in `tests/fixtures/saves/` ("before Boss 3", "Area X at stage 2") serve both scenario tests and manual playtesting.

### Repo and agent rules
- **Layout:** the Godot project (`project.godot`) at the repo root; `src/core/<module>/`, `src/game/<screen>/`, `content/`, `strings/`, `assets/`, `tests/` (mirroring `src/`), `tools/`.
- **`AGENTS.md` rules:**
  - Godot pinned to **4.7.x**
  - typed GDScript only, with the `untyped_declaration` and `unsafe_*` warnings set to **error** in project settings
  - `.uid` files are moved and deleted together with their scripts
  - `.godot/` is never committed
  - `src/core/` stays pure
  - randomness only through `Rng`
  - display text only through `tr()`

### Left to other tickets
- CI provider, export pipeline, signing and which Mac builds iOS → "How are Mendvale's Android and iOS builds made and released?"
- Map-painting workflow → World-structure fog.
- Languages beyond English, colour-blind support and large text → Save, settings & accessibility fog.
