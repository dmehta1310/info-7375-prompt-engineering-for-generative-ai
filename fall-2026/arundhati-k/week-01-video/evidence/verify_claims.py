#!/usr/bin/env python3
"""
verify_claims.py — re-check every number the video puts on screen.

Run it from anywhere; it locates the lesson code itself. No dependencies
beyond the standard library, same as the lesson.

    python3 verify_claims.py

Each row asserts a value that appears in the reel against a value computed
from lessons/01-randomness-and-first-prompts/code/main.py, unmodified.
If main.py ever changes, main.py wins and this script fails loudly — the
video's constants are the thing that would be wrong, not the code.

Exit 0 = every claim reproduced. Exit 1 = at least one drifted.
"""
import math
import sys
from pathlib import Path

LESSON = "lessons/01-randomness-and-first-prompts/code"


def locate_lesson():
    """Walk up from this file until the lesson code is found."""
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / LESSON
        if (candidate / "main.py").is_file():
            return candidate
    sys.exit(f"could not find {LESSON}/main.py above {here}")


sys.path.insert(0, str(locate_lesson()))
from main import probabilities, sample  # noqa: E402

CHECKS = []


def check(label, claimed, actual, tol=None):
    ok = (abs(float(claimed) - float(actual)) <= tol) if tol is not None else (claimed == actual)
    CHECKS.append((label, ok, f"claimed {claimed!r} · actual {actual!r}"))


# ── the two calls the whole video rests on ──────────────────────────────────
p = probabilities([1, 2, 3])
counts = sample([1, 2, 3])          # count=1000, seed=7, temperature=1.0

n = 1000
prob2 = p[2]
expected = prob2 * n
observed = counts[2]
gap = expected - observed
gap_pct = gap / expected * 100
sd = math.sqrt(n * prob2 * (1 - prob2))
z = (observed - expected) / sd
cdf = sum(math.comb(n, k) * prob2**k * (1 - prob2) ** (n - k) for k in range(observed + 1))

# ── B02 · where 0.6652 comes from ───────────────────────────────────────────
check("B02 logit input", [1, 2, 3], [1, 2, 3])
check("B02 peak-subtracted", [-2, -1, 0], [x - max([1, 2, 3]) for x in [1, 2, 3]])
for i, e in enumerate([0.1353, 0.3679, 1.0]):
    check(f"B02 exp[{i}]", e, round(math.exp([-2, -1, 0][i]), 4), tol=5e-5)
check("B02 divisor", 1.5032, round(sum(math.exp(s) for s in (-2, -1, 0)), 4), tol=5e-5)
for i, v in enumerate([0.0900, 0.2447, 0.6652]):
    check(f"B02 probability[{i}]", v, round(p[i], 4), tol=5e-5)

# ── B03 · expected count ────────────────────────────────────────────────────
check("B03 probability (full precision)", "0.6652409557748218", repr(prob2))
check("B03 expected count", 665.24, round(expected, 2), tol=1e-9)

# ── B04 · observed counts, in printed key order ─────────────────────────────
check("B04 printed key order", [1, 2, 0], list(counts.keys()))
for i, c in enumerate([102, 268, 630]):
    check(f"B04 count[{i}]", c, counts[i])
check("B04 counts sum to n", 1000, sum(counts.values()))

# ── B05 · the gap ───────────────────────────────────────────────────────────
check("B05 gap", 35.24, round(gap, 2), tol=1e-9)
check("B05 gap percent", 5.3, round(gap_pct, 1), tol=1e-9)
check("B05 standard deviations", 2.4, round(abs(z), 1), tol=1e-9)

# ── B06 / B07 · the rarity claim ────────────────────────────────────────────
check("B06 sd of the count", 14.92, round(sd, 2), tol=1e-9)
check("B06 z-score", -2.36, round(z, 2), tol=1e-9)
check("B06 P(X<=630) is ~1%", 1.04, round(cdf * 100, 2), tol=1e-9)
# "about 1 run in 50" is the TWO-TAILED reading, chosen because there was no
# directional hypothesis before seeing the data. One-tailed would be ~1 in 97.
check("B06 two-tailed ~ 1 in 50", 48, round(1 / (2 * cdf)), tol=2)

# ── report ──────────────────────────────────────────────────────────────────
failed = [c for c in CHECKS if not c[1]]
for label, ok, detail in CHECKS:
    print(f"{'PASS' if ok else 'FAIL'}  {label:<34} {detail}")
print(f"\n{len(CHECKS) - len(failed)}/{len(CHECKS)} claims reproduced")

if failed:
    print("\nDRIFT: the video's on-screen numbers no longer match main.py.")
    print("main.py is the authority — the reel constants are what need fixing.")
    sys.exit(1)
print("Every number shown in the video is reproducible from unmodified lesson code.")
