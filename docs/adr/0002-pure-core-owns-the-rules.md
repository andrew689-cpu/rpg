# A pure core owns every rule, including the overworld grid

Every game rule lives in `src/core/`: battle, catch %, spawn rolls, XP, Bond, Restoration, the clock, and also the overworld grid simulation (player, follower, NPC and wild-Creature movement on discrete ticks). The core is typed GDScript `RefCounted` classes with no `Node`, scene tree, `Input` or autoload access, and all randomness comes from an injected seeded `Rng`. Scenes only send intent through `GameSession` and play back the events it returns, interpolating sprites between cells.

This goes against the usual Godot style of logic in Node scripts and physics- or tween-driven movement, which would be quicker to make feel good. We chose the core because the game is built mostly by agents. Rules have to be testable headless through small interfaces; encounter, line-of-sight and shy-Creature rules must not hide in scenes; and determinism lets a battle be stored as setup + seed + actions. That record is what makes mid-battle resume (by replay) and exact bug-report replays possible.

## Consequences

- Lint rules fail CI if `src/core/` mentions `Node`, `get_tree`, `Input` or an autoload, or if anything outside the `Rng` wrapper calls `randf`, `randi` or `randomize`.
- Overworld feel (easing, bump and run animations) has to be built in presentation on top of cell-to-cell moves, rather than coming free from physics.
- Changing a battle rule can invalidate a stored `in_battle` replay. Resume then falls back to the pre-battle autosave.
