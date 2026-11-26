# What moves the score (Chapter 9)

## Where every number came from
| Number / object | Value | Origin |
|---|---|---|
| Title words | Analyst, Data Scientist, Data Science, Analytics | **hand-set** (my FILTER.md v1; I widened to any "Analyst") |
| US places list | 50 states, abbreviations, ~45 cities, "US/USA/United States" | **hand-set** by Claude, from my JS1 list (**inherited**) |
| "North America" counts as US | v2 | **fitted on my dev labels** (31→32/34) |
| Years ≤ 2, 3+ skills | tried, rejected | **inherited** from my JS2/JS1 rules, rejected on dev labels |
| Years parser | digits only, 1–30 | **hand-set**; misses years written in words (10 postings) |
| Audit sizes | 30 random rejects, 10 close calls, all kept | 30 = **assignment minimum**; 10 = **hand-set** |
| Seed | 7375 | **inherited** from JS1 |
| 95% Wilson interval | z = 1.96 | **inherited** (standard formula) |
| Claude prompt v1 / v2 | `prompts/judge_v1.txt`, `prompts/judge_v2.txt` | **hand-written** by Claude; v2 adds "Priya's own rule", written from my **dev-label** findings |
| Posting text sent to Claude | first 4,000 characters | **hand-set** |
| Model | claude-sonnet-5-5 | **setting**, pinned with `--model`, and recorded per call |

## One change at a time, measured on my 35 held-out labels
Every call ran by script (`agent/claude_judge.py`), from an empty temporary folder so Claude could not read my files, with model, settings, date and raw reply saved per posting in `out/claude/<run>/`. Commit: `69e5519`.

| Run | Agree | Shown, I said no | Hidden, I said yes | "?" / unparsed | Model reported | Started |
|---|---|---|---|---|---|---|
| R1_base | 21/35 | 0 | 14 | 0 | claude-sonnet-5-5 | 2026-11-26T01:13 UTC |
| R2_prompt | 26/35 | 1 | 8 | 3 | claude-sonnet-5-5 | 2026-11-26T01:13 UTC |
| R3_context | 24/35 | 0 | 11 | 12 | claude-sonnet-5-5 | 2026-11-26T01:13 UTC |

- **R1 → R2 changes only the prompt** (adds Priya's own rule). **R1 → R3 changes only the context** (title + location, no posting text). Same model, same 35 labels.
- For comparison, my **filter v2** on the same held-out labels: 31/35 (no Claude at all).
- **An earlier R1 run** (same prompt, model and labels) finished with **21/35 (hidden, I said yes: 14)** before I re-ran all three runs in parallel; its files were deleted by the re-run, and only the printed summary line remains (FRICTIONAL.md).

## What persistence is not proof of
If Claude gives the same answers tomorrow, or remembers Priya across sessions, **that does not mean anything was trained.** Nothing in this project trains or fine-tunes a model. Same answers come from the same prompt, context, model and settings; different answers come from changing one of those (or from sampling randomness). A changed behavior across sessions could also come from a different model version, a different system prompt, or saved context, so it must be explained by one of those objects, not by "it learned."

## R1 ran twice
The first R1 run (deleted by the parallel re-run) and the re-run gave the **same summary: 21/35, hidden-but-I-said-yes 14**. The answers repeated because the prompt, context, model and settings were the same, **not because Claude learned anything** between runs. Two runs are too few to measure how much answers vary in general.
