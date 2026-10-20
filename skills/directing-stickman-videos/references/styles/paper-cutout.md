# Paper Cutout / Collage (slug `paper-cutout`)

> In this repository: the sample package and its lint facts are `samples/paper-cutout.md` and `samples/paper-cutout.facts.md`. Other research files named below (gallery, tracks, gate output, renderer) stay in the project's `style-research/paper-cutout/` folder and are not part of the skill.

```text
Status: gated (2026-10-20). Covers: code-rendered rig of six cast members (106 poses, 6 mocap walks, one two-character balloon handoff) passing posture_gate; one 3-clip, three-character 16:9 sample package passing package_lint and the opening-hook test.
Not covered: 9:16, crowds, night scenes, more than three characters in one frame. Not tried on Flow: every prompt wording below is a hypothesis until a Flow test confirms it.
```

Evidence: gate report `gallery/cast-gate-results.md`, scene track `gallery/tracks/scene/`, lint facts `samples/paper-cutout.facts.md`, gallery `gallery/README.md`. Draft reference for `skills/directing-stickman-videos/references/`; it is named by slug, not by the next free style number.

## Visual identity

Flat 2D cut-paper puppets photographed as stop motion. Every character and prop is a set of rigid, matte paper pieces with visible paper fibre, slightly irregular scissor-cut or torn edges, and a soft contact shadow on the layer beneath, because the pieces sit a few millimetres above the background card. Scenery is built from overlapping paper layers (sky card, torn hills, foreground strip) that slide past each other for depth. The camera faces the table straight on; no orbiting, no 3D turnarounds.

Two paper families share this grammar:

| Key | Name | Look | Best for |
|---|---|---|---|
| **5A** | Construction Paper Comedy | Bright flat construction-paper colours, crude round heads, big paper-dot eyes, deadpan timing, visible brass split-pin joints | Satire, workplace comedy, punchy shorts, absurd explainers |
| **5B** | Collage Storybook | Mixed papers: kraft, newsprint, knitted and polka-dot scrapbook paper, torn edges, warmer light, joints hidden under overlapping pieces | Gentle stories, children's English, history and culture explainers |

One video normally uses one family. A cast may mix them only with the mixed-cast sentence in the style block below, so the model gets one rule for both materials.

## Sources

General knowledge of these works, not a frame-by-frame review done for this research. The prototype's look was checked against its own renders, not against the films.

| Work | What it supports | Where it runs out |
|---|---|---|
| Lotte Reiniger, *The Adventures of Prince Achmed* (1926) | Jointed cut-paper puppets moved a pose at a time; limbs rotate at visible joints | Silhouettes only: no faces, colour or paper texture |
| Terry Gilliam's cut-out inserts for *Monty Python's Flying Circus* (1969–74) | Stepped, abrupt motion; pieces dropping in; deadpan absurd timing (5A) | Photo collage of real people, which this style does not use |
| Yuri Norstein, *Hedgehog in the Fog* (1975) | Depth from paper layers at different distances; soft light through layers | Multiplane glass and very fine detail that a video model will not hold |
| René Laloux, *Fantastic Planet* (1973) | Cut-out characters with full colour and faces across a long story | Painted detail and a dark science-fiction tone |
| Eric Carle's picture books | Painted and patterned tissue papers cut into simple shapes, torn edges (5B) | Still images, no motion |

Prompts never name these works, their makers or their characters.

## Signature traits

| # | Trait (visible in a still frame) | Tag | Prompt words (in the style block, every clip) |
|---|---|---|---|
| 1 | Every shape is a flat piece of matte paper with visible fibre and cut or torn edges; no drawn outlines | `must` | "separate rigid piece of matte paper with visible paper fibre and slightly irregular cut or torn edges ... No drawn outlines." |
| 2 | Each layer casts a small soft contact shadow on the layer below | `must` | "layered with small soft contact shadows between layers. One warm key light from the upper left." |
| 3 | Limbs are rigid two-piece cutouts that rotate at pins or overlaps, never bend | `must` | "Pieces only rotate around their joints ... limbs stay rigid and never bend or stretch." |
| 4 | Scenery in overlapping torn-paper layers with a foreground strip | `bonus` | Set-layer line per location (back card, mid layers, foreground strip) |
| 5 | Shading gradients, 3D volume, gloss, clay or felt | `forbidden` | Negatives: "no 3D rendering, no clay, no felt, no plastic, no glossy surfaces, no paper folding into 3D shapes" |

