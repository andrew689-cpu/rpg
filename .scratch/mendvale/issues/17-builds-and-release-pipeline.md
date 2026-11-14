# How are Mendvale's Android and iOS builds made and released?

Type: grilling
Status: resolved
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

Added from ticket 15 (How do the Bosses and Area gating sequence the region?): the content tests include a **Boss 1 simulation gate**: 200 seeded headless battles for every starter in every trio, up to 15 starters (3,000 battles), which fail the build below a 70% win rate. The linter also walks the Area graph to check gating. Both run on the pure core and should be cheap, but they belong in the CI time budget.

Added from ticket 16 (How is the Creature roster structured?): the licence ledger gets a `placeholder` column. Internal and closed-testing exports allow placeholder Creature sprites, but a **production** export must fail if any reachable species still uses a placeholder. The linter also gains roster checks (counts, bands, a name blocklist) that run in the same content gate.

## Answer

Resolved by grilling with the human (2026-11-14). Builds on ticket 01 (Godot 4.7.x), ticket 04 (store rules), ticket 06 (app ID) and ticket 09 (bake, linter, test layers, debug menu). Facts were checked against primary sources on 2026-11-14 (GitHub runner docs and image readmes, Apple's upcoming-requirements page, Godot 4.7.2-stable source, Play Developer API docs). Terms are defined in `GLOSSARY.md`: **Build channel**, **Vertical slice**.

### CI: GitHub Actions
- The repo (`andrew689-cpu/rpg`) is **public**, so standard GitHub-hosted runners, macOS included, are **free and unlimited**. At most 5 macOS jobs run at once on the Free plan; larger runners are never used.
- **`check` workflow**, on every PR and every push to `main`, on `ubuntu-latest`:
  1. `bake_content` with the full linter (Area-graph gating, map markers, roster checks).
  2. The Boss 1 simulation gate (ticket 15) and the three gdUnit4 layers (ticket 09).
  3. Gate on the gdUnit4 JUnit XML plus a log scan for `SCRIPT ERROR`, **never on Godot's exit code**. *Added by ticket 20:* the `--import` step also gets the three import gates in ticket 09's Maps section: committed `.import` sidecars with no `valid=false`, a scan for `Error importing` and `Import finished with`, and no map scene with embedded `Image` data.
  - Time budget: **10 minutes**. The job prints its slowest gates so a creeping gate is noticed.
- **On pushes to `main` only** (not PRs), two extra jobs:
  - a **debug APK** (Godot's debug keystore, debug menu included) kept as a workflow artifact for **14 days**, for sideloading onto the human's Android phone;
  - an **unsigned iOS build** on `macos-26` (`xcodebuild build` with `CODE_SIGNING_ALLOWED=NO`), so the iOS path can't rot before the Apple membership exists.
- **`release` workflow**, on a `v*` tag: checks the tag's commit is on `main`, runs `check`, then builds, signs and uploads both platforms (below). Signing secrets live in a GitHub **`release` environment** that only this workflow uses; fork PRs never see secrets.
- **Who releases:** only the human pushes version tags. A GitHub **tag ruleset** limits creating `v*` tags to repo admins; agents work through PRs. The ruleset is the guard, so the environment needs no extra approval click.

### Build channels and versions
- Three **Build channels**:
  - **debug**: debug menu and named fixture saves; from `main` pushes and local runs only, never from a tag.
  - **test**: a release export that may use placeholder Creature sprites. Tag **`vX.Y.Z-beta.N`**. Everything before launch is a beta, starting at `v0.1.0-beta.1`.
  - **production**: tag **`vX.Y.Z`**. Must pass the no-placeholder gate from ticket 16 (licence ledger `placeholder` column; fails if any reachable species uses one).
  - The debug menu and fixture saves are left out of test and production exports by Godot feature tags.
- **`version_name`**: the tag without the `v` on Android (`0.4.0-beta.2`). On iOS, `CFBundleShortVersionString` is the bare `X.Y.Z`, since Apple rejects suffixes.
- **`version_code`** (Android) and **`CFBundleVersion`** (iOS) are the same integer: **`X·1,000,000 + Y·10,000 + Z·100 + B`**, where B is the beta number (1–98) and **99** for the production build. So `0.4.0-beta.2` → 40,002 and `1.0.0` → 1,000,099. It always increases and a beta sorts before its release; nothing is stored. Limits: Y, Z ≤ 99 and at most 98 betas per version. The release workflow refuses a tag that breaks them, or one whose code isn't higher than the last uploaded build.
- **The save `version` is independent** of the app version: a plain integer bumped only when the save's shape changes, and every bump ships with a migration and a migration test (ticket 09). Content IDs are permanent, so content changes never need a migration.
- **The content bundle has no version of its own.** The bake stamps it with the app version and git commit, for bug reports only.
- **Downgrades are refused:** a save whose `version` is newer than the app understands shows a message and isn't loaded or overwritten.

### Android
- Export **AAB**, which in Godot 4.7 requires **Use Gradle Build**. CI installs the Android build template fresh each build; `android/build/` is gitignored, since there are no Java plugins.
- Toolchain as Godot 4.7.2 expects (from its source; the 4.7 docs page is out of date): **Java 17, compile and target SDK 36, build-tools 36.1.0, NDK 29**, set up with `setup-java` and `sdkmanager`.
- **Min SDK 24** (Godot's default). **arm64-v8a only** (Godot's default; Play requires 64-bit). **16 KB page size** is built in since Godot 4.5.
- **Play App Signing:** Google holds the app signing key. One **upload keystore** is generated once and kept in the `release` environment secrets (base64 keystore, alias, passwords), with an offline backup in the human's password manager. A lost upload key can be reset in Play Console.
- `export_presets.cfg` is committed. Godot keeps secret fields (keystore path, user, password) in `.godot/export_credentials.cfg`, which is never committed; CI supplies them through Godot's `GODOT_ANDROID_KEYSTORE_RELEASE_*` env vars.
- **Upload:** every tag, beta or production, uploads its AAB to the **Play internal track** through the Play Developer Publishing API, using `r0adkll/upload-google-play` pinned to a commit SHA and a service-account JSON secret. The AAB is also kept as a workflow artifact.
- **Promotion is manual** in Play Console: internal → closed testing → production. Only production builds are ever promoted to production. The first closed test (≥12 testers for 14 days on a new personal account, ticket 04) starts from a beta of the **vertical slice**.

### iOS
- **Store order:** Android goes first. The iOS pipeline is written and tested from day one (the unsigned `main` build above), but the **$99/yr Apple membership is bought at the vertical slice**, when there is something for TestFlight. Both stores launch together.
- **Built in CI** on a pinned **`macos-26`** runner, with an explicit `xcode-select` to **Xcode 26.6**. Apple has required Xcode 26 and the iOS 26 SDK for uploads since 2026-04-28.
- **Godot exports the Xcode project only** (`application/export_project_only=true`). Our own script then runs `xcodebuild archive` and `xcodebuild -exportArchive -allowProvisioningUpdates` with the `-authenticationKey*` flags and `destination=upload` in the export-options plist. That **signs in Apple's cloud with an App Store Connect API key** and uploads to TestFlight in one step.
  - Why not Godot's own `.ipa` export: it runs `xcodebuild` itself but never passes an API key, so CI would need a certificate and profile in a temporary keychain. Its env-var names also differ from the docs (`GODOT_APPLE_PLATFORM_PROVISIONING_PROFILE_UUID_*`), and in 4.7.2 the release one reads the debug variable.
  - The API key (issuer ID, key ID, `.p8`) lives in the `release` environment. Apple forum reports say cloud signing needs an **Admin**-role key; confirm this when the key is created. *Confirmed 2026-11-14 by ticket 27 ("What exactly do Google Play and Apple require of Mendvale's accounts and rating?"): use an Admin-role team key. Individual keys can't use the provisioning endpoints.*
  - The team ID and signing identity aren't secret and stay in `export_presets.cfg`.
- **Minimum iOS 15.0** (Godot's default), which already meets Apple's April 2027 floor.
- **Upload:** every tag goes to **TestFlight** for internal testers. Submitting for App Store review is **manual** in App Store Connect.
- **The human's Mac** installs full Xcode only for debugging on their iPhone: a free personal team before the membership (7-day provisioning), then test builds through TestFlight, with debug builds still going through Xcode.
- **Test devices:** one Android phone and one iPhone. Each Godot upgrade and each release candidate is installed on both.

### Godot in CI
- **`.godot-version`** at the repo root (`4.7.2-stable`) is the single pin, read by CI and the local setup notes.
- **`tools/ci/install_godot.sh`** (our own script, no third-party setup action in workflows that hold signing secrets) downloads the official Linux x86_64 editor from the `godotengine/godot` GitHub release, checks it against the published `SHA512-SUMS.txt`, and caches it by version. Only export jobs fetch the ~1.28 GB export templates, cached the same way.
- **`.godot/` import cache** is keyed on the Godot version plus a hash of `assets/` and `content/`. CI runs `godot --headless --import` with multi-threaded import off (ticket 19).
- **Third-party actions** are pinned to a commit SHA, and Dependabot proposes updates.
- A GitHub Release with auto-generated notes is created for each tag; no binaries are attached.

### Upgrades and store rules
- **Upgrades are deliberate:** a Godot upgrade is a PR that bumps `.godot-version`, passes `check`, and has a test build installed on both phones. Patch releases are taken when they fix something we hit; minor versions (4.8+) only when a store rule needs them. Xcode is bumped the same way.
- **Annual July check:** a recurring issue reviews store rules ahead of Play's 31 August target-SDK deadline and Apple's April SDK deadline. The first one moves to **Xcode 27 and the iOS 27 SDK before April 2027**.

### Build size
- **Official export templates in v1, no custom template.** Godot 4.7.2's arm64 Android engine library is about 24 MB compressed (71 MB installed, since 16 KB alignment keeps native libraries uncompressed), so a pixel-art game should download at roughly 25 MB plus assets.
- Each release job **reports the AAB size and the estimated per-device download**, and **fails above 150 MB**, leaving headroom under Play's 200 MB base-module limit.
- A custom template (`disable_3d`, `optimize=size`; about 15% smaller per Godot's docs) becomes a separate task only if the report shows more than **60 MB** to download.

### One-time setup (the human's steps, in order)
Listed here; doing them is implementation work, a HITL checklist (a `wizard` script) once the pipeline code exists:
1. Create the GitHub `release` environment and the `v*` tag ruleset (admins only).
2. Generate the Android upload keystore; store it in the `release` environment and back it up in the password manager.
3. Register the Play developer account ($25), create the app (`io.github.andrew689cpu.mendvale`), and **upload the first AAB by hand** from a release run's artifacts. The Publishing API can't create an app or make the first upload.
4. Create a Google Cloud service account, enable the Play Developer API, invite the service account in Play Console (Users & permissions), and store its JSON in the `release` environment.
5. Install full Xcode on the Mac.
6. At the vertical slice: buy the Apple Developer membership ($99/yr), create the App Store Connect app, create an API key (check the role needed for cloud signing), and store it in the `release` environment.

Store listings, privacy-policy hosting, recruiting testers, the trader declaration and filling the licence ledger stay in the map's Quality & release fog.
