import os
import re
from functools import partial
from pathlib import Path, PurePath
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

import huggingface_hub
from fsspec import get_fs_token_paths
from huggingface_hub import HfApi, HfFileSystem
from tqdm.contrib.concurrent import thread_map

from .download.streaming_download_manager import xbasename
from .splits import Split
from .utils import logging
from .utils.file_utils import is_relative_path
from .utils.py_utils import string_to_dict


SANITIZED_DEFAULT_SPLIT = str(Split.TRAIN)


logger = logging.get_logger(__name__)


class Url(str):
    pass


class EmptyDatasetError(FileNotFoundError):
    pass


SPLIT_PATTERN_SHARDED = "data/{split}-[0-9][0-9][0-9][0-9][0-9]-of-[0-9][0-9][0-9][0-9][0-9]*.*"

SPLIT_KEYWORDS = {
    Split.TRAIN: ["train", "training"],
    Split.VALIDATION: ["validation", "valid", "dev", "val"],
    Split.TEST: ["test", "testing", "eval", "evaluation"],
}
NON_WORDS_CHARS = "-._ 0-9"
KEYWORDS_IN_FILENAME_BASE_PATTERNS = ["**[{sep}/]{keyword}[{sep}]*", "{keyword}[{sep}]*"]
KEYWORDS_IN_DIR_NAME_BASE_PATTERNS = ["{keyword}[{sep}/]**", "**[{sep}/]{keyword}[{sep}/]**"]

DEFAULT_SPLITS = [Split.TRAIN, Split.VALIDATION, Split.TEST]
DEFAULT_PATTERNS_SPLIT_IN_FILENAME = {
    split: [
        pattern.format(keyword=keyword, sep=NON_WORDS_CHARS)
        for keyword in SPLIT_KEYWORDS[split]
        for pattern in KEYWORDS_IN_FILENAME_BASE_PATTERNS
    ]
    for split in DEFAULT_SPLITS
}
DEFAULT_PATTERNS_SPLIT_IN_DIR_NAME = {
    split: [
        pattern.format(keyword=keyword, sep=NON_WORDS_CHARS)
        for keyword in SPLIT_KEYWORDS[split]
        for pattern in KEYWORDS_IN_DIR_NAME_BASE_PATTERNS
    ]
    for split in DEFAULT_SPLITS
}

DEFAULT_PATTERNS_ALL = {
    Split.TRAIN: ["**"],
}

ALL_SPLIT_PATTERNS = [SPLIT_PATTERN_SHARDED]
ALL_DEFAULT_PATTERNS = [
    DEFAULT_PATTERNS_SPLIT_IN_DIR_NAME,
    DEFAULT_PATTERNS_SPLIT_IN_FILENAME,
    DEFAULT_PATTERNS_ALL,
]
METADATA_PATTERNS = [
    "metadata.csv",
    "**/metadata.csv",
    "metadata.jsonl",
    "**/metadata.jsonl",
]  # metadata file for ImageFolder and AudioFolder
WILDCARD_CHARACTERS = "*[]"
FILES_TO_IGNORE = ["README.md", "config.json", "dataset_infos.json", "dummy_data.zip", "dataset_dict.json"]


def contains_wildcards(pattern: str) -> bool:
    return any(wilcard_character in pattern for wilcard_character in WILDCARD_CHARACTERS)


def sanitize_patterns(patterns: Union[Dict, List, str]) -> Dict[str, Union[List[str], "DataFilesList"]]:
    """
    Take the data_files patterns from the user, and format them into a dictionary.
    Each key is the name of the split, and each value is a list of data files patterns (paths or urls).
    The default split is "train".

    Returns:
        patterns: dictionary of split_name -> list_of _atterns
    """
    if isinstance(patterns, dict):
        return {str(key): value if isinstance(value, list) else [value] for key, value in patterns.items()}
    elif isinstance(patterns, str):
        return {SANITIZED_DEFAULT_SPLIT: [patterns]}
    elif isinstance(patterns, list):
        return {SANITIZED_DEFAULT_SPLIT: patterns}
    else:
        return {SANITIZED_DEFAULT_SPLIT: list(patterns)}


