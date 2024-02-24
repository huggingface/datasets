import os
import textwrap

import pyarrow as pa
import pytest

from datasets import ClassLabel, Features, Image
from datasets.packaged_modules.csv.csv import Csv

from ..utils import require_pil


@pytest.fixture
def tsv_file(tmp_path):
    filename = tmp_path / "file.tsv"
    data = textwrap.dedent(
        """\
        header1\theader2
        1\t2
        10\t20
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def malformed_tsv_file(tmp_path):
    filename = tmp_path / "malformed_file.tsv"
    data = textwrap.dedent(
        """\
        header1\theader2
        1\t2
        10\t20,
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def tsv_file_with_image(tmp_path, image_file):
    filename = tmp_path / "tsv_with_image.tsv"
    data = textwrap.dedent(
        f"""\
        image
        {image_file}
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def tsv_file_with_label(tmp_path):
    filename = tmp_path / "tsv_with_label.tsv"
    data = textwrap.dedent(
        """\
        label
        good
        bad
        good
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def tsv_file_with_int_list(tmp_path):
    filename = tmp_path / "tsv_with_int_list.tsv"
    data = textwrap.dedent(
        """\
        int_list
        1 2 3
        4 5 6
        7 8 9
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


def test_tsv_generate_tables_raises_error_with_malformed_tsv(tsv_file, malformed_tsv_file, caplog):
    tsv = Csv(delimiter="\t")  # Specify delimiter for TSV
    generator = tsv._generate_tables([[tsv_file, malformed_tsv_file]])
    with pytest.raises(ValueError, match="Error tokenizing data"):
        for _ in generator:
            pass
    assert any(
        record.levelname == "ERROR"
        and "Failed to read file" in record.message
        and os.path.basename(malformed_tsv_file) in record.message
        for record in caplog.records
    )


@require_pil
def test_tsv_cast_image(tsv_file_with_image):
    with open(tsv_file_with_image, encoding="utf-8") as f:
        image_file = f.read().splitlines()[1]
    tsv = Csv(encoding="utf-8", features=Features({"image": Image()}))
    generator = tsv._generate_tables([[tsv_file_with_image]])
    pa_table = pa.concat_tables([table for _, table in generator])
    assert pa_table.schema.field("image").type == Image()()
    generated_content = pa_table.to_pydict()["image"]
    assert generated_content == [{"path": image_file, "bytes": None}]


def test_tsv_cast_label(tsv_file_with_label):
    with open(tsv_file_with_label, encoding="utf-8") as f:
        labels = f.read().splitlines()[1:]
    tsv = Csv(
        encoding="utf-8",
        delimiter="\t",  # Specify delimiter for TSV
        features=Features({"label": ClassLabel(names=["good", "bad"])}),
    )
    generator = tsv._generate_
