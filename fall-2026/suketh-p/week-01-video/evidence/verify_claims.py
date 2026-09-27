"""verify_claims.py — every number shown in "Shifted, Not Changed".

Submitted by Suketh Produtoor (INFO 7375, Week 1). Written by Claude in
Claude Code build sessions the submitter directed — SOURCES.md §4 records
who did what, and what the submitter personally re-ran.
Concept: Chapter 1, "The subtraction that changes nothing important".

This script exists so that no figure in the video is taken on trust. Each
CLAIM below is printed beside the value the course's own reference
implementation actually returns. Nothing here is typed in by hand; every
number the film displays is read out of this run.

It imports the course reference implementation directly and does not modify
it (AGENTS.md: "Do not modify reference solutions"). Standard library only,
offline, no API key, no network.

Run:
    python3 verify_claims.py            # human-readable
    python3 verify_claims.py --json     # machine-readable, for the beat sheet
"""

from __future__ import annotations

import importlib.util
import json
import math
import os
import platform
import sys
from pathlib import Path

# ── Locate and import the course reference implementation ────────────────────
# Searched by walking UP from this file rather than by a fixed parent depth,
# because this folder is posted to GitHub at a different depth than it sits at
# inside the course checkout (fall-2025/<name>/week-01-video/ vs
# course/youtube/<slug>/). A hard-coded parents[3] works in one and silently
# fails in the other. Override with INFO7375_REF if the checkout is elsewhere.
REL = Path("lessons") / "01-randomness-and-first-prompts" / "code" / "main.py"


def find_reference() -> Path:
    override = os.environ.get("INFO7375_REF")
    if override:
        p = Path(override).expanduser().resolve()
        if p.exists():
            return p
        raise SystemExit(f"INFO7375_REF is set but does not exist: {p}")

    here = Path(__file__).resolve()
    # Walk up; at each level also try a sibling `course/` checkout, which is
    # where the repo lands when cloned beside the submission folder.
    for base in here.parents:
        for cand in (base / REL, base / "course" / REL):
            if cand.exists():
                return cand
    raise SystemExit(
        "Could not find the course reference implementation.\n"
        f"Looked for {REL} in every parent of {here.parent}.\n"
        "Clone the course repo nearby, or set INFO7375_REF to the path of\n"
        "lessons/01-randomness-and-first-prompts/code/main.py"
    )


REF = find_reference()

_spec = importlib.util.spec_from_file_location("ch01_main", REF)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

probabilities = _mod.probabilities
sample = _mod.sample


def _ordered(counts: dict, n: int) -> list:
    """Counter order is insertion order. Report outcome order, missing => 0.

    Chapter 1: "When preparing a table, retrieve missing counts as zero rather
    than assuming every index is present."
    """
    return [counts.get(i, 0) for i in range(n)]


def collect() -> dict:
    out: dict = {}

    # ── Environment ──────────────────────────────────────────────────────────
    out["environment"] = {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "reference_implementation": str(REF),
        "note": (
            "Chapter 1 records its saved run on Python 3.14.6. This run is a "
            "different interpreter version; the seeded counts below are what "
            "THIS environment produced."
        ),
    }

    # ── CLAIM 1 — the intermediates the subtraction actually changes ─────────
    # Chapter 1: "For [1, 2, 3], the shifted scores are [-2, -1, 0]."
    logits = [1, 2, 3]
    peak = max(logits)
    shifted = [x - peak for x in logits]
    weights = [math.exp(x) for x in shifted]
    total = sum(weights)
    out["claim_1_intermediates"] = {
        "claim": "max-subtraction rewrites every intermediate value",
        "logits": logits,
        "peak": peak,
        "shifted": shifted,
        "weights": weights,
        "total": total,
        "largest_weight_is_exactly_one": weights[shifted.index(0)] == 1.0,
    }

    # ── CLAIM 2 — the distribution is unchanged by the shift ─────────────────
    # Shifted (the reference implementation) vs direct exponentiation.
    shifted_probs = probabilities(logits)
    direct_w = [math.exp(x) for x in logits]
    direct_t = sum(direct_w)
    direct_probs = [w / direct_t for w in direct_w]
    out["claim_2_distribution_unchanged"] = {
        "claim": "the normalized distribution is the same either way",
        "shifted_path": shifted_probs,
        "direct_path": direct_probs,
        "max_abs_difference": max(
            abs(a - b) for a, b in zip(shifted_probs, direct_probs)
        ),
        "allclose_1e_12": all(
            math.isclose(a, b, rel_tol=0.0, abs_tol=1e-12)
            for a, b in zip(shifted_probs, direct_probs)
        ),
        "sums_to_one_within_1e_12": math.isclose(
            sum(shifted_probs), 1.0, rel_tol=0.0, abs_tol=1e-12
        ),
        "chapter_table_T1": [0.0900305732, 0.2447284711, 0.6652409558],
        "matches_chapter_table_to_10dp": [
            round(p, 10) for p in shifted_probs
        ] == [0.0900305732, 0.2447284711, 0.6652409558],
    }

    # ── CLAIM 3 — what the subtraction PREVENTS (the large end) ─────────────
    # The failure is real, not narrated: exponentiating the raw score raises.
    big = [1000, 1000]
    raw_error = None
    raw_weights = None
    try:
        raw_weights = [math.exp(x) for x in big]
    except OverflowError as exc:
        raw_error = f"{type(exc).__name__}: {exc}"
    out["claim_3_prevents_overflow"] = {
        "claim": "without the shift, the raw exponential overflows",
        "logits": big,
        "raw_exponential": raw_weights,
        "raw_exponential_error": raw_error,
        "shifted_result": probabilities(big),
        "shifted_result_is_half_half": probabilities(big) == [0.5, 0.5],
        "float_max": sys.float_info.max,
        "log_float_max": math.log(sys.float_info.max),
    }

    # ── CLAIM 4 — the guarantee it DOES give (denominator floor) ────────────
    # After the shift the largest exponent is 0, so its weight is exactly 1,
    # so the denominator is >= 1 and can never underflow to zero.
    floor_cases = [[1, 2, 3], [1000, 1000], [0, -800], [-5, -5, -5], [0.0, -1e9]]
    out["claim_4_denominator_floor"] = {
        "claim": "after the shift the denominator is always >= 1",
        "cases": [
            {
                "logits": c,
                "total": sum(math.exp(x - max(c)) for x in c),
                "at_least_one": sum(math.exp(x - max(c)) for x in c) >= 1.0,
            }
            for c in floor_cases
        ],
    }

    # ── CLAIM 5 — the BOUNDARY: the small end is not fixed ──────────────────
    # This is the film's "what this does not establish" beat. The shift
    # protects the largest term. It does nothing for the smallest, which can
    # still underflow to a hard zero.
    boundary = []
    for c in [[0, -700], [0, -745], [0, -746], [0, -800]]:
        p = probabilities(c)
        boundary.append(
            {
                "logits": c,
                "probabilities": p,
                "smallest": p[1],
                "is_exactly_zero": p[1] == 0.0,
                "true_value_log10": c[1] / math.log(10),
            }
        )
    out["claim_5_boundary_underflow"] = {
        "claim": (
            "the shift fixes the large end only; a small term can still "
            "underflow to exactly 0.0"
        ),
        "smallest_normal": sys.float_info.min,
        "cases": boundary,
        "chapter_warning": (
            "Chapter 1: 'Keep the tested claim narrower than the slogan "
            '"numerically stable."\''
        ),
    }

    # ── CONTEXT — the sampling run, for the report's honesty line ───────────
    counts = sample(logits)
    out["context_sample"] = {
        "claim": "a distribution is not the sample you happened to see",
        "seed": 7,
        "count": 1000,
        "counts_outcome_order": _ordered(counts, len(logits)),
        "expected_count_outcome_2": shifted_probs[2] * 1000,
        "observed_count_outcome_2": counts.get(2, 0),
    }

    return out


