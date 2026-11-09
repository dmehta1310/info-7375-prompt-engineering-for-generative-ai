# Job-Search Agent 2: The Loop, the Tools, and the Diff
A bounded agent loop that watches **3 public job boards on 3 different applicant-tracking systems** (Greenhouse, Lever, Ashby) plus **1 board that fails on purpose**, under a permission policy enforced in code, and judges each posting with a deterministic **relevance rule (with a years-of-experience check)**. Persona: **Priya Nair** (fictional; `persona/priya_nair.json`, copied to `config/persona.json`).

**Started from:** my Job-Search Agent 1 (`js1-contract-and-watch/`): its persona, its rule, two of its real postings as test data, and its watcher as a reference (`agent/js1_watch_reference.py`, not used by the JS2 code).

## Language, toolchain, setup
- **Python 3.12.7**, standard library only (`urllib`, `json`, `re`, `html`, `unittest`). **Setup: none**; nothing to install.
- git; Claude Code 2.1.303 (review packet only); macOS Terminal.
- **Tested from a fresh clone** on 2026-11-09: cloned commit 45e8c37 into `/tmp`, ran the tests there: **35 tests OK** (`evidence/fresh_clone_test.txt`).

## Exact commands (from a fresh clone)
- `git clone https://github.com/dmehta1310/info-7375-prompt-engineering-for-generative-ai.git`
- `cd info-7375-prompt-engineering-for-generative-ai/fall-2026/dhruvi-m/js2-loop-tools-diff`
- `python3 -m unittest discover -s tests -v` runs all 35 tests (no network needed)
- `python3 agent/run.py` is a **live** run; it writes `out/runs/<UTC time>_LIVE/` (trace, report, raw responses, relevance) and does **not** change `state/`
- `python3 agent/check.py out/runs/<run folder>` is the **independent check** of a run
- `python3 agent/run.py --approve out/runs/<run folder>/state_proposal.json` accepts a run's job IDs (**my approval**)
- `python3 agent/run.py --seed out/seed_empty_stripe --boards config/boards_demo.json --wrong-empty-rule` is the **SEEDED** finished-wrong demo

## What ran (2026-11-09; details in RUNS.md)
| What | Where | Result |
|---|---|---|
| Live run 1, incl. deliberate 404 | `out/runs/2026-11-09T203507Z_LIVE/` | `incomplete`; stripe 771, palantir 304, linear 32, bad-board failed not-found; 4 requests, 2.0 s |
| Finished-wrong demo (SEEDED, wrong version) | `out/runs/2026-11-09T203530Z_SEEDED-WRONG-VERSION/` | agent said `finished`; independent check **FAIL** (stripe 0 vs 771) |
| Same seeded data, correct version | `out/runs/2026-11-09T203531Z_SEEDED/` | `incomplete`, stripe `suspicious-empty` |
| Live run 2, with the years rule | `out/runs/2026-11-09T220326Z_LIVE/` | `incomplete`; **2 new** Stripe jobs; **0 relevant by rule**; check PASS |
| Tests | `evidence/test_run_1.txt` → `evidence/test_run_rule.txt` | 27 → 28 (review fix) → **35** (rule) all OK |

## Before → after: what improved over JS1
| | JS1 | JS2 |
|---|---|---|
| Boards | 1 board (Stripe, Greenhouse) | 3 boards on 3 systems + 1 deliberate failure |
| Loop control | none | written exits, budgets, repeat rule, error policy (GATE.md, before code) |
| Permissions | allow-listed host only | host, https, GET-only, path, symlink, read/write, and approval checks in code; 16 predicted boundary tests |
| **Years of experience** | **not checked**: rule marked 8026689 (5–10 yrs) relevant | **checked**: same real posting now not relevant (`test_Y1`) |
| "United States" location | missing from US list (7964568) | counts as US (`test_L1`) |
| Wrong answers | not caught | independent check catches a "finished" empty board |
| Claude-written code | not reviewed this way | test-first review packet; model + settings recorded |

## Where things are
GATE.md · BOUNDARY_TESTS.md · RUNS.md · REVIEW_PACKET.md · `agent/` (loop, policy, boards, rule, checker, runner) · `tests/` (+ `tests/fixtures/`: 2 real JS1 postings) · `config/` · `out/runs/` (traces + saved raw responses) · `state/seen_ids.json` · SOURCES.md · FRICTIONAL.md

