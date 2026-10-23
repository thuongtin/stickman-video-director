# POV Story Series (style pack)

> In this repository: the sample package and its lint facts are `samples/pov-story.md` and `samples/pov-story.facts.md`; the README preview is `docs/style-previews/pov-story.gif`. Other research files named below (renderer, sheets, tracks, gate output, frame study) stay in the project's `style-research/pov-story/` folder and are not part of the skill.

```text
Status: gated (2026-10-23). Covers: 3 clips, 9:16, 1–2 characters on screen, a photo handoff across a counter, a parcel held in both hands, character dialogue with three speakers, caption box and word-by-word subtitles as code overlays, a "Part 2" cliffhanger.
Not covered: 16:9, Priya, Mrs. Oakley and Theo in a package, 3+ characters in one clip, sitting, running, outdoor sets, night scenes.
```

Slug: `pov-story`. Evidence: posture gate on 48 pose tracks (6 characters × 8 poses) and a three-shot 9:16 motion test (5 tracks, two of them two-character shots checked with `--scene`), all 0 errors and 0 warnings (`gallery/tracks/`, `motion/tracks/`); the sample package [samples/pov-story.md](samples/pov-story.md) passes `package_lint.py` and `hand_ledger.py` ([facts block](samples/pov-story.facts.md)); `tests/verify-opening-hook.py` passes on it.

Short vertical drama told as a series: a white caption box at the top states the premise in the second person ("POV: ...") and the part number, cartoon characters with big round white heads and thin stick limbs act it out in flat everyday sets, every spoken word appears as a bold subtitle that lights up word by word, and each part ends on a twist that sends the viewer to the next part. The acting is in the eyes: heavy half-closed lids, slow side-eyes and deadpan stares at the camera. All characters are original; specs name no account, creator, platform or work.

## 1. Signature checklist

### Sources

These works are named here as research only. Specs never name them, and the cast copies none of their characters, captions, stories or layouts. Frames studied on 2026-10-23 (YouTube thumbnails and auto-frames, `i.ytimg.com/vi/<id>/{hqdefault,hq1,hq2,hq3}.jpg`); local copies in `research/frame-study.jpg`.

| Work | Images looked at | Confirms | Contradicts, and what changed |
|---|---|---|---|
| The owner's reference screenshot (a short-video animation account's post, shared in the project, 2026-10-23) | The screenshot itself: one full 9:16 frame and eight thumbnails of the same series | Trait 1: big round white heads with coloured hair shapes, thin-outlined eyes with a lid line and small pupils, solid black stick limbs, simple A-line clothes. Trait 2: a white rounded caption box at the top with a "POV: ..." premise and "Part N". Trait 3: bold capital subtitles in the middle with the current word highlighted. Trait 4: flat everyday sets (an office counter, an apartment door, a store) in pastel wall colours. Trait 5: the half-lidded, unimpressed looks. Multi-part numbering on every thumbnail. | The reference cast (a red-haired clerk with a lanyard, a ginger woman in a mustard dress) and its captions are that account's own; this cast avoids red buns, ginger hair, lanyards, shoulder bags and mustard, and the stories are new. |
| "POV: Your Landlord Was Old Money — He Taught You 6 Rules" (Wealth Decisions, YouTube 8EyEHV2IpLw) | https://i.ytimg.com/vi/8EyEHV2IpLw/hqdefault.jpg ; hq1, hq2, hq3 | Trait 3: bold subtitle words with one word in yellow, set low in the frame. The second-person "POV:" premise as the title of a short story. | Painterly, shaded illustration with realistic proportions, not flat cartoon heads. Kept only the caption grammar; the flat look comes from the reference. |
| "POV You Look Like You're Still Renting — You're the Landlord" (Rental Life POV, YouTube BFAwomH_jYk) | https://i.ytimg.com/vi/BFAwomH_jYk/hqdefault.jpg ; hq1, hq2, hq3 | The genre's settings: apartment doors, a driveway, a kitchen table; one lead in the same clothes in every frame. | Same painterly rendering and a horizontal frame. This pack keeps the vertical frame and the flat fills. |
| "My Best Friend Kept A Huge Secret From Me" (storybooth, YouTube CHfj6DDzymI) | https://i.ytimg.com/vi/CHfj6DDzymI/hqdefault.jpg ; hq1, hq2, hq3 | Trait 1 and 5: flat 2D figures with simple outlines, a palms-up shrug, a sideways unimpressed look, plain flat backgrounds behind a speaking character. | Skin-coloured faces and full hands, 16:9. The white heads and stick hands stay the reference's. |
| "My Best Friend Found Out I'm A Girl" (MSA, YouTube 1sPxtNejKLE) | https://i.ytimg.com/vi/1sPxtNejKLE/hqdefault.jpg ; hq1, hq2, hq3 | Subtitles of the spoken line along the bottom of every frame; a door-opening reveal as a story beat (hq3). | Anime-like shaded drawing. Not used for the look. |

