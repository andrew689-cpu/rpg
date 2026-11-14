# What is the core game loop, and what makes Project Wildling different?

Type: grilling
Status: resolved
Blocked by: none

## Question

Define the moment-to-moment, session, and long-term loops (explore → encounter → battle/catch → grow team → beat challenge → unlock area …), and 3–5 design pillars that every later decision is tested against. What is the hook that makes this more than a generic creature collector? Typical session length on mobile?

## Answer

Resolved by grilling with the human (2026-11-13). Terms are defined in `GLOSSARY.md` (Area, Restoration, Restoration stage, Habitat, Time of day, Bond, Boss).

**Player.** Teens and adults who grew up on handheld creature collectors. 13+ in spirit, deliberately not child-directed (avoids the Families-policy risk).

**Hook.** **Restoration** leads; **Habitat** and **Bond** support it. Pitch: *"Heal a broken region with Creatures who grow from how you raise them."*

- **Restoration:** each Area has a few Restoration stages (about 3). The first stage comes from the critical path (story or Boss), so nobody gets soft-locked. Later stages come from optional local actions: registering the Area's native Creatures in the collection log, beating its local trainers and challenge, finding hidden sites. Restoration **only moves forward**: no decay, no punishment for being away. The story may *show* an Area under threat as a scripted beat, but saved progress never drops. Each stage is data that changes the Area's encounter table, decorations, NPCs and open paths.
- **Bond:** visible on the Creature's page, never hidden. It may steer the **evolution branch** (many Creatures have two) and unlock **extra moves** beyond the level-up list. It never adds hidden stat growth.
- **Habitat & time:** an in-game clock, not the device clock. One in-game day ≈ 24 minutes of play (morning, day, evening, night). Resting at camps or inns jumps to a chosen time of day. Weather rolls per Area per in-game day. Creatures that only appear at certain times are always reachable by resting, so nothing is permanently missable.

**Pillars.** When two conflict, the higher one wins.
1. **A World That Heals.** Progress is visible in the world itself, not just in menus.
2. **Raised, Not Rolled.** Your Creatures become what you made them; growth is visible and earned, not random.
3. **Belongs Somewhere.** Every Creature has a habitat, a time and a reason to be where it is.
4. **Respect the Player's Time.** Short sessions, suspend anywhere, no grinding, nothing permanently missable.
5. **Depth on Demand.** Easy to pick up, rewarding to master; randomness is always visible.

**Loops.**
- **Moment-to-moment (seconds to minutes):** explore an Area → meet a Creature or trainer → battle and/or catch → Creatures gain XP and Bond.
- **Session (5–15 min):** every session ends with at least one meaningful beat (a catch, a level-up or Bond milestone, a route cleared, a Restoration stage, a story step). Suspend anywhere, resume instantly, autosave at safe points (after battles, on Area changes). Twenty such beats chained over an hour should flow too.
- **Long-term (hours):** build a team → beat a Boss → a big Restoration stage → new Areas, habitats and Creatures open → choose the next Boss from 2–3 on offer (a mostly linear "string of pearls", no level scaling).
- **Postgame:** finish the collection log, fully restore the region, Boss rematches at higher difficulty. Same data and systems, no new mechanics; bigger postgame waits for the Large scale.

**Difficulty.** The default is approachable but never brainless. Grinding is never required (XP that helps lower levels catch up), and Bosses reward type choice and switching. A later optional **challenge mode**, chosen at new-game (tougher AI, level caps), must have room in the design now. Nothing is monetised.

**Follow-ups:** new tickets 12 (How does Restoration change an Area?) and 13 (How does Bond shape a Creature?). Tickets 07 and 08 were amended, and the Story & world, Creature roster and Progression & bosses fog was updated.
