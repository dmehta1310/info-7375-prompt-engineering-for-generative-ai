# REVIEW.md — week-01-shifted-not-changed

> **Current state (2026-09-24).** Runtime **195.72 s (3:16)** · Gate V **0 BLOCKER / 0
> MAJOR** · GATE T **0 FAIL · 1 WARN · 29 PASS** · **29** tests · 4/4 mutations caught ·
> **113** caption cues.
>
> Everything below is a **dated log of rounds**. Earlier entries quote the numbers that
> were true *at that time* — 195.46 s, 3:16, 111 cues, 22 tests, 0/3/27 — and are left
> standing on purpose, because a review log that silently rewrites its own history is
> not a review log. Where a round's figure differs from the block above, the block above
> is current.

Timestamped review of the rendered cut: what was wrong, what was requested, what the
re-render fixed. Per [`youtube/README.md`](../README.md), this file holds the real human
review decision — so it distinguishes clearly between what was found by inspecting frames
and what still needs a person to watch the film with sound.

**Who reviewed what.** Rounds 1–9 are **Claude's** review — of sampled frames, gate
reports and the scripts — run in the build sessions; "I" in a round is Claude, and a
"fix requested" is Claude's request of the build. **No human review decision is recorded
yet.** Mine is the `[MINE]` section at the end, written after I watch the cut with sound.

**A compile is not a review.** The first cut compiled successfully at 186.0 s with 11/11
slots filled and zero BLOCKER defects. It was still wrong in two substantive ways that no
file probe could have caught.

---

## Round 1 — review cut, 2026-09-15 10:17

Compiled: `week-01-shifted-not-changed-slate.mp4`, 186.0 s, 11/11 filled, 0 slates.
Gate V: 22 frames sampled, **BLOCKER 0 · MAJOR 4**.

### R1-1 · B01 — the correction never happened (substantive, caught by eye)

**Severity: MAJOR.** Not reported by any gate.

**Problem.** The beat-2 overview is supposed to type the misconception and then visibly
correct it — that correction *is* the beat's pedagogy under EXECUTIVE-SUMMARY LAW. On the
contact sheet, B01 types `Subtracting the max makes softmax numerically stable.` and the
phrase **just stays there**. The video's whole thesis is that "numerically stable" is the
wrong word, and the frame was leaving the wrong word uncorrected on screen.

**Cause.** `BrutalistHesitantWriter` matches `triggerWords` **per whitespace token**:
it splits the text on whitespace and compares each token's core against the trigger list.
My trigger was the two-word phrase `numerically stable.`, which can never equal a single
token. It failed silently — no warning, no error, a clean render of a broken beat.

Reproduced outside the renderer by mirroring the component's own tokenizer:

```
triggers parsed as: ['numerically stable.']
tokens: ['Subtracting','the','max','makes','softmax','numerically','stable.', ...]
MATCHES: NONE — the correction never fires
```

**This is a third doctrine/implementation gap** (the other two are in `FRICTIONAL.md`).
The SKILL.md explicitly instructs: *"when the misconception lives in a phrase, put the
whole phrase in `triggerWords`"* — and its own worked example
(`list of topics` → `sequence of distinctions`) would fail exactly the same way.

**Fix requested:** carry the misconception on a single token so the correction actually
fires, and keep the corrected sentence standing alone as the reel's claim.
`stable` → `overflow-safe`, giving *"Subtracting the max makes softmax overflow-safe."*
B01's narration was rewritten to read that corrected line aloud.

### R1-2 · B01, B10 — underfill (FILL-THE-CANVAS LAW)

**Severity: MAJOR ×4** (B01 at 50% and 85%, B10 at 50% and 85%).
Reported by Gate V: content filled 10–15% of the safe area against a 55% floor.

