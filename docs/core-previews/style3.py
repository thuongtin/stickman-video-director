"""Style 3, prehistoric dark comedy: inside a cave, the chief offers a roast leg and the caveman takes it."""
import math
import random

from rig2d import (Backdrop, Pen, add, axis, chaikin, circle_pts, ease, finish, grain, ik, lerp, mirror, rot, save_gif,
                   side_pose, track, vignette, wob)

P = {"torso": 60, "neck": 44, "drop": 6, "ua": 33, "fa": 31, "th": 40, "sh": 38, "foot": 15, "sx": 14, "hx": 8}
HEAD_R = 42
S = 1.25
GROUND = 334.0
FIG = {"head_radius": HEAD_R * S, "limb_width": 3.4 * S, "body_width": 30 * S, "hand_length": 6 * S}

INK = (44, 30, 22)
SKIN = (252, 248, 238)
LID = (236, 226, 208)
HIDE = (214, 160, 92)
SPOT = (96, 60, 34)
HAIR = (34, 26, 22)
STUB = (128, 106, 88)
MEAT = (176, 76, 46)
MEAT_HI = (214, 118, 72)
BONE = (248, 244, 230)
SPARK = (250, 206, 80)

CAVE_X, CHIEF_X = 246.0, 412.0
MEET = (329.0, 204.0)
N = 84


def stand():
    return {"lean": 1, "neck": 2, "shoulder_l": -6, "elbow_l": 18, "shoulder_r": 6, "elbow_r": 20,
            "hip_l": -4, "knee_l": 3, "hip_r": 4, "knee_r": 4}


def cave_pose(a):
    return side_pose(a, P, CAVE_X, GROUND, S)


def chief_pose(a):
    """The chief faces left: author the pose facing right (own right near), then mirror it (own left near)."""
    return mirror(side_pose(a, P, 2 * CHIEF_X - CHIEF_X, GROUND, S), CHIEF_X)


# ---------------------------------------------------------------- background
def cave(img, pen):
    for y in range(-60, 420, 3):  # wall, darker up in the vault
        t = max(0.0, min(1.0, (y + 60) / 380))
        c = (round(112 + 96 * t), round(76 + 74 * t), round(46 + 50 * t))
        pen.poly([(-120, y), (760, y), (760, y + 3.2), (-120, y + 3.2)], c)
    rnd = random.Random(4)
    slabs = [[(-80, 40), (60, 20), (140, 70), (150, 190), (60, 250), (-80, 230)],
             [(150, -30), (300, -50), (330, 60), (280, 150), (170, 140)],
             [(300, 90), (440, 60), (470, 170), (420, 260), (310, 250), (290, 170)],
             [(440, -40), (620, -60), (720, 40), (690, 120), (520, 110)],
             [(-60, 230), (90, 250), (170, 300), (-60, 320)]]
    for k, sl in enumerate(slabs):
        pts = chaikin(wob(sl, 3, 10 + k, True, 2), 2)
        pen.poly(pts, (204, 154, 98) if k % 2 == 0 else (190, 140, 88), (118, 78, 46), 2.4)
        for _ in range(4):  # cracks
            p = (rnd.uniform(min(x for x, _ in sl) + 20, max(x for x, _ in sl) - 20), rnd.uniform(min(y for _, y in sl) + 20, max(y for _, y in sl) - 20))
            q = add(p, (rnd.uniform(-22, 22), rnd.uniform(10, 26)))
            pen.line(wob([p, lerp(p, q, 0.5), q], 1.5, rnd.randrange(999), False, 1), (140, 96, 58), 1.6)
    for x in range(-60, 720, 46):  # stalactites
        h = rnd.uniform(30, 70)
        pen.poly(wob([(x - 16, -50), (x + 18, -50), (x + 4, -50 + h + 40)], 1.5, x, True, 2), (150, 104, 62), (106, 70, 42), 2)
    # cave mouth on the right, a glimpse of the bright plain outside
    arch = chaikin([(500, 334), (500, 200), (530, 120), (600, 96), (690, 110), (720, 180), (720, 334)], 2)
    pen.poly(arch, (236, 206, 150))
    pen.poly(chaikin([(520, 290), (600, 250), (720, 262), (720, 334), (520, 334)], 2), (206, 168, 110))
    pen.poly(chaikin([(560, 250), (590, 200), (640, 196), (670, 240)], 1), (196, 160, 104))
    rim = chaikin([(470, 334), (476, 190), (520, 100), (600, 66), (700, 82), (760, 160), (760, 334), (722, 334),
                   (720, 180), (690, 112), (600, 98), (532, 122), (502, 200), (502, 334)], 1)
    pen.poly(rim, (120, 82, 50), INK, 2.4)
    # floor
    pen.poly(wob([(-120, 318), (200, 312), (480, 320), (760, 314), (760, 440), (-120, 440)], 2, 21, True, 3), (178, 128, 76))
    pen.line(wob([(-120, 318), (200, 312), (480, 320), (760, 314)], 1.4, 22, False, 4), (120, 82, 50), 2.2)
    for _ in range(70):
        x, y = rnd.uniform(-100, 740), rnd.uniform(330, 420)
        pen.ellipse((x, y), rnd.uniform(2, 6), rnd.uniform(1.4, 3), (150, 104, 62), (112, 76, 46), 1)
    # straw bed behind the caveman
    pen.poly(wob([(100, 300), (278, 300), (272, 314), (106, 314)], 1, 31), (134, 88, 50), INK, 2)
    for x in (112, 264):
        pen.line([(x, 312), (x, 330)], INK, 3.6)
    straw = chaikin(wob([(92, 304), (130, 276), (190, 270), (250, 276), (286, 302)], 2.5, 32, True, 3), 1)
    pen.poly(straw, (226, 188, 112), (150, 112, 58), 2)
    for i in range(46):
        x = rnd.uniform(104, 276); y = rnd.uniform(282, 302)
        pen.line([(x, y), (x + rnd.uniform(-10, 10), y + rnd.uniform(-5, 3))], (170, 130, 66), 1.3)
    pen.ellipse((136, 280), 22, 10, (232, 224, 204), (150, 120, 80), 1.6, ang=-8)  # hide pillow


