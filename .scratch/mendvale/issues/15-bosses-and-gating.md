# How do the Bosses and Area gating sequence the region?

Type: grilling
Status: resolved
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

## Answer

Resolved by grilling with the human (2026-11-14). Builds on ticket 05 (pillars), ticket 07 (battle), ticket 08 (catching), ticket 09 (architecture), ticket 12 (Restoration) and ticket 14 (economy). Terms are defined in `GLOSSARY.md`: Boss, Chapter, Blight barrier, Restoration stage, Area challenge. **Every number is data with a starting value, tuned in playtesting.**

### Chapters (the string of pearls)
- The ~8 Bosses fall into **5 Chapters**: **1 / 2 / 3 / 1 / 1** Bosses.
  - Chapter 1: Boss 1.
  - Chapter 2: Bosses 2 and 3, in either order.
  - Chapter 3: Bosses 4, 5 and 6, in any order.
  - Chapter 4: Boss 7.
  - Chapter 5: Boss 8, the finale. The credits roll after it.
- The next Chapter opens only when **every Boss in the current one** is beaten.
- Bosses in the same Chapter share one level. Whichever the player takes later feels a little easier, and the catch-up XP from ticket 07 keeps that gap small. There is no level scaling.

### Gating
- The **only critical-path gate is a Blight barrier** (brambles, a dried ford, a rockfall) cleared by an Area's **stage-1** bundle. There are no NPC roadblocks, badge checks or field moves.
- Every Area is **Locked** (not reachable yet), **Blighted** (reachable, stage 0) or **Restored 1+**. Players walk into the next Chapter's Areas while they are still Blighted, catch and train there, and restore them by beating that Chapter's Bosses.
- **What a Boss restores:** its flag brings **its home Area plus the 1–2 routes that led to it** to stage 1. Story-beat flags, set by events, restore any other Area, for example to open the first route after the starter pick.
  *Amended 2026-11-14 by ticket 18 ("How is the region laid out?"): a Boss flag restores **its whole spoke** (the landmark plus every Area between it and the hub, at most 4), not just 1–2 routes. Each `chapter_N_open` flag restores the hub being left and the connector route out of it.*
- **"Beat every Boss in the Chapter" gates:** a stage-1 trigger stays a single flag (ticket 12). After each Boss win, an event checks the others and sets a combined flag, e.g. `if_flag boss_2 and boss_3 → set_flag chapter_3_open`, with a short story beat. Chapter 4's gate needs all three Chapter-3 flags the same way.

### The Bosses

| Boss | Chapter | Theme Type | Ace level | Team | AI tier | Care-item uses | Format |
|---|---|---|---|---|---|---|---|
| 1 | 1 | Wild | 12 | 2 | Trainer | 1 | 1v1 |
| 2 | 2 | Grove | 22 | 3 | Boss | 1 | 1v1 |
| 3 | 2 | Tide | 22 | 3 | Boss | 1 | 1v1 |
| 4 | 3 | Stone | 34 | 4 | Boss | 2 | 1v1 |
| 5 | 3 | Volt | 34 | 4 | Boss | 2 | **2v2** |
| 6 | 3 | Frost | 34 | 4 | Boss | 2 | 1v1 |
| 7 | 4 | Lumen | 44 | 5 | Boss | 2 | 1v1 |
| 8 | 5 | mixed | 52 | 6 | Boss | 3 | 1v1 |

- **Ace level** is the highest level on the team. The others sit 1–3 levels below.
- **Type identity:** most of each team shares the Boss's theme Type. **From Chapter 3 on**, each team adds **one off-type "coverage" Creature**, so a single counter-pick can't sweep it and switching pays (pillar 5). Boss 8 has a mixed team.
- **Unthemed Types: Flame, Gale, Shade.** They are left for Area challenges, the rival and the antagonist. Shade is free to become the Blight faction's Type in the Story & world fog.
- **Boss 5** is a pair of Menders sharing **one Boss record**: one flag, one prize, one +1 to Bosses beaten. Volt support moves suit 2v2 (one Creature charging while the other strikes). *(Ticket 21: the charge is the Volt `empower_ally` move plus a self-or-ally `energy` move, built from data, not special code.)*
- The player's whole Party of 6 is always allowed, whatever the Boss's team size.
- A Boss's home Area should suit its Type (a Tide Boss by water). The World structure fog places it.
- Losing to a Boss follows ticket 07 (money loss, immediate retry).

### What beating a Boss gives
- **Its flag** (Restoration stage 1 and the opened routes).
- **The Marks prize:** 100 × the ace level (ticket 14).
- **+1 to Bosses beaten**, which drives shop stock (ticket 14) and the challenge-mode cap table.
- A **crest on the Region map** that lights up. It is purely cosmetic.
- Nothing else: no badges with stat effects, no move-teaching items, no gift Creature.

### Showing Bosses
On the Region map, every **reachable** unbeaten Boss shows its theme Type icon and ace level ("Grove · Lv 22"). Bosses in Locked Areas show as "?".

### Level curve
With **L** the current Chapter's ace level and **P** the previous Chapter's (P = 5 for Chapter 1, the starter level):

