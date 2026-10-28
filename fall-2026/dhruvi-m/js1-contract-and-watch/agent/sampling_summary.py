"""Summarize sampling runs: rule verdict vs. Claude verdicts per posting (v1)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import watch
from validate import validate

persona = json.loads(Path("persona/priya_nair.json").read_text())
jobs = {j["id"]: j for j in json.loads(Path("evidence/manual-snapshots/stripe_2026-10-27T232715Z.json").read_text())["jobs"]}
print("posting_id | rule verdict | Claude verdicts (runs 1-4) | valid | resume fields cited per run")
for pid in (8189909, 5416444, 8222149, 8026689, 7440963):
    rule = watch.judge(jobs[pid], persona)["rule_verdict"]
    verdicts, cites, valid = [], [], 0
    for run in range(1, 5):
        ok, errs, obj = validate(Path(f"responses/v1_{pid}_run{run}.json").read_text(), pid)
        valid += ok
        verdicts.append(obj["verdict"] if ok else "INVALID")
        cites.append(",".join(sorted(obj["cited_resume_fields"])) if ok else "-")
    print(f"{pid} | {rule} | {verdicts} | {valid}/4 | {cites}")
