# FRICTIONAL — honest build log

Dated record of what broke, what I tried, and what I did instead. Kept as I
worked, not reconstructed afterwards.

## 2026-09-14 — Phase 0, getting the toolkit to READY

- **`ffmpeg` not on PATH.** `./setup` cannot verify anything without it — the
  whole pipeline muxes through ffmpeg. Fixed with `brew install ffmpeg`
  (now ffmpeg 9.0.1). Not a toolkit bug; a missing system dependency.
- **Default `python3` was 3.9.10; the toolkit needs 3.10+.** Newer Pythons were
  installed but not the default. I did **not** change the system interpreter —
  I made a project venv instead: `python3.12 -m venv .venv` (Python 3.12.9).
  Consequence I had to keep remembering: `./art` shells out to plain `python3`,
  so **every** terminal has to `source .venv/bin/activate` first or the
  pipeline silently runs on 3.9 and fails on imports.
- **Re-ran `main.py` after switching interpreters.** Counts were identical on
  3.9.10 and 3.12.9 (`{0: 102, 1: 268, 2: 630}`), and identical across 3 runs
  on each. That is a real, checkable observation about seeded repeatability —
  recorded in `SOURCES.md` as "matched on these two versions", **not** as
  "reproducible everywhere", which the evidence does not support.

## 2026-09-16 — Phase 1/2, authoring and building

- **The stock Claude outro hardcodes someone else's channel.** `ClaudeTitleOutro`
  bakes in `@NikBearBrown` (locked by `OUTRO-LOCK.md`, which scopes that card
  to `claude-liam-*` reels). Using it would have credited my coursework to the
  course instructor's channel. I built a new registered composition,
  `ClaudeTitleOutroCredit` (title · credit · subcredit), and ran
  `./art scene-index` so it is findable. Logged as a deliberate deviation in
  the beat sheet's metadata note.
