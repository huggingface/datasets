import os

import pytest

from datasets.filesystems import COMPRESSION_FILESYSTEMS
from datasets.utils.streaming_download_manager import xopen

from .utils import require_lz4, require_zstandard


TEST_URL = "https://huggingface.co/datasets/lhoestq/test/raw/main/some_text.txt"
TEST_URL_CONTENT = "foo\nbar\nfoobar"


@pytest.mark.parametrize(
    "input_path, paths_to_join, expected_path",
    [
        ("https://host.com/archive.zip", ("file.txt",), "https://host.com/archive.zip/file.txt"),
        (
            "zip://::https://host.com/archive.zip",
            ("file.txt",),
            "zip://file.txt::https://host.com/archive.zip",
        ),
        (
            "zip://folder::https://host.com/archive.zip",
            ("file.txt",),
            "zip://folder/file.txt::https://host.com/archive.zip",
        ),
    ],
)
def test_xjoin(input_path, paths_to_join, expected_path):
    from datasets.utils.streaming_download_manager import xjoin

    output_path = xjoin(input_path, *paths_to_join)
    assert output_path == expected_path


def test_xopen_local(text_path):

    with xopen(text_path, encoding="utf-8") as f, open(text_path, encoding="utf-8") as expected_file:
        assert list(f) == list(expected_file)


def test_xopen_remote():
    from datasets.utils.streaming_download_manager import xopen

    with xopen(TEST_URL, encoding="utf-8") as f:
        assert list(f) == TEST_URL_CONTENT.splitlines(keepends=True)


@pytest.mark.parametrize("urlpath", [r"C:\\foo\bar.txt", "/foo/bar.txt", "https://f.oo/bar.txt"])
def test_streaming_dl_manager_download_dummy_path(urlpath):
    from datasets.utils.streaming_download_manager import StreamingDownloadManager

    dl_manager = StreamingDownloadManager()
    assert dl_manager.download(urlpath) == urlpath


def test_streaming_dl_manager_download(text_path):
    from datasets.utils.streaming_download_manager import StreamingDownloadManager, xopen

    dl_manager = StreamingDownloadManager()
    out = dl_manager.download(text_path)
    assert out == text_path
    with xopen(out, encoding="utf-8") as f, open(text_path, encoding="utf-8") as expected_file:
        assert f.read() == expected_file.read()


@pytest.mark.parametrize("urlpath", [r"C:\\foo\bar.txt", "/foo/bar.txt", "https://f.oo/bar.txt"])
def test_streaming_dl_manager_download_and_extract_no_extraction(urlpath):
    from datasets.utils.streaming_download_manager import StreamingDownloadManager

    dl_manager = StreamingDownloadManager()
    assert dl_manager.download_and_extract(urlpath) == urlpath


def test_streaming_dl_manager_extract(text_gz_path, text_path):
    from datasets.utils.streaming_download_manager import StreamingDownloadManager, xopen

    dl_manager = StreamingDownloadManager()
    output_path = dl_manager.extract(text_gz_path)
    path = os.path.basename(text_gz_path).rstrip(".gz")
    assert output_path == f"gzip://{path}::{text_gz_path}"
    fsspec_open_file = xopen(output_path, encoding="utf-8")
    with fsspec_open_file as f, open(text_path, encoding="utf-8") as expected_file:
        assert f.read() == expected_file.read()


def test_streaming_dl_manager_download_and_extract_with_extraction(text_gz_path, text_path):
    from datasets.utils.streaming_download_manager import StreamingDownloadManager, xopen

    dl_manager = StreamingDownloadManager()
    output_path = dl_manager.download_and_extract(text_gz_path)
    path = os.path.basename(text_gz_path).rstrip(".gz")
    assert output_path == f"gzip://{path}::{text_gz_path}"
    fsspec_open_file = xopen(output_path, encoding="utf-8")
    with fsspec_open_file as f, open(text_path, encoding="utf-8") as expected_file:
        assert f.read() == expected_file.read()


@pytest.mark.parametrize(
    "input_path, filename, expected_path",
    [("https://domain.org/archive.zip", "filename.jsonl", "zip://filename.jsonl::https://domain.org/archive.zip")],
)
def test_streaming_dl_manager_download_and_extract_with_join(input_path, filename, expected_path):
    from datasets.utils.streaming_download_manager import StreamingDownloadManager, xjoin

    dl_manager = StreamingDownloadManager()
    extracted_path = dl_manager.download_and_extract(input_path)
    output_path = xjoin(extracted_path, filename)
    assert output_path == expected_path


@require_zstandard
@require_lz4
@pytest.mark.parametrize("compression_fs_class", COMPRESSION_FILESYSTEMS)
def test_streaming_dl_manager_extract_all_supported_single_file_compression_types(
    compression_fs_class, gz_file, xz_file, zstd_file, bz2_file, lz4_file, text_file
):
    from datasets.utils.streaming_download_manager import StreamingDownloadManager, xopen

    input_paths = {"gzip": gz_file, "xz": xz_file, "zstd": zstd_file, "bz2": bz2_file, "lz4": lz4_file}
    input_path = str(input_paths[compression_fs_class.protocol])
    dl_manager = StreamingDownloadManager()
    output_path = dl_manager.extract(input_path)
    path = os.path.basename(input_path)
    path = path[: path.rindex(".")]
    assert output_path == f"{compression_fs_class.protocol}://{path}::{input_path}"
    fsspec_open_file = xopen(output_path, encoding="utf-8")
    with fsspec_open_file as f, open(text_file, encoding="utf-8") as expected_file:
        assert f.read() == expected_file.read()
