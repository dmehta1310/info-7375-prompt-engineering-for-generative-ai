# SOURCES

## Concept source

- **Chapter 1, "Randomness and first prompts,"** Part 1, section "One question, asked over and over" (course textbook). This is the source of the claim that models predict tokens rather than words, and that character-level tasks are awkward for a system whose atoms are subword chunks. I also borrowed its `unbelievable` example.

## Data and evidence (all real, none constructed)

| ID | What | Source |
|---|---|---|
| S1 | Token IDs, pieces, and character counts for `strawberry`, ` strawberry`, `unbelievable`, `raspberry` | My own run of tiktoken 0.14.0, encoding `cl100k_base`. Reproduce command in README.md and FACTCHECK.md. |
| S2 | Claude's answer: "strawberry" has 3 r's, grouped as "straw, ber, and ry" | Screenshot I captured, 22 Sep 2026, 11:34 PM (macOS clock visible). Claude desktop app; model version not recorded. |
| S3 | Claude's answer: "blueberry" has 2 r's | Screenshot I captured, 22 Sep 2026, 11:34 PM. |
| S4 | Token IDs for `Thank you!` (`Thank` / ` you` / `!` = 13359 / 499 / 0) | tiktoken 0.14.0 run by Claude Code during the build and re-checkable with the README command. |

**Tokenizer caveat:** `cl100k_base` is GPT-4's tokenizer, not Claude's. The video says so on screen.

**No constructed illustrations:** Every number on screen comes from S1 or S4. The only non-token grouping shown (B06's "straw / ber / ry") comes from S2. It is labelled as Claude's grouping, with no token IDs.

## Tools used

| Tool | Version | Role | Licence |
|---|---|---|---|
| Brutalist toolkit (`nikbearbrown/brutalist.art`) | cloned Sep 2026 | Reel pipeline, QC gates, compile | No licence declared: the repo has no LICENSE file, and GitHub reports none (checked 26 Sep 2026). Used as the course's toolkit. |
| Manim Community | 0.18.1 | All scene animation | MIT |
| Kokoro TTS, voice `am_onyx` | Kokoro-82M v1.0 weights via kokoro-onnx 0.6.1, local | Narration | Model weights: Apache-2.0 (`hexgrad/Kokoro-82M` model card). kokoro-onnx wrapper: MIT (its bundled LICENSE). |
| tiktoken | 0.14.0 | Token data | MIT |
| ffmpeg / ffprobe | local | Audio measurement and muxing | LGPL/GPL |
| TeX Live, with `dvisvgm` | 2026 (pdfTeX 3.141592653-2.6-1.40.29) | Typesets the live counters in B01 and B03 (Manim's `Integer`) | No single licence: a collection of free packages, each under its own terms (TeX Live's LICENSE.TL) |
| Computer Modern (`cmr10`) | TeX Live 2026, AMS Type 1 version (`amsfonts`) | Digits in the B01/B03 counters | Computer Modern: Knuth's licence (`cm`). The AMS Type 1 files that `dvisvgm` outlines: SIL Open Font License 1.1 (`amsfonts`) |
| Menlo font | macOS system font | Monospace text in scenes | Bundled with macOS; used for local rendering only |
| Times (serif text font) | macOS system font (`Times.ttc`), resolved by Pango 1.58.2 (CoreText backend) from its default `serif` | Labels and captions | Bundled with macOS; used for local rendering only |

No stock footage, music, images, or paid generation. No API keys were used.

## What I made

- Chose the concept and approved every beat of the script.
- Ran the tiktoken measurements (S1) and captured the two dated Claude responses (S2, S3).
- Watched the review cuts and requested the changes: letter spacing, a natural personal open, connected flow between beats, a less abrupt ending, and the "Thank you" token ending (my idea).
- Made the final decisions on runtime, what to claim, and what to leave out.

## What Claude contributed

- **Claude (claude.ai chat):** Explained the concept, drafted the script and beat structure, and wrote every prompt given to Claude Code (see BUILD-PROMPT.md). It also drafted README.md, SOURCES.md, FRICTIONAL.md, and BUILD-PROMPT.md, which I reviewed and edited. The draft script contained one factual error, which was corrected before the final render: it said "belie" is not a word (see FRICTIONAL.md).
- **Claude Code (VS Code extension):** Explored the toolkit and chose the rendering path from evidence. It wrote `scenes.py`, `beat_sheet.json`, `FACTCHECK.md`, `SHOTLIST.md`, and `PROMPTS.md`, ran audio generation and renders, fixed pipeline bugs, and verified frames by looking at them. It caught several false visual claims that the automated gates missed (see FRICTIONAL.md).

I am responsible for the submission and can explain every claim in it.
