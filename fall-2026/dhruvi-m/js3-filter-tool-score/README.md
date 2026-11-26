# Job-Search Agent 3: The Filter, the Tool, and the Score
Decides which collected postings reach me and why: a **filter I can read** (FILTER.md), a **reject audit judged by hand**, a **source-grounded shortlist**, my agent offered to Claude as an **MCP tool server written from scratch**, and a **score whose numbers I can account for**, changed one object at a time and measured on held-out labels. Persona: **Priya Nair** (fictional; data analyst, 2 years' experience, US-based).

**Started from:** my Job-Search Agent 2 (`../js2-loop-tools-diff/`) and its saved raw responses from 2026-11-09 (1,107 postings: Stripe/Greenhouse 771, Palantir/Lever 304, Linear/Ashby 32; plus the deliberately failing board, which is reported as "not judged").

## Language, toolchain, setup
- **Python 3.12.7**, standard library only. **Setup: none.**
- git · Claude Code 2.1.303 (`claude -p`, model **claude-sonnet-5-5**, pinned) · Node/npx (only to run the official filesystem MCP server for the evaluation) · macOS Terminal.
- The commands below read `../js2-loop-tools-diff/out/runs/2026-11-09T220326Z_LIVE/raw`, which is in the same repo.

## Exact commands (from a fresh clone)
- `git clone https://github.com/dmehta1310/info-7375-prompt-engineering-for-generative-ai.git`
- `cd info-7375-prompt-engineering-for-generative-ai/fall-2026/dhruvi-m/js3-filter-tool-score`
- `python3 -m unittest discover -s tests -v` runs all tests (no network)
- `python3 agent/run_filter.py --raw ../js2-loop-tools-diff/out/runs/2026-11-09T220326Z_LIVE/raw --filter config/filter_v2.json` runs the filter on everything
- `python3 agent/audit.py report` shows the reject audit against my hand verdicts
- `python3 agent/measure.py --part heldout config/filter_v1.json config/filter_v2.json` measures on held-out labels
- `python3 agent/shortlist.py` writes SHORTLIST.md
- `python3 agent/mcp_client.py --name own --calls mcp/own_calls.json -- python3 agent/mcp_server.py` talks to my MCP server and saves the transcript
- `python3 agent/claude_judge.py --label R1_base --prompt prompts/judge_v1.txt --context full --model claude-sonnet-5-5` re-runs a Claude judgment (needs Claude Code logged in)

## What ran (all real, dated by commit)
| What | Result | Where |
|---|---|---|
| FILTER.md v1, before any code | title words + US location; evidence rules; "I cannot tell"; 4 wrong versions | FILTER.md, `24a0b4b` |
| Filter v1 on all postings | 27 relevant, 2 cannot tell, 1,078 rejected | `out/v1/`, `8278070` |
| Reject audit (69 judged by me) | 2 of 30 random rejects wrong (95%: 2%–21%); false friend "Analyst" | AUDIT.md |
| Rule changes on dev labels | added "North America" (v2); rejected years ≤ 2, cutting "Analyst", 3+ skills | FILTER.md, AUDIT.md |
| Shortlist (v2) | 28 postings, 140 claims: 108 supported, 15 contradicted, 17 insufficient | SHORTLIST.md |
| MCP server + 2 evaluations | my 1-tool read-only server (all 4 bad calls refused; used by Claude Code) vs. official filesystem server (16 tools, can write) | MCP_EVALUATION.md |
| Claude judge, one change at a time, held-out | R1_base 21/35, R2_prompt 26/35, R3_context 24/35 | SCORE_REPORT.md |

## Before → after: what improved over JS2
| | JS2 | JS3 |
|---|---|---|
| What reaches me | every new posting, plus one fixed rule | a versioned FILTER.md with a reason per rule, and every rule added or rejected **after measuring** |
| Knowing what the filter misses | nothing | hand-judged audit of 30 random rejects + close calls + all kept, with an honest interval |
| Explaining a result | a verdict | every shortlist claim labeled supported / contradicted / insufficient, with a quote |
| Claude's role | Claude Code made one code change | Claude judges postings **by script**, model pinned, every reply saved; Claude Code used my agent **as a tool** |
| Years rule (JS1 feedback) | added, tested on 8026689 | re-tested on my own labels and **rejected with evidence** (dev 20/34 vs 31/34) |

## Sign-off — Job-Search Agent 3
**Checked** (each with *how*)
- **Filter rules and the 4 wrong versions** → `tests/test_filter.py` (e.g. `test_L2_not_us_and_W1_contains_us_is_fooled`, `test_C1_missing_location_and_W2_missing_as_us`, `test_T2_lowercase_matches_W3_case_sensitive_does_not`, `test_T3_inside_another_word_no_match_W4_substring_does`). *How: with Claude's help*: Claude wrote the tests from my FILTER.md; I ran them.
- **The filter's errors** → 69 postings judged **by hand**, filter verdict hidden (AUDIT.md).
- **Audit numbers** → *by recomputation*: `agent/audit.py report` recomputes them from my saved verdicts.
- **Rule changes** → *by recomputation* on dev labels, then once on held-out (`agent/measure.py`).
- **MCP server refuses what it should** → `tests/test_mcp.py` (`test_R1_path_escape_refused`, `test_R2_extra_argument_refused`, `test_M4_unknown_method_and_unknown_tool`) and the real transcript. *How: with Claude's help* (Claude wrote the server and tests; I ran them and read the transcript).
- **Claude judge** → every reply saved with model and date; compared with my labels *by recomputation*.

**Not checked**
1. **The miss rate for all 1,078 rejects.** I only have 30 random rejects; the true rate could be anywhere from about 2% to 21%.
2. **Whether my own labels are consistent.** I judged once; I did not re-judge a sample later to check that I'd give the same answers. For 8026689 my reason code contradicts the location field.
3. **Claude's run-to-run variation, properly.** I have one extra R1 summary line, not a planned repeat of every run.
4. **The years parser on words.** 10 postings state years in words ("five years"); the parser reads digits only.
5. **The filesystem server beyond 5 calls.** I did not test symlinks, large files, or its other write tools.

**Not claiming**
- That my filter or Claude finds **every** job worth Priya's time, or that the shortlist verdicts are **true**: they are consistent with my rules and labels, nothing more.
- That anything was **trained**: no model was trained or fine-tuned here.
- That results carry over to other boards, other days, or a real applicant.

**Signed:** Dhruvi Mehta, 2026-11-25

## Driver's seat
| Part | What Claude should do | What I should do | Why it stays mine | Evidence |
|---|---|---|---|---|
| The filter | Turn my picks into FILTER.md; write the code and tests | Choose the rules and wrong versions; decide which changes to keep after measuring | What "relevant" means for Priya is my definition | FILTER.md `24a0b4b`; dev decisions `d66395f` |
| The audit | Draw the sample; show the facts; compute intervals | **Judge every posting myself**, with the filter's answer hidden | The audit only means something if the verdicts are mine | `audit/v1_hand_verdicts.json`, `37efc38` |
| The shortlist | Label claims against the posting text, with quotes | Read the labels; decide whether a posting is worth my time | Relevance is not entailment: matching words is not a reason to apply | SHORTLIST.md |
| The tool | Write the server and client | Decide what it may read, write and send; make the trust decisions | A tool that can act on my files needs my permission, not the model's | MCP_EVALUATION.md, `a7c6f63` |
| The score | Run the judge by script, pinned model, saved replies | Pick what to change, one thing at a time; read held-out results | **The judgment that a posting is worth my time stays mine**: Claude's verdicts are compared *against* my labels, never used *as* them | SCORE_REPORT.md, `69e5519` |

**Fresh-clone test:** see `evidence/fresh_clone_test.txt` (tests run from a new clone of GitHub).
