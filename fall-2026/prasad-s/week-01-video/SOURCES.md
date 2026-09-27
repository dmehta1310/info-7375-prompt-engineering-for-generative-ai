# SOURCES — Less Room to Wander

## Evidence (this folder)
- `evidence/temp-1.0.json`, `evidence/temp-0.5.json`: probabilities and counts; logits [1, 2, 3], seed 7, n = 1000. Re-verified against a fresh run on 2026-09-26.
- `evidence/ANALYSIS.md`: expected-vs-observed table, spreads, standard-deviation figures, and Prasad's prediction, verdict, reasoning and limitation (quoted verbatim in B05).

## Course material
- `lessons/01-randomness-and-first-prompts/code/main.py`: course reference implementation, unedited. Lines 9–17 (B02) and 19–24 (B07) are shown verbatim. It isn't Prasad's own implementation, and the video labels it as reference code.
- `lessons/01-randomness-and-first-prompts/docs/en.md:27`: "Temperature changes the distribution, not the truth of the answer."

## Toolkit and local additions
- brutalist.art (https://github.com/nikbearbrown/brutalist.art) at revision `6a8380ae169cca81e0633664a65c958f5c12ab4b`, `ai-explainer` free beginner path. Local-only changes to that checkout (10 removed example files and a regenerated `runtime/remotion/package-lock.json`, logged in FRICTIONAL.md) don't affect this reel's scenes. One local change does affect the build: `runtime/scripts/compile.py` was patched so that `./art final` honors `ART_STRICT` the same way `./art run` does (exact diff and rationale in BUILD-LOG.md).
- **Local addition: `tools/kokoro_phoneme_override.py`** (in this folder, not in the toolkit). It regenerates B00 and BOUT audio through kokoro-onnx 0.6.1's `create(..., is_phonemes=True)` so that "Namaste" is said nˌʌməstˈeɪ (espeak default: nˈæmæst) and "Prasad" pɹəsˈɑːd (default: pɹˈæsæd). With the overrides switched off, its output is sample-identical to the toolkit's `generate_audio_kokoro.py`. The narration text and all on-screen text are unchanged.

## Third-party media
- None. Every visual is a Remotion scene rendered from this folder's `beat_sheet.json`; no photos, stock footage, music or sound effects.

## Disclosure
- **Narration:** synthetic, Kokoro `af_bella`, generated locally at $0.00. Disclosed aloud in B00's first sentence and printed on screen on the BOUT outro card. It isn't Prasad's voice, it isn't Bear, and it isn't an official voice.
- **Claude interface:** B00 and BHTF show a Remotion reconstruction of the Claude composer, not a screen recording.
- **Assistance:** Claude Code (Opus 5.5) drafted the beat plan, narration, beat sheet and paperwork and ran the toolkit. Prasad set the question, method and takeaway, wrote ANALYSIS.md, approved the plan, and signed off the narration (PEDAGOGY.md).
- **Not an endorsed or official course video.**
