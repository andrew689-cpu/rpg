# Spawn entries live with the line, not the Area

A species' wild spawn entries (Area, stages, form, Rarity tier, levels, Habitat, times, weather) are written in its evolution **line record**, `content/lines/<line_id>.json`. They are not written in the Area's spawn tables. `tools/bake_content` groups every line's entries into the per-Area × stage spawn tables the game reads, so the runtime shape is unchanged. The Area JSON keeps only what is the Area's own: its `native_species` list, weather table, music and shop stock. The linter checks that each native species has a Common or Uncommon entry in that Area.

The alternative was the obvious one: spawn tables in the Area files, edited by whoever adds a species. We rejected it because the roster is built as 34 line-sized slices, often in parallel by different agents, and almost every line places Creatures in several Areas. With tables in the Area files, nearly every line PR would edit shared files and conflict with every other. A line's placement would also be scattered across many files, away from the design sheet that justifies it. Keeping the entries with the line makes a line PR touch only its own files.

## Consequences

- An Area's assembled mix can't be read from any one source file, so `tools/area_sheet` renders it per Area × stage for review. Balance checks across lines (Common species counts, the counter rule, at most 2 wild starters per Area, Chapter 1's two most Common species) run in the linter on the assembled tables.
- Payoff Creatures and the rare one-offs' set encounters are not spawn entries, so they stay with the Area and the world data.
- Spawn state is still never saved, so moving where entries are authored never touches the save format.
