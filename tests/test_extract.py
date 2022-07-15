import pytest

from datasets.utils.extract import Extractor, SevenZipExtractor, ZstdExtractor

from .utils import require_py7zr, require_zstandard


@require_py7zr
def test_seven_zip_extractor(seven_zip_file, tmp_path, text_file):
    input_path = seven_zip_file
    assert SevenZipExtractor.is_extractable(input_path)
    output_path = tmp_path / "extracted"
    SevenZipExtractor.extract(input_path, output_path)
    assert output_path.is_dir()
    for file_path in output_path.iterdir():
        assert file_path.name == text_file.name
        extracted_file_content = file_path.read_text(encoding="utf-8")
    expected_file_content = text_file.read_text(encoding="utf-8")
    assert extracted_file_content == expected_file_content


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
@pytest.mark.parametrize(
    "compression_format, is_archive", [("gzip", False), ("xz", False), ("zstd", False), ("bz2", False), ("7z", True)]
)
def test_extractor(
    compression_format, is_archive, gz_file, xz_file, zstd_file, bz2_file, seven_zip_file, tmp_path, text_file
):
    input_paths = {"gzip": gz_file, "xz": xz_file, "zstd": zstd_file, "bz2": bz2_file, "7z": seven_zip_file}
    input_path = input_paths[compression_format]
    if input_path is None:
        reason = f"for '{compression_format}' compression_format, "
        if compression_format == "7z":
            reason += require_py7zr.kwargs["reason"]
        pytest.skip(reason)
    input_path = str(input_path)
    assert Extractor.is_extractable(input_path)
    output_path = tmp_path / ("extracted" if is_archive else "extracted.txt")
    Extractor.extract(input_path, output_path)
    if is_archive:
        assert output_path.is_dir()
        for file_path in output_path.iterdir():
            assert file_path.name == text_file.name
            extracted_file_content = file_path.read_text(encoding="utf-8")
    else:
        extracted_file_content = output_path.read_text(encoding="utf-8")
    expected_file_content = text_file.read_text(encoding="utf-8")
    assert extracted_file_content == expected_file_content
