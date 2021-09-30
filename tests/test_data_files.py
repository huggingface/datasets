import os
from pathlib import Path

import pytest
from huggingface_hub.hf_api import DatasetInfo

from datasets.data_files import _resolve_patterns_in_dataset_repository, _resolve_patterns_locally_or_by_urls, DataFilesList, DataFilesDict
from datasets.utils.file_utils import hf_hub_url


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


@pytest.mark.parametrize(
    "pattern,size", [("*", 2), ("**/*", 2), ("*.txt", 2), ("data/*", 2), ("**/*.txt", 2), ("**/train.txt", 1)]
)
def test_resolve_patterns_locally_or_by_urls(complex_data_dir, pattern, size):
    resolved_data_files = _resolve_patterns_locally_or_by_urls(complex_data_dir, [pattern])
    files_to_ignore = {".dummy", "README.md"}
    expected_resolved_data_files = [
        path for path in Path(complex_data_dir).rglob(pattern) if path.name not in files_to_ignore and path.is_file()
    ]
    assert len(resolved_data_files) == size
    assert sorted(resolved_data_files) == sorted(expected_resolved_data_files)
    assert all(isinstance(path, Path) for path in resolved_data_files)
    assert all(path.is_file() for path in resolved_data_files)


def test_resolve_patterns_locally_or_by_urls_with_absolute_path(tmp_path, complex_data_dir):
    abs_path = os.path.join(complex_data_dir, "data", "train.txt")
    resolved_data_files = _resolve_patterns_locally_or_by_urls(str(tmp_path / "blabla"), [abs_path])
    assert len(resolved_data_files) == 1


@pytest.mark.parametrize("pattern,size,extensions", [("*", 2, ["txt"]), ("*", 2, None), ("*", 0, ["blablabla"])])
def test_resolve_patterns_locally_or_by_urls_with_extensions(complex_data_dir, pattern, size, extensions):
    if size > 0:
        resolved_data_files = _resolve_patterns_locally_or_by_urls(
            complex_data_dir, [pattern], allowed_extensions=extensions
        )
        assert len(resolved_data_files) == size
    else:
        with pytest.raises(FileNotFoundError):
            _resolve_patterns_locally_or_by_urls(complex_data_dir, pattern, allowed_extensions=extensions)


def test_fail_resolve_patterns_locally_or_by_urls(complex_data_dir):
    with pytest.raises(FileNotFoundError):
        _resolve_patterns_locally_or_by_urls(complex_data_dir, ["blablabla"])


@pytest.mark.parametrize(
    "pattern,size", [("*", 2), ("**/*", 2), ("*.txt", 2), ("data/*", 2), ("**/*.txt", 2), ("**/train.txt", 1)]
)
def test_resolve_patterns_in_dataset_repository(complex_data_dir, pattern, size):
    dataset_info = DatasetInfo(
        siblings=[
            {"rfilename": path.relative_to(complex_data_dir).as_posix()}
            for path in Path(complex_data_dir).rglob("*")
            if path.is_file()
        ],
        sha="foobarfoobar",
        id="foo",
    )
    resolved_data_files = _resolve_patterns_in_dataset_repository(dataset_info, [pattern])
    files_to_ignore = {".dummy", "README.md"}
    expected_data_files = [
        path.relative_to(complex_data_dir)
        for path in Path(complex_data_dir).rglob(pattern)
        if path.name not in files_to_ignore and path.is_file()
    ]
    expected_resolved_data_files = [
        hf_hub_url(dataset_info.id, "", revision=dataset_info.sha) + str(expected_data_file)
        for expected_data_file in expected_data_files
    ]
    assert len(resolved_data_files) == size
    assert sorted(resolved_data_files) == sorted(expected_resolved_data_files)
    assert all(isinstance(path, str) for path in resolved_data_files)
    assert all((Path(complex_data_dir) / path).is_file() for path in expected_data_files)


@pytest.mark.parametrize("pattern,size,extensions", [("*", 2, ["txt"]), ("*", 2, None), ("*", 0, ["blablabla"])])
def test_resolve_patterns_in_dataset_repository_with_extensions(complex_data_dir, pattern, size, extensions):
    dataset_info = DatasetInfo(
        siblings=[
            {"rfilename": path.relative_to(complex_data_dir).as_posix()}
            for path in Path(complex_data_dir).rglob("*")
            if path.is_file()
        ],
        sha="foobarfoobar",
        id="foo",
    )
    if size > 0:
        resolved_data_files = _resolve_patterns_in_dataset_repository(
            dataset_info, [pattern], allowed_extensions=extensions
        )
        assert len(resolved_data_files) == size
    else:
        with pytest.raises(FileNotFoundError):
            resolved_data_files = _resolve_patterns_in_dataset_repository(
                dataset_info, [pattern], allowed_extensions=extensions
            )


def test_fail_resolve_patterns_in_dataset_repository(complex_data_dir):
    dataset_info = DatasetInfo(
        siblings=[
            {"rfilename": path.relative_to(complex_data_dir).as_posix()}
            for path in Path(complex_data_dir).rglob("*")
            if path.is_file()
        ]
    )
    with pytest.raises(FileNotFoundError):
        _resolve_patterns_in_dataset_repository(dataset_info, "blablabla")


def test_DataFilesList_from_hf_repo():
    pass


def test_DataFilesList_from_local_or_remote():
    pass


def test_DataFilesDict_from_hf_repo():
    pass


def test_DataFilesDict_from_local_or_remote():
    pass


def test_DataFilesDict_hashing():
    pass
