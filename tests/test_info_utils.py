import pytest

import datasets.config
from datasets.utils.info_utils import is_small_dataset


@pytest.mark.parametrize("dataset_size", [None, 400 * 2**20, 600 * 2**20])
@pytest.mark.parametrize("input_in_memory_max_size", ["default", 0, 100 * 2**20, 900 * 2**20])
def test_is_small_dataset(dataset_size, input_in_memory_max_size, monkeypatch):
    if input_in_memory_max_size != "default":
        monkeypatch.setattr(datasets.config, "IN_MEMORY_MAX_SIZE", input_in_memory_max_size)
    in_memory_max_size = datasets.config.IN_MEMORY_MAX_SIZE
    if input_in_memory_max_size == "default":
        assert in_memory_max_size == 0
    else:
        assert in_memory_max_size == input_in_memory_max_size
    if dataset_size and in_memory_max_size:
        expected = dataset_size < in_memory_max_size
    else:
        expected = False
    result = is_small_dataset(dataset_size)
    assert result == expected
