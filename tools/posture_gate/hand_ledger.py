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
  * a hand change inside a clip with no beat sentence about that prop that passes, swaps,
    drops or picks it up, and a hand left empty with no beat that lets go of the prop,
  * "with both hands" while one hand holds another prop all clip,
  * one prop in two characters' hands in the same hands line,
  * a beat sentence that puts a ledger prop in the other hand,
  * a package with no hands lines at all while a beat holds, grabs or carries something,
  * "near hand" / "far arm" wording, which flips meaning when the character turns,
  * (warning) an unlisted prop put in a hand the hands lines keep empty,
  * (warning) a pass that names no receiving hand, and a prop changing hands that the beats never name,
  * a hand taking or holding "it"/"them" in the wrong hand (read as the prop named last),
    or before any prop is named.
Spoken narration ("(VO: "...")" and curly-quoted dialogue) is not read as a beat.
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
LIMB = r"(?:hand|paw|flipper|wing|hoof|claw|fin|glove|mitten|mitt|fist|palm)"
ENTRY = re.compile(rf"(?P<name>\s*(?:(?:Mr|Mrs|Ms|Dr|St)\.\s*)?[^:;.]+?):\s*(?P<a>(?:right|left) {LIMB}\s+[^;]+?);\s*(?P<b>(?:right|left) {LIMB}\s+[^.;\n]+)", re.I)
HAND = re.compile(rf"(right|left) {LIMB}\s+(.+)", re.I | re.S)
TRANSFER = re.compile(r"\b(pass(es|ed)?|hands (it )?over|hand it over|hands (?:\w+ )?(?:the|a|an|it|her|his|them)|gives?|takes?|swaps?|switch(es)?|moves? .* to (his|her|their|its) "
                      r"(left|right) hand|drops?|puts?|sets? (?:\S+ ){0,3}?down|places?|picks?|grabs?|catch(es)?|toss(es)?|"
                      r"throws?|releases?|lets? go|tucks?|hangs?|pockets?|stows?|slides?|lays?|leaves?|receives?|"
                      r"accepts?|snatch(es)?|pulls? out|takes? out)\b", re.I)
# Verbs of holding an object; "holds still", "holds her breath", "holds the pose" are not props.
HOLDING = re.compile(r"\b(?:hold(?:s|ing)?(?! (?:still|on|tight|steady|position|the pose|(?:\w+ )?(?:key )?poses?|(?:his|her|their|its) "
                     r"(?:breath|pose|gaze|ground|head|position)))|grab(?:s|bing|bed)?|grip(?:s|ping)?|"
                     r"clutch(?:es|ing)?|carr(?:y|ies|ying)|picks? up|picking up|wields?|"
                     rf"(?:in|with) (?:his|her|their|its|one|both) (?:left |right )?{LIMB}s?)\b[^.\n]{{0,40}}", re.I)
# verbs that let go of a prop: a hand that ends empty needs one ("sets the brush down")
RELEASE = re.compile(r"\b(pass(es|ed)?|hands (it )?over|hand it over|hands (?:\w+ )?(?:the|a|an|it|her|his|them)|gives?|"
                     r"swaps?|switch(es)?|moves?|drops?|puts?|sets?|places?|toss(es)?|throws?|releases?|lets? go|"
                     r"tucks?|hangs?|pockets?|stows?|slides?|lays?|leaves?|rests?|lowers? .* (?:onto|on|into)|offers?)\b", re.I)
BOTH = re.compile(rf"\b(?:both|two) {LIMB}s\b", re.I)
# description lines that are not actions ("Props: ... wrapped in green leaves")
STATIC = re.compile(r"^\W*(?:output|style(?: and environment)?|characters?|props?|composition|audio|voice|dialogue|"
                    r"camera|lighting|palette|first frame)\b[^:\n]{0,40}:.*$", re.I | re.M)
