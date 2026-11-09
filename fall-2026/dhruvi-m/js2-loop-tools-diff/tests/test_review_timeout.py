"""Review packet test, written BEFORE the fix (2026-11-09).

Defect: the per-request timeout is a fixed 15 s, even when less time is left in the
60-second run budget, so one slow request can push the run past max_seconds.
"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "agent"))
from loop import run_loop  # noqa: E402

BUDGET = {"max_boards": 5, "max_requests": 10, "max_seconds": 60}
GH = {"name": "gh", "ats": "greenhouse", "slug": "gh"}
LV = {"name": "lv", "ats": "lever", "slug": "lv"}
GH_JOBS = json.dumps({"jobs": [{"id": 1, "title": "A"}]}).encode()
LV_JOBS = json.dumps([{"id": "a", "text": "B"}]).encode()


class TestTimeoutRespectsBudget(unittest.TestCase):
    def test_R1_request_timeout_never_exceeds_time_left(self):
        now = {"t": 0}
        timeouts = []

        def slow_net(url, timeout):          # each request "takes" 55 seconds
            timeouts.append(timeout)
            now["t"] += 55
            return (200, GH_JOBS) if "/gh" in url else (200, LV_JOBS)

        run_loop([GH, LV], BUDGET, {}, fetch=slow_net, clock=lambda: now["t"])
        # after the first board, only 5 of the 60 seconds are left
        self.assertGreaterEqual(len(timeouts), 2, "second board should still be tried")
        self.assertLessEqual(timeouts[1], 5, f"timeout {timeouts[1]}s is more than the 5s left")


if __name__ == "__main__":
    unittest.main()
