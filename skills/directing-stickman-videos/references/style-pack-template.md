# Style Pack Template

Use this when drafting a new visual style for the skill. One style is one file named by its slug (`chibi-anime.md`, `paper-cutout.md`), not by the next free number. A style pack states how honest its evidence is, what makes the style recognizable, and how it changes the core rules.

## 1. Status

A style's status is the lowest level whose evidence exists. A level covers only the scenes and topics that were tried; a new style never inherits another style's level.

| Level | What it means | Evidence the pack must link |
|---|---|---|
| `research` | References studied, signature checklist written, cast sheets or poses drawn | Sources, checklist, gallery |
| `gated` | Rigs or poses pass `tools/posture_gate/posture_gate.py`; the sample package passes `tools/package_lint/package_lint.py` | Gate report, the lint facts block (`--facts`) |
| `approved` | The owner accepted named samples | The owner's words, the date and what the acceptance covers |
| `core` | Styles 1–4, shipped with the skill (catalog only; a new pack never uses this level) | The catalog entry |

- The setup gate offers the core styles (Styles 1–4, marked `core` in the catalog) and `approved` styles. Offer `research` or `gated` styles only when the user asks for an experimental style, and say which level it is.
- Write the status block at the top of the pack:

```text
Status: gated (2026-10-20). Covers: 3 clips, two characters, cup handoff, 16:9.
Not covered: 9:16, crowds, night scenes.
```

- When a pack is scored, the self-score and an independent reviewer's score are both written down and the lower one counts. A reviewer who did not make the style reads only the samples. Any veto in section 3 keeps the style at `gated` or below.

## 2. Signature checklist

1. **Sources.** At least three different works, films or episodes, not three frames of one. Say what each supports and where the sources run out; do not claim to have seen what was not looked at.
2. **Five signature traits**, each observable in a still frame and tagged:
   - `must`: missing it means the style is not there (for a lacquer style: flat shapes on a dark polished ground);
   - `bonus`: strengthens it;
   - `forbidden`: breaks it (for a minimal style: busy backgrounds).
3. **Nearest neighbour.** Name the closest style already in the catalog or in research and two differences that a viewer can see. Styles that only differ in palette are one style.
4. **How it is drawn, not what is in the pictures.** Keep line, fill, material, light, colour relationships and how the frame is organized. Do not carry over the references' characters, props or layouts. Segment specs name no studio, artist, brand or signature character, and the cast borrows no named character's costume colour combination.
5. **Spec wording.** For each `must` trait, the plain words the segment spec uses to ask for it, repeated verbatim in every clip.

## 3. Review

- Put a sample frame next to the references. Ask: is the style recognizable with the name hidden, and does it differ from the nearest neighbour?
- Optional score for ranking: signature traits 35, material and medium 20, composition and story 15, characters and objects 15, motion 10, technical 5. Veto: signature traits below 25, or characters that read as childish stickers.
- A new style or character direction is shown as three options that differ in composition, not only in colour. When no one can choose, follow the brief and list the other two directions in one line each.

## 4. Sections every pack fills

- Character anchor and cast cards, verbatim text repeated in every clip
- Core rules this style overrides, named by their ID in `core-contract.md` (C1–C18), each with the reason; rules marked "never" there cannot be overridden
- Text policy: `none`, `blank-zone` or `post-overlay`
- Motion cadence: `smooth`, `on-twos` or `stepped`
- Camera moves allowed, following the camera grammar in `storyboard-template.md`
- Style bans and posture limits (moves the rig cannot do)
- Post-production steps
- One sample clip spec that passes `package_lint.py`, with its facts block
- The status block from section 1

The status levels, signature checklist and review rules adapt the style-research protocol of huashu-art-motion (MIT, alchaincyf), where self-scores ran about ten points above independent review.
