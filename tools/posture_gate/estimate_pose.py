#!/usr/bin/env python3
"""Estimate a pose track from a generated clip (or a folder of frames) with MediaPipe Pose.

Usage:
  estimate_pose.py clip.mp4 -o track.json [--fps 4] [--hands] [--frames-dir DIR] [--model pose_landmarker_full.task]

Then gate it:  posture_gate.py check track.json --profile video --report out/

Needs: pip install mediapipe opencv-python-headless   (Apache-2.0)
The model file is downloaded once to ~/.cache/posture_gate/ if --model is not given.

MediaPipe is trained on real people. On thin stick figures it often finds no pose, or
latches onto background shapes; frames without a confident pose are recorded as
"no pose" and never fail the gate on their own. --hands adds a hand-shape check
(which hand is drawn on which arm); it needs visible fingers, so it does nothing on
mitten or stick hands. Treat the video gate as a filter
for clear errors, not a certificate.
"""
import argparse
import json
import sys
import urllib.request
from pathlib import Path

MODEL_URL = ("https://storage.googleapis.com/mediapipe-models/pose_landmarker/"
             "pose_landmarker_full/float16/latest/pose_landmarker_full.task")
HAND_URL = ("https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
            "hand_landmarker/float16/latest/hand_landmarker.task")

# MediaPipe BlazePose landmark index -> gate joint name
MP_JOINTS = {
    "shoulder_l": 11, "shoulder_r": 12, "elbow_l": 13, "elbow_r": 14, "wrist_l": 15, "wrist_r": 16,
    "hip_l": 23, "hip_r": 24, "knee_l": 25, "knee_r": 26, "ankle_l": 27, "ankle_r": 28,
    "heel_l": 29, "heel_r": 30, "toe_l": 31, "toe_r": 32,
}
EARS = (7, 8)


def model_path(arg, url=MODEL_URL):
    if arg:
        return arg
    p = Path.home() / ".cache/posture_gate" / url.rsplit("/", 1)[-1]
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        print(f"downloading {url}", file=sys.stderr)
        urllib.request.urlretrieve(url, p)
    return str(p)


def attach_hands(frame, result, w, h):
    """Put each detected hand on the nearer body wrist and record which hand it looks like.
    MediaPipe labels handedness as if the image were a mirrored selfie, so the label is
    swapped here for ordinary (unmirrored) video frames."""
    j = frame["joints"]
    for lms, cls in zip(result.hand_landmarks, result.handedness):
        hx, hy = lms[0].x * w, lms[0].y * h
        near = [(abs(hx - j[k][0]) + abs(hy - j[k][1]), k[-1]) for k in ("wrist_l", "wrist_r") if k in j]
        if not near:
            continue
        dist, side = min(near)
        forearm = [abs(j[f"elbow_{s}"][0] - j[f"wrist_{s}"][0]) + abs(j[f"elbow_{s}"][1] - j[f"wrist_{s}"][1])
                   for s in ("l", "r") if f"elbow_{s}" in j and f"wrist_{s}" in j]
        if forearm and dist > max(forearm):
            continue  # a hand that belongs to no wrist we know of
        label = cls[0].category_name.lower()[0]
        frame.setdefault("hands", {})[side] = {"looks_like": "r" if label == "l" else "l",
                                               "score": round(cls[0].score, 3)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="video file or folder of PNG/JPG frames")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--fps", type=float, default=4.0, help="frames per second to sample from a video")
    ap.add_argument("--frames-dir", help="where to save sampled frames (referenced by the report)")
    ap.add_argument("--model")
    ap.add_argument("--min-detection", type=float, default=0.5)
    ap.add_argument("--hands", action="store_true",
                    help="also run MediaPipe Hand Landmarker to catch a left hand drawn on a right arm")
    ap.add_argument("--hand-model")
    a = ap.parse_args(argv)

    import cv2
    import mediapipe as mp
    from mediapipe.tasks.python import BaseOptions, vision

    landmarker = vision.PoseLandmarker.create_from_options(vision.PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=model_path(a.model)),
        num_poses=1, min_pose_detection_confidence=a.min_detection))
    hands = vision.HandLandmarker.create_from_options(vision.HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=model_path(a.hand_model, HAND_URL)),
        num_hands=2)) if a.hands else None

    src = Path(a.source)
    out = Path(a.out)
    frames_dir = Path(a.frames_dir) if a.frames_dir else out.parent / (out.stem + "_frames")
    frames_dir.mkdir(parents=True, exist_ok=True)

    images = []
    if src.is_dir():
        images = [(p, cv2.imread(str(p))) for p in sorted(src.iterdir()) if p.suffix.lower() in (".png", ".jpg", ".jpeg")]
        fps = a.fps
    else:
        cap = cv2.VideoCapture(str(src))
        native = cap.get(cv2.CAP_PROP_FPS) or 24
        step, i, fps = max(1, round(native / a.fps)), 0, native / max(1, round(native / a.fps))
        while True:
            ok, img = cap.read()
            if not ok:
                break
            if i % step == 0:
                p = frames_dir / f"f{len(images):04d}.jpg"
                cv2.imwrite(str(p), img)
                images.append((p, img))
            i += 1

    frames = []
    for path, img in images:
        h, w = img.shape[:2]
        mpimg = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        res = landmarker.detect(mpimg)
        f = {"image": str(Path(path).resolve()), "image_size": [w, h], "joints": {}, "conf": {}}
        if res.pose_landmarks:
            lm = res.pose_landmarks[0]
            for name, idx in MP_JOINTS.items():
                f["joints"][name] = [round(lm[idx].x * w, 1), round(lm[idx].y * h, 1)]
                f["conf"][name] = round(lm[idx].visibility, 3)
            e1, e2 = lm[EARS[0]], lm[EARS[1]]
            f["joints"]["head"] = [round((e1.x + e2.x) / 2 * w, 1), round((e1.y + e2.y) / 2 * h, 1)]
            f["conf"]["head"] = round(min(e1.visibility, e2.visibility), 3)
            if hands:
                attach_hands(f, hands.detect(mpimg), w, h)
        frames.append(f)

    track = {"source": "estimator", "estimator": "mediapipe-pose-landmarker-full", "profile": "video",
             "fps": round(fps, 3), "frames": frames}
    out.write_text(json.dumps(track, indent=1))
    found = sum(1 for f in frames if f["joints"])
    print(f"wrote {out}: pose found in {found}/{len(frames)} frames")


if __name__ == "__main__":
    sys.exit(main())
