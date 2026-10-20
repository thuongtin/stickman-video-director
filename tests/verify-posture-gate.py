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

# a planned hand-off is allowed when the taking hand is at the prop the frame before
t = front_track(ex.cup_switches_hand)
t["frames"][6]["handoff"] = True
f5 = t["frames"][5]; new = (pg.hands_of(t["frames"][6]["holds"]["cup"]) - pg.hands_of(f5["holds"]["cup"])).pop()
far = list(f5["joints"][f"wrist_{new}"])
f5["joints"][f"wrist_{new}"] = list(f5["props"]["cup"])
assert "prop_hand_switch" not in kinds(pg.check(t)), [i for i in pg.check(t)["issues"] if i["kind"] == "prop_hand_switch"]
f5["joints"][f"wrist_{new}"] = far  # the taking hand jumps onto the cup from far away
assert "prop_hand_switch" in kinds(pg.check(t))

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

# ---- feedback from the style threads ----
import math  # noqa: E402

def front3d(bug=None, n=6):
    """Front-facing wave as a 3D rig (y up, character faces +z, its left is +x)."""
    t = front_track()
    t.pop("rest")
    for i, f in enumerate(t["frames"][:n]):
        j = {k: [x, -y, 0.0] for k, (x, y) in f["joints"].items()}
        for side in ("l", "r"):  # feet point forward, toward the camera
            a = j[f"ankle_{side}"]; j[f"toe_{side}"] = [a[0], a[1] - 1, 10.0]
        j["nose"] = [j["head"][0], j["head"][1], 8.0]
        f["joints"], f["props"] = j, {k: [x, -y, 0.0] for k, (x, y) in f["props"].items()}
        if bug:
            bug(i, f)
    t["frames"] = t["frames"][:n]
    return t

def point_at_camera(i, f):
    j = f["joints"]; sh = j["shoulder_r"]
    j["elbow_r"] = [sh[0], sh[1], 30.0]; j["wrist_r"] = [sh[0], sh[1], 58.0]

def yaw_120(i, f):
    h = f["joints"]["head"]
    f["joints"]["nose"] = [h[0] + 8 * math.sin(math.radians(120)), h[1], 8 * math.cos(math.radians(120))]

def flip3d(i, f):
    j = f["joints"]
    for k in ("shoulder", "elbow", "wrist"):
        j[f"{k}_l"], j[f"{k}_r"] = j[f"{k}_r"], j[f"{k}_l"]
    f["props"] = {}

# 3D rigs: an arm pointing at the camera is not a shrunk limb; yaw and twist are caught in 3D
assert pg.check(front3d())["passed"], pg.check(front3d())["issues"][:3]
assert pg.check(front3d(point_at_camera))["passed"], pg.check(front3d(point_at_camera))["issues"][:3]
assert "head_yaw" in kinds(pg.check(front3d(yaw_120)))
assert "torso_flip" in kinds(pg.check(front3d(flip3d)))

# kneeling / sitting: whatever touches the ground supports the body; named supports work too
def kneel(i, a, kw, f):
    a.update(lean=0, hip_l=90, knee_l=90, hip_r=-10, knee_r=150, ankle_r=-40)
r = pg.check(side_track(kneel))
assert "balance" not in kinds(r, "warn"), r["issues"][:3]
t = side_track(ex.topple)
for f in t["frames"]:
    f["supported"] = ["wrist_l"]
    f["joints"]["wrist_l"] = [f["joints"]["neck"][0] + 40, f["joints"]["toe_l"][1]]
assert "balance" not in kinds(pg.check(t), "warn")
t = side_track(ex.topple)
for f in t["frames"]:
    f["supported"] = True
assert "balance" not in kinds(pg.check(t), "warn")

# a big chibi head can be given its own mass
assert pg.center_of_mass({"neck": (0, 1), "head": (10, 2), "pelvis": (0, 0)}, {"head": 0.5}) > \
    pg.center_of_mass({"neck": (0, 1), "head": (10, 2), "pelvis": (0, 0)})

# pixel-snapped rigs: 1 px of rounding on a 4 px bone is not a stretch in the pixel profile
t = side_track()
for f in t["frames"]:
    f["joints"] = {k: [round(x / 9), round(y / 9)] for k, (x, y) in f["joints"].items()}
t.pop("rest")
assert "bone_stretch" in kinds(pg.check(t, "rig")) or "bone_shrink" in kinds(pg.check(t, "rig"))
assert not ({"bone_stretch", "bone_shrink"} & kinds(pg.check(t, "pixel")))

# front view: a sideways-looking knee under a raised thigh (cross-legged) is only a warning
def cross_legged(i, a, f):
    a["leg_l"] = a["leg_r"] = 80
r = pg.check(front_track(cross_legged))
assert "joint_limit" not in kinds(r) and "joint_limit" in kinds(r, "warn"), r["issues"][:2]

# hand contact and arm over face
t = front_track()
t["frames"][3]["props"]["door"] = [400, 100]; t["frames"][3]["contacts"] = {"r": "door"}
assert "contact_miss" in kinds(pg.check(t))
t = front_track()
f = t["frames"][2]; f["joints"]["wrist_l"] = [f["joints"]["head"][0] - 10, f["joints"]["head"][1]]
f["joints"]["elbow_l"] = [f["joints"]["head"][0] + 14, f["joints"]["head"][1] + 20]; f["props"] = {}; f["holds"] = {}
assert "arm_over_face" in kinds(pg.check(t), "warn")
f["contacts"] = {"l": f["joints"]["wrist_l"]}  # a hand on the chin is meant to be there
assert "arm_over_face" not in kinds(pg.check(t), "warn")
del f["contacts"]
f["face_cover"] = True
assert "arm_over_face" not in kinds(pg.check(t), "warn")
# facing the camera, both hands jumping across the midline in one frame warns (arms folding fast look the same)
t = front_track()
for i, f in enumerate(t["frames"]):
    j = f["joints"]; f["props"] = {}; f["holds"] = {}
    T = ((j["neck"][0] - j["pelvis"][0]) ** 2 + (j["neck"][1] - j["pelvis"][1]) ** 2) ** 0.5
    x, y = j["pelvis"][0], j["pelvis"][1]
    d = 0.28 * T if i < 3 else -0.14 * T
    j["wrist_l"], j["wrist_r"] = [x + d, y - (0 if i < 3 else 0.1 * T)], [x - d, y - (0 if i < 3 else 0.1 * T)]
