#!/usr/bin/env python3
from seed_demo import probabilities, sample


def test_probabilities_match_course_output():
    got = probabilities([1.0, 2.0, 3.0])
    expected = [0.09003057317038046, 0.24472847105479764, 0.6652409557748218]
    assert all(abs(a - b) < 1e-15 for a, b in zip(got, expected))


def test_same_seed_repeats():
    assert sample([1.0, 2.0, 3.0], seed=7) == sample([1.0, 2.0, 3.0], seed=7)


def test_recorded_counts():
    assert sample([1.0, 2.0, 3.0], seed=7) == {1: 268, 2: 630, 0: 102}
    assert sample([1.0, 2.0, 3.0], seed=8) == {1: 239, 2: 685, 0: 76}


if __name__ == "__main__":
    test_probabilities_match_course_output()
    test_same_seed_repeats()
    test_recorded_counts()
    print("3/3 checks passed")
