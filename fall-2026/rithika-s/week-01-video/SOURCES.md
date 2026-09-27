# SOURCES — "The Token That Followed"

INFO 7375 · Week 01 · Chapter 1 · Rithika Sankar Rajeswari

---

## 1. Academic honesty: what is constructed and what is exact

**The example is constructed. The arithmetic is not.**

Invented for teaching, and labelled `CONSTRUCTED EXAMPLE` on screen wherever shown:

- the corpus line **"The moon is made of green cheese"** and its attribution to a
  science-fiction novel — there is no such novel; the sentence is a well-known English
  idiom for an absurd belief, used here as a case where text and truth come apart;
- the four-token vocabulary `rock · cheese · gas · light` — a real model's softmax runs
  over ~10⁵ tokens, not four;
- the four logits `+4.0 · +1.0 · 0.0 · −0.5` — chosen so the probabilities round to
  values that sum to exactly 1.0000, which is a *presentation* choice.

Computed exactly, and asserted in `verify_softmax.py`:

- `exp(z)`, the denominator `Σ exp(z) = 58.9230`;
- the softmax `0.9266 · 0.0461 · 0.0170 · 0.0103`, summing to exactly `1.0000`
  (and `92.7 + 4.6 + 1.7 + 1.0 = 100.0%`);
- the cross-entropy `−ln 0.0461 = 3.0762` nats and the counterfactual `−ln 0.9266 = 0.0762`;
- the identity `L(cheese) − L(rock) = z(rock) − z(cheese) = 3.0`, verified to `1e-12`;
- the gradient `p − y = +0.9266 · −0.9539 · +0.0170 · +0.0103`, summing to `0`.

`verify_softmax.py` exits non-zero if any displayed figure fails to reproduce. It was
run before the build and again after; it passes.

**No claim is made about any real trained model.** The reel says so out loud in beat
B09 and prints it in `metadata.honesty`.

## 2. What Claude contributed

Built with **Claude Opus 5** in Claude Code, driven by the author's prompt and design
constraints (see `BUILD-PROMPT.md`). Specifically, Claude:

- chose the four logits by **searching** a grid of half-integer values for a set whose
  4-dp probabilities sum to exactly 1.0 — 35 candidates qualified, and the cleanest
  (`4.0 / 1.0 / 0.0 / −0.5`) was taken;
- noticed the identity `loss gap = logit gap` falls out of `ln pᵢ − ln pⱼ = zᵢ − zⱼ`
  and made it beat B07's closing strip;
- wrote `verify_softmax.py`, the 13-beat `beat_sheet.json` (narration, `show` blocks,
  scene props), and all eight Remotion components below;
- wrote the narration in the toolkit's Teardown register and, after the first audio
  pass measured 4:13 — over the 4-minute cap — cut ~100 words and regenerated to
  3:42, then re-timed a second time to **3:16** when the brief settled on a ~3:15
  target, trimming only words the frame already carried.

**What Claude did not do:** it did not choose the topic, the persona, the honesty
policy, or the runtime target, and it cannot watch the result. The visual-QC judgment
and the decision to ship are the author's.

## 3. Components written for this reel

All eight are new and are registered in `runtime/remotion/src/Root.tsx` under the
`Ch1-Pretraining` folder. Written because **GATE L** (library-first search) returned a
genuine miss — `./art scenes "softmax probabilities over candidate tokens, logit
scores, next-token prediction"` produced eight leads, none of them a distribution,
logit, loss or gradient scene. Per the skill's own rule, a miss is a design card, not
a licence to slate.

