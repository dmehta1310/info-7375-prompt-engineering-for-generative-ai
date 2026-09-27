# SOURCES.md — "Shifted, Not Changed"

**Submitted by:** Suketh Produtoor · INFO 7375, Week 1 — drafted by Claude; who did what is §4
**Reel:** `week-01-shifted-not-changed`
**Built:** 2026-09-15 · revised 2026-09-18, 2026-09-20, 2026-09-24

Per [`prerequisites/brutalist-video-sources.md`](../../../prerequisites/brutalist-video-sources.md):
what I used, what I made, what Claude contributed, and every third-party asset with its
licence.

---

## 1. Synthetic narration — disclosed

**Every spoken word in this video is synthetic.** It is
[Kokoro-82M](https://github.com/thewh1teagle/kokoro-onnx) voice `am_onyx`, generated
locally by `runtime/scripts/generate_audio_kokoro.py`. No API key, no cloud call, no voice
cloning, $0.00.

The voice is **not mine and does not claim to be**. It is not Nik Bear Brown's, and this
reel is **not** a @NikBearBrown / `claude-liam` episode:

- The narration deliberately **omits the IN-FOR-BEAR line** ("…this is Liam, in for Bear")
  that every worked example in the toolkit carries.
- The locked `@NikBearBrown` outro card, handle and mascot are **not used**.
  `OUTRO-LOCK.md` scopes them to `claude-liam-*` reels and states that other channels
  "NEVER get this card, handle, or mascot". This reel ships its own `ShiftOutro`.
- The disclosure appears **on screen** on the outro card, not only in this file.
- Nothing here implies endorsement by the instructor, the channel, Northeastern, or
  Anthropic.

This follows the prerequisite's rule verbatim: *"Do not imply a synthetic narrator is me,
Bear, or an official endorsement."*

## 2. The concept and its source text

| Item | Source |
|---|---|
| Concept | Chapter 1, Part 2 — §"The subtraction that changes nothing important" |
| Chapter file | [`chapters/01-randomness-and-first-prompts.md`](../../../chapters/01-randomness-and-first-prompts.md) |
| Reference implementation | [`lessons/01-randomness-and-first-prompts/code/main.py`](../../../lessons/01-randomness-and-first-prompts/code/main.py) — imported, **never modified** (AGENTS.md: "Do not modify reference solutions") |
| Chapter's own probability table | Chapter 1, §"Temperature is a concentration control", T = 1.0 row |
| Quoted on screen (B07) | Chapter 1: "Keep the tested claim narrower than the slogan 'numerically stable.'" — the one verbatim quote in the film, attributed on the card |

The algebraic cancellation shown in B04 is the chapter's own derivation, re-set as a
Remotion scene rather than reproduced as an image.

## 3. Every number on screen — and where it came from

Every figure the film renders is supplied as a **prop** from `beat_sheet.json`. The same values also appear as Zod schema defaults inside each component so a composition can be previewed standalone in Remotion Studio; the beat sheet overrides every one of them at render time. So a wrong figure is fixed in the beat sheet, never in the component. Each prop value was read out of one recorded run:

- **Script:** [`evidence/verify_claims.py`](evidence/verify_claims.py) — standard library
  only, offline, imports the course reference implementation by path.
- **Recorded output:** [`evidence/run-output.txt`](evidence/run-output.txt)
- **Environment of record:** Python 3.12.7 (CPython), macOS 26.6.2 arm64. Re-run on
  2026-09-24 under macOS 27.0: the output is byte-identical except the platform line.

| Shown in | Figure | Claim it supports |
|---|---|---|
| B02 | `OverflowError: math range error` | verbatim exception from `math.exp(1000)` |
| B02 | `709.7827`, `1.797693e+308` | `ln(sys.float_info.max)` and `sys.float_info.max` |
| B03 | `[-2, -1, 0]`; `0.1353352832`, `0.3678794412`, `1.0`; total `1.5032147244` | the intermediates the shift rewrites |
| B03 | `0.0900305732`, `0.2447284711`, `0.6652409558` | matches the chapter's published T = 1.0 table to 10 dp |
| B06 | both 62-character vectors, differing at indices 19 and 60 | shifted path vs direct exponentiation, full precision |
| B06 | `1 ULP` between each differing pair (added 2026-09-25, `REVIEW.md` Round 10) | each differing pair is two adjacent floats — `math.nextafter`, and their IEEE-754 integer patterns differ by exactly 1 |
| B06 | `1.1102230246251565e-16` | measured max absolute difference between the two paths — exactly `2**-53`, half of `sys.float_info.epsilon`; each differing pair is two adjacent floats (`math.nextafter`) |
| B07 | `9.85967654375977e-305`, `5e-324`, `0.0`, `0.0` | `probabilities([0, n])` for n = −700, −745, −746, −800 |
| B08 | `~1e-348` | the true share of the outcome that returns a hard `0.0` |
| B07 | `−1075 · ln 2 = −745.133219102`, `−746` | the cliff in closed form — derived, then confirmed by bisection to 9 dp. Source: [`evidence/boundary-output.txt`](evidence/boundary-output.txt) |

**Reproduce all of it:**

```bash
python3 evidence/verify_claims.py             # prints every claim beside its value
python3 evidence/boundary_analysis.py         # derives the cliff; shows what it costs
python3 -m unittest discover -s evidence -v   # 29 tests; fail if any figure drifts
python3 evidence/mutation_check.py            # proves those tests bite (4/4 caught)
python3 evidence/gate_t_typecheck.py          # GATE T -> TYPECHECK.md (0 FAIL)
python3 evidence/cross_check.py               # every figure, every python3.N on PATH
python3 evidence/doc_consistency.py           # the docs vs the artifact (0 mismatches)
```

**Captions.** `final/week-01-shifted-not-changed.srt` — 113 cues. Timing comes from the
toolkit's `align.py` word clock (faster-whisper word-level timing, sequence-aligned to the
known narration; 11 beats aligned, 0 fallback), converted to an SRT by
`evidence/make_srt.py`. The public toolkit ships the aligner but not the SRT writer, which
lived in the removed publishing module — so that script is mine. Captions are a sidecar,
never burned in.

