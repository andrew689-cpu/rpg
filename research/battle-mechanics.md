# Battle mechanics reference: stats, damage, types and more in creature-collectors

Resolves ticket `03-battle-mechanics-reference` ("What stat, damage and type-chart systems do creature-collector games use?"). Feeds `07-battle-system` and `08-catching-and-party`.

This is a **menu of genre mechanics**, not a spec and not content to copy. Each section lists what existing games do, with pros and cons. Each idea is tagged:

- **[STANDARD]**: appears in several games or is common JRPG practice. Safe to use in our own form.
- **[SIGNATURE: Game]**: a mechanic that a game is known for. Avoid copying it as-is. If we want the same effect, reach it a different way.

Claims are cited as `[Sn]` (see **Sources** at the end). Lines marked *Analysis* are our own reasoning from the cited formulas, not a sourced claim.

> **How the sources were checked.** For the genre progenitor (the mainline monster-catching series from Nintendo/Game Freak, called "the progenitor" below), formulas were read straight from the community decompilation of the 2004 GBA entry (`pret/pokeemerald`) and the Gen 1 disassembly (`pret/pokered`). Later-generation rules were read from the Pokémon Showdown simulator source and the `pokeemerald-expansion` engine. These are primary in the sense that they are the executable rules, not write-ups. Bulbapedia, Fandom wikis and megatenwiki block automated fetches (Cloudflare/402/403), so they were **not** used. Temtem, Cassette Beasts and Coromon numbers come from their wiki.gg/official wikis. A few points rest on secondary sources (reviews, guides) and are marked *(secondary)*. **Legal note:** the decomp/disassembly code is derived from copyrighted ROMs. Use it only to understand mechanics. Do not copy code, tables or data from it.

---

## 1. Stat models

### What exists

| Game | Stats | Per-individual variation | Trainable growth |
|---|---|---|---|
| Progenitor (Gen 3+) | HP, Atk, Def, SpAtk, SpDef, Speed [S1] | IVs 0–31 per stat (`MAX_IV_MASK 31`) [S6]; 25 natures giving +10%/−10% to one stat pair [S1 `ModifyStatByNature`, S6] | EVs: max 255 per stat, 510 total [S6] |
| Temtem | HP, STA, SPD, ATK, DEF, SPATK, SPDEF [S16] | SVs 1–50, random on wild Temtem, inheritable through breeding [S16] | TVs: max 500 per stat, 1000 total [S16] |
| Coromon | Base stats + SP [S30, S32] | One **Potential** value 1–21 per Coromon. It sets the tier: Standard 1–16 (97.09%), Potent 17–20 (2.88%), Perfect 21 (0.031%) [S30] | Each Potential Unlock gives 3 points the player assigns [S30] |
| Cassette Beasts | Max HP, Melee/Ranged Atk & Def, Speed, plus AP and move slots [S24, S26] | Not verified (the stats page could not be fetched) | — |

### Stat formulas (as documented)

- **Progenitor, Gen 3** [S1 `CALC_STAT`, `CalculateMonStats`]:
  - HP = ⌊(2·Base + IV + ⌊EV/4⌋)·L/100⌋ + L + 10
  - Other stats = (⌊(2·Base + IV + ⌊EV/4⌋)·L/100⌋ + 5) × nature (1.1 / 1.0 / 0.9)
- **Temtem** [S16]. The wiki rendering is partly garbled, so treat operator placement with care:
  - HP = ⌊((1.5·Base + SV + TV/5)·L/80) + (SV·Base·L/20000) + L + 15⌋
  - Other stats = ⌊((1.5·Base + SV + TV/5)·L/100) + (SV·Base·L/25000) + 10⌋
  - STA has its own formula, mainly driven by base stat and level [S13, S16].

### Options

| Option | Pros | Cons |
|---|---|---|
| **A. Species base stats × level, linear growth** [STANDARD] (every game above) | Easy to balance as data. Keeps stat *ratios* steady across levels, so the damage formula behaves the same at every level (see §2). | Two same-species Creatures play the same unless variation is added. |
| **B. Hidden per-stat random values (IV/SV-style)** [STANDARD in shape. The exact IV+EV+nature *trio* is SIGNATURE: progenitor] | Every catch is a little different, which gives a "hunt for a good one" loop. | Invisible to casual players. Pushes competitive players into grinding and min-maxing. 6 hidden numbers is a lot to show on a phone. |
| **C. One visible quality grade (Coromon "Potential" tiers)** [SIGNATURE: Coromon for the 1–21 + Potent/Perfect wording] | One number is easy to read on mobile. Rare high rolls give an exciting moment. | Less nuance. Tiers that look like rarity grades can feel gacha-like. |
| **D. Effort/training points (EV/TV-style)** [STANDARD] | Lets players shape a Creature. Temtem lets TVs be reassigned at max level, which reduces regret [S16]. | Grind-heavy unless the UI makes it visible. |
| **E. Player-assigned points per level or unlock** (Coromon [S30]) | Clear and player-driven. | Players can make weak builds. Needs a respec. |
| **F. Few stats (e.g. HP / Power / Guard / Speed)** | Readable on a small screen. Fewer balancing axes. | Fewer niches across 150+ species. |

