# Retro Space-Age Astronomy (draft style reference, slug `retro-space`)

> In this repository: the sample package and its lint facts are `samples/retro-space.md` and `samples/retro-space.facts.md`. Other research files named below (gallery, tracks, gate output, renderer) stay in the project's `style-research/retro-space/` folder and are not part of the skill.

```text
Status: gated (2026-10-20). Covers: 3 clips of 16:9, up to four crew members on screen, microgravity in a station
cabin (a released object that stays put, a catch, a hand-to-hand apple pass, a somersault, stopping on a handrail),
a standing throw on a tiny planet, location cuts cabin -> space -> cabin.
Not covered: 9:16, Moon-surface walking in a package, more than four on screen, character dialogue, night-side
lighting.
```

Evidence: 53 v2 pose tracks (`gallery/tracks/v2/`) pass the shared `posture_gate.py` (rig profile) plus this style's
`zero_g_drift` check: 0 FAIL, 0 warnings (`gallery/gate-output-v2.txt`). The three-shot animatic (10 character tracks)
passes per track and `check_scene` (`motion/motion-gate.txt`). The sample package passes `hand_ledger.py`,
`package_lint.py --clips 3` and `tests/verify-opening-hook.py` (facts block below). All files live in
`/mnt/project-files/style-research/retro-space/`. Draft pack, not yet in the skill catalog; the slug is the name until
it is merged.

## When to use

Space science explainers: orbits, gravity and free fall, the Moon, planets, rockets, light and distance. A poor fit for
anything that must look current or documentary (real missions, real hardware); use Style 4 or Style 2B there.

## Signature checklist

### Sources

| Work | What it supports | Where it runs out |
|---|---|---|
| "Visions of the Future" travel posters (JPL design studio, 2016, public domain) | Flat screen-print colour fields, a limited warm-and-navy palette, grain, big planet circles and poster staging | A modern pastiche, and posters, not animation; full of hand lettering that this style must leave out. Studied from memory of the published set, not a frame study in this thread |
| Space-race propaganda posters (USSR, about 1958-1965) | Flat silkscreen shapes with thin outlines, rounded heroic astronauts, dot stars, rockets and orbit curves as graphic shapes | Political slogans and emblems on almost every poster (none of that is used); stiff heroic poses rather than gentle comedy |
| *The Jetsons* (TV animation, 1962) | Rounded retro-futurist cartoon forms, clear bubble domes, a family-friendly comic tone in animation | A licensed show: none of its characters, costumes, colour combinations or designs are used; its limited animation is not this style's cadence |

Classic painted space art (Chesley Bonestell and the 1950s magazine series) was considered and left out: it is
painterly realism, not flat print.

### Five signature traits

1. `must` Flat, grainy screen-printed colour shapes with a thin dark-navy outline and halftone-dot shading on the shadow
   side instead of gradients.
2. `must` A limited palette: midnight navy, burnt orange, mustard yellow, teal, coral pink and warm cream, with tiny
   cream dot stars.
3. `must` Rounded, padded cartoon astronauts in clear round bubble helmets with the face visible inside and one white
   highlight crescent on the glass.
4. `bonus` Side-on poster staging around big circles: a porthole with the Earth, a ringed planet, the curved top of a
   tiny planet, orbits drawn as dotted cream curves.
5. `forbidden` Any text, letters, numbers, logos, flags, agency marks or mission patches, and any glossy 3D or airbrushed
   gradient.

### Nearest neighbour

`mid-century` (gated, same research round). Visible differences: (1) mid-century bodies are angular geometric shapes on
stick limbs with off-register ink in office interiors; here bodies are rounded padded suits with bubble helmets in a
cabin or in space; (2) mid-century shades with flat offset blocks and moves in held poses on twos; here the shadow side
carries halftone dots, and floating bodies drift smoothly under the microgravity rules. Second neighbour:
`science-lab` (lab interiors, normal gravity, no helmets).

### Prompt wording (verbatim in every clip)

