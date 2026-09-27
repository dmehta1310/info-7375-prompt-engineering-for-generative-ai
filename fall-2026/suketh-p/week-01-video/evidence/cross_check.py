"""cross_check.py — do the film's numbers survive a change of interpreter?

Submitted by Suketh Produtoor (INFO 7375, Week 1). Written by Claude in
Claude Code build sessions the submitter directed — SOURCES.md §4 records
who did what, and what the submitter personally re-ran.

FACTCHECK.md originally listed this under "Claims deliberately NOT made":

    "Not claimed: that these figures reproduce on any other interpreter.
     Chapter 1 records its saved run on Python 3.14.6; this run is 3.12.7."

That was the honest position while only one interpreter had been tried. It is
also a testable claim, so this tests it instead of conceding it.

The script finds every `python3.N` on PATH, runs `verify_claims.py --json`
under each, and compares the figures the film actually displays. Chapter 1's
own recorded run is Python **3.14.6**, so if that interpreter is present this
doubles as a check against the book's published values.

WHAT AGREEMENT HERE DOES AND DOES NOT ESTABLISH — the same discipline the film
argues for, applied to the film's own evidence:

  IT DOES show the figures are not an artifact of one interpreter version.
  IT DOES NOT show platform independence. Every interpreter here runs on the
    same machine and architecture. IEEE-754 binary64 should give the same
    answers elsewhere, but "should" is not "was measured", and this script
    reports the platform precisely so the claim stays the size of its evidence.

Standard library only. Run:
    python3 cross_check.py
    python3 cross_check.py --json
"""

from __future__ import annotations

import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE / "verify_claims.py"

# The figures the film puts on screen. Keyed by the path into verify_claims'
# JSON, so a drift anywhere in the chain is caught, not just in the headline.
PROBES: list[tuple[str, list[str]]] = [
    ("B03 shifted scores", ["claim_1_intermediates", "shifted"]),
    ("B03 weights", ["claim_1_intermediates", "weights"]),
    ("B03 total weight", ["claim_1_intermediates", "total"]),
    ("B03 distribution", ["claim_2_distribution_unchanged", "shifted_path"]),
    ("B03 matches book table", ["claim_2_distribution_unchanged", "matches_chapter_table_to_10dp"]),
    ("B06 max abs difference", ["claim_2_distribution_unchanged", "max_abs_difference"]),
    ("B02 overflow error text", ["claim_3_prevents_overflow", "raw_exponential_error"]),
    ("B02 shifted [1000,1000]", ["claim_3_prevents_overflow", "shifted_result"]),
    ("B02 exp ceiling", ["claim_3_prevents_overflow", "log_float_max"]),
    ("B07 boundary cases", ["claim_5_boundary_underflow", "cases"]),
    ("ctx seeded counts", ["context_sample", "counts_outcome_order"]),
]


def dig(d: dict, path: list[str]):
    for k in path:
        d = d[k]
    return d


def interpreters() -> list[tuple[str, str]]:
    """Every distinct python3.N on PATH, plus the one running this script."""
    found: dict[str, str] = {}
    for minor in range(9, 20):
        exe = shutil.which(f"python3.{minor}")
        if not exe:
            continue
        try:
            v = subprocess.run([exe, "-c", "import platform;print(platform.python_version())"],
                               capture_output=True, text=True, timeout=30).stdout.strip()
        except Exception:
            continue
        if v:
            found[v] = exe
    found.setdefault(platform.python_version(), sys.executable)
    return sorted(found.items(), key=lambda kv: [int(x) for x in kv[0].split(".")])


def run_under(exe: str) -> dict | None:
    try:
        r = subprocess.run([exe, str(TARGET), "--json"],
                           capture_output=True, text=True, timeout=180)
    except Exception:
        return None
    if r.returncode != 0 or not r.stdout.strip():
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def main() -> int:
    versions = interpreters()
    results: dict[str, dict] = {}
    failed: list[str] = []
    for ver, exe in versions:
        data = run_under(exe)
        if data is None:
            failed.append(ver)
        else:
            results[ver] = data

    if len(results) < 2:
        print("Need at least two working interpreters to cross-check; "
              f"found {len(results)}.")
        return 1

    baseline_ver = sorted(results)[0]
    baseline = results[baseline_ver]
    rows = []
    for label, path in PROBES:
        base_val = dig(baseline, path)
        agree = all(dig(results[v], path) == base_val for v in results)
        rows.append({"figure": label, "identical_across_all": agree,
                     "value": base_val})

    out = {
        "platform": platform.platform(),
        "machine": platform.machine(),
        "interpreters_tested": sorted(results),
        "interpreters_failed": failed,
        "chapter_recorded_interpreter": "3.14.6",
        "chapter_interpreter_included": any(v == "3.14.6" for v in results),
        "all_figures_identical": all(r["identical_across_all"] for r in rows),
        "figures": rows,
        # Generated from the actual count. A hardcoded "three" here was wrong
        # the moment a fourth interpreter turned up on PATH — the same
        # unchecked-number habit this whole project keeps catching.
        "scope_note": (
            f"{len(results)} interpreters, ONE platform and architecture "
            f"({platform.platform()}, {platform.machine()}). This shows the "
            "figures are not an artifact of a single interpreter version. It is "
            "not a measurement of behaviour on other architectures."
        ),
    }

    if "--json" in sys.argv:
        print(json.dumps(out, indent=2))
        return 0 if out["all_figures_identical"] else 1

    print("=" * 74)
    print("  cross_check.py — the same figures, every interpreter on PATH")
    print(f"  platform: {out['platform']} ({out['machine']})")
    print(f"  tested:   {', '.join(out['interpreters_tested'])}")
    if failed:
        print(f"  FAILED to run: {', '.join(failed)}")
    mark = "YES" if out["chapter_interpreter_included"] else "no"
    print(f"  includes Chapter 1's own recorded interpreter (3.14.6): {mark}")
    print("=" * 74)
    print()
    for r in rows:
        status = "identical" if r["identical_across_all"] else "*** DIFFERS ***"
        val = r["value"]
        s = str(val)
        if len(s) > 46:
            s = s[:43] + "..."
        print(f"  {status:<16} {r['figure']:<26} {s}")
    print()
    print("-" * 74)
    if out["all_figures_identical"]:
        print(f"Every displayed figure is identical across "
              f"{len(out['interpreters_tested'])} interpreters.")
    else:
        print("A figure DIFFERS across interpreters — the film must say so.")
    print()
    print("Scope, stated at the size of the evidence:")
    print("  " + out["scope_note"].replace(". ", ".\n  "))
    print()
    return 0 if out["all_figures_identical"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
