# Voxel studio (style pack, slug `voxel-studio`)

> In this repository: the sample package and its lint facts are `samples/voxel-studio.md` and `samples/voxel-studio.facts.md`. Research files named below (renderer, tracks, gate output, frame study) stay in the project's `style-research/voxel-studio/` folder and are not part of the skill.

```text
Status: gated (2026-10-22). Covers: 3 clips of 16:9, 2 to 5 characters on screen, a hand-sized cube passed between
two hands, a cube stack carried in both hands, placing cubes in a gap, a hopping robot with no hands, one white studio set.
Not covered: 9:16, crowds of more than 5, other sets or outdoor scenery, fast action, character dialogue.
```

Evidence: 61 poses of the five humans (13 for Khôi, 12 each for the others) pass `tools/posture_gate/posture_gate.py`
as true 3D tracks and as front and side projections (front tracks carry the drawn torso width, arm thickness, hand
length and head radius); the first draft had 15 FAIL and 27 WARN, now 0 and 0. The motion test (Khôi walks the
platform path carrying a cube and raises it; Mai passes Khôi a cube) passes per character and with `--scene`. The
sample package passes `package_lint.py` with 0 red and 0 yellow, `hand_ledger.py` and `tests/verify-opening-hook.py`,
and the ledger catches 8 of 8 seeded hand errors. Pictures and GIFs are drawn by code from the same rigs; no AI image
or video model was used. Not yet checked against generated video.

## When to use

Tech and how-to explainers, "from one task to a team" stories, productivity and teamwork tips, step-by-step guides
where one small object stands for one idea (a cube for a task, a platform for a step). The clean white set keeps
attention on one action at a time. Not for moody or dramatic stories, outdoor places, realistic people or anything
that needs fingers.

## Signature checklist

### Sources

Frame study, 2026-10-22. The owner's reference picture (a banner image he sent, kept in the research folder because it
carries a third-party logo and text) defines the target: a chibi figure built from small cubes, curly cube hair, black
glasses, a grey hoodie, on round floating platforms with orange tops, on a white background, black, white and grey
with orange accents. I then downloaded official store screenshots (1920×1080) of three voxel games and looked at each
frame at full size; contact sheets are in `research/frames-*.jpg`. Work names stay in this pack and never go into
prompts.

