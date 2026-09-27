# CHECKS-REPORT — temperature-is-concentration

PROOF GATE, written before the first slate compiles (ai-explainer SKILL.md).

```
9 SHOW / 1 justified-CARD / 0 PUNT

Teaching arc:  FRAMEWORK ✓ | WORKED EXAMPLE ✓ | FALSIFIABILITY ✓
               SCAFFOLDED TASK ✓ | BOOKENDS ✓ | NO-SOURCE-NO-VERDICT ✓
```

## Per-beat classification

| Beat | Act | Class | Artifact named in `shot.show` |
|---|---|---|---|
| B00 | ASK | SHOW | composer types the student's prompt; the spark line reads "the question this video answers". No Claude answer is shown (result lines removed 2026-09-25) |
| B01 | BLUF | SHOW | writer types "a creativity control." and "truthful the choice is."; each wrong word ("creativity", "truthful") shows terracotta, is deleted, and is retyped ("concentration", "concentrated"). **Corrected 2026-09-25** — see the section at the end: this row previously claimed a correction that never ran. |
| B01A | ANALOGY | SHOW | contrast slider travels; three swatches spread to near-ink/near-white, then wash to one grey; the terracotta marker on the brightest never moves. Re-timed to the words 2026-09-25; the inversion (lower temperature, higher contrast) is shown as it is spoken |
| B02 | FRAMEWORK | SHOW | 3 score chips → bars rise while their values count up → sum settles 1.000000 |
| B03 | ASK | SHOW | composer with the plot request typed; send button pulses |
| B04 | MECHANISM | SHOW | p₂/p₀ written as two fractions over the same total; the total is boxed and cancels; the identity rises; gap pins at 2; three ratio bars grow to 4/2/1 units as each value is spoken; e-column lands; the ordering strip darkens on the conclusion (derivation added 2026-09-26) |
| B05 | BOUNDARY | SHOW | bars sweep T=1→0.1; sliver remains; refusal card snaps; closing line holds alone |
| B06 | VERDICT | SHOW | artifact page reveals 6 numbered lines — mechanism, verified ratios, ordering with the seed-7 counts and the full T = 2 row, limit case, boundary, reproduction note |
| B07 | HANDOFF | SHOW | the viewer's prompt types itself in full, held for pausing; the narration reads it aloud word for word (2026-09-26) |
| B08 | OUTRO | CARD | title restate + credit (reel-local Manim) — **justified**: the outro brand card is a CARD by doctrine (OUTRO LAW) |

No beat is a bare CARD carrying a factual claim. No PUNTs.

## Teaching-arc checklist

- **FRAMEWORK before examples** ✓ — B02 builds the whole softmax machine before
  B04 uses it. The baseline distribution is on screen before any ratio.
- **WORKED EXAMPLE** ✓ — B04 first derives the identity on screen (the shared
  total cancels), then computes p₂/p₀ at three temperatures and checks
  each against exp(2/T); the numbers are the chapter's own.
- **FALSIFIABILITY** ✓ — B05 is a dedicated boundary beat: it names what the
  explanation does NOT establish, and shows the function refusing T=0 rather
  than degrading gracefully. This is the 2-point rubric line, on screen.
- **SCAFFOLDED TASK** ✓ — B07 gives a runnable task with a specific
  perturbation (change only the middle score) and tells the viewer what to look
  for (which ratio stays fixed, and why it had to).
- **BOOKENDS** ✓ — cold open (B00) → BLUF (B01) → body → verdict (B06) →
  handoff (B07) → title outro (B08).
