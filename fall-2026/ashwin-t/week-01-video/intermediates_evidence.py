# w1-evidence/intermediates_evidence.py
# Prints the intermediate values inside the lesson's softmax
# (same steps as probabilities() in lessons/01-randomness-and-first-prompts/code/main.py)
# so every number shown in Beat 3's "why" shot traces to printed output.
import math

for logits in ([1, 2, 3], [1001, 1002, 1003]):
    peak = max(logits)
    shifted = [x - peak for x in logits]
    weights = [math.exp(x) for x in shifted]
    total = sum(weights)
    print(f"logits          {logits}")
    print(f"  minus max     {shifted}")
    print(f"  exp(...)      {weights}")
    print(f"  total         {total}")
    print(f"  / total       {[w / total for w in weights]}")
    print()

# Beat 3 animates the offset counting 0 -> 1000 in whole steps while the
# probabilities stay frozen. Check every one of those frames, not just the last.
def softmax(logits):
    peak = max(logits)
    w = [math.exp(x - peak) for x in logits]
    s = sum(w)
    return [x / s for x in w]

base = softmax([1, 2, 3])
same = [c for c in range(0, 1001) if softmax([1 + c, 2 + c, 3 + c]) == base]
print(f"offsets 0..1000 checked: {1001}")
print(f"bitwise identical to [1, 2, 3]: {len(same)}")
print(f"all identical? {len(same) == 1001}")
