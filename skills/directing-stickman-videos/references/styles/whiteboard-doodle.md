# Whiteboard Doodle — Draw-On Explainer (style pack draft)

> In this repository: the sample package and its lint facts are `samples/whiteboard-doodle.md` and `samples/whiteboard-doodle.facts.md`. Other research files named below (gallery, tracks, gate output, renderer) stay in the project's `style-research/whiteboard-doodle/` folder and are not part of the skill.

```text
Status: gated (2026-10-20). Covers: one 3-clip 16:9 package with three characters (Bean, Candy, Mr. Square) and two balloon
passes; cast sheets, expressions and posture tracks for six characters; one two-character scene track (the balloon pass).
Not covered: 9:16, eraser-only beats in a cast package, readable handwriting, crowds, night or colored boards.
Not tried on Flow.
```

Drafted with `references/style-pack-template.md` (repo main, PR #5). Evidence: posture gate reports in `gallery/report.md` (Bean poses) and `gallery/cast/cast_report.md` (cast), scene track `gallery/scene/`, package lint facts in [`samples/whiteboard-doodle.facts.md`](samples/whiteboard-doodle.facts.md). Not scored; no independent review yet.

## What makes this a different style

Styles 1–4 show finished drawings that move. This style shows **the act of drawing**: a marker draws the idea in sync with the narration, the doodle then comes alive, and the next idea is drawn beside it on the same board. The viewer watches an explanation being built.

## Sources

Studied from memory of the works and their public descriptions; no frame-by-frame review was done in this thread.

1. **RSA Animate, "Changing Education Paradigms"** (Cognitive Media for the RSA, 2010, over a Ken Robinson talk). Supports: a real hand drawing on a white surface in sync with speech, stroke-order reveals, the camera sliding to clean board, a final pull-back over the whole board. Runs out: it leans on handwritten keywords (our no-text rule drops them), its people are one-off caricatures rather than a recurring cast, and its drawing speed is far beyond what a video model holds.
2. **MinutePhysics** (Henry Reich, YouTube, from 2011). Supports: black marker on white with one or two accent colors, sped-up drawing synced to narration, simple recurring stick characters, limited animation by redrawing. Runs out: it is paper, not a board, usually without a visible hand, and much of it is labeled diagrams.
3. **Mike Rohde, *The Sketchnote Handbook*** (2012). Supports: a marker grammar for drawing people and objects fast (simple bodies, a few colors, consistent line weight) and telling characters apart by shape. Runs out: static pages, nothing on motion or timing.

## Signature traits

1. `must` — A physical matte whiteboard fills the frame, with faint gray ghosting of old marks; all line art is black marker with an irregular hand-drawn path and medium, consistent weight.
2. `must` — Lines draw on exactly under a marker tip in stroke order (outline first, details after); nothing fades in or pops in.
3. `must` — Characters and props are outlines left white inside; color comes only from three accent markers (red, blue, green) on small areas.
4. `bonus` — A realistic drawing hand at the frame edge that interacts with the doodles: draws a ladder the character climbs, wipes a rain cloud away with the side of its fist.
5. `forbidden` — Painted, textured or full-color backgrounds, shading, gradients, 3D, paper or chalkboard texture, and letters or pseudo-text generated on the board.

## Nearest neighbour

Style 1 Light (white canvas, monochrome line, a few accents). Visible differences: (a) here the drawing process and the drawing hand are on screen, there only finished lines move; (b) here the surface is a physical board with marker ink density and ghosting, there a flat digital white. The cast also has faces and costume silhouettes, which Style 1 does not.

## Frozen style block

Repeat verbatim in every clip (lint: `--anchor`).

```text
Board: a matte white whiteboard fills the entire frame, seen flat and front-on, soft even daylight, very faint gray ghosting of old erased marks. All drawings are black whiteboard-marker line art with slightly irregular hand-drawn strokes, natural ink density and rounded line ends, medium consistent line weight; characters and props are outlines left white inside. Lines appear exactly under the marker tip in natural stroke order; nothing appears ahead of the tip and nothing fades in. The only other marker colors are red, blue and green, used on small areas such as a blush, a bow, a tie, a collar, a scarf, a balloon, a small circle or an arrow. No painted background, no shading, no gradients, no 3D.
```

```text
Drawing hand: one adult right hand holding a black whiteboard marker with the cap off enters from the lower right; plain dark sleeve cuff at the frame edge, no rings, no watch, five natural fingers, one marker. It stays at the edge of the drawing and leaves frame while the doodles move.
```

Choose the hand mode once per video in Phase A: **hand on** (default, block above), **ghost marker** (a marker tip alone draws; use when hands deform in tests) or **no tool** (lines draw themselves; most robust, least charm). The hand is a tool, not a character: it never waves, points at the viewer or gestures as a speaker.

## Cast cards

Full blocks, repeated verbatim in every clip where the character is on screen. Source of truth: `gallery/cast/cast_meta.json` (written by `gallery/cast_rig.py`); sheets in `gallery/cast/index.html`. Bean is the default lead. The cast differs by silhouette (bean / tall rectangle / small triangle dress / square head and wide jacket / round body / box), not by color alone. A prop belongs to a rule, not to the design: the anchor never puts a prop in a hand.

### Bean (Đậu)

Role: Nhân vật chính, tò mò, dễ thương. Prop rule: Bean never holds a marker; only the drawing hand does. His hands are free unless a beat hands him something.

```text
One hand-drawn whiteboard doodle character in black marker ink called Bean: a large round head with one small curly hair loop on top, two small solid dot eyes, short curved eyebrows, a small smile line and two tiny red marker blush strokes on the cheeks; below it a bean-shaped body outline, slightly narrower at the top, left white inside; two thin curved noodle arms ending in small round hollow hands; two short leg lines ending in small rounded shoe shapes. No clothing and no other hair. The head is about as wide as the body and about one third of the total height. Slightly irregular hand-drawn strokes with medium, consistent marker weight. Exactly two arms and two legs; a moving limb replaces its previous pose. Expressions change only the eyes, eyebrows and mouth; head size, bean body and proportions stay the same in every shot.
```

### Ms. Pencil (Cô Chì)

Role: Cô giáo cao gầy, cầm thước chỉ. Prop rule: Her thin blue pointer stick stays in her right hand.

```text
One hand-drawn whiteboard doodle character in black marker ink called Ms. Pencil: a tall thin woman with a small oval head, a straight solid black bob haircut with a fringe, round glasses, two small solid dot eyes and a small smile line; below it a long narrow rectangle body outline left white inside, with a blue marker collar; two long thin arms ending in small round hollow hands; two long thin leg lines ending in small black shoes. No blush and no other hair. Her head is about one quarter of her height, and she is the tallest of the cast. Slightly irregular hand-drawn strokes with medium, consistent marker weight. Exactly two arms and two legs; a moving limb replaces its previous pose. Expressions change only the eyes, eyebrows and mouth; head size, narrow body and proportions stay the same in every shot.
```

### Candy (Bé Kẹo)

Role: Em bé nhỏ, hiếu động, cầm bóng bay. Prop rule: Her red balloon on a string stays in her right hand until a beat passes it to someone.

```text
One hand-drawn whiteboard doodle character in black marker ink called Candy: a small child with a big round head, two short solid black pigtails tied with tiny red bows, two small solid dot eyes, short curved eyebrows, a wide smile line and two tiny red marker blush strokes on the cheeks; below it a short triangle dress outlined in green marker with a dotted green waistline, left white inside; two short thin arms ending in small round hollow hands; two short leg lines ending in small rounded black shoes. No other hair and no other clothing. The head is wider than the top of the dress, and she is about three quarters of Bean's height. Slightly irregular hand-drawn strokes with medium, consistent marker weight. Exactly two arms and two legs; a moving limb replaces its previous pose. Expressions change only the eyes, eyebrows and mouth; head size, triangle dress and proportions stay the same in every shot.
```

### Mr. Square (Sếp Vuông)

Role: Ông sếp vuông vức, xách cặp. Prop rule: His black briefcase stays in his left hand in every shot.

```text
One hand-drawn whiteboard doodle character in black marker ink called Mr. Square: a stocky man with a square head with rounded corners, a solid black side-parted hair cap, two small solid dot eyes, short eyebrows and a short flat black moustache above a small mouth line; below it a wide rectangle jacket outline with a V collar, left white inside, and a solid blue marker tie; two thin arms ending in small round hollow hands; two straight leg lines ending in small black shoes. No blush and no other hair. The head is narrower than the jacket, and he is the widest of the cast and about as tall as Bean. Slightly irregular hand-drawn strokes with medium, consistent marker weight. Exactly two arms and two legs; a moving limb replaces its previous pose. Expressions change only the eyes, eyebrows and mouth; square head, jacket and proportions stay the same in every shot.
```

### Granny Round (Bà Tròn)

Role: Bà cụ hiền, chống gậy. Prop rule: Her simple hooked walking cane stays in her right hand; when she leans on it, its tip rests on the ground.

```text
One hand-drawn whiteboard doodle character in black marker ink called Granny Round: a short round grandmother with a round head, a small round hair bun on top and a curved hairline, round glasses, two small solid dot eyes and a gentle smile line; below it a wide round body outline left white inside, with a red marker scarf at the neck; two short thin arms ending in small round hollow hands; two short leg lines ending in small black shoes. No blush. The body is wider than the head, and she is a little shorter than Bean. Slightly irregular hand-drawn strokes with medium, consistent marker weight. Exactly two arms and two legs; a moving limb replaces its previous pose. Expressions change only the eyes, eyebrows and mouth; round head, round body and proportions stay the same in every shot.
```

### Robo Stroke (Robo Nét)

Role: Rô-bốt vuông, cầm cờ lê. Prop rule: His wrench stays in his right hand.

```text
One hand-drawn whiteboard doodle character in black marker ink called Robo Stroke: a boxy robot with a square head with rounded corners and a small black bolt on each side, one thin antenna with a small green ring tip, two small solid dot eyes and a simple mouth line; below it a rectangle box body outline left white inside, with two small green marker dial circles and one short line on the chest; two thin stick arms ending in small round hollow hands; two short stick legs ending in flat black rectangle feet. No blush and no hair. The head is narrower than the body, and he is a little shorter than Bean. Slightly irregular hand-drawn strokes with medium, consistent marker weight. Exactly two arms and two legs; a moving limb replaces its previous pose. Expressions change only the eyes, eyebrows and mouth; square head, box body and proportions stay the same in every shot.
```

When the drawing hand draws a character on screen, describe the stroke order once (for Bean: head, hair curl, eyes, eyebrows and mouth, blush, bean body, arms and hands, legs and shoes). After the reveal the character keeps that design.

## Core rules this style overrides

- **Narration length**: about 18–22 VO words per 10-second clip instead of 20–25, to leave drawing time. Split the VO across the three beats so each drawn noun lands on its word.
- **One realistic element**: the drawing hand is the only non-doodle thing on screen; everything else follows the marker grammar.
- **Characters do not speak**: one off-screen narrator; the voice block from `voice-continuity.md` is kept unchanged.
- **Locations**: a place is sketched with a few lines on the same board, never painted; changing place means sliding to clean board or one full eraser wipe.
- **Idle beats**: a held doodle still boils gently; while the hand draws, the characters may hold a pose for up to three seconds.

## Text policy

`blank-zone`. Generate no letters or numbers. Keep one named part of the board blank in every clip (default: the upper-right third) and list 2–4 word overlay phrases in the post-production note.

## Motion cadence

`on-twos`. Doodles move in held key poses with a gentle hand-drawn line boil, like a flipbook drawn on the board. Marker strokes themselves draw on smoothly.

## Camera moves

Following the camera grammar in `storyboard-template.md`; every beat names its move.

- **Hold** is the default: while lines draw on and while a character does a demanding action (a hand pass, a turn, a climb).
- **Transition moves**: lateral track along the board to clean space (board travel), slow pull back to show more of the board, hard cut on a full eraser wipe.
- **Accent**: at most one fast push-in on a payoff, in at most one clip of three. Never shake, orbit or tilt: a flat board reveals the trick.

## Style bans and posture limits

- Bans: everything tagged `forbidden` above; extra doodle characters; a character borrowing another's features; more than one marker on screen; a doodle holding a marker beside the drawing hand.
- Big-head characters (Bean, Candy; head about a third of the body mass): no straight overhead reach in side view, because the arm crosses the face. Raised arms open into a V; jumps swing the arms forward and back below the face; bows stay at about 30° with the hips pushed back; cheering hands stay off the cheeks.
- Kicks, stomps and cross-legged sits are drawn side-on; a front view cannot bend a knee sideways.
- Sitting, leaning, pushing and pulling name what holds the body up: a stool, a wall, a rope, Granny Round's cane.
- Robo Stroke keeps human joint limits so the video model sees normal arms.
- Side views: facing screen right shows the character's right side to the camera; facing screen left shows the left side. A pass between two characters uses each character's camera-side hand where possible.
- Shared posture negatives (in the negative block below): no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no prop switching hands without a visible pass.

## Negative block

```text
Negative constraints: no painted or full-color backgrounds, no paper texture, no chalkboard, no glass reflections, no 3D, no shading or gradients, no lines appearing ahead of the marker tip, no whole-drawing fade-ins, no morphing of drawings into other drawings, no extra hands, no deformed fingers, no more than one marker in hand, no extra doodle characters, no character taking another character's features, no dark-filled bodies, no visible letters, numbers, scribbled pseudo-text, captions, subtitles, logos or watermarks, no speech bubbles, no dialogue boxes, no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no prop switching hands without a visible pass.
```

## Opening hook

Suits: **Visual metaphor** drawn on the board (a rain cloud over a character, a cage drawn around them), **Satisfying motion** (one perfect stroke completing a shape), **Partial reveal** (start tight on a half-drawn shape, pull back by 2s), and **Sudden entry** when the drawing hand enters and changes the drawing. The first frame always has a drawn character already on the board; never open on an empty board. Loudness: soft. The hit is a marker squeak, a cap click, a small pop or a single pluck, never a bass hit or impact boom.

## Voice and music

The voice block follows `voice-continuity.md` unchanged and is chosen per video. The score is frozen:

```text
light, playful ukulele with soft pizzicato strings, gentle and curious; synchronized marker squeaks on every stroke and a small pop when a doodle comes alive
```

Clip 1 sets it; clips 2–N say the identical score continues from clip 1 with identical tempo and instrumentation.

## Post-production steps

1. Review every clip at the risky moments before editing: lines popping in ahead of the tip, the drawing hand's fingers and marker count, hand passes between characters, a character changing design after the reveal. Regenerate failing clips.
2. Trim and stitch on the planned joins (board slides or matching final/first frames).
3. Add the overlay phrases in the blank zone, timed to the VO, with a handwriting font or scanned real marker strokes.
4. Optional finale: build the whole-board pull-back from real frames of the clips, not from a generated wide shot.
5. Mix: VO on top, score under it, marker squeaks kept; normalize loudness.
6. Subtitles, if wanted, as a separate track or burned in at this step only.

## Sample package

[`samples/whiteboard-doodle.md`](samples/whiteboard-doodle.md): three clips, Bean, Candy and Mr. Square, two visible balloon passes, Mr. Square's briefcase fixed in his left hand. Lint facts: [`samples/whiteboard-doodle.facts.md`](samples/whiteboard-doodle.facts.md). The older Bean-only `sample-prompts-30s.md` is superseded.

## Catalog rows (ready, not merged)

| Style Key | Style Name | Visual Theme | Best For | Character Design |
|---|---|---|---|---|
| **whiteboard-doodle** | Whiteboard Doodle (Draw-On Explainer) | Matte white board, black marker line art drawn on by a hand, red/blue/green marker accents, faint ghosting | Step-by-step explainers, habits and ideas built up piece by piece, light social stories | Bean: big round head with a hair curl, bean-shaped body, noodle arms; optional cast of five shape-distinct doodles |

| Style | Status | Evidence |
|---|---|---|
| whiteboard-doodle | gated | Posture gate reports and lint facts linked in `whiteboard-doodle.md`; not tried on Flow |

Setup gate line: `whiteboard-doodle` — experimental (gated); offer only when the user asks for an experimental style, and say it has not been tried on Flow.
