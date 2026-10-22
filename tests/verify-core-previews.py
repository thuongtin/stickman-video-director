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
    assert data[:6] in (b"GIF87a", b"GIF89a") and len(data) < 1_200_000, (name, "missing or too large")
    assert int.from_bytes(data[6:8], "little") == 400 and int.from_bytes(data[8:10], "little") == 225, (name, "400x225")

tracks = sorted((HERE / "tracks").glob("*.json"))
assert {t.stem for t in tracks} == {"style1_light", "style1_dark", "style3_campfire", "style4_park_walk", "style4_cafe_wave"}
for t in tracks:
    data = json.loads(t.read_text())
    assert data["profile"] == "rig" and data.get("body_width") and data.get("limb_width"), f"{t.name}: rig figure sizes"
    out = subprocess.run([sys.executable, str(GATE), "check", "--json", str(t)], capture_output=True, text=True)
    clip = json.loads(out.stdout)["clips"][0]
    assert out.returncode == 0 and clip["errors"] == 0 and clip["warnings"] == 0, \
        f"{t.name}: {[i['message'] for i in clip['issues']]}"

# Style 4 keeps the cup in the own right hand across the cut
for name in ("style4_park_walk", "style4_cafe_wave"):
    frames = json.loads((HERE / "tracks" / f"{name}.json").read_text())["frames"]
    assert all(f["holds"] == {"cup": "r"} for f in frames), name
both = subprocess.run([sys.executable, str(GATE), "check", "--json", str(HERE / "tracks/style4_park_walk.json"),
                       str(HERE / "tracks/style4_cafe_wave.json")], capture_output=True, text=True)
assert both.returncode == 0, both.stdout[-400:]

for readme in ("README.md", "README.vi.md", "README.en.md", "README.ja.md", "README.ko.md", "README.pt-BR.md"):
    text = (ROOT / readme).read_text()
    for name in GIFS:
        assert f'src="docs/core-previews/{name}"' in text, (readme, name)
print(f"Core previews: {len(tracks)} rig tracks pass the posture gate with no warnings; every README shows them.")
