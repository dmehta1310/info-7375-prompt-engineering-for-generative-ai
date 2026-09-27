# REVIEW — Why 630, Not 665?

## 2026-09-25 — pre-build review (narration and evidence)

Reviewer: Atharva C (human).

- Voice: replied "af_bella".
- Asked to approve (1) the reworded takeaway, (2) neutral branding (greeting "Hi, Atharva", chip "INFO 7375 · Week 1", no NBB logo, FormACard outro), (3) B00–B09 narration as drafted. Reply: "yes". Recorded as approval of all three.

## Review cut

_Pending — watch the review cut and record timestamp · problem · requested fix here._

### 2026-09-25 — review cut 1 ready

File: `week-01-video-atharva-c-slate.mp4` (185.2 s, 1080p). Automated QC: GATE V 0 BLOCKER / 0 MAJOR after three rounds; see `_qc/VISUAL-QC-LOG.md`.
Changes since pre-build approval, for Atharva to confirm: B01 wording ("exactly" → "about"), outro now a Credits page.
Human review decision: _pending_.

### 2026-09-26 — Atharva C

- Reply: "accept both changes". Recorded: B01 wording ("exactly" → "about") and the Credits-page outro are approved.
- Full watch-through notes on review cut 1: _not yet received_. No final exported.

### 2026-09-26 — presentation changes requested by Atharva C

Approved: (1) Option A, existing props only, gaps logged in FRICTIONAL.md; (2) badges "source code" (B02, B06), "computed from output" (B05), "recorded output" (B03, B04); (3) heading "What This Does Not Show" in Title Case; (4) B04 visual replaced by an expected-vs-observed table with outcome 2 marked, B04 narration unchanged; (5) B06 narration split into B06 + new B06B card, wording as proposed.
Requested: new B00 narration leading with the name. Shown for review before audio regeneration.

### 2026-09-26 — further decisions by Atharva C

- B00: spoken narration "This is Atharva C. This is my week-one assignment for INFO 7375. …" with no spoken disclosure; disclosure moved on screen (top-left label, whole beat). Claude flagged that the synthetic voice now speaks in Atharva's first person; Atharva decided.
- Plain-language narration for B01–B07 approved, with three fixes accepted ("thirty-five fewer times"; coin analogy ends "…bigger than a four or a six"; "Coming up thirty-five short").
- B05 relabelled "Typical wander" / "Gap ÷ wander".
- B04 visual: TtEffectBars exact-count bars (Option 2), outcome 2 observed in terracotta.

### 2026-09-26 — review cut 2 ready

File: `week-01-video-atharva-c-slate.mp4` (181.0 s, 1080p, 11 beats). Audio regenerated for B00–B07 and B06B. GATE V 0/0 (run-05.log); frame notes in `_qc/VISUAL-QC-LOG.md` rounds 4–5.

### 2026-09-26 — B08 handoff

- Atharva asked to remove B08. Claude checked: no automated gate in `./art run` / `./art final` requires it (only `repoloop.py`, not used here), but ai-explainer HANDOFF LAW and the nopunt teaching-arc checklist (scaffolded task, four bookends) do. Reported instead of deleting.
- Atharva chose to shorten it. Draft (prompt read aloud + one check) approved; measured 17.77 s (target 15–18 s), so no trim needed.

### 2026-09-26 — review cut 3 ready

File: `week-01-video-atharva-c-slate.mp4` (163.0 s, 1080p, 11 beats). Only B08 audio/scene regenerated. GATE V 0/0 (run-06.log); frames in `_qc/VISUAL-QC-LOG.md` round 6.

### 2026-09-26 — on-screen text fixes after Atharva watched cut 3

- B06B body now matches its narration word for word; B07 card: bullet "One seeded run…" removed, "Gap ≈ 2.4 × typical wander".
- B01 on-screen text: Option 1 wording approved. Size/timing rounds failed GATE V (see FRICTIONAL.md §5). Atharva then chose: drop the typed correction; if still failing, reuse B03/B07's passing card. No-correction version failed (52 %); B01 now uses ClaudeVerdictArtifact ("The Idea", three lines) and passes.

### 2026-09-26 — review cut 4 ready

File: `week-01-video-atharva-c-slate.mp4` (163.0 s, 1080p, 11 beats). No narration changes. GATE V 0/0 (run-11.log); rounds 7–15 in `_qc/VISUAL-QC-LOG.md`.

### 2026-09-26 — local final exported

Atharva supplied the command `./art final <reel> --height 1080 --out <reel>/final`; Claude ran it (final-01.log, exit 0).
- `final/week-01-video-atharva-c.mp4` — 1920×1080, 24 fps, 163.04 s, audio mean −23.9 dB / peak −2.9 dB.
- Receipt `final/week-01-video-atharva-c.verified.json`: status `ready`, sha256 `332f9cd97342c20e5a6ad7dbc2471860ce16ede27542555663518c6baaab6b2b` (matches `shasum -a 256` of the file); per-beat media/mp3 hashes recorded.
- Frames sampled from the final (`_qc/frames/final_grid.png`): no review beat-markers; B00 disclosure label, B01 card, B04 bars, B06B, B08, credits all present.
- The receipt means automated export checks passed. It is not publication approval. Submission/sharing decision: Atharva's. Not published.

### 2026-09-27 — class naming convention (fall-2026/: no full names)

Decisions by Atharva C:
- Full name replaced with "Atharva C" in every committed file, including beat_sheet.json (metadata.author, B07 card label, outro credits).
- B00 narration: "This is Atharva. This is my week-one assignment for INFO 7375. …" (first name only, to avoid "Atharva see").
- Re-render B00, B07, outro and re-export the final.
- Do not commit the MP4; submit it to Canvas only.
- Repo-scoped GitHub noreply commit email before the rebase.
- Files move to fall-2026/atharva-c/week-01-video/ on the branch rebased onto origin/main; push to main only after Atharva reviews the re-rendered video.

### 2026-09-27 — re-export after the naming change

- B00 audio regenerated (16.41 s); B00, B07, outro re-rendered. Review build GATE V 0/0 (run-12.log).
- `./art final … --height 1080 --out …/final` (final-02.log): 1920×1080, 162.46 s, receipt `ready`, sha256 `5ea22141aa84e24df805eb292a7bae4248db56f5d991e2518c0f181bdb92c080` (replaces the 2026-09-26 export `332f9cd9…`).
- Frames from the final: B00 disclosure label and "Hi, Atharva"; B07 footer "Atharva C · INFO 7375"; credits "Atharva C · INFO 7375, Week 1".
- **Human review:** Atharva C watched the updated final and confirmed B00's opening line is correct (2026-09-27). MP4 goes to Canvas, not Git.