## Nearest neighbour

Style 3 (Prehistoric Hand-Drawn) is the closest: both are hand-made 2D with subtle paper texture and expressive cartoon faces. A viewer sees two differences: paper cutout has **no ink outlines**, with shapes bounded by cut paper edges and contact shadows; and its limbs are **rigid two-piece paper pieces on pins**, not drawn stick lines. A third difference shows in motion only: stepped on-twos cadence.

## Character anchor and cast cards

Freeze one card per role and repeat it in full in every clip where the role appears. Cards hold design only; poses, positions and props live in the beats and the prop rules. Any two roles differ in at least two non-colour ways (head shape, hair piece, height, accessory, clothing cut). Arms are cut from a paper that contrasts with the torso, or are bare skin paper, so the arm never fuses into the body in front view.

**Pip (5A)**
```text
Pip, a boy of about eight, one flat paper cutout puppet made of separate rigid pieces of matte construction paper: a large cream-coloured circular paper head with a brown zig-zag paper hair strip glued on top, two white oval paper eyes with black paper-dot pupils, short black paper eyebrow strips, two pink paper cheek circles and a small black paper mouth piece; a mustard-yellow trapezoid paper torso with a small cream V-neck notch; two brick-red paper sleeve arms, each an upper-arm piece and a forearm piece, ending in round cream mitten hands that reach mid-thigh; two navy paper legs, each a thigh piece and a shin piece, ending in dark brown paper shoes; small brass split pins at the shoulders, elbows, hips and knees.
```

**Mai (5A)**
```text
Mai, a young woman in her twenties, one flat paper cutout puppet made of separate rigid pieces of matte construction paper, tall and slim, about three heads tall: a tall oval light-tan paper head with long straight black paper hair falling past her shoulders and a small yellow paper hair clip above her temple, two white oval paper eyes with black paper-dot pupils, short black paper eyebrow strips, two coral paper cheek circles and a small black paper mouth piece; a sleeveless teal paper dress with a darker waist seam that flares into an A-line skirt; bare light-tan paper arms, each an upper-arm piece and a forearm piece with a round mitten hand; light-tan paper legs and white paper shoes; small brass split pins at the shoulders, elbows and knees.
```

**Ông Bảo (5B)**
```text
Ông Bảo, a grandfather in his seventies, one flat collage paper puppet made of separate rigid pieces of mixed paper, short and slightly stooped, about two and a half heads tall: a pear-shaped light-tan paper head, wider at the jaw and bald on top, with two fluffy white paper tufts of hair above the ears, two thin brown forehead lines, round black paper wire glasses, white paper eyebrows, a white paper moustache and rose paper cheek circles; a brown knitted-pattern paper cardigan with three pale buttons and one patch pocket, open over a cream shirt; sleeves cut from darker brown knitted paper so the arms stand out against the cardigan, ending in light-tan mitten hands; grey pinstriped paper trousers and dark brown paper shoes; joints hidden under overlapping paper pieces.
```

**Bé Na (5B)**
```text
Bé Na, a three-year-old girl, one flat collage paper puppet made of separate rigid pieces of mixed paper, very small, about two heads tall: a big round pale peach paper head with short dark brown paper hair, a fringe and two round pigtail buns tied with small red paper ties, two white oval paper eyes with black paper-dot pupils, pink paper cheek circles and a small mouth piece; a short sleeveless pink paper dress printed with white polka dots; short bare pale peach paper arms with round mitten hands, the shoulders showing below the head; bare pale peach legs and red paper shoes; joints hidden under overlapping paper pieces.
```

