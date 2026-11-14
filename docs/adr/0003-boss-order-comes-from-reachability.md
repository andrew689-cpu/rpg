# Boss order comes from reachability, not a list

Nothing in the content lists the order of Bosses or Chapters. Which Bosses are on offer follows only from which Areas the player can reach. Reachability comes from Blight barriers, each cleared by an Area's stage-1 Restoration bundle, which is triggered by a story flag that a Boss win or an event sets. "Beat every Boss in a Chapter" gates are events that set a combined flag. The region record holds only its Boss list (for the Bosses-beaten count and the Region map), the challenge-mode level-cap table and the unordered set of its Areas.

The alternative was an explicit progression record (`"chapters": [["boss_1"], ["boss_2", "boss_3"], …]`) that the game reads to decide who is on offer. We rejected it because the map still needs barriers to stop players walking to a later Boss early, so the same fact would live in two places. A moved barrier or an edited list would let them drift apart, e.g. a Boss "on offer" behind a barrier that is still standing. With one source of truth, a second region is only Areas, barriers and Bosses.

## Consequences

- The content linter must walk the Area graph from the new-game state, following flags, and check the Chapter shape: every barrier's flag is set somewhere reachable before it, each Boss in a Chapter is reachable without beating the others, and every staged Area gets its stage 1 (the finale's own flag counts).
- "Chapter" is a design convention the linter checks, not a field the game reads. A designer who wants a different shape changes barriers and events, not a list.
- *Amended 2026-11-14 by ticket 25 ("Which way do the spec's seven conflicts go?"): the region record also lists its Areas, unordered, for the per-region Region map and Restoration %. That is membership, not order, so this decision stands.*
- Anything keyed to progress (shop stock, the level cap) uses the Bosses-beaten **count**, never which Bosses, so any order the map allows works.
