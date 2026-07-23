import json
from dataclasses import asdict

import pytest
from fsspec.implementations.dirfs import DirFileSystem
from fsspec.implementations.memory import MemoryFileSystem

from datasets import config
from datasets.arrow_dataset import _get_updated_dataset_card
from datasets.features import Features, Value
from datasets.info import DatasetInfo
from datasets.splits import SplitDict, SplitInfo


@pytest.mark.unit
def test_get_updated_dataset_card_returns_legacy_infos_as_dict():
    """Regression test: `_get_updated_dataset_card` must return the legacy dataset_infos as a
    plain ``dict`` (its declared ``Optional[dict]`` return type), not a pre-serialized JSON string.

    The call sites in ``_push_to_repo`` / ``_push_to_bucket`` ``json.dumps`` the returned value
    once before upload. When the helper returned ``json.dumps(...)`` itself, the value was encoded
    twice, so ``dataset_infos.json`` was written as a JSON *string* instead of a JSON *object*.
    """
    mem = MemoryFileSystem(skip_instance_cache=True)
    fs = DirFileSystem("/repo", fs=mem)

    # Seed an existing legacy dataset_infos.json so the legacy branch is exercised.
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

    # Must be a dict, so the single json.dumps at the call site writes a JSON object.
    assert isinstance(new_legacy_dataset_infos, dict)
    assert "default" in new_legacy_dataset_infos
    # What gets written to dataset_infos.json parses back to an object, not a string.
    written = json.loads(json.dumps(new_legacy_dataset_infos))
    assert isinstance(written, dict)
