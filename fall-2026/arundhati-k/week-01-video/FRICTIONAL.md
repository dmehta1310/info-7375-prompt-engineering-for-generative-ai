# FRICTIONAL.md — Week 1 Explainer Video

Arundhati Kandelkar · INFO 7375 · Fall 2026
Concept: expected count (665.24) versus observed count (630)

---

## 2026-09-26 — verifying the numbers before building anything

**What I was working on.** Confirming that every figure I planned to put on
screen actually comes out of the course code, before committing them to a beat
sheet and a narration track.

**I tried / expected.** Ran `lessons/01-randomness-and-first-prompts/code/main.py`
unmodified from a clean clone. I expected the run to be reproducible without a
seed argument, because `sample()` defaults to `seed=7` in the signature, and I
expected the printed probabilities to match the three values I had drafted into
my beat sheet from reading the lesson.

**What happened.** It matched exactly:

```
probabilities: [0.09003057317038046, 0.24472847105479764, 0.6652409557748218]
counts:        {"1": 268, "2": 630, "0": 102}
```

Two things I had not noticed from reading alone. First, `Counter` prints its
keys in *first-encountered* order, not sorted order — so the raw output reads
`1, 2, 0`, and my beat sheet lists them as `0, 1, 2`. That is a display
reordering, not a data change, but it is the kind of silent tidy-up that would
make a grader wonder what else I rearranged, so I am recording it here rather
than letting the video imply the program printed them in index order. Second,
`probabilities()` divides by `temperature` *before* exponentiating, inside the
same expression as the max-subtraction — the subtraction is not a separate
stabilisation step bolted on, it is fused into the comprehension on line 15.

**What I did.** Kept the printed values to full precision in the beat sheet and
derived every on-screen number from them rather than from my own arithmetic:
665.24 is `0.6652409557748218 × 1000`, and the gap is `665.24 − 630 = 35.24`.
I re-derived both with Python rather than by hand so the video's arithmetic and
the code's output cannot drift apart.

**What I understand now / still do not understand.** I understand that the seed
makes my run *repeatable* and that is all it makes it — running it again gives
me 630 again, which is not independent evidence that 0.6652 is right. What I
still cannot do from this single run is say how far from 665 a run would have to
land before I should actually doubt the distribution. That boundary is the thing
the video explicitly declines to establish, and naming it honestly is the
falsifiability beat rather than a hedge.

**Evidence.** `main.py` output above, reproduced from an unmodified clone.
**Next step.** Restructure the beat sheet into the Brutalist schema.

---

## 2026-09-26 — toolkit setup: three things the free pipeline did not have

**What I was working on.** Getting `brutalist.art` to the point where it could
actually render, before authoring beats against components that might not exist.

**I tried / expected.** Cloned the toolkit, installed the Python requirements
and the Remotion dependencies, and fetched the Kokoro model. I expected the
Fellow Tier to be complete after that, because the toolkit's own CLAUDE.md
states the free path runs with no account and no keys.

**What happened.** Three separate gaps, none of them key-related:

1. **`ffmpeg` was absent.** This is not a cosmetic missing dependency — the
   whole pipeline is audio-first, so per-beat MP3 durations *are* the master
   clock that video conforms to. With no `ffprobe` there is nothing to measure
   and nothing renders at all.
2. **`ClaudeCallout` is not renderable.** `./art scenes --check ClaudeCallout`
   returned `NOT RENDERABLE — no <Composition> in Root.tsx`. The ai-explainer
   SKILL.md describes it as "the signature move of the brand" (freeze the UI,
   annotate it), so I had planned a beat around it.
3. **No LaTeX on the machine**, so Manim's `MathTex` cannot typeset anything.
   `docs/MATH-TYPESETTING.md` forbids silently falling back to plain text when
   the math renderer is missing, so this is a real constraint, not a style
   preference.

**What I did.** Installed `ffmpeg` via Homebrew (9.0.2), which fixed (1)
outright. For (2) I treated the miss as a punt per GATE L — the toolkit logs it
to `TEMPLATE-MISSES.md` itself — and designed the body beats around components
that `./art scenes --check` confirms are renderable, rather than authoring
against a composition that does not exist and discovering it at render time.

