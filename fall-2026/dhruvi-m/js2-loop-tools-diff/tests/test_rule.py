"""Relevance-rule tests (JS2). Both outcomes are present: relevant and not relevant.

Fixtures:
  tests/fixtures/js1_8026689.json  REAL posting from my JS1 snapshot (2026-10-27): the one my
                                   JS1 rule wrongly marked relevant (it asks for 5-10 years).
  tests/fixtures/js1_7964568.json  REAL posting from my JS1 run 2 (2026-10-28): location
                                   "United States", which my JS1 US list did not include.
  The other jobs below are CONSTRUCTED examples (made up for the test, labeled as such).
"""
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "agent"))
from rule import evaluate, location_is_us, min_years  # noqa: E402

PERSONA = json.loads((HERE.parent / "config" / "persona.json").read_text())


def fixture(name):
    j = json.loads((HERE / "fixtures" / name).read_text())
    return {"title": j["title"], "location": j["location"]["name"], "text": j["content"]}


CONSTRUCTED_GOOD = {  # constructed example
    "title": "Data Analyst", "location": "New York, NY",
    "text": "You will use SQL, Python and Tableau. 1+ years of experience in analytics.",
}
CONSTRUCTED_SENIOR = dict(CONSTRUCTED_GOOD, text=CONSTRUCTED_GOOD["text"].replace("1+ years", "5+ years"))


class TestYearsCheck(unittest.TestCase):
    def test_Y1_js1_bug_8026689_now_not_relevant(self):
        """BEFORE (JS1 rule, no years check) = relevant. AFTER (JS2 rule) = not relevant."""
        job = fixture("js1_8026689.json")
        before = evaluate(job, PERSONA, years_check=False)
        after = evaluate(job, PERSONA)
        self.assertTrue(before["relevant"], f"JS1 version should say relevant: {before}")
        self.assertFalse(after["relevant"], f"JS2 rule should say not relevant: {after}")
        self.assertGreater(after["min_years"], PERSONA["years_experience"])

    def test_Y2_constructed_relevant_job_passes(self):
        r = evaluate(CONSTRUCTED_GOOD, PERSONA)
        self.assertTrue(r["relevant"], r)                      # the "relevant" outcome

    def test_Y3_constructed_senior_job_fails_on_years_only(self):
        r = evaluate(CONSTRUCTED_SENIOR, PERSONA)
        self.assertFalse(r["relevant"])
        self.assertTrue(r["title_ok"] and r["skills_ok"] and r["location_ok"])
        self.assertFalse(r["years_ok"])

    def test_Y4_no_years_stated_does_not_fail(self):
        job = dict(CONSTRUCTED_GOOD, text="SQL, Python, Tableau and dbt every day.")
        self.assertIsNone(min_years(job["text"]))
        self.assertTrue(evaluate(job, PERSONA)["relevant"])

    def test_Y5_lowest_number_counts(self):
        self.assertEqual(min_years("PhD with 3 years, MS with 6 years, or BS with 8 years"), 3)
        self.assertEqual(min_years("5-10 years of audit experience"), 5)


class TestLocation(unittest.TestCase):
    def test_L1_js1_gap_7964568_united_states_is_us(self):
        job = fixture("js1_7964568.json")
        self.assertTrue(location_is_us(job["location"]), job["location"])

    def test_L2_canada_alone_is_not_us(self):
        self.assertFalse(location_is_us("Canada"))
        self.assertFalse(location_is_us("Toronto"))
        self.assertFalse(location_is_us("Singapore"))


if __name__ == "__main__":
    unittest.main()
