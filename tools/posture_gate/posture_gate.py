#!/usr/bin/env python3
"""Posture gate: reject anatomically impossible or broken character poses.

Works on a pose track (JSON of 2D joint positions per frame) from either
  * a code-rendered rig (exact joints, strict "rig" profile), or
  * a pose estimator run on generated frames (estimate_pose.py, "video" profile).

Usage:
  posture_gate.py check track.json [more clips in order...] [--profile rig|pixel|video] [--report DIR]
  posture_gate.py fix   track.json -o fixed.json

Exit code 0 = pass (or REVIEW: video-profile errors sent to a human, see --strict),
1 = at least one blocking error, 2 = bad input.
Only the Python standard library is needed.
"""
import argparse
import json
import math
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIMITS = json.loads((HERE / "joint_limits.json").read_text())
SIDES = ("l", "r")

# (name, pivot, parent vector (a, b), child vector (a, b), sign, descendants)
# Angles are measured in the character's frame, mirrored so it always faces +x,
# y up.  value = sign * signed angle from parent vector to child vector.
def _sagittal_joints(s):
    torso_down = ("neck", "pelvis")
    return [
        ("shoulder", f"shoulder_{s}", torso_down, (f"shoulder_{s}", f"elbow_{s}"), 1,
         [f"elbow_{s}", f"wrist_{s}"]),
        ("elbow", f"elbow_{s}", (f"shoulder_{s}", f"elbow_{s}"), (f"elbow_{s}", f"wrist_{s}"), 1,
         [f"wrist_{s}"]),
        ("hip", f"hip_{s}", torso_down, (f"hip_{s}", f"knee_{s}"), 1,
         [f"knee_{s}", f"ankle_{s}", f"heel_{s}", f"toe_{s}"]),
        ("knee", f"knee_{s}", (f"hip_{s}", f"knee_{s}"), (f"knee_{s}", f"ankle_{s}"), -1,
         [f"ankle_{s}", f"heel_{s}", f"toe_{s}"]),
        ("ankle", f"ankle_{s}", (f"knee_{s}", f"ankle_{s}"), (f"ankle_{s}", f"toe_{s}"), 1,
         [f"toe_{s}", f"heel_{s}"]),
    ]

NECK = ("neck", "neck", ("pelvis", "neck"), ("neck", "head"), -1, ["head"])
ANKLE_OFFSET = 90  # a foot at right angles to the shin is neutral

BONES = [("pelvis", "neck"), ("neck", "head")] + [
    b for s in SIDES for b in [
        (f"shoulder_{s}", f"elbow_{s}"), (f"elbow_{s}", f"wrist_{s}"),
        (f"hip_{s}", f"knee_{s}"), (f"knee_{s}", f"ankle_{s}"), (f"ankle_{s}", f"toe_{s}")]
]

# Segment mass fractions (Winter, Biomechanics and Motor Control of Human Movement).
MASS = [(("neck", "head"), 0.081), (("pelvis", "neck"), 0.497)] + [
    m for s in SIDES for m in [
        ((f"shoulder_{s}", f"elbow_{s}"), 0.028), ((f"elbow_{s}", f"wrist_{s}"), 0.022),
        ((f"hip_{s}", f"knee_{s}"), 0.100), ((f"knee_{s}", f"ankle_{s}"), 0.061)]
]


# ---------- geometry ----------
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def norm(v): return math.sqrt(sum(x * x for x in v))
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def unit(v):
    n = norm(v)
    return tuple(x / n for x in v) if n > 1e-9 else None

def signed(p, c):
    """Signed angle in degrees from vector p to vector c, counter-clockwise positive (y up)."""
    return math.degrees(math.atan2(p[0] * c[1] - p[1] * c[0], p[0] * c[0] + p[1] * c[1]))

def wrap(a): return (a + 180) % 360 - 180

def arc_violation(v, lo, hi):
    """Degrees by which angle v lies outside the arc lo..hi (handles wrap-around)."""
    span = hi - lo
    if wrap(v - lo) % 360 <= span:
        return 0.0
    return min(abs(wrap(v - lo)), abs(wrap(v - hi)))

def rotate(pt, pivot, deg):
    a = math.radians(deg)
    x, y = pt[0] - pivot[0], pt[1] - pivot[1]
    return (pivot[0] + x * math.cos(a) - y * math.sin(a), pivot[1] + x * math.sin(a) + y * math.cos(a))


# ---------- 3D tracks ----------
def is_3d(track):
    return any(v is not None and len(v) == 3 for f in track["frames"] for v in f["joints"].values())


