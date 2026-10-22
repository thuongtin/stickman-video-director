# Embroidered linen / May

Status: gated (22 October 2026), only for the tested 20-second, one-character, right-facing pickup/carry/place scene with three camera shots. The original gesture test remains motion-insufficient. Not owner acceptance, production approval or catalog promotion.

Base: main c3f63c98c66912d553368438aafba893a791d224, including Historical Cartoon Style 5 and the code-motion-graphics workflow. Read current core contract, style-pack template, style catalog and segment contract before this study. Nothing in the historical Flow wording is carried forward.

## Current material, composition and coverage

Continuous unbleached linen, directional thread fills, short edge stitches and shallow fibre highlights. The action figure, furniture, ball and basket share one flat textile field. No glass translucency, lead network, separate paper pieces, stuffed volume or manufacturing claim.

Three initial image-generated compositions were actually inspected before code: (1) a left-side figure balancing one larger sprig on the right, (2) a centred bow framed by smaller plants, (3) an advancing diagonal pose with asymmetric plants and wind marks. Option 1 established the quiet, separated staging; the other two remain alternatives, not additional implemented actions. The later three-shot action storyboard precedes the action code and replaces the sprig scene with a meaningful pickup/carry/place task.

Current tested action: one right-facing side-view character, world-space locomotion, visible paired grip/lift, constrained carry, placement/release, closing steps into support stances and three motivated camera shots. The 20-second silent render has 480 actual frames at 24 FPS, organized as two ten-second segments. Eight decoded action milestones are selected from this same video; their number comes from scene coverage, not a quota.

The front-view, empty-hand, 120-frame sprig gesture study is historical only. Its seven snapshots include identical start/rest images, and its narrow gate results do not transfer to this action. See review/original-readme.md and the original files for that superseded scope.

Research covers three distinct museum objects from one institution. See research.md for the actual visual coverage and limits. No reference photograph, character, motif or layout is copied into the artwork. Both generated concept artifacts were visually opened before their corresponding code was written.

The current full and per-segment posture checks and the two-segment package fixture pass. Independent review inspected all 480 decoded final frames sequentially, both risk sheets and selected full-size moments. See action/review/final-review.md. Numerical invariants alone do not prove visual contact, convincing weight or material fidelity.

## Nearest neighbours and visible differences

Closest existing directions are paper cutout and stitched/plush toy studies. Compared with paper cutout, this scene has directional thread rows and short edge stitches rather than solid paper fills or cut fibre edges, and a continuous woven ground rather than separated hovering layers. Compared with plush, the bodies stay flat and show no stuffing, volumetric pile or round toy mass. Compared with the preceding glass study, there is no lead network, transmitted light or glossy pane gradient. These are drawing and material differences, not palette changes.

## Known visual limits

The orderly thread rows and geometric panels look more cord-like than the concept's soft, irregular fibre relief. Facial stitching, hair and mitten hands are approximations. The gait is deliberately constrained and mechanically regular, with modest weight transfer. Detailed fingers, turns, running, jumping, multi-character handoffs, rear views, actual textile physics, voice/audio and production acceptance remain untested.

## Five observable signature traits

1. `must`: continuous unbleached linen with visible warp and weft. Spec wording: “continuous unbleached linen with visible perpendicular warp and weft”.
2. `must`: directional short thread rows follow each shape. Spec wording: “directional satin-like thread rows”.
3. `must`: stitch segments define edges rather than a black cartoon outline. Spec wording: “short blanket-like edge stitches”.
4. `bonus`: restrained fibre highlights and shallow stitch shadows, rather than heavy cast shadows or polished shine.
5. `forbidden`: glass panes, paper-cut edges, floating paper layers, stuffed toy volume or copied museum motifs.

The required phrases belong in every segment's Style paragraph. Inspect full-resolution frames as well as thumbnails: tiny stitches may disappear when reduced.

## Action character anchor and cast card

May is an original adult-proportioned embroidered figure with a softly oval linen face, short swept brown thread hair, small brown knot-like eyes, a quiet stitched smile, a long indigo tunic, slender ochre trousers, brown shoes and ivory mitten-shaped hands. Two arms and two legs. A rust thread loop marks only May's own right wrist; in the right-facing side view, the own-right arm and leg are nearer the camera.

Exactly one character. The action rig is tested separately from the earlier front-view gesture rig. The reference photographs provide material vocabulary, not a borrowed character, costume or prop layout.

## Core rules and limits

- C3: only the prospective audio fixture changes instrumentation to a quiet warm bed. The continuity requirement is retained. No actual audio is rendered or claimed tested.
- C9: text policy `none`; no scene lettering or post-overlay.
- C14: a short action arc of approach, acquire, transport and place, rather than a five-stage teaching narrative.
- C15: motion cadence `smooth`, sampled at 24 FPS for the final action render; no dialogue in the actual silent demo. The final scene has two ten-second segments. The draft is 12 FPS. Holds serve a visible foot plant, grip or release, not a static replacement for action.
- C16: locked wide shot, motivated close pickup cut and medium horizontal tracking. No orbit, shake, Dutch tilt or reversing screen direction. Cuts preserve the same world-space action.
- C5 and C6 only gain limits: one carrying character, two hands on one prop, no handoff, no demanding camera rotation during body action.
- No rule marked “never” is overridden. The experimental fixture is not represented as an owner-approved production Phase B.

## Drawing, post-production and coverage

Original procedural strand fills and line stitching are rendered with Pillow. The action scene uses a deterministic timeline, two-link inverse kinematics, explicit world-space foot plants, paired grip offsets and a separate camera transform. These are drawn 2D mechanisms, not simulated physical cloth or 3D collision avoidance.

Post-production order: render numbered frames, encode H.264, inspect metadata and full decode, gate exported pose tracks, inspect risky moments and the whole action progression. No text overlays or audio pass are performed. The original pose samples and first animatic remain historical; they never substitute for reviewing a changed final file.

Style bans: no skin/background gaps at the collar, no hidden far-hand grip presented as visibly two-handed, no floor sliding, no moving through furniture without a clear depth lane, no ball teleport, no frame-cut reset of the carry. Unsupported moves include turning around, side switching, running, jumping, actual handoffs and physically simulated textile deformation.

## Review and scoring

The historical static sample had an independent score of 71/100 and specific material weaknesses; that is not the action revision's score or acceptance. The first action animatic required staging, contact visibility and gait-transition fixes. Its review is preserved under action/review/. The final action self-score is 74/100 and independent score is 77/100; the lower 74 counts. No signature veto was found. See action/review/final-review.md for breakdowns and limitations. These scores do not establish owner acceptance or production readiness.

Evidence: [full posture gate](action/review/demo-full-gate.json), [segment 1 gate](action/review/demo-clip1-gate.json), [segment 2 gate](action/review/demo-clip2-gate.json), [lint facts](action/sample.facts.md), [contact invariants](action/review/demo-invariants.json), [actual decoded milestones](action/gallery/contact-sheet.jpg).
