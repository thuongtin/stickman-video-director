#!/usr/bin/env python3
"""Draw Style 5 (Historical Cartoon) from a code rig: one drawing grammar, several era packs.

Writes, next to this file:
  sheet.png          cast sheet: four era cast cards (front and side), expressions, poses, palettes
  motion.gif         two-shot motion clip (Roman soldier walks a country road, then an Edo-period student waves)
  tracks/*.json      every pose drawn above, as posture-gate tracks (tests/verify-historical-cartoon.py gates them)

The rig math (joint layout, walk cycle, front/side poses) is the Style 2 lead's, imported from
docs/lead-character/render.py; only the drawing differs. Pillow is the only dependency. Nothing here is
AI-generated: every frame is drawn from the joints in tracks/.
"""
import importlib.util
import json
import math
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("lead_rig", HERE.parent / "lead-character" / "render.py")
rig = importlib.util.module_from_spec(_spec)  # the Style 2 lead's rig
_spec.loader.exec_module(rig)

SS = rig.SS
LEN = rig.LEN
HEAD_R = rig.HEAD_R
add, lerp, axis, chaikin, rot = rig.add, rig.lerp, rig.axis, rig.chaikin, rig.rot

INK = (22, 20, 20)
WHITE = (255, 255, 255)
LINE = 2.2    # thick clean outline (the style's "thick clean black outlines")
LIMB = 2.2    # thin black stick limbs

# ---------------------------------------------------------------- era cast cards (plain colours, two non-colour differences each)
CAST = {
    "soldier": {
        "label": "Roman soldier", "era": "Roman",
        "card": "Bronze-gold helmet with a black horsehair crest, grey mail shirt, red tunic, brown strip skirt, "
                "short sword at the left hip, brown sandals",
        "tunic": (196, 48, 44), "mail": (150, 156, 164), "skirt": (122, 78, 44), "metal": (214, 168, 64),
        "crest": (30, 26, 26), "feet": (110, 70, 40), "hem": 23, "flare": 19,
    },
    "citizen": {
        "label": "Roman townsman", "era": "Roman",
        "card": "Short brown hair, knee-length cream tunic with a rope belt, a rolled scroll, brown sandals",
        "tunic": (238, 226, 196), "hair": (92, 60, 36), "belt": (150, 110, 64), "feet": (110, 70, 40),
        "hem": 26, "flare": 21,
    },
    "student": {
        "label": "Edo-period student", "era": "Edo Japan",
        "card": "Black hair tied in a small top knot, indigo kimono top with a white collar, wide grey trousers "
                "to the ankle, a cloth-wrapped book bundle, pale split-toe socks",
        "tunic": (46, 62, 108), "collar": (244, 242, 236), "trousers": (124, 124, 132), "hair": (26, 24, 26),
        "feet": (236, 232, 222), "bundle": (176, 72, 60), "hem": 4, "flare": 16,
    },
    "attendant": {
        "label": "Egyptian temple attendant", "era": "Ancient Egypt",
        "card": "Straight black bob with a fringe, broad blue-and-gold bead collar, white linen kilt to the knee, "
                "bare stick legs, reed sandals",
        "tunic": (250, 248, 240), "hair": (20, 20, 24), "collar_a": (52, 112, 170), "collar_b": (222, 176, 60),
        "feet": (190, 160, 96), "hem": 22, "flare": 20,
    },
}


def darker(c, k=0.78):
    return tuple(round(v * k) for v in c)


def lighter(c, k=0.35):
    return tuple(round(v + (255 - v) * k) for v in c)


# ---------------------------------------------------------------- cel-shaded drawing on masks
class Cel(rig.Pen):
    """Draws flat shapes with a cel shadow band on their lower/back edge and an optional highlight band."""

    def _mask(self, pts=None, circle=None):
        m = Image.new("L", self.img.size, 0)
        dm = ImageDraw.Draw(m)
        if pts:
            dm.polygon([(x * SS, y * SS) for x, y in pts], fill=255)
        if circle:
            (cx, cy), r = circle
            dm.ellipse([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS], fill=255)
        return m

    def shape(self, pts, fill, shade=None, light=None, w=LINE, s=1.0, offset=(-3.2, -2.2), circle=None, outline=True):
        m = self._mask(pts, circle)
        self.img.paste(fill, (0, 0), m)
        for col, off in ((shade, offset), (light, (-offset[0] * 0.55, -offset[1] * 0.55))):
            if col is None:
                continue
            moved = ImageChops.offset(m, round(off[0] * s * SS), round(off[1] * s * SS))
            band = ImageChops.subtract(m, moved)
            if col is light:  # highlights are a thin band only
                band = ImageChops.subtract(band, ImageChops.offset(m, round(off[0] * 0.4 * s * SS), round(off[1] * 0.4 * s * SS)))
            self.img.paste(col, (0, 0), band)
        if outline:
            if circle:
                (cx, cy), r = circle
                self.d.ellipse([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS], outline=INK, width=round(w * s * SS))
            else:
                p = [(x * SS, y * SS) for x, y in pts]
                self.d.line(p + [p[0]], fill=INK, width=round(w * s * SS), joint="curve")

    def dot(self, c, r, fill):
        x, y = c[0] * SS, c[1] * SS
        self.d.ellipse([x - r * SS, y - r * SS, x + r * SS, y + r * SS], fill=fill)


