# Research: Which 2D engine fits an agent-built pixel-art game for Android + iOS?

Ticket: [`.scratch/project-wildling/issues/01-engine-choice.md`](../.scratch/project-wildling/issues/01-engine-choice.md)
Researched: 2026-11-13. Version numbers and licence terms below are as of that date.
Method: primary sources only (official docs, licence pages, release notes, first-party repos). Every claim carries a numbered citation from the [Sources](#sources) list. Where only community or vendor-comparison data exists, the text says so. Lines marked **Analysis** are my judgement, not something a source states.

## TL;DR

**Recommendation: Godot 4 (pin 4.7.x stable), scripted in statically-typed GDScript, with game content as custom `Resource` (`.tres`) files and/or JSON.** It is the only candidate that scores well on every criterion: MIT licence with no fees [G1], text scene and resource formats built for version control [G5][G6], a first-class headless CLI for import, export and scripted runs [G4], built-in pixel-art scaling [G8] and a full TileMapLayer editor with terrains (autotiling) [G7], and the largest open-source community of the four [G15].

**Runner-up: Defold.** Pick it instead if APK/IPA size or a guaranteed "text files only, no editor needed" workflow matters more than ecosystem size and tooling depth. Its empty builds are about 10x smaller [D3], but its community and asset ecosystem are much smaller [D10][D11], it uses Lua, and its tile maps have no documented autotiling [D6].

**Not recommended:** Unity, because the Personal licence cannot be activated from the command line [U6], scenes are GUID-linked YAML [U4], and the editor is heavy. libGDX, because iOS depends on a third-party AOT VM with Java 8/11 limits [L6][L7] and there is no scene or level editor beyond Tiled [L4].

## Versions checked (2026-11-13)

| Engine | Current stable | Notes |
|---|---|---|
| Godot | 4.7.2-stable (2026-08-18); 4.8 at beta3 (2026-11-09) [G2] | Docs "stable" = 4.7 [G3] |
| Unity | 6.3 LTS (6000.3.28f1); 6.6 is the current Supported release (6000.6.9f1, 2026-11-12) [U2] | 6.0 LTS main support ended 2026-10-16 [U2] |
| Defold | 1.14.1 (2026-11-10) [D1] | 1.14.0 shipped 2026-10-12 [D1] |
| libGDX | 1.14.2 (announced with 1.14.1, 2026-05-28) [L1] | Liftoff setup tool targets 1.14.2 by default [L6] |
| Flame (Flutter) | 1.x, MIT [F1][F2] | Alternative, considered briefly |

## Comparison table

Ratings: ++ strong, + adequate, − weak, −− blocker-level concern. They apply to *this* project: agent-built, 2D pixel art, tile maps, turn-based, mobile, $0 budget.

| Criterion | Godot 4 | Unity 6 (2D) | Defold | libGDX (Kotlin/Java) |
|---|---|---|---|---|
| Android export | ++ APK/AAB; needs JDK 17 + Android SDK 35 / NDK r28b; AAB needs Gradle build [G9] | ++ via Hub modules (SDK/NDK/OpenJDK bundled) [U8] | ++ APK or AAB from editor or `bob.jar` [D4][D5] | + Gradle `android:assembleRelease`, sign yourself [L3] |
| iOS export | + needs macOS + Xcode [G10] | + generates an Xcode project; final build in Xcode [U7] | + editor iOS bundling is Mac-only [D7] | − via RoboVM/MobiVM AOT; needs macOS + Xcode; Java 8/11 runtime limits [L6][L7] |
| Pixel-perfect rendering | ++ `viewport` stretch + `integer` scale mode [G8] | ++ Pixel Perfect Camera package [U5] | + nearest filtering via `game.project` [D8]; scaling is DIY (Analysis) | + DIY: nearest filter + viewports (Analysis) |
| Tile maps | ++ TileMapLayer, terrains/autotiling, physics, patterns [G7] | ++ Tilemap + Tile Palette, hex/iso [U9] | + layers, collision, runtime get/set; Tiled exports to it; no autotiling documented [D6] | + loads Tiled TMX; orthogonal renderer; no in-engine editor [L4] |
| Data-driven content | ++ typed custom `Resource` (.tres) + `JSON` class [G6][G11] | + ScriptableObject assets [U10]; JSON via code | + Lua tables / JSON (Analysis) | ++ plain code + any JSON lib (Analysis) |
| Text files agents can edit/diff | ++ `.tscn`/`.tres` human-readable, VCS-friendly [G5][G6]; commit `.uid` sidecars [G12] | − text YAML by default (Force Text) [U4], but GUID/fileID cross-refs (Analysis) | ++ "All data is in text files"; `game.project` is INI [D3][D9] | ++ pure code + Tiled XML (Analysis) |
| Headless / CLI tests | + `--headless`, `--script`, `--import`, `--export-release` [G4]; GUT / gdUnit4 CLI [G13][G14]; exit-code pitfalls [G16] | − `-batchmode -runTests` exists [U3][U11], but Personal licence needs Hub login, no CLI activation [U6] | + `bob.jar` CLI build/bundle (OpenJDK 25) [D5]; headless variant + DefTest [D12] | ++ JUnit on JVM + `gdx-backend-headless` [L8] (GL calls need mocking, Analysis) |
| Licence and cost at $0 revenue | ++ MIT, no fees [G1] | + free under $200K revenue+funding; splash optional on Unity 6; Runtime Fee cancelled [U1][U12] | ++ free, no royalties; Apache-derived; cannot resell the engine [D2] | ++ Apache 2.0 [L2] |
| Empty APK / IPA size | − ~25 MB both (vendor test) [D3] | − ~32 MB APK / ~37 MB IPA (vendor test) [D3] | ++ 2.56 MB APK / 1.35 MB IPA [D3] | n/a (no first-party figure) |
| Community / assets | ++ 120k GitHub stars [G15]; 5,454 Asset Library items [G17] | ++ largest commercial asset store (Analysis) | − 6.5k stars [D10]; 329 portal assets [D11] | + 25.5k stars [L2] |
| Scale to 150+ Creatures, multi-region | ++ data in Resources/JSON; scenes per region (Analysis) | ++ (Analysis) | + (Analysis) | + (Analysis) |

Store costs are the same whichever engine is chosen: Apple Developer Program is US$99/year [P1], Google Play registration is a one-time US$25 [P2], and **every option needs a Mac with Xcode for iOS** (Xcode is a Mac app [P3]; each engine's docs require it [G10][D7][L7]; Unity's "Build Automation" cloud service is the only off-Mac route mentioned [U7]).

## Per-criterion notes

### 1. Android + iOS export maturity and requirements

- **Godot 4.7.** Android needs OpenJDK 17 and the Android SDK (Platform-Tools ≥ 35.0.0, Build-Tools 35.0.1, Platform 35, NDK r28b). AAB export for Google Play requires the Gradle build option. Release builds need a non-debug keystore [G9]. iOS export "must" happen on macOS with Xcode installed and needs an App Store Team ID [G10]. 4.7 added more mobile features: Android export-option splash screens, a built-in `VirtualJoystick` node (useful for an on-screen D-pad), and a per-platform export-template downloader [G18].
- **Unity 6.x.** Android SDK, NDK and OpenJDK install as Unity Hub modules [U8]. iOS is a two-step pipeline: Unity generates an Xcode project, then Xcode builds and deploys it [U7]. It supports iOS 15+ and recommends Xcode 16+ [U13].
- **Defold 1.14.** Android bundles as APK or AAB, with optional R8 shrinking from 1.14.0 [D4]. "Bundling a game for iOS is available only on Mac version of the Defold Editor" [D7]. `bob.jar` can bundle both platforms from the CLI (`--identity`, `--mobileprovisioning` for iOS) [D5]. Native extensions are compiled on Defold's free cloud build server, which can be self-hosted [D13]. This is an external dependency to note.
- **libGDX 1.14.2.** Android uses the standard Gradle flow, and you sign the APK yourself [L3]. iOS goes through the RoboVM/MobiVM backend [L3][L8]. MobiVM requires macOS + Xcode [L7] and supports "most Java 8 and Java 11 runtime features" [L7]. Liftoff notes Java 8 language-level limits for RoboVM, with MOE as an alternative iOS backend [L6]. **Analysis:** iOS is the weakest link of the four here. It depends on a small third-party AOT compiler rather than the engine vendor.

### 2. Pixel-perfect rendering and tile-map support

- **Godot.** The docs prescribe pixel-art setup directly: stretch mode `viewport` (renders at low base resolution, then scales) and stretch scale mode `integer` ("prevents uneven pixel scaling"). Most pixel-art games use base sizes from 256×224 to 640×480, and 640×360 scales cleanly [G8]. TileMapLayer supports multiple layers, shared external TileSets, reusable patterns, terrain autotiling (Connect / Path modes), and per-tile collision [G7].
- **Unity.** The 2D Pixel Perfect package gives a Pixel Perfect Camera with reference resolution, upscale render texture, pixel snapping and crop frame. It needs sprites set to Point filter and no compression [U5]. Tilemap supports Tile Palette painting, collision, and hex and isometric grids [U9].
- **Defold.** Nearest filtering is set via `default_texture_min_filter` / `default_texture_mag_filter = nearest` in `game.project`. Both default to `linear` [D8]. Tile maps support layers, collision from the tile source, and runtime `tilemap.get_tile` / `set_tile`. Tiled and Tilesetter "can export directly to Defold" [D6]. The manual documents no autotiling [D6].
- **libGDX.** `TmxMapLoader` loads Tiled maps, and `OrthogonalTiledMapRenderer` draws them. Infinite TMX maps are not supported [L4]. All level authoring happens in Tiled (external).

### 3. Data-driven content (Creatures, moves, regions as data)

- **Godot.** Custom `Resource` classes give typed, inspector-editable data saved as "version-control-friendly text files (*.tres)". The docs contrast them with JSON, which only yields an untyped Dictionary [G6]. The `JSON` class parses and stringifies for plain-JSON content [G11]. **Analysis:** a `CreatureSpecies` Resource per Creature (or one JSON file per region) scales linearly to 150+ entries with no code change.
- **Unity.** ScriptableObjects are "a data store … independent of GameObjects", saved as project assets [U10].
- **Defold / libGDX.** No first-party data-asset type was found in the sources reviewed. Content would be Lua tables or JSON (Defold) or JSON/Kotlin data classes (libGDX). **Analysis:** fine, but schema validation is entirely up to us.

### 4. Text-based project files agents can edit and diff

This is the criterion that most separates the candidates for an agent-built project.

- **Godot.** `.tscn`/`.tres` are "mostly human-readable and easy for version control systems to manage" [G5]. Scenes carry a `uid` so moved files still resolve [G5]. Since 4.4, scripts and shaders get `.uid` sidecar files that **must be committed**. If agents move files outside the editor, the `.uid` must move too, or scenes warn until re-saved [G12]. Ignore `.godot/` (the cache) [G19].
- **Unity.** Asset serialization defaults to Force Text [U4]. **Analysis:** scenes and prefabs are YAML that links objects by `fileID`/GUID through `.meta` files. Agents can read it but cannot safely author it by hand, so most work has to go through C# editor scripts run in batch mode.
- **Defold.** "All data is in text files - easy for version control systems". Defold markets this explicitly for AI-assisted and agentic workflows [D3]. `game.project` is INI [D9].
- **libGDX.** Everything is source code plus Tiled XML. This is the most agent-friendly format, but it has no visual editor for UI or scenes.

### 5. Headless / CLI testability

- **Godot.** `--headless` is required in CI without a GPU, `--script` runs a script, `--import` imports then quits, and `--export-release` / `--export-debug` build presets [G4]. Test frameworks: GUT 9.x for Godot 4.x, which has a CLI [G13]. gdUnit4 has a CI command-line tool, JUnit XML output, a GitHub Action, and GDScript + C# tests [G14]. **Caveat (community report, reproduced on 4.4.1–4.7.2):** several failures exit 0 in headless mode, including script parse errors and add-on compile errors. CI should therefore gate on JUnit XML and log scanning for `SCRIPT ERROR`, not the exit code alone [G16].
- **Unity.** `-batchmode`, `-nographics`, `-executeMethod`, `-runTests -testPlatform EditMode|PlayMode -testResults` (NUnit XML) [U3][U11]. **Blocker for a $0 project:** "The following procedures don't apply to Unity Personal. To activate a license for Unity Personal, log in to the Unity Hub" [U6]. Ephemeral CI runners and agent sandboxes therefore cannot self-activate a Personal licence.
- **Defold.** `bob.jar` builds and bundles from the CLI (needs OpenJDK 25) [D5]. The automated-testing manual covers a `--variant headless` bundle and DefTest unit tests (Telescope-based) with exit status and logs as the CI signal [D12].
- **libGDX.** It ships a `gdx-backend-headless` backend [L8], and logic tests are plain JUnit on the JVM. **Analysis:** best-in-class for pure-logic tests, but anything touching OpenGL needs mocking.

**Analysis, applying to all engines:** structure the battle, catch and stat logic as engine-independent pure code (GDScript classes with no scene dependency, in Godot's case), so most tests are fast unit tests.

### 6. Licensing and cost at $0 revenue

- **Godot:** MIT. "free to use … for any purpose". Its terms don't apply to your content. You must ship the engine's copyright and licence notice [G1].
- **Unity:** Personal is free for "less than $200K USD of revenue and funds raised in the last 12 months" [U12]. The Runtime Fee was cancelled. The splash screen is optional with Unity 6. Pro/Enterprise prices rose 5% from 2026-01-12 [U1]. **Analysis:** free today, but the terms are set by a company that has changed them before (the Runtime Fee episode, [U1]).
- **Defold:** free, "never … royalty payments", never a subscription. Apache-2.0-derived, but you may not sell the engine itself or derivatives "as a Game Engine Product". Include the licence notices [D2].
- **libGDX:** Apache 2.0 [L2].

### 7. APK / IPA size

The only side-by-side first-party measurement is **Defold's own product page**, a vendor comparison with an incentive to look good. It used empty projects, default settings and release builds: Android arm64 = Defold 2.56 MB, Godot 25.29 MB, Unity 31.75 MB. iOS .ipa = Defold 1.35 MB, Godot 25.29 MB, Unity 36.81 MB. Versions tested were Defold 1.13.0, Godot 4.7.1 and Unity 6.5 [D3]. (The identical Godot Android/iOS figure looks like a possible copy error on their page.) Godot's docs say a custom export template can cut size: stripping debug symbols gives 5–10x on compiled binaries, and disabling 3D about −15% [G20]. Dropping armv7 also helps [G9]. **Analysis:** for a hobby RPG, ~25 MB of engine overhead is acceptable. The art and audio for 100–150 Creatures will dominate the download either way.

### 8. Community and asset ecosystem

GitHub stars: Godot 120.1k [G15], libGDX 25.5k [L2], Flame 10.8k [F2], Defold 6.5k [D10]. Godot Asset Library: 5,454 items [G17]. Defold Asset Portal: 329 assets [D11]. Unity has the largest commercial Asset Store (not measured here). **Analysis:** for AI agents, ecosystem size also means training-data coverage. Godot 4 GDScript and Unity C# are far better represented than Defold Lua or libGDX. Watch out for agents producing Godot 3 syntax. Pin the version in agent instructions.

### 9. Scaling to Large content (150+ Creatures, multiple regions)

**Analysis (no source directly measures this):** none of the engines has a hard limit relevant to 150 Creatures or a few regions. What matters is (a) content-as-data with typed schemas, where Godot Resources and Unity ScriptableObjects are strongest, and (b) per-region scenes or tile maps loaded on demand. Godot's UID system lets files be reorganised without breaking references [G5][G12], which helps as the content tree grows.

### Alternative considered: Flame (Flutter)

Flame is an MIT-licensed, Flutter-based 2D engine [F1][F2] with a `flame_tiled` bridge package listed in its docs [F1]. **Analysis:** all-Dart code is very agent-friendly and Flutter's test tooling is strong. But there is no scene or tile editor, it has a smaller game-specific ecosystem, and iOS still needs Xcode on macOS. It offers no advantage over Godot for a tile-map RPG, so it was not evaluated further.

## Recommendation and trade-offs

**Choose Godot 4.7.x (stable), typed GDScript, with no C#.**

Why:
1. **Agent-editable everything.** Scenes, resources and project settings are text [G5][G6], and content can be typed `.tres` Resources or JSON [G6][G11]. This matches the map's "content is data, not code" rule.
2. **Real CLI.** Import, export and test from the command line with no licence activation step [G4][G13][G14]. This beats Unity Personal for agent sandboxes [U6].
3. **Pixel art and tile maps are first-class**, with documented integer scaling [G8] and terrain autotiling [G7]. That saves building tooling Defold or libGDX would need.
4. **No licence risk** (MIT) [G1] and the largest open-source community [G15].

Trade-offs accepted:
- **Use GDScript, not C#.** C# on Android and iOS is still "experimental" in 4.7 [G21].
- **Bigger binaries** than Defold, about 25 MB vs about 2.5 MB empty [D3]. This can be reduced later with custom templates [G20].
- **Headless exit codes are unreliable**, so CI must parse JUnit/logs [G16]. Write this into the testing ticket.
- **`.uid` sidecar discipline.** Agents must move or delete `.uid` files alongside scripts [G12]. Add this to agent instructions.
- **iOS still needs a Mac with Xcode** and a US$99/yr Apple account [G10][P1]. This is true of every option.
- **Godot 4.8 is in beta** [G2]. Start on 4.7.x and upgrade deliberately.

**When to pick Defold instead:** if download size becomes a hard requirement, or Godot's editor-generated files prove painful for agents. Defold is the only other option with a fee-free licence, all-text project data, and a CLI bundler [D2][D3][D5]. The cost is a smaller ecosystem [D10][D11], Lua, and DIY autotiling and pixel scaling.

## Follow-ups for other tickets

- **09 technical architecture:** define the Creature/Move/Region Resource schemas and keep battle logic scene-independent for unit tests.
- **Quality and release:** CI recipe (`godot --headless --import`, then GUT or gdUnit4 with JUnit output, then `--export-release`), plus log scanning for `SCRIPT ERROR` [G4][G14][G16]. Decide which Mac builds iOS.
- **Agent instructions:** pin Godot 4.7, require typed GDScript, keep `.uid` files with their scripts, and never commit `.godot/` [G12][G19].

## Sources

Godot
- [G1] Godot license page: https://godotengine.org/license/
- [G2] Godot download archive (4.7.2-stable 2026-08-18; 4.8-beta3 2026-11-09): https://godotengine.org/download/archive/
- [G3] Godot docs, "stable" = 4.7 (header on all pages below)
- [G4] Command line tutorial: https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html
- [G5] TSCN file format: https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html
- [G6] Resources: https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html
- [G7] Using TileMaps: https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.html
- [G8] Multiple resolutions (pixel art section): https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html
- [G9] Exporting for Android: https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_android.html
- [G10] Exporting for iOS: https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_ios.html
- [G11] JSON class: https://docs.godotengine.org/en/stable/classes/class_json.html
- [G12] "UID changes coming to Godot 4.4": https://godotengine.org/article/uid-changes-coming-to-godot-4-4/
- [G13] GUT repository: https://github.com/bitwes/Gut
- [G14] gdUnit4 repository: https://github.com/MikeSchulze/gdUnit4
- [G15] godotengine/godot repository: https://github.com/godotengine/godot
- [G16] Godot Forum, "Things that exit 0 in Godot 4 headless even though they failed" (community, not official): https://forum.godotengine.org/t/things-that-exit-0-in-godot-4-headless-even-though-they-failed-measured-reproducible/145990
- [G17] Godot Asset Library: https://godotengine.org/asset-library/asset
- [G18] Godot 4.7 release page: https://godotengine.org/releases/4.7/
- [G19] Version control systems: https://docs.godotengine.org/en/stable/tutorials/best_practices/version_control_systems.html
- [G20] Optimizing a build for size: https://docs.godotengine.org/en/stable/engine_details/development/compiling/optimizing_for_size.html
- [G21] C# basics / platform support: https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/index.html

Unity
- [U1] Changes to Unity plans and pricing (Runtime Fee cancelled, splash optional, 2026 price change): https://unity.com/products/pricing-updates
- [U2] Unity release/support dates (endoflife.date aggregator, used for version/date table only): https://endoflife.date/unity
- [U3] Editor command-line arguments (Unity 6.6 manual): https://docs.unity.com/en-us/engine/current/manual/unity-editor/command-line-arguments/editor
- [U4] Editor settings, Asset Serialization: https://docs.unity.com/en-us/engine/current/manual/unity-editor/editor-settings-reference/comp-manager-group/class-editor-manager
- [U5] 2D Pixel Perfect package manual: https://docs.unity3d.com/Packages/com.unity.2d.pixel-perfect@5.0/manual/index.html
- [U6] Manage your license through the command line: https://docs.unity.com/en-us/engine/6000.6/manual/get-started/install-and-upgrade/licenses-and-activation/managing-your-unity-license
- [U7] How Unity builds iOS applications: https://docs.unity.com/en-us/engine/current/manual/platform-specific/iphone/ios-introducing/how-unity-builds-ios-applications (and the macOS/Build Automation note in the iOS environment-setup docs: https://docs-alpha.unity3d.com/Manual/ios-environment-setup.html)
- [U8] Android dependencies (Unity 6.3 LTS): https://docs.unity3d.com/Manual/android-install-dependencies.html
- [U9] Tilemaps: https://docs.unity.com/en-us/engine/current/manual/unity2d/tilemaps
- [U10] ScriptableObject: https://docs.unity.com/en-us/engine/current/manual/scripting/get-started/fundamental-unity-types/class-scriptable-object
- [U11] Test Framework command-line reference: https://docs.unity.com/en-us/engine/6000.6/manual/programming-environment/test-framework-introduction/reference-command-line
- [U12] Unity Personal: https://unity.com/products/unity-personal
- [U13] iOS requirements and compatibility: https://docs.unity.com/en-us/engine/6000.6/manual/platform-specific/iphone/ios-introducing/ios-requirements-and-compatibility

Defold
- [D1] Defold blog (release posts): https://defold.com/blog
- [D2] Defold License: https://defold.com/license/
- [D3] Defold product page (text files, build-size comparison; vendor-published): https://defold.com/product/
- [D4] Android manual: https://defold.com/manuals/android/
- [D5] Bob the builder manual: https://defold.com/manuals/bob/
- [D6] Tile map manual: https://defold.com/manuals/tilemap/
- [D7] iOS manual: https://defold.com/manuals/ios/
- [D8] Texture filtering manual: https://defold.com/manuals/texture-filtering/
- [D9] Project settings manual: https://defold.com/manuals/project-settings/
- [D10] defold/defold repository: https://github.com/defold/defold
- [D11] Defold Asset Portal: https://defold.com/assets/
- [D12] Automated testing manual: https://defold.com/manuals/automated-testing/
- [D13] Native extensions manual (cloud build server): https://defold.com/manuals/extensions/

libGDX
- [L1] libGDX news index: https://libgdx.com/news/all ; 1.14.1 release notes: https://libgdx.com/news/2026/05/gdx-1-14-1
- [L2] libgdx/libgdx repository (Apache 2.0, platforms, stars): https://github.com/libgdx/libgdx
- [L3] Deploying your application: https://libgdx.com/wiki/deployment/deploying-your-application
- [L4] Tile maps: https://libgdx.com/wiki/graphics/2d/tile-maps
- [L5] Project setup (JDK 17/21, RoboVM plugin): https://libgdx.com/wiki/start/setup
- [L6] gdx-liftoff (Kotlin/KTX, iOS backend notes, targets 1.14.2): https://github.com/libgdx/gdx-liftoff
- [L7] MobiVM getting started (macOS + Xcode; Java 8/11 features): https://mobivm.github.io/dev/
- [L8] libGDX backends directory (incl. gdx-backend-headless, robovm, robovm-metalangle): https://github.com/libgdx/libgdx/tree/master/backends

Flame
- [F1] Flame docs: https://docs.flame-engine.org/latest/
- [F2] flame-engine/flame repository: https://github.com/flame-engine/flame

Platform / store
- [P1] Apple Developer Program enrolment (US$99/yr): https://developer.apple.com/programs/enroll/
- [P2] Google Play Console registration (US$25 one-time): https://support.google.com/googleplay/android-developer/answer/6112435
- [P3] Xcode: https://developer.apple.com/xcode/
