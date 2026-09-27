# SHOTLIST — week-01-shifted-not-changed
## Total: 3:16 (195.72s) · 11 beats · 0 slates · 0 pantry slots

Typed work order. Durations are **measured** from the Kokoro mp3s (audio is the master
clock), not estimated. Every beat renders natively in this environment — there is no
media to source, no slate to fill, and no human-supplied asset.

| Beat | Act | Lane | Medium | Source/Pattern | Duration | Notes |
|---|---|---|---|---|---:|---|
| B00 | ASK | bookend | REMOTION | `ShiftComposer` *(wraps toolkit composer)* | 20.18s | Cold open. Greeting "Namaste, Suketh"; pill **RECONSTRUCTED INTERFACE · NOT A CLAUDE TRANSCRIPT**; **no answer lines** — the film answers the question |
| B01 | BLUF | bookend | REMOTION | `BrutalistHesitantWriter` | 16.36s | Exec summary. `stable` → `overflow-safe` (single-token trigger — a phrase never matches); seed `shifted-not-changed-b01`; `charMs: 8` so the overview completes at 8.0s, well before the cut; ≥9s law satisfied |
| B02 | THE BREAK | body | REMOTION | `ShiftOverflow` *(reel-local)* | 20.67s | Exponent axis; ceiling tick at 709.78; terracotta bar runs past the axis end; real `OverflowError` card stamps |
| B03 | THE MOVE | body | REMOTION | `ShiftPipeline` *(reel-local)* | 19.61s | **The core beat.** 4 columns reveal L→R; outcome 2's `0` and `1.0` are the one terracotta moment; TOTAL rules off under weights |
| B04 | THE PROOF | body | REMOTION | `ShiftCancellation` *(reel-local)* | 18.69s | Fraction re-forms as a product; both copies of `exp(−m/T)` strike through on the spoken "cancels"; spark line at top (bottom collided with the verdict band) |
| B05 | ASK | body | REMOTION | `ShiftComposer` *(reel-local wrapper)* | 9.56s | The question the evidence script answers, with the disclosure pill; opens with the command **already typed** (`preTyped` — inner beat); the result is B06, a recorded script run, not a Claude response |
| B06 | THE RECEIPT | body | REMOTION | `ShiftReceipt` *(reel-local)* | 20.63s | Two 62-char vectors aligned; indices 19 and 60 turn terracotta; `1.1102230246251565e-16` scales to 104px, glossed `exactly 2**-53 — adjacent floats, one step apart`. From "adjacent" to "indistinguishable" (≈ 6 s) the agreeing digits step back and a `1 ULP` marker sits between each differing pair — the change asked for after watching (REVIEW.md Round 10) |
| B07 | THE BOUNDARY | body | REMOTION | `ShiftBoundary` *(reel-local)* | 20.57s | Descending rail −700 → −800; the `0.0` at −746 goes terracotta and a cliff line draws across the table |
| B08 | VERDICT | bookend | REMOTION | `ClaudeVerdictArtifact` | 21.40s | Artifact page — UI earns it, the verdict IS the subject. 4 lines: GUARANTEED / UNCHANGED / MEASURED / NOT ESTABLISHED |
| B09 | HANDOFF | bookend | REMOTION | `ShiftComposer` | 18.92s | Greeting `Your turn.`; pill **SUGGESTED PROMPT · NOT YET RUN**; prompt read aloud verbatim then discussed |
| B10 | OUTRO | bookend | REMOTION | `ShiftOutro` *(reel-local)* | 9.13s | Title restate + terracotta period; author + course; synthetic-narration disclosure on the card |

## Lane histogram

```
REMOTION (toolkit)   2 beats   B01 B08                  37.76s   19%
REMOTION (wrapped)   3 beats   B00 B05 B09              48.66s   25%   toolkit composer inside ShiftComposer
REMOTION (reel)      6 beats   B02 B03 B04 B06 B07 B10 109.30s   56%
MANIM                0 beats   — blocked in this environment and not called
VOX / STILL          0 beats   — no pantry, no Ken Burns, no archival
USER-CAPTURE         0 beats   — no screen recordings (REBUILD LAW)
SLATE                0 beats   — nothing punted, nothing unfilled
```

## Typing budget (HANDOFF LAW)

Typing appears in **exactly three** beats, each for a different reason:

- **B00** — the *ask*
- **B01** — the *overview being thought through* (the hesitation is the pedagogy)
- **B09** — the *viewer's prompt*

Inner beats show no typing. B05 is a composer beat but shows the command already typed —
true since 2026-09-24; until then it typed, because the toolkit composer always does
(`SOURCES.md` §5.18).

## ILLUSTRATE LAW — UI vs illustration

| Beat | Surface | Why it is legal |
|---|---|---|
| B00 | Claude UI | Cold open — the law's first named exemption |
| B05 | Claude UI | Ask micro-beat of an ask→result pair |
| B08 | Claude UI | Verdict artifact page |
| B09 | Claude UI | Handoff |
| B02, B03, B04, B06, B07 | Illustration | Each illustrates its own concept, no interface present |
| B10 | Own outro card | Title restate |

No two consecutive beats share a visual scheme. The longest UI run is one beat.

## Work order — what was built, in order

1. `evidence/verify_claims.py` → `evidence/run-output.txt` (all numbers fixed before any authoring)
2. GATE L search → genuine miss → 6 components in `runtime/remotion/src/ShiftedNotChanged.tsx` (a 7th, `ShiftComposer`, added 2026-09-24)
3. Register in `Root.tsx` under folder `ShiftedNotChanged`; `./art scene-index` (610 → 616; 617 with `ShiftComposer`)
4. `beat_sheet.json` — SHOW blocks authored before narration (SHOW-DON'T-TELL LAW)
5. `generate_audio_kokoro.py` → 11 mp3s, `actual_duration_s` written back
6. `CHECKS-REPORT.md` (PROOF GATE), then this file + `FACTCHECK.md` + `PROMPTS.md` (GATE F)
7. `./art run` → review cut → visual QC → `./art final`

## Open slots

**None.** Nothing in this reel requires a human-supplied asset, a generated image, or a
paid service. If a beat had needed one it would appear here with its window and tier; the
list is empty by design, not by omission.
