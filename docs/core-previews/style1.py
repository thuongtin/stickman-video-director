"""Style 1, classic minimalist line figure.
Light: a cage of worry slams down, the figure grips the bars, bends them and breaks out (black, one red accent).
Dark: the figure pushes a huge progress bar until it fills with electric blue (white, blue and red accents)."""
import math
import random

from PIL import Image

from rig2d import H, SS, W, Pen, add, axis, ease, finish, front_pose, ik, lerp, rot, save_gif, side_pose, track

P = {"torso": 62, "neck": 30, "drop": 6, "ua": 31, "fa": 30, "th": 44, "sh": 42, "foot": 12, "sx": 3, "hx": 2}
HEAD_R = 24
LW = 6.5
FIG = {"head_radius": HEAD_R, "limb_width": LW, "body_width": 6.0, "hand_length": 0.0}
RED = (226, 44, 52)
BLUE = (40, 150, 255)


def line_figure(pen, j, ink, bg, face=None, view="front"):
    """Hollow circle head, one line per limb segment, round caps, one weight."""
    for k in ("l", "r"):
        pen.line([j[f"hip_{k}"], j[f"knee_{k}"], j[f"ankle_{k}"]], ink, LW)
        if view != "front":
            pen.line([j[f"ankle_{k}"], j[f"toe_{k}"]], ink, LW)
    pen.line([j["pelvis"], j["neck"]], ink, LW)
    root = lerp(j["neck"], j["pelvis"], 0.08)
    for k in ("l", "r"):
        pen.line([root, j[f"elbow_{k}"], j[f"wrist_{k}"]], ink, LW)
    up = axis(j["neck"], j["head"])[0]
    r = HEAD_R
    pen.line([j["neck"], add(j["head"], up, -r)], ink, LW)
    pen.circle(j["head"], r, bg, ink, LW)
    if face:
        draw_face(pen, j["head"], ink, face, view)


def draw_face(pen, c, ink, face, view):
    cx, cy = c
    o = 7 if view == "right" else 0
    ex = (cx - 8 + o, cx + 8 + o)
    w = 3.6
    if face == "happy":
        for x in ex:
            pen.arc((x, cy - 1), 4, 3.5, 200, 340, ink, w)
        pen.arc((cx + o, cy + 4), 9, 7, 20, 160, ink, w)
        return
    for x in ex:
        pen.line([(x, cy - 5), (x, cy + 1)], ink, w)
    if face == "worried":
        pen.line([(ex[0] - 5, cy - 9), (ex[0] + 3, cy - 12)], ink, 3)
        pen.line([(ex[1] - 3, cy - 12), (ex[1] + 5, cy - 9)], ink, 3)
        pen.line([(cx - 7 + o, cy + 11), (cx - 2 + o, cy + 9), (cx + 3 + o, cy + 11), (cx + 8 + o, cy + 9)], ink, 3)
    elif face == "determined":
        pen.line([(ex[0] - 5, cy - 12), (ex[0] + 4, cy - 8)], ink, 3.2)
        pen.line([(ex[1] - 4, cy - 8), (ex[1] + 5, cy - 12)], ink, 3.2)
        pen.line([(cx - 6 + o, cy + 10), (cx + 6 + o, cy + 10)], ink, 3.4)
    else:
        pen.line([(cx - 5 + o, cy + 10), (cx + 5 + o, cy + 10)], ink, 3)


# ================================================================ light: the cage
GROUND_L = 318.0
FX = 320.0
CAGE_X = (232, 258, 286, 354, 382, 408)
CAGE_TOP = 100.0
BACK = (24, -20)
GRIP_Y = 198.0


def cage(pen, drop, bend, shake, alpha=255):
    """A perspective box of bars. drop = vertical offset (falling in), bend = how far the two middle bars bow out."""
    ink = (16, 16, 16, alpha)
    y0, y1 = CAGE_TOP + drop, GROUND_L + drop
    bx = [x + BACK[0] for x in CAGE_X]
    # back face
    for x in bx:
        pen.line([(x, y0 + BACK[1]), (x, y1 + BACK[1])], ink, 3.4)
    pen.line([(bx[0], y0 + BACK[1]), (bx[-1], y0 + BACK[1])], ink, 3.4)
    for x0, x1 in ((CAGE_X[0], bx[0]), (CAGE_X[-1], bx[-1])):
        pen.line([(x0, y0), (x1, y0 + BACK[1])], ink, 5)


