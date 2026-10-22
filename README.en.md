<!-- readme:hero -->

<div align="center">

[Tiếng Việt](README.vi.md) · [**English**](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Português do Brasil](README.pt-BR.md)

# AI Stickman Animation Style Library

**Turn an idea into a polished stickman video with a consistent visual style.**

[![GitHub Stars](https://img.shields.io/github/stars/kaomei/stickman-video-director?style=flat-square)](https://github.com/kaomei/stickman-video-director/stargazers)
![MIT License](https://img.shields.io/badge/License-MIT-16a34a?style=flat-square)

</div>

<div align="center">

I'm testing popular stickman animation styles from across the web and sharing the workflows here, free and open source. Install the Skill, give your AI a topic, and get a script, animated storyboards, and prompts for narration and sound effects.

<strong>Next time you want to make a stickman animation, start here.</strong> For **YouTube explainers, TikTok videos, workplace and motivational stories, educational content, and punchy shorts about everyday life.**

</div>

<table width="100%">
<tr>
<td width="50%" align="center">
<strong>Minimalist Monochrome</strong><br>
<a href="#style-gallery"><img src="assets/readme/previews/dark-theme-demo.gif" alt="Minimalist stickman animation with white lines on black" width="90%"></a>
</td>
<td width="50%" align="center">
<strong>Modern Tech</strong><br>
<a href="#style-gallery"><img src="assets/readme/previews/style-2a-demo.gif" alt="Red-beanie stickman with clean tech visuals" width="90%"></a>
</td>
</tr>
<tr>
<td width="50%" align="center">
<strong>Prehistoric Dark Comedy</strong><br>
<a href="#style-gallery"><img src="assets/readme/previews/style-3-demo.gif" alt="Prehistoric stickman story with a comic twist" width="90%"></a>
</td>
<td width="50%" align="center">
<strong>Cozy Storytelling</strong><br>
<a href="#style-gallery"><img src="assets/readme/previews/style-4-cozy-cafe.gif" alt="Expressive stick characters in a colorful everyday setting" width="90%"></a>
</td>
</tr>
</table>

<div align="center">

**4 styles · 6 visual options · 24 experimental styles · Posture gate · Free and open source**

⭐ **Star it now. Next time you make an animation, skip the hunt for prompts.**

[Get started](#quick-start) · [24 new styles](#experimental-styles) · [What this fork adds](#fork-additions) · [Latest updates](#recent-updates) · [Full walkthrough (Chinese)](https://x.com/CrazyKaomei/status/2102311241046008268)

</div>

<!-- readme:demos -->

<a id="style-gallery"></a>

## Find your style

### Style 1: Minimalist Monochrome

A few lines can explain a big idea. On a pure-white or pure-black canvas, characters, props, and accent colors do the storytelling. A good fit for fast, clear explainers.

- **The look:** Round heads, line limbs, consistent stroke weight, and occasional simple expressions. Up to three vivid accent colors distinguish emotions, risks, or actions. Turn anxiety into a cage or attention into a progress bar.
- **Best for:** Science, psychology, motivation, self-management, business breakdowns, and explaining concepts.
- **Which version?** White backgrounds feel clean and direct; choose black backgrounds for stronger contrast, tension, and emotional impact.

| Style 1A: Black on White | Style 1B: White on Black |
|:---:|:---:|
| <!-- demo:light:start --><img src="assets/readme/previews/light-theme-demo.gif" alt="Black stick figure on a pure-white background" width="360"><!-- demo:light:end --> | <!-- demo:dark:start --><img src="assets/readme/previews/dark-theme-demo.gif" alt="White stick figure on a pure-black background" width="360"><!-- demo:dark:end --> |
| White canvas · Black figure | Black canvas · White figure |

---

### Style 2: Modern Pop

In this fork the lead has a short dark buzz cut, dark rectangular glasses, a white short-sleeved button-up shirt, and jeans, on the same body as upstream's lead; upstream's red-beanie, yellow-shirt character is still there if you ask for it. Use a clean tech setting to explain a product, or take the character into bedrooms, streets, and open landscapes for a story.

- **The look:** One recognizable character, two kinds of world. 2A pairs white space and a faint grid with floating glass interfaces and cyan-blue light. 2B uses colorful settings, cinematic lighting, and depth.
- **Best for:** 2A suits AI tools, tech products, tutorials, and feature demos. 2B suits personal growth, everyday situations, adventures, and motivational stories.
- **Which version?** Choose 2A to explain a tool or method; choose 2B to follow a character through an experience.

| Style 2A: Minimal Tech | Style 2B: Cinematic Story |
|:---:|:---:|
| <img src="assets/readme/previews/style-2a-demo.gif" alt="Minimal tech animation with a red-beanie character" width="360"> | <img src="assets/readme/previews/style-2b-demo.gif" alt="Red-beanie character in a colorful cinematic setting" width="360"> |
| White space · Faint grid · Cyan glow | Colorful settings · Cinematic light · Story atmosphere |

The two clips above were made upstream with the red-beanie lead. Here is this fork's default lead, drawn from a code rig that passed the posture gate ([character sheet](docs/lead-character/sheet.png)):

<a id="lead-character-preview"></a>

<p align="center"><img src="docs/lead-character/motion.gif" alt="The default Style 2 lead, a stick figure with a buzz cut, glasses, a white shirt and jeans, walks in and waves" width="480"></p>

<p align="center"><img src="docs/lead-character/sheet.png" alt="Nam's character sheet: four views, outfit locks, seven expressions and seven poses" width="760"></p>

<p align="center"><sub>Nam, the default lead: buzz cut, glasses, white short-sleeved shirt, jeans. Ask for upstream's red-beanie Zeke to use him instead.</sub></p>

---

### Style 3: Prehistoric Sketch / Dark Comedy

Take today's problems back to a world without phones or offices. Caves, animal hides, campfires, and exaggerated expressions turn familiar workplace frustrations and human quirks into stories with a twist.

- **The look:** Rough hand-drawn outlines, white-filled heads, dark stick limbs, animal-hide clothes, and earthy scenery. Character interaction, reaction shots, and comic timing matter. Cast adults, children, or elders to fit the story; every story needn't use the same face.
- **Best for:** Prehistoric what-ifs, workplace satire, observations about human nature, dark comedy, fables, and children's English stories.
- **Why choose it?** For a short setup and an unexpected payoff—especially when modern relationships become absurdly familiar in a prehistoric tribe.

| Example 1: “How Did Humans Get Their First Job?” | Example 2: “Humans Discover Fire” |
|:---:|:---:|
| <img src="assets/readme/previews/style-3-demo.gif" alt="How Did Humans Get Their First Job? animated preview" width="360"> | <img src="assets/readme/previews/style-3-community-fire.gif" alt="Humans Discover Fire, a community-made animation" width="360"> |
| Prehistoric workplace comedy | Fire discovery · Community creation |

---

### Style 4: Cozy Storytelling

A mug you've been saving for a special occasion. A message you feel compelled to answer. An afternoon you finally keep for yourself. Simple characters step into colorful everyday settings, with actions, expressions, and camera work carrying the story.

- **The look:** White-filled round heads, slender bodies, dark stick limbs, and small, natural expressions in full-color 2D cartoon environments. Wide shots establish the place; close-ups catch hesitation or relief; tracking shots keep the story moving.
- **Best for:** Relatable everyday stories, personal growth, relationships, warm moments, habit building, and children's English content.
- **Why choose it?** To help viewers recognize themselves in a small moment. Color and lighting follow the topic: warmth, anxiety, exhaustion, or a fresh start.

| Example 1: Message Anxiety on the Commute | Example 2: Making Time for Yourself |
|:---:|:---:|
| <img src="assets/readme/previews/style-4-cozy-station.gif" alt="A character dealing with message anxiety at a train station" width="360"> | <img src="assets/readme/previews/style-4-cozy-cafe.gif" alt="Taking a break at a sunlit outdoor café" width="360"> |
| Train station · Tracking shots · Emotional close-ups | Outdoor café · Warm light · Everyday gestures |

---

<a id="experimental-styles"></a>

### Experimental styles: 24 new styles

This fork adds 24 styles. Each has its own cast of original characters, its own rules, and a three-clip sample package that passed the posture gate and the package checks. To use one, ask for an experimental style or name it by its key, for example “make it in the `dong-ho` style”. These styles are `gated`: they have not been checked against generated video. Each card is a few seconds of motion rendered from that style's own code-drawn rigs, which passed the posture gate; none of it was made with an AI video model. “See the cast” opens the full cast. [How to pick one and the checking tools](#fork-additions).

<table width="100%">
<tr>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/chibi-anime.gif" alt="Motion clip of the style Chibi Anime" width="360"><br>
<strong>Chibi Anime</strong> · <code>chibi-anime</code><br>
Good for: Everyday-life comedy, study tips, relationship sketches, children's content, reaction-heavy shorts<br>
<a href="docs/style-previews/chibi-anime.jpg">See the cast</a>
</td>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/paper-cutout.gif" alt="Motion clip of the style Paper Cutout / Collage" width="360"><br>
<strong>Paper Cutout / Collage</strong> · <code>paper-cutout</code><br>
Good for: Deadpan comedy; gentle stories and children's English<br>
<a href="docs/style-previews/paper-cutout.jpg">See the cast</a>
</td>
</tr>
<tr>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/whiteboard-doodle.gif" alt="Motion clip of the style Whiteboard Doodle" width="360"><br>
<strong>Whiteboard Doodle</strong> · <code>whiteboard-doodle</code><br>
Good for: Step-by-step explainers, habits and ideas built up piece by piece, light social stories<br>
<a href="docs/style-previews/whiteboard-doodle.jpg">See the cast</a>
</td>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/watercolor-storybook.gif" alt="Motion clip of the style Watercolor Storybook" width="360"><br>
<strong>Watercolor Storybook</strong> · <code>watercolor-storybook</code><br>
Good for: Bedtime stories, children's education, fables, family and nostalgia<br>
<a href="docs/style-previews/watercolor-storybook.jpg">See the cast</a>
</td>
</tr>
<tr>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/ink-wash.gif" alt="Motion clip of the style Ink-Wash / Sumi-e" width="360"><br>
<strong>Ink-Wash / Sumi-e</strong> · <code>ink-wash</code><br>
Good for: Reflective explainers, habits and patience, craft, folk-tale style stories<br>
<a href="docs/style-previews/ink-wash.jpg">See the cast</a>
</td>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/mid-century.gif" alt="Motion clip of the style 1950s Mid-Century Limited Animation" width="360"><br>
<strong>1950s Mid-Century Limited Animation</strong> · <code>mid-century</code><br>
Good for: Satirical explainers, workplace and money topics, small ensembles of character types<br>
<a href="docs/style-previews/mid-century.jpg">See the cast</a>
</td>
</tr>
<tr>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/dong-ho.gif" alt="Motion clip of the style Đông Hồ Folk Print" width="360"><br>
<strong>Đông Hồ Folk Print</strong> · <code>dong-ho</code><br>
Good for: Vietnamese culture, Tết and village stories, gentle fables<br>
<a href="docs/style-previews/dong-ho.jpg">See the cast</a>
</td>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/science-lab.gif" alt="Motion clip of the style Science Lab Explainer" width="360"><br>
<strong>Science Lab Explainer</strong> · <code>science-lab</code><br>
Good for: Science and how-it-works explainers for kids and families, hands-on demos<br>
<a href="docs/style-previews/science-lab.jpg">See the cast</a>
</td>
</tr>
<tr>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/blueprint.gif" alt="Motion clip of the style Engineering Blueprint" width="360"><br>
<strong>Engineering Blueprint</strong> · <code>blueprint</code><br>
Good for: Science, engineering, invention and how-it-works explainers<br>
<a href="docs/style-previews/blueprint.jpg">See the cast</a>
</td>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/cell-biology.gif" alt="Motion clip of the style Cell-Biology Micro-World" width="360"><br>
<strong>Cell-Biology Micro-World</strong> · <code>cell-biology</code><br>
Good for: Immunity, blood, wound-healing and infection explainers for kids and families<br>
<a href="docs/style-previews/cell-biology.jpg">See the cast</a>
</td>
</tr>
<tr>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/retro-space.gif" alt="Motion clip of the style Retro Space-Age Astronomy" width="360"><br>
<strong>Retro Space-Age Astronomy</strong> · <code>retro-space</code><br>
Good for: Space science explainers: orbits, gravity and free fall, the Moon, planets<br>
<a href="docs/style-previews/retro-space.jpg">See the cast</a>
</td>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/youtube-storytime.gif" alt="Motion clip of the style Storytime Animation" width="360"><br>
<strong>Storytime Animation</strong> · <code>youtube-storytime</code><br>
Good for: Funny true stories told by a narrator about their own life<br>
<a href="docs/style-previews/youtube-storytime.jpg">See the cast</a>
</td>
</tr>
<tr>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/us-sitcom.gif" alt="Motion clip of the style Prime-Time Sitcom" width="360"><br>
<strong>Prime-Time Sitcom</strong> · <code>us-sitcom</code><br>
Good for: Dry comedy about everyday life, family and office dynamics<br>
<a href="docs/style-previews/us-sitcom.jpg">See the cast</a>
</td>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/modern-tv-cartoon.gif" alt="Motion clip of the style Modern TV Cartoon" width="360"><br>
<strong>Modern TV Cartoon</strong> · <code>modern-tv-cartoon</code><br>
Good for: Comedy explainers, kids and family stories, small-town adventure told by an ensemble<br>
<a href="docs/style-previews/modern-tv-cartoon.jpg">See the cast</a>
</td>
</tr>
<tr>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/stylized-3d-family.gif" alt="Motion clip of the style Stylized 3D Family Film" width="360"><br>
<strong>Stylized 3D Family Film</strong> · <code>stylized-3d-family</code><br>
Good for: Warm family stories, kids' explainers, holiday stories<br>
<a href="docs/style-previews/stylized-3d-family.jpg">See the cast</a>
</td>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/superhero.gif" alt="Motion clip of the style Superhero Action Cartoon" width="360"><br>
<strong>Superhero Action Cartoon</strong> · <code>superhero</code><br>
Good for: Short action stories, team-up gags, hero explainers, kids' content (one narrator, no character voices)<br>
<a href="docs/style-previews/superhero.jpg">See the cast</a>
</td>
</tr>
<tr>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/dino-world.gif" alt="Motion clip of the style Dino World" width="360"><br>
<strong>Dino World</strong> · <code>dino-world</code><br>
Good for: Kids' dinosaur science, fossils, "how do we know?" stories<br>
<a href="docs/style-previews/dino-world.jpg">See the cast</a>
</td>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/toys.gif" alt="Motion clip of the style Toys Come Alive" width="360"><br>
<strong>Toys Come Alive</strong> · <code>toys</code><br>
Good for: Gentle kids' stories, teamwork and sharing, simple physics (balance, towers)<br>
<a href="docs/style-previews/toys.jpg">See the cast</a>
</td>
</tr>
<tr>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/chu-tieu.gif" alt="Motion clip of the style Chú Tiểu Little Monks" width="360"><br>
<strong>Chú Tiểu Little Monks</strong> · <code>chu-tieu</code><br>
Good for: Mindfulness and kindness lessons, Buddhist-inspired everyday stories, slow-living tips<br>
<a href="docs/style-previews/chu-tieu.jpg">See the cast</a>
</td>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/vn-webcomic.gif" alt="Motion clip of the style Vietnamese Web-Comic in Motion" width="360"><br>
<strong>Vietnamese Web-Comic in Motion</strong> · <code>vn-webcomic</code><br>
Good for: One-joke relatable gags, literal wordplay, neighbourhood slice-of-life<br>
<a href="docs/style-previews/vn-webcomic.jpg">See the cast</a>
</td>
</tr>
<tr>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/voxel-world.gif" alt="Motion clip of the style Voxel Block World" width="360"><br>
<strong>Voxel Block World</strong> · <code>voxel-world</code><br>
Good for: Building and teamwork stories, cause and effect, step-by-step assembly<br>
<a href="docs/style-previews/voxel-world.jpg">See the cast</a>
</td>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/brick-build.gif" alt="Motion clip of the style Brick-Built Town" width="360"><br>
<strong>Brick-Built Town</strong> · <code>brick-build</code><br>
Good for: How parts fit together, cause and effect, gentle kids' stories, small physics jokes<br>
<a href="docs/style-previews/brick-build.jpg">See the cast</a>
</td>
</tr>
<tr>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/tech-illustration.gif" alt="Motion clip of the style Soft Tech Illustration" width="360"><br>
<strong>Soft Tech Illustration</strong> · <code>tech-illustration</code><br>
Good for: Software, AI and productivity explainers, app and onboarding stories, helper-robot stories<br>
<a href="docs/style-previews/tech-illustration.jpg">See the cast</a>
</td>
<td width="50%" align="center" valign="top">
<img src="docs/style-previews/voxel-studio.gif" alt="Motion clip of the style Voxel Studio" width="360"><br>
<strong>Voxel Studio</strong> · <code>voxel-studio</code><br>
Good for: Tech and how-to explainers, teamwork and productivity tips, step-by-step guides<br>
<a href="docs/style-previews/voxel-studio.jpg">See the cast</a>
</td>
</tr>
</table>

<a id="fork-additions"></a>

## What this fork adds

This fork of [kaomei/stickman-video-director](https://github.com/kaomei/stickman-video-director) keeps everything above and adds four things: more styles, a posture gate, a more detailed Golden Hook, and its own Style 2 lead.

### 24 experimental styles

Besides Styles 1–4, the Skill can use 24 experimental styles. Each one has a frozen cast of original characters, its own style rules, and a three-clip sample package.

- **How to pick one:** ask for an experimental style, or name one by its key, for example “make it in the `dong-ho` style”. The Skill offers them only when asked, and tells you each one is `gated`.
- **What `gated` means:** the character rigs passed the posture gate, and the sample package passed the package checks below. These styles have not yet been checked against generated video.
- **Where they live:** `skills/directing-stickman-videos/references/styles/<key>.md`, with the sample package in `styles/samples/<key>.md`. The full list is in the “Experimental styles” table of `references/style-catalog.md`.

The table below lists all 24 again. Motion clips and descriptions are under [Experimental styles](#experimental-styles).

| Key | Style | Good for |
|---|---|---|
| `chibi-anime` | Chibi Anime | Everyday-life comedy, study tips, relationship sketches, children's content, reaction-heavy shorts |
| `paper-cutout` | Paper Cutout / Collage | Deadpan comedy; gentle stories and children's English |
| `whiteboard-doodle` | Whiteboard Doodle | Step-by-step explainers, habits and ideas built up piece by piece, light social stories |
| `watercolor-storybook` | Watercolor Storybook | Bedtime stories, children's education, fables, family and nostalgia |
| `ink-wash` | Ink-Wash / Sumi-e | Reflective explainers, habits and patience, craft, folk-tale style stories |
| `mid-century` | 1950s Mid-Century Limited Animation | Satirical explainers, workplace and money topics, small ensembles of character types |
| `dong-ho` | Đông Hồ Folk Print | Vietnamese culture, Tết and village stories, gentle fables |
| `science-lab` | Science Lab Explainer | Science and how-it-works explainers for kids and families, hands-on demos |
| `blueprint` | Engineering Blueprint | Science, engineering, invention and how-it-works explainers |
| `cell-biology` | Cell-Biology Micro-World | Immunity, blood, wound-healing and infection explainers for kids and families |
| `retro-space` | Retro Space-Age Astronomy | Space science explainers: orbits, gravity and free fall, the Moon, planets |
| `youtube-storytime` | Storytime Animation | Funny true stories told by a narrator about their own life |
| `us-sitcom` | Prime-Time Sitcom | Dry comedy about everyday life, family and office dynamics |
| `modern-tv-cartoon` | Modern TV Cartoon | Comedy explainers, kids and family stories, small-town adventure told by an ensemble |
| `stylized-3d-family` | Stylized 3D Family Film | Warm family stories, kids' explainers, holiday stories |
| `superhero` | Superhero Action Cartoon | Short action stories, team-up gags, hero explainers, kids' content (one narrator, no character voices) |
| `dino-world` | Dino World | Kids' dinosaur science, fossils, "how do we know?" stories |
| `toys` | Toys Come Alive | Gentle kids' stories, teamwork and sharing, simple physics (balance, towers) |
| `chu-tieu` | Chú Tiểu Little Monks | Mindfulness and kindness lessons, Buddhist-inspired everyday stories, slow-living tips |
| `vn-webcomic` | Vietnamese Web-Comic in Motion | One-joke relatable gags, literal wordplay, neighbourhood slice-of-life |
| `voxel-world` | Voxel Block World | Building and teamwork stories, cause and effect, step-by-step assembly |
| `brick-build` | Brick-Built Town | How parts fit together, cause and effect, gentle kids' stories, small physics jokes |
| `tech-illustration` | Soft Tech Illustration | Software, AI and productivity explainers, app and onboarding stories, helper-robot stories |
| `voxel-studio` | Voxel Studio | Tech and how-to explainers, teamwork and productivity tips, step-by-step guides |

No prompt names a studio, brand or famous character. Where a style resembles a well-known look, it matches the genre and material only.

### Posture gate and package checks

Video models often bend a knee the wrong way, stretch a limb, or move a held prop to the wrong hand. These tools catch that before and after generation. They need only Python 3; reading poses from a video also needs `pip install mediapipe opencv-python-headless`.

| Tool | What it checks | Run |
|---|---|---|
| Hand ledger | Every held prop stays in one named hand (the character's own left or right) unless a beat passes it; `Hands at start` / `Hands at end` lines chain from clip to clip. | `python3 tools/posture_gate/hand_ledger.py package.md` |
| Package lint | The whole prompt package: hook placement, the same anchors and voice block in every clip, the five posture negatives, music continuity, no logos or written text, plus the hand ledger. | `python3 tools/package_lint/package_lint.py package.md` |
| Posture gate | Pose tracks from code-drawn rigs or from a video: joint limits, limb length, one-frame pops, balance, arms over the torso or face, left and right hands swapping. `--scene` checks several characters in one shot, such as a hand-off. | `python3 tools/posture_gate/posture_gate.py check track.json` |
| Risk sheet | One image per generated clip with frames around the moments its prompt marks as risky (passes, turns, falls), for a person to review. | `python3 tools/risk_sheet/risk_sheet.py package.md --clip 2 --video clip2.mp4 -o out/` |

The Skill runs the hand ledger and package lint before it hands over the prompts. Details: `tools/posture_gate/README.md` and `references/posture-gate.md`.

### Golden Hook in detail

The first stage of the script, the Golden Hook, now has its own card in the director's proposal: a hook pattern, a first frame that already shows the character mid-action with a visible tension, one hook moment by about two seconds that reads with the sound off, and a first spoken line of four to ten words with no greeting. The hook lives in Clip 1's first frame and first beat; it adds no extra line to the prompt. See “Golden Hook in detail” in `references/storyboard-template.md`.

### Style 2 lead

Style 2 now defaults to a lead with a short dark buzz cut, thick dark rectangular glasses, a plain white short-sleeved button-up shirt with rolled sleeves, and dark blue jeans. The body and face follow upstream's red-beanie lead. The glasses stay on in every shot. Upstream's red-beanie Zeke stays as the alternative: ask for the beanie character and the Skill uses its anchor instead. The character sheet, poses and motion clip are in `docs/lead-character/` (shown under [Style 2](#lead-character-preview)); every pose passed the posture gate, and none of it was made with an AI model.

<!-- readme:advantages -->

## What the Skill does

It plans the writing and the visuals together—not just a stick figure's appearance.

| Part | What you get |
|---|---|
| **Script** | A hook, progression, and payoff, with narration and a reference translation where needed. |
| **Visuals** | Character actions, props, camera moves, transitions, and sound cues. |
| **Continuity** | Character, prop, and narrator profiles, plus transitions between clips. |
| **Framing** | Composition and shot choices adapted to landscape or portrait. |
| **Revisions** | A proposal to approve before the final prompts. |

<!-- readme:output -->

First, review the **director's proposal**: narration, scenes, camera work, and sound design. Once you approve it, get standalone **Gemini Omni Flash video prompts** for each segment, plus stitching, transition, and subtitle notes.

The Skill plans the video and writes the prompts. Flow or another video tool generates the clips; a video editor handles the final assembly and subtitles. No API or MCP setup is required for the Skill.

<!-- readme:install -->

<a id="quick-start"></a>

## Get started

### 1. Install the Skill

Send this to your AI assistant:

```text
Install this Skill for me:
https://github.com/kaomei/stickman-video-director
```

<!-- readme:workflow -->

### 2. Give it a topic

Send a topic, draft, or article. For example:

```text
Make a stickman video called “How Did Humans Get Their First Job?”
```

### 3. Follow the prompts and approve the plan

**Choose settings → Review the proposal → Request changes → Approve and get your prompts.**

If you haven't chosen an aspect ratio or style, the Skill asks. Pick landscape `16:9` or portrait `9:16`, then a style from the gallery. It won't ask again for settings you've already given. Videos default to 60 seconds; say “let's try 30 seconds first” for a shorter test.

Next comes the director's proposal: story structure, narration for each segment, character actions, camera work, and sound design. Review the whole plan and request changes before approving the final video prompts.

**“How Did Humans Get Their First Job?” | Landscape 16:9 · Style 3: Prehistoric Dark Comedy · 30 seconds**

This is the storyboard approved before making the example above. The sample's original narration is preserved:

| Time | Scene and action | Voiceover |
|---|---|---|
| **0–10s: Keeping trouble out** | A caveman drags his stone club into the cave and collapses onto a straw bed. A huge saber-toothed tiger's shadow appears at the entrance. He opens one eye: “Again?” He rolls a boulder across the opening, dusts off his hands, and goes back to bed. End on his satisfied face. | **“Ten thousand years ago, one man finally solved all his problems. He shut them outside.”** |
| **10–20s: The boss finds you** | Just as he closes his eyes, three knocks come from the entrance. The boulder shifts open a crack. The chief leans in, smiling, and offers a spear. The caveman waves it away. Then the chief produces a roasted leg of meat. The caveman sniffs, eyes suddenly wide. Cut outside: spear in hand, he's being nudged toward giant animal tracks. | **“Then someone offered him food… in exchange for a small favor. Congratulations. Employment was invented.”** |
| **20–30s: The price of progress** | He returns to the same cave covered in dust, drops the spear, and holds out his hand for the meat. The chief offers a tiny piece with a professional smile, then presses a whole bundle of spears into his arms, pats his shoulder, and leaves. The caveman looks from the meat to the spears, then slowly at the camera. He lies back down, but the spears jab him upright. | **“The reward got smaller. The workload got bigger. And somehow… they called that progress.”** |

Don't like a line or a scene? Say what to change. Final prompts come only after your approval. This 30-second example produces three roughly ten-second prompts covering characters, action, camera work, narration, and audio.

### 4. Generate the clips and edit your video

Submit the prompts to [Google Flow](https://flow.google.com/) in order. Assemble the clips in CapCut or another editor, adjust the joins, and add subtitles. A 30-second video usually uses three roughly ten-second prompts; a 60-second video uses six.

For a first run, follow the [complete production walkthrough](https://x.com/CrazyKaomei/status/2102311241046008268). There's also a [Flow tutorial](https://x.com/CrazyKaomei/status/2093893997223923822?s=20). Both are in Chinese. The Skill is free; video generation costs and model availability depend on the platform.

<!-- readme:reliability -->

## A few practical tips

<!-- readme:platforms -->

**Landscape or portrait?**

| Format | Good for | Composition |
|---|---|---|
| `9:16` | YouTube Shorts, TikTok, Instagram Reels | Vertical action, a central subject, and mobile-safe framing |
| `16:9` | YouTube and landscape educational videos | Lateral movement, wider scenes, and side-by-side comparisons |

Use it for faceless explainers, history and business topics, personal growth, everyday stories, and product demos. English narration with bilingual subtitles added later also works for English-learning content, short dramas, and close-reading videos. Durations can be any multiple of ten seconds: 30 seconds, 60 seconds, 90 seconds, three minutes, and beyond.

- Keep character, prop, and narrator profiles consistent across the whole video. Choose any voice changes in the proposal first.
- If one clip's character, props, or voice drift, adjust and retest that clip rather than remaking everything.
- Improve the writing without inventing facts, statistics, or product claims.

<a id="recent-updates"></a>

## Latest updates

- **2026-10-22:** New experimental style `tech-illustration` (Soft Tech Illustration): a soft 2.5D tech explainer look with a chibi developer team and a robot sidekick.
- **2026-10-22:** New experimental style `voxel-studio` (Voxel Studio): chibi figures built from small cubes on orange-topped floating platforms in a white studio.
- **2026-10-20:** This fork adds 22 experimental styles, the posture gate with the hand ledger and package lint, and the detailed Golden Hook card. Style 2 now has a buzz-cut, glasses-wearing default lead. See [What this fork adds](#fork-additions).
- **2026-10-15:** Refined the Chinese homepage, installation steps, and examples; added lighter previews and a Star History chart. Skill rules unchanged.
- **2026-10-14:** Added Style 4, Cozy Storytelling, with train-station and café examples.
- **2026-10-13:** Refined Style 1's character descriptions and current-pose constraints.
- **2026-10-12:** Improved shared voice-consistency rules and added prehistoric and community examples.

Already installed? Homepage changes alone don't require a reinstall. Update the Skill if you want Style 4 or installed before the character and voice-rule changes. [Detailed changelog (Chinese)](CHANGELOG.zh-CN.md).

<!-- readme:contribute -->

## What should we add next?

These styles are planned, not available yet:

- **Mixed-media worlds** — Exploring 2D stick figures in richer environments.
- **Style 5: Blackboard Explainer** — Lessons and talks with blackboard interaction.
- **Style 6: Illustrated Storybook** — Fairy tales, fables, and children's stories.
- **Style 7: Graffiti Action** — Fight scenes, short action films, and combos.
- **Style 8: Two-Character Sitcom** — Banter, everyday misunderstandings, and workplace twists.
- **Style 9: Card-Game Adventure** — Level-ups, monster battles, and game-like storytelling.

Suggest a style, share your work, or report a problem in [Issues](https://github.com/kaomei/stickman-video-director/issues). For style requests, include a reference and a topic you'd like to try. For submissions, include the video, style used, and an author link so we can credit you.

## Star History

⭐ **If this library saved you time hunting for prompts or fixing failed generations, consider giving it a Star. It'll be here when you're ready to make your next video.**

I'm [Kaomei](https://x.com/CrazyKaomei). I'll keep testing styles and sharing useful prompts, workflows, and the mistakes worth avoiding—all for free. Less time wrestling with tools, more time for the stories you actually want to tell.

<div align="center">
<a href="https://www.star-history.com/?repos=kaomei%2Fstickman-video-director&amp;type=date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=kaomei/stickman-video-director&amp;type=Date&amp;theme=dark">
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=kaomei/stickman-video-director&amp;type=Date">
    <img src="https://api.star-history.com/svg?repos=kaomei/stickman-video-director&amp;type=Date" alt="GitHub star growth for kaomei/stickman-video-director" width="800">
  </picture>
</a>
</div>

## License

Released under the [MIT License](LICENSE). You can use, modify, redistribute, and use the project commercially. Keep the copyright and license notice when distributing the project or substantial portions of it.

Provided “as is,” without warranty. See [LICENSE](LICENSE) for the full terms.
