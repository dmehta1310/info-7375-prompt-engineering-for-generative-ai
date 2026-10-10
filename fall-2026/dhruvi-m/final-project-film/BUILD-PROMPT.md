# BUILD-PROMPT.md — how to rebuild the Ghost-Job Trust Radar pitch film

Toolkit: Brutalist (show-tell skill), cloned 2026-10-10 into ~/Documents/final-project-film/brutalist.art. Built with Claude Code, run from ~/Documents/final-project-film/.
Planning files: plan/PROJECT-BRIEF.md and plan/BEAT-PLAN.md.

## Phase 1 prompt (Claude Code) — paperwork and beat sheet only, no audio, no render

```
Read these fully before writing anything:
- brutalist.art/skills/make/show-tell/SKILL.md, and every file it says it inherits from (ai-explainer laws, card family, reference/example-make_sheet.py, bookend rules)
- the worked example it names (structure only, do not copy its words)
- plan/BEAT-PLAN.md and plan/PROJECT-BRIEF.md

Then do Phase 1 only:
1. Create the reel folder where the skill expects it (<book>/youtube/<slug>), with the book "dhruvi" and the slug "ghost-job-radar-pitch". Tell me the full path.
2. Write make_sheet.py from the reference, and run it to produce beat_sheet.json. Use BEAT-PLAN.md's narration word for word and its pictures and labels. Use voice af_bella for every beat.
3. Apply the "Assignment overrides" in BEAT-PLAN.md. They take priority over the skill's defaults: no Liam, no Bear, no NikBearBrown, no claude-liam channel, no instructor portraits, and no Claude answer anywhere. If the toolkit rejects a non-instructor channel value, or a bookend component hard-codes an instructor name, STOP and tell me. Don't work around it silently.
4. Evidence for B06: find my Reallocation Engine scripts under ~/Documents/reallocation-dmehta1310-recipe (or ~/Documents/the-reallocation-engine) at scripts/contrib/2026fa/dmehta1310-ghost-job-radar/. Run their offline tests exactly as that README says, and save the raw output with today's date to <reel>/pantry/evidence/tests-YYYY-MM-DD.txt. Also run the break test (a company that isn't in the sample data) and save that output too. Use only those real lines in B06's data rows. Do not invent or tidy output. If a test fails or the count isn't 16, STOP and tell me.
5. Write SOURCES.md (merge in plan/SOURCES.md), FACTCHECK.md (| # | Beat | Claim | Verdict | Source | Fix | — every factual claim in the narration, with verdicts PASS, CORRECTED, or EXEMPT), SHOTLIST.md, and PROMPTS.md saying "no generation prompts".
6. Search the reel folder, case-insensitive, for: liam, bear, nikbearbrown, claude-liam, plugin, portal, hallo, photoelectric. Show me every hit.
7. Do NOT generate audio or render anything yet. End with a short report: reel path, any place where my plan breaks a show-tell law (label counts, card limits, card kinds), the test count you got, and the search results.
```

## Later phases
Added as they run: audio, stills, Gates A, B, V, and T, final render.

## Phase 1 fixes
Prompts I gave Claude Code after the Phase 1 run (verbatim, pasted blocks quoted), and the commands it ran.

### Prompt 1: how to handle the hard-coded outro handle (answer to its question)
~~~
Go with option 1, with a check first. Before building anything: (a) look at bookend_check.py and any gate that checks BOUT, and tell me whether a reel-local plain title card would make a gate refuse to render. (b) If it would, don't edit the shared toolkit. Instead, make a reel-local copy of the outro component inside our reel folder with the handle removed, and point our beat at it, if the toolkit allows that. (c) If neither works, stop and tell me exactly which gate blocks it and what the smallest toolkit patch would be. In every case, write a dated note to plan/FRICTIONAL.md explaining that the assignment bans the instructor's credit line, so the default outro was replaced. Then continue with the rest of Phase 1.
~~~
Then, after it reported that no gate blocks it but no reel-local Remotion component is possible:
~~~
Go with option 1: patch ClaudeTitleOutro.tsx with an optional handle prop that defaults to '@NikBearBrown', so other reels don't change. Show me the diff before applying it. After applying: (a) save the diff to our reel folder as toolkit-patch.diff; (b) set our BOUT handle to "Dhruvi Mehta"; (c) check that nothing in the outro or the audio script adds "At Nik Bear Brown" or any instructor name to the narration on its own; (d) add a dated FRICTIONAL.md entry saying the default outro hard-codes the instructor's handle, which the assignment bans, so I added a 2-line optional prop, with the diff saved in toolkit-patch.diff. Then continue with the rest of Phase 1 and give me the final report.
~~~

