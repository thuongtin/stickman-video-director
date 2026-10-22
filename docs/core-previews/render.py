#!/usr/bin/env python3
"""Motion previews for the core styles 1, 3 and 4, drawn from code rigs (Style 2 has its own lead in docs/lead-character/).

Writes, next to this file:
  style-1-light.gif   Classic Minimalist, light theme: a black line figure walks in and has an idea (gold bulb)
  style-1-dark.gif    Classic Minimalist, dark theme: a white line figure jumps for joy in a blue and red burst
  style-3.gif         Prehistoric dark comedy: a caveman in a hide tunic walks to a campfire and warms his hands
  style-4.gif         Cozy storytelling: a tracking walk through a park with a coffee cup, then a wave in front of a cafe
  tracks/*.json       every shot as posture-gate tracks (tests/verify-core-previews.py gates them)

The joints come from the Style 2 lead's rig (docs/lead-character/render.py); only the drawing changes per style.
Pillow is the only dependency. Nothing here is AI-generated: every frame is drawn from the joints in tracks/.
"""
import importlib.util
import json
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("lead_rig", HERE.parent / "lead-character/render.py")
rig = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rig)
SS, LEN, Pen = rig.SS, rig.LEN, rig.Pen
side_pose, front_pose, walk, stand_side, stand_front = rig.side_pose, rig.front_pose, rig.walk, rig.stand_side, rig.stand_front
lerp, add, axis, chaikin = rig.lerp, rig.add, rig.axis, rig.chaikin

W, H = 400, 225
FPS = 12


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, t)))


def mix(a, b, t):
    return {k: a.get(k, 0) * (1 - t) + b.get(k, 0) * t for k in set(a) | set(b)}


def track(name, frames, rest, fig, **meta):
    return {"name": name, "source": "rig", "profile": "rig", "fps": FPS, **{k: round(v, 2) for k, v in fig.items()},
            "rest": rest, **meta, "frames": [{k: v for k, v in f.items() if not k.startswith("_")} for f in frames]}


