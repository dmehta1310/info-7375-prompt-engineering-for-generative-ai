# FRICTIONAL.md — Week 1 Explainer Video

> **Current state (2026-09-24).** Runtime **195.72 s (3:16)** · Gate V **0 BLOCKER / 0
> MAJOR** · GATE T **0 FAIL · 1 WARN · 29 PASS** · **29** tests · 4/4 mutations caught.
>
> The entries below are **dated as they happened** and quote the numbers that were true
> on each day — 0/3/27, "two digits out of sixty", and so on. Their events and figures are
> left standing on purpose: a log that edits its own past is not evidence of anything.
> Where an entry differs from the block above, the block above is current.
>
> **One edit to the past, disclosed.** On 2026-09-24 the entries' *attribution* was
> corrected. They had been written as if I personally did, expected or understood things
> that Claude did in the session (method disclosure below; `SOURCES.md` §5.19). Only
> who-did-what changed — not the events, dates or numbers. The uncorrected text is in this
> folder's first GitHub commit, `da2695f`.

**Student:** Suketh Produtoor
**Assignment:** Week 1 Explainer Video — Explain One Concept from Chapter 1
**Course AI policy:** [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz)

Per [`prerequisites/frictional.md`](../../../prerequisites/frictional.md): this is an honest
log of what was tried, what broke, and what was decided — not a timesheet and not a
performance of difficulty. Entries are dated as they happened.

**Method disclosure — who wrote this file, and what "I" means in it.** The build ran in
Claude Code sessions on 2026-09-15, 2026-09-18, 2026-09-20 and 2026-09-24: Claude Opus 5
(`claude-opus-5`) throughout, and Claude Opus 5.5 (`claude-opus-5-5`) from 15:13 UTC on
2026-09-24, per the session log. Claude drove the terminal at my direction. My direction
was goal-level, plus these decisions, which were mine: the concept (max-subtraction, the
option Claude recommended from its shortlist); the video going to Canvas only, with
everything else on GitHub under `fall-2026/suketh-p/`; the fork-and-pull-request route
while there was no push access; asking, before submitting, for the audit that found the
last entry's errors; and then having the stale copies deleted and the corrected version
posted to git. Claude
read the chapter and the toolkit doctrine, ran the reference code, diagnosed the install
failures, wrote the beat sheet, the Remotion components, the evidence scripts and **this
file**, and rendered the film.

So, read literally, the dated entries are **Claude's organised record of the build
sessions**. The prerequisite allows exactly that — *"AI can organize your notes; you must
supply the actual experience."* Where an entry says "I tried", "I expected" or "I ran", it
describes a step of the build session, **not** something I personally did, believed or
checked. The **What this showed** paragraphs are observations about the work, not claims
about my understanding. What I personally attempted, checked, decided and understood
appears **only** in the `[MINE]` sections. There, the dated record of my own actions was
compiled by Claude from my messages, and the reflection is my own answers, placed with the
wording unchanged; the assistant does not write it. Nothing in this file claims an approval, a test result, or an understanding that did
not occur.

---

## 2026-09-15 — Picking a concept small enough to finish

**Tried / expected:** The brief warns that the usual failure is a three-minute tour of
the whole chapter. I expected the hard part to be production; it was actually scoping.

**What happened:** Claude read Chapter 1 end to end and shortlisted three candidates from
the brief's own list: the expected-count-versus-observed-count pair (665.24 vs 630),
temperature as a ratio, and the max-subtraction. All three are legitimate. The
max-subtraction is the smallest — it is literally one subtraction — and it is the only one
of the three that has a *provable* core (the factor cancels) sitting next to a *runnable*
failure (the raw exponential actually raises).

**What was done:** I chose the max-subtraction — the option Claude recommended from the
shortlist. Claude's reason for passing over the 665.24-vs-630 concept: the brief lists it
first, so it is the most likely thing for a cohort to converge on. The
distribution-versus-sample point still appears, but as one context line in the
verification script rather than as the subject.

**What Claude contributed:** The shortlist, the argument that max-subtraction is the
smallest of the three, and the observation that it uniquely pairs a proof with a
demonstrable crash.

**Evidence:** [`beat_sheet.json`](beat_sheet.json) `metadata.concept`; Chapter 1 §"The
subtraction that changes nothing important".

---

## 2026-09-15 — The toolkit would not install (four separate causes)

**Tried / expected:** `git clone` the toolkit, run `./setup --install`, start building. I
expected one install step.

**What happened:** Four failures in sequence.

1. `./setup` reported **6 of 7 features blocked**. Only slates/previz/compile were ready.
2. `./setup --install` failed the entire Python dependency step. The actual root cause was
   one line deep in the pip output: `pycairo` could not build because
   `Pkg-config for machine host machine not found`. `cairo` itself was already present via
   Homebrew (1.18.4) — only `pkg-config` was missing. Because `pip install -r
   requirements.txt` is a single transaction, that one package took **Kokoro and
   faster-whisper down with it**. The blocked-audio message was a symptom, not the cause.
3. The first install had gone into the **Anaconda base environment**, which
   [`prerequisites/brutalist-video.md`](../../../prerequisites/brutalist-video.md) explicitly
   warns against ("Avoid the system Python environment"). The session had skipped the venv
   step in the documented setup sequence.
