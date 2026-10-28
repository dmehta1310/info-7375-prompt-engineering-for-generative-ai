import json, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "agent"))
from validate import validate

GOOD = {"posting_id": 1, "verdict": "not relevant", "cited_resume_fields": ["skills"],
        "cited_posting_fields": ["description"], "reason": "Only two of the listed skills appear."}


class TestValidator(unittest.TestCase):
    def test_accepts_good(self):
        self.assertTrue(validate(json.dumps(GOOD), 1)[0])

    def test_rejects_code_fences(self):
        self.assertFalse(validate("```json\n" + json.dumps(GOOD) + "\n```", 1)[0])

    def test_rejects_cites_nothing(self):
        self.assertFalse(validate(json.dumps(dict(GOOD, cited_resume_fields=[])), 1)[0])

    def test_rejects_wrong_posting_id(self):
        self.assertFalse(validate(json.dumps(GOOD), 2)[0])

    def test_rejects_other_verdict_words(self):
        self.assertFalse(validate(json.dumps(dict(GOOD, verdict="maybe")), 1)[0])

    def test_rejects_extra_keys(self):
        self.assertFalse(validate(json.dumps(dict(GOOD, confidence=0.9)), 1)[0])


if __name__ == "__main__":
    unittest.main()
