# How do catching, the party, and storage work?

Type: grilling
Status: resolved
Blocked by: 05

## Question

Specify how wild Creatures are encountered and caught (capture tool, success chance inputs, failure outcomes), party size, storage for the rest, nicknaming, releasing, duplicate handling, and the collection log ("dex"-style registry; name it originally).

Constraints from ticket 05 (core loop & pillars): encounters are driven by **Habitat**, **Time of day**, weather and the Area's **Restoration stage** (in-game clock, rest to skip; nothing permanently missable). Registering an Area's native Creatures in the collection log is one of the actions that advances its Restoration (rules in ticket 12).

Constraints from ticket 07 (How does a battle work?): a caught Creature's **Trait** is fixed at the catch by the Habitat, time of day and weather, and is **shown on the encounter screen before throwing**. Wild battles are always 1v1, and fleeing them always works. HP persists between battles; Rest points heal.

## Answer

Resolved by grilling with the human (2026-11-13). Terms are defined in `GLOSSARY.md`: Lure, Party, Sanctuary, Collection log, Starter, Rarity tier, Habitat patch, Trait, Rest point. "Lure", "Sanctuary" and "Collection log" are placeholder names until ticket 06 (naming) is decided. **Every number is data with a starting value.**

### Encounters
- Wild Creatures are **visible on the map**; touching one starts a 1v1 battle. There are no hidden random encounters.
- **Up to 4 per Habitat patch.** A caught or defeated Creature is replaced after a short delay. The whole patch re-rolls when the time of day or weather changes, or when the player re-enters the Area.
- Each species has a **behaviour** in its data:
  - **wander:** drifts around.
  - **curious:** approaches the player.
  - **shy:** flees if the player runs nearby; walking slowly lets you approach.
- **Rare** and **Very rare** Creatures have a subtle shimmer on the map. No sound alert.
- **Spawn tables** are per **Area × Restoration stage**. Each entry has species, Rarity tier, level range and conditions (Habitat patch, times of day, weather). The game rolls only among entries whose conditions match right now.
- **Rarity tier** default weights: Common 50, Uncommon 30, Rare 15, Very rare 5. Any entry may override its weight.
- No level scaling; levels are fixed per Area.

### Catching
- The player **offers a Lure**. The Creature may accept and *choose* to join. There's no container.
- Lure tiers and Habitat-specific Lures act as the better capture tools. The item list belongs to the Items & economy fog.
- **Catch %** is shown before offering, clamped to 1–95%. It is made from:
  - the species' base rate
  - remaining HP (lower HP raises it a lot)
  - a flat bonus if the target has any Status
  - the Lure's modifier
  - a level factor (harder if the target is far above the Party's highest level)

  There are no hidden factors.
- Offering a Lure **uses up the turn**. On failure the Lure is used up, the Creature refuses, and **it never runs away because of a failed catch**.
- Trainer and Boss Creatures can never be caught.
- The **Trait** is fixed at the catch by the Habitat, time of day and weather, and is shown before offering (from ticket 07).

### Rare one-off Creatures
- **Single set encounters** placed in the world's data, never part of a spawn table.
- If one is fainted or the player flees, it comes back after the player rests at a Rest point, so nothing is permanently missable.
- They are caught with the normal Lure rules, with a low base rate shown as %.

### Starters
- The player **picks 1 of 3**.
- There are **4–5 hand-designed trios**, each a type triangle (e.g. Flame > Grove > Tide > Flame). A new game picks one trio at random.
- A **per-save seed**, rolled at new game and stored in the save, picks the trio. Nothing else uses the seed yet; it's reproducible and can't be beaten by reloading.
- **Every starter species also appears in the wild** (Rare, in a mid-game Area), so every one is catchable in every playthrough.
- Rare one-off Creatures are never starters.
- The first Boss must be beatable with every trio.
- The story framing goes to the Story & world fog.

### Party
- **6 Creatures.** The first one leads in battle.
- The **lead Creature follows the player on the map**, with a settings toggle to turn it off. It reuses the species' 16×16 map sprite.
- The player can't release their last Creature.

### Sanctuary
- Holds every Creature not in the Party. **No size limit**, reachable from any **Rest point**.
- New catches go there automatically when the Party is full.
- **Version 1 is a menu**, with sorting and filters by type, Trait, level and species.
- The data model treats it as a place (a stored Creature can have a spot on a map), so a walkable Sanctuary Area can come later without a rewrite.

### Nicknames, releasing, duplicates
- A **nickname** is offered right after the catch (skippable) and can be changed anytime from the Creature's page. Only a length limit; no profanity filter (offline, single-player).
- **Releasing** needs a "This can't be undone" confirmation. The Creature returns to the wild. It gives **no reward** and does **not count toward Restoration**. The Collection log keeps it as Caught.
- **Duplicates** are unlimited and meaningful because Traits differ (and later Bond and evolution branch).

### Collection log
- For each species it records:
  - Seen or Caught
  - where and when the species can be found (Habitat, time of day, weather), filled in as discovered
  - Rarity tier, once seen
  - Traits discovered
  - evolution branches discovered
- Catching an Area's native species is one of the Restoration actions; the exact rules go to ticket 12.
- Completing the log is a postgame goal.
