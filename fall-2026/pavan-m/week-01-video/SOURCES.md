# Sources

## What I made

- The concept choice (expected count vs. observed count) and the narration
  script for all 8 beats
- All beat-sheet decisions: what's shown per beat, where the real numbers
  appear, the boundary disclosure (B06), and the decision on how to handle
  the constructed-illustration disclosure (B05 -- see `beat_sheet.json`
  metadata for the reasoning)

## What came from real code

All numbers shown on screen (softmax probabilities, the 665.24 expected
count, the 630/671/640 observed counts for seeds 7/42/99) are the actual
printed output of `lessons/01-randomness-and-first-prompts/code/main.py`
from the Brutalist toolkit, not invented or estimated.

## What Claude contributed

Claude (Anthropic) was used throughout this assignment, via chat, for:

- Iterating on the Manim scene code in `scenes.py` (all 10 scene classes)
- Debugging rendering issues (frozen-frame gaps between video and narration
  length, text/background color contrast, an out-of-frame brace/label, a
  bracket spanning the wrong bars, and a word-highlight indexing bug --
  see `FRICTIONAL.md` for the full list)
- Writing the ffmpeg commands used to pair video with narration, recombine
  split scenes, and concatenate the final video
- Drafting this file, `README.md`, and `BUILD-PROMPT.md`

Claude did not choose the concept, write the narration script, generate the
real numbers (those came from running `main.py` myself), or make the
grading-relevant judgment calls (e.g., the boundary statement's wording, or
the decision not to add a separate on-screen "illustrative" label to the
coin-flip analogy).

## Third-party assets

- **Brutalist toolkit** (Manim/Kokoro pipeline): https://github.com/nikbearbrown/brutalist.art
- **Kokoro** (local, free TTS): narration voice `af_bella`
- **Manim Community** (v0.21.0): all on-screen animation
- No paid APIs, no external media accounts, no third-party images, fonts,
  or audio beyond the above were used.
