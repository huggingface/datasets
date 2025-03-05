import copy
import os
from pathlib import Path
from typing import List
from unittest.mock import patch

import fsspec
import pytest
from fsspec.registry import _registry as _fsspec_registry
from fsspec.spec import AbstractFileSystem

from datasets.data_files import (
    DataFilesDict,
    DataFilesList,
    DataFilesPatternsDict,
    DataFilesPatternsList,
    _get_data_files_patterns,
    _is_inside_unrequested_special_dir,
    _is_unrequested_hidden_file_or_is_inside_unrequested_hidden_dir,
    get_data_patterns,
    resolve_pattern,
)
from datasets.fingerprint import Hasher


_TEST_PATTERNS = ["*", "**", "**/*", "*.txt", "data/*", "**/*.txt", "**/train.txt"]
_FILES_TO_IGNORE = {".dummy", "README.md", "dummy_data.zip", "dataset_infos.json"}
_DIRS_TO_IGNORE = {"data/.dummy_subdir", "__pycache__"}
_TEST_PATTERNS_SIZES = {
    "*": 0,
    "**": 4,
    "**/*": 4,
    "*.txt": 0,
    "data/*": 2,
    "data/**": 4,
    "**/*.txt": 4,
    "**/train.txt": 2,
}

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

    (data_dir / "data" / "subdir").mkdir()
    with open(data_dir / "data" / "subdir" / "train.txt", "w") as f:
        f.write("foo\n" * 10)
    with open(data_dir / "data" / "subdir" / "test.txt", "w") as f:
        f.write("bar\n" * 10)

    (data_dir / "data" / ".dummy_subdir").mkdir()
    with open(data_dir / "data" / ".dummy_subdir" / "train.txt", "w") as f:
        f.write("foo\n" * 10)
    with open(data_dir / "data" / ".dummy_subdir" / "test.txt", "w") as f:
        f.write("bar\n" * 10)

    (data_dir / "__pycache__").mkdir()
    with open(data_dir / "__pycache__" / "script.py", "w") as f:
        f.write("foo\n" * 10)

    return str(data_dir)


def is_relative_to(path, *other):
    # A built-in method in Python 3.9+
    try:
        path.relative_to(*other)
        return True
    except ValueError:
        return False


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
            Path(os.path.abspath(path)).as_posix()
            for path in fsspec.filesystem("file").glob(os.path.join(complex_data_dir, pattern))
            if Path(path).name not in _FILES_TO_IGNORE
            and not any(
                is_relative_to(Path(path), os.path.join(complex_data_dir, dir_path)) for dir_path in _DIRS_TO_IGNORE
            )
            and Path(path).is_file()
        )
        for pattern in _TEST_PATTERNS
    }


@pytest.fixture
def hub_dataset_repo_path(tmpfs, complex_data_dir):
    for path in Path(complex_data_dir).rglob("*"):
        if path.is_file():
            with tmpfs.open(path.relative_to(complex_data_dir).as_posix(), "wb") as f:
                f.write(path.read_bytes())
    yield "tmp://"


@pytest.fixture
def hub_dataset_repo_patterns_results(hub_dataset_repo_path, complex_data_dir, pattern_results):
    return {
        pattern: [
            hub_dataset_repo_path + Path(path).relative_to(complex_data_dir).as_posix()
            for path in pattern_results[pattern]
        ]
        for pattern in pattern_results
    }


def test_is_inside_unrequested_special_dir(complex_data_dir, pattern_results):
    # usual patterns outside special dir work fine
    for pattern, result in pattern_results.items():
        if result:
            matched_rel_path = str(Path(result[0]).relative_to(complex_data_dir))
            assert _is_inside_unrequested_special_dir(matched_rel_path, pattern) is False
    # check behavior for special dir
    f = _is_inside_unrequested_special_dir
    assert f("__pycache__/b.txt", "**") is True
    assert f("__pycache__/b.txt", "*/b.txt") is True
    assert f("__pycache__/b.txt", "__pycache__/*") is False
    assert f("__pycache__/__b.txt", "__pycache__/*") is False
    assert f("__pycache__/__b.txt", "__*/*") is False
    assert f("__b.txt", "*") is False