**Cause, B10 — the interesting one.** Not a layout mistake. `remotion_scenes.py` renders
the **registered** composition length and then conforms to the audio: it freeze-holds a
clip that is too short, but **truncates** one that is too long. `ShiftOutro` was
registered at 210 frames (7 s) against a 2.01 s narration, so only the first 29% of the
animation ever played. The author line, the course line and the synthetic-narration
disclosure all animate in after that point — they were never in the file. The 11% reading
was correct; the card was genuinely almost empty.

**Cause, B01.** Genuine undersizing — 74px type in a frame that can carry far more — made
worse by sampling a typing animation at its midpoint, when only half the text exists.

**Fixes requested:**

- Pin every registered `durationInFrames` in this reel's folder to the beat's measured
  mp3 length at 30fps, and add a comment in `Root.tsx` saying why, so the next person does
  not reintroduce it.
- Re-time `ShiftOutro` so everything settles by p = 0.72, and lengthen its narration from
  2.0 s to a real sign-off (9.13 s) so the card has time to land.
- Scale `ShiftOutro`: title to 216px across two lines (a line break is still an exact
  title restate), rule to 1280px, author to 78px.
- B01: 125px type over five shorter lines, and `charMs` 46 → 26 so the typing **completes
  well before the cut** rather than still being mid-performance at the sample points. That
  also satisfies the law's own instruction to verify the correction is on screen before
  the cut.

### R1-3 · B04 — verdict line collided with the fraction (caught by eye)

**Severity: MAJOR.** Not reported by any gate — the overlap sat inside the safe area, so
no edge-bleed or underfill rule caught it.

**Problem.** On the contact sheet, *"The shift never reaches the ratio."* overlaps the
denominator of the second fraction. A fraction occupies ~182px (two 56px lines plus the
bar and its margins); the "what is left" fraction at y=718 therefore ended at ~878, and
the verdict was pinned at y=852. The spark line, placed at the bottom for this beat, sat
in the same band.

**Fix requested:** re-band the beat with the fraction height budgeted explicitly —
eyebrow 185, fraction 255, eyebrow 545, fraction 615 (ends ~782), verdict 852 — and move
the spark line back to the top.

### R1-4 · B02 — ceiling label touched the input block (caught by eye)

**Severity: MINOR.** The `FLOAT64 CEILING` label at y=444 met the input block, which ended
at ~460 — a ~16px overlap.

**Fix requested:** re-band vertically with explicit gaps — input at 200 (ends ~434),
ceiling label at 470, tick from 542 to the axis at 600, error card at 768.

### R1-5 · Motion histogram warning

`'illustrate' carries 5/11 beats (45%) — over the ~40% cap`. My labels were lazy: I had
tagged every body beat `illustrate` when the scenes do different things. Relabelled
honestly to what each actually performs — B02 `drawon`, B03 `stagger`, B04 `illustrate`,
B06 `stagger`, B07 `drawon`. Histogram now type-on 36% · stagger 27% · drawon 18% ·
illustrate 9% · fade 9%. The label was the defect, not the motion.

### R1-6 · Skin lint — accepted, not fixed

`B10: palette=claude but the outro is 'ShiftOutro' — OUTRO LAW wants ClaudeTitleOutro`.

**Accepted as a deliberate deviation.** `ClaudeTitleOutro` hardcodes `@NikBearBrown`, and
`OUTRO-LOCK.md` scopes that card to `claude-liam-*` reels. Using it would stamp the
instructor's channel on a student submission. Reasoning in `FRICTIONAL.md` and
`CHECKS-REPORT.md`; the lint stays visible rather than being suppressed.

---

## Round 2 — re-render after fixes, 2026-09-15 10:35

Re-rendered from cleared `media/` and `clips/` so nothing stale survived.
Gate V: **BLOCKER 0 · MAJOR 2** (down from 4). Total 193.1 s.

Fixed and confirmed: B01's `stable` → `overflow-safe` correction now fires; B04's
collision is gone; B02's bands are clear; the motion histogram is clean
(type-on 36% · stagger 27% · drawon 18% · illustrate 9% · fade 9%).

