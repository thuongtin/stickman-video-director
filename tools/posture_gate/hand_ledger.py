#!/usr/bin/env python3
"""Check left/right-hand continuity in a Phase B prompt package before anything is generated.

Video models often put a prop in the wrong hand or let it jump hands between clips.
The prompt contract asks every clip to state, from each character's own side:

  Hands at start — Pip: right hand holds the red paper card; left hand empty.
  Hands at end — Pip: right hand empty; left hand holds the red paper card.

This script reads the package (Markdown, clips headed "Clip N") and reports:
  * a clip that has no start or end hands line while others do,
  * a prop that changes hands between the end of one clip and the start of the next
    (allowed only when the start line is marked, e.g. "Hands at start (time cut) — ..."
    or "Hands at start (handoff) — ..."),
  * a hand change inside a clip with no beat that passes, swaps, drops or picks it up,
  * a beat sentence that puts a ledger prop in the other hand,
  * a package with no hands lines at all while a beat holds, grabs or carries something,
  * "near hand" / "far arm" wording, which flips meaning when the character turns,
  * a hand taking or holding "it"/"them" in the wrong hand (read as the prop named last),
    or before any prop is named.
Paw, flipper, wing, hoof, claw and fin count as hands for animal characters.

Usage: hand_ledger.py package.md     Exit 0 = consistent, 1 = problems, 2 = bad input.
"""
import re
import sys
from pathlib import Path

CLIP = re.compile(r"^#{1,4}\s*Clip\s+(\d+)\b.*$", re.I | re.M)
# "Hands at start — ..." or "Hands at start (time cut) — ..."
LINE = re.compile(r"^\W*Hands at (start|end)\b([^—:\n]*?)\s*[—:-]+\s*(.+)$", re.I | re.M)
EXCUSE = re.compile(r"\b(handoff|hand-off|time cut)\b[.:,]?\s*", re.I)
# "Name: right hand ...; left hand ..." with the two hands in either order.
# Animal and creature characters: a paw, flipper, wing, hoof, claw or fin is the hand.
LIMB = r"(?:hand|paw|flipper|wing|hoof|claw|fin)"
ENTRY = re.compile(rf"(?P<name>[^:;.]+?):\s*(?P<a>(?:right|left) {LIMB}\s+[^;]+?);\s*(?P<b>(?:right|left) {LIMB}\s+[^.;\n]+)", re.I)
HAND = re.compile(rf"(right|left) {LIMB}\s+(.+)", re.I | re.S)
TRANSFER = re.compile(r"\b(pass(es|ed)?|hands? (it )?over|gives?|takes?|swaps?|switch(es)?|moves? .* to (his|her|their|its) "
                      r"(left|right) hand|drops?|puts?|sets? down|places?|picks?|grabs?|catch(es)?|toss(es)?|"
                      r"throws?|releases?|lets? go|tucks?|hangs?|pockets?|stows?|slides?|lays?|leaves?|receives?|"
                      r"accepts?|snatch(es)?|pulls? out|takes? out)\b", re.I)
# Verbs of holding an object; "holds still", "holds her breath", "holds the pose" are not props.
HOLDING = re.compile(r"\b(?:hold(?:s|ing)?(?! (?:still|on|tight|steady|position|the pose|(?:\w+ )?(?:key )?poses?|(?:his|her|their|its) "
                     r"(?:breath|pose|gaze|ground|head|position)))|grab(?:s|bing|bed)?|grip(?:s|ping)?|"
                     r"clutch(?:es|ing)?|carr(?:y|ies|ying)|picks? up|picking up|wields?|"
                     r"(?:in|with) (?:his|her|their|its|one|both) (?:left |right )?(?:hand|paw|flipper|wing|hoof|claw|fin)s?)\b[^.\n]{0,40}", re.I)
NEAR_FAR = re.compile(rf"\b(near|far|upstage|downstage) (?:arm|{LIMB[3:-1]})s?\b", re.I)
PRONOUN = re.compile(r"\b(it|them)\b", re.I)
CLAUSE = re.compile(r",\s*|;\s*|\s+(?:and|then|while|before|after)\s+", re.I)
SIDE = re.compile(rf"\b(left|right) {LIMB}s?\b", re.I)


def held(text):
    t = text.strip().lower()
    t = re.sub(r"^(holds|holding|grips|gripping|carries|carrying)\s+", "", t)
    return None if t in ("empty", "is empty", "free", "nothing", "-") else re.sub(r"^(the|a|an)\s+", "", t)


def parse_ledger(line):
    out = {}
    for m in ENTRY.finditer(line):
        hands = {}
        for part in (m["a"], m["b"]):
            side, what = HAND.match(part).groups()
            hands[side[0].lower()] = held(what)
        if set(hands) == {"r", "l"}:
            out[m["name"].strip()] = hands
    return out


def split_clips(text):
    heads = list(CLIP.finditer(text))
    return [(int(h[1]), text[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)])
            for i, h in enumerate(heads)]


