# Which content and save fields are still missing?

Type: grilling
Status: open
Blocked by: none

## Question

Close the data gaps `spec.md` §7 lists, so the JSON Schemas and the save format can be written (see `spec.md` §6):
- **Rematches:** the save field that tracks whether each Boss rematch is ready again (once per in-game day).
- **Economy balance check:** each Boss's target shopping list (what the player should be able to afford by then).
- **Events:** the complete closed command list with each command's parameters. Ticket 09 lists `say`, `choice`, `set_flag`, `if_flag`, `give_item`, `give_creature`, `battle`, `move_actor`, `wait`, `heal` and ends with "…".
- **Placeholders:** whether a missing sprite (the built-in placeholder) fails the production no-placeholder gate.
- **Boss forfeits:** whether a Boss battle can be forfeited like a trainer battle.