What was looked at: the reference screenshot and sixteen still frames from four videos, at thumbnail size, on 2026-10-23. Stills show design, captions and staging, not timing; the motion grammar (limited animation, held poses, lip flaps, one punch-in per part) is this pack's choice, checked in the code-rendered motion test.

Changes made because of the frames: the caption box stays white with black text; the faces keep white heads (the reference) while the lids and side-eyes come from the reference and storybooth; nothing painterly. After the owner's review on 2026-10-23 ("make it truly look like the original") the drawing was rebuilt by rendering a counter two-shot framed like the reference frame and comparing them side by side over nine rounds: the eyes became thin-outlined white ovals with a straight lid line and a small pupil (the first version's big pupils read as sunglasses); the head grew to about a fifth of the height and the body shortened; arms and legs became solid black and thicker; garments became soft A-line or boxy shapes with rounded shoulders and one soft shade side; hair became flat colour with no strand lines; sets lost their black outlines; the subtitle highlight became a purple box behind the current word with a soft shadow on white capitals, as in the reference, instead of a yellow word.

### Five signature traits

| Tag | Trait (visible in a still) |
|---|---|
| `must` | Big round white heads with no nose and a bold outline, flat coloured hair shapes, thin-outlined white oval eyes cut by a straight lid line with a small black pupil tucked under it, thin brow arcs, solid black stick arms and legs with small splayed black hands, soft A-line or boxy clothes with one soft shade side, black flat shoes |
| `must` | A vertical 9:16 frame with a white rounded caption box near the top: the second-person premise line and the part number (added in post) |
| `must` | Heavy white capital subtitles of the spoken line in the middle-low band with a soft dark shadow, the word being said on a purple box (added in post) |
| `bonus` | Flat pastel everyday sets with thin slate lines only on furniture and no black outlines: a hallway with plain panel doors, a mailroom counter, a kitchen; a slow push-in on a two-shot and one punch-in on a reaction |
| `forbidden` | Gradients, textures or modelled shading on characters, skin-coloured faces, noses, realistic hands, any text drawn in the art (signs, labels, phone screens), any account name or watermark |

### Nearest neighbour

Catalog: **youtube-storytime** (a first-person storytime cartoon with a narrator cutaway). Two visible differences:

1. Storytime characters have skin-coloured faces with full outlines and the frame is 16:9; here the heads are plain white, limbs are black sticks, and the frame is 9:16 with a caption box on top.
2. Storytime is told by a narrator over the scenes; here the characters speak their own lines, every line is shown as a word-by-word subtitle, and each part ends on a cliffhanger.

Second neighbours: **Style 2** (the white-headed stick lead) and **Style 5** (historical cartoon). They share the white round head, but Style 2 has dot eyes with no lids and one hero, Style 5 is cel-shaded with solid black oval eyes; this style is flat, lidded and built around a series format. **us-sitcom** is a 16:9 couch sitcom with skin-coloured heads.

### Spec wording for each `must` trait

The frozen style block below says each one in plain words. The caption and subtitles are post-production overlays, so the spec asks for clean space for them, never for the text itself.

## 2. Frozen style block

Repeat it verbatim in every clip. The set goes on a separate `Setting:` line, which may change between clips.

