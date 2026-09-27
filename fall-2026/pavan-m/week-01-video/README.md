# Expected Count vs. Observed Count

**Student:** Pavan Jayant Majji
**Course:** INFO7375 -- Prompt Engineering for Generative AI
**Assignment:** Week 01 Video -- Chapter 1 Concept Explainer
**Runtime:** 2:09

## Concept

Expected count vs. observed count: why running softmax's predicted probability
(665.24 expected occurrences of "blue" out of 1000 draws) against a real seeded
sample (630 observed) does not mean the model, or the math, is wrong.

## Why this concept

I picked this because it has a clean, concrete before/after number pulled
straight from real code output (`main.py`'s softmax probabilities and seeded
sampling), which let me show the mechanism moving on screen rather than just
asserting a claim -- and it has a clear, statable boundary (one seeded run
tells you nothing about how much deviation is normal).

## Files

- `week01_expected_vs_observed.mp4` -- the final rendered video (in `final/`)
- `scenes.py` -- all Manim scene definitions
- `beat_sheet.json` -- the reviewed narration + visual plan, beat by beat
- `BUILD-PROMPT.md` -- exact commands used to rebuild the video from this folder
- `SOURCES.md` -- what was made, what Claude contributed, third-party credits
- `FRICTIONAL.md` -- dated log of what broke during the build and how it was resolved

## How to rebuild

Full command-by-command rebuild instructions are in `BUILD-PROMPT.md`. In short:

1. Render all Manim scenes from `scenes.py` (`manim -pql scenes.py <SceneName> ...`)
2. Recombine the coin-flip and comparison-bars scenes into one clip (`Beat05Combined.mp4`)
3. Give the silent intro clip a matching silent audio track
4. Pair each scene's rendered clip with its Kokoro narration in `mp3/`, padding or trimming to match durations
5. Concatenate all 9 clips (intro + 8 narrated beats) into the final video

Narration audio in `mp3/` is pre-generated via Kokoro (`af_bella` voice) and
does not need to be regenerated unless the beat text changes.
