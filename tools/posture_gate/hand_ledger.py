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
# "right front hoof", "left hind paw": a four-legged character's limb is still that side's hand
POS = r"(?:(?:front|fore|back|hind|rear)\s+)?"
ENTRY = re.compile(rf"(?P<name>\s*(?:(?:Mr|Mrs|Ms|Dr|St)\.\s*)?[^:;.]+?):\s*(?P<a>(?:right|left) {POS}{LIMB}\s+[^;]+?);\s*(?P<b>(?:right|left) {POS}{LIMB}\s+[^.;\n]+)", re.I)
HAND = re.compile(rf"(right|left) {POS}{LIMB}\s+(.+)", re.I | re.S)
TRANSFER = re.compile(r"\b(opens? (?:his|her|their|its) (?:left |right )?(?:hand|paw|fist|fingers)|closes? (?:his|her|their|its) "
                      r"(?:left |right )?(?:hand|paw|fingers) (?:around|on|over)|lets? (?:\S+ ){0,3}?go|pass(es|ed)?|hands (it )?over|hand it over|(?<!both )(?<!his )(?<!her )(?<!their )(?<!its )(?<!two )(?<!the )(?<!with )hands (?:\w+ )?(?:the|a|an|it|her|his|them)\b|gives?|takes?|swaps?|switch(es)?|moves? .* to (his|her|their|its) "
                      r"(left|right) hand|drops?|puts?|sets? (?:\S+ ){0,6}?down|places?|leans?|picks?|grabs?|catch(es)?|toss(es)?|"
                      r"throws?|releases?|lets? go|tucks?|hangs?|pockets?|stows?|slides?|lays?|leaves?|receives?|"
                      r"accepts?|snatch(es)?|pulls? out|takes? out)\b", re.I)
# Verbs of holding an object; "holds still", "holds her breath", "holds the pose" are not props.
HOLDING = re.compile(r"\b(?:hold(?:s|ing)?(?! (?:still|on|tight|steady|position|the pose|(?:\w+ )?(?:key )?poses?|(?:his|her|their|its) "
                     r"(?:breath|pose|gaze|ground|head|position)))|grab(?:s|bing|bed)?|grip(?:s|ping)?|"
                     r"clutch(?:es|ing)?|carr(?:y|ies|ying)|picks? up|picking up|wields?|"
                     rf"(?:in|with) (?:his|her|their|its|one|both) (?:left |right )?{LIMB}s?)\b[^.\n]{{0,40}}", re.I)
# verbs that let go of a prop: a hand that ends empty needs one ("sets the brush down")
RELEASE = re.compile(r"\b(opens? (?:his|her|their|its) (?:left |right )?(?:hand|paw|fist|fingers)|lets? (?:\S+ ){0,3}?go|pass(es|ed)?|hands (it )?over|hand it over|(?<!both )(?<!his )(?<!her )(?<!their )(?<!its )(?<!two )(?<!the )(?<!with )hands (?:\w+ )?(?:the|a|an|it|her|his|them)\b|gives?|"
                     r"swaps?|switch(es)?|moves?|drops?|puts?|sets?|places?|toss(es)?|throws?|releases?|lets? go|"
                     r"tucks?|hangs?|pockets?|stows?|slides?|lays?|leaves?|rests?|leans?|lowers? .* (?:onto|on|into)|offers?)\b", re.I)
# letting go of a prop where it stays (not a hand-over, a tuck or a switch of hands)
LETGO = re.compile(r"\b(?:drops?(?! (?:into|onto|down|to|in|on|back|low)\b)|lets? (?:\S+ ){0,3}?go|releases?)\b", re.I)
# put somewhere and left there: "places the block in the gap", "sets the cup on the table", "leans the axe
# against the block" (not "rests the bowl on her lap", "tucks it under his arm" or "puts it in her left hand")
PUTAWAY = re.compile(r"\b(?:places?|sets?|puts?|lays?|slots?|fits?|stands?|plants?|hangs?|leans?|props?)\s+"
                     r"(?:(?:\w+ ){0,2}?(?:the|a|an|his|her|their|its|one|both)\b|it\b|them\b)"
                     rf"(?=(?:(?!{LIMB}|\barms?\b|\blap\b|\bstill\b|\bholding\b|\bkeeps?\b|\bgrip)[^,;])*?\b(?:in|into|on|onto|inside|under|beneath|against|beside|atop|down)\b)"
                     rf"(?!(?:(?!\b(?:and|then|while)\b)[^,;.])*\b(?:still holding|keeps? (?:hold|holding|a grip)|without letting go|{LIMB}s?\b))", re.I)
BOTH = re.compile(rf"\b(?:both|two) {LIMB}s\b", re.I)
# description lines that are not actions ("Props: ... wrapped in green leaves")
STATIC = re.compile(r"^\W*(?:output|style(?: and environment)?|characters?|props?|composition|audio|voice|dialogue|"
                    r"camera|lighting|palette|first frame)\b[^:\n]{0,40}:.*$", re.I | re.M)
