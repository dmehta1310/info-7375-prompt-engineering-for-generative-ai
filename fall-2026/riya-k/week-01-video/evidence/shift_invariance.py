# Evidence for INFO 7375 Week 1 explainer video.
# Concept: softmax is shift-invariant -- subtracting the max changes every
# intermediate value but leaves the distribution identical.
#
# The lesson function (lessons/01-randomness-and-first-prompts/code/main.py)
# ALREADY subtracts the peak. To show what the subtraction does, this file
# defines a naive variant with that one line removed and compares them.
# Nothing here is invented; every printed number comes from math.exp.
import math
import sys
import json

sys.path.insert(0, "../../../../lessons/01-randomness-and-first-prompts/code")
import main as lesson


def naive_probabilities(logits, temperature=1.0):
    """The lesson's probabilities() with the `- peak` removed. Nothing else differs."""
    weights = [math.exp(x / temperature) for x in logits]
    total = sum(weights)
    return [w / total for w in weights]


def intermediates(logits, subtract_peak, temperature=1.0):
    peak = max(logits) if subtract_peak else 0.0
    shifted = [x - peak for x in logits]
    weights = [math.exp(x / temperature) for x in shifted]
    total = sum(weights)
    return {
        "logits": logits,
        "peak_subtracted": peak,
        "shifted_logits": shifted,
        "exp_weights": weights,
        "sum_of_weights": total,
        "probabilities": [w / total for w in weights],
    }


def show(title, d):
    print(f"--- {title} ---")
    for k, v in d.items():
        print(f"  {k}: {v}")
    print()


print("=" * 70)
print("BEAT 2/3: the intermediates move, the distribution does not")
print("=" * 70)
print()

LOGITS = [1, 2, 3]
naive = intermediates(LOGITS, subtract_peak=False)
shifted = intermediates(LOGITS, subtract_peak=True)
show("naive: exp(logit)", naive)
show("lesson: exp(logit - max)", shifted)

print("sum of weights changed by a factor of:",
      naive["sum_of_weights"] / shifted["sum_of_weights"])
print("which is exp(max) = exp(3) =", math.exp(3))
print()
print("probabilities identical to the last bit?",
      naive["probabilities"] == shifted["probabilities"])
print("max absolute difference:",
      max(abs(a - b) for a, b in zip(naive["probabilities"],
                                     shifted["probabilities"])))
print("lesson main.probabilities([1,2,3]) agrees?",
      lesson.probabilities(LOGITS) == shifted["probabilities"])
print()

print("=" * 70)
print("BEAT 4: [1000, 1000] -- where the naive path stops existing")
print("=" * 70)
print()

BIG = [1000, 1000]
try:
    print("naive_probabilities([1000, 1000]) ->", naive_probabilities(BIG))
except OverflowError as e:
    print("naive_probabilities([1000, 1000]) -> OverflowError:", e)
print("exp(1000) is the failure point; largest float is", sys.float_info.max)
print("lesson.probabilities([1000, 1000]) ->", lesson.probabilities(BIG))
print()
print("and the same shift applied to an UNEQUAL pair keeps the asymmetry:")
print("  lesson.probabilities([1000, 1001]) ->", lesson.probabilities([1000, 1001]))
print("  lesson.probabilities([0, 1])       ->", lesson.probabilities([0, 1]))
print("  identical?", lesson.probabilities([1000, 1001]) == lesson.probabilities([0, 1]))
print()

print("=" * 70)
print("BEAT 5: what the distribution does NOT settle -- expected vs observed")
print("=" * 70)
print()

probs = lesson.probabilities(LOGITS)
counts = lesson.sample(LOGITS, count=1000, seed=7)
print("probabilities:", probs)
print("expected counts over 1000 draws:", [p * 1000 for p in probs])
print("observed counts (seed=7):", counts)
for i, p in enumerate(probs):
    print(f"  token {i}: expected {p*1000:.2f}  observed {counts.get(i, 0)}"
          f"  diff {counts.get(i, 0) - p*1000:+.2f}")
print()
print("lesson demo() verbatim:")
print(json.dumps(lesson.demo(), indent=2))
