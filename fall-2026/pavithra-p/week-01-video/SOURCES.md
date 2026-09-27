# SOURCES — Thousands of Years, Divided

## What I used (not made by me)

| Item | What it is | Licence / terms |
|---|---|---|
| Chapter 1, "Scale, in units you can check" | The concept and the reading-time comparison | Course repository, MIT licence (`LICENSE`) |
| `research/llm_scale.py` | The course's derivation script. Imported unchanged; produces every script-output number in the video. | Course repository, MIT licence |
| Brown et al. 2020, *Language Models are Few-Shot Learners*, arXiv:2005.14165 | Origin of the ~300 billion training-token figure, as cited by `llm_scale.py`. I did not re-read the paper to confirm it; it is labelled REPORTED on screen. | Cited, not reproduced |
| Brutalist toolkit (`github.com/nikbearbrown/brutalist.art`) | Audio-first pipeline: `generate_audio_kokoro.py`, `./art run`, `./art final`, QC gates | Used from an external checkout; nothing from it is copied into this folder |
| Kokoro-82M voice model, voice `af_bella` (via `kokoro-onnx`) | Synthetic narration voice, run locally | Kokoro-82M is released under Apache-2.0 |
| Manim Community v0.18.1 | Animation engine | MIT |
| FFmpeg 9.0.2 | Audio/video assembly | LGPL/GPL |
| Helvetica Neue | On-screen font, the macOS system font | System font; used for rendering only, not redistributed |

No stock footage, images, music, or third-party video clips are used.

## What was made for this video

- `beat_sheet.json`: the narration and visual plan.
- `scenes.py`: the eight Manim scenes.
- `evidence.py` / `evidence.json`: pulls every number from the course script and checks it.
- `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`, `FRICTIONAL.md`, `BUILD-PROMPT.md`, this file.
- The "unbelievable → un / believ / able" token split in B01 is a **constructed illustration**, not a real tokenizer's output. It is labelled on screen.
- The 8-hours-a-day figures in B05 are a **calculated extension** (`reading_years() × 24/8`), not output printed by the course script. They are labelled on screen.

## What Claude contributed

This video was built with Claude Code (Claude Opus 5.5) in a session I directed.

- **Claude did:** set up the toolchain; ran the course scripts; suggested the candidate concepts and compared them against the rubric; proposed the "8 hours a day" extension; drafted the beat sheet and narration; wrote `scenes.py`, `evidence.py` and the paperwork drafts; ran the Brutalist build.
- **I did:** chose the concept (switching from a Part 2 topic to this Part 1 topic because I understood it better); reviewed the narration and required two accuracy corrections before approving it (B00: "an estimate produced by division"; B06: "translates a reported training-token count into hypothetical human reading time"); accepted or adjusted wording changes in B01, B02, B04, B05 and B06; decided to skip a Claude-UI opening; watched the rendered drafts and spotted the uneven letter spacing that no automated check caught; asked for the final fix round (spacing, slider direction, name on the title card) and declared that version final.
- **No Claude output appears in the video.** There is no Claude screen or transcript, real or constructed.
- The private Claude Code conversation is not included in this submission.
