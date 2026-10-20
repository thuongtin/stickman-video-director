# chibi-anime — Chibi Anime / Q版萌系

> In this repository: the sample package and its lint facts are `samples/chibi-anime.md` and `samples/chibi-anime.facts.md`. Other research files named below (gallery, tracks, gate output, renderer) stay in the project's `style-research/chibi-anime/` folder and are not part of the skill.

Draft style pack for `skills/directing-stickman-videos/references/`, written from `style-pack-template.md`.

```text
Status: gated (2026-10-20). Covers: 3 clips, 16:9, four of the six cast members on screen together, two teddy-bear
hand-offs (Kai to Mimi, Mimi to Bo), a daytime park and the same park at golden hour.
Not covered: 9:16, more than four characters in one shot, night or interior scenes, characters speaking on screen.
Not tried on Flow.
```

Evidence: 121 rig tracks pass `posture_gate.py` with the drawn body and head sizes declared (`gallery/cast/gate-summary.txt`, `gallery/gate-output.txt`), one two-character `--scene` hand-off passes (`gallery/cast/scene/`), and the sample package passes `package_lint.py` with the facts block in [`samples/chibi-anime.facts.md`](samples/chibi-anime.facts.md). No independent review score yet.

## Signature checklist

### Sources

These works are cited from general knowledge of the shows; no frames were re-inspected for this pack.

1. *Isekai Quartet* (TV anime, 2019–): a whole ensemble drawn super-deformed for every shot, not only for gags. Supports the two-heads-tall body, the stubby mitten-hand limbs and telling many characters apart by hair shape and outfit. Runs out on motion: it is limited TV animation, so it says little about how a video model should move these bodies.
2. *Azumanga Daioh* (TV anime, 2002): normal-proportion characters that switch to chibi for reaction cuts. Supports the anime emotion marks (sweat drop, sparkle eyes, spiral eyes) as short timed graphics and the snappy reaction hold. Runs out on the cast: its chibi form is a gag mode, not a design to freeze.
3. *Chibi Maruko-chan* (TV anime, 1990–): everyday-life comedy with small, flat-coloured, thickly outlined characters in simple pastel settings. Supports the flat fill, the soft outline and backgrounds simpler than the characters. Runs out on the eyes: its dot eyes are the opposite of this pack's large highlighted eyes.

How-to sources (proportion ratios, Flow ingredients) are listed in `README.md`; they are not works.

### Five signature traits

| Tag | Trait (visible in a still frame) | Prompt words, repeated in every clip |
|---|---|---|
| `must` | The head is as tall as the whole body below it; short stubby limbs, round mitten hands | "about two heads tall: a large round head as tall as the entire body below it ... short stubby arms ... small round mitten hands, and short legs" (character body) |
| `must` | Flat cel colour with one shadow tone and a thick, soft, dark-brown outline of constant weight | the frozen style block below |
| `must` | Large simple oval eyes with one big and one small white highlight carry the emotion | "large glossy oval eyes, each with one big white highlight and one small highlight, flat color with no detailed iris texture" (character body) |
| `bonus` | Anime emotion marks (sweat drop, sparkle, small spiral, tiny storm cloud) as timed graphics | named in the beat that uses them, never in the anchor |
| `forbidden` | Realistic or teen proportions, glossy 3D or figurine shading, detailed irises | the negative block below |

### Nearest neighbour

Style 4 (Cozy Storytelling) is the nearest catalog style: both are full-colour 2D cartoon storytelling with location changes per segment. Two differences a viewer sees:

1. Style 4 figures have white filled round heads and dark stick limbs with no clothing; chibi characters have skin, hair, outfits and filled limbs.
2. Style 4 faces are small and simple; chibi eyes are oversized with two white highlights, and the head is as tall as the body.

## Frozen style block

Paste verbatim at the start of `Style and environment` in every clip, then the location sentence:

```text
Flat 2D cel-shaded anime animation with a hand-drawn look; thick soft dark-brown outline of constant weight on characters and props; flat colors with one soft shadow tone and no gradients; soft pastel backgrounds built from simple shapes, with fewer details than the characters; the characters' outfit colors stay the most saturated things on screen.
```

Line, fill and shading live here, not in the character anchors.

## Why this style is risky for video models, and the counter-rules

