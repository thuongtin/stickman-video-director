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
assert w == [], w  # the receiving hands are named in the first sentence ("with both hands")
assert hand_ledger.mentions("drops the phone", "smartphone")

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
# a prop handed from one character to the other must not jump between their hands
a, b = front_track(), front_track()
a["name"], b["name"] = "Sol", "Kip"
for i, (f, g) in enumerate(zip(a["frames"], b["frames"])):
    g["joints"] = {k: [v[0] + 300, v[1]] for k, v in g["joints"].items()}
    f["holds"], g["holds"] = ({"cup": "r"}, {}) if i < 5 else ({}, {"cup": "l"})
    f["props"] = {"cup": f["joints"]["wrist_r"]} if i < 5 else {}
    g["props"] = {"cup": g["joints"]["wrist_l"]} if i >= 5 else {}
assert any(i["kind"] == "handoff_gap" and i["frame"] == 5 for i in pg.check_scene([a, b]))

# the skill points at the gate
skill = (ROOT / "skills/directing-stickman-videos/SKILL.md").read_text()
contract = (ROOT / "skills/directing-stickman-videos/references/omni-flash-prompt-contract.md").read_text()
assert "references/posture-gate.md" in skill
assert "Hands at start" in contract and "Hands at end" in contract

print("posture gate checks passed")
