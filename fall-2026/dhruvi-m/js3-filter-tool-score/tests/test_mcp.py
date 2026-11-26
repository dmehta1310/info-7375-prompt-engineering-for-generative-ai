"""MCP server tests: the protocol shape and the refusals (no data leaves; nothing outside my folder)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "agent"))
import mcp_server as s  # noqa: E402
from claude_judge import parse  # noqa: E402


class TestProtocol(unittest.TestCase):
    def test_M1_initialize_declares_tools_capability(self):
        r = s.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}})
        self.assertEqual(r["result"]["protocolVersion"], "2025-06-18")
        self.assertIn("tools", r["result"]["capabilities"])

    def test_M2_exactly_one_tool_declared(self):
        r = s.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        self.assertEqual([t["name"] for t in r["result"]["tools"]], ["score_posting"])

    def test_M3_notification_gets_no_reply(self):
        self.assertIsNone(s.handle({"jsonrpc": "2.0", "method": "notifications/initialized"}))

    def test_M4_unknown_method_and_unknown_tool(self):
        self.assertEqual(s.handle({"jsonrpc": "2.0", "id": 3, "method": "resources/list"})["error"]["code"], -32601)
        r = s.handle({"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "delete_posting", "arguments": {}}})
        self.assertIn("error", r)


class TestRefusals(unittest.TestCase):
    def call(self, args):
        return s.handle({"jsonrpc": "2.0", "id": 9, "method": "tools/call",
                         "params": {"name": "score_posting", "arguments": args}})["result"]

    def test_R1_path_escape_refused(self):
        self.assertTrue(self.call({"board": "../../etc", "id": "passwd"})["isError"])
        self.assertTrue(self.call({"board": "stripe", "id": "../../x"})["isError"])

    def test_R2_extra_argument_refused(self):
        self.assertTrue(self.call({"board": "stripe", "id": "1", "write_to": "/tmp/x"})["isError"])


class TestJudgeParse(unittest.TestCase):
    def test_J1_parse_reply(self):
        out = '{"type":"result","result":"{\\"verdict\\": \\"y\\", \\"reason\\": \\"fits\\"}","modelUsage":{"claude-sonnet-5-5":{}}}'
        env, v, reason = parse(out)
        self.assertEqual((v, reason), ("y", "fits"))

    def test_J2_garbage_reply_is_not_a_verdict(self):
        self.assertIsNone(parse("not json")[1])
        self.assertIsNone(parse('{"result": "maybe?"}')[1])


if __name__ == "__main__":
    unittest.main()
