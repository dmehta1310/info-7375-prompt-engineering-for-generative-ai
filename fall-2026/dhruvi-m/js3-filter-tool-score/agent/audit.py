"""The reject audit (FILTER.md + Chapter 7).

  python3 agent/audit.py sample  --version v1   # draw the sample (seed 7375), saved to audit/v1_sample.json
  python3 agent/audit.py judge   --version v1   # I judge each one by hand (filter verdict hidden)
  python3 agent/audit.py report  --version v1   # compare my verdicts with the filter's
"""
import argparse
import json
import math
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "agent"))
from postings import load_raw_dir  # noqa: E402

SEED = 7375
NEAR_WORDS = r"\b(data|analysis|analyses|insights?|business intelligence|bi|quantitative|statistic\w*|scientist|reporting)\b"


def paths(v):
    a = ROOT / "audit"
    a.mkdir(exist_ok=True)
    return ROOT / "out" / v / "results.json", a / f"{v}_sample.json", a / f"{v}_hand_verdicts.json"


def sample(v, n_rej=30, n_close=10, n_kept=10, n_cannot=5):
    res_p, samp_p, _ = paths(v)
    res = json.loads(res_p.read_text())
    rng = random.Random(SEED)
    rej = [r for r in res if r["verdict"] == "rejected"]
    kept = [r for r in res if r["verdict"] == "relevant"]
    cant = [r for r in res if r["verdict"] == "cannot_tell"]
    rand_rej = rng.sample(rej, min(n_rej, len(rej)))
    # closest calls: rejects that passed the title rule (failed only on location) first,
    # then US-or-unknown rejects whose title has a near-miss word
    close = [r for r in rej if r["checks"].get("title_word")]
    close += [r for r in rej if not r["checks"].get("title_word") and re.search(NEAR_WORDS, r["title"], re.I)]
    close = close[:n_close]
    items = {}
    for tag, group in (("random_reject", rand_rej), ("close_call", close),
                       ("kept", rng.sample(kept, min(n_kept, len(kept)))),
                       ("cannot_tell", rng.sample(cant, min(n_cannot, len(cant))))):
        for r in group:
            key = f"{r['board']}:{r['id']}"
            items.setdefault(key, {"key": key, "board": r["board"], "id": r["id"], "tags": [],
                                   "filter_verdict": r["verdict"], "filter_reasons": r["reasons"]})
            items[key]["tags"].append(tag)
    out = {"version": v, "seed": SEED, "drawn_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "population": {"rejected": len(rej), "relevant": len(kept), "cannot_tell": len(cant)},
           "items": list(items.values())}
    samp_p.write_text(json.dumps(out, indent=1))
    c = {t: sum(t in i["tags"] for i in out["items"]) for t in ("random_reject", "close_call", "kept", "cannot_tell")}
    print(f"sample saved: {samp_p}  ({len(out['items'])} postings to judge) {c}")
    print(f"population: {out['population']}")


def judge(v, raw):
    _, samp_p, hand_p = paths(v)
    samp = json.loads(samp_p.read_text())
    posts = {f"{p['board']}:{p['id']}": p for p in load_raw_dir(raw)[0]}
    hand = json.loads(hand_p.read_text()) if hand_p.exists() else {}
    todo = [i for i in samp["items"] if i["key"] not in hand]
    rng = random.Random(SEED + 1)
    rng.shuffle(todo)  # mixed order, so I can't tell which group a posting came from
    print("Judge as Priya: data analyst, 2 years' experience, US-based.")
    print("y = worth her time to apply   n = not worth it   ? = I cannot tell   q = save and stop\n")
    for k, i in enumerate(todo, 1):
        p = posts.get(i["key"])
        if not p:
            continue
        print("=" * 78)
        print(f"[{len(hand) + 1}/{len(samp['items'])}]  {p['board']}  #{p['id']}")
        print(f"TITLE:    {p['title']}\nLOCATION: {p['location'] or '(missing)'}")
        print(f"TEXT:     {(p['text'] or '(missing)')[:900]}{' ...' if len(p['text']) > 900 else ''}")
        while True:
            a = input("Worth Priya's time? [y/n/?/q]: ").strip().lower()
            if a in ("y", "n", "?", "q"):
                break
        if a == "q":
            break
        why = input("Why (short, Enter to skip): ").strip()
        hand[i["key"]] = {"verdict": a, "why": why,
                          "judged_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        hand_p.write_text(json.dumps(hand, indent=1))
    print(f"\nsaved {len(hand)} of {len(samp['items'])} verdicts to {hand_p}")


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, (c - m) / d), min(1.0, (c + m) / d))


def report(v):
    _, samp_p, hand_p = paths(v)
    samp = json.loads(samp_p.read_text())
    hand = json.loads(hand_p.read_text())
    rows = []
    for tag, wrong_if in (("random_reject", "y"), ("close_call", "y"), ("kept", "n"), ("cannot_tell", None)):
        grp = [i for i in samp["items"] if tag in i["tags"] and i["key"] in hand]
        judged = [i for i in grp if hand[i["key"]]["verdict"] != "?"]
        wrong = [i for i in judged if wrong_if and hand[i["key"]]["verdict"] == wrong_if]
        lo, hi = wilson(len(wrong), len(judged))
        rows.append((tag, len(grp), len(judged), len(wrong), lo, hi, wrong))
        print(f"{tag:13} judged {len(judged):2} of {len(grp):2} (rest '?')  filter wrong: {len(wrong):2}"
              + (f"   95% Wilson interval {lo:.0%}-{hi:.0%}" if wrong_if else
                 "   (my verdicts: " + ", ".join(f"{a}={sum(hand[i['key']]['verdict'] == a for i in grp)}" for a in 'yn?') + ")"))
        for i in wrong:
            print(f"     WRONG: {i['key']}  filter={i['filter_verdict']}  me={hand[i['key']]['verdict']}  why: {hand[i['key']]['why']}")
    rej = samp["population"]["rejected"]
    rr = rows[0]
    print(f"\nrandom rejects: {rr[3]} wrong of {rr[2]} judged, from {rej} rejected postings in all.")
    print(f"A sample this size is consistent with a true miss rate anywhere from {rr[4]:.0%} to {rr[5]:.0%} "
          f"of all {rej} rejects (95% Wilson interval). It is an estimate, not a measured rate.")
    json.dump({"version": v, "rows": [r[:6] for r in rows]}, open(ROOT / "audit" / f"{v}_audit_numbers.json", "w"), indent=1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["sample", "judge", "report"])
    ap.add_argument("--version", default="v1")
    ap.add_argument("--raw", default=str(ROOT.parent / "js2-loop-tools-diff/out/runs/2026-11-09T220326Z_LIVE/raw"))
    a = ap.parse_args()
    {"sample": lambda: sample(a.version), "judge": lambda: judge(a.version, a.raw), "report": lambda: report(a.version)}[a.cmd]()
