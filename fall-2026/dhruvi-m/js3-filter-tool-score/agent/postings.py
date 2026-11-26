"""Load postings from saved raw board responses and normalize them.

Each posting becomes {board, id, title, location, text, missing}. `missing` lists the
fields FILTER.md says the agent needs but the posting does not have.
"""
import html
import json
import re
from pathlib import Path

ATS = {"stripe": "greenhouse", "palantir": "lever", "linear": "ashby"}


def clean(text):
    t = html.unescape(html.unescape(text or ""))
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def _norm(board, j):
    ats = ATS.get(board)
    if ats == "greenhouse":
        title, loc, text = j.get("title"), (j.get("location") or {}).get("name"), j.get("content")
    elif ats == "lever":
        title = j.get("text")
        loc = (j.get("categories") or {}).get("location")
        text = " ".join([j.get("descriptionPlain") or ""] +
                        [(x.get("text") or "") + " " + clean(x.get("content", "")) for x in (j.get("lists") or [])])
    else:
        title, loc = j.get("title"), j.get("location")
        text = j.get("descriptionPlain") or j.get("descriptionHtml")
    p = {"board": board, "id": str(j.get("id")), "title": (title or "").strip(),
         "location": (loc or "").strip(), "text": clean(text)}
    p["missing"] = [f for f in ("title", "location", "text") if not p[f]]
    return p


def load_raw_dir(raw_dir):
    """Read <board>.json files written by my JS2 agent. Failed boards are skipped and reported."""
    postings, skipped = [], {}
    for f in sorted(Path(raw_dir).glob("*.json")):
        board = f.stem
        if board not in ATS:
            skipped[board] = "not an expected source (see FILTER.md)"
            continue
        try:
            data = json.loads(f.read_text())
        except ValueError:
            skipped[board] = "not valid JSON"
            continue
        jobs = data["jobs"] if isinstance(data, dict) and "jobs" in data else data
        if not isinstance(jobs, list):
            skipped[board] = "unexpected shape"
            continue
        postings += [_norm(board, j) for j in jobs]
    return postings, skipped
