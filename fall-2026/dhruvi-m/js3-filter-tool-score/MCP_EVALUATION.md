# Tool server evaluations (Chapter 8)

Both servers were driven by the same client I wrote (`agent/mcp_client.py`), which saves every message in both directions. Transcripts: `out/mcp/client_own.jsonl`, `out/mcp/client_filesystem.jsonl`, and my server's own log `out/mcp/server_transcript.jsonl`. Evidence commits: `a32a288`, `a7c6f63`.

## 1. My server: `priya-jobs` 1.0.0 (`agent/mcp_server.py`, written from scratch)
JSON-RPC 2.0 over stdio, one message per line: `initialize`, `notifications/initialized`, `ping`, `tools/list`, `tools/call`.

| | What it declares | What it actually did (transcript) |
|---|---|---|
| Tools | 1: `score_posting(board, id)`, read-only | `tools/list` returned exactly 1 tool |
| Normal call | filter v2 verdict + labeled claims | stripe 8189909 → `relevant`, 5 claims, all supported |
| Missing posting | "I cannot tell" | stripe 999999999 → `isError: I cannot tell: no saved posting` |
| Path escape `board: "../../etc"` | board must be one of 3 names | **refused** (`isError`) |
| Extra argument `write_to: "/tmp/x"` | `additionalProperties: false` | **refused** (`isError`) |
| Undeclared tool `delete_posting` | not declared | JSON-RPC error `unknown tool` |
| Real client | n/a | **Claude Code (claude-sonnet-5-5)** connected as client `claude-code`: `initialize` → `tools/list` → `tools/call`, and answered "Verdict: relevant… Claims supported: 5 of 5" (`out/mcp/claude_code_as_client.json`) |

**Read / write / send:** reads only my saved raw board responses and `config/filter_v2.json`; writes only its own log in `out/mcp/`; sends nothing (no network). **It cannot send or change any data outside my folder.**
**What a compatible client is NOT entitled to:** any file outside those two inputs, any posting I did not save, any write, any other tool, and any guarantee that the verdict is *correct* (it is my filter's opinion, consistent with my rules, not truth).
**Trust decision:** I trust it **for read-only scoring of my own saved postings**, because the refusals are tested (`tests/test_mcp.py`) and shown in the transcript. I would **not** trust its verdicts as a decision about whether to apply; that judgment stays mine.

## 2. Someone else's server: `@modelcontextprotocol/server-filesystem` 2.4.0
Source: the official Model Context Protocol reference servers (npm package `@modelcontextprotocol/server-filesystem`, version from `npm view`: `out/mcp/filesystem_server_version.txt`). Run on a throwaway folder: `npx -y @modelcontextprotocol/server-filesystem /tmp/js3_fs_test`.

| | What it declares | What it actually did |
|---|---|---|
| Name | `secure-filesystem-server` 2.4.0 | same |
| Tools | **16**: read_file, read_text_file, read_media_file, read_multiple_files, **write_file, append_file, edit_file, create_directory, move_file, copy_file**, list_directory, list_directory_with_sizes, directory_tree, search_files, get_file_info, list_allowed_directories | all 16 listed |
| Allowed folders | the folder I passed | `/tmp/js3_fs_test` and `/private/tmp/js3_fs_test` (macOS resolves `/tmp`) |
| Read inside | allowed | read `hello.txt` ✓ |
| Read `/etc/hosts` | refused | **Access denied** ✓ |
| `..` escape | refused | **Access denied** ✓ |
| Write | allowed | **wrote `written_by_server.txt`** |

**Read / write / send:** reads, **writes, edits, moves and copies** files inside its allowed folders. Its "secure" name means it keeps to those folders; it does not mean read-only.
**What a client is NOT entitled to:** files outside the allowed folders (it refused them). But a client **is** able to overwrite or move anything inside them, so a careless or manipulated client could damage those files.
**Trust decision:** I would use it **only on a throwaway or copied folder**, never on my repo or my home folder, because one `write_file` / `move_file` call can change data. I did not test symlinks or very large files.
