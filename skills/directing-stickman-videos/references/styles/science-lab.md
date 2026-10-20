# Science Lab Explainer (style pack, slug `science-lab`)

> In this repository: the sample package and its lint facts are `samples/science-lab.md` and `samples/science-lab.facts.md`. Other research files named below (gallery, tracks, gate output, renderer) stay in the project's `style-research/science-lab/` folder and are not part of the skill.

```text
Status: gated (2026-10-20). Covers: 3 clips, 4 characters on screen (Dr. Nova, Kip, Bolt, Prof. Otto),
pouring, a cup picked up and set back, a two-hand to one-hand beaker handoff, a kid jump in profile, 16:9.
Not covered: 9:16, Juno and Dr. Rocco on screen, sitting at the microscope, turns while carrying glass,
more than four characters, outdoor scenes. Not tried on Flow.
```

Evidence for `gated`:
- Pose gate: `gallery/gate-v2.txt` and `gallery/gate-output-v2.txt`, 43 tracks.
- Motion test, with `--scene`: `motion-test/gate-v2.txt` and `motion-test/gate-v2-cli-scene.txt`.
- Package lint facts: [`samples/science-lab.facts.md`](samples/science-lab.facts.md), from `tools/package_lint/package_lint.py samples/science-lab.md --clips 3 --anchor <style block> --facts samples/science-lab.facts.md`.
- Lint and hook output: `prompt-package/lint-output.txt`.
- Hand ledger: `prompt-package/ledger-output.txt`.

A bright flat 2D Saturday-morning science cartoon. A recurring team of original scientists explains one concept per video through a hands-on demo in a school lab. Use it for science and how-it-works explainers aimed at curious kids and families. It fits poorly with satire, workplace stories or cinematic mood pieces; use Style 4 or mid-century there.

## Sources (never paste into prompts)

Studied from general knowledge of the genre, not frame by frame. Treat every claim as a recollection, not a measurement.

| Work | What it supports | Where it runs out |
|---|---|---|
| Bill Nye the Science Guy (PBS, 1993–98) | A host who does the experiment with their own hands, a fast reveal, a lab-coat team, a kid-safe demo per episode | Live action. It says nothing about drawing, and its host's look (bow tie, blue coat) must not be borrowed |
| The Magic School Bus (1994–97) | A recurring ensemble of distinct kids and a teacher, one concept per episode, bright flat cel colours | Its fantasy field trips and its teacher's patterned dresses are out of scope; our demos stay in a real lab |
| Dexter's Laboratory (1996–2003) | Thick even outlines, flat fills, a lab full of glassware read as shapes, a kid scientist's comic reactions | Its sci-fi lab machines and its boy-genius design are trade dress to avoid; our lab is a school lab |
| Sid the Science Kid (PBS, 2008–13) | Science as asking and testing, a warm group of mixed ages | CG rendering, so it supports content only, not the look |

## Signature traits

1. `must`: one clean dark-navy outline of steady weight around every shape, flat solid fills, no gradients or soft shading.
2. `must`: every human wears an open white knee-length lab coat over coloured clothes, with safety goggles on the forehead.
3. `must`: a mint-green school lab with pale tiles and shelves of plain round flasks and straight beakers holding pink, green and blue liquids.
4. `bonus`: the only depth cue is that the arm and leg turned away from the viewer are one shade darker.
5. `forbidden`: any writing in frame. That covers formulas, equations, labels on glassware, scale marks with numbers and chalkboards of text.

## Nearest neighbour

Style 4 (Cozy Storytelling) is the closest style. Two visible differences:
- Science-lab characters have skin tones, hair or headwear, costumes and full cartoon faces with pupils. Style 4 uses white round heads and dark stick limbs.
- Science-lab keeps one recurring lab set, with lab glassware and props at the centre of every beat. Style 4 changes location every clip.

The whiteboard-doodle explainer ("Đậu") shares the teaching purpose. It is a marker drawing on white, with no colour fills and no set.

## Frozen style block

Paste this verbatim in every clip. `make_package.py` holds the source of truth.

