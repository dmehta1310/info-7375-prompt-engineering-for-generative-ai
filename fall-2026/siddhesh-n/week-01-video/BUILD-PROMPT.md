# Build Prompt and Commands

## Final build prompt

> Build a 2–4 minute INFO 7375 Week 1 explainer on one Chapter 1 concept: why subtracting the maximum changes softmax intermediates but not the distribution. Use the unmodified course `main.py` output for `[1,2,3]` and the official `[1000,1000] → [0.5,0.5]` test. Show the subtraction, weights, normalization, and common-factor cancellation. End with the exact claim boundary from the chapter. Use an original course-aligned diagram style based on the professor's visual language, not copied artwork. Use free local Kokoro `af_bella` narration at speed `0.94`, disclose that the voice is synthetic, and ship the required README, MP4, beat sheet, build prompt, sources, and Frictional log.

## Evidence commands

From the public course repository:

```bash
python3 lessons/01-randomness-and-first-prompts/code/main.py
python3 -m unittest lessons/01-randomness-and-first-prompts/code/tests/test_main.py -v
```

From this folder:

```bash
python3 code/softmax_demo.py
python3 build_video.py
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 \
  Nikam_Siddhesh_INFO7375_Week01_Video.mp4
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

- `beat_sheet.json` is the source of truth for narration, visual intent, source claims, and measured audio durations.
- The included MP3 files are the master clock.
- `build_video.py` generates beat-specific motion, the final MP4, the SRT captions, and `build/timeline.json`.
- Numeric labels must agree with `code/course_main_output.txt` and `code/softmax_output.txt`.
- No paid service, API key, private transcript, or external media is required.