def to_2d(track):
    """Project a 3D rig track onto each frame's own side view (the body's sagittal plane),
    so a limb pointing at a camera never looks short or bent. True 3D bone lengths, joints
    and props are kept for the length and left/right checks. Coordinates: "up_axis"
    (default [0, 1, 0]) is up; the character's right is +x when it faces +z, as in
    Blender/three.js. A left-handed engine (Unity) sets "handedness": "left"."""
    up = unit(tuple(float(x) for x in track.get("up_axis", (0, 1, 0))))
    hand = -1 if track.get("handedness") == "left" else 1
    out = json.loads(json.dumps(track))
    out.pop("rest", None)  # rest lengths come from 3D below
    for f in out["frames"]:
        j = {k: tuple(float(c) for c in v) for k, v in f["joints"].items() if v is not None and len(v) == 3}
        for mid, a, b in (("neck", "shoulder_l", "shoulder_r"), ("pelvis", "hip_l", "hip_r")):
            if mid not in j and a in j and b in j:
                j[mid] = tuple((x + y) / 2 for x, y in zip(j[a], j[b]))
        lat = None
        for a, b in (("hip_r", "hip_l"), ("shoulder_r", "shoulder_l")):
            if a in j and b in j:
                v = sub(j[a], j[b]); v = tuple(x - dot(v, up) * u for x, u in zip(v, up))
                lat = unit(v)
                if lat:
                    break
        if lat is None or "pelvis" not in j:
            f["joints"] = {}
            continue
        fwd = tuple(hand * x for x in cross(up, lat))
        o = j["pelvis"]
        f["joints"] = {k: [round(dot(sub(p, o), fwd), 3), round(-dot(sub(p, o), up), 3)] for k, p in j.items()}
        f["facing"] = "right"
        f["_joints3d"] = {k: list(p) for k, p in j.items()}
        f["_len3d"] = {f"{a}>{b}": norm(sub(j[a], j[b])) for a, b in BONES if a in j and b in j}
        props = {k: tuple(float(c) for c in v) for k, v in f.get("props", {}).items() if len(v) == 3}
        if props:
            f["_props3d"] = {k: list(p) for k, p in props.items()}
            f["props"] = {k: [round(dot(sub(p, o), fwd), 3), round(-dot(sub(p, o), up), 3)] for k, p in props.items()}
        # head yaw: nose direction against the body's forward, both flattened onto the ground
        if "nose" in j and "head" in j:
            n = sub(j["nose"], j["head"]); n = unit(tuple(x - dot(n, up) * u for x, u in zip(n, up)))
            if n:
                f["_yaw"] = math.degrees(math.atan2(dot(n, lat), dot(n, fwd)))
    return out


# ---------- track loading ----------
def load_frame(frame, min_conf):
    """Joints in y-up, mirrored so the character faces +x. Derives neck/pelvis if missing."""
    conf = frame.get("conf", {})
    pts = {k: (float(v[0]), -float(v[1])) for k, v in frame["joints"].items()
           if v is not None and conf.get(k, 1.0) >= min_conf}
    for mid, a, b in (("neck", "shoulder_l", "shoulder_r"), ("pelvis", "hip_l", "hip_r")):
        if mid not in pts and a in pts and b in pts:
            pts[mid] = ((pts[a][0] + pts[b][0]) / 2, (pts[a][1] + pts[b][1]) / 2)
    facing = frame.get("facing") or infer_facing(pts)
    if facing == "left":
        pts = {k: (-x, y) for k, (x, y) in pts.items()}
    return pts, facing

def infer_facing(pts):
    dx, n, shin = 0.0, 0, []
    for s in SIDES:
        if f"toe_{s}" in pts and f"ankle_{s}" in pts:
            dx += pts[f"toe_{s}"][0] - pts[f"ankle_{s}"][0]; n += 1
        if f"knee_{s}" in pts and f"ankle_{s}" in pts:
            shin.append(norm(sub(pts[f"knee_{s}"], pts[f"ankle_{s}"])))
    if n and shin and abs(dx / n) > 0.25 * max(shin):
        return "right" if dx > 0 else "left"
    if all(k in pts for k in ("shoulder_l", "shoulder_r", "neck", "pelvis")):
        width = norm(sub(pts["shoulder_l"], pts["shoulder_r"]))
        torso = norm(sub(pts["neck"], pts["pelvis"]))
        if torso and width / torso < 0.35:
            return "side"  # side view, direction unknown: only unsigned checks
    return "front"

def vec(pts, ab):
    a, b = ab
    if a in pts and b in pts:
        v = sub(pts[b], pts[a])
        if norm(v) > 1e-6:
            return v
    return None


# ---------- per-frame angles ----------
def merged_limits(track):
    """Joint limits with the track's own overrides, e.g. {"sagittal": {"hip": {"max": 170}}} for a dancer."""
    lim = json.loads(json.dumps(LIMITS))
    for view, joints in track.get("limits_override", {}).items():
        for j, v in joints.items():
            lim[view].setdefault(j, {}).update(v)
    return lim


def frame_angles(pts, facing, limits=LIMITS):
    """Returns {joint_name: (value, lo, hi, involved_points, (parent_segment, child_segment))}."""
    out = {}
    sag, fro = limits["sagittal"], limits["frontal"]
    if facing in ("left", "right"):
        joints = [NECK] + [j for s in SIDES for j in _sagittal_joints(s)]
        for name, pivot, pv, cv, sign, _ in joints:
            p, c = vec(pts, pv), vec(pts, cv)
            if p is None or c is None:
                continue
            v = sign * signed(p, c) - (ANKLE_OFFSET if name == "ankle" else 0)
            key = name if name == "neck" else f"{name}_{pivot[-1]}"
            out[key] = (wrap(v), sag[name]["min"], sag[name]["max"], {pv[0], pv[1], cv[1]}, (pv, cv))
    elif facing == "side":
        for s in SIDES:
            for name, pv, cv in (("elbow", (f"shoulder_{s}", f"elbow_{s}"), (f"elbow_{s}", f"wrist_{s}")),
                                 ("knee", (f"hip_{s}", f"knee_{s}"), (f"knee_{s}", f"ankle_{s}"))):
                p, c = vec(pts, pv), vec(pts, cv)
                if p is not None and c is not None:
                    out[f"{name}_fold_{s}"] = (abs(signed(p, c)), 0, sag[name]["max"], {pv[0], pv[1], cv[1]}, (pv, cv))
    else:  # front view
        p, c = vec(pts, ("pelvis", "neck")), vec(pts, ("neck", "head"))
        if p is not None and c is not None:
            out["neck_tilt"] = (abs(signed(p, c)), 0, fro["neck_tilt"]["max"], {"pelvis", "neck", "head"},
                                (("pelvis", "neck"), ("neck", "head")))
        for s in SIDES:
            for key, lim, pv, cv in (
                ("hip_abduction", "hip_abduction", ("neck", "pelvis"), (f"hip_{s}", f"knee_{s}")),
                ("knee_lateral", "knee_lateral", (f"hip_{s}", f"knee_{s}"), (f"knee_{s}", f"ankle_{s}")),
                ("elbow_fold", "elbow_fold", (f"shoulder_{s}", f"elbow_{s}"), (f"elbow_{s}", f"wrist_{s}")),
            ):
                p, c = vec(pts, pv), vec(pts, cv)
                if p is not None and c is not None:
                    out[f"{key}_{s}"] = (abs(signed(p, c)), 0, fro[lim]["max"], {pv[0], pv[1], cv[1]}, (pv, cv))
    return out