def test_is_unrequested_hidden_file_or_is_inside_unrequested_hidden_dir(complex_data_dir, pattern_results):
    # usual patterns outside hidden dir work fine
    for pattern, result in pattern_results.items():
        if result:
            matched_rel_path = str(Path(result[0]).relative_to(complex_data_dir))
            assert _is_inside_unrequested_special_dir(matched_rel_path, pattern) is False
    # check behavior for hidden dir and file
    f = _is_unrequested_hidden_file_or_is_inside_unrequested_hidden_dir
    assert f(".hidden_file.txt", "**") is True
    assert f(".hidden_file.txt", ".*") is False
    assert f(".hidden_dir/a.txt", "**") is True
    assert f(".hidden_dir/a.txt", ".*/*") is False
    assert f(".hidden_dir/a.txt", ".hidden_dir/*") is False
    assert f(".hidden_dir/.hidden_file.txt", "**") is True
    assert f(".hidden_dir/.hidden_file.txt", ".*/*") is True
    assert f(".hidden_dir/.hidden_file.txt", ".*/.*") is False
    assert f(".hidden_dir/.hidden_file.txt", ".hidden_dir/*") is True
    assert f(".hidden_dir/.hidden_file.txt", ".hidden_dir/.*") is False


@pytest.mark.parametrize("pattern", _TEST_PATTERNS)
def test_pattern_results_fixture(pattern_results, pattern):
    assert len(pattern_results[pattern]) == _TEST_PATTERNS_SIZES[pattern]
    assert all(Path(path).is_file() for path in pattern_results[pattern])


@pytest.mark.parametrize("pattern", _TEST_PATTERNS)
def test_resolve_pattern_locally(complex_data_dir, pattern, pattern_results):
    try:
        resolved_data_files = resolve_pattern(pattern, complex_data_dir)
        assert sorted(str(f) for f in resolved_data_files) == pattern_results[pattern]
    except FileNotFoundError:
        assert len(pattern_results[pattern]) == 0


def test_resolve_pattern_locally_with_dot_in_base_path(complex_data_dir):
    base_path_with_dot = os.path.join(complex_data_dir, "data", ".dummy_subdir")
    resolved_data_files = resolve_pattern(os.path.join(base_path_with_dot, "train.txt"), base_path_with_dot)
    assert len(resolved_data_files) == 1


def test_resolve_pattern_locally_with_absolute_path(tmp_path, complex_data_dir):
    abs_path = os.path.join(complex_data_dir, "data", "train.txt")
    resolved_data_files = resolve_pattern(abs_path, str(tmp_path / "blabla"))
    assert len(resolved_data_files) == 1


def test_resolve_pattern_locally_with_double_dots(tmp_path, complex_data_dir):
    path_with_double_dots = os.path.join(complex_data_dir, "data", "subdir", "..", "train.txt")
    resolved_data_files = resolve_pattern(path_with_double_dots, str(tmp_path / "blabla"))
    assert len(resolved_data_files) == 1


def test_resolve_pattern_locally_returns_hidden_file_only_if_requested(complex_data_dir):
    with pytest.raises(FileNotFoundError):
        resolve_pattern("*dummy", complex_data_dir)
    resolved_data_files = resolve_pattern(".dummy", complex_data_dir)
    assert len(resolved_data_files) == 1


def test_resolve_pattern_locally_hidden_base_path(tmp_path):
    hidden = tmp_path / ".test_hidden_base_path"
    hidden.mkdir()
    (tmp_path / ".test_hidden_base_path" / "a.txt").touch()
    resolved_data_files = resolve_pattern("*", str(hidden))
    assert len(resolved_data_files) == 1


def test_resolve_pattern_locallyreturns_hidden_dir_only_if_requested(complex_data_dir):
    with pytest.raises(FileNotFoundError):
        resolve_pattern("data/*dummy_subdir/train.txt", complex_data_dir)
    resolved_data_files = resolve_pattern("data/.dummy_subdir/train.txt", complex_data_dir)
    assert len(resolved_data_files) == 1
    resolved_data_files = resolve_pattern("*/.dummy_subdir/train.txt", complex_data_dir)
    assert len(resolved_data_files) == 1