# ---------------------------------------------------------------- body parts
def ring(cx, cy, rx, ry, a0, a1, n=24):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def hakama_front(cel, j, s, c):
    """Front view: the wide pleated trousers read as one flared shape with a split from the knees down."""
    hr, hl, ar, al = j["hip_r"], j["hip_l"], j["ankle_r"], j["ankle_l"]
    top = lerp(hr, hl, 0.5)
    pts = [add(hr, (-9.5 * s, -2 * s)), add(ar, (-11 * s, 0)), add(lerp(ar, al, 0.5), (0, -1.5 * s)), add(al, (11 * s, 0)),
           add(hl, (9.5 * s, -2 * s))]
    cel.shape(pts, c["trousers"], darker(c["trousers"]), s=s)
    split = [lerp(top, lerp(ar, al, 0.5), 0.45), add(lerp(ar, al, 0.5), (0, -1.5 * s))]
    cel.line(split, INK, 1.6 * s)
    for k, sg in (("r", -1), ("l", 1)):  # two pleats per leg
        for off in (3.5, 7.5):
            cel.line([add(j[f"hip_{k}"], (sg * off * 0.6 * s, 2 * s)), add(j[f"ankle_{k}"], (sg * off * s, -2 * s))],
                     darker(c["trousers"], 0.7), 0.9 * s)


def draw_leg(cel, j, k, s, c, view="right"):
    hip, knee, an, toe = j[f"hip_{k}"], j[f"knee_{k}"], j[f"ankle_{k}"], j[f"toe_{k}"]
    if "trousers" in c and view == "front":
        pass  # drawn by hakama_front over both legs
    elif "trousers" in c:  # wide trousers to the ankle, one flared tube per leg
        ux, px = axis(hip, an)
        pts = [add(hip, px, 6.5 * s), add(lerp(hip, an, 0.5), px, 8.5 * s), add(an, px, 10 * s),
               add(an, px, -10 * s), add(lerp(hip, an, 0.5), px, -8.5 * s), add(hip, px, -6.5 * s)]
        cel.shape(pts, c["trousers"], darker(c["trousers"]), s=s)
        cel.line([add(lerp(hip, an, 0.2), px, 2 * s), add(an, px, 3 * s)], darker(c["trousers"], 0.7), 0.9 * s)
    else:
        cel.line([hip, knee, an], INK, LIMB * s)
    heel = lerp(toe, an, 1.3)
    cel.line([heel, toe], INK, (4.2 + 1.4) * s)
    cel.line([heel, toe], c["feet"], 4.2 * s)


def draw_arm(cel, j, k, s, c, prop=None):
    sh, el, wr = j[f"shoulder_{k}"], j[f"elbow_{k}"], j[f"wrist_{k}"]
    cel.line([sh, el, wr], INK, LIMB * s)
    if "mail" in c or "collar" in c:  # short tunic sleeve (soldier) or kimono sleeve (student) over the upper arm
        ux, px = axis(sh, el)
        top = add(sh, ux, -2.5 * s); end = lerp(sh, el, 0.42 if "mail" in c else 0.8)
        wd = 5.0 if "mail" in c else 7.5
        sl = [add(top, px, 4 * s), add(end, px, wd * s), add(end, px, -wd * s), add(top, px, -4 * s)]
        col = c["tunic"]
        cel.shape(chaikin(sl, 1), col, darker(col, 0.75), s=s, w=1.8)
    if prop:
        draw_prop(cel, prop, wr, el, s, c)
    ux, _ = axis(el, wr)
    cel.dot(add(wr, ux, 1.8 * s), 3.3 * s, INK)  # small round black hand


def draw_prop(cel, prop, wr, el, s, c):
    ux, px = axis(el, wr)
    if prop == "scroll":
        a, b = add(wr, px, 7 * s), add(wr, px, -7 * s)
        cel.line([a, b], INK, 6.4 * s)
        cel.line([a, b], (240, 228, 190), 4.4 * s)
    elif prop == "bundle":
        p = add(wr, ux, 4 * s)
        box = [add(add(p, ux, -5 * s), px, -6 * s), add(add(p, ux, 5 * s), px, -6 * s),
               add(add(p, ux, 5 * s), px, 6 * s), add(add(p, ux, -5 * s), px, 6 * s)]
        cel.shape(box, c["bundle"], darker(c["bundle"]), s=s, w=1.6)


def body_shape(neck, pelvis, s, half_top, half_hem, hem):
    ux, px = axis(neck, pelvis)
    top = add(neck, ux, 1 * s); sh = add(neck, ux, 5 * s); bot = add(pelvis, ux, hem * s)
    pts = [add(top, px, half_top * 0.45 * s), add(sh, px, half_top * s), add(lerp(sh, bot, 0.5), px, (half_top + half_hem) * 0.5 * s),
           add(bot, px, half_hem * s), add(bot, px, -half_hem * s), add(lerp(sh, bot, 0.5), px, -(half_top + half_hem) * 0.5 * s),
           add(sh, px, -half_top * s), add(top, px, -half_top * 0.45 * s)]
    return chaikin(pts, 1), ux, px, top, bot


