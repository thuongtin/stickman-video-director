# Voxel world sample package: “The last stone” (3 clips, 16:9, ~30 s)

Six original blocky characters of one village, Xóm Khối; this story uses Gạch, Bấc, Than, Bà Lúa, Tí Mầm and Trâu Đá. Anchors are the `look` fields of src/cast.py, pasted in full. Hands are named from each character's own side; every character wears the lemon-yellow band on the right wrist (Bấc on its right leg, Trâu Đá on its right foreleg). Bấc and Trâu Đá have no hands and stay out of the hands lines. The score is set once in clip 1 and continues unchanged; each beat names its camera move. The hook follows references/opening-hook.md (pattern: Physics break). The prompts never name any existing game. Not yet tested on Flow.

## Global continuity block

- Ratio and length: 16:9, three clips of about ten seconds (about 30 s).
- Style: `voxel-world` (draft pack `voxel-world.md`, status gated, not tried on Flow). The style paragraph and the box rule after the character anchors are repeated verbatim in every clip.
- Cast: Gạch (clips 1–3), Bấc (clips 1–2), Than (clip 2), Bà Lúa, Tí Mầm and Trâu Đá (clip 3). Each anchor is the `look` text from `src/cast.py`, repeated verbatim in every clip the character appears in; a clip lists exactly who is in it. Movement lines (Bà Lúa, Bấc, Trâu Đá) follow the box rule, apart from the anchors.
- Locks: lemon-yellow band on the right wrist (Bấc right leg, Trâu Đá right foreleg); Gạch's wooden mallet stays in her right hand in all three clips; small blocks and tools sit in one box hand; no elbows, no knees.
- Palette: moss green ground, grey stone, warm tan and brown wood, straw gold, brick red, indigo, red lantern paper, clear sky blue, lemon yellow for the right-side band.
- Narrator: one off-screen adult male narrator, General American, warm clean baritone; the voice block is identical in all three clips.
- Score: a light plucked marimba and soft woodblock melody at a calm walking tempo, set in clip 1 and continued unchanged in clips 2–3; the hook's sound is a stone pop and a short tumbling clatter.
- Continuity: the gap appears in clip 1; the small stone travels Than → Gạch and into the gap in clip 2; clip 3 opens on a named time cut to golden hour at the same finished wall.
- Text: none in the frames (text policy `none`). Captions, if wanted, go in platform captions, never in the picture.

## Clip 1 — One stone short

