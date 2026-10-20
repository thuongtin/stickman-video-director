# Core Contract

These are the rules every style shares, Styles 1–4 and every slug style pack alike. Each rule is stated once here. The detailed wording lives in exactly one other file (the "Owner"), and the "Check" column names what enforces it. When a style reference or pack changes a rule, it does so only where the "Override" column allows, and it states the reason in its own file.

Read this file before planning (Phase A), and read it again before assembling prompts (Phase B).

## Rules

| ID | Rule | Owner | Check | Override |
|---|---|---|---|---|
| C1 | Setup gate: source, ratio, duration and style are known before planning. Phase B starts only after the current Phase A is approved; a global change sends the work back to Phase A. | `SKILL.md` | rubric SETUP, PLAN, REV | never |
| C2 | One complete narrator profile per video, repeated verbatim in every clip. No "same narrator" shortcut. Narration is audio-only. | `voice-continuity.md` | lint B5 | never |
| C3 | Clip 1 sets the score. Clips 2–N say that the identical score continues from clip 1 (same tempo and instrumentation). The piano-and-synth wording in `style-catalog.md` is only the Style 1/2 default. | `omni-flash-prompt-contract.md` | lint B12 | instruments: yes; the continuity sentence: never |
| C4 | Golden Hook (Stage 1): a hook card in Phase A; in Phase B, Clip 1's first frame is already mid-action and its first beat times the hook hit by about 2s. No separate `Opening hook:` prompt line. | `storyboard-template.md` (Golden Hook) | lint B2, `verify-opening-hook.py` | intensity and pattern only (its style table) |
| C5 | Hands are named from the character's own side. Every clip has `Hands at start` / `Hands at end` lines, a prop changes hands only in a visible beat, and all five posture negatives are present. | `posture-gate.md` | lint B3, B10 | may add limits, never remove |
| C6 | Posture budget: at most one demanding body action per character per beat, never at the same time as a camera shake, orbit or tilt. | `storyboard-template.md` | lint A3, B11 (camera side) | stricter only |
| C7 | Every character's anchor is repeated verbatim in every clip where that character appears. No "the same figure", ellipsis or per-clip redesign. | the style's reference or pack | lint B4 | never |
| C8 | No liquid or shape morphing. Change happens through a concrete action, a cut or a wipe. | `omni-flash-prompt-contract.md` | lint B8 | never |
| C9 | Text policy: by default the clip shows no words, letters, numbers or interface copy, and any approved phrase goes to the post-production overlay list. A pack may choose `blank-zone` (an empty board, bubble or sign is drawn and the text is added later) or `post-overlay`. No pack generates readable text. | `omni-flash-prompt-contract.md` | lint B7, B13 | `none` → `blank-zone` / `post-overlay` |
| C10 | Colours are named in plain words. No hex, RGB, HSL or Pantone. | `omni-flash-prompt-contract.md` | lint B6 | never |
| C11 | Prompts never name a studio, franchise, brand, signature character or artist, not even as "no X". Describe how it is drawn instead. | this file, `style-pack-template.md` | lint B14 (common names) | never |
| C12 | Cast: every visible character is planned and has a cast card; no unplanned extras ("no other people or animals" in the negatives when a cast is set). When two or more characters share a frame, each keeps a fixed screen side unless a beat moves them, beats name the character instead of using "he/she" when two of the same gender share a sentence, and cast members differ in silhouette, not only in colour. At most two characters do demanding actions in the same beat; the others hold simple poses. | this file | review | a pack may lower the limit |
| C13 | Every clip ending connects to the next opening through an action, a prop, screen direction or a named cut or time jump. | `storyboard-template.md` | rubric PACK-6 | Style 4 and packs: scene changes are allowed if named |
| C14 | Narrative arc: five-stage engine with a closing discussion prompt. | `storyboard-template.md` | rubric PLAN | yes: a pack or style reference may use setup → escalation → payoff (Style 3) or its own arc |
| C15 | Timing and density: three timed beats per clip, about 20–25 VO words, a visual change every two to three seconds, no idle character. | `storyboard-template.md` | lint B9, rubric | yes: holds, word budget, density and motion cadence (`smooth`, `on-twos`, `stepped`) |
| C16 | Camera grammar: slow or held moves for transitions, fast accents only for reveals, and no three inward pushes in a row. | `storyboard-template.md` | lint A3, B11 | a pack may ban moves (no orbit, no zoom) |
| C17 | No invented facts, statistics, quotations or product claims. | `SKILL.md` | rubric | never |
| C18 | After generation: make a risk sheet for every clip and review it before calling the clip accepted. Report the result as a review, not as certification. | `posture-gate.md`, `tools/risk_sheet/README.md` | person, using the sheet | never |

## Optional steps around generation

These steps are part of the stitching guide when they are used. None of them has been tested on Flow yet, so a package states which ones it uses and why.

1. **Reference images (Flow Ingredients) or a first frame.** A pack may ship a model sheet: the character's front and side views on a plain background. A rendered first frame is another option, for code-rendered styles. Either is attached in Flow as a reference image. The anchor text is still repeated in every prompt (C7). The image adds to the text; it does not replace it. Record in the delivery note which image was attached to which clip.
2. **Post-production**, in this order:
   1. Trim joins and short audio crossfades.
   2. The pack's own post step, if it has one (for example a pixel lock or a stop-motion step).
   3. Text overlays from the overlay list, at the listed times and safe areas (C9).
   4. A single external VO and music track, only if C2/C3 drift is heard across joins.

## How a style changes the core

- Styles 3 and 4 change C14 and C15 and, for Style 4, C13, as their reference files say.
- A slug pack lists its overrides in its "Core rules this style overrides" section (`style-pack-template.md`). Each entry names the rule by ID.
- An override marked "never" in the table above is not available to any style. A pack that needs one is not ready to ship.