def front_ambiguous(key, pts):
    """In a flat front view a bent hip or knee seen from the front looks like a sideways bend
    (cross-legged sitting, kneeling, knock knees). Only a knee under a near-vertical thigh is
    unambiguous; everything else is a warning."""
    if key.startswith("hip_abduction"):
        return True
    if key.startswith("knee_lateral"):
        s = key[-1]
        th = vec(pts, ("pelvis", "neck")), vec(pts, (f"hip_{s}", f"knee_{s}"))
        if th[0] is None or th[1] is None:
            return True
        return abs(180 - abs(signed(th[0], th[1]))) > 30  # thigh not hanging down
    return False


SEGMENT_NAMES = {("neck", "head"): "head", ("pelvis", "neck"): "trunk"}
for _s in SIDES:
    SEGMENT_NAMES.update({(f"shoulder_{_s}", f"elbow_{_s}"): "upper_arm", (f"elbow_{_s}", f"wrist_{_s}"): "forearm",
                          (f"hip_{_s}", f"knee_{_s}"): "thigh", (f"knee_{_s}", f"ankle_{_s}"): "shank"})


def center_of_mass(pts, mass=None):
    """Horizontal center of mass. `mass` overrides segment fractions for non-human
    proportions, e.g. {"head": 0.3} for a chibi; they are renormalised."""
    tot, x = 0.0, 0.0
    for (a, b), m in MASS:
        m = (mass or {}).get(SEGMENT_NAMES[(a, b)], m)
        if a in pts and b in pts:
            tot += m; x += m * (pts[a][0] + pts[b][0]) / 2
    return x / tot if tot > 0.5 * sum((mass or {}).get(SEGMENT_NAMES[k], m) for k, m in MASS) else None


