import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__)))
from src.utils.transform import (
    convert_days_to_digits,
    convert_to_24_hour_time,
    match_ticket_tiers,
    convert_ticket_prices,
    split_genres,  # noqa: F401
    parse_genres,  # noqa: F401
    parse_band_name,  # noqa: F401
    parse_all_bands_and_genres,  # noqa: F401
    format_matches,  # noqa: F401
)
from tests.assets.ex01 import HTML_1
from tests.assets.ex02 import HTML_2
from tests.assets.ex03 import HTML_3
from tests.assets.ex04 import HTML_4


TEST_ASSETS = os.path.abspath(os.path.join("tests", "assets"))
TEST_CASES = [HTML_1, HTML_2, HTML_3, HTML_4]


class TestConvertDaysToDigits(unittest.TestCase):
    def test_convert_days_to_digits(self):
        """Test days map to correct digits"""
        days = [
            "Monday",
            "tuesday",
            "WEDNESDAY",
            "thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        for i in range(len(days)):
            self.assertEqual(convert_days_to_digits(days[i]), i + 1)


class TestConvertTo24HourTime(unittest.TestCase):
    def test_conversions_correct(self):
        """Test function output matches expectation"""
        # Correct format left unchanged
        self.assertEqual(convert_to_24_hour_time("10:30"), "10:30")
        # Analogue changed to digital
        self.assertEqual(convert_to_24_hour_time("10pm"), "22:00")
        self.assertEqual(convert_to_24_hour_time("1:30am"), "01:30")
        self.assertEqual(convert_to_24_hour_time("1:30pm"), "13:30")
        self.assertEqual(convert_to_24_hour_time("5:25am"), "05:25")
        self.assertEqual(convert_to_24_hour_time("5:25AM"), "05:25")
        self.assertEqual(convert_to_24_hour_time("5:25pm"), "17:25")
        self.assertEqual(convert_to_24_hour_time("5:25PM"), "17:25")
        # None returns ??:??
        self.assertEqual(convert_to_24_hour_time(None), "??:??")
        # Late returns 00:00
        self.assertEqual(convert_to_24_hour_time("late"), "00:00")

    def test_time_typos_accommodated(self):
        """Test whitespace typos are handled"""
        self.assertEqual(convert_to_24_hour_time("5:25a m"), "05:25")
        self.assertEqual(convert_to_24_hour_time("5:25 a m"), "05:25")
        self.assertEqual(convert_to_24_hour_time("5:25 A M"), "05:25")
        self.assertEqual(convert_to_24_hour_time("5:25 AM"), "05:25")
        self.assertEqual(convert_to_24_hour_time("5:25p m"), "17:25")
        self.assertEqual(convert_to_24_hour_time("5:25 p m"), "17:25")
        self.assertEqual(convert_to_24_hour_time("5:25 P M"), "17:25")
        self.assertEqual(convert_to_24_hour_time("5:25 PM"), "17:25")


class TestMatchTicketTiers(unittest.TestCase):
    def test_tiers_captured(self):
        """Test tier descriptions captured"""
        self.assertEqual(match_ticket_tiers("HK$180 (Advance 預售)"), ("advance", 180))
        self.assertEqual(match_ticket_tiers("HK$100 (Student 學生)"), ("student", 100))
        self.assertEqual(match_ticket_tiers("HK200 (Walk-in 即場)"), ("door", 200))
        # Without parenthesis
        self.assertEqual(match_ticket_tiers("HK$180 Advance 預售"), ("advance", 180))
        self.assertEqual(match_ticket_tiers("$200 Walk-in 即場"), ("door", 200))
        self.assertEqual(match_ticket_tiers("HK$100 Student 學生"), ("student", 100))
        # Added whitespace
        self.assertEqual(match_ticket_tiers("HK$ 100 Student 學生"), ("student", 100))
        self.assertEqual(match_ticket_tiers("$ 100 Student 學生"), ("student", 100))

    def test_tiers_default_to_standard(self):
        """Test prices without descriptions labelled as standard"""
        self.assertEqual(match_ticket_tiers("HK$200"), ("standard", 200))
        self.assertEqual(match_ticket_tiers("$200"), ("standard", 200))
        self.assertEqual(match_ticket_tiers("HK$300"), ("standard", 300))
        self.assertEqual(match_ticket_tiers("HK$250"), ("standard", 250))
        # Added whitespace
        self.assertEqual(match_ticket_tiers("HK 250"), ("standard", 250))
        self.assertEqual(match_ticket_tiers("HK$ 250"), ("standard", 250))


class TestConvertTicketPrices(unittest.TestCase):
    def test_output_type_correct(self):
        self.assertIsInstance(convert_ticket_prices("Free Entry 免費入場"), dict)
        self.assertIsInstance(
            [k for k in convert_ticket_prices("Free Entry 免費入場").keys()][0], str
        )
        self.assertIsInstance(
            [v for v in convert_ticket_prices("Free Entry 免費入場").values()][0], int
        )
        self.assertIsInstance(convert_ticket_prices("HK$100 (Student 學生)"), dict)
        self.assertIsInstance(
            [k for k in convert_ticket_prices("HK$100 (Student 學生)").keys()][0], str
        )
        self.assertIsInstance(
            [v for v in convert_ticket_prices("HK$100 (Student 學生)").values()][0], int
        )
        # Added whitespace
        self.assertIsInstance(
            convert_ticket_prices("HK$180 (Advance 預 售), HK$200 (Walk-in 即場)"), dict
        )
        self.assertIsInstance(
            [
                k
                for k in convert_ticket_prices(
                    "HK$180 (Advance 預 售), HK$200 (Walk-in 即場)"
                ).keys()
            ][0],
            str,
        )
        self.assertIsInstance(
            [
                v
                for v in convert_ticket_prices(
                    "HK$180 (Advance 預 售), HK$200 (Walk-in 即場)"
                ).values()
            ][0],
            int,
        )

    def test_free_entry_handling(self):
        """Test 'Free Entry' returns {'standard': 0}"""
        self.assertEqual(convert_ticket_prices("Free Entry 免費入場"), {"standard": 0})
        self.assertEqual(convert_ticket_prices("Free Entry"), {"standard": 0})
        self.assertEqual(convert_ticket_prices("免費入場"), {"standard": 0})

    def test_conversions_correct(self):
        """Test converted output as expected"""
        self.assertEqual(
            convert_ticket_prices("HK$100 (Student 學生)"), {"student": 100}
        )
        # Added whitespace
        self.assertEqual(
            convert_ticket_prices("HK$180 (Advance 預 售), HK$200 (Walk-in 即場)"),
            {"advance": 180, "door": 200},
        )
        # Without parenthesis
        self.assertEqual(
            convert_ticket_prices("HK$180 Advance 預售, HK$200 (Walk-in 即場)"),
            {"advance": 180, "door": 200},
        )
        # Non-standard descriptions should be returned as-is
        self.assertEqual(convert_ticket_prices("$777 b0om3r8Ng"), {"b0om3r8Ng": 777})
        self.assertEqual(convert_ticket_prices("$777 (b0om3r8Ng)"), {"b0om3r8Ng": 777})


if __name__ == "__main__":
    unittest.main()