1. **Eye drift.** Style 2 avoids detailed eyes because they trigger bug-eye deformation. Chibi needs big eyes, so describe them as *simple flat shapes* (the character body text). Never request realistic irises, reflections or wet eyes.
2. **Proportion creep toward normal anime.** Models drift from 2 heads tall toward 4–6 heads tall in action shots. Repeat the ratio in plain words every clip and forbid "long legs, tall teen proportions, realistic anatomy".
3. **3D / figurine drift.** "Chibi" also matches vinyl figures and 3D game models. The style block says flat 2D cel-shaded; the negative block says "no 3D render, no CGI, no plastic toy or figurine look, no glossy 3D shading".
4. **Short-arm poses.** A two-head-tall figure cannot reach above its own head or its own eyes; requests like "raises both hands over its head" or "pushes up its glasses" produce stretched or extra arms. Use outward waves, arms out to the sides, a V of arms beside the head, hugging a prop to the chest, hopping, leaning and whole-body squash-and-stretch.
5. **Arms on the body.** In front view the rig first drew the arms inside the same-coloured torso, and a video model copies that as arms fused onto the body. Arms hang beside the torso with a visible gap, sleeves end in a light cream cuff, and the negative block says "no arms fused onto the torso".
6. **Text in eyes and signs.** Anime backgrounds invite shop signs, posters and manga onomatopoeia. See the text policy.
7. **Cast clones.** Cute crowds are tempting. As in Style 4, every cast member is planned, described and assigned to clips, and prompts forbid extra background characters.

## Characters and cast cards

Every character is the shared body plus their own design. Freeze each approved anchor and repeat it verbatim wherever that role appears. Keep pose, action, camera, props and emotion marks out of the anchor: props go in the `Props` and `Hands` lines. A second character differs in silhouette first (hair shape, headwear, outfit), not only in face, so the cast stays distinguishable in wide shots. Anchors are generated by `prototype/cast.py` (`anchor()`); the package uses the same text.

```text
Nori: one chibi anime character, about two heads tall: a large round head as tall as the entire body below it, a small rounded torso, short stubby arms that end in a light cream cuff above small round mitten hands, and short legs; large glossy oval eyes, each with one big white highlight and one small highlight, flat color with no detailed iris texture; small pink blush ovals on the cheeks; a tiny simple mouth; exactly two arms and two legs, and a moving limb replaces its previous pose; expressions change only the eyes, eyebrows, mouth and blush, never the head shape, hairstyle, outfit or proportions; one curled cowlick on a soft dark navy bob with blunt jagged bangs and two side locks; dark-brown eyes; an oversized bright orange hoodie with a front pocket, navy trousers and small white shoes.
```

The other five replace the text after the last semicolon of the shared body:

| Name | Design (after the shared body) | Signature prop (Props line, not anchor) |
|---|---|---|
| Kai | tall spiky rust-red hair pointing upward with no bangs covering the eyes; dark eyes; a small bandage on the left cheek; a green zip-up track jacket over a white tee, charcoal trousers and red sneakers; slightly longer legs than the others | basketball, right hand |
| Mimi | pink hair in two round buns on top of the head with thin side locks and a small yellow star clip; rose-pink eyes; a lavender A-line dress with a white collar, bare legs and purple shoes; slightly shorter than the others | bubble tea, right hand |
| Taro | short messy black hair with two upturned tufts; large round glasses; dark eyes; a cream knit sweater with a white shirt collar, brown trousers and gray shoes | book |
| Hana | long chestnut-brown hair falling past the shoulders with a side part and a small white flower clip on the right side; warm brown eyes; a teal cardigan open over a white top, a red pleated skirt, bare legs and dark brown shoes | sketchbook |
| Bo | the smallest of the group, with a bigger head relative to the body; a round yellow bucket hat over short brown hair; a yellow raincoat with white buttons, light blue trousers and red rain boots | teddy bear |

Model sheets show the signature prop in the hand the package uses (`gallery/cast/model-<name>.png`, `lineup.png`). In beats, write one character per sentence and keep hands out of the first sentence after the VO quote: `hand_ledger.py` ties a hand to the first character named in a sentence.

### Reference images (strongly recommended)

Where the generation tool accepts reference images (Flow "Ingredients", up to three per prompt), attach a front-facing full-body model sheet of each recurring character on a plain background, and optionally a location keyframe. Generate the sheet once from the frozen anchor, approve it with the user, and reuse the same file for every clip. The text anchor still repeats in each prompt.

## Core rules this style overrides

- **Faceless / minimal-face rule (Style 1, Style 2):** overridden. Big expressive eyes are the style; the eye wording above keeps them flat to limit drift.
- **No-idle rule:** a two-second reaction hold with a visible emotion mark is allowed, because the reaction is the joke (as Style 3 does); the character still breathes, blinks or trembles.
- **One location:** Style 4's rule applies; each ten-second segment may establish a new setting, named in Phase A with what carries across the cut.
- **Reaching:** the generic "arms over the head" gestures are banned for this body (see risk 4).

## Text policy: `none`

No words, letters, numbers, signs, posters or manga sound-effect lettering in generated frames; message bubbles and screens stay blank or icon-only. Any title or caption is added in the edit (see post-production), never in the prompt.

## Motion cadence: `smooth`

Generated motion stays smooth; the anime feel comes from timing, not from dropped frames: quick anticipation, a fast action and a short hold. Squash-and-stretch on hops, landings and surprise takes. Asking a video model for on-twos stepping is untested and risks jitter.

## Camera grammar

Follows `storyboard-template.md`: every beat names its main move.

