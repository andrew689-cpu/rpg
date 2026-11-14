# How is one evolution line designed and reviewed?

Type: grilling
Status: resolved
Blocked by: none

## Question

Fix the method every evolution line is designed by, so the 34 lines can be authored as content slices against the spec (see `spec.md` §2–§3 and the answers to tickets 13, 16 and 21). Try the method out on starter trio T1's three lines.
- **The checklist for one line:** concept and what it's based on, Types per form, Habitat and Time of day, behaviour, evolution levels and branch axis, Stat archetype, catch % band, map placement and spawn entries, display names (blocklist check), Collection log text.
- **Stat numbers:** the base-stat spread for each of the 6 Stat archetypes at each stage (base, middle, final), and the total budget per stage, so the linter can check a species against its archetype.
- **Traits:** the **closed list of Trait effect kinds** (none is fixed yet), 2–3 Traits per species set by Habitat, time and weather, and how a Trait is chosen at the catch.
- **Moves:** how a line's shared level-up list is picked from the 144 moves (counts per tier, Type coverage), how Bond moves are picked per form, and how signature moves are assigned.
- **Data:** where line-level data lives (a `line` record, or fields repeated on each species) for the shared level-up list and per-line Trait conditions.
- **Review:** what the human checks per line, and what the linter checks.

## Answer

Resolved by grilling with the human (2026-11-14), in three rounds, the third prompted by a trial on trio T1. Builds on tickets 07, 08, 13, 16, 18 and 21. Terms are defined in `GLOSSARY.md`; **Weather** was added. **Every number is a starting value, tuned in playtesting.**