def fire(pen, c, i):
    pen.line([(c[0] - 26, c[1] + 2), (c[0] + 22, c[1] - 6)], (120, 74, 40), 7)
    pen.line([(c[0] - 22, c[1] - 6), (c[0] + 26, c[1] + 2)], (100, 62, 34), 7)
    for k, col in enumerate(((232, 96, 36), (250, 160, 48), (255, 226, 120))):
        h = (62 - 17 * k) * (1 + 0.12 * math.sin(i * 1.9 + k * 1.3))
        w = 26 - 7 * k
        sw = 5 * math.sin(i * 1.1 + k)
        pts = [(c[0] - w, c[1]), (c[0] - w * 0.8, c[1] - h * 0.4), (c[0] - w * 0.2 + sw * 0.5, c[1] - h * 0.62),
               (c[0] + sw, c[1] - h), (c[0] + w * 0.35, c[1] - h * 0.55), (c[0] + w * 0.8, c[1] - h * 0.38), (c[0] + w, c[1])]
        pen.poly(chaikin(pts, 2), col, INK if k == 0 else None, 2)


def glow(img, pen, c, i):
    r = 150 + 8 * math.sin(i * 1.3)
    for k in range(6):
        rr = r * (1 - k * 0.14)
        pen.ellipse(c, rr, rr * 0.75, (255, 170, 70, 10))


# ---------------------------------------------------------------- characters
def foot(pen, j, k, s):
    an, toe = j[f"ankle_{k}"], j[f"toe_{k}"]
    ux, px = axis(an, toe)
    c = lerp(an, toe, 0.45)
    pen.ellipse(c, P["foot"] * s * 0.72, 5.2 * s, SKIN, INK, 2.0, ang=math.degrees(math.atan2(ux[1], ux[0])))


def hand(pen, j, k, s):
    pen.circle(j[f"wrist_{k}"], 5.4 * s, SKIN, INK, 2.0)


def meat(pen, wr, el, s, seed):
    ux, _ = axis(el, wr)
    c = add(wr, ux, 17 * s)
    ang = math.degrees(math.atan2(ux[1], ux[0]))
    pen.line([add(wr, ux, -9 * s), add(wr, ux, 6 * s)], BONE, 5 * s)
    for o in (-2.6, 2.6):
        pen.circle(add(add(wr, ux, -10 * s), (-ux[1], ux[0]), o * s), 3.0 * s, BONE, INK, 1.4)
    pen.poly(wob([add(c, rot((16 * s * math.cos(t), 11.5 * s * math.sin(t)), ang)) for t in
                  [2 * math.pi * q / 18 for q in range(18)]], 0.5, seed, True, 1), MEAT, INK, 2.2)
    pen.ellipse(add(add(c, ux, 3 * s), (-ux[1], ux[0]), -3 * s), 7 * s, 3.4 * s, MEAT_HI, ang=ang)


