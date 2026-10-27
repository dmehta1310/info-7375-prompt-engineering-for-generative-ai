# CONTRACT — Job-Search Agent 1
Written by Dhruvi Mehta, 2026-10-27, before any code.

## In
- The board it watches: Stripe's public job board on Greenhouse (board name "stripe", host boards-api.greenhouse.io).
- The résumé it reads: persona/priya_nair.json, a fictional persona (not a real person).
- What else it needs: a state file that remembers which posting ids it has already seen, and internet access to the one allowed host only.

## Out
For each new posting, the agent returns:
- posting_id and title (so the verdict is tied to the right job)
- rule_verdict: "relevant" or "not relevant", from my written rule (a record anyone can recompute)
- rule_justification: which checks passed or failed, naming the résumé fields (target_titles, skills, locations) and the posting fields (title, content, location) behind each one
- claude_verdict: a separate verdict from Claude, labeled "JUDGMENT (model)", never presented as fact

## Refuses
The agent will not:
- fetch any host except boards-api.greenhouse.io (the allow-list). Any other URL stops the run with an error.
- run with a résumé that is not marked "fictional": true, or that has an email not ending in @example.com, or a phone not starting with 555. This keeps a real résumé off screen and off GitHub.
- present Claude's verdict as a fact. It is always labeled "JUDGMENT (model)", next to the rule's verdict.
- apply to jobs, email or message anyone, or log in anywhere.

## The rule
1. A job title counts if it contains "Data Analyst", "Data Scientist", "Data Science", or "Analytics" anywhere in it. Capitals don't matter. Intern roles count too.
2. A job passes the skills check if at least 3 of Priya's 6 skills (SQL, Python, Tableau, dbt, A/B testing, Excel) appear in the job description as whole words. Capitals don't matter. So "Excel" does not match "excellent" and "SQL" does not match "NoSQL".
3. A location counts as US if it names a US place or tag (US, US-Remote, New York, NYC, NY, SF, San Francisco, Seattle, SEA, WA, Chicago, CHI, IL, Atlanta, Georgia), or if it is exactly "Remote" or "N/A", or if it contains "North America" or "US / Canada". "Remote-Canada" on its own does count.
4. A job is relevant only if the title, skills, and location checks all pass. If any one fails, it is not relevant.

## Wrong versions
Wrong version 1: verdicts paired with the wrong postings.
The code computes the right verdicts but attaches them to the wrong jobs (for example, shifted by one after sorting).
Test that catches it: for 3 postings I hand-checked, the output with that exact posting_id must have the verdict I worked out by hand, and its justification must quote that posting's own title and location.

Wrong version 2: skills matched as parts of words, not whole words.
The code counts "Excel" inside "excellent" and "SQL" inside "NoSQL", so jobs pass the skills check too easily.
Test that catches it: a constructed test posting (labeled as made up) whose description says only "excellent communication, NoSQL experience" must score 0 skills and be "not relevant".

## What a failure looks like
2026-10-27: The agent has failed if the second run reports a posting as new that was already seen in the first run, or gives a rule verdict that I cannot get by hand from the rule above.