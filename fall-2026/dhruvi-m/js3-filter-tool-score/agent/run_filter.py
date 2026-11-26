"""Run a filter version on every posting in a saved raw folder.

python3 agent/run_filter.py --raw ../js2-loop-tools-diff/out/runs/2026-11-09T220326Z_LIVE/raw --filter config/filter_v1.json
Writes out/<version>/results.json and summary.json, and prints the counts.
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from filter import judge  # noqa: E402
from postings import load_raw_dir  # noqa: E402

ROOT = HERE.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True)
    ap.add_argument("--filter", default=str(ROOT / "config" / "filter_v1.json"))
    args = ap.parse_args()
    cfg = json.loads(Path(args.filter).read_text())
    postings, skipped = load_raw_dir(args.raw)
    results = []
    for p in postings:
        r = judge(p, cfg)
        results.append({**{k: p[k] for k in ("board", "id", "title", "location", "missing")}, **r})
    out = ROOT / "out" / cfg["version"]
    out.mkdir(parents=True, exist_ok=True)
    (out / "results.json").write_text(json.dumps(results, indent=1))
    by = Counter((r["board"], r["verdict"]) for r in results)
    total = Counter(r["verdict"] for r in results)
    summary = {"filter": cfg["version"], "raw": args.raw, "postings": len(results),
               "verdicts": dict(total), "by_board": {f"{b}/{v}": n for (b, v), n in sorted(by.items())},
               "boards_not_judged": skipped}
    (out / "summary.json").write_text(json.dumps(summary, indent=1))
    print(f"[filter {cfg['version']}] {len(results)} postings from {args.raw}")
    for v in ("relevant", "cannot_tell", "rejected"):
        print(f"  {v:12} {total.get(v, 0)}")
    for b in sorted({r['board'] for r in results}):
        print(f"  {b:9} " + "  ".join(f"{v}={by.get((b, v), 0)}" for v in ("relevant", "cannot_tell", "rejected")))
    for b, why in skipped.items():
        print(f"  NOT JUDGED: {b} ({why})")
    print("  relevant postings:")
    for r in results:
        if r["verdict"] == "relevant":
            print(f"    {r['board']:9} {r['id']:>12}  {r['title']}  |  {r['location']}")
    print(f"saved: {out}/results.json")


if __name__ == "__main__":
    main()
