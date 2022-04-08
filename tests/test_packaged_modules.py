import os
import textwrap

import pyarrow as pa
import pytest

from datasets import Features, Image, Value
from datasets.packaged_modules.csv.csv import Csv
from datasets.packaged_modules.imagefolder.imagefolder import ImageFolder
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
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def image_file():
    return os.path.join(os.path.dirname(__file__), "features", "data", "test_image_rgb.jpg")


@pytest.fixture
def image_file_with_metadata(tmp_path):
    image_filename = tmp_path / "image_rgb.jpg"
    with open(os.path.join(os.path.dirname(__file__), "features", "data", "test_image_rgb.jpg"), "rb") as f1:
        with open(image_filename, "wb") as f2:
            f2.write(f1.read())
    image_metadata_filename = tmp_path / "metadata.jsonl"
    image_metadata = textwrap.dedent(
        """\
        {"file_name": "image_rgb.jpg", "caption": "Nice image"}
        """
    )
    with open(image_metadata_filename, "w", encoding="utf-8") as f:
        f.write(image_metadata)
    return str(image_filename), str(image_metadata_filename)


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
    with open(text_file, encoding="utf-8") as f:
        expected_content = f.read().splitlines(keepends=keep_linebreaks)
    text = Text(keep_linebreaks=keep_linebreaks, encoding="utf-8")
    generator = text._generate_tables([text_file])
    generated_content = pa.concat_tables([table for _, table in generator]).to_pydict()["text"]
    assert generated_content == expected_content


@pytest.mark.parametrize("drop_labels", [True, False])
def test_imagefolder_drop_labels(image_file, drop_labels):
    imagefolder = ImageFolder(drop_labels=drop_labels)
    generator = imagefolder._generate_examples([(image_file, image_file)], None, "train")
    if not drop_labels:
        assert all(
            example.keys() == {"image", "label"} and all(val is not None for val in example.values())
            for _, example in generator
        )
    else:
        assert all(
            example.keys() == {"image"} and all(val is not None for val in example.values())
            for _, example in generator
        )


@pytest.mark.parametrize("drop_metadata", [True, False])
def test_imagefolder_drop_metadata(image_file_with_metadata, drop_metadata):
    image_file, image_metadata_file = image_file_with_metadata
    if not drop_metadata:
        features = Features({"image": Image(), "label": Value("string"), "caption": Value("string")})
    else:
        features = Features({"image": Image(), "label": Value("string")})
    imagefolder = ImageFolder(drop_metadata=drop_metadata, features=features)
    generator = imagefolder._generate_examples(
        [(image_file, image_file)], {"train": [(image_metadata_file, image_metadata_file)]}, "train"
    )
    if not drop_metadata:
        assert all(
            example.keys() == {"image", "label", "caption"} and all(val is not None for val in example.values())
            for _, example in generator
        )
    else:
        assert all(
            example.keys() == {"image", "label"} and all(val is not None for val in example.values())
            for _, example in generator
        )
