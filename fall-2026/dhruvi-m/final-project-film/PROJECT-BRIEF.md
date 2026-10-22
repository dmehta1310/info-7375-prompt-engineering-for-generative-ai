# PROJECT-BRIEF — Ghost-Job Trust Radar

Dhruvi Mehta · INFO7375 · Final Project Pitch · Target role: Data Analyst

## 1. What is it?
Ghost-Job Trust Radar will be a command-line tool that checks a job posting before an international student on CPT spends time researching it. It will check three things: whether the posting is still live, whether the hiring timeline fits a CPT work window, and whether the company has a sponsorship record in the dataset. Every answer will be labeled with its source.
When done, it will be a GitHub repository with one command that runs every check, a test suite, a synthetic set of test postings, and an evaluation log.

## 2. Why would anyone care?
It will save an international student on CPT the time they would otherwise spend researching a posting that is already dead or that their work authorization timeline can't meet.
Alternatives (Claude researched these with web search on 2026-10-10. I opened MyVisaJobs myself on 2026-10-22; see FRICTIONAL.md and evidence/2026-10-22-my-checks/):
- **MyVisaJobs (a sponsor database).** You can search employers' past H-1B and green-card filings by company, job title, and location. It answers "has this company sponsored before?" Nothing I saw checks whether a specific posting is still live or whether its start date fits a CPT window. It is also history: sponsoring last year doesn't mean sponsoring this year.
- **The manual checklist that student career guides recommend.** Look the company up in a sponsor database, cross-check Department of Labor filing data, search the posting for words like "sponsor" or "visa," then ask the recruiter. This works, but it's four or five separate steps across tabs, it doesn't check whether the posting is live first, and it leaves no record of what was checked.

What mine will do that they don't: it will check liveness first and stop if the posting is dead, before any research time is spent. It will add a CPT timeline gate. It will label every value with its source, and report missing data as "no record in this dataset" instead of guessing.

## 3. Who opens it, and what do they do?
The reader is a hiring manager for a data analyst role. In the first sixty seconds they will open the README, run one command on a sample posting, and see a report where every value shows its source.
The end user is an international student on CPT who is checking a posting.

## 4. What does it prove about me?
- **Verification:** I checked the script output by hand against the raw CSV, and I ran a deliberate break test with a company that isn't in the data.
- **Source grounding:** my two existing scripts already label each value with its source and report a missing company as "no record"; the full report will do the same for every check.
- **Evaluation:** 16 offline tests pass today. I will add an evaluation log across a synthetic set of postings.
- **Prompt contracts:** the recipe file defines the gates, their order, and when to stop.

A reviewer could fairly conclude that I build data checks that fail safely and say what they don't know. They should *not* conclude that the tool is accurate on real-world postings, because that hasn't been tested yet.

## 5. In, out, first
- **In:** a liveness check, a CPT timeline gate, a sponsorship/funding lookup, and a labeled report.
- **Out:** it will not tell anyone whether to apply, and it will give no immigration or legal advice. It will report evidence, not decisions. It will not scrape LinkedIn or use private data.
- **First:** one script that chains every step on one synthetic posting. You'll know it ran because it writes a report file, a test checks that file, and a dated run log is committed to the repo.

## 6. What could sink it?
The sponsorship data is a historical sample, so it is incomplete. A user could read "no record" as "this company doesn't sponsor." The report will print the dataset's date range next to every lookup, and absence will always read "no record in this dataset." My existing break test already checks the labeling.

## 7. Why this project?
It's a mix. It comes from a real problem for international students like me: research time lost on postings that turn out to be dead, or that have start dates CPT can't meet.
- **Skills I already have:** Python, data cleaning and ETL, and working with CSV data. Evidence: timeline_gate.py and build_roles_json.py, with 16 passing tests, in my Reallocation Engine PR #1 (fall 2026).
- **Skills that are new to me:** writing a recipe as a prompt contract, building an evaluation log, and chaining steps into one agent-style pipeline.

## Exists today
- The recipe and summary card (`dmehta1310-ghost-job-radar`) in my fork of the-reallocation-engine
- timeline_gate.py, with 6 passing offline tests
- build_roles_json.py, with 10 passing offline tests
- One worked run on the course sample data, checked by hand, plus one deliberate break test
- PR #1 against the course repo: open, 14 commits, 16 files, review requested from the instructor, not yet reviewed or merged (checked 2026-10-10). Recipe status is DRAFT and self-attested.

## Will exist
- One command that runs every check in order
- A live liveness check run for real (in the worked run, liveness was supplied manually)
- A real fit signal (SOC-code lookup against public BLS/O*NET data) to replace the flat 0.7 default
- A synthetic set of test postings, an evaluation log, and an honest failure analysis
