# Which way do the spec's seven conflicts go?

Type: grilling
Status: resolved
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

## Answer

Resolved by grilling with the human (2026-11-14). Each answer is written into its source ticket as an amendment, and into [`spec.md`](../spec.md) as a current rule.

1. **Snare vs fleeing:** Snare means **can't switch out** only. Fleeing a wild battle always works, Snared or not. *(Ticket 07; ticket 08's "fleeing always works" stands.)*
2. **Collection log Rarity:** shown **per where-found entry** (Area, Habitat, time, weather), derived from content at display time and never saved. *(Ticket 08.)*
3. **Wild evolved forms, by form:**
   - **Middle forms:** wild at Uncommon or rarer, from stage 1, and may be native species.
   - **Final forms:** wild only at Rare or Very rare, from stage 2, and never native.
   - **Branch forms:** never wild.

   *(Ticket 16.)*
4. **Payoff Creatures:** only **Areas with Habitat patches** get one. A town's final stage pays off through its own changes (NPCs, shop stock, music). *(Ticket 12.)*
5. **The region record** holds its Boss list, the level-cap table and the **unordered set of its Areas**. That's membership, not an order list, so ADR 0003 stands. *(Ticket 15, ADR 0003.)*
6. **The finale's flag counts:** linter check 3 becomes "every Area with stages gets its stage 1 from a reachable flag, `boss_8` included", so 100% region Restoration is always possible in the postgame. *(Ticket 15, ADR 0003.)*
7. **OFL fonts:** the SIL OFL is allowed **for fonts only**. Fonts are used unmodified, and the licence text is on an in-game Credits screen. *(Ticket 02; the map's art-sources line updated.)*

**Follow-ups:** none. The spec's §7 now lists these as settled.