def tunic(pen, j, s, hw0, hw1, seed, spots):
    ux, px = axis(j["neck"], j["pelvis"])
    top = add(j["neck"], ux, 2 * s); hem = add(j["pelvis"], ux, 7 * s)
    pts = [add(top, px, hw0 * 0.5 * s), add(lerp(top, hem, 0.15), px, hw0 * s), add(lerp(top, hem, 0.6), px, hw1 * 0.95 * s),
           add(hem, px, hw1 * s)]
    for t in range(6):  # jagged hem
        a = lerp(add(hem, px, hw1 * s), add(hem, px, -hw1 * s), (t + 0.5) / 6)
        b = lerp(add(hem, px, hw1 * s), add(hem, px, -hw1 * s), (t + 1) / 6)
        pts += [add(a, ux, 6 * s), b]
    pts += [add(lerp(top, hem, 0.6), px, -hw1 * 0.95 * s), add(lerp(top, hem, 0.25), px, -hw0 * s), add(top, px, -hw0 * 0.2 * s)]
    pen.poly(wob(pts, 0.7, seed, True, 2), HIDE, INK, 2.6)
    for u, v, r in spots:
        p = add(lerp(top, hem, u), px, v * hw1 * s)
        pen.poly(wob(circle_pts(p, r * s, 8, r * s * 1.3), 0.8 * s, int(u * 100 + v * 10), True, 1), SPOT)


SPOTS = [(0.2, 0.2, 3.4), (0.35, -0.45, 4.2), (0.5, 0.35, 3.8), (0.68, -0.1, 4.6), (0.82, 0.5, 3.2), (0.86, -0.55, 3.6),
         (0.3, 0.65, 2.6), (0.6, -0.65, 2.8)]


def eyes(pen, cx, cy, r, s, sg, expr, look=1):
    for k, (ex, rx) in enumerate(((cx + sg * r * 0.12, 0.2), (cx + sg * r * 0.56, 0.16))):
        ry = 0.27 * r if expr != "surprised" else 0.31 * r
        rx = rx * r * (1.12 if expr == "surprised" else 1)
        ey = cy - r * 0.06
        if expr == "grin":  # squeezed happy eyes
            pen.arc((ex, ey + ry * 0.3), rx * 0.95, ry * 0.75, 200, 340, INK, 3.0)
            pen.line([(ex - rx * 1.1, ey - ry - 0.12 * r), (ex + rx * 1.1, ey - ry - 0.12 * r - 2 * s * (1 if k == 0 else -1))], INK, 3.0)
            continue
        pen.ellipse((ex, ey), rx, ry, SKIN, INK, 2.2)
        pr = 0.075 * r if expr != "surprised" else 0.055 * r
        pen.circle((ex + sg * look * rx * 0.35, ey + (-ry * 0.2 if expr == "grin" else ry * 0.12)), pr, INK)
        if expr in ("deadpan", "smug"):  # heavy upper lids: bored, or pleased with himself
            lid = 0.45 if expr == "deadpan" else 0.35
            pts = [(ex - rx * 1.05, ey - ry * 1.05), (ex + rx * 1.05, ey - ry * 1.05), (ex + rx * 1.05, ey - ry * (1 - 2 * lid)),
                   (ex - rx * 1.05, ey - ry * (1 - 2 * lid))]
            pen.poly(pts, LID)
            pen.line([(ex - rx * 1.02, ey - ry * (1 - 2 * lid)), (ex + rx * 1.02, ey - ry * (1 - 2 * lid))], INK, 2.4)
            pen.ellipse((ex, ey), rx, ry, None, INK, 2.2)
        # brows
        by = ey - ry - (0.16 * r if expr in ("surprised", "grin") else 0.06 * r)
        if expr == "surprised":
            pen.arc((ex, by + 4 * s), rx * 1.1, 4 * s, 200, 340, INK, 3.2)
        else:
            tilt = {"deadpan": 0, "smug": -2, "grin": -3}.get(expr, 0) * s * (1 if k == 0 else -1)
            pen.line([(ex - rx * 1.1, by - tilt), (ex + rx * 1.1, by + tilt)], INK, 3.6 if expr != "grin" else 3.0)


