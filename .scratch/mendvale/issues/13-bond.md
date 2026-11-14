# How does Bond shape a Creature?

Type: grilling
Status: resolved
Blocked by: 07, 08

## Question

Specify Bond (see `GLOSSARY.md` and the answer to ticket 05, "What is the core game loop, and what makes Project Wildling different?"):
- What Bond leanings are tracked (e.g. kinds of moves used, Habitats fought in, battles won together) and how they accumulate.
- How Bond is shown on the Creature's page.
- How leanings select one of a Creature's evolution branches, and when the player sees which way it is heading.
- How Bond unlocks extra moves beyond the level-up list.
- What happens to Bond on trade-like events (release, storage, catching a duplicate).
- How it is expressed as data per Creature species.

Must be visible, never hidden stat growth, and must not copy Coromon's Potential grades.

Added from ticket 07 (How does a battle work?): decide whether and how Bond lets a Creature **swap its Trait** to another of its species' Traits. Bond-unlocked moves join the learned list and use the normal loadout (4 equipped plus the Basic move).

## Answer

Resolved by grilling with the human (2026-11-14). Builds on ticket 05 (pillars), ticket 07 (How does a battle work?) and ticket 08 (How do catching, the party, and storage work?). Terms are defined in `GLOSSARY.md`: Bond, Bond rank, Leaning, Trait, Sanctuary, Collection log, Habitat, Habitat patch, Set encounter, Boss. **Every number is data with a starting value, tuned in playtesting.**

### What Bond is
- **Bond = a Bond rank + Leanings.** The rank is *how much* the Creature has been raised; a Leaning is *which way*. Rank unlocks Bond moves; a Leaning picks the evolution branch.
- Bond **never touches stats**, and **no item affects Bond rank, Leanings or Traits**. Bond is earned only by raising the Creature.
- **No Trait swapping in v1.** The Trait stays a permanent record of where and when the Creature was caught; the data doesn't rule out a later "re-meet the condition" swap.
- Unlike Coromon's Potential grades, nothing here is rolled or graded at catch: every Creature starts at zero and becomes what the player made it.

### Bond rank
- **Ranks 0–5.** A Creature earns Bond points only for battles in which it **acted** (used a move, or a Lure was offered while it was out). Being in the Party, or out without acting, earns nothing.
- Points per battle: **1** wild, **2** set encounter, **5** Boss.
- Rank thresholds: **5 / 15 / 30 / 50 / 80** points. Rank 5 takes roughly 40–60 battles of real use: a core team member gets there within the Medium campaign, and a benched Creature catches up in a few hours.
- Rank only grows; nothing is ever lost.
- Beyond moves, rank has **no battle, catch or economy effect**. At rank 3+ the following Creature uses a happier idle animation or emote (cosmetic only).

### Leanings
- Four axes, a **closed list in code**:
  - **Style:** Power moves vs Focus moves used.
  - **Type:** which of two named move Types it uses (e.g. Flame vs Gale).
  - **Habitat:** which of two Habitats it battles in (e.g. shallows vs cave floor).
  - **Time:** day-side (morning/day) vs night-side (evening/night) battles.
  - "Role" (damaging vs Status/stat moves) was considered and left out: many moves are both.
- Every Creature tracks all four; a two-branch species' data names **one axis** and its two ends.
- Each needle runs **−10 to +10**. Each counted action nudges it one step toward that end:
  - Style and Type: **each move use** (the Basic move doesn't count). A move of a Type that is neither end doesn't move the Type needle.
  - Habitat and Time: **each battle the Creature acted in**.
- A full swing takes about 10 battles, so the player can always steer it back.
- **Habitat outside a patch:** each Area names a **default Habitat** for battles outside a Habitat patch (trainers, Bosses); a set encounter may override it. If the battle's Habitat is neither end, the needle doesn't move.

### Evolution
- Triggered by a **level threshold per species**. When the Creature reaches it, evolution is offered and the player may choose **"Not yet"**; afterwards it can evolve at any time from its page.
- For a two-branch species, the **needle's side at that moment picks the branch**. A needle at exactly the centre lets the **player choose**.
- Once evolved, the **branch is locked**. Single-form evolutions work the same way without a branch.
- **At most one branch point per evolution line in v1** (a branch may sit at either evolution). The data allows more; the linter enforces the v1 limit.

### What the player sees
On the Creature's page, for a two-branch species:
- The axis needle with both ends labelled ("Power ◀──●──▶ Focus"), always visible.
- The two branch forms at its ends as **silhouettes until discovered** (seen or caught, recorded in the Collection log), then named.
- The end the needle currently favours is highlighted.
- From **5 levels before** the evolution level: "Evolves at Lv 24 · leaning toward [silhouette/name]".

Species with one form or no branch show **no needle**, only the Bond rank. Evolving records the branch in the Collection log.

### Bond moves
- Each species lists **2–4 Bond moves, each keyed to a rank (1–5)**, with no Leaning condition. The branch gives the flavour: **each evolved form has its own Bond-move list**.
- On evolving, the Creature **immediately learns every Bond move of its new form up to its current rank**. Moves learned before are kept (learned moves are kept forever, per ticket 07).
- A short card appears at each rank-up ("Rank 3 — learned Ember Dance").
- Bond moves join the learned list and use the normal loadout (4 equipped plus the Basic move).

### Lifecycle
- Bond belongs to the individual Creature.
- **Sanctuary:** kept unchanged, **no decay**.
- **Evolution:** rank and needles carry over. A Type or Habitat needle **re-centres** only if the new form's ends for that axis differ from the ones it was measured against.
- **Release:** Bond is lost, with no refund or transfer.
- **New catches, duplicates and gift Creatures** start at rank 0 with every needle centred; nothing is inherited.

### Data
**Species:**
```yaml
evolution:
  level: 24
  # either a single form:
  into: species_id
  # or two branches:
  branch:
    axis: style | type | time | habitat
    ends: [power, focus]          # or [flame, gale], [day, night], [shallows, cave_floor]
    into: [species_a, species_b]  # matching the ends' order
bond_moves:
  - { rank: 1, move: move_id }    # 2–4 entries, ranks 1–5
```

**Area:** a `default_habitat`; a set encounter may override it.

**Global tuning:** rank thresholds, points per battle kind, needle range and step, the 5-level warning window, the follower-emote rank.

**Save, per Creature:** `bond_points` and `needles` as `{axis: {ends, value}}`. **Rank is derived** from points, and a postponed evolution is derived (level ≥ evolution level, not yet evolved), so neither is stored. Retuning thresholds in a content patch can never take a rank away, matching Restoration's raw-facts rule.

### Content-linter rules
For each branching species:
- **Type axis:** both ends are Types the Creature can learn moves of (level-up or Bond) before its evolution level.
- **Habitat axis:** both ends exist in Areas reachable before the line's usual evolution level.
- **Time axis:** always valid (resting skips the clock).
- **Style axis:** the species can learn at least one Power and one Focus move before evolving.
- **Bond moves:** 2–4 per species, ranks 1–5, no duplicates.
- **At most one branch point per line.**

**Follow-ups:** tickets 09 (technical architecture) and 14 (items and economy) were amended. The new ticket 16, "How is the Creature roster structured?", was graduated from the Creature roster & evolution fog. The Creature art production fog was updated.
