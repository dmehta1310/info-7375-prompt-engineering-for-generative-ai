"""A minimal MCP client that speaks to any stdio server and saves the full transcript (both directions).

  python3 agent/mcp_client.py --name own        --calls mcp/own_calls.json        -- python3 agent/mcp_server.py
  python3 agent/mcp_client.py --name filesystem --calls mcp/filesystem_calls.json -- npx -y @modelcontextprotocol/server-filesystem /tmp/js3_fs_test
Writes out/mcp/client_<name>.jsonl and prints a short summary.
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--calls", required=True)
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args()
    cmd = a.cmd[1:] if a.cmd and a.cmd[0] == "--" else a.cmd
    calls = json.loads(Path(a.calls).read_text())
    out = ROOT / "out" / "mcp" / f"client_{a.name}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    f = out.open("w")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def rec(d, m):
        f.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), "dir": d, "msg": m}) + "\n")

    def send(m, expect=True):
        rec("client->server", m)
        proc.stdin.write(json.dumps(m) + "\n")
        proc.stdin.flush()
        if not expect:
            return None
        while True:
            line = proc.stdout.readline()
            if not line:
                return {"error": "server closed"}
            try:
                r = json.loads(line)
            except ValueError:
                continue
            rec("server->client", r)
            if r.get("id") == m.get("id"):
                return r

    n = 0
    r = send({"jsonrpc": "2.0", "id": (n := n + 1), "method": "initialize", "params": {
        "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "dhruvi-js3-client", "version": "1.0"}}})
    print(f"[{a.name}] initialize -> server {r.get('result', {}).get('serverInfo')}")
    send({"jsonrpc": "2.0", "method": "notifications/initialized"}, expect=False)
    r = send({"jsonrpc": "2.0", "id": (n := n + 1), "method": "tools/list"})
    tools = r.get("result", {}).get("tools", [])
    print(f"[{a.name}] tools/list -> {len(tools)} tools declared: {[t['name'] for t in tools]}")
    for c in calls:
        r = send({"jsonrpc": "2.0", "id": (n := n + 1), "method": "tools/call",
                  "params": {"name": c["name"], "arguments": c.get("arguments", {})}})
        res = r.get("result") or {}
        text = " ".join(x.get("text", "") for x in res.get("content", []) if isinstance(x, dict))
        status = "JSON-RPC error: " + r["error"]["message"] if "error" in r else ("isError" if res.get("isError") else "ok")
        print(f"[{a.name}] call {c['name']} {json.dumps(c.get('arguments', {}))[:80]} -> {status}: {text[:140]!r}")
    proc.stdin.close()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
    f.close()
    print(f"[{a.name}] transcript saved: {out}")


if __name__ == "__main__":
    main()
