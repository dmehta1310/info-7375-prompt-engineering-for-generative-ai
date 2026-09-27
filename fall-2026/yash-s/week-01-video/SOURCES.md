# SOURCES — Repeatable is not the same as true

## What was run

| Source | What it contributed | Licence / note |
|---|---|---|
| `lessons/01-randomness-and-first-prompts/code/main.py` | Unmodified `sample()`. Seed 7 twice: `{0: 102, 1: 268, 2: 630}`. Seed 99: `{0: 93, 1: 267, 2: 640}`. | Course code. Not edited. |
| Python 3.13.5 on this machine | The interpreter those counts were printed with, 2026-09-25 and again 2026-09-26. | Local runtime. |
| `brutalist.art` `6a8380a` | Kokoro, Remotion, `./art final`. | Public toolkit. Local scene edits are in `components/`. |
| Kokoro `af_bella` | Synthetic narration. Not a recording of me. | Local model, free path. |

No stock footage, no paid generator, no Claude chat screenshot.

## What I made

The choice of concept, the decision to show seed 7 twice and seed 99 once, and the limit stated on screen: one seed, one machine, right now. Not a claim about other Python versions or other operating systems.

## What Claude contributed

Claude Code, 2026-09-25, drafted the beat sheet, narration, `FACTCHECK.md`, and the first renders. That session stopped when the organization spend limit hit, with the type check still failing.

Claude in Cursor, 2026-09-26, measured the failing frames, edited the three scene files, re-rendered, and ran `./art final`. It also drafted this file, `README.md`, `BUILD-PROMPT.md`, and `FRICTIONAL.md` from the commands and outputs of that session.

I still have to be able to explain the video without the script. The counts are a property of `random.Random(seed)` in this `sample()`, not a proof that a model's answer is true.

## Constructed, and labelled on screen

B02's card is a diagram of the mechanism, not a screenshot of `main.py`. The line on screen is: "Diagram — illustrative, not literal source code."

## Third-party assets

None beyond the toolkit fonts and Kokoro voice already named above.