def save_gif(path, frames, colors=96):
    probe = Image.new("RGB", (W, H * 4))
    for i, k in enumerate((0, len(frames) // 3, 2 * len(frames) // 3, len(frames) - 1)):
        probe.paste(frames[k], (0, H * i))
    ref = probe.quantize(colors=colors, method=Image.Quantize.FASTOCTREE)
    pal = [f.quantize(palette=ref, dither=Image.Dither.NONE) for f in frames]
    pal[0].save(path, save_all=True, append_images=pal[1:], duration=round(1000 / FPS), loop=0, optimize=True, disposal=1)


def walk_in(n, x0, step, ground, s, stop=6):
    """A side walk to the right, easing into a stand; returns frames with joints."""
    out = []
    for i in range(n):
        out.append({"facing": "right", "joints": side_pose(walk(i / 12), x0 + i * step, ground, s)})
    for i in range(stop):
        t = (i + 1) / stop
        out.append({"facing": "right", "joints": side_pose(mix(walk(n / 12), stand_side(), t),
                                                         x0 + (n + 0.6 * (i + 1) / 2) * step, ground, s)})
    return out


# ================================================================ Style 1: Classic Minimalist
S1 = 0.85
S1_FIG = {"head_radius": 19 * S1, "limb_width": 2.6 * S1, "body_width": 3.0 * S1, "hand_length": 0.0}


def line_figure(img, j, s, ink, bg):
    """Hollow circle head, one line per limb segment, round caps, one weight (the Style 1 anchor)."""
    pen = Pen(img)
    w = 2.6 * s
    for k in ("l", "r"):
        pen.line([j[f"hip_{k}"], j[f"knee_{k}"], j[f"ankle_{k}"]], ink, w)
    pen.line([j["pelvis"], j["neck"]], ink, w)
    for k in ("l", "r"):
        pen.line([j["neck"], j[f"elbow_{k}"], j[f"wrist_{k}"]], ink, w)
    head = j["head"]; r = 19 * s
    up = axis(j["neck"], head)[0]
    pen.line([j["neck"], add(head, up, -r)], ink, w)
    pen.circle(head, r, fill=bg, outline=ink, w=w)


def burst(img, c, r, colors, rays=10, rot0=0.0, w=2.0):
    pen = Pen(img)
    for i in range(rays):
        a = rot0 + 2 * math.pi * i / rays
        p = (c[0] + math.cos(a) * r * 0.55, c[1] + math.sin(a) * r * 0.55)
        q = (c[0] + math.cos(a) * r, c[1] + math.sin(a) * r)
        pen.line([p, q], colors[i % len(colors)], w)


def bulb(img, c, k, glow):
    """A warm gold idea bulb (prop, not part of the figure)."""
    pen = Pen(img)
    gold, ink = (240, 178, 30), (20, 20, 20)
    if glow > 0:
        burst(img, (c[0], c[1] - 2 * k), (22 + 4 * glow) * k, [gold], rays=9, rot0=glow * 0.4, w=2.2 * k)
    pen.circle((c[0], c[1] - 3 * k), 9 * k, fill=gold, outline=ink, w=1.6 * k)
    pen.poly([(c[0] - 4.5 * k, c[1] + 4 * k), (c[0] + 4.5 * k, c[1] + 4 * k), (c[0] + 3.5 * k, c[1] + 10 * k),
              (c[0] - 3.5 * k, c[1] + 10 * k)], (200, 200, 200), ink, 1.4 * k)
    pen.line([(c[0] - 3.6 * k, c[1] + 7 * k), (c[0] + 3.6 * k, c[1] + 7 * k)], ink, 1.1 * k)


def style1_light():
    ground = 196.0
    frames = walk_in(26, 70.0, 4.6, ground, S1)
    last = frames[-1]["joints"]; x = last["pelvis"][0] - 0.0
    base = stand_side()
    raise_ = dict(base, shoulder_r=132, elbow_r=8, neck=-6)
    for i in range(30):
        t = ease(i / 7) if i < 8 else 1.0
        a = mix(base, raise_, t)
        if 8 <= i < 12:  # a tiny bounce on the toes when the idea lands
            a["knee_l"] = a["knee_r"] = 6 + 6 * math.sin(math.pi * (i - 8) / 4)
        frames.append({"facing": "right", "joints": side_pose(a, x, ground, S1), "_bulb": max(0.0, (i - 6) / 4)})
    outs = []
    for i, f in enumerate(frames):
        img = rig.canvas(W, H, (255, 255, 255))
        line_figure(img, f["joints"], S1, (18, 18, 18), (255, 255, 255))
        b = f.get("_bulb", 0)
        if b > 0:
            wr = f["joints"]["wrist_r"]
            k = min(1.0, b) * 0.9 + 0.1 * math.sin(i * 0.9)
            bulb(img, (wr[0] + 4, wr[1] - 26), k, glow=min(1.0, b - 0.5) if b > 0.5 else 0)
        outs.append(rig.finish(img))
    save_gif(HERE / "style-1-light.gif", outs, 32)
    return track("style1_light", frames, side_pose(stand_side(), 40, ground, S1), S1_FIG)


def style1_dark():
    ground = 200.0; x = 200.0
    rest = stand_front()
    up = {"abd_l": 150, "elb_l": 12, "abd_r": 150, "elb_r": 12, "leg_l": 12, "leg_r": 12}
    frames = []
    for i in range(48):
        f = {"facing": "front"}
        lift = 0.0
        if i < 8:
            a = dict(rest)
        elif i < 16:
            a = mix(rest, up, ease((i - 8) / 7))
        elif i < 28:
            a = dict(up); u = (i - 16) / 11
            lift = 26 * math.sin(math.pi * u)
            if 0 < u < 1:
                f["airborne"] = True
        elif i < 38:
            a = dict(up)
        else:
            a = mix(up, rest, ease((i - 38) / 9))
        f["joints"] = front_pose(a, x, ground, S1, lift=lift)
        f["_burst"] = (i - 18) / 14 if i >= 18 else -1
        frames.append(f)
    outs = []
    blue, red = (40, 150, 255), (240, 60, 70)
    for i, f in enumerate(frames):
        img = rig.canvas(W, H, (0, 0, 0))
        b = f["_burst"]
        if 0 <= b <= 1.4:
            c = (x, ground - 120 * S1)
            burst(img, c, 40 + 70 * b, [blue, red], rays=14, rot0=b * 0.6, w=3.0)
            pen = Pen(img)
            for n in range(8):  # small stars flying out
                a = 2 * math.pi * n / 8 + 0.3
                p = (c[0] + math.cos(a) * (60 + 60 * b), c[1] + math.sin(a) * (40 + 50 * b))
                rr = 3.5 * max(0.0, 1.3 - b)
                pen.circle(p, rr, fill=blue if n % 2 else red)
        line_figure(img, f["joints"], S1, (250, 250, 250), (0, 0, 0))
        outs.append(rig.finish(img))
    save_gif(HERE / "style-1-dark.gif", outs, 32)
    return track("style1_dark", frames, front_pose(rest, x, ground, S1), S1_FIG)


# ================================================================ Style 3: Prehistoric dark comedy
S3 = 0.9
S3_FIG = {"head_radius": 20 * S3, "limb_width": 2.4 * S3, "body_width": 26 * S3, "hand_length": 4 * S3}
BLACK3 = (34, 26, 20)
HIDE = (196, 132, 64)
HIDE_DARK = (140, 88, 40)


def wob(pts, amp, seed, closed=False, n=3):
    """A hand-drawn line: subdivide and nudge each point a little (the same seed for a few frames = line boil)."""
    rnd = random.Random(seed)
    src = pts + [pts[0]] if closed else pts
    out = []
    for i in range(len(src) - 1):
        p, q = src[i], src[i + 1]
        for k in range(n):
            t = k / n
            out.append((p[0] + (q[0] - p[0]) * t + rnd.uniform(-amp, amp), p[1] + (q[1] - p[1]) * t + rnd.uniform(-amp, amp)))
    if not closed:
        out.append(src[-1])
    return out


def circle_pts(c, r, n=18):
    return [(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def cave_bg():
    rnd = random.Random(3)
    img = rig.canvas(W, H, (232, 196, 140))
    d = ImageDraw.Draw(img)
    for y in range(0, 150 * SS, SS):  # dusk sky, ochre to pale
        t = y / (150 * SS)
        d.line([(0, y), (W * SS, y)], fill=(round(214 + 26 * t), round(150 + 50 * t), round(96 + 46 * t)))
    pen = Pen(img)
    pen.poly(wob([(0, 120), (90, 96), (170, 118), (260, 92), (400, 112), (400, 160), (0, 160)], 1.2, 5, True), (176, 120, 72))
    pen.poly(wob([(0, 150), (400, 146), (400, 225), (0, 225)], 1.0, 6, True), (166, 112, 62))
    # cave rock on the left with a dark mouth
    rock = wob([(-10, 40), (40, 30), (92, 60), (118, 120), (124, 165), (-10, 165)], 2.0, 7, True)
    pen.poly(rock, (128, 92, 60), BLACK3, 1.6)
    pen.poly(wob([(14, 165), (20, 112), (48, 88), (78, 100), (92, 140), (96, 165)], 1.6, 8, True), (58, 40, 30), BLACK3, 1.4)
    for _ in range(40):  # pebbles
        x, y = rnd.uniform(0, W), rnd.uniform(168, 222)
        pen.circle((x, y), rnd.uniform(0.8, 2.0), fill=(130, 88, 50))
    # subtle paper grain
    rg = random.Random(9)  # seeded, so every run draws the same grain
    grain = Image.frombytes("L", (W * SS, H * SS), bytes(rg.randrange(110, 146) for _ in range(W * SS * H * SS)))
    return Image.blend(img, Image.merge("RGB", [grain] * 3), 0.06)


def fire(img, c, i):
    pen = Pen(img)
    pen.line([(c[0] - 16, c[1] + 2), (c[0] + 14, c[1] - 3)], (110, 70, 40), 4.0)
    pen.line([(c[0] - 14, c[1] - 3), (c[0] + 16, c[1] + 2)], (96, 60, 34), 4.0)
    for k, col in enumerate(((236, 110, 40), (250, 170, 50), (255, 226, 120))):
        h2 = (34 - 9 * k) * (1 + 0.12 * math.sin(i * 1.7 + k))
        w2 = 14 - 4 * k
        sway = 3 * math.sin(i * 0.9 + k)
        pts = [(c[0] - w2, c[1]), (c[0] - w2 * 0.6, c[1] - h2 * 0.5), (c[0] + sway, c[1] - h2),
               (c[0] + w2 * 0.6, c[1] - h2 * 0.45), (c[0] + w2, c[1])]
        pen.poly(chaikin(pts, 1), col, BLACK3 if k == 0 else None, 1.2)
    d = ImageDraw.Draw(img, "RGBA")
    r = 46 + 3 * math.sin(i * 1.3)
    d.ellipse([(c[0] - r) * SS, (c[1] - r * 0.6) * SS, (c[0] + r) * SS, (c[1] + r * 0.4) * SS], fill=(255, 190, 90, 34))


def caveman(img, j, s, seed, expr):
    """Crude black outline, white round head, cartoon face, thin stick limbs, a one-shoulder hide tunic."""
    pen = Pen(img)
    lw = 2.4 * s
    far, near = "l", "r"  # facing right: own right side is toward the camera

    def limb(k):
        pen.line(wob([j[f"shoulder_{k}"], j[f"elbow_{k}"], j[f"wrist_{k}"]], 0.5, seed + ord(k)), BLACK3, lw)
        pen.circle(j[f"wrist_{k}"], 2.8 * s, fill=BLACK3)

    def leg(k):
        pen.line(wob([j[f"hip_{k}"], j[f"knee_{k}"], j[f"ankle_{k}"]], 0.5, seed + 7 + ord(k)), BLACK3, lw)
        pen.line([lerp(j[f"toe_{k}"], j[f"ankle_{k}"], 1.3), j[f"toe_{k}"]], BLACK3, 3.4 * s)

    limb(far); leg(far); leg(near)
    # hide tunic: a sack shape from the neck to below the hips, jagged hem, one strap, a few spots
    ux, px = axis(j["neck"], j["pelvis"])
    top = add(j["neck"], ux, 3 * s); hem = add(j["pelvis"], ux, 10 * s)
    hw = 13 * s
    body = [add(top, px, 5 * s), add(lerp(top, hem, 0.4), px, hw), add(hem, px, hw + 1 * s)]
    teeth = 5
    for t in range(teeth):
        a = lerp(add(hem, px, hw + 1 * s), add(hem, px, -hw - 1 * s), (t + 0.5) / teeth)
        b = lerp(add(hem, px, hw + 1 * s), add(hem, px, -hw - 1 * s), (t + 1) / teeth)
        body += [add(a, ux, 4 * s), b]
    body += [add(lerp(top, hem, 0.4), px, -hw), add(top, px, -6 * s)]
    pen.poly(wob(body, 0.6, seed + 3, True, 2), HIDE, BLACK3, 1.7 * s)
    for t, o in ((0.35, 4), (0.6, -5), (0.8, 6), (0.5, 0)):
        pen.circle(add(lerp(top, hem, t), px, o * s), 1.8 * s, fill=HIDE_DARK)
    # head
    cx, cy = j["head"]; r = 20 * s
    pen.line([j["neck"], lerp(j["neck"], j["head"], 0.4)], BLACK3, lw)
    pen.poly(wob(circle_pts((cx, cy), r), 0.5, seed + 11, True, 2), (255, 255, 255), BLACK3, 1.8 * s)
    # messy black hair tuft and a stubbly jaw
    tuft = [(cx - r * 0.9, cy - r * 0.35), (cx - r * 0.8, cy - r * 1.05), (cx - r * 0.3, cy - r * 1.25), (cx - r * 0.1, cy - r * 0.95),
            (cx + r * 0.25, cy - r * 1.3), (cx + r * 0.55, cy - r * 0.9), (cx + r * 0.8, cy - r * 0.75), (cx + r * 0.2, cy - r * 0.7),
            (cx - r * 0.45, cy - r * 0.6)]
    pen.poly(wob(tuft, 0.4, seed + 13, True, 1), BLACK3)
    rnd = random.Random(42)
    for _ in range(14):
        a = rnd.uniform(0.25, 1.35); rr = rnd.uniform(0.62, 0.86)
        pen.circle((cx + r * rr * math.cos(a), cy + r * rr * math.sin(a)), 0.55 * s, fill=(120, 110, 100))
    # face toward the right
    ex, ey = cx + r * 0.42, cy - r * 0.08
    if expr == "happy":
        pen.arc([ex - 3.5 * s, ey - 2 * s, ex + 3.5 * s, ey + 4 * s], 200, 340, BLACK3, 1.6 * s)
    else:
        pen.circle((ex, ey), 2.0 * s, fill=BLACK3)
    pen.line([(ex - 4 * s, ey - 6.5 * s), (ex + 4 * s, ey - (5.0 if expr == "happy" else 7.5) * s)], BLACK3, 1.8 * s)
    pen.circle((cx + r * 0.98, cy + r * 0.12), 2.6 * s, fill=(255, 255, 255), outline=BLACK3, w=1.3 * s)  # nose
    mx, my = cx + r * 0.5, cy + r * 0.5
    if expr == "happy":
        pen.arc([mx - 6 * s, my - 6 * s, mx + 5 * s, my + 2 * s], 20, 150, BLACK3, 1.6 * s)
    else:
        pen.line([(mx - 4 * s, my), (mx + 3.5 * s, my - 0.6 * s)], BLACK3, 1.6 * s)
    limb(near)


def style3():
    ground = 196.0
    frames = walk_in(24, 140.0, 3.4, ground, S3)
    x = frames[-1]["joints"]["pelvis"][0]
    base = stand_side()
    warm = dict(base, lean=8, neck=6, shoulder_r=72, elbow_r=22, shoulder_l=64, elbow_l=28)
    for i in range(30):
        t = ease(i / 8)
        a = mix(base, warm, t)
        if i >= 10:  # rub the hands over the fire
            a["elbow_r"] = 22 + 8 * math.sin(i * 1.4); a["elbow_l"] = 28 - 8 * math.sin(i * 1.4)
        frames.append({"facing": "right", "joints": side_pose(a, x, ground, S3), "_expr": "happy" if i >= 12 else "plain"})
    fire_at = (x + 46, ground - 2)
    bg = cave_bg()
    outs = []
    for i, f in enumerate(frames):
        img = bg.copy()
        fire(img, fire_at, i)
        j = f["joints"]
        rig.shadow(img, j["pelvis"][0], ground + 1, 26, S3)
        caveman(img, j, S3, seed=(i // 3) * 31, expr=f.get("_expr", "plain"))
        outs.append(rig.finish(img))
    save_gif(HERE / "style-3.gif", outs, 128)
    return track("style3_campfire", frames, side_pose(stand_side(), 140, ground, S3), S3_FIG,
                 solids={"campfire": [36, 30]}, _fire=fire_at)


# ================================================================ Style 4: Cozy storytelling
S4 = 0.85
S4_FIG = {"head_radius": 21 * S4, "limb_width": 2.4 * S4, "body_width": 26 * S4, "hand_length": 4 * S4}
INK4 = (40, 36, 44)
CUP = (214, 96, 64)


def cozy_figure(img, j, s, view, expr="smile", cup=None):
    """White filled round head with dot eyes, brows and a curved mouth; slim white tapered torso; dark limbs."""
    pen = Pen(img)
    lw = 2.4 * s

    def arm(k):
        pen.line([j[f"shoulder_{k}"], j[f"elbow_{k}"], j[f"wrist_{k}"]], INK4, lw)
        pen.circle(j[f"wrist_{k}"], 2.7 * s, fill=INK4)
        if cup == k:
            wr = j[f"wrist_{k}"]
            c = (wr[0] + (3 if view == "right" else 0) * s, wr[1] - 4 * s)
            pen.poly([(c[0] - 4.5 * s, c[1] - 6 * s), (c[0] + 4.5 * s, c[1] - 6 * s), (c[0] + 3.6 * s, c[1] + 5 * s),
                      (c[0] - 3.6 * s, c[1] + 5 * s)], CUP, INK4, 1.2 * s)
            pen.line([(c[0] - 5 * s, c[1] - 6.5 * s), (c[0] + 5 * s, c[1] - 6.5 * s)], (250, 246, 236), 2.0 * s)
            pen.line([(c[0] - 3.8 * s, c[1] - 0.5 * s), (c[0] + 3.8 * s, c[1] - 0.5 * s)], (250, 246, 236), 1.6 * s)

    def leg(k):
        pen.line([j[f"hip_{k}"], j[f"knee_{k}"], j[f"ankle_{k}"]], INK4, lw)
        pen.line([lerp(j[f"toe_{k}"], j[f"ankle_{k}"], 1.2), j[f"toe_{k}"]], INK4, 3.6 * s)

    side = view in ("right", "left")
    if side:
        near = "r" if view == "right" else "l"; far = "l" if near == "r" else "r"
        arm(far)
    leg("l"); leg("r")
    ux, px = axis(j["neck"], j["pelvis"])
    top = add(j["neck"], ux, 1 * s); bot = add(j["pelvis"], ux, 2 * s)
    wt, wb = (6.5, 9.5) if side else (14.5, 10.0)
    torso = chaikin([add(top, px, wt * s), add(bot, px, wb * s), add(bot, px, -wb * s), add(top, px, -wt * s)], 2)
    if not side:  # the arms start under the torso's shoulders, so they grow out of the body
        arm("l"); arm("r")
    pen.poly(torso, (255, 255, 255), INK4, 1.6 * s)
    cx, cy = j["head"]; r = 21 * s
    pen.line([j["neck"], lerp(j["neck"], j["head"], 0.3)], INK4, lw)
    pen.circle((cx, cy), r, fill=(255, 255, 255), outline=INK4, w=1.7 * s)
    if side:
        sg = 1 if view == "right" else -1
        xs = (cx + sg * r * 0.18, cx + sg * r * 0.62); my = cy + r * 0.38; mx = cx + sg * r * 0.42
    else:
        xs = (cx - r * 0.32, cx + r * 0.32); my = cy + r * 0.4; mx = cx
    for x in xs:
        pen.d.ellipse([(x - 1.5 * s) * SS, (cy - 1.2 * s) * SS, (x + 1.5 * s) * SS, (cy + 3.2 * s) * SS], fill=INK4)
        pen.arc([x - 3 * s, cy - 7.5 * s, x + 3 * s, cy - 2.5 * s], 215, 325, INK4, 1.2 * s)
    if expr == "happy":
        pen.poly(chaikin([(mx - 5.5 * s, my - 1.5 * s), (mx + 5.5 * s, my - 1.5 * s), (mx, my + 4.5 * s)], 1), (220, 96, 90), INK4, 1.2 * s)
    else:
        pen.arc([mx - 5 * s, my - 4.5 * s, mx + 5 * s, my + 1.5 * s], 25, 155, INK4, 1.4 * s)
    if side:
        arm(near)


def park_bg(scroll):
    img = rig.canvas(W, H, (180, 220, 240))
    d = ImageDraw.Draw(img)
    for y in range(0, 140 * SS, SS):
        t = y / (140 * SS)
        d.line([(0, y), (W * SS, y)], fill=(round(150 + 90 * t), round(200 + 40 * t), round(236 + 10 * t)))
    pen = Pen(img)
    # far hills (slow), city silhouettes, then trees (faster), path in front
    off = -(scroll * 0.2) % 200
    for k in range(-1, 4):
        x = k * 200 + off
        pen.poly(chaikin([(x - 40, 150), (x + 50, 104), (x + 140, 118), (x + 240, 150)], 2), (150, 196, 150))
    off = -(scroll * 0.45) % 120
    for k in range(-1, 5):
        x = k * 120 + off
        pen.rrect([x, 96, x + 34, 150], 3, (196, 186, 214), 0, fill=(206, 196, 222))
        pen.rrect([x + 44, 112, x + 72, 150], 3, (226, 196, 176), 0, fill=(236, 206, 186))
        for wy in (104, 116, 128):
            pen.rrect([x + 8, wy, x + 14, wy + 6], 1, (255, 236, 170), 0, fill=(255, 236, 170))
    pen.poly([(0, 148), (W, 148), (W, H), (0, H)], (126, 186, 110))
    pen.poly([(0, 176), (W, 176), (W, 214), (0, 214)], (236, 214, 176))
    off = -(scroll * 1.0) % 140
    for k in range(-1, 4):
        x = k * 140 + off
        pen.line([(x + 30, 150), (x + 30, 120)], (126, 92, 66), 5)
        pen.circle((x + 30, 108), 22, fill=(92, 160, 96))
        pen.circle((x + 18, 118), 14, fill=(104, 172, 104))
        pen.circle((x + 44, 116), 15, fill=(84, 150, 88))
        # bench every other tree
        if k % 2 == 0:
            pen.line([(x + 70, 168), (x + 112, 168)], (150, 104, 70), 4)
            pen.line([(x + 74, 168), (x + 74, 176)], (110, 78, 56), 2.5)
            pen.line([(x + 108, 168), (x + 108, 176)], (110, 78, 56), 2.5)
    return img


def cafe_bg():
    img = rig.canvas(W, H, (250, 226, 196))
    pen = Pen(img)
    pen.poly([(0, 0), (W, 0), (W, 160), (0, 160)], (242, 212, 178))
    # cafe front: awning, two warm windows, door
    pen.rrect([40, 40, 360, 160], 4, (170, 110, 80), 2, fill=(196, 132, 96))
    for k in range(8):
        col = (232, 92, 80) if k % 2 == 0 else (250, 244, 232)
        pen.poly([(40 + k * 40, 28), (80 + k * 40, 28), (80 + k * 40, 50), (40 + k * 40, 50)], col)
    pen.poly([(40, 50), (360, 50), (360, 56), (40, 56)], (200, 70, 64))
    for x0 in (62, 262):
        pen.rrect([x0, 74, x0 + 78, 136], 3, (120, 80, 60), 2, fill=(255, 220, 140))
        pen.line([(x0 + 39, 74), (x0 + 39, 136)], (120, 80, 60), 2)
        for px_, py in ((x0 + 18, 98), (x0 + 58, 108)):
            pen.circle((px_, py), 6, fill=(255, 240, 190))
    pen.rrect([172, 78, 228, 160], 3, (100, 64, 48), 2, fill=(126, 84, 62))
    pen.poly([(0, 160), (W, 160), (W, H), (0, H)], (214, 192, 170))
    for x in range(0, W, 40):
        pen.line([(x, 160), (x - 30, H)], (198, 176, 154), 1.2)
    pen.circle((364, 150), 12, fill=(96, 160, 96)); pen.rrect([354, 150, 374, 166], 2, (150, 90, 60), 0, fill=(170, 104, 70))
    return img


def style4():
    s = S4
    cup_arm = {"shoulder_r": 18, "elbow_r": 95}
    ground = 206.0; x = 170.0
    shot1 = []
    for i in range(40):  # tracking walk: the camera follows, the park scrolls behind
        a = walk(i / 12); a.update(cup_arm)
        j = side_pose(a, x, ground, s)
        shot1.append({"facing": "right", "joints": j, "holds": {"cup": "r"}, "props": {"cup": j["wrist_r"]}, "_scroll": i * 4.0})
    shot2 = []
    rest = dict(stand_front(), abd_r=14, elb_r=118)  # own right hand keeps the cup at the waist (screen left)
    gx, gy = 200.0, 214.0
    for i in range(36):
        a = dict(rest); expr = "smile"
        if 4 <= i < 11:
            t = ease((i - 4) / 7); a["abd_l"] = 9 + (100 - 9) * t; a["elb_l"] = 8 + (50 - 8) * t
        elif 11 <= i < 26:
            a["abd_l"] = 100; a["elb_l"] = 50 + 16 * math.sin(2 * math.pi * (i - 11) / 7); expr = "happy"
        elif 26 <= i < 33:
            t = ease((i - 26) / 7); a["abd_l"] = 100 + (9 - 100) * t; a["elb_l"] = 50 + (8 - 50) * t
        j = front_pose(a, gx, gy, 1.05)
        shot2.append({"facing": "front", "joints": j, "holds": {"cup": "r"}, "props": {"cup": j["wrist_r"]}, "_expr": expr})
    outs = []
    for f in shot1:
        img = park_bg(f["_scroll"]); j = f["joints"]
        rig.shadow(img, j["pelvis"][0], ground + 1, 22, s)
        cozy_figure(img, j, s, "right", cup="r")
        outs.append(rig.finish(img))
    cbg = cafe_bg()
    for f in shot2:
        img = cbg.copy(); j = f["joints"]
        rig.shadow(img, j["pelvis"][0], gy + 1, 30, 1.05)
        cozy_figure(img, j, 1.05, "front", f["_expr"], cup="r")
        outs.append(rig.finish(img))
    save_gif(HERE / "style-4.gif", outs, 160)
    fig2 = {k: v / S4 * 1.05 for k, v in S4_FIG.items()}
    return (track("style4_park_walk", shot1, side_pose(dict(stand_side(), **cup_arm), x, ground, s), S4_FIG),
            track("style4_cafe_wave", shot2, front_pose(rest, gx, gy, 1.05), fig2))


def main():
    out = HERE / "tracks"; out.mkdir(exist_ok=True)
    t3 = style3()
    fire_at = t3.pop("_fire")
    for f in t3["frames"]:
        f["props"] = {"campfire": [round(fire_at[0], 2), round(fire_at[1] - 15, 2)]}
    tracks = [style1_light(), style1_dark(), t3, *style4()]
    for t in tracks:
        (out / f"{t['name']}.json").write_text(json.dumps(t, indent=1))


if __name__ == "__main__":
    main()
