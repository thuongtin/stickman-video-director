#!/usr/bin/env python3
"""The Style 1, 3 and 4 previews are drawn from rig tracks that pass the posture gate, and every README shows them."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "docs/core-previews"
GATE = ROOT / "tools/posture_gate/posture_gate.py"
GIFS = ("style-1-light.gif", "style-1-dark.gif", "style-3.gif", "style-4.gif")

for name in GIFS:
    data = (HERE / name).read_bytes()
    assert data[:6] in (b"GIF87a", b"GIF89a") and len(data) < 2_500_000, (name, "missing or too large")
    assert int.from_bytes(data[6:8], "little") == 640 and int.from_bytes(data[8:10], "little") == 360, (name, "640x360")

tracks = sorted((HERE / "tracks").glob("*.json"))
assert {t.stem for t in tracks} == {"style1_light_cage", "style1_dark_progress", "style3_caveman", "style3_chief", "style4_cafe"}
for t in tracks:
    data = json.loads(t.read_text())
    assert data["profile"] == "rig" and data.get("body_width") and data.get("limb_width"), f"{t.name}: rig figure sizes"
    out = subprocess.run([sys.executable, str(GATE), "check", "--json", str(t)], capture_output=True, text=True)
    clip = json.loads(out.stdout)["clips"][0]
    assert out.returncode == 0 and clip["errors"] == 0 and clip["warnings"] == 0, \
        f"{t.name}: {[i['message'] for i in clip['issues']]}"

# Style 3: the roast leg passes from the chief's hand to the caveman's (both hold it, then the chief lets go)
scene = subprocess.run([sys.executable, str(GATE), "check", "--scene", str(HERE / "tracks/style3_caveman.json"),
                        str(HERE / "tracks/style3_chief.json")], capture_output=True, text=True)
assert scene.returncode == 0, scene.stdout[-400:]
cave = json.loads((HERE / "tracks/style3_caveman.json").read_text())["frames"]
chief = json.loads((HERE / "tracks/style3_chief.json").read_text())["frames"]
both = [i for i, (a, b) in enumerate(zip(cave, chief)) if a.get("holds") and b.get("holds")]
assert both and chief[both[-1] + 1].get("holds") is None and cave[-1]["holds"] == {"meat": "r"}, "hand-off order"
# Style 4: the mug is only ever in the own right hand
assert all(f.get("holds", {"mug": "r"}) == {"mug": "r"} for f in json.loads((HERE / "tracks/style4_cafe.json").read_text())["frames"])

for readme in ("README.md", "README.vi.md", "README.en.md", "README.ja.md", "README.ko.md", "README.pt-BR.md"):
    text = (ROOT / readme).read_text()
    for name in GIFS:
        assert f'src="docs/core-previews/{name}"' in text, (readme, name)
print(f"Core previews: {len(tracks)} rig tracks pass the posture gate with no warnings; every README shows them.")
