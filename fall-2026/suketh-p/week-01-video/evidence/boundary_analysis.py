"""boundary_analysis.py — the cliff, derived rather than discovered.

Submitted by Suketh Produtoor (INFO 7375, Week 1). Written by Claude in
Claude Code build sessions the submitter directed — SOURCES.md §4 records
who did what, and what the submitter personally re-ran.
Companion to verify_claims.py. Standard library only, offline, no API key.

The video (B07) shows that Chapter 1's `probabilities()` returns an exact
`0.0` for `[0, -800]`, and that the first integer to do so is -746. That was
found by sweeping inputs — which proves the boundary exists but not why it
sits there. Finding a number by poking at a function is weaker evidence than
predicting it, so this script does three things the sweep could not:

  1. DERIVES the cliff from the float64 format, in closed form, and then
     confirms the prediction by bisection to 9 decimal places.
  2. MEASURES what the boundary actually costs — not just "a small number
     became zero", but that two DIFFERENT outcomes become indistinguishable.
  3. DEMONSTRATES the standard remedy (stay in log space) and shows exactly
     what it recovers.

IMPORTANT — what this is not. This is not a bug report against
lessons/01-randomness-and-first-prompts/code/main.py. Chapter 1 is explicit
that the reference is "a short teaching implementation, not a universal
numeric-validation library", and the underflow here is a property of binary64,
not a defect in that file. The reference is imported unmodified. This script
asks what the documented boundary implies for someone who reuses the idea.

Run:
    python3 boundary_analysis.py
    python3 boundary_analysis.py --json
"""

from __future__ import annotations

import json
import math
import sys

from verify_claims import REF, probabilities  # same unmodified reference


# ── The remedy: the same distribution, carried in log space ──────────────────
def log_probabilities(logits, temperature: float = 1.0):
    """log of the same softmax, computed without ever forming a tiny float.

    Identical mathematics to `probabilities()` — the same max-subtraction,
    the same normalizer — but the final division is a subtraction of logs, so
    a vanishingly small probability is represented by a perfectly ordinary
    negative number instead of underflowing to zero.

    This is the log-sum-exp form that production libraries use, and it is the
    direct answer to the boundary the video ends on.
    """
    if not logits or not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("Need logits and a positive finite temperature")
    if not all(math.isfinite(x) for x in logits):
        raise ValueError("Logits must be finite")
    peak = max(logits)
    shifted = [(x - peak) / temperature for x in logits]
    # The peak contributes exp(0) = 1, so the total is >= 1 and log is safe.
    lse = math.log(sum(math.exp(s) for s in shifted))
    return [s - lse for s in shifted]