# ---------- check ----------
def check(track, profile=None):
    profile = profile or track.get("profile") or ("video" if track.get("source") == "estimator" else "rig")
    P = dict(LIMITS["profiles"][profile])
    if track.get("projected"):
        # A 3D rig flattened through a camera: limbs only ever look shorter, so measure
        # stretch against the longest length seen and never call a limb shrunk.
        P.update(bone_shrink=None, ref_percentile=1.0, left_right_mismatch=None)
    limits = merged_limits(track)
    if is_3d(track):
        track = to_2d(track)
    fps = float(track.get("fps", 12))
    issues = []

    def add(fi, severity, kind, msg, joints):
        issues.append({"frame": fi, "severity": severity, "kind": kind, "message": msg, "joints": sorted(joints)})

    frames = [load_frame(f, P["min_confidence"]) for f in track["frames"]]
    # Too few points, or a figure too small for the estimator's points to be trusted: skip.
    usable = set()
    for fi, (pts, facing) in enumerate(frames):
        ys = [y for _, y in pts.values()]
        if len(pts) >= 6 and max(ys) - min(ys) >= P.get("min_figure_px", 0):
            usable.add(fi)
        else:
            frames[fi] = ({}, facing)

    # Reference bone lengths, normalised by frame scale (rig zoom) — rest pose if given.
    def scaled_len(pts, a, b, scale):
        return norm(sub(pts[a], pts[b])) / scale if a in pts and b in pts else None

    def true_len(fi, pts, a, b, scale):
        """Real limb length: 3D when the track is 3D, else what is drawn."""
        l3 = track["frames"][fi].get("_len3d")
        if l3 is not None:
            return l3.get(f"{a}>{b}") if a in pts and b in pts else None
        return scaled_len(pts, a, b, scale)

    scales = [float(f.get("scale", 1.0)) for f in track["frames"]]
    ref = {}
    if "rest" in track and not track.get("projected"):  # a projected rest pose is foreshortened too
        rest, _ = load_frame({"joints": track["rest"], "facing": "right"}, 0)
        ref = {b: norm(sub(rest[b[0]], rest[b[1]])) for b in BONES if b[0] in rest and b[1] in rest}
    else:
        for b in BONES:
            ls = [true_len(fi, p, *b, s) for fi, ((p, _), s) in enumerate(zip(frames, scales))]
            ls = [l for l in ls if l]
            if ls:
                # Estimated limbs only look shorter (turned toward the camera), so their true
                # length is near the top of what was seen; rig limbs should never change.
                ref[b] = sorted(ls)[int(P.get("ref_percentile", 0.5) * (len(ls) - 1))]

    if P["left_right_mismatch"]:
        for (a, b) in BONES:
            if a.endswith("_l"):
                rb = (a[:-1] + "r", b[:-1] + "r")
                if (a, b) in ref and rb in ref:
                    longest = max(ref[(a, b)], ref[rb])
                    d = abs(ref[(a, b)] - ref[rb]) / longest if longest > 1e-9 else 0.0
                    if d > P["left_right_mismatch"]:
                        add(None, "error", "left_right_mismatch",
                            f"{a[:-2]}->{b[:-2]} left/right lengths differ by {d:.0%}", {a, b, *rb})

    prev = None
    off_balance = []
    for fi, ((pts, facing), scale) in enumerate(zip(frames, scales)):
        # 1. joint limits
        angles = frame_angles(pts, facing, limits)
        # A segment pointing at the camera looks short and its 2D angle means nothing: skip it.
        for key in list(angles):
            for seg in angles[key][4]:
                l = scaled_len(pts, *seg, scale)
                full = true_len(fi, pts, *seg, scale) if "_len3d" in track["frames"][fi] else ref.get(seg)
                if full and l is not None and l < 0.5 * full:
                    del angles[key]
                    break
        for key, (v, lo, hi, inv, _) in angles.items():
            over = arc_violation(v, lo, hi)
            if over > P["angle_tolerance"]:
                sev = "warn" if facing == "front" and front_ambiguous(key, pts) else "error"
                add(fi, sev, "joint_limit",
                    f"{key} at {v:.0f}° (allowed {lo}..{hi}, {facing} view) — {over:.0f}° past the limit", inv)

        # 2. bone lengths (stretching / shrinking limbs)
        torso = true_len(fi, pts, "pelvis", "neck", scale)
        tref = ref.get(("pelvis", "neck"))
        for b in BONES:
            l = true_len(fi, pts, *b, scale)
            if l is None or b not in ref or ref[b] <= 1e-9:
                continue  # (a zero-length reference: e.g. a rest foot pointing straight at the camera)
            if profile == "video":
                # Camera distance changes: compare limb/torso ratios, not raw pixels.
                if not torso or not tref or b == ("pelvis", "neck"):
                    continue
                r = (l / torso) / (ref[b] / tref)
            else:
                r = l / ref[b]
            # Pixel art rounds joints to whole pixels: allow that much on short bones.
            px = P.get("abs_tolerance_px", 0) / max(ref[b] * (scale if profile != "video" else 1), 1e-9)
            if r > 1 + max(P["bone_stretch"], px):
                add(fi, "error", "bone_stretch", f"{b[0]}->{b[1]} stretched to {r:.0%} of its length", set(b))
            elif P["bone_shrink"] and r < 1 - max(P["bone_shrink"], px) and \
                    (facing in ("left", "right") or "_len3d" in track["frames"][fi]):
                # (in front view a limb pointing at the viewer is legitimately short)
                add(fi, "error", "bone_shrink", f"{b[0]}->{b[1]} shrunk to {r:.0%} of its length", set(b))

        # 3. pops and knees/elbows snapping direction between frames
        if prev is not None and prev[1] == facing:
            for key, (v, *_rest) in angles.items():
                if key in prev[0]:
                    pv = prev[0][key][0]
                    speed = abs(wrap(v - pv)) * fps
                    if speed > P["max_joint_speed"]:
                        add(fi, "error" if P["blocking"] else "warn", "pop",
                            f"{key} jumps {abs(wrap(v - pv)):.0f}° in one frame ({speed:.0f}°/s)", angles[key][3])
                    elif key.split("_")[0] in ("elbow", "knee") and facing in ("left", "right") \
                            and pv * v < 0 and min(abs(pv), abs(v)) > 15:
                        add(fi, "error", "snap", f"{key} flips bend direction ({pv:.0f}° -> {v:.0f}°)",
                            angles[key][3])
        prev = (angles, facing)

        # 4. balance: center of mass over what holds the body up
        fr = track["frames"][fi]
        if not (fr.get("airborne") or fr.get("supported") is True):
            feet = [pts[k] for s in SIDES for k in (f"ankle_{s}", f"toe_{s}", f"heel_{s}") if k in pts]
            com = center_of_mass(pts, track.get("mass"))
            if feet and com is not None and len(pts) >= 8:
                ys = [y for _, y in pts.values()]
                height = max(ys) - min(ys)
                ground = min(ys)
                # whatever touches the ground holds the body up: feet, knees, pelvis, hands
                support = [p[0] for p in pts.values() if p[1] - ground < 0.05 * height]
                # Extra support: joints (pelvis when sitting, knee_l when kneeling, wrist_r
                # pushing a block) or props by name, e.g. "supported": ["pelvis", "block"].
                mirror = -1 if facing == "left" else 1
                for k in fr.get("supported") or []:
                    if k in pts:
                        support.append(pts[k][0])
                    elif k in fr.get("props", {}):
                        support.append(mirror * float(fr["props"][k][0]))
                margin = P["balance_margin"] * height
                if support and not (min(support) - margin <= com <= max(support) + margin):
                    off_balance.append(fi)

    # A walk or run is off balance for a frame or two at every step; only a pose held
    # off balance (about a fifth of a second or longer) would really fall over.
    hold = max(2, round(0.2 * fps))
    runs, run = [], []
    for fi in off_balance:
        if run and fi != run[-1] + 1:
            runs.append(run); run = []
        run.append(fi)
    runs.append(run)
    for run in runs:
        if len(run) >= hold:
            for fi in run:
                add(fi, "warn", "balance",
                    "center of mass is outside what supports the body — the pose would topple "
                    "(mark the frame \"airborne\": true for a jump or fall, or list what it rests on: "
                    "\"supported\": [\"pelvis\", \"knee_l\", \"<prop>\"], or true)", {"pelvis", "neck"})

    issues += check_hands(track, P, usable)
    issues.sort(key=lambda i: (-1 if i["frame"] is None else i["frame"]))
    errors = sum(1 for i in issues if i["severity"] == "error")
    return {
        "profile": profile,
        "frames": len(frames),
        "frames_checked": len(usable),
        "errors": errors,
        "warnings": len(issues) - errors,
        "passed": errors == 0,
        "status": "PASS" if errors == 0 else ("FAIL" if P["blocking"] else "REVIEW"),
        "issues": issues,
    }


