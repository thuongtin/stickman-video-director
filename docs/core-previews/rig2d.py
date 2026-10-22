"""A small 2D stick-figure rig and drawing kit for the core-style previews.

Proportions are a dict, so each style keeps its own figure (big cartoon heads for Styles 3 and 4, a plain
line figure for Style 1). Joints come out in image coordinates (y down) with the lowest foot on the ground
line, which is what the posture gate reads. Pillow only.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFilter

SS = 2          # supersampling
W, H = 640, 360
FPS = 12


def rot(v, deg):
    a = math.radians(deg)
    return (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a))


def add(p, v, k=1.0):
    return (p[0] + v[0] * k, p[1] + v[1] * k)


def lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def axis(p, q):
    ax = (q[0] - p[0], q[1] - p[1]); n = math.hypot(*ax) or 1.0; ux = (ax[0] / n, ax[1] / n)
    return ux, (-ux[1], ux[0])


def ease(t):
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def mix(a, b, t):
    return {k: a.get(k, 0) * (1 - t) + b.get(k, 0) * t for k in set(a) | set(b)}


def chaikin(pts, n=2, closed=True):
    for _ in range(n):
        out = [] if closed else [pts[0]]
        m = len(pts) if closed else len(pts) - 1
        for i in range(m):
            p, q = pts[i], pts[(i + 1) % len(pts)]
            out += [lerp(p, q, 0.25), lerp(p, q, 0.75)]
        if not closed:
            out.append(pts[-1])
        pts = out
    return pts


# ---------------------------------------------------------------- kinematics
def _place(j, x, ground, s, low):
    return {k: [round(x + p[0] * s, 2), round(ground - (p[1] - low) * s, 2)] for k, p in j.items()}


def side_pose(a, P, x, ground, s=1.0, lift=0.0, low=None):
    """Facing right. lean (+ forward), neck (+ chin down), shoulder/hip (+ forward), elbow (+ fold up/forward),
    knee (+ fold back), ankle (+ toes up). Own right side is toward the camera."""
    up = rot((0, 1), -a.get("lean", 0)); down = (-up[0], -up[1])
    pelvis = (0.0, 0.0); neck = add(pelvis, up, P["torso"])
    j = {"pelvis": pelvis, "neck": neck, "head": add(neck, rot(up, -a.get("neck", 0)), P["neck"])}
    for k in ("l", "r"):
        ua = rot(down, a.get(f"shoulder_{k}", 0)); fa = rot(ua, a.get(f"elbow_{k}", 0))
        th = rot(down, a.get(f"hip_{k}", 0)); sh = rot(th, -a.get(f"knee_{k}", 0)); ft = rot(sh, 90 + a.get(f"ankle_{k}", 0))
        j[f"shoulder_{k}"] = add(neck, down, P["drop"])
        j[f"elbow_{k}"] = add(j[f"shoulder_{k}"], ua, P["ua"])
        j[f"wrist_{k}"] = add(j[f"elbow_{k}"], fa, P["fa"])
        j[f"hip_{k}"] = pelvis
        j[f"knee_{k}"] = add(pelvis, th, P["th"]); j[f"ankle_{k}"] = add(j[f"knee_{k}"], sh, P["sh"])
        j[f"toe_{k}"] = add(j[f"ankle_{k}"], ft, P["foot"])
    if low is None:
        low = min(min(j[f"ankle_{k}"][1], j[f"toe_{k}"][1]) for k in ("l", "r"))
    return _place(j, x, ground, s, low - lift)


def front_pose(a, P, x, ground, s=1.0, lift=0.0):
    """abd_* = arm out sideways, elb_* = elbow fold, leg_* = leg out sideways. Own left side is on screen right."""
    pelvis = (0.0, 0.0); neck = (0.0, P["torso"])
    j = {"pelvis": pelvis, "neck": neck, "head": (0.0, P["torso"] + P["neck"])}
    for k, out in (("l", 1), ("r", -1)):
        sh = (out * P["sx"], P["torso"] - P["drop"]); hp = (out * P["hx"], 0.0)
        ua = rot((0, -1), out * a.get(f"abd_{k}", 8)); fa = rot(ua, out * a.get(f"elb_{k}", 8))
        th = rot((0, -1), out * a.get(f"leg_{k}", 5))
        j[f"shoulder_{k}"] = sh; j[f"elbow_{k}"] = add(sh, ua, P["ua"]); j[f"wrist_{k}"] = add(j[f"elbow_{k}"], fa, P["fa"])
        j[f"hip_{k}"] = hp; j[f"knee_{k}"] = add(hp, th, P["th"]); j[f"ankle_{k}"] = add(j[f"knee_{k}"], th, P["sh"])
        j[f"toe_{k}"] = add(j[f"ankle_{k}"], (out * P["foot"] * 0.5, -1.0))
    low = min(j[f"toe_{k}"][1] for k in ("l", "r")) - lift
    return _place(j, x, ground, s, low)


def mirror(j, cx):
    """A facing-right pose turned to face left: mirror x and trade own sides (own left is then near the camera)."""
    out = {}
    for k, p in j.items():
        k2 = (k[:-2] + ("_r" if k.endswith("_l") else "_l")) if k.endswith(("_l", "_r")) else k
        out[k2] = [round(2 * cx - p[0], 2), p[1]]
    return out


def ik(pose_fn, a, k, target, keys, ranges, prefer=None):
    """Brute-force two-angle IK: set a[keys[0]], a[keys[1]] so wrist_k reaches target (image coords).
    pose_fn(a) -> joints. prefer(joints) adds a penalty (e.g. elbow inside the body)."""
    best = None
    (r0, r1) = ranges
    for step, span in ((4, None), (1, 4)):
        g0 = range(r0[0], r0[1] + 1, step) if span is None else range(int(best[1]) - span, int(best[1]) + span + 1)
        g1 = range(r1[0], r1[1] + 1, step) if span is None else range(int(best[2]) - span, int(best[2]) + span + 1)
        for v0 in g0:
            if not r0[0] <= v0 <= r0[1]:
                continue
            for v1 in g1:
                if not r1[0] <= v1 <= r1[1]:
                    continue
                a[keys[0]], a[keys[1]] = v0, v1
                j = pose_fn(a)
                c = dist(j[f"wrist_{k}"], target) + (prefer(j) if prefer else 0) + 0.01 * abs(v1)
                if best is None or c < best[0]:
                    best = (c, v0, v1)
    a[keys[0]], a[keys[1]] = best[1], best[2]
    return a


# ---------------------------------------------------------------- drawing
class Pen:
    """Draws in world coordinates through a camera (zoom about a world point, shake offset)."""

    def __init__(self, img, cam=None):
        self.img = img
        self.d = ImageDraw.Draw(img, "RGBA")
        cx, cy, z, ox, oy = cam or (W / 2, H / 2, 1.0, 0.0, 0.0)
        self.cam = (cx, cy, z, ox, oy)
        self.z = z

    def P(self, p):
        cx, cy, z, ox, oy = self.cam
        return ((p[0] - cx) * z + W / 2 + ox) * SS, ((p[1] - cy) * z + H / 2 + oy) * SS

    def w(self, w):
        return max(1, round(w * self.z * SS))

    def line(self, pts, fill, w, caps=True):
        q = [self.P(p) for p in pts]
        self.d.line(q, fill=fill, width=self.w(w), joint="curve")
        if caps:
            r = w * self.z * SS / 2
            for x, y in (q[0], q[-1]):
                self.d.ellipse([x - r, y - r, x + r, y + r], fill=fill)

    def taper(self, pts, fill, w0, w1):
        """A limb that narrows from w0 to w1 along its polyline, with round ends."""
        n = len(pts)
        lens = [0.0]
        for i in range(1, n):
            lens.append(lens[-1] + dist(pts[i - 1], pts[i]))
        tot = lens[-1] or 1.0
        left, right = [], []
        for i, p in enumerate(pts):
            a = pts[max(0, i - 1)]; b = pts[min(n - 1, i + 1)]
            _, nx = axis(a, b)
            w = (w0 + (w1 - w0) * lens[i] / tot) / 2
            left.append(add(p, nx, w)); right.append(add(p, nx, -w))
        self.poly(left + right[::-1], fill)
        self.circle(pts[0], w0 / 2, fill=fill); self.circle(pts[-1], w1 / 2, fill=fill)

    def circle(self, c, r, fill=None, outline=None, w=0):
        x, y = self.P(c); rr = r * self.z * SS
        self.d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=fill, outline=outline, width=self.w(w) if outline else 0)

    def ellipse(self, c, rx, ry, fill=None, outline=None, w=0, ang=0.0, n=36):
        pts = [add(c, rot((rx * math.cos(2 * math.pi * i / n), ry * math.sin(2 * math.pi * i / n)), ang)) for i in range(n)]
        self.poly(pts, fill, outline, w)

    def poly(self, pts, fill=None, outline=None, w=0):
        q = [self.P(p) for p in pts]
        if fill:
            self.d.polygon(q, fill=fill)
        if outline:
            self.d.line(q + [q[0]], fill=outline, width=self.w(w), joint="curve")

    def arc(self, c, rx, ry, a0, a1, fill, w, n=24):
        pts = [(c[0] + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), c[1] + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
               for i in range(n + 1)]
        self.line(pts, fill, w)


def wob(pts, amp, seed, closed=True, n=2):
    """Hand-drawn wobble: subdivide and nudge points; reuse a seed for two or three frames for line boil."""
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


def circle_pts(c, r, n=28, rx=None):
    rx = rx or r
    return [(c[0] + rx * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


# ---------------------------------------------------------------- frames and output
class Backdrop:
    """A static background drawn once at extra resolution, cropped per frame for the camera."""

    def __init__(self, draw_fn, margin=1.3):
        self.k = margin
        img = Image.new("RGB", (round(W * SS * self.k), round(H * SS * self.k)))
        pen = Pen(img, (W / 2, H / 2, self.k, 0, 0))
        pen.cam = (W / 2, H / 2, self.k, (W * self.k - W) / 2, (H * self.k - H) / 2)
        draw_fn(img, pen)
        self.img = img

    def frame(self, cam):
        cx, cy, z, ox, oy = cam
        k = self.k * SS
        # world point (wx, wy) sits at backdrop pixel ((wx - W/2) * k + W*SS*k/2)
        bx = lambda wx: (wx - W / 2) * k + W * SS * self.k / 2
        by = lambda wy: (wy - H / 2) * k + H * SS * self.k / 2
        left = cx - (W / 2 + ox) / z; top = cy - (H / 2 + oy) / z
        box = [bx(left), by(top), bx(left + W / z), by(top + H / z)]
        mw, mh = self.img.size
        dx = max(0.0, -box[0]) - max(0.0, box[2] - mw); dy = max(0.0, -box[1]) - max(0.0, box[3] - mh)
        box = (max(0.0, box[0] + dx), max(0.0, box[1] + dy), min(mw, box[2] + dx), min(mh, box[3] + dy))
        return self.img.resize((W * SS, H * SS), Image.BICUBIC, box=box)


def finish(img):
    return img.resize((W, H), Image.LANCZOS)


def grain(img, amount=0.07, seed=9):
    rg = random.Random(seed)
    w, h = img.size
    n = Image.frombytes("L", (w // 2, h // 2), bytes(rg.randrange(96, 160) for _ in range((w // 2) * (h // 2)))).resize((w, h))
    return Image.blend(img, Image.merge("RGB", [n] * 3), amount)


def vignette(img, strength=70, color=(40, 20, 0)):
    w, h = img.size
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    d.ellipse([-w * 0.15, -h * 0.25, w * 1.15, h * 1.25], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(w / 12))
    dark = Image.new("RGB", (w, h), color)
    inv = m.point(lambda v: round((255 - v) * strength / 255))
    return Image.composite(dark, img, inv)


def save_gif(path, frames, colors=200, probe_at=None):
    probe_at = probe_at or [round(i * (len(frames) - 1) / 5) for i in range(6)]
    probe = Image.new("RGB", (W, H * len(probe_at)))
    for i, k in enumerate(probe_at):
        probe.paste(frames[k], (0, H * i))
    ref = probe.quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
    pal = [f.quantize(palette=ref, dither=Image.Dither.NONE) for f in frames]
    pal[0].save(path, save_all=True, append_images=pal[1:], duration=round(1000 / FPS), loop=0, optimize=True, disposal=1)


def track(name, frames, rest, fig, **meta):
    return {"name": name, "source": "rig", "profile": "rig", "fps": FPS, **{k: round(v, 2) for k, v in fig.items()},
            "rest": rest, **meta, "frames": [{k: v for k, v in f.items() if not k.startswith("_")} for f in frames]}
