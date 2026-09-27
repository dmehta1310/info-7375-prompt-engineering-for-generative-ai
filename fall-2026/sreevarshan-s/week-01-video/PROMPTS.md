# PROMPTS — week-01-token-not-word

## Generation prompts for open slots

**None.** Every beat is pipeline-rendered Manim from `scenes.py`. No beat
requires a generated clip, a stock image, an archival asset or a screen
capture, so there are no beat-prefixed generation prompts to fill.

## The one prompt that was actually sent to a model

Sent by the student in claude.ai web chat, not by the pipeline:

```text
How many r's are in strawberry?
```

Response, provenance and verbatim text: `evidence/claude_response.md`.
It is the only model output in this reel, and it appears on screen in B01
exactly as received.

## Prompts NOT used

- No image-generation prompts.
- No text-to-video or image-to-video prompts.
- No paid API calls of any kind.
- No prompt was used to write or embellish the on-screen numbers; those come
  from `tiktoken` stdout captured in `evidence/`.

## Build direction

The full build instruction given to Claude Code, and every command run, are
recorded in `BUILD-PROMPT.md`.
