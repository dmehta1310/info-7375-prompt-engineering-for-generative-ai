# SOURCES.md — Expected, Observed

Arundhati Kandelkar · INFO 7375 Week 1 · 2026-09-26

---

## 1. The numbers on screen

Every figure in the video comes from one file, run unmodified:

**`lessons/01-randomness-and-first-prompts/code/main.py`**
(nikbearbrown/info-7375-prompt-engineering-for-generative-ai, unmodified clone)

```bash
python3 lessons/01-randomness-and-first-prompts/code/main.py
```

Verified output, 2026-09-26:

```json
{
  "probabilities": [0.09003057317038046, 0.24472847105479764, 0.6652409557748218],
  "counts": { "1": 268, "2": 630, "0": 102 }
}
```

Defaults that make this reproducible, read from the source rather than assumed:
`sample(logits, count=1000, seed=7, temperature=1.0)`, logits `[1, 2, 3]`.

### Derived numbers — recomputed, not hand-estimated

| On screen | How it was obtained | Value |
|---|---|---|
| `665.24` | `0.6652409557748218 × 1000` | 665.2409557748218 |
| `35.24` | `665.2409557748218 − 630` | 35.2409557748218 |
| `5.3%` | `35.2409557748218 / 665.2409557748218 × 100` | 5.297% |
| `≈2.4 sd` | `35.2409557748218 / sqrt(1000·p·(1−p))` = 35.241/14.9230 | 2.3615 |
| `about 1 run in 50` | two-tailed `2 × P(X≤630)`, X~Binomial(1000, p) | 2.073% ≈ 1/48 |
| `0.1353 · 0.3679 · 1.0000` | `exp(−2)`, `exp(−1)`, `exp(0)` | 0.13533, 0.36788, 1.0 |
| `1.5032` | sum of the three exponentials | 1.50321 |
| `0.0900 · 0.2447 · 0.6652` | the printed probabilities, rounded to 4dp | — |

All recomputed in Python against the live module rather than transcribed, so the
video's arithmetic cannot drift from the code. The one rounding on screen is
4 decimal places in B02; B03 shows the probability at full printed precision.

---

## 2. What I made

- `beat_sheet.json` — narration, `show` blocks, scene routing.
- `runtime/remotion/src/scenes/ExpectedObserved.tsx` — five original Remotion
  components (`SoftmaxInOneBeat`, `ExpectedCount`, `ObservedCounts`, `TheGap`,
  `WhatWouldSettleIt`), written for this reel against the toolkit's
  `illustrations/kit.tsx` primitives (`useP`, `remap`, `ease`, `IlluStage`).
- Registration of those five compositions in `runtime/remotion/src/Root.tsx`.
- `CHECKS-REPORT.md`, `FRICTIONAL.md`, `BUILD-PROMPT.md`, this file.

### Determinism / seeds

| Seed | Where | Why |
|---|---|---|
| `7` | `main.py` `sample()` default | the run the video reports |
| `expected-observed-b01` | `BrutalistHesitantWriter` | same typing performance every render |
| `claude-liam-expected-vs-observed` | `ClaudeTitleOutro` slug | slug-seeded mascot choice |
| `hash01(i)` — `sin(i·12.9898+78.233)·43758.5453` | `WhatWouldSettleIt` | seeded spread; `Math.random()` is never called, so renders are identical |

---

## 3. Constructed and schematic material — declared

The assignment requires constructed illustrations to be labelled as constructed.
Two beats qualify, and both carry the label on screen, not only here.

**B05 `TheGap`** — labelled **CONSTRUCTED ILLUSTRATION** from frame 1 for the
beat's full 15.66s, plus a footnote reading *numbers real · diagram authored for
this video*. The two plotted values (630, 665.24) are real; the number line,
spacing and fill are mine.

