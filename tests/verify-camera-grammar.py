#!/usr/bin/env python3
"""Camera grammar regression: the template states the rules and the example storyboard follows them.

This reads the `Motion, camera, and transition` column only; it does not judge rendered footage.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/directing-stickman-videos"
TEMPLATE = SKILL / "references/storyboard-template.md"
EXAMPLES = SKILL / "references/examples.md"
sys.path.insert(0, str(ROOT / "tools/package_lint"))
from package_lint import ACCENT, INWARD  # noqa: E402



def camera_cells(text):
    """Camera column of the first storyboard table that has one."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not line.startswith("|") or "|---" not in (lines[i + 1] if i + 1 < len(lines) else ""):
            continue
        head = [c.strip() for c in line.strip("|").split("|")]
        col = next((k for k, h in enumerate(head) if "camera" in h.lower() or "镜头" in h), None)
        if col is None:
            continue
        cells = []
        for row in lines[i + 2:]:
            if not row.startswith("|"):
                break
            cells.append([c.strip() for c in row.strip("|").split("|")][col])
        return cells
    return []


def lint(cells):
    problems = []
    accents = [n for n, c in enumerate(cells, 1) if ACCENT.search(c)]
    if len(accents) * 3 > len(cells):
        problems.append(f"accent moves in clips {accents}, more than one third of {len(cells)} clips")
    inward = [bool(INWARD.search(c)) for c in cells]
    for k in range(2, len(cells)):
        if inward[k] and inward[k - 1] and inward[k - 2]:
            problems.append(f"clips {k - 1}-{k + 1} all push inward")
    return problems


template = TEMPLATE.read_text()
for phrase in ("## Camera grammar", "Transition moves", "Accent moves", "Hold the camera when the picture already moves by itself",
               "no more than one third of the clips", "three consecutive clips", "huashu-art-motion (MIT"):
    assert phrase in template, f"storyboard-template.md lost camera rule: {phrase}"
assert "camera push, pull, pan, orbit, shake" not in template, "device list still invites shake/orbit as a routine device"
assert "camera grammar" in (SKILL / "SKILL.md").read_text(), "SKILL.md does not point to the camera grammar"

cells = camera_cells(EXAMPLES.read_text())
assert len(cells) == 6, f"expected the six-row example storyboard, found {len(cells)}"
assert not lint(cells), "examples.md breaks camera grammar: " + "; ".join(lint(cells))

# The lint must actually fail on bad tables.
assert lint(["slow push-in", "push in on the cup", "zoom in on the door"]), "three inward pushes not caught"
assert lint(["fast push-in", "whip pan", "hold", "slam zoom", "camera orbits the hero", "pull back"]), "accent overuse not caught"
assert not lint(["slow push-in", "pull back", "lateral track", "fast push-in", "hold", "pull back"]), "good table rejected"

print("camera grammar: PASS")
