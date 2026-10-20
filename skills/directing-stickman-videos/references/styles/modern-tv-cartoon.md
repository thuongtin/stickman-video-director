# Modern TV Cartoon (style pack)

> In this repository: the sample package and its lint facts are `samples/modern-tv-cartoon.md` and `samples/modern-tv-cartoon.facts.md`. Other research files named below (gallery, tracks, gate output, renderer) stay in the project's `style-research/modern-tv-cartoon/` folder and are not part of the skill.

```text
Status: gated (2026-10-20). Covers: 3 clips, 3–4 characters on screen, flashlight and bug-jar handoffs, a low five,
a cane held through two clips, indoor sets, 16:9. Not covered: 9:16, crowds (5+), outdoor scenes, fights or sports.
```

Slug: `modern-tv-cartoon`. Evidence: posture gate on 114 pose tracks and a 2-shot motion test
([README.md](README.md), `gallery/gate-v2.txt`, `motion/motion-gate.txt`); the sample package
[samples/modern-tv-cartoon.md](samples/modern-tv-cartoon.md) passes `package_lint.py` and `hand_ledger.py`
([facts block](samples/modern-tv-cartoon.facts.md)); `tests/verify-opening-hook.py` passes on it.

## 1. Signature checklist

### Sources

The look of American TV animation from about 2010 to 2022. These works are named here as research only; prompts never name them, and the cast copies none of their characters, costumes or colour combinations.

Frame study (2026-10-20). Official character art and episode stills from the four shows' Wikipedia articles, downloaded and looked at side by side. They are low resolution (about 230–420 px) and few: one to two images per work, not whole episodes. Only these six images were looked at.

