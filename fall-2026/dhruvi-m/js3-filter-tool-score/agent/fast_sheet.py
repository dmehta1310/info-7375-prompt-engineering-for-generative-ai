"""Fast judging (same verdicts, less reading). The filter's own verdict stays hidden.

  python3 agent/fast_sheet.py sheet               # print one short line per posting not judged yet
  python3 agent/fast_sheet.py save "n3 y1 n2 ..."  # save MY answers, in the sheet's order

Answer format per posting: a letter (y / n / ?) followed by a reason code:
  1 data/analytics work that fits Priya    2 says "Analyst" but not data work   3 not in the US
  4 too senior                             5 internship / student only           6 different field
  7 not enough info in the text            8 other
"""
import json
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "agent"))
from filter import min_years, skills_found  # noqa: E402
from postings import load_raw_dir  # noqa: E402

V = "v1"
RAW = ROOT.parent / "js2-loop-tools-diff/out/runs/2026-11-09T220326Z_LIVE/raw"
SAMPLE = ROOT / "audit" / f"{V}_sample.json"
HAND = ROOT / "audit" / f"{V}_hand_verdicts.json"
ORDER = ROOT / "audit" / f"{V}_sheet_order.json"
CODES = {"1": "data/analytics work that fits Priya", "2": "says 'Analyst' but not data work",
         "3": "not in the US", "4": "too senior", "5": "internship / student only",
         "6": "different field", "7": "not enough info in the text", "8": "other"}
SKILLS = ["SQL", "Python", "Tableau", "dbt", "A/B testing", "Excel"]
ROLE = re.compile(r"(The Role|About the role|About the team|What you.ll do|In this role|As an? [A-Z][\w &,/-]{2,60}, you will)", re.I)


def role_line(text):
    m = ROLE.search(text or "")
    s = (text or "")[m.end():] if m else (text or "")[300:]
    return re.sub(r"\s+", " ", s).strip()[:150]


def sheet():
    samp = json.loads(SAMPLE.read_text())
    hand = json.loads(HAND.read_text()) if HAND.exists() else {}
    posts = {f"{p['board']}:{p['id']}": p for p in load_raw_dir(RAW)[0]}
    todo = [i["key"] for i in samp["items"] if i["key"] not in hand]
    random.Random(7376).shuffle(todo)
    ORDER.write_text(json.dumps(todo, indent=1))
    print(f"{len(todo)} postings to judge (filter verdict hidden). Answer each with y/n/? + code, e.g. n3")
    print("codes: " + " | ".join(f"{k} {v}" for k, v in CODES.items()) + "\n")
    for n, k in enumerate(todo, 1):
        p = posts[k]
        yrs = min_years(p["text"])
        sk = skills_found(p["text"], SKILLS)
        print(f"{n:2}. {p['title']}  |  {p['location'] or '(no location)'}")
        print(f"    job: {role_line(p['text']) or '(no description)'}")
        print(f"    years asked: {yrs if yrs is not None else 'not stated'}  |  skills: {', '.join(sk) or 'none'}")


def save(answers):
    todo = json.loads(ORDER.read_text())
    toks = answers.replace(",", " ").split()
    if len(toks) != len(todo):
        sys.exit(f"STOP: got {len(toks)} answers but the sheet has {len(todo)}. Nothing saved.")
    hand = json.loads(HAND.read_text()) if HAND.exists() else {}
    for k, t in zip(todo, toks):
        if not re.fullmatch(r"[yn?][1-8]", t):
            sys.exit(f"STOP: '{t}' is not like y1 / n3 / ?7. Nothing saved.")
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for k, t in zip(todo, toks):
        hand[k] = {"verdict": t[0], "why": f"code {t[1]}: {CODES[t[1]]}", "judged_at": now, "method": "sheet"}
    HAND.write_text(json.dumps(hand, indent=1))
    print(f"saved {len(hand)} verdicts to {HAND}")


if __name__ == "__main__":
    if sys.argv[1:2] == ["sheet"]:
        sheet()
    elif sys.argv[1:2] == ["save"] and len(sys.argv) == 3:
        save(sys.argv[2])
    else:
        sys.exit(__doc__)