| Component | Role |
|---|---|
| `Ch1Chrome.tsx` | The chassis (`Ch1Stage`): ground, spark line, `CONSTRUCTED EXAMPLE` banner, course bug, safe-area layout, shared timing helpers and primitives |
| `Ch1PretrainCorpus.tsx` | The false corpus line, tokenized; context recedes, `green` accents, the next slot opens |
| `Ch1PretrainLogits.tsx` | Raw logits and `exp(z)`; bars drawn from `exp(z)`, not `z` |
| `Ch1PretrainSoftmax.tsx` | The division, plus a stacked unit bar proving the mass tiles to exactly 1 |
| `Ch1PretrainTarget.tsx` | The one-hot target beside the truth vector the objective never builds, struck through |
| `Ch1PretrainLoss.tsx` | The sum collapsing to one term; the incurred loss beside the counterfactual |
| `Ch1PretrainGradient.tsx` | `p − y` per row with direction arrows; column sums to zero |
| `Ch1PretrainBoundary.tsx` | The falsifiability beat — what this does not establish |
| `Ch1PretrainOutro.tsx` | Title-restate outro for the course channel (see §5) — *not used in the 2026-09-23 cut* |
| `Ch1PretrainHook.tsx` | **New 2026-09-23** — Act 1. The false sentence as plain English, the question, and the guess pause |
| `Ch1PretrainLadder.tsx` | **New 2026-09-23** — Act 2. All five softmax steps in one component, driven by `step` (1..5) |
| `Ch1PretrainContrast.tsx` | **New 2026-09-23** — Act 3. The same model against a true corpus; both target vectors side by side |
| `Ch1PretrainTakeaway.tsx` | **New 2026-09-23** — Act 6. One sentence, plus the title restate and credit rail |

Inherited from the toolkit and used by the **3:16 cut only**: `ClaudeComposerAsk`,
`BrutalistHesitantWriter`, `ClaudeVerdictArtifact`. The 2026-09-23 six-act cut uses no
Claude-interface beats at all — see §7.

## 4. Tools and attribution

| Tool | Version / detail | Role | Cost |
|---|---|---|---|
| **Brutalist toolkit** | `github.com/nikbearbrown/brutalist.art` @ `ba2d0e0` | Beat-sheet pipeline, Remotion chassis, compile/QC gates, brand laws | free |
| **Kokoro TTS** | Kokoro-82M via `kokoro-onnx`, `kokoro-v1.0.onnx` local | All narration, voice `af_bella` | $0.00 |
| **Remotion** | 4.x | All 13 beat scenes, rendered at `--scale=2` | free |
| **Claude Opus 5** | Claude Code | Authoring and build driving (§2) | — |
| **faster-whisper** | `base` model, local | Word-level caption timing via `align.py` (13/13 beats, 0 fallback) | free |
| **ffmpeg** | 9.0.1 (Homebrew) | Duration conformance, mux, QC frame sampling | free |
| **Python** | 3.12.12 | Pipeline scripts, `verify_softmax.py`, `build_beat_sheet.py`, `make_captions.py` | free |
| **ffmpeg `apad`** | 9.0.1 | The hook's 3.5s guess pause, appended to the narration so the hold is part of the measured clock | free |
| **mutagen** | 1.47 | Re-measuring the padded mp3 — the same library the pipeline measures with | free |

The Brutalist toolkit is Nik Bear Brown's; the `ai-explainer` skill's laws
(COLD OPEN, EXECUTIVE-SUMMARY, ILLUSTRATE, SHOW-DON'T-TELL, SPARK-LINE, HANDOFF,
OUTRO, FILL-THE-CANVAS, VISUAL QC, GATE L, GATE P) govern this reel and are quoted
where they shaped a decision. The Claude palette (`#FAF9F5` / `#3D3929` / `#D97757`)
is a fidelity replication of the Claude desktop app and is used unretinted per
`CLAUDE-BRAND.md`.

`BrutalistHesitantWriter`, used unmodified for beat B01, carries its own upstream
attribution in its header: it is a rewrite of a brik/base44 canvas component
(`typing-animation-mnzzraks`), author unknown, credited in the toolkit's own SOURCES.

**No ElevenLabs.** The toolkit removed it permanently (commit `7ee2da6`); nothing here
calls a paid API.

