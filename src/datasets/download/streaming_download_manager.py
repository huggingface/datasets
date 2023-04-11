import glob
import io
import os
import posixpath
import re
import tarfile
import time
import xml.dom.minidom
import zipfile
from asyncio import TimeoutError
from io import BytesIO
from itertools import chain
from pathlib import Path, PurePosixPath
from typing import Callable, Generator, Iterable, List, Optional, Tuple, Union
from xml.etree import ElementTree as ET

import fsspec
from aiohttp.client_exceptions import ClientError

from .. import config
from ..filesystems import COMPRESSION_FILESYSTEMS
from ..utils.file_utils import (
    get_authentication_headers_for_url,
    http_head,
    is_local_path,
    is_relative_path,
    is_remote_url,
    url_or_path_join,
)
from ..utils.logging import get_logger
from ..utils.py_utils import map_nested
from .download_config import DownloadConfig


logger = get_logger(__name__)

BASE_KNOWN_EXTENSIONS = [
    "txt",
    "csv",
    "json",
    "jsonl",
    "tsv",
    "conll",
    "conllu",
    "orig",
    "parquet",
    "pkl",
    "pickle",
    "rel",
    "xml",
]
COMPRESSION_EXTENSION_TO_PROTOCOL = {
    # single file compression
    **{fs_class.extension.lstrip("."): fs_class.protocol for fs_class in COMPRESSION_FILESYSTEMS},
    # archive compression
    "zip": "zip",
}
SINGLE_FILE_COMPRESSION_PROTOCOLS = {fs_class.protocol for fs_class in COMPRESSION_FILESYSTEMS}
SINGLE_SLASH_AFTER_PROTOCOL_PATTERN = re.compile(r"(?<!:):/")


MAGIC_NUMBER_TO_COMPRESSION_PROTOCOL = {
    bytes.fromhex("504B0304"): "zip",
    bytes.fromhex("504B0506"): "zip",  # empty archive
    bytes.fromhex("504B0708"): "zip",  # spanned archive
    bytes.fromhex("425A68"): "bz2",
    bytes.fromhex("1F8B"): "gzip",
    bytes.fromhex("FD377A585A00"): "xz",
    bytes.fromhex("04224D18"): "lz4",
    bytes.fromhex("28B52FFD"): "zstd",
}
MAGIC_NUMBER_TO_UNSUPPORTED_COMPRESSION_PROTOCOL = {
    b"Rar!": "rar",
}
MAGIC_NUMBER_MAX_LENGTH = max(
    len(magic_number)
    for magic_number in chain(MAGIC_NUMBER_TO_COMPRESSION_PROTOCOL, MAGIC_NUMBER_TO_UNSUPPORTED_COMPRESSION_PROTOCOL)
)


class NonStreamableDatasetError(Exception):
    pass


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
    a, *b = str(a).split("::")
    if is_local_path(a):
        return os.path.join(a, *p)
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
    a, *b = str(a).split("::")
    if is_local_path(a):
        a = os.path.dirname(Path(a).as_posix())
    else:
        a = posixpath.dirname(a)
    # if we end up at the root of the protocol, we get for example a = 'http:'
    # so we have to fix it by adding the '//' that was removed:
    if a.endswith(":"):
        a += "//"
    return "::".join([a] + b)


def xexists(urlpath: str, use_auth_token: Optional[Union[str, bool]] = None):
    """Extend `os.path.exists` function to support both local and remote files.

    Args:
        urlpath (`str`): URL path.
        use_auth_token (`bool` or `str`, *optional*): Whether to use token or token to authenticate on the
            Hugging Face Hub for private remote files.

    Returns:
        `bool`
    """

    main_hop, *rest_hops = _as_str(urlpath).split("::")
    if is_local_path(main_hop):
        return os.path.exists(main_hop)
    else:
        if not rest_hops and (main_hop.startswith("http://") or main_hop.startswith("https://")):
            main_hop, http_kwargs = _prepare_http_url_kwargs(main_hop, use_auth_token=use_auth_token)
            storage_options = http_kwargs
        elif rest_hops and (rest_hops[0].startswith("http://") or rest_hops[0].startswith("https://")):
            url = rest_hops[0]
            url, http_kwargs = _prepare_http_url_kwargs(url, use_auth_token=use_auth_token)
            storage_options = {"https": http_kwargs}
            urlpath = "::".join([main_hop, url, *rest_hops[1:]])
        else:
            storage_options = None
        fs, *_ = fsspec.get_fs_token_paths(urlpath, storage_options=storage_options)
        return fs.exists(main_hop)


def xbasename(a):
    """
    This function extends os.path.basename to support the "::" hop separator. It supports both paths and urls.

    A shorthand, particularly useful where you have multiple hops, is to “chain” the URLs with the special separator "::".
    This is used to access files inside a zip file over http for example.

    Let's say you have a zip file at https://host.com/archive.zip, and you want to access the file inside the zip file at /folder1/file.txt.
    Then you can just chain the url this way:

        zip://folder1/file.txt::https://host.com/archive.zip

    The xbasename function allows you to apply the basename on the first path of the chain.

    Example::

        >>> xbasename("zip://folder1/file.txt::https://host.com/archive.zip")
        file.txt
    """
    a, *b = str(a).split("::")
    if is_local_path(a):
        return os.path.basename(Path(a).as_posix())
    else:
        return posixpath.basename(a)


