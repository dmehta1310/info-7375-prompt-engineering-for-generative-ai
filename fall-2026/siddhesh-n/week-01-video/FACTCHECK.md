# Fact Check

| Video claim | Evidence | Result |
|---|---|---|
| Course input is `[1,2,3]` | Chapter 1 and `main.py::demo()` | PASS |
| Maximum is `3` | `code/softmax_demo.py` | PASS |
| Shifted scores are `[-2,-1,0]` | Chapter 1 § max subtraction; reproduced locally | PASS |
| Weights are approximately `0.135335`, `0.367879`, `1` | Chapter 1 and captured local run | PASS |
| Weight total is approximately `1.503215` | Chapter 1 and captured local run | PASS |
| Probabilities are `0.090030573…`, `0.244728471…`, `0.665240955…` | Actual unmodified `main.py` output in `code/course_main_output.txt` | PASS |
| `[1000,1000]` returns `[0.5,0.5]` | Course `test_main.py::test_02`; local assertion | PASS |
| Shared `exp(−m)` factor cancels | Chapter 1 algebraic derivation | PASS |
| Probabilities sum approximately to one | Course `test_01`; local `math.isclose` assertion | PASS |
| Transformation does not establish truth or universal extreme-input safety | Chapter 1 limitation paragraphs | PASS |

## Inspected revisions

- Course repository commit: `cc6dbf177bc956975636e2fc1d4fed1ee4129d34`
- Brutalist repository commit: `6a8380ae169cca81e0633664a65c958f5c12ab4b`
- Inspection date: 2026-09-26
