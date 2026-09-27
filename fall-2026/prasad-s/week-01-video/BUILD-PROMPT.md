# BUILD-PROMPT — Less Room to Wander

This film was **not** built from one prompt. It was built over two days (2026-09-25 and 2026-09-26) in one Claude Code (Opus 5.5) session, as a series of instructions from Prasad, each one reviewed before the next. Below is that sequence, summarized honestly, including the dead ends. FRICTIONAL.md has the detail and evidence for each step.

Normal permissions were used throughout. The skill's suggestion to run under `--dangerously-skip-permissions` was not followed; the course prerequisite forbids it.

## The actual sequence

1. **Environment (2026-09-25).**
   - Clone `brutalist.art` as a sibling of the course repo, create a venv, run `./setup --install` and `./setup`, and report the readiness table and the revision.
   - Setup first failed at the toolkit's ElevenLabs guard. Ten unused example files were removed from the local clone; the guard's code was not edited.
   - Python 3.9 couldn't install the voice engine, so the venv was rebuilt on Homebrew Python 3.11, with Node 20, ffmpeg, pkgconf, cairo and pango added.
   - Result: 6/7 features ready (equation beats blocked, and not used here).
2. **Evidence.**
   - Run the unedited lesson 01 `main.py` as shipped (temperature 1.0).
   - Read the source to find how to change temperature: there's no CLI or env option, so the unedited `probabilities()` / `sample()` were called with `temperature=0.5`, keeping seed 7 and n = 1000.
   - Prasad wrote `evidence/ANALYSIS.md` (prediction, result, reasoning, limitation). The JSON files were checked against a fresh run.
3. **Pipeline check.**
   - `./art smoke` fails at this revision (its `_smoke` slug is rejected by the toolkit's own filename check).
   - A worked example was rendered in a scratch folder to prove audio and video generation work; Prasad spot-checked it.
4. **Plan.**
   - Read ai-explainer SKILL.md in full plus its required docs, and search the scene library.
   - Claude Code proposed 11 beats, the voice choice (`af_bella` instead of the Liam/Bear `am_onyx`), and departures from the skill defaults (no `@NikBearBrown` branding or persona).
   - Prasad approved with changes: B05 timing wording, the greeting, the title.
5. **Narration sign-off.** `beat_sheet.json` and `PEDAGOGY.md` were drafted; Prasad checked each line against the evidence and signed PEDAGOGY.md on 2026-09-26.
6. **Audio and paperwork.**
   - Kokoro `af_bella` audio: 237 s.
   - Table rows re-timed to faster-whisper word timestamps.
   - FACTCHECK / SHOTLIST / PROMPTS / SOURCES / CHECKS-REPORT written.
7. **Review cuts and fixes** (three render rounds, with frames inspected by eye each time):
   - **Renderer limits found:** fixed-length compositions (`ExecutedData` is capped at 15 s, and the writer defaulted to 20.2 s), and the writer only fires single-word triggers.
   - **Decisions (Prasad):** table rows kept inside 15 s; B01 corrected with "accurate" → "tightly bunched"; FormACard kept for B05 and BOUT, with the `ART_STRICT=0` exception logged in BUILD-LOG.md.
   - **Rejected:** `WantQuote` (it hardcodes a false "Data: Anthropic…" credit) and `largeText` on B07 (it clipped the code).
8. **Pronunciation.**
   - Found that espeak mispronounces "Namaste" and "Prasad", and that `kokoro-onnx` accepts phonemes.
   - Added `tools/kokoro_phoneme_override.py`; with overrides off it is sample-identical to the stock script.
   - Re-rendered only B00 and BOUT and confirmed no other file changed.
   - Prasad watched the review cut in full, with sound, after the pronunciation fix, and approved it.
9. **Final.**
   - Paperwork revised to quote the signed narration verbatim.
   - The first `./art final` was blocked by GATE T (3 FAILs): B02/B07 card-clip false positives (fixed by removing the brand label), and B03 terracotta text contrast (B03 moved to an ExecutedData table; the probability-mode version overflowed the frame).
   - Then `./art final --height 1080 --out final/` failed a second time, for a different reason: the final compile (`compile.py`) ran GATE V through its own hardcoded check that ignored `ART_STRICT=0`. The four B05/BOUT underfill MAJORs, already approved as an exception on the review path, refused it. A first patch passed `--lenient` but still treated the checker's warnings-only exit code 1 as failure. The corrected local patch mirrors `run.sh` (`--lenient` under `ART_STRICT=0`; fail only on exit ≥ 2); BUILD-LOG.md has the exact diff.
   - `ART_STRICT=0 ./art final --height 1080 --out final/` then exited 0 and wrote `final/less-room-to-wander.mp4`.

## To rebuild this exact cut

From the `brutalist.art` checkout at revision `6a8380ae169cca81e0633664a65c958f5c12ab4b`, with its venv active and Node 20 on PATH, and `REEL` = this folder:

```bash
python3 runtime/scripts/generate_audio_kokoro.py "$REEL"
python3 "$REEL/tools/kokoro_phoneme_override.py" "$REEL" --only B00 BOUT
ART_STRICT=0 ./art run "$REEL" --height 1080
ART_STRICT=0 ./art final "$REEL" --height 1080 --out "$REEL/final"   # needs the local compile.py patch (BUILD-LOG.md)
```

`ART_STRICT=0` applies only to the B05/BOUT underfill exception in BUILD-LOG.md. Then inspect `_qc/REPORT.md` and the frames, and watch the whole cut with sound. No step uses a paid service or publishes anything.
