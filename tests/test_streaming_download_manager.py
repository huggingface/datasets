import os

import pytest

from .utils import require_streaming


TEST_URL = "https://huggingface.co/datasets/lhoestq/test/raw/main/some_text.txt"
TEST_URL_CONTENT = "foo\nbar\nfoobar"


@require_streaming
def test_xopen_local(text_path):
    from datasets.utils.streaming_download_manager import xopen

    with xopen(text_path, encoding="utf-8") as f, open(text_path, encoding="utf-8") as expected_file:
        assert list(f) == list(expected_file)


@require_streaming
def test_xopen_remote():
    from datasets.utils.streaming_download_manager import xopen

    with xopen(TEST_URL, encoding="utf-8") as f:
        assert list(f) == TEST_URL_CONTENT.splitlines(keepends=True)


@require_streaming
@pytest.mark.parametrize("urlpath", [r"C:\\foo\bar.txt", "/foo/bar.txt", "https://f.oo/bar.txt"])
def test_streaming_dl_manager_download_dummy_path(urlpath):
    from datasets.utils.streaming_download_manager import StreamingDownloadManager

    dl_manager = StreamingDownloadManager()
    assert dl_manager.download(urlpath) == urlpath


@require_streaming
def test_streaming_dl_manager_download(text_path):
    from datasets.utils.streaming_download_manager import StreamingDownloadManager, xopen

    dl_manager = StreamingDownloadManager()
    out = dl_manager.download(text_path)
    assert out == text_path
    with xopen(out, encoding="utf-8") as f, open(text_path, encoding="utf-8") as expected_file:
        assert f.read() == expected_file.read()


@require_streaming
@pytest.mark.parametrize("urlpath", [r"C:\\foo\bar.txt", "/foo/bar.txt", "https://f.oo/bar.txt"])
def test_streaming_dl_manager_download_and_extract_no_extraction(urlpath):
    from datasets.utils.streaming_download_manager import StreamingDownloadManager

    dl_manager = StreamingDownloadManager()
    assert dl_manager.download_and_extract(urlpath) == urlpath


@require_streaming
def test_streaming_dl_manager_extract(text_gz_path):
    from datasets.utils.streaming_download_manager import StreamingDownloadManager

    dl_manager = StreamingDownloadManager()
    path = os.path.basename(text_gz_path).rstrip(".gz")
    assert dl_manager.extract(text_gz_path) == f"gzip://{path}::{text_gz_path}"


@require_streaming
def test_streaming_dl_manager_download_and_extract_with_extraction(text_gz_path, text_path):
    from datasets.utils.streaming_download_manager import StreamingDownloadManager, xopen

    dl_manager = StreamingDownloadManager()
    filename = os.path.basename(text_gz_path).rstrip(".gz")
    out = dl_manager.download_and_extract(text_gz_path)
    assert out == f"gzip://{filename}::{text_gz_path}"
    with xopen(out, encoding="utf-8") as f, open(text_path, encoding="utf-8") as expected_file:
        assert f.read() == expected_file.read()
