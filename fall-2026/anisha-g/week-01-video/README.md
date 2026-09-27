# Same Seed, Same Run — Not the Same as Truth

**Student:** Anisha Gaikar

**Course:** INFO 7375 — Prompt Engineering for Generative AI

**Assignment:** Week 1 Explainer Video — Explain One Concept from Chapter 1

**Concept:** A seed makes a run repeatable; it does not make the answer true.

**Why this concept:** It is one small Chapter 1 mechanism that can be shown completely with the course sampler's actual seed-7 output, a controlled seed-8 comparison, the official repeatability test, and one clear limitation.

**Runtime:** 3 minutes 13.0 seconds (inside the 2–4 minute target).

**Narration:** Synthetic Kokoro `af_bella`, generated locally at speed `0.94`; it is not the student or instructor's voice.

## What the video shows

1. Where `seed` enters the course `sample()` function.
2. The unmodified program's actual seed-7 counts: `{0: 102, 1: 268, 2: 630}`.
3. A second seed-7 run producing exactly the same counts.
4. A controlled seed-8 run producing `{0: 76, 1: 239, 2: 685}` while logits, count, temperature, and probabilities stay fixed.
5. What the official Chapter 1 repeatability test establishes.
6. The boundary: the sampler has no source, answer key, or verifier, so reproducibility does not establish truth.

## Rebuild

Requirements: Python 3, Pillow, FFmpeg, and the included reviewed narration under `mp3/`.

```bash
python3 code/seed_demo.py
python3 code/test_seed_demo.py
python3 build_video.py
```

The renderer writes:

- `Anisha_Gaikar_INFO7375_Week01_Video.mp4`
- `Anisha_Gaikar_INFO7375_Week01_Video.srt`
- `build/timeline.json`

To regenerate narration instead of using the included audio, follow `BUILD-PROMPT.md`.

## Evidence

- `code/course_main_output.txt` preserves output from the unmodified Chapter 1 `main.py` run on 2026-09-26.
- `code/seed_demo.py` reproduces the course function and both seed comparisons with Python's standard library.
- `code/seed_output.txt` preserves that script's output.
- `FACTCHECK.md` maps the video's important claims to evidence.
- `DEFENSE-NOTES.md` is a short study guide for explaining the submission.

## Submission structure

The GitHub destination is:

`fall-2026/anisha-g/week-01-video/`

The Canvas ZIP contains this same folder and rendered MP4. No credentials, private conversations, caches, or paid media are included.
