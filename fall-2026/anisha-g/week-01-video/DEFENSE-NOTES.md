# Defense Notes — Be Ready to Explain This

## The idea in one sentence

A seed initializes the pseudorandom generator so the same sampling process can be replayed under the same setup; it does not provide evidence that the selected output is true.

## Walk through the course example

1. Logits `[1,2,3]` at temperature `1` produce probabilities about `[0.0900, 0.2447, 0.6652]`.
2. `sample()` creates `random.Random(seed)` and uses its weighted choices 1,000 times.
3. With seed `7`, the observed counts are `{0:102,1:268,2:630}`.
4. A new call with the same seed starts the local generator at the same state and reproduces those counts in this environment.
5. Changing only the seed to `8` gives `{0:76,1:239,2:685}`. The probability rule did not change; the selected finite sequence did.

## What the official test proves

`test_04` compares `sample([1,2])` with another identical call. Both use the default seed `7`, so equality supports repeatability under that tested setup. It does not compare either sampled label against an independently checked answer.

## Why repeatability is not truth

The function receives `logits`, `count`, `seed`, and `temperature`. It does not receive a source, answer key, evidence, or verification rule. A deterministic replay can therefore preserve a wrong preference just as reliably as a correct one.

## Important limitation

Say “repeatable in the recorded environment and setup,” not “guaranteed identical forever.” Chapter 1 explicitly avoids promising identical sequences across all future interpreter versions.

## AI and voice disclosure

Claude was not used. Codex assisted with research, code, narration, rendering, and documentation. The voice is local synthetic Kokoro `af_bella`, not Anisha Gaikar or the instructor. All assistance and assets are disclosed in `SOURCES.md` and `FRICTIONAL.md`.
