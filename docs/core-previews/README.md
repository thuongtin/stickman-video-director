# Core style previews

Motion previews for the core styles 1, 3 and 4. They are shown in every README's style section. Style 2's preview is its lead in [`../lead-character/`](../lead-character/).

| File | Style | Shot |
|---|---|---|
| `style-1-light.gif` | 1 Classic Minimalist, light | A cage of worry slams down on a black line figure; he grips two bars, bends them and breaks out as the red lock flies off |
| `style-1-dark.gif` | 1 Classic Minimalist, dark | A white line figure pushes a huge progress bar until it fills with electric blue, then cheers |
| `style-3.gif` | 3 Prehistoric dark comedy | In the cave, the chief offers a roast leg; the bored caveman lights up and takes it (a real hand-off: both hands on it, then the chief lets go) |
| `style-4.gif` | 4 Cozy storytelling | A quiet coffee at a sidewalk cafe table: reach for the mug, a sip with eyes closed, set it down, lean back |

Everything here is drawn with Pillow from 2D rigs (`rig2d.py`), one module per style (`style1.py`, `style3.py`, `style4.py`). No AI video or image model was used. Each character's joints are saved in `tracks/` and pass `tools/posture_gate/posture_gate.py check` with no errors or warnings; the Style 3 pair also passes `check --scene` for the hand-off (`tests/verify-core-previews.py`).

```bash
python3 docs/core-previews/render.py
```
