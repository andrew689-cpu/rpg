# Which tool authors Area maps, and how do they become content data?

Type: research
Status: open
Blocked by: none

## Question

Find the best way for agents and the human to author Mendvale's Area maps for Godot 4.7.x (see the answers to tickets 01, 09, 10 and 12, and ADRs 0001 and 0002):
- **Candidates:** Godot's own `TileMapLayer` scenes, Tiled (`.tmx`/`.tmj`) and LDtk (`.ldtk`), plus any maintained Godot 4 importer each needs. For each importer: licence, maintenance, and Godot 4.7 support.
- **Agent-friendliness:** can an agent read and edit the map file as text and diff it in a PR, without the GUI?
- **What a map must carry:** 16×16 tiles from Ninja Adventure, collision, Habitat patches, a tile-swap layer per Restoration stage spreading from a focal point, and markers (Rest point, shop, item spot, Forage spot, hidden site, trainer, Area challenge, Blight barrier, Area exits).
- **The bake:** how a map becomes part of the pure core's grid data (ADR 0002) and the content bundle (ADR 0001), so the core never reads a Godot scene. Also whether the linter can check markers, such as barrier flags and level bands.

Already fixed: the core owns the overworld grid, not scenes (ticket 09). Content is JSON with permanent IDs, baked into one bundle, with the linter as the build gate (ticket 09). Tiles are 16×16 and Restoration is shown as tile swaps (ticket 10).