def _is_inside_unrequested_special_dir(matched_rel_path: str, pattern: str) -> bool:
    """
    When a path matches a pattern, we additionnally check if it's inside a special directory
    we ignore by default (if it starts with a double underscore).

    Users can still explicitly request a filepath inside such a directory if "__pycache__" is
    mentioned explicitly in the requested pattern.

    Some examples:

    base directory:

        ./
        └── __pycache__
            └── b.txt

    >>> _is_inside_unrequested_special_dir("__pycache__/b.txt", "**")
    True
    >>> _is_inside_unrequested_special_dir("__pycache__/b.txt", "*/b.txt")
    True
    >>> _is_inside_unrequested_special_dir("__pycache__/b.txt", "__pycache__/*")
    False
    >>> _is_inside_unrequested_special_dir("__pycache__/b.txt", "__*/*")
    False
    """
    # We just need to check if every special directories from the path is present explicly in the pattern.
    # Since we assume that the path matches the pattern, it's equivalent to counting that both
    # the parent path and the parent pattern have the same number of special directories.
    data_dirs_to_ignore_in_path = [part for part in PurePath(matched_rel_path).parent.parts if part.startswith("__")]
    data_dirs_to_ignore_in_pattern = [part for part in PurePath(pattern).parent.parts if part.startswith("__")]
    return len(data_dirs_to_ignore_in_path) != len(data_dirs_to_ignore_in_pattern)


def _is_unrequested_hidden_file_or_is_inside_unrequested_hidden_dir(matched_rel_path: str, pattern: str) -> bool:
    """
    When a path matches a pattern, we additionnally check if it's a hidden file or if it's inside
    a hidden directory we ignore by default, i.e. if the file name or a parent directory name starts with a dot.

    Users can still explicitly request a filepath that is hidden or is inside a hidden directory
    if the hidden part is mentioned explicitly in the requested pattern.

    Some examples:

    base directory:

        ./
        └── .hidden_file.txt

    >>> _is_unrequested_hidden_file_or_is_inside_unrequested_hidden_dir(".hidden_file.txt", "**")
    True
    >>> _is_unrequested_hidden_file_or_is_inside_unrequested_hidden_dir(".hidden_file.txt", ".*")
    False

    base directory:

        ./
        └── .hidden_dir
            └── a.txt

    >>> _is_unrequested_hidden_file_or_is_inside_unrequested_hidden_dir(".hidden_dir/a.txt", "**")
    True
    >>> _is_unrequested_hidden_file_or_is_inside_unrequested_hidden_dir(".hidden_dir/a.txt", ".*/*")
    False
    >>> _is_unrequested_hidden_file_or_is_inside_unrequested_hidden_dir(".hidden_dir/a.txt", ".hidden_dir/*")
    False

    base directory:

        ./
        └── .hidden_dir
            └── .hidden_file.txt

    >>> _is_unrequested_hidden_file_or_is_inside_unrequested_hidden_dir(".hidden_dir/.hidden_file.txt", "**")
    True
    >>> _is_unrequested_hidden_file_or_is_inside_unrequested_hidden_dir(".hidden_dir/.hidden_file.txt", ".*/*")
    True
    >>> _is_unrequested_hidden_file_or_is_inside_unrequested_hidden_dir(".hidden_dir/.hidden_file.txt", ".*/.*")
    False
    >>> _is_unrequested_hidden_file_or_is_inside_unrequested_hidden_dir(".hidden_dir/.hidden_file.txt", ".hidden_dir/*")
    True
    >>> _is_unrequested_hidden_file_or_is_inside_unrequested_hidden_dir(".hidden_dir/.hidden_file.txt", ".hidden_dir/.*")
    False
    """
    # We just need to check if every hidden part from the path is present explicly in the pattern.
    # Since we assume that the path matches the pattern, it's equivalent to counting that both
    # the path and the pattern have the same number of hidden parts.
    hidden_directories_in_path = [
        part for part in PurePath(matched_rel_path).parts if part.startswith(".") and not set(part) == {"."}
    ]
    hidden_directories_in_pattern = [
        part for part in PurePath(pattern).parts if part.startswith(".") and not set(part) == {"."}
    ]
    return len(hidden_directories_in_path) != len(hidden_directories_in_pattern)


