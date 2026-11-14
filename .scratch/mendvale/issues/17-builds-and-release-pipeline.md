# How are Mendvale's Android and iOS builds made and released?

Type: grilling
Status: open
Blocked by: 09

## Question

Specify the build and release pipeline for the architecture in ticket 09 ("What is the technical architecture?"):
- **CI provider and triggers:** where the content bake, tests and exports run (e.g. GitHub Actions), on which events (every PR, main, tags), and what it costs at $0 (macOS runner minutes, public vs private repo).
- **iOS builds:** which Mac builds and signs them (the human's own Mac, a CI macOS runner, or both), Xcode version pinning, certificates and provisioning profiles, and where signing secrets live.
- **Android builds:** AAB export, target API 36, 16 KB page support, keystore and Play App Signing, and where the upload key lives.
- **Godot in CI:** pinning the 4.7.x editor and export templates, caching the `.godot/` import, and the gates from ticket 09 (bake must pass; gdUnit4 JUnit XML plus a `SCRIPT ERROR` log scan, never the exit code).
- **Versioning:** how `version_name` and `version_code` / build numbers are set, and how they relate to the save `version` and content bundle.
- **Release tracks:** Play internal → closed testing (≥12 testers for 14 days for a new personal account) → production; TestFlight → App Store. What gets promoted when, and what is manual.
- **Build size:** whether to use a custom export template (strip debug symbols, disable 3D) to cut the ~25 MB engine overhead.

Already fixed:
- Ticket 01: Godot 4.7.x, typed GDScript; headless exit codes can't be trusted; iOS needs a Mac with Xcode.
- Ticket 04: Play $25 one-off and Apple $99/yr; API 36, AAB and 16 KB pages; no bundled analytics.
- Ticket 06: app ID `io.github.andrew689cpu.mendvale` on both stores.
- Ticket 09: one baked `content.bundle.json` with the linter as the build gate; gdUnit4 with three test layers; a dev-only debug menu stripped from release exports by a feature tag.

Store listings, privacy-policy hosting, recruiting testers and the trader declaration stay in the map's Quality & release fog.
