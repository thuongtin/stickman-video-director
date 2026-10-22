# Style Catalog: Visual Styles & Segment Spec Formulas

This catalog defines the supported visual styles for `directing-stickman-videos`, including character DNA locks, environment specifications, motion pacing, and negative constraints.

---

## 1. Style Matrix Overview

| Style Key | Style Name | Visual Theme | Best For | Character Design |
|---|---|---|---|---|
| **Style 1** | Classic Minimalist (Light / Dark) | Pure white or black canvas, monochrome lines, up to 3 saturated accent colors | High-density explainers, pure logic, mental models, fast-paced cognitive concepts | Hollow circle head, single-line body, no clothing, occasional simple line expressions |
| **Style 2A** | Modern Pop - Studio Tech (极简科技风) | Pure white high-key studio, subtle light-gray perspective grid, glowing cyan/blue glass UI | Tech tutorials, AI tool breakdowns, career insights, methodology breakthroughs | Default lead: dark buzz cut, dark rectangular glasses, plain white short-sleeved button-up shirt, dark blue jeans, black stick arms. Alternative: red beanie (no pom-pom), yellow t-shirt |
| **Style 2B** | Modern Pop - Cinematic Story (彩色故事风) | Full-color narrative environments, cinematic lighting & depth (warm room, dusk, desert, summit) | Emotional storytelling, personal growth, motivational journeys, narrative hooks | Same Style 2 lead (default or beanie alternative) staged inside rich environmental lighting |
| **Style 3** | Prehistoric Hand-Drawn / Dark Comedy (史前手绘 / 黑色幽默) | Earthy prehistoric environments, warm fire accents, subtle paper texture | Satirical stories, visual analogies, ironic callbacks | White filled heads, expressive cartoon faces, black stick limbs, variable story-specific cast |
| **Style 4** | Cozy Storytelling (治愈故事风) | Full-color 2D cartoon locations, gentle atmospheric light, varied cinematic shots | Relatable life stories, emotional growth, educational storytelling | White filled round head and slim torso, dark stick limbs, simple expressive face |

### Status

Levels follow `style-pack-template.md`: a level covers only the samples behind it. `core` marks the styles that ship with the skill from upstream; their looks were accepted upstream, and this repository has no rig or rendered sample for them yet except the Style 2 default lead.

| Style | Status | Evidence |
|---|---|---|
| Style 1 Dark | core | Upstream owner accepted the Dark character look, 2026-10-12/13 |
| Style 1 Light | core | Same look with the polarity swapped; no separate acceptance |
| Style 2A | core | Upstream style; the male voice block was accepted by listening, 2026-10-12 |
| Style 2B | core | Upstream style; no written acceptance |
| Style 2 default lead (buzz cut, glasses) | gated | Code-rendered sheet and motion clip in `docs/lead-character/`, all poses through `posture_gate.py` (`tests/verify-lead-character.py`); not yet used in a full rendered video. The Style 2A/2B evidence above was made with the beanie alternative |
| Style 3 | core | Upstream owner approved the look in three clips of one story, 2026-10-12 |
| Style 4 | core | Upstream owner selected two samples of the look, 2026-10-14 |
| chibi-anime | gated | `styles/chibi-anime.md`, sample `styles/samples/chibi-anime.md` with lint facts |
| paper-cutout | gated | `styles/paper-cutout.md`, sample `styles/samples/paper-cutout.md` with lint facts |
| whiteboard-doodle | gated | `styles/whiteboard-doodle.md`, sample `styles/samples/whiteboard-doodle.md` with lint facts |
| watercolor-storybook | gated | `styles/watercolor-storybook.md`, sample `styles/samples/watercolor-storybook.md` with lint facts |
| ink-wash | gated | `styles/ink-wash.md`, sample `styles/samples/ink-wash.md` with lint facts |
| mid-century | gated | `styles/mid-century.md`, sample `styles/samples/mid-century.md` with lint facts |
| dong-ho | gated | `styles/dong-ho.md`, sample `styles/samples/dong-ho.md` with lint facts |
| science-lab | gated | `styles/science-lab.md`, sample `styles/samples/science-lab.md` with lint facts |
| blueprint | gated | `styles/blueprint.md`, sample `styles/samples/blueprint.md` with lint facts |
| cell-biology | gated | `styles/cell-biology.md`, sample `styles/samples/cell-biology.md` with lint facts |
| retro-space | gated | `styles/retro-space.md`, sample `styles/samples/retro-space.md` with lint facts |
| youtube-storytime | gated | `styles/youtube-storytime.md`, sample `styles/samples/youtube-storytime.md` with lint facts |
| us-sitcom | gated | `styles/us-sitcom.md`, sample `styles/samples/us-sitcom.md` with lint facts |
| modern-tv-cartoon | gated | `styles/modern-tv-cartoon.md`, sample `styles/samples/modern-tv-cartoon.md` with lint facts |
| stylized-3d-family | gated | `styles/stylized-3d-family.md`, sample `styles/samples/stylized-3d-family.md` with lint facts |
| superhero | gated | `styles/superhero.md`, sample `styles/samples/superhero.md` with lint facts |
| dino-world | gated | `styles/dino-world.md`, sample `styles/samples/dino-world.md` with lint facts |
| toys | gated | `styles/toys.md`, sample `styles/samples/toys.md` with lint facts |
| chu-tieu | gated | `styles/chu-tieu.md`, sample `styles/samples/chu-tieu.md` with lint facts |
| vn-webcomic | gated | `styles/vn-webcomic.md`, sample `styles/samples/vn-webcomic.md` with lint facts |
| voxel-world | gated | `styles/voxel-world.md`, sample `styles/samples/voxel-world.md` with lint facts |
| brick-build | gated | `styles/brick-build.md`, sample `styles/samples/brick-build.md` with lint facts |
| tech-illustration | gated | `styles/tech-illustration.md`, sample `styles/samples/tech-illustration.md` with lint facts |

