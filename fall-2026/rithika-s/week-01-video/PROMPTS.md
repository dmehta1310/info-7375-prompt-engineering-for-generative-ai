# PROMPTS — "The Token That Followed"

Beat-prefixed prompts for the **2026-09-23 six-act cut**.

**There are no open slots and no Claude-interface beats in this cut.** Nothing here is a
request for media from a human or a paid engine, and — unlike the previous cut — no beat
displays a Claude reply. The standing constraint is that any Claude response shown must be
a real one, actually obtained and dated; rather than stage one, this cut shows none
(`FRICTIONAL.md` #25).

## The prompt that chose the numbers

The only generative step in the build was selecting logits whose displayed probabilities
sum to exactly 1.0:

> Pick four candidate tokens and four clean logits such that the 4-dp softmax
> probabilities sum to exactly 1.0. Compute the full five-step pipeline — raw logits,
> subtract the max, exponentiate, normalize, probabilities — plus the cross-entropy against
> a one-hot target. Assert every displayed figure, and assert that max-subtraction is
> identical to the naive softmax.

Answered by grid-searching half-integer logits: 35 sets satisfy the constraint, and the
cleanest — `rock 4.0 / cheese 1.0 / gas 0.0 / light −0.5` — was taken. It has the added
property that `z − max` lands on round numbers (0, −3, −4, −4.5), which is what makes step
2 readable on screen. The search is reproducible; `verify_softmax.py` is the gate.

## Regeneration, per beat

Each scene is driven entirely by props built from `softmax_values.json`, so the "prompt"
for a beat is its scene plus its props. Regenerate one with:

```bash
python3 runtime/scripts/remotion_scenes.py <REEL> --only <BEAT> --force
```

- **B00** (HOOK) → `Ch1PretrainHook` — The false claim, as plain English (14.45s)
- **B01** (MECHANISM) → `Ch1PretrainCorpus` — Text → tokens → the next-token question (20.57s)
- **B02** (MECHANISM) → `Ch1PretrainTarget` — The answer key: one on cheese, zero on rock (23.28s)
- **B03** (MECHANISM) → `Ch1PretrainLadder` step 1 — Step 1 — the raw scores (20.04s)
- **B04** (MECHANISM) → `Ch1PretrainLadder` step 2 — Step 2 — subtract the largest score (22.22s)
- **B05** (MECHANISM) → `Ch1PretrainLadder` step 3 — Step 3 — exponentiate (21.77s)
- **B06** (MECHANISM) → `Ch1PretrainLadder` step 4 — Step 4 — divide by the sum (20.62s)
- **B07** (MECHANISM) → `Ch1PretrainLadder` step 5 — Step 5 — the probabilities, summing to exactly 1 (21.77s)
- **B08** (CONTRAST) → `Ch1PretrainContrast` — Same model, two corpora, two answer keys (25.44s)
- **B09** (LOSS) → `Ch1PretrainLoss` — The penalty reads one slot (20.33s)
- **B10** (BOUNDARY) → `Ch1PretrainBoundary` — What this does not establish (34.06s)
- **B11** (TAKEAWAY) → `Ch1PretrainTakeaway` — One sentence, no new claims (9.31s)

## The ladder is one component, five times

`Ch1PretrainLadder` renders all five softmax steps; the beat sheet varies only `step`
(1..5) and `stepNote`. That is deliberate — the viewer sees the same four tokens gaining
exactly one column per beat, so the columns they already understand stay on screen as the
ground the next one is built on.

| Beat | step | Column introduced |
|---|---|---|
| B03 | 1 | Step 1 — the raw scores |
| B04 | 2 | Step 2 — subtract the largest score |
| B05 | 3 | Step 3 — exponentiate |
| B06 | 4 | Step 4 — divide by the sum |
| B07 | 5 | Step 5 — the probabilities, summing to exactly 1 |

## The guess pause

B00 carries 3.5s of appended silence so the viewer can answer the hook's question before
the answer appears. It is applied with `ffmpeg -af "apad=pad_dur=3.5"` as the **last**
audio step and then re-measured, so the hold is part of the measured clock rather than an
illusion in the edit. Re-running `generate_audio_kokoro.py` destroys it
(`FRICTIONAL.md` #22–#24).
