# Shifted, Not Changed

**Week 1 Explainer Video — Explain One Concept from Chapter 1**

| | |
|---|---|
| **Student** | Suketh Produtoor |
| **Course** | INFO 7375 — Prompt Engineering for Generative AI |
| **Concept** | Chapter 1, Part 2 — **the max-subtraction**: why `probabilities()` subtracts the largest score before exponentiating |
| **Why this one** | It is the smallest idea in the chapter — one subtraction — and the only candidate that pairs a provable core (the factor cancels exactly) with a failure you can actually run (the raw exponential raises `OverflowError`), which let me explain it completely inside three minutes instead of touring the chapter. |
| **Runtime** | **3:16** (195.72 s of narration; the file probes at 196.0 s), 11 beats, 1920×1080 |
| **Final file** | `Produtoor_Suketh_INFO7375_Week01_Video.zip` → **Canvas**. The MP4 is not committed here — see *Where the video is*. |
| **Audience** | A classmate who has read Chapter 1 Part 1 and can follow arithmetic, but has not run the code yet |
| **Status** | Local final — **not published**; no YouTube upload, per the brief. Reviewed by Claude frame by frame, and **watched by me on 2026-09-25** — the one change I asked for is in (`REVIEW.md` Round 10). |
| **Who did what** | Claude (Claude Code) wrote the scripts, scenes, beat sheet and these documents; I directed it and made the decisions listed in [`SOURCES.md`](SOURCES.md) §4. |
| **Narration** | **Synthetic** — Kokoro `am_onyx`, generated locally. Not my voice, not the instructor's. See [`SOURCES.md`](SOURCES.md) §1. |
| **Cost** | $0.00 — free pipeline only, no API key, no paid service |

---

## Where the video is

**The MP4 is not in this repository.** It is submitted on Canvas as
`Produtoor_Suketh_INFO7375_Week01_Video.zip` (1920×1080, h264+aac, 3:16, 9.1 MB).

This folder carries everything else — beat sheet, evidence scripts and their recorded
runs, fact-check, build prompt, review log, Frictional log, and a description of the
Remotion source (`components/README.md`; the `.tsx` itself is not vendored). The split is
deliberate: [`youtube/README.md`](../../../youtube/README.md) says *"Large media is not
committed by default"*, and everything here is text a reviewer can read, run and diff.
`captions/*.srt` is included so the spoken content is searchable without the video.

---

## What the video argues

Subtracting the largest score rewrites **every intermediate value** in the softmax and
changes **nothing** about the distribution it returns. The film shows both halves of that
sentence, then refuses the slogan usually attached to it.

1. **B02 — why the subtraction exists, and that it works.** `math.exp(1000)` does not
   return a huge number; it raises `OverflowError: math range error`. float64 stops at
   `1.797693e+308` and the exponential crosses that at ≈ 709.78. The beat then holds the
   break and its resolution **side by side**: the same `[1000, 1000]`, shifted, returns
   `[0.5, 0.5]` — Chapter 1's own canonical test for this choice.
2. **B03 — the mechanism, performed.** `[1, 2, 3]` → peak 3 → `[-2, -1, 0]` → weights
   `0.1353…, 0.3679…, 1.0` → total `1.5032147244` → `0.0900…, 0.2447…, 0.6652…`. Four
   columns, revealed one at a time. The largest weight is **exactly** 1, which is why the
   denominator can never fall below 1.
3. **B04 — why it is allowed.** `exp(−m/T)` is a common factor top and bottom. It cancels
   on screen. Algebra, not a numerical trick.
4. **B06 — the honest receipt.** I expected the shifted and direct paths to return
   identical floats. They differ by `1.1102230246251565e-16` — exactly 2⁻⁵³, **half** of
   Python's `sys.float_info.epsilon`: the two answers are adjacent floats, one step apart,
   in two digit positions out of fifty-three. Those two digits are then isolated on screen
   with a `1 ULP` marker between each pair, and held. Identical in algebra; in floating point
   merely indistinguishable.
5. **B07 — what this does *not* establish.** `probabilities([0, -800])` returns
   `[1.0, 0.0]` — an **exact zero** for an outcome whose true share is ≈ `1e-348`. The
   subtraction protects the large end and does nothing for the small one. And the cliff
   is not a magic number: it is `−1075 · ln 2 = −745.133219102`, so `−746` is simply the
   first integer past it. binary64's smallest subnormal is 2⁻¹⁰⁷⁴, and under
   round-to-nearest anything below half of that rounds to zero. Bisecting the real
   boundary agrees to **nine decimal places**.

