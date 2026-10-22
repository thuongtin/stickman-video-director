"""Style 4, cozy storytelling: a quiet coffee at a sidewalk cafe table, in a soft painted street."""
import math
import random

from PIL import ImageFilter

from rig2d import (SS, Backdrop, Pen, add, axis, chaikin, ease, finish, grain, ik, lerp, save_gif, side_pose,
                   track)

P = {"torso": 52, "neck": 44, "drop": 8, "ua": 30, "fa": 29, "th": 38, "sh": 36, "foot": 12, "sx": 14, "hx": 7}
HEAD_R = 40
S = 1.3
GROUND = 342.0
X = 214.0
FIG = {"head_radius": HEAD_R * S, "limb_width": 7 * S, "body_width": 22 * S, "hand_length": 7 * S}

INK = (38, 40, 58)
LIMB = (36, 38, 56)
WHITE = (252, 252, 250)
TEAL = (128, 168, 164)
TEAL_D = (92, 128, 126)
MUG = (214, 164, 58)
MUG_D = (160, 116, 36)
N = 96


def seated():
    return {"lean": 5, "neck": 4, "hip_l": 86, "knee_l": 84, "hip_r": 92, "knee_r": 92, "ankle_l": 2, "ankle_r": -2,
            "shoulder_l": 0, "elbow_l": 0, "shoulder_r": 0, "elbow_r": 0}


def pose(a):
    return side_pose(a, P, X, GROUND, S)


J0 = pose(seated())
TABLE_Y = J0["elbow_r"][1] - 2.0          # table top at elbow height
TABLE_C = (372.0, TABLE_Y)
MUG_AT = (304.0, TABLE_Y - 2)              # bottom-center of the mug on the table
MW, MH = 11 * S, 15 * S
HANDLE = (MUG_AT[0] - MW - 2, MUG_AT[1] - MH * 0.55)


# ---------------------------------------------------------------- background
def street(img, pen):
    for y in range(-10, 380, 3):
        t = max(0.0, min(1.0, y / 300))
        pen.poly([(-20, y), (660, y), (660, y + 3.2), (-20, y + 3.2)], (round(238 - 14 * t), round(238 - 10 * t), round(228 - 12 * t)))
    rnd = random.Random(5)
    # far buildings across the street
    x = 100
    while x < 680:
        w = rnd.uniform(70, 120); h = rnd.uniform(150, 230)
        col = rnd.choice([(222, 212, 192), (208, 204, 196), (228, 218, 204), (214, 206, 186)])
        pen.poly([(x, 250 - h), (x + w, 250 - h), (x + w, 252), (x, 252)], col)
        pen.poly([(x - 2, 250 - h - 6), (x + w + 2, 250 - h - 6), (x + w + 2, 250 - h), (x - 2, 250 - h)], (196, 188, 172))
        for wy in range(int(250 - h + 16), 228, 30):
            for wx in range(int(x + 10), int(x + w - 16), 24):
                pen.poly([(wx, wy), (wx + 12, wy), (wx + 12, wy + 18), (wx, wy + 18)], (184, 192, 196))
        x += w + rnd.uniform(4, 10)
    for tx in (300, 470, 610):  # young street trees
        pen.line([(tx, 252), (tx, 196)], (150, 136, 116), 4)
        for k in range(7):
            pen.ellipse((tx + rnd.uniform(-18, 18), 176 + rnd.uniform(-22, 16)), rnd.uniform(14, 22), rnd.uniform(12, 18),
                        (174 + rnd.randrange(-10, 10), 198 + rnd.randrange(-8, 8), 150))
    pen.poly([(-20, 250), (660, 250), (660, 268), (-20, 268)], (196, 196, 192))   # road
    # tree trunk behind the table, canopy across the top
    pen.poly([(150, 268), (158, 30), (168, 30), (176, 268)], (132, 112, 92))
    for k in range(16):
        pen.ellipse((rnd.uniform(60, 420), rnd.uniform(-10, 60)), rnd.uniform(28, 46), rnd.uniform(20, 30),
                    (120 + rnd.randrange(-12, 12), 160 + rnd.randrange(-10, 10), 110, 230))
    img.paste(img.filter(ImageFilter.GaussianBlur(3 * SS)))
    # near sidewalk
    pen.poly([(-20, 266), (660, 266), (660, 380), (-20, 380)], (226, 220, 206))
    for k in range(-6, 14):
        pen.line([(k * 60, 268), (k * 120 - 300, 380)], (210, 204, 190), 1.4)
    for y in (286, 312, 346):
        pen.line([(-20, y), (660, y)], (210, 204, 190), 1.4)
    pen.line([(-20, 267), (660, 267)], (188, 184, 176), 2)
    # lamp post
    pen.line([(560, 300), (560, 40)], (88, 96, 104), 5)
    pen.poly([(548, 40), (572, 40), (566, 18), (554, 18)], (88, 96, 104))
    pen.ellipse((560, 302), 10, 4, (88, 96, 104))
    # cafe front on the left: slate-blue frame, glass, an awning edge
    pen.poly([(-20, -20), (96, -20), (96, 300), (-20, 300)], (84, 96, 116))
    pen.poly([(4, 40), (80, 40), (80, 270), (4, 270)], (150, 170, 182))
    pen.poly([(4, 40), (40, 40), (12, 270), (4, 270)], (176, 194, 204))
    pen.line([(42, 40), (42, 270)], (84, 96, 116), 4)
    pen.poly([(-20, -20), (130, -20), (118, 22), (-20, 22)], (170, 96, 80))
    for k in range(5):
        pen.line([(k * 30 - 6, -20), (k * 30 - 10, 22)], (150, 80, 68), 2)