```text
Output: approximately ten seconds, 16:9, 720p target, 24 FPS, synchronized audio.

Style and environment: a cozy blocky voxel world where everything is built from cubes: a small riverside village of mossy green ground blocks on a grey stone embankment, stone-block walls, bamboo, rice paddies, thatch and clay-tile roofs, in warm late-afternoon light. Every block face carries a low-resolution pixel texture of 16 by 16 square texels, rendered crisp with hard nearest-neighbour edges, never smoothed, blurred or painterly; the texel grid is the same size on every block and stays locked to the faces while the camera moves. Simple sunlit block lighting: top faces brightest, side faces a step darker, soft dark shading in the inside corners where blocks meet, soft short shadows under characters and blocks, no glossy highlights, a light distance haze. Clear blue sky with a few flat square clouds. A clean real-time 3D game-render look with a steady camera; not photoreal, not claymation, not smooth CGI.

Characters (exactly 2, no one else): Gạch, a blocky young builder: a cube head with warm tan skin and black hair under a white headscarf with red dots, a brick-red work jacket with a darker zip panel and two pockets and sleeves one shade darker, olive trousers, brown boots and a lemon-yellow band on the right wrist. Bấc, a walking paper lantern: a cube of red paper with darker red ribs that glows warmly from inside, gold caps on top and bottom, a small gold handle loop on top, a plain paper panel on the front with a painted dark pixel face, two short straight brown wooden legs, no arms and no hands, and a lemon-yellow band round the right leg. Every character is built from rigid rectangular boxes. Limbs turn only where they meet the body, arms at the shoulders and legs at the hips, swinging as straight boxes; there are no elbows and no knees, and nothing bends along a limb. Heads turn at the neck and the upper body may tip forward a little. Walking swings the straight legs, and for characters with arms the opposite straight arm, forward and back. Hands are the plain square ends of the arms, with no fingers, and a small held block or tool sits in one box hand. Boxes never stretch, bend, round off or pass through each other. Faces are flat pixel faces painted on the front: expressions change only those pixels, never the head shape. Bấc waddles on its two legs and carries things only on its lid. Every character wears one lemon-yellow band, one texel tall, round the right wrist (Bấc round its right leg); never on the left.

Props: one wooden mallet: a short square brown handle with a grey stone cube head; a low wall of grey stone blocks two blocks high, with one block missing from the top row.

Composition: 16:9 three-quarter view from the front left at chest height of the characters, full-body framing, the wall across the middle of the frame, Gạch at the left of the gap.

Hands at start — Gạch: right hand holds the wooden mallet; left hand empty.
First frame: Gạch stands at the wall, mid-swing, her straight right arm bringing the wooden mallet down onto the top row; the wall is complete except for the block about to fall.

Timed beats:
- [0–3s] (VO: "One stone falls, and the wall has a hole."): Gạch taps the top row with the wooden mallet in her right hand. At about 1s one stone block pops loose, tumbles off the back of the wall and is gone, leaving a square gap. Gạch freezes, eyes wide, mouth open. Camera: hold.
- [3–7s] (VO: "She stares at the hole, and so does Bấc."): Gạch turns her cube head to stare at the gap, her straight arms hanging at her sides. Bấc waddles in from the right on its two short wooden legs, glowing warmly, and stops beside the wall. Camera: slow push-in on the gap.
- [7–10s] (VO: "And the stone pile is empty."): Gạch shrugs: both straight arms swing a little out from the shoulders and back, and Gạch keeps the wooden mallet in her right hand. Bấc tips its whole lantern body toward the left edge of the frame. Camera: hold.

Dialogue: audio voiceover only, strictly no speech bubbles, no dialogue boxes. Speak exactly the quoted lines once, in order; do not add, omit, paraphrase, repeat, caption, subtitle or display any words.

Voice: One off-screen adult male narrator throughout. General American accent, warm clean baritone, medium-low pitch, gentle chest resonance, no raspiness or breathiness. Calm conversational delivery, restrained pitch variation, steady speaking pace, and close, dry studio sound. Keep the same vocal timbre, register, accent, pace, and recording quality throughout. Emotional progression belongs to the visuals and music; do not change the narrator's voice or switch to character dialogue.

Audio: a light plucked marimba and soft woodblock melody at a calm walking tempo; two crisp hollow stone taps; at 1s a stone pop and a short tumbling clatter, then a beat of near-silence.

Final frame: Gạch stands beside the gap holding the wooden mallet in her right hand, looking left; Bấc stands next to her, tipped toward the left.
Hands at end — Gạch: right hand holds the wooden mallet; left hand empty.

Negative constraints: no text, no letters or numbers anywhere, no signs with words, no game interface, no hotbar, no crosshair, no health or hunger icons, no inventory, no buttons, no logos, no brand marks, no watermark, no speech bubbles, no dialogue boxes, no existing video-game characters or creatures, no rounded or smooth limbs, no elbows, no knees, no bending along a box limb, no stretched limbs, no fingers, no limbs passing through bodies, no wristband on the left wrist, no swapped left and right hands, no prop switching hands without a visible pass, no hand or held block covering a face, no blurry, smeared or swimming textures, no texel grid changing size, no morphing, no duplicate characters, no realistic human bodies, no photoreal people, no 2D cartoon outlines, no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders.
```

## Clip 2 — The last stone

