# Stylized 3D Family Film (style pack)

> In this repository: the sample package and its lint facts are `samples/stylized-3d-family.md` and `samples/stylized-3d-family.facts.md`. Other research files named below (gallery, tracks, gate output, renderer) stay in the project's `style-research/stylized-3d-family/` folder and are not part of the skill.

```text
Status: gated (2026-10-20). Covers: 3 clips, 2–3 characters on screen, ball handoffs, a low five, indoor and porch sets, 16:9.
Not covered: Minh and Bảo in a package, 9:16, crowds (4+ in one clip), night scenes, fast action.
```

Slug: `stylized-3d-family`. Evidence: posture gate on 186 pose tracks and two multi-character motion tests ([README.md](README.md), `gallery/gate-output-v2.txt`, `motion/gate-motion.txt`); the sample package [samples/stylized-3d-family.md](samples/stylized-3d-family.md) passes `package_lint.py` and `hand_ledger.py` ([facts block](samples/stylized-3d-family.facts.md)); `tests/verify-opening-hook.py` passes on it.

The mainstream US animated-feature look: stylized 3D characters with appealing exaggerated proportions, big expressive eyes, soft rounded forms, satin skin with a warm glow at the shadow edge, sculpted hair and matte cloth, under soft cinematic light. All characters are original. Specs describe the look in plain words and never name a studio, film or character.

## 1. Signature checklist

### Sources

These works are named here as research only. Specs never name them, and the cast copies none of their characters, costumes or colour combinations. Frames studied on 2026-10-20; local copies for review are in `research/frames/` (the CC-BY Blender stills may be kept; the two posters are copyrighted and are kept only as a research record, never published).

| Work | Image looked at | Confirms | Contradicts, and what changed |
|---|---|---|---|
| *Sprite Fright* (Blender Studio, 2021, CC-BY) | Character lineup, https://www.blender.org/wp-content/uploads/2021/11/sf_lineup_students_beauty-1280x536.jpg ; key art, https://studio.blender.org/files/public/header/project/ff/3d/ff3d8a8048e767cbc92d6489404924b2.jpg | Trait 1: big eyes with white sclera, dark iris, black pupil and one catchlight. Trait 2: smooth satin skin with warm light bleed at the shadow edge. Trait 3: every body built around one pushed shape (a tiny head on a giant chest, a big round belly, a huge nose). Trait 4: hair as sculpted masses (the ponytail, the bowl cut). | Hands have four fingers and a thumb, so three-fingered hands are not a genre trait (they stay a cast rule, below). The adults are 6 to 7 heads tall with long limbs, so "adults 4 to 5.5 heads, short limbs" is not a genre trait either. The punk girl's hair shows fine strand detail, so strands are not forbidden by the genre. One character has freckles: skin is simplified, not always blank. |
| *The Incredibles* (2004) | Theatrical poster, https://upload.wikimedia.org/wikipedia/en/2/27/The_Incredibles_(2004_animated_feature_film).jpg | Trait 3: shape-based exaggeration (a huge wedge torso with a small head on the father, a big head on the baby). Trait 1: big white eyes with a dark iris on every face. Trait 2: smooth one-tone skin. | The mother's long legs and the father's realistic jaw show the genre is not "short limbs" across the board. Four fingers and a thumb again. |
| *Cloudy with a Chance of Meatballs* (2009) | Theatrical poster, https://upload.wikimedia.org/wikipedia/en/d/d1/Cloudy_with_a_chance_of_meatballs_theataposter.jpg | Trait 3: a big head on a very thin, long-legged body; trait 1: big eyes with one catchlight; trait 4: hair as a few sculpted clumps. | The hero's long thin limbs again contradict "short limbs". Four fingers and a thumb. |
| *Coffee Run* (Blender Studio, 2020, CC-BY), contrast case | Header frame, https://studio.blender.org/files/public/header/project/7a/43/7a43fa6b0bc44e62f1cbb21473800e07.png | Stylized 3D humans can avoid the uncanny middle with flat painterly light instead of soft skin shading. | It has small simple eyes and flat lighting with no warm skin glow, so it is a neighbouring stylized-3D look, not this one. It marks where trait 1 and trait 2 stop applying. |
| Masahiro Mori, "The Uncanny Valley" (essay, 1970; English translation 2012) | Text, not frames | The argument for pushing every axis away from the near-human middle | It is about robots and gives no drawing rules |

