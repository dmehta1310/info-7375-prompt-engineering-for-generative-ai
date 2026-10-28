# Sampling report (Chapter 1)

**Date run:** 2026-10-28 (UTC times in `responses/log.csv`)
**Where:** claude.ai, a new incognito chat for every run (not inside my Prompt AI project)
**Model shown in the chat:** not recorded. I did not take screenshots of the chats, so I cannot prove which model answered.
**Prompt:** `prompts/judge_v1.txt` (filled copies in `prompts/filled/`)
**Postings:** 5 from the manual snapshot `evidence/manual-snapshots/stripe_2026-10-27T232715Z.json`
**Runs:** 4 per posting = 20 replies, saved in `responses/v1_<id>_run<n>.json`
**Summary table:** `evidence/sampling_summary.txt` (made by `agent/sampling_summary.py`)
**My hand labels:** `labels/sampling_hand_labels.json`, using `LABELING_RULE.md` (written before labeling)

## Results

| Posting | Title | My hand label | Agent rule | Claude verdicts (4 runs) | Valid |
|---|---|---|---|---|---|
| 8189909 | Data Analyst, NYC | not relevant | not relevant | not relevant ×4 | 4/4 |
| 5416444 | Data Analyst (Canada) | not relevant | not relevant | not relevant ×4 | 4/4 |
| 8222149 | Data Scientist (Seattle) | not relevant | not relevant | not relevant ×4 | 4/4 |
| 8026689 | Internal Audit Data Analytics Lead | not relevant | **relevant** | not relevant ×4 | 4/4 |
| 7440963 | Data Science Manager | not relevant | not relevant | not relevant ×4 | 4/4 |

## How much did the answers vary?
- **Verdict:** no variation. 20 of 20 replies said "not relevant".
- **Format:** 20 of 20 replies passed the validator.
- **Cited fields:** these changed between runs on 4 of 5 postings. Only 7440963 cited exactly the same fields all 4 times. Example: on 5416444, runs 1 and 3 cited `years_experience` but runs 2 and 4 did not.
- **Reasons:** same meaning, different wording each run.

## What I can conclude
- On these 5 postings, Claude's verdict was **repeatable** (same answer 4/4 every time).
- Claude's verdict matched **my hand label 20/20**. My agent rule matched my hand label **4/5**. It missed 8026689 because the rule never checks years of experience (that posting asks for 5–10 years).

## What I cannot conclude
- **Repeatable is not the same as correct.** Agreement with my labels comes from only 5 postings.
- **Claude never said "relevant" here**, and my labels never said "relevant" either. So this sample tells me nothing about how Claude handles a real match.
- The **reasons are not stable**, so I can't rely on the cited fields being the same next time.
- One model, one interface, one day, one persona. I did not control or record settings like temperature.

## Limits of how I collected this
- Saving the replies was manual. Run 1 of 8189909 was pasted into a file in VS Code, and run 3 was typed in from the chat after the clipboard kept being overwritten. From job 5416444 on, I pasted each reply into my tutoring chat and saved it with a heredoc command. The text is Claude's reply as returned, but the log shows **save time, not reply time** (marked `via-chat` / `saved-by-hand` / `unknown-time-before-logger`).
- Some early attempts saved the wrong text (my prompt or a command). The validator rejected them, and I deleted them. They are not counted (see FRICTIONAL.md).
- The v1 prompt's persona says "see rule 3", but the prompt does not include rule 3.

## In my own words
There were two surprises. First, Claude gave the same verdict on all 20 runs, even though its reasons and cited fields changed. Second, it was much easier than I expected to save the wrong text by accident. Several times my clipboard held my prompt or a command instead of Claude's answer. I learned that getting the same answer every time does not mean it is correct. My rule never checked years of experience, so it wrongly marked 8026689 as relevant. I also learned that I need to read the actual job text myself instead of relying on guesses. Next time I will take screenshots and write down the model name for each run.

*(I picked these points from a list of options; Claude turned them into sentences; I then rewrote them myself in VS Code, and Claude corrected facts my rewrite had accidentally changed.)*
