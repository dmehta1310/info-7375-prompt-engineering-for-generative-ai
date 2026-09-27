# FACTCHECK — token-not-word

Convention: **a number appears on screen only with its citation line.** Every
figure below was verified by running the tokenizer locally, not copied from a
secondary source (see `docs/EXECUTABLE-EVIDENCE.md`).

## Sources

- **S1 — tiktoken 0.14.0, encoding `cl100k_base`.** Run locally 22 Sep 2026 on
  this machine. Reproduce:

  ```bash
  python3 -c "
  import tiktoken
  enc = tiktoken.get_encoding('cl100k_base')
  for s in ['strawberry', ' strawberry', 'unbelievable', 'raspberry']:
      ids = enc.encode(s)
      print(repr(s), len(s), ids, [enc.decode([t]) for t in ids])
  "
  ```

  Verified output:

  ```
  'strawberry'    10 [496, 675, 15717]    ['str', 'aw', 'berry']
  ' strawberry'   11 [73700]              [' strawberry']
  'unbelievable'  12 [359, 32898, 24694]  ['un', 'belie', 'vable']
  'raspberry'     9  [13075, 79, 15717]   ['ras', 'p', 'berry']
  ```

- **S2 — Claude, asked 22 Sep 2026, screenshot `media/B05-claude-strawberry.png`.**
  Prompt: "How many times does the letter r appear in the word strawberry?"
  Answer, read off the capture: *"The letter 'r' appears 3 times in 'strawberry'
  — in straw, ber, and ry."* Count correct; the grouping it narrates is **not**
  the tokenizer's split. This is the sole source for B06's top row.
- **S3 — Claude, asked 22 Sep 2026, screenshot `media/B05-claude-blueberry.png`.**
  Prompt: "How many times does the letter r appear in the word blueberry?"
  Answer: *"The letter 'r' appears twice in 'blueberry' — blueberry has the two
  r's together: b-l-u-e-b-e-r-r-y."* Correct.

  Both captures carry a visible macOS clock reading **Tue Sep 22**, which
  corroborates the date on screen.

  **Provenance correction (23 Sep 2026):** as originally dropped into `media/`
  the two filenames were transposed — `B05-claude-strawberry.png` held the
  blueberry conversation and vice versa. Caught by reading the images rather
  than trusting the filenames; the files were renamed to match their contents,
  verified by checksum. Had it shipped, both B05 captions would have been false
  and B06's top row would have cited the wrong capture.

- **S4 — tiktoken 0.14.0, encoding `cl100k_base`, the sign-off strings.** Run
  locally 25 Sep 2026 on this machine. Reproduce:

  ```bash
  python3 -c "
  import tiktoken
  print('tiktoken', tiktoken.__version__)
  enc = tiktoken.get_encoding('cl100k_base')
  for s in ['Thank you!', 'Thank you', ' Thank you!']:
      ids = enc.encode(s)
      print(repr(s), len(s), ids, [enc.decode([t]) for t in ids])
  "
  ```

  Verified output:

  ```
  tiktoken 0.14.0
  'Thank you!'   10 [13359, 499, 0]  ['Thank', ' you', '!']
  'Thank you'    9  [13359, 499]     ['Thank', ' you']
  ' Thank you!'  11 [9930, 499, 0]   [' Thank', ' you', '!']
  ```

  BTHX displays `'Thank you!'` only. Three tokens, not one, so the split visual
  stands. Id `0` is a real id (`enc.decode([0]) == '!'`), not a placeholder.
  The other two strings are recorded as controls: dropping the `!` removes
  exactly one token, and a leading space changes `Thank` (13359) into
  ` Thank` (9930), which is B03's lesson again.

  S1 was re-run on the same date and reproduced exactly.

> **`cl100k_base` is GPT-4's tokenizer, not Claude's.** Claude's vocabulary
> differs. The phenomenon (text is read as frequency-shaped subword tokens)
> carries over; the exact pieces and ids do not. B05 says this on the record and
> the reel makes no claim that these specific ids are Claude's.

## On-screen numbers, beat by beat

