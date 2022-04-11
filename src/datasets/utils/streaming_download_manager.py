import glob
import io
import os
import posixpath
import re
import tarfile
import time
from asyncio import TimeoutError
from io import BytesIO
from itertools import chain
from pathlib import Path, PurePath, PurePosixPath
from typing import Callable, Generator, Iterable, List, Optional, Tuple, Union
from xml.etree import ElementTree as ET

import fsspec
from aiohttp.client_exceptions import ClientError

from .. import config
from ..filesystems import COMPRESSION_FILESYSTEMS
from .download_manager import DownloadConfig, map_nested
from .file_utils import (
    get_authentication_headers_for_url,
    http_head,
    is_local_path,
    is_relative_path,
    is_remote_url,
    url_or_path_join,
)
from .logging import get_logger


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
    "tar": "tar",
    "tgz": "tar",
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
    a, *b = a.split("::")
    if is_local_path(a):
        return os.path.basename(Path(a).as_posix())
    else:
        return posixpath.basename(a)


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
    a, *b = a.split("::")
    if is_local_path(a):
        return os.path.splitext(Path(a).as_posix())
    else:
        a, ext = posixpath.splitext(a)
        return "::".join([a] + b), ext


def xisfile(path, use_auth_token: Optional[Union[str, bool]] = None) -> bool:
    """Extend `os.path.isfile` function to support remote files.

    Args:
        path (:obj:`str`): URL path.

    Returns:
        :obj:`bool`
    """
    main_hop, *rest_hops = path.split("::")
    if is_local_path(main_hop):
        return os.path.isfile(path)
    else:
        if rest_hops and fsspec.get_fs_token_paths(rest_hops[0])[0].protocol == "https":
            storage_options = {
                "https": {"headers": get_authentication_headers_for_url(rest_hops[0], use_auth_token=use_auth_token)}
            }
        else:
            storage_options = None
        fs, *_ = fsspec.get_fs_token_paths(path, storage_options=storage_options)
        return fs.isfile(main_hop)


