import pytest

from datasets.utils.extract import Extractor, ZstdExtractor

from .utils import require_zstandard


@require_zstandard
def test_zstd_extractor(zstd_file, tmp_path, text_file):
    input_path = zstd_file
    assert ZstdExtractor.is_extractable(input_path)
    output_path = str(tmp_path / "extracted.txt")
    ZstdExtractor.extract(input_path, output_path)
    with open(output_path) as f:
        extracted_file_content = f.read()
    with open(text_file) as f:
        expected_file_content = f.read()
    assert extracted_file_content == expected_file_content


@require_zstandard
@pytest.mark.parametrize("compression_format", ["gzip", "xz", "zstd"])
def test_extractor(compression_format, gz_file, xz_file, zstd_file, tmp_path, text_file):
    input_paths = {"gzip": gz_file, "xz": xz_file, "zstd": zstd_file}
    input_path = str(input_paths[compression_format])
    output_path = str(tmp_path / "extracted.txt")
    assert Extractor.is_extractable(input_path)
    Extractor.extract(input_path, output_path)
    with open(output_path) as f:
        extracted_file_content = f.read()
    with open(text_file) as f:
        expected_file_content = f.read()
    assert extracted_file_content == expected_file_content
