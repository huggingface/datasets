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
subsections:
  - name: "Dataset Card for X" # First-level markdown heading
    allow_empty: true
    subsections:
      - name: "Table of Contents"
        allow_empty: false
        subsections: null # meaning it should not be checked.
      - name: "Dataset Description"
        allow_empty: false
        subsections:
          - name: "Dataset Summary"
            allow_empty: false
            subsections: null
          - name: "Supported Tasks and Leaderboards"
            allow_empty: true
            subsections: null
          - name: Languages
            allow_empty: true
            subsections: null
"""
)


CORRECT_DICT = {
    "name": "root",
    "text": "",
    "is_empty": True,
    "subsections": [
        {
            "name": "Dataset Card for My Dataset",
            "text": "",
            "is_empty": True,
            "subsections": [
                {"name": "Table of Contents", "text": "Some text here.", "is_empty": False, "subsections": []},
                {
                    "name": "Dataset Description",
                    "text": "Some text here.",
                    "is_empty": False,
                    "subsections": [
                        {
                            "name": "Dataset Summary",
                            "text": "Some text here.",
                            "is_empty": False,
                            "subsections": [],
                        },
                        {
                            "name": "Supported Tasks and Leaderboards",
                            "text": "",
                            "is_empty": True,
                            "subsections": [],
                        },
                        {"name": "Languages", "text": "", "is_empty": True, "subsections": []},
                    ],
                },
            ],
        }
    ],
}

README_CORRECT = """\
---
languages:
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
"""

EXPECTED_ERROR_README_NO_YAML = (
    "The following issues were found for the README at `{path}`:\n-\tNo YAML markers are present in the README."
)

README_MISSING_TEXT = """\
---
languages:
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
"""
EXPECTED_ERROR_README_MISSING_TEXT = "The following issues were found for the README at `{path}`:\n-\tExpected some header text for section 'Dataset Summary'."

README_MISSING_SUBSECTION = """\
---
languages:
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
"""

EXPECTED_ERROR_README_MISSING_SUBSECTION = "The following issues were found for the README at `{path}`:\n-\tSection 'Dataset Description' is missing subsection: 'Supported Tasks and Leaderboards'."

README_MISSING_FIRST_LEVEL = """\
---
languages:
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
"""
EXPECTED_ERROR_README_MISSING_FIRST_LEVEL = "The following issues were found for the README at `{path}`:\n-\tThe README has no first-level headings. One heading is expected. Skipping further validation for this README."

README_MULTIPLE_WRONG_FIRST_LEVEL = """\
---
languages:
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
# Dataset Card My Dataset
"""

EXPECTED_ERROR_README_MULTIPLE_WRONG_FIRST_LEVEL = "The following issues were found for the README at `{path}`:\n-\tThe README has several first-level headings: \['Dataset Card for My Dataset', 'Dataset Card My Dataset'\]. Only one heading is expected. Skipping further validation for this README."

README_WRONG_FIRST_LEVEL = """\
---
languages:
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
"""

EXPECTED_ERROR_README_WRONG_FIRST_LEVEL = "The following issues were found for the README at `{path}`:\n-\tNo first-level heading starting with `Dataset Card for` found in README. Skipping further validation for this README."

README_EMPTY = ""

EXPECTED_ERROR_README_EMPTY = "The following issues were found for the README at `{path}`:\n-\tThe README has no first-level headings. One heading is expected. Skipping further validation for this README.\n-\tNo YAML markers are present in the README."

README_MULTIPLE_SAME_HEADING_1 = """\
---
languages:
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
"""

EXPECTED_ERROR_README_MULTIPLE_SAME_HEADING_1 = "The following issues were found for the README at `{path}`:\n-\tMultiple sections with the same heading 'Dataset Card for My Dataset' have been found. Please keep only one of these sections."


def test_readme_from_string_correct():

    assert ReadMe.from_string(README_CORRECT, example_yaml_structure).to_dict() == CORRECT_DICT


@pytest.mark.parametrize(
    "readme_md, expected_error",
    [
        (README_NO_YAML, EXPECTED_ERROR_README_NO_YAML),
        (README_EMPTY_YAML, EXPECTED_ERROR_README_EMPTY_YAML),
        (README_EMPTY, EXPECTED_ERROR_README_EMPTY),
        (README_MISSING_FIRST_LEVEL, EXPECTED_ERROR_README_MISSING_FIRST_LEVEL),
        (README_MISSING_SUBSECTION, EXPECTED_ERROR_README_MISSING_SUBSECTION),
        (README_MISSING_TEXT, EXPECTED_ERROR_README_MISSING_TEXT),
        (README_MULTIPLE_SAME_HEADING_1, EXPECTED_ERROR_README_MULTIPLE_SAME_HEADING_1),
        (README_WRONG_FIRST_LEVEL, EXPECTED_ERROR_README_WRONG_FIRST_LEVEL),
        (README_MULTIPLE_WRONG_FIRST_LEVEL, EXPECTED_ERROR_README_MULTIPLE_WRONG_FIRST_LEVEL),
    ],
)
def test_readme_from_string_errors(readme_md, expected_error):
    with pytest.raises(ValueError, match=expected_error.format(path="root")):
        ReadMe.from_string(readme_md, example_yaml_structure)


def test_readme_from_readme_correct():
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = Path(tmp_dir) / "README.md"
        with open(path, "w+") as readme_file:
            readme_file.write(README_CORRECT)
        out = ReadMe.from_readme(path, example_yaml_structure).to_dict()
        assert out["name"] == path
        assert out["text"] == ""
        assert out["is_empty"] == True
        assert out["subsections"] == CORRECT_DICT["subsections"]


@pytest.mark.parametrize(
    "readme_md, expected_error",
    [
        (README_NO_YAML, EXPECTED_ERROR_README_NO_YAML),
        (README_EMPTY_YAML, EXPECTED_ERROR_README_EMPTY_YAML),
        (README_EMPTY, EXPECTED_ERROR_README_EMPTY),
        (README_MISSING_FIRST_LEVEL, EXPECTED_ERROR_README_MISSING_FIRST_LEVEL),
        (README_MISSING_SUBSECTION, EXPECTED_ERROR_README_MISSING_SUBSECTION),
        (README_MISSING_TEXT, EXPECTED_ERROR_README_MISSING_TEXT),
        (README_MULTIPLE_SAME_HEADING_1, EXPECTED_ERROR_README_MULTIPLE_SAME_HEADING_1),
        (README_WRONG_FIRST_LEVEL, EXPECTED_ERROR_README_WRONG_FIRST_LEVEL),
        (README_MULTIPLE_WRONG_FIRST_LEVEL, EXPECTED_ERROR_README_MULTIPLE_WRONG_FIRST_LEVEL),
    ],
)
def test_readme_from_readme_error(readme_md, expected_error):
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = Path(tmp_dir) / "README.md"
        with open(path, "w+") as readme_file:
            readme_file.write(readme_md)
        with pytest.raises(ValueError, match=expected_error.format(path=path)):
            ReadMe.from_readme(path, example_yaml_structure)
