# What items exist, and how does the economy work?

Type: grilling
Status: resolved
Blocked by: none

## Question

Specify the item and economy design:
- **Currency:** one currency or several, and what it's called (ticket 06 left the currency name to this ticket).
- **Income sources:** trainer rewards, selling, finds, postgame.
- **Shops:** what each town sells, how stock grows with progress and Restoration.
- **Item categories:** healing and Status cures, **Lure tiers and Habitat-specific Lures**, held items (if any), key items, and anything Bond- or Trait-related.
- **Prices and bag limits.**
- Whether items can be **used outside battle**.

Already fixed:
- Ticket 07: an item uses up the Creature's turn; trainers and Bosses have a fixed number of item uses in their battle data; Rest points heal for free; losing costs 8 × the Party's highest level × (Bosses beaten + 1), capped at 50% of money carried.
- Ticket 08: Lures are the capture tool, with tiers plus Habitat-specific types; a failed Lure is used up.

Must respect "Respect the Player's Time" (no grinding needed for money) and the out-of-scope ruling: no monetisation. Items are data.

Added from ticket 12 (How does Restoration change an Area?): each Restoration stage may add **shop stock** in its Area, so shop growth can be keyed to stages as well as Bosses. Restoration itself never rewards money or items.

Added from ticket 13 (How does Bond shape a Creature?): **no item affects Bond rank, Leanings or Traits**. There are no Bond treats, needle re-centring items or branch-forcing items; Bond is earned only by raising the Creature.

