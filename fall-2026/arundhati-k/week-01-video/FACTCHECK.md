# FACTCHECK — claude-liam-expected-vs-observed

Status: **GATE F CLOSED — 2026-09-26.** 16 rows verified against
`lessons/01-randomness-and-first-prompts/code/main.py` (unmodified, seed=7,
count=1000, logits `[1,2,3]`, temperature 1.0) and against the binomial
distribution that sampler implies.

**One row failed on the first pass and changed the video.** See row 11 and the
correction log at the bottom — four beats were rewritten and re-rendered.

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation |
|---|---|---|---|---|
| 1 | B00 | probabilities are 9%, 24.5%, 66.5% | ✅ PASS | `main.py` prints `[0.09003057317038046, 0.24472847105479764, 0.6652409557748218]` |
| 2 | B00/B04 | the run returned 630 for index 2 | ✅ PASS | `main.py` prints `{"1": 268, "2": 630, "0": 102}` |
| 3 | B02 | logits `[1,2,3]` are the input | ✅ PASS | `demo()` calls `probabilities([1, 2, 3])` — source line 27 |
| 4 | B02 | softmax subtracts the largest value, exponentiates, divides by the total | ✅ PASS | source line 14–17: `peak = max(logits)`; `exp((x - peak) / temperature)`; `weight / total` |
| 5 | B02 | intermediates 0.1353, 0.3679, 1.0000 | ✅ PASS | `exp(-2)=0.135335`, `exp(-1)=0.367879`, `exp(0)=1.0` — recomputed |
| 6 | B02 | divisor is 1.5032 | ✅ PASS | sum of the three = 1.503214 — recomputed |
| 7 | B03 | `0.6652409557748218 × 1000 = 665.24` | ✅ PASS | = 665.2409557748218; displayed to 2dp |
| 8 | B03 | expected count is a long-run average, not a prediction about one run | ✅ PASS | definition of expectation for a binomial count, `E[X] = np`. The beat strikes through the wrong framing on screen |
| 9 | B04 | seed 7, 1000 draws | ✅ PASS | `sample(logits, count=1000, seed=7, temperature=1.0)` — source line 19 |
| 10 | B05 | gap is 35.24 draws, ≈5.3% below expected | ✅ PASS | `665.2409557748218 − 630 = 35.2409557748218`; `/665.24 = 5.297%` |
| 11 | B01/B05/B06 | **the size and rarity of the gap** | ⚠️ **FAILED → CORRECTED** | See correction log below. 630 is z = −2.3615, P(X≤630) = 1.036% — **unusual, not ordinary** |
| 12 | B05/B06 | ≈2.4 standard deviations; about 1 run in 50 | ✅ PASS | `sd = sqrt(1000 × 0.66524 × 0.33476) = 14.9230`; `z = −2.3615`; `P(X≤630) = 0.010364` → ≈1 in 97 one-tailed, ≈1 in 48 two-tailed. "About one in fifty" is the two-tailed reading and is the conservative claim |
| 13 | B06/B07 | one seeded run, read after the fact, cannot establish the probability is wrong | ✅ PASS | Standard inference: a single realisation selected post hoc is not a pre-specified test. The narration explicitly does *not* claim the gap is ordinary — it claims it is not a verdict |
| 14 | B06/B08 | what would settle it is repetition + checking where 630 falls | ✅ PASS | Correct remedy for the claim being made; B08 hands the viewer exactly that experiment |
| 15 | B07 | a seed makes a run repeatable, not correct | ✅ PASS | `random.Random(seed)` fixes the stream; it carries no information about whether the weights are right. This is a Chapter 1 listed concept |
| 16 | B04 | printed key order is `1, 2, 0` | ✅ PASS | `Counter` preserves first-encountered order; reproduced verbatim rather than sorted |

---

## Correction log — the row that changed the video

**2026-09-26, during GATE F.** The first cut of this reel asserted that 630 was
an *ordinary* sampling outcome. B01's hesitant-writer correction landed on
`broken → normal`, and B06's right panel captioned the observed value
"ordinary, once you can see the spread," drawn mid-pack in the distribution.

I had verified the arithmetic (665.24, 35.24, 5.3%) and stopped there. I had not
verified the *statistical* claim that sat on top of it. Running it:

```python
sd = sqrt(1000 * 0.6652409557748218 * 0.3347590442251782)  # 14.9230
z  = (630 - 665.2409557748218) / 14.9230                   # -2.3615
P(X <= 630)                                                #  0.010364
```

630 is about **2.4 standard deviations** below the expected count — roughly a
**1-in-50** result. Calling it ordinary was false, and it was false in the
direction that flattered the video's thesis, which is the failure mode this
chapter is actually about. A fluent explanation had been built on an unchecked
claim.

**What changed.** The concept survives, and is sharper stated correctly: the gap
*is* unusual, and unusual still is not evidence the probabilities are wrong —
because this is one draw, from one fixed seed, examined after the fact. Surprise
is a reason to run the test, not a substitute for having run it.

| Beat | Before | After |
|---|---|---|
| B01 | correction `broken → proof`… reading "That looks normal." | correction `proof → unusual` — "A gap that size is unusual." |
| B05 | "about five percent below" | adds "two point four standard deviations — roughly one run in fifty" |
| B06 | "ordinary, once you can see the spread"; 630 drawn mid-pack | "in the tail — about 1 run in 50, not mid-pack"; 630 drawn at bin 3, its true position |
| B07 | verdict line said only that a gap is not evidence | adds "630 is ~2.4 sd below expected — about 1 run in 50. Unusual, not ordinary." |

Audio regenerated for B01, B05, B06, B07; those four beats re-rendered.
Runtime moved 141.14s → 146.69s.

**GATE F SIGNED — 2026-09-26.**

---

## Second correction — 2026-09-26, consistency sweep before submission

Re-reading all ten narrations end to end, **B08 still carried the pre-correction
framing.** Two leftovers, both contradicting the corrected B06:

| Where | Said | Problem |
|---|---|---|
| B08 narration | "whether 630 is boring or surprising" | B05–B07 had already established it *is* surprising — ~1 in 50 |
| B08 output line | "if 630 sits mid-pack, the gap was never evidence" | B06 draws 630 in the **tail**, not mid-pack |

Fixing the four beats that made the claim was not enough; the handoff that
*depended* on the claim kept the old version. A viewer reaching B08 would have
been told the question was still open after the video had answered it.

**Corrected to:** the handoff now states the calculated prediction (tail, ~1 in
50), names it as arithmetic rather than measurement, and invites the viewer to
check it — *"if the plot disagrees with my number, the plot is right."* That is
a better handoff than the original, because it hands over a falsifiable claim of
mine instead of an open question.

B08 audio regenerated (19.78s → 20.33s), beat re-rendered, master rebuilt.
Runtime 146.69s → **147.24s**. GATE T **PASS**, GATE V **clean** on the rebuild.
