# US Prime-Time Sitcom Animation (style pack, slug `us-sitcom`)

> In this repository: the sample package and its lint facts are `samples/us-sitcom.md` and `samples/us-sitcom.facts.md`. Other research files named below (gallery, tracks, gate output, renderer) stay in the project's `style-research/us-sitcom/` folder and are not part of the skill.

```text
Status: gated (2026-10-20). Covers: 3 clips, 3–5 characters on screen, a couch TV-remote handoff and a hand-to-hand
pass to a standing character, one living-room set, 16:9. Not covered: kitchen or car sets as full clips, 9:16,
crowds (6+), character dialogue.
```

Slug: `us-sitcom`. Evidence: posture gate on 54 pose tracks and a 5-character motion test ([README.md](README.md), `gallery/gate-v2.txt`, `motion-test/gate-v2.txt`); the sample package [samples/us-sitcom.md](samples/us-sitcom.md) passes `package_lint.py` with 0 red, 0 yellow ([facts block](samples/us-sitcom.facts.md)) and `hand_ledger.py`; `tests/verify-opening-hook.py` passes on it. The style audit of 2026-10-20 (`/mnt/project-files/style-audit/styles/us-sitcom.md`) and its fixes are in the README.

## 1. Signature checklist

### Sources

The look of the American prime-time animated family sitcom, from about 1990 to today. These works are named here as research only, never in prompts. Prompts never name them, and the cast copies none of their characters, skin colours, eye shapes, costumes or colour combinations.

Frame study (2026-10-20). I downloaded and looked at the seven stills below. The copies were kept out of the project folder. Each row says which of the five traits (section "Five signature traits", T1–T5) the frame confirms or contradicts. Four are from episodes: two Simpsons couch-gag frames, the Simpsons opening-sequence collage (one image stitched from many opening frames) and a first-season Bob's Burgers frame. The King of the Hill and Family Guy images are promotional group art, not frames.

| Work | Still (URL) | What it is | Confirms | Contradicts or does not show |
|---|---|---|---|---|
| *The Simpsons* (1989–) | https://static.simpsonswiki.com/images/a/a0/CouchGagS7E13.png | Episode frame, season 7 couch gag (Simpsons Wiki "Couch gag" page) | T1: one black outline of the same weight on people, couch, lamp, phone table and TV. T2: the couch faces the camera, the TV sits in the lower-right foreground, wide locked frame. T5: flat fills, no shading. T4: yellow skin, overbite and big touching eyes are this show's own look. | T3 not shown in a still. |
| *The Simpsons* | https://static.simpsonswiki.com/images/5/54/Circus_Line_couch_gag.png | Episode frame, the "circus line" couch gag | T1 and T5 on a crowded set (black outline on sets and props, flat colour). T2: the couch, rug and TV keep the same front-facing layout even in a gag. | The gag fills the set with spectacle; our pack never does. |
| *The Simpsons* | https://upload.wikimedia.org/wikipedia/en/c/ca/SimpsonsOpenComp2.png | Opening-sequence collage, 1989 and 2009 versions (Wikipedia) | T1 and T5 across outdoor sets in both eras. | Too small to read faces. Outdoor, not the couch stage. |
| *The Simpsons* | https://upload.wikimedia.org/wikipedia/en/c/ca/Simpsons_cast.png | Promotional cast art (Wikipedia) | T4: the trade dress the pack forbids (yellow skin, overbites, touching bulging eyes) is on almost every character. | No set. |
| *King of the Hill* (1997–2010) | https://upload.wikimedia.org/wikipedia/en/8/88/King_of_the_Hill.png | Promotional family art (Wikipedia) | Natural skin tones, separate small eyes, adult bodies at natural proportions. T1 and T5: one dark outline, flat fills. T3: flat lids and a straight mouth on the dad and the son, a deadpan look as the default face. | No set or staging. |
| *Bob's Burgers* (2011–) | https://upload.wikimedia.org/wikipedia/en/8/80/Bob%27s_Burgers_compare.jpg | Episode frame, first-season look (Wikipedia) | T5: flat fills. T3: five characters hold still and stare. T2 logic: a fixed set with the counter staged toward the camera, the family lined up facing it. Natural skin tones; separate oval eyes with dot pupils, like ours. | **T1 contradicted for sets:** the storefront behind is drawn with thinner, coloured lines, not the characters' black outline. See the T1 change below. T2: not a living-room couch. |
| *Family Guy* (1999–) | https://upload.wikimedia.org/wikipedia/en/1/1c/Griffin_family.png | Promotional family art (Wikipedia) | Natural skin tones, separate eyes, a black outline on the characters. | **T5 contradicted in the promo art:** soft shading on faces and clothes. This is promo rendering, not an episode frame, so T5 stands for frames but the negative stays. Cuts to a two-shot cannot be seen in a still. |