- Transition moves: hold, slow push-in, pull back, lateral track, hard cut. Default framing is medium-wide to full body; chibi reads through silhouette.
- Accent moves: fast push-in on a reaction face only. At most one accent per clip and in no more than a third of the clips; the hook may add one.
- Hold the camera during hand-offs, hops and any demanding body action. No orbit (a turning big-head silhouette drifts) and no camera shake.
- After pushing in, come back out: no three clips in a row whose main move is inward.

## Style bans and posture limits

From 121 gated rig poses (2026-10-20):

- No reaching above the head or to the eyes (pushing up glasses, a hand on the brow): the arms are shorter than shoulder-to-eye. Such poses are marked "not for package beats" on the pose sheets.
- No hand or prop over the face: hold phones and books at the chest; point forward and a little down; cheer with arms in a V beside the head.
- Spread emotion across the body: a lean of the torso, not a single joint pushed past range (neck past 50° down or 60° back, a kick past 125°, heels kicked back past 30° of hip extension).
- A bow pushes the hips back: the head is a third of the body's weight.
- Arms hang beside the torso with a gap, never on it.

```text
Negative constraints: no 3D render, no CGI, no plastic toy or figurine look, no glossy 3D shading, no realistic anatomy, no tall teen or adult proportions, no long legs, no detailed iris texture or realistic eyes, no extra arms or legs, no duplicate characters, no extra background characters, no characters swapping outfits, hairstyles or colors, no knees or elbows bending backward, no limbs changing length, no arms fused onto the torso, no head turned past the shoulders, no swapped left and right hands, no prop switching hands without a visible pass, no arms reaching above the head, no hand covering the face, no manga sound-effect lettering, no visible text, letters or numbers, no logos, no speech bubbles, no dialogue boxes, no watermark.
```

Follow `posture-gate.md`: hands named from the character's own side, `Hands at start` / `Hands at end` lines in every clip that holds something. Write `time cut` after the hands in a ledger line, not before them.

## Opening hook override

Prefer Reaction before cause, Sudden entry and a cartoon Physics break; the hit is a small physical event (a bounce, a drop, a squash) or an emotion mark popping in. The sound cue is a cartoon boing, pop or sparkle chime, never a bass hit or impact. The sample uses Sudden entry: a basketball bounces into Bo's back at about 1.5 seconds.

## Audio

Apply `voice-continuity.md` unchanged: one off-screen narrator, full voice block repeated in every clip. Characters do not speak on screen unless the user approves dialogue. Frozen score, written once in clip 1 and continued verbatim afterwards:

```text
Audio: voiceover clearly audible over light ukulele and soft glockenspiel with a playful, gentle tempo; synchronized cartoon SFX on actions.
```

## Post-production

1. Stitch the clips in order at 24 FPS; trim up to a quarter second at each join if a clip starts on a settling frame.
2. Check each character's outfit colours and hair shape across joins against the model sheets, and the hands at every pass against the `Hands` lines.
3. Keep the music bed continuous across joins; duck it under the voice if a clip's music level differs.
4. Optional captions or a title are added here, in the edit, outside the character area.

## Sample package

[`samples/chibi-anime.md`](samples/chibi-anime.md): 3 clips, Bo, Kai, Mimi and Nori, teddy bear passed Bo → Kai → Mimi → Bo. `package_lint.py` PASS (facts: [`samples/chibi-anime.facts.md`](samples/chibi-anime.facts.md)), `tests/verify-opening-hook.py` PASS, `hand_ledger.py` PASS. The Kai → Mimi hand-off is also gated as a two-character scene (`gallery/cast/scene/`).

## Catalog rows (ready to add)

Style matrix:

```text
| **chibi-anime** | Chibi Anime (Q版萌系) | Flat cel-shaded 2D anime, thick soft dark-brown outline, soft pastel settings simpler than the characters | Everyday-life comedy, study and productivity tips, relationship sketches, children's and language content, reaction-heavy shorts | About two heads tall, big highlighted eyes, stubby limbs with mitten hands, a frozen cast told apart by hair and outfit |
```

Status:

```text
| chibi-anime | gated | 121 rig tracks and one --scene hand-off pass posture_gate; sample package passes package_lint (samples/chibi-anime.facts.md). Not tried on Flow |
```

Setup gate (offered only when the user asks for an experimental style):

```text
- `chibi-anime (Chibi Anime / Q版萌系, gated, experimental)`: two-heads-tall anime characters with big highlighted eyes in flat pastel 2D settings; a frozen multi-character cast
```

## Final check (in addition to the shared Phase B checks)

- Every prompt starts `Style and environment` with the frozen style block and repeats the full anchor of every character on screen and the negative block.
- No anchor names a prop; props are in `Props` and `Hands` lines.
- No beat asks a character to reach above its own head or to its face.
- Every beat names its camera move; holds during hand-offs.
- Every emotion mark is scoped to one timed beat.
- If reference images are used, the same approved model sheet file is attached to every clip, showing props in the hands the package uses.
- Generated proportions and arm separation are checked on action frames and at every hand-off.