What was looked at: the two Sprite Fright images, the two theatrical posters and the Coffee Run frame above, checked at full size on 2026-10-20. Posters are key art, not film frames, so the poster rows show character design and render quality, not staging or acting. No full films were watched for this research. A third poster (The Polar Express, the usual uncanny-valley example) was fetched but shows no face, so it supports nothing and was dropped from the sources.

Changes made because of the frames: trait 3 now asks for shape-based exaggeration rather than fixed head counts and short limbs, and the frozen style block says so. Three-fingered hands, the head counts and "no individual strands" stay, but as this cast's own simplifications for clean hand counts and stable hair in video, not as genre traits.

### Five signature traits

| Tag | Trait (visible in a still) |
|---|---|
| `must` | Big simple eyes with white sclera, one flat iris colour, a black pupil and one catchlight; on kids each eye is about a quarter of the head width |
| `must` | Smooth satin skin of one tone with a warm glow where light meets shadow; no pores, wrinkles or nostril holes |
| `must` | Exaggerated, shape-based proportions: kids with oversized heads, adults built around one pushed shape (a round belly, a long neck, a tall thin frame), never realistic anatomy |
| `bonus` | Hair as a few large sculpted clumps; plain matte cloth with clear seams where sleeves meet the body |
| `forbidden` | The uncanny middle: realistic skin texture, small realistic eyes, seven-head realistic bodies with a cartoon face |

### Nearest neighbour

Research: **toys** (3D toys that come alive, warm lamp light). Two visible differences:

1. Toys are hard and soft toy materials (molded plastic, muslin, tin) seen at floor level with a shallow macro focus. This style has soft satin human skin and cloth at human eye level, with deep focus on a whole room.
2. Toys has no people. This style is a human family with big expressive faces that act every beat.

Catalog: **Style 2B** is the closest catalog entry (full-colour cinematic sets, warm light) but bans 3D humanoid CGI and uses the stick figure. This style is that ban's one controlled exception (section 4).

### Why this style is allowed when Style 2B bans 3D CGI

Style 2B bans "3D humanoid CGI" because a spec that only says "3D" invites semi-realistic humans: small eyes, real skin texture, adult proportions on a doll body. That middle zone is the uncanny valley. This style avoids it by pushing far to the stylized side on every axis at once, and by naming those axes in every clip:

| Axis | Stylized side (ask for) | Uncanny middle (ban) |
|---|---|---|
| Proportions | shape-based exaggeration (this cast: kids 2.5 to 4 heads tall, adults 4 to 5.5) | 7-head realistic bodies with a cartoon face |
| Eyes | each eye about a quarter of the head width (kids), one flat iris colour, black pupil, one catchlight | small realistic eyes, wet red rims, veins, detailed eyelashes |
| Skin | smooth satin, one tone, warm glow at the shadow edge | pores, wrinkles, stubble, glossy plastic or doll sheen |
| Face detail | button nose, no nostril holes, simple mouth shapes, soft sculpted brows | realistic teeth and lips, nostrils, eye bags |
| Hair | a few large sculpted clumps of one colour (strands are allowed in the genre, banned in this cast to keep hair stable in motion) | flyaways, wet or greasy realistic hair |
| Hands | simplified cartoon hands (this cast: three fingers and a thumb) | realistic knuckles, nails and veins |
| Motion | clear key poses, slight squash and stretch, weighty | motion-capture jitter, realistic micro-movement |

Will the build hold it? The characters are built once as simple 3D rigs, so faces, materials, proportions and the three-fingered hands are fixed in the model sheet, not re-described per shot. The risks are (1) adults posed or scaled to realistic heights in wide shots, (2) a five-fingered hand swapped in from a stock asset, (3) a likeness of a famous character if a studio or film is named, which is why specs never name one. Build order: one character close-up, one adult in a wide shot, then the package.

### Spec wording for each `must` trait

The frozen style block below says each one in plain words. It is repeated verbatim in every clip.

## 2. Frozen style block

Repeat it verbatim in every clip. The set goes on a separate `Setting:` line, which may change between clips.