# timed beat lines, "- [3-7s] ..."
TIMED = re.compile(r"^\s*[-*]?\s*\[[^\]\n]*\d[^\]\n]*\].*$", re.M)
NEAR_FAR = re.compile(rf"\b(near|far|upstage|downstage) (?:arm|{LIMB[3:-1]})s?\b", re.I)
PRONOUN = re.compile(r"\b(it|them)\b", re.I)
# "it" / "them" as the thing a hand holds or passes
PRON_OBJ = re.compile(r"\b(?:hold|grab|grip|take|took|catch|caught|pick|carr(?:y|ie)|clutch|lift|raise|pass|hand|give|gave|"
                      r"drop|put|set|place|toss|throw|tuck|swap|switch|move|receive|accept|snatch|hug|cradle|lower|offer)"
                      r"\w*\s+(?:\w+\s+)?\b(it|them)\b(?!\s+(?:\w+\s+)?(?:between|among))", re.I)
CLAUSE = re.compile(r",\s*|;\s*|\s+(?:and|then|while|before|after|as|when|until|but)\s+", re.I)
SIDE = re.compile(rf"\b(left|right) {POS}{LIMB}s?\b", re.I)
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
OBJ_IN_HAND = re.compile(rf"\b(?:a|an|the|his|her|their|its)\s+((?:[\w-]+\s+){{0,3}}?[\w-]+)\s+(?:(?:still|out|up|high|tight|close)\s+)?in\s+"
                         rf"(?:his|her|their|its|the|one)\s+(left|right)\s+{POS}{LIMB}\b", re.I)
# "with her hand": a hand that takes or holds something without saying which
UNSIDED = re.compile(rf"\b(?:with|in|into) (?:his|her|their|its|one|a) {POS}{LIMB}\b", re.I)
FINGER = re.compile(r"\b(left|right) (?:index |pointer |middle |little )?(?:finger|thumb)s?\b", re.I)
POINTS = re.compile(r"\b(?:point|gesture)(?:s|ed|ing)?\b", re.I)
# picking up, grabbing or catching something; the next words name it
PICKUP = re.compile(r"\b(?:picks? up|picking up|scoops? up|snatch(?:es)?|catch(?:es)?|takes? (?=[^,;.]*\b(?:from|off|out of)\b))\s+", re.I)
STOP = {"from", "off", "out", "with", "in", "into", "and", "to", "up", "onto", "on", "at", "by", "as", "while", "then",
        "before", "after", "of", "toward", "towards", "over", "under", "between", "it", "them"}
# "hands now empty": whatever was in them is gone
EMPTIED = re.compile(rf"\b(?:{LIMB}s?|arms) (?:are |is )?(?:now )?(?:empty|free)\b|\bempty-handed\b", re.I)
NOT_THINGS = {"step", "steps", "breath", "look", "seat", "bow", "turn", "sip", "bite", "moment", "peek", "glance",
              "photo", "picture", "note", "notes", "chance", "deep", "pose", "position", "lead", "aim", "cue", "beat"}
# a character drawn without hands ("no arms, no hands") has no hands to hold anything with
NO_HANDS = re.compile(r"\b(?:no (?:arms|hands)|armless|handless|without (?:arms|hands))\b", re.I)
NOT_PROPS = {"side", "shoulder", "coat", "sleeve", "back", "front", "air", "way", "place", "time", "face", "chin", "head", "cheek", "hair", "pocket", "hand", "paw", "arm", "nose", "mouth", "ear", "eye",
             "hip", "waist", "lap", "chest", "belly", "tail", "string", "handle", "strap"}
# "Two-hand props: red brick, crate" / "Two-hand holders: Bông, Thiếc": always held in both hands
TWO_HAND = re.compile(r"^\W*two[- ]hand(?:ed)?(?: props?| holders?| characters?| only)?\s*:\s*(.+)$", re.I | re.M)
# capitalized words that open a clause without naming a character
NOT_NAMES = {"The", "A", "An", "At", "In", "On", "Behind", "Then", "Now", "She", "He", "They", "It", "Her", "His",
             "Their", "Its", "Camera", "Medium", "Close", "Wide", "Push", "Cut", "Both", "One", "Each", "Everyone",
             "Final", "First", "Audio", "Music", "Voiceover", "VO", "Slowly", "Suddenly", "Meanwhile", "Finally"}
# sentence breaks, but not after "Mr." / "Dr." in a name
SENT = re.compile(r"(?<!\bMr\.)(?<!\bMs\.)(?<!\bDr\.)(?<!\bSt\.)(?<!\bMrs\.)(?<=[.!?;])\s+|\s*\n\s*")


def keys(prop):
    """Words that name a prop in a beat: its last word ("four paper cards" -> "card") and its parts."""
    # "shoulder pole (with baskets)": a Hands line can list parts that name the prop in beats
    inner = re.findall(r"\(([^)]*)\)", prop.lower())
    words = [w.rstrip("s") for w in re.sub(r"\([^)]*\)", " ", prop.lower()).split()] or ["?"]
    if words[-1] in ("hand", "paw", "arm", "finger", "wrist") and len(words) > 1:  # "Bé Na's hand" held in hand-holding: the whole name, not every "hand"
        return {re.sub(r"\s+", " ", re.sub(r"\([^)]*\)", " ", prop.lower())).strip()}
    out = {words[-1]}
    for part in inner:
        out |= {item.split()[-1].rstrip("s") for item in re.split(r",|\band\b|\bwith\b", part) if item.split()}
    out |= {part for part, objs in PARTS.items() if any(o in words for o in objs)}
    out |= {w for w in words if words[-1] in PARTS and w in PARTS[words[-1]]}  # "balloon string" is a balloon
    return out


