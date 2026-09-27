# BUILD-LOG — "The Token That Followed"

INFO 7375 · Week 01 · Chapter 1 · Rithika Sankar Rajeswari
Built 2026-09-22 / 2026-09-23 · Claude Opus 5 in Claude Code · macOS Darwin 25.6.0
Total spend: **$0.00** (Kokoro TTS is local; no paid API was called)

---

## 1. Gate record

Gates as this toolkit edition actually implements them. `./art run` prints each
one; nothing below is inferred.

| Gate | What it checks | Result |
|---|---|---|
| **GATE L** (library-first) | ask the scene library before authoring a beat | **MISS** — 8 leads, none a distribution/logit/loss/gradient scene. A miss is a design card, so 9 components were written. Logged to `TEMPLATE-MISSES.md` by the search itself. |
| `build_safety.py` | project/approval validation | **rc=0** |
| **GATE L** (beat-mix lint) | no single-sentence Remotion text slide, no stray card | **clean** — `[beat-lint] clean — beat mix OK` |
| **GATE SHAPE** | finance chart-shape enforcement | **skipped** — not a finance reel |
| **GATE F** (paperwork set) | `FACTCHECK.md` + `SHOTLIST.md` + `PROMPTS.md` exist *before* rendering | **PASS** on the second attempt — the first `./art run` exited 2 because none of the three existed. All three written, then pass. |
| **GATE A** (static pre-flight) | render-free check on pending Manim scenes | **not exercised** — this reel has zero Manim beats (`no Manim beats in this reel's beat sheet — skipping Manim stage`) |
| **GATE W** (WCAG/margins/overlap) | independent second check on Manim scenes | **not exercised** — same reason |
| **GATE B** (Manim layout audit) | per-scene layout errors | **not exercised** — same reason |
| **GATE V** (frame-level visual QC) | 9-point rubric on the COMPILED cut, 26 sampled frames | **first run: 0 BLOCKER / 6 MAJOR** → all six `underfill` → fixed → **final run: 0 BLOCKER / 0 MAJOR** |
| `align.py` (word clock) | word-level timings from each beat's mp3, aligned onto the known narration | **13/13 beats aligned, 0 fallback** — 533 words at 24 fps → `mp3/words.json` |
| `verify_softmax.py` | every on-screen figure reproduces exactly | **PASS** before the build, after the build, and from inside the extracted submission zip |
| beat-sheet cross-check | all 24 figures stored in scene props re-derived from the four logits | **24/24 match** |
| `scripts/validate_course.py` | the course repo's own validator (required by `AGENTS.md`) | **rc=0**, 13/13 tests OK with these files in the tree |
| Decoded-stream check | not a file check — actual streams, durations, audio signal | h264 3840×2160 + AAC 48 kHz stereo; video 195.625 s = audio 195.625 s; 4695 frames @ 24 fps; **mean −23.9 dB / max −3.4 dB** (not a silent build) |

### Gates the skill mandates that this edition does not implement

- **GATE T (type-lock).** `ai-explainer/SKILL.md` says GATE T "ALWAYS RUN" and that
  neither `./art run` nor `./art final` may report success while `TYPECHECK.md` has any
  FAIL. The script it names, `scripts/type_check.py`, **does not exist** in this
  toolkit edition, and `run.sh` contains no reference to it. **No `TYPECHECK.md` was
  produced and none is claimed.** The §8.1 min-size and §8.2 overflow concerns it
  covers were instead checked by hand during the Gate V frame reads, and one residual
  min-size finding is recorded in §3 below rather than passed silently.
- **GATE SHARPNESS.** Referenced by the PIXEL-ART LAW as a Laplacian-variance audit
  after GATE T. Also absent. Moot here in substance: the law governs
  `shapeRendering="crispEdges"` pixel-art rects, and this reel renders none — the one
  component that would have (`ClaudeTitleOutro`, with its mascots) is deliberately not
  used. `grep -n rotate` over the nine new components returns exactly one hit, and it
  is a comment in `Ch1PretrainOutro.tsx` ("Nothing rotates") — **zero rotation
  transforms in the rendered output**.

## 2. Gate V defect log — the six MAJORs and their root-cause fixes

All six were `underfill` (FILL-THE-CANVAS LAW), and all six were on the three beats
that do **not** inherit the `Ch1Stage` chassis. The chassis pins the spark line to
SAFE's top edge and the course bug to its bottom-right, so the eight `Ch1Pretrain*`
beats spanned the canvas for free.

