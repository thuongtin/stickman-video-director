# Mid-Century Limited Animation

> In this repository: the sample package and its lint facts are `samples/mid-century.md` and `samples/mid-century.facts.md`. Other research files named below (gallery, tracks, gate output, renderer) stay in the project's `style-research/mid-century/` folder and are not part of the skill.

Slug: `mid-century`. Number it only when it is merged into `style-catalog.md`.

```text
Status: gated (2026-10-20). Covers: 3 clips, a cast of five office characters with up to three in one clip, two hand-to-hand folder passes, office interiors, 16:9.
Not covered: 9:16, crowds, outdoor or night scenes, character dialogue. Not tried on Flow.
```

Evidence: 35 rig poses and a three-shot animatic pass `posture_gate.py` (per track and `--scene`), the sample package passes `package_lint.py` (facts block below). Gallery, gate output and before/after sheets: `gallery/`, `motion/`, `cast/` next to this file.

## Visual identity

1950s mid-century modern cartoon animation: angular geometric characters, flat unshaded colour shapes printed a little off-register from a thin wobbly near-black ink line, sparse sets built from flat colour fields, and limited animation with held key poses. Every character keeps the skill's stick-thin limbs of constant length; the torso and head carry the design.

Use it for satirical explainers, workplace and money topics, retro public-information pastiches, and stories with a small ensemble of types. It is a poor fit for calm, intimate or cinematic stories; use Style 4 or 2B there.

Frozen style paragraph, verbatim in every clip:

```text
1950s mid-century modern limited animation. Flat colour shapes, lightly grainy, printed a little off-register from a thin, slightly wobbly near-black ink line, so each fill sits a few pixels up and to the right of its outline. Angular geometric character designs in flat unshaded colour, one colour per shape with no shadow tones, on sparse sets of flat colour fields with a little sponge texture on the walls; no gradients, no soft shading, no 3D. Limited animation on twos: each character holds a clear, balanced key pose, then moves through one in-between drawing into the next key pose; while a pose is held, only the face or one arm moves. Palette: warm cream paper, mustard, teal, coral, olive, charcoal, with brick red as the accent.
```

## Signature checklist

### Sources

Frame study, 2026-10-20: four public-domain-marked prints downloaded from the Internet Archive, 24 evenly spaced frames per film pulled with ffmpeg into contact sheets, plus full-size frames at the timecodes below and a duplicate-frame count for the drawing rate. Contact sheets and study frames: `research/` next to this file (study copies only, never shown to a model or used in prompts).

- *Gerald McBoing-Boing* (1950), https://archive.org/details/gerald-mc-boing-boing-1950 (`research/contact-gerald.png`; frames 00:00:52, 00:01:26, 00:02:54 in `research/study-1950-1951.png`). Confirms trait 1: the pink armchair, the rug and the mother's dress are colour patches that sit off their black line or stop short of it. Confirms trait 2: tall angular parents with thin tapering limbs, a block-shaped butler. Confirms trait 3: furniture and lamps are drawn as line only, with hairpin and scroll legs, on one flat colour field with no floor line. **Contradicts trait 4**: no character has a shadow tone; every shape is one flat colour. Confirms trait 5: no gradients. The line is near-black, not brown, and character fills are smooth, not grainy.
- *Rooty Toot Toot* (1951), https://archive.org/details/rooty-toot-toot-1951 (`research/contact-rooty.png`; frames 00:02:32 and 00:03:29). Confirms trait 1: the red hat fill spills past its line. Confirms trait 2: elongated angular figures on thin legs. Confirms trait 3, with a correction: the walls are sponge-textured colour fields, with furniture in line on top. **Contradicts trait 4**: the white-suited figure and the woman in red are unshaded; contrast comes from colour blocking (a white figure on a dark field). Confirms trait 5.
- *Gerald McBoing! Boing! on Planet Moo* (1956), https://archive.org/details/gerald-mc-boing-boing-on-planet-moo-1956 (`research/contact-moo.png`; frames 00:00:36 and 00:05:40). Confirms trait 2: block-bodied figures on thin legs. Confirms trait 3: a flat pink ground with a skyline of flat blocks, and starbursts in the space scenes. **Contradicts trait 1 for later work**: fills sit on register. **Contradicts trait 4**: unshaded. Confirms trait 5. Motion cadence: a dialogue stretch from 00:02:20 changes drawing every second frame at 24 fps (on twos) with held frames between.
- *Destination Earth* (1956), https://archive.org/details/1956-destination-earth-04 (file "1956 - Destination Earth_04.mp4"; `research/contact-dest.png`). Confirms trait 3: boomerang and atomic-antenna shapes, flat colour blocks, starbursts. Shows two-tone shadows on a few props and cars, but none on the characters, so it does not rescue trait 4. Fills are on register (trait 1 again an early-1950s mark).
- Not looked at: *Toot, Whistle, Plunk and Boom* (1953) (no study copy found); Amid Amidi, *Cartoon Modern* (2006), kept only as further reading.