```text
Style and environment: a bright flat 2D Saturday-morning science cartoon. Clean uniform dark navy outlines of one steady weight around every shape, flat solid colors with no gradients, no textures and no soft shading; the arm and leg on the side turned away from the viewer are one shade darker than the pair facing the viewer. A cheerful mint-green school lab with tall pale tiles, simple shelves of round flasks and straight beakers holding pink, green and blue liquids, a white wall chart showing only a picture of an atom with three orbits, and a long grey-blue lab bench. Even, bright, shadowless lighting. Every glass container is plain, with no labels, scale marks or writing.
```

The body block goes after the character anchors. Leave out the Bolt clause in clips without Bolt, so that it does not summon him.

```text
Every character has exactly two arms and two legs and round mitten hands with a thumb; a moving limb replaces its previous pose. Limbs keep their length and bend smoothly at elbows and knees. Each character wears a yellow band on the right wrist only, which never moves to the left wrist. Human faces have round white eyes with black pupils, simple line eyebrows and a line mouth; Bolt's screen face keeps its cyan eyes and mouth. Expressions change only the eyes, eyebrows and mouth, never the head shape, hair, goggles, clothing colors or proportions.
```

Never write "far arm" or "near hand" anywhere, the style block included. `hand_ledger.py` rejects them because they flip when a character turns.

## Character anchors and cast cards

Adults are about 4.5 to 5 heads tall; Kip and Bolt are about 3.5. The silhouette differences sit in the head: hair puff, bald tufts, braids, spiky hair, hard hat, robot screen. Every character wears a yellow band on the right wrist only, as a fixed left/right marker.

- **Dr. Nova** (chemist, lead): deep brown skin, big round curly hair puff, purple goggles, teal shirt, purple trousers, orange sneakers.
- **Prof. Otto** (physicist, elder): short and round, bald with white side tufts, white walrus mustache, round glasses, red bow tie, brown trousers.
- **Juno** (teen biology student): two long black braids, green headband and goggles, yellow shirt, blue jeans, green sneakers.
- **Kip** (10-year-old assistant): spiky ginger hair, freckles, orange goggles, oversized coat with rolled sleeves, red T-shirt, navy shorts.
- **Dr. Rocco** (geologist): broad, short black beard, orange hard hat with headlamp, blue shirt, khaki trousers, brown boots.
- **Bolt** (lab robot): silver, rounded-square head with a dark screen face (cyan oval eyes, cyan line mouth), antenna with a red ball, blue chest light, blue boots, yellow ring on the right wrist.

Frozen full anchors, pasted verbatim into every clip where the character appears (the source is `src/rig.py`, `CAST[..]["anchor"]`):

```text
Dr. Nova: a tall cheerful chemist woman with deep brown skin and a big round dark curly hair puff on top of her head, purple safety goggles pushed up on her forehead, an open white knee-length lab coat over a teal shirt, purple trousers, orange sneakers, and a yellow wristband on her right wrist.
Prof. Otto: a short round elderly physicist with light skin, a bald head with two fluffy white tufts above the ears, a big white walrus mustache, round black glasses, a red bow tie on a white shirt, an open white knee-length lab coat stretched over a round belly, brown trousers, brown shoes, and a yellow wristband on his right wrist.
Juno: a teenage biology student with tan skin and two long black braids, a green headband with green safety goggles pushed up on top of it, an open white lab coat over a yellow shirt, blue jeans, green sneakers, and a yellow wristband on her right wrist.
Kip: a ten-year-old lab assistant boy with light skin, freckles and short spiky ginger hair, big orange safety goggles pushed up on his forehead, an oversized white lab coat reaching below his knees with the sleeves rolled up to the elbows, a red T-shirt, navy shorts, red sneakers, and a yellow wristband on his right wrist.
Dr. Rocco: a big broad-shouldered geologist with warm brown skin and a short thick black beard, an orange hard hat with a small round headlamp, an open white lab coat over a blue shirt, khaki trousers, brown boots, and a yellow wristband on his right wrist.
Bolt: a small friendly silver lab robot about as tall as Kip, with a rounded-square head whose dark screen face shows two glowing cyan oval eyes and a cyan line mouth, one short antenna with a red ball, a rounded silver body with a round blue chest light, jointed silver arms with round grey hands, short legs with blue boots, and a yellow ring on its right wrist.
``` Keep design out of the anchors' poses, positions and props; those go in First frame, Hands lines and beats.

