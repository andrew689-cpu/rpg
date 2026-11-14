# What stat, damage and type-chart systems do creature-collector games use?

Type: research
Status: resolved
Blocked by: none

## Question

Survey the *mechanics* (not content) used across the creature-collector genre and adjacent turn-based RPGs (e.g. Cassette Beasts, Temtem, Coromon, Monster Sanctuary, Dragon Quest Monsters, Shin Megami Tensei), plus open-source engines' documented formulas, to give the battle-design ticket a menu of options:

- stat models (which stats, growth curves, individual variation)
- damage formulas and their balance properties
- type/element systems (size of chart, single vs dual typing, alternatives like fusion or status-combos)
- turn order, accuracy, crits, status effects, stamina/energy vs PP-style move limits
- capture-rate formulas
- XP / level curves

Note which ideas are distinctive to specific games (avoid copying) vs genre-standard.

## Answer

Findings: branch `research/battle-mechanics`, file `research/battle-mechanics.md`. It is a menu of options; the actual design is decided in **How does a battle work?**

- **Genre baseline (progenitor):** stats, the damage formula (85–100% random roll, 1.5× same-type bonus), crits, accuracy stages, priority then speed for turn order, per-move uses (PP), a capture formula (overall success ≈ a/255; the "shakes" only animate it), and six XP curves.
- **Type systems:** 18 types / 324 matchups with immunities (progenitor). Temtem: 12 types, no damage immunities. Coromon: 8 Creature types plus 6 move-only types. Cassette Beasts: 14 types with type reactions.
- **Damage:** attack ÷ defence formulas keep hits-to-KO roughly constant across levels, so move power is the main tuning knob (our own inference). Attack − defence (Dragon Quest) needs a damage floor.
- **Move resources:** per-move uses; a shared stamina pool with an overspend penalty (Temtem); a shared pool with forced rest (Coromon); points that refill each round (Cassette Beasts).
- **Capture:** every game weights the chance by the target's remaining HP. Some also use its level; Dragon Quest Monsters shows the % up front.
- **Signature mechanics to avoid copying:**
  - Temtem: synergy bonus and stamina overspend.
  - Cassette Beasts: fusion and type reactions.
  - SMT: Press Turn.
  - Monster Sanctuary: combo meter.
  - Coromon: Potential grades.
- **Mobile levers:**
  - Keep randomness visible to the player.
  - 8–12 types, with a cap on how much two types can multiply together.
  - One energy bar per Creature instead of four move counters.
  - Show the capture chance.
  - XP scaled by level gap, so lower-level Creatures catch up.
  - Status effects with visible countdowns.
- **Caveats:** the Monster Sanctuary and SMT details rest on secondary sources. The Temtem and Cassette Beasts formulas are garbled on their wikis and need checking in a browser. The decompiled code is reference only: never copy its code or data tables.
