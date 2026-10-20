#!/usr/bin/env python3
"""Check left/right-hand continuity in a Phase B prompt package before anything is generated.

Video models often put a prop in the wrong hand or let it jump hands between clips.
The prompt contract asks every clip to state, from each character's own side:

  Hands at start — Pip: right hand holds the red paper card; left hand empty.
  Hands at end — Pip: right hand empty; left hand holds the red paper card.

This script reads the package (Markdown, clips headed "Clip N") and reports:
  * a clip that has no start or end hands line while others do,
  * a prop that changes hands between the end of one clip and the start of the next
    (allowed only when the start line says "handoff" or "time cut"),
  * a hand change inside a clip with no beat that passes, swaps, drops or picks it up,
  * a beat sentence that puts a ledger prop in the other hand.

Usage: hand_ledger.py package.md     Exit 0 = consistent, 1 = problems, 2 = bad input.
"""
import re
import sys
from pathlib import Path

CLIP = re.compile(r"^#{1,4}\s*Clip\s+(\d+)\b.*$", re.I | re.M)
LINE = re.compile(r"^\W*Hands at (start|end)\s*[—:-]+\s*(.+)$", re.I | re.M)
ENTRY = re.compile(r"(?P<name>[^:;.]+?):\s*right hand\s+(?P<r>[^;]+?);\s*left hand\s+(?P<l>[^.;\n]+)", re.I)
TRANSFER = re.compile(r"\b(pass(es|ed)?|hands? (it )?over|gives?|takes?|swaps?|switch(es)?|moves? .* to (his|her|their|its) "
                      r"(left|right) hand|drops?|puts? down|sets? down|places?|picks? up|grabs?|catch(es)?|toss(es)?|"
                      r"throws?|releases?|lets? go)\b", re.I)
SIDE = re.compile(r"\b(left|right) hand\b", re.I)


def held(text):
    t = text.strip().lower()
    t = re.sub(r"^(holds|holding|grips|gripping|carries|carrying)\s+", "", t)
    return None if t in ("empty", "is empty", "free", "nothing", "-") else re.sub(r"^(the|a|an)\s+", "", t)


def parse_ledger(line):
    out = {}
    for m in ENTRY.finditer(line):
        out[m["name"].strip()] = {"r": held(m["r"]), "l": held(m["l"])}
    return out


def split_clips(text):
    heads = list(CLIP.finditer(text))
    return [(int(h[1]), text[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)])
            for i, h in enumerate(heads)]


def lint(text):
    problems = []
    clips = split_clips(text)
    if not clips:
        return ["no 'Clip N' headings found"]
    ledgers = []
    for n, body in clips:
        lines = {k.lower(): (v, parse_ledger(v)) for k, v in LINE.findall(body)}
        ledgers.append((n, body, lines))
    if not any(lines for _, _, lines in ledgers):
        return []  # nobody holds anything: nothing to check
    prev_end = None
    for n, body, lines in ledgers:
        for k in ("start", "end"):
            if k not in lines:
                problems.append(f"Clip {n}: missing 'Hands at {k}' line")
            elif not lines[k][1]:
                problems.append(f"Clip {n}: cannot read 'Hands at {k}' line: {lines[k][0].strip()}")
        start = lines.get("start", ("", {}))
        end = lines.get("end", ("", {}))
        # across the cut
        if prev_end and start[1] and not re.search(r"handoff|time cut", start[0], re.I):
            for name, hands in start[1].items():
                if name in prev_end:
                    for side in ("r", "l"):
                        if hands[side] != prev_end[name][side]:
                            problems.append(
                                f"Clip {n}: {name}'s {'right' if side == 'r' else 'left'} hand starts with "
                                f"{hands[side] or 'nothing'} but the previous clip ended with "
                                f"{prev_end[name][side] or 'nothing'}")
        # inside the clip
        beats = LINE.sub("", body)
        if start[1] and end[1]:
            for name, hands in start[1].items():
                if name in end[1] and hands != end[1][name] and not TRANSFER.search(beats):
                    problems.append(f"Clip {n}: {name}'s hands change between start and end, "
                                    f"but no beat passes, swaps, drops or picks anything up")
        # beat sentences that name a ledger prop with a hand it is never in during this clip
        for name, hands in start[1].items():
            for prop in {p for p in hands.values() if p}:
                allowed = {side for led in (start[1], end[1]) for side, p in led.get(name, {}).items() if p == prop}
                key = prop.split()[-1]
                for sent in re.split(r"(?<=[.!?])\s+", beats):
                    if key in sent.lower() and not TRANSFER.search(sent):
                        sides = {m.group(1).lower()[0] for m in SIDE.finditer(sent)}
                        if sides and not sides & allowed:
                            problems.append(f"Clip {n}: beat puts the {prop} in {name}'s "
                                            f"{'left' if 'l' in sides else 'right'} hand, but the hands lines "
                                            f"keep it in the {'right' if 'r' in allowed else 'left'} hand: "
                                            f"\"{sent.strip()[:90]}\"")
        prev_end = end[1] or None
    return problems


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print(__doc__, file=sys.stderr); return 2
    try:
        text = Path(argv[0]).read_text()
    except OSError as e:
        print(e, file=sys.stderr); return 2
    problems = lint(text)
    for p in problems:
        print("ERROR", p)
    print("PASS" if not problems else f"FAIL: {len(problems)} hand continuity problems")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