*Analysis:* For mobile, a visible, small variation (1 grade, or 1–2 visible "traits") plus optional training reads better than six hidden IVs. A physical/special pair (two attack and two defence stats) is common to the progenitor, Temtem and Cassette Beasts (melee/ranged) [S1, S16, S26]. It adds roles but doubles the defensive axes to balance.

---

## 2. Damage formulas and their balance properties

### Documented formulas

- **Progenitor (Gen 3)** [S1 `CalculateBaseDamage`, S2 `Cmd_damagecalc`/`Cmd_typecalc`/`ApplyRandomDmgMultiplier`]:
  `base = ⌊⌊(A·Power·⌊2L/5+2⌋)/D⌋ / 50⌋`, then burn ×0.5 (physical), screens, spread ÷2. Floor at 1, then +2. Then ×crit (2), ×STAB 1.5, ×type (per defending type), then a random factor of 85–100% (`100 − rand%16`).
- **Progenitor (Gen 5+)** [S9 `getDamage`/`modifyDamage`, S10 `randomizer`]: same core, `⌊⌊⌊2L/5+2⌋·Power·A/D⌋/50⌋ + 2`, then spread 0.75, weather, crit (1.5× from Gen 6), random 85–100%, STAB 1.5, type (×2 per weak type, ÷2 per resist), burn.
- **Temtem** [S14]: `Damage = (7 + Level/200 × TechniqueDamage × ATK/DEF) × Modifiers`, rounded to the nearest integer. STAB is 1.5×. The page lists no random factor *(rendering partly garbled)*. Reviews report Temtem has no damage roll and no crits *(secondary)* [S21, S22].
- **Cassette Beasts** [S26]: power × attack/defence × a level term, ×Random (uniform integer 85–100)/100, +1. Then ×STAB **1.2**, ×**1.3^(advantages − disadvantages)**, ×crit (1.5 + sticker bonus). *(The rendered formula is garbled. The modifiers are stated clearly.)*
- **Dragon Quest (mainline, classic)** [S37]: subtractive, `(Attack − Defence/2)/2`. 4 points of defence remove 1 damage. A separate formula keeps much stronger defenders taking some damage. Variance is "between this and double" in DQ I/II, and ±1/16 in DQ VIII.

### Balance properties

| Family | Properties |
|---|---|
| **Ratio (A/D) × Power × level term** [STANDARD] (progenitor, Temtem, Cassette Beasts) | Never reaches zero, so defence has diminishing returns. Doubling A doubles damage. *Analysis:* stats and HP both grow about linearly with level (§1), so A/D stays about constant and damage ∝ level × power while HP ∝ level. Hits-to-KO stay **roughly the same at every level**, which keeps balance across 1–100 manageable. Move Power becomes the main tuning knob. |
| **Subtractive (A − k·D)** [STANDARD JRPG] (Dragon Quest) | Easy to read ("armour blocks X"). Gives hard break-points. Needs a minimum-damage rule or high defence shuts a fight down [S37]. *Analysis:* sensitive to stat growth. A few levels' gap swings damage a lot, so it handles wide level ranges badly. |
| **Flat additive term** (Temtem's "+7" [S14], the progenitor's "+2" [S1, S9]) | Gives low-level and weak moves a minimum, so early fights aren't 1-damage slogs. |
| **Random variance** (85–100% in the progenitor [S2, S10] and Cassette Beasts [S26]; none in Temtem [S14, S21]) | Variance stops fights from playing out the same every time and blurs exact KO thresholds. No variance makes the game deterministic and better for planning, and avoids "RNG lost me the match". |
| **Same-type bonus (STAB)** [STANDARD]: 1.5 in the progenitor [S2, S9] and Temtem [S14], 1.2 in Cassette Beasts [S26] | Pushes Creatures toward moves of their own type, which gives identity. A smaller bonus (1.2) leaves more room for off-type coverage. |

*Analysis on clarity:* The +2 / floor / multi-step rounding in the progenitor exists to fit 8- and 16-bit integer math. We can use floats or fixed-point with one rounding at the end. That makes damage previews easier to show ("~40–47").