New styles are drafted with `style-pack-template.md` and named by slug.

### Experimental styles

Each style below is a slug-named pack in `styles/<slug>.md` with a gated sample package in `styles/samples/`. All are `gated`: rigs pass the posture gate and the sample passes `package_lint.py`. Offer them only when the user asks for an experimental style or names one, and say it is `gated`. Before planning, read the style's pack: its anchors, overrides, bans and acceptance list win over the generic rules here, as for Styles 3 and 4.

| Style Key | Style Name | Visual Theme | Best For | Character Design |
|---|---|---|---|---|
| `chibi-anime` | Chibi Anime | Flat cel-shaded 2D anime, thick soft dark-brown outline, soft pastel settings simpler than the characters | Everyday-life comedy, study tips, relationship sketches, children's content, reaction-heavy shorts | About two heads tall, big highlighted eyes, stubby limbs with mitten hands; a frozen cast told apart by hair and outfit |
| `paper-cutout` | Paper Cutout / Collage | Flat matte paper pieces with fibre, cut or torn edges and contact shadows on layered paper sets; stepped stop motion | Deadpan comedy; gentle stories and children's English | Rigid two-piece paper limbs on pins, paper-dot eyes, replacement mouths; story-specific cast from frozen cards |
| `whiteboard-doodle` | Whiteboard Doodle | Matte white board, black marker line art drawn on by a hand, red/blue/green marker accents, faint ghosting | Step-by-step explainers, habits and ideas built up piece by piece, light social stories | Đậu: big round head with a hair curl, bean body, noodle arms; optional cast of five shape-distinct doodles |
| `watercolor-storybook` | Watercolor Storybook | Transparent watercolor washes on warm off-white paper, unpainted highlights, paler backgrounds, slow multiplane parallax | Bedtime stories, children's education, fables, family and nostalgia | Painted picture-book characters (children, adults, small animals) with a thin sepia ink outline, dot eyes, rosy cheeks |
| `ink-wash` | Ink-Wash / Sumi-e | Black ink and gray wash on warm rice paper, misty mountains, large empty paper, one vermilion accent per character | Reflective explainers, habits and patience, craft, folk-tale style stories | Open brush-circle head, dot eyes, ink-blot hands, gray-wash clothing; each character's red accent in a different place |
| `mid-century` | 1950s Mid-Century Limited Animation | Sparse flat colour fields, hairpin-leg furniture, starburst shapes; unshaded fills printed slightly off-register from a thin line; held poses on twos | Satirical explainers, workplace and money topics, small ensembles of character types | Angular geometric torsos on stick-thin limbs, one fixed left/right marker each |
| `dong-ho` | Đông Hồ Folk Print | Flat natural-pigment blocks on shimmering điệp paper, black woodblock key line, off-register colour | Vietnamese culture, Tết and village stories, gentle fables | Round-faced villagers in folk costume, children four heads tall, adults six |
| `science-lab` | Science Lab Explainer | Bright flat 2D lab cartoon, steady navy outlines, mint-green school lab with coloured glassware | Science and how-it-works explainers for kids and families, hands-on demos | Team of six scientists in white lab coats and goggles, full cartoon faces, yellow band on the right wrist |
| `blueprint` | Engineering Blueprint | White construction lines on Prussian-blue cyanotype paper, drafting grid, blank dimension capsules, cutaway machines | Science, engineering, invention and how-it-works explainers | Six inventors and engineers as white-line figures with pin joints and centre lines, a solid white cuff on the right wrist |
| `cell-biology` | Cell-Biology Micro-World | Inside a blood vessel: translucent jelly cells on a pink lining-cell floor, pale peach plasma, histology-stain palette | Immunity, blood, wound-healing and infection explainers for kids and families | Six cell creatures with a rounded membrane body, visible nucleus, small face, tube arms, navy band on the right wrist; limbless germs |
| `retro-space` | Retro Space-Age Astronomy | 1960s space-poster illustration: flat grainy screen-print shapes, thin navy outline, halftone shading, dot stars, ringed planets | Space science explainers: orbits, gravity and free fall, the Moon, planets | One crew in rounded padded suits and clear bubble helmets, a mustard gauge on every right wrist |
| `youtube-storytime` | Storytime Animation | Flat 2D first-person storytime cartoon, even medium-weight outline, flat fills, radial-stripe cutaways to the narrator | Funny true stories told by a narrator about their own life | Big round heads, small bodies, thin limbs; the narrator appears as an avatar; text post-overlay; stepped motion |
| `us-sitcom` | Prime-Time Sitcom | Flat cel fills, one uniform black outline on everything, a locked-off front-facing living-room stage, no shading | Dry comedy about everyday life, family and office dynamics | Family-and-neighbour ensemble with natural skin tones, separate oval eyes, distinct silhouettes, one right-wrist marker each |
| `modern-tv-cartoon` | Modern TV Cartoon | Flat bright fills, one thin even outline, simple indoor sets, no shading | Comedy explainers, kids and family stories, small-town adventure told by an ensemble | Bean bodies, big round heads with dot eyes, noodle limbs that keep their length, one right-wrist marker each |
| `stylized-3d-family` | Stylized 3D Family Film | Warm stylized 3D homes and porches, soft three-light setup, satin skin, sculpted hair | Warm family stories, kids' explainers, holiday stories | Big-eyed stylized 3D humans, kids 2.5–4 heads and adults 4–5.5 heads tall, three-fingered hands, yellow band on the right wrist |
| `superhero` | Superhero Action Cartoon | Bright flat city skyline with a halftone-dot sky, cel shading with one hard shadow tone, speed lines and impact stars | Short action stories, team-up gags, hero explainers, kids' content (one narrator, no character voices) | Costumed cast with heroic proportions, one non-letter emblem each, white cuff band on the right wrist |
| `dino-world` | Dino World | Sunny Cretaceous valley, flat cel colour with one soft shade, thick warm dark-brown outline | Kids' dinosaur science, fossils, "how do we know?" stories | Cartoon dinosaurs with real body plans (level back, tail counterweight, pillar legs), yellow band on the right, plus kid explorer Lan |
| `toys` | Toys Come Alive | Real toys on a child's bedroom floor at dusk, floor-level macro lens, warm lamp and blue window light | Gentle kids' stories, teamwork and sharing, simple physics (balance, towers) | Six different toys, each bending only at its built joints, lime-green band on the right wrist |
| `chu-tieu` | Chú Tiểu Little Monks | Calm, near-empty temple yard in flat pastels with one thin warm brown-grey outline; no statues, altar or writing | Mindfulness and kindness lessons, Buddhist-inspired everyday stories, slow-living tips | Chibi temple cast (novices, a novice nun, an old monk teacher, a lay grandmother, a temple cat); bead bracelet on every right wrist |
| `vn-webcomic` | Vietnamese Web-Comic in Motion | Flat pastel Vietnamese alley, thick even outline, comic-strip hold-and-snap timing | One-joke relatable gags, literal wordplay, neighbourhood slice-of-life | Round animals about two heads tall, dot eyes that snap to empty white circles, red rubber band on the right wrist |
| `voxel-world` | Voxel Block World | A cube-built Vietnamese river village, crisp 16×16 pixel textures, flat block lighting | Building and teamwork stories, cause and effect, step-by-step assembly | Rigid box characters with cube heads and painted pixel faces; straight limbs swing only at shoulder and hip; right-wrist lemon band |
| `brick-build` | Brick-Built Town | A tabletop town of glossy plastic toy bricks on studded baseplates, macro lens, shallow depth of field, stop-motion on twos | How parts fit together, cause and effect, gentle kids' stories, small physics jokes | Brick figures: rounded-cube head with no stud, box torso, hinged two-piece limbs, round knob hands, lime ring on the right wrist |
| `tech-illustration` | Soft Tech Illustration | White and pale-blue 2.5D tech scenes: isometric white blocks, floating UI cards of bars, nodes and icons, clean dark-navy outlines with soft gradient shading | Software, AI and productivity explainers, app and onboarding stories, helper-robot stories | Outlined chibi team about 2.5 heads tall plus a white robot sidekick with a dark visor; cyan band on the right wrist |

