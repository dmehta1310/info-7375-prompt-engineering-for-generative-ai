# FRICTIONAL — Week 1 Explainer Video

Riya Kapadnis · INFO 7375 SEC 01 · Fall 2026

---

## Entry

**Date and what I was working on:** 2026-09-23 — choosing a concept and getting the real numbers before writing any script.

**I tried / expected:** I picked softmax shift-invariance ("subtracting the max changes the intermediates but not the distribution") because it is the smallest Chapter 1 idea I could explain end to end with arithmetic on screen. I expected to run `lessons/01-randomness-and-first-prompts/code/main.py`, read off the probabilities, and be done collecting evidence in one command.

**What happened:** `main.py` printed `[0.09003057317038046, 0.24472847105479764, 0.6652409557748218]` and counts `{1: 268, 2: 630, 0: 102}`. Those reproduce the 665.24-vs-630 figures the assignment quotes, so my checkout matches. But the lesson's `probabilities()` already subtracts the peak on line 15 — there is no un-subtracted path in the file. I could not show the contrast using the lesson code alone.

**What I did:** Wrote `evidence/shift_invariance.py`, which imports the lesson module unmodified and defines one naive variant with the `- peak` term removed and nothing else changed, so the comparison is honest rather than a retyped copy. Running it turned up something I had not predicted: the two probability lists are **not** bit-identical. `max absolute difference: 1.1102230246251565e-16` — one unit in the last place. My planned narration line was "the probabilities are identical," which is true in exact arithmetic and false in float64. I cut that line rather than keep a claim the evidence contradicts.

I also abandoned a second framing. I had planned to open on `[1000, 1000] → [0.5, 0.5]` as the hook, but the naive path there raises `OverflowError: math range error` rather than producing a wrong number, so it demonstrates a crash, not a distribution being preserved. It works as the consequence beat, not the opening one.

**What Claude or another person contributed:** Claude (Opus 5, Claude Code) located the course repo, ran `main.py`, and drafted `evidence/shift_invariance.py`. I accepted the naive-variant approach because it changes exactly one line and stays traceable to the lesson source. The 1.11e-16 finding came out of actually running the script, not from the draft — the draft's own summary line had also assumed the lists would match. That is the thing I would have narrated wrongly if I had not run it.

**What I understand now / still do not understand:** I understand why the shift is safe: `exp(x - c)` divides every weight by the same `exp(c)`, and a common factor cancels in the normalization. The check `probabilities([1000, 1001]) == probabilities([0, 1])` returns `True`, which is the same fact from the other side — the shared offset never carried the answer. Still open: I can state that the 1-ULP gap comes from float rounding, but I have not worked out *why* it lands on token 0 and token 2 and not token 1, and I do not yet know whether that is stable across machines or specific to this one. I will say on screen that this is float rounding and not claim more than I have checked.

**Evidence and next step:** `evidence/shift_invariance.py` and its captured run `evidence/shift_invariance_output.txt`. Course repo at commit `8f590fa0455aebc7a81f74f3c99ab0218bda5fa4`. Next: install FFmpeg (missing on this machine — `ffmpeg -version` returns `command not found`), then `./setup --install` in the `brutalist.art` checkout and draft the beat sheet against these numbers.

---

## Entry

**Date and what I was working on:** 2026-09-26 — checking the concept against what the rest of the section had posted, before committing a render to it.

**I tried / expected:** I had three days on max-subtraction and expected to spend today installing Brutalist and rendering it. Before that I pulled the course repo to sync, mostly as housekeeping.

**What happened:** The pull brought down eleven `fall-2026/*/week-01-video/` folders that did not exist on the 23rd. Two of them are my concept. `suketh-p/README.md` names it outright — "the max-subtraction: why `probabilities()` subtracts the largest score before exponentiating." `atharva-h` is the same property from the other side, "the softmax keeps only the gaps," and his version is 3:04 at 4K with twelve beats and a `verify/verify_claims.py` harness whose claim IDs map to individual beats.

Worse for me specifically: the thing I thought was my edge was already covered and covered further. I had `1.11e-16` — the last-bit disagreement between the naive and shifted probabilities. His C6 proves shift-invariance holds at `2**53-3` and breaks at `2**53-2`, and C8 shows the collapse to uniform at `1e17`. He did not miss the float story; he went past where I stopped.

