"""
Utilities for working with the local dataset cache.
This file is adapted from the AllenNLP library at https://github.com/allenai/allennlp
Copyright by the AllenNLP authors.
"""

import copy
import io
import json
import os
import re
import shutil
import sys
import tempfile
import time
import urllib
import warnings
from contextlib import closing, contextmanager
from dataclasses import dataclass
from functools import partial
from hashlib import sha256
from pathlib import Path
from typing import Dict, List, Optional, TypeVar, Union
from urllib.parse import urlparse

import numpy as np
import posixpath
import requests
from tqdm.contrib.concurrent import thread_map

from .. import __version__, config, utils
from . import logging
from .extract import ExtractManager
from .filelock import FileLock
from .tqdm_utils import tqdm


logger = logging.get_logger(__name__)  # pylint: disable=invalid-name

INCOMPLETE_SUFFIX = ".incomplete"

T = TypeVar("T", str, Path)


def init_hf_modules(hf_modules_cache: Optional[Union[Path, str]] = None) -> str:
    """
    Add hf_modules_cache to the python path.
    By default hf_modules_cache='~/.cache/huggingface/modules'.
    It can also be set with the environment variable HF_MODULES_CACHE.
    This is used to add modules such as `datasets_modules`
    """
    hf_modules_cache = hf_modules_cache if hf_modules_cache is not None else config.HF_MODULES_CACHE
    hf_modules_cache = str(hf_modules_cache)
    if hf_modules_cache not in sys.path:
        sys.path.append(hf_modules_cache)

        os.makedirs(hf_modules_cache, exist_ok=True)
        if not os.path.exists(os.path.join(hf_modules_cache, "__init__.py")):
            with open(os.path.join(hf_modules_cache, "__init__.py"), "w"):
                pass
    return hf_modules_cache


@contextmanager
def temp_seed(seed: int, set_pytorch=False, set_tensorflow=False):
    """Temporarily set the random seed. This works for python numpy, pytorch and tensorflow."""
    np_state = np.random.get_state()
    np.random.seed(seed)

    if set_pytorch and config.TORCH_AVAILABLE:
        import torch

        torch_state = torch.random.get_rng_state()
        torch.random.manual_seed(seed)

        if torch.cuda.is_available():
            torch_cuda_states = torch.cuda.get_rng_state_all()
            torch.cuda.manual_seed_all(seed)

    if set_tensorflow and config.TF_AVAILABLE:
        import tensorflow as tf
        from tensorflow.python import context as tfpycontext

        tf_state = tf.random.get_global_generator()
        temp_gen = tf.random.Generator.from_seed(seed)
        tf.random.set_global_generator(temp_gen)

        if not tf.executing_eagerly():
            raise ValueError("Setting random seed for TensorFlow is only available in eager mode")

        tf_context = tfpycontext.context()  # eager mode context
        tf_seed = tf_context._seed
        tf_rng_initialized = hasattr(tf_context, "_rng")
        if tf_rng_initialized:
            tf_rng = tf_context._rng
        tf_context._set_global_seed(seed)

    try:
        yield
    finally:
        np.random.set_state(np_state)

        if set_pytorch and config.TORCH_AVAILABLE:
            torch.random.set_rng_state(torch_state)
            if torch.cuda.is_available():
                torch.cuda.set_rng_state_all(torch_cuda_states)

        if set_tensorflow and config.TF_AVAILABLE:
            tf.random.set_global_generator(tf_state)

            tf_context._seed = tf_seed
            if tf_rng_initialized:
                tf_context._rng = tf_rng
            else:
                delattr(tf_context, "_rng")


def is_remote_url(url_or_filename: str) -> bool:
    parsed = urlparse(url_or_filename)
    return parsed.scheme in ("http", "https", "s3", "gs", "hdfs", "ftp")


def is_local_path(url_or_filename: str) -> bool:
    # On unix the scheme of a local path is empty (for both absolute and relative),
    # while on windows the scheme is the drive name (ex: "c") for absolute paths.
    # for details on the windows behavior, see https://bugs.python.org/issue42215
    return urlparse(url_or_filename).scheme == "" or os.path.ismount(urlparse(url_or_filename).scheme + ":/")


