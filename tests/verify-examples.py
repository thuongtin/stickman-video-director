#!/usr/bin/env python3
"""The bundled examples must obey the rules they illustrate (prompt text only; no generated-video score)."""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "skills/directing-stickman-videos"
REFS = SKILL / "references"
sys.path.insert(0, str(REPO / "tools/posture_gate"))
import hand_ledger  # noqa: E402

examples = (REFS / "examples.md").read_text()
catalog = (REFS / "style-catalog.md").read_text()
style1, style2a = examples.split("# Example 2:", 1)


def prompts(text):
    return re.findall(r"```text\n(.*?)\n```", text, re.S)


# Hands: each example passes the same gate Phase B packages must pass.
for name, part in (("Style 1", style1), ("Style 2A", style2a)):
    problems = hand_ledger.lint(part)
    assert problems == [], f"{name} example fails hand_ledger: {problems}"
    for prompt in prompts(part):
        assert "Hands at start —" in prompt and "Hands at end —" in prompt, f"{name}: clip without Hands lines"
        assert "no swapped left and right hands" in prompt.lower(), f"{name}: clip without posture negatives"

# Character anchors are the current ones, verbatim, in every clip; no "same figure..." shortcut.
dark = re.findall(r"```text\n(.*?)\n```", catalog.split("**Classic Dark", 1)[1], re.S)[0]
assert all(dark in p for p in prompts(style1)), "Style 1 example must repeat the current Dark anchor"
lead = re.findall(r"```text\n(.*?)\n```", catalog.split("**Character Anchor (every clip, verbatim):**", 1)[1], re.S)[0]
beanie = re.findall(r"```text\n(.*?)\n```", catalog.split("**Alternative: Beanie Zeke anchor", 1)[1], re.S)[0]
assert "white round head" in lead and "dot eyes" in lead and "buzz cut" in lead and "glasses" in lead and "white short-sleeved button-up shirt" in lead and "small pointed collar" in lead and "very short neck" in lead and "stick arms" in lead and "legs in dark blue jeans" in lead and "short wide sleeves" in lead and "cut like a t-shirt" in lead, "Style 2 default lead is the buzz-cut, glasses one"
assert "red beanie" in beanie and "no pom-pom" in beanie, "the beanie lead stays documented as the alternative"
assert all(f"Character: {lead}" in p for p in prompts(style2a)), "Style 2A example must repeat the full default anchor"
assert not any(beanie in p for p in prompts(style2a)), "one lead per video"
for path in (SKILL / "SKILL.md", REFS / "omni-flash-prompt-contract.md"):
    assert lead in path.read_text(), f"{path.name} must carry the same default Style 2 anchor"
assert "shorts" not in style2a.replace("never shorts", ""), "the default lead wears jeans, not shorts"
for path in [SKILL / "SKILL.md", *REFS.glob("*.md")]:
    assert "The same minimalist 2D animated stick figure" not in path.read_text().replace(
        '("The same minimalist 2D animated stick figure in a bright red beanie and yellow shirt" followed by an ellipsis)', ""), \
        f"Retired Style 2 shortcut in {path.name}"

# Opening hook: carried by clip 1's first frame and first beat, never a separate line.
for part in (style1, style2a):
    ps = prompts(part)
    assert not any("Opening hook:" in p for p in ps)
    assert re.search(r"\[0–3s\][^\n]*at about 1\.5s", ps[0], re.I), "Clip 1's first beat times the hook hit"

# No on-screen words or abstract morphing taught by example.
for p in prompts(examples):
    beats = re.sub(r'\(VO: "[^"]*"\)|“[^”]*”', "", p)
    assert not re.search(r"text reading|BONK|'[A-Z][A-Z ]+'", beats), "Example puts words on screen"
    assert not re.search(r"\b(splits into|separates into|snaps back into|Transform the|Fold the|Bend the)\b", beats), \
        "Example uses shape morphing"

# Storyboard rules the examples follow.
story = (REFS / "storyboard-template.md").read_text()
assert "| Motion, camera, and transition | Hands |" in story
assert "shape morph," not in story and "fluid," not in story
assert "Posture budget per beat" in story
assert "手（以角色自身左右为准）" in style1
# the old flannel outfit is gone everywhere the default lead is described
for path in [SKILL / "SKILL.md", *REFS.glob("*.md")]:
    assert "flannel" not in path.read_text().lower(), f"{path.name} still describes the old flannel outfit"
print("Examples follow the hands, anchor, hook, no-text and no-morph rules; no generated-video score claimed.")
