import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__)))
from src.utils.pipeline import data_pipeline
from tests.assets.ex01 import HTML_1
from tests.assets.ex02 import HTML_2
from tests.assets.ex03 import HTML_3
from tests.assets.ex04 import HTML_4


TEST_ASSETS = os.path.abspath(os.path.join("tests", "assets"))
TEST_CASES = [HTML_1, HTML_2, HTML_3, HTML_4]


class TestDataPipeline(unittest.TestCase):
    def test_all_matches_persist(self):
        """Test all matches retained after formatting"""
        num_matches = {HTML_1: 93, HTML_2: 113, HTML_3: 89, HTML_4: 115}
        for test_case in TEST_CASES:
            self.assertEqual(
                sum(1 for _ in data_pipeline(test_case, False)), num_matches[test_case]
            )

    def test_matches_are_dicts(self):
        """Test all matches in dict format"""
        for test_case in TEST_CASES:
            matches = data_pipeline(test_case, False)
            for match in matches:
                self.assertIsInstance(match, dict)

    def test_expected_fields_present(self):
        """Test expected fields present"""
        for test_case in TEST_CASES:
            matches = data_pipeline(test_case, False)
            for match in matches:
                self.assertIn("weekday", match)
                self.assertIn("month", match)
                self.assertIn("date", match)
                self.assertIn("desc", match)
                self.assertIn("open", match)
                self.assertIn("close", match)
                self.assertIn("bands", match)
                self.assertIn("tickets", match)
                if "venue" in match:
                    self.assertIn("address_en", match)
                    self.assertIn("address_cn", match)
                else:
                    self.assertIn("address_raw", match)

    def test_match_content_types_correct(self):
        """Test values in each match dict are of expected types"""
        for test_case in TEST_CASES:
            matches = data_pipeline(test_case, False)
            for match in matches:
                self.assertIsInstance(match["_id"], str)
                self.assertIsInstance(match["datestring"], str)
                self.assertIsInstance(match["weekday"], str)
                self.assertIsInstance(match["day"], int)
                self.assertIsInstance(match["month"], int)
                self.assertIsInstance(match["date"], int)
                self.assertIsInstance(match["desc"], str)
                self.assertIsInstance(match["open"], str)
                self.assertIsInstance(match["close"], str)
                self.assertIsInstance(match["bands"], list)
                self.assertIsInstance(match["tickets"], dict)
                if "venue" in match:
                    self.assertIsInstance(match["venue"], str)
                    self.assertIsInstance(match["address_en"], str)
                    self.assertIsInstance(match["address_cn"], str)
                else:
                    self.assertIsInstance(match["address_raw"], str)


if __name__ == "__main__":
    unittest.main()
