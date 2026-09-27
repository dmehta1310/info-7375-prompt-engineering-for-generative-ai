# FACTCHECK — Less Room to Wander

Status: checked 2026-09-26 by Claude Code (Opus 5.5) against the narration Prasad S signed in PEDAGOGY.md (SIGNED, 2026-09-26). Every "Claim" cell quotes the signed narration or the on-screen text word for word; the "Source / derivation" cell follows PEDAGOGY.md's evidence notes.

Method: figures recomputed from `evidence/temp-1.0.json` and `evidence/temp-0.5.json`. Both files match a fresh call of the unedited `probabilities()` / `sample()` in `lessons/01-randomness-and-first-prompts/code/main.py` (logits [1, 2, 3], seed 7, n = 1000). The spread √(n·p·(1−p)) is computed only as a check and never shown as a formula.

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | B00 | on screen: "temp 1.0: expected 665.24, observed 630" | PASS | 0.6652409557748218 × 1000 = 665.24; temp-1.0.json counts["2"] = 630 | — |
| 2 | B00 | on screen: "temp 0.5: expected 866.8, observed 849" | PASS | 0.8668133321973349 × 1000 = 866.81 (1 dp as in ANALYSIS.md); temp-0.5.json counts["2"] = 849 | — |
| 3 | B00 | on screen: "same seed (7) both runs"; spoken: "two temperatures, same seed" | PASS | `sample(..., seed=7)` default, main.py:19 | — |
| 4 | B00 | "This is a synthetic narrator, Kokoro's Bella voice, reading a script Prasad reviewed. It isn't Prasad, and it isn't anyone official." | PASS | Kokoro `af_bella`; PEDAGOGY.md sign-off 2026-09-26 | — |
| 5 | B01 | "Lower the temperature and the sample has less room to wander. That part is guaranteed." | PASS | ANALYSIS.md: "that part is guaranteed by the math"; spread 14.92 → 10.74 | — |
| 6 | B01 | "one seeded run can't settle it" | PASS | ANALYSIS.md limitation paragraph (both runs seed 7) | — |
| 7 | B02 | "This is the course's reference code, untouched." | PASS | main.py lines 9–17 copied by script; `git status` shows lessons/ unchanged | — |
| 8 | B02 | "The biggest is subtracted for stability, everything is divided by the temperature, then exponentiated and normalized." | PASS | main.py:14–17 (`peak = max(logits)`, `(x - peak) / temperature`, `math.exp`, `/ total`) | — |
| 9 | B02 | "Temperature reshapes the odds. It doesn't change which answer is right." | PASS | docs/en.md:27 "Temperature changes the distribution, not the truth of the answer." | — |
| 10 | B03 | "At 1.0, the top token gets about two-thirds of the probability." | PASS | temp-1.0.json probabilities[2] = 0.6652 | — |
| 11 | B03 | "Drop to 0.5 and it jumps to about eighty-seven percent, while the other two shrink." | PASS | temp-0.5.json probabilities[2] = 0.8668; others 0.0900→0.0159, 0.2447→0.1173 | — |
| 12 | B03 | on screen: "Top token · temp 1.0" 66.5, "Top token · temp 0.5" 86.7, "Other two · temp 1.0" 33.5, "Other two · temp 0.5" 13.3 (%); note "Other two = sum of tokens 0 and 1" | PASS | probabilities[2] = 0.6652 / 0.8668; probabilities[0] + [1] = 0.0900 + 0.2447 = 0.3348 and 0.0159 + 0.1173 = 0.1332 | — |
| 13 | B04 | "expected count is probability times a thousand draws" | PASS | counts sum to 1000 in both files | — |
| 14 | B04 | "At temperature 1.0 that predicts 665 top-token picks. The run got 630, about 35 short." | PASS | 665.24 − 630 = 35.24 (ANALYSIS.md ~35) | — |
| 15 | B04 | "At 0.5 the prediction is 867, and the run got 849, about 18 short." | PASS | 866.81 − 849 = 17.81 (ANALYSIS.md ~18) | — |
| 16 | B04 | "The gap roughly halved." | PASS | 35.24 / 17.81 = 1.98 | — |
| 17 | B05 | "Before the temperature 0.5 run, Prasad predicted the direction: the gap would get closer." | EXEMPT | timing rests on Prasad's own statement of 2026-09-26; no file records it (as noted in PEDAGOGY.md) | — |
| 18 | B05 | on screen: two quoted sentences + "Prasad S · evidence/ANALYSIS.md (verbatim)" | PASS | ANALYSIS.md lines 6 and 8, verbatim | — |
| 19 | B05 | "It did, both in raw counts and measured in standard deviations" | PASS | 35.24 → 17.81 raw; 2.36 → 1.66 SD | — |
| 20 | B06 | "The spread, how far a thousand draws usually wander, drops from about fifteen to about eleven." | PASS | √(1000·0.6652·0.3348) = 14.92; √(1000·0.8668·0.1332) = 10.74; ANALYSIS.md ±14.9 / ±10.7 | — |
| 21 | B06 | "The math guarantees that as the favorite gets more dominant." | PASS | n·p·(1−p) decreases for p above 0.5; ANALYSIS.md line 10 | — |
| 22 | B06 | "this run's miss also shrank in spread units, from 2.4 to 1.7" | PASS | 35.24 / 14.92 = 2.36; 17.81 / 10.74 = 1.66; ANALYSIS.md 2.4 / 1.7 | — |
| 23 | B07 | "Both runs used seed 7, so they drew from the same stream of random numbers." | PASS | main.py:22 `rng = random.Random(seed)` with seed=7 in both runs | — |
| 24 | B07 | "nothing here says what happens at 2.0, because that run hasn't been done" | PASS | only temp-1.0.json and temp-0.5.json exist in evidence/ | — |
| 25 | BVDT | "sixty-six and a half percent at 1.0, eighty-six point seven at 0.5"; "about 35 at 1.0 and about 18 at 0.5" | PASS | rows 10–11, 14–15 (66.52%, 86.68%) | — |
| 26 | BVDT | "The expected spread shrinks as the favorite dominates; that part is guaranteed. Landing closer in standard-deviation terms may be this seed's luck, because both runs shared seed 7." | PASS | rows 21–23; ANALYSIS.md reasoning + limitation | — |
| 27 | BHTF | "I ran a softmax sampler on logits [1, 2, 3], 1,000 draws, seed 7, at temperatures 1.0 and 0.5" | PASS | method in beat_sheet.json metadata | — |
| 28 | BOUT | "Narrated by a synthetic voice for Prasad S, INFO 7375."; on screen: "Synthetic narration (Kokoro af_bella) · Claude interface reconstructed · not an official or endorsed video" | PASS | Kokoro af_bella; ClaudeComposerAsk is a Remotion reconstruction | — |

## Notes that don't change any claim
- **B01 on-screen wording differs from the PEDAGOGY.md scene note.** PEDAGOGY.md describes the writer correcting "gets more accurate" → "has less room to wander". The rendered B01 corrects "accurate" → "tightly bunched" instead ("the sample gets more tightly bunched."), because the toolkit's writer only fires single-word triggers (FRICTIONAL.md, 2026-09-26). This was Prasad's decision on 2026-09-26. The narration itself is unchanged.
- **Pronunciation.** B00 and BOUT audio say "Namaste" and "Prasad" through a phoneme override (`tools/kokoro_phoneme_override.py`); the text and everything on screen are unchanged.
