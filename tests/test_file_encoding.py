import re
from pathlib import Path, PurePath
from typing import Union
from unittest import TestCase


REGEX = re.compile(r"(?!.*\b(?:encoding|rb|w|wb|w+|wb+|ab|ab+)\b)(?<=\s)(open)\((.*)\)")


def _no_encoding_on_file_open(filepath: Union[str, PurePath]) -> bool:
    r"""Find all instances where a non-binary file is opened without UTF-8 encoding.

    This function uses regular expressions to find instances where Python's `open()` function is used to open
    non-binary files. See below for an explanation of the regular expression:

    (?!.*\b(?:encoding|rb|w|wb|w+|wb+|ab|ab+)\b): Lookahead and discard match if `encoding` or `rb` etc. are
    arguments of `open()`.

    (?<=\s): Lookbehind and match if `open()` preceded by one whitespace.

    (open)\((.*)\): Capture everything in parentheses of `open()`.
    """

    with open(filepath, encoding="utf-8") as input_file:
        return REGEX.search(input_file.read()) is not None


class TestFileEncoding(TestCase):
    def test_no_encoding_on_file_open(self):
        for dataset_path in Path("./datasets").absolute().glob("**/*.py"):
            if _no_encoding_on_file_open(dataset_path):
                raise ValueError(f"open(...) must use utf-8 encoding in {dataset_path}")
