# Frictional — Week 1 Seed Explainer

**Student:** Anisha Gaikar  
**Assignment:** Week 1 Explainer Video — Explain One Concept from Chapter 1  
**Course:** INFO 7375

This is an honest build record. Codex organized it from the work performed on 2026-09-26; it does not invent a personal test, difficulty, or Claude interaction.

## 2026-09-26 — Selecting a genuinely different backup concept

**Date and what I was working on:** 2026-09-26, choosing a second submission candidate without duplicating the first max-subtraction video.

**I tried / expected:** I requested another complete assignment as a spare. I expected the new topic to be different while still meeting every Week 1 requirement.

**What happened:** “A seed makes a run repeatable; it does not make the answer true” was narrow enough for one video and directly supported by Chapter 1's code, test, and boundary language.

**What I did:** I kept the first project untouched and placed this version in an independent submission folder. I limited the video to the seed's role rather than expanding into a general summary of randomness.

**What Claude or another person contributed:** Claude was not used. Codex proposed the topic, found the relevant course passages and test, drafted the beat sheet, and assembled the independent project. I requested the distinct spare and the complete deliverables.

**What I understand now / still do not understand:** The artifact separates repeatability from truth. Before submitting, I still need to watch the full video and practice explaining why a fixed seed is a replay control rather than an answer key.

**Evidence and next step:** `beat_sheet.json`, `SOURCES.md`, and the independent project history. Next: reproduce the exact course output.

## 2026-09-26 — Reproducing the observed counts

**Date and what I was working on:** 2026-09-26, verifying every number shown on screen.

**I tried / expected:** The unmodified Chapter 1 program was run for its published seed-7 result. A second script repeated seed 7 and changed only the seed to 8.

**What happened:** Seed 7 returned `{0: 102, 1: 268, 2: 630}` twice. Seed 8 returned `{0: 76, 1: 239, 2: 685}`. The probabilities remained `[0.090030573…, 0.244728471…, 0.665240955…]` because the logits and temperature were unchanged.

**What I did:** I preserved the output in `code/course_main_output.txt` and `code/seed_output.txt`, labeled `[1,2,3]` as a course-constructed input, and added three executable checks for the probabilities, repeatability, and recorded counts.

**What Claude or another person contributed:** Codex ran the course program, wrote the standalone reproduction and checks, and mapped the results to the narration. No result was invented or copied from a fabricated chat transcript.

**What I understand now / still do not understand:** I can see that the seed changes the selected pseudorandom sequence, not the probability formula. I should avoid claiming universal cross-version determinism because Chapter 1 explicitly limits that promise.

**Evidence and next step:** `code/seed_demo.py`, `code/seed_output.txt`, `code/test_seed_demo.py`, and `FACTCHECK.md`. Next: render the mechanism and boundary clearly.

## 2026-09-26 — Improving voice, graphics, and claim boundary

**Date and what I was working on:** 2026-09-26, narration and visual production.

**I tried / expected:** I used the already installed free local Brutalist/Kokoro pipeline and aimed for the professor's clear figure language rather than decorative stock graphics.

**What happened:** Kokoro `af_bella` at speed `0.94` produced eight narration beats totaling about 3 minutes 13 seconds. The first complete render passed the runtime and media checks. A contact-sheet review showed that the mechanism, two-run comparison, controlled change, official test, and limitation were all legible.

**What I did:** I kept the synthetic-voice disclosure on screen, normalized audio to a consistent level, rendered original 1920×1080 motion graphics, generated captions, and ended with a two-column “establishes / does not establish” boundary.

**What Claude or another person contributed:** Codex generated the local narration, rendered and inspected the frames, and documented the technical checks. I supplied the preference for a clearer voice and professor-style templates through my review of the earlier project.

**What I understand now / still do not understand:** The final claim is defensible: the demonstrated seed makes the computational run repeatable in the recorded environment, but the sampler never receives the information needed to judge truth. I still need to complete the account-specific GitHub and Canvas upload myself.

**Evidence and next step:** Final MP4, SRT, `build/timeline.json`, `REVIEW.md`, and `CHECKS-REPORT.md`. Next: watch the MP4, choose which of the two assignments to submit, upload the matching folder, and paste its GitHub URL and remote commit hash into Canvas.
