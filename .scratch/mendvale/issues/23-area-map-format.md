# What exactly does an Area's `.tmj` contain?

Type: grilling
Status: open
Blocked by: none

## Question

Pin down Mendvale's Area map format, so agents can draw Areas and the bake, linter and shell can be written against it (see `GLOSSARY.md`, the answers to tickets 09, 12, 18, 19 and 20, and ADRs 0001 and 0002):
- **Layers:** the fixed list of layer names and their order. How a `restore_N` layer swaps tiles: which layer each swap lands on, and how a stage changes or removes **detail** tiles, such as a dead tree becoming a living one. Ticket 20 found that a `restore_N` layer drawn above `detail` hides it, and ticket 12 has the shell swap cells outward in rings anyway.
- **Logic tiles:** the closed set of logic kinds (walls, the 8 Habitat patch kinds from ticket 18, ledges, water, anything else), and whether Habitat patches are logic tiles, rectangle markers, or both.
- **Marker classes:** for every kind (Rest point, shop, item spot, Forage spot, hidden site, trainer, NPC, Area challenge, Blight barrier, Area exit and internal warp, focal point, Habitat patch), the shape (point or rectangle), the fields and their types, and how `stage_from` / `stage_until` work. Avoid Tiled 1.12 list properties (ticket 19).
- **Class defaults:** the linter requires every field to be set, or the bake merges project defaults in, or maps are exported with `--resolve-types-and-properties` (ticket 20).
- **Tilesets and files:** one external `.tsj` per Ninja Adventure sheet, the folder layout, and committed `.import` sidecars (ticket 20).
- **What the shell takes from the YATI import:** the import options per map, and whether the `markers` layer is dropped by a YATI post-processor. Ticket 20 found that rectangle markers import as `StaticBody2D` physics bodies, while the core owns markers through the bake (ADR 0002).
