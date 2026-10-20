#!/usr/bin/env python3
"""risk_sheet.py finds the risky moments a prompt names and cuts a contact sheet around them (no error detection claimed)."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools/risk_sheet"))
import risk_sheet as rs  # noqa: E402

ok = (ROOT / "tools/posture_gate/examples/ledger_ok.md").read_text()
moments = rs.plan(ok, 1)
kinds = [k for _, k, _, _ in moments]
assert kinds[0] == "start" and kinds[-1] == "end"
passing = [m for m in moments if m[1] == "hand pass"]
assert len(passing) == 1 and "passes the card" in passing[0][2], moments
assert passing[0][3].startswith("changing: Pip: R red paper card, L empty -> Pip: R empty, L red paper card")
assert moments[0][3] == "Pip: R red paper card, L empty" and moments[-1][3] == "Pip: R empty, L red paper card"

pkg = """### Clip 1
Hands at start — Mai: right hand holds the cup; left hand empty.
[0–3s] Mai walks right. At about 1.5s she turns to face the window.
[3–7s] A clock spins on the wall; the leaves fall outside.
[7–10s] Mai passes the cup to her left hand.
Audio-only dialogue, exactly once: “She turns, she falls, she passes it on.”
Hands at end — Mai: right hand empty; left hand holds the cup.
"""
moments = rs.plan(pkg, 1)
found = {(t, k) for t, k, _, _ in moments}
assert (1.5, "turn") in found, moments                       # "at about 1.5s" sets the time
assert not any(k == "fall" or "clock" in c for _, k, c, _ in moments), moments  # scenery and dialogue are not body moments
turn = next(m for m in moments if m[1] == "turn")
assert turn[3] == "Mai: R cup, L empty", turn                # before the pass: the start hands
assert "Mai: R cup" in rs.checklist(1, moments)

# Every shipped style sample has a plan for every clip.
for sample in sorted((ROOT / "skills/directing-stickman-videos/references/styles/samples").glob("*.md")):
    if sample.name.endswith(".facts.md"):
        continue
    text = sample.read_text()
    for n in range(1, 4):
        if f"Clip {n}" in text:
            assert rs.plan(text, n)[0][1] == "start"

if shutil.which("ffmpeg") and shutil.which("ffprobe"):
    try:
        import PIL  # noqa: F401
    except ImportError:
        print("Pillow missing; skipped the sheet render")
    else:
        with tempfile.TemporaryDirectory() as tmp:
            video = Path(tmp) / "clip1.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                            "testsrc=size=320x180:rate=24:duration=10", "-pix_fmt", "yuv420p", str(video)], check=True)
            assert rs.main([str(ROOT / "tools/posture_gate/examples/ledger_ok.md"), "--batch", tmp, "-o", f"{tmp}/out"]) == 0
            out = Path(tmp) / "out/clip1"
            assert (out / "clip1-sheet.png").stat().st_size > 10_000
            assert "clip1-sheet.png" in (out / "clip1-checklist.md").read_text()
else:
    print("ffmpeg missing; skipped the sheet render")
print("risk sheet plans and renders passed; it marks moments for a person, it does not judge them.")
