#!/usr/bin/env python3
"""Build example rig pose tracks: one clean walk cycle and one track per common posture bug.

Writes examples/*.json next to this file. Used by tests/verify-posture-gate.py and the README images.
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEN = {"torso": 60, "head": 22, "upper_arm": 30, "forearm": 28, "thigh": 36, "shin": 34, "foot": 12}


def rot(v, deg):
    a = math.radians(deg)
    return (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a))

def add(p, v, k): return (p[0] + v[0] * k, p[1] + v[1] * k)


def pose(a, x=200.0, ground=300.0, stretch=None):
    """Forward kinematics for a side-view stick figure facing right. Angles in degrees:
    lean (torso forward), neck (+ = chin down), shoulder/hip (+ = forward),
    elbow (+ = fold), knee (+ = fold), ankle (+ = toes up)."""
    stretch = stretch or {}
    L = {k: v * stretch.get(k, 1.0) for k, v in LEN.items()}
    up = rot((0, 1), -a.get("lean", 0))
    down = (-up[0], -up[1])
    pelvis = (0.0, 0.0)
    neck = add(pelvis, up, L["torso"])
    j = {"pelvis": pelvis, "neck": neck, "head": add(neck, rot(up, -a.get("neck", 0)), L["head"])}
    for s in ("l", "r"):
        ua = rot(down, a[f"shoulder_{s}"]); fa = rot(ua, a[f"elbow_{s}"])
        th = rot(down, a[f"hip_{s}"]); sh = rot(th, -a[f"knee_{s}"]); ft = rot(sh, 90 + a.get(f"ankle_{s}", 0))
        j[f"shoulder_{s}"] = neck
        j[f"elbow_{s}"] = add(neck, ua, L["upper_arm"]); j[f"wrist_{s}"] = add(j[f"elbow_{s}"], fa, L["forearm"])
        j[f"hip_{s}"] = pelvis
        j[f"knee_{s}"] = add(pelvis, th, L["thigh"]); j[f"ankle_{s}"] = add(j[f"knee_{s}"], sh, L["shin"])
        j[f"toe_{s}"] = add(j[f"ankle_{s}"], ft, L["foot"])
    low = min(min(j[f"ankle_{s}"][1], j[f"toe_{s}"][1]) for s in ("l", "r"))
    # image coordinates (y down), feet on the ground line
    return {k: [round(x + p[0], 2), round(ground - (p[1] - low), 2)] for k, p in j.items()}


def walk(t):
    ph = 2 * math.pi * t
    a = {"lean": 4, "neck": 4}
    for s, off in (("l", 0), ("r", math.pi)):
        a[f"hip_{s}"] = 22 * math.sin(ph + off)
        a[f"knee_{s}"] = 8 + 40 * max(0.0, math.sin(ph + off + 1.2))
        a[f"ankle_{s}"] = 8 * math.sin(ph + off)
        a[f"shoulder_{s}"] = -20 * math.sin(ph + off)
        a[f"elbow_{s}"] = 25 + 10 * math.sin(ph + off)
    return a


def track(frames, **meta):
    return {"source": "rig", "profile": "rig", "fps": 12, "rest": pose(walk(0.0)), **meta, "frames": frames}


def frames_with(bug=None, n=12):
    out = []
    for i in range(n):
        a, kw, f = walk(i / n), {}, {"facing": "right"}
        if bug:
            bug(i, a, kw, f)
        f["joints"] = pose(a, x=200 + 6 * i, **kw)
        out.append(f)
    return out


def knee_backward(i, a, kw, f):
    if 4 <= i <= 7: a["knee_r"] = -35          # shin folds forward: a knee bending the wrong way

def elbow_backward(i, a, kw, f):
    if 3 <= i <= 6: a["elbow_l"] = -45         # forearm folds backward past straight

def rubber_arm(i, a, kw, f):
    if 5 <= i <= 8: kw["stretch"] = {"forearm": 1.45, "upper_arm": 1.25}   # limbs stretching like rubber

def pop(i, a, kw, f):
    if i == 6: a["shoulder_l"] += 150          # one frame where the arm teleports

def topple(i, a, kw, f):
    a["lean"] = 55; a["hip_l"] = a["hip_r"] = 0; a["knee_l"] = a["knee_r"] = 0   # standing, leaning far forward

def head_backward(i, a, kw, f):
    if i >= 6: a["neck"] = -120                # head bent backward far past the neck limit


# ---- front view (character faces the camera: its left side is on screen right) ----
def front_pose(a, x=200.0, ground=300.0):
    """abd_* = arm/leg raised out sideways (+ = away from body), elb_* = elbow fold toward the body."""
    pelvis = (0.0, 0.0); neck = (0.0, LEN["torso"])
    j = {"pelvis": pelvis, "neck": neck, "head": (0.0, LEN["torso"] + LEN["head"])}
    for s, out in (("l", 1), ("r", -1)):
        sh = (out * 14.0, LEN["torso"] - 4); hp = (out * 9.0, 0.0)
        ua = rot((0, -1), out * a[f"abd_{s}"]); fa = rot(ua, -out * a[f"elb_{s}"])
        th = rot((0, -1), out * a.get(f"leg_{s}", 6))
        j[f"shoulder_{s}"] = sh; j[f"elbow_{s}"] = add(sh, ua, LEN["upper_arm"])
        j[f"wrist_{s}"] = add(j[f"elbow_{s}"], fa, LEN["forearm"])
        j[f"hip_{s}"] = hp; j[f"knee_{s}"] = add(hp, th, LEN["thigh"])
        j[f"ankle_{s}"] = add(j[f"knee_{s}"], th, LEN["shin"])
        j[f"toe_{s}"] = add(j[f"ankle_{s}"], (out * 4.0, -3.0), 1)
    low = min(j[f"toe_{s}"][1] for s in ("l", "r"))
    return {k: [round(x + p[0], 2), round(ground - (p[1] - low), 2)] for k, p in j.items()}


def wave(t):
    # right hand raised and waving, left hand down holding a cup
    return {"abd_r": 150 + 15 * math.sin(2 * math.pi * t * 2), "elb_r": 30, "abd_l": 12, "elb_l": 70}


def front_frames(bug=None, n=12):
    out = []
    for i in range(n):
        a, f = wave(i / n), {"facing": "front", "holds": {"cup": "l"}}
        if bug:
            bug(i, a, f)
        f["joints"] = j = front_pose(a)
        side = f["holds"]["cup"]
        f.setdefault("props", {})["cup"] = f.get("_cup_at") or j[f"wrist_{side}"]
        f.pop("_cup_at", None)
        if "_swap" in f:  # generated video drew each hand where the other should be
            j["elbow_l"], j["elbow_r"], j["wrist_l"], j["wrist_r"] = j["elbow_r"], j["elbow_l"], j["wrist_r"], j["wrist_l"]
            del f["_swap"]
        if "_flip" in f:  # upper body turned around against the legs
            for k in ("shoulder", "elbow", "wrist"):
                j[f"{k}_l"], j[f"{k}_r"] = j[f"{k}_r"], j[f"{k}_l"]
            del f["_flip"]
        out.append(f)
    return out


def hand_swap(i, a, f):
    if i in (5, 6): f["_swap"] = True; f["props"] = {}

def torso_flip(i, a, f):
    if i >= 6: f["_flip"] = True; f["props"] = {}

def cup_switches_hand(i, a, f):
    if i >= 6: f["holds"] = {"cup": "r"}; a["abd_r"], a["elb_r"] = 12, 70; a["abd_l"], a["elb_l"] = 150, 30

def cup_in_wrong_hand(i, a, f):
    if i >= 4: f["_cup_at"] = front_pose(a)["wrist_r"]   # script says left hand, picture shows it in the right

def mirrored_hand(i, a, f):
    f["hands"] = {"l": {"looks_like": "l", "score": 0.95}, "r": {"looks_like": "r", "score": 0.94}}
    if i >= 7: f["hands"]["r"] = {"looks_like": "l", "score": 0.91}   # a left hand drawn on the right arm


FRONT = {"hand_swap": hand_swap, "torso_flip": torso_flip, "cup_switches_hand": cup_switches_hand,
         "cup_in_wrong_hand": cup_in_wrong_hand, "mirrored_hand": mirrored_hand}


def two_clips():
    """Clip 1 ends with the cup in the left hand; clip 2 opens with it in the right hand."""
    c1 = front_frames()
    c2 = front_frames(lambda i, a, f: cup_switches_hand(99, a, f))
    return track(c1, name="clip1_cup_left", rest=front_pose(wave(0))), \
        track(c2, name="clip2_cup_right", rest=front_pose(wave(0)))


EXAMPLES = {
    "walk_clean": None, "knee_backward": knee_backward, "elbow_backward": elbow_backward,
    "rubber_arm": rubber_arm, "arm_pop": pop, "topple": topple, "head_backward": head_backward,
}


if __name__ == "__main__":
    for name, bug in EXAMPLES.items():
        (HERE / f"{name}.json").write_text(json.dumps(track(frames_with(bug), name=name), indent=1))
    for name, bug in {"front_clean": None, **FRONT}.items():
        t = track(front_frames(bug), name=name, rest=front_pose(wave(0)))
        (HERE / f"{name}.json").write_text(json.dumps(t, indent=1))
    for t in two_clips():
        (HERE / f"{t['name']}.json").write_text(json.dumps(t, indent=1))
    print("wrote", len(list(HERE.glob("*.json"))), "example tracks to", HERE)
