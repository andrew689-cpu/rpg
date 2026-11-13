# What should Project Wildling's pixel art look like?

Type: prototype
Status: resolved
Blocked by: 01, 02

## Question

Decide tile size, Creature sprite sizes (battle front/back, overworld), character sprite size and animation frames, internal render resolution and scaling on phones, palette constraints, and font, by making rough mock screens (overworld + battle) to react to, using CC0 or placeholder art.

## Answer

Resolved with the human (2026-11-13) by reacting to the prototype:
- Artifact: https://claude.ai/artifact/BF3KpShuSLG8qRX7wtW2m8
- Code: branch `prototype/art-direction`, folder `prototypes/art-direction/`, never merged. Asset licences are in its `LICENCES.md`.

Decided together with ticket 11 (orientation: **portrait first**).

- **Render:** **180 pixels wide internally**, scaled up by **whole numbers** (×4 on 720p Android, ×6 on 1080p/iPhone). The height is extended to fill the screen, with no black bars (in Godot: viewport stretch, aspect expand, integer scale). The map shows about 11 × 12 tiles above the control deck.
- **Tiles:** **16×16**, using the Ninja Adventure pack (CC0) for the world.
- **Player character:** 16×16, with a 4-frame walk in 4 directions.
- **Creature map sprites:** **16×16**, 2 walk frames in each of 4 directions. Used for wild Creatures and for the following lead Creature.
- **Creature battle sprites:** **64×64, front and back, never scaled up.** They're still frames animated by code: an idle bob, a lunge when attacking, a flash when hit, a fade when fainting. An animations setting turns these off. Drawn idle animations can be added later per species without code changes.
- **Palette:** Ninja Adventure's **53 colours are locked** as the master palette. New colours are added only deliberately, and self-drawn Creatures are drawn within it.
- **Fonts:**
  - **Public Pixel** (CC0) for dialogue and menus.
  - **Tiny5** (OFL) for dense battle labels.
  - No text smaller than **8 internal pixels** (about 2.3mm at ×4).
  - No UI-scale setting in version 1.
- **How Restoration looks:** tile swaps at each Restoration stage, **spreading out from a focal point** (a spring, a shrine), using the pack's dead and abandoned tiles. The Blighted state is **muted grey-green and quiet, not burnt**: "broken but hopeful". Smooth edges between healed and blighted ground can be drawn later.
- **Battle scene backdrop:** drawn from the current Area, so it follows Restoration.