def xsplit(a):
    """
    This function extends os.path.split to support the "::" hop separator. It supports both paths and urls.

    A shorthand, particularly useful where you have multiple hops, is to “chain” the URLs with the special separator "::".
    This is used to access files inside a zip file over http for example.

    Let's say you have a zip file at https://host.com/archive.zip, and you want to access the file inside the zip file at /folder1/file.txt.
    Then you can just chain the url this way:

        zip://folder1/file.txt::https://host.com/archive.zip

    The xsplit function allows you to apply the xsplit on the first path of the chain.

    Example::

        >>> xsplit("zip://folder1/file.txt::https://host.com/archive.zip")
        ('zip://folder1::https://host.com/archive.zip', 'file.txt')
    """
    a, *b = str(a).split("::")
    if is_local_path(a):
        return os.path.split(Path(a).as_posix())
    else:
        a, tail = posixpath.split(a)
        return "::".join([a + "//" if a.endswith(":") else a] + b), tail


def xsplitext(a):
    """
    This function extends os.path.splitext to support the "::" hop separator. It supports both paths and urls.

    A shorthand, particularly useful where you have multiple hops, is to “chain” the URLs with the special separator "::".
    This is used to access files inside a zip file over http for example.

    Let's say you have a zip file at https://host.com/archive.zip, and you want to access the file inside the zip file at /folder1/file.txt.
    Then you can just chain the url this way:

        zip://folder1/file.txt::https://host.com/archive.zip

    The xsplitext function allows you to apply the splitext on the first path of the chain.

    Example::

        >>> xsplitext("zip://folder1/file.txt::https://host.com/archive.zip")
        ('zip://folder1/file::https://host.com/archive.zip', '.txt')
    """
    a, *b = str(a).split("::")
    if is_local_path(a):
        return os.path.splitext(Path(a).as_posix())
    else:
        a, ext = posixpath.splitext(a)
        return "::".join([a] + b), ext


def xisfile(path, use_auth_token: Optional[Union[str, bool]] = None) -> bool:
    """Extend `os.path.isfile` function to support remote files.

    Args:
        path (`str`): URL path.
        use_auth_token (`bool` or `str`, *optional*): Whether to use token or token to authenticate on the
            Hugging Face Hub for private remote files.

    Returns:
        `bool`
    """
    main_hop, *rest_hops = str(path).split("::")
    if is_local_path(main_hop):
        return os.path.isfile(path)
    else:
        if not rest_hops and (main_hop.startswith("http://") or main_hop.startswith("https://")):
            main_hop, http_kwargs = _prepare_http_url_kwargs(main_hop, use_auth_token=use_auth_token)
            storage_options = http_kwargs
        elif rest_hops and (rest_hops[0].startswith("http://") or rest_hops[0].startswith("https://")):
            url = rest_hops[0]
            url, http_kwargs = _prepare_http_url_kwargs(url, use_auth_token=use_auth_token)
            storage_options = {"https": http_kwargs}
            path = "::".join([main_hop, url, *rest_hops[1:]])
        else:
            storage_options = None
        fs, *_ = fsspec.get_fs_token_paths(path, storage_options=storage_options)
        return fs.isfile(main_hop)


def xgetsize(path, use_auth_token: Optional[Union[str, bool]] = None) -> int:
    """Extend `os.path.getsize` function to support remote files.

    Args:
        path (`str`): URL path.
        use_auth_token (`bool` or `str`, *optional*): Whether to use token or token to authenticate on the
            Hugging Face Hub for private remote files.

    Returns:
        `int`: optional
    """
    main_hop, *rest_hops = str(path).split("::")
    if is_local_path(main_hop):
        return os.path.getsize(path)
    else:
        if not rest_hops and (main_hop.startswith("http://") or main_hop.startswith("https://")):
            main_hop, http_kwargs = _prepare_http_url_kwargs(main_hop, use_auth_token=use_auth_token)
            storage_options = http_kwargs
        elif rest_hops and (rest_hops[0].startswith("http://") or rest_hops[0].startswith("https://")):
            url = rest_hops[0]
            url, http_kwargs = _prepare_http_url_kwargs(url, use_auth_token=use_auth_token)
            storage_options = {"https": http_kwargs}
            path = "::".join([main_hop, url, *rest_hops[1:]])
        else:
            storage_options = None
        fs, *_ = fsspec.get_fs_token_paths(path, storage_options=storage_options)
        size = fs.size(main_hop)
        if size is None:
            # use xopen instead of fs.open to make data fetching more robust
            with xopen(path, use_auth_token=use_auth_token) as f:
                size = len(f.read())
        return size


def xisdir(path, use_auth_token: Optional[Union[str, bool]] = None) -> bool:
    """Extend `os.path.isdir` function to support remote files.

    Args:
        path (`str`): URL path.
        use_auth_token (`bool` or `str`, *optional*): Whether to use token or token to authenticate on the
            Hugging Face Hub for private remote files.

    Returns:
        `bool`
    """
    main_hop, *rest_hops = str(path).split("::")
    if is_local_path(main_hop):
        return os.path.isdir(path)
    else:
        if not rest_hops and (main_hop.startswith("http://") or main_hop.startswith("https://")):
            raise NotImplementedError("os.path.isdir is not extended to support URLs in streaming mode")
        elif rest_hops and (rest_hops[0].startswith("http://") or rest_hops[0].startswith("https://")):
            url = rest_hops[0]
            url, http_kwargs = _prepare_http_url_kwargs(url, use_auth_token=use_auth_token)
            storage_options = {"https": http_kwargs}
            path = "::".join([main_hop, url, *rest_hops[1:]])
        else:
            storage_options = None
        fs, *_ = fsspec.get_fs_token_paths(path, storage_options=storage_options)
        inner_path = main_hop.split("://")[1]
        if not inner_path.strip("/"):
            return True
        return fs.isdir(inner_path)


