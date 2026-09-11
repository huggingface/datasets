import fnmatch
import json
import socket
from contextlib import nullcontext
from datetime import datetime, time
from decimal import Decimal
from io import BytesIO
from pathlib import Path
from types import SimpleNamespace

import pyarrow.parquet as pq
import pytest
from fsspec.implementations.memory import MemoryFileSystem
from huggingface_hub import CommitOperationAdd, CommitOperationCopy, CommitOperationDelete, DatasetCard

from datasets import Audio, ClassLabel, Dataset, DatasetDict, Features, Image, Value, load_dataset
from datasets.data_files import sanitize_patterns
from datasets.info import DatasetInfosDict
from datasets.utils.metadata import MetadataConfigs


@pytest.fixture
def hub(monkeypatch):
    """Run real serialization and card updates, replacing only Hub I/O."""

    def no_network(*args, **kwargs):
        raise AssertionError("Append unit tests must not access the network")

    monkeypatch.setattr(socket.socket, "connect", no_network)
    fs = MemoryFileSystem(skip_instance_cache=True)
    monkeypatch.setattr(fs, "store", {})
    monkeypatch.setattr(fs, "pseudo_dirs", [""])
    root = "/datasets/append-test/data@sha"
    fs.makedirs(root)
    uploads, commits, downloads = [], [], []
    staged = {}

    class Api:
        def __init__(self, *args, **kwargs):
            pass

        def repo_info(self, repo_id, **kwargs):
            return SimpleNamespace(id=repo_id, sha="sha")

        def create_branch(self, *args, **kwargs):
            pass

        def list_repo_tree(self, repo_id, path_in_repo=None, **kwargs):
            assert kwargs["revision"] == "sha"
            return [
                SimpleNamespace(path=path[len(root) + 1 :], size=fs.size(path))
                for path in fs.find(root)
                if path_in_repo is None or path.startswith(root + "/" + path_in_repo + "/")
            ]

        def hf_hub_download(self, repo_id, filename, **kwargs):
            raise AssertionError("Use the snapshot filesystem for downloads")

        def preupload_lfs_files(self, repo_id, additions, **kwargs):
            for operation in additions:
                with operation.as_file() as file:
                    staged[id(operation)] = file.read()
                uploads.append(operation.path_in_repo)

        def create_commit(self, repo_id, operations, **kwargs):
            assert kwargs.get("parent_commit") == "sha"
            commits.append(operations)
            # Copy from the parent snapshot, even if deletions precede copies.
            copies = {
                op.path_in_repo: fs.cat_file(root + "/" + op.src_path_in_repo)
                for op in operations
                if isinstance(op, CommitOperationCopy)
            }
            for op in operations:
                path = root + "/" + op.path_in_repo
                if isinstance(op, CommitOperationAdd):
                    if id(op) in staged:
                        data = staged[id(op)]
                    else:
                        with op.as_file() as file:
                            data = file.read()
                    fs.pipe_file(path, data)
                elif isinstance(op, CommitOperationCopy):
                    fs.pipe_file(path, copies[op.path_in_repo])
                else:
                    assert isinstance(op, CommitOperationDelete)
                    fs.rm(path)
            return SimpleNamespace(oid="sha", commit_url="https://example.invalid/commit/sha")

    original_get_file = fs.get_file

    def get_file(remote, local, **kwargs):
        downloads.append(remote[len(root) + 1 :].lstrip("/"))
        return original_get_file(remote, local, **kwargs)

    monkeypatch.setattr(fs, "get_file", get_file)
    for module in ["datasets.arrow_dataset", "datasets.dataset_dict"]:
        monkeypatch.setattr(module + ".HfApi", Api)
        monkeypatch.setattr(module + ".HfFileSystem", lambda **kwargs: fs)

    def files(pattern="*.parquet"):
        return {
            path[len(root) + 1 :]: fs.cat_file(path)
            for path in fs.find(root)
            if fnmatch.fnmatch(path[len(root) + 1 :], pattern)
        }

    def card():
        return DatasetCard(fs.cat_file(root + "/README.md").decode())

    return SimpleNamespace(
        repo_id="append-test/data",
        fs=fs,
        root=root,
        files=files,
        card=card,
        uploads=uploads,
        commits=commits,
        downloads=downloads,
    )


def parquet_prefix(data):
    return data[: -8 - int.from_bytes(data[-8:-4], "little")]


def rows(files):
    return [row for path, data in sorted(files.items()) for row in pq.read_table(BytesIO(data)).to_pylist()]


def configured_rows(hub, config_name="default"):
    data_files = MetadataConfigs.from_dataset_card_data(hub.card().data)[config_name]["data_files"]
    return {
        split: [
            row
            for pattern in patterns
            for path in hub.fs.glob(hub.root + "/" + pattern)
            if path.endswith(".parquet")
            for row in pq.read_table(BytesIO(hub.fs.cat_file(path))).to_pylist()
        ]
        for split, patterns in sanitize_patterns(data_files).items()
    }


def load_local_hub(hub, tmp_path, config_name="default"):
    repo = tmp_path / "repo"
    for path, data in hub.files("*").items():
        destination = repo / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    return load_dataset(str(repo), name=config_name, cache_dir=str(tmp_path / "cache"))


def seed_train_directories(hub, directories=("data", "more"), explicit_paths=False):
    """Build a mapped parent snapshot without relying on append's directory selection."""
    Dataset.from_dict({"x": [0, 1]}).push_to_hub(hub.repo_id, num_shards=2)
    paths = [f"{directory}/train-00000-of-00001.parquet" for directory in directories]
    for index, path in enumerate(paths):
        hub.fs.mv(hub.root + f"/data/train-{index:05d}-of-00002.parquet", hub.root + "/" + path)
    card = hub.card()
    configs = MetadataConfigs.from_dataset_card_data(card.data)
    configs["default"]["data_files"] = [
        {"split": "train", "path": paths if explicit_paths else [f"{directory}/train-*" for directory in directories]}
    ]
    configs.to_dataset_card_data(card.data)
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    return paths


