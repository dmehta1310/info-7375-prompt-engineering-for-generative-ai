# Final Checks Report

Audit basis: the 25-point Week 1 Canvas brief supplied by the student. That brief supersedes the general syllabus wording for Week 1.

## Required deliverables

| Requirement | Evidence | Status |
|---|---|---|
| Correct ZIP name | `Gaikar_Anisha_INFO7375_Week01_Video.zip` | PASS |
| Correct GitHub folder structure | `fall-2026/anisha-g/week-01-video/` | PASS locally; remote push still required |
| `README.md` with name, concept, why, runtime, rebuild | `README.md` | PASS |
| Rendered MP4 | 1920×1080 H.264 + AAC, 193.02 seconds | PASS |
| Reviewed narration and visual plan | `beat_sheet.json`, eight measured beats | PASS |
| Rebuild prompts and commands | `BUILD-PROMPT.md` | PASS |
| Sources, licences, AI contribution | `SOURCES.md` | PASS |
| Dated Frictional entries | `FRICTIONAL.md`, three specific entries following the seven prompts | PASS |
| GitHub folder link and final remote hash in Canvas | Account-specific external action | PENDING |
| Caches, credentials, private transcripts omitted | ZIP manifest and `.gitignore` | PASS |

## Explanation rubric — 15 points

| Criterion | Evidence | Status |
|---|---|---|
| Correct and defensible concept | Course chapter, implementation, test, `FACTCHECK.md`, `DEFENSE-NOTES.md` | PASS |
| Mechanism is shown | Input pipeline, paired rerun, changed-seed bars, official test, boundary panel | PASS |
| Real and reproducible numbers | Unmodified course output plus `seed_demo.py`; 3/3 local checks and 6/6 course tests pass | PASS |
| One limitation named | Final two beats distinguish replayability from truth and cross-version guarantees | PASS |

## Other rubric components

| Component | Status |
|---|---|
| Frictional — 2.5 | Content prepared and traceable; grading remains instructor judgment |
| Matching GitHub post — 2.5 | Pending the student's remote upload and Canvas link/hash |
| Relative Quartile — 5 | Cannot be guaranteed before group review; the artifact emphasizes specificity, evidence, revision, usability, and honest boundaries |

## Technical validation

- Course reference tests: **6/6 passed**.
- Local evidence checks: **3/3 passed**.
- `beat_sheet.json`: valid JSON.
- Python source: compiles successfully.
- Video: complete decode with no FFmpeg error.
- Runtime: **193.02 seconds**, inside 2–4 minutes.
- Resolution/codecs: **1920×1080 H.264 + AAC**.
