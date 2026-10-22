# Motion-Graphics Segment Spec Contract

Use this contract only after explicit approval of the current Phase A. It owns the segment spec order and the wording of several shared rules; `core-contract.md` lists every shared rule once and says which file owns it and what a style may override. Refer to `references/style-catalog.md` for full style specifications and spec blueprints. Apply `voice-continuity.md` to every style; visual-style overrides never replace its complete video-level voice profile.

## How the video is built

The video is motion graphics. Each character is a rig drawn in the style's look (2D joints, cut-out pieces or a simple 3D skeleton) and animated with key poses; backgrounds, props, icons and effects are separate layers; the camera is a move over that layered scene. Narration is recorded or synthesised as one off-screen VO track; music and SFX are laid in the edit. The skill writes the director's proposal and then one standalone segment spec per approximately ten-second segment. An animator or a coding agent builds each segment from its spec alone, so every spec repeats the locks it needs.

Style 3 (Prehistoric Hand-Drawn / Dark Comedy): read `prehistoric-dark-comedy.md` and apply its override rules. Repeat the full approved cast descriptions for all visible roles, white filled heads, expressive cartoon faces, hair/clothing, earthy setting and layout in every spec. Do not apply generic face/hair/texture bans or idle bans to its deliberate reaction beats. Use story-appropriate music instead of mandatory piano. Explicitly identify intended time jumps; otherwise match adjacent states.

Style 4 (Cozy Storytelling / 治愈故事风): read `cozy-storytelling.md`. Repeat full character and voice anchors, but give each segment its approved new setting. Describe each scene opening as a recognizable new location, then connect action/prop/screen direction or a named time cut. Do not repeat one global room layout, inherit Style 1's no-face/filled-body bans, or require hand-drawn/paper aesthetics. Keep movable-object appearance separate from initial positions and timed state changes.

Style 5 (Historical Cartoon / 历史卡通风): read `historical-cartoon.md` for its standalone spec order and overrides. Repeat the full frozen drawing anchor, visible cast cards, approved era pack and complete `voice-continuity.md` voice block in every segment. Keep solid oval eyes and black stick limbs, with historical costume layers on the shared rig and colored painterly scenery. Do not inherit Style 1's hollow-head/no-face/no-clothes contract or generic piano, three-color, four-device and no-idle requirements. Follow its era score, physical beats and planned cuts; do not shorten approved anchors to meet an arbitrary character budget.

## Production package order

Deliver these sections in order:

1. Global continuity block
2. N standalone English segment specs (where N = target duration / 10; default 6 segments for 60s)
3. Stitching guide
4. Voice and music continuity note

## Global continuity block

State the chosen aspect ratio (`16:9` or `9:16`), target duration, selected visual style (Style 1 Classic, Style 2A Studio Tech, Style 2B Cinematic Story, Style 3 Prehistoric, Style 4 Cozy Storytelling, or Style 5 Historical Cartoon), character anchor design, palette or environment definition, narrator identity, audio arc, and continuity strategy. Treat this block as a review summary; each spec still repeats all critical locks.

## Standalone segment spec order

Write every segment spec in this order:

1. Render specification: approximately ten seconds, chosen aspect ratio (`16:9` or `9:16`), 1080p, 24 FPS; VO, music and SFX are separate tracks timed to the beats
2. Environment and background definition:
   - For Style 1 Light: flat, uniform, digitally pure-white canvas with no shading or 3D depth
   - For Style 1 Dark: flat, uniform, pitch-black canvas with pure white line art
   - For Style 2A (Studio Tech): modern bright white studio space with subtle light-gray perspective grid lines on the floor plane, high-key lighting, clean white negative space, sleek glowing cyan/blue glass elements
   - For Style 2B (Cinematic Story): rich full-color cinematic environment with soft light shafts and layered depth
   - For Style 4 (Cozy Storytelling): full-color 2D cartoon environment and a segment-specific setting, with varied wide/close/moving shots; new segment means an intentional scene change unless otherwise approved
   - For Style 5 (Historical Cartoon): full-color painterly historical setting from the approved era pack, with clean cel shading; name the segment's location and any planned time cut