### Prompt 2: narration and label fixes
~~~
Apply these changes in make_sheet.py, regenerate beat_sheet.json, and update FACTCHECK.md and plan/BEAT-PLAN.md to match. Narration word for word:
BIDEA: "Hi, I'm Dhruvi Mehta, and this is my final project pitch: Ghost-Job Trust Radar. If something already ran, I'll show it. Everything else is a plan."
BDEFS: change the term "Sponsorship record" to "Sponsor record" on screen; narration unchanged.
B03: "I looked at two alternatives. MyVisaJobs shows who sponsored before, but nothing I saw checks whether a posting is live or fits a CPT window. The manual checklist from career guides works, but it's four or five steps across tabs, with no record kept."
B04: "Mine will check liveness first and stop if the posting is dead, before research starts. Every value will carry its source. If the data has nothing, it will say 'no record in this dataset,' never 'doesn't sponsor.'"
B06: label the derived row as "total" so it is clearly a sum, not a raw output line.
B09: "What's out: it won't tell anyone whether to apply, and it won't give legal or immigration advice. First, I'll make one command run every check on a synthetic posting. You'll know it ran because it writes a report, a test checks it, and a dated run log goes in the repo."
B11: "Why this project? It's a real problem for international students like me, and it's a mix: Python and data cleaning I already have, with last assignment's scripts as evidence. Prompt contracts and evaluation logs are new to me."
B12: "So, where things stand. Today: a recipe, two scripts, sixteen passing tests, and a break test, in an open pull request not yet reviewed. The single command, live check, and evaluation log come later. This film does not establish that the tool works on real postings."
BHTF: set the composer prompt to exactly "Before researching your next posting: is it still accepting applications, and does the start date fit your work window? Note where each answer came from." Narration: "Your turn." followed by that exact prompt, so it is read in full.
Leave the nikbearbrown repo URLs in SOURCES.md; they are source credit.
For the Kokoro licence, run `pip show kokoro-onnx` and check the model files in brutalist.art/runtime/models for a licence. Write only what you actually find, with where you found it.
Then re-check every narration line for present or past tense about things that don't exist yet, give me the new word count and estimated length, and add a dated FRICTIONAL.md entry for these fixes. Do not generate audio yet.
~~~

### Commands run (Phase 1 fixes)
~~~
git diff -- runtime/remotion/src/scenes/ClaudeTitleOutro.tsx > dhruvi/youtube/ghost-job-radar-pitch/toolkit-patch.diff   # run in brutalist.art
grep -n -i "nikbearbrown\|nik bear brown\|BOUT\|outro" runtime/scripts/generate_audio_kokoro.py
python3 scripts/contrib/2026fa/dmehta1310-ghost-job-radar/test_timeline_gate.py            # in ~/Documents/the-reallocation-engine
python3 scripts/contrib/2026fa/dmehta1310-ghost-job-radar/test_build_roles_json.py
python3 scripts/contrib/2026fa/dmehta1310-ghost-job-radar/build_roles_json.py --company "Zzyzx Quantum Analytics Corp" --title "Data Analyst" --role-id break-test-not-in-sample --liveness-result live --timeline-result pass --out course/2026fa/submissions/dmehta1310/runs/roles-break-test.json
python3 make_sheet.py
grep -rniE "liam|bear|nikbearbrown|claude-liam|plugin|portal|hallo|photoelectric" .
pip show kokoro-onnx ; head -5 .../kokoro_onnx-0.6.1.dist-info/licenses/LICENSE
~~~

## Phase 2
Prompts and commands, in order.

