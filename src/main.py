import argparse
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))
from utils.pipeline import data_pipeline

# Path to save JSON under
DATA_DIR = os.path.join(os.getcwd(), "data")


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
        with open(os.path.join(DATA_DIR, "data.json"), "w") as f:
            json.dump(formatted_matches, f)


if __name__ == "__main__":
    main()
