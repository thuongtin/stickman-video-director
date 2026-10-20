#!/usr/bin/env python3
"""Draw the Style 2 default lead (buzz cut, dark rectangular glasses, open plaid flannel over a white tee, jeans;
same body as upstream's red-beanie lead) from a code rig.

Writes, next to this file:
  sheet.png          character sheet: turnaround, expressions, poses, palette
  motion.gif         two-shot motion clip (side walk, then front wave and glasses push)
  tracks/*.json      every pose drawn above, as posture-gate tracks (tests/verify-lead-character.py gates them)

Pillow is the only dependency. Nothing here is AI-generated: every frame is drawn from the joints in tracks/.
"""
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SS = 3  # supersampling

# rest lengths at scale 1 (track units = pixels at scale 1)
LEN = {"torso": 52, "head": 22, "upper_arm": 25, "forearm": 24, "thigh": 37, "shin": 35, "foot": 10}
HEAD_R = 21
INK = (24, 24, 24)
HAIR = (34, 30, 30)
FRAME = (40, 38, 38)
FLANNEL = (176, 38, 40)    # open red flannel shirt
PLAID = (34, 40, 78)       # navy check bands
CUFF = (128, 26, 30)       # rolled cuffs and collar
TEE_WHITE = (250, 250, 248)
JEANS = (46, 74, 120)      # dark blue jeans
SKIN = (255, 255, 255)     # the head stays white like every Style 2 figure
STUBBLE = (150, 150, 150)
PEN = (40, 200, 230)


def rot(v, deg):
    a = math.radians(deg)
    return (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a))


def add(p, v, k=1.0):
    return (p[0] + v[0] * k, p[1] + v[1] * k)


def place(j, x, ground, s, low=None):
    """Math coords (y up, pelvis at 0) -> image coords with the lowest foot point on the ground line."""
    if low is None:
        low = min(min(j[f"ankle_{k}"][1], j[f"toe_{k}"][1]) for k in ("l", "r"))
    return {k: [round(x + p[0] * s, 2), round(ground - (p[1] - low) * s, 2)] for k, p in j.items()}


# ---------------------------------------------------------------- side view (facing right)
def side_pose(a, x=200.0, ground=300.0, s=1.0, lift=0.0):
    """lean (+ = torso forward), neck (+ = chin down), shoulder/hip (+ = forward),
    elbow/knee (+ = fold), ankle (+ = toes up). Own right side is toward the camera."""
    up = rot((0, 1), -a.get("lean", 0))
    down = (-up[0], -up[1])
    pelvis = (0.0, 0.0)
    neck = add(pelvis, up, LEN["torso"])
    j = {"pelvis": pelvis, "neck": neck, "head": add(neck, rot(up, -a.get("neck", 0)), LEN["head"])}
    for k in ("l", "r"):
        ua = rot(down, a[f"shoulder_{k}"]); fa = rot(ua, a[f"elbow_{k}"])
        th = rot(down, a[f"hip_{k}"]); sh = rot(th, -a[f"knee_{k}"]); ft = rot(sh, 90 + a.get(f"ankle_{k}", 0))
        j[f"shoulder_{k}"] = add(neck, down, 4)
        j[f"elbow_{k}"] = add(j[f"shoulder_{k}"], ua, LEN["upper_arm"])
        j[f"wrist_{k}"] = add(j[f"elbow_{k}"], fa, LEN["forearm"])
        j[f"hip_{k}"] = pelvis
        j[f"knee_{k}"] = add(pelvis, th, LEN["thigh"]); j[f"ankle_{k}"] = add(j[f"knee_{k}"], sh, LEN["shin"])
        j[f"toe_{k}"] = add(j[f"ankle_{k}"], ft, LEN["foot"])
    low = min(min(j[f"ankle_{k}"][1], j[f"toe_{k}"][1]) for k in ("l", "r")) - lift
    return place(j, x, ground, s, low)


def stand_side():
    return {"lean": 2, "neck": 3, "shoulder_l": -8, "elbow_l": 22, "shoulder_r": 8, "elbow_r": 26,
            "hip_l": -5, "knee_l": 3, "hip_r": 5, "knee_r": 6}


def walk(t):
    ph = 2 * math.pi * t
    a = {"lean": 4, "neck": 4}
    for k, off in (("l", 0), ("r", math.pi)):
        a[f"hip_{k}"] = 22 * math.sin(ph + off)
        a[f"knee_{k}"] = 8 + 40 * max(0.0, math.sin(ph + off + 1.2))
        a[f"ankle_{k}"] = 8 * math.sin(ph + off)
        a[f"shoulder_{k}"] = -20 * math.sin(ph + off)
        a[f"elbow_{k}"] = 25 + 10 * math.sin(ph + off)
    return a


def mirror(j, cx):
    """A facing-right drawing turned to face left: mirror x and trade own sides, so the own left side is near."""
    out = {}
    for k, p in j.items():
        k2 = k[:-2] + ("_r" if k.endswith("_l") else "_l") if k.endswith(("_l", "_r")) else k
        out[k2] = [round(2 * cx - p[0], 2), p[1]]
    return out


