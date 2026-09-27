# Defense Notes — Be Ready to Explain This

## The idea in one sentence

Subtracting the same maximum from every score makes the largest shifted exponent zero, while the common exponential factor cancels and preserves the normalized probability ratios.

## Walk through the course example

1. The course scores are `[1, 2, 3]`; their maximum is `3`.
2. Subtracting `3` gives `[-2, -1, 0]`.
3. Exponentiation gives approximately `[0.135335, 0.367879, 1]`.
4. The weights sum to approximately `1.503215`.
5. Dividing each weight by the total gives `[0.090030573…, 0.244728471…, 0.665240955…]`, the actual output printed by course `main.py`.

## Explain the official large-score test

For `[1000, 1000]`, subtracting the maximum gives `[0, 0]`. The weights become `[1, 1]`, so normalization returns `[0.5, 0.5]`. The shared offset `1000` carried no relative-preference information.

## Explain the algebra

`exp(z_i - m) = exp(z_i) × exp(-m)`.

The factor `exp(-m)` appears in every weight. Factoring it out of the denominator makes it cancel with the same factor in the numerator. Therefore the normalized ratios are unchanged.

## Why the maximum?

Any shared constant preserves the mathematical distribution. The maximum is useful because the largest shifted score becomes zero and every other shifted score is non-positive. Their exponential weights are therefore no larger than one, avoiding unnecessarily large positive exponentials.

## What it does not prove

It does not prove that the scores are correct, that the most likely token is true, that probabilities are calibrated, or that the short teaching implementation safely covers every extreme input. Use the narrow wording “overflow protection in this calculation,” not the unlimited slogan “perfectly stable.”

## AI and voice disclosure

Claude was not used. Codex assisted with research, code, narration, rendering, and documentation. The voice is local synthetic Kokoro `af_bella`, not Siddhesh Nikam or the instructor. The course source, toolkit, fonts, and AI assistance are disclosed in `SOURCES.md` and the actual revision process is documented in `FRICTIONAL.md`.