assert any(i["kind"] == "hand_swap" and i["frame"] == 3 and i["severity"] == "warn" for i in pg.check(t)["issues"])
# side view: arms swinging past each other in a walk are not a hand swap
assert "hand_swap" not in kinds(pg.check(ex.track(ex.frames_with(None))))
# side view: the near arm across the head warns, unless it holds or touches something there
t = ex.track(ex.frames_with(None))
f = t["frames"][4]; hx, hy = f["joints"]["head"]
f["joints"]["elbow_r"] = [hx + 25, hy + 20]; f["joints"]["wrist_r"] = [hx + 4, hy - 4]
assert "arm_over_face" in kinds(pg.check(t), "warn")
f["holds"] = {"mug": "r"}; f["props"] = {"mug": [hx - 10, hy]}
assert "arm_over_face" not in kinds(pg.check(t), "warn")
# side view: a held prop on the face warns; a prop at the face edge (a cup at the mouth) does not
t = ex.track(ex.frames_with(None))
f = t["frames"][4]; hx, hy = f["joints"]["head"]
f["holds"] = {"ball": "r"}; f["props"] = {"ball": [hx + 2, hy]}
assert "arm_over_face" in kinds(pg.check(t), "warn")
f["face_cover"] = True
assert "arm_over_face" not in kinds(pg.check(t), "warn")
# a prop point can have its own contact: the cane tip must reach the ground
t = ex.track(ex.frames_with(None))
f = t["frames"][4]; wx, wy = f["joints"]["wrist_r"]
ground = max(v[1] for k, v in f["joints"].items() if k.startswith(("toe", "ankle", "heel")))
f["holds"] = {"cane": "r"}; f["props"] = {"cane": [wx, wy], "cane.tip": [wx + 5, ground - 40]}
f["contacts"] = {"r": "cane", "cane.tip": "ground"}
assert "contact_miss" in kinds(pg.check(t))
f["props"]["cane.tip"][1] = ground
assert "contact_miss" not in kinds(pg.check(t))
# contacts: a wrist 0.3 torso-lengths short of its target misses by default, passes with a looser tolerance
t = front_track(); f = t["frames"][3]; j = f["joints"]
torso = ((j["neck"][0] - j["pelvis"][0]) ** 2 + (j["neck"][1] - j["pelvis"][1]) ** 2) ** 0.5
f["props"]["chin"] = [j["wrist_r"][0] + 0.3 * torso, j["wrist_r"][1]]; f["contacts"] = {"r": "chin"}
assert "contact_miss" in kinds(pg.check(t))
t["contact_tolerance"] = 0.35
assert "contact_miss" not in kinds(pg.check(t))

# mirrored figure: every joint labelled on the wrong side while facing the camera
t = front_track()
for f in t["frames"]:
    f["joints"] = {(k[:-1] + {"l": "r", "r": "l"}[k[-1]] if k[-2:] in ("_l", "_r") else k): v
                   for k, v in f["joints"].items()}
    f["holds"], f["props"] = {}, {}
assert "mirrored_body" in kinds(pg.check(t))

# a zero-length rest bone (foot pointing straight at the camera) must not crash
t = front_track()
t["rest"]["toe_l"] = list(t["rest"]["ankle_l"]); t["rest"]["toe_r"] = list(t["rest"]["ankle_r"])
pg.check(t)

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
assert any("ended clip 1 with" in p for p in problems), problems
assert hand_ledger.lint("### Clip 1\nNo props here. She holds her breath.\n") == []
# no ledger at all while a beat holds something
assert hand_ledger.lint("### Clip 1\n[0-3s] Mia grabs the phone from the table.\n")
assert hand_ledger.lint("[0-3s] Mia grabs the phone from the table.\n")  # one prompt, no heading
assert hand_ledger.lint("[0-3s] Mia waves.\n") == []
# spoken narration is not a beat: neither a VO "carrying" nor a VO "it" counts as a hand action
assert hand_ledger.lint('Audio-only dialogue: “Your mind is already carrying a hundred disasters.”\n[0-3s] Mia waves.\n') == []
assert hand_ledger.lint('### Clip 1\nHands at start — Mia: right hand empty; left hand empty.\n'
                        '[3-7s] (VO: "Push and it begins to open."): Mia places her right hand on the door.\n'
                        'Hands at end — Mia: right hand empty; left hand empty.\n') == []
problems = hand_ledger.lint("Style: the character holds clean key poses; speed lines carry the energy.\n"
                            "[0-3s] Mia's right hand grabs the phone.\n")
assert len(problems) == 1 and "grabs the phone" in problems[0], problems
assert hand_ledger.lint("Style: the character holds clean key poses between snaps.\n") == []
assert any("near arm" in p for p in hand_ledger.lint("[0-3s] Pip raises his near arm.\n"))
# paws count as hands, and a sentence is checked against the character it names
pkg = """### Clip 1
Hands at start — Kaka: right flipper holds the blue folder; left flipper empty. Miso: right paw empty; left paw holds the red folder.
[0-3s] Miso opens the folder in her right paw.
Hands at end — Kaka: right flipper holds the blue folder; left flipper empty. Miso: right paw empty; left paw holds the red folder.
"""
problems = hand_ledger.lint(pkg)
assert len(problems) == 1 and "Miso's right hand" in problems[0], problems
# several characters: a hand belongs to the clause's subject or to "Name's"; a pass must be about
# the prop; one prop is never in two characters' hands; "Mr." stays part of a name
pkg = """### Clip 1
Hands at start — Candy: right hand holds the red balloon; left hand empty. Bean: right hand empty; left hand empty. Mr. Square: right hand empty; left hand holds the briefcase.
[0-3s] Candy walks up to Bean and holds the red balloon out in her right hand.
[3-7s] Candy passes the red balloon from her right hand into Bean's left hand. Mr. Square watches, briefcase in his left hand.
Hands at end — Candy: right hand empty; left hand empty. Bean: right hand empty; left hand holds the red balloon. Mr. Square: right hand empty; left hand holds the briefcase.
"""
assert hand_ledger.lint(pkg) == [], hand_ledger.lint(pkg)
problems = hand_ledger.lint(pkg.replace("Candy passes the red balloon from her right hand into Bean's left hand.",
                                        "Candy smiles. The marker leaves frame."))
assert len(problems) == 2 and all("no beat passes" in p for p in problems), problems
assert hand_ledger.lint(pkg.replace("Candy passes the red balloon from her right hand into Bean's left hand.",
                                    "Candy sets the red balloon down. Bean picks the red balloon up with his left hand.")) == []
problems = hand_ledger.lint(pkg.replace("Hands at end — Candy: right hand empty", "Hands at end — Candy: right hand holds the red balloon"))
assert len(problems) == 1 and "Bean and Candy's hands at the end" in problems[0], problems
problems = hand_ledger.lint(pkg.replace("briefcase in his left hand", "briefcase in his right hand"))
assert len(problems) == 1 and "Mr. Square's right hand" in problems[0], problems
pkg = """### Clip 1
Hands at start — Kai: right hand holds the teddy bear; left hand empty. Mimi: right hand empty; left hand empty.
- [0-3s] (VO: "Mimi tries a different one."): Kai holds the teddy bear out in his right hand.
- [3-7s] Kai lets go of the teddy bear as Mimi takes it with her left hand.
Hands at end — Kai: right hand empty; left hand empty. Mimi: right hand empty; left hand holds the teddy bear.
"""
assert hand_ledger.lint(pkg) == [], hand_ledger.lint(pkg)
assert hand_ledger.lint(pkg.replace("as Mimi takes it with her left hand", "and passes it to Mimi, who takes it with the left hand")) == []
assert hand_ledger.lint(pkg.replace("Kai lets go of the teddy bear as Mimi takes it with her left hand",
                                    "Mimi walks over, takes the teddy bear from Kai with her left hand")) == []
