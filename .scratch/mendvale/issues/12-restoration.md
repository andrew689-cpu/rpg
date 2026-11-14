# How does Restoration change an Area?

Type: grilling
Status: resolved
Blocked by: 08

## Question

Specify Restoration (see `GLOSSARY.md` and the answer to ticket 05, "What is the core game loop, and what makes Project Wildling different?"):
- How many Restoration stages an Area has.
- Exactly which actions trigger each stage: critical-path stage first, then optional local actions (registering native Creatures, beating local trainers and challenge, hidden sites).
- What each stage changes: encounter table, decorations and tiles, NPCs, open paths, shops.
- How progress toward the next stage is shown to the player, in the world and in a menu.
- How a stage change is presented when it happens.
- How Restoration is expressed as data, so new Areas and regions need no code.

Must be forward-only and must never block the critical path.

Added from ticket 08 (How do catching, the party, and storage work?): each **Restoration stage has its own spawn table** (species, Rarity tier, level range, conditions), and wild Creatures are visible on the map, so restoring an Area visibly changes who wanders it. **Released Creatures never count toward Restoration.** The Collection log records Caught per species, so define exactly what "registering an Area's native species" means (caught anywhere, or caught in that Area?).

## Answer

Resolved by grilling with the human (2026-11-13). Terms are defined in `GLOSSARY.md`: Restoration, Restoration stage, Blighted, Mending, Native species, Area challenge, Hidden site, Focal point. "Mending" is a placeholder name until ticket 06 (naming) is decided. **Every number is data with a starting value.**

### Stages
- Every restorable Area starts **Blighted** (stage 0) and has **3 Restoration stages** by default, set per Area in data (1–4).
- An Area may have **0 stages** (interiors, the Sanctuary, an untouched town); it is never Blighted.
- Stages always apply **in order** and only move forward.

### What triggers a stage
- **Stage 1 comes only from the critical path:** a story flag (a Boss beaten, a story beat). One flag may restore **one or more Areas at once**, e.g. a Boss's own Area plus two neighbouring routes.
- **Stages 2+ come only from Mendings.** Each stage lists its own Mendings and needs **K of M** of them (e.g. 3 of 5); the player picks which.
- **Mendings count early.** A Mending finished while the Area is still Blighted is saved and applies the moment stage 1 lands.
- Some Mendings are **counted**, with their own mini-progress, so a stage stays a short checklist:
  - "Register 3 of 4 native species"
  - "Beat the 4 trainers here"
  - "Beat the Area challenge"
  - "Find the hidden spring"
- **Linter rule:** every Mending for stage N must be completable while the Area is at stage N−1 (e.g. a species to register must spawn in an earlier stage's table). The content pipeline checks this; designers don't have to remember it.

### Mending kinds
- **Registering native species.** Each Area lists **3–6 native species**, Common or Uncommon only, never Very rare. A species is registered for that Area when it is **caught inside that Area**, at the moment of the catch, once per species per Area. Registration is **permanent**: releasing the Creature later doesn't undo it, and a release never earns anything. Evolved forms don't stand in for the listed species. Catches elsewhere don't count.
- **Beating local trainers.** One counted Mending per group of trainers.
- **The Area challenge.** At most **one per Area**: a stronger set encounter (a veteran trainer, a strong wild Creature, or a 2v2 pair), visible on the map from the start, showing a recommended level, retryable, never on the critical path. Postgame repeats go through the Boss-rematch system, not here.
- **Hidden sites.** Interactable spots (a choked spring, a buried seed cache, a cracked shrine), found by exploring with what the player already has. **No field-move or ability gates in v1**; the data has an optional condition (story flag or Party species) for later. A path opened by one stage may lead to a site that counts toward the next.

### What a stage changes
A stage is a data bundle that may change any of:
1. the spawn table (per Area × stage, from ticket 08)
2. the tile-swap layer, spreading from the Area's **focal point** (from ticket 10)
3. Habitat patches added or removed (e.g. a pond refills and a water patch appears)
4. NPCs added, removed, or given new dialogue
5. paths opened
6. shop stock additions
7. the weather table
8. the music and ambient track

Rules:
- **Only stage 1 may open critical-path routes.** Stages 2+ open only optional paths: shortcuts, side pockets, hidden sites.
- **Restoration never changes battle rules.** Blighted Areas have no buffs or debuffs; only the battle backdrop follows Restoration.

### Payoffs
- Each Area's **final stage adds a payoff Creature**: either a rare one-off set encounter at the focal point, or a Very rare entry in that stage's spawn table.
- **100% region Restoration** earns a postgame acknowledgement and a cosmetic (e.g. a flower crown on the following Creature).
- Restoration rewards are **never money or items**; the economy stays separate.

### How progress is shown
- **In the world:** the **focal point changes visibly at every stage** (a dry spring trickles, then flows, then blooms). Touching it opens the Area's Mending checklist. Hidden sites get no marker. Unbeaten trainers and the Area challenge keep their usual idle cue.
- **In the menu:** a **Region map** with a panel per Area showing:
  - stage pips (●●○)
  - **only the next stage's** Mendings with K/M, plus "1 more stage after this"
  - native species as silhouettes until Seen, then named
  - hidden sites as "Hidden site — ?" with no location
  - the Area challenge with its recommended level
  - for a Blighted Area, what restores it ("Restored when Boss X is beaten"); Mendings done early show as "✓ — counts once restored"
  - a **region-wide Restoration %** in the map header

### How a stage change is shown
- If it triggers **while the player is in the Area**, it plays as soon as the current battle or dialogue ends: the camera pans to the focal point, tiles swap outward in rings over about 3 seconds with a chime, then a banner ("<Area> — Restored: Stage 2") and a card listing what changed (new Creatures nearby, a path opened, new shop stock).
- Skippable with a tap; instant with battle animations off.
- If it triggers **elsewhere**, it's queued and plays on the next entry to that Area.
- **Several stages at once** (stage 1 landing with enough saved Mendings for stage 2) play as **one sequence** with one combined card.
- **Autosave** right after.

### Data and save
- **Area data:** `native_species[]` and `stages[]`. Each stage has:
  - a trigger: `story_flag` (stage 1) or `mendings_required: K` (stages 2+)
  - `mendings[]`
  - a spawn table reference
  - a tile layer and focal point
  - Habitat-patch changes, NPC changes, opened paths, shop additions, weather table, music
  - an optional payoff Creature
- **Mending kinds are a closed list:** `register_natives(n)`, `defeat_trainers(ids)`, `defeat_challenge(id)`, `find_site(id)`. A new *kind* needs code; a new Area or region doesn't.
- **The save stores raw facts:** species registered per Area, trainers beaten, sites found, story flags. It also stores **the highest stage reached per Area** and a **pending-presentation queue** per Area.
- **On load**, an Area's stage is the higher of its stored stage and the stage computed from the facts, so a content patch that changes requirements can never move an Area backwards.

**Follow-ups:** tickets 09 (technical architecture) and 14 (items and economy) were amended. The new ticket 15, "How do the Bosses and Area gating sequence the region?", was graduated from the Progression & bosses fog. The World structure & maps fog was updated.
