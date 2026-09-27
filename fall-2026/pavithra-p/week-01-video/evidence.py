"""Every number in the video comes from this script.

It imports the course's Chapter 1 derivation script unchanged
(research/llm_scale.py) and writes evidence.json.

    python3 evidence.py

Two kinds of number come out, kept apart on purpose:
  - "script_output": exactly what llm_scale.py itself prints.
  - "extension": the 8-hours-a-day figures. llm_scale.py does not print these.
    They come from its own reading_years() function, scaled by 24 / 8.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "research"))
import llm_scale  # noqa: E402  (the course file, not a copy)

TOKENS = llm_scale.GPT3_TRAIN_TOKENS
WPT = llm_scale.WORDS_PER_TOKEN
RATES = [300, 250, 200, 150]
HOURS_PER_DAY = 8


def build():
    printed = llm_scale.result["reading_years_by_rate"]
    nonstop = {r: llm_scale.reading_years(TOKENS, WPT, r) for r in RATES}
    for r in RATES:
        assert round(nonstop[r], 1) == printed[str(r)], "must match the script's printed output"
    words = TOKENS * WPT
    return {
        "source": "research/llm_scale.py (cited figures: Brown et al. 2020, arXiv:2005.14165)",
        "script_output": {
            "gpt3_train_tokens": TOKENS,
            "words_per_token": WPT,
            "seconds_per_year": llm_scale.SECONDS_PER_YEAR,
            "reading_years_by_rate": printed,
        },
        "derived_steps": {
            "words": words,
            "minutes_at_250_wpm": words / 250,
        },
        "extension": {
            "note": "Not printed by llm_scale.py. reading_years() x (24 / 8) for 8 hours of reading per day.",
            "hours_per_day": HOURS_PER_DAY,
            "reading_years_by_rate": {str(r): round(nonstop[r] * 24 / HOURS_PER_DAY, 1) for r in RATES},
        },
    }


if __name__ == "__main__":
    data = build()
    (HERE / "evidence.json").write_text(json.dumps(data, indent=1))
    print(json.dumps(data, indent=2))
