"""Measure filter versions against MY hand labels (Chapter 9: one change at a time).

  python3 agent/measure.py --part dev      config/filter_v1.json config/cand_A_north_america.json ...
  python3 agent/measure.py --part heldout  config/filter_v1.json config/filter_v2.json

A filter verdict of 'relevant' counts as "shown to me". 'rejected' and 'cannot_tell' count as
"not shown". It is compared with my verdict y (worth Priya's time) / n (not worth it).
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "agent"))
from filter import judge  # noqa: E402
from postings import load_raw_dir  # noqa: E402

RAW = ROOT.parent / "js2-loop-tools-diff/out/runs/2026-11-09T220326Z_LIVE/raw"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", choices=["dev", "heldout"], required=True)
    ap.add_argument("configs", nargs="+")
    a = ap.parse_args()
    split = json.loads((ROOT / "audit/label_split.json").read_text())
    hand = json.loads((ROOT / "audit/v1_hand_verdicts.json").read_text())
    posts = {f"{p['board']}:{p['id']}": p for p in load_raw_dir(RAW)[0]}
    keys = [k for k in split[a.part] if hand[k]["verdict"] in ("y", "n")]
    ny = sum(hand[k]["verdict"] == "y" for k in keys)
    print(f"{a.part}: {len(keys)} of my labels ({ny} yes, {len(keys) - ny} no)\n")
    print(f"{'filter':26} {'agree':>7} {'shown,me=n':>11} {'hidden,me=y':>12} {'cannot_tell':>12}")
    out = []
    for c in a.configs:
        cfg = json.loads(Path(c).read_text())
        agree = fp = fn = ct = 0
        changed = []
        for k in keys:
            v = judge(posts[k], cfg)["verdict"]
            shown = v == "relevant"
            me = hand[k]["verdict"] == "y"
            ct += v == "cannot_tell"
            agree += shown == me
            fp += shown and not me
            fn += me and not shown
        row = {"filter": cfg["version"], "n": len(keys), "agree": agree, "shown_but_me_n": fp,
               "hidden_but_me_y": fn, "cannot_tell": ct}
        out.append(row)
        print(f"{cfg['version']:26} {agree:>3}/{len(keys):<3} {fp:>11} {fn:>12} {ct:>12}")
    dest = ROOT / "out" / "measure"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"{a.part}.json").write_text(json.dumps(out, indent=1))
    print(f"\nsaved {dest / (a.part + '.json')}")


if __name__ == "__main__":
    main()
