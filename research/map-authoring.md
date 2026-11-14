# Research: Which tool authors Area maps, and how do they become content data?

Ticket: [`.scratch/mendvale/issues/19-map-authoring.md`](../.scratch/mendvale/issues/19-map-authoring.md) (on branch `grilling/bosses-and-gating`)
Researched: 2026-11-14. Versions, dates and repo activity below are as of that date.
Method: primary sources only (official docs, the tools' and importers' repos, release notes, licence files, and engine and editor source code where the docs are silent). Every claim carries a numbered citation from the [Sources](#sources) list. Lines marked **Analysis** are my judgement, not something a source states. One community forum thread is cited and labelled as such.

Context taken as fixed: Godot 4.7.x and typed GDScript with `untyped_declaration` and `unsafe_*` warnings as errors (ticket 09); the pure core owns the overworld grid and never reads a scene (ADR 0002); content is JSON with permanent IDs, baked by `tools/bake_content` into one `content.bundle.json` with the linter as the build gate (ADR 0001); 16×16 Ninja Adventure tiles and Restoration shown as tile swaps spreading from a focal point (ticket 10); the stage bundle contents from ticket 12; Blight barriers and the reachability linter from ticket 15.

## TL;DR

**Recommendation: author Area maps in Tiled 1.12.x, saved as `.tmj` (JSON, CSV tile data) inside one Tiled project that defines a custom class for every marker kind. `tools/bake_content` reads the `.tmj` directly as JSON and bakes the `AreaGrid` into the bundle. For the visuals, vendor the YATI importer (MIT) so Godot turns the same file into `TileMapLayer`s at import time.**

- The map file is text an agent can edit and review. Tiled writes tile layers one map row per line in both TMJ and TMX [T5][T6], and objects carry a class plus typed custom properties [T3][T4].
- The core and linter never touch Godot or the importer. The bake parses plain JSON whose format Tiled documents [T3].
- Both the editor and the importer are maintained. Tiled 1.12.2 shipped 2026-05-27 [T1]. YATI 2.2.9 shipped 2026-10-04 and says it is "tested … with Godot 4.7.2 and Tiled 1.12.2" [Y1][Y2].

**Runner-up: Godot's own `TileMapLayer` scenes** (what ADR 0001 and ticket 09 currently say). They need no third-party tool, and Ninja Adventure ships a Godot 4 project [N1]. The catch is that Godot 4.7 stores each layer's tiles as **one base64 blob of 12-byte binary records** [G3][G4]. An agent can't read, hand-edit or meaningfully diff it, and large layers become one very long line that merge tools choke on [G7]. Pick it only if agents will always paint tiles through scripts (`set_cell`) and review the *baked* JSON rather than the scene.

**Not recommended: LDtk.** It has the nicest data model for this game (IntGrid layers, typed entity fields, a published JSON Schema) [L3][L4]. But the editor hasn't released since 1.5.3 on 2024-01-15 [L1][L2], and the only Godot 4 importer last released 2.0.1 on 2024-09-19. That importer has an open report of failing on Godot 4.7.1, with the fix still unreleased on `main` [L6][L7].

## Versions checked (2026-11-14)

| Tool | Current release | Licence | Activity |
|---|---|---|---|
| Godot `TileMapLayer` | Godot 4.7.2 (engine pinned by ticket 01) | MIT (engine) | Built in; `TileMap` is deprecated in favour of it [G1][G2] |
| Tiled | 1.12.2 (2026-05-27); 1.12.0 2026-03-13 [T1] | Editor and plugins GPL; libtiled and tmxrasterizer BSD-2 [T2] | Last push 2026-11-11 [T1] |
| YATI (Tiled → Godot 4) | GDScript 2.2.9 (2026-10-04) / C# 2.2.10 (2026-10-05); needs Godot ≥ 4.3 [Y1][Y2] | MIT [Y1] | Last commit 2026-10-05; "Support is active" [Y1][Y3] |
| Tiled's built-in Godot 4 exporter | Ships with Tiled since 1.10 [T7] | GPL (Tiled plugin) [T2] | Last change 2024-02-28 [T8] |
| LDtk | 1.5.3 (2024-01-15) [L1] | MIT [L1] | Since then only CI and build fixes (last 2026-10-06) [L2] |
| godot-ldtk-importer (heygleeson) | 2.0.1 (2024-09-19); badge "Godot 4.1+", "LDtk 1.4.1" [L5][L6] | MIT [L5] | Last commit 2025-02-02; open 4.6 and 4.7 import issues [L6][L7] |

## Comparison table

Ratings: ++ strong, + adequate, − weak, −− blocker-level concern. They apply to *this* project: agent-authored, a pure-core grid, a JSON bundle, typed GDScript.

| Criterion | Godot `TileMapLayer` scene | Tiled `.tmj` (+ YATI for visuals) | LDtk `.ldtk` (+ godot-ldtk-importer) |
|---|---|---|---|
| Importer licence and health | ++ none needed [G1] | + YATI MIT, released Oct 2026, tested on 4.7.2 [Y1][Y2] | − MIT, but no release since Sep 2024; 4.7.1 failure open [L5][L7] |
| Editor health | ++ Godot itself | ++ 1.12.2, May 2026 [T1] | −− no release since Jan 2024 [L1] |
| Agent reads and edits tiles as text | −− one base64 blob per layer [G3][G4] | ++ GID arrays wrapped one map row per line [T5][T6] | + JSON, but each tile is an object `{px, src, f, t, d}` [L4]; auto-layer tiles are derived by rules (Analysis: a hand edit leaves them stale) |
| PR diff of a one-tile change | −− the layer's whole line changes [G4][G7] | ++ one line (one map row) changes [T5][T6] | + one object changes (Analysis) |
| Typed markers | + `Marker2D` nodes with exported vars or metadata; this part of the `.tscn` is text [G5] | ++ object `type` (class), with typed members, enums, and lists since 1.12 [T3][T4][T1] | ++ entities with typed fields (Int, Float, String, Bool, Color, Enum, Point, EntityRef, Tile, arrays) [L4] |
| Collision and Habitat patches | + TileSet physics or custom data layers [G6] | + a "logic" tile layer, or rectangle objects (Analysis) | ++ IntGrid layers built for exactly this [L4] |
| Restoration tile-swap layers | + one `TileMapLayer` per stage [G2] | + one tile layer per stage | + one layer per stage |
| Bake without a Godot scene | − bake must instantiate the scene headless and read cells back | ++ parse JSON with Godot's `JSON` class [G8] | ++ parse JSON; JSON Schema published [L3] |
| Headless export from the editor | n/a | + not needed (the save format is the source); CLI export needs an X server on Linux [T9] | − no CLI (Analysis) |

## Per-criterion notes

### 1. Importer licence, maintenance and Godot 4.7 support

- **Godot `TileMapLayer`** is the engine's own 2D tile node. The `TileMap` page says "Deprecated: Use multiple TileMapLayer nodes instead" [G1]. The 4.7 docs advise using several `TileMapLayer` nodes to split foreground and background [G2]. No importer is involved.
- **Tiled.** The editor and its plugins are GPL. libtiled, tmxrasterizer and tmxviewer are BSD 2-clause [T2]. **Analysis:** the GPL covers the editor binary, not the maps we save with it, and we ship no Tiled code. Releases are steady: 1.11.2 (2025-01-28), 1.12.0 (2026-03-13), 1.12.1, and 1.12.2 (2026-05-27) [T1].
- **YATI** (Yet Another Tiled Importer) is MIT and copyright 2023–2026 Roland Helmerichs [Y1]. Its README says "Tested on Windows 11 with Godot 4.7.2 and Tiled 1.12.2" and "needs Godot 4.3.0 or higher". It imports `.tmx` and `.tmj`, "all kinds of layers", "all kinds of objects", tile collisions, animations, templates and custom properties. It also offers a runtime package [Y1]. Its reference maps a tile layer to a `TileMapLayer` and a point object to a `Marker2D`. It can copy the Tiled class and object id into node metadata, and runs a user post-processor script after import [Y4]. Its author also contributed a fix to Tiled 1.12.0 itself [T1]. Known issue: Godot "may freeze (+crash)" while importing several maps unless *Use multiple threads* is turned off in the import settings [Y1].
- **Tiled's built-in Godot 4 exporter** (since 1.10) [T7] is a weaker option. Its source writes the **deprecated `TileMap` node** with `layer_N/tile_data` arrays, not `TileMapLayer` [T8][G1]. It only exports objects that have a `resPath` property naming a `.tscn` to instance [T7], and its last code change was 2024-02-28 [T8].
- **LDtk** is MIT [L1]. Its last release is 1.5.3 (2024-01-15) [L1]. Commits since then are CI and compile fixes, the latest on 2026-10-06 [L2].
- **godot-ldtk-importer** (heygleeson) is MIT. It badges "Godot 4.1+" and "LDtk 1.4.1" [L5]. Its last release is 2.0.1 (2024-09-19), and its last commit is 2025-02-02 [L6]. Two problems are open:
  - Issue #65: "LDtk Importer fails to import ldtk files in Godot 4.7.1". A commenter says the cause is fixed on `main` by #46, which is still unreleased [L7].
  - Issue #63: a Godot 4.6 parse error from type inference treated as an error [L7]. **Analysis:** that user had installed it outside `res://addons`. Godot's default `debug/gdscript/warnings/directory_rules` is `{ "res://addons": 0 }` [G9], so an add-on under `addons/` would normally escape Mendvale's warnings-as-errors.

### 2. Can an agent edit the map as text and diff it in a PR?

- **Godot `TileMapLayer`: no, not for tiles.** The `tile_map_data` property is "The raw tile map data as a byte array" (`PackedByteArray`) [G3]. In 4.7 the encoding is a 2-byte format version, then 12 bytes per cell (x, y, source id, atlas x, atlas y, alternative tile, each 16-bit) [G4]. Godot's text serializer writes a non-empty `PackedByteArray` as **one base64 string** [G4]. A one-tile change therefore rewrites part of a single line that can be hundreds of KB long. A community report on 4.5.1 describes a ~590,000-character `TileMapLayer` line that crashed kdiff3 during a merge [G7] (community, not official). Markers, by contrast, are ordinary nodes in the human-readable `.tscn` [G5], so they diff fine.
- **Tiled: yes.**
  - **TMJ:** the tile layer `data` field is an array of GIDs, `csv` by default (`base64` optional), with no compression by default [T3]. Tiled's JSON writer wraps arrays every *map-width* values, so each map row is one line [T6].
  - **TMX:** CSV data is likewise written one row per line unless "minimize output" is on [T5].
  - **Objects:** each object has a unique incremental `id`, a `name`, a `type` (the class), pixel `x`/`y`/`width`/`height`, a `point` flag, and a `properties` array whose entries carry `name`, `type`, `propertytype` and `value` [T3].
  - **Analysis:** an agent can change a tile by editing one number on one line, and add a marker by appending one JSON object. The two traps are the GID offset (`firstgid` + local id) and the flip bits in the top bits of each GID [T3]. The bake and the linter should own both.
- **LDtk: partly.**
  - IntGrid layers are an `intGridCsv` array of ints, row-major, where `0` means empty [L4].
  - Painted tiles are objects with pixel position `px`, tileset pixel `src`, flip bits `f`, tile id `t`, and editor-internal `d` [L4].
  - **Analysis:** an agent can edit IntGrid values. But auto-layer tiles (`autoLayerTiles`) are generated by editor rules [L4], so a hand edit to the IntGrid leaves the visible tiles stale until a human reopens the editor.

### 3. Can the format carry what a Mendvale map needs?

| Need | `TileMapLayer` scene | Tiled | LDtk |
|---|---|---|---|
| 16×16 Ninja Adventure tiles | Atlas TileSet; the pack ships a Godot 4 project [N1][G6] | `.tsx` tileset per sheet (one-time setup); terrain sets for floor autotiling (Analysis) | Tileset per sheet; auto-layer rules |
| Collision | TileSet physics layer, or a custom data layer `walkable` [G6] | A `logic` tile layer over a tiny "logic" tileset (wall, patch kinds), or tile custom properties (Analysis) | An IntGrid value such as `wall` [L4] |
| Habitat patches | A logic layer of patch tiles, or `Area2D` nodes | A logic tile layer, or rectangle objects of class `habitat_patch` with `patch_id` and `habitat` | IntGrid values per Habitat [L4] |
| Tile-swap layer per Restoration stage | `restore_1`…`restore_N` `TileMapLayer`s | `restore_1`…`restore_N` tile layers | `restore_1`…`restore_N` layers |
| Typed markers | `Marker2D` + script `@export`s | Object classes with typed members and enums; lists since 1.12 [T4][T1] | Entities with typed fields and `EntityRef` [L4] |
| Area exits linking to other Areas | Exported `to_area` / `to_exit` strings | Object properties (strings, or `object` refs within a map) [T3] | `EntityRef` fields [L4] |

**Analysis:** all three can carry everything. "Spreading from a focal point" needs no extra map data. The shell orders each stage's swapped cells by distance from the `focal_point` marker and plays them in rings (ticket 12). Per-stage *logic* changes (a patch appears, a barrier clears, a path opens) are best kept as markers with a `stage_from` / `stage_until` property, so one rule covers all of them.

**Tiled caveats:**
- **Class defaults aren't written into the map.** Custom types are saved in the Tiled project file, not in each map [T4][T10]. An object shows inherited values in grey and stores only what it overrides [T4]. "Resolve object types and properties", which writes the effective values, is an *export* option, not a save option [T11]. **Analysis:** the bake must read class defaults from the `.tiled-project` file, or the linter must require every marker field to be set explicitly. The second is simpler and safer for agents.
- **The manual lags 1.12.** It still lists array properties as a "future extension" [T4], but the 1.12.0 changelog says "Added support for lists in custom properties (#1493)" [T1]. Treat lists as new and test them before relying on them.

### 4. The bake: map → `AreaGrid` → bundle

**Recommended flow (Tiled):**

1. **Source files:** `content/areas/<area_id>.json` (stages, native species and so on, as in ticket 12) and `maps/<area_id>.tmj`, one Tiled project `maps/mendvale.tiled-project`, and `.tsx` tilesets for the Ninja Adventure sheets.
2. **`tools/bake_content`** (headless Godot, as in ticket 09) parses each `.tmj` with Godot's `JSON` class [G8]. **No scene, no importer and no `.godot/imported` output is involved.** It emits into `content.bundle.json`:
   - grid size and the walkable bitmap per stage, built from the `logic` layer plus barrier and path markers by stage
   - patch cells per stage, by `patch_id`
   - markers by permanent ID: kind, cell (pixel x / 16, y / 16), and typed fields
   - the per-stage swap-cell lists for the shell to animate
3. **The core** (`AreaGrid`) is built from the bundle only, so ADR 0002 holds. Scenario tests can use small hand-written `.tmj` fixtures.
4. **The shell** instances the YATI-imported scene for the visuals only, with the `restore_N` layers hidden until their stage. The core never sees it.

**What the linter can check** (Analysis; the rules come from tickets 12, 14 and 15):

- **Each marker is well-formed:**
  - the `type` is in a closed list: `rest_point`, `shop`, `item_spot`, `forage_spot`, `hidden_site`, `trainer`, `area_challenge`, `blight_barrier`, `area_exit`, `focal_point`, `habitat_patch`, `npc`
  - every required field is present and of the right type
  - the marker sits on the grid (x and y are multiples of 16)
- **References resolve:** `trainer_id` → a trainer record, `site_id` → the Area's `find_site` Mendings, `to_area` / `to_exit` → an existing exit with a matching return exit, and `patch_id` → a spawn table for every stage in which the patch exists.
- **Counts match:** exactly one `focal_point` for an Area with stages; at most one `area_challenge` (ticket 12); at least one `rest_point` reachable from each entry, if that becomes a rule.
- **Barriers:** every `blight_barrier` has `clears_at_stage: 1`. No `stage_from ≥ 2` marker opens a critical-path exit (ticket 12: "Only stage 1 may open critical-path routes").
- **Reachability:** the grid flood fill from each entry reaches every marker that should be reachable at its stage. Ticket 15's region walk then runs over the baked exits and barriers.
- **Level bands:** a trainer's or Area challenge's level comes from its record, so the map only provides *which Area* the record sits in, and the ticket 15 band check runs on that.
- **Tiles:** every GID resolves to a tileset, and every cell on a `restore_N` layer swaps a tile that exists on the layer below.

**If the runner-up (`TileMapLayer`) is chosen**, step 2 instead instances each scene headless and reads cells with `get_used_cells`, `get_cell_source_id`, `get_cell_atlas_coords` and `get_cell_tile_data` (for custom data) [G3]. It then walks the `Marker2D` children. This works, but the bake now depends on scene loading and the editor's import cache. **Analysis:** agents should then edit maps only through a checked-in `@tool` or headless script calling `set_cell` [G3], and review the baked JSON (or a per-Area grid dump the bake writes) in PRs, never the `.tscn` blob.

### 5. Why not avoid the importer entirely?

**Analysis:** the shell could paint `TileMapLayer`s at runtime from the bundle with `set_cell` [G3]. For an atlas tileset, Tiled's local tile id maps straight to atlas coordinates (`id % columns`, `id / columns`). That removes YATI, at the cost of a small painter script (tile animations and flips by hand) and visual tile data in the bundle. Keep this as the **fallback if YATI stalls**. YATI is MIT, so it can also be vendored and patched.

## Recommendation and trade-offs

**Choose Tiled 1.12.x with `.tmj` maps (CSV), one Tiled project holding a custom class per marker kind, a bake that reads `.tmj` directly, and YATI 2.2.x (vendored under `addons/`) for the Godot-side visuals.**

Why:
1. **Agents can author and review maps as text.** One map row is one line [T5][T6], and markers are small typed JSON objects [T3]. The `TileMapLayer` blob can't be read or reviewed [G3][G4][G7].
2. **The core and linter stay Godot-free.** The bake reads a documented JSON format [T3], so the importer only affects how maps *look*.
3. **Every piece is maintained and licence-safe.** Tiled 1.12.2 is from May 2026 [T1], YATI 2.2.9 from October 2026 and tested on 4.7.2 [Y1][Y2], and both import and editor code are MIT or BSD where we would ever touch them [T2][Y1].
4. **Humans get a full editor.** Tiled has terrain autotiling, templates for marker presets and class colours for marker kinds [T4], so a human can still paint maps comfortably.

Trade-offs accepted:
- **Two tools instead of one.** The human installs Tiled, and a Tiled project plus `.tsx` tilesets must be set up once for the Ninja Adventure sheets. The pack's bundled Godot 4 project doesn't carry over [N1].
- **Class defaults live in the project file** [T4][T10]. The linter should require explicit values on every marker (or the bake merges defaults).
- **YATI import quirks:** turn off multi-threaded import [Y1]. Imported scenes live in the import cache, so CI must run `godot --headless --import` before tests and export (already in the ticket 01 CI recipe).
- **GID and flip-bit handling** must live in one bake function with tests [T3].
- **This changes ADR 0001 and ticket 09.** Their "Maps" text says maps "stay Godot `TileMapLayer` scenes" with a loader extracting `AreaGrid`. Under this recommendation the source of truth becomes the `.tmj`, the bake extracts `AreaGrid`, and the `TileMapLayer`s are a derived import.

**When to pick `TileMapLayer` scenes instead:** if a third-party editor and importer is judged too much risk, or the human wants to paint inside Godot with the Ninja Adventure project's ready-made TileSets [N1]. Then make agents edit tiles only through scripts and review baked JSON, not scenes.

**When to reconsider LDtk:** only if it ships a new release and its Godot importer releases a 4.7-compatible version. Its IntGrid and typed entity model [L4] is otherwise the best match for collision, patches and markers.

## Open risks

- **YATI is effectively one maintainer** [Y1][Y3]. Mitigation: vendor it (MIT), or fall back to a runtime `set_cell` painter (section 5).
- **Tiled list properties are new in 1.12** and not yet in the manual [T1][T4]. Avoid them in v1 marker schemas unless tested.
- **Not verified here:** whether YATI's import is deterministic enough for exported builds to be reproducible, and how it behaves on macOS (its README tests only on Windows [Y1]). A short spike, importing one Ninja Adventure Area on the Mac that builds iOS, would settle both.
- **Large maps:** Tiled's row-per-line output keeps diffs small, but a 100-wide map is still a 100-number line per row. **Analysis:** keep Areas to screen-scale chunks (the render shows about 11 × 12 tiles, ticket 10), and use exits rather than one huge map.

## Follow-ups for other tickets

- **ADR 0001 / ticket 09 "Maps" section:** record that maps are Tiled `.tmj`, baked into `AreaGrid` data in the bundle, with `TileMapLayer`s as a derived import.
- **AGENTS.md:** keep maps as `.tmj` with CSV encoding and "minimize output" off; never hand-edit `firstgid`; markers must use a class from the project file and set every field.
- **Content linter:** add the marker rules in section 4.
- **Ticket 18 (region layout):** Area size limits and the exit-pairing convention.

## Sources

Godot
- [G1] TileMap class (4.7 docs), deprecation note: https://docs.godotengine.org/en/stable/classes/class_tilemap.html
- [G2] Using TileMaps (4.7 docs): https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.html
- [G3] TileMapLayer class (4.7 docs): `tile_map_data`, `get_used_cells`, `get_cell_*`, `set_cell`: https://docs.godotengine.org/en/stable/classes/class_tilemaplayer.html
- [G4] Godot source at tag `4.7-stable`: `scene/2d/tile_map_layer.cpp` (`get_tile_map_data_as_array`, 2-byte format + 12-byte cells): https://github.com/godotengine/godot/blob/4.7-stable/scene/2d/tile_map_layer.cpp ; `core/variant/variant_parser.cpp` (non-compat `PackedByteArray` written as one base64 string): https://github.com/godotengine/godot/blob/4.7-stable/core/variant/variant_parser.cpp
- [G5] TSCN file format: https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html
- [G6] Using TileSets (custom data layers, physics layers, scene collections, terrains): https://docs.godotengine.org/en/stable/tutorials/2d/using_tilesets.html
- [G7] Godot Forum, "Large TileMapLayer nodes cause issues with merging git branches" (community, not official): https://forum.godotengine.org/t/large-tilemaplayer-nodes-cause-issues-with-merging-git-branches/136301
- [G8] JSON class: https://docs.godotengine.org/en/stable/classes/class_json.html
- [G9] ProjectSettings, `debug/gdscript/warnings/directory_rules` default: https://docs.godotengine.org/en/stable/classes/class_projectsettings.html

Tiled
- [T1] mapeditor/tiled releases (1.12.2 2026-05-27; 1.12.0 changelog incl. "Added support for lists in custom properties (#1493)"): https://github.com/mapeditor/tiled/releases ; 1.12 announcement: https://www.mapeditor.org/2026/03/13/tiled-1-12-released.html
- [T2] Tiled `COPYING` (per-component licences): https://github.com/mapeditor/tiled/blob/master/COPYING
- [T3] JSON map format reference (tile layer `data`/`encoding`/`compression`, object fields, properties, GIDs): https://doc.mapeditor.org/en/stable/reference/json-map-format/
- [T4] Custom properties, custom types, classes and inheritance: https://doc.mapeditor.org/en/latest/manual/custom-properties/ (source: https://github.com/mapeditor/tiled/blob/master/docs/manual/custom-properties.rst)
- [T5] Tiled source, TMX writer (CSV row-per-line unless minimized): https://github.com/mapeditor/tiled/blob/master/src/libtiled/mapwriter.cpp
- [T6] Tiled source, JSON plugin (`setAutoFormattingWrapArrayCount(map width)`): https://github.com/mapeditor/tiled/blob/master/src/plugins/json/jsonplugin.cpp ; writer: https://github.com/mapeditor/tiled/blob/master/src/plugins/json/qjsonparser/json.cpp
- [T7] Godot 4 export manual page (since 1.10; `resPath` objects; limitations): https://doc.mapeditor.org/en/latest/manual/export-tscn/
- [T8] Tiled source, Godot exporter (`type="TileMap"`, `layer_N/tile_data`) and its commit history: https://github.com/mapeditor/tiled/blob/master/src/plugins/tscn/tscnplugin.cpp ; https://github.com/mapeditor/tiled/commits/master/src/plugins/tscn/tscnplugin.cpp
- [T9] Exporting (`--export-map`; needs an X server / `xvfb-run` on Linux): https://github.com/mapeditor/tiled/blob/master/docs/manual/export.rst
- [T10] Projects (custom types saved in the project): https://github.com/mapeditor/tiled/blob/master/docs/manual/projects.rst
- [T11] Preferences, export options ("Resolve object types and properties", "Minimize output"): https://github.com/mapeditor/tiled/blob/master/docs/manual/preferences.rst

YATI
- [Y1] Kiamo2/YATI README (Godot 4.7.2 / Tiled 1.12.2 tested, ≥ 4.3, features, limitations, MIT): https://github.com/Kiamo2/YATI
- [Y2] YATI releases (2.2.9 2026-10-04, 2.2.10 2026-10-05, 1.7.1 for 4.2): https://github.com/Kiamo2/YATI/releases
- [Y3] YATI commit history: https://github.com/Kiamo2/YATI/commits/main
- [Y4] YATI reference (Tiled → Godot element mapping, metadata options, post-processor): https://github.com/Kiamo2/YATI/blob/main/Reference.md

LDtk
- [L1] deepnight/ldtk repository and releases (MIT; 1.5.3 2024-01-15): https://github.com/deepnight/ldtk ; https://github.com/deepnight/ldtk/releases
- [L2] deepnight/ldtk commit history: https://github.com/deepnight/ldtk/commits/master
- [L3] LDtk JSON page (JSON 1.5.3, `JSON_SCHEMA.json`, QuickType): https://ldtk.io/json/
- [L4] LDtk JSON documentation (`intGridCsv`, `gridTiles`, `autoLayerTiles`, tile instance, entity instance, field types, `externalLevels`): https://github.com/deepnight/ldtk/blob/master/docs/JSON_DOC.md
- [L5] heygleeson/godot-ldtk-importer README (Godot 4.1+, LDtk 1.4.1, features, MIT): https://github.com/heygleeson/godot-ldtk-importer
- [L6] godot-ldtk-importer releases (2.0.1 2024-09-19) and commits: https://github.com/heygleeson/godot-ldtk-importer/releases ; https://github.com/heygleeson/godot-ldtk-importer/commits/main
- [L7] godot-ldtk-importer issues #65 (fails on Godot 4.7.1) and #63 (4.6 parse error): https://github.com/heygleeson/godot-ldtk-importer/issues/65 ; https://github.com/heygleeson/godot-ldtk-importer/issues/63

Assets
- [N1] Ninja Adventure Asset Pack page (CC0, 16×16, includes a Godot 4 project; last update 2026-03-29): https://pixel-boy.itch.io/ninja-adventure-asset-pack
