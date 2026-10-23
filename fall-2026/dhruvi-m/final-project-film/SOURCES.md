# SOURCES.md

## What I used
- Brutalist toolkit, show-tell skill (https://github.com/nikbearbrown/brutalist.art), commit b21f6253a336098f3f55847a9525ae6868ccbdb7, cloned 2026-10-10. Voice: Kokoro af_bella, run locally. Rendering: Manim 0.18.1, Remotion, ffmpeg 9.0.2, Node 26.9.0, Python 3.12.
- My own Reallocation Engine work: fork of nikbearbrown/the-reallocation-engine, PR #1, branch contrib/2026fa-dmehta1310-ghost-job-radar. Scripts at scripts/contrib/2026fa/dmehta1310-ghost-job-radar/ (README, timeline_gate.py, build_roles_json.py, two test files). My WORKED-RUN.md in that repo documents the hand check against the raw CSV (grep "AVY INC").
- Course sample data used in that work: 80 Days to Stay sponsorship/funding sample CSV (data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv, 30,370 lines).
- Alternatives reviewed on 2026-10-10: MyVisaJobs (myvisajobs.com), and the manual sponsor-check process described in F1Jobs career guides (f1jobs.io).
- Claude did that first research with web search on 2026-10-10. I opened MyVisaJobs, the Stripe posting and the Greenhouse API myself on 2026-10-22. My screenshots (browser bar cropped) are in evidence/2026-10-22-my-checks/, and my notes are in FRICTIONAL.md.
- PROJECT-BRIEF.md (in this folder): the film's source text.
- faster-whisper (small.en), used only to check the generated narration against the script.

## Real evidence captured for this film (raw, unedited)
- pantry/evidence/tests-2026-10-10.txt: both offline test suites, run 2026-10-10 from the repo root exactly as the scripts' README says. 6 tests + 10 tests = 16, all OK.
- pantry/evidence/break-test-2026-10-10.txt: build_roles_json.py run on "Zzyzx Quantum Analytics Corp", a company not in the CSV (checked with grep). Output: sponsorship tier NoRecordInSample, company_found_in_sample false.
- The tests were run in the git-tracked checkout of my fork. A second copy of the same scripts had identical file sizes for all five files.

## What I made
- Everything in my Reallocation Engine PR (recipe, card, timeline_gate.py, build_roles_json.py, tests).
- The project idea and the final decisions in the brief.
- B06 uses the real test output above; B07's drawing shows the real break-test result. No screenshots are used.

## What Claude contributed
All dates are 2026-10-10, the date recorded in FRICTIONAL.md for each piece of work.
- **Claude (claude.ai chat), 2026-10-10:** planning, drafting PROJECT-BRIEF.md and the beat plan from my existing work, researching the alternatives with web search, and reviewing drafts. I reviewed and edited all of it.

- 2026-10-22: Claude (chat) helped me with a fill-in template and finding the facts in my screenshots. The checks and decisions are mine.

- **Claude Code, 2026-10-10:**
  - wrote make_sheet.py (which generates beat_sheet.json) from the beat plan, and scenes.py (the ten Manim scenes);
  - wrote FACTCHECK.md, SHOTLIST.md, PROMPTS.md and PEDAGOGY.md;
  - made four small additive patches to the shared toolkit, each leaving its default behaviour unchanged, with the diffs in this folder:
    1. `toolkit-patch.diff`: ClaudeTitleOutro.tsx, an optional `handle` prop (the default outro hard-coded the instructor's handle, which the assignment bans);
    2. `toolkit-patch-2.diff`: ShowTellCard.tsx, an optional `valueFont` prop (so "OK" is not misread as "0K" on the B06 card);
    3. `toolkit-patch-3.diff`: ClaudeComposerAsk.tsx, an optional `tag` prop (the "Constructed" tag on the Your Turn beat);
    4. `toolkit-patch-4.diff`: ClaudeDefinitions.tsx, an optional `meaningSize` prop (GATE T measured the default meaning text 1 px under its size floor);
  - ran my offline tests and the break test and saved their raw output;
  - generated the narration audio (Kokoro af_bella), padded the outro with a 1.0 s silent tail, and checked every beat against the script with faster-whisper;
  - ran the renders (`art run`, then `art final`), diagnosed and fixed the GATE T failures, and checked the master;
  - assembled this submission folder and the zip.

## Third-party assets
- Kokoro TTS voice model (af_bella), as shipped with the Brutalist toolkit (runtime/models/kokoro/kokoro-v1.0.onnx and voices-v1.0.bin).
- The `kokoro-onnx` Python package, version 0.6.1. `pip show kokoro-onnx` shows an empty License field, but the package's own LICENSE file (kokoro_onnx-0.6.1.dist-info/licenses/LICENSE, in site-packages) reads, exactly:

```
MIT License

Copyright (c) 2025 github.com/thewh1teagle

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- No licence file ships alongside the model weights in the toolkit's runtime/models/kokoro/ folder, so the licence of the model weights themselves is not confirmed from anything on this machine.
- No other third-party images, music, or footage.

- 2026-10-22 revision: Claude (chat) drafted the revised narration, which I read and approved, and wrote apply_2026-10-22.py and finish_2026-10-22.py. I ran every command myself, listened to the new audio, and watched the new cut.
