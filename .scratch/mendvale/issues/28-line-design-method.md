# How is one evolution line designed and reviewed?

Type: grilling
Status: claimed
Blocked by: none

## Question

Fix the method every evolution line is designed by, so the 34 lines can be authored as content slices against the spec (see `spec.md` §2–§3 and the answers to tickets 13, 16 and 21). Try the method out on starter trio T1's three lines.
- **The checklist for one line:** concept and what it's based on, Types per form, Habitat and Time of day, behaviour, evolution levels and branch axis, Stat archetype, catch % band, map placement and spawn entries, display names (blocklist check), Collection log text.
- **Stat numbers:** the base-stat spread for each of the 6 Stat archetypes at each stage (base, middle, final), and the total budget per stage, so the linter can check a species against its archetype.
- **Traits:** the **closed list of Trait effect kinds** (none is fixed yet), 2–3 Traits per species set by Habitat, time and weather, and how a Trait is chosen at the catch.
- **Moves:** how a line's shared level-up list is picked from the 144 moves (counts per tier, Type coverage), how Bond moves are picked per form, and how signature moves are assigned.
- **Data:** where line-level data lives (a `line` record, or fields repeated on each species) for the shared level-up list and per-line Trait conditions.
- **Review:** what the human checks per line, and what the linter checks.