**Trial (asset):** [`prototypes/line-design-t1/`](https://github.com/andrew689-cpu/rpg/tree/prototype/line-design-t1/prototypes/line-design-t1) on the throwaway branch `prototype/line-design-t1` (never merged). `python3 prototypes/line-design-t1/build.py` writes content-shaped drafts for the **Brockle** (Flame badger, Style branch), **Hazelpip** (Grove dormouse, Type branch) and **Lodgekit** (Tide beaver, Habitat branch) lines. It renders each design sheet's `line_sheet` summary and runs a mini-lint of the rules below. The drafts use move *slots*, since the move records don't exist yet. They are **not approved content**: batch 1 re-does T1 properly.

### Before any line: the roster plan
- **`content/roster_plan.json`:** one row per line, giving line ID, stage count, primary Type and any planned second Types, branch axis and ends, debut Chapter, best Rarity tier and home Habitat.
- **Its own content slice,** after the move slice and before batch 1, reviewed by the human as one table.
- **The linter checks every roster budget on the plan** (errors), not on the partial set of records. Each authored line must match its plan row (error). Planned but unauthored lines are fine in test-channel builds and an error in production.
- **Starter branch axes:** 3 lines per axis, with no axis repeated within a trio. With the 6 non-starter branches, every axis reaches ≥4 lines.

### Data
- **New `line` record**, `content/lines/<line_id>.json`. The line ID is **its base form's species ID**. It holds:
  - the ordered species list
  - home Habitat and times of day
  - the shared level-up list
  - the ordered Trait slots
  - the line's **spawn entries** (`{area, stages, form, tier, levels, conditions}`); the bake groups them into the per-Area × stage tables ([ADR 0004](../../../docs/adr/0004-spawn-entries-live-with-the-line.md)). Areas keep `native_species`, and the linter checks each has a Common/Uncommon entry there. `tools/area_sheet` renders each Area's assembled mix.
- **Species records** hold per-form data: `line`, Collection log number, stage, Types, archetype, stats, Energy, base catch %, behaviour, 1–3 extra level-up moves, a Trait ID for each slot, `evolution` and `bond_moves`. Branch forms override Habitat or times only along their own axis.

### Stats
Stage totals cover the **6 scaled stats** (HP, Power, Guard, Focus, Will, Speed). **Energy is outside the total.** The archetype share tables give percent of the total:

| Archetype | HP | Pow | Grd | Foc | Will | Spd | Energy (final) |
|---|---|---|---|---|---|---|---|
| Bruiser | 22 | 22 | 16 | 10 | 14 | 16 | 80 |
| Bulwark | 18 | 13 | 22 | 13 | 22 | 12 | 100 |
| Caster | 15 | 10 | 14 | 25 | 18 | 18 | 130 |
| Skirmisher | 14 | 22 | 13 | 13 | 13 | 25 | 100 |
| Balanced | 17 | 17 | 17 | 17 | 16 | 16 | 100 |
| Warden | 18 | 10 | 17 | 15 | 24 | 16 | 130 |

- Base forms get 80% of the final Energy and middle forms 90%, rounded to 5.
- Archetype is **per form**. A line may shift archetype, and a Style branch may split, e.g. Bruiser and Caster.
- **Lint:** each stat within ±3 points of its share, the total within ±5% of the stage budget (300 / 400 / 500), and a line's two branch forms with **exactly** equal totals.

### Weather
A **closed list in code:** `clear`, `rain`, `fog`, `snow`, `storm`. Each Area's weather table rolls among them per in-game day. Spawn conditions, Trait slots, Trait `when` and `condition_boost` all use this list.

### Traits
- **10 effect kinds (closed list), battle-only, one effect per Trait**, each with an optional in-battle `when` (the battle's time of day, weather or Habitat):

  | Kind | Parameters | Magnitude: base / middle / final |
  |---|---|---|
  | `type_damage` | Type | +10 / 15 / 20% |
  | `category_damage` | power or focus | +8 / 12 / 15% |
  | `resist_type` | Type | −15 / 20 / 25% taken |
  | `start_stage` | stat | +1 at every stage |
  | `status_immune` | Status | – |
  | `status_chance` | – | +5 / 8 / 10 points |
  | `energy_regen` | – | +5 / 8 / 10 points of max per turn |
  | `low_hp_boost` | HP threshold (⅓) | +15 / 20 / 25% |
  | `turn_heal` | – | 3 / 4 / 6% of max HP |
  | `retaliate` | category | 3 / 4 / 5% of the attacker's max HP |

- A Trait with a `when` gets **×1.5** magnitude. The linter checks magnitudes against the bands within ±20%. Every effect folds into the damage preview.
- **A shared pool:** `content/traits/<id>.json`, reusable by any line, with unique display names and card text generated like move cards. A Trait's magnitude is **per stage**. A form may put a different Trait ID in a slot when it wants a different effect, as Smokesage swaps Stoked for Smoulder.
- **Slots:** a line's ordered slots, each with a condition of **time of day or weather only** (Habitat can't vary at a catch, because a species spawns only in its home Habitat), plus the default slot last. **Starters have 3 slots; other lines 2–3.** **Conditioned slots are sidegrades, not upgrades.**
- **How a Trait is picked:** at a wild catch, the first matching slot wins, otherwise the default.
  - **Gifts** (starters included) use the same rule at the gift event, with the Area's clock and weather. The home town's first-day weather rolls from the per-save seed like any other day.
  - **Starter lines have no `morning` condition** (lint), because the gift happens on the story's first morning.
  - **Trainer and Boss Creatures** name their slot in data, and the linter checks that it exists.

### Moves
**Shared level-up template** (a guideline; the linter enforces only the existing rules). A three-stage line has **10 line moves**:

| Level | Slot |
|---|---|
| 1 | own Type, weak, main category |
| 4–7 | own Type, weak, other category |
| 8–11 | coverage Type B, weak |
| 12–15 | own Type, mid, main |
| 18–22 | own Type, no-damage move |
| 25–28 | own Type, strong, main |
| 29–33 | coverage Type C, mid |
| 36–40 | own Type, finisher, main |
| 42–48 | own Type, strong, other category, or a coverage strong |
| 50–55 | own Type, all-foes or second finisher |

- "Main" is the archetype's favoured category; Balanced and Bulwark lines pick one. Two-stage lines drop the 42–48 slot (9 moves), and single-stage lines use 8.
- **Form extras:** base 1, middle 1–2, finals 1–3. Final extras carry the branch's flavour.
- Coverage Types are chosen so a Type branch's ends are learnable before evolving (existing lint).
- **Style-axis lines alternate Power and Focus up to the branch level.** The linter **errors** if the Power and Focus moves learnable before the branch level (from the line list, form extras and Bond lists) differ by more than 1.

**Bond moves:**
- **Counts:** base forms 2 (ranks 1–2), middle forms 3 (ranks 1–3), final forms 4 (ranks 1–4, or 2–5 with a signature).
- **What goes where:** ranks 1–2 hold utility or coverage moves, rank 3 the form's Bond-only move, and rank 4 a finisher.
- **Lists are fresh per form:** a form's Bond list doesn't repeat moves its earlier forms can learn. A repeat gets a lint **warning**.

**Signature moves:** a starter line's signature is its primary Type, shared by both branch forms at rank 5. It may take **`category: best`** (it uses whichever of Power and Focus is higher, like the Basic move), so a Style branch isn't favoured. `category: best` is allowed on signature moves only.

### Spawns
Wild starter base forms are always **level 12–15** wherever they're placed (Chapter 2 or 3), below their evolution at 16. This is a named exemption from the Area band lint.

### The checklist for one line
1. **Plan row** (from the roster plan): stages, Types, axis and ends, debut, best tier, Habitat.
2. **Concept:** the real animal, plant or fungus behind each form, plus its Type element.
3. **Per form:** Types, archetype, stats, Energy, base catch % (band ±5), behaviour.
4. **Evolution levels and branch** (within the bands), with a branch story that offers two real choices.
5. **Times of day; Trait slots and the Trait per slot per form.**
6. **Level-up list, form extras, Bond lists**, and the signature move for starter lines and one-offs.
7. **Spawn entries** that fit the plan and the Area bands.
8. **Display names** (4–9 letters, blocklist) and **Collection log text** (1–2 sentences per form) in `strings/en.csv`.
9. **Design sheet** `content/lines/<line_id>.md` (the bake reads only `.json`), covering concept, silhouette notes per form, 2 key colours, archetype per form, branch story and the do-not-echo check. `tools/line_sheet` appends a generated summary (stats, moves by level, Bond lists, Traits, spawns, log text) below a marker.

### Review
- **One PR per line:** the line JSON, its species, any new Traits, its signature move, string rows and the design sheet.
- **Merge gate:** lint clean, matches its plan row, and **the human approves the design sheet**.
  - **The human checks** names, concept and silhouettes, key colours, do-not-echo, log text, and whether the branch reads as two real choices.
  - **The linter checks** every number and rule above.
- Art follows separately under "Who draws the Creatures, and how is each sprite made and reviewed?", with placeholders until then.

### Content-linter rules added
1. Roster budgets on the plan; each line matches its plan row; unplanned lines fail; planned but unauthored lines fail only in production.
2. Stats: ±3 points per share, ±5% total, equal branch totals.
3. Trait magnitudes within ±20% of the bands (×1.5 with `when`); one effect per Trait; slot conditions time or weather only; default slot last; every form fills every slot; no `morning` condition on starter lines; trainer and Boss Trait slots exist.
4. Style-axis balance before the branch (±1, error).
5. Bond moves repeating an earlier form's moves (warning).
6. `category: best` only on signature moves.
7. Each native species has a Common/Uncommon spawn entry in its Area.
8. Wild starter base forms at levels 12–15 (the band exemption).

### Follow-ups
- **Ticket 07** amended: the Trait condition rule and the closed list of effect kinds.
- **Ticket 09** amended: the `line` and `roster_plan` kinds, spawn entries on lines, weather kinds as a closed list, and `tools/line_sheet` and `tools/area_sheet`.
- **Ticket 16** amended: wild starter levels, spawn entries on lines, and Trait slots on the `line` record.
- **Ticket 21** amended: `category: best` on signature moves.
- **ADR 0004:** spawn entries live with the line.
- **Order of work:** the move slice, then the **roster-plan slice**, then batch 1.
- **Fog:** nothing new. The weather tables per Area and the signature band stay with content work and "What are the starting values for the untuned numbers?". "Reassemble the spec" folds this answer into `spec.md`.
