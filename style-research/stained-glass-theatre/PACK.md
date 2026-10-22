# Stained-glass theatre

Status: gated, narrowly scoped (22 October2026)
Scope: one original Lumen front-view rig,16:9, planted empty-hand gestures, one10-second silent demo. Not covered: locomotion, side/rear views, multiple characters, contact/transfer, narrated production, physically simulated transmission/refraction.

## Frozen anchor
Lumen is an original adult-proportioned articulated glass puppet. Oval pale amber face, tiny dark eyes and small painted mouth, teal faceted tunic, amber collar, slender glass arms and legs with circular dark hinges. Two arms and two legs. Small rounded ivory glass palms. One gold ring on Lumen's own right wrist only; own right is screen left in the front view.

## Signature wording
A luminous stained-glass theatre with hard coloured glass facets joined by dark lead seams, small pale edge glints, slender articulated glass limbs and circular dark hinges. Dark indigo stage, teal tunic and warm amber face and lantern. No paper texture.

See research.md for three museum sources, reference coverage, nearest-neighbour comparison and the mandatory/bonus/forbidden checklist. Three composition options were imagegen-created before code. This draft does not add a catalog entry.

## Overrides and limits
- C9: none, no scene lettering or overlay.
- C14: proposed mini-arc: dim lantern, ignition and greeting, settled pose. A short technical demonstration, not a full five-stage teaching story.
- C15: proposed sparse narration and pose holds for a10-second sample. Actual demo is silent and does not claim full narrator/audio acceptance.
- C16: locked camera, no orbit/shake/tilt. Character remains front-facing.
- All non-overridable rules remain intact. This draft fixture is not an owner-approved PhaseB production package.

## Construction and postproduction
Pillow draws each coloured pane and opaque seam as independent geometry over the stage; joint math is reused from the repository. Exported joint tracks are the same joints used to draw frames. Encode PNG sequence with ffmpeg H.264. No video-generation service or paid API. Shape texture and glow are illustrative2D approximations.

## Gates and review
sample.md is the lintable prospective segment specification, sample.facts.md its measured lint block. motion/gate.json checks the actual120-frame rig. review/risk is generated from the real MP4 with the repository's risk-sheet routine and a documented last-frame seek clamp. Neither machine check grades material aesthetics. Independent review and remaining limitations live in review/. Approval remains absent unless the owner later accepts named samples explicitly.