## 5. Documented deviations from the default skill

1. **Channel `claude-sasha`, voice `af_bella`.** The skill's working default is
   `claude-liam` / `am_onyx`. The assignment specifies the persona and narrator name
   **Sasha**, so a new channel key was used. No Kokoro voice is named "Sasha" — the
   persona is Sasha, the voice is `af_bella` ("Bella"), one of the two voices the
   toolkit documents and reports green in `./art doctor`. The IN-FOR-BEAR LAW does not
   apply: Sasha is not standing in for Bear on Bear's channel, and does not claim to be.
2. **Custom outro.** `ClaudeTitleOutro` hardcodes the `@NikBearBrown` handle with no
   prop override, and `OUTRO-LOCK.md` scopes it to claude-liam reels — "Other channels
   use their own outro components — never this one." `Ch1PretrainOutro` is this
   channel's own, keeping the law's substance: exact title restate, poster-plain serif,
   terracotta period, handle beneath. No mascot, since the 18 crisp-safe mascots are
   @NikBearBrown channel identity.
3. **Folder chip** reads `INFO 7375 · CH 1` rather than a YouTube handle, this being
   coursework rather than a channel upload.
4. **Submission path.** Built into `fall-2025/rithika-s/week-01-video/` as instructed.
   Note for the grader: the course repo currently contains `fall-2026/`, not
   `fall-2025/`, and its student folders follow the `firstname-l` convention that
   `rithika-s` matches. Flagged rather than silently relocated.

## 6. Corrections applied (DOUBLE-CHECK LAW)

- **"40× harder" cut.** A draft line said being right was penalized "forty times
  harder." The ratio `3.0762 / 0.0762 ≈ 40.4` is real but rhetorical — a ratio of
  log-losses is not a meaningful quantity. Replaced with the exact, defensible
  statement: being right costs **exactly three more nats**, which is the logit gap.
- **No model version claims.** Nothing asserts how any shipped model was trained, which
  keeps the reel from dating (DOUBLE-CHECK LAW: strip what will drift).
- **Probability presentation.** The probabilities are displayed at 4 dp *because* that
  is where this logit set sums to exactly 1.0; the reel does not claim softmax outputs
  are "clean numbers" in general.


## 7. The 2026-09-23 revision — what changed and why

**Runtime floor.** Raised to 4:00 by a live-class instruction from the professor,
overriding the written 2–4 minute syllabus target. There is no written source for it;
`FRICTIONAL.md` § Revision — 2026-09-23 records it, with the class date left as a
placeholder for the author rather than invented.

**No Claude interface in this cut.** The standing constraint is that any Claude response
shown must be a real one, actually obtained and dated. The previous cut's cold open
displayed four RESULT lines inside `ClaudeComposerAsk` that I had written as a summary of
the build — they read as a Claude reply and were not one. Rather than stage a response or
present `verify_softmax.py` output as chat, this cut contains no Claude UI. Consequence:
COLD OPEN LAW, ASK→RESULT LAW and HANDOFF LAW do not apply to this reel.

**Numbers are now generated, not transcribed.** `verify_softmax.py --emit` writes
`softmax_values.json`; `build_beat_sheet.py` builds every scene prop from it. No figure on
screen is hand-typed, which closes the one gap the earlier cut had — the script could be
right while a number was mistyped into a prop. The script now also proves the five-step
pipeline the video actually shows, including the max-subtraction step, and asserts that
max-subtraction is identical to the naive softmax to 1e-12.

**What Claude contributed in this revision:** the six-act restructure into 12 beats, the
four new components, `build_beat_sheet.py`, the beginner-register narration, and the
diagnosis of the audio-regeneration and `timings.json` cache behaviours in
`FRICTIONAL.md` #22–#24. **What Claude did not do:** set the runtime floor, choose the
six-act structure (both came from the brief), or judge the result on screen.
