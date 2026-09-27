# FRICTIONAL — tool execution log and friction points

"The Token That Followed" · INFO 7375 Week 01 · built 2026-09-22 on macOS (Darwin 25.6.0),
Python 3.12.12, Node 24.14.1, ffmpeg 8.0, Claude Opus 5 in Claude Code.

Every friction point below is a real thing that cost time or nearly produced a wrong
build. Total spend across the whole build: **$0.00** — no paid API was called.

---

---

## Revision — 2026-09-23: rebuilt for a 4:00 floor and a beginner audience

**Why the runtime changed.** The professor said in class on **[DATE — TO BE FILLED IN]**
that this video should run **at least 4:00**, overriding the written 2–4 minute syllabus
target. This was a **live-class comment, not a Canvas update** — there is no written
source for it, nothing in the syllabus or the assignment brief was edited, and the
instruction exists only as something said aloud in the room.

> **Open item for the author:** I have left the date as a placeholder rather than
> guessing it. `AGENTS.md` forbids fabricating provenance, and a date attached to a
> named person's spoken instruction is provenance. Replace `[DATE — TO BE FILLED IN]`
> above with the actual class date before submitting. Everything else in this entry is
> verified.

**What changed.** The 3:16 cut was re-authored, not padded. It was restructured from the
ai-explainer bookend arc (cold open → BLUF → body → verdict → handoff → outro) into the
six-act teaching structure the brief specifies, for a viewer who has never heard of
next-token prediction:

| Act | Beats | Measured | What it does |
|---|---|---|---|
| 1 Hook | B00 | 14.45s | The false sentence in plain English, the question asked, then a real pause |
| 2 Mechanism | B01–B07 | 150.27s | Tokens → the answer key → the five-step softmax ladder |
| 3 Contrast | B08 | 25.44s | The same model against a TRUE corpus; the target moves |
| 4 Loss | B09 | 20.33s | The penalty reads the next actual token, whatever its truth value |
| 5 Boundary | B10 | 34.06s | What this does not establish, with real screen time |
| 6 Takeaway | B11 | 9.31s | One sentence, no new claims |
| | **12** | **253.86s = 4:13.86** | clears the 4:00 floor |

**New in this cut.** Four new components (`Ch1PretrainHook`, `Ch1PretrainLadder`,
`Ch1PretrainContrast`, `Ch1PretrainTakeaway`), the max-subtraction step shown on screen
for the first time, and `build_beat_sheet.py`, which builds every scene prop from
`verify_softmax.py --emit` so no on-screen number is hand-typed.

**Dropped from this cut.** `Ch1PretrainGradient` (the p − y beat) and the three
`ClaudeComposerAsk` beats. The six-act structure has no ask/handoff slot, and the brief's
standing constraint — *any Claude response shown must be a real one you actually got,
dated* — means a composer beat whose RESULT lines I authored to look like a reply is
exactly the wrong thing to render. Rather than fabricate or stage a Claude response, the
cut contains no Claude interface at all. The components remain registered and indexed;
they are simply not used by this reel.

## A. Execution log

