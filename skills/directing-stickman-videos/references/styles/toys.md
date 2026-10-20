# Toys come alive (draft style reference, slug `toys`)

> In this repository: the sample package and its lint facts are `samples/toys.md` and `samples/toys.facts.md`. Other research files named below (gallery, tracks, gate output, renderer) stay in the project's `style-research/toys/` folder and are not part of the skill.

```text
Status: gated (2026-10-20). Covers: 3 clips, up to 4 toys on screen, a falling block caught, a block passed between
two toys, a block tower, 16:9.
Not covered: 9:16, close-ups of hands, crowds of toys, outdoor or daylight scenes, toys talking.
```

Evidence: posture gate and toy joint check on 61 poses and a 3-toy motion test (the cast of clip 2) (`README.md`,
`gallery/gate-v2.txt`, `motion-test/gate-v2.txt`); sample package `samples/toys.md` with its lint facts
block `samples/toys.facts.md` (`package_lint.py`: 0 red, 0 yellow; `hand_ledger.py` PASS;
`tests/verify-opening-hook.py` PASS). Everything lives in `/mnt/project-files/style-research/toys/`.

## When to use

Gentle stories, kids' explainers and short "what happens at night in the toy box" episodes: teamwork, sharing,
being different, simple physics (balance, towers, rolling). One small floor-level world, a cast of very different
toys, warm humour. Not for anything needing real people on screen.

## Sources

From general knowledge of these works; no frames were reviewed in this research, so treat the claims as the
direction, not a measured match.

| Work | What it supports | Where it runs out |
|---|---|---|
| Ladislas Starevich, *The Mascot* (*Fétiche*, 1933), stop-motion | Real handmade toys of mixed materials (plush, cloth, wood) come alive at night and stay visibly the material they are made of | Puppets are fully articulated and often grotesque; black-and-white; no joint limits |
| Hans Christian Andersen, *The Steadfast Tin Soldier* (1838) and its illustrated editions | The toy-box ensemble (soldier, dancer, toys that move only when no one watches), the "freeze when people come" rule | A text, not a look; the soldier is tin, not wood |
| Contemporary toy photography (macro shots of real figures on floors and tables, e.g. the toy photography community on Instagram) | The camera: floor-level macro lens, shallow depth of field, warm practical light, real textures | Still images: no motion, no rule for how a toy moves |
| Action-figure articulation guides (DC Collectibles, "Anatomy of an action figure", 2014; TFormers articulation articles) | Which joints each toy type has and how far they turn: the joint table below | Only plastic figures, nothing on plush, tin or tumblers (those limits are our own design) |

## Signature traits

| # | Trait (visible in a still) | Tag |
|---|---|---|
| 1 | Real toy materials that never change: molded plastic, stitched muslin, plush, painted tin, painted wood, glossy shell | must |
| 2 | Floor-level macro lens: shallow depth of field, a child's bedroom floor, warm lamp light and blue window glow | must |
| 3 | Toys bend only at their built joints: plush and dowel limbs stay straight or gently curved, the tin robot's arms never rise sideways | must |
| 4 | A mixed toy box: every character is a different kind of toy, distinct in silhouette and material | bonus |
| 5 | People, human hands, printed packaging, logos or letters on blocks | forbidden |

## Nearest neighbour

`brick-build` (research, gated): a stop-motion town built entirely of interlocking plastic bricks. Two differences a
viewer can see: (1) here every toy is a different material (plush, cloth, tin, wood, painted shell) on a real wooden
floor, there everything is glossy studded plastic on a studded baseplate; (2) here motion is smooth, there it is
stop-motion on twos with flicker. Among catalog styles the closest is Style 2B (full-colour cinematic environments),
which keeps the Style 2 stick-figure lead and has no material rule.

## Originality

No Toy Story, LEGO, Barbie, Funko, Playmobil, Transformers, Sylvanian or other recognisable designs or trade dress:
no cowboy/space-ranger pair, no stud-topped bricks or C-hand minifigures, no oversized square-headed vinyl, no
fashion doll. Chest plates carry no emblem. Prompts name no brand, film or studio, not even in the negatives
("no logos, no brand marks" is enough). The cast is one generic toy box with our own colours, faces and details.

## Frozen style block

Repeat verbatim in every clip:

```text
Style and environment: a warm, cozy toy-photography look: real toys come alive on the wooden floor of a child's bedroom at dusk, filmed like a macro lens close to the floor, shallow depth of field, soft warm lamp light from the right and a gentle blue window glow from the left. Every material reads true and stays the same: glossy molded plastic, cream muslin with visible stitches, soft fuzzy plush, painted tin with rivets, painted wood with fine grain, a glossy painted shell. Honey-colored floorboards, a plain cream wall with a skirting board, a few plain colored wooden blocks blurred in the background. Smooth, charming character animation with a handmade feel; toys keep their toy proportions and materials; not a cartoon drawing, no people anywhere.
```

Body rule, also verbatim in every clip, after the anchors:

```text
Every toy moves only the way it is built and never bends where it has no joint. Every toy wears one lime-green band on its right wrist only. In front view, hanging arms stay beside the body with a clear gap at the waist. Limbs keep their length, toys never stretch, melt or change material, and a moving limb replaces its previous pose.
```

## Character anchors and cast cards

Every toy wears a **lime-green band on the right wrist** (Đật on its right stub arm), the fixed left/right marker.
Each anchor ends with that toy's joint rule in plain words, because the joint rule is the identity. Paste the full
anchor of every toy on screen into each clip, unchanged (source: `src/rig.py`, `anchor` fields). Pose, position and
props stay out of the anchors.

| Toy | Kind | Silhouette and material (non-colour differences) | Hands / grip |
|---|---|---|---|
| Kit | action figure | slim jointed figure, pin hinges, sculpted hair, molded plastic | C-shaped grip: small props in one hand |
| Mây | rag doll | soft cloth body, yarn braids, dress, **button eyes that never change** | soft cloth hands: small light props only |
| Bông | plush bear | round and chubby, fuzzy, round ears, mitten paws | **cannot grip**: hugs with both paws |
| Thiếc | wind-up tin robot | boxy metal body, rivets, antenna, key on the back | knob hands: **clamps with both arms only** |
| Chốt | wooden soldier | thin dowel limbs, ball head, tall cylinder cap | ball hand with a hole: holds a stick only |
| Đật | roly-poly tumbler | pear-shaped shell, no legs, weighted base, stub arms | stub arms: hugs only |

```text
Kit, a jointed plastic action figure with a teal molded bodysuit, a plain orange chest plate with no emblem, short sculpted dark-brown hair, small round pin hinges visible at the elbows and knees, C-shaped grip hands, dark teal boots and a lime-green band on the right wrist; his elbows and knees bend only one way, as pin hinges, up to a right angle.

Mây, a soft rag doll of cream muslin with coral-orange yarn hair in two short braids, two round black button eyes that never change shape, a stitched smile, a blue gingham dress, small black cloth shoes and a lime-green band on the right wrist; her cloth arms and legs fold only at stitched seams, softly and one way.

Bông, a chubby lavender plush bear with soft fuzzy fabric, a pale lilac belly patch with a stitched seam, round ears with pink insides, small embroidered dark-purple eyes and nose, round mitten paws with no fingers and a lime-green ribbon band on the right wrist; his stuffed arms and legs have no elbows or knees and only curve a little.

Thiếc, a boxy wind-up tin robot of pale blue-silver metal with red trim, rows of round rivets, a round glowing amber window in the chest, two round amber lamp eyes, a short antenna with a red ball, a brass wind-up key on his back, round knob hands and a lime-green band on the right wrist; his straight tin arms swing only forward and back from the shoulders, never out to the side, and his short legs have no knees.

Chốt, a slim painted wooden toy soldier with a natural wood ball head, rosy painted cheeks and dot eyes, a tall plain black cylinder cap, a red painted coat with a row of gold dot buttons, black dowel legs, round wooden ball hands and a lime-green band on the right wrist; his straight dowel arms and legs have no elbows or knees and pivot only at the shoulders and hips.

Đật, a round roly-poly tumbler toy shaped like a pear, a glossy coral-pink shell painted with yellow and white dot flowers, a cream painted face with black painted hair, dot eyes and rosy cheeks, no legs, a round weighted base, two short stub arms and a lime-green band on the right stub arm; it rocks on its base and always rights itself.
```

## Articulation and posture limits

A toy only bends where it was built to bend. This is what makes it read as a toy and not a cartoon person, and it is
also where a video model is most likely to drift (a plush bear growing elbows, a tin robot waving like a person).
The table is enforced on every rig track by `src/toy_limits.py`, on top of the shared posture gate. Side-view
angles; "none" means the joint does not exist (held at 0 ± 4°).