---

## 3. Type / element systems

### What exists

| Game | Size | Typing | Multipliers | Notes |
|---|---|---|---|---|
| Progenitor | 18 types → 324 matchups, of which 204 neutral, 51 ×2, 61 ×0.5, **8 immune (×0)** (counted from [S11]) | Dual. Multipliers stack ×2/÷2 per defending type [S9] | 0, ¼, ½, 1, 2, 4 | Physical/special split per move. |
| Temtem | 12 types [S15] | Dual | 0.25–4×. A weakness and a resistance on the two types cancel to 1×. **No 0× damage immunity.** Types instead give **status immunities** (Fire→Burned, Mental→Asleep, Toxic→Poisoned) [S15, S20] | Synergy: a technique gains an effect if the *ally* is a given type [S17]. **[SIGNATURE: Temtem]** |
| Coromon | 8 Creature types + **6 skill-only types** (Magic, Foul, Heavy, Air, Poison, Cut) [S31] | Chart uses only 2×/1×/0.5×, no immunities [S31] | | Attack-only types widen move variety without growing the defensive chart. |
| Cassette Beasts | 14 types [S25] | One type per form. Fusions combine [S25] | Advantage ×1.3 per hit, applied as 1.3^(adv−disadv) [S26] | Hits cause **reactions**: a hit can debuff the defender, buff it, or **transmute** its type [S25]. A type-advantage hit gives +1 AP [S24]. **[SIGNATURE: Cassette Beasts]** |
| SMT | Element affinities per demon (weak / resist / null / repel / drain) *(the affinity list is from series knowledge and was not verified from a fetched source)* | Per-element affinity, not a type pairing | | Hitting a weakness gives extra actions through Press Turn [S39, S40]. **[SIGNATURE: SMT]** |

### Options