def xrelpath(path, start=None):
    """Extend `os.path.relpath` function to support remote files.

    Args:
        path (`str`): URL path.
        start (`str`): Start URL directory path.

    Returns:
        `str`
    """
    main_hop, *rest_hops = str(path).split("::")
    if is_local_path(main_hop):
        return os.path.relpath(main_hop, start=start) if start else os.path.relpath(main_hop)
    else:
        return posixpath.relpath(main_hop, start=str(start).split("::")[0]) if start else os.path.relpath(main_hop)


def _add_retries_to_file_obj_read_method(file_obj):
    read = file_obj.read
    max_retries = config.STREAMING_READ_MAX_RETRIES

    def read_with_retries(*args, **kwargs):
        disconnect_err = None
        for retry in range(1, max_retries + 1):
            try:
                out = read(*args, **kwargs)
                break
            except (ClientError, TimeoutError) as err:
                disconnect_err = err
                logger.warning(
                    f"Got disconnected from remote data host. Retrying in {config.STREAMING_READ_RETRY_INTERVAL}sec [{retry}/{max_retries}]"
                )
                time.sleep(config.STREAMING_READ_RETRY_INTERVAL)
        else:
            raise ConnectionError("Server Disconnected") from disconnect_err
        return out

    file_obj.read = read_with_retries


def _get_path_extension(path: str) -> str:
    # Get extension: https://foo.bar/train.json.gz -> gz
    extension = path.split(".")[-1]
    # Remove query params ("dl=1", "raw=true"): gz?dl=1 -> gz
    # Remove shards infos (".txt_1", ".txt-00000-of-00100"): txt_1 -> txt
    for symb in "?-_":
        extension = extension.split(symb)[0]
    return extension


def _get_extraction_protocol_with_magic_number(f) -> Optional[str]:
    """read the magic number from a file-like object and return the compression protocol"""
    # Check if the file object is seekable even before reading the magic number (to avoid https://bugs.python.org/issue26440)
    try:
        f.seek(0)
    except (AttributeError, io.UnsupportedOperation):
        return None
    magic_number = f.read(MAGIC_NUMBER_MAX_LENGTH)
    f.seek(0)
    for i in range(MAGIC_NUMBER_MAX_LENGTH):
        compression = MAGIC_NUMBER_TO_COMPRESSION_PROTOCOL.get(magic_number[: MAGIC_NUMBER_MAX_LENGTH - i])
        if compression is not None:
            return compression
        compression = MAGIC_NUMBER_TO_UNSUPPORTED_COMPRESSION_PROTOCOL.get(magic_number[: MAGIC_NUMBER_MAX_LENGTH - i])
        if compression is not None:
            raise NotImplementedError(f"Compression protocol '{compression}' not implemented.")


def _get_extraction_protocol(urlpath: str, use_auth_token: Optional[Union[str, bool]] = None) -> Optional[str]:
    # get inner file: zip://train-00000.json.gz::https://foo.bar/data.zip -> zip://train-00000.json.gz
    urlpath = str(urlpath)
    path = urlpath.split("::")[0]
    extension = _get_path_extension(path)
    if (
        extension in BASE_KNOWN_EXTENSIONS
        or extension in ["tgz", "tar"]
        or path.endswith((".tar.gz", ".tar.bz2", ".tar.xz"))
    ):
        return None
    elif extension in COMPRESSION_EXTENSION_TO_PROTOCOL:
        return COMPRESSION_EXTENSION_TO_PROTOCOL[extension]
    if is_remote_url(urlpath):
        # get headers and cookies for authentication on the HF Hub and for Google Drive
        urlpath, kwargs = _prepare_http_url_kwargs(urlpath, use_auth_token=use_auth_token)
    else:
        urlpath, kwargs = urlpath, {}
    with fsspec.open(urlpath, **kwargs) as f:
        return _get_extraction_protocol_with_magic_number(f)


def _prepare_http_url_kwargs(url: str, use_auth_token: Optional[Union[str, bool]] = None) -> Tuple[str, dict]:
    """
    Prepare the URL and the kwargs that must be passed to the HttpFileSystem or to requests.get/head

    In particular it resolves google drive URLs and it adds the authentication headers for the Hugging Face Hub.
    """
    kwargs = {
        "headers": get_authentication_headers_for_url(url, use_auth_token=use_auth_token),
        "client_kwargs": {"trust_env": True},  # Enable reading proxy env variables.
    }
    if "drive.google.com" in url:
        response = http_head(url)
        cookies = None
        for k, v in response.cookies.items():
            if k.startswith("download_warning"):
                url += "&confirm=" + v
                cookies = response.cookies
                kwargs["cookies"] = cookies
    # Fix Google Drive URL to avoid Virus scan warning
    if "drive.google.com" in url and "confirm=" not in url:
        url += "&confirm=t"
    if url.startswith("https://raw.githubusercontent.com/"):
        # Workaround for served data with gzip content-encoding: https://github.com/fsspec/filesystem_spec/issues/389
        kwargs["block_size"] = 0
    return url, kwargs


