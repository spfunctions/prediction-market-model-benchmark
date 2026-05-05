import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "sf_pm_benchmark"))

from scoring import score_output


class ScoringTests(unittest.TestCase):
    def test_exact_match(self):
        self.assertEqual(score_output({"value": "2"}, {"method": "exact_match"}, "2"), 1.0)

    def test_json_subset(self):
        expected = {"value": {"buy": False, "edge_cents": -8.5}}
        self.assertEqual(score_output(expected, {"method": "json_subset"}, '{"buy":false,"edge_cents":-8.5,"reason":"negative"}'), 1.0)

    def test_label_match(self):
        self.assertEqual(score_output({"value": "REJECT"}, {"method": "label_match"}, "REJECT: max size and liquidity gates violated"), 1.0)

    def test_range(self):
        self.assertEqual(score_output({"min": 45, "max": 65}, {"method": "range"}, "Updated probability: 58%"), 1.0)


if __name__ == "__main__":
    unittest.main()
