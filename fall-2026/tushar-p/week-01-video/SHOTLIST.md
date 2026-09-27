# SHOTLIST — token-not-word

Typed work order. Every beat is `shot.type GRAPHIC · source own · lane manim`,
rendered by the pipeline from `scenes.py` to `manim/<BEAT_ID>.mp4`.
Class naming is load-bearing: `run.sh` discovers scenes by the regex
`class ([A-Z][A-Za-z0-9]*_\w+)\(Scene\)` and takes the beat id from the prefix
before the first underscore.

| Beat | Scene class | Owner | Slot | Est |
|---|---|---|---|---|
| B00 | `B00_TenLetters` | pipeline | `manim/B00.mp4` | 8s |
| B01 | `B01_ThreeTokens` | pipeline | `manim/B01.mp4` | 15s |
| B02 | `B02_ScatteredRs` | pipeline | `manim/B02.mp4` | 15s |
| B03 | `B03_SpaceCollapse` | pipeline | `manim/B03.mp4` | 18s |
| B04 | `B04_NotMeaning` | pipeline | `manim/B04.mp4` | 18s |
| B05 | `B05_DidItFail` | pipeline (+2 screenshots, now **filled**) | `manim/B05.mp4` | 24s |
| B06 | `B06_TellSplit` | pipeline | `manim/B06.mp4` | 30s |
| BOUT | `BOUT_Closing` | pipeline | `manim/BOUT.mp4` | 10s |
| BTHX | `BTHX_ThankYou` | pipeline | `manim/BTHX.mp4` | 6s |

## Open slots (human)

Two dated screenshots, both owned by the author, both inside B05. They are not
separate beats — `B05_DidItFail` draws a labelled empty frame naming the file it
wants, and swaps in the real PNG automatically once it exists:

- `media/B05-claude-strawberry.png`
- `media/B05-claude-blueberry.png`

See PROMPTS.md. The beat renders and reviews without them; it is not a slate.

## Per beat

**B00 · COLD OPEN — the question, word still whole.**
Rail "TOKEN, NOT WORD". Question in bold at y=1.95. `strawberry` mono at 92pt,
centred. Two soft lines beneath. Nothing is split yet — that is the point.

**B01 · THE SPLIT — three boxes and the 10 → 3 readout.**
`strawberry` at top; `TransformFromCopy` into three white token cards
(`str` 496 · `aw` 675 · `berry` 15717), ids beneath each. Bottom rail: two live
counters, "characters in" and "tokens out", counting up to 10 and 3 across a
terracotta arrow. Caption "GPT-4 tokenizer · cl100k_base".

**B02 · THE SPLIT — where the r's actually are.**
Same three cards. `ReplacementTransform` stamps terracotta on `str[2]` and
`berry[2]`,`berry[3]`. Tallies above each card: one r / no r / two r. Then the
three r's in the whole word light up at indices 2, 7, 8 — same three letters,
two different groupings.

**B03 · FREQUENCY — the collapse.**
Opens on the three cards with the 10/3 counters already up. A leading space is
introduced: `ReplacementTransform` collapses the row into one card
`' strawberry'` / 73700, and the counters move to 11 and 1. The label above
flips "no leading space" → "one leading space".

**B04 · FREQUENCY — not meaning, and reuse.**
Two rows, each with its source word set left and its token cards to the right.
Row 1 `unbelievable` → `un` 359 · `belie` 32898 · `vable` 24694, under a line
reading "not un · believe · able". Row 2 `raspberry` → `ras` 13075 · `p` 79 ·
`berry` 15717, with a terracotta ring around `berry` and the label
"15717 — the same token as in strawberry".

**B05 · THE HONEST LIMIT — the two real answers, and the boundary.**
Rail dated "asked 22 Sep 2026". The two real screenshots side by side, each
captioned with model, word, date and "correct". Then the verdict line, then the
boundary stated in two parts: what this **does** explain (why counting is
unreliable) above what it **does not** establish (that a model gets it wrong
today). Closes on the GPT-4-tokenizer caveat. This is the beat that refuses to
overclaim; the "tell" moved out to B06.

**B06 · THE HONEST LIMIT — the tell.**
Two rows, same width, on one shared baseline.
TOP: `straw` / `ber` / `ry` — Claude's **spoken** grouping from the 22 Sep
capture, rendered as plain cards with **NO token IDs**, under the label
"Claude's grouping (what it said)" and an explicit "not tokenizer output — no
token IDs". BOTTOM: the real split `str` 496 · `aw` 675 · `berry` 15717, under
"actual tokens · cl100k_base". Between them a hairline ruler carries terracotta
ticks — up for where Claude's grouping cuts, down for where the tokenizer cuts.
They do not line up, and that misalignment is the whole beat.

Both rows span the same width because both cover the same ten characters
(5+3+2 and 3+2+5, identical card padding and gaps), so the cut points are
directly comparable. See FACTCHECK.md §B06 for the honesty rule: an id under
the top row would be a false claim.