def test_resolve_pattern_locally_returns_special_dir_only_if_requested(complex_data_dir):
    with pytest.raises(FileNotFoundError):
        resolve_pattern("data/*dummy_subdir/train.txt", complex_data_dir)
    resolved_data_files = resolve_pattern("data/.dummy_subdir/train.txt", complex_data_dir)
    assert len(resolved_data_files) == 1
    resolved_data_files = resolve_pattern("*/.dummy_subdir/train.txt", complex_data_dir)
    assert len(resolved_data_files) == 1


def test_resolve_pattern_locally_special_base_path(tmp_path):
    special = tmp_path / "__test_special_base_path__"
    special.mkdir()
    (tmp_path / "__test_special_base_path__" / "a.txt").touch()
    resolved_data_files = resolve_pattern("*", str(special))
    assert len(resolved_data_files) == 1


@pytest.mark.parametrize("pattern,size,extensions", [("**", 4, [".txt"]), ("**", 4, None), ("**", 0, [".blablabla"])])
def test_resolve_pattern_locally_with_extensions(complex_data_dir, pattern, size, extensions):
    if size > 0:
        resolved_data_files = resolve_pattern(pattern, complex_data_dir, allowed_extensions=extensions)
        assert len(resolved_data_files) == size
    else:
        with pytest.raises(FileNotFoundError):
            resolve_pattern(pattern, complex_data_dir, allowed_extensions=extensions)


def test_fail_resolve_pattern_locally(complex_data_dir):
    with pytest.raises(FileNotFoundError):
        resolve_pattern(complex_data_dir, ["blablabla"])


@pytest.mark.skipif(os.name == "nt", reason="Windows does not support symlinks in the default mode")
def test_resolve_pattern_locally_does_not_resolve_symbolic_links(tmp_path, complex_data_dir):
    (tmp_path / "train_data_symlink.txt").symlink_to(os.path.join(complex_data_dir, "data", "train.txt"))
    resolved_data_files = resolve_pattern("train_data_symlink.txt", str(tmp_path))
    assert len(resolved_data_files) == 1
    assert Path(resolved_data_files[0]) == tmp_path / "train_data_symlink.txt"


def test_resolve_pattern_locally_sorted_files(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("unsorted_text_files"))
    unsorted_names = ["0.txt", "2.txt", "3.txt"]
    for name in unsorted_names:
        with open(os.path.join(path, name), "w"):
            pass
    resolved_data_files = resolve_pattern("*", path)
    resolved_names = [os.path.basename(data_file) for data_file in resolved_data_files]
    assert resolved_names == sorted(unsorted_names)


@pytest.mark.parametrize("pattern", _TEST_PATTERNS)
def test_resolve_pattern_in_dataset_repository(hub_dataset_repo_path, pattern, hub_dataset_repo_patterns_results):
    try:
        resolved_data_files = resolve_pattern(pattern, hub_dataset_repo_path)
        assert sorted(str(f) for f in resolved_data_files) == hub_dataset_repo_patterns_results[pattern]
    except FileNotFoundError:
        assert len(hub_dataset_repo_patterns_results[pattern]) == 0


@pytest.mark.parametrize(
    "pattern,size,base_path", [("**", 4, None), ("**", 4, "data"), ("**", 2, "data/subdir"), ("**", 0, "data/subdir2")]
)
def test_resolve_pattern_in_dataset_repository_with_base_path(hub_dataset_repo_path, pattern, size, base_path):
    base_path = hub_dataset_repo_path + (base_path or "")
    if size > 0:
        resolved_data_files = resolve_pattern(pattern, base_path)
        assert len(resolved_data_files) == size
    else:
        with pytest.raises(FileNotFoundError):
            resolve_pattern(pattern, base_path)


@pytest.mark.parametrize("pattern,size,extensions", [("**", 4, [".txt"]), ("**", 4, None), ("**", 0, [".blablabla"])])
def test_resolve_pattern_in_dataset_repository_with_extensions(hub_dataset_repo_path, pattern, size, extensions):
    if size > 0:
        resolved_data_files = resolve_pattern(pattern, hub_dataset_repo_path, allowed_extensions=extensions)
        assert len(resolved_data_files) == size
    else:
        with pytest.raises(FileNotFoundError):
            resolved_data_files = resolve_pattern(pattern, hub_dataset_repo_path, allowed_extensions=extensions)