4. Rebuilt the venv — and it landed on **Python 3.14**, for which `manim>=0.18,<0.19` has
   no distribution at all (`No matching distribution found`). So the fix for (2) exposed a
   fresh incompatibility.

**What was done:** `brew install pkgconf` for the real cause, then rebuilt the venv on
**Python 3.12.7** and installed the audio pipeline *without* Manim. That last decision is
the one worth defending: the prerequisite says a first video should "use existing
chart/diagram components and avoid equation beats", and that "the doctor may still report
that unused feature as blocked: record it honestly". Manim stays blocked in this
environment and this film never calls it — all the mathematics renders as Remotion scenes
instead. Final readiness: audio ✅, captions ✅, Remotion ✅, slates/compile ✅, fonts ✅,
**Manim ❌ (blocked, unused)**.

**What Claude contributed:** Found the `pkg-config` line in ~200 lines of pip output,
identified that a single-transaction install was masking the cause, caught its own
skipped venv step against the prerequisite, and made the call to drop Manim rather than
fight a version conflict for a feature the film does not use.

**Unresolved:** Why `requirements.txt` pins `manim<0.19` when 0.19+ exists. Not
investigated, because the dependency was removed instead of satisfied. If a later
assignment needs equation beats, this is the first thing to go back to.

**Evidence:** `./setup` readiness table; [`BUILD-PROMPT.md`](BUILD-PROMPT.md)
"Environment" section, which records the exact working recipe.

---

## 2026-09-15 — The finding I did not go looking for

**Tried / expected:** I only wanted to verify that the shift is harmless — that
`probabilities([1,2,3])` matches the chapter's published table. I expected a clean tick and
a short beat.

**What happened:** Two results I did not predict.

- **The two paths are not bit-identical.** I assumed shifted-then-normalize and
  direct-exponentiate-then-normalize would return the same floats. They do not. They
  differ by `1.1102230246251565e-16` — one machine epsilon, in exactly **two digits out of
  fifty-three** (character positions 19 and 60; this line first said "sixty", from the
  62-character string length — corrected 2026-09-24, `SOURCES.md` §5.12). *[Also corrected
  2026-09-24: "one machine epsilon" is wrong — the gap is 2⁻⁵³, half of Python's
  `sys.float_info.epsilon`, and the two answers are adjacent floats. `SOURCES.md` §5.17.]*
  Mathematically the cancellation is exact; in
  float64 it is only indistinguishable. I had been about to narrate "the same numbers".