def cage_front(pen, drop, bend, alpha=255):
    ink = (16, 16, 16, alpha)
    y0, y1 = CAGE_TOP + drop, GROUND_L + drop
    for k, x in enumerate(CAGE_X):
        if k in (2, 3) and bend:
            out = -1 if k == 2 else 1
            grip = (x + out * bend, GRIP_Y + drop)
            # quadratic curve through the grip point at its middle: control = 2*grip - (start+end)/2
            ctl = (2 * grip[0] - x, 2 * grip[1] - (y0 + y1) / 2)
            pts = [(x, y0)] + [lerp(lerp((x, y0), ctl, t), lerp(ctl, (x, y1), t), t) for t in [q / 16 for q in range(1, 16)]] + [(x, y1)]
            pen.line(pts, ink, 7)
        else:
            pen.line([(x, y0), (x, y1)], ink, 7)
    pen.line([(CAGE_X[0] - 6, y0), (CAGE_X[-1] + 6, y0)], ink, 9)
    pen.line([(CAGE_X[0] - 6, y1), (CAGE_X[-1] + 6, y1)], ink, 9)
    pen.line([(CAGE_X[0], y0 + 14), (CAGE_X[-1], y0 + 14)], ink, 4)


def lock(pen, c, ang=0.0):
    body = [add(c, rot(p, ang)) for p in ((-11, -2), (11, -2), (11, 16), (-11, 16))]
    pen.poly(body, RED)
    shackle = [add(c, rot((7 * math.cos(math.radians(a)), -2 - 9 * math.sin(math.radians(a))), ang)) for a in range(0, 181, 15)]
    pen.line(shackle, RED, 4.2)
    pen.circle(add(c, rot((0, 6), ang)), 2.4, (255, 255, 255))


def light_build():
    rest = {"abd_l": 9, "elb_l": 6, "abd_r": 9, "elb_r": 6, "leg_l": 6, "leg_r": 6}
    pose = lambda a, lift=0.0: front_pose(a, P, FX, GROUND_L, 1.0, lift)
    def prefer(j):
        return sum(4.0 for k in ("l", "r") if abs(j[f"elbow_{k}"][0] - FX) < 14)
    grip = dict(rest)
    ik(pose, grip, "r", (CAGE_X[2], GRIP_Y), ("abd_r", "elb_r"), ((-20, 170), (-150, 150)), prefer)
    ik(pose, grip, "l", (CAGE_X[3], GRIP_Y), ("abd_l", "elb_l"), ((-20, 170), (-150, 150)), prefer)
    wide = dict(grip)
    ik(pose, wide, "r", (CAGE_X[2] - 24, GRIP_Y), ("abd_r", "elb_r"), ((-20, 170), (-150, 150)), prefer)
    ik(pose, wide, "l", (CAGE_X[3] + 24, GRIP_Y), ("abd_l", "elb_l"), ((-20, 170), (-150, 150)), prefer)
    flinch = dict(rest, abd_l=28, elb_l=70, abd_r=28, elb_r=70)
    cheer = {"abd_l": 128, "elb_l": -6, "abd_r": 128, "elb_r": -6, "leg_l": 12, "leg_r": 12}

    def blend(a, b, t):
        t = ease(t)
        return {k: a[k] + (b[k] - a[k]) * t for k in a}

    frames = []
    N = 90
    for i in range(N):
        lift = 0.0; f = {"facing": "front"}
        drop = -420 if i < 8 else (-420 * (1 - ((i - 8) / 6) ** 2) if i < 14 else (-10 * math.sin(math.pi * (i - 14) / 4) if i < 18 else 0))
        bend = 0.0; face = "neutral"
        if i < 14:
            a = dict(rest)
        elif i < 28:
            a = blend(rest, flinch, (i - 14) / 4) if i < 20 else blend(flinch, rest, (i - 20) / 8); face = "worried"
        elif i < 38:
            a = blend(rest, grip, (i - 28) / 10); face = "worried"
        elif i < 54:
            t = (i - 38) / 16
            a = blend(grip, wide, t); bend = 24 * ease(t); face = "determined"
        elif i < 62:
            a = blend(wide, cheer, (i - 54) / 8); face = "happy"
        else:
            a = dict(cheer); face = "happy"
            u = (i - 64) / 10
            if 0 < u < 1:
                lift = 26 * math.sin(math.pi * u); f["airborne"] = True
            elif i >= 74:
                a = blend(cheer, rest, (i - 76) / 10) if i >= 76 else dict(cheer)
        j = pose(a, lift)
        f["joints"] = j
        if 38 <= i < 54:  # gripping the two middle bars, which bow out with the hands
            f["contacts"] = {"r": "bar_l", "l": "bar_r"}
            f["props"] = {"bar_l": [round(CAGE_X[2] - bend, 2), GRIP_Y], "bar_r": [round(CAGE_X[3] + bend, 2), GRIP_Y]}
        f["_drop"] = drop; f["_bend"] = bend; f["_face"] = face
        frames.append(f)
    return frames, pose(rest)


