# Posture gate

Catches the body and left/right-hand errors video models make, at three points in the pipeline:

| When | Tool | Blocks? |
|---|---|---|
| Phase B prompts, before generating | `hand_ledger.py package.md` | yes |
| Code-rendered characters (SVG/JS/3D rigs) | `posture_gate.py check track.json` | yes |
| Generated clips (Flow) | `estimate_pose.py` then `posture_gate.py check` | review only |

Only the Python standard library is needed, except `estimate_pose.py` (`pip install mediapipe opencv-python-headless`).

![Posture errors the gate catches, and the result of fix](docs/posture-before-after.svg)

![Left/right hand errors the gate catches](docs/hands-before-after.svg)

## What it checks

- **Joint limits** in side view (knee and elbow only fold one way, hip, shoulder, neck, ankle) and front view (knee never bends sideways, leg/head tilt), from clinical range-of-motion norms in [`joint_limits.json`](joint_limits.json). A track can widen a limit with `"limits_override": {"sagittal": {"hip": {"max": 170}}}`, e.g. for a dancer's high kick.
- **Limb length**: a limb stretching or shrinking against its rest length (rigs), or stretching against the longest length seen (video).
- **Pops and snaps**: a joint turning faster than a person can in one frame (in front view too: an arm flung up in one frame); a knee or elbow flipping bend direction.
- **Balance** (warning): center of mass outside whatever touches the ground (feet, knees, pelvis, hands), held for about a fifth of a second or longer (3 frames at 12 fps, so a drawing held on twos passes), so a walk's single-support moments pass. Mark jumps and falls `"airborne": true`; list other supports per frame, `"supported": ["pelvis", "wrist_r", "chair"]` (joints or prop names), or `"supported": true`. A big-headed character can set `"mass": {"head": 0.3}` (segments: head, trunk, upper_arm, forearm, thigh, shank).
- **Head yaw** (3D tracks with a `nose` joint): head turned more than 80° from the body, measured about the neck, so a head tipped back (limbo, knee slide) is not a turned head. In 3D tracks elbows and knees are measured from their true 3D bones, a knee's bend direction from its own foot, and the front-view limits (leg spread sideways, knee bending sideways out of the plane of its thigh and foot) in the pelvis's own frame; the head turn is measured against the shoulders.
- **Left/right**: hands trading places (in side view arms may swing past each other at a human speed), both hands jumping across the body's midline in one frame (a warning), shoulders facing against the hips, a held prop jumping to the other hand (within a clip or across a cut), a prop drawn at the wrong hand, a left hand shape drawn on a right arm.
- **Contact** (optional): `"contacts": {"r": "door"}` (a prop name or a point) fails when that wrist stops more than 0.25 torso-lengths short of it. A big-handed character can widen this with `"contact_tolerance": 0.35` on the track or a frame, or give `"hand_length"` (track units, wrist to fingertip) so the whole hand counts as touching. A prop with a second point names it `"<prop>.<part>"` in `props`, and that point can have its own contact: a cane held at `"cane"` with `"cane.tip"` and `"contacts": {"l": "cane", "cane.tip": "ground"}` (the ground is the lowest foot); list `"cane.tip"` in `supported` when the character leans on it.
- **Ground** (optional): with `"ground_y"` (image y of the ground line) on the track or a frame, any joint or the bottom of the head below it fails (a roll or bow sinking into the floor).
- **Solid props** (optional): `"solids": {"block": [w, h]}` (`[w, h, d]` in 3D, track units) is a box of that size centered on the prop's point; a head or body joint inside it fails (a push with the head through the block). Hands may touch it.
- **Arms on the body** (warning, front view): with `"body_width"` (the drawn torso's width at the chest, track units) on the track or a frame, a shoulder joint inside the torso outline, or an arm hanging over the chest instead of beside it. Every joint angle can be legal while the arms lie on the body, and the joints alone cannot show it when the drawn torso is wider than the shoulders.
- **Arm over face** (warning): in front view a forearm sweeping across the head; in side view the near arm (the right arm when facing right) crossing the face half of the head, unless that hand holds a prop or has a contact there; in side view also a held prop sitting on the face (a raised ball). Mark intended moments `"face_cover": true`. The face is a circle of half the neck-to-head distance; a big-headed character sets its drawn head radius with `"head_radius"` on the track (or a frame), in track units. Not checked: a hand hidden behind a big head (2D occlusion).

`fix` repairs a rig track by clamping joint angles into range and restoring limb lengths. It does not invent new key poses for pops, balance or hand mix-ups; those still fail after `fix`.

## Several characters in one shot

`posture_gate.py check --scene sol.json kip.json` checks tracks of one shot against each other (same frames, same coordinates; each track has a `"name"`): a prop handed from one character to the other must be at the same place in both hands at the pass, a contact naming another character's joint (`"contacts": {"r": "Kip.wrist_l"}` for a high five or fist bump) must reach it, and one head must not sit inside another (`"overlap_ok": true` when one passes behind the other). Without `--scene`, several tracks are clips in story order.

## Pose track format

```json
{
  "fps": 12,
  "profile": "rig",
  "rest": {"neck": [0, -60], "...": "joints of the rest pose"},
  "frames": [
    {
      "facing": "right",
      "joints": {"head": [x, y], "neck": [x, y], "pelvis": [x, y],
                 "shoulder_l": [x, y], "elbow_l": [x, y], "wrist_l": [x, y],
                 "hip_l": [x, y], "knee_l": [x, y], "ankle_l": [x, y], "toe_l": [x, y],
                 "shoulder_r": "...", "...": "..."},
      "holds": {"cup": "l", "box": ["l", "r"]},
      "props": {"cup": [x, y]},
      "hands": {"l": {"looks_like": "l", "score": 0.95}}
    }
  ]
}
```

Image coordinates, y down. A 3D rig can pass `[x, y, z]` joints (and props) instead: each frame is checked in the body's own side view with true 3D bone lengths, so a limb pointing at the camera is not "shrunk" (`"up_axis"` defaults to `[0, 1, 0]`; coordinates are right-handed as in three.js/glTF, so a character facing +z has its own right hand at -x; set `"handedness": "left"` for Unity-style coordinates). If only a camera projection of a 3D rig is available, set `"projected": true`: limbs are then never called shrunk, and stretch is measured against the longest length seen. Draw `rest` in the same view as the frames. A rig that turns or tips the skull at the top of the neck exports `head` along the face direction (the skull's center, not a point straight above the neck), or the gate sees only part of the neck angle. `_l` / `_r` are the **character's** left and right. A prop carried in both hands is `"holds": {"box": ["l", "r"]}` or `"both"`. Put a held prop's point at the grip, not at its middle: a prop drawn more than 0.6 torso-lengths from its hand fails (`"hold_tolerance": 0.9` on the track or a frame widens this for a big prop), and a long prop's far end goes in its own `"<prop>.<part>"` point. `facing` is `left`, `right`, `front` (toward the camera), `back` or `side`; when omitted it is inferred from the feet and shoulder width. With `front` or `back` given, the gate also checks that the right shoulder is on the correct side of the screen, which catches a mirrored figure. Missing joints skip the checks that need them. `holds`, `props`, `hands`, `handoff`, `airborne`, `supported`, `contacts`, `face_cover` and `scale` (camera zoom on a rig) are optional.