- **LaTeX is deliberately not installed, so `MathTex` was off the table.**
  Rather than install a TeX distribution for three equations, I wrote them as
  Unicode serif text. Before trusting that, I checked EB Garamond's actual
  glyph coverage with Pillow (rendering each character and comparing against
  the font's notdef box) for `₀ ₂ ¹ ² ⁴ Σ ÷ × ≠ ≈ − · → —` — all present, so
  no tofu boxes and no raw TeX can reach the screen.
- **GATE A caught my B04 beat being text-only.** My first version of the ratio
  beat was typography and numbers with no shapes — the static checker reported
  "no shapes recorded — scene may be text-only", which is exactly the
  narrate-over-a-slide failure the rubric punishes. I added a bar per
  temperature whose **length is the exponent** (z₂−z₀)/T = 4, 2, 1. That is an
  honest encoding rather than decoration: the raw ratios span 54.6 → 2.7 and
  would not fit the frame, so the bar shows the quantity the identity actually
  varies. Captioned on screen as `bar length = (z₂ − z₀) / T`.
- **The outcome-0 sliver problem in B05.** At T = 0.1, p₀ = 2.061060e-09. Drawn
  to true scale it is invisible — but drawing it as zero would teach the exact
  error the beat exists to correct ("low temperature is argmax"). I drew a
  minimum-visible sliver and captioned it "sliver exaggerated for visibility",
  with the precise value on screen beside it.

## 2026-09-16 — Phase 2, the QC gates pushed back

- **GATE V failed the first build: 6 MAJOR defects, 0 blockers.** The
  toolkit's frame-level check samples every beat at 50% and 85% of its span
  and measures the *bounding box* of on-screen ink against the title-safe
  area, requiring 55%. Four of the six were genuine and two taught me
  something about the metric:
  - **B05 sampled as an empty frame.** My own bug. I faded the `ValueError`
    card out and then faded the closing line in, which leaves a blank frame
    between the two. Worse, the closing line alone — one sentence centred on
    white — could never pass a 55% spread test anyway. Fixed by *cross-fading*
    (one `play` call does both) and by landing the closer **beneath** the card
    instead of replacing it. That is better than the original: the refusal is
    the evidence for the claim, so the two belong on screen together.
  - **B04 filled only 37% at its midpoint.** Also mine: I revealed the three
    temperature rows one at a time, so half way through the beat only two
    existed. Fixed by landing the table *frame* first — all three `T =`
    labels and the invariant strip — and then populating the values. Better
    pedagogy too: you need the axis of comparison before the numbers.
  - **B01 filled 3% / 9%.** This one is inherent to the component, not to my
    beat: `BrutalistHesitantWriter` centres two lines of text, and a
    two-line block cannot span a frame. Because I had decided not to modify
    the toolkit, the only levers were its *props* — so I restructured the
    overview into four short lines and raised `fontSize` from 76 to 120.
    The 50% sample was also landing mid-typing, so I dropped `charMs` from
    46 to 22 to get the correction finished and held.
  - **B06 filled 47%.** Same shape of problem in `ClaudeVerdictArtifact`,
    whose card grows with the number of `artifactLines`. Rather than pad it,
    I added a fifth line that carries real evidence — the T = 0.1 limit case
    and the T = 0 refusal.
- **Two lints worth taking seriously.** The compiler warned that `type`
  motion carried 44% of beats (over a ~40% cap) and that B03 had an empty
  spark line. Both were honest mistakes: B03's own stage directions say the
  ask is *already typed*, so labelling its motion `type` was simply wrong —
  `reveal` is accurate, and fixing it brought the histogram to 33%. B03 also
  got the short serif cue the spark-line rule asks for.
- **Decision: the assignment adds nothing to the toolkit.** I had built a new
  Remotion component (`ClaudeTitleOutroCredit`) for the outro, because the
  shipped Claude title card hardcodes the instructor's channel handle. That
  worked, but it meant the assignment could only be rebuilt against a
  *modified* toolkit. I rewrote the outro as a reel-local Manim scene
  (`B08_TitleCredit`) in `scenes.py` and reverted the toolkit to a clean
  state. Slightly different lane — Manim rather than the Remotion skin —
  but the card is the same cream/ink/terracotta and the reel is now
  genuinely self-contained.

## 2026-09-16 — Phase 2, round 2: stop guessing, start measuring

My first pass at the canvas-fill defects was guesswork — I estimated text
widths from a rule of thumb and was wrong by more than a factor of two. Two
full pipeline runs (about six minutes each) bought very little information.

**What fixed it was building a measuring tool instead.** GATE V's checker
(`runtime/qc/final_frame_check.py`) exposes an `analyze_frame()` function, so I
wrote a 20-line harness that renders *one* beat, samples it at the same 50% and
85% points the gate uses, and reports the exact coverage figure the gate would
report. That turned a six-minute blind guess into a ninety-second measurement,
and it is the only reason the numbers below converged.

What the measurements actually showed:

- **The metric is bounding-box SPREAD, not ink density.** `cover = (bbox width ×
  bbox height) / safe area`. So "fill the canvas" means content has to *reach*
  across the frame; making text bolder or denser does nothing. This is why every
  remaining defect was a centred card.
- **B01 had two independent problems, and I had misdiagnosed it as one.** The
  11%/24% scores were mostly because the typing had not finished by either
  sample point — the component's `mistakeRate` and `hesitate*` knobs were eating
  the beat. Setting those to 0 made both samples read *identically* (50.9%),
  which proved the animation had settled. Only then was it a pure sizing
  problem, and I could solve it arithmetically: measured bbox at `fontSize` 130,
  scaled linearly, and found 140 clears the 55% bar while 160 would exceed the
  component's own `maxWidth` (86% of frame) and silently re-wrap. Chose 145 for
  margin on both sides.
- **B06 needed 46 more pixels of height.** The artifact card was already at 85%
  of the safe width, so width was maxed and height was the only lever — one more
  `artifactLines` entry. I used the reproducibility observation rather than
  padding, so the extra line carries real evidence.
- **B08 was a timing bug, not a layout bug.** My outro laid out fine but revealed
  its four elements in sequence across a 2.5-second beat, so at the 1.2s sample
  the frame was still half-built (47%). Landing everything inside the first
  0.9s took it to 63% at both samples. Obvious in hindsight: on a very short
  beat, a staggered reveal means the frame is never complete when it matters.

**One fix I would not have found without looking at the frames.** The composer
beats render a footer chip that defaults to `@NikBearBrown` — the instructor's
channel. My own coursework was quietly branded with someone else's handle in
three beats. `folderLabel` turned out to be a real schema prop whose comment
says "change only for off-brand one-offs", so it was a one-line fix per beat to
`INFO 7375`. The mp4 probe would never have caught this; the contact sheet did.

## 2026-09-17 — the final master: a stale failure hiding a real one

- **The build had been sitting in `"status": "failed"` since 17:22 the previous
  day, and the recorded cause was misleading.** `build-state.json` blamed
  `ENOSPC: no space left on device` — the machine was down to 549 MB. That was
  true, and by the time I came back it was also irrelevant: 55 GB free. The
  tempting move was to re-run and assume a disk error is transient. It is not,
  or not only: **the crash happened mid-Remotion-re-render and destroyed an
  asset.** `media/B07.mp4` was rewritten at 17:22 and survived; `media/B06.mp4`
  was deleted and never rewritten, because the disk filled in between. The
  error message named the symptom, not the damage.
- **`./art final` refused on a clear disk, and the refusal was correct.**
  `REFUSED: clean master would carry 1 slate(s): B06`. `resolve_slot()` looks
  only in `media/` and `manim/`; a beat with no source there becomes a request
  card, and the compiler's master law rejects a master containing one. Note
  that `clips/B06.mp4` still existed from the 16:21 run, so the *review* cut
  looked complete — the gap was invisible unless you checked the sources rather
  than the outputs. This is the toolkit being right: shipping a 4K "final" with
  a slate in it, because a stale intermediate made it look finished, is exactly
  the failure the gate exists to prevent.
- **Fix was narrow, because the diagnosis was.** `remotion_scenes.py` has an
  `--only` flag and its own `slate_resolves()` check, so
  `remotion_scenes.py <reel> --only B06` re-rendered just the missing beat from
  the props already in the beat sheet — no `--force`, nothing else touched.
  Verified the output at 3840×2160 and 22.367 s against the beat's recorded
  `actual_duration_s` of 22.36, and pulled a frame to confirm all six
  `artifactLines` were actually on screen rather than trusting the exit code.
- **The 4K master then built clean:** 9/9 slots filled, no slates, 147.583 s
  (2:27.58), 3840×2160 at 24 fps, AAC 48 kHz stereo, sha256
  `bdc5a921c9a91097c53dbcd0151f02743301f8a5ee02a40db4a6dc83f23aadc0` recorded in
  `build-state.json`. Confirmed the burned-in beat markers present in the review
  cut (`B00 UI VIDEO 0.0s +13.9s`) are absent from the master.
- **What I would do differently.** After any crash mid-build, diff the asset
  directory against the beat sheet before re-running — the failure message
  describes what stopped the build, not what the build had already broken. A
  disk-full error is recoverable; the half-finished write it interrupted may
  not be.

## 2026-09-22 — adding the everyday analogy, and a defect the gate could not see

- **Why I reopened a finished video.** Watching it back, the reel is correct but
  it goes from "temperature is a concentration control" straight into a softmax
  in under thirty seconds. Anyone who does not already read notation is lost
  before the evidence arrives. I added one beat (B01A) between the overview and
  the framework: a photo contrast slider, which is a thing everyone has dragged.
  Deliberately additive — no number changed, no beat removed, and the graded
  evidence beats re-used their existing renders byte-for-byte (confirmed via
  `input_sha256` in `temperature-is-concentration.verified.json`).
- **Library-first, and a real miss.** Ran the Gate L search before authoring
  anything: `./art scenes "everyday analogy: contrast knob rescales differences
  without reordering"`. Five candidates came back and all five were unrelated
  figure scenes — the top hit at score 6.0 was a WCAG contrast-ratio meter,
  which matched on the word "contrast" and nothing else. That is a genuine PUNT,
  so the beat went into the reel's own `scenes.py` as a fourth Manim scene
  rather than being slated. Worth noting the search ranks on text overlap, so a
  word that is a term of art in one domain ("contrast") pulls in matches from
  a completely different one.
- **`./art final` wrote to the wrong folder, and that was my error, not the
  tool's.** The master landed in `brutalist.art/renders/` instead of the reel.
  `RENDER-TARGETS.md` is explicit: destination is `--out DIR`, else `$ART_OUT`,
  else `<toolkit>/renders/` — I had passed none of them, so it used the
  documented fallback. Re-ran with `--out ../week-01-video/reel` and deleted the
  duplicate. The toolkit's own CLAUDE.md rule 3 ("videos travel with their
  book") is the reason this matters: a master sitting in the toolkit is a master
  nobody will find later.
- **The real find: a defect the automated gate structurally cannot catch.**
  Gate V passed the first B01A render — 20 frames, 0 BLOCKER, 0 MAJOR. I ran the
  manual VISUAL QC LAW pass anyway (sample each beat at 15/50/85% of its OWN
  span, then actually look at the PNGs) and at t=18.5s the caption was a pile of
  overlapping letters. Cause: Manim's `Transform()` between two `Text` mobjects
  morphs glyph-by-glyph, and when the two strings have different letter counts
  the in-between frames are unreadable. Four caption changes, four ~1.2s windows
  of garble.
- **Why the gate missed it, which is the part worth keeping.** Gate V samples 20
  frames across 171 seconds — one roughly every 8.6s. A 1.2s defect has about a
  14% chance of landing on any given sample. The gate was not broken and its
  report was not wrong; it was answering a coarser question than the one I
  needed. Fixed at the root with an explicit `FadeOut`/`FadeIn` cross-fade
  (`swap_cap()`), re-rendered, and verified legible at t=20.0s by pulling the
  frame rather than trusting the exit code — the same discipline that caught the
  missing B06 asset on the 17th.
- **Runtime went 2:27 → 2:51.** Still inside the 2–4 minute target with room,
  and the added time buys an on-ramp rather than padding: the analogy beat makes
  a claim (ordering is preserved) that the rest of the video then proves with
  real numbers.

## 2026-09-23 — the analogy pays off, and captions

- **The analogy was an orphan.** B01A introduced the contrast slider and then
  nothing ever referred to it again, so it read as a nice opening image rather
  than a tool. I extended B05 — the boundary beat, the hardest one — to close
  on the callback: *"turn the contrast all the way up on a photo of the wrong
  person, and all you get is a sharper picture of the wrong person."* The three
  swatches return above the `ValueError` card at full contrast. Narration went
  67 → 80 words and the measured beat 23.70s → 26.30s, so the scene was rebuilt
  to the new clock rather than stretched.
- **Expected the callback to be cosmetic; it changed the beat.** I thought I was
  adding a memorable line. What it actually does is give the boundary claim a
  second, non-numeric proof: "concentration ≠ correctness" is abstract, and a
  sharper photo of the wrong person is not. Two encodings of the same claim in
  one beat is stronger than either alone.
- **No captions existed at all.** The reel had run eight builds without a single
  caption file, which for an explainer is an accessibility failure I simply had
  not thought about. `align.py` gets me word-level timing (faster-whisper for
  the timestamps, `SequenceMatcher` to snap the *known* narration text onto
  them, so the caption text is exact rather than a transcription guess) — 10
  beats aligned, 0 fallbacks. But it writes `mp3/words.json`, not SRT: the
  toolkit's SRT writer lives in a `stage_publish.py` that ships with the
  publishing skills, and this toolkit never publishes by design. So I wrote
  `make_srt.py` in the reel.
- **Two bugs in my own SRT writer, both found by checking instead of trusting.**
  (1) The greedy line-wrap filled line 1 to 42 characters and dumped the
  remainder into line 2 — producing 51-character lines. Replaced with a split
  that minimises the longest line. (2) The cue grouper flushed *after* the
  budget was exceeded, so every cue could overshoot by one word. Restructured
  to test the candidate before committing it, and to budget against the
  **wrapped** lines rather than the raw string — a cue can be under 84
  characters and still wrap to a 44-character line, because the split has to
  land on a word boundary. Final: 57 cues, longest line exactly 42, zero cues
  over two lines, zero overlapping or inverted timestamps.
- **Caption offsets come from the clips, not the beat sheet.** My first instinct
  was to accumulate `actual_duration_s`. Those are the audio clock; the clips
  are quantised to 24 fps, and the two differ by a frame or so per beat. Summed
  over ten beats the drift is ~0.33s — small, but it all lands at the end,
  where the outro is. I switched to `ffprobe` on each `clips/<id>.mp4`. The
  clips are what the master is concatenated from, so the clips are the truth.
- **What I got wrong about the rubric, and what it cost.** I set out to push the
  Frictional log past ten entries because I assumed a longer log scored better.
  Reading `prerequisites/frictional.md` properly says the opposite: *"More
  hours, mistakes, commits, or polished prose do not earn extra points,"* and
  it scores five specific criteria instead. Auditing my own log against those
  five, two rows were weak and one was absent — see the two sections below,
  which exist because of that check. Entry count was never the thing.

## 2026-09-25 — the overview contradicted the narration, and I found it by watching

- **What I noticed.** Watching the video through, the overview beat (B01) says
  on screen *"It decides how truthful the answer is"* while the voice is saying
  *"not how truthful it is."* The two most important sentences in the video were
  contradicting each other at the same moment.
- **What the frames showed.** Worse than a timing slip: the correction never ran
  at all. The writer typed the misconception and stopped, and the screen held
  *"a creativity dial … how truthful the answer is"* to the end of the beat. It
  was in every master since the first one. My 2026-09-16 entry above says I sped
  up the typing "to get the correction finished and held" — that belief was
  wrong. The correction had never happened, and nobody had checked the frames
  for it; `CHECKS-REPORT.md` recorded it as working.
- **Why.** The writer component splits the text on whitespace and looks each
  *single word* up in its trigger list. My triggers were phrases, so they could
  never match, and nothing warned. The toolkit's own `SKILL.md` tells authors to
  use phrase triggers — the doctrine and the component it ships disagree. I did
  not change the shared component; I worked within what it actually does: one
  wrong word per sentence (`creativity → concentration`,
  `truthful → concentrated`).
- **Checked before rendering, not after.** Every keystroke takes at least one
  frame at 30 fps, and each correction pauses 1.0–1.5 s, so a correction that
  runs past the end of an 11-second beat gets cut off the same way. The
  component's timeline was simulated first and the simulation was checked
  against the broken render (it predicted typing done at 5.34 s; the frames show
  ~5.0 s). A three-correction version overflowed and was rejected. The one that
  shipped holds the corrected text for ~2 s, and "truthful" turns terracotta at
  ~6.1 s — as the voice says "truthful."
- **A second doctrine field that does nothing.** The beat carries
  `lead_silence_s: 0.8`, which `SKILL.md` requires on this beat. No script in
  the runtime reads it; the voice starts at t = 0. I left the field and recorded
  it here rather than pretend it works.
- **Then I checked everything the same way.** Every beat sampled at 30 / 60 /
  92 % of its span in the final master and read against its script. Two more
  problems, one small and one not:
  - B06 said *"Counts at seed 7, n=1000: 849 / 630 / 469"* — which reads as three
    outcomes in one run, and those sum to 1,948. They are outcome 2 at
    T = 0.5 / 1 / 2. The line now says that.
  - B00 showed three result lines landing under my prompt **as Claude's answer**,
    under a chip reading a real model name. I wrote those lines; Claude never
    produced them. The assignment requires a shown Claude response to be real
    and dated, and a fabricated transcript fails it outright. `SOURCES.md`
    defended them as "the film's own content." Reading the rule again, I do not
    think that holds — a viewer sees Claude answering. I removed them, blanked the
    model chip, and replaced B03's "rendering Manim…" indicator.
- **B01A was ~3 seconds late, and could be heard backwards.** The word timings
  showed "slide it up" spoken at 2.5 s with the slider first moving at 6.0 s. And
  "That is temperature," straight after "slide it up," invites exactly the wrong
  mapping: sliding up is *lower* temperature. The narration now says "run
  backwards: lower temperature, higher contrast," and the whole scene is timed to
  its words. The inversion is not a figure of speech — the slider `k` plays the
  role of `1/T`, because `log p_i − log p_k = (z_i − z_k)/T` (in `FACTCHECK.md`).
- **Human and AI, this time.** I caught the contradiction; Claude found the
  cause, simulated the fix, ran the whole-reel audit, and made the edits. The
  gates and Claude's own QC passes had all missed it: Gate V passed the broken
  beat and the fixed beat identically, because it measures how full the frame
  is, not what the words say. Claude's frame checks earlier this week covered
  only the beats it had changed. I chose to remove the implied Claude responses
  rather than keep them with a label, and to have the B01A inversion said out
  loud.
- **What I understand now.** A report that says a correction happens is not
  evidence that it does, and a gate that passes is not a check on meaning. The
  check that actually catches a contradiction is the plainest one: read what is
  on screen against what is being said, at the moment it is said.
- **Still open.** Why does the writer accept a trigger that can never match, in
  silence? A trigger that matches nothing should be an error, not a no-op.
  **Next step:** raise it — and the unused `lead_silence_s` — as toolkit issues,
  rather than patch the shared component from inside one assignment.

## 2026-09-26 — the video stated its key step instead of showing it

- **What I asked.** With the contradictions fixed, I asked what else would move
  the rubric. The answer was about the argument, not the polish: the step the
  whole video rests on — divide one probability by another and the total
  cancels — was never shown. B02 showed the softmax formula; B04 jumped straight
  to `p₂/p₀ = exp((z₂ − z₀)/T)`. The step between existed only as text on B06
  ("Normalization cancels"), which is what the assignment warns against: *"a
  slide that says 'this is numerically stable' while you talk over it is not an
  explanation."*
- **What changed.** B04 now opens by writing p₂/p₀ as two fractions over the
  same total, Σ exp(z/T). The totals are boxed on "the same total underneath",
  fall away on "so it cancels", and what is left, exp((z₂ − z₀)/T), rises into
  the identity. Narration 61 → 85 words, 21.97 s → 31.25 s, every event timed to
  its phrase from `mp3/words.json`. It pays twice: once the total is gone, T only
  divides the gap, and dividing by a positive number cannot change a sign — so
  the ordering cannot flip at any temperature. That half of the thesis used to be
  a caption; now it follows from the one line shown.
- **Friction: the obvious visual was not allowed.** The natural way to show a
  cancellation is a strike-through. Under `--curve-strict` the layout gate treats
  any stroke crossing a text label as an ERROR, and the gate was not loosened to
  make the picture work. The totals are boxed instead — a box sits outside the
  text — and faded together. Same meaning; the gate passed, 41 snapshots, clean.
- **Friction: a layout that was right but could not be verified.** Gate A
  rejected the first version before rendering: *"explicit coord(s) outside the
  frame, e.g. (-7.5,-0.2)"*. Positions had been computed from `Text.width` at
  runtime, and the render-free check uses stand-in widths, so one evaluated off
  frame. The real render would have been fine — the widths had been measured —
  but a check that cannot verify a position is right to refuse it. The
  coordinates are now pinned from the measured widths (EB Garamond at 44 pt:
  1.95 / 2.45 / 3.23 / 4.39 units), which is the house style anyway, and Gate B
  still checks the rendered pixels.
- **B06 had a claim with half its evidence.** The verdict says outcome two wins
  at every temperature but showed only outcome 2's counts, 849 / 630 / 469 — and
  at T = 2, 469 is not a majority. `main.py`'s own `sample()` was re-run at
  T = 0.5, 1 and 2 (seed 7, n = 1000, Python 3.12.9): all nine counts match the
  course's recorded table, including T = 2's 202 / 329 / 469, now on screen.
- **B07 reads its prompt word for word,** including "2.5" and "why the fixed one
  had to stay fixed", which a listener previously never heard.
- **Found in the code.** `main.py` computes `exp((x − peak) / T)`, subtracting the
  largest score first for numerical stability. The peak cancels in a ratio
  exactly as the total does, so B04's derivation holds for the program as
  written, not only for the textbook formula (`FACTCHECK.md`).
- **Human and AI.** I asked what to improve against the rubric and approved the
  three changes. Claude proposed them, wrote the narration and the scene, chose
  the box when the strike-through was barred, measured the text widths, ran the
  gates, and audited every beat of the final master against its script.
- **Result.** 3:08; captions 58 cues with zero timing errors; all gates clean;
  the whole-reel audit agrees with the narration beat by beat.

## 2026-09-26 — pre-push audit: the folder could not rebuild itself

- **What I asked.** Before pushing, I asked for every deliverable to be checked
  against the rubric — the files themselves, not the earlier summaries of them.
- **The real find: the submission could not rebuild the video.** The pipeline's
  GATE F refuses to render without `SHOTLIST.md`, and it was not in the
  submission folder — so the README's "how to rebuild" could not have worked
  from the folder as submitted. The reel's own copy was also stale: nine beats,
  2:27, and the ask → result pairs that were removed on 2026-09-25. It was
  regenerated from `beat_sheet.json`, so its durations cannot drift, and shipped.
- **Smaller gaps in the instructions.** The README's rebuild step did not copy
  `make_srt.py` or the paperwork set; `BUILD-PROMPT.md` had no `--out` (the master
  would have landed in the toolkit, the mistake logged on 2026-09-22), no caption
  step, and still said "9 mp3s". All fixed.
- **A check that failed, and was left failing on purpose.** `beat_sheet.json`
  fails the toolkit's JSON schema on 14 values — `source: 'manim'` /
  `'remotion'`, `type: 'UI'`. The toolkit's own ai-explainer example fails the
  same way, and the router routes on exactly these values, so the schema is
  stale, not the sheet. Rewriting routing fields the day before the deadline
  would risk the render for no rubric gain; recorded in `CHECKS-REPORT.md`.
- **Then the test that settles it.** A fresh folder holding only the seven files
  the README says to copy, the README's commands run verbatim. Every gate
  passed, all ten beats rendered from scratch, and the rebuilt master was
  byte-identical to the submitted one — same SHA-256, identical audio, identical
  captions, 21 of 21 sampled frames identical. The README now says this rather
  than the weaker claim it made before.
- **Where it is posted, and the commit trail.** Until 2026-09-26 the posting
  lived on a fork (`hemanthrayuduu/info-7375-prompt-engineering-for-generative-ai`,
  branch `week-01-video-rayudu-h`), because my account showed no write access to
  the course repository (`push: false`). The instructor had sent a write-access
  invitation on 2026-09-24 that I had not accepted — GitHub does not switch
  access on until the invitation is accepted. Once it was (via the GitHub API, at
  my instruction), the same commits were merged with the current `main` and
  pushed straight into `fall-2026/rayudu-h/week-01-video/` in the course
  repository, so the trail carries over unchanged: `c31cc13` (2026-09-23, first
  posting, 2:54), `945b4d6` (2026-09-25, overview fixed, implied Claude answers
  removed, 2:56), `f16e9f6` (2026-09-26, cancellation shown, 3:08), `7b388a8`
  (2026-09-26, this audit). The final commit's hash is in the Canvas submission.
- **Human and AI.** I asked for the audit and set the bar (check every
  deliverable before pushing). Claude wrote and ran the checks, found and fixed
  the gaps above, and ran the rebuild test.

## 2026-09-26 — final review

- I watched the final 3:08 cut and approved it for submission. Nothing further
  to change. The review record, with every problem found, who found it, the fix
  and how it was re-checked, is in `REVIEW.md`.

---

## Human and AI contributions (retrospective — added 2026-09-23)

Flagged as retrospective rather than back-dated into the entries above, per the
Frictional guide's instruction to label retrospective entries honestly. The
course AI policy permits using Claude throughout; this records what it actually
did. Prompt excerpts are in `PROMPTS.md`.

**What I did.** Chose the concept from Chapter 1 and rejected two alternatives
(logged in `ROADMAP.md`). Ran `main.py` and verified every number before any
authoring. Set the constraints the build had to satisfy — free pipeline only,
real numbers only, one concept, a boundary beat. Made every judgement call
about what the video claims and refuses to claim. Decided the toolkit must stay
unmodified, which forced the outro rewrite. Directed each revision, including
the two in this final pass.

**What Claude (Claude Code) contributed.** Drafted and revised the narration
against my register and length constraints. Authored `beat_sheet.json` to the
toolkit schema. Wrote the Manim code in `scenes.py` to my beat designs. Ran the
gate/fix loop and the frame-level QC passes. Wrote `make_srt.py`. Drafted the
paperwork, including this file, from the real build record.

**What I accepted.** The gate refusals — `./art final` blocking a master with a
slate in it, and GATE A flagging my text-only B04 — were right every time, and
I fixed causes rather than overriding checks.

**What I changed or rejected.**
- Rejected a full "explain it like I'm five" rewrite that would have dropped the
  identity and the ten-digit ratios. The rubric pays 15 of 25 for *showing the
  mechanism with real numbers*; trading that for approachability is a bad deal.
  Kept every figure and added the analogy as an on-ramp instead.
- Rejected the first analogy framing I was offered as decoration. An analogy
  earns a beat only if it is faithful: the contrast slider works because
  `v = mid + (b − mid)·k` is a positive affine map and cannot reorder its
  inputs — the same reason dividing logits by `T > 0` cannot reorder a softmax.
  I required that argument in writing before the beat was built; it is in
  `FACTCHECK.md`.
- Rejected padding this log to eleven entries once I read what it is actually
  scored on.
- Changed the caption cue budget twice after reading the output rather than the
  exit code.
- Rejected the ask→answer opening the toolkit prescribes for B00 (added
  2026-09-25): it showed words I wrote as Claude's reply. The prompt stays; the
  "answer" is gone.

**What I have not verified myself.** I have read and can explain every line of
`scenes.py` and every field in `beat_sheet.json`, and I re-derived the softmax
figures independently of the video. I have *not* independently re-implemented
`align.py`'s alignment algorithm — I checked its output (10/10 beats aligned, no
fallbacks, caption text matches the narration verbatim) rather than its method.