**The claim the film ends on:** this code is **overflow-safe**, not *numerically stable*.
Those are different claims and only one of them was tested — which is Chapter 1's own
instruction to keep the tested claim narrower than the slogan.

## Every number is reproducible

No figure on screen was typed in by hand. Every figure the film renders is supplied as a **prop** from `beat_sheet.json`. The same values also appear as Zod schema defaults inside each component so a composition can be previewed standalone in Remotion Studio; the beat sheet overrides every one of them at render time. So a wrong figure is fixed in the beat sheet, never in the component. Every prop value was read out of
one recorded run of the course's own reference implementation, imported unmodified:

```bash
python3 evidence/verify_claims.py
```

That prints all sixteen fact-checked claims beside the values the reference code actually
returns. `evidence/run-output.txt` is the recorded output every prop was taken from.
Add `--json` for the machine-readable form.

The claims are also **regression-tested**, so a drifting figure fails loudly instead of
quietly disagreeing with the video:

```bash
python3 evidence/boundary_analysis.py        # the derivation and the remedy
python3 -m unittest discover -s evidence -v  # 29 tests
python3 evidence/mutation_check.py           # do those tests bite? 4/4 mutations caught
python3 evidence/gate_t_typecheck.py         # GATE T: contrast, type floor, figure wiring
python3 evidence/cross_check.py              # same figures under every python3.N on PATH
python3 evidence/doc_consistency.py          # do the 11 documents still match the artifact?
```

`cross_check.py` answers a question the paperwork originally conceded. Every figure —
including the seeded counts and the 2⁻⁵³ difference — is **byte-identical
across CPython 3.10.19, 3.12.7, 3.13.3 and 3.14.6**, and 3.14.6 is the interpreter
Chapter 1 records *its* run on. Scope, stated at the size of the evidence: four
interpreters, **one** platform and architecture. IEEE-754 says this should hold
elsewhere; "should" is not "was measured".

That last one matters more than the green checkmark. A passing suite is a claim *about*
evidence; `mutation_check.py` is what turns it into evidence. Running it is also what
caught a false statement I had written about my own tests — see [`SOURCES.md`](SOURCES.md)
§5.5.

Each test names the beat it defends — `TestB07TheBoundary::test_the_cliff_sits_between_745_and_746`
is the one guarding the film's closing claim. Both scripts locate the course reference
implementation by walking up from their own location (or via `INFO7375_REF`), so they run
from this folder or from the posted `fall-2026/suketh-p/week-01-video/` folder without edits.

## Contents

