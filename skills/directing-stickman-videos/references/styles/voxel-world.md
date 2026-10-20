# Voxel block world (draft style reference, slug `voxel-world`)

> In this repository: the sample package and its lint facts are `samples/voxel-world.md` and `samples/voxel-world.facts.md`. Other research files named below (gallery, tracks, gate output, renderer) stay in the project's `style-research/voxel-world/` folder and are not part of the skill.

```text
Status: gated (2026-10-20). Covers: 3 clips of 16:9, 2 to 4 characters on screen, a small-block handoff between two
box hands, placing a block in a wall, a walking lantern and a four-legged buffalo, daylight on one village set.
Not covered: 9:16, night or interiors, crowds of more than 4, fast action, character dialogue. Not tried on Flow.
```

Evidence: 86 v2 poses pass `posture_gate.py` (shared PR #4 copy: 3D, front with `body_width`, side, and pixel-snapped
front/side with `--profile pixel`; 0 FAIL, 0 WARN) and `src/voxel_limits.py` (0/86); the 4-character motion test passes
`--scene` and the body-clip check (`motion-test/gate-v2.txt`); the sample package passes `package_lint.py` with the
shared hand ledger (facts block below), `hand_ledger.py` and `tests/verify-opening-hook.py`. Draft pack, not yet in the
skill catalog. Files: `/mnt/project-files/style-research/voxel-world/`; rebuild with `sh src/run_all.sh`.

## When to use

Building, crafting and teamwork stories, cozy village life, cause and effect where one piece is missing (a wall short
one block, a bridge short one plank), explainers where things are assembled piece by piece. Audiences who know block
games read the genre at once. Not for soft bodies, realistic people, fine hand acting or anything needing fingers.

## Signature checklist

### Sources

Frame study, 2026-10-20. I downloaded the official store screenshots (publisher press stills, 1920×1080) of four
block-world works and looked at each frame, with zoomed crops of terrain and characters. Contact sheets are in
`research/frames-*.jpg`. The best-known sandbox game itself has no store page I could reach (its site and Wikipedia
were blocked from this container), so its own spin-off stands in for it. Work names stay in this pack and never go
into prompts.

