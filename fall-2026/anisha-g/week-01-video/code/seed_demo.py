#!/usr/bin/env python3
"""Standalone reproduction of the Chapter 1 sampling mechanism."""
from collections import Counter
import json
import math
import random


def probabilities(logits, temperature=1.0):
    peak = max(logits)
    weights = [math.exp((x - peak) / temperature) for x in logits]
    total = sum(weights)
    return [w / total for w in weights]


def sample(logits, count=1000, seed=7, temperature=1.0):
    rng = random.Random(seed)
    return dict(Counter(rng.choices(
        range(len(logits)),
        probabilities(logits, temperature),
        k=count,
    )))


def ordered(counts):
    return {str(i): counts.get(i, 0) for i in range(3)}


if __name__ == "__main__":
    logits = [1.0, 2.0, 3.0]
    run_a = sample(logits, seed=7)
    run_b = sample(logits, seed=7)
    run_c = sample(logits, seed=8)
    print(json.dumps({
        "course_constructed_input": {
            "logits": logits,
            "count": 1000,
            "temperature": 1.0,
        },
        "probabilities": probabilities(logits),
        "seed_7_run_a": ordered(run_a),
        "seed_7_run_b": ordered(run_b),
        "same_seed_equal": run_a == run_b,
        "seed_8_run": ordered(run_c),
    }, indent=2))