def light_render(out_dir):
    frames, rest = light_build()
    rnd = random.Random(3)
    shards = [(rnd.uniform(-1, 1), rnd.uniform(-1.2, 0.3), rnd.uniform(-0.4, 0.4), rnd.choice(CAGE_X), rnd.uniform(110, 300))
              for _ in range(18)]
    out = []
    for i, f in enumerate(frames):
        shake = 0.0
        if 14 <= i < 18:
            shake = 5 * math.sin(i * 2.3) * (18 - i) / 4
        if 54 <= i < 58:
            shake = 6 * math.sin(i * 2.7) * (58 - i) / 4
        z = 1.12 + 0.16 * ease((i - 28) / 26) - 0.16 * ease((i - 54) / 6)
        cam = (FX, 212, z, shake, shake * 0.4)
        img = Image.new("RGB", (W * SS, H * SS), (255, 255, 255))
        pen = Pen(img, cam)
        ink, bg = (16, 16, 16), (255, 255, 255)
        drop, bend = f["_drop"], f["_bend"]
        if i < 54:
            cage(pen, drop, bend, shake)
        if 14 <= i < 20:  # impact strokes at the feet of the cage
            k = (i - 14) / 6
            for x0, s in ((CAGE_X[0], -1), (CAGE_X[-1], 1)):
                for q in range(3):
                    a = math.radians(-20 - q * 25)
                    p = (x0 + s * (10 + 30 * k), GROUND_L - 4 - q * 8)
                    pen.line([p, add(p, (s * math.cos(a) * 16, math.sin(a) * 16))], ink, 4)
        if i >= 54:  # burst: red rays, flying bar pieces, the lock spinning away
            u = (i - 54) / 12
            if u < 1.4:
                for q in range(16):
                    a = 2 * math.pi * q / 16 + 0.2
                    r0, r1 = 60 + 220 * u, 90 + 320 * u
                    pen.line([add((FX, 210), (math.cos(a), math.sin(a)), r0), add((FX, 210), (math.cos(a), math.sin(a)), r1)],
                             RED, 9 * max(0.2, 1 - u))
            for vx, vy, va, x0, y0 in shards:
                t = (i - 54)
                if t < 22:
                    p = (x0 + vx * 22 * t, y0 + vy * 18 * t + 1.6 * t * t)
                    ang = va * t
                    pen.line([add(p, rot((0, -30), math.degrees(ang))), add(p, rot((0, 30), math.degrees(ang)))], ink, 7)
            t = i - 54
            lock(pen, (FX - 40 - 9 * t, 200 - 22 * t + 1.4 * t * t), ang=-25 * t)
        line_figure(pen, f["joints"], ink, bg, f["_face"])
        if i < 54:
            cage_front(pen, drop, bend)
            if i >= 8:
                sh = 4 * math.sin(i * 1.9) if 40 <= i < 54 else 0.0
                lock(pen, (FX + sh, 232 + drop), ang=sh * 2)
        out.append(finish(img))
    save_gif(out_dir / "style-1-light.gif", out, 64, list(range(0, len(out), 5)))
    return track("style1_light_cage", frames, rest, FIG)


# ================================================================ dark: the progress bar
GROUND_D = 318.0
BAR_W, BAR_H = 270.0, 128.0
CELLS = 8


def push_legs(t):
    ph = 2 * math.pi * t
    a = {}
    for k, off in (("l", 0), ("r", math.pi)):
        a[f"hip_{k}"] = 6 + 22 * math.sin(ph + off)
        a[f"knee_{k}"] = 10 + 34 * max(0.0, math.sin(ph + off + 1.2))
        a[f"ankle_{k}"] = 6 * math.sin(ph + off)
    return a