# a character who skips a clip is compared with their own last hands line
pkg = """### Clip 1
Hands at start — Ti: right hand holds the teddy; left hand empty.
[0-3s] Ti hugs the teddy in his right hand.
Hands at end — Ti: right hand holds the teddy; left hand empty.
### Clip 2
Hands at start — Mai: right hand empty; left hand empty.
[0-3s] Mai waves.
Hands at end — Mai: right hand empty; left hand empty.
### Clip 3
Hands at start — Ti: right hand empty; left hand holds the teddy.
[0-3s] Ti hugs the teddy in his left hand.
Hands at end — Ti: right hand empty; left hand holds the teddy.
"""
assert any("ended clip 1 with teddy" in p for p in hand_ledger.lint(pkg)), hand_ledger.lint(pkg)
# paws and "who"; a part names its prop; pointing is not holding; an unlisted prop in an empty hand warns
pkg = """### Clip 1
Hands at start — Pip: right paw empty; left paw holds the carrot. Toby: right paw empty; left paw empty. Na: right hand empty; left hand empty.
[0-3s] Pip hops out holding the carrot in his left paw and gives the carrot to Toby, who takes it in his right paw.
[3-7s] Na points at it with her right hand. Mai gives Na the yellow paper balloon; Na takes the string in her left hand.
Hands at end — Pip: right paw empty; left paw empty. Toby: right paw holds the carrot; left paw empty. Na: right hand empty; left hand holds the yellow paper balloon.
"""
assert hand_ledger.lint(pkg) == [], hand_ledger.lint(pkg)
problems = hand_ledger.lint(pkg.replace("takes the string in her left hand", "takes the string in her right hand"))
assert len(problems) == 1 and "balloon in Na's right hand" in problems[0], problems
warnings = []
assert hand_ledger.lint(pkg.replace("Na points at it", "Na draws with a paper pencil in her right hand. Na points at it"), warnings) == []
assert len(warnings) == 1 and "paper pencil in Na's right hand" in warnings[0], warnings
# "her" in a sentence naming nobody is the character named last; the quoted beat drops the VO placeholder
pkg = """### Clip 1
Hands at start — Tilly: right hand holds the stamp; left hand holds the red folder. Marge: right hand holds the red folder; left hand empty.
- [0-3s] (VO: "Again."): Tilly stamps the square; her left hand keeps holding the red folder open.
- [3-7s] Marge waits.
Hands at end — Tilly: right hand holds the stamp; left hand holds the red folder. Marge: right hand holds the red folder; left hand empty.
"""
assert not any("Marge's left" in p for p in hand_ledger.lint(pkg)), hand_ledger.lint(pkg)
problems = hand_ledger.lint(pkg.replace("her left hand keeps", "her right hand keeps"))
assert any("Tilly's right" in p for p in problems) and all('""' not in p for p in problems), problems
# names match whole words with their case: "Ti" is not "Timed", "May" is not "may"
pkg = """### Clip 1
Hands at start — May: right hand empty; left hand holds the lantern. Ti: right hand empty; left hand empty.
Timed beats:
- [0-3s] May flips around and holds the lantern up in her right hand.
Hands at end — May: right hand empty; left hand holds the lantern. Ti: right hand empty; left hand empty.
"""
problems = hand_ledger.lint(pkg)
assert len(problems) == 1 and "lantern in May's right hand" in problems[0], problems
# gloves and mittens are hands; "Name's open left glove" is that character's
pkg = """### Clip 1
Hands at start — Bơ: right hand holds the pie; left hand empty. Mít: right hand empty; left hand empty.
- [0-3s] Bơ slides the pie onto Mít's open left glove and lets go.
Hands at end — Bơ: right hand empty; left hand empty. Mít: right hand empty; left hand holds the pie.
"""
assert hand_ledger.lint(pkg) == [], hand_ledger.lint(pkg)
problems = hand_ledger.lint(pkg.replace("- [0-3s] Bơ slides", "- [0-3s] Bơ balances the pie on his left glove. Bơ slides"))
assert len(problems) == 1 and "pie in Bơ's left hand" in problems[0], problems
# short names: "Na" is not in "Final frame" or "banana"; ", and Grandma holds" is Grandma's clause
pkg = """### Clip 1
Hands at start — Na: right hand holds the drawing; left hand empty. Grandma: right hand holds the cane; left hand empty.
[0–3s] Na passes the drawing to Grandma, and the narrator laughs at a banana.
[3–7s] Their hands meet at the sheet, Na lets go, and Grandma holds the drawing in her left hand.
Final frame: Grandma holds the drawing up in her left hand.
Hands at end — Na: right hand empty; left hand empty. Grandma: right hand holds the cane; left hand holds the drawing.
"""
assert hand_ledger.lint(pkg) == [], hand_ledger.lint(pkg)
problems = hand_ledger.lint(pkg.replace("Final frame: Grandma holds the drawing up in her left", "Final frame: Na holds the drawing up in her left"))
assert len(problems) == 1 and "drawing in Na's left hand" in problems[0], problems
# a pass that names no receiving hand warns; the end line already says which hand
pkg = """### Clip 1
Hands at start — Bao: right hand holds the loaf; left hand empty. Mira: right hand empty; left hand empty.
[0-3s] Bao hands Mira the loaf.
Hands at end — Bao: right hand empty; left hand empty. Mira: right hand holds the loaf; left hand empty.
"""
warnings = []
assert hand_ledger.lint(pkg, warnings) == [] and len(warnings) == 1 and "Mira the loaf names no hand" in warnings[0], warnings
warnings = []
assert hand_ledger.lint(pkg.replace("the loaf.", "the loaf, and Mira takes it in her right hand."), warnings) == [] and not warnings
# a Hands line can name a prop's parts: "the baskets" are the shoulder pole
pkg = """### Clip 1
Hands at start — Ba: right hand holds the shoulder pole (with baskets); left hand empty.
[0-3s] Ba lowers the baskets to the ground with his left hand.
Hands at end — Ba: right hand holds the shoulder pole (with baskets); left hand empty.
"""
assert any("Ba's left hand" in p for p in hand_ledger.lint(pkg)), hand_ledger.lint(pkg)
assert hand_ledger.lint(pkg.replace("his left hand", "his right hand")) == []
# only the hand in the prop's own clause counts
pkg = """### Clip 1
Hands at start — Nori: right hand holds the phone; left hand empty.
[0-3s] Nori opens the fridge door with the left hand and takes out the milk tea with the right hand.
Hands at end — Nori: right hand holds the phone; left hand holds the milk tea.
"""
assert any("milk tea in Nori's right hand" in p for p in hand_ledger.lint(pkg)), hand_ledger.lint(pkg)
assert hand_ledger.lint(pkg.replace("tea with the right", "tea with the left")) == []
# either hand order, a marked time cut, a prop picked up mid-clip named with the wrong hand
pkg = """### Clip 1
Hands at start — Nori: right hand holds the phone; left hand empty.
[0-3s] Nori takes out the milk tea with the right hand.
[3-7s] She tucks the phone into her pocket.
Hands at end — Nori: right hand empty; left hand holds the milk tea.
### Clip 2
Hands at start (time cut) — Nori: left hand empty; right hand holds the milk tea.
[0-3s] Nori sips the milk tea.
Hands at end — Nori: left hand empty; right hand holds the milk tea.
"""
problems = hand_ledger.lint(pkg)
assert len(problems) == 1 and "milk tea in Nori's right hand" in problems[0], problems
# "it" is read as the prop named last before it; with no prop named yet, the lint asks for the name
pkg = """### Clip 1
Hands at start — Miso: right paw empty; left paw empty.
[0-3s] Kaka slides the blue folder to Miso. Miso catches it with her left paw.
Hands at end — Miso: right paw holds the blue folder; left paw empty.
"""
problems = hand_ledger.lint(pkg)
assert len(problems) == 1 and "(the folder) goes in the left hand" in problems[0], problems
assert hand_ledger.lint(pkg.replace("her left paw.", "her right paw.")) == []
assert hand_ledger.lint(pkg.replace("Miso catches it", "Miso blows on the folder and catches it")
                        .replace("her left paw.", "her right paw.")) == []
problems = hand_ledger.lint(pkg.replace("Kaka slides the blue folder to Miso. ", ""))
assert any("name the prop" in p for p in problems), problems

