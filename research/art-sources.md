# Research: Pixel art sources for Project Wildling

Ticket: [`.scratch/mendvale/issues/02-art-sources.md`](../.scratch/mendvale/issues/02-art-sources.md)
Researched: 2026-11-13. All prices and licence texts are as shown on the cited page on that date. They can change, so re-check before you download or buy.

**Question:** With $0 now and maybe a small budget later, where can Project Wildling get 2D pixel art? That covers Creature front/back sprites, overworld characters, tilesets, UI, battle effects and icons. For each source: licence terms, risk of mismatched styles, gaps in coverage, and which sources are ripped from (or imitate) commercial games.

---

## TL;DR

1. **iOS rules out most attribution licences.** CC-BY and CC-BY-SA forbid adding "effective technological measures" (DRM) that restrict what the licence allows ([CC BY 4.0 §2(a)(5)(B)][cc-by-legal]; [CC FAQ][cc-faq]). OpenGameArt's own FAQ says Apple's App Store terms "conflict with the terms of the GNU GPL, the GNU LGPL, CC-BY-SA, and CC-BY" ([OGA FAQ][oga-faq]). **Whitelist: CC0, OGA-BY, and paid or commissioned licences that allow commercial use.** Allow CC-BY only with the artist's written permission for app stores. Exclude CC-BY-SA, GPL art, NonCommercial licences and "personal use only" commissions.
2. **Creatures are the gap.** Every other category (tiles, overworld characters, UI, VFX, fonts) has good CC0 options. Only one CC0 set I found has **front and back** battle sprites: *50+ Monsters Pack 2D*, with 56 monsters at 64×64 ([OGA][oga-50monsters]). No free source covers about 100 Creatures in one style.
3. **AI art is allowed in both stores, but it is weak IP.** Neither store bans static AI-made assets. Google Play's AI policy covers apps that generate content "based on user prompts" ([Play AI policy][gp-ai]). Apple's guidelines (updated 2026-10-16) have no AI-asset rule beyond "content that you created or that you have a license to use" ([Apple 5.2][apple-guidelines]). However, prompt-only output is **not copyrightable** in the US ([USCO Part 2][usco-newsnet]). The usual IP rules still apply to output that resembles Pokémon.
4. **$0-phase recommendation:**
   - Use **Ninja Adventure** (CC0, 16×16, one artist team) for the world, characters, UI and VFX.
   - Use **50+ Monsters Pack 2D** (CC0) as placeholder battle Creatures.
   - Draw the final Creatures yourself in **LibreSprite (GPLv2) or Pixelorama (MIT)**, both free.
   - Keep a licence manifest for every asset file.
5. **Avoid:**
   - The Spriters Resource
   - PokéAPI sprites. The repo says "CC0" but its LICENCE file says "All image contents within are Copyright The Pokémon Company."
   - Pokémon Essentials
   - Itch packs sold as "Pokémon-like" or "Pokémon style". At least one says it "refined every detail of the original Pokémon tilesets" while being labelled CC-BY 4.0.
   - Tuxemon art: mostly CC-BY-SA 4.0, and some of it has unclear origins.

---

## 1. Options table

