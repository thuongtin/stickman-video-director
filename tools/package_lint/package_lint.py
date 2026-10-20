#!/usr/bin/env python3
"""Lint a director's proposal (Phase A) and/or an Omni Flash prompt package (Phase B) before anything is generated.

    package_lint.py package.md [--clips N] [--anchor "verbatim text" ...] [--facts out.md]
    package_lint.py --verify out.md

Reads Markdown: the Phase A storyboard is the first table with a Hands or camera column;
Phase B prompts are the ```text blocks. Each check prints RED (must fix) or YELLOW (look at it, or say why it stays).

Phase A (storyboard table)
  A1 row count = N (with --clips)                       RED
  A2 Hands column filled on every row                    RED
  A3 camera grammar (storyboard-template.md): accents (fast push-in, slam, whip, shake, orbit)
     in more than a third of the rows; three rows in a row pushing inward    YELLOW
  A4 last row is a title, text or quote card                                 RED
  A5 a scene beat only "appears / shows / fades in"                          YELLOW
  A6 a number in the post-production overlay note that the English VO never says   RED
Phase B (prompts)
  B1 prompt count = N (with --clips), and Phase A rows = prompts when both exist   RED
  B2 `Opening hook:` exactly once, in Clip 1 only                            RED
  B3 tools/posture_gate/hand_ledger.py on the whole package                  RED
  B4 a catalog anchor (style-catalog.md) or --anchor used in Clip 1 is missing from a later clip   RED
  B5 the narrator paragraph differs between clips; with approved dialogue written as one
     "Voice — Name: ..." line per speaker, each speaker's line must match wherever it appears   RED
  B6 technical color notation (hex, RGB, HSL, Pantone)                       RED
  B7 quoted words outside the spoken dialogue (they tend to render on screen)  RED
  B8 a beat asks for morphing, melting or liquid shapes                      RED
  B9 a clip has fewer than three timed beats covering 0 to about 10 s            RED
  B10 a clip missing any of the five posture negatives (knees or elbows bending backward, limbs
      changing length, head turned past the shoulders, swapped left and right hands, a prop
      switching hands without a visible pass)                                  RED
  B11 more than one accent camera move in a clip; weak "appears/fades in" beats   YELLOW
  B12 clips 2–N whose Audio/Music line does not say the score continues from clip 1   YELLOW
  B13 a clip whose negatives never forbid logos                                YELLOW

--facts writes the measured facts (counts, results, sha256 of the package) with a fingerprint, so a
delivery note can quote them instead of claiming a pass; --verify reports whether the block was edited.
The checks read prompt text only. They do not score generated video.

Ideas adapted from storyboard_lint.py and deliver.py of huashu-art-motion (MIT, alchaincyf); no code copied.
Exit: 0 = no RED, 1 = RED found, 2 = bad input or edited facts.
"""
import argparse
import datetime
import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CATALOG = REPO / "skills/directing-stickman-videos/references/style-catalog.md"
sys.path.insert(0, str(REPO / "tools/posture_gate"))
import hand_ledger  # noqa: E402

RED, YELLOW = "RED", "YELLOW"

# Camera accents only: "panels slam down" or "vines whip up" are object actions, not camera moves.
ACCENT = re.compile(r"快速推近|快推|镜头震动|震动|晃动|甩镜|砸入|环绕|fast push|(?:slam|crash|snap) zoom|whip[- ]?pan|"
                    r"camera shake|shakes? the camera|camera (?:briefly )?shakes|orbit(?:s|ing)? (?:around|the)|camera orbits?", re.I)
