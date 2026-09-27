# PEDAGOGY — Less Room to Wander (week-01 video)

Narration sign-off for `beat_sheet.json` in this folder. **No audio exists yet.** Audio is generated only after the sign-off below is completed by Prasad. The toolkit's rule: narration is approved before audio, and silence is never approval.

- **Builder:** brutalist.art `ai-explainer`, free beginner path (toolkit revision `6a8380ae169cca81e0633664a65c958f5c12ab4b`)
- **Voice:** Kokoro `af_bella`, synthetic. Disclosed in B00's first sentence and on the outro card. Not Prasad's voice, not Bear, not an official or endorsed video.
- **Evidence:** `evidence/temp-1.0.json`, `evidence/temp-0.5.json`, `evidence/ANALYSIS.md`; code from unedited `lessons/01-randomness-and-first-prompts/code/main.py`.
- **Question:** Does the gap between a predicted sample count and the actual count shrink as one outcome becomes more dominant (lower temperature)?
- **Takeaway:** a more lopsided distribution has less room for a sample to wander (spread ≈14.9 → ≈10.7), but this run also landing closer in standard-deviation terms is partly seed 7's luck.
- **Limitation:** untested at other temperatures (e.g. 2.0); both runs share seed 7, so they aren't independent evidence.

## Narration, beat by beat (exact text that will be recorded)

### B00 — cold open · `ClaudeComposerAsk` (reconstructed UI) (53 words)

> Namaste. This is a synthetic narrator, Kokoro's Bella voice, reading a script Prasad reviewed. It isn't Prasad, and it isn't anyone official. A model samples its answers from a distribution. When one answer gets more dominant, does the sample land closer to what the math predicts? One small experiment: two temperatures, same seed.

**Evidence:** Output lines = temp-1.0.json / temp-0.5.json `counts["2"]` (630, 849) and ANALYSIS.md expected values (665.24, 866.8); seed 7 from the method. Disclosure in the first sentence.

### B01 — summary · `BrutalistHesitantWriter` ("gets more accurate" → "has less room to wander") (31 words)

> Lower the temperature and the sample has less room to wander. That part is guaranteed. Whether one run lands closer is a different question, and one seeded run can't settle it.

**Evidence:** ANALYSIS.md reasoning ("guaranteed by the math") and limitation. The corrected phrase is the misconception the video takes apart.

### B02 — mechanism · `ClaudeCodeBeat`, main.py lines 9–17 verbatim (51 words)

> This is the course's reference code, untouched. Scores come in. The biggest is subtracted for stability, everything is divided by the temperature, then exponentiated and normalized. A smaller temperature stretches the gaps between scores, so the favorite pulls further ahead. Temperature reshapes the odds. It doesn't change which answer is right.

**Evidence:** The code itself; `docs/en.md:27`: "Temperature changes the distribution, not the truth of the answer."

### B03 — distribution · `ReqBars` (grey 1.0 vs terracotta 0.5) (44 words)

> Same three scores, two temperatures. At 1.0, the top token gets about two-thirds of the probability. Drop to 0.5 and it jumps to about eighty-seven percent, while the other two shrink. The scores didn't change. Only how confidently the model bets on its favorite.

**Evidence:** `probabilities` in both JSON files: 0.6652 → "about two-thirds"; 0.8668 → "about eighty-seven percent". Bars show whole-percent rounding (9/24/67, 2/12/87), and the on-screen note says so.

### B04 — framework + worked example · `ExecutedData` table (44 words)

> Here's the yardstick: expected count is probability times a thousand draws. At temperature 1.0 that predicts 665 top-token picks. The run got 630, about 35 short. At 0.5 the prediction is 867, and the run got 849, about 18 short. The gap roughly halved.

**Evidence:** ANALYSIS.md table: 665.24 → "665", 630, ~35; 866.8 → "867", 849, ~18. "Roughly halved": 35 → 18. "Expected = probability × 1,000" is plain arithmetic, allowed by MATH-TYPESETTING.

### B05 — prediction · `FormACard`, verbatim quotes (44 words)

> Before the temperature 0.5 run, Prasad predicted the direction: the gap would get closer. It did, both in raw counts and measured in standard deviations, the fairer ruler. But a prediction coming true once is where the careful part starts, not where it ends.

**Evidence:** ANALYSIS.md prediction + verdict lines (verbatim on screen). **Timing ("before the temperature 0.5 run") rests on Prasad's own statement of 2026-09-26; no file records it.**

### B06 — guaranteed vs. this run · `ExecutedData` table (57 words)

> Two different things are shrinking. The spread, how far a thousand draws usually wander, drops from about fifteen to about eleven. The math guarantees that as the favorite gets more dominant. But this run's miss also shrank in spread units, from 2.4 to 1.7. The math doesn't promise that. One run can land anywhere in its spread.

**Evidence:** ANALYSIS.md: ±14.9 → "about fifteen", ±10.7 → "about eleven", 2.4 SD, 1.7 SD; "guaranteed by the math" / "a single sample could land anywhere in that spread".

