import glob
import os
import re
import time
from pathlib import Path, PurePosixPath
from typing import Optional, Tuple, Union

import fsspec
import posixpath
from aiohttp.client_exceptions import ClientError
from fsspec.exceptions import FSTimeoutError

from .. import config
from ..filesystems import COMPRESSION_FILESYSTEMS
from .download_manager import DownloadConfig, map_nested
from .file_utils import get_authentication_headers_for_url, is_local_path, is_relative_path, url_or_path_join
from .logging import get_logger


logger = get_logger(__name__)

BASE_KNOWN_EXTENSIONS = ["txt", "csv", "json", "jsonl", "tsv", "conll", "conllu", "parquet", "pkl", "pickle", "xml"]
COMPRESSION_EXTENSION_TO_PROTOCOL = {
    # single file compression
    **{fs_class.extension.lstrip("."): fs_class.protocol for fs_class in COMPRESSION_FILESYSTEMS},
    # archive compression
    "zip": "zip",
    "tar": "tar",
    "tgz": "tar",
}
SINGLE_FILE_COMPRESSION_PROTOCOLS = {fs_class.protocol for fs_class in COMPRESSION_FILESYSTEMS}
SINGLE_SLASH_AFTER_PROTOCOL_PATTERN = re.compile(r"(?<!:):/")


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


def xdirname(a):
    """
    This function extends os.path.dirname to support the "::" hop separator. It supports both paths and urls.

    A shorthand, particularly useful where you have multiple hops, is to “chain” the URLs with the special separator "::".
    This is used to access files inside a zip file over http for example.

    Let's say you have a zip file at https://host.com/archive.zip, and you want to access the file inside the zip file at /folder1/file.txt.
    Then you can just chain the url this way:

        zip://folder1/file.txt::https://host.com/archive.zip

    The xdirname function allows you to apply the dirname on the first path of the chain.

    Example::

        >>> xdirname("zip://folder1/file.txt::https://host.com/archive.zip")
        zip://folder1::https://host.com/archive.zip
    """
    a, *b = a.split("::")
    if is_local_path(a):
        a = os.path.dirname(Path(a).as_posix())
    else:
        a = posixpath.dirname(a)
    # if we end up at the root of the protocol, we get for example a = 'http:'
    # so we have to fix it by adding the '//' that was removed:
    if a.endswith(":"):
        a += "//"
    return "::".join([a] + b)


def _as_posix(path: Path):
    """Extend :meth:`pathlib.PurePath.as_posix` to fix missing slashes after protocol.

    Args:
        path (:obj:`~pathlib.Path`): Calling Path instance.

    Returns:
        obj:`str`
    """
    path_as_posix = path.as_posix()
    path_as_posix = SINGLE_SLASH_AFTER_PROTOCOL_PATTERN.sub("://", path_as_posix)
    path_as_posix += "//" if path_as_posix.endswith(":") else ""  # Add slashes to root of the protocol
    return path_as_posix


def xpathjoin(a: Path, *p: Tuple[str, ...]):
    """Extend :func:`xjoin` to support argument of type :obj:`~pathlib.Path`.

    Args:
        a (:obj:`~pathlib.Path`): Calling Path instance.
        *p (:obj:`tuple` of :obj:`str`): Other path components.

    Returns:
        obj:`str`
    """
    return type(a)(xjoin(_as_posix(a), *p))


def _add_retries_to_file_obj_read_method(file_obj):
    read = file_obj.read
    max_retries = config.STREAMING_READ_MAX_RETRIES

    def read_with_retries(*args, **kwargs):
        for retry in range(1, max_retries + 1):
            try:
                out = read(*args, **kwargs)
                break
            except (ClientError, FSTimeoutError):
                logger.warning(
                    f"Got disconnected from remote data host. Retrying in {config.STREAMING_READ_RETRY_INTERVAL}sec [{retry}/{max_retries}]"
                )
                time.sleep(config.STREAMING_READ_RETRY_INTERVAL)
        else:
            raise ConnectionError("Server Disconnected")
        return out

    file_obj.read = read_with_retries


