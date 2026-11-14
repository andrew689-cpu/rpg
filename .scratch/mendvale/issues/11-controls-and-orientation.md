# How does the game feel on a touchscreen?

Type: prototype
Status: resolved
Blocked by: 01

## Question

Portrait or landscape? Virtual D-pad, tap-to-move, or swipe? How do menus and battle commands map to touch? Gamepad support? Decide by making a rough playable control stub in the chosen engine.

Added from ticket 07 (How does a battle work?): also decide the **battle screen layout** for 1v1 and 2v2 in the chosen orientation. That covers where the HP and Energy bars, Status countdowns, stat-stage arrows, turn-order indicator, damage preview (% of HP plus effectiveness) and Trait sit, the Fight / Catch / Team / Run command layout, the move list (Energy cost, Power/Focus icon, accuracy), and tap-to-target in 2v2.

## Answer

Resolved with the human (2026-11-13) by playing the prototype:
- Artifact: https://claude.ai/artifact/X4zuWpD2Ddb7Y7J1cXPpc2
- Code: branch `prototype/controls`, folder `prototypes/controls/`, never merged.

Also covers the battle screen layout moved here from ticket 07.

### Orientation and input
- **Portrait first.** Screen layouts are data, so landscape can be added later without a rewrite.
- **Movement:**
  - Default: **floating D-pad plus tap-to-move** together. Tap-to-move works anywhere on the map, and tapping an NPC or sign walks you to it and interacts.
  - Option: a **fixed pad**.
  - **Swipe-and-hold is dropped.**
- Grid movement; a quick press only turns you. **Run is on by default**, with a toggle.
- **The pad hides in battles and menus**, where you tap buttons directly.
- **Left-handed mirroring** at launch (a layout setting).
- **Gamepad and keyboard** work as secondary input in version 1. Every input reduces to **five actions**: `move(dir)`, `walkTo(tile)`, `confirm`, `back`, `menu`, which map to Godot input actions. Every menu has a focus cursor with direction-based navigation.
- **Battle text** advances on tap, with a fast auto-advance setting.

### Overworld screen
- The **map** fills the top ~60%.
- The **control deck** fills the bottom ~40%: the floating pad zone, **A (interact)** and **B (back)** on the main-thumb side, and a small **Menu** button.
- **Dialogue boxes** cover the bottom of the map, just above the deck.
- The layout respects notches and gesture bars.
- No page scrolling or zooming on the game surface.

### Battle screen (top to bottom)
1. **Info strip:** for each side, name, level, HP bar, Energy bar, Status with its countdown, stat-stage arrows and a Trait icon, plus the **turn-order indicator** (small portraits in order).
2. **Scene:** an Area-drawn backdrop, the foe's front sprite and the player's back sprite (64×64).
3. **Message line.**
4. **Command deck** (same area as the overworld controls):
   - A **thumb arc** on the main-thumb side, in order: **Fight** (under the thumb), **Catch** (shows the catch %), **Team**, **Run** (furthest). A simple list is available as a setting, and left-handed mode mirrors it.
   - **Move list:** 4 moves plus the Basic move, each showing name, Energy cost, Power/Focus icon, type colour and accuracy. Moves you can't afford are greyed out.
   - **Tap a move once to preview it** on the target (damage as % of HP, effectiveness, any status chance) and **tap again to confirm**. A "one-tap moves" setting skips the preview. Tapping elsewhere cancels.
- **2v2:** two foes side by side at the top, the player's two at the bottom, and the info strip grows to two rows. Actions are chosen for each Creature in turn (the active one is highlighted). After picking a move, **tap a foe sprite** to target it; valid targets glow, and a single valid target is picked automatically.

### Menu
- Team / Bag / Save. An "Autosaved" notice appears after battles and Area changes.