### Prompt 3: Phase 2
~~~
Phase 2, in order. Stop at each STOP.
1. Open WORKED-RUN.md in my Reallocation Engine repo and quote the lines that show I checked the output by hand against the raw CSV. If you can't find it, remove "I also checked one run by hand against the raw data." from B06 and tell me.
2. GATE P: write PEDAGOGY.md in the reel folder in the format the toolkit's examples use, then print every beat's narration in order for me to read. STOP and wait for me to type "PASS".
3. After I type PASS: add "VERDICT: PASS" signed "Dhruvi Mehta, <today's date>", then generate the audio with generate_audio_kokoro.py using af_bella, pad BOUT with a 1.0 s silent tail, write the ffprobe durations to actual_duration_s, and re-run make_sheet.py so audio_file and actual_duration_s carry forward.
4. Transcribe every beat's audio with faster-whisper (it's installed) and compare it to the script. List any beat where the words differ, and whether "Dhruvi Mehta", "CPT", "MyVisaJobs" and "Ghost-Job" come out right.
5. Report the total runtime. It must be under 4:00. STOP.
Also append every prompt I've given you since Phase 1, and the commands you ran, to plan/BUILD-PROMPT.md under "Phase 1 fixes" and "Phase 2", and add a dated FRICTIONAL.md entry. Do not run art run or art final.
~~~

### Prompt 4 and 5: review printouts
~~~
Print every beat's narration again, in order, one beat per line, with the beat name first.
~~~
~~~
Write every beat's narration, in order, to plan/NARRATION-REVIEW.md, one beat per paragraph with the beat name in bold. Then stop.
~~~

### Prompt 6: PASS and two fixes
~~~
PASS. Two small fixes first: in B02 change "Is there a public sponsorship record?" to "Is there a sponsorship record?", and in PEDAGOGY.md change the auditor model to Sonnet 5 (not Sonnet 5.5). Update FACTCHECK.md to match. Then continue with steps 3 to 5.
~~~

### Commands run (Phase 2)
~~~
find ~/Documents/the-reallocation-engine ~/Documents/reallocation-dmehta1310-recipe -iname "WORKED-RUN*"
cat -n .../course/2026fa/submissions/dmehta1310/WORKED-RUN.md
python3 make_sheet.py                      # after the B02 fix (also applied to BEAT-PLAN.md, NARRATION-REVIEW.md, PEDAGOGY.md, FACTCHECK.md)
printf '\nVERDICT: PASS\nDhruvi Mehta, 2026-10-10\n' >> PEDAGOGY.md
python3 runtime/scripts/generate_audio_kokoro.py <reel>     # run in brutalist.art; voice af_bella, 16 beats, $0.00
cp mp3/beat-BOUT.mp3 _superseded/beat-BOUT-unpadded.mp3
ffmpeg -y -loglevel error -i _superseded/beat-BOUT-unpadded.mp3 -af "apad=pad_dur=1.0" -c:a libmp3lame -q:a 2 mp3/beat-BOUT.mp3
ffprobe -v error -show_entries format=duration -of csv=p=0 mp3/beat-*.mp3
python3 make_sheet.py                      # now probes mp3/ and carries audio_file + actual_duration_s forward (and durationSeconds for BDEFS, B06, B12)
python3 _qc/whisper_check.py               # faster-whisper small.en, int8, CPU; writes _qc/whisper_transcripts.json
~~~

## Phase 3a
Stills only. No `art run`, no `art final`.

### Prompt 7: Phase 3a
~~~
Phase 3a: stills only. Follow show-tell SKILL.md steps 4 and 5 exactly.
1. Write scenes.py with one Manim scene per body beat (B01–B12, except the card beats B06 and B12), using the pictures and labels in plan/BEAT-PLAN.md. Follow every show-tell law: isometric drawings in the Claude palette, labels of 1–3 words and at most 3 per beat, DIM grey for big backing shapes, motion finished by 70% and type settled by 45% of each beat, at least one NEW shape per scene, and the text sizes that pass GATE T. Use the toolkit's approved props where they fit. B05 must show a visible "Constructed" tag.
2. B06's card rows must come only from pantry/evidence/tests-2026-10-10.txt, word for word, plus the "total (6 + 10)" row. Show "Real output · 2026-10-10" on the card.
3. Render each Manim scene's last frame at low quality (manim -ql -s), and render each card and bookend (BIDEA, BDEFS, B06, B12, BHTF, BOUT) with npx remotion still at 25%, 50% and 95% of its frames. Make one contact sheet PNG of everything, labeled by beat, and save it as plan/contact-sheet-3a.png.
4. Run the Gate A pre-audit from a scratch folder holding only scenes.py: static_scene_check.py and manim_layout_audit.py --curve-strict for every scene class. Report each result.
5. Check that every label and number sits fully inside the frame with a safe margin, and that no "Liam", "Bear" or "NikBearBrown" appears in any still.
STOP after that. Do not run art run or art final. Append this prompt and your commands to plan/BUILD-PROMPT.md under "Phase 3a", and add a dated FRICTIONAL.md entry.
~~~

