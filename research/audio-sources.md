# Research: $0 music and sound-effect sources for Mendvale

Ticket: [`.scratch/mendvale/issues/26-audio-sources.md`](../.scratch/mendvale/issues/26-audio-sources.md)
Researched: 2026-11-14. All licence texts and pack contents are as shown on the cited page (or in the downloaded file) on that date. They can change, so re-check before you download.
Method: first-party pack pages, licence texts, files inside the downloaded packs, official tool repos, Suno's own terms, and the Godot 4.7 docs. Every claim cites a source ID from the [Sources](#sources) list. Lines marked **Analysis** are my judgement, not something a source states.

**Question:** Where can Mendvale get music and SFX for $0 that it can ship on Android and iOS, under the same licence rules as art (§5.1 of the spec: CC0, OGA-BY, or a commercial licence granting app-store rights; CC-BY, CC-BY-SA and GPL clash with the App Store)? It needs music for ~33 Areas with a Blighted and a restored mood, plus battle, Boss, town and title themes, and UI, battle, footstep, catch and ambient SFX. Can one composer cover it in one style? What about free tools, AI music, and Godot 4.7 format, looping and size limits?

---

## TL;DR

1. **Use Ninja Adventure's own audio as the base.** The world-art pack we already use bundles **40 music tracks (42.6 min), 15 jingles and 132 SFX**, all under the pack's **CC0 1.0** `LICENSE.txt` ([NA-zip]; [NA-page]). The itch page still advertises "37 Music" and "100+ Sound effect", so the current zip holds more than the page says ([NA-page]). It is one creator, one toolchain (FL Studio) and the same pack as the art, so it is the only source that matches the visual style by default.
2. **One catalogue can cover the overworld, but not the battles.** Ninja Adventure has a full spread of moods: 3 village themes plus "Lost Village", fields, caves, crypts, ruins, "Curse", "Dark Forest", "Lament", title, story, end and credits. That gives about 22 overworld cues to share across ~33 Areas × 2 moods. It has **only 2 "Fight" tracks and 1 "Tension"**, so wild, trainer, Rival and Boss battles can't each get their own theme ([NA-zip]).
3. **Best CC0 fill for battles is Juhani Junkala** (uploaded as SubspaceAudio). His CC0 *JRPG Music Pack* #1–#5 has 24 tracks across Exploration, Towns, Evil, Calm and Action, each pack's `INFO.txt` says "released under CC0", and there is a CC0 "Epic Boss Battle" loop ([oga-jrpg1]–[oga-jrpg5]; [oga-boss]). His 17-track *G&T RPG soundtrack* is **OGA-BY 3.0**, so it's allowed with credit ([oga-gt]). **Trap:** his *paid* itch bundles (400 loops, 1000 SFX) are **CC-BY 4.0**, so only the free OGA subsets are safe ([itch-400]; [itch-1000]).
4. **SFX gaps after Ninja Adventure:** footsteps (none in the pack), Creature cries (only 5 animal sounds), catch, and most ambience (it has only rain, river, storm, waves and wind) ([NA-zip]). Fill them from **Kenney** (CC0: Interface 100, UI 50, Impact 130, RPG Audio 50 tagged "footstep", Music Jingles 85) ([kenney-support]; [kenney-*]), **rubberduck's** CC0 OGA packs (80 creature, 80 RPG, 40 water/slime) ([oga-rd-creature]; [oga-rd-rpg]; [oga-rd-water]), and **freesound with the CC0 filter only** ([freesound-faq]). Make catch and cry sounds in **ChipTone** (output stated CC0) or **jsfxr** (Unlicense) ([chiptone]; [jsfxr]).
5. **AI music is out for $0.** Suno's free tier is "personal and non-commercial" only. Paid tiers get an assignment, but Suno "makes no representation… that any copyright will vest in any Output" and gives no non-infringement warranty ([suno-terms]; [suno-blog]). Prompt-only output isn't copyrightable in the US ([usco-newsnet]).
6. **Godot 4.7:** use **Ogg Vorbis for music and WAV for short SFX**. WAV imports default to **Quite OK Audio** compression. Ogg loops support only a loop *start* (Loop Offset) ([godot-import]). **AudioStreamInteractive** can crossfade Blighted→restored on beat or bar boundaries ([godot-interactive]). **AudioStreamSynchronized** can layer up to 32 synced stems ([godot-sync]), but no free pack found ships stems.
7. **Size:** Ninja Adventure music is 62.5 MB as shipped (160–320 kbps). Re-encoding it to 96 kbps gives about **31 MB**, and to 64 kbps about **20 MB**. Its SFX are 37.6 MB of 16-bit stereo PCM ([NA-zip]; my arithmetic). Godot shows no bitrate option for Ogg ([godot-import]), so re-encode before import. Engine (~25 MB) plus audio at 96 kbps already reaches ticket 17's **60 MB** custom-template trigger before art. The **150 MB** fail gate is far away (spec §6).

