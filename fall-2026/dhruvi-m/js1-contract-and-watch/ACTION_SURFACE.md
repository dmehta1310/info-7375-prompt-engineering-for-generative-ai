# Action-surface comparison

The task: decide whether a Stripe posting is relevant to Priya (fictional persona). I did it three ways, all on 2026-10-28.

| | 1. Paste into chat | 2. Give Claude a file | 3. Agent (my code fetches + writes state) |
|---|---|---|---|
| **Evidence** | 40+ runs: `responses/`, `experiment/responses/` | 1 run: `evidence/action_surface/file_upload_8194291.json` + screenshot | 2 live runs: `evidence/raw/`, `evidence/reports/`, `state/seen_ids.json` |
| **Can read** | Only the text I paste | Only the file I attach | The internet, but `watch.py` only allows `boards-api.greenhouse.io` (tested: `test_allow_list_blocks_other_hosts`) |
| **Can write** | Nothing; I save the reply myself | Nothing; I save the reply myself | `evidence/raw/`, `evidence/reports/`, `state/seen_ids.json` |
| **Can send** | Nothing | Nothing | HTTP GET requests to the allow-listed host only |
| **What went wrong / could go wrong** | **Happened:** my clipboard saved my prompt or a command instead of the reply; the validator caught it. No memory of which postings are new. | Same manual saving risk. Claude could misread a long file. No memory of which postings are new. | A bug could overwrite the state file, and then "new" postings would be wrong. Posting text is untrusted and could contain instructions aimed at Claude (prompt injection), which I did not test. |

## The least autonomy that works: option 3, with limits
**My choice:** my own code fetches from **one allow-listed host** and writes the state file. **Claude only judges text it is given**, and its answer must pass the validator.

**Why not less (options 1 and 2):** the task is a **daily watch**. That needs memory of which posting IDs were already seen, and a human copy-pasting 700+ postings every day is not realistic. Copy-paste was also my biggest source of errors (see FRICTIONAL.md).

**Why not more (a full agent that browses and writes by itself):** this task never needs Claude to open arbitrary websites, write files, or send anything. Giving it those powers adds risk (wrong hosts, overwritten files, acting on injected instructions in a posting) and gives no benefit. Keeping fetching and state in plain, tested code means anyone can check what happened.

## Honest limits
- In this assignment, the "Claude judges text it is given" step was still done **by hand in claude.ai**. My code does not call Claude automatically yet, so option 3 was not run end-to-end in one program.
- The file-upload way was run **only once**, on one posting.
- I did not test prompt injection or what happens if the state file is corrupted.

*(I chose option 3 myself. Claude drafted this write-up from what we ran, and I checked the facts.)*