Originality: the cast is our own. Do not add a bow tie and blue coat to a host, a patterned dress to a teacher, or purple gloves, black boots and a neat side part to a small lab boy. Kip is a freckled ten-year-old assistant with spiky hair, rolled sleeves, shorts and bare hands, not a genius inventor, and he never runs the lab alone.

## Core rules this style overrides

| Core rule | Override | Reason |
|---|---|---|
| No facial features (pupils, realistic eyes, lips) unless approved | Round white eyes with black pupils, line brows, a mouth that opens with a tongue | Explainers live on reaction shots (surprise, eureka, worry), and twelve expressions are drawn and checked in `gallery/expressions.png` |
| No hair unless approved | Hair and headwear are the main identity cue | Six characters share one white coat, so the head carries the silhouette difference |
| Monochrome or limited accents (Styles 1–2A) | Full flat colour: skin tones, clothes, three liquid colours | The liquids' colour is the science (colour change, foam) |
| Stick limbs | Filled limbs with coat sleeves and trousers | The coats and the lab glassware need volume to read |
| (added) | Lab-safety bans: no flames, explosions, smoke clouds, tasting or sniffing, nothing near the mouth; goggles always present | The audience is kids; every frame models safe practice |

## Text policy

`post-overlay`. Generated frames carry no words, letters or numbers. Terms ("catalase", "oxygen") and numbers ("3%") are added in post from the approved VO script, never in the prompt.

## Motion cadence

`smooth` (24 FPS full motion). The posture test renders at 12 FPS only for the gate. Reactions use a held key pose of about half a second (foam rising, eureka finger) instead of constant motion.

## Camera moves

These follow the camera grammar in `storyboard-template.md`.

- **Transition moves** are hold, slow push-in, slow pull back and slow lateral track or pan. Use them by default.
- **Accent move:** at most one fast push-in, used only on the reveal or punchline, in no more than one clip in three. The hook clip may add one more.
- **Hold the camera during demanding body actions:**
  - a pour or a hand-off;
  - a two-hand lift or a kid jump;
  - sitting down at the microscope.

  Move before or after the action, never during it.
- No shake, orbit or tilt near glassware.
- Do not push in three clips in a row.

The sample package's moves per clip:
- Clip 1: hold, then a slow pull back, then hold.
- Clip 2: hold, then a slow track right with Bolt, then hold.
- Clip 3: a slow push-in on the foam, then hold during the hand-off and the jump.

## Style bans and posture limits

Shared posture negatives, verbatim in every clip:

```text
no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no prop switching hands without a visible pass
```

Lab work and the hands:
- Lab work means two props in two hands: flask and beaker, pipette and dish, or cup and bench edge. Name both hands in the beat, one character per sentence. Every such gallery pose failed its first draft because the hands stopped short of the props.
- Every prop picked up inside a clip needs its own set-down sentence, for example "sets the small yellow cup back on the metal tray with her left hand". The shared `hand_ledger.py` now flags a missing set-down, but write it anyway: the model needs the beat.
- Point with the free hand. A character holding a flask in the right hand points with the left index finger. The shared ledger now flags pointing with a busy hand.
- A hand-off is its own beat: who holds out, which hand receives, and that the giver's hands are now empty. A receiver bending toward a short character says so in the beat.

Keeping the face clear:
- Held instruments stay off the face. A magnifier hovers over the specimen. A test tube is held up at arm's length in front of the eyes, not between the eyes and the viewer. A plant pot stays at chest height. The gate does not check props in front view or a prop's far end.
- Kid jump in profile: both fists pump low in front of the chest. Kip's arms are shorter than his head is tall, so a fist raised overhead hides behind the head in profile, and the camera-side one would cross the face (gallery pose `kip_jump_side`, gated). A front-view jump may raise both arms (`kip_jump`).
- Front view: the shoulders stay at the torso edge, with a gap between a hanging arm and the waist.