### Commands run (Phase 3a)
~~~
# environment: the Anaconda python can't import manim (scipy built for numpy 1.x, numpy is 2.2.6). Isolated venv instead of upgrading scipy globally:
/opt/anaconda3/bin/python3 -m venv ~/Documents/final-project-film/.venv
~/Documents/final-project-film/.venv/bin/pip install -r brutalist.art/requirements.txt    # manim 0.18.1, numpy 2.5.4, scipy 1.18.1

# scenes.py = kit header (_qc/3a/scenes_head.py) + scenes (_qc/3a/scenes_body.py); ISO=(ox, oy, s) per scene is set by the fit script:
cat _qc/3a/scenes_head.py _qc/3a/scenes_body.py > scenes.py
.venv/bin/python _qc/3a/fit.py                    # computes and patches ISO for each scene so its drawing fills its FIT box

# Manim stills (last frame, low quality), one media dir per scene:
.venv/bin/manim -ql -s scenes.py <Class> --media_dir _qc/3a/media/<Class>     # via _qc/3a/render_manim_stills.sh

# Remotion stills at 25/50/95% (the toolkit's wrapper around remotion renderStill; writes _qc/preflight/):
python3 runtime/scripts/remotion_scenes.py <reel> --stills                    # run in brutalist.art

# contact sheet:
.venv/bin/python _qc/3a/contact_sheet.py                                      # -> plan/contact-sheet-3a.png

# Gate A pre-audit (scratch folder _qc/3a/gateA holds only scenes.py; layout audit also run in the reel folder):
python3 runtime/qc/static_scene_check.py scenes.py --class <Class>
.venv/bin/python runtime/qc/manim_layout_audit.py scenes.py --class <Class> --curve-strict
_qc/3a/gate_a.sh                                                              # all ten classes -> _qc/3a/gate_a_results.txt

# margins and banned names:
.venv/bin/python _qc/3a/bounds.py                                             # label/drawing margins to the +-6.2 x +-3.3 safe box
_qc/3a/ocr.sh                                                                 # tesseract on every still, then grep liam|bear|nikbearbrown|claude-liam|hallo|plugin|portal|photoelectric|humanitarians
~~~

## Phase 3a fixes and Phase 3b

### Prompt 8: Phase 3a fixes, then Phase 3b
~~~
Phase 3a fixes, then Phase 3b.
Fixes:
1. BIDEA: set the replacement to "live and CPT-feasible" (no commas), so the typed line becomes "Is this job live and CPT-feasible?". The narration stays the same.
2. Scale up the drawings in B01, B03, B07, B09 and B10 (and any other scene where the drawing covers less than about half the frame width), so each picture fills more of the frame while every label stays inside the safe margin. Re-run the Gate A pre-audit and the margin check after.
3. BHTF: add a visible "Constructed" tag like B05's. If the composer props allow it, remove the "Opus 5.5 · High" model label. Make the prompt text as large as GATE T allows.
4. B06: use a font where "OK" can't be misread as "0K" (for example a monospace font with a slashed or dotted zero), keeping the rows word for word from the evidence file.
Re-render the stills and save plan/contact-sheet-3a-v2.png.
Phase 3b: put .venv/bin first on PATH, then run ./brutalist.art/art run <reel> --height 2160 (Gates A, B, V and the review cut). From the review cut, extract one frame per beat at 50% of that beat's time with ffmpeg, and save a contact sheet as plan/contact-sheet-3b.png. Report each gate's result, and do not submit over any failure. Do NOT run art final. Append the prompts and commands to plan/BUILD-PROMPT.md, including the .venv setup, and add a dated FRICTIONAL.md entry.
~~~

### Commands run (Phase 3a fixes)
~~~
# .venv setup (made in Phase 3a; needed because the Anaconda python can't import manim)
/opt/anaconda3/bin/python3 -m venv ~/Documents/final-project-film/.venv
~/Documents/final-project-film/.venv/bin/pip install -r brutalist.art/requirements.txt
export PATH="$HOME/Documents/final-project-film/.venv/bin:$PATH"       # every art run / art final shell must do this first

