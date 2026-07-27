import json
import posixpath
from dataclasses import asdict

import pytest
from fsspec.implementations.dirfs import DirFileSystem
from fsspec.implementations.memory import MemoryFileSystem

import datasets.data_files as datasets_data_files
import datasets.load as datasets_load
from datasets import DownloadConfig, config
from datasets.arrow_dataset import _get_updated_dataset_card
from datasets.features import Features, Value
from datasets.info import DatasetInfo
from datasets.iterable_dataset import IterableDataset
from datasets.load import HubBucketDatasetModuleFactory
from datasets.splits import SplitDict, SplitInfo


README_WITH_CONFIG = (
    "---\nconfigs:\n- config_name: default\n  data_files:\n  - split: train\n    path: data/train-*\n---\n"
)


def _load_bucket_module(monkeypatch, files, path="buckets/ns/name"):
    # run get_module() over an in-memory FS, stubbing the network-bound data-file
    # resolution so only the card / metadata handling under test runs for real
    mem = MemoryFileSystem(skip_instance_cache=True)
    # Write files with full paths relative to the bucket path (forward slashes for MemoryFileSystem)
    for filename, content in files.items():
        full_path = posixpath.join("/", path, filename)
        mem.open(full_path, "w").write(content)

    fake_fs = mem

    def fake_hffs(**kwargs):
        return fake_fs

    monkeypatch.setattr(datasets_load, "HfFileSystem", fake_hffs)
    monkeypatch.setattr(datasets_data_files, "url_to_fs", lambda pattern, **kwargs: (fake_fs, pattern))
    monkeypatch.setattr(
        datasets_load.DataFilesDict,
        "from_patterns",
        classmethod(lambda cls, *args, **kwargs: datasets_load.DataFilesDict({})),
    )
    monkeypatch.setattr(datasets_load, "infer_module_for_data_files", lambda *args, **kwargs: ("parquet", {}))
    monkeypatch.setattr(
        datasets_load, "create_builder_configs_from_metadata_configs", lambda *args, **kwargs: ([], "default")
    )
    monkeypatch.setattr(datasets_load, "get_data_patterns", lambda *args, **kwargs: {})
    # Use forward-slash join to match MemoryFileSystem conventions (avoids Windows backslash issues)
    monkeypatch.setattr(datasets_load, "xjoin", posixpath.join)
    factory = HubBucketDatasetModuleFactory(path, download_config=DownloadConfig())
    return factory.get_module()


@pytest.mark.unit
def test_bucket_module_uses_dataset_card_data_not_card(monkeypatch):
    # get_module() must pass DatasetCard.data, not the DatasetCard, to the metadata
    # parsers. A standalone YAML is present so this isolates the .data fix.
    module = _load_bucket_module(
        monkeypatch,
        {config.REPOCARD_FILENAME: README_WITH_CONFIG, config.REPOYAML_FILENAME: "license: mit\n"},
    )
    assert "default" in module.builder_configs_parameters.metadata_configs


@pytest.mark.unit
def test_bucket_module_preserves_card_when_standalone_yaml_missing(monkeypatch):
    # when the standalone .huggingface.yaml is absent, the parsed README card must
    # survive (the buggy except branch reset it to an empty DatasetCardData)
    module = _load_bucket_module(monkeypatch, {config.REPOCARD_FILENAME: README_WITH_CONFIG})
    metadata_configs = module.builder_configs_parameters.metadata_configs
    assert "default" in metadata_configs
    assert metadata_configs["default"]["data_files"] == [{"split": "train", "path": "data/train-*"}]


@pytest.mark.unit
def test_push_parquet_shards_reports_dataset_nbytes(monkeypatch):
    def gen():
        for i in range(3):
            yield {"x": i}

    ds = IterableDataset.from_generator(gen)
    # (additions, new_parquet_paths, features, dataset_nbytes, num_examples)
    worker_output = ([], [], ds.features, 4242, 3)

    def fake_single(**kwargs):
        yield 0, True, worker_output

    monkeypatch.setattr(IterableDataset, "_push_parquet_shards_to_hub_single", fake_single)

    _, _, _, split_info, _ = ds._push_parquet_shards_to_hub(
        resolved_output_path=None,
        data_dir="data",
        split="train",
        token=None,
        create_pr=False,
        max_shard_size=None,
        num_shards=1,
        embed_external_files=False,
        num_proc=None,
    )
    # dataset_nbytes must reach SplitInfo.num_bytes (was dropped -> 0)
    assert split_info.num_bytes == 4242
    assert split_info.num_examples == 3


@pytest.mark.unit
def test_get_updated_dataset_card_returns_legacy_infos_as_dict():
    mem = MemoryFileSystem(skip_instance_cache=True)
    fs = DirFileSystem("/repo", fs=mem)

    existing = {
        "default": asdict(
            DatasetInfo(config_name="default", features=Features({"x": Value("int64")}), splits=SplitDict())
        )
    }
    with fs.open(config.DATASETDICT_INFOS_FILENAME, "w") as f:
        f.write(json.dumps(existing))

    _, new_legacy_dataset_infos = _get_updated_dataset_card(
        fs=fs,
        config_name="default",
        splits_info=[SplitInfo(name="train", num_bytes=123, num_examples=1)],
        features=Features({"x": Value("int64")}),
        data_dir="data",
        set_default=None,
        uploaded_sizes=[456],
        deleted_sizes=[0],
        remove_other_splits=False,
    )

    # must be a dict (Optional[dict]) so the call site json.dumps writes an object, not a string
    assert isinstance(new_legacy_dataset_infos, dict)
    assert "default" in new_legacy_dataset_infos
    assert isinstance(json.loads(json.dumps(new_legacy_dataset_infos)), dict)
