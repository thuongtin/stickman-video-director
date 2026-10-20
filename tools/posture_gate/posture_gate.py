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
import re
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


# ---------- four-legged characters ----------
QUAD_LEGS = {"fl": "shoulder", "fr": "shoulder", "hl": "hip", "hr": "hip"}


def _point(v):
    return isinstance(v, (list, tuple)) and len(v) in (2, 3) and all(isinstance(x, (int, float)) for x in v)


def as_joint_track(track):
    """Frames that list their points at the top level ({"hip": [x, y], "fl_paw": ...}) get them under
    "joints", so a cat track joins a --scene run with the people."""
    for f in track.get("frames", []):
        if isinstance(f, dict) and "joints" not in f:
            f["joints"] = {k: v for k, v in f.items() if _point(v)}
    return track


def is_quadruped(track):
    return track.get("body_plan") == "quadruped" or any(
        "fl_paw" in f.get("joints", {}) and "hl_paw" in f.get("joints", {}) for f in track["frames"][:3])


def check_quadruped(track, P, profile):
    """A four-legged animal in side view: legs "fl", "fr", "hl", "hr" (front/hind, the animal's own
    left/right), each "<leg>_mid" (elbow or hock) and "<leg>_paw", hanging from "shoulder" (front) and
    "hip" (hind); "neck", "head" and a tail chain "tail0", "tail1", ... Bones keep their length, all
    four legs stay drawn, no joint teleports, a leg never flips its bend, and a straight stiff tail
    that reads as a fifth leg is flagged."""
    issues = []

    def add(fi, severity, kind, msg, joints):
        issues.append({"frame": fi, "severity": severity, "kind": kind, "message": msg, "joints": sorted(joints)})

    frames = [{k: tuple(float(x) for x in v[:2]) for k, v in f["joints"].items() if v is not None}
              for f in track["frames"]]
    tails = sorted({k for j in frames for k in j if re.fullmatch(r"tail\d+", k)}, key=lambda k: int(k[4:]))
    bones = [("hip", "shoulder"), ("shoulder", "neck"), ("neck", "head")]
    for leg, top in QUAD_LEGS.items():
        bones += [(top, f"{leg}_mid"), (f"{leg}_mid", f"{leg}_paw")]
    chain = ["hip"] + tails
    bones += list(zip(chain, chain[1:])) if tails else []
    rest = track.get("rest") or {}
    rest = rest.get("joints", rest)
    stretch, shrink = P["bone_stretch"], P.get("bone_shrink")
    abs_px = P.get("abs_tolerance_px", 0)
    if track.get("projected"):
        shrink = None
    ref = {}
    for a, b in bones:
        ls = sorted(norm(sub(j[a], j[b])) for j in frames if a in j and b in j)
        if rest and a in rest and b in rest:
            ref[(a, b)] = norm(sub(rest[a][:2], rest[b][:2]))
        elif ls:
            ref[(a, b)] = ls[-1] if track.get("projected") else ls[len(ls) // 2]
    body = ref.get(("hip", "shoulder")) or 1.0
    leg_len = max([ref.get((t, f"{g}_mid"), 0) + ref.get((f"{g}_mid", f"{g}_paw"), 0) for g, t in QUAD_LEGS.items()] or [body])
    paws = [f"{g}_paw" for g in QUAD_LEGS]
    fps = float(track.get("fps", 12))
    prev_bend = {}
    for fi, j in enumerate(frames):
        f = track["frames"][fi]
        for (a, b), r in ref.items():
            if a in j and b in j and r > 0:
                l = norm(sub(j[a], j[b]))
                if l - r > stretch * r + abs_px:
                    add(fi, "error", "bone_stretch", f"{a}-{b} is {l / r:.2f}x its length", {a, b})
                elif shrink is not None and r - l > shrink * r + abs_px:
                    add(fi, "error", "bone_shrink", f"{a}-{b} is {l / r:.2f}x its length", {a, b})
        have = [p for p in paws if p in j]
        if have and len(have) < 4:
            add(fi, "error", "leg_missing", f"only {len(have)} of the four legs are drawn "
                f"(missing {', '.join(sorted(set(paws) - set(have)))}); a hidden far leg still gets its points", set(have))
        if fi and not f.get("cut"):
            pj = frames[fi - 1]
            if "hip" in j and "hip" in pj and norm(sub(j["hip"], pj["hip"])) > body:
                add(fi, "error" if P["blocking"] else "warn", "pop",
                    f"the body jumps {norm(sub(j['hip'], pj['hip'])) / body:.1f} body-lengths in one frame", {"hip"})
            for a2, b2 in bones:  # each bone turns no faster than a person's limb may
                if all(k in j and k in pj for k in (a2, b2)):
                    u, v = sub(j[b2], j[a2]), sub(pj[b2], pj[a2])
                    turn = abs(wrap(math.degrees(math.atan2(u[1], u[0]) - math.atan2(v[1], v[0]))))
                    if turn * fps > P["max_joint_speed"]:
                        add(fi, "error" if P["blocking"] else "warn", "pop",
                            f"{a2}-{b2} swings {turn:.0f}° in one frame ({turn * fps:.0f}°/s)", {a2, b2})
        for g, top in QUAD_LEGS.items():
            m, w = f"{g}_mid", f"{g}_paw"
            if top in j and m in j and w in j:
                u, v = sub(j[m], j[top]), sub(j[w], j[m])
                c = u[0] * v[1] - u[1] * v[0]
                ang = math.degrees(math.atan2(abs(c), dot(u, v)))
                if g in prev_bend and prev_bend[g][0] * c < 0 and min(ang, prev_bend[g][1]) > 15:
                    add(fi, "error", "snap", f"the {g} leg flips its bend direction at {m}", {top, m, w})
                prev_bend[g] = (c, ang)
        # a straight, steep tail as long as a leg reads as a fifth leg (the sitting cat's stick tail)
        if len(tails) >= 2 and all(t in j for t in tails) and "hip" in j:
            pts = [j["hip"]] + [j[t] for t in tails]
            segs = [sub(b2, a2) for a2, b2 in zip(pts, pts[1:])]
            turn = max((math.degrees(math.atan2(abs(a2[0] * b2[1] - a2[1] * b2[0]), dot(a2, b2)))
                        for a2, b2 in zip(segs, segs[1:])), default=0)
            whole = sub(pts[-1], pts[0])
            steep = math.degrees(math.atan2(abs(whole[1]), abs(whole[0]) or 1e-9))
            if turn < 12 and steep > 55 and norm(whole) > 0.6 * leg_len:
                add(fi, "warn", "tail_like_leg", "the tail is a straight stiff stick standing like a fifth leg; "
                    "curve it, wrap it round the paws or lay it along the ground", set(tails))
    issues.sort(key=lambda i: (-1 if i["frame"] is None else i["frame"]))
    errors = sum(1 for i in issues if i["severity"] == "error")
    return {"profile": profile, "frames": len(frames), "frames_checked": len(frames), "errors": errors,
            "warnings": len(issues) - errors, "passed": errors == 0,
            "status": "PASS" if errors == 0 else ("FAIL" if P["blocking"] else "REVIEW"), "issues": issues}


# ---------- 3D tracks ----------
def is_3d(track):
    return any(v is not None and len(v) == 3 for f in track["frames"] for v in f["joints"].values())


def to_2d(track):
    """Project a 3D rig track onto each frame's own side view (the body's sagittal plane),
    so a limb pointing at a camera never looks short or bent. True 3D bone lengths, joints
    and props are kept for the length and left/right checks. Coordinates: "up_axis"
    (default [0, 1, 0]) is up; a character facing +z has its own right side at -x,
    as in three.js/glTF (right-handed coordinates). A left-handed engine (Unity) sets "handedness": "left"."""
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
        # head yaw: the turn of the nose about the neck, against the shoulders' forward, both seen
        # down the neck (a head tipped back in a limbo or knee slide is not a turned head)
        if "nose" in j and "head" in j:
            ax = unit(sub(j["head"], j["neck"])) if "neck" in j else up
            ax = ax or up
            flat = lambda v: tuple(x - dot(v, ax) * a for x, a in zip(v, ax))
            n, fw, lt = flat(sub(j["nose"], j["head"])), flat(fwd), flat(lat)
            if "shoulder_r" in j and "shoulder_l" in j and unit(flat(sub(j["shoulder_r"], j["shoulder_l"]))):
                # against the shoulders: a look back over a twisted trunk turns the neck less
                lt = flat(sub(j["shoulder_r"], j["shoulder_l"]))
                fw = tuple(hand * x for x in cross(ax, unit(lt)))
            if norm(n) > 1e-6 and norm(fw) > 0.3 and norm(lt) > 0.3:
                f["_yaw"] = math.degrees(math.atan2(dot(unit(n), unit(lt)), dot(unit(n), unit(fw))))
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
            # no limit in front view, but an arm flung 130° in one frame is still a pop
            for key, pv, cv in (("arm_swing", ("neck", "pelvis"), (f"shoulder_{s}", f"elbow_{s}")),
                                ("forearm_swing", (f"shoulder_{s}", f"elbow_{s}"), (f"elbow_{s}", f"wrist_{s}"))):
                p, c = vec(pts, pv), vec(pts, cv)
                if p is not None and c is not None:
                    out[f"{key}_{s}"] = (signed(p, c), -180, 180, {cv[0], cv[1]}, (cv,))
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


def center_of_mass_2d(pts, mass=None):
    """Center of mass as a point (x, y), with the same segment fractions as center_of_mass."""
    tot, x, y = 0.0, 0.0, 0.0
    for (a, b), m in MASS:
        m = (mass or {}).get(SEGMENT_NAMES[(a, b)], m)
        if a in pts and b in pts:
            tot += m; x += m * (pts[a][0] + pts[b][0]) / 2; y += m * (pts[a][1] + pts[b][1]) / 2
    return (x / tot, y / tot) if tot else None


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
    as_joint_track(track)
    if is_quadruped(track):
        return check_quadruped(track, P, profile)
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
    # standing height, for "is this joint on the ground": a folded bow is short, its tolerance is not
    spans = [max(y for _, y in p.values()) - min(y for _, y in p.values()) for p, _ in frames if len(p) >= 8]
    tall = max(spans, default=0)
    if "rest" in track:
        rp, _ = load_frame({"joints": track["rest"], "facing": "right"}, 0)
        if len(rp) >= 8:
            tall = max(y for _, y in rp.values()) - min(y for _, y in rp.values())
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
    drift = {}  # zero_g frames: (center of mass, torso, touching something)
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
        # A 3D rig's elbow or knee bends by the angle between its true 3D bones: in the side
        # projection an arm brought across the chest with the upper arm twisted inward reads
        # far more bent than it is. A knee's bend direction comes from its own foot, so a
        # turned-out leg does not read as bending backward.
        j3 = track["frames"][fi].get("_joints3d")
        if j3 and facing in ("left", "right"):
            for name, (a, b, c) in (("elbow", ("shoulder", "elbow", "wrist")), ("knee", ("hip", "knee", "ankle"))):
                for s_ in SIDES:
                    a_, b_, c_ = f"{a}_{s_}", f"{b}_{s_}", f"{c}_{s_}"
                    if all(k in j3 for k in (a_, b_, c_)):
                        u, w = sub(j3[b_], j3[a_]), sub(j3[c_], j3[b_])
                        if norm(u) and norm(w):
                            flex = math.degrees(math.acos(max(-1.0, min(1.0, dot(u, w) / (norm(u) * norm(w))))))
                            key = f"{name}_{s_}"
                            # an elbow cannot fold backward far, so its projected direction only
                            # counts near straight (a twisted upper arm flips the projection)
                            sign = -1 if key in angles and angles[key][0] < 0 and (name == "knee" or flex <= 15) else 1
                            toe = j3.get(f"toe_{s_}")
                            if name == "knee" and toe:
                                # a knee bends toward its own toes, whichever way the leg is turned out
                                ha = sub(j3[c_], j3[a_]); tt = dot(sub(j3[b_], j3[a_]), ha) / (dot(ha, ha) or 1.0)
                                out_ = sub(j3[b_], tuple(x + tt * y for x, y in zip(j3[a_], ha)))
                                # the front of the shin is the foot's direction across the shin
                                ft = sub(toe, j3[c_]); sh = unit(sub(j3[c_], j3[b_]))
                                front = sub(ft, tuple(dot(ft, sh) * x for x in sh)) if sh else ft
                                if norm(out_) > 0.05 * norm(ha) and norm(front) > 0.3 * norm(ft):
                                    sign = 1 if dot(out_, front) >= 0 else -1
                            lim = limits["sagittal"][name]
                            angles[key] = (sign * flex, lim["min"], lim["max"], {a_, b_, c_}, ((a_, b_), (b_, c_)))
        # Front-view limits in a 3D rig, in the pelvis's own frame: a leg spread sideways
        # (hip abduction) and a knee bending sideways out of the plane of its thigh and foot.
        if j3 and all(k in j3 for k in ("hip_l", "hip_r")):
            lat = unit(sub(j3["hip_r"], j3["hip_l"]))
            fro = limits["frontal"]
            for s_ in SIDES:
                out_dir = lat if s_ == "r" else tuple(-x for x in lat) if lat else None
                hip, knee, ankle, toe = (j3.get(f"{k}_{s_}") for k in ("hip", "knee", "ankle", "toe"))
                if not (out_dir and hip and knee):
                    continue
                thigh = unit(sub(knee, hip))
                if thigh:
                    ab = math.degrees(math.asin(max(-1.0, min(1.0, dot(thigh, out_dir)))))
                    angles[f"hip_abduction_{s_}"] = (ab, -60, fro["hip_abduction"]["max"], {f"hip_{s_}", f"knee_{s_}"},
                                                     ((f"hip_{s_}", f"knee_{s_}"),))
                if ankle and toe and thigh:
                    # the foot points along the knee's bending plane; how far it points out of
                    # that plane (across the shin) is a sideways knee. The shin twists and the
                    # foot turns out a little at the ankle, hence the wider 3D allowance.
                    shin, ft = unit(sub(ankle, knee)), sub(toe, ankle)
                    hinge = unit(cross(thigh, shin)) if shin else None
                    fp = sub(ft, tuple(dot(ft, shin) * x for x in shin)) if shin else None
                    if hinge and norm(fp) > 0.3 * norm(ft) and math.degrees(math.acos(max(-1.0, min(1.0, dot(thigh, shin))))) > 20:
                        side = math.degrees(math.asin(min(1.0, abs(dot(hinge, unit(fp))))))
                        angles[f"knee_lateral_{s_}"] = (side, 0, fro["knee_lateral"].get("max_3d", 40), {f"knee_{s_}", f"ankle_{s_}"},
                                                        ((f"knee_{s_}", f"ankle_{s_}"),))
        # sitting cross-legged in a flat front view ("cross_legged": true, or both knees and the pelvis
        # on the ground): the crossed shins and the spread thighs are the pose, not a sideways bend
        sup = track["frames"][fi].get("supported") or []
        crossed = facing == "front" and not j3 and (track["frames"][fi].get("cross_legged") or (
            isinstance(sup, list) and {"pelvis", "knee_l", "knee_r"} <= set(sup)))
        for key, (v, lo, hi, inv, _) in angles.items():
            if crossed and key.startswith(("knee_lateral", "hip_abduction")):
                continue
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
                        # a projected 3D arm swinging through the camera axis sweeps a big flat angle
                        # for a small real move: only a warning there
                        axis = track.get("projected") and facing in ("front", "back") and key.startswith(("arm_swing", "forearm_swing"))
                        add(fi, "error" if P["blocking"] and not axis else "warn", "pop",
                            f"{key} jumps {abs(wrap(v - pv)):.0f}° in one frame ({speed:.0f}°/s)"
                            + (" (projected: check it is not a swing toward the camera)" if axis else ""), angles[key][3])
                    elif key.split("_")[0] in ("elbow", "knee") and facing in ("left", "right") \
                            and pv * v < 0 and min(abs(pv), abs(v)) > 15:
                        add(fi, "error", "snap", f"{key} flips bend direction ({pv:.0f}° -> {v:.0f}°)",
                            angles[key][3])
        prev = (angles, facing)

        # 4. balance: center of mass over what holds the body up
        fr = track["frames"][fi]
        if fr.get("zero_g") and torso:
            drift[fi] = (center_of_mass_2d(pts, track.get("mass")), torso,
                         bool(fr.get("contacts") or fr.get("supported")))
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
                listed = fr.get("supported") or []
                for k in listed:
                    if k in pts:
                        support.append(pts[k][0])
                        # a joint holding the body up must reach the ground; a joint resting on a prop lists
                        # the prop too (12% of the standing height: a thick cartoon knee or fist sits a little
                        # above the floor line); a head is on the ground when its circle is
                        # knees and a head on the floor; hands and elbows when the body is on the floor too
                        # (a lone "wrist_r" can push a wall or a block, a lone "pelvis" sits on a chair)
                        # ("floor" in the list: every listed joint, the pelvis of a floor sit too)
                        part = k.split("_")[0]
                        if not (part in ("knee", "head") or "floor" in listed or part in ("wrist", "elbow") and any(
                                x.split("_")[0] in ("knee", "ankle", "toe", "heel") for x in listed)):
                            continue
                        low = pts[k][1] - ((fr.get("head_radius", track.get("head_radius")) or 0) if k == "head" else 0)
                        # a drawn limb's thickness ("limb_width") is the tighter tolerance when given
                        lw = fr.get("limb_width", track.get("limb_width"))
                        tol = min(0.12 * max(height, tall), float(lw)) if lw else 0.12 * max(height, tall)
                        if all(x in pts or x == "floor" for x in listed) and low - ground > tol:
                            add(fi, "warn", "support_floating", f"{k} is listed as holding the body up but is "
                                f"{(low - ground) / max(height, tall):.0%} of the figure's standing height above the "
                                "ground (lower it to the ground, or list the prop it rests on)", {k})
                    elif k in fr.get("props", {}):
                        support.append(mirror * float(fr["props"][k][0]))
                margin = P["balance_margin"] * height
                if support and not (min(support) - margin <= com <= max(support) + margin):
                    off_balance.append(fi)

    # Floating in zero gravity ("zero_g": true): with nothing touched for three frames, the center
    # of mass drifts in a straight line at a steady speed; limbs may move, the hips move against them.
    for fi in sorted(drift):
        trio = [drift.get(fi + d) for d in (-1, 0, 1)]
        if all(trio) and not any(t[2] for t in trio) and all(t[0] for t in trio):
            (a, b, c), torso_ = [t[0] for t in trio], trio[1][1]
            acc = math.hypot(c[0] - 2 * b[0] + a[0], c[1] - 2 * b[1] + a[1])
            if acc > 0.04 * torso_:
                add(fi, "error", "zero_g_drift", f"floating body's center of mass speeds up or turns "
                    f"({acc / torso_:.2f} torso/frame²) with nothing touched; in free fall only a push "
                    "changes the drift", {"pelvis"})

    # A walk or run is off balance for a frame or two at every step; only a pose held
    # off balance (about a fifth of a second or longer) would really fall over.
    hold = max(2, math.ceil(0.2 * fps))  # 3 frames at 12 fps, so a pose held on twos still passes
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
            # in profile the two arms legitimately swing past each other (a run on twos at 12 fps);
            # there a swap only counts if an arm would have had to turn faster than a person can
            facing = f.get("facing") or infer_facing(pts)
            if facing in ("left", "right") and not three_d:
                step = P["max_joint_speed"] / float(track.get("fps", 12))
                turn = [abs(wrap(signed(sub(prev[f"elbow_{s}"], prev[f"shoulder_{s}"]), sub(pts[f"elbow_{s}"], pts[f"shoulder_{s}"]))))
                        for s in SIDES if all(f"{k}_{s}" in pts and f"{k}_{s}" in prev for k in ("shoulder", "elbow"))]
                # ...unless each wrist lands almost exactly on the other's spot: the labels jumped
                plausible = len(turn) == 2 and max(turn) <= step and swap >= 0.2 * keep
            else:
                plausible = False
            if keep > 0.8 * torso and swap < 0.35 * keep and not plausible:
                add(fi, "hand_swap", "left and right hands traded places in one frame", {
                    "shoulder_l", "elbow_l", "wrist_l", "shoulder_r", "elbow_r", "wrist_r"})
            elif facing not in ("left", "right") and not three_d and all(k in pts and k in prev for k in ("neck", "pelvis")):
                # facing the camera: both hands jumping across the body's midline in one frame
                def side_of(p, q):
                    a = sub(p["neck"], p["pelvis"])
                    return (a[0] * (q[1] - p["pelvis"][1]) - a[1] * (q[0] - p["pelvis"][0])) / (norm(a) or 1.0)
                was = [side_of(prev, prev[f"wrist_{s}"]) for s in SIDES]
                now = [side_of(pts, pts[f"wrist_{s}"]) for s in SIDES]
                moved = [norm(sub(pts[f"wrist_{s}"], prev[f"wrist_{s}"])) for s in SIDES]
                if all(w * n < 0 and min(abs(w), abs(n)) > 0.1 * torso for w, n in zip(was, now)) \
                        and min(moved) > 0.3 * torso:  # arms folding across the chest move less per frame
                    # a warning: arms folding across the chest fast look the same as a swap
                    add(fi, "hand_swap", "both arms cross the body in one frame, too fast to read; "
                        "add a passing pose", {
                        "shoulder_l", "elbow_l", "wrist_l", "shoulder_r", "elbow_r", "wrist_r"}, severity="warn")
        prev = pts

        # Head turned past the shoulders (3D tracks with a nose joint).
        if "_yaw" in f and abs(f["_yaw"]) > yaw_max + P["angle_tolerance"]:
            add(fi, "head_yaw", f"head turned {abs(f['_yaw']):.0f}° from the body (more than "
                f"{yaw_max}° turns it past the shoulders)", {"neck", "head"})

        # Which hand holds which prop must not change without a planned hand-off.
        holds = f.get("holds", {})
        if fi > 0 and not f.get("handoff"):
            for prop, side in holds.items():
                before = hands_of(frames[fi - 1].get("holds", {}).get(prop))
                now = hands_of(side)
                if before and now and not before & now:  # taking a second hand to it is fine
                    add(fi, "prop_hand_switch", f"{prop} jumps from the {_side(sorted(before))} hand to the "
                        f"{_side(sorted(now))} hand (mark \"handoff\": true if it is passed on purpose)",
                        {f"wrist_{x}" for x in before | now})
        # a planned change of hand: the taking hand must already be at the prop the frame before
        # (not jump onto it from the hip in one frame)
        if fi > 0 and f.get("handoff") and torso:
            pf = frames[fi - 1]
            ppts = raw_points(pf, P["min_confidence"])
            tol_h = f.get("hold_tolerance", track.get("hold_tolerance", 0.6))
            for prop, side in holds.items():
                before, now = hands_of(pf.get("holds", {}).get(prop)), hands_of(side)
                at = (pf.get("_props3d") or pf.get("props", {})).get(prop)
                for x in sorted(now - before) if before else []:
                    w = ppts.get(f"wrist_{x}")
                    if at and w and norm(sub(at, w)) > tol_h * torso:
                        add(fi, "prop_hand_switch", f"the {_side(x)} hand takes the {prop} from "
                            f"{norm(sub(at, w)) / torso:.1f} torso-lengths away; bring it to the {prop} a frame "
                            "before the hand-off", {f"wrist_{x}"})

        # A prop said to be in one hand must be drawn at that hand.
        # how far (in torso lengths) a held prop's point may sit from the wrist; put the prop's
        # point at the grip, a long prop's far end goes in its own "<prop>.<part>" point
        hold_tol = f.get("hold_tolerance", track.get("hold_tolerance", 0.6))
        for prop, side in holds.items():
            at = (f.get("_props3d") or f.get("props", {})).get(prop)
            just_passed = f.get("handoff") or (fi > 0 and frames[fi - 1].get("handoff"))
            if len(hands_of(side)) == 2:  # carried in both hands: drawn between them
                if at and torso and not just_passed and all(f"wrist_{x}" in pts for x in SIDES):
                    mid = tuple((a + b) / 2 for a, b in zip(pts["wrist_l"], pts["wrist_r"]))
                    if norm(sub(at, mid)) > hold_tol * torso:
                        add(fi, "prop_wrong_hand", f"{prop} should be carried in both hands but is drawn away "
                            "from them", {"wrist_l", "wrist_r"})
                    # grip points "<prop>.l" / "<prop>.r" from the prop's shape: each hand must reach its own
                    # (a big gear passes the midpoint test with the hands under it). Points copied from the
                    # wrists check nothing.
                    grips = f.get("_props3d") or f.get("props", {})
                    for x in SIDES:
                        g = grips.get(f"{prop}.{x}")
                        if g and torso and not just_passed and f"wrist_{x}" in pts:
                            span = hand_span(f, track, pts, x)
                            d = _seg_dist(g, *span) if span[0] != span[1] else norm(sub(g, span[0]))
                            o = grips.get(f"{prop}.{'r' if x == 'l' else 'l'}")
                            stacked = o and norm(sub(g[:2], o[:2])) < max(float(f.get("limb_width", track.get("limb_width", 0))), 0.05 * torso)
                            if d < 1e-6 * torso and fi == 0 and not stacked:  # grips one behind the other in side view
                                add(fi, "prop_wrong_hand", f"{prop}.{x} is the {_side(x)} wrist itself, so the grip "
                                    "check is empty; take the grip points from the prop's shape",
                                    {f"wrist_{x}"}, severity="warn")
                            elif x not in f.get("contacts", {}) and \
                                    d > f.get("contact_tolerance", track.get("contact_tolerance", 0.25)) * torso:
                                add(fi, "prop_wrong_hand", f"the {_side(x)} hand is {d / torso:.1f} torso-lengths from "
                                    f"its grip on the {prop}", {f"wrist_{x}"})
                continue
            side = next(iter(hands_of(side)), None)
            other = "r" if side == "l" else "l"
            if at and side and f"wrist_{side}" in pts and torso and not just_passed:
                d_own = norm(sub(at, pts[f"wrist_{side}"]))
                d_other = norm(sub(at, pts[f"wrist_{other}"])) if f"wrist_{other}" in pts else float("inf")
                if d_own > hold_tol * torso or d_other < d_own:
                    add(fi, "prop_wrong_hand", f"{prop} should be in the {_side(side)} hand but is drawn "
                        f"{'at the ' + _side(other) + ' hand' if d_other < d_own else 'away from it'}",
                        {f"wrist_{side}", f"elbow_{side}"})

        # A hand meant to touch something (a door, a table, a face) must reach it. A prop's own
        # point can have a contact too: {"cane.tip": "ground"} for a cane held at "cane".
        props = f.get("_props3d") or f.get("props", {})
        feet = [pts[k][1] for k in pts if k.split("_")[0] in ("ankle", "toe", "heel")]
        tol = f.get("contact_tolerance", track.get("contact_tolerance", 0.25))
        for src, target in f.get("contacts", {}).items():
            hand = src in SIDES
            frm = pts.get(f"wrist_{src}") if hand else props.get(src)
            span = hand_span(f, track, pts, src) if hand else (frm, frm)
            if not frm or not torso:
                continue
            if target == "ground":
                if three_d or not feet:
                    continue
                d = abs(frm[1] - max(feet))  # image y grows downward; the lowest foot is the ground
            else:
                at = props.get(target) if isinstance(target, str) else target
                if not at:
                    continue
                d = _seg_dist(at, *span) if span[0] != span[1] else norm(sub(at, frm))
            if d > tol * torso:
                label = target if isinstance(target, str) else "its target"
                who = f"the {_side(src)} hand" if hand else f"the {src}"
                add(fi, "contact_miss", f"{who} should touch {label} but stops {d / torso:.1f} torso-lengths away",
                    {f"wrist_{src}", f"elbow_{src}"} if hand else set())

        # Front view: a forearm sweeping across the face, unless the beat asks for it.
        if not three_d and f.get("facing", "front") == "front" and not f.get("face_cover") \
                and "head" in pts and "neck" in pts:
            r = f.get("head_radius", track.get("head_radius")) or 0.5 * norm(sub(pts["head"], pts["neck"]))
            for side in SIDES:
                ks = (f"shoulder_{side}", f"elbow_{side}", f"wrist_{side}")
                if side in f.get("contacts", {}) or any(side in hands_of(v) for v in f.get("holds", {}).values()):
                    continue  # a hand on the chin or holding a cup to the mouth is meant to be there
                if r and all(k in pts for k in ks):
                    crosses = (pts[ks[2]][0] - pts["head"][0]) * (pts[ks[0]][0] - pts["head"][0]) < 0
                    if _seg_dist(pts["head"], pts[ks[1]], pts[ks[2]]) < r and \
                            (crosses or norm(sub(pts[ks[2]], pts["head"])) < r):
                        add(fi, "arm_over_face", f"the {_side(side)} forearm crosses the face "
                            "(mark the frame \"face_cover\": true if the beat covers the face on purpose)",
                            {ks[1], ks[2], "head"}, severity="warn")
            # a held prop (a pot, a magnifier lens) over the face; give a long prop its far end as
            # "<prop>.<part>" (the grip is the prop's own point)
            for prop, hs, at in held_points(f):
                if r and norm(sub(at, pts["head"])) < 0.8 * r:
                    add(fi, "arm_over_face", f"the {prop} covers the face "
                        "(mark the frame \"face_cover\": true if the beat covers the face on purpose)",
                        {f"wrist_{hs}", "head"}, severity="warn")
                    break

        # Front view, standing: with "body_width" (the drawn torso's width at the chest, track units,
        # on the track or a frame), a shoulder joint inside the torso outline or an arm hanging over
        # the chest instead of beside it is a warning (every joint angle is legal, but the arms lie on
        # the body). Joints alone cannot show this: the drawn torso can be wider than the shoulders.
        facing = f.get("facing") or (infer_facing(pts) if pts else None)
        bw = f.get("body_width", track.get("body_width"))
        if bw and not three_d and facing == "front" and not f.get("airborne") and "neck" in pts:
            # a tilted body (a roly-poly rocking, a lean) is measured across its own neck-pelvis axis
            pts0 = pts
            if "pelvis" in pts:
                dx, dy = sub(pts["pelvis"], pts["neck"])
                tilt = math.atan2(dx, dy)
                if abs(tilt) > math.radians(5):
                    c, sn = math.cos(tilt), math.sin(tilt)
                    nx, ny = pts["neck"]
                    pts = {k: (nx + (x - nx) * c - (y - ny) * sn, ny + (x - nx) * sn + (y - ny) * c)
                           for k, (x, y) in pts.items()}
            mid, half = pts["neck"][0], float(bw) / 2
            # the drawn body's half-width at a height: "body_profile" [[t, half_width], ...] from the
            # pelvis (t=0) to the neck (t=1), or a straight taper from "hip_width" to "body_width"
            prof = f.get("body_profile", track.get("body_profile"))
            hw = float(f.get("hip_width", track.get("hip_width", bw))) / 2
            def half_at(y):
                if "pelvis" not in pts or pts["pelvis"][1] == pts["neck"][1]:
                    return half
                t = max(0.0, min(1.0, (pts["pelvis"][1] - y) / (pts["pelvis"][1] - pts["neck"][1])))
                if prof:
                    pr = sorted(prof)
                    for (t0, w0), (t1, w1) in zip(pr, pr[1:]):
                        if t0 <= t <= t1:
                            return w0 + (w1 - w0) * (t - t0) / ((t1 - t0) or 1)
                    return pr[0][1] if t < pr[0][0] else pr[-1][1]
                return hw + (half - hw) * t
            # the drawn forearm and hand have thickness: "limb_width" (track units), and the hand
            # reaches "hand_length" past the wrist
            lw = float(f.get("limb_width", track.get("limb_width", 0))) / 2
            def arm_points(ks):
                e, w = pts[ks[1]], pts[ks[2]]
                out = [w, tuple((a + b) / 2 for a, b in zip(e, w))]
                if not (prof or lw or "hip_width" in f or "hip_width" in track):
                    return out  # chest width only: the wrist and forearm, as before
                tip = hand_span(f, track, pts, ks[2][-1])[1]
                return out + ([tip] if tip and tip != w else [])
            down = lambda a, b: math.degrees(math.atan2(abs(b[0] - a[0]), b[1] - a[1]))  # 0 = straight down
            inside_elbow = lambda sd: f"elbow_{sd}" in pts and \
                abs(pts[f"elbow_{sd}"][0] - mid) < 0.6 * half_at(pts[f"elbow_{sd}"][1])
            # both upper arms folded into the chest with the hands out past the shoulders: the elbows bend
            # the wrong way (an IK solver picked the inner elbow); crossed arms keep the hands in
            arm = [f"{k}_{sd}" for sd in SIDES for k in ("shoulder", "elbow", "wrist")]
            if all(k in pts for k in arm) and inside_elbow("l") and inside_elbow("r") and all(
                    (pts[f"wrist_{sd}"][0] - mid) * (pts[f"shoulder_{sd}"][0] - mid) > 0
                    and abs(pts[f"wrist_{sd}"][0] - mid) > abs(pts[f"shoulder_{sd}"][0] - mid) for sd in SIDES):
                add(fi, "elbow_inverted", "both elbows fold into the chest while the hands sit out past the shoulders, "
                    "so the elbows bend the wrong way; put the elbows at the sides and bring the hands in front",
                    set(arm))
            for side in SIDES:
                ks = (f"shoulder_{side}", f"elbow_{side}", f"wrist_{side}")
                if ks[0] in pts and abs(pts[ks[0]][0] - mid) < 0.8 * half:
                    add(fi, "arm_over_body", f"the {_side(side)} shoulder sits inside the torso outline; put it at "
                        "the edge of the torso", {ks[0]}, severity="warn")
                    continue
                busy = side in f.get("contacts", {}) or any(side in hands_of(v) for v in f.get("holds", {}).values())
                if not busy and all(k in pts for k in ks) and pts[ks[2]][1] > pts[ks[1]][1] > pts[ks[0]][1] \
                        and down(pts[ks[0]], pts[ks[1]]) < 25 and down(pts[ks[1]], pts[ks[2]]) < 25 \
                        and any(abs(q[0] - mid) - lw < half_at(q[1]) for q in arm_points(ks)):
                    add(fi, "arm_over_body", f"the {_side(side)} arm hangs over the body, not beside it",
                        set(ks), severity="warn")
                # an upper arm folded in across the chest ("chicken wing"): the elbow well inside the
                # torso outline and the forearm angling down and back out to its own side while the hand
                # reaches for nothing. A raised or inward forearm (think, facepalm, gasp) or both elbows
                # folded in (crossed arms) is a pose.
                elif not busy and all(k in pts for k in ks) and "pelvis" in pts \
                        and inside_elbow(side) and not inside_elbow("lr"[side == "l"]) \
                        and pts[ks[2]][1] - pts[ks[1]][1] > 0.25 * math.dist(pts[ks[1]], pts[ks[2]]) \
                        and (pts[ks[2]][0] - mid) * (pts[ks[0]][0] - mid) > 0 \
                        and abs(pts[ks[2]][0] - mid) > abs(pts[ks[1]][0] - mid) \
                        and pts[ks[0]][1] < pts[ks[1]][1] < pts["pelvis"][1]:
                    add(fi, "arm_over_body", f"the {_side(side)} upper arm folds in across the chest (elbow inside the "
                        "torso outline)", {ks[0], ks[1]}, severity="warn")
                # reaching past the body to the far side (both hands on a wheel rim with the forearms
                # crossed over the chest): held or not, the grip is outside the torso but the arm is on it
                elif all(k in pts for k in ks) and (pts[ks[1]][0] - mid) * (pts[ks[2]][0] - mid) < 0 \
                        and pts[ks[2]][1] > pts[ks[0]][1] \
                        and abs(pts[ks[2]][0] - mid) > half and "pelvis" in pts \
                        and pts[ks[0]][1] <= (pts[ks[1]][1] + pts[ks[2]][1]) / 2 <= pts["pelvis"][1]:
                    add(fi, "arm_over_body", f"the {_side(side)} forearm crosses the chest to reach the far side; "
                        "grip on the near side of the body instead", {ks[1], ks[2]}, severity="warn")
            pts = pts0

        # Side view: the near arm (the right arm when facing right) cutting across the head
        # hides the face; a hand holding a prop or touching something there is meant to.
        facing = f.get("facing") or (infer_facing(pts) if pts else None)
        if not three_d and facing in ("left", "right") and not f.get("face_cover") \
                and "head" in pts and "neck" in pts:
            side = facing[0]
            ks = (f"shoulder_{side}", f"elbow_{side}", f"wrist_{side}")
            r = f.get("head_radius", track.get("head_radius")) or 0.5 * norm(sub(pts["head"], pts["neck"]))
            # a hand holding a cup at the mouth is meant to be there; one holding a ball cocked behind
            # the head for a throw is not, so only a prop at the face excuses the arm
            busy = side in f.get("contacts", {}) or any(
                hs == side and r and norm(sub(at, pts["head"])) < 1.3 * r and at[1] >= pts["head"][1] - 0.3 * r
                for _, hs, at in held_points(f, both=True))
            ahead = 1 if facing == "right" else -1
            if r and not busy and all(k in pts for k in ks) and any(
                    _seg_dist(pts["head"], a, b) < r and (_closest(pts["head"], a, b)[0] - pts["head"][0]) * ahead > 0
                    for a, b in ((tuple(p + 0.4 * (q - p) for p, q in zip(pts[ks[0]], pts[ks[1]])), pts[ks[1]]),
                                 (pts[ks[1]], pts[ks[2]]))):  # the face half, not the back of the head; not the shoulder
                add(fi, "arm_over_face", f"the near ({_side(side)}) arm crosses the face in side view "
                    "(mark the frame \"face_cover\": true if the beat covers the face on purpose)",
                    {ks[1], ks[2], "head"}, severity="warn")
            # a held prop (a raised ball, a book) sitting on the face; a cup at the mouth stays at the edge
            for prop, hs, at in held_points(f):
                if r and norm(sub(at, pts["head"])) < 0.6 * r and (at[0] - pts["head"][0]) * ahead >= 0:
                    add(fi, "arm_over_face", f"the {prop} covers the face in side view "
                        "(mark the frame \"face_cover\": true if the beat covers the face on purpose)",
                        {f"wrist_{hs}", "head"}, severity="warn")

        # Front view: a raised forearm lying across the face (a cheer drawn with the arms over a big
        # head); a hand touching the face or holding something there is meant to be there
        if not three_d and facing == "front" and not f.get("face_cover") and "head" in pts and "neck" in pts:
            r = f.get("head_radius", track.get("head_radius")) or 0.5 * norm(sub(pts["head"], pts["neck"]))
            for side in SIDES:
                ks = (f"elbow_{side}", f"wrist_{side}")
                busy = side in f.get("contacts", {}) or any(hs == side for _, hs, _ in held_points(f, both=True))
                # only an arm raised past the head: a hand at the brow, the glasses or the face (salute,
                # facepalm, think) is a pose
                if r and not busy and all(k in pts for k in ks) and pts[ks[1]][1] < pts["head"][1] - 0.5 * r \
                        and _seg_dist(pts["head"], *(pts[k] for k in ks)) < r + max(
                            float(f.get("limb_width", track.get("limb_width", 0))) / 2, 0.1 * r):
                    add(fi, "arm_over_face", f"the {_side(side)} forearm lies over the head in front view; raise it "
                        "clear of the head (mark the frame \"face_cover\": true if the beat covers the face on purpose)",
                        set(ks) | {"head"}, severity="warn")

        # Nothing goes through the floor: with "ground_y" (image y of the ground line, y down),
        # a head, hand or foot below it is an error (a roll or bow sinking into the ground).
        gy = f.get("ground_y", track.get("ground_y"))
        if gy is not None and not three_d and torso:
            low = dict((k, p[1]) for k, p in pts.items())
            if "head" in pts and "neck" in pts:  # the drawn head is a disc, not a point
                low["head"] += f.get("head_radius", track.get("head_radius")) or 0.5 * norm(sub(pts["head"], pts["neck"]))
            sunk = sorted(k for k, y in low.items() if y - float(gy) > 0.05 * torso)
            if sunk:
                add(fi, "below_ground", f"{', '.join(sunk)} below the ground line "
                    f"({max(low[k] for k in sunk) - float(gy):.0f} px)", set(sunk))

        # The body stays outside solid props: "solids": {"block": [w, h]} (or [w, h, d] in 3D) is a
        # box of that size centered on the prop's point; a head or body joint inside it fails
        # (a push with the head through the block). Hands may touch or grip it.
        solids = f.get("solids", track.get("solids")) or {}
        if solids and torso:
            src = f.get("_joints3d") or pts
            where = f.get("_props3d") or f.get("props", {})
            for prop, size in solids.items():
                c = where.get(prop)
                if not c or len(size) < len(c[:2]):
                    continue
                inside = sorted(k for k, q in src.items() if k.split("_")[0] not in ("wrist", "hand", "finger", "thumb")
                                and all(abs(q[i] - c[i]) < size[i] / 2 - 0.05 * torso for i in range(min(len(c), len(size), len(q)))))
                if inside:
                    add(fi, "body_in_prop", f"{', '.join(inside)} inside the {prop}", set(inside))

        # Hand shape (thumb side) must match the arm it is on.
        for side, h in f.get("hands", {}).items():
            if h and h.get("looks_like") in ("l", "r") and h["looks_like"] != side \
                    and h.get("score", 1.0) >= 0.8:
                add(fi, "mirrored_hand", f"the hand on the {_side(side)} arm is drawn as a "
                    f"{_side(h['looks_like'])} hand (thumb on the wrong side)",
                    {f"wrist_{side}", f"elbow_{side}"})
    return issues


def _closest(p, a, b):
    """Point on segment a-b closest to p."""
    ab = sub(b, a)
    t = max(0.0, min(1.0, dot(sub(p, a), ab) / (dot(ab, ab) or 1.0)))
    return tuple(x + t * y for x, y in zip(a, ab))


def _seg_dist(p, a, b):
    """Distance from point p to segment a-b."""
    ab, ap = sub(b, a), sub(p, a)
    t = max(0.0, min(1.0, (ap[0] * ab[0] + ap[1] * ab[1]) / max(ab[0] ** 2 + ab[1] ** 2, 1e-9)))
    return norm(sub(p, (a[0] + ab[0] * t, a[1] + ab[1] * t)))


def _seg_seg(a, b, c, d):
    """Distance between segments a-b and c-d (0 when they cross)."""
    cross = lambda o, p, q: (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])
    if cross(a, b, c) * cross(a, b, d) < 0 and cross(c, d, a) * cross(c, d, b) < 0:
        return 0.0
    return min(_seg_dist(a, c, d), _seg_dist(b, c, d), _seg_dist(c, a, b), _seg_dist(d, a, b))