def collect() -> dict:
    out: dict = {}

    # ── 1. Derive the cliff ──────────────────────────────────────────────────
    # binary64's smallest positive subnormal is 2**-1074. Under round-to-
    # nearest, a positive value below HALF of that (2**-1075) has no nearer
    # representable neighbour than zero, so exp(z) returns exactly 0.0 once
    #     z < ln(2**-1075) = -1075 * ln 2
    predicted = -1075 * math.log(2)
    smallest_subnormal = 2.0**-1074

    lo, hi = -746.0, -745.0
    for _ in range(200):  # bisect the real boundary to full double precision
        mid = (lo + hi) / 2
        if math.exp(mid) == 0.0:
            lo = mid
        else:
            hi = mid
    measured = hi

    out["derivation"] = {
        "claim": "the cliff is -1075*ln(2), not an arbitrary number",
        "smallest_subnormal_2_pow_-1074": smallest_subnormal,
        "round_to_zero_threshold_2_pow_-1075": 2.0**-1075,
        "predicted_boundary": predicted,
        "measured_boundary_by_bisection": measured,
        "agree_to_1e_6": abs(measured - predicted) < 1e-6,
        "first_integer_below": math.floor(predicted),
        "why_746": (
            "floor(-745.133219) = -746, which is exactly the integer the "
            "empirical sweep in B07 landed on"
        ),
    }

    # ── 2. What the boundary actually costs ──────────────────────────────────
    # The sharper harm is not that one probability reads 0.0. It is that two
    # DIFFERENT outcomes, 100 nats apart, become the same number.
    collapse = [0, -800, -900]
    lin = probabilities(collapse)
    log = log_probabilities(collapse)
    out["information_loss"] = {
        "claim": "past the cliff, distinct outcomes become indistinguishable",
        "logits": collapse,
        "linear": lin,
        "log_space": log,
        "linear_ties_outcomes_1_and_2": lin[1] == lin[2],
        "log_space_separation_nats": log[1] - log[2],
        "note": (
            "outcomes 1 and 2 differ by 100 nats — a factor of e^100 — and the "
            "linear result reports both as 0.0"
        ),
    }

    # ── 3. The remedy, measured ──────────────────────────────────────────────
    cases = []
    for z in ([1, 2, 3], [0, -800], [0, -5000]):
        lin = probabilities(z)
        log = log_probabilities(z)
        cases.append(
            {
                "logits": z,
                "linear": lin,
                "log_space": log,
                "linear_lost_outcomes": [i for i, v in enumerate(lin) if v == 0.0],
                "log_space_lost_outcomes": [
                    i for i, v in enumerate(log) if v == -math.inf
                ],
            }
        )
    out["remedy"] = {
        "claim": "log space carries what linear space cannot represent",
        "cases": cases,
    }

    # ── 4. The remedy agrees with the reference where BOTH are valid ────────
    # A fix that changed the answer would not be a fix. On moderate inputs the
    # two must round-trip to the same distribution.
    z = [1, 2, 3]
    round_trip = [math.exp(v) for v in log_probabilities(z)]
    ref = probabilities(z)
    out["agreement"] = {
        "claim": "on moderate inputs the log-space form reproduces the reference",
        "logits": z,
        "reference": ref,
        "exp_of_log_space": round_trip,
        "max_abs_difference": max(abs(a - b) for a, b in zip(ref, round_trip)),
        "agree_to_1e_12": all(
            math.isclose(a, b, rel_tol=0.0, abs_tol=1e-12)
            for a, b in zip(ref, round_trip)
        ),
    }

    out["reference_implementation"] = str(REF)
    return out


def main() -> int:
    d = collect()
    if "--json" in sys.argv:
        print(json.dumps(d, indent=2))
        return 0

    print("=" * 74)
    print("  The cliff, derived — boundary_analysis.py")
    print(f"  Reference (unmodified): {d['reference_implementation']}")
    print("=" * 74)

    x = d["derivation"]
    print(f"\n[1] {x['claim']}")
    print(f"    smallest subnormal  2^-1074        = {x['smallest_subnormal_2_pow_-1074']!r}")
    print(f"    round-to-zero below 2^-1075        = {x['round_to_zero_threshold_2_pow_-1075']!r}")
    print(f"    so exp(z) == 0.0 once z < -1075*ln2 = {x['predicted_boundary']:.9f}  (predicted)")
    print(f"    bisection of the real boundary      = {x['measured_boundary_by_bisection']:.9f}  (measured)")
    print(f"    prediction matches measurement      : {x['agree_to_1e_6']}")
    print(f"    -> first integer past it            = {x['first_integer_below']}   {x['why_746']}")

    y = d["information_loss"]
    print(f"\n[2] {y['claim']}")
    print(f"    logits    {y['logits']}")
    print(f"    linear    {y['linear']}")
    print(f"    log space {[round(v, 1) for v in y['log_space']]}")
    print(f"    linear reports outcomes 1 and 2 as equal : {y['linear_ties_outcomes_1_and_2']}")
    print(f"    they are actually {abs(y['log_space_separation_nats']):.0f} nats apart")

    z = d["remedy"]
    print(f"\n[3] {z['claim']}")
    for c in z["cases"]:
        print(f"    {str(c['logits']):<14} linear lost {str(c['linear_lost_outcomes']):<8}"
              f" log-space lost {c['log_space_lost_outcomes']}")

    a = d["agreement"]
    print(f"\n[4] {a['claim']}")
    print(f"    reference        {a['reference']}")
    print(f"    exp(log-space)   {a['exp_of_log_space']}")
    print(f"    max abs diff     {a['max_abs_difference']}")
    print(f"    agree to 1e-12   : {a['agree_to_1e_12']}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
