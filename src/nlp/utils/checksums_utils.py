import os
from hashlib import sha256
from typing import Tuple

URLS_CHECKSUMS_FOLDER_NAME = "urls_checksums"
CHECKSUMS_FILE_NAME = "checksums.txt"


class MissingChecksumsFile(Exception):
  """The checksum file is missing."""


def parse_sizes_checksums(checksums_file) -> dict:
    """Returns {URL: (size, checksum)}s stored within given file."""
    checksums = {}
    for line in checksums_file:
        line = line.strip()  # Remove the trailing '\r' on Windows OS.
        if not line or line.startswith('#'):
            continue
        # URL might have spaces inside, but size and checksum will not.
        url, size, checksum = line.rsplit(' ', 2)
        checksums[url] = (int(size), checksum)
    return checksums


def load_sizes_checksums(checksums_path) -> dict:
    sizes_checksums = {}
    if not os.path.isfile(checksums_path):
        raise MissingChecksumsFile(checksums_path)
    with open(checksums_path, "r") as checksums_file:
        sizes_checksums.update(parse_sizes_checksums(checksums_file))
    return sizes_checksums


def store_sizes_checksum(sizes_checksums: dict, path: str):
    with open(path, 'w') as f:
        for url, (size, checksum) in sorted(sizes_checksums.items()):
            f.write('%s %s %s\n' % (url, size, checksum))


def get_size_checksum(path: str) -> Tuple[int, str]:
    m = sha256()
    with open(path, 'rb') as f: 
            for chunk in iter(lambda: f.read(4096),b""):
                m.update(chunk)
    return os.path.getsize(path), m.hexdigest()
