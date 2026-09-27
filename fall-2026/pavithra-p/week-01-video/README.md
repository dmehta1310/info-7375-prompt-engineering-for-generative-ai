# Week 01 video — A training-scale slogan, restated as a division with its hidden assumptions

**Name:** Pavithra Prasad
**Course:** INFO 7375, Prompt Engineering for Generative AI (Fall 2026)
**Submitted:** 2026-09-27 (final version)
**Video:** [`thousands-of-years-divided.mp4`](thousands-of-years-divided.mp4)
**Runtime:** 2:28 (148.3 s) · 3840×2160 · 24 fps · H.264 + AAC
**Video SHA-256:** `d3f26f37b3c8ee62a542b9f6a35ad74b4bff2235b5bc86eb4feb479c37daf761` (check with `shasum -a 256 thousands-of-years-divided.mp4`)

> **Video and audio on GitHub:** the `.mp4` and `mp3/*.mp3` files are not in this GitHub folder, because the course repo's `.gitignore` excludes generated audio and video. The video is in the Canvas zip (`Prasad_Pavithra_INFO7375_Week01_Video.zip`) and can be rebuilt with [`BUILD-PROMPT.md`](BUILD-PROMPT.md).

## Concept

**A training-scale slogan, restated as a division with its hidden assumptions.**
Chapter 1, Part 1, "Scale, in units you can check": "it would take a human thousands of years to read GPT-3's training text."

**Why this one:** it is a single idea I can defend with nothing but multiplication and division, and every number in it comes from the course's own script, so the mechanism can be shown moving on screen instead of asserted.

## What the video shows

| Beat | Idea | Evidence on screen |
|---|---|---|
| B00 | The slogan is an estimate produced by division, not a measured fact | — |
| B01 | Starting number: ~300 billion training tokens | **REPORTED**: Brown et al. 2020, arXiv:2005.14165 |
| B02 | × 0.75 words per token = 225 billion words | 0.75 labelled as an approximation |
| B03 | ÷ 250 wpm → 900,000,000 minutes → ≈ 1,711.2 years | script output |
| B04 | Hidden guess #1, reading speed: 1,426.0 / 1,711.2 / 2,138.9 / 2,851.9 years | script output; live dial |
| B05 | Hidden guesses #2 (0.75 words/token) and #3 (24 hours a day). At 8 h/day every answer triples. | **CALCULATED EXTENSION** label |
| B06 | **What this does not establish:** understanding, accuracy, or that the tokens were unique text | — |
| B07 | Ask: what is being divided, and what did someone assume? | — |

**Boundary (named in B06):** the calculation only turns a *reported* token count into *hypothetical* human reading time. It says nothing about whether the model understood anything, whether its answers are accurate, or whether all 300 billion tokens were unique text.

**Constructed items, labelled on screen:** the "un / believ / able" token split (B01) is an illustration, not real tokenizer output. The 8-hours-a-day figures (B05) are my extension, computed with the course script's own `reading_years()` but not printed by it. No Claude screen or transcript appears in the video.

## Rebuild it

Full steps are in [`BUILD-PROMPT.md`](BUILD-PROMPT.md). In short, with the Brutalist toolkit checked out beside the course repo:

```bash
cd brutalist.art && . .venv/bin/activate
REEL=../info-7375-prompt-engineering-for-generative-ai/fall-2026/pavithra-p/week-01-video
python3 $REEL/evidence.py                               # numbers, from research/llm_scale.py
python runtime/scripts/generate_audio_kokoro.py $REEL   # narration (Kokoro af_bella, local)
./art run $REEL --height 1080                           # QC gates + Manim renders + review cut
./art final $REEL                                       # clean master → brutalist.art/renders/
```


## Files

| File | What it is |
|---|---|
| `thousands-of-years-divided.mp4` | The video |
| `beat_sheet.json` | Reviewed narration and visual plan, with the approval record and build stamps |
| `scenes.py` | The eight Manim scenes |
| `evidence.py` / `evidence.json` | Every number, pulled from and checked against `research/llm_scale.py` |
| `mp3/` | Narration audio per beat (Kokoro output) |
| `BUILD-PROMPT.md` | Prompts and commands that rebuild the video |
| `SOURCES.md` | What I used, what I made, what Claude contributed, licences |
| `FRICTIONAL.md` | Dated log of what broke and what I did instead |
| `FACTCHECK.md` | Every claim with its verdict and source |
| `SHOTLIST.md`, `PROMPTS.md`, `STATUS.md`, `ToDo.md`, `TYPECHECK.md`, `qc-sheet.png`, `_qc/REPORT.md` | Brutalist build paperwork and QC results (all gates passed) |
