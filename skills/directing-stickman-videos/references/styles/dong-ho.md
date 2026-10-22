# Đông Hồ Folk Print (slug `dong-ho`)

> In this repository: the sample package and its lint facts are `samples/dong-ho.md` and `samples/dong-ho.facts.md`. Other research files named below (gallery, tracks, gate output, renderer) stay in the project's `style-research/dong-ho/` folder and are not part of the skill.

```text
Status: gated (2026-10-20). Covers: code-rendered rig of five villagers (35 poses incl. CMU mocap walks, 12 expressions,
one 6 s four-character motion test with a two-handed rice-cake handoff) passing posture_gate; one 3-clip, four-character
16:9 sample package passing package_lint, hand_ledger and the opening-hook test.
Not covered: 9:16, crowds, animals as cast, night scenes, three-quarter views.
```

Evidence: gate output `gallery/gate-output-v2.txt` and `gallery/front-arms-fix/gate-front-rest.txt`, motion-test tracks `motion-test/tracks-v2/` (`--scene` PASS), package `samples/dong-ho.md` with lint facts `samples/dong-ho.facts.md`, gallery `gallery/` (see `README.md`). Draft for `skills/directing-stickman-videos/references/`, named by slug. Self-score not given; an independent review (style-audit thread) has read the samples, and its findings are fixed below.

## Sources

Museum and archive records and articles were read as text; the prints themselves were not inspected at full resolution. Where sources disagree (number of blocks, order of printing) this pack takes the point all of them share.

