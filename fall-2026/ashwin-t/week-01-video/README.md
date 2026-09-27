# Week 1 Explainer Video — [1000, 1000] → [0.5, 0.5]

**Ashwin Thankachan** · INFO 7375 Prompt Engineering for Generative AI · Northeastern · Fall 2026

**Concept:** "[1000, 1000] → [0.5, 0.5], and what the shared offset never carried"
(Chapter 1, Part 2). Softmax only sees the *gaps* between logits; a shared offset
is discarded, so you can't read confidence from how large a logit is.

**Why this one:** it's the smallest idea in the chapter that can be explained
completely in a few minutes, and it corrects a real misconception: that a big
score means a confident model.

**Runtime:** 2:38 (158.5 s) · 16:9 · narration is a synthetic Kokoro voice (`af_bella`)

**Video:** `w1-softmax-offset.mp4`, submitted on **Canvas only**. TA instruction (2026-09-27):
the mp4 goes to Canvas, all other files to GitHub. The root `.gitignore` also excludes video.

**GitHub location:** `fall-2026/ashwin-t/week-01-video/`. The course docs say
`fall-2025/`, but this section is Fall 2026 and the repo's term folder is
`fall-2026/` (confirmed by me, 2026-09-24).

## What's in this folder

| File | What it is |
|---|---|
| `w1-softmax-offset.mp4` | the rendered video (in the Canvas zip; not in the GitHub folder) |
| `beat_sheet.json` | the reviewed narration + visual plan (18 beats, measured durations) |
| `BUILD-PROMPT.md` | the prompts and exact commands that rebuild it |
| `SOURCES.md` | what I made, what Claude contributed, tools, licences |
| `FRICTIONAL.md` | dated log |
| `FACTCHECK.md` | every claim → its evidence |
| `QC-GATE-V.md`, `QC-GATE-T.md` | the toolkit's final visual-layout and typography checks (both pass) |
| `SHOTLIST.md`, `PROMPTS.md` | toolkit paperwork (Gate F) |
| `reference-output.txt`, `offset-output.txt`, `intermediates-output.txt` | the evidence: every on-screen number comes from these |
| `offset_evidence.py`, `intermediates_evidence.py` | scripts that print the evidence |
| `tools/` | beat-sheet builder, audio-cue sync, number verifier |
| `remotion/` | the custom Remotion component (`SoftmaxOffset.tsx.txt`) + the patch that registers it. Saved as `.tsx.txt` because the course validator rejects `.tsx` outside `learning-artifacts/`; rename to `.tsx` when copying into the Brutalist toolkit, where it compiles |

## Reprint the numbers (no toolkit needed)

From the course repository root. `main.py` was run, never edited.

```bash
python3 lessons/01-randomness-and-first-prompts/code/main.py      # = reference-output.txt
cd fall-2026/ashwin-t/week-01-video
python3 offset_evidence.py          # = offset-output.txt
python3 intermediates_evidence.py   # = intermediates-output.txt
python3 tools/verify_numbers.py     # every on-screen number traced to those files
```

## Rebuild the video

Needs the Brutalist toolkit at commit `6a8380a` with its setup done (Kokoro model,
Remotion `npm install`, ffmpeg); see `BUILD-PROMPT.md` for the full one-time setup.
Work on a copy so audio and clips aren't written into the course repo:

```bash
cp -R fall-2026/ashwin-t/week-01-video /tmp/w1 && cd /tmp/w1
TK=/path/to/brutalist.art && source $TK/.venv/bin/activate
cp remotion/SoftmaxOffset.tsx.txt $TK/runtime/remotion/src/scenes/SoftmaxOffset.tsx
git -C $TK apply "$PWD/remotion/Root.tsx.patch"
python3 tools/build_beat_sheet.py                         # numbers read from the .txt evidence
python3 $TK/runtime/scripts/generate_audio_kokoro.py .    # audio first: measured durations
python3 tools/sync_cues.py                                # animation cues from the audio
(cd $TK && ./art final /tmp/w1 --height 1080 --out /tmp/w1/final)
```

`./art final` renders every beat, runs Gate V (layout) and Gate T (typography), and
writes `final/w1-softmax-offset.mp4`.
