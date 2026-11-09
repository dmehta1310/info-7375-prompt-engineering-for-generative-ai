"""INDEPENDENT check of a run. Does not import the agent's loop or parsers.

It recounts jobs straight from the saved raw files, and compares them with
(a) what the report claims and (b) the last approved state file.

  python3 agent/check.py out/runs/<run folder>
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def recount(raw):
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if isinstance(data, list):                      # Lever
        return len(data)
    if isinstance(data, dict) and isinstance(data.get("jobs"), list):  # Greenhouse, Ashby
        return len(data["jobs"])
    return None


def main(run_dir):
    run_dir = Path(run_dir)
    report = json.loads((run_dir / "report.json").read_text())
    state_f = ROOT / "state" / "seen_ids.json"
    state = json.loads(state_f.read_text()) if state_f.exists() else {}
    problems = []
    for name, r in report["boards"].items():
        raw_f = run_dir / "raw" / f"{name}.json"
        n = recount(raw_f.read_text()) if raw_f.exists() else None
        prev = len(state.get(name, []))
        line = f"  {name:10} report={r['status']:16} recount={n}  last-approved={prev}"
        if r["status"] == "ok" and n != r["count"]:
            problems.append(f"{name}: report says {r['count']} jobs, raw file has {n}")
        if r["status"] == "ok" and n == 0 and prev > 0:
            problems.append(f"{name}: 0 jobs now but {prev} last time; 'no new jobs' is not believable")
        print(line)
    if report["status"] == "finished" and any(r["status"] != "ok" for r in report["boards"].values()):
        problems.append("report says finished but not every board is ok")
    print(f"agent's own status: {report['status']}  ({report.get('label')})")
    if problems:
        print("INDEPENDENT CHECK: FAIL")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("INDEPENDENT CHECK: PASS")


if __name__ == "__main__":
    main(sys.argv[1])
