# Ghost-Job Trust Radar: final project pitch film

| | |
|---|---|
| **Name** | Dhruvi Mehta |
| **Course** | INFO7375, Final Project Pitch |
| **Working title** | Ghost-Job Trust Radar |
| **Target role** | Data Analyst |
| **Runtime** | 3:35.8 (215.83 s) |
| **Master** | `ghost-job-radar-pitch.mp4`: 3840×2160, 24 fps, H.264 video + AAC audio, 16,895,050 bytes (16.9 MB), ends with a silent tail of 1.09 s (1.0 s padding) |
| **SHA-256** | `912b2de2096f8358acbd4f5f4a9f0872bc378f2341942eb5afb67a5db6b9399c` |

## What this is
A 3.5-minute pitch for a tool that does not exist yet: a command-line tool that checks a job posting (is it still live, does its start date fit a CPT work window, is there a sponsorship record in the dataset) before an international student on CPT spends time researching it.

The film follows one rule, stated in its first line: if something already ran, it is shown; everything else is a plan. Two beats are real. B06 shows the real output of my 16 offline tests (6 + 10, run 2026-10-10), and B07 shows the real result of my break test on a company that is not in the sample data. Every other drawing is a constructed illustration, and the film says so on screen where a picture could be mistaken for real. Beat B12 states what the film does not establish: that the tool works on real-world postings.

The narration is a Kokoro text-to-speech voice (`af_bella`) reading my script; no Claude response is shown anywhere in the film.

## What is in this folder
| Item | What it is |
|---|---|
| `ghost-job-radar-pitch.mp4` | The final master (checked: 3840×2160, silent tail of 1.09 s). |
| `PROJECT-BRIEF.md` | The project brief the film is built from. |
| `beat_sheet.json` | The finished, build-stamped beat sheet: narration, voice, on-screen props, measured audio durations. |
| `make_sheet.py` | Generates `beat_sheet.json`. All narration and card/bookend props live here. |
| `scenes.py` | The ten Manim scenes (isometric drawings), one per drawn beat. |
| `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`, `PEDAGOGY.md` | Paperwork the toolkit requires: every claim with its source and verdict, the shot list (REAL vs constructed, and why each card is a card), "no generation prompts", and the signed narration review. |
| `SOURCES.md` | Everything I used, what I made, and what Claude contributed (with dates), including the Kokoro licence. |
| `BUILD-PROMPT.md` | Every prompt I gave Claude Code, in order, and the commands it ran. |
| `FRICTIONAL.md` | Dated log of what went wrong and what I changed. |
| `toolkit-patch.diff`, `toolkit-patch-2.diff`, `toolkit-patch-3.diff`, `toolkit-patch-4.diff` | The four small changes I made to the shared video toolkit (see below). |
| `pantry/evidence/` | The raw, dated output of my tests and break test, used word for word in B06 and B07. |
| `gate-reports/` | Every gate report and QC log the toolkit produced (index below). |

## Results of the toolkit's gates
| Gate | Result |
|---|---|
| L (beat-mix lint) | clean |
| SHAPE | skipped (not a finance reel) |
| A (static pre-flight) | 10 of 10 scenes clean |
| W (WCAG contrast, margins, text overlap) | 10 of 10 clean |
| B (pixel layout audit at 4K) | 10 of 10 clean |
| V (frame-level visual QC) | 32 frames, 0 blockers, 0 major defects |
| T (type lock, run by `art final`) | **PASS** on the third attempt (0 fails, 16 beats). Attempts 1 and 2 failed and are logged in `gate-reports/`; see `FRICTIONAL.md` for the causes and fixes. |

One advisory remains and is expected: the toolkit's "cold open law" note that the opening beat is the hesitant-writer animation rather than the composer.

## How to rebuild the film
Tested on macOS (Darwin 25.5) with Python 3.12.7, Node v26.9.0, ffmpeg 9.0.2 and git. Remotion downloads its own headless Chrome on first use.

