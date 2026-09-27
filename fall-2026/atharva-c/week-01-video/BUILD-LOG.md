# BUILD-LOG — Why 630, Not 665?

## 2026-09-25

- **Toolkit readiness.** `./setup` (rev `29ba0e8`) exits 1 before its feature checks: its ElevenLabs guard matches files under the toolkit's own `youtube/brutalist/` examples. Not caused by this reel; toolkit left unmodified. Features used here (Kokoro, Remotion, ffmpeg) are verified by the actual build below instead of the readiness table.
- **Deliberate deviations from ai-explainer defaults** (approved by Atharva C, 2026-09-25), because the defaults would imply the instructor or an endorsement:
  - No `claude-liam` persona / "in for Bear" sign-off; narration opens with a synthetic-voice disclosure.
  - Footer chip `INFO 7375 · Week 1` instead of `@NikBearBrown`.
  - No NBB logo bug (LOGO LAW not applied).
  - Outro is `FormACard` (title restate + credit + disclosure) instead of `ClaudeTitleOutro`, whose handle is hardcoded `@NikBearBrown` (OUTRO-LOCK.md).
  - Voice `af_bella` (Plain register), chosen by Atharva.
- **Equations.** None typeset, per the course prerequisite for a first video.
- **Consecutive ExecutedData beats (B03–B05).** Same component three times — the ILLUSTRATE-LAW smell. Kept: the course beginner path asks for existing components only; B03/B04 are probability bars, B05 a table.
- **TTS spellings.** `normalize_for_tts` passes text unchanged, so narration_text uses spoken forms: "info seventy-three seventy-five", "main dot py", "sample" (for `sample()`). On-screen text keeps the exact strings.
- **lead_silence_s: 0.8** written on B01 per the skill; no script in this revision reads it. B01's ≥ 9 s window must come from narration length — checked after audio.
- **ffmpeg/ffprobe** were missing; installed with `brew install ffmpeg` (9.0.2) on Atharva's instruction.
- **Audio:** Kokoro af_bella, 10 beats, 184.99 s total, $0.00. B01 = 14.14 s (≥ 9 s ✓).
- **Review-cut fixes (layout only, narration unchanged):** see `_qc/VISUAL-QC-LOG.md`. Two changes differ from the pre-build plan Atharva approved:
  - B01 on-screen text is now "Probability 0.665 means ~~exactly~~ about 665 hits in 1,000 draws. / One run came back 630." (the component can't correct a multi-word phrase).
  - The outro is a `ClaudeVerdictArtifact` "Credits" page instead of `FormACard` (FormACard can't pass the fill gate). SKIN LINT notes that OUTRO LAW expects ClaudeTitleOutro; that deviation is deliberate (see above).
- **Toolkit doc/component mismatches found (not fixed here, toolkit untouched):** ai-explainer SKILL.md says to put a whole phrase in `triggerWords`, but BrutalistHesitantWriter matches single tokens; ClaudeCodeBeat drops everything after " — " in `title`; `lead_silence_s` is not read by any script; GATE T `type_check.py` is absent.
- **Review cut:** `week-01-video-atharva-c-slate.mp4`, 185.2 s, 1920×1080, GATE V 0/0 (run-03.log).

## 2026-09-26

All changes approved by Atharva C; decisions recorded in REVIEW.md, frame checks in `_qc/VISUAL-QC-LOG.md` (rounds 4–15), toolkit gaps in FRICTIONAL.md.

- **Presentation (Option A, existing props only):** "source code" badge on B02/B06 (ClaudeCodeBeat `language` slot); "recorded output" / "computed from output" + source line in `ExecutedData.note` / `TtEffectBars.note` on B03–B05 (serif, not monospace).
- **B00:** narration now "This is Atharva C. This is my week-one assignment…" with no spoken disclosure (Atharva's decision; Claude flagged the first-person synthetic voice). Disclosure moved on screen: topic label "…Synthetic narration — Kokoro af_bella", visible from 0.4 s for the whole beat.
- **Plain-language narration** for B01–B07 (no "spread"/statistics jargon), with three accuracy fixes; B05 relabelled "Typical wander" / "Gap ÷ wander"; B07 card "Gap ≈ 2.4 × typical wander", duplicate bullet removed.
- **B04:** ExecutedData → TtEffectBars exact-count bars (outcome-2 observed in terracotta); spark line removed because the component draws the banned "*" glyph.
- **B06 split:** B06 keeps the seed code; new **B06B** SkillTeardownMechanism card "What This Does Not Show" (body matches narration word for word).
- **B08 shortened** (17.77 s): prompt "Run sample() from my main.py with seeds 0 to 199. First, ask me to predict how often outcome 2 lands within 30 of 665." + one check (own seed each run). Removal was requested first; reported instead because HANDOFF LAW / nopunt checklist require it (no automated gate does).
- **B01:** six hesitant-writer rounds failed GATE V (width/height overflow, mid-beat underfill; FRICTIONAL.md §5). Now ClaudeVerdictArtifact "The Idea" (B07's passing component); no typed correction — EXECUTIVE-SUMMARY LAW's hesitant writer not applied, by Atharva's decision.
- **Audio:** Kokoro af_bella regenerated for B00–B08 + B06B; total 163.0 s; $0.00.
- **Final:** `./art final … --height 1080 --out …/final` (final-01.log): `final/week-01-video-atharva-c.mp4`, receipt `ready`, sha256 `332f9cd9…6b2b`. Not published; final/ is gitignored.
