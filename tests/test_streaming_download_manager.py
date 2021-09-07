import os
import re
from pathlib import Path

import pytest

from datasets.filesystems import COMPRESSION_FILESYSTEMS
from datasets.utils.streaming_download_manager import (
    StreamingDownloadManager,
    _as_posix,
    _get_extraction_protocol,
    xjoin,
    xopen,
    xpathjoin,
    xpathopen,
    xpathstem,
    xpathsuffix,
)

from .utils import require_lz4, require_zstandard


TEST_URL = "https://huggingface.co/datasets/lhoestq/test/raw/main/some_text.txt"
TEST_URL_CONTENT = "foo\nbar\nfoobar"


def _readd_double_slash_removed_by_path(path_as_posix: str) -> str:
    """Path(...) on an url path like zip://file.txt::http://host.com/data.zip
    converts the :// to :/
    This function readds the ://

    It handles cases like:

    - https://host.com/data.zip
    - C://data.zip
    - zip://file.txt::https://host.com/data.zip
    - zip://file.txt::/Users/username/data.zip
    - zip://file.txt::C://data.zip

    Args:
        path_as_posix (str): output of Path(...).as_posix()

    Returns:
        str: the url path with :// instead of :/
    """
    return re.sub("([A-z]:/)([A-z:])", r"\g<1>/\g<2>", path_as_posix)


@pytest.mark.parametrize(
    "input_path, expected_path",
    [("zip:/test.txt::/Users/username/bar.zip", "zip://test.txt::/Users/username/bar.zip")],
)
def test_as_posix(input_path, expected_path):
    assert _as_posix(Path(input_path)) == expected_path


@pytest.mark.parametrize(
    "input_path, paths_to_join, expected_path",
    [
        (str(Path(__file__).resolve().parent), (Path(__file__).name,), str(Path(__file__).resolve())),
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
        (
            ".",
            ("file.txt",),
            "file.txt",
        ),
        (
            Path().resolve().as_posix(),
            ("file.txt",),
            (Path().resolve() / "file.txt").as_posix(),
        ),
    ],
)
def test_xjoin(input_path, paths_to_join, expected_path):
    output_path = xjoin(input_path, *paths_to_join)
    output_path = _readd_double_slash_removed_by_path(Path(output_path).as_posix())
    assert output_path == _readd_double_slash_removed_by_path(Path(expected_path).as_posix())
    output_path = xpathjoin(Path(input_path), *paths_to_join)
    assert output_path == Path(expected_path)


@pytest.mark.parametrize(
    "input_path, expected_path",
    [
        (str(Path(__file__).resolve()), str(Path(__file__).resolve().parent)),
        ("https://host.com/archive.zip", "https://host.com"),
        (
            "zip://file.txt::https://host.com/archive.zip",
            "zip://::https://host.com/archive.zip",
        ),
        (
            "zip://folder/file.txt::https://host.com/archive.zip",
            "zip://folder::https://host.com/archive.zip",
        ),
    ],
)
def test_xdirname(input_path, expected_path):
    from datasets.utils.streaming_download_manager import xdirname

    output_path = xdirname(input_path)
    output_path = _readd_double_slash_removed_by_path(Path(output_path).as_posix())
    assert output_path == _readd_double_slash_removed_by_path(Path(expected_path).as_posix())


def test_xopen_local(text_path):
    with xopen(text_path, encoding="utf-8") as f, open(text_path, encoding="utf-8") as expected_file:
        assert list(f) == list(expected_file)
    with xpathopen(Path(text_path), encoding="utf-8") as f, open(text_path, encoding="utf-8") as expected_file:
        assert list(f) == list(expected_file)


def test_xopen_remote():
    with xopen(TEST_URL, encoding="utf-8") as f:
        assert list(f) == TEST_URL_CONTENT.splitlines(keepends=True)
    with xpathopen(Path(TEST_URL), encoding="utf-8") as f:
        assert list(f) == TEST_URL_CONTENT.splitlines(keepends=True)