```text
1960s space-age poster illustration, retro-futurist. Flat, grainy screen-printed colour shapes with a thin dark-navy outline, soft rounded chunky forms, halftone-dot shading on the shadow side of each shape instead of gradients, a limited palette of midnight navy, burnt orange, mustard yellow, teal, coral pink and warm cream, with tiny cream dot stars. Characters are rounded cartoon astronauts in clear round bubble helmets with their faces visible inside; each helmet has one white highlight crescent. No 3D, no photorealism, no glossy CGI.
```

Describe the look; never name a studio, an agency, a show or a real poster series in a prompt.

## Cast: one crew, one suit system

Plan the cast in Phase A as one mission crew. Everyone wears the same suit system (bubble helmet, padded suit, chest
box with plain coloured lamps, belt, ribbed rings at elbows and knees, backpack, mitten gloves, boots) and differs in
height, build, suit colour and what is inside the helmet. One shared left/right marker for the whole crew: **a round
mustard-yellow gauge on the right wrist** (the robot has a red lamp there). Sheets: `cast/` (front, both profiles,
silhouette, 12 front and 4 profile expressions each).

The six frozen anchors. Repeat each visible character's anchor verbatim in every clip:

```text
Vega, the tall mission commander: a round clear bubble helmet, inside it a warm brown face with dot eyes, small floating eyebrows and a short black bob; a padded burnt-orange spacesuit with broad rounded shoulders, a narrow waist with a cream belt, a cream chest box with three coloured lamps, ribbed cream rings at the elbows and knees, a cream backpack, cream mitten gloves with a thumb, cream boots, and a round mustard-yellow gauge on her right wrist.
```

```text
Orion, the stout old astronomer: a round clear bubble helmet, inside it a bald head with white side tufts, round glasses, rosy cheeks and a big white beard; a padded cream spacesuit with teal rings at the elbows and knees, a teal belt, a teal chest box with three coloured lamps, a teal backpack, teal mitten gloves with a thumb, teal boots, and a round mustard-yellow gauge on his right wrist.
```

```text
Juno, a ten-year-old cadet, the smallest of the crew: a big round clear bubble helmet, inside it a round face with freckles, rosy cheeks and two brown hair buns; a padded coral-pink spacesuit with white rings at the elbows and knees, a white belt, a white chest box with three coloured lamps, a white backpack, white mitten gloves with a thumb, white boots, and a round mustard-yellow gauge on her right wrist.
```

```text
Rusty, the broad flight engineer: a round clear bubble helmet, inside it a cheerful face with short copper hair and a short copper beard; a bulky mustard-yellow spacesuit with orange rings at the elbows and knees, an orange belt, an orange chest box with three coloured lamps, a navy backpack, navy mitten gloves with a thumb, navy boots, and a round mustard-yellow gauge on his right wrist.
```

```text
Lyra, the slim navigator: a round clear bubble helmet, inside it a face with dot eyes and black hair in a long braid; a slim teal spacesuit with mustard rings at the elbows and knees, a mustard belt, a mustard chest box with three coloured lamps, a white backpack, white mitten gloves with a thumb, white boots, and a round mustard-yellow gauge on her right wrist.
```

```text
Beep, the crew's small helper robot, half Juno's height: a round silver dome head with a dark visor showing two pale-teal dot eyes, a short antenna with a red ball on top and a round grey ear disc on each side, a flat coral collar; a rounded silver body with a round dark dial on its chest and a coral belt, short jointed silver arms and legs, dark-navy mitten hands and boots, and a small red lamp on its right wrist.
```

Shared body rule, once per prompt after the anchors:

```text
Every character keeps exactly two arms and two legs of constant length; a moving limb replaces its previous pose. Each astronaut's round mustard-yellow gauge stays on that astronaut's right wrist in every shot. Expressions change only the eyebrows, eyes and mouth inside the helmet, never the helmet, suit colours or proportions.
```

Front-view proportions: shoulders about 22% of the standing height, the torso outline ending at the shoulder joints, a
narrower waist, resting arms angled out with a gap to the waist (padded suits make fused arms easy to draw). In profile
the neck ring is a flat collar on the shoulders, never a loop hanging below the helmet.

## Core rules this style overrides

