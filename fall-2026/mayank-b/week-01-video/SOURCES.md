# SOURCES

## What I used
| Item | Use | Licence / terms |
|---|---|---|
| Chapter 1, `01-randomness-and-first-prompts.md` (INFO 7375 course text) | concept, scores [1, 2, 3], the `probabilities()` / `sample()` code, the constructed wrong-answer counterexample, the boundary | course material, used for coursework |
| brutalist.art toolkit (github.com/nikbearbrown/brutalist.art) | pipeline, bookend scenes (ClaudeComposerAsk, BrutalistHesitantWriter, ClaudeVerdictArtifact; the outro is a reel-local copy of ClaudeTitleOutro with a handle prop), compile + QC gates | public course toolkit; no licence file in the repo |
| Kokoro-82M via kokoro-onnx, voice `am_onyx` | narration, generated locally | Apache-2.0 |
| Remotion 4 | rendering | Remotion licence (free for individuals) |
| matplotlib mathtext (via `typeset_math.py`) | equation SVGs | matplotlib licence (PSF-style) |
| faster-whisper (via `align.py`) | word timings only | MIT |
| EB Garamond (bundled in the toolkit) | serif type | SIL Open Font License 1.1 |
| "@Mayank" corner wordmark and outro handle (v7) | channel mark per the skill's LOGO LAW fallback (no logo file → handle as a serif wordmark); replaced the NikBearBrown logo used in v1–v6 | made for this video |
| Python `random` / `math` | sampling and arithmetic | PSF |

No stock footage, no images, no music, no paid services.

## What was made for this video
- `code/run_temperature.py`, `code/build_props.py`, `code/author_sheet.py`
- `remotion-src/TemperatureConcentration.tsx.txt` — seven new scenes (B02–B08); TypeScript stored as .txt, see remotion-src/README.md
- The script, the beat sheet, and all paperwork in this folder

## Constructed vs. real
- **Real, reproducible:** every probability, ratio, count and draw on screen comes from running the
  chapter's code (Python 3.11.16, 2026-09-23) and matches the chapter's published tables.
- **Constructed, and labelled on screen:** the scores [1, 2, 3] ("CONSTRUCTED TOY SCORES"), and the
  B07 answer key ("CONSTRUCTED HYPOTHETICAL · NOT AN OBSERVED CLAUDE ERROR").
- **No Claude responses are shown.** B00's output lines are the program's stdout. The recap page (BVDT)
  is labelled "Recap written by the author, not a Claude response". (The earlier "Your turn" suggested-prompt beat was removed in v6.)

## What Claude contributed
Claude Code (Opus 5.5), working in my terminal and VS Code, 2026-09-21 → 2026-09-25:
- set up and debugged the toolkit (see FRICTIONAL.md)
- read the chapter and proposed the concept shortlist; **I chose the concept**
- reproduced the chapter's numbers and wrote the evidence scripts
- drafted the narration, the beat sheet and the seven Remotion components
- ran the audio, render, compile and visual-QC passes, and fixed the defects they found
- drafted README, SOURCES, FRICTIONAL, CHANGELOG, FACTCHECK and the other paperwork

I reviewed the review cut before submission and am responsible for every claim in the video.