Remaining, both at the **50%-of-beat** sample only — the 85% frames passed:

- **B01 underfill 33%** (was 10%). A typing beat is genuinely sparse at its midpoint.
- **B10 underfill 49%** (was 11%). The disclosure was still fading up at p = 0.5, so it
  was not in the measured ink bounding box.

**Fixes requested:** re-time `ShiftOutro` so the rule, meta and disclosure are all fully
present by p = 0.44 rather than 0.66, and model B01's typing timeline against the
component's own pause costs to choose `charMs`. At the shipped `charMs: 26` the overview
did not finish until 11.5 s of a 13.8 s beat; `charMs: 14` with `hesitateWithin: 0` and
`hesitateBetween: 4` completes 4 of 5 lines at 5.4 s (39%) and all five by 7.1 s (51%), so
the corrected overview holds through both sample points and through the cut.

## Round 3 — 2026-09-15 11:28

Gate V: **BLOCKER 0 · MAJOR 1**. B10 now passes.

### R3-1 · The renderer silently skipped the beat I had just edited

**B01 came back at exactly 33% — byte-identical to round 2.** That precision was the tell:
an unchanged number after a real change means the change never rendered.

The round-3 log contains `[remotion] B10: ok: ShiftOutro -> media/B10.mp4` and **no B01
line at all**, yet `media/B01.mp4` existed at compile time with a fresh mtime.
`remotion_scenes.py` gates each beat on
`if not a.force and not slate_resolves(folder, bid): "filled already (skip)"` — so a beat
whose **props changed** is not re-rendered by `./art run`, because the beat still resolves
as filled from the previous build's stamp. Deleting `media/B01.mp4` was not enough.

**This is the failure mode most likely to put a stale frame in a finished film**, and it
is silent: the run reports 11/11 filled and compiles happily around the old clip.

**Fix:** re-render the edited beat explicitly —

```bash
python3 runtime/scripts/remotion_scenes.py <reel> --only B01 --force
```

Recorded in `BUILD-PROMPT.md` so a rebuild does not inherit the trap.

## Round 4 — forced re-render, 2026-09-15 11:30

B01 re-rendered with `--force` and measured directly rather than by re-running the whole
gate. The result showed the correction now fires — but also that **4 lines at 124px only
reaches 51% coverage even when complete**, and that typing finished at 8.0 s of a 13.8 s
beat (58%), i.e. after the 50% sample.

Measured coverage curve of `media/B01.mp4` (bbox as a fraction of SAFE), which is what
made the fix tractable instead of guesswork:

| t | p | coverage |
|---:|---:|---:|
| 3.0 s | 0.22 | 18% |
| 5.0 s | 0.36 | 33% |
| 6.9 s | 0.50 | 46% |
| 8.0 s | 0.58 | 51% ← typing complete |
| 13.4 s | 0.97 | 51% |

Two conclusions from the curve: the block had to get **taller** (coverage is bbox area, and
four lines at 124px spans only 61% of the safe height), and the typing had to finish
**before** the midpoint sample. The component's hard-coded pauses — 400 ms per newline,
600 ms per punctuation mark, ~1.25 s for the reconsideration — dominate the timeline, so
`charMs` alone could not buy enough time; a line break had to go.

**Fixes:** `fontSize` 124 → 136; `charMs` 8; `mistakeRate`, `hesitateWithin` and
`hesitateBetween` all to 0; and B01's narration extended from 43 to 54 words (13.74 s →
16.36 s) so the finished overview is on screen for two thirds of the beat instead of
being raced to the cut.

Zeroing the random typos deserves a note, because it looks like removing character. The
SKILL.md's point is that *"the hesitation is the pedagogy, not decoration"* — the
pedagogical hesitation is the **deliberate correction**, `stable` → `overflow-safe`.
Random typos are the decoration. Removing them makes the one reconsideration the clear
focal moment rather than one stumble among several.

