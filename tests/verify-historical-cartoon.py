#!/usr/bin/env python3
"""Style 5 (Historical Cartoon): source anchor, routing, motion-graphics wording, and a cast rig that passes the posture gate."""
import json
import re
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
skill = root / "skills/directing-stickman-videos"
ref = (skill / "references/historical-cartoon.md").read_text()
anchor = (
    "Polished 2D cel-shaded cartoon animation with thick clean black outlines and soft metallic shading. "
    "Stick-figure characters with smooth white filled round heads, simple black oval eyes, expressive brows and mouths, "
    "no nose, and thin black stick limbs, in the described costume. Exactly two arms and two legs, each shown only in its "
    "current pose. Clean, sunlit, painterly landscapes."
)
assert anchor in ref, "Preserve the contributor's complete drawing anchor"
for token in (
    "https://github.com/leksautomate", "/pull/41",
    "repeat its **full description**", "two visible non-color differences",
    "no style-specific character-count cap", "voice-continuity.md",
    "default when no other voice is requested", "opening/action/ending states",
    "Backgrounds are full-color", "do not rewrite Styles 1–4",
    "docs/style-5/", "posture_gate.py", "Hands at start",
):
    assert token in ref, token
# Motion graphics only: no AI video generator, prompt-box or text-to-video wording comes back with the port.
for path in [ref] + [(skill / f).read_text() for f in ("SKILL.md", "references/style-catalog.md")]:
    assert not re.search(r"omni flash|google flow|seedance|veo\b|text-to-video|provider|generation is authorized",
                         path, re.IGNORECASE)
for filename in (
    "SKILL.md", "references/style-catalog.md",
    "references/storyboard-template.md", "references/segment-spec-contract.md",
):
    assert "historical-cartoon.md" in (skill / filename).read_text(), filename
catalog = (skill / "references/style-catalog.md").read_text()
assert re.search(r"^\| Style 5 \| core \|", catalog, re.M), "Style 5 status row"
assert "Style 5: Historical Cartoon" in (skill / "references/storyboard-template.md").read_text() or \
    "- Style 5:" in (skill / "references/storyboard-template.md").read_text()
assert "Styles 1–5" in (skill / "references/core-contract.md").read_text()

# The code-rendered cast: sheet, motion clip and gated tracks.
style5 = root / "docs/style-5"
for name in ("render.py", "sheet.png", "motion.gif", "README.md"):
    assert (style5 / name).is_file(), f"missing docs/style-5/{name}"
assert (style5 / "motion.gif").stat().st_size < 1_200_000, "motion.gif too large for the README"
gate = root / "tools/posture_gate/posture_gate.py"
tracks = sorted((style5 / "tracks").glob("*.json"))
assert {"shot1_roman_walk", "shot2_edo_wave"} <= {t.stem for t in tracks}
assert len([t for t in tracks if t.stem.startswith("pose_")]) >= 6
casts = set()
for t in tracks:
    data = json.loads(t.read_text())
    assert data["profile"] == "rig" and data.get("limb_width") and data.get("body_width"), t.name
    casts.add(data["cast"])
    out = subprocess.run([sys.executable, str(gate), "check", "--json", str(t)], capture_output=True, text=True)
    clip = json.loads(out.stdout)["clips"][0]
    assert out.returncode == 0 and clip["errors"] == 0 and clip["warnings"] == 0, \
        f"{t.name}: {[i['message'] for i in clip['issues']]}"
assert casts == {"soldier", "citizen", "student", "attendant"}, casts
print(f"Style 5: anchor, routing and motion-graphics wording passed; {len(tracks)} cast tracks pass the posture gate.")
