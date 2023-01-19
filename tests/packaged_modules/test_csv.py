import os
import textwrap

import pyarrow as pa
import pytest

from datasets import ClassLabel, Features, Image
from datasets.packaged_modules.csv.csv import Csv

from ..utils import require_pil


@pytest.fixture
def csv_file(tmp_path):
    filename = tmp_path / "file.csv"
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
def csv_file_with_image(tmp_path, image_file):
    filename = tmp_path / "csv_with_image.csv"
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
def csv_file_with_label(tmp_path):
    filename = tmp_path / "csv_with_label.csv"
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
def csv_file_with_int_list(tmp_path):
    filename = tmp_path / "csv_with_int_list.csv"
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


def test_csv_generate_tables_raises_error_with_malformed_csv(csv_file, malformed_csv_file, caplog):
    csv = Csv()
    generator = csv._generate_tables([[csv_file, malformed_csv_file]])
    with pytest.raises(ValueError, match="Error tokenizing data"):
        for _ in generator:
            pass
    assert any(
        record.levelname == "ERROR"
        and "Failed to read file" in record.message
        and os.path.basename(malformed_csv_file) in record.message
        for record in caplog.records
    )


@require_pil
def test_csv_cast_image(csv_file_with_image):
    with open(csv_file_with_image, encoding="utf-8") as f:
        image_file = f.read().splitlines()[1]
    csv = Csv(encoding="utf-8", features=Features({"image": Image()}))
    generator = csv._generate_tables([[csv_file_with_image]])
    pa_table = pa.concat_tables([table for _, table in generator])
    assert pa_table.schema.field("image").type == Image()()
    generated_content = pa_table.to_pydict()["image"]
    assert generated_content == [{"path": image_file, "bytes": None}]


def test_csv_cast_label(csv_file_with_label):
    with open(csv_file_with_label, encoding="utf-8") as f:
        labels = f.read().splitlines()[1:]
    csv = Csv(encoding="utf-8", features=Features({"label": ClassLabel(names=["good", "bad"])}))
    generator = csv._generate_tables([[csv_file_with_label]])
    pa_table = pa.concat_tables([table for _, table in generator])
    assert pa_table.schema.field("label").type == ClassLabel(names=["good", "bad"])()
    generated_content = pa_table.to_pydict()["label"]
    assert generated_content == [ClassLabel(names=["good", "bad"]).str2int(label) for label in labels]


def test_csv_convert_int_list(csv_file_with_int_list):
    csv = Csv(encoding="utf-8", sep=",", converters={"int_list": lambda x: [int(i) for i in x.split()]})
    generator = csv._generate_tables([[csv_file_with_int_list]])
    pa_table = pa.concat_tables([table for _, table in generator])
    assert pa.types.is_list(pa_table.schema.field("int_list").type)
    generated_content = pa_table.to_pydict()["int_list"]
    assert generated_content == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