**Thầy Dũng (5A)**
```text
Thầy Dũng, a sports coach in his forties, one flat paper cutout puppet made of separate rigid pieces of matte construction paper, broad and sturdy, about three heads tall: a rounded-square warm brown paper head under a blue paper baseball cap whose brim points the way he faces (straight at the camera in front view), short black hair at the back, two white oval paper eyes with black paper-dot pupils, black paper eyebrow strips and a small mouth piece; a barrel-shaped paper shirt with red and white horizontal stripes and a silver paper whistle on a thin black cord around his neck; striped sleeves with warm brown forearms and mitten hands; navy paper shorts, warm brown legs and red paper shoes; small brass split pins at the shoulders, elbows, hips and knees.
```

**Cô Lan (5B)**
```text
Cô Lan, a schoolteacher in her thirties, one flat collage paper puppet made of separate rigid pieces of mixed paper, slim, about three heads tall: a tall oval light peach paper head with brown paper hair swept into a round bun at the back, red rectangular paper glasses, brown paper eyebrow strips and rose paper cheek circles; a short-sleeved cream newsprint-patterned paper blouse whose grey type bars are not legible, over a knee-length ochre-and-brown plaid paper skirt; bare light peach paper arms with mitten hands; ochre stockings and black paper shoes; joints hidden under overlapping paper pieces.
```

### Prop rules (kept apart from the cards)

| Role | Prop | Hand rule |
|---|---|---|
| Pip | red paper cards | right hand; waves with the left |
| Mai | red spiral sketchbook; yellow paper pencil | sketchbook in the left hand, pencil in the right only while drawing |
| Ông Bảo | brown wooden paper cane | never leaves his right hand: he bows, kneels and sits with the right hand on the cane, gestures with the left, and does not carry or push things |
| Bé Na | yellow paper balloon on a thin grey string | right hand; her short arms need a wide V for overhead gestures |
| Thầy Dũng | silver whistle (worn on the cord) | lifts it with his right hand; hands otherwise empty |
| Cô Lan | green paper book | right hand |

Every prop the beats use is listed in the clip's Props line before the first frame; nothing is spawned mid-clip.

## Style block (verbatim in every clip)

Material lock, one palette line per paper family used, and the mixed-cast sentence when both families appear:

```text
Flat two-dimensional paper cutout stop-motion animation shot straight down onto a tabletop. Every character, prop and scenery element is a separate rigid piece of matte paper with visible paper fibre and slightly irregular cut or torn edges, layered with small soft contact shadows between layers. One warm key light from the upper left. No drawn outlines.
```

```text
Construction-paper palette: mustard, brick red, navy, teal, cream and white paper with black paper details, flat colours with no gradients.
```

```text
Collage palette: kraft brown, newsprint grey, dusty pink, warm ochre, sky blue and cream papers; patterns such as knit, polka dots, plaid and pinstripes appear on clothing and scenery, never on faces.
```

```text
This video mixes two kinds of paper puppet in one frame: construction-paper characters show small brass split pins at their joints, while collage characters hide their joints under overlapping paper pieces. Both kinds share the same matte paper fibre, cut edges, contact shadows and warm light.
```

Motion lock:

```text
Animated on twos like hand-moved stop motion: about twelve distinct held poses per second with slight hand-placed jitter between poses. Pieces only rotate around their joints, slide across the table, or are swapped for replacement pieces; limbs stay rigid and never bend or stretch. Depth comes from paper layers sliding at different speeds. The camera stays parallel to the table and never orbits.
```

## Core rules this style overrides

| Core rule | Override | Reason |
|---|---|---|
| Never leave a character idle | 5A may hold a deadpan pose for half a second to two seconds | The held pose is the joke in cutout comedy; filling it with motion kills the timing |
| Smooth kinetic motion graphics | Motion cadence `on-twos` | Smooth interpolation reads as vector animation, not paper |
| Raised arms in any view | Overhead gestures (cheer, jump, reach up) switch to a front-view body with arms in a V | A big cutout head is taller than the arm; in 3/4 view a raised hand covers the face or hides behind the head |
| Gestures use whichever hand is free | A role with a fixed prop gestures only with the other hand | The gate caught six poses where a pointing hand dropped the grandfather's cane |
| Piano BGM default | The frozen score below | Paper comedy and storybook need their own instruments |

