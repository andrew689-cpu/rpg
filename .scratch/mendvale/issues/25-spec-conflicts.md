# Which way do the spec's seven conflicts go?

Type: grilling
Status: claimed
Blocked by: 24

## Question

Assembling the spec ([`spec.md`](../spec.md), §7 "Conflicts to settle") found seven places where two tickets disagree and no amendment settles it. Decide each one, then amend the source tickets and the spec:

1. **Snare vs fleeing:** fleeing a wild battle "always works" (tickets 07 and 08), but a Snared Creature "can't switch or flee" (ticket 07).
2. **Collection log Rarity:** the log shows a species' Rarity tier "once seen" (ticket 08), but Rarity lives on spawn entries, so a species can have several tiers (ticket 16). Which one does the log show: the highest, the lowest, per Area, or none?
3. **Evolved forms as native species:** middle forms fill native-species lists, which must be Common or Uncommon (tickets 12 and 16), but evolved forms spawn wild only at Rare or Very rare (ticket 16).
4. **Town payoff Creatures:** every Area's final stage adds a payoff Creature (ticket 12), but towns have no Habitat patches and neither one-off is in a town (ticket 18). Do towns get a different payoff, or none?
5. **What the region record holds:** only the Boss list and the level-cap table (ticket 15, ADR 0003), but also its Areas (ticket 18).
6. **Stage 1 "before the finale":** every Area must reach stage 1 before the finale (ticket 15's linter check 3), but `boss_8` itself restores `blight_heart`, `source` and `outpost` (ticket 18). Does the finale's own flag count?
7. **OFL fonts:** the allowed art licences are CC0, OGA-BY and commercial (ticket 02), but the chosen font Tiny5 is OFL (ticket 10). Is OFL allowed for fonts?
