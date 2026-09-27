# PROMPTS — temperature-is-concentration

Beat-prefixed prompts. **There are no open media slots in this reel** — every
beat renders deterministically from `scenes.py` or a registered Remotion
composition, so no beat is waiting on a generated or human-supplied asset.
This file therefore records (a) the two in-reel Claude prompts that appear ON
SCREEN as part of the film, and (b) the authoring prompt that produced the
build, so the reel is reproducible.

## On-screen prompts (these are content, not requests)

**B00 — the cold-open ask** (typed into the composer; no answer is shown — see `SOURCES.md`):
```
Chapter 1 gives me a softmax over the scores 1, 2, 3 and a temperature knob.
Show me exactly what temperature changes and what it leaves alone — using the
ratio between two outcomes, not a creativity metaphor. Then name the one thing
that explanation still cannot establish.
```

**B03 — the question the B04 figure answers** (B04 is the reel's own Manim scene, not a Claude output):
```
Plot p2/p0 for the softmax over scores [1, 2, 3] at T = 0.5, 1, 2. Show the
score gap staying fixed at 2 while only T changes, and check each ratio
against exp(2/T).
```

**B07 — the HANDOFF prompt** (read aloud verbatim, then discussed):
```
Take a softmax over the scores [1, 2, 3]. Compute p2/p0 at T = 0.5, 1, and 2,
and check each value against exp(2/T). Now change ONLY the middle score, to
2.5, and recompute: tell me which ratios moved, which stayed fixed, and why
the fixed one had to stay fixed.
```

Why that handoff is worth running: the middle score is the one that does NOT
appear in p₂/p₀, so changing it moves every probability but leaves that one
ratio exactly where it was. The viewer discovers the identity by breaking
everything around it.

## Open slots

None. `./art todo <reel>` should report zero beats needing fill. If it reports
any, that is a bug in this shotlist, not a missing asset.

## Build authoring prompt

The paste-ready prompt that rebuilds this reel end to end lives in
`BUILD-PROMPT.md` (also shipped as an assignment deliverable).
