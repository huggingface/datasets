import pytest

import datasets.config
from datasets.utils.info_utils import is_small_dataset


@pytest.mark.parametrize("dataset_size", [None, 400 * 2 ** 20, 600 * 2 ** 20])
@pytest.mark.parametrize("max_in_memory_dataset_size", ["default", 0, 100 * 2 ** 20, 900 * 2 ** 20])
def test_is_small_dataset(dataset_size, max_in_memory_dataset_size, monkeypatch):
    if max_in_memory_dataset_size == "default":
        # default = 250 * 2 ** 20
        max_in_memory_dataset_size = datasets.config.MAX_IN_MEMORY_DATASET_SIZE_IN_BYTES
    else:
        monkeypatch.setattr(datasets.config, "MAX_IN_MEMORY_DATASET_SIZE_IN_BYTES", max_in_memory_dataset_size)
    if dataset_size and max_in_memory_dataset_size:
        expected = dataset_size < max_in_memory_dataset_size
    else:
        expected = False
    result = is_small_dataset(dataset_size)
    assert result == expected
