# What is Mendvale's story, and which beat sets each flag?

Type: grilling
Status: resolved
Blocked by: none

## Question

Specify the story of the Medium region well enough that every event and set encounter can be written as data:
- **Setting and tone:** the region's name and history, what the Blight is and why it came, and the protagonist's reason to mend it. Cozy to adventurous, for 13+ (ticket 05).
- **Cast:** the 8 Bosses (who they are, why each guards their landmark), the rival, and the antagonist faction. The rival and antagonist use the unthemed Types **Flame, Gale and Shade** (ticket 15), and Shade may become the Blight faction's Type. No starter line may be on a trainer or Boss team before Chapter 3 (ticket 16), which affects whether the rival uses a starter.
- **The beat behind every flag** from ticket 18:
  - `starter_chosen`, and a framing for why a random Starter trio is on offer (ticket 08)
  - `chapter_2_open` to `chapter_5_open`, including the combined-flag beats after Chapters 2 and 3
  - each Boss win, and the `boss_8` finale and credits
- **The postgame:** what Bosses and NPCs say once the region heals, and a story reason for the 2 rare one-offs waiting at `observatory` and `source`.
- **Who gives the 3-Lure safety net** at Rest points (ticket 14).
- **Display names** for the region and its 33 Areas (working IDs in ticket 18), in the plain-English register of Mendvale, Verdling and Mender (ticket 06).
- How the story leaves room for a second region reached by the dormant ferry at `harbour`.

Already fixed:
- **Ticket 05:** a broken region the player restores, the Restoration hook, the 5 pillars, and a string-of-pearls Boss order.
- **Ticket 15:** 5 Chapters of 1 / 2 / 3 / 1 / 1 Bosses with their theme Types, ace levels and formats (Boss 5 is a pair of Menders in 2v2).
- **Ticket 18:** the hub-per-Chapter layout, the 33 Areas, the 5 Blight barriers and what each flag restores. Each hub is lived in Blighted and heals as its Chapter closes. The home town was never Blighted. The finale landmark `source` is where the Blight comes from.

## Answer

Resolved by grilling with the human (2026-11-14). Builds on ticket 05 (pillars), ticket 06 (naming), ticket 07 (battle), ticket 08 (catching), ticket 12 (Restoration), ticket 14 (economy), ticket 15 (Bosses), ticket 16 (roster) and ticket 18 (region layout). New terms are defined in `GLOSSARY.md`: Region, Blight, Wellspring, Root, Faction, Rival, Mentor, Lantern-keeper, and Steward as the in-world name for a Boss. **Every name is a display string** in `strings/en.csv`, and every level and count is data with a starting value.

### How the story is told
- **Medium weight.** Short beats at each flag, plus one running thread (the rival and the Yield) through the Chapter transitions. Most of the story is told by the world: NPC lines that change with each Restoration stage, and hidden-site flavour (pillar 1).
- **Budget:** a flag beat is **≤ 60 seconds** of reading (about 8–12 `say` lines). Story text can be fast-forwarded but not skipped.
- Every beat is built from the closed command list (`say`, `move_actor`, `set_flag` …) on existing sprites. There's no cutscene art.
- The tone runs from cozy to adventurous, for 13+. The antagonists are **misguided, not evil**.

### Setting
- **The region is Mendvale**, a long vale with a river running south from **the Wellspring** at its northern heart (`source`). The Region map reads bottom to top.
- **The Blight.** About 30 years ago, in a drought year, the Wellspring's own Steward tapped it to make Verdlings grow faster and stronger: forced, not raised. The spring soured, and the Blight has crept south ever since. It leaves Areas and their Verdlings muted and quiet, never monstrous. This is pillar 2 ("Raised, Not Rolled") as the villain's mistake.
- **The roots.** Each landmark holds a **root**, one of the springs the Wellspring once fed. When the Blight came, each Steward put their root to sleep so the Blight couldn't drink from it, and has guarded it since. A Steward won't wake it until a Mender's team proves its Bond. **Beating a Boss is that proof:** afterwards the Steward and the player wake the root together, and the spoke heals outward (ticket 12's ring animation). The landmark's focal point is its root.
- **Lowfold (`home_town`) was never Blighted** because the Blight simply hasn't reached it yet. It reached Wellside Lane (`route_1`) this spring. Young Verdlings fleeing south shelter in Lowfold. The creeping happens before the game starts: during play nothing ever re-Blights (ticket 05).
- **No "Blight" Type.** The faction uses Shade (this settles the open note in ticket 07).

