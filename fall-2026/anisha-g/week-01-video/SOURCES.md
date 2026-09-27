# Sources and Contributions

## Course sources

- Nik Bear Brown, **INFO 7375: Randomness and first prompts**: <https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/chapters/01-randomness-and-first-prompts.md>. The relevant passages describe the seed as a repeatability control, explain that changing it changes the selected sequence, and state that it does not give a sample privileged factual status.
- Course reference implementation: `lessons/01-randomness-and-first-prompts/code/main.py` in the same repository.
- Course tests: `lessons/01-randomness-and-first-prompts/code/tests/test_main.py`; `test_04` compares two calls that use the same default seed.
- Course figure used only as a visual-language reference: `images/01-randomness-and-first-prompts-fig-01.png`. No pixels or diagram contents were copied. Original graphics use a related white canvas, serif headings, outlined process boxes, gray support text, red emphasis, and gold footer rule.
- Sources were inspected and the reference program was run on 2026-09-26. The exact repository revision appears in `FACTCHECK.md`.

## Toolkit, narration, and fonts

- Nik Bear Brown, **Brutalist (Film as Code)**: <https://github.com/nikbearbrown/brutalist.art>. The submission follows its beat-sheet and audio-first workflow.
- **Kokoro-82M / Kokoro v1.0**, rendered locally through `kokoro-onnx`; Apache-2.0 as documented by Brutalist. Voice: `af_bella`, speed `0.94`. Wrapper: <https://github.com/thewh1teagle/kokoro-onnx>.
- **DejaVu Serif, Sans, and Sans Mono**, rasterized into original frames. DejaVu/Bitstream Vera permissive licence: <https://dejavu-fonts.github.io/License.html>.

## What was made for this submission

- All layouts, motion graphics, process boxes, animated count bars, arrows, comparison panels, and captions.
- The reviewed narration and `beat_sheet.json`.
- The seed reproduction and checks, captured outputs, video renderer, SRT generator, fact-check, review record, and documentation.
- No third-party images, music, stock footage, Claude transcript, fabricated model response, or invented numerical result appears in the video.

## AI contribution

- **Claude contribution: none.** No Claude response or transcript is represented.
- OpenAI Codex inspected the supplied assignment and professor example, read the public course and Brutalist repositories, ran the course program, proposed this distinct backup concept, drafted and revised the narration, wrote evidence and rendering code, generated the local synthetic narration, rendered the MP4, checked the frames, and organized the deliverables.
- Anisha Gaikar requested a second, distinct backup submission after reviewing the first assignment's voice and graphics. Anisha remains responsible for watching, understanding, selecting, and submitting the final version.

## Claim boundary

The video supports a narrow claim: in the recorded environment, the same seed and same setup replay the same sample, while changing only the seed changes this observed sample without changing its probabilities. It does not establish that a sampled label is true, correct, or supported by evidence, and it does not promise identical results across every future Python version or implementation.