@pytest.mark.parametrize("num_shards", [None, 2])
@pytest.mark.parametrize("config_name", ["default", "fr"])
@pytest.mark.parametrize("train_path", ["data/train-00000-of-00002.parquet", "data/custom.parquet"])
def test_append_respects_explicit_split_files(hub, tmp_path, num_shards, config_name, train_path):
    DatasetDict(train=Dataset.from_dict({"x": [0]}), test=Dataset.from_dict({"x": [1]})).push_to_hub(
        hub.repo_id, config_name=config_name, data_dir="data"
    )
    test_path = "data/train-00001-of-00002.parquet"
    hub.fs.mv(hub.root + "/data/train-00000-of-00001.parquet", hub.root + "/" + train_path)
    hub.fs.mv(hub.root + "/data/test-00000-of-00001.parquet", hub.root + "/" + test_path)
    card = hub.card()
    configs = MetadataConfigs.from_dataset_card_data(card.data)
    configs[config_name]["data_files"] = [
        {"split": "train", "path": train_path},
        {"split": "test", "path": test_path},
    ]
    configs.to_dataset_card_data(card.data)
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    test_bytes = hub.files()[test_path]
    hub.uploads.clear()
    Dataset.from_dict({"x": [2]}).push_to_hub(
        hub.repo_id, config_name=config_name, data_dir="data", append=True, num_shards=num_shards
    )
    assert configured_rows(hub, config_name) == {"train": [{"x": 0}, {"x": 2}], "test": [{"x": 1}]}
    assert hub.files()[test_path] == test_bytes
    assert hub.downloads == [train_path]
    assert len(hub.uploads) == 1
    result = load_local_hub(hub, tmp_path, config_name)
    assert list(result["train"]["x"]) == [0, 2]
    assert list(result["test"]["x"]) == [1]


def test_append_explicit_split_mapping_keeps_rows_and_counts(hub, tmp_path):
    DatasetDict(train=Dataset.from_dict({"x": [0]}), test=Dataset.from_dict({"x": [1]})).push_to_hub(hub.repo_id)
    paths = [f"data/train-{index:05d}-of-00002.parquet" for index in range(2)]
    for split, path in zip(["train", "test"], paths):
        hub.fs.mv(hub.root + f"/data/{split}-00000-of-00001.parquet", hub.root + "/" + path)
    card = hub.card()
    configs = MetadataConfigs.from_dataset_card_data(card.data)
    configs["default"]["data_files"] = [
        {"split": split, "path": path} for split, path in zip(["train", "test"], paths)
    ]
    configs.to_dataset_card_data(card.data)
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    test_bytes = hub.files()[paths[1]]

    Dataset.from_dict({"x": [2]}).push_to_hub(hub.repo_id, split="train", append=True)

    assert configured_rows(hub) == {"train": [{"x": 0}, {"x": 2}], "test": [{"x": 1}]}
    info = DatasetInfosDict.from_dataset_card_data(hub.card().data)["default"]
    assert {split: stats.num_examples for split, stats in info.splits.items()} == {"train": 2, "test": 1}
    assert hub.files()[paths[1]] == test_bytes
    result = load_local_hub(hub, tmp_path)
    assert list(result["train"]["x"]) == [0, 2]
    assert list(result["test"]["x"]) == [1]


def test_review_append_wrong_split_shard(hub, tmp_path):
    DatasetDict(train=Dataset.from_dict({"x": [0]}), test=Dataset.from_dict({"x": [1]})).push_to_hub(hub.repo_id)
    paths = [f"data/train-{index:05d}-of-00002.parquet" for index in range(2)]
    for split, path in zip(["train", "test"], paths):
        hub.fs.mv(hub.root + f"/data/{split}-00000-of-00001.parquet", hub.root + "/" + path)
    card = hub.card()
    configs = MetadataConfigs.from_dataset_card_data(card.data)
    configs["default"]["data_files"] = [
        {"split": split, "path": path} for split, path in zip(["train", "test"], paths)
    ]
    configs.to_dataset_card_data(card.data)
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    original_test = hub.files()[paths[1]]

    Dataset.from_dict({"x": [2]}).push_to_hub(hub.repo_id, split="train", append=True)

    result = load_local_hub(hub, tmp_path)
    assert list(result["train"]["x"]) == [0, 2]
    assert list(result["test"]["x"]) == [1]
    assert hub.files()[paths[1]] == original_test
    info = DatasetInfosDict.from_dataset_card_data(hub.card().data)["default"]
    assert {split: stats.num_examples for split, stats in info.splits.items()} == {"train": 2, "test": 1}


@pytest.mark.parametrize("paths", [["data/part-0.parquet"], ["z/part-0.parquet", "a/part-1.parquet"]])
def test_review_append_nonstandard_glob(hub, tmp_path, paths):
    Dataset.from_dict({"x": [0, 1]}).push_to_hub(hub.repo_id, num_shards=len(paths))
    for old_path, path in zip(hub.files(), paths):
        hub.fs.mv(hub.root + "/" + old_path, hub.root + "/" + path)
    patterns = [str(Path(path).parent / "*.parquet") for path in paths]
    card = hub.card()
    configs = MetadataConfigs.from_dataset_card_data(card.data)
    configs["default"]["data_files"] = [{"split": "train", "path": patterns}]
    configs.to_dataset_card_data(card.data)
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    hub.uploads.clear()

    Dataset.from_dict({"x": [2]}).push_to_hub(hub.repo_id, append=True)

    assert configured_rows(hub) == {"train": [{"x": 0}, {"x": 1}, {"x": 2}]}
    assert sanitize_patterns(MetadataConfigs.from_dataset_card_data(hub.card().data)["default"]["data_files"]) == {
        "train": patterns
    }
    assert hub.downloads == hub.uploads == [paths[-1]]
    assert list(load_local_hub(hub, tmp_path)["train"]["x"]) == [0, 1, 2]


@pytest.mark.parametrize(
    "shared_pattern", ["data/train-00000-of-00001.parquet", "data/*-of-00001.parquet", "data/train-*", "**/*.parquet"]
)
@pytest.mark.parametrize("num_shards", [None, 2])
def test_review_append_shared_file(hub, tmp_path, shared_pattern, num_shards):
    Dataset.from_dict({"x": [0]}).push_to_hub(hub.repo_id)
    path = "data/train-00000-of-00001.parquet"
    original = hub.files()[path]
    card = hub.card()
    configs = MetadataConfigs.from_dataset_card_data(card.data)
    configs["other"] = {"data_files": [{"split": "train", "path": shared_pattern}]}
    configs.to_dataset_card_data(card.data)
    infos = DatasetInfosDict.from_dataset_card_data(card.data)
    infos["other"] = infos["default"].copy()
    infos["other"].config_name = "other"
    infos.to_dataset_card_data(card.data)
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())

    Dataset.from_dict({"x": [1]}).push_to_hub(hub.repo_id, append=True, num_shards=num_shards)

    assert hub.files().get(path) == original
    assert configured_rows(hub) == {"train": [{"x": 0}, {"x": 1}]}
    assert configured_rows(hub, "other") == {"train": [{"x": 0}]}
    other = MetadataConfigs.from_dataset_card_data(hub.card().data)["other"]
    # A broad pattern may be narrowed only to its complete original file set.
    assert other == configs["other"] or sanitize_patterns(other["data_files"]) == {"train": [path]}
    assert DatasetInfosDict.from_dataset_card_data(hub.card().data)["other"] == infos["other"]
    assert list(load_local_hub(hub, tmp_path, "other")["train"]["x"]) == [0]


