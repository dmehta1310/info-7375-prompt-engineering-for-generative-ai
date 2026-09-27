# Final Checks Report

Audit basis: the 25-point Week 1 Canvas brief supplied by the student. That brief explicitly supersedes the general syllabus wording for Week 1.

## Required deliverables

| Requirement | Evidence | Status |
|---|---|---|
| Correct ZIP name | `Nikam_Siddhesh_INFO7375_Week01_Video.zip` | PASS |
| Correct GitHub folder structure | `fall-2026/siddhesh-n/week-01-video/` | PASS locally; remote push still required |
| `README.md` with name, concept, why, runtime, rebuild | `README.md` | PASS |
| Rendered MP4 | 1920×1080 H.264 + AAC, 192.81 seconds | PASS |
| Reviewed narration and visual plan | `beat_sheet.json`, eight beats, measured audio | PASS |
| Rebuild prompts and commands | `BUILD-PROMPT.md` | PASS |
| Sources, licences, AI contribution | `SOURCES.md` | PASS |
| Dated Frictional entries | `FRICTIONAL.md`, three specific entries following the seven prompts | PASS |
| GitHub folder link and final remote hash in Canvas | Account-specific external action | PENDING |
| Caches, credentials, private transcripts omitted | ZIP manifest and `.gitignore` | PASS |

## Explanation rubric — 15 points

| Criterion | Evidence | Status |
|---|---|---|
| Correct and defensible concept | Chapter derivation, official program/test, `FACTCHECK.md`, `DEFENSE-NOTES.md` | PASS |
| Mechanism is shown | Animated shift, weights, normalization, official test, and factor cancellation | PASS |
| Real and reproducible numbers | Actual `main.py` output plus `softmax_demo.py`; all six course tests pass | PASS |
| One limitation named | Final beat separates supported and unsupported claims | PASS |

## Other rubric components

| Component | Status |
|---|---|
| Frictional — 2.5 | Content prepared and traceable; grading remains instructor judgment |
| Matching GitHub post — 2.5 | Pending the student's remote upload and Canvas link/hash |
| Relative Quartile — 5 | Cannot be guaranteed before cohort review; the artifact provides specificity, execution evidence, revision history, usability, and honest boundaries |

## Technical validation

- Course reference tests: **6/6 passed**.
- Local evidence output exactly matches `code/softmax_output.txt`.
- `beat_sheet.json`: valid JSON.
- Python source: compiles successfully.
- Video: complete decode with no FFmpeg error.
- Captions: 45 timed SRT cues.
- Runtime: **192.81 seconds**, inside 2–4 minutes.
