# Shared voice continuity — all visual styles

This is the common voice contract for Style 1 Light/Dark, Style 2A, Style 2B and Style 3, plus Style 4 Cozy Storytelling. Voice identity belongs to the video, not to a visual style or a clip. Different videos may choose different voices; every clip of one video must use the same complete approved voice profile. Do not force every project into the accepted male profile.

In a motion-graphics video the narration is its own track: a voice actor reads it, or a speech-synthesis voice renders it. The voice block below is the casting and performance spec for that track, repeated in every segment spec so each segment can be timed and checked on its own.

## Choose once in Phase A

Honor the user's voice choice. If unspecified, propose one suitable voice for approval rather than adding another mandatory setup question. Describe perceived gender/age, accent, timbre, pitch/register, resonance, texture (including breathiness/rasp), delivery/intonation, steady pace, and recording character. Name these in ordinary language, not a list of vague adjectives such as "warm, energetic, same narrator". Summarize the profile in the user's language. Resolve all attributes before producing segment specs; no placeholders in production output.

For example, a male choice can become adult, General American, warm clean baritone, medium-low pitch, gentle chest resonance, no rasp/breathiness, calm conversational delivery, restrained pitch variation, steady pace, close dry studio recording. A bright female choice can instead become adult, General American, clear warm mid-high voice, gentle forward resonance, no rasp/breathiness, lively conversational delivery with controlled pitch variation, steady pace, close dry studio recording. Older, youthful or other requested voices need their own internally coherent profile; they do not inherit male/baritone traits. Alternative profiles are design examples, not separately accepted voices.

## Freeze once in Phase B

Write one self-contained English voice block from the approved profile and copy it **verbatim** into every standalone segment spec, including clip 1. Never abbreviate it to "same narrator", "continue the voice from clip 1", an ellipsis or a speaker label alone. Independent specs must carry their own complete voice instructions.

The following complete male block was accepted by the user after a three-clip listening comparison. Reuse it unchanged when its attributes match the approved choice:

```text
One off-screen adult male narrator throughout. General American accent, warm clean baritone, medium-low pitch, gentle chest resonance, no raspiness or breathiness. Calm conversational delivery, restrained pitch variation, steady speaking pace, and close, dry studio sound. Keep the same vocal timbre, register, accent, pace, and recording quality throughout. Emotional progression belongs to the visuals and music; do not change the narrator's voice or switch to character dialogue.
```

For a different approved voice, compose its own complete block using the same identity/pitch/texture/delivery/recording fields, then freeze that block. Do not append contradictory attributes such as "bright high-pitched youthful voice" to a low baritone or "now shout dramatically" to restrained conversational narration.

## Separate voice, performance and music

- Keep the narrator off-screen and narration audio-only unless the user explicitly approves another arrangement. A change in character gender, age, scene, costume, lighting or visual style does not recast the narrator. No spontaneous lip-synced character dialogue, added speakers or grunts presented as new spoken lines.
- Put escalation, anxiety, triumph, deadpan reaction and cinematic intensity in action, editing, music and SFX. Do not rewrite the narrator's register, timbre, texture, accent, pacing or recording treatment by scene. Natural sentence emphasis and pauses may vary within the frozen delivery, without adopting a new character voice.
- Keep the voice close and dry even in caves or large halls; location reverb belongs to environmental SFX unless another recording treatment was approved. Preserve voice-first mixing. Music/SFX may follow their own approved arc; they do not override this voice contract. Style 3's primitive-percussion or reaction-pause rules change music/timing, not the frozen voice.
- Shorten excessive VO before changing the approved pace to squeeze it into a clip. A global voice change requires a revised Phase A and approval, followed by replacing the block in **all** segment specs and re-recording the whole VO, not just one segment.
- For explicitly approved multi-speaker dialogue, freeze a separate complete profile for each recurring speaker and keep line-to-speaker assignments explicit. Repeat each appearing speaker's full profile in every relevant clip, one line per speaker written as `Voice — Name: <frozen block>` so `tools/package_lint/package_lint.py` compares each speaker separately; a speaker absent from a clip is left out of it rather than named; identity stays consistent per speaker, rather than forcing all characters to sound alike. Do not add multi-speaker dialogue unrequested. For an explicitly silent video, omit speech instead of inserting a default narrator.

## Check and record

Before delivery, compare all spec voice blocks for exact equality (or per-speaker equality for approved dialogue). Check other spec sentences for conflicting voice directions, confirm exact approved spoken lines, and keep speech-bubble/subtitle bans separate from the voice profile.

Record or synthesise the narration in one session with one voice and one set of settings (one take per approved speaker), then cut it to the segment timings. A segment re-recorded later uses the same voice, settings, microphone and room. Check the assembled VO by listening: perceived speaker identity, timbre, register, accent, pace, texture and recording sound. Matching text and screenshots do not prove audio consistency. If segments sound like different people, first look for missing, abbreviated or contradictory voice wording, then for a segment recorded with different settings, and re-record it with everything else held fixed.

Do not claim a voice reference or a particular voice was used when none was chosen.
