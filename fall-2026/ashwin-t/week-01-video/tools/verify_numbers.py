"""Check that every number in beat_sheet.json traces to the evidence files.

On-screen numbers (anything in shot.remotion.props) must appear verbatim in
w1-evidence/*.txt, or be a 2-decimal percentage of a printed probability.
Spoken numbers (narration_text, written as words) are listed for a human to
compare against the same files — this script prints them, it does not judge them.

    python3 tools/verify_numbers.py        # exit 1 on any untraced on-screen number
"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
# evidence sits beside this folder's files in the submission, or in ../w1-evidence while building
EV = HERE if (HERE / "offset-output.txt").exists() else HERE.parent / "w1-evidence"
evidence = "\n".join(p.read_text() for p in sorted(EV.glob("*.txt")))
printed_floats = [float(x) for x in re.findall(r"-?\d+\.\d+", evidence)]
pct_ok = {f"{p * 100:.2f}" for p in printed_floats if 0 <= p <= 1}

# layout/timing keys are not claims; only text a viewer reads is checked
NOT_SHOWN = {"appearAtS", "atS", "probsAtS", "sourceAtS", "countStartS", "countDurS",
             "sweepAtS", "verdictAtS", "errorAtS", "footerAtS", "step", "durationS", "bodyScale"}
NUM = re.compile(r"-?\d+(?:\.\d+)?%?")


def walk(node, key=None):
    if isinstance(node, dict):
        for k, v in node.items():
            if k not in NOT_SHOWN and not k.endswith(("AtS", "DurS", "StartS")):
                yield from walk(v, k)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v, key)
    elif isinstance(node, (int, float)) and not isinstance(node, bool):
        yield key, str(node)
    elif isinstance(node, str):
        yield key, node


LABELS = {"7375"}   # course code on the title card (INFO 7375) — a label, not a claim


def traced(tok):
    if tok in LABELS:
        return True
    if tok.endswith("%"):
        return tok[:-1] in pct_ok
    return re.search(r"(?<![\d.])" + re.escape(tok) + r"(?![\d])", evidence) is not None


sheet = json.loads((HERE / "beat_sheet.json").read_text())
bad, n = [], 0
for b in sheet["beats"]:
    props = b["shot"]["remotion"]["props"]
    for key, text in walk(props):
        if key == "source":          # file paths, e.g. "01-randomness"
            continue
        for tok in NUM.findall(text):
            n += 1
            if not traced(tok):
                bad.append((b["beat_id"], key, tok, text))

print(f"on-screen numbers checked: {n}")
for bid, key, tok, text in bad:
    print(f"  UNTRACED  {bid}.{key}: {tok!r} in {text!r}")
print("on-screen: all traced to w1-evidence/*.txt" if not bad else f"on-screen: {len(bad)} untraced")

print("\nspoken numbers (compare by ear/eye with the evidence):")
NUMWORDS = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
            "twenty", "twenty-four", "twenty-six", "sixty", "sixty-six", "seventy",
            "seventy-three", "thousand", "hundred", "point", "percent", "negative",
            "fifty-fifty", "and"}
for b in sheet["beats"]:
    words = re.findall(r"[A-Za-z-]+", b["narration_text"])
    groups, cur = [], []
    for w in words + ["."]:
        if w.lower() in NUMWORDS:
            cur.append(w)
        else:
            while cur and cur[-1].lower() == "and":
                cur.pop()
            if cur and cur[0].lower() != "and":
                groups.append(" ".join(cur))
            cur = []
    if groups:
        print(f"  {b['beat_id']}: " + " | ".join(groups))
sys.exit(1 if bad else 0)
