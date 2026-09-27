# BUILD-PROMPT — Repeatable is not the same as true

Toolkit checkout: `brutalist.art` at `6a8380a`.  
Reel folder used to render: `/Users/saket/brutalist.art/youtube/yash-s-seed-repeatable`.  
Master written 2026-09-26: `yash-s-seed-repeatable.mp4` (137.8s).

Free path only. Kokoro locally. No paid video API, no upload.

## Prompts that produced the cut

Concept, 2026-09-25, with Claude Code:

> Pick a Chapter 1 concept for a 2–4 minute explainer that can be shown with real output from `main.py`. Use one idea, not a chapter tour.

That settled on: a seed makes a run repeatable; it does not make the answer true.

Beat plan, same session:

> Open on whether the same script run twice gives the same answer. Show `sample([1,2,3], seed=7)` called twice. Explain that the seed fixes generator state, and label that card as a diagram. Call the unmodified `sample()` with `seed=99` and put the counts beside seed 7. Then say repeatable and correct are different, name one boundary (this machine, this Python, right now), and close.

2026-09-26, this session, after the previous one stopped on the type gate:

> The type check is still failing and there is no clean master. Fix the failing beats, render `./art final`, and write the Canvas files.

## Commands

Reprint the evidence, from the course repo root:

```bash
python3 -c "import sys; sys.path.insert(0,'lessons/01-randomness-and-first-prompts/code'); from main import sample; print(sample([1,2,3], seed=7)); print(sample([1,2,3], seed=7)); print(sample([1,2,3], seed=99))"
```

Render, from the toolkit root. `PYTHONPATH` has to include Pillow, numpy, and scipy or `./art final` skips the type check and then the frame check exits:

```bash
export PYTHONPATH="/tmp/typecheck-venv/lib/python3.13/site-packages"
python3 runtime/scripts/remotion_scenes.py \
  /Users/saket/brutalist.art/youtube/yash-s-seed-repeatable --only B01 --force
./art final /Users/saket/brutalist.art/youtube/yash-s-seed-repeatable \
  --out /Users/saket/brutalist.art/youtube/yash-s-seed-repeatable
```

`--only` takes one beat. The full re-render on 2026-09-26 looped `B00` through `B06` with `--force`.

Scene files that differ from toolkit `6a8380a` are in `components/` as `.tsx.txt` (the course repo rejects a real `.tsx` outside `learning-artifacts/`). Copy each one back to `runtime/remotion/src/scenes/` under its `.tsx` name before a rebuild, or the master will not match.

## What those scene edits are

- `MedhavyConceptCard.tsx` and `MedhavyTwoColumnCard.tsx`: larger spark line, and a card with a dark rule that fills the title-safe area. The white card on cream was invisible to the fill check.
- `ShellSession.tsx`: larger terminal type, a cream page behind a large dark window, a `|` prompt instead of `%` (the percent slash measured as a too-short text run at 8K), and no translucent highlight bar behind the counts. That bar failed the local contrast check at 1.17:1.

`ShellSession` is registered at 3840×2160, and `remotion_scenes.py` also passes `--scale=2`, so those beats are 7680×4320. The type floor is 1.9% of that height, 82px. The other cards are 1920×1080 scaled to 3840×2160, floor 41px.
