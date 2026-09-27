"""Write beat_sheet.json for the Week 1 explainer.

Every number that appears on screen is READ from the evidence files in
../../w1-evidence/ — never typed by hand. Run once to create the sheet; the
audio script then stamps measured durations into it. Re-running overwrites
those stamps, so regenerate audio afterwards.

    python3 tools/build_beat_sheet.py
"""
import ast, json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
# evidence sits beside this folder's files in the submission, or in ../w1-evidence while building
EV = HERE if (HERE / "offset-output.txt").exists() else HERE.parent / "w1-evidence"

ref = json.loads((EV / "reference-output.txt").read_text())
offset_lines = (EV / "offset-output.txt").read_text().splitlines()
inter_lines = (EV / "intermediates-output.txt").read_text().splitlines()


def after_arrow(line):
    return line.split("->", 1)[1].strip()


def find(lines, startswith):
    hits = [l for l in lines if l.startswith(startswith)]
    assert len(hits) == 1, (startswith, hits)
    return hits[0]


# reference-output.txt (main.py): the printed probabilities, as Python printed them
probs_ref = [repr(p) for p in ref["probabilities"]]
pcts = [f"{p * 100:.2f}%" for p in ref["probabilities"]]

# offset-output.txt
base = ast.literal_eval(after_arrow(find(offset_lines, "[1, 2, 3] ")))
shifted = ast.literal_eval(after_arrow(find(offset_lines, "[1001, 1002, 1003] ")))
identical_line = find(offset_lines, "bitwise identical?")        # printed verbatim
assert [repr(x) for x in base] == probs_ref, "offset script disagrees with main.py"


def row(key):
    vals = ast.literal_eval(after_arrow(find(offset_lines, key + " ")))
    return key, ", ".join(vals)


r1000, r00, r55, r12, r1001 = (row(k) for k in
                               ("[1000, 1000]", "[0, 0]", "[-5, -5]", "[1, 2]", "[1001, 1002]"))
naive_head = find(offset_lines, "naive exp at")
naive_err = find(offset_lines, "  OverflowError").strip()

# intermediates-output.txt
minus_max = [l.split("minus max", 1)[1].strip() for l in inter_lines if "minus max" in l]
assert len(minus_max) == 2 and minus_max[0] == minus_max[1]
sweep_n = find(inter_lines, "bitwise identical to [1, 2, 3]:").split(":")[1].strip()
sweep_all = find(inter_lines, "all identical?")
assert sweep_all.endswith("True")

SRC_MAIN = "source: lesson code/main.py → reference-output.txt · inputs [1, 2, 3] from demo()"
SRC_OFFSET = "source: w1-evidence/offset_evidence.py → offset-output.txt"
SRC_INTER = "source: w1-evidence/intermediates_evidence.py → intermediates-output.txt"


def beat(bid, act, text, props, est, cues=None):
    """cues: {prop path: "pN" or "pN+0.2"} — resolved to seconds by tools/sync_cues.py
    from the Nth pause measured in this beat's own narration mp3."""
    shot = {"type": "REMOTION", "source": "own",
            "lane": "card" if props["mode"] == "card" else "remotion",
            "remotion": {"pattern": "SoftmaxOffset", "props": props}}
    if cues:
        shot["remotion"]["cues"] = cues
    return {
        "beat_id": bid,
        "act": act,
        "narration_text": text,
        "estimated_duration_s": est,
        "shot": shot,
    }


def table(**kw):
    return {"mode": "table", "logits": [1, 2, 3], "probs": probs_ref, "pcts": pcts,
            "title": "Real output from the course lesson", "label": "recorded output",
            "source": SRC_MAIN, **kw}


def rows(rs, **kw):
    return {"mode": "rows", "title": "Same scores, any size", "label": "recorded output",
            "source": SRC_OFFSET, "rows": rs, **kw}


def r(pair, at=0, **kw):
    return {"input": pair[0], "output": pair[1], "appearAtS": at, **kw}