- **The subtraction only protects one end.** Checking that the denominator can never
  underflow (it cannot — the peak's weight is exactly 1, so the total is always ≥ 1) made
  me ask the mirror question about the *numerator*. `probabilities([0, -800])` returns
  `[1.0, 0.0]` — an **exact zero** for an outcome whose true share is about `1e-348`.
  Walking the second score down found the cliff: `-745` still returns `5e-324` (the last
  denormal), and `-746` is where it becomes a hard `0.0`.

**What was done:** Rebuilt the video around the second finding. It became B07 and the
"NOT ESTABLISHED" line of the verdict — which is exactly the rubric's "name one thing your
explanation does not establish", except demonstrated on the real function instead of
hedged in a sentence. The first finding became B06, and it changed a claim I was about to
make on camera.

This also connects to the chapter's own warning, which the first read had passed over:
*"Keep the tested claim narrower than the slogan 'numerically stable.'"* That sentence
turns out to be the point of the whole section, not a caveat to it.

**What Claude contributed:** all of it — the check, the boundary sweep that located the
`-746` tipping point, and the measurement that replaced the draft narration's "the two
paths are equal" before it was recorded.

**Evidence:** [`evidence/verify_claims.py`](evidence/verify_claims.py) claims 4 and 5;
[`evidence/run-output.txt`](evidence/run-output.txt) — the recorded run every on-screen
number is read from.

---

## 2026-09-15 — Three places the doctrine and the tooling disagree

All found while following `skills/make/ai-explainer/SKILL.md` literally. A fourth — the
one that actually broke a beat — is in the QC entry below.

**1. `lead_silence_s` is required but not implemented.** The SKILL.md's
EXECUTIVE-SUMMARY LAW requires beat 2 to carry an explicit `lead_silence_s: 0.8` so the
hesitant-writer typing gets a head start. `grep -rn "lead_silence" runtime/scripts/*.py`
returns **nothing** — the free toolkit's audio script does not read that field. I left it
in the beat sheet because the doctrine asks for it, and instead guaranteed the ≥9 s window
by writing B01 long enough to earn it on measured audio. Recorded here rather than
silently dropped.

**2. The locked outro card would have been an impersonation.** `OUTRO-LOCK.md` hardcodes
the handle `@NikBearBrown` into `ClaudeTitleOutro` and says the handle is "a constant, not
a lookup". Using the shipped outro would have stamped the instructor's channel onto a
student submission. The lock's own scope clause resolves it: it applies to
`claude-liam-*` reels only, and "Other channels … NEVER get this card, handle, or mascot."
So this reel has its own `ShiftOutro`, its own corner bug, and no mascot — and the
narration deliberately omits the IN-FOR-BEAR line ("this is Liam, in for Bear") that every
worked example carries.

**3. GATE T cannot be run at all in this checkout.** The SKILL.md says "**GATE T
(type-lock) — ALWAYS RUN**, like factcheck. `scripts/type_check.py` asserts §8.1 min-size,
§8.2 overflow, §8.3 contrast … then writes `TYPECHECK.md`. No `./art run` and no
`./art final` may report success while `TYPECHECK.md` has any FAIL." That script is not in
the public cut — there is no `scripts/` directory at the toolkit root, and
`find . -name type_check.py` returns nothing. So the gate the doctrine calls mandatory is
unrunnable here. I did the type checks it describes by hand instead: min type size, the
overflow/edge-safe check, and contrast are all covered by the Gate V pass and the band
arithmetic I worked out for B02 and B04. Recording it because a missing mandatory gate is
exactly the kind of thing that should not be discovered silently.

**Why the outro one mattered more than it looks:** the prerequisite's own rule is "Do not imply a
synthetic narrator is me, Bear, or an official endorsement." Copying the exemplar's
bookends faithfully would have broken that rule *by being faithful*. The synthetic voice
therefore never says "I am" anyone; authorship is carried on screen, and the disclosure is
on the outro card, in `SOURCES.md`, and in the README.

**What Claude contributed:** Caught both conflicts by reading the lock file's scope clause
rather than just its rules, and proposed the own-outro fix.

---

## 2026-09-15 — Library-first, and a miss that became components

**Tried / expected:** GATE L in the SKILL.md requires asking the scene library before
authoring anything: "A miss is never a licence to slate." I expected to find a
numbers-transforming component among the 610 registered scenes.

**What happened:** Genuine miss. `./art scenes` returned leads for pipelines, code blocks
and comparisons, but every candidate was reel-local to someone else's film with its
content hardcoded and only a `sparkLine` prop — nothing parameterized for arbitrary
figures.

**What was done:** Claude treated it as the PUNT the doctrine describes — a design card, not a
slate — and authored six reel-local components in
`brutalist.art/runtime/remotion/src/ShiftedNotChanged.tsx` and registered them in
`Root.tsx`, then ran `./art scene-index` so they are discoverable (index went 610 → 616
renderable). Every component takes its numbers as **props**, so a wrong figure is a
beat-sheet fix and never a component fix.

**Evidence:** `./art scenes --check ShiftPipeline` → `RENDERABLE 16:9`; the six scenes now
in `scenes.json`.

---

## 2026-09-15 — The first cut compiled cleanly and was still wrong

**Tried / expected:** `./art run` finished, reported 11/11 slots filled, 186.0 s, zero
BLOCKER defects. I expected to be done and to go write the README.

**What happened:** Gate V flagged 4 MAJOR `underfill` defects, so I opened the contact
sheet — and found **two more problems no gate reported**, both inside the safe area where
no automated rule looks:

1. **B01's correction never fired.** The beat types "…makes softmax numerically stable."
   and the phrase just *stays there*. The entire video argues that "numerically stable" is
   the wrong word, and my overview beat was leaving the wrong word uncorrected on screen.
   Cause: `BrutalistHesitantWriter` matches `triggerWords` **per whitespace token**, so my
   two-word trigger `numerically stable.` could never match anything. It failed silently.
   Fixed by moving the misconception onto one token: `stable` → `overflow-safe`.
2. **B04's verdict line overlapped the fraction above it.** "The shift never reaches the
   ratio." was sitting on top of the denominator.

And the `underfill` on B10 turned out not to be a layout mistake at all.
`remotion_scenes.py` renders the *registered* composition length and then conforms to the
audio — freeze-holding a short clip but **truncating** a long one. My outro was registered
at 7 s against a 2 s narration, so only the first 29% ever played and the author line and
the disclosure were never in the file. Fixed by pinning every registered duration to the
measured mp3 and giving the outro a real sign-off.

**What was done:** Re-banded B02 and B04 with explicit vertical gaps, scaled B01 and B10 up,
relabelled the motion field honestly (every body beat had been tagged `illustrate` when the
scenes do different things — the label was the defect, not the motion), cleared `media/`
and `clips/`, and re-rendered. Full write-up with severities in
[`REVIEW.md`](REVIEW.md).

**What Claude contributed:** Read the sampled frames, spotted the two collisions the gate
missed, and traced the B10 underfill to the truncation rule in `remotion_scenes.py` rather
than treating it as a font-size problem. It also reproduced the token-matching bug outside
the renderer to prove the cause instead of guessing.

**What this showed:** the "VISUAL QC LAW" had been treated as bureaucracy — a box to
tick after the render. It is the opposite. A successful compile reported 11/11 slots
filled; it could not report that one of those slots contained the exact misconception the
film exists to demolish. **The mp4 probe and the gate agreed the film was fine. Looking at
it was what disagreed.** That is the same distinction the chapter keeps making — a passing
check is evidence for its stated property, and nothing more — and the build hit it within
an hour of narrating it.

**Evidence:** `_qc/REPORT.md` (round 1: BLOCKER 0, MAJOR 4), `_qc/contact_sheet.png`,
`REVIEW.md` R1-1 through R1-6.

---

## 2026-09-15 — A submission-path conflict I did not invent a rule for

**What happened:** The Canvas brief says to post under
`fall-2025/first-name-last-initial/week-01-video/`.
[`prerequisites/github-submission.md`](../../../prerequisites/github-submission.md) says
`fall-2025/first-name-last-initial/assignment-XX/`. They disagree, and the folder also
says `fall-2025` while the course is Fall 2026.

**What was done:** Followed **Canvas verbatim** (`week-01-video`, `fall-2025`), because the
brief states "Canvas is the authority on which version applies to your section" and the
same policy note logs the unreconciled wording under instructor decisions, item 7. Flagged
rather than silently normalized — a grading rule is not the session's to pick. (Superseded
on 2026-09-24: the live repo settles the path as `fall-2026/suketh-p/`.)

