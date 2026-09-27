# 665.24 Is Not a Promise

**Riya Kapadnis** · `kapadnis.ri@northeastern.edu`
INFO 7375 — Prompt Engineering for Generative AI · Week 01 · Chapter 1, Part 2

| | |
|---|---|
| **Concept** | Expected count (**665.24**) versus observed count (**630**) |
| **Why it matters** | An expected count is a rate times a number of draws. It is not a prediction that any single run will produce it — and one run cannot tell you whether a gap means bad luck or a broken sampler. |
| **Runtime** | **3:33.7** (213.7 s) · 1920×1080 · 30 fps · 8 beats |
| **Deliverable** | `riya-k-expected-is-not-a-promise.mp4` — **submitted via Canvas, not in this folder** (see note below) |
| **Source** | `lessons/01-randomness-and-first-prompts/code/main.py`, run on 2026-09-23 and 2026-09-26 |
| **Cost** | $0.00 — Kokoro TTS, Manim and ffmpeg, all local. No API key, no paid call, no account. |

> **Where is the video?** The repository's root `.gitignore` excludes `*.[mM][pP]4` at any
> depth ("Keep generated audio/video out of Git"), and `prerequisites/github-submission.md`
> states *"A video is not required"* for the GitHub posting. The file is on Canvas.
> Everything needed to rebuild it bit-for-bit is here. Logged in `FRICTIONAL.md`.

---

## What the video does

Chapter 1 tells you to compare expected counts with observed counts. It publishes
**no numbers** for that comparison — `docs/en.md` is 106 lines and contains none of the
figures below. Run the chapter's own code and it predicts token 2 appears **665.24**
times in 1000 draws, then prints **630**.

The video asks whether that 35-count gap means the code is broken, and answers it by
measurement rather than by formula.

| Beat | Act | What happens on screen |
|---|---|---|
| B00 | open | Title, name, course; the setup in three lines; the question the reel answers |
| B01 | the problem | Verbatim `main.py` output — expected `665.24`, observed `630`, gap `−35.24` |
| B02 | define | `0.6652409557748218 × 1000` written out; you cannot draw a fraction of a token |
| B03 | **mechanism** | `sd = sqrt(n·p·(1−p))` fills in term by term → **14.92**; 630 lands outside the ±2 SD band at **z = −2.36** |
| B04 | **evidence** | 10,000 seeds run; the histogram builds; measured mean **665.234** settles onto the predicted **665.24**, measured SD 14.71 vs 14.92 |
| B05 | the turn | **89 of 10,000** seeds at or below 630 — the **0.89th percentile**, below p1 = 631 |
| B06 | **boundary** | A sampler biased to p = 0.63 produces 630 with probability 0.026 — **15.5× more readily** than the fair sampler's 0.0017 |
| B07 | close | Not a bug · the sampler is fair · seed 7 is unusual — then the closing claim |

### The four rubric constraints

1. **Show the mechanism, don't assert it.** The standard deviation fills in term by term,
   the histogram assembles from 10,000 real runs, and both distributions draw on screen.
   No beat is a slide with a voice over it.
2. **Numbers real and reproducible.** Every figure comes from
   `evidence/expected_vs_observed.py`, and `evidence/build_data.py` caches them into
   `video_data.json`, which the scenes read. **No number is typed into `scenes.py`.**
3. **Constructed illustrations labelled.** There are none — every frame is measured
   output, so nothing required a `CONSTRUCTED` stamp.
4. **Name the boundary.** B06 states it on screen and reads it aloud:

   > Shown: 630 is consistent with a fair sampler.
   > **Not shown: that a fair sampler is the only thing that could have produced it.**

---

## Verify

```bash
python3 evidence/expected_vs_observed.py
```

Re-derives every figure in the video from the chapter's own `main.py`, which it imports
unmodified: the binomial SD and z-score, the exact tail `P(≤630) = 1.04%` computed in log
space, the 10,000-seed sweep with its percentile ladder, and the biased-sampler
comparison. Deterministic — seeds 0–9999 via `random.Random(seed)`, plus the lesson's own
`seed=7`, so re-runs reproduce every number exactly.

Saved output for comparison: `evidence/expected_vs_observed_output.txt`.

## Rebuild

Requires Python **3.11** (Manim 0.18 does not support 3.13), FFmpeg, and `pkg-config`.

```bash
python3 evidence/build_data.py        # 1. recompute every figure -> video_data.json
python  make_audio.py                 # 2. Kokoro narration -> audio/ + timings.json

for S in B00_Title B01_TheGap B02_TwoKinds B03_HowBigIsANormalMiss \
         B04_TenThousandSeeds B05_WhereSeedSevenLands \
         B06_WhatThisDoesNotEstablish B07_Conclusion; do
  python -m manim -qh --disable_caching --media_dir render -o "$S" scenes.py "$S"
done                                  # 3. the eight scenes at 1080p60

python  assemble.py                   # 4. sync to narration, concatenate -> .mp4
```

`assemble.py` treats narration as the master clock: each scene is padded (last frame held)
or trimmed to its measured audio length, and prints the per-beat table it used. Full
command log, environment versions, and the seven defects visual QC caught are in
`BUILD-PROMPT.md`.

---

## Package contents

```
README.md                             this file
FRICTIONAL.md                         process log, 5 dated entries (graded separately)
SOURCES.md                            attributions, human/AI split, licences
BUILD-PROMPT.md                       exact prompts + commands to rebuild end to end

beat_sheet.json                       8 beats: narration, timing, visual plan
scenes.py                             the 8 Manim scenes; reads video_data.json
make_audio.py                         Kokoro narration + duration measurement
assemble.py                           audio-led sync and concatenation
video_data.json                       every on-screen figure, computed

evidence/expected_vs_observed.py      the analysis — re-derives every number
evidence/expected_vs_observed_output.txt   its saved run
evidence/build_data.py                analysis -> video_data.json
evidence/shift_invariance.py          superseded work on a dropped concept, kept
evidence/shift_invariance_output.txt       because FRICTIONAL.md refers to it

audio/timings.json                    measured narration: 213.57 s across 8 beats
qc-sheet.png                          contact sheet used for visual review
```

The video itself is on Canvas — see the note at the top.