@pytest.mark.parametrize("directory", [".staging", "__staging", "_staging"])
@pytest.mark.parametrize("explicit", [False, True])
def test_review_append_hidden_directories(hub, tmp_path, directory, explicit):
    Dataset.from_dict({"x": [0]}).push_to_hub(hub.repo_id)
    visible = "data/train-00000-of-00001.parquet"
    hidden = f"data/z/{directory}/train-00000-of-00001.parquet"
    buffer = BytesIO()
    Dataset.from_dict({"x": [1]}).to_parquet(buffer)
    hub.fs.pipe_file(hub.root + "/" + hidden, buffer.getvalue())
    requested = explicit or directory == "_staging"
    patterns = [visible, hidden] if explicit else ["data/**/*.parquet"]
    card = hub.card()
    configs = MetadataConfigs.from_dataset_card_data(card.data)
    configs["default"]["data_files"] = [{"split": "train", "path": patterns}]
    configs.to_dataset_card_data(card.data)
    info = card.data["dataset_info"]
    info["splits"][0]["num_examples"] = 2 if requested else 1
    info["splits"][0]["num_bytes"] = info["dataset_size"] = 16 if requested else 8
    if requested:
        info["download_size"] += len(buffer.getvalue())
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    hub.uploads.clear()

    Dataset.from_dict({"x": [2]}).push_to_hub(hub.repo_id, append=True)

    assert hub.downloads == [hidden if requested else visible]
    assert hub.uploads == hub.downloads
    assert list(load_local_hub(hub, tmp_path)["train"]["x"]) == ([0, 1, 2] if requested else [0, 2])
    assert sanitize_patterns(MetadataConfigs.from_dataset_card_data(hub.card().data)["default"]["data_files"]) == {
        "train": patterns
    }


def test_review_append_new_split_worker_order(hub, tmp_path, monkeypatch):
    Dataset.from_dict({"x": [-1]}).push_to_hub(hub.repo_id)

    def reversed_workers(pool, function, kwargs_iterable):
        # Execute real shard writers, deterministically delivering worker 1 first.
        for kwargs in reversed(kwargs_iterable):
            yield from function(**kwargs)

    monkeypatch.setattr("datasets.arrow_dataset.iflatmap_unordered", reversed_workers)
    monkeypatch.setattr(
        "datasets.arrow_dataset.mp.get_context",
        lambda method: SimpleNamespace(Pool=lambda num_proc: nullcontext(object())),
    )
    Dataset.from_dict({"x": [0, 1, 2, 3]}).push_to_hub(
        hub.repo_id, split="validation", append=True, num_shards=2, num_proc=2
    )

    assert list(load_local_hub(hub, tmp_path)["validation"]["x"]) == [0, 1, 2, 3]


@pytest.mark.parametrize(
    "dtype,values",
    [
        ("date64", [datetime(2020, 1, 1), datetime(2020, 1, 2)]),
        ("time32[s]", [time(1, 2, 3), time(4, 5, 6)]),
        ("timestamp[s]", [datetime(2020, 1, 1), datetime(2020, 1, 2)]),
    ],
)
@pytest.mark.parametrize("recover_info", [False, True])
def test_review_append_temporal_normalization(hub, tmp_path, dtype, values, recover_info):
    features = Features({"x": Value(dtype)})
    Dataset.from_dict({"x": values[:1]}, features=features).push_to_hub(hub.repo_id)
    if recover_info:
        card = hub.card()
        card.data.pop("dataset_info")
        hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    original = hub.files()
    assert load_local_hub(hub, tmp_path / "before")["train"].num_rows == 1

    error = None
    try:
        Dataset.from_dict({"x": values[1:]}, features=features).push_to_hub(hub.repo_id, append=True)
    except ValueError as caught:
        error = caught
    assert error is None, str(error)

    path = next(iter(original))
    assert hub.files()[path].startswith(parquet_prefix(original[path]))
    result = load_local_hub(hub, tmp_path / "after")["train"]
    assert result.num_rows == 2
    expected = Dataset.from_dict({"x": values}, features=features).cast(result.features)
    assert result.to_dict() == expected.to_dict()


@pytest.mark.parametrize(
    "old_dtype,new_dtype,old_value,new_value",
    [
        ("time32[s]", "time32[ms]", time(1, 2, 3), time(1, 2, 3, 123000)),
        ("timestamp[s]", "timestamp[ms]", datetime(2020, 1, 1), datetime(2020, 1, 1, microsecond=123000)),
    ],
)
def test_review_append_temporal_card_precision(hub, old_dtype, new_dtype, old_value, new_value):
    Dataset.from_dict({"x": [old_value]}, features=Features({"x": Value(old_dtype)})).push_to_hub(hub.repo_id)
    original = hub.files("*")
    error = None
    try:
        Dataset.from_dict({"x": [new_value]}, features=Features({"x": Value(new_dtype)})).push_to_hub(
            hub.repo_id, append=True
        )
    except ValueError as caught:
        error = caught
    assert error is not None, "Append must reject rows that cannot be loaded with the card's features"
    assert hub.files("*") == original


@pytest.mark.parametrize(
    "dtype,values,writer_options",
    [
        ("time64[us]", [time(1, 2, 3), time(4, 5, 6)], {"write_time_adjusted_to_utc": True}),
        ("time64[ns]", [time(1, 2, 3), time(4, 5, 6)], {"write_time_adjusted_to_utc": True}),
        (
            "timestamp[ns]",
            [datetime(2020, 1, 1, microsecond=123456), datetime(2020, 1, 2, microsecond=654321)],
            {"coerce_timestamps": "ms", "allow_truncated_timestamps": True},
        ),
        (
            "timestamp[ns, tz=UTC]",
            [datetime(2020, 1, 1), datetime(2020, 1, 2)],
            {"coerce_timestamps": "us", "allow_truncated_timestamps": True},
        ),
    ],
)
@pytest.mark.parametrize("nested", [False, True])
def test_review_append_temporal_writer_properties(hub, tmp_path, dtype, values, writer_options, nested):
    features = Features({"x": {"times": [Value(dtype)]} if nested else Value(dtype)})
    values = [{"times": [value]} for value in values] if nested else values
    data = Dataset.from_dict({"x": values}, features=features)
    data.select([0]).push_to_hub(hub.repo_id)
    path = next(iter(hub.files()))
    buffer = BytesIO()
    pq.write_table(data.select([0]).data.table, buffer, **writer_options)
    original = buffer.getvalue()
    hub.fs.pipe_file(hub.root + "/" + path, original)
    card = hub.card()
    card.data["dataset_info"]["download_size"] = len(original)
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())

    error = None
    try:
        data.select([1]).push_to_hub(hub.repo_id, append=True)
    except (ValueError, RuntimeError) as caught:
        error = caught
    assert error is None, str(error)

    appended = hub.files()[path]
    assert appended.startswith(parquet_prefix(original))
    assert pq.read_metadata(BytesIO(appended)).schema.equals(pq.read_metadata(BytesIO(original)).schema)
    expected = BytesIO()
    pq.write_table(data.data.table, expected, **writer_options)
    assert pq.read_table(BytesIO(appended)).to_pydict() == pq.read_table(expected).to_pydict()
    assert load_local_hub(hub, tmp_path)["train"].num_rows == 2


