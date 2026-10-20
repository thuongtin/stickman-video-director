# Watercolor Storybook (`watercolor-storybook`) / 水彩绘本风

> In this repository: the sample package and its lint facts are `samples/watercolor-storybook.md` and `samples/watercolor-storybook.facts.md`. Other research files named below (gallery, tracks, gate output, renderer) stay in the project's `style-research/watercolor-storybook/` folder and are not part of the skill.

Draft style pack for `skills/directing-stickman-videos/references/`, written to `style-pack-template.md`. It replaces `style-5-watercolor-storybook.draft.md`.

```text
Status: gated (2026-10-20). Covers: 3 clips at 16:9, six recurring characters (two children, a mother, a grandfather with a cane, a rabbit, a bear cub), two character-to-character hand-offs (lantern, carrot), parallax trucks, holds, one slow push-in, one slow pull back.
Not covered: 9:16, crowds, fast action, rain or water in motion, close-ups of hands.
```

Evidence: 105 cast pose tracks and 2 two-character `--scene` shots pass `posture_gate.py` with no warnings (`gallery/cast/gate-results.txt`); the sample package `samples/watercolor-storybook.md` passes `tools/package_lint/package_lint.py` (facts block `samples/watercolor-storybook.facts.md`). No independent review score yet, so no score is claimed.

## Visual identity

A gently animated children's picture book. Soft transparent watercolor washes on warm off-white cold-press paper, with a thin, slightly irregular dark sepia ink contour around characters and key props. Pale paper is left unpainted for highlights, sky glow and negative space. Edges show soft wet blooms and darker pigment rims; large areas show gentle granulation. Backgrounds are looser and paler than characters; the character is the most saturated, most clearly outlined element in frame.

Feel: quiet, warm, unhurried. Best for bedtime-style stories, children's education, fables, gentle life lessons, family and nostalgia topics, and emotional explainers that need tenderness rather than kinetic density.

## Signature traits

| # | Trait (visible in a still) | Tag | Prompt wording (verbatim in every clip) |
|---|---|---|---|
| 1 | Transparent washes on visible warm off-white paper, with unpainted paper as the highlights | `must` | "Soft transparent washes, gentle granulation, wet-edge blooms and pale unpainted paper highlights" on "warm off-white cold-press paper" (environment block) |
| 2 | A thin, slightly irregular dark sepia ink contour around every character | `must` | "drawn in soft watercolor with a thin, slightly irregular dark sepia ink outline" (every anchor) |
| 3 | Backgrounds looser, paler and lower in contrast than the characters | `must` | "Backgrounds are looser, paler and lower in contrast than the character" (environment block) |
| 4 | Multiplane depth: soft out-of-focus foreground, far layers paler | `bonus` | "foreground is soft and slightly out of focus" plus the parallax camera line in the beat |
| 5 | Flat colour fills, thick black outlines, glossy or 3D shading | `forbidden` | "no glossy vector flat color, no thick black cartoon outlines, no 3D CGI or plastic rendering" (negatives) |

## Nearest neighbour

Style 4 (Cozy Storytelling). Visible differences:
1. Style 4 characters are white-filled heads and torsos with dark stick limbs; these are fully painted children's-book characters with clothes, fur and faces in wash.
2. Style 4 environments are full-colour 2D cartoon fills; here everything is transparent wash on visible paper grain with unpainted highlights. A stick figure in a watercolor room is Style 4 with a filter, not this style.

## Sources and where they stop

Prompts name no artist, studio, book or character. The cast borrows no named character's look or costume colour combination: a brown bear cub in red with a honey jar and a cream rabbit in a blue jacket were redesigned in the audit round (see `gallery/cast/characters.md`).

| Source | What it supports | Where it stops |
|---|---|---|
| Beatrix Potter's tales | Transparent wash over light ink, unpainted paper, small animals in clothes | Her characters and their costumes are not carried over; studied from reproductions only |
| E. H. Shepard's drawings for A. A. Milne | Light, broken pen line with a little wash; lots of empty paper | Line quality only; no bear-in-red, no honey pot |
| Anita Jeram, Guess How Much I Love You | Soft wash animals, a large pale ground, two-character warmth | Stills only; no motion evidence |
| Quentin Blake | Loose, quick ink with splashed wash | His line is far looser than ours; we keep a steady contour for model stability |
| Ernest & Celestine (2012 film) | The closest moving reference: watercolor backgrounds, ink outlines that hold in motion, slow camera | Only trailers and stills were looked at; frame-by-frame texture behaviour not studied |
| The Tale of the Princess Kaguya (2013) | Unfinished paper, line that breaks around fast action | Its fast sketchy passages are out of scope; we avoid fast action |
| Song of the Sea (2014) | Multiplane depth and paper texture layers | Its flat graphic shapes are closer to Style 4 than to wash |

