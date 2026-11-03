import pytest

from datasets import Dataset


def _dataset():
    return Dataset.from_dict({"a": [1, 2, 3], "b": [3, 1, 2]})


@pytest.mark.parametrize(
    "column_names",
    [["b", "b"], ["a", "b", "a"], ["b", "a", "b", "a"]],
)
def test_sort_duplicate_columns_raises(column_names):
    # The code promises to check for duplicates in column_names; a duplicated
    # column must be reported instead of silently sorting by it twice.
    with pytest.raises(ValueError, match="must be unique"):
        _dataset().sort(column_names)


def test_sort_unique_columns_still_work():
    assert _dataset().sort("b")["a"] == [2, 3, 1]
    assert _dataset().sort(["b", "a"])["a"] == [2, 3, 1]