## Text policy

`post-overlay`. Generated clips carry no words, letters or numbers, even on newsprint or book pieces, which show grey bars only. Titles and labels are added in the edit, ideally as cut-paper title cards rendered in code.

## Motion cadence

`on-twos`: about twelve held poses per second, played at 24 FPS.

## Camera grammar

Following `storyboard-template.md`:

- **Transition moves:** hold (the default table shot), lateral truck or pan parallel to the table, slow push-in (the layers grow), pull back, hard cut, and punch-in cut to a close-up.
- **Accent moves:** a snap zoom on a punchline, at most one per clip and in no more than a third of the clips. In 5A only, a camera bump (the table jolts once) can be the accent.
- **Never:** orbit, tilt or dolly-around, because any move that reveals the paper's thickness breaks the flat table. Hold the camera during a demanding body action such as a pass between characters, a kneel or a front-view jump.

## Style bans and posture limits

- No bending or rubbery limbs and no 3D turns. A turn is a flip of the whole puppet or a swap to the front-view body in one step.
- No hand behind the head in 3/4 view: raised hands use the front view.
- A character facing left is a flipped puppet whose right hand is now the far hand: the right arm and anything it holds are drawn behind the body, never swapped onto the near arm.
- Toddler proportions (Bé Na) need a wider overhead V (upper arm about 115° out) than adults, or the hands land on her cheeks.
- A character with a fixed prop (Ông Bảo's cane) never carries or pushes with both hands.

Negatives (append to every clip):

```text
Negative constraints: no smooth vector animation, no 3D rendering, no clay, no felt, no plastic, no glossy surfaces, no paper folding into 3D shapes, no bending or rubbery limbs, no characters turning in 3D, no drawn ink outlines, no photorealistic humans, no extra limbs, no duplicate characters, no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no prop switching hands without a visible pass, no visible words, letters or numbers, no speech bubbles, no dialogue boxes, no subtitles, no captions, no logos, no watermark.
```

## Topic translation

Turn abstract ideas into physical paper props: a growing stack of paper cards for workload, a paper chain for habits, a cut-out bar chart that a character climbs. 5B can use collage metaphors such as old maps, stamps and ticket stubs, as long as no legible text is generated.

## Hook override

- **5A:** use Sudden entry, Reaction before cause or Physics break. The hit is a paper piece slapping onto the table or a puppet flipping, synced to a dry paper slap or woodblock. A held deadpan look counts as the confirmation.
- **5B:** keep hooks gentle, using Partial reveal (a foreground paper layer slides away), Satisfying motion or Visual metaphor. The sound cue is a soft paper rustle or a single music-box note, not an impact.
- In both families, the first frame already shows the cast card and the set layers, with a character mid-action.

## Voice and music

The shared `voice-continuity.md` contract is unchanged: one frozen narrator block per video, off-screen, audio-only. The style never recasts the narrator.

Frozen score: pick one per video, write it in clip 1, and have clips 2–N continue it.

```text
Music (5A): plucky pizzicato strings with light ukulele and dry woodblock at about 104 BPM, playful and unhurried, with a short comic sting only on the punchline. SFX: paper rustle on moves, soft taps when pieces land, a small snip on blinks.
```

```text
Music (5B): a gentle music-box melody over soft fingerpicked acoustic guitar and light glockenspiel at about 84 BPM, warm and unhurried. SFX: soft paper rustle on moves, light taps when pieces land.
```

A mixed cast uses one of the two scores, chosen by tone.

## Phase A additions

Phase A for this style includes:
- the paper family (5A, 5B or a named mix);
- cast cards and prop rules;
- set layers per location (back card, mid layers, foreground strip);
- timed beats with prop transfers;
- exact English VO with its translation;
- the voice block;
- the chosen score.

## Prompt assembly

Each prompt follows `omni-flash-prompt-contract.md` in this order:
1. Output spec.
2. No separate hook line: Clip 1's hook lives in its first frame and first timed beat (Golden Hook section of `storyboard-template.md`).
3. Style block: material lock, palette lines, the mixed-cast sentence if needed, and the motion lock.
4. Full cast cards for every visible role.
5. Set layers.
6. Props line.
7. `First frame:` and `Hands at start`.
8. Three timed beats, each naming its camera move.
9. Quoted VO and the line "Audio voiceover only, strictly no speech bubbles, no dialogue boxes." with the no-add/omit/caption sentence.
10. The voice block.
11. Music: the score in clip 1; in clips 2–N, "continues the identical ... from clip 1, maintaining identical tempo and instrumentation".
12. `Final frame:` and `Hands at end`.
13. Negatives.

Sample package: `samples/paper-cutout.md`.

## Post-production

1. Add titles, labels and subtitles in the edit, as cut-paper cards or plain text in the safe area; never in generation.
2. If a clip comes out smooth rather than stepped, conform it to on-twos in the edit, for example `ffmpeg -i in.mp4 -vf "fps=12,fps=24" out.mp4`, and check that the lip and mouth swaps still land.
3. Match the paper colour and light across clips with one grade, warm and slightly lifted blacks, before stitching.
4. Trim any fade-in at clip starts so each clip opens on its first frame.
5. Optionally lay one continuous external VO and music track over the stitched clips, keeping the paper SFX from generation.
6. In the deterministic-rig route (below), render the puppets in code and composite generated or painted backgrounds behind them.

## Reference images

Paper texture and puppet construction are easier to show than to describe. When the interface accepts reference images, attach the approved sheet for each role (`gallery/cast/sheet-<id>.png`: front, 3/4, walk, signature pose, mouth set, paper swatches) and a background layer card per location to every clip. Treat references as a strong hint, not a guarantee, and check pieces, colours and joints in the footage.

## Alternative: deterministic rig (no video model)

Because the style is rigid pieces plus pivots, it can also be animated exactly in code, using the AI only for the script, VO and optionally the background art. The rig in `gallery/src/` does this:
- SVG paper filters;
- two-piece limbs with split pins;
- walks from CMU motion capture;
- 2-bone IK for gestures;
- feet planted on the ground;
- 12 fps stepped timing;
- replacement mouths;
- one shared pose library across six characters, gated with `tools/posture_gate`.

Offer it when the user needs zero character drift or a long series with one cast.

## Catalog rows

Style matrix:

| Style Key | Style Name | Visual Theme | Best For | Character Design |
|---|---|---|---|---|
| **paper-cutout** | Paper Cutout / Collage (5A Construction Paper, 5B Collage Storybook) | Flat matte paper pieces with fibre, cut or torn edges and contact shadows on layered paper sets; stepped stop motion | Deadpan comedy (5A); gentle stories and children's English (5B) | Rigid two-piece paper limbs on pins, paper-dot eyes, replacement mouths; story-specific cast from frozen cards |

Status row:

| Style | Status | Evidence |
|---|---|---|
| paper-cutout | gated | `gallery/cast-gate-results.md`, `samples/paper-cutout.facts.md`; not tried on Flow |

Setup-gate line (offered only when the user asks for an experimental style):

```text
- `paper-cutout` (experimental, gated, not tried on Flow): flat cut-paper puppets in stop motion, 5A construction-paper comedy or 5B collage storybook
```

## Review checklist

- Paper family chosen; cast cards complete and repeated in full in every clip; the mixed-cast sentence is present when the families mix.
- Footage reads as paper: visible fibre, cut or torn edges, contact shadows, no outlines.
- Limbs stay rigid and rotate at joints; no bending, stretching or 3D turns.
- Stepped stop-motion cadence, not smooth vector interpolation.
- Expressions are swaps; faces keep the same pieces and colours across clips.
- Light direction and shadow side are the same across clips.
- Prop ownership follows the prop rules; no spawning or duplicated pieces.
- No generated text, subtitles or speech bubbles; overlays are listed for post.
- The voice block is identical across clips and the score continues from clip 1.
- Limitations are disclosed: anchors are untested until a Flow test confirms them.