```text
Style: a flat 2D cartoon for a vertical short drama series. Characters have big round plain white heads with no nose and a bold black outline, about a fifth of their height, with flat coloured hair shapes. Eyes are two close-set white ovals with thin outlines, each cut by a straight eyelid line that drops for deadpan and side-eye looks, with a small black pupil tucked under the lid; thin arched eyebrows and small simple mouths. Bodies are short, soft A-line or boxy clothing shapes with rounded shoulders, a flat fill and one slightly darker side, on solid black stick arms and legs, with small splayed black hands and black flat shoes. No gradients or texture. Sets are flat pastel everyday interiors with no black outlines and few details. Limited animation: characters hold clear poses, mouths flap on their lines, eyes blink and slide sideways, and gestures are small and quick. Vertical 9:16 framing from the knees up, with clean wall space in the top fifth for a caption box and clean space across the middle-low band for subtitles; nobody's face sits in those bands.
```

## 3. Cast cards (verbatim anchors)

Six original characters for apartment-building stories. They differ first by silhouette (hair shape, height, skirt or trousers), then by one dominant colour. Sheet: `sheets/cast-sheet.png` (front, three-quarter and side per character, ten expressions, 48 gated poses); lineup: `sheets/cast-lineup.jpg`.

| Character | Role | Anchor |
|---|---|---|
| Jess | the POV lead ("you" in the caption) | Jess: a young woman with a big round plain white head, wavy dark-brown hair past her shoulders with a side-swept fringe, a lavender A-line dress to above the knee, black stick legs and black flats. |
| Marcus | building manager | Marcus: a tall man with a big round plain white head, short black curly hair and a short black boxed beard along his jaw, a navy polo shirt with a small white collar, khaki trousers and black shoes. |
| Priya | next-door neighbour | Priya: a young woman with a big round plain white head, long black hair in one thick braid hanging over her right shoulder, a coral blouse, a teal knee-length skirt, black stick legs and black flats. |
| Derek | neighbour across the hall | Derek: a tall young man with a big round plain white head, blond hair swept up into a tall quiff, a maroon bomber jacket over a white t-shirt, black trousers and white sneakers. |
| Mrs. Oakley | landlady | Mrs. Oakley: an older woman with a big round plain white head, short silver curls like a small cloud, small round brown-framed glasses, a green cardigan over a cream blouse, a long brown skirt, black stick legs and black shoes. |
| Theo | Jess's little brother, nine | Theo: a small boy about three quarters of Jess's height with a big round plain white head, messy spiky brown hair, a yellow t-shirt with one blue stripe across the chest, blue shorts, black stick legs and red sneakers. |

After the anchors in every clip, add this rule once:

```text
Every character has exactly two solid black stick arms and two solid black stick legs, and small black hands with four short splayed fingers. Elbows and knees bend one way only and limbs never stretch. Heads stay plain white circles with no nose and no skin colour.
```

Anchor rules:

- ASCII names in specs ("Jess", "Mrs. Oakley"), one spelling per character; the caption's "you" is Jess.
- Write each role so it reads without the others ("a tall man", not "Jess's manager").
- Props stay out of the anchors; the phone, the photo and the parcel go in `Props:` and the `Hands` lines.
- The phone screen shows one plain parcel icon at most, never words or numbers; the photo is a grey camera still of shapes.

## 4. Core rules this style overrides

| Core rule | Override | Reason |
|---|---|---|
| Catalog look (Styles 1–2): stick figures with plain or line faces, one hero | White-headed cartoon cast with lidded eyes and coloured hair, six named characters; at most two on screen in the sample (C12 still applies) | The genre is an ensemble drama acted with the eyes |
| C13 (scene changes) | Clips may change set when the spec names the time cut in its `Hands at start (time cut)` line and the stitching guide | A part moves through a building (door, mailroom, hallway) |
| C14 (arc) | Premise → escalation → twist, ending on an open cliffhanger for the next part; the discussion prompt goes in the post caption, not the video | The series format: each part pays off its own hook and opens the next |
| C3 (instruments only) | The frozen light pizzicato and soft synth-pad bed in section 6; the continuity sentence is kept | Light, tense comedy-drama tone under dialogue |
| C9 (`none` → `post-overlay`) | The caption box, the part tag and the subtitles are added in post by code; the art keeps clean bands for them (section 5) | They are the format's signature and must stay exact and editable |
| C15 (motion cadence) | `stepped`, with long holds, lip flaps and eye moves | Limited animation is part of the look |
| C16 (bans a move) | No orbit and no whip pan | They break the flat front-on staging and the caption band |

## 5. Text, motion, camera