| Work | Frames looked at | Confirms | Contradicts or differs |
|---|---|---|---|
| Owner's reference banner (2026-10-22) | the attached image | T1 to T5 as written: small flat-colour cubes, white studio, orange-topped floating platforms with white stepped undersides, soft studio light, a chibi figure with a big head and bendable arms and legs | It is one still; it shows text and a logo, which the style bans |
| *Voxelgram* (Procedural Level, 2019) | [1](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1158470/ss_bf76d454bf279870469ba669f219fa23b11f5d51.1920x1080.jpg), [2](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1158470/ss_fc6d6d80d803d70f59bbfb2490dfc086a05cc9d2.1920x1080.jpg), [3](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1158470/ss_73ef41b920f69e549b86c202c3fc1d96a4947d0d.1920x1080.jpg) | T1: one model of same-size cubes, each one flat colour, with a thin darker seam between cubes (1, 3). T3: soft even light, a soft shadow under the model, no specular glints (1, 2). T2: a single object floats alone on a plain backdrop (2) | The backdrops are muted colour washes of a blurred room, not white; numbers and puzzle UI sit on the cubes (3) |
| *Voxelgram 2* (Procedural Level, 2025) | [1](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1820620/ead179d18aafc1ad5c7f0f76ab2d1961d4a071cc/ss_ead179d18aafc1ad5c7f0f76ab2d1961d4a071cc.1920x1080.jpg), [2](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1820620/73be9679c3f6d8a29537ebde46dcab5f502895aa/ss_73be9679c3f6d8a29537ebde46dcab5f502895aa.1920x1080.jpg), [3](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1820620/043444b3ec8c35d8f4d6e44f49db7fe77c99b226/ss_043444b3ec8c35d8f4d6e44f49db7fe77c99b226.1920x1080.jpg) | T4: small voxel people read with very few cubes when the head is big and the clothes are flat blocks of colour (1, 2). T1 and T3 again: matte cubes, seams, soft shade under each model (2, 3) | The people are tiny props in a diorama, not leads; the miner (2) is a few dozen cubes, much coarser than our cast |
| *Shooty Skies* (Mighty Games, 2018) | [1](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/702810/ss_e9155fbf0fc2c2e8b28716ac97001212cc60e08c.1920x1080.jpg), [2](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/702810/ss_afa2b5b9cfe71dc16fc9b140fc017c7cf9eed797.1920x1080.jpg), [3](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/702810/ss_80b4494aefea4b61a910fd08c8e234dbc91cf025.1920x1080.jpg) | T1: flat-colour cubes with no pixel texture on characters, clouds and trees (1, 3). T4: chibi voxel characters with big heads and small bodies (2). White stepped cube clouds like our platform undersides (1) | Saturated rainbow palettes, score counters and busy action on every frame: the opposite of T2 and T5 |
| *Pixel Gun 3D: PC Edition* (Cubic Games Studio, 2024), as a contrast | [1](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2524890/e12f224df44fc984aeefb0670b586a32a747a504/ss_e12f224df44fc984aeefb0670b586a32a747a504.1920x1080.jpg), [2](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2524890/ss_cee65de9db9f4f3ffc06fe5aa3976ecf718ebc33.1920x1080.jpg) | Nothing: this is the textured-block branch (`voxel-world`'s), shown to say what to avoid | Pixel textures on every face, outdoor block terrain, HUD and weapons in every frame |

Where the sources run out: none of the games shows a white seamless studio or our orange-topped platforms; those come
from the owner's picture only. I did not find a reachable official gallery of single-colour voxel character renders
on white (the MagicaVoxel site is text and tool pages), so T2 rests on the owner's image and Voxelgram's plain
backdrops.

**What the study changed:** the cube seams. The first renders had a dark grid line round every cube, which read as
graph paper; Voxelgram's seams are a hair darker than the face, so the renderer's seam went from 86% to 90% of the face
colour and the prompt asks for "softly rounded edges" instead of outlines.

### Five signature traits

1. `must` Everything is built from many small matte cubes of one size, each cube one flat colour, with soft seams
   between cubes; no texture on any face (all sources).
2. `must` A bright white seamless studio with no horizon; characters stand on floating round platforms with a flat
   orange top over a white stepped underside of cubes; a few out-of-focus floating cubes at the frame edges (owner's
   picture; Voxelgram's plain backdrops).
3. `must` Soft even studio light from the upper left, gentle shading where cubes meet, soft round contact shadows,
   no glossy highlights (Voxelgram 1, 2).
4. `must` Chibi figures about two and a half heads tall: a big rounded cube head, a small blocky body, short blocky
   limbs that bend at elbow and knee; faces are cubes on the front of the head (owner's picture, Shooty Skies 2).
5. `forbidden` Any colour beyond black, white, greys, skin and orange accents (navy jeans are the one darker neutral),
   any text, logo, UI or screen with writing, any pixel texture, studs or glossy plastic.

### Nearest neighbour

`voxel-world` (gated). Visible differences: (1) voxel-world puts 16×16 pixel textures on big unit blocks in a sunlit
village, voxel-studio uses many small flat-colour cubes on a white studio set; (2) voxel-world's box limbs swing
straight from shoulder and hip, voxel-studio's chibi figures bend at elbows and knees. The next closest is
`brick-build`: glossy plastic bricks with studs and stop-motion on twos, against matte cubes with smooth motion here.
Style 2A shares the white tech studio and a glasses-wearing lead, but its people are stick figures with no cubes.

## Visual identity and frozen style block

The set is one white studio: a seamless white backdrop fading to the palest grey at the floor, round floating
platforms (orange top, white stepped underside), a few blurred white, grey and orange cubes near the frame edges. The
palette is black, white and soft greys, navy for jeans, one warm light skin tone, and orange for accents only:
platform tops, the task cubes, the right-wrist bands, Mai's hair clip, Su's backpack and Bit's ear light.

The frozen block, repeated verbatim in every clip (`STYLE` in `src/make_package.py`):

```text
Style and environment: a clean, minimal 3D voxel studio. Every character and object is built from many small matte
cubes of one size, each cube one flat colour with softly rounded edges, so hair, faces, clothes and props read as tidy
little cube steps. A bright white seamless studio backdrop with no horizon line and a few small white and light grey
cubes floating out of focus near the edges of the frame. The characters stand on floating round voxel platforms: a
flat orange top layer over a white stepped underside of cubes. A limited palette of black, white and soft greys with
orange accents only; skin is the one warm neutral. Soft even studio light from the upper left, gentle shading where
cubes meet, soft round contact shadows on the platforms, no glossy highlights and no textures on the cube faces. The
background alone is softly out of focus. A clean high-key 3D render look with a steady camera; not photoreal, not
claymation, not pixel-textured game blocks, not smooth CGI.
```

The body rule (`BODY`) follows the anchors in every clip:

```text
Every human is a chibi figure about two and a half heads tall: a big rounded cube head, a small blocky body and short
blocky arms and legs. Arms bend only at the shoulder and the elbow, legs only at the hip and the knee, always the
natural way; hands are small plain cubes with no fingers, and a held cube sits in one named hand. Bodies and limbs
keep their size and never stretch or pass through each other. Faces are made of cubes on the front of the head:
expressions change only those face cubes, never the head shape. Every human wears one orange band round the right
wrist; never on the left.
```

## Originality (hard rule, the videos are published)

- Prompts name no game, studio, brand or app. Describe the look: "a clean, minimal 3D voxel studio".
- The owner's picture carries a product logo, a product name and title text; none of it is copied. The round black
  helper is redrawn as Bit (white eyes, grey ear pods, an orange light), with no fuse and no logo.
- The cast is original. Khôi follows the owner's picture in genre (curly hair, black glasses, grey hoodie), as asked,
  and carries no real person's name in prompts.

## Character anchors and cast cards

The anchor is `LOOK` in `src/cast.py`, pasted in full into every clip by `src/make_package.py` and printed on every
model sheet.

| Character | Anchor (verbatim) | Movement line |
|---|---|---|
| Khôi | Khôi, a chibi voxel young man built from small cubes: a big rounded cube head with light skin, fluffy curly black hair made of little cubes, thick black square glasses, a grey zip hoodie worn open over a white T-shirt with white drawstrings, navy jeans, chunky white sneakers with grey soles and an orange band on the right wrist. | — |
| Mai | Mai, a chibi voxel young woman built from small cubes: a big rounded cube head with light skin, a straight black bob with a blunt fringe and a small orange hair clip on her right side, a loose white sweater with grey ribbed cuffs and hem, charcoal wide trousers, black shoes and an orange band on the right wrist. | — |
| Hà | Hà, a chibi voxel young woman built from small cubes: a big rounded cube head with light skin, black hair pulled into a high ponytail, a black bomber jacket worn open over a white T-shirt with dark grey ribbed cuffs and collar, light grey jeans, white sneakers with black soles and an orange band on the right wrist. | — |
| Bác Tùng | Bác Tùng, a chibi voxel older man built from small cubes: a big rounded cube head with light skin, a bald top with short grey hair round the sides and back, bushy grey eyebrows and a grey moustache, a charcoal cardigan with dark buttons over a white collared shirt, light grey trousers, black shoes and an orange band on the right wrist. | moves a little slower; waves from the elbow |
| Su | Su, a small chibi voxel boy built from small cubes: an extra big rounded cube head with light skin, spiky black hair, a white T-shirt with short sleeves, an orange backpack with orange straps, grey shorts, white socks, black shoes and an orange band on the right wrist. | — |
| Bit | Bit, a small round helper robot built from small black cubes: a ball of matte black cubes with two tall white rectangle eyes, a grey ear pod on each side with a small orange light on its right pod, no arms, no hands and no legs; it floats a hand's width above the ground and moves by hopping. | floats and hops; never holds anything |

Non-colour differences: hair shape (curly mop, blunt bob, high ponytail, bald top with grey sides, spikes), glasses
and moustache, scale (adult, small child with an extra big head, a ball robot), and outline (open hoodie, sweater,
bomber, cardigan, backpack). The **orange band on the right wrist** is the left/right marker; Bit's marker is the
orange light on its right ear pod.

Faces: 9 cube expressions per human (`gallery/sheet-*.png`: neutral, happy, laugh, talk, surprised, sad, think,
calm, wink) and 4 for Bit. Glasses stay on Khôi in every shot; his brows sit above the frame.

## Core rules this style overrides

| Core rule | Override | Reason |
|---|---|---|
| C6 posture budget | Hand-offs, cube placements and raised arms happen only on a held camera; one of them per character per beat | Small cube hands only read as holding when the frame is still |
| C12 cast | Bit is the only non-human; it never holds anything and has no hands lines | No hands, so no grip to keep honest |
| C14 narrative arc | A three-clip sample may run setup → escalation → payoff and end on a closing question | Three clips are too short for the five-stage engine |
| C16 camera grammar | No orbit, whip pan or shake at all; the one accent per clip is a fast push-in on a reveal | Cube seams and the white backdrop shimmer under fast parallax |
| Music (C3 stays) | One score, soft plucked kalimba and light marimba over a gentle synth pad, set in clip 1 and continued unchanged | Calm studio mood; the score is frozen like the voice |
| Location changes | One white studio per package; a new place is a different stretch of the same platform path, by hard cut | The set is the style; a second world breaks it |

## Articulation and posture limits

The shared gate's human limits apply (the rig has real elbows and knees). Rules the gate and the review added:

| Move | Rule | Why |
|---|---|---|
| Raised arm (wave, cheer, holding a cube up) | Lift the arm out to the side, upper arm straight up in side view, the elbow folding back toward the head, never forward | A forward fold of a raised arm is an elbow bent backward; leaning the raised arm forward crosses the face in side view |
| Hand to the face (glasses push, chin) | The hand comes up from the side with the elbow low and on its own side (glasses: elbow out at shoulder height) | The arm must not lie across the face (`examples/face_cover_arm_across.json`) |
| Hand-off | Face to face about three heads apart, both near-camera hands (giver's right to taker's left, or the reverse), the cube between the two palms for a beat | Big heads touch if the two stand closer; short arms cannot reach farther |
| Sitting | Thighs slightly down from level, knees together, on a white studio block | A level thigh pointed at the camera reads as a sideways knee in front view |
| Bow | Hips back a little, head down at most 10° past the lean | The big head hides the face and tips the balance |

Gate setup: 3D tracks run with `--profile rig`, `mass {"head": 0.32}`, `head_radius` = half the head width, and heel
points so the balance check sees the whole shoe. Front tracks add `body_width`, `limb_width` 3 and `hand_length` 3.
Multi-character shots run with `--scene`. Bit has no skeleton and is not gated.

Style bans, which go in the negatives of every clip together with the five shared posture negatives: no pixel
textures on the cube faces, no shiny plastic, no round studs, no outdoor scenery, no strong colours other than orange,
no fingers, no stretched limbs, no hand or held cube covering a face, no cubes growing or shrinking.

## Text policy

`none`. No letters, numbers, screens with writing, logos or UI in frame. Captions, if wanted, go in post.

## Motion cadence

`smooth`. The figures move like a clean 3D animation; do not ask for stop-motion.

## Camera moves

Following the camera grammar in `storyboard-template.md`:

- **Transition moves:** hold, slow push-in, slow pull back, slow lateral track along the platform path, hard cut.
- **Accent moves:** at most one per clip, a fast push-in on a reveal. No orbit, whip pan or shake.
- **Demanding body actions:** hold the camera during a hand-off, a placement or a raised arm.
- **Variety:** after a push-in, the next move is a hold, a pull back or a lateral track.

## Staging and motion

- **Walking:** along the platform path, screen left to right; facing right shows the right side and the orange band.
- **Carrying:** a hand-sized cube in one named hand at the hip; a stack in both hands, one under and one beside it.
- **Placing a cube:** it clicks into place at the same size; never write that it grows into a bigger block.
- **Bit:** hops in small arcs and floats; it reacts with its eyes and by tilting its round body.

## Post-production

1. Trim each clip to the beat boundaries; cut on the click if a placed cube changes size.
2. Stitch with hard cuts; no dissolves.
3. Check every frame at full size for text, logos, a pixel-textured or glossy look and a band on the left wrist.
4. Captions only as platform captions or post overlays, matching the VO exactly.

## Hooks that fit

From the Golden Hook section of `references/storyboard-template.md`:

- Physics break: a cube tips off a carried stack (used in the sample).
- Satisfying motion: cubes click into a bridge one by one.
- Before → after cut: an empty platform, then the finished build.
- Scale shock: one orange cube as big as a platform.

Keep the hit sound soft (a pop, a click), never a blast.

## Sample package and facts block

The sample is `samples/voxel-studio.md`, "Pass it on", 3 clips, generated by `src/make_package.py`: Khôi drops a task
cube, hands cubes to Mai and Hà, and the three build a bridge for Bit. It carries a global continuity block, the 3
prompts, a stitching guide and a voice and music continuity note. Its facts block is
`samples/voxel-studio.facts.md`. Mutation tests are in `prompt-package/ledger-tests.md` (8 of 8 caught).

A hand-ledger gap found on the way: a beat where a prop is the subject of a release verb ("the top cube slides off the
cube stack, drops onto the platform") is read as the character letting go of the whole stack, so a missing put-down
beat later passes. The sample avoids it ("tips off ... falls to the platform").

## Acceptance checklist

- [ ] No prompt names a game, studio, brand or app; no text, logo or UI in frame.
- [ ] Every clip carries STYLE, BODY and the full anchor of each character on screen.
- [ ] Cubes stay matte, flat-coloured and the same size; no pixel textures, studs or gloss.
- [ ] The backdrop stays white and the palette stays black, white, grey and orange.
- [ ] The orange band stays on the right wrist every time a character turns.
- [ ] Each cube sits in one named hand; passes are on the camera side; the package passes `package_lint.py`.
- [ ] No arm or cube covers a face; raised arms go out to the side.
- [ ] Bit never holds anything.
- [ ] Every frame has been watched by eye; the gates pass postures that still look wrong.

## Generation risks

- **Texture pull.** "Voxel" can pull in pixel-textured game blocks; the style block and negatives say no textures.
- **Seam outlines.** The model may draw a black outline round every cube; cut or regenerate.
- **Colour creep.** Extra saturated colours from the genre's games may appear.
- **Cube growth.** A placed cube may grow; cut on the click.
- **Glasses drift.** Khôi's glasses may thin out or vanish when he turns; check side views.

## Catalog row

| Style Key | Style Name | Visual Theme | Best For | Character Design |
|---|---|---|---|---|
| `voxel-studio` | Voxel Studio | Chibi figures of small flat-colour cubes on orange-topped floating platforms in a white studio, black, white and grey with orange accents | Tech and how-to explainers, teamwork and productivity tips, step-by-step guides | Big rounded cube heads, cube faces, elbows and knees that bend; orange band on the right wrist; a black cube-ball robot helper |
