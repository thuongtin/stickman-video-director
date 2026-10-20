# Flow benchmark

These are twelve fixed clips for checking, on Flow itself, whether the skill's prompts keep hands, bodies and characters right. Every clip comes from a package that already passes `package_lint.py`. Each one contains a moment that video models often get wrong:

- a prop passing between hands
- a turn
- a fall
- two or three characters in one frame

| Set | Clips | What it stresses |
|---|---|---|
| `style1-dark` | 1, 4, 5 of the Style 1 example | letting go of a cord and turning; a second figure trips and rolls; grabbing and dropping vines |
| `style2a` | 1–3 of the Style 2A example | leap into a glass ceiling; a pen from the right pocket into the right hand; a hand on a vault ring |
| `paper-cutout` | sample clips 1–3 | three characters; a balloon passed from one character's right hand to another's |
| `chibi-anime` | sample clips 1–3 | short arms; several cast members in one frame; a teddy-bear handoff |

## Generating (Flow)

1. Open `prompts.md`. It is regenerated from the source packages with `python3 tests/flow-benchmark/kit.py prompts -o tests/flow-benchmark/prompts.md`.
2. Use the same settings for every clip: Omni Flash, 16:9, 720p, one output, no reference image.
3. Paste one prompt per generation, and save the clip with the name the list gives, e.g. `paper-cutout-clip2.mp4`.
4. Note the Flow asset ID and the model version.

## Reviewing

```bash
python3 tests/flow-benchmark/kit.py review path/to/clips/ -o review/
```

This makes a risk sheet and a checklist for every clip it finds, plus `review/results.csv` with one row per clip.

For each clip:

1. Look at the clip's sheet.
2. Mark each column of its `results.csv` row `ok` or `fail`:
   - hands match the sheet
   - no extra or missing limbs
   - joints bend the right way
   - same character design as clip 1
   - no words on screen
   - hook lands by 2s (clip 1 only)
   - same voice as clip 1 (needs listening)
3. Add a note for every `fail`.

Record the outcome in `tests/reports/` with the date, the Flow model version, the asset IDs and the results table.

A style pack moves from `gated` to `flow-tested` only on this evidence (`style-pack-template.md`). The sheets show the moments that matter; the judgement in each cell is a person's.
