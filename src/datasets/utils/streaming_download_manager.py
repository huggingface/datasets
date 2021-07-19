import os
import time
from pathlib import Path
from typing import Optional

import fsspec
import posixpath
from aiohttp.client_exceptions import ClientError

from .. import config
from .download_manager import DownloadConfig, map_nested
from .file_utils import get_authentication_headers_for_url, is_local_path, is_relative_path, url_or_path_join
from .logging import get_logger


logger = get_logger(__name__)
BASE_KNOWN_EXTENSIONS = ["txt", "csv", "json", "jsonl", "tsv", "conll"]


def xjoin(a, *p):
    """
    This function extends os.path.join to support the "::" hop separator. It supports both paths and urls.

    A shorthand, particularly useful where you have multiple hops, is to “chain” the URLs with the special separator "::".
    This is used to access files inside a zip file over http for example.

    Let's say you have a zip file at https://host.com/archive.zip, and you want to access the file inside the zip file at /folder1/file.txt.
    Then you can just chain the url this way:

        zip://folder1/file.txt::https://host.com/archive.zip

    The xjoin function allows you to apply the join on the first path of the chain.

    Example::

        >>> xjoin("zip://folder1::https://host.com/archive.zip", "file.txt")
        zip://folder1/file.txt::https://host.com/archive.zip
    """
    a, *b = a.split("::")
    if is_local_path(a):
        a = Path(a, *p).as_posix()
    else:
        a = posixpath.join(a, *p)
    return "::".join([a] + b)


def _add_retries_to_file_obj_read_method(file_obj):
    read = file_obj.read
    max_retries = config.STREAMING_READ_MAX_RETRIES

    def read_with_retries(*args, **kwargs):
        for retry in range(1, max_retries + 1):
            try:
                out = read(*args, **kwargs)
                break
            except ClientError:
                logger.warning(
                    f"Got diconnected from remote data host. Retrying in {config.STREAMING_READ_RETRY_INTERVAL}sec [{retry}/{max_retries}]"
                )
                time.sleep(config.STREAMING_READ_RETRY_INTERVAL)
        else:
            raise ConnectionError("Server Disconnected")
        return out

    file_obj.read = read_with_retries


def xopen(file, mode="r", *args, **kwargs):
    """
    This function extends the builtin `open` function to support remote files using fsspec.

    It also has a retry mechanism in case connection fails.
    The args and kwargs are passed to fsspec.open, except `use_auth_token` which is used for queries to private repos on huggingface.co
    """
    if fsspec.get_fs_token_paths(file)[0].protocol == "https":
        kwargs["headers"] = get_authentication_headers_for_url(file, use_auth_token=kwargs.pop("use_auth_token", None))
    file_obj = fsspec.open(file, mode=mode, *args, **kwargs).open()
    _add_retries_to_file_obj_read_method(file_obj)
    return file_obj


class StreamingDownloadManager(object):
    """
    Download manager that uses the "::" separator to naviguate through (possibly remote) compressed archives.
    Contrary to the regular DownloadManager, the `download` and `extract` methods don't actually download nor extract
    data, but they rather return the path or url that could be opened using the `xopen` function which extends the
    builtin `open` function to stream data from remote files.
    """

    def __init__(
        self,
        dataset_name: Optional[str] = None,
        data_dir: Optional[str] = None,
        download_config: Optional[DownloadConfig] = None,
        base_path: Optional[str] = None,
    ):
        self._dataset_name = dataset_name
        self._data_dir = data_dir
        self._download_config = download_config or DownloadConfig()
        self._base_path = base_path or os.path.abspath(".")

    @property
    def manual_dir(self):
        return self._data_dir

    def download(self, url_or_urls):
        url_or_urls = map_nested(self._download, url_or_urls, map_tuple=True)
        return url_or_urls

    def _download(self, url_or_filename):
        if is_relative_path(url_or_filename):
            # append the relative path to the base_path
            url_or_filename = url_or_path_join(self._base_path, url_or_filename)
        return url_or_filename

    def extract(self, path_or_paths):
        urlpaths = map_nested(self._extract, path_or_paths, map_tuple=True)
        return urlpaths

    def _extract(self, urlpath):
        protocol = self._get_extraction_protocol(urlpath)
        if protocol is None:
            # no extraction
            return urlpath
        elif protocol == "gzip":
            # there is one single file which is the uncompressed gzip file
            return f"{protocol}://{os.path.basename(urlpath.split('::')[0]).rstrip('.gz')}::{urlpath}"
        else:
            return f"{protocol}://::{urlpath}"

    def _get_extraction_protocol(self, urlpath) -> Optional[str]:
        path = urlpath.split("::")[0]
        if path.split(".")[-1] in BASE_KNOWN_EXTENSIONS:
            return None
        elif path.endswith(".gz") and not path.endswith(".tar.gz"):
            return "gzip"
        elif path.endswith(".zip"):
            return "zip"
        raise NotImplementedError(f"Extraction protocol for file at {urlpath} is not implemented yet")

    def download_and_extract(self, url_or_urls):
        return self.extract(self.download(url_or_urls))