For Style 3 read `prehistoric-dark-comedy.md`. It overrides this catalog's generic motion and piano rules. Fix the drawing grammar across stories, not one universal face; fix each approved character within a story.

For Style 4 read `cozy-storytelling.md`. Treat locations as story beats, not one universal room. Its English display name is **Cozy Storytelling**; do not rename it Sketchbook Stories, hand-drawn, or prehistoric.

---

## 2. Style 1: Classic Minimalist

### Polarity & Background
- **Light Theme**: Flat, uniform, digitally pure-white canvas. Strictly forbid gray tint, paper texture, gradients, shadows, lighting, bloom, fog, or 3D depth.
- **Dark Theme**: Flat, uniform, pitch-black canvas. Pure white line art with high-contrast accent colors.

### Character DNA

**Classic Dark — accepted faceless base:**
```text
Use minimalist two-dimensional white line animation. Show the same consistent stick figure with a hollow circular head, no face, no eyes, no mouth, no hair, no clothing, no filled body, stable proportions, connected line limbs, and uniform medium line weight. Exactly two arms and two legs are visible per figure. Each limb appears only in its current pose: raising or lowering the character's own right arm replaces that arm's previous line, never leaving a resting arm beneath an active arm. The figure stays white; accent colors affect only props and graphic effects.
```

