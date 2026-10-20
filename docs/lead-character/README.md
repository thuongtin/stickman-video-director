# Style 2 default lead

Nam is the default lead of Style 2 (Modern Pop): a very short dark buzz cut, thick dark rectangular glasses, an open red-and-navy plaid flannel shirt with rolled sleeves over a plain white tee, dark blue jeans and black stick limbs. The body (big round white head, short neck, boxy shirt, thin stick limbs, simple face) is the same as upstream's red-beanie lead; only the hair, glasses and clothes differ. Upstream's red-beanie Zeke stays available as the alternative lead; the skill uses it only when asked. The prompt anchors for both live in `skills/directing-stickman-videos/references/style-catalog.md`.

![Character sheet](sheet.png)

![Motion clip: a side-view walk, then a front-view wave and a push of the glasses](motion.gif)

Everything here is drawn by `render.py` (Pillow) from a 2D rig. No AI video or image model was used. Each pose and both shots of the clip are saved in `tracks/` and pass `tools/posture_gate/posture_gate.py check` with no errors and no warnings; `tests/verify-lead-character.py` re-checks them.

```bash
python3 docs/lead-character/render.py          # redraw sheet.png, motion.gif and tracks/
python3 tests/verify-lead-character.py         # gate every track
```

Notes on the look:

- The glasses stay on in every shot. When a beat touches them, the hand pushes them up and lets go.
- Light stubble is left out of the anchor, since at this size it reads as dirt. The sheet shows it as an option.
- In side view facing right, the character's own right arm and leg are drawn in front, as the posture gate expects.