---

## 2026-09-18 — Second pass, after re-reading the AI policy

**Tried / expected:** The film was clean on 2026-09-15. I then sent the instructor's
AI-policy video and asked for a better version. Re-reading the
[AI policy](../../../prerequisites/ai-policy.md), one line reframed the pass: *"Iterate:
examine the first result, identify weaknesses, revise, test, and improve it."* Treating the
first clean render as the deliverable is exactly what that sentence warns against, so the
session went looking for the weakest part of the submission rather than polishing the
strong parts.

**What the session found — the weakest claim was the best one.** B07 said the cliff is at −746. True,
but I had found it by *sweeping inputs*. Poking a function until it breaks proves a
boundary exists; it does not explain why it sits there, and it would not transfer to
another float format or another function. That is a thinner kind of evidence than the rest
of the film, and it was sitting on the film's most important beat.

**What was done:**

1. **Derived it instead.** binary64's smallest subnormal is 2⁻¹⁰⁷⁴; under round-to-nearest
   anything below half of that has no nearer representable neighbour than zero, so
   `exp(z)` returns `0.0` once `z < ln(2⁻¹⁰⁷⁵) = −1075·ln 2 = −745.133219102`. Bisecting
   the real boundary agrees **to nine decimal places**, and −746 is simply the first
   integer past it. B07 now shows the closed form. The number went from discovered to
   predicted.
2. **Measured what the boundary actually costs.** I had been saying "a small probability
   becomes zero", which undersells it. `probabilities([0, −800, −900])` returns
   `[1.0, 0.0, 0.0]` — two outcomes **100 nats apart** reported as the same number. That
   is not a rounding nuisance, it is a loss of ordering.
3. **Showed the remedy.** Carrying the same distribution in log space keeps
   `[0.0, −800.0, −900.0]` — correctly ranked, nothing lost — and reproduces the reference
   to 1e-12 on `[1,2,3]`, so it is the same mathematics and not a different answer. This
   is what production libraries do, and it is the practical end of the film's boundary.
4. **Kept it out of the film.** All of (2) and (3) live in `evidence/boundary_analysis.py`,
   not as beats. The brief says pick the smallest idea and explain it completely; adding a
   remedy act would have been a second concept. Only the one-line derivation went on
   screen, because it deepens the claim already there.

**The correction I did not expect to have to make.** I wrote into `mutation_check.py` that
removing the max-subtraction would leave "the sum-to-one and chapter-table tests" green.
Then I ran it. **Wrong.** The 8 survivors are almost entirely the tests that never call
`probabilities()` at all — my own closed-form derivation tests, plus the raw `math.exp`
overflow test. Those verify the *mathematics* and are structurally blind to a defect in
the *implementation*.

That is a real coverage boundary in the suite, and it only showed because the check was
run instead of trusted. The script now prints the survivor list
from the run rather than asserting it, so the claim cannot drift from the evidence again.

**What this showed:** "28 tests, all green" had been treated as the evidence. It is not
— it is a claim *about* evidence. Mutation testing is what turns it into evidence, and
when it ran, the suite was still sound (4/4 mutations caught) but the *description* of it
was false. That is the film's own distinction — a passing check is evidence for its stated
property and nothing more — arriving a third time, in the paperwork, after the film had
already narrated it twice.

**What Claude contributed:** the derivation, the log-space demonstration, and
`mutation_check.py` itself — including the run that corrected the claim written into it. Per-portion
breakdown in [`SOURCES.md`](SOURCES.md) §4.

**Evidence:** `evidence/boundary-output.txt`, `evidence/mutation-output.txt`,
`FACTCHECK.md` rows 17–18, `SOURCES.md` §5.5–5.6, `REVIEW.md` round 6.

---

## 2026-09-20 — I stopped using a missing script as an excuse

**Tried / expected:** Three times now I had written a version of "GATE T could not be
run — the script is not in the public checkout." It is a true sentence. It is also an
excuse, and the SKILL.md is blunt that the gate is mandatory: *"No `./art run` and no
`./art final` may report success while `TYPECHECK.md` has any FAIL."* My film was
reporting success with no TYPECHECK.md at all.

**What was done:** Claude wrote the gate. `evidence/gate_t_typecheck.py` implements the parts of §8
that can be checked honestly from the scene source and the beat sheet — §8.1 min-size,
§8.3 WCAG contrast, §8.5 word budget, §8.6 figure-wiring — and writes `TYPECHECK.md`. The
header states plainly what it does **not** cover (§8.2 overflow and §8.4 kerning need
rendered frames and font metrics; §8.6 checks wiring, not pixels) so it cannot be mistaken
for the real gate.

**What happened — it failed on the first run, and it was right.**