def xgetsize(path, use_auth_token: Optional[Union[str, bool]] = None) -> int:
    """Extend `os.path.getsize` function to support remote files.

    Args:
        path (:obj:`str`): URL path.

    Returns:
        :obj:`int`, optional
    """
    main_hop, *rest_hops = path.split("::")
    if is_local_path(main_hop):
        return os.path.getsize(path)
    else:
        if rest_hops and fsspec.get_fs_token_paths(rest_hops[0])[0].protocol == "https":
            storage_options = {
                "https": {"headers": get_authentication_headers_for_url(rest_hops[0], use_auth_token=use_auth_token)}
            }
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
        path (:obj:`str`): URL path.

    Returns:
        :obj:`bool`
    """
    main_hop, *rest_hops = path.split("::")
    if is_local_path(main_hop):
        return os.path.isdir(path)
    else:
        if rest_hops and fsspec.get_fs_token_paths(rest_hops[0])[0].protocol == "https":
            storage_options = {
                "https": {"headers": get_authentication_headers_for_url(rest_hops[0], use_auth_token=use_auth_token)}
            }
        else:
            storage_options = None
        fs, *_ = fsspec.get_fs_token_paths(path, storage_options=storage_options)
        return fs.isdir(main_hop)


def xrelpath(path, start=None):
    """Extend `os.path.relpath` function to support remote files.

    Args:
        path (:obj:`str`): URL path.
        start (:obj:`str`): Start URL directory path.

    Returns:
        :obj:`str`
    """
    main_hop, *rest_hops = path.split("::")
    if is_local_path(main_hop):
        return os.path.relpath(main_hop, start=start) if start else os.path.relpath(main_hop)
    else:
        return posixpath.relpath(main_hop, start=start.split("::")[0]) if start else os.path.relpath(main_hop)


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
            except (ClientError, TimeoutError):
                logger.warning(
                    f"Got disconnected from remote data host. Retrying in {config.STREAMING_READ_RETRY_INTERVAL}sec [{retry}/{max_retries}]"
                )
                time.sleep(config.STREAMING_READ_RETRY_INTERVAL)
        else:
            raise ConnectionError("Server Disconnected")
        return out

    file_obj.read = read_with_retries


def _get_extraction_protocol_with_magic_number(f) -> Optional[str]:
    """read the magic number from a file-like object and return the compression protocol"""
    prev_loc = f.loc
    magic_number = f.read(MAGIC_NUMBER_MAX_LENGTH)
    f.seek(prev_loc)
    for i in range(MAGIC_NUMBER_MAX_LENGTH):
        compression = MAGIC_NUMBER_TO_COMPRESSION_PROTOCOL.get(magic_number[: MAGIC_NUMBER_MAX_LENGTH - i])
        if compression is not None:  # TODO(QL): raise an error for .tar.gz files as in _get_extraction_protocol
            return compression
        compression = MAGIC_NUMBER_TO_UNSUPPORTED_COMPRESSION_PROTOCOL.get(magic_number[: MAGIC_NUMBER_MAX_LENGTH - i])
        if compression is not None:
            raise NotImplementedError(f"Compression protocol '{compression}' not implemented.")


def _get_extraction_protocol(urlpath: str, use_auth_token: Optional[Union[str, bool]] = None) -> Optional[str]:
    # get inner file: zip://train-00000.json.gz::https://foo.bar/data.zip -> zip://train-00000.json.gz
    path = urlpath.split("::")[0]
    # Get extension: https://foo.bar/train.json.gz -> gz
    extension = path.split(".")[-1]
    # Remove query params ("dl=1", "raw=true"): gz?dl=1 -> gz
    # Remove shards infos (".txt_1", ".txt-00000-of-00100"): txt_1 -> txt
    for symb in "?-_":
        extension = extension.split(symb)[0]
    if extension in BASE_KNOWN_EXTENSIONS:
        return None
    elif path.endswith(".tar.gz") or path.endswith(".tgz"):
        raise NotImplementedError(
            f"Extraction protocol for TAR archives like '{urlpath}' is not implemented in streaming mode. Please use `dl_manager.iter_archive` instead."
        )
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
    kwargs = {"headers": get_authentication_headers_for_url(url, use_auth_token=use_auth_token)}
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
    """
    This function extends the builtin `open` function to support remote files using fsspec.

    It also has a retry mechanism in case connection fails.
    The args and kwargs are passed to fsspec.open, except `use_auth_token` which is used for queries to private repos on huggingface.co
    """
    # required for `xopen(str(Path(...)))` to work
    file = _as_posix(PurePath(file))
    main_hop, *rest_hops = file.split("::")
    # add headers and cookies for authentication on the HF Hub and for Google Drive
    if not rest_hops and (main_hop.startswith("http://") or main_hop.startswith("https://")):
        file, new_kwargs = _prepare_http_url_kwargs(file, use_auth_token=use_auth_token)
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
        path (:obj:`str`): URL path.

    Returns:
        :obj:`list` of :obj:`str`
    """
    main_hop, *rest_hops = path.split("::")
    if is_local_path(main_hop):
        return os.listdir(path)
    else:
        # globbing inside a zip in a private repo requires authentication
        if rest_hops and fsspec.get_fs_token_paths(rest_hops[0])[0].protocol == "https":
            storage_options = {
                "https": {"headers": get_authentication_headers_for_url(rest_hops[0], use_auth_token=use_auth_token)}
            }
        else:
            storage_options = None
        fs, *_ = fsspec.get_fs_token_paths(path, storage_options=storage_options)
        objects = fs.listdir(main_hop.split("://")[1])
        return [os.path.basename(obj["name"]) for obj in objects]


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
        if rest_hops and (rest_hops[0].startswith("http://") or rest_hops[0].startswith("https://")):
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


def xpathparent(path: Path):
    """Name function for argument of type :obj:`~pathlib.Path` that supports both local paths end remote URLs.

    Args:
        path (:obj:`~pathlib.Path`): Calling Path instance.

    Returns:
        :obj:`~pathlib.Path`
    """
    return type(path)(xdirname(_as_posix(path)))


def xpathname(path: Path):
    """Name function for argument of type :obj:`~pathlib.Path` that supports both local paths end remote URLs.

    Args:
        path (:obj:`~pathlib.Path`): Calling Path instance.

    Returns:
        :obj:`str`
    """
    return PurePosixPath(_as_posix(path).split("::")[0]).name


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


def xwalk(urlpath, use_auth_token: Optional[Union[str, bool]] = None):
    """Extend `os.walk` function to support remote files.

    Args:
        urlpath (:obj:`str`): URL root path.
        use_auth_token (:obj:`bool` or :obj:`str`, optional): Whether to use token or token to authenticate on the
            Hugging Face Hub for private remote files.

    Yields:
        :obj:`tuple`: 3-tuple (dirpath, dirnames, filenames).
    """
    main_hop, *rest_hops = urlpath.split("::")
    if is_local_path(main_hop):
        return os.walk(main_hop)
    else:
        # walking inside a zip in a private repo requires authentication
        if rest_hops and (rest_hops[0].startswith("http://") or rest_hops[0].startswith("https://")):
            url = rest_hops[0]
            url, kwargs = _prepare_http_url_kwargs(url, use_auth_token=use_auth_token)
            storage_options = {"https": kwargs}
            urlpath = "::".join([main_hop, url, *rest_hops[1:]])
        else:
            storage_options = None
        fs, *_ = fsspec.get_fs_token_paths(urlpath, storage_options=storage_options)
        for dirpath, dirnames, filenames in fs.walk(main_hop):
            yield "::".join([f"{fs.protocol}://{dirpath}"] + rest_hops), dirnames, filenames


