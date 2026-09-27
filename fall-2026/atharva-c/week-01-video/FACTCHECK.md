# FACTCHECK — Why 630, Not 665?

Verified 2026-09-25 by Claude Code (Opus 5.5) against local evidence. Python 3.12.7.
Evidence folder: `learning-artifacts/week-01-atharva-c/` (course repo root).

## Evidence identity

- `main.py` sha256 `a2847abab5646fe09bcdcfa8fe744a784d9a9639d45ebb9ea519c6343b10326d`
  — byte-identical to the course reference `lessons/01-randomness-and-first-prompts/code/main.py`.
  It is shown as the **course reference, unmodified**, not as Atharva's own implementation.
- Command: `python3 main.py` (run from the evidence folder). Stdout sha256, two runs:
  `21d13a7abe795a69299fd4731553614fbef47ac2b89a00ac61085b34b4670d25` (identical both times).
- Recorded stdout (matches notes.md exactly):

```
{"probabilities": [0.09003057317038046, 0.24472847105479764, 0.6652409557748218],
 "counts": {"1": 268, "2": 630, "0": 102}}
```

## Claims

| # | Claim (beat) | Evidence | Status |
|---|---|---|---|
| C1 | Probabilities ≈ 9.0 / 24.5 / 66.5 % (B00, B03) | stdout | ✓ |
| C2 | Counts 102 / 268 / 630, total 1,000 (B00, B04) | stdout; sum checked | ✓ |
| C3 | Softmax → seeded `rng.choices` → `Counter` (B02) | main.py L9–24 | ✓ |
| C4 | Expected counts ≈ 90 / 245 / 665 (665.24) (B03) | p × 1000: 90.03, 244.73, 665.24 | ✓ |
| C5 | Outcome 2 came in 35 short; others high (+12, +23) (B04) | 665.24 − 630 = 35.24; 102 − 90.03 = 11.97; 268 − 244.73 = 23.27 | ✓ |
| C6 | Typical wander ≈ 15 (B05; narration "wanders by about fifteen") | √(1000 · 0.66524 · 0.33476) = 14.923 (the binomial standard deviation, called "wander" on screen) | ✓ |
| C7 | Gap ≈ 2.4 × typical wander (B05 "Gap ÷ wander", B07) | 35.24 / 14.923 = 2.3615 | ✓ |
| C8 | Fair sampler gives ≤ 630 in ~1 run in 100 (B05) | exact binomial P(X ≤ 630 \| n=1000, p=0.66524) = 0.010364 | ✓ |
| C9 | Seed fixed at 7; reruns print the same 630 (B06) | main.py L19 `seed=7`, L27 `sample([1, 2, 3])`; two reruns identical sha256 | ✓ |
| C10 | One run cannot establish fairness (B06, B07) | Atharva's stated limitation; C8 shows fair samplers produce this result ~1% of the time | ✓ (reasoning) |
| C11 | B04 bars: outcome 2 expected 665.24 vs observed 630; outcome 1 expected 244.73 vs observed 268; note: outcome 0 expected 90.03 vs observed 102 | C2 (stdout counts) + C4 (p × 1000). Bar length ∝ count on a zero baseline (TtEffectBars scales to the largest value, 665.24); printed labels are the exact values | ✓ |
| C12 | B06B "What This Does Not Show": one run is one data point and can't tell bad luck apart from a biased die; telling them apart takes many rolls with different starting points | Same basis as C10: a fair sampler yields ≤ 630 in ~1 % of runs (C8), so a single run is consistent with both a fair and a biased sampler; distinguishing them needs repeated runs with different seeds. "Die" is an analogy for the three-outcome sampler | ✓ (reasoning) |
| C13 | B08 check: with the default seed, every run prints 630 | main.py L19 `def sample(logits, count=1000, seed=7, …)`; `sample.__defaults__` = (1000, 7, 1.0). 2026-09-26: five calls of `main.sample([1, 2, 3])` → outcome-2 counts [630, 630, 630, 630, 630]; seeds 0–4 → [669, 683, 683, 660, 655]. Holds for these logits and count; main.py hash unchanged after the check | ✓ |

Verification command (C6–C8):

```bash
python3 -c "
import math
p=0.6652409557748218; n=1000
mu=n*p; sd=math.sqrt(n*p*(1-p)); print(mu, sd, (630-mu)/sd)
pmf=lambda k: math.comb(n,k)*p**k*(1-p)**(n-k)
print(sum(pmf(k) for k in range(631)))"
# 665.2409557748218 14.92298316472358 -2.361522182650978
# 0.010363986526186503
```

C13 verification command (run from the evidence folder; `-B` writes no `__pycache__`):

```bash
python3 -B -c "
import main
print([main.sample([1, 2, 3])[2] for _ in range(5)])        # [630, 630, 630, 630, 630]
print([main.sample([1, 2, 3], seed=s)[2] for s in range(5)])  # [669, 683, 683, 660, 655]
print(main.sample.__defaults__)"                             # (1000, 7, 1.0)
```

## Corrections applied (DOUBLE-CHECK LAW)

1. **Takeaway wording.** Original: "can differ by a normal amount". 630 sits in about the
   bottom 1 % of fair runs (C8), so "normal" overstated it. Approved rewording (Atharva
   C, 2026-09-25): *"Expected (665.24) and observed (630) counts can differ by chance
   even when the sampler is correct. This gap is unusual (about 2.4 typical spreads) but not
   evidence of a bug."*
2. **Authorship of the code.** The evidence `main.py` is the course reference, not a student
   reimplementation; on-screen titles say so.

## Algebra / math note

No typeset equation beats (course prerequisite: avoid equation beats in a first video).
Numbers only; "Gap ÷ spread" and "630/1000"-style arithmetic are short and unambiguous.
The spread formula appears only in this file.