### B07 — stress test · `ClaudeCodeBeat`, main.py lines 19–24 verbatim (56 words)

> Here's the catch. Both runs used seed 7, so they drew from the same stream of random numbers. That ties them together; they aren't two independent tests. A different seed could show a bigger gap or a smaller one, at either temperature. And nothing here says what happens at 2.0, because that run hasn't been done.

**Evidence:** `seed=7` default + `random.Random(seed)` in the code; ANALYSIS.md limitation (seed 7 shared, not independent; 2.0 untested).

### BVDT — verdict · `ClaudeVerdictArtifact` (69 words)

> Let's recap with Claude. Lower temperature concentrates probability on the top token: sixty-six and a half percent at 1.0, eighty-six point seven at 0.5. The top token missed its expected count by about 35 at 1.0 and about 18 at 0.5. The expected spread shrinks as the favorite dominates; that part is guaranteed. Landing closer in standard-deviation terms may be this seed's luck, because both runs shared seed 7.

**Evidence:** Recaps B03–B07. 66.5% / 86.7% are the JSON probabilities to one decimal.

### BHTF — your turn · `ClaudeComposerAsk` (117 words)

> I ran a softmax sampler on logits [1, 2, 3], 1,000 draws, seed 7, at temperatures 1.0 and 0.5, and compared the top token's expected and observed counts. Help me design a follow-up: (1) repeat the comparison across 20 different seeds and add temperature 2.0, (2) report each gap in standard deviations, (3) tell me whether the 'gap shrinks' pattern survives or was one seed's luck. Check three things in the answer: does it use different seeds so the runs are independent, does it measure gaps in standard deviations instead of raw counts, and does it say plainly when the evidence is too thin to call a pattern? Take it and run it on your own sampler.

**Evidence:** Viewer task with a three-point rubric (seeds, SD units, says when evidence is too thin).

### BOUT — outro · `FormACard` (title + disclosure colophon) (14 words)

> Less Room to Wander. Narrated by a synthetic voice for Prasad S, INFO 7375.

**Evidence:** Disclosure.

## Act structure (teaching-arc checklist, `skills/make/nopunt/SKILL.md`)

| Item | Where | Status |
|---|---|---|
| Framework before the example | B02 (mechanism) + B04 opening line ("expected = probability × 1,000") | ✓ |
| Worked example | B04 (both temperatures, row by row) | ✓ |
| Falsifiability / edge case, a full beat | B07 (shared seed, untested 2.0) | ✓ |
| Scaffolded viewer task | BHTF (prompt + three-point rubric) | ✓ |
| Four frame beats | B00, BVDT, BHTF, BOUT | ✓ |
| No source, no verdict | every claim beat shows its code or evidence on screen; B03/B04/B06 carry source notes | ✓ |

Beat classes: 9 SHOW, 2 CARD (B05 verbatim quote card, BOUT outro), 0 PUNT. `build_safety.validate_project` passes (voice `af_bella`); `qc/beat_lint.py`: clean. B04 and B06 share a scene type but aren't consecutive (B05 sits between them).

## Deliberate departures from the skill's defaults

- No claude-liam persona or @NikBearBrown branding (course prerequisite: do not imply Bear or endorsement).
- Outro is FormACard, not ClaudeTitleOutro (its @NikBearBrown handle is hardcoded; OUTRO-LOCK scopes it to claude-liam reels only).
- Voice af_bella instead of am_onyx (am_onyx is the Liam/Bear voice in this toolkit).
- Single ASK (B00, the actual run); no extra composer micro-beats before each chart.
- LOGO LAW: brand label only where the component supports brandLabel (not ExecutedData, ReqBars, FormACard).

## Friction protected

- **Kept:** the prediction (B05) stays in, and so does the admission that part of the result may be luck (B06–B07). That distinction is the lesson; cutting it would turn the video into "lower temperature = more accurate", the misconception B01 corrects.
- **Kept off screen:** the standard-deviation formula. No equation renderer is used; only values from ANALYSIS.md appear.
- **Left for the viewer:** the multi-seed / temperature-2.0 follow-up is the handoff task, not a claim in the video.

## Still to do after sign-off (not part of this approval)

- Generate audio; re-time `rows[].at` in B04/B06 to the measured audio.
- Write `FACTCHECK.md`, `SHOTLIST.md`, `SOURCES.md` (toolkit GATE F) and `CHECKS-REPORT.md` before the first review cut.
- Review cut → frame-level visual QC → Prasad watches with sound → revisions → final.

## Sign-off

**Status: SIGNED.**

By signing, I confirm I've read every narration line above, checked each claim against the named evidence, and approve this exact text for synthetic narration.

- Reviewer: Prasad S
- Decision: ☑ approved as written
- Date: 2026-09-26
- Changes requested: none

_Drafted by Claude Code (Opus 5.5) from Prasad's approved beat plan; Prasad confirmed on 2026-09-26 that the narration table traces to the evidence files. This draft is not the sign-off._
