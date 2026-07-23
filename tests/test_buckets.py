"""Regression tests for the storage-bucket (``buckets/...``) read/write code paths.

Each test targets one fix and is written to fail on the pre-fix code:

1. `test_bucket_module_uses_dataset_card_data_not_card`  -> src/datasets/load.py
2. `test_bucket_module_preserves_card_when_standalone_yaml_missing` -> src/datasets/load.py
3. `test_push_parquet_shards_reports_dataset_nbytes` -> src/datasets/iterable_dataset.py
4. `test_get_updated_dataset_card_returns_legacy_infos_as_dict` -> src/datasets/arrow_dataset.py

The full bucket read/write flow needs live Hub credentials; these drive the exact
buggy code in isolation over in-memory filesystems / stubbed uploads instead.
"""

import io
import json
from dataclasses import asdict
from unittest.mock import MagicMock

import pytest
from fsspec.implementations.dirfs import DirFileSystem
from fsspec.implementations.memory import MemoryFileSystem

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


class _FakeHfFileSystem:
    """Minimal in-memory stand-in for ``HfFileSystem``, keyed by basename."""

    def __init__(self, files):
        self._files = dict(files)

    @staticmethod
    def _basename(path):
        return str(path).rstrip("/").rsplit("/", 1)[-1]

    def read_text(self, path, **kwargs):
        name = self._basename(path)
        if name in self._files:
            return self._files[name]
        raise FileNotFoundError(path)

    def exists(self, path):
        return self._basename(path) in self._files

    def isfile(self, path):
        return self._basename(path) in self._files

    def open(self, path, *args, **kwargs):
        name = self._basename(path)
        if name in self._files:
            return io.StringIO(self._files[name])
        raise FileNotFoundError(path)


def _load_bucket_module(monkeypatch, files):
    """Run ``HubBucketDatasetModuleFactory.get_module()`` against an in-memory FS,
    stubbing out the network-bound data-file resolution so only the card / metadata
    handling under test runs for real."""
    fake_fs = _FakeHfFileSystem(files)
    monkeypatch.setattr(datasets_load, "HfFileSystem", lambda **kwargs: fake_fs)
    monkeypatch.setattr(
        datasets_load.DataFilesDict,
        "from_patterns",
        classmethod(lambda cls, *args, **kwargs: MagicMock(name="DataFilesDict")),
    )
    monkeypatch.setattr(datasets_load, "infer_module_for_data_files", lambda *args, **kwargs: ("parquet", {}))
    monkeypatch.setattr(
        datasets_load, "create_builder_configs_from_metadata_configs", lambda *args, **kwargs: ([], "default")
    )
    factory = HubBucketDatasetModuleFactory("buckets/ns/name", download_config=DownloadConfig())
    return factory.get_module()


@pytest.mark.unit
def test_bucket_module_uses_dataset_card_data_not_card(monkeypatch):
    """Fix 1 (load.py): the factory must pass ``DatasetCard.data`` to the metadata
    parsers. Passing the ``DatasetCard`` object raises
    ``AttributeError: 'DatasetCard' object has no attribute 'get'`` on load.

    A standalone YAML is present here so the failure isolates fix 1 (fix 2's
    ``except`` branch is not reached).
    """
    module = _load_bucket_module(
        monkeypatch,
        {config.REPOCARD_FILENAME: README_WITH_CONFIG, config.REPOYAML_FILENAME: "license: mit\n"},
    )
    assert "default" in module.builder_configs_parameters.metadata_configs


@pytest.mark.unit
def test_bucket_module_preserves_card_when_standalone_yaml_missing(monkeypatch):
    """Fix 2 (load.py): when the standalone ``.huggingface.yaml`` is absent, the
    parsed README card must survive. The buggy ``except FileNotFoundError`` reset
    ``dataset_card_data`` to an empty ``DatasetCardData``, dropping the configs.
    """
    module = _load_bucket_module(monkeypatch, {config.REPOCARD_FILENAME: README_WITH_CONFIG})
    metadata_configs = module.builder_configs_parameters.metadata_configs
    assert "default" in metadata_configs
    assert metadata_configs["default"]["data_files"] == [{"split": "train", "path": "data/train-*"}]


@pytest.mark.unit
def test_push_parquet_shards_reports_dataset_nbytes(monkeypatch):
    """Fix 3 (iterable_dataset.py): the collector must accumulate the worker's
    ``dataset_nbytes`` into ``SplitInfo.num_bytes``. The buggy code unpacked that
    4th tuple element as ``uploaded_size`` and left ``num_bytes`` at 0.
    """

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
    assert split_info.num_bytes == 4242
    assert split_info.num_examples == 3


@pytest.mark.unit
def test_get_updated_dataset_card_returns_legacy_infos_as_dict():
    """Fix 4 (arrow_dataset.py): ``_get_updated_dataset_card`` must return the legacy
    dataset_infos as a ``dict`` (its declared ``Optional[dict]``), which the call
    sites ``json.dumps`` once. The buggy line serialized the wrong variable
    (``dataset_infos``), which is unbound when no README exists -> ``UnboundLocalError``.
    """
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

    assert isinstance(new_legacy_dataset_infos, dict)
    assert "default" in new_legacy_dataset_infos
    # What gets written to dataset_infos.json parses back to an object, not a string.
    assert isinstance(json.loads(json.dumps(new_legacy_dataset_infos)), dict)