| Toy | Shoulder | Elbow | Hip | Knee | Neck | Raise arm sideways | Other |
|---|---|---|---|---|---|---|---|
| Kit | −60…180 | 0…95 (one way) | −35…95 | 0…95 (one way) | ±15 | 0…110 | swivel waist, legs spread ≤ 35° |
| Mây | −45…160 | 0…60 (soft seam) | −35…100 | 0…60 (soft seam) | ±25 | 0…160 | button eyes never change |
| Bông | −30…130 | 0…25 (curve only) | −15…95 | 0…20 (curve only) | ±15 | 0…130 | waddles |
| Thiếc | −50…180 | none | −22…22 | none | none | **0…10 (never)** | shuffles on straight legs |
| Chốt | −60…180 | none | −35…60 | none | none | 0…170 | marches stiff-legged |
| Đật | −40…90 | none | no legs | no legs | none | 0…80 | rocks ≤ 35°, always rights itself |

Moves the rigs cannot do (found while posing the cast):
- Scratching the head is impossible for Kit, Mây, Bông (arms too short or too stiff to reach): use a shrug.
  Thiếc and Đật sway instead; Chốt raises one straight arm.
- Thiếc never waves or cheers sideways: wave and cheer in side view, arms swinging forward. He carries with two
  straight arms held out in front and cannot hug. He cannot sit: "running out of wind" replaces sitting.
