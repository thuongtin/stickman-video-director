#!/usr/bin/env python3
"""Motion previews for the core styles 1, 3 and 4, drawn from code rigs (Style 2 has its own lead in docs/lead-character/).

Writes, next to this file:
  style-1-light.gif   Classic Minimalist, light: a cage of worry slams down; the figure bends the bars and breaks out
  style-1-dark.gif    Classic Minimalist, dark: the figure pushes a huge progress bar until it fills with electric blue
  style-3.gif         Prehistoric dark comedy: in the cave, the chief offers a roast leg and the caveman takes it
  style-4.gif         Cozy storytelling: a quiet coffee at a sidewalk cafe table, in a soft painted street
  tracks/*.json       every character's joints, frame by frame (tests/verify-core-previews.py gates them)

The rig and drawing kit is rig2d.py; each style has its own module. Pillow is the only dependency.
Nothing here is AI-generated: every frame is drawn from the joints in tracks/.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import style1  # noqa: E402
import style3  # noqa: E402
import style4  # noqa: E402


def main():
    out = HERE / "tracks"; out.mkdir(exist_ok=True)
    for mod in (style1, style3, style4):
        for t in mod.render(HERE):
            (out / f"{t['name']}.json").write_text(json.dumps(t, indent=1))


if __name__ == "__main__":
    main()
