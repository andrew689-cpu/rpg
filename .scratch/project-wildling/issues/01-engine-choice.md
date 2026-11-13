# Which 2D engine fits an agent-built pixel-art game for Android + iOS?

Type: research
Status: resolved
Blocked by: none

## Question

Compare Godot 4, Unity (2D), Kotlin/libGDX, and Defold (plus any strong alternative found) for Project Wildling: a 2D pixel-art, tile-map, turn-based RPG built mostly by AI agents, exported to Android and iOS, free hobby release.

Criteria: Android + iOS export maturity and requirements (e.g. macOS/Xcode for iOS), pixel-perfect rendering & tile-map support, data-driven content (JSON/resources), text-based project files that agents can edit and diff, headless/CLI testability, licensing & cost (incl. fees at $0 revenue), APK/IPA size, community/asset ecosystem, and ability to scale to Large content (150+ Creatures, multiple regions).

## Answer

Findings: branch `research/engine-choice`, file `research/engine-choice.md` (official docs, licences and release notes as of 2026-11-13).

**Recommendation: Godot 4.7.x stable, typed GDScript only.** Defold is the runner-up.

- **Godot wins on:** MIT licence with $0 fees; text scene and resource files that agents can edit and diff; typed Resources or JSON for content; a full CLI (import, export, headless) with no login; GUT / gdUnit4 for tests; built-in pixel-perfect scaling and TileMap autotiling; the largest community and asset library.
- **Costs and caveats:** C# on mobile is still experimental, so use GDScript only. The base export is about 25 MB (Defold is about 2.5 MB). Headless test runs can exit 0 even when scripts failed (reproduced up to 4.7.2), so CI must parse results and logs. Agents must keep `.uid` sidecar files with their scripts when moving them.
- **Defold:** free, text-based, CLI, tiny builds. But it has a small ecosystem, uses Lua, and has no documented autotiling.
- **Unity: rejected.** The Personal licence can't be activated from the CLI (it needs a Hub login), and its YAML scenes are linked by fileIDs that agents can't safely write.
- **libGDX: rejected.** iOS depends on MobiVM/RoboVM (Java 8/11 limits), and there's no editor besides Tiled.
- **All engines:** iOS builds need a Mac with Xcode.
- **Follow-ups the research raised:** a Creature data-structure sketch, a CI recipe, and version-pinning and `.uid` rules for agent instructions. These feed **What is the technical architecture?**
