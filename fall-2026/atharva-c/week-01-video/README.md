Expected Count vs. Observed Count
==================================

Student: Atharva C
Course: INFO 7375 -- Prompt Engineering for Generative AI
Assignment: Week 01 Video -- Chapter 1 Concept Explainer
Runtime: 2:42 (162.46 s)

Concept
-------
Expected count vs. observed count: Chapter 1's own code turns three scores
(logits `[1, 2, 3]`) into probabilities with softmax, giving one outcome a
probability of 0.665, then samples 1,000 times with a fixed seed. The
expected count is 0.66524 x 1,000 = 665.24. The actual recorded run gave
630 -- a gap of 35.24, about 2.4x the typical wander for a sample this
size. That gap is unusual but not impossible, and it isn't evidence the
sampler is broken.

Why this concept
-----------------
The real output from `main.py` already contains this exact gap, so the
whole explanation could be built from one worked example with no invented
numbers -- probabilities, counts, and the seed all come straight from the
course's own reference code. It also has a clean, statable boundary: a
single seeded run can tell you the gap is unusual, but it can't by itself
prove whether the sampler is fair. That takes many runs with different
seeds, which this assignment didn't do.

Files
-----
| File | What it is |
|---|---|
| `beat_sheet.json` | the reviewed narration + visual plan, beat by beat |
| `BUILD-PROMPT.md` | the prompts and exact commands used to rebuild the video |
| `SOURCES.md` | evidence paths, what Claude contributed, synthetic-narration disclosure |
| `FRICTIONAL.md` | dated log of what broke during the build and how it was resolved |
| `REVIEW.md` | the review and decision record -- every approval, rejection, and revision |
| `FACTCHECK.md` | every on-screen claim traced back to its evidence |
| `BUILD-LOG.md` | a chronological log of the build across all review-cut rounds |

The rendered video (`week-01-video-atharva-c.mp4`) is submitted through
Canvas only, per the course convention of keeping large media out of the
shared repository; it is not included in this GitHub folder.

Reprint the numbers (no toolkit needed)
----------------------------------------
`main.py` was run, never edited. From the course repository root:

```
python3 lessons/01-randomness-and-first-prompts/code/main.py
```

This prints the exact probabilities `[0.09003057317038046,
0.24472847105479764, 0.6652409557748218]` and the exact counts
`{"1": 268, "2": 630, "0": 102}` (outcomes 0, 1, 2 = 102, 268, 630) that
every number in the video is traced back to.

Rebuild the video
------------------
Needs the Brutalist toolkit (`brutalist.art`) with its one-time setup done
(`./setup --install` in the toolkit: Python and Remotion npm packages, fonts,
and the Kokoro voice model), plus ffmpeg/ffprobe on your PATH. See
`BUILD-PROMPT.md` for the complete build loop. In short:

```
TK=~/Applications/brutalist.art
cd $TK && source .venv/bin/activate

REEL=~/Applications/info-7375-prompt-engineering-for-generative-ai/youtube/week-01-video-atharva-c
python3 runtime/scripts/generate_audio_kokoro.py "$REEL"   # audio first: measured durations
./art run "$REEL" --height 1080                            # compile the 1080p review cut, run gates
./art todo "$REEL"                                          # list any unfilled beats
./art final "$REEL" --height 1080 --out "$REEL/final"       # clean 1080p master
```

Narration is a synthetic Kokoro voice (`af_bella`), disclosed on screen in
the opening beat and again on the closing credits card; it is not the
author's voice and not the instructor's.