## Round 5 — clean, 2026-09-15 11:47

```
Gate V — frames sampled: 22 · BLOCKER: 0 · MAJOR: 0
Clean — no BLOCKER/MAJOR defects. ✓
```

Verified, each against the round-1 finding it answers:

| Check | Result |
|---|---|
| B01 coverage at 50% / 85% | **61% / 61%**, wspan 92%, hspan 66% — both pass |
| B01 ink x-range | 163–1747, inside title-safe 96–1824 (no edge bleed from the larger type) |
| B01 correction | `stable` deletes, `overflow-safe` types in its place, holds through the cut |
| B10 | title, rule, author, course and disclosure all present in both steady-state frames |
| B04 | 69 px gap between the second fraction (ends 783) and the verdict (852) |
| B02 | input block ends 434, ceiling label starts 470 — 36 px clear |
| Motion histogram | type-on 36% · stagger 27% · drawon 18% · illustrate 9% · fade 9% |
| Master | `final/week-01-shifted-not-changed.mp4` · 1920×1080 · h264+aac · **195.75 s** |
| Audio not silent | mean −27.2 dB, max −2.7 dB (a silent master is a FAILED BUILD) |
| Runtime vs brief | 3:16, inside the 2–4 minute target, no padding beat |

The only remaining warning is the accepted skin lint on B10 (R1-6), left visible.

**Rounds to clean: five.** The first cut compiled on the first try and had four defects,
two of which no gate reported. That ratio is the argument for the frame-reading pass.

---

## Round 6 — iteration pass, 2026-09-18

Not a defect round. I went back to the [AI policy](../../../prerequisites/ai-policy.md) —
*"Iterate: examine the first result, identify weaknesses, revise, test, and improve it"* —
and looked for the **weakest claim in a film that had already passed every gate**.

It was the best beat. B07 stated the cliff at −746, found by sweeping inputs. Sweeping
proves a boundary exists; it does not explain why it is there, and it would not transfer.

| Change | Before | After |
|---|---|---|
| B07 cliff | `-746`, swept | `−1075 · ln 2 = −745.133219102`, derived; −746 is the first integer past it, bisection agrees to 9 dp |
| B07 accent | derivation was terracotta | moved to ink — the cliff is the beat's ONE terracotta moment, per the accent law |
| B07 glyphs | `⌊⌋ → −746` | `first integer past it: −746` — the floor brackets read as cryptic in the frame |
| B07 narration | 62 words (as reported) | 67 words (as measured); duration 20.39 s → 20.10 s |
| Evidence | 1 script, 22 tests | 3 scripts, 28 tests, + a mutation check |
| Captions | 111 cues | 112 cues, B07 realigned |

Gate V after the change: **BLOCKER 0 · MAJOR 0**, 22 frames. Master re-exported at
**195.46 s**.

### R6-1 · Two claims in my own paperwork were false

Both found by running a check rather than re-reading the prose.

1. **Which tests survive removing the max-subtraction.** I had written "the sum-to-one and
   chapter-table tests survive". Measured: the 8 survivors are almost entirely the tests
   that never call `probabilities()` at all — my closed-form derivation tests and the raw
   `math.exp` overflow test. Those verify the mathematics and are structurally blind to an
   implementation defect. `mutation_check.py` now prints survivors from the run so the
   claim cannot drift again.
2. **The body-beat word counts.** `CHECKS-REPORT.md` listed "65 / 63 / 66 / 30 / 66 / 62".
   Measured from the beat sheet: **69 / 67 / 72 / 35 / 71 / 67**, with B04 and B06 sitting
   1–2 words *over* the soft 70-word target. The row is now ⚠ with real numbers.

Neither error changed the film. Both were confident numbers in the submission that nobody
had checked — which is the exact failure the film is about, found twice in my own
supporting documents.

### What I deliberately did NOT add

