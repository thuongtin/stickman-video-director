#!/usr/bin/env python3
"""Draw the Style 2 default lead (buzz cut, dark rectangular glasses, dark red crew-neck tee) from a code rig.

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
LEN = {"torso": 58, "head": 30, "upper_arm": 30, "forearm": 28, "thigh": 38, "shin": 36, "foot": 11}
HEAD_R = 21
INK = (24, 24, 24)
HAIR = (34, 30, 30)
FRAME = (40, 38, 38)
TEE = (139, 45, 42)        # dark red / maroon
TEE_DARK = (104, 30, 29)
SHORTS = (58, 62, 72)      # charcoal
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
    return {"lean": 2, "neck": 3, "shoulder_l": -6, "elbow_l": 18, "shoulder_r": 6, "elbow_r": 18,
            "hip_l": -3, "knee_l": 4, "hip_r": 3, "knee_r": 4}


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
        sh = (out * 13.0, LEN["torso"] - 5); hp = (out * 8.0, 0.0)
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
    return {"abd_l": 9, "elb_l": -6, "abd_r": 9, "elb_r": -6}


def ik_front(a, k, target_math):
    """Set abd_k/elb_k so the wrist reaches target (math coords relative to pelvis), elbow out to the side."""
    out = 1 if k == "l" else -1
    sh = (out * 13.0, LEN["torso"] - 5)
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
        self.d.polygon(p, fill=fill)
        if outline:
            self.d.line(p + [p[0]], fill=outline, width=round(w * SS), joint="curve")

    def rrect(self, box, r, outline, w, fill=None):
        self.d.rounded_rectangle([v * SS for v in box], radius=r * SS, outline=outline, width=round(w * SS), fill=fill)

    def arc(self, box, a0, a1, fill, w):
        self.d.arc([v * SS for v in box], a0, a1, fill=fill, width=round(w * SS))


def lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def tee_shape(neck, pelvis, s, half_top=11.0, half_hem=13.0):
    ax = (pelvis[0] - neck[0], pelvis[1] - neck[1]); n = math.hypot(*ax); ux = (ax[0] / n, ax[1] / n)
    px = (-ux[1], ux[0])
    top = add(neck, ux, 3 * s); sh = add(neck, ux, 9 * s); hem = add(pelvis, ux, 3 * s)
    return [add(top, px, half_top * 0.75 * s), add(sh, px, half_top * s), add(hem, px, half_hem * s),
            add(hem, px, -half_hem * s), add(sh, px, -half_top * s), add(top, px, -half_top * 0.75 * s)]


def draw_leg(pen, j, k, s, view):
    pen.line([j[f"hip_{k}"], j[f"knee_{k}"], j[f"ankle_{k}"]], INK, 4.2 * s)
    if view in ("front", "back"):
        pen.line([j[f"ankle_{k}"], j[f"toe_{k}"]], INK, 6 * s)
    else:
        pen.line([j[f"ankle_{k}"], j[f"toe_{k}"]], INK, 6.5 * s)


def draw_shorts(pen, j, s):
    for k in ("l", "r"):
        pen.line([j["pelvis"], lerp(j[f"hip_{k}"], j[f"knee_{k}"], 0.42)], INK, 14 * s)
    for k in ("l", "r"):
        pen.line([j["pelvis"], lerp(j[f"hip_{k}"], j[f"knee_{k}"], 0.40)], SHORTS, 10.5 * s)


def draw_arm(pen, j, k, s, prop=None):
    sh, el, wr = j[f"shoulder_{k}"], j[f"elbow_{k}"], j[f"wrist_{k}"]
    pen.line([sh, el, wr], INK, 4.2 * s)
    if prop == "pen":
        tip = add(wr, (math.cos(math.radians(-35)), math.sin(math.radians(-35))), 18 * s)
        pen.line([add(wr, (tip[0] - wr[0], tip[1] - wr[1]), -0.25), tip], INK, 5 * s)
        pen.line([add(wr, (tip[0] - wr[0], tip[1] - wr[1]), -0.2), tip], PEN, 2.6 * s)
    pen.circle(wr, 5.2 * s, fill=INK)
    # short sleeve over the top of the upper arm
    sl = lerp(sh, el, 0.48)
    pen.line([sh, sl], INK, 11.5 * s)
    pen.line([sh, sl], TEE, 8 * s)


def draw_tee(pen, j, s, view):
    pen.poly(tee_shape(j["neck"], j["pelvis"], s), TEE, INK, 2.4 * s)
    if view == "front":
        c = add(j["neck"], (0, 2.5 * s))
        pen.arc([c[0] - 7 * s, c[1] - 5 * s, c[0] + 7 * s, c[1] + 5 * s], 10, 170, TEE_DARK, 2.6 * s)
    elif view in ("right", "left"):
        sgn = 1 if view == "right" else -1
        c = add(j["neck"], (sgn * 4 * s, 3.5 * s))
        pen.line([add(c, (-sgn * 6 * s, -1.5 * s)), c], TEE_DARK, 2.4 * s)


def spiky_hair(cx, cy, r, s, a0, a1, cut):
    """Buzz cut: a thin dark cap following the skull from angle a0 to a1 (degrees, image coords, 0 = +x),
    with a short spiky edge, closed along the hairline points `cut`."""
    pts = []
    n = round(abs(a1 - a0) / 3.2)
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        rr = r + (2.6 if i % 2 else 0.9) * s
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts + cut


def draw_head(pen, j, s, view, expr="smile", stubble=False):
    cx, cy = j["head"]; r = HEAD_R * s
    pen.line([j["neck"], lerp(j["neck"], j["head"], 0.4)], INK, 4.2 * s)
    pen.circle((cx, cy), r, fill=SKIN, outline=INK, w=2.6 * s)
    if view == "back":
        cut = [(cx + r * 0.8, cy + r * 0.58), (cx, cy + r * 0.74), (cx - r * 0.8, cy + r * 0.58)]
        pen.poly(spiky_hair(cx, cy, r, s, 144, 396, cut), HAIR)
        pen.line([(cx - r * 0.98, cy - 1 * s), (cx - r * 0.8, cy - 1 * s)], FRAME, 2.4 * s)
        pen.line([(cx + r * 0.8, cy - 1 * s), (cx + r * 0.98, cy - 1 * s)], FRAME, 2.4 * s)
        return
    if view == "front":
        hl = cy - r * 0.48
        cut = [(cx + r * 0.86, hl + 2 * s), (cx + r * 0.45, hl - 1.5 * s), (cx, hl - 0.5 * s),
               (cx - r * 0.45, hl - 1.5 * s), (cx - r * 0.86, hl + 2 * s)]
        pen.poly(spiky_hair(cx, cy, r, s, 192, 348, cut), HAIR)
        if stubble:
            for i in range(15):
                a = math.radians(40 + 100 * i / 14)
                for rr, off in ((0.7, 0.0), (0.82, 0.5)):
                    a2 = a + math.radians(3.5 * off)
                    p = (cx + r * rr * math.cos(a2), cy + r * rr * math.sin(a2) + 2 * s)
                    if p[1] > cy + r * 0.55:
                        pen.circle(p, 0.55 * s, fill=STUBBLE)
        draw_face_front(pen, cx, cy, r, s, expr)
    else:
        sgn = 1 if view == "right" else -1
        # close-cropped: a band hugging the skull from the forehead over the crown to the nape
        a0, a1 = (150, 318) if sgn == 1 else (222, 390)
        inner = []
        for i in range(25):
            a = math.radians(a1 - (a1 - a0) * i / 24)
            depth = 0.70 if 0.25 < i / 24 < 0.8 else 0.80
            inner.append((cx + r * depth * math.cos(a), cy + r * depth * math.sin(a)))
        pen.poly(spiky_hair(cx, cy, r, s, a0, a1, inner), HAIR)
        draw_face_side(pen, cx, cy, r, s, sgn, expr)


def brows(pen, cx, cy, r, s, expr, xs):
    for i, x in enumerate(xs):
        side = -1 if i == 0 else 1
        y = cy - r * 0.3
        if expr == "surprised":
            pen.arc([x - 4 * s, y - 6 * s, x + 4 * s, y], 200, 340, INK, 1.8 * s)
        elif expr == "determined":
            pen.line([(x - side * 4 * s, y - 4 * s), (x + side * 4 * s, y - 1.5 * s)], INK, 2 * s)
        elif expr == "sad":
            pen.line([(x - side * 4 * s, y - 1.5 * s), (x + side * 4 * s, y - 4.5 * s)], INK, 2 * s)
        elif expr == "thinking" and i == 1:
            pen.arc([x - 4 * s, y - 7 * s, x + 4 * s, y - 1 * s], 200, 340, INK, 1.8 * s)
        elif expr == "thinking":
            pen.line([(x - 4 * s, y - 2.5 * s), (x + 4 * s, y - 2.5 * s)], INK, 1.8 * s)


def draw_face_front(pen, cx, cy, r, s, expr):
    ey = cy - 1 * s
    xs = (cx - 9 * s, cx + 9 * s)
    for x in xs:
        if expr == "happy":
            pen.arc([x - 2.5 * s, ey - 1 * s, x + 2.5 * s, ey + 3 * s], 200, 340, INK, 1.6 * s)
        else:
            pen.circle((x, ey + 0.5 * s), (2.1 if expr == "surprised" else 1.7) * s, fill=INK)
    for x in xs:
        pen.rrect([x - 7.5 * s, ey - 5.5 * s, x + 7.5 * s, ey + 5.5 * s], 2.5 * s, FRAME, 2.4 * s)
    pen.line([(xs[0] + 7.5 * s, ey - 2 * s), (xs[1] - 7.5 * s, ey - 2 * s)], FRAME, 2.2 * s)
    pen.line([(xs[0] - 7.5 * s, ey - 3 * s), (cx - r * 0.99, ey - 4 * s)], FRAME, 2.2 * s)
    pen.line([(xs[1] + 7.5 * s, ey - 3 * s), (cx + r * 0.99, ey - 4 * s)], FRAME, 2.2 * s)
    brows(pen, cx, cy, r, s, expr, xs)
    my = cy + 10 * s
    if expr in ("smile", "thinking") :
        if expr == "smile":
            pen.arc([cx - 6 * s, my - 5 * s, cx + 6 * s, my + 2 * s], 20, 160, INK, 1.9 * s)
        else:
            pen.line([(cx - 3 * s, my), (cx + 4 * s, my - 1 * s)], INK, 1.9 * s)
    elif expr == "happy":
        pen.poly([(cx - 7 * s, my - 2 * s), (cx + 7 * s, my - 2 * s), (cx, my + 5 * s)], (200, 70, 70), INK, 1.8 * s)
    elif expr == "surprised":
        pen.circle((cx, my + 1 * s), 3 * s, fill=None, outline=INK, w=1.9 * s)
    elif expr == "determined":
        pen.line([(cx - 4 * s, my), (cx + 4 * s, my)], INK, 2 * s)
    elif expr == "sad":
        pen.arc([cx - 5 * s, my - 0.5 * s, cx + 5 * s, my + 6 * s], 200, 340, INK, 1.9 * s)


def draw_face_side(pen, cx, cy, r, s, sgn, expr):
    ey = cy - 1 * s
    ex = cx + sgn * r * 0.6
    pen.circle((ex, ey + 0.5 * s), 1.7 * s, fill=INK)
    pen.rrect([ex - 4.5 * s, ey - 5.5 * s, ex + 4.5 * s, ey + 5.5 * s], 2 * s, FRAME, 2.4 * s)
    pen.line([(ex - sgn * 4.5 * s, ey - 3 * s), (cx - sgn * 3 * s, ey - 2 * s)], FRAME, 2.2 * s)
    mx = cx + sgn * r * 0.55; my = cy + 10 * s
    if expr == "surprised":
        pen.circle((mx, my), 2.5 * s, outline=INK, w=1.8 * s)
    else:
        a0, a1 = (20, 120) if sgn == 1 else (60, 160)
        pen.arc([mx - 5 * s, my - 5 * s, mx + 5 * s, my + 2 * s], a0, a1, INK, 1.9 * s)
    brows(pen, cx, cy, r, s, expr if expr != "thinking" else "smile", (ex,) if sgn == 1 else (ex,))


def draw_figure(img, j, view, s=1.0, expr="smile", stubble=False, holds=None, over_face=None):
    """view: front | back | right | left (the way the character faces). holds: {'r': 'pen'}."""
    pen = Pen(img)
    holds = holds or {}
    gx = (j["toe_l"][1] + j["toe_r"][1]) / 2
    if view in ("right", "left"):
        near = "r" if view == "right" else "l"; far = "l" if near == "r" else "r"
        draw_arm(pen, j, far, s, holds.get(far))
        draw_leg(pen, j, far, s, view); draw_leg(pen, j, near, s, view)
        draw_shorts(pen, j, s)
        draw_tee(pen, j, s, view)
        draw_head(pen, j, s, view, expr, stubble)
        draw_arm(pen, j, near, s, holds.get(near))
    else:
        draw_leg(pen, j, "l", s, view); draw_leg(pen, j, "r", s, view)
        draw_shorts(pen, j, s)
        draw_tee(pen, j, s, view)
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
FIG = {"head_radius": HEAD_R, "limb_width": 4.2, "body_width": 24, "hand_length": 5}


def track(name, frames, rest, scale=1.0, **meta):
    fig = {k: round(v * scale, 2) for k, v in FIG.items()}
    return {"name": name, "source": "rig", "profile": "rig", "fps": 12, **fig, "rest": rest, **meta, "frames": frames}


def sheet_poses():
    """(label, view, joints, frame extras, holds, over_face) for the pose row, all at x=0, ground=0, scale 1."""
    out = []
    a = stand_front(); a["abd_r"] = 145; a["elb_r"] = 55
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
    a = {"lean": 12, "neck": 2, "hip_r": 50, "knee_r": 75, "hip_l": -22, "knee_l": 45, "ankle_l": 10,
         "shoulder_r": -40, "elbow_r": 85, "shoulder_l": 45, "elbow_l": 80}
    out.append(("Run", "right", side_pose(a, 0, 0), {"airborne": True}, {}, None))
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
    pal = [o.convert("P", palette=Image.ADAPTIVE, colors=48) for o in out]
    pal[0].save(HERE / "motion.gif", save_all=True, append_images=pal[1:], duration=83, loop=0, optimize=True, disposal=1)


def make_sheet(poses):
    W, H = 1600, 1180
    img = canvas(W, H, (252, 251, 248))
    text(img, (60, 52), "Style 2 lead Nam: buzz cut, glasses, dark red tee", 34, True, anchor="lm")
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
            (TEE, "Plain dark red crew-neck tee"), (SHORTS, "Dark shorts"), (INK, "Black stick limbs, round hands"),
            ((255, 255, 255), "White round head, dot eyes")]
    for i, (c, lab) in enumerate(rows):
        y = 195 + i * 46
        ImageDraw.Draw(img).rounded_rectangle([px * SS, (y - 15) * SS, (px + 30) * SS, (y + 15) * SS], radius=6 * SS,
                                              fill=c, outline=(120, 120, 120), width=SS)
        text(img, (px + 44, y), lab, 16, anchor="lm")
    text(img, (px, 480), "Not in the anchor: logos, text on the tee,", 15, anchor="lm", fill=(110, 110, 110))
    text(img, (px, 502), "pupils, reflections on the lenses, a hat.", 15, anchor="lm", fill=(110, 110, 110))
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
        x, gy = 140 + i * 230, 1100
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