3. Character lock:
   - For Style 1: repeat the concise frozen character anchor from `style-catalog.md`, including the chosen polarity and expression setting; no "same character" shortcuts, numeric anatomy recipes or pen paths in the spec (the rig owns its measurements). Keep the circular head hollow, proportions and line weight stable, and only the current pose of each of the two arms and two legs. A raised arm replaces its old lowered line. Keep accents on props/graphics, never recolor the figure. Do not let action or camera wording redefine the drawing; preserve rich motion and effects separately.
   - For Style 2 (Modern Pop):
     - Every segment, verbatim, the default lead: `A minimalist 2D animated stick figure with a big white round head on a very short neck, simple dot eyes, a very short dark buzz cut (close-cropped spiky black hair) and thick dark rectangular glasses, wearing a loose plain white short-sleeved button-up shirt with a small pointed collar, buttoned all the way down, cut like a t-shirt that flares slightly to just below the hips, with short wide sleeves rolled up above the elbows, with simple black stick arms and slim legs in dark blue jeans. Simple black lines, vibrant colors, smooth 2D animation style.`
     - Only when the user asked for the beanie character: the beanie alternative anchor from `style-catalog.md`, verbatim, instead. One lead per video.
     - No "the same figure" or ellipsis shortcut in segments 2–N. The glasses stay on in every beat.
   - For Style 4: repeat its full frozen character anchor from `cozy-storytelling.md`, including white head/torso fill, dark limbs and simple facial marks. Location and expression changes do not redesign the character.
   - For Style 5: repeat its full drawing anchor from `historical-cartoon.md` and the full approved cast card of every visible role. Era costume layers sit on the shared rig; solid oval eyes, white head fill and black stick limbs never change.
4. Palette and accent roles (expressed only with ordinary color names, no hex or technical codes)
5. Composition strategy for the chosen ratio (`16:9` or `9:16`)
6. First-frame state inherited from the previous segment, including the `Hands at start` ledger line from `posture-gate.md` whenever a character holds something
7. `[0–3s]`, `[3–7s]`, and `[7–10s]` visual beats tied to spoken ideas
8. Exact English VO lines in quotation marks, recorded as audio only (strictly no speech bubbles or dialogue boxes)
9. Complete frozen English voice block from `voice-continuity.md`, verbatim in every segment: identity/age, accent, timbre, register, resonance, texture, delivery, pace and recording treatment; no "same narrator" shortcuts or segment-specific recasting
10. BGM, synchronized SFX, and voice-first mixing (segments 2–N state that the BGM continues seamlessly from clip 1)
11. Final-frame transition state inherited by the next segment, including the `Hands at end` ledger line
12. Negative constraints (including style-specific clutter/deformation bans)

Make each spec self-contained and buildable without any external context beyond the style's rigs.

Clip 1 only: follow "Golden Hook in detail" in `storyboard-template.md`. Make the first-frame state the approved hook's first frame, time the hook hit inside the first beat, sync its sound cue, and start the quoted VO with the approved first spoken line. The hook adds no separate line to the spec.

## Style language

Use this wording to request density without character drift:

> rapid scene changes, kinetic motion-graphic transformations, and frequent visual events, while preserving an identical stick-figure design, constant line weight, and strict temporal consistency

Avoid `rapid style changes`: the look of the rig, its line weight and its design stay fixed for the whole video.

## Timed visual sequence & motion dynamics

Translate the approved storyboard row into three connected physical events:

- `[0–3s]`: establish or inherit the visual premise.
- `[3–7s]`: transform, escalate, or explain the metaphor through character action.
- `[7–10s]`: deliver a climax and create the next transition.

### Readable-motion guidelines
- Do not use abstract liquid or object shape morphing (e.g., stairs melting into a clock): it breaks the silhouettes the rigs and props are built from and reads as a change of style. Change things through a concrete action, a cut or a wipe.
- Drive motion with concrete character actions (leaping, touching glass, drawing luminous lines, opening heavy doors).
- Ensure continuous character engagement; never leave the character standing idle or staring at the camera for multiple seconds.

## Dialogue and visual text

Quote the approved English VO exactly once as audio-only narration:
```text
Audio voiceover only, strictly no speech bubbles, no dialogue boxes.
```
The VO track carries exactly these lines: nothing added, omitted, paraphrased, repeated or reordered, and no caption, subtitle or visual transcription inside the scene layers.

Default every segment to no visible words, letters, numbers, captions, subtitles, interface copy, palette labels, production annotations, logos, or watermarks in the scene art. Require icon-only message bubbles, content cards, clocks, meters, and notifications. Put optional approved phrases in a separate post-production overlay list outside the specs, so subtitles and titles stay one editable layer that can be translated or removed.

## Palette notation

Use ordinary descriptive color names such as vivid red, electric blue, or warm gold. Never put hexadecimal, RGB, HSL, Pantone, or other technical color notation in a segment spec. The exact values live once in the style's rig and palette files; a number copied into each spec drifts from segment to segment and ends up as stray label text.

## Audio continuity contract

Use the shared contract in `voice-continuity.md` for Style 1 Light/Dark, Style 2A, Style 2B, Style 3, Style 4 and Style 5. Choose voices per video, not per segment. Every standalone spec carries its own full voice and music instructions:

1. **Narrator Lock**: Resolve one complete approved profile, then repeat its frozen English block verbatim across all N specs. Use the accepted male block or build another coherent profile; do not force all videos into one voice. "Same narrator" and "continue the voice from clip 1" alone are insufficient. Separate voice identity/delivery/recording treatment from the emotional and musical arc; no scene-specific timbre changes or switches into character dialogue unless explicitly approved.
2. **BGM Lock**:
   - Clip 1 establishes the musical theme.
   - Clips 2–N say explicitly: `Audio: Voiceover seamlessly continues the identical quiet, thoughtful piano and subtle soft ambient synth from clip 1, maintaining identical tempo, instrumentation, and optimistic narrative momentum. Synchronized crisp SFX on physical actions.`

## Negative contract

Forbid:

- photorealism and unwanted 3D humanoid rendering
- facial features (pupils, realistic eyes, lips) or hair unless approved
- extra limbs, malformed anatomy, disconnected lines, or changed proportions
- knees or elbows bending backward, limbs changing length, a head turned past the shoulders, swapped left and right hands, or a prop switching hands without a visible pass
- broken or changing line weight
- **For Style 1**: do not reject allowed occasional simple line expressions as character drift; filled heads, sudden head/body proportion changes, duplicated/retained limb poses, body silhouettes, separate hand/foot shapes and detached body lines remain failures. Inspect the rendered segment at reaches, releases, turns and walking poses, and compare segments. State the scope of inspection: sparse keyframes cannot prove the absence of brief errors between them.
- inverted theme polarity or unexplained colors
- unintended characters or irrelevant spectacle
- visible words, letters, numbers, technical color notation, palette labels, interface copy, captions, subtitles, logos, or watermarks
- altered, omitted, repeated, reordered, or added dialogue
- speech bubbles, comic dialog balloons, or visual text boxes
- **For Style 2A specifically**: `strictly minimalist studio aesthetic, no circuit board textures, no sci-fi wall panels, no spaceship corridors, no cracked concrete, no grunge textures`
- **For Style 2B specifically**: `no photorealistic human skin, no 3D humanoid CGI models, no chaotic line glitches`

## Stitching guide

List all N segments in order. For every cut, repeat the ending state and its continuing action/prop/direction, or state the approved location/time change. Styles 4 and 5 change scenery intentionally rather than requiring identical backgrounds. Include any trim, short audio crossfade, or match-cut note needed for assembly; check the rendered joins rather than assuming a wipe lands on the last frame.

## Audio continuity note

Keep one voice across the video:

1. Check that every spec repeats the full frozen voice block and contains no conflicting voice directions.
2. Record or synthesise the whole narration in one session with one voice (or one recorded take per approved speaker), then cut it to the segment timings; do not record segment by segment with different settings.
3. Compare the assembled VO by listening, not from screenshots or waveforms. A re-record of one segment uses the same voice, settings and microphone as the rest.

## Phase B checks

- The user approved the current Phase A.
- Exactly N standalone segment specs are present (matching approved Phase A duration).
- Each spec repeats ratio (`16:9` or `9:16`), style/theme, character, palette, voice, audio, transition, and negative locks.
- Style 1 specs repeat one identical full character block and contain no contradictory appearance instructions. Simple-expression allowance agrees with the negative constraints. The rendered look is checked separately from spec compliance.
- Each spec has all three timed beats and at least four relevant visual devices.
- Clip 1's first-frame state and first timed beat match the approved hook card, the hit is timed at about 2s or earlier, no spec carries an `Opening hook:` line, and the hook contains no on-screen words or numbers.
- Every ending connects to the next opening through a planned action/prop/direction or an approved location/time cut. Style 4 does not repeat one room unless requested.
- Dialogue exactly matches the approved narration.
- Dialogue is explicitly audio-only and is never displayed visually.
- Standalone specs contain no hexadecimal, RGB, HSL, Pantone, or other technical color notation.
- Style 2 specs feature the verified character anchor, BGM continuity lock, and anti-clutter negative constraints.
- All styles repeat an identical complete voice block per video (or per approved recurring speaker); no unresolved profile fields, abbreviated voice references or contradictory per-scene vocal directions remain. The recorded VO is checked by listening, separately from spec compliance.
- The scene art contains no visible writing; optional overlay phrases are listed separately for post-production.
- Every held prop is named with the character's own hand; `Hands at start` / `Hands at end` lines are present and `tools/posture_gate/hand_ledger.py` reports no problems for the package.
- `tools/package_lint/package_lint.py <package.md> --clips N` reports no RED (it also runs the hand ledger, checks verbatim anchors and voice blocks, quoted on-screen words, morphs, beats, camera accents and overlay numbers). Add `--anchor "..."` for each approved Style 3/4 cast anchor. Answer each YELLOW in one line or fix it. When reporting the result, quote the facts block written by `--facts` instead of claiming a pass; the lint reads spec text only and is not a check of the rendered video.