1. **The worst one.** `GHOST` (`#B0AD9A`) on the cream stage measures **1.98:1**. WCAG
   AA-large wants 3:1. And `GHOST` was the colour of the **synthetic-narration
   disclosure** on the outro card — the single line in this film that has an ethical
   reason to be readable, rendered almost invisibly. I had picked it by eye for
   "quiet" and never measured it. All three `GHOST` text uses are now `SOFT` (4.37:1).
2. **`ACC` on cream is 2.74:1**, also under AA-large. This one I cannot fix:
   `CLAUDE-BRAND.md` says the palette replicates the real product and must not be
   retinted. So the gate now records it as a brand-locked WARN and **checks the
   mitigation** instead (§8.3b) — every terracotta element must also differ by weight,
   size, or a rule, so colour is never the only signal. That check immediately found
   B03's focal cells were colour-only; they gained `fontWeight: 700`.
3. **Two figures flagged as "not in any recorded run" — a false positive in my own
   check.** `0.3678794412` and `0.6652409558` are correct 10-dp roundings of
   full-precision values, and the second is verbatim Chapter 1's published table. The
   check now accepts a correct rounding and prints which value it rounded, instead of
   demanding a substring match.

State on this date: **0 FAIL · 3 WARN · 27 PASS** — the brand-locked accent plus two beats
1–2 words over the soft word budget. (The two word-budget warnings were cleared on
2026-09-24 when I rewrote those beats for precision; the gate now reads **0 FAIL · 1 WARN ·
29 PASS**, with only the un-retintable accent remaining.)

**What Claude contributed:** wrote the gate, and ran it. The GHOST contrast defect had
survived five rounds of visual QC, including Claude's own frame-by-frame reads of that
outro card, which had judged the disclosure "appropriately subtle" rather than "failing
contrast." An arithmetic check caught what looking had not.

**What this showed:** this is the third time in this project the same shape has
appeared. A green gate, a passing test suite, and a frame-by-frame read all reported
"fine" about something that was measurably not. The film argues that ranking a
continuation highly is not evidence it is true; the build kept demonstrating the same
thing about its own checks. The useful question for any check is not "did it pass" but
"what would still be wrong if it did."

**Evidence:** [`TYPECHECK.md`](TYPECHECK.md), `evidence/gate_t_typecheck.py`,
`CHECKS-REPORT.md` §GATE T, `REVIEW.md` round 7.

---

## 2026-09-24 — Preparing the GitHub posting, and a claim I could stop conceding

**Tried / expected:** I asked for everything except the video to be pushed to
`nikbearbrown/info-7375-prompt-engineering-for-generative-ai/fall-2026/suketh-p`. Write
access was assumed.

**What happened — four things I did not know:**

1. **There was no push access** (at the time — it was granted later that day; see the
   last entry). `gh api` reported
   `{"pull": true, "push": false, "admin": false}`. A direct push is impossible; the
   route is fork → branch → PR. Two forks and one open PR already exist on the repo, so
   that is how it is being done in practice.
2. **The path is `fall-2026`, not `fall-2025`.** The Canvas brief says
   `fall-2025/first-name-last-initial/week-01-video/` and I had flagged that as an
   unreconciled conflict. The live repo settles it: `fall-2026/`, one folder per person,
   and `suketh-p/` already exists with a stub README the instructor seeded.
3. **CI runs on every pull request** — `.github/workflows/course.yml` executes
   `scripts/validate_course.py` on Python 3.11, 3.12 and 3.13. A submission that breaks
   it lands with a red X on a category explicitly graded for *proper* posting. The
   validator was run locally with the folder in place: **exit 0, 13 tests OK**.
4. **No classmate has submitted yet.** Every other `fall-2026/*` folder is still the stub
   README.

**The refinement that came out of it.** Checking the CI matrix prompted running the
evidence under more than one interpreter — and that is something `FACTCHECK.md` had explicitly
*conceded*: "Not claimed: that these figures reproduce on any other interpreter." It was
an honest concession, but it was a **testable** claim that had simply never been tested.

So Claude wrote `evidence/cross_check.py`. Every figure the film displays — the weights, the
distribution, the `1.1102230246251565e-16` difference, the boundary cases, the seeded
counts `[102, 268, 630]` — is **byte-identical across CPython 3.10.19, 3.12.7, 3.13.3 and
3.14.6**. And 3.14.6 is the interpreter **Chapter 1 records its own run on**, so this also
checks the film's numbers against the book's published environment, not just this machine's.

**What was deliberately not claimed:** turn that into "platform independent". All four
interpreters run on one machine, one architecture. The script prints the platform and
says so in its own output, and FACTCHECK now states the claim at exactly that size.

**And the same slip again, smaller.** The script's scope note said "Three interpreters".
It found **four**. A hardcoded count in a script whose entire job is checking numbers —
the note is now generated from the actual run. That is the fifth time this project caught
a figure asserted without being re-derived, and by now it reads less as carelessness than
as the default failure mode the film is about.

**What Claude contributed:** found the permissions and path facts with `gh`, ran the
validator, wrote `cross_check.py`, and caught its own hardcoded "three".

**Evidence:** `evidence/cross_check.py`, `evidence/crosscheck-output.txt`,
`FACTCHECK.md` §"Claims deliberately NOT made" (now measured), `S7`.