# timed beat lines, "- [3-7s] ..."
TIMED = re.compile(r"^\s*[-*]?\s*\[[^\]\n]*\d[^\]\n]*\].*$", re.M)
NEAR_FAR = re.compile(rf"\b(near|far|upstage|downstage) (?:arm|{LIMB[3:-1]})s?\b", re.I)
PRONOUN = re.compile(r"\b(it|them)\b", re.I)
CLAUSE = re.compile(r",\s*|;\s*|\s+(?:and|then|while|before|after|as|when|until|but)\s+", re.I)
SIDE = re.compile(rf"\b(left|right) {LIMB}s?\b", re.I)
# a prop tucked under or carried in an arm is on that side: "tucks the box under his left arm"
ARM_SIDE = re.compile(r"\b(?:under|in|with|beneath) (?:his|her|their|its|the|one) (left|right) (?:arm|armpit|elbow)s?\b", re.I)
# what may come before a clause's subject: list marks, "[3-7s]", a stripped "(VO: ...)", ", and then"
LEAD = re.compile(r'^[\W_]*(?:\[[^\]]*\][\W_]*)?(?:""[\W_]*)?(?:(?:and|but|so|then|now|finally|meanwhile|suddenly)\s+)*')
NOT_BEAT = re.compile(r"^\W*(?:negative|negatives|avoid|do not|don't)\b.*$|[^.!?\n]*\?", re.I | re.M)
# looking at, pointing at or touching a prop is not holding it
POINTING = re.compile(r"\b(?:point|look|gesture|nod|wave|stare|glance|tap|touch|poke|wag)(?:s|es|ed|ing)?\b", re.I)
GRASP = re.compile(r"\b(?:hold|grab|grip|take|catch|pick|carr(?:y|ie)|clutch|lift|raise|wave[sd]? (?:the|a|an|her|his))", re.I)
# a part of a prop names the prop: "takes the string" is the balloon, "the handle" the bag
PARTS = {"string": ("balloon", "kite", "yo-yo"), "strap": ("bag", "backpack", "camera", "satchel"),
         "handle": ("bag", "cane", "umbrella", "suitcase", "briefcase", "mug", "cup", "basket", "bucket", "pan",
                    "kettle", "racket", "broom"), "leash": ("dog", "puppy"), "stick": ("lollipop",)}
# "a pencil in her right hand": an object put in a hand, for props the hands lines never list
OBJ_IN_HAND = re.compile(rf"\b(?:a|an|the|his|her|their|its)\s+((?:[\w-]+\s+){{0,3}}?[\w-]+)\s+(?:still\s+)?in\s+"
                         rf"(?:his|her|their|its|the|one)\s+(left|right)\s+{LIMB}\b", re.I)
NOT_PROPS = {"face", "chin", "head", "cheek", "hair", "pocket", "hand", "paw", "arm", "nose", "mouth", "ear", "eye",
             "hip", "waist", "lap", "chest", "belly", "tail", "string", "handle", "strap"}
# sentence breaks, but not after "Mr." / "Dr." in a name
SENT = re.compile(r"(?<!\bMr\.)(?<!\bMs\.)(?<!\bDr\.)(?<!\bSt\.)(?<!\bMrs\.)(?<=[.!?;])\s+|\s*\n\s*")


def keys(prop):
    """Words that name a prop in a beat: its last word ("four paper cards" -> "card") and its parts."""
    # "shoulder pole (with baskets)": a Hands line can list parts that name the prop in beats
    inner = re.findall(r"\(([^)]*)\)", prop.lower())
    words = [w.rstrip("s") for w in re.sub(r"\([^)]*\)", " ", prop.lower()).split()] or ["?"]
    out = {words[-1]}
    for part in inner:
        out |= {item.split()[-1].rstrip("s") for item in re.split(r",|\band\b|\bwith\b", part) if item.split()}
    out |= {part for part, objs in PARTS.items() if any(o in words for o in objs)}
    out |= {w for w in words if words[-1] in PARTS and w in PARTS[words[-1]]}  # "balloon string" is a balloon
    return out


