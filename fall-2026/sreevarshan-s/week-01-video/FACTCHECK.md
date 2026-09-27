# FACTCHECK — week-01-token-not-word

Every claim spoken or shown, with the file that backs it. Regenerate the
evidence with the scripts in `evidence/`; all three print their own run date.

| # | Claim on screen / in narration | Source | Verified |
|---|---|---|---|
| 1 | "strawberry" contains 3 r's, at positions 2, 7, 8 | `evidence/token_split_demo.txt` (computed in Python from the string) | yes |
| 2 | The prompt "How many r's are in strawberry?" is 8 tokens | `evidence/prompt_tokens_demo.txt` | yes |
| 3 | Those token ids are 4438, 1690, 436, 596, 527, 304, 73700, 30 | `evidence/prompt_tokens_demo.txt` | yes |
| 4 | Inside that prompt the word is carried by ONE token, id 73700 | `evidence/prompt_tokens_demo.txt` | yes |
| 5 | The letter r appears as its own token (` r`, id 436) | `evidence/prompt_tokens_demo.txt` | yes |
| 6 | Both cl100k_base and o200k_base agree the word is 1 token in context | `evidence/prompt_tokens_demo.txt` | yes |
| 7 | Bare "strawberry" is 3 tokens: `str`/`aw`/`berry`, ids 496, 675, 15717 | `evidence/token_split_demo.txt` | yes |
| 8 | Those pieces hold 1, 0 and 2 r's respectively | `evidence/token_split_demo.txt` | yes |
| 9 | o200k_base splits the same word `st`/`raw`/`berry`, ids 302, 1618, 19772 | `evidence/token_split_demo.txt` | yes |
| 10 | id 73699 = `' Smoking'`, 73701 = `' CMP'` | `evidence/id_is_arbitrary_demo.txt` | yes |
| 11 | `' straw'` is id 31107, unrelated to 73700 | `evidence/id_is_arbitrary_demo.txt` | yes |
| 12 | Claude answered "There are 3 r's in "strawberry" (strawberry)." | `evidence/claude_response.md` | yes — verbatim, student-supplied |
| 13 | That response was claude.ai web chat, Claude Sonnet 5, September 22, 2026 | `evidence/claude_response.md` | student-attested |
| 14 | The answer was correct | claims 1 and 12 agree | yes |

## Deliberately NOT claimed

- **Not claimed:** that Claude's tokenizer splits this word this way. Anthropic
  does not publish it. B09 says so on screen.
- **Not claimed:** that tokenization caused this particular answer. The answer
  was correct; nothing here shows the mechanism that produced it.
- **Not claimed:** that letter-counting is unreliable in general. We ran one
  prompt, once, and it succeeded. No failure was observed, so none is shown.
- **Not claimed:** that the 3-token split applies in prose. It does not — with a
  leading space the word is 1 token. Both facts are shown, in B03 and B04.

## Constructed material

B07 only. Labelled "CONSTRUCTED ILLUSTRATION — not tokenizer output" on screen
for the beat's full duration, and named as constructed in the narration.

## Provenance of the numbers

`tiktoken` 0.14.0, Python 3.11.14, run 2026-09-22 in the brutalist.art `.venv`.
Encodings `cl100k_base` (GPT-4/3.5-turbo) and `o200k_base` (GPT-4o).
Toolkit revision `ba2d0e0f043f5b3b35a50d336e0fc66fbfecfc0c`.
