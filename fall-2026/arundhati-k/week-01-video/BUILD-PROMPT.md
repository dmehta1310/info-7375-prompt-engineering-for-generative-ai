# BUILD-PROMPT.md — Expected, Observed

Arundhati Kandelkar · INFO 7375 Week 1 · 2026-09-26

Everything needed to rebuild the video from source. No API keys, no accounts,
no paid calls — the whole pipeline is the Brutalist Fellow Tier.

---

## 0. Prerequisites

```bash
git clone https://github.com/nikbearbrown/brutalist.art
cd brutalist.art && ./setup --install
```

`./setup --install` installs the Python and Remotion dependencies and fetches
the Kokoro model (~325 MB ONNX + ~28 MB voices) into `runtime/models/kokoro/`.

**It does not install `ffmpeg`, and nothing renders without it** — the pipeline
is audio-first, so per-beat MP3 durations are the master clock and `ffprobe` is
what measures them:

```bash
brew install ffmpeg
```

Verify before building — all four must succeed:

```bash
ffmpeg -version && node --version && .venv/bin/python -c "import kokoro_onnx, manim; print('ok')" && ls runtime/models/kokoro/
```

---

## 1. Layout assumed by the commands below

```
INFO7375_Week01/
├── brutalist.art/                                   # the toolkit
└── info-7375-prompt-engineering-for-generative-ai/  # the book
    └── youtube/claude-liam-expected-vs-observed/    # the reel folder
```

Videos travel with their book, per the toolkit's house rule — the reel is built
inside the course repo, never inside `brutalist.art/`.

---

## 2. Verify the numbers FIRST

This is not optional setup, it is the assignment's actual standard. Do it before
authoring anything, and again if the lesson code ever changes:

```bash
cd info-7375-prompt-engineering-for-generative-ai/lessons/01-randomness-and-first-prompts/code
python3 main.py
```

Must print:

```json
{
  "probabilities": [0.09003057317038046, 0.24472847105479764, 0.6652409557748218],
  "counts": { "1": 268, "2": 630, "0": 102 }
}
```

Re-derive every on-screen figure from that output rather than trusting the ones
baked into the components:

```bash
python3 -c "
from main import probabilities, sample
p = probabilities([1,2,3]); c = sample([1,2,3])
e = p[2]*1000
print('expected', round(e,2), 'observed', c[2], 'gap', round(e-c[2],2), 'pct', round((e-c[2])/e*100,3))
"
# expected 665.24 observed 630 gap 35.24 pct 5.297
```

**If these disagree with `ExpectedObserved.tsx`'s `REAL` constants, `main.py`
wins and the components are wrong.**

---

## 3. Install the reel's five components

The body scenes live in the toolkit, not the reel folder:

- `runtime/remotion/src/scenes/ExpectedObserved.tsx` — the five components
- `runtime/remotion/src/Root.tsx` — their five `<Composition>` registrations,
  inside `<Folder name="Expected-Observed">`

Register them so the index can find them, then confirm:

```bash
cd brutalist.art
./art scene-index
for s in SoftmaxInOneBeat ExpectedCount ObservedCounts TheGap WhatWouldSettleIt; do
  ./art scenes --check $s
done
```

All five must report `RENDERABLE 16:9`. If any reports `NOT RENDERABLE — no
<Composition> in Root.tsx`, the registration is not literal enough: the index
parses `Root.tsx` **statically**, so compositions generated inside a `.map()`
are invisible to it. Write each `<Composition>` out by hand.

---

## 4. Build

Audio first — its durations become the clock for everything after:

```bash
cd brutalist.art
REEL=../info-7375-prompt-engineering-for-generative-ai/youtube/claude-liam-expected-vs-observed

.venv/bin/python runtime/scripts/generate_audio_kokoro.py $REEL   # Kokoro am_onyx, free
.venv/bin/python runtime/scripts/remotion_scenes.py     $REEL     # ten beats -> media/B0*.mp4
.venv/bin/python runtime/scripts/compile.py             $REEL     # conform, mux, captions
```

