# Build prompt — Three Scores Are Not Yet Three Chances

Everything needed to rebuild the video from this folder. Commands are in the order they were run
on 2026-09-26 (macOS 26.6, Apple Silicon). Cost: $0.00 — no API keys, no paid services.

## 1. Tools

```bash
# Homebrew (asks for your password; run in Terminal yourself)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install python@3.12 node ffmpeg cairo pkgconf pango
```

## 2. Brutalist toolkit

```bash
git clone https://github.com/nikbearbrown/brutalist.art.git
cd brutalist.art
git checkout 6a8380ae169cca81e0633664a65c958f5c12ab4b
python3.12 -m venv .venv
source .venv/bin/activate
./setup --install
```

Two workarounds were needed on this machine (details in `FRICTIONAL.md`):

- **Python packages failed to compile** (`pycairo`: "Compiler cc cannot compile programs"), because
  the newest Command Line Tools SDK (MacOSX27.0) does not link. Install with the 26.5 SDK instead:
  ```bash
  SDKROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX26.5.sdk python3 -m pip install -r requirements.txt
  ```
- **`./setup` stops on its own ElevenLabs guard**, which flags the toolkit's own tutorial files. The
  installs still complete; the readiness checks can be run from a copy of `setup` with that guard
  removed. Expected result: everything ready except "Manim equation beats" (LaTeX, not used).

## 3. Verify the numbers first

From the course repository root:

```bash
python3.12 lessons/01-randomness-and-first-prompts/code/main.py
python3.12 lessons/01-randomness-and-first-prompts/code/tests/test_main.py -v
```

Expected: probabilities `0.09003057317038046, 0.24472847105479764, 0.6652409557748218`; 6 tests OK.
`scenes.py` checks the same values and refuses to render if they differ.

## 4. Narration audio (the clock)

```bash
cd <brutalist.art> && source .venv/bin/activate
python3 runtime/scripts/generate_audio_kokoro.py <course>/fall-2026/varnika-m/week-01-video
```

Writes one MP3 per beat from `narration_text` in `beat_sheet.json` and records each measured length.
Never hand-tune timing: to change a line, edit `beat_sheet.json`, regenerate that beat with
`--only B0x`, and rebuild.

## 5. Review cut

```bash
./art run <course>/fall-2026/varnika-m/week-01-video
```

Renders the Manim scenes from `scenes.py` and the Remotion scenes named in `beat_sheet.json`, runs the
toolkit's checks, and writes `three-scores-not-three-chances-slate.mp4` (with beat labels) for review.
A beat is only re-rendered if its file is deleted first, e.g. `rm manim/B04.mp4` or `rm media/B01.mp4`.

## 6. Final

```bash
./art final <course>/fall-2026/varnika-m/week-01-video --height 1080 \
  --out <course>/fall-2026/varnika-m/week-01-video/final
```

Output: `final/three-scores-not-three-chances.mp4`, 135.8 s, 1920×1080.

## 7. Prompts

I built this with Claude Code (NEU-provisioned) in one session. The main requests, in order:

1. "Go through the entire repo and explain this assignment in easy, simple English."
2. "Let's do the setup first." (toolkit installation and debugging)
3. "Select one concept from Chapter 1, the easiest to understand and explain." I chose
   "Three scores are not yet three chances" from the options offered.
4. Claude drafted the narration and a plan for each beat from my saved evidence; I read it and
   approved it before anything was rendered.
5. Revisions I requested after watching the review cut:
   - remove the narrator's spoken self-introduction; disclose the synthetic voice in `SOURCES.md`
   - relabel the bars A, B, C so "the third option" matches what is on screen
   - shorten the end-card voice note
6. "Finalize."

No image, video, or voice generation prompts were used; every visual is rendered locally from
`scenes.py` or a toolkit scene. The only prompt shown in the video is the viewer exercise in B09.
