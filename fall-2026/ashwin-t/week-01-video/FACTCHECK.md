# FACTCHECK — w1-softmax-offset

Every factual claim in the narration, what supports it, and its status.
Evidence files are in `w1-evidence/` (copied into this folder for submission).
Numbers were checked by `tools/verify_numbers.py` (on-screen) and by hand (spoken).

| Beat | Claim | Support | Verdict |
|---|---|---|---|
| B00 | A huge score does not necessarily mean a confident model | B04A–B: [1000,1000] → 0.500000, 0.500000 | holds — the video's own evidence |
| B01A | For every possible next token the model produces a raw score (a logit) | Chapter 1 Part 2; `probabilities(logits)` in `main.py` takes one score per candidate | holds — simplified (real vocabularies are large; three tokens is the lesson's toy) |
| B01B | Softmax makes every score positive, then divides each by the total | `main.py`: `math.exp(...)` then `weight / total` | holds (positive via exp; the max-subtraction detail is B03D) |
| B01B | Scores are converted into probabilities that add up to one | `main.py`: `weight / total`; printed values sum to 1 (0.0900… + 0.2447… + 0.6652…) | holds |
| B01C | The model draws one token by weighted chance, in a loop | `main.py` `sample()` uses `rng.choices(..., probabilities)` | holds — `main.py` samples; "loop" is the Chapter 1 framing of repeated next-token prediction |
| B02A | Scores one, two, three are the lesson's inputs | `main.py` `demo()` → `probabilities([1, 2, 3])` | holds — inputs are in the code, not the printout (credit line says so) |
| B02B | 9.00%, 24.47%, 66.52% | `reference-output.txt`: 0.09003057317038046, 0.24472847105479764, 0.6652409557748218 | holds (rounded to 2 dp) |
| B02C | This is actual printed output | `reference-output.txt`, reproduced under Python 3.13.7 and 3.9.6, byte-identical | holds |
| B03A | Adding 1000 gives 1001, 1002, 1003 | arithmetic; `offset_evidence.py` input | holds |
| B03A (visual) | Probabilities stay frozen while the offset counts 0 → 1000 | `intermediates-output.txt`: all 1001 whole-number offsets bitwise identical | holds — every animation frame is covered |
| B03B | Bitwise identical, every digit the same | `offset-output.txt`: `bitwise identical?  True` (Python `==` on floats) | holds |
| B03C | Softmax divides each score's exponential by the total | `main.py` lines computing `weights` and `weight / total` | holds |
| B03C | Adding a constant multiplies every exponential by the same factor, top and bottom, so it cancels | exp(x + c) = exp(x)·exp(c); the factor appears in numerator and denominator | holds — mathematical identity; shown on screen as a constructed word diagram, labelled "constructed diagram" |
| B03D | The code subtracts the largest score first; both runs compute the same intermediates | `main.py` `peak = max(logits)`; `intermediates-output.txt`: both give `[-2, -1, 0]` and identical exp/total | holds — this explains *bitwise* equality, not the cancellation itself |
| B04A–B | [1000,1000], [0,0], [-5,-5] each → 0.500000, 0.500000 | `offset-output.txt` | holds |
| B04C | [1,2] and [1001,1002] → 0.268941, 0.731059 (26.89 / 73.11%) | `offset-output.txt` | holds |
| B04C | "Only the gap survives" | follows from B03C; illustrated by the equal-gap rows | holds for softmax at a fixed temperature |
| B04D | "A huge logit is not a confident model" | [1000,1000] → 50/50 | holds as stated about magnitude; a logit that is large *relative to the others* does raise its probability — the video's claim is about the shared size, and the gap rows say so |
| B04D | A naive version overflows at 1000 | `offset-output.txt`: `OverflowError: math range error` from `math.exp(1000)` | holds for Python floats (IEEE-754 double, max ≈ 1.8e308) |
| B06 | Softmax keeps the gaps and throws away the (shared) size | B03A–B04C | holds — restates the demonstrated result |
| B05 | This does not show calibration | nothing in the evidence compares probabilities with observed correctness | holds — stated boundary |

## Claims deliberately NOT made

- That real models use exactly this code (the lesson's `main.py` is a teaching reference).
- Anything about temperature (T = 1 throughout; T is a different concept).
- The sampled counts in `reference-output.txt` (`268 / 630 / 102`) — printed by `main.py` but not used; they belong to a different Chapter 1 concept.
- Any Claude response. None appears in the video.