INWARD = re.compile(r"推近|推进|穿过|钻进|push(?:es|ing)?[- ](?:in|closer)|zoom(?:s|ing)? in|fly(?:ing)? through", re.I)
WEAK = re.compile(r"\b(?:appears?|shows? up|is shown|fades? in|is displayed|displays?)\b|出现|浮现|显示|展示|淡入", re.I)
TEXT_CARD = re.compile(r"\b(?:title card|text card|quote card|end card with (?:text|words)|caption card)\b|金句卡|字卡|标题卡", re.I)
TECH_COLOR = re.compile(r"#[0-9a-f]{6}\b|#[0-9a-f]{3}\b|\brgba?\s*\(|\bhsla?\s*\(|\bpantone\b", re.I)
MORPH = re.compile(r"\b(?:morph\w*|melts? into|melting into|turns? (?:in)?to liquid|liquid (?:shapes?|forms?)|"
                   r"splits? into|separates? into|reshapes?|dissolves? into)\b", re.I)
BEAT = re.compile(r"^\s*(?:[-*]\s*)?\[(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)\s*s\]")
# the five posture negatives every clip carries (posture-gate.md)
POSTURE_NEGATIVES = {
    "knees or elbows bending backward": re.compile(r"\b(?:knees?|elbows?)\b[^.\n]{0,40}\bbend\w*\s+backwards?\b", re.I),
    "limbs changing length": re.compile(r"\blimbs?\s+(?:chang|stretch|shrink)\w*\s+(?:in\s+)?length\b|\blimbs?\b[^.\n]{0,30}\bkeep\w* (?:their|its) length\b", re.I),
    "head turned past the shoulders": re.compile(r"\bheads?\b[^.\n]{0,30}\bturn\w*\s+past\s+the\s+shoulders?\b", re.I),
    "swapped left and right hands": re.compile(r"\bswapped left and right hands\b", re.I),
    "prop switching hands without a visible pass": re.compile(r"\bswitch\w*\s+hands\s+without\s+a\s+visible\s+pass\b", re.I),
}
# "Audio: ...", "Music/SFX: ..." or a sentence that opens with it ("Music seamlessly continues ...")
MUSIC_LINE = re.compile(r"^\W*(?:audio|music(?:/sfx)?|bgm|score|soundtrack)\b.*$", re.I | re.M)
FROM_CLIP1 = re.compile(r"\b(?:from|of|in|as in)\s+(?:clip\s*(?:1|one)|the first clip)\b", re.I)
SPEAKER = re.compile(r"^\s*Voice\s*(?:[—–-]\s*|\()([^:()\n]{1,40})\)?:\s*(.+)$", re.M)
VOICE = re.compile(r"\b(?:accent|timbre|register|resonance|baritone|tenor|alto|soprano|pitch)\b", re.I)
NUMBER_WORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
    "seventeen eighteen nineteen twenty".split())}
NUMBER_WORDS.update({"thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80,
                     "ninety": 90, "hundred": 100, "thousand": 1000, "million": 10 ** 6})


# ---------------------------------------------------------------- parsing
def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def storyboard(text):
    """(header, rows) of the first table with a Hands or camera column, else (None, [])."""
    lines = text.splitlines()
    for i, line in enumerate(lines[:-1]):
        if not line.startswith("|") or not re.match(r"^\|\s*:?-{2,}", lines[i + 1]):
            continue
        head = cells(line)
        if not any(re.search(r"hands|手|camera|镜头", h, re.I) for h in head):
            continue
        rows = []
        for row in lines[i + 2:]:
            if not row.startswith("|"):
                break
            rows.append(cells(row))
        return head, rows
    return None, []


def column(head, *keys):
    for k, h in enumerate(head):
        if any(re.search(key, h, re.I) for key in keys):
            return k
    return None


def prompts(text):
    """```text blocks; failing that, the bodies under "Clip N" headings that carry timed beats."""
    found = re.findall(r"```text\n(.*?)\n```", text, re.S)
    if found:
        return found
    return [body.strip() for _, body in hand_ledger.split_clips(text) if "[0–3s]" in body]


def catalog_anchors():
    if not CATALOG.exists():
        return []
    blocks = re.findall(r"```text\n(.*?)\n```", CATALOG.read_text(), re.S)
    # Character anchors only: they mention a stick figure or stickman and are a sentence or more long.
    return [b.strip() for b in blocks if re.search(r"stick ?figure|stickman", b, re.I) and len(b) > 60]