def xopen(file: str, mode="r", *args, use_auth_token: Optional[Union[str, bool]] = None, **kwargs):
    """Extend `open` function to support remote files using `fsspec`.

    It also has a retry mechanism in case connection fails.
    The `args` and `kwargs` are passed to `fsspec.open`, except `use_auth_token` which is used for queries to private repos on huggingface.co

    Args:
        file (`str`): Path name of the file to be opened.
        mode (`str`, *optional*, default "r"): Mode in which the file is opened.
        *args: Arguments to be passed to `fsspec.open`.
        use_auth_token (`bool` or `str`, *optional*): Whether to use token or token to authenticate on the
            Hugging Face Hub for private remote files.
        **kwargs: Keyword arguments to be passed to `fsspec.open`.

    Returns:
        file object
    """
    # This works as well for `xopen(str(Path(...)))`
    file_str = _as_str(file)
    main_hop, *rest_hops = file_str.split("::")
    if is_local_path(main_hop):
        return open(main_hop, mode, *args, **kwargs)
    # add headers and cookies for authentication on the HF Hub and for Google Drive
    if not rest_hops and (main_hop.startswith("http://") or main_hop.startswith("https://")):
        file, new_kwargs = _prepare_http_url_kwargs(file_str, use_auth_token=use_auth_token)
    elif rest_hops and (rest_hops[0].startswith("http://") or rest_hops[0].startswith("https://")):
        url = rest_hops[0]
        url, http_kwargs = _prepare_http_url_kwargs(url, use_auth_token=use_auth_token)
        new_kwargs = {"https": http_kwargs}
        file = "::".join([main_hop, url, *rest_hops[1:]])
    else:
        new_kwargs = {}
    kwargs = {**kwargs, **new_kwargs}
    try:
        file_obj = fsspec.open(file, mode=mode, *args, **kwargs).open()
    except ValueError as e:
        if str(e) == "Cannot seek streaming HTTP file":
            raise NonStreamableDatasetError(
                "Streaming is not possible for this dataset because data host server doesn't support HTTP range "
                "requests. You can still load this dataset in non-streaming mode by passing `streaming=False` (default)"
            ) from e
        else:
            raise
    _add_retries_to_file_obj_read_method(file_obj)
    return file_obj


def xlistdir(path: str, use_auth_token: Optional[Union[str, bool]] = None) -> List[str]:
    """Extend `os.listdir` function to support remote files.

    Args:
        path (`str`): URL path.
        use_auth_token (`bool` or `str`, *optional*): Whether to use token or token to authenticate on the
            Hugging Face Hub for private remote files.

    Returns:
        `list` of `str`
    """
    main_hop, *rest_hops = _as_str(path).split("::")
    if is_local_path(main_hop):
        return os.listdir(path)
    else:
        # globbing inside a zip in a private repo requires authentication
        if not rest_hops and (main_hop.startswith("http://") or main_hop.startswith("https://")):
            raise NotImplementedError("os.listdir is not extended to support URLs in streaming mode")
        elif rest_hops and (rest_hops[0].startswith("http://") or rest_hops[0].startswith("https://")):
            url = rest_hops[0]
            url, http_kwargs = _prepare_http_url_kwargs(url, use_auth_token=use_auth_token)
            storage_options = {"https": http_kwargs}
            path = "::".join([main_hop, url, *rest_hops[1:]])
        else:
            storage_options = None
        fs, *_ = fsspec.get_fs_token_paths(path, storage_options=storage_options)
        inner_path = main_hop.split("://")[1]
        if inner_path.strip("/") and not fs.isdir(inner_path):
            raise FileNotFoundError(f"Directory doesn't exist: {path}")
        objects = fs.listdir(inner_path)
        return [os.path.basename(obj["name"]) for obj in objects]


def xglob(urlpath, *, recursive=False, use_auth_token: Optional[Union[str, bool]] = None):
    """Extend `glob.glob` function to support remote files.

    Args:
        urlpath (`str`): URL path with shell-style wildcard patterns.
        recursive (`bool`, default `False`): Whether to match the "**" pattern recursively to zero or more
            directories or subdirectories.
        use_auth_token (`bool` or `str`, *optional*): Whether to use token or token to authenticate on the
            Hugging Face Hub for private remote files.

    Returns:
        `list` of `str`
    """
    main_hop, *rest_hops = _as_str(urlpath).split("::")
    if is_local_path(main_hop):
        return glob.glob(main_hop, recursive=recursive)
    else:
        # globbing inside a zip in a private repo requires authentication
        if not rest_hops and (main_hop.startswith("http://") or main_hop.startswith("https://")):
            raise NotImplementedError("glob.glob is not extended to support URLs in streaming mode")
        elif rest_hops and (rest_hops[0].startswith("http://") or rest_hops[0].startswith("https://")):
            url = rest_hops[0]
            url, kwargs = _prepare_http_url_kwargs(url, use_auth_token=use_auth_token)
            storage_options = {"https": kwargs}
            urlpath = "::".join([main_hop, url, *rest_hops[1:]])
        else:
            storage_options = None
        fs, *_ = fsspec.get_fs_token_paths(urlpath, storage_options=storage_options)
        # - If there's no "*" in the pattern, get_fs_token_paths() doesn't do any pattern matching
        #   so to be able to glob patterns like "[0-9]", we have to call `fs.glob`.
        # - Also "*" in get_fs_token_paths() only matches files: we have to call `fs.glob` to match directories.
        # - If there is "**" in the pattern, `fs.glob` must be called anyway.
        inner_path = main_hop.split("://")[1]
        globbed_paths = fs.glob(inner_path)
        protocol = fs.protocol if isinstance(fs.protocol, str) else fs.protocol[-1]
        return ["::".join([f"{protocol}://{globbed_path}"] + rest_hops) for globbed_path in globbed_paths]