# every prop the hands lines list in the clip being checked: "the drum baton" is not "the drum"
LISTED = set()


def mentions(text, prop):
    low = text.lower()
    for other in sorted(LISTED, key=len, reverse=True):
        if len(other) > len(prop) and any(re.search(rf"(?<!\w){re.escape(k)}(?!\w)", other) for k in keys(prop)):
            low = re.sub(rf"(?<!\w){re.escape(other)}(?!\w)", " ", low)
    ks = keys(prop)
    # the verb made from the noun names it too: "fanning" is the fan, "phoning" the phone
    verbs = [rf"{re.escape(k)}{re.escape(k[-1])}(?:ing|ed)" for k in ks if len(k) >= 3 and k[-1] not in "aeiouy"] + \
            [rf"{re.escape(k[:-1])}(?:ing|ed)" for k in ks if len(k) >= 4 and k.endswith("e")]
    if any(re.search(rf"(?<!\w){v}(?!\w)", low) for v in verbs):
        return True
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
        # a named character the hands lines never list (a hoofed ox, a passer-by) opening the clause
        # is its subject, so "holding the bundle in its right hoof" is not pinned on someone else
        lead = re.match(r"[^\w\[]*(?:\[[^\]]*\][\W_]*)?(?:(?:and|but|so|then|now|finally|meanwhile|suddenly)\s+)*",
                        clause).end()
        words = re.findall(r"[^\W\d_][\w'-]*", clause[lead:])[:4]
        caps = []
        for w in words:
            if not w[0].isupper() or w in NOT_NAMES:
                break
            caps.append(w)
        outsider = " ".join(caps) if caps and len(caps) < len(words) and words[len(caps)][0].islower() \
            and re.fullmatch(r"\w+s", words[len(caps)]) and not any(name_at(c, clause) == lead for c in cast) else None
        if re.match(r"\s*(?:who|whose)\b", low) and last:  # "passes it to Bo, who takes it" is Bo
            subject = last
        elif found and (subject is None or found[0][0] <= LEAD.match(low).end()):
            subject = found[0][1]  # a name opening the clause; "takes the bear from Kai" keeps its subject
        elif outsider:
            subject = outsider
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
        state.setdefault("clauses", []).append((clause, subject or state.get("subject")))
        out.append((clause, hands))
    if subject:
        state["subject"] = subject
    return out


