# Vietnamese Social-Media Comic Strip in Motion (draft style pack, slug `vn-webcomic`)

> In this repository: the sample package and its lint facts are `samples/vn-webcomic.md` and `samples/vn-webcomic.facts.md`. Other research files named below (gallery, tracks, gate output, renderer) stay in the project's `style-research/vn-webcomic/` folder and are not part of the skill.

```text
Status: gated (2026-10-20). Covers: 3 clips, 16:9, two characters per clip, one stool held with both hands,
a glass set down on a table, a seated character, a reaction cut; poses for six characters; one 4-character
motion test (table pass). Not covered: 9:16, crowds, night scenes, more than two characters in one prompt.
Not tried on Flow.
```

Evidence: gate report `gallery/gate-v2.txt` (73 poses, including Mèo Mướp pointing with his far right hand while facing left, as in clip 2) and `motion-test/gate-v2.txt` (`--scene`, 4 characters); lint facts block `samples/vn-webcomic.facts.md`; hand ledger `prompt-package/ledger-output.txt`. Research notes, sources and gallery: `README.md` next to this file (in Vietnamese).

## What the format is

The look of the short gag comics that spread on Vietnamese Facebook and Instagram pages: small round animal characters, thick even outlines, flat pastel colors, tiny dot-eyed faces that are calm most of the time and snap into big empty eyes when the character's brain "stops". Each strip is a few panels about an everyday situation (a stool, a glass of iced tea, school, a bánh mì), and the joke is a character taking something too literally, or a reaction that makes no logical sense, delivered with a straight face.

In motion, each comic panel becomes one held beat. The empty space before the last panel becomes about one second of silence with a frozen face, and the punchline pose snaps in and is held, never cut away at once.

Use it for short relatable gags, wordplay that can be shown literally, slice-of-life Vietnamese neighborhood stories, and one-joke clips for Reels/Shorts.

## Originality

This style takes the spirit of Vietnamese webcomics (round animals, dot eyes, deadpan absurd humor, everyday Vietnamese life), not any comic's designs. Never name an existing comic, creator or character in a prompt. The sample cast avoids the best-known species and signatures of that scene on purpose: no swallows or small blue birds, no rabbits, no hats, no bowler hats or canes as a gag prop on a bird. (Cô Vịt is a white duck: a different silhouette, colour and role.) The negative list carries `no resemblance to any existing comic or webcomic character` and `no hats`.

## Sources