The log-space remedy (`boundary_analysis.py`) is genuinely useful and is the practical
answer to the boundary the film ends on. It is **not a beat**. The brief says pick the
smallest idea and explain it completely; a "and here's how to fix it" act would be a second
concept and would cost the film its discipline. It lives in the evidence folder, is
referenced from the README, and the handoff prompt already points a viewer at it.

---

## Round 7 — GATE T, 2026-09-20

I had written "GATE T could not be run" three times across the paperwork. True, and an
excuse: the SKILL.md is explicit that no build may report success while `TYPECHECK.md` has
a FAIL, and mine had no `TYPECHECK.md` at all. So I wrote the gate —
`evidence/gate_t_typecheck.py` — implementing the §8 checks that can be done honestly from
the scene source and the beat sheet, and stating in its header the ones that cannot.

**It failed on its first run, on three counts.**

### R7-1 · The synthetic-narration disclosure was at 1.98:1

**Severity: MAJOR (accessibility).** Not caught by Gate V, which measures ink *coverage*,
not ink *contrast*.

`GHOST` (`#B0AD9A`) on the cream stage measures **1.98:1**. WCAG 2.1 AA-large wants 3:1;
AA-normal wants 4.5:1. That colour was carrying the synthetic-narration disclosure on the
outro card — the one line in this film with an ethical reason to be legible — plus the
B02 axis label and the B04 struck factor.

The uncomfortable part: this survived **five rounds of visual QC and my own frame-by-frame
review**. I had looked straight at that outro card repeatedly and read the disclosure as
*appropriately subtle*. Looking could not tell me it was failing; arithmetic on two hex
values could, in milliseconds.

**Fix:** all three `GHOST` text uses → `SOFT` (4.37:1). `GHOST` is now unused as a text
colour, with a comment in the palette block saying why so nobody reaches for it again.

### R7-2 · Terracotta was the only signal in B03

`ACC` on cream is **2.74:1** — also under AA-large. This one cannot be fixed:
`CLAUDE-BRAND.md` states the palette replicates the real product and must not be retinted,
and the reel is explicitly a fidelity brand.

So the gate records it as a **brand-locked WARN** and checks the *mitigation* instead
(§8.3b): wherever the accent marks a value, a non-colour signal must travel with it. That
check immediately found B03's focal cells were distinguished **by hue alone** — same size,
same weight. They now carry `fontWeight: 700`. B04 (strikethrough), B06 (bold) and B07
(bold + larger) already had one; now all four are verified rather than assumed.

### R7-3 · A false positive in my own gate

§8.6 flagged `0.3678794412` and `0.6652409558` as "on screen but not in any recorded run".
Both are correct 10-dp roundings of full-precision recorded values — and the second is
**verbatim Chapter 1's own published table**. My check was doing naïve substring matching.

It now accepts a correct rounding and prints which full-precision value it rounded. A
gate that cries wolf gets ignored, which would have been worse than not having it.

**Result on this date: 0 FAIL · 3 WARN · 27 PASS** → [`TYPECHECK.md`](TYPECHECK.md).
The two word-budget warnings cleared in round 8; the gate now reads **0 FAIL · 1 WARN ·
29 PASS**, the one remaining warning being the un-retintable brand accent.

Four beats re-rendered (B02, B03, B04, B10); Gate V re-run clean.

### R7-4 · A beat render reported FAIL and the build shipped a master anyway

Found while doing exactly that re-render. The log reads:

```
[remotion] B02: ok: ShiftOverflow  -> media/B02.mp4
[remotion] B03: ok: ShiftPipeline  -> media/B03.mp4
[remotion] B04: ok: ShiftCancellation -> media/B04.mp4
[remotion] B10: FAIL: ShiftOutro
[gate-v] frames=22 BLOCKER=0 MAJOR=0
[art] wrote .../final/week-01-shifted-not-changed.mp4
```