def _get_extraction_protocol(urlpath: str) -> Optional[str]:
    # get inner file: zip://train-00000.json.gz::https://foo.bar/data.zip -> zip://train-00000.json.gz
    path = urlpath.split("::")[0]
    # Get extension: https://foo.bar/train.json.gz -> gz
    extension = path.split(".")[-1]
    # Remove query params ("dl=1", "raw=true"): gz?dl=1 -> gz
    extension = extension.split("?")[0]
    if extension in BASE_KNOWN_EXTENSIONS:
        return None
    elif path.endswith(".tar.gz") or path.endswith(".tgz"):
        pass
    elif extension in COMPRESSION_EXTENSION_TO_PROTOCOL:
        return COMPRESSION_EXTENSION_TO_PROTOCOL[extension]
    raise NotImplementedError(f"Extraction protocol '{extension}' for file at '{urlpath}' is not implemented yet")


def xopen(file, mode="r", *args, use_auth_token: Optional[Union[str, bool]] = None, **kwargs):
    """
    This function extends the builtin `open` function to support remote files using fsspec.

    It also has a retry mechanism in case connection fails.
    The args and kwargs are passed to fsspec.open, except `use_auth_token` which is used for queries to private repos on huggingface.co
    """
    if fsspec.get_fs_token_paths(file)[0].protocol == "https":
        kwargs["headers"] = get_authentication_headers_for_url(file, use_auth_token=use_auth_token)
    file_obj = fsspec.open(file, mode=mode, *args, **kwargs).open()
    _add_retries_to_file_obj_read_method(file_obj)
    return file_obj


def xpathopen(path: Path, *args, **kwargs):
    """Extend :func:`xopen` to support argument of type :obj:`~pathlib.Path`.

    Args:
        path (:obj:`~pathlib.Path`): Calling Path instance.
        **kwargs: Keyword arguments passed to :func:`fsspec.open`.

    Returns:
        :obj:`io.FileIO`: File-like object.
    """
    return xopen(_as_posix(path), *args, **kwargs)


def xglob(urlpath, *, recursive=False, use_auth_token: Optional[Union[str, bool]] = None):
    """Extend `glob.glob` function to support remote files.

    Args:
        urlpath (:obj:`str`): URL path with shell-style wildcard patterns.
        recursive (:obj:`bool`, default `False`): Whether to match the "**" pattern recursively to zero or more
            directories or subdirectories.

    Returns:
        :obj:`list` of :obj:`str`
    """
    main_hop, *rest_hops = urlpath.split("::")
    if is_local_path(main_hop):
        return glob.glob(main_hop, recursive=recursive)
    else:
        # globbing inside a zip in a private repo requires authentication
        if rest_hops and fsspec.get_fs_token_paths(rest_hops[0])[0].protocol == "https":
            storage_options = {
                "https": {"headers": get_authentication_headers_for_url(rest_hops[0], use_auth_token=use_auth_token)}
            }
        else:
            storage_options = None
        fs, *_ = fsspec.get_fs_token_paths(urlpath, storage_options=storage_options)
        # - If there's no "*" in the pattern, get_fs_token_paths() doesn't do any pattern matching
        #   so to be able to glob patterns like "[0-9]", we have to call `fs.glob`.
        # - Also "*" in get_fs_token_paths() only matches files: we have to call `fs.glob` to match directories.
        # - If there is "**" in the pattern, `fs.glob` must be called anyway.
        globbed_paths = fs.glob(main_hop)
        return ["::".join([f"{fs.protocol}://{globbed_path}"] + rest_hops) for globbed_path in globbed_paths]


