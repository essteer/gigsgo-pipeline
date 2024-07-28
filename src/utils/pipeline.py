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
    if url:  # Scrape HTML
        target = get_html(target)

    # Parse and preprocess HTML content
    text = parse_html(target)
    text = preprocess_text(text)

    if not url:
        # Decode text in Quoted Printable format
        text = decode_quoted_printable_text(text)

    # Get list of gigs in dict format
    matches = get_regex_matches(text)
    # Format matches
    formatted_matches = format_matches(matches)

    return formatted_matches


if __name__ == "__main__":
    data_pipeline()