B10 failed, and the pipeline **compiled around the stale clip and exported a master**.
Gate V passed because the old B10 is visually fine — it just still had the 1.98:1
disclosure this round exists to fix. So a genuine render failure produced a clean gate
and a "final" file.

The failure itself was transient: re-running `--only B10 --force` on its own succeeded
immediately, so it was most likely a bundler hiccup under four sequential forced renders,
not a defect in the scene. The hazard is not the flake — it is that **a FAIL in the render
stage did not stop the export**, which is the same silent-stale-clip family as R3-1 and
the reason that trap is written into `BUILD-PROMPT.md`.

**Practice added:** after any multi-beat re-render, grep the log for `FAIL:` before
trusting the master. A clean Gate V is not evidence that every beat actually re-rendered.

---

## Round 8 — back to the brief, 2026-09-24

The last three rounds all improved *evidence*. The rubric puts **15 of 25 points on the
explanation** and 5 on Relative Quartile, so I had been optimising the smaller number. This
round audited the teaching instead — by printing all eleven narration blocks and reading
them as **one continuous script** rather than beat by beat.

That reframing found the largest remaining defect immediately.

### R8-1 · The film broke `[1000, 1000]` and never showed it working

**Severity: MAJOR (teaching).** No gate can see this — every frame was individually fine.

B02 exists to answer *why does this subtraction exist?* It raises a real
`OverflowError` on `[1000, 1000]`… and then B03 switches to `[1, 2, 3]` and the
motivating failure is **never resolved on screen**. The viewer watches something break and
has to take on trust that the fix repairs it. The single most satisfying moment available
to this film — *the input that just failed now returns a clean answer* — was missing.

It is also Chapter 1's own canonical test for this exact choice: *"The lesson tests this
choice with equal large scores, `[1000, 1000]`, and expects `[0.5, 0.5]`."*

Reading beat-by-beat hid it because each beat is coherent alone. Only the continuous read
exposed the dangling setup.

**Fix:** B02 now ends on a **side-by-side** pair — the real error on the left (terracotta),
the same input shifted returning `[0.5, 0.5]` on the right (ink). Both are fully present
by the 85% sample, because a comparison that appears sequentially is not a comparison.
Narration gained one clause: *"Now shift first: the same input returns one half, one
half."*

### R8-2 · "two digits out of sixty" — wrong count

The two vectors are 62-character strings containing **53** digit characters. I had said
"sixty", taken from the string length. In a film whose entire subject is the gap between a
figure and a rounded impression of one, that is the wrong place to be loose. Now "two
digits out of fifty-three."

### R8-3 · Three narration precision fixes

| Beat | Was | Now | Why |
|---|---|---|---|
| B05 | "take **my own proof** on faith" | "take **the algebra** on faith" | The cancellation is Chapter 1's derivation. I do not own it. |
| B07 | "minus 1075 times **log two**" | "…times the **natural** log of two" | Spoken aloud, "log two" is ambiguous between base 10 and base e. The value only works for ln. |
| B03 | "sixty-seven percent" | "**roughly** nine, twenty-four, and sixty-seven percent" | Stated as a value while the screen showed `0.6652409558`. |

### R8-4 · I claimed a result I had not measured. Again.

I wrote here that "both word-budget warnings cleared" and listed five counts. Then I ran
GATE T: **B06 cleared (71 → 69), B04 did not — it was still 72, because I never rewrote
it this round.** My five-number list had silently omitted B04 altogether.

This is the third time in this project (see `SOURCES.md` §5.5, §5.7) that I have written a
confident number into the paperwork without re-running the check that produces it. The
film's whole argument is that a fluent claim and a supported one are different things, and
the supporting documents kept demonstrating it against me.

B04 is now trimmed by two words ("Now, why is that allowed" → "Why is that allowed";
"Every single term" → "Every term"), which brings it to 70. Body beats measure
**70 / 70 / 68 / 34 / 69 / 70** for B02–B07 — verified by re-running the gate, not by
counting in my head. *[Corrected 2026-09-24: the gate printed **70 / 68 / 70 / 34 / 69 /
70**. B03 and B04 were transposed when this list was typed, in the sentence saying it was
not typed from memory. `SOURCES.md` §5.20.]*

