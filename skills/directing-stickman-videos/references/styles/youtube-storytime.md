# Storytime Animation (style pack, slug `youtube-storytime`)

> In this repository: the sample package and its lint facts are `samples/youtube-storytime.md` and `samples/youtube-storytime.facts.md`. Other research files named below (gallery, tracks, gate output, renderer) stay in the project's `style-research/youtube-storytime/` folder and are not part of the skill.

```text
Status: gated (2026-10-20). Covers: 3 clips, 4 characters (Mo, Rosa, Dex, Bea), coffee handoff, high five, 16:9.
Not covered: Ms. Hargrove and Grandpa Walt in a package, 9:16, crowds, outdoor scenes. Not tried on Flow.
```

Evidence for `gated`: 72 pose tracks pass the posture gate with 0 errors and 0 warnings (`gallery/gate-output-v2.txt`), the 4-character motion test passes `posture_gate.py --scene` (`motion-test/gate-v2.txt`), and the sample package passes `hand_ledger.py`, `package_lint.py` (facts block: [`samples/youtube-storytime.facts.md`](samples/youtube-storytime.facts.md)) and `tests/verify-opening-hook.py`. Every claim below about how the model behaves is a prompt design choice, not an observed result. Research notes, sources, gallery and gate results are in `README.md` next to this file. The slug names the genre for the catalog only; no prompt contains the word "YouTube".

Catalog lines (to add when the pack moves into `references/`):

| Catalog | Line |
|---|---|
| Style matrix | `youtube-storytime`: flat 2D first-person storytime cartoon, big round heads, even medium-weight outline, flat fills, narrator avatar with radial-stripe cutaways; text post-overlay; motion stepped |
| Status | `youtube-storytime`: gated (2026-10-20), not tried on Flow |
| Setup gate | Offer only when the user asks for an experimental style; say it is `gated`, not `flow-tested` |

## What the format is

The US "storytime" animation genre: a narrator tells a true, usually funny story about their own life, and appears in it as a simple cartoon avatar. The look is close to an animatic: big round heads, small bodies, thin limbs, flat colors, one even outline, little motion. The comedy comes from the gap between what the narrator says and what the next cut shows, from held reaction faces, and from quick cutaways to the narrator talking to the viewer.

Use it for first-person stories, embarrassing or relatable moments, family and roommate comedy, "the time I…" videos. It fits this skill's narrator-led structure directly: the narrator is the VO and also a character.

## Signature checklist

Sources: a frame study of five official uploads from four channels (2026-10-20). For each video I looked at the official thumbnail and the three frames YouTube extracts from the video itself (`hq1`, `hq2`, `hq3`, at about a quarter, half and three quarters of the running time). That is four images per work, 20 in all, not a viewing of the videos. Contact sheet: [`sources/frame-study.jpg`](sources/frame-study.jpg); the single images are in `sources/` as `<video id>_<image>.jpg`. Work and channel names stay in this pack and never go into a prompt.