def xwalk(urlpath, use_auth_token: Optional[Union[str, bool]] = None, **kwargs):
    """Extend `os.walk` function to support remote files.

    Args:
        urlpath (`str`): URL root path.
        use_auth_token (`bool` or `str`, *optional*): Whether to use token or token to authenticate on the
            Hugging Face Hub for private remote files.
        **kwargs: Additional keyword arguments forwarded to the underlying filesystem.


    Yields:
        `tuple`: 3-tuple (dirpath, dirnames, filenames).
    """
    main_hop, *rest_hops = _as_str(urlpath).split("::")
    if is_local_path(main_hop):
        yield from os.walk(main_hop, **kwargs)
    else:
        # walking inside a zip in a private repo requires authentication
        if not rest_hops and (main_hop.startswith("http://") or main_hop.startswith("https://")):
            raise NotImplementedError("os.walk is not extended to support URLs in streaming mode")
        elif rest_hops and (rest_hops[0].startswith("http://") or rest_hops[0].startswith("https://")):
            url = rest_hops[0]
            url, kwargs = _prepare_http_url_kwargs(url, use_auth_token=use_auth_token)
            storage_options = {"https": kwargs}
            urlpath = "::".join([main_hop, url, *rest_hops[1:]])
        else:
            storage_options = None
        fs, *_ = fsspec.get_fs_token_paths(urlpath, storage_options=storage_options)
        inner_path = main_hop.split("://")[1]
        if inner_path.strip("/") and not fs.isdir(inner_path):
            return []
        protocol = fs.protocol if isinstance(fs.protocol, str) else fs.protocol[-1]
        for dirpath, dirnames, filenames in fs.walk(inner_path, **kwargs):
            yield "::".join([f"{protocol}://{dirpath}"] + rest_hops), dirnames, filenames


class xPath(type(Path())):
    """Extension of `pathlib.Path` to support both local paths and remote URLs."""

    def __str__(self):
        path_str = super().__str__()
        main_hop, *rest_hops = path_str.split("::")
        if is_local_path(main_hop):
            return main_hop
        path_as_posix = path_str.replace("\\", "/")
        path_as_posix = SINGLE_SLASH_AFTER_PROTOCOL_PATTERN.sub("://", path_as_posix)
        path_as_posix += "//" if path_as_posix.endswith(":") else ""  # Add slashes to root of the protocol
        return path_as_posix

    def exists(self, use_auth_token: Optional[Union[str, bool]] = None):
        """Extend `pathlib.Path.exists` method to support both local and remote files.

        Args:
            use_auth_token (`bool` or `str`, *optional*): Whether to use token or token to authenticate on the
                Hugging Face Hub for private remote files.

        Returns:
            `bool`
        """
        return xexists(str(self), use_auth_token=use_auth_token)

    def glob(self, pattern, use_auth_token: Optional[Union[str, bool]] = None):
        """Glob function for argument of type :obj:`~pathlib.Path` that supports both local paths end remote URLs.

        Args:
            pattern (`str`): Pattern that resulting paths must match.
            use_auth_token (`bool` or `str`, *optional*): Whether to use token or token to authenticate on the
                Hugging Face Hub for private remote files.

        Yields:
            [`xPath`]
        """
        posix_path = self.as_posix()
        main_hop, *rest_hops = posix_path.split("::")
        if is_local_path(main_hop):
            yield from Path(main_hop).glob(pattern)
        else:
            # globbing inside a zip in a private repo requires authentication
            if rest_hops and (rest_hops[0].startswith("http://") or rest_hops[0].startswith("https://")):
                url = rest_hops[0]
                url, kwargs = _prepare_http_url_kwargs(url, use_auth_token=use_auth_token)
                storage_options = {"https": kwargs}
                posix_path = "::".join([main_hop, url, *rest_hops[1:]])
            else:
                storage_options = None
            fs, *_ = fsspec.get_fs_token_paths(xjoin(posix_path, pattern), storage_options=storage_options)
            # - If there's no "*" in the pattern, get_fs_token_paths() doesn't do any pattern matching
            #   so to be able to glob patterns like "[0-9]", we have to call `fs.glob`.
            # - Also "*" in get_fs_token_paths() only matches files: we have to call `fs.glob` to match directories.
            # - If there is "**" in the pattern, `fs.glob` must be called anyway.
            globbed_paths = fs.glob(xjoin(main_hop, pattern))
            for globbed_path in globbed_paths:
                yield type(self)("::".join([f"{fs.protocol}://{globbed_path}"] + rest_hops))

    def rglob(self, pattern, **kwargs):
        """Rglob function for argument of type :obj:`~pathlib.Path` that supports both local paths end remote URLs.

        Args:
            pattern (`str`): Pattern that resulting paths must match.

        Yields:
            [`xPath`]
        """
        return self.glob("**/" + pattern, **kwargs)

    @property
    def parent(self) -> "xPath":
        """Name function for argument of type :obj:`~pathlib.Path` that supports both local paths end remote URLs.

        Returns:
            [`xPath`]
        """
        return type(self)(xdirname(self.as_posix()))

    @property
    def name(self) -> str:
        """Name function for argument of type :obj:`~pathlib.Path` that supports both local paths end remote URLs.

        Returns:
            `str`
        """
        return PurePosixPath(self.as_posix().split("::")[0]).name

    @property
    def stem(self) -> str:
        """Stem function for argument of type :obj:`~pathlib.Path` that supports both local paths end remote URLs.

        Returns:
            `str`
        """
        return PurePosixPath(self.as_posix().split("::")[0]).stem

    @property
    def suffix(self) -> str:
        """Suffix function for argument of type :obj:`~pathlib.Path` that supports both local paths end remote URLs.

        Returns:
            `str`
        """
        return PurePosixPath(self.as_posix().split("::")[0]).suffix

    def open(self, *args, **kwargs):
        """Extend :func:`xopen` to support argument of type :obj:`~pathlib.Path`.

        Args:
            **args: Arguments passed to :func:`fsspec.open`.
            **kwargs: Keyword arguments passed to :func:`fsspec.open`.

        Returns:
            `io.FileIO`: File-like object.
        """
        return xopen(str(self), *args, **kwargs)

    def joinpath(self, *p: Tuple[str, ...]) -> "xPath":
        """Extend :func:`xjoin` to support argument of type :obj:`~pathlib.Path`.

        Args:
            *p (`tuple` of `str`): Other path components.

        Returns:
            [`xPath`]
        """
        return type(self)(xjoin(self.as_posix(), *p))

    def __truediv__(self, p: str) -> "xPath":
        return self.joinpath(p)

    def with_suffix(self, suffix):
        main_hop, *rest_hops = str(self).split("::")
        if is_local_path(main_hop):
            return type(self)(str(super().with_suffix(suffix)))
        return type(self)("::".join([type(self)(PurePosixPath(main_hop).with_suffix(suffix)).as_posix()] + rest_hops))