| Beat | On screen | Source |
|---|---|---|
| B00 | "you see ten letters" — 10 | S1 (`len('strawberry') == 10`) |
| B01 | boxes `str` `aw` `berry` | S1 |
| B01 | ids `496`, `675`, `15717` | S1 |
| B01 | counters `10` characters → `3` tokens | S1 |
| B01 | caption "GPT-4 tokenizer · cl100k_base" | S1 |
| B01–B04 | rail "tiktoken 0.14.0" | S1 (version pinned) |
| B02 | tallies "one r" / "no r" / "two r" | S1 — derived: `'str'.count('r')==1`, `'aw'.count('r')==0`, `'berry'.count('r')==2` |
| B02 | r's stamped at `strawberry[2]`, `[7]`, `[8]` | S1 — `[i for i,c in enumerate('strawberry') if c=='r'] == [2,7,8]` |
| B03 | id `73700`, counters `11` characters → `1` token | S1 (`' strawberry'`, 11 chars incl. the leading space) |
| B04 | `un` `belie` `vable`, ids `359`, `32898`, `24694` | S1 |
| B04 | `ras` `p` `berry`, ids `13075`, `79`, `15717` | S1 |
| B04 | "15717 — the same token as in strawberry" | S1 (`encode('strawberry')[-1] == encode('raspberry')[-1] == 15717`) |
| B05 | rail "asked 22 Sep 2026"; both slot captions dated | S2, S3 |
| B05 | "this explains why counting is unreliable / it does not establish that a model gets it wrong today" | boundary of the claim — S2, S3 are both CORRECT answers |
| B06 | top row `straw` `ber` `ry` — **no token ids** | S2 (Claude's spoken grouping; NOT a tokenizer output) |
| B06 | bottom row `str` `aw` `berry`, ids `496`, `675`, `15717` | S1 |
| B06 | ticks marking where each split cuts | derived from the two rows above; both cover the same 10 characters |
| BOUT | r's stamped at `strawberry[2]`, `[7]`, `[8]` | S1 (same derivation as B02) |
| BOUT | "3" beside "r's" | S1 — `'strawberry'.count('r') == 3`; also S2's answer |
| BOUT | cards `str` `aw` `berry`, ids `496`, `675`, `15717`, r's stamped `str[2]`, `berry[2]`,`[3]` | S1 (B01/B02 again, no new numbers) |
| BOUT | row label "what the model sees · cl100k_base tokens"; rail "tiktoken 0.14.0" | S1 |
| BTHX | phrase `Thank you!` | S4 (displayed string) |
| BTHX | cards `'Thank'` `' you'` `'!'`, ids `13359`, `499`, `0` | S4 |
| BTHX | terracotta underscore in the space cell of `' you'`; "the space rides inside the second token" | S4 — the second piece decodes to `' you'` (leading space) |
| BTHX | caption "cl100k_base · GPT-4 tokenizer"; rail "tiktoken 0.14.0" | S4 |

## B06 — the one rule that governs this beat

**`straw` / `ber` / `ry` is Claude's SPOKEN grouping, observed in the 22 Sep
screenshot (S2). It is NOT a tokenizer output.** No such tokens exist in
`cl100k_base`; the string "straw" is not token-aligned there at all. The beat
therefore renders that row **with no token IDs**, under the label "Claude's
grouping (what it said)" plus an explicit "not tokenizer output — no token IDs".

Only the bottom row — `str` 496 · `aw` 675 · `berry` 15717 — is real
`cl100k_base` output (S1). `_token_box(piece, None)` is the code path that
omits the id line; a made-up id must never be passed to fill the slot, because
an id under the top row would assert that straw/ber/ry are real tokens, which
is false.

Both rows span the same width because both cover the same ten characters, which
is what makes the differing cut points readable off one shared baseline. That
equal width is a consequence of the data, not a layout fudge.

## Display conventions (not claims)

- B03 renders the token as `' strawberry'` **with visible quote marks** so the
  leading space is legible. The token itself is `" strawberry"` — the quotes are
  typography, not part of the string. The "11 characters" count excludes them.
- BTHX quotes all three pieces (`'Thank'`, `' you'`, `'!'`) with the same
  typographic quotes as B03, so the leading space in `' you'` shows as a gap
  inside the quotes. The terracotta underscore marks that space cell and is
  not a character in the token.
- B04 sets `unbelievable` and `raspberry` against their token rows; the
  strawberry row is not re-shown, so "the same token as in strawberry" is carried
  by the label, sourced above.
- B04's middle-dot form (`un · believe · able`) uses the dots as separators for
  legibility; they are not characters in the strings. The same goes for the
  middots in captions and labels (e.g. "GPT-4 tokenizer · cl100k_base").

## Claims deliberately NOT made

- Not claimed: that Claude gets these questions wrong. S2 and S3 are both
  **correct answers**, and B05 says so. The reel claims only that tokenization
  explains why character-level counting is *unreliable*.
- Not claimed: that these ids are Claude's tokens. See the callout above.
- Not claimed: any accuracy rate, benchmark, or frequency statistic. No such
  number appears on screen, because no source here supports one.
- **B06 — claimed:** that Claude's narrated grouping (straw/ber/ry) and the
  tokenizer's split (str/aw/berry) cut the same ten letters in different
  places, and that both yield the correct count of 3. Both halves are on the
  record: S2 for the narration, S1 for the tokens.
- **B06 — NOT claimed:** that straw/ber/ry are tokens, of any vocabulary. They
  are shown without ids for exactly this reason.
- **B06 — NOT claimed:** that Claude's answer was wrong, or that its stated
  reasoning was dishonest. The claim is narrower and is the point of the beat:
  a correct, fluent explanation is not a view of the mechanism underneath.
- **B04 — claimed:** that `belie` and `vable` are not meaning-aligned
  pieces of *unbelievable*. **NOT claimed:** that `belie` is meaningless.
  *Belie* is a real English word, and B04's narration says so (corrected
  25 Sep 2026; the earlier line "belie and vable don't mean anything" was
  false). B04's on-screen text never made the meaningless claim, and still
  doesn't.
- **BOUT — claimed:** the reader and the model reach the same count (3; the
  model's answer is S2) from different inputs: letters vs. `str`/`aw`/`berry`. **NOT claimed:** that
  the model counts by inspecting these tokens, or any mechanism beyond
  "these are the units it receives".
- **BTHX — claimed:** `cl100k_base` splits "Thank you!" into `Thank` 13359 ·
  ` you` 499 · `!` 0 (S4), and the space belongs to the second token.
  **NOT claimed:** a token count in narration (none is spoken), or that Claude's
  tokenizer splits it this way.
- **B06 — NOT claimed:** that Claude's *own* tokenizer would produce
  str/aw/berry. It would not necessarily; those are GPT-4's. B05 states this
  on the record immediately before B06 runs.
