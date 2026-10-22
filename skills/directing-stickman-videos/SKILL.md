---
name: directing-stickman-videos
description: "Use when turning copy, notes, articles, or topics into customizable-length English stick-figure or illustrated-character videos (classic stickman plus experimental styles such as paper cutout, chibi, watercolor or Vietnamese folk prints) (in 10-second multiples: 30s, 60s, 3min, 5min, default 60s), kinetic line-animation explainers, motivational shorts, or Gemini Omni Flash prompt packages."
---

# Directing Stickman Videos

## Core contract

Turn one source into a confirmed director's proposal and then N standalone prompts for approximately ten-second Gemini Omni Flash clips (where N = target duration in seconds / 10; default 6 clips for 60 seconds). Preserve the source's meaning while structuring it through a high-completion 5-stage emotional narrative arc.

## Setup gate

Require these before planning:

- source material
- aspect ratio: `16:9` or `9:16`
- target duration: in multiples of 10 seconds (e.g. `30s`, `60s`, `90s`, `3min`, `5min`; default: `60s` / 6 clips if unspecified)
- visual style and theme:
  - `Style 1 (Classic Minimalist)`: light (white background, black figure) or dark (black background, white figure)
  - `Style 2 (Modern Pop)`: default lead Nam (dark buzz cut, dark rectangular glasses, white short-sleeved button-up shirt, jeans; same body as the beanie lead); upstream's red-beanie Zeke only when the user asks for it
    - `Style 2A (Modern Studio Tech)`: pure white high-key studio, subtle light-gray perspective grid, floating cyan/blue glass UI
    - `Style 2B (Cinematic Story)`: full-color narrative environments, cinematic lighting & depth
  - `Style 3 (Prehistoric Hand-Drawn / Dark Comedy)`: expressive white filled heads, black stick limbs, animal-hide costumes and earthy prehistoric settings; story-specific casting
  - `Style 4 (Cozy Storytelling / 治愈故事风)`: expressive minimalist white-filled characters with dark stick limbs in full-color 2D cartoon environments; varied story locations and cinematic shot changes
  - Experimental styles (`gated`), offered only when the user asks for an experimental style or names one by slug: the 23 slug styles in the "Experimental styles" table of `references/style-catalog.md` (for example `dong-ho`, `chu-tieu`, `watercolor-storybook`). Say the style is `gated` when offering it.

If aspect ratio or visual style is missing, ask for all missing items in one concise message and stop. If duration is omitted, default to 60 seconds (6 clips). If a user provides a duration not divisible by 10, round to the nearest 10-second multiple. If a user specifies only light or dark theme, default to Style 1. Never select an aspect ratio or style silently. Do not re-ask choices already supplied.

Urgency, generation cost, client pressure, and requests to "pick normal settings" do not waive this gate.

## Workflow

1. Read `references/core-contract.md`, `references/storyboard-template.md`, `references/style-catalog.md` and `references/voice-continuity.md`. Structure the narrative using the **5-Stage High-Completion Heartbeat Engine** (Golden Hook → Disrupting Assumptions → Unveiling Insider Secrets → Ultimate Truth Revelation → Elevation & Interactive Discussion), with timing dynamically scaled to the target duration. Produce Phase A in the user's language, with English VO and a reference translation.
2. Stop after the director's proposal and request explicit approval.
3. If the user changes ratio, duration, style, theme, narration, scene structure, or global direction, recompose Phase A and request approval again.
4. Only after approval of the current Phase A, read `references/omni-flash-prompt-contract.md` and `references/posture-gate.md` and produce Phase B.
5. Use `references/examples.md` only when a concrete end-to-end example would resolve ambiguity.

Topic approval, schedule pressure, or approval of an older draft is not approval of the current Phase A.

## Output rules

For Style 3, read `references/prehistoric-dark-comedy.md` before planning. Its casting, story rhythm, palette and continuity rules override the generic no-idle, device-count and five-stage discussion-ending rules below. Use setup → escalation → ironic payoff for narrative shorts; do not force a discussion question into a visual punchline. This is a visual storytelling style, not a claim about actual prehistory.

For an experimental slug style, read `references/styles/<slug>.md` before planning and prompt assembly, and use its sample in `references/styles/samples/<slug>.md` as the prompt shape. Its frozen anchors, style block, overrides, bans and acceptance list win over the generic rules below, the same way the Style 3 and Style 4 references do; the voice contract, hands ledger and package lint still apply.

For Style 4, read `references/cozy-storytelling.md` before planning and prompt assembly. Default each new ten-second segment to a different recognizable story setting, unless the user explicitly requests one location or approves a deliberate return. Preserve characters, drawing grammar, important props, movement direction and narrator—not an identical table or background across the whole video. Name the location cuts and any time jumps in Phase A. This is full-color cartoon storytelling, not a hand-drawn/sketchbook mode and not a claim of photorealistic 3D backgrounds.

