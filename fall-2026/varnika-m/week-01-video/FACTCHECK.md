# FACTCHECK — three-scores-not-three-chances

Status: checked 2026-09-26 by Claude Code against the saved evidence; narration approved by Varnika M 2026-09-26.
Every figure was recomputed by running the course code with Python 3.12.14. `scenes.py` imports the same
`main.py` and refuses to render if the numbers drift.

Evidence files: `evidence/main_py_output.txt` (real `main.py` output), `evidence/worked_steps.txt` (all
intermediate steps). Chapter = `chapters/01-randomness-and-first-prompts.md`, "Three scores are not yet three chances".

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | B00 | `main.py` turns scores 1, 2, 3 into chances 0.090, 0.245, 0.665 | PASS | `evidence/main_py_output.txt`: 0.09003057317038046, 0.24472847105479764, 0.6652409557748218 | — |
| 2 | B00 | The composer screen is not a Claude reply | EXEMPT | Labelled on screen "Reconstructed interface · not a Claude reply"; no Claude call was made | — |
| 3 | B01/B02 | Chances must be nonnegative and sum to one | PASS | Chapter 1: "Probabilities must be nonnegative and sum to one." | — |
| 4 | B02 | Scores 1, 2, 3 add up to six | PASS | 1 + 2 + 3 = 6; chapter: "These scores sum to six." | — |
| 5 | B03 | Divide-by-total gives 1/6, 2/6, 3/6 (0.167, 0.333, 0.500) | PASS | `evidence/worked_steps.txt`, "divide-by-sum shortcut" | — |
| 6 | B03 | For the CONSTRUCTED scores −1, 2, 3, the total is 4 and −1 ÷ 4 = −0.25 | PASS | `evidence/worked_steps.txt`; labelled CONSTRUCTED EXAMPLE on screen | — |
| 7 | B04 | The code subtracts the top score, then applies the exponential | PASS | `lessons/01-randomness-and-first-prompts/code/main.py` lines 14–15 | — |
| 8 | B04 | The exponential turns any number into a positive one; bigger score → bigger weight | PASS | exp is positive and increasing for finite real input; chapter: "An exponential converts any finite real input into a positive mathematical value." | — |
| 9 | B04 | Subtracting the top score keeps numbers small and does not change the answer | PASS | Chapter 1, "The subtraction that changes nothing important" (common factor cancels) | — |
| 10 | B04 | 1, 2, 3 → −2, −1, 0 → weights 0.135, 0.368, 1.000 | PASS | `evidence/worked_steps.txt`: 0.135335, 0.367879, 1.0 | — |
| 11 | B05 | Weights total about 1.503 | PASS | `evidence/worked_steps.txt`: total 1.503215 | — |
| 12 | B05 | Weight ÷ total = 0.090, 0.245, 0.665, "exactly what main.py prints" | PASS | `evidence/main_py_output.txt` (three decimals shown; full values in the on-screen printed panel) | — |
| 13 | B05 | Top score keeps the top chance | PASS | Order preserved: 0.090 < 0.245 < 0.665 | — |
| 14 | B06 | CONSTRUCTED −1, 2, 3 → about 0.013, 0.265, 0.721; all positive; total 1 | PASS | `evidence/worked_steps.txt`: 0.0132, 0.2654, 0.7214; weights 0.018316, 0.367879, 1.0, total 1.386195 | — |
| 15 | B07 | The conversion never checks which option is correct | PASS | `probabilities(logits, temperature)` takes no answer key; chapter's constructed hypothetical (chapter: outcome zero correct, lower temperature still favours outcome two; shown as options A and C) | — |
| 16 | B07 | The answer key "option A is correct" | EXEMPT | Constructed hypothetical, labelled CONSTRUCTED HYPOTHETICAL on screen; taken from the chapter's own hypothetical | — |
| 17 | B09 | Suggested prompt uses scores 2, 0, −3 | EXEMPT | A viewer exercise; no answer is shown or claimed | — |
| 18 | B10 | Narration is a synthetic voice | PASS | Kokoro `am_onyx`, generated locally by `generate_audio_kokoro.py` | — |
