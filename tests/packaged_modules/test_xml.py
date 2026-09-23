import textwrap

import pytest

from datasets import load_dataset
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.xml.xml import XmlConfig


@pytest.fixture
def xml_file(tmp_path):
    filename = tmp_path / "file.xml"
    data = textwrap.dedent(
        """\
        <?xml version="1.0" encoding="UTF-8"?>
        <catalog>
          <book id="1"><title>First</title></book>
          <book id="2"><title>Second</title></book>
        </catalog>
        """
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def second_xml_file(tmp_path):
    filename = tmp_path / "other.xml"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("<catalog><book id=\"3\"><title>Third</title></book></catalog>\n")
    return str(filename)


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = XmlConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = XmlConfig(name="name", data_files=data_files)


def test_xml_load_single_file(xml_file):
    """The whole document is read into one row under an `xml` column."""
    ds = load_dataset("xml", data_files=xml_file, split="train")
    assert ds.column_names == ["xml"]
    assert ds.num_rows == 1
    assert "<title>First</title>" in ds[0]["xml"]
    assert "<title>Second</title>" in ds[0]["xml"]


def test_xml_load_multiple_files(xml_file, second_xml_file):
    """One row per file, in the order the files were given."""
    ds = load_dataset("xml", data_files=[xml_file, second_xml_file], split="train")
    assert ds.num_rows == 2
    assert "<title>First</title>" in ds[0]["xml"]
    assert "<title>Third</title>" in ds[1]["xml"]


def test_xml_respects_encoding(tmp_path):
    filename = tmp_path / "latin.xml"
    with open(filename, "w", encoding="latin-1") as f:
        f.write("<root><a>café</a></root>")
    ds = load_dataset("xml", data_files=str(filename), split="train", encoding="latin-1")
    assert "café" in ds[0]["xml"]
