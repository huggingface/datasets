"""
Utilities for working with the local dataset cache.
This file is adapted from the AllenNLP library at https://github.com/allenai/allennlp
Copyright by the AllenNLP authors.
"""

import gzip
import json
import logging
import os
import shutil
import sys
import tarfile
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from functools import partial
from hashlib import sha256
from typing import Dict, Optional, Union
from urllib.parse import urlparse
from zipfile import ZipFile, is_zipfile

import requests
from filelock import FileLock
from tqdm.auto import tqdm

from .. import __version__


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

try:
    USE_TF = os.environ.get("USE_TF", "AUTO").upper()
    USE_TORCH = os.environ.get("USE_TORCH", "AUTO").upper()
    if USE_TORCH in ("1", "ON", "YES", "AUTO") and USE_TF not in ("1", "ON", "YES"):
        import torch

        _torch_available = True  # pylint: disable=invalid-name
        logger.info("PyTorch version {} available.".format(torch.__version__))
    else:
        logger.info("Disabling PyTorch because USE_TF is set")
        _torch_available = False
except ImportError:
    _torch_available = False  # pylint: disable=invalid-name

try:
    USE_TF = os.environ.get("USE_TF", "AUTO").upper()
    USE_TORCH = os.environ.get("USE_TORCH", "AUTO").upper()

    if USE_TF in ("1", "ON", "YES", "AUTO") and USE_TORCH not in ("1", "ON", "YES"):
        import tensorflow as tf

        assert hasattr(tf, "__version__") and int(tf.__version__[0]) >= 2
        _tf_available = True  # pylint: disable=invalid-name
        logger.info("TensorFlow version {} available.".format(tf.__version__))
    else:
        logger.info("Disabling Tensorflow because USE_TORCH is set")
        _tf_available = False
except (ImportError, AssertionError):
    _tf_available = False  # pylint: disable=invalid-name


hf_cache_home = os.path.expanduser(
    os.getenv("HF_HOME", os.path.join(os.getenv("XDG_CACHE_HOME", "~/.cache"), "huggingface"))
)
default_datasets_cache_path = os.path.join(hf_cache_home, "datasets")
try:
    from pathlib import Path

    HF_DATASETS_CACHE = Path(os.getenv("HF_DATASETS_CACHE", default_datasets_cache_path))
except (AttributeError, ImportError):
    HF_DATASETS_CACHE = os.getenv(os.getenv("HF_DATASETS_CACHE", default_datasets_cache_path))

S3_DATASETS_BUCKET_PREFIX = "https://s3.amazonaws.com/datasets.huggingface.co/nlp/datasets"
CLOUDFRONT_DATASETS_DISTRIB_PREFIX = "https://cdn-datasets.huggingface.co/nlp/datasets"


default_metrics_cache_path = os.path.join(hf_cache_home, "metrics")
try:
    from pathlib import Path

    HF_METRICS_CACHE = Path(os.getenv("HF_METRICS_CACHE", default_metrics_cache_path))
except (AttributeError, ImportError):
    HF_METRICS_CACHE = os.getenv(os.getenv("HF_METRICS_CACHE", default_metrics_cache_path))

S3_METRICS_BUCKET_PREFIX = "https://s3.amazonaws.com/datasets.huggingface.co/nlp/metrics"
CLOUDFRONT_METRICS_DISTRIB_PREFIX = "https://cdn-datasets.huggingface.co/nlp/metric"

INCOMPLETE_SUFFIX = ".incomplete"


def is_torch_available():
    return _torch_available


def is_tf_available():
    return _tf_available


def is_remote_url(url_or_filename):
    parsed = urlparse(url_or_filename)
    return parsed.scheme in ("http", "https", "s3", "gs", "hdfs")


def hf_bucket_url(identifier: str, filename: str, use_cdn=False, dataset=True) -> str:
    if dataset:
        endpoint = CLOUDFRONT_DATASETS_DISTRIB_PREFIX if use_cdn else S3_DATASETS_BUCKET_PREFIX
    else:
        endpoint = CLOUDFRONT_METRICS_DISTRIB_PREFIX if use_cdn else S3_METRICS_BUCKET_PREFIX
    return "/".join((endpoint, identifier, filename))


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
    """ Configuration for our cached path manager
    Args:
        cache_dir: specify a cache directory to save the file to (overwrite the default cache dir).
        force_download: if True, re-dowload the file even if it's already cached in the cache dir.
        resume_download: if True, resume the download if incompletly recieved file is found.
        user_agent: Optional string or dict that will be appended to the user-agent on remote requests.
        extract_compressed_file: if True and the path point to a zip or tar file, extract the compressed
            file in a folder along the archive.
        force_extract: if True when extract_compressed_file is True and the archive was already extracted,
            re-extract the archive and overide the folder where it was extracted.


    """

    cache_dir: Optional[Union[str, Path]] = None
    force_download: bool = False
    resume_download: bool = False
    local_files_only: bool = False
    proxies: Optional[Dict] = None
    user_agent: Optional[str] = None
    extract_compressed_file: bool = False
    force_extract: bool = False


