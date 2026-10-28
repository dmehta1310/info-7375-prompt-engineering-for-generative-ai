"""Score v1/v2 replies against my hand labels (DEV: v1 only; HELDOUT: v1 and v2)."""
import json, sys
from pathlib import Path
sys.path.insert(0, "agent")
from validate import validate
L = json.load(open("experiment/labels.json")); s = json.load(open("experiment/split.json"))
def verdict(v, i):
    ok, errs, obj = validate(Path(f"experiment/responses/{v}_{i}.json").read_text(), i)
    return obj["verdict"] if ok else "INVALID"
dev = [(i, L[str(i)]["my_label"], verdict("v1", i)) for i in s["dev"]]
print("DEV (v1 only)")
for i, m, a in dev: print(f"  {i} | mine: {m:12} | v1: {a:12} | {'match' if a == m else 'DISAGREE'}")
print(f"  v1 DEV: {sum(a == m for _, m, a in dev)}/10")
print("\nHELDOUT (v1 vs v2)")
rows = [(i, L[str(i)]["my_label"], verdict("v1", i), verdict("v2", i)) for i in s["heldout"]]
for i, m, a, b in rows: print(f"  {i} | mine: {m:12} | v1: {a:12} | v2: {b:12}")
print(f"  v1 HELDOUT: {sum(a == m for _, m, a, _ in rows)}/10")
print(f"  v2 HELDOUT: {sum(b == m for _, m, _, b in rows)}/10")
print(f"  v1 and v2 gave the same verdict on {sum(a == b for _, _, a, b in rows)}/10")
print(f"  relevant postings in HELDOUT (by my labels): {sum(m == 'relevant' for _, m, _, _ in rows)}")