def draw_body(cel, j, s, view, key):
    c = CAST[key]
    side = view in ("right", "left")
    neck, pelvis = j["neck"], j["pelvis"]
    ht, hh = (9.5, c["flare"] * 0.7) if side else (13.0, c["flare"])
    cel.line([neck, lerp(neck, j["head"], 0.5)], INK, LIMB * s)
    if key == "soldier":
        body, ux, px, top, bot = body_shape(neck, pelvis, s, ht, hh, c["hem"])
        cel.shape(body, c["tunic"], darker(c["tunic"]), s=s)
        # strip skirt from the belt down, over the tunic
        n = 4 if side else 6
        belt = add(pelvis, ux, -3 * s)
        for i in range(n):
            t0 = -1 + 2 * i / n; t1 = -1 + 2 * (i + 0.86) / n
            wbelt, whem = hh * 0.86, hh * 0.92
            strip = [add(belt, px, t0 * wbelt * s), add(belt, px, t1 * wbelt * s),
                     add(add(pelvis, ux, (c["hem"] - 10) * s), px, t1 * whem * s), add(add(pelvis, ux, (c["hem"] - 10) * s), px, t0 * whem * s)]
            cel.shape(strip, c["skirt"], darker(c["skirt"]), s=s, w=1.4)
        # mail shirt over the chest, with ring rows
        mail, _, _, mt, mb = body_shape(neck, pelvis, s, ht + 0.6, hh * 0.86, -2.5)
        cel.shape(mail, c["mail"], darker(c["mail"]), lighter(c["mail"]), s=s)
        for r in range(1, 6):
            q = lerp(mt, mb, r / 6.2)
            half = (ht + (hh * 0.86 - ht) * r / 6) * 0.82
            for i in range(-3, 4):
                cel.dot(add(q, px, i * half / 3.6 * s), 0.7 * s, darker(c["mail"], 0.62))
        bl = [add(belt, px, (hh * 0.9) * s), add(belt, px, -(hh * 0.9) * s)]
        cel.line(bl, INK, 4.4 * s); cel.line(bl, c["skirt"], 2.8 * s)
        # short sword on the own left hip (screen right in front view, behind the body in side view facing right)
        if not side:
            hilt = add(add(pelvis, ux, -2 * s), px, -(hh * 0.95) * s)
            blade = [add(hilt, ux, 1 * s), add(hilt, ux, 13 * s)]
            cel.line(blade, INK, 4.6 * s); cel.line(blade, (130, 84, 46), 3.0 * s)
            cel.dot(hilt, 2.4 * s, c["metal"])
    elif key == "citizen":
        body, ux, px, top, bot = body_shape(neck, pelvis, s, ht, hh, c["hem"])
        cel.shape(body, c["tunic"], darker(c["tunic"], 0.86), s=s)
        for i in (-1, 1):  # soft drape folds
            cel.line([add(add(top, ux, 9 * s), px, i * 4 * s), add(add(bot, ux, -4 * s), px, i * 7 * s)], darker(c["tunic"], 0.8), 1.0 * s)
        belt = add(pelvis, ux, -3 * s)
        bl = [add(belt, px, (hh * 0.84) * s), add(belt, px, -(hh * 0.84) * s)]
        cel.line(bl, INK, 3.4 * s); cel.line(bl, c["belt"], 2.0 * s)
    elif key == "student":
        body, ux, px, top, bot = body_shape(neck, pelvis, s, ht, hh, c["hem"])
        cel.shape(body, c["tunic"], darker(c["tunic"], 0.72), s=s)
        # white V collar crossing left over right
        if side:
            f = 1 if view == "right" else -1
            v = [add(top, px, 0), add(add(top, ux, 3 * s), px, 2 * s * f * (1 if px[0] > 0 else -1)), add(add(top, ux, 14 * s), px, 0)]
            cel.line(v, INK, 4.2 * s); cel.line(v, c["collar"], 2.6 * s)
        else:
            for side_k, end in ((1, 18), (-1, 12)):
                v = [add(top, px, side_k * 5.5 * s), add(add(top, ux, end * s), px, -side_k * 3 * s)]
                cel.line(v, INK, 4.4 * s); cel.line(v, c["collar"], 2.8 * s)
        belt = add(pelvis, ux, -2 * s)
        bl = [add(belt, px, hh * 0.92 * s), add(belt, px, -hh * 0.92 * s)]
        cel.line(bl, INK, 4.6 * s); cel.line(bl, darker(c["trousers"], 0.75), 3.0 * s)
    elif key == "attendant":
        # kilt from the waist to the knee, and a white linen top under the bead collar
        kilt, ux, px, top, bot = body_shape(add(pelvis, axis(neck, pelvis)[0], -16 * s), pelvis, s, hh * 0.8, hh, c["hem"])
        cel.shape(kilt, c["tunic"], (214, 210, 196), s=s)
        for i in (-2, -1, 0, 1, 2):  # pleats
            cel.line([add(add(pelvis, ux, -2 * s), px, i * 3 * s), add(add(pelvis, ux, (c["hem"] - 3) * s), px, i * 4.2 * s)], (206, 200, 186), 0.9 * s)
        topb, ux, px, tt, tb = body_shape(neck, pelvis, s, ht, ht + 2, -6)
        cel.shape(topb, c["tunic"], (214, 210, 196), s=s)
        # broad collar: three bead bands round the neck
        ctr = add(neck, ux, 1.5 * s)
        ang = math.degrees(math.atan2(ux[1], ux[0]))
        for r, col in ((13.5, c["collar_b"]), (10.5, c["collar_a"]), (7.5, c["collar_b"])):
            rx = r * (0.62 if side else 1.0)
            pts = [add(ctr, rot((rx * s * math.cos(math.radians(a)), r * 0.78 * s * math.sin(math.radians(a))), ang - 90))
                   for a in range(0, 181, 12)]
            cel.line(pts, INK, 4.6 * s); cel.line(pts, col, 3.0 * s)


# ---------------------------------------------------------------- head, face and headwear
def eye(cel, x, y, s, expr, k=1.0):
    """Simple solid black ovals; a blink is a short arc and never redesigns the eye."""
    if expr == "blink":
        cel.arc([x - 2.6 * k * s, y - 2 * s, x + 2.6 * k * s, y + 2 * s], 20, 160, INK, 1.4 * s)
        return
    big = 1.15 if expr == "surprised" else 1.0
    rx, ry = 2.0 * k * big * s, 3.0 * big * s
    cel.d.ellipse([(x - rx) * SS, (y - ry) * SS, (x + rx) * SS, (y + ry) * SS], fill=INK)