**BOUT · OUTRO — the callback: same answer, different path.**
(Rebuilt 25 Sep 2026; replaced the "frequency-shaped chunks" text card so the
visual matches the narration.) The question "how many r's in strawberry?" in
bold; beneath it `strawberry` whole, with its r's (indices 2, 7, 8) stamped
terracotta and underlined, like B02. An arrow runs to a large ink **3** with
"r's" beneath. Then `TransformFromCopy` drops B01's token row under the word
(`str` 496 · `aw` 675 · `berry` 15717, r's stamped inside the cards), labelled
"what the model sees · cl100k_base tokens", and a second arrow points it to the
same 3. Cite: "same answer, different path". No new numbers.

**BTHX · THANKS — the sign-off, read the model's way.**
"thanks for watching" in bold; `Thank you!` mono; `TransformFromCopy` into the
real `cl100k_base` split (FACTCHECK S4): `'Thank'` 13359 · `' you'` 499 ·
`'!'` 0, in B01's `_token_box` style. Quoted as in B03, so the leading space in
`' you'` is visible, and a terracotta underscore marks the space cell. Beneath
it, "the space rides inside the second token". Cite: "cl100k_base · GPT-4
tokenizer". The narration states no token count.
Ends on a **0.6s fade to cream** via `_hold(self, "BTHX", fade_out=0.6)`. The
fade runs inside the mp3's own trailing silence: speech ends at 4.52s, the mp3
at 5.16s. The pipeline has no silent-tail mechanism (`compile.py` requires each
mp3 to match its beat within 0.15s), so the fade can't be any longer than that
silence without a pipeline change. Gate V's 85% sample (4.39s) lands before the
fade starts (4.57s).

## Layout law observed

Gate V samples each beat at 50% and 85% of its span and requires the content
bounding box to cover ≥55% of the safe area. Every scene therefore reaches its
full-width steady state before halfway and holds it to the end; the `_rail()`
top bar spans x −6.0…6.0 to anchor that width. Nothing fades out at the tail.

Terracotta (#D97757) is 2.73:1 on cream and is never used as a `Text` colour —
only as indexed `set_color` on built glyphs, and on strokes. This keeps Gate W's
W2 contrast rule satisfied.

## Timing law — scenes are cut to the measured mp3

`compile.py` conforms a short clip by **slowing it** (`setpts`), never by
freezing, so any scene that runs shorter than its narration ships as slow-mo.
Every scene therefore ends in `_hold(self, "<BEAT_ID>")`, which reads
`actual_duration_s` straight out of `beat_sheet.json` and holds the composed
frame until the scene matches its mp3. Every beat renders at 1.0x.

Measured clock (Kokoro am_onyx, local, $0.00):

| Beat | measured |
|---|---|
| B00 | 13.95s |
| B01 | 15.49s |
| B02 | 14.78s |
| B03 | 19.61s |
| B04 | 22.23s |
| B05 | 29.71s |
| B06 | 25.87s |
| BOUT | 16.36s |
| BTHX | 5.16s |
| **Total** | **163.16s = 2:43.16** |

If narration is regenerated, the scenes re-cut themselves on the next render —
no hand-edited timings anywhere.

## Two defects caught in frame review (fixed)

Both were invisible to the static gates and only showed up by looking at
rendered frames:

1. **B04 — the terracotta ring was around `ras`, not `berry`.**
   `TransformFromCopy` aligns submobject counts and mutates its *target* group,
   so `row2[2]` stopped pointing at the berry card once the transform had run.
   The scene was ringing the wrong token under a label reading
   "15717 — the same token as in strawberry" — a false visual claim.
   Fixed by capturing the card's centre/size as plain floats *before* the
   transform.
2. **B04 — `unbelievable` collided with its first token card** by 0.68 units.
   Gate W could not see it: the row is positioned with `.arrange()`, and Gate W
   skips geometry for mobjects it cannot resolve statically. Fixed by measuring
   the word's real width and placing the row from its right edge.

A third, smaller one: B05's verdict line touched the screenshot captions; lowered.


## Open slots — now closed

Both B05 screenshots have been supplied and are rendering in the beat:
`media/B05-claude-strawberry.png` and `media/B05-claude-blueberry.png`.

As dropped, the two filenames were **transposed** — each file held the other
conversation. Caught by reading the images, not the filenames; renamed to match
content and verified by checksum. See FACTCHECK.md S2/S3.

## Branding

`palette` and `style_preset` are deliberately **unset** in metadata. Setting
`palette: claude` makes `lint_skin` demand `ClaudeComposerAsk` on the cold open
and `ClaudeTitleOutro` on the outro (COLD OPEN LAW / OUTRO LAW) — branded cards
this course reel does not use. OUTRO-LOCK.md scopes itself to `claude-liam-*`
slugs in any case. The cream/ink/terracotta palette is unaffected: those values
are hardcoded in `scenes.py`, not read from metadata.


## Typography — why every Text is built at size 96 and scaled down

Pango quantises glyph advances when a `Text` is built at a small point size. At
`font_size=20`, "cl100k_base" rendered as "cl 100k_bas e" and the space before a
middot collapsed ("tokenizer·"). The same string built at `font_size=96` and
scaled to 20 is evenly spaced. `_label` and `_mono` therefore build at
`_TEXT_REF = 96.0` and scale down; never pass a small font_size straight to
`Text` in this file.

This was a *sizing* bug, not a font fallback — the monospace cards and the big
words were always fine. Monospace is nonetheless pinned to `MONO = "Menlo"`
rather than the generic `"monospace"` alias, which is not a real Pango family
(there is no lowercase entry) and was being silently resolved.

Knock-on: B04's rows are now placed with `to_edge`/`next_to`/`match_x` instead
of coordinate literals built from `.width`. Gate A's mock manim does not apply
`.scale()`, so a literal derived from `.width` read as off-frame (11.6) there and
blocked the build. The trade is that Gate W can no longer resolve that geometry
statically, so B04's margins and overlaps are verified by measurement and by
frame review instead — both done, both clean.