**Classic Light — accepted faceless base:**
```text
Use minimalist two-dimensional black line animation. Show the same consistent stick figure with a hollow circular head, no face, no eyes, no mouth, no hair, no clothing, no filled body, stable proportions, connected line limbs, and uniform medium line weight. Exactly two arms and two legs are visible per figure. Each limb appears only in its current pose: raising or lowering the character's own right arm replaces that arm's previous line, never leaving a resting arm beneath an active arm. The figure stays black; accent colors affect only props and graphic effects.
```

Choose the theme, then freeze its full anchor and repeat it verbatim in every clip. Do not expand it into numeric ratios, pen paths, separate hand/foot shapes or body-volume descriptions; the rig holds the measurements, the spec holds the look. Keep pose, movement, props and camera in the timed sequence, not in competing character definitions. The current-pose rule applies to every limb; if the approved story uses a left-arm lead action, adjust the handedness once before freezing, never clip by clip. "Right" means the character's own right side, as in `posture-gate.md`. Preserve energetic actions and rich effects; draw motion trails on props or detached graphics, not as additional limb poses.

Occasional simple line expressions are allowed by default. Before freezing either base anchor, replace only "no face, no eyes, no mouth," with "occasional simple line expressions, no detailed facial features," and keep the spec's negative constraints compatible with that choice. If the user explicitly requests a faceless character, keep the base unchanged. Expressions never change head fill, head outline, body structure or proportions; no detailed eyes, pupils or realistic facial rendering.

Build the figure once as a rig (hollow circle head, one line per limb segment, round line caps) and reuse it in every segment; line weight is a rig setting, not a per-segment choice. Gate the rig's pose tracks with `posture-gate.md` before rendering.

### Palette Contract
- Maximum of three saturated accent colors named with ordinary words (e.g., vivid red, electric blue, warm gold).
- No technical color notations (hex, RGB, Pantone).

---

## 3. Style 2: Modern Pop

Style 2 has one recurring lead per video. The default is Nam (buzz cut, glasses, white short-sleeved button-up shirt, jeans). Nam keeps the beanie lead's body: the same big round white head on a very short neck, loose tee-cut shirt flaring slightly to just below the hips, short wide sleeves, thin black stick limbs and simple face; only the hair, glasses and clothes change. Upstream's red-beanie Zeke is kept as an alternative: use it only when the user asks for the beanie character or for Zeke by name. Never mix the two anchors in one video.

