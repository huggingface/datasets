import os
from itertools import chain
from pathlib import Path, PurePath
from unittest.mock import patch

import fsspec
import pytest
from huggingface_hub.hf_api import DatasetInfo

from datasets.data_files import (
    DataFilesDict,
    DataFilesList,
    Url,
    _get_data_files_patterns,
    resolve_patterns_in_dataset_repository,
    resolve_patterns_locally_or_by_urls,
)
from datasets.fingerprint import Hasher
from datasets.utils.file_utils import hf_hub_url


_TEST_PATTERNS = ["*", "**", "**/*", "*.txt", "data/*", "**/*.txt", "**/train.txt"]
_FILES_TO_IGNORE = {".dummy", "README.md", "dummy_data.zip", "dataset_infos.json"}
_TEST_PATTERNS_SIZES = dict(
    [("*", 0), ("**", 2), ("**/*", 2), ("*.txt", 0), ("data/*", 2), ("**/*.txt", 2), ("**/train.txt", 1)]
)

_TEST_URL = "https://raw.githubusercontent.com/huggingface/datasets/9675a5a1e7b99a86f9c250f6ea5fa5d1e6d5cc7d/setup.py"


@pytest.fixture
def complex_data_dir(tmp_path):
    data_dir = tmp_path / "complex_data_dir"
    data_dir.mkdir()
    (data_dir / "data").mkdir()
    with open(data_dir / "data" / "train.txt", "w") as f:
        f.write("foo\n" * 10)
    with open(data_dir / "data" / "test.txt", "w") as f:
        f.write("bar\n" * 10)
    with open(data_dir / "README.md", "w") as f:
        f.write("This is a readme")
    with open(data_dir / ".dummy", "w") as f:
        f.write("this is a dummy file that is not a data file")
    return str(data_dir)


@pytest.fixture
def pattern_results(complex_data_dir):
    # We use fsspec glob as a reference for data files resolution from patterns.
    # This is the same as dask for example.
    #
    # /!\ Here are some behaviors specific to fsspec glob that are different from glob.glob, Path.glob, Path.match or fnmatch:
    # - '*' matches only first level items
    # - '**' matches all items
    # - '**/*' matches all at least second level items
    #
    # More generally:
    # - '*' matches any character except a forward-slash (to match just the file or directory name)
    # - '**' matches any character including a forward-slash /

    return {
        pattern: sorted(
            str(Path(path).resolve())
            for path in fsspec.filesystem("file").glob(os.path.join(complex_data_dir, pattern))
            if Path(path).name not in _FILES_TO_IGNORE and Path(path).is_file()
        )
        for pattern in _TEST_PATTERNS
    }


@pytest.fixture
def hub_dataset_info(complex_data_dir):
    return DatasetInfo(
        siblings=[
            {"rfilename": path.relative_to(complex_data_dir).as_posix()}
            for path in Path(complex_data_dir).rglob("*")
            if path.is_file()
        ],
        sha="foobarfoobar",
        id="foo",
    )


@pytest.fixture
def hub_dataset_info_patterns_results(hub_dataset_info, complex_data_dir, pattern_results):
    return {
        pattern: [
            hf_hub_url(
                hub_dataset_info.id, Path(path).relative_to(complex_data_dir).as_posix(), revision=hub_dataset_info.sha
            )
            for path in pattern_results[pattern]
        ]
        for pattern in pattern_results
    }


@pytest.mark.parametrize("pattern", _TEST_PATTERNS)
def test_pattern_results_fixture(pattern_results, pattern):
    assert len(pattern_results[pattern]) == _TEST_PATTERNS_SIZES[pattern]
    assert all(Path(path).is_file() for path in pattern_results[pattern])


@pytest.mark.parametrize("pattern", _TEST_PATTERNS)
def test_resolve_patterns_locally_or_by_urls(complex_data_dir, pattern, pattern_results):
    try:
        resolved_data_files = resolve_patterns_locally_or_by_urls(complex_data_dir, [pattern])
        assert sorted(str(f) for f in resolved_data_files) == pattern_results[pattern]
        assert all(isinstance(path, Path) for path in resolved_data_files)
    except FileNotFoundError:
        assert len(pattern_results[pattern]) == 0