| Source type | Cost | Typical licence | Commercial / app store | Attribution | Modify | Style consistency risk | Coverage |
|---|---|---|---|---|---|---|---|
| **Kenney** (kenney.nl) | $0 (donations optional) | CC0 ([Kenney support][kenney-support]) | Yes, "even in commercial projects" | Not required | Yes, under CC0 ([CC0 deed][cc0]) | **Low within one series** ("Tiny", "Roguelike"). High if you mix series. | Tiles, UI, small characters. Few creatures and no front/back battle sprites. |
| **OpenGameArt** (CC0 / OGA-BY items) | $0 | Per item: CC0, CC-BY, CC-BY-SA, OGA-BY, GPL ([OGA FAQ][oga-faq]) | CC0 and OGA-BY: yes. CC-BY, BY-SA and GPL: conflict with the App Store ([OGA FAQ][oga-faq]). | CC0: no. OGA-BY: yes. | Yes (BY-SA: derivatives must use the same licence) | **High.** Thousands of artists, so sizes, palettes and outline styles differ. | Very broad. Includes the only CC0 front/back monster set found. |
| **itch.io free / CC0** | $0 or pay-what-you-want | Set per pack, so read every page. The CC0 tag listed 471 asset packs ([itch CC0 tag][itch-cc0]). | CC0 packs: yes. Many "free" packs are **non-commercial only** (e.g. Sprout Lands Basic, Cute Fantasy free). | Varies | Usually | Low if one pack covers everything (Ninja Adventure). High if you mix packs. | Good for tiles, characters, VFX and fonts. Weak for creatures. |
| **Paid packs** (itch.io etc.) | ~$1.50–$13 for typical packs. Premium monster packs ~$200. | Custom EULA: commercial use OK, **no redistribution**, sometimes credit required ([LimeZu][limezu-mi]; [Josee][josee]; [Cyangmou][cyangmou]) | Yes | Some require it (LimeZu: "Credits required") | Yes | Medium. Same issue as free packs when mixed. | Fills gaps (interiors, a creature roster), but rarely all of them. |
| **Commissions** | ~$5–$95+ per sprite, depending on artist and size (see §5) | Whatever you negotiate. **Default can be "personal use only"** ([Zoiskart][zoiskart]) | Only if the contract says so | Negotiable | Negotiable | Low with one artist for the whole roster | Whatever you pay for |
| **AI-generated** | $0 to subscription | Vendor terms assign or affirm user ownership ([OpenAI][openai-tou]; [Midjourney][mj-tos]; [PixelLab][pixellab-tos]). Prompt-only output is not copyrightable ([USCO][usco-newsnet]). | Allowed by both stores for static assets (see §3) | No | Yes | **High** across ~100 Creatures without heavy manual cleanup (author judgement, not a cited fact) | Anything, but with legal and lookalike risk |
| **Self-made** (LibreSprite / Pixelorama / Aseprite) | $0 (LibreSprite, Pixelorama, or Aseprite built from source) or $19.99 (Aseprite binary) | You own your work. Aseprite: use creations "in any product" ([Aseprite FAQ][aseprite-faq]) | Yes | No | Yes | **Lowest**, if you define a style guide (ticket 10) | Anything, limited by your time |

---

## 2. Licensing notes

### 2.1 CC0
- The deed says you can "copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission" ([CC0 deed][cc0]).
- Caveat: "In no way are the patent or trademark rights of any person affected by CC0," and the person who applied CC0 "makes no warranties about the work" ([CC0 deed][cc0]). **A CC0 label is only as good as the uploader's right to grant it.** The PokéAPI case in §6 shows how this goes wrong.

### 2.2 CC-BY, CC-BY-SA, GPL art vs. iOS
- CC BY 4.0 §2(a)(5)(B): "You may not offer or impose any additional or different terms or conditions on… the Licensed Material if doing so restricts exercise of the Licensed Rights by any recipient" ([legal code][cc-by-legal]).
- CC FAQ, "Can I use effective technological measures (such as DRM) when I share CC-licensed material?": "No… This includes using effective technological measures (ETMs) that would restrict a licensee's ability to exercise the licensed rights" ([CC FAQ][cc-faq]).
- OGA FAQ, "Can I use the art downloaded here in the Apple App Store?": "Not necessarily. Apple's App Store in particular has been found to have usage terms that conflict with the terms of the GNU GPL, the GNU LGPL, CC-BY-SA, and CC-BY… you must ask the artist directly" ([OGA FAQ][oga-faq]). The FAQ also says Google Android may or may not use DRM, depending on how the game is packaged.
- **OGA-BY 3.0/4.0** is CC-BY with the DRM restriction removed. It was "created to provide an option for artists wishing to be credited… but not wanting to restrict its distribution on DRM-using platforms" ([OGA FAQ][oga-faq]). It is safe for iOS, and credit is required.
- **CC-BY-SA** also requires that "If you make derivatives… you must distribute them under the same license" ([OGA FAQ][oga-faq]). That is a poor fit if Creatures are the game's own IP.
- Some art is dual-licensed: you "must follow only one of the licenses" ([OGA FAQ][oga-faq]). For example, LPC assets by Sharm and Redshrike are also available as OGA-BY 3.0 ([LPC page][oga-lpc]).