def is_relative_path(url_or_filename: str) -> bool:
    return urlparse(url_or_filename).scheme == "" and not os.path.isabs(url_or_filename)


def relative_to_absolute_path(path: T) -> T:
    """Convert relative path to absolute path."""
    abs_path_str = os.path.abspath(os.path.expanduser(os.path.expandvars(str(path))))
    return Path(abs_path_str) if isinstance(path, Path) else abs_path_str


def hf_bucket_url(identifier: str, filename: str, use_cdn=False, dataset=True) -> str:
    if dataset:
        endpoint = config.CLOUDFRONT_DATASETS_DISTRIB_PREFIX if use_cdn else config.S3_DATASETS_BUCKET_PREFIX
    else:
        endpoint = config.CLOUDFRONT_METRICS_DISTRIB_PREFIX if use_cdn else config.S3_METRICS_BUCKET_PREFIX
    return "/".join((endpoint, identifier, filename))


def head_hf_s3(
    identifier: str, filename: str, use_cdn=False, dataset=True, max_retries=0
) -> Union[requests.Response, Exception]:
    return http_head(
        hf_bucket_url(identifier=identifier, filename=filename, use_cdn=use_cdn, dataset=dataset),
        max_retries=max_retries,
    )


def hf_github_url(path: str, name: str, dataset=True, revision: Optional[str] = None, version="deprecated") -> str:
    from .. import SCRIPTS_VERSION

    if version != "deprecated":
        warnings.warn(
            "'version' was renamed to 'revision' in version 1.13 and will be removed in 1.15.", FutureWarning
        )
        revision = version
    revision = revision or os.getenv("HF_SCRIPTS_VERSION", SCRIPTS_VERSION)
    if dataset:
        return config.REPO_DATASETS_URL.format(revision=revision, path=path, name=name)
    else:
        return config.REPO_METRICS_URL.format(revision=revision, path=path, name=name)


def hf_hub_url(path: str, name: str, revision: Optional[str] = None, version="deprecated") -> str:
    if version != "deprecated":
        warnings.warn(
            "'version' was renamed to 'revision' in version 1.13 and will be removed in 1.15.", FutureWarning
        )
        revision = version
    revision = revision or config.HUB_DEFAULT_VERSION
    return config.HUB_DATASETS_URL.format(path=path, name=name, revision=revision)


def url_or_path_join(base_name: str, *pathnames: str) -> str:
    if is_remote_url(base_name):
        return posixpath.join(base_name, *(str(pathname).replace(os.sep, "/").lstrip("/") for pathname in pathnames))
    else:
        return Path(base_name, *pathnames).as_posix()


def url_or_path_parent(url_or_path: str) -> str:
    if is_remote_url(url_or_path):
        return url_or_path[: url_or_path.rindex("/")]
    else:
        return os.path.dirname(url_or_path)


def hash_url_to_filename(url, etag=None):
    """
    Convert `url` into a hashed filename in a repeatable way.
    If `etag` is specified, append its hash to the url's, delimited
    by a period.
    If the url ends with .h5 (Keras HDF5 weights) adds '.h5' to the name
    so that TF 2.0 can identify it as a HDF5 file
    (see https://github.com/tensorflow/tensorflow/blob/00fad90125b18b80fe054de1055770cfb8fe4ba3/tensorflow/python/keras/engine/network.py#L1380)
    """
    url_bytes = url.encode("utf-8")
    url_hash = sha256(url_bytes)
    filename = url_hash.hexdigest()

    if etag:
        etag_bytes = etag.encode("utf-8")
        etag_hash = sha256(etag_bytes)
        filename += "." + etag_hash.hexdigest()

    if url.endswith(".py"):
        filename += ".py"

    return filename


