from utils.extract import (
    parse_html,
    preprocess_text,
    decode_quoted_printable_text,
    get_regex_matches,
)
from utils.transform import format_matches


def data_pipeline(raw_html: str):
    """
    Extracts data from HTML
    Processes data into useable format
    Creates classes for data instances
    """
    # Parse and decode HTML content
    text = parse_html(raw_html)
    text = preprocess_text(text)
    text = decode_quoted_printable_text(text)
    # Get list of gigs in dict format
    matches = get_regex_matches(text)
    # Format matches
    formatted_matches = format_matches(matches)

    print(formatted_matches)


if __name__ == "__main__":
    from assets.html_demo_2 import HTML_2

    # data_pipeline(HTML_1)
    data_pipeline(HTML_2)
    # data_pipeline(HTML_3)
    # data_pipeline(HTML_4)