### 2.3 Other gotchas
- **Previews are not licensed:** "assume the previews are 'All rights reserved'". Only the files you download carry the licence ([OGA FAQ][oga-faq]).
- **Licences are irrevocable** once obtained, even if the artist later changes them ([OGA FAQ][oga-faq]). Save a copy of the licence page when you download.
- **Paid packs forbid redistribution.** Examples: "can't be resold or redistributed even if modified" ([Sprout Lands][sproutlands]), "Resell or distribute the asset to others" listed as not allowed ([LimeZu][limezu-mi]). **If the game repo ever becomes public, paid raw assets can't be committed to it.** Keep them in a private asset store or a git-ignored folder.
- **Commissions:** some artists default to "Commissioned works are for PERSONAL USE ONLY," with commercial rights negotiated separately ([Zoiskart][zoiskart]). Get a written licence or assignment that covers app-store distribution and modification.

---

## 3. AI-generated art

### 3.1 Copyright (US)
- The US Copyright Office's Part 2 report (29 Jan 2025) says outputs are protectable only "where a human author has determined sufficient expressive elements," for example through human-authored work perceptible in the output, or human "creative arrangements or modifications." "Simply providing prompts" does not qualify. Using AI to assist, or including AI material in a larger human work, "does not bar copyrightability" ([USCO NewsNet 1060][usco-newsnet]; [USCO AI hub][usco-ai]).
- **Implication:** Creatures generated from prompts alone would effectively be unprotectable. Anyone could copy them. Creatures are the main IP of a creature-collector.

### 3.2 Vendor terms
| Tool | Ownership / commercial terms | Source |
|---|---|---|
| OpenAI (ChatGPT / image gen) | "you (a) retain your ownership rights in Input and (b) own the Output," and OpenAI assigns its rights in Output to you. The terms also note output may not be unique. | [OpenAI Terms of Use][openai-tou] (via search snippet: page returned 403 to direct fetch) |
| Midjourney | You own your Assets. A company with more than $1,000,000/yr revenue needs a Pro or Mega plan. Ownership "persists even if… You downgrade or cancel." | [Midjourney ToS][mj-tos], [Commercial use][mj-commercial] (via search snippet: 403 on fetch) |
| PixelLab (pixel-art AI) | "You retain ownership of any content you create using PixelLab." Use is allowed "for both commercial and non-commercial purposes." No infringement warranty: the user must ensure content doesn't "infringe on the rights of any third parties." Last updated 2026-10-30. | [PixelLab ToS][pixellab-tos] |
| Retro Diffusion | **Unverified:** I couldn't find first-party terms. | n/a |

### 3.3 Store policy
- **Google Play, AI-Generated Content policy:** defines AI-generated content as content "created by generative AI models based on user prompts." Its examples are chatbots and image or video generation from prompts, and it requires in-app reporting ([Play AI policy][gp-ai]; [Play AI FAQ/overview][gp-ai-faq]). It doesn't address static assets made during development. Static assets don't clearly fit the definition. This is inference, not stated policy.
- **Apple App Store Review Guidelines** (Last Updated 2026-10-16): no AI-asset-specific rule. §1.2 covers "AI content creation apps," meaning runtime generation. The rule that governs static art is §5.2: "Make sure your app only includes content that you created or that you have a license to use" ([Apple guidelines][apple-guidelines]).
- **Lookalike risk applies to AI output too:**
  - Google Play lists "Reproductions or 'fan art' indistinguishable from the original work under copyright" as a violation ([Play IP policy][gp-ip]).
  - Apple §5.2.1 forbids "protected third-party material… without permission" and "copycat representations." §4.1(a) says "Don't simply copy the latest popular app" ([Apple guidelines][apple-guidelines]).
  - Google Play's Impersonation policy bars icons or in-app elements that mislead users about a relationship to another app or company ([Play Impersonation][gp-impersonation]).
  - Nintendo and The Pokémon Company sued Pocketpair (Palworld) on 18 Sept 2024 for patent infringement. Nintendo said it "will continue to take necessary actions against any infringement of its intellectual property rights" ([Nintendo release][nintendo-palworld]). Prompts that name or describe Pokémon are an obvious risk.

**AI verdict:** acceptable for ideation, concept thumbnails and throwaway placeholders. For shipped Creatures, use human-drawn art or AI output that a human has substantially redrawn, so the designs are protectable and checked for lookalikes.

---

## 4. Self-made pipeline

