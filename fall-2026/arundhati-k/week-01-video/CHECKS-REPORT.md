# CHECKS-REPORT.md — claude-liam-expected-vs-observed

Written **before** the first slate compiled, per the PROOF GATE.
Date: 2026-09-26 · Author: Arundhati Kandelkar

---

## Classification

```
9 SHOW / 1 justified-HOLD / 0 PUNT-flagged
```

| Beat | Act | Class | Artifact named in `shot.show` |
|---|---|---|---|
| B00 | ASK | SHOW | Composer types the ask; send arms; three result lines land |
| B01 | BLUF | SHOW | Writer types, deletes `broken`, types `normal` |
| B02 | SOURCE | SHOW | Four rows transform logits → probabilities |
| B03 | EXPECTED | SHOW | Counter spins to 665.24; caption strikes through and replaces |
| B04 | OBSERVED | SHOW | Three bars grow to 102 / 268 / 630; dashed rule at 665.24 |
| B05 | GAP | SHOW | Number line; span fills; 35.24 counts up |
| B06 | FALSIFIABILITY | SHOW | One tick vs an accumulating spread; right panel dims |
| B07 | VERDICT | **HOLD** | Artifact page; four lines land in sequence |
| B08 | HANDOFF | SHOW | Prompt types itself verbatim as it is read |
| B09 | OUTRO | SHOW | Title restates; mascot performs (translation + scaleY only) |

**The one HOLD, justified.** B07 is the sanctioned verdict artifact page. Its
four lines land on spoken cues, but I am not going to claim that clears the PPT
test — a staggered text reveal is close to a slide, and calling it SHOW would be
inflating my own report. It is held deliberately for three reasons: the spine
(`cold open → BLUF → body → verdict page → HANDOFF → outro`) requires a verdict
beat; ILLUSTRATE LAW names the verdict artifact page as one of the five places
the Claude UI is legally the subject; and the assignment requires the boundary
statement to be read plainly rather than dramatised. It is not adjacent to
another UI beat — B06 (illustration) precedes it and B08 is separated from it by
a full act — so the two-consecutive-slides failure does not arise.

---

## Teaching arc

```
Teaching arc: FRAMEWORK ✓ | WORKED EXAMPLE ✓ | FALSIFIABILITY ✓
              SCAFFOLDED TASK ✓ | BOOKENDS ✓ | NO-SOURCE-NO-VERDICT ✓
```

- **FRAMEWORK before examples ✓** — B01 states the whole idea in one breath
  (expect ≠ observe, and that is not a defect) before any specific number is
  worked. B02 then sources the single input the worked example needs.
- **WORKED EXAMPLE ✓** — B03–B05 is one continuous worked example on real
  numbers: 0.6652 × 1000 = 665.24, observed 630, gap 35.24 (≈5.3%). Every figure
  is recomputed from `main.py`'s printed output, not transcribed by hand.
- **FALSIFIABILITY ✓** — B06 states what would actually settle the question
  (many runs, and whether 630 sits inside the expected spread) and says plainly
  that this video does not do it. B07 restates the boundary as an unhedged line.
- **SCAFFOLDED TASK ✓** — B08 hands the viewer the *specific* experiment B06
  named as missing, as a runnable prompt, read aloud verbatim and then discussed
  (what to look for: the spread, not the single number).
- **BOOKENDS ✓** — four: B00 cold open on the composer with its RESULT lines,
  B01 hesitant-writer BLUF, B08 handoff, B09 title-restate outro.
- **NO-SOURCE-NO-VERDICT ✓** — every claim in the B07 verdict traces to a beat
  that showed its source: 665.24 ← B03, 630 ← B04, the gap ← B05, the
  not-established line ← B06.

---

## Legibility contract (SHOW/HOLD claim beats)

- Every beat names its on-screen artifact in `shot.show`. ✓
- Negative space held at ~15–35% by `fitToSafe(…, target=0.92)`; to be confirmed
  against real frames in `_qc/REPORT.md`, not assumed here.
- Un-highlighted elements never below ~40% opacity. The only deliberate dim is
  B06's right panel at **45%**, above the floor. ✓
- Comparisons held ≥2s: B04's bar-vs-665.24 rule occupies the last ~5.6s of a
  13.97s beat; B06's two panels are co-present for ~6s of 16.87s. ✓

---

## Typing discipline (HANDOFF LAW)

Typing appears in exactly three beats, each for a different reason:
B00 = the *ask*; B01 = the *overview being thought through*; B08 = the *viewer's
prompt*. No inner beat types — B02–B06 show values already resolved.

---

## Measured audio (ground truth, not estimates)

| Beat | s | Beat | s |
|---|---:|---|---:|
| B00 | 14.87 | B05 | 13.91 |
| B01 | 10.43 | B06 | 16.87 |
| B02 | 14.87 | B07 | 17.75 |
| B03 | 15.66 | B08 | 20.33 |
| B04 | 13.97 | B09 | 3.03 |

**Total 141.14s — 2:21.** Inside the assignment's 2–4 minute target.
B01 = 10.43s, clearing the EXECUTIVE-SUMMARY LAW floor of ≥9s audio / ≥8s media.

**Known risk, carried into QC:** B09 at 3.03s is a short window for a
title-restate plus a mascot performance. Flagged here rather than discovered
later; to be checked on real frames and fixed by lengthening the outro line if
the card has no time to land.

---

## Violations

None outstanding. One design constraint was forced by a toolkit defect rather
than chosen, and is logged in `FRICTIONAL.md` and in B01's `authoring_note`:
`BrutalistHesitantWriter` matches trigger words per whitespace token
(`BrutalistHesitantWriter.tsx:133`), so the multi-word phrase correction that
the ai-explainer SKILL.md's own worked example demonstrates cannot match. B01
uses a single-word correction (`broken` → `normal`) that still flips the whole
sentence, which is what the law actually requires.

---

## AMENDMENT — 2026-09-26, after GATE F

The report above was written before the first render, as the PROOF GATE
requires. Two things changed afterwards, and I am appending rather than editing
the original so the sequence stays visible.

**1. Four beats were re-authored.** GATE F fact-checking found that the reel's
central characterisation of the gap was wrong: I had called 630 an *ordinary*
sampling result, and it is not — z = −2.36, P(X≤630) = 1.04%, about 1 run in 50.
B01, B05, B06 and B07 were rewritten and re-rendered. Full detail and the
before/after table are in `FACTCHECK.md`. The concept and the beat
classifications are unchanged; the claim is now correct.

**B01's correction changed with it:** `broken → normal` became
`proof → unusual`. The replacement word had to become *true*, not merely
opposite.

**2. Final measured audio** (the earlier table is superseded):

| Beat | s | Beat | s |
|---|---:|---|---:|
| B00 | 14.87 | B05 | 15.66 |
| B01 | 10.69 | B06 | 19.41 |
| B02 | 14.87 | B07 | 18.75 |
| B03 | 15.66 | B08 | 20.33 |
| B04 | 13.97 | B09 | 3.03 |

**Total 147.24s — 2:27.** Still inside the 2–4 minute target. B01 = 10.69s,
clearing the EXECUTIVE-SUMMARY LAW floor; its media measures 10.7s and the
correction is fully on screen by ~9.0s, holding for the final 1.7s (verified on
extracted frames, not assumed).

**Outcome of the gates:** GATE T **PASS** (0 FAILs) · GATE V **clean**
(0 BLOCKER, 0 MAJOR, 20 frames sampled). The B09 risk flagged above — 3.03s for
the outro card — was inspected in the contact sheet and the title restate,
handle and mascot all land; no fix needed.
