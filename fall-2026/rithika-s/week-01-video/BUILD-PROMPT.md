# BUILD-PROMPT — "The Token That Followed"

The paste-ready prompt and the exact commands that build this reel end to end.
Per the skill's Step 6, a reel without its build prompt is unfinished.

---

## 0. Environment

macOS, Python 3.12.12, Node 24.14.1, ffmpeg 8.0. No API keys — Kokoro TTS ships
inside the toolkit. Total spend: **$0.00**.

Two paths matter and are easy to get wrong (see `FRICTIONAL.md` #1, #2):

```bash
# the toolkit is the CLONE, not the parent folder
export ART_HOME=/Users/rithika/Downloads/brutalist/brutalist.art
# ./art only auto-detects $ART_HOME/.venv — this venv lives one level up
export VIRTUAL_ENV=/Users/rithika/Downloads/brutalist/.venv
export PATH="$VIRTUAL_ENV/bin:$PATH"
export REEL=/Users/rithika/Downloads/brutalist/info-7375-prompt-engineering-for-generative-ai/fall-2025/rithika-s/week-01-video
```

## 1. The paste-ready prompt

> Act as an expert AI engineering educator and technical video director. Using the
> Brutalist toolkit (`github.com/nikbearbrown/brutalist.art`), build a 3-to-4-minute
> Chapter 1 explainer, narrator persona **Sasha**, Kokoro TTS, on the topic
> **"What pretraining actually targets (the token that followed, not the truth)."**
>
> Obey four constraints:
>
> 1. **Show the mechanism, do not assert it.** Do not talk over a slide reading
>    "models learn to predict the next word, not facts." Display a factually
>    incorrect training sentence from a hypothetical corpus — a sci-fi text reading
>    "The moon is made of green cheese." Show the model predicting the token after
>    "green." Show the target vector being strictly `cheese` because it is in the
>    text, not `rock` because it is true. Show the raw logits, the softmax
>    probabilities, and how the loss penalizes low probability on `cheese`
>    regardless of empirical truth.
> 2. **Worked example, honest numbers.** Compute real softmax probabilities that sum
>    to exactly 1.0. Label the sequence `CONSTRUCTED EXAMPLE` on screen.
> 3. **Name the boundary.** Close by stating and displaying what this does *not*
>    establish — e.g. how post-training (preference tuning, RLHF) later attempts to
>    steer the model away from raw corpus mimicry toward factual accuracy.
> 4. **Ship the paperwork.** `beat_sheet.json`, `BUILD-PROMPT.md`, `SOURCES.md`,
>    `FRICTIONAL.md`, `README.md`, and the `Ch1Pretrain*` Remotion components
>    inheriting a `Ch1Chrome` chassis.
>
> Run GATE L before authoring any beat. Verify the softmax arithmetic with a runnable
> script. Audio is the master clock — never hand-tune timing. Package to
> `SankarRajeswari_Rithika_INFO7375_Week01_Video.zip` laid out for
> `fall-2025/rithika-s/week-01-video/`.

## 2. The build, command by command

```bash
# ── GATE L — library-first. Ask the library BEFORE authoring a beat. ──────────
cd "$ART_HOME"
./art doctor                       # readiness: all green, $0.00
./art scenes "softmax probabilities over candidate tokens, logit scores, next-token prediction"
./art scenes --check ClaudeComposerAsk
./art scenes --check BrutalistHesitantWriter
./art scenes --check ClaudeVerdictArtifact
./art scenes --check ClaudeTitleOutro
```

GATE L returned a **genuine miss** — eight leads, none a distribution/logit/loss/
gradient scene. A miss is a design card, so the chassis and seven mechanism scenes
were written (`runtime/remotion/src/scenes/Ch1*.tsx`), registered in `Root.tsx` under
the `Ch1-Pretraining` folder, then:

```bash
# ── verify the components compile and are actually renderable ────────────────
cd "$ART_HOME/runtime/remotion"
npx tsc --noEmit -p .                        # zero errors
npx remotion compositions src/index.ts | grep Ch1Pretrain   # all 8 listed
cd "$ART_HOME"
./art scene-index                            # 610 → 618 renderable, 0 unresolved

# ── prove the arithmetic BEFORE it is narrated ───────────────────────────────
python3 "$REEL/verify_softmax.py"            # exits 0 only if every figure reproduces

# ── author beat_sheet.json (13 beats, show blocks, scene props) ──────────────

# ── audio is the master clock ────────────────────────────────────────────────
python3 runtime/scripts/generate_audio_kokoro.py "$REEL"
#   pass 1: 698 words measured 4:13 — over the 4-minute cap.
#   pass 2: cut ~100 words of number-reciting narration -> 3:42.
#   pass 3: re-timed to the ~3:15 target -> 532 words, 3:16 (195.63 s decoded).
#   NEVER hand-tune timing: cut words, regenerate, re-sync durationS, recompile.
#   Delete the stale mp3s first — the script skips beats whose clip exists.
rm -f "$REEL"/mp3/*.mp3
python3 runtime/scripts/generate_audio_kokoro.py "$REEL"

# ── render the beat scenes (conformed to the measured clock) ─────────────────
python3 runtime/scripts/remotion_scenes.py "$REEL"

# ── compile the review cut, then the verified master ────────────────────────
./art run   "$REEL"
./art todo  "$REEL"
./art final "$REEL"

# ── VISUAL QC LAW — frame-level, not an mp4 probe ───────────────────────────
ffmpeg -i "$REEL/<slug>.mp4" -vf fps=2 "$REEL/_qc/frames/%05d.png"
#   then READ the PNGs and audit the 9-point rubric; log to _qc/REPORT.md

# ── re-prove the arithmetic after the build ─────────────────────────────────
python3 "$REEL/verify_softmax.py"
```

## 3. The generation prompt shown on screen (beat B03)

ASK→RESULT LAW requires the reel to show the prompt that produced its generated
figures. B03's composer displays this verbatim, and it is the prompt that actually
chose the logits:

> Pick four candidate tokens and four clean logits such that the 4-dp softmax
> probabilities sum to exactly 1.0. Compute `exp(z)`, the softmax, the cross-entropy
> against a one-hot target, and the gradient `p − y`. Assert every displayed figure.

Its RESULT lines are the real assertion output of `verify_softmax.py`.

## 4. Rebuild contract

`beat_sheet.json` is the only source of truth; `mp3/` durations are the clock;
`media/` is derived. To change a number on screen, change it in `verify_softmax.py`
first, re-run it, and only then edit the beat sheet's scene props — the script is the
gate, not the commentary.


---

# Revision 2 — 2026-09-23: the 4:00 floor and the six-act rebuild

Runtime floor raised to 4:00 by a live-class instruction from the professor, overriding
the written 2–4 minute syllabus target (`FRICTIONAL.md` § Revision — 2026-09-23). The cut
was re-authored into six acts for a viewer who has never heard of next-token prediction,
not padded.

## The paste-ready prompt

> Rebuild the Week 1 explainer to run at least 4:00 and to be genuinely followable by
> someone who has never heard of next-token prediction — by pacing, not by simplifying
> the mechanism and not by adding graphics, faster cuts, or hype. Six acts:
> (1) **Hook** 10–15s — open on "The moon is made of green cheese" as a plain sentence,
> ask on screen what the model learns to predict after "green", and let the viewer guess
> before showing the answer. (2) **Mechanism, slowly** — reveal that the target is
> "cheese" not "rock" because the model is scored against what is IN the text, then show
> the real math one step at a time, held long enough to read: raw logits → subtract max →
> exponentiate → normalize → final probabilities, summing to exactly 1.0, labelled
> CONSTRUCTED EXAMPLE throughout. (3) **Contrast** 20–30s — the same setup against a
> corpus containing the TRUE sentence, and how the target vector differs. (4) **Loss
> consequence** 15–20s — the penalty lands on "cheese" because it is the next actual
> token, regardless of truth. (5) **Named boundary** 20–30s — what this does NOT
> establish: post-training (RLHF / preference tuning) is a separate, later mechanism.
> Real screen time, not a title card. (6) **Takeaway** 10s — one plain sentence, no new
> claims. Every on-screen number must be real output from re-running the softmax
> calculation and verified to sum to 1.0. Verify the final duration with
> `ffprobe -show_entries format=duration` and report the actual number. If it clears
> 4:00 through acts 1–6, stop — do not add a seventh act to pad.

## The commands, in order

```bash
export ART_HOME=/Users/rithika/Downloads/brutalist/brutalist.art
export VIRTUAL_ENV=/Users/rithika/Downloads/brutalist/.venv
export PATH="$VIRTUAL_ENV/bin:$PATH"
export REEL=.../fall-2025/rithika-s/week-01-video

# ── 1. the arithmetic first, and emit it as data ─────────────────────────────
python3 "$REEL/verify_softmax.py" --emit     # 5-step pipeline asserted -> softmax_values.json

# ── 2. build the beat sheet FROM the verified figures ───────────────────────
python3 "$REEL/build_beat_sheet.py"          # 12 beats, 6 acts; no number hand-typed

# ── 3. the four new components, then make them renderable ──────────────────
#     Ch1PretrainHook · Ch1PretrainLadder · Ch1PretrainContrast · Ch1PretrainTakeaway
cd "$ART_HOME/runtime/remotion"
npx tsc --noEmit -p .
npx remotion compositions src/index.ts | grep Ch1Pretrain
cd "$ART_HOME" && ./art scene-index

# ── 4. audio = the clock ───────────────────────────────────────────────────
python3 runtime/scripts/generate_audio_kokoro.py "$REEL"

# ── 5. the guess pause — LAST audio step, never before step 4 ──────────────
#     generate_audio_kokoro.py regenerates EVERY beat unconditionally and would
#     destroy this; mp3/timings.json is a cache it trusts over the real files.
ffmpeg -y -i "$REEL/mp3/beat-B00.mp3" -af "apad=pad_dur=3.5" \
       -c:a libmp3lame -q:a 2 "$REEL/mp3/_b00.mp3"
mv "$REEL/mp3/_b00.mp3" "$REEL/mp3/beat-B00.mp3"
#     then rewrite beat_sheet actual_duration_s + durationS + mp3/timings.json
#     from ONE mutagen measurement of the files on disk. Do not re-run step 4.

# ── 6. render, compile, gate ───────────────────────────────────────────────
python3 runtime/scripts/remotion_scenes.py "$REEL" --force
./art run   "$REEL"                          # GATE F/L/V
./art final "$REEL"                          # verified master

# ── 7. captions from the word clock ────────────────────────────────────────
python3 runtime/scripts/align.py "$REEL" --model base
python3 "$REEL/make_captions.py"

# ── 8. report the REAL duration, never an estimate from the beat sheet ─────
ffprobe -v error -show_entries format=duration -of csv=p=0 "$REEL/<slug>.mp4"
```

## Ordering rule this revision established

Audio generation is **destructive and unconditional**. Any hand-applied audio edit — the
guess pause here — is the last audio step, and the clock (`beat_sheet.json`,
`durationS`, `mp3/timings.json`) is written once from a single measurement afterwards.
Re-running step 4 silently reverts the pause and shortens the film by 3.5s.
