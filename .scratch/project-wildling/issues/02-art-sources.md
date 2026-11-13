# Where can original or licensable pixel art come from, and at what cost?

Type: research
Status: resolved
Blocked by: none

## Question

For a $0 budget now (and a possible small budget later), what are the viable sources of 2D pixel art for a Creature-collecting RPG: Creature front/back sprites, overworld characters, tilesets (towns, routes, caves, interiors), UI, battle effects, icons?

Cover: CC0 / permissive packs (Kenney, OpenGameArt, itch.io, etc.), paid packs, commissions (typical rates), AI-generated art (licensing and store-policy implications), and self-made pipelines (Aseprite/LibreSprite). For each: license terms (commercial use, attribution, modification), style consistency risk, and coverage gaps. Explicitly flag anything that is actually ripped from commercial games.

## Answer

Findings: branch `research/art-sources`, file `research/art-sources.md`.

- **Licensing:** the iOS App Store's terms conflict with CC-BY, CC-BY-SA and GPL (OpenGameArt FAQ: anti-DRM clauses). The safe set is **CC0, OGA-BY, and paid or commissioned licences that grant commercial app-store rights**. CC-BY is usable only with written permission from the artist.
- **Coverage gap: Creature battle sprites.** CC0 covers tiles, characters, UI, effects and fonts well. The only CC0 battle set found with front and back sprites is *50+ Monsters Pack 2D* (56 monsters at 64×64). No free source covers about 100 Creatures in one style.
- **$0 plan:**
  - **Ninja Adventure** (CC0, 16×16, one consistent style) for the world, characters, UI and effects.
  - *50+ Monsters Pack 2D* as placeholder Creatures.
  - Final Creatures drawn in LibreSprite or Pixelorama (free; Aseprite is $19.99).
  - A licence ledger for every asset. Paid assets must never go in a public repo.
- **AI art:** neither store bans AI art bundled with the game (Apple guidelines updated 2026-10-16 require only owned or licensed content). Art made from prompts alone isn't copyrightable (US Copyright Office). Use AI for ideas or as a base that gets substantially redrawn, not for final art.
- **Commissions:** about $30–$60 per 64×64 sprite. 100 Creatures with front and back sprites comes to roughly $6k–$12k before animation. Contracts must explicitly grant app-store rights.
- **Avoid:**
  - The Spriters Resource.
  - PokéAPI sprites: labelled CC0, but the licence file says "Copyright The Pokémon Company".
  - Pokémon Essentials (DMCA'd in 2018).
  - The "Pokemon DS Style" tileset, and other "Pokémon-like" or "fakemon" packs on itch.io.
  - Tuxemon art (CC-BY-SA, with some unclear origins).
  - LPC art, except the Sharm and Redshrike pieces that are also OGA-BY.
- **Unverified:**
  - OpenAI and Midjourney terms, cited from search snippets.
  - Retro Diffusion's terms, which couldn't be found.
  - Two effects/icon packs, seen only in an itch.io CC0 listing.
