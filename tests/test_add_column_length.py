import pytest

from datasets import Dataset


def _dataset():
    return Dataset.from_dict({"a": [1, 2, 3]})


@pytest.mark.parametrize("column", [[10, 20], [10, 20, 30, 40], []])
def test_add_column_length_mismatch_raises(column):
    """A column of the wrong length must be reported clearly, not as a failed concat."""
    with pytest.raises(ValueError, match="has length .* but the dataset has 3 rows"):
        _dataset().add_column("b", column)


def test_add_column_matching_length_still_works():
    dataset = _dataset().add_column("b", [10, 20, 30])

    assert dataset["b"] == [10, 20, 30]