---

## Round 9 — a deeper look at the brief, 2026-09-24

Requested by the submitter: a deeper look at whether the assignment was done and submitted
right. Claude read the brief's own sentences against every frame and document instead of against the
toolkit's laws. Nine rounds had checked the film against the doctrine; none had checked it
against the brief's one hard rule.

### R9-1 · B00 showed a fabricated Claude answer (BLOCKER — integrity)

The cold open landed "answered": three authored answer lines under a "Fable 5" model chip,
for a prompt that was never sent. The toolkit's COLD OPEN LAW asks for exactly that; the
brief says a fabricated Claude transcript *"has failed the assignment on its own terms."*
**Fix:** answer lines removed; B00, B05 and B09 render through `ShiftComposer`, which
overlays a disclosure pill from the first frames (**RECONSTRUCTED INTERFACE · NOT A CLAUDE
TRANSCRIPT**; B09: **SUGGESTED PROMPT · NOT YET RUN — YOURS TO TRY**) and a generic
"Claude" model chip. Verified on the frames of the final master. `SOURCES.md` §5.16.

### R9-2 · "One machine epsilon", "one bit", and "sixty" still on screen (MAJOR — correctness)

`sys.float_info.epsilon` is 2⁻⁵², twice the measured gap of 2⁻⁵³. "Wrong by exactly one
bit" was false for one of the two differing pairs (two bits). And the scene's gloss still
said "two digits out of sixty" two cuts after R8-2 corrected the narration, because no
check read the beat sheet's on-screen text. **Fix:** new gloss and narration, B06
re-recorded (20.63 s) and re-rendered, and a test that reads the on-screen text against the
recorded run. Run against the old beat sheet, that test fails on "sixty". `SOURCES.md` §5.17.

### R9-3 · B05 typed (MINOR — doctrine, and a false line in `SHOTLIST.md`)

Inner beats must show the command already typed; B05 typed, because the toolkit composer
always does. **Fix:** `preTyped`, which starts the unmodified component's clock past its
typing window. Verified at 0.1 s: the command is complete. `SOURCES.md` §5.18.

### R9-4 · The documents spoke for the submitter (BLOCKER — integrity)

`PROMPTS.md` claimed the B05 prompt produced `verify_claims.py`, but it was written after
the script ran and was never sent. `SOURCES.md` §4 had a column headed "What I checked
myself" listing Claude's checks. Every code file named the submitter as author.
`FRICTIONAL.md` carried six understanding paragraphs, and sentences about things the
submitter never did, all written by Claude. **Fix:** every document re-attributed; `SOURCES.md` §5.19 lists each case.

**Result of this round:** Gate V **BLOCKER 0 · MAJOR 0** (22 frames); master 1920×1080,
h264+aac, **196.0 s** as probed (195.72 s of narration); **113** caption cues; GATE T
**0 FAIL · 1 WARN · 29 PASS**; **29** tests green, and the mutation check still catches 4/4.

---

## Round 10 — the change the submitter asked for after watching, 2026-09-25

The first change requested by a person who watched the cut rather than by a gate. The
submitter's words are quoted in full in the `[MINE]` section below: the floating-point
comparison at 1:46–2:05 left the point *"buried in the last digit of two long numbers"*.
They asked for the frame to be held longer, the two differing digits isolated, and a small
"1 ULP apart" marker between them. Implemented by Claude.

### R10-1 · B06 — isolate the two differing digits, mark them, hold the view

**What changed.** `ShiftReceipt` gained an `isolateLabel` prop (`"1 ULP"` in the beat
sheet). The beat is re-timed to its own word clock, and the audio is untouched, so the
runtime is too:

| Beat fraction | Narration | On screen |
|---|---|---|
| ≈ 0.26 | "…minus sixteen." | both vectors in place |
| 0.25–0.30 | "Not zero" | the four differing digits turn terracotta and bold |
| 0.29–0.34 | "adjacent floats…" | every agreeing digit steps back; a `1 ULP` marker appears between each differing pair |
| to 0.60 | "…merely indistinguishable." | held — about six seconds on the one comparison that matters |
| 0.60–0.66 | "Both match the chapter's…" | the view releases as the headline figure scales up |

**How the markers stay on their digits.** They ride on a transparent copy of the upper
row's text in the same monospace face, so each one is centred on its digit by the font
itself — no measured character widths.

**Two defects found before shipping, both fixed.**

1. *Found by looking.* On the first render, the lower row's label faded out while the left
   marker faded in, and for about a second they overlapped ("…the raw 1 ULP scores"). The
   crossfade is now sequential: the label is gone before the markers arrive, and back only
   after they leave. Checked at 6.2, 6.5, 6.8, 12.5, 12.9 and 13.3 s.
2. *Found by Gate V.* The first version dimmed the agreeing digits to 22 % opacity, and the
   compile failed: **MAJOR `low-contrast` on B06 at 50 %, luminance separation 0.22 < 0.30.**
   Fading text by opacity mostly adds faint anti-aliased pixels. The agreeing digits now
   step back by *colour* instead — ink to the reel's secondary grey (`SOFT`, about 5:1 on
   the white card, still readable) — and the frame measures clean.

**The claim on screen is checked against the record.** "1 ULP" is a factual claim: each
differing pair must be exactly one representable step apart. The screen test in
`evidence/test_verify_claims.py` now reads the label from `beat_sheet.json`, and checks it
against the step count between the two recorded vectors' IEEE-754 bit patterns.
`FACTCHECK.md` row 22.

**Result, measured after the fix:** Gate V **BLOCKER 0 · MAJOR 0** across 22 frames. GATE T
**0 FAIL · 1 WARN · 29 PASS** — with one §8.3b FAIL on the way: a refactor had moved the
`markIn > 0.2` condition into a variable, so the bold was still there but the literal
expression the gate checks was not. The expression was restored rather than the gate
loosened. All 29 tests pass, the mutation check still catches 4 of 4, and the final master
is 196.0 s at 1920×1080 — the same runtime, since the audio did not change.

---

## `[MINE — the part a gate cannot do]`

Frame inspection found four defects that compiled cleanly, which is the argument for doing
it. It still cannot judge whether the film **teaches**. Before submitting I watch the whole
cut with sound and answer, in my own words:

- Does the narration ever get ahead of what is on screen? Kokoro reads long numbers at its
  own pace, and B06/B07 both hinge on hearing a figure while seeing it.
- Is B03 legible at a glance, or do four columns of ten-decimal numbers need longer than
  19.61 s?
- Could a classmate who has not read Chapter 1 state, after watching once, both what the
  subtraction guarantees and what it does not?
- One change I request after watching, and how it improved **understanding** rather than
  appearance — logged here with its timestamp, then re-rendered and re-checked.

**My watch-through, 2026-09-25 (13:56 EDT).** I watched the cut. The change I asked for,
as I wrote it (all four of my answers are in `FRICTIONAL.md`, `[MINE]`):

> Yes. One thing I would change is the floating-point comparison around 1:46–2:05. The video shows both full-precision probability vectors and then the 1.1102230246251565e-16 difference, but the important change is buried in the last digit of two long numbers. I would hold that frame slightly longer and isolate only the two differing digits, with a small “1 ULP apart” marker between them. The narration explains the idea correctly, but making that last-place difference visually obvious would make the distinction between algebraic equality and floating-point equality land faster.

Claude carried it out and re-checked it — Round 10 above. The first three questions in this
list are not answered yet, so the honest status is: **reviewed for defects, watched once by
me with one change made; the teaching questions are still open.**