def face(cel, cx, cy, r, s, view, expr):
    if view == "front":
        xs = (cx - 7.5 * s, cx + 7.5 * s); mx = cx
    else:
        sgn = 1 if view == "right" else -1
        xs = (cx + sgn * r * 0.08, cx + sgn * r * 0.6); mx = cx + sgn * r * 0.38
    ey = cy + 0.5 * s
    for i, x in enumerate(xs):
        eye(cel, x, ey, s, expr, 1.0 if (view == "front" or i == 0) else 0.8)
    rig.brows(cel, cx, cy + 1.2 * s, r, s, "smile" if expr == "blink" else expr, xs)
    m = {"blink": "smile", "angry": "determined"}.get(expr, expr)
    rig.mouth(cel, mx, cy + 10.5 * s, s, m, 0 if view == "front" else (1 if view == "right" else -1))


def draw_head(cel, j, s, view, key, expr="smile"):
    c = CAST[key]
    cx, cy = j["head"]; r = HEAD_R * s
    sgn = 0 if view in ("front", "back") else (1 if view == "right" else -1)
    # behind the head: crest tail, top knot, bob
    if key == "student":
        knot = (cx - sgn * r * 0.15, cy - r * 1.08)
        cel.shape(None, c["hair"], circle=(knot, 5.2 * s), s=s, w=1.4)
    if key == "attendant":
        bob = [(cx - r * 1.1, cy - r * 0.2), (cx - r * 1.08, cy + r * 0.62), (cx + r * 1.08, cy + r * 0.62), (cx + r * 1.1, cy - r * 0.2)]
        bob = ring(cx, cy - r * 0.05, r * 1.12, r * 1.08, 180, 360) + bob[::-1][:0] + [(cx + r * 1.08, cy + r * 0.62), (cx - r * 1.08, cy + r * 0.62)]
        cel.shape(chaikin(bob, 1), c["hair"], s=s, w=1.6)
    cel.shape(None, WHITE, (226, 226, 230), s=s, circle=((cx, cy), r), w=LINE)
    if key == "soldier":
        dome = ring(cx, cy, r * 1.06, r * 1.06, 180, 360) + [(cx + r * 1.06, cy - r * 0.18), (cx - r * 1.06, cy - r * 0.18)]
        cel.shape(dome, c["metal"], darker(c["metal"]), lighter(c["metal"], 0.55), s=s)
        brim = [(cx - r * 1.16, cy - r * 0.28), (cx + r * 1.16, cy - r * 0.28), (cx + r * 1.12, cy - r * 0.12), (cx - r * 1.12, cy - r * 0.12)]
        cel.shape(brim, c["metal"], darker(c["metal"]), s=s, w=1.6)
        # cheek guard on the near side, behind the eyes
        for side_k in ((1, -1) if view == "front" else (-sgn,)):
            g = [(cx + side_k * r * 1.02, cy - r * 0.15), (cx + side_k * r * 0.98, cy + r * 0.5),
                 (cx + side_k * r * 0.72, cy + r * 0.42), (cx + side_k * r * 0.76, cy - r * 0.15)]
            cel.shape(g, c["metal"], darker(c["metal"]), s=s, w=1.6)
        if view != "front":  # horsehair crest seen from the side: a raised arc from brow to nape
            outer = ring(cx - sgn * r * 0.1, cy - r * 0.1, r * 1.0, r * 1.4, 215, 330)
            inner = ring(cx - sgn * r * 0.1, cy - r * 0.1, r * 0.9, r * 1.0, 330, 215)
            cel.shape(chaikin(outer + inner, 1), c["crest"], s=s, w=1.4)
        if view == "front":
            crest = [(cx - r * 0.2, cy - r * 1.02), (cx - r * 0.24, cy - r * 1.62), (cx, cy - r * 1.78),
                     (cx + r * 0.24, cy - r * 1.62), (cx + r * 0.2, cy - r * 1.02)]
            cel.shape(chaikin(crest, 1), c["crest"], s=s, w=1.4)
    elif key in ("citizen", "student"):
        hl = cy - r * 0.42
        if view == "front":
            cap = ring(cx, cy, r * 1.04, r * 1.04, 192, 348) + [(cx + r * 0.7, hl), (cx, hl - r * 0.12), (cx - r * 0.7, hl)]
        else:
            cap = ring(cx, cy, r * 1.04, r * 1.04, 150, 335) if sgn == 1 else ring(cx, cy, r * 1.04, r * 1.04, 205, 390)
            cap += ([(cx + sgn * r * 0.4, hl), (cx - sgn * r * 0.5, cy - r * 0.1), (cx - sgn * r * 0.85, cy + r * 0.4)] if sgn == 1
                    else [(cx - sgn * r * 0.85, cy + r * 0.4), (cx - sgn * r * 0.5, cy - r * 0.1), (cx + sgn * r * 0.4, hl)][::-1])
        cel.shape(chaikin(cap, 1), c["hair"], darker(c["hair"], 0.7), s=s, w=1.6)
    elif key == "attendant":
        if view == "front":
            fringe = ring(cx, cy, r * 1.06, r * 1.06, 185, 355) + [(cx + r * 0.95, cy - r * 0.3), (cx - r * 0.95, cy - r * 0.3)]
        else:
            fringe = (ring(cx, cy, r * 1.06, r * 1.06, 160, 330) + [(cx + r * 0.85, cy - r * 0.3), (cx - r * 0.6, cy - r * 0.2)]
                      if sgn == 1 else ring(cx, cy, r * 1.06, r * 1.06, 210, 380) + [(cx + r * 0.6, cy - r * 0.2), (cx - r * 0.85, cy - r * 0.3)])
        cel.shape(fringe, c["hair"], s=s, w=1.6)
    face(cel, cx, cy, r, s, view, expr)


