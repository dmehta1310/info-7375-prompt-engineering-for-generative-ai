# Runs: the trace, the deliberate failure, and the finished-wrong answer
All runs on 2026-11-09 on my laptop (Python 3.12.7). Times in folder names are UTC.

## 1. LIVE run with the deliberate failure: `out/runs/2026-11-09T203507Z_LIVE/`
Command: `python3 agent/run.py`
| Board | System | Result |
|---|---|---|
| stripe | Greenhouse | ok, 771 jobs (baseline) |
| palantir | Lever | ok, 304 jobs (baseline) |
| linear | Ashby | ok, 32 jobs (baseline) |
| bad-board (`this-board-does-not-exist-js2`) | Greenhouse | **failed: not-found (HTTP 404)** |

- **Exit status: `incomplete`.** Correct per GATE.md: one board failed, so the run is not "finished."
- **4 requests, 2.049 seconds.** The 404 was **not retried** (error policy), and no job count was invented for the failed board.
- Every observation (start, each request, each response, each board result, exit) is in `trace.json`; the raw responses are in `raw/`, including the 404 body.
- Independent check (`python3 agent/check.py <run>`): **PASS**. It recounted 771 / 304 / 32 from the raw files.
- Then **I approved** the new state: `python3 agent/run.py --approve out/runs/2026-11-09T203507Z_LIVE/state_proposal.json`. Before that, `state/seen_ids.json` did not exist.

## 2. Finished-wrong answer (SEEDED + WRONG VERSION): `out/runs/2026-11-09T203530Z_SEEDED-WRONG-VERSION/`
**This is a simulation, labeled as such.** In `out/seed_empty_stripe/`, Stripe's response was replaced with `{"jobs": []}`; Palantir and Linear are copies of the real live responses.
Command: `python3 agent/run.py --seed out/seed_empty_stripe --boards config/boards_demo.json --wrong-empty-rule`
- The **wrong version** (empty-board rule switched off) ended cleanly: **`finished`**, stripe "0 jobs, 0 new." That is wrong: Stripe had 771 jobs on the last approved run.
- **Independent check** (`agent/check.py` does not import the agent's loop or parsers; it recounts from the raw files and compares with the last approved state): **FAIL**, "stripe: 0 jobs now but 771 last time; 'no new jobs' is not believable."

## 3. Same seeded data, correct version: `out/runs/2026-11-09T203531Z_SEEDED/`
Command: `python3 agent/run.py --seed out/seed_empty_stripe --boards config/boards_demo.json`
- Exit status **`incomplete`**, with stripe marked **`suspicious-empty`** (GATE.md's empty-board rule).