### Cast
| Role | Name | Who |
|---|---|---|
| Protagonist | player-named | A young Mender who grew up in Lowfold, set on going north. Mostly silent: occasional choice lines that change nothing. **2 looks** in v1 (data). |
| Mentor | Hollis | Lowfold's innkeeper, a retired Mender who sends the player north. Their old field notebook becomes the **Almanac**. Not a professor: no lab and no handout speech. |
| Rival | Bryn | A Lowfold friend who leaves the same morning, too impatient to wait for a Starter (see Rival). |
| Steward 1, `warren` (Wild) | Pip | Young; inherited the root from a parent last year. Nervous and earnest. |
| Steward 2, `elder_tree` (Grove) | Hazel | An old forester, slow-spoken. The Yield asked for this root and was refused. |
| Steward 3, `tide_shrine` (Tide) | Marlow | A cove fisher, blunt and warm. |
| Steward 4, `quarry` (Stone) | Slate | The quarry boss, proud of the work. |
| Steward 5, `storm_tower` (Volt, 2v2) | Sparrow and Kit | Siblings who rebuilt the tower. They bicker constantly and fight as one (one Boss record, ticket 15). |
| Steward 6, `glacier` (Frost) | Tarn | A mountain guide, laconic. |
| Steward 7, `lighthouse` (Lumen) | Morrow | Weller's oldest friend, who carries the guilt of not stopping them. |
| Steward 8, `source` (mixed) | Weller | Founder of the Yield and the Wellspring's own Steward 30 years ago. |
| Faction | the Yield | Members are **Yield hands** (see The Yield). |
| Rest-point NPC | Lantern-keeper | One NPC record used at every inn and camp. |
| Ferry | Ferry operator | At `harbour`'s dormant exit. |

- **All text is pronoun-free** for the protagonist and every named character. All names are gender-neutral.
- **Name entry:** a free text field of up to 10 characters, plus a **🎲 button** that suggests a name from a short gender-neutral list (data).

### The Yield
- A misguided faction that believes the tap failed only because it was too timid. It wants to tap the Wellspring "properly" and give the vale strong Verdlings overnight. Its motto: "the vale needs strength, not patience."
- **Teams:** Shade-led, with some Flame.
- **Forced Verdlings are flavour only:** ordinary species records within the level bands, with quiet, tired idle lines. There's no special Status, Trait or rule.
- **Yield hands are ordinary trainer records.** They count toward their Area's "beat the trainers here" Mending.
  - Chapters 2–4: 2–3 per Chapter.
  - Chapter 5: they hold `blight_heart`, filling its 3–5 trainers.
  - There is no separate faction system.

### Starters and the gift
- **Why the trio is random:** which three young Verdlings are sheltering in Lowfold this season varies, which is the per-save seed (ticket 08). The player picks one, and **the other two slip off north**. That's why every starter turns up Rare in Chapter 2–3 Areas (ticket 16).
- **The gift:** Hollis hands over the Almanac and ticket 14's **starting kit, unchanged** (1,000 Marks, 5 basic Lures, 3 small heals).
- **The Lure safety net** (ticket 14) is given by the **Lantern-keeper** at whatever Rest point it fires: *"Hollis asked us to keep a few spare for you."*