---

## 1. Ninja Adventure's bundled audio (inspected)

I listed and probed the pack zip (`Ninja Adventure - Asset Pack.zip`, 89 MB, top folder dated 2026-03-30), which the art-direction work downloaded on 2026-11-13 ([NA-zip]). Its `LICENSE.txt` is the full CC0 1.0 Universal text. The README says "They are released under the Creative Commons Zero (CC0) license… Attribution is not required but appreciated" (`prototypes/art-direction/assets/NinjaAdventure-README.md`).

| Folder | Files | Size | Format | Contents |
|---|---|---|---|---|
| `Audio/Musics` | 41 (40 tracks + a short cut of "Story") | 62.5 MB | Ogg Vorbis, 44.1 kHz stereo, 160 / 192 / 320 kbps nominal | 19–154 s each, 42.6 min in all. No loop tags; the Vorbis comments only say `ENCODER=FL Studio` |
| `Audio/Jingles` | 15 | 4.2 MB | WAV 44.1 kHz/16-bit stereo | GameOver ×4, LevelUp ×3, Secret ×4, Success ×4 |
| `Audio/Sounds` | 132 | 33.4 MB | WAV 44.1 kHz/16-bit stereo | Alert 6, Ambient 9, Bonus 10, Creature 5, Elemental 26, Hit & Impact 13, Jump & Bounce 8, Magic & Skill 11, Menu 25, Voice 10, Whoosh & Slash 9 |

**Music track titles, grouped by possible use** (the grouping is Analysis, a starting point for ticket 33):

| Use | Tracks |
|---|---|
| Title / story | 38 Intro, 1 Adventure Begin, 6 Story, 3 Revelation |
| Town (restored) | 4 Village, 33 Calm Village, 36 Village, 20 Good Time |
| Town (Blighted) | 26 Lost Village |
| Fields / routes (restored) | 5 Peaceful, 11 Clearing, 23 Road, 27 Chill, 31 Sunny, 35 Adventure |
| Water | 18 Aquatic, 39 Boat |
| Caves / dungeons / landmarks | 2 The Cave, 21 Dungeon, 40 Crypt, 30 Ruins, 12 Temple, 32 Manor, 10 Dark Castle |
| Blighted / sad / eerie | 14 Curse, 37 Dark Forest, 16 Melancholia, 29 Lament, 9 Quiet, 7 Sad Theme, 13 Mystical, 22 Dream |
| Battle | 17 Fight (32 s), 34 Fight (96 s), 28 Tension |
| Finale / ending | 24 Final Area, 19 Ascension, 8 End Theme, 25 End Theme 2, 15 Credit Theme |

- **Style consistency: high.** Every track is an FL Studio render ([NA-zip] tags). The author says "I use FL Studio!" and "I use this soundfont: https://musical-artifacts.com/artifacts/8" ([NA-comments]).
- **Looping:** 17 of the 40 tracks are a whole number of seconds long (32.0, 48.0, 60.0, 96.0 s and so on). **Analysis:** that suggests bar-aligned renders that may loop cleanly, but I didn't verify the seams by ear.
- **Red flags:**
  - **No composer is named** apart from the pack credit "Pixel-boy and AAA" ([NA-page]).
  - **The soundfont's licence is unknown.** musical-artifacts.com returned a Cloudflare challenge, so I couldn't read it. CC0 "makes no warranties" about the work ([cc0]), so the risk sits with us if a sample licence is ever disputed. **Analysis:** low, because the samples are rendered into an original composition, but log it.
