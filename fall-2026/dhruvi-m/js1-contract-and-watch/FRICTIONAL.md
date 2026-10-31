# FRICTIONAL — my friction notes

How this file was written: I picked which events were real friction for me from a list Claude made out of my own terminal history. Claude turned my picks into sentences, and I checked them. I only kept events I remember.

## 2026-10-27 — Contract day
- **My decision:** I rejected the first persona titles ("Data Analyst", "Analytics Engineer") and changed them to "Data Analyst", "Data Scientist", "Data Science", "Analytics" so the persona matched the roles I actually wanted to watch.
- **My decision:** I decided that "Remote-Canada" counts as a US-acceptable location in rule 3. That was my call, not Claude's.

## 2026-10-28 — Sampling day
- **Clipboard kept overwriting itself.** Several times my clipboard held my own prompt or a terminal command instead of Claude's reply, so the wrong text got saved. The validator rejected those files and I deleted them. In the end I pasted each reply into my tutoring chat and saved it from there, which worked every time.
- **Labeled too fast on 8026689.** I first marked it "apply" before finding the years. After searching "Minimum requirements" I saw 5–10 years, so by my labeling rule it is "not relevant".
- **Read the wrong job's text for 7440963.** I said "6+ years", but that came from an older job (8189909) still on my terminal screen. After clearing the screen and printing only 7440963's requirements, it said 10 years plus 3 years of management, so it is "not relevant".
- **Rewording changed my facts.** I rewrote my sampling reflection myself in VS Code, and some facts accidentally changed (e.g. it said my rule marked 8026689 "incorrect" instead of wrongly "relevant"). Claude caught it and we fixed it in 91fc49e.

## What I learned from the friction
- I have to read the actual posting myself, on a clean screen, before I label it.
- Copy-paste is the weakest part of my process. Next time I'd save replies automatically.
- When I reword something, I must re-check the facts against my results.

## 2026-10-31: Missed requirement found in my final check
- **What happened:** during a final check against the assignment with Claude, I found that the 16 new postings from my second live run (2026-10-28) only had the rule's verdict. None had a Claude judgment, even though every new posting needs both. I ran all 16 through Claude today (`responses/run2/`). All 16 were VALID and all agreed with the rule: not relevant.
- **Friction:** my clipboard kept getting overwritten. Every time I copied terminal output to check it, the prompt I had just copied was gone, and once I pasted my terminal text into a judge chat by mistake. I threw that chat away and redid it.
- **What I'd do differently:** run the Claude judging right after each live run, not days later.