# a hand that ends empty needs a beat that lets go; "both hands" cannot use a hand that holds
# something else all clip; a prop that changes hands but is never named in the beats warns
pkg = """## Clip 1
Hands at start — Do: right hand holds the brush; left hand empty. Man: right hand empty; left hand empty.
- [0-3s] Do sets the brush down on the table, lifts the red paper with both hands and gives it to Man; Man receives the red paper with both hands.
Hands at end — Do: right hand empty; left hand empty. Man: right hand holds the red paper; left hand holds the red paper.
"""
assert hand_ledger.lint(pkg) == []
assert any("put it down" in p or "no beat" in p for p in hand_ledger.lint(pkg.replace("Do sets the brush down on the table, lifts", "Do lifts")))
kept = pkg.replace("Do sets the brush down on the table, lifts", "Do lifts").replace(
    "Hands at end — Do: right hand empty;", "Hands at end — Do: right hand holds the brush;")
assert any("both hands" in p for p in hand_ledger.lint(kept))
w = []; hand_ledger.lint(pkg.replace("the red paper; left hand holds the red paper", "the scroll; left hand holds the scroll"), w)
assert any("never name the scroll" in x for x in w), w
w = []; hand_ledger.lint(pkg.replace("Man receives the red paper with both hands", "Man takes it"), w)
assert any("names no hand" in x for x in w), w  # "with both hands" in that beat are Do's, not Man's
assert hand_ledger.mentions("drops the phone", "smartphone")
one = """## Clip 1
Hands at start — Ray: right hand holds the cereal box; left hand empty.
- [0-3s] Ray walks in and tucks the cereal box under his right arm.
Hands at end — Ray: right hand holds the cereal box; left hand empty.
"""
assert hand_ledger.lint(one) == []
assert any("left hand" in p for p in hand_ledger.lint(one.replace("under his right arm", "under his left arm")))
assert not hand_ledger.mentions("a small smug smile", "coffee mug") and hand_ledger.mentions("two mugs", "coffee mug")

# a thing picked up mid-clip that the hands lines never list must be put down again; pointing
# with the hand that holds something all clip fails; a character without hands holds nothing
lab = """Characters: Nova, a chemist. Germ, a round germ with no arms, no hands.
## Clip 1
Hands at start — Nova: right hand holds the flask; left hand empty.
- [0-3s] Nova picks up the yellow cup from the tray with her left hand. Nova sets the yellow cup back on the tray with her left hand.
- [3-7s] Nova points at the foam with her left index finger.
Hands at end — Nova: right hand holds the flask; left hand empty.
"""
assert hand_ledger.lint(lab) == [], hand_ledger.lint(lab)
assert any("no later beat puts it down" in p for p in hand_ledger.lint(lab.replace(" Nova sets the yellow cup back on the tray with her left hand.", "")))
assert any("points with the right hand" in p for p in hand_ledger.lint(lab.replace("left index finger", "right index finger")))
w = []; hand_ledger.lint(lab.replace("with her left hand. Nova sets", "with her hand. Nova sets"), w)
assert any("say which hand" in x for x in w), w
assert any("no hands" in p for p in hand_ledger.lint(lab.replace("left hand empty.\n- [0-3s]", "left hand empty. Germ: right hand holds the key; left hand empty.\n- [0-3s]")))
# the last beat with a prop sets how the clip ends; "opens her hand" lets go
assert any("last beat" in p for p in hand_ledger.lint(lab.replace("Nova points at the foam with her left index finger.", "Nova cradles the flask in both hands.")))
space = """## Clip 1
Hands at start — Lyra: right hand holds the apple; left hand empty.
- [0-3s] Lyra opens her right hand and the apple stays in mid-air.
Hands at end — Lyra: right hand empty; left hand empty.
"""
assert hand_ledger.lint(space) == [], hand_ledger.lint(space)
# "it" is a held prop only after a hold or pass verb: not "slaps it", not "between them"
five = """## Clip 1
Hands at start — Sprout: right hand empty; left hand holds the cane.
- [0-3s] Sprout leans on the cane with the left hand. Benny holds out a hand and Sprout slaps it with its right hand, a low five between them.
Hands at end — Sprout: right hand empty; left hand holds the cane.
"""
assert hand_ledger.lint(five) == [], hand_ledger.lint(five)
# an unknown name for the one thing a character holds, put in the other hand, warns
drink = space.replace("- [0-3s] Lyra opens her right hand and the apple stays in mid-air.", "- [0-3s] Lyra sips the drink in her left hand.").replace(
    "Hands at end — Lyra: right hand empty;", "Hands at end — Lyra: right hand holds the apple;")
w = []; hand_ledger.lint(drink, w)
assert any("if it is the apple" in x for x in w), w

# 3D axes as documented: facing +z, the character's right is at -x; an arm reaching forward passes
j = {"head": [0, 1.7, 0], "neck": [0, 1.5, 0], "pelvis": [0, 1, 0], "shoulder_r": [-.2, 1.45, 0],
     "elbow_r": [-.2, 1.45, .25], "wrist_r": [-.2, 1.45, .45], "shoulder_l": [.2, 1.45, 0], "elbow_l": [.2, 1.2, 0],
     "wrist_l": [.2, 1, 0], "hip_r": [-.1, 1, 0], "knee_r": [-.1, .55, .02], "ankle_r": [-.1, .1, 0],
     "toe_r": [-.1, .02, .12], "hip_l": [.1, 1, 0], "knee_l": [.1, .55, .02], "ankle_l": [.1, .1, 0], "toe_l": [.1, .02, .12]}
assert pg.check({"fps": 12, "frames": [{"joints": j}]}, "rig")["status"] == "PASS"
# 3D tracks get front-view limits too, in the pelvis's own frame: a leg spread 80° sideways fails
spread = dict(j, knee_r=[-.1 - .443, 1 - .078, .02], ankle_r=[-.1 - .886, 1 - .156, 0], toe_r=[-.1 - .886, 1 - .156, .12])
assert any("hip_abduction_r" in i["message"] for i in pg.check({"fps": 12, "frames": [{"joints": spread}]}, "rig")["issues"])
# a knee bending sideways (shin swings out while the foot still points forward) fails; a bent
# knee with the foot turned out a little at the ankle passes
side = dict(j, ankle_r=[-.1 - .3, .2, .02], toe_r=[-.1 - .3, .12, .14])
assert any("knee_lateral_r" in i["message"] for i in pg.check({"fps": 12, "frames": [{"joints": side}]}, "rig")["issues"])
bent = dict(j, knee_r=[-.1, .6, .2], ankle_r=[-.1, .2, 0], toe_r=[-.13, .12, .11])
assert not any("knee_lateral" in i["message"] for i in pg.check({"fps": 12, "frames": [{"joints": bent}]}, "rig")["issues"])
mirrored = {k: [-v[0], v[1], v[2]] for k, v in j.items()}
assert pg.check({"fps": 12, "frames": [{"joints": mirrored}]}, "rig")["status"] == "FAIL"

# front view with the drawn torso width: shoulders inside the torso outline warn
t = front_track(); j = t["frames"][3]["joints"]
assert "arm_over_body" not in kinds(pg.check(t), "warn")
sw = abs(j["shoulder_l"][0] - j["shoulder_r"][0])
t["body_width"] = sw * 0.9
assert "arm_over_body" not in kinds(pg.check(t), "warn")
t["body_width"] = sw * 1.6
assert "arm_over_body" in kinds(pg.check(t), "warn")

