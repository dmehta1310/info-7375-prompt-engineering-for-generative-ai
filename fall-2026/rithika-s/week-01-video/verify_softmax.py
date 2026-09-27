#!/usr/bin/env python3
"""
verify_softmax.py — arithmetic proof for every number shown on screen in
"The Token That Followed" (INFO 7375, Week 01, Chapter 1).

CONSTRUCTED EXAMPLE. The corpus lines, the four-token vocabulary, and the four
logits are invented teaching values, not measurements from a real trained
model. What IS real is the arithmetic: the softmax is computed here in the five
steps the video shows on screen — raw logits, subtract the max, exponentiate,
normalize, final probabilities — with no rounding fudges, and every figure the
video displays is asserted against this script.

The max-subtraction step is not decoration. It is how softmax is actually
implemented (exp(z) overflows for large z), and it is mathematically identical
to the naive form because exp(z-m)/Σexp(z-m) = exp(z)/Σexp(z). The video shows
the real implementation, so this script proves both forms agree.

Run:   python3 verify_softmax.py            # prove, print the worked table
       python3 verify_softmax.py --emit      # also write softmax_values.json
Exit 0 = every on-screen number is reproduced exactly.
"""
import json
import math
import sys
from pathlib import Path

# ── The constructed setup ───────────────────────────────────────────────────
FALSE_LINE = "The moon is made of green cheese"
TRUE_LINE  = "The moon is made of grey rock"
CONTEXT    = "The moon is made of green"
TARGET     = "cheese"          # the token that FOLLOWED in the false corpus
TRUTH      = "rock"            # the token that follows in the true corpus

# Vocabulary slice, ordered by the model's own ranking (descending logit).
VOCAB  = ["rock", "cheese", "gas", "light"]
LOGITS = [ 4.0,    1.0,      0.0,   -0.5  ]

DP = 4                          # display precision used on screen


def pipeline(logits):
    """The five steps, in the order the video shows them."""
    m = max(logits)                                  # step 2: the max
    shifted = [z - m for z in logits]                # step 2: z - max
    exps = [math.exp(s) for s in shifted]            # step 3: exponentiate
    total = sum(exps)                                # step 4: the denominator
    probs = [e / total for e in exps]                # step 5: normalize
    return m, shifted, exps, total, probs


zmax, shifted, exps, exp_sum, probs = pipeline(LOGITS)

# Naive form, for the identity check only — never shown on screen.
naive = [math.exp(z) for z in LOGITS]
naive_probs = [e / sum(naive) for e in naive]

print("CONSTRUCTED EXAMPLE")
print(f'false corpus : "{FALSE_LINE}"')
print(f'true corpus  : "{TRUE_LINE}"')
print(f'context      : "{CONTEXT}" -> ?')
print(f"target       : {TARGET!r}  (the token that followed in the false corpus)")
print()

# ── The five steps, as a table ─────────────────────────────────────────────
print(f"{'token':>8} {'1: z':>7} {'2: z-max':>10} {'3: exp':>9} {'4: /sum':>20} {'5: p':>9} {'p %':>7}")
for tok, z, s, e, p in zip(VOCAB, LOGITS, shifted, exps, probs):
    frac = f"{e:.4f}/{exp_sum:.4f}"
    print(f"{tok:>8} {z:>7.1f} {s:>10.1f} {e:>9.4f} {frac:>20} {p:>9.4f} {p*100:>6.1f}%")
print(f"{'SUM':>8} {'':>7} {'':>10} {exp_sum:>9.4f} {'':>20} {sum(probs):>9.4f} {sum(probs)*100:>6.1f}%")
print(f"\nmax subtracted: {zmax:.1f}")
print()

# ── Step assertions: every displayed value, at display precision ───────────
assert zmax == 4.0, zmax
assert [round(s, 1) for s in shifted] == [0.0, -3.0, -4.0, -4.5], shifted

EXP4 = [round(e, DP) for e in exps]
assert EXP4 == [1.0, 0.0498, 0.0183, 0.0111], EXP4
# the exp column as displayed must add up to the denominator as displayed
assert round(sum(EXP4), DP) == round(exp_sum, DP) == 1.0792, (sum(EXP4), exp_sum)

