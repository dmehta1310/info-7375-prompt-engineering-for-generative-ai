# SOURCES: what I used, and who did what (JS2)

## Data
- Public job-board APIs, opened in my browser on 2026-11-09: Greenhouse `boards-api.greenhouse.io/v1/boards/stripe/jobs`, Lever `api.lever.co/v0/postings/palantir?mode=json`, Ashby `api.ashbyhq.com/posting-api/job-board/linear`, and the deliberately bad Greenhouse board `this-board-does-not-exist-js2` (404). The agent's saved raw responses are in `out/runs/`.
- Persona: Priya Nair, fictional (from my JS1). No real résumé, contacts, or tracker.
- I started from my own Job-Search Agent 1, not from the Reallocation Engine or Lectern.

## Claude (Anthropic)
1. **Tutoring chat** (claude.ai, my Prompt AI project), 2026-11-09:
   - Suggested the boards (I checked them in my browser) and proposed the budget (5 boards / 10 requests / 60 s), which I accepted.
   - Gave me options for GATE.md and turned my picks into its sentences.
   - **Wrote all the code and tests** in `agent/` and `tests/`, and ran the tests in its own sandbox with a fake network while writing them. I ran every test and run on my own machine.
   - Wrote the review-packet test (`tests/test_review_timeout.py`) before the fix.
   - Drafted RUNS.md, REVIEW_PACKET.md, README.md, and this file from my real outputs; I checked the numbers.
2. **Claude Code 2.1.303** (2026-11-09 15:37 EST): made the one change in the review packet (`agent/loop.py`, 6 lines), with read/edit tools only. Prompt and reply are in `evidence/review/`.

## What stayed mine
The GATE.md rules (boards, error policy, approval rule, accepting the budget); my 16 boundary predictions, including the 4 that were wrong; running every command; approving the state file; reading the diff; and the decision to accept Claude Code's fix.

## Other tools
Python 3.12.7, git/GitHub, macOS Terminal. No other AI tools.
