import re
import tempfile
from pathlib import Path

import pytest
import yaml

from datasets.utils.readme import ReadMe


# @pytest.fixture
# def example_yaml_structure():

example_yaml_structure = yaml.safe_load(
    """\
name: ""
allow_empty: false
allow_empty_text: true
subsections:
  - name: "Dataset Card for X" # First-level markdown heading
    allow_empty: false
    allow_empty_text: true
    subsections:
      - name: "Table of Contents"
        allow_empty: false
        allow_empty_text: false
        subsections: null
      - name: "Dataset Description"
        allow_empty: false
        allow_empty_text: false
        subsections:
          - name: "Dataset Summary"
            allow_empty: false
            allow_empty_text: false
            subsections: null
          - name: "Supported Tasks and Leaderboards"
            allow_empty: true
            allow_empty_text: true
            subsections: null
          - name: Languages
            allow_empty: false
            allow_empty_text: true
            subsections: null
"""
)


CORRECT_DICT = {
    "name": "root",
    "text": "",
    "is_empty_text": True,
    "subsections": [
        {
            "name": "Dataset Card for My Dataset",
            "text": "",
            "is_empty_text": True,
            "subsections": [
                {"name": "Table of Contents", "text": "Some text here.", "is_empty_text": False, "subsections": []},
                {
                    "name": "Dataset Description",
                    "text": "Some text here.",
                    "is_empty_text": False,
                    "subsections": [
                        {
                            "name": "Dataset Summary",
                            "text": "Some text here.",
                            "is_empty_text": False,
                            "subsections": [],
                        },
                        {
                            "name": "Supported Tasks and Leaderboards",
                            "text": "",
                            "is_empty_text": True,
                            "subsections": [],
                        },
                        {"name": "Languages", "text": "Language Text", "is_empty_text": False, "subsections": []},
                    ],
                },
            ],
        }
    ],
}


README_CORRECT = """\
---
language:
- zh
- en
---

# Dataset Card for My Dataset
## Table of Contents
Some text here.
## Dataset Description
Some text here.
### Dataset Summary
Some text here.
### Supported Tasks and Leaderboards
### Languages
Language Text
"""


README_CORRECT_FOUR_LEVEL = """\
---
language:
- zh
- en
---

# Dataset Card for My Dataset
## Table of Contents
Some text here.
## Dataset Description
Some text here.
### Dataset Summary
Some text here.
#### Extra Ignored Subsection
### Supported Tasks and Leaderboards
### Languages
Language Text
"""

CORRECT_DICT_FOUR_LEVEL = {
    "name": "root",
    "text": "",
    "is_empty_text": True,
    "subsections": [
        {
            "name": "Dataset Card for My Dataset",
            "text": "",
            "is_empty_text": True,
            "subsections": [
                {"name": "Table of Contents", "text": "Some text here.", "is_empty_text": False, "subsections": []},
                {
                    "name": "Dataset Description",
                    "text": "Some text here.",
                    "is_empty_text": False,
                    "subsections": [
                        {
                            "name": "Dataset Summary",
                            "text": "Some text here.",
                            "is_empty_text": False,
                            "subsections": [
                                {
                                    "name": "Extra Ignored Subsection",
                                    "text": "",
                                    "is_empty_text": True,
                                    "subsections": [],
                                }
                            ],
                        },
                        {
                            "name": "Supported Tasks and Leaderboards",
                            "text": "",
                            "is_empty_text": True,
                            "subsections": [],
                        },
                        {"name": "Languages", "text": "Language Text", "is_empty_text": False, "subsections": []},
                    ],
                },
            ],
        }
    ],
}

README_EMPTY_YAML = """\
---
---
# Dataset Card for My Dataset
## Table of Contents
Some text here.
## Dataset Description
Some text here.
### Dataset Summary
Some text here.
### Supported Tasks and Leaderboards
### Languages
Language Text
"""

EXPECTED_ERROR_README_EMPTY_YAML = (
    "The following issues were found for the README at `{path}`:\n-\tEmpty YAML markers are present in the README."
)

README_NO_YAML = """\
# Dataset Card for My Dataset
## Table of Contents
Some text here.
## Dataset Description
Some text here.
### Dataset Summary
Some text here.
### Supported Tasks and Leaderboards
### Languages
Language Text
"""

EXPECTED_ERROR_README_NO_YAML = (
    "The following issues were found for the README at `{path}`:\n-\tNo YAML markers are present in the README."
)

README_INCORRECT_YAML = """\
---
# Dataset Card for My Dataset
## Table of Contents
Some text here.
## Dataset Description
Some text here.
### Dataset Summary
Some text here.
### Supported Tasks and Leaderboards
### Languages
Language Text
"""

EXPECTED_ERROR_README_INCORRECT_YAML = "The following issues were found for the README at `{path}`:\n-\tOnly the start of YAML tags present in the README."

