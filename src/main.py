import argparse
import json
import os
import sys
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__)))
from utils.pipeline import data_pipeline

JSON_SAVE_DIR = os.path.join(os.getcwd(), "assets")


def main():
    """
    Runs the data pipeline with a user-provided URL

    Terminal command:
    $ python3 -m src.main [-v] 'https://www.example.com'
    """
    parser = argparse.ArgumentParser(description="Run data pipeline with target URL")
    parser.add_argument(
        "target", type=str, help="target URL -> 'https://www.example.com'"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="print formatted matches"
    )
    parser.add_argument(
        "-s", "--save", action="store_true", help="save results to JSON"
    )

    args = parser.parse_args()

    formatted_matches = data_pipeline(target=args.target)

    if args.verbose:
        for match in formatted_matches:
            print(match, "\n")

    if args.save:
        os.makedirs(JSON_SAVE_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%y%m%d%H%M%S")
        filename = f"{timestamp}_data.json"
        filepath = os.path.join(JSON_SAVE_DIR, filename)
        with open(filepath, "w") as f:
            # set ensure_ascii=False to preserve Chinese characters in human-readable form
            json.dump(formatted_matches, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
