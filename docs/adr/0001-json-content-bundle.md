# Content is JSON baked into one bundle, not Godot Resources

All game content (species, moves, Traits, items, Areas, spawn tables, trainers, events) is written as one JSON file per record, cross-referenced by permanent string IDs. A headless `tools/bake_content` step lints it and bakes it into a single `content.bundle.json`, which is the only content the game reads.

Godot's default would be typed `.tres` Resources. We rejected them because most content is written by agents by hand: `.tres` files cross-reference by `ext_resource` path and uid, which is fragile to hand-write. JSON can be diffed, validated against a schema, and checked inside or outside Godot.

The bake doubles as the build gate: a lint error fails the build, so broken content can't ship. It also avoids opening about 1,000 small files on phone startup.

## Consequences

- Nothing typed exists until load time. `ContentDB` turns the bundle into typed GDScript classes, and the JSON Schemas plus the linter do the job the inspector would have done.
- Content isn't editable in the Godot inspector. Maps are the exception: they stay Godot `TileMapLayer` scenes, reached through the `AreaGrid` seam.
- IDs are permanent once released. A rename goes through `content/aliases.json`, never an edit of the ID.
