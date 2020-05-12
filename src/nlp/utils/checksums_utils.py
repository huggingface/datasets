import logging
import os
from hashlib import sha256
from typing import Tuple


logger = logging.getLogger(__name__)

URLS_CHECKSUMS_FOLDER_NAME = "urls_checksums"
CHECKSUMS_FILE_NAME = "checksums.txt"
CACHED_SIZES_FILE_NAME = "cached_sizes.txt"


class MissingChecksumsFile(Exception):
    """The checksum file is missing."""


class MissingCachedSizesFile(Exception):
    """The cached sizes file is missing."""


def parse_sizes_checksums(checksums_file) -> dict:
    """
    Returns {URL: (size, checksum)}s stored within given file where
    lines look like: <url> <size> <checksum>
    """
    checksums = {}
    for line in checksums_file:
        line = line.strip()  # Remove `\n` and the trailing '\r' on Windows OS.
        if not line or line.startswith("#"):
            continue
        # URL might have spaces inside, but size and checksum will not.
        url, size, checksum = line.rsplit(" ", 2)
        checksums[url] = (int(size), checksum)
    return checksums


def load_sizes_checksums(checksums_file_path: str) -> dict:
    """
    Load sizes_checksums data from a file.
    The format is one line per (url, size, checksum), formated like this:
    <url> <size> <checksum>

    Args:
        checksums_file_path: the file to load the data from
    """
    sizes_checksums = {}
    if not os.path.isfile(checksums_file_path):
        raise MissingChecksumsFile(checksums_file_path)
    with open(checksums_file_path, "r") as checksums_file:
        sizes_checksums.update(parse_sizes_checksums(checksums_file))
    return sizes_checksums


def store_sizes_checksum(sizes_checksums: dict, path: str, overwrite=False):
    """
    Store sizes_checksums data in a file. You can either overwrite the file if it already exists, or simply complete it.
    The format is one line per (url, size, checksum), formated like this:
    <url> <size> <checksum>

    Args:
        sizes_checksums: `dict` of {url: (size, checksum)} is the data to store
        path: `str` where to store the checksums
        overwrite: if True, the file is overwritten. It is False by default,
            so that previous data are simply completed with the new ones.
            When completing the file, if the checksum of a url in `sizes_checksums`
            already existed, it is replaced by the new one.

    """
    total_sizes_checksums = {}
    if os.path.isfile(path):
        if overwrite:
            logger.info("Checksums file {} already exists. Overwriting it.".format(path))
        else:
            logger.info("Checksums file {} already exists. Completing it with new checksums.".format(path))
            total_sizes_checksums = load_sizes_checksums(path)
    total_sizes_checksums.update(sizes_checksums)
    with open(path, "w") as f:
        f.write("# Checksums: <url> <num_bytes> <sha256>\n")
        for url, (size, checksum) in sorted(total_sizes_checksums.items()):
            f.write("%s %s %s\n" % (url, size, checksum))


def get_size_checksum(path: str) -> Tuple[int, str]:
    """Compute the file size and the sha256 checksum of a file"""
    m = sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            m.update(chunk)
    return os.path.getsize(path), m.hexdigest()


def store_cached_sizes(cached_sizes: dict, path: str, overwrite=False):
    """
    Store cached_sizes data in a file. You can either overwrite the file if it already exists, or simply complete it.
    The format is one line per (full_config_name, num_bytes, num_examples), formated like this:
    <full_config_name> <num_bytes> <num_examples>

    Args:
        cached_sizes: `dict` of {full_config_name: (num_bytes, num_examples)} is the data to store
        path: `str` where to store the sizes
        overwrite: if True, the file is overwritten. It is False by default,
            so that previous data are simply completed with the new ones.
            When completing the file, if the full_config_name of a url in `cached_sizes`
            already existed, it is replaced by the new one.

    """
    total_cached_sizes = {}
    if os.path.isfile(path):
        if overwrite:
            logger.info("Cached sizes file {} already exists. Overwriting it.".format(path))
        else:
            logger.info("Cached sizes file {} already exists. Completing it with new split sizes.".format(path))
            total_cached_sizes = load_cached_sizes(path)
    total_cached_sizes.update(cached_sizes)
    with open(path, "w") as f:
        f.write("# Cached sizes: <full_config_name> <num_bytes> <num_examples>\n")
        for full_config_name, (size, num_examples) in sorted(total_cached_sizes.items()):
            f.write("%s %s %s\n" % (full_config_name, size, num_examples))


def load_cached_sizes(cached_sizes_file_path: str) -> dict:
    """
    Load cached_sizes data from a file.
    The format is one line per (full_config_name, num_bytes, num_examples), formated like this:
    <full_config_name> <num_bytes> <num_examples>

    Args:
        cached_sizes_file_path: the file to load the data from
    """
    cached_sizes = {}
    if not os.path.isfile(cached_sizes_file_path):
        raise MissingCachedSizesFile(cached_sizes_file_path)
    with open(cached_sizes_file_path, "r") as cached_sizes_file:
        cached_sizes.update(parse_cached_sizes(cached_sizes_file))
    return cached_sizes


def parse_cached_sizes(cached_sizes_file) -> dict:
    """
    Returns {full_config_name: (size, num_examples)}s stored within given file where
    lines look like: <full_config_name> <num_bytes> <num_examples>
    """
    cached_sizes = {}
    for line in cached_sizes_file:
        line = line.strip()  # Remove `\n` and the trailing '\r' on Windows OS.
        if not line or line.startswith("#"):
            continue
        # config names might have spaces inside, but size and checksum will not.
        full_config_name, size, num_examples = line.rsplit(" ", 2)
        cached_sizes[full_config_name] = (int(size), int(num_examples))
    return cached_sizes