def mentions(text, prop):
    low = text.lower()
    ks = keys(prop)
    # "the phone" names the smartphone, "the ball" the basketball
    # whole words only ("mug" is not in "smug"), allowing plural and short endings ("cups", "glasses")
    return any(re.search(rf"(?<!\w){re.escape(k)}\w{{0,3}}(?!\w)", low) for k in ks) or any(len(w) >= 4 and k.endswith(w) and k != w
                                           for w in set(re.findall(r"\w+", low)) for k in ks)


def name_at(name, text):
    """Where a character's name appears as a whole word, matching case ("Ti" is not "Timed",
    "May" is not "may", "Bo" is not "both"); -1 if it does not."""
    m = re.search(rf"(?<!\w){re.escape(name)}(?!\w)", text)
    return m.start() if m else -1


def sentences(text):
    return SENT.split(text)


def hand_owners(sent, cast, state=None):
    """Each clause of a sentence with the hands it names and whose they are:
    "Bean's left hand" is Bean's; "her right hand" belongs to the clause's subject (the first
    character it names, else the subject of the nearest earlier clause, else of the last sentence
    that named someone, carried in `state`); None if nobody is named yet."""
    state = {} if state is None else state
    out, subject, last = [], None, None
    for clause in CLAUSE.split(sent):
        low = clause.lower()
        found = sorted((name_at(c, clause), c) for c in cast if name_at(c, clause) >= 0)
        if re.match(r"\s*(?:who|whose)\b", low) and last:  # "passes it to Bo, who takes it" is Bo
            subject = last
        elif found and (subject is None or found[0][0] <= LEAD.match(low).end()):
            subject = found[0][1]  # a name opening the clause; "takes the bear from Kai" keeps its subject
        if found:
            last = found[-1][1]
        hands = []
        for m in sorted([*SIDE.finditer(clause), *ARM_SIDE.finditer(clause)], key=lambda m: m.start()):
            owner = next((c for c in cast if re.search(rf"(?<!\w){re.escape(c)}'s(?:\s+[\w-]+){{0,2}}$",
                                                       clause[:m.start()].rstrip())),
                         subject or state.get("subject"))
            hands.append((m.group(1).lower()[0], owner))
        for m in BOTH.finditer(clause):  # "with both hands" is each hand
            owner = subject or state.get("subject")
            hands += [("r", owner), ("l", owner), ("b", owner)]
        if POINTING.search(clause) and not GRASP.search(clause):
            hands = []  # "points at the jar with her right hand" holds nothing
        out.append((clause, hands))
    if subject:
        state["subject"] = subject
    return out


def attribute(beats, cast):
    """hand_owners for every sentence of a clip, in order, so "her" can reach back a sentence."""
    state = {}
    return [(sent, hand_owners(sent, cast, state)) for sent in sentences(beats)]


def excerpt(sent):
    """A beat as quoted in a report, without the emptied "(VO: ...)" placeholder."""
    return re.sub(r'""\s*:?\s*', "", sent.strip())[:90]


# Spoken lines are heard, not acted: "(VO: "...")" and curly-quoted dialogue are left out of the check,
# so "your mind is already carrying a hundred disasters" or "it begins to open" is not read as a beat.
SPOKEN = re.compile(r'\(VO:\s*"[^"\n]*"\)|“[^”\n]*”', re.I)


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


