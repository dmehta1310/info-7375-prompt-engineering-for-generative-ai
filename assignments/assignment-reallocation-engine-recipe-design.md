# The Reallocation Engine — Recipe Design Assignment

**Due:** Canvas · **Points:** 100 · **Course:** INFO 7375 · Fall 2026

Assignments follow the ten-day cadence published in Canvas. The syllabus's 10% daily late penalty applies.

Read the [course AI policy](../prerequisites/ai-policy.md) and watch [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz) before beginning graded work.

## Executive summary

- **What:** design a new **recipe** for [The Reallocation Engine](https://github.com/nikbearbrown/the-reallocation-engine/), built for your own career situation, and a **rough working prototype** that runs it end to end on sample data.
- **Why:** an international student's job search is an information-asymmetry problem, not a motivation problem. Your recipe makes one hidden signal visible — sponsorship history, funding, whether a posting is real, role quality, or visa timing — using verified data and code that runs, not an AI's guess. That is what turns an eight-hour scramble of applications into a **3-3-2 day**: three hours networking, three building credibility, two applying.
- **What you hand in:** the recipe and its one-page card, a small prototype with at least one test, a one-page domain justification, a worked run with real pasted output, a run-log entry, one GitHub pull request, and a Canvas ZIP of the same commit.
- **What gets graded hardest:** the line between what your prototype *verified* and what it *inferred*, and how honest you are about what it cannot do.

"Rough" is meant literally. The prototype can be one script, can handle only the happy path plus the failure cases you name, and can run on sample data only. It cannot pretend. A small prototype that does one thing honestly beats a large one that claims more than it checked.

---

## What the Reallocation Engine is

### The problem it solves

An international student on F-1 OPT has a limited window — usually 90 days of allowed unemployment — to find an employer, and for many roles that employer must also be willing to sponsor an H-1B. Most job-search advice treats this as a motivation problem: apply to more jobs, polish the résumé, network harder. The engine starts from a different claim. **The problem is information asymmetry.** From the outside, a student cannot easily see:

- which companies have actually sponsored visas before, for this kind of role;
- which companies just raised money and are likely hiring (SEC Form D filings);
- whether a posting is still live, or a "ghost" left up after the role was filled;
- whether the role is the kind of work AI is about to make cheap;
- whether the hiring timeline fits the time the student has left on their visa.

AI makes this worse before it makes it better. A chatbot will produce a confident, fluent answer to "does this company sponsor?" whether or not any record backs it. For a student with weeks left on the clock, a confident wrong answer costs days of effort.

### What it does

The engine **reallocates effort**. It checks each candidate role against evidence and returns a sourced **Apply / Consider / Skip** decision with every input labeled, then stops and hands the decision to the person.

| Evidence | Question it answers | Role in the decision |
|---|---|---|
| **Funding** (SEC Form D) | Did this company just raise money? | a vote |
| **Sponsorship** (DOL / H-1B history) | Has this company sponsored visas for this kind of role? | a vote |
| **Liveness** (ATS detection) | Is this posting real and still open? | **a gate** |
| **Role quality** (BLS / O\*NET) | Is this well-paid, AI-resilient work? | a vote |
| **Visa timeline** | Can hiring finish before my OPT window closes? | **a gate** |

Votes combine into a score; gates multiply it, so a dead posting or an impossible timeline scores zero regardless of everything else. **Skip is a success** — a healthy run skips at least half of what it evaluates. **Every value is labeled** record, model judgment, or your own input; nothing is presented as a record unless a record produced it. **The human decides** at every gate.

### Why it matters: the 3-3-2 split

Nik Bear Brown's essay *The 3-3-2 Split: Why Your Job Search Is Probably Backwards* argues for splitting an eight-hour search day three ways: **3** hours networking, **3** hours building credibility (a real project that shows judgment), **2** hours researching and tailoring applications. The hard part is the **2** — every application worth tailoring first needs research, and done by hand that research eats the day. **That research is what the engine automates.** A recipe and a working prototype, with tests and an honest account of what they can't verify, is also exactly the kind of judgment-showing project the credibility **3** asks for.

If your recipe cites one of the essay's own figures (ghost-job shares, referral rates, the AI-skills wage premium), trace it to its primary source rather than pasting it in as a record — the engine's own rule applies to its own essay too.

### How it's built

The repository is a book and a working machine at once. **Recipes** in `recipes/` connect the two: an operating procedure an AI agent can execute step by step and a person can read and check, naming the data to check, the scripts to run, the gates where a human signs off, and the output shape. The data is organized in three layers:

| Layer | What it holds | Where it lives |
|---|---|---|
| **80 Days to Stay** | 30,000+ companies mapped to SEC Form D funding signals and H-1B sponsorship history | `data/80-days-to-stay/`, `data/sec/form-d/processed/sample/` |
| **Job-Ops** | ATS detection (Greenhouse, Lever, Ashby, SmartRecruiters), posting liveness, tracker integrity | `scripts/ats/` |
| **The Cognitive Pivot** | BLS OEWS wages and O\*NET ability levels, 1,000+ occupations (SOC codes) | `data/bls/compact/soc_occupation_compact.csv` |

The scorer that combines votes and applies gates is `scripts/score/role-scorer.mjs` (`npm run score`): it takes a JSON list of roles, each with its evidence and a source label, and writes a decision plus a per-term audit trace. That is the easiest place for your prototype to plug in.

The repo is governed by `SNICKERDOODLE.md` (the constitution) and indexed by `DOMAIN.md`. Read both first. The prime directive: **use verified local data and tested scripts first; use an AI only to explain, summarize, draft, or make bounded judgments after the data has been checked.** Your recipe and prototype follow the same rule.

---

## Facts about the engine that will bite you

These are true of the repo today (see `DOMAIN.md` → *Known gaps*). A recipe that ignores them will make claims the engine can't back up.

1. **Role quality carries zero weight in the scorer.** `role-scorer.mjs` sets `role_quality: 0.0`, tagged `[VERIFY]`. If your recipe leans on role-quality or wage data, say how it uses that signal *outside* the scorer, or propose and justify a weight.
2. **`bls:local-wage` feeds nothing yet.** Where it runs it returns a real metro-adjusted wage band, but no decision reads that band.
3. **Only samples of the SEC data ship.** Full Form D quarters are gitignored. A fresh clone has `data/sec/form-d/processed/sample/*.sample.json` only. Say which data you ran on.
4. **Some directories named in recipes don't exist.** `data/raw/`, `data/verified/`, and `logs/gate-decisions/` are planned, not present. Point your gates at paths that exist.
5. **The `snickerdoodle` CLI is roadmap, not runtime.** Commands with that name run nowhere.
6. **Every top-level recipe is still `DRAFT`.** You aren't behind the repo; you're working at its edge.
7. **`npm run bls:local-wage` fails on a fresh clone** — missing `.venv`, and its `requirements.txt` isn't shipped.
8. **`scripts/sec/validate-h1b-join-sample.py` needs full data** it doesn't have; use the shipped CSV and Form D samples instead, or document the gap.

---

## Before you start: get the engine running

1. Fork [`the-reallocation-engine`](https://github.com/nikbearbrown/the-reallocation-engine/), clone your fork, and install: `npm install` (Node 20+, Python 3).
2. Read `SNICKERDOODLE.md`, `DOMAIN.md`, `CONTRIBUTING.md`, `DATA_CONTRACT.md` (§Zero-Conditions), and `recipes/README.md`.
3. Confirm the toolchain: `npm run doctor`, then `npm run verify`.
4. Run the engine once so you know what its output looks like:

   ```bash
   npm run ats:scan -- --dry-run
   npm run ats:liveness -- <job-url>
   npm run score -- data/examples/ch11-roles.json --out-dir course/2026fa/submissions/<handle>/runs
   ```

   **Always pass `--out-dir` to `npm run score`** — without it the scorer overwrites the tracked example output, and that change then shows up in your PR.

5. Save the real terminal output — you'll paste it into your worked run.

> **Personal data stays private, including in git history.** Your real résumé, tracker, and contacts live in `private/`, `search/resume.json`, and `data/ats/`, all gitignored. Use the fictional personas in `search/examples/` or one you invent with `@example.com` addresses. CI scans your entire branch history; deleting a file later doesn't remove it.

Work in your own fork, in the namespaces `CONTRIBUTING.md` assigns you. Your branch name must begin with `contrib/2026fa-`, for example `contrib/2026fa-maya-k-biostat-h1b`. Do not push directly to the instructor's repository.

---

## 1. Predict

Before you build, write `CHANGE-BRIEF.md`:

- The career situation you're designing for (see *What "specific enough" looks like* below) and which engine layer(s) it draws on.
- What existing data or scripts you'll reuse, with exact paths, and what — if anything — you're proposing that the repo doesn't have yet, with a reason it belongs.
- The gate(s) your recipe stops at, and what a human needs to see to clear each one.
- At least two predicted failure cases (a company missing from the CSV, a SOC code with no row, a posting that 404s, an OPT date already past) and how you'll check each.
- One prediction about what your prototype will get wrong or fail to cover on the first pass.

Keep the original predictions. Add later revisions rather than rewriting the record to make every prediction look correct.

## 2. Build It — the recipe

Write the recipe in the style of `recipes/scan.md` and `recipes/local-wage-adjustment.md`, and its card in the style of `recipes/local-wage-adjustment.card.md`. It must include:

- **An executive summary** first: what it does, who it's for, what it decides, in plain language.
- **Lifecycle frontmatter** (below) — claim only the stage you reached.
- **Purpose and source inventory:** exact paths and commands, including your prototype's.
- **Proposed additions**, each justified and marked `[TODO: DEV]` or `[TODO: DATA SOURCE]`.
- **Phase gates:** hard stops with a testable condition against paths that exist. Liveness and visa timeline are gates, not votes.
- **What it can and can't verify** — this boundary is the heart of the grade.
- **Output contract:** a JSON log for the agent, a Markdown report for the person — one file can't serve both.
- **Stop conditions**, and **next action per result** (an application to tailor, a company to network into, or a skip — this is where your recipe connects to the 3-3-2 day).
- A run-log template for `logs/runs/`.

```yaml
---
status: DRAFT          # DRAFT | SPECIFIED | RUNNABLE-SAMPLE | RUNNABLE-LIVE
todos_open: 0
last_gate: null
attestation: null
recipe_version: 0.1.0
---
```

`status` may not exceed `RUNNABLE-SAMPLE` for this assignment; `attestation` stays `null` unless a named human signed it. A recipe honestly marked `RUNNABLE-SAMPLE` with a clear list of what it can't do scores **higher** than one that claims more than its evidence shows.

## 3. Use It — build and run the prototype

A small program in `scripts/contrib/2026fa/<handle>-<slug>/`, Python or JavaScript, that runs at least one full path of your recipe. It must:

- **run with one documented command** from the repo root (put it in a `README.md` in your folder);
- **read real repo data** — not numbers typed into the code;
- **write both outputs** from your output contract into your own folder, never over a tracked repo file;
- **label every value** `record`, `model-judgment`, or `your-input`;
- **fail clearly, without inventing a value**, on your named failure cases;
- **have at least one offline test** running from a fixture, with no network calls;
- **pass** `node scripts/conformance.mjs scripts/contrib/2026fa/<handle>-<slug>/` and `npm run verify`.

**The easiest way to plug in:** have your prototype write a `roles.json` shaped like `data/examples/ch11-roles.json`, each evidence term carrying its `source` label, and run it through the existing scorer with `npm run score -- <your roles.json> --out-dir <your folder>`. Don't re-implement the scorer — a harness that tests its own copy of the scorer tests nothing.

Do not hardcode the verdicts you expect, weaken a rule so a role you like passes, call any network host your recipe doesn't name, or read from `private/`/`search/resume.json` in anything you commit.

Run the finished prototype yourself from a clean checkout of your branch and record it in `TEST-REPORT.md`: toolchain baseline (`npm run doctor`/`npm run verify` before and after), the real sample run and its output, each failure case exercised, `git diff --stat` showing only your namespaced paths, and what the gate requires a human to judge.

## 4. Ship It — domain justification and worked run

### Domain justification (one page or less)

- **Who** uses this recipe, in exactly what situation (see the specificity table below).
- **What information asymmetry** it addresses — what can this person not easily see without it?
- **How it connects** to one or more engine layers.
- **Where it fits the 3-3-2 day** — which part of the two research-and-apply hours it takes over, roughly how much time it saves per week (an estimate, labeled as one), and whether it feeds the networking or credibility hours.
- **Failure modes:** one or two errors specific to your domain — not "the model might hallucinate," but the *shape* of the error and who would find it hardest to catch.

### Worked run

Run your prototype against at least one real or realistic scenario:

- **Inputs** you used, from a persona or anonymized.
- **Commands you ran**, word for word, with their real terminal output pasted in, not described.
- **Verified vs. inferred:** a line-by-line split using the record / model-judgment / your-input labels.
- **Verification:** how you confirmed the output was real — cross-check a value against the source CSV by hand, run your test, or deliberately try to break it.
- **Reflection:** what worked, what the recipe or prototype got wrong or missed, and one concrete next improvement. A session with no correction is a session you did not look at closely enough.

Add `logs/runs/2026fa-<handle>-1.md` recording the run using the template in `recipes/_shared.md`. Never edit `logs/RUN_LOG.md`.

## 5. Verify and submit to Canvas

1. **GitHub.** Open one PR from `contrib/2026fa-<handle>-<slug>` to `nikbearbrown/the-reallocation-engine`, titled with your domain and the lifecycle stage you reached. Before pushing, run these and paste their output into the PR:

   ```bash
   npm run verify
   npm run doctor
   node scripts/pii-scan.mjs
   ```

   plus your prototype's test command. A PR that fails conformance, touches another student's folder or `logs/RUN_LOG.md`, or leaks personal data can't be graded yet.

2. **Canvas.** Upload `reallocation-<handle>-recipe.zip`, a source ZIP of the same commit as the PR (no `node_modules`, caches, credentials, `search/resume.json`, or `private/`), with a short `SUBMISSION.md`:

   ```
   Assignment: The Reallocation Engine — Recipe Design Assignment
   Student:
   GitHub handle:
   Domain / situation:
   Recipe path:
   Prototype command:
   GitHub repository / branch / PR URL:
   Submitted commit SHA:
   Lifecycle stage claimed:
   Summary of my changes:
   Known limitations:
   ```

The ZIP is your submission of record; the PR is the proof it runs in the real repo. They must be the same work.

### Attestation (include in your worked run)

```markdown
## Attestation
- Recipe: <name> v<version>
- By: <name> · <date>

### Tested
| Ran | Saw | Expected |
|---|---|---|
| <command or action> | <observed result> | <expected result> |
| <at least one deliberate attempt to break it> | ... | ... |

### Did not test
- <honest list — an empty one is the new "it works">

### Broke during testing, fixed
- <what failed, what changed, where>
```

---

## Where your work goes (and nowhere else)

Replace `<handle>` with your GitHub handle and `<slug>` with a short name for your situation (for example `biostat-h1b-soc-15-2041`).

| What | Path |
|---|---|
| Recipe + card | `recipes/cases/2026fa/<handle>-<slug>.md` and `<handle>-<slug>.card.md` |
| Prototype code, tests, fixtures | `scripts/contrib/2026fa/<handle>-<slug>/` |
| Run-log entry | `logs/runs/2026fa-<handle>-1.md` |
| Justification, worked run, attestation, reports | `course/2026fa/submissions/<handle>/` |

---

## What "specific enough" looks like

| Too generic | Specific enough |
|---|---|
| Job-seeker in tech | International master's student in data science, OPT expiring in 8 months |
| Researcher | PhD student in biostatistics evaluating industry roles that sponsor H-1B for SOC 15-2041 |
| Business professional | MBA candidate targeting pre-Series B fintech companies with recent Form D filings |
| Engineer | Mechanical engineer on STEM OPT extension scoring role resilience with O\*NET ability levels |

The test: would a student in that exact situation recognize the workflow as built for them, or could it describe any international job-seeker?

---

## Examples of possible recipes

Starting points, not requirements. Design for your own situation.

- `biotech`: roles at Form D-funded biotech firms, checked against life-sciences SOC codes and H-1B history for those codes specifically. *Prototype:* filter the 80 Days CSV to biotech sponsors, join to Form D samples, emit a `roles.json` for the scorer.
- `opt-countdown`: prioritizing applications by hiring timeline against a specific OPT end date. *Prototype:* compute a timeline factor from your OPT date and a stated hiring-lag assumption, labeled `your-input`.
- `cognitive-fit`: filtering roles by O\*NET ability levels to find positions resilient to AI substitution in a target SOC group. *Must address fact 1.*
- `salary-floor`: OEWS wages and H-1B wage fields to set a realistic salary floor before applying. *Must address facts 2 and 7.*
- `network-targets`: turning the engine's rejects into a networking list — strong sponsorship and recent funding but no live posting, worth an informational interview before the role opens. *Prototype:* join the 80 Days CSV to Form D samples, run liveness on each company's board, output a "network, don't apply" list.
- `startup-triage`: Form D recency and amount to separate viable early-stage firms from funding-dry ghost employers. *Must address fact 3.*

---

## Rubric — 100 points

| Component | Points |
|---|---|
| Implementation and explanation | 60 |
| [Frictional](../prerequisites/frictional.md) | 10 |
| [GitHub version posting](../prerequisites/github-submission.md) | 10 |
| [Relative Quartile](../prerequisites/relative-quartile.md) | 20 |
| **Total** | **100** |

### Implementation and explanation — 60 points

| Criterion | Points |
|---|---|
| **Recipe design:** specific to a real domain; data sources, commands, gates, and outputs named precisely, every path/command exists or is a typed `[TODO]`; the verified/inferred boundary is clear; the *Facts that bite* that apply are addressed rather than ignored. | 15 |
| **Working prototype:** runs with one documented command on a fresh clone; reads real repo data; writes both outputs, labels every value; handles its named failure cases without inventing a value; has a passing offline test; uses the existing scorer rather than a copy of it (or explains why not); passes conformance. | 15 |
| **Domain justification:** names a specific information asymmetry; connects to at least one engine layer; says concretely which part of the 3-3-2 research-and-apply time it takes over, with an honestly labeled estimate; names domain-specific failure modes and who would struggle to catch them. | 11 |
| **Worked run:** real prototype output, pasted, not described; explicit verified-vs-inferred split; attestation includes a deliberate break attempt; reflection names what worked, what was missed, and a concrete next step. | 8 |
| **In-class presentation** (five minutes, no slides required): domain and asymmetry are clear, the prototype runs live, one honest limitation is named, on time. | 11 |
| **Subtotal** | **60** |

Award partial credit for demonstrated work within each criterion. A recipe that claims more than its evidence shows scores lower than one that is honestly incomplete.

### [Frictional](../prerequisites/frictional.md) — honest log — 10 points

In `FRICTIONAL.md`, record actual attempts, expectations, difficulties or checks, responses, and learning. Distinguish your work from the AI's.

- 3 points: specific, honest accounts of what you tried and what happened.
- 3 points: what you checked, changed, or learned in response, including unresolved questions.
- 2 points: explicit human/AI contributions — what you accepted, modified, or rejected.
- 2 points: traceability to relevant commits, transcripts, tests, or observations.

An unsuccessful attempt can earn full Frictional credit. More hours or invented struggle do not earn extra credit.

### [GitHub version posting](../prerequisites/github-submission.md) matching Canvas — 10 points

- 4 points: the recipe, prototype, tests, and logs are actually posted in the assigned namespaces, with one open PR and CI green.
- 3 points: Canvas identifies the exact submitted commit and supplies matching source files and clear run instructions.
- 3 points: no personal data anywhere in the branch history; `pii-scan.mjs` output is clean and included.

### [Relative Quartile](../prerequisites/relative-quartile.md) — 20 points

Assigned after the instructor and TAs review the full comparison group. Reflects specificity, honesty about what is and isn't verified, and evidence that you actually built and ran the prototype rather than described doing so.

| Quartile | Points |
|---|---|
| Top 25% | 16–20 |
| Second 25% | 8–15 |
| Third 25% | 4–7 |
| Bottom 25% | 0–3 |

Meeting the stated criteria can earn the other 80 points; it does not guarantee these 20.

---

## The honesty rule

The engine's prime directive: **use collected data and tested scripts first; use prompting only to explain, summarize, draft, or make bounded judgments after the relevant data has been checked.** Your recipe and prototype follow the same rule. If data is missing, say it's missing. If a step isn't built, mark it with a typed `[TODO]`; don't pretend it runs. The best submissions are the ones clearest about what they *can't* do.

## You must be able to explain it

Use `SOURCES.md` to credit the repository, its governing documents, the sample data, collaborators, and tools, and describe what AI contributed versus what you personally decided, checked, changed, or rejected.

The instructor or a TA may ask you to explain any part of your submission — any gate, any number in your worked run, any line of the prototype. Inability to explain it reduces points under the relevant criterion. Misrepresenting authorship, verification, or what an AI agent did is an academic-integrity matter under the course AI policy.
