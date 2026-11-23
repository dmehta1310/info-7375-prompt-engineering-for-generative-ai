# SOURCES.md — ghost-job-radar-project-film

- Beat plan: project-film-plan/BEAT-PLAN.md (narration used word for word).
- Screenshots I took on 2026-11-21 (I opened all five sources myself and took every screenshot; copied to images/, originals untouched in project-film-plan/screenshots/):
  01 Entrepreneur (Greenhouse internal review: nearly 70% of companies posted at least one ghost job, Q2 2024);
  02 Resume Builder survey (40% of companies posted a fake job listing this year, 2024);
  03 GhostJob Chrome extension; 04 Subspace Ghost Job Scanner (Firefox); 05 MyVisaJobs, Stripe employer list.
- Beat 9 evidence: JS1 folder, evidence/reports/run_2026-10-28T024904Z_baseline.json (714 postings, 0 new) and run_2026-10-28T182823Z_follow-up.json (720 postings, 16 new), in ~/Documents/week01-video/info-7375-prompt-engineering-for-generative-ai/fall-2026/dhruvi-m/js1-contract-and-watch/.
- Toolkit: Brutalist, show-tell skill (brutalist.art, unchanged). Voice: Kokoro af_bella.
- Toolkit patches already in the shared checkout from the pitch film (ClaudeTitleOutro `handle` prop, etc.). No new toolkit edits for this film.

## What Claude did vs. what I did
**What I did (Dhruvi Mehta):**
- Wrote the beat plan's content decisions and approved it: the four parts, the narration, the pass marks and why.
- On Nov 21, 2026, opened all 5 sources myself (Entrepreneur, Resume Builder, GhostJob extension page, Subspace scanner page, MyVisaJobs Stripe) and took screenshots 01-05.
- Ran the Stripe watch on Oct 27-28 (JS1) and built the CPT check, sponsorship lookup and judges (JS1, JS2 assignments).
- Reviews the narration at GATE P and decides when to type PASS.

**What Claude (Claude Code) did:**
- Read BEAT-PLAN.md and the show-tell skill, and wrote make_sheet.py, which generates beat_sheet.json with the narration copied word for word (checked by script against BEAT-PLAN.md).
- Created the reel folder and wrote SOURCES.md, FACTCHECK.md, SHOTLIST.md, PROMPTS.md and PEDAGOGY.md.
- Checked the screenshots against the claims on screen, and the Stripe run counts against the JS1 run reports.
- Did not write or change any narration, and made no change to the shared toolkit.
- Next, once I approve at GATE P: generate audio, write the scenes, render, and check frames.

## Toolkit change by Claude Code
- Claude Code added an optional `showMascot` prop to brutalist.art's `runtime/remotion/src/scenes/ClaudeTitleOutro.tsx` (default true, so other reels are unchanged). The closing card here sets it false. Diff saved as `toolkit-patch-showmascot.diff` in this folder.