def _as_str(path: Union[str, Path, xPath]):
    return str(path) if isinstance(path, xPath) else str(xPath(str(path)))


def xgzip_open(filepath_or_buffer, *args, use_auth_token: Optional[Union[str, bool]] = None, **kwargs):
    import gzip

    if hasattr(filepath_or_buffer, "read"):
        return gzip.open(filepath_or_buffer, *args, **kwargs)
    else:
        filepath_or_buffer = str(filepath_or_buffer)
        return gzip.open(xopen(filepath_or_buffer, "rb", use_auth_token=use_auth_token), *args, **kwargs)


def xnumpy_load(filepath_or_buffer, *args, use_auth_token: Optional[Union[str, bool]] = None, **kwargs):
    import numpy as np

    if hasattr(filepath_or_buffer, "read"):
        return np.load(filepath_or_buffer, *args, **kwargs)
    else:
        filepath_or_buffer = str(filepath_or_buffer)
        return np.load(xopen(filepath_or_buffer, "rb", use_auth_token=use_auth_token), *args, **kwargs)


def xpandas_read_csv(filepath_or_buffer, use_auth_token: Optional[Union[str, bool]] = None, **kwargs):
    import pandas as pd

    if hasattr(filepath_or_buffer, "read"):
        return pd.read_csv(filepath_or_buffer, **kwargs)
    else:
        filepath_or_buffer = str(filepath_or_buffer)
        if kwargs.get("compression", "infer") == "infer":
            kwargs["compression"] = _get_extraction_protocol(filepath_or_buffer, use_auth_token=use_auth_token)
        return pd.read_csv(xopen(filepath_or_buffer, "rb", use_auth_token=use_auth_token), **kwargs)


def xpandas_read_excel(filepath_or_buffer, use_auth_token: Optional[Union[str, bool]] = None, **kwargs):
    import pandas as pd

    if hasattr(filepath_or_buffer, "read"):
        try:
            return pd.read_excel(filepath_or_buffer, **kwargs)
        except ValueError:  # Cannot seek streaming HTTP file
            return pd.read_excel(BytesIO(filepath_or_buffer.read()), **kwargs)
    else:
        filepath_or_buffer = str(filepath_or_buffer)
        try:
            return pd.read_excel(xopen(filepath_or_buffer, "rb", use_auth_token=use_auth_token), **kwargs)
        except ValueError:  # Cannot seek streaming HTTP file
            return pd.read_excel(
                BytesIO(xopen(filepath_or_buffer, "rb", use_auth_token=use_auth_token).read()), **kwargs
            )


def xsio_loadmat(filepath_or_buffer, use_auth_token: Optional[Union[str, bool]] = None, **kwargs):
    import scipy.io as sio

    if hasattr(filepath_or_buffer, "read"):
        return sio.loadmat(filepath_or_buffer, **kwargs)
    else:
        return sio.loadmat(xopen(filepath_or_buffer, "rb", use_auth_token=use_auth_token), **kwargs)


def xet_parse(source, parser=None, use_auth_token: Optional[Union[str, bool]] = None):
    """Extend `xml.etree.ElementTree.parse` function to support remote files.

    Args:
        source: File path or file object.
        parser (`XMLParser`, *optional*, default `XMLParser`): Parser instance.
        use_auth_token (`bool` or `str`, optional): Whether to use token or token to authenticate on the
            Hugging Face Hub for private remote files.

    Returns:
        `xml.etree.ElementTree.Element`: Root element of the given source document.
    """
    if hasattr(source, "read"):
        return ET.parse(source, parser=parser)
    else:
        with xopen(source, "rb", use_auth_token=use_auth_token) as f:
            return ET.parse(f, parser=parser)


