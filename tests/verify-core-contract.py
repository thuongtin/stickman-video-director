#!/usr/bin/env python3
"""core-contract.md lists each shared rule once, points at files and checks that exist, and the skill routes through it."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/directing-stickman-videos"
REFS = SKILL / "references"
sys.path.insert(0, str(ROOT / "tools/package_lint"))
import package_lint as pl  # noqa: E402

core = (REFS / "core-contract.md").read_text()
rows = re.findall(r"^\| (C\d+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$", core, re.M)
assert [r[0] for r in rows] == [f"C{i}" for i in range(1, 19)], [r[0] for r in rows]

lint_doc = pl.__doc__
for cid, rule, owner, check, override in rows:
    for f in re.findall(r"`([\w./-]+\.md)`", owner):
        assert (REFS / f).exists() or (SKILL / f).exists() or (ROOT / f).exists(), f"{cid}: owner {f} missing"
    for code in re.findall(r"\b([AB]\d+)\b", check):
        assert re.search(rf"^\s+{code}\b", lint_doc, re.M), f"{cid}: package_lint has no check {code}"
    for t in re.findall(r"`(verify-[\w-]+\.py)`", check):
        assert (ROOT / "tests" / t).exists(), f"{cid}: {t} missing"
never = {r[0] for r in rows if r[4].strip() == "never"}
assert {"C2", "C7", "C8", "C10", "C11"} <= never, never
assert "never remove" in dict((r[0], r[4]) for r in rows)["C5"]

# Routing: the skill, the segment spec contract and the pack template point at the core contract.
skill = (SKILL / "SKILL.md").read_text()
assert "references/core-contract.md" in skill
assert "core-contract.md" in (REFS / "segment-spec-contract.md").read_text()
assert "core-contract.md" in (REFS / "style-pack-template.md").read_text()
assert "tools/risk_sheet/risk_sheet.py" in skill and "risk_sheet.py" in (REFS / "posture-gate.md").read_text()
# SKILL.md no longer carries its own copies of rules the core owns elsewhere.
for copy in ("Never place technical color notation", "Default generated clips to no visible words",
             "avoid abstract liquid/shape morphing", "Treat narration as audio-only"):
    assert copy not in skill, f"SKILL.md still repeats: {copy}"

# C11: no bundled spec names a studio, franchise, brand or artist.
packages = [REFS / "examples.md", *sorted((REFS / "styles/samples").glob("*.md"))]
for path in packages:
    for block in re.findall(r"```text\n(.*?)\n```", path.read_text(), re.S):
        m = pl.NAMED_SOURCE.search(block)
        assert not m, f"{path.name} spec names {m.group(0)}"
print(f"core contract: 18 rules, owners and checks exist, skill routes through it, {len(packages)} packages name no sources")