What changed from the study: trait 4 is now "unshaded, one colour per shape" (none of the four films shades a character with a darker slab), the frozen style paragraph says "near-black" ink, "flat unshaded colour" and "a little sponge texture on the walls", and the rig no longer draws the torso shadow slab. Trait 1 stays a must because it is what marks the early films, but the study shows it fading by 1956. The 1950 and 1951 drawing rate could not be measured cleanly: the prints are telecined and pans read as change.

The sources run out on two points: how a 2026 video model renders "off-register" fills, and whether it holds poses instead of tweening smoothly. Neither has been tested. Nothing here copies a character, prop or layout from these works, and prompts name no studio, film or artist.

### Five signature traits

| # | Trait (visible in a still frame) | Tag | Prompt wording (in the frozen style paragraph) |
|---|---|---|---|
| 1 | Flat colour fills shifted a few pixels off their thin wobbly near-black ink outline | must | "Flat colour shapes, lightly grainy, printed a little off-register from a thin, slightly wobbly near-black ink line" |
| 2 | Angular geometric bodies (trapezoid, A-line, block, triangle, diamond) on stick-thin limbs | must | "Angular geometric character designs" plus each anchor's named torso shape and "stick-thin legs" |
| 3 | Sparse sets: flat colour fields with a little sponge texture, line-drawn hairpin-leg furniture, starburst and boomerang shapes | bonus | "sparse sets of flat colour fields with a little sponge texture on the walls" plus each clip's set sentence |
| 4 | Characters unshaded: one flat colour per shape, no shadow tone; contrast from colour blocking | bonus | "flat unshaded colour, one colour per shape with no shadow tones" |
| 5 | Gradients, airbrushed shading, 3D volume or round rubber-hose limbs | forbidden | "no gradients, no soft shading, no 3D" and the negative list |

### Nearest neighbour

`paper-cutout` (gated) is the closest: both use flat shapes and limited motion. Visible differences: mid-century draws a thin ink outline with the colour printed off-register, where paper-cutout has no ink line and layered paper with cast shadows; mid-century limbs are single stick lines, where paper-cutout limbs are cut-paper pieces pinned at visible joints. `flat-vector` is further away: clean vector fills on register, smooth tweened motion.

## Cast cards

The style is an ensemble style. Plan the cast as types from one world and give each a different geometric silhouette; two characters with the same body shape merge in generated clips. Each anchor names role and build, head shape and face marks, hat or hair, torso shape and outfit colour, legs and shoes, mitten hands, and **one fixed left/right marker**. The marker shows which hand is the character's own right (untested on Flow). Repeat every visible character's full card verbatim in every clip it appears in. Names in Hands lines have no periods ("Boxley", not "Mr. Boxley").

**Wendell**

```text
Wendell, a very tall thin office clerk: a tall slab-shaped head with a long jaw and a big triangular nose, dot eyes and floating thick eyebrows, a small olive porkpie hat with a brick-red band, a mustard suit jacket shaped like an inverted trapezoid with broad square shoulders and a thin brick-red tie, charcoal trousers on long stick-thin legs, pointed black shoes, round mitten hands with a small thumb, and a small teal wristwatch on his left wrist.
```

