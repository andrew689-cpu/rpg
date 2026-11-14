# How is the move list structured?

Type: grilling
Status: resolved
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

## Answer

Resolved by grilling with the human (2026-11-14). Builds on ticket 03 (research menu), ticket 07 (How does a battle work?), ticket 13 (How does Bond shape a Creature?), ticket 15 (Bosses) and ticket 16 (How is the Creature roster structured?). Terms are defined in `GLOSSARY.md`: Power move, Focus move, Basic move, Energy, Status, Bond move, Signature move, Type. **Every number is data with a starting value, tuned in playtesting.**

### Fixes to the battle maths (ticket 07 amended)
- **Damage has a level term:** `power × attacker level × attack ÷ defence × k × modifiers`. Because stats and HP both grow with level, a move of a given power takes the same share of an equal-level foe's HP all game long. Power bands therefore never creep; later moves get better through tiers and side effects.
- `k` is set so that a move of power P takes about **P ÷ 3 % of HP** from an equal-level, neutral target, with a mid roll and no same-type bonus. The Basic move does about 10%.
- **Energy is a flat species value, not scaled by level.** A typical max is about 100 (Casters and Wardens about 120–140, Bruisers about 80). It changes only when the Creature evolves. Move costs are absolute, and regen stays at 20% of the Creature's own max, so a high-Energy Creature really does fire more big moves.
- **Every move is a Power or a Focus move**, including moves that deal no damage, chosen by flavour (a war-cry is Power, a ward is Focus). Style Leaning therefore counts every move use, and the "a Power and a Focus move before the first evolution" rule may be met by a move that deals no damage.
- **The Basic move uses whichever of the user's Power and Focus is higher**, against the matching defence. It still never moves a Leaning.
- **A crit does 1.5×**, and only a move whose card shows a `crit_pct` can crit.
- **The 75% spread penalty applies only when a move actually hits 2 or more targets.** In 1v1 an all-foes move does full damage.

### The move record
One JSON file per move (`content/moves/<id>.json`):

```json
{
  "id": "cinder_nip",
  "type": "flame",
  "category": "power",
  "tier": "weak",
  "pool": "level_up",
  "power": 40,
  "cost": 15,
  "accuracy": 100,
  "target": "one_foe",
  "priority": 0,
  "crit_pct": 0,
  "effects": [{ "kind": "inflict_status", "status": "burn", "chance": 20 }],
  "anim": "bite"
}
```

- `category`: `power` or `focus`.
- `tier`: `weak`, `mid`, `strong`, `finisher` or `signature`. It's explicit so the linter knows which band to check. Moves with no damage and all-foes moves take the tier nearest their cost.
- `pool`: `level_up`, `bond_only` or `signature`.
- `power`: 0 for a move with no damage.
- `target`: `one_foe`, `all_foes`, `one_ally`, `self`, `self_or_ally` or `all`. `all` (both sides) is only for moves with no damage in v1, so no damaging move hits its own ally.
- `priority`: only −1, 0 or +1.
- `crit_pct`: 0 unless shown on the card.
- `anim`: one of a closed list of about 12 code effects (`strike`, `slash`, `bite`, `burst`, `beam`, `orb`, `wave`, `rain`, `quake`, `gust`, `aura`, `shield`), tinted by the Type's colour. Move visuals need no art.

### Closed list of effect kinds
A new effect kind needs code; a new move is data only.

| Kind | Parameters |
|---|---|
| `inflict_status` | Status, chance % |
| `stat_stage` | self, target or ally; stat; ±1 or ±2; chance % |
| `heal` | self or ally; % of max HP |
| `drain` | % of the damage dealt, healed by the user |
| `recoil` | % of the damage dealt, lost by the user |
| `energy` | add to self or ally, or drain from a foe; a fixed amount |
| `cure` | clears the Status of self or an ally |
| `reset_stages` | clears the target's stat stages |
| `empower_ally` | the ally's move this turn does ×1.5 |
| `redirect` | this turn, single-target foe moves hit the user |
| `condition_boost` | ×1.3 power when the battle's time of day, weather or Habitat matches |

- **Readability limit:** a damaging move has **at most one side effect**, and a move with no damage has **at most two effects**, so every card fits in one line.
- **Left out of v1:** setting weather or terrain (weather belongs to the world and Restoration), Protect-style full-block turns, one-hit KOs, multi-hit, two-turn charge or recharge, forced or self switching, type changes, copying moves, fixed damage, field hazards, and **bonuses based on the ally's Type** (Temtem's signature "Synergy", flagged by ticket 03).