**What in this film is reconstructed, and how it is labelled.** The brief requires:
*"Label constructed illustrations as constructed … If you show a Claude response, it must
be a real one you actually got, with the date."*

- **B00, B05, B09 show a reconstructed Claude interface.** These are the toolkit's composer
  scene, not screenshots and not transcripts. **No prompt shown in them was ever sent to a
  model** — B00's and B05's were written as on-screen content for the beat sheet
  (`PROMPTS.md`, §5.19). Each carries an on-screen pill from its first frames:
  **RECONSTRUCTED INTERFACE · NOT A CLAUDE TRANSCRIPT** (B00, B05) and
  **SUGGESTED PROMPT · NOT YET RUN — YOURS TO TRY** (B09). The model chip reads a generic
  "Claude", not a specific model version.
- **No Claude response appears anywhere in the film.** B00 no longer shows answer lines
  (see §5.16), and B06's output is the recorded run of `verify_claims.py`, labelled
  on screen as a recorded run of that script.
- **The exponent axis in B02** is drawn to scale from two real figures (709.78 against a
  score of 1000). It is a diagram of measured values, not an invented distribution.
- **Chapter 1's hypothetical answer-key counterexample is not used.**

## 4. What Claude contributed — portion by portion

The [AI policy](../../../prerequisites/ai-policy.md) requires stating *"what Claude
contributed and what you personally attempted, checked, revised, and decided."* Prose is
too vague for that, so this is per artifact.

**Model and sessions (from the session log).** Claude Opus 5 (`claude-opus-5`) via Claude
Code, NEU access, in sessions on 2026-09-15, 2026-09-18, 2026-09-20 and 2026-09-24; Claude
Opus 5.5 (`claude-opus-5-5`) from 15:13 UTC on 2026-09-24. No direct API credits.

