"""Prints every number that appears on screen in the reel."""
import json, math, platform, sys
from main import probabilities, sample

SCORES = [1, 2, 3]
TEMPS = [0.5, 1.0, 2.0]
out = {"python": platform.python_version(), "scores": SCORES, "rows": []}
for T in TEMPS:
    p = probabilities(SCORES, T)
    c = sample(SCORES, count=1000, seed=7, temperature=T)
    counts = [c.get(i, 0) for i in range(len(SCORES))]
    ratio_2_0 = p[2] / p[0]
    out["rows"].append({"T": T, "p": [round(x, 10) for x in p],
                        "counts_seed7_n1000": counts,
                        "ratio_p2_over_p0": round(ratio_2_0, 4),
                        "exp_check": round(math.exp((3 - 1) / T), 4)})
    print(f"T={T}: p={[f'{x:.10f}' for x in p]}  counts={counts}  p2/p0={ratio_2_0:.4f}  exp(2/T)={math.exp(2/T):.4f}")
# ordering survives: argmax is always outcome 2
assert all(max(range(3), key=lambda i: r["p"][i]) == 2 for r in out["rows"])
# temperature 0 is rejected by this interface
try:
    probabilities(SCORES, 0)
except ValueError as e:
    print("T=0 ->", e); out["T0"] = str(e)
json.dump(out, open("temperature_results.json", "w"), indent=2)
print("python", out["python"])