def xxml_dom_minidom_parse(filename_or_file, use_auth_token: Optional[Union[str, bool]] = None, **kwargs):
    """Extend `xml.dom.minidom.parse` function to support remote files.

    Args:
        filename_or_file (`str` or file): File path or file object.
        use_auth_token (`bool` or `str`, *optional*): Whether to use token or token to authenticate on the
            Hugging Face Hub for private remote files.
        **kwargs (optional): Additional keyword arguments passed to `xml.dom.minidom.parse`.

    Returns:
        :obj:`xml.dom.minidom.Document`: Parsed document.
    """
    if hasattr(filename_or_file, "read"):
        return xml.dom.minidom.parse(filename_or_file, **kwargs)
    else:
        with xopen(filename_or_file, "rb", use_auth_token=use_auth_token) as f:
            return xml.dom.minidom.parse(f, **kwargs)


class _IterableFromGenerator(Iterable):
    """Utility class to create an iterable from a generator function, in order to reset the generator when needed."""

    def __init__(self, generator: Callable, *args, **kwargs):
        self.generator = generator
        self.args = args
        self.kwargs = kwargs

    def __iter__(self):
        yield from self.generator(*self.args, **self.kwargs)


class ArchiveIterable(_IterableFromGenerator):
    """An iterable of (path, fileobj) from a TAR archive, used by `iter_archive`"""

    @staticmethod
    def _iter_tar(f):
        stream = tarfile.open(fileobj=f, mode="r|*")
        for tarinfo in stream:
            file_path = tarinfo.name
            if not tarinfo.isreg():
                continue
            if file_path is None:
                continue
            if os.path.basename(file_path).startswith((".", "__")):
                # skipping hidden files
                continue
            file_obj = stream.extractfile(tarinfo)
            yield file_path, file_obj
            stream.members = []
        del stream

    @staticmethod
    def _iter_zip(f):
        zipf = zipfile.ZipFile(f)
        for member in zipf.infolist():
            file_path = member.filename
            if member.is_dir():
                continue
            if file_path is None:
                continue
            if os.path.basename(file_path).startswith((".", "__")):
                # skipping hidden files
                continue
            file_obj = zipf.open(member)
            yield file_path, file_obj

    @classmethod
    def _iter_from_fileobj(cls, f) -> Generator[Tuple, None, None]:
        compression = _get_extraction_protocol_with_magic_number(f)
        if compression == "zip":
            yield from cls._iter_zip(f)
        else:
            yield from cls._iter_tar(f)

    @classmethod
    def _iter_from_urlpath(
        cls, urlpath: str, use_auth_token: Optional[Union[str, bool]] = None
    ) -> Generator[Tuple, None, None]:
        compression = _get_extraction_protocol(urlpath, use_auth_token=use_auth_token)
        with xopen(urlpath, "rb", use_auth_token=use_auth_token) as f:
            if compression == "zip":
                yield from cls._iter_zip(f)
            else:
                yield from cls._iter_tar(f)

    @classmethod
    def from_buf(cls, fileobj) -> "ArchiveIterable":
        return cls(cls._iter_from_fileobj, fileobj)

    @classmethod
    def from_urlpath(cls, urlpath_or_buf, use_auth_token: Optional[Union[str, bool]] = None) -> "ArchiveIterable":
        return cls(cls._iter_from_urlpath, urlpath_or_buf, use_auth_token)


class FilesIterable(_IterableFromGenerator):
    """An iterable of paths from a list of directories or files"""

    @classmethod
    def _iter_from_urlpaths(
        cls, urlpaths: Union[str, List[str]], use_auth_token: Optional[Union[str, bool]] = None
    ) -> Generator[str, None, None]:
        if not isinstance(urlpaths, list):
            urlpaths = [urlpaths]
        for urlpath in urlpaths:
            if xisfile(urlpath, use_auth_token=use_auth_token):
                if xbasename(urlpath).startswith((".", "__")):
                    # skipping hidden files
                    return
                yield urlpath
            else:
                for dirpath, dirnames, filenames in xwalk(urlpath, use_auth_token=use_auth_token):
                    # skipping hidden directories; prune the search
                    # [:] for the in-place list modification required by os.walk
                    # (only works for local paths as fsspec's walk doesn't support the in-place modification)
                    dirnames[:] = sorted([dirname for dirname in dirnames if not dirname.startswith((".", "__"))])
                    if xbasename(dirpath).startswith((".", "__")):
                        # skipping hidden directories
                        continue
                    for filename in sorted(filenames):
                        if filename.startswith((".", "__")):
                            # skipping hidden files
                            continue
                        yield xjoin(dirpath, filename)

    @classmethod
    def from_urlpaths(cls, urlpaths, use_auth_token: Optional[Union[str, bool]] = None) -> "FilesIterable":
        return cls(cls._iter_from_urlpaths, urlpaths, use_auth_token)


