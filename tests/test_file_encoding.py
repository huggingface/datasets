import re
from pathlib import Path


def no_encoding_on_file_open(filepath: str):
    """Find all instances where a non-binary file is opened without UTF-8 encoding."""

    with open(filepath, "r", encoding="utf-8") as input_file:
        regexp = re.compile(r"""(?!.*\b(?:encoding|rb|w|wb|w+|wb+|ab|ab+)\b)(?<!\.)(open)\((.*)\)""")
        input_text = input_file.read()
        match = regexp.search(input_text)

    return match


def test_encoding_on_file_open():
    dataset_paths = Path("./datasets")
    dataset_files = list(dataset_paths.absolute().glob("**/*.py"))

    for dataset in dataset_files:
        if no_encoding_on_file_open(str(dataset)):
            raise ValueError(f"UTF-8 encoding missing in dataset {dataset}")
