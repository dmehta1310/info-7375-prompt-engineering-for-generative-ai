# BUILD-PROMPT — rebuild this video end to end

Everything needed to reproduce `temperature-is-concentration.mp4` from this
folder. Free pipeline only: Kokoro TTS, Manim, Remotion, ffmpeg. No API keys,
no paid calls, no account.

---

## 0. Prerequisites

```bash
brew install ffmpeg                  # required; the pipeline muxes through it
python3 --version                    # must be 3.10+ (I used 3.12.9)
node --version                       # must be >= 20 (I used 23.11.0)
```

Fonts **EB Garamond** and **PT Mono** must be visible to fontconfig
(`fc-list | grep -i garamond`). Both ship in the toolkit's `runtime/fonts/`.
LaTeX is *not* required — the equations are Unicode text by design.

## 1. Get the toolkit

```bash
git clone <brutalist.art toolkit> brutalist.art
cd brutalist.art
python3.12 -m venv .venv && source .venv/bin/activate
./setup --install                    # python deps + remotion node_modules + Kokoro model (~340MB)
./setup                              # readiness table — every row should read READY
```

> `./art` calls bare `python3`, so **activate the venv in every new terminal**
> before running any of the commands below.

## 2. Get the real numbers (the source of truth)

```bash
git clone https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai.git chapter1-course
cd chapter1-course
python3 lessons/01-randomness-and-first-prompts/code/main.py | tee ../week-01-video/main-output.txt
```

Expected (seed 7, n = 1000, T = 1):

```json
{"probabilities": [0.09003057317038046, 0.24472847105479764, 0.6652409557748218],
 "counts": {"1": 268, "2": 630, "0": 102}}
```

Every figure on screen traces back to this file — see `FACTCHECK.md` in the
reel folder for the claim-by-claim table.

## 3. Stage the reel

```bash
mkdir -p ../week-01-video/reel
cp beat_sheet.json scenes.py make_srt.py \
   FACTCHECK.md SHOTLIST.md PROMPTS.md CHECKS-REPORT.md ../week-01-video/reel/   # from this submit folder
```

The reel also needs its paperwork set, or GATE F refuses to render:
`FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md` (and `CHECKS-REPORT.md` for the
PROOF GATE). All four ship in this folder, and the `cp` above stages them.

**No toolkit modification is required.** Every beat renders from either
`scenes.py` (the five Manim beats, including the outro) or a composition the
toolkit already ships. Confirm the shipped ones are renderable:

```bash
for c in ClaudeComposerAsk BrutalistHesitantWriter ClaudeVerdictArtifact; do
  ./art scenes --check $c        # each must print RENDERABLE
done
```

## 4. Build (audio first — audio is the master clock)

```bash
cd brutalist.art && source .venv/bin/activate
REEL=../week-01-video/reel

python3 runtime/scripts/generate_audio_kokoro.py "$REEL"   # 10 mp3s, af_bella, $0.00
./art run "$REEL" --height 1080                            # gates + Manim + Remotion + review cut (1080 = faster QC pass)
./art todo "$REEL"                                         # must report zero open slots
./art final "$REEL" --out "$REEL"                          # 4K master -> $REEL/temperature-is-concentration.mp4
                                                           # (without --out it lands in the toolkit's renders/)
python3 runtime/scripts/align.py "$REEL"                   # word timings -> $REEL/mp3/words.json
python3 "$REEL/make_srt.py" "$REEL"                        # captions -> $REEL/temperature-is-concentration.srt
```

Never hand-tune timing. If narration needs to change, edit `narration_text` in
`beat_sheet.json`, re-run `generate_audio_kokoro.py`, and recompile — the
measured mp3 durations are the clock, and `scenes.py` reads them from the
`DUR` table at the top of the file.

## 5. Visual QC (required — the mp4 probe is not QC)

```bash
ffmpeg -i "$REEL/temperature-is-concentration.mp4" -vf fps=2 "$REEL/_qc/frames/%05d.png"
```

Then actually look at the frames against the 9-point rubric (edge bleed,
title-safe margins, container overflow, collision, offscreen anchors,
legibility, brand bug, aspect, canvas fill) and log findings in
`_qc/REPORT.md`. Full spec: `CLAUDE-CODE-VISUAL-QC-CHECK.md` at the toolkit
root.

---

## The prompts I actually gave Claude

**Authoring the reel:**

```
Build an ai-explainer reel about "temperature is a concentration control, not a
fact checker" into ../week-01-video/reel/.
Constraints for this school assignment:
- 2–4 minutes, ONE concept, not a chapter summary.
- The core beat must SHOW the mechanism with these REAL numbers from
  main-output.txt: probabilities [0.09003057317038046, 0.24472847105479764,
  0.6652409557748218]; counts {0: 102, 1: 268, 2: 630} at seed 7.
- Explain it via the RATIO p2/p0 = exp((z2 - z0)/T), not a creativity metaphor.
- Add a beat that names ONE thing this explanation does NOT establish.
- Label any constructed illustration on screen as "illustrative, not measured".
- Voice: kokoro af_bella. Free pipeline only, no keys.
```

**Building it (the paste-ready build prompt):**

```
Read skills/make/ai-explainer/SKILL.md completely, then build
../week-01-video/reel to a 4K master.
- Verify every on-screen figure against week-01-video/main-output.txt first;
  recompute the softmax independently and stop if anything disagrees.
- Library-first: ./art scenes --check every composition the beat sheet names
  before rendering anything.
- Write scenes.py for the four Manim beats, sized to the MEASURED audio
  durations in mp3/timings.json. No MathTex — LaTeX is not installed; use
  Unicode and verify the glyphs exist in EB Garamond.
- Keep all text inside the house safe area (±6.3, ±3.4); gates A, W and B must
  pass clean with ART_STRICT=1.
- Audio first, then ./art run, then frame-level visual QC into _qc/REPORT.md,
  then ./art final.
- Never publish. No paid API. Stop and report if any step asks for a key.
```