@pytest.mark.parametrize("directories", [("data", "more"), ("z", "a"), ("data", "data/nested")])
@pytest.mark.parametrize("explicit_paths", [False, True])
@pytest.mark.parametrize("num_shards", [None, 3])
def test_append_uses_last_mapped_shard_across_directories(hub, tmp_path, directories, explicit_paths, num_shards):
    paths = seed_train_directories(hub, directories, explicit_paths)
    original = hub.files()[paths[0]]
    hub.uploads.clear()

    Dataset.from_dict({"x": [2]}).push_to_hub(hub.repo_id, append=True, num_shards=num_shards)

    assert configured_rows(hub) == {"train": [{"x": 0}, {"x": 1}, {"x": 2}]}
    assert list(load_local_hub(hub, tmp_path)["train"]["x"]) == [0, 1, 2]
    assert hub.downloads == [paths[1]]
    if num_shards is None:
        assert hub.files()[paths[0]] == original
        assert hub.uploads == [paths[1]]
    else:
        assert len(hub.files()) == 3
        assert len(hub.uploads) == 1


@pytest.mark.parametrize("explicit_paths", [False, True])
def test_append_empty_preserves_pattern_order(hub, tmp_path, explicit_paths):
    old = Dataset.from_dict({"x": [0]})
    seed_train_directories(hub, explicit_paths=explicit_paths)
    before = hub.files("*")
    old.select([]).push_to_hub(hub.repo_id, data_dir="data", append=True)
    assert configured_rows(hub) == {"train": [{"x": 0}, {"x": 1}]}
    assert hub.files("*") == before
    assert list(load_local_hub(hub, tmp_path)["train"]["x"]) == [0, 1]


def test_append_new_split_preserves_foreign_filename(hub, tmp_path):
    Dataset.from_dict({"x": [1]}).push_to_hub(hub.repo_id, split="test")
    path = "data/train-00000-of-00001.parquet"
    hub.fs.mv(hub.root + "/data/test-00000-of-00001.parquet", hub.root + "/" + path)
    card = hub.card()
    configs = MetadataConfigs.from_dataset_card_data(card.data)
    configs["default"]["data_files"] = [{"split": "test", "path": path}]
    configs.to_dataset_card_data(card.data)
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    original = hub.files()[path]
    Dataset.from_dict({"x": [2]}).push_to_hub(hub.repo_id, split="train", append=True)
    assert configured_rows(hub) == {"train": [{"x": 2}], "test": [{"x": 1}]}
    assert hub.files()[path] == original
    result = load_local_hub(hub, tmp_path)
    assert list(result["train"]["x"]) == [2]
    assert list(result["test"]["x"]) == [1]


@pytest.mark.parametrize("pattern", ["data/*.parquet", "data/**", "**/*.parquet", "data/*-00000-of-*.parquet"])
@pytest.mark.parametrize("append_options", [{}, {"num_shards": 3}, {"max_shard_size": 1}])
@pytest.mark.parametrize("recover_info", [False, True])
def test_append_bare_glob_keeps_all_mapped_files(hub, tmp_path, pattern, append_options, recover_info):
    DatasetDict(train=Dataset.from_dict({"x": [0]}), test=Dataset.from_dict({"x": [1]})).push_to_hub(hub.repo_id)
    card = hub.card()
    configs = MetadataConfigs.from_dataset_card_data(card.data)
    configs["default"]["data_files"][0]["path"] = pattern
    configs.to_dataset_card_data(card.data)
    # The glob includes the test file in train too. Its rows must remain visible
    # in both splits, with statistics describing what load_dataset actually reads.
    test_path = "data/test-00000-of-00001.parquet"
    test_bytes = hub.files()[test_path]
    info = card.data["dataset_info"]
    info["splits"][0].update(num_examples=2, num_bytes=16)
    info["dataset_size"] = 24
    info["download_size"] += len(test_bytes)
    if recover_info:
        card.data.pop("dataset_info")
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    before = load_local_hub(hub, tmp_path / "before")
    assert list(before["train"]["x"]) == [1, 0]
    assert list(before["test"]["x"]) == [1]
    hub.uploads.clear()

    Dataset.from_dict({"x": [2, 3]}).push_to_hub(hub.repo_id, append=True, **append_options)

    assert configured_rows(hub) == {"train": [{"x": 1}, {"x": 0}, {"x": 2}, {"x": 3}], "test": [{"x": 1}]}
    assert hub.files()[test_path] == test_bytes
    assert hub.downloads == ["data/train-00000-of-00001.parquet"]
    assert all(path.startswith("data/train-") for path in hub.uploads)
    info = DatasetInfosDict.from_dataset_card_data(hub.card().data)["default"]
    assert {split: stats.num_examples for split, stats in info.splits.items()} == {"train": 4, "test": 1}
    assert info.dataset_size == 40
    configs = MetadataConfigs.from_dataset_card_data(hub.card().data)
    assert info.download_size == sum(
        hub.fs.size(path)
        for patterns in sanitize_patterns(configs["default"]["data_files"]).values()
        for pattern in patterns
        for path in hub.fs.glob(hub.root + "/" + pattern)
        if path.endswith(".parquet")
    )
    result = load_local_hub(hub, tmp_path / "after")
    assert list(result["train"]["x"]) == [1, 0, 2, 3]
    assert list(result["test"]["x"]) == [1]