@dataclass
class DownloadConfig:
    """Configuration for our cached path manager.

    Attributes:
        cache_dir (:obj:`str` or :obj:`Path`, optional): Specify a cache directory to save the file to (overwrite the
            default cache dir).
        force_download (:obj:`bool`, default ``False``): If True, re-dowload the file even if it's already cached in
            the cache dir.
        resume_download (:obj:`bool`, default ``False``): If True, resume the download if incompletly recieved file is
            found.
        proxies (:obj:`dict`, optional):
        user_agent (:obj:`str`, optional): Optional string or dict that will be appended to the user-agent on remote
            requests.
        extract_compressed_file (:obj:`bool`, default ``False``): If True and the path point to a zip or tar file,
            extract the compressed file in a folder along the archive.
        force_extract (:obj:`bool`, default ``False``): If True when extract_compressed_file is True and the archive
            was already extracted, re-extract the archive and override the folder where it was extracted.
        delete_extracted (:obj:`bool`, default ``False``): Whether to delete (or keep) the extracted files.
        use_etag (:obj:`bool`, default ``True``):
        num_proc (:obj:`int`, optional):
        max_retries (:obj:`int`, default ``1``): The number of times to retry an HTTP request if it fails.
        use_auth_token (:obj:`str` or :obj:`bool`, optional): Optional string or boolean to use as Bearer token
            for remote files on the Datasets Hub. If True, will get token from ~/.huggingface.
    """

    cache_dir: Optional[Union[str, Path]] = None
    force_download: bool = False
    resume_download: bool = False
    local_files_only: bool = False
    proxies: Optional[Dict] = None
    user_agent: Optional[str] = None
    extract_compressed_file: bool = False
    force_extract: bool = False
    delete_extracted: bool = False
    use_etag: bool = True
    num_proc: Optional[int] = None
    max_retries: int = 1
    use_auth_token: Optional[Union[str, bool]] = None

    def copy(self) -> "DownloadConfig":
        return self.__class__(**{k: copy.deepcopy(v) for k, v in self.__dict__.items()})


def cached_path(
    url_or_filename,
    download_config=None,
    **download_kwargs,
) -> str:
    """
    Given something that might be a URL (or might be a local path),
    determine which. If it's a URL, download the file and cache it, and
    return the path to the cached file. If it's already a local path,
    make sure the file exists and then return the path.

    Return:
        Local path (string)

    Raises:
        FileNotFoundError: in case of non-recoverable file
            (non-existent or no cache on disk)
        ConnectionError: in case of unreachable url
            and no cache on disk
        ValueError: if it couldn't parse the url or filename correctly
        requests.exceptions.ConnectionError: in case of internet connection issue
    """
    if download_config is None:
        download_config = DownloadConfig(**download_kwargs)

    cache_dir = download_config.cache_dir or config.DOWNLOADED_DATASETS_PATH
    if isinstance(cache_dir, Path):
        cache_dir = str(cache_dir)
    if isinstance(url_or_filename, Path):
        url_or_filename = str(url_or_filename)

    if is_remote_url(url_or_filename):
        # URL, so get it from the cache (downloading if necessary)
        output_path = get_from_cache(
            url_or_filename,
            cache_dir=cache_dir,
            force_download=download_config.force_download,
            proxies=download_config.proxies,
            resume_download=download_config.resume_download,
            user_agent=download_config.user_agent,
            local_files_only=download_config.local_files_only,
            use_etag=download_config.use_etag,
            max_retries=download_config.max_retries,
            use_auth_token=download_config.use_auth_token,
        )
    elif os.path.exists(url_or_filename):
        # File, and it exists.
        output_path = url_or_filename
    elif is_local_path(url_or_filename):
        # File, but it doesn't exist.
        raise FileNotFoundError("Local file {} doesn't exist".format(url_or_filename))
    else:
        # Something unknown
        raise ValueError("unable to parse {} as a URL or as a local path".format(url_or_filename))

    if output_path is None:
        return output_path

    if download_config.extract_compressed_file:
        output_path = ExtractManager(cache_dir=download_config.cache_dir).extract(
            output_path, force_extract=download_config.force_extract
        )

    return output_path