# ---------------------------------------------------------------- front view
def front_pose(a, x=200.0, ground=300.0, s=1.0, lift=0.0):
    """abd_* = arm out sideways (+ = away from body), elb_* = elbow fold toward the head side,
    leg_* = leg out sideways, knee_* = knee bend shown as a shorter-looking leg (kept straight in 2D).
    Own left side is on screen right."""
    pelvis = (0.0, 0.0); neck = (0.0, LEN["torso"])
    j = {"pelvis": pelvis, "neck": neck, "head": (0.0, LEN["torso"] + LEN["head"])}
    for k, out in (("l", 1), ("r", -1)):
        sh = (out * 15.0, LEN["torso"] - 5); hp = (out * 8.0, 0.0)
        ua = rot((0, -1), out * a[f"abd_{k}"]); fa = rot(ua, out * a[f"elb_{k}"])
        th = rot((0, -1), out * a.get(f"leg_{k}", 5)); shin = rot(th, -out * a.get(f"knee_{k}", 0))
        j[f"shoulder_{k}"] = sh; j[f"elbow_{k}"] = add(sh, ua, LEN["upper_arm"])
        j[f"wrist_{k}"] = add(j[f"elbow_{k}"], fa, LEN["forearm"])
        j[f"hip_{k}"] = hp; j[f"knee_{k}"] = add(hp, th, LEN["thigh"])
        j[f"ankle_{k}"] = add(j[f"knee_{k}"], shin, LEN["shin"])
        j[f"toe_{k}"] = add(j[f"ankle_{k}"], (out * 5.0, -2.0))
    low = min(j[f"toe_{k}"][1] for k in ("l", "r")) - lift
    return place(j, x, ground, s, low)


def stand_front():
    return {"abd_l": 9, "elb_l": 8, "abd_r": 9, "elb_r": 8, "leg_l": 6, "leg_r": 6}


def ik_front(a, k, target_math):
    """Set abd_k/elb_k so the wrist reaches target (math coords relative to pelvis), elbow out to the side."""
    out = 1 if k == "l" else -1
    sh = (out * 15.0, LEN["torso"] - 5)
    dx, dy = target_math[0] - sh[0], target_math[1] - sh[1]
    d = min(math.hypot(dx, dy), LEN["upper_arm"] + LEN["forearm"] - 0.5)
    u, f = LEN["upper_arm"], LEN["forearm"]
    inner = math.degrees(math.acos((u * u + d * d - f * f) / (2 * u * d)))
    # angle of the target from straight down, measured away from the body
    ang = math.degrees(math.atan2(out * dx, -dy))
    a[f"abd_{k}"] = ang + inner
    a[f"elb_{k}"] = -(180 - math.degrees(math.acos((u * u + f * f - d * d) / (2 * u * f))))
    return a


# ---------------------------------------------------------------- drawing
class Pen:
    def __init__(self, img):
        self.img = img
        self.d = ImageDraw.Draw(img)

    def line(self, pts, fill, w):
        pts = [(x * SS, y * SS) for x, y in pts]
        self.d.line(pts, fill=fill, width=max(1, round(w * SS)), joint="curve")
        r = w * SS / 2
        for x, y in (pts[0], pts[-1]):
            self.d.ellipse([x - r, y - r, x + r, y + r], fill=fill)

    def circle(self, c, r, fill=None, outline=None, w=0):
        x, y = c[0] * SS, c[1] * SS
        self.d.ellipse([x - r * SS, y - r * SS, x + r * SS, y + r * SS], fill=fill, outline=outline,
                       width=round(w * SS))

    def poly(self, pts, fill, outline=None, w=0):
        p = [(x * SS, y * SS) for x, y in pts]
        if fill:
            self.d.polygon(p, fill=fill)
        if outline:
            self.d.line(p + [p[0]], fill=outline, width=round(w * SS), joint="curve")

    def rrect(self, box, r, outline, w, fill=None):
        self.d.rounded_rectangle([v * SS for v in box], radius=r * SS, outline=outline, width=round(w * SS), fill=fill)

    def arc(self, box, a0, a1, fill, w):
        self.d.arc([v * SS for v in box], a0, a1, fill=fill, width=round(w * SS))


def lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def axis(p, q):
    ax = (q[0] - p[0], q[1] - p[1]); n = math.hypot(*ax) or 1.0; ux = (ax[0] / n, ax[1] / n)
    return ux, (-ux[1], ux[0])


def plaid(pen, pts, s, origin, ux):
    """Fill a polygon with a large, simple red-and-navy check (few, wide bands so it cannot shimmer).
    The bands are laid out from `origin` along the garment axis `ux`, so the check moves and turns with the garment."""
    xs = [x * SS for x, _ in pts]; ys = [y * SS for _, y in pts]
    box = (int(min(xs)) - 2, int(min(ys)) - 2, int(max(xs)) + 3, int(max(ys)) + 3)
    w, h = box[2] - box[0], box[3] - box[1]
    ox, oy = round(origin[0] * SS), round(origin[1] * SS)
    reach = int(math.hypot(max(abs(box[0] - ox), abs(box[2] - ox)), max(abs(box[1] - oy), abs(box[3] - oy)))) + 4
    n = 2 * reach
    tile = Image.new("RGB", (n, n), FLANNEL)
    d = ImageDraw.Draw(tile, "RGBA")
    step, band = 11 * s * SS, 3.6 * s * SS
    k = reach - math.ceil(reach / step) * step   # a band edge sits on the origin (tile centre)
    while k < n:
        d.rectangle([k, 0, k + band, n], fill=PLAID + (150,))
        d.rectangle([0, k, n, k + band], fill=PLAID + (150,))
        k += step
    # tile "down" is the garment axis: rotate it from (0, 1) onto ux
    ang = math.degrees(math.atan2(ux[1], ux[0])) - 90
    tile = tile.rotate(-ang, resample=Image.BICUBIC, center=(reach, reach), fillcolor=FLANNEL)
    tile = tile.crop((box[0] - (ox - reach), box[1] - (oy - reach), box[2] - (ox - reach), box[3] - (oy - reach)))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).polygon([(x - box[0], y - box[1]) for x, y in zip(xs, ys)], fill=255)
    pen.img.paste(tile, box[:2], mask)


