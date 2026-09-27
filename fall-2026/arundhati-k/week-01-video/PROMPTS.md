# PROMPTS — claude-liam-expected-vs-observed

Generation inputs for this reel. **No paid generation service was used.** There
are no image, video, or voice prompts to log, because every visual is a
deterministic Remotion composition and all narration is local Kokoro TTS.
What follows is what actually produced the film.

---

## 1. Media generation: none

| Channel | Used | Note |
|---|---|---|
| Higgsfield / AI video | ✗ | CLI absent; free path ran silently, as designed |
| Text-to-image | ✗ | REBUILD LAW — every figure is a native animated component |
| Stock / archival | ✗ | nothing in this reel needs a photograph |
| Paid TTS | ✗ | Kokoro `am_onyx`, local, `cost $0.00` |

**Total spend: $0.00.**

There is no pantry shopping list and no human-capture request. Under the HOLD vs
PUNT rule, a HOLD requires a genuine photograph of a real person, place, or
event; nothing here qualifies, so every beat is authored.

---

## 2. Narration prompts: none — narration is authored, not generated

Every `narration_text` in `beat_sheet.json` is written, fact-checked against
`main.py` (see `FACTCHECK.md`), and then synthesised verbatim by Kokoro. The
text was not model-generated at synthesis time; the TTS step is a reading, not a
writing.

```bash
.venv/bin/python runtime/scripts/generate_audio_kokoro.py <REEL>   # am_onyx
```

---

## 3. Component generation prompts

The five body compositions in
`runtime/remotion/src/scenes/ExpectedObserved.tsx` were written with Claude Code
against the toolkit's `illustrations/kit.tsx` primitives. The governing
instruction, in substance:

> Write five Remotion components for a 1920×1080 Claude-skin reel, using
> `useP()` as the only clock — no timers, no CSS transitions, no `Math.random()`,
> so every render is identical. Each wraps in `<IlluStage spark="…">`, keeps
> everything essential inside `SAFE`, and carries exactly ONE terracotta accent.
>
> Every numeric constant must come from `main.py`'s actual printed output, held
> in a single `REAL` object with the verification date and the derivation of
> each value in a comment. Do not round on screen beyond what the beat needs.
>
> `TheGap` must carry a `CONSTRUCTED ILLUSTRATION` label for its entire
> duration. `WhatWouldSettleIt` draws an experiment that was **not performed** —
> generate its spread from a seeded hash, dim it to 45%, and caption it
> `NOT RUN IN THIS VIDEO`. Neither may be capable of reading as collected data.

The ASK→RESULT pairs in the film (B00, B08) show prompts typed into the Claude
composer. Those are the *viewer-facing* prompts and are reproduced verbatim in
`beat_sheet.json` under each beat's `shot.remotion.props.command`:

- **B00** — the question the reel answers, ending *"Is the probability wrong?"*
- **B08** — the handoff experiment: run `sample([1,2,3])` 100 times with 100
  seeds, 1000 draws each, plot the distribution of the count for index 2, and
  mark where 630 falls.

Neither beat displays a Claude *response*. B00's three output lines are findings
the video itself proves in later beats, not a transcript.

---

## 4. Determinism

| Seed | Where | Effect |
|---|---|---|
| `7` | `main.py` `sample()` | the run the video reports |
| `expected-observed-b01` | `BrutalistHesitantWriter` | identical typing performance every render |
| `claude-liam-expected-vs-observed` | `ClaudeTitleOutro` | slug-seeded mascot |
| `sin(i·12.9898+78.233)·43758.5453` | `WhatWouldSettleIt` | seeded schematic spread; `Math.random()` is never called |

Re-running the full build from a clean clone reproduces the same frames.
