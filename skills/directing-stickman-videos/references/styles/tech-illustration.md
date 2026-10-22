# Soft Tech Illustration (style pack)

> In this repository: the sample package and its lint facts are `samples/tech-illustration.md` and `samples/tech-illustration.facts.md`; the README preview is `docs/style-previews/tech-illustration.gif`. Other research files named below (renderer, gallery, tracks, gate output, sheets) stay in the project's `style-research/tech-illustration/` folder and are not part of the skill.

```text
Status: gated (2026-10-22). Covers: 3 clips, 1–2 characters on screen, a chip handoff from the robot to the lead, seated laptop work on a white block, floating UI cards, 16:9.
Not covered: Lan, Mai, Tung and Hai in a package, 9:16, crowds (3+ in one clip), outdoor scenes, fast action, text on screens.
```

Slug: `tech-illustration`. Evidence: posture gate on 133 pose track pairs (true 3D plus the drawing camera's projection) and a two-character motion test with `--scene`, all 0 errors and 0 warnings (`gallery/gate-v1.json`, `motion/gate-motion.txt`); the sample package [samples/tech-illustration.md](samples/tech-illustration.md) passes `package_lint.py` and `hand_ledger.py` ([facts block](samples/tech-illustration.facts.md)); `tests/verify-opening-hook.py` passes on it.

The soft 2.5D tech-explainer look used by app landing pages and SaaS explainers: chibi people with big round heads, clean dark-navy outlines and soft gradient shading, sitting on white isometric blocks with a laptop, a friendly white robot sidekick, and floating rounded UI cards (a code window, a flow diagram, a green check) on a white to pale-blue background with bright blue accents. All characters are original. Specs describe the look in plain words and never name a product, brand, icon set or app.

## 1. Signature checklist

### Sources

These works are named here as research only. Specs never name them, and the cast copies none of their characters, colours or layouts. Frames studied on 2026-10-22; local copies are in `research/` (the Fluent Emoji images are MIT-licensed; the icons8 previews are watermarked and kept only as a research record, never published).

| Work | Image looked at | Confirms | Contradicts, and what changed |
|---|---|---|---|
| The owner's reference image (shared in the project, 2026-10-22) | The image itself | Trait 1: a chibi developer with a big round head, black glasses, gray hoodie over a white tee, navy jeans and white sneakers. Trait 2: clean dark outlines with soft shading. Trait 3: floating UI cards (code window, flow diagram, green check). Trait 4: white isometric blocks, a plant, a white robot sidekick. Trait 5: a white and light-blue palette with blue accents. | The reference shows a fruit logo on the laptop lid and a code-hosting mascot on a card. Both are brand marks, so the lid here is plain aluminium and the cards carry only bars, nodes and icons (section 5). |
| icons8, "Robot and developer collaborating on code, AI-assisted programming" (3D isometric set) | Preview, https://ouch-prod-var-cdn.icons8.com/wm/illustrations/previews/hFKIvRcrMONTLxrf.webp | Trait 3: a floating flow-diagram card and a check bubble beside a developer at a laptop. Trait 4: a small robot sidekick with a dark visor and glowing eyes sharing the scene; the isometric three-quarter view from above. Soft shading on rounded forms. | No outlines at all and a lime-green palette, so the outline and the blue palette are this style's choices, not the genre's. Adult proportions (about four heads), not chibi. The robot rolls on treads; ours walks, so the posture gate covers it. |
| icons8, "Developer interface" (isometric set) | Preview, https://ouch-prod-var-cdn.icons8.com/rf/illustrations/previews/iaQDwXsI261QjlnI.webp | Trait 3: stacked floating UI tiles (a code-bracket tile, an image tile, toggles, a search bar) at an isometric angle. Clean dark outlines on flat fills. | Flat fills with no gradient shading, so soft shading is a `must` of this style rather than of every isometric tech set. |
| Microsoft Fluent Emoji 3D (MIT) | Technologist, https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Technologist/Default/3D/technologist_3d_default.png ; robot, https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Robot/3D/robot_3d.png ; laptop, https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Laptop/3D/laptop_3d.png | Trait 2: soft gradient shading on rounded, simplified forms; a white robot head with a dark visor and blue eyes; a plain silver laptop with no mark. | No outlines (soft 3D only), and the person is a bust, not a full chibi body. Kept as the shading reference; the outline comes from the reference image. |

What was looked at: the reference image, the two icons8 previews and the three Fluent Emoji images, at full size on 2026-10-22. They are illustrations, not video frames, so they show design, palette and staging, not motion. The motion grammar (small eased moves, UI cards popping in) is this pack's choice, checked in the code-rendered motion test.

Changes made because of the frames: the outline is a cast choice from the reference image, not a genre must; logos and mascots are banned and replaced by plain shapes; the robot walks on two short legs instead of treads so its hands can be gated like everyone else's.

### Five signature traits

| Tag | Trait (visible in a still) |
|---|---|
| `must` | Chibi people about two and a half heads tall: a big round head, a small body, short limbs, simple dot eyes with one catchlight |
| `must` | Clean, even dark-navy outlines around every shape, with soft gradient shading inside (no hard cel bands, no texture) |
| `must` | Floating rounded UI cards around the characters, each with a soft drop shadow: a code window of coloured bars, a node-and-arrow flow diagram, a round green check |
| `bonus` | White isometric blocks to sit on, a potted plant, small server towers, a white robot sidekick with a dark visor and glowing cyan eyes |
| `forbidden` | Brand marks of any kind (a logo on a laptop lid, an app mascot on a card), readable code or words on screens, photographic textures |

### Nearest neighbour

Catalog: **science-lab** (a clean explainer set with a cast of scientists). Two visible differences:

1. Science-lab is a flat 2D lab with lab coats and glassware. This style is soft 2.5D: rounded shaded volumes on isometric white blocks, seen a little from above.
2. Science-lab explains with apparatus in the room. This style explains with floating UI cards that pop in beside the characters.

Second neighbour: **blueprint** (technical line drawing on a blue ground). This style keeps a white ground and only uses blue as the accent.

### Spec wording for each `must` trait

The frozen style block below says each one in plain words. It is repeated verbatim in every clip.

## 2. Frozen style block

Repeat it verbatim in every clip. The set goes on a separate `Setting:` line, which may change between clips.

```text
Style: a soft 2.5D tech illustration brought to life, like a clean explainer animation for a software product. Chibi characters about two and a half heads tall with big round heads, small bodies and short rounded limbs, simple dark dot eyes with one white catchlight, small simple mouths and rosy cheeks. Every shape has a clean, even dark-navy outline and soft gradient shading inside, no texture, no hard shadow bands. The scene is seen from slightly above at a three-quarter isometric angle. White isometric blocks with softly rounded edges and a faint blue glow along their bottom edges serve as seats and tables. Floating rounded white UI cards hover around the characters with soft drop shadows, drawn as simple shapes: a code window is short coloured bars, a flow diagram is round nodes joined by arrows, a status badge is one round icon. Each clip names which cards are on screen. Cards carry shapes and icons only, never letters or numbers. Palette: white and very pale blue background with a soft radial glow, bright blue and cyan accents, gray and navy clothing, a touch of mint and orange for status icons; no neon, no dark scenes. Smooth, gentle motion: small eased moves, cards pop in with a slight overshoot, characters hold clear poses.
```

## 3. Cast cards (verbatim anchors)

Six original characters, a small software team and its robot. They differ first by silhouette (height, hair shape, the robot's egg body), then by one dominant colour. Model sheets: `sheets/model-<name>.png` (front, 3/4, side, back, ten expressions, palette); lineup: `sheets/cast-lineup.png`; hero still: `sheets/style-frame.png`; poses: `gallery/poses-<name>-v1.png`.

| Character | Role | Anchor |
|---|---|---|
| Khoa | lead developer | Khoa: a young man, chibi, about two and a half heads tall. Big round head, light peach skin, messy short black hair with a soft fringe, thick black rectangular glasses, dark eyes. A light-gray zip hoodie worn open over a plain white t-shirt, with gray drawstrings and a hood behind his neck, navy jeans, plain white sneakers. |
| Bit | robot sidekick | Bit: a small white robot, about two heads tall, a round glossy white head with a dark navy face screen and two glowing cyan oval eyes, round blue ear pods, a short antenna with a blue bead, an egg-shaped white body with a small cyan chest light, short white arms with round dark-gray mitten hands, short legs and dark gray feet. |
| Lan | UI designer | Lan: a young woman, chibi, about two and a half heads tall. Big round head, light peach skin, a dark-brown chin-length bob with a straight fringe, dark eyes. A sky-blue sweater, white trousers, pale-blue sneakers. |
| Mai | product lead | Mai: a young woman, chibi, about two and a half heads tall. Big round head, warm light-tan skin, a black high ponytail tied with a mint band, dark eyes. A mint-green jacket worn open over a white t-shirt, gray trousers, white sneakers. |
| Tung | senior engineer | Tung: an older man, chibi, the tallest of the team, about two and three-quarter heads tall. Big round head, warm tan skin, short silver-gray hair, a short neat silver beard, dark eyes. A navy cardigan over a pale-blue shirt, gray trousers, brown shoes. |
| Hai | intern | Hai: a young man, chibi, the shortest of the team, about two and a quarter heads tall. Big round head, light peach skin, spiky brown hair, dark eyes, white headphones resting around his neck. A cobalt-blue hoodie with the hood down, dark charcoal trousers, white sneakers. |

After the anchors in every clip, add this rule once:

```text
Every character has exactly two arms and two legs and small rounded hands with four fingers and a thumb (Bit has round mitten hands). Elbows and knees bend one way only and limbs never stretch. Every character wears one bright cyan band on the right wrist only.
```

Anchor rules:

- Use ASCII names in specs ("Khoa", "Tung", "Hai"), one spelling per character.
- Write each role so it reads correctly without the others ("a small white robot", not "Khoa's robot").
- Keep props out of the anchors; the laptop, the chip and the tablet go in `Props:` and in the `Hands` lines.
- The laptop is "a plain silver laptop with a blank lid": never a fruit, a letter or any mark on it.

## 4. Core rules this style overrides

Each entry names the rule by its ID in `core-contract.md`. The first two rows change the Style 1/2 catalog look, which is not a core rule.

| Core rule | Override | Reason |
|---|---|---|
| Catalog look (Styles 1–2): stick figures with plain or line faces | Chibi characters with outlined, softly shaded rounded bodies and simple dot-eye faces | The tech-explainer genre is built from these characters |
| Catalog look (Styles 1–2): one hero figure | A team of six named characters, each with a cast card; at most two in a clip in the sample (C12 still applies) | Team and helper stories |
| C3 (instruments only) | The frozen soft synth-pluck and marimba score in section 6 instead of piano and synth; the continuity sentence is kept | Bright product-explainer tone |
| C5 (adds limits) | Raised hands go out beside the head, never in front of the face; a hand never reaches the forehead; Bit holds and passes with its right hand only (section 7) | Big heads and short arms hide hands and faces |
| C9 (`none` → `post-overlay`) | Cards carry shapes and icons only; any titles or labels are added in post (sections 5 and 8) | Explainers need labels, and labels kept out of the art stay editable and translatable |
| C15 (motion cadence) | `smooth`, with clear holds | Small eased moves suit the clean product look |
| C16 (bans a move) | No orbit | An orbit turns the big heads past the shoulders and breaks the isometric angle |

## 5. Text, motion, camera

- **Text policy: `post-overlay`.** No words, letters, numbers or readable code anywhere: the code window is coloured bars, the flow card is nodes and arrows, the check is an icon. Titles, labels or captions are added in post (section 8), never in the spec.
- **Motion cadence: `smooth`.** Small eased moves with clear holds; UI cards pop in with a slight overshoot and settle; typing is a gentle alternate tap of both hands on the keys, never fast finger blur.
- **Camera.** Follow the camera grammar in `storyboard-template.md`; name the move at the start of every beat.
  - Transition moves: hold, slow push-in, slow pull back, slow lateral track, hard cut.
  - Keep the slightly-high three-quarter angle the whole video; it is part of the look.
  - Hold the camera during every pass and every thumbs-up; those are the risky moments for left and right hands.
  - Accents: at most one per video, a quick push-in on a card as it pops. No orbit: it turns the big heads past the shoulders and breaks the isometric angle.
  - The sample goes hold → push-in → hold, then hold → hold → pull back, then lateral track → hold → pull back.

## 6. Voice and score

The shared voice contract (`voice-continuity.md`) still applies. The sample uses this block verbatim in every clip:

```text
Voice: One off-screen adult female narrator throughout. General American accent, bright clear mid-range voice, light forward resonance, no raspiness or breathiness. Friendly, upbeat conversational delivery, restrained pitch variation, steady speaking pace, and close, dry studio sound. Keep the same vocal timbre, register, accent, pace, and recording quality throughout. Emotional progression belongs to the visuals and music; do not change the narrator's voice or switch to character dialogue.
```

Score, frozen. Clip 1 sets it:

```text
Audio: soft synth plucks and light marimba around 110 BPM; <SFX>; keep the voice dominant.
```

Clips 2–N:

```text
Audio: the same soft synth-pluck and light marimba theme continues from clip 1, same tempo (about 110 BPM) and instrumentation; <SFX>; keep the voice dominant.
```

SFX may change per clip (soft key taps, a gentle UI blip as a card pops, a bright chime on the check). Any change to the music itself is done in post.

## 7. Style bans and posture limits

Gating 133 pose track pairs (6 characters × 23 actions, minus 5 two-hand or hands-on-body actions Bit cannot do; the walk is a code cycle at a 55° three-quarter angle) as true 3D tracks plus the drawing camera's projection with `body_width` and `body_profile` found the habits below. The motion test was then checked by eye frame by frame for left and right hands. Put the matching phrase in the beat.

- **No hand to the forehead.** A chibi arm is shorter than the head is tall: a hand on the forehead (a facepalm, a salute) puts the forearm across the eyes. Use a hand on the cheek below the glasses, elbow out to the side.
- **Raised arms go out beside the head.** A cheer, a jump or a surprise raises the arms out to the sides first, then up beside the head, never straight up in front of the face. Ask for "arms up beside his head, clear of his face".
- **Hands in front of the body come in with the elbows out.** Crossed arms, a tablet held in front, a box carried in both hands: the elbows swing out first, so the upper arms never press flat across the chest.
- **Bit cannot hold anything with two hands, rest hands on hips or touch its chin.** Its arms are shorter than its body is wide. Bit holds and passes with its right hand only and waves with its left.
- **Seated knees point straight forward.** On a block, feet sit under the knees at hip width; knees splayed sideways read as broken legs in the three-quarter view.
- **The laptop lid hides typing hands.** Only the forearms show behind the lid; do not ask for visible fingers on the keys.
- **Passes happen in open space low and to the side.** A pass between Bit and a seated Khoa happens beside the laptop at knee height, never in front of either face; the chip never crosses Bit's visor.
- **A thumbs-up stays on its own side.** Khoa's right-hand thumbs-up is raised beside his right shoulder (screen left when he faces the camera), never across his chest or in front of his face.

Negatives, verbatim in every clip. They include the five shared posture negatives from `posture-gate.md`:

```text
Negative constraints: no logos, no brand marks, no fruit or letter on the laptop lid, no app mascots, no readable code, no letters, numbers or words on screens, cards or anywhere in the frame, no captions, no subtitles, no speech bubbles, no dialogue boxes, no watermark, no photorealistic people, no realistic textures, no hard cel-shaded shadow bands, no missing outlines, no dark or neon scenes, no extra fingers, no extra arms or legs, no duplicate characters, no unintended characters, no raised hand, arm or prop covering anyone's face, no cyan band on the left wrist, no changed proportions or colors between shots, no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no prop switching hands without a visible pass, no morphing.
```

## 8. Post-production

1. Trim each clip to its 10 s beats and cut hard between clips; clip 3 continues the same moment.
2. Check the risky frames before stitching: the chip pass, the thumbs-up, and each character's first frame for the cyan band on the RIGHT wrist and a blank laptop lid. Fix the rig or layer and re-render a clip if the band moves wrists or any mark appears on the lid or cards.
3. Check every UI card for letters or numbers. Fix the card layer and re-render; the cards must stay shapes only.
4. Normalise the stitched video to about -14 LUFS integrated, with the warning blip no more than 6 dB above the music bed.
5. Titles, card labels and subtitles, if wanted, are added after stitching (text policy `post-overlay`), on the white background beside the cards.

## 9. Hook override

Accent ignition and Reaction before cause suit this style: one small orange warning dot popping onto a calm white and blue scene, and a chibi face freezing, read at a glance. The sample uses Accent ignition (the orange warning dot pops onto the code card at about 1 s and Khoa stops typing and stares at it); the payoff is the green check in clip 3. A soft UI blip is the loudest the hit may be; no alarms or sirens.

## 10. Sample package and gates

- [samples/tech-illustration.md](samples/tech-illustration.md): 3 clips, "The missing chip", with 1, 2 and 2 characters on screen.
- `tools/package_lint/package_lint.py samples/tech-illustration.md`: PASS, 0 red, 0 yellow. [Facts block](samples/tech-illustration.facts.md). `hand_ledger.py`: PASS. `tests/verify-opening-hook.py`: passed.
- Posture gate: 133/133 pose track pairs PASS with 0 errors and 0 warnings, both as true 3D tracks and as the drawing camera's projection (front-view frames carry `body_width`, `body_profile` and `limb_width`). The first drafts failed or warned on: a facepalm (the forearm crossed the eyes; dropped for a cheek hand), raised arms folding past 150° in front view (fixed with an arms-out in-between key), arms pressed across the chest on holds (fixed with an elbows-out key and narrower torsos), knees splayed when seated, and Bit's short arms on two-hand holds (dropped for Bit).
- Motion test (`motion/motion.gif`, 42 frames): Khoa types, the warning card pops, Bit passes the chip from its right hand to Khoa's left hand with two frames of both hands on it, Khoa gives a right-hand thumbs-up, the check card pops. All four tracks (both characters, 3D and camera) and `--scene` PASS with 0 errors and 0 warnings. A first staging with Bit giving from its left hand failed (its arm crossed its body), and the chip held up by Khoa's shoulder covered Bit's visor; both were re-staged.

## 11. Catalog entry (ready to merge)

Style matrix row:

```text
| **tech-illustration** | Soft Tech Illustration | White and pale-blue 2.5D tech scenes with isometric blocks, floating UI cards and soft gradient shading | Software, AI and productivity explainers, app and SaaS stories, onboarding videos | Outlined chibi team about 2.5 heads tall plus a white robot sidekick, one cyan band on the RIGHT wrist |
```

Status row:

```text
| tech-illustration | gated | Posture gate and package lint (`style-research/tech-illustration/`) |
```

Setup gate line (offered only when the user asks for an experimental style):

```text
tech-illustration (gated, experimental): soft 2.5D tech-explainer look with a chibi software team and a robot sidekick.
```

## Files

- `sheets/model-<name>.png` (4 views, 10 expressions, palette), `cast-lineup.png`, `style-frame.png`
- `gallery/poses-<name>-v1.png`, `gallery/tracks/v1/` (3D and camera tracks), `gallery/gate-v1.json`
- `motion/motion.gif`, `motion/motion.mp4`, `motion/tracks/`, `motion/gate-motion.txt`
- `samples/tech-illustration.md`, `samples/tech-illustration.facts.md`
- `src/` rig (`rig.py`), drawing (`draw.py`, `scene.py`), cast, poses, tracks, gallery, sheets, motion