**What I did:** Dropped the concept with the evidence already built. Relative Quartile is scored against the group, and being the third submission on ground someone has already covered thoroughly is a worse position than being first on ground nobody has taken. Cross-referenced the eleven posted READMEs against the assignment's suggested list and found "Expected count (665.24) versus observed count (630)" unclaimed. Kept `shift_invariance.py` in the folder rather than deleting it — it is real work that informed the decision, and the log should show what I abandoned.

Wrote `evidence/expected_vs_observed.py` and found something better than what I gave up. The lesson's default seed is not a typical draw. Expected 665.24, observed 630, which is 2.36 SD low; exact binomial puts `P(count <= 630)` at 1.04%, about one run in 96. I did not trust the formula alone, so I ran seeds 0–9999: the empirical mean is 665.234 against the formula's 665.24 and the empirical SD is 14.71 against 14.92, so the sampler is fair — but only 89 of 10,000 seeds land at or below 630, putting seed 7 at the **0.89th percentile**, below p1 (631). The textbook's own default is one of the ~1% most extreme low draws.

**What Claude or another person contributed:** Claude (Opus 5, Claude Code) pulled the repo, surveyed the eleven posted submissions, read `atharva-h`'s verify log, and recommended the switch. I accepted it — the reasoning about being third on a crowded concept matched what the Relative Quartile rubric actually compares. Claude wrote `expected_vs_observed.py`; I asked for the 10,000-seed empirical check specifically, because a video that only quotes a binomial formula asserts the spread instead of showing it. Claude also caught, on the 23rd and again today, that two AI-written plans I was handed claimed these numbers "come from the chapter." They do not. `docs/en.md` is 106 lines and contains none of them — grep for `0.6652`, `1000`, `0.5, 0.5` returns zero hits each. The numbers come from running `main.py`. I am citing the run, not the chapter.

**What I understand now / still do not understand:** The gap between 665.24 and 630 is not a bug and not evidence of one — it is ordinary sampling variance, just an unusually large draw of it. What I did not expect is how strong the boundary case is: a sampler genuinely biased to p=0.63 produces exactly 630 with probability 0.026, about fifteen times more likely than the fair sampler's 0.0017. Both stories produce the number I saw. One run of 1000 cannot separate them.

Still open: I do not know whether seed 7 was chosen deliberately to make this point or is just the default someone typed. I cannot establish intent from the code, so I will not claim it in the video — I will say the default seed happens to sit at the 0.89th percentile, which is what I verified, and stop there.

**Evidence and next step:** `evidence/expected_vs_observed.py` and `evidence/expected_vs_observed_output.txt` (10,000-seed run, deterministic — seeds 0–9999, re-runs identical). Superseded work kept at `evidence/shift_invariance.py`. Next: install FFmpeg, `./setup --install` in `brutalist.art`, and draft the beat sheet against these numbers.

---

## Entry

**Date and what I was working on:** 2026-09-26 (later the same evening) — installing the toolkit and rendering.

**I tried / expected:** I expected `./setup --install` to be one command, and the render to be the risky part. I had it backwards: the install broke three times and the render worked first try. What actually cost me was QC.

**What happened, in order:**

1. `pip install -r requirements.txt` failed on `manim<0.19`. My Python is 3.13.7; every manim 0.18 release pins `Requires-Python >=3.9,<3.13`. Not a network problem — no such wheel exists.
2. Rebuilt the venv on Homebrew's Python 3.11.14. `pycairo` then failed at `meson setup`. `cairo` and `pango` were already installed; `pkg-config` was not, so the build could not locate them. `brew install pkg-config ffmpeg` fixed it.
3. `./setup` exits early on an internal lint ("ElevenLabs reference found") that fires on the toolkit's own example files, before printing its readiness table. I checked each dependency directly instead of trusting the script's exit code.
4. First manim run: `RuntimeError: latex failed but did not produce a log file` on four of seven scenes. I had deliberately avoided `MathTex`, but `include_numbers=True` on `NumberLine` and `Axes` routes tick labels through MathTex. Replaced them with a `Text`-based `tick_labels()` helper. No LaTeX is installed and none is needed.

**What I did:** After the first full assembly I nearly stopped — the pipeline reported success, all seven scenes rendered, the runtime was 2:48, inside the target. Then I read the sync table `assemble.py` prints, and it showed B04 holding a frozen frame for 17.00 seconds and B06 for 16.99. The animations were roughly half the length of their narration, so `tpad` was holding a still image for half of each beat. A green build and a video that was one-fifth frozen frames.

