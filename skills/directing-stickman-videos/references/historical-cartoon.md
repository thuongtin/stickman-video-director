# Style 5 — Historical Cartoon / 历史卡通风

Historical explainers, daily life, civilization stories and comic historical shorts, using expressive stick figures in colorful historical worlds.

Visual concept and Roman era-pack contribution: [Lawal Ridwan / @leksautomate](https://github.com/leksautomate), via [History Stickman](https://github.com/kaomei/stickman-video-director/pull/41), adapted upstream as Style 5. This fork builds the style as motion graphics: the drawing grammar below is drawn by a rig, and each era pack changes costumes, sets, props, palette and music, never the rig. A code-rendered cast sheet and motion clip for four era roles live in `docs/style-5/` (`render.py`, every pose gated).

## Fixed drawing grammar

Repeat this anchor verbatim in every standalone segment spec:

```text
Polished 2D cel-shaded cartoon animation with thick clean black outlines and soft metallic shading. Stick-figure characters with smooth white filled round heads, simple black oval eyes, expressive brows and mouths, no nose, and thin black stick limbs, in the described costume. Exactly two arms and two legs, each shown only in its current pose. Clean, sunlit, painterly landscapes.
```

Keep white head fill, head/body proportions, outline weight and black stick limbs fixed within a story. Open eyes are simple solid black ovals without iris/pupil detail; a blink or closed-eye expression does not redesign the eyes. Cloth, leather and metal can have soft shading and small highlights: one flat shadow band on the side away from the light, and a thin highlight band on metal. Backgrounds are full-color painted landscapes or architecture, not empty white canvases, paper textures, ink wash, photorealistic people or glossy 3D characters. Approved night/interior lighting changes illumination, not drawing grammar. Costume may cover limbs without changing their underlying black line design.

In the rig, costume parts are layers on the same skeleton: a helmet, hair or headwear layer on the head, a garment layer on the torso, sleeve caps on the upper arms, and skirts, kilts or wide trousers over the legs. The joints, limb lengths and head size do not change between eras, so every era reuses the same walk cycle, gestures and posture-gate settings.

## Phase A: era and cast

Use the existing proposal and approval workflow. Include a compact era pack:

- **Era/place:** period, region and the story's factual premise.
- **Roles/wardrobe:** each visible role's silhouette, clothing and recognizable accessory.
- **Settings:** story locations, architectural landmarks, screen direction and planned time cuts.
- **Palette:** four to six ordinary color names and their roles.
- **Props/symbols:** tools, weapons, furniture and icon-only emblems, with ownership and counts.
- **Music:** era-appropriate instruments and one coherent score direction.
- **Facts:** distinguish supported history from illustrative scenes or fictional jokes; do not invent quotations, statistics or historical events.

For a different era, draft and confirm a new pack rather than borrowing Roman armor or symbols. Adapt Egyptian, Chinese, Japanese, Vietnamese or other clothing and buildings while preserving the drawing grammar. Do not make one Roman soldier a universal cast for all stories.

For each recurring role, write a complete story-specific cast card: role/age range, head/body proportions, face and eye shape, hair/beard or explicit absence, headwear, clothing layers and silhouette, limb treatment, footwear and distinguishing accessory. Give recurring roles at least two visible non-color differences. Resolve concrete features instead of writing only “a soldier” or “a princess.” Freeze each approved card and repeat its **full description** in every standalone segment spec where the role appears; never substitute “same character,” an ellipsis or a name alone. A crowd can use one uniform group description, with named foreground characters separately identified.

Keep appearance separate from action: a spade's shape belongs in its prop description; who holds it, in which hand, and whether it touches the ground belong in opening/action/ending states. Do not make all props permanently held or all characters permanently front-facing merely to prevent drift.

### Roman era pack

- **Place:** Roman Republic/Empire, Mediterranean roads, camps, towns and countryside; specify the period needed by the topic.
- **Soldier:** bronze-gold helmet with black horsehair crest, grey chainmail, red tunic, brown segmented leather skirt, thin black limbs and a short sword. Include a red shield with a gold icon only when the scene needs it. Officers can use a distinct crest or cape, frozen in their own cast cards.
- **Civilian:** cream tunic or toga with a story-specific accessory; approve the complete card rather than treating all civilians as soldiers without helmets.
- **Settings:** green hills, cypress trees, dusty roads, wooden palisades and camp ditches; Forum, harbor or market architecture when relevant.
- **Palette:** Roman red, bronze gold, steel grey, grass green, sky blue, earthy tan.
- **Music:** restrained drums, brass and strings for epic scenes; light plucked strings and woodwinds for daily life or comic scenes. No mandatory piano.
- **Treatment:** costume is simplified illustration, not evidence for an exact historical uniform. Preserve the factual narration while using fictional individual characters to illustrate it.

The sheet in `docs/style-5/` also shows an Edo-period student and an Egyptian temple attendant. They are examples of how far one rig can travel, not approved era packs: a story set in those eras still drafts and confirms its own pack and cast cards in Phase A.

## Phase B: standalone segment specs

Each spec contains:

1. Approved duration/ratio and technical targets.
2. Full drawing-style anchor, era palette and segment setting.
3. Full cast cards for every visible recurring role, plus relevant prop designs/counts.
4. Opening layout, held items, `Hands at start` / `Hands at end` and screen direction.
5. `[0–3s]`, `[3–7s]`, `[7–10s]` physical beats, camera work and ending state.
6. Exact approved audio-only VO and the complete frozen voice block from `voice-continuity.md`.
7. Era score, timed SFX and voice-first mix; retain the same score identity across segments.
8. Compatible negatives, including the posture negatives from `posture-gate.md`.

Use the existing accepted male profile by default when no other voice is requested. Honor female, older, youthful or other voice choices by resolving a complete profile through `voice-continuity.md`, then freezing it across the whole video. Cast gender or a change of era never recasts the off-screen narrator. Keep voice identity separate from music and visual emotion.

Use the five-stage engine for explainers where useful; narrative shorts can use setup → escalation → payoff without forcing a discussion question. Prefer a few readable physical actions over four unrelated effects. A deliberate reaction pause is valid. Wide establishing shots, lateral tracking, medium actions and close reactions should serve the narration. Maintain screen direction and describe a planned time jump explicitly when adjacent states do not directly match.

Keep one current pose per limb. Give prop transfers a clear release, travel and receiving state; do not spawn duplicate tools or transform one item into another. Use the smallest cast the story needs. Describe background groups as uniform ranks, not many competing named roles: in motion graphics a rank is one rigged figure repeated with small timing offsets, not many hand-animated extras.

Preserve complete approved style, cast and voice blocks; there is no style-specific character-count cap. Remove conflicting or redundant wording rather than stripping identity details.

```text
NO VISIBLE TEXT, LETTERS, NUMBERS, SUBTITLES, LOGOS OR WATERMARKS (blank paper or abstract brush strokes only), NO SPEECH BUBBLES, NO BLOOD OR GORE, NO PHOTOREALISTIC FACES, NO 3D CGI, NO PAPER TEXTURE, NO EXTRA LIMBS, NO FUSED OR DUPLICATE HEADS, NO COSTUME CHANGES, NO EXTRA CHARACTERS.
```

Keep negatives compatible with the approved cast: do not ban simple faces, historical clothing or chosen hair/beards. A model sheet drawn from the rig (front and side of each role, as in `docs/style-5/sheet.png`) is the visual reference the segments are built against; it adds to the cast card text and never replaces it.

## Review

Before delivery, compare repeated style/cast/voice blocks and all adjacent prop states. After rendering, gate every character's exported pose track with `posture_gate.py`, review each segment's risk sheet, and check the frames for head fill, eye design, costume silhouette, limbs, prop counts and action joins; listen separately for narrator consistency. Record spec compliance separately from what the rendered frames show. Localize changes to Style 5; do not rewrite Styles 1–4.