@pytest.mark.parametrize(
    "input_path, expected",
    [
        ("zip://file.txt::https://host.com/archive.zip", "file"),
        ("file.txt", "file"),
        ((Path().resolve() / "file.txt").as_posix(), "file"),
    ],
)
def test_xpathstem(input_path, expected):
    assert xpathstem(Path(input_path)) == expected


@pytest.mark.parametrize(
    "input_path, expected",
    [
        ("zip://file.txt::https://host.com/archive.zip", ".txt"),
        ("file.txt", ".txt"),
        ((Path().resolve() / "file.txt").as_posix(), ".txt"),
    ],
)
def test_xpathsuffix(input_path, expected):
    assert xpathsuffix(Path(input_path)) == expected


@pytest.mark.parametrize("urlpath", [r"C:\\foo\bar.txt", "/foo/bar.txt", "https://f.oo/bar.txt"])
def test_streaming_dl_manager_download_dummy_path(urlpath):
    dl_manager = StreamingDownloadManager()
    assert dl_manager.download(urlpath) == urlpath


def test_streaming_dl_manager_download(text_path):
    dl_manager = StreamingDownloadManager()
    out = dl_manager.download(text_path)
    assert out == text_path
    with xopen(out, encoding="utf-8") as f, open(text_path, encoding="utf-8") as expected_file:
        assert f.read() == expected_file.read()


@pytest.mark.parametrize("urlpath", [r"C:\\foo\bar.txt", "/foo/bar.txt", "https://f.oo/bar.txt"])
def test_streaming_dl_manager_download_and_extract_no_extraction(urlpath):
    dl_manager = StreamingDownloadManager()
    assert dl_manager.download_and_extract(urlpath) == urlpath


def test_streaming_dl_manager_extract(text_gz_path, text_path):
    dl_manager = StreamingDownloadManager()
    output_path = dl_manager.extract(text_gz_path)
    path = os.path.basename(text_gz_path)
    path = path[: path.rindex(".")]
    assert output_path == f"gzip://{path}::{text_gz_path}"
    fsspec_open_file = xopen(output_path, encoding="utf-8")
    with fsspec_open_file as f, open(text_path, encoding="utf-8") as expected_file:
        assert f.read() == expected_file.read()


def test_streaming_dl_manager_download_and_extract_with_extraction(text_gz_path, text_path):
    dl_manager = StreamingDownloadManager()
    output_path = dl_manager.download_and_extract(text_gz_path)
    path = os.path.basename(text_gz_path)
    path = path[: path.rindex(".")]
    assert output_path == f"gzip://{path}::{text_gz_path}"
    fsspec_open_file = xopen(output_path, encoding="utf-8")
    with fsspec_open_file as f, open(text_path, encoding="utf-8") as expected_file:
        assert f.read() == expected_file.read()


@pytest.mark.parametrize(
    "input_path, filename, expected_path",
    [("https://domain.org/archive.zip", "filename.jsonl", "zip://filename.jsonl::https://domain.org/archive.zip")],
)
def test_streaming_dl_manager_download_and_extract_with_join(input_path, filename, expected_path):
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


@pytest.mark.parametrize(
    "urlpath, expected_protocol",
    [
        ("zip://train-00000.json.gz::https://foo.bar/data.zip", "gzip"),
        ("https://foo.bar/train.json.gz?dl=1", "gzip"),
        ("http://opus.nlpl.eu/download.php?f=Bianet/v1/moses/en-ku.txt.zip", "zip"),
    ],
)
def test_streaming_dl_manager_get_extraction_protocol(urlpath, expected_protocol):
    assert _get_extraction_protocol(urlpath) == expected_protocol


@pytest.mark.parametrize(
    "urlpath",
    [
        "zip://train-00000.tar.gz::https://foo.bar/data.zip",
        "https://foo.bar/train.tar.gz",
        "https://foo.bar/train.tar",
    ],
)
@pytest.mark.xfail(raises=NotImplementedError)
def test_streaming_dl_manager_get_extraction_protocol_throws(urlpath):
    _get_extraction_protocol(urlpath)