- **SFX gaps:** no footsteps, no catch or capture sounds, only 5 creature sounds (Bird, Dog, Duck, Wings ×2), and ambience limited to Rain ×3, River, Storm, Wave ×2 and Wind ×2. **Useful as-is:** Menu ×25 for UI; Hit, Impact, Slash and Elemental for battle effects; Secret, Success and LevelUp jingles for the Restoration chime, a successful catch and evolution.

---

## 2. Music sources

| Source | Licence (exact) | Link | Coverage | Style consistency | Red flags |
|---|---|---|---|---|---|
| **Ninja Adventure** (Pixel-boy & AAA) | CC0 1.0 (pack `LICENSE.txt`) | [NA-page] | 40 tracks, 42.6 min: towns, fields, caves, dark, battle ×2, title, credits | **Highest**: one toolchain, same pack as the art | Composer unnamed; soundfont licence unverified (§1) |
| **Juhani Junkala: JRPG Music Pack #1–#5** (uploader SubspaceAudio) | CC0 (OGA field + `INFO.txt`: "released under CC0 creative commons license. You can do anything you want with these tunes.") | [oga-jrpg1] [oga-jrpg2] [oga-jrpg3] [oga-jrpg4] [oga-jrpg5] | 24 tracks, 32.6 min: Exploration 6, Towns 4, Evil 5, Calm 6, Action 3. Ogg ~260 kbps | High within the series (one composer, one series) | None found. Full 400-loop bundle is CC-BY 4.0 (see below) |
| Juhani Junkala: Epic Boss Battle | CC0 | [oga-boss] | 1 seamless loop (WAV, 21.8 MB) | Orchestral, "inspired by God of War game series" | Inspiration only; no sampled content claimed |
| Juhani Junkala: 4 Chiptunes (Adventure), 5 Chiptunes (Action), 12 Music Loops | CC0 | [oga-chip4] [oga-chip5] [oga-12loops] | 4 + 5 + 12 tracks (3.2 + 4.7 + 14 min); "seamlessly looping" | **Different style** (NES/C64 chiptune, metal-chip, sports) from the JRPG packs | — |
| Juhani Junkala: G&T RPG soundtrack (posted by Bo Jingles) | **CC-BY 4.0 / OGA-BY 3.0** (dual): take it under OGA-BY | [oga-gt] | 17 tracks: overworld, towns, caves, battle, victory, harbour, pub | Coherent RPG OST | Credit "Juhani Junkala" required. Remixes of it by others are CC-BY/OGA-BY too ([oga-ambient-evil]) |
| SubspaceAudio paid bundles (400 Indie Game Music Loops, $79.90+) | **CC BY 4.0** ("all licenses are CC BY 4.0") | [itch-400] | 400 loops + 55 extras, 8 h 25 min | Many styles | **Not allowed without written permission** (CC-BY clashes with iOS) |
| **Holizna** (HoliznaCC0) | CC0 on every OGA page checked ("This music is Public Domain CC0, Use it how you want") | [oga-holizna-adv], [fma-holizna] | Huge: 692 tracks on FMA. OGA collections: Adventure / Happy / Chill Chiptunes, Quiet Village, Caves, Haunted Mansion, Title Screens, Game Over, Lo-Fi (several) | **Low across the catalogue** (chiptune, lo-fi, funk, retrowave, phonk) | Long MP3 songs, not loops. A separate Patreon account ("Orphaned Media") is *not* CC0 ([fma-holizna] search listing). Lo-fi sample sources not stated |
| Kenney Music Jingles | CC0 | [kenney-jingles] | 85 short jingles | Mixed instruments | None |
| Kevin MacLeod (incompetech) | Free tier "Requires that you credit the music" (CC-BY); paid Standard License | [incompetech] | Very large | — | **Exclude** unless the paid licence is bought |
| Pixabay Music | Pixabay Content License (no attribution; no "Standalone" redistribution) | [pixabay] | Large | Mixed | Not CC0 or OGA-BY. The no-standalone-redistribution clause conflicts with a **public repo**. **Exclude** |

