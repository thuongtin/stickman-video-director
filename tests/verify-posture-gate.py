#!/usr/bin/env python3
"""Posture gate fixtures: each known posture or left/right bug must be caught, clean motion must pass."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "tools/posture_gate"
sys.path[:0] = [str(GATE), str(GATE / "examples")]

import hand_ledger  # noqa: E402
import make_examples as ex  # noqa: E402
import posture_gate as pg  # noqa: E402


def kinds(result, severity="error"):
    return {i["kind"] for i in result["issues"] if i["severity"] == severity}


def side_track(bug=None):
    return ex.track(ex.frames_with(bug))


def front_track(bug=None):
    return ex.track(ex.front_frames(bug), rest=ex.front_pose(ex.wave(0)))


# clean motion passes in both profiles
for t in (side_track(), front_track()):
    r = pg.check(t)
    assert r["passed"] and not r["issues"], r["issues"][:3]
    assert pg.check(t, "video")["status"] == "PASS"

# posture bugs
expect = {
    ex.knee_backward: {"joint_limit", "snap"},
    ex.elbow_backward: {"joint_limit", "snap"},
    ex.head_backward: {"joint_limit"},
    ex.rubber_arm: {"bone_stretch"},
    ex.pop: {"pop"},
}
for bug, want in expect.items():
    r = pg.check(side_track(bug))
    assert not r["passed"] and want <= kinds(r), (bug.__name__, kinds(r))

r = pg.check(side_track(ex.topple))
assert r["passed"] and "balance" in kinds(r, "warn"), "standing 55 degree lean must warn"

# left/right hand bugs
expect = {
    ex.hand_swap: {"hand_swap"},
    ex.torso_flip: {"torso_flip"},
    ex.cup_switches_hand: {"prop_hand_switch"},
    ex.cup_in_wrong_hand: {"prop_wrong_hand"},
    ex.mirrored_hand: {"mirrored_hand"},
}
for bug, want in expect.items():
    r = pg.check(front_track(bug))
    assert not r["passed"] and want <= kinds(r), (bug.__name__, kinds(r))

# a planned hand-off is allowed
t = front_track(ex.cup_switches_hand)
t["frames"][6]["handoff"] = True
assert "prop_hand_switch" not in kinds(pg.check(t))

# prop must stay in the same hand across a cut
c1, c2 = ex.two_clips()
assert not any(pg.check(c)["errors"] for c in (c1, c2))
seq = pg.check_sequence([c1, c2])
assert [i["kind"] for i in seq] == ["prop_hand_switch"], seq

# fix repairs joint limits and limb lengths but does not invent repairs for pops
for bug in (ex.knee_backward, ex.elbow_backward, ex.head_backward, ex.rubber_arm):
    fixed = pg.check(pg.fix(side_track(bug)))
    assert fixed["passed"], (bug.__name__, fixed["issues"][:2])
assert not pg.check(pg.fix(side_track(ex.pop)))["passed"]

# the video profile sends errors to review instead of failing, unless strict,
# and skips figures too small for estimated joints to be trusted
def scaled(t, k):
    for f in t["frames"]:
        f["joints"] = {n: [x * k, y * k] for n, (x, y) in f["joints"].items()}
    return t

r = pg.check(scaled(side_track(ex.knee_backward), 3), "video")
assert r["status"] == "REVIEW" and not r["passed"] and "joint_limit" in kinds(r)
assert pg.check(scaled(side_track(ex.knee_backward), 0.5), "video")["frames_checked"] == 0

# per-track limit overrides (e.g. a dancer's high kick)
t = side_track(ex.head_backward)
t["limits_override"] = {"sagittal": {"neck": {"min": -130}}}
assert "joint_limit" not in kinds(pg.check(t))

# CLI exit codes
ok = GATE / "examples/walk_clean.json"
bad = GATE / "examples/knee_backward.json"
run = lambda *a: subprocess.run([sys.executable, str(GATE / "posture_gate.py"), *map(str, a)],
                                capture_output=True, text=True).returncode
assert run("check", ok) == 0 and run("check", bad) == 1
big = GATE / "examples/_big_knee.json"
big.write_text(__import__("json").dumps(scaled(side_track(ex.knee_backward), 3)))
try:
    assert run("check", big, "--profile", "video") == 0
    assert run("check", big, "--profile", "video", "--strict") == 1
finally:
    big.unlink()
assert run("check", GATE / "examples/clip1_cup_left.json", GATE / "examples/clip2_cup_right.json") == 1

# prompt-level hand ledger
assert hand_ledger.lint((GATE / "examples/ledger_ok.md").read_text()) == []
problems = hand_ledger.lint((GATE / "examples/ledger_bad.md").read_text())
assert any("beat puts the red paper card" in p for p in problems), problems
assert any("missing 'Hands at end'" in p for p in problems), problems
assert any("previous clip ended" in p for p in problems), problems
assert hand_ledger.lint("### Clip 1\nNo props here.\n") == []

# the skill points at the gate
skill = (ROOT / "skills/directing-stickman-videos/SKILL.md").read_text()
contract = (ROOT / "skills/directing-stickman-videos/references/omni-flash-prompt-contract.md").read_text()
assert "references/posture-gate.md" in skill
assert "Hands at start" in contract and "Hands at end" in contract

print("posture gate checks passed")