### Size and per-Type grid: 144 moves
Each Type has the same **11 level-up moves**:

| Slot | Power | Focus |
|---|---|---|
| Weak, single target | 1 | 1 |
| Mid, single target | 1 | 1 |
| Strong, single target | 1 | 1 |
| Finisher, single target | 1 | 1 |
| All-foes damage (mid tier) | 1, either category | |
| Moves with no damage (stat, Status, support) | 2, either category | |

- 3 of each Type's 8 single-target damage moves carry a side effect.
- **110 level-up moves**, plus **20 Bond-only** (2 per Type: 1 damaging with a side effect, 1 with no damage), plus **14 signature moves**, for **144** in total.
- That gives about **42% pure damage, 37% damage with a side effect and 21% with no damage**.
- Every Type has a Power and a Focus move at every tier, so the Style rule can always be met with a line's own Type.
- The grid is a **floor** the linter checks, not a ceiling. Large adds moves freely.

### Bands
These go in one global tuning file, `content/tuning/move_bands.json` (`k`, the bands and the reference %). Assumptions: a typical max Energy of 100 and regen of 20 per turn.

| Tier | Power | Cost | Accuracy | ≈ % HP, same-type, neutral |
|---|---|---|---|---|
| Basic | 30 | 0 | 100 | 10 |
| Weak | 50 | 15 | 100 | 21 |
| Mid | 75 | 30 | 100 | 31 |
| Strong | 100 | 45 | 95 | 42 |
| Finisher | 130 | 60 | 90 | 54 |

- What each extra point of Energy buys over the Basic move is flat across the tiers (about 2.1–2.2 power per Energy). Finishers trade that efficiency for tempo, with a miss risk.
- A weak move every turn can be kept up forever. A typical fight lasts 3–5 turns. A same-type, super-effective finisher takes about 100% of an equal-level foe's HP.

**Pricing side effects and specials:** each one costs **one step** of power at the same Energy cost, unless noted. A step is about 20% of the tier's power (weak 50 → 40, mid 75 → 60, strong 100 → 80, finisher 130 → 105). A whole tier down would leave a weak move with a side effect at the Basic move's 30 power, which costs nothing.

| Effect | Band |
|---|---|
| Status on hit | 20% / 30% / 50% chance; never 100% on a damaging move |
| Status-only move | 100% chance, 90% accuracy, cost 30 (Drowsy: 45) |
| Stat stage on hit | +1 self or −1 foe, at 30% or 100%; ±2 only on moves with no damage |
| Stat-only move | ±1 for cost 20, ±2 for cost 35 |
| Priority +1 | power 40, cost 20; about 5 in total |
| Priority −1 | only a few strong Stone and Wild moves, one step **higher** |
| Crit | `crit_pct` 25 on the card, one step lower; about 6 in total |
| Drain | heals 50% of the damage dealt, one step lower |
| Recoil | 25% of the damage dealt, one step **higher** |
| Heal | 25% (cost 30) or 50% (cost 50) of max HP, never more |
| `empower_ally` | cost 20 |
| `redirect` | cost 25, priority +1 |
| `condition_boost` | ×1.3, no power cost; about 1 per Type |

The linter checks each move against its band, within a tolerance.

### When each tier becomes available
"Every stage of the game" comes from *when* moves are learned, not from power creep.

| Tier | Earliest level on a level-up list | Earliest Bond rank |
|---|---|---|
| Weak | 1 | 1 |
| Mid | 12 | 2 |
| Strong | 25 (Chapter 3) | 3 |
| Finisher | 36 (Chapter 4) | 4 |
| Signature | n/a | 5 only |

This puts finishers before Bosses 6–8.

### Type identity
A design guide: a Type's side effects and moves with no damage come mostly from what it "owns".

| Type | Statuses | Leans on |
|---|---|---|
| Flame | Burn | recoil, Power up |
| Tide | – | heal, cure, Guard up |
| Grove | Poison, Snare | drain, heal |
| Gale | – | priority, Speed up/down |
| Stone | – | Guard up, recoil, redirect, −1 priority |
| Volt | Fatigue | `energy`, `empower_ally`, crit |
| Frost | Chill | Speed down, Will up |
| Shade | Snare, Drowsy | drain, `energy` drain, crit |
| Lumen | Drowsy | cure, `reset_stages`, Will up |
| Wild | – | Power up, recoil, priority |

The linter checks only one rule from this table: a Status sits on its 1–2 home Types, and each other Type borrows **at most 1 move per Status**.

