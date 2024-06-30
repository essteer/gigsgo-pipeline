import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))
from app import data_pipeline


def main():
    """
    Runs the data pipeline with a user-provided URL
    """
    parser = argparse.ArgumentParser(description="Run data pipeline with target URL")
    parser.add_argument(
        "target", type=str, help="target URL -> 'https://www.example.com'"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="print formatted matches"
    )

    args = parser.parse_args()

    formatted_matches = data_pipeline(target=args.target)

    if args.verbose:
        for match in formatted_matches:
            print(match, "\n")


if __name__ == "__main__":
    main()