# a held prop (or its far end, "<prop>.<part>") over the face warns in front view
t = front_track(); f = t["frames"][3]; j = f["joints"]
f["holds"] = {"lens": "r"}; f["props"] = {"lens": list(j["wrist_r"]), "lens.glass": list(j["head"])}
assert "arm_over_face" in kinds(pg.check(t), "warn")
f["props"]["lens.glass"] = [j["wrist_r"][0], j["wrist_r"][1] + 5]
assert "arm_over_face" not in kinds(pg.check(t), "warn")

# zero gravity: with nothing touched the center of mass drifts in a straight line
t = side_track()
for i, f in enumerate(t["frames"]):
    f["airborne"] = f["zero_g"] = True
    f["joints"] = {k: [x + 3 * i, y] for k, (x, y) in f["joints"].items()}
assert "zero_g_drift" not in kinds(pg.check(t))
t["frames"][5]["joints"] = {k: [x, y - 40] for k, (x, y) in t["frames"][5]["joints"].items()}
assert "zero_g_drift" in kinds(pg.check(t))

# a knee listed as support must reach the ground
t = side_track(); f = t["frames"][0]; f["supported"] = ["knee_l"]
assert "support_floating" in kinds(pg.check(t), "warn")

# a forearm crossing the chest to grip the far side warns even while it holds something
t = front_track(); f = t["frames"][3]; j = f["joints"]
sw = abs(j["shoulder_l"][0] - j["shoulder_r"][0]); t["body_width"] = sw * 0.9
mx, ys, yp = j["neck"][0], j["shoulder_r"][1], j["pelvis"][1]
side_r = 1 if j["shoulder_r"][0] > mx else -1
j["elbow_r"] = [mx + side_r * sw * 0.3, (ys + yp) / 2]; j["wrist_r"] = [mx - side_r * sw * 0.6, (ys + yp) / 2]
f["holds"] = {"wheel": "r"}; f["props"] = {"wheel": list(j["wrist_r"])}
assert any("crosses the chest" in i["message"] for i in pg.check(t)["issues"])

# a solid prop: the head inside a block fails, hands on its face pass
t = front_track(); f = t["frames"][3]; j = f["joints"]
f["props"] = {"block": list(j["head"])}; f["solids"] = {"block": [80, 80]}
assert "body_in_prop" in kinds(pg.check(t))
f["props"]["block"] = [j["head"][0] + 400, j["head"][1]]
assert "body_in_prop" not in kinds(pg.check(t))

# a box carried in both hands sits between them; a mitten hand reaches past the wrist
t = front_track(); f = t["frames"][3]; j = f["joints"]
mid = [(j["wrist_l"][0] + j["wrist_r"][0]) / 2, (j["wrist_l"][1] + j["wrist_r"][1]) / 2]
f["holds"] = {"box": ["l", "r"]}; f["props"] = {"box": mid}
assert not any(i["kind"] in ("prop_wrong_hand", "prop_hand_switch") for i in pg.check(t)["issues"]), pg.check(t)["issues"][:3]
f["props"]["box"] = [mid[0], mid[1] + 400]
assert any(i["kind"] == "prop_wrong_hand" and i["frame"] == 3 for i in pg.check(t)["issues"])
f["holds"] = {"box": "both"}  # "both" is the same as ["l", "r"]
assert any(i["kind"] == "prop_wrong_hand" and i["frame"] == 3 for i in pg.check(t)["issues"])
f["props"]["box"] = [mid[0], mid[1] + 0.4 * ((j["neck"][1] - j["pelvis"][1]) ** 2) ** 0.5]
assert not any(i["kind"] == "prop_wrong_hand" for i in pg.check(t)["issues"])
f["props"]["box"] = [mid[0], mid[1] + 0.8 * ((j["neck"][1] - j["pelvis"][1]) ** 2) ** 0.5]
assert any(i["kind"] == "prop_wrong_hand" for i in pg.check(t)["issues"])
t["hold_tolerance"] = 0.9  # a big prop whose point sits off the grip
assert not any(i["kind"] == "prop_wrong_hand" for i in pg.check(t)["issues"])
t = front_track(); f = t["frames"][3]; j = f["joints"]
T = ((j["neck"][0] - j["pelvis"][0]) ** 2 + (j["neck"][1] - j["pelvis"][1]) ** 2) ** 0.5
dx, dy = j["wrist_r"][0] - j["elbow_r"][0], j["wrist_r"][1] - j["elbow_r"][1]; L = (dx * dx + dy * dy) ** 0.5
f["props"]["cheek"] = [j["wrist_r"][0] + dx / L * 0.4 * T, j["wrist_r"][1] + dy / L * 0.4 * T]; f["contacts"] = {"r": "cheek"}
assert "contact_miss" in kinds(pg.check(t))
t["hand_length"] = 0.4 * T
assert "contact_miss" not in kinds(pg.check(t))

# a prop the beats only look at was never passed; "fanning" names the fan; "lets go" after the prop
pkg = ("## Clip 1\nHands at start — Ba: right hand empty; left hand empty. Hu: right hand holds the red envelope; left hand empty.\n"
       "- [0-3s] Hu places the red envelope into Ba's right hand with his right hand.\n"
       "- [3-6s] Ba looks at the red envelope in her right hand, then slides her eyes to the viewer.\n"
       "Hands at end — Ba: right hand holds the red envelope; left hand empty. Hu: right hand empty; left hand empty.\n")
assert hand_ledger.lint(pkg) == [], hand_ledger.lint(pkg)
assert any("no beat passes" in p for p in hand_ledger.lint(pkg.replace("- [0-3s] Hu places the red envelope into Ba's right hand with his right hand.\n", "")))
fan = ("## Clip 1\nHands at start — Tu: right hand holds the palm-leaf fan; left hand empty.\n"
       "- [0-3s] Tu sits on the stool, fanning with his right hand.\n"
       "Hands at end — Tu: right hand holds the palm-leaf fan; left hand empty.\n")
assert hand_ledger.lint(fan) == [], hand_ledger.lint(fan)
assert any("left hand" in p for p in hand_ledger.lint(fan.replace("fanning with his right", "fanning with his left")))
# a hand that still holds the axe cannot pick up the slipper; the axe must be put down by its holder
axe = ("## Clip 1\nHands at start — Lam: right hand holds the axe; left hand holds the axe.\n"
       "- [0-3s] Lam lowers the axe.\n"
       "- [3-6s] Lam picks up the red slipper from the block with his right hand.\n"
       "Hands at end — Lam: right hand holds the red slipper; left hand empty.\n")
problems = hand_ledger.lint(axe)
assert any("still holds the axe" in p for p in problems) and any("without the axe" in p for p in problems), problems
assert hand_ledger.lint(axe.replace("Lam lowers the axe.", "Lam leans the axe against the block.")) == []
# a long prop name between "sets" and "down"
tea = ("## Clip 1\nHands at start — Vit: right hand empty; left hand holds the glass of iced tea.\n"
       "- [0-3s] Vit sets the glass of iced tea down on the table with her left hand.\n"
       "Hands at end — Vit: right hand empty; left hand empty.\n")
assert hand_ledger.lint(tea) == [], hand_ledger.lint(tea)
# a two-handed grip described hand by hand; "alone" against a two-hand ledger
broom = ("## Clip 1\nHands at start — An: right hand holds the broom; left hand empty. Tu: right hand empty; left hand empty.\n"
         "- [0-3s] An holds the broom out in his right hand.\n"
         "- [3-6s] Tu takes the broom from An in his right hand and adds his left hand above it on the handle.\n"
         "- [6-9s] Tu sweeps, holding the broom low in his right hand and high in his left hand.\n"
         "Hands at end — An: right hand empty; left hand empty. Tu: right hand holds the broom; left hand holds the broom.\n")
