# How is the Creature roster structured?

Type: grilling
Status: open
Blocked by: 13

## Question

Specify the shape of the Medium roster (~100 species) so it can be designed and drawn species by species, and grow to Large (150+) without rework (see `GLOSSARY.md` and the answers to tickets 07, 08 and 13):
- How many **evolution lines** and how many species per line (single-stage, two-stage, three-stage), adding up to ~100.
- How many lines **branch**, at which evolution, and on which Leaning axis (Style, Type, Habitat, Time); each branch costs one extra form to draw.
- The **Type spread**: how many species of each of the 10 Types and which dual-type pairings, so every Type has answers and none dominates.
- The **4–5 starter trios**, each a type triangle; whether starters branch.
- The **design conventions** for a species: what it's based on, how its Habitat and Time of day show in its look, base-stat archetypes, how many Traits and Bond moves, Rarity tiers across the roster.
- The **species naming conventions** (tone, length, no collisions with existing franchises).
- The order in which species get designed and drawn, given placeholders from `issues/02-art-sources.md` and self-drawn finals.

Already fixed: 10 Types; 2–3 Traits per species set by Habitat/time/weather; 2–4 Bond moves per species at ranks 1–5; at most one branch point per line; every species needs a Habitat, Time of day, behaviour, Rarity tier, 16×16 map sprite and 64×64 front and back battle sprites; every starter also appears in the wild (Rare, mid-game). Spreading species across Areas stays in the World structure fog.

Added from ticket 09 (What is the technical architecture?): each species is one **JSON record** (`content/species/<id>.json`) with a **permanent snake_case ID** separate from its display name; the Collection log number is a separate display-order field, so species can be inserted when growing to Large. Sprites are found by convention at `assets/creatures/<id>/front.png`, `back.png` and `map.png`, with a placeholder when missing, and the bake checks palette, size and a licence-ledger row for each.

Added from ticket 15 (How do the Bosses and Area gating sequence the region?):
- **Boss teams:** Bosses carry the theme Types **Wild, Grove, Tide, Stone, Volt, Frost and Lumen**, with Boss 8 mixed. Each themed Type needs enough species, evolved forms included, for a team of 2–6 at its Boss's level (12 / 22 / 34 / 44) and a rematch team of 6 at 58–66. **Flame, Gale and Shade** have no Boss; they're for Area challenges, the rival and the antagonist.
- **Counter rule:** the Areas before each Boss must offer at least 2 catchable species that hit its theme Type for 2×. Before Boss 1 (Wild) that means Flame, Gale or Shade species. Lumen is hit 2× **only by Shade**, so at least 2 Shade species must be catchable before Chapter 4.
- **Starters:** start at level 5 (a starting value). For every starter in every trio, a bot party (the starter plus the two most Common species before Boss 1, at level 10) must win at least 70% of 200 seeded runs against Boss 1, or the content tests fail.
