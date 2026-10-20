# Brick-built town (draft style reference, slug `brick-build`)

> In this repository: the sample package and its lint facts are `samples/brick-build.md` and `samples/brick-build.facts.md`. Other research files named below (gallery, tracks, gate output, renderer) stay in the project's `style-research/brick-build/` folder and are not part of the skill.

```text
Status: gated (2026-10-20). Covers: 3 clips of 16:9, up to 3 figures on screen, a two-hand brick clamp, a bar-prop
handoff between two figures (baguette), a stick touching a set piece (wick pole to lamp), a legless skirt figure.
Not covered: 9:16, night or interiors, crowds of more than 4, fast action, dialogue by characters.
```

Evidence: 60 v2 pose tracks in `gallery/tracks/v2/` pass `posture_gate.py` (shared PR #4 copy, 0 FAIL, 0 WARN) and
`src/brick_limits.py` (0/60); the 4-figure motion test passes `--scene`; the sample package passes
`package_lint.py` (facts below). Signature checklist below. Draft pack, not yet in the skill catalog. All files live in
`/mnt/project-files/style-research/brick-build/`.

## When to use

Short explainers and gentle stories that benefit from a "built world": how things fit together, cause and effect,
teamwork, small physics jokes (a wall popping apart, a piece that only fits one way). A tiny town where everything,
people included, is made of interlocking plastic bricks, filmed like real tabletop brick stop-motion.

## Signature checklist

### Sources

| Work | What it supports | Where it runs out |
|---|---|---|
| *The Magic Portal* (Lindsay Fleay, Perth, 1985-89; [ACMI](https://www.acmi.net.au/works/102--the-magic-portal/), [Wikipedia](https://en.wikipedia.org/wiki/The_Magic_Portal)) | Real brick stop-motion on a table: hard plastic that only moves at its joints, stepped timing, practical light on glossy studs | Mixes plasticine, cardboard and live action; I read about it and saw stills, not every frame |
| *The Lego Movie* (2014, Animal Logic; [MPA](https://www.motionpictures.org/2014/02/how-the-lego-movie-got-its-stop-motion-look/), [Animal Logic](https://animallogic.com/portfolio/projects/tlm/)) | "Emulated stop-motion": every brick given fingerprints, dents, seam lines, scratches and dust; the look of a real toy under macro light | It is CGI, licensed figures and sets (nothing of its design is used); its frame-rate choices are not documented in what I read |
| Brickfilm genre and Brotherhood Workshop (Kevin Ulrich, YouTube, from 2012; [Brickfilm](https://en.wikipedia.org/wiki/Brickfilm), [interview](https://blog.firestartoys.com/interview-with-an-afol-brotherhood-workshop/), [technique notes](https://thebrickblogger.com/2013/06/lego-video-tutorial-how-to-make-things-fly)) | Fan stop-motion grammar: baseplate sets, macro framing, hidden rigs for flying props, low frame rates, small camera slider moves | Mostly licensed figures and parody; I used written descriptions and tutorials, not a frame study |

The trademark cases under "Originality" are legal sources, not visual ones.

### Five signature traits

1. `must` Glossy molded plastic everywhere, with round plain studs, crisp seams, faint fingerprints and scuffs under
   macro light and shallow depth of field.
2. `must` Figures move only at plastic joints: head swivels, torso rigid, elbows and knees fold one way in visible
   15° clicks, knob hands hold only bars.
3. `must` Stop-motion on twos: 12 held poses per second, no motion blur, slight light flicker between poses.
4. `bonus` A tabletop town on a green studded baseplate with a grey studded road, stacked-brick buildings and
   round-brick trees.
5. `forbidden` Any brand mark, letters or numbers, and the minifigure silhouette (cylinder head with a stud, C hands,
   trapezoid torso, yellow default skin).

### Nearest neighbour

`voxel-world` (gated, same round). Visible differences: (1) brick-build is glossy molded ABS with round studs,
fingerprints and specular highlights under a macro lens, voxel-world is flat 16×16 pixel textures on matte cubes with
block-game lighting and no studs; (2) brick-build moves on twos in joint clicks with knob hands and hinged elbows and
knees, voxel-world swings straight box limbs with no elbows or knees. Second neighbour: `toys` (mixed materials,
smooth motion, one action figure among plush and tin).

## Visual identity

- Real brick stop-motion, as if shot frame by frame on a table: a town on a green studded baseplate with a grey
  studded road, buildings stacked from 2x4 bricks and plates, round-brick trees with cone leaves, a pale backdrop.
- Macro lens at baseplate height, shallow depth of field, soft warm key from the upper right, cool fill from the left.
- Every surface is glossy molded ABS: round **plain** studs, crisp seams between bricks, faint fingerprints and fine
  scuffs catching the light. Plastic never bends, stretches or melts.
- Motion: 12 poses per second, each held two frames (shot "on twos"), no motion blur, a very slight light flicker
  between poses. Limbs move in visible clicks.
- **No people, no human hands, no logos, no letters or numbers anywhere** (not on studs, bricks, signs or prints).

## Originality and the brand risk

The interlocking brick itself is a functional shape that cannot be a trademark in the EU (Lego Juris v OHIM,
C-48/09 P, 2010), so studded bricks are free to use. The **minifigure shape is a registered 3D EU trade mark** and has
been upheld twice: Best-Lock v OHIM (T-395/14, T-396/14, 2015) and BB Services (Bluebrixx) v EUIPO (T-297/22,
6 Dec 2023). So this style keeps the bricks and never draws that figure:

| Minifigure trait (avoid) | Our figure |
|---|---|
| cylinder head with a stud on top | rounded-cube head, no stud, on a visible round neck peg |
| trapezoid torso, wider at the hips | straight-sided box torso and a separate hip block |
| one-piece arms and legs, no elbows or knees | two-piece arms and legs with small grey click hinges |
| C-shaped claw hands | round knob hands with a hole through them |
| yellow default skin | varied skin tones (tan, light, brown, medium-brown, deep-brown) |
| printed brand on every stud | plain smooth studs |

- Never write the brand word in a prompt: it pulls the model straight to minifigures, logo studs and licensed sets.
  Say "plastic toy bricks", "brick-built figure", "studded baseplate".
- No licensed sets, characters or themes (no city police, space or castle themes copied from catalogues).

## Cast grammar (town of Phố Khối)

| Figure | Build | Identity marks (keep in every anchor) |
|---|---|---|
| Bác Vữa, builder | standard | tan head, printed bushy mustache, orange hard hat, teal shirt, navy overalls print |
| Cô Bột, baker | standard | light head, short dark-brown hair, tall white chef hat, white sleeves, coral top, cream apron print |
| Anh Tem, mail carrier | standard | brown head, red cap with short visor, sky-blue jacket, printed satchel strap, brown satchel brick on his **left** hip |
| Bé Nút, kid | short | medium-brown head, freckles, green cap worn backwards, yellow-white striped shirt, red shorts, white plate sneakers |
| Bà Rêu, grandma gardener | skirt (no legs) | light head, grey bun, round printed glasses, lilac cardigan, moss-green sloped skirt brick |
| Ông Tạ, lamplighter | tall | deep-brown head, printed light-grey full beard, grey-olive flat cap, dark indigo hip-length coat with gold printed buttons |

Every figure wears **one lime-green ring on the right wrist only** (fixed left/right marker). Full anchors are the
`anchor` fields in `src/rig.py`; copy them verbatim into every clip together with `FIGURE_RULE` and `JOINT_RULE`.
Faces are printed decals and can be swapped (10 expressions); the head itself never changes shape.

## Articulation (the core rule)

A brick figure only moves at its plastic joints. This is what makes it read as a toy, and it is where a video model
drifts most (heads nodding, waists bending, elbows bending like rubber, legs doing splits).

| Joint | Range | Notes |
|---|---|---|
| Neck | swivel ±90°, no nod, no tilt | to look up, the whole body leans back on the hip pins |
| Shoulder | −90…180° swing; splay 0…20° | a raised arm cannot go out sideways; waving and cheering go forward-up |
| Elbow | 0…90°, one way, 15° clicks | forearm stays in the upper arm's swing plane |
| Torso | rigid, one piece with the hip block | bowing = tipping on the hip pins with straight legs |
| Hip | −45…90°, no sideways spread | |
| Knee | 0…90°, one way, 15° clicks | |
| Ankle | none | the plate foot is fixed to the shin |
| Hand | round knob with a through hole | holds only a round bar, **square to the forearm**; anything without a bar is clamped between both hands |
| Skirt figure | no legs | glides in small even steps, cannot sit or kneel |

Consequences that look odd in words but right on screen (all checked by eye):
- Because the hole is square to the forearm, a stick aimed forward-up needs the forearm aimed forward-down (lamplighter
  pole, pinwheel); a level trowel needs the arm hanging almost plumb.
- A bar prop may spin in the hole (a watering can or parcel hangs level by itself).
- Sitting: knees 90°, knobs beside the knees (shoulders are wider than knees and the splay only opens outward).

`src/brick_limits.py` checks every 3D track against this table, alongside the shared posture gate.

## Core rules this style overrides

| Core rule | Override here | Why |
|---|---|---|
| Expressive animated faces | Faces are printed decals, swapped between poses (10 expressions); the mouth never animates mid-pose | A real brick head is a printed part; a talking mouth breaks the toy |
| Idle and reaction beats with small body acting | Idle = a held pose; reactions are a head swivel or one arm click, never a shrug, nod or sigh | The rig has no neck nod, no waist, no shoulder shrug |
| Smooth motion | Stepped on twos, camera moves stepped too | Stop-motion is the style's identity |
| Music | One light marimba and soft woodblock theme set in clip 1, repeated "the same theme continues from clip 1 with identical tempo and instrumentation" in every later clip; plastic tick and click SFX on poses | Keeps the score frozen across clips |
| Location changes | Only within the one tabletop town (bakery, wall, lamp, garden); a new location is a hard cut to another part of the same baseplate | The world is one built set |
| Body bans | No waist bend, head nod or tilt, leg spread, limbs past 90°, legs on the skirt figure | Joint table above |

## Text policy and cadence

- Text policy: `none`. No letters or numbers anywhere in frame; any captions are added in post.
- Motion cadence: `on-twos` (12 poses per second, each held two frames).

## Camera moves

- Allowed transition moves: hold (default, and always during a brick clamp, a handoff or a fall), slow lateral track
  or pan along the baseplate, slow push-in, slow pull back (the Reveal hook), hard cut to another part of the town.
  All are slider moves stepped on the same twos and stay horizontal: no tilt.
- Accent moves: at most one per clip and in at most one third of the clips; only a quick push-in on a physics-break
  hit. No orbit, shake, whip pan or tilt during any two-hand clamp or handoff.
- No three inward moves in a row across clips. The sample package uses hold → track → push-in, track → hold → track,
  hold → pan → pull back.

## Post-production

1. Conform the three clips to 24 fps and trim each to the last held pose before its end so cuts land on holds.
2. Keep the light flicker; do not add motion blur or frame interpolation (it turns the style into CGI).
3. Any subtitles or titles are added in post, outside the baseplate area, never as printed bricks.
4. Check the right-wrist ring, the two-hand clamp and Bà Rêu's skirt on the risky frames before publishing.

## Shared prompt blocks

Repeat in every clip (Omni Flash keeps no memory between clips); exact text in `samples/brick-build.md`:
`Style and environment`, `Characters (exactly N, no one else)` = anchors + figure rule + joint rule + ring line,
`Dialogue` (voiceover only), `Voice` (approved General American male narrator block), `Negative constraints`
(no humans or human hands, no logos or brand marks, no lettering on studs, no letters or numbers anywhere, no
cylinder heads, no stud on a head, no claw or C hands, no bending at the waist, no head nod or tilt, no head turned
past the shoulders, no knees or elbows bending backward, no elbows or knees past a right angle, no limbs changing
length, no leg splits, no legs on the skirt figure, no ring on the left wrist, no swapped left and right hands, no
prop switching hands without a visible pass, no smooth CGI motion, no motion blur, no melting plastic).

The style block, written once and frozen (from `src/make_package.py`, verbatim in every clip):

```text
Style and environment: real brick stop-motion, like a tabletop film shot frame by frame: a small town built entirely
from glossy plastic toy bricks on a green studded baseplate with a grey studded road, a tan brick bakery with a
red-and-white striped awning and a clear window, a dark grey street lamp, a tree of stacked round brown bricks with
green cone leaves, and a pale blue backdrop. Filmed with a macro lens close to the baseplate: shallow depth of field,
the background softly blurred, a soft warm key light from the upper right and a cool fill from the left. Every surface
is glossy molded ABS plastic with round studs on top, crisp seams between bricks, faint fingerprints and fine scuffs
catching the light. The studs are plain and smooth. Animation is stop-motion at 12 poses per second, each pose held for
two frames, no motion blur, a very slight light flicker between poses; figures move in small clicks. When the camera
moves it is a slow slider move stepped on the same twos. Not CGI, not a cartoon drawing, no people anywhere.
```

The figure rule allows the skirt figure explicitly ("…two-piece legs with click hinges at the knees and flat plate
feet, except a skirt figure, which stands on one sloped skirt brick and has no legs").

## Staging and motion

- Side-on views for any action with props or contact; front view only for waves and cheers.
- Walk: legs swing from the hip pins, the swinging knee clicks 0-15-30-45, the stance leg stays straight and the foot
  stays planted (no sliding).
- One character per hand sentence; name the hand from the figure's own side, never "near hand".
- Props keep one name across clips (red brick, baguette, wick pole, watering can) and never share a word with a set
  piece (the pole was renamed "wick pole" so it is not confused with the lamp).
- Bricks are always handled with both hands; a released brick lands on studs, not mid-air.
- Bending is always written as "tipped forward on the hip pins with straight legs", never "bends at the hips".
- Name one camera move per beat (see Camera moves).

## Hooks that fit

Physics break (a row pops off its studs), Sudden event (a piece falls into frame), Reveal (pull back from one brick to
the whole town), Question (the VO asks which figure to build next). See the Golden Hook section of `references/storyboard-template.md`. The hit stays
toy-sized: a cascade of plastic clicks and a short clatter, no explosion, no camera shake.

## Acceptance checklist

1. No brand word, no logos, no letters or numbers anywhere in frame.
2. No minifigure traits (table above); heads are rounded cubes with no stud.
3. Each figure keeps its anchor marks and the lime ring on the right wrist.
4. Head never nods or tilts; torso never bends; elbows and knees fold one way up to 90°; legs never spread.
5. Knob hands hold only bars; bricks are clamped in both hands; the skirt figure never shows legs.
6. Stepped stop-motion timing, no motion blur, no morphing or melting plastic.
7. Every clip with a brick declares `Two-hand props: red brick.` (or the brick's name); hands lines pass `hand_ledger.py`; Clip 1's first frame and first beat carry the hook and pass `verify-opening-hook.py`.

## Sample package and lint facts

Sample: `samples/brick-build.md` ("The top row pops", 3 clips). `hand_ledger.py` (shared PR #4 copy): PASS;
`tests/verify-opening-hook.py`: PASS; `package_lint.py --clips 3` from the PR #4 branch (claude/posture-gate-drmgl9 at 99de4b9, which contains f99e90a, same hand_ledger as the shared copy): 0 RED, 0 YELLOW. Facts block
(`samples/brick-build.facts.md`, `--verify`: intact):

<!-- package_lint facts: generated, do not edit -->
- package: `package.md` sha256 a6296bfc63d4627e
- checked: 2026-10-20
- storyboard rows: none
- prompts: 3
- hand_ledger: PASS
- red: 0
- yellow: 0
<!-- package_lint facts end sha256=a1451c107ea28bd0905c3180d345cd39135859f899d8d7a8a7b62fa84df6677a -->

## Catalog entry (draft)

| Style Key | Style Name | Visual Theme | Best For | Character Design |
|---|---|---|---|---|
| **brick-build** | Brick-Built Town (stop-motion) | A tabletop town of glossy plastic toy bricks on studded baseplates, macro lens, shallow depth of field, stop-motion on twos | Explainers about how parts fit together, cause and effect, gentle kids' stories, small physics jokes | Original brick figures: rounded-cube head with no stud, neck peg, box torso, hinged two-piece limbs, round knob hands, lime ring on the right wrist |

Status row: `| brick-build | gated | 60 gated pose tracks, 4-figure scene, linted 3-clip package |`.
Setup-gate line (offer only when the user asks for an experimental style): `` `brick-build (Brick-Built Town, gated, experimental)`: glossy plastic brick figures and a brick town filmed as tabletop stop-motion ``.

## Generation risks

- Drift back to the famous minifigure (yellow cylinder head, C hands) even without the brand word: anchors spell out
  the head, neck peg and knob hands, negatives ban the rest.
- Logo or letters printed on studs, or random text on bricks and signs.
- Smooth CGI motion instead of stepped stop-motion; motion blur; rubbery limbs.
- Heads nodding and waists bending like people; the skirt figure growing legs.
- A brick held in one hand, or the ring jumping to the left wrist.
- Faces: printed faces may animate like cartoon faces; keep expression changes as swaps between poses.
