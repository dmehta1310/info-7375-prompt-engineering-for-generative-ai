"""Boundary tests for the permission policy (GATE.md). Predictions: BOUNDARY_TESTS.md."""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "agent"))
from policy import (CONFIG, OUT, ROOT, STATE_FILE, ApprovalRequired,  # noqa: E402
                    PolicyError, check_read, check_request, check_state_write, check_write)


class TestHosts(unittest.TestCase):
    def test_B01_host_off_allow_list_refused(self):
        with self.assertRaises(PolicyError):
            check_request("https://evil.example.com/jobs")

    def test_B02_lookalike_host_refused(self):
        with self.assertRaises(PolicyError):
            check_request("https://boards-api.greenhouse.io.evil.com/v1/boards/stripe/jobs")

    def test_B03_http_not_https_refused(self):
        with self.assertRaises(PolicyError):
            check_request("http://boards-api.greenhouse.io/v1/boards/stripe/jobs")

    def test_B04_post_refused(self):
        with self.assertRaises(PolicyError):
            check_request("https://api.lever.co/v0/postings/palantir", method="POST")

    def test_B05_allowed_get_passes(self):
        check_request("https://api.lever.co/v0/postings/palantir?mode=json")  # no error

    def test_B06_credentials_in_url_refused(self):
        with self.assertRaises(PolicyError):
            check_request("https://user:secret@api.lever.co/v0/postings/palantir")


class TestPaths(unittest.TestCase):
    def test_B07_write_inside_out_allowed(self):
        check_write(OUT / "runs" / "x" / "report.json")  # no error

    def test_B08_dotdot_escape_refused(self):
        with self.assertRaises(PolicyError):
            check_write(OUT / ".." / "state" / "seen_ids.json")

    def test_B09_prefix_trick_refused(self):
        with self.assertRaises(PolicyError):
            check_write(ROOT / "out-evil" / "x.json")

    def test_B10_symlink_escape_refused(self):
        OUT.mkdir(exist_ok=True)
        target = tempfile.mkdtemp()
        link = OUT / "_test_link_outside"
        try:
            if link.is_symlink():
                link.unlink()
            os.symlink(target, link)
            with self.assertRaises(PolicyError):
                check_write(link / "x.json")
        finally:
            if link.is_symlink():
                link.unlink()

    def test_B11_read_config_allowed(self):
        check_read(CONFIG / "boards.json")  # no error

    def test_B12_write_config_refused(self):
        with self.assertRaises(PolicyError):
            check_write(CONFIG / "boards.json")

    def test_B13_read_outside_refused(self):
        with self.assertRaises(PolicyError):
            check_read("/etc/passwd")


class TestApproval(unittest.TestCase):
    def test_B14_state_write_without_approval_refused(self):
        with self.assertRaises(ApprovalRequired):
            check_state_write(STATE_FILE, approved=False)

    def test_B15_state_write_with_approval_allowed(self):
        check_state_write(STATE_FILE, approved=True)  # no error

    def test_B16_approval_does_not_unlock_other_paths(self):
        with self.assertRaises(PolicyError):
            check_state_write(ROOT / "state" / "other.json", approved=True)


if __name__ == "__main__":
    unittest.main()
