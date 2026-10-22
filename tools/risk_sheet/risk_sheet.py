#!/usr/bin/env python3
"""Contact sheet of the risky moments in a rendered clip, read from its own segment spec.

Animation gets hands and bodies wrong at predictable moments: a prop passing between hands,
a turn, a reach overhead, crossed arms, a fall. The segment spec already says when those happen.
This script reads one clip of a Phase B package, lists those moments with the hands the
ledger expects, and (given the rendered video) cuts a short burst of frames around each one
into a single PNG, so a person checks one sheet instead of scrubbing the whole clip.

    risk_sheet.py package.md --clip 2                       # print the plan (no video needed)
    risk_sheet.py package.md --clip 2 --video clip2.mp4 -o out/
    risk_sheet.py package.md --batch videos/ -o out/        # files named ...clip1.mp4, ...clip-2.mp4

Writes out/clipN-sheet.png and out/clipN-checklist.md (one row per moment, OK/FAIL to fill in).
Times come from "at about 1.5s" when the beat says so, otherwise they are spread across the
beat's window, so each burst covers +/- --window seconds (default 0.5) at --fps (default 8).
Needs ffmpeg/ffprobe for frames and Pillow for the sheet; the plan needs only the standard library.
This is a review aid, not a verdict: it does not detect errors, a person marks each row.
"""
import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "posture_gate"))
import hand_ledger as hl  # noqa: E402

BEAT = re.compile(r"^\W*\[(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)\s*s\]\s*(.*)$", re.M)
AT = re.compile(r"\bat (?:about|around|roughly)?\s*(\d+(?:\.\d+)?)\s*s\b", re.I)
KINDS = [
    ("hand pass", hl.TRANSFER),
    ("turn", re.compile(r"\b(turns?|turning|spins?|pivots?|faces? (?:left|right|away|the camera|back)|looks back|whirls?)\b", re.I)),
    ("overhead reach", re.compile(r"\b(overhead|above (?:his|her|their|its) head|raises? both|reaches? up|arms? up)\b", re.I)),
    ("crossed arms", re.compile(r"\b(cross(?:es|ed)? (?:his|her|their|its) arms|across (?:his|her|their|its) (?:body|chest|face)|covers? (?:his|her|their|its) (?:head|face))\b", re.I)),
    ("fall", re.compile(r"\b(trips?|falls?|rolls?|tumbles?|stumbles?|slips?|staggers?|jerks? \w+ back|crouch(?:es)?|kneels?|sits? down)\b", re.I)),
]
SUBJECT = re.compile(r"\b(he|she|they|him|her|them)\b", re.I)


def ledger_text(hands):
    if not hands:
        return "(no Hands line)"
    side = lambda v: v or "empty"  # noqa: E731
    return "; ".join(f"{n}: R {side(h['r'])}, L {side(h['l'])}" for n, h in hands.items())


def plan(text, clip):
    """Risky moments of one clip: [(time, kind, clause, expected hands)]."""
    text = hl.SPOKEN.sub('""', text)
    clips = dict(hl.split_clips(text)) or {1: text}
    if clip not in clips:
        raise SystemExit(f"Clip {clip} not found (have {sorted(clips)})")
    body = clips[clip]
    led = {k.lower(): hl.parse_ledger(hl.EXCUSE.sub("", v)) for k, _, v in hl.LINE.findall(body)}
    start, end = led.get("start", {}), led.get("end", {})
    beats = [(float(a), float(b), t) for a, b, t in BEAT.findall(body)]
    if not beats:
        raise SystemExit(f"Clip {clip} has no timed beats like [0–3s]")
    last = max(b for _, b, _ in beats)
    found = []
    for a, b, line in beats:
        clauses = [(c, s) for s in re.split(r"(?<=[.!?;])\s+", line) for c in hl.CLAUSE.split(s) if c.strip()]
        names = list({**start, **end})
        # only clauses about a character count: "the tangles roll" or "a clock spins" are not body moments
        named = lambda c: (SUBJECT.search(c) or not names  # noqa: E731
                           or any(re.search(rf"\b{re.escape(n)}\b", c) for n in names))
        # "A lets go of the cord and turns": a clause starting with a verb shares its sentence's subject
        about = lambda c, sent: named(c) or (named(sent) and re.match(r"[a-z]+s\b", c.strip()))  # noqa: E731
        # the character acts: its name or pronoun comes before the verb ("tangles roll in behind A" is not A rolling)
        def acts(c, rx):
            if not named(c):
                return True  # a verb-first clause; its subject is earlier in the sentence
            who = [m.start() for m in SUBJECT.finditer(c)] + [m.start() for n in names
                                                               for m in re.finditer(rf"\b{re.escape(n)}\b", c)]
            verb = rx.search(c)
            return bool(who and verb and min(who) < verb.start())
        hits = [(c, sent, [k for k, rx in KINDS if rx.search(c) and acts(c, rx)] if about(c, sent) else [])
                for c, sent in clauses]
        hits = [(c, sent, ks) for c, sent, ks in hits if ks]
        for i, (c, sent, ks) in enumerate(hits):
            m = AT.search(c) or AT.search(sent)
            t = float(m.group(1)) if m else a + (i + 0.5) * (b - a) / len(hits)
            found.append((round(min(max(t, a), b), 2), " + ".join(ks), c.strip(), ks))
    passes = [t for t, _, _, ks in found if "hand pass" in ks]
    moments = [(0.2, "start", "first frame", ledger_text(start))]
    for t, kind, clause, _ in sorted(found):
        if not passes or t < min(passes) or start == end:
            expect = ledger_text(start)
        elif t > max(passes):
            expect = ledger_text(end)
        else:
            moved = [n for n in {**start, **end} if start.get(n) != end.get(n)]
            expect = (f"changing: {ledger_text({n: start[n] for n in moved if n in start})} -> "
                      f"{ledger_text({n: end[n] for n in moved if n in end})}")
        moments.append((t, kind, clause, expect))
    moments.append((round(last - 0.2, 2), "end", "last frame", ledger_text(end)))
    return moments