def draw_figure(img, j, view, key, s=1.0, expr="smile", holds=None):
    """view: front | right | left. holds: {'r': 'scroll'}. Own right arm is near the camera when facing right."""
    cel = Cel(img)
    holds = holds or {}
    c = CAST[key]
    if view in ("right", "left"):
        near = "r" if view == "right" else "l"; far = "l" if near == "r" else "r"
        draw_arm(cel, j, far, s, c, holds.get(far))
        if key == "soldier":  # sword on the own left hip: behind the body when facing right
            ux, px = axis(j["neck"], j["pelvis"])
            hilt = add(add(j["pelvis"], ux, -3 * s), (1 if view == "right" else -1, 0), -6 * s)
            blade = [hilt, add(hilt, (-(1 if view == "right" else -1) * 0.5, 0.86), 15 * s)]
            cel.line(blade, INK, 4.6 * s); cel.line(blade, (130, 84, 46), 3.0 * s); cel.dot(hilt, 2.4 * s, c["metal"])
        draw_leg(cel, j, far, s, c); draw_leg(cel, j, near, s, c)
        draw_body(cel, j, s, view, key)
        draw_head(cel, j, s, view, key, expr)
        draw_arm(cel, j, near, s, c, holds.get(near))
    else:
        for k in ("l", "r"):
            draw_leg(cel, j, k, s, c, "front")
        if "trousers" in c:
            hakama_front(cel, j, s, c)
        draw_body(cel, j, s, view, key)
        draw_head(cel, j, s, view, key, expr)
        for k in ("l", "r"):
            draw_arm(cel, j, k, s, c, holds.get(k))


# ---------------------------------------------------------------- painterly backgrounds
def soft(img, r=2.2):
    return img.filter(ImageFilter.GaussianBlur(r * SS))


