# SHOTLIST — claude-liam-expected-vs-observed

1920×1080 · 30fps · 10 beats · 147.24s (2:27)
Palette: Claude fidelity — cream `#FAF9F5`, stage `#F2F0E9`, ink `#3D3929`,
terracotta `#D97757` as the ONE accent per beat.
All durations are measured Kokoro audio, not estimates.

| # | Beat | s | Composition | Stage | The one accent |
|---|---|--:|---|---|---|
| 1 | B00 ASK | 14.87 | `ClaudeComposerAsk` | Claude composer, cream | send button + spark |
| 2 | B01 BLUF | 10.69 | `BrutalistHesitantWriter` | bare cream page | the doomed word `proof` |
| 3 | B02 SOURCE | 14.87 | `SoftmaxInOneBeat` | illustration stage | final cell `0.6652` |
| 4 | B03 EXPECTED | 15.66 | `ExpectedCount` | illustration stage | the `665.24` counter |
| 5 | B04 OBSERVED | 13.97 | `ObservedCounts` | illustration stage | bar `[2]` = 630 |
| 6 | B05 GAP | 15.66 | `TheGap` | illustration stage | the filled span + `35.24` |
| 7 | B06 FALSIFIABILITY | 19.41 | `WhatWouldSettleIt` | illustration stage, two panels | `630` tail bar + `NOT RUN` rule |
| 8 | B07 VERDICT | 18.75 | `ClaudeWindow` (artifact) | Claude window | the NOT-ESTABLISHED line |
| 9 | B08 HANDOFF | 20.33 | `ClaudeComposerAsk` | Claude composer | send button + spark |
| 10 | B09 OUTRO | 3.03 | `ClaudeTitleOutro` | poster card | the terracotta period |

---

## Per-beat stage directions

Full `show` event lists (with fractional cue points) live in `beat_sheet.json`
under each beat's `shot.show`. Summary:

**B00 — cold open.** Serif greeting `Namaste, Liam` above the composer. The ask
types itself; send arms; `running main.py…`; three result lines land. The cold
open lands answered (ASK→RESULT begins here).

**B01 — the executive summary, written.** Four lines type with hesitation. The
writer commits to `proof`, pauses, deletes it character by character, and types
`unusual`. `lead_silence_s: 0.8`. Seed `expected-observed-b01` — same
performance every render.

**B02 — where 0.6652 comes from.** Four rows of three mono cells, each row
sliding in: scores → peak-subtracted → exponentiated → normalised. A divisor
rule draws under row 3. Only the last cell takes terracotta. Footer: *this video
uses **one** of these numbers* — the scope handoff, on screen.

**B03 — one multiplication.** `0.6652409557748218` at full printed precision,
`× 1000 draws`, a rule, then a counter spinning to `665.24`. The wrong framing
(*what this run will do*) is struck through and replaced by *the average over
many runs* on the spoken word.

**B04 — what actually ran.** Verbatim JSON block at left in printed key order
(`1, 2, 0`), bars at right growing to 102 / 268 / 630 as each is spoken, labelled
`[0] [1] [2]`. A dashed rule drops at 665.24; the terracotta bar visibly stops
short of it. Plot scaled to 700 so the rule sits inside the frame.

**B05 — the gap. CONSTRUCTED.** `CONSTRUCTED ILLUSTRATION` chip present from
frame 1, never removed. Number line 600→700; marks at 630 and 665.24; the span
between fills terracotta; `35.24` counts up; then *5.3% below expected, ≈2.4
standard deviations*. Footnote: *numbers real · diagram authored for this video*.

**B06 — what would settle it.** Two panels. Left: one tick at 630, *Can this
refute 0.6652?*, `NO` stamp, and *one seed, read after the fact — a reason to
test, not a verdict*. Right: a seeded spread accumulating, with 630 marked at
**bin 3 — the left tail, its true position at z = −2.36** — captioned *in the
tail — about 1 run in 50, not mid-pack*. The right panel then dims to 45% under
a terracotta rule reading `NOT RUN IN THIS VIDEO`.

**B07 — verdict artifact.** Claude window, artifact view. Four lines land in
sequence; the fourth — the NOT-ESTABLISHED boundary — lands in terracotta.

**B08 — handoff.** Composer returns, greeting `Your turn.` (persona dropped).
The prompt types itself verbatim as it is read aloud, then two lines on what to
look for in the answer.

**B09 — outro.** Title restate, `@NikBearBrown`, slug-seeded mascot.
PIXEL-ART LAW: `nod` is foot-anchored scaleY — translation and axis-aligned
scale only, zero rotation.

---

## Typing discipline

Typing appears in exactly three beats, each for a different reason:
**B00** = the ask · **B01** = the overview being thought through ·
**B08** = the viewer's prompt. B02–B07 show values already resolved.

## Honesty labels that must stay legible in QC

- B05 `CONSTRUCTED ILLUSTRATION` — full duration
- B06 `NOT RUN IN THIS VIDEO` — from 82% of the beat to the cut
- B07 the `NOT ESTABLISHED:` line

If any of these is clipped or unreadable in sampled frames, the build has failed
the assignment, not merely QC.