# ---------- left / right hands ----------
def raw_points(frame, min_conf):
    """Image-space joints (no mirroring), or the true 3D joints of a 3D track,
    confidence-filtered, with neck/pelvis derived."""
    conf = frame.get("conf", {})
    src = frame.get("_joints3d") or frame["joints"]
    pts = {k: tuple(float(c) for c in v) for k, v in src.items()
           if v is not None and conf.get(k, 1.0) >= min_conf}
    for mid, a, b in (("neck", "shoulder_l", "shoulder_r"), ("pelvis", "hip_l", "hip_r")):
        if mid not in pts and a in pts and b in pts:
            pts[mid] = tuple((x + y) / 2 for x, y in zip(pts[a], pts[b]))
    return pts


def check_hands(track, P, usable=None):
    """Left/right mistakes generated video makes: arms trading places, the upper body
    flipped against the legs, a prop jumping to the other hand, a prop drawn in the
    wrong hand, a left hand drawn on the right arm (mirrored hand), a hand missing what
    it should touch, and a forearm sweeping across the face."""
    issues = []
    def add(fi, kind, msg, joints, severity="error"):
        issues.append({"frame": fi, "severity": severity, "kind": kind, "message": msg, "joints": sorted(joints)})

    frames = track["frames"]
    yaw_max = merged_limits(track)["yaw"]["neck_yaw"]["max"]
    prev = None
    for fi, f in enumerate(frames):
        pts = raw_points(f, P["min_confidence"]) if usable is None or fi in usable else {}
        torso = norm(sub(pts["neck"], pts["pelvis"])) if "neck" in pts and "pelvis" in pts else None

        # Upper body facing the opposite way from the hips: shoulders' left/right order
        # is reversed against the hips' order while both are seen square-on.
        three_d = "_joints3d" in f
        if three_d and torso and all(k in pts for k in ("shoulder_l", "shoulder_r", "hip_l", "hip_r")):
            if dot(sub(pts["shoulder_r"], pts["shoulder_l"]), sub(pts["hip_r"], pts["hip_l"])) < 0:
                add(fi, "torso_flip", "shoulders face the opposite way from the hips (upper body twisted "
                    "more than 90° against the legs)", {"shoulder_l", "shoulder_r", "hip_l", "hip_r"})
        elif torso and all(k in pts for k in ("shoulder_l", "shoulder_r", "hip_l", "hip_r")):
            sw = pts["shoulder_l"][0] - pts["shoulder_r"][0]
            hw = pts["hip_l"][0] - pts["hip_r"][0]
            if sw * hw < 0 and abs(sw) > 0.3 * torso and abs(hw) > 0.2 * torso:
                add(fi, "torso_flip", "shoulders face the opposite way from the hips (left and right "
                    "sides swapped between upper and lower body)", {"shoulder_l", "shoulder_r", "hip_l", "hip_r"})

        # Facing the camera, the character's right side is on the screen's left. Labels the
        # other way round mean the figure is drawn mirrored (or its joints are mislabelled).
        if not three_d and f.get("facing") in ("front", "back") and torso and \
                all(k in pts for k in ("shoulder_l", "shoulder_r")):
            sw = pts["shoulder_l"][0] - pts["shoulder_r"][0]
            if abs(sw) > 0.2 * torso and (sw < 0) == (f["facing"] == "front"):
                add(fi, "mirrored_body", f"facing {'the camera' if f['facing'] == 'front' else 'away'}, the "
                    f"character's right shoulder should be on screen {'left' if f['facing'] == 'front' else 'right'}"
                    " — the figure is mirrored or its left/right labels are swapped",
                    {"shoulder_l", "shoulder_r"})

        # Arms trading places between frames: each wrist lands where the other one was.
        if prev is not None and torso and all(k in pts and k in prev for k in ("wrist_l", "wrist_r")):
            keep = norm(sub(pts["wrist_l"], prev["wrist_l"])) + norm(sub(pts["wrist_r"], prev["wrist_r"]))
            swap = norm(sub(pts["wrist_l"], prev["wrist_r"])) + norm(sub(pts["wrist_r"], prev["wrist_l"]))
            if keep > 0.8 * torso and swap < 0.35 * keep:
                add(fi, "hand_swap", "left and right hands traded places in one frame", {
                    "shoulder_l", "elbow_l", "wrist_l", "shoulder_r", "elbow_r", "wrist_r"})
        prev = pts

        # Head turned past the shoulders (3D tracks with a nose joint).
        if "_yaw" in f and abs(f["_yaw"]) > yaw_max + P["angle_tolerance"]:
            add(fi, "head_yaw", f"head turned {abs(f['_yaw']):.0f}° from the body (more than "
                f"{yaw_max}° turns it past the shoulders)", {"neck", "head"})

        # Which hand holds which prop must not change without a planned hand-off.
        holds = f.get("holds", {})
        if fi > 0 and not f.get("handoff"):
            for prop, side in holds.items():
                before = frames[fi - 1].get("holds", {}).get(prop)
                if before and side and before != side:
                    add(fi, "prop_hand_switch", f"{prop} jumps from the {_side(before)} hand to the "
                        f"{_side(side)} hand (mark \"handoff\": true if it is passed on purpose)",
                        {f"wrist_{before}", f"wrist_{side}"})

        # A prop said to be in one hand must be drawn at that hand.
        for prop, side in holds.items():
            at = (f.get("_props3d") or f.get("props", {})).get(prop)
            other = "r" if side == "l" else "l"
            just_passed = f.get("handoff") or (fi > 0 and frames[fi - 1].get("handoff"))
            if at and side and f"wrist_{side}" in pts and torso and not just_passed:
                d_own = norm(sub(at, pts[f"wrist_{side}"]))
                d_other = norm(sub(at, pts[f"wrist_{other}"])) if f"wrist_{other}" in pts else float("inf")
                if d_own > 0.6 * torso or d_other < d_own:
                    add(fi, "prop_wrong_hand", f"{prop} should be in the {_side(side)} hand but is drawn "
                        f"{'at the ' + _side(other) + ' hand' if d_other < d_own else 'away from it'}",
                        {f"wrist_{side}", f"elbow_{side}"})

        # A hand meant to touch something (a door, a table, a face) must reach it.
        for side, target in f.get("contacts", {}).items():
            at = (f.get("_props3d") or f.get("props", {})).get(target) if isinstance(target, str) else target
            if at and f"wrist_{side}" in pts and torso:
                d = norm(sub(at, pts[f"wrist_{side}"]))
                if d > 0.35 * torso:
                    label = target if isinstance(target, str) else "its target"
                    add(fi, "contact_miss", f"the {_side(side)} hand should touch {label} but stops "
                        f"{d / torso:.1f} torso-lengths away", {f"wrist_{side}", f"elbow_{side}"})

        # Front view: a forearm sweeping across the face, unless the beat asks for it.
        if not three_d and f.get("facing", "front") == "front" and not f.get("face_cover") \
                and "head" in pts and "neck" in pts:
            r = 0.5 * norm(sub(pts["head"], pts["neck"]))
            for side in SIDES:
                ks = (f"shoulder_{side}", f"elbow_{side}", f"wrist_{side}")
                if r and all(k in pts for k in ks):
                    crosses = (pts[ks[2]][0] - pts["head"][0]) * (pts[ks[0]][0] - pts["head"][0]) < 0
                    if _seg_dist(pts["head"], pts[ks[1]], pts[ks[2]]) < r and \
                            (crosses or norm(sub(pts[ks[2]], pts["head"])) < r):
                        add(fi, "arm_over_face", f"the {_side(side)} forearm crosses the face "
                            "(mark the frame \"face_cover\": true if the beat covers the face on purpose)",
                            {ks[1], ks[2], "head"}, severity="warn")

        # Hand shape (thumb side) must match the arm it is on.
        for side, h in f.get("hands", {}).items():
            if h and h.get("looks_like") in ("l", "r") and h["looks_like"] != side \
                    and h.get("score", 1.0) >= 0.8:
                add(fi, "mirrored_hand", f"the hand on the {_side(side)} arm is drawn as a "
                    f"{_side(h['looks_like'])} hand (thumb on the wrong side)",
                    {f"wrist_{side}", f"elbow_{side}"})
    return issues