Added from ticket 06 (What are the game's title and the in-world name for Creatures?): the Lure's in-world name is **Offering**, so tiers and Habitat variants read as "<X> Offering". Item data keeps the generic `lure` kind. A currency name should fit the family of plain English words (Mender, Mending, Haven, Almanac).

Added from ticket 09 (What is the technical architecture?): each item is a **JSON record** (`content/items/<id>.json`) with a permanent snake_case ID, its icon found by convention at `assets/items/<id>.png`, and its display text in strings. Item effects should be built from a **closed list of effect kinds** in code (like Mending kinds and Leaning axes), so new items need no code. Shop stock and prices are data on the shop or Area record. The save stores only the bag (item ID → count) and money.

## Answer

Resolved by grilling with the human (2026-11-14). Builds on ticket 05 (pillars), ticket 07 (battle), ticket 08 (catching), ticket 12 (Restoration), ticket 13 (Bond) and ticket 09 (architecture). Terms are defined in `GLOSSARY.md`: Money, Forage, Habitat Lure, Lure, Rest point, Hidden site. **Every number is data with a starting value, tuned in playtesting.**

### Money
- **One currency.** Code and data call it `money`, and it displays as **Marks** (a string, so a rename is one edit). There are no second tokens, crafting materials or premium currency. Display cap 9,999,999.
- **Income is one-off:**
  - **Trainers:** a prize of class base (16 for a casual trainer, up to 48 for a veteran) × the highest level on their team.
  - **Area challenges:** 60 × level. **Bosses:** 100 × their highest level. Boss rematch prizes belong to the Bosses ticket.
  - **Visible item spots:** pickups on the map, each taken once. **There are no invisible items.**
  - **Selling:** 50% of the buy price. Key items can't be sold. Forage has its own low sell price.
- **Wild battles pay no money**, so battling wild Creatures over and over is never a money strategy.
- **Hidden sites give no money or items.** Their reward is the Mending plus Collection log or story flavour, which keeps the Restoration ticket's rule that Restoration never pays money or items.
- **The only money sink in v1** is the defeat loss from ticket 07. Late-game money piling up is accepted; see Out of scope on the map.

### Renewable floor
- **Forage:**
  - Forage spots are map marker nodes with an ID and a small item table filtered by Habitat and time of day. Each shows as a plant sprite that looks empty once picked.
  - A spot **regrows one in-game day** (~24 min of play) after picking. Its yield is rolled from the seeded `Rng`.
  - Yields are Care items: a small heal herb, a cure berry for one Status, and occasionally a rare Energy fruit. They sell for about 20–40 Marks.
  - **Restoration adds Forage spots.** A Blighted Area has few or none, and stages 2+ add more (part of each stage's Habitat-patch changes).
  - The save stores the in-game day each spot was last picked. Regrowth is derived.
- **Lure safety net:** resting at any Rest point while holding **zero Lures of any kind** gives **3 basic Lures**, with a line of NPC flavour. There's no cooldown, since it only fires at zero. Who gives them goes to the Story & world fog.
  *Amended 2026-11-14 by ticket 22 ("What is Mendvale's story, and which beat sets each flag?"): the Lantern-keeper at that Rest point gives them ("Hollis asked us to keep a few spare for you.").*

### Items
Each item's effect is built from a closed list of effect kinds in code (`heal_hp`, `cure_status`, `revive`, `restore_energy`, `lure`, `key`), so new items are data only.

| Item | Price | Effect | Use |
|---|---|---|---|
| Basic Lure | 200 | catch ×1 | battle |
| Better Lure | 600 | catch ×1.5; in shops after 2 Bosses | battle |
| Best Lure | 1,200 | catch ×2; in shops after 5 Bosses | battle |
| Habitat Lure (one per Habitat kind) | 1,000 | catch ×2.5 if the target's Habitat matches, ×1 otherwise | battle |
| Small / medium / full heal | 150 / 450 / 1,000 | 30% / 60% / 100% of max HP | anywhere |
| Single-Status cure (one per Status) | 150 | clears that Status | anywhere |
| All-cure | 500 | clears any Status | anywhere |
| Revive | 1,200 | revives at 50% HP | anywhere |
| Energy tonic | 400 | +50% of max Energy | battle |
| Forage items | n/a (20–40 sell) | Care effects as above | anywhere |
| Key items | n/a | story and progression; never consumed or sold | through the world |

- **Heals are percentages**, so they never go stale as levels rise.
- **No guaranteed catch.** The 1–95% clamp from ticket 08 holds for every Lure, and rare one-off Creatures keep their low base rate.
- The list of **Habitat kinds** (and so of Habitat Lures) waits for the World-structure fog.
- **Deliberately absent from v1:** held items (Traits fill the passive slot), stat-stage boosters, move-teaching items, evolution items, repels, escape items, and anything affecting Bond or Traits (ticket 13).

### Shops
- **One shop per town.** Camps and route Rest points sell nothing, and there are no wandering vendors in v1.
- **Stock** = a base list + **global additions by number of Bosses beaten** (better Lure tiers, stronger heals) + **local additions by that Area's Restoration stage** (Habitat Lures from stage 2, local Forage goods).
- **The same prices everywhere.** All of this is data on the town or Area record.

### Bag
- **No capacity limit**, 99 per stack. At 99, a pickup is refused and the spot stays full, and buying stops at 99.
- **Three pockets:** Care, Lures, Key.
- Care items are usable from the Bag outside battle. Lures only work in battle. Key items are used through interaction or the story, never from a menu "use" button.
- **Starting kit:** 1,000 Marks, 5 basic Lures, 3 small heals.

### Trainers' items
- Trainers and Bosses use **Care items only** (never Lures or Energy tonics), from a per-battle list in their data that is separate from the player's bag. The count of uses is already fixed by ticket 07.
- **One shared rule for every AI tier:** heal a Creature below 30% HP if its expected damage this turn won't KO the foe.
- Every use is **announced** in battle text.

### Data, save and lint
- The save stores only the **bag** (item ID → count), **money**, item spots taken, and each Forage spot's last-picked day. Shop stock is derived from Bosses beaten and Restoration stages.
- The content linter adds a **balance check**: critical-path income up to each Boss (trainers, challenges and item spots on the way) must cover a target shopping list for that point.

### Follow-ups
- Bosses ticket: Boss prize formula, rematch prizes, and stock unlocks keyed to Bosses beaten.
- World-structure fog: item-spot and Forage-spot markers, and the Habitat kind list (which sets the Habitat Lures).