def dark_build():
    N = 92
    x0 = 150.0
    frames = []
    base = {"lean": 2, "neck": 0, "shoulder_l": -6, "elbow_l": 14, "shoulder_r": 6, "elbow_r": 16,
            "hip_l": -3, "knee_l": 3, "hip_r": 3, "knee_r": 3}
    prev = None
    for i in range(N):
        f = {"facing": "right"}; face = "neutral"; lift = 0.0
        if i < 10:
            x = x0; a = dict(base); t = ease(i / 10)
            a["lean"] = 2 + 16 * t
        elif i < 62:
            x = x0 + 3.0 * (i - 10)
            a = dict(base, lean=18, neck=-4); a.update(push_legs((i - 10) / 16)); face = "determined"
        else:
            x = x0 + 3.0 * 52
            t = ease((i - 62) / 8)
            a = dict(base, lean=18 - 18 * t, neck=-4 + 4 * t); face = "happy"
        bar_x = x0 + 46 + (x - x0)
        pose = lambda aa, x=x, lift=lift: side_pose(aa, P, x, GROUND_D, 1.0, lift)
        if i < 66:
            ik(pose, a, "r", (bar_x - 2, GROUND_D - 116), ("shoulder_r", "elbow_r"), ((-40, 170), (0, 150)))
            ik(pose, a, "l", (bar_x - 2, GROUND_D - 104), ("shoulder_l", "elbow_l"), ((-40, 170), (0, 150)))
            if i >= 62:  # hands leave the bar
                pass
        if i >= 66:
            t = ease((i - 66) / 8)
            a["shoulder_r"] = 60 + 74 * t; a["elbow_r"] = 40 - 30 * t
            a["shoulder_l"] = 20 - 30 * t; a["elbow_l"] = 30
            u = (i - 74) / 10
            if 0 < u < 1:
                lift = 20 * math.sin(math.pi * u); f["airborne"] = True
        j = side_pose(a, P, x, GROUND_D, 1.0, lift)
        f["joints"] = j
        if 8 <= i < 64:
            f["contacts"] = {"r": "bar", "l": "bar"}
            f["props"] = {"bar": [round(bar_x - 2, 2), round(GROUND_D - 110, 2)]}
            f["supported"] = ["wrist_r"]
            f["contact_tolerance"] = 0.3
        f["_x"] = x; f["_bar"] = bar_x; f["_face"] = face
        f["_fill"] = max(0.0, min(1.0, (i - 12) / 48))
        frames.append(f)
    return frames, side_pose(base, P, x0, GROUND_D, 1.0)


def dark_render(out_dir):
    frames, rest = dark_build()
    rnd = random.Random(5)
    dust = [(rnd.uniform(-200, 1000), rnd.uniform(40, 300), rnd.uniform(1.2, 2.6)) for _ in range(60)]
    out = []
    white, bg = (244, 244, 244), (0, 0, 0)
    for i, f in enumerate(frames):
        camx = f["_x"] + 150
        z = 1.15 + 0.1 * ease((i - 60) / 14)
        cam = (camx - 10, 214, z, 0.0, 0.0)
        img = Image.new("RGB", (W * SS, H * SS), bg)
        pen = Pen(img, cam)
        for x, y, r in dust:  # distant specks for a sense of travel
            pen.circle((x, y), r, (60, 60, 70))
        for k in range(-4, 30):  # dashed electric-blue floor line
            x = k * 48
            pen.line([(x, GROUND_D + 3), (x + 26, GROUND_D + 3)], BLUE, 4)
        bx = f["_bar"]; top = GROUND_D - BAR_H
        fill = f["_fill"]
        cw = (BAR_W - 16) / CELLS
        for c in range(CELLS):
            lit = min(1.0, max(0.0, fill * CELLS - c))
            if lit > 0:
                x0 = bx + 8 + c * cw + 3
                pen.poly([(x0, top + 11), (x0 + (cw - 6) * lit, top + 11), (x0 + (cw - 6) * lit, GROUND_D - 11), (x0, GROUND_D - 11)],
                         BLUE if c < CELLS - 1 or fill < 1 else (110, 200, 255))
        pen.poly([(bx, top), (bx + BAR_W, top), (bx + BAR_W, GROUND_D), (bx, GROUND_D)], None, white, 6)
        if 60 <= i < 80:  # completion burst
            u = (i - 60) / 14
            c = (bx + BAR_W / 2, top + BAR_H / 2)
            for q in range(18):
                a = 2 * math.pi * q / 18
                col = BLUE if q % 2 else RED
                pen.line([add(c, (math.cos(a), math.sin(a)), 120 + 160 * u), add(c, (math.cos(a), math.sin(a)), 150 + 230 * u)],
                         col, 7 * max(0.2, 1 - u))
            for q in range(10):
                a = 2 * math.pi * q / 10 + 0.3
                p = add(c, (math.cos(a), math.sin(a) * 0.7), 150 + 140 * u)
                pen.circle(p, 6 * max(0.0, 1.2 - u), RED if q % 2 else BLUE)
        if 10 <= i < 62 and i % 4 < 2:  # effort ticks behind the figure
            j = f["joints"]
            for q in range(3):
                p = (j["pelvis"][0] - 40 - q * 8, j["pelvis"][1] - 30 + q * 22)
                pen.line([p, add(p, (-18, 0))], BLUE, 3)
        line_figure(pen, f["joints"], white, bg, f["_face"], view="right")
        out.append(finish(img))
    save_gif(out_dir / "style-1-dark.gif", out, 96, list(range(0, len(out), 5)))
    return track("style1_dark_progress", frames, rest, FIG)


def render(out_dir):
    return (light_render(out_dir), dark_render(out_dir))
