import os
from functools import partial
from pathlib import Path, PurePath
from typing import Callable, Dict, List, Optional, Set, Tuple, Union

import huggingface_hub
from fsspec.implementations.local import LocalFileSystem
from tqdm.contrib.concurrent import thread_map

from datasets.filesystems.hffilesystem import HfFileSystem

from .splits import Split
from .utils import logging
from .utils.file_utils import hf_hub_url, is_remote_url, request_etag
from .utils.py_utils import string_to_dict
from .utils.tqdm_utils import tqdm


DEFAULT_SPLIT = str(Split.TRAIN)


logger = logging.get_logger(__name__)


class Url(str):
    pass


SPLIT_PATTERN_SHARDED = "data/{split}-[0-9][0-9][0-9][0-9][0-9]-of-[0-9][0-9][0-9][0-9][0-9].*"

DEFAULT_PATTERNS_SPLIT_IN_FILENAME = {
    str(Split.TRAIN): ["**train*"],
    str(Split.TEST): ["**test*", "**eval*"],
    str(Split.VALIDATION): ["**dev*", "**valid*"],
}

DEFAULT_PATTERNS_SPLIT_IN_DIR_NAME = {
    str(Split.TRAIN): ["**train*/**"],
    str(Split.TEST): ["**test*/**", "**eval*/**"],
    str(Split.VALIDATION): ["**dev*/**", "**valid*/**"],
}

DEFAULT_PATTERNS_ALL = {
    str(Split.TRAIN): ["**"],
}

ALL_SPLIT_PATTERNS = [SPLIT_PATTERN_SHARDED]
ALL_DEFAULT_PATTERNS = [
    DEFAULT_PATTERNS_SPLIT_IN_FILENAME,
    DEFAULT_PATTERNS_SPLIT_IN_DIR_NAME,
    DEFAULT_PATTERNS_ALL,
]
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
        return {DEFAULT_SPLIT: [patterns]}
    elif isinstance(patterns, list):
        return {DEFAULT_SPLIT: patterns}
    else:
        return {DEFAULT_SPLIT: list(patterns)}


def _get_data_files_patterns(pattern_resolver: Callable[[str], List[PurePath]]) -> Dict[str, List[str]]:
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
            data_files = [p.as_posix() for p in data_files]
            splits: Set[str] = {string_to_dict(p, split_pattern)["split"] for p in data_files}
            return {split: [split_pattern.format(split=split)] for split in splits}
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


def _resolve_single_pattern_locally(
    base_path: str, pattern: str, allowed_extensions: Optional[List[str]] = None
) -> List[Path]:
    """
    Return the absolute paths to all the files that match the given patterns.
    It also supports absolute paths in patterns.
    If an URL is passed, it is returned as is.
    """
    pattern = os.path.join(base_path, pattern)
    data_files_ignore = FILES_TO_IGNORE
    fs = LocalFileSystem()
    glob_iter = [PurePath(filepath) for filepath in fs.glob(pattern) if fs.isfile(filepath)]
    matched_paths = [
        Path(filepath).resolve()
        for filepath in glob_iter
        if filepath.name not in data_files_ignore and not filepath.name.startswith(".")
    ]
    if allowed_extensions is not None:
        out = [
            filepath
            for filepath in matched_paths
            if any(suffix[1:] in allowed_extensions for suffix in filepath.suffixes)
        ]
        if len(out) < len(matched_paths):
            invalid_matched_files = list(set(matched_paths) - set(out))
            logger.info(
                f"Some files matched the pattern '{pattern}' at {Path(base_path).resolve()} but don't have valid data file extensions: {invalid_matched_files}"
            )
    else:
        out = matched_paths
    if not out and not contains_wildcards(pattern):
        error_msg = f"Unable to find '{pattern}' at {Path(base_path).resolve()}"
        if allowed_extensions is not None:
            error_msg += f" with any supported extension {list(allowed_extensions)}"
        raise FileNotFoundError(error_msg)
    return sorted(out)


