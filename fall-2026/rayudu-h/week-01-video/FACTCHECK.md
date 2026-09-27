# FACTCHECK — temperature-is-concentration

Every figure that reaches the screen, with its source and its verification.
Source of truth: `chapter1-course/lessons/01-randomness-and-first-prompts/code/main.py`
(scores `[1, 2, 3]`, seed 7, n = 1000), saved to `week-01-video/main-output.txt`.
Independently recomputed 2026-09-16 with a standalone softmax before authoring
the Manim scenes; every value below matched to the digits shown.

## Claims and their evidence

| # | Claim on screen / in narration | Beat | Source | Status |
|---|---|---|---|---|
| 1 | p = exp(z/T) ÷ Σ exp(z/T) | B02 | chapter 1 prose + `main.py` | VERIFIED — the function's own form |
| 2 | At T=1: 0.0900, 0.2447, 0.6652 | B02 | `main-output.txt` `probabilities` | VERIFIED exactly (0.09003057317038046, 0.24472847105479764, 0.6652409557748218) |
| 3 | The three probabilities sum to 1.000000 | B02 | recomputed | VERIFIED — 1.000000000000 |
| 4 | p₂/p₀ = exp((z₂ − z₀)/T) | B04 | derivation; normalization cancels | VERIFIED symbolically and numerically. **Shown on screen since 2026-09-26:** both probabilities carry the same total Σ exp(z/T), which cancels |
| 5 | z₂ − z₀ = 2, fixed at every T | B04 | scores `[1, 2, 3]` | VERIFIED — 3 − 1 = 2 by construction |
| 6 | Ratios 54.5981500331 / 7.3890560989 / 2.7182818285 at T = 0.5 / 1 / 2 | B04 | recomputed from softmax | VERIFIED to 10 dp |
| 7 | Those ratios are exactly e⁴, e², e¹ | B04 | recomputed | VERIFIED — matched to < 1e-9 |
| 8 | Ordering [2, 1, 0] never changes | B04, B06 | all four T values computed | VERIFIED at T = 0.5, 1, 2, 0.1 |
| 9 | At T=0.1, p₀ = 2.061060e-09 — small, not zero | B05 | recomputed | VERIFIED — 2.061060e-09 |
| 10 | T=0 raises `ValueError: Need logits and a positive finite temperature` | B05 | `main.py` guard clause | VERIFIED — also rejects negative, inf, nan, empty |
| 11 | Seed-7 counts 849 / 630 / 469 (outcome 2 at T = 0.5 / 1 / 2), and the full T = 2 row 202 / 329 / 469 | B06 | `worked-examples.json`, reproduced by `main.py` | VERIFIED; T=1 count 630 matches `main-output.txt`. Re-run 2026-09-26 via `main.py`'s own `sample()` at T = 0.5, 1 and 2 (Python 3.12.9): all nine counts match the recorded table exactly |
| 12 | Concentration is not correctness | B05, B06 | argument, not measurement | JUDGEMENT — stated as the boundary, never as a measured result |
| 13 | No temperature can turn a positive gap negative, so no two outcomes ever swap places | B04 | for T > 0, (z_i − z_k)/T has the same sign as z_i − z_k, so p_i/p_k > 1 exactly when z_i > z_k | VERIFIED symbolically — holds at every T > 0, not only the three temperatures tested |

**The code, not just the textbook formula.** `main.py` computes `exp((x − peak) / T)`, subtracting the largest score before exponentiating, for numerical stability. The peak cancels in any ratio exactly as the total does, so the derivation shown in B04 holds for the program as written.

## Numbers deliberately NOT used

- The chapter's "labels as answers / answer key = label 0" wrong-answer
  hypothetical is a **constructed illustration**, so it is cut from this reel
  entirely rather than shown with a caption. Nothing on screen depends on it.
- No model-version numbers, no vendor benchmark figures, nothing that dates. *(True as of
  2026-09-25. Until then the Claude composer's model chip showed its default — a real
  model name — in B00, B03 and B07. It is now blank.)*

## Constructed / exaggerated visuals, labelled on screen

| Where | What | On-screen label |
|---|---|---|
| B05 | The outcome-0 bar at T=0.1 is 2.061060e-09 tall and would be invisible at true scale; it is drawn as a 0.06-unit sliver | "sliver exaggerated for visibility" |
| B04 | Bar length encodes the exponent (z₂ − z₀)/T = 4, 2, 1 rather than the raw ratio (a 20× span would not fit the frame) | "bar length = (z₂ − z₀) / T" |
| B01A | The contrast-slider analogy. The three swatch brightnesses are chosen for legibility and are **not** the measured probabilities; no figure from `main.py` appears anywhere in this beat | "analogy — illustrative, not measured" |
| B05 | The same three swatches return at full contrast as the closing callback. Identical encoding to B01A, still no measured figure; the caption obligation was discharged when the analogy was introduced | carries the B01A caption by reference |

Both are honest encodings captioned in-frame. No other figure is scaled,
rounded up, or stylised.

## The analogy beat (B01A) and what it is allowed to claim

B01A explains temperature with an everyday contrast slider before any algebra.
It is an ANALOGY, captioned as one on screen for its whole duration, and it
carries no measured figure — deliberately, so nothing in it can be mistaken for
evidence.

The one structural claim it makes IS faithful, which is why it earns its place
rather than merely decorating the reel. On-screen brightness is computed as

    v = mid + (b - mid) * k

a positive affine map of the baseline brightness `b`. For any `k > 0` such a map
is strictly order-preserving, so the brightest swatch is the brightest swatch at
every slider position — the marker pinned to it never has to move. That is the
same reason temperature cannot reorder a softmax: dividing every logit by `T > 0`
rescales the gaps between them and leaves their order alone. The analogy and the
mechanism share a property; they are not merely similar-sounding.

The "run backwards" line (added 2026-09-25) is faithful for the same reason. In the scene
the slider position `k` multiplies every deviation from the mid grey; in the softmax `1/T`
multiplies every score gap, since `log p_i − log p_k = (z_i − z_k)/T`. So `k` plays the role
of `1/T`, and lower temperature means higher contrast — the inversion is the mathematics,
not a figure of speech.

What the analogy does NOT carry: the exponential. Contrast is linear in
brightness, softmax is exponential in the logits, so the analogy is exact about
ORDERING and only suggestive about MAGNITUDE. The magnitudes are established
properly in B04 with the real ratios, which is why B01A precedes it rather than
replacing it.

## Rounding policy

Narration speaks rounded values ("zero point six seven", "fifty-four point six")
because spoken 10-dp figures are unlistenable. The SCREEN always carries the
precise figure: 4 dp for probabilities as `main.py` prints them, 10 dp for the
ratios, full scientific notation for 2.061060e-09.