def _get_data_files_patterns(pattern_resolver: Callable[[str], List[str]]) -> Dict[str, List[str]]:
    """
    Get the default pattern from a directory or repository by testing all the supported patterns.
    The first patterns to return a non-empty list of data files is returned.

    In order, it first tests if SPLIT_PATTERN_SHARDED works, otherwise it tests the patterns in ALL_DEFAULT_PATTERNS.
    """
    # first check the split patterns like data/{split}-00000-of-00001.parquet
    for split_pattern in ALL_SPLIT_PATTERNS:
        pattern = split_pattern.replace("{split}", "*")
        data_files = pattern_resolver(pattern)
        if len(data_files) > 0:
            splits: Set[str] = {string_to_dict(p, split_pattern)["split"] for p in data_files}
            sorted_splits = [str(split) for split in DEFAULT_SPLITS if split in splits] + sorted(
                splits - set(DEFAULT_SPLITS)
            )
            return {split: [split_pattern.format(split=split)] for split in sorted_splits}
    # then check the default patterns based on train/valid/test splits
    for patterns_dict in ALL_DEFAULT_PATTERNS:
        non_empty_splits = []
        for split, patterns in patterns_dict.items():
            try:
                for pattern in patterns:
                    data_files = pattern_resolver(pattern)
                    if len(data_files) > 0:
                        non_empty_splits.append(split)
                        break
            except FileNotFoundError:
                pass
        if non_empty_splits:
            return {split: patterns_dict[split] for split in non_empty_splits}
    raise FileNotFoundError(f"Couldn't resolve pattern {pattern} with resolver {pattern_resolver}")


def _get_metadata_files_patterns(pattern_resolver: Callable[[str], List[str]]) -> Dict[str, List[str]]:
    """
    Get the supported metadata patterns from a directory or repository.
    """
    non_empty_patterns = []
    for pattern in METADATA_PATTERNS:
        try:
            metadata_files = pattern_resolver(pattern)
            if len(metadata_files) > 0:
                non_empty_patterns.append(pattern)
        except FileNotFoundError:
            pass
    if non_empty_patterns:
        return non_empty_patterns
    raise FileNotFoundError(f"Couldn't resolve pattern {pattern} with resolver {pattern_resolver}")


def resolve_pattern(
    pattern: str,
    base_path: str,
    allowed_extensions: Optional[List[str]] = None,
    storage_options: Optional[Dict[str, Any]] = None,
) -> List[str]:
    if is_relative_path(pattern):
        pattern = base_path + "/" + pattern
    else:
        base_path = os.path.splitdrive(pattern)[0] + "/"
    fs, _, (fs_base_path,) = get_fs_token_paths(base_path, storage_options=storage_options)
    protocol_prefix = fs.protocol + "://" if fs.protocol != "file" else ""
    files_to_ignore = set(FILES_TO_IGNORE) - set(xbasename(pattern))
    matched_paths = [
        protocol_prefix + filepath
        for filepath in fs.glob(pattern)
        if fs.isfile(filepath)
        and (xbasename(filepath) not in files_to_ignore)
        and not _is_inside_unrequested_special_dir(
            os.path.relpath(filepath, fs_base_path), os.path.relpath(pattern, fs_base_path)
        )
        and not _is_unrequested_hidden_file_or_is_inside_unrequested_hidden_dir(
            os.path.relpath(filepath, fs_base_path), os.path.relpath(pattern, fs_base_path)
        )
    ]  # ignore .ipynb and __pycache__, but keep /../
    if allowed_extensions is not None:
        out = [
            filepath
            for filepath in matched_paths
            if any("." + suffix in allowed_extensions for suffix in xbasename(filepath).split("."))
        ]
        if len(out) < len(matched_paths):
            invalid_matched_files = list(set(matched_paths) - set(out))
            logger.info(
                f"Some files matched the pattern '{pattern}' at {base_path} but don't have valid data file extensions: {invalid_matched_files}"
            )
    else:
        out = matched_paths
    if not out and not contains_wildcards(pattern):
        error_msg = f"Unable to find '{pattern}' at {base_path}"
        if allowed_extensions is not None:
            error_msg += f" with any supported extension {list(allowed_extensions)}"
        raise FileNotFoundError(error_msg)
    return out


