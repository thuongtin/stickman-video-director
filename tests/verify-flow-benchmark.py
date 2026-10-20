#!/usr/bin/env python3
"""The Flow benchmark prompt list matches its source packages, and the review step builds sheets and a results table."""
import csv
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests/flow-benchmark"))
import kit  # noqa: E402

listed = (ROOT / "tests/flow-benchmark/prompts.md").read_text()
assert listed == kit.prompts_md(), "prompts.md is stale; run: python3 tests/flow-benchmark/kit.py prompts -o tests/flow-benchmark/prompts.md"
assert listed.count("```text") == 12
for key, _, _, clips, _ in kit.SET:
    for n in clips:
        assert f"`{key}-clip{n}.mp4`" in listed
for block in listed.split("```text")[1:]:
    assert "Hands at start" in block and "no swapped left and right hands" in block.lower()

with tempfile.TemporaryDirectory() as tmp:
    clips = Path(tmp, "clips")
    clips.mkdir()
    if shutil.which("ffmpeg"):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc=size=320x180:rate=24:duration=10",
                        "-pix_fmt", "yuv420p", str(clips / "paper-cutout-clip2.mp4")], check=True)
    rows = kit.review(clips, Path(tmp, "review"))
    assert len(rows) == 12
    table = list(csv.DictReader(open(Path(tmp, "review/results.csv"))))
    assert [r["clip"] for r in table] == [r["clip"] for r in rows]
    done = [r for r in table if r["file"] != "MISSING"]
    if shutil.which("ffmpeg"):
        assert len(done) == 1 and Path(tmp, "review", done[0]["sheet"]).exists()
print("Flow benchmark kit: 12 prompts in sync with their packages; review builds sheets and results.csv")
