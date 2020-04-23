# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Classes to specify download or extraction information."""

import base64
import codecs
import enum
import hashlib
import itertools
import json
import os
import re
import urllib

from ..utils import py_utils
from . import util

_hex_codec = codecs.getdecoder("hex_codec")


def _decode_hex(hexstr):
    """Returns binary digest, given str hex digest."""
    return _hex_codec(hexstr)[0]


class ExtractMethod(enum.Enum):
    """The extraction method to use to pre-process a downloaded file."""

    NO_EXTRACT = 1
    TAR = 2
    TAR_GZ = 3  # Deprecated: use TAR.
    GZIP = 4
    ZIP = 5
    BZIP2 = 6
    TAR_STREAM = 7
    TAR_GZ_STREAM = 8  # Deprecated: use TAR_STREAM


_EXTRACTION_METHOD_TO_EXTS = [
    (ExtractMethod.TAR_GZ, [".tar.gz", ".tgz"]),
    (ExtractMethod.TAR, [".tar", ".tar.bz2", ".tbz2", ".tbz", ".tb2"]),
    (ExtractMethod.ZIP, [".zip"]),
    (ExtractMethod.GZIP, [".gz"]),
    (ExtractMethod.BZIP2, [".bz2"]),
]

_KNOWN_EXTENSIONS = [
    ext_
    for ext_ in itertools.chain(  # pylint: disable=g-complex-comprehension
        *[extensions_ for _, extensions_ in _EXTRACTION_METHOD_TO_EXTS]
    )
]

_NETLOC_COMMON_PREFIXES = [
    "www.",
    "storage.googleapis.com",
    "drive.google.com",
    "github.com",
]

_NETLOC_COMMON_SUFFIXES = [
    ".github.io",
    ".s3-website.eu-central-1.amazonaws.com",
    ".amazonaws.com",  # Must be kept after the other amazonaws.com subdomains.
]

_URL_COMMON_PARTS = [
    "_data_",
    "_dataset_",
    "_static_",
    "_of_",
    "-of-",
]


def _guess_extract_method(fname):
    """Guess extraction method, given file name (or path)."""
    for method, extensions in _EXTRACTION_METHOD_TO_EXTS:
        for ext in extensions:
            if fname.endswith(ext):
                return method
    return ExtractMethod.NO_EXTRACT


def _sanitize_url(url, max_length):
    """Sanitize and shorten url to fit in max_length.

	Function is stable: same input MUST ALWAYS give same result, accros changes
	in code as well. Different URLs might give same result.
	As much as possible, the extension should be kept.

	Heuristics are applied to only keep useful info from url.

	1- Drop generic [sub]domains.
		'www.cs.toronto.edu/...' -> 'cs.toronto.edu/...'
		'storage.googleapis.com/foo/...' -> 'foo/...'
		'drive.google.com/bar/...' -> 'bar/...'
		'github.com/baz/...' -> 'baz/...'

	2- Remove leading '0's from url components:
		'foo/train-00004-of-00010.tfrecords' -> 'foo/train-4-of-10.tfrecords'

	3- Truncate each component of url until total size fits or each component is
		 left with 4 chars (or total size is <= limit):
		 'MoveUnitToBorder_64x64_png/train-4-of-10.tfrecords'
		 (here truncate components to 4 chars per component max)
			-> 'Move_64x6_png/trai-4-of-10.tfrecords'

	4- Truncate result, keeping prefix: 'abc_def_ghi_jkl' -> 'abc_def'

	Args:
		url: string, url to sanitize and shorten.
		max_length: int, max length of result.

	Returns:
		(string, string): sanitized and shorted url, file extension.
	"""
    url = urllib.parse.urlparse(url)
    netloc = url.netloc
    for prefix in _NETLOC_COMMON_PREFIXES:
        if netloc.startswith(prefix):
            netloc = netloc[len(prefix) :]
    for suffix in _NETLOC_COMMON_SUFFIXES:
        if netloc.endswith(suffix):
            netloc = netloc[: -len(suffix)]
    url = "%s%s%s%s" % (netloc, url.path, url.params, url.query)
    # Get the extension:
    for ext in _KNOWN_EXTENSIONS:
        if url.endswith(ext):
            extension = ext
            url = url[: -len(extension)]
            break
    else:
        url, extension = os.path.splitext(url)
    max_length -= len(extension)
    # Replace non authorized chars (including '/') by '_':
    url = re.sub(r"[^a-zA-Z0-9\.\-_]+", "_", url)
    # Remove parts with no info:
    for common_part in _URL_COMMON_PARTS:
        url = url.replace(common_part, "_")
    url = url.strip("_")
    # Remove leading zeros in groups of numbers:
    url = re.sub("(?<![0-9])0+(?=[0-9])", "", url)
    # Decrease max size of URL components:
    c_size = max(len(c) for c in re.split(r"[\.\-_]", url))
    while c_size > 4 and len(url) > max_length:
        c_size -= 1
        url = re.sub(r"[^\.\-_]{4,}", lambda match: match.group(0)[:c_size], url)
    return url[:max_length], extension


