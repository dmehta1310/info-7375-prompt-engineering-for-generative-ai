# SOURCES

**Riya Kapadnis** · INFO 7375 Week 1 Explainer Video · compiled 2026-09-26

## What I used

| Source | Role | Licence / terms |
|---|---|---|
| `lessons/01-randomness-and-first-prompts/code/main.py` (this repo) | The subject. Imported unmodified by my scripts; `probabilities()` and `sample()` produce every figure in the reel. | MIT (course repo `LICENSE`) |
| `lessons/01-randomness-and-first-prompts/docs/en.md` (this repo) | Read to confirm the concept is in scope. Contains **none** of the numbers used — see note below. | MIT (course repo) |
| [brutalist.art](https://github.com/nikbearbrown/brutalist.art) @ `6a8380ae169cca81e0633664a65c958f5c12ab4b` | Toolkit. Supplied the `beat_sheet.json` schema my plan validates against, the audio-as-master-clock discipline, and the Kokoro voice model. | Per repo |
| Kokoro-82M (`kokoro-v1.0.onnx`, `voices-v1.0.bin`), voice `af_bella` | All narration. Local inference, no account, no key. | Apache-2.0 (Kokoro-82M) |
| Manim Community v0.18.1 | All seven scenes. | MIT |
| FFmpeg 9.0.2 | Sync, concatenation, contact sheet. | LGPL/GPL |
| Python 3.11.14 (Homebrew) | Runtime. Manim 0.18 does not support 3.13. | PSF |

**Fonts:** Menlo and Helvetica Neue — macOS system faces, used through Manim's `Text`.
No font files are redistributed in this folder.

**Third-party media:** none. No stock footage, images, music, or archival assets. Every
frame is drawn by `scenes.py` from `video_data.json`.

**Paid services:** none. No API keys, no generation credits, no media accounts. Total
cost $0.00.

## What I made

- `evidence/expected_vs_observed.py` — the analysis: binomial SD, exact tail via
  log-gamma, the 10,000-seed sweep, and the biased-sampler comparison.
- `evidence/build_data.py` → `video_data.json` — recomputes every on-screen figure so
  that no number is hand-typed into the scenes.
- `scenes.py` — seven Manim scenes.
- `make_audio.py`, `assemble.py` — narration synthesis and audio-led assembly.
- `beat_sheet.json` — the narration and visual plan.
- Narration script — the spoken text in `beat_sheet.json`, reviewed line by line
  against `evidence/expected_vs_observed_output.txt` before synthesis.

## What Claude contributed

Claude Opus 5, via Claude Code, across sessions on 2026-09-23 and 2026-09-26. Substantial
and worth stating precisely:

**Wrote, with my direction and review:** `expected_vs_observed.py`, `build_data.py`,
`scenes.py`, `make_audio.py`, `assemble.py`, the beat sheet, and the first drafts of this
file and `README.md`.

**Specific things I asked for that changed the result:**

- The 10,000-seed empirical sweep in B04. The first draft established the spread from the
  binomial formula alone. I asked for the measured version, because a video that quotes a
  formula asserts the spread rather than showing it — and showing it is what the rubric
  scores. The measured mean (665.234) landing on the predicted (665.24) became the beat.
- The concept switch itself. Claude surveyed the eleven `week-01-video` folders already
  pushed, found two students on max-subtraction, read `atharva-h`'s verify log, and
  recommended moving. I made the call to drop three days of finished work; the reasoning
  is in FRICTIONAL.md.

**What Claude caught that I would have shipped wrong:** two AI-written plans I brought to
the session both asserted that the numbers "come from the chapter." Claude grepped
`docs/en.md` — 106 lines, zero hits for `0.6652`, `1000`, `0.5, 0.5`, `cancel`, and six
other patterns — and showed the chapter has exactly one line on the mechanism and none of
the figures. Had I not checked, this file would have carried a false provenance claim.
The numbers come from executing `main.py`, and that is what is cited.

**What I corrected in Claude's work:** the first render held a frozen frame for 17 seconds
in two beats because the animations were much shorter than the narration; I had the scenes
repaced rather than padded. Three label collisions (B02's highlight box landing
mid-number, B03's mean label over the formula, B06's closing card printed on top of the
curves) were found by inspecting rendered frames and fixed.

**What I verified myself:** every figure in the video against
`evidence/expected_vs_observed_output.txt`; the runtime with `ffprobe`; that
`docs/en.md` does not contain the numbers; and the rendered frames in `qc-sheet.png`.

## A note on provenance

Chapter 1's subject is the difference between a fluent output and a supported claim, so
it matters where these numbers came from. They came from running
`lessons/01-randomness-and-first-prompts/code/main.py` on this machine on 2026-09-23 and
again on 2026-09-26, both times producing
`{"1": 268, "2": 630, "0": 102}`. They are not quoted from the chapter prose, which does
not contain them. No Claude conversation is reproduced in the video, so no transcript
required a date stamp. The video itself carries no credits card — attribution lives in
this file, which is the graded deliverable.