| Work | What it supports | Where it runs out |
|---|---|---|
| Én (Trần Tuấn Dũng, 2018–): [Znews](https://znews.vn/en-khung-vao-vung-sang-tao-moi-post1690153.html), [Thanh Niên](https://thanhnien.vn/ba-tac-gia-truyen-tranh-viet-chia-se-chuyen-nghe-sau-nhung-net-ve-185260618084727133.htm) | Humour from absurd, non-logical reactions, idioms read literally, wordplay, reversed endings; a hero described in 2–3 keywords; the "forgot his brain" blank reaction | Press covers the humour and the business, not the drawing; line and panel notes are my reading of the strips |
| Thỏ Bảy Màu (Huỳnh Thái Ngọc): [Vietcetera](https://vietcetera.com/en/father-of-the-seven-colored-rabbit-first-dont-compromise), [Vietcetera list](https://vietcetera.com/amp/vn/cuoi-la-ca-nguoi-voi-9-fanpage-giai-tri-hai-huoc-bac-nhat-tai-viet-nam) | A tiny expressionless lead whose deadpan line in an awkward situation is the joke; a face of "little black eyes and rosy cheeks"; consistent design as the reason readers follow | No source on panel timing |
| Vàng Xám Comic: [Vietcetera list](https://vietcetera.com/amp/vn/cuoi-la-ca-nguoi-voi-9-fanpage-giai-tri-hai-huoc-bac-nhat-tai-viet-nam) | An animal duo split by temperament (a loud one and a serious one) with short, witty exchanges in family and neighbourhood life: the model for a cast that differs by personality and silhouette, not only colour | One article paragraph; no drawing analysis |
| Quỳnh Aka: same list | A big-headed lead built on one exaggerated feature and illogical-but-forceful arguments: one strong silhouette feature per character | Same |

## Signature traits

| # | Trait (visible in a still) | Tag |
|---|---|---|
| 1 | Small round animals about two heads tall with one thick, even black outline and flat pastel fills | must |
| 2 | Tiny black dot eyes on a calm face; for the big reaction the dots snap into two large empty white circles | must |
| 3 | Everyday Vietnamese street objects in flat shapes: red plastic stools, a low tea table, ribbed iced-tea glasses, áo bà ba | must |
| 4 | Reaction shots on a plain flat colour with thin speed lines from the edges | bonus |
| 5 | Shading, gradients, texture, or any text, speech bubble or floating symbol in the frame | forbidden |

Prompt wording for the `must` traits is in the frozen style block below (`small round animals about two heads tall … one thick uniform black outline … flat pastel color fills only`, `two small black dot eyes … snap into two large empty white circles`, `red plastic stools`, `small low green tea table`).

## Nearest neighbour

`youtube-storytime` (gated style in this project): also flat 2D with big round heads, one thick even outline, flat fills, a right-wrist marker and hold-and-snap motion. Two visible differences: its cast are people with large white oval eyes, black pupils, floating eyebrows and a D-shaped mouth, here they are whole animals (ears, bills, snouts, tails) with tiny black dot eyes that snap to empty white circles; its sets are American rooms with a narrator cutaway whose mouth moves with the VO, here a Vietnamese alley with red plastic stools and a low tea table, and no mouth ever moves with the VO.

## Visual identity

- Characters: small round animals about two heads tall; a big round head, a soft bean-shaped body, short noodle arms and legs of even width, round mitten hands, bare legs or simple everyday Vietnamese clothes (white undershirt, áo bà ba, school shirt with red scarf).
- Line and color: one thick uniform black outline around every shape; flat pastel fills; no shading, gradients, texture or lighting.
- Faces: two tiny black dot eyes and a small mouth. Reactions are snaps, not morphs: dots → two big empty white circles (the "brain stopped" face), dots → white circles with a pinpoint pupil (shock). Blush, a single sweat drop and tear streams are drawn on the face; nothing floats in the air.
- Backgrounds: a flat pastel Vietnamese alley (cream wall, rolled-up shutter, hanging bulb, small low green tea table, red plastic stools) or a pond bank. Reaction shots use a plain flat color with thin speed lines from the edges.
- Motion: hold, snap, hold. Small idle trembles are fine; long smooth moves are not the look.

## Expression vocabulary

13 faces drawn in `gallery/expressions.png`: neutral, happy, laugh, deadpan, blank (empty white eyes), shocked, angry, sad, crying, cringe, smug, confused, panic. Prompts name only the ones the joke needs and describe them physically (`his dot eyes snap into two big empty white circles`), never by mood word alone.

## Cast grammar

Every character shares the drawing grammar above and differs first by species silhouette (head shape, ears, bill, snout, horns), then height, then clothing color. **Every character wears a red rubber band on the right wrist only** (a common Vietnamese everyday object), so left and right can be read in any shot. Each character has a frozen anchor repeated verbatim in every clip it appears in, and every clip says `Characters (exactly N, no one else)`.

Sample cast "Xóm Ao" (anchors in `src/rig.py`, `CAST[..]["anchor"]`):

- **Cóc**: a small round green toad: a wide flat head almost as wide as his body, two tiny black dot eyes set far apart, a very wide thin mouth, a pale yellow-green belly, a loose white sleeveless undershirt, bare green legs with wide flat feet, and a red rubber band on the right wrist.
- **Mèo Mướp**: a grey tabby cat: a round head with two pointed ears, three dark stripes on the forehead, tiny black dot eyes, a small pink nose and short whiskers, a teal short-sleeved T-shirt, bare grey legs, a long striped tail, and a red rubber band on the right wrist.
- **Cô Vịt**: a white duck who runs the iced-tea stall: a round white head with a wide flat orange bill, tiny black dot eyes, a small curl of feathers on top, a purple long-sleeved áo bà ba blouse with two front pockets, loose black trousers, orange webbed feet, and a red rubber band on the right wrist.
- **Heo Mập**: a chubby pink pig: a round pink head with two floppy ears, a big pale pink snout with two nostrils, tiny black dot eyes, a red sleeveless top, blue shorts, a little curly tail, and a red rubber band on the right wrist.
- **Bác Trâu**: an old grey-blue water buffalo: a broad head with two cream crescent horns curving up, a pale grey muzzle with two nostrils, sleepy tiny black dot eyes, a brown long-sleeved áo bà ba with a black-and-white checked scarf around the neck, black trousers, dark hooves, and a red rubber band on the right wrist.
- **Bé Chuột**: a tiny grey-brown mouse schoolkid about half Cóc's height: two big round ears with pink insides, tiny black dot eyes, a pink nose, a white short-sleeved school shirt with a red triangle scarf tied at the neck, navy shorts, a long thin tail, and a red rubber band on the right wrist.

## Shared prompt blocks

Style and environment (verbatim every clip):

```text
Style and environment: a flat 2D cartoon in the look of a Vietnamese social-media comic strip brought to motion, original animal characters only. Characters are small round animals about two heads tall: big round heads, soft bean-shaped bodies, short noodle arms and legs of even width, round mitten hands, and one thick uniform black outline around every shape. Flat pastel color fills only: no shading, no gradients, no texture, no lighting effects. Faces are tiny and calm: two small black dot eyes and a small mouth. For a big reaction the dot eyes snap into two large empty white circles, or white circles with a pinpoint pupil, and later snap back; small comic marks drawn on the face (a sweat drop, pink blush) are allowed. Backgrounds are a simple Vietnamese alley in flat pastel shapes: a warm cream wall, a shopfront with a rolled-up shutter and a hanging bulb, a small low green tea table, red plastic stools. Reaction shots use a plain flat pastel color with thin speed lines from the edges. Comic-strip timing: a character holds a pose, then snaps quickly into the next; each punchline lands after a held, silent beat of about one second.
```

After the character anchors:

```text
Every character has exactly two arms and two legs, each arm ending in one round hand; a moving limb replaces its previous pose. Limbs keep their length and bend smoothly at elbows and knees. Every character wears a red rubber band on the right wrist only. Characters stand at least an arm's length apart; heads, bills and snouts never touch or overlap.
```

Voice (first-person deadpan narrator; adapt identity fields per video, keep the last two sentences):

```text
Voice: One off-screen young adult male narrator throughout, telling his own story in the first person. Light Northern Vietnamese accent speaking clear English, soft light tenor, medium pitch, slightly nasal forward resonance, clean texture with no raspiness or breathiness. Sincere, completely deadpan delivery, as if every sentence were perfectly reasonable; flat pitch with small pauses before the last words of a joke. Steady unhurried pace, close and dry studio sound. Keep the same vocal timbre, register, accent, pace and recording quality throughout. Emotional progression belongs to the visuals and music; do not change the narrator's voice or switch to character dialogue. No character's mouth moves with the words.
```

```text
Dialogue: audio voiceover only, strictly no speech bubbles, no dialogue boxes. Speak exactly the quoted lines once, in order; do not add, omit, paraphrase, repeat, caption, subtitle or display any words.
```

Negatives (with the posture negatives from `posture-gate.md`):

```text
Negative constraints: no 3D render, no CGI, no anime or manga style, no realistic animals or realistic anatomy, no shading or gradients, no paper texture, no resemblance to any existing comic or webcomic character, no hats, no extra arms, legs or fingers, no duplicate characters, no extra animals in the background, no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no prop switching hands without a visible pass, no heads, bills or snouts overlapping, no visible text, letters, numbers or signboards, no logos, no speech bubbles, no dialogue boxes, no emoji or symbols floating in the air, no watermark.
```

## Core rules this style overrides

- **Idle and reaction beats:** the core asks for a visible change every two to three seconds. Here one beat per clip is about one second of silence with a frozen face (the gutter before the last panel), and the punchline pose is held for at least a second. Reason: the comic's timing is the joke; the frozen face is the visual change.
- **Narrator:** the voice is first person and deadpan (the lead tells his own story) and never explains the joke. No character's mouth moves with the VO.
- **Music:** the score drops out for the silent hold in every clip and comes back after it.

## Text policy

`post-overlay`. Nothing is written in the frame; speech-bubble lines become VO. A caption, if any, is added in post-production (the sample package needs none: the joke reads muted).

## Motion cadence

`stepped`: hold a pose, snap to the next, hold. Small idle trembles are allowed; long smooth moves and face morphs are not.

## Camera moves allowed

Transition moves: hold (the default, and always during a demanding body action such as lifting the stool), hard cut to a chest-up reaction shot on a flat colour, slow pull back. Accent move: fast push-in on a face, at most one per clip and in at most one third of the clips (the sample uses it once, clip 2). No shake, orbit or whip pan: they fight the still-panel look.

## Post-production

1. Trim each clip to its last held frame; do not cut into the one-second silent hold or the punchline hold.
2. Join on hard cuts; no transitions or zooms added in the edit.
3. Captions or a title only as overlays after generation, outside the faces and hands.
4. Conform audio: one music level across clips, the silent beats left silent.

## Music (frozen)

```text
a light plucky đàn bầu-and-ukulele loop at a slow walking tempo
```

Clip 1's Audio line uses these words verbatim and adds that the music drops out for the silent beat.

Clips 2–N say: `the score seamlessly continues the identical light plucky đàn bầu-and-ukulele loop from clip 1, same tempo and instrumentation`, then the clip's own sound cues.

## Strip-to-motion timing

One 10-second clip carries one strip (see `gallery/strip-to-motion.png`):

| Time | Comic | Clip |
|---|---|---|
| 0–3 s | Panel 1: setup | Wide shot, the situation and the line that will be taken literally (VO) |
| 3–6 s | Panel 2: development | One move or one punch-in; the "thinking" blank-eye snap |
| 6–7.2 s | The gutter before the last panel | About one second of silence: VO stops, music drops, face frozen. Write it in the beat and the Audio line |
| 7.2–10 s | Last panel: punchline | Snap into the punchline pose and hold it for at least one second; one small sound cue (boing, clink) |

- Speech-bubble text cannot be generated. Turn it into VO, or make the gag readable with sound off; list any caption as a post-production overlay.
- The narrator never explains the joke. The last spoken line ends before the punchline pose, or states the absurd logic as if it were normal (`"Exactly as he asked."`).
- A 3-clip story can open with the punchline image as the hook and then cut back (`ten minutes earlier`), with `(time cut)` on the Hands lines.

## Big-head staging rules (from the gallery and motion test)

These came from errors the gate or a visual check caught in the code-drawn rig.

- Hands cannot reach above a two-head-tall character's own head. "Holding something overhead" reads as a broken pose; hold it out in front of the chest with straight arms instead.
- Bills and snouts stick out up to about 1.5 head-radii. Face-to-face characters stand at least an arm's length apart (the prompt's spacing rule) and do not lean in; a pass goes via a table (one sets it down, the other picks it up) or at arm's length.
- A small child next to an adult looks up (head tilt) instead of leaning in.
- A hand at the head (scratching, saluting) sits just outside the head outline at the temple, with the elbow out; a wide low head (toad) also needs a smaller forward arm swing when walking, or the hand crosses the face.
- Sitting on a low plastic stool: thighs level, hands on the knees (clear of the face), feet just off the ground so the stool's legs show below the seat. A deep hip bend hides the stool and drops the big head onto the knees.
- A bow is about 30° with the hips pushed back; 70° throws the big head past the toes.
- The frozen "brain stopped" pose keeps the arms off the body; arms pressed straight down merge into the torso. Long sleeves are one flat tone darker than the garment so the arm never melts into the jacket.
- A sad slump is a small neck bend and dropped shoulders; a big head drops to the chest at a small angle.

## Hands

Follow `posture-gate.md`. Name every held prop with the character's own hand, one character per hand sentence, every put-down and pass gets its own sentence with a verb, one noun per prop (`glass of iced tea`, never also `cup`). The ledger only warns about a gesture made with a hand that is already holding something (a wave with the stool hand); treat that warning as an error. For multi-character tracks, give every animal with a bill or snout a `"snout"` length so `--scene` checks it against other heads.

## Hooks that fit

Reaction before cause (the absurd result first: Cóc guarding a stool, a passer-by's eyes go blank), Before → after cut, and Visual metaphor when the joke is a phrase taken literally (the literal image is the first frame). First spoken line under ten words, the premise only.

## Risks on Omni Flash (untested)

1. The model morphs faces smoothly instead of snapping dot eyes to empty white circles.
2. The one-second silent hold may be filled with motion or music; it is written in both the beat and the Audio line.
3. "Vietnamese comic" may pull toward a famous existing character (a blue bird with a hat, a rabbit). If so, remove the phrase and keep only the physical description.
4. Text on stools, glasses, shop signs; the negatives ban it.
5. Bills and snouts colliding when two characters face each other.
6. The narrator's accent drifting between clips; the voice block is repeated verbatim.

## Sample package

`samples/vn-webcomic.md`, "Save my seat", 3 clips. `package_lint.py` (shared hand ledger, `--anchor` for the style block, Cóc's anchor and the anatomy line): `PASS: 0 red, 0 yellow`; facts block: `samples/vn-webcomic.facts.md`. `tests/verify-opening-hook.py`: passed.

## Catalog row (draft)

| Style Key | Style Name | Visual Theme | Best For | Character Design |
|---|---|---|---|---|
| `vn-webcomic` | Vietnamese Web-Comic in Motion | Flat pastel Vietnamese alley, thick even outline, comic-strip hold-and-snap timing | One-joke relatable gags, literal wordplay, neighbourhood slice-of-life | Original round animals about two heads tall, dot eyes that snap to empty white circles, red rubber band on the right wrist |

Status row: `vn-webcomic | gated | gate-v2 reports, samples/vn-webcomic.facts.md; not tried on Flow`. Setup gate: offer only when the user asks for an experimental style, and say it is `gated`.

## Acceptance checklist

- Every clip repeats the style block, the anchors of everyone present, the anatomy line, the voice block, the dialogue line and the negatives verbatim.
- Each clip has a held silent beat before its punchline and holds the punchline pose for at least a second.
- No mouth moves with the VO; no speech bubbles, captions or text.
- Heads, bills and snouts never overlap; passes go via a table or at arm's length.
- The red rubber band stays on the right wrist; props stay in the hands the ledger names; `hand_ledger.py` passes.
- Nothing is held above a character's head.
- Each beat names its camera move; at most one fast push-in in the whole package.
