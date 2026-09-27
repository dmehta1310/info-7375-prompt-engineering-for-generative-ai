# TYPECHECK.md — GATE T

Reel: `w1-softmax-offset`  |  Checked: 2026-09-27T13:38  |  Overall: PASS  |  Beats checked: 18  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| B00 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B01A | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B01B | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B01C | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B01D | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B02A | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B02B | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B02C | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B03A | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B03B | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B03C | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B03D | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B04A | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B04B | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B04C | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B04D | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B05 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B06 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 18 | 0 |
| min-size §8.1 | 18 | 0 |
| overflow §8.2 | 18 | 0 |
| contrast §8.3 | 18 | 0 |
| contrast-local §8.3b | 18 | 0 |
| bbox-overlap §8.6b | 18 | 0 |
| card-clip §8.13 | 18 | 0 |
| kerning §8.4 | 0 | 0 |
| redundancy §8.10 (advisory) | 0 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