def acts_on(sent, verb, prop, cast, prev=""):
    """Whether the verb acts on the prop: the prop is named in the verb's clause, or in a clause
    right after it that names nobody new ("places the cup and the saucer"); "it" counts when the
    prop was named just before. "Looks at the envelope, then slides her eyes away" does not pass
    the envelope, and "sets the slipper down, and Lâm freezes with the axe" does not set the axe down."""
    clauses = CLAUSE.split(sent)
    for i, c in enumerate(clauses):
        m = verb.search(c)
        if not m:
            continue
        # "lifts the gear onto the shaft and lets go": a verb with no object of its own acts on the
        # thing just before it
        # (back through "presses it down" to "sets the brick onto the wall")
        if i and not re.search(r"\b(?:the|a|an|his|her|their|its|it|them)\b", c[m.end():], re.I):
            for d in reversed(clauses[:i]):
                if any(name_at(x, d) >= 0 for x in cast) and not mentions(d, prop):
                    break
                if mentions(d, prop):
                    return True
                if not PRONOUN.search(d):
                    break
        for j, d in enumerate(clauses[i:]):
            if j and any(name_at(x, d) >= 0 for x in cast):
                break
            if mentions(d, prop) or (PRONOUN.search(d) and mentions(prev + " " + " ".join(clauses[:i + j]), prop)):
                return True
    return False


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
    t = re.sub(r"\s*\(shared\)", "", t)  # one big prop two characters hold together
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
        for sent in sentences(STATIC.sub("", LINE.sub("", body))):  # "far arm one shade darker" is drawing
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
    two_names = {w.strip().rstrip(".").lower() for m in TWO_HAND.finditer(text)
                 for w in re.split(r",|;|\band\b", re.sub(r"\([^)]*\)", "", m.group(1))) if w.strip()}
    for n, body, lines in ledgers:
        for k in ("start", "end"):
            if k not in lines:
                problems.append(f"Clip {n}: missing 'Hands at {k}' line")
            elif not lines[k][1]:
                problems.append(f"Clip {n}: cannot read 'Hands at {k}' line: {lines[k][0].strip()}")
        start = lines.get("start", ("", {}))
        end = lines.get("end", ("", {}))
        LISTED.clear()
        LISTED.update(p for x in (start[1], end[1]) for h in x.values() for p in h.values() if p)
        # one prop in two characters' hands at once
        for k in ("start", "end"):
            holders = {}
            for name, hands in lines.get(k, ("", {}))[1].items():
                for p in hands.values():
                    if p:
                        holders.setdefault(p, set()).add(name)
            for p, who in holders.items():
                if len(who) > 1 and not re.search(rf"{re.escape(p)}\s*\(shared\)", lines[k][0], re.I):
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
            # the final frame shows how the clip ends, not the beat that gets it there
            sents = sentences(re.sub(r"^\W*final frame\b.*$", "", STATIC.sub("", beats), flags=re.I | re.M))
            for name, hands in start[1].items():
                if name not in end[1] or hands == end[1][name]:
                    continue
                # the pass must happen in a sentence about that prop ("passes the balloon", or
                # "picks it up" right after the prop is named), not in an unrelated "leaves frame"
                moved = {p for side in ("r", "l")
                         for p in (hands[side], end[1][name][side]) if p and hands[side] != end[1][name][side]}
                cast = set(start[1]) | set(end[1])
                passes = [x for i, x in enumerate(sents) if TRANSFER.search(x) and any(
                    acts_on(x, TRANSFER, p, cast, sents[i - 1] if i else "") for p in moved)]
                # a prop nobody holds at the end was let go of: "sets the brush down", not just "lifts the paper"
                # and by this character, even when someone else ends up with it: "Đá Núi catches the barrel"
                # does not let it go from Gọng Sắt's hand
                gone = {p for p in moved if p in hands.values() and p not in end[1][name].values()}
                st, subjects = {"clauses": []}, []
                for x in sents:
                    k = len(st["clauses"])
                    hand_owners(x, cast, st)
                    subjects.append({w for _, w in st["clauses"][k:]})
                held_end = {p for led in end[1].values() for p in led.values() if p}
                said = lambda k: re.search(rf"(?<!\w){re.escape(name)}(?!\w)", sents[k], re.I)
                # let go by this character, or taken from them by someone else ("takes the stone from Than")
                unreleased = sorted(p for p in gone if not any(
                    (RELEASE.search(x) and acts_on(x, RELEASE, p, cast, sents[i - 1] if i else "")
                     and any(name in subjects[k] or said(k) for k in {i, max(i - 1, 0)}))
                    or (TRANSFER.search(x) and acts_on(x, TRANSFER, p, cast, sents[i - 1] if i else "")
                        and (said(i) or (i and said(i - 1))) and (name not in subjects[i] or p in held_end))
                    for i, x in enumerate(sents)))
                if not passes:
                    problems.append(f"Clip {n}: {name}'s hands change between start and end "
                                    f"({', '.join(sorted(moved))}), but no beat passes, swaps, drops or picks it up")
                elif unreleased:
                    problems.append(f"Clip {n}: {name}'s hands end without the {', '.join(unreleased)}, but no beat "
                                    f"puts it down, drops or gives it away")
                elif warnings is not None and any(end[1][name][sd] in moved for sd in ("r", "l")) \
                        and not any(o in (name, None) for x in sents
                                    if (TRANSFER.search(x) or re.search(r"\b(?:grip|grab|catch|clutch)\w*", x, re.I))
                                    and any(mentions(x, end[1][name][sd]) for sd in ("r", "l") if end[1][name][sd] in moved)
                                    for _, hs in hand_owners(x, set(start[1]) | set(end[1])) for _, o in hs):
                    # "Bao hands Mira the loaf": the model picks the receiving hand itself
                    warnings.append(f"Clip {n}: the beat that gives {name} the "
                                    f"{next(end[1][name][sd] for sd in ('r', 'l') if end[1][name][sd] in moved)} "
                                    f"names no hand; say which hand takes it: \"{excerpt(next((x for x in passes if any(mentions(x, end[1][name][sd]) for sd in ('r', 'l') if end[1][name][sd] in moved)), passes[0]))}\"")
        # beat sentences that name a ledger prop with a hand it is never in during this clip
        # (start or end ledger; a prop picked up mid-clip only appears in the end ledger)
        everyone = set(start[1]) | set(end[1])
        for name in everyone:
            props = {p for led in (start[1], end[1]) for p in led.get(name, {}).values() if p}
            for prop in props:
                allowed = {side for led in (start[1], end[1]) for side, p in led.get(name, {}).items() if p == prop}
                for sent, owned in attribute(re.sub(r"^\W*characters?\b[^:\n]{0,40}:.*$", "", beats, flags=re.I | re.M), everyone):  # not the cast list
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
                pron = PRON_OBJ.search(clause)  # "takes it", not "slaps it" or "a low five between them"
                hands = next((h for c, h in owned if c == clause), [])
                if not (pron and hands and (HOLDING.search(clause) or TRANSFER.search(clause))) \
                        or any(mentions(low, p) for p in owners) or (n, sent) in seen:
                    continue
                before = low_beats[:cursor + pron.start(1)]
                last = lambda p: max(before.rfind(k) for k in keys(p))
                prop = max(owners, key=last, default=None)
                key = prop and prop.split()[-1]
                if prop is None or last(prop) < 0:
                    seen.add((n, sent))
                    problems.append(f"Clip {n}: name the prop instead of \"{pron.group(1)}\" "
                                    f"when a hand takes or holds it: \"{excerpt(sent)}\"")
                    continue
                who = {o for _, o in hands if o in owners[prop]}
                if not who and any(o for _, o in hands):
                    continue  # someone the hands lines never give it to: not their hands to compare
                allowed = set().union(*(owners[prop][c] for c in (who or owners[prop])))
                sides = {side for side, o in hands if side != "b" and (not who or o in who)}
                if not sides & allowed:
                    seen.add((n, sent))
                    problems.append(f"Clip {n}: \"{pron.group(1)}\" (the {key}) goes in the "
                                    f"{'left' if 'l' in sides else 'right'} hand, but the hands lines keep it in the "
                                    f"{'right' if 'r' in allowed else 'left'} hand: \"{excerpt(sent)}\"")
        # "with a paper pencil in her right hand" while the hands lines keep that hand empty, or
        # "the cog in his left hand" while they call it the big gear
        listed = {p for x in (start[1], end[1]) for h in x.values() for p in h.values() if p}
        for sent, owned in attribute(beats, everyone):
            for clause, hands in owned:
                for m in OBJ_IN_HAND.finditer(clause):
                    what, side = m.group(1).lower(), m.group(2).lower()[0]
                    owner = next((o for sd, o in hands if sd == side), None) or (next(iter(everyone)) if len(everyone) == 1 else None)
                    if owner is None or what.split()[-1].rstrip("s") in NOT_PROPS or not hands or \
                            any(mentions(what, p) or any(k in what for k in keys(p)) for p in listed) or (n, sent) in seen:
                        continue
                    led = [x.get(owner) for x in (start[1], end[1]) if x.get(owner)]
                    if not led:
                        continue
                    other = {h["l" if side == "r" else "r"] for h in led} - {None}
                    hand = "right" if side == "r" else "left"
                    if all(h[side] is None for h in led) and len(other) == 1 and all(h["l" if side == "r" else "r"] for h in led) \
                            and warnings is not None:
                        # the one thing this character holds is in the other hand: perhaps it, renamed
                        warnings.append(f"Clip {n}: beat puts {m.group(1)} in {owner}'s {hand} hand, which the hands "
                                        f"lines keep empty; if it is the {next(iter(other))}, they keep that in the other "
                                        f"hand (call it the same in both, or list an alias in brackets): \"{excerpt(sent)}\"")
                    elif warnings is None:
                        continue
                    elif all(h[side] is None for h in led):
                        warnings.append(f"Clip {n}: beat puts {m.group(1)} in {owner}'s {hand} hand, which the hands "
                                        f"lines keep empty; list it there or drop it: \"{excerpt(sent)}\"")
                    else:
                        p = next(h[side] for h in led if h[side])
                        warnings.append(f"Clip {n}: beat calls {m.group(1)} what the hands lines call the {p}; use one "
                                        f"name, or add it in brackets: \"{p} ({what.split()[-1]})\": \"{excerpt(sent)}\"")
        # every clause with its subject, for the checks below
        st, rows = {}, []
        # sentences from here on are the final frame: how the clip ends, not a beat
        timed_n = len(sentences("\n".join(TIMED.findall(beats)))) if TIMED.search(beats) else 10 ** 9
        for si, x in enumerate(sentences("\n".join(TIMED.findall(beats)) + "\n" + "\n".join(
                re.findall(r"^\W*final frame\b.*$", beats, re.I | re.M)) if TIMED.search(beats) else STATIC.sub("", beats))):
            for clause, hands in hand_owners(x, everyone, st):
                rows.append((si, x, clause, st["clauses"][len(rows)][1], hands))
        # the last beat that puts a prop in a character's hands sets how the clip ends
        for name in end[1]:
            for p in sorted({v for v in end[1][name].values() if v}):
                want = {sd for sd in ("r", "l") if end[1][name][sd] == p}
                last, ctx = None, None
                for si, x, clause, _, hands in rows:
                    sides = {sd for sd, o in hands if sd != "b" and o == name}
                    # one grip described hand by hand in one sentence: "holding the broom low in his
                    # right hand and high in his left hand", "takes the broom in his right hand and
                    # adds his left hand above it on the handle"
                    named = mentions(clause, p)
                    # a clause with no object of its own ("and high in his left hand") goes on with the prop
                    bare = ctx == si and not BOTH.search(clause) and set(re.findall(r"[\w-]+", SIDE.sub("", clause).lower())) <= {
                        "low", "high", "higher", "lower", "up", "down", "in", "on", "with", "at", "near", "top", "bottom",
                        "above", "below", "it", "his", "her", "their", "its", "too", "also", "end", "further", "farther"}
                    if not (named or bare):
                        ctx = None if any(mentions(clause, q) for q in LISTED) else ctx
                        continue
                    if sides:
                        joins = bare or re.search(r"\b(?:too|also|adds?|joins?|together)\b", clause, re.I)
                        last = (last[0] | sides, x) if last and ctx == si and joins else (sides, x)
                    ctx = si
                if last and (n, last[1]) not in seen:
                    sides, x = last
                    say = lambda ss: " and ".join("right hand" if sd == "r" else "left hand" for sd in sorted(ss, reverse=True))
                    if sides - want:
                        seen.add((n, x))
                        problems.append(f"Clip {n}: the last beat with the {p} has it in {name}'s {say(sides)}, but "
                                        f"the end line has it in the {say(want)}: \"{excerpt(x)}\"")
                    elif want - sides and warnings is not None:
                        warnings.append(f"Clip {n}: the end line has the {p} in {name}'s {say(want)}, but the last "
                                        f"beat with it uses only the {say(sides)}; show the other hand join it: "
                                        f"\"{excerpt(x)}\"")
        # held all clip: (character, side) -> prop
        held_all = {(c, sd): start[1][c][sd] for c in start[1] if c in end[1] for sd in ("r", "l")
                    if start[1][c][sd] and end[1][c][sd] == start[1][c][sd]}
        # what each hand holds as the beats go, from the start line: a hand that picks up a new
        # prop must have put the old one down first
        now = {(c, sd): p for c in start[1] for sd, p in start[1][c].items() if p}
        # props a character holds in both hands at the end, or at the start and the end
        two = {(c, p) for led in (start[1], end[1]) for c in led for p in set(led[c].values())
               if p and led[c]["r"] == led[c]["l"]}
        steady = {(c, p) for c, p in two if all(c in led and led[c]["r"] == led[c]["l"] == p for led in (start[1], end[1]))}
        released = {}
        for idx, (si, x, clause, who, hands) in enumerate(rows):
            final = si >= timed_n or re.match(r"\W*final frame\b", x, re.I)
            # "Gạch places the block in the gap" while the block is still in Than's hand: the take is missing
            put = PUTAWAY if PUTAWAY.search(clause) else LETGO if LETGO.search(clause) else None
            if put and who in everyone and not final and (n, x) not in seen:
                prev = " ".join(c2 for s2, _, c2, _, _ in rows[max(0, idx - 3):idx] if s2 == si)
                for q in sorted(listed, key=len, reverse=True):
                    others = sorted({c for (c, _), p in now.items() if p == q and c != who})
                    if others and q not in {p for (c, _), p in now.items() if c == who} \
                            and acts_on(prev + ", " + clause, put, q, everyone):
                        seen.add((n, x))
                        problems.append(f"Clip {n}: {who} puts down the {q}, but it is still in {' and '.join(others)}'s "
                                        f"hand; add the beat where {who} takes it: \"{excerpt(x)}\"")
                        break
            if who and RELEASE.search(clause) and not final:
                prev = " ".join(c2 for s2, _, c2, _, _ in rows[max(0, idx - 3):idx] if s2 == si)
                for key in [k for k in now if k[0] == who and (PRONOUN.search(clause)
                                                               or acts_on(prev + ", " + clause, RELEASE, now[k], everyone))]:
                    del now[key]
                # put down out of reach ("places the block in the gap and lets go"): the end line can't keep it
                for q in listed:
                    let = LETGO if LETGO.search(clause) else PUTAWAY
                    if let.search(clause) and acts_on(prev + ", " + clause, let, q, everyone) \
                            and not any(name_at(c, clause) >= 0 for c in everyone if c != who):
                        released[(who, q)] = (x, {sd for sd, o in hands if o == who and sd != "b"})
            if TRANSFER.search(clause) and not final:
                for c in everyone:  # handed to someone ("gives the cup back to Mia"): theirs again
                    if c != who and name_at(c, clause) >= 0:
                        for q in [q for (c2, q) in released if c2 == c and mentions(clause, q)]:
                            del released[(c, q)]
            elif who and EMPTIED.search(clause) and not final:
                named = {sd for sd, o in hands if o == who and sd != "b"}
                for key in [k for k in now if k[0] == who and (not named or k[1] in named)]:
                    del now[key]
            took = PICKUP.search(clause) or re.search(r"\b(?:takes?|receives?|accepts?|grabs?|catch(?:es)?)\b", clause, re.I)
            got = next((p for p in sorted(listed, key=len, reverse=True) if mentions(clause, p)), None)
            if took and got and who and not final:
                for sd in sorted({sd for sd, o in hands if sd != "b" and o == who}):
                    old = now.get((who, sd))
                    if old and old != got and not mentions(x, old) and (n, x) not in seen:
                        seen.add((n, x))
                        problems.append(f"Clip {n}: {who}'s {'right' if sd == 'r' else 'left'} hand takes the {got} "
                                        f"while it still holds the {old}; add a beat that puts the {old} down first: "
                                        f"\"{excerpt(x)}\"")
                    now[(who, sd)] = got
                for c in everyone:  # "takes the stone from Than": out of Than's hand
                    if c != who and re.search(rf"\bfrom {re.escape(c)}(?!\w)", clause):
                        for key in [k for k in now if k[0] == c and now[k] == got]:
                            del now[key]
                        released[(c, got)] = (x, set())
                released.pop((who, got), None)
            elif who and not final and (GRASP.search(clause) or HOLDING.search(clause)):
                # laid on the table, then lifted again: "lifts her folded sheet with her left hand"
                for q in [q for (c2, q) in released if c2 == who and mentions(clause, q)]:
                    del released[(who, q)]
            # a prop held in both hands, used with one: "lifts the broom in his left hand alone"
            for c, p in two:
                sides = {sd for sd, o in hands if o == c}
                if len(sides) != 1 or "b" in sides or not mentions(clause, p) or (n, x) in seen or final:
                    continue
                sd = next(iter(sides))
                hand, other = ("right", "left") if sd == "r" else ("left", "right")
                if (c, p) in steady and re.search(r"\b(?:alone|only|one-handed|single)\b", clause, re.I):
                    seen.add((n, x))
                    problems.append(f"Clip {n}: {c} holds the {p} in the {hand} hand alone, but the hands lines keep it "
                                    f"in both hands all clip; drop \"alone\" or show the {other} hand let go and "
                                    f"take hold again: \"{excerpt(x)}\"")
                elif (took or HOLDING.search(clause)) and warnings is not None \
                        and not re.search(r"\b(?:off|lets? go|releases?)\b", x, re.I) and not any(
                        o == c and s2 in ("l" if sd == "r" else "r", "b")
                        for j3, (s3, x3, c3, _, h3) in enumerate(rows) if s3 < timed_n
                        and (s3 == si or (j3 > idx and mentions(c3, p))) for s2, o in h3):
                    seen.add((n, x))
                    warnings.append(f"Clip {n}: a beat has {c} hold the {p} in the {hand} hand, but the hands lines "
                                    f"have it in both hands; show the {other} hand join it or let go in a beat: "
                                    f"\"{excerpt(x)}\"")
            # waving with a hand that holds something all clip
            if who and re.search(r"\bwav(?:e|es|ed|ing)\b(?! (?:the|a|an|his|her|their|its)\b)", clause, re.I) \
                    and warnings is not None and (n, x) not in seen:
                sides = {mm.group(1).lower()[0] for mm in SIDE.finditer(clause)}
                busy = {sd: p for (c, sd), p in held_all.items() if c == who and not mentions(clause, p)}
                hit = sorted(sides & set(busy)) or (sorted(busy) if not sides and len(busy) == 2 else [])
                if hit:
                    seen.add((n, x))
                    sd = hit[0]
                    warnings.append(f"Clip {n}: {who} waves with the {'right' if sd == 'r' else 'left'} hand, which holds "
                                    f"the {busy[sd]} all clip: \"{excerpt(x)}\"")
            # a thing picked up or caught that the hands lines never list must be put down again
            for m in PICKUP.finditer(clause):
                words = []
                for w in re.findall(r"[\w'-]+", clause[m.end():]):
                    if w.lower() in STOP:
                        break
                    words.append(w)
                words = [w for w in words if w.lower() not in ("the", "a", "an", "his", "her", "their", "its", "one", "another")]
                if not words or (n, x) in seen:
                    continue
                noun, thing = words[-1], " ".join(words)
                if noun.lower().rstrip("s") in NOT_PROPS or noun.lower() in NOT_THINGS or \
                        any(mentions(thing, p) for p in listed) or noun.lower() in ("him", "her", "them", "it"):
                    continue
                pat = re.compile(rf"(?<!\w){re.escape(noun)}(?!\w)", re.I)
                if not any((RELEASE.search(c2) and (pat.search(c2) or (s2 == si and PRONOUN.search(c2))))
                           or (EMPTIED.search(c2) and w2 == who) for s2, _, c2, w2, _ in rows[idx + 1:]):
                    gained = sorted({end[1][who][sd] for sd in ("r", "l") if who in end[1] and end[1][who][sd]
                                     and (who not in start[1] or start[1][who][sd] != end[1][who][sd])})
                    seen.add((n, x))
                    if gained and warnings is not None:
                        warnings.append(f"Clip {n}: {who} {m.group(0).strip()} the {thing}, which the hands lines never "
                                        f"list; if it is the {gained[0]}, use one name or add it in brackets: "
                                        f"\"{gained[0]} ({noun.lower()})\": \"{excerpt(x)}\"")
                    elif not gained:
                        problems.append(f"Clip {n}: {who or 'a character'} {m.group(0).strip()} the {thing}, but no later "
                                        f"beat puts it down or passes it on, and the hands lines never list it: \"{excerpt(x)}\"")
            # pointing with a hand that holds something all clip
            if POINTS.search(clause) and not GRASP.search(clause) and who and (
                    name_at(who, clause) >= 0 or re.match(r"\W*(?:(?:and|then)\s+)?(?:he|she|they|point|gesture)", clause, re.I)):
                sides = {mm.group(1).lower()[0] for mm in (*SIDE.finditer(clause), *FINGER.finditer(clause))}
                busy = {sd: p for (c, sd), p in held_all.items() if c == who}
                for sd in sorted(sides):
                    if sd in busy and not mentions(clause, busy[sd]) and (n, x) not in seen:
                        seen.add((n, x))
                        problems.append(f"Clip {n}: {who} points with the {'right' if sd == 'r' else 'left'} hand, "
                                        f"which holds the {busy[sd]} all clip: \"{excerpt(x)}\"")
                if not sides and busy and warnings is not None and re.search(r"\bpoint", clause, re.I):
                    sd, p = next(iter(busy.items()))
                    warnings.append(f"Clip {n}: say which hand {who} points with ({who}'s "
                                    f"{'right' if sd == 'r' else 'left'} hand holds the {p}): \"{excerpt(x)}\"")
            # "picks it up with her hand": which hand?
            u = UNSIDED.search(clause)
            if u and warnings is not None and not hands and not POINTING.search(clause) and \
                    (GRASP.search(clause) or PICKUP.search(clause) or TRANSFER.search(clause)):
                warnings.append(f"Clip {n}: say which hand (\"{u.group(0)}\"): \"{excerpt(x)}\"")
        # a prop a beat put in a hand and never let go of, missing from the end line
        for (c, sd), q in sorted(now.items()):
            if c in end[1] and q not in end[1][c].values() and not (start[1].get(c) or {}).get(sd) == q \
                    and not any(q in h.values() for h in end[1].values()) and (n, c, q) not in seen:
                seen.add((n, c, q))
                problems.append(f"Clip {n}: {c} takes the {q} in a beat but ends without it, and no later beat puts "
                                f"it down, drops or gives it away")
        for (c, q), (x, sds) in sorted(released.items()):
            if any(end[1].get(c, {}).get(sd) == q for sd in (sds or ("r", "l"))) and (n, x) not in seen:
                seen.add((n, x))
                problems.append(f"Clip {n}: {c} lets go of the {q} (puts it down or hands it over), but the end line still has it in {c}'s hand; "
                                f"empty that hand in the end line or pick it up again in a beat: \"{excerpt(x)}\"")
        # declared two-hand props and holders: never one hand, in the hands lines or in a beat
        if two_names:
            cast_low = {c.lower(): c for c in everyone}
            for k in ("start", "end"):
                for c, h in lines.get(k, ("", {}))[1].items():
                    for sd in ("r", "l"):
                        q = h[sd]
                        if q and h["l" if sd == "r" else "r"] != q and (c.lower() in two_names or any(
                                mentions(q, t) or q == t for t in two_names if t not in cast_low)):
                            problems.append(f"Clip {n}: the {k} line has {c} hold the {q} in one hand, but it is declared "
                                            f"two-handed; list it in both hands")
            for si, x, clause, w, hands in rows:
                if (n, x, "two") in seen or si >= timed_n or not (GRASP.search(clause) or HOLDING.search(clause)
                                                         or PICKUP.search(clause) or TRANSFER.search(clause)):
                    continue
                for c in {o for _, o in hands if o}:
                    sides = {sd for sd, o in hands if o == c}
                    if len(sides) != 1 or "b" in sides:
                        continue
                    q = next((t for t in sorted(listed, key=len, reverse=True) if mentions(clause, t)), None) \
                        or next((t for t in two_names if t not in cast_low and re.search(rf"(?<!\w){re.escape(t)}(?!\w)", clause.lower())), None)
                    if q and (c.lower() in two_names or any(t not in cast_low and (mentions(q, t) or q == t) for t in two_names)):
                        seen.add((n, x, "two"))
                        problems.append(f"Clip {n}: {c} holds the {q} in the {'right' if 'r' in sides else 'left'} hand "
                                        f"alone, but it is declared two-handed; use both hands: \"{excerpt(x)}\"")
        # a character outside the hands lines who has no hands ("Trâu Đá has no hands") holding something
        for o in sorted({w for _, _, _, w, _ in rows if w and w not in everyone}):
            said = [x2 for x2 in sentences(text) if name_at(o, x2) >= 0
                    and NO_HANDS.search(x2[name_at(o, x2):]) and not re.search(r"\bhands?\b(?! *(?:lines?|ledger))", x2[:name_at(o, x2)])]
            for _, x, clause, w, hands in rows:
                # "in its right front hoof", or "grips the bundle in its hoof" with no side
                if w == o and said and (n, x) not in seen and (any(sd != "b" for sd, ow in hands if ow == o)
                                                               or UNSIDED.search(clause)) \
                        and (OBJ_IN_HAND.search(clause) or HOLDING.search(clause) or GRASP.search(clause)):
                    seen.add((n, x))
                    problems.append(f"Clip {n}: {o} has no hands (\"{NO_HANDS.search(said[0][name_at(o, said[0]):]).group(0)}\"), "
                                    f"but a beat has {o} hold something in one; carry it on the back or in the mouth: \"{excerpt(x)}\"")
        # a character drawn without hands
        for name in everyone:
            for x in sentences(text):  # "Bacillo has no hands", "Bacillo: a rod-shaped germ with no arms"
                at = name_at(name, x)
                if at < 0:
                    continue
                seg = x[at + len(name):]
                cut = min([name_at(c, seg) for c in everyone if c != name and name_at(c, seg) >= 0] or [len(seg)])
                seg = seg[:cut]
                if NO_HANDS.search(seg) and not re.search(r"\b(?:paw|flipper|wing|hoof|claw|fin|glove|mitten|tentacle)s?\b", seg, re.I):
                    things = sorted({p for led in (start[1], end[1]) for p in led.get(name, {}).values() if p})
                    if things:
                        problems.append(f"Clip {n}: {name} has no hands (\"{NO_HANDS.search(seg).group(0)}\"), "
                                        f"but the hands lines put the {', '.join(things)} in them")
                    elif warnings is not None:
                        warnings.append(f"Clip {n}: {name} has no hands (\"{NO_HANDS.search(seg).group(0)}\"); "
                                        f"leave {name} out of the hands lines")
                    break
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
