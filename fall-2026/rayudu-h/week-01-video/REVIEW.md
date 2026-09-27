# REVIEW — Temperature Is Concentration, Not Truth

**Film:** `temperature-is-concentration.mp4`, 3:08, 3840×2160
**SHA-256:** `88bbcabcb507da049398d1b56f30d5665bfeaab008634a6dcd86324df3e585ba`
**Reviewer:** me, the author
**Status:** reviewed local final, approved for submission on 2026-09-26. Not published.

Timestamps are positions in the final 3:08 cut. "Raised by" is whoever found the problem first: me watching the video, or Claude's checks (frame QC, the whole-reel audit, the pre-push audit). Every fix was re-checked by looking at the frames again, not by trusting a render log.

## Problems, changes, and re-checks

| Date | Where | Raised by | Problem or request | Change | Re-check |
|---|---|---|---|---|---|
| 2026-09-22 | whole film | me | Too much notation for someone new to this. I wanted it easier to follow without losing the maths | Added an everyday analogy, the contrast slider (B01A, 0:25–0:51), captioned on screen as an analogy | Frames at 15 / 50 / 85 % of the beat; `FACTCHECK.md` explains why the analogy is faithful and what it can't carry |
| 2026-09-22 | 0:25–0:51 (B01A) | Claude (frame QC) | Captions turned into a pile of overlapping letters while changing | Cross-fade instead of a letter-by-letter morph | Same moment re-read: legible |
| 2026-09-23 | 2:12–2:18 (B05) | Claude suggested, I agreed | The analogy was never used again after B01A | B05 now closes on it: "a sharper picture of the wrong person" | Frames at the closing lines |
| 2026-09-23 | whole film | Claude suggested, I agreed | No captions | Added captions (`.srt`, 58 cues) | Caption text matches the narration word for word; no timing errors |
| 2026-09-25 | 0:19–0:25 (B01) | **me** | The screen said "It decides how truthful the answer is" while the voice said "not how truthful it is" | The on-screen correction had never actually run; rewritten so it does | "truthful" is struck out at 0:20 as the voice says it, and the corrected sentence holds from 0:23 |
| 2026-09-25 | 0:00–0:14 (B00), 1:14–1:21 (B03) | Claude (whole-reel audit) | B00 showed three lines as if Claude had answered, under a real model name. Claude never gave that answer. B03 said "rendering Manim…" | I chose to remove them rather than label them. Prompts only now | Frames re-read: no answer lines, no model name |
| 2026-09-25 | 2:18–2:41 (B06) | Claude (whole-reel audit) | "849 / 630 / 469" read like one run of 1,000, but they add up to 1,948 | Now says they're outcome 2's counts at T = 0.5 / 1 / 2 | Frame re-read |
| 2026-09-25 | 0:25–0:51 (B01A) | Claude (whole-reel audit) | The slider moved about 3 s after the voice described it, and "that is temperature" could be heard backwards | Re-timed to the words; the narration now says the slider runs backwards | Frames at six phrase points |
| 2026-09-26 | 2:41–3:05 (B07) | me, through a question about the ending | The narration paraphrased the prompt and never said "2.5" | Reads the prompt word for word | Frames at five phrase points |
| 2026-09-26 | 1:21–1:31 (B04) | Claude suggested, I agreed | The key step, that the total cancels, was stated but never shown | B04 now works it out on screen before the numbers | Frames at nine phrase points; all gates clean |
| 2026-09-26 | 2:18–2:41 (B06) | Claude suggested, I agreed | "Outcome two wins" was backed only by outcome 2's own counts | Added the full T = 2 row, 202 / 329 / 469, re-run from `main.py` | Frame re-read |
| 2026-09-26 | the folder | Claude (pre-push audit) | The folder couldn't rebuild the video: `SHOTLIST.md` was missing | Added it and fixed the rebuild steps | Rebuilt from the folder alone: byte-identical to the submitted file |

## Decision

**2026-09-26: I watched the final 3:08 cut. Nothing further to change. Approved for submission**, as the zip on Canvas and this folder in the course repository. It hasn't been published anywhere else.
