# Temperature as a Concentration Control

**Student:** Dhruvi Mehta
**Course:** INFO 7375 — Prompt Engineering for Generative AI
**Assignment:** Week 1 Video Explainer

## Concept

This video explains **temperature as a concentration control** in language model sampling. The core idea: temperature reshapes how *confident* a model sounds, not *which* answer it picks.

Three steps happen when temperature is applied to a set of logits:

1. **Division** — each logit is divided by the temperature value.
2. **Exponentiation** — dividing by a smaller temperature widens the gaps between logits; exponentiating amplifies those widened gaps further.
3. **Normalization (softmax)** — the exponentiated values are turned into a probability distribution that sums to 100%.

The critical point demonstrated in the video: temperature never changes *which* logit is highest, only how concentrated or spread out the resulting probability distribution is around that same winner.

## Real numbers used

Using logits `[1, 2, 3]` (via `lessons/01-randomness-and-first-prompts/code/main.py` from the course repo), the video shows the actual softmax percentage on the top logit at three temperatures:

| Temperature | Top logit confidence |
|---|---|
| 0.2 | 99.3% |
| 1.0 | 66.5% |
| 2.0 | 50.6% |

Lower temperature sharply concentrates probability on the top candidate; higher temperature spreads probability more evenly across alternatives — but the ranking (which logit is "best") never changes.

## Structure

The video follows the `ai-explainer` beat format:
- Cold open
- BLUF / misconception-correction beat
- Body (mechanism beats: division → exponentiation → normalization)
- Verdict
- "Your turn" handoff
- Title-restate outro

Built with the Brutalist toolkit (`nikbearbrown/brutalist.art`), audio generated locally via Kokoro TTS, custom Remotion/Manim scenes for the mechanism beats.