Character sheet, expressions, poses and a motion clip of the default lead: `docs/lead-character/` at repository level (code-rendered from a posture-gated rig).

### Character DNA Anchors (Anti-Deformation Lock)

To prevent character drift, bug-eye faces, or clothing loss across clips, use one of these exact character anchors:

**Character Anchor (every clip, verbatim):**
```text
A minimalist 2D animated stick figure with a big white round head on a very short neck, simple dot eyes, a very short dark buzz cut (close-cropped spiky black hair) and thick dark rectangular glasses, wearing a loose plain white short-sleeved button-up shirt with a small pointed collar, buttoned all the way down, cut like a t-shirt that flares slightly to just below the hips, with short wide sleeves rolled up above the elbows, with simple black stick arms and slim legs in dark blue jeans. Simple black lines, vibrant colors, smooth 2D animation style.
```

**Alternative: Beanie Zeke anchor (every clip, verbatim, only when the user asks for it):**
```text
A minimalist 2D animated stick figure wearing a bright red beanie (smooth rounded knit, no pom-pom) and a yellow t-shirt, with simple black stick limbs and shorts. Simple black lines, vibrant colors, smooth 2D animation style.
```

Repeat the chosen full anchor in clips 2–N as well. The earlier short form for later clips ("The same minimalist 2D animated stick figure in a bright red beanie and yellow shirt" followed by an ellipsis) dropped the no-pom-pom, limbs and shorts locks and is retired; no shortened form of either anchor is allowed. The full-anchor-every-clip form follows the Style 1, Style 4 and voice rules.

