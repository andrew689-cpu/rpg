# Which settings and accessibility options ship in v1?

Type: grilling
Status: open
Blocked by: none

## Question

Finish the settings and accessibility design (see `spec.md` §5 and §6):
- **Colour-blind support:** Type colours need icons or labels as well. Decide which screens show which, and whether there are colour-blind palettes, given the locked 53-colour palette.
- **Large text:** whether there is a large-text mode, how it works with integer scaling at 180 px wide, and which screens must reflow.
- **Localisation:** English-only in v1 is fixed. Decide what v1 must do so a later language is only strings: string length budgets, `tr()` keys, and font coverage (Public Pixel covers 98 languages, Tiny5 fewer).
- **The settings list:** confirm defaults for the settings already named (movement scheme, left-handed mirroring, Run, follower, battle text auto-advance, one-tap moves, battle command layout, battle animations), and add audio volumes, haptics, text speed and any others.