Prototype evidence: an SVG wash/ink/paper-grain mock with four parallax layers (`prototype/parallax-demo.mp4`). It shows composition and parallax, not real watercolor quality.

## Character anchors and cast cards

The frozen anchors live in one place, `gallery/cast/characters.md`, and are repeated verbatim in every clip where a role is on screen. Mia's anchor is the default child anchor:

```text
Mia, a small storybook girl drawn in soft watercolor with a thin, slightly irregular dark sepia ink outline. Round head with a light peach wash, short tousled brown hair, two small dark dot eyes, a short curved smile and rosy watercolor cheeks; no nose detail, no detailed pupils or eyelashes. Wears a mustard-yellow raincoat that flares slightly at the hem, with sleeves a shade darker than the coat, a short red knitted scarf with one loose end, dark brown legs and small red boots. Simple rounded body about three heads tall. Keep the same proportions, outfit colors, ink line weight and wash softness in every shot. Exactly two arms and two legs; a moving limb replaces its previous pose. Expressions change only the dot eyes, eyebrows, mouth and cheek blush.
```

Rules carried over from Style 4: one anchor per recurring role, repeated verbatim; action, camera and props stay outside the anchor; no spawned background extras. Props (Ông Bảo's cane, the lantern, the teddy bear, the carrot, the kite, the basket) are listed per clip under `Props:` with their hand rule, never inside an anchor. Write one character per sentence in beats; the hand ledger ties a hand to the first character a sentence names.

Why an outline instead of a pure wash figure: pure wet-on-wet figures drift and melt between frames; the ink contour gives the model a stable silhouette to hold, while the wash supplies the style.

## Environment specification

```text
Hand-painted watercolor storybook illustration on warm off-white cold-press paper. Soft transparent washes, gentle granulation, wet-edge blooms and pale unpainted paper highlights. Backgrounds are looser, paler and lower in contrast than the character; foreground is soft and slightly out of focus. Muted natural palette of sky blue, sage green, warm ochre, dusty rose and soft brown, with the character's mustard yellow and red as the strongest colors. The paper grain stays fixed to the frame and does not crawl, shimmer or move with the characters.
```

Append one `Setting:` sentence per clip. Each ten-second segment is a new picture-book page by default (meadow, garden at dusk, forest path, porch at night); the page-turn wipe or a slow fade through paper white is the cut.

## Core rules this style overrides

| Core rule | Override | Reason |
|---|---|---|
| A visual change every two to three seconds; four visual devices per clip | Three timed beats still apply, but a beat may be one character action plus continuous parallax drift | Wash textures crawl when the frame changes quickly; the style reads as calm |
| Camera accents allowed at reveals | No accent moves at all; the hook uses a slow pull back | Fast moves resample the paper and break the picture-book feel |

## Text policy

`post-overlay`. Clips show no words, letters, numbers or book text (picture-book settings invite lettering on books and signs). Any title or line of text is added in post-production on the paper margin.

## Motion cadence

`smooth`, slow. Ease in and out on every action; one main action per character per beat; small ambient life (drifting leaves, a lantern swinging, a scarf end). No on-twos or stepped timing: held drawings read as frozen paint.

## Camera moves

Following the camera grammar in `storyboard-template.md`:

- Allowed: hold, slow lateral parallax truck (the signature: far layers slowest, foreground fastest), slow push-in, slow pull back, page-turn or paper-white cut.
- At most one accent per clip and accents in no more than one third of clips; this style uses none by default.
- Never three inward moves (push-ins) in a row across clips; truck, hold or pull back in between.
- Hold the camera during demanding body actions: hand-offs between characters, passing a prop between hands, kneeling, bending to a child, setting something down.
- Name the move in every beat ("Camera: hold.", "Camera: slow lateral parallax truck right; …").

## Style bans and posture limits

Style negatives, repeated in every clip:

```text
Negative constraints: no photorealism, no 3D CGI or plastic rendering, no glossy vector flat color, no anime cel shading, no thick black cartoon outlines, no digital airbrush gradients, no oil paint impasto, no crawling or flickering paper texture, no melting or smeared limbs, no extra characters, no visible words, letters, numbers or book text, no speech bubbles, no dialogue boxes, no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no prop switching hands without a visible pass, no logos or watermarks.
```

Moves the cast cannot do, found with the posture gate (`gallery/cast/README.md`):
- Big-headed characters (Mia, Tí, Pip) tip over in deep bows and when leaning back to look up: bow with the hips back and knees soft; look up with the head, not the torso.
- Both arms straight overhead in side view hide the face, and in front view the hands disappear behind the big head: open the arms into a V beside the head, or reach forward at shoulder height.
- Ông Bảo keeps the cane in his right hand, so he does not run, jump, cheer with both arms, kneel or sit on the floor; he points, waves and gives with his left hand.
- Sitting down goes through a crouch; lying down goes through a crouch; nobody drops straight from standing.
- A hand-off between two characters is its own beat, with the camera held, the giver's hand named, the receiver's hand named, and the giver's hand letting go.

## Opening hook override

Gentle patterns only: Partial reveal (start close on a glowing or small detail, pull back by about 2 s), Reaction before cause, Satisfying motion. The hit is a soft visual event (a light coming on, a reveal by a slow pull back); the sound cue is a single soft note or an action sound, never an impact or bass hit. The first frame already shows the character mid-action in the page's setting.

## Audio

Shared `voice-continuity.md` applies unchanged. Default narrator: the bright female profile, close and dry. Frozen score line for clip 1, which later clips continue verbatim:

```text
Music: soft fingerpicked acoustic guitar with a light music-box melody, slow and warm at about 70 beats per minute, mixed under the voice.
```

Clips 2–N: "Music: seamlessly continues the identical soft fingerpicked acoustic guitar and light music-box melody from clip 1, same tempo and instrumentation, mixed under the voice." SFX stay gentle and organic (birds, crickets, footsteps on gravel, page rustle).

## Post-production steps

1. Join clips with a page-turn wipe or a 0.5 s fade through paper white; do not cross-dissolve wash into wash.
2. Overlay one shared static paper-grain plate at low opacity over the whole video, so grain that crawls between generations is masked by a fixed texture.
3. Grade all clips to the same warm off-white paper tone; do not raise contrast (it kills the wash).
4. Add any title or text as a post overlay on the paper margin (text policy `post-overlay`).
5. Check the risky moments frame by frame: the two hand-offs, Ông Bảo's cane hand, Pip's ears and Toby's vest colour.

## Sample package

`samples/watercolor-storybook.md`: three standalone prompts (garden at dusk, forest path, home porch), every section the prompt contract asks for. Results on 2026-10-20: `package_lint.py --clips 3 --anchor <environment block>` PASS 0 red 0 yellow (facts `samples/watercolor-storybook.facts.md`), `hand_ledger.py` PASS (main and the shared gate copy), `tests/verify-opening-hook.py <package>` PASS.

## Catalog rows (draft, for when the style is merged)

Matrix row in `style-catalog.md`:

```text
| **watercolor-storybook** | Watercolor Storybook (水彩绘本风) | Transparent watercolor washes on warm off-white paper, unpainted highlights, paler backgrounds, slow multiplane parallax | Bedtime stories, children's education, fables, family and nostalgia | Painted picture-book characters (children, adults, small animals) with a thin sepia ink outline, dot eyes, rosy cheeks |
```

Status row:

```text
| watercolor-storybook | gated | 105 pose tracks and 2 `--scene` hand-offs pass the posture gate; the 3-clip sample package passes package_lint (`watercolor-storybook.md`) |
```

Setup-gate line in `SKILL.md` (offered only when the user asks for an experimental style, naming its level):

```text
  - `watercolor-storybook (Watercolor Storybook / 水彩绘本风, experimental: gated)`: transparent watercolor washes on paper, painted picture-book characters with a thin sepia ink outline, slow parallax pages
```
