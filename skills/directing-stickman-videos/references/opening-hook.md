# Opening Hook Contract

Use this reference for Stage 1 (Golden Hook) in Phase A and for the first prompt in Phase B. It applies to every style; the style overrides at the end only change intensity and pattern choice.

Source: the hook craft here (what the viewer sees and hears in the first two seconds, and the pattern names) is learned from the MIT-licensed `rediumvex/ai-video-generator-claude` skills (© 2026 Roman Knox), rewritten in our own words for stick figures and our no-text rule. That repository writes prompts for a different video model and has nothing to do with Flow or Omni Flash. Only its hook technique is taken here; none of its prompt-writing rules, prompt order or claims about how a model reads a prompt.

## Why the first two seconds are separate work

- `0–2s` is the gate: viewers decide to stay or swipe before the narration has explained anything. `2–5s` confirms the promise.
- The first frame is the thumbnail. It must already show the subject and a tension, not an empty canvas waiting for something to appear.
- Many viewers start muted. The hook must read with the sound off; voice and sound then strengthen it.
- A spoken question alone is not a hook. "Do you ever feel…?" over a standing figure is a weak opening even when the question is good. The picture carries the hook; the first words name it.

## Hook card (Phase A)

Design the hook before writing the rest of the storyboard. Add this card under "Core message and opening hook" in the Phase A header:

| Field | Requirement |
|---|---|
| Pattern | One name from the pattern menu below. |
| First frame (0.0s) | One sentence a stranger understands without context: who, where, what is already wrong or strange. The character is visible and mid-action. |
| Hook hit | The single visual event that lands between about 0.8s and 2s (impact, reveal, impossible change). One event, not a montage. |
| Sound cue | What the audio does at the hit (silence → impact, whoosh, single note, crisp action sound). No beat drops for calm styles. |
| First spoken line | Starts in the first half-second; about four to ten words; no greeting, channel intro, "in this video" or "today we…". It names the tension the picture shows. |
| Open loop and payoff | The question the hook raises and the clip number that answers it. Every hook is paid off; never bait with a claim the source cannot support. |
| Sound-off check | One line on what a muted viewer understands from the first frame and hit. |

The Clip 1 storyboard row then splits its first beat as `0–2s` hook and `2–3s` confirmation; the `3–7s` and `7–10s` beats are unchanged. For 3–5 minute videos the premise may build over 5–15 seconds, but the first two seconds still follow this card.

## Pattern menu

Choose the pattern that fits the source's actual tension, not the loudest one. Each pattern is written for our characters and our no-text rule.

| Pattern | Mechanism | Stick-figure execution | Best for |
|---|---|---|---|
| Visual metaphor | One image states the whole thesis | First frame: the character already carries, fights or is trapped by the oversized metaphor of the topic | Self-help, business, abstract ideas |
| Reaction before cause | Show the response, hide what caused it | First frame: the character recoils, freezes or drops something while looking off-frame; the cause is revealed at about 2s or in the next beat | Surprising facts, stories, comedy |
| Partial reveal | Camera hides the full subject | Start tight on the character's hands or a detail of the action; pull back by about 2s to reveal the larger, stranger situation | Process, "how it works", mysteries |
| Physics break | Expectation set, then broken | 0–0.8s a normal action; 0.8–2s it goes wrong in a concrete physical way (the cup pours upward, the stairs move backward). Treat it as ordinary; no morphing | Counter-intuitive claims |
| Scale shock | Familiar object at an impossible size | The character stands next to a coin, phone or clock the size of a building; slow push-in so the scale reads | Money, time, attention topics |
| Accent ignition | A monochrome frame gets one burst of color | The figure touches or triggers one prop that ignites in one approved accent color; the color spreads along a line or path, not as liquid morph | Style 1 especially; turning points |
| Before → after cut | Two states, one hard cut | 0–0.8s the problem state; whoosh and hard cut or foreground wipe; the after state. Keep the same character position so it reads as a change | Transformations, tips, fixes |
| Sudden entry | Calm frame, then motion from the edge | Up to one second of a calm but not idle moment, then an object or second figure bursts in from the frame edge or crosses the lens | Danger, interruption, comedy |
| Silence then hit | Audio contrast | 0.3–0.8s near-silence while the first frame already shows the tension; the hit is a single impact synced to a visual cut. Never more than one second of silence or black | Dramatic or serious topics |
| Impossible scene | A world that cannot exist | The character goes about an ordinary task inside an impossible setting (a desk at the bottom of the sea, a staircase over clouds) | Speculative, "what if" topics |
| Satisfying motion | Smooth, precise action holds the eye | One clean physical action shown with care: a line drawn perfectly, a domino chain, a perfect stack. No ASMR macro textures in flat 2D styles | Calm explainers, Style 4 |

