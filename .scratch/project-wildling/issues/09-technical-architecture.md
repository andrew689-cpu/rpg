# What is the technical architecture?

Type: grilling
Status: open
Blocked by: 01, 07, 08

## Question

Given the chosen engine and battle/catching rules: module boundaries (overworld, battle, party, content, save, UI), the data-driven content format for Creatures/moves/items/maps (so Medium → Large needs no code changes), save-file format and versioning, scene/state flow, and the test strategy that lets agents build modules independently.

Added from tickets 10 and 11:
- Input reduces to five actions (`move(dir)`, `walkTo(tile)`, `confirm`, `back`, `menu`), shared by touch, gamepad and keyboard.
- Screen layouts are data (portrait now, landscape later; left-handed mirroring is a layout setting).
- Render is 180 pixels wide internally, with integer scaling and the height extended to fill the screen.
- Battle animations are code effects on still sprites, with an off setting.
- Art is swapped through data: tiles, 16×16 map sprites, and 64×64 front and back battle sprites, all within a locked 53-colour palette.