def chaikin(pts, n=2):
    """Round a closed outline (corner cutting), so garments read as soft cartoon shapes."""
    for _ in range(n):
        out = []
        for i in range(len(pts)):
            p, q = pts[i], pts[(i + 1) % len(pts)]
            out += [lerp(p, q, 0.25), lerp(p, q, 0.75)]
        pts = out
    return pts


LINE = 1.5   # outline weight, thin and even like the beanie lead
LIMB = 2.4   # stick forearm weight


def draw_leg(pen, j, k, s, view):
    """Slim jeans leg (a narrow tube, still reads as a stick) and a flat black shoe."""
    pts = [j[f"hip_{k}"], j[f"knee_{k}"], j[f"ankle_{k}"]]
    an, toe = j[f"ankle_{k}"], j[f"toe_{k}"]
    heel = lerp(toe, an, 1.25)
    pen.line([heel, toe], INK, 3.6 * s)
    pen.line(pts, INK, (4.6 + LINE) * s)
    pen.line(pts, JEANS, 4.6 * s)


def sleeve_shape(sh, el, s):
    ux, px = axis(sh, el)
    end = lerp(sh, el, 0.82)
    top = add(sh, ux, -2.5 * s)
    pts = [add(top, px, 4.5 * s), add(lerp(top, end, 0.4), px, 5.6 * s), add(end, px, 5.0 * s),
           add(end, px, -5.0 * s), add(lerp(top, end, 0.4), px, -5.6 * s), add(top, px, -4.5 * s)]
    return chaikin(pts, 1), end, px


def glove(pen, wr, el, s):
    """Cartoon glove like the beanie lead's: an oval palm along the forearm with a thumb on one side."""
    ux, px = axis(el, wr)
    c = add(wr, ux, 1.6 * s)
    pts = [add(add(c, ux, 4.4 * s * math.cos(t)), px, 3.5 * s * math.sin(t)) for t in
           [i * math.pi / 12 for i in range(24)]]
    pen.poly(pts, INK)
    th = add(add(wr, ux, 0.8 * s), px, 3.4 * s)
    pen.circle(th, 1.7 * s, fill=INK)


def draw_arm(pen, j, k, s, prop=None):
    sh, el, wr = j[f"shoulder_{k}"], j[f"elbow_{k}"], j[f"wrist_{k}"]
    pen.line([lerp(sh, el, 0.6), el, wr], INK, LIMB * s)
    if prop == "pen":
        tip = add(wr, (math.cos(math.radians(-35)), math.sin(math.radians(-35))), 18 * s)
        pen.line([add(wr, (tip[0] - wr[0], tip[1] - wr[1]), -0.25), tip], INK, 4.4 * s)
        pen.line([add(wr, (tip[0] - wr[0], tip[1] - wr[1]), -0.2), tip], PEN, 2.4 * s)
    glove(pen, wr, el, s)
    # flannel sleeve rolled up to just above the elbow, so the forearm stays a stick
    poly, end, px = sleeve_shape(sh, el, s)
    plaid(pen, poly, s, sh, axis(sh, el)[0])
    pen.poly(poly, None, INK, LINE * s)
    pen.line([add(end, px, 4.6 * s), add(end, px, -4.6 * s)], CUFF, 2.6 * s)


def shirt_shape(neck, pelvis, s, half_top=14.5, half_hem=16.0):
    """Boxy tee-shaped shirt like the beanie lead's: rounded shoulders, a slight flare, hem just below the hips."""
    ux, px = axis(neck, pelvis)
    top = add(neck, ux, 0.5 * s); sh = add(neck, ux, 4 * s); hem = add(pelvis, ux, 4 * s)
    # rounded shoulders, square hem
    pts = [add(top, px, half_top * 0.4 * s), add(add(top, ux, 0.8 * s), px, half_top * 0.85 * s), add(sh, px, half_top * s),
           add(lerp(sh, hem, 0.45), px, (half_top + 0.6) * s), add(hem, px, half_hem * s)]
    right = [add(top, px, -half_top * 0.4 * s), add(add(top, ux, 0.8 * s), px, -half_top * 0.85 * s), add(sh, px, -half_top * s),
             add(lerp(sh, hem, 0.45), px, -(half_top + 0.6) * s), add(hem, px, -half_hem * s)]
    return chaikin(pts + right[::-1], 1)


