# FACTCHECK — week-01-shifted-not-changed

Status: **GATE F — all 22 rows PASS. Two narration fixes applied before audio (rows 5 and 14); rows 17–18 added 2026-09-18; row 14 corrected, rows 19–20 added 2026-09-24; row 13 corrected and row 21 added later on 2026-09-24; row 22 added 2026-09-25.**

Figures reach the screen as beat-sheet props, which override the components' schema
defaults (see `SOURCES.md` §5.8). Every claim the film makes is either (a) an arithmetic result reproducible by
`evidence/verify_claims.py` against the course's unmodified reference implementation, or
(b) a statement the chapter itself makes. The reel shows **no Claude response**, no
screenshots and no generated imagery. It **does** show a reconstructed Claude interface in
B00, B05 and B09. Every one of those beats carries an on-screen disclosure pill, and no
prompt shown in them was ever sent (row 20; `SOURCES.md` §3, §5.16).

**Primary sources.**
`S1` = [`chapters/01-randomness-and-first-prompts.md`](../../../chapters/01-randomness-and-first-prompts.md)
`S2` = [`lessons/01-randomness-and-first-prompts/code/main.py`](../../../lessons/01-randomness-and-first-prompts/code/main.py) (imported unmodified)
`S3` = [`evidence/run-output.txt`](evidence/run-output.txt) — recorded run, Python 3.12.7 (CPython), macOS 26.6.2 arm64, 2026-09-15 (re-run 2026-09-24 under macOS 27.0: byte-identical except the platform line)
`S4` = CPython `sys.float_info` / `math` on the same interpreter
`S5` = [`evidence/boundary-output.txt`](evidence/boundary-output.txt) — recorded run of `boundary_analysis.py`; first recorded 2026-09-18, file last written 2026-09-24, and a re-run reproduces it byte for byte
`S6` = [`evidence/mutation-output.txt`](evidence/mutation-output.txt) — recorded run of `mutation_check.py`, 2026-09-24 (29 tests)
`S7` = [`evidence/crosscheck-output.txt`](evidence/crosscheck-output.txt) — recorded run of `cross_check.py` across four interpreters, 2026-09-24

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix if needed |
|---|---|---|---|---|---|
| 1 | B00 | Chapter 1's constructed input is the scores `[1, 2, 3]`, and the code subtracts the largest before exponentiating | ✓ PASS | S1 §"Three scores are not yet three chances"; S2 `peak = max(logits)` | — |
| 2 | B00/B01 | The subtraction changes every intermediate but not the returned distribution | ✓ PASS | S1: "We have changed the intermediate weights, not the intended normalized distribution"; measured in S3 rows 1–2 | — |
| 3 | B02 | `math.exp(1000)` raises `OverflowError: math range error` | ✓ PASS | S3 claim 3 — verbatim exception text, caught and printed, not paraphrased | — |
| 4 | B02 | float64 tops out at `1.797693e+308`, and `exp` crosses it at ≈ `709.7827` | ✓ PASS | S4 — `sys.float_info.max` and `math.log(sys.float_info.max)`, printed in S3 | — |
| 5 | B02 | "That is not rounding. It is a refusal." | ✓ PASS | S3 — Python raises rather than returning `inf`, because `math.exp` signals range errors. Narration says *refusal*, not *crash* | **FIXED**: draft said "Python crashes". It does not crash — it raises a catchable exception. Reworded to "It refuses." |
| 6 | B03 | For `[1, 2, 3]` the shifted scores are `[-2, -1, 0]` | ✓ PASS | S1 states this verbatim; S3 claim 1 confirms | — |
| 7 | B03 | Weights ≈ `0.1353352832`, `0.3678794412`, `1.0`; total ≈ `1.5032147244` | ✓ PASS | S1 gives `0.135335 / 0.367879 / 1` and sum `1.503215`; S3 claim 1 gives full precision | — |
| 8 | B03 | The largest weight is **exactly** 1.0, because e⁰ = 1 | ✓ PASS | S3 claim 1 `largest_weight_is_exactly_one: True` — an equality test, not a tolerance | — |
| 9 | B03 | The distribution is `0.0900305732`, `0.2447284711`, `0.6652409558` | ✓ PASS | Matches S1's published T = 1.0 table to 10 dp; S3 claim 2 asserts the match programmatically | — |
| 10 | B03 | "The denominator can never fall below 1" | ✓ PASS | Follows from row 8: the peak contributes exactly 1 and all other weights are ≥ 0. S3 claim 4 checks five cases including `[0, -1e9]`, all `>= 1: True` | — |
| 11 | B04 | `exp(−m/T)` is a common factor in numerator and every denominator term, so it cancels | ✓ PASS | S1 §"The subtraction that changes nothing important" — the chapter's own derivation, re-set as a scene | — |
| 12 | B04 | "That is algebra, not a numerical trick" | ✓ PASS | S1 distinguishes exactly this: "The cancellation above establishes equality in the mathematical expression. A numerical test compares values represented by a computer." | — |
| 13 | B06 | Shifted and direct paths differ by `1.1102230246251565e-16` — "exactly 2\*\*-53 — adjacent floats, one step apart" | ✓ PASS (after fix) | S3 claim 2 `max_abs_difference`. Equals 2⁻⁵³ exactly — **half** of Python's `sys.float_info.epsilon` (2⁻⁵²) — and one ulp of the largest probability; each differing pair is two adjacent floats (`math.nextafter`) | **FIXED 2026-09-24**: gloss and narration said "one machine epsilon", which Python defines as 2⁻⁵², twice this. `SOURCES.md` §5.17 |
| 14 | B06 | The two vectors differ in exactly two digit positions out of fifty-three | ✓ PASS | Both strings are 62 chars containing **53 digit characters**; differing indices are 19 and 60 (verified by character comparison) | **FIXED**: draft narration said the two paths return "the same numbers". Measured, they do not. Rewritten to "identical in algebra, indistinguishable in floating point" — see `SOURCES.md` §5 |
| 15 | B07 | `probabilities([0, -800])` returns `[1.0, 0.0]` — an exact zero for an outcome whose true share is ≈ `1e-348`; the cliff is at `-746` (`-745` still returns `5e-324`) | ✓ PASS | S3 claim 5, four cases. `true_value_log10 = z/ln(10)`; `5e-324` is the smallest denormal | — |
| 16 | B07/B08 | The claim earned is "overflow-safe", **not** "numerically stable" | ✓ PASS | S1 instructs exactly this: "Keep the tested claim narrower than the slogan 'numerically stable'", and "not a proof that every imaginable numeric input is handled perfectly" | Quote shown on screen, attributed to Chapter 1 |
| 17 | B07 | The cliff is `−1075 · ln 2 = −745.133219102`, and −746 is the first integer past it | ✓ PASS | `S5` = [`evidence/boundary-output.txt`](evidence/boundary-output.txt). binary64's smallest subnormal is 2⁻¹⁰⁷⁴; under round-to-nearest anything below half of that (2⁻¹⁰⁷⁵) has no nearer neighbour than zero, so `exp(z) == 0.0` once `z < ln(2⁻¹⁰⁷⁵)`. Bisection of the real boundary agrees to 9 dp | Added 2026-09-18 — upgrades row 15 from a swept result to a predicted one |
| 22 | B06 | The `1 ULP` markers drawn between each differing pair | ✓ PASS | Each differing pair is exactly one representable step apart: `math.nextafter` steps from one to the other, and their IEEE-754 integer patterns differ by exactly 1. The screen test reads the label from `beat_sheet.json` and checks it against that step count | Added 2026-09-25 with the change the submitter asked for after watching (`REVIEW.md` Round 10) |
| 18 | evidence only (not in the film) | Past the cliff, two outcomes 100 nats apart both report as `0.0`; log space keeps them ranked | ✓ PASS | `S5` — `probabilities([0,−800,−900])` → `[1.0, 0.0, 0.0]` vs log space `[0.0, −800.0, −900.0]`. The log-space form reproduces the reference to 1e-12 on `[1,2,3]` | Deliberately NOT a beat — one concept per the brief; it lives in `boundary_analysis.py` |
| 19 | B02 | The same `[1000, 1000]` that raises `OverflowError` returns `[0.5, 0.5]` once the max is subtracted | ✓ PASS | `S3` claim 3 — `shifted_result_is_half_half: True`, an exact equality. S1 makes this its canonical test: "The lesson tests this choice with equal large scores, [1000, 1000], and expects [0.5, 0.5]" | Added 2026-09-24 — the film previously showed the break with no payoff |
| 20 | B00, B05, B09 | The composer beats show no Claude response, and are labelled as reconstructed | ✓ PASS (after fix) | B00 `output` is now `[]`; all three render through `ShiftComposer` with a disclosure pill present from the first frames; model chip reads "Claude", not a version | **FIXED 2026-09-24**: B00 had shown three authored answer lines under "Fable 5" — a fabricated transcript the brief says fails the assignment. See `SOURCES.md` §5.16 |
| 21 | B06 | "Had I called them equal, I would have been wrong in the last place of two numbers" | ✓ PASS (after fix) | Two of the three entries differ, each by one step (one ulp at its own magnitude); the third is identical. Checked by `math.nextafter` and by comparing IEEE-754 bit patterns | **FIXED 2026-09-24**: said "wrong by exactly one bit"; the first pair differs in two bits (`…1010` vs `…1001`). `SOURCES.md` §5.17 |

