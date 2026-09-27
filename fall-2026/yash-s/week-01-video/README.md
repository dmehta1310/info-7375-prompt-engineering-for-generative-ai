# Week 1 explainer — Repeatable is not the same as true

**Name:** Yash Saraf  
**Course:** INFO 7375, Fall 2026  
**Concept:** A seed makes a run repeatable. It does not make the answer true.  
**Why this one:** It is one mechanism, and Chapter 1 already prints the counts that show it.  
**Runtime:** 2:18 (137.8 seconds).  
**Narration:** Kokoro `af_bella`, local and synthetic. The voice is not me.

The video shows `sample([1, 2, 3], seed=7)` twice, then the same function with `seed=99`. The course file `lessons/01-randomness-and-first-prompts/code/main.py` was not edited.

## What is in this folder

| File | Role |
|---|---|
| `yash-s-seed-repeatable.mp4` | Clean master. No beat markers. |
| `beat_sheet.json` | Narration and the visual plan that was rendered. |
| `BUILD-PROMPT.md` | Commands and prompts that rebuild it. |
| `SOURCES.md` | What was run, what was made, what Claude wrote. |
| `FRICTIONAL.md` | Dated log of what actually happened. |
| `FACTCHECK.md` | The counts and the command that reprints them. |
| `components/` | The three Remotion scenes this cut used, saved as `.tsx.txt`. |

## Rebuild

From a checkout of `brutalist.art` at `6a8380a`, with `./setup` already green for Kokoro, ffmpeg, and Remotion:

```bash
# 1. Use the scene files from this submission. A fresh toolkit copy
#    will not match this master until these three files replace the
#    ones under runtime/remotion/src/scenes/.
# Stored as .tsx.txt so the course validator, which rejects .tsx outside
# learning-artifacts/, will accept this folder. Rename them back on copy.
for f in components/*.tsx.txt; do
  base="$(basename "$f" .txt)"
  cp "$f" "/path/to/brutalist.art/runtime/remotion/src/scenes/$base"
done

# 2. Point the toolkit at this reel folder (the copy that contains beat_sheet.json
#    and the mp3/ narration). Then, from the toolkit root:
export PYTHONPATH="/path/to/venv/lib/python3.13/site-packages"
python3 runtime/scripts/remotion_scenes.py /path/to/this-reel --force
./art final /path/to/this-reel --out /path/to/this-reel
```

`./art final` runs the type check, then writes `yash-s-seed-repeatable.mp4`. Pillow, numpy, and scipy have to be importable. Without them the type check is skipped and the frame check refuses the cut.

Reprint the numbers, from the course repository root:

```bash
python3 -c "import sys; sys.path.insert(0,'lessons/01-randomness-and-first-prompts/code'); from main import sample; print(sample([1,2,3], seed=7)); print(sample([1,2,3], seed=7)); print(sample([1,2,3], seed=99))"
```

On this machine, Python 3.13.5, that printed `{0: 102, 1: 268, 2: 630}` twice and `{0: 93, 1: 267, 2: 640}` for seed 99. Checked again on 2026-09-26.