| Tool | Licence / price | Notes | Source |
|---|---|---|---|
| **Aseprite** | $19.99 binary. The source is available, and you may "compile it, and use it for your personal purposes," including making assets for commercial games. Compiled builds may not be redistributed. | Industry-standard animation and palette tools. Your creations can be used "in any product." | [Aseprite FAQ][aseprite-faq] |
| **LibreSprite** | GPL-2.0, free | Fork of the last GPLv2 Aseprite commit (Aseprite went proprietary on 26 Aug 2016). Linux, macOS, Windows, Android. | [LibreSprite GitHub][libresprite-gh], [site][libresprite] |
| **Pixelorama** | MIT, free | Built on Godot. Windows, Linux, macOS, web. | [Pixelorama GitHub][pixelorama-gh], [site][pixelorama] |

Cost is $0 in money but large in time: about 100 Creatures × front + back + icon. Style consistency is the best of all options if ticket 10 locks in sprite sizes, palette rules and outline style. One example of a strict rule: "pure black and 4 other colors" per monster, as the 50+ Monsters Pack does ([OGA][oga-50monsters]).

---

## 5. Commissions and paid packs: price points

Published artist rate cards (starting prices, static unless noted):

| Artist (page) | 16×16 / small | 32×32 | 64×64 | Larger | Animation | Tilesets | Rights |
|---|---|---|---|---|---|---|---|
| YourDed4Dey ([itch][rate-ded]) | $5 | $15 | $30 | n/a | +$15 | n/a | Not stated, so ask |
| David Filus ([carrd][rate-filus]) | n/a | <32×32: $35 | <64×64: $60 | >64×64 from $95 | Separate animation figures listed ($15 / $25 / $35 by size; per-frame vs. flat not clear on page) | From $100 | ~$25/hr. Rights not stated. |
| Zoiskart ([carrd][rate-zoiskart]) | <64×64: $20 | (same) | 64–128: $80 | 128–256: $160; >256: $320 | +$2 on the first 3 frames, then 50% of the base price per extra frame | n/a | **Personal use only** unless commercial rights are bought |

**Rough roster arithmetic** (my calculation from the rates above, not quotes): 100 Creatures × 2 sprites (front and back) at 64×64 = 200 sprites. That is about **$6,000** at $30/sprite and **$12,000** at $60/sprite, before animation, evolutions or commercial-rights fees.

Paid packs for comparison:

| Pack | Price | Licence | Contents | Source |
|---|---|---|---|---|
| Pocket Creature Tamer Adventure Kit (Josee) | $12.99+ | Premium: commercial use OK. No resale or redistribution. Free tier is non-commercial. | 94 creatures, 2 palettes each, many with 2–3 evolution stages, battle UI, VFX, tiles. Tagged "pokemon" and "fakemon". **Check designs for imitation before buying.** Front/back sprites not stated. | [itch][josee] |
| Pixel 50 16-Bit Designer Fantasy Monsters (Cyangmou) | $199.99+ | Commercial OK, edits OK, no redistribution, no print or physical products. Extra EULA in an external Google Doc. | 50 monsters, 64×64, no animations | [itch][cyangmou] |
| Modern Interiors (LimeZu) | $1.50+ | Commercial OK, edits OK, **credits required**, no redistribution | Interiors at 16/32/48 px, character generator, UI | [itch][limezu-mi] |
| Sprout Lands Premium (Cup Nooble) | $3.99+ | Commercial OK, no redistribution. Asks for credit. | 16-bit farm/RPG tiles | [itch][sproutlands] |
| Cute Fantasy RPG Premium (Kenmi) | $3.99+ | Commercial OK, no redistribution | 16×16 tiles, characters, a few enemies, animals | [itch][kenmi] |

---

## 6. Avoid: ripped, mislabelled or Pokémon-imitating sources