| Core rule | Override here | Why |
|---|---|---|
| Balance: the body's weight sits over its support | In the cabin there is no "down": floating frames are exempt from balance and instead obey Newton's first law (below) | Microgravity is the subject; a balance check would demand a floor |
| Faces act freely | Faces live inside the helmet; only eyebrows, eyes and mouth change; the helmet never comes off | The bubble helmet is a signature trait, and a removed helmet in space is wrong science |
| One left/right marker per character | One marker for the whole crew: the gauge on every right wrist | Six suits in one system; one rule is easier for the model and the reviewer |
| Background continuity in one location | Location cuts are planned: cabin -> space -> cabin, each marked `First frame (location cut):` and `Hands at start (time cut)`, with a stitching guide | The science needs both the cabin and an outside view |
| Music | One space-age library theme set in clip 1 and restated with its full instrumentation in every later clip | Keeps the score frozen across clips |
| Arm poses | No near arm raised past about 120° in profile and no overhand throw: it sweeps across the bubble helmet | Gate finding `arm_over_face` (see Posture limits) |

## Microgravity and low gravity

- **Floating rest pose is the neutral body posture**: hips and knees bent about 50°, arms floating forward with bent
  elbows, toes pointed. Not standing, not lying.
- **A floating body only changes speed or direction by pushing or pulling on something** (a handrail, a wall, another
  person). Otherwise it drifts in a straight line at a steady speed. To stop, a hand grabs a handrail and the arm bends.
  No swimming strokes.
- **Loose objects stay where they are released** and keep the hand's speed. Nothing falls to the floor.
- **Limbs moving in free flight move the hips, not the centre of mass**; a somersault turns about the centre of mass at
  a steady rate.
- **Two floating characters never touch helmets.** Stop the moving one with a handrail a hand's width away.
- **Moon surface**: walk and stand normally (balance applies); hops hang about 2.5x longer than on Earth for the same
  height (the square root of 6), with a soft landing.
- Gate mapping: floating frames are `"airborne": true` and `"zero_g": true`; `src/gate.py` adds `zero_g_drift` (with no
  hand on anything, the centre of mass moves straight and evenly). A hand on a rail is a `contacts` entry.
- Science line for scripts: astronauts float because they are falling around the Earth, not because gravity is gone (it
  is about 90% of the ground value at station height).

## Posture limits (from gating 53 poses and the animatic)

- Never raise the near arm through the bubble helmet in profile. Point forward-up at about 120° and tip the head back;
  throws are sidearm, below the shoulder.
- Handrails held for a whole clip sit at shoulder height, the arm straight out below the helmet.
- Reach past the helmet with the far hand below the head line; a far arm straight up behind a big helmet looks like it
  grows out of it.
- Kneel for real: back thigh vertical, shin flat on the ground, front thigh level. Only frames with the knee down are
  `supported`.
- Name which hand pulls or grabs the rail and which way the body goes.
- Props in the glove align with the forearm (wrench) or the gaze (a spyglass touches the helmet glass; it cannot reach
  the eye).

## Props and hands

Follow `posture-gate.md`. Use explicit verbs both the ledger and the model read: "lets go of the red apple", "catches
the red apple with her left hand", "takes the red apple with her right hand; for one held moment both hands are on the
apple". A rail held through a clip is a held prop in the hands lines; two rails held at once get different names
("the handrail", "the low handrail").

## Text policy, cadence and camera

- Text policy: `post-overlay`. Nothing resembling text in any frame (posters of this era are full of type); titles and
  captions are added in post-production over the navy sky or a blank cabin wall.
- Motion cadence: `smooth`. Suits move on ones; floating drifts are slow and even.
- Camera, following the camera grammar in `storyboard-template.md`:
  - Transition moves: hold (default, and always during a catch, a hand-to-hand pass, a somersault or any floating
    stop, because drifting bodies already move), slow pull back (to reveal an orbit or a planet), slow lateral track
    along the cabin, hard cut between cabin and space.
  - Accent moves: at most one per clip and in at most one third of the clips; only a quick push-in on a physics-break
    hit. No orbit, shake or whip pan: with floating bodies they hide which way is "moving".
  - No three inward moves in a row. The sample package uses hold -> hold then slow pull back -> hold.

