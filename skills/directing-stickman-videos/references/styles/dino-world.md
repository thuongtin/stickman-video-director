# Dino world (style pack, slug `dino-world`)

> In this repository: the sample package and its lint facts are `samples/dino-world.md` and `samples/dino-world.facts.md`. Other research files named below (gallery, tracks, gate output, renderer) stay in the project's `style-research/dino-world/` folder and are not part of the skill.

```text
Status: gated (2026-10-20). Covers: 3 clips of 10 s, 16:9, one kid explorer with up to two dinosaurs per clip,
one prop handoff (dinosaur to kid), a sauropod walk, a hadrosaur dropping to four legs.
Not covered: 9:16, more than three characters in a clip, night or rain, close-ups of mouths eating, fights.
Not scored (no independent review yet).
```

Evidence: posture gate on every pose and the motion test (`gallery/gate-v2.txt`, `motion-test/scene-gate-v2.txt`,
the 4-character `--scene` run included), the dinosaur rule check (`src/dino_rules.py`), and the sample package
`samples/dino-world.md`, which passes `package_lint.py` with the shared hand ledger. Lint facts block:
[`samples/dino-world.facts.md`](samples/dino-world.facts.md); lint and hook-test output:
[`prompt-package/lint-output.txt`](prompt-package/lint-output.txt).

## When to use

Kids' science and nature explainers about dinosaurs, fossils, footprints, food webs and "how do we know?" stories;
friendly adventure shorts for ages 4–10. Not for scary dinosaur action, survival horror or museum-realistic
reconstructions.

## Sources (look, not characters)

Named from general knowledge of these works; no frames were collected in this thread, so the claims are about the
overall look only. Nothing below is named in any prompt.

1. **Dinosaur Train** (PBS Kids TV series, 2009–). Supports: a friendly kids'-science tone, many clades side by side
   with big expressive eyes, a bright but natural palette, simple valley settings. Runs out: it is soft-shaded CG,
   not flat cel colour with outlines, and its theropods often stand upright with palms-down hands, which this style
   forbids.
2. **Bluey** (TV series, 2018–). Supports: flat cel colour with one soft shade tone, rounded chunky shapes, sunny
   simple backgrounds with paler depth, gentle family pacing. Runs out: dogs, not dinosaurs; thin or no outlines; no
   anatomy guidance at all.
3. **Picture-book dinosaur illustration for young readers** (for example Ben Cort's chunky cartoon dinosaurs in the
   *Dinosaurs Love Underpants* books). Supports: thick dark outlines, glossy eyes with a white highlight, candy-bright
   colours on chunky bodies. Runs out: slapstick tone, upright tail-dragging poses and flat backgrounds; it gives the
   line and colour, not the body plans.

Anatomy (level back, tail counterweight, palms facing in, sauropod footfall order) comes from the science sources in
`README.md`, not from these works.

## Signature traits

| # | Tag | Trait (visible in a still frame) |
|---|---|---|
| 1 | must | Flat cel colour with one soft shade tone and a thick warm dark-brown outline of even width. |
| 2 | must | Real dinosaur body plans: two-legged dinosaurs with the back level and the tail straight out behind, ankles high above the toes; four-legged dinosaurs on straight pillar legs. |
| 3 | must | Rounded chunky shapes and big glossy eyes with one white highlight. |
| 4 | bonus | Sunny Cretaceous valley: pale sky, soft green hills, cycad and fern clumps, paler background plants for depth. |
| 5 | forbidden | Realistic, scary or 3D-rendered dinosaurs; upright "monster" posture with the tail dragging; museum-diorama look. |

**Nearest neighbour:** Style 3, prehistoric hand-drawn dark comedy (`prehistoric-dark-comedy.md`). Two visible
differences: (1) Style 3 has white-headed stick figures with black stick limbs; here every character is a full
filled body with a thick warm dark-brown outline and real dinosaur anatomy; (2) Style 3 is earthy with paper texture
and fire accents; here the frame is clean flat colour in sunny daylight, with no texture and no fire.

## Frozen style block (verbatim in every clip)

```text
Style and environment: a bright, friendly 2D cartoon dinosaur world for kids, like a modern picture-book TV cartoon. Flat cel colors with one soft shade tone, thick warm dark-brown outlines of even width, rounded chunky shapes, big glossy eyes with one white highlight. Sunny Cretaceous valley: pale sky, soft green rolling hills, cycad and fern clumps, warm sand-and-moss ground. Gentle depth: background plants slightly paler. Soft even daylight, short soft shadows under the feet. Clean, rounded educational cartoon; not photorealistic, not a museum diorama, not 3D.
```

## Character anchors and cast (verbatim wherever the character appears)