beats = [
    # ── 0 · the question (added after draft 1: the start felt abrupt) ───────
    beat("B00", "0 question",
         "If a language model gives a word a huge score, does that mean it's confident? "
         "Not necessarily. Here's why.",
         {"mode": "card", "light": True, "bodyScale": 1.45, "lines": [
             {"text": "INFO 7375 · WEEK 1 · SOFTMAX", "atS": 0.3},
             {"text": "Does a huge score mean a confident model?", "atS": 0.6, "strong": True},
             {"text": "What softmax keeps, and what it throws away.", "atS": 3.0},
         ]}, 6, {"lines.2.atS": "p2"}),
    # ── 1 · the engine ──────────────────────────────────────────────────────
    beat("B01A", "1 engine",
         "When a language model writes, it doesn't retrieve an answer. For every possible "
         "next token, it produces a raw score called a logit.",
         {"mode": "pipeline", "step": 1, "title": "How the next token is chosen",
          "label": "diagram"}, 8, {"stepAtS": "p2"}),
    beat("B01B", "1 engine",
         "Those scores get converted into probabilities that add up to one. That conversion "
         "is called softmax: it makes every score positive, then divides each by the total.",
         {"mode": "pipeline", "step": 2, "title": "How the next token is chosen",
          "label": "diagram"}, 9),
    beat("B01C", "1 engine",
         "Then the model rolls a weighted die and picks one. That's the loop.",
         {"mode": "pipeline", "step": 3, "title": "How the next token is chosen",
          "label": "diagram"}, 5, {"captionAtS": "p1"}),
    beat("B01D", "1 engine",
         "Today I want to show you one thing about the conversion step: what it keeps, "
         "and what it silently throws away.",
         {"mode": "pipeline", "step": 4, "title": "How the next token is chosen",
          "label": "diagram"}, 7, {"captionAtS": "p1"}),
    # ── 2 · real output ─────────────────────────────────────────────────────
    beat("B02A", "2 real output",
         "Here are real numbers from the course lesson file. Three candidate tokens, "
         "with scores one, two, and three.",
         table(probsAtS=-1), 7),
    beat("B02B", "2 real output",
         "Run it, and softmax turns them into nine point zero zero percent, twenty-four "
         "point four seven percent, and sixty-six point five two percent.",
         table(probsAtS=0.9), 9, {"probsAtS": "p1"}),
    beat("B02C", "2 real output",
         "This is actual printed output, not an illustration.",
         table(probsAtS=0, sourceAtS=0.4), 3),
    # ── 3 · the test (mechanism) ────────────────────────────────────────────
    beat("B03A", "3 the test",
         "Now a test. I'm going to add one thousand to every score. One thousand and one, "
         "one thousand and two, one thousand and three. The inputs are now enormous.",
         {"mode": "shift", "logits": [1, 2, 3], "probs": probs_ref, "pcts": pcts,
          "offsetTo": 1000, "countStartS": 1.2, "countDurS": 2.5, "sweepAtS": 7.0,
          "title": "Add 1000 to every score", "label": "recorded output",
          "footer": f"Checked every whole-number offset 0 to 1000: {sweep_n} of {sweep_n} "
                    "outputs bitwise identical (intermediates-output.txt).",
          "source": SRC_OFFSET}, 10,
         {"countStartS": "p1", "sweepAtS": "p4"}),
    beat("B03B", "3 the test",
         "Watch the percentages. They don't move. Not approximately. Bitwise identical, "
         "every digit the same. The thousand vanished.",
         {"mode": "compare", "title": "Every printed digit, both runs",
          "label": "recorded output",
          "runs": [{"label": "[1, 2, 3]", "values": [repr(x) for x in base]},
                   {"label": "[1001, 1002, 1003]", "values": [repr(x) for x in shifted]}],
          "verdict": identical_line, "verdictAtS": 3.4, "source": SRC_OFFSET}, 8,
         {"verdictAtS": "p3"}),
    beat("B03C", "3 the test",
         "Here's why. Softmax divides each score's exponential by the total. Adding a "
         "thousand multiplies every exponential by the same factor, on top and on the "
         "bottom, so it cancels.",
         {"mode": "cancel", "title": "Why the thousand cancels",
          "label": "constructed diagram", "probsAtS": 3.8, "verdictAtS": 7.5}, 10,
         {"probsAtS": "p2", "verdictAtS": "p4"}),
    beat("B03D", "3 the test",
         "And because this code subtracts the largest score first, both runs compute the "
         "exact same intermediate numbers. That's why every digit matches.",
         {"mode": "intermediates", "title": "Why the digits match exactly",
          "label": "recorded output",
          "runs": [{"label": "[1, 2, 3]", "values": [minus_max[0]]},
                   {"label": "[1001, 1002, 1003]", "values": [minus_max[1]]}],
          "probsAtS": 1.6, "verdictAtS": 4.2,
          "footer": "Identical numbers go into exp(), so identical digits come out.",
          "source": SRC_INTER}, 8,
         {"verdictAtS": "p2"}),
    # ── 4 · the punchline ───────────────────────────────────────────────────
    beat("B04A", "4 punchline",
         "So what happens with one thousand and one thousand? Fifty-fifty. A coin flip.",
         rows([r(r1000, at=0.3, outAtS=2.8)]), 5,
         {"rows.0.outAtS": "p1"}),
    beat("B04B", "4 punchline",
         "Zero and zero? Fifty-fifty. Negative five and negative five? Fifty-fifty.",
         rows([r(r1000), r(r00, at=0.1, outAtS=1.4), r(r55, at=2.4, outAtS=4.4)]), 6,
         {"rows.1.outAtS": "p1", "rows.2.appearAtS": "p2", "rows.2.outAtS": "p3"}),
    beat("B04C", "4 punchline",
         "The size carried nothing. Only the gap survives. One and two gives twenty-six "
         "point eight nine and seventy-three point one one. And one thousand and one, "
         "one thousand and two gives exactly the same.",
         rows([r(r1000, dim=True), r(r00, dim=True), r(r55, dim=True),
               r(r12, at=3.7, outAtS=4.6, highlight=True),
               r(r1001, at=8.3, outAtS=9.9, highlight=True)]), 11,
         {"rows.3.appearAtS": "p2", "rows.3.outAtS": "p2+0.9",
          "rows.4.appearAtS": "p3", "rows.4.outAtS": "p4"}),
    beat("B04D", "4 punchline",
         "A huge logit is not a confident model. One caveat: the code only returns these "
         "numbers because it subtracts the max first. A naive version raises an overflow "
         "error at one thousand.",
         rows([r(r1000, highlight=True)], footer="A huge logit is not a confident model.",
              footerAtS=0.3, errorInput=naive_head, errorOutput=naive_err, errorAtS=5.0), 11,
         {"errorAtS": "p3"}),
    # ── 5 · the boundary ────────────────────────────────────────────────────
    beat("B05", "5 boundary",
         "One thing this does not establish. It shows that the size of the scores carries "
         "no information once softmax runs. It does not show that the resulting "
         "probabilities are calibrated. Sixty-six point five two percent is not evidence "
         "that the token is correct sixty-six point five two percent of the time. Nothing "
         "here says the model is right.",
         {"mode": "card", "light": True, "bodyScale": 1.12, "lines": [
             {"text": "WHAT THIS DOES NOT SHOW", "atS": 0.3},
             {"text": "Shown: the shared size of the scores carries no information after softmax.", "atS": 2.5},
             {"text": "Not shown: that the probabilities are calibrated.", "atS": 7.0},
             {"text": f"{pcts[2]} is not evidence of being right {pcts[2]} of the time.", "atS": 10.5},
             {"text": "Nothing here says the model is right.", "atS": 17.0, "strong": True},
         ]}, 20,
         {"lines.1.atS": "p1", "lines.2.atS": "p2", "lines.3.atS": "p3", "lines.4.atS": "p6"}),
    # ── 6 · the close (added after draft 1: the ending felt abrupt) ─────────
    beat("B06", "6 close",
         "So, in one line: softmax keeps the gaps and throws away the size. A big score, "
         "on its own, is not confidence.",
         {"mode": "card", "light": True, "bodyScale": 1.45, "lines": [
             {"text": "IN ONE LINE", "atS": 0.3},
             {"text": "Softmax keeps the gaps between scores.", "atS": 1.2},
             {"text": "It throws away their shared size.", "atS": 3.0},
             {"text": "A big score, on its own, is not confidence.", "atS": 5.0, "strong": True},
         ]}, 8, {"lines.1.atS": "p1", "lines.2.atS": "p1+1.6", "lines.3.atS": "p2"}),
]

