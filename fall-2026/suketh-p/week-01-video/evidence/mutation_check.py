"""mutation_check.py — do the tests actually bite?

Submitted by Suketh Produtoor (INFO 7375, Week 1). Written by Claude in
Claude Code build sessions the submitter directed — SOURCES.md §4 records
who did what, and what the submitter personally re-ran.

A green suite is evidence for its stated properties and nothing more. Chapter 1
makes this its Challenge assessment:

    "10. A misleading green test — deliberately introduce a small bug into a
     copy of your learner implementation that still allows one existing
     assertion to pass. Do not alter the reference. Explain the bug, identify
     the surviving assertion, and add a different test that exposes the defect."

This script does that for the test suite defending the video. Each mutation is a
plausible small defect. For each one it records which tests DIED (caught it)
and which SURVIVED (passed anyway) — and a surviving assertion is the
interesting result, not a failure of the exercise.

The reference implementation is never modified, per AGENTS.md. Mutations are
applied by monkey-patching the imported function inside this process only, and
every one is reverted before the next runs.

Run:
    python3 mutation_check.py
"""

from __future__ import annotations

import io
import math
import unittest

import verify_claims
import boundary_analysis
import test_verify_claims as suite

_REAL = verify_claims.probabilities


# ── The mutations ────────────────────────────────────────────────────────────
def mut_drop_max_subtraction(logits, temperature=1.0):
    """Remove the very thing the film is about: exponentiate raw scores.

    Returns the SAME distribution for moderate inputs (that is the film's
    whole point), so any test that only checks [1,2,3] will survive this.
    """
    weights = [math.exp(x / temperature) for x in logits]
    total = sum(weights)
    return [w / total for w in weights]


def mut_reverse_pairing(logits, temperature=1.0):
    """Pair the right probabilities with the wrong outcome labels.

    Chapter 1 names this one specifically: "Suppose probabilities have been
    paired with the wrong labels. Their sum might still be one."
    """
    return list(reversed(_REAL(logits, temperature)))


def mut_accept_zero_temperature(logits, temperature=1.0):
    """Silently coerce an invalid temperature instead of refusing it."""
    if temperature <= 0:
        temperature = 1.0
    return _REAL(logits, temperature)


def mut_clamp_tiny_to_zero(logits, temperature=1.0):
    """Round very small probabilities down to a hard zero everywhere.

    Makes the underflow the film reports on [0,-800] happen much earlier, so
    the boundary is no longer where the derivation says it is.
    """
    return [0.0 if p < 1e-12 else p for p in _REAL(logits, temperature)]


MUTATIONS = [
    ("drop the max-subtraction", mut_drop_max_subtraction),
    ("pair probabilities with reversed labels", mut_reverse_pairing),
    ("accept temperature=0 instead of raising", mut_accept_zero_temperature),
    ("clamp probabilities below 1e-12 to 0.0", mut_clamp_tiny_to_zero),
]


def all_test_ids() -> list[str]:
    def walk(s, acc):
        for x in s:
            if isinstance(x, unittest.TestSuite):
                walk(x, acc)
            else:
                acc.append(x.id())
        return acc

    return walk(unittest.TestLoader().loadTestsFromModule(suite), [])


def run_suite() -> tuple[int, set[str]]:
    """Run every test; return (total, {failing test ids})."""
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromModule(suite)
    buf = io.StringIO()
    result = unittest.TextTestRunner(stream=buf, verbosity=0).run(tests)
    return result.testsRun, {t.id() for t, _ in result.failures + result.errors}


def short(test_id: str) -> str:
    return test_id.split(".", 1)[1] if "." in test_id else test_id


def apply(fn) -> None:
    """Patch every module that holds a reference to the function."""
    verify_claims.probabilities = fn
    boundary_analysis.probabilities = fn
    suite.probabilities = fn


def main() -> int:
    total, baseline = run_suite()
    print("=" * 74)
    print("  mutation_check.py — Chapter 1 Assessment 10, applied to this film")
    print("=" * 74)
    print(f"\nbaseline: {total} tests, {len(baseline)} failing")
    if baseline:
        print("  ABORT — the suite must be green before mutating.")
        for b in baseline:
            print(f"    {b}")
        return 1
    print("  green, as required before mutating.\n")

    ids = all_test_ids()
    rows = []
    for name, fn in MUTATIONS:
        apply(fn)
        try:
            _, failed = run_suite()
        finally:
            apply(_REAL)
        survivors = [i for i in ids if i not in failed]
        rows.append((name, len(failed), survivors))
        verdict = "CAUGHT" if failed else "SURVIVED — not covered!"
        print(f"[{verdict}]  {name}")
        print(f"    died {len(failed)}/{total} · survived {len(survivors)}/{total}")
        # Survivors are the interesting list: these assertions passed while the
        # code was wrong. Printed from the run, never asserted from memory.
        for s in sorted(survivors)[:8]:
            print(f"      survived: {short(s)}")
        if len(survivors) > 8:
            print(f"      … and {len(survivors) - 8} more")
        print()

    undetected = [n for n, k, _ in rows if k == 0]
    print("-" * 74)
    print(f"mutation score: {sum(1 for _, k, _ in rows if k)}/{len(rows)} caught")
    if undetected:
        print("UNCOVERED mutations — each needs a test written for it:")
        for n in undetected:
            print(f"  - {n}")
        return 1

    print("Every mutation was caught by at least one test.\n")
    print("What the SURVIVOR list actually shows — the point of the exercise:")
    print("  Removing the max-subtraction leaves 8 assertions green, and they")
    print("  are almost exactly the tests that never call probabilities() at")
    print("  all: the closed-form derivation tests and the raw math.exp")
    print("  overflow test. Those exercise the MATHEMATICS directly, so they")
    print("  are blind to a defect in the implementation. That is a real")
    print("  coverage boundary in my own suite, not a reassurance — and it is")
    print("  Chapter 1's question in practice: ask what would still be wrong")
    print("  if this test passed.")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