**How I used it.** My prompts were goal-level — do this assignment to the brief and the
course material; refine it toward full marks (with the instructor's AI-policy video); post
everything but the video to GitHub under `fall-2026/suketh-p/`; take a deeper look before
submitting. The decisions that were mine are listed under the table. Everything in the
table's third column is **Claude's own working method**, paraphrased — none of it is a
prompt I typed.

**Read the fourth column carefully.** It records checks **Claude ran in the session**, with
their recorded outputs. It is *not* a claim that I repeated them. What I personally re-ran
is the `[MINE]` checklist under the table, and only I fill it in.

| Artifact | AI-assisted? | How it was produced | Checked in the session — by Claude |
|---|---|---|---|
| Concept choice | Shortlist AI, decision mine | Claude shortlisted three candidates from the brief's own list with an argument for each, and recommended against 665.24-vs-630 as the one a cohort would converge on; I picked its recommendation | Read Chapter 1 end to end; confirmed max-subtraction is the smallest of the three |
| `evidence/verify_claims.py` | Written by Claude | Imports the reference unmodified; prints each claim beside the value it actually returns; rounds nothing | Ran it; every probability cross-checked against Chapter 1's published T=1.0 table |
| The boundary finding (`[0,-800]` → `0.0`) | **Found by Claude** | After establishing that the denominator can never underflow, Claude asked the mirror question about the numerator itself, and swept the small end | Re-ran the sweep; confirmed −745 returns `5e-324` and −746 returns `0.0` |
| The derivation (`−1075·ln 2`) | Derived by Claude | Claude asked whether −746 is arbitrary or predictable from the float64 format, and derived it | Confirmed by bisection to 9 dp; checked `2**-1074` and `2**-1075` independently |
| `evidence/boundary_analysis.py` | Written by Claude | Derives the cliff, measures what the boundary costs, and demonstrates the log-space remedy | Ran it; verified the remedy reproduces the reference to 1e-12 on `[1,2,3]` |
| `evidence/test_verify_claims.py` (29 tests) | Written by Claude | One job per check; each test names the beat it defends; no aggregate 'it works' test | Ran them, then ran the mutation check below to confirm they bite |
| `evidence/gate_t_typecheck.py` | Written by Claude | The SKILL.md calls GATE T mandatory and the script is missing, so Claude implemented the parts that can be checked honestly and stated what cannot be | Ran it; it failed on first run and found the disclosure contrast defect. The WCAG maths was re-computed independently of the script on 2026-09-24 from the palette hexes: 1.98, 2.74 and 4.37 all reproduce |
| `evidence/mutation_check.py` | Written by Claude | Implements Chapter 1's Assessment 10 against the suite | Ran it; **it corrected a claim the paperwork had made** — see §5.5 |
| `evidence/doc_consistency.py` | Written by Claude | Five numbers had drifted between the docs and the artifact, each found by accident; this is the check that should have existed from the start | Ran it; it immediately found a sixth stale figure in this very submission (recorded in §5.14). Checked that it exempts the dated logs and the corrections ledger rather than policing their history |
| `evidence/cross_check.py` | Written by Claude | FACTCHECK conceded the figures might not reproduce on another interpreter; that is testable, so this tests it and reports the scope | Ran it; confirmed 3.14.6 (the chapter's own) was among those tested, and checked the scope wording does not overreach to other architectures |
| `evidence/make_srt.py` + captions | Written by Claude | Closes the gap left by the toolkit's removed publishing module | Cue count, total span and first/last cue checked against the narration (the script prints all three) |
| `beat_sheet.json` | Authored by Claude | SHOW blocks first, narration second, per SHOW-DON'T-TELL LAW | Read every narration line against `evidence/run-output.txt` |
| `components/ShiftedNotChanged.tsx` (7 scenes) | Written by Claude | Parameterized scenes that take every figure as a prop; `ShiftComposer` (2026-09-24) wraps the toolkit composer with a disclosure pill | Read the props contract; confirmed the beat sheet supplies and overrides every figure-bearing default — and corrected an over-broad claim in the paperwork, §5.8 |
| Visual QC (5 rounds on the first build; re-run on every re-render since) | Run by Claude | Reads the sampled frames, not just the gate report | Reviewed the contact sheets; two defects were found this way that no gate reported |
| This file, `FACTCHECK.md`, `SHOTLIST.md`, `CHECKS-REPORT.md`, `BUILD-PROMPT.md`, `PROMPTS.md`, `README.md`, `REFINEMENTS.md`, and the dated entries of `FRICTIONAL.md` and `REVIEW.md` | Drafted by Claude | Paperwork keyed to the specific laws in the SKILL.md and the brief | Checked against the artifact — imperfectly: §5.16–§5.20 are errors in these files that survived earlier checks |
| `[MINE]` sections of `FRICTIONAL.md`, `REVIEW.md` and this file | The dated record of my own actions was compiled by Claude from my messages. The reflection is **my own four answers of 2026-09-25**, placed with the wording unchanged — Claude converted only the math notation | — | My review request (answer 1) was carried out by Claude as `REVIEW.md` Round 10 |

**What I decided — these are mine:** the concept (max-subtraction, the option Claude
recommended from its shortlist of three); the video going to Canvas only, with everything
else on GitHub under `fall-2026/suketh-p/`; the fork-and-pull-request route when there was
no push access; asking for the audit that found §5.16–§5.20 before submitting; once push
access was granted, having the stale copies deleted and the corrected version posted
straight to `main`; and the decision to submit.

**`[MINE]` — what I personally re-ran or read.** I watched the cut (my answer of 2026-09-25,
in `FRICTIONAL.md`). No script re-runs are claimed: every check in the table above was run
by Claude in the session.

## 5. Corrections applied (DOUBLE-CHECK LAW)

The SKILL.md requires the source be fact-checked and rewritten rather than parroted, with
corrections logged here.

1. **"The two paths give the same numbers" → corrected before it was narrated.** The
   cancellation is exact in algebra, so I expected bit-identical floats. Measured, they
   differ by `1.1102230246251565e-16`. B06 now states "identical in algebra,
   indistinguishable in floating point" and shows the two digits that differ. Had this not
   been measured, the film would have asserted something false.
2. **"Numerically stable" → "overflow-safe".** The common gloss on max-subtraction
   overstates it. The film narrows the claim on screen and demonstrates the counterexample
   (B07, B08). This follows the chapter's own instruction to keep the tested claim
   narrower than the slogan.
3. **No model version numbers, no drifting counts.** Per DOUBLE-CHECK LAW the script avoids
   anything that dates the video. The only version stated is the Python interpreter, which
   is stated *because* the chapter makes a point of distinguishing a concrete execution
   environment from a universal repeatability claim.
4. **Scope kept narrow.** Chapter 1's temperature table, the stochastic-parrot argument,
   and the 665.24-vs-630 sampling comparison were all cut from the film. The sampling
   comparison survives only as one context line in the verification script. One concept,
   per the brief.

5. **"The sum-to-one tests survive removing the max-subtraction" → measured, and it was
   wrong.** I wrote that claim into `mutation_check.py` from reasoning, then ran it. The
   8 survivors are almost entirely the tests that never call `probabilities()` at all —
   the closed-form derivation tests and the raw `math.exp` overflow test. The script now
   **prints the survivor list from the run** instead of asserting it, so the claim cannot
   drift from the evidence again. The honest finding is sharper than the one I guessed:
   my derivation tests verify the mathematics and are blind to the implementation, which
   is a real coverage boundary in my own suite.

6. **The cliff went from discovered to derived.** The first cut stated `−746` as a swept
   result. It is `−1075 · ln 2 = −745.133219102`, confirmed by bisection to 9 decimal
   places, and `−746` is simply the first integer past it. B07 now shows the closed form.
   Predicting a number is stronger evidence than finding it.

7. **I published word counts I had not counted.** `CHECKS-REPORT.md` claimed the body
   beats ran "65 / 63 / 66 / 30 / 66 / 62 words". Measured from `beat_sheet.json` they are
   **69 / 67 / 72 / 35 / 71 / 67** — and two beats are 1–2 words over the soft 70-word
   target rather than comfortably inside it. The row is now marked ⚠ with the real
   numbers and computed from the sheet instead of asserted. Small, but it is the same
   failure mode as §5.5 and exactly what this film is about: a confident number that no
   one had checked.

8. **"No component hardcodes a number" → too strong, corrected.** I had written that in
   three files. Checking the source, the figures *do* appear inside the components as Zod
   schema defaults — that is how each composition stays previewable in Remotion Studio
   without a beat sheet. The accurate claim is narrower: the beat sheet supplies every
   figure as a prop and **overrides** all of those defaults at render time, which is what
   makes a wrong number a beat-sheet fix. Verified: B02 `logits`, B03 `rows`, B06 `rows`
   and B07 `steps` are all supplied explicitly. The wide version of the claim was the kind
   of sentence this film exists to object to.

9. **The synthetic-narration disclosure was nearly unreadable.** `GHOST` (`#B0AD9A`) on
   the cream stage is **1.98:1** — WCAG AA-large wants 3:1. That colour was carrying the
   disclosure on the outro card, which is the one line in this film with an ethical reason
   to be legible. I had chosen it by eye for "quiet" and never measured it, and it
   survived five rounds of visual QC because looking at it read as *appropriately subtle*
   rather than *failing contrast*. Moved to `SOFT` (4.37:1), along with the two other
   `GHOST` text uses. Found by `gate_t_typecheck.py`, which I only wrote because I was
   tired of recording the missing gate as an excuse.

10. **Terracotta was the only signal in B03.** `ACC` on cream is 2.74:1 and cannot be
    changed — `CLAUDE-BRAND.md` forbids retinting a fidelity palette. The mitigation is
    that the accent must never be the *sole* carrier of meaning, and B03's focal cells
    were exactly that: same size, same weight, distinguished only by hue. They now carry
    `fontWeight: 700`, and §8.3b of the gate checks the mitigation on all four accent
    beats rather than trusting it.

11. **The film broke `[1000, 1000]` and never showed it working.** B02 raised
    `OverflowError` to motivate the subtraction, then B03 switched to `[1, 2, 3]` and the
    motivating failure was never resolved on screen — the viewer had to take the fix on
    trust. This was the largest teaching gap in the film and I only saw it by reading the
    eleven narration blocks as one continuous script instead of beat by beat. B02 now
    holds the break and its resolution **side by side**: the real error on the left, and
    the same input returning `[0.5, 0.5]` on the right. That pair is Chapter 1's own
    canonical test — *"The lesson tests this choice with equal large scores, `[1000,
    1000]`, and expects `[0.5, 0.5]`."*

12. **"two digits out of sixty" was wrong.** The two vectors are 62-character strings
    containing **53** digit characters. I had said "sixty" from the string length, in a
    film whose subject is the difference between a figure and a rounded impression of
    one. Corrected to "two digits out of fifty-three."

13. **Two smaller overclaims in the narration, both fixed before re-recording.**
    B05 said *"I did not want to take my own proof on faith"* — the cancellation is
    Chapter 1's derivation, not mine; now "the algebra". B07 said the cliff sits at
    "minus one thousand seventy-five times **log two**", which is ambiguous spoken aloud
    (log base 10 vs natural log); now "the **natural** log of two". B03 stated
    "sixty-seven percent" as a value while the screen showed `0.6652409558`; now
    "**roughly** nine, twenty-four, and sixty-seven percent".

14. **A sixth number had drifted, and this time a script found it.** `README.md` still
    said the master was `195.44 s`; it is `195.16 s`. That one survived nine rounds and
    three separate find-and-replace sweeps. It was found by
    `evidence/doc_consistency.py`, written specifically because five earlier drifts
    (§5.5, §5.7, §5.8, §5.12, and the "Three interpreters" slip in `cross_check.py`) were
    each caught by luck rather than by method. The script derives runtime, cue count,
    GATE T tally and test count **live** and asserts the current-state documents agree.
    `REVIEW.md` and `FRICTIONAL.md` are exempt as dated logs — they are supposed to quote
    the numbers that were true on the day — so both now carry a verified current-state
    header instead, and the script checks that header rather than rewriting their history.

15. **My staging script falsified two quotations — the most serious error here.** A
    path-rewriting rule changed every `fall-2025/…` to `fall-2026/…`, including two places
    in `FRICTIONAL.md` that **quote** the Canvas brief. The GitHub copy would have claimed
    Canvas said something it never said. The rule is gone, navigation text is corrected at
    the source instead, and the staging step now asserts that staged documents differ
    from their sources only by link depth and the video note. The guard was verified by
    reintroducing the original rule and confirming it catches all four changed lines.

16. **The film showed a fabricated Claude response, and this file said it did not.** B00
    opened on a Claude composer with **three answer lines** beneath the prompt —
    "changes — every intermediate weight / cannot change — the normalized distribution /
    still broken — the small end returns a hard 0.0" — under a model chip reading
    **"Fable 5"**. I wrote those lines as a summary of the film and the composer styled them
    as output. **No such prompt was ever sent to any model.** To a viewer that is a Claude
    transcript, and the brief says of exactly this: *"A video that fabricates a Claude
    transcript to make a cleaner story has failed the assignment on its own terms."*
    Meanwhile this file and `FACTCHECK.md` both asserted *"no Claude transcript is shown"*.
    That is the kind of misstatement about what was verified that the brief calls an
    academic-integrity matter.

    **Why it survived nine rounds.** I was checking against the toolkit's COLD OPEN LAW,
    which *requires* B00 to "land answered" with output lines. The assignment brief
    forbids a fabricated answer. The two conflict, and the brief is what is graded. I
    never read the composer frames against the brief's sentence until asked to take a
    deeper look at the assignment itself.

    **Fix.** B00's answer lines removed; the indicator now reads *"answered by this video —
    not by a transcript"*. All three composer beats (B00, B05, B09) render through a
    reel-local `ShiftComposer` wrapper that overlays a disclosure pill from the first
    frames; the shared toolkit component is untouched. The model chip no longer names a
    model version. B05's narration no longer says "I asked for a check" — the evidence
    script runs both paths, and that is what it now says.

17. **"One machine epsilon" was wrong — on screen and aloud — and so was "one bit".** B06
    glossed `1.1102230246251565e-16` as *"one machine epsilon — the smallest gap float64
    can express near 1"*, and the narration said *"one machine epsilon"*. Python's
    `sys.float_info.epsilon` is `2.220446049250313e-16` = 2⁻⁵², **twice** the measured gap;
    the gap is exactly 2⁻⁵³ (some texts call that the unit roundoff, but a viewer checking
    in Python gets the other number). What is exactly true: each differing pair is two
    **adjacent** floats — `math.nextafter` steps from one to the other — and the largest
    gap is one ulp of `0.665…`. The narration's close, *"wrong by exactly one bit"*, was
    also false: the third pair differs in one bit, but the first differs in two
    (`…1010` vs `…1001`). And the same gloss still ended *"Two digits out of sixty"*:
    §5.12 corrected the narration and the docs, **not the on-screen text**, because no check
    read the beat sheet's on-screen strings.
    **Fix.** Gloss: *"exactly 2\*\*-53 — adjacent floats, one step apart. Two digits out of
    fifty-three."* Narration: *"Not zero — adjacent floats, one step apart … Had I called them
    equal, I would have been wrong in the last place of two numbers."* B06 re-recorded
    (20.50 → 20.63 s) and re-rendered. A new test,
    `test_screen_and_narration_say_what_the_record_says`, reads the on-screen gloss and the
    narration from `beat_sheet.json` and checks them against the recorded run; run against
    the old beat sheet it **fails**, on "sixty". The "one machine epsilon" test was renamed
    and now asserts adjacency and the ulp directly.

18. **B05 typed, and `SHOTLIST.md` said it did not.** The SPARK-LINE LAW: *"typing belongs
    to B00 and the handoff beat only — inner beats show the command already typed."* B05 is
    an inner beat, but the toolkit's `ClaudeComposerAsk` always types from frame 18, so the
    command typed itself in over 1.5 s. `SHOTLIST.md` said *"B05 … shows the command already
    typed"* and `CHECKS-REPORT.md` said typing appears in exactly three beats; both were
    false. **Fix.** `ShiftComposer` gained `preTyped`, which starts the unmodified
    component's own clock past its typing window (`<Sequence from={-64}>`); B05 now opens
    fully typed. Verified on the frame at 0.1 s.

19. **The paperwork spoke for me.** The AI policy: *"State what Claude contributed and what
    you personally attempted, checked, revised, and decided … do not ask AI to invent your
    struggle or understanding."* The deeper look found the documents doing exactly that:
    - `PROMPTS.md` said the B05 prompt was *"the prompt that produced
      `evidence/verify_claims.py` claim 2"*. The session log shows `run-output.txt` was
      recorded at 09:51 EDT on 2026-09-15, and the B05 text was first written into the beat
      sheet at 09:58 — as on-screen content. It was never sent to anyone. Fabricated
      provenance.
    - This file's §4 had a column headed **"What I checked myself"** listing checks Claude
      ran; described its paraphrases of its own method in quotation marks, as if they were
      my prompts; said *"I asked the mirror question"* that found the boundary (Claude asked
      it); and credited me with setting constraints that came from the course documents.
    - Every evidence script and the `.tsx` said **"Author: Suketh Produtoor"**; §6 below
      labelled Claude-written code **"Mine"**, and `SHOTLIST.md` / `PROMPTS.md` marked
      scenes *(mine)*.
    - `FRICTIONAL.md`'s header said all work happened *"in a single Claude Code session on
      2026-09-15"* with Claude Opus 5; the work spans four dates and two models. It held
      six **"What changed in my understanding"** paragraphs Claude wrote, and sentences
      such as *"[Claude] pushed back when I wanted to state the two paths were equal"* and
      *"declined the `.tsx.txt` workaround when I raised it"* — events that did not happen.
      Its `[MINE]` section even contained a self-assessment Claude had written for me.
    - `README.md` said `REVIEW.md` holds *"the change I requested"* — still a `[MINE]` item.
    **Fix.** Every one is re-attributed: §4 now separates Claude's checks from a `[MINE]`
    checklist; the code headers say who wrote the code; `FRICTIONAL.md` is labelled as
    Claude's organised record of the sessions, with "What this showed" replacing the
    understanding claims and those sentences rewritten to say what actually happened; the
    `[MINE]` sections are prompts only. The uncorrected text is in the first GitHub commit,
    `da2695f`.

20. **Smaller misstatements found in the same pass.** `BUILD-PROMPT.md` still carried the
    §5.8 overreach (*"no Remotion component hardcodes a number"*). `CHECKS-REPORT.md` said
    visual QC *"took six rounds"*; `REVIEW.md` records five. `REVIEW.md` R8-4 listed body
    word counts as *"70 / 70 / 68"* — B03 and B04 transposed — in a sentence saying they
    were verified by re-running the gate; the gate had printed 70 / 68 / 70. `FACTCHECK.md`
    ended *"Signed on the evidence above"*, which reads as a sign-off nobody gave, and dated
    `S5`/`S6` to 2026-09-18 when both files were last written on 2026-09-24. The
    `README.md` credit named only Opus 5. `SHOTLIST.md`'s lane histogram still counted B00,
    B05 and B09 as unmodified toolkit scenes. All corrected; the numbers now come from the
    files and the session log, not from memory.

## 6. Third-party assets and licences

| Asset | Source | Licence / terms |
|---|---|---|
| Kokoro-82M voice model (`am_onyx`) | `kokoro-onnx` releases, model-files-v1.0 | Apache-2.0 (kokoro-onnx); model weights per upstream Kokoro-82M release |
| `brutalist.art` toolkit | [github.com/nikbearbrown/brutalist.art](https://github.com/nikbearbrown/brutalist.art) @ `ba2d0e0` | Per repository LICENSE. Used as an external checkout, not vendored into this repo (AGENTS.md). |
| `BrutalistHesitantWriter` (B01) | Toolkit component. Its own header credits an auto-converted `brik/base44` canvas component, author unknown — see the toolkit's `SOURCES.md`. | Used as shipped, props only; motion math untouched. |
| `ClaudeComposerAsk` (inside `ShiftComposer`: B00, B05, B09), `ClaudeVerdictArtifact` (B08) | Toolkit components | Used as shipped — the composer is wrapped, never modified. |
| EB Garamond | Google Fonts, installed by `./setup --install` | SIL Open Font License 1.1 |
| `ShiftOverflow`, `ShiftPipeline`, `ShiftCancellation`, `ShiftReceipt`, `ShiftBoundary`, `ShiftComposer`, `ShiftOutro` | **Written for this reel, by Claude** (§4) — not third-party | Contributed to the toolkit checkout under its licence |
| All eight `evidence/*.py` scripts | **Written for this reel, by Claude** (§4) — not third-party | Standard library only |

**No** paid service, no stock footage, no AI-generated imagery, no screen recordings, no
lifted figures, no Higgsfield, no ElevenLabs. Total spend: **$0.00**.

## 7. Not included, deliberately

- **No YouTube upload.** The brief states no upload is required or expected, and the
  toolkit never publishes. The file is submitted, not posted.
- **No private conversation transcripts**, no credentials, no `.env`, no caches — per the
  GitHub-posting rubric's safe-sharing row.
- **No Manim.** Blocked in this environment and unused; all mathematics renders as
  Remotion. Recorded honestly per the prerequisite rather than hidden.