```text
Output: approximately ten seconds, 16:9, 720p target, 24 FPS, synchronized audio.

Style and environment: a cozy blocky voxel world where everything is built from cubes: a small riverside village of mossy green ground blocks on a grey stone embankment, stone-block walls, bamboo, rice paddies, thatch and clay-tile roofs, in warm late-afternoon light. Every block face carries a low-resolution pixel texture of 16 by 16 square texels, rendered crisp with hard nearest-neighbour edges, never smoothed, blurred or painterly; the texel grid is the same size on every block and stays locked to the faces while the camera moves. Simple sunlit block lighting: top faces brightest, side faces a step darker, soft dark shading in the inside corners where blocks meet, soft short shadows under characters and blocks, no glossy highlights, a light distance haze. Clear blue sky with a few flat square clouds. A clean real-time 3D game-render look with a steady camera; not photoreal, not claymation, not smooth CGI.

Characters (exactly 3, no one else): Than, a blocky young miner: deep brown skin, black hair, a slate-grey cap with a small glowing lamp at the front, a charcoal jacket with one orange band round the chest, darker charcoal sleeves with orange cuffs, dusk-blue trousers, black boots and a lemon-yellow band on the right wrist. Gạch, a blocky young builder: a cube head with warm tan skin and black hair under a white headscarf with red dots, a brick-red work jacket with a darker zip panel and two pockets and sleeves one shade darker, olive trousers, brown boots and a lemon-yellow band on the right wrist. Bấc, a walking paper lantern: a cube of red paper with darker red ribs that glows warmly from inside, gold caps on top and bottom, a small gold handle loop on top, a plain paper panel on the front with a painted dark pixel face, two short straight brown wooden legs, no arms and no hands, and a lemon-yellow band round the right leg. Every character is built from rigid rectangular boxes. Limbs turn only where they meet the body, arms at the shoulders and legs at the hips, swinging as straight boxes; there are no elbows and no knees, and nothing bends along a limb. Heads turn at the neck and the upper body may tip forward a little. Walking swings the straight legs, and for characters with arms the opposite straight arm, forward and back. Hands are the plain square ends of the arms, with no fingers, and a small held block or tool sits in one box hand. Boxes never stretch, bend, round off or pass through each other. Faces are flat pixel faces painted on the front: expressions change only those pixels, never the head shape. Bấc waddles on its two legs and carries things only on its lid. Every character wears one lemon-yellow band, one texel tall, round the right wrist (Bấc round its right leg); never on the left.

Props: one small stone block, a plain grey textured cube about as big as a character's hand; one wooden mallet: a short square brown handle with a grey stone cube head; a low wall of grey stone blocks two blocks high, with one block missing from the top row.

Composition: 16:9 three-quarter view from the front left, full-body framing; Than enters from the left edge facing right, Gạch faces him at the left of the gap, both of their hands for the pass on the side nearest the camera; Bấc at the right.

Hands at start (time cut) — Than: right hand holds the small stone block; left hand empty. Gạch: right hand holds the wooden mallet; left hand empty.
First frame: Than walks in from the left edge, mid-stride, straight legs and straight arms swinging, carrying the small stone block in his right hand; Gạch stands at the wall facing him.

Timed beats:
- [0–3s] (VO: "Than brings the last stone in the village."): Than walks toward Gạch, his straight legs swinging from the hips and his left arm swinging, his right arm held a little forward with the small stone block. Camera: slow lateral track with Than.
- [3–7s] (VO: "He holds it out, and she takes it."): Than stops facing Gạch and raises his straight right arm forward, holding out the small stone block. Gạch takes the small stone block from Than with her left hand. Than lowers his empty right hand and steps back. Camera: hold.
- [7–10s] (VO: "One straight arm, and the gap is filled."): Gạch turns to the wall and raises her straight left arm forward to the gap. Gạch places the small stone block in the gap and lets go; it settles into place as a full-size stone block with a crisp click. Camera: hold, then a slow pull back after the click.

Dialogue: audio voiceover only, strictly no speech bubbles, no dialogue boxes. Speak exactly the quoted lines once, in order; do not add, omit, paraphrase, repeat, caption, subtitle or display any words.

Voice: One off-screen adult male narrator throughout. General American accent, warm clean baritone, medium-low pitch, gentle chest resonance, no raspiness or breathiness. Calm conversational delivery, restrained pitch variation, steady speaking pace, and close, dry studio sound. Keep the same vocal timbre, register, accent, pace, and recording quality throughout. Emotional progression belongs to the visuals and music; do not change the narrator's voice or switch to character dialogue.

Audio: the same light plucked marimba and soft woodblock melody continues from clip 1 with identical tempo and instrumentation; a steady woodblock step on each of Than's strides; a soft knock at the pass; a crisp stone click when the block settles.

Final frame: the wall's top row is complete; Gạch stands at it with her left hand empty at her side and the wooden mallet in her right hand; Than stands back at the left with empty hands, smiling; Bấc glows at the right.
Hands at end — Than: right hand empty; left hand empty. Gạch: right hand holds the wooden mallet; left hand empty.

Negative constraints: no text, no letters or numbers anywhere, no signs with words, no game interface, no hotbar, no crosshair, no health or hunger icons, no inventory, no buttons, no logos, no brand marks, no watermark, no speech bubbles, no dialogue boxes, no existing video-game characters or creatures, no rounded or smooth limbs, no elbows, no knees, no bending along a box limb, no stretched limbs, no fingers, no limbs passing through bodies, no wristband on the left wrist, no swapped left and right hands, no prop switching hands without a visible pass, no hand or held block covering a face, no blurry, smeared or swimming textures, no texel grid changing size, no morphing, no duplicate characters, no realistic human bodies, no photoreal people, no 2D cartoon outlines, no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders.
```