def draw_shirt(pen, j, s, view):
    side = view in ("right", "left")
    body = shirt_shape(j["neck"], j["pelvis"], s, *((10.5, 12.0) if side else (14.5, 16.0)))
    plaid(pen, body, s, j["neck"], axis(j["neck"], j["pelvis"])[0])
    ux, px = axis(j["neck"], j["pelvis"])
    top = add(j["neck"], ux, 0.5 * s); hem = add(j["pelvis"], ux, 4 * s)
    if view == "front":
        # open flannel: the white tee shows down the middle, collar points either side
        tee = chaikin([add(top, px, 4.6 * s), add(lerp(top, hem, 0.5), px, 3.6 * s), add(hem, px, 4.4 * s),
                       add(hem, px, -4.4 * s), add(lerp(top, hem, 0.5), px, -3.6 * s), add(top, px, -4.6 * s)], 1)
        pen.poly(tee, TEE_WHITE, INK, 1.1 * s)
        c = add(j["neck"], (0, 1.0 * s))
        pen.arc([c[0] - 4.6 * s, c[1] - 3.2 * s, c[0] + 4.6 * s, c[1] + 3.2 * s], 15, 165, INK, 1.1 * s)
        for side in (1, -1):
            pen.poly([add(top, px, side * 4.6 * s), add(top, px, side * 8.5 * s), add(add(top, ux, 6.5 * s), px, side * 5.2 * s)],
                     CUFF, INK, 1.1 * s)
    elif view in ("right", "left"):
        sgn = 1 if view == "right" else -1
        f = 1 if (px[0] * sgn) > 0 else -1
        tee = chaikin([add(top, px, f * 4.0 * s), add(add(top, ux, 6 * s), px, f * 8.6 * s), add(hem, px, f * 11.8 * s),
                       add(hem, px, f * 8.6 * s), add(lerp(top, hem, 0.5), px, f * 6.8 * s)], 1)
        pen.poly(tee, TEE_WHITE, INK, 1.1 * s)
        pen.poly([add(top, px, f * 2.5 * s), add(top, px, f * 6.4 * s), add(add(top, ux, 6 * s), px, f * 4.6 * s)],
                 CUFF, INK, 1.1 * s)
    else:
        pen.poly(chaikin([add(top, px, 6.5 * s), add(top, px, -6.5 * s), add(add(top, ux, 3.2 * s), px, -5.5 * s),
                          add(add(top, ux, 3.2 * s), px, 5.5 * s)], 1), CUFF, INK, 1.1 * s)
    pen.poly(body, None, INK, LINE * s)


def spiky_hair(cx, cy, r, s, a0, a1, cut):
    """Buzz cut: a thin dark cap following the skull from angle a0 to a1 (degrees, image coords, 0 = +x),
    with a short fuzzy edge, closed along the hairline points `cut`."""
    pts = []
    n = round(abs(a1 - a0) / 2.6)
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        rr = r + (1.9 if i % 2 else 0.5) * s
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts + cut


def draw_head(pen, j, s, view, expr="smile", stubble=False):
    cx, cy = j["head"]; r = HEAD_R * s
    pen.line([j["neck"], lerp(j["neck"], j["head"], 0.5)], INK, LIMB * s)
    pen.circle((cx, cy), r, fill=SKIN, outline=INK, w=1.7 * s)
    if view == "back":
        cut = [(cx + r * 0.9, cy + r * 0.3), (cx + r * 0.45, cy + r * 0.42), (cx, cy + r * 0.46),
               (cx - r * 0.45, cy + r * 0.42), (cx - r * 0.9, cy + r * 0.3)]
        pen.poly(spiky_hair(cx, cy, r, s, 160, 380, cut), HAIR)
        pen.line([(cx - r * 0.99, cy - 1 * s), (cx - r * 0.84, cy - 1 * s)], FRAME, 2 * s)
        pen.line([(cx + r * 0.84, cy - 1 * s), (cx + r * 0.99, cy - 1 * s)], FRAME, 2 * s)
        return
    if view == "front":
        hl = cy - r * 0.52
        cut = [(cx + r * 0.84, hl + 2 * s), (cx + r * 0.45, hl - 1.2 * s), (cx, hl - 0.4 * s),
               (cx - r * 0.45, hl - 1.2 * s), (cx - r * 0.84, hl + 2 * s)]
        pen.poly(spiky_hair(cx, cy, r, s, 194, 346, cut), HAIR)
        if stubble:
            for i in range(15):
                a = math.radians(40 + 100 * i / 14)
                for rr, off in ((0.7, 0.0), (0.82, 0.5)):
                    a2 = a + math.radians(3.5 * off)
                    p = (cx + r * rr * math.cos(a2), cy + r * rr * math.sin(a2) + 2 * s)
                    if p[1] > cy + r * 0.55:
                        pen.circle(p, 0.5 * s, fill=STUBBLE)
        draw_face_front(pen, cx, cy, r, s, expr)
    else:
        sgn = 1 if view == "right" else -1
        # three-quarter head like the beanie lead: hairline across the forehead, crown and nape behind
        cut = [(cx + sgn * r * 0.9, cy - r * 0.42), (cx + sgn * r * 0.35, cy - r * 0.58), (cx - sgn * r * 0.3, cy - r * 0.52),
               (cx - sgn * r * 0.6, cy - r * 0.15), (cx - sgn * r * 0.74, cy + r * 0.36)]
        if sgn == 1:
            pen.poly(spiky_hair(cx, cy, r, s, 150, 335, cut), HAIR)
        else:
            pen.poly(spiky_hair(cx, cy, r, s, 205, 390, cut[::-1]), HAIR)
        draw_face_side(pen, cx, cy, r, s, sgn, expr)