README_MISSING_TEXT = """\
---
language:
- zh
- en
---

# Dataset Card for My Dataset
## Table of Contents
Some text here.
## Dataset Description
Some text here.
### Dataset Summary
### Supported Tasks and Leaderboards
### Languages
Language Text
"""
EXPECTED_ERROR_README_MISSING_TEXT = "The following issues were found for the README at `{path}`:\n-\tExpected some content in section `Dataset Summary` but it is empty.\n-\tExpected some text in section `Dataset Summary` but it is empty (text in subsections are ignored)."


README_NONE_SUBSECTION = """\
---
language:
- zh
- en
---

# Dataset Card for My Dataset
"""
EXPECTED_ERROR_README_NONE_SUBSECTION = "The following issues were found for the README at `{path}`:\n-\tExpected some content in section `Dataset Card for My Dataset` but it is empty.\n-\tSection `Dataset Card for My Dataset` expected the following subsections: `Table of Contents`, `Dataset Description`. Found 'None'."

README_MISSING_SUBSECTION = """\
---
language:
- zh
- en
---

# Dataset Card for My Dataset
## Table of Contents
Some text here.
## Dataset Description
Some text here.
### Dataset Summary
Some text here.
### Languages
Language Text
"""

EXPECTED_ERROR_README_MISSING_SUBSECTION = "The following issues were found for the README at `{path}`:\n-\tSection `Dataset Description` is missing subsection: `Supported Tasks and Leaderboards`."


README_MISSING_CONTENT = """\
---
language:
- zh
- en
---

# Dataset Card for My Dataset
## Table of Contents
Some text here.
## Dataset Description
Some text here.
### Dataset Summary
Some text here.
### Supported Tasks and Leaderboards
### Languages
"""

EXPECTED_ERROR_README_MISSING_CONTENT = "The following issues were found for the README at `{path}`:\n-\tExpected some content in section `Languages` but it is empty."

README_MISSING_FIRST_LEVEL = """\
---
language:
- zh
- en
---

## Table of Contents
Some text here.
## Dataset Description
Some text here.
### Dataset Summary
Some text here.
### Supported Tasks and Leaderboards
### Languages
Language Text
"""
EXPECTED_ERROR_README_MISSING_FIRST_LEVEL = "The following issues were found for the README at `{path}`:\n-\tThe README has no first-level headings. One heading is expected. Skipping further validation for this README."

README_MULTIPLE_WRONG_FIRST_LEVEL = """\
---
language:
- zh
- en
---

# Dataset Card for My Dataset
## Table of Contents
Some text here.
## Dataset Description
Some text here.
### Dataset Summary
Some text here.
### Supported Tasks and Leaderboards
### Languages
Language Text
# Dataset Card My Dataset
"""

EXPECTED_ERROR_README_MULTIPLE_WRONG_FIRST_LEVEL = "The following issues were found for the README at `{path}`:\n-\tThe README has several first-level headings: `Dataset Card for My Dataset`, `Dataset Card My Dataset`. Only one heading is expected. Skipping further validation for this README."

README_WRONG_FIRST_LEVEL = """\
---
language:
- zh
- en
---

# Dataset Card My Dataset
## Table of Contents
Some text here.
## Dataset Description
Some text here.
### Dataset Summary
Some text here.
### Supported Tasks and Leaderboards
### Languages
Language Text
"""

EXPECTED_ERROR_README_WRONG_FIRST_LEVEL = "The following issues were found for the README at `{path}`:\n-\tNo first-level heading starting with `Dataset Card for` found in README. Skipping further validation for this README."

README_EMPTY = ""

EXPECTED_ERROR_README_EMPTY = "The following issues were found for the README at `{path}`:\n-\tThe README has no first-level headings. One heading is expected. Skipping further validation for this README.\n-\tNo YAML markers are present in the README."

README_MULTIPLE_SAME_HEADING_1 = """\
---
language:
- zh
- en
---

# Dataset Card for My Dataset
# Dataset Card for My Dataset
## Table of Contents
Some text here.
## Dataset Description
Some text here.
### Dataset Summary
Some text here.
### Supported Tasks and Leaderboards
### Languages
Language Text
"""

EXPECTED_ERROR_README_MULTIPLE_SAME_HEADING_1 = "The following issues were found while parsing the README at `{path}`:\n-\tMultiple sections with the same heading `Dataset Card for My Dataset` have been found. Please keep only one of these sections."


@pytest.mark.parametrize(
    "readme_md, expected_dict",
    [
        (README_CORRECT, CORRECT_DICT),
        (README_CORRECT_FOUR_LEVEL, CORRECT_DICT_FOUR_LEVEL),
    ],
)
def test_readme_from_string_correct(readme_md, expected_dict):
    assert ReadMe.from_string(readme_md, example_yaml_structure).to_dict() == expected_dict