def lint(text):
    problems = []
    clips = split_clips(text) or [(1, text)]  # a single prompt without a heading is clip 1
    ledgers = []
    for n, body in clips:
        lines = {k.lower(): (q + " " + v, parse_ledger(EXCUSE.sub("", v))) for k, q, v in LINE.findall(body)}
        ledgers.append((n, body, lines))
    for n, body, _ in ledgers:
        for sent in re.split(r"(?<=[.!?;])\s+", LINE.sub("", body)):
            m = NEAR_FAR.search(sent)
            if m:
                problems.append(f"Clip {n}: \"{m.group(0)}\" is ambiguous (it flips when the character turns); "
                                f"name the character's own left or right: \"{sent.strip()[:90]}\"")
    if not any(lines for _, _, lines in ledgers):
        # No ledger at all is fine only when nobody holds anything.
        for n, body, _ in ledgers:
            # quote the beat that holds a real thing: a hand or a timed beat beats style text
            # such as "holds clean key poses" or "speed lines carry the energy"
            sents = [x for x in re.split(r"(?<=[.!?;])\s+", body) if HOLDING.search(x)]
            best = sorted(sents, key=lambda x: (not re.search(rf"\b{LIMB}s?\b", x, re.I),
                                                not re.match(r"\W*\[", x.strip())))
            m = HOLDING.search(best[0]) if best else None
            if m:
                problems.append(f"Clip {n}: a beat has a character holding something (\"{m.group(0).strip()}\") "
                                f"but the package has no 'Hands at start' / 'Hands at end' lines")
        return problems
    prev_end = None
    seen = set()
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
        # (start or end ledger; a prop picked up mid-clip only appears in the end ledger)
        everyone = set(start[1]) | set(end[1])
        for name in everyone:
            props = {p for led in (start[1], end[1]) for p in led.get(name, {}).values() if p}
            for prop in props:
                allowed = {side for led in (start[1], end[1]) for side, p in led.get(name, {}).items() if p == prop}
                key = prop.split()[-1].rstrip("s")  # "four paper cards" also matches "a second card"
                for sent in re.split(r"(?<=[.!?;])\s+", beats):
                    named = {c for c in everyone if c.lower() in sent.lower()}
                    if key in sent.lower() and (not named or name in named):
                        # only the hand named in the same clause as the prop counts:
                        # "opens the door with the left hand and takes out the tea with the right hand"
                        clauses = [c for c in CLAUSE.split(sent) if key in c.lower()]
                        sides = {m.group(1).lower()[0] for c in clauses for m in SIDE.finditer(c)}
                        if sides and not sides & allowed and (n, sent) not in seen:
                            seen.add((n, sent))
                            problems.append(f"Clip {n}: beat puts the {prop} in {name}'s "
                                            f"{'left' if 'l' in sides else 'right'} hand, but the hands lines "
                                            f"keep it in the {'right' if 'r' in allowed else 'left'} hand: "
                                            f"\"{sent.strip()[:90]}\"")
        # "catches it with her left paw": "it" is the ledger prop named last before it in the clip;
        # check that prop's hand, and ask for the name when no prop was named yet
        owners = {}
        for name in everyone:
            for led in (start[1], end[1]):
                for side, p in led.get(name, {}).items():
                    if p:
                        owners.setdefault(p.split()[-1].rstrip("s"), {}).setdefault(name, set()).add(side)
        low_beats, cursor = beats.lower(), 0
        for sent in re.split(r"(?<=[.!?;])\s+", beats):
            for clause in CLAUSE.split(sent):
                at = low_beats.find(clause.lower(), cursor) if clause else -1
                cursor = at if at >= 0 else cursor
                low = clause.lower()
                pron = PRONOUN.search(clause)
                if not (pron and SIDE.search(clause) and (HOLDING.search(clause) or TRANSFER.search(clause))) \
                        or any(k in low for k in owners) or (n, sent) in seen:
                    continue
                before = low_beats[:cursor + pron.start()]
                key = max(owners, key=before.rfind, default=None)
                if key is None or before.rfind(key) < 0:
                    seen.add((n, sent))
                    problems.append(f"Clip {n}: name the prop instead of \"{pron.group(0)}\" "
                                    f"when a hand takes or holds it: \"{sent.strip()[:90]}\"")
                    continue
                named = {c for c in owners[key] if c.lower() in sent.lower()}
                allowed = set().union(*(owners[key][c] for c in (named or owners[key])))
                sides = {m.group(1).lower()[0] for m in SIDE.finditer(clause)}
                if not sides & allowed:
                    seen.add((n, sent))
                    problems.append(f"Clip {n}: \"{pron.group(0)}\" (the {key}) goes in the "
                                    f"{'left' if 'l' in sides else 'right'} hand, but the hands lines keep it in the "
                                    f"{'right' if 'r' in allowed else 'left'} hand: \"{sent.strip()[:90]}\"")
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