## Sets and composition

Side-on poster staging, full-body framing. Station cabin: cream padded walls, a big round porthole with the Earth,
panels with only round coloured lamps, short mustard handrails. Space: navy sky with dot stars, a ringed planet, the
curved top of a tiny planet (keep characters on its flattest part). Orbits are dotted cream curves.

## Music

Warm 1960s space-age library music: vibraphone, a soft analog synth arpeggio, brushed drums and a theremin-like glide.
Every later clip says: "the identical vibraphone, analog synth arpeggio, brushed drums and soft theremin-like glide from
clip 1, same tempo and instrumentation". Keep the frozen voice block from `voice-continuity.md`.

## Hooks that fit

Physics break (an object that stays put when released), Scale shock (a planet next to a child astronaut), Partial reveal
(porthole first). The hit is one quiet event on a single vibraphone note; no beat drops, no shake.

## Style bans (negative constraints, added to the shared list)

```text
no text, letters, numbers, logos, flags, insignia or mission patches anywhere, no real space agency marks, no 3D render, no CGI, no photorealism, no gradients or airbrushed shading, no anime style, no extra arms or legs, no duplicate characters, no knees or elbows bending backward, no limbs changing length, no head turned past the shoulders, no swapped left and right hands, no gauge moving to the left wrist, no prop switching hands without a visible pass, no swimming strokes or falling objects in the cabin, no helmet removed, no speech bubbles, no watermark
```

## Post-production

1. Conform the clips to 24 fps and trim duplicate holds so each cut lands on a still moment (a stop on a rail, a held
   apple).
2. Use very short audio crossfades at the cuts; check that the theme keeps one tempo.
3. Add titles and captions in post over the navy sky or a blank wall area; never ask the model for lettering.
4. Before publishing, check on the risky frames: the gauge stays on each right wrist, the released apple does not fall,
   helmets do not touch, nobody swims, and no near arm crosses a helmet.

## Sample package and lint facts

Sample: `samples/retro-space.md` ("Why astronauts float", 3 clips, five crew members, opening hook, hands lines for everyone,
location cuts and a stitching guide). `hand_ledger.py` (shared copy): PASS, and three deliberately broken controls
(`package/control-*.md`: an unmarked cut, a beat naming the wrong hand, "near hand") are all caught
(`package/ledger-output.txt`). `tests/verify-opening-hook.py`: PASS. `package_lint.py --clips 3` (also with `--anchor`
on the gauge line): 0 RED, 0 YELLOW. Facts block (`samples/retro-space.facts.md`, `--verify`: intact):

<!-- package_lint facts: generated, do not edit -->
- package: `package.md` sha256 5ffa5ee58360bf1e
- checked: 2026-10-20
- storyboard rows: none
- prompts: 3
- hand_ledger: PASS
- red: 0
- yellow: 0
<!-- package_lint facts end sha256=35719c2dc0fb6c818b2d3e279194d99b10ff9c9d106eddcc72bd4bbd62f791fc -->

## Catalog entry (draft)

| Style Key | Style Name | Visual Theme | Best For | Character Design |
|---|---|---|---|---|
| **retro-space** | Retro Space-Age Astronomy | 1960s space-poster illustration: flat grainy screen-print shapes, thin navy outline, halftone-dot shading, limited navy, orange, mustard, teal, coral and cream palette, dot stars, ringed planets | Space science explainers: orbits, gravity and free fall, the Moon, planets | One original crew in one suit system: rounded padded suits, clear bubble helmets with faces inside, a mustard gauge on every right wrist |

Status row: `| retro-space | gated | 53 gated pose tracks, 3-shot microgravity animatic with scene check, linted 3-clip package |`.
Setup-gate line (offer only when the user asks for an experimental style): `` `retro-space (Retro Space-Age Astronomy, gated, experimental)`: 1960s space-poster astronauts in bubble helmets for space science ``.

## Generation risks

- The released apple drops to the floor, or floating characters "swim".
- The gauge jumps to the left wrist, or faces move outside the helmets.
- Lettering, flags or agency-like patches creep in because the era's posters are full of them.
- Helmets of two floating characters merge when one drifts up to the other.
