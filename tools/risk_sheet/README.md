# Risk sheet

One PNG per generated clip with frame bursts around the moments its own prompt says are risky. Use it instead of scrubbing the whole clip.

The tool reads the clip's beats and `Hands at start` / `Hands at end` lines. It picks the moments where a named character does one of these:

- passes, grabs or drops a prop
- turns
- reaches overhead
- crosses its arms
- falls, kneels or sits

The time is taken from "at about 1.5s" when a beat gives one; otherwise it is spread across the beat's window. Each moment gets ±0.5 s of frames at 8 per second, plus the hands the ledger expects at that point.

```bash
python3 tools/risk_sheet/risk_sheet.py package.md --clip 2                      # the plan only
python3 tools/risk_sheet/risk_sheet.py package.md --clip 2 --video clip2.mp4 -o out/
python3 tools/risk_sheet/risk_sheet.py package.md --batch clips/ -o out/   # files named ...clip1.mp4
```

Each clip gets two files:

- `clipN-sheet.png`: the red frame is the moment itself.
- `clipN-checklist.md`: one row per moment with an empty OK / FAIL column.

Hands are the character's own: when the character faces the camera, its right hand is on screen left.

The tool does not detect errors. It only puts the frames that matter in front of a person, so it works for any style, including the cartoon and paper characters MediaPipe cannot read.

The plan needs only the standard library. The sheet needs `ffmpeg`, `ffprobe` and Pillow.