def get_datasets_user_agent(user_agent: Optional[Union[str, dict]] = None) -> str:
    ua = "datasets/{}; python/{}".format(__version__, config.PY_VERSION)
    ua += "; pyarrow/{}".format(config.PYARROW_VERSION)
    if config.TORCH_AVAILABLE:
        ua += "; torch/{}".format(config.TORCH_VERSION)
    if config.TF_AVAILABLE:
        ua += "; tensorflow/{}".format(config.TF_VERSION)
    if config.JAX_AVAILABLE:
        ua += "; jax/{}".format(config.JAX_VERSION)
    if config.BEAM_AVAILABLE:
        ua += "; apache_beam/{}".format(config.BEAM_VERSION)
    if isinstance(user_agent, dict):
        ua += "; " + "; ".join("{}/{}".format(k, v) for k, v in user_agent.items())
    elif isinstance(user_agent, str):
        ua += "; " + user_agent
    return ua


def get_authentication_headers_for_url(url: str, use_auth_token: Optional[Union[str, bool]] = None) -> dict:
    """Handle the HF authentication"""
    headers = {}
    if url.startswith("https://huggingface.co/"):
        token = None
        if isinstance(use_auth_token, str):
            token = use_auth_token
        elif bool(use_auth_token):
            from huggingface_hub import hf_api

            token = hf_api.HfFolder.get_token()
        if token:
            headers["authorization"] = "Bearer {}".format(token)
    return headers


class OfflineModeIsEnabled(ConnectionError):
    pass


def _raise_if_offline_mode_is_enabled(msg: Optional[str] = None):
    """Raise a OfflineModeIsEnabled error (subclass of ConnectionError) if HF_DATASETS_OFFLINE is True."""
    if config.HF_DATASETS_OFFLINE:
        raise OfflineModeIsEnabled(
            "Offline mode is enabled." if msg is None else "Offline mode is enabled. " + str(msg)
        )


def _request_with_retry(
    method: str,
    url: str,
    max_retries: int = 0,
    base_wait_time: float = 0.5,
    max_wait_time: float = 2,
    timeout: float = 10.0,
    **params,
) -> requests.Response:
    """Wrapper around requests to retry in case it fails with a ConnectTimeout, with exponential backoff.

    Note that if the environment variable HF_DATASETS_OFFLINE is set to 1, then a OfflineModeIsEnabled error is raised.

    Args:
        method (str): HTTP method, such as 'GET' or 'HEAD'.
        url (str): The URL of the resource to fetch.
        max_retries (int): Maximum number of retries, defaults to 0 (no retries).
        base_wait_time (float): Duration (in seconds) to wait before retrying the first time. Wait time between
            retries then grows exponentially, capped by max_wait_time.
        max_wait_time (float): Maximum amount of time between two retries, in seconds.
        **params: Params to pass to :obj:`requests.request`.
    """
    _raise_if_offline_mode_is_enabled(f"Tried to reach {url}")
    tries, success = 0, False
    while not success:
        tries += 1
        try:
            response = requests.request(method=method.upper(), url=url, timeout=timeout, **params)
            success = True
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as err:
            if tries > max_retries:
                raise err
            else:
                logger.info(f"{method} request to {url} timed out, retrying... [{tries/max_retries}]")
                sleep_time = min(max_wait_time, base_wait_time * 2 ** (tries - 1))  # Exponential backoff
                time.sleep(sleep_time)
    return response


def ftp_head(url, timeout=10.0):
    _raise_if_offline_mode_is_enabled(f"Tried to reach {url}")
    try:
        with closing(urllib.request.urlopen(url, timeout=timeout)) as r:
            r.read(1)
    except Exception:
        return False
    return True


def ftp_get(url, temp_file, timeout=10.0):
    _raise_if_offline_mode_is_enabled(f"Tried to reach {url}")
    try:
        logger.info(f"Getting through FTP {url} into {temp_file.name}")
        with closing(urllib.request.urlopen(url, timeout=timeout)) as r:
            shutil.copyfileobj(r, temp_file)
    except urllib.error.URLError as e:
        raise ConnectionError(e) from None


