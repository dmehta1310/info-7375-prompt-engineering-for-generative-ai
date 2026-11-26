"""A tiny Model Context Protocol tool server, written from scratch (Chapter 8).

Transport: JSON-RPC 2.0 over stdio, one JSON message per line.
Methods: initialize, notifications/initialized, ping, tools/list, tools/call.
One tool: score_posting(board, id) -> my filter v2 verdict + labeled claims, for a posting my agent saved.

What it can do: READ my saved raw board responses and my filter config. Nothing else.
It never uses the network, never sends anything, and writes only its own transcript file in out/mcp/.
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "agent"))
from filter import judge  # noqa: E402
from postings import load_raw_dir  # noqa: E402
from shortlist import RAW, claims_for  # noqa: E402

BOARDS = ("stripe", "palantir", "linear")
ID_RE = re.compile(r"^[A-Za-z0-9-]{1,64}$")
LOG = ROOT / "out" / "mcp" / "server_transcript.jsonl"
TOOL = {
    "name": "score_posting",
    "description": ("Score one job posting my agent already saved (read-only). Returns my filter v2 verdict "
                    "(relevant / rejected / cannot_tell) with reasons, and each justification claim labeled "
                    "supported / contradicted / insufficient against the posting's own text."),
    "inputSchema": {"type": "object", "additionalProperties": False, "required": ["board", "id"],
                    "properties": {"board": {"type": "string", "enum": list(BOARDS)},
                                   "id": {"type": "string", "pattern": ID_RE.pattern}}},
}


def log(direction, msg):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                            "dir": direction, "msg": msg}) + "\n")


def score(args):
    board, pid = args.get("board"), args.get("id")
    if board not in BOARDS or not isinstance(pid, str) or not ID_RE.match(pid) or set(args) - {"board", "id"}:
        return {"isError": True, "content": [{"type": "text", "text": "refused: board must be one of "
                f"{list(BOARDS)} and id must match {ID_RE.pattern}; no other arguments"}]}
    cfg = json.loads((ROOT / "config" / "filter_v2.json").read_text())
    posts = {p["id"]: p for p in load_raw_dir(RAW)[0] if p["board"] == board}
    p = posts.get(pid)
    if not p:
        return {"isError": True, "content": [{"type": "text", "text": f"I cannot tell: no saved posting {board}:{pid}"}]}
    v = judge(p, cfg)
    out = {"posting": f"{board}:{pid}", "title": p["title"], "location": p["location"], "filter": cfg["version"],
           "verdict": v["verdict"], "reasons": v["reasons"], "claims": claims_for(p, cfg, v)}
    return {"isError": False, "content": [{"type": "text", "text": json.dumps(out, indent=1)}]}


def handle(msg):
    mid, method = msg.get("id"), msg.get("method")
    if method == "initialize":
        ver = (msg.get("params") or {}).get("protocolVersion", "2025-06-18")
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": ver, "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "priya-jobs", "version": "1.0.0"}}}
    if method and method.startswith("notifications/"):
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": [TOOL]}}
    if method == "tools/call":
        params = msg.get("params") or {}
        if params.get("name") != "score_posting":
            return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32602, "message": f"unknown tool: {params.get('name')}"}}
        return {"jsonrpc": "2.0", "id": mid, "result": score(params.get("arguments") or {})}
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"method not found: {method}"}}


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}}
            log("in", line)
        else:
            log("in", msg)
            resp = handle(msg)
        if resp is not None:
            log("out", resp)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
