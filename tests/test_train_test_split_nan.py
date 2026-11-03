import pytest

from datasets import Dataset


def _dataset():
    return Dataset.from_dict({"a": list(range(10))})


@pytest.mark.parametrize("size_name", ["test_size", "train_size"])
def test_train_test_split_rejects_nan(size_name):
    # NaN fails every comparison, so the range check used to miss it and the
    # call only failed later with "cannot convert float NaN to integer".
    with pytest.raises(ValueError, match="should be either positive"):
        _dataset().train_test_split(**{size_name: float("nan")})


@pytest.mark.parametrize("size_name", ["test_size", "train_size"])
def test_train_test_split_still_accepts_valid_fractions(size_name):
    split = _dataset().train_test_split(**{size_name: 0.2})

    assert len(split["train"]) + len(split["test"]) == 10
    assert len(split["train"]) > 0 and len(split["test"]) > 0