```text
Style: a stylized 3D animated feature-film look for families. Appealing exaggerated, shape-based proportions: oversized heads on kids, one boldly pushed shape on adults (a round belly, a long neck, a tall thin frame), soft rounded simplified forms, no realistic anatomy. Skin is smooth and satin with a soft warm glow where light meets shadow, no pores, wrinkles, veins or visible nostrils. Big eyes with one solid iris color, a black pupil and one bright catchlight; soft sculpted eyebrows; simple mouths. Hair is a few large sculpted clumps of one color, never individual strands. Clothes are plain matte cotton with no prints, text or logos. Warm soft key light from the upper left, a cool soft fill, a gentle warm rim light, soft contact shadows. Smooth, weighty, readable acting with clear poses and slight squash and stretch. Palette: warm cream walls and honey-wood floors, soft sunlit gold, clear but gentle costume colors (coral, teal, purple, rust orange, sky blue, moss green), deep warm browns for hair, no neon colors and no grey, desaturated grading.
```

## 3. Cast cards (verbatim anchors)

Six original characters, one family and a neighbour. They differ first by silhouette (height, body shape, hair shape), then by one dominant colour. Model sheets: `sheets/model-<name>.png`; lineup: `sheets/cast-lineup.png`; expressions: `sheets/expressions.png`.

| Character | Role | Anchor |
|---|---|---|
| Lulu | lead, 8 | Lulu: an eight-year-old girl, about three heads tall. Large round head, warm light-tan skin, rosy cheeks, big dark-brown eyes; dark-brown hair in two short puffy pigtails low at the sides of her head, tied with coral hair ties, and a short fringe. Coral short-sleeved t-shirt under teal overall shorts; white sneakers with red soles. |
| Su | little brother, 3 | Su: a three-year-old boy, about two and a half heads tall, very round head, light-tan skin, rosy cheeks, huge dark-brown eyes, short dark-brown hair with one curl standing up on top. Green long-sleeved t-shirt, navy shorts, red shoes. |
| Ray | neighbour, 11 | Ray: an eleven-year-old boy, about four heads tall, lanky. Warm brown skin, big dark-brown eyes, a rounded cap of tight dark curls. Purple sweatshirt with slightly darker plum sleeves, charcoal trousers, orange sneakers. |
| Linh | mother | Linh: a mother, a tall slim woman about five and a half heads tall, long neck, light-tan skin, dark-brown eyes, a sleek dark chin-length bob with side-swept fringe. Rust-orange long-sleeved sweater with a cream collar, dark-blue jeans, brown shoes. |
| Minh | father | Minh: a father, a stout pear-shaped man about five heads tall with short legs and a round belly, tan skin, dark-brown eyes, short dark hair, a full short dark beard and a small moustache. Blue short-sleeved t-shirt, khaki trousers, gray sneakers. His arms hang clear of his belly. |
| Bao | grandfather | Bao: a grandfather, short and round, about four heads tall, bald on top with puffy white hair at the sides, big bushy white eyebrows, a white walrus moustache, a big round nose, kind dark-brown eyes. Moss-green cardigan with slightly darker green sleeves and a cream collar, brown trousers, dark slippers. |

After the anchors in every clip, add this rule once:

```text
Every character has exactly two arms and two legs and cartoon hands with three fingers and a thumb. Elbows and knees bend one way only and limbs never stretch. Every character wears one bright yellow band on the right wrist only.
```

Anchor rules:

- Use ASCII names in specs ("Su", "Linh", "Bao"), one spelling per character; Vietnamese family titles (Bé, Mẹ, Bố, Ông) stay out of specs.
- Write each relation so it reads correctly without the other character in the clip ("a mother", not "Lulu's mother").
- Keep props out of the anchors; a ball goes in `Props:` and in the `Hands` lines.
- Lulu's hair is two low pigtails with coral ties. The first design (two round buns on top of a round head) read in silhouette as a famous mouse mascot's ears and was dropped.

## 4. Core rules this style overrides

| Core rule | Override | Reason |
|---|---|---|
| Style 2B: no 3D humanoid CGI | Stylized 3D humans, with the uncanny middle banned axis by axis (section 1) | The family-film look is the point of the style; the ban targets the near-real middle, which the negatives still forbid |
| Stick figures with plain or line faces | Full 3D characters whose eyes, lids, brows and mouth act every beat | The genre is acted through faces |
| Piano and ambient score | The frozen ukulele and glockenspiel score below | Warm family comedy, not a reflective explainer |
| One hero figure | An ensemble of six named characters, at most three in a clip | Family stories are told by a group |
| Body bans | Toddler and kid reaches stay below and beside the head; contacts happen at the shortest character's reach (section 7) | Big heads and short arms hide hands and faces |

## 5. Text, motion, camera

