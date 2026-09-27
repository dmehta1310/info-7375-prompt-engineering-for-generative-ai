# Expected, Observed

**Arundhati Kandelkar** · INFO 7375 — Prompt Engineering for Generative AI
Week 1 Explainer Video · Fall 2026

---

## The concept

**Expected count (665.24) versus observed count (630)** — from Chapter 1,
Part 2. One run of 1000 draws came up 35 short of what the math predicts. That
gap is genuinely unusual — about 2.4 standard deviations, roughly 1 run in 50.
And it still is not evidence the probabilities are wrong, because it is a single
draw from one fixed seed, read after the fact. Surprise is a reason to test, not
a verdict.

**Why this one.** It is the smallest idea in the chapter that can be explained
completely and still change how you read a result. The whole video turns on a
single number that does not match a single other number — and on the discipline
of not drawing a conclusion from that. Chapter 1's real subject is telling a
fluent output apart from a supported claim, and a 35-draw gap is the cheapest
place to practise that: it *looks* like a finding, and it is not one.

**Runtime.** 2 minutes 27 seconds (147.2s). 3840×2160, h264 + AAC.

---

## What's in this folder

| File | What it is |
|---|---|
| `README.md` | This file |
| `beat_sheet.json` | The reviewed narration and visual plan — ten beats, each with a `show` block of visual events |
| `BUILD-PROMPT.md` | The prompts and commands that rebuild the video from scratch |
| `SOURCES.md` | Every number's origin, what I made, what Claude contributed, seeds, licences |
| `FRICTIONAL.md` | Dated log — what I tried, what broke, what I did |
| `CHECKS-REPORT.md` | PROOF GATE report, written before the first render, amended after |
| `FACTCHECK.md` | Every claim, its verdict, its derivation — including the one that **failed** and changed the video |
| `SHOTLIST.md` | Per-beat stage directions and the honesty labels QC must confirm |
| `PROMPTS.md` | Generation inputs — there are none; no paid media, no generated narration |
| `TYPECHECK.md` | GATE T typography report (PASS) |
| `components/ExpectedObserved.tsx.txt` | The five Remotion components I wrote for the body beats. Stored with a `.txt` suffix because `scripts/validate_course.py` rejects `.tsx` anywhere in the repo as a "Non-Python implementation" — the course is Python-and-Claude only. Rename to `.tsx` to use it. |
| `captions/expected-observed.srt` | Captions — built from the authored narration and the measured per-beat audio, not machine-transcribed, so they match the script exactly |
| `evidence/main-py-output.json` | The raw, unmodified output of the lesson code |
| `evidence/verify_claims.py` | **Re-checks all 23 on-screen numbers against `main.py`.** Standard library only |
| `_qc/REPORT.md`, `_qc/contact_sheet.png` | GATE V frame-level QC result and the sampled frames |

### Where the video is

This repository's `.gitignore` excludes `*.mp4` and `*.mp3` at any depth
(*"Keep generated audio/video out of Git"*), so the rendered file is **submitted
on Canvas**, not committed here. What is posted here is everything needed to
rebuild it: the beat sheet, the components, the build prompt and the gate
reports. The render is deterministic — same seeds, same frames.

### Check the numbers yourself

```bash
python3 fall-2026/arundhati-k/week-01-video/evidence/verify_claims.py
```

```
23/23 claims reproduced
Every number shown in the video is reproducible from unmodified lesson code.
```

It recomputes every figure from `lessons/01-randomness-and-first-prompts/code/main.py`
and fails loudly if any drifts. Verified on Python 3.9.6 and 3.12.14.

---

## How the video is built

Ten beats on the Brutalist `ai-explainer` spine — cold open, executive summary,
body, verdict, handoff, title outro:

| Beat | Act | What it does |
|---|---|---|
| B00 | ASK | The question, typed into the Claude composer |
| B01 | BLUF | The overview, written and **corrected** on screen: *proof* → *unusual* |
| B02 | SOURCE | Where 0.6652 comes from — one beat, deliberately |
| B03 | EXPECTED | `0.6652… × 1000 = 665.24`, then bounded as a long-run average |
| B04 | OBSERVED | The real printed counts; bars grow to 102 / 268 / 630 |
| B05 | GAP | The 35.24 difference, ≈2.4 sd — **labelled as a constructed illustration** |
| B06 | FALSIFIABILITY | Where 630 really falls (the tail), and that this video doesn't run the test |
| B07 | VERDICT | What this video does and does not establish |
| B08 | HANDOFF | A runnable prompt: the experiment B06 named as missing |
| B09 | OUTRO | Title restate |

**One concept, not a chapter tour.** Softmax appears once (B02) and only to
source the single number B03 multiplies — the beat ends by saying so on screen.
The max-subtraction is a *separate* concept on the assignment's list and is not
taught here.

**What it does not establish** (B06, B07, stated plainly on screen): that
`0.6652` is the correct probability for logits `[1,2,3]`. One sample of 1000
cannot show that. Confirming it needs repeated runs and a check on whether 630
sits inside the expected spread — which is exactly the experiment the video
hands to the viewer in B08 rather than pretending to have run.

**Honesty labels.** B05 carries `CONSTRUCTED ILLUSTRATION` for its full
duration; B06's right-hand panel is dimmed and captioned `NOT RUN IN THIS VIDEO`
because it schematises an experiment I did not perform. No Claude conversation
appears in the video — the composer beats show a prompt being typed, never a
claimed response.

---

## Rebuilding it

Full detail in [`BUILD-PROMPT.md`](BUILD-PROMPT.md). The short version, from a
folder containing both `brutalist.art/` and the course repo:

```bash
brew install ffmpeg                       # required; ./setup does NOT install it
cd brutalist.art && ./setup --install
```

```bash
cd brutalist.art
REEL=../info-7375-prompt-engineering-for-generative-ai/youtube/claude-liam-expected-vs-observed
.venv/bin/python runtime/scripts/generate_audio_kokoro.py $REEL
.venv/bin/python runtime/scripts/remotion_scenes.py     $REEL
.venv/bin/python runtime/scripts/compile.py             $REEL
```

Two things the rebuild depends on that are easy to miss:

1. **The five body components live in the toolkit, not here** —
   `runtime/remotion/src/scenes/ExpectedObserved.tsx`, registered in
   `Root.tsx`. Run `./art scene-index` and confirm all five report
   `RENDERABLE` before rendering.
2. **Verify the numbers first.** Run
   `lessons/01-randomness-and-first-prompts/code/main.py` and check its output
   against the `REAL` constants in `ExpectedObserved.tsx`. If they ever
   disagree, `main.py` is right and the components are wrong.

Free pipeline throughout — Kokoro narration is local, Manim and Remotion render
locally. No API keys, no paid generation, no upload. Total spend: $0.00.
