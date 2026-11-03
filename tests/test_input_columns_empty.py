import pytest

from datasets import Dataset


def test_filter_with_empty_input_columns_is_named():
    dataset = Dataset.from_dict({"a": [1, 2, 3]})

    with pytest.raises(ValueError, match="input_columns cannot be an empty list"):
        dataset.filter(lambda example: True, input_columns=[])


def test_map_with_empty_input_columns_is_named():
    dataset = Dataset.from_dict({"a": [1, 2, 3]})

    with pytest.raises(ValueError, match="input_columns cannot be an empty list"):
        dataset.map(lambda example: example, input_columns=[])


def test_a_single_input_column_still_works():
    dataset = Dataset.from_dict({"a": [1, 2, 3]})

    filtered = dataset.filter(lambda a: a > 1, input_columns=["a"])

    assert filtered["a"] == [2, 3]