def _seg_dist(p, a, b):
    """Distance from point p to segment a-b."""
    ab, ap = sub(b, a), sub(p, a)
    t = max(0.0, min(1.0, (ap[0] * ab[0] + ap[1] * ab[1]) / max(ab[0] ** 2 + ab[1] ** 2, 1e-9)))
    return norm(sub(p, (a[0] + ab[0] * t, a[1] + ab[1] * t)))


def _side(s): return {"l": "left", "r": "right"}.get(s, s)


def check_sequence(tracks):
    """Across clips: a prop must stay in the same hand from the end of one clip to the start of the next."""
    issues = []
    for k in range(len(tracks) - 1):
        a, b = tracks[k]["frames"], tracks[k + 1]["frames"]
        if not a or not b or b[0].get("handoff"):
            continue
        end, start = a[-1].get("holds", {}), b[0].get("holds", {})
        for prop, side in start.items():
            if end.get(prop) and side and end[prop] != side:
                issues.append({"frame": None, "clip": k + 1, "severity": "error", "kind": "prop_hand_switch",
                               "message": f"{prop} ends clip {k + 1} in the {_side(end[prop])} hand but starts "
                                          f"clip {k + 2} in the {_side(side)} hand", "joints": []})
    return issues


# ---------- fix (rigs only) ----------
def fix(track):
    """Clamp side-view joint angles into range and restore limb lengths.
    Front-view frames, one-frame pops and balance are reported by check() but not repaired here."""
    sag = merged_limits(track)["sagittal"]
    out = json.loads(json.dumps(track))
    lengths = {}
    for b in BONES:
        ls = []
        for f in track["frames"]:
            p, _ = load_frame(f, 0)
            if b[0] in p and b[1] in p:
                ls.append(norm(sub(p[b[0]], p[b[1]])) / float(f.get("scale", 1.0)))
        if ls:
            lengths[b] = statistics.median(ls)
    if "rest" in track and not track.get("projected"):  # a projected rest pose is foreshortened too
        rest, _ = load_frame({"joints": track["rest"], "facing": "right"}, 0)
        lengths.update({b: norm(sub(rest[b[0]], rest[b[1]])) for b in BONES if b[0] in rest and b[1] in rest})

    for f in out["frames"]:
        pts, facing = load_frame(f, 0)
        if facing not in ("left", "right"):
            continue
        scale = float(f.get("scale", 1.0))
        # proximal to distal: restore lengths, then clamp angles
        chain = [("neck", "head", [])]
        for s in SIDES:
            chain += [(f"shoulder_{s}", f"elbow_{s}", [f"wrist_{s}"]), (f"elbow_{s}", f"wrist_{s}", []),
                      (f"hip_{s}", f"knee_{s}", [f"ankle_{s}", f"heel_{s}", f"toe_{s}"]),
                      (f"knee_{s}", f"ankle_{s}", [f"heel_{s}", f"toe_{s}"]), (f"ankle_{s}", f"toe_{s}", [])]
        for a, b, desc in chain:
            if (a, b) in lengths and a in pts and b in pts:
                v = sub(pts[b], pts[a]); l = norm(v)
                if l > 1e-6:
                    want = lengths[(a, b)] * scale
                    d = (v[0] * (want / l - 1), v[1] * (want / l - 1))
                    for k in [b] + desc:
                        if k in pts:
                            pts[k] = (pts[k][0] + d[0], pts[k][1] + d[1])
        for name, pivot, pv, cv, sign, desc in [NECK] + [j for s in SIDES for j in _sagittal_joints(s)]:
            p, c = vec(pts, pv), vec(pts, cv)
            if p is None or c is None:
                continue
            v = wrap(sign * signed(p, c) - (ANKLE_OFFSET if name == "ankle" else 0))
            lo, hi = sag[name]["min"], sag[name]["max"]
            if arc_violation(v, lo, hi) == 0:
                continue
            target = lo if abs(wrap(v - lo)) < abs(wrap(v - hi)) else hi
            delta = sign * wrap(target - v)
            for k in desc:
                if k in pts:
                    pts[k] = rotate(pts[k], pts[pivot], delta)
        mirror = -1 if facing == "left" else 1
        for k in f["joints"]:
            if k in pts:
                f["joints"][k] = [round(mirror * pts[k][0], 2), round(-pts[k][1], 2)]
    return out