---

## 2026-09-24 — The repo rejected my submission, and it was right to

**Tried / expected:** Stage the folder, run the repo's own validator as a formality,
open the PR.

**What happened:** `python3 scripts/validate_course.py` **exited 1**:

```
Non-Python implementation: fall-2026/suketh-p/week-01-video/components/ShiftedNotChanged.tsx
```

Not a warning — a hard failure, and `.github/workflows/course.yml` runs that validator on
**every push and pull request** across Python 3.11/3.12/3.13. Committing the Remotion
source would have put a red CI check on the submission, in the one category
(`GitHub version posting`) that exists specifically to assess *proper* posting.

And the validator is only enforcing what `AGENTS.md` already says: *"use an external
brutalist.art checkout for its Node/Remotion and Python packages, **never vendor that
stack into the course**."* The build had read that line and applied it to `node_modules`
— it also covers the reel's own `.tsx`.

**The tempting fix, and why it was not taken.** Renaming to `ShiftedNotChanged.tsx.txt`
slips past the extension check in one second. That is gaming a validator whose rule I
agree with: the point is keeping a Node stack out of a Python-and-Claude course, not
policing suffixes. Writing the workaround would have been a small dishonesty aimed at a
grader's automation.

**What was done instead:** Claude dropped the `.tsx` and wrote
`components/README.md` (in the posted repo folder) — why it is not vendored (quoting both
AGENTS.md and the validator's actual source), where the file lives in the external
checkout, and the three excerpts a reviewer needs to judge the work: the no-hardcoded-
figures contract, the palette with the GHOST accessibility note, and the single frame
clock. The excerpts are **generated from the real file** at staging time, so they cannot
drift from it.

**Then the validator caught a second error.** The new `components/README.md` linked to
`../../../AGENTS.md`. From `week-01-video/components/` the repo root is **four** levels
up, not three. The session's own link checker had reported "14 resolve, 0 broken" —
because it ran *before* that file was written. The repo's validator found what the
session's check had already passed.

**Final state:** `validate_course.py` exit **0**. CI will be green.

**What this showed:** the submission had been treated as "a folder, dropped into their
repo." It is not — it is a contribution to a repository with a stated contract and
automated enforcement, and the contract disagreed with the layout. Reading
`AGENTS.md` as *rules for the course authors* rather than *rules for anything in this
tree* was the actual mistake.

**What Claude contributed:** ran the validator before proposing the PR rather than after,
read the rejection back to its source rule, and considered and rejected the `.tsx.txt`
workaround itself.

**Evidence:** `scripts/validate_course.py` lines 22–26; `.github/workflows/course.yml`;
`components/README.md` (in the posted repo folder).

---

## 2026-09-24 — Six drifts is a process problem, not six accidents

**Tried / expected:** A last read-through before submitting, expected to be tidying.

**What happened:** Claude counted how many times a number in the paperwork had drifted
from the thing it described. **Five.** The test-survivor claim, the body-beat word counts, the
"no component hardcodes a number" overreach, "two digits out of sixty", and "Three
interpreters" in a script whose whole job is checking numbers. Every one was found by
accident — because a check happened to be run, or because an unchanged duration looked
suspicious.

Five accidents is not luck running out. It is the absence of a check.

**What was done:** Claude wrote `evidence/doc_consistency.py`. It derives runtime, caption-cue
count, GATE T tally and test count **live** from `beat_sheet.json`, the `.srt`,
`TYPECHECK.md` and the test file, then asserts the seven current-state documents agree.

It found a **sixth** on its first run: `README.md` still said the master was `195.44 s`
when it is `195.16 s`. That figure had survived nine rounds and three find-and-replace
sweeps.

**The design decision worth defending.** `REVIEW.md` and `FRICTIONAL.md` are *dated logs*.
They quote 195.46 s, 111 cues, 0/3/27 — all true on the day they were written. The easy
implementation would have "fixed" those too, and that would have been the worst possible
outcome: a review log that edits its own history is not evidence of a review. So both
files are **exempt by design**, each now carries a current-state header at the top, and
the script verifies *that header* instead of policing the entries beneath it.

**What this showed:** each drift had been treated as a small slip to correct. Six of them says the artifact and its description were never mechanically
coupled — the documents were hand-maintained prose about a thing that kept changing
underneath them. That is the same shape as the film's own argument: a fluent description
and a supported one are different objects, and only one of them is checked.

**What Claude contributed:** counted the drifts, wrote the checker, and chose to exempt
the dated logs rather than normalise them.

**Evidence:** `evidence/doc_consistency.py`, `SOURCES.md` §5.14, the current-state headers
at the top of this file and `REVIEW.md`.

---

## 2026-09-24 — My tooling fabricated a quotation, and I nearly published it

**This is the most serious error in the project**, so it gets its own entry rather than a
line in a list.

**What happened:** Staging for GitHub, Claude ran a script it had written to rewrite
paths for the new folder depth. One rule changed every `fall-2025/…/week-01-video/` into
`fall-2026/suketh-p/week-01-video/`. Comparing the Canvas and GitHub copies before
submitting, Claude found what that rule had done to **this file**. The GitHub copy read:

> *"The Canvas brief says to post under `fall-2026/suketh-p/week-01-video/`."*

**Canvas never said that.** It says `fall-2025/first-name-last-initial/week-01-video/` —
that discrepancy is the entire point of the entry it appeared in. The rewrite didn't just
introduce an error; it **fabricated what a source document said**, and turned a passage
about a real conflict into a self-contradiction. In the Frictional log. Which exists
specifically to be an honest record, and which the AI policy says must not contain
fabricated citations.

**Why it happened.** A find-and-replace cannot tell a *navigation instruction* ("run this
from the posted folder at …" — safe, and correct, to update) from a *quotation of a
source* ("Canvas says …" — must never change). One rule treated both the same.

**What was done:**

1. **Removed the rule entirely.** Retargeting is now link depth and the video note —
   nothing else. The two genuine navigation instructions were fixed **at the source**,
   so both the Canvas and GitHub copies are right without any rewriting.
2. **Added an invariant to the staging step.** After normalising link depth, every
   staged document must equal its source except for the known, additive video section.
   Any other difference fails the stage.
3. **Proved the guard works** instead of assuming it: the original falsifying rule was
   reintroduced into a copy and the check run. It caught **all four** changed lines —
   both quotations, before and after. A guard never seen to fail is a claim, not
   evidence.

**What this showed:** every earlier drift in this log was a number that fell *out of
date*. This was different in kind — a tool written in this build produced a *false
statement about a source*, and it would have gone out under my name. The film argues that
fluent output and supported output are different objects. The staging script produced
fluent, plausible, wrong text about what a document said, and nothing about its output
looked wrong. It was caught only because the Canvas and GitHub copies were diffed before
submitting.

**What Claude contributed:** noticed the Canvas/GitHub copies differed where they should
not, traced the difference to the substitution rule, removed it, and wrote and
mutation-tested the invariant.

**Evidence:** the staging invariant; the verbatim quotations at the two passages above
(`grep "The Canvas brief says" FRICTIONAL.md`).

---

## 2026-09-24 — Before submitting: the film showed a fabricated Claude answer, and this paperwork spoke for me

**Tried / expected:** I asked for a deeper look at whether the assignment had been done and
submitted right. By then the instructor had given every student push permission for their
own `fall-2026/` folder, and said the GitHub posting is part of the assignment question and
rubric.

**What happened:** Claude re-read the brief sentence by sentence against the rendered frames
and every document, and found errors that nine rounds of review had not. This supersedes the
previous entry as the most serious error in the project.

1. **B00 showed a fabricated Claude response.** The cold open had three answer lines under a
   "Fable 5" model chip, and no prompt was ever sent. The brief: *"A video that fabricates a
   Claude transcript to make a cleaner story has failed the assignment on its own terms."*
   `SOURCES.md` and `FACTCHECK.md` meanwhile said no transcript was shown. (`SOURCES.md` §5.16)
2. **"One machine epsilon" was wrong, on screen and aloud.** The measured gap is 2⁻⁵³; Python's
   `sys.float_info.epsilon` is 2⁻⁵², twice that. "Wrong by exactly one bit" was also wrong:
   one of the two differing pairs differs in two bits. And "two digits out of sixty", logged
   as corrected in §5.12, was still in the scene's on-screen text — that fix had reached the
   narration and the docs but not the frame. (§5.17)
3. **B05 typed**, which the toolkit's typing rule forbids for inner beats, while
   `SHOTLIST.md` said it did not. (§5.18)
4. **The paperwork spoke for me.** `PROMPTS.md` said the B05 prompt "produced"
   `verify_claims.py`, but the session log shows the script ran before that text was written,
   and it was never sent to anyone. `SOURCES.md` §4 had a column headed "What I checked
   myself" listing checks Claude ran, and said I "asked the mirror question" that found the
   film's boundary; Claude asked it. Every code file said "Author: Suketh Produtoor". And this
   file's header said all the work happened on 2026-09-15, while it held six "What changed in
   my understanding" paragraphs that Claude wrote. The AI policy: *"do not ask AI to invent
   your struggle or understanding."* (§5.19)

**What was done:** Claude re-rendered B00, B05, B06 and B09 and re-narrated B06. It added a
test that reads the film's on-screen text against the recorded run, and showed that test
fails on the old beat sheet. It then re-attributed the documents: the dated entries here are
now labelled as Claude's record of the session, "What this showed" replaces the
understanding claims, the code headers say who wrote the code, and my own attempts, checks
and understanding are left to the `[MINE]` sections below. At my instruction the stale
pre-fix copies were then moved to the Trash, and the corrected version was posted straight
to `fall-2026/suketh-p/` on `main` — push access had been granted that day — on top of the
pull request's first commit, so the pull request and `main` carry the same history.

**What Claude contributed:** all of the above, and all four errors in the first place.

**Evidence:** `SOURCES.md` §5.16–§5.20; `REVIEW.md` Round 9;
`evidence/test_verify_claims.py` → `test_screen_and_narration_say_what_the_record_says`.

---

## `[MINE]` — my part

### What I did — the record

**Compiled by Claude from my own messages in the build sessions**, with the times those
messages were sent (EDT, from the session log). These are facts about what I did, not a
reflection, and not a claim about anything I did outside the sessions.

| When | What I did |
|---|---|
| 2026-09-15 09:42 | Cloned the `brutalist.art` toolkit into the project folder myself, and asked for the assignment to be done by following every piece of the course material, including the instructor's videos |
| 2026-09-15 09:46 | Chose the concept: the max-subtraction, the option Claude recommended from its shortlist |
| 2026-09-18 17:18 | Sent the instructor's AI-policy video and asked for a better version, "till I submit" |
| 2026-09-20 13:30 | Asked for another pass toward the best version |
| 2026-09-24 09:58 | Sent the rubric and asked for the work to be refined against the assignment again |
| 2026-09-24 10:49 | Set the posting rule: everything except the video goes to `fall-2026/suketh-p` on GitHub, for every refinement; the video goes to Canvas only |
| 2026-09-24 10:54 | Stopped the work to ask for an analysis of how to submit before anything was pushed |
| 2026-09-24 11:09 | Approved going ahead with the fork-and-pull-request route, after one more refinement pass |
| 2026-09-24 11:13 | Switched the session's model to Claude Opus 5.5 |
| 2026-09-24 11:26 | Asked for a list of every refinement made since the start — now `REFINEMENTS.md` |
| 2026-09-24 17:13 | Sent the instructor's push-permission announcements and asked for a deeper look at whether the assignment had been done and submitted right. That request found the errors in `SOURCES.md` §5.16–§5.20 |
| 2026-09-24 18:00 | Had the stale pre-fix copies deleted and the corrected version posted to git, and asked for the final Canvas submission |
| 2026-09-25 13:56 | Watched the cut and answered four reflection questions — below, as I wrote them. Answer 1 asked for the B06 change that became `REVIEW.md` Round 10 |

### My reflection — my own answers, 2026-09-25

On 2026-09-25 at 13:56 EDT I answered four questions Claude sent me. The answers below
are **as I wrote them**. Claude only converted the math notation to GitHub's `$…$` syntax
and placed them here. Answer 1 is also my review request: it is logged in
[`REVIEW.md`](REVIEW.md), and Claude re-rendered B06 to carry it out (Round 10).

#### 1. Did you watch the video? One thing you'd change.

Yes. One thing I would change is the floating-point comparison around 1:46–2:05. The video shows both full-precision probability vectors and then the 1.1102230246251565e-16 difference, but the important change is buried in the last digit of two long numbers. I would hold that frame slightly longer and isolate only the two differing digits, with a small “1 ULP apart” marker between them. The narration explains the idea correctly, but making that last-place difference visually obvious would make the distinction between algebraic equality and floating-point equality land faster.

#### 2. In your words: why does subtracting the max change nothing in algebra, yet the last digit still differs?

Subtracting the max does not change the softmax probability because it introduces the same multiplicative factor everywhere. If I subtract $m$ from every score, then

$$
e^{(z_i-m)/T}=e^{-m/T}e^{z_i/T}.
$$

That $e^{-m/T}$ appears in both the numerator and every term of the denominator, so it cancels exactly. In real-number algebra, the shifted and unshifted formulas are therefore identical.

The computer is doing something slightly different. Python uses finite binary64 floating-point numbers, not exact real numbers. The direct path and shifted path exponentiate different values, create different intermediate approximations, sum them, and round at different stages. Those rounding paths eventually land on adjacent representable floats. In the video, the maximum difference is only 1.1102230246251565e-16, or $2^{-53}$. So the mathematics did not change; the representation and rounding path did. That is why the formulas are exactly equal algebraically while two returned values can still disagree in their final digit.

#### 3. One thing you learned or that surprised you.

What surprised me most was that subtracting the max only protects one side of the numeric range. I initially associated the trick with making softmax generally “stable,” but the [0, -800] example makes that wording too broad. After shifting, the largest exponent becomes exp(0) = 1, so overflow at the large end disappears. But exp(-800) is so small that binary64 rounds it all the way to 0.0, even though the mathematical probability is still nonzero, around $10^{-348}$.

The part that made this concrete for me was that the cutoff is not an arbitrary experimental value. It comes from approximately

$$
-1075\ln(2)=-745.133219102.
$$

That is why -745 can still produce the smallest subnormal value while -746 becomes a hard zero. It changed how I think about the claim: overflow-safe is something the code demonstrates; numerically stable is a much stronger statement.

#### 4. One part you couldn't yet explain to a TA.

I could explain the overflow argument, the common-factor cancellation, and why [0, -800] underflows. The part I could not yet defend to a TA without working it out on paper is the exact IEEE-754 boundary at $-1075\ln 2$, especially why the derivation uses 1075 rather than 1074.

I understand the outline: binary64's smallest positive subnormal is $2^{-1074}$, and round-to-nearest introduces the halfway threshold $2^{-1075}$. Taking the natural log gives the cutoff where exp(z) starts rounding to zero. But I would want to re-derive the subnormal spacing and rounding behavior carefully before trying to explain the boundary conditions or tie case from memory. That is the part I understand conceptually but cannot yet teach cleanly without notes.

### Still open

- **What I personally re-ran or checked.** I watched the cut (answer 1). No script re-runs
  are claimed; every check in `SOURCES.md` §4 was run by Claude.
- **`REVIEW.md`'s three teaching questions** — does the narration get ahead of the screen,
  is B03 legible at a glance, could a classmate state both halves — are not answered yet.