### Beat sheet
| Flag or moment | Where | Beat |
|---|---|---|
| New game | Lowfold inn | Hollis: the Blight reached Wellside Lane this spring, and Verdlings are sheltering here. Name and look are chosen. Bryn bursts in and leaves to "fix it first", with no Starter. |
| `starter_chosen` | Lowfold → Wellside Lane's edge | Pick 1 of the 3 sheltering Verdlings; the others slip off north. Hollis gives the Almanac and the kit. Player and Starter tend the dried spring (the route's focal point), the tutorial Restoration plays, and the barrier clears. |
| `boss_1` | Burrow Hill | Pip wakes the first root with the player and explains the Wellspring, the Stewards and the sleeping roots, then points north. The win event sets `chapter_2_open` (Dryford Road heals). |
| Rival battle 1 | Dryford Road | Bryn, on Gale and Flame, is proud of a team caught on the road. |
| First Yield sighting | Mossway / The Deepwood | Yield hands stripping Forage. |
| `boss_2` | The Elder Tree | Hazel wakes the root. Lore: the Yield asked for it. |
| `boss_3` | Tide Shrine | Marlow wakes the root. Lore: the Wellspring soured about 30 years ago. |
| `chapter_3_open` (combined) | Wherever the second Chapter-2 Boss falls | That Steward: "Both roots awake; Millbrook will feel it." Millbrook heals through the pending-presentation queue the next time the player enters. The Ridgeback Road barrier clears. |
| Rival battle 2 | Ridgeback Road | Bryn now has a forced Shade Verdling from the Yield and is winning fast. Loses anyway and leaves rattled. |
| The Yield in Chapter 3 | The Sunken Works | Restarting old pumps that once piped water north toward the Wellspring. |
| `boss_4`, `boss_5`, `boss_6` | Greystone Quarry, Storm Tower, Frostcrown Glacier | Each wakes its root. Tarn has seen Yield hands heading for the coast. |
| `chapter_4_open` (combined) | Wherever the third Chapter-3 Boss falls | That Steward sends the player to the coast. Threeways heals; the Seawind Road barrier clears. |
| Rival battle 3 | Seawind Road | Bryn's Shade Verdling is struggling. After the loss, Bryn sees it, turns from the Yield, and starts raising it properly. |
| Optional reveal | Starwatch | Old notes show the Yield's founder was the Wellspring's own Steward, who tapped it in a drought year. |
| `boss_7` | Lastlight | Morrow tells Weller's story outright, whether or not the notes were found. The win event sets `chapter_5_open` (Saltharbour and Coldstep Road heal). |
| Tag battle | The Hushed Halls entrance | Bryn joins the player against a Yield pair in a 2v2. Afterwards Bryn stays at Highwatch. |
| `boss_8` | The Wellspring | Weller fights to finish the tap. After the loss, Weller and the player wake the Wellspring together, and Weller stays to tend it. The Hushed Halls, The Wellspring and Highwatch heal. Credits. |

