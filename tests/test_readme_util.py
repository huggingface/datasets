import tempfile
import unittest
from pathlib import Path

import yaml

from datasets.utils.readme import ReadMe


def _dedent(string: str) -> str:
    return "\n".join([line.lstrip() for line in string.splitlines()])


EXPECTED_STRUCTURE = yaml.safe_load(
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
"""

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

README_EMPTY = ""

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


class TestReadMeUtils(unittest.TestCase):
    def test_from_string(self):
        ReadMe.from_string(README_CORRECT, EXPECTED_STRUCTURE)
        with self.assertRaises(ValueError):
            ReadMe.from_string(README_EMPTY_YAML, EXPECTED_STRUCTURE)
        with self.assertRaises(ValueError):
            ReadMe.from_string(README_INCORRECT_YAML, EXPECTED_STRUCTURE)
        with self.assertRaises(ValueError):
            ReadMe.from_string(README_NO_YAML, EXPECTED_STRUCTURE)
        with self.assertRaises(ValueError):
            ReadMe.from_string(README_MISSING_TEXT, EXPECTED_STRUCTURE)
        with self.assertRaises(ValueError):
            ReadMe.from_string(README_MISSING_SUBSECTION, EXPECTED_STRUCTURE)
        with self.assertRaises(ValueError):
            ReadMe.from_string(README_MISSING_FIRST_LEVEL, EXPECTED_STRUCTURE)
        with self.assertRaises(ValueError):
            ReadMe.from_string(README_MULTIPLE_WRONG_FIRST_LEVEL, EXPECTED_STRUCTURE)
        with self.assertRaises(ValueError):
            ReadMe.from_string(README_WRONG_FIRST_LEVEL, EXPECTED_STRUCTURE)
        with self.assertRaises(ValueError):
            ReadMe.from_string(README_EMPTY, EXPECTED_STRUCTURE)

        ReadMe.from_string(README_MULTIPLE_SAME_HEADING_1, EXPECTED_STRUCTURE)
        # ReadMe.from_string(MISSING_SUBSECTION, EXPECTED_STRUCTURE)
        # ReadMe.from_string(README_CORRECT, EXPECTED_STRUCTURE)
        # ReadMe.from_string(README_CORRECT, EXPECTED_STRUCTURE)
        # ReadMe.from_string(README_CORRECT, EXPECTED_STRUCTURE)
        # ReadMe.from_string(README_CORRECT, EXPECTED_STRUCTURE)
        # ReadMe.from_string(README_CORRECT, EXPECTED_STRUCTURE)


if __name__ == "__main__":
    unittest.main()