w = []
assert hand_ledger.lint(broom, w) == [] and w == [], (hand_ledger.lint(broom), w)
w = []
hand_ledger.lint(broom.replace(" and adds his left hand above it on the handle", "").replace(" and high in his left hand", ""), w)
assert any("in both hands" in x or "other hand" in x for x in w), w
steady = ("## Clip 1\nHands at start — An: right hand holds the broom; left hand holds the broom.\n"
          "- [0-3s] An lifts the broom in his left hand alone.\n"
          "Hands at end — An: right hand holds the broom; left hand holds the broom.\n")
assert any("alone" in p for p in hand_ledger.lint(steady))
# waving with a hand that holds something all clip
w = []
hand_ledger.lint("## Clip 1\nHands at start — Coc: right hand holds the stool; left hand holds the stool.\n"
                 "- [0-3s] Coc nods and waves at the viewer with his right hand.\n"
                 "Hands at end — Coc: right hand holds the stool; left hand holds the stool.\n", w)
assert any("waves" in x for x in w), w
# a take from someone empties their hand; a prop taken and never let go of, or let go of and still in the end line
stone = ("## Clip 1\nHands at start — Than: right hand holds the stone; left hand empty. Gach: right hand holds the mallet; left hand empty.\n"
         "- [0-3s] Than holds out the stone. Gach takes the stone from Than with her left hand. Than lowers his empty right hand.\n"
         "- [3-6s] Gach turns to the wall. Gach places the stone in the gap and lets go.\n"
         "Final frame: Gach stands at the wall with her left hand empty.\n"
         "Hands at end — Than: right hand empty; left hand empty. Gach: right hand holds the mallet; left hand empty.\n")
assert hand_ledger.lint(stone) == [], hand_ledger.lint(stone)
assert any("Than's hands end without" in p for p in hand_ledger.lint(stone.replace(" Gach takes the stone from Than with her left hand.", "")))
assert any("ends without it" in p for p in hand_ledger.lint(stone.replace("- [3-6s] Gach turns to the wall. Gach places the stone in the gap and lets go.\n", "")))
assert any("lets go of the stone" in p for p in hand_ledger.lint(stone.replace("Gach: right hand holds the mallet; left hand empty.\n", "Gach: right hand holds the mallet; left hand holds the stone.\n")))
# one big prop two characters hold together is marked "(shared)"
sheet = ("## Clip 1\nHands at start — Ba: right hand holds the paper sheet (shared); left hand holds the paper sheet (shared). "
         "Mai: right hand holds the paper sheet (shared); left hand holds the paper sheet (shared).\n"
         "- [0-3s] Ba and Mai lift the paper sheet together with both hands.\n"
         "Hands at end — Ba: right hand holds the paper sheet (shared); left hand holds the paper sheet (shared). "
         "Mai: right hand holds the paper sheet (shared); left hand holds the paper sheet (shared).\n")
assert hand_ledger.lint(sheet) == [], hand_ledger.lint(sheet)
assert any("at once" in p for p in hand_ledger.lint(sheet.replace(" (shared)", "")))
# a character outside the hands lines who has no hands
ox = ("## Clip 1\nCharacters: Lua, a farmer; Trau Da, a stone ox. Trau Da has no hands and stays out of the hands lines.\n"
      "Hands at start — Lua: right hand empty; left hand empty.\n"
      "- [0-3s] Trau Da walks along the wall, the rice bundle on its back. Lua waves at it with her right hand.\n"
      "Hands at end — Lua: right hand empty; left hand empty.\n")
assert hand_ledger.lint(ox) == [], hand_ledger.lint(ox)
assert any("Trau Da has no hands" in p for p in hand_ledger.lint(ox.replace("the rice bundle on its back", "holding the rice bundle in its right hoof")))

# "the drum stick" is not "the drum" when both are props
drum = ("## Clip 1\nHands at start — Chot: right hand holds the drum stick; left hand empty. Bo: right hand empty; left hand holds the drum.\n"
        "- [0-3s] Chot raises the drum stick in his right hand.\n"
        "Hands at end — Chot: right hand holds the drum stick; left hand empty. Bo: right hand empty; left hand holds the drum.\n")
w = []
assert hand_ledger.lint(drum, w) == [] and w == [], (hand_ledger.lint(drum), w)
assert hand_ledger.lint(drum.replace("Chot raises the drum stick in his right hand.", "Bo lifts the drum in his right hand."))

# a scene: two characters in one shot, checked against each other
import copy  # noqa: E402
a, b = front_track(), front_track()
a["name"], b["name"] = "Sol", "Kip"
for f in b["frames"]:
    f["joints"] = {k: [v[0] + 300, v[1]] for k, v in f["joints"].items()}
    f["props"], f["holds"] = {}, {}
fa, fb = a["frames"][4], b["frames"][4]
fa["contacts"] = {"r": "Kip.wrist_l"}
assert any(i["kind"] == "contact_miss" for i in pg.check_scene([a, b]))
fb["joints"]["wrist_l"] = list(fa["joints"]["wrist_r"])
assert not any(i["kind"] == "contact_miss" for i in pg.check_scene([a, b]))
c = copy.deepcopy(b); c["name"] = "Vex"
for f in c["frames"]:
    f["joints"] = {k: [v[0] - 295, v[1]] for k, v in f["joints"].items()}
assert any(i["kind"] == "head_overlap" for i in pg.check_scene([a, c]))
# one character's raised ball over the other's face
d = copy.deepcopy(b); fd = d["frames"][4]
fa["holds"], fa["props"] = {"ball": "r"}, {"ball": list(fd["joints"]["head"])}
assert any(i["kind"] == "face_covered" for i in pg.check_scene([a, d]))
fa["holds"], fa["props"] = {}, {}
# both characters hold the prop at the hand-off frame: their hands must meet
e = copy.deepcopy(b); fe = e["frames"][4]
fa["holds"], fe["holds"], fa["handoff"] = {"slipper": "r"}, {"slipper": "l"}, True
fe["joints"]["wrist_l"] = [fa["joints"]["wrist_r"][0] + 200, fa["joints"]["wrist_r"][1]]
assert any(i["kind"] == "handoff_gap" for i in pg.check_scene([a, e]))
fe["joints"]["wrist_l"] = list(fa["joints"]["wrist_r"])
assert not any(i["kind"] == "handoff_gap" for i in pg.check_scene([a, e]))
fa["holds"], fa["handoff"] = {}, False
# a prop handed from one character to the other must not jump between their hands
a, b = front_track(), front_track()
a["name"], b["name"] = "Sol", "Kip"
for i, (f, g) in enumerate(zip(a["frames"], b["frames"])):
    g["joints"] = {k: [v[0] + 300, v[1]] for k, v in g["joints"].items()}
    f["holds"], g["holds"] = ({"cup": "r"}, {}) if i < 5 else ({}, {"cup": "l"})
    f["props"] = {"cup": f["joints"]["wrist_r"]} if i < 5 else {}
    g["props"] = {"cup": g["joints"]["wrist_l"]} if i >= 5 else {}
