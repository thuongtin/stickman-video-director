#!/usr/bin/env python3
"""The Style 2 default lead's sheet and motion clip are drawn from rig tracks that pass the posture gate cleanly."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAD = ROOT / "docs/lead-character"
GATE = ROOT / "tools/posture_gate/posture_gate.py"

for name in ("render.py", "sheet.png", "motion.gif", "README.md"):
    assert (LEAD / name).is_file(), f"missing docs/lead-character/{name}"
assert (LEAD / "motion.gif").stat().st_size < 1_200_000, "motion.gif too large for the README"

tracks = sorted((LEAD / "tracks").glob("*.json"))
names = {t.stem for t in tracks}
assert {"shot1_walk", "shot2_wave_glasses"} <= names, names
assert len([n for n in names if n.startswith("pose_")]) >= 6, "every sheet pose has its own track"

for t in tracks:
    data = json.loads(t.read_text())
    assert data["profile"] == "rig" and data.get("body_width") and data.get("limb_width"), f"{t.name}: rig figure sizes"
    out = subprocess.run([sys.executable, str(GATE), "check", "--json", str(t)], capture_output=True, text=True)
    result = json.loads(out.stdout)
    clip = result["clips"][0]
    assert out.returncode == 0 and clip["errors"] == 0 and clip["warnings"] == 0, \
        f"{t.name}: {[i['message'] for i in clip['issues']]}"

# the glasses push is the only planned face cover, and the pen stays in the right hand
wave = json.loads((LEAD / "tracks/shot2_wave_glasses.json").read_text())
assert any(f.get("face_cover") for f in wave["frames"])
pen = json.loads((LEAD / "tracks/pose_light_pen.json").read_text())
assert pen["frames"][0]["holds"] == {"pen": "r"}
print(f"Lead character: {len(tracks)} rig tracks pass the posture gate with no warnings.")
