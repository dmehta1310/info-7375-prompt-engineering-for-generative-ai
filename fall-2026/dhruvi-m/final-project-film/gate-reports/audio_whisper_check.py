import json, re, difflib, sys
from pathlib import Path
from faster_whisper import WhisperModel
HERE = Path(__file__).resolve().parent.parent
model = WhisperModel("small.en", device="cpu", compute_type="int8")
sheet = json.load(open(HERE / "beat_sheet.json"))
def norm(t):
    t = t.lower().replace("-", " ").replace("’", "'")
    return re.findall(r"[a-z0-9']+", t)
out = {}
for b in sheet["beats"]:
    segs, _ = model.transcribe(str(HERE / b["audio_file"]), language="en", beam_size=5)
    heard = " ".join(s.text.strip() for s in segs)
    want = b["narration_text"]
    a, h = norm(want), norm(heard)
    diffs = [(op, " ".join(a[i1:i2]), " ".join(h[j1:j2]))
             for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, h).get_opcodes() if op != "equal"]
    out[b["beat_id"]] = {"script": want, "heard": heard, "diffs": diffs}
json.dump(out, open(HERE / "_qc" / "whisper_transcripts.json", "w"), indent=2, ensure_ascii=False)
for k, v in out.items():
    print(k, "MATCH" if not v["diffs"] else "DIFF")
    print("  heard:", v["heard"])
    for d in v["diffs"]: print("  ", d)