**Deformation Prevention Rules:**
- **No Realistic Facial Features**: Round white head with minimal dot eyes only. Never request detailed pupils, irises, or photorealistic facial contours; on a stick-figure head they read as bug eyes.
- **Glasses stay on** (default lead): in every shot, including jumps, bumps and close-ups, with clear lenses and the dot eyes behind them. No lens glare, no sunglasses, no glasses floating off the face. If a beat needs the glasses adjusted, the hand pushes them up and lets go; they never come off.
- **Buzz cut stays close-cropped** (default lead): no long, swept or spiked-up hair, no hat, no beanie.
- **Outfit locks** (default lead): the shirt is plain white with a thin black outline, buttoned, with a small pointed collar and a thin button line down the front; short wide sleeves rolled up above the elbows (drawn like the beanie lead's tee sleeves, flaring open) so the stick arms show below them. No pattern, logo, text or tie, no jacket, no long sleeves; jeans stay dark blue, never shorts. Light stubble is not in the anchor: at stick-figure scale it reads as dirt or a beard. Add "faint light stubble dots along the jaw" to the anchor only when the user asks, and then in every clip.
- **No Pom-Poms** (beanie alternative): Specify smooth rounded beanie top, with no pom-pom or winter tassels.
- **Always include every clothing lock**: a spec without the shirt describes a bare stick body; without the glasses and hair (or the beanie) it describes a standard Style 1 character.

---

### Sub-Style 2A: Modern Studio Tech (极简科技风)

**In Plain Language**: Apple 发布会式极简科技风。纯白亮面高光空间 + 极淡浅灰透视地砖网格 + 悬浮青蓝半透明玻璃 UI/微光质感。

#### Environment Specification
```text
in a modern bright white studio space with subtle light-gray perspective grid lines on the floor plane. High-key studio lighting, clean white negative space, sleek glowing cyan and electric blue glass holographic UI elements.
```

#### Mandatory Negative Constraints (Anti-Clutter)
Studio-tech sets drift toward motherboard circuitry, spaceship corridors and cracked concrete when they are dressed up for "tech". **Always append this negative clause in 2A segment specs:**
```text
Negative constraints: strictly minimalist studio aesthetic, no circuit board textures, no sci-fi wall panels, no spaceship corridors, no cracked concrete, no grunge textures, no photorealistic human skin, no speech bubbles, no dialogue text boxes.
```

#### Motion Dynamics (Readable Motion)
- **Do not use abstract liquid/morphing transformations** (e.g., stairs melting into a clock); they break the clean layered shapes and read as a change of style.
- **Use physical, character-driven interactions**:
  - Leaping and bumping an invisible glass ceiling with a comedic bounce.
  - Tapping a sneaker onto the floor grid to emit an expanding cyan ripple wave.
  - Pulling out a glowing light-pen to draw a crisp luminous line bridge across an abyss.
  - Touching a sleek floating glass panel to reveal an icon-only illuminated lock.
  - Pushing open a heavy minimalist vault door to step forward into bright horizon light.
- **Pacing**: Every 10-second clip must feature distinct actions across `[0–3s]`, `[3–7s]`, and `[7–10s]`. Never let the character stand idle or stare at the camera for multiple seconds.

---

### Sub-Style 2B: Cinematic Story (彩色故事风)

**In Plain Language**: Pixar 故事短片风。全彩沉浸式场景（暖光台灯卧室、黄昏窗前、荒野公路、云端山顶）+ 电影叙事光影。

#### Environment Specification
```text
in a rich full-color cinematic environment [describe setting: e.g., a dimly lit cozy bedroom with warm lamplight / a vast open desert highway under a glowing dusk sky / a dramatic mountain ridge above rolling golden clouds]. Cinematic volumetric lighting, soft depth of field, atmospheric narrative mood.
```

#### Character & Style Consistency
- The character remains the same minimalist 2D stick figure: the default lead's buzz cut, glasses, white button-up shirt and jeans (or the beanie alternative, if chosen).
- Maintain smooth 2D vector animation aesthetics for the character even within a textured, atmospheric background.

#### Negative Constraints
```text
Negative constraints: no photorealistic human skin or faces, no 3D humanoid CGI uncanny valley models, no chaotic line glitches, no speech bubbles, no dialogue text boxes.
```

---

## 4. Style 4: Cozy Storytelling (治愈故事风)

Minimalist expressive characters inside colorful cartoon worlds: an office, a metro platform, a street-side cafe, a park or another story-appropriate setting. Use close action inserts, wide establishing views, lateral tracking and motivated location cuts. Warmth belongs to the visual treatment; preserve the source's conflict and meaning rather than making every topic cheerful.

Each new ten-second segment normally establishes a different location. Keep the character, important props, screen direction and full voice profile consistent, while deliberately changing scenery. A new camera angle on the same desk is not a substitute for a new story location. Single-location requests and approved callbacks remain valid exceptions.

Use the full character anchor, prop-state rules and acceptance checklist in `cozy-storytelling.md`; do not inherit Style 1's hollow-head/no-face/no-filled-body bans or Style 3's crude sketch/animal-hide rules.

---

## 5. Universal Audio Continuity Contract

Voice continuity is a shared foundation for **all styles**, including Styles 3 and 4. Apply `voice-continuity.md` before style-specific music rules. Different videos can choose different voices, while all clips of one video repeat one complete approved voice profile. Keep voice identity separate from the musical arc.

### Narrator Voice Lock
```text
One off-screen adult male narrator throughout. General American accent, warm clean baritone, medium-low pitch, gentle chest resonance, no raspiness or breathiness. Calm conversational delivery, restrained pitch variation, steady speaking pace, and close, dry studio sound. Keep the same vocal timbre, register, accent, pace, and recording quality throughout. Emotional progression belongs to the visuals and music; do not change the narrator's voice or switch to character dialogue.
```
This is the user-accepted male example, not a compulsory voice for every project. For female, older, youthful or other approved voices, resolve a complete coherent profile using `voice-continuity.md`, then repeat it verbatim across every clip. Do not use only "same narrator" or inherit a prior clip by name. Keep narration audio-only, voice-first, with no speech bubbles or dialogue boxes. Listening acceptance exists for this male block only; other profiles are accepted when the user hears the recorded VO.

### BGM Continuity Lock

This piano-and-synth wording is the Style 1/2 default. Other styles choose their own instruments but keep the same continuity sentence in clips 2–N (`core-contract.md` C3).

- **Clip 1**:
  ```text
  Audio: Voiceover clearly audible over quiet, thoughtful piano and subtle soft ambient synth, building gentle optimistic momentum.
  ```
- **Clips 2–N**:
  ```text
  Audio: Voiceover seamlessly continues the identical quiet, thoughtful piano and subtle soft ambient synth from clip 1, maintaining identical tempo, instrumentation, and optimistic narrative momentum. Synchronized crisp SFX on physical actions.
  ```

---

## 6. Visual Beat Pacing Template (10-Second Clip)

Every segment spec must divide its 10 seconds into three active narrative beats:

```text
Timed Synchronized Visual Beats:
- [0–3s] (VO: "..."): [Setup / premise action — character enters, acts, or inherits momentum from previous clip]
- [3–7s] (VO: "..."): [Escalation / discovery — character interacts with environment or solves visual obstacle]
- [7–10s] (VO: "..."): [Climax & outgoing transition — character delivers payoff and initiates outgoing motion for next clip]
```
