# Week 1 Explainer Video — Temperature Is Concentration, Not Truth

**Assignment:** Week 1 Explainer Video — Explain One Concept from Chapter 1 (25 points)
**Student:** Hemanth Rayudu
**Course:** INFO 7375 · Prompt Engineering & Agentic AI · Fall 2026 · Section 01
**Concept:** Temperature is a *concentration* control, not a fact checker
**Source:** Chapter 1 — Randomness and first prompts, Part 2
**Audience:** INFO 7375 classmates and graders, or anyone who's been told temperature is a "creativity dial"
**Status:** reviewed local final, watched and approved by me on 2026-09-26 (see `REVIEW.md`). Not published.
**Runtime:** 3:08 (187.88 s) · 3840×2160 · 24 fps · H.264 / AAC · captions included
**Licence:** MIT for code, CC BY 4.0 for the video and documents — see `LICENSE`

## The one sentence

Temperature rescales the **ratio** between outcomes — it never reorders them,
and it never adds information the model didn't have.

## Why this concept

Chapter 1 hands you a softmax and a temperature knob, and every popular
explanation calls that knob "the creativity dial." That framing is wrong in a
way that matters: it implies the number has something to do with whether the
answer is *right*. One line of arithmetic shows what it actually controls.
Because normalization cancels out of a ratio, temperature's entire effect fits
in one exponent:

$$\frac{p_2}{p_0} = \exp\!\left(\frac{z_2 - z_0}{T}\right)$$

With scores `[1, 2, 3]` the gap `z₂ − z₀` is fixed at 2, so only `T` moves.
The best outcome is **54.6×** the worst at T = 0.5 and only **2.7×** at T = 2 —
exactly e⁴ and e¹. Same scores, same winner, different concentration. The video
lands that identity and then names its limit out loud: concentration is not
correctness.

## What it shows

| Beat | What happens |
|---|---|
| B00 | The question the video answers, typed as a prompt in the Claude app — no Claude answer is shown |
| B01 | The overview is typed with the misconception, then corrected on screen — "creativity" → "concentration", "truthful" → "concentrated" — ending word-for-word on the narration |
| B01A | **The everyday analogy** — a contrast slider spreads three greys apart and washes them back together, and the marker on the brightest never moves. Temperature is the slider run backwards: lower temperature, higher contrast |
| B02 | The whole softmax: three scores → three bars → sum settles at 1.000000 |
| B03 | The question the next figure answers: what happens to the ratio between two outcomes |
| B04 | **The why, shown:** p₂/p₀ written as two fractions over the same total, which cancels — leaving exp((z₂ − z₀)/T). Then the ratio collapsing 54.6 → 7.39 → 2.72 = e⁴/e²/e¹, and why no two outcomes can ever swap places |
| B05 | **The boundary** — at T = 0.1 the worst outcome is 2.061060e-09, not zero; T = 0 is refused outright. Closes on the analogy callback: a sharper picture of the wrong person |
| B06 | One-page verdict, including the seed-7 counts 849 / 630 / 469 and the full T = 2 row 202 / 329 / 469 |
| B07 | Your turn — a prompt that breaks everything except the fixed ratio, read aloud word for word |
| B08 | Title restate + credit |

## What this explanation does NOT establish

No change in concentration can supply information the program never received.
Temperature reshapes *preference*, not *correctness*. A lower temperature makes
a confident answer more likely to be selected — it does nothing to make it
true. That is beat B05, stated on screen and in the narration.

## Evidence

Every figure on screen was reproduced locally from
`lessons/01-randomness-and-first-prompts/code/main.py` (scores `[1, 2, 3]`,
seed 7, n = 1000) and independently recomputed before authoring. The
claim-by-claim table is in `FACTCHECK.md`; licences and attribution are in
`SOURCES.md`. Two visuals are honest exaggerations for visibility and one beat
is an explicit analogy — all three are captioned as such on screen and listed
in `FACTCHECK.md`.

## Contents

| File | What it is |
|---|---|
| `temperature-is-concentration.mp4` | the video (3:08, 4K) |
| `temperature-is-concentration.srt` | captions, 58 cues, built from the aligned narration |
| `beat_sheet.json` | the reviewed narration + visual plan, one entry per beat |
| `scenes.py` | the Manim scenes (B01A, B02, B04, B05, and the B08 outro card) |
| `README.md` | this file |
| `BUILD-PROMPT.md` | the prompts and commands that rebuild the video |
| `SOURCES.md` | what I used / made / Claude contributed, with licences |
| `FACTCHECK.md` | every on-screen claim and its verification |
| `CHECKS-REPORT.md` | the proof gate: per-beat classification and QC results |
| `SHOTLIST.md` | the typed work order: one row per beat — lane, fill, measured duration |
| `FRICTIONAL.md` | dated honest log of what broke and what I did instead |
| `REVIEW.md` | my review: every problem found, who found it, the fix, how it was re-checked, and my approval |
| `make_srt.py` | builds the .srt from the word-level alignment |
| `PROMPTS.md` | the on-screen prompts and the authoring prompt |
| `LICENSE` | MIT (code) + CC BY 4.0 (video and documents) |