I repaced the scenes rather than padding them — the histogram build went 4s → 11s, the two distribution curves 1.8s → 4.0s each — so the motion fills the narration. Longest hold is now 1.99s, and that is a deliberate pause on the closing card.

Then I extracted frames and looked at them, which found three more things no log reported: B02's highlight ring sat in the middle of the number instead of around the fractional tail (`Circle` with a fixed radius, replaced with `SurroundingRectangle`); B03's mean label was printed on top of the SD formula; and B06's closing card — the boundary statement, the most important frame in the reel — was printed directly over both curves and the x-axis labels, unreadable. Fixed by parking the formula in a corner and dimming the chart to 10% before the card appears.

**What Claude or another person contributed:** Claude (Opus 5, Claude Code) did the installs, wrote the scenes, and drove the renders. It also diagnosed all four failures above. The 17-second frozen frames were caught by Claude reading its own sync table and flagging it rather than reporting success — worth recording, because the pipeline's exit code was 0 at that point and I would not have known. The three label collisions were found by rendering frames to a contact sheet and inspecting them; two rounds of fixes were needed, because the first fix for B03 introduced a new overlap with the scene title.

**What I understand now / still do not understand:** The lesson I will actually keep: an exit code of 0 and a plausible runtime told me nothing about whether the video was watchable. Every real defect was found by looking at frames. "It rendered" and "it explains the concept" are different claims, which is uncomfortably close to the thing my own video is about.

Still open: I do not know why manim's `include_numbers` routes through LaTeX when a `Text` path exists, and I have not checked whether 0.19+ changed that. Not worth resolving before submission, but it is the first thing I would look at if I reuse this setup.

**Evidence and next step:** `qc-sheet.png` (the contact sheet the defects were found in), `audio/timings.json` (measured narration, the master clock), `BUILD-PROMPT.md` §"Stage 6" (all four defects with fixes), `riya-k-expected-is-not-a-promise.mp4` (168.53s, verified with `ffprobe`). Toolkit at `6a8380ae169cca81e0633664a65c958f5c12ab4b`. Next: review the cut end to end, then commit and push.

---

## Entry

**Date and what I was working on:** 2026-09-26 (late) — watching the finished cut in QuickTime before committing.

**I tried / expected:** I expected to watch it once and push. The contact sheet had looked clean and the sync table showed no hold longer than two seconds, so I thought review was a formality.

**What happened:** Watching it in a player rather than as stills found two collisions the contact sheet had missed, because I had sampled frames at times where the colliding elements had not both appeared yet.

At 1:57, B05 was unreadable: the observed-value marker, its "630" label and the "p1 = 631" gridline were all printed across the words "0.89th percentile". The cause is that 630 and 631 are one apart, so at this axis scale they occupy the same horizontal position — they can never sit in the same band, no matter how the text is nudged. At 2:19, B06's orange curve label was anchored relative to a data point near the left edge of the plot and ran off the frame: it rendered as "pler  p = 0.6300".

Two structural problems that were not bugs at all, just wrong decisions I had signed off on: the reel opened cold on the problem with no title, so a viewer had no idea what they were about to watch or who made it; and it ended on a credits card listing my name and the build files, which is not an ending — it is a colophon.

**What I did:** Moved the 630 label below the axis with its own tick and shortened the p1 gridline, so the two values are separated vertically instead of competing for the same x. Made both curve labels in B06 a legend pinned to the frame corners rather than positioned relative to data, which is what let one drift off-screen in the first place.

Then restructured the ends. Added `B00_Title`: title, my name and the course, then the setup in three lines and the question the reel actually answers. Rewrote B01's narration so it no longer re-introduces the premise B00 now covers, and cut it from 45 words to 32. Replaced the credits card with `B07_Conclusion` — not a bug, the sampler is fair, seed 7 is unusual — closing on "reproducing a number is not the same as knowing why you got it." Attribution moved entirely to SOURCES.md, where it is graded anyway.

Both new beats then needed repacing: B00's animation ran 11.1s against 25.4s of narration and B07's ran 12.9s against 30.4s, so `assemble.py` was again holding frozen frames for half the beat. Same failure as this afternoon, caught the same way — by reading the sync table rather than the exit code.

