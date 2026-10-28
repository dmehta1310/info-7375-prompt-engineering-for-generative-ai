"""Tests for Job-Search Agent 1, written against CONTRACT.md.
Postings built inside these tests are CONSTRUCTED (made up), not real."""
import json, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "agent"))
import watch

PERSONA_PATH = ROOT / "persona" / "priya_nair.json"
PERSONA = json.loads(PERSONA_PATH.read_text())
SNAPSHOT = ROOT / "evidence" / "manual-snapshots" / "stripe_2026-10-27T232715Z.json"
HAND = ROOT / "tests" / "hand_checks.json"


def job(i, title="Data Analyst", loc="New York", content=""):
    return {"id": i, "title": title, "location": {"name": loc}, "content": content}


def run_agent(d, raw_path, state_path):
    args = ["--persona", str(PERSONA_PATH), "--state", str(state_path),
            "--from-file", str(raw_path), "--out", str(Path(d) / "out")]
    assert watch.main(args) == 0
    reports = sorted((Path(d) / "out" / "reports").glob("*.json"))
    return json.loads(reports[-1].read_text())


class TestRule(unittest.TestCase):
    def test_wrong_version_2_whole_words(self):
        r = watch.judge(job(1, content="excellent communication, NoSQL experience"), PERSONA)
        self.assertEqual(r["rule_justification"]["skills"]["count"], 0)
        self.assertEqual(r["rule_verdict"], "not relevant")

    def test_three_skills_pass(self):
        r = watch.judge(job(2, content="&lt;p&gt;SQL, Python and Excel daily&lt;/p&gt;"), PERSONA)
        self.assertEqual(r["rule_justification"]["skills"]["count"], 3)
        self.assertEqual(r["rule_verdict"], "relevant")

    def test_title_analyst_alone_fails(self):
        r = watch.judge(job(3, title="AR Analyst", content="SQL Python Excel"), PERSONA)
        self.assertFalse(r["rule_justification"]["title"]["pass"])

    def test_locations_from_contract(self):
        cases = {"Toronto, Remote-Canada": True, "Canada": False, "Remote": True,
                 "Remote ": True, "N/A": True, "US / Canada": True,
                 "Seattle, WA OR New York, NY OR Remote North America": True,
                 "Chicago, IL": True, "Singapore": False, "Bengaluru": False,
                 "Dublin, Ireland": False, "Mexico City": False}
        for loc, expected in cases.items():
            with self.subTest(loc=loc):
                self.assertEqual(watch.location_check(loc)[0], expected)


class TestRefuses(unittest.TestCase):
    def test_allow_list_blocks_other_hosts(self):
        with self.assertRaises(watch.Refused):
            watch.fetch("https://example.org/jobs")

    def test_rejects_real_looking_email(self):
        with self.assertRaises(watch.Refused):
            watch.validate_persona(dict(PERSONA, email="someone@gmail.com"))

    def test_rejects_persona_not_marked_fictional(self):
        bad = dict(PERSONA)
        bad.pop("fictional")
        with self.assertRaises(watch.Refused):
            watch.validate_persona(bad)


class TestWatch(unittest.TestCase):
    def test_baseline_then_only_new(self):
        with tempfile.TemporaryDirectory() as d:
            state = Path(d) / "state.json"
            a = Path(d) / "a.json"
            b = Path(d) / "b.json"
            a.write_text(json.dumps({"jobs": [job(1), job(2)]}))
            b.write_text(json.dumps({"jobs": [job(1), job(2), job(3)]}))
            r1 = run_agent(d, a, state)
            self.assertEqual(r1["kind"], "BASELINE")
            self.assertEqual(r1["new_postings"], 0)
            r2 = run_agent(d, b, state)
            self.assertEqual([r["posting_id"] for r in r2["results"]], [3])
            r3 = run_agent(d, b, state)
            self.assertEqual(r3["new_postings"], 0)


class TestHandChecks(unittest.TestCase):
    @unittest.skipUnless(HAND.exists(), "tests/hand_checks.json not written yet (Dhruvi fills it by hand)")
    def test_wrong_version_1_pairing(self):
        checks = json.loads(HAND.read_text())
        jobs = json.loads(SNAPSHOT.read_text())["jobs"]
        by_job = {j["id"]: j for j in jobs}
        ids = {c["posting_id"] for c in checks}
        with tempfile.TemporaryDirectory() as d:
            state = Path(d) / "state.json"
            state.write_text(json.dumps({"seen_ids": [j["id"] for j in jobs if j["id"] not in ids], "runs": []}))
            rep = run_agent(d, SNAPSHOT, state)
        by_id = {r["posting_id"]: r for r in rep["results"]}
        for c in checks:
            with self.subTest(posting_id=c["posting_id"]):
                r = by_id[c["posting_id"]]
                self.assertEqual(r["rule_verdict"], c["my_verdict"])
                self.assertEqual(r["rule_justification"]["title"]["posting_value"], by_job[c["posting_id"]]["title"])
                self.assertEqual(r["rule_justification"]["location"]["posting_value"], by_job[c["posting_id"]]["location"]["name"])


if __name__ == "__main__":
    unittest.main()
