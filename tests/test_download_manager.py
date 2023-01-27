import json
import os
from pathlib import Path

import pytest

from datasets.download.download_config import DownloadConfig
from datasets.download.download_manager import DownloadManager
from datasets.utils.file_utils import hash_url_to_filename


URL = "http://www.mocksite.com/file1.txt"
CONTENT = '"text": ["foo", "foo"]'
HASH = "6d8ce9aa78a471c7477201efbeabd3bb01ac2e7d100a6dc024ba1608361f90a8"


class MockResponse:
    status_code = 200
    headers = {"Content-Length": "100"}
    cookies = {}

    def iter_content(self, **kwargs):
        return [bytes(CONTENT, "utf-8")]


def mock_request(*args, **kwargs):
    return MockResponse()


@pytest.mark.parametrize("urls_type", [str, list, dict])
def test_download_manager_download(urls_type, tmp_path, monkeypatch):
    import requests

    monkeypatch.setattr(requests, "request", mock_request)

    url = URL
    if issubclass(urls_type, str):
        urls = url
    elif issubclass(urls_type, list):
        urls = [url]
    elif issubclass(urls_type, dict):
        urls = {"train": url}
    dataset_name = "dummy"
    cache_subdir = "downloads"
    cache_dir_root = tmp_path
    download_config = DownloadConfig(
        cache_dir=os.path.join(cache_dir_root, cache_subdir),
        use_etag=False,
    )
    dl_manager = DownloadManager(dataset_name=dataset_name, download_config=download_config)
    downloaded_paths = dl_manager.download(urls)
    input_urls = urls
    for downloaded_paths in [downloaded_paths]:
        if isinstance(urls, str):
            downloaded_paths = [downloaded_paths]
            input_urls = [urls]
        elif isinstance(urls, dict):
            assert "train" in downloaded_paths.keys()
            downloaded_paths = downloaded_paths.values()
            input_urls = urls.values()
        assert downloaded_paths
        for downloaded_path, input_url in zip(downloaded_paths, input_urls):
            assert downloaded_path == dl_manager.downloaded_paths[input_url]
            downloaded_path = Path(downloaded_path)
            parts = downloaded_path.parts
            assert parts[-1] == HASH
            assert parts[-2] == cache_subdir
            assert downloaded_path.exists()
            content = downloaded_path.read_text()
            assert content == CONTENT
            metadata_downloaded_path = downloaded_path.with_suffix(".json")
            assert metadata_downloaded_path.exists()
            metadata_content = json.loads(metadata_downloaded_path.read_text())
            assert metadata_content == {"url": URL, "etag": None}


@pytest.mark.parametrize("paths_type", [str, list, dict])
def test_download_manager_extract(paths_type, xz_file, text_file):
    filename = str(xz_file)
    if issubclass(paths_type, str):
        paths = filename
    elif issubclass(paths_type, list):
        paths = [filename]
    elif issubclass(paths_type, dict):
        paths = {"train": filename}
    dataset_name = "dummy"
    cache_dir = xz_file.parent
    extracted_subdir = "extracted"
    download_config = DownloadConfig(
        cache_dir=cache_dir,
        use_etag=False,
    )
    dl_manager = DownloadManager(dataset_name=dataset_name, download_config=download_config)
    extracted_paths = dl_manager.extract(paths)
    input_paths = paths
    for extracted_paths in [extracted_paths]:
        if isinstance(paths, str):
            extracted_paths = [extracted_paths]
            input_paths = [paths]
        elif isinstance(paths, dict):
            assert "train" in extracted_paths.keys()
            extracted_paths = extracted_paths.values()
            input_paths = paths.values()
        assert extracted_paths
        for extracted_path, input_path in zip(extracted_paths, input_paths):
            assert extracted_path == dl_manager.extracted_paths[input_path]
            extracted_path = Path(extracted_path)
            parts = extracted_path.parts
            assert parts[-1] == hash_url_to_filename(input_path, etag=None)
            assert parts[-2] == extracted_subdir
            assert extracted_path.exists()
            extracted_file_content = extracted_path.read_text()
            expected_file_content = text_file.read_text()
            assert extracted_file_content == expected_file_content


def _test_jsonl(path, file):
    assert path.endswith(".jsonl")
    for num_items, line in enumerate(file, start=1):
        item = json.loads(line.decode("utf-8"))
        assert item.keys() == {"col_1", "col_2", "col_3"}
    assert num_items == 4


@pytest.mark.parametrize("archive_jsonl", ["tar_jsonl_path", "zip_jsonl_path"])
def test_iter_archive_path(archive_jsonl, request):
    archive_jsonl_path = request.getfixturevalue(archive_jsonl)
    dl_manager = DownloadManager()
    for num_jsonl, (path, file) in enumerate(dl_manager.iter_archive(archive_jsonl_path), start=1):
        _test_jsonl(path, file)
    assert num_jsonl == 2


@pytest.mark.parametrize("archive_nested_jsonl", ["tar_nested_jsonl_path", "zip_nested_jsonl_path"])
def test_iter_archive_file(archive_nested_jsonl, request):
    archive_nested_jsonl_path = request.getfixturevalue(archive_nested_jsonl)
    dl_manager = DownloadManager()
    for num_tar, (path, file) in enumerate(dl_manager.iter_archive(archive_nested_jsonl_path), start=1):
        for num_jsonl, (subpath, subfile) in enumerate(dl_manager.iter_archive(file), start=1):
            _test_jsonl(subpath, subfile)
    assert num_tar == 1
    assert num_jsonl == 2


def test_iter_files(data_dir_with_hidden_files):
    dl_manager = DownloadManager()
    for num_file, file in enumerate(dl_manager.iter_files(data_dir_with_hidden_files), start=1):
        assert os.path.basename(file) == ("test.txt" if num_file == 1 else "train.txt")
    assert num_file == 2