---

## What I understand now, and what I still do not (added 2026-09-23)

**What changed in my understanding.**

- *Temperature's whole effect fits in one exponent, and that is not a
  simplification.* I started out thinking of temperature as "sharpening the
  distribution," which is true but vague. Working the ratio
  `p_i/p_k = exp((z_i − z_k)/T)` showed me the normalizing constant cancels, so
  there is nothing else for temperature to touch — the entire mechanism is one
  exponent over a fixed score gap. That is why it cannot reorder anything, and
  the reason is algebraic, not empirical.
- *"Concentration is not correctness" is a claim about information, not about
  probability.* The distribution can be made arbitrarily sharp and still be
  sharp about the wrong thing, because nothing in the rescaling introduces new
  evidence. That is the boundary, and it is the part of Chapter 1 I would have
  skimmed past.
- *A gate that passes is not the same as a thing that is correct.* Gate V
  reported 0 BLOCKER / 0 MAJOR on a beat whose captions were an unreadable pile
  of letters for 1.2 seconds. The gate samples 20 frames across 171 seconds; a
  1.2-second defect falls between samples about 86% of the time. The check was
  not broken — it was answering a coarser question than the one I needed.
- *An analogy is only worth a beat if it is faithful.* The contrast slider earns
  its place because `v = mid + (b − mid)·k` is a positive affine map, which
  cannot reorder its inputs — structurally the same reason temperature cannot.
  If I had not been able to state that, it would have been decoration.

