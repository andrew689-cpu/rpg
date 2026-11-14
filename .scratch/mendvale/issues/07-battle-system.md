# How does a battle work?

Type: grilling
Status: resolved
Blocked by: 03, 05

## Question

Specify the battle system: format (1v1 / 2v2 / other), stats, damage formula, type system, move limits, turn order, status effects, switching, fleeing, wild vs trainer battles, AI behaviour tiers, and how it reads on a phone screen. Must scale to ~150+ Creatures and many moves as data.

Constraints from ticket 05 (core loop & pillars): leave room for an optional new-game **challenge mode** (tougher AI, level caps), and for **Bond** to unlock extra moves (the Bond rules themselves are decided in ticket 13). Bosses must reward type choice and switching; grinding must never be required; randomness stays visible.

## Answer

Resolved by grilling with the human (2026-11-13). Builds on ticket 03 (research menu) and ticket 05 (pillars). Terms are defined in `GLOSSARY.md`: Type, Energy, Basic move, Trait, Status, Power move, Focus move, Set encounter, Rest point. **Every number below is data with a starting value, tuned in playtesting.** The **on-screen layout** was moved to ticket 11, "How does the game feel on a touchscreen?"

### Format
- **1v1** is the default.
- **2v2** happens only in **set encounters** (some trainers, some Bosses, tag fights), never wild battles. The data model allows N Creatures per side.
- In 2v2 the player picks both Creatures' actions, then taps the enemy sprite to target it. A move with only one valid target picks it automatically.
  *Amended 2026-11-14 by ticket 22 ("What is Mendvale's story, and which beat sets each flag?"): a set-encounter slot may have an AI `controller` (an AI tier) instead of the player. In the tag battle the rival's slot fights from the rival's team; the player loses only when their own Party is out, and the ally's Creatures gain no XP or Bond.*
- Each move has a target field: one foe / all foes / one ally / self / all. A move that hits all foes deals 75% to each. *(Ticket 21: only when it actually hits 2 or more targets; in 1v1 it does full damage.)*

### Types
- 10 types: **Flame, Tide, Grove, Gale, Stone, Volt, Frost, Shade, Lumen, Wild**. Every Creature has 1–2 types; every move has 1.
- Multipliers are 2× / 1× / 0.5×, with **no immunities**. For dual types the combined multiplier is **capped at 2× and floored at 0.5×**.
- Same-type bonus: **1.25×**.
- A possible "Blight" type for the antagonist is left to the Story & world fog.
  *Amended 2026-11-14 by ticket 22 ("What is Mendvale's story, and which beat sets each flag?"): there is no Blight Type; the faction uses Shade.*

Starting chart:

| Attacker | 2× vs | 0.5× vs |
|---|---|---|
| Flame | Grove, Frost, Wild | Tide, Stone, Flame |
| Tide | Flame, Stone | Tide, Grove, Frost |
| Grove | Tide, Stone | Flame, Gale, Grove |
| Gale | Grove, Wild | Stone, Volt |
| Stone | Flame, Gale, Volt | Grove, Wild |
| Volt | Tide, Gale | Stone, Grove, Volt |
| Frost | Grove, Gale | Flame, Frost |
| Shade | Lumen, Wild | Shade |
| Lumen | Shade, Frost | Lumen, Grove |
| Wild | Volt, Stone | Gale, Shade |

### Stats
- **HP, Power, Guard, Focus, Will, Speed, Energy.**
- **Power moves** (fist icon) use Power vs Guard. **Focus moves** (spark icon) use Focus vs Will. Each move sets its own category. *(Ticket 21: so does every move that deals no damage, so Style Leaning counts every move use.)*
- Readability: colour-paired horizontal bars with numbers (Power and Guard warm, Focus and Will cool). The damage preview does the maths for the player.
- Levels run **1–100**; the Medium credits roll around level 50–55. The stat formula is species base × level, with no random component.

### Individuals
- **No random stat rolls**: no IVs, natures or grades.
- Each species has **2–3 Traits**. Each Trait has a condition (Habitat, time of day or weather), plus one default Trait when no condition matches. If several match, the first listed in data wins.
- The Trait is fixed at the catch and **shown before throwing**.
- A Trait is a passive effect built from a fixed set of effect types (e.g. "+20% Tide damage in rain", "starts battle with +1 Guard").
- Trait swapping is deferred to ticket 13 (Bond).

