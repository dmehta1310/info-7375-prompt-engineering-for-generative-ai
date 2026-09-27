#!/usr/bin/env python3
"""Reproduce every numeric claim shown in the Week 1 explainer.

The probabilities function is reproduced from the INFO 7375 Chapter 1 reference
implementation, with attribution in SOURCES.md. This file adds labeled prints for
the intermediate values used in the video.
"""
import math


def probabilities(logits, temperature=1.0):
    if not logits or not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("Need logits and a positive finite temperature")
    if not all(math.isfinite(x) for x in logits):
        raise ValueError("Logits must be finite")
    peak = max(logits)
    weights = [math.exp((x - peak) / temperature) for x in logits]
    total = sum(weights)
    return [weight / total for weight in weights]


logits = [1, 2, 3]
peak = max(logits)
shifted = [x - peak for x in logits]
weights = [math.exp(x) for x in shifted]
total = sum(weights)
probs = probabilities(logits)
large_equal = probabilities([1000, 1000])

print("SOURCE INPUT: Chapter 1 reference example")
print("logits:", logits)
print("peak:", peak)
print("shifted:", shifted)
print("weights:", weights)
print("weight total:", total)
print("probabilities:", probs)
print("probability sum:", sum(probs))
print("OFFICIAL TEST INPUT: [1000, 1000]")
print("official test probabilities:", large_equal)
assert large_equal == [0.5, 0.5]
assert math.isclose(sum(probs), 1.0)
