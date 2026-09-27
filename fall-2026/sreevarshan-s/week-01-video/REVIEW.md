# REVIEW — week-01-token-not-word

Required by `youtube/README.md`: timestamped problems, requested changes,
re-checks, and the real human review decision.

> **The human review decision below is deliberately unfilled.** A rendered file
> is not a reviewed final. `youtube/README.md` is explicit about that, and the
> prerequisite adds that "a successful compile is not evidence that the teaching
> works." Only the student can watch the cut and decide.

## Automated re-checks performed during the build

| When | Problem | Change made | Re-check |
|---|---|---|---|
| 2026-09-22 | Gate A: `B01_ClaudeTranscript` static — "shapes never change" | Card is drawn rather than faded; rule drawn across it; marker travels from the question to the "3" | Gate A clean |
| 2026-09-22 | Gate A: `B04_IsolatedSplit` same failure | Marker travels box to box as each r-count lands | Gate A clean |
| 2026-09-22 | Gate A: `B08_LearnedNotGiven` same failure, persisted after first fix | Root cause: the static checker cannot resolve `SurroundingRectangle` geometry. Replaced with explicit `Rectangle` at explicit coordinates | Gate A clean |
| 2026-09-22 | Gate B strict: `correct` in B01 outside safe area, box y −3.45 vs limit −3.40 | Bottom margin raised 0.55 → 0.80; same fix applied pre-emptively to the shared citation helper and the B07 stamp | Gate B re-run |
| 2026-09-22 | Gate B: `B02_TextToIntegers` — **40 text-on-text errors**, e.g. `m` ✕ `r` at 100% overlap | Cause: the sentence was built as one `Text` per character, then scaled to fit; adjacent glyph boxes then register as overlapping text objects. Rebuilt B02 as a single `Text` and added an explicit rectangle for the required shape motion | Gates A + W clean; Gate B re-run |

