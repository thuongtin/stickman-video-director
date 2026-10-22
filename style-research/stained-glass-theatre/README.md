# Lumen: stained-glass theatre

Experimental original character and 10-second silent motion demo. Narrowly gated technical draft, not an owner-approved style pack. See [research and coverage](research.md), [concept options](concept/options.png), [demo](motion/demo.mp4), [state gallery](gallery/contact-sheet.jpg), and [posture report](motion/gate.json).

## Reproduce

From the repository root, with Python3 and Pillow available:

```sh
python3 style-research/stained-glass-theatre/src/render.py
python3 tools/posture_gate/posture_gate.py check --json style-research/stained-glass-theatre/motion/track.json
ffmpeg -y -v error -framerate 12 -i style-research/stained-glass-theatre/motion/frames/%04d.png -c:v libx264 -crf 19 -pix_fmt yuv420p -movflags +faststart style-research/stained-glass-theatre/motion/demo.mp4
python3 tools/package_lint/package_lint.py style-research/stained-glass-theatre/sample.md --clips 1 --facts style-research/stained-glass-theatre/sample.facts.md
python3 tests/verify-opening-hook.py style-research/stained-glass-theatre/sample.md
python3 style-research/stained-glass-theatre/src/review_sheet.py
python3 style-research/stained-glass-theatre/src/verify.py
```

The rig reuses this repository's front-pose math with original drawing code and longer limb dimensions. No dependency or security changes. Tested with Python3, Pillow12.3.0 and ffmpeg7.1.5 in an assistant cloud workspace. The prospective narrated sample is a text lint fixture only, not the soundtrack of the silent demo and not an external rendering service test. Imagegen concept is an illustration used before coding, not an exact production image or optical simulation.

The gallery covers notice, outward flourish, release, raising the own-right hand, wave, lowering and rest. It does not certify walking, side/rear views, grasping or multiple characters. The source parameters and exported joints remain editable. Run src/review_sheet.py for the real-video risk sheet and src/verify.py for framecount/decode/hash checks. The sheet helper documents a 12fps last-frame seek issue in the repository extractor and adds explicit wave-transition times; it does not change posture scoring. Generated per-frame PNGs are intentionally ignored; retained gallery and MP4 are review artifacts.