| Work | Image looked at | Confirms | Contradicts |
|---|---|---|---|
| *Adventure Time* (2010–2018) | [Marceline playing bass, episode still](https://upload.wikimedia.org/wikipedia/en/4/48/Adventure_Time_-_Marceline.png); [title card, Finn and Jake on a peak](https://upload.wikimedia.org/wikipedia/en/3/37/Adventure_Time_-_Title_card.png) | Black dot eyes; noodle arms with no elbow corner (Marceline's arms, Finn's raised arms); flat fills on the characters; thin dark outline | Backgrounds are painted with soft texture (the stormy sky), not flat |
| *Steven Universe* (2013–2019) | [Steven character art](https://upload.wikimedia.org/wikipedia/en/d/d1/Steven_Universe_%28Steven_Universe_Future%29.webp); [Pearl and Rose, episode still](https://upload.wikimedia.org/wikipedia/en/e/e2/Pearl_and_Rose_embracing_in_Steven_Universe.jpg) | Round, bean-like body on short legs; big round head; flat fills; four-finger cartoon hands | Eyes are white circles with black pupils, not dots; the episode still has soft glow and same-hue (not dark) lines |
| *Gravity Falls* (2012–2016) | [Dipper Pines character art](https://upload.wikimedia.org/wikipedia/en/1/15/Dipper_Pines.png) | Thin even dark outline; flat fills with no shading on the character; thin limbs with no joint corners | Eyes are big white circles with dot pupils; the body is a narrow kid's body, not a bean |
| *Amphibia* (2019–2022) | [Anne Boonchuy character art](https://upload.wikimedia.org/wikipedia/en/9/9a/Anne_Boonchuy_pro.webp) | Thin dark outline; flat fills; noodle-thin legs with no knee corner; big round head with hair | Eyes are white circles with dot pupils; a stick-thin body, not a bean |

What the frames changed: the genre does not share one eye or body type. Dot eyes and bean bodies appear in only some of the shows (dot eyes in *Adventure Time*, a round body in *Steven Universe*); white circle eyes with dot pupils and thin kid bodies are just as common. What all four share is a big round head, very simple eyes, one thin dark line, flat character fills and limbs with no joint corners. The traits below now say so. This pack keeps dot eyes and bean bodies, and the frozen block is unchanged: they are a real variant of the genre (both are visible in the frames above), and the cast and the gate rules here were built on them. Painted backgrounds and glow appear in the sources but are left out of this pack (flat sets read more cleanly and keep hands visible).

### Five signature traits

| Tag | Trait (visible in a still) |
|---|---|
| `must` | Big round heads with very simple eyes and no iris detail; in this pack black dot eyes with one white highlight on bean-shaped bodies (the genre also uses white circle eyes with dot pupils and thin kid bodies) |
| `must` | Noodle arms and legs: smooth curves with no sharp elbows or knees, always the same length |
| `must` | One thin, even, dark outline on every character; flat fills on the characters with no shading, gradient or texture (this pack keeps the sets flat too) |
| `bonus` | Snappy key poses that read in silhouette, with emotion carried by the brows, the mouth and the torso lean |
| `forbidden` | Rubber stretch: arms that shoot out longer to point or grab, or legs that stretch on a jump |

### Nearest neighbour

Catalog: **Style 4 Cozy Storytelling** (round head, simple expressive face, full-colour sets). Two visible differences:

1. Style 4 has a white filled head and thin dark stick limbs. This style has skin-coloured heads with hair, and limbs with thickness and colour: sleeves, trousers and shoes.
2. Style 4 has one hero figure on soft-lit cinematic sets. This style has a cast of different body shapes on flat, evenly lit sets with no atmospheric light.

Research: whiteboard-doodle's "Đậu" also has a bean body and round head, but it is black marker on a white board with no fills and no set.

### Prompt wording for each `must` trait

The frozen style block below says each one in plain words. It is repeated verbatim in every clip.

## 2. Frozen style block

Repeat it verbatim in every clip, on its own line. The set goes on a separate `Environment:` line, which may change between clips.

```text
Style: modern American TV cartoon. Flat bright colour fills with no shading, no gradients and no texture; one thin, even, dark-plum outline on every shape. Characters have rounded bean-shaped bodies, big round heads, simple black dot eyes with one white highlight, small simple mouths, and bendy noodle arms and legs that curve smoothly instead of showing sharp elbows or knees. Noodle limbs always keep the same length: they bend by curving, never by stretching or shrinking. Hands are small rounded cartoon hands with four fingers. Snappy, clear key poses with smooth in-betweens; squash and stretch only on the body, never on the arms or legs. Seen from the front, the arms grow from the outer edge of the shoulders and hang with a visible gap from the waist; they never lie on the chest or belly. Palette: warm tan wood, navy, mustard yellow, teal and coral, with the light source as the brightest shape.
```

## 3. Cast cards (verbatim anchors)

Research cast: "The Gullport Fix-It Club". A small seaside town, Aunt Dot's repair shop, and something odd every summer. The characters differ first by silhouette (height and body shape), then by colour, then by one prop.

**June**: the leader: curious, brave, bossy. Prop: flashlight.

```text
June, an eleven-year-old girl: brown skin, a big round puff of dark curly hair tied with a coral hairband, dot eyes, a mustard-yellow raincoat with three round buttons, teal shorts, white socks, red sneakers, and a bright blue bead bracelet on her right wrist.
```

**Benny**: the little brother: hungry, loyal, collects bugs. Prop: bug jar.

```text
Benny, a seven-year-old boy: a short round egg-shaped body, brown skin, short dark hair with one curly tuft on top, a gap-toothed grin, a red-and-white striped T-shirt, navy shorts, green sneakers, and an orange sweatband on his right wrist.
```

**Marco**: the teen neighbour: lanky, anxious, tech whiz. Prop: walkie-talkie.

```text
Marco, a fourteen-year-old teen neighbour: very tall and thin with long noodle legs, a tall oval head, pale skin, a swoop of ginger hair, green headphones around his neck, a purple hoodie with a front pocket, blue jeans, white sneakers, and a black digital watch on his right wrist.
```

**Aunt Dot**: the aunt who runs the repair shop: loud, warm, fearless. Prop: wrench.

```text
Aunt Dot, a stout pear-shaped woman in her forties: tan skin, a short magenta bob with straight bangs, a coral headband, huge round glasses, a coral T-shirt under blue denim overalls, brown work boots, and a gold bangle on her right wrist.
```

**Grandpa Lou**: Dot's father: slow, dry jokes, secretly the bravest. Prop: cane.

```text
Grandpa Lou, a small stooped old man: pale skin, a bald round head with white tufts over the ears, a huge white moustache, bushy white eyebrows, an olive-green cardigan over a white shirt, brown trousers, dark brown shoes, and a red string bracelet on his right wrist.
```

**Sprout**: a forest sprite living in the shop's attic: mute, curious, mischievous. Prop: acorn.

```text
Sprout, a tiny forest sprite about half the height of a seven-year-old child: a round leaf-green body with a pale green belly, a big round head with one curled leaf sprouting on top, huge dot eyes, no clothes, short green noodle limbs, and a small white flower tied to its right wrist.
```


After the anchors in every clip, add this rule once:

```text
Every character keeps exactly two arms and two legs, the same proportions, outfit and colours in every frame, and the same wrist marker on the RIGHT wrist. Expressions change only the eyes, eyebrows and mouth.
```

Anchor rules:

- Write each anchor in this order: name and role, build, skin, hair, face marks, outfit colours from top to bottom, shoes, and one fixed marker on the **RIGHT** wrist.
- Keep props out of the anchors. A cane, flashlight or jar goes in `Props:` and in the `Hands` lines.
- Name no other character in an anchor ("a seven-year-old boy", not "her brother" or "June's brother"): the anchor is pasted into clips where that character is absent.

## 4. Core rules this style overrides

| Core rule | Override | Reason |
|---|---|---|
| Stick limbs with no thickness (Styles 1–4) | Noodle limbs with thickness and colour segments: sleeve, then skin; trousers, then sock and shoe | Thick colour limbs are part of the look. Length still never changes. |
| Plain or line faces | Dot eyes, eyebrows and a mouth that change per beat; only those three change | The genre is acted through faces |
| Piano and ambient score | The frozen xylophone and pizzicato score below | Spooky-fun comedy, not reflective explainer |
| One hero figure | An ensemble of 4–6 named characters, at most 4 on screen | Adventure-comedy is told by a group |
| Body bans | No limb stretch, even for gags; raised arms clear the big head (see section 7) | The gate failed every stretch, and big heads hide raised arms |

## 5. Text, motion, camera

- **Text policy: `post-overlay`.** The prompts ask for no words, letters or numbers in the frame, and shelves, boxes and signs carry no labels. Titles or subtitles, if a video needs them, are overlaid in post (see section 8).
- **Motion cadence: `smooth`.** Clear key poses with smooth in-betweens. Squash and stretch on the body only.
- **Camera.** Follow the camera grammar in `storyboard-template.md`.
  - Transition moves: hold, slow push-in, pull back, slow lateral pan, hard cut.
  - Hold the camera while hands pass a prop, touch hands or kneel. Those are the risky moments for left/right and hand count.
  - Accents: at most one per video, a slam zoom on a punchline face. No camera shake or orbit: an orbit turns big heads past the shoulders.
  - Do not let three clips in a row end on a push-in. The sample goes hold → hold → push-in, then hold → pan → pull back, then hold → hold → push-in.

## 6. Voice and score

The shared voice contract (`voice-continuity.md`) still applies; this style does not recast the narrator. The sample uses the block below verbatim in every clip.

```text
Voice: One off-screen adult female narrator throughout. General American accent, bright friendly mid-range voice, clean and close, no raspiness. Light, upbeat conversational delivery with a steady pace. Keep the same vocal timbre, accent, pace and recording quality throughout; do not switch to character voices.

Dialogue: audio voiceover only, strictly no speech bubbles, no dialogue boxes. Speak exactly the quoted lines once, in order; do not add, omit, paraphrase, repeat, caption, subtitle or display any words.
```

Score, frozen. Clip 1 sets it:

```text
Audio: A light, playful, spooky-fun xylophone and pizzicato strings theme at a medium-slow walking tempo; <SFX>
```

Clips 2–N:

```text
Audio: continue the identical light, playful, spooky-fun xylophone and pizzicato strings theme at a medium-slow walking tempo from clip 1, with identical tempo and instrumentation; <SFX>
```

SFX may change per clip: cartoon boings, claps, creaks, twinkles. Any change to the music itself, such as a music-box ending, is done in post.

## 7. Style bans and posture limits

Gating 114 rig-drawn pose tracks (6 characters × 19 actions; walk and run from CMU motion capture) found 21 failing drafts. A re-run on the updated gate found one more habit. Each failure traced to one of these habits. Put the matching phrase in the beat.

- **No rubber stretch.** The style invites an arm that shoots out to point or grab. That failed every time (bone stretch 112–140%). Reach with the body instead: a step and a lean.
- **Raised arms clear the big head.** In front view, arms raised overhead cross the head. Ask for "both arms up in a wide V beside the head".
- **In profile, the near arm stays below the face.** The arms are shorter than the head is tall. A raised near arm is drawn across the face, and a raised far arm disappears behind the head. Ask for "aims forward and up, arm below the face".
- **Two big heads cannot touch hands in profile.** Their arms are shorter than their head radius, so the heads collide before the hands meet. Stage high fives and hand-offs between short characters side by side, facing the camera, with "a low five at shoulder height, below both faces".
- **Arms hang with a gap.** Pear and bean bodies are wider at the belly than at the chest, so an arm hanging straight down lies on the belly. Ask for "arms hang with a visible gap from the waist".
- **Crouches are hip-deep, not ankle-deep.** A crouch with the knees forward and the feet flat needs 52° of ankle flex (limit 35°). Fold at the hips so the thighs are near level.
- **Lean back with the legs.** Laughing or recoiling backward with the feet left forward tips the centre of mass behind the heels. Ask for "leans back with the feet under the body".
- **Kneel with the shins on the floor.** A fall onto all fours drafted with the toes down left the knees 20% of the body height in the air. Ask for "lands on hands and knees, shins flat on the floor".
- **In profile, a prop in the far hand reads as in the near hand** whenever the near arm passes it. Carry it in the near hand, or swing it back behind the hip.
- **Keep the prop's tail clear of the wrist marker.** A dark flashlight tail below the fist read as Marco's black watch on the wrong wrist. Props are light grey or coloured, never the colour of a wrist marker.

Negatives, verbatim in every clip. They include the five shared posture negatives from `posture-gate.md`:

```text
Negative constraints: no 3D render, no CGI, no anime style, no realistic anatomy, no shading or gradients, no texture, no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no prop switching hands without a visible pass, no limbs stretching or shrinking, no extra arms, legs or fingers, no duplicate characters, no unintended extra people or creatures, no outfit or colour swapped between characters, no wrist marker moving to the other wrist, no raised arm or prop covering a face, no heads overlapping, no limb jumping to a new position without an in-between, no visible text, letters or numbers, no speech bubbles, no logos, no watermark.
```

## 8. Post-production

1. Trim each clip to its 10 s beats and cut hard between clips. Clip 3 is a time cut.
2. Check the risky frames before stitching: each hand pass, the low five, and each character's first frame for the RIGHT-wrist marker. Re-generate a clip if a marker has moved to the other wrist.
3. Normalise the stitched video to about -14 LUFS integrated, with the hook hit no more than 6 dB above the music bed.
4. Add any ending variation in post (for example a single music-box phrase under the last line), not in the prompt.
5. Subtitles, if wanted, are burned in after stitching. Never ask for them in the prompt.

## 9. Hook override

Reaction before cause, Sudden entry and Visual metaphor suit this style: a big-eyed double-take reads instantly. The sample uses Reaction before cause / Sudden entry (a flashlight beam finds a face at 1.2 s and both characters jump). A cartoon boing plus a gasp is the loudest the hit may be, within the loudness limit above. No impact booms.

## 10. Sample package and gates

- [samples/modern-tv-cartoon.md](samples/modern-tv-cartoon.md): 3 clips, "Who's in the attic?", with 3, 4 and 3 characters on screen.
- `tools/package_lint/package_lint.py package.md --clips 3 --anchor "<style block>" --anchor "<negatives>"`: PASS, 0 red, 0 yellow. [Facts block](samples/modern-tv-cartoon.facts.md).
- `hand_ledger.py`: PASS. Four controls, each with one deliberate error, all fail ([ledger-output.txt](package/ledger-output.txt)).
- Posture gate: 114/114 pose tracks PASS with 0 warnings. 7/7 motion tracks and both `--scene` shots PASS ([README.md](README.md)).

## 11. Catalog entry (ready to merge)

Style matrix row:

```text
| **modern-tv-cartoon** | Modern TV Cartoon | Flat bright fills, one thin even outline, simple indoor sets, no shading | Comedy explainers, kids and family stories, small-town adventure and mystery told by an ensemble | Bean bodies, big round heads with dot eyes, noodle limbs that keep their length, one RIGHT-wrist marker per character |
```

Status row:

```text
| modern-tv-cartoon | gated | Posture gate and package lint (`style-research/modern-tv-cartoon/`) |
```

Setup gate line (offered only when the user asks for an experimental style):

```text
modern-tv-cartoon (gated, experimental): modern American TV cartoon look with an ensemble cast.
```

Research files: `/mnt/project-files/style-research/modern-tv-cartoon/`.