def test_resolve_patterns_locally_or_by_urls_with_absolute_path(tmp_path, complex_data_dir):
    abs_path = os.path.join(complex_data_dir, "data", "train.txt")
    resolved_data_files = resolve_patterns_locally_or_by_urls(str(tmp_path / "blabla"), [abs_path])
    assert len(resolved_data_files) == 1


@pytest.mark.parametrize("pattern,size,extensions", [("**", 2, ["txt"]), ("**", 2, None), ("**", 0, ["blablabla"])])
def test_resolve_patterns_locally_or_by_urls_with_extensions(complex_data_dir, pattern, size, extensions):
    if size > 0:
        resolved_data_files = resolve_patterns_locally_or_by_urls(
            complex_data_dir, [pattern], allowed_extensions=extensions
        )
        assert len(resolved_data_files) == size
    else:
        with pytest.raises(FileNotFoundError):
            resolve_patterns_locally_or_by_urls(complex_data_dir, pattern, allowed_extensions=extensions)


def test_fail_resolve_patterns_locally_or_by_urls(complex_data_dir):
    with pytest.raises(FileNotFoundError):
        resolve_patterns_locally_or_by_urls(complex_data_dir, ["blablabla"])


def test_resolve_patterns_locally_or_by_urls_sorted_files(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("unsorted_text_files"))
    unsorted_names = ["0.txt", "2.txt", "3.txt"]
    for name in unsorted_names:
        with open(os.path.join(path, name), "w"):
            pass
    resolved_data_files = resolve_patterns_locally_or_by_urls(path, ["*"])
    resolved_names = [os.path.basename(data_file) for data_file in resolved_data_files]
    assert resolved_names == sorted(unsorted_names)


@pytest.mark.parametrize("pattern", _TEST_PATTERNS)
def test_resolve_patterns_in_dataset_repository(hub_dataset_info, pattern, hub_dataset_info_patterns_results):
    try:
        resolved_data_files = resolve_patterns_in_dataset_repository(hub_dataset_info, [pattern])
        assert sorted(str(f) for f in resolved_data_files) == hub_dataset_info_patterns_results[pattern]
        assert all(isinstance(url, Url) for url in resolved_data_files)
    except FileNotFoundError:
        assert len(hub_dataset_info_patterns_results[pattern]) == 0


@pytest.mark.parametrize("pattern,size,extensions", [("**", 2, ["txt"]), ("**", 2, None), ("**", 0, ["blablabla"])])
def test_resolve_patterns_in_dataset_repository_with_extensions(hub_dataset_info, pattern, size, extensions):
    if size > 0:
        resolved_data_files = resolve_patterns_in_dataset_repository(
            hub_dataset_info, [pattern], allowed_extensions=extensions
        )
        assert len(resolved_data_files) == size
    else:
        with pytest.raises(FileNotFoundError):
            resolved_data_files = resolve_patterns_in_dataset_repository(
                hub_dataset_info, [pattern], allowed_extensions=extensions
            )


def test_fail_resolve_patterns_in_dataset_repository(hub_dataset_info):
    with pytest.raises(FileNotFoundError):
        resolve_patterns_in_dataset_repository(hub_dataset_info, "blablabla")


def test_resolve_patterns_in_dataset_repository_sorted_files():
    unsorted_names = ["0.txt", "2.txt", "3.txt"]
    siblings = [{"rfilename": name} for name in unsorted_names]
    datasets_infos = DatasetInfo(id="test_unsorted_files", siblings=siblings, sha="foobar")
    resolved_data_files = resolve_patterns_in_dataset_repository(datasets_infos, ["*"])
    resolved_names = [os.path.basename(data_file) for data_file in resolved_data_files]
    assert resolved_names == sorted(unsorted_names)


