import os
from dotenv import load_dotenv
from utils.extract import (
    get_html,
    parse_html,
    preprocess_text,
    decode_quoted_printable_text,
    get_regex_matches,
)
from utils.transform import format_matches

load_dotenv()


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

    print(len(formatted_matches))


if __name__ == "__main__":
    from assets.html_demo_1 import HTML_1
    from assets.html_demo_2 import HTML_2
    from assets.html_demo_3 import HTML_3
    from assets.html_demo_4 import HTML_4

    data_pipeline(HTML_1, False)  # 93 gigs
    data_pipeline(HTML_2, False)  # 113 gigs
    data_pipeline(HTML_3, False)  # 88 gigs
    data_pipeline(HTML_4, False)  # 115 gigs
    data_pipeline(os.environ["HTML_5"])  # 84 gigs