What these frames do not cover: motion (held beats, stepped timing and cuts are from memory of the shows, not checked), and King of the Hill or Family Guy episode sets. Attempts to fetch a Simpsons couch-gag GIF and more frames from Wikipedia and the Simpsons Fandom wiki were refused (rate limit, 403).

Changes made from the study:
- **T1:** the black outline is a `must` on characters and props only. Bob's Burgers draws its sets with thinner, coloured lines, so a same-weight set line is not universal in the genre. This pack keeps black same-weight set lines, as the Simpsons couch frame has, and says so as a choice. The frozen style block already asks for exactly that variant, so it and the package are unchanged.
- The Bob's Burgers row used to say our "separate oval eyes" differ from its eyes. The frame shows its eyes are separate ovals with dot pupils too, so that claim was wrong. The device is common to the genre; what we avoid is the other shows' faces and costumes, not oval eyes as such.

### Five signature traits

1. `must` One uniform black outline on characters and props, with flat cel fills and no shading. Sets: this pack also draws them with the same black outline (as in the Simpsons couch frame); a thinner, coloured set line (as in the Bob's Burgers frame) is also in the genre, but the pack does not mix the two.
2. `must` A locked-off, front-facing living-room stage: the couch faces the viewer like a TV set, people enter through a side doorway.
3. `bonus` A held deadpan beat: flat upper lids and a straight mouth, everyone still, one blink, the joke lands on the look.
4. `forbidden` Yellow skin, overbites, or huge bulging eyes that touch each other (one show's trade dress).
5. `forbidden` Shading, gradients, rim light or texture on characters or sets.

### Nearest neighbour

`modern-tv-cartoon`. Two differences a viewer can see in a still frame:

- Bodies: our adults are about 4.5 heads with natural proportions (pear-shaped dad, tall slim mom); modern-tv-cartoon uses big round heads on bean bodies with noodle limbs.
- Staging: our frame is a locked-off front-facing couch set held like a stage; modern-tv-cartoon moves through attics and yards with pans and push-ins, and plays big-eyed double-takes instead of deadpan holds.

### Prompt wording for each `must` trait

- Trait 1: "Every shape has one clean, uniform black outline of the same weight everywhere, on characters, props and backgrounds alike. Flat cel colors only: no shading, no gradients, no rim light, no texture."
- Trait 2: "a suburban living room with a blue three-seat couch facing the viewer … The camera is the TV: the couch faces straight at the viewer, a locked-off wide shot like a stage."

Both sentences sit inside the frozen style block below, repeated verbatim in every clip.

## 2. Frozen style block

```text
Style and environment: a flat 2D prime-time American animated sitcom look. Every shape has one clean, uniform black outline of the same weight everywhere, on characters, props and backgrounds alike. Flat cel colors only: no shading, no gradients, no rim light, no texture. Characters have natural human skin tones, simple oval eyes that sit apart with small black dot pupils, thick single-stroke eyebrows, and a nose shape of their own. Backgrounds are simple, slightly muted flat interiors with straight lines: a suburban living room with a blue three-seat couch facing the viewer, beige walls, a window with red curtains, a framed landscape picture, a yellow floor lamp and an open doorway on the right. The camera is the TV: the couch faces straight at the viewer, a locked-off wide shot like a stage. Animation is limited and deliberate: characters hold still between actions, and comedy lands on held deadpan looks.
```

After the character anchors, verbatim:

```text
Every character has exactly two arms, two legs and four-fingered cartoon hands; a moving limb replaces its previous pose. Limbs keep their length and bend smoothly at elbows and knees. Arms hang beside the body with a gap at the waist, never drawn over the chest. Each character wears their wrist marker on the right wrist only, in every shot. Expressions change only eyelids, eyebrows and mouth, never the face shape, hair, clothes or proportions.
```

## 3. Cast cards (verbatim anchors)

Each anchor below is copied from `src/rig.py` (`CAST[..]["anchor"]`) and appears word for word in every clip the character is in. A clip lists exactly who is in it (`Characters (exactly 5, no one else)`). **Every character wears one fixed marker on the right wrist**, so left and right read in any frame, including the front view, where a character's right hand is on the viewer's left.

- **Gary**: `Gary: a pear-shaped middle-aged dad with peach skin, a receding brown comb-over, a bushy brown mustache and a round nose, a short-sleeved white button-up shirt with a teal tie, khaki trousers, brown shoes, and a gold wristwatch on his right wrist.`
- **Denise**: `Denise: a tall, slim mom with tan skin and a rust-red chin-length bob with straight bangs, small gold hoop earrings, an open maroon cardigan over a mint-green top, dark blue jeans, navy flats, and a yellow hair tie worn on her right wrist.`
- **Kayla**: `Kayla: a lanky fifteen-year-old girl with light peach skin and a high black ponytail, a purple pullover hoodie with white drawstrings and a front pocket, black leggings, white sneakers, and a pink beaded bracelet on her right wrist.`
- **Benji**: `Benji: a short, round nine-year-old boy with brown skin, a backwards blue baseball cap over short black curls, a green-and-orange horizontally striped T-shirt, blue knee-length shorts, red sneakers, and a red sweatband on his right wrist.`
- **Grandpa Walt**: `Grandpa Walt: a stooped grandfather with pale rosy skin, a bald head with tufts of white hair above the ears, thick black-rimmed glasses and a long nose, an olive sweater vest over a white long-sleeved shirt, grey slacks, dark loafers, and a silver wristwatch on his right wrist.`
- **Ray**: `Ray: a tall, lanky next-door neighbor with deep brown skin, a short black flat-top haircut and a small goatee, an orange short-sleeved bowling shirt with a cream vertical panel, black trousers, black shoes, and a blue sweatband on his right wrist.`

Props are not part of anyone's anchor. They are named in the clip's `Props:` line with one noun each, used the same way everywhere: "TV remote", "coffee mug", "phone", "cereal box", "wooden cane" (Grandpa Walt's walking cane, held in his right hand in the sample).

## 4. Core rules this style overrides

| Core rule | Override | Reason |
|---|---|---|
| A perceptible visual change every two to three seconds (`storyboard-template.md`) | A beat may be "Everyone holds still for a beat", with at least one small motion (a blink, one click) | The held deadpan look is the genre's punchline. A held beat with a blink still reads as acted, not frozen. |
| Stick limbs with no thickness (Styles 1–4) | Limbs with thickness and colour segments: sleeve, then skin; trousers, then shoe | Coloured costumes are how six characters stay apart. Length still never changes. |
| Piano and ambient score | The frozen bass-and-brass sitcom theme below | Dry comedy needs a light, bouncy bed, not a reflective one |
| One hero figure | An ensemble of 6 named characters, at most 5 on screen | Family sitcom comedy is told by a group |
| Varied cinematic shots (Style 4) | One locked-off wide shot is the default; cuts to a medium two-shot are the only change of framing | The couch facing the viewer is the stage; moving cameras break the TV-set look |

## 5. Text, motion, camera

- **Text policy: `post-overlay`.** The generated video has no words, letters, numbers or logos on the TV, remote, cereal box, mug or signs. Titles or subtitles, if a video needs them, are added in post (section 8).
- **Motion cadence: `stepped`.** Limited animation: characters hold a pose, move to the next key pose, and hold again. The comedy lands on the holds.
- **Camera.** Follow the camera grammar in `storyboard-template.md`.
  - Default: hold, locked-off wide shot of the couch. Every beat names its camera move.
  - Transition moves allowed: hold, hard cut to a medium two-shot on the couch and hard cut back, slow push-in on a held deadpan.
  - Hold the camera while a hand passes the TV remote; cut before or after the pass, never during it.
  - Accents: none in the sample. At most one per video, and never a whip pan, shake or orbit: they break the stage.
  - The sample goes hold → hold → hold, then hold → cut to two-shot → cut back, then hold → hold → slow push-in.

## 6. Voice and score

The shared voice contract (`voice-continuity.md`) still applies: one off-screen narrator, no character dialogue. The sample uses this block verbatim in every clip:

```text
Voice: One off-screen adult male narrator throughout. General American accent, dry mid-range voice, relaxed and slightly amused, like a calm nature-documentary narrator describing a family. Steady pace, restrained pitch, close and dry studio sound. Keep the same vocal timbre, register, accent, pace and recording quality throughout. Emotional progression belongs to the visuals and music; do not change the narrator's voice or switch to character dialogue.
```

Score, frozen. Clip 1 sets it:

```text
light, bouncy sitcom bass-and-brass theme at low volume
```

Clips 2 and 3: "voiceover seamlessly continues the identical light, bouncy sitcom bass-and-brass theme from clip 1, same tempo and instrumentation". SFX may change per clip (plastic clicks, a carpet swish, cane taps, a single-note bass sting); the last clip may end the theme on a short brass button.

## 7. Style bans and posture limits

Negatives, verbatim in every clip. They include the five shared posture negatives from `posture-gate.md`:

```text
no 3D render, no CGI, no gradients or soft shading, no anime or manga eyes, no yellow skin, no overbites, no huge bulging eyes that touch each other, no wobbly line boil, no variable or tapered outlines, no extra arms or legs, no duplicate characters, no extra family members, no studio audience, no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no wrist marker on the left wrist, no prop switching hands without a visible pass, no visible text, letters, numbers or logos on the TV, the remote, the cereal box or anywhere else, no speech bubbles, no captions, no watermark.
```

Posture limits from the gate and from eye checks:

- Seated beats dominate (couch, kitchen table, car seat, recliner). Write what holds the body: "sits on the couch", "leans on the counter with her right forearm". In code-rendered references, gate these with `"supported": ["pelvis", "<seat>"]`, `"contacts"` for the hand on the counter, cushion or door frame, and `"ground_y"`; without `ground_y` a reclined character can sink through the floor and still pass.
- Front-view couch: a character's right hand is on the viewer's left. Hand-offs along the couch go between the two **near** hands (the sitter on the left passes with their left hand to the right hand of the sitter on their left). The sample states this in the Composition line and names both hands in the pass sentence.
- Arms over the body: in front view, keep shoulders at the torso edge and a gap between the arms and the waist. On the couch the hands rest on the cushion beside the thighs, elbows a little out, not on the knees (arms down the torso edge read as fused when the sleeve matches the top). Shrugs keep the elbows low beside the waist with forearms opening outward; raised elbows read as flexing.
- Profile, hand at the head: a phone at the ear in profile puts the forearm across the face and hides the hand. Write "holds the phone upright in front of her chin" (speaker call) instead, with the other arm hanging. A mug at the lips sits ahead of the hand so the fingers stay visible; the other arm hangs and never crosses the chest.
- Hand sentences: one character per sentence, the first sentence of a beat carries no hand, name the holder and the hand in the same sentence, one noun per prop ("TV remote" everywhere, including the final frame). Avoid prop names that hide inside common words in other sentences.
- A character who has a `Hands at start` line is in the First frame; beats then give them an action, not "appears".

## 8. Post-production

1. Trim each clip to its 10 s beats and cut hard between clips.
2. Check the risky frames before stitching: the TV-remote pass in clip 2 and clip 3, and each character's first frame for the RIGHT-wrist marker. Re-generate a clip if a marker moves to the other wrist or the remote changes hands without a visible pass.
3. Check that the TV, remote and cereal box carry no lettering; re-generate if they do (do not blur in post).
4. Normalise the stitched video to about -14 LUFS integrated, with the hook hit (a plastic click and a carpet swish) no more than 6 dB above the music bed.
5. Add any title card or subtitles after stitching. Never ask for them in the prompt.

## 9. Hook override

Sudden entry, Reaction before cause and Before → after cut suit this style. The sample uses Sudden entry (at 1.2 s Benji slides in on his knees and stares up at the remote while Gary keeps clicking with a blank face). As `opening-hook.md` says for dry comedy, the held deadpan look is the hit: a plastic click plus a carpet swish is the loudest it may be, within the loudness limit above. No impact booms or record scratches.

## 10. Sample package and gates

- [samples/us-sitcom.md](samples/us-sitcom.md): 3 clips, "The remote", with 3, 5 and 4 characters on screen.
- `tools/package_lint/package_lint.py package.md --facts samples/us-sitcom.facts.md`: PASS, 0 red, 0 yellow. [Facts block](samples/us-sitcom.facts.md).
- `hand_ledger.py`: PASS. Nine mutation tests catch 8; the 9th is a WARN by design ([ledger-tests.md](prompt-package/ledger-tests.md)).
- Posture gate: 54/54 pose tracks PASS with 0 warnings. 5/5 motion tracks and the 5-track `--scene` run PASS ([README.md](README.md)).

## 11. Catalog entry (ready to merge)

Style matrix row:

```text
| **us-sitcom** | US Prime-Time Sitcom | Flat cel fills, one uniform black outline on everything, a locked-off front-facing living-room stage, no shading | Dry comedy about everyday life, family and office dynamics, "who really decides" stories | A family-and-neighbour ensemble with natural skin tones, separate oval eyes and distinct silhouettes, one RIGHT-wrist marker per character |
```

Status row:

```text
| us-sitcom | gated | Posture gate and package lint (`style-research/us-sitcom/`) |
```

Setup gate line (offered only when the user asks for an experimental style):

```text
us-sitcom (gated, experimental): American prime-time animated sitcom look with a family ensemble on a couch stage.
```