def resolve_patterns_locally_or_by_urls(
    base_path: str, patterns: List[str], allowed_extensions: Optional[List[str]] = None
) -> List[Union[Path, Url]]:
    """
    Resolve the paths and URLs of the data files from the patterns passed by the user.
    URLs are just returned as is.

    You can use patterns to resolve multiple local files. Here are a few examples:
    - *.csv to match all the CSV files at the first level
    - **.csv to match all the CSV files at any level
    - data/* to match all the files inside "data"
    - data/** to match all the files inside "data" and its subdirectories

    The patterns are resolved using the fsspec glob.
    Here are some behaviors specific to fsspec glob that are different from glob.glob, Path.glob, Path.match or fnmatch:
    - '*' matches only first level items
    - '**' matches all items
    - '**/*' matches all at least second level items

    More generally:
    - '*' matches any character except a forward-slash (to match just the file or directory name)
    - '**' matches any character including a forward-slash /

    Examples:

        >>> import huggingface_hub
        >>> from datasets.data_files import resolve_patterns_locally_or_by_urls
        >>> base_path = "."
        >>> resolve_patterns_locally_or_by_urls(base_path, ["src/**/*.yaml"])
        [PosixPath('/Users/quentinlhoest/Desktop/hf/datasets/src/datasets/utils/resources/readme_structure.yaml')]

    Args:
        base_path (str): Base path to use when resolving relative paths.
        patterns (List[str]): Unix patterns or paths or URLs of the data files to resolve.
            The paths can be absolute or relative to base_path.
        allowed_extensions (Optional[list], optional): White-list of file extensions to use. Defaults to None (all extensions).
            For example: allowed_extensions=["csv", "json", "txt", "parquet"]

    Returns:
        List[Union[Path, Url]]: List of paths or URLs to the local or remote files that match the patterns.
    """
    data_files = []
    for pattern in patterns:
        if is_remote_url(pattern):
            data_files.append(Url(pattern))
        else:
            for path in _resolve_single_pattern_locally(base_path, pattern, allowed_extensions):
                data_files.append(path)

    if not data_files:
        error_msg = f"Unable to resolve any data file that matches '{patterns}' at {Path(base_path).resolve()}"
        if allowed_extensions is not None:
            error_msg += f" with any supported extension {list(allowed_extensions)}"
        raise FileNotFoundError(error_msg)
    return data_files


def get_patterns_locally(base_path: str) -> Dict[str, List[str]]:
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
    resolver = partial(_resolve_single_pattern_locally, base_path)
    try:
        return _get_data_files_patterns(resolver)
    except FileNotFoundError:
        raise FileNotFoundError(f"The directory at {base_path} doesn't contain any data file") from None


def _resolve_single_pattern_in_dataset_repository(
    dataset_info: huggingface_hub.hf_api.DatasetInfo,
    pattern: str,
    allowed_extensions: Optional[list] = None,
) -> List[PurePath]:
    data_files_ignore = FILES_TO_IGNORE
    fs = HfFileSystem(repo_info=dataset_info)
    glob_iter = [PurePath(filepath) for filepath in fs.glob(pattern) if fs.isfile(filepath)]
    matched_paths = [
        filepath
        for filepath in glob_iter
        if filepath.name not in data_files_ignore and not filepath.name.startswith(".")
    ]
    if allowed_extensions is not None:
        out = [
            filepath
            for filepath in matched_paths
            if any(suffix[1:] in allowed_extensions for suffix in filepath.suffixes)
        ]
        if len(out) < len(matched_paths):
            invalid_matched_files = list(set(matched_paths) - set(out))
            logger.info(
                f"Some files matched the pattern {pattern} in dataset repository {dataset_info.id} but don't have valid data file extensions: {invalid_matched_files}"
            )
    else:
        out = matched_paths
    if not out and not contains_wildcards(pattern):
        error_msg = f"Unable to find {pattern} in dataset repository {dataset_info.id}"
        if allowed_extensions is not None:
            error_msg += f" with any supported extension {list(allowed_extensions)}"
        raise FileNotFoundError(error_msg)
    return sorted(out)


def resolve_patterns_in_dataset_repository(
    dataset_info: huggingface_hub.hf_api.DatasetInfo,
    patterns: List[str],
    allowed_extensions: Optional[list] = None,
) -> List[Url]:
    """
    Resolve the URLs of the data files from the patterns passed by the user.

    You can use patterns to resolve multiple files. Here are a few examples:
    - *.csv to match all the CSV files at the first level
    - **.csv to match all the CSV files at any level
    - data/* to match all the files inside "data"
    - data/** to match all the files inside "data" and its subdirectories

    The patterns are resolved using the fsspec glob.
    Here are some behaviors specific to fsspec glob that are different from glob.glob, Path.glob, Path.match or fnmatch:
    - '*' matches only first level items
    - '**' matches all items
    - '**/*' matches all at least second level items

    More generally:
    - '*' matches any character except a forward-slash (to match just the file or directory name)
    - '**' matches any character including a forward-slash /

    Examples:

        >>> import huggingface_hub
        >>> from datasets.data_files import resolve_patterns_in_dataset_repository
        >>> dataset_info = huggingface_hub.HfApi().dataset_info("lhoestq/demo1")
        >>> resolve_patterns_in_dataset_repository(dataset_info, ["data/*.csv"])
        ['https://huggingface.co/datasets/lhoestq/demo1/resolve/0ca0d9f35b390ad11516095aeb27fd30cfe72578/data/test.csv',
        'https://huggingface.co/datasets/lhoestq/demo1/resolve/0ca0d9f35b390ad11516095aeb27fd30cfe72578/data/train.csv']

    Args:
        dataset_info (huggingface_hub.hf_api.DatasetInfo): dataset info obtained using the hugginggace_hub.HfApi
        patterns (List[str]): Unix patterns or paths of the files in the dataset repository.
            The paths should be relative to the root of the repository.
        allowed_extensions (Optional[list], optional): White-list of file extensions to use. Defaults to None (all extensions).
            For example: allowed_extensions=["csv", "json", "txt", "parquet"]

    Returns:
        List[Url]: List of URLs to the files in the dataset repository that match the patterns.
    """
    data_files_urls: List[Url] = []
    for pattern in patterns:
        for rel_path in _resolve_single_pattern_in_dataset_repository(dataset_info, pattern, allowed_extensions):
            data_files_urls.append(Url(hf_hub_url(dataset_info.id, rel_path.as_posix(), revision=dataset_info.sha)))
    if not data_files_urls:
        error_msg = f"Unable to resolve any data file that matches {patterns} in dataset repository {dataset_info.id}"
        if allowed_extensions is not None:
            error_msg += f" with any supported extension {list(allowed_extensions)}"
        raise FileNotFoundError(error_msg)
    return data_files_urls