Each anchor holds design only: role, proportions, head, colours, markings, one right-side yellow band. Pose,
position and props live in the beats. Every pair of characters differs in at least two non-colour ways (body plan,
leg count, head shape, crest, frill, horns, tail fan).

**Lan**

```text
Lan, a 9-year-old girl explorer with a short dark ponytail, an olive-green bucket hat, an orange vest over a white T-shirt, brown shorts, a blue backpack and brown boots, a yellow wristband on her right wrist
```

**Bo**

```text
Bo, a huge gentle long-necked sauropod dinosaur, lavender with darker purple round spots and a pale lilac belly, a long smoothly curved neck and a small round head with sleepy kind eyes, four straight pillar legs with round padded hoof-like feet, a long tapering tail held off the ground, a yellow band around the right front ankle, no hands or fingers
```

**Mira**

```text
Mira, a small quick feathered raptor dinosaur, teal with a mint-white belly, a crest of magenta feathers on her head and a magenta feather fan at the tip of her long straight tail, big bright eyes, two long bird-like legs with three toes, short feathered arms with three-fingered hands, and a yellow band on her right wrist
```

**Tok**

```text
Tok, a young tyrannosaur-like dinosaur, coral-orange with darker orange back stripes and a cream belly, a big box-shaped head with a wide friendly grin, two strong bird-like legs with three toes, tiny two-fingered arms, and a yellow band on his right wrist
```

**Hoot**

```text
Hoot, a duck-billed crested dinosaur, sunflower-yellow with a cream belly and a long curved orange crest sweeping back from the head, a flat duck-like bill, two strong legs with three toes, short arms about half the length of his legs with small hoof-like finger pads, and a yellow band on his right wrist
```

**Tuk**

```text
Tuk, a stocky three-horned frill dinosaur, sky-blue with a pale-blue belly, a coral-orange neck frill with cream spots, two short brow horns and one nose horn, a parrot-like beak, four short sturdy legs with round hoof-like feet, a yellow band around the right front ankle, no hands or fingers
```

Lumo (stegosaur-like, four legs, orange back plates) is in the cast and gallery but not in the sample story, so it has
no frozen anchor yet; write one in the same pattern before its first clip.

Body block, repeated after the anchors in every clip:

```text
Every dinosaur keeps its body plan in every frame: two-legged dinosaurs walk with the back level and the tail held straight out behind as a counterweight; four-legged dinosaurs always stand and walk on four straight pillar legs. Two-legged dinosaurs hold their hands with the palms facing each other, never palms down. Legs bend at the ankle high above the toes like a bird's. Tails never drag on the ground. Each yellow band stays on the character's right side only. Lan has exactly two arms and two legs, and her arms hang outside her body with a clear gap. A moving limb replaces its previous pose; limbs keep their length and bend smoothly at elbows, knees and ankles. Bodies never split, merge, melt or change color.
```

Model sheets: `gallery/sheet-*.png`. The two-legged dinosaurs' middle view is a three-quarter front view built from
the side rig (head toward the camera, body and tail behind it): a straight head-on drawing of a level-backed animal
read as an upright teddy bear. The front gate tracks still check the straight front joints.

## Core rules this style overrides

1. **Hands lines for animals without hands.** Bo and Tuk have no hands; their front hooves stand in for hands in the
   `Hands at start` / `Hands at end` lines ("Bo: right front hoof empty; left front hoof empty.") so the ledger and
   the model both track them. Hooves never hold props; the mouth never carries props in this style (the ledger cannot
   track a mouth).
2. **Posture limits.** Dinosaur tracks widen the gate's human hip range (−40…175°) and ankle range (−100…85°): a
   level-backed animal is bent at the hip all the time and its ankle is the high intertarsal joint. Everything else
   stays human-strict, and `dino_rules.py` adds the dinosaur limits (neck curve, snout direction, footfall order,
   pillar front legs, tail off the ground).
3. **Music.** The score is a light marimba-and-ukulele melody, not the catalog's piano: it keeps the kids'-science
   tone and stays under the narrator.
4. **Faces.** Dinosaurs have side-set eyes and long snouts; at any handoff the dinosaur lifts its head high first so
   the snout cannot reach the other character's face.

## Text policy: none

No words, letters, numbers, labels or signs in any frame. Titles and captions go in the video's metadata or thumbnail,
not in the picture.

## Motion cadence: smooth

Full 24 FPS motion. Quadruped moves stay slow and short, one gait per beat; write the sauropod footfall order into the
beat when the walk matters.

## Camera moves

- Transition moves: hold, slow push-in, slow pull back, slow lateral track, slow pan. A slow tilt up is allowed only
  for a scale reveal (a giant foot, then up the neck) while nobody is doing a demanding move.
- Accent moves (a short camera shake on a giant footfall is the only one that fits): at most one per clip and in at
  most one clip in three; never during a handoff, a run, a jump or a dinosaur going down onto its hands.