| # | Step | Command | Result |
|---|---|---|---|
| 1 | Locate the toolkit | `git status --short \| wc -l` | 8449 deletions — the tracked tree is gone; the toolkit is the `brutalist.art/` clone |
| 2 | Readiness | `./art doctor` | all 7 features green, `$0.00` |
| 3 | GATE L search | `./art scenes "softmax probabilities over candidate tokens, logit scores, next-token prediction"` | 8 leads, **genuine miss** — none is a distribution/logit/loss/gradient scene |
| 4 | GATE L prop checks | `./art scenes --check ClaudeComposerAsk` (×4) | all RENDERABLE; prop lists truncated (see #5) |
| 5 | Pick the logits | grid search over half-integers | 35 sets give 4-dp probabilities summing to exactly 1.0; took `4.0 / 1.0 / 0.0 / −0.5` |
| 6 | Prove the arithmetic | `python3 verify_softmax.py` | ALL ASSERTIONS PASSED |
| 7 | Write components | 9 files, `Ch1Chrome` + 8 scenes | — |
| 8 | Typecheck | `npx tsc --noEmit -p .` | 0 errors |
| 9 | Renderability | `npx remotion compositions src/index.ts` | all 8 `Ch1Pretrain*` listed at 1920×1080/30 |
| 10 | Scene index | `./art scene-index` | 610 → **618** renderable, 0 unresolved |
| 11 | Audio, pass 1 | `generate_audio_kokoro.py <REEL>` | 13 mp3s, **4:13** — over the 4-minute cap |
| 12a | Trim + audio, pass 2 | `rm mp3/*.mp3` then regenerate | 602 words → **3:42** |
| 12b | Re-time to ~3:15, pass 3 | trim 9 beats, `rm` only those mp3s, regenerate | 532 words → **3:16** (195.63 s decoded) |
| 13a | Render beats, pass 1 | `remotion_scenes.py <REEL>` | **halted at beat 5** — QC of B04 found the sum row truncated away (see #13) |
| 13b | Fix + re-render | add `durationS` + `calculateMetadata`, then `remotion_scenes.py <REEL> --force` | 13 scenes, each spanning its measured window |
| 14 | Compile | `./art run` → `./art final` | see §C |
| 15 | Visual QC | `ffmpeg -vf fps=2` + read the PNGs | `_qc/REPORT.md` |
| 16 | Re-prove | `python3 verify_softmax.py` | ALL ASSERTIONS PASSED (post-build) |

## B. Friction points

**1. The repository's working tree was empty of the toolkit.**
`git status` reported 8,449 deleted tracked files at the parent, and the actual toolkit
was an untracked fresh clone at `brutalist.art/`. Anything run from the parent would
have found no `art`, no `runtime/`, no scenes. *Fix:* treat `brutalist.art/` as
`ART_HOME`; never assume the repo root is the toolkit root.

**2. `./art` cannot see this machine's venv.**
`art` and `setup` both auto-activate only `$ART_HOME/.venv`. The venv here is one level
up, at `/Users/rithika/Downloads/brutalist/.venv`, so `art` silently used the system
`python3` and every feature reported red. *Fix:* export `VIRTUAL_ENV` and prepend its
`bin` to `PATH` on every invocation. This matches a standing note in the project's
memory; it is a real, repeating papercut, and a symlink
`brutalist.art/.venv → ../.venv` would retire it permanently.

**3. I misdiagnosed the TTS dependency and nearly "fixed" a non-problem.**
Probing for the obvious module names — `kokoro`, `torch`, `soundfile` — returned three
`ModuleNotFoundError`s, which reads like a blocking install of a multi-gigabyte
PyTorch stack. It was wrong: the toolkit uses **`kokoro-onnx`**, which needs no torch,
and the 325 MB `kokoro-v1.0.onnx` plus `voices-v1.0.bin` already ship in
`runtime/models/kokoro/`. *Lesson:* `./art doctor` is the authoritative readiness
check; hand-probing guessed module names produces false blockers.

**4. `./art scenes --check` prints a truncated prop list that disagrees with the component.**
The check reported `BrutalistHesitantWriter` as having six props
(`text, face, fontSize, lineSpacing, align, ink`). Its zod schema actually has
nineteen, including the `triggerWords` / `replacementWords` / `seed` / `banner` props
that EXECUTIVE-SUMMARY LAW *requires* an author to set. Authoring from the check alone
would have produced a beat 2 with no correction in it — the exact defect the law
exists to prevent. *Fix:* read the component source; treat `--check` as a
renderability probe, not a prop contract.

**5. `BrutalistHesitantWriter` silently ignores multi-word `triggerWords`. (Toolkit bug.)**
`ai-explainer/SKILL.md` instructs, with a worked failure example, that "when the
misconception lives in a phrase, put the whole phrase in `triggerWords`." The
component cannot honour that: it splits `text` on whitespace and compares each
single-word core against the trigger list, so a multi-word trigger never matches and
**fails silently** — the beat renders with no correction and no warning. *Workaround:*
a single-word trigger, `facts` → `sequences`, chosen so the corrected sentence
("Pretraining learns sequences.") still stands alone as the reel's claim. *Real fix:*
match trigger phrases across token runs, or validate triggers against the text and
raise. Verified the correction landed by sampling the beat's final frame.

**6. `ClaudeTitleOutro` hardcodes another channel's handle.**
The obvious component for OUTRO LAW has `@NikBearBrown` compiled in with no prop, and
`OUTRO-LOCK.md` scopes it to claude-liam reels: "Other channels use their own outro
components — never this one." Using it would have published a course submission under
someone else's channel handle. *Fix:* wrote `Ch1PretrainOutro`, keeping the law's
substance (exact title restate, poster serif, terracotta period, handle beneath).

**7. The docs overstate voice enforcement.**
`HOW-TO.md` states "Any other voice code is rejected by the audio script," implying
only `af_bella` and `am_onyx` are usable. No such allowlist exists in
`generate_audio_kokoro.py` — all 54 Kokoro voices resolve, and `--list-voices` prints
them. Harmless here (`af_bella` was wanted anyway, and it is one of the two documented
voices) but the doc would mislead anyone choosing a voice.

**8. Stale schema text: `voice_id` still documents ElevenLabs.**
`runtime/schema/beat_sheet.schema.json` describes `metadata.voice_id` as an
"ElevenLabs voice ID; resolved from `ELEVENLABS_VOICE_*` in `.env`" although
ElevenLabs was permanently removed (commit `7ee2da6`) and there is no `.env`. Left the
field unset. Cosmetic, but it invites an author to configure a vendor that is gone.

**9. `shot.source: "remotion"` is in the shipped examples but not in the schema.**
`examples/ai-explainer/claude-debunked/beat_sheet.json` uses it; the enum permits
`own | archive | capture | screen | gen | …` and not `remotion`. Used `own`, which is
what the pipeline actually means by "the pipeline animates it."

**10. The first audio pass overran the assignment's cap, and timing cannot be hand-fixed.**
Narration of 698 words measured **4:13** against a 2–4 minute requirement. Because the
measured MP3 durations *are* the clock, the only correct fix is fewer words — so ~100
words of number-reciting narration were cut (which also tightened SHOW-DON'T-TELL
compliance: the figures were already on screen) and the audio regenerated to **3:42**.
A later pass to a ~3:15 target repeated the exercise — nine beats trimmed to 532
words for a measured **3:16** — and confirmed the discipline scales: each re-time is
cut words → regenerate → re-sync `durationS` → re-render only the beats whose
measured duration actually moved (four of thirteen survived pass 3 untouched).
*Correction (2026-09-23):* I wrote here that `generate_audio_kokoro.py` "skips beats
whose MP3 already exists." **That is wrong** — see #22. The script has no skip logic at
all and re-synthesises every beat on every run. Deleting the stale clips was harmless
but unnecessary; the reason the kept beats reported identical durations is that Kokoro
is deterministic, so the same text produced the same audio.

**11. Concurrent write hazard on the beat sheet.**
`remotion_scenes.py` stamps render provenance back into `beat_sheet.json` with an
atomic replace. Editing the beat sheet while it runs races that write and can discard
the edit. *Practice:* let the renderer finish before touching the sheet.

**12. Rendering is the long pole.**
Each beat renders at `--scale=2` (true 3840×2160, PNG frames, CRF 16) at concurrency 1,
which costs a couple of minutes per beat — roughly half an hour for thirteen beats on
this machine. Worth knowing before scheduling a rebuild; it is a quality choice, not a
misconfiguration.

**13. A composition registered LONGER than its audio loses its late reveals, silently. (The worst bug of the build.)**
`remotion_scenes.py` renders a composition at its registered length and then conforms
the clip to the beat duration with `ffmpeg -t`. Extending is handled explicitly
(`tpad=stop_mode=clone`), but **shortening is just truncation, and nothing warns.** My
`Ch1PretrainLogits` was registered at 720 frames (24 s) against 16.90 s of audio, so the
render was cut at 70% progress — and the `Sum exp(z) = 58.9230` row, which reveals at
74-84% and is the entire point of the beat, **was not in the file.** The clip was the
right duration, had video and audio streams, and was completely wrong. Five other beats
had the same defect (`Ch1PretrainSoftmax` lost `Sum p = 1.0000`, `Ch1PretrainGradient`
lost `Sum (p - y) = 0`, `Ch1PretrainTarget` lost most of its cross-out,
`Ch1PretrainOutro` lost its credit line).

*Fix:* adopted the toolkit's own `calculateMetadata` convention — a `durationS` prop on
each of the eight schemas, and
`calculateMetadata={({props}) => ({durationInFrames: Math.round(props.durationS * 30)})}`
on each `<Composition>` — with `durationS` written from the beat's **measured**
`actual_duration_s`. Every scene now spans exactly its spoken window, so the reveals
distribute across the real clock instead of a frame count guessed at authoring time.

*Lesson:* this is precisely why VISUAL QC LAW insists the mp4 probe is a FILE check and
never counts as QC. Duration and frame count were perfect on a broken beat; only reading
a rendered frame found it.

**14. My own token-index error, caught the same way.**
`Ch1PretrainCorpus` takes a `focusIndex` for the conditioning token that gets the
accent. I passed `4`, counting "green" by eye; in `The moon is made of green cheese`,
`green` is index **5** and index 4 is `of`. The reel rendered with the terracotta accent
on the preposition — a beat about which token is being conditioned on, highlighting the
wrong word. Nothing could have caught this except looking at the frame.

*Fix:* the beat sheet now derives it — `props["focusIndex"] = tokens.index("green")`,
asserted — so the index cannot drift from the sentence it describes.

**15. `lead_silence_s` is mandated by the skill and implemented by nothing.**
EXECUTIVE-SUMMARY LAW is explicit about beat 2: *"narration of 20-35 words plus an
explicit `lead_silence_s: 0.8` written on the beat — it is not defaulted, and B01 is
exactly where the typing needs the head start."* A grep for `lead_silence` across
`runtime/scripts/` returns **nothing** — no script reads the field, so writing it has
no effect on the render. An author following the law would reasonably believe beat 2
had been given its head start.

*What I did:* kept the field, because the law requires it to be written and a future
pipeline may honour it, and then satisfied the law's actual intent by measurement
instead of by declaration — B01's audio window is **11.83 s** (the law's floor is 9 s),
and I confirmed from the beat's final rendered frame that the `facts` to `sequences`
correction is fully on screen before the cut. The substance holds; the mechanism the
law names does not exist.

*Side effect worth stating plainly:* the reel's runtime is therefore **195.63 s
(3:16)** in the decoded master, not the 196.18 s that summing the sheet's durations
plus the declared lead silence would suggest. The 0.8 s is never inserted.

**16. GATE V measures the ink BOUNDING BOX, not ink density — which changes how you fix an underfill.**
The first compiled cut failed Gate V with 0 BLOCKER and 6 MAJOR, all of them
`underfill`: B01 at 41%/53%, B10 at 41%/41%, B12 at 16%/20%, against a 55% floor. My
first instinct was to add more content. Reading `runtime/qc/final_frame_check.py`
showed that the metric is

```
cover = (x1 - x0) * (y1 - y0) / (SAFE.w * SAFE.h)
```

— the bounding box of all non-background pixels over the safe area. So *extent* is what
scores, not how much is drawn. That explains why the eight `Ch1Pretrain*` beats all
passed without effort: `Ch1Stage` pins the spark line to SAFE's top edge and the course
bug to its bottom-right, so every scene inheriting the chassis already spans the canvas.
The three failures were exactly the three beats that do **not** use `Ch1Stage`.

Three different fixes, because the three beats permit different things:

- **B12 `Ch1PretrainOutro` (mine — 16% → 97.6%).** Restructured: the eyebrow is anchored
  to SAFE's top edge and the credit rail to its bottom edge, with the title spanning the
  width between them. It still reads as a spare poster; the negative space is now inside
  a frame that claims the canvas, which is the distinction FILL-THE-CANVAS actually
  draws ("deliberate negative space for emphasis is legal … accidental dead space under
  undersized content is the defect this law kills").
- **B10 `ClaudeVerdictArtifact` (shipped — 41% → 57.9%).** A fidelity component with no
  size props; its height is driven by line count and wrapping. So instead of forking its
  layout I stated the recap more fully and added a fourth line naming the boundary the
  viewer just heard in B09. Content change, not a layout hack.
- **B01 `BrutalistHesitantWriter` (shipped, mandated verbatim — 46.9% → 59.5%).** This
  one was subtler. It passed at the 85% sample and failed at 50%, because Gate V samples
  each beat at 50% and 85% of its span and at 5.9 s the sentence was **still being
  typed** — a narrow bbox around half-written text. Raising the type size alone would
  not have fixed the 50% sample. The fix was to let the sentence FINISH before the first
  steady-state sample: a shorter third line, `charMs` 26 → 10, and the decorative
  hesitations (`mistakeRate`, `hesitateWithin`, `hesitateBetween`) set to zero. The ONE
  hesitation that carries meaning — `facts` → `sequences` — is untouched, because that
  correction is the beat's entire pedagogy.

*A trap worth naming:* the obvious lever on B01 is `fontSize`, but the component sets
`whiteSpace: 'pre'`, so it never wraps. Past roughly 90 px the longest line runs past
the title-safe edge, which would have traded an `underfill` MAJOR for an `edge-bleed`
**BLOCKER**. I measured the fix against the gate's own `analyze_frame` on extracted
frames before recompiling, rather than paying a full 4K re-encode per guess.

**17. SKIN LINT flags the custom outro, correctly, and it stays.**
The compile prints `SKIN LINT: B12: palette=claude but the outro is
'Ch1PretrainOutro' — OUTRO LAW wants ClaudeTitleOutro`. This is a warning, not a gate,
and it is the lint noticing the deliberate deviation documented in `SOURCES.md` §5:
`ClaudeTitleOutro` hardcodes the `@NikBearBrown` handle with no prop override, and
`OUTRO-LOCK.md` scopes it to claude-liam reels — "Other channels use their own outro
components — never this one." Using it would have shipped a course submission under
someone else's channel handle. The warning is left standing rather than suppressed.

**18. GATE T is mandated "ALWAYS RUN" and does not exist in this edition.**
`ai-explainer/SKILL.md` is emphatic: GATE T (type-lock) runs like factcheck,
`scripts/type_check.py` asserts min-size / overflow / contrast / kerning / golden
strings and writes `TYPECHECK.md`, and *"no `./art run` and no `./art final` may report
success while `TYPECHECK.md` has any FAIL — wired as a hard block in both `run.sh` and
the `art final` pre-flight."* None of that is here. The script does not exist, `run.sh`
never mentions it, and the gates it does implement are A, B, F, L, SHAPE, V, W. The
same is true of GATE SHARPNESS (the Laplacian audit the PIXEL-ART LAW cites).

*What I did:* did not claim a gate I never ran. `BUILD-LOG.md` records both as absent
rather than as passed, and the §8.1 min-size concern GATE T would have caught is logged
there as an open finding — the mono RESULT lines in the three `ClaudeComposerAsk` beats
render at roughly 22 px effective, just under the ~24 px floor, which is the shipped
component's own sizing and not an authored value.

**19. The SRT writer was removed with the publishing stage, but the example reels still ship captions.**
`align.py` produces the word clock and its docstring names `stage_publish.py` as the
consumer that emits "word-grouped SRT cues where words.json exists". That file is gone
from this edition (all publishing was stripped), yet three example reels ship a `.srt`,
so captions are clearly still expected of a finished reel. A grep for `srt` across
`runtime/scripts/` and `runtime/qc/` hits only that one docstring line.

*What I did:* ran `align.py` (13/13 beats aligned with real word-level timings,
**0 fallback**, 533 words at 24 fps) and wrote `make_captions.py`, which ships with the
submission so the captions are reproducible rather than hand-made.

*And deliberately did NOT copy the exemplar's caption style.* The shipped examples emit
**one cue per beat and truncate the narration to three lines**, so text is silently
dropped mid-sentence — `claude-liam-algorithmic-art.srt` cue 1 ends "Not the code. Not"
and cue 2 starts a different thought entirely. That is a defect, not a house
convention. `make_captions.py` asserts the opposite invariant: every word of every beat
lands in exactly one cue, in order, with no overlaps, two lines maximum, 42 characters
maximum. Result: **61 cues, 533/533 words, no drops.**

*One real bug this surfaced in my own first draft:* I quantized each beat to the frame
grid with `round()`, and the caption clock finished at 195.458 s against a 195.625 s
master — four frames early, drifting the captions progressively against the picture.
`compile.py:387` stamps the authoritative value: `render_duration_s =
math.ceil(measured * fps - 1e-8) / fps`. Those sum to exactly 195.625 s. The script now
reads `render_duration_s` and **asserts** its own clock equals the render clock, so the
drift cannot come back silently.

**20. The runtime floor rests on an unwritten instruction.**
The 4:00 floor comes from a live-class comment, not from the syllabus, the assignment
brief, or Canvas — all of which still say 2–4 minutes. Nothing I can read supports the
change, so `beat_sheet.json` records it explicitly as
`metadata.runtime_floor_reason` and points at this file, and the date is left as a
placeholder for the author rather than invented. If a grader checks the written brief,
this reel is over its stated cap, and the only record of why is the entry above.

**21. The brief's per-act ranges cannot reach the brief's own floor.**
Taking the maximum of every range — Hook 15 + Mechanism 90 + Contrast 30 + Loss 20 +
Boundary 30 + Takeaway 10 — gives **195s = 3:15**, which is *less than* the 4:00 floor the
same brief sets, and the brief also says not to add a seventh act to make up the
difference. The two constraints cannot both hold literally.
*Resolution:* treated the ranges as proportions rather than caps and scaled the act that
the brief itself asks to slow down — "Mechanism, slowly" is now 150.27s of a 253.86s film
(59%). Act order, act count and emphasis are unchanged; no seventh act was added. Flagged
here rather than resolved silently, because which constraint yields is the author's call.

**22. `generate_audio_kokoro.py` regenerates EVERY beat on every run. (Corrects #10.)**
There is no skip-if-exists check anywhere in it: the `todo` list is built from every beat
that has narration text, and the loop unconditionally calls `k.create(...)`,
`write_mp3(out)` and overwrites `actual_duration_s`. I had assumed the opposite for most
of this build. It matters because it means **anything you do to an mp3 outside the script
is destroyed by the next invocation** — which is exactly what happened to the hook's
guess pause (#24).

**23. `mp3/timings.json` is a duration cache that outranks the actual audio.**
After padding the hook to 14.38s (ffprobe) / 14.45s (mutagen), I ran the audio script
once more to see whether it would pick the new length up. It printed `beat-B00.mp3
10.88s` — the **cached** value from `mp3/timings.json` — and wrote that stale 10.88 back
over the corrected duration in `beat_sheet.json`, silently shortening my clock by 3.5s.
The file's real length was never consulted.
*Fix:* the pause is now applied as the LAST audio step; `beat_sheet.json`,
`durationS` and `mp3/timings.json` are all written from one `mutagen` measurement of the
files on disk (the same library the pipeline measures with); and the audio script is not
run again afterwards. The rewrite also dropped a stale `B12` row left in `timings.json`
by the previous 13-beat cut.

**24. `ffmpeg concat` silently produced a same-length file; `apad` worked.**
The hook needs a real pause so the viewer can answer the question before the answer
appears — silence in the *audio*, not a hold faked in the edit, because the measured mp3
is the clock. My first attempt concatenated an `anullsrc` input onto the narration with
the `concat` filter. It exited 0, wrote a file, printed no warning — and the output was
byte-for-byte the same 10.88s. No padding, no error. `-af "apad=pad_dur=3.5"` did it in
one flag. Worth knowing: a zero exit from ffmpeg is not evidence that a filter did
anything.

**25. The "real, dated Claude response" constraint removed three beats.**
The previous cut opened on `ClaudeComposerAsk` with four RESULT lines I had written as a
summary of the build. They read as a Claude reply and were not one — the B03 lines were
genuine `verify_softmax.py` output, but presented inside a chat UI, which implies a
provenance it does not have. Under the constraint that any Claude response shown must be
a real one, actually obtained and dated, the honest options were to show a real dated
transcript or to show none. The six-act structure has no ask/handoff slot anyway, so this
cut shows no Claude interface. Consequence worth stating: COLD OPEN LAW, ASK→RESULT LAW
and HANDOFF LAW no longer apply to this reel, and the ai-explainer bookend arc is
deliberately abandoned in favour of the brief's teaching structure.

**26. A column collision that GATE V cannot see — found only by reading a frame.**
The revision-2 compile passed GATE V with **0 BLOCKER / 0 MAJOR** on the first pass, and
the ladder beats scored 98.8% canvas fill. Reading the step-5 frame showed the `÷ Σ`
column's text — `1.0000 ÷ 1.0792`, about 14 monospace characters at 40px, roughly 340px —
overflowing its 300px column and running straight into the `p` column with no gap:
`1.0792` and `0.9266` touching. On the payoff beat of the whole film.

GATE V's rubric lists "collision" as one of its nine points, but
`runtime/qc/final_frame_check.py` only actually computes background/ink separation, the
ink bounding box against SAFE, and edge bleed. **An interior collision is invisible to
it** — the bbox is unchanged whether two columns touch or not, and the fill score is
unaffected. The automated gate cannot substitute for the law's actual instruction, which
is to *Read the PNGs*.

*Fix:* the `÷ Σ` column widened 300 → 380px and its cell given its own 32px size
(1520px of columns + 156px of gaps = 1676px, inside SAFE's 1728px). B06 and B07 — the two
beats that display that column — re-rendered, re-measured, and the frame re-read to
confirm a clear gap. Then recompiled and the master re-exported, because two beats
changed.

*Worth stating plainly:* this is the second time in this build that a beat with a perfect
duration, valid streams and a passing gate was still wrong on screen. The first was the
truncated Σ row (#13). Both were caught the same way.

**27. My own generator was destructive, and only extracting the zip revealed it.**
`build_beat_sheet.py` authors narration and scene props, so I had it write
`beat_sheet.json` outright. But the sheet also holds things that are *measurements*, not
authored values: `audio_file`, `actual_duration_s`, `render_duration_s` (stamped by
`compile.py`) and `shot.remotion.rendered`. Writing a fresh sheet silently discarded all
of them.

Nothing in the real reel folder broke, because I never re-ran the script after audio. I
found it by unzipping the submission and running the shipped scripts against the shipped
data — which is what a grader would do. In that clean copy the sequence
`verify_softmax.py --emit` → `build_beat_sheet.py` → `make_captions.py` **failed**:
`KeyError: 'actual_duration_s'`, because step 2 had just deleted the clock that step 3
needs. The shipped artifacts were not reproducible in the order their own README implies.

*Fix:* the script now merges. If `beat_sheet.json` already exists it carries the measured
fields and the render provenance forward per `beat_id`, sets `durationS` from the measured
duration rather than the estimate, and preserves the `runtime_*` metadata. Verified
idempotent: a re-run leaves every duration and the ffprobe stamp byte-identical, and
`make_captions.py` still produces 84 cues / 745 of 745 words afterwards.

*Lesson:* "it works in my working directory" is not the same claim as "the deliverable
works." Testing the artifact meant extracting it and running it as a stranger would.

## C. Compile and QC notes

See `_qc/REPORT.md` for the frame-level VISUAL QC LAW audit (9-point rubric, defects
and fixes). The mp4 probe — duration and frame count — is a file check and is recorded
there as such, never as QC.