| 2026-09-22 | Gate B: `B04` title colliding with the scaled-up token boxes | Boxes narrowed 10.6 → 10.0 and lowered to y 1.15 | Gate B clean |
| 2026-09-22 | Gate B: `B05` content at y ±5, fully off-frame | `scale_to_fit_width` only constrains one axis and *enlarged* a short wide group. Added a `_fit()` helper taking the smaller of the width/height ratios; applied to B09 which had the same latent bug | Gate B clean |
| 2026-09-22 | Gate V: 19 → 6 → 0 `underfill` defects | Type scaled up throughout, layouts run full width, composition lands by ~1/3 of each beat, card surfaces added behind B06/B08 content | Gate V clean: 0 BLOCKER, 0 MAJOR |
| 2026-09-22 | Gate B: `B06` seven-row stack 5.62 units tall, hitting title and footer | Plate height 0.70 → 0.58, buff 0.12 → 0.07, type 32 → 28 | Gate B clean |
| 2026-09-22 | **Found by eye, not by any gate:** the highlight box on B01 clipped the `e` of "are" and hid the `r` of "r's", visually altering the verbatim quote | Replaced the surrounding box with a `Line`-based underline plus an explicit marker rail. (Manim's `Underline` is absent from the Gate A mock, and derived geometry defeats its distinctness check, hence both pieces) | Frame re-extracted and inspected |
| 2026-09-22 | **Found by eye:** quote rendered as `3r's` — Manim strips leading spaces from split `Text` fragments | Inter-word gap restored explicitly (buff 0.26); quote now reads exactly as received | Frame re-extracted and inspected |

| 2026-09-22 | **Reported by the student from frame-by-frame review:** garbled overlapping glyphs at the "What the model is handed" beat | Root cause found at ~24.2–24.7s (not 15s): `TransformFromCopy(sentence, row)` in B02 spawns a copy on top of the sentence and morphs it down *through* the original — ~6 frames of doubled then garbled text. Replaced with a plain `FadeIn` of the integer row; no glyph-matching state exists | 20 frames re-pulled at 0.1s across 23.2–25.2s, plus 40 frames 25.0–29.0s: all clean |
| 2026-09-22 | Same defect class, found while auditing: B00's counter used `Transform` between `Text` mobjects | One blob frame per digit tick and two garbled frames on "3"→"three". Replaced with fades | Re-pulled at 0.1s: a simultaneous crossfade still showed "3" over "three" reading "th3ee", so the fades were made **strictly sequential** (fade fully out, then in). Re-verified: no frame holds two glyph states |
| 2026-09-22 | Same class, cosmetic: B01's underline swept across the RESPONSE, VERBATIM label, reading as a strikethrough | Underline now crossfades in place rather than travelling | 24 frames re-pulled at 0.1s across 14.4–16.8s: clean |
| 2026-09-22 | Audit: are any glyph-matching animations left? | All `Transform` calls in the reel now operate on rectangles or lines only; zero `Text`→`Text` transforms, zero `TransformFromCopy`, zero `TransformMatching*` | B03 and B08 shape transforms spot-checked at 0.1s: text crisp throughout |

| 2026-09-22 | **Polish pass — alignment audit.** Header ink-top measured 2s into all 11 beats: B01–B09 consistent within 9px, but **B00 sat 30px (0.22u) low** and **B10 132px (0.98u) low**, both hand-placed instead of using `_title()`. `_title()` also anchored by centre, so headers with descenders sat ~9px higher than those without | `_title()` switched to a top-edge anchor (`to_edge(UP, buff=0.72)`); B00's question, B07's stamp and B10's headline put on the same anchor; B10's stack restretched so the frame stays filled | Re-measured at the same checkpoints: header ink-top spread **132px → 1px**, centre-x spread 1px → 0px |
| 2026-09-22 | Polish pass — horizontal audit | Body left-edges span 120–793px, but nine of eleven beats are centred compositions of differing widths, so this is not drift. Only B01 (card) and B09 (columns) are left-aligned blocks and they are structurally different. **Deliberately not changed** — forcing a shared left edge would break the centred designs | no change |
| 2026-09-22 | Polish pass — pacing audit. Every beat began animating 0.00–0.25s after its cut (no settle). Six beats front-loaded: animation finished at 15–43% of the beat (B07 15%, B09 27%, B08 28%, B03 33%, B05 34%, B04 43%), leaving 10–17.7s frozen under live narration. B06 the reverse — animation ran to 98%, abrupt cut-out | 0.35s settle added at each cut-in; internal waits restretched so reveals track the narration. Waits only — no content added, no run_time of any reveal changed | Re-measured: animation now ends at 51–75% (B03 33→64%, B04 43→74%, B05 34→66%, B06 98→75%, B08 28→65%, B09 27→71%); first motion after the cut 0.25–0.62s. **Runtime unchanged at 3:01.75**, no "slowed" warnings, Gate V still 0/0 |

| 2026-09-25 | Weight pass: body `_t` NORMAL→SEMIBOLD, mono `_m` NORMAL→BOLD, headers BOLD→HEAVY, key numbers ("73700", "three", "correct") →HEAVY. Palette and typefaces unchanged | weight only | Gates A/W/V clean |
| 2026-09-25 | **Regression caught by frame inspection, not by any gate:** B06's name-tag rows overflowed their plates — descenders on "Smoking"/"strawberry" collided with adjacent rows. Cause was my own `_fit()` helper: it takes `min(w_ratio, h_ratio)` and **scales up** when content is smaller than the box, so using it as a clamp *enlarged* the rows once glyphs got heavier | Added `_clamp()` (shrink-only, never scales above 1.0) and switched B06 and B08 to it | B06 and B08 re-rendered and re-inspected at full resolution: all rows inside their plates, descenders intact |
| 2026-09-25 | Boxed/tabular beats re-checked for weight-induced clipping | B03 (8-token row) and B04 (str/aw/berry) auto-size their boxes from label width, so no clipping was possible; B02's integer row is width-scaled; B06/B08 fixed above | all 11 beats sampled at 78% and inspected: no overlap, no clipping |
| 2026-09-25 | End credit "Built by Sreevarshan" added | Placed inside B10's existing 3.45s static tail, so it costs **zero** runtime. Headline, both rules and the synthetic-narration disclosure stay on screen so it resolves the same card rather than acting as a separate slide. Holds 2.0s | runtime identical at 181.75s |

| 2026-09-25 | **Reported by the student:** caption/annotation lines throughout the deck showing merged words — "the entire input"→"theentireinput", "one letter at"→"oneletterat" | **Neither hypothesis held.** There is no fit-to-width squeeze on caption text: `_foot()` applies no width constraint, and every `scale_to_fit_width`/`_fit`/`_clamp` call targets token-box groups only. Nor was it the weight change — size-20 NORMAL and size-20 SEMIBOLD merge identically. Actual cause: Manim 0.18.1 rounds the space advance to ~zero below ~22px for this face. Render sweep: 20 merges, 21 partly merges, **22+ clean at every weight** | Caption style raised 20→23 via a single `CAPTION` constant. Four more lines below threshold also found and fixed (B01 "PROMPT"/"RESPONSE, VERBATIM" at 20; B09 bullets and B10 disclosure at 22). Zoomed crops pulled from **all 11 beats** — footers, B01 card labels, B03 "8 tokens", B04/B05/B06 notes, B07 labels, B08 arrow label, B09 bullets, B10 disclosure: every line shows visible word gaps. Widths re-checked: widest caption 9.66u against 12.60u safe. Runtime unchanged at 181.75s |

All 11 scenes pass Gate W (WCAG contrast, margins, text overlap) with no
warnings. No gate was disabled at any point; `ART_QC` and `ART_STRICT` were left
at their defaults.

## Timing check

Estimated 3:39 from the beat sheet; measured Kokoro audio 181.6 s = **3:02**.
Inside the 2–4 minute requirement. Nothing padded or trimmed to hit a number.

## [YOUR REVIEW — to complete]

Watch the whole cut **with sound** before filling this in. The prerequisite asks
you to check specifically:

- [ ] Do the numbers on screen match `evidence/*.txt`?
- [ ] Is the code/evidence legible at your viewing size?
- [ ] Is the Kokoro pronunciation acceptable (especially "cl100k", "o200k", the token ids)?
- [ ] Is B01's transcript exactly what you received, with correct date and model?
- [ ] Is the B07 "CONSTRUCTED ILLUSTRATION" stamp readable for the whole beat?
- [ ] Is the limitation in B09 clear and honest?
- [ ] Any unfinished slates or missing assets?

**Timestamp / problem / requested fix:**

*(record at least one change you requested after watching — the prerequisite's
"Record the split" asks you to explain how it improved understanding, not just
appearance)*

**Review decision:** ☐ draft ☐ review cut ☐ reviewed local final

**Reviewed by:** ______________________  **Date:** ______________
