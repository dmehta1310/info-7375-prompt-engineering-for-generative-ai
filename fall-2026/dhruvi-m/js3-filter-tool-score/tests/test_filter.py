"""Filter tests (FILTER.md v1). Each wrong version must give a different answer than the real filter."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "agent"))
from filter import judge, location_is_us, title_matches  # noqa: E402

CFG = json.loads((ROOT / "config" / "filter_v1.json").read_text())
WORDS = CFG["title_words"]


def post(title, location, text="SQL and Python."):
    p = {"board": "t", "id": "1", "title": title, "location": location, "text": text}
    p["missing"] = [f for f in ("title", "location", "text") if not p[f]]
    return p


class TestTitle(unittest.TestCase):
    def test_T1_any_analyst_title_matches(self):
        self.assertEqual(title_matches("Financial Analyst", WORDS), "Analyst")

    def test_T2_lowercase_matches_W3_case_sensitive_does_not(self):
        self.assertEqual(title_matches("data analyst", WORDS), "Analyst")
        self.assertIsNone(title_matches("data analyst", WORDS, wrong_case_sensitive=True))

    def test_T3_inside_another_word_no_match_W4_substring_does(self):
        self.assertIsNone(title_matches("Psychoanalyst", WORDS))
        self.assertIsNotNone(title_matches("Psychoanalyst", WORDS, wrong_substring=True))

    def test_T4_non_data_title_rejected(self):
        self.assertEqual(judge(post("Software Engineer", "Seattle, WA"), CFG)["verdict"], "rejected")


class TestLocation(unittest.TestCase):
    def test_L1_us_forms(self):
        for loc in ("United States", "US", "US-Remote", "Remote - US", "New York, NY", "Seattle, WA",
                    "Toronto, New York, San Francisco, Atlanta, Seattle", "Remote (USA)"):
            self.assertTrue(location_is_us(loc), loc)

    def test_L2_not_us_and_W1_contains_us_is_fooled(self):
        for loc in ("Brussels", "Australia"):
            self.assertFalse(location_is_us(loc), loc)
            self.assertTrue(location_is_us(loc, wrong_contains_us=True), loc)
        self.assertFalse(location_is_us("Toronto, Canada"))

    def test_L3_remote_alone_is_cannot_tell(self):
        self.assertIsNone(location_is_us("Remote"))
        self.assertEqual(judge(post("Data Analyst", "Remote"), CFG)["verdict"], "cannot_tell")


class TestCannotTell(unittest.TestCase):
    def test_C1_missing_location_and_W2_missing_as_us(self):
        p = post("Data Analyst", "")
        self.assertEqual(judge(p, CFG)["verdict"], "cannot_tell")
        self.assertEqual(judge(p, CFG, wrong_missing_is_us=True)["verdict"], "relevant")

    def test_C2_missing_description(self):
        self.assertEqual(judge(post("Data Analyst", "New York, NY", text=""), CFG)["verdict"], "cannot_tell")


class TestBothOutcomes(unittest.TestCase):
    def test_O1_relevant_and_rejected_both_occur(self):
        self.assertEqual(judge(post("Data Analyst", "New York, NY"), CFG)["verdict"], "relevant")
        self.assertEqual(judge(post("Data Analyst", "London"), CFG)["verdict"], "rejected")


class TestLaterVersions(unittest.TestCase):
    def test_V1_years_rule_only_when_configured(self):
        senior = post("Data Analyst", "New York, NY", text="Needs 5+ years of SQL.")
        self.assertEqual(judge(senior, CFG)["verdict"], "relevant")              # v1 ignores years
        self.assertEqual(judge(senior, dict(CFG, max_years=2))["verdict"], "rejected")


if __name__ == "__main__":
    unittest.main()
