#!/usr/bin/env python3
"""Flow benchmark kit: the fixed set of hard clips to generate, and the review of what comes back.

    kit.py prompts  [-o prompts.md]          # copy-paste list: one prompt per clip, with the file name to save it as
    kit.py review   clips/ [-o review/]      # risk sheets for every downloaded clip + results.csv to fill in

The set is twelve clips from packages that already pass package_lint, chosen for the moments video
models get wrong: a prop passing between hands, turns, a fall, two or three characters in one frame.
Name each downloaded clip exactly as the prompt list says (for example paper-cutout-clip2.mp4).
"""
import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REFS = ROOT / "skills/directing-stickman-videos/references"
sys.path.insert(0, str(ROOT / "tools/risk_sheet"))
import risk_sheet  # noqa: E402

# (key, file, part of the file, clips, what it stresses)
SET = [
    ("style1-dark", "examples.md", "before:# Example 2:", [1, 4, 5],
     "Style 1 line figure: letting go of a cord and turning; a second figure trips and rolls; grabbing and dropping vines"),
    ("style2a", "examples.md", "after:# Example 2:", [1, 2, 3],
     "Style 2A beanie figure: leap into a glass ceiling; pen from the right pocket in the right hand; hand on a vault ring"),
    ("paper-cutout", "styles/samples/paper-cutout.md", "all", [1, 2, 3],
     "Paper cutout, three characters: balloon passed from one character's right hand to another's; sketchbook and pencil in two hands"),
    ("chibi-anime", "styles/samples/chibi-anime.md", "all", [1, 2, 3],
     "Chibi, short arms: several cast members in one frame, teddy-bear handoff"),
]
CHECKS = ["hands_match_sheet", "no_extra_or_missing_limbs", "joints_bend_the_right_way", "character_design_same_as_clip1",
          "no_words_on_screen", "hook_by_2s_clip1_only", "voice_same_as_clip1"]


def package(file, part):
    text = (REFS / file).read_text()
    if part.startswith("before:"):
        return text.split(part[7:], 1)[0]
    if part.startswith("after:"):
        return text.split(part[6:], 1)[1]
    return text


def clip_prompt(text, n):
    heads = list(re.finditer(r"^#{1,4}\s*Clip\s+(\d+)\b.*$", text, re.M))
    for i, h in enumerate(heads):
        if int(h.group(1)) == n:
            body = text[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
            return re.search(r"```text\n(.*?)\n```", body, re.S).group(1)
    raise KeyError(n)


def prompts_md():
    out = ["# Flow benchmark: 12 clips", "",
           "Settings for every clip: Omni Flash in Flow, 16:9, 720p, one output, no reference image. "
           "Paste one prompt per generation and save the clip with the file name shown.", ""]
    k = 0
    for key, file, part, clips, why in SET:
        text = package(file, part)
        out += [f"## {key}", "", why, ""]
        for n in clips:
            k += 1
            out += [f"### {k}. Save as `{key}-clip{n}.mp4`", "", "```text", clip_prompt(text, n), "```", ""]
    return "\n".join(out)


def review(clips_dir, out):
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for key, file, part, clips, _ in SET:
        text = package(file, part)
        tmp = out / f"{key}.package.md"
        tmp.write_text(text)
        for n in clips:
            video = next((p for p in Path(clips_dir).glob(f"{key}-clip{n}.*")), None)
            row = {"clip": f"{key}-clip{n}", "file": video.name if video else "MISSING", "sheet": ""}
            if video:
                risk_sheet.run(tmp, n, video, out / f"{key}-clip{n}", 8, 0.5)
                row["sheet"] = f"{key}-clip{n}/clip{n}-sheet.png"
            rows.append({**row, **{c: "" for c in CHECKS}, "notes": ""})
    with open(out / "results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["clip", "file", "sheet", *CHECKS, "notes"])
        w.writeheader()
        w.writerows(rows)
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prompts")
    p.add_argument("-o", "--out", default="-")
    r = sub.add_parser("review")
    r.add_argument("clips")
    r.add_argument("-o", "--out", default="review")
    a = ap.parse_args(argv)
    if a.cmd == "prompts":
        md = prompts_md()
        print(md) if a.out == "-" else Path(a.out).write_text(md)
    else:
        rows = review(a.clips, Path(a.out))
        missing = [r["clip"] for r in rows if r["file"] == "MISSING"]
        print(f"{len(rows) - len(missing)} clips reviewed into {a.out}/; missing: {', '.join(missing) or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