I also deleted `render/` during a cleanup and did not notice until `assemble.py` crashed on a missing B02 with `ValueError: could not convert string to float: ''`. Cheap to fix (re-render), but the failure was unhelpful — `vdur()` does not check whether ffprobe actually returned anything, so a missing file surfaces as a float parse error four frames up the stack.

**What Claude or another person contributed:** I watched the cut and sent Claude three screenshots with what was wrong in each. Claude diagnosed the 630/631 collision as a geometric impossibility rather than a spacing problem, which is why the fix moved one label to a different axis instead of nudging it. It wrote B00 and B07, and repaced both after the sync table showed the holds. I directed the structural changes: title at the front, conclusion at the back, my name out of the ending.

**What I understand now / still do not understand:** Stills are not a substitute for watching. Both collisions existed in frames I never sampled — the contact sheet was seven frames out of 6,400, and I picked the times, so I was checking the moments I already expected to be fine. The only reason I found these is that I watched it.

Still open: I do not have a way to catch label overlap automatically. Claude suggested rendering every beat's final frame rather than one mid-beat frame, which would have caught both of these, but it would not catch a collision that appears mid-animation and resolves. I do not know what the real answer is short of watching every cut.

**Evidence and next step:** `scenes.py` (`B00_Title`, `B07_Conclusion`, and the B05/B06 fixes), `audio/timings.json` (now 213.57s across eight beats), `BUILD-PROMPT.md` §"Stage 6" items 5–7. Final cut 213.66s, verified with `ffprobe`. Next: commit and push.

---

## Entry

**Date and what I was working on:** 2026-09-26 (final) — staging the submission for GitHub.

**I tried / expected:** I expected `git add fall-2026/riya-k/week-01-video/` to stage everything in the folder, including the video, because the assignment brief lists "The rendered video file (mp4)" as a GitHub deliverable.

**What happened:** 17 files staged and the mp4 was not among them. `git check-ignore -v` pointed at the repository's own root `.gitignore` line 33, `*.[mM][pP]4`, under the comment "Keep generated audio/video out of Git, at any depth and in any case." The exclusion is deliberate and repo-wide, not something in my folder.

That is a direct conflict with the assignment brief. Two things resolve it against the brief: `prerequisites/github-submission.md` says plainly "A video is not required" for the GitHub posting category, and `atharva-h`, who submitted before me, hit the same rule — his README records "Submitted via Canvas; not in this folder yet — media is held back from the repo."

Separately, and more seriously: staging is also where I found that 280 files belonging to other students were showing as deleted in my working tree. I had deleted those folders in Finder earlier to tidy up my Documents directory, not realising they are tracked — so git had them queued as deletions. If I had staged broadly with `git add -A` instead of by explicit path, I would have committed the removal of 47 classmates' submitted work and pushed it to `main`. Restored with `git checkout -- fall-2026/`; verified `HEAD == origin/main` and that the only untracked path is my own folder.

**What I did:** Did not override the ignore rule with `git add -f`. Forcing a 9 MB file past an explicit repo-wide policy in a repository shared by 48 people is not my call to make unilaterally, and the grading guide does not ask for it. The video goes to Canvas; the README now states where it is and why, and the folder rebuilds it exactly.

Staged by explicit path rather than `git add -A`, and checked `git diff --cached --name-status` before committing: 17 files, 0 outside `fall-2026/riya-k/`, 0 deletions.

**What Claude or another person contributed:** Claude caught the missing mp4 by reading the staged file list instead of assuming the add had worked, traced it to the ignore rule with `git check-ignore -v`, and found the supporting evidence in `github-submission.md` and `atharva-h`'s README. It also caught the 280 pending deletions and restored them before anything was committed, and flagged the policy conflict rather than silently forcing the file in.

**What I understand now / still do not understand:** Deleting tracked files in Finder is not a local tidy-up — git reads it as a change to publish. I did not connect those two things until it nearly went out.

Still open: the brief and `github-submission.md` disagree about whether the mp4 belongs in the repo. I have followed the repo's own rule and the grading guide, and documented it here rather than picking a side quietly. If the intended answer is that the video should be committed, this entry is where to look.

**Evidence and next step:** `git check-ignore -v` output quoted above; README "Video" paragraph; `git diff --cached --name-status` (17 files, none outside my folder). Next: commit, push, zip for Canvas.

---