def _side(s): return {"l": "left", "r": "right"}.get(s, s) if isinstance(s, str) else " and ".join(map(_side, s))


def held_points(f, both=False):
    """(prop, hand, point) for every point of every held prop: its grip and its "<prop>.<part>" points
    (with both=True, once per holding hand)."""
    props = f.get("props", {})
    for prop, v in f.get("holds", {}).items():
        for hs in sorted(hands_of(v))[:None if both else 1]:
            for k, at in props.items():
                if at and (k == prop or k.startswith(prop + ".")):
                    yield (k, hs, at)


def hands_of(v):
    """A "holds" value as a set of sides: "r", or ["l", "r"] (or "both") for a two-handed carry."""
    if v in ("both", "b", "lr", "rl"):
        return {"l", "r"}
    return set() if not v else {v} if isinstance(v, str) else set(v)


def hand_span(f, track, pts, side):
    """The hand as a segment from the wrist to its tip: "hand_length" (track units) on the track or
    frame extends it along the forearm, for mitten or glove hands that reach past the wrist."""
    w, e = pts.get(f"wrist_{side}"), pts.get(f"elbow_{side}")
    hl = f.get("hand_length", track.get("hand_length"))
    if not (w and e and hl):
        return w, w
    d = unit(sub(w, e))
    return w, (tuple(a + hl * b for a, b in zip(w, d)) if d else w)


