import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))
from extract import (
    get_html,
    parse_html,
    preprocess_text,
    decode_quoted_printable_text,
    get_regex_matches,
)
from transform import format_matches


def data_pipeline(target: str, url: bool = True):
    """
    Extracts data from HTML
    Processes data into useable format
    Creates classes for data instances
    """
    if url:
        target = get_html(target)

    text = parse_html(target)
    text = preprocess_text(text)

    if not url:
        text = decode_quoted_printable_text(text)

    matches_in_dict_format = get_regex_matches(text)
    formatted_matches = format_matches(matches_in_dict_format)

    return formatted_matches


if __name__ == "__main__":
    data_pipeline()