| Source | Why avoid | Evidence |
|---|---|---|
| **The Spriters Resource** (spriters-resource.com) | Archive of sprites ripped from commercial games, including whole Pokémon games (B/W, B2/W2, SV, ORAS, PMD) | [Site search results][tsr-search] (direct fetch returned 403) |
| **PokéAPI `sprites` repo** | The repo is labelled "CC0 1.0 Universal," but its LICENCE says "All image contents within are Copyright The Pokémon Company." The README thanks Smogon for "custom B&W-style sprites," which are fan derivatives. **A standard example of a CC0 label that is not valid for the images.** | [LICENCE.txt][pokeapi-licence], [README][pokeapi] |
| **Pokémon Essentials** (RPG Maker XP kit) and its forks | Bundled assets from the real games. Downloads were taken down in Aug 2018 after a Nintendo of America copyright claim. | Secondary press: [Kotaku][kotaku-essentials], [Nintendo Life][nl-essentials] (no first-party notice found) |
| **El Espriteador, "Pokemon DS Style Tileset"** and siblings ("Pokemon DS Style Extra", "Zelda-Inspired (GBC & GBA Style)") | The page says it "refined every detail of the original Pokémon tilesets," yet is labelled CC-BY 4.0. A derivative of Game Freak/Nintendo work can't be validly CC-licensed by a third party. | [itch][espriteador] |
| **Itch packs marketed as Pokémon-like / Pokémon-style:** maciaz "Pokemon-like Top Down Tile Set", Aarya Yt "Pokemon Like/Inspired" tilesets, Yelta "Poké-like 1bit", Serenity "GB Pokemon-style", Pixelmister "Pokemon Styled", ApoloA4 "Pokemon 8bit Style" ("styled on Pokemon Red and Blue"), Enrisco "Greenhill" ("Pokemon Gold/Silver/Crystal style"; no licence stated), Kensu William "Gameboy Tileset like Zelda & Pokemon", "fakemon tilesets 001–003" | Even if the art is hand-made, these packs aim to imitate the Pokémon look. That conflicts with the map's rule ("no Pokémon… look"). It also makes copycat claims under Apple §4.1 and Play's IP and impersonation policies more likely. Several also state no licence at all. | [itch "pokemon" + tileset tag][itch-pokemon-tag], [ApoloA4][apoloa4], [Enrisco][enrisco] |
| **Tuxemon art** | Original, but **146+ entries are CC-BY-SA 4.0**, which conflicts with iOS and is ShareAlike. Origins are uneven: "Fruitera" is "based on 'Fruit bat starter'" from DeviantArt, and purchased LimeZu packs are listed as "licensed under CC BY," which doesn't match LimeZu's own no-redistribution terms. | [Tuxemon ATTRIBUTIONS.md][tuxemon-attr], [LimeZu terms][limezu-mi] |
| **LPC (Liberated Pixel Cup)** base assets | CC-BY-SA 3.0 / GPL 3.0, which conflicts with iOS. *Exception:* the Sharm and Redshrike pieces are also available as OGA-BY 3.0. | [OGA LPC][oga-lpc] |
| **Fan "fakemon" / sprite-collab sites** in general (DeviantArt, Relic Castle, PMD sprite collabs) | Fan derivatives of Pokémon designs. OGA itself bans "Modifications of existing commercial game art" and "clearly non-free IP" | [OGA FAQ][oga-faq] |

**Rule for agents:** reject any asset whose page, title, tags or description name Pokémon, "Poké", "fakemon", or a specific Pokémon generation or game as the style target. Reject any asset whose origin is a rip or edit of a commercial game.

---

## 7. Candidate packs ($0 phase), checked against primary pages

