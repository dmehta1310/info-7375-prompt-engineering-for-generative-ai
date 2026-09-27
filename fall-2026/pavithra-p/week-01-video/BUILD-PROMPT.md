# BUILD-PROMPT — Thousands of Years, Divided

How to rebuild this video from this folder, for $0, offline except for the one-time installs.

## 1. What you need

- macOS with Homebrew, Python 3.12, Node ≥ 20
- `ffmpeg`, `cairo`, `pkg-config`, `pango` (Manim needs the last three)
- A checkout of the Brutalist toolkit **beside** the course repo:

```bash
git clone https://github.com/nikbearbrown/brutalist.art
```

```bash
brew install ffmpeg cairo pkg-config pango
```

(On this machine Homebrew needed `HOMEBREW_NO_AUTO_UPDATE=1 HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1` in front; see FRICTIONAL.md.)

**Toolkit revision used:** `brutalist.art` commit `6a8380ae169cca81e0633664a65c958f5c12ab4b` (2026-09-20). To rebuild with the same version: `git -C brutalist.art checkout 6a8380a`. The only local change in that checkout is `runtime/remotion/package-lock.json`, rewritten by `./setup --install` (`npm install`).

```bash
cd brutalist.art && python3.12 -m venv .venv && . .venv/bin/activate && ./setup --install
```

`./setup` may end with an "ElevenLabs reference found" message caused by the toolkit's own example files. The installs still complete; see FRICTIONAL.md for the manual readiness checks.

## 2. Rebuild, in order

Run from `brutalist.art/` with the venv active. `REEL` is this folder.

```bash
REEL=../info-7375-prompt-engineering-for-generative-ai/fall-2026/pavithra-p/week-01-video
```

**a. Numbers.** Regenerate `evidence.json` from the course script. It fails loudly if the script's printed output ever differs.

```bash
python3 $REEL/evidence.py
```

**b. Narration (the master clock).** Kokoro voice `af_bella`, local, $0. It writes `mp3/beat-B0*.mp3` and stamps the measured durations into `beat_sheet.json`.

```bash
python runtime/scripts/generate_audio_kokoro.py $REEL
```

**c. Visuals + review cut.** Runs QC gates L, A, W, B and V, renders each Manim scene in `scenes.py` at 4K into `manim/`, and compiles a review cut.

```bash
./art run $REEL --height 1080
```

**d. Clean master.**

```bash
./art final $REEL
```

## 3. What drives what

- `beat_sheet.json`: narration text, the visual plan per beat, and (after step b) the measured audio lengths.
- `scenes.py`: one Manim `Scene` per beat (`B00_Hook` … `B07_Close`). Each scene reads its beat's audio length and narration from `beat_sheet.json`, places cues where the matching phrase is spoken, and checks every number against `evidence.json`.
- `evidence.py`: imports `research/llm_scale.py` unchanged. The only numbers it adds are the labelled 8-hours-a-day extension, computed with the script's own `reading_years()`.

## 4. The prompts that produced it

The video was built in a Claude Code session (Claude Opus 5.5) directed by me. The private transcript is not included. In summary, the requests were:

1. "Tell me what the assignment needs and give me a plan." Then: "Pick a concept from Chapter 1 that is easy to explain and scores well on the rubric."
2. Concept chosen: *a training-scale slogan restated as a division with a hidden assumption* (after first trying and dropping a Part 2 topic).
3. "Show me the beat plan." I asked for wording changes in B01, B02, B04, B05 and B06, and to skip the Claude-UI opening.
4. "Show me the full narration." I required two accuracy corrections (B00, B06) before approving.
5. "Generate the voice and animations", in the style of Brutalist's ai-explainer (one idea per beat, numbers move on screen), made original rather than copied.
6. Constraint throughout: free pipeline only, and **do not commit or push anything**.
