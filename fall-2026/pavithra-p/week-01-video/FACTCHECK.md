# FACTCHECK — Thousands of Years, Divided

Every on-screen or spoken claim, what backs it, and how far it was checked.
"Reproduced" = re-run on 2026-09-23 with `python3 evidence.py`, which imports the course's `research/llm_scale.py` unchanged.

| Beat | Claim | Verdict | Source / how checked |
|---|---|---|---|
| B00 | The slogan "a human would need thousands of years to read GPT-3's training text" circulates | Paraphrase, labelled on screen | Chapter 1, "Scale, in units you can check" quotes this reading comparison. Not attributed to any one speaker. |
| B00 | The reading time is an estimate produced by division | Correct | `llm_scale.reading_years()` is `tokens × words_per_token ÷ wpm`, converted to years |
| B01 | GPT-3 was trained on approximately 300 billion tokens | **Reported, not re-measured** | Brown et al. 2020, arXiv:2005.14165, as cited in `llm_scale.py` (`GPT3_TRAIN_TOKENS`) and in the chapter. We did not re-read the paper to confirm; it is labelled "REPORTED" on screen. |
| B01 | "unbelievable" → un / believ / able | **Constructed illustration** | Made up for this video, not a real tokenizer's output. Labelled on screen. |
| B02 | 0.75 words per token is an approximation | Correct | `llm_scale.py`: "Stated convention for English, not a measurement." |
| B02 | 300,000,000,000 × 0.75 = 225,000,000,000 words | Reproduced | `evidence.json → derived_steps.words` |
| B03 | 225,000,000,000 ÷ 250 = 900,000,000 minutes | Reproduced | `evidence.json → derived_steps.minutes_at_250_wpm` |
| B03 | 525,960 minutes per year (365.25-day year) | Correct | `SECONDS_PER_YEAR = 31,557,600` in `llm_scale.py`; ÷ 60 = 525,960 |
| B03 | ≈ 1,711.2 years at 250 wpm | Reproduced | script output `reading_years_by_rate["250"]` |
| B04 | 1,426.0 / 2,138.9 / 2,851.9 years at 300 / 200 / 150 wpm | Reproduced | script output `reading_years_by_rate` |
| B04 | The slowest answer is twice the fastest | Correct | 150 wpm is half of 300 wpm, and years ∝ 1/wpm. Rounded values: 2,851.9 vs 2 × 1,426.0 = 2,852.0 (0.1 rounding gap). |
| B05 | The formula assumes 24 hours/day of reading | Correct | `reading_years()` converts minutes straight to years with no hours-per-day term |
| B05 | At 8 hours/day every answer triples: 1,711.2 → 5,133.5 | **Calculated extension**, labelled on screen | `evidence.json → extension`: `reading_years() × 24/8`. Not printed by `llm_scale.py`. |
| B05 | In-between values while the clock moves (e.g. 12 h → 3,422.3 years at 250 wpm) | Correct: same formula | `years_at(wpm) × 24 / hours` in `scenes.py`; same function as the extension. Shown only during the transition. |
| B06 | Every version is far more than one lifetime | Correct | Smallest figure shown is 1,426.0 years |
| B06 | The calculation does not show understanding, accuracy, or that the tokens were unique | Correct (a limit, not a finding) | Nothing in the inputs of `reading_years()` concerns any of these |

Rounding in narration: "about five thousand, one hundred and thirty-four" is 5,133.5 rounded. The screen shows 5,133.5.
