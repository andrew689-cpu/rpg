# What are the starting values for the untuned numbers?

Type: grilling
Status: open
Blocked by: none

## Question

Give a starting value to every tuning number that no ticket has set (listed in `spec.md` §7, "Tuning gaps"), so each module can be built and tested against real numbers:
- **Statuses:** countdown length for each of the 6, Poison's damage and how it ramps, how much Burn lowers Power.
- **XP:** the XP curve to level 66, and the constants of the level-gap split.
- **Catching:** how the catch % factors combine (HP curve, Status bonus, level factor, Lure tier).
- **World:** the respawn delay for wild Creatures, the stage-swap ring width, and the tick rate and clock speed if not already set.
- **Moves:** the `signature` tier's power, cost and accuracy band, and the band lint tolerance.
- **AI:** what challenge mode's fourth Boss AI tier does differently.
- **Misc:** the nickname length limit.