For (3) I considered installing KaTeX into the toolkit's Remotion runtime,
which `MATH-TYPESETTING.md` explicitly permits ("No LaTeX installation is
required if another route works"). I rejected it, for a reason that is about
the assignment rather than the tooling: the only thing that *needed* a fraction
bar and a summation index was a general statement of the softmax formula, and
the softmax derivation was a second concept competing with my actual one. Once
I cut the derivation down to a single "where 0.6652 comes from" beat, the
remaining math is unambiguous arithmetic, which `MATH-TYPESETTING.md` permits
in ordinary cards. Removing the dependency was the same edit as fixing the
scope problem.

**What Claude contributed.** Claude Code ran the verification, read the
790-line `ai-explainer` SKILL.md, and ran the GATE L `--check` calls that
surfaced the `ClaudeCallout` miss — that check is the one I would most likely
have skipped, and it would have cost me a render cycle. I accepted the
`ffmpeg` diagnosis and the scene-availability findings, because both are
directly verifiable from command output I can re-run.

I rejected its first framing of the LaTeX problem. It presented the choice as
a tooling decision — install KaTeX, install BasicTeX, or drop the formula — and
recommended installing KaTeX. That framing took my beat sheet's scope as
settled and asked only how to render it. The actual question was whether a
50-second softmax derivation belonged in a video about sampling variance at
all, given the brief's warning that covering several things badly is the
common failure. It named the scope problem when I pushed back on it, but the
order matters: the dependency question should never have come first, and I
should not have to catch that.

**What I still do not understand.** `lead_silence_s` is required by the
ai-explainer SKILL.md on the executive-summary beat (`0.8`, "it is not
defaulted"), and other skills in the toolkit write it into their beat sheets —
but grepping `runtime/` I cannot find anything that reads it. I have written it
on the beat as the law requires and will verify the rendered beat length
directly instead of trusting the field to do anything.

**Evidence.** `ffmpeg -version` → 9.0.2; `./art scenes --check ClaudeCallout`
output quoted above; `which latex pdflatex xelatex` → all not found.
**Next step.** Author the beat sheet, then run the PROOF GATE before the first
render.

---

## 2026-09-26 — the fact-check that changed the video

**What I was working on.** GATE F paperwork — writing `FACTCHECK.md`, a row per
claim, before the toolkit would build a final cut.

**I tried / expected.** I expected this to be transcription. I had already
verified every number against `main.py` and assumed the table would be ten rows
of ✅ and done in fifteen minutes.

**What happened.** It was not transcription. Writing the row for "a gap this
size is ordinary" forced me to ask *how* ordinary, which I had never computed.
The count for index 2 is Binomial(1000, 0.6652), so:

```
sd = sqrt(1000 * 0.6652409557748218 * 0.3347590442251782)  # 14.9230
z  = (630 - 665.2409557748218) / 14.9230                   # -2.3615
P(X <= 630)                                                #  0.010364
```

630 is about **2.4 standard deviations** low — roughly a **1-in-50** result. My
script called it ordinary. B01's on-screen correction landed on
`broken → normal`, and B06 drew 630 mid-pack in the distribution with the
caption "ordinary, once you can see the spread." All of that was false.

What bothers me is the direction of the error. It was false in the way that made
my thesis easier — the gap being unremarkable is a tidier story than the gap
being rare. I had verified the arithmetic and stopped, because the arithmetic
was the part I knew how to check. The claim resting on top of it went unchecked
for hours and would have shipped.

**What I did.** Rewrote B01, B05, B06 and B07 and re-rendered them. The concept
survives and is sharper stated correctly: the gap *is* unusual, and unusual
still is not evidence the probabilities are wrong, because it is one draw from
one fixed seed examined after the fact. A 1-in-50 result is a reason to run the
test, not a substitute for having run it. I also moved the 630 marker in B06 to
bin 3 — where z = −2.36 actually falls — so the picture and the narration agree.

I considered keeping "ordinary" and softening it to "not unusual enough to
worry about." I rejected that: it would have been a hedge chosen to avoid
re-rendering, not because it was true.

**What Claude contributed.** Claude Code ran the binomial calculation, flagged
that its own earlier script was wrong, and proposed the corrected framing. I
accepted the correction because I could re-run the arithmetic myself. Worth
recording that the error was in Claude's draft *and* that I had reviewed that
draft twice without catching it — fluent prose about statistics reads as
correct, which is the exact failure Chapter 1 is about. The check that caught it
was a mechanical one (fill in every row of a table), not a careful reading.

**What I still do not understand.** Whether "about 1 in 50" is the right thing
to say. P(X≤630) = 1.04% is one-tailed — about 1 in 97. I chose the two-tailed
reading (≈1 in 48) because I had no directional hypothesis before seeing the
data. I believe that is the conservative and honest choice, but I cannot yet
argue it as confidently as I can state it.

**Evidence.** `FACTCHECK.md` row 11 and its correction log.
**Next step.** Run the gates.

---

## 2026-09-26 — the two gates that disagree

**What I was working on.** Getting GATE V (frame-level visual QC) and GATE T
(typography) both green so `./art final` would produce a master.

**I tried / expected.** I expected these to be independent checks I could fix in
one pass each.

**What happened.** Five rounds, because they pull against each other.

- GATE V rejected 8 beats for `underfill` — content covering under 55% of the
  safe area. Most were not "too small" in the obvious sense; they were sampled
  at the 50% mark, mid-reveal, when only half the elements had animated in.
- Enlarging everything then produced **BLOCKER** `edge-bleed` on B02 and B04 —
  I had pushed content past the title-safe right edge (B02's grid reached
  x=1872 against a 1824 limit).
- GATE T then failed B07 for a wordy card (16 words > 12). Shortening the lines
  made the card physically smaller, which **re-failed GATE V** for underfill on
  the same beat. Fixing one gate broke the other.
- GATE T also failed B04/B05 on contrast: terracotta `#D97757` on cream is
  2.74:1, below WCAG 4.5:1.

**What I did.** Three different kinds of fix, and the distinction matters:

1. **Real defects — fixed at the source.** Front-loaded every reveal schedule so
   frames are full by ~50% and hold (this also made the beats read better).
   Recomputed the B02 grid and B04 plot geometry against `SAFE` arithmetic
   instead of eyeballing. Darkened B04's non-focal bars, which were genuinely
   too faint to read as data.
2. **A real constraint — resolved by separating two uses of one colour.** I
   split the accent: `#D97757` stays for *fills* (bars, spans), and terracotta
   *text* moved to `#A2442A`, the same hue at 5.42:1. WCAG governs text, not a
   solid shape, so this keeps the brand and clears the gate rather than
   trading one off against the other.
3. **False positives — registered, with reasons.** GATE T reported a 36px text
   run in B03. I extracted the frame at full resolution before touching
   anything: every designed element is 62–336px, and the sub-floor blob is the
   `×` glyph's ink extent. Same class as the period-dot and crossbar false
   positives the checker already documents. I added `ExpectedCount`,
   `ObservedCounts` and `TheGap` to the existing exemption lists with written
   justifications, matching ~20 prior reels.

I made myself look at the frame before claiming false positive, because
"the checker is wrong" is the most convenient possible conclusion and I did not
want to reach it by assumption.

**Two toolkit defects fixed along the way.** `ClaudeWindow` declared `width` and
`fontSize` in its schema but never destructured them — the card was hard-locked
to 1100px and 19px body text, which cannot pass canvas-fill on a 1920×1080
stage. I wired the props through, with the old values as defaults so no existing
reel changes. I also added an optional `sparkSize` to `IlluStage`/`SparkLine`
(default 40, unchanged) because the shared spark line sits just under the 41px
type floor.

**What I still do not understand.** The two gates encode real and partly
opposing goals — fill the frame, use fewer words — and nothing reconciles them.
I resolved B07 by making the card bigger while keeping the lines short, but I
found that by trial, not by any rule in the docs. I do not know whether there is
an intended order of precedence or whether every reel rediscovers this.

**Evidence.** `TYPECHECK.md` (GATE T: PASS), `_qc/REPORT.md` (0 BLOCKER,
0 MAJOR), `_qc/contact_sheet.png`.
**Outcome.** Master: 147.3s, 3840×2160, h264 + AAC, $0.00 spend.

---

## 2026-09-26 — the correction that did not propagate

**What I was working on.** A last consistency pass: reading all ten narrations
end to end against the assignment's requirements before submitting.

**I tried / expected.** I expected this to find nothing. I had already caught the
statistical error, rewritten four beats, re-rendered and passed both gates, so I
thought the reel was internally consistent.

**What happened.** B08 — the handoff — still carried the old framing. It asked
the viewer to find out "whether 630 is boring or surprising," and its on-screen
line read "if 630 sits mid-pack, the gap was never evidence." Both were written
before I knew 630 sits in the tail. B06 now draws it in the tail explicitly, so
the reel contradicted itself in its second-to-last beat.

I had fixed every beat that *made* the wrong claim and missed the beat that
*depended* on it. That is a different kind of miss from the first one: not an
unchecked fact, but an unchecked consequence. When I corrected B01, B05, B06 and
B07 I was working from a list of beats that mentioned the word "ordinary" —
B08 did not use the word, so it was not on the list.

**What I did.** Rewrote the handoff so it states the prediction the video
actually derived (tail, ~1 in 50), labels it as arithmetic rather than
measurement, and ends "if the plot disagrees with my number, the plot is right."
Regenerated B08's audio, re-rendered, rebuilt the master, re-ran both gates.
Runtime 146.69s → 147.24s.

The replacement is a better handoff than what I originally wrote. The first
version asked the viewer to answer an open question; this one hands them a
falsifiable claim of mine and asks them to try to break it.

**What I understand now.** Grepping for the wrong word finds the beats that say
it, not the beats that assume it. The check that worked was the dumb one — read
all ten in order, out loud, and listen for the contradiction. I do not have a
better method than that yet.

**Evidence.** `FACTCHECK.md` second correction section; `TYPECHECK.md` PASS and
`_qc/REPORT.md` clean on the rebuild.
