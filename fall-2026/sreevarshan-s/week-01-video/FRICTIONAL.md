# FRICTIONAL — Week 1 explainer video

Format follows `prerequisites/frictional.md`.

> **Authorship notice, read this first.** The guide says: *"AI can organize your
> notes; you must supply the actual experience."* Everything below marked
> **[build log]** is a factual record of what happened mechanically during an
> AI-assisted build session on 2026-09-22 — commands, failures, fixes. It is
> organized by Claude, and it is true, but it is **not** a record of the
> student's own experience or understanding.
>
> The sections marked **[YOUR ENTRY — to write]** are deliberately empty.
> They carry the rubric rows that only you can earn: your attempts, your
> confusion, what you accepted or rejected, what you still do not understand.
> Submitting this file with those sections blank will lose those points, and
> filling them with invented difficulty would be exactly what the guide forbids.

---

## 2026-09-22 — [build log] Orientation

- **Tried:** locate anything on tokenization already in the course repo before
  writing new code. Expected lesson 1 to have a tokenizer example.
- **What happened:** it does not. Lesson 1 is softmax/temperature sampling with
  a deliberate three-token toy model. The concept text is in
  `chapters/01-randomness-and-first-prompts.md`, which states that character
  tasks ask the machine "to reason about a unit it does not natively see."
  `requirements.txt` is standard-library-only by course policy.
- **Decision:** install `tiktoken` into the *toolkit's* venv, never the course
  repo, so the no-dependency policy is preserved. `AGENTS.md` explicitly allows
  the external brutalist.art checkout as a media-tool exception.

## 2026-09-22 — [build log] Schema read, not guessed

- **Tried:** find the real beat-sheet schema rather than copy an example.
- **What happened:** `runtime/scripts/beat_plan.py` is the authority. A beat
  routes to Manim via `shot.manim` / `graphic.manim` / `shot.source: "manim"`.
  A trap: `beat.engine` is `"kokoro"` for audio, so setting `engine: "manim"`
  would have silently conflicted. Used `shot.source: "manim"` instead.
- **Also found:** `run.sh` Gate F refuses to render unless `FACTCHECK.md`,
  `SHOTLIST.md` and `PROMPTS.md` exist, and refuses Manim beats without a
  reel-local `scenes.py`.

## 2026-09-22 — [build log] Claude API checkpoint — the required stop

- **Checked:** `ANTHROPIC_API_KEY` unset. `ANTHROPIC_BASE_URL` set, `claude`
  CLI present, no `.env` anywhere. So: **no API access** by the assignment's
  definition.
- **What happened:** the build **stopped** and asked, rather than generating a
  plausible transcript. Nothing was written to any evidence file at this point.
- **Resolution:** the student obtained the response from claude.ai web chat and
  supplied it with provenance. Recorded verbatim in
  `evidence/claude_response.md`. Between receiving the text and receiving the
  date/model, the provenance fields were held as
  `NOT SUPPLIED — student to fill in` rather than assumed.

## 2026-09-22 — [build log] The demo did not fail, and the script was rewritten

- **Expected:** the model would miscount the r's. The whole rev-1 script was
  built on that, including the cold-open line "a language model cannot do it."
- **What happened:** Claude Sonnet 5 answered **correctly** — "There are 3 r's".
- **Response:** the claim was cut as overstated rather than kept for drama, and
  the video was re-aimed at the harder question: it was right, using what?
  A third evidence script (`id_is_arbitrary_demo.py`) was added to support the
  new claim, showing id 73700 sits between `' Smoking'` and `' CMP'`, and that
  `' straw'` is id 31107 — so the integer carries no spelling.
- **Why this matters:** the honest version is stronger. "Correct by recall, not
  by inspection" is a real mechanism claim; "the model can't count" would have
  been false on the evidence collected.

## 2026-09-22 — [build log] Gate A blocked the render three times

- **Attempt 1:** `./art run` exited 2. Gate A: *"B01_ClaudeTranscript — shapes
  never change, 1 distinct shape-state across 7 frames."* The transcript beat
  was a static card.
- **Fix:** gave B01 real motion — the card is drawn, a rule is drawn across it,
  and a marker travels from the question to the "3" in the answer. Clean.
- **Attempt 2:** pre-flighted all 11 scenes before re-rendering rather than
  discovering failures one render at a time. Two more errors: `B04_IsolatedSplit`
  and `B08_LearnedNotGiven`, same cause.
- **Fix:** B04 got a marker that travels box to box as each r-count lands.
- **Attempt 3:** B08 still failed after adding a `SurroundingRectangle`
  transform. Cause: Gate A is a *static* AST checker and cannot resolve a
  `SurroundingRectangle` whose geometry depends on another mobject, so both
  states collapsed to one. Replaced with explicit `Rectangle(width=…, height=…)`
  at explicit coordinates. Clean.
