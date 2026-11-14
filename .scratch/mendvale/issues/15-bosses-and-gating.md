# How do the Bosses and Area gating sequence the region?

Type: grilling
Status: open
Blocked by: none

## Question

Specify progression for the Medium scale (see `GLOSSARY.md`, the answers to tickets 05, 07 and 12):
- The ~8 Bosses: each one's Type focus, rough level, AI tier and team size, and the order in which they are offered (string of pearls: 2–3 on offer at a time, no level scaling).
- The level curve across the region: wild level bands per Area, trainer levels, and how they line up with the catch-up XP from ticket 07.
- Area gating: what opens each new Area (a Boss, a story beat, a stage-1 Restoration), and which Areas each Boss's story flag restores to stage 1.
- The first Boss being beatable with every starter trio (from ticket 08).
- Postgame Boss rematches: difficulty, levels, and how often they can be repeated.
- Room for the later optional challenge mode (level caps, tougher AI).
- How the whole sequence is expressed as data, so a second region needs no code.

Already fixed: stage 1 of any Area comes only from a story flag, and one flag may restore several Areas (ticket 12); only stage 1 opens critical-path routes.

Added from ticket 09 (What is the technical architecture?): Bosses, trainers and set encounters are **JSON records** with permanent IDs; story beats, gating and Boss rewards are **events** built from the closed command list (`set_flag`, `battle`, `if_flag`, `give_item` …) run by `EventRunner`, so a second region is content only. The content linter should check the sequence: every gate's flag is set somewhere reachable, and the 2–3 Bosses on offer at each point are reachable without the others.

Added from ticket 14 (What items exist, and how does the economy work?): a Boss pays **100 × its highest level** in Marks, an Area challenge 60 × level, and trainers class base (16–48) × highest level, all one-off. Rematch prizes are for this ticket to set. Shop stock unlocks are keyed to the **number of Bosses beaten** (Better Lures after 2, Best Lures after 5), not to which ones, so any string-of-pearls order works. The content linter checks that critical-path income up to each Boss covers a target shopping list.
