# Evidence for INFO 7375 Week 1 explainer video.
# Concept: an expected count is not a promise. The lesson's own run draws
# token 2 exactly 630 times where the probability predicts 665.24.
#
# Question the video answers: is 630 evidence that the sampler is broken?
# Everything below is computed, not asserted. No invented figures.
import math
import sys
from collections import Counter
import random

sys.path.insert(0, "../../../../lessons/01-randomness-and-first-prompts/code")
import main as lesson

LOGITS = [1, 2, 3]
N = 1000
TOKEN = 2

print("=" * 72)
print("BEAT 1 — what the lesson actually prints")
print("=" * 72)
probs = lesson.probabilities(LOGITS)
counts = lesson.sample(LOGITS, count=N, seed=7)
print("probabilities:", probs)
print("counts (seed=7):", counts)
print()
p = probs[TOKEN]
expected = p * N
observed = counts[TOKEN]
print(f"token {TOKEN}: p = {p}")
print(f"  expected = p * {N} = {expected}")
print(f"  observed = {observed}")
print(f"  shortfall = {observed - expected:.2f}")
print()

print("=" * 72)
print("BEAT 2 — how big is a normal miss? (binomial spread)")
print("=" * 72)
sd = math.sqrt(N * p * (1 - p))
z = (observed - expected) / sd
print(f"standard deviation = sqrt(n*p*(1-p)) = sqrt({N}*{p:.6f}*{1-p:.6f})")
print(f"                   = {sd}")
print(f"z-score for {observed} = ({observed} - {expected:.2f}) / {sd:.3f} = {z:.4f}")
print(f"so the lesson's own default seed lands {abs(z):.2f} SD BELOW expectation")
print()
print("typical range (expected +/- 1 SD):",
      f"{expected - sd:.1f} to {expected + sd:.1f}")
print("2 SD range:", f"{expected - 2*sd:.1f} to {expected + 2*sd:.1f}")
print(f"{observed} falls outside the 2 SD range: {abs(z) > 2}")
print()

print("=" * 72)
print("BEAT 3 — exact binomial tail: how rare is <= 630?")
print("=" * 72)
# exact, in log space to avoid underflow
def log_binom_pmf(k, n, p):
    return (math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
            + k * math.log(p) + (n - k) * math.log1p(-p))

tail = math.fsum(math.exp(log_binom_pmf(k, N, p)) for k in range(0, observed + 1))
print(f"P(count <= {observed}) = {tail:.8f}")
print(f"                        = about 1 in {1/tail:.1f} runs")
print(f"P(count == {observed}) = {math.exp(log_binom_pmf(observed, N, p)):.8f}")
print()

print("=" * 72)
print("BEAT 4 — don't take the formula's word for it. Run 10,000 seeds.")
print("=" * 72)
TRIALS = 10000
tallies = []
for seed in range(TRIALS):
    rng = random.Random(seed)
    c = Counter(rng.choices(range(len(LOGITS)), probs, k=N))
    tallies.append(c[TOKEN])

tallies_sorted = sorted(tallies)
mean_obs = sum(tallies) / TRIALS
sd_obs = math.sqrt(sum((t - mean_obs) ** 2 for t in tallies) / TRIALS)
at_or_below = sum(1 for t in tallies if t <= observed)

print(f"seeds 0..{TRIALS-1}, {N} draws each")
print(f"  mean count for token {TOKEN} = {mean_obs}   (formula said {expected:.2f})")
print(f"  observed SD                  = {sd_obs:.4f}   (formula said {sd:.4f})")
print(f"  min = {tallies_sorted[0]}   max = {tallies_sorted[-1]}")
print()
print(f"  seeds landing at or below {observed}: {at_or_below} of {TRIALS}"
      f" = {100*at_or_below/TRIALS:.2f}%")
print(f"  exact binomial predicted:            {100*tail:.2f}%")
print()
print("  percentiles of the 10,000 counts:")
for q in (1, 5, 25, 50, 75, 95, 99):
    print(f"    p{q:<3} = {tallies_sorted[int(q/100*TRIALS)]}")
print()
print(f"  where seed 7 ({observed}) ranks: "
      f"{100*at_or_below/TRIALS:.2f}th percentile")
print()

print("=" * 72)
print("BEAT 5 — the boundary: one run cannot tell you which story is true")
print("=" * 72)
print("A sampler biased to p =", f"{observed/N}", "would ALSO produce 630.")
biased_p = observed / N
print(f"  fair sampler   (p={p:.4f}) producing exactly {observed}: "
      f"{math.exp(log_binom_pmf(observed, N, p)):.6f}")
print(f"  biased sampler (p={biased_p:.4f}) producing exactly {observed}: "
      f"{math.exp(log_binom_pmf(observed, N, biased_p)):.6f}")
print()
print("Both stories produce the number we saw. One run of 1000 does not")
print("separate them. That is the thing this video does NOT establish.")