| Work | Frames looked at | Confirms | Contradicts or differs |
|---|---|---|---|
| *Minecraft Legends* (Mojang Studios, Blackbird Interactive, 2023), the famous game's own spin-off | [1](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1928870/ss_65720eb73a2dd8fc993172cfbfcdc8fe40ec44c2.1920x1080.jpg), [2](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1928870/ss_87b5f26fd65475c2605013fae8f17c5085cbd024.1920x1080.jpg), [3](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1928870/ss_4dba4e59eabcf5c3631e5c28b52ffcae46d3bad8.1920x1080.jpg) | T1: terrain, walls and trees are unit cubes, and the clouds are flat blocks (1, 3). T2: crisp pixel textures on every face, one texel size (zoom of 2). T4: box-limbed characters with pixel faces (1, 2). T5: every frame carries hotbar, hearts and resource counters, and the green-lip-over-brown-earth block appears in 2. This confirms the genre's stills are full of UI and that the signature block must be banned by name. | T3: the lighting is not flat. There are soft cast shadows from blocks and characters, warm bloom, and painterly skies (1, 2). Cut-out grass tufts and flowers cover the cube tops (2). |
| *Cube World* (Picroma, 2019) | [1](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1128000/ss_452f10f60d51b30a736daf98680e45da4fe2f872.1920x1080.jpg), [2](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1128000/ss_98156101d5ea52e62420a3567505d3405db29429.1920x1080.jpg), [3](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1128000/ss_b4ab5328b2ab7b7d09451fee1b273f36bfc9a788.1920x1080.jpg) | T1: everything is cubes, including voxel clouds (2) and stepped terrain (3). T3: top faces are bright, sides darker, with soft shadows. T5: dense UI and text in every frame. | T2: no textures. Each voxel is one flat colour and the voxels are small, so detail comes from voxel count, not 16×16 pixel faces. T4: the characters are chunky voxel figures with floating hands and feet, not box limbs (1). |
| *Teardown* (Tuxedo Labs, 2022) | [1](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1167630/ss_b140eeaf8e489dfa4451411ae23c28a0ecb26729.1920x1080.jpg), [2](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1167630/ss_9a48b92d7144b7f4a27c0b5bc7dac1e687698f5b.1920x1080.jpg), [3](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1167630/ss_9fd3e8de605efc42e29ba98f72432cb78a15d7ac.1920x1080.jpg) | T1: one fine voxel grid for buildings, trees and vehicles. T4: the player figure has box limbs and a block head (1). | T2 and T3: the voxels are tiny and there are no texel faces. The lighting is near-photoreal: smoke, fire, fog and long soft shadows (1, 3). Billboards carry words (2), which reinforces the text ban. |
| *Dragon Quest Builders 2* (Square Enix, Koei Tecmo, 2019) | [1](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1072420/ss_47cc0703debbb8c0ed66b96fea2e164af5c548a7.1920x1080.jpg), [2](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1072420/ss_d52a284f0afb2f56d88051870e8fc75aa31b12de.1920x1080.jpg), [3](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1072420/ss_1007a35a45f4109046398fe4d39bce2a5a7885c7.1920x1080.jpg) | T1: building happens on a unit-block grid (1, 2). T5: a hotbar and HP bar in every frame, and the green-lip-over-brown-earth block in 1 and 3. | T2: the blocks are bevelled, with smooth painted textures, not pixel faces. T3: soft shadows and specular highlights. T4: smooth anime characters with elbows and fingers. This is a different branch of the genre. |
| Nearest-neighbour filtering notes: [Godot forum](https://forum.godotengine.org/t/texturearray2d-texture-filtering/129316), [learn-wgpu](https://git.blob42.xyz/Archives/learn-wgpu/commit/63f790e633dcc25d23586395306a1509729456d4), [Unigine](https://developer.unigine.com/forum/topic/6447-how-to-use-nearest-neighbor-texture-filtering-for-pixel-art) | Text only | Why T2 looks crisp: each screen pixel takes the nearest texel. | Rendering notes, not art direction. |

**What the study changed:**

- **Trait 3 is rewritten.** None of the four works has flat, shadowless lighting. Every one shows soft shadows cast
  by blocks and characters, so "square soft shadow under each character" became "soft short shadows under
  characters and blocks, no glossy highlights" in the frozen block, and the package was regenerated.
- **T2 and T4 are kept as `must`.** They define the textured-cube branch of the genre, the branch the famous game
  and its spin-off show. Cube World, Teardown and Dragon Quest Builders 2 are other branches: untextured voxels,
  micro-voxels and smooth bevelled blocks.
- **No Flow results.** No Veo or Omni Flash voxel test was found, so every Flow risk below is still inferred.

### Five signature traits

1. `must` Everything is built from unit cubes on one grid: ground, walls, plants, water, characters and props
   (seen in all four works).
2. `must` Every face carries a low-resolution 16×16 pixel texture with hard nearest-neighbour edges; the texel grid is
   one size everywhere and stays locked to the faces (the textured-cube branch: *Minecraft Legends* terrain zoom).
3. `must` Simple sunlit block lighting: top faces brightest, sides a step darker, soft corner shading where blocks
   meet, soft short shadows under characters and blocks, no glossy highlights (all four show cast shadows).
4. `must` Characters are rigid boxes with a cube head; straight box limbs swing only at the shoulder and hip, no elbows,
   no knees, no fingers; faces are pixels painted on the front of the head (*Minecraft Legends*, *Teardown*).
5. `forbidden` Any game interface, text or icon (hotbar, crosshair, hearts, inventory, resource counters), the
   signature green-lip-over-brown-earth block, and any existing mob or character design (UI in every studied still;
   the green-lip block in two of the four works).

### Nearest neighbour

`brick-build` (gated, same round). Visible differences: (1) voxel-world is matte cubes with flat 16×16 pixel textures
and block-game lighting, brick-build is glossy molded plastic with round studs, fingerprints and macro-lens depth of
field; (2) voxel-world swings straight box limbs with no joints along them, brick-build figures click at hinged elbows
and knees and move on twos.

## Visual identity and frozen style block

Our world is **Xóm Khối**, a riverside Vietnamese village: mossy green ground blocks on a grey stone embankment,
stone-block walls, bamboo, rice paddies, thatch and clay-tile roofs, red paper lanterns, warm late-afternoon light,
clear blue sky with flat square clouds. Textures and palette are generated in `src/textures.py`; ground blocks are
green on every face (never a green lip over brown earth).

The frozen block, repeated verbatim in every clip (`STYLE` in `src/make_package.py`):

```text
Style and environment: a cozy blocky voxel world where everything is built from cubes: a small riverside village of
mossy green ground blocks on a grey stone embankment, stone-block walls, bamboo, rice paddies, thatch and clay-tile
roofs, in warm late-afternoon light. Every block face carries a low-resolution pixel texture of 16 by 16 square
texels, rendered crisp with hard nearest-neighbour edges, never smoothed, blurred or painterly; the texel grid is the
same size on every block and stays locked to the faces while the camera moves. Simple sunlit block lighting: top
faces brightest, side faces a step darker, soft dark shading in the inside corners where blocks meet, soft short
shadows under characters and blocks, no glossy highlights, a light distance haze. Clear blue sky with a few flat square clouds. A clean real-time 3D
game-render look with a steady camera; not photoreal, not claymation, not smooth CGI.
```

The box rule (`BOXES`) follows it in every clip. It is the only defence against elbows appearing.

## Originality (hard rule, the videos are published)

- Never write "Minecraft" or any game title in a prompt, not even in the negatives. Describe the genre: "a cozy blocky
  voxel world where everything is built from cubes". The negatives say "no existing video-game characters or
  creatures".
- No Steve, Alex, Creeper, Enderman, villager, pig, cow or other existing mob; no Mojang logo, font, UI or texture
  pack; no block or item copied pixel for pixel (the grass block with its green lip over dirt, ore speckles, crafting
  table, TNT, diamond tools, the pickaxe silhouette).
- Proportions are deliberately different: a 10-texel cube head on a 10×11×6 body with 4×11×4 arms (the famous game
  uses an 8-texel head on an 8×12×4 body). Long sleeves are one shade darker than the jacket with a dark seam.
- The cast is Vietnamese village people plus a walking paper lantern and a stone buffalo, which no block game has.

## Character anchors and cast cards

The anchor is the `look` field in `src/cast.py`, pasted in full into every clip by `src/make_package.py` and
printed on every model sheet. Anchors hold design only; how a character moves is a separate line (`MOVES`).

| Character | Anchor (verbatim) | Movement line |
|---|---|---|
| Gạch | Gạch, a blocky young builder: a cube head with warm tan skin and black hair under a white headscarf with red dots, a brick-red work jacket with a darker zip panel and two pockets and sleeves one shade darker, olive trousers, brown boots and a lemon-yellow band on the right wrist. | — |
| Than | Than, a blocky young miner: deep brown skin, black hair, a slate-grey cap with a small glowing lamp at the front, a charcoal jacket with one orange band round the chest, darker charcoal sleeves with orange cuffs, dusk-blue trousers, black boots and a lemon-yellow band on the right wrist. | — |
| Bà Lúa | Bà Lúa, a blocky grandmother farmer: warm tan skin, silver hair with a small bun at the back, a stepped conical straw hat in three tiers, an indigo button-front blouse with darker indigo sleeves, black trousers, brown sandals and a lemon-yellow band on the right wrist. | moves a little slower and smaller, keeps her head up so the hat never hides her face |
| Tí Mầm | Tí Mầm, a small blocky child with a big cube head: light skin, black hair and a small green sprout with two leaves growing from the top of his head, a cream T-shirt with a small green leaf on the chest, short cream sleeves, navy shorts, red sandals and a lemon-yellow band on the right wrist. | — |
| Bấc | Bấc, a walking paper lantern: a cube of red paper with darker red ribs that glows warmly from inside, gold caps on top and bottom, a small gold handle loop on top, a plain paper panel on the front with a painted dark pixel face, two short straight brown wooden legs, no arms and no hands, and a lemon-yellow band round the right leg. | waddles; carries things only on its lid |
| Trâu Đá | Trâu Đá, a big slate-grey block water buffalo: a pale grey square muzzle, cream stepped horns built from small cubes that step out, back and up, four straight legs with dark hooves, a thin tail, no hands, and a lemon-yellow band round the right foreleg. | walks on diagonal leg pairs; carries things only on its back |

Non-colour differences: headgear (scarf, lamp cap, three-tier hat, sprout, lantern handle, stepped horns), scale (adult,
small child with a big head, lantern, buffalo), limb count (four limbs, two legs, four legs). The **right-wrist
lemon band** is the fixed left/right marker; the clip's marker sentence names only the odd cases on screen.

Faces: 10 pixel expressions (`gallery/expressions.png`). Laugh is arched closed eyes and an upturned open mouth on
every character, because a `><` squint reads as anger at this size.

## Core rules this style overrides

| Core rule | Override | Reason |
|---|---|---|
| Expressive cartoon faces | Expressions change only the painted face pixels; the head never squashes or changes shape | A cube head that deforms stops being a block |
| Natural limb bends | No elbows, no knees; limbs swing straight from shoulder or hip (table below) | The box limb is the genre; bent limbs are the most likely model drift |
| Idle and reaction beats | Idle is a small head turn (≤ 20°) and an arm sway ≤ 10°; reactions are a shrug of straight arms, a hop, or a face change | Box arms cannot reach the face, so no facepalms, scratches or hugs |
| Hands and props | A small block or tool sits in one box hand; crates take two straight parallel arms; Bấc and Trâu Đá hold nothing | Square hand ends have no fingers to grip; the hand ledger stays honest |
| Music | One score, a light plucked marimba and soft woodblock melody at a calm walking tempo, set in clip 1 and continued unchanged | Keeps clips stitchable; the score is frozen like the voice |
| Location changes | One village set per package; a new place comes by hard cut, never a dissolve, and keeps the same texel size | A dissolve between block worlds smears the grid |

## Articulation and posture limits

`src/voxel_limits.py` enforces this table on every frame, on top of the shared posture gate. Degrees: pitch is
forward/back, roll is out to the side.

| Rig | Arm pitch | Arm roll | Leg pitch | Leg roll | Head yaw | Head pitch | Body lean |
|---|---|---|---|---|---|---|---|
| Humanoid | −60…180 | −10…100 | −30…90 | −5…30 | ±70 | ±40 | −10…30 |
| Bà Lúa | −60…160 | −10…100 | −25…90 | −5…30 | ±70 | ≤ 15 (hat brim covers face) | ≤ 20 |
| Tí Mầm | as humanoid | | | | | ≤ 22 (big head hides face) | |
| Bấc (lantern) | none | none | ±40 | | | | ±25 |
| Trâu Đá (quadruped) | none | none | ±35 | | ±40 | −30…50 | |

Other checks:

- **Bent limbs:** any bend along a limb.
- **Box clipping:** oriented boxes overlapping, with a 0.6-texel tolerance.
- **Face cover:** an arm, tool or held block in front of the face. This is tested along the face normal and along
  the front and three-quarter camera sight lines, so a tool swung up and forward is caught. Frames are skipped only
  when marked `face_away` (back to camera).
- **Ground:** sinking or floating.
- **Holds:** no-hands characters, one hand per small item, two hands per crate.
- **Gait:** the buffalo must not pace.
- **Scene clip:** characters must not pass through each other.

Shared gate setup: 3D tracks run with `--profile rig`. Front views are projected with `body_width` and side views
face right; both also run pixel-snapped with `--profile pixel`. Multi-character shots run with `--scene`, using
`hand_length 2`.

Style bans, which go in the negatives of every clip together with the five shared posture negatives:

- no rounded or smooth limbs
- no elbows, no knees, no bending along a box limb
- no stretched limbs, no fingers
- no hand or held block covering a face
- no blurry, smeared or swimming textures, no texel grid changing size

## Text policy

`none`. No letters, numbers, signs with words, game UI or icons in frame. Captions, if wanted, go in post (below).

## Motion cadence

`smooth`. Block games interpolate box rotations every frame; do not ask for stop-motion "on twos". The 12 fps
tracks in this folder are a check rate, not the target cadence.

## Camera moves

Following the camera grammar in `storyboard-template.md`:

- **Transition moves:** hold, slow push-in, pull back, lateral track or pan, hard cut.
- **Accent moves:** at most one per clip, and only in the hook or a reveal. Use a fast push-in, never an orbit or
  shake, because fast parallax is where the texel grid swims.
- **Demanding body actions:** hold the camera during a handoff, a reach to place a block, a turn, or a two-arm
  carry. Move before or after the action.
- **Variety:** after a push-in, the next main move is a hold, a pull back or a lateral track. Do not use three
  inward moves in a row. Each beat in the sample names its move.

## Staging and motion

- **Walking:** straight legs swing from the hip, with the opposite straight arm. Bà Lúa uses about 0.7× the
  amplitude.
- **Raising an arm:** swing it out to the side, then up. Tool swings go up and out to the side, then down beside
  the body, so the arm and tool never pass between camera and face.
- **Placing a block:** a held block is hand size. When placed it settles into place as a full-size block; write it
  that way so it reads as placing, not morphing.
- **Handoffs:** do them on the camera side, with both hands on the block for a beat. Each sentence covers one
  character: "Gạch takes the small stone block from Than with her left hand."

## Post-production

1. Trim each clip to the beat boundaries. Cut on the stone click in clip 2 if Flow blurs the block growing to full
   size.
2. Stitch the clips with hard cuts only; no dissolves (see Location changes).
3. Check every frame at full size for UI, text, a familiar green mob or a grass-lip block. Cut or regenerate any such
   frame before publishing.
4. Add captions or titles only as platform captions or post overlays outside the picture, matching the VO exactly.
5. Optional conform: when a clip looks soft, a 2× nearest-neighbour downscale and upscale can re-harden texels. This
   is untested, so check faces after it.

## Hooks that fit

These patterns from `references/opening-hook.md` suit the style:

- Physics break: a block pops out of a wall. This is used in the sample.
- Impossible object: a floating block.
- Before/after: an empty plot becomes a house.
- Countdown: blocks placed one by one, with no numbers on screen.

Keep the hit sound crisp but soft (a stone pop, a clatter), not a blast.

## Sample package and facts block

The sample is `samples/voxel-world.md`, "The last stone", 3 clips. It is generated by `src/make_package.py` and
checked by `src/package.sh`. It carries a global continuity block, the 3 prompts, a stitching guide and a voice and music
continuity note. Its facts block, from `package_lint.py` on PR #4 (`claude/posture-gate-drmgl9` at f99e90a; the newer head
99de4b9 also passes), is `samples/voxel-world.facts.md`:

```text
- package: `package.md` sha256 37dd07abebc77523
- storyboard rows: none · prompts: 3 · hand_ledger: PASS · red: 0 · yellow: 0
```

Mutation tests are in `prompt-package/ledger-tests.md`: 8 of 8 seeded hand errors are caught.

## Acceptance checklist

- [ ] No prompt contains "Minecraft" or another game title; no existing mob, UI, logo or text in frame.
- [ ] Every clip carries STYLE, BOXES, the marker sentence and the full anchor for each character on screen.
- [ ] No elbows or knees in any frame; limbs stay straight boxes of fixed length.
- [ ] The texel grid stays crisp, one size, and locked to faces, with no smearing during camera moves.
- [ ] The right-wrist band stays on the right side every time a character turns.
- [ ] Each held block or tool sits in one named hand, and the package passes `package_lint.py`.
- [ ] No arm, block or hat brim covers a face.
- [ ] Bấc and Trâu Đá never hold anything in a "hand".
- [ ] Every frame has been watched by eye; the gates pass postures that still look wrong.

## Flow risks (inferred, not yet tested)

- **Pixel grid loss.** Expect softening and texel size drift, worst on wide shots and fast moves.
- **IP pull.** Even without the name, the genre may bring a hotbar, a crosshair, a green mob or a grass-lip block.
- **Elbows and knees appear.** The model may "humanise" reaches and handoffs, even with BOXES and "straight arm" in
  every beat.
- **Block growth reads as morphing.** If it does, cut on the click or hold a full-size block.
- **Cube head turning past ±70°.** It may be drawn with the face on the side.

## Draft catalog row

| Style Key | Style Name | Visual Theme | Best For | Character Design |
|---|---|---|---|---|
| `voxel-world` | Voxel Block World | A cube-built Vietnamese river village, crisp 16×16 pixel textures, flat block lighting | Building and teamwork stories, cause and effect, step-by-step assembly | Rigid box characters with cube heads and painted pixel faces; straight limbs swing only at shoulder and hip; right-wrist lemon band |

Status row: `voxel-world | gated | 86 poses + motion test gated, package_lint PASS; not tried on Flow`.
Setup-gate line: "voxel-world (gated, experimental): cozy blocky voxel village, box characters, no Flow test yet".