| Pack | Author / link | Licence | Grid | What it covers | Notes |
|---|---|---|---|---|---|
| **Ninja Adventure Asset Pack** | Pixel-boy & AAA ([itch][ninja]) | **CC0** ("not required but appreciated") | 16×16 | 50+ characters with animations and facesets, 30+ monsters, 9 bosses, autotile floors, exterior and interior tiles, UI, 30+ VFX, 60+ items, 2 fonts (plus 100+ SFX and 37 music tracks) | **Best single-source base:** one style across world, characters, UI and effects. Its monsters are overworld-style, not battle front/back. |
| **50+ Monsters Pack 2D** | isaiah658 ([OGA][oga-50monsters]) | **CC0** | 64×64 | 56 monsters with **front and back** sprites plus an alternate palette each | The only CC0 front/back battle set found. Strict palette (black + 4 colours). Covers about 56% of a 100-Creature roster. |
| **Tiny Creatures** | Clint Bellanger, made with Kenney's permission ([OGA][oga-tinycreatures]) | **CC0** | 16×16 | 180 sprites: 100+ monsters, 50+ animals | Matches Kenney Tiny Dungeon and Tiny Town. Single view only. Classic fantasy monsters. |
| **Kenney Tiny Town / Tiny Dungeon** | Kenney ([Tiny Town][kenney-tinytown], [Tiny Dungeon][kenney-tinydungeon]) | **CC0** | 16×16 | Town/overworld; dungeon/sewer (130 files each) | Pairs with Tiny Creatures for a consistent "Tiny" look. |
| **Kenney Roguelike RPG Pack** | Kenney ([link][kenney-roguelike]) | **CC0** | 16×16 | 1,700 files: town, furniture, buttons, panels | Interiors and furniture |
| **Kenney Pixel UI Pack** | Kenney ([link][kenney-pixelui]) | **CC0** | n/a | 750 files: panels, buttons | Menus and battle UI frames |
| **Zelda-like tilesets and sprites** | ArMM1998 ([OGA][oga-zelda]) | **CC0** | 16×16 | Overworld (castle, houses), **cave**, **indoors**, character with animation, effects, objects, UI | "Zelda-like" describes the genre. The art is original and CC0, and Tuxemon also uses ArMM1998 objects. |
| **Dungeon Crawl Stone Soup tiles** (+ supplemental) | DCSS artists, maintained by Chris Hamons ([OGA][oga-dcss], [suppl.][oga-dcss-sup]) | **CC0** | 32×32 | 6,000+ tiles: monsters, terrain, spell effects, items, GUI | Huge creature pool for placeholders. Top-down ¾ view, mixed artists. |
| **Public Pixel Font** | GGBotNet ([itch][ggbot-font]) | **CC0** | 8×8 | Monospace pixel font, 98 languages | Good for localisation |
| PVFX Foundry (101 VFX); 1-bit Pixel Icons (Nikoichu) | ([itch CC0 tag listing][itch-cc0]) | Listed under the CC0 tag | n/a | Battle VFX; 1,400+ 16×16 icons | **Verify each pack page.** I saw only the listing. |

Free tiers that are **not** usable (non-commercial only): Sprout Lands Basic ([itch][sproutlands]), Cute Fantasy RPG free ([itch][kenmi]), Pocket Creature Tamer free ([itch][josee]). Not recommended for iOS: Sharm's 16×16 Overworld Tiles if taken under CC-BY. Take it under its **OGA-BY 3.0** option instead ([OGA][oga-sharm]).

---

## 8. Coverage gaps (after the CC0 candidates)

| Asset class | Covered by | Gap |
|---|---|---|
| Creature battle sprites (front + back) | 50+ Monsters Pack 2D (56) | **About 44+ Creatures missing. No evolutions-as-lines. Style has to match the rest of the game.** This is the critical gap, and self-made or commissioned art is needed for the final roster. |
| Creature overworld / party icons | Tiny Creatures, Ninja Adventure monsters, DCSS | Not the same designs as the battle sprites, so icons need redrawing per Creature |
| Overworld characters (player, NPCs, rivals) | Ninja Adventure (50+), ArMM1998 | Trainer battle portraits/sprites in front view |
| Tilesets: town, routes, caves, interiors | Ninja Adventure, Kenney Tiny/Roguelike, ArMM1998 | Genre-specific tiles: tall-grass encounter tiles, water-surfing edges, ledges, a healing-centre interior. Mostly edits of existing tiles. |
| UI | Kenney Pixel UI, Ninja Adventure UI | HP/XP bars, type badges, party screen, catching-device icon |
| Battle effects | Ninja Adventure (30+), PVFX Foundry (verify), DCSS spell effects | Effects for each type, plus capture and evolution sequences |
| Icons / items | Ninja Adventure (60+ items), 1-bit Icons (verify), DCSS items | Capture-device item set, type icons |
| Fonts | Public Pixel Font, Ninja Adventure fonts | None |

**Style consistency:** mixing sources is the main visual risk. Two combinations look internally consistent:
- (a) **Ninja Adventure only**, for everything except battle Creatures, or
- (b) **Kenney Tiny + Tiny Creatures**, which were built to match ([OGA][oga-tinycreatures]).

The battle screen is a separate visual context, so its Creature sprites (64×64, front/back) can follow their own art rules. They should share a palette rule with the world art (ticket 10).

---

## 9. Recommendation for the $0 phase

1. **Licence whitelist, written into the asset pipeline:**
   - Allowed: CC0, OGA-BY 3.0/4.0, a self-made original, or a paid/commissioned licence that explicitly allows commercial distribution in app stores.
   - Allowed with conditions: CC-BY, only with the artist's written permission for app stores (per the [OGA FAQ][oga-faq]).
   - Rejected: CC-BY-SA, GPL art, NC, "personal use", "no licence stated", and anything in §6.
