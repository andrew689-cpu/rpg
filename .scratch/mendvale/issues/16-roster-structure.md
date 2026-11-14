# How is the Creature roster structured?

Type: grilling
Status: resolved
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

## Answer

Resolved by grilling with the human (2026-11-14). Builds on ticket 07 (battle), ticket 08 (catching), ticket 12 (Restoration), ticket 13 (Bond), ticket 15 (Bosses), ticket 10 (art direction) and ticket 02 (art sources). Terms are defined in `GLOSSARY.md`: Evolution line, Branch form, Stat archetype, Starter trio, Trait, Leaning, Rarity tier, Habitat. **Every number is data or a design budget with a starting value, tuned in playtesting.**

### What counts
- The Medium roster is **100 species records**. Every evolved form and every branch form is one species with its own Collection log number.
- A line's forms sit together in display order: base, then middle, then the two branch forms side by side.

### Budget
| | Lines | Three-stage | Two-stage | Single-stage | Branching | Species |
|---|---|---|---|---|---|---|
| Starters | 12 | 12 | – | – | 12 | 36 + 12 = **48** |
| Others | 22 | 6 | 12 | 4 (2 ordinary, 2 rare one-offs) | 6 (2 three-stage, 4 two-stage) | 46 + 6 = **52** |
| **Total** | **34** | 18 | 12 | 4 | **18 of 30 evolving lines** | **100** |

- **Area payoff Creatures** (ticket 12) reuse existing species, as Very rare entries or evolved forms at level L. They add nothing to draw.

### Starters
- **4 Starter trios** (12 lines, every one a distinct species). A 5th trio is Large content.
- They use 4 of the 7 type triangles in ticket 07's chart:

  | Trio | Triangle | Vs Boss 1 (Wild) |
  |---|---|---|
  | T1 | Flame › Grove › Tide | Flame strong, others neutral |
  | T3 | Flame › Wild › Stone | Flame strong, Stone weak |
  | T5 | Grove › Stone › Gale | Gale strong, Stone weak |
  | T7 | Gale › Wild › Volt | Gale strong, Volt weak |

  Flame, Grove, Wild, Stone and Gale have 2 starters each, and Tide and Volt have 1 each. Frost, Shade and Lumen are never starters. Any 4 triangles include at least 2 Stone starters, so they are the hardest cases for the Boss 1 gate (ticket 15). Chapter 1's Common counters (below) carry them.
- Starters **must not copy the genre's iconic starter archetypes** (no fire lizard, grass toad or water turtle).
- Starters are **single-type** at base and middle stage. **All 12 branch at the final evolution.** The axis is chosen per line, with each axis used by at least 2 starter lines. A Type-axis branch may give each final form a different second Type.
- Starter level stays **5**. Starters evolve at **16 and 34**, so the final form and its branch arrive in Chapter 3, after about 10 hours of Leaning.

### Branching
- 18 branching lines in total. **Each of the four axes is used by at least 4 lines.**
- Non-starter branches lean on **Habitat and Time** (about 2 + 2, plus 1 Style and 1 Type), for pillar 3 ("Belongs Somewhere").
- A non-starter three-stage line may branch at either evolution. At most one branch point per line (ticket 13).
- **Branch forms never spawn wild** in Medium; they're only obtainable by evolving. They can still be *seen* (unsilhouetted) on a trainer's or Boss's team. Completing the Collection log therefore means raising both branches of every line.

### Evolution levels
| Line | Bands |
|---|---|
| Starters | 16 and 34 |
| Other three-stage | first 14–22, second 30–40 |
| Two-stage | 12–32 (some early Common lines at about 12, so Chapter 1 has an evolution) |

- **No evolution above level 44**, so every final form is usable before Boss 8. The linter checks the bands.