**1. Workspace and toolkit**
```bash
mkdir -p ~/Documents/final-project-film && cd ~/Documents/final-project-film
git clone https://github.com/nikbearbrown/brutalist.art
git -C brutalist.art checkout b21f6253a336098f3f55847a9525ae6868ccbdb7   # the commit I used (on origin/main)
```

**2. Toolkit setup** (installs the Remotion packages and the Kokoro voice model)
```bash
cd brutalist.art && ./setup --install && cd ..
```
The setup's ElevenLabs check flags files inside the toolkit's own example reels and stops before it prints its readiness table. I use none of those files; check the tools directly instead (`ffmpeg -version`, `node --version`, `python3 --version`).

**3. A Python environment where Manim imports** (the `.venv` setup)
```bash
python3 -m venv .venv
.venv/bin/pip install -r brutalist.art/requirements.txt          # manim 0.18.1, numpy, scipy, kokoro-onnx, faster-whisper, ...
export PATH="$PWD/.venv/bin:$PATH"                              # repeat in every shell that runs art run / art final
python3 -c "import manim; print(manim.__version__)"            # expect 0.18.1
```
I needed this because the Anaconda Python on my machine could not import Manim (a numpy 2 / scipy mismatch). If `import manim` already works for you, you can skip the venv, but the `PATH` line is what makes `art run` find the right `manim`, `python3` and `ffmpeg`.

**4. Apply the four toolkit patches** (each is additive: with no new prop set, every other reel renders exactly as before)
```bash
cd brutalist.art
for p in toolkit-patch toolkit-patch-2 toolkit-patch-3 toolkit-patch-4; do
  git apply --check <path-to-this-folder>/$p.diff && git apply <path-to-this-folder>/$p.diff
done
cd ..
```
| Patch | File | Change | Why |
|---|---|---|---|
| `toolkit-patch.diff` | `ClaudeTitleOutro.tsx` | optional `handle` prop (default unchanged) | the default outro hard-codes the instructor's handle, which the assignment bans |
| `toolkit-patch-2.diff` | `ShowTellCard.tsx` | optional `valueFont` prop | so "OK" on the B06 card cannot be misread as "0K" |
| `toolkit-patch-3.diff` | `ClaudeComposerAsk.tsx` | optional `tag` prop | the "Constructed" tag on the Your Turn beat |
| `toolkit-patch-4.diff` | `ClaudeDefinitions.tsx` | optional `meaningSize` prop | GATE T measured the default meaning text 1 px under its size floor |

My earlier notes said "three patches"; there are four because the fourth was added after GATE T failed on the terms card.

**5. Create the reel folder**
```bash
mkdir -p dhruvi/youtube/ghost-job-radar-pitch/pantry/evidence
cp make_sheet.py scenes.py SOURCES.md FACTCHECK.md SHOTLIST.md PROMPTS.md PEDAGOGY.md dhruvi/youtube/ghost-job-radar-pitch/
cp pantry/evidence/* dhruvi/youtube/ghost-job-radar-pitch/pantry/evidence/
cd dhruvi/youtube/ghost-job-radar-pitch
```
(`beat_sheet.json` in this folder is the finished sheet. Step 6 regenerates it; do not copy it in.)

**6. Generate the beat sheet**
```bash
python3 make_sheet.py
```

**7. Generate the audio, pad the outro, and re-run the sheet so it carries the measured durations**
```bash
python3 ../../../brutalist.art/runtime/scripts/generate_audio_kokoro.py .      # voice af_bella, writes mp3/beat-*.mp3
mkdir -p _superseded && cp mp3/beat-BOUT.mp3 _superseded/beat-BOUT-unpadded.mp3
ffmpeg -y -i _superseded/beat-BOUT-unpadded.mp3 -af "apad=pad_dur=1.0" -c:a libmp3lame -q:a 2 mp3/beat-BOUT.mp3
python3 make_sheet.py        # now reads mp3/ with ffprobe and writes audio_file and actual_duration_s
```
Optional: `gate-reports/audio_whisper_check.py` (copy it into a `_qc/` folder in the reel) transcribes every beat with faster-whisper and compares it to the script.