def sky(w, h, top, bottom):
    img = Image.new("RGB", (w * SS, h * SS))
    d = ImageDraw.Draw(img)
    for y in range(h * SS):
        t = y / (h * SS)
        d.line([(0, y), (w * SS, y)], fill=tuple(round(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return img


def blobs(img, rnd, n, box, col, rmin, rmax, alpha=150):
    mask = Image.new("L", img.size, 0)
    d = ImageDraw.Draw(mask)
    for _ in range(n):
        x = rnd.uniform(box[0], box[2]); y = rnd.uniform(box[1], box[3]); r = rnd.uniform(rmin, rmax)
        d.ellipse([(x - r * 1.6) * SS, (y - r) * SS, (x + r * 1.6) * SS, (y + r) * SS], fill=alpha)
    img.paste(col, (0, 0), soft(mask, 1.6))


def hill(img, pts, col, edge=None, blur=1.2):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).polygon([(x * SS, y * SS) for x, y in pts], fill=255)
    img.paste(col, (0, 0), soft(mask, blur))
    if edge:
        ImageDraw.Draw(img).line([(x * SS, y * SS) for x, y in pts[1:-1]], fill=edge, width=round(1.6 * SS))


def wave_line(x0, x1, base, amp, freq, phase, step=8):
    return [(x, base - amp * math.sin(freq * x + phase) - amp * 0.4 * math.sin(2.3 * freq * x + phase * 1.7))
            for x in range(int(x0), int(x1) + step, step)]


def cypress(d, x, ground, h, s=1.0):
    pts = [(x, ground - h)] + [(x + 7 * s * math.sin(math.pi * t) ** 0.7, ground - h + h * t) for t in (0.2, 0.45, 0.7, 0.95)] + \
          [(x - 7 * s * math.sin(math.pi * t) ** 0.7, ground - h + h * t) for t in (0.95, 0.7, 0.45, 0.2)]
    d.polygon([(px * SS, py * SS) for px, py in pts], fill=(48, 88, 56), outline=INK, width=round(1.4 * SS))
    d.line([(x * SS, (ground - h * 0.9) * SS), ((x + 2) * SS, (ground - 4) * SS)], fill=(36, 70, 44), width=round(1.4 * SS))


def roman_bg(w, h, ground):
    rnd = random.Random(5)
    img = sky(w, h, (120, 176, 222), (214, 232, 240))
    blobs(img, rnd, 9, (0, 20, w, 100), (255, 255, 255), 10, 24, 170)
    hill(img, [(0, ground)] + wave_line(0, w, ground - 70, 16, 0.012, 0.6) + [(w, ground)], (150, 178, 120), None, 2.0)
    hill(img, [(0, ground)] + wave_line(0, w, ground - 38, 12, 0.02, 2.0) + [(w, ground)], (112, 158, 82), (70, 110, 56), 1.0)
    d = ImageDraw.Draw(img)
    # distant villa: tan walls and a red tile roof
    vx, vy = 470, ground - 64
    d.rectangle([vx * SS, vy * SS, (vx + 54) * SS, (vy + 20) * SS], fill=(222, 196, 150), outline=INK, width=round(1.2 * SS))
    d.polygon([((vx - 5) * SS, vy * SS), ((vx + 27) * SS, (vy - 12) * SS), ((vx + 59) * SS, vy * SS)], fill=(178, 76, 52),
              outline=INK, width=round(1.2 * SS))
    for i in range(3):
        d.rectangle([(vx + 8 + i * 16) * SS, (vy + 6) * SS, (vx + 13 + i * 16) * SS, (vy + 14) * SS], fill=(90, 66, 44))
    for x, hh in ((60, 70), (82, 54), (420, 58), (600, 76), (622, 52)):
        cypress(d, x, ground - 30, hh)
    # dusty road and grass verge
    d.rectangle([0, (ground - 14) * SS, w * SS, h * SS], fill=(128, 164, 86))
    road = [(0, ground - 8), (w, ground - 8), (w, ground + 16), (0, ground + 16)]
    d.polygon([(x * SS, y * SS) for x, y in road], fill=(214, 186, 136))
    blobs(img, rnd, 30, (0, ground - 6, w, ground + 14), (196, 164, 112), 2, 5, 130)
    d = ImageDraw.Draw(img)
    d.line([(0, (ground - 8) * SS), (w * SS, (ground - 8) * SS)], fill=(150, 122, 82), width=round(1.4 * SS))
    d.rectangle([0, (ground + 16) * SS, w * SS, h * SS], fill=(104, 146, 70))
    blobs(img, rnd, 40, (0, ground + 18, w, h), (80, 124, 56), 3, 7, 120)
    return img


def edo_bg(w, h, ground):
    rnd = random.Random(9)
    img = sky(w, h, (244, 196, 150), (250, 232, 206))
    blobs(img, rnd, 6, (0, 20, w, 90), (255, 244, 230), 12, 26, 160)
    # a far mountain with a pale cap
    hill(img, [(80, ground - 40), (250, ground - 196), (420, ground - 40)], (150, 140, 170), None, 1.6)
    hill(img, [(214, ground - 152), (250, ground - 196), (288, ground - 150), (262, ground - 160), (240, ground - 148)],
         (246, 242, 240), None, 0.8)
    hill(img, [(0, ground)] + wave_line(0, w, ground - 44, 10, 0.016, 1.0) + [(w, ground)], (122, 150, 96), (82, 108, 66), 1.0)
    d = ImageDraw.Draw(img)
    # wooden town house: dark tiled roof, plaster wall, timber frame, paper sliding doors
    hx, hy, hw, hh = 400, ground - 120, 210, 104
    d.rectangle([hx * SS, hy * SS, (hx + hw) * SS, (hy + hh) * SS], fill=(240, 228, 204), outline=INK, width=round(1.6 * SS))
    for i in range(1, 5):
        x = hx + i * hw / 5
        d.line([(x * SS, hy * SS), (x * SS, (hy + hh) * SS)], fill=(110, 72, 44), width=round(3 * SS))
    for i in range(4):
        x0 = hx + 8 + i * hw / 5 + hw / 5
        if i == 3:
            continue
        for gx in range(3):
            for gy in range(4):
                d.rectangle([(x0 - hw / 5 + 6 + gx * 10) * SS, (hy + 40 + gy * 14) * SS, (x0 - hw / 5 + 14 + gx * 10) * SS,
                             (hy + 52 + gy * 14) * SS], outline=(196, 170, 130), width=SS)
    d.line([(hx * SS, (hy + 30) * SS), ((hx + hw) * SS, (hy + 30) * SS)], fill=(110, 72, 44), width=round(3 * SS))
    roof = [(hx - 26, hy + 4), (hx + 20, hy - 34), (hx + hw - 20, hy - 34), (hx + hw + 26, hy + 4)]
    d.polygon([(x * SS, y * SS) for x, y in roof], fill=(70, 74, 86), outline=INK, width=round(1.8 * SS))
    for i in range(1, 14):
        x = hx - 20 + i * (hw + 40) / 14
        d.line([(x * SS, (hy - 30) * SS), ((x + (x - hx - hw / 2) * 0.12) * SS, (hy + 2) * SS)], fill=(56, 60, 70), width=round(1.2 * SS))
    # blossom tree on the left
    for pts, wdt in ((((98, ground), (104, ground - 64), (78, ground - 112)), 11), (((104, ground - 64), (146, ground - 104)), 8),
                     (((101, ground - 40), (70, ground - 70)), 6)):
        q = [(x * SS, y * SS) for x, y in pts]
        d.line(q, fill=INK, width=round((wdt + 3) * SS), joint="curve")
        d.line(q, fill=(96, 64, 46), width=round(wdt * SS), joint="curve")
    blobs(img, rnd, 34, (36, ground - 160, 186, ground - 84), (232, 150, 176), 7, 15, 255)
    blobs(img, rnd, 22, (46, ground - 150, 176, ground - 92), (248, 196, 212), 5, 10, 255)
    d = ImageDraw.Draw(img)
    # packed-earth street
    d.rectangle([0, (ground - 4) * SS, w * SS, h * SS], fill=(208, 182, 140))
    blobs(img, rnd, 34, (0, ground, w, h), (190, 160, 118), 3, 7, 120)
    ImageDraw.Draw(img).line([(0, (ground - 4) * SS), (w * SS, (ground - 4) * SS)], fill=(150, 122, 86), width=round(1.4 * SS))
    return img


def egypt_swatch(w, h, ground):
    """Small sheet backdrop for the Egypt card: sand, a pale sky and a distant pyramid."""
    img = sky(w, h, (236, 210, 160), (248, 236, 210))
    hill(img, [(w * 0.45, ground - 10), (w * 0.72, ground - 110), (w * 0.99, ground - 10)], (220, 184, 120), (170, 134, 80), 0.6)
    hill(img, [(0, ground)] + wave_line(0, w, ground - 12, 4, 0.03, 0.3) + [(w, ground)], (232, 200, 140), None, 0.8)
    ImageDraw.Draw(img).rectangle([0, ground * SS, w * SS, h * SS], fill=(226, 194, 136))
    return img


def shadow(img, x, y, w, s=1.0):
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([(x - w * s) * SS, (y - 4 * s) * SS, (x + w * s) * SS, (y + 4 * s) * SS], fill=(40, 30, 20, 52))


# ---------------------------------------------------------------- tracks
FIG = {"head_radius": HEAD_R, "limb_width": LIMB, "body_width": 34, "hand_length": 6}


def track(name, frames, rest, scale=1.0, **meta):
    fig = {k: round(v * scale, 2) for k, v in FIG.items()}
    return {"name": name, "source": "rig", "profile": "rig", "fps": 12, **fig, "rest": rest, **meta, "frames": frames}


def sheet_poses():
    """(label, cast, view, joints, frame extras, holds, expr), all at x=0, ground=0, scale 1."""
    out = []
    a = rig.stand_side(); a["shoulder_r"] = 88; a["elbow_r"] = 6; a["lean"] = 4
    out.append(("Point the way", "soldier", "right", rig.side_pose(a, 0, 0), {}, {}, "determined"))
    a = rig.stand_front(); a["abd_r"] = 125; a["elb_r"] = 60
    out.append(("Wave", "student", "front", rig.front_pose(a, 0, 0), {}, {}, "happy"))
    a = rig.stand_side(); a["shoulder_r"] = 52; a["elbow_r"] = 58
    j = rig.side_pose(a, 0, 0)
    out.append(("Read a scroll", "citizen", "right", j, {"holds": {"scroll": "r"}, "props": {"scroll": j["wrist_r"]}},
                {"r": "scroll"}, "thinking"))
    a = {"lean": 12, "neck": 2, "hip_r": 50, "knee_r": 75, "hip_l": -30, "knee_l": 75, "ankle_l": 10,
         "shoulder_r": -40, "elbow_r": 85, "shoulder_l": 45, "elbow_l": 80}
    out.append(("Run", "attendant", "right", rig.side_pose(a, 0, 0), {}, {}, "surprised"))
    a = {"abd_l": 150, "elb_l": 10, "abd_r": 150, "elb_r": 10, "leg_l": 14, "leg_r": 14}
    out.append(("Cheer jump", "citizen", "front", rig.front_pose(a, 0, 0, lift=16), {"airborne": True}, {}, "happy"))
    a = rig.stand_side(); a["shoulder_l"] = 40; a["elbow_l"] = 70
    j = rig.side_pose(a, 0, 0)
    out.append(("Carry books", "student", "right", j, {"holds": {"bundle": "l"}, "props": {"bundle": j["wrist_l"]}},
                {"l": "bundle"}, "smile"))
    return out


def walk_shot(n=36, s=1.0, x0=70.0, ground=300.0):
    frames = []
    for i in range(n):
        frames.append({"facing": "right", "joints": rig.side_pose(rig.walk(i / 12), x0 + i * 4.6 * s, ground, s)})
    for i in range(6):  # ease into a stand
        t = (i + 1) / 6; w = rig.walk(n / 12); st = rig.stand_side()
        a = {k: w.get(k, 0) * (1 - t) + st.get(k, 0) * t for k in set(w) | set(st)}
        frames.append({"facing": "right", "joints": rig.side_pose(a, x0 + (n + 1.2 * (i + 1) / 2) * 4.6 * s, ground, s)})
    # point down the road
    for i in range(14):
        t = 0.5 - 0.5 * math.cos(math.pi * min(1.0, i / 6)); st = rig.stand_side()
        a = dict(st); a["shoulder_r"] = st["shoulder_r"] + (88 - st["shoulder_r"]) * t; a["elbow_r"] = st["elbow_r"] * (1 - t) + 6 * t
        frames.append({"facing": "right", "joints": rig.side_pose(a, x0 + (n + 3.6) * 4.6 * s, ground, s), "_expr": "determined"})
    return frames


def wave_shot(s=1.0, x=290.0, ground=318.0):
    def ease(t): return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, t)))
    rest = rig.stand_front(); up = {"abd_r": 125, "elb_r": 75}
    frames = []
    for i in range(40):
        a = dict(rest); expr = "smile"
        if 4 <= i < 12:
            t = ease((i - 4) / 8)
            for k in up:
                a[k] = rest[k] + (up[k] - rest[k]) * t
        elif 12 <= i < 28:
            a.update(up); a["elb_r"] = up["elb_r"] - 8 + 16 * math.sin(2 * math.pi * (i - 12) / 7); expr = "happy"
        elif 28 <= i < 36:
            t = ease((i - 28) / 8)
            for k in up:
                a[k] = up[k] + (rest[k] - up[k]) * t
        if i in (34, 35):
            expr = "blink"
        frames.append({"facing": "front", "joints": rig.front_pose(a, x, ground, s), "_expr": expr})
    return frames