def numbers(text):
    """Numbers written as digits or as plain English words."""
    found = {float(n.replace(",", "")) for n in re.findall(r"\d+(?:,\d{3})*(?:\.\d+)?", text)}
    words = re.findall(r"[a-z]+", text.lower())
    for k, w in enumerate(words):
        if w in NUMBER_WORDS:
            v = NUMBER_WORDS[w]
            if k + 1 < len(words) and words[k + 1] in ("hundred", "thousand", "million"):
                v *= NUMBER_WORDS[words[k + 1]]
            found.add(float(v))
    return found


# ---------------------------------------------------------------- checks
def lint_camera(cams):
    """Camera grammar on a list of per-row (or per-clip) camera cells."""
    out = []
    accents = [n for n, c in enumerate(cams, 1) if ACCENT.search(c)]
    if cams and len(accents) * 3 > len(cams):
        out.append((YELLOW, "A3", f"accent camera moves in rows {accents}: more than a third of {len(cams)}; "
                                  "keep fast moves for reveals and use hold, slow push, pull back or track elsewhere"))
    inward = [bool(INWARD.search(c)) for c in cams]
    for k in range(2, len(cams)):
        if inward[k] and inward[k - 1] and inward[k - 2]:
            out.append((YELLOW, "A3", f"rows {k - 1}-{k + 1} all push inward; pull back, track or hold in between"))
    return out


def lint_phase_a(text, head, rows, clips):
    out = []
    if clips and len(rows) != clips:
        out.append((RED, "A1", f"storyboard has {len(rows)} rows, expected {clips}"))
    hands, cam = column(head, r"hands|手"), column(head, r"camera|镜头")
    scene = column(head, r"scene|场景|画面")
    vo = column(head, r"english vo|^vo$|voice ?over")
    for n, row in enumerate(rows, 1):
        if hands is not None and (hands >= len(row) or not row[hands].strip("-— ")):
            out.append((RED, "A2", f"row {n}: Hands column is empty; name what each hand holds at start and end"))
        if scene is not None and scene < len(row):
            for beat in re.split(r"\*\*[^*]+\*\*|\[\d[^\]]*\]", row[scene]):
                if WEAK.search(beat) and not re.search(r"\b(?:runs?|jumps?|grabs?|throws?|drops?|slams?|walks?)\b|跑|跳|抓|扔|砸|走|摔", beat, re.I):
                    out.append((YELLOW, "A5", f"row {n}: a beat only appears or fades in — give it an action: "
                                              f"\"{beat.strip()[:70]}\""))
    if cam is not None:
        out += lint_camera([r[cam] if cam < len(r) else "" for r in rows])
    if rows and scene is not None and scene < len(rows[-1]) and TEXT_CARD.search(rows[-1][scene]):
        out.append((RED, "A4", "last row ends on a title, text or quote card; end on a character action "
                               "(put words on an object in the scene or in post-production)"))
    # A6: overlay numbers must be spoken.
    if vo is not None:
        spoken = numbers(" ".join(r[vo] for r in rows if vo < len(r)))
        for m in re.finditer(r"^.*(?:overlay|叠加|后期文字).*$", text, re.I | re.M):
            for q in re.findall(r"[“\"]([^”\"]+)[”\"]", m.group(0)):
                for num in re.findall(r"\d+(?:\.\d+)?", q):
                    if float(num) not in spoken:
                        out.append((RED, "A6", f"overlay \"{q}\" shows {num}, which the English VO never says"))
    return out


def spoken_free(p):
    """The prompt without spoken lines: '(VO: "...")', curly-quoted dialogue and the dialogue sentence itself."""
    p = re.sub(r'\([^()"\n]{1,40}:\s*"[^"\n]*"\)', "", p)  # (VO: "...") and (Name: "...")
    p = re.sub(r"“[^”]*”", "", p)
    return "\n".join(l for l in p.splitlines()
                     if not re.match(r"\s*(audio-only dialogue|dialogue|voiceover|vo|voice|audio|music|sfx|sound)\b", l, re.I))


