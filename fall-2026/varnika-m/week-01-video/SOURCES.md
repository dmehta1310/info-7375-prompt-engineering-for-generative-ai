# Sources

**Video:** Three Scores Are Not Yet Three Chances
**Author:** Varnika M · INFO 7375 · Week 01
**Date:** 2026-09-26

## 1. Disclosures

**Narration.** The narration is a synthetic voice (Kokoro `am_onyx`), generated locally with the
Brutalist toolkit. It is not my voice or any real person's. No voice cloning or paid service was used.
The end card of the video states this as well.

**Interface screens.** The opening screen (B00) and the "Your turn" screen (B09) are Claude-style
interface graphics drawn by the toolkit. They are not screenshots and do not show Claude replies.
B00 is labelled "Reconstructed interface · not a Claude reply", and the numbers it shows are the
real output of `main.py`. The model name visible in that graphic is part of the toolkit's design;
no Claude model was called to produce any content in the video.

## 2. Sources used

| Source | Used for |
|---|---|
| Chapter 1, Part 2, "Three scores are not yet three chances" (`chapters/01-randomness-and-first-prompts.md`) | The concept, the two rules for probabilities, and the hypothetical answer key in B07 |
| Lesson code `probabilities()` (`lessons/01-randomness-and-first-prompts/code/main.py`) | Every number in the video; the code excerpt in B04 (lines 14–17) |
| My run of `main.py`, Python 3.12.14, course commit `24f4af3` | Output `[0.0900, 0.2447, 0.6652]`, saved in `evidence/main_py_output.txt` |
| Brutalist toolkit, revision `6a8380ae169cca81e0633664a65c958f5c12ab4b` (https://github.com/nikbearbrown/brutalist.art) | Narration audio, Claude-style scenes, video assembly and quality checks. Used unmodified. |

## 3. What I made

- `beat_sheet.json`: the plan for all 11 beats, including narration
- `scenes.py`: the animated scenes B02–B07 and the end card (B10). Every number is computed by importing `main.py`.
- `evidence/`: the saved `main.py` output and all intermediate steps
- `FACTCHECK.md`: each claim in the video with its source
- The rendered video

**Constructed examples** (labelled on screen as constructed):
- Scores `[-1, 2, 3]` (B03, B06), used to show that dividing by the total can give a negative chance. The results for these scores are still computed by `main.py`.
- "Answer key: option A is correct" (B07), a hypothetical adapted from Chapter 1.

## 4. Contributions

**Me:** chose the concept, reviewed and approved the narration, installed Homebrew, and reviewed the
rendered video. After watching the review cut I decided to: disclose the synthetic voice here instead
of in the narration, relabel the options A, B, C so the narration matches the screen, keep the
Claude-style opening screen, and shorten the end-card voice note.

**Claude Code (NEU-provisioned):** explained the assignment and suggested candidate concepts; set up
and debugged the Brutalist toolkit; ran `main.py` and verified the numbers; drafted the narration;
wrote `beat_sheet.json`, `scenes.py`, `FACTCHECK.md`, `README.md`, `BUILD-PROMPT.md` and the
supporting files; built the video, checked it frame by frame, and made the changes I requested.

No conversation transcripts are included.

## 5. Third-party software and licences

| Software / asset | Licence |
|---|---|
| Manim Community 0.18.1 | MIT |
| Remotion | Remotion License (free for individuals) |
| EB Garamond font | SIL Open Font License |
| Kokoro-82M voice model, `kokoro-onnx` 0.6.1 | Not listed in the installed package; not verified |
| Brutalist toolkit | No licence file in the repository; not verified |

No stock footage, music, or images are used.
