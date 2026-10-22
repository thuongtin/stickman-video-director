# Core style previews

Motion previews for the core styles 1, 3 and 4. They are shown in every README's style section. Style 2's preview is its lead in [`../lead-character/`](../lead-character/).

| File | Style | Shot |
|---|---|---|
| `style-1-light.gif` | 1 Classic Minimalist, light | A black line figure walks in and raises a hand; a gold idea bulb lights up |
| `style-1-dark.gif` | 1 Classic Minimalist, dark | A white line figure jumps for joy in a blue and red burst |
| `style-3.gif` | 3 Prehistoric dark comedy | A caveman in a hide tunic walks to a campfire and warms his hands |
| `style-4.gif` | 4 Cozy storytelling | A tracking walk through a park with a coffee cup, then a wave outside a cafe (the cup stays in the right hand) |

Everything here is drawn by `render.py` (Pillow) from 2D rigs. The joints come from the Style 2 lead's rig and only the drawing changes per style. No AI video or image model was used. Each shot's joints are saved in `tracks/` and pass `tools/posture_gate/posture_gate.py check` with no errors or warnings (`tests/verify-core-previews.py`).

```bash
python3 docs/core-previews/render.py
```