def eye(pen, x, y, s, expr, k=1.0):
    if expr == "happy":
        pen.arc([x - 2.4 * s, y - 1.5 * s, x + 2.4 * s, y + 2.5 * s], 200, 340, INK, 1.4 * s)
        return
    k *= 1.2 if expr == "surprised" else 1.0
    pen.d.ellipse([(x - 1.6 * k * s) * SS, (y - 2.5 * k * s) * SS, (x + 1.6 * k * s) * SS, (y + 2.5 * k * s) * SS], fill=INK)
    pen.circle((x + 0.5 * s, y - 1.2 * s), 0.55 * s, fill=(255, 255, 255))


def brows(pen, cx, cy, r, s, expr, xs):
    for i, x in enumerate(xs):
        side = -1 if i == 0 else 1
        y = cy - r * 0.36
        if expr == "surprised":
            pen.arc([x - 3.6 * s, y - 5.5 * s, x + 3.6 * s, y], 200, 340, INK, 1.3 * s)
        elif expr == "determined":
            pen.line([(x - side * 3.6 * s, y - 3.6 * s), (x + side * 3.6 * s, y - 1.2 * s)], INK, 1.5 * s)
        elif expr == "sad":
            pen.line([(x - side * 3.6 * s, y - 1.2 * s), (x + side * 3.6 * s, y - 4 * s)], INK, 1.5 * s)
        elif expr == "thinking" and i == 1:
            pen.arc([x - 3.6 * s, y - 6.5 * s, x + 3.6 * s, y - 1 * s], 200, 340, INK, 1.3 * s)
        elif expr == "thinking":
            pen.line([(x - 3.6 * s, y - 2.4 * s), (x + 3.6 * s, y - 2.4 * s)], INK, 1.3 * s)
        else:
            pen.arc([x - 3 * s, y - 4.2 * s, x + 3 * s, y - 0.4 * s], 215, 325, INK, 1.2 * s)


def mouth(pen, mx, my, s, expr, sgn=0):
    if expr == "smile":
        # the beanie lead's smile: a soft curve with a small tick at the outer end
        pen.arc([mx - 5.5 * s, my - 5 * s, mx + 5.5 * s, my + 1.6 * s], 25, 155, INK, 1.4 * s)
        t = sgn or 1
        e = (mx + t * 5.0 * s, my - 1.6 * s)
        pen.line([e, add(e, (t * 1.2 * s, -1.6 * s))], INK, 1.2 * s)
    elif expr == "thinking":
        pen.line([(mx - 3 * s, my), (mx + 3.6 * s, my - 0.8 * s)], INK, 1.4 * s)
    elif expr == "happy":
        pen.poly(chaikin([(mx - 6.5 * s, my - 2 * s), (mx + 6.5 * s, my - 2 * s), (mx, my + 4.8 * s)], 1), (205, 75, 75), INK, 1.3 * s)
    elif expr == "surprised":
        pen.circle((mx, my + 1 * s), 2.6 * s, fill=None, outline=INK, w=1.4 * s)
    elif expr == "determined":
        pen.line([(mx - 3.6 * s, my), (mx + 3.6 * s, my)], INK, 1.5 * s)
    elif expr == "sad":
        pen.arc([mx - 4.6 * s, my - 0.5 * s, mx + 4.6 * s, my + 5.5 * s], 205, 335, INK, 1.4 * s)


def lens(pen, x, y, hw, s):
    pen.rrect([x - hw * s, y - 4.8 * s, x + hw * s, y + 4.8 * s], 2.0 * s, FRAME, 2.0 * s)


def draw_face_front(pen, cx, cy, r, s, expr):
    ey = cy - 0.5 * s
    xs = (cx - 8.4 * s, cx + 8.4 * s)
    for x in xs:
        eye(pen, x, ey + 0.4 * s, s, expr)
    for x in xs:
        lens(pen, x, ey, 6.4, s)
    pen.line([(xs[0] + 6.4 * s, ey - 1.8 * s), (xs[1] - 6.4 * s, ey - 1.8 * s)], FRAME, 1.8 * s)
    pen.line([(xs[0] - 6.4 * s, ey - 2.6 * s), (cx - r * 0.99, ey - 3.4 * s)], FRAME, 1.8 * s)
    pen.line([(xs[1] + 6.4 * s, ey - 2.6 * s), (cx + r * 0.99, ey - 3.4 * s)], FRAME, 1.8 * s)
    brows(pen, cx, cy, r, s, expr, xs)
    mouth(pen, cx, cy + 10 * s, s, expr)


def draw_face_side(pen, cx, cy, r, s, sgn, expr):
    ey = cy - 0.5 * s
    near, far = cx + sgn * r * 0.12, cx + sgn * r * 0.64
    eye(pen, near, ey + 0.4 * s, s, expr)
    eye(pen, far, ey + 0.4 * s, s, expr, 0.9)
    lens(pen, near, ey, 5.6, s)
    lens(pen, far, ey, 4.0, s)
    pen.line([(near + sgn * 5.6 * s, ey - 1.8 * s), (far - sgn * 4.0 * s, ey - 1.8 * s)], FRAME, 1.8 * s)
    pen.line([(near - sgn * 5.6 * s, ey - 2.6 * s), (cx - sgn * r * 0.6, ey - 3.4 * s)], FRAME, 1.8 * s)
    e2 = "smile" if expr == "thinking" else expr
    brows(pen, cx, cy, r, s, e2, (near, far))
    mouth(pen, cx + sgn * r * 0.36, cy + 10 * s, s, e2, sgn)


