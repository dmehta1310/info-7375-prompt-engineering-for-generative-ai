# The Token That Followed

**Rithika Sankar Rajeswari** · INFO 7375 — Prompt Engineering for Generative AI · Week 01 · Chapter 1

**Concept:** What pretraining actually targets — the token that followed, not the truth.

**Why (one sentence):** Everyone repeats that "models predict the next word, not facts,"
but almost nobody shows the arithmetic where that happens, so this video displays a
factually false training line and walks the exact numbers — logits, max-subtraction,
exponentiation, normalization, loss — that reward the model for reproducing it.

**Runtime:** **4:14.042** (254.042 s), verified with
`ffprobe -v error -show_entries format=duration` on the delivered master — not
estimated from `beat_sheet.json`. The measured narration clock sums to 253.86 s; the
master is 254.042 s because `compile.py` ceilings each beat to the 24 fps frame grid.
Clears the 4:00 floor by 14.04 s.

**Narrator:** Sasha (persona) · Kokoro TTS voice `af_bella`, local, $0.00.

**Audience:** absolute beginners. No prior term is assumed — "token", "logit", "softmax"
and "loss" are each introduced the moment they are first needed and not before.

> **Runtime note.** The written syllabus target is 2–4 minutes. This cut runs past that
> because the professor said in class that the video should run at least 4:00, overriding
> the written target. That was a live-class comment, not a Canvas update — see
> `FRICTIONAL.md` § Revision — 2026-09-23, which also carries an open item: the class date
> is left as a placeholder for me to fill in rather than guessed.

---

## Structure — six acts, twelve beats

| Beat | Act | Measured | Scene | What appears |
|---|---|---|---|---|
| B00 | HOOK | 14.45s | `Ch1PretrainHook` | The false claim, as plain English |
| B01 | MECHANISM | 20.57s | `Ch1PretrainCorpus` | Text → tokens → the next-token question |
| B02 | MECHANISM | 23.28s | `Ch1PretrainTarget` | The answer key: one on cheese, zero on rock |
| B03 | MECHANISM | 20.04s | `Ch1PretrainLadder` | Step 1 — the raw scores |
| B04 | MECHANISM | 22.22s | `Ch1PretrainLadder` | Step 2 — subtract the largest score |
| B05 | MECHANISM | 21.77s | `Ch1PretrainLadder` | Step 3 — exponentiate |
| B06 | MECHANISM | 20.62s | `Ch1PretrainLadder` | Step 4 — divide by the sum |
| B07 | MECHANISM | 21.77s | `Ch1PretrainLadder` | Step 5 — the probabilities, summing to exactly 1 |
| B08 | CONTRAST | 25.44s | `Ch1PretrainContrast` | Same model, two corpora, two answer keys |
| B09 | LOSS | 20.33s | `Ch1PretrainLoss` | The penalty reads one slot |
| B10 | BOUNDARY | 34.06s | `Ch1PretrainBoundary` | What this does not establish |
| B11 | TAKEAWAY | 9.31s | `Ch1PretrainTakeaway` | One sentence, no new claims |

The film opens on the false sentence with no math on screen, asks what the model learns
to predict after "green", and **holds on 3.5s of real silence** so the viewer answers
before the answer appears. The mechanism act then adds exactly one column per beat, so no
beat asks the viewer to absorb two new things at once.

## The claim, and the mechanism that carries it

A constructed science-fiction corpus contains the line **"The moon is made of green cheese."**
Conditioning on `The moon is made of green`, the reel shows the softmax in the five steps a real
implementation performs:

| Candidate | 1: z | 2: z − max | 3: exp(z − max) | 4: ÷ Σ | 5: p | Percent |
|---|---|---|---|---|---|---|
| `rock` | +4.0 | 0.0 | 1.0000 | 1.0000 ÷ 1.0792 | 0.9266 | 92.7% |
| `cheese` | +1.0 | -3.0 | 0.0498 | 0.0498 ÷ 1.0792 | 0.0461 | 4.6% |
| `gas` | 0.0 | -4.0 | 0.0183 | 0.0183 ÷ 1.0792 | 0.0170 | 1.7% |
| `light` | -0.5 | -4.5 | 0.0111 | 0.0111 ÷ 1.0792 | 0.0103 | 1.0% |
| **Σ** | | | **1.0792** | | **1.0000** | **100.0%** |

Step 2 is in the film because it is what real implementations do — `exp(z)` overflows for
large `z`, and `exp(z−m)/Σexp(z−m) = exp(z)/Σexp(z)` exactly. `verify_softmax.py` asserts
both forms agree to 1e-12.

The answer key is one-hot on `cheese` — because `cheese` is the token that
followed in the text. `rock`, which is true of the actual moon, gets the same hard
zero as `gas` and `light`.