| Beat | Before | After | Root-cause fix |
|---|---|---|---|
| B01 `BrutalistHesitantWriter` | 41% / 53% | **59.5% / 59.5%** | Failed only at the 50% sample: at 5.9 s the sentence was *still being typed*, so the ink bbox hugged half-written text. Type alone could not fix that. Shortened the third line and set `charMs` 26 → 10, with the decorative hesitations (`mistakeRate`, `hesitateWithin`, `hesitateBetween`) → 0, so the overview completes before the first steady-state sample. The one meaningful hesitation — `facts` → `sequences` — is untouched. |
| B10 `ClaudeVerdictArtifact` | 41% / 41% | **57.9% / 57.9%** | A fidelity component with no size props; height is driven by line count and wrapping. Stated the recap more fully and added a fourth line naming the boundary. Content change, not a layout fork. |
| B12 `Ch1PretrainOutro` | 16% / 20% | **97.6% / 97.7%** | My own component — restructured so the eyebrow anchors to SAFE's top edge and the credit rail to its bottom edge, with the title spanning between. Still a spare poster; the negative space now sits inside a frame that claims the canvas. |

Fixes were measured against the gate's own `analyze_frame` on extracted frames before
recompiling, rather than paying a full 4K re-encode per guess.

## 3. Justified deviations — recorded, not silently passed

1. **`Ch1PretrainOutro` instead of `ClaudeTitleOutro`.** The compile prints
   `SKIN LINT: B12: palette=claude but the outro is 'Ch1PretrainOutro' — OUTRO LAW
   wants ClaudeTitleOutro`. The warning is correct and is left standing. Reason:
   `ClaudeTitleOutro` hardcodes the `@NikBearBrown` handle with no prop override, and
   `OUTRO-LOCK.md` scopes it to claude-liam reels — "Other channels use their own outro
   components — never this one." Using it would have shipped coursework under another
   channel's handle. The law's substance is kept: exact title restate, poster-plain
   serif, terracotta period, handle beneath.
2. **B09 carries no `CONSTRUCTED EXAMPLE` banner.** Deliberate: that beat displays no
   constructed figure — it describes the construction's edges. The banner would be
   false furniture there. Every one of the eight beats that *does* show a figure
   carries it.
3. **B00 / B03 / B11 mono RESULT lines render at ~22 px effective**, just under the
   ~24 px legibility floor. This is the shipped `ClaudeComposerAsk`'s own sizing, not an
   authored value, and it is the finding GATE T would have caught had it existed.
   Flagged rather than fixed, because fixing it means forking a fidelity component.
4. **`lead_silence_s: 0.8` on B01 has no effect.** EXECUTIVE-SUMMARY LAW requires the
   field be written explicitly; a grep for `lead_silence` across `runtime/scripts/`
   returns nothing, so no script reads it. The field is kept (the law requires it) and
   the law's *intent* was satisfied by measurement instead: B01's audio window is
   11.24 s against a 9 s floor, and the correction was confirmed on screen before the
   cut by reading the beat's final frame.
5. **Channel `claude-sasha`, voice `af_bella`.** The skill's default is `claude-liam` /
   `am_onyx`. The assignment names the persona **Sasha**; no Kokoro voice is named
   Sasha, so the persona is Sasha and the voice is `af_bella` — one of the two voices
   this edition documents and reports green. IN-FOR-BEAR LAW does not apply: Sasha is
   not standing in for Bear on Bear's channel and never claims to be.

## 4. Path conflicts left for the human

Flagged rather than resolved, because each is the author's call:

1. **`fall-2025/` does not exist in the course repo** — it has `fall-2026/`, and today
   is 2026-09-23. Built to `fall-2025/rithika-s/week-01-video/` as instructed. The
   `firstname-l` folder convention that `rithika-s` follows is correct either way.
2. **`AGENTS.md` says films belong under `youtube/`** — "Store course films and their
   source records under `youtube/`". The instruction specified a `fall-*` student path,
   which won. The conflict is recorded here per `AGENTS.md`'s own rule that course
   policy conflicts stay visible.
3. **Nothing was pushed or published.** `AGENTS.md`: "Do not publish or push without
   user authorization." No commit, no push, no upload.

## 5. Rebuild

`beat_sheet.json` is the only source of truth; `mp3/` durations are the clock; `media/`
and the master are derived. Full command sequence in `BUILD-PROMPT.md`. To change a
figure on screen: edit `verify_softmax.py` first, re-run it, and only then touch the
scene props — the script is the gate, not the commentary.

---

# Revision 2 — 2026-09-23: the six-act rebuild