def draw_figure(img, j, view, s=1.0, expr="smile", stubble=False, holds=None, over_face=None):
    """view: front | back | right | left (the way the character faces). holds: {'r': 'pen'}."""
    pen = Pen(img)
    holds = holds or {}
    if view in ("right", "left"):
        near = "r" if view == "right" else "l"; far = "l" if near == "r" else "r"
        draw_arm(pen, j, far, s, holds.get(far))
        draw_leg(pen, j, far, s, view); draw_leg(pen, j, near, s, view)
        draw_shirt(pen, j, s, view)
        draw_head(pen, j, s, view, expr, stubble)
        draw_arm(pen, j, near, s, holds.get(near))
    else:
        draw_leg(pen, j, "l", s, view); draw_leg(pen, j, "r", s, view)
        draw_shirt(pen, j, s, view)
        arms = ("l", "r")
        late = [k for k in arms if over_face == k]
        for k in arms:
            if k not in late:
                draw_arm(pen, j, k, s, holds.get(k))
        draw_head(pen, j, s, view, expr, stubble)
        for k in late:
            draw_arm(pen, j, k, s, holds.get(k))


def shadow(img, x, y, w, s=1.0):
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([(x - w * s) * SS, (y - 4 * s) * SS, (x + w * s) * SS, (y + 4 * s) * SS], fill=(0, 0, 0, 28))


def canvas(w, h, bg=(250, 250, 250)):
    return Image.new("RGB", (w * SS, h * SS), bg)


def finish(img):
    return img.resize((img.width // SS, img.height // SS), Image.LANCZOS)


def font(size, bold=False):
    for p in ("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf" if bold else "/usr/share/fonts/opentype/inter/Inter-Regular.otf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if Path(p).exists():
            return ImageFont.truetype(p, size * SS)
    return ImageFont.load_default()


def text(img, xy, s, size=18, bold=False, fill=(40, 40, 40), anchor="mm"):
    ImageDraw.Draw(img).text((xy[0] * SS, xy[1] * SS), s, font=font(size, bold), fill=fill, anchor=anchor)


# ---------------------------------------------------------------- tracks
FIG = {"head_radius": HEAD_R, "limb_width": 2.4, "body_width": 30, "hand_length": 6}


def track(name, frames, rest, scale=1.0, **meta):
    fig = {k: round(v * scale, 2) for k, v in FIG.items()}
    return {"name": name, "source": "rig", "profile": "rig", "fps": 12, **fig, "rest": rest, **meta, "frames": frames}


def sheet_poses():
    """(label, view, joints, frame extras, holds, over_face) for the pose row, all at x=0, ground=0, scale 1."""
    out = []
    a = stand_front(); a["abd_r"] = 125; a["elb_r"] = 60
    out.append(("Wave", "front", front_pose(a, 0, 0), {}, {}, None))
    a = stand_side(); a["shoulder_r"] = 88; a["elbow_r"] = 6; a["lean"] = 4
    out.append(("Point", "right", side_pose(a, 0, 0), {}, {}, None))
    a = ik_front(stand_front(), "r", (-3, LEN["torso"] + LEN["head"] - 15))
    out.append(("Think", "front", front_pose(a, 0, 0), {"face_cover": True, "contacts": {"r": "chin"}}, {}, "r"))
    a = stand_side(); a["shoulder_r"] = 70; a["elbow_r"] = 40
    j = side_pose(a, 0, 0)
    out.append(("Light-pen", "right", j, {"holds": {"pen": "r"}, "props": {"pen": j["wrist_r"]}}, {"r": "pen"}, None))
    a = {"abd_l": 150, "elb_l": 10, "abd_r": 150, "elb_r": 10, "leg_l": 14, "leg_r": 14}
    out.append(("Cheer jump", "front", front_pose(a, 0, 0, lift=16), {"airborne": True}, {}, None))
    a = {"lean": 12, "neck": 2, "hip_r": 50, "knee_r": 75, "hip_l": -30, "knee_l": 75, "ankle_l": 10,
         "shoulder_r": -40, "elbow_r": 85, "shoulder_l": 45, "elbow_l": 80}
    out.append(("Run", "right", side_pose(a, 0, 0), {"airborne": True}, {}, None))
    a = stand_side(); a["shoulder_r"] = -30; a["elbow_r"] = 105; a["shoulder_l"] = 55; a["elbow_l"] = 45
    j = side_pose(a, 0, 0)
    out.append(("Hand on hip", "right", j, {"holds": {"pen": "l"}, "props": {"pen": j["wrist_l"]}}, {"l": "pen"}, None))
    return out


def walk_shot(n=30, s=1.0, x0=110.0, ground=322.0):
    frames = []
    for i in range(n):
        frames.append({"facing": "right", "joints": side_pose(walk(i / 12), x0 + i * 4.6 * s, ground, s)})
    for i in range(6):  # ease into a stand
        t = (i + 1) / 6; w = walk(n / 12); st = stand_side()
        a = {k: w.get(k, 0) * (1 - t) + st.get(k, 0) * t for k in set(w) | set(st)}
        frames.append({"facing": "right", "joints": side_pose(a, x0 + (n + 1.2 * (i + 1) / 2) * 4.6 * s, ground, s)})
    return frames


def wave_shot(s=1.0, x=320.0, ground=344.0):
    frames = []
    def ease(t): return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, t)))
    rest = stand_front()
    up = {"abd_r": 125, "elb_r": 75}
    T, Hh = LEN["torso"], LEN["head"]
    path = [(16.0, -2.0), (36.0, T - 10), (22.0, T + Hh - 4), (0.0, T + Hh + 1.0)]  # rest wrist -> out -> up -> glasses
    path[0] = tuple(front_pose(rest, 0, 0)["wrist_l"])  # placeholder, replaced below
    rj = front_pose(rest, 0.0, 0.0); pv = rj["pelvis"]
    path[0] = (rj["wrist_l"][0] - pv[0], -(rj["wrist_l"][1] - pv[1]))

    def along(t):
        t = max(0.0, min(1.0, t)) * (len(path) - 1); i = min(int(t), len(path) - 2); u = t - i
        return lerp(path[i], path[i + 1], u)
    for i in range(48):
        a = dict(rest); f = {"facing": "front"}; expr = "smile"
        if 4 <= i < 12:
            t = ease((i - 4) / 8); a["abd_r"] = rest["abd_r"] + (up["abd_r"] - rest["abd_r"]) * t
            a["elb_r"] = rest["elb_r"] + (up["elb_r"] - rest["elb_r"]) * t
        elif 12 <= i < 26:
            a["abd_r"] = up["abd_r"]; a["elb_r"] = up["elb_r"] - 8 + 16 * math.sin(2 * math.pi * (i - 12) / 7); expr = "happy"
        elif 26 <= i < 32:
            t = ease((i - 26) / 6); a["abd_r"] = up["abd_r"] + (rest["abd_r"] - up["abd_r"]) * t
            a["elb_r"] = up["elb_r"] + (rest["elb_r"] - up["elb_r"]) * t
        t = None
        if 30 <= i < 38:
            t = ease((i - 30) / 7)
        elif 38 <= i < 41:
            t = 1.0
        elif 41 <= i:
            t = 1 - ease((i - 40) / 7)
        if t is not None and t > 0:
            w = along(t); ik_front(a, "l", w)
            if w[1] > T + Hh - 16:
                f["face_cover"] = True
        f["joints"] = front_pose(a, x, ground, s)
        f["_expr"] = "smile" if i >= 26 and i < 36 else ("determined" if 36 <= i < 44 else expr)
        frames.append(f)
    return frames