Style bans: photorealism, 3D or CGI, gradients, glossy highlights, anime or manga eyes, extra scientists or crowds, flames, explosions, smoke clouds, chemical formulas, equations, labels on bottles, scale marks with numbers, visible text, speech bubbles, dialogue boxes, logos or watermarks.

## Voice and music

The narrator is the frozen General American female block in `samples/science-lab.md`. It comes from the shared voice contract and is never recast by this style.

The frozen score, set in clip 1:

```text
light bubbly pizzicato strings around 110 BPM with soft popping bubble sounds; keep the voice dominant.
```

Clips 2–N say "continue the identical light bubbly pizzicato strings from clip 1, same tempo and instrumentation". The SFX palette is fizzing whooshes, glugs, clinks, pops and bright chimes, never an explosion.

## Hook overrides

The hook patterns that suit this style:
- Reaction before cause: someone braces and the reaction erupts at about 1.5s.
- Physics break: a liquid does something unexpected.
- Satisfying motion: a clean pour or a colour change.

The sound cue is a fizzing whoosh, a pop or a bright chime.

## Post-production

1. Trim each clip at its beat boundaries and drop any frames where hands or glass pop.
2. Check every clip at the risky moments: the pour, the pick-up and set-down, the hand-off and the jump. Look for left/right hands, the yellow band on the right wrist and the glass staying whole.
3. Add the overlays: terms and numbers from the VO script as clean sans-serif labels near the demo. Add subtitles from the approved script, not from speech recognition.
4. Conform the music across the cuts with a short crossfade, then normalize loudness so the voice stays on top.
5. Add a short science note in the description, for example the one-line fact check from Phase A.

## Science and safety in Phase A

- The science must be right. Keep a one-line fact check for each demo. For the sample: yeast's catalase speeds the breakdown of hydrogen peroxide into water and oxygen, soap traps the oxygen as foam, and the kid-safe version uses 3% peroxide.
- Show safe practice in every frame:
  - goggles on the forehead at rest and over the eyes when a reaction is live;
  - coats on;
  - hands never near the mouth.

## Sample package

[`samples/science-lab.md`](samples/science-lab.md) is "The foam fountain": 3 clips, about 30 s, 16:9, four characters. Its results:
- `package_lint.py`: 0 red, 0 yellow. The facts are in [`samples/science-lab.facts.md`](samples/science-lab.facts.md).
- `verify-opening-hook.py`: passes.
- `hand_ledger.py`: passes.

## Catalog rows (ready to paste)

Style matrix:

```text
| **science-lab** | Science Lab Explainer | Bright flat 2D lab cartoon, steady navy outlines, mint-green school lab with coloured glassware | Science and how-it-works explainers for kids and families, hands-on demos | Recurring team of six original scientists in white lab coats and goggles, full cartoon faces, yellow band on the right wrist |
```

Status:

```text
| science-lab | gated | Gate and lint evidence in /mnt/project-files/style-research/science-lab/ (science-lab.md); not tried on Flow |
```

Setup gate (experimental styles only):

```text
  - `science-lab (Science Lab Explainer, experimental: gated)`: bright flat 2D lab cartoon with a recurring team of original scientists doing hands-on demos
```

## Acceptance

- No writing, formulas, labels or numbers appeared anywhere.
- Colours stayed flat, with no gradients, glow or 3D shading.
- Each character kept their hair or headwear, goggles colour, coat and proportions, and the yellow band stayed on the right wrist.
- Every held prop stayed in the named hand. Hand-offs and set-downs happened only in the named beat, and no one pointed with a busy hand.
- Safety held: goggles present, no flames or smoke, nothing near a mouth.
- For a code-rendered version (the rig in `src/`):
  - every track passes `posture_gate.py check`, and multi-character shots also pass with `--scene`;
  - the package passes `package_lint.py` and `hand_ledger.py`.