- A combined flag's beat plays right after the Boss win that completes it, at that landmark. The hub's Restoration then plays the next time the player enters it (ticket 12's queue).

### Rival
- **Gale and Flame** from Chapter 1, plus the forced **Shade** Verdling from rival battle 2 on. Bryn **never uses a Starter line**, so ticket 16's "no Starter line on a trainer team before Chapter 3" holds trivially. It also skips the counter-pick cliché, which a random trio would make awkward.
- **Levels:** rival battles 1–3 sit where a Chapter opens, so the ace is **the previous Chapter's ace + 1**, with the rest 1–2 levels below:

  | Battle | Where | Team | Ace | AI tier |
  |---|---|---|---|---|
  | 1 | Dryford Road | 2 | 13 | Trainer |
  | 2 | Ridgeback Road | 3 | 23 | Trainer |
  | 3 | Seawind Road | 4 | 35 | Boss |
  | Tag (ally) | The Hushed Halls | Bryn's own | 46 | Boss |
  | Postgame friendly | Highwatch | 6 | 60 | Boss |

  The Yield pair in the tag battle is at ≤ 50. All of these fit ticket 15's trainer ceilings.

### Tag battle: an AI ally slot
- A set encounter's side gains an **optional per-slot controller**: `player` (the default) or an AI tier. `BattleAI.choose` already takes a side and tier; this narrows it to a slot.
- In the tag battle, Bryn's slot sends Creatures from Bryn's team and the player's slot sends from the Party, one at a time. **The player loses when the Party is out.** If only Bryn's team is out, the player fights on alone.
- Bryn's Creatures gain no XP or Bond. The ally's slot shows its own HP and Energy bars but takes no player input.
- This is reusable later (for example, a pair of Menders joining the player).

### Postgame
- **Stewards:** one new line each when their rematch is ready ("The root's strong now. Want to see what it's grown?").
- **NPCs:** each Area's final-stage lines, written with that Area.
- **Weller** tends the Wellspring at `source`.
- **Bryn** stays at Highwatch raising the Shade Verdling and offers a friendly battle **once per in-game day**, shown by the rematch idle cue. Bryn is a trainer record with a rematch-style team, not a Boss: no Bosses-beaten count, and the prize is ticket 15's rematch formula (50 × the highest level).
- **Rare one-offs (ticket 18):**
  - **Starwatch** (stage 3): the Verdling young Weller was studying, seen in the notes. It returns once the observatory is fully restored.
  - **The Wellspring** (stage 2): the Wellspring's own Verdling, which wakes once the spring is healed.
- **The ferry at Saltharbour:** the operator says boats stopped when the Blight came. After the finale they add: *"Word from across the water: their shore's gone quiet too."* That's a hook with no promise. A second region wakes the exit with an event (ticket 18).

### Display names
The region is **Mendvale**. Interiors are named after their parent ("Lowfold Inn"). The names were checked against well-known Pokémon character names (Rowan, Oak, Alder, Birch, Elm, Willow, Flint and Ash were dropped) and avoid "haven", the Sanctuary's in-world name.

| ID | Name | ID | Name | ID | Name |
|---|---|---|---|---|---|
| `home_town` | Lowfold | `tide_shrine` | Tide Shrine | `ice_cave` | Rimefall Cave |
| `route_1` | Wellside Lane | `route_6` | Ridgeback Road | `glacier` | Frostcrown Glacier |
| `route_2` | Reedwood Trail | `hub_3` | Threeways | `route_10` | Seawind Road |
| `warren` | Burrow Hill | `route_7` | Shale Trail | `harbour` | Saltharbour |
| `route_3` | Dryford Road | `old_mine` | Tinmouth Mine | `route_11` | Cliffside Path |
| `hub_2` | Millbrook | `quarry` | Greystone Quarry | `observatory` | Starwatch |
| `route_4` | Mossway | `route_8` | Old Works Road | `lighthouse` | Lastlight |
| `deepwood` | The Deepwood | `sunken_works` | The Sunken Works | `route_12` | Coldstep Road |
| `elder_tree` | The Elder Tree | `storm_tower` | Storm Tower | `outpost` | Highwatch |
| `route_5` | Saltmarsh Path | `route_9` | Highpass Trail | `blight_heart` | The Hushed Halls |
| `cove_town` | Gullcove | `peak_village` | Cloudrest | `source` | The Wellspring |

Area IDs stay as they are (ticket 09: IDs are permanent, names are strings).

### Linter checks added
1. No Starter line on Bryn's teams.
2. Rival battles 1–3 sit at the previous Chapter's ace + 1. Every rival and Yield team fits the derived Chapter's trainer ceiling.
3. A set encounter with an AI-controlled slot on the player's side has exactly one `player` slot.

### Follow-ups
- **Ticket 07** (battle) amended: the per-slot controller and the tag-battle rules; no "Blight" Type.
- **Ticket 08** (catching) amended: the Starter framing.
- **Ticket 09** (architecture) amended: the optional `controller` on a set-encounter slot.
- **Ticket 14** (economy) amended: the Lantern-keeper gives the Lure safety net.
- **Writing every event and each Area's per-stage NPC lines** is implementation work for the slices, past this map's destination.
