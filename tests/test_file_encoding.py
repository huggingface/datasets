import re
from pathlib import Path
from unittest import TestCase


class TestFileEncoding(TestCase):
    def _no_encoding_on_file_open(self, filepath: str):
        r"""Find all instances where a non-binary file is opened without UTF-8 encoding.

        This function uses regular expressions to find instances where Python's `open()` function is used to open
        non-binary files. See below for an explanation of the regular expression:

        (?!.*\b(?:encoding|rb|w|wb|w+|wb+|ab|ab+)\b): Lookahead and discard match if `encoding` or `rb` etc are
        arguments of `open()`.

        (?<=\s): Lookbehind and match if `open()` predeceded by one whitespace.

        (open)\((.*)\): Capture everything in parentheses of `open()`.
        """

        with open(filepath, "r", encoding="utf-8") as input_file:
            regexp = re.compile(r"(?!.*\b(?:encoding|rb|w|wb|w+|wb+|ab|ab+)\b)(?<=\s)(open)\((.*)\)")
            input_text = input_file.read()
            match = regexp.search(input_text)

        return match

    def test_no_encoding_on_file_open(self):
        dataset_paths = Path("./datasets")
        dataset_files = list(dataset_paths.absolute().glob("**/*.py"))

        for dataset in dataset_files:
            if self._no_encoding_on_file_open(str(dataset)):
                raise ValueError(f"open(...) must use utf-8 encoding in {dataset}")
