# TYPECHECK.md — GATE T

Reel: `thousands-of-years-divided`  |  Checked: 2026-09-27T14:08  |  Overall: PASS  |  Beats checked: 8  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| B00 | ? | light | min-size §8.1: min text-run height 41px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B01 | ? | light | min-size §8.1: min text-run height 45px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B02 | ? | light | min-size §8.1: min text-run height 42px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B03 | ? | light | min-size §8.1: min text-run height 90px >= floor 41px | PASS | — |
| B04 | ? | light | min-size §8.1: min text-run height 79px >= floor 41px | PASS | — |
| B05 | ? | light | min-size §8.1: min text-run height 170px >= floor 41px | PASS | — |
| B06 | ? | light | min-size §8.1: min text-run height 44px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B07 | ? | light | min-size §8.1: min text-run height 41px >= floor 41px (individual-char fallback at 2×) | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 0 | 0 |
| min-size §8.1 | 8 | 0 |
| overflow §8.2 | 8 | 0 |
| contrast §8.3 | 8 | 0 |
| contrast-local §8.3b | 8 | 0 |
| bbox-overlap §8.6b | 8 | 0 |
| card-clip §8.13 | 8 | 0 |
| kerning §8.4 | 8 | 0 |
| redundancy §8.10 (advisory) | 0 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