### Moves and Energy
- **4 equipped moves plus the free Basic move.** The Basic move has 30 power, uses the Creature's first type, gets no same-type bonus and costs no Energy. *(Ticket 21: it uses whichever of the user's Power and Focus is higher, against the matching defence.)*
- Learned moves are kept forever and can be swapped freely outside battle.
- A single **Energy** bar per Creature. It regains **20% of max per turn** and refills after battle. Move costs run about 15% (weak) to 60% (finisher) of a typical max.
  *Amended 2026-11-14 by ticket 21: max Energy is a **flat species value, not scaled by level** (typical about 100), and move costs are absolute numbers.*
- No overspend penalty and no forced rest (those are Temtem's and Coromon's signature mechanics).

### Damage and randomness
- **Ratio formula:** power × attacking stat ÷ defending stat × modifiers (type, same-type bonus, stat stages, Trait).
  *Amended 2026-11-14 by ticket 21 ("How is the move list structured?"): the formula gains a level term, `power × attacker level × attack ÷ defence × k × modifiers`, so a move takes the same share of an equal-level foe's HP all game long. `k` is set so that power P takes about P ÷ 3 % of HP from a neutral target (no same-type bonus, mid roll).*
- **90–100% roll.** No random crits; a move may carry a crit chance only if the % shows on its card. *(Ticket 21: a crit does 1.5×.)*
- Accuracy is fixed per move and shown. **No accuracy or evasion stages.**
- Before confirming, the preview shows the **damage range as a % of the target's HP, plus effectiveness**. Any chance to inflict a status shows its %.

### Turns
- **Pick, then resolve.** Order is priority, then Speed; **ties go to the player's side**. A turn-order indicator shows the order before confirming.
- **Switching** uses up the turn; the incoming Creature arrives before the opponent's move.
- **Items** use up the Creature's turn. Trainers and Bosses have a fixed number of item uses in their battle data.
- **Fleeing** from wild battles always works. You can't flee trainers or Bosses; you can forfeit a trainer battle, losing only the reward.

### Statuses and stat stages
- **6 statuses.** Each has a visible turn countdown. A Creature has at most 1 at a time, and all clear after battle. No random "may skip a turn" effects.
  - **Burn:** lose 1/12 max HP per turn, Power lowered.
  - **Poison:** lose HP each turn, increasing each turn.
  - **Chill:** Speed halved.
  - **Fatigue:** no Energy regained.
  - **Snare:** can't switch or flee.
    *Amended 2026-11-14 by ticket 25 ("Which way do the spec's seven conflicts go?"): Snare means **can't switch out** only. Fleeing a wild battle always works, Snared or not.*
  - **Drowsy:** skips its next turn, then immune to Drowsy for 3 turns.
- **Stat stages** run from −2 to +2 at ±25% per step (×0.5 to ×1.5). They show as arrows on the HP bar and reset on switching or at battle end.

### AI
- A separate module behind a fixed interface, testable on its own. Three tiers:
  - **Wild:** weighted-random.
  - **Trainer:** best expected damage, with type awareness.
  - **Boss:** also thinks one turn ahead, switches out of bad matchups, and uses Statuses on purpose.
- Challenge mode (a later option chosen at new-game) raises everyone one tier and gives Bosses a fourth.

### Around battles
- **HP persists** between battles; Energy, Statuses and stat stages reset.
- **Rest points** heal for free, revive fainted Creatures, and skip the in-game clock.
- **XP** goes to the whole party, scaled by level gap: Creatures below the enemy's level get more, those far above get much less.
- **Losing** (whole party fainted): return to the last Rest point used, healed. Lose **8 × the party's highest level × (Bosses beaten + 1)** in money, **capped at 50% of the money carried**. The same applies to Boss losses. Items, catches and XP are kept, and Bosses can be retried straight away.

### Moved elsewhere
- On-screen battle layout and command buttons → ticket 11.
- Catch chance and catching → ticket 08.
- Bond-unlocked moves and Trait swaps → ticket 13.
- Item list and prices → Items & economy fog.
- Species stats, movesets and Trait lists → Creature roster fog.