# ---------- report ----------
SEGMENTS = [("pelvis", "neck"), ("neck", "head")] + [
    seg for s in SIDES for seg in [
        ("neck", f"shoulder_{s}"), (f"shoulder_{s}", f"elbow_{s}"), (f"elbow_{s}", f"wrist_{s}"),
        ("pelvis", f"hip_{s}"), (f"hip_{s}", f"knee_{s}"), (f"knee_{s}", f"ankle_{s}"),
        (f"ankle_{s}", f"toe_{s}"), (f"ankle_{s}", f"heel_{s}")]
]

def skeleton_svg(frame, bad, x0, y0, w, h, title=""):
    """One cell: the frame image (if any) plus the skeleton, offending joints in red.
    The character's left side is blue, right side green; props are orange squares."""
    j = {k: v for k, v in frame["joints"].items() if v is not None}
    for mid, a, b in (("neck", "shoulder_l", "shoulder_r"), ("pelvis", "hip_l", "hip_r")):
        if mid not in j and a in j and b in j:
            j[mid] = [(j[a][0] + j[b][0]) / 2, (j[a][1] + j[b][1]) / 2]
    if not j:
        return ""
    allp = list(j.values()) + list(frame.get("props", {}).values())
    xs = [p[0] for p in allp]; ys = [p[1] for p in allp]
    pad = 0.2 * max(max(xs) - min(xs), max(ys) - min(ys), 1)
    bx0, by0 = min(xs) - pad, min(ys) - pad
    iw, ih = max(xs) - min(xs) + 2 * pad, max(ys) - min(ys) + 2 * pad
    s = min(w / iw, (h - 22) / ih)
    tx = lambda p: (x0 + (p[0] - bx0) * s + (w - iw * s) / 2, y0 + (p[1] - by0) * s)
    parts = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="#f6f4ef" stroke="#ccc"/>']
    if frame.get("image") and frame.get("image_size"):
        # crop the frame to the figure
        (cx, cy), fw, fh = tx((bx0, by0)), frame["image_size"][0], frame["image_size"][1]
        parts.append(f'<svg x="{cx:.1f}" y="{cy:.1f}" width="{iw * s:.1f}" height="{ih * s:.1f}" '
                     f'viewBox="{bx0:.1f} {by0:.1f} {iw:.1f} {ih:.1f}"><image href="{frame["image"]}" '
                     f'x="0" y="0" width="{fw}" height="{fh}" opacity="0.8"/></svg>')
    lw = max(2.0, 0.012 * h)
    for a, b in SEGMENTS:
        if a in j and b in j:
            red = a in bad and b in bad
            col = "#e0312b" if red else {"l": "#1f6feb", "r": "#12a150"}.get(b[-1], "#5a6b80")
            (x1, y1), (x2, y2) = tx(j[a]), tx(j[b])
            parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                         f'stroke="{col}" stroke-width="{lw * (1.8 if red else 1):.1f}" stroke-linecap="round"/>')
    if "head" in j:
        hx, hy = tx(j["head"])
        parts.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{lw * 3:.1f}" fill="none" stroke="#5a6b80" stroke-width="{lw:.1f}"/>')
    for k, p in j.items():
        x, y = tx(p)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{lw * (1.6 if k in bad else 0.9):.1f}" fill="{"#e0312b" if k in bad else "#0b3d91"}"/>')
        if k in ("wrist_l", "wrist_r"):
            parts.append(f'<text x="{x + 2 * lw:.1f}" y="{y + 4:.1f}" font-family="sans-serif" font-size="12" '
                         f'font-weight="bold" fill="{"#1f6feb" if k[-1] == "l" else "#12a150"}">{k[-1].upper()}</text>')
    for side, hand in (frame.get("hands") or {}).items():
        if hand and f"wrist_{side}" in j:
            x, y = tx(j[f"wrist_{side}"])
            wrong = hand.get("looks_like") != side
            parts.append(f'<text x="{x - 9 * lw:.1f}" y="{y + 5 * lw:.1f}" font-family="sans-serif" font-size="11" '
                         f'fill="{"#e0312b" if wrong else "#555"}">{hand.get("looks_like", "?").upper()} hand</text>')
    for name, p in frame.get("props", {}).items():
        x, y = tx(p)
        parts.append(f'<rect x="{x - 2.5 * lw:.1f}" y="{y - 2.5 * lw:.1f}" width="{5 * lw:.1f}" height="{5 * lw:.1f}" '
                     f'fill="#f08c00" stroke="#7a4600"/><text x="{x + 3 * lw:.1f}" y="{y - 2 * lw:.1f}" '
                     f'font-family="sans-serif" font-size="11" fill="#7a4600">{name}</text>')
    if title:
        parts.append(f'<text x="{x0 + 6}" y="{y0 + h - 6}" font-family="sans-serif" font-size="13" fill="#333">{title}</text>')
    return "\n".join(parts)

