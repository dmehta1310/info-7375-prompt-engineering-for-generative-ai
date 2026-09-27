# BUILD-PROMPT — Temperature Is Not a Fact Checker.

## The prompt that started the build (Claude Code, 2026-09-23)

```
in this folder, use skills/make/ai-explainer to make a 120-180 seconds Brutalist AI Explainer
about "Temperature controls how concentrated the choices are; it doesn't check facts",.
12 beats, Kokoro am_onyx, stop at the review cut so I can watch it before anything is submitted.
```

## Rebuild from this folder (free, local, no keys)

Prereqs: `git clone https://github.com/nikbearbrown/brutalist.art` beside this folder,
`./setup --install`, then `pip install matplotlib` in its venv.

```bash
source ../brutalist.art/.venv/bin/activate
TK=../brutalist.art

# 0. evidence — reproduce every number (prints the chapter's tables)
(cd code && python3 run_temperature.py)

# 1. components — register the reel-local scenes (skip if already present)
cp remotion-src/TemperatureConcentration.tsx.txt $TK/runtime/remotion/src/TemperatureConcentration.tsx
#    + add the import and <Folder name="TemperatureConcentration"> block to Root.tsx
#    (7 Compositions, calculateMetadata from props.durationSeconds)

# 2. audio — the master clock
python3 $TK/runtime/scripts/generate_audio_kokoro.py . < /dev/null   # am_onyx, $0.00 (stdin closed: it can hang waiting on it)
ffmpeg -y -f lavfi -t 0.8 -i anullsrc=r=24000:cl=mono -i mp3/beat-B01.mp3 \
  -filter_complex "[0:a][1:a]concat=n=2:v=0:a=1" mp3/_b01.mp3 && mv mp3/_b01.mp3 mp3/beat-B01.mp3
#    then set B01.actual_duration_s to the new ffprobe duration
python3 $TK/runtime/scripts/align.py .                          # word clock

# 3. props — cues from word timings, typeset math, real draw sequences
python3 code/build_props.py

# 4. render every beat (Remotion, 4K supersampled)
python3 $TK/runtime/scripts/remotion_scenes.py . --force

# 5. review cut (timecode + beat ids burned in)
python3 $TK/runtime/scripts/compile.py . --review --height 1080

# 6. visual QC — sample frames, READ them, log in _qc/REPORT.md
ffmpeg -i temperature-concentration-review.mp4 -vf fps=2 _qc/frames/%05d.png
```

Never publishes. The clean master (`./art final .`) is a separate, human-approved step.
