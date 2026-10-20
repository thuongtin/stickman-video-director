# Wave 1 — examples, Style 2 anchor, density and hands

2026-10-20. Prompt-text update only; no new Flow generations.

## What changed

- `examples.md`: both examples now pass `tools/posture_gate/hand_ledger.py` (before: FAIL, 3 problems on `main` fd44321). Every clip carries `Hands at start` / `Hands at end` lines and the posture negatives. The Style 1 example uses the current Classic Dark anchor verbatim; Clip 1 follows `opening-hook.md` (hook card in Phase A, `Opening hook:` line, mid-action first frame). Abstract morphs ("dot splits into hundreds of lines", B "separates into line components") are replaced by concrete actions and cuts. The Style 2A example no longer puts "BONK!" or a quoted phrase on screen, names the hand that holds the light-pen, and introduces the pen from a pocket instead of an unmentioned backpack. Narration is unchanged.
- Style 2: clips 2–N repeat the full clip 1 anchor instead of the "The same … …" short form. SKILL.md and the contract said "smooth knit"; all three files now say "smooth rounded knit".
- Style 1 anchor: "the right arm" is now "the character's own right arm".
- `storyboard-template.md`: Hands column; "shape morph" and "fluid" removed from the device list; posture budget (one demanding body action per character per beat, not paired with camera shake/orbit/tilt).
- `hand_ledger.py`: spoken narration (`(VO: "...")`, curly-quoted dialogue) is no longer read as a beat, which removed two false positives on the examples.

## Evidence boundary

- `tests/verify-examples.py` checks prompt text only.
- The full Style 2 anchor in clips 2–N and the "character's own right arm" wording have not been compared on Flow.
- The posture budget is a design choice from the posture-gate and style-research findings. It has not been measured as a cause of fewer generated errors.