| Chapter | Ace level L | Expected party level | Wild levels (P − 1 to L − 4) | Trainers | Area challenges | Play time to reach (cumulative) |
|---|---|---|---|---|---|---|
| 1 | 12 | 10 | 4–8 | ≤ 10 | 14 | ~1.5 h |
| 2 | 22 | 20 | 11–18 | ≤ 20 | 24 | ~5 h |
| 3 | 34 | 32 | 21–30 | ≤ 32 | 36 | ~12 h |
| 4 | 44 | 42 | 33–40 | ≤ 42 | 46 | ~16 h |
| 5 | 52 | 50 | 43–48 | ≤ 50 | 54 | ~19 h |

- **Expected party level** = L − 2. It is what a player reaches by fighting only what's on the way, with no grinding. The XP constants from ticket 07 are tuned to it, and the simulation gates use it.
- Later Restoration stages may add **+1–2 at the top** of an Area's wild band. **Payoff Creatures** (ticket 12) sit at L.
- The strongest trainers stand nearest the Boss.
- Area challenges are optional and deliberately above the Boss.
- Starter level 5 is a starting value; ticket 16 may adjust it.

### Boss 1 is beatable with every starter
This is a **test, not a Type restriction**, so the starter trios in ticket 16 stay free:
- A headless scenario on the seeded core (ticket 09) runs, for **every starter in every trio**, a bot party: the starter plus the **two most Common species from the Areas before Boss 1**, all at the expected level (10).
- The bot must win at least **70% of 200 seeded runs**, or the content tests fail.
- Boss 1 runs on **Trainer-tier AI** with 2 Creatures.
- The same harness can later run every Boss against an "expected party" as a balance report.

### Postgame rematches
- Each Boss has **one rematch team** in data: a full 6 with Boss-tier AI. The theme is kept, with two coverage picks.
- Fixed levels: **58** (Bosses 1–3), **61** (Bosses 4–6), **63** (Boss 7), **66** (Boss 8).
- Fought at the Boss's own location, **once per in-game day**, shown by an idle cue when ready.
- Prize: **50 × the highest level** (about 3,000 Marks). This is a token amount, because money already piles up late.
- No rematch ladders in v1. A second rematch set can come with the Large scale.

### Room for challenge mode (data only in v1)
- A **level-cap table keyed to the number of Bosses beaten**. Its rule is: cap = the ace level of the lowest Chapter with a Boss still unbeaten.

  | Bosses beaten | 0 | 1–2 | 3–5 | 6 | 7 | 8 |
  |---|---|---|---|---|---|---|
  | Cap | 12 | 22 | 34 | 44 | 52 | 100 |

- In challenge mode, **XP stops at the cap**. A Creature over the cap can't occur, because the linter checks that no reachable wild Creature or gift is above it.
- Each Boss record has an optional **`challenge_team`**. When it's absent, the normal team runs with the AI one tier up (ticket 07).
- v1 ships the table and fields filled in, with no menu option.

### Data
- There is **no progression record and no Boss-order list.** Which Bosses are on offer follows only from **which Areas are reachable**, and reachability comes from the stage-1 flags that clear Blight barriers. Chapters are a design convention the linter checks. See ADR 0003.
- The **region record** holds only:
  - its **Boss list** (for the Bosses-beaten count and the Region map)
  - the **level-cap table**
  *Amended 2026-11-14 by ticket 25 ("Which way do the spec's seven conflicts go?"): it also holds the **unordered set of its Areas** (ticket 18), which the per-region Region map, Restoration % and dormant-exit check need. It still holds no order list.*
- **Boss records** (JSON, permanent IDs, ticket 09):
  - team and format
  - AI tier and Care-item uses
  - its flag
  - its home Area
  - `rematch_team`
  - optional `challenge_team`
- Prizes come from the formulas, never hand-set.
- Gates and story beats are **events** from the closed command list (ticket 09).
- A second region is content only.

### Linter checks added
Walking the Area graph from the new-game state:
1. Every barrier's flag is set somewhere reachable before the barrier.
2. Each Boss becomes reachable, and **each Boss in a Chapter can be reached without beating the others** in it.
3. Every Area with stages gets its stage 1 from some reachable flag before the finale.
   *Amended 2026-11-14 by ticket 25 ("Which way do the spec's seven conflicts go?"): **the finale's own `boss_8` flag counts**, so the check reads "every Area with stages gets its stage 1 from a reachable flag", and 100% region Restoration is always possible in the postgame.*
4. **At least 2 catchable species with a 2× edge over each Boss's theme Type** are reachable before that Boss.
5. Wild, trainer and Area-challenge levels fit the bands above.
6. No reachable wild Creature or gift is above the cap for the Bosses-beaten count at that point.
7. The Boss 1 simulation gate passes for every starter in every trio.

The economy check from ticket 14 runs against this same walk.

### Follow-ups
- **New ticket 18**, "How is the region laid out?", graduated from the World structure fog.
- **New ticket 19**, "Which tool authors Area maps, and how do they become content data?", graduated from the World structure fog.
- Ticket 16 (roster structure): Boss-team and counter needs, and the Boss 1 simulation gate on every trio.
- Ticket 17 (builds and release): the simulation gate runs in CI.
- Story & world fog: the 5 Chapters, combined-flag story beats, the rival and antagonist on Flame, Gale and Shade.
- ADR 0003 (Boss order comes from reachability).