def test_fail_resolve_pattern_in_dataset_repository(hub_dataset_repo_path):
    with pytest.raises(FileNotFoundError):
        resolve_pattern("blablabla", hub_dataset_repo_path)


def test_resolve_pattern_in_dataset_repository_returns_hidden_file_only_if_requested(hub_dataset_repo_path):
    with pytest.raises(FileNotFoundError):
        resolve_pattern("*dummy", hub_dataset_repo_path)
    resolved_data_files = resolve_pattern(".dummy", hub_dataset_repo_path)
    assert len(resolved_data_files) == 1


def test_resolve_pattern_in_dataset_repository_hidden_base_path(tmpfs):
    tmpfs.touch(".hidden/a.txt")
    resolved_data_files = resolve_pattern("*", base_path="tmp://.hidden")
    assert len(resolved_data_files) == 1


def test_resolve_pattern_in_dataset_repository_returns_hidden_dir_only_if_requested(hub_dataset_repo_path):
    with pytest.raises(FileNotFoundError):
        resolve_pattern("data/*dummy_subdir/train.txt", hub_dataset_repo_path)
    resolved_data_files = resolve_pattern("data/.dummy_subdir/train.txt", hub_dataset_repo_path)
    assert len(resolved_data_files) == 1
    resolved_data_files = resolve_pattern("*/.dummy_subdir/train.txt", hub_dataset_repo_path)
    assert len(resolved_data_files) == 1


def test_resolve_pattern_in_dataset_repository_returns_special_dir_only_if_requested(hub_dataset_repo_path):
    with pytest.raises(FileNotFoundError):
        resolve_pattern("data/*dummy_subdir/train.txt", hub_dataset_repo_path)
    resolved_data_files = resolve_pattern("data/.dummy_subdir/train.txt", hub_dataset_repo_path)
    assert len(resolved_data_files) == 1
    resolved_data_files = resolve_pattern("*/.dummy_subdir/train.txt", hub_dataset_repo_path)
    assert len(resolved_data_files) == 1


def test_resolve_pattern_in_dataset_repository_special_base_path(tmpfs):
    tmpfs.touch("__special__/a.txt")
    resolved_data_files = resolve_pattern("*", base_path="tmp://__special__")
    assert len(resolved_data_files) == 1


@pytest.fixture
def dummy_fs():
    DummyTestFS = mock_fs(["train.txt", "test.txt"])
    _fsspec_registry["mock"] = DummyTestFS
    _fsspec_registry["dummy"] = DummyTestFS
    yield
    del _fsspec_registry["mock"]
    del _fsspec_registry["dummy"]


def test_resolve_pattern_fs(dummy_fs):
    resolved_data_files = resolve_pattern("mock://train.txt", base_path="")
    assert resolved_data_files == ["mock://train.txt"]


@pytest.mark.parametrize("pattern", _TEST_PATTERNS)
def test_DataFilesList_from_patterns_in_dataset_repository_(
    hub_dataset_repo_path, hub_dataset_repo_patterns_results, pattern
):
    try:
        data_files_list = DataFilesList.from_patterns([pattern], hub_dataset_repo_path)
        assert sorted(data_files_list) == hub_dataset_repo_patterns_results[pattern]
        assert len(data_files_list.origin_metadata) == len(data_files_list)
    except FileNotFoundError:
        assert len(hub_dataset_repo_patterns_results[pattern]) == 0


def test_DataFilesList_from_patterns_locally_with_extra_files(complex_data_dir, text_file):
    data_files_list = DataFilesList.from_patterns([_TEST_URL, text_file.as_posix()], complex_data_dir)
    assert list(data_files_list) == [_TEST_URL, text_file.as_posix()]
    assert len(data_files_list.origin_metadata) == 2


def test_DataFilesList_from_patterns_raises_FileNotFoundError(complex_data_dir):
    with pytest.raises(FileNotFoundError):
        DataFilesList.from_patterns(["file_that_doesnt_exist.txt"], complex_data_dir)


class TestDataFilesDict:
    def test_key_order_after_copy(self):
        data_files = DataFilesDict({"train": "train.csv", "test": "test.csv"})
        copied_data_files = copy.deepcopy(data_files)
        assert list(copied_data_files.keys()) == list(data_files.keys())  # test split order with list()