def head(pen, j, s, expr, seed, who):
    cx, cy = j["head"]; r = HEAD_R * s
    sg = 1 if j["toe_r"][0] > j["ankle_r"][0] else -1  # facing direction
    pen.line([j["neck"], lerp(j["neck"], j["head"], 0.5)], INK, 3.4 * s)
    pen.poly(wob(circle_pts((cx, cy), r, 26), 0.7, seed, True, 1), SKIN, INK, 2.8)
    # ear at the back of the head
    ex = cx - sg * r * 0.3
    pen.ellipse((ex, cy + r * 0.12), r * 0.12, r * 0.18, SKIN, INK, 2.0)
    if who == "cave":
        rnd = random.Random(7)
        pts = []
        a0, a1 = (205, 345) if sg == 1 else (195, 335)
        n = 15
        for i in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * i / n)
            rr = r * (1.05 if i % 2 == 0 else rnd.uniform(1.22, 1.4))
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        # fringe hanging over the forehead, back down to the nape
        fx = cx + sg * r * 0.3
        pts += [(fx + sg * r * 0.42, cy - r * 0.42), (fx + sg * r * 0.12, cy - r * 0.22), (fx - sg * r * 0.05, cy - r * 0.44),
                (fx - sg * r * 0.3, cy - r * 0.3), (fx - sg * r * 0.55, cy - r * 0.48), (cx - sg * r * 0.8, cy - r * 0.2),
                (cx - sg * r * 0.98, cy + r * 0.1)]
        pen.poly(wob(pts, 0.9, seed + 3, True, 1), HAIR)
        rnd = random.Random(42)
        for _ in range(22):  # stubble
            a = math.radians(rnd.uniform(30, 120) if sg == 1 else rnd.uniform(60, 150)); rr = rnd.uniform(0.62, 0.9) * r
            pen.circle((cx + rr * math.cos(a), cy + rr * math.sin(a)), 0.9 * s, STUB)
    else:
        # chief: bald, a tuft tied with a bone, grey stubble beard
        beard = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(10, 171, 10)]
        beard += [(cx - sg * r * 0.2, cy + r * 0.25), (cx + sg * r * 0.3, cy + r * 0.2), (cx + sg * r * 0.85, cy + r * 0.12)]
        pen.poly(beard, (234, 226, 214))
        rnd = random.Random(43)
        for _ in range(18):
            a = math.radians(rnd.uniform(15, 165)); rr = rnd.uniform(0.45, 0.95) * r
            pen.circle((cx + rr * math.cos(a), cy + rr * math.sin(a)), 1.0 * s, STUB)
        pen.poly(wob(circle_pts((cx, cy), r, 26), 0.7, seed, True, 1), None, INK, 2.8)
        tx, ty = cx - sg * r * 0.05, cy - r * 1.0
        pen.poly(wob([(tx - 9 * s, ty + 4 * s), (tx - 6 * s, ty - 10 * s), (tx, ty - 4 * s), (tx + 5 * s, ty - 12 * s),
                      (tx + 9 * s, ty + 4 * s)], 0.6, seed + 5, True, 1), HAIR)
        pen.line([(tx - 19 * s, ty - 1 * s), (tx + 19 * s, ty - 1 * s)], BONE, 5 * s)
        for bx in (-21, 21):
            for o in (-2.6, 2.6):
                pen.circle((tx + bx * s, ty - 1 * s + o * s), 3.0 * s, BONE, INK, 1.3)
        pen.line([(tx - 18 * s, ty - 3.6 * s), (tx + 18 * s, ty - 3.6 * s)], INK, 1.0)
        pen.line([(tx - 18 * s, ty + 1.6 * s), (tx + 18 * s, ty + 1.6 * s)], INK, 1.0)
        ex = cx - sg * r * 0.3
        pen.ellipse((ex, cy + r * 0.12), r * 0.12, r * 0.18, SKIN, INK, 2.0)
    eyes(pen, cx, cy, r, s, sg, expr)
    # nose and mouth
    nx = cx + sg * r * 0.86
    pen.arc((nx, cy + r * 0.2), r * 0.13, r * 0.12, -100 if sg == 1 else 100, 100 if sg == 1 else 280, INK, 2.2)
    mx, my = cx + sg * r * 0.42, cy + r * 0.55
    if expr == "deadpan":
        pen.line([(mx - r * 0.2, my), (mx + r * 0.22, my - r * 0.03)], INK, 2.6)
    elif expr == "surprised":
        pen.ellipse((mx, my), r * 0.1, r * 0.13, (120, 40, 36), INK, 2.2)
    elif expr == "smug":
        pen.arc((mx - sg * r * 0.05, my - r * 0.12), r * 0.32, r * 0.14, 20, 160, INK, 2.8)
    else:  # grin: big open mouth with teeth
        pts = [(mx - r * 0.36, my - r * 0.1), (mx + r * 0.36, my - r * 0.12), (mx + r * 0.22, my + r * 0.2), (mx - r * 0.2, my + r * 0.2)]
        pts = chaikin(pts, 2)
        pen.poly(pts, (112, 36, 34), INK, 2.4)
        pen.poly([(mx - r * 0.3, my - r * 0.08), (mx + r * 0.3, my - r * 0.1), (mx + r * 0.27, my - r * 0.01), (mx - r * 0.27, my + r * 0.01)],
                 SKIN)