def leaves(pen, i):
    """Out-of-focus foreground leaves at the top corners, swaying."""
    rnd = random.Random(8)
    for k in range(14):
        side = -1 if k % 2 else 1
        bx = 640 + 10 if side == 1 else -10
        x = bx - side * rnd.uniform(0, 90); y = rnd.uniform(-10, 80)
        sw = 3 * math.sin(i * 0.15 + k)
        ang = rnd.uniform(0, 180) + sw * 4
        pen.ellipse((x + sw, y), rnd.uniform(16, 26), rnd.uniform(7, 11), (64 + rnd.randrange(20), 104 + rnd.randrange(20), 66, 235), ang=ang)


def chair(pen, j):
    px, py = j["pelvis"]
    back = px - 22 * S
    pen.line([(back, py + 4), (back - 6, py - 64 * S)], TEAL_D, 5)
    pen.line([(back - 2, py - 30 * S), (back - 5, py - 62 * S)], TEAL_D, 3)
    pen.arc((back - 4, py - 60 * S), 12, 6, 180, 360, TEAL_D, 4)
    pen.line([(back - 6, py + 6), (px + 22 * S, py + 6)], TEAL, 6)
    pen.line([(back, py + 8), (back - 6, GROUND)], TEAL_D, 4)
    pen.line([(px + 18 * S, py + 8), (px + 26 * S, GROUND)], TEAL_D, 4)


def table(pen):
    cx, cy = TABLE_C
    pen.poly([(cx - 6, cy + 10), (cx + 6, cy + 10), (cx + 5, GROUND - 6), (cx - 5, GROUND - 6)], TEAL_D)
    pen.ellipse((cx, GROUND - 4), 34, 7, TEAL_D)
    pen.ellipse((cx, cy + 5), 108, 17, TEAL_D)
    pen.ellipse((cx, cy), 108, 17, TEAL, TEAL_D, 1.6)
    # open notebook and a pen, a phone
    nb = (356, cy - 2)
    pen.poly([(nb[0] - 34, nb[1] + 4), (nb[0], nb[1] + 7), (nb[0] + 4, nb[1] - 6), (nb[0] - 28, nb[1] - 9)], (246, 240, 224), (170, 160, 140), 1.2)
    pen.poly([(nb[0], nb[1] + 7), (nb[0] + 36, nb[1] + 3), (nb[0] + 34, nb[1] - 10), (nb[0] + 4, nb[1] - 6)], (250, 246, 232), (170, 160, 140), 1.2)
    for k in range(3):
        pen.line([(nb[0] + 9, nb[1] - 4 + k * 3), (nb[0] + 28, nb[1] - 6 + k * 3)], (190, 184, 170), 1)
    pen.line([(nb[0] - 20, nb[1] + 10), (nb[0] + 8, nb[1] + 12)], (70, 74, 90), 2.4)
    pen.poly([(416, cy - 4), (446, cy - 6), (450, cy + 2), (420, cy + 4)], (52, 56, 66), (30, 32, 40), 1)