- **Text policy: `post-overlay`.** No words, letters or numbers in the frame; shelves, boxes and toys carry no labels. Titles, captions or subtitles are added in post (section 8), never in the spec.
- **Motion cadence: `smooth`.** Clear key poses held for a beat, then smooth eased moves; anticipation before big actions; slight squash and stretch on the body, never on limbs.
- **Camera.** Follow the camera grammar in `storyboard-template.md`; name the move at the start of every beat.
  - Transition moves: hold, slow push-in, slow pull back, slow lateral track or pan, hard cut.
  - Hold the camera during every hand pass, high five and pick-up; those are the risky moments for left and right hands.
  - Accents: at most one per video, a fast push-in on a reaction face. No orbit or camera shake: an orbit turns big heads past the shoulders.
  - The sample goes track → hold → push-in, then push-in → hold → pull back, then pan → hold → pull back, so no three inward moves follow each other.

## 6. Voice and score

The shared voice contract (`voice-continuity.md`) still applies; this style does not recast the narrator. The sample uses this block verbatim in every clip:

```text
One off-screen adult female narrator throughout. General American accent, warm clear mid-range voice, gentle forward resonance, no raspiness or breathiness. Calm, smiling conversational delivery, restrained pitch variation, steady speaking pace, and close, dry studio sound. Keep the same vocal timbre, register, accent, pace, and recording quality throughout. Emotional progression belongs to the visuals and music; do not change the narrator's voice or switch to character dialogue.
```

```text
Dialogue: audio voiceover only, strictly no speech bubbles, no dialogue boxes. Speak exactly the quoted lines once, in order; do not add, omit, paraphrase, repeat, caption, subtitle or display any words: “<line>”
```

Score, frozen. Clip 1 sets it:

```text
Music/SFX: light ukulele and soft glockenspiel around 100 BPM; <SFX>; keep the voice dominant.
```

Clips 2–N:

```text
Music/SFX: the same light ukulele and soft glockenspiel theme continues from clip 1, same tempo (about 100 BPM) and instrumentation; <SFX>; keep the voice dominant.
```

SFX may change per clip (a rubbery boing, a clap, sneaker squeaks, evening crickets). Any change to the music itself is done in post.

## 7. Style bans and posture limits

Gating 186 pose tracks (6 characters × 31 actions; walk from CMU motion capture) as true 3D tracks plus front and side camera projections with `body_width` found the habits below. The two motion tests were re-staged after an independent visual audit. Put the matching phrase in the beat.

- **Arms are separate from the torso.** Sleeves meet the body with a seam and hanging arms keep a gap from the waist; ask for "arms hang with a visible gap from the body". Minh, Bao and Su hang their arms slightly out from their round bellies. A self-hug lifts the elbows forward and out so the upper arms leave the sides.
- **Kids' raised arms go up beside the head, not in front of it.** A kid's arm is shorter than the head is tall, so a hand raised straight forward and up stops on the forehead and covers the eyes. Ask for "raises the ball up beside her head, arm out to the side".
- **No hand-on-chin for the toddler.** Su's chin sits on his shoulder line, so a hand at the chin reads as a hand on the chest. Use a hand on the cheek.
- **Kids cover the face with both hands on the cheeks.** One small hand sinks into a round cheek (Su) or reads as a lump on it (Lulu).
- **Contacts happen at the shortest character's reach.** A high five with Su is a low five in front of his chest, below his chin, clear of his face; the older character bends. Aiming above his head put his hand behind his own head, and a hand rising past his face read as touching it.
- **Nobody stands on the pass line.** A third character stands beside the pair, not behind the hands, or the ball covers their face.
- **Cross the arms one at a time.** Both hands crossing the midline in one frame is too fast to read.
- **Big heads lean back from crates.** A big-headed toddler pushing a crate keeps his back straight; bending forward puts his face into the crate before his hands.

Negatives, verbatim in every clip. They include the five shared posture negatives from `posture-gate.md`:

```text
Do not draw photorealistic people, realistic skin pores, wrinkles or stubble, glossy plastic or doll-like skin, small realistic eyes, individual hair strands, uncanny-valley faces, likenesses of existing animated characters, extra fingers, extra arms or legs, duplicate characters, unintended characters, a raised hand, arm or ball covering anyone's face, changed proportions or colors between shots, the yellow wrist band on the left wrist, visible writing, letters, numbers, captions, subtitles, speech bubbles, dialogue boxes, logos or watermarks. No knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no prop switching hands without a visible pass. Do not alter, omit, repeat, reorder, or add dialogue.
```