def cached_path(url_or_filename, download_config=None, **download_kwargs,) -> Optional[str]:
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
    """
    if download_config is None:
        download_config = DownloadConfig(**download_kwargs)

    cache_dir = download_config.cache_dir or HF_DATASETS_CACHE
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
        )
    elif os.path.exists(url_or_filename):
        # File, and it exists.
        output_path = url_or_filename
    elif urlparse(url_or_filename).scheme == "":
        # File, but it doesn't exist.
        raise FileNotFoundError("Local file {} doesn't exist".format(url_or_filename))
    else:
        # Something unknown
        raise ValueError("unable to parse {} as a URL or as a local path".format(url_or_filename))

    if download_config.extract_compressed_file and output_path is not None:
        if not is_zipfile(output_path) and not tarfile.is_tarfile(output_path) and not is_gzip(output_path):
            return output_path

        # Path where we extract compressed archives
        # We extract in the cache dir, and get the extracted path name by hashing the original path"
        abs_output_path = os.path.abspath(output_path)
        output_path_extracted = os.path.join(cache_dir, "extracted", hash_url_to_filename(abs_output_path))

        if (
            os.path.isdir(output_path_extracted)
            and os.listdir(output_path_extracted)
            and not download_config.force_extract
        ) or (os.path.isfile(output_path_extracted) and not download_config.force_extract):
            return output_path_extracted

        # Prevent parallel extractions
        lock_path = output_path + ".lock"
        with FileLock(lock_path):
            shutil.rmtree(output_path_extracted, ignore_errors=True)
            os.makedirs(output_path_extracted, exist_ok=True)
            if is_zipfile(output_path):
                with ZipFile(output_path, "r") as zip_file:
                    zip_file.extractall(output_path_extracted)
                    zip_file.close()
            elif tarfile.is_tarfile(output_path):
                tar_file = tarfile.open(output_path)
                tar_file.extractall(output_path_extracted)
                tar_file.close()
            elif is_gzip(output_path):
                os.rmdir(output_path_extracted)
                with gzip.open(output_path, "rb") as gzip_file:
                    with open(output_path_extracted, "wb") as extracted_file:
                        shutil.copyfileobj(gzip_file, extracted_file)
            else:
                raise EnvironmentError("Archive format of {} could not be identified".format(output_path))

        return output_path_extracted

    return output_path


def http_get(url, temp_file, proxies=None, resume_size=0, user_agent=None, cookies=None):
    ua = "datasets/{}; python/{}".format(__version__, sys.version.split()[0])
    if is_torch_available():
        ua += "; torch/{}".format(torch.__version__)
    if is_tf_available():
        ua += "; tensorflow/{}".format(tf.__version__)
    if isinstance(user_agent, dict):
        ua += "; " + "; ".join("{}/{}".format(k, v) for k, v in user_agent.items())
    elif isinstance(user_agent, str):
        ua += "; " + user_agent
    headers = {"user-agent": ua}
    if resume_size > 0:
        headers["Range"] = "bytes=%d-" % (resume_size,)
    response = requests.get(url, stream=True, proxies=proxies, headers=headers, cookies=cookies)
    if response.status_code == 416:  # Range not satisfiable
        return
    content_length = response.headers.get("Content-Length")
    total = resume_size + int(content_length) if content_length is not None else None
    progress = tqdm(
        unit="B",
        unit_scale=True,
        total=total,
        initial=resume_size,
        desc="Downloading",
        disable=bool(logger.getEffectiveLevel() == logging.NOTSET),
    )
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:  # filter out keep-alive new chunks
            progress.update(len(chunk))
            temp_file.write(chunk)
    progress.close()


def get_from_cache(
    url,
    cache_dir=None,
    force_download=False,
    proxies=None,
    etag_timeout=10,
    resume_download=False,
    user_agent=None,
    local_files_only=False,
) -> Optional[str]:
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
        cache_dir = HF_DATASETS_CACHE
    if isinstance(cache_dir, Path):
        cache_dir = str(cache_dir)

    os.makedirs(cache_dir, exist_ok=True)

    original_url = url  # Some parameters may be added
    connected = False
    cookies = None
    etag = None
    if not local_files_only:
        try:
            response = requests.head(url, allow_redirects=True, proxies=proxies, timeout=etag_timeout)
            if response.status_code == 200:  # ok
                etag = response.headers.get("ETag")
                for k, v in response.cookies.items():
                    # In some edge cases, we need to get a confirmation token
                    if k.startswith("download_warning") and "drive.google.com" in url:
                        url += "&confirm=" + v
                        cookies = response.cookies
                connected = True
            # In some edge cases, head request returns 400 but the connection is actually ok
            elif (response.status_code == 400 and "firebasestorage.googleapis.com" in url) or (
                response.status_code == 405 and "drive.google.com" in url
            ):
                connected = True
                logger.info("Couldn't get ETag version for url {}".format(url))
        except (EnvironmentError, requests.exceptions.Timeout):
            # not connected
            pass

    filename = hash_url_to_filename(original_url, etag)

    # get cache path to put the file
    cache_path = os.path.join(cache_dir, filename)

    # connected == False = we don't have a connection, or url doesn't exist, or is otherwise inaccessible.
    # try to get the last downloaded one
    if not connected:
        if os.path.exists(cache_path):
            return cache_path
        if local_files_only:
            raise FileNotFoundError(
                "Cannot find the requested files in the cached path and outgoing traffic has been"
                " disabled. To enable model look-ups and downloads online, set 'local_files_only'"
                " to False."
            )
        raise ConnectionError("Couldn't reach {}".format(url))

    # From now on, connected is True.
    if os.path.exists(cache_path) and not force_download:
        return cache_path

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
            http_get(url, temp_file, proxies=proxies, resume_size=resume_size, user_agent=user_agent, cookies=cookies)

        logger.info("storing %s in cache at %s", url, cache_path)
        shutil.move(temp_file.name, cache_path)

        logger.info("creating metadata file for %s", cache_path)
        meta = {"url": url, "etag": etag}
        meta_path = cache_path + ".json"
        with open(meta_path, "w") as meta_file:
            json.dump(meta, meta_file)

    return cache_path


def is_gzip(path: str) -> bool:
    """from https://stackoverflow.com/a/60634210"""
    with gzip.open(path, "r") as fh:
        try:
            fh.read(1)
            return True
        except OSError:
            return False
