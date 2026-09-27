# BUILD-PROMPT

How this video was built, in the order it happened. Every command below was actually run
on macOS 14 (Darwin 23.6.0, Apple Silicon).

## Environment

| Component | Version | Note |
|---|---|---|
| Python | 3.11.14 (Homebrew) | **Not 3.13.** Manim 0.18 requires `<3.13`; see FRICTIONAL.md |
| Manim Community | 0.18.1 | No LaTeX installed — scenes use `Text`, never `MathTex` |
| Kokoro | kokoro-onnx 0.6.1, model `v1.0`, voice `af_bella` | Local, free |
| FFmpeg / ffprobe | 9.0.2 | `brew install pkg-config ffmpeg` |
| brutalist.art | `6a8380ae169cca81e0633664a65c958f5c12ab4b` | Schema + doctrine + voice model |

```bash
brew install pkg-config ffmpeg          # pkg-config is required for pycairo -> manim
git clone https://github.com/nikbearbrown/brutalist.art
cd brutalist.art
/opt/homebrew/bin/python3.11 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
# Kokoro model (~340MB), as ./setup --install would fetch:
mkdir -p runtime/models/kokoro && cd runtime/models/kokoro
curl -fLO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -fLO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```

## Stage 1 — evidence before script

No narration was written until the numbers existed.

```bash
python3 lessons/01-randomness-and-first-prompts/code/main.py
python3 evidence/expected_vs_observed.py | tee evidence/expected_vs_observed_output.txt
python3 evidence/build_data.py                     # -> video_data.json
```

**Prompt used:**

> Write an evidence script for the concept "expected count 665.24 versus observed count
> 630". Import the lesson's `main.py` unmodified — do not reimplement it. Compute the
> binomial standard deviation and the z-score for the observed count, the exact tail
> probability in log space, and then **do not stop at the formula**: run the same sampler
> across seeds 0–9999 and report the empirical mean, SD, percentiles, and where 630 ranks.
> Finally, compute how readily a sampler biased to `observed/n` would produce the same
> count, because that is the boundary the video has to state. Print everything; invent
> nothing.

The 10,000-seed sweep was requested specifically. A video that quotes a formula asserts
the spread; one that measures it shows the spread, and showing it is the graded criterion.

## Stage 2 — beat sheet

```bash
python3 -c "import json; json.load(open('beat_sheet.json'))"   # validated against
# brutalist.art/runtime/schema/beat_sheet.schema.json (beat_id pattern, shot.type/source enums)
```

**Prompt used:**

> Write `beat_sheet.json` for a 2–4 minute explainer on one concept. Seven beats, one idea,
> no chapter tour. Every number in the narration must appear in
> `evidence/expected_vs_observed_output.txt` — quote nothing that is not in that file. One
> beat must state what the explanation does not establish, phrased as a limit on my own
> claim rather than a general disclaimer. Match the shot/graphic fields to
> `runtime/schema/beat_sheet.schema.json`.

## Stage 3 — narration (audio is the master clock)

```bash
python make_audio.py        # -> audio/B0*.wav + audio/timings.json
```

Measured: B00 25.41s · B01 16.02s · B02 22.42s · B03 25.90s · B04 32.40s · B05 24.04s ·
B06 36.99s · B07 30.39s — **total 213.57s**. These measurements, not the estimates in the beat sheet,
drive the edit.

## Stage 4 — scenes

```bash
for S in B00_Title B01_TheGap B02_TwoKinds B03_HowBigIsANormalMiss B04_TenThousandSeeds \
         B05_WhereSeedSevenLands B06_WhatThisDoesNotEstablish B07_Conclusion; do
  python -m manim -qh --disable_caching --media_dir render -o "$S" scenes.py "$S"
done
```

**Prompt used:**

> Write seven Manim scenes, one per beat. Read every figure from `video_data.json` — do not
> type any number into the scene file, so the frames change if the data changes. No
> `MathTex` or `Tex` anywhere: there is no LaTeX install, and `include_numbers=True` on
> `NumberLine`/`Axes` routes through MathTex, so draw tick labels as `Text`.

## Stage 5 — assembly

```bash
python assemble.py          # -> riya-k-expected-is-not-a-promise.mp4
```

Per beat: `ffprobe` the rendered scene, compare against the measured narration, then pad
with `tpad=stop_mode=clone` or trim with `-t`, encode at CRF 18, and concatenate.

## Stage 6 — visual QC, and what it caught

```bash
ffmpeg -ss <t> -i riya-k-expected-is-not-a-promise.mp4 -frames:v 1 frame.png   # -> qc-sheet.png
```

Inspecting rendered frames — not the logs — found four defects that a green build would
have hidden:

1. **17-second frozen frames in B04 and B06.** Animations were far shorter than their
   narration, so `tpad` held a still for half the beat. Fixed by repacing the scenes
   (histogram build 4s → 11s, curve draws 1.8s → 4.0s), not by padding.
2. **B02** — the highlight box landed mid-number; replaced `Circle` with
   `SurroundingRectangle` around the actual fractional tail.
3. **B03** — the mean label collided with the SD formula; the formula now parks in the
   top-left corner and the title fades.
4. **B06** — the closing card printed on top of the two curves; the chart now dims to 10%
   and the card centres.

A second review round, after watching the cut, found three more:

5. **B05** — the observed marker, its label and the `p1 = 631` gridline all collided with
   the "0.89th percentile" text. 630 and 631 are one apart and cannot share a horizontal
   band, so the observed label moved below the axis and the p1 gridline was shortened.
6. **B06** — `biased sampler p = 0.6300` was anchored off the left edge of the frame and
   rendered as "pler p = 0.6300". Both curve labels became a legend pinned inside the frame.
7. **Structure** — the reel opened straight into the problem with no title, and closed on
   a credits card. Added `B00_Title` (name, course, and the question the reel answers) and
   replaced the credits with `B07_Conclusion`. Runtime went 2:48 → 3:34.

## Reproduce

```bash
python3 evidence/build_data.py && python make_audio.py && \
for S in B00_Title B01_TheGap B02_TwoKinds B03_HowBigIsANormalMiss B04_TenThousandSeeds \
         B05_WhereSeedSevenLands B06_WhatThisDoesNotEstablish B07_Conclusion; do
  python -m manim -qh --disable_caching --media_dir render -o "$S" scenes.py "$S"; done && \
python assemble.py
```

Deterministic: seeds 0–9999 via `random.Random(seed)`, and the lesson's own `seed=7`.
Re-running reproduces every figure exactly.