| Work (official upload) | Images looked at | Confirms | Contradicts |
|---|---|---|---|
| TheOdd1sOut, "Work Stories (sooubway)" | [thumbnail](https://i.ytimg.com/vi/cV542dRK3uk/maxresdefault.jpg), [hq1](https://i.ytimg.com/vi/cV542dRK3uk/hq1.jpg), [hq2](https://i.ytimg.com/vi/cV542dRK3uk/hq2.jpg), [hq3](https://i.ytimg.com/vi/cV542dRK3uk/hq3.jpg) | T2: huge round heads, bean bodies, mitten hands; T3: the narrator talks to camera on plain white (hq1, hq2); D-shaped open mouths, no nose | T1: the outline is medium weight, not thick; T4: the white characters carry one flat light-blue shadow tone; T5: a "09-09" plate and a picture-in-picture photo are on screen |
| TheOdd1sOut, "Sooubway 4: The Final Sandwich" | [thumbnail](https://i.ytimg.com/vi/5rB7zgPlC5M/maxresdefault.jpg), [hq1](https://i.ytimg.com/vi/5rB7zgPlC5M/hq1.jpg), [hq2](https://i.ytimg.com/vi/5rB7zgPlC5M/hq2.jpg), [hq3](https://i.ytimg.com/vi/5rB7zgPlC5M/hq3.jpg) | T2 again (two characters in a shop, hq2); T3: soft radial stripes behind the thumbnail figure; flat-colour rooms with a few outlined objects (hq2, hq3) | T5: a Chinese character on the aprons and a live-action clip with text (hq1) |
| JaidenAnimations, "My Childhood Stories" | [thumbnail](https://i.ytimg.com/vi/0R7MQwmbiQc/maxresdefault.jpg), [hq1](https://i.ytimg.com/vi/0R7MQwmbiQc/hq1.jpg), [hq2](https://i.ytimg.com/vi/0R7MQwmbiQc/hq2.jpg), [hq3](https://i.ytimg.com/vi/0R7MQwmbiQc/hq3.jpg) | T3: a pink radial vignette behind a reaction (hq3); big white eyes with dot pupils; snapped, held reaction poses | T1: sketchy, uneven line and partly uncoloured frames (hq2); T2: heads are big but not a third of the height, and hands have fingers; T4: a soft gradient vignette (hq3); T5: hand-lettered labels ("BAD FLOWER!", "shelf", hq1) |
| Alex Clark, "My Dad's Proudest Moment" | [thumbnail](https://i.ytimg.com/vi/CvllW-HQ0P8/maxresdefault.jpg), [hq1](https://i.ytimg.com/vi/CvllW-HQ0P8/hq1.jpg), [hq2](https://i.ytimg.com/vi/CvllW-HQ0P8/hq2.jpg), [hq3](https://i.ytimg.com/vi/CvllW-HQ0P8/hq3.jpg) | T1: clean, even dark outline and flat fills; T2: a very big round head on a small body (hq1); simple dot-eye faces | T4: one flat shadow tone on objects and a textured background (hq1, hq2); T5: an "ARTSKOOL" sign (hq3) |
| Domics, "Ex Best Friend" | [thumbnail](https://i.ytimg.com/vi/2XCQOZc262M/maxresdefault.jpg), [hq1](https://i.ytimg.com/vi/2XCQOZc262M/hq1.jpg), [hq2](https://i.ytimg.com/vi/2XCQOZc262M/hq2.jpg), [hq3](https://i.ytimg.com/vi/2XCQOZc262M/hq3.jpg) | T2: heads about a third of the height (hq1); T3: characters on plain white; white eyes with black pupils | T1 and T4 differ in another direction: black line art with no colour fill at all; noses and fingers are drawn |

What the frames changed: the outline is medium weight, not thick, in every work that has clean lines, so the trait and the style block now say `one clean black outline of even, medium weight` (it said "uniform thick"). Plain white is the most common narrator background (three of five works); radial stripes and vignettes appear for big reactions, so the block now says `a plain white or flat-color background with soft radial stripes for reaction shots`. Mitten hands and no nose hold in the TheOdd1sOut frames but not in all five works; they stay as this pack's design choice. Flat fills with no shadow tone is stricter than the genre (two works add one flat shadow tone) and is kept to keep the model away from rendered shading. On-screen text is a real signature of the genre (four of five works), so it is a `bonus` added in post, not part of generation. Where the sources run out: these are 20 still images; motion, cutting rhythm and timing claims still rest on the genre article and the editing guides in `README.md`, not on watching the videos.

| Trait | Tag | Prompt words (verbatim in every clip) |
|---|---|---|
| One clean black outline of even, medium weight and flat fills, no shadow tone (T1) | `must` | `one clean black outline of even, medium weight around every shape. Flat color fills only: no shading, no gradients, no texture, no lighting effects` |
| Big round head about a third of the height, bean body, noodle limbs, mitten hands (T2) | `must` | `big round heads about a third of their height, small bean-shaped bodies, thin noodle arms and legs of constant width, round mitten hands` |
| Narrator and reactions on plain white or a flat color, soft radial stripes for big reactions (T3) | `bonus` | `a plain white or flat-color background with soft radial stripes for reaction shots` |
| Rendered shading, soft gradients, texture or a 3D look (T4) | `forbidden` | negatives: `no 3D render, no CGI, … no shading or gradients, no paper or canvas texture` |
| Hand-lettered labels and captions (T5) | `bonus`, added in post only | negatives keep generated frames clean: `no visible text, letters, numbers or captions`; every label goes in the edit |

Nearest neighbour: `us-sitcom` (prime-time animated sitcom). Two differences a viewer can see: (1) storytime heads are about a third of the body height with no nose, sitcom characters have near-normal proportions and a nose shape each; (2) storytime rooms are almost empty flat colors with two or three outlined objects, or a radial-stripe card, while sitcom backgrounds are furnished interiors (couch, curtains, pictures).

The cast is original. No character copies a known creator's avatar (no round white "marshmallow" people, no creator's signature hair, outfit or colour combination), and prompts name no channel, creator or character.

## Cast cards (verbatim, repeated in every clip the character appears in)

Every character wears a plain white wristband on the right wrist only, so left and right can be checked in any shot. Copy a card exactly; do not shorten or reword it between clips. Source: `src/rig.py` `CAST[..]["anchor"]`, role tag dropped.

**Mo** (narrator):

```text
Mo: a short young adult with a big round head, medium-brown skin, a fluffy cloud of dark brown curly hair, round black glasses, a teal hoodie with a front pocket and the hood resting behind the neck, blue jeans, white sneakers, and a plain white wristband on the right wrist.
```

**Rosa** (roommate):

```text
Rosa: a young woman with a big round head, light tan skin, a long black high ponytail tied with a red scrunchie, a mustard-yellow sweater, dark grey jeans, black sneakers, and a plain white wristband on the right wrist.
```

**Dex** (big brother):

```text
Dex: a tall broad-shouldered young man with a big round head, pale freckled skin, a short brown buzz cut, a red tank top, black basketball shorts, red sneakers, and a plain white wristband on the right wrist.
```

**Ms. Hargrove** (strict teacher):

```text
Ms. Hargrove: a middle-aged woman with a big round head, dark brown skin, silver-grey hair in a high round bun, red cat-eye glasses, a purple cardigan over a white top, a long navy skirt, black flat shoes, and a plain white wristband on the right wrist.
```

**Bea** (six-year-old sister):

```text
Bea: a small six-year-old girl about half Mo's height with an extra-big round head, peach skin, two round orange pigtail puffs, a green hoodie with a row of small yellow spikes on the hood, lilac leggings, pink sneakers, and a plain white wristband on the right wrist.
```

**Grandpa Walt** (grandfather):

```text
Grandpa Walt: an old man with a big round head, pink skin, a bald top with fluffy white tufts above the ears, a bushy white mustache, a red flannel shirt with brown suspenders, khaki trousers, brown shoes, and a plain white wristband on the right wrist.
```

Every clip lists exactly who is in it: `Characters (exactly N, no one else):` followed by the cards and the anatomy line. A character named in the VO but not on screen is called by role ("my roommate"), never by name, so the model does not draw them.

## Frozen prompt blocks

Style and environment (verbatim every clip, includes the palette):

```text
Style and environment: a flat 2D American first-person storytime cartoon, original characters only. Characters have big round heads about a third of their height, small bean-shaped bodies, thin noodle arms and legs of constant width, round mitten hands, and one clean black outline of even, medium weight around every shape. Flat color fills only: no shading, no gradients, no texture, no lighting effects. Faces are simple: large white oval eyes with small black pupils, thick floating eyebrows, a mouth that opens wide in a D shape for big reactions; no nose. Backgrounds are simple flat-color rooms with a few outlined objects (a window, a blank picture frame, a counter), or a plain white or flat-color background with soft radial stripes for reaction shots. Palette: pale peach and butter-yellow walls, sky-blue and soft-yellow reaction backgrounds, clothing in teal, mustard yellow, tomato red and grass green, white eyes, black outlines; backgrounds are a step paler than the characters. Limited, snappy animation: a character holds a pose, then snaps quickly into the next one; faces change in one quick snap, not a slow morph.
```

Anatomy line (after the cards):

```text
Every character has exactly two arms and two legs, each arm ending in one round hand; a moving limb replaces its previous pose. Limbs keep their length and bend smoothly at elbows and knees. Every character wears a plain white wristband on the right wrist only. During a hand-over two characters stand close, with a small gap of less than half a head-width between their heads and both arms held fully straight out; heads never touch or overlap.
```

Voice (the narrator is a character, so the block names who may move their mouth; adapt identity fields per video, keep the last sentence):

```text
Voice: Mo is the only voice, speaking as the narrator telling his own story. Young adult male, General American accent, light dry baritone, slightly nasal forward resonance, clean texture with no rasp. Casual conversational storytime delivery with deadpan comic timing: quick sentences, a short pause before each punchline, small smile in the voice. Medium-fast pace, close and dry home-studio microphone sound. Keep the same voice, accent, pace and recording quality throughout. In narrator shots only Mo's mouth moves with the words; in story shots no character lip-syncs, mouths only show expressions.
```

Score (frozen; clip 1 states it, later clips continue it):

```text
Clip 1: voiceover clearly audible over a light bouncy ukulele and soft hand-clap loop at a medium tempo
Clips 2+: voiceover seamlessly continues the identical light bouncy ukulele and soft hand-clap loop from clip 1, same tempo and instrumentation
```

Dialogue line:

```text
Dialogue: audio voiceover only, strictly no speech bubbles, no dialogue boxes. Speak exactly the quoted lines once, in order; do not add, omit, paraphrase, repeat, caption, subtitle or display any words.
```

Negatives (style bans plus the posture negatives from `posture-gate.md`):

```text
Negative constraints: no 3D render, no CGI, no anime or manga style, no realistic anatomy, no shading or gradients, no paper or canvas texture, no resemblance to any existing online animator's characters, no extra arms, legs or fingers, no duplicate characters, no extra people in the background, no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no prop switching hands without a visible pass, no heads overlapping, no visible text, letters, numbers or captions, no logos on the phone or cup, no speech bubbles, no dialogue boxes, no emoji or symbols floating in the air, no watermark.
```

## Core rules this style overrides

| Override | Reason |
|---|---|
| The narrator's mouth moves with the VO, but only in narrator cutaways; in story shots no one lip-syncs | The narrator on screen is the genre's signature; limiting lip-sync to one character in one shot type keeps the top Flow risk (lip-sync spreading to everyone) contained |
| Text policy: `post-overlay` | Real storytime videos use labels and captions constantly ("3 hours later"), but generated text is unreliable; every text item goes to post |
| Up to three shots per 10-second clip (story wide, reaction close-up, narrator cutaway) | The genre's comedy lives in the cut to the reaction; one shot per clip would lose it |

## Motion and camera

Motion cadence: `stepped`. A character holds a pose, then snaps into the next one; faces change in one snap, not a morph.

Camera, following the camera grammar in `storyboard-template.md`:

- Transition moves: hold and hard cut. Storytime "punch-ins" are written as a hard cut to a closer shot size, not a zoom.
- Accent: one whip pan or fast push-in for the reveal or the punchline, at most one per clip and in no more than a third of the clips. The `0–2s` hook may use its own whip pan (the sample's clip 1).
- Hold the camera during a hand-over, a high five or any demanding body action; name the move in every beat (`Camera holds through the pass.`).

## Storytime cutting grammar

| Shot | Use | Prompt wording |
|---|---|---|
| Story wide | Show what happened, full bodies, side view for actions | `wide two-shot in the kitchen, side view, Mo at the left facing right` |
| Reaction close-up | The face that sells the joke, held for at least a second | `Hard cut to a close-up of Mo's face; camera holds: his eyes snap wide, pupils shrink to dots` |
| Narrator cutaway | Mo talks to the viewer, chest-up, on a flat color with soft radial stripes; the only shot where a mouth moves with the VO | `Hard cut; camera holds. Narrator cutaway: Mo alone, chest-up on a flat yellow background with soft radial stripes` |
| Contradiction cut | VO claims something; the next beat shows the opposite | VO `"And I believed her."` then `"For about four seconds."` over the reaction |

- One visual change about every 3–4 seconds; never hold a static wide for a whole clip.
- Half a second of silence before a punchline, then the reaction cut and a sound cue (slap, record-scratch, slurp). Write it in the Audio line.
- A mouth action (sip, bite) in a narrator cutaway happens after the spoken line, never during it.

## Style bans and posture limits (from the gallery and motion test)

These came from errors the gate or a visual check caught in the code-drawn rig; they apply to prompts because a video model faces the same geometry.

- Arms are shorter than the head is wide. In a hand-over the heads end up close: write `a small gap of less than half a head-width between their heads and both arms held fully straight out` (the motion test measures about 0.3 head-widths). Never write a larger distance than the arms can reach, and never let them lean in.
- A small child cannot reach past her own face in side view. Turn the child to face the viewer and stretch the arm out to the side for a high five or a grab.
- Raised hands easily cross the big face: waves and cheers keep the hand beside the head, a jump uses a wide V. A drink is held in one named hand beside the mouth, the other arm hanging free; two hands on one small prop fold both arms onto the body.
- Keep a prop hand below the chin in side view (phone, shaker), so the wristband stays readable.
- A big head tips a long way for a small neck angle. Sadness is a small lean plus dropped shoulders; a deep bend drops the head to chest level.
- Before a free hand reaches across, the other hand puts its prop away (`slides the phone into his hoodie pocket`), so two hands never meet over one prop.
- When carrying a prop, the free arm swings less, so it does not pass the prop.

## Hands

Follow `posture-gate.md`. Name every held prop with the character's own hand, write one character per hand sentence, give every put-away and pass its own sentence with a verb, and use one noun per prop everywhere (`iced coffee`, never also `drink` or `cup` in beats or frames). The ledger only checks bookkeeping; staging (distance, who reaches across whom) needs the rules above.

## Hooks that fit

Reaction before cause (a frozen deadpan face, then the cut to what caused it), Sudden entry (a character bursts in from the edge), and Before → after cut. The first spoken line is the story's premise in under ten words (`"I once lost a coffee to a six-year-old."`). Avoid starting with a narrator greeting.

Hook loudness: the hook hit is one short, light sound (a whoosh on the whip pan, a slap on the high five) at about the music's level, never a bass drop or a loud sting; the VO stays the loudest thing. The music may cut to silence for half a second before the first punchline.

## Post-production steps

1. Trim each clip to its beats; cut on the first frame of each reaction close-up.
2. Add every text overlay in the edit (time cards such as "3 hours later", labels, captions), in a plain rounded sans font, white with a black outline.
3. Level the VO above the ukulele loop; check the loop's tempo matches across clips and crossfade it at each clip join.
4. Add or strengthen the sound cues the prompt asked for (whoosh, slap, record-scratch, slurp) if the model's are weak.
5. Check every clip for model-drawn text on phones and cups and for lip-sync outside narrator cutaways; regenerate the clip if either appears.

## Sample package

`samples/youtube-storytime.md` ("The coffee I didn't earn", 3 clips, 16:9): passes `hand_ledger.py` with no warnings, `package_lint.py` with 0 red and 0 yellow (facts: [`samples/youtube-storytime.facts.md`](samples/youtube-storytime.facts.md)) and `verify-opening-hook.py`.

## Risks on Omni Flash (untested)

1. Lip-sync spreading to every character in story shots. The voice block restricts it; check the first clip.
2. Smooth motion and face morphing instead of snapped poses.
3. Three shots inside one 10-second clip may not all land.
4. The model may still drift toward famous creators' avatars; the negatives ban resemblance, and prompts carry no brand word.
5. Model-invented text on phones, cups and signs; the negatives ban it.

## Acceptance checklist

- Every clip repeats the style block, all present characters' cards, the anatomy line, the voice block, the score sentence and the negatives verbatim.
- Only the narrator's mouth moves with the VO, and only in narrator shots.
- Heads never overlap; hand-overs happen with straight arms and a small head gap.
- The white wristband stays on the right wrist; props stay in the hands the ledger names; `hand_ledger.py` passes with no warnings.
- No text, captions, logos or floating symbols on screen; overlays listed separately.
- Each clip has at least one reaction close-up or narrator cutaway, and the joke's sound cue is in the Audio line.
- Every beat names its camera move; at most one accent per clip and in no more than a third of the clips.
