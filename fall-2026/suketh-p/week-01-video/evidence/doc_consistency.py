"""doc_consistency.py — do the documents still agree with the artifact?

Submitted by Suketh Produtoor (INFO 7375, Week 1). Written by Claude in
Claude Code build sessions the submitter directed — SOURCES.md §4 records
who did what, and what the submitter personally re-ran.

This submission has eleven documents and went through nine rounds of edits.
Five separate times a number in the paperwork drifted from the thing it
described, and every single time I found it by accident rather than by
checking (`SOURCES.md` §5.5, §5.7, §5.8, §5.12, and the "Three interpreters"
slip in `cross_check.py`). That is a process failure, not five coincidences,
so this is the check that should have existed from the start.

It derives the facts LIVE — from `beat_sheet.json`, the `.srt`, `TYPECHECK.md`
and the test file — and then asserts the current-state documents agree.

WHAT IT DELIBERATELY DOES NOT CHECK
  `SOURCES.md` §5 is a **corrections ledger** — it quotes the figures it is
  recording as wrong, so that section is skipped for the same reason.

  `REVIEW.md` and `FRICTIONAL.md` are **dated logs**. They quote the numbers
  that were true on the day of each entry — 195.46 s, 111 cues, 0/3/27 — and
  those are supposed to stay standing. A log that silently rewrites its own
  history is worse than a stale number. Both files instead carry a
  current-state header, and this script verifies that header exists and is
  correct rather than policing the entries beneath it.

Standard library only. Run:
    python3 doc_consistency.py          # human-readable
    python3 doc_consistency.py --check  # exit 1 on any mismatch (for CI)
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

REEL = pathlib.Path(__file__).resolve().parent.parent

# Documents that state the CURRENT artifact. Must agree with live truth.
CURRENT_STATE = ["README.md", "CHECKS-REPORT.md", "SHOTLIST.md",
                 "BUILD-PROMPT.md", "FACTCHECK.md", "SOURCES.md", "PROMPTS.md"]
# Dated logs. Exempt by design — see the module docstring.
DATED_LOGS = ["REVIEW.md", "FRICTIONAL.md", "REFINEMENTS.md"]

# A corrections ledger quotes the value it is correcting. Scanning it would
# flag the very figures it exists to record as wrong — the same reasoning that
# exempts the dated logs, applied to a section rather than a file.
CORRECTION_HEADINGS = ("## 5. Corrections applied",)


def strip_corrections(text: str) -> str:
    """Drop any corrections section so quoted former values are not flagged."""
    for h in CORRECTION_HEADINGS:
        i = text.find(h)
        if i == -1:
            continue
        j = text.find("\n## ", i + len(h))
        text = text[:i] + (text[j:] if j != -1 else "")
    return text


def truth() -> dict[str, object]:
    sheet = json.loads((REEL / "beat_sheet.json").read_text())
    beats = sheet["beats"]
    total = sum(b.get("actual_duration_s") or 0 for b in beats)

    srt = next((REEL / d).glob("*.srt") for d in ("captions", "final")
               if (REEL / d).exists())
    cues = sum(p.read_text().count(" --> ") for p in srt)

    tc = (REEL / "TYPECHECK.md").read_text()
    m = re.search(r"\*\*(\d+) FAIL · (\d+) WARN · (\d+) PASS\*\*", tc)

    tests = len(re.findall(r"\n    def test_",
                           (REEL / "evidence/test_verify_claims.py").read_text()))

    body = [b for b in beats if b["beat_id"] not in
            {"B00", "B01", "B08", "B09", "B10"}]
    return {
        "total_s": round(total, 2),
        "mmss": f"{int(total // 60)}:{int(round(total % 60)):02d}",
        "beats": len(beats),
        "cues": cues,
        "gate_t": f"{m.group(1)} FAIL · {m.group(2)} WARN · {m.group(3)} PASS",
        "tests": tests,
        "body_words": [len(b["narration_text"].split()) for b in body],
    }


def main() -> int:
    t = truth()
    problems: list[str] = []
    notes: list[str] = []

    def scan(pattern: str, label: str, ok_values: set[str]) -> None:
        for name in CURRENT_STATE:
            p = REEL / name
            if not p.exists():
                continue
            for m in re.finditer(pattern, strip_corrections(p.read_text())):
                got = m.group(0)
                if got not in ok_values:
                    problems.append(
                        f"{name}: {label} says {got!r}, live value is "
                        f"{' or '.join(sorted(ok_values))}")

    scan(r"195\.\d+", "runtime seconds", {str(t["total_s"])})
    scan(r"\b3:\d\d\b", "runtime m:ss", {str(t["mmss"])})
    scan(r"\d+ cues", "caption cues", {f"{t['cues']} cues"})
    scan(r"\d+ FAIL · \d+ WARN · \d+ PASS", "GATE T tally", {str(t["gate_t"])})
    # "13 tests" is the repo's own validator, not this suite — allow it.
    scan(r"\b\d+ tests\b", "test count", {f"{t['tests']} tests", "13 tests"})
    # Body-beat word counts, written as a bold "a / b / c / d / e / f" list.
    # B05's count changed on 2026-09-24 (34 -> 31) and nothing would have
    # noticed the stale list; now it is derived like everything else.
    scan(r"(?<=\*\*)\d+(?: / \d+){5}(?=\*\*)", "body word counts",
         {" / ".join(str(n) for n in t["body_words"])})

    # The dated logs must each carry a correct current-state header.
    for name in DATED_LOGS:
        p = REEL / name
        if not p.exists():
            continue
        head = "\n".join(p.read_text().splitlines()[:14])
        if "Current state" not in head:
            problems.append(f"{name}: dated log has no current-state header")
        else:
            for token in (str(t["total_s"]), str(t["gate_t"])):
                if token not in head:
                    problems.append(
                        f"{name}: current-state header omits {token!r}")
            notes.append(f"{name}: dated log, entries exempt; header checked")

    print("=" * 74)
    print("  doc_consistency.py — do the documents match the artifact?")
    print("=" * 74)
    print("\nLIVE TRUTH (derived, not typed)")
    for k, v in t.items():
        print(f"  {k:12} {v}")
    print(f"\nCHECKED  {', '.join(CURRENT_STATE)}")
    print(f"EXEMPT   {', '.join(DATED_LOGS)} — dated logs; header verified instead")
    for n in notes:
        print(f"           {n}")
    print()
    print("-" * 74)
    if problems:
        print(f"{len(problems)} MISMATCH(ES):\n")
        for pr in problems:
            print(f"  {pr}")
        print()
        return 1 if "--check" in sys.argv else 0
    print("Every current-state document agrees with the artifact.")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
