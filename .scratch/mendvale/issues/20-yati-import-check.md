# Does the YATI importer turn a Tiled Area into Godot tile maps on the Mac, the same way every time?

Type: task
Status: open
Blocked by: 19

## Question

Before the map pipeline from ticket 19 is relied on, check its one unverified link on the Mac that builds iOS:
- Install Godot 4.7.2 and Tiled 1.12.2. Vendor YATI 2.2.9 into a throwaway project under `addons/`, with multi-threaded import turned off.
- Draw one small Area in Tiled from Ninja Adventure 16×16 tiles: ground, detail, a logic layer, two `restore_N` layers, and a few typed markers.
- Run `godot --headless --import` twice from a clean `.godot/` folder. Record whether the `TileMapLayer`s and markers come out right, and whether the two imports give identical output.
- Record the result. If YATI fails or the output differs between runs, that confirms the fallback from ticket 19 (the bake still reads the `.tmj`, and a small script paints the layers at runtime with `set_cell`).

The agent can drive this alone if Godot and Tiled can be installed from the command line. Otherwise it hands the human a checklist.
