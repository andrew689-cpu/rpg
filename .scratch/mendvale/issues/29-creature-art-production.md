# Who draws the Creatures, and how is each sprite made and reviewed?

Type: grilling
Status: open
Blocked by: none

## Question

Decide how Mendvale's 100 species get their final art (see `spec.md` §5 and the answers to tickets 02, 10 and 16):
- **Who draws:** the human, a volunteer, a later commission, or a mix, and what happens to the plan if no one can draw all 100.
- **Tools:** LibreSprite, Pixelorama or Aseprite, the palette file, and the export settings for the 64×64 front and back battle sprites and the 16×16 map sheet (4 directions × 2 frames).
- **The per-sprite workflow:** concept, silhouette, palette, export, then drop into `assets/creatures/<id>/`. Whether AI concept art is used as a base that gets substantially redrawn (ticket 02), and how that is recorded in the licence ledger.
- **Review:** the human's review step, the linter's palette and size checks, and how a sprite moves from placeholder to final (the `placeholder` column).
- **Pace:** the vertical slice first (T1 plus the Chapter 1 lines), then each form in the order players first see it.
