from types import SimpleNamespace

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

import datasets
from datasets import DownloadConfig, load_dataset
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.parquet import parquet as parquet_module
from datasets.packaged_modules.parquet.parquet import ParquetConfig, _get_cached_file


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = ParquetConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = ParquetConfig(name="name", data_files=data_files)


def test_parquet_reshard(multi_row_groups_parquet_path):
    ds = load_dataset("parquet", data_files=multi_row_groups_parquet_path, split="train", streaming=True)
    assert ds.num_shards == 1
    expected = list(ds)
    resharded_ds = ds.reshard()
    assert resharded_ds.num_shards == 4
    assert list(resharded_ds) == expected


def test_parquet_columns(parquet_path):
    ds = load_dataset("parquet", data_files=parquet_path, split="train", streaming=True)
    full_features = ds.features
    assert len(ds.features) == 3
    assert len(next(iter(ds))) == 3
    ds = load_dataset("parquet", data_files=parquet_path, split="train", streaming=True, columns=["col_1"])
    assert len(ds.features) == 1
    assert len(next(iter(ds))) == 1
    ds = load_dataset(
        "parquet", data_files=parquet_path, split="train", streaming=True, columns=["col_1"], features=full_features
    )
    assert len(ds.features) == 1
    assert len(next(iter(ds))) == 1


@pytest.fixture
def remote_parquet_url(mockfs):
    table = pa.table({"text": ["a", "b", "c"], "label": [0, 1, 0], "extra": [b"x" * 100] * 3})
    with mockfs.open("data/train.parquet", "wb") as f:
        pq.write_table(table, f, row_group_size=2)
    return "mock://data/train.parquet"


def _fail_on_download(*args, **kwargs):
    raise AssertionError("the file should be read remotely instead of being downloaded")


@pytest.mark.parametrize("num_proc", [None, 2])
def test_parquet_columns_reads_remote_files_without_downloading_them(
    remote_parquet_url, mockfs, monkeypatch, num_proc, tmp_path
):
    monkeypatch.setattr(datasets.download.download_manager, "cached_path", _fail_on_download)
    ds = load_dataset(
        "parquet",
        data_files=remote_parquet_url,
        columns=["text", "label"],
        split="train",
        storage_options=mockfs.storage_options,
        cache_dir=str(tmp_path / "cache"),
        num_proc=num_proc,
    )
    assert ds.to_dict() == {"text": ["a", "b", "c"], "label": [0, 1, 0]}


def test_parquet_columns_reads_local_copy_of_remote_file_if_cached(remote_parquet_url, mockfs, monkeypatch, tmp_path):
    local_copy = tmp_path / "train.parquet"
    pq.write_table(pa.table({"text": ["cached"], "label": [1]}), local_copy)
    monkeypatch.setattr(datasets.download.download_manager, "cached_path", _fail_on_download)
    monkeypatch.setattr(parquet_module, "_get_cached_file", lambda file, download_config: str(local_copy))
    ds = load_dataset(
        "parquet",
        data_files=remote_parquet_url,
        columns=["text"],
        split="train",
        storage_options=mockfs.storage_options,
        cache_dir=str(tmp_path / "cache"),
    )
    assert ds.to_dict() == {"text": ["cached"]}


@pytest.mark.parametrize("columns", [None, ["text"]])
@pytest.mark.parametrize("num_proc", [None, 2])
def test_parquet_reads_remote_files_with_storage_options_of_download_config(
    remote_parquet_url, mockfs, columns, num_proc, tmp_path
):
    ds = load_dataset(
        "parquet",
        data_files=remote_parquet_url,
        columns=columns,
        split="train",
        download_config=DownloadConfig(storage_options=mockfs.storage_options),
        cache_dir=str(tmp_path / "cache"),
        num_proc=num_proc,
    )
    assert ds["text"] == ["a", "b", "c"]


@pytest.mark.parametrize("columns, offline", [(None, False), (["text"], True)])
def test_parquet_downloads_remote_files_without_columns_or_offline(
    remote_parquet_url, mockfs, monkeypatch, columns, offline, tmp_path
):
    downloaded = []
    local_copy = tmp_path / "train.parquet"
    with mockfs.open("data/train.parquet", "rb") as f:
        local_copy.write_bytes(f.read())

    def track_cached_path(url_or_filename, *args, **kwargs):
        # stands for the download cache, which is the only source of remote files in offline mode
        downloaded.append(url_or_filename)
        return str(local_copy)

    monkeypatch.setattr(datasets.download.download_manager, "cached_path", track_cached_path)
    monkeypatch.setattr(datasets.config, "HF_HUB_OFFLINE", offline)
    ds = load_dataset(
        "parquet",
        data_files=remote_parquet_url,
        columns=columns,
        split="train",
        storage_options=mockfs.storage_options,
        cache_dir=str(tmp_path / "cache"),
    )
    assert downloaded == [remote_parquet_url]
    assert ds.column_names == (columns or ["text", "label", "extra"])


def test_parquet_get_cached_file(monkeypatch, tmp_path):
    cached_file = tmp_path / "train.parquet"
    cached_file.touch()
    revision = "0123456789abcdef0123456789abcdef01234567"
    requested = []

    class FakeHfFileSystem:
        def __init__(self, **kwargs):
            pass

        def resolve_path(self, path):
            repo_id_and_revision, path_in_repo = path[len("hf://datasets/") :].split("/data/")
            repo_id, revision = repo_id_and_revision.split("@")
            return SimpleNamespace(
                repo_id=repo_id, revision=revision, repo_type="dataset", path_in_repo="data/" + path_in_repo
            )

    def try_to_load_from_cache(repo_id, filename, revision=None, repo_type=None):
        requested.append((repo_id, filename, revision, repo_type))
        return str(cached_file) if filename == "data/train.parquet" else None

    monkeypatch.setattr(parquet_module.huggingface_hub, "HfFileSystem", FakeHfFileSystem)
    monkeypatch.setattr(parquet_module.huggingface_hub, "try_to_load_from_cache", try_to_load_from_cache)
    download_config = DownloadConfig()
    url = f"hf://datasets/user/name@{revision}/data/"
    assert _get_cached_file(url + "train.parquet", download_config) == str(cached_file)
    assert requested == [("user/name", "data/train.parquet", revision, "dataset")]
    assert _get_cached_file(url + "test.parquet", download_config) is None
    assert _get_cached_file("hf://buckets/user/name/data/train.parquet", download_config) is None
    assert _get_cached_file("mock://data/train.parquet", download_config) is None