| Option | Pros | Cons |
|---|---|---|
| **A. Small chart (6–10 types), single typing** | Readable on a phone. Easy to learn. Cheap to balance. | Less variety across 150+ Creatures. More same-type Creatures. |
| **B. Medium chart (12–14), dual typing** [STANDARD] | Many combinations (12 types → 78 pairs) with a moderate chart. | Dual stacking (¼–4×) gives swingy one-shots. Players must memorise more. |
| **C. Large chart (18) with immunities** [the full 18 chart is SIGNATURE: progenitor] | Deep, and immunities create switching mind-games. | Hard to learn. Immunities can feel bad (move does 0). |
| **D. No 0× immunities. Types give status immunity instead** (Temtem [S15]) | Every attack does *something*, and type still matters. | Less dramatic switching. |
| **E. Attack-only types** (Coromon [S31]) | More move flavour without growing the defensive chart. | Players have to learn two lists. |
| **F. Gentle multiplier (1.2–1.3×)** (Cassette Beasts [S26]) instead of 2× | Off-type picks stay viable. Less one-shot swinginess. | Type knowledge pays off less. |
| **G. Type hits apply buffs/debuffs/type-change instead of only damage** | Rich combo play. | **[SIGNATURE: Cassette Beasts]**. Copying it would read as derivative. |
| **H. Ally-type bonuses in doubles** | Rewards team building. | **[SIGNATURE: Temtem]** as "Synergy". |
| **I. Weakness → tempo reward (extra action/resource)** (SMT [S39], CB's +1 AP [S24]) | Rewards knowing types with tempo instead of raw damage. | SMT's exact half-icon Press Turn is SIGNATURE. A milder version (e.g. a small meter gain) is closer to genre-generic. |

*Analysis:* Dual stacking (up to 4× and ¼×) is the main source of one-shots. Clamping the combined multiplier (e.g. to 0.5–2×), or adding instead of multiplying, keeps fights readable.

---

## 4. Turn order / speed

| Game | Rule |
|---|---|
| Progenitor | Move **priority bracket** first, then Speed (with stat stages). Ties are a coin-flip [S3 `GetWhoStrikesFirst`]. Paralysis quarters Speed in Gen 3 [S3]. |
| Temtem | Priority **multiplies** Speed: Low 0.5×, Normal 1×, High 1.5×, Very High 1.75×. "Very Low" acts after all others, and "Ultra" acts before switches [S18]. |
| SMT | Side-based phases. The whole party acts using one shared pool of turn points (one per member). Weakness hits and crits save points, and misses cost 2 [S39]. |
| Monster Sanctuary | 3 monsters per side. The player orders actions within a round, and each action builds a combo meter that boosts later hits *(secondary)* [S33, S34]. Combo is **[SIGNATURE: Monster Sanctuary]**. |
| Cassette Beasts | AP gained per round (2/turn) is spent on moves [S24]. Order details not verified. |

**Options:**

| Option | Pros | Cons |
|---|---|---|
| A. Speed-sorted with discrete priority brackets [STANDARD] | Clear. Gives speed-control a role. | Small speed differences decide everything ("outspeed ties"). |
| B. Priority as a speed multiplier (Temtem) | Smoother. Fast Creatures still matter. | Harder to predict at a glance. |
| C. Timeline/initiative bar (CTB/ATB-style, common JRPG) [STANDARD JRPG] | Shows order in the UI, which suits mobile. Speed scales smoothly. | More UI. Changes pacing. |
| D. Side-phase (whole team acts) | Fast to play on a phone with fewer back-and-forth waits. | The SMT Press Turn economy on top of it is SIGNATURE. |

---

## 5. Accuracy and evasion

- **Progenitor:** each move has an accuracy %. One combined stage (accuracy − evasion), clamped −6..+6, maps to 33/36/43/50/60/75/100/133/166/200/233/266/300% [S2 `sAccuracyStageRatios`].
- **Temtem:** techniques have no accuracy stat. The Techniques page lists none [S18], and reviews say moves never miss *(secondary)* [S21, S22]. The developer's AMA framing was "no low rolls also mean no high rolls" [S21 cites; secondary]. An "Evading" condition dodges the next offensive technique, so dodging is deterministic and visible [S20].
- **SMT:** a miss costs extra turn resources (2 points instead of 1) [S39].
- **DQ:** the base hit uses a flat evasion chance rather than a full hit roll [S37].

| Option | Pros | Cons |
|---|---|---|
| Per-move accuracy % [STANDARD] | Lets strong moves carry risk. | Misses are the most-hated randomness. Two misses in a row feel unfair (Kotaku's anecdote, [S23] secondary). |
| No misses, dodge only through visible statuses (Temtem-style) | Deterministic. Good for short mobile sessions and async PvP. | Removes a balancing lever. Strong moves need other costs (resource, charge, recoil). |
| Hidden "pity"/streak breaker | Keeps randomness and cuts down bad streaks. | Hidden rules can confuse expert players. |

---

## 6. Critical hits

| Game | Rate | Multiplier |
|---|---|---|
| Progenitor Gen 1 | Based on **base Speed**: ≈ (BaseSpeed/2)/256 for normal moves, ×8 for high-crit moves. Focus Energy is bugged and *quarters* the rate [S8 `CriticalHitTest`] | 2× |
| Progenitor Gen 2–5 | Stage table 1/16, 1/8, 1/4, 1/3, 1/2 [S2, S9] | 2× [S2] |
| Progenitor Gen 6 / 7+ | Gen 6: 1/16, 1/8, 1/2, 1. Gen 7+: **1/24**, 1/8, 1/2, 1 [S9] | **1.5×** from Gen 6 [S9] |
| Gen 3 detail | A crit ignores the attacker's attack *drops* and the defender's defence *boosts* [S1] | |
| Cassette Beasts | not verified | 1.5 + sticker bonus [S26] |
| Temtem | none *(secondary)* [S21] | — |
| Dragon Quest I/II, V | fixed 1/64. Later games base it on a stat (Deftness), ~5% cap in DQ XI [S38] | ignores defence [S38] |

**Options:** fixed low rate [STANDARD]; rate from a stat (Gen 1, DQ IX+) [STANDARD]; no crits (Temtem); crits that pay out in resources rather than burst damage (CB has "Critical AP" stickers [S24]). *Analysis:* the series trend (2× → 1.5×, 1/16 → 1/24) moves toward **less crit swing**.

---

## 7. Status effects

| Game | Model |
|---|---|
| Progenitor (Gen 3) | One "major" status at a time (sleep, poison, burn, paralysis, freeze, toxic in a `status1` field) plus separate short-lived effects [S1, S2]. Sleep 2–5 turns [S4]. Freeze: 4/5 chance to stay frozen each turn [S4]. Paralysis: 1/4 chance to lose the turn [S4] and Speed ÷4 [S3]. Burn halves physical damage [S1]. |
| Temtem | **Up to two** conditions at once. A new one pushes out the oldest. A repeat of the same condition is ignored. Conditions last on swap-out. Type-based immunities [S20]. Includes positive conditions (Regenerated, Evading, Invigorated) and resource-targeting ones (Exhausted: +50% stamina cost) [S20]. |
| Cassette Beasts | Four categories: Buff, Debuff, **Transmutation** (type change), Misc [S29]. Effects from type reactions [S25]. |

**Options:**

| Option | Pros | Cons |
|---|---|---|
| A. One major status slot + short-lived effects [STANDARD] | Simple to read. Limits stacking. | Random lost turns (sleep, freeze, full paralysis) are frustrating. |
| B. Small fixed number of slots (e.g. 2) with turn timers, oldest pushed out | Clear UI (icons with timers). Bounded. | More states to show. |
| C. Statuses only on known timers, no random skips | Deterministic. Mobile-friendly. | Fewer surprises. |
| D. Statuses that affect the move resource (stamina/energy drain) | Ties statuses into the resource economy. | Needs a resource system (§8). |
| E. Positive "buff statuses" on the same system | One UI covers buffs and debuffs. | — |

*Analysis:* Random lost turns (sleep 2–5, 20% thaw, 25% full paralysis) are the least mobile-friendly kind of randomness. Fixed durations shown as icon countdowns are easier to read.

---

## 8. Move-resource systems

| System | Game | Rules |
|---|---|---|
| **PP per move** | Progenitor | Each move has its own PP. PP Ups add +20% of base per use, up to 3 [S1 `CalculatePPWithBonus`]. With no PP left the Creature falls back to a default move (Struggle) [S3 `GetWhoStrikesFirst`: `noValidMoves` → `MOVE_STRUGGLE`]. |
| **Shared stamina pool + regen + overexertion** | Temtem | Techniques cost STA. Regen each turn is ≈5% of the STA stat + 1, and Rest adds 15% more [S13]. Spending past 0 **costs HP (2–5 per missing STA point, by level) and the next turn** [S13]. Full refill after battle [S13]. Some techniques have **Hold** (a cooldown before first use or reuse) [S18]. Overexertion is **[SIGNATURE: Temtem]**. |
| **Shared SP pool, rest when empty** | Coromon | Each skill costs SP from one pool. When none are usable the Coromon must rest [S32]. |
| **Action points that regenerate per round** | Cassette Beasts | Max 5–10 AP per form. +2 AP per round. +1 AP for a type-advantage hit [S24]. Fusion gains 4 AP per turn [S27]. |
| **MP / mana** | DQ, SMT, Monster Sanctuary | Classic JRPG MP pool [STANDARD JRPG]. Monster Sanctuary's mana is mentioned only by secondary sources here. |

**Options and properties:**

| Option | Pros | Cons |
|---|---|---|
| PP per move [STANDARD in this genre] | Each move feels like it has its own value. Works over a long dungeon trip. | In short fights PP rarely runs out, so it's just bookkeeping. Tracking 4 counters is fiddly on mobile. |
| Shared pool, refilled after battle | Each battle is a resource puzzle. Easy to show (one bar). | Needs regen tuning so fights don't stall. |
| Per-round regenerating points (AP/energy) | Strong in-battle tempo decisions ("save for the big move"). | Basic moves need cost 0 or the turn feels dead. |
| Cooldowns / charge-up | Deterministic and easy to show on a button. | Can become a fixed rotation. |
| Over-spend with a penalty | Creates a dramatic risk choice. | Temtem's exact HP-and-lost-turn version is signature. |

*Analysis:* For phone play, **one bar per Creature** (a shared pool or per-round energy) is far easier to read than 4 PP counters, and it gives an in-battle decision instead of a between-battle chore.

---

## 9. Capture-rate formulas

| Game | Formula / inputs |
|---|---|
| Progenitor Gen 3 | `a = (rate × ball/10) × (3·Max − 2·HP) / (3·Max)`, ×2 for sleep/freeze, ×1.5 for poison/burn/paralysis. If a > 254 the catch succeeds. Otherwise `b = 1048560 / √√(16711680 / a)` and **4 shake checks** pass if `Random16 < b` [S2 `Cmd_handleballthrow`, S7]. *Analysis:* each check passes with (a/255)^¼, so overall P ≈ a/255. The shakes only animate one roll. Situational balls change the multiplier (e.g. by turn count, level, type, already caught) [S2]. Trainer-owned Creatures can't be caught [S2]. |
| Progenitor Gen 5+ (expansion engine) | Adds a "critical capture" (a one-shake fast path) whose chance grows with collection completion [S12 `CriticalCapture`]. |
| Temtem | `a = ((4·Max − 3·HP) × CatchRate × CardBonus) / (2·Max + 10·Level) × StatusBonus × CloverBonus`. a ≥ 140 is guaranteed. Otherwise 4 shakes, each drawing 0–50,000. The card is used up either way [S19]. Status bonus 1.3–1.5. *Evading/Invigorated lower it* (0.8) [S19]. **Includes target level.** |
| Cassette Beasts | `RecordRate = DamageBonus × HPBonus × LevelBonus × SpeciesRate × TapeRate × Upgrades / 10000`. **DamageBonus** compares damage dealt to the target with damage taken by the recorder (clamped ¼–4). HPBonus = 1 − ⅔·HP/Max. LevelBonus favours low-level targets. Elemental tapes give 4.5× on a type match [S28]. The target can't be KO'd while recording [S28]. Recording-while-dominating is **[SIGNATURE: Cassette Beasts]**. |
| Dragon Quest Monsters | **Scouting**: the party makes a "show of force" built from the normal-attack damage calculation (Attack, or Wisdom in Dark Prince if higher). The success % is shown, and a failure can anger the target so it can't be scouted [S36]. Items/traits add flat % [S36]. **[SIGNATURE: DQM]** |

**Options:**

| Option | Pros | Cons |
|---|---|---|
| A. HP-weighted chance × species rate × tool bonus × status bonus [STANDARD] (all of the above use an HP term of roughly ⅓ at full HP → ~1 near 0 [S2, S28]) | Familiar. Rewards weakening the target without KO'ing it. | "Don't accidentally KO it" tension can annoy. Needs a non-lethal option. |
| B. Show the % to the player (DQM [S36]) | Honest and mobile-friendly. Avoids superstition. | Less suspense. |
| C. Level/power-gap term (Temtem, CB) | Stops early catches of late-game Creatures. Natural pacing. | One more input to explain. |
| D. Performance-based (damage dealt vs taken, CB) | Rewards skilful play. | Hard to explain. Signature feel. |
| E. Collection-progress bonus (critical capture) | Late-game catching speeds up. | Hidden. |
| F. Pity / guaranteed after N fails | Respects session time on mobile. | Can be exploited unless the tool is used up. |

---

## 10. XP and level curves

- **Progenitor curves** (total XP to reach level n) [S5]:

| Curve | Formula | Lv 10 | Lv 50 | Lv 100 |
|---|---|---|---|---|
| Fast | 4n³/5 | 800 | 100,000 | 800,000 |
| Medium Fast | n³ | 1,000 | 125,000 | 1,000,000 |
| Medium Slow | 6n³/5 − 15n² + 100n − 140 | 560 | 117,360 | 1,059,860 |
| Slow | 5n³/4 | 1,250 | 156,250 | 1,250,000 |
| Erratic | piecewise (fast early, slow late) | 1,800 | 125,000 | 600,000 |
| Fluctuating | piecewise (slow early, very slow late) | 540 | 142,500 | 1,640,000 |

*(Values computed from the [S5] formulas.)*

- **XP gain, Gen 3:** `yield × L_defeated / 7`, split among participants. Exp Share takes half. ×1.5 for trainer battles, traded Creatures and the boosting item [S2 `Cmd_getexp`, S12].
- **XP gain, Gen 5-style scaled:** `(yield × L_d / 5) × ((2·L_d + 10) / (L_d + L_p + 10))^2.5 + 1` [S12 `ApplyExperienceMultipliers`, `sExperienceScalingFactors` = i^2.5/4]. *Analysis:* this is a **catch-up mechanic**. Under-levelled Creatures gain much more and over-levelled ones much less, so the team levels up together without hard caps.
- **Gen 6+ split behaviour** is a separate setting in the expansion engine (`B_SPLIT_EXP`) [S12].

**Options:**

| Option | Pros | Cons |
|---|---|---|
| Cubic curves, several growth groups per species [STANDARD] | Long tail. Species feel different. | Late-game grind. Groups are invisible to players. |
| One curve for all | Simple to balance. | Less variety. |
| Level-gap-scaled XP (catch-up) | Bench Creatures catch up. Limits over-levelling. | Players may not see why XP changes. |
| Whole-party XP share (common in modern games) | Mobile-friendly. Less grinding. | Teams over-level unless paired with gap scaling. |
| Low level cap (e.g. 50) | Smaller numbers on screen. Easier balancing. | Less "number go up". |

---

## 11. Signature mechanics to avoid copying as-is

| Game | Signature mechanics |
|---|---|
| Progenitor | The IV + EV + nature trio. The 18-type chart with these immunities. Poké Ball shake-check presentation and ball family. PP Ups. Struggle. Abilities/held items as named. |
| Temtem | Overexertion (HP + lost turn). Synergy (ally-type bonus). Hold. Doubles-only battles. SV/TV naming. |
| Cassette Beasts | Fusion of any two forms. Type reactions (buff/debuff/transmute). Recording with tapes and DamageBonus. AP from type advantage. Stickers. |
| Coromon | Potential 1–21 with Standard/Potent/Perfect tiers. Skill-only types. |
| Monster Sanctuary | Combo meter across a 3-monster turn. Light/Dark Shift *(not verified: fandom blocked)*. Skill trees per monster. |
| DQM | Scouting by show of force, with anger on failure. Synthesis/breeding. |
| SMT | Press Turn icons (half-icon on weakness/crit, extra loss on miss). Demon negotiation. |

---

## 12. Design levers for a mobile Project Wildling

1. **Format.** 1v1 gives the clearest UI. 2v2 adds depth (targeting, ally combos) but needs more screen. Pick early, because type and resource tuning depend on it.
2. **Randomness budget.** Choose where randomness lives: damage roll, accuracy, crits, status skips, capture. Mobile players accept *visible* randomness (a shown capture %) better than *hidden* randomness (a 90% move missing). Temtem shows a deterministic option is viable [S14, S20, S21].
3. **Damage shape.** A ratio formula (A/D × Power × level term) [STANDARD] gives level-invariant hits-to-KO and one main tuning knob (Power). Use one rounding step and a small flat term for early-game feel.
4. **Type chart size and stacking.** 8–12 types is a good mobile range. Clamp or soften dual-type stacking so the most extreme matchups don't one-shot. Consider status immunities instead of 0× damage.
5. **Move resource.** Show one bar per Creature (a pool or per-round energy) instead of 4 PP counters. Basic move costs 0. Big moves cost resource or charge.
6. **Stat variation.** One visible quality signal plus optional training, not 6 hidden IVs. Allow respec.
7. **Capture.** HP-weighted chance with a level-gap term. Show the % (or a 3-step "low/med/high"). Add a non-lethal or "hold at 1 HP" option. Consider pity after repeated fails.
8. **XP.** Cubic-ish curves in 2–3 groups plus level-gap scaling and party-wide XP. A lower cap (50) keeps on-screen numbers small.
9. **Statuses.** 1–2 slots with visible countdowns. Avoid random lost turns.
10. **Data-driven.** Every lever above is a per-species or per-move number (base stats, type, power, cost, accuracy, status chance, capture rate, growth group). That matches the ticket's "~150+ Creatures as data" goal.

---

## Gaps and caveats

- Bulbapedia, Fandom (Monster Sanctuary, SMT) and megatenwiki returned 403/402 to automated fetches. Monster Sanctuary combo details and SMT affinities rely on secondary or partial sources.
- The Temtem and Cassette Beasts wiki formulas render with lost fraction bars. Operator placement is reconstructed and should be checked in a browser before quoting numbers.
- The DQM scout formula is not public in a primary source. Only its inputs are documented [S36].
- The Gen 5+ progenitor capture shake formula was not verified (the expansion engine keeps the Gen 3/4 shake constant [S12]). The Gen 3 numbers above are exact.
- Coromon's and Cassette Beasts' stat-growth formulas were not found.

---

## Sources

Progenitor (executable rules: decompilations, disassembly, simulators)
- [S1] pret/pokeemerald, `src/pokemon.c` (`CALC_STAT`, `CalculateMonStats`, `CalculateBaseDamage`, `gStatStageRatios`, `ModifyStatByNature`, `CalculatePPWithBonus`): https://github.com/pret/pokeemerald/blob/master/src/pokemon.c
- [S2] pret/pokeemerald, `src/battle_script_commands.c` (`Cmd_accuracycheck`, `sAccuracyStageRatios`, `sCriticalHitChance`, `Cmd_critcalc`, `Cmd_damagecalc`, `Cmd_typecalc`, `ApplyRandomDmgMultiplier`, `Cmd_getexp`, `Cmd_handleballthrow`): https://github.com/pret/pokeemerald/blob/master/src/battle_script_commands.c
- [S3] pret/pokeemerald, `src/battle_main.c` (`GetWhoStrikesFirst`, speed modifiers): https://github.com/pret/pokeemerald/blob/master/src/battle_main.c
- [S4] pret/pokeemerald, `src/battle_util.c` (sleep duration, freeze, paralysis checks): https://github.com/pret/pokeemerald/blob/master/src/battle_util.c
- [S5] pret/pokeemerald, `src/data/pokemon/experience_tables.h`: https://github.com/pret/pokeemerald/blob/master/src/data/pokemon/experience_tables.h
- [S6] pret/pokeemerald, `include/constants/pokemon.h` (`MAX_IV_MASK`, `MAX_PER_STAT_EVS`, `MAX_TOTAL_EVS`, `NUM_NATURES`): https://github.com/pret/pokeemerald/blob/master/include/constants/pokemon.h
- [S7] pret/pokeemerald, `include/battle_controllers.h` (ball shake enum): https://github.com/pret/pokeemerald/blob/master/include/battle_controllers.h
- [S8] pret/pokered, `engine/battle/core.asm` (`CriticalHitTest`): https://github.com/pret/pokered/blob/master/engine/battle/core.asm
- [S9] smogon/pokemon-showdown, `sim/battle-actions.ts` (`getDamage`, `modifyDamage`, crit tables per gen): https://github.com/smogon/pokemon-showdown/blob/master/sim/battle-actions.ts
- [S10] smogon/pokemon-showdown, `sim/battle.ts` (`randomizer`): https://github.com/smogon/pokemon-showdown/blob/master/sim/battle.ts
- [S11] smogon/pokemon-showdown, `data/typechart.ts`: https://github.com/smogon/pokemon-showdown/blob/master/data/typechart.ts
- [S12] rh-hideout/pokeemerald-expansion, `src/battle_script_commands.c` (scaled EXP, `ApplyExperienceMultipliers`, `CriticalCapture`, `ComputeBallShakeOdds`): https://github.com/rh-hideout/pokeemerald-expansion/blob/master/src/battle_script_commands.c

Temtem (official wiki, wiki.gg)
- [S13] Stamina: https://temtem.wiki.gg/wiki/Stamina
- [S14] Damage: https://temtem.wiki.gg/wiki/Damage
- [S15] Types: https://temtem.wiki.gg/wiki/Types
- [S16] Single Values (SVs/TVs, stat formulas): https://temtem.wiki.gg/wiki/Single_Values
- [S17] Synergy: https://temtem.wiki.gg/wiki/Synergy
- [S18] Techniques (priority, hold, class): https://temtem.wiki.gg/wiki/Techniques
- [S19] Taming: https://temtem.wiki.gg/wiki/Taming
- [S20] Conditions: https://temtem.wiki.gg/wiki/Conditions
- [S21] *(secondary)* PC Gamer, Temtem review: https://www.pcgamer.com/temtem-review/ (no-dice-roll and no-crit claims were taken from the search excerpt; the page body did not load). Crema AMA on r/NintendoSwitch referenced there.
- [S22] *(secondary)* TechRadar, "Temtem does what Pokemon should have done years ago": https://techradar.com/features/temtem-does-what-pokemon-should-have-done-years-ago
- [S23] *(secondary)* Kotaku on Temtem's design (VGC miss anecdote): https://kotaku.com/pokemon-mmo-temtem-games-like-nintendo-crema-pc-switch-1849657570

Cassette Beasts (official wiki)
- [S24] AP: https://wiki.cassettebeasts.com/wiki/AP
- [S25] Types: https://wiki.cassettebeasts.com/wiki/Types
- [S26] Damage: https://wiki.cassettebeasts.com/wiki/Damage
- [S27] Fusion: https://wiki.cassettebeasts.com/wiki/Fusion
- [S28] Recording: https://wiki.cassettebeasts.com/wiki/Recording
- [S29] Status Effects: https://wiki.cassettebeasts.com/wiki/Status_Effects

Coromon (wiki.gg)
- [S30] Potential: https://coromon.wiki.gg/wiki/Potential
- [S31] Types: https://coromon.wiki.gg/wiki/Types
- [S32] SP: https://coromon.wiki.gg/wiki/SP

Monster Sanctuary
- [S33] Official Steam store page: https://store.steampowered.com/app/814370/Monster_Sanctuary/
- [S34] *(secondary)* "Monster Sanctuary core combat mechanics" guide: https://leetguides.blogspot.com/2019/09/monster-sanctuary-core-combat-mechanics.html

Dragon Quest / Dragon Quest Monsters
- [S36] Dragon Quest Wiki, Monster scouting: https://dragon-quest.org/wiki/Monster_scouting
- [S37] Game Developer, "Number Punchers: How Final Fantasy and Dragon Quest handle combat math": https://gamedeveloper.com/design/number-punchers-how-i-final-fantasy-i-and-i-dragon-quest-i-handle-combat-math
- [S38] Dragon Quest Wiki, Critical Hit: https://dragon-quest.org/wiki/Critical_Hit

Shin Megami Tensei
- [S39] Game Developer, "The evolution of a mechanic" (Nocturne's Press Turn): https://gamedeveloper.com/design/the-evolution-of-a-mechanic
- [S40] *(secondary)* Game8, SMT V battle system guide: https://game8.co/games/Shin-Megami-Tensei-V/archives/348352