def figure(pen, j, s, expr, seed, who, holds_meat=False):
    sg = 1 if j["toe_r"][0] > j["ankle_r"][0] else -1
    near = "r" if sg == 1 else "l"; far = "l" if near == "r" else "r"
    lw = 3.4 * s
    pen.line(wob([j[f"shoulder_{far}"], j[f"elbow_{far}"], j[f"wrist_{far}"]], 0.4, seed + 1, False, 1), INK, lw)
    hand(pen, j, far, s)
    for k in (far, near):
        pen.line(wob([j[f"hip_{k}"], j[f"knee_{k}"], j[f"ankle_{k}"]], 0.4, seed + ord(k), False, 1), INK, lw)
        foot(pen, j, k, s)
    if who == "cave":
        tunic(pen, j, s, 15, 18, seed + 9, SPOTS)
    else:
        tunic(pen, j, s, 19, 22, seed + 9, SPOTS[::-1])
    head(pen, j, s, expr, seed + 17, who)
    pen.line(wob([j[f"shoulder_{near}"], j[f"elbow_{near}"], j[f"wrist_{near}"]], 0.4, seed + 2, False, 1), INK, lw)
    if holds_meat:
        meat(pen, j[f"wrist_{near}"], j[f"elbow_{near}"], s, seed + 4)
    hand(pen, j, near, s)


def sparks(pen, c, i, s):
    for k in range(7):
        a = 2 * math.pi * k / 7 + i * 0.15
        r0, r1 = 26 * s, (36 + 4 * math.sin(i + k)) * s
        pen.line([add(c, (math.cos(a), math.sin(a)), r0), add(c, (math.cos(a), math.sin(a)), r1)], SPARK, 3)