## Clip 3 — The wall holds

```text
Output: approximately ten seconds, 16:9, 720p target, 24 FPS, synchronized audio.

Style and environment: a cozy blocky voxel world where everything is built from cubes: a small riverside village of mossy green ground blocks on a grey stone embankment, stone-block walls, bamboo, rice paddies, thatch and clay-tile roofs, in warm late-afternoon light. Every block face carries a low-resolution pixel texture of 16 by 16 square texels, rendered crisp with hard nearest-neighbour edges, never smoothed, blurred or painterly; the texel grid is the same size on every block and stays locked to the faces while the camera moves. Simple sunlit block lighting: top faces brightest, side faces a step darker, soft dark shading in the inside corners where blocks meet, soft short shadows under characters and blocks, no glossy highlights, a light distance haze. Clear blue sky with a few flat square clouds. A clean real-time 3D game-render look with a steady camera; not photoreal, not claymation, not smooth CGI.

Characters (exactly 4, no one else): Gạch, a blocky young builder: a cube head with warm tan skin and black hair under a white headscarf with red dots, a brick-red work jacket with a darker zip panel and two pockets and sleeves one shade darker, olive trousers, brown boots and a lemon-yellow band on the right wrist. Bà Lúa, a blocky grandmother farmer: warm tan skin, silver hair with a small bun at the back, a stepped conical straw hat in three tiers, an indigo button-front blouse with darker indigo sleeves, black trousers, brown sandals and a lemon-yellow band on the right wrist. Tí Mầm, a small blocky child with a big cube head: light skin, black hair and a small green sprout with two leaves growing from the top of his head, a cream T-shirt with a small green leaf on the chest, short cream sleeves, navy shorts, red sandals and a lemon-yellow band on the right wrist. Trâu Đá, a big slate-grey block water buffalo: a pale grey square muzzle, cream stepped horns built from small cubes that step out, back and up, four straight legs with dark hooves, a thin tail, no hands, and a lemon-yellow band round the right foreleg. Every character is built from rigid rectangular boxes. Limbs turn only where they meet the body, arms at the shoulders and legs at the hips, swinging as straight boxes; there are no elbows and no knees, and nothing bends along a limb. Heads turn at the neck and the upper body may tip forward a little. Walking swings the straight legs, and for characters with arms the opposite straight arm, forward and back. Hands are the plain square ends of the arms, with no fingers, and a small held block or tool sits in one box hand. Boxes never stretch, bend, round off or pass through each other. Faces are flat pixel faces painted on the front: expressions change only those pixels, never the head shape. Bà Lúa moves a little slower and smaller than the others and keeps her head up so the wide hat never hides her face. Trâu Đá walks on diagonal leg pairs and carries things only on its back. Every character wears one lemon-yellow band, one texel tall, round the right wrist (Trâu Đá round its right foreleg); never on the left.

Props: one wooden mallet: a short square brown handle with a grey stone cube head; one small brown seed pouch, a square cloth bag; one bundle of golden rice stalks tied in a square bale.

Composition: 16:9 wide three-quarter view of the finished wall at golden hour, full-body framing; Gạch at the left, Bà Lúa at the right, Tí Mầm walking in the middle ground, Trâu Đá walking behind along the wall.

Hands at start (time cut) — Gạch: right hand holds the wooden mallet; left hand empty. Bà Lúa: right hand empty; left hand empty. Tí Mầm: right hand holds the seed pouch; left hand empty.
First frame: Trâu Đá is already walking along behind the finished wall with the rice bundle on its back; Tí Mầm walks in front of the wall holding the seed pouch in his right hand; Bà Lúa raises her straight right arm to wave.

Timed beats:
- [0–3s] (VO: "Now the whole village walks past it."): Trâu Đá walks along the wall on its four straight legs, diagonal pairs swinging, the rice bundle steady on its back. Bà Lúa waves her straight right arm slowly from the shoulder. Camera: slow pull back to the wide shot.
- [3–7s] (VO: "Tí Mầm brings seeds for the new field."): Tí Mầm walks along the wall, his short straight legs swinging, holding the seed pouch in his right hand. Gạch lifts the wooden mallet in her right hand and taps the new stone once, gently. Camera: slow lateral track along the wall.
- [7–10s] (VO: "What would you build first in your village?"): Gạch raises both straight arms high beside her head, the wooden mallet still in her right hand. Bà Lúa lifts both straight arms out to the sides in a happy cheer, keeping her head up. Tí Mầm hops once with straight legs. Camera: hold.

Dialogue: audio voiceover only, strictly no speech bubbles, no dialogue boxes. Speak exactly the quoted lines once, in order; do not add, omit, paraphrase, repeat, caption, subtitle or display any words.

Voice: One off-screen adult male narrator throughout. General American accent, warm clean baritone, medium-low pitch, gentle chest resonance, no raspiness or breathiness. Calm conversational delivery, restrained pitch variation, steady speaking pace, and close, dry studio sound. Keep the same vocal timbre, register, accent, pace, and recording quality throughout. Emotional progression belongs to the visuals and music; do not change the narrator's voice or switch to character dialogue.

Audio: the same light plucked marimba and soft woodblock melody continues from clip 1 with identical tempo and instrumentation; slow heavy hoof thuds; one gentle stone tap; a soft happy chime at the end.

Final frame: the four of them stand along the finished wall in golden light: Gạch with both arms raised, Bà Lúa with both arms out, Tí Mầm landed from his hop with the seed pouch in his right hand, Trâu Đá behind with the rice bundle on its back.
Hands at end — Gạch: right hand holds the wooden mallet; left hand empty. Bà Lúa: right hand empty; left hand empty. Tí Mầm: right hand holds the seed pouch; left hand empty.

Negative constraints: no text, no letters or numbers anywhere, no signs with words, no game interface, no hotbar, no crosshair, no health or hunger icons, no inventory, no buttons, no logos, no brand marks, no watermark, no speech bubbles, no dialogue boxes, no existing video-game characters or creatures, no rounded or smooth limbs, no elbows, no knees, no bending along a box limb, no stretched limbs, no fingers, no limbs passing through bodies, no wristband on the left wrist, no swapped left and right hands, no prop switching hands without a visible pass, no hand or held block covering a face, no blurry, smeared or swimming textures, no texel grid changing size, no morphing, no duplicate characters, no realistic human bodies, no photoreal people, no 2D cartoon outlines, no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders.
```

