# SOURCES: what I used, and who did what

## Data
- **Stripe's public Greenhouse job board API:** https://boards-api.greenhouse.io/v1/boards/stripe/jobs?content=true. I opened it in my browser myself (screenshot: `evidence/manual-snapshots/board_in_browser.png`) and saved a manual snapshot on 2026-10-27 (commit c701b05). Every posting I hand-labeled, I read in its printed text.
- **Persona:** Priya Nair is invented (@example.com email, 555 phone). No real résumé was used.

## Claude (Anthropic), two roles
1. **Tutor/builder chat** (claude.ai, my Prompt AI project), 2026-10-27 to 2026-10-28:
   - Wrote all code in `agent/` and `tests/`. I ran every command and test myself.
   - Asked questions and pressure-tested my CONTRACT.md. I wrote the contract.
   - Gave me multiple-choice options for my labeling rule, report conclusions, FRICTIONAL.md, and sign-off. I picked; Claude turned my picks into sentences.
   - Drafted the factual parts of SAMPLING_REPORT.md, EXPERIMENT_REPORT.md, ACTION_SURFACE.md, and README.md from my real results. I checked them.
   - When I rewrote my sampling reflection myself, a few facts changed by accident. Claude pointed them out and they were corrected (commit 91fc49e).
2. **Judge** (claude.ai, a new incognito chat per run): produced the 20 sampling replies, the 30 experiment replies, the 16 run-2 replies (one per new posting), and 1 file-upload reply. These are **model judgments**, not facts. The model name was not recorded.

## Other tools
- Python 3, git/GitHub, VS Code, macOS Terminal. No other AI or rewording tools.

## What stayed mine
CONTRACT.md; the persona title choices; every hand label; the labeling rule thresholds and the rule v2 change; which v2 prompt change to test; choosing option 3 as the least autonomy; my picks for every reflection, and my own rewrite of the sampling reflection; running every command and every Claude chat.
