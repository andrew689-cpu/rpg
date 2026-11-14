# How is the move list structured?

Type: grilling
Status: open
Blocked by: none

## Question

Specify the shape of Mendvale's move list, so every evolution line's level-up and Bond moves can be picked from it (see `GLOSSARY.md` and the answers to tickets 07, 13 and 16):
- **How many moves** (around 120–150) and how many per Type, so every Type has a weak, mid and finisher option at each stage of the game.
- The **closed list of move effects** the core supports: damage, Status chance, stat stages, healing, Energy effects, multi-target, priority, shown crit chance, and anything else. A new *effect kind* needs code; a new move doesn't.
- **Damage and Status moves:** what share of moves are pure damage, damage plus a side effect, or Status and stat moves only.
- The **Energy cost bands** (about 15% weak to 60% finisher of a typical max) against power and accuracy bands.
- **Power and Focus balance:** how many of each per Type, so the Style linter rule (a Power and a Focus move before the first evolution) is always satisfiable.
- **Signature and Bond-only moves:** whether some moves are reserved for one line or for Bond, and how many.
- **2v2 support moves** (Boss 5 is Volt 2v2: one Creature charging while the other strikes) and the all-foes moves at 75%.
- **Naming conventions** for moves (no collisions with other franchises' move names).
- Room for Large: moves keep permanent IDs and are only ever added.

Already fixed:
- **Ticket 07:** 4 equipped moves plus the free Basic move (30 power, the first Type, no same-type bonus, no Energy). Ratio damage formula; 90–100% roll; no random crits unless the % is on the card; fixed accuracy, no accuracy or evasion stages. Each move has one Type, a Power or Focus category, and a target (one foe / all foes / one ally / self / all). 6 Statuses with countdowns; stat stages −2 to +2. Learned moves are kept forever.
- **Ticket 13:** each form has 2–4 Bond moves keyed to ranks 1–5. Style and Type Leanings count each move use (not the Basic move).
- **Ticket 16:** the level-up list is shared across a line (8–12 line moves across levels 1–55, plus 1–3 per form). Every line has a Power and a Focus move before its first evolution, and moves of at least 2 Types besides its own by the final form. 34 lines across 10 Types.

Choosing each species' actual moves stays in the map's Creature roster fog.
