# Fact Check

| Video claim | Evidence | Result |
|---|---|---|
| Course demonstration uses logits `[1,2,3]`, count `1000`, temperature `1`, seed `7` | `main.py::demo()` and `sample()` defaults | PASS |
| Probabilities are `0.090030573…`, `0.244728471…`, `0.665240955…` | Unmodified course output and `code/seed_output.txt` | PASS |
| Seed-7 counts are `{0:102,1:268,2:630}` | Unmodified `main.py` output | PASS |
| Repeating seed 7 returns the same counts here | `code/seed_demo.py`; equality check is `true` | PASS |
| Changing only to seed 8 gives `{0:76,1:239,2:685}` | Recorded local run of the course function | PASS |
| The seed initializes a local generator | `main.py`: `rng = random.Random(seed)` | PASS |
| Official test 04 checks repeatability of two same-default calls | Course `test_main.py::test_04` | PASS |
| Repeatability does not establish truth | Chapter 1 paragraphs on the seed and claim boundary | PASS |
| No source, answer key, or verifier enters `sample()` | Function signature and body in `main.py` | PASS |

## Inspected revisions

- Course repository commit: `cc6dbf177bc956975636e2fc1d4fed1ee4129d34`
- Brutalist repository commit: `6a8380ae169cca81e0633664a65c958f5c12ab4b`
- Inspection date: 2026-09-26
