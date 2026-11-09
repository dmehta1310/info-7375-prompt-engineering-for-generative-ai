# Job-Search Agent 2: The Loop, the Tools, and the Diff
A bounded agent loop that watches **3 public job boards on 3 different applicant-tracking systems** (Greenhouse, Lever, Ashby) plus **1 board that fails on purpose**, under a permission policy enforced in code. Persona: **Priya Nair** (fictional; `persona/priya_nair.json`).

**Started from:** my Job-Search Agent 1 (`js1-contract-and-watch/`): its persona, and its watcher as a reference (`agent/js1_watch_reference.py`, not used by the JS2 code). The JS2 loop, policy, checker, and tests are new.

## Language and toolchain
Python 3.12.7 (standard library only: `urllib`, `json`, `unittest`; no packages to install) · git · Claude Code 2.1.303 (review packet only) · macOS Terminal.

## Exact commands (from a fresh clone)
- `git clone https://github.com/dmehta1310/info-7375-prompt-engineering-for-generative-ai.git`
- `cd info-7375-prompt-engineering-for-generative-ai/fall-2026/dhruvi-m/js2-loop-tools-diff`
- `python3 -m unittest discover -s tests -v` runs all 28 tests (no network needed)
- `python3 agent/run.py` is a **live** run of `config/boards.json`; it writes `out/runs/<UTC time>_LIVE/` and does **not** change `state/`
- `python3 agent/check.py out/runs/<run folder>` is the **independent check** of a run
- `python3 agent/run.py --approve out/runs/<run folder>/state_proposal.json` accepts a run's job IDs into `state/seen_ids.json` (**my approval**)
- `python3 agent/run.py --seed out/seed_empty_stripe --boards config/boards_demo.json --wrong-empty-rule` is the **seeded** finished-wrong demo

## What ran (2026-11-09; details in RUNS.md)
| What | Where | Result |
|---|---|---|
| Live run, 4 boards incl. deliberate 404 | `out/runs/2026-11-09T203507Z_LIVE/` | `incomplete`; stripe 771, palantir 304, linear 32, bad-board failed not-found; 4 requests, 2.0 s |
| Finished-wrong demo (SEEDED, wrong version) | `out/runs/2026-11-09T203530Z_SEEDED-WRONG-VERSION/` | agent said `finished`; independent check **FAIL** (stripe 0 vs 771) |
| Same seeded data, correct version | `out/runs/2026-11-09T203531Z_SEEDED/` | `incomplete`, stripe `suspicious-empty` |
| Tests | `evidence/test_run_1.txt`, `evidence/review/4_after_fix_all_tests.txt` | 27 OK, then 28 OK after the review fix |

## Where things are
GATE.md (rules, written first: commit 8adaf50) · BOUNDARY_TESTS.md (16 predicted cases) · RUNS.md (trace + demo) · REVIEW_PACKET.md (Claude Code change) · `agent/` (code) · `tests/` · `config/` · `out/runs/` (traces + saved raw responses) · `state/seen_ids.json` · SOURCES.md · FRICTIONAL.md

## Sign-off — Job-Search Agent 2
**Checked, and how**
- Permission policy: hosts, https, GET only, credentials, `..`, prefix trick, symlink, read vs write, approval → `tests/test_policy.py` B01–B16, **predicted before running** (commit ab832d1), then run (commit f05890c).
- Exits, budgets, repeat rule, error policy → `tests/test_loop.py` (e.g. `test_404_not_retried_and_no_invented_value`, `test_server_error_retried_once_and_counted`, `test_request_budget_exhausted`, `test_time_budget_exhausted`, `test_repeat_blocked`, `test_empty_board_is_suspicious_not_finished`).
- A real run handled the deliberate failure without inventing a value → live run above, recounted **by an independent script** (`agent/check.py`, which does not import the agent's code).
- A finished-wrong answer is caught → seeded demo, independent check FAIL.
- Claude Code's fix → `test_R1_request_timeout_never_exceeds_time_left`, written and committed **before** the patch (7b921d3): failed before, passed after; all 28 tests pass.
- How: the tests were written by Claude (my tutoring chat), not by me. My own parts were the GATE rules, the predictions before running, running every command myself, and the accept decision for the Claude Code change.

**Not checked**
1. **Total download time.** The timeout limits each wait for data, not the total; a server trickling a large response slowly is not tested (REVIEW_PACKET.md §8).
2. **Only one machine, one day.** I ran the agent on my laptop on 2026-11-09 only; other days, networks, and boards were not tried.
3. **The finished-wrong demo used seeded data.** I did not see a real board return empty; Stripe's empty response was simulated and labeled SEEDED.

**Not claiming**
- That the agent finds **relevant** jobs for Priya. JS2 counts and diffs postings; it does not judge relevance.
- That it works on boards or applicant-tracking systems **beyond these three**.

**Signed:** Dhruvi Mehta, 2026-11-09

## Driver's seat
| Part | What Claude should do | What I should do | Why it stays mine | Evidence |
|---|---|---|---|---|
| Loop rules (exits, budgets, errors, permissions) | Offer options; turn my picks into sentences | Choose the rules; accept or change the budget | The rules decide what counts as success; that judgment is mine | GATE.md, commit 8adaf50 (before any code) |
| Loop code and tests | Write the code and tests | Predict boundary results before running; run everything myself | A prediction only counts if it comes before the result | BOUNDARY_TESTS.md, commits ab832d1 → f05890c |
| Live run and approval | Nothing (the code runs) | Run it; read the trace; approve the state | Only I decide which job IDs become "seen" | RUNS.md; `--approve` run |
| Review: defect and test | Explain the defect; write the failing test | Run it and see it fail; commit before any fix | Test-first proves the bug is real | 7b921d3, `evidence/review/1_before_fix.txt` |
| Review: the fix | Claude Code edits `agent/loop.py` only (read/edit, no commands) | Read the diff as behavior, check scope, run all tests | Claude Code said it had not run the tests; checking is my job | `evidence/review/2_claude_code_output.txt`, `3_diff.patch` |
| Review: decision | Nothing | Accept, revise, or reject on evidence | The decision to ship code is mine | REVIEW_PACKET.md §7, commit e5a3fef |
