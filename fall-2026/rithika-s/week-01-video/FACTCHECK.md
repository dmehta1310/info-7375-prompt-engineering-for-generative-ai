# FACTCHECK — "The Token That Followed"

DOUBLE-CHECK LAW. Every claim the narration makes, with a verdict and the fix applied.
The reel's load-bearing claims are mathematical, so the "source" for most rows is the
definition plus `verify_softmax.py`, which re-derives the figure and asserts it.

| # | Claim, as narrated | Verdict | Source | Fix applied |
|---|---|---|---|---|
| 1 | "softmax is exp(z) divided by the sum of exp(z)" | **TRUE** — definition | Standard definition of the softmax function | none |
| 2 | `Σ exp(z) = 58.9230` for these four logits | **TRUE** | `verify_softmax.py`, asserted | none |
| 3 | The four probabilities are `0.9266 / 0.0461 / 0.0170 / 0.0103` | **TRUE at 4 dp** | `verify_softmax.py`, asserted | Displayed at 4 dp *because* that is where this set sums to exactly 1.0 — stated in SOURCES rather than implied to be general |
| 4 | "They sum to exactly one hundred percent" | **TRUE as displayed** | `92.7 + 4.6 + 1.7 + 1.0 = 100.0`, asserted | none |
| 5 | "Cross-entropy is the negative log of the probability on the target" | **TRUE** for a one-hot target | `L = −Σ yᵢ ln pᵢ` collapses to `−ln p_target` when `y` is one-hot | Narration says "every other term is multiplied by zero and vanishes" so the collapse is shown, not assumed |
| 6 | `L = −ln 0.0461 = 3.0762` nats | **TRUE** | `verify_softmax.py`, asserted | Unit named as *nats* (natural log), not bits |
| 7 | "Had the corpus said rock … zero point zero seven" | **TRUE** — `−ln 0.9266 = 0.0762` | `verify_softmax.py`, asserted | Narration rounds to "zero point zero seven"; the screen shows `0.0762` |
| 8 | "Being right costs exactly three more nats" | **TRUE, exactly** | `ln pᵢ − ln pⱼ = zᵢ − zⱼ` under a shared denominator; asserted to `1e-12` | Replaced an earlier draft's "penalized forty times harder" — see below |
| 9 | "The gradient on the scores is simply p minus y" | **TRUE** — exact, not an approximation | Standard result for softmax composed with cross-entropy | Narration says "exact, not an approximation" and the screen repeats it |
| 10 | `p − y` column sums to zero | **TRUE** | Both `p` and `y` sum to 1, so their difference sums to 0; asserted | none |
| 11 | "rock … pushed down harder than gas or light" | **TRUE** for this example | `+0.9266 > +0.0170 > +0.0103` | Scoped to the example, not stated as a general law |
| 12 | "The real moon is rock" | **TRUE** | The Moon is a rocky/silicate body | Phrased plainly; no figure or composition claim attached |
| 13 | "The moon is made of green cheese" is a corpus line | **CONSTRUCTED — not a real corpus** | A long-standing English idiom for an absurd belief; invented here as a training line | Labelled `CONSTRUCTED EXAMPLE` on screen on every beat that shows a figure, and named as invented in the narration ("a science-fiction novel I invented for this video") |
| 14 | The four-token vocabulary | **CONSTRUCTED** | — | Beat B09 states a real vocabulary is ~10⁵ tokens; the reel never implies four is realistic |
| 15 | "Pretraining's target is the token that followed in the text" | **TRUE** of the next-token prediction objective | The objective's own definition — the label comes from the corpus, not from a truth oracle | none |
| 16 | Post-training / RLHF "steers the model toward factual accuracy" | **NOT ASSERTED — named as out of scope** | — | Beat B09 states this explicitly as something the reel *does not* establish. No mechanism, rate, or result is claimed for it |
| 17 | Any claim about a specific shipped model | **NONE MADE** | — | Deliberate: no model names, versions, or counts appear anywhere, so the reel cannot date |

## Corrections applied

1. **"Forty times harder" — cut.** A draft line said being right was "penalized forty
   times harder." `3.0762 / 0.0762 ≈ 40.4` is arithmetically real but meaningless: a
   *ratio* of log-losses is not a quantity anyone interprets. Replaced with the exact
   and defensible statement — being right costs **exactly three more nats**, which is
   the logit gap itself.
2. **The accent token.** B02 originally highlighted `of` rather than `green` (an index
   error, `focusIndex` 4 vs 5). A beat about which token is being conditioned on was
   accenting the wrong word. The index is now derived from the sentence and asserted.
3. **Rounding is disclosed, not hidden.** The narration says "four point six percent"
   while the screen shows `0.0461`; both are the same number at different precision,
   and the screen always carries the higher precision.

## What would falsify the reel

Running `python3 verify_softmax.py`. It recomputes `exp(z)`, the softmax, both
cross-entropy values, the loss-gap identity and the gradient from the four logits, and
**exits non-zero** if any figure shown on screen fails to reproduce. That is the only
claim in the reel that could be wrong in a way arithmetic would catch — everything else
is either a definition or explicitly scoped out in B09.