2. **World, characters, UI and VFX:** start from **Ninja Adventure** (CC0). Fill gaps with ArMM1998 (CC0) and Kenney (CC0) tiles, recoloured to Ninja Adventure's palette.
3. **Battle Creatures (placeholders):** **50+ Monsters Pack 2D** (CC0, front/back). For more placeholder slots, use DCSS or Tiny Creatures.
4. **Final Creatures:** draw them yourself in **LibreSprite or Pixelorama** ($0). Aseprite at $19.99 is optional, and you can also compile it from source for free. Follow the ticket-10 style guide. Use AI only for ideation, or as a base that is substantially redrawn, never prompt-only finals. That keeps designs copyrightable ([USCO][usco-newsnet]) and checked for lookalikes.
5. **Provenance manifest:** for every asset file, record the source URL, author, licence, download date and a saved copy of the licence page. This meets attribution duties (OGA-BY, LimeZu credits), guards against licence changes and supports the map's "art must be swappable" note. Generate the in-game credits screen from it.
6. **Keep paid raw assets out of any public repo** (no-redistribution clauses).
7. **When a budget appears:** the highest-value spend is a single commissioned artist for the Creature roster. At about $30–$60 per 64×64 sprite (§5), 200 sprites cost ~$6k–$12k, so phase it, e.g. starters and early routes first. Use a contract that grants commercial and app-store rights and modification. Cheap paid packs (LimeZu $1.50+, Josee $12.99+) fill tile and UI gaps, but check Josee's creatures for Pokémon imitation before use.

---

## 10. Open items / unverified

- Retro Diffusion's first-party terms weren't found.
- OpenAI and Midjourney terms are quoted from search snippets of the first-party pages, because direct fetch returned 403.
- PVFX Foundry and Nikoichu icon licences were seen only on the itch.io CC0 tag listing.
- The Pokémon Essentials takedown is sourced from press coverage, not a first-party notice.
- Fiverr gig prices appeared in search results but weren't verified, so they're excluded from §5.
- Whether Google Play's AI policy reaches static, pre-generated assets is inferred from its definition ("based on user prompts"), not stated.

---

## Sources