- Chốt drums by swinging the whole straight arm from the shoulder; he sits on the edge of a block, legs straight out.
- Đật has no legs and is moved by others (nudged, rolled) or rocks in place.
- A lifted prop stays in front of the chest, below the face. Kit holds a block with his arms about level; past about
  45° above level the near arm crosses his face in profile (the shared gate's arm_over_face check).
- In front view, hanging arms keep a visible gap from the body at the waist (Bông's plush arms hang 20° out, Thiếc's
  7°).

## Core rules this style overrides

- **Posture negatives become joint-specific.** The five shared posture negatives stay verbatim; the style adds "no
  elbows or knees on toys built without them, no bending past a hinge, no tin robot arm raised out to the side, no
  legs on the roly-poly", because a toy with a hinge can still be asked to bend where it has none.
- **Faces.** Mây's button eyes never change; her expression lives only in stitched brows and mouth. Other toys have
  painted or embroidered faces that change only the small marks.
- **Holding.** Plush, tin and the roly-poly hold only with both hands. Each clip lists them in a `Two-hand holders:`
  line (a package extension `hand_ledger.py` reads; it errors on any one-hand hold for them).
- **Location changes.** The whole story stays on one bedroom floor (toys are small; a new setting is a new spot on
  the floor or a new shelf), unlike Style 4's new setting per clip. Time of night moves the light instead.
- **Characters do not speak.** The narrator speaks; toys act.

## Text policy

`none`. No letters, numbers or symbols on blocks, packaging, walls or anywhere in frame. Titles and subtitles are added
in post-production.

## Motion cadence

`smooth`. Charming, slightly weighted movement with a handmade feel; no stop-motion stepping, no motion smear on
jointless limbs.

## Camera moves

Follow the camera grammar in `storyboard-template.md`:
- Name the move in every beat. Default to transition moves: hold, slow lateral track at floor level, slow pull back,
  slow tilt.
- Hold during demanding toy actions: a catch, a pass between two toys, a fall and a roly-poly righting itself, an
  overhead reach. Never tilt, shake or orbit during them.
- At most one accent move per clip and in no more than one third of clips. Good accents: a fast push-in on a toy
  that freezes when light comes on.
- The camera stays at toy height; no human eye-level shots looking down at the floor (that reads as a person in the
  room).

## Prompt blocks per clip

1. Output line. (Clip 1's hook lives in its first frame and first timed beat, not in a separate line.)
2. Frozen style block.
3. `Characters (exactly N, no one else):` with the full anchor of every toy on screen, then the body rule.
4. Props with one fixed name each ("red block", "blue block", "big button", "red-tipped stick"), sized against a
   toy that is in the clip. Avoid a prop whose name contains another prop's name.
5. Composition with the camera rule, `Hands at start`, `Two-hand holders:`, first frame, three timed beats with the
   camera move named in each, the dialogue block, the frozen voice block, audio, final frame, `Hands at end`.
6. Negatives:

```text
Negative constraints: no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no humans, no human hands, no children, no adults, no toy packaging, no boxes with printing, no logos, no brand marks, no letters or numbers on blocks or anywhere, no visible text, no speech bubbles, no dialogue boxes, no watermark, no extra arms or legs, no third hand, no elbows or knees on toys built without them, no bending past a hinge, no tin robot arm raised out to the side, no legs on the roly-poly, no wristband on the left wrist, no swapped left and right hands, no prop switching hands without a visible pass, no hand covering the face, no morphing, no toy changing material or color, no duplicate characters, no 2D cartoon outlines, no anime style.
```

## Voice and music

The shared narrator contract is kept unchanged (the General American male narrator block from
`voice-continuity.md`, verbatim in every clip). The style's score, set in clip 1 and frozen:

```text
Audio: a light music-box melody with soft woodblock taps
```

Clips 2 and later begin their audio with: "the identical light music-box melody with soft woodblock taps from clip 1
continues, same tempo and instrumentation", then list sound effects separately (tin clicks, plush boffs, wooden
knocks, toy-drum taps on screen). The last clip may end the score "on one soft chime". Toy sounds are effects, never
new score instruments.

## Staging

- Side-on at floor level, full-body framing; front view only for reactions and two-handed hugs.
- Passes happen side-on between two toys facing each other, with the giver's arms straight out (Thiếc) or hugging
  (Bông) and the taker's hands on the far side of the prop. One character per hand sentence: "Kit takes the red block
  from Bông with both hands."
- Big props are sized to the hands: a marble or spool vanishes inside a hand, so use a button or a block.
- Toys freeze into ordinary toys whenever light or a person's arrival is implied: a reliable ending beat.

## Hooks that fit

Sudden event (a tower block falls and a toy catches it at about 1 s), Reaction before cause (all toys freeze and
stare off-frame), Scale shock (a toy beside a giant marble or slipper), Partial reveal (start on a mitten paw holding
a block, pull back). Keep the hit sound woody or soft (clack, thump, boff, tin click), not a bass drop.

## Post-production

- Trim each clip at its last usable frame where the next clip's first frame matches (same toys, same hands); do not
  assume the generated last frame is usable.
- Add titles and subtitles in post (text policy `none`).
- Check the right-wrist band and the jointless limbs at every pass and catch; regenerate a clip rather than paint
  over a bent plush arm.
- Level the music across clips (the music box should not restart audibly at a cut); keep the narrator dry.

## Sample package

`samples/toys.md`: "Tower before morning", 3 clips, 16:9, about 30 s. Lint facts block:
`samples/toys.facts.md` (`package_lint.py --clips 3` with the style, body and voice blocks passed as
`--anchor`): 0 red, 0 yellow. Rebuild with `sh src/package.sh`.

## Acceptance checklist

- Every pose and animation track passes `posture_gate.py check` (`rig` profile, `ground_y` on the floor,
  `body_width` = drawn chest width on front-view tracks) **and** `toy_limits.py` (the table above); multi-character
  shots pass `--scene`.
- The package passes `package_lint.py`, `hand_ledger.py` and `tests/verify-opening-hook.py`; one character per hand
  sentence; one name per prop.
- Visual review by eye: no bend on a jointless limb, Thiếc's arms never out to the side, the band on the right wrist
  in every view, a gap between hanging arms and the waist in front view, a prop held where the hands actually are.
- In a generated clip, also check: material consistency (plush stays plush, tin stays tin), whether the model keeps jointless
  limbs straight, Mây's unchanging button eyes, the wristband, and no letters on blocks.

## Generation risks

- The model's prior for "animated toys" is one famous film franchise; expect drift toward its look and toward a
  cowboy or space ranger. The negatives and plain designs push against it but this is the first thing to check.
- Human-like bending: plush arms gaining elbows, the tin robot waving like a person, the roly-poly growing legs.
- Letters appearing on blocks (alphabet blocks are the default), and packaging or brand marks.
- Human hands entering frame to pick up a toy.

## Catalog row (draft)

| Style Key | Style Name | Visual Theme | Best For | Character Design |
|---|---|---|---|---|
| `toys` | Toys Come Alive | Real toys on a child's bedroom floor at dusk, floor-level macro lens, warm lamp and blue window light | Gentle kids' stories, teamwork and sharing, simple physics (balance, towers) | Six different toys (action figure, rag doll, plush bear, tin robot, wooden soldier, roly-poly), each bending only at its built joints, lime-green band on the right wrist |

Status row: `toys | gated | Gate and lint reports in /mnt/project-files/style-research/toys/`.
Setup-gate line: "Toys come alive (experimental, gated): real toys on a bedroom floor."