def write_report(track, result, out_dir, max_cells=24):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(json.dumps(result, indent=2, ensure_ascii=False))
    by_frame = {}
    for i in result["issues"]:
        if i["frame"] is not None:
            by_frame.setdefault(i["frame"], []).append(i)
    flagged = sorted(by_frame)[:max_cells]
    cw, ch, cols = 260, 300, 4
    rows = max(1, math.ceil(len(flagged) / cols))
    lines = []
    cells = []
    for n, fi in enumerate(flagged):
        bad = set().union(*(set(i["joints"]) for i in by_frame[fi] if i["severity"] == "error")) \
            or set().union(*(set(i["joints"]) for i in by_frame[fi]))
        kinds = sorted({i["kind"] for i in by_frame[fi]})
        cells.append(skeleton_svg(track["frames"][fi], bad, (n % cols) * cw, (n // cols) * ch, cw - 6, ch - 6,
                                  f"frame {fi}: {', '.join(kinds)}"))
        for i in by_frame[fi]:
            lines.append(f"frame {fi} [{i['severity']}] {i['message']}")
    status = result["status"]
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{cols * cw}" height="{rows * ch + 40}" viewBox="0 0 {cols * cw} {rows * ch + 40}">'
            f'<rect width="100%" height="100%" fill="#fff"/>'
            f'<text x="8" y="26" font-family="sans-serif" font-size="18" font-weight="bold" '
            f'fill="{ {"PASS": "#1a7f37", "REVIEW": "#b26b00"}.get(status, "#e0312b") }">Posture gate {status}: '
            f'{result["errors"]} errors, {result["warnings"]} warnings, '
            f'{result["frames_checked"]}/{result["frames"]} frames with a usable pose</text>'
            f'<g transform="translate(0 40)">')
    (out / "report.svg").write_text(head + "\n".join(cells) + "</g></svg>")
    (out / "report.txt").write_text("\n".join(lines) + "\n")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub_ = ap.add_subparsers(dest="cmd", required=True)
    c = sub_.add_parser("check", help="gate one or more clip tracks, in story order")
    c.add_argument("tracks", nargs="+"); c.add_argument("--profile", choices=["rig", "pixel", "video"])
    c.add_argument("--report", help="folder for report.svg/.json/.txt (one subfolder per clip if several)")
    c.add_argument("--json", action="store_true", help="print the full result as JSON")
    c.add_argument("--strict", action="store_true", help="fail on errors even in the non-blocking video profile")
    f = sub_.add_parser("fix", help="repair a rig track"); f.add_argument("track"); f.add_argument("-o", "--out", required=True)
    a = ap.parse_args(argv)
    paths = [a.track] if a.cmd == "fix" else a.tracks
    try:
        tracks = [json.loads(Path(p).read_text()) for p in paths]
    except (OSError, ValueError) as e:
        print(f"cannot read track: {e}", file=sys.stderr); return 2
    if a.cmd == "fix":
        fixed = fix(tracks[0])
        Path(a.out).write_text(json.dumps(fixed, indent=1))
        r = check(fixed, "rig")
        print(f"wrote {a.out}; still left after fix: {r['errors']} errors, {r['warnings']} warnings")
        for i in r["issues"]:
            print(f"  {i['severity']} frame {i['frame']}: {i['message']}")
        return 0 if r["passed"] else 1
    results = [check(t, a.profile) for t in tracks]
    if a.strict:
        for r in results:
            r["status"] = "PASS" if r["passed"] else "FAIL"
    seq = check_sequence(tracks)
    passed = all(r["status"] != "FAIL" for r in results) and not seq
    if a.report:
        for n, (t, r) in enumerate(zip(tracks, results)):
            write_report(t, r, Path(a.report) / f"clip{n + 1}" if len(tracks) > 1 else a.report)
    if a.json:
        print(json.dumps({"passed": passed, "clips": results, "sequence": seq}, indent=2, ensure_ascii=False))
        return 0 if passed else 1
    for n, (p, r) in enumerate(zip(paths, results)):
        if len(paths) > 1:
            print(f"== clip {n + 1}: {p}")
        for i in r["issues"]:
            where = "track" if i["frame"] is None else f"frame {i['frame']}"
            print(f"{i['severity'].upper():5} {where}: {i['message']}")
        print(f"{r['status']} ({r['profile']} profile): {r['errors']} errors, "
              f"{r['warnings']} warnings, {r['frames_checked']}/{r['frames']} frames checked")
    for i in seq:
        print(f"ERROR between clips: {i['message']}")
    if len(paths) > 1:
        print("PASS" if passed else "FAIL", "(all clips)")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