## 8. Post-production

1. Trim each clip to its 10 s beats and cut hard between clips; clip 3 is a time and place cut.
2. Check the risky frames before stitching: each ball pass, the low five, and each character's first frame for the yellow band on the RIGHT wrist and three fingers plus a thumb. Fix the rig and re-render a clip if the band moves wrists or a fifth finger appears.
3. Check adults in wide shots for height and eye-size drift against `sheets/cast-lineup.png`.
4. Normalise the stitched video to about -14 LUFS integrated, with the hook boing no more than 6 dB above the music bed.
5. Titles and subtitles, if wanted, are burned in after stitching (text policy `post-overlay`).

## 9. Hook override

Sudden entry, Reaction before cause and Visual metaphor suit this style: a prop bouncing into a warm room or a big-eyed double-take reads instantly. The sample uses Sudden entry (a red ball bounces in from off-screen at 0 s and Lulu follows it). A rubbery boing or a gasp is the loudest the hit may be. No impact booms or whooshes.

## 10. Sample package and gates

- [samples/stylized-3d-family.md](samples/stylized-3d-family.md): 3 clips, "The red ball", with 3, 2 and 2 characters on screen. Earlier versions: `specs/package-v1.md`, `specs/package-v2.md`.
- `tools/package_lint/package_lint.py package.md --clips 3 --anchor "<style block>" --anchor "<shared rules>" --anchor "<negatives>" --anchor "<voice>"`, from branch `claude/posture-gate-drmgl9` at f99e90a and at 99de4b9 (its hand ledger matches the shared copy): PASS, 0 red, 0 yellow (none storyboard rows, 3 specs). [Facts block](samples/stylized-3d-family.facts.md).
- `tests/verify-opening-hook.py`: passed. `hand_ledger.py` (shared copy): PASS.
- Posture gate: 186/186 pose tracks PASS with 0 errors in v2; front-view tracks export `body_width`, `body_profile` (the pear bodies are wider at the belly) and `limb_width`. With the gate's arm-thickness check (PR #4 @f99e90a), 178/186 have no warnings. Su's hanging arms first grazed his belly by about a pixel (10 tracks warned), so his arms now hang a little further out. The 8 that still warn were checked by eye and kept: self-hug and crossed-arm poses whose upper arms pass in front of the chest by design (cold for Ray, Linh, Minh and Bao, Su's belly laugh), one in-between frame of Su's cross and cold, and Minh's facepalm, whose bare upper arm stays readable against the blue shirt (v1 drafts, re-gated with the current gate: 166/186 clean, 4 failing, plus 4 faults found only by eye: Su's hand on chin read as hand on chest, the kids' raised ball covering the eyes, and the kids' one-hand face cover). 6/6 motion tracks and both `--scene` shots PASS; the high five and the handoff were re-staged after the audit found a hand passing Su's face and the ball crossing his face, both of which the gate passed ([README.md](README.md), `motion/v2/` keeps the earlier staging).

## 11. Catalog entry (ready to merge)

Style matrix row:

```text
| **stylized-3d-family** | Stylized 3D Family Film | Warm stylized 3D homes and porches, soft three-light setup, satin skin, sculpted hair | Warm family stories, kids' explainers, holiday and brand stories for a US audience | Big-eyed stylized 3D humans, kids 2.5–4 heads and adults 4–5.5 heads tall, three-fingered hands, one yellow band on the RIGHT wrist |
```

Status row:

```text
| stylized-3d-family | gated | Posture gate and package lint (`style-research/stylized-3d-family/`) |
```

Setup gate line (offered only when the user asks for an experimental style):

```text
stylized-3d-family (gated, experimental): stylized 3D family-film look with a six-character family cast.
```

## Files

- `sheets/` model sheets (4 views each), `expressions.png` (6 × 10), `cast-lineup.png`
- `gallery/poses-<character>-v1|v2.png`, `gallery/gate-fixes.png`, tracks and gate JSON
- `motion/motion-handoff.*`, `motion/motion-highfive.*`, `motion/v1/` (first staging), tracks
- `samples/stylized-3d-family.md`, `samples/stylized-3d-family.facts.md`
- `src/` renderer (`sdf.py`), rig (`rig.py`), cast, poses, fixes, gallery, motion, sheets
