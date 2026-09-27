# PROMPTS — Less Room to Wander

**Open slots: none.** Every beat renders from an existing Remotion composition with props in `beat_sheet.json`; there are no generation prompts, no pantry requests and no paid calls.

Prompts that appear on screen (recorded here so they can be checked word for word):

- **B00 (the actual run, shown in a reconstructed composer):** "Run main.py's sample() at temperature 1.0 and 0.5: logits [1, 2, 3], seed 7, 1,000 draws. How far is the top token from its expected count?" In reality the runs were done in Claude Code (Opus 5.5): temperature 1.0 as `python3 lessons/01-randomness-and-first-prompts/code/main.py` (unedited); temperature 0.5 by importing the unedited `probabilities()` / `sample()` and passing `temperature=0.5`.
- **BHTF (viewer handoff):** "I ran a softmax sampler on logits [1, 2, 3], 1,000 draws, seed 7, at temperatures 1.0 and 0.5, and compared the top token's expected and observed counts. Help me design a follow-up: (1) repeat the comparison across 20 different seeds and add temperature 2.0, (2) report each gap in standard deviations, (3) tell me whether the 'gap shrinks' pattern survives or was one seed's luck."
