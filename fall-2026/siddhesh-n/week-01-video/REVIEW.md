# Review and Revision Record

## Cut 1 — deadline-safe fallback

- Produced a complete MP4 and all required files.
- Problem: FFmpeg flite narration sounded robotic.
- Problem: visuals behaved mostly like zooming presentation cards.
- Decision: retain only as a deadline fallback; do not submit it if Kokoro and stronger motion can be completed.

## Cut 2 — Kokoro and beat-specific motion

- Installed the toolkit's documented Kokoro dependency and voice model manually.
- Replaced flite with Kokoro `am_onyx`.
- Added animated score transformations, probability bars, algebraic cancellation, and the claim boundary.
- User review on 2026-09-26: voice still felt too hard; visuals did not yet resemble the professor's clear templates.

## Cut 3 — submitted candidate

- Inspected the actual course repository and ran the unmodified Chapter 1 program.
- Replaced the constructed `[1000,999,998]` example with the course's actual `[1,2,3]` output.
- Added the lesson's official `[1000,1000] → [0.5,0.5]` test.
- Switched to clearer Kokoro `af_bella` at speed `0.94`.
- Rebuilt every frame in an original course-aligned style: white background, serif titles, outlined process boxes, gray support text, red emphasis, and gold footer rule.
- Added a synthetic-voice disclosure and SRT captions.
- Technical checks: 1920×1080 H.264, AAC audio, complete decode, runtime within 2–4 minutes, valid JSON, valid Python, and intact ZIP.

## Student action still required

Siddhesh must watch the complete Cut 3 MP4, confirm that the narration is easy to understand, and upload the exact matching folder to GitHub before placing the final folder URL and remote commit hash in Canvas.
