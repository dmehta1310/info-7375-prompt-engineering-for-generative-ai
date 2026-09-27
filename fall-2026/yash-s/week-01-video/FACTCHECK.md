# Fact-check — Repeatable Is Not the Same as True

| Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|
| B01 | `sample([1,2,3], seed=7)` returns `{0: 102, 1: 268, 2: 630}` on two independent calls | VERIFIED | Direct call to `sample()` from `lessons/01-randomness-and-first-prompts/code/main.py`, run twice back to back, this machine, 2026-09-25 | none |
| B02 | A seed fixes the starting state of Python's `random.Random`, not the outcomes themselves | VERIFIED | Python `random` module documentation; consistent with `main.py`'s use of `random.Random(seed)` | none |
| B03 | `sample([1,2,3], seed=99)` returns `{0: 93, 1: 267, 2: 640}` | VERIFIED | Direct call to `sample()` from `main.py` with `seed=99`, this machine, 2026-09-25 | none |
| B04 | Repeatability and correctness are logically independent properties | VERIFIED (reasoning, not empirical) | General claim about determinism vs. correctness; not tied to a specific citation, flagged as reasoning in narration | none |
| B05 | This evidence does not establish cross-version/cross-platform repeatability | VERIFIED (explicit boundary) | Only one Python version (3.13.5) and one machine were tested | stated on screen as a limitation |

## Constructed illustrations

- B02's "seed -> generator state -> draws" diagram is an illustrative simplification of the mechanism, not literal source code or a screenshot. Labelled on screen: "Diagram -- illustrative, not literal source code."

## Reproduction command

```bash
python3 -c "import sys; sys.path.insert(0,'lessons/01-randomness-and-first-prompts/code'); from main import sample; print(sample([1,2,3], seed=7)); print(sample([1,2,3], seed=7)); print(sample([1,2,3], seed=99))"
```

Run from the `info-7375-prompt-engineering-for-generative-ai` repo root. `main.py` itself was not modified; the alternate seed was passed directly to the unmodified `sample()` function.

Verified: 2026-09-25.
