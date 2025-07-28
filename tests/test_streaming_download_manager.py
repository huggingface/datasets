import json
import os

import pytest

from datasets.download.streaming_download_manager import (
    StreamingDownloadManager,
    xbasename,
    xglob,
    xjoin,
    xopen,
)
from datasets.filesystems import COMPRESSION_FILESYSTEMS

from .utils import require_lz4, require_zstandard, slow


TEST_GG_DRIVE_FILENAME = "train.tsv"
TEST_GG_DRIVE_URL = "https://drive.google.com/uc?export=download&id=17bOgBDc3hRCoPZ89EYtKDzK-yXAWat94"
TEST_GG_DRIVE_GZIPPED_URL = "https://drive.google.com/uc?export=download&id=1Bt4Garpf0QLiwkJhHJzXaVa0I0H5Qhwz"
TEST_GG_DRIVE_ZIPPED_URL = "https://drive.google.com/uc?export=download&id=1k92sUfpHxKq8PXWRr7Y5aNHXwOCNUmqh"
TEST_GG_DRIVE_CONTENT = """\
pokemon_name, type
Charmander, fire
Squirtle, water
Bulbasaur, grass"""


@pytest.mark.parametrize("urlpath", [r"C:\\foo\bar.txt", "/foo/bar.txt", "https://f.oo/bar.txt"])
def test_streaming_dl_manager_download_dummy_path(urlpath):
    dl_manager = StreamingDownloadManager()
    assert dl_manager.download(urlpath) == urlpath


@pytest.mark.parametrize(
    "urlpath",
    [
        "zip://train-00000.tar.gz::https://foo.bar/data.zip",
        "https://foo.bar/train.tar.gz",
        "https://foo.bar/train.tgz",
        "https://foo.bar/train.tar",
    ],
)
def test_streaming_dl_manager_extract_throws(urlpath):
    with pytest.raises(NotImplementedError):
        _ = StreamingDownloadManager().extract(urlpath)


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


@pytest.mark.parametrize("compression_fs_class", COMPRESSION_FILESYSTEMS)
def test_streaming_dl_manager_extract_all_supported_single_file_compression_types(
    compression_fs_class, gz_file, xz_file, zstd_file, bz2_file, lz4_file, text_file
):
    input_paths = {"gzip": gz_file, "xz": xz_file, "zstd": zstd_file, "bz2": bz2_file, "lz4": lz4_file}
    input_path = input_paths[compression_fs_class.protocol]
    if input_path is None:
        reason = f"for '{compression_fs_class.protocol}' compression protocol, "
        if compression_fs_class.protocol == "lz4":
            reason += require_lz4.kwargs["reason"]
        elif compression_fs_class.protocol == "zstd":
            reason += require_zstandard.kwargs["reason"]
        pytest.skip(reason)
    dl_manager = StreamingDownloadManager()
    output_path = dl_manager.extract(input_path)
    path = os.path.basename(input_path)
    path = path[: path.rindex(".")]
    assert output_path == f"{compression_fs_class.protocol}://{path}::{input_path}"
    fsspec_open_file = xopen(output_path, encoding="utf-8")
    with fsspec_open_file as f, open(text_file, encoding="utf-8") as expected_file:
        assert f.read() == expected_file.read()


@slow  # otherwise it spams Google Drive and the CI gets banned
@pytest.mark.integration
def test_streaming_gg_drive_no_extract():
    urlpath = StreamingDownloadManager().download_and_extract(TEST_GG_DRIVE_URL)
    with xopen(urlpath) as f:
        assert f.read() == TEST_GG_DRIVE_CONTENT


@slow  # otherwise it spams Google Drive and the CI gets banned
@pytest.mark.integration
def test_streaming_gg_drive_gzipped():
    urlpath = StreamingDownloadManager().download_and_extract(TEST_GG_DRIVE_GZIPPED_URL)
    with xopen(urlpath) as f:
        assert f.read() == TEST_GG_DRIVE_CONTENT


@slow  # otherwise it spams Google Drive and the CI gets banned
@pytest.mark.integration
def test_streaming_gg_drive_zipped():
    urlpath = StreamingDownloadManager().download_and_extract(TEST_GG_DRIVE_ZIPPED_URL)
    all_files = list(xglob(xjoin(urlpath, "*")))
    assert len(all_files) == 1
    assert xbasename(all_files[0]) == TEST_GG_DRIVE_FILENAME
    with xopen(all_files[0]) as f:
        assert f.read() == TEST_GG_DRIVE_CONTENT


def _test_jsonl(path, file):
    assert path.endswith(".jsonl")
    for num_items, line in enumerate(file, start=1):
        item = json.loads(line.decode("utf-8"))
        assert item.keys() == {"col_1", "col_2", "col_3"}
    assert num_items == 4


@pytest.mark.parametrize("archive_jsonl", ["tar_jsonl_path", "zip_jsonl_path"])
def test_iter_archive_path(archive_jsonl, request):
    archive_jsonl_path = request.getfixturevalue(archive_jsonl)
    dl_manager = StreamingDownloadManager()
    archive_iterable = dl_manager.iter_archive(archive_jsonl_path)
    num_jsonl = 0
    for num_jsonl, (path, file) in enumerate(archive_iterable, start=1):
        _test_jsonl(path, file)
    assert num_jsonl == 2
    # do it twice to make sure it's reset correctly
    num_jsonl = 0
    for num_jsonl, (path, file) in enumerate(archive_iterable, start=1):
        _test_jsonl(path, file)
    assert num_jsonl == 2


@pytest.mark.parametrize("archive_nested_jsonl", ["tar_nested_jsonl_path", "zip_nested_jsonl_path"])
def test_iter_archive_file(archive_nested_jsonl, request):
    archive_nested_jsonl_path = request.getfixturevalue(archive_nested_jsonl)
    dl_manager = StreamingDownloadManager()
    files_iterable = dl_manager.iter_archive(archive_nested_jsonl_path)
    num_tar, num_jsonl = 0, 0
    for num_tar, (path, file) in enumerate(files_iterable, start=1):
        for num_jsonl, (subpath, subfile) in enumerate(dl_manager.iter_archive(file), start=1):
            _test_jsonl(subpath, subfile)
    assert num_tar == 1
    assert num_jsonl == 2
    # do it twice to make sure it's reset correctly
    num_tar, num_jsonl = 0, 0
    for num_tar, (path, file) in enumerate(files_iterable, start=1):
        for num_jsonl, (subpath, subfile) in enumerate(dl_manager.iter_archive(file), start=1):
            _test_jsonl(subpath, subfile)
    assert num_tar == 1
    assert num_jsonl == 2


def test_iter_files(data_dir_with_hidden_files):
    dl_manager = StreamingDownloadManager()
    for num_file, file in enumerate(dl_manager.iter_files(data_dir_with_hidden_files), start=1):
        assert os.path.basename(file) == ("test.txt" if num_file == 1 else "train.txt")
    assert num_file == 2