**8. Render the review cut, then the master**
```bash
cd ~/Documents/final-project-film
export PATH="$PWD/.venv/bin:$PATH"
./brutalist.art/art run   dhruvi/youtube/ghost-job-radar-pitch --height 2160
./brutalist.art/art final dhruvi/youtube/ghost-job-radar-pitch --height 2160 --out dhruvi/youtube/ghost-job-radar-pitch/exports/landscape
```
`art run` renders the Manim and Remotion clips at 4K, runs gates A, B, W and V, and writes the review cut (`ghost-job-radar-pitch-slate.mp4`, with beat labels burned in). `art final` runs GATE T and, only if it passes, writes the clean master. On my machine the first full `art run` took roughly 25 minutes and each `art final` attempt roughly 10 (approximate figures). Do not re-run `make_sheet.py` after `art final`: it wipes the build stamps. Nothing here publishes anything.

Renders are not guaranteed to be byte-identical on another machine, so a rebuilt master may have a different SHA-256 from the one above.

**9. Regenerate the evidence (optional)** from my fork of the course Reallocation Engine repo, branch `contrib/2026fa-dmehta1310-ghost-job-radar`, from the repo root:
```bash
python3 scripts/contrib/2026fa/dmehta1310-ghost-job-radar/test_timeline_gate.py
python3 scripts/contrib/2026fa/dmehta1310-ghost-job-radar/test_build_roles_json.py
python3 scripts/contrib/2026fa/dmehta1310-ghost-job-radar/build_roles_json.py --company "Zzyzx Quantum Analytics Corp" --title "Data Analyst" --role-id break-test-not-in-sample --liveness-result live --timeline-result pass --out course/2026fa/submissions/dmehta1310/runs/roles-break-test.json
```
Expected: 6 tests OK, 10 tests OK, and a `NoRecordInSample` result for the break test.

## Index of `gate-reports/`
| File | What it is |
|---|---|
| `gate-T_TYPECHECK_final-PASS.md` | GATE T report from the passing run. |
| `art-final_attempt-1_GATE-T-FAIL.log`, `art-final_attempt-2_GATE-T-FAIL.log`, `art-final_attempt-3_GATE-T-PASS.log` | The three `art final` runs. |
| `gate-V_REPORT.md` | Gate V: 32 frames, 0 blockers, 0 major. |
| `gate-B_layout_audit_last-scene.md/.json` | Gate B's report file for the last scene it audited; the per-scene results for all ten scenes are in the `art-run` logs. |
| `art-run_1_first-full-render_all-gates.log` | First complete `art run`: gates L, SHAPE, A, W, B, V, and every render. |
| `art-run_2_after-B05-and-BDEFS-fixes.log`, `art-run_3.log` | The two later `art run`s. |
| `master_verified.json` | The toolkit's verification record for the master (SHA-256, duration, input hashes). |
| `beat-fill-status_STATUS.md` | All 16 beats filled, none left as slates. |
| `qc-sheet_art-run.png`, `qc-contact-sheet_art-final.png` | The toolkit's QC contact sheets. |
| `remotion-stills-preflight_receipt.json` | Receipt for the 25/50/95% stills of the Remotion beats. |
| `gate-A_*.txt`, `margins_*.txt` | My Gate A pre-audit runs (static check and layout audit with `--curve-strict`) and the label and drawing margin check. |
| `audio_whisper-transcripts.json`, `audio_whisper_check.py` | Transcripts of every narration beat and the script that compares them to the text. |
| `contact-sheet-3a-v2_stills.png`, `contact-sheet-3b_review-cut.png` | Contact sheets of the stills and of the review cut at 50% of each beat. |