- Structure every script using the 5-stage high-completion flow:
  1. **Golden Hook**: Instant curiosity trigger via a counter-intuitive question or visual paradox. Timing is flexible based on duration (e.g. within the first 2–5 seconds in short videos, up to 10–15s in long videos); never open with generic platitudes. For every style, follow "Golden Hook in detail" in `references/storyboard-template.md`: a complete hook card in Phase A, a first frame that already shows the character mid-action with a visible tension, one hook hit by about 2s that reads with the sound off, and a first spoken line of about four to ten words with no greeting. In Phase B the hook lives in Clip 1's first-frame state and first timed beat; it adds no extra prompt line.
  2. **Disrupting Assumptions**: State what everyone thinks is true, then shatter it in one sentence to build cognitive conflict.
  3. **Unveiling Insider Secrets**: Pull back the curtain on hidden mechanics, counter-intuitive details, or the real obstacle.
  4. **Ultimate Truth Revelation**: Deliver the underlying business logic or human psychology truth with maximum cognitive payoff.
  5. **Elevation & High-Engagement Discussion**: Conclude with a memorable punchline and an irresistible discussion prompt that sparks debate in the comments.
- Scale English VO word count to approximately 20–25 words per 10-second clip across N clips (e.g. ~60–75 words for 30s / 3 clips, ~120–150 words for 60s / 6 clips, ~360–450 words for 3min / 18 clips, ~600–750 words for 5min / 30 clips).
- Give each clip three timed beats, at least four relevant visual devices, and a visual change every two to three seconds. Choose camera moves with the camera grammar in `references/storyboard-template.md`: hold or move slowly for transitions, keep fast accents for reveals, and do not push inward in three clips in a row.
- Keep character proportions, line weight, style, and narrator consistent across all clips.
- For Style 1, freeze the concise character anchor from `references/style-catalog.md` and repeat it verbatim in every clip. Keep two arms and two legs, one current pose per limb, stable proportions and uniform medium line weight; a moving arm replaces its previous pose rather than adding another arm. Keep the figure monochrome and saturated accents on props/graphics. Do not replace the anchor with "same character", ellipses, numeric anatomy recipes, skeleton/path instructions or clip-specific appearance descriptions. Occasional simple line expressions are allowed; the head remains hollow. Keep rich actions and effects separate from character design. Treat generated consistency as a visual acceptance check, not a guarantee from repeated text.
- For Style 1, limit the video to three saturated accent colors named with ordinary descriptive words (e.g. vivid red, electric blue, warm gold). For light theme, enforce a flat, digitally pure-white canvas with no textures, gradients, or 3D depth.
- For Style 2 (Modern Pop), enforce character consistency:
  - Every clip, 1 through N, repeats this default anchor verbatim: `A minimalist 2D animated stick figure with a big white round head on a very short neck, simple dot eyes, a very short dark buzz cut (close-cropped spiky black hair) and thick dark rectangular glasses, wearing a loose plain white short-sleeved button-up shirt with a small pointed collar, buttoned all the way down, cut like a t-shirt that flares slightly to just below the hips, with short wide sleeves rolled up above the elbows, with simple black stick arms and slim legs in dark blue jeans. Simple black lines, vibrant colors, smooth 2D animation style.`
  - Use the beanie alternative from `references/style-catalog.md` instead only when the user asks for the beanie character or Zeke; never mix the two leads in one video.
  - Never shorten the anchor to "the same figure" or an ellipsis in later clips; that drops the clothing, glasses and limb locks.
  - No detailed eyes, pupils, or photorealistic features (avoids bug-eye deformation). The glasses stay on in every shot.
- For Style 2A (Modern Studio Tech), enforce: `in a modern bright white studio space with subtle light-gray perspective grid lines on the floor plane. High-key studio lighting, clean white negative space, sleek glowing cyan and electric blue glass holographic UI elements.` Always include negative constraint: `STRICTLY MINIMALIST, NO CIRCUIT BOARD TEXTURES, NO SCI-FI WALL PANELS, NO CRACKED CONCRETE.`
- For Style 2B (Cinematic Story), specify full-color narrative setting and cinematic lighting while preserving the 2D animated stick-figure character design.
- For Style 4, freeze each approved character's complete anchor and repeat it in every clip where that role appears. Separate static design from first-frame positions, timed prop transfers and final states; changing scene does not reset prop ownership or the narrator. Read its reference for shot variety and visual acceptance checks.

- For all styles, apply `references/core-contract.md`. It states each shared rule once, with the file that owns its wording and what checks it:
  - one narrator block repeated verbatim (`references/voice-continuity.md`) and a score that continues from clip 1;
  - hands named from the character's own side with `Hands at start` / `Hands at end` lines and the posture negatives (`references/posture-gate.md`), plus the posture budget;
  - anchors verbatim in every clip;
  - no morphing;
  - no generated text: overlays go to post-production;
  - plain colour words;
  - no studio, franchise, brand or artist names;
  - planned cast only;
  - planned joins between clips;
  - no invented facts.

  Style 3, Style 4 and slug packs override only the rules its table marks as overridable.
- Before delivering Phase B, run `tools/package_lint/package_lint.py` on the package (Phase A storyboard included when available) and fix every RED; it runs `tools/posture_gate/hand_ledger.py` as check B3. After generation, review each clip with `tools/risk_sheet/risk_sheet.py` (`references/posture-gate.md`); report generated-clip results as a review, not as certification.

## Revision rules

Recompose rather than rename:

- `16:9`: stage action across left, center, and right; use lateral tracking and negative space.
- `9:16`: use depth, stacked motion, vertical reveals, and interface-safe placement.

Theme, ratio, duration, or style changes require a fresh visual balance check. A global change invalidates prior approval.

## Final check

Apply the checklist in the loaded reference. Repair any failed condition before responding.