def get_patterns_in_dataset_repository(dataset_info: huggingface_hub.hf_api.DatasetInfo) -> Dict[str, List[str]]:
    """
    Get the default pattern from a repository by testing all the supported patterns.
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

        {"train": ["**train*"], "test": ["**test*"]}

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
    resolver = partial(_resolve_single_pattern_in_dataset_repository, dataset_info)
    try:
        return _get_data_files_patterns(resolver)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"The dataset repository at '{dataset_info.id}' doesn't contain any data file."
        ) from None


def _get_single_origin_metadata_locally_or_by_urls(
    data_file: Union[Path, Url], use_auth_token: Optional[Union[bool, str]] = None
) -> Tuple[str]:
    if isinstance(data_file, Url):
        data_file = str(data_file)
        return (request_etag(data_file, use_auth_token=use_auth_token),)
    else:
        data_file = str(data_file.resolve())
        return (str(os.path.getmtime(data_file)),)


def _get_origin_metadata_locally_or_by_urls(
    data_files: List[Union[Path, Url]], max_workers=64, use_auth_token: Optional[Union[bool, str]] = None
) -> Tuple[str]:
    return thread_map(
        partial(_get_single_origin_metadata_locally_or_by_urls, use_auth_token=use_auth_token),
        data_files,
        max_workers=max_workers,
        tqdm_class=tqdm,
        desc="Resolving data files",
        disable=len(data_files) <= 16 or logging.get_verbosity() == logging.NOTSET,
    )


class DataFilesList(List[Union[Path, Url]]):
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

    def __init__(self, data_files: List[Union[Path, Url]], origin_metadata: List[Tuple[str]]):
        super().__init__(data_files)
        self.origin_metadata = origin_metadata

    @classmethod
    def from_hf_repo(
        cls,
        patterns: List[str],
        dataset_info: huggingface_hub.hf_api.DatasetInfo,
        allowed_extensions: Optional[List[str]] = None,
    ) -> "DataFilesList":
        data_files = resolve_patterns_in_dataset_repository(dataset_info, patterns, allowed_extensions)
        origin_metadata = [(dataset_info.id, dataset_info.sha) for _ in patterns]
        return cls(data_files, origin_metadata)

    @classmethod
    def from_local_or_remote(
        cls,
        patterns: List[str],
        base_path: Optional[str] = None,
        allowed_extensions: Optional[List[str]] = None,
        use_auth_token: Optional[Union[bool, str]] = None,
    ) -> "DataFilesList":
        base_path = base_path if base_path is not None else str(Path().resolve())
        data_files = resolve_patterns_locally_or_by_urls(base_path, patterns, allowed_extensions)
        origin_metadata = _get_origin_metadata_locally_or_by_urls(data_files, use_auth_token=use_auth_token)
        return cls(data_files, origin_metadata)


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
        use_auth_token: Optional[Union[bool, str]] = None,
    ) -> "DataFilesDict":
        out = cls()
        for key, patterns_for_key in patterns.items():
            out[key] = (
                DataFilesList.from_local_or_remote(
                    patterns_for_key,
                    base_path=base_path,
                    allowed_extensions=allowed_extensions,
                    use_auth_token=use_auth_token,
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
        allowed_extensions: Optional[List[str]] = None,
    ) -> "DataFilesDict":
        out = cls()
        for key, patterns_for_key in patterns.items():
            out[key] = (
                DataFilesList.from_hf_repo(
                    patterns_for_key, dataset_info=dataset_info, allowed_extensions=allowed_extensions
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
