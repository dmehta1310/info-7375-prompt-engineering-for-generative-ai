# SOURCES — Week 1 Explainer Video

Ashwin Thankachan · INFO 7375 · "[1000, 1000] → [0.5, 0.5], and what the shared offset never carried"

## What I made / decided

- Chose the concept (from the professor's Chapter 1, Part 2 list) and why.
- Wrote the narration script in the build brief (five beats) and approved the edits listed below.
- Wrote `offset_evidence.py` (in the build brief).
- Reviewed every beat, the fact-check and the rendered frames; approved or rejected each change.
- Watched draft 1 and identified the revision: softmax was never defined, and the start and end felt abrupt. Chose a single consistent palette (draft 4).
- Re-ran `main.py` myself (2026-09-26); the printed probabilities matched `reference-output.txt`.
- `FRICTIONAL.md` is my own log.

## What Claude (Claude Code, Anthropic — model Claude Opus 5.5) contributed

Claude contributed to the build; it does not appear in the video. No Claude response is shown or quoted on screen.

- Read the Brutalist toolkit and found where it differed from my brief. Installed ffmpeg (Homebrew, with my approval), set up the Python venv, Remotion `npm install`, and the Kokoro model.
- Ran `main.py` and `offset_evidence.py` to produce the evidence files and cross-checked them under two Python versions.
- Proposed and wrote `intermediates_evidence.py`, which prints the post-max-subtraction values and runs the 0–1000 offset sweep.
- Proposed three narration edits, which I approved: Beat 1 "percentages" → "probabilities"; Beat 3 "here's why" rewritten so the cancellation is attributed to the common factor, and max-subtraction only to bitwise identity; and the beats split into sub-beats with unchanged wording.
- Wrote the Remotion component `SoftmaxOffset.tsx`, `tools/build_beat_sheet.py`, `tools/sync_cues.py`, `tools/verify_numbers.py`, `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`, and drafts of this file, `README.md` and `BUILD-PROMPT.md`.
- Drafted the revision wording (B00 question, B01B softmax sentence, B06 recap) from my notes, which I approved; fixed the Gate V underfill defects (drafts 1–2).
- Ran the audio and render commands and did the visual QC passes; fixed the Gate T typography failures (accent contrast, label size, title-safe margins) before the final render.

## Evidence (all on-screen numbers)

| File | Produced by | Notes |
|---|---|---|
| `reference-output.txt` | `lessons/01-randomness-and-first-prompts/code/main.py`, course repo commit `e6c6c49dd8b65d7f81dd8e72b89fd6c1f6b23738` | run under Python 3.13.7; byte-identical under 3.9.6 |
| `offset-output.txt` | `offset_evidence.py` | same cross-check |
| `intermediates-output.txt` | `intermediates_evidence.py` | same cross-check |

## Tools and third-party assets

| Item | Version / commit | Licence | Use |
|---|---|---|---|
| Brutalist toolkit (`nikbearbrown/brutalist.art`) | commit `6a8380ae169cca81e0633664a65c958f5c12ab4b` | no LICENSE file in the repository at this commit | pipeline, gates, compile |
| **Kokoro-82M, voice `af_bella`** — **synthetic voice** (text-to-speech, not my voice or any real person's recording) | model files `kokoro-v1.0.onnx`, `voices-v1.0.bin` from `thewh1teagle/kokoro-onnx` release `model-files-v1.0` | Apache-2.0 (Kokoro-82M) | all narration |
| kokoro-onnx (Python) | 0.6.1 | not declared in package metadata — see github.com/thewh1teagle/kokoro-onnx | runs Kokoro locally |
| onnxruntime | 1.30.0 | MIT | Kokoro inference |
| Remotion | 4.0.486 | Remotion License — free tier (individuals) | renders every visual |
| FFmpeg | 9.0.2 (Homebrew) | LGPL/GPL | audio encode, measuring, compile |
| Fonts | macOS system fonts (Georgia, SF Pro, SF Mono/Menlo) chosen by headless Chrome from the toolkit's font stack | Apple system fonts | on-screen text |

No stock footage, images, music, AI-generated video/images, or paid services were used. Cost: $0.00.