| Path | What it is |
|---|---|
| `README.md` | This file |
| `beat_sheet.json` | The reviewed narration + visual plan. Measured `actual_duration_s` per beat. |
| `captions/*.srt` | 113 cues, word-aligned. The MP4 is the Canvas deliverable. |
| `evidence/verify_claims.py` | Regenerates every on-screen number from the course reference code |
| `evidence/run-output.txt` | The recorded run those numbers came from |
| `evidence/boundary_analysis.py` | Derives the cliff in closed form; measures what it costs; demonstrates the log-space remedy |
| `evidence/test_verify_claims.py` | 29 tests that fail if any on-screen number drifts — one reads the film's on-screen text against the recorded run |
| `evidence/mutation_check.py` | Chapter 1 Assessment 10 — perturbs the code to prove those 29 tests actually bite (4/4 caught) |
| `evidence/gate_t_typecheck.py` | **Implements GATE T**, which the toolkit declares mandatory but does not ship. WCAG contrast, type floor, word budget, figure-wiring → `TYPECHECK.md` |
| `evidence/cross_check.py` | Runs every displayed figure under **every `python3.N` on PATH** and reports whether they agree |
| `evidence/doc_consistency.py` | Derives the facts live and asserts the current-state docs still agree. Dated logs are exempt by design; their headers are checked instead |
| `evidence/make_srt.py` | Builds the caption sidecar from the toolkit's aligned word clock |
| `TYPECHECK.md` | GATE T result: 0 FAIL · 1 WARN · 29 PASS |
| `components/README.md` | Why the seven reel-local Remotion scenes (written by Claude) are not vendored here, where they live, and excerpts cut from the real file |
| `REFINEMENTS.md` | **Every refinement from first draft to submission, on one page, mapped to the rubric** — start here |
| `FACTCHECK.md` | 21 rows · verdict · source · fix |
| `SOURCES.md` | Sources, third-party licences, synthetic-narration disclosure, what Claude contributed |
| `FRICTIONAL.md` | Dated log of the build sessions, organised by Claude — install failures, the boundary finding, doctrine/tooling gaps, and the errors found before submitting — plus my `[MINE]` sections |
| `CHECKS-REPORT.md` | PROOF GATE: 11 SHOW / 0 HOLD / 0 PUNT, teaching-arc and law compliance |
| `SHOTLIST.md` | Typed work order, lane histogram, typing budget |
| `PROMPTS.md` | The three on-screen prompts verbatim (none was ever sent); records that there are no open slots |
| `BUILD-PROMPT.md` | The single paste-ready prompt that rebuilds the film end to end |
| `REVIEW.md` | Timestamped review rounds of the rendered cut (Claude's); my watch-through and requested change go in its `[MINE]` section |

Generated artifacts — `mp3/`, `media/`, `clips/`, `_qc/`, `pantry/` — are **not committed**.
All are reproducible from `beat_sheet.json` via `BUILD-PROMPT.md`.

## How to rebuild the video from this folder

Requires an external [`brutalist.art`](https://github.com/nikbearbrown/brutalist.art)
checkout — the media engine stays outside this repository, per `AGENTS.md`. The seven
Remotion components this film uses live in that checkout at
`runtime/remotion/src/ShiftedNotChanged.tsx` and are registered in `Root.tsx` under the
folder `ShiftedNotChanged`.

```bash
# 0. Environment that actually works on macOS/arm64 (see FRICTIONAL.md for the four
#    failures this recipe routes around)
brew install pkgconf                  # pycairo needs it; its absence aborts the whole pip run
cd /path/to/brutalist.art
python3.12 -m venv .venv              # NOT 3.14 — manim<0.19 has no build for it
source .venv/bin/activate
pip install "kokoro-onnx>=0.4" "mutagen>=1.47,<1.48" "Pillow>=10.2,<11" \
            "numpy>=2.0.2" "faster-whisper>=1.0,<2"
(cd runtime/remotion && npm install)
./setup                               # expect Manim ❌ (blocked, unused); everything else ✅

# 1. Verify the numbers before trusting the film
python3 /path/to/course/youtube/week-01-shifted-not-changed/evidence/verify_claims.py

# 2. Audio is the master clock — regenerate and re-measure
REEL="/path/to/course/youtube/week-01-shifted-not-changed"
python3 runtime/scripts/generate_audio_kokoro.py "$REEL"

# 3. Review cut, then what still needs filling (expect: nothing)
./art run  "$REEL"
./art todo "$REEL"

# 4. The 1080p master
./art final "$REEL" --height 1080 --out "$REEL/final"
```

`--height 1080` is explicit: the toolkit defaults to 4K, and the course prerequisite
chooses a 1080p local master. Never publishes — the file stays in `final/`.

If you change any narration, **regenerate audio before recompiling**. Timing is never
patched by hand; the mp3 durations are the clock.

## Credits and assistance

- **Starting material:** Chapter 1 and `lessons/01-randomness-and-first-prompts/code/main.py`
  by Nik Bear Brown (INFO 7375). The reference implementation is imported, never modified.
- **Media toolkit:** [`brutalist.art`](https://github.com/nikbearbrown/brutalist.art) @ `ba2d0e0`.
- **AI assistance:** Claude Opus 5 via Claude Code (2026-09-15 to 2026-09-24), and Claude
  Opus 5.5 for the final pass on 2026-09-24 — read the doctrine, diagnosed the install,
  wrote every evidence script and Remotion component, authored the beat sheet and these
  documents, and ran the build. It also found the underflow boundary the film ends on, and,
  in the final audit, the errors in its own earlier work (`SOURCES.md` §5.16–§5.20). Full
  breakdown in [`SOURCES.md`](SOURCES.md) §4 and [`FRICTIONAL.md`](FRICTIONAL.md).
- **Voice:** Kokoro-82M `am_onyx`, local. Disclosed on the outro card.
- **Type:** EB Garamond (SIL OFL 1.1).
- Not affiliated with or endorsed by the @NikBearBrown channel, Northeastern, or Anthropic.