# ---------------------------------------------------------------- outputs
def studio_bg(w, h, horizon):
    img = canvas(w, h, (246, 247, 249))
    d = ImageDraw.Draw(img)
    for y in range(horizon * SS, h * SS, SS):
        t = (y / SS - horizon) / (h - horizon)
        c = round(246 - 10 * t)
        d.line([(0, y), (w * SS, y)], fill=(c, c + 1, c + 3))
    vx = w / 2
    for i in range(-12, 13):
        d.line([(vx * SS, (horizon - 60) * SS), ((vx + i * 70) * SS, h * SS)], fill=(224, 227, 232), width=SS)
    y = horizon; k = 8.0
    while y < h:
        d.line([(0, y * SS), (w * SS, y * SS)], fill=(224, 227, 232), width=SS)
        y += k; k *= 1.35
    d.rectangle([0, 0, w * SS, (horizon - 0) * SS], fill=(250, 251, 252))
    return img


def make_gif(walk_frames, wave_frames, s_walk, s_wave):
    W, H = 640, 360
    walk_bg, wave_bg = studio_bg(W, H, 200), studio_bg(W, H, 230)
    out = []
    for f in walk_frames:
        img = walk_bg.copy(); j = f["joints"]
        shadow(img, (j["toe_l"][0] + j["toe_r"][0]) / 2, max(j["toe_l"][1], j["toe_r"][1]) + 1, 26, s_walk)
        draw_figure(img, j, "right", s_walk)
        out.append(finish(img))
    for f in wave_frames:
        img = wave_bg.copy(); j = f["joints"]
        shadow(img, j["pelvis"][0], max(j["toe_l"][1], j["toe_r"][1]) + 1, 34, s_wave)
        draw_figure(img, j, "front", s_wave, expr=f["_expr"], over_face="l" if f.get("face_cover") or
                    j["wrist_l"][1] < j["neck"][1] else None)
        out.append(finish(img))
    # one shared palette for every frame, so the plaid and the jeans keep their colours
    probe = Image.new("RGB", (W, H * 4))
    for i, k in enumerate((0, len(walk_frames) // 2, len(walk_frames) + 6, len(out) - 10)):
        probe.paste(out[k], (0, H * i))
    ref = probe.quantize(colors=128, method=Image.Quantize.FASTOCTREE)
    pal = [o.quantize(palette=ref, dither=Image.Dither.NONE) for o in out]
    pal[0].save(HERE / "motion.gif", save_all=True, append_images=pal[1:], duration=83, loop=0, optimize=True, disposal=1)


def make_sheet(poses):
    W, H = 1600, 1180
    img = canvas(W, H, (252, 251, 248))
    text(img, (60, 52), "Style 2 lead Nam: buzz cut, glasses, plaid flannel", 34, True, anchor="lm")
    text(img, (60, 92), "Code-rendered from a posture-gated rig. Default lead for Style 2A/2B; the red-beanie Zeke stays as an alternative.",
         17, anchor="lm", fill=(90, 90, 90))
    # row 1: turnaround
    text(img, (60, 145), "Turnaround", 22, True, anchor="lm")
    base = side_pose(stand_side(), 0, 0, 1.6)
    views = [("Front", "front", front_pose(stand_front(), 0, 0, 1.6)),
             ("Side, facing right", "right", base),
             ("Back", "back", front_pose(stand_front(), 0, 0, 1.6)),
             ("Side, facing left", "left", mirror(base, 0))]
    for i, (lab, view, j) in enumerate(views):
        x, gy = 170 + i * 260, 470
        jj = {k: [p[0] + x, p[1] + gy] for k, p in j.items()}
        if view == "back":  # seen from behind: own left on screen left
            jj = {k[:-2] + ("_r" if k.endswith("_l") else "_l") if k.endswith(("_l", "_r")) else k: v for k, v in jj.items()}
        shadow(img, x, gy + 2, 34, 1.6)
        draw_figure(img, jj, view, 1.6)
        text(img, (x, gy + 32), lab, 17)
    # palette
    px = 1180
    text(img, (px, 145), "Locks", 22, True, anchor="lm")
    rows = [(HAIR, "Very short dark buzz cut, spiky edge"), (FRAME, "Dark rectangular glasses, thick frame"),
            (FLANNEL, "Open red-and-navy plaid flannel, sleeves rolled"), (TEE_WHITE, "Plain white crew-neck tee"),
            (JEANS, "Dark blue jeans, black shoes"), (INK, "Black stick forearms, round hands")]
    for i, (c, lab) in enumerate(rows):
        y = 195 + i * 46
        ImageDraw.Draw(img).rounded_rectangle([px * SS, (y - 15) * SS, (px + 30) * SS, (y + 15) * SS], radius=6 * SS,
                                              fill=c, outline=(120, 120, 120), width=SS)
        text(img, (px + 44, y), lab, 16, anchor="lm")
    text(img, (px, 480), "Body and head as the beanie lead. Not in the anchor:", 15, anchor="lm", fill=(110, 110, 110))
    text(img, (px, 502), "logos, text, pupils, lens glare, a hat.", 15, anchor="lm", fill=(110, 110, 110))
    # row 2: expressions
    text(img, (60, 560), "Expressions (glasses stay on)", 22, True, anchor="lm")
    exprs = ["smile", "happy", "surprised", "thinking", "determined", "sad"]
    for i, e in enumerate(exprs):
        x, y = 150 + i * 190, 655
        j = {"head": [x, y], "neck": [x, y + 60]}
        pen = Pen(img)
        draw_head(pen, j, 2.4, "front", e)
        text(img, (x, y + 78), e.capitalize(), 16)
    x, y = 1330, 655
    draw_head(Pen(img), {"head": [x, y], "neck": [x, y + 60]}, 2.4, "front", "smile", stubble=True)
    text(img, (x, y + 78), "Optional: light stubble", 16, fill=(110, 110, 110))
    # row 3: poses
    text(img, (60, 800), "Poses (each one gated)", 22, True, anchor="lm")
    for i, (lab, view, j, extra, holds, over) in enumerate(poses):
        x, gy = 120 + i * 205, 1100
        jj = {k: [p[0] * 1.3 + x, p[1] * 1.3 + gy] for k, p in j.items()}
        shadow(img, x, gy + 2, 30, 1.3)
        draw_figure(img, jj, view, 1.3, expr="thinking" if lab == "Think" else ("happy" if "jump" in lab else "smile"),
                    holds=holds, over_face=over)
        text(img, (x, gy + 34), lab, 17)
    finish(img).save(HERE / "sheet.png", optimize=True)


def main():
    tracks = HERE / "tracks"; tracks.mkdir(exist_ok=True)
    poses = sheet_poses()
    for lab, view, j, extra, holds, over in poses:
        name = "pose_" + lab.lower().replace(" ", "_").replace("-", "_")
        props = dict(extra.get("props", {}))
        f = {"facing": "front" if view == "front" else view, "joints": j, **extra}
        if "contacts" in extra:  # chin = bottom of the head circle
            props["chin"] = [j["head"][0], j["head"][1] + HEAD_R * 0.8]
        if props:
            f["props"] = props
        if lab == "Run":
            f.pop("airborne")
        rest = front_pose(stand_front(), 0, 0) if view == "front" else side_pose(stand_side(), 0, 0)
        (tracks / f"{name}.json").write_text(json.dumps(track(name, [f], rest), indent=1))
    s_walk, s_wave = 1.0, 1.25
    wf = walk_shot(s=s_walk)
    vf = wave_shot(s=s_wave)
    (tracks / "shot1_walk.json").write_text(json.dumps(
        track("shot1_walk", wf, side_pose(stand_side(), 110, 322, s_walk), s_walk), indent=1))
    (tracks / "shot2_wave_glasses.json").write_text(json.dumps(track(
        "shot2_wave_glasses", [{k: v for k, v in f.items() if not k.startswith("_")} for f in vf],
        front_pose(stand_front(), 320, 344, s_wave), s_wave), indent=1))
    make_sheet(poses)
    make_gif(wf, vf, s_walk, s_wave)


if __name__ == "__main__":
    main()