class StreamingDownloadManager:
    """
    Download manager that uses the "::" separator to navigate through (possibly remote) compressed archives.
    Contrary to the regular `DownloadManager`, the `download` and `extract` methods don't actually download nor extract
    data, but they rather return the path or url that could be opened using the `xopen` function which extends the
    built-in `open` function to stream data from remote files.
    """

    is_streaming = True

    def __init__(
        self,
        dataset_name: Optional[str] = None,
        data_dir: Optional[str] = None,
        download_config: Optional[DownloadConfig] = None,
        base_path: Optional[str] = None,
    ):
        self._dataset_name = dataset_name
        self._data_dir = data_dir
        self._base_path = base_path or os.path.abspath(".")
        self.download_config = download_config or DownloadConfig()

    @property
    def manual_dir(self):
        return self._data_dir

    def download(self, url_or_urls):
        """Normalize URL(s) of files to stream data from.
        This is the lazy version of `DownloadManager.download` for streaming.

        Args:
            url_or_urls (`str` or `list` or `dict`):
                URL(s) of files to stream data from. Each url is a `str`.

        Returns:
            url(s): (`str` or `list` or `dict`), URL(s) to stream data from matching the given input url_or_urls.

        Example:

        ```py
        >>> downloaded_files = dl_manager.download('https://storage.googleapis.com/seldon-datasets/sentence_polarity_v1/rt-polaritydata.tar.gz')
        ```
        """
        url_or_urls = map_nested(self._download, url_or_urls, map_tuple=True)
        return url_or_urls

    def _download(self, urlpath: str) -> str:
        urlpath = str(urlpath)
        if is_relative_path(urlpath):
            # append the relative path to the base_path
            urlpath = url_or_path_join(self._base_path, urlpath)
        return urlpath

    def extract(self, url_or_urls):
        """Add extraction protocol for given url(s) for streaming.

        This is the lazy version of `DownloadManager.extract` for streaming.

        Args:
            url_or_urls (`str` or `list` or `dict`):
                URL(s) of files to stream data from. Each url is a `str`.

        Returns:
            url(s): (`str` or `list` or `dict`), URL(s) to stream data from matching the given input `url_or_urls`.

        Example:

        ```py
        >>> downloaded_files = dl_manager.download('https://storage.googleapis.com/seldon-datasets/sentence_polarity_v1/rt-polaritydata.tar.gz')
        >>> extracted_files = dl_manager.extract(downloaded_files)
        ```
        """
        urlpaths = map_nested(self._extract, url_or_urls, map_tuple=True)
        return urlpaths

    def _extract(self, urlpath: str) -> str:
        urlpath = str(urlpath)
        protocol = _get_extraction_protocol(urlpath, use_auth_token=self.download_config.use_auth_token)
        # get inner file: zip://train-00000.json.gz::https://foo.bar/data.zip -> zip://train-00000.json.gz
        path = urlpath.split("::")[0]
        extension = _get_path_extension(path)
        if extension in ["tgz", "tar"] or path.endswith((".tar.gz", ".tar.bz2", ".tar.xz")):
            raise NotImplementedError(
                f"Extraction protocol for TAR archives like '{urlpath}' is not implemented in streaming mode. "
                f"Please use `dl_manager.iter_archive` instead.\n\n"
                f"Example usage:\n\n"
                f"\turl = dl_manager.download(url)\n"
                f"\ttar_archive_iterator = dl_manager.iter_archive(url)\n\n"
                f"\tfor filename, file in tar_archive_iterator:\n"
                f"\t\t..."
            )
        if protocol is None:
            # no extraction
            return urlpath
        elif protocol in SINGLE_FILE_COMPRESSION_PROTOCOLS:
            # there is one single file which is the uncompressed file
            inner_file = os.path.basename(urlpath.split("::")[0])
            inner_file = inner_file[: inner_file.rindex(".")] if "." in inner_file else inner_file
            return f"{protocol}://{inner_file}::{urlpath}"
        else:
            return f"{protocol}://::{urlpath}"

    def download_and_extract(self, url_or_urls):
        """Prepare given `url_or_urls` for streaming (add extraction protocol).

        This is the lazy version of `DownloadManager.download_and_extract` for streaming.

        Is equivalent to:

        ```
        urls = dl_manager.extract(dl_manager.download(url_or_urls))
        ```

        Args:
            url_or_urls (`str` or `list` or `dict`):
                URL(s) to stream from data from. Each url is a `str`.

        Returns:
            url(s): (`str` or `list` or `dict`), URL(s) to stream data from matching the given input `url_or_urls`.
        """
        return self.extract(self.download(url_or_urls))

    def iter_archive(self, urlpath_or_buf: Union[str, io.BufferedReader]) -> Iterable[Tuple]:
        """Iterate over files within an archive.

        Args:
            urlpath_or_buf (`str` or `io.BufferedReader`):
                Archive path or archive binary file object.

        Yields:
            `tuple[str, io.BufferedReader]`:
                2-tuple (path_within_archive, file_object).
                File object is opened in binary mode.

        Example:

        ```py
        >>> archive = dl_manager.download('https://storage.googleapis.com/seldon-datasets/sentence_polarity_v1/rt-polaritydata.tar.gz')
        >>> files = dl_manager.iter_archive(archive)
        ```
        """

        if hasattr(urlpath_or_buf, "read"):
            return ArchiveIterable.from_buf(urlpath_or_buf)
        else:
            return ArchiveIterable.from_urlpath(urlpath_or_buf, use_auth_token=self.download_config.use_auth_token)

    def iter_files(self, urlpaths: Union[str, List[str]]) -> Iterable[str]:
        """Iterate over files.

        Args:
            urlpaths (`str` or `list` of `str`):
                Root paths.

        Yields:
            str: File URL path.

        Example:

        ```py
        >>> files = dl_manager.download_and_extract('https://huggingface.co/datasets/beans/resolve/main/data/train.zip')
        >>> files = dl_manager.iter_files(files)
        ```
        """
        return FilesIterable.from_urlpaths(urlpaths, use_auth_token=self.download_config.use_auth_token)