**B06 `WhatWouldSettleIt`** — the right-hand panel draws a spread of repeated
runs **that were not performed**. It is generated from the seeded `hash01`
function above, dimmed to 45%, and captioned **NOT RUN IN THIS VIDEO** in
terracotta. It is a picture of an experiment I am recommending, never data I
collected.

**No Claude conversation appears in this video.** B00 and B08 show a prompt
being *typed into* a composer; neither claims to show a response. B00's three
output lines are the findings the video itself demonstrates, and each is proved
on screen in a later beat. Because no Claude response is displayed, the
assignment's "real response, with the date" requirement does not arise — I chose
not to show one rather than stage one.

---

## 4. Third-party assets and licences

| Asset | Source | Licence |
|---|---|---|
| Brutalist toolkit (Remotion scenes, Kokoro pipeline, `art` CLI) | `nikbearbrown/brutalist.art` | per repo |
| Kokoro TTS v1.0 (`am_onyx`), local ONNX | bundled via `./setup` | local, free, no account |
| EB Garamond | bundled in `runtime/fonts` | SIL Open Font License |
| Course code + lesson text | `nikbearbrown/info-7375-…` | per repo LICENSE |
| Remotion | `remotion.dev` | free for individuals / small teams |

No paid API was called. No media account was used. Total spend: **$0.00**
(the Kokoro step reports `cost $0.00`).

---

## 5. What Claude contributed

Claude Code (Opus 5) was used throughout. Naming the tool is not the disclosure;
the disposition is.

**Accepted.**
- Running `main.py` and cross-checking every derived figure against the live
  module. Verifiable by re-running, which is why I accepted it.
- Reading the 790-line `ai-explainer` SKILL.md and extracting the binding laws
  (cold open, executive summary, ILLUSTRATE, HANDOFF, OUTRO-LOCK, PROOF GATE).
- Running GATE L `./art scenes --check` before authoring. This caught that
  `ClaudeCallout` has no `<Composition>` in `Root.tsx` and that my first
  registration attempt — five compositions generated by `.map()` — was invisible
  to the static index parser. Both would have cost me a render cycle.
- Drafting the five Remotion components and the narration.

**Changed.**
- It first proposed writing a multi-word phrase correction into
  `BrutalistHesitantWriter`, following the SKILL.md's own worked example. I had
  it read the component instead: line 133 matches triggers per whitespace token,
  so multi-word triggers silently never fire. Changed to a single-word
  correction that still flips the sentence. (It became `proof` → `unusual` after the
  statistical correction in §7 — the replacement word had to be *true*, not just opposite.)
- Its first `WhatWouldSettleIt` draft drew the repeated-runs panel as an
  ordinary chart. I had it dimmed and captioned `NOT RUN IN THIS VIDEO`, because
  a clean histogram of an experiment I never ran is exactly the fabrication this
  chapter is about.

**Rejected.**
- It proposed installing KaTeX into the toolkit's Remotion runtime to typeset a
  general softmax formula, and recommended that as the default. I rejected it.
  The formula was only needed because the beat sheet spent ~50 seconds deriving
  softmax — a *different* concept on the assignment's list. Cutting that to one
  sourcing beat fixed the scope problem and removed the dependency at the same
  time. The tooling question had been asked before the scope question, and the
  scope question was the one that mattered.

**Still unresolved.** `lead_silence_s` is mandated by the ai-explainer SKILL.md
on the executive-summary beat, and other skills write it, but neither Claude nor
I can find anything under `runtime/` that reads it. It is written on B01 as the
law requires; I verified the beat's real length (10.69s audio, 10.7s media) rather than
trusting the field.

---

## 6. Corrections applied (DOUBLE-CHECK LAW)

1. **Key order.** `Counter` prints `{"1": 268, "2": 630, "0": 102}` in
   first-encountered order. B04 reproduces that order verbatim instead of
   sorting it, and labels the bars `[0] [1] [2]` so the difference is visible
   rather than quietly tidied.