# make_sheet.py edits: BIDEA replacementWords "live and CPT-feasible"; BHTF tag "Constructed", modelLabel "", effortLabel "", largeText true; B06 valueFont "Helvetica Neue, Arial, sans-serif"
python3 make_sheet.py

# toolkit patches (all additive, default behaviour unchanged; diffs saved in the reel folder):
#   toolkit-patch-2.diff  ShowTellCard.tsx: optional valueFont prop (focus card value column)
#   toolkit-patch-3.diff  ClaudeComposerAsk.tsx: optional tag prop (corner pennant + word)
git diff -- runtime/remotion/src/scenes/ShowTellCard.tsx > .../toolkit-patch-2.diff
git diff -- runtime/remotion/src/scenes/ClaudeComposerAsk.tsx > .../toolkit-patch-3.diff

# scenes.py layouts changed in _qc/3a/scenes_body.py (B01, B03, B05, B07, B09, B10 re-laid out; B02/B04 shortened; fit box widened to +-5.8 x -1.8..2.9; SMAX 1.7)
cat _qc/3a/scenes_head.py _qc/3a/scenes_body.py > scenes.py
.venv/bin/python _qc/3a/fit.py
_qc/3a/render_manim_stills.sh
python3 runtime/scripts/remotion_scenes.py <reel> --stills                 # run in brutalist.art
.venv/bin/python _qc/3a/contact_sheet.py contact-sheet-3a-v2.png
_qc/3a/gate_a.sh ; .venv/bin/python _qc/3a/bounds.py ; _qc/3a/ocr.sh
~~~

### Commands run (Phase 3b)
~~~
cd ~/Documents/final-project-film
export PATH="$HOME/Documents/final-project-film/.venv/bin:$PATH"
./brutalist.art/art run dhruvi/youtube/ghost-job-radar-pitch --height 2160 > dhruvi/youtube/ghost-job-radar-pitch/_qc/3b/art_run.log 2>&1
# gates reported by the run (all in _qc/3b/art_run.log): L clean, SHAPE skipped (not a finance reel), A 10/10 clean, W 10/10 clean, B 10/10 CLEAN, V frames=32 BLOCKER=0 MAJOR=0
# review cut: dhruvi/youtube/ghost-job-radar-pitch/ghost-job-radar-pitch-slate.mp4 (3840x2160, 24 fps, 215.83 s)
.venv/bin/python _qc/3b/contact_sheet_3b.py        # ffmpeg -ss <start + render_duration_s/2> -i <cut> -frames:v 1 for each beat -> plan/contact-sheet-3b.png
~~~

## Phase 4
Final master and submission folder.

### Prompt 9: Phase 4
~~~
Phase 4: final master and submission folder.
1. With .venv/bin first on PATH, run ./brutalist.art/art final <reel> --height 2160 --out <reel>/exports/landscape (GATE T, then the master). Report GATE T's result. If it fails, fix and re-run; never package over a failure. Check the master: 3840×2160, the 1.0 s silent tail, its sha256, and its file size.
2. GitHub blocks files over 100 MB. If the master is over 95 MB, make one high-quality H.264 re-encode under 95 MB and use that SAME file in both the Canvas zip and GitHub, so they match. Note this in FRICTIONAL.md.
3. Build the submission folder at ~/Documents/final-project-film/submission/final-project-film/ containing: README.md (my name, working title "Ghost-Job Trust Radar", target role Data Analyst, the runtime, and step-by-step rebuild instructions including the .venv setup and applying the three toolkit patches), the .mp4, PROJECT-BRIEF.md, beat_sheet.json, BUILD-PROMPT.md, SOURCES.md, FRICTIONAL.md, a gate-reports/ folder with every gate report and QC log the toolkit produced, plus FACTCHECK.md, SHOTLIST.md, PROMPTS.md, PEDAGOGY.md, make_sheet.py, scenes.py, toolkit-patch.diff, toolkit-patch-2.diff, toolkit-patch-3.diff, and pantry/evidence/.
4. SOURCES.md must list what Claude contributed, with dates: Claude chat (planning, brief, beat plan, review) and Claude Code (make_sheet.py, scenes.py, the three toolkit patches, running my tests, audio, renders, packaging). Include the Kokoro licence exactly as found.
5. Final scan of the submission folder: search for "[CONFIRM", "[Add", "[DATE", "TBD", "TODO", "Liam", "Bear", "Photoelectric", and any leftover placeholder text, and fix every hit except the honest repo URLs and the patch diffs. Make sure there are no caches, .venv, node_modules, credentials, or private data, and no conversation transcripts.
6. Make the zip at ~/Documents/final-project-film/submission/Mehta_Dhruvi_INFO7375_FinalProjectFilm.zip.
7. Find my local clone of the course repo (where fall-2026/dhruvi-m/week-01-video/ lives), and tell me its path and current branch. Do NOT copy, commit, or push anything to GitHub yet. STOP and report.
Append this prompt and your commands to BUILD-PROMPT.md, and add dated FRICTIONAL.md entries.
~~~