def checklist(clip, moments, sheet=None):
    rows = [f"# Clip {clip}: risky moments", "",
            "Hands are the character's own: facing the camera, the right hand is on screen left.", ""]
    if sheet:
        rows += [f"![contact sheet]({sheet})", ""]
    rows += ["| Time | Moment | Beat | Expected hands | OK / FAIL | Note |", "|---|---|---|---|---|---|"]
    rows += [f"| {t:.1f}s | {k} | {c[:80]} | {e} |  |  |" for t, k, c, e in moments]
    rows += ["", "Also mark FAIL for: an extra or missing limb, a knee or elbow bending backward, a limb changing "
             "length, words on screen, or a character whose design changed."]
    return "\n".join(rows) + "\n"


def duration(video):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def grab(video, t, dest, width):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1",
                    "-vf", f"scale={width}:-2", str(dest)], check=True)


def sheet(video, moments, out_png, fps=8, window=0.5, width=240):
    from PIL import Image, ImageDraw, ImageFont
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 15)
        small = ImageFont.truetype("DejaVuSans.ttf", 12)
    except OSError:
        font = small = ImageFont.load_default()
    dur = duration(video)
    n = int(round(2 * window * fps)) + 1
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, (t, kind, clause, expect) in enumerate(moments):
            times = sorted({round(min(max(t - window + j / fps, 0), max(dur - 0.05, 0)), 3) for j in range(n)})
            frames = []
            for j, ft in enumerate(times):
                p = Path(tmp) / f"{i}_{j}.png"
                grab(video, ft, p, width)
                frames.append((ft, Image.open(p).convert("RGB")))
            rows.append((t, kind, clause, expect, frames))
        fh = max(f.height for r in rows for _, f in r[4])
        cols = max(len(r[4]) for r in rows)
        head, label, pad = 44, 18, 8
        W = pad + cols * (width + pad)
        H = sum(head + fh + label + pad for _ in rows) + pad
        img = Image.new("RGB", (W, H), (250, 250, 247))
        d = ImageDraw.Draw(img)
        y = pad
        for t, kind, clause, expect, frames in rows:
            d.text((pad, y), f"{t:.1f}s  {kind.upper()}  {clause[:110]}", fill=(29, 29, 27), font=font)
            d.text((pad, y + 22), f"expected hands: {expect}"[:160], fill=(47, 109, 179), font=small)
            y += head
            for k, (ft, f) in enumerate(frames):
                x = pad + k * (width + pad)
                img.paste(f, (x, y))
                if abs(ft - t) < 0.5 / fps:
                    d.rectangle([x - 2, y - 2, x + f.width + 1, y + f.height + 1], outline=(200, 55, 45), width=3)
                d.text((x, y + fh + 2), f"{ft:.2f}s", fill=(91, 91, 85), font=small)
            y += fh + label + pad
        img.save(out_png)
    return out_png


def run(package, clip, video, out, fps, window):
    moments = plan(Path(package).read_text(), clip)
    out.mkdir(parents=True, exist_ok=True)
    name = None
    if video:
        name = f"clip{clip}-sheet.png"
        sheet(video, moments, out / name, fps, window)
    (out / f"clip{clip}-checklist.md").write_text(checklist(clip, moments, name))
    return moments


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("package")
    ap.add_argument("--clip", type=int)
    ap.add_argument("--video")
    ap.add_argument("--batch", help="folder of clips named ...clip1.mp4, ...clip-2.mp4")
    ap.add_argument("-o", "--out", default="risk-sheets")
    ap.add_argument("--fps", type=float, default=8)
    ap.add_argument("--window", type=float, default=0.5)
    a = ap.parse_args(argv)
    out = Path(a.out)
    if a.batch:
        vids = sorted(p for p in Path(a.batch).iterdir() if p.suffix.lower() in (".mp4", ".mov", ".webm"))
        for v in vids:
            m = re.search(r"clip[\s_-]*(\d+)", v.stem, re.I)
            if not m:
                print(f"skip {v.name}: no clip number in the name", file=sys.stderr)
                continue
            run(a.package, int(m.group(1)), v, out / v.stem, a.fps, a.window)
            print(f"{v.name}: {out / v.stem}")
        return 0
    if a.clip is None:
        ap.error("--clip or --batch is required")
    moments = run(a.package, a.clip, a.video, out, a.fps, a.window)
    if not a.video:
        print(checklist(a.clip, moments))
    else:
        print(f"wrote {out}/clip{a.clip}-sheet.png and clip{a.clip}-checklist.md ({len(moments)} moments)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
