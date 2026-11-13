# How do catching, the party, and storage work?

Type: grilling
Status: open
Blocked by: 05

## Question

Specify how wild Creatures are encountered and caught (capture tool, success chance inputs, failure outcomes), party size, storage for the rest, nicknaming, releasing, duplicate handling, and the collection log ("dex"-style registry; name it originally).

Constraints from ticket 05 (core loop & pillars): encounters are driven by **Habitat**, **Time of day**, weather and the Area's **Restoration stage** (in-game clock, rest to skip; nothing permanently missable). Registering an Area's native Creatures in the collection log is one of the actions that advances its Restoration (rules in ticket 12).

Constraints from ticket 07 (How does a battle work?): a caught Creature's **Trait** is fixed at the catch by the Habitat, time of day and weather, and is **shown on the encounter screen before throwing**. Wild battles are always 1v1, and fleeing them always works. HP persists between battles; Rest points heal.
