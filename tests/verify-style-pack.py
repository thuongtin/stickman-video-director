#!/usr/bin/env python3
"""Style pack template states honest status levels and a signature checklist; the catalog labels Styles 1-4."""
from pathlib import Path

REFS = Path(__file__).resolve().parents[1] / "skills/directing-stickman-videos/references"
template = (REFS / "style-pack-template.md").read_text()
for phrase in ("`research`", "`gated`", "`flow-tested`", "`approved`", "lowest level whose evidence exists",
               "the lower one counts", "Five signature traits", "`must`", "`bonus`", "`forbidden`",
               "Nearest neighbour", "no studio, artist, brand or signature character", "three options that differ in composition",
               "package_lint.py", "huashu-art-motion (MIT"):
    assert phrase in template, f"style-pack-template.md lost: {phrase}"

catalog = (REFS / "style-catalog.md").read_text()
status = catalog.split("### Status", 1)[1].split("New styles are drafted", 1)[0]
for style in ("Style 1 Dark", "Style 1 Light", "Style 2A", "Style 2B", "Style 3", "Style 4"):
    row = next((l for l in status.splitlines() if l.startswith(f"| {style} |")), None)
    assert row, f"catalog has no status row for {style}"
    assert any(f"| {lvl} |" in row for lvl in ("research", "gated", "flow-tested", "approved")), row
assert "style-pack-template.md" in catalog
print("style pack template and catalog status: PASS")
