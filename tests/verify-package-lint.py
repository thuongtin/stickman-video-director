#!/usr/bin/env python3
"""package_lint passes the bundled examples and catches each broken package it claims to catch (prompt text only)."""
from pathlib import Path
import re
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools/package_lint"))
import package_lint as pl  # noqa: E402

examples = (ROOT / "skills/directing-stickman-videos/references/examples.md").read_text()
style1, style2a = examples.split("# Example 2:", 1)


def codes(text, **kw):
    return {c for level, c, _ in pl.lint(text, **kw)[0] if level == pl.RED}


assert codes(style1, clips=6) == set(), pl.lint(style1, clips=6)[0]
assert codes(style2a, clips=3) == set(), pl.lint(style2a, clips=3)[0]

clip2 = style1.index("### Clip 2")
mutations = {
    "A1": (style1, {"clips": 5}),
    "A2": (style1.replace("| A 双手空。 |", "|  |", 1), {}),
    "A4": (style1.replace("镜头拉远，A 走向金色地平线", "切到一张金句卡", 1), {}),
    "A6": (style1.replace("“WHAT IF?”", "“90% WHAT IF?”", 1), {}),
    "B2": (style1[:clip2] + style1[clip2:].replace("Use a pure black background.",
                                                   "Opening hook: A is already falling.\n\nUse a pure black background.", 1), {}),
    "B3": (style1.replace("Hands at end — A: right hand empty; left hand empty.",
                          "Hands at end — A: right hand holds the violet cord; left hand empty.", 1), {}),
    "B4": (style1[:clip2] + style1[clip2:].replace("no filled body, stable proportions", "stable proportions", 1), {}),
    "B5": (style1[:clip2] + style1[clip2:].replace("steady speaking pace", "brisk speaking pace", 1), {}),
    "B6": (style1.replace("saturated anxiety violet,", "saturated anxiety violet (#7B2CBF),", 1), {}),
    "B7": (style1.replace("an icon-only envelope is struck", "a sign reading \"FAIL\" appears and an icon-only envelope is struck", 1), {}),
    "B8": (style1.replace("The red bars snap apart,", "The red bars morph into vines,", 1), {}),
    "B9": (style1.replace("[3–7s] Travel across", "Travel across", 1), {}),
    "B10": (style1.replace("no swapped left and right hands, ", "", 1), {}),
}
for code, (text, kw) in mutations.items():
    assert text != style1 or kw, f"mutation for {code} did not apply"
    got = codes(text, **kw)
    assert code in got, f"package_lint missed {code}: got {sorted(got)}"

# Per-speaker voice lines: a speaker may be absent from a clip, but their block never changes.
duo = "\n".join([
    "```text\n[0–3s] Ana runs; at about 1s she trips.\n[3–7s] Ana stops.\n[7–10s] Ana waves.\n"
    "Voice — Ana: adult woman, General American accent, warm alto.\nNo swapped left and right hands.\n```",
    "```text\n[0–3s] Ben runs.\n[3–7s] Ana and Ben stop.\n[7–10s] Ben waves.\n"
    "Voice — Ana: adult woman, General American accent, warm alto.\n"
    "Voice — Ben: adult man, Scottish accent, light tenor.\nNo swapped left and right hands.\n```"])
assert "B5" not in codes(duo), pl.lint(duo)[0]
assert "B5" in codes(duo.replace("Scottish accent, light tenor.\nNo", "Irish accent, light tenor.\nNo").replace(
    "Voice — Ana: adult woman, General American accent, warm alto.\nVoice — Ben", "Voice — Ana: adult woman, General American accent, bright alto.\nVoice — Ben")), "speaker drift not caught"

# Every one of the five posture negatives is required, not only the left/right one.
for phrase in ("No knees or elbows bending backward, ", "no limbs changing length, ", "no head turned past the shoulders, ",
               "no prop switching hands without a visible pass"):
    broken = style1.replace(phrase, "", 1)
    assert broken != style1 and "B10" in codes(broken), f"missing \"{phrase}\" not caught"

# Music continuity and logos are flagged for a look (the bundled Style 1 example scores an arc on purpose).
yellow = lambda text: {c for level, c, _ in pl.lint(text)[0] if level == pl.YELLOW}
assert "B12" not in yellow(style2a), [x for x in pl.lint(style2a)[0] if x[1] == "B12"]
assert "B12" in yellow(style2a.replace("synth from clip 1", "synth", 1))
assert "B12" not in yellow(style2a.replace("Audio: Voiceover seamlessly continues", "Music seamlessly continues"))
assert "B13" not in yellow(style1) and "B13" in yellow(style1.replace("logos, or watermarks", "or watermarks"))

# A named studio, franchise or artist is RED even inside a negative (core-contract.md C11).
assert "B14" in codes(style2a.replace("no 3D humanoid models", "no Pixar-style 3D humanoid models", 1))
assert "B14" in codes(style1.replace("no clothing,", "no LEGO bricks, no clothing,", 1))

# Yellow checks: camera grammar and weak beats.
cam = style1.replace("低机位固定镜头", "低机位推近", 1).replace("侧向跟拍、摔倒拆解", "快速推近、摔倒拆解", 1)
assert any(c == "A3" for _, c, _ in pl.lint(cam)[0]), "three inward rows not flagged"
weak = style1.replace("[3–7s] An icon-only white clock", "[3–7s] An icon-only white clock fades in and", 1)
assert any(c == "B11" for _, c, _ in pl.lint(weak)[0]), "fade-in beat not flagged"
assert not any(c == "B11" for _, c, _ in pl.lint(style1)[0]), "object verbs (slam down, whip up) read as camera accents"

# Facts block: written by the script, edits are detected.
with tempfile.TemporaryDirectory() as d:
    pkg, facts = Path(d, "package.md"), Path(d, "facts.md")
    pkg.write_text(style1)
    facts.write_text(pl.facts_block(pkg, pl.lint(style1, clips=6)[1]))
    assert pl.verify(facts) and "hand_ledger: PASS" in facts.read_text()
    facts.write_text(facts.read_text().replace("red: 0", "red: 0 (all good)"))
    assert not pl.verify(facts), "edited facts block not detected"

assert "package_lint.py" in (ROOT / "skills/directing-stickman-videos/references/omni-flash-prompt-contract.md").read_text()
print(f"package lint: PASS ({len(mutations)} broken packages caught; examples clean)")