def get_data_patterns(base_path: str, storage_options: Optional[Dict[str, Any]] = None) -> Dict[str, List[str]]:
    """
    Get the default pattern from a directory testing all the supported patterns.
    The first patterns to return a non-empty list of data files is returned.

    Some examples of supported patterns:

    Input:

        my_dataset_repository/
        ├── README.md
        └── dataset.csv

    Output:

        {"train": ["**"]}

    Input:

        my_dataset_repository/
        ├── README.md
        ├── train.csv
        └── test.csv

        my_dataset_repository/
        ├── README.md
        └── data/
            ├── train.csv
            └── test.csv

        my_dataset_repository/
        ├── README.md
        ├── train_0.csv
        ├── train_1.csv
        ├── train_2.csv
        ├── train_3.csv
        ├── test_0.csv
        └── test_1.csv

    Output:

        {"train": [**train*], "test": ["**test*"]}

    Input:

        my_dataset_repository/
        ├── README.md
        └── data/
            ├── train/
            │   ├── shard_0.csv
            │   ├── shard_1.csv
            │   ├── shard_2.csv
            │   └── shard_3.csv
            └── test/
                ├── shard_0.csv
                └── shard_1.csv

    Output:

        {"train": ["**train*/**"], "test": ["**test*/**"]}

    Input:

        my_dataset_repository/
        ├── README.md
        └── data/
            ├── train-00000-of-00003.csv
            ├── train-00001-of-00003.csv
            ├── train-00002-of-00003.csv
            ├── test-00000-of-00001.csv
            ├── random-00000-of-00003.csv
            ├── random-00001-of-00003.csv
            └── random-00002-of-00003.csv

    Output:

        {
            "train": ["data/train-[0-9][0-9][0-9][0-9][0-9]-of-[0-9][0-9][0-9][0-9][0-9].*"],
            "test": ["data/test-[0-9][0-9][0-9][0-9][0-9]-of-[0-9][0-9][0-9][0-9][0-9].*"],
            "random": ["data/random-[0-9][0-9][0-9][0-9][0-9]-of-[0-9][0-9][0-9][0-9][0-9].*"],
        }

    In order, it first tests if SPLIT_PATTERN_SHARDED works, otherwise it tests the patterns in ALL_DEFAULT_PATTERNS.
    """
    resolver = partial(resolve_pattern, base_path=base_path, storage_options=storage_options)
    try:
        return _get_data_files_patterns(resolver)
    except FileNotFoundError:
        raise EmptyDatasetError(f"The directory at {base_path} doesn't contain any data files") from None