## Claims deliberately NOT made

Checked and excluded, because the evidence in this film does not support them:

- **Was not claimed; now measured — and the claim is stated at the size of the evidence.**
  This bullet used to read *"Not claimed: that these figures reproduce on any other
  interpreter."* That was honest while only one interpreter had been tried, but it was a
  testable claim, so `evidence/cross_check.py` tests it. Every figure the film displays —
  including the seeded counts `[102, 268, 630]` and the `1.1102230246251565e-16`
  difference — is **byte-identical across CPython 3.10.19, 3.12.7, 3.13.3 and 3.14.6**,
  and **3.14.6 is the interpreter S1 records its own run on**. What that still does *not*
  establish: all four run on **one platform and architecture** (macOS 27.0, arm64). IEEE-754
  says the float64 behaviour should hold elsewhere; "should" is not "was measured", and no
  other architecture was tested. `S7` = [`evidence/crosscheck-output.txt`](evidence/crosscheck-output.txt).
- **Not claimed:** that any of this describes what a Claude model does. The film explains
  a normalization in a teaching implementation. S1's own framing — the toy "is that step,
  at a scale you can print" — is not stretched into a claim about a production system, and
  no temperature setting of any product is mentioned.
- **Not claimed:** that a concentrated distribution is evidence of correctness. That is
  Chapter 1's separate point and belongs to a different concept; it is out of scope here
  and no hypothetical answer key appears.