- **Text policy: `post-overlay`.** No words, letters or numbers in the art: plain doors, blank lockers, a parcel icon on the phone. The caption box ("POV: <premise>" on one or two lines, then "Part N"), the closing "Part N+1" tag and the subtitles are drawn by code after the scene, in the bands the style block keeps clean: caption box in the top fifth, subtitles across the middle-low band, part tag near the bottom edge above the platform bar. The overlay text is listed in the sample's continuity block, never in a spec.
- **Subtitles:** heavy white capitals with a soft dark shadow, at most two lines of about 250 px at 360 px width, set at about 70% of the frame height; the word being said sits on a purple box; the line stays on screen about one second after the speaker stops.
- **Motion cadence: `stepped`.** Hold poses; animate mouths (open, mid, closed on a short loop), blinks, pupil slides and one small gesture per beat; a pass is eased over about one second.
- **Camera.** Follow the camera grammar in `storyboard-template.md`; name the move at the start of every beat.
  - Base framing: from the knees up, feet near the bottom edge, faces in the upper-middle band.
  - Transition moves: hold, slow push-in, hard cut. Cut between shots on a held face.
  - Hold the camera during every pass.
  - Accent: at most one per part, a quick punch-in on a reaction face after a reveal. No orbit, no whip pan.

## 6. Voice and score

Dialogue is approved for this style, using the approved multi-speaker path of `voice-continuity.md` (C2 is not overridden: every voice profile is complete and repeated verbatim; lint B5 compares each speaker separately). There is no narrator. Each speaker has one frozen line, repeated verbatim in every clip where they speak, and a speaker who does not speak in a clip is left out:

```text
Voice — Jess: adult female, General American accent, clear mid-range voice, light forward resonance, dry and slightly sarcastic conversational delivery, restrained pitch variation, steady pace, close, dry studio sound; keep the same timbre, register, accent and recording quality in every clip.
Voice — Marcus: adult male, General American accent, warm low baritone, gentle chest resonance, calm, unhurried and a little weary delivery, restrained pitch variation, steady pace, close, dry studio sound; keep the same timbre, register, accent and recording quality in every clip.
Voice — Derek: adult male, General American accent, bright light tenor, smooth and overly friendly delivery, restrained pitch variation, steady pace, close, dry studio sound; keep the same timbre, register, accent and recording quality in every clip.
```

Lines for Priya, Mrs. Oakley and Theo are frozen the same way the first time they speak.

Score, frozen. Clip 1 sets it:

```text
Audio: light pizzicato strings and a soft synth pad around 96 BPM, low under the dialogue; <SFX>; keep the dialogue dominant.
```

Clips 2–N:

```text
Audio: the same light pizzicato and soft synth-pad bed continues from clip 1, same tempo (about 96 BPM) and instrumentation; <SFX>; keep the dialogue dominant.
```

SFX per clip: a phone buzz, a door latch, a soft whoosh on the punch-in, a low string sting on the cliffhanger.

## 7. Style bans and posture limits

Gating 48 pose tracks (each of six characters in stand, wave, shrug, phone, carry parcel, point, walk, explain) and the motion tracks with `body_width`, `body_profile`, `limb_width` and `head_radius` found the habits below. Put the matching phrase in the beat.

- **Phones and photos stay at chest height on their own side.** The head is wider than the shoulders: a phone raised to the face puts the forearm across the eyes. Ask for "holds the phone in front of her chest with her right hand, elbow out to her right side".
- **Raised hands go out beside the head.** A wave goes up beside the head on its own side, never across the face.
- **A shrug opens out to the sides.** Elbows low and out, forearms up and outward, palms up beside the hips, never in front of the chest.
- **Two-hand holds keep the elbows out.** A parcel is held at the waist with one hand on each side of it, elbows bowed out past the body.
- **Passes happen in profile across open space.** The giver faces right and gives with the near (right) hand, the receiver faces left and takes with the near (left) hand, at chest height, below both faces, with the camera held. Heads stay at least a head-width apart.
- **A reaction is a face, not an arm.** Shock, side-eye and deadpan come from lids, pupils and mouth; keep hands down so they never cross the face.
- **Behind a counter only the upper body shows.** The legs still stand; never ask for a character sitting on nothing.

Negatives, verbatim in every clip. They include the five shared posture negatives from `posture-gate.md`:

```text
Negative constraints: no logos, no brand marks, no watermark, no account names, no letters, numbers or words anywhere in the art, no writing on signs, doors, lockers, parcels or phone screens, no captions or subtitles drawn into the scene, no speech bubbles, no skin-coloured faces, no noses, no realistic hands, no gradients, no textures, no photorealistic people, no faces inside the top caption band or the subtitle band, no extra fingers, no extra arms or legs, no duplicate characters, no unintended characters, no raised hand, arm or prop covering anyone's face, no changed proportions or colors between shots, no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no prop switching hands without a visible pass, no morphing.
```

## 8. Post-production

1. Trim each clip to its beats and cut hard between clips on a held face.
2. Check the risky frames before stitching: the pass (giver's near hand to receiver's near hand), each character's first frame for hair, clothes and the plain white head, and every frame for drawn text.
3. Add the overlay layer by code: the caption box from the first frame to the last, subtitles word by word on the dialogue timing, the "Part N+1" tag over the final second.
4. Normalise to about -14 LUFS integrated, dialogue on top, the music bed about 14 dB under it.
5. Post the parts in order; the next part's caption repeats the premise line with the new part number.

## 9. Hook override

Reaction before cause suits this style: the first frame shows the lead frozen and staring at something off-frame; the cause lands at about 1 s (a buzz, a door, an object that is not there). The sample uses it: Jess stares at her empty doormat, and at about 1 s her phone buzzes with a delivered-parcel icon. The open loop (who takes the parcels) is paid off in clip 3, and the twist there (Derek is holding her parcel) is the series hook for Part 2.

## 10. Sample package and gates

- [samples/pov-story.md](samples/pov-story.md): 3 clips, 9:16, "Part 1" of a parcel story, with 1, 2 and 2 characters on screen.
- `tools/package_lint/package_lint.py samples/pov-story.md`: PASS, 0 red, 0 yellow. [Facts block](samples/pov-story.facts.md). `hand_ledger.py`: PASS. `tests/verify-opening-hook.py`: passed.
- Turnaround view check (`posture-gate.md`): one sheet per character (head and full figure in front, three-quarter both ways and side both ways) reviewed by eye. Fixed from it: Marcus's beard ran up onto the cheek and mouth in profile (now sideburn, jaw, under the mouth); Priya's braid showed behind the head when facing left, where her right shoulder is the far side; Mrs. Oakley's glasses had no far lens in profile and the arm ran past the head; part lines crossed the hair outline in profile; a hair tail stuck out under Mrs. Oakley's nape; Derek's quiff had a second point at the back of the head.
- Posture gate: 48/48 pose tracks PASS with 0 errors and 0 warnings (front-view frames carry `body_width`, `body_profile`, `limb_width`, `hand_length` and `head_radius`).
- Motion test (`motion/motion.mp4`, 9:16, 204 frames at 12 fps): Jess's phone buzz; Marcus passes the camera still from his right hand to Jess's left hand across the counter with six frames of both hands on it; the door across the hall opens on Derek holding the parcel in both hands. All five tracks PASS, and `--scene` PASSES for both two-character shots, 0 errors and 0 warnings.

## 11. Catalog entry (ready to merge)

Style matrix row:

```text
| `pov-story` | POV Story Series | Flat 2D vertical drama: white round heads with lidded eyes, stick limbs, pastel everyday sets, a POV caption box and word-by-word subtitles added in post | Short multi-part drama series about everyday conflicts (neighbours, landlords, coworkers, family) told as "POV: you ..." | Six original characters with plain white heads and coloured hair; character dialogue; 9:16 only |
```

Status row:

```text
| pov-story | gated | `styles/pov-story.md`, sample `styles/samples/pov-story.md` with lint facts |
```

Setup gate line (offered only when the user asks for an experimental style):

```text
pov-story (gated, experimental): vertical POV drama series with white-headed cartoon characters, caption box and subtitles.
```

## Files

- `sheets/cast-sheet.png`, `sheets/cast-lineup.jpg`
- `gallery/tracks/` (48 pose tracks)
- `motion/motion.mp4`, `motion/motion.gif`, `motion/tracks/`, `motion-keyframes.png`
- `research/frame-study.jpg`
- `src/` drawing (`draw.py`), sets and overlays (`scenes.py`), IK and track export (`posing.py`), `sheet.py`, `motion.py`