@pytest.mark.parametrize("pattern", _TEST_PATTERNS)
def test_DataFilesList_from_hf_repo(hub_dataset_info, hub_dataset_info_patterns_results, pattern):
    try:
        data_files_list = DataFilesList.from_hf_repo([pattern], hub_dataset_info)
        assert sorted(str(f) for f in data_files_list) == hub_dataset_info_patterns_results[pattern]
        assert all(isinstance(url, Url) for url in data_files_list)
        assert len(data_files_list.origin_metadata) > 0
    except FileNotFoundError:
        assert len(hub_dataset_info_patterns_results[pattern]) == 0


@pytest.mark.parametrize("pattern", _TEST_PATTERNS)
def test_DataFilesList_from_local_or_remote(complex_data_dir, pattern_results, pattern):
    try:
        data_files_list = DataFilesList.from_local_or_remote([pattern], complex_data_dir)
        assert sorted(str(f) for f in data_files_list) == pattern_results[pattern]
        assert all(isinstance(path, Path) for path in data_files_list)
        assert len(data_files_list.origin_metadata) > 0
    except FileNotFoundError:
        assert len(pattern_results[pattern]) == 0


def test_DataFilesList_from_local_or_remote_with_extra_files(complex_data_dir, text_file):
    data_files_list = DataFilesList.from_local_or_remote([_TEST_URL, str(text_file)], complex_data_dir)
    assert list(data_files_list) == [Url(_TEST_URL), Path(text_file)]
    assert len(data_files_list.origin_metadata) == 2


@pytest.mark.parametrize("pattern", _TEST_PATTERNS)
def test_DataFilesDict_from_hf_repo(hub_dataset_info, hub_dataset_info_patterns_results, pattern):
    split_name = "train"
    try:
        data_files = DataFilesDict.from_hf_repo({split_name: [pattern]}, hub_dataset_info)
        assert all(isinstance(data_files_list, DataFilesList) for data_files_list in data_files.values())
        assert sorted(str(f) for f in data_files[split_name]) == hub_dataset_info_patterns_results[pattern]
        assert all(isinstance(url, Url) for url in data_files[split_name])
    except FileNotFoundError:
        assert len(hub_dataset_info_patterns_results[pattern]) == 0


@pytest.mark.parametrize("pattern", _TEST_PATTERNS)
def test_DataFilesDict_from_local_or_remote(complex_data_dir, pattern_results, pattern):
    split_name = "train"
    try:
        data_files = DataFilesDict.from_local_or_remote({split_name: [pattern]}, complex_data_dir)
        assert all(isinstance(data_files_list, DataFilesList) for data_files_list in data_files.values())
        assert sorted(str(f) for f in data_files[split_name]) == pattern_results[pattern]
        assert all(isinstance(url, Path) for url in data_files[split_name])
    except FileNotFoundError:
        assert len(pattern_results[pattern]) == 0


def test_DataFilesDict_from_hf_repo_hashing(hub_dataset_info):
    patterns = {"train": ["**/train.txt"], "test": ["**/test.txt"]}
    data_files1 = DataFilesDict.from_hf_repo(patterns, hub_dataset_info)
    data_files2 = DataFilesDict.from_hf_repo(patterns, hub_dataset_info)
    assert Hasher.hash(data_files1) == Hasher.hash(data_files2)

    data_files2 = DataFilesDict(sorted(data_files1.items(), reverse=True))
    assert Hasher.hash(data_files1) == Hasher.hash(data_files2)

    patterns2 = {"train": ["data/train.txt"], "test": ["data/test.txt"]}
    data_files2 = DataFilesDict.from_hf_repo(patterns2, hub_dataset_info)
    assert Hasher.hash(data_files1) == Hasher.hash(data_files2)

    patterns2 = {"train": ["data/train.txt"], "test": ["data/train.txt"]}
    data_files2 = DataFilesDict.from_hf_repo(patterns2, hub_dataset_info)
    assert Hasher.hash(data_files1) != Hasher.hash(data_files2)

    with patch.object(hub_dataset_info, "id", "blabla"):
        data_files2 = DataFilesDict.from_hf_repo(patterns, hub_dataset_info)
        assert Hasher.hash(data_files1) != Hasher.hash(data_files2)

    with patch.object(hub_dataset_info, "sha", "blabla"):
        data_files2 = DataFilesDict.from_hf_repo(patterns, hub_dataset_info)
        assert Hasher.hash(data_files1) != Hasher.hash(data_files2)


