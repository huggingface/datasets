import pytest
import zstandard as zstd

from datasets.utils.extract import Extractor, ZstdExtractor


FILE_CONTENT = """\
    Text data.
    Second line of data."""


@pytest.fixture(scope="session")
def zstd_path(tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / "file.zstd"
    data = bytes(FILE_CONTENT, "utf-8")
    with zstd.open(path, "wb") as f:
        f.write(data)
    return path


def test_zstd_extractor(zstd_path, tmp_path, text_file):
    input_path = zstd_path
    assert ZstdExtractor.is_extractable(input_path)
    output_path = str(tmp_path / "extracted.txt")
    ZstdExtractor.extract(input_path, output_path)
    with open(output_path) as f:
        extracted_file_content = f.read()
    with open(text_file) as f:
        expected_file_content = f.read()
    assert extracted_file_content == expected_file_content


@pytest.mark.parametrize(
    "compression_format, expected_text_path_name", [("gzip", "text_path"), ("xz", "text_file"), ("zstd", "text_file")]
)
def test_extractor(
    compression_format, expected_text_path_name, text_gz_path, xz_file, zstd_path, tmp_path, text_file, text_path
):
    input_paths = {"gzip": text_gz_path, "xz": xz_file, "zstd": zstd_path}
    input_path = str(input_paths[compression_format])
    output_path = str(tmp_path / "extracted.txt")
    assert Extractor.is_extractable(input_path)
    Extractor.extract(input_path, output_path)
    with open(output_path) as f:
        extracted_file_content = f.read()
    expected_text_paths = {"text_file": text_file, "text_path": text_path}
    expected_text_path = str(expected_text_paths[expected_text_path_name])
    with open(expected_text_path) as f:
        expected_file_content = f.read()
    assert extracted_file_content == expected_file_content