def xpathglob(path, pattern, use_auth_token: Optional[Union[str, bool]] = None):
    """Glob function for argument of type :obj:`~pathlib.Path` that supports both local paths end remote URLs.

    Args:
        path (:obj:`~pathlib.Path`): Calling Path instance.
        pattern (:obj:`str`): Pattern that resulting paths must match.

    Yields:
        :obj:`~pathlib.Path`
    """
    posix_path = _as_posix(path)
    main_hop, *rest_hops = posix_path.split("::")
    if is_local_path(main_hop):
        yield from Path(main_hop).glob(pattern)
    else:
        # globbing inside a zip in a private repo requires authentication
        if rest_hops and fsspec.get_fs_token_paths(rest_hops[0])[0].protocol == "https":
            storage_options = {
                "headers": get_authentication_headers_for_url(rest_hops[0], use_auth_token=use_auth_token)
            }
        else:
            storage_options = None
        fs, *_ = fsspec.get_fs_token_paths(xjoin(posix_path, pattern), storage_options=storage_options)
        # - If there's no "*" in the pattern, get_fs_token_paths() doesn't do any pattern matching
        #   so to be able to glob patterns like "[0-9]", we have to call `fs.glob`.
        # - Also "*" in get_fs_token_paths() only matches files: we have to call `fs.glob` to match directories.
        # - If there is "**" in the pattern, `fs.glob` must be called anyway.
        globbed_paths = fs.glob(xjoin(main_hop, pattern))
        for globbed_path in globbed_paths:
            yield type(path)("::".join([f"{fs.protocol}://{globbed_path}"] + rest_hops))


def xpathrglob(path, pattern, **kwargs):
    """Rglob function for argument of type :obj:`~pathlib.Path` that supports both local paths end remote URLs.

    Args:
        path (:obj:`~pathlib.Path`): Calling Path instance.
        pattern (:obj:`str`): Pattern that resulting paths must match.

    Yields:
        :obj:`~pathlib.Path`
    """
    return xpathglob(path, "**/" + pattern, **kwargs)


def xpathstem(path: Path):
    """Stem function for argument of type :obj:`~pathlib.Path` that supports both local paths end remote URLs.

    Args:
        path (:obj:`~pathlib.Path`): Calling Path instance.

    Returns:
        :obj:`str`
    """
    return PurePosixPath(_as_posix(path).split("::")[0]).stem


def xpathsuffix(path: Path):
    """Suffix function for argument of type :obj:`~pathlib.Path` that supports both local paths end remote URLs.

    Args:
        path (:obj:`~pathlib.Path`): Calling Path instance.

    Returns:
        :obj:`str`
    """
    return PurePosixPath(_as_posix(path).split("::")[0]).suffix


def xpandas_read_csv(path, use_auth_token: Optional[Union[str, bool]] = None, **kwargs):
    import pandas as pd

    return pd.read_csv(xopen(path, use_auth_token=use_auth_token), **kwargs)


class StreamingDownloadManager(object):
    """
    Download manager that uses the "::" separator to navigate through (possibly remote) compressed archives.
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

    def _download(self, urlpath: str) -> str:
        urlpath = str(urlpath)
        if is_relative_path(urlpath):
            # append the relative path to the base_path
            urlpath = url_or_path_join(self._base_path, urlpath)
        return urlpath

    def extract(self, path_or_paths):
        urlpaths = map_nested(self._extract, path_or_paths, map_tuple=True)
        return urlpaths

    def _extract(self, urlpath: str) -> str:
        urlpath = str(urlpath)
        protocol = _get_extraction_protocol(urlpath)
        if protocol is None:
            # no extraction
            return urlpath
        elif protocol in SINGLE_FILE_COMPRESSION_PROTOCOLS:
            # there is one single file which is the uncompressed file
            inner_file = os.path.basename(urlpath.split("::")[0])
            inner_file = inner_file[: inner_file.rindex(".")]
            # check for tar.gz, tar.bz2 etc.
            if inner_file.endswith(".tar"):
                return f"tar://::{urlpath}"
            else:
                return f"{protocol}://{inner_file}::{urlpath}"
        else:
            return f"{protocol}://::{urlpath}"

    def download_and_extract(self, url_or_urls):
        return self.extract(self.download(url_or_urls))