def lint_phase_b(text, ps, clips, extra_anchors):
    out = []
    if clips and len(ps) != clips:
        out.append((RED, "B1", f"package has {len(ps)} prompts, expected {clips}"))
    hooks = [p.count("Opening hook:") for p in ps]
    if hooks[0] != 1 or any(hooks[1:]):
        out.append((RED, "B2", f"`Opening hook:` counts per clip {hooks}; it belongs once in Clip 1 only"))
    for problem in hand_ledger.lint(text):
        out.append((RED, "B3", problem))
    for anchor in catalog_anchors() + list(extra_anchors):
        if anchor in ps[0] or anchor in extra_anchors:
            missing = [n for n, p in enumerate(ps, 1) if anchor not in p]
            if missing:
                out.append((RED, "B4", f"anchor \"{anchor[:60]}…\" is not repeated verbatim in clips {missing}"))
    speakers = {}  # approved dialogue: one "Voice — Name: ..." line per speaker, present only in clips where they speak
    for n, p in enumerate(ps, 1):
        for name, block in SPEAKER.findall(p):
            speakers.setdefault(name.strip(), []).append((n, block.strip()))
    if speakers:
        for name, blocks in speakers.items():
            bad = [n for n, b in blocks if b != blocks[0][1]]
            if bad:
                out.append((RED, "B5", f"{name}'s voice block differs from its first appearance in clips {bad}; "
                                       "repeat each speaker's frozen block verbatim"))
    else:
        voices = []
        for p in ps:
            v = [l for l in p.splitlines() if re.search(r"\b(?:narrator|voice)\b", l, re.I) and VOICE.search(l)]
            voices.append(v[0].strip() if v else None)
        if any(voices) and len({v for v in voices}) > 1:
            bad = [n for n, v in enumerate(voices, 1) if v != voices[0]]
            out.append((RED, "B5", f"the narrator paragraph differs from Clip 1 in clips {bad}; repeat the frozen voice block verbatim"))
    accent_clips = []
    for n, p in enumerate(ps, 1):
        body = spoken_free(p)
        if TECH_COLOR.search(p):
            out.append((RED, "B6", f"clip {n}: technical color notation \"{TECH_COLOR.search(p).group(0)}\"; name colors in words"))
        for q in re.findall(r"\"([^\"\n]{2,})\"|'([A-Z][A-Z!?.' ]{2,})'", body):
            q = q[0] or q[1]
            out.append((RED, "B7", f"clip {n}: quoted words \"{q[:40]}\" outside the dialogue can render on screen; "
                                   "move them to the post-production overlay note"))
        beat_lines = [l for l in body.splitlines() if BEAT.match(l)]
        for l in beat_lines:
            m = MORPH.search(l)
            if m:
                out.append((RED, "B8", f"clip {n}: beat asks for \"{m.group(0)}\"; drive change with a concrete action or a cut"))
            if WEAK.search(l):
                out.append((YELLOW, "B11", f"clip {n}: beat only appears or fades in: \"{l.strip()[:70]}\""))
        spans = [tuple(float(x) for x in BEAT.match(l).groups()) for l in p.splitlines() if BEAT.match(l)]
        if len(spans) < 3 or spans[0][0] != 0 or spans[-1][1] < 9:
            out.append((RED, "B9", f"clip {n}: needs at least three timed beats from [0–…s] to about [..–10s]; found {spans}"))
        missing = [k for k, rx in POSTURE_NEGATIVES.items() if not rx.search(p)]
        if missing:
            out.append((RED, "B10", f"clip {n}: posture negatives missing: no {'; no '.join(missing)}"))
        music = [l for l in MUSIC_LINE.findall(p) if not re.match(r"\W*audio[- ]only dialogue", l, re.I)]
        if n > 1 and not any(FROM_CLIP1.search(l) for l in music):
            out.append((YELLOW, "B12", f"clip {n}: the Audio line does not say the score continues from clip 1 "
                                       "(\"seamlessly continues the identical ... from clip 1, same tempo and instrumentation\")"))
        if not re.search(r"\blogos?\b", body, re.I):
            out.append((YELLOW, "B13", f"clip {n}: the negatives never forbid logos (\"no logos or watermarks\")"))
        accents = sum(bool(ACCENT.search(l)) for l in beat_lines)
        if accents > 1:
            out.append((YELLOW, "B11", f"clip {n}: {accents} beats with an accent camera move; keep one per clip"))
        accent_clips.append(accents > 0)
    if len(ps) >= 3 and sum(accent_clips) * 3 > len(ps):
        out.append((YELLOW, "B11", f"accent camera moves in {sum(accent_clips)} of {len(ps)} clips; keep them to a third"))
    return out