@pytest.mark.parametrize("pattern", _TEST_PATTERNS)
def test_DataFilesDict_from_patterns_in_dataset_repository(
    hub_dataset_repo_path, hub_dataset_repo_patterns_results, pattern
):
    split_name = "train"
    try:
        data_files = DataFilesDict.from_patterns({split_name: [pattern]}, hub_dataset_repo_path)
        assert all(isinstance(data_files_list, DataFilesList) for data_files_list in data_files.values())
        assert sorted(data_files[split_name]) == hub_dataset_repo_patterns_results[pattern]
    except FileNotFoundError:
        assert len(hub_dataset_repo_patterns_results[pattern]) == 0


@pytest.mark.parametrize(
    "pattern,size,base_path,split_name",
    [
        ("**", 4, None, "train"),
        ("**", 4, "data", "train"),
        ("**", 2, "data/subdir", "train"),
        ("**", 0, "data/subdir2", "train"),
    ],
)
def test_DataFilesDict_from_patterns_in_dataset_repository_with_base_path(
    hub_dataset_repo_path, pattern, size, base_path, split_name
):
    base_path = hub_dataset_repo_path + (base_path or "")
    if size > 0:
        data_files = DataFilesDict.from_patterns({split_name: [pattern]}, base_path=base_path)
        assert len(data_files[split_name]) == size
    else:
        with pytest.raises(FileNotFoundError):
            resolve_pattern(pattern, base_path)


@pytest.mark.parametrize("pattern", _TEST_PATTERNS)
def test_DataFilesDict_from_patterns_locally(complex_data_dir, pattern_results, pattern):
    split_name = "train"
    try:
        data_files = DataFilesDict.from_patterns({split_name: [pattern]}, complex_data_dir)
        assert all(isinstance(data_files_list, DataFilesList) for data_files_list in data_files.values())
        assert sorted(data_files[split_name]) == pattern_results[pattern]
    except FileNotFoundError:
        assert len(pattern_results[pattern]) == 0


def test_DataFilesDict_from_patterns_in_dataset_repository_hashing(hub_dataset_repo_path):
    patterns = {"train": ["**/train.txt"], "test": ["**/test.txt"]}
    data_files1 = DataFilesDict.from_patterns(patterns, hub_dataset_repo_path)
    data_files2 = DataFilesDict.from_patterns(patterns, hub_dataset_repo_path)
    assert Hasher.hash(data_files1) == Hasher.hash(data_files2)

    data_files2 = DataFilesDict(sorted(data_files1.items(), reverse=True))
    assert Hasher.hash(data_files1) == Hasher.hash(data_files2)

    # the tmpfs used to mock the hub repo is based on a local directory
    # therefore os.stat is used to get the mtime of the data files
    with patch("os.stat", return_value=os.stat(__file__)):
        data_files2 = DataFilesDict.from_patterns(patterns, hub_dataset_repo_path)
        assert Hasher.hash(data_files1) != Hasher.hash(data_files2)


def test_DataFilesDict_from_patterns_locally_or_remote_hashing(text_file):
    patterns = {"train": [_TEST_URL], "test": [str(text_file)]}
    data_files1 = DataFilesDict.from_patterns(patterns)
    data_files2 = DataFilesDict.from_patterns(patterns)
    assert Hasher.hash(data_files1) == Hasher.hash(data_files2)

    data_files2 = DataFilesDict(sorted(data_files1.items(), reverse=True))
    assert Hasher.hash(data_files1) == Hasher.hash(data_files2)

    patterns2 = {"train": [_TEST_URL], "test": [_TEST_URL]}
    data_files2 = DataFilesDict.from_patterns(patterns2)
    assert Hasher.hash(data_files1) != Hasher.hash(data_files2)

    with patch("fsspec.implementations.http._file_info", return_value={}):
        data_files2 = DataFilesDict.from_patterns(patterns)
        assert Hasher.hash(data_files1) != Hasher.hash(data_files2)

    with patch("os.stat", return_value=os.stat(__file__)):
        data_files2 = DataFilesDict.from_patterns(patterns)
        assert Hasher.hash(data_files1) != Hasher.hash(data_files2)