def test_append_recovery_respects_config_boundaries(hub, tmp_path):
    Dataset.from_dict({"x": [0]}).push_to_hub(hub.repo_id)
    Dataset.from_dict({"x": [1]}).push_to_hub(hub.repo_id, config_name="other", data_dir="data", split="test")
    card = hub.card()
    other_config = MetadataConfigs.from_dataset_card_data(card.data)["other"]
    other_info = DatasetInfosDict.from_dataset_card_data(card.data)["other"]
    for info in card.data["dataset_info"]:
        if info["config_name"] == "default":
            info.pop("download_size")
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    test_bytes = hub.files("data/test-*")
    Dataset.from_dict({"x": [2]}).push_to_hub(hub.repo_id, append=True)
    configs = MetadataConfigs.from_dataset_card_data(hub.card().data)
    assert configs["default"]["data_files"] == [{"split": "train", "path": "data/train-*"}]
    assert configs["other"] == other_config
    infos = DatasetInfosDict.from_dataset_card_data(hub.card().data)
    assert infos["other"] == other_info
    assert infos["default"].download_size == sum(map(len, hub.files("data/train-*").values()))
    assert hub.files("data/test-*") == test_bytes
    result = load_local_hub(hub, tmp_path)
    assert set(result) == {"train"}
    assert list(result["train"]["x"]) == [0, 2]


def test_append_recovery_uses_arrow_byte_counts(hub):
    Dataset.from_dict({"x": [0]}).push_to_hub(hub.repo_id)
    card = hub.card()
    card.data.pop("dataset_info")
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    Dataset.from_dict({"x": [1]}).push_to_hub(hub.repo_id, append=True)
    info = DatasetInfosDict.from_dataset_card_data(hub.card().data)["default"]
    assert info.splits["train"].num_bytes == 16
    assert info.dataset_size == 16
    assert info.splits["train"].num_examples == 2
    assert info.download_size == sum(map(len, hub.files().values()))


@pytest.mark.parametrize("missing_field", ["dataset_info", "features"])
@pytest.mark.parametrize(
    "feature,values",
    [
        (ClassLabel(names=["negative", "positive"]), [0, 1]),
        (Image(decode=False), [{"bytes": b"old image", "path": None}, {"bytes": b"new image", "path": None}]),
        (Audio(decode=False), [{"bytes": b"old audio", "path": None}, {"bytes": b"new audio", "path": None}]),
    ],
    ids=["class_label", "image", "audio"],
)
def test_append_recovers_huggingface_features(hub, tmp_path, missing_field, feature, values):
    features = Features({"x": feature})
    # Cast encoded storage so audio coverage does not require a codec installation.
    Dataset.from_dict({"x": values[:1]}).cast(features).push_to_hub(hub.repo_id)
    card = hub.card()
    if missing_field == "dataset_info":
        card.data.pop("dataset_info")
    else:
        card.data["dataset_info"].pop("features")
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())

    error = None
    try:
        Dataset.from_dict({"x": values[1:]}).cast(features).push_to_hub(hub.repo_id, append=True)
    except ValueError as caught:
        error = caught
    assert error is None, str(error)

    info = DatasetInfosDict.from_dataset_card_data(hub.card().data)["default"]
    assert info.features == features
    assert info.splits["train"].num_examples == 2
    result = load_local_hub(hub, tmp_path)
    assert result["train"].features == features
    assert list(result["train"]["x"]) == values


@pytest.mark.parametrize("null_splits", [False, True])
@pytest.mark.parametrize("as_dict", [False, True])
def test_append_missing_splits_without_parquet(hub, tmp_path, null_splits, as_dict):
    Dataset.from_dict({"x": [0]}).push_to_hub(hub.repo_id)
    card = hub.card()
    info = card.data["dataset_info"]
    info.pop("splits")
    if null_splits:
        info["splits"] = None
    info.pop("download_size")
    info.pop("dataset_size")
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    for path in hub.files():
        hub.fs.rm(hub.root + "/" + path)

    new = Dataset.from_dict({"x": [2]})
    error = None
    try:
        (DatasetDict(train=new) if as_dict else new).push_to_hub(hub.repo_id, append=True)
    except TypeError as caught:
        error = caught
    assert error is None, str(error)

    assert configured_rows(hub) == {"train": [{"x": 2}]}
    info = DatasetInfosDict.from_dataset_card_data(hub.card().data)["default"]
    assert info.splits["train"].num_examples == 1
    assert info.splits["train"].num_bytes == info.dataset_size == 8
    assert info.download_size == sum(map(len, hub.files().values()))
    assert list(load_local_hub(hub, tmp_path)["train"]["x"]) == [2]


@pytest.mark.parametrize("precision", [8, 16, 25])
def test_append_preserves_decimal_writer_properties(hub, precision):
    features = Features({"x": Value(f"decimal128({precision}, 2)"), "y": Value("int64")})
    old = Dataset.from_dict({"x": [Decimal("1.23")], "y": [0]}, features=features)
    old.push_to_hub(hub.repo_id)
    path = next(iter(hub.files()))
    buffer = BytesIO()
    pq.write_table(
        old.data.table,
        buffer,
        store_decimal_as_integer=True,
        compression={"x": "gzip", "y": "zstd"},
        use_dictionary=False,
    )
    original = buffer.getvalue()
    hub.fs.pipe_file(hub.root + "/" + path, original)
    card = hub.card()
    card.data["dataset_info"]["download_size"] = len(original)
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    error = None
    try:
        Dataset.from_dict({"x": [Decimal("4.56")], "y": [1]}, features=features).push_to_hub(hub.repo_id, append=True)
    except RuntimeError as caught:
        error = caught
    assert error is None, str(error)
    appended = hub.files()[path]
    assert appended.startswith(parquet_prefix(original))
    assert rows(hub.files()) == [{"x": Decimal("1.23"), "y": 0}, {"x": Decimal("4.56"), "y": 1}]
    metadata = pq.read_metadata(BytesIO(appended))
    assert metadata.schema.equals(pq.read_metadata(BytesIO(original)).schema)
    for column in range(metadata.num_columns):
        assert metadata.row_group(1).column(column).compression == metadata.row_group(0).column(column).compression
        assert metadata.row_group(1).column(column).encodings == metadata.row_group(0).column(column).encodings


