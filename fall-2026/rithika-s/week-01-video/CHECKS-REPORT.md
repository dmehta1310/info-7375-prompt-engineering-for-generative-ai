# CHECKS-REPORT — "The Token That Followed"

Written before the compile, per the PROOF GATE. Classification rules:
`skills/make/nopunt/SKILL.md`. This is the **2026-09-23 six-act cut**.

```
12 SHOW / 0 justified-HOLD / 0 PUNT-flagged

Teaching arc: FRAMEWORK ✓ | WORKED EXAMPLE ✓ | FALSIFIABILITY ✓
              SCAFFOLDED TASK — see note | BOOKENDS — see note | NO-SOURCE-NO-VERDICT ✓
```

## Per-beat classification

Every beat carries a `shot.show` block and a `shot.visual_intent` naming its on-screen
artifact, so none is a bare CARD.

| Beat | Act | Class | Scene |
|---|---|---|---|
| B00 | HOOK | SHOW | `Ch1PretrainHook` |
| B01 | MECHANISM | SHOW | `Ch1PretrainCorpus` |
| B02 | MECHANISM | SHOW | `Ch1PretrainTarget` |
| B03 | MECHANISM | SHOW | `Ch1PretrainLadder` step 1 |
| B04 | MECHANISM | SHOW | `Ch1PretrainLadder` step 2 |
| B05 | MECHANISM | SHOW | `Ch1PretrainLadder` step 3 |
| B06 | MECHANISM | SHOW | `Ch1PretrainLadder` step 4 |
| B07 | MECHANISM | SHOW | `Ch1PretrainLadder` step 5 |
| B08 | CONTRAST | SHOW | `Ch1PretrainContrast` |
| B09 | LOSS | SHOW | `Ch1PretrainLoss` |
| B10 | BOUNDARY | SHOW | `Ch1PretrainBoundary` |
| B11 | TAKEAWAY | SHOW | `Ch1PretrainTakeaway` |

No beat could be exported as a static slide with a voice over it (THE PPT TEST). The five
ladder beats share a component by design — that is the opposite of the "two consecutive
beats sharing a visual scheme" smell, because the whole point is that the viewer returns
to the *same* table and finds exactly one new column. The scheme changes at every act
boundary: sentence → card → paired vectors → table×5 → paired corpora → paired panels →
ruled list → poster.

## Teaching arc, and two honest departures

- **FRAMEWORK before examples** ✓ — B00 poses the question in plain English; B01
  establishes what the objective receives (text, tokens, one guess) before any number
  appears. The first figure is B03.
- **WORKED EXAMPLE** ✓ — B03–B07, computed rather than asserted. Every figure is generated
  by `verify_softmax.py --emit` and injected by `build_beat_sheet.py`, so no on-screen
  number is hand-typed.
- **FALSIFIABILITY** ✓ — twice, which is new in this cut. B08 is a genuine falsification
  test: hold the model fixed, swap only the corpus, and watch the target move — if the
  target tracked truth the two columns would coincide. B10 then names what the whole
  explanation does not establish, with 34.1s of screen time.
- **SCAFFOLDED TASK — departed, deliberately.** The previous cut discharged this with a
  HANDOFF beat: a prompt typed into `ClaudeComposerAsk` for the viewer to paste. The
  six-act brief has no handoff slot, and the constraint that any Claude response shown must
  be a real, dated one rules out a staged composer beat (`FRICTIONAL.md` #25). There is
  therefore no viewer task in this cut. Recorded as a departure, not passed silently.
- **BOOKENDS — departed, deliberately.** COLD OPEN LAW (open on the Claude UI),
  EXECUTIVE-SUMMARY LAW (beat 2 = the hesitant writer), HANDOFF LAW and the verdict page
  are all abandoned for the brief's structure. The brief is explicit about what act 1 must
  be — the false sentence as plain English, no math — which is incompatible with opening on
  a composer window. Act 6 serves the outro function (title restate + credit rail).
- **NO-SOURCE-NO-VERDICT** ✓ — the only load-bearing claim is arithmetical and ships as a
  runnable script. The example is labelled `CONSTRUCTED EXAMPLE` on screen on all nine
  beats that display a figure — B10 omits it because that beat displays no figure, and B11
  omits it because it introduces no new claim.

## Legibility contract

- **Named artifact** — every beat names it in `shot.visual_intent`. ✓
- **Negative space ~15–35%** — `Ch1Stage` reserves an 84px spark band and a 46px bug band
  inside SAFE and centres content in the remainder. ✓
- **Un-highlighted elements never below ~40% opacity** — the floor is the named constant
  `CH1.DIM = 0.45`. In the ladder, established columns sit at 0.62, never lower, so the
  ground the viewer already has stays fully readable. ✓
- **Comparisons side-by-side and held ≥2s** — B02 (answer key vs truth key), B08 (two
  corpora) and B09 (incurred vs counterfactual loss) are all two-panel and all hold to the
  end of a 23.3s, 25.4s and 20.3s beat respectively. ✓

## Pacing, which is the point of this cut

Runtime is **253.86s (4:13.86)** against a 4:00 floor. Act 2 holds 59% of the film.
The hook ends on 3.5s of real silence so the viewer answers before the answer appears —
silence in the measured audio, not a hold faked in the edit. No beat introduces more than
one new idea, and no term is used before the beat that defines it: "token" in B01, "logit"
in B03, "softmax" across B03–B07, "loss" in B09.