Runtime floor raised to 4:00 by a live-class instruction from the professor, overriding
the written 2–4 minute syllabus target. There is no written source; the class date is left
as a placeholder for the author rather than invented (`FRICTIONAL.md` § Revision —
2026-09-23, and #20).

## What this revision changed

| | 3:16 cut | 4:13 cut |
|---|---|---|
| Structure | ai-explainer bookends (cold open → BLUF → body → verdict → handoff → outro) | the brief's six acts (hook → mechanism → contrast → loss → boundary → takeaway) |
| Beats | 13 | 12 |
| Softmax shown | `exp(z)` then normalize (2 visible steps) | all 5 steps: z → z−max → exp → ÷Σ → p |
| Claude interface | 3 beats | **none** (`FRICTIONAL.md` #25) |
| Numbers | typed into scene props, cross-checked after | **generated** into props by `build_beat_sheet.py` from `verify_softmax.py --emit` |
| Audience | practitioners | absolute beginners; no term used before the beat that defines it |
| Viewer pause | none | 3.5s of real appended silence in the hook |

## New in the gate record

| Gate | Result |
|---|---|
| `verify_softmax.py` | **PASS** — now proves the full five-step pipeline, and asserts max-subtraction is identical to the naive softmax to 1e-12 |
| Numbers-to-props | **structurally closed.** `build_beat_sheet.py` builds every scene prop from `softmax_values.json`. The previous cut needed a separate cross-check because a figure could be right in the script and mistyped in a prop; that gap no longer exists |
| Clock integrity | **re-verified after a corruption.** `generate_audio_kokoro.py` overwrote a corrected duration with a stale cached value from `mp3/timings.json`, silently shortening the film by 3.5s. Clock rewritten from one `mutagen` measurement of the files on disk; `timings.json` rewritten truthfully and a stale `B12` row from the previous cut dropped |
| GATE T | still **absent** from this toolkit edition — not claimed |

## Departures this revision introduces, recorded not passed

1. **No Claude interface, so three frame laws no longer apply.** COLD OPEN LAW,
   ASK→RESULT LAW and HANDOFF LAW governed beats that no longer exist. The brief specifies
   act 1 as the false sentence in plain English with no math, which cannot also be a
   composer window; and the constraint that any Claude response shown must be a real, dated
   one rules out the composed RESULT lines the previous cut used. Showing none is the honest
   option.
2. **No scaffolded viewer task.** It lived in the HANDOFF beat. The six-act structure has no
   slot for it and the brief says not to add a seventh act. Recorded in `CHECKS-REPORT.md`.
3. **EXECUTIVE-SUMMARY LAW abandoned.** `BrutalistHesitantWriter` was beat 2 of the previous
   cut. The brief's act 1 *is* the advance organizer, in plain language, so a second framing
   beat would be redundant for a beginner.
4. **Act 2 exceeds the brief's own 60–90s range** (150.27s, 59% of the film). The brief's
   per-act maxima sum to 195s, which is below its own 4:00 floor, and it forbids a seventh
   act — the constraints cannot all hold literally. Act 2 is the act the brief asks to slow
   down, so it absorbed the difference. `FRICTIONAL.md` #21.
5. **`Ch1PretrainGradient` and `Ch1PretrainOutro` are no longer used.** The p − y beat is
   not part of the six acts, and act 6 carries the outro function. Both remain registered
   and indexed.

## Lints raised by the revision-2 compile, and their disposition

All three fired as expected. None is a gate failure; all are left standing rather than
suppressed.

1. **`WARNING: 'column-reveal' carries 5/12 beats (41%) — over the ~40% cap (MOTION.md)`.**
   Accurate, and accepted deliberately. The cap exists to stop a reel becoming monotonous
   by reusing one motion language. Here the reuse *is* the teaching device: the five ladder
   beats return the viewer to the same four-row table and add exactly one column, so the
   columns already understood stay on screen as the ground the next one is built on. Giving
   each step its own motion language would be the defect — a beginner would be relearning
   the layout five times instead of learning five steps. The cut is 41% against a ~40%
   guideline, and the act boundaries around it change scheme every time (sentence → card →
   paired vectors → table×5 → paired corpora → paired panels → ruled list → poster).
2. **`SKIN LINT: B00 … COLD OPEN LAW wants ClaudeComposerAsk`.** The brief specifies act 1
   as the false sentence in plain English with no math on screen, which cannot also be a
   composer window. See `FRICTIONAL.md` #25.
3. **`SKIN LINT: B11 … OUTRO LAW wants ClaudeTitleOutro`.** `ClaudeTitleOutro` hardcodes the
   `@NikBearBrown` handle and `OUTRO-LOCK.md` scopes it to claude-liam reels. Act 6 carries
   the outro function with the course's own credit rail.

**Revision-2 GATE V: 24 frames, 0 BLOCKER, 0 MAJOR — clean on the first pass.** The three
new components inherit `Ch1Stage`, which anchors furniture to the SAFE edges, so the
underfill class of defect that cost revision 1 six MAJORs did not recur.