@pytest.mark.parametrize("config_name,data_dir", [("default", None), ("fr", None), ("fr", "custom/nested")])
def test_append_preserves_prefix_rows_and_card(hub, config_name, data_dir):
    old = Dataset.from_dict({"x": list(range(7))})
    kwargs = {"config_name": config_name, "data_dir": data_dir}
    old.push_to_hub(hub.repo_id, **kwargs)
    original = hub.files()
    path = next(iter(original))
    # Exercise several row groups, including a partial last row group and page indexes.
    buffer = BytesIO()
    old.to_parquet(buffer, batch_size=3)
    hub.fs.pipe_file(hub.root + "/" + path, buffer.getvalue())
    card = hub.card()
    infos = DatasetInfosDict.from_dataset_card_data(card.data)
    infos[config_name].download_size = len(buffer.getvalue())
    infos.to_dataset_card_data(card.data)
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    hub.uploads.clear()
    for values in ([7, 8], [9]):
        Dataset.from_dict({"x": values}).push_to_hub(hub.repo_id, append=True, **kwargs)
    result = hub.files()
    assert list(result) == [path]
    assert result[path].startswith(parquet_prefix(buffer.getvalue()))
    assert rows(result) == [{"x": i} for i in range(10)]
    metadata = pq.read_metadata(BytesIO(result[path]))
    assert [metadata.row_group(i).num_rows for i in range(metadata.num_row_groups)] == [3, 3, 1, 2, 1]
    info = DatasetInfosDict.from_dataset_card_data(hub.card().data)[config_name]
    assert info.splits["train"].num_examples == 10
    assert info.splits["train"].num_bytes == 80
    assert info.dataset_size == 80
    assert info.download_size == len(result[path])
    assert hub.uploads == [path, path]
    assert all(not isinstance(op, (CommitOperationCopy, CommitOperationDelete)) for op in hub.commits[-1])


def test_append_feature_mismatch_leaves_repository_unchanged(hub):
    Dataset.from_dict({"x": [1]}).push_to_hub(hub.repo_id)
    before = hub.files("*")
    with pytest.raises(ValueError, match="[Ff]eatures.*match"):
        Dataset.from_dict({"x": ["wrong"]}).push_to_hub(hub.repo_id, append=True)
    assert hub.files("*") == before


def test_append_overflow_renumbers_using_copies(hub):
    old = Dataset.from_dict({"x": list(range(8))})
    old.push_to_hub(hub.repo_id, num_shards=2)
    original = hub.files()
    hub.uploads.clear()
    Dataset.from_dict({"x": [8, 9]}).push_to_hub(
        hub.repo_id, append=True, max_shard_size=max(map(len, original.values()))
    )
    result = hub.files()
    assert sorted(result) == [f"data/train-{i:05d}-of-00003.parquet" for i in range(3)]
    for i, data in enumerate(original.values()):
        assert result[f"data/train-{i:05d}-of-00003.parquet"] == data
    assert rows(result) == [{"x": i} for i in range(10)]
    assert hub.uploads == ["data/train-00002-of-00003.parquet"]
    assert sum(isinstance(op, CommitOperationCopy) for op in hub.commits[-1]) == 2
    assert sum(isinstance(op, CommitOperationDelete) for op in hub.commits[-1]) == 2
    info = DatasetInfosDict.from_dataset_card_data(hub.card().data)["default"]
    assert info.splits["train"].num_examples == 10
    assert info.splits["train"].num_bytes == 80
    assert info.download_size == sum(map(len, result.values()))


def test_append_dict_preserves_other_splits_configs_and_paths(hub):
    old = Dataset.from_dict({"x": [0, 1]})
    DatasetDict(train=old, test=old).push_to_hub(hub.repo_id)
    old.push_to_hub(hub.repo_id, config_name="fr")
    before = hub.files()
    DatasetDict(train=Dataset.from_dict({"x": [2]}), validation=old).push_to_hub(
        hub.repo_id, append=True, data_dir="more"
    )
    for path, data in before.items():
        if path == "data/train-00000-of-00001.parquet":
            assert hub.files()[path].startswith(parquet_prefix(data))
        else:
            assert hub.files()[path] == data
    info = DatasetInfosDict.from_dataset_card_data(hub.card().data)["default"]
    assert {name: split.num_examples for name, split in info.splits.items()} == {
        "train": 3,
        "test": 2,
        "validation": 2,
    }
    configs = MetadataConfigs.from_dataset_card_data(hub.card().data)
    assert configs["default"]["data_files"] == [
        {"split": "train", "path": "data/train-*"},
        {"split": "test", "path": "data/test-*"},
        {"split": "validation", "path": "more/validation-*"},
    ]
    assert "fr" in configs
    assert configured_rows(hub) == {
        "train": [{"x": 0}, {"x": 1}, {"x": 2}],
        "test": [{"x": 0}, {"x": 1}],
        "validation": [{"x": 0}, {"x": 1}],
    }


@pytest.mark.parametrize("as_dict", [False, True])
def test_append_false_is_identical_to_default(hub, as_dict):
    data = Dataset.from_dict({"x": [1, 2]})
    dset = DatasetDict(train=data) if as_dict else data
    dset.push_to_hub(hub.repo_id)
    expected = hub.files("*")
    dset.push_to_hub(hub.repo_id, append=False)
    assert hub.files("*") == expected
    new = Dataset.from_dict({"x": [3]})
    (DatasetDict(train=new) if as_dict else new).push_to_hub(hub.repo_id, append=False)
    assert rows(hub.files()) == [{"x": 3}]


def test_append_new_split_is_normal_push(hub):
    data = Dataset.from_dict({"x": [1, 2]})
    data.push_to_hub(hub.repo_id, append=True)
    appended = hub.files("*")
    data.push_to_hub(hub.repo_id)
    assert hub.files("*") == appended


def test_append_num_shards_is_total_and_cannot_remove_shards(hub):
    data = Dataset.from_dict({"x": [1, 2]})
    data.push_to_hub(hub.repo_id, num_shards=2)
    with pytest.raises(ValueError, match="num_shards"):
        data.push_to_hub(hub.repo_id, append=True, num_shards=1)
    data.push_to_hub(hub.repo_id, append=True, num_shards=3)
    assert len(hub.files()) == 3
    assert rows(hub.files()) == [{"x": 1}, {"x": 2}, {"x": 1}, {"x": 2}]


def test_append_empty_keeps_data(hub):
    Dataset.from_dict({"x": [1]}).push_to_hub(hub.repo_id)
    before = hub.files("*")
    Dataset.from_dict({"x": []}, features=Features({"x": Value("int64")})).push_to_hub(hub.repo_id, append=True)
    assert hub.files("*") == before


def test_append_only_downloads_and_uploads_last_shard(hub):
    Dataset.from_dict({"x": list(range(6))}).push_to_hub(hub.repo_id, num_shards=3)
    before = hub.files()
    hub.uploads.clear()
    Dataset.from_dict({"x": [6]}).with_format("numpy").push_to_hub(hub.repo_id, append=True)
    paths = sorted(before)
    assert hub.downloads == [paths[-1]]
    assert hub.uploads == [paths[-1]]
    assert all(hub.files()[path] == before[path] for path in paths[:-1])
    assert hub.files()[paths[-1]].startswith(parquet_prefix(before[paths[-1]]))
    assert rows(hub.files()) == [{"x": i} for i in range(7)]