### Bond-only and signature moves
- **Bond-only moves** (`pool: bond_only`, 20) never appear on any level-up list. They give off-type coverage and stronger side effects. A form's Bond list may use Bond-only moves and ordinary level-up moves.
- **Signature moves** (`pool: signature`, 14): one per Starter line, at Bond rank 5 on **both** of its final branch forms (12), and one for each rare one-off (2). Each belongs to exactly one line. Rank 5 pays off with something you can only raise into.

### Multi-target and 2v2 support
- 1 all-foes damage move per Type (10).
- Heal, `energy` and `cure` are written as "self or one ally", so they still work in 1v1. **Only `empower_ally` and `redirect` moves are 2v2-only.** In 1v1 they're greyed out, like a move you can't afford.
- There are **at most 8 moves that are 2v2-only**, and none appears on a line's level-up list before level 20, so the 1v1 early game never fills slots with dead moves.
- **Boss 5's Volt kit:** the two Volt moves with no damage are `empower_ally` (the "charge") and a self-or-ally `energy` move, so ticket 15's "one charges while the other strikes" is built from data, not special code.

### Card text and strings
- The rules line on a card ("20% Burn", "+1 Guard to self", "Heals 50% of damage dealt") is **generated from `effects[]`**, so it can never disagree with what the move does.
- Strings hold only `move.<id>.name` and an optional one-line `move.<id>.flavour`. The flavour text shows on the Creature's page, not on the battle deck.
- The battle deck already shows the name, cost, Power/Focus icon, Type colour and accuracy (ticket 11).

### Who knows which moves
- **Wild Creatures** equip the **4 most recent level-up moves** they could have learned by their level (the line list plus the form's extras). They have no Bond moves, because wild Creatures are rank 0. A new catch keeps that loadout.
- **Trainers and Bosses** list each Creature's 4 moves in their data. They may include Bond moves, up to a rank set in that data.
- After battle, a newly learned move **fills an empty slot automatically if there is one**. Otherwise a "Learned X" card appears and the move waits in the learned list. There's no "forget a move" prompt, since learned moves are kept forever (ticket 07).

### Names
- 1–2 plain-English words in the register of Mendvale, Verdling and Mender (craft, nature and material words).
- At most **12 characters** including spaces, title case, and unique. The limit gets checked against the real button width when the battle UI is built.
- The linter checks names against the same franchise **blocklist file** as species names (ticket 16), extended with the genre's well-known move names ("Thunderbolt", "Ember", "Tackle", "Flamethrower" …). Generic English words are fine unless they're a famous move name.

### Room for Large and patches
- Moves keep **permanent snake_case IDs** and are only ever added, never removed or renumbered.
- A move's **Type and category never change**. Power, cost, accuracy and effect values may be retuned in a content patch: ticket 09's replay fallback covers a paused battle whose moves changed.
- A new effect kind is a code change and joins the closed list.

### Content-linter rules added
- The schema, the closed effect-kind list, the `anim` list and the readability limit (≤1 side effect on a damaging move, ≤2 effects on a move with no damage).
- Each move within its tier band and side-effect pricing, within a tolerance.
- The per-Type grid floor (11 level-up moves in their slots, 2 Bond-only moves).
- A Status sits on its home Types, plus at most 1 borrow per other Type.
- Tier floors: by level on level-up lists, by Bond rank on Bond lists, and signature moves only at rank 5.
- `bond_only` moves on no level-up list; each signature move on exactly one line.
- 2v2-only moves: at most 8, and none on a level-up list before level 20.
- Damaging moves never use the `all` target.
- Trainer and Boss loadouts learnable by that species at that level and Bond rank.
- Move names: at most 12 characters, unique, and absent from the blocklist.

### Order of work
- The **110 level-up moves and the 20 Bond-only moves are one content slice, done before roster batch 1**, because every line picks from them. The slice is done when every move lints clean.
- **Signature moves are written with their own line.**

### Follow-ups
- **Ticket 07** (battle) amended: the level term, flat Energy, categories for every move and the Basic move, crit 1.5×, and the spread penalty only on 2+ targets.
- **Ticket 09** (architecture) amended: `move_bands.json`, move string keys, the move lint rules, and the example ID `ember_bite` renamed to `cinder_nip` ("Ember" is a famous move name).
- **Ticket 15** (Bosses): Boss 5's Volt kit is built from data.
- **Ticket 16** (roster): the move-list slice goes before batch 1.
- **Fog:** the Creature roster fog no longer waits on this ticket.
