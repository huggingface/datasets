import re
from pathlib import Path


def no_encoding_on_file_open(filepath: str):
    r"""Find all instances where a non-binary file is opened without UTF-8 encoding.

    Regex explanation

    (?!.*\b(?:encoding|rb|w|wb|w+|wb+|ab|ab+)\b): Lookahead and discard match if `encoding` or `rb` etc are args of open(...)

    (?<!\.): Lookbehind and discard match if open(...) preceded by `.`. Used to exclude gzip.open(...)

    (?<!csv.reader\(): Lookahead and discard match if open(...) preceded by `csv.reader(`

    (open)\((.*)\): Capture everything in braces of open(...)
    """

    with open(filepath, "r", encoding="utf-8") as input_file:
        regexp = re.compile(r"(?!.*\b(?:encoding|rb|w|wb|w+|wb+|ab|ab+)\b)(?<!\.)(?<!csv.reader\()(open)\((.*)\)")
        input_text = input_file.read()
        match = regexp.search(input_text)

    return match


def test_encoding_on_file_open():
    dataset_paths = Path("./datasets")
    dataset_files = list(dataset_paths.absolute().glob("**/*.py"))

    for dataset in dataset_files:
        if no_encoding_on_file_open(str(dataset)):
            raise ValueError(f"open(...) must use utf-8 encoding in {dataset}")
