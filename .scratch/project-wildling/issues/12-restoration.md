# How does Restoration change an Area?

Type: grilling
Status: open
Blocked by: 08

## Question

Specify Restoration (see `GLOSSARY.md` and the answer to ticket 05, "What is the core game loop, and what makes Project Wildling different?"):
- How many Restoration stages an Area has.
- Exactly which actions trigger each stage: critical-path stage first, then optional local actions (registering native Creatures, beating local trainers and challenge, hidden sites).
- What each stage changes: encounter table, decorations and tiles, NPCs, open paths, shops.
- How progress toward the next stage is shown to the player, in the world and in a menu.
- How a stage change is presented when it happens.
- How Restoration is expressed as data, so new Areas and regions need no code.

Must be forward-only and must never block the critical path.

Added from ticket 08 (How do catching, the party, and storage work?): each **Restoration stage has its own spawn table** (species, Rarity tier, level range, conditions), and wild Creatures are visible on the map, so restoring an Area visibly changes who wanders it. **Released Creatures never count toward Restoration.** The Collection log records Caught per species, so define exactly what "registering an Area's native species" means (caught anywhere, or caught in that Area?).