**Can one composer cover it in one style?**
- **Ninja Adventure** covers the overworld, title and ending in one style, and it matches the art. It falls short only on battle variety.
- **Juhani Junkala's JRPG #1–#5 + G&T OST** (24 CC0 + 17 OGA-BY ≈ 41 tracks) could cover the whole game in a single synth-orchestral JRPG style, battles included ([oga-jrpg1]–[oga-jrpg5]; [oga-gt]).
- **Analysis:** mixing the two is the main audio-style risk. Ninja Adventure is a soundfont/FL Studio sound and Juhani's JRPG packs are orchestral. Listen-test before mixing. If they clash, either keep Ninja Adventure everywhere and write the extra battle cues yourself (§4), or move the whole soundtrack to Juhani.

---

## 3. SFX sources

| Source | Licence (exact) | Link | Coverage | Style | Red flags |
|---|---|---|---|---|---|
| **Ninja Adventure** | CC0 1.0 | [NA-page] | 132 SFX + 15 jingles (§1) | Matches the music and art | No footsteps or catch sounds; few creature sounds |
| **Kenney** audio packs | "all game assets on the asset pages are public domain licensed (CC0)… even in commercial projects. Attribution is not required." | [kenney-support] | Interface Sounds 100, UI Audio 50, Impact Sounds 130 (tags impact, foley), RPG Audio 50 (tags foley, rpg, footstep, weapon), Digital Audio 60, Music Jingles 85; also *50 RPG sound effects* on OGA (CC0) | Clean, consistent within a pack | Pages list tags only, not file names, so contents weren't checked file by file |
| **SubspaceAudio: 512 Sound Effects (8-bit style)** | CC0 | [oga-512] | 512 retro SFX (UI, jumps, hits, explosions, pick-ups) | 8-bit / chip | Full 1000/6000 packs are CC BY 4.0 ([itch-1000]) |
| **rubberduck** packs | CC0 | [oga-rd-creature] [oga-rd-rpg] [oga-rd-water] [oga-rd-synth] | 80 creature (cute ×10, grunt, roar, hurt…), 80 RPG (creature ×22, items, spells), 40 water/slime (6 loops), 50 retro synth (made in LMMS "from scratch") | Home-recorded; varied | Quality varies ("recorded with an android device" for the 100-SFX pack) |
| artisticdude **RPG Sound Pack** | CC0 | [oga-artisticdude] | 95 WAV: spells, swings, sword clash, inventory | Realistic | — |
| **Fantozzi's Footsteps** | CC0 (from freesound pack 10338) | [oga-fantozzi] | 12 steps (grass/sand, stone) | Realistic | — |
| **freesound.org** | Per sound: CC0, CC-BY, CC-BY-NC, legacy Sampling+ | [freesound-faq] | Ambience, foley, anything | Varies per uploader | **Use the CC0 filter only.** Uploaders are "required" not to upload copyrighted material, but moderation is by volunteers ([freesound-faq]). Record each sound ID |
| Leohpaz **RPG Essentials SFX – Free** | Custom: "free to use in your projects", commercial use OK (author's reply), "You may not sell it or distribute this asset pack for free" | [leohpaz] | ~46–48 retro RPG SFX (UI, magic, status, steps, combat) | Retro, consistent | Not CC0. No redistribution, so **keep it out of the public repo** |
| kmontesdev **Fantasy Ambient SFX Pack (CC0)** | "Under a CC0 Public Domain license… commercial or non-commercial" | [kmontes] | "2 gigabytes": hits, ambience, foley, monsters, spells | Realistic | **Origin not stated** (only "No generative AI was used"). Verify before use |
| **Sonniss GDC bundles** | Royalty-free, "No attribution is required"; no resale "as sound effects… original files and any edited or re-designed versions"; no AI/ML training | [sonniss] | ~207 GB of 2015–2024 bundles: pro ambience, foley | Realistic, studio quality | Not CC0. **Can't be committed to the public repo**; ship only inside the build |

**Analysis, coverage against Mendvale's list:**
- UI: Ninja Adventure Menu, plus Kenney Interface/UI if needed.
- Battle hits and effects: Ninja Adventure Hit, Slash, Elemental and Magic, plus Kenney Impact.
- Footsteps by ground: Kenney RPG Audio or Fantozzi.
- Catch, evolution and Restoration chime: Ninja Adventure jingles plus ChipTone/jsfxr.
- Creature cries: generate one per species in ChipTone or jsfxr, or pitch-shift rubberduck's creature set.
- Ambience: Ninja Adventure's 9 loops plus freesound CC0 (forest, birds, cave, town, night).
- Mixing realistic Sonniss or freesound ambience with chip-style SFX is a style risk. Prefer soft, low-level ambience beds.

---

## 4. Self-made and generated

| Tool | Licence | Output rights | Source |
|---|---|---|---|
| **jsfxr** (browser sfxr) | Unlicense | Not stated. **Analysis:** synthesised from parameters, with no bundled samples | [jsfxr] |
| **Bfxr** (bfxr2) | MIT | Not stated | [bfxr2], [bfxr] |
| **ChipTone** (SFB Games) | Name your own price | "All sounds created using ChipTone are FREE to use for any purpose, commercial or otherwise, under the CC0 licence." | [chiptone] |
| **BeepBox** | MIT | Not stated | [beepbox] |
| **Furnace** (chiptune tracker) | GPLv2 or later | Not stated. Exports "entire song, per chip or per channel" audio | [furnace] |
| **LMMS** | GPL | FAQ: "As long as you have just used samples, instruments and effects from LMMS, or know that the external material has correct licenses, you can sell your song" | [lmms-faq] |

- **GPL tools don't make the music GPL:** "The output of a program is not, in general, covered by the copyright on the code of the program" ([gnu-faq]). The exception is output that copies the program's own art or audio, so check any bundled samples or soundfonts.
- **Analysis:** BeepBox or Furnace are the cheapest way to write the missing battle, Rival and Boss cues, and per-species cries come quickly from ChipTone or jsfxr. If you do this, add your own compositions to the ledger as `self-made`.

### AI-generated music
- **Suno** (terms last revised 2026-08-10, effective 2026-09-03):
  - Free/Basic users "will only use such Outputs for your lawful, personal and non-commercial purposes."
  - Pro and Premier: "Suno hereby assigns to you all of its right, title and interest in and to any Output owned by Suno", but Suno "makes no representation or warranty to you that any copyright will vest in any Output." It also disclaims any warranty that use "WILL NOT INFRINGE THE RIGHTS OF ANY THIRD PARTY" ([suno-terms]).
  - Free accounts get "Up to 7 (lifetime) trial downloads… for personal use only" ([suno-blog]).
- **Udio:** I couldn't verify its first-party terms. Secondary reports say downloads were disabled after the 2025 Universal settlement ([udio-press]). Treat it as unavailable.
- **Copyright:** prompt-only output is not protectable in the US ([usco-newsnet]).
- **Stores:** same as art. Apple requires "content that you created or that you have a license to use" (§5.2). Google Play's AI policy targets apps that generate content from user prompts ([apple-guidelines]; [gp-ai]).
- **Verdict:** a $0 budget means Suno's free tier, which is non-commercial, so it's ruled out. Even paid output comes with no ownership or non-infringement guarantee. Use AI for mood references at most.

---

## 5. Godot 4.7 constraints

- **Formats:** "WAV, Ogg Vorbis and MP3." The docs advise: "Consider using WAV for short and repetitive sound effects, and Ogg Vorbis for music, speech, and long sound effects." WAV is light on CPU but large; Ogg is smaller but needs "significantly more processing power"; MP3 uses less CPU than Ogg ([godot-import]).
- **WAV compression:** PCM, IMA ADPCM, or **Quite OK Audio (the default)**, which "reduces file size a bit more than IMA ADPCM and the quality decrease is much less noticeable." Import options can **Force Mono**, **Force Max Rate**, **Trim** and **Normalize**. "There's no audible benefit to using a sample rate greater than 48 kHz" ([godot-import]).
- **Looping:**
  - Ogg and MP3 have **Loop** plus **Loop Offset** (in seconds) only, with forward looping and no loop-end point. WAV has Forward, Ping-Pong and Backward modes with loop points in samples.
  - The Advanced import dialog edits the loop point "with a real-time preview."
  - `finished` "won't be emitted for looping audio" ([godot-import]).
  - So a track with an intro needs Loop Offset set to the bar where the loop starts, and the file must end exactly at the loop's end.
- **Blighted ↔ restored:**
  - **AudioStreamInteractive** combines "clips and a transition table". Transitions can start immediately, on the next beat or bar, or at clip end, with cross-fade or fade in/out and an optional filler clip ([godot-interactive]).
  - **AudioStreamSynchronized** plays up to `MAX_STREAMS = 32` sub-streams "in-sync", with `set_sync_stream_volume()` per stream ([godot-sync]). That suits stem layering, but every pack above ships stereo mixdowns, so layering would need self-made stems.
  - **Conflict to check:** the import page still says the BPM, Beat Count and Bar Beats settings "are currently unused, but they will be used in the future for interactive music support" ([godot-import]), while AudioStreamInteractive offers beat/bar-synced transitions ([godot-interactive]). Test bar-sync in 4.7.2 before relying on it.
- **Size budget** (my arithmetic, from [NA-zip] durations):

| Content | As shipped | Re-encoded |
|---|---|---|
| Ninja Adventure music (2,559 s) | 62.5 MB | 96 kbps ≈ 30.7 MB; 80 kbps ≈ 25.6 MB; 64 kbps ≈ 20.5 MB |
| Ninja Adventure SFX + jingles (147 WAV) | 37.6 MB PCM stereo | QOA (Godot default) plus Force Mono: a few MB. Not measured; check the export size report |
| Juhani JRPG #1–#5 (1,957 s) | ~67 MB (~260 kbps) | 96 kbps ≈ 23.5 MB |

- Godot shows no bitrate option for Ogg imports ([godot-import]). **Analysis:** encode the Ogg files at the target bitrate before committing them.
- Spec §6 (ticket 17): the engine is ~25 MB, the build fails above **150 MB**, and a custom export template becomes a task above **60 MB**. Music at 80–96 kbps plus SFX puts the build around 55–65 MB before art. Expect to hit the 60 MB trigger, but nowhere near the gate.

---

## 6. Avoid: ripped, unclear or incompatible audio

| Source | Why |
|---|---|
| Remixes, covers or rips of Pokémon or other commercial game music (YouTube "OST" uploads, VGM sites) | Spec §6: no Pokémon "music or look". OGA bans "Modifications of existing commercial game art" and "clearly non-free IP" ([oga-faq]). Copycat and IP rules apply ([apple-guidelines]; [gp-ip]) |
| CC-BY / CC-BY-SA / GPL music and SFX (incompetech free tier, SubspaceAudio paid bundles, much of OGA's music) | Clash with iOS DRM: "Apple's App Store in particular has been found to have usage terms that conflict with the terms of the GNU GPL, the GNU LGPL, CC-BY-SA, and CC-BY" ([oga-faq]). Allowed only with written permission |
| freesound sounds that aren't CC0 (CC-BY-NC, Sampling+) | NC forbids earning money; Sampling+ is a legacy licence ([freesound-faq]). OGA refuses freesound Sampling+ material ([oga-faq]) |
| Free-to-use but no-redistribution licences (Pixabay, Sonniss, Leohpaz) in the **public repo** | Their raw files can't be published. Same rule as paid art (spec §5.1) |
| CC0 uploads with no stated origin (e.g. the kmontesdev 2 GB pack) | CC0 is only as good as the uploader's rights ([cc0]). Verify or skip |
| Suno free tier / Udio | Non-commercial or unavailable (§4) |

---

## 7. Recommendation

1. **Music:**
   - **Base:** Ninja Adventure's 40 tracks (CC0) for title, towns, routes, caves, Blighted moods, finale and credits. Areas share cues by Habitat and chapter (ticket 33).
   - **Blighted → restored:** give each pair two tracks (e.g. Lost Village → Village, Dark Forest → Clearing). Crossfade with AudioStreamInteractive on Restoration.
   - **Battles:** listen-test Juhani Junkala's CC0 JRPG #5 Action, #3 Evil and Epic Boss Battle against Ninja Adventure. If they fit, use them for wild, trainer, Rival and Boss battles. If not, write 3–4 battle cues in BeepBox or Furnace to match.
2. **SFX:**
   - Ninja Adventure for UI, battle and jingles.
   - Kenney (CC0) for footsteps and extra UI and impacts.
   - ChipTone or jsfxr for catch, Creature cries and the Restoration chime.
   - freesound **CC0 only** for missing ambience beds.
3. **Licence whitelist for audio:** the same as art. CC0, OGA-BY (credit), self-made, or a paid licence that explicitly grants app-store rights. Reject CC-BY without written permission, CC-BY-SA, GPL-licensed audio, NC, and anything with no stated licence.
4. **Ledger:** add a row to `assets/LICENCES.csv` for every audio file: source URL, author, licence, download date, and a saved copy of the pack's licence or `INFO.txt`. For freesound, add the sound ID and uploader. Credit Juhani Junkala for any OGA-BY track. Keep no-redistribution files (Sonniss, Leohpaz, Pixabay) out of the public repo.
5. **Build:** re-encode music to 80–96 kbps Ogg before import. Keep SFX as WAV with QOA. Use Force Mono for mono-intended SFX. Set Loop and Loop Offset per track and check every loop seam by ear.

---

## 8. Open items / unverified

- The licence of the soundfont Ninja Adventure's author uses (musical-artifacts.com/artifacts/8) could not be read: Cloudflare challenge.
- Ninja Adventure loop seams were not checked by ear. "Loopable" is inferred from bar-exact lengths for 17 of 40 tracks.
- Kenney audio pack contents were checked by tags and file counts only, not file lists.
- Holizna track counts per OGA collection weren't checked. The non-CC0 Patreon account appears only in search listings.
- Udio's current first-party terms weren't checked; only press reports were read.
- The QOA size reduction for the SFX wasn't measured.
- Godot 4.7's beat/bar-synced transitions need testing, because the import docs still call BPM/beat settings "unused".
- Ninja Adventure's itch page says 37 tracks and 100+ SFX, while the zip has 40 tracks and 132 SFX. The page appears outdated.

---

## Sources

Packs and pages:
- [NA-page] Ninja Adventure Asset Pack (itch.io): https://pixel-boy.itch.io/ninja-adventure-asset-pack
- [NA-comments] Ninja Adventure comments (author on FL Studio and soundfont): https://pixel-boy.itch.io/ninja-adventure-asset-pack/comments
- [NA-zip] `Ninja Adventure - Asset Pack.zip` from [NA-page], downloaded 2026-11-13: `Audio/` folder and `LICENSE.txt` inspected (file list, Vorbis headers and tags, WAV headers)
- [oga-jrpg1] https://opengameart.org/content/jrpg-pack-1-exploration
- [oga-jrpg2] https://opengameart.org/content/jrpg-pack-2-towns
- [oga-jrpg3] https://opengameart.org/content/jrpg-pack-3-evil
- [oga-jrpg4] https://opengameart.org/content/jrpg-pack-4-calm
- [oga-jrpg5] https://opengameart.org/content/jrpg-pack-5-action (zips for #1–#5 downloaded and `INFO.txt` read)
- [oga-boss] https://opengameart.org/content/boss-battle-music
- [oga-chip4] https://opengameart.org/content/4-chiptunes-adventure
- [oga-chip5] https://opengameart.org/content/5-chiptunes-action
- [oga-12loops] https://opengameart.org/content/12-music-loops
- [oga-gt] https://opengameart.org/content/gt-rpg-soundtrack
- [oga-ambient-evil] https://opengameart.org/content/ambient-evil-juhani-junkala
- [oga-512] https://opengameart.org/content/512-sound-effects-8-bit-style
- [itch-400] https://subspaceaudio.itch.io/indie-game-music-loops
- [itch-1000] https://subspaceaudio.itch.io/1000-retro-sound-effects
- [oga-holizna-adv] https://opengameart.org/content/adventure-chiptunes-collection (also checked: chill-chiptunes-collection, happy-chiptunes-collection, quiet-village-collection, caves-collection, haunted-mansion-collection, title-screens-beginnings-collection, game-over-collection, lo-fi-and-chill-collection, happy-lo-fi-lofi-collection, sad-lo-fi-lofi-collectioni, chill-beats-collection, gamer-beats-collection, relaxing-instrumentals-collection, chillout-instrumentals-collection, game-boi-collection)
- [fma-holizna] https://freemusicarchive.org/music/holiznacc0/
- [kenney-support] https://kenney.nl/support
- [kenney-*] https://kenney.nl/assets/interface-sounds, https://kenney.nl/assets/ui-audio, https://kenney.nl/assets/impact-sounds, https://kenney.nl/assets/rpg-audio, https://kenney.nl/assets/digital-audio; [kenney-jingles] https://kenney.nl/assets/music-jingles; Kenney on OGA: https://opengameart.org/content/50-rpg-sound-effects
- [oga-rd-creature] https://opengameart.org/content/80-cc0-creature-sfx
- [oga-rd-rpg] https://opengameart.org/content/80-cc0-rpg-sfx
- [oga-rd-water] https://opengameart.org/content/40-cc0-water-splash-slime-sfx
- [oga-rd-synth] https://opengameart.org/content/50-cc0-retro-synth-sfx (and https://opengameart.org/content/100-cc0-sfx)
- [oga-artisticdude] https://opengameart.org/content/rpg-sound-pack
- [oga-fantozzi] https://opengameart.org/content/fantozzis-footsteps-grasssand-stone
- [leohpaz] https://leohpaz.itch.io/rpg-essentials-sfx-free
- [kmontes] https://kmontesdev.itch.io/fantasy-ambient-sound-effects-pack-cc0
- [sonniss] https://sonniss.com/gameaudiogdc
- [incompetech] https://incompetech.com/music/royalty-free/licenses/
- [pixabay] https://pixabay.com/service/license-summary/

Licences and policies:
- [cc0] CC0 1.0 deed: https://creativecommons.org/publicdomain/zero/1.0/
- [oga-faq] OpenGameArt FAQ (licences, App Store, DRM, commercial-game modifications, freesound): https://opengameart.org/content/faq
- [freesound-faq] https://freesound.org/help/faq/
- [gnu-faq] GNU GPL FAQ (output of GPL programs): https://www.gnu.org/licenses/gpl-faq.en.html#GPLOutput
- [suno-terms] Suno Terms of Service (rev. 2026-08-10): https://suno.com/terms
- [suno-blog] "An update to our downloads policy and Terms of Service" (2026-08-10): https://suno.com/blog/suno-updates-tos
- [udio-press] Secondary press only: https://www.digitalmusicnews.com/2025/10/31/udio-umg-deal-downloads-resumed-48-hours/
- [usco-newsnet] US Copyright Office, AI Part 2: https://www.copyright.gov/newsnet/2025/1060.html
- [apple-guidelines] App Store Review Guidelines: https://developer.apple.com/app-store/review/guidelines/
- [gp-ai] Google Play AI-Generated Content: https://support.google.com/googleplay/android-developer/answer/13985936
- [gp-ip] Google Play Intellectual Property: https://support.google.com/googleplay/android-developer/answer/9888072

Tools:
- [jsfxr] https://github.com/chr15m/jsfxr
- [bfxr] https://www.bfxr.net/ ; [bfxr2] https://github.com/increpare/bfxr2
- [chiptone] https://sfbgames.itch.io/chiptone
- [beepbox] https://github.com/johnnesky/beepbox
- [furnace] https://github.com/tildearrow/furnace
- [lmms-faq] https://docs.lmms.io/user-manual/getting-started/faq

Godot 4.7 docs:
- [godot-import] Importing audio samples: https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_audio_samples.html
- [godot-interactive] AudioStreamInteractive: https://docs.godotengine.org/en/stable/classes/class_audiostreaminteractive.html
- [godot-sync] AudioStreamSynchronized: https://docs.godotengine.org/en/stable/classes/class_audiostreamsynchronized.html
