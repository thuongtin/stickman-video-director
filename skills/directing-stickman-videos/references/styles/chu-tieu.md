# Chú Tiểu Little Monks (draft style pack, slug `chu-tieu`)

> In this repository: the sample package and its lint facts are `samples/chu-tieu.md` and `samples/chu-tieu.facts.md`. Other research files named below (gallery, tracks, gate output, renderer) stay in the project's `style-research/chu-tieu/` folder and are not part of the skill.

```text
Status: gated (2026-10-20). Covers: 3 clips in 16:9, up to four characters plus the temple cat, one temple yard
in morning light, a broom pass and a two-handed tea-cup offering, joined palms, bows, seated meditation,
walking meditation and the full prostration (lạy), 44 human poses and 4 cat poses through the posture gate.
Not covered: 9:16, indoor shrine scenes, night, crowds, dialogue between characters, Vietnamese narration.
Not tried on Flow.
```

Draft for the skill's `references/` folder, named by slug. Every claim below about how Omni Flash behaves is a prompt design choice, not an observed result.

Use it for short, gentle life lessons on mindfulness, kindness and simple living (a page like "Thân Tâm Tuệ"): one small everyday moment in a temple yard, a quiet turn, one question for the viewer.

## Signature checklist

### Sources

1. **Thích Nhất Hạnh, "The Mountain Cliff Robe" (letter, plumvillage.org).** It supports the role colours: grey for a novice (compared to incense smoke or mist) and the long brown áo tràng for monks and nuns. It runs out quickly: it is a teaching story, not a dress code, it has no pictures, and dress varies between temples.
2. **Longquan Monastery's Xian'er (the temple's 2013 cartoon novice, and the 2016 robot made from it, as reported by Reuters and Engadget).** It shows that a temple itself uses a big-headed, shaved-head chibi novice for gentle teaching, without mocking monastic life. It runs out because I read news reports about it, not the comics. Its design is not copied: no yellow robe, no chest screen, no likeness.
3. **Chibi drawing guides (for example FPT Shop, "Hình chibi cute dễ vẽ").** They support the proportions: the head is close to half the body, short rounded limbs, a simple but expressive face, soft round lines. They have no temple or Buddhist content.

What the sources do not cover: I found no published survey of Vietnamese chú tiểu illustration, so the "minimal, pastel, quiet" look follows the brief ("bình yên, tối giản"), not a studied canon.

### Five signature traits

1. `must`: **Chibi temple figures.** Novices are about two and a half heads tall and adults about three to three and a half. Shaved heads (or a hood or bun), dot eyes, tiny mouth, soft pink cheeks.
2. `must`: **Flat pastel fills under one thin, even, warm brown-grey outline.** No gradients, no shading, no texture, no black ink line.
3. `must`: **A mostly empty frame.** One pale ground line and at most three set pieces (the plain corner of a tiled roof, one bare branch, a pale sun or a cushion). At least half of every frame stays quiet.
4. `bonus`: **Temple-role colour code and the right-wrist bead bracelet.** Novice grey, monastic brown, light-tan hood for the novice nun, blue-grey áo lam for lay visitors, and a dark wooden bead bracelet on every person's right wrist.
5. `forbidden`: **Sacred images, writing and manga marks.** No Buddha or bodhisattva figure, statue, altar or incense. No script, signs or Chinese characters. No sparkle eyes, sweat drops or anger veins.

### Nearest neighbour

**`chibi-anime`** (research) uses the same chibi proportions. Two visible differences:
- **Rendering:** chibi-anime uses cel shading with a shadow tone and a thick dark outline. Chú tiểu uses flat fills with no shadow and a thin warm-grey line.
- **Emotion and scene:** chibi-anime shows emotion with anime marks (sparkle eyes, sweat drops, storm clouds) in busy, furnished rooms. Chú tiểu moves only the eyes, brows, mouth and cheeks, in a near-empty yard.

### Prompt wording for the `must` traits

The style block, body rule and negative below are frozen. Paste them verbatim in every clip.

## Respect

The subject is monastic life, so the gentleness is part of the style, not decoration.

- **Sacred figures:**
  - Never make the Buddha, a bodhisattva or a sacred image a character, a joke or an animated figure.
  - By default keep statues and altars out of frame entirely; the negative carries `no Buddha statue, no altar, no incense`.
  - If a story needs the shrine hall, show it from outside or as a soft blurred shape that never moves.
- **Humour:**
  - Monks and nuns are never the butt of a joke about their vows. The humour is about being human (impatience, sleepiness, curiosity), and the lesson is kind.
  - No meat, alcohol, money-grabbing or romance gags around monastic characters.
- **Offerings:** lay visitors offer with two hands; monastics receive calmly.
- **Rituals** are shown correctly and briefly:
  - joined palms (chắp tay búp sen: palms together, fingers up, a little hollow between them);
  - a bow from the hips;
  - the prostration (lạy), see Posture limits;
  - walking meditation with the hands folded at the belly.
  - Do not invent mudras or chants.
- **Original characters only.** Do not copy a known artist's chú tiểu designs, the Longquan Monastery's Xian'er, or Ikkyū-san. These names stay in this pack and never go into a prompt.

## Shared prompt blocks (frozen)

Style and environment (verbatim in every clip):

> a calm, minimal 2D chibi illustration in a soft picture-book style. Flat pastel colors with no gradients and no texture: warm rice-paper cream background, soft grey, monastic brown, light tan, blue-grey and one gentle sage green, with a single soft pink accent. Every shape has one thin, even, warm brown-grey outline. Lots of empty space: a quiet temple yard with one pale ground line, the plain curved corner of a tiled roof at the upper left, one bare branch with a few leaves at the upper right and a pale morning sun. Few elements, no clutter, no crowds, no statues, no altar, no signs.

Body rule, pasted right after the anchors. It has two frozen versions; use the first when Mướp is on screen and the second when the cat is not in the clip.

> Every person has exactly two arms and two legs and the cat exactly four legs; a moving limb replaces its previous pose. Limbs keep their length and bend smoothly at elbows and knees. Faces are simple: dot eyes, small brows, a tiny mouth and soft pink cheeks; expressions change only the eyes, brows, mouth and cheeks, never the head shape, headwear, robe or proportions. Movements are slow and gentle; humor stays quiet.

> Every person has exactly two arms and two legs; a moving limb replaces its previous pose. Limbs keep their length and bend smoothly at elbows and knees. Faces are simple: dot eyes, small brows, a tiny mouth and soft pink cheeks; expressions change only the eyes, brows, mouth and cheeks, never the head shape, headwear, robe or proportions. Movements are slow and gentle; humor stays quiet.

Negative (verbatim):

> no 3D render, no CGI, no gradients, no shading or soft airbrush, no glossy look, no paper or canvas texture, no detailed backgrounds, no crowds, no anime sparkle eyes, no manga symbols, no sweat drops, no anger veins, no slapstick falls, no realistic anatomy, no extra arms or legs, no duplicate characters, no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no bead bracelet on the left wrist, no prop switching hands without a visible pass, no Buddha statue, no altar, no incense, no visible text, letters, numbers, Chinese characters or scripture writing, no signs or banners, no speech bubbles, no dialogue boxes, no logos, no watermark.

Music (frozen score): a slow, sparse bamboo flute melody over a soft low drone, with at most one temple-bell tone per clip and no beat drops. Clip 1 sets it; later clips say the identical score continues with the same tempo and instrumentation.

Voice: the narrator is chosen per video and follows the shared voice contract (`voice-continuity.md`); this style does not fix the voice, accent or language. The sample package casts a calm adult male narrator with a gentle Vietnamese accent speaking English. A Vietnamese-narrated video freezes its own Voice paragraph the same way.

## Character anchors and cast cards (frozen, pasted from `src/rig.py` and `src/cat.py`)

- **Bracelet marker:** every human character wears a dark wooden bead bracelet on the right wrist and on no other wrist. It is the fixed left/right marker.
- **Each clip:** lists exactly who is in it ("Characters (exactly 3, no one else)") and repeats each visible character's anchor word for word, as `Name: anchor.`
- **Anchors hold design only:** pose, position and props stay out of them.

- **An:** the youngest novice, a tiny round chibi boy about two and a half heads tall with a big round freshly shaved head, one small dark leaf-shaped tuft of hair at the front of the crown, dot eyes and soft pink cheeks, a plain light-grey knee-length monk's tunic with a crossed collar over light-grey trousers, a dark wooden bead bracelet on his right wrist, small bare feet
- **Hỷ:** a plump round chibi novice about two and a half heads tall with a big round shaved head and no hair at all, a wide round belly, crescent smiling eyes and pink cheeks, a plain light-grey knee-length monk's tunic with a crossed collar over light-grey trousers, a dark wooden bead bracelet on his right wrist, small bare feet
- **Tịnh:** a small chibi novice nun about two and a half heads tall with a soft light-brown cloth hood (mũ ni) that covers her head and ears and falls to her shoulders, leaving only her round face showing, dot eyes and pink cheeks, a long light-brown robe to the ankles with wide sleeves, a small brown cloth bag hanging from her left shoulder to her right hip, a dark wooden bead bracelet on her right wrist
- **Thầy Từ:** an old monk teacher about three and a half heads tall, slim and slightly stooped, with a round shaved head, long soft white eyebrows that droop at the ends, calm narrow smiling eyes and faint smile lines, a long plain brown robe (áo tràng) to the ankles with wide sleeves, a dark wooden bead bracelet on his right wrist, simple brown sandals
- **Bà Sáu:** a small kind grandmother about three heads tall with neat grey hair parted in the middle and tied in a low round bun, gentle crescent eyes, a long blue-grey lay Buddhist robe (áo lam) to mid-calf with wide sleeves over dark trousers, a dark wooden bead bracelet on her right wrist, simple brown sandals
- **Mướp:** a small round grey-and-cream tabby temple cat with soft darker stripes on its back, a white chest and paws, a big round chibi head with two triangle ears, dot eyes and a tail with a dark grey tip. It has no hands and never holds a prop.

Grey and brown robes make chibi monks look alike, so the silhouettes differ on purpose: a tuft, a bald round head, a hood, a tall stooped figure, a bun, a cat. They differ in size and build as well, not only in colour.

## Core rules this style overrides

- **Holds are welcome.** The idle ban still holds (breathing, blinking and sweeping count as motion), but a calm beat may hold the pose. Reason: the style is about stillness.
- **Faces stay minimal.** Expressions move only the eyes, brows, mouth and cheeks, with no manga marks. Reason: marks break the calm, and detailed faces drift.
- **Music is one quiet frozen score** with a single bell tone at most per clip, not a mood change per clip. Reason: calm audio is part of the style.
- **One location per video by default** (the temple yard). A change of place needs a time cut stated in the first-frame line. Reason: empty frames make background drift easy to spot.
- **Humour is quiet.** No slapstick falls or pratfalls. Reason: the subject is monastic life.

## Text policy

`post-overlay`. No words, numbers or scripture in any frame; a book or sutra is a plain closed or blank-paged book. Captions, the page name and any subtitle are added in post-production.

## Motion cadence

`smooth`, with holds. Movements are slow and eased. A held pose is allowed for a beat while something small still moves: a leaf falling, steam rising, breathing.

## Camera grammar

- **Transition moves only:** hold, slow push-in, pull back, slow lateral track or pan, hard cut.
- **No accent moves:** no fast push-in, slam zoom, whip pan, shake or orbit. The quiet style has no punchline accents.
- **Hold during demanding body actions:** a hand-over, a bow, a prostration.
- **At most one inward move per clip,** and never inward moves in three clips in a row.
- **Name the move at the start of every timed beat.**

## Posture limits (from the posture gate)

These came out of gating 44 human poses, 4 cat poses and a 4-character motion test.

- **Joined palms (gassho):** say "palms joined in front of the chest, fingers up" and keep both wrists on their own side; the hands meet in the middle and do not cross. With short chibi arms the palms sit low on the chest, below the chin.
- **Bow:** the hips go back and the knees soften as the torso tips. A stiff-legged bow with a big chibi head topples (the gate's balance check flagged all five drafts).
- **Prostration (lạy):**
  - The steps: kneel with toes tucked and thighs upright, fold forward from the hips with the hips staying highest, bow the head so the face turns to the floor and the forehead rests on it, then rest the forearms and flat palms on the floor beside the head.
  - Stage it in side view only.
  - Two drafts read as crawling on hands and knees with the head up, and both passed the gate. Check this pose by eye, every time.
  - A chibi head is bigger than the upper arm, so the elbows rest just above the floor rather than flat.
  - Prompt wording: "kneels, bows forward from the hips until the forehead rests on the floor, face down, forearms and palms flat on the floor beside the head".
- **Lotus / cross-legged sitting:**
  - In front view, mark the track `"cross_legged": true`. Cross-legged looks the same as a bad knee there, so the gate skips the hip abduction and knee lateral checks; still check the pose by eye.
  - Robes cover the legs, which hides most crossing errors.
  - Prompt wording: "seated cross-legged on a round cushion, robe covering the legs".
- **Meditation hands:** "hands resting in the lap, right hand on the left palm, thumbs touching". The wrists stay on their own sides; only the hands overlap.
- **Two-handed offering:**
  - Offer and receive with both hands, but chibi arms are short: the cup stays at chest height, within about 85% of the arm's reach.
  - The two people stand about two head-widths apart, and neither leans in so far that the big heads touch.
  - Name one holding hand per character ("his left hand under it and his right hand steadying its side").
- **Front-view sleeves:** the sleeves are one tone darker than the robe body, with an outline (the novices' grey sleeve takes a bigger step, since grey has no hue to help). In every front-view pose the elbows open far enough that the outer edge of the sleeve sits outside the body outline, with a sliver of background between elbow and waist.
  - Gassho: the wrists stay a palm-width apart so the short chibi arms can open the elbows; the lotus bud widens to join both palms. Meditation: the wrists also sit apart and the drawn mudra (right hand on the left palm, thumbs touching) bridges them at the centre of the lap. These tracks carry `contact_tolerance: 0.55` because the wrists, not the palms, are what the gate measures.
  - Prompt wording: "sleeves a shade darker than the robe, elbows held slightly away from the body, a little space between the arms and the waist".
- **Front view:** shoulders at the edge of the torso, with a small gap between the hanging arms and the waist. In the rig the rest angle is 22° for novices and 13–14° for adults.
- **Big heads:** the forehead-to-floor, hand-to-face and cup-to-mouth moments are where chibi proportions fail; stage them in side view.
- **The cat:**
  - It walks in a lateral sequence: hind, front, other hind, other front.
  - Its front elbows and hind hocks fold toward the tail.
  - When sitting or lying, its legs are tucked out of sight.
  - The tail is thin and curved, so it never reads as a fifth leg. Sitting, it lies back along the floor with the tip curled up; curled up, it wraps round the paws. A cat settling from a walk blends its legs and tail over about ten frames; it never snaps into the sit.
  - The cat tracks carry `"body_plan": "quadruped"` and pass both the shared posture gate (it reads four-legged tracks now) and the thread's own gait check in `src/cat.py`; the cat joins the `--scene` run.

## Hook overrides

- **Gentle hooks only:**
  - Sudden entry with a soft cause (a gust, a falling leaf, a cat);
  - Reaction before cause;
  - Partial reveal;
  - Satisfying motion.
- **The sound cue** is one soft natural sound or a single bell tone, never an impact or bass hit.
- **Avoid** Scale shock and Physics break unless the image stays calm (no giant objects crashing into the yard).

## Post-production

1. Trim each clip to its first clean frame and cut on motion (a broom stroke, a step).
2. Join a time cut with one short cross-dissolve (about half a second). Use hard cuts everywhere else.
3. Add captions, subtitles or the page name as overlays in a calm sans-serif in the empty sky area, never over a face or hands.
4. If music is laid in post, mute the generated score and keep the VO and sound effects.
5. Before publishing, review each clip at its risky moments:
   - the bracelet is on the right wrist;
   - hand passes are visible;
   - nothing sacred or written has appeared;
   - the cat has four legs and a thin tail.

## Sample package

[`samples/chu-tieu.md`](samples/chu-tieu.md), "The yard that never stays clean": 3 clips, a hook card, global continuity, a stitching guide and voice/music continuity. Lint facts are in [`samples/chu-tieu.facts.md`](samples/chu-tieu.facts.md). They were written by `tools/package_lint/package_lint.py package.md --clips 3 --anchor <An> --anchor <style block> --facts samples/chu-tieu.facts.md` and read `PASS: 0 red, 0 yellow`. `hand_ledger.py` (the shared PR #4 copy) reports `PASS`, and `tests/verify-opening-hook.py` passes.

## Catalog entry (draft)

Rows ready for `style-catalog.md` and the setup gate in `SKILL.md`. They should only be added once the owner wants the style offered.

Style matrix row:

```text
| **chu-tieu** | Chú Tiểu Little Monks (chú tiểu tối giản) | Calm, near-empty temple yard in flat pastels with one thin warm brown-grey outline; no statues, altar or writing | Mindfulness and kindness lessons, Buddhist-inspired everyday stories, slow-living tips | Original chibi temple cast (novices, a novice nun, an old monk teacher, a lay grandmother, a temple cat); bead bracelet on every right wrist |
```

Status row:

```text
| chu-tieu | gated | Posture gate 0 FAIL / 0 WARN on 44 human poses, cat tracks through the shared gate, 4-character scene incl. the cat; package_lint facts in the pack (`chu-tieu.md`); not tried on Flow |
```

Setup-gate line (offered only when the user asks for an experimental style, per the status rules):

```text
  - `chu-tieu (Chú Tiểu Little Monks, experimental: gated)`: calm, minimal chibi little monks in a near-empty temple yard, flat pastels, reverent and quietly funny; for mindfulness and kindness stories
```

## Acceptance

- Every human character's bead bracelet is on the right wrist in every frame. Reject a clip where it moves.
- No statue, altar, incense, writing or symbol appears, and no sacred figure moves.
- Joined palms meet in the middle without crossing, and bows bend at the hips with soft knees. In a prostration the face turns to the floor and the forehead, not the face, meets it.
- At least half of each frame is quiet empty space, with no more than four characters and three set pieces.
- The cat walks on four legs that keep their length and fold the right way, and its tail never reads as a leg.
- The package passes `package_lint.py` and `hand_ledger.py`, with one character per hand sentence and one name per prop.