Also during Phase 4 (verbatim): "While art final runs, edit plan/PROJECT-BRIEF.md (text only, nothing else)": three edits to sections 1, 2 and 4 (sponsorship record "in the dataset"; "What mine will do that they don't" paragraph; source-grounding bullet), then a tense re-check of the whole brief, and "Use this version when you package."

### Commands run (Phase 4)
~~~
cd ~/Documents/final-project-film
export PATH="$HOME/Documents/final-project-film/.venv/bin:$PATH"
./brutalist.art/art final dhruvi/youtube/ghost-job-radar-pitch --height 2160 --out dhruvi/youtube/ghost-job-radar-pitch/exports/landscape
#   attempt 1: GATE T FAIL (BDEFS 40px text run under the 41px floor; B05 ink-outlined README page inside the desk outline read as overlapping text)
#   fixes: B05 page/laptop outlines to deep kraft in scenes.py; BDEFS footer label set to empty; then
mv manim/B05.mp4 media/BDEFS.mp4 media/videos _superseded/phase4/        # old clips and the Manim cache, so art run re-renders them
python3 make_sheet.py
./brutalist.art/art run <reel> --height 2160 && ./brutalist.art/art final <reel> --height 2160 --out <reel>/exports/landscape
#   attempt 2: GATE T FAIL (BDEFS still 40px: the lowercase meaning text at the component's fixed 48px has a 40px x-height at 4K)
#   fix: toolkit-patch-4.diff (ClaudeDefinitions meaningSize prop, default 48), BDEFS meaningSize 54 in make_sheet.py, then
python3 make_sheet.py
python3 brutalist.art/runtime/scripts/remotion_scenes.py <reel> --only BDEFS --force
.venv/bin/python <check_min_size on the BDEFS 50% frame>                        # PASS, 45px >= 41px
./brutalist.art/art run <reel> --height 2160 && ./brutalist.art/art final <reel> --height 2160 --out <reel>/exports/landscape
#   attempt 3: GATE T PASS (0 FAILs, 16 beats)

# master check
ffprobe -v error -show_entries stream=codec_name,codec_type,width,height,r_frame_rate,pix_fmt,duration -of compact exports/landscape/ghost-job-radar-pitch.mp4
shasum -a 256 exports/landscape/ghost-job-radar-pitch.mp4
ffmpeg -i exports/landscape/ghost-job-radar-pitch.mp4 -af silencedetect=n=-50dB:d=0.5 -f null -

# submission folder (see README.md in it for the rebuild steps)
mkdir -p ~/Documents/final-project-film/submission/final-project-film/{gate-reports,pantry/evidence}
cp (the files listed in step 3, plus toolkit-patch-4.diff) into it; redact the instructor persona names in the BUILD-PROMPT.md and FRICTIONAL.md copies
grep -rniE "\[CONFIRM|\[Add|\[DATE|TBD|TODO|Liam|Bear|Photoelectric" ~/Documents/final-project-film/submission/final-project-film
find ... -name ".venv" -o -name "node_modules" -o -name "__pycache__" -o -name ".DS_Store" -o -name ".env*"    # none expected
cd ~/Documents/final-project-film/submission && zip -r -X Mehta_Dhruvi_INFO7375_FinalProjectFilm.zip final-project-film -x "*.DS_Store"
unzip -l Mehta_Dhruvi_INFO7375_FinalProjectFilm.zip
# course repo clone (read-only)
find ~ -maxdepth 6 -type d -path "*fall-2026/dhruvi-m/week-01-video"
git -C <clone> rev-parse --abbrev-ref HEAD
~~~

## Phase 5
Fix, then GitHub.

