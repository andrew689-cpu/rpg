# How is the region laid out?

Type: grilling
Status: open
Blocked by: none

## Question

Specify the Medium region's map as a list of Areas (see `GLOSSARY.md` and the answers to tickets 05, 10, 12, 14 and 15):
- **The Area list per Chapter:** how many towns, routes and dungeons; their rough size in screens (portrait, about 11 × 12 tiles visible); and their connections, adding up to the ~19 h critical path in ticket 15.
- **Boss home Areas:** where each of the 8 Bosses stands, matched to its theme Type (a Tide Boss by water), and which 1–2 routes its flag restores.
- **Blight barriers:** where each one stands, which flag clears it, and the story-beat flags that restore Areas no Boss covers (including the first route after the starter pick).
- **The Habitat kinds list:** the terrain kinds Creatures belong to. This sets the Habitat Lures (ticket 14) and Habitat patches (ticket 08).
- **Per-Area furniture:** Rest points (reachable in Blighted Areas too), one shop per town, focal points, and which Areas have 0 stages (interiors, untouched towns).
- **Optional paths** that only stages 2+ open, and where Area challenges and hidden sites sit, at the level bands from ticket 15.
- How the layout leaves room for a second region (the Large scale) without moving anything.

Already fixed:
- **Ticket 15:** 5 Chapters of 1 / 2 / 3 / 1 / 1 Bosses with ace levels 12 / 22 / 34 / 44 / 52. Each Chapter's Bosses are reachable without beating each other. Gates are Blight barriers only. Boss order comes from reachability (ADR 0003). The Areas before each Boss must offer at least 2 catchable species that hit its Type for 2×.
- **Ticket 12:** each restorable Area has a focal point, a tile-swap layer per stage, 3–6 native species, its trainers, at most one Area challenge, hidden sites, and optional paths that only stages 2+ open.
- **Ticket 14:** item-spot and Forage-spot markers. Blighted Areas have few Forage spots, and stages 2+ add more.

Placing each species in Areas waits for this ticket and the roster ticket (16). The tool used to draw Areas is ticket 19.

Added from ticket 16 (How is the Creature roster structured?):
- **Lines by debut Chapter:** 7 lines first appear in Ch 1, 5 in Ch 2, 5 in Ch 3, 4 in Ch 4 and 1 in Ch 5 or postgame. Three-stage lines debut only in Ch 1–2. Shade lines debut in Ch 2–3, Lumen in Ch 3–4, and Frost by Ch 3.
- **Before Boss 1:** a **Gale** line and a **Flame** line must be the **two most Common species** in the Areas before Boss 1 (the Boss 1 gate's bot party uses them), and at least 2 Wild lines live there for Boss 1's team.
- **Wild starters:** all 12 starter base forms appear **Rare in Chapter 2–3 Areas**, each matching its Habitat, at most 2 per Area.
- **Rare one-offs:** 2 set encounters at **final-stage focal points**, one in Chapter 4 and one postgame.
- Each species has one home Habitat kind, so the Habitat kinds list sets every species' Habitat field as well as the Habitat Lures.
- No starter line is on a trainer or Boss team before Chapter 3, and branch forms are in no spawn table.
