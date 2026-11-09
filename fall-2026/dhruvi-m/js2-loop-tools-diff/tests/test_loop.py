"""Loop tests with a fake network and a fake clock (no real requests)."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "agent"))
from loop import run_loop  # noqa: E402

BUDGET = {"max_boards": 5, "max_requests": 10, "max_seconds": 60}
GH = {"name": "gh", "ats": "greenhouse", "slug": "gh"}
LV = {"name": "lv", "ats": "lever", "slug": "lv"}
AB = {"name": "ab", "ats": "ashby", "slug": "ab"}
GH_JOBS = json.dumps({"jobs": [{"id": 1, "title": "Data Analyst"}, {"id": 2, "title": "X"}]}).encode()
LV_JOBS = json.dumps([{"id": "a", "text": "Analyst"}]).encode()
AB_JOBS = json.dumps({"jobs": [{"id": "z", "title": "Analytics"}]}).encode()


class FakeNet:
    def __init__(self, plan):
        self.plan = {k: list(v) for k, v in plan.items()}   # url-substring -> list of responses
        self.calls = []

    def __call__(self, url, timeout):
        self.calls.append(url)
        for key, seq in self.plan.items():
            if f"/{key}" in url:
                r = seq.pop(0) if len(seq) > 1 else seq[0]
                if r == "timeout":
                    raise TimeoutError("fake timeout")
                return r
        raise AssertionError(f"unexpected url {url}")


def ok_net():
    return FakeNet({"gh": [(200, GH_JOBS)], "lv": [(200, LV_JOBS)], "ab": [(200, AB_JOBS)]})


class TestLoop(unittest.TestCase):
    def test_all_ok_is_finished(self):
        r = run_loop([GH, LV, AB], BUDGET, {}, fetch=ok_net())
        self.assertEqual(r["status"], "finished")
        self.assertEqual(r["boards"]["gh"]["count"], 2)

    def test_404_not_retried_and_no_invented_value(self):
        net = FakeNet({"gh": [(404, b"{}")], "lv": [(200, LV_JOBS)]})
        r = run_loop([GH, LV], BUDGET, {}, fetch=net)
        self.assertEqual(r["status"], "incomplete")
        self.assertEqual(r["boards"]["gh"]["status"], "failed")
        self.assertEqual(r["boards"]["gh"]["reason"], "not-found")
        self.assertNotIn("count", r["boards"]["gh"])          # no invented "0 jobs"
        self.assertEqual(sum("/gh" in c for c in net.calls), 1)  # wrong version 6: retrying a 404

    def test_server_error_retried_once_and_counted(self):
        net = FakeNet({"gh": [(503, b""), (503, b"")]})
        r = run_loop([GH], BUDGET, {}, fetch=net)
        self.assertEqual(r["boards"]["gh"]["status"], "failed")
        self.assertEqual(len(net.calls), 2)
        self.assertEqual(r["requests_used"], 2)               # retries count against the budget

    def test_timeout_then_success(self):
        net = FakeNet({"gh": ["timeout", (200, GH_JOBS)]})
        r = run_loop([GH], BUDGET, {}, fetch=net)
        self.assertEqual(r["boards"]["gh"]["status"], "ok")

    def test_empty_board_is_suspicious_not_finished(self):
        net = FakeNet({"gh": [(200, b'{"jobs": []}')]})
        r = run_loop([GH], BUDGET, {"gh": ["1", "2"]}, fetch=net)
        self.assertEqual(r["status"], "incomplete")           # wrong version 1
        self.assertEqual(r["boards"]["gh"]["status"], "suspicious-empty")

    def test_wrong_version_reports_empty_board_as_finished(self):
        """Documents the WRONG version used in the demo: it ends 'finished'."""
        net = FakeNet({"gh": [(200, b'{"jobs": []}')]})
        r = run_loop([GH], BUDGET, {"gh": ["1", "2"]}, fetch=net, empty_rule=False)
        self.assertEqual(r["status"], "finished")

    def test_failed_board_never_counts_as_finished(self):
        net = FakeNet({"gh": [(200, b"not json")], "lv": [(200, LV_JOBS)]})
        r = run_loop([GH, LV], BUDGET, {}, fetch=net)
        self.assertNotEqual(r["status"], "finished")          # wrong version 2
        self.assertEqual(r["boards"]["gh"]["reason"], "bad-response")

    def test_request_budget_exhausted(self):
        net = FakeNet({"gh": [(503, b""), (503, b"")], "lv": [(200, LV_JOBS)], "ab": [(200, AB_JOBS)]})
        r = run_loop([GH, LV, AB], dict(BUDGET, max_requests=2), {}, fetch=net)
        self.assertEqual(r["status"], "budget-exhausted")
        self.assertEqual(r["never_attempted"], ["lv", "ab"])

    def test_time_budget_exhausted(self):
        now = {"t": 0}
        inner = ok_net()

        def slow_net(url, timeout):        # the first request "takes" 100 seconds
            now["t"] += 100
            return inner(url, timeout)
        r = run_loop([GH, LV], BUDGET, {}, fetch=slow_net, clock=lambda: now["t"])
        self.assertEqual(r["status"], "budget-exhausted")
        self.assertIn("lv", r["never_attempted"])

    def test_repeat_blocked(self):
        net = ok_net()
        r = run_loop([GH, dict(GH, name="gh-again")], BUDGET, {}, fetch=net)
        self.assertEqual(r["boards"]["gh-again"]["status"], "repeat-blocked")
        self.assertEqual(len(net.calls), 1)
        self.assertNotEqual(r["status"], "finished")

    def test_new_ids_against_state(self):
        r = run_loop([GH], BUDGET, {"gh": ["1"]}, fetch=ok_net())
        self.assertEqual(r["boards"]["gh"]["new_ids"], ["2"])


if __name__ == "__main__":
    unittest.main()
