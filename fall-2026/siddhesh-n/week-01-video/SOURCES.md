# Sources and Contributions

## Course sources

- Nik Bear Brown, **INFO 7375: Randomness and first prompts**, section “The subtraction that changes nothing important”: <https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/chapters/01-randomness-and-first-prompts.md>
- Course reference implementation: `lessons/01-randomness-and-first-prompts/code/main.py` in the same repository.
- Course reference tests: `lessons/01-randomness-and-first-prompts/code/tests/test_main.py`; specifically, `test_02` checks `[1000, 1000] → [0.5, 0.5]`.
- Course figure used only as a style reference: `images/01-randomness-and-first-prompts-fig-01.png`. No pixels or diagram contents were copied into the video. The original graphics use the same course-oriented visual language: white ground, serif title, outlined process boxes, gray supporting text, red emphasis, and a gold footer rule.
- All were inspected and the reference program was run on 2026-09-26. The exact inspected repository revision is recorded in `FACTCHECK.md`.

## Toolkit and narration

- Nik Bear Brown, **Brutalist (Film as Code)**: <https://github.com/nikbearbrown/brutalist.art>
- The project follows Brutalist's beat-sheet and audio-first workflow. The public setup check issue and manual recovery are documented in `FRICTIONAL.md`.
- **Kokoro-82M / Kokoro v1.0**, rendered locally through `kokoro-onnx`; model licence: Apache-2.0 as documented by Brutalist. Voice: `af_bella`, speed `0.94`. Wrapper: <https://github.com/thewh1teagle/kokoro-onnx>.
- **DejaVu Serif, Sans, and Sans Mono**, rasterized into original frames. Licence: DejaVu/Bitstream Vera permissive licence: <https://dejavu-fonts.github.io/License.html>.

## What was made for this submission

- All motion graphics, layouts, animations, arrows, boxes, bars, equations, captions, and the course-aligned visual system.
- The reviewed narration and `beat_sheet.json`.
- The reproducibility script, captured outputs, renderer, SRT caption generator, fact-check, review record, and documentation.
- No third-party images, music, stock footage, Claude transcript, or fabricated model response appears in the video.

## AI contribution

- **Claude contribution: none.** No Claude transcript or response is represented in the submission.
- OpenAI Codex inspected the supplied assignment and screenshot, cloned and read the public course and Brutalist repositories, ran the course reference program, drafted and revised the narration, wrote the evidence and rendering code, generated the local synthetic narration, rendered the MP4, and organized the documentation.
- Siddhesh Nikam selected the goal, requested the rapid first build, rejected the first voice and visual treatment as too hard/generic, supplied the professor's example, requested another requirements audit, and remains responsible for watching and explaining the final submission.

## Claim boundary

The video supports this claim: subtracting the shared maximum keeps the intended normalized ratios while avoiding unnecessarily large positive exponentials in the demonstrated course function. It does not establish that the scores are correct, that a likely token is true, that probabilities are calibrated, or that the teaching implementation handles every imaginable extreme input.