def check_sequence(tracks):
    """Across clips: a prop must stay in the same hand from the end of one clip to the start of the next."""
    issues = []
    for k in range(len(tracks) - 1):
        a, b = tracks[k]["frames"], tracks[k + 1]["frames"]
        if not a or not b or b[0].get("handoff"):
            continue
        end, start = a[-1].get("holds", {}), b[0].get("holds", {})
        for prop, side in start.items():
            if hands_of(end.get(prop)) and hands_of(side) and not hands_of(end[prop]) & hands_of(side):
                issues.append({"frame": None, "clip": k + 1, "severity": "error", "kind": "prop_hand_switch",
                               "message": f"{prop} ends clip {k + 1} in the {_side(end[prop])} hand but starts "
                                          f"clip {k + 2} in the {_side(side)} hand", "joints": []})
    return issues


def check_scene(tracks):
    """Several characters of one shot, frame by frame in the same coordinates (each track has a
    "name"): a prop passed from one to another must be at the same place in both hands at the
    pass, a contact naming another character's joint ("contacts": {"r": "Kip.wrist_l"} for a
    high five) must reach it, and one head must not sit inside another."""
    issues = []
    for t in tracks:
        as_joint_track(t)
    def add(fi, kind, msg, severity="error"):
        issues.append({"frame": fi, "severity": severity, "kind": kind, "message": msg, "joints": []})
    names = [t.get("name") or (t.get("character") or "").split(" (")[0] or f"track {k + 1}" for k, t in enumerate(tracks)]
    def torso(f):
        j = f.get("joints", {})
        return norm(sub(j["neck"], j["pelvis"])) if "neck" in j and "pelvis" in j else None
    def head_r(t, f):
        j = f.get("joints", {})
        return f.get("head_radius", t.get("head_radius")) or (0.5 * norm(sub(j["head"], j["neck"])) if "head" in j and "neck" in j else None)
    n = min(len(t["frames"]) for t in tracks)
    for fi in range(n):
        fr = [t["frames"][fi] for t in tracks]
        for a, (ta, fa) in enumerate(zip(tracks, fr)):
            T = torso(fa)
            if not T:
                continue
            tol = fa.get("contact_tolerance", ta.get("contact_tolerance", 0.25))
            # a prop held by both at once (the hand-off frames): the giver's and the receiver's hands
            # meet, and the prop is drawn in one place
            for prop, va in (fa.get("holds") or {}).items():
                for b in range(a + 1, len(tracks)):
                    fb = fr[b]
                    if prop not in (fb.get("holds") or {}):
                        continue
                    pa, pb = (fa.get("props") or {}).get(prop), (fb.get("props") or {}).get(prop)
                    if pa and pb and norm(sub(pa, pb)) > 0.35 * T:
                        add(fi, "handoff_gap", f"{names[a]} and {names[b]} both hold the {prop}, but it is drawn "
                            f"{norm(sub(pa, pb)) / T:.1f} torso-lengths apart in their hands")
                        continue
                    wa = [fa["joints"][f"wrist_{x}"] for x in hands_of(va) if f"wrist_{x}" in fa.get("joints", {})]
                    wb = [fb["joints"][f"wrist_{x}"] for x in hands_of(fb["holds"][prop]) if f"wrist_{x}" in fb.get("joints", {})]
                    gap = min((norm(sub(p, q)) for p in wa for q in wb), default=0)
                    reach = (fa.get("hand_length", ta.get("hand_length")) or 0) + (fb.get("hand_length", tracks[b].get("hand_length")) or 0)
                    # a big prop gripped at opposite edges: each holder's own grip points ("gear.l", "gear.r")
                    # are checked against that holder's hands, so the hands may be far apart
                    gripped = pa and pb and all(any(f"{prop}.{x}" in (fx.get("props") or {}) for x in hands_of(fx["holds"][prop]))
                                                for fx in (fa, fb))
                    if gap - reach > 0.35 * T and not gripped:
                        add(fi, "handoff_gap", f"{names[a]} and {names[b]} both hold the {prop}, but their hands are "
                            f"{gap / T:.1f} torso-lengths apart; both hands must be on it (for a big prop held at "
                            f"opposite edges, give each holder grip points \"{prop}.l\" / \"{prop}.r\" from the prop's "
                            f"shape and the same \"{prop}\" point)")
            # a prop leaving this character's hand appears at the same place in the receiver's
            if fi:
                for prop in (tracks[a]["frames"][fi - 1].get("holds") or {}):
                    if prop in (fa.get("holds") or {}):
                        continue
                    for b, fb in enumerate(fr):
                        if b != a and prop in (fb.get("holds") or {}) and prop not in (tracks[b]["frames"][fi - 1].get("holds") or {}):
                            pa, pb = tracks[a]["frames"][fi - 1].get("props", {}).get(prop), fb.get("props", {}).get(prop)
                            if pa and pb and norm(sub(pa, pb)) > 0.35 * T:
                                add(fi, "handoff_gap", f"{prop} jumps {norm(sub(pa, pb)) / T:.1f} torso-lengths from "
                                    f"{names[a]} to {names[b]} at the hand-off")
            # hands meeting another character's joint (high five, fist bump, handshake)
            for side, target in (fa.get("contacts") or {}).items():
                if side not in SIDES or not isinstance(target, str) or "." not in target:
                    continue
                who, joint = target.split(".", 1)
                if who in names and f"wrist_{side}" in fa.get("joints", {}):
                    other = fr[names.index(who)].get("joints", {})
                    # another character's joint, or a point of what they hold ("Mam.ladle.tip")
                    at = other.get(joint) or (fr[names.index(who)].get("props") or {}).get(joint)
                    if at:
                        span = hand_span(fa, ta, fa["joints"], side)
                        d = _seg_dist(at, *span) if span[0] != span[1] else norm(sub(span[0], at))
                        if d > tol * T:
                            add(fi, "contact_miss", f"{names[a]}'s {_side(side)} hand should meet {who}'s "
                                f"{joint.replace('_l', ' (left)').replace('_r', ' (right)')} but stops {d / T:.1f} torso-lengths away")
            # one head inside another
            for b in range(a + 1, len(tracks)):
                ja, jb = fa.get("joints", {}), fr[b].get("joints", {})
                ra, rb = head_r(ta, fa), head_r(tracks[b], fr[b])
                if "head" in ja and "head" in jb and ra and rb and not (fa.get("overlap_ok") or fr[b].get("overlap_ok")):
                    d = norm(sub(ja["head"], jb["head"]))
                    if d < max(ra, rb):
                        add(fi, "head_overlap", f"{names[a]}'s and {names[b]}'s heads overlap (mark \"overlap_ok\": true "
                            "if one passes behind the other)")
                    elif d < 0.97 * (ra + rb):  # drawn heads partly overlapping
                        add(fi, "head_overlap", f"{names[a]}'s and {names[b]}'s heads touch or partly overlap "
                            f"({d:.0f} apart, radii {ra:.0f} + {rb:.0f})", severity="warn")
            # a snout, bill or beak ("snout": its length from the head centre, track units) pokes ahead
            # of the head in the facing direction; its tip must stay out of another head
            sn = fa.get("snout", ta.get("snout"))
            ja = fa.get("joints", {})
            ahead = {"right": 1, "left": -1}.get(fa.get("facing") or (infer_facing(ja) if ja else None))
            # "snout_dir": [dx, dy] (image axes, y down) when it does not point straight ahead
            sd = fa.get("snout_dir", ta.get("snout_dir"))
            if sn and (ahead or sd) and "head" in ja and not fa.get("overlap_ok"):
                u = unit(tuple(float(x) for x in sd)) if sd else (ahead, 0.0)
                tip = (ja["head"][0] + u[0] * float(sn), ja["head"][1] + u[1] * float(sn))
                for b in range(len(tracks)):
                    jb, rb = fr[b].get("joints", {}), head_r(tracks[b], fr[b])
                    if b == a or fr[b].get("overlap_ok"):
                        continue
                    if "head" in jb and rb and _seg_dist(jb["head"], ja["head"], tip) < rb:
                        add(fi, "head_overlap", f"{names[a]}'s snout pokes into {names[b]}'s head "
                            f"({rb - _seg_dist(jb['head'], ja['head'], tip):.0f} px inside; mark \"overlap_ok\": true "
                            "if one passes behind the other)")
                    elif "neck" in jb and "pelvis" in jb and _seg_seg(ja["head"], tip, jb["neck"], jb["pelvis"]) < float(
                            fr[b].get("body_width", tracks[b].get("body_width", 0.5 * (torso(fr[b]) or 0)))) / 2:
                        add(fi, "head_overlap", f"{names[a]}'s snout pokes into {names[b]}'s body (mark \"overlap_ok\": "
                            "true if one passes behind the other)", severity="warn")
            # bodies as solids ("solid_body": true on both tracks): a torso or limb of one passing through
            # the other's torso (a flying body through a standing one)
            for b in range(a + 1, len(tracks)):
                fb, tb = fr[b], tracks[b]
                ja, jb = fa.get("joints", {}), fb.get("joints", {})
                if not (fa.get("solid_body", ta.get("solid_body")) and fb.get("solid_body", tb.get("solid_body"))) \
                        or fa.get("overlap_ok") or fb.get("overlap_ok") or not all("neck" in j and "pelvis" in j for j in (ja, jb)):
                    continue
                Tb = torso(fb) or T
                half = lambda f, t, T_: float(f.get("body_width", t.get("body_width", 0.5 * T_))) / 2
                limb = lambda f, t, T_: float(f.get("limb_width", t.get("limb_width", 0.12 * T_))) / 2
                def parts(j, f, t, T_):
                    yield "body", (j["neck"], j["pelvis"]), half(f, t, T_)
                    if "head" in j and head_r(t, f):
                        yield "head", (j["head"], j["head"]), head_r(t, f)
                    for x, y in (("shoulder", "elbow"), ("elbow", "wrist"), ("hip", "knee"), ("knee", "ankle"), ("ankle", "toe")):
                        for sd in SIDES:
                            if f"{x}_{sd}" in j and f"{y}_{sd}" in j:
                                yield f"{_side(sd)} {'arm' if x in ('shoulder', 'elbow') else 'leg'}", \
                                    (j[f"{x}_{sd}"], j[f"{y}_{sd}"]), limb(f, t, T_)
                hit = None
                for (pn, sa, wa) in parts(ja, fa, ta, T):
                    for (qn, sb, wb) in parts(jb, fb, tb, Tb):
                        if {pn, qn} & {"body", "head"} and not {pn, qn} == {"head"} and _seg_seg(*sa, *sb) < 0.9 * (wa + wb):
                            hit = (pn, qn)
                            break
                    if hit:
                        break
                if hit:
                    add(fi, "body_overlap", f"{names[a]}'s {hit[0]} passes through {names[b]}'s {hit[1]} (mark "
                        "\"overlap_ok\": true if one passes behind the other)", severity="warn")
            # another character's held prop or body over this one's face (a raised ball, walking across)
            for b in range(len(tracks)):
                jb = fr[b].get("joints", {})
                rb = head_r(tracks[b], fr[b])
                if b == a or "head" not in jb or not rb or fa.get("overlap_ok") or fr[b].get("overlap_ok"):
                    continue
                ja = fa.get("joints", {})
                cover = next((k for k, _, at in held_points(fa) if norm(sub(at, jb["head"])) < 0.8 * rb), None)
                if not cover and "neck" in ja and "pelvis" in ja and _seg_dist(jb["head"], ja["neck"], ja["pelvis"]) < 0.8 * rb:
                    cover = "body"
                if cover:
                    add(fi, "face_covered", f"{names[a]}'s {cover} covers {names[b]}'s face (mark \"overlap_ok\": true "
                        "if one passes behind the other)", severity="warn")
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
    c.add_argument("--scene", action="store_true",
                   help="the tracks are characters of one shot (same frames, same coordinates), not clips in order")
    f = sub_.add_parser("fix", help="repair a rig track"); f.add_argument("track"); f.add_argument("-o", "--out", required=True)
    a = ap.parse_args(argv)
    paths = [a.track] if a.cmd == "fix" else a.tracks
    try:
        tracks = [json.loads(Path(p).read_text()) for p in paths]
    except (OSError, ValueError) as e:
        print(f"cannot read track: {e}", file=sys.stderr); return 2
    for p, t in zip(paths, tracks):
        if not isinstance(t, dict) or not isinstance(t.get("frames"), list):
            print(f"{p}: not a pose track (needs a \"frames\" list)", file=sys.stderr); return 2
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
    seq = check_scene(tracks) if a.scene else check_sequence(tracks)
    if a.scene:
        # each character's result carries the scene issues that name it, and fails on a scene error,
        # so a summary that reads only the clips does not miss them
        for k, (t, r) in enumerate(zip(tracks, results)):
            name = t.get("name") or (t.get("character") or "").split(" (")[0] or f"track {k + 1}"
            r["scene_issues"] = [i for i in seq if re.search(rf"(?<!\w){re.escape(name)}(?!\w)", i["message"])]
            if any(i.get("severity", "error") == "error" for i in r["scene_issues"]):
                r["status"], r["passed"] = "FAIL", False
    passed = all(r["status"] != "FAIL" for r in results) and not any(i.get("severity", "error") == "error" for i in seq)
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
        print(f"{i.get('severity', 'error').upper():5} {'frame ' + str(i['frame']) if a.scene else 'between clips'}: {i['message']}")
    if len(paths) > 1:
        print("PASS" if passed else "FAIL", "(whole scene)" if a.scene else "(all clips)")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