[kenney-support]: https://kenney.nl/support
[kenney-tinytown]: https://kenney.nl/assets/tiny-town
[kenney-tinydungeon]: https://kenney.nl/assets/tiny-dungeon
[kenney-roguelike]: https://kenney.nl/assets/roguelike-rpg-pack
[kenney-pixelui]: https://kenney.nl/assets/pixel-ui-pack
[cc0]: https://creativecommons.org/publicdomain/zero/1.0/
[cc-by-legal]: https://creativecommons.org/licenses/by/4.0/legalcode.en
[cc-faq]: https://creativecommons.org/faq/
[oga-faq]: https://opengameart.org/content/faq
[oga-50monsters]: https://opengameart.org/content/50-monsters-pack-2d
[oga-tinycreatures]: https://opengameart.org/content/tiny-creatures
[oga-zelda]: https://opengameart.org/content/zelda-like-tilesets-and-sprites
[oga-dcss]: https://opengameart.org/content/dungeon-crawl-32x32-tiles
[oga-dcss-sup]: https://opengameart.org/content/dungeon-crawl-32x32-tiles-supplemental
[oga-lpc]: https://opengameart.org/content/liberated-pixel-cup-lpc-base-assets-sprites-map-tiles
[oga-sharm]: https://opengameart.org/content/16x16-overworld-tiles
[itch-cc0]: https://itch.io/game-assets/free/tag-cc0
[itch-pokemon-tag]: https://itch.io/game-assets/tag-pokemon/tag-tileset
[ninja]: https://pixel-boy.itch.io/ninja-adventure-asset-pack
[ggbot-font]: https://ggbot.itch.io/public-pixel-font
[limezu-mi]: https://limezu.itch.io/moderninteriors
[sproutlands]: https://cupnooble.itch.io/sprout-lands-asset-pack
[kenmi]: https://kenmi-art.itch.io/cute-fantasy-rpg
[josee]: https://n3cloud.itch.io/pocket-creature-tamer-adventure-kit-16-x16-rpg-asset-pack
[cyangmou]: https://cyangmou.itch.io/pixel-rpg-monster
[espriteador]: https://el-espriteador.itch.io/pokemon-style-tileset
[apoloa4]: https://apoloa4.itch.io/pokemon-8bit-style-asset-pack
[enrisco]: https://enrisco.itch.io/greenhill-tilemap
[rate-ded]: https://yourded4dey.itch.io/commission-info
[rate-filus]: https://davidfilus.carrd.co/
[rate-zoiskart]: https://zoiskart.carrd.co/
[zoiskart]: https://zoiskart.carrd.co/
[aseprite-faq]: https://www.aseprite.org/faq/
[libresprite]: https://libresprite.github.io/
[libresprite-gh]: https://github.com/LibreSprite/LibreSprite
[pixelorama]: https://pixelorama.org/
[pixelorama-gh]: https://github.com/Orama-Interactive/Pixelorama
[usco-ai]: https://www.copyright.gov/ai/
[usco-newsnet]: https://www.copyright.gov/newsnet/2025/1060.html
[openai-tou]: https://openai.com/policies/row-terms-of-use/
[mj-tos]: https://docs.midjourney.com/hc/en-us/articles/32083055291277-Terms-of-Service
[mj-commercial]: https://docs.midjourney.com/hc/en-us/articles/27870375276557-Using-Images-Videos-Commercially
[pixellab-tos]: https://www.pixellab.ai/termsofservice
[gp-ai]: https://support.google.com/googleplay/android-developer/answer/13985936
[gp-ai-faq]: https://support.google.com/googleplay/android-developer/answer/14094294
[gp-ip]: https://support.google.com/googleplay/android-developer/answer/9888072
[gp-impersonation]: https://support.google.com/googleplay/android-developer/answer/9888374
[apple-guidelines]: https://developer.apple.com/app-store/review/guidelines/
[nintendo-palworld]: https://www.nintendo.co.jp/corporate/release/en/2024/240919.html
[tsr-search]: https://www.spriters-resource.com/browse/games/?name=pokemon
[pokeapi]: https://github.com/PokeAPI/sprites
[pokeapi-licence]: https://raw.githubusercontent.com/PokeAPI/sprites/master/LICENCE.txt
[tuxemon-attr]: https://github.com/Tuxemon/Tuxemon/blob/development/ATTRIBUTIONS.md
[kotaku-essentials]: https://kotaku.com/popular-pokemon-fan-game-creation-tool-disappears-after-1828694609
[nl-essentials]: https://www.nintendolife.com/news/2018/08/nintendo_enforces_takedown_of_fan-made_game_creator_pokemon_essentials

Licences and terms:
- Kenney licence: https://kenney.nl/support
- CC0 deed: https://creativecommons.org/publicdomain/zero/1.0/
- CC BY 4.0 legal code: https://creativecommons.org/licenses/by/4.0/legalcode.en
- CC FAQ (DRM/ETMs): https://creativecommons.org/faq/
- OpenGameArt FAQ (licences, App Store, ripped art): https://opengameart.org/content/faq
- Aseprite FAQ: https://www.aseprite.org/faq/
- LibreSprite: https://github.com/LibreSprite/LibreSprite
- Pixelorama: https://github.com/Orama-Interactive/Pixelorama
- OpenAI Terms of Use: https://openai.com/policies/row-terms-of-use/
- Midjourney ToS: https://docs.midjourney.com/hc/en-us/articles/32083055291277-Terms-of-Service
- PixelLab ToS: https://www.pixellab.ai/termsofservice

Store policy and law:
- Apple App Store Review Guidelines (updated 2026-10-16): https://developer.apple.com/app-store/review/guidelines/
- Google Play AI-Generated Content: https://support.google.com/googleplay/android-developer/answer/13985936 and https://support.google.com/googleplay/android-developer/answer/14094294
- Google Play Intellectual Property: https://support.google.com/googleplay/android-developer/answer/9888072
- Google Play Impersonation: https://support.google.com/googleplay/android-developer/answer/9888374
- US Copyright Office, AI Part 2 (NewsNet 1060): https://www.copyright.gov/newsnet/2025/1060.html
- Nintendo v. Pocketpair release: https://www.nintendo.co.jp/corporate/release/en/2024/240919.html

Packs and rate cards: see the link definitions above (each is cited inline where used).