assert any(i["kind"] == "handoff_gap" and i["frame"] == 5 for i in pg.check_scene([a, b]))
# a snout reaching into the other character's head; bodies as solids
a, b = front_track(), front_track()
a["name"], b["name"] = "Vit", "Heo"
for f, g in zip(a["frames"], b["frames"]):
    f["facing"] = "right"; f["holds"], f["props"] = {}, {}
    g["joints"] = {k: [v[0] + 3.2 * a.get("head_radius", 20), v[1]] for k, v in g["joints"].items()}
    g["holds"], g["props"] = {}, {}
r = pg.check_scene([a, b])
hr = pg.check_scene([a, b])
assert not any("snout" in i["message"] for i in hr)
a["snout"] = 2.5 * (a.get("head_radius") or 20)
gap = abs(b["frames"][0]["joints"]["head"][0] - a["frames"][0]["joints"]["head"][0])
a["snout"] = gap  # the snout tip reaches the other head's centre
assert any("snout" in i["message"] for i in pg.check_scene([a, b]))
b["frames"][2]["overlap_ok"] = True
assert not any("snout" in i["message"] and i["frame"] == 2 for i in pg.check_scene([a, b]))
del b["frames"][2]["overlap_ok"]
# a snout aimed down ("snout_dir") into the other character's chest, under its head
jb0, ja0 = b["frames"][0]["joints"], a["frames"][0]["joints"]
chest = [(jb0["neck"][0] + jb0["pelvis"][0]) / 2, (jb0["neck"][1] + jb0["pelvis"][1]) / 2]
d = [chest[0] - ja0["head"][0], chest[1] - ja0["head"][1]]
a["snout"], a["snout_dir"] = (d[0] ** 2 + d[1] ** 2) ** 0.5, d
assert any("snout pokes into Heo's body" in i["message"] and i["frame"] == 0 for i in pg.check_scene([a, b]))
del a["snout"], a["snout_dir"]
assert not any(i["kind"] == "body_overlap" for i in pg.check_scene([a, b]))
for f in b["frames"]:
    f["joints"] = {k: [v[0] - 2.8 * (a.get("head_radius") or 20), v[1]] for k, v in f["joints"].items()}
a["solid_body"] = b["solid_body"] = True
assert any(i["kind"] == "body_overlap" for i in pg.check_scene([a, b]))
del b["solid_body"]
assert not any(i["kind"] == "body_overlap" for i in pg.check_scene([a, b]))

# a tilted torso is measured across its own axis: a rocking roly-poly's shoulder is on its edge
t = front_track()
for f in t["frames"]:
    f.pop("holds", None); f.pop("props", None)
t["body_width"] = 2 * abs(t["frames"][0]["joints"]["shoulder_l"][0] - t["frames"][0]["joints"]["neck"][0]) / 0.9
base = [i for i in pg.check(t)["issues"] if "shoulder sits inside" in i["message"]]
import math as _m  # noqa: E402
for f in t["frames"]:
    n0 = f["joints"]["neck"]; c, s_ = _m.cos(_m.radians(30)), _m.sin(_m.radians(30))
    f["joints"] = {k: [n0[0] + (v[0] - n0[0]) * c - (v[1] - n0[1]) * s_, n0[1] + (v[0] - n0[0]) * s_ + (v[1] - n0[1]) * c]
                   for k, v in f["joints"].items()}
assert len([i for i in pg.check(t)["issues"] if "shoulder sits inside" in i["message"]]) == len(base)

# a supported wrist off the floor in a crouch warns; listing "floor" checks the seat too
t = side_track(); f = t["frames"][2]; j = f["joints"]
ys = [v[1] for v in j.values()]; ground, tall = max(ys), max(ys) - min(ys)
j["wrist_r"] = [j["wrist_r"][0], ground - 0.3 * tall]
f["supported"] = ["ankle_l", "ankle_r", "wrist_r"]
assert any(i["kind"] == "support_floating" and "wrist_r" in i["joints"] for i in pg.check(t)["issues"])
f["supported"] = ["wrist_r"]  # a lone wrist can push a wall
assert not any(i["kind"] == "support_floating" for i in pg.check(t)["issues"])
f["supported"] = ["pelvis"]  # a lone pelvis sits on a chair
assert not any(i["kind"] == "support_floating" for i in pg.check(t)["issues"])
f["supported"] = ["pelvis", "floor"]
assert any(i["kind"] == "support_floating" and "pelvis" in i["joints"] for i in pg.check(t)["issues"])

# --scene --json: a scene error fails the clip of each character it names, not only the scene
import json as _json, tempfile as _tf  # noqa: E402
a, b = front_track(), front_track()
a["name"], b["name"] = "Sol", "Kip"
for f in b["frames"]:
    f["joints"] = {k: [v[0] + 5, v[1]] for k, v in f["joints"].items()}
    f["props"], f["holds"] = {}, {}
for f in a["frames"]:
    f["props"], f["holds"] = {}, {}
with _tf.TemporaryDirectory() as d:
    pa, pb = Path(d) / "a.json", Path(d) / "b.json"
    pa.write_text(_json.dumps(a)); pb.write_text(_json.dumps(b))
    out = subprocess.run([sys.executable, str(GATE / "posture_gate.py"), "check", "--scene", "--json", pa, pb],
                         capture_output=True, text=True)
    res = _json.loads(out.stdout)
    assert out.returncode == 1 and not res["passed"]
    assert all(c["status"] == "FAIL" and c["scene_issues"] for c in res["clips"]), res["clips"]

# a projected 3D arm swinging through the camera axis pops only as a warning
def arm_jump(i, a, f):
    if i == 6:
        a["abd_l"] += 150
t = ex.track(ex.front_frames(arm_jump), rest=ex.front_pose(ex.wave(0)))
assert "pop" in kinds(pg.check(t))
t["projected"] = True
assert "pop" not in kinds(pg.check(t)) and "pop" in kinds(pg.check(t), "warn")

# grip points copied from the wrists warn, unless the two grips sit one behind the other
def two_hand_grips(stack):
    t = ex.track(ex.front_frames(), rest=ex.front_pose(ex.wave(0)))
    for f in t["frames"]:
        j = f["joints"]
        if stack:
            j["wrist_r"] = [j["wrist_l"][0] + 1, j["wrist_l"][1]]
        f["holds"] = {"cup": "both"}
        f["props"] = {"cup": [(a + b) / 2 for a, b in zip(j["wrist_l"], j["wrist_r"])],
                      "cup.l": list(j["wrist_l"]), "cup.r": list(j["wrist_r"])}
    return [i for i in pg.check(t)["issues"] if "wrist itself" in i["message"]]
assert two_hand_grips(False) and not two_hand_grips(True)

# "Two-hand props:" / "Two-hand holders:" lines: a one-hand hold of a declared prop or by a declared holder fails
brick = ("### Clip 1\nTwo-hand props: red brick.\nProps: one red brick.\n"
         "Hands at start — Vua: right hand holds the red brick; left hand holds the red brick. "
         "Nut: right hand empty; left hand empty.\n"
         "- [0-3s] Vua sets the red brick onto the wall, presses it down and lets go.\n"
         "- [3-7s] Nut picks up the red brick with both hands.\n"
         "- [7-10s] Nut holds the red brick out with both hands.\n"
         "Hands at end — Vua: right hand empty; left hand empty. "
         "Nut: right hand holds the red brick; left hand holds the red brick.\n")
assert hand_ledger.lint(brick) == [], hand_ledger.lint(brick)
assert any("declared two-handed" in p for p in hand_ledger.lint(
    brick.replace("picks up the red brick with both hands", "picks up the red brick with his right hand")))