def get_dl_fname(url, checksum):
    """Returns name of file for (url, checksum).

	The max length of linux and windows filenames is 255 chars.
	Windows however expects short paths (260 chars), so we limit the file name
	to an arbitrary 90 chars.

	Naming pattern: '{url}{checksum}'.
	 - url: url sanitized and shortened to 46 chars.
	 - checksum: base64url encoded sha256: 44 chars (removing trailing '=').

	Args:
		url: `str`, url of the file.
		checksum: `str` (hex), the sha256 hexdigest of file or url.

	Returns:
		string of 90 chars max.
	"""
    checksum = base64.urlsafe_b64encode(_decode_hex(checksum))
    checksum = str(checksum)[:-1]
    name, extension = _sanitize_url(url, max_length=46)
    return "%s%s%s" % (name, checksum, extension)


def get_dl_dirname(url):
    """Returns name of temp dir for given url."""
    checksum = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return get_dl_fname(url, checksum)


def _get_info_path(path):
    """Returns path (`str`) of INFO file associated with resource at path."""
    return "%s.INFO" % path


def _read_info(info_path):
    """Returns info dict or None."""
    if not os.path.exists(info_path):
        return None
    with open(info_path) as info_f:
        return json.load(info_f)


# TODO(pierrot): one lock per info path instead of locking everything.
@util.build_synchronize_decorator()
def write_info_file(resource, path, dataset_name, original_fname):
    """Write the INFO file next to local file.

	Although the method is synchronized, there is still a risk two processes
	running at the same time overlap here. Risk accepted, since potentially lost
	data (`dataset_name`) is only for human consumption.

	Args:
		resource: resource for which to write the INFO file.
		path: path of downloaded file.
		dataset_name: data used to dl the file.
		original_fname: name of file as downloaded.
	"""
    info_path = _get_info_path(path)
    info = _read_info(info_path) or {}
    urls = set(info.get("urls", []) + [resource.url])
    dataset_names = info.get("dataset_names", [])
    if dataset_name:
        dataset_names.append(dataset_name)
    if "original_fname" in info and info["original_fname"] != original_fname:
        raise AssertionError(
            '`original_fname` "%s" stored in %s does NOT match "%s".'
            % (info["original_fname"], info_path, original_fname)
        )
    info = dict(urls=list(urls), dataset_names=list(set(dataset_names)), original_fname=original_fname)
    with py_utils.atomic_write(info_path, "w") as info_f:
        json.dump(info, info_f, sort_keys=True)


def get_extract_method(path):
    """Returns `ExtractMethod` to use on resource at path. Cannot be None."""
    info_path = _get_info_path(path)
    info = _read_info(info_path)
    fname = info.get("original_fname", path) if info else path
    return _guess_extract_method(fname)


class Resource(object):
    """Represents a resource to download, extract, or both."""

    def __init__(self, url=None, extract_method=None, path=None):
        """Resource constructor.

		Args:
			url: `str`, the URL at which to download the resource.
			extract_method: `ExtractMethod` to be used to extract resource. If
				not set, will be guessed from downloaded file name `original_fname`.
			path: `str`, path of resource on local disk. Can be None if resource has
				not be downloaded yet. In such case, `url` must be set.
		"""
        self.url = url
        self.path = path
        self._extract_method = extract_method

    @classmethod
    def exists_locally(cls, path):
        """Returns whether the resource exists locally, at `resource.path`."""
        # If INFO file doesn't exist, consider resource does NOT exist, as it would
        # prevent guessing the `extract_method`.
        return os.path.exists(path) and os.path.exists(_get_info_path(path))

    @property
    def extract_method(self):
        """Returns `ExtractMethod` to use on resource. Cannot be None."""
        if self._extract_method:
            return self._extract_method
        return get_extract_method(self.path)
