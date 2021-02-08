import json
import os
from pathlib import Path

import pytest

from datasets.utils.download_manager import DownloadConfig, DownloadManager

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


@pytest.mark.parametrize("urls", [URL, [URL], {"train": URL}])
def test_download_manager_download(urls, tmp_path, monkeypatch):
    import requests
    monkeypatch.setattr(requests, "request", mock_request)

    dataset_name = "dummy"
    cache_subdir = "downloads"
    cache_dir_root = str(tmp_path)
    download_config = DownloadConfig(
        cache_dir=os.path.join(cache_dir_root, cache_subdir),
        use_etag=False,
    )
    dl_manager = DownloadManager(dataset_name=dataset_name, download_config=download_config)
    downloaded_paths = dl_manager.download(urls)
    if isinstance(urls, str):
        downloaded_paths = [downloaded_paths]
    elif isinstance(urls, dict):
        assert "train" in downloaded_paths.keys()
        downloaded_paths = downloaded_paths.values()
    assert downloaded_paths
    for downloaded_path in downloaded_paths:
        downloaded_path = Path(downloaded_path)
        parts = downloaded_path.parts
        assert parts[-1] == HASH
        assert parts[-2] == cache_subdir
        assert downloaded_path.exists()
        with open(downloaded_path, "r") as f:
            content = f.read()
        assert content == CONTENT
        metadata_downloaded_path = downloaded_path.with_suffix(".json")
        assert metadata_downloaded_path.exists()
        with open(metadata_downloaded_path, "r") as f:
            metadata_content = json.load(f)
        assert metadata_content == {"url": URL, "etag": None}