**Boxley**

```text
Boxley, a short wide boss: a large bald egg-shaped head with three combed-over hairs, a big black moustache, a wedge nose and floating thick eyebrows, a boxy charcoal suit shaped like a block with a small brick-red bow tie and a brick-red pocket square on his left chest, charcoal sleeves edged by a thin cream gap so his arms always read apart from the jacket, short stubby legs, black shoes, round mitten hands with a small thumb.
```

**Marge**

```text
Marge, a sharp office secretary: a small square head with angular cat-eye glasses and a tall plum-coloured beehive hairdo, a teal A-line dress with narrow shoulders and a wide hem, short sleeves, thin dark stick legs, red pumps, round mitten hands with a small thumb, and a mustard bangle on her right wrist.
```

**Tilly**

```text
Tilly, an eight-year-old girl: a big rounded head with freckles, dot eyes and two brown pigtail bunches, a coral triangle dress, thin dark stick legs with a small white plaster on her right knee, navy shoes, round mitten hands with a small thumb.
```

**Hank**

```text
Hank, a tall mail-room runner: a square-jawed head with a navy cap and black brim, an olive uniform jacket with a barrel chest shaped like a diamond, a brown satchel strap running from his right shoulder to his left hip, navy trousers, brown shoes, round mitten hands with a small thumb.
```

Shared body rule, once per prompt after the cards:

```text
Every character keeps exactly two arms and two legs drawn as thin stick limbs of constant length; a moving limb replaces its previous pose. Resting arms hang slightly away from the body, drawn outside the outline of a wide skirt, dress or jacket, never painted over it. Expressions change only the eyebrows, eyes and mouth, never the head shape, hat, hair, outfit or proportions.
```

## Core rules this style overrides

- **Idle ban (prompt contract: never leave a character idle).** Held poses are the style; a hold counts as action when the face or one arm moves, and no hold runs longer than about one second without a change. Reason: limited animation reads through holds, and the gate showed held poses must be balanced, not that they must move.
- **Opening hook.** Prefer Sudden entry, Reaction before cause and Visual metaphor; the hook hit is a held surprise pose landing on one hard sound, no beat drops. Reason: the take is the style's native hook.
- **Location per segment (Style 4 habit).** New clips move to another room of the same world (office, typing pool, mail room) connected by a travelling prop. Reason: the ensemble needs one world; different rooms keep sets readable.
- **Faces.** Expressions use floating eyebrows, dot or wide eyes and simple mouths only; never realistic faces. Reason: the geometry of the head is the identity.

## Text policy: `post-overlay`

No signs, labels, numerals, lettering or clock numerals in any generated frame (the starburst clock has a blank face). Titles and captions are added in post-production.

## Motion cadence: `on-twos`

Each character holds a clear, balanced key pose, then moves through one in-between drawing into the next key pose. Rules from gating 35 rig poses and the three-shot animatic (draft keys: 9 of 35 tracks failed, every failure from a limited-animation habit):

- Every pose change passes through one in-between. A snap into a take is a pop the gate blocks and the motion a video model renders as a teleporting limb. Write "moves through one in-between into", never "snaps".
- A held pose must be balanced: feet under the body, or a named support ("both hands land on the desk"). Bows stay within about 45 degrees with the hips bent.
- Front-view squats open the knees outward over the toes (a diamond shape), never bow-legged.
- Exaggerate with arms, head and timing, not stride: scaled leg angles push the standing foot behind the body, and a scaled arm swing drawn on twos makes the wrists land on each other's spots.
- Short arms cannot reach over a big head: children and big-headed types throw their arms up and out in a V, or lift props forward in front of the face.
- Mirroring changes the near arm: re-check a pose for the arm crossing the face when the character faces the other way.
- In a hand-to-hand pass, both hands are on one prop position for one held drawing; then the giver lets go.
- Gate assembled shots (`posture_gate.py check --scene`), not only single poses.

## Camera grammar

