#!/usr/bin/env python3
"""Draw the before/after figures in tools/posture_gate/docs/ from the example tracks.

Usage: make_figures.py [--lang en|vi] [--out DIR]
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import make_examples as ex  # noqa: E402
import posture_gate as pg  # noqa: E402

TEXT = {
    "en": {
        "before": "Before: gate catches", "after_fix": "After posture_gate.py fix", "correct": "Correct",
        "pass": "PASS", "error": "ERROR", "warn": "WARNING", "nofix": " (not auto-fixed)",
        "legend": "blue = character's left side, green = right side, red = what the gate flags, orange = prop",
        "knee_backward": "Knee bends forward", "elbow_backward": "Elbow bends backward",
        "rubber_arm": "Arm stretches like rubber (+45%)", "head_backward": "Head tipped back 120°",
        "arm_pop": "Arm jumps 160° in one frame", "topple": "Leaning 55° while standing",
        "hand_swap": "Hands trade places", "torso_flip": "Upper body turned against hips",
        "cup_switches_hand": "Cup jumps to the other hand", "cup_in_wrong_hand": "Script: left hand. Drawn: right",
        "mirrored_hand": "Left hand drawn on right arm",
        "title_posture": "Posture gate: body errors", "title_hands": "Posture gate: left / right hand errors",
    },
    "vi": {
        "before": "Trước: gate bắt lỗi", "after_fix": "Sau posture_gate.py fix", "correct": "Đúng",
        "pass": "ĐẠT", "error": "LỖI", "warn": "CẢNH BÁO", "nofix": " (không tự sửa)",
        "legend": "xanh dương = bên trái nhân vật, xanh lá = bên phải, đỏ = chỗ gate bắt, cam = đồ vật",
        "knee_backward": "Đầu gối gập ngược ra trước", "elbow_backward": "Khuỷu tay gập ngược ra sau",
        "rubber_arm": "Tay dài ra như cao su (+45%)", "head_backward": "Đầu ngửa ra sau 120°",
        "arm_pop": "Tay nhảy 160° trong 1 khung", "topple": "Nghiêng 55° mà vẫn đứng",
        "hand_swap": "Hai tay tráo chỗ cho nhau", "torso_flip": "Thân trên quay ngược với hông",
        "cup_switches_hand": "Cốc tự nhảy sang tay kia", "cup_in_wrong_hand": "Kịch bản: tay trái. Vẽ: tay phải",
        "mirrored_hand": "Bàn tay trái gắn vào tay phải",
        "title_posture": "Posture gate: lỗi tư thế cơ thể", "title_hands": "Posture gate: lỗi tay trái / tay phải",
    },
}

POSTURE = [("knee_backward", ex.knee_backward, 5), ("elbow_backward", ex.elbow_backward, 4),
           ("rubber_arm", ex.rubber_arm, 7), ("head_backward", ex.head_backward, 8),
           ("arm_pop", ex.pop, 6), ("topple", ex.topple, 8)]
HANDS = [("hand_swap", ex.hand_swap, 6), ("torso_flip", ex.torso_flip, 8),
         ("cup_switches_hand", ex.cup_switches_hand, 6), ("cup_in_wrong_hand", ex.cup_in_wrong_hand, 6),
         ("mirrored_hand", ex.mirrored_hand, 8)]
W, H, LABEL = 230, 250, 290


def tag(result, fi, T):
    found = [i for i in result["issues"] if i["frame"] == fi]
    if not found:
        return T["pass"], "#1a7f37"
    if any(i["severity"] == "error" for i in found):
        return T["error"], "#e0312b"
    return T["warn"], "#b26b00"


def bad_joints(result, fi):
    return set().union(set(), *(set(i["joints"]) for i in result["issues"] if i["frame"] == fi))


def figure(rows, make, after, T, title, right_head):
    cells, y = [], 70
    for name, bug, fi in rows:
        before = make(bug)
        good = pg.fix(before) if after == "fix" else make(None)
        rb, rg = pg.check(before), pg.check(good, "rig")
        cells.append(f'<text x="12" y="{y + H / 2}" font-family="sans-serif" font-size="16" fill="#222">{T[name]}</text>')
        for col, (tr, res) in enumerate(((before, rb), (good, rg))):
            x = LABEL + col * (W + 20)
            cells.append(pg.skeleton_svg(tr["frames"][fi], bad_joints(res, fi), x, y, W, H - 10))
            text, color = tag(res, fi, T)
            if col == 1 and after == "fix" and text != T["pass"]:
                text += T["nofix"]
            cells.append(f'<text x="{x + 8}" y="{y + 22}" font-family="sans-serif" font-size="15" '
                         f'font-weight="bold" fill="{color}">{text}</text>')
        y += H
    width = LABEL + 2 * (W + 20) + 10
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{y + 40}" viewBox="0 0 {width} {y + 40}">'
            f'<rect width="100%" height="100%" fill="#fff"/>'
            f'<text x="12" y="28" font-family="sans-serif" font-size="20" font-weight="bold">{title}</text>'
            f'<text x="{LABEL}" y="58" font-family="sans-serif" font-size="16" font-weight="bold">{T["before"]}</text>'
            f'<text x="{LABEL + W + 20}" y="58" font-family="sans-serif" font-size="16" font-weight="bold">{right_head}</text>'
            + "".join(cells) +
            f'<text x="12" y="{y + 26}" font-family="sans-serif" font-size="13" fill="#555">{T["legend"]}</text></svg>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="en", choices=TEXT)
    ap.add_argument("--out", default=str(HERE.parent / "docs"))
    a = ap.parse_args()
    T, out = TEXT[a.lang], Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    side = lambda bug: ex.track(ex.frames_with(bug))
    front = lambda bug: ex.track(ex.front_frames(bug), rest=ex.front_pose(ex.wave(0)))
    suffix = "" if a.lang == "en" else f".{a.lang}"
    (out / f"posture-before-after{suffix}.svg").write_text(
        figure(POSTURE, side, "fix", T, T["title_posture"], T["after_fix"]))
    (out / f"hands-before-after{suffix}.svg").write_text(
        figure(HANDS, front, "correct", T, T["title_hands"], T["correct"]))
    print("wrote figures to", out)


if __name__ == "__main__":
    main()