`generate_audio_kokoro.py` writes `actual_duration_s` back into
`beat_sheet.json`. Each beat's props carry a matching `durationSeconds` so the
Remotion compositions are *sized* to the audio via `calculateMetadata` — without
it, `remotion_scenes.py` freeze-holds the final frame to fill the beat and the
animation finishes early. If you change narration, regenerate audio and re-sync
those props; never hand-adjust timing.

```bash
python3 -c "
import json; p='$REEL/beat_sheet.json'; d=json.load(open(p))
for b in d['beats']:
    r=b.get('shot',{}).get('remotion')
    if r: r.setdefault('props',{})['durationSeconds']=round(b['actual_duration_s'],2)
json.dump(d,open(p,'w'),indent=2,ensure_ascii=False)"
```

---

## 5. The gates — a build that skipped these is not done

```bash
./art run   $REEL     # review cut, beat markers
./art final $REEL     # clean master
```

**VISUAL QC LAW** — the mp4 probe is a file check and never counts as QC.
Sample frames and actually look at them:

```bash
ffmpeg -i $REEL/claude-liam-expected-vs-observed.mp4 -vf fps=2 $REEL/_qc/frames/%05d.png
```

Audit the 9-point rubric (edge bleed, title-safe margins, container overflow,
collision, offscreen anchors, legibility, brand bug, aspect, canvas fill) and
log defects and fixes to `_qc/REPORT.md`. Fix root causes in the scene source
and re-render until zero BLOCKER and zero MAJOR remain.

**GATE T** — `TYPECHECK.md` must contain no FAIL. Neither `./art run` nor
`./art final` may report success while it does.

`./art` calls a bare `python3`, which resolves to the system interpreter and
will not have `numpy`/`Pillow`. Put the venv first or both gates silently skip:

```bash
export PATH="$PWD/.venv/bin:$PATH"
```

**Verify the numbers, not just the gates:**

```bash
python3 fall-2026/arundhati-k/week-01-video/evidence/verify_claims.py   # 23/23
```

Two beat-specific checks this reel needs:

- **B01 media ≥ 8s** and the `proof` → `unusual` correction is fully on screen
  before the cut (EXECUTIVE-SUMMARY LAW). `lead_silence_s: 0.8` is written on
  the beat as the law requires, but nothing under `runtime/` appears to read it
  — verify the rendered length, do not trust the field.
- **B05's `CONSTRUCTED ILLUSTRATION` chip and B06's `NOT RUN IN THIS VIDEO`
  caption are legible in sampled frames.** These are honesty labels; if they
  are clipped or unreadable the build has failed the assignment, not just QC.

---

## 6. The single paste-ready prompt

Run from the parent folder that holds both repos:

> Build the reel at
> `info-7375-prompt-engineering-for-generative-ai/youtube/claude-liam-expected-vs-observed/`
> using the `ai-explainer` skill in `brutalist.art` — read
> `skills/make/ai-explainer/SKILL.md` completely first.
>
> Before anything else, run
> `lessons/01-randomness-and-first-prompts/code/main.py` and confirm its output
> matches the `REAL` constants in
> `runtime/remotion/src/scenes/ExpectedObserved.tsx`. If they disagree, stop and
> report it — `main.py` is the authority and the components are wrong.
>
> Then: verify GATE L (`./art scenes --check` for all five body components),
> generate Kokoro `am_onyx` audio, sync each beat's `durationSeconds` prop to its
> measured `actual_duration_s`, render the ten beats, compile, and run the full
> visual QC pass — sample frames at 2fps, read the PNGs, and write
> `_qc/REPORT.md`. Confirm B01's media is ≥8s with the correction landing before
> the cut, and that B05's constructed-illustration chip and B06's "NOT RUN IN
> THIS VIDEO" caption are legible in real frames.
>
> Free pipeline only: no paid API, no keys, no upload. Never publish — leave the
> master in the reel folder.