## Stitching guide

1. Clip 1 → Clip 2: clip 1 ends with Gạch beside the gap, mallet in her right hand, looking left; clip 2 opens with Gạch at the same spot facing left as Than walks in from the left edge. Hard cut on Than's first step; 4–6 frame audio crossfade on the marimba.
2. Clip 2 → Clip 3: approved time cut to golden hour at the same wall. What continues: Gạch, her mallet in the right hand, the finished wall. What changes: light, Than and Bấc leave, Bà Lúa, Tí Mầm and Trâu Đá join. Hard cut; no dissolve (a dissolve between block worlds smears the texel grid).
3. If Flow blurs the small stone growing into the full block, trim clip 2 to cut on the click.
4. Inspect each real join: if a clip ends on a different hand or side of the frame, trim to the last frame that matches the Hands at end line rather than trusting the prompt. Check every frame for game UI, text, a familiar green mob or a green-lip-over-dirt block before publishing.

## Voice and music continuity note

- Every clip repeats the same narrator paragraph word for word, and clips 2–3 say the marimba and woodblock continue from clip 1 with identical tempo and instrumentation. Check by listening to the three clips back to back.
- If the voice or score drifts, first retest a voice-only change with the visuals, dialogue and music held fixed; the fallback is one continuous external English VO and marimba track laid over the assembled picture.
- Post-production: no colour grade that softens edges; an optional 2× nearest-neighbour down-and-up pass can re-harden soft texels (untested; check faces after it).
