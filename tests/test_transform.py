import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__)))
from src.utils.transform import (
    convert_days_to_digits,
    convert_to_24_hour_time,
    match_ticket_tiers,
    convert_ticket_prices,
    split_genres,
    parse_genres,
    parse_band_name,
    parse_all_bands_and_genres,
)


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
        # Correct format should be left unchanged
        self.assertEqual(convert_to_24_hour_time("07:30"), "07:30")
        self.assertEqual(convert_to_24_hour_time("10:30"), "10:30")
        # Analogue converts to digital
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


class TestSplitGenres(unittest.TestCase):
    def test_non_genres_ignored(self):
        """Test place names aren't included as genres"""
        # Update maps.py list over time to capture quoted locations
        self.assertIsNone(split_genres("Japan, 日本"), None)
        self.assertIsNone(split_genres("Qingdao, China 青島,中國"), None)

    def test_phone_numbers_ignore(self):
        """Test strings containing HK phone numbers are ignored"""
        self.assertIsNone(split_genres("Call +852-4444-4444 for more info"), None)
        self.assertIsNone(split_genres("Call +852 4444 4444 for more info"), None)
        self.assertIsNone(split_genres("Call 4444-4444 for more info"), None)
        self.assertIsNone(split_genres("Call44444444for more info"), None)

    def test_genre_output_types_correct(self):
        """Test valid input processed as correct types"""
        self.assertIsInstance(split_genres("all musicians welcome to jam"), list)
        self.assertIsInstance(split_genres("Funk/Rock"), list)
        self.assertIsInstance(split_genres("hip hop"), list)
        self.assertIsInstance(split_genres("jazz / pop"), list)
        self.assertIsInstance(split_genres("pop & R'n'B"), list)

    def test_genre_output_values_correct(self):
        """Test valid input processed correctly"""
        self.assertEqual(split_genres("all musicians welcome to jam"), ["jam session"])
        self.assertEqual(split_genres("Funk/Rock"), ["funk", "rock"])
        self.assertEqual(split_genres("hip hop"), ["hip-hop"])
        self.assertEqual(split_genres("jazz / pop"), ["jazz", "pop"])
        self.assertEqual(split_genres("pop & R'n'B"), ["pop", "r&b"])


class TestParseGenres(unittest.TestCase):
    def test_non_genres_ignored(self):
        """Test entries specified in NOT_GENRES ignored"""
        self.assertEqual(parse_genres("Loremipsum (Japan 日本) (rock)"), ["rock"])
        self.assertEqual(
            parse_genres(
                "Lorem ipsum (all musicians welcome to jam) (lorem 3332-5333 ipsum)"
            ),
            ["jam session"],
        )

    def test_missing_genre_returns_unknown(self):
        """Test unknown returned if no content found"""
        self.assertEqual(parse_genres(""), ["unknown"])
        self.assertEqual(parse_genres("  "), ["unknown"])
        self.assertEqual(parse_genres("()"), ["unknown"])

    def test_genres_sorted_alphabetically(self):
        """Test results sorted alphabetically"""
        self.assertEqual(
            parse_genres("lorem (C, ba, Bb, a, D)"), ["a", "ba", "bb", "c", "d"]
        )

    def test_genres_not_duplicated(self):
        """Test duplicates are removed"""
        self.assertEqual(parse_genres("(rock, funk, Rock)"), ["funk", "rock"])


class TestParseBandName(unittest.TestCase):
    def test_single_name_captured(self):
        """Test content outside of parenthesis is captured"""
        self.assertEqual(parse_band_name("lorem (ipsum)"), "lorem")
        self.assertEqual(parse_band_name("lorem! (ipsum)"), "lorem!")
        self.assertEqual(
            parse_band_name("lorem 憤駛撓充據 (ipsum)"), "lorem 憤駛撓充據"
        )
        self.assertEqual(parse_band_name("lorem (ipsum) dolor (sit)"), "lorem")
        self.assertEqual(
            parse_band_name("lorem IPSUM dolor (sit)"), "lorem IPSUM dolor"
        )

    def test_absent_names_return_unknown(self):
        """Test 'unknown' is returned if no names found"""
        self.assertEqual(parse_band_name(""), "unknown")
        self.assertEqual(parse_band_name(" "), "unknown")


class TestParseAllBandsAndGenres(unittest.TestCase):
    def test_output_type(self):
        """Test output is list of dicts"""
        self.assertIsInstance(
            parse_all_bands_and_genres("Lorem ipsum (dolor sit)"), list
        )
        self.assertIsInstance(
            parse_all_bands_and_genres(
                "Lorem ipsum (dolor ) sit (amet, consectetur) adipiscing elit"
            ),
            list,
        )
        for e in parse_all_bands_and_genres("Lorem ipsum (dolor sit)"):
            self.assertIsInstance(e, dict)
        for e in parse_all_bands_and_genres(
            "Lorem ipsum (dolor ) sit amet, (consectetur) adipiscing elit"
        ):
            self.assertIsInstance(e, dict)

    def test_output_values(self):
        """Test output is as expected"""
        self.assertEqual(
            parse_all_bands_and_genres("Lorem ipsum (dolor sit)"),
            [{"name": "Lorem ipsum", "genre": ["dolor sit"]}],
        )
        self.assertEqual(
            parse_all_bands_and_genres(
                "Lorem (ipsum), dolor (SIT), AMET (consectetur, adipiscing)"
            ),
            [
                # Case of name remains unchanged
                {"name": "Lorem", "genre": ["ipsum"]},
                # Case of genre made lowercase
                {"name": "dolor", "genre": ["sit"]},
                # Genre names reordered alphabetically
                {"name": "AMET", "genre": ["adipiscing", "consectetur"]},
            ],
        )


if __name__ == "__main__":
    unittest.main()
