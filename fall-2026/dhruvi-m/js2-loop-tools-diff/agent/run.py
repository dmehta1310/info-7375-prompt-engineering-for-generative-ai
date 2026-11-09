"""Command line entry point.

  python3 agent/run.py                         live run of config/boards.json
  python3 agent/run.py --seed DIR              SEEDED run: responses come from DIR/<board>.json
  python3 agent/run.py --wrong-empty-rule ...  the WRONG version (demo only): empty board counted as fine
  python3 agent/run.py --approve PROPOSAL      apply a state proposal (needs my explicit approval)
"""
import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from loop import run_loop  # noqa: E402
from policy import (CONFIG, OUT, STATE_FILE, check_read, check_state_write,  # noqa: E402
                    check_write)


def write(path: Path, text: str):
    p = check_write(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def seeded_fetch(seed_dir: Path, boards):
    by_url = {}
    from boards import board_url
    for b in boards:
        by_url[board_url(b["ats"], b["slug"])] = seed_dir / f"{b['name']}.json"

    def fetch(url, timeout):
        f = by_url[url]
        if not f.exists():
            return 404, b'{"seeded": "missing file = 404"}'
        return 200, f.read_bytes()
    return fetch


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--boards", default=str(CONFIG / "boards.json"))
    ap.add_argument("--seed", help="SEEDED run: read responses from this folder")
    ap.add_argument("--wrong-empty-rule", action="store_true", help="demo of the WRONG version")
    ap.add_argument("--approve", help="apply this state proposal to state/seen_ids.json")
    a = ap.parse_args()

    if a.approve:
        prop = json.loads(check_read(a.approve).read_text())
        target = check_state_write(STATE_FILE, approved=True)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(prop, indent=2))
        print(f"APPROVED: wrote {target.name} from {a.approve}")
        return

    boards = json.loads(check_read(a.boards).read_text())
    budget = json.loads(check_read(CONFIG / "budget.json").read_text())
    seen = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}
    fetch_kw = {}
    label = "LIVE"
    if a.seed:
        fetch_kw["fetch"] = seeded_fetch(Path(a.seed), boards)
        label = "SEEDED"
    if a.wrong_empty_rule:
        label += "-WRONG-VERSION"

    report = run_loop(boards, budget, seen, empty_rule=not a.wrong_empty_rule, **fetch_kw)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    run_dir = OUT / "runs" / f"{stamp}_{label}"
    for name, r in report["boards"].items():
        raw = r.pop("raw", None)
        r.pop("jobs", None)
        if raw is not None:
            write(run_dir / "raw" / f"{name}.json", raw.decode("utf-8", "replace"))
    report.update({"label": label, "utc": stamp, "boards_file": a.boards})
    write(run_dir / "trace.json", json.dumps(report.pop("trace"), indent=2))
    write(run_dir / "report.json", json.dumps(report, indent=2))
    proposal = {n: r["ids"] for n, r in report["boards"].items() if r["status"] == "ok"}
    write(run_dir / "state_proposal.json", json.dumps(proposal, indent=2))

    print(f"[{label}] status: {report['status'].upper()}  "
          f"requests: {report['requests_used']}  seconds: {report['seconds']}")
    for n, r in report["boards"].items():
        extra = (f"{r['count']} jobs, {len(r['new_ids'])} new" + (" (baseline)" if r.get("baseline") else "")
                 if r["status"] == "ok" else r.get("reason", ""))
        print(f"  {n:10} {r['status']:16} {extra}")
    if report["never_attempted"]:
        print(f"  never attempted: {report['never_attempted']}")
    print(f"saved: {run_dir.relative_to(OUT.parent)}")
    print("state NOT changed. To accept this run's IDs, run:")
    print(f"  python3 agent/run.py --approve {(run_dir / 'state_proposal.json').relative_to(OUT.parent)}")


if __name__ == "__main__":
    main()
