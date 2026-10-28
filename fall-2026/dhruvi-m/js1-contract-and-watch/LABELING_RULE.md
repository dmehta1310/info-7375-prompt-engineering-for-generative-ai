# Hand-labeling rule (written 2026-10-28, before labeling)
Question I answer: "Would I honestly tell Priya to apply?" — my judgment, not the agent's rule.

A posting is labeled **apply (relevant)** only if all three are true:
1. It is a data role: the title contains Data Analyst, Data Scientist, Data Science, or Analytics.
2. It is in the US (same as rule 3 in CONTRACT.md).
3. The minimum years of experience it requires is 2 or less. If it lists options (e.g. "MS + 2 or BS + 3"), I use the lowest number. If no years are stated, this passes.

Title level (Lead, Manager, Senior...) does not matter by itself — only the years.
Otherwise: **not relevant**.

Decisions are mine (picked 2026-10-28); Claude wrote the sentences from my picks and I reviewed them.

## Rule v2 (changed 2026-10-28, after labeling 8 of 20 experiment postings)
Change: rule 1 now also passes **any title containing "Analyst"** (e.g. "GTM Strategy & Operations Analyst"). Rules 2 and 3 are unchanged.
Why: while labeling 8201680 I decided an Analyst role in the US with ≤2 years is something I would tell Priya to apply to.
Re-check: I re-applied v2 to the 8 postings already labeled; no label changed (8142302 now passes rule 1 but still fails rule 3 with 5+ years).
Note: this makes my labels broader than the agent's CONTRACT.md title rule, which I did not change.
Outcome: after checking the real text, 8201680 needs 7+ years, so it is "not relevant" anyway. Rule v2 ended up changing no label among the 20.
