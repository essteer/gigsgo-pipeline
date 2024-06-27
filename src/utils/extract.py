import quopri
import re
from bs4 import BeautifulSoup


def parse_html(html: str) -> str:
    """
    Uses BeautifulSoup to extract text from HTML
    """
    return BeautifulSoup(html, "html.parser").get_text()


def preprocess_text(raw_text: str) -> str:
    """
    Applies regex to preprocess text before decoding

    Parameters
    ----------
    raw_text : str
        text extracted from HTML via BeautifulSoup

    Returns
    -------
    text : str
        raw_text cleaned via regex
    """
    text = raw_text.strip()
    # Replace "&nbsp;" with single "\s" char
    text = re.sub(r"&nbsp;", " ", text)
    # Remove newlines created via "=" chars
    text = re.sub(r"=\s+", "", text)
    # Insert single space before "(" char if absent
    text = re.sub(r"(\S)(\()", r"\1 (", text)
    # Replace multiple "\s" chars with single "\s" char
    text = re.sub(r"\s+", " ", text)
    # Insert missing space between English and Chinese day of week
    text = re.sub(r"day=E6", "day =E6", text)
    # Remove overlooked HTML tags, non-greedy
    text = re.sub(r"<.*?>", "", text)

    return text


def decode_quoted_printable_text(encoded_text: str) -> str:
    """
    Decodes Quoted Printable characters into human-readable format

    Parameters
    ----------
    encoded_text : str
        text in combination of ASCII and Quoted Printable encoding

    Returns
    -------
    decoded_text : str
        text with Chinese characters converted to readable format
    """
    # Convert Quoted Printable text to Chinese characters
    decoded_text = quopri.decodestring(encoded_text).decode("utf-8")
    # Replace non-standard punctuation with ASCII versions
    decoded_text = decoded_text.replace("–", "-")
    decoded_text = decoded_text.replace("’", "'")

    return decoded_text


def get_regex_matches(text: str) -> list[re.Match]:
    """
    Creates and returns dict of matches

    Parameters
    ----------
    text : str
        decoded and processed HTML content to extract matches from

    Returns
    -------
    matches : list[re.Match]
        list of Match objects found in text
    """
    pattern = re.compile(
        r"""
        (?P<weekday>[FMSTW][a-z]{2,5}day)   # English day of week
        \s?
        星期[⼀一二三四五六日]                 # Chinese day of week (including char variants)
        \s?[\w\s]+                          # Longform date
        (?P<month>(\d){1,2})月              # Month
        (?P<date>(\d){1,2})日               # Date

        \s?
        (?P<desc>.*?[^V])                   # Event description
        Venue\s地點:\s?                      # "Venue 地點:"
        (?P<venue>.*?)                      # Venue name, non-greedy
        
        \sTime\s時間:\s?                     # "Time 時間:"
        (?P<open>                           # Start time
        \d{1,2}                             # Hour
        (:\d{2})?                           # Minutes (optional)
        ([APMapm]{2})?)                     # am/pm (optional)
        \s?-\s?                             # hyphen with or without spaces
        (?P<close>                          # End time
        (\d{1,2}(:\d{2})?([APMapm]{2})?     # Logic as per start time
        |[Ll][Aa][Tt][Ee]))                   # End time may be "late"
        
        \sBands\s樂隊:\s?                     # "Bands 樂隊:"
        (?P<bands>.*?)                       # Bands info, non-greedy
        \s?Ticket\s(門|⾨)票:\s?              # "Ticket 門票:" or "Ticket ⾨票:" (character variants)
        (?P<tickets>.*?                       # Ticket info, non-greedy
        (?=([FMSTW][a-z]{2,5}day|Enjoy|$)))  # Lookahead to day, "Enjoy" or end of string
        """,
        re.VERBOSE | re.DOTALL,
    )
    # Find all matches
    matches = pattern.finditer(text)

    return matches