- **Attempt 4 (Gate B, post-render pixel check):** two more blocks, both found
  only after rendering. First, the word `correct` in B01 sat at y −3.45 against
  a −3.40 safe line — a 0.05-unit miss. Raised that margin and pre-emptively
  applied the same fix to the shared citation helper and the B07 stamp rather
  than waiting to be told twice.
- **Attempt 5:** `B02_TextToIntegers` failed with **40** text-on-text errors.
  The sentence had been built as one `Text` object per character so the letters
  could animate individually; after scaling to fit the frame, adjacent glyph
  boxes overlapped by up to 100% and the gate counts each character as its own
  text object. Rebuilt the beat around a single `Text`. Worth noting the same
  pattern in B00 passed — larger glyphs, wider spacing — so the failure was
  about scale, not about the technique.
- **Nothing was worked around.** No gate was disabled; `ART_QC` and `ART_STRICT`
  were left at their defaults.

## 2026-09-22 — [build log] Gate V, and the defect no gate caught

- **Gate V** (frame-level QC on the compiled cut) rejected the reel three times
  for `underfill` — content covering as little as 16% of the safe area against
  a 55% minimum. The house style wants a full frame; my first layouts were
  small type floating in cream. Fixed by scaling type up throughout, running
  layouts full width, and getting the whole composition on screen by about a
  third of the way into each beat instead of at the end. 19 → 6 → 0 defects.
- **A real bug of mine:** `scale_to_fit_width` constrains one axis only. On a
  short, wide group it scaled *up* until B05's content sat at y ±5 in a frame
  that ends at ±4 — text entirely off screen. Replaced with a `_fit()` helper
  that takes the smaller of the width and height ratios.
- **The compiler was also silently stretching my scenes.** The log showed
  "B09: clip 8.2s slowed 2.86x to fill 23.5s beat" — near-3× slow motion,
  because I had written the animations shorter than the narration. Measured
  every beat with ffprobe, put the real durations in a `DUR` table, and added a
  `_hold()` helper so each scene runs out to its own narration length. No clip
  is stretched in the final.
- **The one that matters most was found by looking, not by a gate.** After
  every gate passed, I pulled the B01 frame and read it: the highlight box
  around the "3" was clipping the neighbouring glyphs, so the verbatim Claude
  quote on screen no longer read the way it was received. A second look after
  fixing that caught `3r's` — Manim strips leading spaces from split text
  fragments. Both are fixed and re-verified from the exported master.
  This is the concrete case for the toolkit's rule that a probe is not
  verification: the file was valid, the gates were green, and the quote was
  still wrong.
- **House-style deviation, recorded not hidden:** the compiler warns that
  `graphic` carries 11/11 beats (100%) against a ~40% cap for one visual
  language. That is a direct consequence of making every beat reel-local Manim,
  which was chosen so nothing in the shared public toolkit had to be edited.
  Advisory only; it does not block.

## 2026-09-22 — [build log] A defect every gate missed, caught by watching

- **Reported by the student after frame-by-frame review:** garbled glyphs at the
  "What the model is handed" beat. Their timestamp (~15s) pointed at B01, but
  sampling at 0.1s put the real fault at 24.2–24.7s in B02. Their *diagnosis*
  was exactly right: a transform passing through an intermediate glyph-matching
  state. `TransformFromCopy` creates its copy on top of the source and animates
  it to the target, so the sentence was briefly drawn twice, then morphed into
  unreadable fragments — "How m any r's are in st raw ber ry?".
- **Fixed** by replacing it with a plain `FadeIn` of the integer row. The two
  elements sit at different heights anyway, so the morph bought nothing.
- **Auditing for the same class found two more.** B00's counter used
  `Transform` between `Text` mobjects (one blob frame per tick, two on
  "3"→"three"), and B01's underline swept across a label like a strikethrough.
- **The first fix for B00 was not good enough and the frames said so.** A
  simultaneous crossfade still put "3" and "three" on the same frame, reading
  "th3ee". Made the fades strictly sequential — out, then in — so no frame
  contains two glyph states. Only re-pulling the frames showed this.
- **What I take from it:** every gate was green before and after this defect
  existed. Gate A checks that shapes move, Gate B checks pixel margins and
  overlap of *static* bounding boxes, Gate V samples two frames per beat at 50%
  and 85% — none of them inspect glyph legibility mid-animation, and a 0.5s
  fault can fall between the sampled frames entirely. Automated QC bounds the
  failure modes someone thought to encode; it does not replace watching.

## 2026-09-22 — [build log] Polish pass: measured, not eyeballed

- **Method:** pulled a frame 2s into each of the 11 beats and measured ink
  bounding boxes programmatically rather than judging by eye, then re-measured
  the same checkpoints after the change.
- **Alignment:** B01–B09 were already consistent to 9px. The outliers were
  B00 (0.22u low) and B10 (0.98u low), both hand-placed instead of going
  through `_title()`. A subtler cause: `_title()` centred the bounding box, so
  a header with a descender sat higher than one without. Switching to a
  top-edge anchor fixed both classes at once — spread went 132px → 1px.
