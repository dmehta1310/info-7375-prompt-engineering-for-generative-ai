# BUILD-PROMPT — how this video was built, and how to rebuild it

## 1. The prompts

The build was driven from Claude Code, starting with my build brief (concept,
approved narration, hard constraints: free pipeline, no LaTeX, no invented numbers,
no fabricated Claude output, one concept). The decisions made in that session:

1. *"Read the toolkit README/CLAUDE.md and schema; report the commands, the
   beat_sheet fields, and the non-LaTeX components; confirm the evidence files; list
   what the toolkit can't do as specified."*
2. Approved installs: ffmpeg (Homebrew, global); venv, `npm install`, Kokoro model
   (local to the toolkit folder). Python 3.13 used instead of 3.12 (Kokoro supports <3.14).
3. Approved narration edits: Beat 1 "probabilities"; Beat 3 "here's why" →
   *"Here's why. Softmax divides each score's exponential by the total. Adding a
   thousand multiplies every exponential by the same factor, on top and on the bottom,
   so it cancels. And because this code subtracts the largest score first, both runs
   compute the exact same intermediate numbers. That's why every digit matches."*
4. Voice: Kokoro `af_bella`.
5. Build location: `~/Desktop/CSYE7375/`.
6. After watching draft 1 (my notes: no clue what softmax is; start and end abrupt):
   add B00 question, define softmax in B01B, add B06 recap. Fix Gate V underfill.
7. Palette: one consistent cream palette (B05 no longer dark). Skipped an extra
   "softmax arithmetic" beat to stay on one concept.
8. Final: accessible accent #A84A28 (Gate T contrast); no em dashes in narration or on
   screen (B01D, B03B, B03D, B04C re-voiced).

## 2. Layout expected by the commands

```
CSYE7375/
├── brutalist.art/                      toolkit @ 6a8380ae…  (+ .venv, node_modules, model)
├── info-7375-prompt-engineering-for-generative-ai/   course repo @ e6c6c49d…
├── w1-evidence/                        *.py + *.txt evidence
└── w1-video/                           this folder
```

## 3. Commands (from `CSYE7375/`)

```bash
# 0. one-time setup
git clone https://github.com/nikbearbrown/brutalist.art
git -C brutalist.art checkout 6a8380ae169cca81e0633664a65c958f5c12ab4b
git clone https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai
brew install ffmpeg
python3.13 -m venv brutalist.art/.venv && source brutalist.art/.venv/bin/activate
pip install "kokoro-onnx>=0.4" "mutagen>=1.47,<1.48" "Pillow>=10.2,<11" "numpy>=2.0.2" scipy
(cd brutalist.art/runtime/remotion && npm install)
mkdir -p brutalist.art/runtime/models/kokoro && cd brutalist.art/runtime/models/kokoro
curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
cd ../../../..

# 1. install the custom component into the toolkit
# stored as .tsx.txt (the course validator rejects .tsx here); rename back on copy
cp w1-video/remotion/SoftmaxOffset.tsx.txt brutalist.art/runtime/remotion/src/scenes/SoftmaxOffset.tsx
git -C brutalist.art apply ../w1-video/remotion/Root.tsx.patch

# 2. evidence
(cd info-7375-prompt-engineering-for-generative-ai && python3.13 lessons/01-randomness-and-first-prompts/code/main.py) > w1-evidence/reference-output.txt
python3.13 w1-evidence/offset_evidence.py        > w1-evidence/offset-output.txt
python3.13 w1-evidence/intermediates_evidence.py > w1-evidence/intermediates-output.txt

# 3. beat sheet (numbers are read from the evidence files), then audio = the clock
python3.13 w1-video/tools/build_beat_sheet.py
python brutalist.art/runtime/scripts/generate_audio_kokoro.py w1-video
python3.13 w1-video/tools/sync_cues.py           # cues + clip lengths from the measured audio
python3.13 w1-video/tools/verify_numbers.py      # every on-screen number traced

# 4. draft, ledger, final
(cd brutalist.art && ./art run  ../w1-video --height 1080)
(cd brutalist.art && ./art todo ../w1-video)
(cd brutalist.art && ./art final ../w1-video --height 1080 --out ../w1-video/final)
```

If narration text changes: rerun step 3 from `generate_audio_kokoro.py` onward.
Don't hand-edit durations or cue seconds.
