# SHOTLIST — week-01-token-not-word

Typed work order. Every beat is a reel-local Manim scene in `scenes.py`; there
are no human-filled slots, no stock, no AI-generated video, no screen capture.

| Beat | Scene class | Type | Owner | Status |
|---|---|---|---|---|
| B00 | `B00_ColdOpen` | GRAPHIC / manim | pipeline | authored |
| B01 | `B01_ClaudeTranscript` | GRAPHIC / manim | pipeline | authored — renders the real dated transcript |
| B02 | `B02_TextToIntegers` | GRAPHIC / manim | pipeline | authored |
| B03 | `B03_PromptTokens` | GRAPHIC / manim | pipeline | authored |
| B04 | `B04_IsolatedSplit` | GRAPHIC / manim | pipeline | authored |
| B05 | `B05_TwoVocabularies` | GRAPHIC / manim | pipeline | authored |
| B06 | `B06_IdIsArbitrary` | GRAPHIC / manim | pipeline | authored |
| B07 | `B07_ConstructedLetterVsToken` | GRAPHIC / manim | pipeline | authored — constructed, stamped |
| B08 | `B08_LearnedNotGiven` | GRAPHIC / manim | pipeline | authored |
| B09 | `B09_NotEstablished` | GRAPHIC / manim | pipeline | authored |
| B10 | `B10_EndCard` | GRAPHIC / manim | pipeline | authored |

**Open human slots: none.** Nothing in this reel falls to a slate.

## Why reel-local Manim rather than library components

`./art scenes` was run first, per CLAUDE.md rule 8, for "word splitting into
subword token chunks", "chat transcript with model response" and "sentence
broken into labelled boxes". All returns were other films' figures scoring
4.0–5.5 — leads, not matches. No tokenization component exists in the library,
so this is a genuine miss. Authoring Remotion components would have meant
editing the shared public toolkit tree; `scenes.py` lives in this reel folder
and modifies nothing outside it.

## Palette and accessibility

Cream `#F2F0E9` ground, warm ink `#3D3929` body text, terracotta `#D97757` as
the single accent. Gold is never used as a text colour (Gate W1). Layout uses
`arrange()`/`move_to` to stay inside the safe area.