- **Not claimed:** that the function is unsafe or buggy. The underflow in row 15 is a
  float64 limit, not a defect in `main.py` — which S1 explicitly frames as "a short
  teaching implementation, not a universal numeric-validation library". The film says the
  *slogan* is too wide, not that the *code* is wrong. This distinction is load-bearing and
  is stated in B08.

## Verification

Run from the reel folder (or from the posted `fall-2026/suketh-p/week-01-video/` folder — the scripts locate
the course reference by walking up, or via `INFO7375_REF`):

```bash
python3 evidence/verify_claims.py          # rows 1–16
python3 evidence/boundary_analysis.py      # rows 17–18, the derivation and the remedy
python3 -m unittest discover -s evidence   # 29 tests; every row above, as an assertion
python3 evidence/mutation_check.py         # do those 29 tests actually bite? 4/4 caught
python3 evidence/gate_t_typecheck.py       # GATE T: §8.6 re-checks every figure above
python3 evidence/cross_check.py            # every figure, under every python3.N on PATH
```

`mutation_check.py` is the honesty check on the other three: it implements Chapter 1's
Assessment 10 by perturbing the function under test and reporting which assertions
survive. It is the reason row 17 exists at all — it showed that a suite can be green and
still be blind, which is the same distinction this film is about.

Drafted and checked by Claude in the build sessions: 2026-09-15; rows 17–18 added
2026-09-18; rows 19–21 and the row-13 correction 2026-09-24, when the verification block
was re-run; row 22 on 2026-09-25. This is an evidence check, not a sign-off. The human
review of the rendered cut is the `[MINE]` section of `REVIEW.md`: watched by the submitter
on 2026-09-25, with one change requested and made; its teaching questions are still open.
