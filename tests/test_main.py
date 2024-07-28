import unittest
from unittest.mock import patch
import argparse
from src.main import main, JSON_SAVE_DIR

class TestMain(unittest.TestCase):

    @patch("src.main.data_pipeline")
    @patch("argparse.ArgumentParser.parse_args")
    def test_main_verbose(self, mock_parse_args, mock_data_pipeline):
        """Running in verbose mode prints matches to the console"""
        mock_parse_args.return_value = argparse.Namespace(
            target="https://www.example.com",
            verbose=True,
            save=False
        )
        mock_data_pipeline.return_value = ["match1", "match2"]

        with patch("builtins.print") as mock_print:
            main()
            mock_print.assert_any_call("match1", "\n")
            mock_print.assert_any_call("match2", "\n")


    @patch("src.main.data_pipeline")
    @patch("argparse.ArgumentParser.parse_args")
    def test_main_save(self, mock_parse_args, mock_data_pipeline):
        """Running in save mode saves a JSON file"""
        mock_parse_args.return_value = argparse.Namespace(
            target="https://www.example.com",
            verbose=False,
            save=True
        )
        mock_data_pipeline.return_value = ["match1", "match2"]

        with patch("json.dump") as mock_json_dump, patch("os.makedirs") as mock_makedirs:
            main()
            mock_makedirs.assert_called_with(JSON_SAVE_DIR, exist_ok=True)
            mock_json_dump.assert_called_once()
            args, kwargs = mock_json_dump.call_args
            self.assertEqual(args[0], ["match1", "match2"])
            # ensure_ascii=False required to save Chinese characters in human-readable format
            self.assertTrue("ensure_ascii" in kwargs and not kwargs["ensure_ascii"])


    @patch("src.main.data_pipeline")
    @patch("argparse.ArgumentParser.parse_args")
    def test_main_save_and_verbose(self, mock_parse_args, mock_data_pipeline):
        """Running in verbose and save modes prints to the console and saves a JSON file"""
        mock_parse_args.return_value = argparse.Namespace(
            target="https://www.example.com",
            verbose=True,
            save=True
        )
        mock_data_pipeline.return_value = ["match1", "match2"]

        with patch("builtins.print") as mock_print, patch("json.dump") as mock_json_dump, patch("os.makedirs") as mock_makedirs:
            main()
            mock_print.assert_any_call("match1", "\n")
            mock_print.assert_any_call("match2", "\n")
            mock_makedirs.assert_called_with(JSON_SAVE_DIR, exist_ok=True)
            mock_json_dump.assert_called_once()


if __name__ == "__main__":
    unittest.main()
