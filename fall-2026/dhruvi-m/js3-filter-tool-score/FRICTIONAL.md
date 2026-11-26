# FRICTIONAL: my honest log (JS3)

*How this file was written: the events, and what I accepted, changed or rejected, are mine; Claude (my tutoring chat) wrote the sentences from events I confirmed. Each entry points to a commit, test or file.*

## 2026-11-20: I widened the title rule to any "Analyst"
- **What happened:** my first FILTER.md draft listed only data titles. I changed it to accept **any** title with the word "Analyst", before any code (`24a0b4b`).
- **What it led to:** this produced my false friend, *Mobility Tax Analyst*, and most of my 28 shortlisted jobs are Analyst roles outside data (Compliance, Operations, Security, Finance). I kept the rule after measuring, because cutting it hid 12 jobs I said yes to (dev 22/34 vs 31/34).

## 2026-11-25: Judging one posting at a time was too slow
- **What happened:** the one-by-one judging tool showed long posting text, and I stopped after 1 of 69. Claude built a sheet with one short line per posting (title, location, role line, years, skills) and reason codes, and I answered the other 68 from it. I asked Claude to choose the answers for me; it refused, because the audit has to be my own judgment.
- **Accepted / rejected:** I accepted the sheet and the reason codes; the verdicts are mine (`37efc38`).
- **Unresolved:** for 8026689 I kept reason code 3 ("not in the US") although its location lists US cities (AUDIT.md).

## 2026-11-25: My years rule failed on my own labels
- **What happened:** my JS1 feedback asked for a years-of-experience check, and JS2 had one. In JS3 I measured it on my dev labels: **20/34** vs **31/34** without it. It hid 14 jobs I said yes to, because I said yes to many jobs asking 3–7 years.
- **Decision:** I **rejected** it (FILTER.md, `d66395f`). The check still exists in code and tests; my evidence says Priya would apply above 2 years.

## 2026-11-25: Held-out could not tell v1 from v2
- **What happened:** v2 ("North America" = US) improved dev from 31 to 32 of 34, but on held-out both scored 31/35, because the only posting it fixes is in the dev half. This is the same kind of problem I lost a mark for in JS1, so I report it plainly instead of claiming an improvement.

## 2026-11-25: Wrong dates, and a deleted Claude run
- **What happened:** FILTER.md first said "2026-11-21" for v2; the real commit date was 2026-11-25, so I corrected it from git (`9dbef4b`). Later, my first R1 Claude run finished at **21/35**, then a parallel re-run deleted its files and ran R1 again; only that summary line survives (SCORE_REPORT.md).
- **Unresolved:** I did not plan repeated runs, so I cannot say how much Claude's answers vary.

## 2026-11-25: The other MCP server can write
- **What happened:** the official filesystem server refused reads outside its folder, but `write_file` **succeeded** (`written_by_server.txt`, `a7c6f63`). My own server has one read-only tool and refused all 4 bad calls.
- **Decision:** I'd only run the filesystem server on a throwaway folder (MCP_EVALUATION.md).
