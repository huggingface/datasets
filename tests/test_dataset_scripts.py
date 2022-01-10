import re
from pathlib import Path
from unittest import TestCase


class TestDatasetScripts(TestCase):
    def _no_encoding_on_file_open(self, filepath: str):
        r"""Find all instances where a non-binary file is opened without UTF-8 encoding.

        This function uses regular expressions to find instances where Python's `open()` function is used to open
        non-binary files. See below for an explanation of the regular expression:

        (?!.*\b(?:encoding|rb|w|wb|w+|wb+|ab|ab+)\b): Lookahead and discard match if `encoding` or `rb` etc are
        arguments of `open()`.

        (?<=\s): Lookbehind and match if `open()` predeceded by one whitespace.

        (open)\((.*)\): Capture everything in parentheses of `open()`.
        """

        with open(filepath, encoding="utf-8") as input_file:
            regexp = re.compile(r"(?!.*\b(?:encoding|rb|w|wb|w+|wb+|ab|ab+)\b)(?<=\s)(open)\((.*)\)")
            input_text = input_file.read()
            match = regexp.search(input_text)

        return match

    def _no_print_statements(self, filepath: str):
        r"""Find all instances where a python sctipt file contains a `print` statement.

        #[^\r\n]*print\(: Match print statement inside a comment. We ignore this group.

        \"[^\r\n]*print\(: Match print statement inside a string. We ignore this group.

        \"\"\".*?print\(.*?\"\"\"": Match print statement inside a triple-quoted string. Uses re.DOTALL to also match newlines with ".".
        We ignore this group.

        (print\()): Match print statement.
        """

        with open(filepath, encoding="utf-8") as input_file:
            regexp = re.compile(r"#[^\r\n]*print\(|\"[^\r\n]*print\(|\"\"\".*?print\(.*?\"\"\"|(print\()", re.DOTALL)
            input_text = input_file.read()
            # use `re.finditer` to handle the case where the ignored groups would be matched first by `re.search`
            matches = regexp.finditer(input_text)

        matches = [match for match in matches if match is not None and match.group(1) is not None]
        return matches[0] if matches else None

    def test_no_encoding_on_file_open(self):
        dataset_paths = Path("./datasets")
        dataset_files = list(dataset_paths.absolute().glob("**/*.py"))

        for dataset in dataset_files:
            if self._no_encoding_on_file_open(str(dataset)):
                raise AssertionError(f"open(...) must use utf-8 encoding in {dataset}")

    def test_no_print_statements(self):
        dataset_paths = Path("./datasets")
        dataset_files = list(dataset_paths.absolute().glob("**/*.py"))

        for dataset in dataset_files:
            if self._no_print_statements(str(dataset)):
                raise AssertionError(f"print statement found in {dataset}. Use datasets.logger/logging instead.")