def get_metadata_patterns(base_path: str, storage_options: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    Get the supported metadata patterns from a local directory.
    """
    resolver = partial(resolve_pattern, base_path=base_path, storage_options=storage_options)
    try:
        return _get_metadata_files_patterns(resolver)
    except FileNotFoundError:
        raise FileNotFoundError(f"The directory at {base_path} doesn't contain any metadata file") from None


def _get_single_origin_metadata(
    data_file: str,
    storage_options: Optional[Dict[str, Any]] = None,
    hf_repos_sha_cache: Optional[dict] = None,
) -> Tuple[str]:
    hf_repos_sha_cache = {} if hf_repos_sha_cache is None else hf_repos_sha_cache
    fs, _, _ = get_fs_token_paths(data_file, storage_options=storage_options)
    if isinstance(fs, HfFileSystem):
        resolved_path = fs.resolve_path(data_file)
        hf_repos_sha_cache_key = (resolved_path.repo_type, resolved_path.repo_id, resolved_path.revision)
        if hf_repos_sha_cache_key not in hf_repos_sha_cache:
            repo_info = HfApi(endpoint=fs.endpoint, token=fs.token).repo_info(
                resolved_path.repo_id, revision=resolved_path.revision, repo_type=resolved_path.repo_type
            )
            hf_repos_sha_cache[hf_repos_sha_cache_key] = (repo_info.id, repo_info.sha)
        return hf_repos_sha_cache[hf_repos_sha_cache_key]
    info = fs.info(data_file)
    # s3fs uses "ETag", gcsfs uses "etag", and for local we simply check mtime
    for key in ["ETag", "etag", "mtime"]:
        if key in info:
            return (str(info[key]),)
    return ()


def _get_origin_metadata(
    data_files: List[str],
    max_workers=64,
    storage_options: Optional[Dict[str, Any]] = None,
) -> Tuple[str]:
    return thread_map(
        partial(_get_single_origin_metadata, storage_options=storage_options, hf_repos_sha_cache={}),
        data_files,
        max_workers=max_workers,
        tqdm_class=logging.tqdm,
        desc="Resolving data files",
        disable=len(data_files) <= 16 or not logging.is_progress_bar_enabled(),
    )


class DataFilesList(List[str]):
    """
    List of data files (absolute local paths or URLs).
    It has two construction methods given the user's data files patterns :
    - ``from_hf_repo``: resolve patterns inside a dataset repository
    - ``from_local_or_remote``: resolve patterns from a local path

    Moreover DataFilesList has an additional attribute ``origin_metadata``.
    It can store:
    - the last modified time of local files
    - ETag of remote files
    - commit sha of a dataset repository

    Thanks to this additional attribute, it is possible to hash the list
    and get a different hash if and only if at least one file changed.
    This is useful for caching Dataset objects that are obtained from a list of data files.
    """

    def __init__(self, data_files: List[str], origin_metadata: List[Tuple[str]]):
        super().__init__(data_files)
        self.origin_metadata = origin_metadata

    @classmethod
    def from_hf_repo(
        cls,
        patterns: List[str],
        dataset_info: huggingface_hub.hf_api.DatasetInfo,
        base_path: Optional[str] = None,
        allowed_extensions: Optional[List[str]] = None,
        token: Optional[Union[bool, str]] = None,
    ) -> "DataFilesList":
        base_path = f"hf://datasets/{dataset_info.id}@{dataset_info.sha}/{base_path or ''}".rstrip("/")
        storage_options = {"hf": {"token": token}}
        return cls.from_patterns(
            patterns, base_path=base_path, allowed_extensions=allowed_extensions, storage_options=storage_options
        )

    @classmethod
    def from_local_or_remote(
        cls,
        patterns: List[str],
        base_path: Optional[str] = None,
        allowed_extensions: Optional[List[str]] = None,
        token: Optional[Union[bool, str]] = None,
    ) -> "DataFilesList":
        base_path = base_path if base_path is not None else Path().resolve().as_posix()
        storage_options = {"hf": {"token": token}}
        return cls.from_patterns(
            patterns, base_path=base_path, allowed_extensions=allowed_extensions, storage_options=storage_options
        )

    @classmethod
    def from_patterns(
        cls,
        patterns: List[str],
        base_path: Optional[str] = None,
        allowed_extensions: Optional[List[str]] = None,
        storage_options: Optional[Dict[str, Any]] = None,
    ) -> "DataFilesList":
        base_path = base_path if base_path is not None else Path().resolve().as_posix()
        data_files = [
            path
            for pattern in patterns
            for path in resolve_pattern(
                pattern, base_path=base_path, allowed_extensions=allowed_extensions, storage_options=storage_options
            )
        ]
        origin_metadata = _get_origin_metadata(data_files, storage_options=storage_options)
        return cls(data_files, origin_metadata)

    def filter_extensions(self, extensions: List[str]) -> "DataFilesList":
        pattern = "|".join("\\" + ext for ext in extensions)
        pattern = re.compile(f".*({pattern})(\\..+)?$")
        return DataFilesList(
            [data_file for data_file in self if pattern.match(data_file)],
            origin_metadata=self.origin_metadata,
        )


class DataFilesDict(Dict[str, DataFilesList]):
    """
    Dict of split_name -> list of data files (absolute local paths or URLs).
    It has two construction methods given the user's data files patterns :
    - ``from_hf_repo``: resolve patterns inside a dataset repository
    - ``from_local_or_remote``: resolve patterns from a local path

    Moreover each list is a DataFilesList. It is possible to hash the dictionary
    and get a different hash if and only if at least one file changed.
    For more info, see ``DataFilesList``.

    This is useful for caching Dataset objects that are obtained from a list of data files.

    Changing the order of the keys of this dictionary also doesn't change its hash.
    """

    @classmethod
    def from_local_or_remote(
        cls,
        patterns: Dict[str, Union[List[str], DataFilesList]],
        base_path: Optional[str] = None,
        allowed_extensions: Optional[List[str]] = None,
        token: Optional[Union[bool, str]] = None,
    ) -> "DataFilesDict":
        out = cls()
        for key, patterns_for_key in patterns.items():
            out[key] = (
                DataFilesList.from_local_or_remote(
                    patterns_for_key,
                    base_path=base_path,
                    allowed_extensions=allowed_extensions,
                    token=token,
                )
                if not isinstance(patterns_for_key, DataFilesList)
                else patterns_for_key
            )
        return out

    @classmethod
    def from_hf_repo(
        cls,
        patterns: Dict[str, Union[List[str], DataFilesList]],
        dataset_info: huggingface_hub.hf_api.DatasetInfo,
        base_path: Optional[str] = None,
        allowed_extensions: Optional[List[str]] = None,
        token: Optional[Union[bool, str]] = None,
    ) -> "DataFilesDict":
        out = cls()
        for key, patterns_for_key in patterns.items():
            out[key] = (
                DataFilesList.from_hf_repo(
                    patterns_for_key,
                    dataset_info=dataset_info,
                    base_path=base_path,
                    allowed_extensions=allowed_extensions,
                    token=token,
                )
                if not isinstance(patterns_for_key, DataFilesList)
                else patterns_for_key
            )
        return out

    @classmethod
    def from_patterns(
        cls,
        patterns: List[str],
        base_path: Optional[str] = None,
        allowed_extensions: Optional[List[str]] = None,
        storage_options: Optional[Dict[str, Any]] = None,
    ) -> "DataFilesList":
        out = cls()
        for key, patterns_for_key in patterns.items():
            out[key] = (
                DataFilesList.from_patterns(
                    patterns_for_key,
                    base_path=base_path,
                    allowed_extensions=allowed_extensions,
                    storage_options=storage_options,
                )
                if not isinstance(patterns_for_key, DataFilesList)
                else patterns_for_key
            )
        return out

    def __reduce__(self):
        """
        To make sure the order of the keys doesn't matter when pickling and hashing:

        >>> from datasets.data_files import DataFilesDict
        >>> from datasets.fingerprint import Hasher
        >>> assert Hasher.hash(DataFilesDict(a=[], b=[])) == Hasher.hash(DataFilesDict(b=[], a=[]))

        """
        return DataFilesDict, (dict(sorted(self.items())),)

    def filter_extensions(self, extensions: List[str]) -> "DataFilesDict":
        out = type(self)()
        for key, data_files_list in self.items():
            out[key] = data_files_list.filter_extensions(extensions)
        return out
