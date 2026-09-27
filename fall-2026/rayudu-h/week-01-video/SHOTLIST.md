# SHOTLIST — temperature-is-concentration

Typed work order. One row per beat; audio durations are MEASURED from each
beat's mp3, never estimated. Measured audio totals 187.65 s; the master is
187.88 s = **3:08** after 24 fps frame quantization (assignment target 2–4 min).
Table generated from `beat_sheet.json`, so it cannot drift from the build.

| Beat | Act | Dur (s) | Lane | Fill | Status |
|---|---|---|---|---|---|
| B00 | ASK | 13.91 | remotion | `ClaudeComposerAsk` | AUTO — cold open: the student's prompt; no result lines, no model name (2026-09-25) |
| B01 | BLUF | 10.99 | remotion | `BrutalistHesitantWriter` | AUTO — overview; single-word corrections creativity→concentration, truthful→concentrated (2026-09-25) |
| B01A | ANALOGY | 26.18 | manim | `scenes.py::B01A_ContrastSlider` | AUTO — the everyday analogy; library PUNT, authored in-reel (2026-09-22) |
| B02 | FRAMEWORK | 22.42 | manim | `scenes.py::B02_ScoresToProbs` | AUTO |
| B03 | ASK | 7.17 | remotion | `ClaudeComposerAsk` | AUTO — the question B04 answers; no generation claimed |
| B04 | MECHANISM | 31.25 | manim | `scenes.py::B04_RatioCollapse` | AUTO — derivation (the shared total cancels), then the worked example (2026-09-26) |
| B05 | BOUNDARY | 26.30 | manim | `scenes.py::B05_ConcentrationLimit` | AUTO — boundary; closes on the analogy callback (2026-09-23) |
| B06 | VERDICT | 22.36 | remotion | `ClaudeVerdictArtifact` | AUTO — one-page verdict, six lines |
| B07 | HANDOFF | 24.60 | remotion | `ClaudeComposerAsk` | AUTO — the viewer's prompt, read aloud verbatim (2026-09-26) |
| B08 | OUTRO | 2.47 | manim | `scenes.py::B08_TitleCredit` | AUTO — title restate + author credit |

**No open slots.** Every beat is filled deterministically by the free pipeline
(Manim + Remotion + Kokoro). Nothing waits on a human, a recording, a stock
asset, or a paid API. `pantry/` is empty by design.

## Library-first record (GATE L)

Checked with `./art scenes --check` before authoring anything:

| Composition | Result |
|---|---|
| `ClaudeComposerAsk` | RENDERABLE 16:9 — props match (command/topic/segment/greeting/runningText/output/modelLabel) |
| `BrutalistHesitantWriter` | RENDERABLE 16:9 — props match (text/triggerWords/replacementWords/…) |
| `ClaudeVerdictArtifact` | RENDERABLE 16:9 — props match (artifactTitle/artifactHeading/artifactLines) |

Three hits, zero slates. The math beats route to Manim because no registered
composition draws a softmax distribution, a ratio identity with its derivation,
or a concentration limit — the correct Manim lane, not a library miss.

**Two genuine library gaps, both filled in-reel.**
- *The analogy (B01A).* `./art scenes "everyday analogy: contrast knob rescales
  differences without reordering"` returned five unrelated candidates (the top
  hit, score 6.0, a WCAG contrast meter). A PUNT, authored as
  `B01A_ContrastSlider` — never slated.
- *The outro (B08).* `ClaudeTitleOutro` is hard-locked to the `@NikBearBrown`
  handle (OUTRO-LOCK.md) and every other registered outro carries another
  brand's palette. Rendered in-reel as `B08_TitleCredit`, so the assignment
  modifies nothing outside its own folder.

## Claude UI beats — prompts, never responses

B00 (the student's prompt), B03 (the question B04 answers) and B07 (the
viewer's prompt). None shows a Claude answer or a model name: the assignment
requires any Claude response shown on screen to be real and dated. So there are
**no ASK → RESULT pairs** — a deliberate deviation from the toolkit's COLD OPEN
LAW, logged in the beat sheet metadata. B06 is the reel's own one-page summary.
B01A / B02 / B04 / B05 are Manim figures (ILLUSTRATE LAW); B08 is the
reel-local title card.

## Render order

1. `generate_audio_kokoro.py` — 10/10 beats, af_bella, $0.00
2. `align.py` — word timings → `mp3/words.json` (captions and scene timing)
3. `./art run` — gates A / W / B / F / L, Manim renders, Remotion fill, review cut, Gate V
4. Frame-level visual QC — every beat read against its narration at 30 / 60 / 92 %
5. `./art final <reel> --out <reel>` — 4K master → `temperature-is-concentration.mp4`
6. `make_srt.py` — captions → `temperature-is-concentration.srt`