def mug(pen, base, i, steam=True):
    """A yellow mug standing at base (bottom-center), handle toward the drinker."""
    w, h = MW, MH
    x, y = base
    pen.arc((x - w - 1, y - h * 0.55), 6, 7, 90, 270, MUG_D, 3.2)
    pen.poly([(x - w, y - h), (x + w, y - h), (x + w * 0.92, y), (x - w * 0.92, y)], MUG, MUG_D, 1.6)
    pen.ellipse((x, y - h), w, 3.2, (110, 70, 40), MUG_D, 1.4)
    pen.line([(x + w * 0.45, y - h + 4), (x + w * 0.45, y - 3)], (236, 196, 110), 2)
    if steam:
        for k in range(2):
            pts = [(x - 4 + 7 * k + 3 * math.sin(i * 0.4 + q * 0.9 + k), y - h - 6 - q * 6) for q in range(5)]
            pen.line(pts, (255, 255, 255, 150), 2)


# ---------------------------------------------------------------- the character
def hand(pen, wr, el):
    ux, px = axis(el, wr)
    c = add(wr, ux, 3 * S)
    pen.ellipse(c, 6.2 * S, 5 * S, LIMB, ang=math.degrees(math.atan2(ux[1], ux[0])))
    pen.circle(add(add(wr, ux, 1 * S), px, -4.2 * S), 2.4 * S, LIMB)


def figure(pen, j, expr, mug_in_hand=None, i=0):
    near, far = "r", "l"
    for k in (far, near):
        pen.taper([j[f"hip_{k}"], j[f"knee_{k}"], j[f"ankle_{k}"]], LIMB, 8.5 * S, 6.5 * S)
        an, toe = j[f"ankle_{k}"], j[f"toe_{k}"]
        ux, _ = axis(an, toe)
        pen.ellipse(lerp(an, toe, 0.5), P["foot"] * S * 0.62, 4.6 * S, LIMB, ang=math.degrees(math.atan2(ux[1], ux[0])))
    table(pen)
    if not mug_in_hand:
        mug(pen, MUG_AT, i)
    pen.taper([j[f"shoulder_{far}"], j[f"elbow_{far}"], j[f"wrist_{far}"]], LIMB, 8 * S, 6 * S)
    hand(pen, j[f"wrist_{far}"], j[f"elbow_{far}"])
    ux, px = axis(j["neck"], j["pelvis"])
    top = add(j["neck"], ux, -2 * S); bot = add(j["pelvis"], ux, 6 * S)
    torso = chaikin([add(top, px, 7 * S), add(lerp(top, bot, 0.22), px, 16 * S), add(lerp(top, bot, 0.7), px, 14 * S),
                     add(bot, px, 11 * S), add(bot, px, -11 * S), add(lerp(top, bot, 0.7), px, -14 * S),
                     add(lerp(top, bot, 0.22), px, -16 * S), add(top, px, -7 * S)], 3)
    pen.poly(torso, WHITE, INK, 2.6)
    # head
    cx, cy = j["head"]; r = HEAD_R * S
    pen.circle((cx, cy), r, WHITE, INK, 2.6)
    e1, e2 = (cx + r * 0.16, cx + r * 0.56)
    ey = cy - r * 0.02
    for k, ex in enumerate((e1, e2)):
        sc = 1.0 if k == 0 else 0.85
        if expr in ("content", "smile_closed"):
            pen.arc((ex, ey), 5.6 * S * sc, 4 * S, 20, 160, INK, 2.6)
        elif expr == "blink":
            pen.line([(ex - 5 * S * sc, ey + 1), (ex + 5 * S * sc, ey + 1)], INK, 2.6)
        else:
            pen.ellipse((ex + 1.5 * S, ey), 3.4 * S * sc, 5.2 * S, INK)
        pen.arc((ex, ey - 9 * S), 5 * S * sc, 2.4 * S, 200, 330, INK, 2.2)
    mx, my = cx + r * 0.45, cy + r * 0.42
    if expr != "content":
        pen.arc((mx, my - 4 * S), 7 * S, 5 * S, 25, 150, INK, 2.6)
    else:
        pen.arc((mx, my - 2 * S), 4 * S, 3 * S, 20, 160, INK, 2.4)
    pen.circle((cx + r * 0.62, cy + r * 0.3), 4 * S, (250, 200, 196, 140))  # a little blush
    # near arm last
    pen.taper([j[f"shoulder_{near}"], j[f"elbow_{near}"], j[f"wrist_{near}"]], LIMB, 8 * S, 6 * S)
    if mug_in_hand:
        mug(pen, mug_in_hand, i, steam=False)
    hand(pen, j[f"wrist_{near}"], j[f"elbow_{near}"])