- **NO-SOURCE-NO-VERDICT** ✓ — every figure traces to `main.py`; see
  `FACTCHECK.md`. The one judgement claim ("concentration is not
  correctness") is stated as an argument, never as a measurement.

## PPT test

No two consecutive beats share a visual scheme, and no beat is a headline over
a paragraph: B02/B04/B05 animate their mechanism, B01 animates its own
correction, B06 reveals line by line, B07 types. The only static hold is the
2.47s outro.

## Legibility contract

Checked on every SHOW beat: artifact named in `shot.show`; ~15–35% negative
space; nothing faded below ~40%; the three-temperature comparison in B04 is
side-by-side and held well over 2s (each row holds ≥2.8s).

## Gate status at time of writing

| Gate | Result |
|---|---|
| A — static pre-flight (all 5 Manim scenes) | CLEAN — B08 carries the expected non-blocking "text-only" note (it is a title card) |
| W — WCAG + margins + overlap (all 5) | CLEAN |
| L — library-first | 3 hits, 0 slates; the outro gap is filled in-reel (see SHOTLIST.md). B01A re-ran the gate — `./art scenes "everyday analogy: contrast knob rescales differences without reordering"` returned 5 candidates, all unrelated figure scenes (top score 6.0, a WCAG contrast meter). A genuine PUNT, so the beat was authored in the reel's own `scenes.py` rather than slated. |
| F — paperwork set | FACTCHECK.md · SHOTLIST.md · PROMPTS.md present |
| B — post-render layout audit | CLEAN — 27 snapshots, 0 errors, 0 warnings (`--curve-strict`, `ART_STRICT=1`) |
| V — frame-level visual QC | CLEAN — 20 frames, 0 BLOCKER, 0 MAJOR. Round 1 found 6 MAJOR (canvas-fill); the B01A pass found a caption defect the sampler missed (below). |

### GATE V round 1 → fixes applied

| Defect | Beat | Root cause | Fix |
|---|---|---|---|
| empty-frame | B05 @85% | card faded out before the closer faded in | cross-fade in one `play`; closer lands beneath the card |
| underfill 37% | B04 @50% | rows revealed one at a time, so the midpoint was half-empty | table frame (all 3 `T =` + strip) lands first, values populate after |
| underfill 3%/9% | B01 @50/85% | component centres 2 lines; sample landed mid-typing | props only: 4 short lines, `fontSize` 76→120, `charMs` 46→22 |
| underfill 47% | B06 @50/85% | artifact card sized to 4 lines | 5th line added carrying the T=0.1 / T=0 evidence |

No gate was loosened and `ART_STRICT` stayed at 1 — every fix is a root-cause
fix in the reel's own source or props.


---

## B01A — the everyday-analogy beat (added 2026-09-22)

Added on request: the reel was correct but front-loaded with algebra, so one
beat now grounds the idea in something anyone has touched — a photo contrast
slider — before B02 opens the softmax.

**Why it is a SHOW and not a decorative card.** The slider is the mechanism:
sliding it rescales how much the three swatches differ while the marker pinned
to the brightest one never moves. That is the reel's two central claims
(temperature rescales the ratio; temperature never reorders) enacted in a
medium with no notation in it. The beat carries no figure from `main.py` and
says "analogy — illustrative, not measured" on screen for its whole duration,
so it cannot be mistaken for evidence. Fidelity argument in `FACTCHECK.md`.

**Placement.** After the BLUF (B01), before the framework (B02) — the advance
organizer lands, then the intuition, then the machine. Nothing was removed and
no number changed: the graded evidence beats B02/B04/B05/B06 are byte-identical
to the previous master (`input_sha256` in `temperature-is-concentration.verified.json`).

### Gate V round 2 — the defect the sampler could not see

| Defect | Beat | Root cause | Fix |
|---|---|---|---|
| Caption illegible mid-change (glyph soup) | B01A @ ~18.5s | `Transform()` between two `Text` mobjects interpolates letter-by-letter when the glyph counts differ; every caption change had a ~1.2s unreadable window | Replaced all four caption changes with an explicit `FadeOut`/`FadeIn` cross-fade (`swap_cap()` in `scenes.py`) |

Gate V samples 20 frames across 171s — roughly one per 8.6s — so a 1.2s garble
window is very likely to fall between samples, and did. It was caught by the
manual VISUAL QC LAW pass (frames at 15/50/85% of the beat's own span, read
rather than probed) and verified fixed at t=20.0s. Recorded here because the
lesson generalises: a gate that samples uniformly across a reel cannot be
trusted to catch a defect shorter than its sampling interval, and per-beat
sampling is the thing that actually finds them.

---

## B05 — the analogy callback, and captions (2026-09-23)

**B05 extended.** The boundary beat now closes on the B01A callback: the three
swatches return above the `ValueError` card at full contrast, and the line "a
sharper picture of the wrong person" lands beneath "concentration ≠
correctness". Narration 67 → 80 words; measured clock 23.70s → 26.30s; the
scene was rebuilt to the new duration rather than stretched. Reel total
171.24s → 174.08s (2:54), still inside the 2–4 minute target.

Classification unchanged — B05 was already SHOW and remains SHOW. The callback
adds a second, non-numeric encoding of the same boundary claim; it introduces
no figure, and the "analogy — illustrative, not measured" obligation was
discharged at B01A where the analogy is established.

**Captions added.** `align.py` produced word-level timing for all 10 beats (0
fallbacks — the caption text is the known narration snapped onto Whisper
timestamps, not a transcription). The reel's own `make_srt.py` emits the SRT,
because the toolkit's writer ships with the publishing skills and this pipeline
never publishes.

| Check | Result |
|---|---|
| Gate A / W — static pre-flight, WCAG, margins | CLEAN |
| Gate B — post-render layout audit | CLEAN, 0 errors / 0 warnings |
| Gate V — frame-level visual QC | CLEAN, 20 frames, 0 BLOCKER / 0 MAJOR |
| Manual per-beat frame pass | CLEAN — B05 ending read at t=22.0s and t=25.0s |
| Caption lint | 57 cues · longest line 42 chars · 0 cues over 2 lines · 0 overlapping or inverted timestamps · last cue ends 173.96s against a 174.17s timeline |

Two defects in `make_srt.py` were found by reading its output rather than its
exit code — a greedy wrap that overflowed to 51 characters, and a cue grouper
that flushed after exceeding its budget instead of before. Both fixed at the
root; the budget is now enforced against the *wrapped* lines, which is the
only formulation that actually holds.

---

## B01 correction never ran — found by a viewer, not a gate (2026-09-25)

The B01 row above claimed, from 2026-09-16 until today, that the hesitant writer
corrects its misconception. It did not. Frames show the overview holding
*"Temperature is a creativity dial. It decides how truthful the answer is."*
from t≈5s to the end of the beat — while the narration says the opposite. It was
in every master, including the first. It was caught by watching the video.

**Cause.** `BrutalistHesitantWriter` splits `text` on whitespace and looks each
single word up in `triggerWords`. The triggers were phrases ("a creativity
dial", "how truthful the answer is"), which can never equal a single word, so
no correction ever fired and nothing reported it. The ai-explainer `SKILL.md`
instructs phrase triggers ("put the whole phrase in `triggerWords`"); the
component it ships cannot match them.

**Fix, within the component's actual contract.** One wrong word per sentence:
`creativity → concentration`, `truthful → concentrated`, `hesitateBetween: 0`.
The component's timeline was simulated before rendering (every keystroke floors
at one frame at 30 fps) and the simulation was calibrated against the broken
render. Verified by frames: "truthful" turns terracotta at ~6.1 s as the voice
says "not how truthful it is", and the corrected overview — word-for-word the
narration — holds from ~8.9 s to 11.0 s.

**Whole-reel audit.** Every beat sampled at 30 / 60 / 92 % of its span in the
final master and read against its narration. One further defect: B06 line 3
read "Counts at seed 7, n=1000: 849 / 630 / 469", which looks like three
outcomes in one run (they sum to 1,948, not 1,000). They are outcome 2's count
at T = 0.5 / 1 / 2; the line now says so.

| Check | Broken B01 | Fixed B01 |
|---|---|---|
| Gate V (frame-level QC) | 0 BLOCKER / 0 MAJOR | 0 BLOCKER / 0 MAJOR |
| Reading the screen against the script | **contradiction** | agrees word-for-word |

Gate V measures canvas fill and legibility; it passed the broken beat and the
fixed beat identically. It is not a check on meaning, and this report should not
have used it as one.

### Second pass the same day — Claude UI beats, and B01A timing

**Claude UI beats show prompts, never responses.** The audit also surfaced a
risk worse than any contradiction. B00 showed three result lines landing under
the prompt as Claude's answer, beneath a composer chip reading a real model
name ("Fable 5 · High", the component default). Those lines were written into
the beat sheet, not produced by Claude — and the assignment requires any Claude
response shown on screen to be real and dated. Fixed with props only: B00's
`output` removed, `modelLabel`/`effortLabel` blanked in B00/B03/B07, and B03's
"rendering Manim…" replaced with "the question the next figure answers". This
deliberately breaks the toolkit's COLD OPEN LAW (which requires result lines);
the assignment governs a graded submission. Logged in the beat sheet metadata.

**B01A ran ~3 s behind its own narration.** Word timings from `mp3/words.json`
showed the voice saying "slide it up" at 2.5 s while the slider first moved at
6.0 s. Its line "That is temperature" could also be heard backwards — sliding
*up* is *lower* temperature. The narration now says so outright ("Temperature is
that slider, run backwards: lower temperature, higher contrast", 73 → 77 words,
23.87 s → 26.18 s), and every event in the scene was re-timed to its phrase. The
knob swings to high contrast on "lower temperature, higher contrast" as it is
spoken.

| Check | Result |
|---|---|
| Layout audit (Gate B) | CLEAN — 31 snapshots |
| Gate V | CLEAN — 0 BLOCKER / 0 MAJOR |
| Changed beats read against the words at the moment each is spoken | B00, B03, B07, and B01A at six phrase points — all agree |
| Captions | 57 cues · longest line 42 · 0 timing errors · all 10 beats aligned |
| Reel | 176.42 s (2:56), 3840×2160 |

### Third pass — rubric-driven improvements (2026-09-26)

**B04 now derives its identity instead of asserting it.** p₂/p₀ is written as
two fractions over the same total, Σ exp(z/T); the totals are boxed on "the
same total underneath" and fall away on "so it cancels", leaving
exp((z₂ − z₀)/T), which rises into the identity line. Narration 61 → 85 words,
21.97 s → 31.25 s, every event timed to its phrase. The derivation also carries
the ordering claim: T only divides the gap, so no temperature changes its sign.
Boxed rather than struck through, because `--curve-strict` makes any stroke
across a label an ERROR and the gate was not loosened.

**B06** carries the full T = 2 row (202 / 329 / 469), re-run from `main.py`'s
`sample()` today. **B07**'s narration reads the on-screen prompt verbatim.

| Check | Result |
|---|---|
| Gate A — static pre-flight | CLEAN, after pinning coordinates (first version rejected: a width-derived position read x = −7.5 render-free) |
| Gate B — layout audit | CLEAN — 41 snapshots, 0 errors / 0 warnings, `--curve-strict` |
| Gate V | CLEAN — 0 BLOCKER / 0 MAJOR |
| Phrase-timed read: B04 at 9 points, B06, B07 at 5 points | all agree with the narration |
| Whole-reel audit of the final master, every beat at 30 / 60 / 92 % | all agree |
| Captions | 58 cues · longest line 42 · 0 timing errors |
| Reel | 187.88 s (3:08), 3840×2160 |

---

## Pre-push audit of every deliverable (2026-09-26)

Every deliverable checked against the assignment's list by verifying files,
hashes and cross-consistency — not by re-reading earlier summaries.

| Deliverable | Checks | Result |
|---|---|---|
| `temperature-is-concentration.mp4` | 3840×2160 H.264 24 fps + AAC; 187.88 s inside 2–4 min; identical to the reel master and the pipeline's `verified.json`; the clean master, not the marked review cut | PASS |
| `beat_sheet.json` | narration word-count equals the aligned audio for all 10 beats; every `actual_duration_s` equals its measured mp3 | PASS |
| | toolkit JSON schema | **14 enum errors — known toolkit inconsistency, not changed** (below) |
| `README.md` | name, assignment, concept, why, runtime = actual, setup / run / verify, licence, credits; Contents lists exactly the files present | PASS after fix — rebuild step now copies `make_srt.py` and the paperwork set |
| `BUILD-PROMPT.md` | audio / run / final commands, authoring prompt | PASS after fix — added `--out`, the caption step, 10 mp3s |
| `SOURCES.md` | used / made / Claude contributed / licences | PASS |
| `FRICTIONAL.md` | dated entries covering all five criteria of the Frictional guide | PASS |
| `SHOTLIST.md` | **was missing from the submission** — GATE F refuses to render without it — and stale in the reel | FIXED — regenerated from the beat sheet and shipped |
| Captions | caption text equals the narration verbatim, in order; 58 cues, longest line 42, 0 timing errors | PASS |
| Safe sharing | no credentials, tokens, email addresses, local paths, caches or dotfiles | PASS |
| Canvas zip | correct filename; entries equal `submit/`; integrity OK | PASS |
| GitHub | posted directly to the course repository at `fall-2026/rayudu-h/week-01-video/`, with the write access the instructor granted; public; every pushed file checked byte-for-byte against this folder (the mp4 is excluded by the repo's media policy — it is the Canvas upload) | PASS |

**Schema note.** The sheet fails `runtime/schema/beat_sheet.schema.json` on
`shot.source` (`'manim'`, `'remotion'`) and `shot.type` (`'UI'`). The toolkit's
own ai-explainer example (`claude-debunked`) fails the same way — 10 errors, all
`'remotion'` — and the router routes on exactly these values (`beat_plan.py`:
`src == "manim"`). The schema is stale relative to the runtime. The routing
fields were not rewritten, since the render depends on them and the rubric does
not.

**Rebuild from the folder alone.** A fresh directory holding only the seven
files the README lists (`beat_sheet.json`, `scenes.py`, `make_srt.py`,
`FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`, `CHECKS-REPORT.md`), built with the
README's commands verbatim: every gate passed, 10/10 beats rendered from
scratch, Gate V 0 / 0, and the master was **byte-identical** to the submitted
file (SHA-256 `88bbcabc…`), with identical audio, identical captions, and 21/21
sampled frames identical.

**Added after this audit**, per the course's film-folder guide
(`youtube/README.md`): `REVIEW.md` with the author's review decision, *Audience*
and *Status* lines in the README, and an explicit synthetic-narration disclosure
in `SOURCES.md`. The guide's `final/` folder was not adopted: the assignment's
deliverable list is flat, no classmate uses it, and moving the captions would
break the rebuild paths verified above.
