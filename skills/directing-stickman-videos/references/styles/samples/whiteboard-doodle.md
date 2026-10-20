# Multi-character prompt package — Whiteboard Doodle, 30s, 16:9 (gated, not tried on Flow)

Built by `make_cast_package.py` from the frozen blocks in `whiteboard-doodle.md` and the cast cards in `gallery/cast/cast_meta.json`. Lint facts: [`cast-prompts-30s.facts.md`](cast-prompts-30s.facts.md).

## Hook card

| Field | Value |
|---|---|
| Pattern | Visual metaphor |
| First frame (0.0s) | Bean and Mr. Square already drawn and frowning; the marker is mid-stroke on a cloud above Bean. |
| Hook hit | At about 1.5s the cloud closes and drops three rain strokes on Bean. |
| Sound cue | Soft marker squeak, then a light patter; no impact. |
| First spoken line | "A bad mood spreads fast." |
| Open loop and payoff | Who lifts the cloud? Paid off in clips 2 and 3 (the balloon passes). |
| Sound-off check | A muted viewer sees two gloomy doodles under a rain cloud. |

## Global continuity

- One board, no slides: Mr. Square at the left, Bean at the center right, Candy drawn between them in clip 1; upper-right third blank in every clip (overlay zone).
- Props: one red balloon (Candy's right hand → Bean's left hand in clip 2 → Mr. Square's right hand in clip 3); Mr. Square's black briefcase stays in his left hand throughout; Bean never holds a marker.
- Each pass happens with the camera-side hands: Candy faces screen right, Bean faces screen left, Mr. Square faces screen right. Scene tracks for both passes (clip 2 Candy → Bean, clip 3 Bean → Mr. Square): `gallery/scene/` (`posture_gate.py check --scene`).
- One rain cloud: drawn in clip 1, Bean's half wiped in clip 2, Mr. Square's half in clip 3.
- VO words per clip: [22, 21, 20] (style target 18–22).

## Clip 1 — The rain cloud

```text
Create an approximately 10-second 16:9 horizontal whiteboard animation clip targeting 720p at 24 FPS with synchronized audio.

Opening hook: from the first frame Bean and Mr. Square already stand drawn on the board, both frowning, with the marker tip mid-stroke above Bean's head, and at about 1.5s the marker closes a small black rain cloud that drops three short rain strokes onto Bean with a soft marker squeak.

Board: a matte white whiteboard fills the entire frame, seen flat and front-on, soft even daylight, very faint gray ghosting of old erased marks. All drawings are black whiteboard-marker line art with slightly irregular hand-drawn strokes, natural ink density and rounded line ends, medium consistent line weight; characters and props are outlines left white inside. Lines appear exactly under the marker tip in natural stroke order; nothing appears ahead of the tip and nothing fades in. The only other marker colors are red, blue and green, used on small areas such as a blush, a bow, a tie, a collar, a scarf, a balloon, a small circle or an arrow. No painted background, no shading, no gradients, no 3D.

Drawing hand: one adult right hand holding a black whiteboard marker with the cap off enters from the lower right; plain dark sleeve cuff at the frame edge, no rings, no watch, five natural fingers, one marker. It stays at the edge of the drawing and leaves frame while the doodles move.

Cast: Bean, Candy and Mr. Square are told apart by shape, never by color alone: Bean has the big round head and bean body, Candy is the smallest with pigtails and a triangle dress, Mr. Square has the square head and the widest jacket.

One hand-drawn whiteboard doodle character in black marker ink called Bean: a large round head with one small curly hair loop on top, two small solid dot eyes, short curved eyebrows, a small smile line and two tiny red marker blush strokes on the cheeks; below it a bean-shaped body outline, slightly narrower at the top, left white inside; two thin curved noodle arms ending in small round hollow hands; two short leg lines ending in small rounded shoe shapes. No clothing and no other hair. The head is about as wide as the body and about one third of the total height. Slightly irregular hand-drawn strokes with medium, consistent marker weight. Exactly two arms and two legs; a moving limb replaces its previous pose. Expressions change only the eyes, eyebrows and mouth; head size, bean body and proportions stay the same in every shot.

One hand-drawn whiteboard doodle character in black marker ink called Mr. Square: a stocky man with a square head with rounded corners, a solid black side-parted hair cap, two small solid dot eyes, short eyebrows and a short flat black moustache above a small mouth line; below it a wide rectangle jacket outline with a V collar, left white inside, and a solid blue marker tie; two thin arms ending in small round hollow hands; two straight leg lines ending in small black shoes. No blush and no other hair. The head is narrower than the jacket, and he is the widest of the cast and about as tall as Bean. Slightly irregular hand-drawn strokes with medium, consistent marker weight. Exactly two arms and two legs; a moving limb replaces its previous pose. Expressions change only the eyes, eyebrows and mouth; square head, jacket and proportions stay the same in every shot.

One hand-drawn whiteboard doodle character in black marker ink called Candy: a small child with a big round head, two short solid black pigtails tied with tiny red bows, two small solid dot eyes, short curved eyebrows, a wide smile line and two tiny red marker blush strokes on the cheeks; below it a short triangle dress outlined in green marker with a dotted green waistline, left white inside; two short thin arms ending in small round hollow hands; two short leg lines ending in small rounded black shoes. No other hair and no other clothing. The head is wider than the top of the dress, and she is about three quarters of Bean's height. Slightly irregular hand-drawn strokes with medium, consistent marker weight. Exactly two arms and two legs; a moving limb replaces its previous pose. Expressions change only the eyes, eyebrows and mouth; head size, triangle dress and proportions stay the same in every shot.

Layout on the board: Mr. Square stands at the left, Bean at the center right; Candy is drawn between them. The upper-right third of the board stays completely blank.

First frame: Mr. Square drawn at the left and Bean drawn at the center right, both frowning; the marker tip is mid-stroke on a small cloud above Bean's head. Candy is not drawn yet.
Hands at start — Bean: right hand empty; left hand empty. Mr. Square: right hand empty; left hand holds the black briefcase. Drawing hand: right hand holds the black whiteboard marker.

[0–3s] (VO: "A bad mood spreads fast."): Camera holds. The marker closes the rain cloud above Bean; three short rain strokes fall on him and his shoulders drop.
[3–7s] (VO: "One gloomy cloud, and the whole line sags."): Camera holds. The hand stretches the cloud with one long stroke to the left until it also hangs over Mr. Square; his frown deepens and he glances at his wrist.
[7–10s] (VO: "Then a small girl shows up with a balloon."): Slow lateral track left. The hand draws Candy between them in stroke order: head, pigtails and bows, face, green triangle dress, arms, legs, then a red balloon on a string held in her right hand. The hand leaves frame and Candy bounces once, looking at Bean.

Dialogue: audio voiceover only, strictly no speech bubbles, no dialogue boxes. Speak exactly the quoted lines once, in order; do not add, omit, paraphrase, repeat, caption, subtitle or display any words.

One off-screen adult female narrator throughout. General American accent, warm clear mezzo voice, medium pitch, soft smile in the tone, no raspiness or breathiness. Calm conversational delivery, restrained pitch variation, steady speaking pace, and close, dry studio sound. Keep the same vocal timbre, register, accent, pace, and recording quality throughout. Emotional progression belongs to the visuals and music; do not change the narrator's voice, and the doodle characters never speak.

Audio: Voiceover clearly audible over light, playful ukulele with soft pizzicato strings, gentle and curious; synchronized marker squeaks on every stroke and a small pop when a doodle comes alive.

Final frame: Candy between the two, the balloon floating above her right hand, both men under the rain cloud.
Hands at end — Bean: right hand empty; left hand empty. Mr. Square: right hand empty; left hand holds the black briefcase. Candy: right hand holds the red balloon string; left hand empty. Drawing hand: right hand holds the black whiteboard marker.

Negative constraints: no painted or full-color backgrounds, no paper texture, no chalkboard, no glass reflections, no 3D, no shading or gradients, no lines appearing ahead of the marker tip, no whole-drawing fade-ins, no morphing of drawings into other drawings, no extra hands, no deformed fingers, no more than one marker in hand, no extra doodle characters, no character taking another character's features, no dark-filled bodies, no visible letters, numbers, scribbled pseudo-text, captions, subtitles, logos or watermarks, no speech bubbles, no dialogue boxes, no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no prop switching hands without a visible pass. Do not alter, omit, repeat, reorder or add dialogue.
```

## Clip 2 — The balloon pass

```text
Create an approximately 10-second 16:9 horizontal whiteboard animation clip targeting 720p at 24 FPS with synchronized audio.

Board: a matte white whiteboard fills the entire frame, seen flat and front-on, soft even daylight, very faint gray ghosting of old erased marks. All drawings are black whiteboard-marker line art with slightly irregular hand-drawn strokes, natural ink density and rounded line ends, medium consistent line weight; characters and props are outlines left white inside. Lines appear exactly under the marker tip in natural stroke order; nothing appears ahead of the tip and nothing fades in. The only other marker colors are red, blue and green, used on small areas such as a blush, a bow, a tie, a collar, a scarf, a balloon, a small circle or an arrow. No painted background, no shading, no gradients, no 3D.

Drawing hand: one adult right hand holding a black whiteboard marker with the cap off enters from the lower right; plain dark sleeve cuff at the frame edge, no rings, no watch, five natural fingers, one marker. It stays at the edge of the drawing and leaves frame while the doodles move.

Cast: Bean, Candy and Mr. Square are told apart by shape, never by color alone: Bean has the big round head and bean body, Candy is the smallest with pigtails and a triangle dress, Mr. Square has the square head and the widest jacket.

One hand-drawn whiteboard doodle character in black marker ink called Bean: a large round head with one small curly hair loop on top, two small solid dot eyes, short curved eyebrows, a small smile line and two tiny red marker blush strokes on the cheeks; below it a bean-shaped body outline, slightly narrower at the top, left white inside; two thin curved noodle arms ending in small round hollow hands; two short leg lines ending in small rounded shoe shapes. No clothing and no other hair. The head is about as wide as the body and about one third of the total height. Slightly irregular hand-drawn strokes with medium, consistent marker weight. Exactly two arms and two legs; a moving limb replaces its previous pose. Expressions change only the eyes, eyebrows and mouth; head size, bean body and proportions stay the same in every shot.

One hand-drawn whiteboard doodle character in black marker ink called Mr. Square: a stocky man with a square head with rounded corners, a solid black side-parted hair cap, two small solid dot eyes, short eyebrows and a short flat black moustache above a small mouth line; below it a wide rectangle jacket outline with a V collar, left white inside, and a solid blue marker tie; two thin arms ending in small round hollow hands; two straight leg lines ending in small black shoes. No blush and no other hair. The head is narrower than the jacket, and he is the widest of the cast and about as tall as Bean. Slightly irregular hand-drawn strokes with medium, consistent marker weight. Exactly two arms and two legs; a moving limb replaces its previous pose. Expressions change only the eyes, eyebrows and mouth; square head, jacket and proportions stay the same in every shot.

One hand-drawn whiteboard doodle character in black marker ink called Candy: a small child with a big round head, two short solid black pigtails tied with tiny red bows, two small solid dot eyes, short curved eyebrows, a wide smile line and two tiny red marker blush strokes on the cheeks; below it a short triangle dress outlined in green marker with a dotted green waistline, left white inside; two short thin arms ending in small round hollow hands; two short leg lines ending in small rounded black shoes. No other hair and no other clothing. The head is wider than the top of the dress, and she is about three quarters of Bean's height. Slightly irregular hand-drawn strokes with medium, consistent marker weight. Exactly two arms and two legs; a moving limb replaces its previous pose. Expressions change only the eyes, eyebrows and mouth; head size, triangle dress and proportions stay the same in every shot.

Layout on the board: Mr. Square stands at the left, Bean at the center right; Candy is drawn between them. The upper-right third of the board stays completely blank.

First frame: matches the previous clip's final frame.
Hands at start — Bean: right hand empty; left hand empty. Mr. Square: right hand empty; left hand holds the black briefcase. Candy: right hand holds the red balloon string; left hand empty. Drawing hand: right hand holds the black whiteboard marker.

[0–3s] (VO: "She sees the cloud and does something kind."): Camera holds. Candy faces screen right and walks up to Bean, who turns to face screen left toward her. Candy holds the red balloon string out in her right hand.
[3–7s] (VO: "She hands over her balloon."): Camera holds during the pass. Bean reaches out with his left hand, the hand on the camera side; Candy passes the balloon string from her right hand into Bean's left hand in one slow visible pass, both hands on the string for a moment.
[7–10s] (VO: "No speech, no plan, just a small gift."): Slow push-in on Bean. His frown turns into a wide smile, and the drawing hand wipes the cloud above him away with the side of its fist. Candy steps back with empty hands.

Dialogue: audio voiceover only, strictly no speech bubbles, no dialogue boxes. Speak exactly the quoted lines once, in order; do not add, omit, paraphrase, repeat, caption, subtitle or display any words.

One off-screen adult female narrator throughout. General American accent, warm clear mezzo voice, medium pitch, soft smile in the tone, no raspiness or breathiness. Calm conversational delivery, restrained pitch variation, steady speaking pace, and close, dry studio sound. Keep the same vocal timbre, register, accent, pace, and recording quality throughout. Emotional progression belongs to the visuals and music; do not change the narrator's voice, and the doodle characters never speak.

Audio: Voiceover seamlessly continues the identical light, playful ukulele with soft pizzicato strings, gentle and curious from clip 1, maintaining identical tempo and instrumentation; synchronized marker squeaks on every stroke and a small pop when a doodle comes alive.

Final frame: Bean smiles with the balloon string in his left hand. Candy stands back with empty hands. Mr. Square, still under his part of the cloud, looks toward Bean.
Hands at end — Bean: right hand empty; left hand holds the red balloon string. Mr. Square: right hand empty; left hand holds the black briefcase. Candy: right hand empty; left hand empty. Drawing hand: right hand holds the black whiteboard marker.

Negative constraints: no painted or full-color backgrounds, no paper texture, no chalkboard, no glass reflections, no 3D, no shading or gradients, no lines appearing ahead of the marker tip, no whole-drawing fade-ins, no morphing of drawings into other drawings, no extra hands, no deformed fingers, no more than one marker in hand, no extra doodle characters, no character taking another character's features, no dark-filled bodies, no visible letters, numbers, scribbled pseudo-text, captions, subtitles, logos or watermarks, no speech bubbles, no dialogue boxes, no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no prop switching hands without a visible pass. Do not alter, omit, repeat, reorder or add dialogue.
```

## Clip 3 — Passing it on

```text
Create an approximately 10-second 16:9 horizontal whiteboard animation clip targeting 720p at 24 FPS with synchronized audio.

Board: a matte white whiteboard fills the entire frame, seen flat and front-on, soft even daylight, very faint gray ghosting of old erased marks. All drawings are black whiteboard-marker line art with slightly irregular hand-drawn strokes, natural ink density and rounded line ends, medium consistent line weight; characters and props are outlines left white inside. Lines appear exactly under the marker tip in natural stroke order; nothing appears ahead of the tip and nothing fades in. The only other marker colors are red, blue and green, used on small areas such as a blush, a bow, a tie, a collar, a scarf, a balloon, a small circle or an arrow. No painted background, no shading, no gradients, no 3D.

Drawing hand: one adult right hand holding a black whiteboard marker with the cap off enters from the lower right; plain dark sleeve cuff at the frame edge, no rings, no watch, five natural fingers, one marker. It stays at the edge of the drawing and leaves frame while the doodles move.

Cast: Bean, Candy and Mr. Square are told apart by shape, never by color alone: Bean has the big round head and bean body, Candy is the smallest with pigtails and a triangle dress, Mr. Square has the square head and the widest jacket.

One hand-drawn whiteboard doodle character in black marker ink called Bean: a large round head with one small curly hair loop on top, two small solid dot eyes, short curved eyebrows, a small smile line and two tiny red marker blush strokes on the cheeks; below it a bean-shaped body outline, slightly narrower at the top, left white inside; two thin curved noodle arms ending in small round hollow hands; two short leg lines ending in small rounded shoe shapes. No clothing and no other hair. The head is about as wide as the body and about one third of the total height. Slightly irregular hand-drawn strokes with medium, consistent marker weight. Exactly two arms and two legs; a moving limb replaces its previous pose. Expressions change only the eyes, eyebrows and mouth; head size, bean body and proportions stay the same in every shot.

One hand-drawn whiteboard doodle character in black marker ink called Mr. Square: a stocky man with a square head with rounded corners, a solid black side-parted hair cap, two small solid dot eyes, short eyebrows and a short flat black moustache above a small mouth line; below it a wide rectangle jacket outline with a V collar, left white inside, and a solid blue marker tie; two thin arms ending in small round hollow hands; two straight leg lines ending in small black shoes. No blush and no other hair. The head is narrower than the jacket, and he is the widest of the cast and about as tall as Bean. Slightly irregular hand-drawn strokes with medium, consistent marker weight. Exactly two arms and two legs; a moving limb replaces its previous pose. Expressions change only the eyes, eyebrows and mouth; square head, jacket and proportions stay the same in every shot.

One hand-drawn whiteboard doodle character in black marker ink called Candy: a small child with a big round head, two short solid black pigtails tied with tiny red bows, two small solid dot eyes, short curved eyebrows, a wide smile line and two tiny red marker blush strokes on the cheeks; below it a short triangle dress outlined in green marker with a dotted green waistline, left white inside; two short thin arms ending in small round hollow hands; two short leg lines ending in small rounded black shoes. No other hair and no other clothing. The head is wider than the top of the dress, and she is about three quarters of Bean's height. Slightly irregular hand-drawn strokes with medium, consistent marker weight. Exactly two arms and two legs; a moving limb replaces its previous pose. Expressions change only the eyes, eyebrows and mouth; head size, triangle dress and proportions stay the same in every shot.

Layout on the board: Mr. Square stands at the left, Bean at the center right; Candy is drawn between them. The upper-right third of the board stays completely blank.

First frame: matches the previous clip's final frame.
Hands at start — Bean: right hand empty; left hand holds the red balloon string. Mr. Square: right hand empty; left hand holds the black briefcase. Candy: right hand empty; left hand empty. Drawing hand: right hand holds the black whiteboard marker.

[0–3s] (VO: "And kindness travels down the line."): Camera holds. Candy steps aside to the lower left. Mr. Square faces screen right and walks up to Bean, the black briefcase in his left hand; Bean still faces screen left.
[3–7s] (VO: "Pass it on to the next frown,"): Camera holds during the pass. Mr. Square holds out his free right hand. Bean passes the balloon string from his left hand into Mr. Square's right hand in one slow visible pass, and the drawing hand wipes the cloud above Mr. Square away with the side of its fist.
[7–10s] (VO: "and the whole board ends up smiling."): Slow pull back to show all three. Mr. Square smiles under his moustache; the hand draws three small blue arrows linking the three of them, then leaves frame.

Dialogue: audio voiceover only, strictly no speech bubbles, no dialogue boxes. Speak exactly the quoted lines once, in order; do not add, omit, paraphrase, repeat, caption, subtitle or display any words.

One off-screen adult female narrator throughout. General American accent, warm clear mezzo voice, medium pitch, soft smile in the tone, no raspiness or breathiness. Calm conversational delivery, restrained pitch variation, steady speaking pace, and close, dry studio sound. Keep the same vocal timbre, register, accent, pace, and recording quality throughout. Emotional progression belongs to the visuals and music; do not change the narrator's voice, and the doodle characters never speak.

Audio: Voiceover seamlessly continues the identical light, playful ukulele with soft pizzicato strings, gentle and curious from clip 1, maintaining identical tempo and instrumentation; synchronized marker squeaks on every stroke and a small pop when a doodle comes alive.

Final frame: Mr. Square smiles with the balloon string in his right hand and the briefcase in his left hand. The other two smile with empty hands. The upper-right third is still blank.
Hands at end — Bean: right hand empty; left hand empty. Mr. Square: right hand holds the red balloon string; left hand holds the black briefcase. Candy: right hand empty; left hand empty. Drawing hand: right hand holds the black whiteboard marker.

Negative constraints: no painted or full-color backgrounds, no paper texture, no chalkboard, no glass reflections, no 3D, no shading or gradients, no lines appearing ahead of the marker tip, no whole-drawing fade-ins, no morphing of drawings into other drawings, no extra hands, no deformed fingers, no more than one marker in hand, no extra doodle characters, no character taking another character's features, no dark-filled bodies, no visible letters, numbers, scribbled pseudo-text, captions, subtitles, logos or watermarks, no speech bubbles, no dialogue boxes, no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no prop switching hands without a visible pass. Do not alter, omit, repeat, reorder or add dialogue.
```

## Stitching guide

- Clip 1 → 2: hard cut on matching frames (Candy between the two, balloon in her right hand).
- Clip 2 → 3: hard cut on matching frames (Bean smiling, balloon in his left hand).
- Trim each clip at its final frame; no dissolves (they read as fades on a whiteboard).

## Voice and music continuity

- The female narrator block is identical in all three clips; check by listening, not only by reading.
- Clip 1 sets the score; clips 2 and 3 continue it with identical tempo and instrumentation.

## Post-production overlay note

Optional overlays in the upper-right blank zone: clip 1 "Bad moods spread", clip 2 "Small kindness", clip 3 "Pass it on".

## What the first Flow test should check

1. Can a viewer tell the three apart in every frame without color?
2. Does the balloon move only through the two visible passes, and is there ever more than one balloon?
3. Does the briefcase stay in Mr. Square's left hand for all 30 seconds?
4. Does any character borrow another's features (blush on Mr. Square, tie on Bean, pigtails on Bean)?
5. Does the drawing hand keep five fingers and one marker, and leave frame when the doodles act?