def test_DataFilesDict_from_hf_local_or_remote_hashing(text_file):
    patterns = {"train": [_TEST_URL], "test": [str(text_file)]}
    data_files1 = DataFilesDict.from_local_or_remote(patterns)
    data_files2 = DataFilesDict.from_local_or_remote(patterns)
    assert Hasher.hash(data_files1) == Hasher.hash(data_files2)

    data_files2 = DataFilesDict(sorted(data_files1.items(), reverse=True))
    assert Hasher.hash(data_files1) == Hasher.hash(data_files2)

    patterns2 = {"train": [_TEST_URL], "test": [_TEST_URL]}
    data_files2 = DataFilesDict.from_local_or_remote(patterns2)
    assert Hasher.hash(data_files1) != Hasher.hash(data_files2)

    with patch("datasets.data_files.request_etag") as mock_request_etag:
        mock_request_etag.return_value = "blabla"
        data_files2 = DataFilesDict.from_local_or_remote(patterns)
        assert Hasher.hash(data_files1) != Hasher.hash(data_files2)

    with patch("datasets.data_files.os.path.getmtime") as mock_getmtime:
        mock_getmtime.return_value = 123
        data_files2 = DataFilesDict.from_local_or_remote(patterns)
        assert Hasher.hash(data_files1) != Hasher.hash(data_files2)


@pytest.mark.parametrize(
    "data_file_per_split",
    [
        # === Main cases ===
        # file named afetr split at the root
        {"train": "train.txt", "test": "test.txt", "validation": "valid.txt"},
        # file named after split in a directory
        {
            "train": "data/train.txt",
            "test": "data/test.txt",
            "validation": "data/valid.txt",
        },
        # directory named after split
        {
            "train": "train/split.txt",
            "test": "test/split.txt",
            "validation": "valid/split.txt",
        },
        # sharded splits
        {
            "train": [f"data/train_{i}.txt" for i in range(3)],
            "test": [f"data/test_{i}.txt" for i in range(3)],
        },
        # sharded splits with standard format (+ custom split name)
        {
            "train": [f"data/train-0000{i}-of-00003.txt" for i in range(3)],
            "random": [f"data/random-0000{i}-of-00003.txt" for i in range(3)],
        },
        # === Secondary cases ===
        # Default to train split
        {"train": "dataset.txt"},
        {"train": "data/dataset.txt"},
        # With prefix or suffix in directory or file names
        {"train": "my_train_dir/dataset.txt"},
        {"train": "data/my_train_file.txt"},
        {"test": "my_test_dir/dataset.txt"},
        {"test": "data/my_test_file.txt"},
        {"validation": "my_validation_dir/dataset.txt"},
        {"validation": "data/my_validation_file.txt"},
        # With test<>eval aliases
        {"test": "eval.txt"},
        {"test": "data/eval.txt"},
        {"test": "eval/dataset.txt"},
        # With valid<>dev aliases
        {"validation": "dev.txt"},
        {"validation": "data/dev.txt"},
        {"validation": "dev/dataset.txt"},
        # With other extensions
        {"train": "train.parquet", "test": "test.parquet", "validation": "valid.parquet"},
    ],
)
def test_get_data_files_patterns(data_file_per_split):
    data_file_per_split = {k: v if isinstance(v, list) else [v] for k, v in data_file_per_split.items()}

    def resolver(pattern):
        return [PurePath(path) for path in chain(*data_file_per_split.values()) if PurePath(path).match(pattern)]

    patterns_per_split = _get_data_files_patterns(resolver)
    assert sorted(patterns_per_split.keys()) == sorted(data_file_per_split.keys())
    for split, patterns in patterns_per_split.items():
        matched = [
            path
            for path in chain(*data_file_per_split.values())
            for pattern in patterns
            if PurePath(path).match(pattern)
        ]
        assert len(matched) == len(data_file_per_split[split])
        assert matched == data_file_per_split[split]