## Sign-off — Job-Search Agent 2
**Checked** (each with *how*)
- **Permission policy** (hosts, https, GET only, credentials, `..`, prefix trick, symlink, read vs write, approval) → `tests/test_policy.py` B01–B16. *How: with Claude's help.* Claude wrote the tests; **I predicted every result before running** (commit ab832d1) and ran them myself (f05890c).
- **Exits, budgets, repeat rule, error policy** → `tests/test_loop.py` (`test_404_not_retried_and_no_invented_value`, `test_server_error_retried_once_and_counted`, `test_request_budget_exhausted`, `test_time_budget_exhausted`, `test_repeat_blocked`, `test_empty_board_is_suspicious_not_finished`). *How: with Claude's help.* Claude wrote them; I ran them.
- **Deliberate failure handled with no invented value** → live runs 1 and 2. *How: by hand* (I read the report and trace) *and by recomputation* (`agent/check.py` recounts from the raw files and does not import the agent's code).
- **A finished-wrong answer is caught** → seeded demo. *How: by recomputation* (independent check FAIL: 0 vs 771).
- **Claude Code's fix** → `test_R1_request_timeout_never_exceeds_time_left`. *How: by a test written before reading Claude Code's code*: it was written in my tutoring chat and **committed (7b921d3) before Claude Code ran**; it failed before, passed after; I ran all tests myself.
- **The years check fixes my JS1 mistake** → `test_Y1_js1_bug_8026689_now_not_relevant` on the real JS1 posting. *How: by hand*: it matches my own JS1 hand label for 8026689 (not relevant, 5–10 years).
- **Runs from a fresh clone** → 35 tests OK in `/tmp`. *How: by hand.*

**Not checked**
1. **Total download time.** The timeout limits each wait for data, not the total; a slow, trickling server is not tested (REVIEW_PACKET.md §8).
2. **Only one machine, one day.** Both live runs were on my laptop on 2026-11-09; other days, networks, and boards were not tried.
3. **The finished-wrong demo used seeded data.** I never saw a real board return empty; Stripe's empty response was simulated and labeled SEEDED.
4. **No real "relevant" posting yet.** Both live runs found 0 relevant postings, so the "relevant" outcome is only tested on a constructed job (`test_Y2`). The years parser was also not checked on every phrasing (e.g. "two years" written in words).

**Not claiming**
- That the rule's relevant / not-relevant verdicts are **correct** for real postings; they are only consistent with my JS1 labeling rule.
- That it works on boards or applicant-tracking systems **beyond these three**.

**Signed:** Dhruvi Mehta, 2026-11-09

## Driver's seat
| Part | What Claude should do | What I should do | Why it stays mine | Evidence |
|---|---|---|---|---|
| Loop rules (exits, budgets, errors, permissions) | Offer options; turn my picks into sentences | Choose the rules; accept or change the budget | The rules decide what counts as success | GATE.md, commit 8adaf50 (before any code) |
| Loop code and tests | Write the code and tests | Predict boundary results before running; run everything myself | A prediction only counts if it comes before the result | BOUNDARY_TESTS.md, ab832d1 → f05890c |
| Relevance rule (years check) | Write the rule and tests | Decide the rule from my JS1 labels; write the GATE decision first | What "relevant" means for Priya is my judgment | GATE decision 46d8ddf, rule 411323b, `test_Y1` |
| Live runs and approval | Nothing (the code runs) | Run it; read the trace; approve the state | Only I decide which job IDs become "seen" | RUNS.md; `--approve` after run 1 |
| Review: defect and test | Explain the defect; write the failing test | Run it and see it fail; commit before any fix | Test-first proves the bug is real | 7b921d3, `evidence/review/1_before_fix.txt` |
| Review: the fix | Claude Code (claude-sonnet-5-5) edits `agent/loop.py` only | Read the diff as behavior, check scope, run all tests | Claude Code said it had not run the tests | `evidence/review/2_claude_code_output.txt`, `3_diff.patch`, `5_claude_code_model.txt` |
| Review: decision | Nothing | Accept, revise, or reject on evidence | The decision to ship code is mine | REVIEW_PACKET.md §7, e5a3fef |
