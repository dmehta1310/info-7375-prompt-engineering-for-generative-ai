# ~/w1-evidence/offset_evidence.py
import math

def softmax(logits, T=1.0):
    peak = max(logits)
    w = [math.exp((x - peak) / T) for x in logits]
    s = sum(w)
    return [x / s for x in w]

base = softmax([1, 2, 3])
shifted = softmax([1001, 1002, 1003])

print("[1, 2, 3]          ->", base)
print("[1001, 1002, 1003] ->", shifted)
print("bitwise identical? ", base == shifted)
print()

for L in [[1000, 1000], [0, 0], [-5, -5], [1, 2], [1001, 1002]]:
    print(f"{str(L):<16} -> " + str([f"{x:.6f}" for x in softmax(L)]))
print()

print("naive exp at [1000, 1000]:")
try:
    print([math.exp(x) for x in [1000, 1000]])
except OverflowError as e:
    print("  OverflowError:", e)