def xpandas_read_csv(filepath_or_buffer, use_auth_token: Optional[Union[str, bool]] = None, **kwargs):
    import pandas as pd

    if hasattr(filepath_or_buffer, "read"):
        return pd.read_csv(filepath_or_buffer, **kwargs)
    else:
        return pd.read_csv(xopen(filepath_or_buffer, use_auth_token=use_auth_token), **kwargs)


def xpandas_read_excel(filepath_or_buffer, **kwargs):
    import pandas as pd

    return pd.read_excel(BytesIO(filepath_or_buffer.read()), **kwargs)


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
        parser (optional, default `XMLParser`): Parser instance.
        use_auth_token (:obj:`bool` or :obj:`str`, optional): Whether to use token or token to authenticate on the
            Hugging Face Hub for private remote files.

    Returns:
        :obj:`xml.etree.ElementTree.Element`: Root element of the given source document.
    """
    if hasattr(source, "read"):
        return ET.parse(source, parser=parser)
    else:
        with xopen(source, "rb", use_auth_token=use_auth_token) as f:
            return ET.parse(f, parser=parser)


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

    @classmethod
    def _iter_from_fileobj(cls, f) -> Generator[Tuple, None, None]:
        stream = tarfile.open(fileobj=f, mode="r|*")
        for tarinfo in stream:
            file_path = tarinfo.name
            if not tarinfo.isreg():
                continue
            if file_path is None:
                continue
            if os.path.basename(file_path).startswith(".") or os.path.basename(file_path).startswith("__"):
                # skipping hidden files
                continue
            file_obj = stream.extractfile(tarinfo)
            yield file_path, file_obj
            stream.members = []
        del stream

    @classmethod
    def _iter_from_urlpath(
        cls, urlpath: str, use_auth_token: Optional[Union[str, bool]] = None
    ) -> Generator[Tuple, None, None]:
        with xopen(urlpath, "rb", use_auth_token=use_auth_token) as f:
            yield from cls._iter_from_fileobj(f)

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
                yield urlpath
            else:
                for dirpath, _, filenames in xwalk(urlpath, use_auth_token=use_auth_token):
                    for filename in filenames:
                        yield xjoin(dirpath, filename)

    @classmethod
    def from_urlpaths(cls, urlpaths, use_auth_token: Optional[Union[str, bool]] = None) -> "FilesIterable":
        return cls(cls._iter_from_urlpaths, urlpaths, use_auth_token)


class StreamingDownloadManager:
    """
    Download manager that uses the "::" separator to navigate through (possibly remote) compressed archives.
    Contrary to the regular DownloadManager, the `download` and `extract` methods don't actually download nor extract
    data, but they rather return the path or url that could be opened using the `xopen` function which extends the
    builtin `open` function to stream data from remote files.
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
        protocol = _get_extraction_protocol(urlpath, use_auth_token=self.download_config.use_auth_token)
        if protocol is None:
            # no extraction
            return urlpath
        elif protocol in SINGLE_FILE_COMPRESSION_PROTOCOLS:
            # there is one single file which is the uncompressed file
            inner_file = os.path.basename(urlpath.split("::")[0])
            inner_file = inner_file[: inner_file.rindex(".")] if "." in inner_file else inner_file
            # check for tar.gz, tar.bz2 etc.
            if inner_file.endswith(".tar"):
                return f"tar://::{protocol}://{inner_file}::{urlpath}"
            else:
                return f"{protocol}://{inner_file}::{urlpath}"
        else:
            return f"{protocol}://::{urlpath}"

    def download_and_extract(self, url_or_urls):
        return self.extract(self.download(url_or_urls))

    def iter_archive(self, urlpath_or_buf: Union[str, io.BufferedReader]) -> Iterable[Tuple]:
        """Iterate over files within an archive.

        Args:
            urlpath_or_buf (:obj:`str` or :obj:`io.BufferedReader`): Archive path or archive binary file object.

        Yields:
            :obj:`tuple`[:obj:`str`, :obj:`io.BufferedReader`]: 2-tuple (path_within_archive, file_object).
                File object is opened in binary mode.
        """

        if hasattr(urlpath_or_buf, "read"):
            return ArchiveIterable.from_buf(urlpath_or_buf)
        else:
            return ArchiveIterable.from_urlpath(urlpath_or_buf, use_auth_token=self.download_config.use_auth_token)

    def iter_files(self, urlpaths: Union[str, List[str]]) -> Iterable[str]:
        """Iterate over files.

        Args:
            urlpaths (:obj:`str` or :obj:`list` of :obj:`str`): Root paths.

        Yields:
            str: File URL path.
        """
        return FilesIterable.from_urlpaths(urlpaths, use_auth_token=self.download_config.use_auth_token)
