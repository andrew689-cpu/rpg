# Does the YATI importer turn a Tiled Area into Godot tile maps on the Mac, the same way every time?

Type: task
Status: resolved
Blocked by: 19

## Question

Before the map pipeline from ticket 19 is relied on, check its one unverified link on the Mac that builds iOS:
- Install Godot 4.7.2 and Tiled 1.12.2. Vendor YATI 2.2.9 into a throwaway project under `addons/`, with multi-threaded import turned off.
- Draw one small Area in Tiled from Ninja Adventure 16×16 tiles: ground, detail, a logic layer, two `restore_N` layers, and a few typed markers.
- Run `godot --headless --import` twice from a clean `.godot/` folder. Record whether the `TileMapLayer`s and markers come out right, and whether the two imports give identical output.
- Record the result. If YATI fails or the output differs between runs, that confirms the fallback from ticket 19 (the bake still reads the `.tmj`, and a small script paints the layers at runtime with `set_cell`).

The agent can drive this alone if Godot and Tiled can be installed from the command line. Otherwise it hands the human a checklist.

## Answer

Done by the agent alone on the Mac (2026-11-14). Evidence and rerun steps: branch `spike/yati-import-check`, folder `spikes/yati-import-check/` (README, map, scripts, renders). Tools came from their GitHub releases, no Homebrew: Godot 4.7.2 (SHA-512 checked), Tiled 1.12.2 and YATI 2.2.9 GDScript. YATI 2.2.10 changes only the C# build.

**What was done:** Tiled itself drew a 20 × 18 Area through its script API (`Tiled --evaluate`). It uses Ninja Adventure tiles and has:
- `ground`, two hidden `restore_N` layers, `detail` (with 38 flipped or rotated cells) and a 50 %-opacity `logic` layer whose tiles carry a `data_kind` property
- 10 typed markers from a `.tiled-project`, including an enum and a trainer left at its class defaults

The map references four external `.tsj` tilesets. It was imported with `godot --headless --import` from a clean `.godot/` several times, and with multi-threaded import off (`editor/import/use_multiple_threads=false`; YATI has no thread option of its own).

**Result: YATI works on macOS, so the `set_cell` fallback is not needed.**
- **Correct:** all 853 cells match the `.tmj` (tile, atlas coords, flip and transpose), the logic tile property becomes a TileSet custom-data layer, and every marker keeps its position, class, id and typed properties. YATI also fills in class defaults from the project file. A real Godot render matches Tiled's `tmxrasterizer` render with **0 differing pixels** at stage 0 and at stage 2.
- **The same every time in substance:** two clean imports differ only in the per-node `unique_id=` values, which Godot 4.7 randomises on every save. With those stripped, the scenes are identical. Texture UIDs and sub-resource ids were stable. So imported scenes, and builds made from them, are not byte-reproducible.

**Facts later tickets depend on:**
1. **Embedded-texture trap.** If a tileset PNG has no `.import` sidecar yet when a map imports, YATI embeds the raw pixels in the scene: 2.1 MB instead of 20 KB, though it looks the same. A fresh clone with committed `.import` files always gets the small version. The bloated one stays cached until the map's content changes.
2. **Import failures exit 0.**
   - **Broken `.tmj` JSON** logs `SCRIPT ERROR` and `ERROR: Error importing`. Godot then writes **`valid=false` into the `.tmj.import`** and silently never re-imports that map again, even once it's fixed and `.godot/` is wiped. Only restoring the `.import` recovers.
   - **A missing `.tsj`** logs `ERROR: Tileset file … not found` and `Import finished with 1 error.` with **no `SCRIPT ERROR` line**, and still writes a partial scene.
   - Leaked-RID errors at exit are noise.
3. **Rectangle markers import as `StaticBody2D` + `CollisionShape2D`**, and point markers as `Marker2D`.
4. **A `restore_N` layer drawn above `detail` hides it**, because a swap layer can only cover what's below it. How stages change detail tiles is still open.
5. **Tiled tooling:**
   - Tiled's CLI can draw and save maps headless (`--evaluate`), but its script API can't open a tileset asset there ("Editor not available").
   - `--export-map json` re-saves a map and keeps its external tilesets.
   - `--resolve-types-and-properties` writes class defaults into an exported map.
   - Tiled escapes `/` as `\/` in JSON.

**Consequences, recorded in the Maps section of ticket 09 ("What is the technical architecture?"):** the `check` job must
- require a committed `.import` for every asset and reject any `valid=false`
- scan the import log for `Error importing` and `Import finished with`, not only `SCRIPT ERROR`
- fail if any `.tmj` lacks an imported scene, or if an imported map scene contains an `Image` sub-resource

The new ticket 23, "What exactly does an Area's `.tmj` contain?", takes items 3–5: layer order and restore semantics, marker schemas, and what the shell keeps from the import.
