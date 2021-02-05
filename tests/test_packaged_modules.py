import textwrap

import pytest

from datasets.packaged_modules.csv.csv import Csv


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


def test_csv_generate_tables_raises_error_with_malformed_csv(csv_file, malformed_csv_file, capsys):
    csv = Csv()
    generator = csv._generate_tables([csv_file, malformed_csv_file])
    with pytest.raises(ValueError, match="Error tokenizing data"):
        for _ in generator:
            pass
    captured = capsys.readouterr()
    assert f"Failed to read file '{malformed_csv_file}'" in captured.out
