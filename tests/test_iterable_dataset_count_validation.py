import pytest

from datasets import IterableDataset


@pytest.mark.parametrize("method", ["take", "skip"])
@pytest.mark.parametrize("n", ["2", 1.5, None])
def test_a_count_that_is_not_an_integer_is_named(method, n):
    dataset = IterableDataset.from_list([{"a": i} for i in range(3)])

    with pytest.raises(ValueError, match="n must be an integer"):
        getattr(dataset, method)(n)


def test_an_integer_count_still_works():
    dataset = IterableDataset.from_list([{"a": i} for i in range(3)])

    assert list(dataset.take(2)) == [{"a": 0}, {"a": 1}]
    assert list(dataset.skip(2)) == [{"a": 2}]