def test_DataFilesPatternsList(text_file):
    data_files_patterns = DataFilesPatternsList([str(text_file)], allowed_extensions=[None])
    data_files = data_files_patterns.resolve(base_path="")
    assert data_files == [text_file.as_posix()]
    assert isinstance(data_files, DataFilesList)
    data_files_patterns = DataFilesPatternsList([str(text_file)], allowed_extensions=[[".txt"]])
    data_files = data_files_patterns.resolve(base_path="")
    assert data_files == [text_file.as_posix()]
    assert isinstance(data_files, DataFilesList)
    data_files_patterns = DataFilesPatternsList([str(text_file).replace(".txt", ".tx*")], allowed_extensions=[None])
    data_files = data_files_patterns.resolve(base_path="")
    assert data_files == [text_file.as_posix()]
    assert isinstance(data_files, DataFilesList)
    data_files_patterns = DataFilesPatternsList([Path(text_file).name], allowed_extensions=[None])
    data_files = data_files_patterns.resolve(base_path=str(Path(text_file).parent))
    assert data_files == [text_file.as_posix()]
    data_files_patterns = DataFilesPatternsList([str(text_file)], allowed_extensions=[[".zip"]])
    with pytest.raises(FileNotFoundError):
        data_files_patterns.resolve(base_path="")


def test_DataFilesPatternsDict(text_file):
    data_files_patterns_dict = DataFilesPatternsDict(
        {"train": DataFilesPatternsList([str(text_file)], allowed_extensions=[None])}
    )
    data_files_dict = data_files_patterns_dict.resolve(base_path="")
    assert data_files_dict == {"train": [text_file.as_posix()]}
    assert isinstance(data_files_dict, DataFilesDict)
    assert isinstance(data_files_dict["train"], DataFilesList)


def mock_fs(file_paths: List[str]):
    """
    Set up a mock filesystem for fsspec containing the provided files

    Example:

    ```py
    >>> DummyTestFS = mock_fs(["data/train.txt", "data.test.txt"])
    >>> fs = DummyTestFS()
    >>> assert fsspec.get_filesystem_class("mock").__name__ == "DummyTestFS"
    >>> assert type(fs).__name__ == "DummyTestFS"
    >>> print(fs.glob("**"))
    ["data", "data/train.txt", "data.test.txt"]
    ```
    """
    file_paths = [file_path.split("://")[-1] for file_path in file_paths]
    dir_paths = {
        "/".join(file_path.split("/")[: i + 1]) for file_path in file_paths for i in range(file_path.count("/"))
    }
    fs_contents = [{"name": dir_path, "type": "directory"} for dir_path in dir_paths] + [
        {"name": file_path, "type": "file", "size": 10} for file_path in file_paths
    ]

    class DummyTestFS(AbstractFileSystem):
        protocol = ("mock", "dummy")
        _fs_contents = fs_contents

        def ls(self, path, detail=True, refresh=True, **kwargs):
            if kwargs.pop("strip_proto", True):
                path = self._strip_protocol(path)

            files = not refresh and self._ls_from_cache(path)
            if not files:
                files = [file for file in self._fs_contents if path == self._parent(file["name"])]
                files.sort(key=lambda file: file["name"])
                self.dircache[path.rstrip("/")] = files

            if detail:
                return files
            return [file["name"] for file in files]

    return DummyTestFS


