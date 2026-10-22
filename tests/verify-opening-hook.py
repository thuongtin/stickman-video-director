#!/usr/bin/env python3
"""Hook instruction regression and package lint; this does not score rendered video retention."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/directing-stickman-videos"
STORYBOARD = SKILL / "references/storyboard-template.md"


def golden_hook():
    """The Golden Hook detail section of the storyboard template (the only hook reference)."""
    return STORYBOARD.read_text().split("### Golden Hook in detail", 1)[1].split("\n### ", 1)[0]

GREETINGS = ("hi ", "hello", "hey ", "welcome", "in this video", "today we", "today i",
             "let's talk", "let me tell")
WEAK_OPENINGS = ("appears", "appear ", "fades in", "fade in", "empty", "blank canvas",
                 "stands still", "standing alone")
ON_SCREEN_TEXT = ("countdown", "counter", "number", "statistic", "text", "words", "letters",
                  "typography", "caption")
BANNED_EFFECTS = ("morph", "strobe", "subliminal", "liquid")


def patterns():
    table = golden_hook().split("#### Pattern menu", 1)[1].split("####", 1)[0]
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


def first_beat(spec):
    start = re.search(r"\[0\s*[–-]", spec)
    assert start, "Clip 1 has no first timed beat"
    rest = spec[start.start():]
    end = re.search(r"\[3\s*[–-]", rest)
    return rest[:end.start()] if end else rest


def check_package(specs):
    """The hook lives in Clip 1's first frame and first beat; no spec carries a separate hook line."""
    assert specs, "No segment specs"
    for spec in specs:
        assert not re.search(r"^\s*Opening hook:", spec, re.M), "No separate Opening hook line in any spec"
    beat = first_beat(specs[0])
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

spec = "Build an approximately 10-second 16:9 horizontal 2D kinetic motion-graphics segment."
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

# Routing: one hook system, Stage 1 of the storyboard template; no separate hook reference.
assert not (SKILL / "references/opening-hook.md").exists(), "Hook detail belongs in the Golden Hook stage"
skill = (SKILL / "SKILL.md").read_text()
assert '"Golden Hook in detail"' in skill and "adds no extra spec line" in skill
storyboard = STORYBOARD.read_text()
assert "complete Golden Hook card" in storyboard and "`0–2s` hook" in storyboard
assert "passes the hook checks in \"Golden Hook in detail\"" in storyboard
assert storyboard.count("Golden Hook in detail") >= 3 and "Stage 1: Golden Hook" in storyboard
contract = (SKILL / "references/segment-spec-contract.md").read_text()
assert 'Clip 1 only: follow "Golden Hook in detail"' in contract
assert "The hook adds no separate line to the spec." in contract

ref = golden_hook()
for style in ("Style 1:", "Style 2A:", "Style 2B:", "Style 3:", "Style 4:"):
    assert style in ref, f"Missing style override: {style}"
assert "MIT-licensed" in ref, "Source attribution missing"
assert "not a second hook system" in ref and "Only the hook technique is taken" in ref, "Source scope must stay explicit"
assert "Opening hook:" not in ref and "weight the start of a prompt" not in ref, "Borrowed spec-order claim is back"
assert len(patterns()) >= 10

if len(sys.argv) > 1:
    check_package(re.findall(r"```text\n(.*?)\n```", Path(sys.argv[1]).read_text(), re.S))
    print("Supplied package hook check passed.")
print(f"Opening hook regression passed ({len(patterns())} patterns); no retention score claimed.")