### Adapted or excluded from the source library

- Kinetic typography, countdown numbers, bold statistics and "data reveal" counters put words or numbers on screen. Keep them out of the generation prompt. Show the idea with icon-only symbols and, if wanted, list the text as a post-production overlay at the hook timestamp.
- Subliminal three-frame flashes and strobe lighting are unreliable in generated clips and risky for photosensitive viewers; do not use them.
- An extreme close-up stare into the camera conflicts with the idle ban and, for Style 1, the no-face rule. Use a quick turn-and-point toward the viewer instead, followed by action.
- Liquid or shape morphing remains banned in every pattern; express change through concrete action, cuts and wipes.
- Do not name a hook pattern, a "viral" label or a platform inside the prompt; describe only what is seen and heard.

## Carrying the hook into Phase B (Clip 1)

The hook adds no new line or section to the prompt. It lives in the slots `omni-flash-prompt-contract.md` already has:

- The Clip 1 first-frame state is the hook's first frame: the character is present and already moving in the first second.
- The first timed beat of Clip 1 (`[0–3s]`, or `[0–2s]` then `[2–3s]`) times the hook hit, for example "at about 1.5s", then the confirmation.
- The Music/SFX line syncs the sound cue to the hit.
- The quoted dialogue begins with the approved first spoken line; the full voice block is unchanged.
- Clips 2–N are unaffected.

## Ending loop (optional)

For `9:16` shorts that are watched on repeat, the final clip may end on a frame that mirrors the first frame: same composition, character position and key prop, so a replay looks continuous. The discussion question in Stage 5 still plays over it. Name this choice in Phase A and in the stitching guide. Do not use it when the ending must show a changed state the story depends on.

## Composition by ratio

- `9:16`: place the first-frame subject and the hook hit in the central safe area, away from the top and bottom bands that platform interface covers. Keep the key action in the upper two thirds.
- `16:9`: the hook can stage across left and right, but leave clean space on one side if a post-production title will sit there.

## Style overrides

- Style 1: prefer Accent ignition, Visual metaphor, Physics break or Scale shock; one accent color carries the hit. The figure stays monochrome.
- Style 2A: hooks can use the glass interface elements as the oversized or broken object; still no text on them.
- Style 2B: cinematic environments allow Partial reveal and Impossible scene with lighting changes as the hit.
- Style 3: the cold open is the joke's setup. Use Reaction before cause, Sudden entry or a deadpan Visual metaphor; a held deadpan look counts as the hit. Do not force a loud sound cue.
- Style 4: keep hooks gentle. Prefer Partial reveal, Reaction before cause and Satisfying motion; the sound cue is a soft action sound or single note, not an impact or bass hit. The first segment's setting must already be recognizable in the first frame.

## Hook checks

- The hook card is complete and names one pattern.
- The first frame shows the character mid-action with a visible tension; no empty canvas, slow fade-in or "an element appears" opening.
- One hook hit lands by about 2s and is synced to a sound cue suited to the style.
- The first spoken line starts within the first half-second, is about four to ten words, and contains no greeting or channel intro.
- A muted viewer understands the tension from the picture alone.
- The open loop is paid off in a named clip, and the hook does not claim anything the source does not support.
- No words, numbers, counters or text cards appear in the hook; any such text is a post-production overlay.
- No morphing, strobe or subliminal flashes; silence or black lasts no longer than one second.
- Clip 1's first-frame state and first timed beat carry the hook, with the hit timed at about 2s or earlier; no prompt carries a separate `Opening hook:` line.