- **Penalty incurred:** `L = −ln p(cheese) = −ln 0.0461 = 3.0762` nats
- **Same weights, true corpus:** `L = −ln p(rock) = 0.0762` nats
- **Exact identity:** `3.0762 − 0.0762 = 3.0 = z(rock) − z(cheese)` — the penalty *is* the ranking gap

**The contrast beat is what makes "not the truth" a mechanism rather than an assertion.**
Hold the model fixed and swap only the corpus — `"The moon is made of green cheese"` becomes
`"The moon is made of grey rock"` — and the answer key moves from `cheese` to `rock`. If
the target tracked truth, those two columns would be identical. They are not.

**Academic honesty.** The two corpus lines, the four-token vocabulary and the four logits
are **constructed teaching values** — invented to make the arithmetic legible, never
measured from a trained model. Every beat that displays a figure carries an on-screen
`CONSTRUCTED EXAMPLE` banner, on all nine of them, not just once. The arithmetic is exact:
`verify_softmax.py --emit` computes it and writes `softmax_values.json`, and
`build_beat_sheet.py` builds every scene prop from that file, so **no number on screen is
hand-typed.**

**The boundary the reel states out loud (beat B10, 34.1s of screen time).** This does
**not** establish how post-training — preference tuning, RLHF — later steers the model
away from corpus mimicry toward factual accuracy; that is a separate, later mechanism with
a different target, and none of it appears here. It does not establish that models must
end up wrong. And it establishes nothing measured.

---

## Rebuild instructions

Prerequisites: `python3` ≥ 3.10 (3.12 used here), `ffmpeg`, Node ≥ 20. No API keys —
Kokoro TTS ships inside the toolkit and costs $0.00.

```bash
git clone https://github.com/nikbearbrown/brutalist.art
cd brutalist.art && ./setup --install && ./art doctor
```

Copy the components in (`components/` → `runtime/remotion/src/scenes/`) and register them
per `components/README.md` — each needs the `calculateMetadata` hook. Then:

```bash
export ART_HOME="$PWD"
source /path/to/.venv/bin/activate                        # see FRICTIONAL.md #2
python3 <REEL>/verify_softmax.py --emit                   # prove, then emit the figures
python3 <REEL>/build_beat_sheet.py                        # beat sheet FROM those figures
python3 runtime/scripts/generate_audio_kokoro.py <REEL>   # audio = the master clock
#   then append the hook's guess pause and re-measure — LAST audio step, see BUILD-PROMPT.md
python3 runtime/scripts/remotion_scenes.py <REEL> --force
./art run   <REEL>                                        # GATE F / L / V
./art final <REEL>                                        # verified master
python3 runtime/scripts/align.py <REEL> --model base      # word clock
python3 <REEL>/make_captions.py                           # captions
ffprobe -v error -show_entries format=duration -of csv=p=0 <REEL>/<slug>.mp4
```

**Ordering rule:** `generate_audio_kokoro.py` regenerates every beat unconditionally and
`mp3/timings.json` is a cache it trusts over the real files, so the guess pause is applied
*after* the last audio run and the clock is written once from one `mutagen` measurement.
Re-running audio generation silently reverts the pause. Never fix timing by hand
otherwise — cut words, regenerate, recompile.

## Files

| File | What it is |
|---|---|
| `beat_sheet.json` | 12 beats, 6 acts — narration, measured durations, `show` blocks, scene props |
| `verify_softmax.py` | Runnable proof of all five softmax steps; `--emit` writes `softmax_values.json` |
| `softmax_values.json` | The verified figures. Generated, never edited |
| `build_beat_sheet.py` | Builds the beat sheet from the verified figures — no number hand-typed |
| `make_captions.py` | Rebuilds the `.srt` from the word clock; asserts no word is dropped |
| `ch1-token-that-followed.srt` | Captions — every narration word, real word-level timings |
| `BUILD-PROMPT.md` | The exact commands and prompts, both revisions |
| `SOURCES.md` | Attribution — what Claude contributed, Kokoro, faster-whisper, the toolkit |
| `FRICTIONAL.md` | Tool-execution log and 25 friction points, incl. the runtime-floor entry |
| `BUILD-LOG.md` | Gate record, Gate V defect log, justified deviations |
| `CHECKS-REPORT.md` | Beat classification and teaching-arc gate |
| `FACTCHECK.md` | Every narrated claim, with a verdict and source |
| `SHOTLIST.md` / `PROMPTS.md` | Typed work order · beat-prefixed prompts |
| `components/` | `Ch1Chrome` chassis + the Ch1Pretrain* scenes, with install notes |
| `mp3/` | Per-beat narration (the master clock) + `words.json`, the aligned word clock |
| `_qc/` | Gate V report and contact sheet |