### Types
Counting each Type of a dual-type species once:
- Each Type is on **12–20 of the 100 species**.
- Each Type is the **primary Type of at least 2 non-starter lines**. Starters put none on Frost, Shade or Lumen, so the other lines carry them (in practice about 3 lines each).
- Each Boss theme Type (Wild, Grove, Tide, Stone, Volt, Frost, Lumen) has **at least 4 distinct final forms**, branch and dual-type forms included, so a rematch team (4 on theme plus 2 coverage) never repeats a species.
- **Shade:** at least 2 lines catchable before Chapter 4 (ticket 15's counter rule).
- **About 40% of species are dual-type.** Base forms are mostly single-type, and the second Type usually comes at evolution. No dual-type pair is used by more than 2 lines.
- The linter checks the counts.

### Traits through evolution
- 2–3 Traits per species, and one of them is the **default**: 1 default plus 1–2 with a condition.
- Trait **conditions are defined per line**. Each form may give each Trait a different or stronger effect.
- A Creature keeps **which Trait it got** through evolution and branching (its "night Trait" stays its night Trait). A wild-caught evolved form uses the same condition list.

### Habitat and time
- Each species has exactly **one home Habitat kind** (the one the Habitat Lure checks) and a **set of 1–4 times of day**. The linter checks that its spawn entries fit both.
- The forms in a line share their Habitat. In a Habitat-axis branch, each branch form takes the Habitat of its own end.
- The Habitat kinds themselves come from ticket 18. *Decided 2026-11-14 by ticket 18: Meadow, Woodland, Wetland, Coast, Cavern, Crag, Snowfield, Ruins.*

### Look
- Each species is based on a **real animal, plant or fungus that fits its Habitat**, plus one visible element of its Type.
- Time of day shows in its colouring: night species use the cool half of the palette and have larger eyes.
- Every form reads as a **clear silhouette with 2 key colours at 16×16**, within the locked palette (ticket 10).
- A **"do not echo" list** of iconic genre designs (an electric yellow rodent, a fire-tailed lizard, a pink blob, a gas ghost) is checked by eye in review, not by the linter.

### Stats
- A **closed list of 6 Stat archetypes**, used as data templates that a species adjusts slightly:

  | Archetype | Leans on |
  |---|---|
  | Bruiser | HP, Power |
  | Bulwark | Guard, Will |
  | Caster | Focus, Energy |
  | Skirmisher | Speed, Power |
  | Balanced | even spread |
  | Warden | Will, Energy (Status-focused) |

- Stat totals by stage:

  | Stage | Total |
  |---|---|
  | Base | ≈ 300 |
  | Middle | ≈ 400 |
  | Final | ≈ 500 |
  | Single-stage | 420–480 |
  | Rare one-off | ≈ 520 |

- The two branch forms of a line share one stat total, so neither is strictly better.

### Moves
- The **level-up list is shared across the line**: 8–12 line moves across levels 1–55, plus 1–3 moves for each form.
- A Creature learns the line's list whatever its form, plus its current form's extras. On evolving, it immediately learns any of the new form's extras at or below its level. Postponing evolution never costs a move, and evolving never skips one.
- Every line has **1 Power and 1 Focus move before its first evolution**, and moves of **at least 2 Types besides its own** by the final form.
- Bond moves stay as ticket 13 set them: 2–4 per form, each keyed to a rank.
- The moves themselves are the new ticket 21, "How is the move list structured?".

### Catching
**Base catch %** (full HP, basic Lure, before the other factors from ticket 08):

| Base | Middle | Final | Wild starters | Rare one-offs |
|---|---|---|---|---|
| 40 | 25 | 12 | 12 | 5 |

The linter checks each species sits within ±5 of its band.

### Rarity
- **Rarity tiers stay on spawn entries**, never on the species record. The roster plan only aims for a spread.
- Best tier for each line's base form:

  | Best tier | Lines |
  |---|---|
  | Common | 10 |
  | Uncommon | 7 |
  | Rare | 3, plus all 12 starters |
  | Rare one-off | 2 |

- The 17 Common and Uncommon lines, plus middle forms in later Restoration stages, supply the Areas' native-species lists (ticket 12: Common or Uncommon only).
- Evolved forms other than branch forms may appear wild, but only at Rare or Very rare and only in later Restoration stages.

### Debut Chapters
Three-stage lines debut only in Chapters 1–2. A later debut would meet the line already past its first evolution level.

| Debut | Three-stage | Two-stage | Single-stage | Lines |
|---|---|---|---|---|
| Ch 1 (wild 4–8) | 4 | 3 | – | 7 |
| Ch 2 (11–18) | 2 | 3 | – | 5 |
| Ch 3 (21–30) | – | 4 | 1 ordinary | 5 |
| Ch 4 (33–40) | – | 2 | 1 ordinary + 1 one-off | 4 |
| Ch 5 / postgame | – | – | 1 one-off | 1 |

- **Type timing follows the Bosses:** Shade lines debut in Ch 2–3 (they're Lumen's only counter), Lumen lines in Ch 3–4, and Frost lines by Ch 3.
- **Chapter 1** includes:
  - at least 1 **Gale** and at least 1 **Flame** line, which are the **two most Common species before Boss 1**, so the Boss 1 gate's bot party always carries both Wild counters
  - at least 2 **Wild** lines, for Boss 1's team of 2
- **No starter line is on a trainer or Boss team before Chapter 3.**
- **Wild starters:** all 12 starter base forms appear **Rare in Chapter 2–3 Areas**, each in an Area matching its Habitat, at most 2 per Area, the player's own trio included.
- **Rare one-offs:** each is a set encounter at a **final-stage focal point**, one in Chapter 4 and one postgame. They respawn after resting (ticket 08). Neither may be Shade or Lumen if that would make it the only counter on offer.

### Names
- Display names are **4–9 letters, 2–3 syllables**, in the plain-English register of Mendvale, Verdling, Mender and Haven: blends of English roots (plant, animal, craft or material words).
- A **blocklist file** of names from other creature franchises is checked by the linter.
- The forms in a line don't need to share a prefix. IDs stay separate, snake_case and permanent (ticket 09).

### Growing to Large
- Medium species are **never removed, renumbered or retyped**.
- Large adds new lines with later numbers. It may add a new **final stage** to an existing Medium line, as a new species, without changing the existing forms. Regional variants are their own species in their own lines.

### Unit of work and "done"
- The design unit is **one evolution line**, because Traits, level-up moves, branches and evolution levels all span the line. An agent drafts each line, and the human approves silhouettes and names.
- A line is **designed** when:
  - its records lint clean
  - each form has a 1–2 sentence Collection log entry
  - the line has a short design sheet: what it's based on, its silhouette, its 2 key colours, and its archetype per form
- A line is **drawn** when every form's front, back and map sprites are final, within the palette, with licence-ledger rows.

### Placeholders
- A **dev-only mapping** gives every species a placeholder: one of the 56 sprites from *50+ Monsters Pack 2D* (ticket 02), or a generated silhouette in the palette (shape from its archetype, colour from its Type).
- The licence ledger gets a `placeholder` column.
- Internal and closed-testing exports allow placeholders. A **production** export fails if any reachable species still uses one.
- A final replaces its placeholder by dropping files at the conventional paths (ticket 09), with no data change.

### Order of work
0. *Added 2026-11-14 by ticket 21 ("How is the move list structured?"):* the **move-list slice** (110 level-up moves and 20 Bond-only moves) comes first, because every line picks from it. Signature moves are written with their own line.
1. **Batch 1 data:** all **12 starter lines** (the Boss 1 gate runs every starter in every trio), plus the **7 Chapter-1 lines** and Boss 1's team.
2. **Batch 1 art, the vertical slice:** trio **T1** plus the 7 Chapter-1 lines as finals. Everything else stays a placeholder.
3. **Batches 2–5:** data and art follow the **Chapter where each form is first seen**. Starter middle forms and the other three trios' base forms come with Chapter 2. Starter final and branch forms come with Chapter 3.
4. **Rare one-offs last.**

Each batch is a set of line-sized slices, and data may run a batch ahead of the art.

### Content-linter rules added
- Total species count against the budget, and the forms per line.
- Evolution levels within their bands, and none above 44.
- At most one branch point per line; branch forms in no spawn table.
- Type counts: 12–20 per Type; at least 2 non-starter primary lines per Type; at least 4 final forms per Boss theme Type; no dual-type pair on more than 2 lines.
- Base catch % within ±5 of its stage band.
- Spawn entries fit the species' home Habitat and times of day.
- Every line has a Power and a Focus move before its first evolution, and 2 extra move Types by its final form.
- Display names are 4–9 letters and absent from the blocklist.
- Production exports have no placeholders.

### Follow-ups
- **New ticket 21**, "How is the move list structured?" (grilling, unblocked). The per-species design work hangs on it.
- **Ticket 18** (region layout): the Chapter 1 most-Common rule, wild starters in Chapter 2–3 Areas, the one-offs at focal points, and lines placed by their debut Chapter.
- **Ticket 17** (builds and release): the production export fails on placeholders.
- **Fog:** the Creature roster fog now hangs on ticket 21 and ticket 18. The Creature art fog gets the batch order. The Story & world fog gets the framing for the rival and the one-offs.