- **What I chose not to "fix":** body left-edges vary by 673px, which looks
  like drift in a table but is not — most beats are centred compositions of
  different widths. Forcing a common left edge would have damaged them.
- **Pacing:** the real problem was not the cuts but the distribution. Six beats
  finished animating in their first third and then froze for 10–17s while the
  narration kept going; B06 had the opposite fault and cut out 0.5s after its
  last movement. Restretching the existing waits (no new content, no changed
  reveal speeds) moved the finish line to 51–75% across the board.
- **Constraint respected:** total runtime is identical at 181.75s because every
  scene still ends via `_hold()` at its measured narration length — the added
  waits come out of the static tail, not out of the clock.

## 2026-09-25 — [build log] Weight pass, and the same bug class a third time

- Raised type weight across the deck (body SEMIBOLD, mono BOLD, headers and key
  numbers HEAVY). Palette untouched, typefaces untouched.
- **The predicted risk was real, and it was my own helper that caused it.**
  Heavier glyphs are wider, so I clamped the two fixed-width containers with
  the `_fit()` helper I had written earlier — forgetting that `_fit()` takes
  `min(w_ratio, h_ratio)` and therefore *enlarges* a group that is smaller than
  its box. B06's table rows were scaled **up** past their plates; the
  descenders on "Smoking" and "strawberry" collided with the rows below.
- This is the third appearance of one root cause: a scale helper that grows
  content when asked to constrain it (first `scale_to_fit_width` on B05, then
  `_fit` as a clamp on B06/B08). Fixed properly this time by adding a separate
  shrink-only `_clamp()` that can never scale above 1.0, rather than reusing a
  fit helper for a clamp job.
- Again the gates were green while the defect existed — Gate W measures static
  bounding boxes of *text against text*, not text against the box it is
  supposed to sit inside. Caught by pulling the frame at full resolution.
- End credit added inside B10's existing static tail, so total runtime is
  unchanged at 181.75s.

## 2026-09-25 — [build log] A defect whose cause was neither proposed explanation

- Reported: caption text across the deck showing merged words. Two plausible
  causes were on the table — a fit-to-width squeeze, or the new bold weight.
  **Both were wrong, and checking beat guessing.**
- No width constraint exists on caption text; grep showed every scaling call
  targets token-box groups. And rendering the same string at NORMAL and
  SEMIBOLD at size 20 produced identical merging, so weight was not the cause
  either — it only made an existing defect easier to see.
- The real cause: Manim 0.18.1 rounds the inter-word space advance to
  approximately zero below ~22px for this typeface. A render sweep over sizes
  20/21/22/23/24/26 at two weights located the threshold exactly: 20 merges
  badly, 21 partly, 22 and above are clean.
- This matters because the obvious remedy — *reduce* the caption size so the
  bolder strings fit — would have pushed it further below the threshold and
  made it worse. Fixed by raising the caption style to 23.
- My first measurement attempt was also wrong: I compared glyph bounding-box
  gaps in the mobject and concluded the spaces were present (ratio 7.9). They
  are present in geometry but round away in the rendered raster. Only pulling
  actual pixels settled it. Second time this session that mobject geometry
  disagreed with the render, and the render was right both times.

## 2026-09-22 — [build log] Timing

- Estimated durations in the beat sheet summed to 3:39. Real Kokoro audio came
  in at **181.6 s (3:02)** — Kokoro speaks faster than estimated. Inside the
  2–4 minute window, so nothing was padded or cut to hit a number.

---

## [YOUR ENTRY — to write] Your attempts

*Rubric row: "Specific things you actually tried and what you expected." What
did you try yourself before or alongside this build? What did you predict the
model would answer, and were you right?*

## [YOUR ENTRY — to write] Friction and response

*Rubric row: a confusion, unexpected result, difficult decision, or assumption
checked. The honest candidate here: the demo did not fail the way the concept
predicted. What did you make of that? Do not invent difficulty — if a part was
straightforward, say so.*

## [YOUR ENTRY — to write] Human and AI contributions

*Rubric row: what you did, what Claude contributed, and what you accepted,
changed, rejected, or still do not understand. `SOURCES.md` lists the mechanical
split; this row wants your judgement on it. Name at least one thing you changed
or pushed back on after watching the cut.*

## [YOUR ENTRY — to write] Learning and uncertainty

*Rubric row: what changed in your understanding, or what remains unresolved.
One genuinely open question this video does not answer: since Anthropic does not
publish Claude's tokenizer, we never established how Claude splits this word —
only how two OpenAI vocabularies do. What would you need to settle it?*

## [YOUR ENTRY — to write] Traceable process

*Rubric row: dated entries connected to commits, prompts, outputs or tests.
Add your commit hash once pushed. The outputs are already here:
`evidence/*.txt`, `evidence/claude_response.md`, `FACTCHECK.md`.*
