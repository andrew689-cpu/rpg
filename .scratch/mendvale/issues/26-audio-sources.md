# Where can $0 music and sound effects come from?

Type: research
Status: resolved
Blocked by: none

## Question

Find sources of music and sound effects Mendvale can ship for $0 on Android and iOS (see `spec.md` §5 and the answer to ticket 02, "Where can original or licensable pixel art come from, and at what cost?"):
- **Licences:** the same rules as art. CC0, OGA-BY and commercial licences granting app-store rights are safe. CC-BY, CC-BY-SA and GPL clash with the App Store's terms. Check each source's actual licence text, and flag anything ripped from commercial games.
- **Music:** CC0 or OGA-BY chiptune and lo-fi packs that are cozy to adventurous, enough for about 33 Areas with a Blighted and a restored mood (each Restoration stage may change an Area's music and ambient track), plus battle, Boss, town and title themes. Can one composer's catalogue cover it in one style?
- **SFX:** CC0 UI, battle, footstep, catch and ambient packs (Kenney, OpenGameArt, freesound CC0, itch.io). Ninja Adventure's bundled audio counts.
- **Self-made and generated:** free tools (jsfxr, Bfxr, BeepBox, LMMS, Furnace). The store-policy and copyright status of AI-generated music, as ticket 02 checked for art.
- **Godot 4.7 constraints:** formats (Ogg Vorbis, WAV), seamless looping, and file sizes against the 150 MB build limit (ticket 17).

## Answer

Findings: branch `research/audio-sources`, file `research/audio-sources.md` (licence files, pack pages, store terms and Godot 4.7 docs, checked 2026-11-14).

**Recommendation: Ninja Adventure's own audio as the base, Juhani Junkala's CC0 packs for battles, and CC0 SFX packs to fill the gaps.**

- **Ninja Adventure audio (CC0 1.0, the pack's `LICENSE.txt`):** 40 music tracks (42.6 min), 15 jingles and 132 SFX in the current zip (the itch page undercounts). It comes from the same pack as the world art, so the style matches.
  - **Overworld coverage:** towns, fields, caves, crypts, ruins, dark moods ("Curse", "Dark Forest", "Lament"), title, story, finale and credits. That's about 22 overworld cues to share across 33 Areas, each Blighted and restored.
- **Battle music gap:** the pack has only 2 fight tracks and 1 tension track.
  - **The fill:** Juhani Junkala's **JRPG Music Pack #1–#5** (24 tracks, each `INFO.txt` says CC0) and his CC0 Epic Boss Battle loop. His 17-track G&T RPG OST is **OGA-BY 3.0** (usable with credit).
  - **One style?** Juhani's packs could cover the whole game alone, but they're orchestral and haven't been listened to side by side with Ninja Adventure, so **test the mix by ear first**.
- **SFX gaps:** Ninja Adventure has **no footsteps and no catch sounds**, only 5 creature sounds, and 9 ambient loops (rain, river, storm, waves, wind).
  - **The fill (all CC0):**
    - **Kenney:** Interface, UI, Impact, RPG Audio (with footsteps) and Jingles
    - **rubberduck on OpenGameArt:** creature, RPG and water sounds
    - **SubspaceAudio's** free 512 SFX
    - **freesound**, with the CC0 filter only
- **Self-made:** ChipTone (output stated CC0) or jsfxr (Unlicense) for catch sounds and per-species cries. BeepBox (MIT) or Furnace for any extra battle cues. A GPL tool doesn't make its output GPL.
- **AI music is out:** Suno's free tier is personal and non-commercial only, and paid tiers give no copyright guarantee and no non-infringement warranty. Prompt-only output isn't copyrightable in the US. Udio's terms weren't checked.
- **Godot 4.7:**
  - **Formats:** Ogg Vorbis for music, WAV for SFX (imported as Quite OK Audio by default).
  - **Loops:** Ogg loops have only a loop start (Loop Offset).
  - **Blighted to restored:** `AudioStreamInteractive` can crossfade between tracks. `AudioStreamSynchronized` can layer synced tracks, but no free pack ships separate stems, so **Restoration changes music by crossfade, not by adding layers**.
- **Size:** the music is 62.5 MB as shipped, about 31 MB re-encoded at 96 kbps or 20 MB at 64 kbps. Godot has no Ogg bitrate setting, so re-encode before import. This likely passes ticket 17's 60 MB custom-template trigger, but stays far below the 150 MB fail gate.

**Risks:**
- **CC-BY trap:** SubspaceAudio's paid bundles are CC-BY 4.0. Only the free OpenGameArt subsets are safe.
- **Unknown origins:**
  - Ninja Adventure names no composer, and the licence of the soundfont its author used is unknown.
  - The kmontesdev "CC0" 2 GB pack doesn't say where its sounds came from, so avoid it.
- **Can't go in the public repo:** Sonniss, Leohpaz and Pixabay are free for games but forbid redistributing the raw files. Kevin MacLeod's free tier is CC-BY, so it's excluded.
- **No game-music remixes, covers or rips.**
- **Not yet checked:** loop seams by ear, Kenney's file lists, and Godot's beat- or bar-synced transitions.

**Consequences:** ticket 33, "What does Mendvale sound like?", is unblocked. It picks the style (whether Ninja Adventure and Juhani mix), the track list per Area and stage (crossfades, not layers), and the SFX list including footsteps, catch sounds and cries.
