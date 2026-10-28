"""Print title, location and the requirements part of postings, for hand-labeling."""
import json, sys
sys.path.insert(0, "agent")
import watch
jobs = {j["id"]: j for j in json.load(open("evidence/manual-snapshots/stripe_2026-10-27T232715Z.json"))["jobs"]}
for n, pid in enumerate(map(int, sys.argv[1:]), 1):
    j = jobs[pid]; t = watch.clean(j["content"])
    i = t.find("Minimum requirements")
    if i < 0: i = t.find("Who you are")
    print("=" * 70)
    print(f"JOB {n}: {pid}\nTITLE:    {j['title']}\nLOCATION: {j['location']['name']}\n")
    print(t[i:i+600] if i >= 0 else "(no 'Minimum requirements' section found: " + t[:600] + ")")
print("=" * 70)
