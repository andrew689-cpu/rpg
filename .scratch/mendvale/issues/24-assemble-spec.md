# Assemble the spec

Type: task
Status: resolved
Blocked by: none

## Question

Merge every resolved ticket's answer, with its amendments applied, into one current-truth document, `.scratch/mendvale/spec.md`: the hand-off the map's destination asks for, ready for agents to slice into implementation tickets. It states each decision as it stands now (no history, no superseded versions), uses `GLOSSARY.md` terms, links the ticket each section comes from, and invents nothing. Anything still in the map's **Not yet specified** is marked **Open** in the spec, so the spec can be updated as those patches close.

Run early at the human's request (2026-11-14), before the remaining fog was ticketed. Re-run or update it once the open areas resolve.

## Answer

Done by the agent (2026-11-14): [`spec.md`](../spec.md), about 200 KB in 8 sections, each subsection linking its source ticket.

1. Game, story and naming (tickets 05, 06, 22)
2. Battle and moves (03, 07, 21)
3. Creatures: catching, party, Bond and roster (08, 13, 16)
4. World: Restoration, region, Bosses and economy (12, 14, 15, 18, ADR 0003)
5. Look and feel: art, controls and screens (02, 10, 11)
6. Technology and release (01, 04, 09, 17, 19, 20, 23, ADRs 0001–0002), including **one consolidated linter list of 62 rules**
7. Still open
8. Out of scope

**What assembling it found:**
- **7 conflicts** between tickets that no amendment settles, listed in §7 under "Conflicts to settle" and marked **Conflict:** where they appear. They go to the new ticket 25, "Which way do the spec's seven conflicts go?".
- **Tuning gaps:** starting values no ticket gives (Status lengths, the XP curve, catch formula factors, the Trait effect list, and others).
- **Data gaps:** where a line's shared moves live, the rematch-readiness save field, Boss shopping lists, and the full event command list.
- **Unverified store facts.**

The tuning gaps, data gaps and unverified store facts are in §7 and in the map's **Not yet specified**. Settings defaults that no ticket states are marked **Open** in §5.

**Applied while merging:** each stage's tile changes, patches and focal point live in the map (ticket 23), while its trigger, Mendings, spawn table, shops, weather, music and payoff stay in the Area JSON. The Sanctuary is a menu, not a 0-stage Area. The Boss 1 simulation gate covers 12 Starters (2,400 battles). The save gains item spots taken, Forage last-picked day and the Rest point last used.

**Re-run** once the remaining fog and ticket 25 resolve, so the spec reaches the destination with nothing open.
