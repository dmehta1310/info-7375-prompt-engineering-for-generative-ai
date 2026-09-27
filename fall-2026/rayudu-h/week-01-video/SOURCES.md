# SOURCES — Week 1 explainer

Three columns of honesty: what I **used**, what I **made**, and what **Claude
contributed**.

## Used

| Thing | Where it came from | Licence / terms |
|---|---|---|
| The numbers | `lessons/01-randomness-and-first-prompts/code/main.py` in the course repo (`nikbearbrown/info-7375-prompt-engineering-for-generative-ai`), run locally; output saved to `main-output.txt` | course material |
| The derivation and boundary statements | `chapters/01-randomness-and-first-prompts.md` (same repo) | course material |
| Cross-check table (T = 0.5 / 1 / 2) | `research/worked-examples.json` → `chapters.01` (same repo) | course material |
| Narration voice | **Kokoro-82M** (`af_bella`) via `kokoro-onnx`, run locally on CPU | Apache-2.0 · no account, no API, $0.00 |
| Animation engine | **Manim Community Edition** 0.18 | MIT |
| Caption timing | **faster-whisper** 1.2.1, via the toolkit's `align.py` — supplies word timestamps only; the caption TEXT is the known narration, snapped on by `SequenceMatcher`, never a transcription | MIT |
| Scene/compositing engine | **Remotion** 4.0.x | Remotion licence (free for individuals / non-commercial; this is unpublished coursework) |
| Muxing / conform | **ffmpeg** 9.0.1 | LGPL/GPL |
| Typeface | **EB Garamond** (bundled in the toolkit's `runtime/fonts`) | SIL Open Font License 1.1 |
| Typeface | **PT Mono** (the `ValueError` card only) | SIL Open Font License 1.1 |
| Pipeline / toolkit | `brutalist.art` — `./art` toolkit, its `ai-explainer` skill doctrine, and its QC gates | course toolkit |

No paid API was called at any point. No stock footage, no AI-generated images,
no third-party imagery — every frame is drawn by Manim or Remotion from code in
this folder plus the toolkit's registered compositions.

**The narration is a synthetic voice.** Every word you hear is the Kokoro-82M
text-to-speech model (voice `af_bella`) reading my script, generated locally. It
is not my voice, and it is not a recording of anyone.

## Made

- **`beat_sheet.json`** — the 9-beat plan: act structure, the `show` block for
  every beat (what the viewer watches, event by event), narration, and the
  props passed to each composition.
- **`scenes.py`** — the four Manim scenes (`B01A_ContrastSlider`,
  `B02_ScoresToProbs`, `B04_RatioCollapse`, `B05_ConcentrationLimit`), written
  against the toolkit's safe-area and contrast gates.
- **`B01A_ContrastSlider`** — the everyday-analogy beat, added 2026-09-22. A
  photo contrast slider rescales how much three greys differ while the marker on
  the brightest never moves. Authored here rather than reused: the toolkit's
  library search returned no component for it (logged to the toolkit's
  `TEMPLATE-MISSES.md` by the search itself). Carries no measured figure and is
  captioned "analogy — illustrative, not measured" throughout.
- **`B08_TitleCredit`** — the outro, written as a reel-local Manim scene
  because the stock Claude title card (`ClaudeTitleOutro`) hardcodes the
  instructor's channel handle and the other registered outros carry other
  brands' palettes. Keeping it in `scenes.py` means this assignment adds
  **nothing** to the toolkit — the reel builds against a clean clone.
- **`make_srt.py`** — the reel's own SRT writer. The toolkit produces word-level
  timing (`mp3/words.json`) but has no publish step, so no SRT emitter ships with
  the free pipeline; this one groups the aligned words into cues, wraps them to a
  42-character budget, and offsets each beat by its real clip duration.
- **The narration script** — all ten beats, written to be the voice *reacting*
  to what is on screen rather than a self-sufficient essay.
- **`FACTCHECK.md`**, **`SHOTLIST.md`**, **`PROMPTS.md`**, **`CHECKS-REPORT.md`**
  — the reel's own verification and work-order paperwork.
- **The independent numeric re-derivation** used to fact-check every on-screen
  figure before authoring (a standalone softmax, not the course code).

## Claude contributed

Claude Code was used as a working collaborator throughout, and specifically:

- **Beat-sheet authoring** — drafting the act structure and the `show` blocks,
  and the narration passes that followed.
- **Manim scene code** — the scenes in `scenes.py`, including the layout
  arithmetic that keeps every label inside the safe area.
- **The reel-local Manim outro** (`B08_TitleCredit`) — written to replace the
  channel-locked stock outro without modifying the toolkit.
- **Pipeline work** — reading the toolkit's skill doctrine and QC gate rules,
  running the audio/render/QC chain, and diagnosing gate failures.
- **The fact-check pass** — recomputing every figure independently and flagging
  the two visuals that needed "constructed / exaggerated" captions.

I directed the work, chose the concept and the argument, verified every number
against `main.py` myself, and reviewed the rendered frames. **No Claude
response appears on screen.** The Claude app styling in B00, B03 and B07 frames
prompts I wrote; it never shows an answer.

That was not true of every earlier cut, and the correction belongs here. Until
2026-09-24, B00 showed three result lines landing under my prompt, as Claude's
answer, under a composer chip reading a real model name — lines I had written
into the beat sheet, not a response Claude gave. I had described them in this
file as "the film's own content," and I no longer think that framing holds: a
viewer sees Claude answering, and the assignment requires any Claude response
shown on screen to be real and dated. On 2026-09-25 I removed the result lines,
blanked the model chip in all three composer beats, and replaced B03's
"rendering Manim…" indicator, which implied Claude generated the next figure.

## Corrections applied during the build (DOUBLE-CHECK LAW)

1. **"Temperature is the creativity dial"** — the framing the video exists to
   dismantle. It appears on screen in B01 only as the writer's *first, wrong*
   sentence, visibly corrected to "a concentration control".
2. **Dropped the chapter's wrong-answer hypothetical entirely.** It is a
   constructed illustration (labels treated as answers, answer key = label 0),
   and showing it — even captioned — would have spent screen time on a
   fabricated error instead of the mechanism. Nothing in the reel depends on it.
3. **"Low temperature is argmax" corrected on screen.** At T = 0.1 the worst
   outcome still holds 2.061060e-09. B05 shows the sliver rather than letting
   the bar read as zero.
4. **Spoken vs. screen precision separated.** Narration speaks rounded figures
   because 10-decimal numbers are unlistenable; the screen always carries the
   exact value. Nothing is rounded *up*, and no spoken figure contradicts its
   on-screen source.

## Reproducibility note

`main.py` was run **3 times** under Python 3.9.10 and again under 3.12.9, and
returned identical counts `{0: 102, 1: 268, 2: 630}` every time. The chapter
records its own saved run under Python 3.14.6. So the honest claim is: **these
counts matched on these interpreter versions** — not that they are reproducible
on every platform, which I did not test.

On 2026-09-26 `main.py`'s own `sample()` was also run at T = 0.5 and T = 2 (Python 3.12.9, seed 7, n = 1000). All nine counts matched the course's recorded worked examples exactly, including the T = 2 row 202 / 329 / 469 now shown in B06.

Also on 2026-09-26, the whole video was rebuilt from this folder alone — the seven source files the README lists, the README's commands verbatim. The result was byte-identical to the submitted mp4 (same SHA-256), with identical audio and captions.

## Licence of this submission

My own contributions in this folder are released under two licences, recorded
in full in `LICENSE`:

- **MIT** — `scenes.py` and `beat_sheet.json`
- **CC BY 4.0** — `temperature-is-concentration.mp4` and the written documents

Nothing above relicenses the third-party components in the table at the top of
this file; each keeps its own terms. The numeric results on screen are outputs
of the course repository's `main.py` — facts about that program, attributed
rather than claimed.
