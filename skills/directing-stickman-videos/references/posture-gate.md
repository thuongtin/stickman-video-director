# Posture and Hand Gate

Video models break bodies in repeatable ways: knees or elbows folding the wrong way, limbs stretching like rubber, heads twisting past the neck, an arm teleporting for one frame, and above all **left/right mix-ups**: hands trading places, a prop jumping to the other hand, a left hand drawn on the right arm. This reference covers how to prevent those in prompts and how to check output with `tools/posture_gate/` at repository level.

## In Phase A and Phase B (prevention)

- Name hands from the character's own side, never the viewer's: "her right hand". When the character faces the camera, add the screen side once in the beat that matters: "her right hand (on screen left)".
- Keep every held prop in one named hand. A change of hand is its own visible beat ("passes the cup to his left hand"), never implied.
- Phase A lists which hand holds each recurring prop. A late request to switch a lead hand is a global change: update it once before freezing, never clip by clip.
- Every Phase B prompt where a character holds or uses something carries two ledger lines, in the first-frame and final-frame states:

  ```text
  Hands at start — Pip: right hand holds the red paper card; left hand empty.
  Hands at end — Pip: right hand empty; left hand holds the red paper card.
  ```

  One entry per character, separated by a period; either hand may come first, and an animal's paw, flipper, wing, hoof, claw or fin, and a glove, mitten, fist or palm, counts as its hand. The next clip's start line equals the previous end line; for an approved change across the cut, mark the line itself: `Hands at start (time cut) — ...` or `Hands at start (handoff) — ...`. Any package where a beat holds, grabs or carries something needs these lines in every clip. Never write "near hand" or "far arm": they swap when the character turns.
- With several characters, the ledger is checked per character: name the character who acts at the start of each clause ("Mimi takes the bear with her left hand", "passes it to Bo, who takes it with his right hand"), empty the giver's hand after a pass (one prop is never in two characters' hands in one line), and name the prop and the receiving hand in the sentence that passes, drops or picks it up ("Bao hands Mira the loaf, and Mira takes it in her right hand"). A prop carried in both hands is listed in both: `right hand holds the box; left hand holds the box`. A prop the beats name by its parts lists them in brackets: `right hand holds the shoulder pole (with baskets)`. A hand that ends empty needs a beat that lets go ("sets the brush down on the table", "opens her right hand"), and "with both hands" needs both hands free of other props. Something picked up or caught mid-clip that the hands lines never list is put down again in a later beat. Name the hand that picks up, takes or points ("with her left hand", not "with her hand"), and never point with a hand that holds something. The last beat that shows a prop in a character's hands matches their end line. A character with no hands has no hands lines. Call a prop in the beats by the word the hands lines use, or list that word in brackets: `left hand holds the bánh chưng (cake)`. A character who skips a clip starts the next one with their own last hands line. Every object a hand holds is in the ledger; one missing from it gets a warning. A hand picks up something new only after a beat puts down what it held, and the character who held a prop is the one who lets it go or passes it (a catch by someone else is not a release; "lowers the axe" is not a release, "leans the axe against the block" is). A beat that only looks at a prop in a hand does not pass it. A prop the hands lines keep in both hands is shown in both: describe a two-handed grip hand by hand in one sentence ("low in his right hand and high in his left hand", "adds his left hand above it"), never "in his left hand alone". Don't wave with a hand that holds something all clip. The final frame shows how the clip ends; it is not the beat that gets there.
- Add posture negatives to every prompt: `no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no prop switching hands without a visible pass`. Keep them in the negative list, not in the character anchor. (A rubber-hose or noodle-arm character may bend smoothly; it still keeps its limb length.)

Before delivering Phase B, save the package as Markdown and run:

```bash
python3 tools/posture_gate/hand_ledger.py package.md
```

Repair every reported problem before responding.

## After generation (acceptance)

**Code-rendered characters** (paper cutout, flat vector, low-poly rigs): export a pose track (2D joints per frame, see `tools/posture_gate/README.md`) and gate it strictly. This blocks: joints past human range of motion, limbs changing length, one-frame pops, knees/elbows snapping direction, shoulders facing against the hips, hands trading places, props in or jumping to the wrong hand, mirrored hands. `fix` clamps joint angles and restores limb lengths; pops and balance need a new key pose. Mark seated, kneeling, leaning or pushing frames with what holds the body up (`"supported": ["pelvis"]`), use the `pixel` profile for pixel-snapped rigs, and export 3D rigs as 3D joints rather than a camera projection. For several characters in one shot, also run `check --scene` on their tracks together. In front view, put the shoulders at the edge of the drawn torso so hanging arms fall beside the body, and give the track `"body_width"` so the gate warns when they lie over the chest.

```bash
python3 tools/posture_gate/posture_gate.py check track.json --report out/
python3 tools/posture_gate/posture_gate.py fix track.json -o fixed.json
```

**Generated clips** (Flow): estimate poses, then review the flagged frames.

```bash
python3 tools/posture_gate/estimate_pose.py clip.mp4 -o track.json --fps 4 --hands
python3 tools/posture_gate/posture_gate.py check track.json --report out/
```

The video gate reports `REVIEW`, not `FAIL`: MediaPipe Pose is trained on real people, finds a pose in only part of the frames of stick figures and cartoons, and sometimes draws a skeleton on scenery or a hat. Look at `out/report.svg`, confirm or dismiss each flagged frame, and say how many frames had a usable pose. A clean video report is not proof the clip is clean. For several clips in story order, pass all tracks to one `check` to also catch props changing hands across cuts.
