# Which tool authors Area maps, and how do they become content data?

Type: research
Status: resolved
Blocked by: none

## Question

Find the best way for agents and the human to author Mendvale's Area maps for Godot 4.7.x (see the answers to tickets 01, 09, 10 and 12, and ADRs 0001 and 0002):
- **Candidates:** Godot's own `TileMapLayer` scenes, Tiled (`.tmx`/`.tmj`) and LDtk (`.ldtk`), plus any maintained Godot 4 importer each needs. For each importer: licence, maintenance, and Godot 4.7 support.
- **Agent-friendliness:** can an agent read and edit the map file as text and diff it in a PR, without the GUI?
- **What a map must carry:** 16×16 tiles from Ninja Adventure, collision, Habitat patches, a tile-swap layer per Restoration stage spreading from a focal point, and markers (Rest point, shop, item spot, Forage spot, hidden site, trainer, Area challenge, Blight barrier, Area exits).
- **The bake:** how a map becomes part of the pure core's grid data (ADR 0002) and the content bundle (ADR 0001), so the core never reads a Godot scene. Also whether the linter can check markers, such as barrier flags and level bands.

Already fixed: the core owns the overworld grid, not scenes (ticket 09). Content is JSON with permanent IDs, baked into one bundle, with the linter as the build gate (ticket 09). Tiles are 16×16 and Restoration is shown as tile swaps (ticket 10).

## Answer

Findings: branch `research/map-authoring`, file `research/map-authoring.md` (official docs, importer repos, release notes and engine source as of 2026-11-14).

**Recommendation: author Area maps in Tiled 1.12.x, saved as `.tmj` with CSV-encoded tile layers.** One Tiled project file defines a custom class for each marker kind. Godot's own `TileMapLayer` scenes are the runner-up. LDtk is not recommended.

- **The bake reads the `.tmj` directly.** `tools/bake_content` parses it as plain JSON into the `AreaGrid` in `content.bundle.json`, so the core and the linter never see a Godot scene or an importer (ADR 0001, ADR 0002).
- **Visuals come from the YATI importer** (MIT, 2.2.9, tested with Godot 4.7.2 and Tiled 1.12.2), vendored in `addons/`. It turns the same `.tmj` into `TileMapLayer`s on import. Tiled's built-in Godot exporter isn't used: it writes the deprecated `TileMap` node and hasn't changed since 2024-02.
- **Diffable:** Tiled writes one map row per line, so a one-tile change is a one-line diff, and each marker is a small JSON object with an `id`, a class and typed properties. Godot 4.7 stores each `TileMapLayer`'s tiles as one base64 string, which agents can't read, hand-edit or meaningfully diff.
- **Carries everything on the list:**
  - collision and Habitat patches on a logic tile layer or as rectangle objects
  - one `restore_N` tile layer per Restoration stage, with the spread from the focal point ordered by the shell
  - every marker kind as a typed object class
  - The findings draft the marker linter rules: allowed kinds, required fields, ID resolution, exit pairing, a single focal point, barriers clearing only at stage 1, flood-fill reachability, and level bands from the trainer records.
- **LDtk has stalled:** the editor's last release was 2024-01, and its Godot importer fails on Godot 4.7.1 with the fix unreleased.

**Risks for the decision:**
- Tiled keeps class defaults in the project file, not the map, so the linter must require every marker field to be set explicitly (or the bake merges the defaults in).
- YATI has a single maintainer and has only been tested on Windows. It needs multi-threaded import turned off, and CI must run `godot --headless --import`. The fallback is a small script that paints the map at runtime with `set_cell`.
- Tiled 1.12's new list properties are undocumented, so v1 marker schemas should avoid them.
- **Adopting Tiled contradicts ADR 0001 and ticket 09's "Maps" section**, which keep maps as `TileMapLayer` scenes. Taking the recommendation means amending both, so that the `.tmj` is the source of truth and the `TileMapLayer`s are generated from it.

**Decision (the human, 2026-11-14): adopted.** ADR 0001 and the Maps section of ticket 09 are amended to make the `.tmj` the source of truth. The new task ticket 20, "Does the YATI importer turn a Tiled Area into Godot tile maps on the Mac, the same way every time?", checks the importer on macOS.
