# Three Scores Are Not Yet Three Chances

**Name:** Varnika M · INFO 7375 · Week 01 video

**Concept (Chapter 1, Part 2):** Three scores are not yet three chances. A model's scores only rank
its options; to become probabilities they must be made positive and scaled to add up to one, which
is what the lesson's `probabilities()` function does in two steps.

**Why this concept:** it is the basic step behind every next-token choice, and the lesson code prints
real numbers for it, so the whole explanation can be shown and checked rather than asserted.

**Runtime:** 2:15.8 (135.8 s, measured from the rendered file)

**Video:** `final/three-scores-not-three-chances.mp4` (1920×1080, 24 fps, H.264/AAC).
Play it in QuickTime, a browser, or VLC; VS Code's built-in preview plays it without sound.

## What the video shows

| Beat | Content |
|---|---|
| B00 | The question: scores 1, 2, 3 — what are the chances? Real `main.py` output, on a labelled reconstructed interface |
| B01 | Overview: scores rank; chances must be positive and add up to one |
| B02 | Scores 1, 2, 3 sum to 6, so they are not chances |
| B03 | Dividing by the total works for 1, 2, 3 but gives −0.25 for the constructed scores −1, 2, 3 |
| B04 | Step 1 in the real code: subtract the top score, apply `exp` → 0.135, 0.368, 1.000 |
| B05 | Step 2: divide by 1.503 → 0.090, 0.245, 0.665, exactly what `main.py` prints |
| B06 | The constructed −1, 2, 3 now gives 0.013, 0.265, 0.721 |
| B07 | **What this does not establish:** the conversion never checks which option is correct |
| B08 | Summary |
| B09 | A prompt for the viewer to try, then check against the code |
| B10 | Title and credits |

## Evidence

- `evidence/main_py_output.txt`: the real output of `lessons/01-randomness-and-first-prompts/code/main.py`
- `evidence/worked_steps.txt`: every intermediate number
- `FACTCHECK.md`: each claim in the video with its source
- `scenes.py` imports `main.py` to compute every number on screen and stops if they differ from the evidence

## How to rebuild

Full steps, including setup, are in `BUILD-PROMPT.md`. In short, with the Brutalist toolkit
(revision `6a8380ae`) installed and its virtual environment active:

```bash
cd <brutalist.art>
source .venv/bin/activate
python3 runtime/scripts/generate_audio_kokoro.py <this folder>
./art run <this folder>
./art final <this folder> --height 1080 --out <this folder>/final
```

This folder must stay at `fall-2026/varnika-m/week-01-video/` inside the course repository, because
`scenes.py` loads `main.py` by relative path.

## Other files

- `beat_sheet.json`: the narration and visual plan
- `BUILD-PROMPT.md`: prompts and commands that rebuild the video
- `SOURCES.md`: sources, what I made, what Claude contributed, licences, synthetic-voice disclosure
- `FRICTIONAL.md`: dated log of what I tried, what broke, and what I decided
- `SHOTLIST.md`, `PROMPTS.md`: work-order files the toolkit requires before rendering