2. **"Expected" de-sensationalised.** An early narration line called 665.24 what
   the run "should" produce. Corrected: it is the long-run average over repeated
   1000-draw experiments, not a target for any single run. B03 states the
   correction on screen by striking through the wrong framing.
3. **Scope.** The softmax derivation was cut from two beats to one, which now
   ends by saying the video uses only one of those numbers.
4. **No version numbers.** No model version or drifting count is named on
   screen, so the video does not date.

---

## 7. Corrections and changes made after the first render

### The statistical correction (the important one)

The first cut called 630 an *ordinary* sampling result. It is not:
`sd = 14.9230`, `z = −2.3615`, `P(X≤630) = 1.04%` — about 1 run in 50. Four
beats (B01, B05, B06, B07) were rewritten and re-rendered, and B06's 630 marker
was moved from mid-distribution to bin 3, where z = −2.36 actually falls. Full
row-by-row detail in `FACTCHECK.md`; the reasoning in `FRICTIONAL.md`.

The video's claim is now: the gap is unusual, **and** unusual is not evidence
the probabilities are wrong, because it is one draw from one fixed seed read
after the fact.

### Design decision: the accent is split in two

Terracotta `#D97757` on cream is 2.74:1, below the 4.5:1 that the toolkit's type
spec §8.3 requires for text. Rather than abandon the accent or ignore the rule,
the two uses are separated:

| Use | Colour | Contrast on `#F2F0E9` |
|---|---|---|
| Fills — bars, spans, rules | `#D97757` (CLAUDE.SPARK) | n/a — WCAG text contrast does not govern a solid shape |
| Text — focal numbers, labels | `#A2442A` | 5.42:1 ✓ |

Same hue, darkened for type only. `ObservedCounts` and `TheGap` are registered
in the checker's existing `STRUCTURAL_TERRACOTTA_PATTERNS` list with a written
justification, as ~20 prior reels have done for the same reason.

### Changes made to the brutalist.art toolkit

These live in the toolkit, not in this folder, and are needed to rebuild:

| File | Change | Why |
|---|---|---|
| `src/scenes/ExpectedObserved.tsx` | **new** — the five body components | this reel |
| `src/Root.tsx` | five `<Composition>` registrations | so the scenes are renderable |
| `src/scenes/ClaudeWindow.tsx` | wire `width` + `fontSize` | both were declared in the schema but never destructured; the card was locked to 1100px / 19px text and could not pass canvas-fill at 1920×1080. Old values kept as defaults, so no existing reel changes |
| `src/illustrations/kit.tsx` | optional `sparkSize` on `IlluStage`/`SparkLine` | the shared spark line is 40px, just under the 41px type floor. Defaults to 40 — non-breaking |
| `runtime/scripts/type_check.py` | 3 exemption entries + justifications | 2 structural-accent, 1 documented false positive (the `×` glyph in B03) |

### Two toolkit defects found and worked around, not fixed

1. **`BrutalistHesitantWriter` cannot match multi-word triggers.** Line 133 does
   `triggers.indexOf(core.toLowerCase())` where `core` is a single
   whitespace-delimited token, so a phrase trigger never fires — even though the
   ai-explainer SKILL.md's own worked example (`list of topics` →
   `sequence of distinctions`) is multi-word. B01 uses a single-word correction
   (`proof` → `unusual`) that still flips the whole sentence.
2. **`lead_silence_s` appears to be unimplemented.** The SKILL.md mandates it on
   the executive-summary beat and other skills write it, but nothing under
   `runtime/` reads it. It is written on B01 as the law requires; the beat's real
   length was verified on extracted frames instead.

### Gate results

`GATE F` signed · `GATE T` **PASS** (0 FAILs) · `GATE V` **clean**
(0 BLOCKER, 0 MAJOR across 20 sampled frames).
Master: 147.3s, 3840×2160, h264 + AAC, 10.5 MB. Total spend **$0.00**.