### Prompt 10: Phase 5
~~~
Phase 5: fix, then GitHub.
1. In the submission copies of BUILD-PROMPT.md and FRICTIONAL.md, restore the exact original wording from plan/ (remove the redaction and its note). The instructor names there only record my overrides, which is evidence, not persona use. Re-make the zip, re-test it, and confirm the folder and zip contents are identical (diff -r against the extracted zip).
2. In ~/Documents/week01-video/info-7375-prompt-engineering-for-generative-ai: run git pull, then check whether .gitignore would ignore .mp4 or any file in our folder (git check-ignore). If anything would be ignored, STOP and tell me.
3. Copy the submission folder's contents into fall-2026/dhruvi-m/final-project-film/ there. Run git status, and confirm the only changes are inside that folder.
4. Show me the exact git add, commit and push commands, then STOP and wait for me to type "PUSH".
Add a dated FRICTIONAL.md line for this step (inside the submission folder and the GitHub copy, so they still match), and append the commands to BUILD-PROMPT.md.
~~~

### Commands run (Phase 5)
~~~
cp plan/BUILD-PROMPT.md plan/FRICTIONAL.md submission/final-project-film/        # exact originals, no redaction
cd submission && rm -f Mehta_Dhruvi_INFO7375_FinalProjectFilm.zip
zip -r -X -q Mehta_Dhruvi_INFO7375_FinalProjectFilm.zip final-project-film -x "*.DS_Store"
unzip -tq Mehta_Dhruvi_INFO7375_FinalProjectFilm.zip
T=$(mktemp -d) && unzip -q Mehta_Dhruvi_INFO7375_FinalProjectFilm.zip -d $T && diff -r final-project-film $T/final-project-film

cd ~/Documents/week01-video/info-7375-prompt-engineering-for-generative-ai
git pull                                          # Already up to date (main at a7faf71)
git check-ignore -v --stdin < <(every file path under fall-2026/dhruvi-m/final-project-film/)
#   result: ONE file ignored: ghost-job-radar-pitch.mp4, by .gitignore line 33 "*.[mM][pP]4"; the other 41 files are not ignored.
#   Per the prompt: STOPPED here. Steps 3 and 4 (copy, git status, add/commit/push) have not been run.
~~~

### Prompt 11: Option 1 for the ignored mp4, then steps 3 and 4
~~~
Option 1: force-add only ghost-job-radar-pitch.mp4 with git add -f; don't touch .gitignore. Add a dated FRICTIONAL.md note: the repo's .gitignore excludes *.mp4, but the assignment requires the film in the GitHub folder to match Canvas, so I force-added only my own file (16.9 MB), and other students' mp4s are already tracked. Then do steps 3 and 4: re-make the zip so the folder, zip and GitHub copy all match, copy the folder in, run git status, confirm the only changes are inside fall-2026/dhruvi-m/final-project-film/, and show me the exact git add, commit and push commands. STOP and wait for "PUSH".
~~~

### Commands run (Phase 5, continued)
~~~
cp plan/BUILD-PROMPT.md plan/FRICTIONAL.md submission/final-project-film/
cd submission && rm -f Mehta_Dhruvi_INFO7375_FinalProjectFilm.zip && zip -r -X -q Mehta_Dhruvi_INFO7375_FinalProjectFilm.zip final-project-film -x "*.DS_Store"
unzip -tq Mehta_Dhruvi_INFO7375_FinalProjectFilm.zip ; diff -r final-project-film <extracted zip>/final-project-film

C=~/Documents/week01-video/info-7375-prompt-engineering-for-generative-ai
mkdir -p $C/fall-2026/dhruvi-m/final-project-film
cp -R submission/final-project-film/. $C/fall-2026/dhruvi-m/final-project-film/
diff -r submission/final-project-film $C/fall-2026/dhruvi-m/final-project-film
cd $C && git status --short --branch ; git status --short --ignored | grep final-project-film
git add -n -f fall-2026/dhruvi-m/final-project-film/ghost-job-radar-pitch.mp4 ; git add -n fall-2026/dhruvi-m/final-project-film     # dry runs only

# NOT yet run: to be run only after "PUSH" (the exact commands are shown in the reply that follows this prompt)
#   git add -f fall-2026/dhruvi-m/final-project-film/ghost-job-radar-pitch.mp4
#   git add fall-2026/dhruvi-m/final-project-film
#   git commit -m "Add Dhruvi Mehta final project film: Ghost-Job Trust Radar (INFO7375)"
#   git push origin main
~~~