P4 = [round(p, DP) for p in probs]
PCT1 = [round(p * 100, 1) for p in probs]
assert P4 == [0.9266, 0.0461, 0.0170, 0.0103], P4
assert sum(P4) == 1.0, f"4-dp probabilities must sum to exactly 1.0, got {sum(P4)}"
assert sum(PCT1) == 100.0, f"percentages must sum to exactly 100.0, got {sum(PCT1)}"

# max-subtraction must be numerically identical to the naive form
for a, b in zip(probs, naive_probs):
    assert math.isclose(a, b, rel_tol=0, abs_tol=1e-12), (a, b)

print(f"step 2  z-max          {[round(s,1) for s in shifted]}")
print(f"step 3  exp(z-max)     {EXP4}   sum = {round(exp_sum, DP)}   EXACT")
print(f"step 5  probabilities  {P4}   sum = {sum(P4)}   EXACT")
print(f"        percentages    {PCT1}  sum = {sum(PCT1)}  EXACT")
print(f"        max-subtraction == naive softmax to 1e-12   OK")
print()

# ── Cross-entropy: the loss only ever reads the TARGET slot ────────────────
i_t, i_r = VOCAB.index(TARGET), VOCAB.index(TRUTH)
loss_target = -math.log(probs[i_t])
loss_truth  = -math.log(probs[i_r])
assert round(loss_target, DP) == 3.0762, round(loss_target, DP)
assert round(loss_truth, DP) == 0.0762, round(loss_truth, DP)

# The identity: the loss gap IS the logit gap, exactly.
logit_gap = LOGITS[i_r] - LOGITS[i_t]
assert math.isclose(loss_target - loss_truth, logit_gap, rel_tol=0, abs_tol=1e-12)

print(f"false corpus  L = -ln p({TARGET}) = -ln {probs[i_t]:.4f} = {loss_target:.4f} nats")
print(f"true corpus   L = -ln p({TRUTH})   = -ln {probs[i_r]:.4f} = {loss_truth:.4f} nats")
print(f"gap = {loss_target - loss_truth:.4f} nats == logit gap {logit_gap:.1f}   (exact)")
print()

# ── The two target vectors the contrast beat compares ─────────────────────
y_false = [1.0 if t == TARGET else 0.0 for t in VOCAB]
y_true  = [1.0 if t == TRUTH  else 0.0 for t in VOCAB]
assert y_false == [0.0, 1.0, 0.0, 0.0], y_false
assert y_true  == [1.0, 0.0, 0.0, 0.0], y_true
assert sum(y_false) == sum(y_true) == 1.0
print(f"y (false corpus, target {TARGET!r}) = {[int(v) for v in y_false]}")
print(f"y (true  corpus, target {TRUTH!r})   = {[int(v) for v in y_true]}")
print("the SAME forward pass; only the corpus, and therefore y, changed")
print()
print("ALL ASSERTIONS PASSED — every on-screen number is reproduced exactly.")

# ── Emit the verified figures so the beat sheet cannot drift from them ─────
if "--emit" in sys.argv:
    out = {
        "_note": "Generated by verify_softmax.py. Beat-sheet scene props are built "
                 "from this file so no on-screen number is hand-typed.",
        "vocab": VOCAB,
        "logits": LOGITS,
        "max": zmax,
        "shifted": [round(s, 1) for s in shifted],
        "exps": EXP4,
        "exp_sum": round(exp_sum, DP),
        "probs": P4,
        "pct": PCT1,
        "target": TARGET,
        "truth": TRUTH,
        "y_false": [int(v) for v in y_false],
        "y_true": [int(v) for v in y_true],
        "loss_target": round(loss_target, DP),
        "loss_truth": round(loss_truth, DP),
        "logit_gap": logit_gap,
        "false_line": FALSE_LINE,
        "true_line": TRUE_LINE,
        "context": CONTEXT,
    }
    p = Path(__file__).resolve().parent / "softmax_values.json"
    p.write_text(json.dumps(out, indent=2) + "\n")
    print(f"wrote {p.name}")