def lint(text, clips=None, anchors=()):
    """Return (findings, facts). findings: [(level, code, message)]."""
    head, rows = storyboard(text)
    ps = prompts(text)
    if head is None and not ps:
        raise ValueError("no storyboard table (with a Hands or camera column) and no ```text prompts found")
    out = []
    if head is not None:
        out += lint_phase_a(text, head, rows, clips)
    if ps:
        out += lint_phase_b(text, ps, clips, anchors)
        if head is not None and len(rows) != len(ps):
            out.append((RED, "B1", f"Phase A has {len(rows)} rows but Phase B has {len(ps)} prompts"))
    facts = {
        "storyboard rows": len(rows) if head is not None else "none",
        "prompts": len(ps),
        "hand_ledger": "PASS" if not any(c == "B3" for _, c, _ in out) else "FAIL",
        "red": sum(l == RED for l, _, _ in out),
        "yellow": sum(l == YELLOW for l, _, _ in out),
    }
    return out, facts


# ---------------------------------------------------------------- facts block
START = "<!-- package_lint facts: generated, do not edit -->"
END = re.compile(r"<!-- package_lint facts end sha256=([0-9a-f]{64}) -->")


def facts_block(path, facts):
    lines = [START, f"- package: `{path.name}` sha256 {hashlib.sha256(path.read_bytes()).hexdigest()[:16]}",
             f"- checked: {datetime.date.today().isoformat()}"]
    lines += [f"- {k}: {v}" for k, v in facts.items()]
    body = "\n".join(lines)
    return f"{body}\n<!-- package_lint facts end sha256={hashlib.sha256(body.encode()).hexdigest()} -->\n"


def verify(path):
    text = path.read_text()
    m = END.search(text)
    if START not in text or not m:
        return False
    body = text[text.index(START):m.start()].rstrip("\n")
    return hashlib.sha256(body.encode()).hexdigest() == m.group(1)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("package", nargs="?")
    ap.add_argument("--clips", type=int, help="expected clip count N (duration / 10)")
    ap.add_argument("--anchor", action="append", default=[], help="text that must appear verbatim in every clip")
    ap.add_argument("--facts", help="write the facts block to this file")
    ap.add_argument("--verify", help="check that a facts block was not edited")
    a = ap.parse_args()
    if a.verify:
        ok = verify(Path(a.verify))
        print("facts block intact" if ok else "facts block missing or edited")
        return 0 if ok else 2
    if not a.package:
        ap.error("give a package file")
    path = Path(a.package)
    try:
        findings, facts = lint(path.read_text(), a.clips, a.anchor)
    except (OSError, ValueError) as e:
        print(f"package_lint: {e}", file=sys.stderr)
        return 2
    for level, code, msg in findings:
        print(f"{level:6} {code:4} {msg}")
    print(f"{'FAIL' if facts['red'] else 'PASS'}: {facts['red']} red, {facts['yellow']} yellow "
          f"({facts['storyboard rows']} storyboard rows, {facts['prompts']} prompts)")
    if a.facts:
        Path(a.facts).write_text(facts_block(path, facts))
    return 1 if facts["red"] else 0


if __name__ == "__main__":
    sys.exit(main())
