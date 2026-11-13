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

Added from ticket 12 (How does Restoration change an Area?):
- Area data holds `native_species[]` and `stages[]`. Each stage has a trigger (`story_flag` or `mendings_required: K`), `mendings[]`, a spawn table, a tile layer and focal point, and Habitat-patch, NPC, path, shop, weather and music changes, plus an optional payoff Creature.
- Mending kinds are a closed list in code (`register_natives`, `defeat_trainers`, `defeat_challenge`, `find_site`); new Areas need no code.
- The save stores raw facts (registrations per Area, trainers beaten, sites found, story flags), the highest stage reached per Area, and a pending-presentation queue. On load the stage is the higher of stored and computed, so a content patch never moves it backwards.
- A content linter must check that every Mending for stage N is completable at stage N−1, and that only stage 1 opens critical-path routes.