def http_get(url, temp_file, proxies=None, resume_size=0, headers=None, cookies=None, timeout=100.0, max_retries=0):
    headers = copy.deepcopy(headers) or {}
    headers["user-agent"] = get_datasets_user_agent(user_agent=headers.get("user-agent"))
    if resume_size > 0:
        headers["Range"] = "bytes=%d-" % (resume_size,)
    response = _request_with_retry(
        method="GET",
        url=url,
        stream=True,
        proxies=proxies,
        headers=headers,
        cookies=cookies,
        max_retries=max_retries,
        timeout=timeout,
    )
    if response.status_code == 416:  # Range not satisfiable
        return
    content_length = response.headers.get("Content-Length")
    total = resume_size + int(content_length) if content_length is not None else None
    progress = utils.tqdm(
        unit="B",
        unit_scale=True,
        total=total,
        initial=resume_size,
        desc="Downloading",
        disable=bool(logging.get_verbosity() == logging.NOTSET),
    )
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:  # filter out keep-alive new chunks
            progress.update(len(chunk))
            temp_file.write(chunk)
    progress.close()


def http_head(
    url, proxies=None, headers=None, cookies=None, allow_redirects=True, timeout=10.0, max_retries=0
) -> requests.Response:
    headers = copy.deepcopy(headers) or {}
    headers["user-agent"] = get_datasets_user_agent(user_agent=headers.get("user-agent"))
    response = _request_with_retry(
        method="HEAD",
        url=url,
        proxies=proxies,
        headers=headers,
        cookies=cookies,
        allow_redirects=allow_redirects,
        timeout=timeout,
        max_retries=max_retries,
    )
    return response


def request_etag(url: str, use_auth_token: Optional[Union[str, bool]] = None) -> Optional[str]:
    headers = get_authentication_headers_for_url(url, use_auth_token=use_auth_token)
    response = http_head(url, headers=headers, max_retries=3)
    response.raise_for_status()
    etag = response.headers.get("ETag") if response.ok else None
    return etag


def request_etags(
    urls: List[str],
    use_auth_token: Optional[Union[str, bool]] = None,
    max_workers=64,
    tqdm_kwargs: Optional[dict] = None,
) -> List[Optional[str]]:
    tqdm_kwargs = tqdm_kwargs if tqdm_kwargs is not None else {}
    tqdm_kwargs["desc"] = tqdm_kwargs.get("desc", "Get ETags")
    tqdm_kwargs["disable"] = tqdm_kwargs.get("disable", len(urls) <= 16 or logging.get_verbosity() == logging.NOTSET)
    return thread_map(
        partial(request_etag, use_auth_token=use_auth_token),
        urls,
        max_workers=max_workers,
        tqdm_class=tqdm,
        **tqdm_kwargs,
    )