@pytest.mark.parametrize(
    "readme_md, expected_error",
    [
        (README_NO_YAML, EXPECTED_ERROR_README_NO_YAML),
        (README_EMPTY_YAML, EXPECTED_ERROR_README_EMPTY_YAML),
        (README_INCORRECT_YAML, EXPECTED_ERROR_README_INCORRECT_YAML),
        (README_EMPTY, EXPECTED_ERROR_README_EMPTY),
        (README_NONE_SUBSECTION, EXPECTED_ERROR_README_NONE_SUBSECTION),
        (README_MISSING_FIRST_LEVEL, EXPECTED_ERROR_README_MISSING_FIRST_LEVEL),
        (README_MISSING_SUBSECTION, EXPECTED_ERROR_README_MISSING_SUBSECTION),
        (README_MISSING_TEXT, EXPECTED_ERROR_README_MISSING_TEXT),
        (README_WRONG_FIRST_LEVEL, EXPECTED_ERROR_README_WRONG_FIRST_LEVEL),
        (README_MULTIPLE_WRONG_FIRST_LEVEL, EXPECTED_ERROR_README_MULTIPLE_WRONG_FIRST_LEVEL),
        (README_MISSING_CONTENT, EXPECTED_ERROR_README_MISSING_CONTENT),
    ],
)
def test_readme_from_string_validation_errors(readme_md, expected_error):
    with pytest.raises(ValueError, match=re.escape(expected_error.format(path="root"))):
        readme = ReadMe.from_string(readme_md, example_yaml_structure)
        readme.validate()


@pytest.mark.parametrize(
    "readme_md, expected_error",
    [
        (README_MULTIPLE_SAME_HEADING_1, EXPECTED_ERROR_README_MULTIPLE_SAME_HEADING_1),
    ],
)
def test_readme_from_string_parsing_errors(readme_md, expected_error):
    with pytest.raises(ValueError, match=re.escape(expected_error.format(path="root"))):
        ReadMe.from_string(readme_md, example_yaml_structure)


@pytest.mark.parametrize(
    "readme_md,",
    [
        (README_MULTIPLE_SAME_HEADING_1),
    ],
)
def test_readme_from_string_suppress_parsing_errors(readme_md):
    ReadMe.from_string(readme_md, example_yaml_structure, suppress_parsing_errors=True)


@pytest.mark.parametrize(
    "readme_md, expected_dict",
    [
        (README_CORRECT, CORRECT_DICT),
        (README_CORRECT_FOUR_LEVEL, CORRECT_DICT_FOUR_LEVEL),
    ],
)
def test_readme_from_readme_correct(readme_md, expected_dict):
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = Path(tmp_dir) / "README.md"
        with open(path, "w+") as readme_file:
            readme_file.write(readme_md)
        out = ReadMe.from_readme(path, example_yaml_structure).to_dict()
        assert out["name"] == path
        assert out["text"] == ""
        assert out["is_empty_text"]
        assert out["subsections"] == expected_dict["subsections"]


@pytest.mark.parametrize(
    "readme_md, expected_error",
    [
        (README_NO_YAML, EXPECTED_ERROR_README_NO_YAML),
        (README_EMPTY_YAML, EXPECTED_ERROR_README_EMPTY_YAML),
        (README_INCORRECT_YAML, EXPECTED_ERROR_README_INCORRECT_YAML),
        (README_EMPTY, EXPECTED_ERROR_README_EMPTY),
        (README_NONE_SUBSECTION, EXPECTED_ERROR_README_NONE_SUBSECTION),
        (README_MISSING_FIRST_LEVEL, EXPECTED_ERROR_README_MISSING_FIRST_LEVEL),
        (README_MISSING_SUBSECTION, EXPECTED_ERROR_README_MISSING_SUBSECTION),
        (README_MISSING_TEXT, EXPECTED_ERROR_README_MISSING_TEXT),
        (README_WRONG_FIRST_LEVEL, EXPECTED_ERROR_README_WRONG_FIRST_LEVEL),
        (README_MULTIPLE_WRONG_FIRST_LEVEL, EXPECTED_ERROR_README_MULTIPLE_WRONG_FIRST_LEVEL),
        (README_MISSING_CONTENT, EXPECTED_ERROR_README_MISSING_CONTENT),
    ],
)
def test_readme_from_readme_error(readme_md, expected_error):
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = Path(tmp_dir) / "README.md"
        with open(path, "w+") as readme_file:
            readme_file.write(readme_md)
        expected_error = expected_error.format(path=path)
        with pytest.raises(ValueError, match=re.escape(expected_error)):
            readme = ReadMe.from_readme(path, example_yaml_structure)
            readme.validate()


@pytest.mark.parametrize(
    "readme_md, expected_error",
    [
        (README_MULTIPLE_SAME_HEADING_1, EXPECTED_ERROR_README_MULTIPLE_SAME_HEADING_1),
    ],
)
def test_readme_from_readme_parsing_errors(readme_md, expected_error):
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = Path(tmp_dir) / "README.md"
        with open(path, "w+") as readme_file:
            readme_file.write(readme_md)
        expected_error = expected_error.format(path=path)
        with pytest.raises(ValueError, match=re.escape(expected_error)):
            ReadMe.from_readme(path, example_yaml_structure)


@pytest.mark.parametrize(
    "readme_md,",
    [
        (README_MULTIPLE_SAME_HEADING_1),
    ],
)
def test_readme_from_readme_suppress_parsing_errors(readme_md):
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = Path(tmp_dir) / "README.md"
        with open(path, "w+") as readme_file:
            readme_file.write(readme_md)
        ReadMe.from_readme(path, example_yaml_structure, suppress_parsing_errors=True)
