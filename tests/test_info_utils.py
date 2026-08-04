import pytest

import datasets.config
from datasets.exceptions import NonMatchingSplitsSizesError
from datasets.splits import SplitInfo
from datasets.utils.info_utils import is_small_dataset, verify_splits


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


def test_verify_splits_raises_on_mismatch_by_default():
    expected = {"train": SplitInfo(name="train", num_bytes=1000, num_examples=100)}
    recorded = {"train": SplitInfo(name="train", num_bytes=400, num_examples=40)}
    with pytest.raises(NonMatchingSplitsSizesError):
        verify_splits(expected, recorded)


def test_verify_splits_skipped_when_user_provided_data_files():
    expected = {"train": SplitInfo(name="train", num_bytes=1000, num_examples=100)}
    smaller = {"train": SplitInfo(name="train", num_bytes=400, num_examples=40)}
    larger = {"train": SplitInfo(name="train", num_bytes=2000, num_examples=200)}
    different_names = {"test": SplitInfo(name="test", num_bytes=400, num_examples=40)}
    verify_splits(expected, smaller, user_provided_data_files=True)
    verify_splits(expected, larger, user_provided_data_files=True)
    verify_splits(expected, different_names, user_provided_data_files=True)


def test_verify_splits_passes_when_sizes_match():
    expected = {"train": SplitInfo(name="train", num_bytes=1000, num_examples=100)}
    recorded = {"train": SplitInfo(name="train", num_bytes=1000, num_examples=100)}
    verify_splits(expected, recorded)
    verify_splits(expected, recorded, user_provided_data_files=True)
