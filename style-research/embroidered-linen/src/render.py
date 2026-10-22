#!/usr/bin/env python3
"""Original stitched-linen motion study. Local Pillow drawing, no network/API.
All posture coordinates exported are the coordinates used by the drawing.
"""
import importlib.util
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('lead', ROOT / 'docs/lead-character/render.py')
rig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rig)
rig.LEN.update(torso=58, head=27, upper_arm=30, forearm=28, thigh=37, shin=37)
W, H, SS, FPS, N, SCALE = 960, 540, 2, 12, 120, 2.2
NAVY, OCHRE, CREAM, BROWN = (55, 76, 94), (171, 124, 50), (220, 202, 166), (84, 59, 40)


def pxy(p):
    return (round(p[0] * SS), round(p[1] * SS))


def shade(c, k):
    return tuple(max(0, min(255, int(v * k))) for v in c)


def rotate(p, centre, degrees):
    t = math.radians(degrees)
    x, y = p[0] - centre[0], p[1] - centre[1]
    return [centre[0] + x * math.cos(t) - y * math.sin(t), centre[1] + x * math.sin(t) + y * math.cos(t)]


def cord(im, points, color, width=2.0):
    """Thread body, shallow relief shadow and a narrow fibre highlight."""
    d = ImageDraw.Draw(im)
    p = [pxy(v) for v in points]
    d.line([(x + SS, y + SS) for x, y in p], fill=shade(color, .56), width=max(1, round(width * SS)), joint='curve')
    d.line(p, fill=color, width=max(1, round(width * SS)), joint='curve')
    d.line([(x, y - 1) for x, y in p], fill=shade(color, 1.24), width=max(1, SS // 2), joint='curve')


def seam(im, polygon, color):
    """Short edge stitches, with small inward blanket-stitch crossbars."""
    cx = sum(p[0] for p in polygon) / len(polygon)
    cy = sum(p[1] for p in polygon) / len(polygon)
    for a, b in zip(polygon, polygon[1:] + polygon[:1]):
        length = math.dist(a, b)
        for i in range(max(1, int(length / 7))):
            t = i / max(1, int(length / 7))
            u = min(1, t + 4 / max(length, 1))
            q = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            q2 = (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
            cord(im, [q, q2], color, 1.4)
            n = math.dist(q, (cx, cy)) or 1
            cord(im, [q, (q[0] + (cx - q[0]) / n * 3, q[1] + (cy - q[1]) / n * 3)], color, 1.0)


def satin(im, polygon, color, angle=0, border=True):
    """Parallel strand fill clipped to an original cloth silhouette."""
    pts = [pxy(p) for p in polygon]
    xs, ys = zip(*pts)
    x0, y0, x1, y1 = min(xs) - 2, min(ys) - 2, max(xs) + 3, max(ys) + 3
    size = (x1 - x0, y1 - y0)
    tile = Image.new('RGB', size, shade(color, .8))
    d = ImageDraw.Draw(tile)
    theta = math.radians(angle)
    vx, vy = math.cos(theta), math.sin(theta)
    nx, ny = -vy, vx
    radius = math.hypot(*size)
    cx, cy = size[0] / 2, size[1] / 2
    # Spacing is perpendicular to the strand, so vertical sleeves do not
    # collapse into a solid fill as the arm turns.
    for offset in range(-int(radius), int(radius) + 1, 6):
        mx, my = cx + nx * offset, cy + ny * offset
        q = [(mx - vx * radius, my - vy * radius), (mx + vx * radius, my + vy * radius)]
        d.line([(x+nx*2, yy+ny*2) for x,yy in q], fill=shade(color,.58), width=5)
        d.line(q,fill=color,width=4)
        d.line([(x-nx, yy-ny) for x,yy in q],fill=shade(color,1.23),width=1)
        for along in range(-int(radius), int(radius), 17):
            x, yy = mx + vx * along, my + vy * along
            d.line((x-nx, yy-ny, x+nx*2, yy+ny*2),fill=shade(color,1.06),width=1)
    mask = Image.new('L', size)
    ImageDraw.Draw(mask).polygon([(x - x0, y - y0) for x, y in pts], fill=255)
    im.paste(tile, (x0, y0), mask)
    if border:
        seam(im, polygon, shade(color, 1.35))


def ellipse(im, centre, rx, ry, color, angle=0, border=True):
    polygon = [rotate((centre[0] + rx * math.cos(i * math.pi / 24), centre[1] + ry * math.sin(i * math.pi / 24)), centre, angle) for i in range(48)]
    satin(im, polygon, color, angle, border)


def limb(im, a, b, radius, color):
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    nx, ny = -dy / length, dx / length
    polygon = [(a[0] + nx * radius, a[1] + ny * radius), (b[0] + nx * radius * .85, b[1] + ny * radius * .85), (b[0] - nx * radius * .85, b[1] - ny * radius * .85), (a[0] - nx * radius, a[1] - ny * radius)]
    # Transverse stitches bend with the limb, not a screen-space recoloured slab.
    satin(im, polygon, color, math.degrees(math.atan2(ny, nx)))


def background():
    im = Image.new('RGB', (W * SS, H * SS), (227, 215, 188))
    d = ImageDraw.Draw(im)
    for x in range(0, W * SS, 6):
        c = 8 + (x // 6 % 5)
        d.line((x, 0, x, H * SS), fill=(211 + c, 198 + c, 171 + c), width=2)
        d.line((x + 2, 0, x + 2, H * SS), fill=(239, 229, 205), width=1)
    for y in range(0, H * SS, 6):
        d.line((0, y, W * SS, y), fill=(219, 206, 179), width=1)
        for x in range((y // 6 % 2) * 6, W * SS, 12):
            d.line((x, y + 1, x + 5, y + 1), fill=(242, 231, 208), width=2)
    # A sparse stitched baseline, not a three-dimensional floor.
    for x in range(65, 900, 15):
        cord(im, [(x, 475), (x + 8, 475)], (172, 153, 113), 1.3)
    return im


def sprig(im):
    stem = [(728, 473), (726, 438), (735, 400), (727, 365)]
    cord(im, stem, (101, 112, 65), 2.3)
    for i, (x, y) in enumerate([(727, 445), (730, 422), (733, 400), (729, 381)]):
        side = -1 if i % 2 else 1
        end = (x + side * 30, y - 17)
        cord(im, [(x, y), end], (102, 111, 64), 1.6)
        ellipse(im, (end[0] - side * 6, end[1] + 2), 11, 4, (119, 127, 75), -side * 30)
        ellipse(im, (end[0] + side * 3, end[1] - 4), 5, 6, (220, 202, 151), 0)
    ellipse(im, (727, 361), 5, 7, (219, 201, 153))


def ease(x):
    return .5 - .5 * math.cos(math.pi * max(0, min(1, x)))


def pose(f):
    t = f / FPS
    a = rig.stand_front()
    a.update(abd_l=24, abd_r=24, elb_l=8, elb_r=8)
    if t < 2.5:
        u = ease(t / 2.5)
        lean = -4 * math.sin(u * math.pi)
        state = 'listen'
    elif t < 5.5:
        u = ease((t - 2.5) / 3)
        a.update(abd_l=24 + 39 * u, abd_r=24 + 49 * u, elb_l=8 + 14 * u, elb_r=8 + 14 * u)
        lean = 2 * math.sin(u * math.pi)
        state = 'open'
    elif t < 7:
        a.update(abd_l=63, abd_r=73, elb_l=22, elb_r=22)
        lean = 2 * math.sin((t - 5.5) / 1.5 * math.pi)
        state = 'welcome'
    elif t < 9:
        u = ease((t - 7) / 2)
        a.update(abd_l=63 - 39 * u, abd_r=73 - 49 * u, elb_l=22 - 14 * u, elb_r=22 - 14 * u)
        lean = -2 * math.sin(u * math.pi)
        state = 'lower'
    else:
        lean = 0
        state = 'rest'
    j = rig.front_pose(a, 365, 468, SCALE)
    for name in ['neck', 'head', 'shoulder_l', 'shoulder_r', 'elbow_l', 'elbow_r', 'wrist_l', 'wrist_r']:
        j[name] = rotate(j[name], j['pelvis'], lean)
    return j, state, lean


def character(im, j, lean, f):
    for k in ('l', 'r'):
        limb(im, j['hip_' + k], j['knee_' + k], 11, OCHRE)
        limb(im, j['knee_' + k], j['ankle_' + k], 10, OCHRE)
        ellipse(im, (j['ankle_' + k][0], j['ankle_' + k][1] + 2), 15, 7, BROWN)
    n, p = j['neck'], j['pelvis']
    body = [(n[0] - 25, n[1] + 3), (n[0] - 35, n[1] + 14), (p[0] - 41, p[1] + 21), (p[0] + 41, p[1] + 21), (n[0] + 35, n[1] + 14), (n[0] + 25, n[1] + 3)]
    satin(im, body, NAVY, lean + 9)
    for k in ('l', 'r'):
        limb(im, j['shoulder_' + k], j['elbow_' + k], 11, NAVY)
        limb(im, j['elbow_' + k], j['wrist_' + k], 9, NAVY)
        ellipse(im, j['wrist_' + k], 9, 11, CREAM, lean)
    # Own-right side marker is explicit, not inferred from the generated concept.
    wr = j['wrist_r']
    cord(im, [(wr[0] - 8, wr[1] - 5), (wr[0], wr[1] - 2), (wr[0] + 7, wr[1] - 5)], (174, 86, 40), 2.5)
    limb(im, j['neck'], j['head'], 8, CREAM)
    h = j['head']
    ellipse(im, h, 34, 42, CREAM, lean)
    # Swept strands follow a curved scalp. No rigid rectangular cap.
    hp = [(-34, -20), (-33, -37), (-20, -48), (3, -49), (25, -43), (34, -31), (17, -25), (3, -33), (-12, -24)]
    satin(im, [rotate((h[0]+x, h[1]+y), h, lean) for x,y in hp], BROWN, -22, False)
    for i in range(11):
        a = (h[0]-31+i*3.1, h[1]-22-i*.8)
        b = (h[0]-30+i*3.2, h[1]-51+i*.4)
        c = (h[0]+24+i*.5, h[1]-39+i*.7)
        curve = []
        for step in range(18):
            u=step/17
            q=((1-u)**2*a[0]+2*(1-u)*u*b[0]+u*u*c[0], (1-u)**2*a[1]+2*(1-u)*u*b[1]+u*u*c[1])
            curve.append(rotate(q,h,lean))
        cord(im,curve,BROWN,2.0)
    blink = f in (25, 26, 83, 84)
    for dx in (-11, 11):
        e = rotate((h[0] + dx, h[1] + 2), h, lean)
        if blink:
            cord(im, [(e[0] - 3, e[1]), (e[0] + 3, e[1])], BROWN, 1.7)
        else:
            ellipse(im, e, 2, 3, BROWN, 0, False)
    mouth = [rotate((h[0] - 9 + i * 1.5, h[1] + 15 + 4 * math.sin(i / 12 * math.pi)), h, lean) for i in range(13)]
    cord(im, mouth, BROWN, 1.4)


def main():
    (OUT / 'motion/frames').mkdir(parents=True, exist_ok=True)
    base = background()
    sprig(base)
    frames = []
    chosen = {0: 'start', 15: 'listen', 40: 'opening', 65: 'open', 75: 'welcome', 96: 'lower', 119: 'rest'}
    for f in range(N):
        j, state, lean = pose(f)
        im = base.copy()
        character(im, j, lean, f)
        im = im.resize((W, H), Image.Resampling.LANCZOS)
        im.save(OUT / f'motion/frames/{f:04}.png')
        frame = {'facing': 'front', 'joints': j}
        frames.append(frame)
        if f in chosen:
            im.save(OUT / f'gallery/{chosen[f]}.png')
    track = {'name': 'May', 'fps': FPS, 'profile': 'rig', 'head_radius': 51, 'body_width': 70, 'hip_width': 82, 'limb_width': 22, 'hand_length': 11, 'source': 'rig', 'rest': pose(0)[0], 'frames': frames}
    (OUT / 'motion/track.json').write_text(json.dumps(track, indent=2))
    for f, name in chosen.items():
        one = dict(track, name=name, frames=[frames[f]])
        (OUT / f'gallery/{name}.json').write_text(json.dumps(one, indent=2))
    print(f'Rendered {N} frames and {len(chosen)} state snapshots.')


if __name__ == '__main__':
    main()