# ---------------------------------------------------------------- outputs
def make_gif(walk_frames, wave_frames, s_walk, s_wave, W=640, H=360):
    bg1, bg2 = roman_bg(W, H, 300), edo_bg(W, H, 322)
    out = []
    for f in walk_frames:
        img = bg1.copy(); j = f["joints"]
        shadow(img, j["pelvis"][0], max(j["toe_l"][1], j["toe_r"][1]) + 1, 24, s_walk)
        draw_figure(img, j, "right", "soldier", s_walk, f.get("_expr", "smile"))
        out.append(rig.finish(img))
    for f in wave_frames:
        img = bg2.copy(); j = f["joints"]
        shadow(img, j["pelvis"][0], max(j["toe_l"][1], j["toe_r"][1]) + 1, 30, s_wave)
        draw_figure(img, j, "front", "student", s_wave, f["_expr"])
        out.append(rig.finish(img))
    # one shared palette built from two halves: the two backgrounds, and crops around the character in every
    # fourth frame, so the few costume colours are not swamped by the sky
    bgs = Image.new("RGB", (W, H * 2)); bgs.paste(rig.finish(bg1), (0, 0)); bgs.paste(rig.finish(bg2), (0, H))
    figs = [f["joints"] for f in walk_frames + wave_frames]
    crops = []
    for o, j in list(zip(out, figs))[::4]:
        xs = [p[0] for p in j.values()]; ys = [p[1] for p in j.values()]
        crops.append(o.crop((int(min(xs)) - 40, int(min(ys)) - 50, int(max(xs)) + 40, int(max(ys)) + 10)).resize((120, 200)))
    sheet = Image.new("RGB", (120 * len(crops), 200))
    for i, cimg in enumerate(crops):
        sheet.paste(cimg, (120 * i, 0))
    p1 = bgs.quantize(colors=96, method=Image.Quantize.MEDIANCUT).getpalette()[:96 * 3]
    p2 = sheet.quantize(colors=160, method=Image.Quantize.MEDIANCUT).getpalette()[:160 * 3]
    ref = Image.new("P", (1, 1)); ref.putpalette(p1 + p2)
    pal = [o.quantize(palette=ref, dither=Image.Dither.NONE) for o in out]
    pal[0].save(HERE / "motion.gif", save_all=True, append_images=pal[1:], duration=83, loop=0, optimize=True, disposal=1)


