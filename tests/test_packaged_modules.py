import os
import textwrap

import pyarrow as pa
import pytest

from datasets.packaged_modules.csv.csv import Csv
from datasets.packaged_modules.text.text import Text


@pytest.fixture
def csv_file(tmp_path):
    filename = tmp_path / "malformed_file.csv"
    data = textwrap.dedent(
        """\
        header1,header2
        1,2
        10,20
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def malformed_csv_file(tmp_path):
    filename = tmp_path / "malformed_file.csv"
    data = textwrap.dedent(
        """\
        header1,header2
        1,2
        10,20,
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def text_file(tmp_path):
    filename = tmp_path / "text.txt"
    data = textwrap.dedent(
        """\
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
        Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


def test_csv_generate_tables_raises_error_with_malformed_csv(csv_file, malformed_csv_file, caplog):
    csv = Csv()
    generator = csv._generate_tables([csv_file, malformed_csv_file])
    with pytest.raises(ValueError, match="Error tokenizing data"):
        for _ in generator:
            pass
    assert any(
        record.levelname == "ERROR"
        and "Failed to read file" in record.message
        and os.path.basename(malformed_csv_file) in record.message
        for record in caplog.records
    )


@pytest.mark.parametrize("keep_linebreaks", [True, False])
def test_text_linebreaks(text_file, keep_linebreaks):
    with open(text_file) as f:
        expected_content = f.read().splitlines(keepends=keep_linebreaks)
    text = Text(keep_linebreaks=keep_linebreaks)
    generator = text._generate_tables([text_file])
    generated_content = pa.concat_tables([table for _, table in generator]).to_pydict()["text"]
    assert generated_content == expected_content