def main() -> int:
    data = collect()

    if "--json" in sys.argv:
        print(json.dumps(data, indent=2))
        return 0

    env = data["environment"]
    print("=" * 72)
    print('  "Shifted, Not Changed" — claim verification')
    print(f"  Python {env['python']} ({env['implementation']}) · {env['platform']}")
    print(f"  Reference: {env['reference_implementation']}")
    print("=" * 72)

    c1 = data["claim_1_intermediates"]
    print(f"\n[1] {c1['claim']}")
    print(f"    logits   {c1['logits']}   peak {c1['peak']}")
    print(f"    shifted  {c1['shifted']}")
    print(f"    weights  {c1['weights']}")
    print(f"    total    {c1['total']}")
    print(f"    largest weight is exactly 1.0 : {c1['largest_weight_is_exactly_one']}")

    c2 = data["claim_2_distribution_unchanged"]
    print(f"\n[2] {c2['claim']}")
    print(f"    shifted path  {c2['shifted_path']}")
    print(f"    direct  path  {c2['direct_path']}")
    print(f"    max abs diff  {c2['max_abs_difference']}")
    print(f"    agrees to 1e-12          : {c2['allclose_1e_12']}")
    print(f"    sums to 1 within 1e-12   : {c2['sums_to_one_within_1e_12']}")
    print(f"    matches chapter's table  : {c2['matches_chapter_table_to_10dp']}")

    c3 = data["claim_3_prevents_overflow"]
    print(f"\n[3] {c3['claim']}")
    print(f"    exp(1000) raw   -> {c3['raw_exponential_error']}")
    print(f"    shifted [1000,1000] -> {c3['shifted_result']}")
    print(f"    largest representable float: {c3['float_max']:.6e}")
    print(f"    exp overflows above score gap ~{c3['log_float_max']:.4f}")

    c4 = data["claim_4_denominator_floor"]
    print(f"\n[4] {c4['claim']}")
    for case in c4["cases"]:
        print(
            f"    {str(case['logits']):<16} total {case['total']:<22}"
            f" >= 1 : {case['at_least_one']}"
        )

    c5 = data["claim_5_boundary_underflow"]
    print(f"\n[5] BOUNDARY — {c5['claim']}")
    print(f"    smallest normal float: {c5['smallest_normal']:.6e}")
    for case in c5["cases"]:
        flag = "  <-- HARD ZERO" if case["is_exactly_zero"] else ""
        print(
            f"    {str(case['logits']):<12} -> {str(case['probabilities']):<34}"
            f" true p1 ~ 1e{case['true_value_log10']:.0f}{flag}"
        )
    print(f"    {c5['chapter_warning']}")

    cs = data["context_sample"]
    print(f"\n[ctx] {cs['claim']}")
    print(f"    counts (outcome order) {cs['counts_outcome_order']}")
    print(
        f"    outcome 2: expected {cs['expected_count_outcome_2']:.2f}"
        f" vs observed {cs['observed_count_outcome_2']}"
    )
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