Profiles: `rig` (strict, default for rig tracks), `pixel` (rigs snapped to a pixel grid: 1.5 px of rounding allowed on lengths; angles stay as strict as `rig`, so if rounding a 3 px bone trips an angle, gate the pre-snap joints for angles and the snapped joints for lengths), `video` (estimated poses, REVIEW only). In flat front view only a knee bending sideways under a hanging thigh is an error; other front-view hip and knee readings are warnings, since cross-legged sitting and kneeling look the same there, and limbs pointing at the viewer may look short.

[`examples/make_examples.py`](examples/make_examples.py) builds a walk cycle, a front-facing wave with a cup, and one track per bug; [`examples/make_figures.py`](examples/make_figures.py) redraws the figures above.

## Generated clips: what to expect

`estimate_pose.py` uses MediaPipe Pose Landmarker (Apache-2.0). It is trained on real people. On this repository's own Flow demo clips (sampled at 4 fps) it found a usable pose in 3 to 16 of 40 frames per clip, and 5 of 113 for the Style 3 demo. The poses it found were often drawn on scenery, a giant gavel or a beanie rather than the character: in the Style 1 Light, Style 2B and Style 4 café clips we inspected, every flag was an estimator mistake, not a character mistake. That is why the `video` profile reports `REVIEW` and exits 0: open `report.svg`, keep the flags that are real. Use `--strict` to fail instead.

The checks themselves were run on eight CMU Motion Capture clips projected to side view (walking, running, jumping and dance). The six everyday clips pass with no errors; two dance/gymnastics clips trip the hip and ankle limits on high kicks and pivots, which `limits_override` covers.

Pose models that may do better on cartoons (not tested here): RTMPose / DWPose (Apache-2.0, via `rtmlib`) and SDPose (MIT). Their keypoints map to the same track format. Avoid OpenPose (non-commercial licence), Ultralytics YOLO-pose (AGPL) and the AGPL anime pose weights unless that licence fits.
