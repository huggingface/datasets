import pytest

from datasets import Dataset


def _streaming_dataset():
    return Dataset.from_dict({"a": [1, 2, 3]}).to_iterable_dataset()


@pytest.mark.parametrize("bad_return", [[1, 2, 3], "text", 42])
def test_iterable_dataset_map_invalid_return_type_raises(bad_return):
    ds = _streaming_dataset()

    with pytest.raises(TypeError, match="returns a variable of type"):
        list(ds.map(lambda example: bad_return))


def test_iterable_dataset_map_invalid_return_type_batched_raises():
    ds = _streaming_dataset()

    with pytest.raises(TypeError, match="returns a `dict` of types"):
        list(ds.map(lambda batch: {"b": batch["a"][0]}, batched=True))


def test_iterable_dataset_map_valid_return_types_still_work():
    ds = _streaming_dataset()

    assert list(ds.map(lambda example: {"b": example["a"] * 2})) == [{"a": 1, "b": 2}, {"a": 2, "b": 4}, {"a": 3, "b": 6}]
    assert list(ds.map(lambda batch: {"b": [a * 2 for a in batch["a"]]}, batched=True)) == [
        {"a": 1, "b": 2},
        {"a": 2, "b": 4},
        {"a": 3, "b": 6},
    ]