def test_append_updates_explicit_card_paths_when_renumbering(hub):
    Dataset.from_dict({"x": [1, 2]}).push_to_hub(hub.repo_id)
    old_path = next(iter(hub.files()))
    card = hub.card()
    configs = MetadataConfigs.from_dataset_card_data(card.data)
    configs["default"]["data_files"] = [{"split": "train", "path": old_path}]
    configs.to_dataset_card_data(card.data)
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    Dataset.from_dict({"x": [3]}).push_to_hub(hub.repo_id, append=True, num_shards=2)
    data_files = MetadataConfigs.from_dataset_card_data(hub.card().data)["default"]["data_files"]
    assert data_files == [{"split": "train", "path": "data/train-*"}]
    assert rows(hub.files()) == [{"x": 1}, {"x": 2}, {"x": 3}]


def test_append_without_card_info_preserves_counts(hub):
    Dataset.from_dict({"x": [1, 2]}).push_to_hub(hub.repo_id)
    card = hub.card()
    card.data.pop("dataset_info")
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    Dataset.from_dict({"x": [3]}).push_to_hub(hub.repo_id, append=True)
    info = DatasetInfosDict.from_dataset_card_data(hub.card().data)["default"]
    assert info.splits["train"].num_examples == 3
    assert info.download_size == sum(map(len, hub.files().values()))


def test_append_updates_legacy_info(hub):
    from dataclasses import asdict

    Dataset.from_dict({"x": [1, 2]}).push_to_hub(hub.repo_id)
    info = DatasetInfosDict.from_dataset_card_data(hub.card().data)["default"]
    hub.fs.pipe_file(hub.root + "/dataset_infos.json", json.dumps({"default": asdict(info)}).encode())
    Dataset.from_dict({"x": [3]}).push_to_hub(hub.repo_id, append=True)
    legacy = json.loads(hub.fs.cat_file(hub.root + "/dataset_infos.json"))["default"]
    assert legacy["splits"]["train"]["num_examples"] == 3
    assert legacy["splits"]["train"]["num_bytes"] == 24
    assert legacy["download_size"] == sum(map(len, hub.files().values()))


def test_append_embeds_media(hub, tmp_path):
    from datasets import Image

    features = Features({"image": Image(decode=False)})
    image_path = tmp_path / "image.png"
    image_path.write_bytes(b"local image contents")
    Dataset.from_dict({"image": [str(image_path)]}, features=features).push_to_hub(hub.repo_id)
    before = next(iter(hub.files().values()))
    Dataset.from_dict({"image": [str(image_path)]}, features=features).push_to_hub(hub.repo_id, append=True)
    assert next(iter(hub.files().values())).startswith(parquet_prefix(before))
    assert [row["image"]["bytes"] for row in rows(hub.files())] == [b"local image contents"] * 2


@pytest.mark.parametrize("arrow_version,cdc", [("20.0.0", False), ("21.0.0", True)])
def test_append_parquet_cdc_version_gate(hub, tmp_path, monkeypatch, arrow_version, cdc):
    from packaging.version import parse

    from datasets import config
    from datasets.io.parquet import _append_parquet_file

    original = tmp_path / "original.parquet"
    destination = tmp_path / "appended.parquet"
    Dataset.from_dict({"x": [1]}).to_parquet(original)
    writer = pq.ParquetWriter
    options = []

    def checked_writer(*args, **kwargs):
        options.append(kwargs)
        return writer(*args, **kwargs)

    monkeypatch.setattr(config, "PYARROW_VERSION", parse(arrow_version))
    monkeypatch.setattr(pq, "ParquetWriter", checked_writer)
    _append_parquet_file(Dataset.from_dict({"x": [2]}), str(original), str(destination))
    assert options[0].get("use_content_defined_chunking", False) is cdc
    assert destination.read_bytes().startswith(parquet_prefix(original.read_bytes()))
    assert pq.read_table(destination).to_pydict() == {"x": [1, 2]}


@pytest.mark.parametrize("data_dir", ["./data", "data/", ".", "./custom/nested/"])
def test_append_normalizes_data_dir_without_replacing_rows(hub, data_dir):
    Dataset.from_dict({"x": [1, 2]}).push_to_hub(hub.repo_id, data_dir=Path(data_dir).as_posix())
    Dataset.from_dict({"x": [3]}).push_to_hub(hub.repo_id, data_dir=data_dir, append=True)
    assert rows(hub.files()) == [{"x": 1}, {"x": 2}, {"x": 3}]
    assert len(hub.files()) == 1


@pytest.mark.parametrize("pattern", ["data/*.parquet", "data/**", "**/*.parquet", "./data/train-*.parquet"])
def test_append_card_patterns_do_not_duplicate_rows(hub, pattern):
    Dataset.from_dict({"x": [1, 2]}).push_to_hub(hub.repo_id)
    card = hub.card()
    configs = MetadataConfigs.from_dataset_card_data(card.data)
    configs["default"]["data_files"] = [{"split": "train", "path": pattern}]
    configs.to_dataset_card_data(card.data)
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    Dataset.from_dict({"x": [3]}).push_to_hub(hub.repo_id, append=True)
    paths = MetadataConfigs.from_dataset_card_data(hub.card().data)["default"]["data_files"][0]["path"]
    patterns = paths if isinstance(paths, list) else [paths]
    resolved = [
        path
        for pattern in patterns
        for path in hub.fs.glob(hub.root + "/" + pattern.removeprefix("./"))
        if path.endswith(".parquet")
    ]
    assert len(resolved) == len(set(resolved)) == 1


def test_append_old_nested_parquet_encoding(hub, tmp_path):
    from datasets.io.parquet import _append_parquet_file

    old = Dataset.from_dict({"x": [[1, 2], [3]]})
    original, appended = tmp_path / "old.parquet", tmp_path / "appended.parquet"
    pq.write_table(old.data.table, original, use_compliant_nested_type=False)
    _append_parquet_file(Dataset.from_dict({"x": [[4]]}), str(original), str(appended))
    assert appended.read_bytes().startswith(parquet_prefix(original.read_bytes()))
    assert pq.read_table(appended).to_pydict() == {"x": [[1, 2], [3], [4]]}