> **Where the video file lives.** The course repository keeps generated media
> out of Git by policy (`.gitignore`: *"Keep generated audio/video out of Git,
> at any depth and in any case."*), so `temperature-is-concentration.mp4` is
> **not** in the GitHub folder — it is the file uploaded to Canvas, inside
> `Rayudu_Hemanth_INFO7375_Week01_Video.zip`. Everything needed to rebuild it
> byte-for-content is here: `beat_sheet.json`, `scenes.py`, `make_srt.py`, and
> the commands under **Run** below. The captions (`.srt`) are text, so they are
> committed.

## Setup

Requires macOS or Linux, Python 3.10+, Node 20+, and ffmpeg. Built entirely on
the free local pipeline — no API keys, no paid calls, total cost **$0.00**.

```bash
# 1. system dependency
brew install ffmpeg                       # or: apt install ffmpeg

# 2. the toolkit
git clone https://github.com/nikbearbrown/brutalist.art
cd brutalist.art
python3.12 -m venv .venv && source .venv/bin/activate
./setup --install                         # Python deps, Remotion modules, Kokoro model (~340 MB)
./setup                                   # readiness table — every row should read READY

# 3. the course repo, for the numbers
git clone https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai chapter1-course
```

Re-activate the venv (`source .venv/bin/activate`) in every new terminal before
running `./art` — the scripts shell out to plain `python3`.

## Run — rebuild the video from this folder

Copy `beat_sheet.json`, `scenes.py`, `make_srt.py` and the paperwork set
(`FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`, `CHECKS-REPORT.md` — the pipeline's
GATE F refuses to render without the first three) into a reel folder, then, from the
toolkit with its venv active:

```bash
REEL=../week-01-video/reel

python3 runtime/scripts/generate_audio_kokoro.py "$REEL"   # audio first — durations are the clock
./art run   "$REEL"                                        # QC gates + render + review cut
./art final "$REEL" --out "$REEL"                          # clean 4K master, no beat markers

python3 runtime/scripts/align.py "$REEL"                   # word-level timing -> mp3/words.json
python3 "$REEL/make_srt.py" "$REEL"                        # -> temperature-is-concentration.srt
```

Audio is the master clock: per-beat MP3 durations are measured and written back
into `beat_sheet.json`, and every scene is built to its measured duration. Never
fix timing by hand — change the narration, regenerate the audio, recompile.

Full step-by-step, prerequisites, and the exact authoring prompts are in
**`BUILD-PROMPT.md`**.

## Verify

```bash
# 1. the numbers on screen are real — reproduce them
python3 chapter1-course/lessons/01-randomness-and-first-prompts/code/main.py
#    expect probabilities [0.09003057317038046, 0.24472847105479764, 0.6652409557748218]
#    and counts {"0": 102, "1": 268, "2": 630} at seed 7, n = 1000

# 2. the delivered file is the intended one
shasum -a 256 temperature-is-concentration.mp4
#    88bbcabcb507da049398d1b56f30d5665bfeaab008634a6dcd86324df3e585ba

# 3. the render is what it claims to be
ffprobe -v error -show_entries format=duration -show_entries stream=width,height \
        -of default=noprint_wrappers=1 temperature-is-concentration.mp4
#    expect 187.875 s at 3840×2160
```

**Tested, not assumed.** On 2026-09-26 the video was rebuilt from a fresh folder
containing only the seven files listed under **Run**, using those commands
verbatim. Every gate passed, all ten beats rendered from scratch, and the rebuilt
master was **byte-identical** to the submitted file — same SHA-256 — with
identical narration audio and captions. On a different machine or toolchain
version, expect the same content rather than the same bytes; Manim and ffmpeg
are not bit-deterministic across versions. The per-input SHA-256 record
for the submitted master is in the reel's `temperature-is-concentration.verified.json`.

Renders are verified by **looking at frames**, not by the probe alone. Gate V
samples the compiled reel and writes `_qc/REPORT.md`; the per-beat frame pass
that caught the one real defect in this build is described in `FRICTIONAL.md`
(2026-09-22) and `CHECKS-REPORT.md`.

## Credits and assistance

Detailed, line-by-line attribution is in **`SOURCES.md`**. In summary:

- **Mine** — the concept choice and the argument, the narration script, the beat
  structure, the Manim scenes' design and layout, the verification of every
  figure, and all judgement calls about what the video does and does not claim.
- **Claude (Claude Code)** — drafting and editing passes on the narration,
  authoring `beat_sheet.json` against the toolkit's schema, writing the
  `scenes.py` Manim code to my designs, and the QC and fix loop. Named per the
  course AI policy; I can explain every part of what is submitted.
- **Starting sources** — the `brutalist.art` toolkit (pipeline, gates, Remotion
  scenes) and the course repository's Chapter 1 `main.py` and
  `research/worked-examples.json` for every number on screen.
- **Third-party components** — Kokoro-82M (Apache-2.0), Manim CE (MIT),
  Remotion, EB Garamond and PT Mono (SIL OFL 1.1), ffmpeg. Full terms in
  `LICENSE` section 3 and `SOURCES.md`.
