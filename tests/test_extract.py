import os
import re
import sys
import unittest


sys.path.append(os.path.join(os.path.dirname(__file__)))
from src.utils.extract import (
    get_html,
    parse_html,
    preprocess_text,
    decode_quoted_printable_text,
    get_regex_matches,
)
from src.utils.maps import DAY_MAP
from tests.assets.ex01 import HTML_1
from tests.assets.ex02 import HTML_2
from tests.assets.ex03 import HTML_3
from tests.assets.ex04 import HTML_4

TEST_ASSETS = os.path.abspath(os.path.join("tests", "assets"))
TEST_CASES = [HTML_1, HTML_2, HTML_3, HTML_4]


class TestGetHTML(unittest.TestCase):
    def test_invalid_urls(self):
        """Test with invalid URL input"""
        url = ""
        self.assertEqual(get_html(url), None)
        url = "Test with invalid URL input"
        self.assertEqual(get_html(url), None)

    def test_valid_urls(self):
        """Test with stable URLs"""
        url = "https://www.google.com"
        self.assertIsInstance(get_html(url), str)
        url = "https://www.scrapethissite.com/"
        self.assertIsInstance(get_html(url), str)


class TestParseHTML(unittest.TestCase):
    def test_html_from_emails(self):
        """Test with HTML email examples"""
        for test_case in TEST_CASES:
            self.assertIsInstance(parse_html(test_case), str)

    def test_html_from_url(self):
        """Test with raw HTML from URLs"""
        url = "https://www.google.com"
        html = get_html(url)
        self.assertIsInstance(parse_html(html), str)
        url = "https://www.scrapethissite.com/"
        html = get_html(url)
        self.assertIsInstance(parse_html(html), str)


class TestPreprocessText(unittest.TestCase):
    def test_text_replacements(self):
        """Test undesired characters are replaced"""
        for test_case in TEST_CASES:
            text = parse_html(test_case)
            # Ensure non-standard punctuation handled
            self.assertNotIn("–", preprocess_text(text))
            self.assertNotIn("’", preprocess_text(text))
            self.assertNotIn("&nbsp;", preprocess_text(text))
            # Quoted Printable "...day星..." missing space
            self.assertNotIn("day=E6", preprocess_text(text))

    def test_no_regex_matches(self):
        """Test matches removed"""
        for test_case in TEST_CASES:
            text = parse_html(test_case)
            text = preprocess_text(text)
            # Ensure no equal-sign newline characters present
            matches = re.findall(r"=\s+", text)
            self.assertEqual(matches, [])
            # Ensure no instances of multiple whitespace characters present
            matches = re.findall(r"\s\s+", text)
            self.assertEqual(matches, [])
            # Ensure spaces added before "(" signs
            matches = re.findall(r"\S\(", text)
            self.assertEqual(matches, [])
            # Ensure no HTML tags remain
            matches = re.findall(r"<.*?>", text)
            self.assertEqual(matches, [])


class TestDecodeQuotedPrintableText(unittest.TestCase):
    def test_no_quopri_text_present(self):
        """Test quopri text decoded"""
        for test_case in TEST_CASES:
            text = parse_html(test_case)
            text = preprocess_text(text)
            # Ensure Quoted Printable text converted
            matches = re.findall(r"=[A-Z]{2}", decode_quoted_printable_text(text))
            self.assertEqual(matches, [])
            # Ensure non-standard punctuation handled
            self.assertNotIn("–", preprocess_text(text))
            self.assertNotIn("’", preprocess_text(text))


class TestGetRegexMatches(unittest.TestCase):
    def test_all_matches_found(self):
        """Test expected number of matches found"""
        num_matches = {HTML_1: 93, HTML_2: 113, HTML_3: 89, HTML_4: 115}
        for test_case in TEST_CASES:
            text = parse_html(test_case)
            text = preprocess_text(text)
            text = decode_quoted_printable_text(text)
            self.assertEqual(
                sum(1 for _ in get_regex_matches(text)), num_matches[test_case]
            )

    def test_mandatory_fields_present(self):
        """Test weekday, month, date, open, bands, tickets fields present"""
        for test_case in TEST_CASES:
            text = parse_html(test_case)
            text = preprocess_text(text)
            text = decode_quoted_printable_text(text)
            matches = get_regex_matches(text)
            for match in matches:
                self.assertIn("weekday", match.groupdict())
                self.assertIn("month", match.groupdict())
                self.assertIn("date", match.groupdict())
                self.assertIn("open", match.groupdict())
                self.assertIn("bands", match.groupdict())
                self.assertIn("tickets", match.groupdict())

    def test_match_format_values_correct(self):
        """Test match contents match expected value formats"""
        for test_case in TEST_CASES:
            text = parse_html(test_case)
            text = preprocess_text(text)
            text = decode_quoted_printable_text(text)
            matches = get_regex_matches(text)
            for match in matches:
                # weekday matches
                self.assertIsInstance(match.groupdict()["weekday"], str)
                self.assertIn(match.groupdict()["weekday"].lower(), DAY_MAP)
                # month matches
                self.assertIsInstance(match.groupdict()["month"], str)
                self.assertIn(int(match.groupdict()["month"]), range(1, 13))
                # date matches
                self.assertIsInstance(match.groupdict()["date"], str)
                self.assertIn(int(match.groupdict()["date"]), range(1, 32))
                # desc matches
                if "desc" in match.groupdict():
                    # Ensure regex did not include venue data in description
                    self.assertNotIn("Venue 地點", match.groupdict()["desc"])
                    self.assertNotIn("Venue地點", match.groupdict()["desc"])
                # venue matches
                self.assertIsNotNone(match.groupdict()["venue"])
                # Ensure regex did not include time data in description
                self.assertNotIn("Time 時間", match.groupdict()["venue"])
                self.assertNotIn("Time時間", match.groupdict()["venue"])
                # open time matches
                self.assertIsInstance(match.groupdict()["open"], str)
                m = re.match(
                    r"(\d{1,2}(:\d{2})?\s*([AaPp]{1}\s?[Mm]{1})?)",
                    match.groupdict()["open"],
                )
                self.assertIsNotNone(m)
                # close time matches
                if "close" in match.groupdict():
                    self.assertIsInstance(match.groupdict()["close"], str)
                    m = re.match(
                        r"(\d{1,2}(:\d{2})?\s*([AaPp]{1}\s?[Mm]{1})?|[Ll][Aa][Tt][Ee])",
                        match.groupdict()["close"],
                    )
                    self.assertIsNotNone(m)
                # bands matches
                self.assertIsNotNone(match.groupdict()["bands"])
                # Ensure regex did not include ticket data in bands info
                self.assertNotIn("Ticket 門票", match.groupdict()["bands"])
                self.assertNotIn("Ticket門票", match.groupdict()["bands"])
                # Ensure same for character variant of 門|⾨
                self.assertNotIn("Ticket ⾨票", match.groupdict()["bands"])
                self.assertNotIn("Ticket⾨票", match.groupdict()["bands"])
                # tickets matches
                self.assertIsNotNone(match.groupdict()["tickets"])


if __name__ == "__main__":
    unittest.main()
