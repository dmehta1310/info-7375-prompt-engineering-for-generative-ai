# FACTCHECK.md

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | B04 | Nearly 70% of companies on Greenhouse posted at least one ghost job (Q2 2024) | PASS | images/01-entrepreneur.png ("nearly 70% ... second quarter of 2024"; Greenhouse internal review via Entrepreneur) | Caption as planned |
| 2 | B04 | 40% of companies admitted posting a fake job (2024 survey) | PASS | images/02-resumebuilder.png ("40% of companies posted a fake job listing this year") | Check the survey year on the page; the screenshot says "this year" only |
| 3 | B05 | GhostJob gives LinkedIn posts a 0-100 trust score, nothing on visas or CPT | PASS | images/03-ghostjob-extension.png ("see a 0–100 Trust Score"; signals listed are reposting, listing age, pay, location, responsibilities, careers-site match; nothing on visas or CPT). Opened 2026-11-21 | Free accounts get the standard score; Pro adds employer-posting comparison. Still no visa/CPT |
| 4 | B05 | Subspace's scanner checks many signals, nothing on visa sponsorship | PASS | images/04-subspace-scanner.png (seven signals: posting age, salary transparency, repost, description quality, role specificity, hiring patterns, compensation; none about visa sponsorship). Opened 2026-11-21 | Page shows "ghost probability score" as a percentage; the film says only "checks lots of signals" |
| 5 | B05 | Stripe, Llc has 219 filings, Stripe, Inc. has 45 | PASS | images/05-myvisajobs-stripe.png (also Stripe Malpb 3, Stripe Payments Company 2: four names) | |
| 6 | B09 | First run saw 714 postings, second 720, 16 new | PASS | JS1 evidence/reports, both run files | 714 + 16 = 730, not 720, so postings were also removed between runs. Not stated in the film; confirm before filming |
| 7 | B09 | Runs were on October 27 and 28 | PASS | run_at_utc 2026-10-28T02:49Z (evening Oct 27 in Boston) and 2026-10-28T18:28Z | Dates are local time |
| 8 | B10 | 16 passing tests for the CPT check | PASS | pitch film FACTCHECK (6 + 10 offline tests, 2026-10-10) | Re-run before final if I want fresh evidence |
| 9 | B10 | JS2 added a loop with budgets and a permission gate | EXEMPT | My own assignment, per BEAT-PLAN | |
| 10 | B12 | A deleted Stripe posting currently comes back "uncertain" | EXEMPT | My own observation, per BEAT-PLAN | Needs a saved output before it is shown as fact |
| 11 | B13 | Stripe has four company names on MyVisaJobs | PASS | images/05-myvisajobs-stripe.png | |
| 12 | B13 | I hand-labeled 20 postings and held 10 back | EXEMPT | My own work, per BEAT-PLAN | Check against JS1 labels/ |

## Evidence check 2026-11-21 (copied read-only into evidence/)
| # | Beat | Claim | Verdict | Source | Note |
|---|---|---|---|---|---|
| E1 | B10 | 16 passing tests | PASS | evidence/tests/tests-2026-11-21.txt: 6 (timeline gate) + 10 (sponsorship builder), both OK, re-run today | The 6 are the CPT check; the other 10 test the sponsorship-data builder |
| E2 | B12 | A deleted Stripe posting comes back "uncertain" | PARTIAL | evidence/liveness/04b-liveness-dead-madeup-id.txt line 12 (job 1111111111, a made-up ID) and 04d-crosscheck-greenhouse-api.txt (that ID returns HTTP 404) | The saved run is a made-up ID, not a posting that was once live and then deleted. Narration unchanged; wording is your call |
| E3 | B13 | 20 hand-labeled postings, 10 held out | PASS | evidence/js1/experiment/split.json (dev 10, heldout 10), labels.json (20 entries) | All 10 held-out postings are labeled "not relevant" by my labels, and results.txt already shows v1 and v2 at 10/10 |

## Narration revision 2026-11-21 (Dhruvi's edits)
| # | Beat | Claim | Verdict | Source | Note |
|---|---|---|---|---|---|
| R1 | B10 | 6 passing tests (CPT check), 10 more (sponsorship lookup) | PASS | evidence/tests/tests-2026-11-21.txt | replaces "16 passing tests" |
| R2 | B11, B12 | A Stripe job link that returns 404 still comes back uncertain, not dead | PASS | evidence/liveness/04b (line 12) and 04d (HTTP 404) | the link is a made-up ID that the Greenhouse API answers with 404 |
| R3 | B13 | I'll hold out 10 postings with both relevant and not relevant ones | PLANNED | evidence/js1/experiment/split.json, results.txt | A future plan, not a claim about the current set. The saved JS1 held-out set is all "not relevant"; I will build a new mixed held-out set for the final |