def get_from_cache(
    url,
    cache_dir=None,
    force_download=False,
    proxies=None,
    etag_timeout=10,
    resume_download=False,
    user_agent=None,
    local_files_only=False,
    use_etag=True,
    max_retries=0,
    use_auth_token=None,
) -> str:
    """
    Given a URL, look for the corresponding file in the local cache.
    If it's not there, download it. Then return the path to the cached file.

    Return:
        Local path (string)

    Raises:
        FileNotFoundError: in case of non-recoverable file
            (non-existent or no cache on disk)
        ConnectionError: in case of unreachable url
            and no cache on disk
    """
    if cache_dir is None:
        cache_dir = config.HF_DATASETS_CACHE
    if isinstance(cache_dir, Path):
        cache_dir = str(cache_dir)

    os.makedirs(cache_dir, exist_ok=True)

    original_url = url  # Some parameters may be added
    connected = False
    response = None
    cookies = None
    etag = None

    # Try a first time to file the file on the local file system without eTag (None)
    # if we don't ask for 'force_download' then we spare a request
    filename = hash_url_to_filename(original_url, etag=None)
    cache_path = os.path.join(cache_dir, filename)

    if os.path.exists(cache_path) and not force_download and not use_etag:
        return cache_path

    # Prepare headers for authentication
    headers = get_authentication_headers_for_url(url, use_auth_token=use_auth_token)
    if user_agent is not None:
        headers["user-agent"] = user_agent

    # We don't have the file locally or we need an eTag
    if not local_files_only:
        if url.startswith("ftp://"):
            connected = ftp_head(url)
        try:
            response = http_head(
                url,
                allow_redirects=True,
                proxies=proxies,
                timeout=etag_timeout,
                max_retries=max_retries,
                headers=headers,
            )
            if response.status_code == 200:  # ok
                etag = response.headers.get("ETag") if use_etag else None
                for k, v in response.cookies.items():
                    # In some edge cases, we need to get a confirmation token
                    if k.startswith("download_warning") and "drive.google.com" in url:
                        url += "&confirm=" + v
                        cookies = response.cookies
                connected = True
            # In some edge cases, head request returns 400 but the connection is actually ok
            elif (
                (response.status_code == 400 and "firebasestorage.googleapis.com" in url)
                or (response.status_code == 405 and "drive.google.com" in url)
                or (
                    response.status_code == 403
                    and re.match(r"^https?://github.com/.*?/.*?/releases/download/.*?/.*?$", url)
                )
            ):
                connected = True
                logger.info("Couldn't get ETag version for url {}".format(url))
        except (EnvironmentError, requests.exceptions.Timeout):
            # not connected
            pass

    # connected == False = we don't have a connection, or url doesn't exist, or is otherwise inaccessible.
    # try to get the last downloaded one
    if not connected:
        if os.path.exists(cache_path):
            return cache_path
        if local_files_only:
            raise FileNotFoundError(
                f"Cannot find the requested files in the cached path at {cache_path} and outgoing traffic has been"
                " disabled. To enable file online look-ups, set 'local_files_only' to False."
            )
        elif response is not None and response.status_code == 404:
            raise FileNotFoundError("Couldn't find file at {}".format(url))
        _raise_if_offline_mode_is_enabled(f"Tried to reach {url}")
        raise ConnectionError("Couldn't reach {}".format(url))

    # Try a second time
    filename = hash_url_to_filename(original_url, etag)
    cache_path = os.path.join(cache_dir, filename)

    if os.path.exists(cache_path) and not force_download:
        return cache_path

    # From now on, connected is True.
    # Prevent parallel downloads of the same file with a lock.
    lock_path = cache_path + ".lock"
    with FileLock(lock_path):

        if resume_download:
            incomplete_path = cache_path + ".incomplete"

            @contextmanager
            def _resumable_file_manager():
                with open(incomplete_path, "a+b") as f:
                    yield f

            temp_file_manager = _resumable_file_manager
            if os.path.exists(incomplete_path):
                resume_size = os.stat(incomplete_path).st_size
            else:
                resume_size = 0
        else:
            temp_file_manager = partial(tempfile.NamedTemporaryFile, dir=cache_dir, delete=False)
            resume_size = 0

        # Download to temporary file, then copy to cache dir once finished.
        # Otherwise you get corrupt cache entries if the download gets interrupted.
        with temp_file_manager() as temp_file:
            logger.info("%s not found in cache or force_download set to True, downloading to %s", url, temp_file.name)

            # GET file object
            if url.startswith("ftp://"):
                ftp_get(url, temp_file)
            else:
                http_get(
                    url,
                    temp_file,
                    proxies=proxies,
                    resume_size=resume_size,
                    headers=headers,
                    cookies=cookies,
                    max_retries=max_retries,
                )

        logger.info("storing %s in cache at %s", url, cache_path)
        shutil.move(temp_file.name, cache_path)

        logger.info("creating metadata file for %s", cache_path)
        meta = {"url": url, "etag": etag}
        meta_path = cache_path + ".json"
        with open(meta_path, "w", encoding="utf-8") as meta_file:
            json.dump(meta, meta_file)

    return cache_path


def add_start_docstrings(*docstr):
    def docstring_decorator(fn):
        fn.__doc__ = "".join(docstr) + (fn.__doc__ if fn.__doc__ is not None else "")
        return fn

    return docstring_decorator


def add_end_docstrings(*docstr):
    def docstring_decorator(fn):
        fn.__doc__ = (fn.__doc__ if fn.__doc__ is not None else "") + "".join(docstr)
        return fn

    return docstring_decorator


def estimate_dataset_size(paths):
    return sum(path.stat().st_size for path in paths)


def readline(f: io.RawIOBase):
    # From: https://github.com/python/cpython/blob/d27e2f4d118e7a9909b6a3e5da06c5ff95806a85/Lib/_pyio.py#L525
    res = bytearray()
    while True:
        b = f.read(1)
        if not b:
            break
        res += b
        if res.endswith(b"\n"):
            break
    return bytes(res)