# Text cards reveal one line per spoken sentence, so a mid-beat frame is emptier
# by design. Declared for Gate V (toolkit: qc.sparse_by_design); the fully
# revealed card is sized to fill the frame on its own.
SPARSE = "line-by-line reveal timed to the narration; the full card fills the safe area"
for b in beats:
    if b["shot"]["remotion"]["props"]["mode"] == "card":
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE}

old_path = HERE / "beat_sheet.json"
if old_path.exists():
    old = {b["beat_id"]: b for b in json.loads(old_path.read_text())["beats"]}
    for b in beats:
        o = old.get(b["beat_id"])
        if o and o.get("narration_text") == b["narration_text"]:
            for k in ("audio_file", "actual_duration_s"):
                if k in o:
                    b[k] = o[k]

sheet = {
    "metadata": {
        "slug": "w1-softmax-offset",
        "title": "[1000, 1000] → [0.5, 0.5]: what the shared offset never carried",
        "topic": "INFO 7375 · WEEK 1 · SOFTMAX",
        "purpose": "Softmax only sees the gaps between logits; the shared magnitude is "
                   "discarded, so a logit's size is not a measure of confidence.",
        "author": "Ashwin Thankachan",
        "course": "INFO 7375 — Prompt Engineering for Generative AI (Northeastern)",
        "clock": "narration",
        "engine": "kokoro",
        "voice_kokoro": "af_bella",
        "voice_note": "Kokoro af_bella is a synthetic voice, not the author's.",
        "aspect": "16:9",
        "evidence": ["w1-evidence/reference-output.txt", "w1-evidence/offset-output.txt",
                     "w1-evidence/intermediates-output.txt"],
    },
    "beats": beats,
}
(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
print(f"wrote beat_sheet.json — {len(beats)} beats")
