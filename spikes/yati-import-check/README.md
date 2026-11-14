# YATI import check on macOS (ticket 20)

Throwaway evidence for ticket 20, "Does the YATI importer turn a Tiled Area into Godot tile maps on the Mac, the same way every time?". This branch is never merged.

Run on 2026-11-14 on an Apple Silicon Mac running macOS 26.6.2. Tools, all downloaded from their GitHub releases, no Homebrew:

- Godot **4.7.2-stable** (`Godot_v4.7.2-stable_macos.universal.zip`, SHA-512 checked against `SHA512-SUMS.txt`)
- Tiled **1.12.2** (`Tiled-1.12.2_macOS-13+.zip`)
- YATI **2.2.9** GDScript (`v2.2.9-gdscript.zip`). The later 2.2.10 release is "C# specific … no change for GDScript". It isn't committed here; unzip it into `addons/` to rerun.

Tiles are Ninja Adventure (CC0) from `prototype/art-direction`, plus a 4-tile `logic.png` made by `scripts/make_logic_png.py`.

## What was built

`maps/check_area.tmj` is a 20 × 18 Area, **written by Tiled itself**: `scripts/draw_area.js` runs through `Tiled --project mendvale.tiled-project --evaluate`. It has these layers:

| Layer | Contents |
|---|---|
| `ground` | grass, path and a pond; mixes two tilesets on one layer |
| `restore_1`, `restore_2` | hidden; lush-grass swaps (stage 1 is the diamond around the focal point) |
| `detail` | trees on both edges; the right side is horizontally flipped, plus one V-flipped and one rotated tile (38 flipped cells) |
| `logic` | 50 % opacity; wall, meadow, wetland and ledge tiles with a `data_kind` tile property |
| `markers` | 7 point markers (focal_point, rest_point, 2 × trainer, item_spot, 2 × area_exit) and 3 rectangles (blight_barrier, 2 × habitat_patch with a `Habitat` enum) |

`trainer_b` deliberately leaves `facing` and `sight_tiles` at their class defaults.

The map references four external `.tsj` tilesets. Tiled's script API can't open a tileset as an asset without the GUI editor ("Editor not available"), so the script writes the map with embedded tilesets. `scripts/externalise.py` then swaps them for `{firstgid, source}` entries, and `Tiled --export-map json` re-saves the result. So the committed file is genuine Tiled 1.12.2 output.

The import options are in `maps/check_area.tmj.import`: `add_class_as_metadata`, `add_id_as_metadata` and `tiled_project_file`. `project.godot` sets `editor/import/use_multiple_threads=false`. (YATI has no thread option of its own; the README's "Use multiple threads" is this Godot setting.)

## Results

**Correct.** `check/verify.gd` (headless) compares the imported scene with the `.tmj`:

- **Tiles:** all **853 cells match**: source, atlas coords and flip/transpose flags (including the 38 flipped). There are no extra cells, and visibility and opacity match.
- **Custom data:** `data_kind` became a TileSet custom-data layer `kind`.
- **Markers:** every marker's position, class, id and typed properties came through. Ints stay ints, and the enum comes out as its string value.

`check/render.gd` draws the imported scene in a real (non-headless) `SubViewport` and diffs it against Tiled's own `tmxrasterizer` render. **Stage 0 and stage 2 both differ in 0 of 92,160 pixels** (see `renders/`).

**Deterministic in substance, not byte for byte.** Two clean imports (`rm -rf .godot`) from the same starting state give identical scenes apart from the per-node `unique_id=` values. Godot 4.7 assigns those randomly on every save; YATI doesn't control them. With them stripped, the md5 matches across both clean runs and a warm reimport. Sub-resource ids and texture UIDs were stable in every run.

**The trap: embedded textures.** YATI's `DataLoader.load_image` references a tileset PNG only if that PNG already has a `.import` sidecar. If it doesn't, YATI falls back to `Image.load_from_file` and **writes the raw pixels into the scene**. There are two cases:

| Starting state | Imported scene |
|---|---|
| A: every PNG's `.import` committed, no `.godot/` (fresh CI clone) | **20 KB**, textures are `ext_resource`s |
| B: PNGs with no `.import` yet (brand-new assets), no `.godot/` | **2.1 MB**, 4 embedded `Image` sub-resources |

Both look identical on screen. B's bloated scene stays in the cache until the map's content changes or the cache is wiped; touching the file isn't enough, because Godot compares content hashes.

**Failures are silent.** Every one of these runs exited **0**:

- **Broken JSON in the `.tmj`:** YATI logs `SCRIPT ERROR … Importer.gd:99` and Godot logs `ERROR: Error importing`. No scene is produced. Godot then writes **`valid=false` into `check_area.tmj.import`**, and from then on it **never re-imports that map**, even after the map is fixed and `.godot/` is wiped. Nothing is logged, and only restoring the `.import` file recovers.
- **Missing `.tsj`:** YATI logs `ERROR: Tileset file … not found` and `Import finished with 1 error.` It still writes a partial scene. **No `SCRIPT ERROR` line appears.**
- Every run also logs leaked-RID or resources-in-use errors at exit. That's noise.

**Rectangle markers become physics bodies.** YATI turns each rectangle object into a `StaticBody2D` with a `CollisionShape2D`, and point objects into `Marker2D`.

**Timing:** a clean `--import` of this project takes about 2.4 s.

## Rerun

```sh
# from this folder, with Godot/Tiled unzipped somewhere and YATI unzipped into ./addons
G=/path/Godot.app/Contents/MacOS/Godot; T=/path/Tiled.app/Contents/MacOS/Tiled
sed -i '' "s|__ROOT__|$PWD|" scripts/draw_area.js        # only to redraw the map
rm -rf .godot && $G --headless --path . --import
$G --headless --path . --script res://check/verify.gd       # prints "checked cells: 853 (38 flipped), problems: 0"
$G --path . --script res://check/render.gd -- "$PWD/renders"  # opens a window briefly
```
