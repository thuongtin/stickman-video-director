# Ink-Wash / Sumi-e (draft style pack, slug `ink-wash`)

> In this repository: the sample package and its lint facts are `samples/ink-wash.md` and `samples/ink-wash.facts.md`. Other research files named below (gallery, tracks, gate output, renderer) stay in the project's `style-research/ink-wash/` folder and are not part of the skill.

```text
Status: gated (2026-10-20). Covers: 3 clips on one riverbank, up to 4 characters per clip, a brush handoff
between two characters, a shoulder pole and a walking staff, 16:9. Not covered: 9:16, crowds, night scenes,
interiors, location changes.
```

Evidence for `gated`: 60 pose tracks (5 characters × 12) and two multi-character motion tests pass
`tools/posture_gate/posture_gate.py` (shared copy tracking PR #4, `--scene` for the motion tests), report in
`gate/gate-output.txt`; the sample package [`samples/ink-wash.md`](samples/ink-wash.md) passes
`tools/package_lint/package_lint.py`, facts block in [`samples/ink-wash.facts.md`](samples/ink-wash.facts.md) (copied
below).

## Visual identity

Traditional East Asian ink-wash painting brought to life as 2D animation: black ink brush strokes with
dry-brush streaks, soft gray washes with darker dried edges, misty layered mountains that fade into blank
paper, and a lot of empty rice paper. The only color is one small vermilion accent per character. Characters
are small inside wide, quiet landscapes; calm pacing, but every shot still has a concrete action.

Best for: reflective explainers, habits and mindset, craft and patience, folk-tale style stories, history-flavored
analogies. Not a claim about any real culture's history; settings are generic riverbanks, mountains, pines,
villages and boats.

## Sources

The frame study was done on 2026-10-20 from the stills below, each looked at one by one. Contact sheet:
[`sources/frame-study.jpg`](sources/frame-study.jpg). The film stills come from the Animation Obsessive article
"Animating Chinese Ink-Wash Paintings" (https://animationobsessive.substack.com/p/animating-chinese-ink-wash-paintings).
The painting comes from World History Encyclopedia, credited to the Tokyo National Museum. This is a handful of stills,
not whole films, so motion, timing and sound were not studied. *The Cowherd's Flute* (1963) was dropped because no
still of it could be reached. None of these names may appear in a spec.

| Work | Frames looked at | Confirms | Contradicts | Where it runs out |
|---|---|---|---|---|
| Sesshū Tōyō, *Splashed-ink Landscape* (1495, Tokyo National Museum) | Full scroll: https://www.worldhistory.org/img/r/p/1500x1500/10954.jpg | 1 (splashed and dry-brush strokes, gray washes); 2 (peaks fading into blank paper, most of the sheet empty); 3 (ink only; the one red is the seal) | 5: the painting carries a brushed signature and a red seal in the lower left | A still painting: no figures, no motion |
| *Feelings from Mountain and Water* (Shanghai Animation Film Studio, 1988) | Top row of https://substackcdn.com/image/fetch/$s_!Y30F!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd63cb5f-43e8-41cd-845b-1ce88eddeeae_2960x2166.png (the old master in profile; the master on a rock in mist). The pupil playing a flute: https://substackcdn.com/image/fetch/$s_!tzPu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2Febf017fb-b2ae-451a-a18e-c0a40a3c70c0_1309x660.png | 1 (black splashed-ink rock; gray mist washes with dried bloom edges); 2 (a tiny figure on a rock in a mostly empty frame). Figures have one fine dark brush contour over a pale wash robe | 3: robes and skin carry pale teal and pink tints, not pure gray. 4: faces are drawn with fine realistic lines, not an open circle and dot eyes | Figure proportions are realistic. Its elder (bald dome, back topknot, long beard) is the same archetype as Old Tung, so Old Tung keeps his own marks (white topknot ring, stoop, red gourd, staff) and copies nothing else |
| *Where Is Mama* (same studio, 1960) | Four stills (tadpoles among stems; a hen and chicks; goldfish; frogs on lily pads): https://substackcdn.com/image/fetch/$s_!ik7V!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F00afe214-0001-49a8-8d1a-a36ad1149781_2770x2114.png | 1 (creatures as soft wash blots with no outline; dry-brush stems); 2 (plain empty paper behind every subject) | 3: full colour (green leaves, red and yellow goldfish, pink lotus). 2: no mountains | The cast is animals only, so there are no human hands, props or handoffs |
| *The Deer's Bell* (same studio, 1982) | Bottom row of the 1988 still above (a girl kneeling with a fawn; a fawn on a cliff) | 1 (dry-brush cliff texture and wash) | 3: strong red, blue and yellow. 2: busy rock and foliage fill the frame | A coloured children's-book look. It is a counter-example: it shows how far the studio itself moved from monochrome |

What changed after the study:
- Trait 3 is now marked as this pack's choice: the films add pale tints, and only the monochrome painting supports it.
- Trait 4 is marked as our simplification, since no source draws faces this way.
- Trait 5 is explained as a production rule rather than a feature of the look.

The frozen style block was checked against the frames and still describes them, so the package did not change.

## Signature traits

| # | Trait (visible in a still) | Tag | Frame evidence |
|---|---|---|---|
| 1 | Black ink brush strokes with dry-brush streaks and gray washes with darker dried edges. Figures carry one fine dark contour, never a thick uniform outline | `must` | All four sources |
| 2 | Large calm areas of empty warm rice paper, with misty layered mountains fading into it | `must` | The painting and the 1988 film. The 1960 film has the empty paper but no mountains |
| 3 | Black, gray and paper only, except one small vermilion accent per character | `must` | A choice of this pack, supported by the painting (red only in the seal). The films add pale or full colour. Kept so the style stays apart from `watercolor-storybook` |
| 4 | Every character drawn with the same simple brush grammar: open brush-circle head, dot eyes, ink-blot hands | `bonus` | Our simplification for character consistency. The films draw faces with fine realistic lines |
| 5 | Any writing drawn in frame: seals, calligraphy columns, signatures, shop signs | `forbidden` | The painting has a signature and a seal. Drawn as decoration they read as pseudo-characters, so the seal is stamped in post instead |

The `must` traits are asked for in the frozen environment block below, word for word in every clip.

## Nearest neighbour

`watercolor-storybook` (also a wash medium on paper). Two differences a viewer sees: (1) ink-wash is black
ink and gray wash with one small vermilion accent per character, while watercolor-storybook uses a warm
multi-colour palette with a thin sepia outline; (2) ink-wash keeps characters small inside large empty paper
and misty mountains drawn with dry-brush strokes, while watercolor-storybook makes the character the most
saturated, most outlined element and fills the frame with parallax layers. `chu-tieu` shares the
calm, empty frame but uses flat pastels and an even brown outline, with no black ink.

## Shared brush grammar (every character)

Freeze this sentence and repeat it verbatim in every clip that shows a character:

```text
Every character is drawn with the same brush grammar: a round head outlined by one open brush circle, two dot eyes, simple brush eyebrows and mouth, small round ink-blot hands, short black brush-stroke shoes, and clothing as soft gray washes with one confident dark contour stroke. Each character has exactly two arms and two legs and keeps the same proportions; a moving limb replaces its previous pose. Expressions change only the eyes, eyebrows and mouth, never the head, hair, clothes or proportions.
```

## A cast, not one hero

Monochrome makes characters look alike, so each role needs a different **silhouette** and a red accent in a
different **place**. Do not tell characters apart by gray tone alone.

| Role | Silhouette | Red accent | Height |
|---|---|---|---|
| Mac, apprentice painter | small topknot, short robe | sash at the waist (+ tiny cord in the topknot) | ~7 heads |
| Old Tung, ink master | bald with white topknot ring, long dry-brush beard, knee-length robe, slight stoop | gourd at the left hip | ~7 heads |
| Lien, quick girl | two hair buns | a ribbon on each bun | ~6.5 heads |
| Ba, fisherman | wide conical hat, broad bare arms, rolled trousers | thin rope belt | ~7 heads |
| Dom, small child | big head, one curled tuft | triangular bib | ~4.5 heads |

Sample anchors (repeat the full anchor of every character that appears in a clip, verbatim, after the grammar sentence):

```text
Mac, a young apprentice painter about seven heads tall: a small black topknot tied with a tiny red cord, a short pale gray robe to mid-thigh with a crossed collar and a vivid red sash at the waist, dark gray trousers and black shoes.
```

Old Tung always holds the walking staff in his **left** hand and takes the brush with his right; the gourd hangs
at his left hip, so in a view facing screen-right it is hidden behind the robe. Ba carries the shoulder pole on his
right shoulder with his right hand on the pole in front of the shoulder, below the chin, never across his face.
Mac paints with his right hand.

```text
Old Tung, an elderly ink master about seven heads tall, slightly stooped: a bald head with a tiny white topknot ring, long wispy dry-brush eyebrows, a long dry-brush gray beard, a knee-length mid-gray robe with a crossed collar, a small red gourd hanging at his left hip, pale gray trousers and black shoes.
```

```text
Lien, a quick-footed girl about six and a half heads tall: two round black hair buns on top of her head, each tied with a small red ribbon, a short white robe with a crossed collar, solid dark ink trousers and black shoes.
```

```text
Ba, a broad-shouldered fisherman about seven heads tall: a wide conical straw hat in gray wash with dry-brush ribs, bare arms drawn as bold black strokes, a short dark gray sleeveless jacket with a thin red rope belt, pale gray trousers rolled to the knee and bare black brush-stroke shins.
```

```text
Dom, a small child about four and a half heads tall with a large head: one curled tuft of hair on top, a red triangular bib under the chin, a short white robe and dark trousers.
```

Other stories may approve another cast; keep the grammar sentence and the "different silhouette, red accent in a
different place" rule. Robes end at or above the knee so knees stay readable.

Keep at most four characters in one ten-second clip and at most two doing
something with their hands at the same time; let others enter or leave on a beat rather than stand idle.

## Environment block

```text
Style and environment: traditional East Asian ink-wash painting brought to life as 2D animation, sumi-e style, on warm off-white rice paper with a faint fibre texture. Black ink brush strokes with dry-brush streaks where the brush runs out, soft gray ink washes with darker dried edges, misty layered mountains fading into blank paper, and large calm areas of empty paper. The only color in the whole video is a small vermilion red accent on each character; everything else is black ink, gray wash and paper.
```

Follow it with one sentence naming the clip's place (riverbank at dawn, village lane, boat on a lake, pine
ridge). Name color only as "vermilion red"; never hex or other notation.

## No writing, not even "decorative"

Seals, signatures, calligraphy columns and shop signs drawn as decoration read as pseudo-characters.
In the prototype, a seal built from abstract cuts (a ring, two bars, a line) still read as a Hangul syllable; a
plum-blossom picture did not. Rules:

- Never ask for a seal, signature, calligraphy, scroll writing or poem in the scene art. The negative list bans them.
- Paintings inside the story show pictures only: mountains, birds, boats, pines.
- Stamp the seal in post-production with an approved image (a picture, not a glyph).

## Posture and hands (lessons from the gate)

Apply `posture-gate.md` in full. These style-specific rules come from the 17 failing draft tracks:

- **Hand to chin or beard**: stage it in profile. In a flat front view the elbow cannot come toward the camera, so
  the hand only reaches the chin by folding the elbow past 150°, and the forearm crosses the face.
- **Looking up at peaks or birds**: lean the whole body back and bend the knees a little; the neck alone tops out
  near 50–55°. The skull turns at the top of the neck; it must not hang behind the shoulders.
- **Bows**: push the hips back as the chest goes down (about 60° for an elder); a 75° bow on straight legs topples.
- **Kicks (đá cầu, shuttlecock)**: thigh no higher than about level-and-a-bit (≈115°), body leaning back.
- **Throws (casting a net)**: wind up by turning the torso; the arm swings back at most about 55°.
- **Runs**: include a passing pose between strides. At 12–24 fps, arms jumping from front to back in one frame read
  as the hands trading places.
- **Falls**: the head looks at the ground ahead, not thrown back.
- **Hand-offs between characters**: one beat for the reach, one for both hands on the prop, one for the release;
  name both hands ("takes the brush from Mac's right hand with his own right hand").
- A shoulder pole rests on one named shoulder with that hand on it; a walking staff stays in one named hand.

## Motion vocabulary

- Painting is a character action: the brush touches paper and a stroke appears behind the tip. Ink never moves
  or morphs on its own; no liquid transformations.
- Good beats: an ink drop falling, a single bold stroke, a sleeve swinging, walking along a bank, a boat pushing
  off, wind in a pine, mist drifting across.

## Motion cadence

`smooth`. Ink-wash animation reads as one continuous brush in motion; stepped or on-twos timing makes the
paper texture and the washes flicker.

## Camera grammar

Follow the camera grammar in `storyboard-template.md`. For this style:

- Transition moves (most beats): hold, slow push-in, pull back, lateral track along the bank (`16:9`), slow
  vertical reveal of a tall peak (`9:16`, not covered yet), hard cut to a new shot size.
- Accent moves: at most one per clip and in at most one clip in three. The only accent that suits the style is a
  fast push-in on a stroke or ink drop at a reveal; no whip pans, shakes or orbits.
- Hold the camera while a character does a demanding body action (a handoff, a kick, a bow, a throw) and while
  the picture already moves by itself (an ink drop falling, mist drifting).
- Name the camera move in every beat of every clip.

## Text policy

`post-overlay`. No words, letters, numbers, seals or calligraphy are drawn in frame. Optional overlays and
the seal are added in post-production; an overlay uses only words the voiceover says.

## Core rules this style overrides

- **Idle and reaction beats**: a held character is allowed when mist, water or ink is moving in the same shot,
  because the stillness is part of the style; the beat still names that motion. A character with nothing to do
  leaves the frame on a beat instead of standing idle.
- **Faces**: simple faces (dot eyes, brush brows, a mouth) are allowed and expressions change only these; this
  replaces the no-face rule of Style 1. No detailed pupils or noses.
- **Location changes**: one place per package by default, with named time steps (dawn, a moment later, full
  morning). A new place needs a named cut and its own place sentence after the environment block; the
  environment block itself never changes.
- **Music**: a slow, sparse plucked-string score replaces the default; the voice contract is unchanged.
- **Visual density**: the four-devices rule still applies, but mist, a falling drop or a single stroke counts
  as a device; no extra effects are added for density.

## Opening hook overrides

Keep hooks quiet and visual. Prefer **Silence then hit** (an ink drop landing after near-silence), **Satisfying
motion** (one perfect stroke) and **Partial reveal** (a brush tip, pull back to a vast landscape). The sound cue
is a soft wet drip, a brush swish or one plucked note, never an impact or bass hit.

## Post-production

- Stamp the plum-blossom seal (an approved picture, not a glyph) in a lower corner.
- Overlays only under the `post-overlay` policy above, using words the voiceover says.
- Trim joins so the held prop is in the same hand on both sides of each cut; short audio crossfades at the joins.

## Negative block

```text
Negative constraints: no colors other than black ink, gray washes, warm paper and the small vermilion red accents, no 3D render, no CGI, no photorealism, no anime cel shading, no thick uniform vector outlines, no glossy or gradient digital look, no visible text, letters, numbers, calligraphy characters, seal stamps or signatures, no speech bubbles, no dialogue boxes, no watermark, no extra arms or legs, no duplicate characters, no characters other than the ones named, no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no prop switching hands without a visible pass, no ink morphing into new shapes on its own, no liquid melting effects, no logos.
```

## Audio

Apply `voice-continuity.md` unchanged. Music suggestion: slow, sparse guzheng with breathy bamboo flute and a soft
low drum; same instruments and tempo in every clip. SFX: brush bristles on paper, water, footsteps on gravel.

## Checks before delivery

- Every visible character has its full anchor after the shared grammar sentence; no "same character" shortcut.
- Each character keeps its one red accent in its one place; no other colors.
- No seal, calligraphy, signature or writing is requested anywhere; the seal is listed for post-production.
- Hand-to-face beats are in profile; look-ups lean the body; bows push the hips back.
- `Hands at start` / `Hands at end` lines for every character in every clip; `hand_ledger.py` passes.
- At most four characters per clip; every visible character is doing something.
- Clip 1's first frame and first timed beat carry the hook (Golden Hook section of `storyboard-template.md`); no spec has a separate `Opening hook:` line.
- Every beat names its camera move; at most one accent per clip.

## Sample package and facts

[`samples/ink-wash.md`](samples/ink-wash.md): "One drop of ink", 3 clips, 16:9, cast of five (at most four per clip),
global continuity block, stitching guide and voice and music continuity note. `hand_ledger.py`: PASS;
`package_lint.py --clips 3` with the environment block, brush grammar, voice block and negative block as
`--anchor`: PASS; `tests/verify-opening-hook.py`: PASS.

<!-- package_lint facts: generated, do not edit -->
- package: `ink-wash.md` sha256 0d34293e56ea6118
- checked: 2026-10-22
- storyboard rows: none
- segment specs: 3
- hand_ledger: PASS
- red: 0
- yellow: 0
<!-- package_lint facts end sha256=1a9067fc9b032d2d75f062930cb5443aed17355a4b942188a939b3c6a46e143f -->

## Catalog entry (draft)

Style-matrix row:

```text
| **ink-wash** | Ink-Wash / Sumi-e (水墨) | Black ink and gray wash on warm rice paper, misty mountains, large empty paper, one vermilion accent per character | Reflective explainers, habits and patience, craft, folk-tale style stories | Open brush-circle head, dot eyes, ink-blot hands, gray-wash clothing; each character a different silhouette with its red accent in a different place |
```

Status row:

```text
| ink-wash | gated | 60 pose tracks and 2 motion tests pass posture_gate; 3-clip package passes package_lint (`ink-wash.md`, facts block) |
```

Setup-gate line (offered only when the user asks for an experimental style):

```text
- `ink-wash (Ink-Wash / Sumi-e, gated, experimental)`: black ink and gray wash on rice paper with one vermilion accent per character; small characters in misty, mostly empty landscapes
```
