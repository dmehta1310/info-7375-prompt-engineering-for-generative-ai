# Build Instructions

Run from the `expected-vs-observed/` project folder. Assumes the Brutalist
toolkit is already set up (Kokoro model downloaded, Manim + ffmpeg installed)
per the toolkit's own README.

## 1. Render all Manim scenes

```bash
manim -pql scenes.py BeatIntro Beat00Hook Beat01Setup Beat02Expected Beat03Observed Beat04SecondSeeds Beat05Coin Beat06Comparison Beat07Boundary Beat08Recap
```

Output lands in `media/videos/scenes/480p15/`.

## 2. Recombine the coin-flip and comparison-bars scenes

These two Manim scenes share a single narration beat (B05), so they get
concatenated into one clip before pairing with audio:

```bash
cd media/videos/scenes/480p15
python3 -c "
with open('concat_list.txt', 'w') as f:
    f.write(\"file 'Beat05Coin.mp4'\n\")
    f.write(\"file 'Beat06Comparison.mp4'\n\")
"
ffmpeg -f concat -safe 0 -i concat_list.txt -c copy Beat05Combined.mp4
cd ../../../..
```

## 3. Give the silent intro clip a matching silent audio track

The intro has no narration. Mux in silence at the same format (24kHz mono
AAC) as the Kokoro narration so it concatenates cleanly with the other clips:

```bash
ffmpeg -y -i media/videos/scenes/480p15/BeatIntro.mp4 \
  -f lavfi -i anullsrc=r=24000:cl=mono \
  -c:v copy -c:a aac -shortest \
  final/beat_intro.mp4
```

## 4. Pair each narrated scene with its Kokoro audio

Run this from the project root. It checks each pair's duration and either
freezes the last frame (video shorter than audio) or trims the video
(video longer than audio) so video and audio always match exactly:

```bash
python3 << 'PYEOF'
import subprocess

pairs = [
    ("media/videos/scenes/480p15/Beat00Hook.mp4", "mp3/beat-B00.mp3", "final/beat00.mp4"),
    ("media/videos/scenes/480p15/Beat01Setup.mp4", "mp3/beat-B01.mp3", "final/beat01.mp4"),
    ("media/videos/scenes/480p15/Beat02Expected.mp4", "mp3/beat-B02.mp3", "final/beat02.mp4"),
    ("media/videos/scenes/480p15/Beat03Observed.mp4", "mp3/beat-B03.mp3", "final/beat03.mp4"),
    ("media/videos/scenes/480p15/Beat04SecondSeeds.mp4", "mp3/beat-B04.mp3", "final/beat04.mp4"),
    ("media/videos/scenes/480p15/Beat05Combined.mp4", "mp3/beat-B05.mp3", "final/beat05.mp4"),
    ("media/videos/scenes/480p15/Beat07Boundary.mp4", "mp3/beat-B06.mp3", "final/beat06.mp4"),
    ("media/videos/scenes/480p15/Beat08Recap.mp4", "mp3/beat-B07.mp3", "final/beat07.mp4"),
]

def get_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True
    )
    return float(out.stdout.strip())

for video, audio, out in pairs:
    v_dur = get_duration(video)
    a_dur = get_duration(audio)
    gap = a_dur - v_dur
    print(f"{video}: video={v_dur:.2f}s audio={a_dur:.2f}s gap={gap:.2f}s")

    if gap > 0.05:
        cmd = [
            "ffmpeg", "-y", "-i", video, "-i", audio,
            "-filter_complex", f"[0:v]tpad=stop_mode=clone:stop_duration={gap}[v]",
            "-map", "[v]", "-map", "1:a",
            "-c:v", "libx264", "-c:a", "aac",
            "-shortest", out
        ]
    else:
        cmd = [
            "ffmpeg", "-y", "-i", video, "-i", audio,
            "-map", "0:v", "-map", "1:a",
            "-c:v", "libx264", "-c:a", "aac",
            "-t", str(a_dur), out
        ]
    subprocess.run(cmd, check=True)
    print(f" -> wrote {out}")

print("done")
PYEOF
```

## 5. Concatenate into the final video

```bash
cd final
cat > list.txt << 'PYEOF'
file 'beat_intro.mp4'
file 'beat00.mp4'
file 'beat01.mp4'
file 'beat02.mp4'
file 'beat03.mp4'
file 'beat04.mp4'
file 'beat05.mp4'
file 'beat06.mp4'
file 'beat07.mp4'
PYEOF
ffmpeg -f concat -safe 0 -i list.txt -c copy week01_expected_vs_observed.mp4
cd ..
```

Output: `final/week01_expected_vs_observed.mp4` (~2:09).