def lint(text, warnings=None):
    problems = []
    text = SPOKEN.sub('""', text)
    clips = split_clips(text) or [(1, text)]  # a single prompt without a heading is clip 1
    ledgers = []
    for n, body in clips:
        lines = {k.lower(): (q + " " + v, parse_ledger(EXCUSE.sub("", v))) for k, q, v in LINE.findall(body)}
        ledgers.append((n, body, lines))
    for n, body, _ in ledgers:
        for sent in sentences(LINE.sub("", body)):
            m = NEAR_FAR.search(sent)
            if m:
                problems.append(f"Clip {n}: \"{m.group(0)}\" is ambiguous (it flips when the character turns); "
                                f"name the character's own left or right: \"{excerpt(sent)}\"")
    if not any(lines for _, _, lines in ledgers):
        # No ledger at all is fine only when nobody holds anything.
        for n, body, _ in ledgers:
            # quote the beat that holds a real thing: a hand or a timed beat beats style text
            # such as "holds clean key poses" or "speed lines carry the energy"
            sents = [x for x in sentences(body) if HOLDING.search(x)]
            best = sorted(sents, key=lambda x: (not re.search(rf"\b{LIMB}s?\b", x, re.I),
                                                not re.match(r"\W*\[", x.strip())))
            m = HOLDING.search(best[0]) if best else None
            if m:
                problems.append(f"Clip {n}: a beat has a character holding something (\"{m.group(0).strip()}\") "
                                f"but the package has no 'Hands at start' / 'Hands at end' lines")
        return problems
    last_seen = {}
    seen = set()
    for n, body, lines in ledgers:
        for k in ("start", "end"):
            if k not in lines:
                problems.append(f"Clip {n}: missing 'Hands at {k}' line")
            elif not lines[k][1]:
                problems.append(f"Clip {n}: cannot read 'Hands at {k}' line: {lines[k][0].strip()}")
        start = lines.get("start", ("", {}))
        end = lines.get("end", ("", {}))
        # one prop in two characters' hands at once
        for k in ("start", "end"):
            holders = {}
            for name, hands in lines.get(k, ("", {}))[1].items():
                for p in hands.values():
                    if p:
                        holders.setdefault(p, set()).add(name)
            for p, who in holders.items():
                if len(who) > 1:
                    problems.append(f"Clip {n}: the {p} is in {' and '.join(sorted(who))}'s hands at the {k} "
                                    f"at once; after a pass, empty the giver's hand (two separate props need "
                                    f"different names, e.g. \"{sorted(who)[0]}'s {p}\")")
        # across the cut, against each character's last hands line (they may skip a clip)
        if start[1] and not re.search(r"handoff|time cut", start[0], re.I):
            for name, hands in start[1].items():
                if name in last_seen:
                    for side in ("r", "l"):
                        if hands[side] != last_seen[name][1][side]:
                            problems.append(
                                f"Clip {n}: {name}'s {'right' if side == 'r' else 'left'} hand starts with "
                                f"{hands[side] or 'nothing'} but {name} ended clip {last_seen[name][0]} with "
                                f"{last_seen[name][1][side] or 'nothing'}")
        # inside the clip
        # the negative list ("no prop switching hands without a visible pass") and review
        # questions are not beats
        beats = NOT_BEAT.sub("", LINE.sub("", body))
        if start[1] and end[1]:
            sents = sentences(STATIC.sub("", beats))
            for name, hands in start[1].items():
                if name not in end[1] or hands == end[1][name]:
                    continue
                # the pass must happen in a sentence about that prop ("passes the balloon", or
                # "picks it up" right after the prop is named), not in an unrelated "leaves frame"
                moved = {p for side in ("r", "l")
                         for p in (hands[side], end[1][name][side]) if p and hands[side] != end[1][name][side]}
                passes = [x for i, x in enumerate(sents) if TRANSFER.search(x) and any(
                    mentions(x, p) or (PRONOUN.search(x) and i and mentions(sents[i - 1], p)) for p in moved)]
                # a prop nobody holds at the end was let go of: "sets the brush down", not just "lifts the paper"
                held_end = {p for led in end[1].values() for p in led.values() if p}
                gone = {p for p in moved if p in hands.values() and p not in held_end}
                unreleased = sorted(p for p in gone if not any(
                    RELEASE.search(x) and (mentions(x, p) or (PRONOUN.search(x) and i and mentions(sents[i - 1], p)))
                    for i, x in enumerate(sents)))
                if not passes:
                    problems.append(f"Clip {n}: {name}'s hands change between start and end "
                                    f"({', '.join(sorted(moved))}), but no beat passes, swaps, drops or picks it up")
                elif unreleased:
                    problems.append(f"Clip {n}: {name}'s hands end without the {', '.join(unreleased)}, but no beat "
                                    f"puts it down, drops or gives it away")
                elif warnings is not None and any(end[1][name][sd] in moved for sd in ("r", "l")) \
                        and not any(SIDE.search(x) or ARM_SIDE.search(x) or BOTH.search(x) for x in passes):
                    # "Bao hands Mira the loaf": the model picks the receiving hand itself
                    warnings.append(f"Clip {n}: the beat that gives {name} the "
                                    f"{next(end[1][name][sd] for sd in ('r', 'l') if end[1][name][sd] in moved)} "
                                    f"names no hand; say which hand takes it: \"{excerpt(passes[0])}\"")
        # beat sentences that name a ledger prop with a hand it is never in during this clip
        # (start or end ledger; a prop picked up mid-clip only appears in the end ledger)
        everyone = set(start[1]) | set(end[1])
        for name in everyone:
            props = {p for led in (start[1], end[1]) for p in led.get(name, {}).values() if p}
            for prop in props:
                allowed = {side for led in (start[1], end[1]) for side, p in led.get(name, {}).items() if p == prop}
                for sent, owned in attribute(beats, everyone):
                    named = {c for c in everyone if name_at(c, sent) >= 0}
                    if mentions(sent, prop) and (not named or name in named):
                        # only the hand named in the same clause as the prop counts:
                        # "opens the door with the left hand and takes out the tea with the right hand"
                        sides = {side for clause, hands in owned if mentions(clause, prop)
                                 for side, owner in hands
                                 if side != "b" and (owner == name or (owner is None and len(named) <= 1))}
                        if sides and not sides & allowed and (n, sent) not in seen:
                            seen.add((n, sent))
                            problems.append(f"Clip {n}: beat puts the {prop} in {name}'s "
                                            f"{'left' if 'l' in sides else 'right'} hand, but the hands lines "
                                            f"keep it in the {'right' if 'r' in allowed else 'left'} hand: "
                                            f"\"{excerpt(sent)}\"")
        # "lifts the red paper with both hands" while one hand holds the brush all clip
        for sent, owned in attribute(beats, everyone):
            for clause, hands in owned:
                for side, owner in hands:
                    if side != "b" or owner not in start[1] or owner not in end[1] or (n, sent) in seen:
                        continue
                    if not (HOLDING.search(clause) or TRANSFER.search(clause) or GRASP.search(clause)):
                        continue
                    busy = [(sd, start[1][owner][sd]) for sd in ("r", "l")
                            if start[1][owner][sd] and start[1][owner][sd] == end[1][owner][sd]
                            and start[1][owner][{"r": "l", "l": "r"}[sd]] != start[1][owner][sd]
                            and not mentions(clause, start[1][owner][sd])]
                    if busy:
                        seen.add((n, sent))
                        sd, p = busy[0]
                        problems.append(f"Clip {n}: {owner} uses both hands, but the {'right' if sd == 'r' else 'left'} "
                                        f"hand holds the {p} all clip; put it down first or use one hand: \"{excerpt(sent)}\"")
        # a ledger prop the action never names ("bánh chưng" in the hands lines, "cake" in the beats)
        if warnings is not None:
            action = "\n".join(TIMED.findall(beats)) or STATIC.sub("", beats)
            # only props that change hands here: one held still all clip needs no beat
            moving = {p for led in (start[1], end[1]) for h in led.values() for p in h.values() if p} - {
                p for name in set(start[1]) & set(end[1]) for sd in ("r", "l")
                for p in [start[1][name][sd]] if p and end[1][name][sd] == p} if start[1] and end[1] else set()
            for p in sorted(moving):
                if not mentions(action, p):
                    warnings.append(f"Clip {n}: the beats never name the {p} from the hands lines; use the beats' "
                                    f"word for it or add it in brackets, e.g. \"bánh chưng (cake)\"")
        # "catches it with her left paw": "it" is the ledger prop named last before it in the clip;
        # check that prop's hand, and ask for the name when no prop was named yet
        owners = {}
        for name in everyone:
            for led in (start[1], end[1]):
                for side, p in led.get(name, {}).items():
                    if p:
                        owners.setdefault(p, {}).setdefault(name, set()).add(side)
        low_beats, cursor = beats.lower(), 0
        for sent, owned in attribute(beats, everyone):
            for clause in CLAUSE.split(sent):
                at = low_beats.find(clause.lower(), cursor) if clause else -1
                cursor = at if at >= 0 else cursor
                low = clause.lower()
                pron = PRONOUN.search(clause)
                hands = next((h for c, h in owned if c == clause), [])
                if not (pron and hands and (HOLDING.search(clause) or TRANSFER.search(clause))) \
                        or any(mentions(low, p) for p in owners) or (n, sent) in seen:
                    continue
                before = low_beats[:cursor + pron.start()]
                last = lambda p: max(before.rfind(k) for k in keys(p))
                prop = max(owners, key=last, default=None)
                key = prop and prop.split()[-1]
                if prop is None or last(prop) < 0:
                    seen.add((n, sent))
                    problems.append(f"Clip {n}: name the prop instead of \"{pron.group(0)}\" "
                                    f"when a hand takes or holds it: \"{excerpt(sent)}\"")
                    continue
                who = {o for _, o in hands if o in owners[prop]}
                allowed = set().union(*(owners[prop][c] for c in (who or owners[prop])))
                sides = {side for side, o in hands if side != "b" and (not who or o in who)}
                if not sides & allowed:
                    seen.add((n, sent))
                    problems.append(f"Clip {n}: \"{pron.group(0)}\" (the {key}) goes in the "
                                    f"{'left' if 'l' in sides else 'right'} hand, but the hands lines keep it in the "
                                    f"{'right' if 'r' in allowed else 'left'} hand: \"{excerpt(sent)}\"")
        # "with a paper pencil in her right hand" while the hands lines keep that hand empty
        if warnings is not None:
            for sent, owned in attribute(beats, everyone):
                for clause, hands in owned:
                    for m in OBJ_IN_HAND.finditer(clause):
                        what, side = m.group(1).lower(), m.group(2).lower()[0]
                        owner = next((o for sd, o in hands if sd == side), None) or (next(iter(everyone)) if len(everyone) == 1 else None)
                        if owner is None or what.split()[-1].rstrip("s") in NOT_PROPS or not hands:
                            continue
                        led = [x.get(owner) for x in (start[1], end[1]) if x.get(owner)]
                        listed = {p for x in (start[1], end[1]) for h in x.values() for p in h.values() if p}
                        if led and all(h[side] is None for h in led) and not any(mentions(what, p) or
                                                                                 any(k in what for k in keys(p)) for p in listed):
                            warnings.append(f"Clip {n}: beat puts {m.group(1)} in {owner}'s "
                                            f"{'right' if side == 'r' else 'left'} hand, which the hands lines keep empty; "
                                            f"list it there or drop it: \"{excerpt(sent)}\"")
        for name, hands in (end[1] or start[1]).items():
            last_seen[name] = (n, hands)
    return problems


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print(__doc__, file=sys.stderr); return 2
    try:
        text = Path(argv[0]).read_text()
    except OSError as e:
        print(e, file=sys.stderr); return 2
    warnings = []
    problems = lint(text, warnings)
    for p in problems:
        print("ERROR", p)
    for w in warnings:
        print("WARN", w)
    print("PASS" if not problems else f"FAIL: {len(problems)} hand continuity problems")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