assert any("declared two-handed" in p for p in hand_ledger.lint(
    brick.replace("Nut: right hand holds the red brick; left hand holds the red brick.",
                  "Nut: right hand holds the red brick; left hand empty.")))
plush = ("### Clip 1\nTwo-hand holders: Bong.\nProps: one red block.\n"
         "Hands at start — Kit: right hand empty; left hand empty. Bong: right paw empty; left paw empty.\n"
         "- [0-3s] Bong catches the red block against his belly with both paws.\n"
         "- [3-7s] Bong holds the red block out in both paws. Kit takes the red block from Bong with both hands.\n"
         "Hands at end — Kit: right hand holds the red block; left hand holds the red block. "
         "Bong: right paw empty; left paw empty.\n")
assert hand_ledger.lint(plush) == [], hand_ledger.lint(plush)
assert any("declared two-handed" in p for p in hand_ledger.lint(
    plush.replace("against his belly with both paws", "in his right paw")))

# a take "from" someone empties their hand: the end line may not keep the prop there
mug = ("### Clip 1\nProps: one blue mug.\n"
       "Hands at start — Kit: right hand empty; left hand empty. Mo: right hand holds the blue mug; left hand empty.\n"
       "- [0-3s] Kit takes the blue mug from Mo with his right hand.\n"
       "Hands at end — Kit: right hand holds the blue mug; left hand empty. Mo: right hand empty; left hand empty.\n")
assert hand_ledger.lint(mug) == [], hand_ledger.lint(mug)
assert any("Mo lets go of the blue mug" in p for p in hand_ledger.lint(
    mug.replace("Mo: right hand empty; left hand empty.\n", "Mo: right hand holds the blue mug; left hand empty.\n")))

# placing a prop counts as letting go; placing one still in someone else's hand misses the take;
# a no-hands animal holds nothing in a hoof, sided ("right front hoof") or not
gap = ("### Clip 1\nProps: one stone block.\n"
       "Hands at start — Than: right hand holds the stone block; left hand empty. Gach: right hand empty; left hand empty.\n"
       "- [0-3s] Gach takes the stone block from Than with her left hand. Than lowers his empty right hand.\n"
       "- [3-7s] Gach places the stone block in the gap and lets go.\n"
       "Hands at end — Than: right hand empty; left hand empty. Gach: right hand empty; left hand empty.\n")
assert hand_ledger.lint(gap) == [], hand_ledger.lint(gap)
assert any("add the beat where Gach takes it" in p for p in hand_ledger.lint(
    gap.replace(" Gach takes the stone block from Than with her left hand. Than lowers his empty right hand.", "")
       .replace("Hands at end — Than: right hand empty;", "Hands at end — Than: right hand holds the stone block;")))
assert any("Gach lets go of the stone block" in p for p in hand_ledger.lint(
    gap.replace("in the gap and lets go", "in the gap")
       .replace("Gach: right hand empty; left hand empty.\n", "Gach: right hand empty; left hand holds the stone block.\n")
       .replace("Gach: right hand empty; left hand holds the stone block.\n- [0-3s]", "Gach: right hand empty; left hand empty.\n- [0-3s]")))
relift = gap.replace("in the gap and lets go.", "on the table.\n- [7-10s] Gach lifts the stone block again with her left hand.") \
    .replace("Gach: right hand empty; left hand empty.\n", "Gach: right hand empty; left hand holds the stone block.\n") \
    .replace("Gach: right hand empty; left hand holds the stone block.\n- [0-3s]", "Gach: right hand empty; left hand empty.\n- [0-3s]")
assert hand_ledger.lint(relift) == [], hand_ledger.lint(relift)
ox = ("### Clip 1\nTrau, a stone buffalo with no hands. Lua, a farmer.\n"
      "Hands at start — Lua: right hand empty; left hand empty.\n"
      "- [0-3s] Trau walks along the wall, the rice bundle steady on its back.\n"
      "Hands at end — Lua: right hand empty; left hand empty.\n")
assert hand_ledger.lint(ox) == [], hand_ledger.lint(ox)
for bad in ("the rice bundle held in its right front hoof", "the rice bundle steady on its back. Trau grips the rice bundle in its hoof"):
    assert any("Trau has no hands" in p for p in hand_ledger.lint(ox.replace("the rice bundle steady on its back", bad))), bad
assert hand_ledger.lint("### Clip 1\nHands at start — Bo: right front hoof empty; left front hoof empty.\n"
                        "Hands at end — Bo: right front hoof empty; left front hoof empty.\n") == []

# four-legged tracks (points at the frame's top level) are read: bones, legs, pops, a stick tail
def cat(i, sit=False):
    j = {"hip": [100, 50], "shoulder": [60, 50], "neck": [52, 42], "head": [45, 36],
         "tail0": [106, 46], "tail1": [112, 44], "tail2": [118, 46]}
    for g, x in (("fl", 60), ("fr", 58), ("hl", 100), ("hr", 98)):
        swing = 4 * math.sin(i / 3 + (0 if g in ("fl", "hr") else math.pi))
        j[f"{g}_mid"] = [x + swing / 2 + (2 if g[0] == "f" else -2), 62]
        j[f"{g}_paw"] = [x + swing, 74]
    if sit:
        j["tail0"], j["tail1"], j["tail2"] = [101, 40], [102, 28], [103, 16]
    return j
q = {"character": "Mup", "fps": 12, "frames": [cat(i) for i in range(12)]}
assert pg.check(q)["passed"] and not pg.check(q)["issues"], pg.check(q)["issues"][:3]
q["frames"][5] = dict(cat(5), fl_paw=[60, 90])
assert "bone_stretch" in kinds(pg.check(q))
q["frames"][5] = {k: v for k, v in cat(5).items() if k != "hr_paw"}
assert "leg_missing" in kinds(pg.check(q))
q["frames"][5] = dict(cat(5), tail1=[100, 56], tail2=[94, 52])
assert "pop" in kinds(pg.check(q))
q["frames"] = [cat(i, sit=True) for i in range(12)]
assert "tail_like_leg" in kinds(pg.check(q), "warn")
person = front_track(); person["name"] = "An"
q = {"name": "Mup", "frames": [cat(i) for i in range(12)]}
assert isinstance(pg.check_scene([person, q]), list)

# a big prop two holders grip at opposite edges passes the hand-off when each lists its grip points
a, b = front_track(), front_track()
a["name"], b["name"] = "Hank", "Nova"
for fa, fb in zip(a["frames"], b["frames"]):
    fb["joints"] = {k: [v[0] + 120, v[1]] for k, v in fa["joints"].items()}
    c = [(fa["joints"]["wrist_l"][0] + fb["joints"]["wrist_r"][0]) / 2, fa["joints"]["wrist_l"][1]]
    fa["holds"] = fb["holds"] = {"gear": "both"}
    fa["props"], fb["props"] = {"gear": c}, {"gear": c}
assert any(i["kind"] == "handoff_gap" and "gear.l" in i["message"] for i in pg.check_scene([a, b]))
for t in (a, b):
    for f in t["frames"]:
        f["props"].update({"gear.l": f["joints"]["wrist_l"], "gear.r": f["joints"]["wrist_r"]})
assert not any(i["kind"] == "handoff_gap" for i in pg.check_scene([a, b]))

# the skill points at the gate
skill = (ROOT / "skills/directing-stickman-videos/SKILL.md").read_text()
contract = (ROOT / "skills/directing-stickman-videos/references/omni-flash-prompt-contract.md").read_text()
assert "references/posture-gate.md" in skill
assert "Hands at start" in contract and "Hands at end" in contract

print("posture gate checks passed")
