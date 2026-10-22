#!/usr/bin/env python3
"""Every slug style pack is gated with a sample package that passes package_lint and the hook test, and is listed in the catalog."""
import hashlib
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "skills/directing-stickman-videos/references"
STYLES = REFS / "styles"
sys.path.insert(0, str(ROOT / "tools/package_lint"))
import package_lint as pl  # noqa: E402

catalog = (REFS / "style-catalog.md").read_text()
experimental = catalog.split("### Experimental styles", 1)[1].split("\n---", 1)[0]
status = catalog.split("### Status", 1)[1].split("New styles are drafted", 1)[0]
# Prompts never carry brand or work names; packs may name works only in their Sources sections.
BRANDS = re.compile(r"\b(lego|minecraft|mario|nintendo|disney|pixar|marvel|youtube|ghibli|simpsons|bluey|pokemon|barbie)\b", re.I)

packs = sorted(STYLES.glob("*.md"))
assert len(packs) >= 24, f"expected the 24 kept style packs, found {len(packs)}"
for pack in packs:
    slug = pack.stem
    text = pack.read_text()
    assert re.search(r"Status: (gated|approved) \(", text), f"{slug}: no status block"
    assert f"| `{slug}` |" in experimental, f"{slug}: not in the experimental styles table"
    assert re.search(rf"^\| {re.escape(slug)} \| (gated|approved) \|", status, re.M), f"{slug}: no status row"
    sample = STYLES / "samples" / f"{slug}.md"
    facts = STYLES / "samples" / f"{slug}.facts.md"
    assert sample.exists() and facts.exists(), f"{slug}: sample package or facts missing"
    body = sample.read_text()
    findings, _ = pl.lint(body)
    reds = [f for f in findings if f[0] == pl.RED]
    assert not reds, f"{slug}: package_lint RED {reds}"
    lint = subprocess.run([sys.executable, str(ROOT / "tools/package_lint/package_lint.py"), str(sample), "--verify", str(facts)],
                          capture_output=True, text=True)
    assert lint.returncode == 0, f"{slug}: facts block was edited\n{lint.stdout}{lint.stderr}"
    digest = hashlib.sha256(sample.read_bytes()).hexdigest()[:16]
    assert f"sha256 {digest}" in facts.read_text(), f"{slug}: facts block is for another version of the sample; re-run package_lint --facts"
    hook = subprocess.run([sys.executable, str(ROOT / "tests/verify-opening-hook.py"), str(sample)], capture_output=True, text=True)
    assert hook.returncode == 0, f"{slug}: opening hook test failed\n{hook.stdout}{hook.stderr}"
    assert not BRANDS.search(body), f"{slug}: brand name in sample prompts: {BRANDS.search(body).group(0)}"
print(f"style packs: PASS ({len(packs)} gated packs, samples lint clean, hooks placed, catalog rows present)")