# ---------------------------------------------------------------- the shot
def build():
    rest = seated()
    on_table_l = ik(pose, dict(rest), "l", (262, TABLE_Y - 2), ("shoulder_l", "elbow_l"), ((-30, 150), (0, 150)))
    rest.update(shoulder_l=on_table_l["shoulder_l"], elbow_l=on_table_l["elbow_l"])
    rest_r = ik(pose, dict(rest), "r", (272, TABLE_Y + 1), ("shoulder_r", "elbow_r"), ((-30, 150), (0, 150)))
    grip = ik(pose, dict(rest), "r", HANDLE, ("shoulder_r", "elbow_r"), ((-30, 150), (0, 150)))
    jr = pose(rest)
    sip = ik(pose, dict(rest), "r", (jr["head"][0] + HEAD_R * S * 0.86, jr["head"][1] + HEAD_R * S * 0.62),
             ("shoulder_r", "elbow_r"), ((-30, 150), (0, 150)))
    keys = {"rest": (rest_r["shoulder_r"], rest_r["elbow_r"]), "grip": (grip["shoulder_r"], grip["elbow_r"]),
            "sip": (sip["shoulder_r"], sip["elbow_r"])}

    def arm(a, k0, k1, t):
        (s0, e0), (s1, e1) = keys[k0], keys[k1]
        a["shoulder_r"] = s0 + (s1 - s0) * ease(t); a["elbow_r"] = e0 + (e1 - e0) * ease(t)

    frames = []
    for i in range(N):
        a = dict(rest); expr = "smile"
        if i < 14:
            arm(a, "rest", "rest", 0)
        elif i < 24:
            arm(a, "rest", "grip", (i - 14) / 10)
        elif i < 28:
            arm(a, "grip", "grip", 0)
        elif i < 40:
            arm(a, "grip", "sip", (i - 28) / 12)
            a["neck"] = rest["neck"] - 6 * ease((i - 28) / 12)
        elif i < 54:
            arm(a, "sip", "sip", 0); a["neck"] = rest["neck"] - 6; expr = "content"
        elif i < 66:
            arm(a, "sip", "grip", (i - 54) / 12); a["neck"] = rest["neck"] - 6 * (1 - ease((i - 54) / 12))
        elif i < 78:
            arm(a, "grip", "rest", (i - 66) / 12)
        else:
            arm(a, "rest", "rest", 0)
            t = ease((i - 78) / 12); a["lean"] = rest["lean"] - 4 * t; a["neck"] = rest["neck"] - 5 * t
            expr = "smile_closed" if i >= 86 else "smile"
        if i in (8, 9, 74):
            expr = "blink"
        j = pose(a)
        f = {"facing": "right", "joints": j, "supported": ["pelvis"], "_expr": expr}
        held = 24 <= i < 67
        if held:
            ux, _ = axis(j["elbow_r"], j["wrist_r"])
            base = (j["wrist_r"][0] + MW + 2, j["wrist_r"][1] + MH * 0.55)
            f["holds"] = {"mug": "r"}; f["props"] = {"mug": j["wrist_r"]}; f["_mug"] = base
        else:
            f["props"] = {"mug": [round(HANDLE[0], 2), round(HANDLE[1], 2)]}
        if 36 <= i < 58:
            f["face_cover"] = True
        frames.append(f)
    return frames, rest


def camera(i):
    t = ease((i - 60) / 36)
    return (304 - 20 * t, 196 + 6 * t, 1.12 + 0.1 * t, 0.0, 0.0)


def render(out_dir):
    frames, rest = build()
    bd = Backdrop(street)
    out = []
    for i, f in enumerate(frames):
        cam = camera(i)
        img = bd.frame(cam)
        pen = Pen(img, cam)
        j = f["joints"]
        pen.ellipse((TABLE_C[0], GROUND - 2), 120, 10, (90, 90, 80, 40))
        chair(pen, j)
        figure(pen, j, f["_expr"], f.get("_mug"), i)
        leaves(pen, i)
        out.append(finish(grain(img, 0.03, 12)))
    save_gif(out_dir / "style-4.gif", out, 255)
    return (track("style4_cafe", frames, pose(rest), FIG),)