# ---------------------------------------------------------------- the shot
def build():
    rest = stand()
    # chief: his near (own left) hand holds the roast low at his side, then offers it
    c_rest = dict(rest, shoulder_r=10, elbow_r=30)
    c_offer = ik(lambda a: chief_pose(a), dict(c_rest), "l", (MEET[0] + 4, MEET[1]), ("shoulder_r", "elbow_r"),
                 ((-40, 150), (0, 150)))
    k_take = ik(cave_pose, dict(rest), "r", (MEET[0] - 4, MEET[1]), ("shoulder_r", "elbow_r"), ((-40, 150), (0, 150)))
    hug_target = None
    cave_frames, chief_frames = [], []
    for i in range(N):
        a = dict(rest); c = dict(c_rest)
        if 12 <= i < 28:
            t = ease((i - 12) / 15); c["shoulder_r"] = c_rest["shoulder_r"] + (c_offer["shoulder_r"] - c_rest["shoulder_r"]) * t
            c["elbow_r"] = c_rest["elbow_r"] + (c_offer["elbow_r"] - c_rest["elbow_r"]) * t
        elif 28 <= i < 42:
            c.update(shoulder_r=c_offer["shoulder_r"], elbow_r=c_offer["elbow_r"])
        elif 42 <= i < 56:
            t = ease((i - 42) / 13); c["shoulder_r"] = c_offer["shoulder_r"] + (12 - c_offer["shoulder_r"]) * t
            c["elbow_r"] = c_offer["elbow_r"] + (24 - c_offer["elbow_r"]) * t
        elif i >= 56:
            c.update(shoulder_r=12, elbow_r=24)
            c["neck"] = 2 + 4 * math.sin((i - 56) * 0.9)  # chuckling
        if 26 <= i < 38:
            t = ease((i - 26) / 11); a["shoulder_r"] = rest["shoulder_r"] + (k_take["shoulder_r"] - rest["shoulder_r"]) * t
            a["elbow_r"] = rest["elbow_r"] + (k_take["elbow_r"] - rest["elbow_r"]) * t
        elif 38 <= i < 42:
            a.update(shoulder_r=k_take["shoulder_r"], elbow_r=k_take["elbow_r"])
        elif i >= 42:
            if hug_target is None:
                j0 = cave_pose(rest)
                hug_target = ik(cave_pose, dict(rest), "r", (j0["head"][0] + HEAD_R * S * 1.25, j0["neck"][1] - 4),
                                ("shoulder_r", "elbow_r"), ((-40, 150), (0, 150)))
            t = ease((i - 42) / 10)
            a["shoulder_r"] = k_take["shoulder_r"] + (hug_target["shoulder_r"] - k_take["shoulder_r"]) * t
            a["elbow_r"] = k_take["elbow_r"] + (hug_target["elbow_r"] - k_take["elbow_r"]) * t
            if i >= 54:
                a["neck"] = 2 - 5 * abs(math.sin((i - 54) * 0.7))  # happy bob
                a["lean"] = 1 - 2 * abs(math.sin((i - 54) * 0.7))
        jk, jc = cave_pose(a), chief_pose(c)
        fk = {"facing": "right", "joints": jk}
        fc = {"facing": "left", "joints": jc}
        if i < 38:
            fc["holds"] = {"meat": "l"}; fc["props"] = {"meat": jc["wrist_l"]}
        elif i < 42:  # both hands on it
            mid = [round(v, 2) for v in lerp(jk["wrist_r"], jc["wrist_l"], 0.5)]
            fk["holds"] = {"meat": "r"}; fk["props"] = {"meat": mid}
            fc["holds"] = {"meat": "l"}; fc["props"] = {"meat": mid}
        else:
            fk["holds"] = {"meat": "r"}; fk["props"] = {"meat": jk["wrist_r"]}
        fk["_expr"] = "deadpan" if i < 22 else ("surprised" if i < 44 else "grin")
        fc["_expr"] = "smug" if i < 56 else "grin"
        cave_frames.append(fk); chief_frames.append(fc)
    return cave_frames, chief_frames


def camera(i):
    t2 = ease((i - 48) / 26)
    z = 1.1 + 0.12 * t2
    cx = 326 - 36 * t2; cy = 192 + 8 * t2
    return (cx, cy, z, 0.0, 0.0)


def render(out_dir):
    kf, cf = build()
    bd = Backdrop(cave)
    frames = []
    for i in range(N):
        cam = camera(i)
        img = bd.frame(cam)
        pen = Pen(img, cam)
        glow(img, pen, (76, 300), i)
        seed = (i // 2) * 37
        for f, who in ((cf[i], "chief"), (kf[i], "cave")):
            j = f["joints"]
            pen.ellipse((j["pelvis"][0], GROUND + 2), 34 * S, 5 * S, (60, 36, 20, 60))
        figure(pen, cf[i]["joints"], S, cf[i]["_expr"], seed + 500, "chief", holds_meat="holds" in cf[i] and i < 38)
        figure(pen, kf[i]["joints"], S, kf[i]["_expr"], seed, "cave", holds_meat="holds" in kf[i])
        if 22 <= i < 36:
            sparks(pen, cf[i]["joints"]["wrist_l"], i, S)
        fire(pen, (76, GROUND - 4), i)
        img = vignette(grain(img, 0.05, 11), 90, (50, 24, 6))
        frames.append(finish(img))
    save_gif(out_dir / "style-3.gif", frames, 220)
    rest = cave_pose(stand())
    return (track("style3_caveman", kf, rest, FIG), track("style3_chief", cf, chief_pose(stand()), FIG))