Follow `storyboard-template.md`. Side-on stage staging and full-body framing; name one move per beat. Default to holds, a lateral track for walks, one slow push-in or pull back per clip. At most one accent per clip (a fast push-in to a close-up on a key prop), in no more than one clip of three. No orbit or camera shake during a take or a pass.

## Style bans and posture limits

The rig cannot do: arms overhead for Tilly-sized characters, bows past 45 degrees, leans past the feet in a held pose, a limb change without an in-between. Negative list, verbatim in every clip:

```text
no 3D render, no CGI, no gradients or soft airbrushed shading, no realistic anatomy or faces, no anime style, no thick rubber-hose limbs, no extra arms or legs, no duplicate characters, no unintended extra people, no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no prop switching hands without a visible pass, no limb jumping to a new position without an in-between, no held pose leaning past the feet, no visible text, letters or numbers, no clock numerals, no speech bubbles, no dialogue boxes, no watermark, no logos
```

## Music

One frozen score per video: a brisk muted-trumpet, walking upright-bass and brushed-snare jazz theme, established in clip 1 and restated word for word in clips 2 to N ("the identical brisk muted-trumpet, walking upright-bass and brushed-snare jazz theme from clip 1, same tempo and instrumentation"). Slide whistle and wood-block hits on takes. Keep the frozen voice block from `voice-continuity.md`.

## Post-production

1. Trim each clip on its last clean held pose; check pass frames for a doubled or vanishing prop before joining.
2. Short audio crossfade (about four frames) for the score at each cut; never crossfade the voice.
3. Add titles and captions as overlays (text policy `post-overlay`).
4. Optional: a light paper-grain overlay and a single colour grade across all clips, if the clips drift in paper tone.
5. Review takes, slams, bows and passes frame by frame for popping limbs, swapped hands and the left/right markers changing sides; record what Flow kept.

## Sample package

[`samples/mid-century.md`](samples/mid-century.md): 3 clips, 5 characters, two hand-to-hand passes, opening hook, Hands lines for every character, global continuity block, stitching guide and voice/music note. Facts block from `package_lint.py package.md --clips 3 --facts`:

<!-- package_lint facts: generated, do not edit -->
- package: `package.md` sha256 bb3fc4e697ea78eb
- checked: 2026-10-20
- storyboard rows: none
- prompts: 3
- hand_ledger: PASS
- red: 0
- yellow: 0
<!-- package_lint facts end sha256=43a1054d5daa3df1cff3012758d03b5ef85aa1346bdd3927975a448e62ada2d1 -->

## Catalog entry (ready to paste)

Style matrix row:

```text
| **mid-century** | 1950s Mid-Century Limited Animation | Sparse sets of flat colour fields with a little sponge texture, line-drawn hairpin-leg furniture, starburst and boomerang shapes; flat unshaded fills printed slightly off-register from a thin near-black line; held poses on twos | Satirical explainers, workplace and money topics, retro public-information pastiches, small ensembles of character types | Original office cast with angular geometric torsos (trapezoid, A-line, block, triangle, diamond) on stick-thin limbs, one fixed left/right marker each |
```

Status row:

```text
| mid-century | gated | 35 pose tracks and a 3-shot, 5-character animatic pass the posture gate (per track and --scene); sample package passes package_lint and hand_ledger; frame study of 4 period films (style-research/mid-century) |
```

Setup gate line (offered only when the user asks for an experimental style):

```text
  - `mid-century (1950s Mid-Century Limited Animation)`: experimental, gated, not tried on Flow; original angular office cast on stick-thin limbs, flat off-register colour, sparse sets, held poses on twos
```

## Checks before delivery

- Each character has a distinct silhouette, a full verbatim card in every clip it appears in, and its left/right marker.
- Beats describe key poses and in-betweens; no "snap", "instantly" or "freeze-frame" limb moves; each beat names its camera move.
- Held poses have feet under the body or a named support; every pass shows both hands on the prop for one drawing.
- `package_lint.py` passes with a facts block; `hand_ledger.py` passes; names have no periods.
- No text, numerals or signage in sets or props; no logos.
