#!/usr/bin/env python3
"""Hook instruction regression and package lint; this does not score generated video retention."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/directing-stickman-videos"
REF = SKILL / "references/opening-hook.md"

GREETINGS = ("hi ", "hello", "hey ", "welcome", "in this video", "today we", "today i",
             "let's talk", "let me tell")
WEAK_OPENINGS = ("appears", "appear ", "fades in", "fade in", "empty", "blank canvas",
                 "stands still", "standing alone")
ON_SCREEN_TEXT = ("countdown", "counter", "number", "statistic", "text", "words", "letters",
                  "typography", "caption")
BANNED_EFFECTS = ("morph", "strobe", "subliminal", "liquid")


def patterns():
    table = REF.read_text().split("## Pattern menu", 1)[1].split("### ", 1)[0]
    return {row.split("|")[1].strip() for row in table.splitlines()
            if row.startswith("| ") and not row.startswith("| Pattern")}


def check_card(card, clip_count):
    for field in ("pattern", "first_frame", "hit_seconds", "sound_cue", "first_line",
                  "payoff_clip", "sound_off"):
        assert card.get(field) not in (None, ""), f"Hook card missing {field}"
    assert card["pattern"] in patterns(), f"Unknown hook pattern: {card['pattern']}"
    first_frame = card["first_frame"].lower()
    assert not any(w in first_frame for w in WEAK_OPENINGS), "First frame is an empty or idle opening"
    assert 0.5 <= card["hit_seconds"] <= 2.0, "Hook hit must land by about 2s"
    words = re.findall(r"[A-Za-z']+", card["first_line"])
    assert 4 <= len(words) <= 10, "First spoken line must be about four to ten words"
    assert not card["first_line"].lower().startswith(GREETINGS), "First spoken line is a greeting"
    assert 1 <= card["payoff_clip"] <= clip_count, "Open loop has no payoff clip"
    hook_text = " ".join((card["first_frame"], card["hit"])).lower()
    assert not any(w in hook_text for w in BANNED_EFFECTS), "Banned effect in hook"
    assert not any(re.search(rf"\b{w}", hook_text) for w in ON_SCREEN_TEXT), "On-screen text in hook"


def first_beat(prompt):
    start = re.search(r"\[0\s*[–-]", prompt)
    assert start, "Clip 1 has no first timed beat"
    rest = prompt[start.start():]
    end = re.search(r"\[3\s*[–-]", rest)
    return rest[:end.start()] if end else rest


def check_package(prompts):
    """The hook lives in Clip 1's first frame and first beat; no prompt carries a separate hook line."""
    assert prompts, "No prompts"
    for prompt in prompts:
        assert not re.search(r"^\s*Opening hook:", prompt, re.M), "No separate Opening hook line in any prompt"
    beat = first_beat(prompts[0])
    hits = [float(n) for n in re.findall(r"at about (\d+(?:\.\d+)?)\s*(?:s\b|sec)", beat, re.I)]
    assert hits and min(hits) <= 2.5, "Clip 1's first beat must time the hook hit at about 2s or earlier"
    low = beat.lower()
    assert not any(w in low for w in BANNED_EFFECTS), "Banned effect in the hook beat"


good_card = {
    "pattern": "Visual metaphor",
    "first_frame": "Stick Figure A is already bent under a violet thought tangle as big as a house, "
                   "knees buckling, on a black floor.",
    "hit": "the tangle drops another meter and the floor cracks under A",
    "hit_seconds": 1.5,
    "sound_cue": "half a second of near-silence, then one heavy thud on the drop",
    "first_line": "You're exhausted, and nothing has happened yet.",
    "payoff_clip": 4,
    "sound_off": "A person is crushed by a giant mess of thoughts.",
}
check_card(good_card, 6)
for field, bad in (
    ("pattern", "Countdown tension"),
    ("first_frame", "A violet dot appears beside Stick Figure A, who stands still."),
    ("hit_seconds", 4.0),
    ("first_line", "Hey everyone, welcome back to the channel, today we talk about overthinking."),
    ("first_line", "Tired?"),
    ("payoff_clip", 9),
    ("hit", "a counter spins and freezes on a huge number"),
    ("hit", "the tangle morphs into a liquid clock"),
    ("sound_off", ""),
):
    mutated = dict(good_card, **{field: bad})
    try:
        check_card(mutated, 6)
    except AssertionError:
        pass
    else:
        raise AssertionError(f"Bad hook card was not rejected: {field}={bad!r}")

spec = "Create an approximately 10-second 16:9 horizontal 2D kinetic motion-graphics clip."
hooked = ("First frame: Stick Figure A is already buckling under a house-sized violet thought tangle.\n"
          "[0–3s] A strains upward; at about 1.5s the tangle drops lower and the floor cracks.\n[3–7s] ...\n[7–10s] ...")
plain = "First frame: A walks right.\n[0–3s] A walks.\n[3–7s] ...\n[7–10s] ..."
check_package([f"{spec}\n\n{hooked}", f"{spec}\n\n{plain}", f"{spec}\n\n{plain}"])
for bad in (
    [f"{spec}\n\n{plain}", f"{spec}\n\n{plain}"],
    [f"{spec}\n\nOpening hook: A is buckling.\n\n{hooked}", f"{spec}\n\n{plain}"],
    [f"{spec}\n\n{hooked}", f"{spec}\n\nOpening hook: A is buckling.\n\n{plain}"],
    [f"{spec}\n\n{hooked.replace('at about 1.5s', 'at about 4s')}"],
    [f"{spec}\n\n{hooked.replace('drops lower', 'morphs into liquid')}"],
):
    try:
        check_package(bad)
    except AssertionError:
        pass
    else:
        raise AssertionError("Bad package hook placement was not rejected")

# Routing: every planning and prompt contract points at the hook reference.
skill = (SKILL / "SKILL.md").read_text()
assert "references/opening-hook.md" in skill and "adds no extra prompt line" in skill
storyboard = (SKILL / "references/storyboard-template.md").read_text()
assert "hook card from `opening-hook.md`" in storyboard and "`0–2s` hook" in storyboard
assert "passes the hook checks in `opening-hook.md`" in storyboard
contract = (SKILL / "references/omni-flash-prompt-contract.md").read_text()
assert "Clip 1 only: follow `opening-hook.md`" in contract
assert "The hook adds no separate line to the prompt." in contract

ref = REF.read_text()
for style in ("Style 1:", "Style 2A:", "Style 2B:", "Style 3:", "Style 4:"):
    assert style in ref, f"Missing style override: {style}"
assert "MIT-licensed" in ref, "Source attribution missing"
assert "nothing to do with Flow" in ref and "Only its hook technique is taken" in ref, "Source scope must stay explicit"
assert "Prompt placement" not in ref and "weight the start of a prompt" not in ref, "Borrowed prompt-order claim is back"
assert len(patterns()) >= 10

if len(sys.argv) > 1:
    check_package(re.findall(r"```text\n(.*?)\n```", Path(sys.argv[1]).read_text(), re.S))
    print("Supplied package hook check passed.")
print(f"Opening hook regression passed ({len(patterns())} patterns); no retention score claimed.")
