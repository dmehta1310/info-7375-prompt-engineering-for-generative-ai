# Shift the Scores, Keep the Chances

**Student:** Siddhesh Nikam

**Course:** INFO 7375 — Prompt Engineering for Generative AI

**Assignment:** Week 1 Explainer Video — Explain One Concept from Chapter 1

**Concept:** Why subtracting the maximum changes softmax intermediates but not the distribution

**Why this concept:** It is one small mechanism that can be explained completely with the course program's actual output, the lesson's official large-score test, one algebraic cancellation, and one explicit limitation.

**Runtime:** 3 minutes 12.8 seconds (inside the 2–4 minute target).

**Narration:** Synthetic Kokoro `af_bella`, generated locally at speed `0.94`; not the student or instructor's voice.

## What the video shows

1. The course reference program's actual probabilities for `[1, 2, 3]`.
2. The shift `[1, 2, 3] − 3 → [−2, −1, 0]`.
3. The published weights `0.135335`, `0.367879`, and `1`, with total `1.503215`.
4. The official course test `[1000, 1000] → [0.5, 0.5]`.
5. The shared `exp(−m)` factor cancelling algebraically.
6. The boundary: overflow protection does not establish truth, calibration, or universal safety for every extreme input.

## Rebuild

Requirements: Python 3, Pillow, FFmpeg, and the included reviewed narration under `mp3/`.

```bash
python3 code/softmax_demo.py
python3 build_video.py
```

The renderer writes:

- `Nikam_Siddhesh_INFO7375_Week01_Video.mp4`
- `Nikam_Siddhesh_INFO7375_Week01_Video.srt`
- `build/timeline.json`

To regenerate narration instead of using the included audio, follow `BUILD-PROMPT.md`.

## Evidence

- `code/course_main_output.txt` preserves the actual output from the unmodified Chapter 1 `main.py` run on 2026-09-26.
- `code/softmax_demo.py` reproduces every intermediate number displayed in the video using Python's standard library.
- `code/softmax_output.txt` preserves that script's output.
- `FACTCHECK.md` maps each important claim to its evidence.
- `REVIEW.md` records the revision from the first working cut to the submitted cut.

## Submission structure

The GitHub destination is:

`fall-2026/siddhesh-n/week-01-video/`

The Canvas ZIP contains this same folder and the rendered MP4. No credentials, private conversations, caches, or paid media are included.
