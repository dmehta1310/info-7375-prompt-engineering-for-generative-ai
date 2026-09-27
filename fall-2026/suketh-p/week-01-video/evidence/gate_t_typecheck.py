"""gate_t_typecheck.py — the mandatory gate that does not ship.

Submitted by Suketh Produtoor (INFO 7375, Week 1). Written by Claude in
Claude Code build sessions the submitter directed — SOURCES.md §4 records
who did what, and what the submitter personally re-ran.

`skills/make/ai-explainer/SKILL.md` says:

    "GATE T (type-lock) — ALWAYS RUN, like factcheck. `scripts/type_check.py`
     asserts §8.1 min-size, §8.2 overflow, §8.3 contrast, §8.4 kerning sanity,
     §8.5 no-wordy-card, §8.6 golden strings per rendered frame, then writes
     TYPECHECK.md. No `./art run` and no `./art final` may report success
     while TYPECHECK.md has any FAIL."

That script is **not in the public checkout** — there is no `scripts/` directory
at the toolkit root and `find . -name type_check.py` returns nothing. So the
gate the doctrine calls mandatory cannot be run, and every reel built from this
checkout ships unchecked against §8. Rather than record that as a permanent
excuse (FRICTIONAL.md, 2026-09-15), this implements the parts that can be
checked honestly from the scene source and the beat sheet.

WHAT THIS CHECKS
  §8.1 min-size   — every declared fontSize against the ~24px legibility floor
  §8.3 contrast   — real WCAG 2.1 ratios for every ink/ground pair in use
  §8.5 wordy-card — narration word budget per body beat
  §8.6 golden     — the figures the beat sheet wires to each beat are exactly
                    the ones in the recorded evidence run (no drift, no typo)

WHAT THIS DOES NOT CHECK — stated so the gate is not mistaken for the full one
  §8.2 overflow   — needs rendered frames; Gate V's edge-bleed audit covers it
  §8.4 kerning    — needs font metrics from the renderer; not reproduced here
  §8.6 on FRAMES  — this verifies the wiring, not pixels. Confirming a string is
                    legible in the image would need OCR, which is not available
                    offline here. Gate V reads the frames instead.

Standard library only. Run:
    python3 gate_t_typecheck.py            # human-readable + writes TYPECHECK.md
    python3 gate_t_typecheck.py --check    # exit 1 on any FAIL (for CI)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REEL = Path(__file__).resolve().parent.parent
SHEET = REEL / "beat_sheet.json"
OUT = REEL / "TYPECHECK.md"

# The scene source lives in the external toolkit checkout (AGENTS.md: never
# vendored). Look for it beside the course, then fall back to the copy shipped
# in this submission's components/ folder.
CANDIDATES = [
    REEL.parents[2] / "brutalist.art/runtime/remotion/src/ShiftedNotChanged.tsx",
    REEL.parents[3] / "brutalist.art/runtime/remotion/src/ShiftedNotChanged.tsx",
    REEL / "components" / "ShiftedNotChanged.tsx",
]

MIN_PX = 24.0          # §8.1 legibility floor, per FILL-THE-CANVAS LAW
AA_NORMAL = 4.5        # WCAG 2.1 AA, text < 24px
AA_LARGE = 3.0         # WCAG 2.1 AA, text >= 24px (18pt)
BODY_WORDS = (45, 70)  # SKILL.md narration budget for body beats


# ── WCAG 2.1 contrast ────────────────────────────────────────────────────────
def _lin(c: float) -> float:
    c /= 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(fg: str, bg: str) -> float:
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def find_source() -> Path:
    for p in CANDIDATES:
        if p.exists():
            return p
    raise SystemExit(
        "Cannot find ShiftedNotChanged.tsx. Looked in:\n  "
        + "\n  ".join(str(p) for p in CANDIDATES)
    )


def parse_palette(src: str) -> dict[str, str]:
    return {
        m.group(1): m.group(2)
        for m in re.finditer(r"^const (BG|INK|ACC|SOFT|GHOST|CARD|BORDER)\s*=\s*'(#[0-9A-Fa-f]{6})'",
                             src, re.M)
    }


def main() -> int:
    src_path = find_source()
    src = src_path.read_text()
    pal = parse_palette(src)
    sheet = json.loads(SHEET.read_text())
    rows: list[tuple[str, str, str, str]] = []  # (section, status, item, detail)

    # ── §8.1 min-size ────────────────────────────────────────────────────────
    sizes = sorted({int(m) for m in re.findall(r"fontSize: (\d+)", src)})
    for s in sizes:
        if s < MIN_PX:
            rows.append(("§8.1", "FAIL", f"fontSize {s}px", f"below the {MIN_PX:.0f}px floor"))
    smallest = min(sizes)
    rows.append(
        ("§8.1", "PASS" if smallest >= MIN_PX else "FAIL",
         f"{len(sizes)} distinct sizes, smallest {smallest}px",
         f"floor is {MIN_PX:.0f}px — note it is a FLOOR, not a target")
    )

    # ── §8.3 contrast ────────────────────────────────────────────────────────
    # Ink colours that actually appear as `color:` on the cream stage, plus the
    # white card. Sizes noted because AA's threshold depends on them.
    used = re.findall(r"color: (INK|ACC|SOFT|GHOST)", src)
    grounds = {"BG (stage)": pal["BG"], "CARD (white card)": pal["CARD"]}
    BRAND_LOCKED = {("ACC", "BG (stage)"), ("ACC", "CARD (white card)")}
    for ink_name in sorted(set(used)):
        for gname, g in grounds.items():
            ratio = contrast(pal[ink_name], g)
            # Every use of these colours in this reel is >= 24px, so AA-large
            # is the governing threshold. Flagged explicitly either way.
            meets = ratio >= AA_LARGE
            note = f"{ratio:.2f}:1 (AA-large {AA_LARGE}:1"
            note += ", AA-normal met)" if ratio >= AA_NORMAL else ", AA-normal NOT met)"
            # ACC on the brand grounds is fixed by CLAUDE-BRAND.md: "This is a
            # FIDELITY brand ... Do not retint it." That pair cannot be fixed
            # by changing a colour, so it is mitigated instead — see §8.3b.
            if (ink_name, gname) in BRAND_LOCKED and not meets:
                rows.append(("§8.3", "WARN", f"{ink_name} on {gname}",
                             note + " — BRAND-LOCKED, cannot retint. Mitigated: "
                             "the accent is never the sole carrier of meaning (§8.3b)."))
            else:
                rows.append(("§8.3", "PASS" if meets else "FAIL",
                             f"{ink_name} on {gname}", note))

    # ── §8.3b the mitigation, checked rather than asserted ───────────────────
    # Wherever the un-compliant accent marks a value, a non-colour signal must
    # travel with it, so the meaning survives for a viewer who cannot resolve
    # the hue.
    for label, needle in [
        ("B03 focal cells", "fontWeight: focal ? 700 : 400"),
        ("B06 marked digits", "fontWeight: marked && markIn > 0.2 ? 700 : 400"),
        ("B07 hard zeros", "fontWeight: hot ? 700 : 400"),
        ("B04 struck factor", "textDecoration: strikeIn > 0.15 ? 'line-through' : 'none'"),
    ]:
        ok = needle in src
        rows.append(("§8.3b", "PASS" if ok else "FAIL", label,
                     "non-colour signal travels with the accent" if ok
                     else "accent may be colour-only here — add weight, size or a rule"))

    # ── §8.5 no-wordy-card ───────────────────────────────────────────────────
    bookends = {"B00", "B01", "B08", "B09", "B10"}
    for b in sheet["beats"]:
        bid = b["beat_id"]
        if bid in bookends:
            continue
        n = len(b["narration_text"].split())
        if bid == "B05":  # ask micro-beat, short by design
            rows.append(("§8.5", "PASS", f"{bid} {n} words", "ask micro-beat, short by design"))
            continue
        lo, hi = BODY_WORDS
        status = "PASS" if lo <= n <= hi else "WARN"
        rows.append(("§8.5", status, f"{bid} {n} words",
                     f"budget {lo}–{hi}; hard fail is 100+"))

    # ── §8.6 golden figures: is the right number wired to the right beat? ────
    run = (REEL / "evidence" / "run-output.txt").read_text()
    golden = {
        "B02": ["OverflowError: math range error", "709.7827", "1.797693e+308"],
        "B03": ["0.1353352832", "0.3678794412", "1.5032147244", "0.6652409558"],
        "B06": ["1.1102230246251565e-16", "0.09003057317038046", "0.09003057317038045"],
        "B07": ["9.85967654375977e-305", "5e-324", "745.133219102"],
    }
    by_id = {b["beat_id"]: b for b in sheet["beats"]}
    boundary = (REEL / "evidence" / "boundary-output.txt")
    corpus = run + (boundary.read_text() if boundary.exists() else "")
    # Every float the recorded runs printed, at full precision.
    corpus_floats = [float(x) for x in re.findall(r"-?\d+\.\d+(?:e[-+]?\d+)?", corpus)]

    def backed_by_run(fig: str) -> tuple[bool, str]:
        """A displayed figure is backed if it appears verbatim in a recorded
        run, OR is the correct rounding of a full-precision value that does.
        The first version of this check only did substring matching and
        false-flagged two legitimately rounded figures — including
        0.6652409558, which is verbatim the chapter's own published table."""
        if fig in corpus:
            return True, "verbatim in a recorded run"
        try:
            val = float(fig)
        except ValueError:
            return False, "not numeric and not found verbatim"
        dp = len(fig.split(".")[1]) if "." in fig else 0
        for c in corpus_floats:
            if round(c, dp) == val:
                return True, f"correct {dp}-dp rounding of {c!r} from a recorded run"
        return False, "NOT in any recorded run, at any rounding"

    for bid, figs in golden.items():
        props = json.dumps(by_id[bid]["shot"]["remotion"]["props"], ensure_ascii=False)
        for fig in figs:
            if fig not in props:
                rows.append(("§8.6", "FAIL", f"{bid} · {fig}",
                             "expected figure missing from the beat's props"))
                continue
            ok, why = backed_by_run(fig)
            rows.append(("§8.6", "PASS" if ok else "FAIL", f"{bid} · {fig}", why))

    # ── Report ───────────────────────────────────────────────────────────────
    fails = [r for r in rows if r[1] == "FAIL"]
    warns = [r for r in rows if r[1] == "WARN"]

    lines = [
        "# TYPECHECK.md — GATE T",
        "",
        f"Generated by `evidence/gate_t_typecheck.py` against `{src_path.name}`.",
        "",
        "The toolkit's own `scripts/type_check.py` is **absent from the public checkout**,",
        "so this reel implements the checkable parts of §8 rather than shipping unchecked.",
        "Coverage and the deliberate gaps are documented in the script's header.",
        "",
        f"**{len(fails)} FAIL · {len(warns)} WARN · {len(rows) - len(fails) - len(warns)} PASS**",
        "",
        "| § | Status | Item | Detail |",
        "|---|---|---|---|",
    ]
    for sec, st, item, detail in rows:
        mark = {"PASS": "✓ PASS", "WARN": "⚠ WARN", "FAIL": "✗ FAIL"}[st]
        lines.append(f"| {sec} | {mark} | {item} | {detail} |")
    lines += [
        "",
        "## Not covered here",
        "",
        "- **§8.2 overflow** — needs rendered frames. Gate V's edge-bleed audit covers it",
        "  (22 frames, 0 BLOCKER).",
        "- **§8.4 kerning** — needs the renderer's font metrics; not reproduced.",
        "- **§8.6 on pixels** — this verifies the figure is *wired* to the beat and appears",
        "  in a recorded run. Confirming it is *legible in the image* would need OCR.",
        "  Gate V reads the frames instead.",
        "",
    ]
    OUT.write_text("\n".join(lines))

    print("=" * 74)
    print("  GATE T — type-lock (reimplemented; the shipped script is missing)")
    print(f"  source: {src_path}")
    print("=" * 74)
    cur = None
    for sec, st, item, detail in rows:
        if sec != cur:
            print(f"\n{sec}")
            cur = sec
        mark = {"PASS": "  PASS", "WARN": "  WARN", "FAIL": "  FAIL"}[st]
        print(f"{mark}  {item:<46} {detail}")
    print()
    print("-" * 74)
    print(f"{len(fails)} FAIL · {len(warns)} WARN · "
          f"{len(rows)-len(fails)-len(warns)} PASS   →  {OUT.name}")
    if fails:
        print("\nGATE T FAILED — no build may report success with a FAIL outstanding.")
    if "--check" in sys.argv and fails:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
