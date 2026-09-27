# SHOTLIST — "The Token That Followed"

The typed work order for the **2026-09-23 six-act cut**. Every slot is filled by the
pipeline — no open slots, no pantry requests, no slates — because every beat is a
deterministic Remotion scene rather than found media.

Total: **12 beats · 253.86s (4:13.86)**. Durations are MEASURED from
the narration MP3s, never authored.

| Beat | Act | Duration | Scene | Lane / source | New visual element |
|---|---|---|---|---|---|
| B00 | HOOK | 14.45s | `Ch1PretrainHook` | REMOTION / own | The false claim, as plain English |
| B01 | MECHANISM | 20.57s | `Ch1PretrainCorpus` | REMOTION / own | Text → tokens → the next-token question |
| B02 | MECHANISM | 23.28s | `Ch1PretrainTarget` | REMOTION / own | The answer key: one on cheese, zero on rock |
| B03 | MECHANISM | 20.04s | `Ch1PretrainLadder` step 1 | REMOTION / own | Step 1 — the raw scores |
| B04 | MECHANISM | 22.22s | `Ch1PretrainLadder` step 2 | REMOTION / own | Step 2 — subtract the largest score |
| B05 | MECHANISM | 21.77s | `Ch1PretrainLadder` step 3 | REMOTION / own | Step 3 — exponentiate |
| B06 | MECHANISM | 20.62s | `Ch1PretrainLadder` step 4 | REMOTION / own | Step 4 — divide by the sum |
| B07 | MECHANISM | 21.77s | `Ch1PretrainLadder` step 5 | REMOTION / own | Step 5 — the probabilities, summing to exactly 1 |
| B08 | CONTRAST | 25.44s | `Ch1PretrainContrast` | REMOTION / own | Same model, two corpora, two answer keys |
| B09 | LOSS | 20.33s | `Ch1PretrainLoss` | REMOTION / own | The penalty reads one slot |
| B10 | BOUNDARY | 34.06s | `Ch1PretrainBoundary` | REMOTION / own | What this does not establish |
| B11 | TAKEAWAY | 9.31s | `Ch1PretrainTakeaway` | REMOTION / own | One sentence, no new claims |

## Act budget

| Act | Beats | Measured | Share |
|---|---|---|---|
| HOOK | B00 | 14.45s | 6% |
| MECHANISM | B01, B02, B03, B04, B05, B06, B07 | 150.27s | 59% |
| CONTRAST | B08 | 25.44s | 10% |
| LOSS | B09 | 20.33s | 8% |
| BOUNDARY | B10 | 34.06s | 13% |
| TAKEAWAY | B11 | 9.31s | 4% |

Act 2 carries 59% of the film deliberately: it is the act the brief asks to slow down, and
it is the only place a beginner meets a new idea. See `FRICTIONAL.md` #21 for why the
brief's per-act ranges could not be met literally.

## Lane histogram

| Lane | Beats | Note |
|---|---|---|
| Remotion — `Ch1Pretrain*` (all new or adapted) | B00–B11 | every beat; the chassis is `Ch1Chrome` |
| Remotion — inherited Claude chrome | — | **none.** This cut shows no Claude interface (`FRICTIONAL.md` #25) |
| Manim | — | none: every figure is a table, a vector or a distribution, which Remotion types better |
| Vox / pantry stills | — | none, and none requested |
| Slates | — | **zero** |

## Per-beat stage directions

Ordered visual events live in each beat's `shot.show` block in `beat_sheet.json`
(SHOW-DON'T-TELL LAW). `shot.visual_intent` names the on-screen artifact for every beat.

## Fill status

All 12 slots filled by `remotion_scenes.py` → `media/B*.mp4`, each conformed to its beat's
measured duration. Re-render one slot with
`remotion_scenes.py <REEL> --only B07 --force`.