- No three inward moves in a row; hold the camera during demanding body actions. Every beat names its move.
- Side-on, full-body framing for walks: video models confuse the left and right legs of animals seen from the side.

## Style bans and posture limits

- Never: extra or missing legs, legs merging or swapping, a four-legged dinosaur on two legs, a two-legged dinosaur on
  four unless the beat says so, tails dragging, palms-down "bunny hands", a neck kinked or a head hooked under the
  neck, a snout poking another character's face, a band on the left side.
- The rig cannot do: a sauropod rearing up, a ceratopsian or stegosaur sitting up, a theropod scratching its head
  (arms too short), anything carried in a mouth.
- Shared negatives, verbatim in every clip:

```text
Negative constraints: no other dinosaurs or people, no crowds, no famous movie or toy dinosaur designs, no realistic or scary dinosaurs, no teeth-baring attacks, no blood, no 3D render, no photographic textures, no anime or manga eyes, no extra legs, no missing legs, no legs merging or swapping places, no quadruped standing on two legs, no two-legged dinosaur walking on four legs unless the beat says so, no tail dragging on the ground, no palms-down 'bunny hands', no extra arms, no third hand, no band on the left side, no duplicate characters, no knees or elbows bending backward, no limbs changing length, no neck kinking or folding, no head turned past the shoulders, no swapped left and right hands, no prop switching hands without a visible pass, no hand covering the face, no snout poking into another character's face, no morphing or melting bodies, no visible text, letters, numbers or labels, no speech bubbles, no dialogue boxes, no logos, no watermark.
```

## Voice and music

Narrator: the project's shared male narrator block, verbatim (`Voice:` line in the package); the style never recasts
it and dinosaurs never speak. Frozen score line, clip 1:

```text
Audio: a light marimba-and-ukulele melody; a deep soft thump at 1.5s with a little rattle of pebbles; slow heavy padded footsteps.
```

Clips 2–N open their audio line with: `Audio: the identical light marimba-and-ukulele melody from clip 1 continues, same tempo and instrumentation;` then the clip's own sound effects. "Ends on a warm held chord"
may follow in the last clip.

## Opening hooks that fit

Scale shock (a tiny thing, then a giant foot lands beside it), partial reveal (only a foot, a tail tip or a shadow,
then the tilt up), sudden entry (Mira darts in holding something), mystery object (a footprint, a cracked egg, a seed
cone). Loudness: the hit is a deep soft thump with a little pebble rattle, below the narrator's level; never a roar,
a jump scare or a sting.

## Post-production

1. Stitch the clips with hard cuts; no transitions or overlays (text policy none).
2. Level the narrator to one loudness across clips; duck the score under it; keep footfalls below the voice.
3. Before accepting a clip, check its risky moments frame by frame: clip 1 Bo's footfall order (7–10 s), clip 2 the
   seed-cone handoff (3–7 s), clip 3 Hoot going down onto his hands and back up (0–7 s). Count legs and check the
   yellow band is on the right in each.
4. Trim a clip's last frames rather than regenerate when only the tail end morphs.

## Sample package

`samples/dino-world.md` ("Whose footprint?", 3 clips): built by `src/make_package.py` from the blocks above.
`package_lint.py` with the shared hand ledger: see [`prompt-package/lint-output.txt`](prompt-package/lint-output.txt),
facts in [`samples/dino-world.facts.md`](samples/dino-world.facts.md). Ledger mutation tests:
`prompt-package/ledger-tests.md`.

## Acceptance checklist

- [ ] Leg count right in every frame (2 or 4), legs never merge or swap.
- [ ] Quadruped front legs straight while planted; sauropod footfall order lateral sequence.
- [ ] Two-legged dinosaurs: back level, tail off the ground, palms facing each other.
- [ ] Necks curve smoothly; no head hooked under the neck.
- [ ] Yellow band on the right side of every character, every shot.
- [ ] Props stay in the hand named by the hands lines; passes are visible.
- [ ] No snout through another character's face at a handoff.
- [ ] No text, no franchise look-alikes.

## Catalog entry (ready to paste)

Style matrix row:

```text
| **dino-world** | Dino World | Sunny Cretaceous valley, flat cel colour with one soft shade, thick warm dark-brown outline | Kids' dinosaur science, fossils, "how do we know?" stories | Original cartoon dinosaurs with real body plans (level back, tail counterweight, pillar legs), one yellow band on the right, plus kid explorer Lan |
```

Status row: `| dino-world | gated | Posture gate + dino rules (gallery/gate-v2.txt, motion-test/scene-gate-v2.txt); package_lint facts (samples/dino-world.facts.md) |`

Setup-gate line: `dino-world (gated, experimental): kids' dinosaur science with original cartoon dinosaurs; offer only when the user asks for an experimental style.`