def test_append_recovers_only_missing_card_fields(hub):
    DatasetDict(train=Dataset.from_dict({"x": [1, 2]}), test=Dataset.from_dict({"x": [0]})).push_to_hub(hub.repo_id)
    card = hub.card()
    card.data["dataset_info"].pop("download_size")
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    Dataset.from_dict({"x": [3]}).push_to_hub(hub.repo_id, append=True)
    info = DatasetInfosDict.from_dataset_card_data(hub.card().data)["default"]
    assert info.splits["train"].num_bytes == 24
    assert info.splits["test"].num_bytes == 8
    assert info.dataset_size == 32
    assert info.download_size == sum(map(len, hub.files().values()))
    assert MetadataConfigs.from_dataset_card_data(hub.card().data)["default"]["data_files"] == [
        {"split": "train", "path": "data/train-*"},
        {"split": "test", "path": "data/test-*"},
    ]


def test_append_new_non_train_split_is_normal_push(hub):
    data = Dataset.from_dict({"x": [1]})
    data.push_to_hub(hub.repo_id, append=True, split="test")
    assert MetadataConfigs.from_dataset_card_data(hub.card().data)["default"]["data_files"] == [
        {"split": "test", "path": "data/test-*"}
    ]


def test_append_dict_updates_existing_splits_additively(hub):
    data = Dataset.from_dict({"x": [0, 1]})
    DatasetDict(train=data, validation=data, test=data).push_to_hub(hub.repo_id)
    test_path = "data/test-00000-of-00001.parquet"
    test_bytes = hub.files()[test_path]
    DatasetDict(train=Dataset.from_dict({"x": [2]}), validation=Dataset.from_dict({"x": [3, 4]})).push_to_hub(
        hub.repo_id, append=True
    )
    assert rows(hub.files("data/train-*")) == [{"x": 0}, {"x": 1}, {"x": 2}]
    assert rows(hub.files("data/validation-*")) == [{"x": 0}, {"x": 1}, {"x": 3}, {"x": 4}]
    assert hub.files()[test_path] == test_bytes
    info = DatasetInfosDict.from_dataset_card_data(hub.card().data)["default"]
    assert info.dataset_size == 72
    assert info.download_size == sum(map(len, hub.files().values()))
    assert {name: split.num_examples for name, split in info.splits.items()} == {
        "train": 3,
        "validation": 4,
        "test": 2,
    }


def test_append_overflow_splits_large_new_data(hub):
    Dataset.from_dict({"x": list(range(8))}).push_to_hub(hub.repo_id)
    original = next(iter(hub.files().values()))
    limit = len(original)
    Dataset.from_dict({"x": list(range(8, 208))}).push_to_hub(hub.repo_id, append=True, max_shard_size=limit)
    files = hub.files()
    assert len(files) > 2
    assert all(len(data) <= limit for data in files.values())
    assert next(iter(files.values())) == original
    assert rows(files) == [{"x": i} for i in range(208)]


def test_append_empty_media_keeps_data(hub):
    from datasets import Image

    features = Features({"image": Image(decode=False)})
    Dataset.from_dict({"image": [{"bytes": b"image", "path": None}]}, features=features).push_to_hub(hub.repo_id)
    before = hub.files("*")
    Dataset.from_dict({"image": []}, features=features).push_to_hub(hub.repo_id, append=True)
    assert hub.files("*") == before


def test_append_old_int96_parquet_encoding(hub, tmp_path):
    from datetime import datetime

    from datasets.io.parquet import _append_parquet_file

    data = Dataset.from_dict({"x": [datetime(2020, 1, 1)]}, features=Features({"x": Value("timestamp[ns]")}))
    original, appended = tmp_path / "old.parquet", tmp_path / "appended.parquet"
    pq.write_table(data.data.table, original, use_deprecated_int96_timestamps=True)
    _append_parquet_file(data, str(original), str(appended))
    assert appended.read_bytes().startswith(parquet_prefix(original.read_bytes()))
    assert pq.read_table(appended).num_rows == 2


def test_append_card_patterns_cover_untouched_shards_once(hub):
    Dataset.from_dict({"x": [0, 1]}).push_to_hub(hub.repo_id, num_shards=2)
    card = hub.card()
    configs = MetadataConfigs.from_dataset_card_data(card.data)
    configs["default"]["data_files"] = [
        {"split": "train", "path": ["data/*-00000-of-*.parquet", "data/train-00001-of-00002.parquet"]}
    ]
    configs.to_dataset_card_data(card.data)
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    Dataset.from_dict({"x": [2]}).push_to_hub(hub.repo_id, append=True)
    patterns = MetadataConfigs.from_dataset_card_data(hub.card().data)["default"]["data_files"][0]["path"]
    patterns = patterns if isinstance(patterns, list) else [patterns]
    paths = [path for pattern in patterns for path in hub.fs.glob(hub.root + "/" + pattern)]
    assert len(paths) == len(set(paths)) == 2


def test_append_card_patterns_include_nested_directory(hub):
    Dataset.from_dict({"x": [0]}).push_to_hub(hub.repo_id)
    card = hub.card()
    configs = MetadataConfigs.from_dataset_card_data(card.data)
    configs["default"]["data_files"] = [{"split": "train", "path": "data/*.parquet"}]
    configs.to_dataset_card_data(card.data)
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    Dataset.from_dict({"x": [1]}).push_to_hub(hub.repo_id, append=True, data_dir="data/nested", num_shards=2)
    patterns = MetadataConfigs.from_dataset_card_data(hub.card().data)["default"]["data_files"][0]["path"]
    patterns = patterns if isinstance(patterns, list) else [patterns]
    paths = [path for pattern in patterns for path in hub.fs.glob(hub.root + "/" + pattern)]
    assert len(paths) == len(set(paths)) == 2


@pytest.mark.parametrize("config_name", ["default", "fr"])
def test_append_without_configs_keeps_other_splits(hub, config_name):
    data = Dataset.from_dict({"x": [0]})
    DatasetDict(train=data, test=data).push_to_hub(hub.repo_id, config_name=config_name)
    card = hub.card()
    card.data.pop("configs")
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    data.push_to_hub(hub.repo_id, config_name=config_name, append=True)
    data_files = MetadataConfigs.from_dataset_card_data(hub.card().data)[config_name]["data_files"]
    assert {item["split"] for item in data_files} == {"train", "test"}


def test_append_infers_both_known_directories_without_configs(hub):
    data = Dataset.from_dict({"x": [2]})
    seed_train_directories(hub)
    card = hub.card()
    card.data.pop("configs")
    hub.fs.pipe_file(hub.root + "/README.md", str(card).encode())
    data.push_to_hub(hub.repo_id, data_dir="more", append=True)
    patterns = MetadataConfigs.from_dataset_card_data(hub.card().data)["default"]["data_files"][0]["path"]
    assert set(patterns) == {"data/train-*", "more/train-*"}
    assert configured_rows(hub) == {"train": [{"x": 0}, {"x": 1}, {"x": 2}]}