| Work or source | What it supports | Where it runs out |
|---|---|---|
| *Phú quý* (Prosperity and honour), Đông Hồ New Year print, Hopp Museum Budapest, [record 128345](https://hoppmuseum.hu/en/collection/traditional-new-year-picture-prosperity-and-honour-vietnamese-phu-quy-/128345?n=en) | a single chubby child in front view holding an animal against the chest: round face, flat costume blocks, auspicious subject; paired with a rooster print | sources disagree on the child's sex; record text only |
| *Chăn trâu thổi sáo* (boy on a buffalo playing the flute), Hopp Museum, [record 128347](https://hoppmuseum.hu/en/collection/pdfexport/128347-traditional-new-year-painting-boy-sitting-on-a-buffalo-and-playing-the-flute-vietnamese-chan-trau-th) | profile staging of a folk-life action, a child with a bamboo flute | not copied: Tí plays the flute standing, never on a buffalo |
| *Đám cưới chuột* (The rats' wedding), Hopp Museum [record 128353](https://hoppmuseum.hu/en/collection/traditional-new-year-picture-rat-s-wedding-vietnamese-dam-cuoi-chuot-/128353?n=760) and [UMMA 1960/1.162](https://umma.umich.edu/objects/the-rats-wedding-1960-1-162/) | a procession read left to right along one ground band, gift-giving as story, gentle satire of a situation; inscriptions sit in panels | not copied; the inscription panels are dropped (see text policy) |
| EFEO virtual exhibition on Maurice Durand's *Imagerie populaire vietnamienne* (1960; colour reissue with Philippe Papin, 2011), [PDF](https://www.efeo.fr/exposition-virtuelle/Image_Pop_Vietnam.pdf) | Đông Hồ is the flat-colour woodblock centre, as against Hàng Trống's brush-painted colour | the book itself was not read |
| UNESCO, [Đông Hồ folk woodblock printing](https://ich.unesco.org/en/RL/01737) (Urgent Safeguarding List), and Vietnam News / Tạp chí Công Thương articles listed in `README.md` | điệp paper (dó paper brushed with powdered scallop shell), one block per natural pigment, the black key block printed last | sources give 2 to 7 blocks per print |

## Signature checklist

| # | Trait (visible in a still) | Tag |
|---|---|---|
| 1 | Warm off-white điệp paper ground with a pearly shimmer and diagonal brush grain showing through everywhere | `must` |
| 2 | Flat blocks of the natural pigments only (cinnabar red, pagoda-flower yellow, leaf green, indigo, soft brick pink, charcoal black), each printed slightly off register from the outline | `must` |
| 3 | One bold, slightly uneven black woodblock outline around every shape, with white carved lines inside dark blocks (folds, sleeve edges) | `must` |
| 4 | Figures in flat profile or front view on ground bands; far things sit higher on the page, not smaller; a thin double border | `bonus` |
| 5 | Shading, gradients, lighting, perspective depth or any writing (Hán Nôm, seals, banners) | `forbidden` |

Spec wording for each `must` trait is the style block below, repeated verbatim in every clip.

**Nearest neighbour:** `paper-cutout` (Paper Cutout / Collage, research thread). Both are flat 2D with visible paper. A viewer sees two differences: Đông Hồ shapes are bounded by a printed black key line with colour slipping off register, while cut paper has no outline and casts a soft shadow onto the layer beneath; and the Đông Hồ ground is one shimmering điệp sheet with no layering or stop-motion jitter.

## Character anchors (frozen)

Five sample villagers, all original (no famous print's figure or costume set). Children about four heads tall, adults about six; at least two non-colour differences between any two (headwear, hair, beard, height, robe length). Repeat each anchor verbatim in every clip the character appears in, and list exactly who is in the clip (`Characters (exactly N, no one else)`). Source of truth: `src/rig.py` `CAST[..]["anchor"]`.

```text
Tí: a small round-bodied village boy about four heads tall with a shaved head and a single black peach-shaped tuft of hair on the crown, chubby cheeks with pink dots, a bright yellow diamond apron (yếm) tied over a bare chest, short red trousers, bare feet.
Mận: a small village girl about four heads tall with black hair gathered in two small round tufts on top of the head, chubby cheeks with pink dots, a short green blouse with elbow-length sleeves, red calf-length trousers, bare feet.
Cô Thắm: a young village woman about six heads tall with a black crow's-beak headscarf (khăn mỏ quạ) folded to a point above the forehead and tied under the chin, a knee-length indigo four-panel dress (áo tứ thân) open over a red bodice (yếm), a green sash tied at the waist with its ends hanging in front, a black skirt to mid-calf, bare feet.
Bác Cả: a sturdy middle-aged farmer about six heads tall with a black wrapped turban (khăn đầu rìu) knotted in a small horn above the forehead, a short black beard and moustache, a hip-length indigo work shirt with a red cloth belt, off-white trousers rolled up above the knees, bare feet.
Ông Đồ: an old village scholar about six heads tall with a flat round black turban (khăn xếp), a long white beard and thin white moustache, a long black robe (áo dài) reaching below the knees with wide sleeves, white trousers, small black slippers.
```

After the anchors, verbatim:

```text
Every character has exactly two arms and two legs; a moving limb replaces its previous pose. Limbs keep their length and bend smoothly at elbows and knees. Faces are round with long single-stroke almond eyes, round red-pink cheek dots and a small red mouth; expressions change only the eyes, eyebrows and mouth, never the face shape, headwear, costume or proportions.
```

## Style block (frozen)

```text
Style and environment: an animated Vietnamese Đông Hồ folk woodblock print in flat 2D. Warm off-white điệp paper with a faint pearly shell shimmer and fine diagonal brush grain shows through everywhere. Only flat areas of natural pigment colors: cinnabar red, pagoda-flower yellow, leaf green, indigo blue, soft brick pink and charcoal black, each color printed slightly off register from the outlines. Every shape has a bold, slightly uneven black woodblock outline printed over the colors. No shading, no gradients, no lighting effects, no perspective depth: figures stand in flat side or front view on simple ground bands, farther things sit higher on the page instead of smaller. Sparse folk motifs only: swirling cloud scrolls, a peach-blossom branch, bamboo, grass tufts. A thin double black border frames the picture.
```

## Core rules this style overrides

- **Faces** (overrides the no-face Style 1 bans): round faces with almond eyes, cheek dots and a small red mouth, because folk-print figures always carry them; expressions change only eyes, brows and mouth, never manga marks.
- **Hands and props**: folk-life actions are two-handed (shoulder pole, pestle, hoe, flute, a gift). Name both hands in the beat, give each gift its own beat (who holds out, which hands receive, that the giver's hands are empty), and keep one noun per prop in beats and Hands lines (`rice cake`). Reason: in the gallery, 6 of 13 failing drafts were hands missing a two-handed prop.
- **Receiving**: a polite gift is received with both hands, then one hand may let go in a named beat.
- **Music**: one frozen folk score instead of the catalog's piano (below).
- **Location**: one village courtyard or porch per story; a time cut is named (`(time cut)` on the Hands line).

## Text policy: `post-overlay`

Real prints carry Hán or Nôm captions, but drawn into the scene art they come out as fake characters. Specs ban all writing; captions, a title or calligraphy are added in post-production on the paper margins. A scholar "writing" paints a picture (a plum-blossom branch) instead.

## Motion cadence: `on-twos`

Woodblock figures should move like printed puppets, not like smooth 3D: hold each pose about two frames, keep limbs rigid between joints, and let the paper and border stay still. (The motion test renders at 12 fps, which is on twos at 24 fps.)

## Camera grammar

Follow `storyboard-template.md`. Allowed moves: hold, slow lateral pan or track (the natural move for a left-to-right folk procession), slow push-in or pull back, hard cut to a new shot size. Hold through every handoff, bow and two-handed action. Accent moves (whip pan, slam zoom, shake, orbit) break the flat print and are not used. No three inward moves in a row; the sample package goes pan, cut, push-in.

## Style bans and posture limits

Style negatives (with the five posture negatives from `posture-gate.md`), verbatim in every clip:

```text
Negative constraints: no 3D render, no CGI, no gradients or soft shading, no glossy or airbrushed look, no anime or manga eyes, no realistic anatomy, no photographic textures, no extra arms or legs, no duplicate characters, no extra villagers or crowds, no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no prop switching hands without a visible pass, no Chinese characters, no Hán Nôm calligraphy, no red seal stamps, no inscription panels or banners, no visible text, letters or numbers, no speech bubbles, no dialogue boxes, no logos, no watermark.
```

Rig and drawing limits found by the gate and the visual review:

- No three-quarter turns: the flat style cannot draw them consistently. Side view for actions, front view for greetings.
- Front view: shoulder joints sit at the edge of the torso and hanging arms leave a strip of paper at the waist; a black sleeve on a black robe needs a white carved edge line, or it fuses into the body (Ông Đồ). Tracks carry `body_width` so the gate's `arm_over_body` check runs.
- In profile, the near arm stays below the chin for pounding and hoeing; only shading the eyes and wiping the brow cover the face, on purpose (`face_cover`).
- A scroll or any wide prop is held at its ends on each hand's own side; forearms never cross the chest.
- Children's arms are short: no hands overhead from a crouch.

## Hook overrides

Prefer Reaction before cause, Partial reveal and Satisfying motion. The hit is one soft gong note or wooden clapper, never an impact.

## Voice and music

- **Score (frozen):** a gentle bamboo flute melody over a soft wooden clapper keeping a slow beat. Clip 1 sets it; later clips say it continues from clip 1 with the same tempo and instrumentation.
- **Narrator:** a per-video choice under `voice-continuity.md`; the style never recasts the narrator. The sample package chose one female narrator with a gentle Northern Vietnamese accent speaking English.

## Post-production steps

1. Trim each clip to the last frame whose hands match its `Hands at end` line; hard cuts at the joins, 4 to 6 frame audio crossfades.
2. Add any caption, title or calligraphy as an overlay on the paper margins.
3. Do not colour-grade or add vignettes: they break the flat pigments and the paper white.
4. Record the narration as one VO track and lay the flute/clapper score as one continuous bed over the assembled picture.

## Sample package

[`samples/dong-ho.md`](samples/dong-ho.md): “The cake that came back”, 3 clips, 16:9, Mận, Tí, Ông Đồ and Cô Thắm, with global continuity block, stitching guide and voice/music note. Facts block from `package_lint.py --facts`: [`samples/dong-ho.facts.md`](samples/dong-ho.facts.md).

## Catalog row (ready to paste)

| Style Key | Style Name | Visual Theme | Best For | Character Design |
|---|---|---|---|---|
| `dong-ho` | Đông Hồ Folk Print | Flat natural-pigment blocks on shimmering điệp paper, black woodblock key line, off-register colour | Vietnamese culture, Tết and village stories, gentle fables | Round-faced villagers in folk costume, children four heads tall, adults six |

Status row: `| dong-ho | gated | this file, gallery gate output, package facts |`.

Setup-gate line for `SKILL.md` (offer only when the user asks for an experimental style, and say it is `gated`):

```text
  - `dong-ho (Đông Hồ Folk Print, gated)`: flat natural-pigment blocks on shimmering điệp paper with a black woodblock key line, round-faced villagers in folk costume; no writing in frames (captions added in post)
```

## Acceptance

- No writing, seals or caption panels anywhere.
- Colours stay flat, the paper ground stays visible; no gradients, glow or 3D shading.
- Each character keeps its headwear, costume colours and proportions; no extra villagers.
- Every held prop stays in the named hand; gifts change hands only in the named beat.