def make_sheet(poses):
    W, H = 1600, 1290
    img = rig.canvas(W, H, (251, 248, 240))
    rig.text(img, (60, 52), "Style 5 Historical Cartoon: one drawing grammar, many eras", 34, True, anchor="lm")
    rig.text(img, (60, 92), "Code-rendered from a posture-gated rig. White round heads, solid black oval eyes, no nose, thin black stick "
             "limbs, thick outlines, cel shading. Only the era pack changes.", 17, anchor="lm", fill=(90, 80, 70))
    rig.text(img, (60, 145), "Era cast cards (front and side)", 22, True, anchor="lm")
    order = ["soldier", "citizen", "student", "attendant"]
    bgs = {"Roman": roman_bg(360, 330, 300), "Edo Japan": edo_bg(360, 330, 300), "Ancient Egypt": egypt_swatch(360, 330, 300)}
    for i, key in enumerate(order):
        c = CAST[key]
        x0, y0 = 60 + i * 380, 170
        bg = bgs[c["era"]].copy()
        img.paste(bg, (x0 * SS, y0 * SS))
        ImageDraw.Draw(img).rectangle([x0 * SS, y0 * SS, (x0 + 360) * SS, (y0 + 330) * SS], outline=INK, width=round(1.5 * SS))
        fj = rig.front_pose(rig.stand_front(), x0 + 105, y0 + 300, 1.45)
        sj = rig.side_pose(rig.stand_side(), x0 + 255, y0 + 300, 1.45)
        for j in (fj, sj):
            shadow(img, j["pelvis"][0], y0 + 301, 26, 1.45)
        holds = {"citizen": {"r": "scroll"}, "student": {"l": "bundle"}}.get(key, {})
        draw_figure(img, fj, "front", key, 1.45, holds=holds)
        draw_figure(img, sj, "right", key, 1.45, holds={k: v for k, v in holds.items() if k == "r"})
        rig.text(img, (x0 + 180, y0 + 352), f"{c['label']}", 19, True)
        words = c["card"].split(", ")
        for li, part in enumerate(words):
            rig.text(img, (x0 + 4, y0 + 380 + li * 21), "· " + part, 14, anchor="lm", fill=(70, 62, 54))
    # expressions, the soldier and the attendant
    rig.text(img, (60, 700), "Expressions (eyes stay solid ovals; a blink is a short arc)", 22, True, anchor="lm")
    exprs = ["smile", "happy", "surprised", "thinking", "determined", "sad", "blink"]
    for i, e in enumerate(exprs):
        x, y = 120 + i * 205, 800
        key = "soldier" if i % 2 == 0 else "attendant"
        draw_head(Cel(img), {"head": [x, y], "neck": [x, y + 60]}, 2.3, "front", key, e)
        rig.text(img, (x, y + 86), e.capitalize(), 16)
    rig.text(img, (60, 950), "Poses (each one gated)", 22, True, anchor="lm")
    for i, (lab, key, view, j, extra, holds, expr) in enumerate(poses):
        x, gy = 140 + i * 230, 1215
        jj = {k: [p[0] * 1.3 + x, p[1] * 1.3 + gy] for k, p in j.items()}
        shadow(img, x, gy + 2, 30, 1.3)
        draw_figure(img, jj, view, key, 1.3, expr=expr, holds=holds)
        rig.text(img, (x, gy + 34), lab, 17)
    rig.finish(img).save(HERE / "sheet.png", optimize=True)


def main():
    tracks = HERE / "tracks"; tracks.mkdir(exist_ok=True)
    poses = sheet_poses()
    for lab, key, view, j, extra, holds, expr in poses:
        name = "pose_" + lab.lower().replace(" ", "_").replace("-", "_")
        f = {"facing": view, "joints": j, **extra}
        if lab == "Run":
            f.pop("airborne", None)
        rest = rig.front_pose(rig.stand_front(), 0, 0) if view == "front" else rig.side_pose(rig.stand_side(), 0, 0)
        (tracks / f"{name}.json").write_text(json.dumps(track(name, [f], rest, cast=key), indent=1))
    s_walk, s_wave = 1.15, 1.35
    wf, vf = walk_shot(s=s_walk), wave_shot(s=s_wave)
    clean = lambda fr: [{k: v for k, v in f.items() if not k.startswith("_")} for f in fr]
    (tracks / "shot1_roman_walk.json").write_text(json.dumps(
        track("shot1_roman_walk", clean(wf), rig.side_pose(rig.stand_side(), 70, 300, s_walk), s_walk, cast="soldier"), indent=1))
    (tracks / "shot2_edo_wave.json").write_text(json.dumps(
        track("shot2_edo_wave", clean(vf), rig.front_pose(rig.stand_front(), 290, 318, s_wave), s_wave, cast="student"), indent=1))
    make_sheet(poses)
    make_gif(wf, vf, s_walk, s_wave)


if __name__ == "__main__":
    main()