@pytest.mark.parametrize("base_path", ["", "mock://", "my_dir"])
@pytest.mark.parametrize(
    "data_file_per_split",
    [
        # === Main cases ===
        # file named after split at the root
        {"train": "train.txt", "validation": "valid.txt", "test": "test.txt"},
        # file named after split in a directory
        {
            "train": "data/train.txt",
            "validation": "data/valid.txt",
            "test": "data/test.txt",
        },
        # directory named after split
        {
            "train": "train/split.txt",
            "validation": "valid/split.txt",
            "test": "test/split.txt",
        },
        # sharded splits
        {
            "train": [f"data/train_{i}.txt" for i in range(3)],
            "validation": [f"data/validation_{i}.txt" for i in range(3)],
            "test": [f"data/test_{i}.txt" for i in range(3)],
        },
        # sharded splits with standard format (+ custom split name)
        {
            "train": [f"data/train-0000{i}-of-00003.txt" for i in range(3)],
            "validation": [f"data/validation-0000{i}-of-00003.txt" for i in range(3)],
            "test": [f"data/test-0000{i}-of-00003.txt" for i in range(3)],
            "random": [f"data/random-0000{i}-of-00003.txt" for i in range(3)],
        },
        # === Secondary cases ===
        # Default to train split
        {"train": "dataset.txt"},
        {"train": "data/dataset.txt"},
        {"train": ["data/image.jpg", "metadata.jsonl"]},
        {"train": ["data/image.jpg", "metadata.csv"]},
        # With prefix or suffix in directory or file names
        {"train": "my_train_dir/dataset.txt"},
        {"train": "data/my_train_file.txt"},
        {"test": "my_test_dir/dataset.txt"},
        {"test": "data/my_test_file.txt"},
        {"validation": "my_validation_dir/dataset.txt"},
        {"validation": "data/my_validation_file.txt"},
        {"train": "train_dir/dataset.txt"},
        {"train": "data/train_file.txt"},
        {"test": "test_dir/dataset.txt"},
        {"test": "data/test_file.txt"},
        {"validation": "validation_dir/dataset.txt"},
        {"validation": "data/validation_file.txt"},
        {"train": "my_train/dataset.txt"},
        {"train": "data/my_train.txt"},
        {"test": "my_test/dataset.txt"},
        {"test": "data/my_test.txt"},
        {"validation": "my_validation/dataset.txt"},
        {"validation": "data/my_validation.txt"},
        # With test<>eval aliases
        {"test": "eval.txt"},
        {"test": "data/eval.txt"},
        {"test": "eval/dataset.txt"},
        # With valid<>dev aliases
        {"validation": "dev.txt"},
        {"validation": "data/dev.txt"},
        {"validation": "dev/dataset.txt"},
        # With valid<>val aliases
        {"validation": "val.txt"},
        {"validation": "data/val.txt"},
        # With other extensions
        {"train": "train.parquet", "validation": "valid.parquet", "test": "test.parquet"},
        # With "dev" or "eval" without separators
        {"train": "developers_list.txt"},
        {"train": "data/seqeval_results.txt"},
        {"train": "contest.txt"},
        # With supported separators
        {"test": "my.test.file.txt"},
        {"test": "my-test-file.txt"},
        {"test": "my_test_file.txt"},
        {"test": "my test file.txt"},
        {"test": "my-test_file.txt"},
        {"test": "test00001.txt"},
        # <split>.<split> case
        {"test": "test/train.txt"},
    ],
)
def test_get_data_files_patterns(base_path, data_file_per_split):
    data_file_per_split = {k: v if isinstance(v, list) else [v] for k, v in data_file_per_split.items()}
    data_file_per_split = {
        split: [
            base_path + ("/" if base_path and base_path[-1] != "/" else "") + file_path
            for file_path in data_file_per_split[split]
        ]
        for split in data_file_per_split
    }
    file_paths = sum(data_file_per_split.values(), [])
    DummyTestFS = mock_fs(file_paths)
    fs = DummyTestFS()

    def resolver(pattern):
        pattern = base_path + ("/" if base_path and base_path[-1] != "/" else "") + pattern
        return [
            file_path[len(fs._strip_protocol(base_path)) :].lstrip("/")
            for file_path in fs.glob(pattern)
            if fs.isfile(file_path)
        ]

    patterns_per_split = _get_data_files_patterns(resolver)
    assert list(patterns_per_split.keys()) == list(data_file_per_split.keys())  # Test split order with list()
    for split, patterns in patterns_per_split.items():
        matched = [file_path for pattern in patterns for file_path in resolver(pattern)]
        expected = [
            fs._strip_protocol(file_path)[len(fs._strip_protocol(base_path)) :].lstrip("/")
            for file_path in data_file_per_split[split]
        ]
        assert matched == expected


def test_get_data_patterns_from_directory_with_the_word_data_twice(tmp_path):
    repo_dir = tmp_path / "directory-name-ending-with-the-word-data"  # parent directory contains the word "data/"
    data_dir = repo_dir / "data"
    data_dir.mkdir(parents=True)
    data_file = data_dir / "train-00001-of-00009.parquet"
    data_file.touch()
    data_file_patterns = get_data_patterns(repo_dir.as_posix())
    assert data_file_patterns == {"train": ["data/train-[0-9][0-9][0-9][0-9][0-9]-of-[0-9][0-9][0-9][0-9][0-9]*.*"]}
