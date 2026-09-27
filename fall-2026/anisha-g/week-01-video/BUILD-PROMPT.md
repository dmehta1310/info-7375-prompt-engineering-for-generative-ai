# Build Prompt and Commands

## Final build prompt

> Build a 2–4 minute INFO 7375 Week 1 explainer on one Chapter 1 concept: a seed makes a run repeatable, but it does not make the answer true. Use the unmodified course `main.py` seed-7 counts and a controlled seed-8 run. Show where the seed enters `sample()`, show two identical seed-7 calls, change only the seed, explain the official repeatability test, and end by showing that the function receives no source, answer key, or verifier. Label `[1,2,3]` as a course-constructed input. Use original course-aligned diagrams, local Kokoro `af_bella` narration at speed `0.94`, a visible synthetic-voice disclosure, and all required documentation.

## Evidence commands

From the public course repository:

```bash
python3 lessons/01-randomness-and-first-prompts/code/main.py
python3 -m unittest lessons/01-randomness-and-first-prompts/code/tests/test_main.py -v
```

From this folder:

```bash
python3 code/seed_demo.py
python3 code/test_seed_demo.py
python3 build_video.py
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 \
  Gaikar_Anisha_INFO7375_Week01_Video.mp4
```

## Narration regeneration

```bash
git clone https://github.com/nikbearbrown/brutalist.art.git
python3 -m pip install kokoro-onnx
mkdir -p /path/to/brutalist.art/runtime/models/kokoro
cd /path/to/brutalist.art/runtime/models/kokoro
curl -fLO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -fLO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
cd /path/to/this/week-01-video
ART_HOME=/path/to/brutalist.art python3 \
  /path/to/brutalist.art/runtime/scripts/generate_audio_kokoro.py . --speed 0.94
python3 build_video.py
```

## Rebuild contract

- `beat_sheet.json` is the source of truth for narration, visuals, source claims, and measured beat durations.
- Included MP3 files are the master clock.
- `build_video.py` produces original motion graphics, the MP4, captions, and timeline.
- Numeric labels must match `code/course_main_output.txt` and `code/seed_output.txt`.
- No paid service, API key, private transcript, or external media is required.
