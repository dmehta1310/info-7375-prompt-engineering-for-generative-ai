# FRICTIONAL — toolkit gaps met while building this reel

Logged 2026-09-26. brutalist.art revision `29ba0e8`. The toolkit was NOT modified; these are
workarounds using existing props only (Atharva C chose Option A).

## 1. No per-beat topic tag / beat-type badge

Wanted: a persistent top-left topic tag and a top-right badge ("diagram" / "recorded output"
/ "source code" / "computed from output") on every beat.
Library search (`./art scenes`) found no header/badge component. `compile.py`'s corner label
is review-cut only and never reaches a final.
Workaround coverage:

| Beat | Topic tag | Badge |
|---|---|---|
| B00, B08 (ClaudeComposerAsk) | `topic` prop, top-left ✓ | — (no slot) |
| B02, B06 (ClaudeCodeBeat) | — | `language` slot, top-right: "SOURCE CODE" (component uppercases it) |
| B03, B04 (ExecutedData) | — | text prefix in the bottom `note`: "recorded output" |
| B05 (ExecutedData) | — | text prefix in the bottom `note`: "computed from output" |
| B06B (SkillTeardownMechanism) | `eyebrow`, top-centre (not top-left) | — |
| B01, B07, BOUT | — | — |

## 2. No monospace source-citation footer

Wanted: a small monospace "source: lessons/…/main.py -> [exact output]" line on every beat
showing real numbers. No shared citation-footer mechanism exists.
Workaround: `ExecutedData.note` on B03, B04, B05 — but it renders in the **serif** face, not
monospace, and wraps when the exact output is long. B00's recorded output lines were left as
approved (no source line).

## 3. No row highlight in a data table

Wanted: the outcome-2 row highlighted in the expected-vs-observed table. `ExecutedData` has no
highlight prop; `BrandPipelineAudit` has `highlightRow` but hard-coded data.
Workaround: text marker "»" on the row and "(» largest gap)" in the title.

## 4. No accent-coloured heading card

Wanted: bold heading in the accent colour for "What This Does Not Show".
`SkillTeardownMechanism` renders the heading in ink; the terracotta is on its verdict pill
("Limitation"). Its `body` ignores line breaks, so the three lines wrap as one paragraph.

## 5. BrutalistHesitantWriter: size mis-estimation and punctuation-bound timing (B01)

Logged 2026-09-26. Getting B01's on-screen text to match its narration took six render
rounds and never passed GATE V inside this component:

| Round | Layout | Result |
|---|---|---|
| 7 | Option A, 5 lines, fontSize 105, correction "means" → "doesn't mean" | Underfill 32 % / 40 %; still typing at 85 %, correction visible only at ~95 % |
| 8 | Option 1 text, 3 lines, fontSize 190 | Edge-bleed BLOCKER: lines ≈ 2,700 px wide vs 1,728 px safe |
| 9 | Same text, 6 lines, fontSize 180 | Edge-bleed BLOCKER: ≈ 1,290 px tall vs 972 px safe |
| 10 | 6 lines, fontSize 130 | Fits; mid-beat (50 %) underfill 47 % |
| 11 | 5 lines (merged), fontSize 130 | Mid-beat underfill 52 % |
| 13 | 5 lines, fontSize 130, no correction | Mid-beat underfill 52 % |

(Round 12 tried a static FormACard: 14 %, capped type size.)

Resolved by reusing ClaudeVerdictArtifact (B07's passing component) with B01's text —
not by any fontSize.

Causes:
- **fontSize behaves as ≈ CSS pixels at 1080p** (≈ 54 px per character and a 155 px line
  pitch at 130 × 1.2), not 4K design units as first assumed. Estimates made before
  rendering were wrong in both directions (too wide at 190, too tall at 180).
- **Fixed per-punctuation pauses** (400–800 ms after every `. , : ' "` etc., plus
  400 ms per line break and 1.0–1.5 s per correction) are not configurable. With
  `charMs` at 12, typing time is dominated by punctuation count, so text length and
  punctuation directly limit what can finish inside a 13.8 s beat.
- **GATE V samples at 50 %**, while a typing component is by design incomplete then;
  the block height at mid-beat is what fails the 55 % fill minimum.

## Also seen earlier (see BUILD-LOG.md)

BrutalistHesitantWriter matches single-token triggers only (SKILL.md says phrases);
ClaudeCodeBeat drops title text after " — "; `lead_silence_s` is not read; GATE T
`type_check.py` is absent; `./setup` guard trips on the toolkit's own example files.