**What I still do not understand, and what I would check next.**

- *How far the toy generalizes.* Everything here is a softmax over three fixed
  scores. The ordering argument is algebraic and should hold for any logit
  vector, but I have not tested whether the intuition survives contact with a
  real model, where the logits themselves shift with context. **Next step:**
  run the same ratio check across two prompts that differ only in context and
  see whether the *gap* is anything like stable.
- *Whether the analogy helps or quietly misleads.* Contrast is linear in
  brightness; softmax is exponential in the logits. I caption the beat as an
  analogy and B04 supplies the real magnitudes, but I have not shown the video
  to anyone who did not already know the material, so "this makes it clearer"
  is currently my assumption rather than a finding. **Next step:** show it to
  two people outside the course and ask them to state the boundary claim back.
- *Why the ratio is the natural object to look at.* I can derive that
  normalization cancels, and I can see that it makes temperature's effect
  visible in one term. I cannot yet say whether the ratio is *the* right
  invariant or simply the most convenient one — whether there is a principled
  reason pairwise ratios are the thing to reason about in a softmax rather than
  some other functional of the distribution. **Next step:** look at how the
  log-odds formulation is used in the chapter's later material.
- *Whether the QC gate should sample per beat.* My defect argues it should, but
  I do not know the cost — per-beat sampling at 15/50/85% is 30 frames for this
  reel instead of 20, which is cheap here and might not be for a long one.
  **Next step:** raise it as a toolkit issue rather than assume my reel's shape
  generalizes.
