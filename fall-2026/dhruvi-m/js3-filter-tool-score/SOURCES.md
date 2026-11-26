# SOURCES (JS3): what I used, and who did what

## Data
- My own JS2 agent's saved raw responses (2026-11-09): Stripe (Greenhouse), Palantir (Lever), Linear (Ashby), 1,107 postings. No new collection in JS3.
- Persona Priya Nair: fictional. No real résumé, contacts, tracker or transcripts.
- I started from my JS2 agent, not from the Reallocation Engine or Lectern.

## Claude (Anthropic)
1. **Tutoring chat** (claude.ai, my Prompt AI project), 2026-11-20 to 2026-11-25:
   - Suggested starting from my JS2 data (I accepted) and the "Remote alone = I cannot tell" detail; turned my picks into FILTER.md.
   - **Wrote all code and tests** in `agent/` and `tests/`, the prompts in `prompts/`, and the MCP call scripts in `mcp/`; ran them in its own sandbox on fake data while writing them. Every real run was on my machine.
   - Suggested the reason codes 1–8 and built the one-line judging sheet; **I chose every verdict and code**. Pulled facts (location, role line, years, skills) out of postings for me; it did not give me verdicts.
   - Proposed the 4 candidate rule changes; **I decided** to keep A and reject B, C and D.
   - Wrote the prompts; v2's "Priya's own rule" was written from my dev-label findings.
   - Wrote `agent/make_docs.py`, which writes README.md, AUDIT.md, MCP_EVALUATION.md, SCORE_REPORT.md from my result files, and wrote the sentences in FRICTIONAL.md from events I confirmed.
2. **Claude Code 2.1.303, model claude-sonnet-5-5** (pinned with `--model`, recorded per call):
   - judged my 35 held-out postings by script (`agent/claude_judge.py`; raw replies in `out/claude/`);
   - acted as an MCP client of my server (`out/mcp/claude_code_as_client.json`).

## Other tools
Python 3.12.7, git/GitHub, macOS Terminal, Node/npx with `@modelcontextprotocol/server-filesystem` 2.4.0 (evaluated only, on a `/tmp` test folder). No other AI tools.
