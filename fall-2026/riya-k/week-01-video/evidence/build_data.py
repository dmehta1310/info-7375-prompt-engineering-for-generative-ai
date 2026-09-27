# Computes every figure the video displays and caches it to video_data.json.
# The Manim scenes read this file, so nothing on screen is typed by hand.
import json, math, random, sys
from collections import Counter

sys.path.insert(0, "../../../../lessons/01-randomness-and-first-prompts/code")
sys.path.insert(0, "../../../lessons/01-randomness-and-first-prompts/code")
sys.path.insert(0, "lessons/01-randomness-and-first-prompts/code")
import main as lesson

LOGITS, N, TOKEN, TRIALS = [1, 2, 3], 1000, 2, 10000

probs = lesson.probabilities(LOGITS)
counts = lesson.sample(LOGITS, count=N, seed=7)
p, observed = probs[TOKEN], counts[TOKEN]
expected = p * N
sd = math.sqrt(N * p * (1 - p))

def log_pmf(k, n, pp):
    return (math.lgamma(n+1) - math.lgamma(k+1) - math.lgamma(n-k+1)
            + k*math.log(pp) + (n-k)*math.log1p(-pp))

tallies = []
for seed in range(TRIALS):
    rng = random.Random(seed)
    tallies.append(Counter(rng.choices(range(len(LOGITS)), probs, k=N))[TOKEN])

ts = sorted(tallies)
mean_obs = sum(tallies)/TRIALS
sd_obs = math.sqrt(sum((t-mean_obs)**2 for t in tallies)/TRIALS)
at_or_below = sum(1 for t in tallies if t <= observed)
biased_p = observed / N

data = {
    "lesson_raw": lesson.demo(),
    "p": p, "n": N, "token": TOKEN,
    "expected": expected, "observed": observed,
    "shortfall": observed - expected,
    "sd": sd, "z": (observed - expected)/sd,
    "band1": [expected - sd, expected + sd],
    "band2": [expected - 2*sd, expected + 2*sd],
    "trials": TRIALS,
    "mean_obs": mean_obs, "sd_obs": sd_obs,
    "min": ts[0], "max": ts[-1],
    "at_or_below": at_or_below,
    "pct_at_or_below": 100*at_or_below/TRIALS,
    "exact_tail": math.fsum(math.exp(log_pmf(k, N, p)) for k in range(observed+1)),
    "percentiles": {str(q): ts[int(q/100*TRIALS)] for q in (1,5,25,50,75,95,99)},
    "histogram": dict(sorted(Counter(tallies).items())),
    "p_obs_given_fair": math.exp(log_pmf(observed, N, p)),
    "p_obs_given_biased": math.exp(log_pmf(observed, N, biased_p)),
    "biased_p": biased_p,
}
json.dump(data, open("video_data.json", "w"), indent=2)
print(f"wrote video_data.json")
print(f"  expected {data['expected']:.2f}  observed {data['observed']}  z {data['z']:.3f}")
print(f"  10k seeds: mean {data['mean_obs']}  sd {data['sd_obs']:.4f}")
print(f"  at/below {observed}: {at_or_below} = {data['pct_at_or_below']:.2f}%")
print(f"  P(630|fair) {data['p_obs_given_fair']:.6f}  P(630|biased) {data['p_obs_given_biased']:.6f}")
