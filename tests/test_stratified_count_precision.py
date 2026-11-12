from fractions import Fraction

import numpy as np
import pytest

from datasets import ClassLabel, Dataset, Features, Value
from datasets.utils.stratify import approximate_mode, stratified_shuffle_split_generate_indices


def _exact_allocation(counts, draws, rng):
    """Largest-remainder allocation without fixed-width integer arithmetic."""
    total = sum(int(count) for count in counts)
    proportions = [Fraction(int(count) * draws, total) for count in counts]
    allocation = [value.numerator // value.denominator for value in proportions]
    remainders = [value - whole for value, whole in zip(proportions, allocation)]
    remaining = draws - sum(allocation)
    for remainder in sorted(set(remainders), reverse=True):
        if remaining == 0:
            break
        tied = [index for index, value in enumerate(remainders) if value == remainder]
        selected = rng.choice(tied, size=min(len(tied), remaining), replace=False)
        for index in selected:
            allocation[index] += 1
        remaining -= len(selected)
    return np.array(allocation, dtype=np.int64)


@pytest.mark.parametrize("dtype", [np.int64, np.uint64])
@pytest.mark.parametrize(
    "counts,draws",
    [
        ([4_000_000_000, 6_000_000_000], 8_000_000_000),
        ([3_000_000_001, 4_000_000_003, 5_000_000_007], 9_000_000_005),
        ([0, 5_000_000_000, 5_000_000_000], 10_000_000_000),
    ],
)
def test_approximate_mode_large_integer_counts(counts, draws, dtype):
    counts = np.array(counts, dtype=dtype)
    original = counts.copy()
    rng = np.random.default_rng(12)
    reference_rng = np.random.default_rng(12)

    actual = approximate_mode(counts, draws, rng)
    expected = _exact_allocation(counts, draws, reference_rng)

    np.testing.assert_array_equal(actual, expected)
    assert actual.dtype == np.int64
    assert actual.sum() == draws
    assert np.all(actual >= 0)
    assert np.all(actual <= counts)
    np.testing.assert_array_equal(counts, original)


@pytest.mark.parametrize("draws", [0, 1, 7, 12])
@pytest.mark.parametrize("rng_factory", [np.random.default_rng, np.random.RandomState])
def test_approximate_mode_small_counts_and_tie_breaking(draws, rng_factory):
    counts = np.array([4, 4, 4])
    rng = rng_factory(12)
    reference_rng = rng_factory(12)

    np.testing.assert_array_equal(
        approximate_mode(counts, draws, rng), _exact_allocation(counts, draws, reference_rng)
    )
    # A change in arithmetic must not add random draws to the tie-breaking path.
    np.testing.assert_array_equal(rng.random(5), reference_rng.random(5))


def test_stratified_indices_match_sklearn():
    sklearn = pytest.importorskip("sklearn.model_selection")
    labels = np.repeat(np.arange(3), [12, 18, 30])
    expected = sklearn.StratifiedShuffleSplit(n_splits=3, train_size=48, test_size=12, random_state=17)
    actual = stratified_shuffle_split_generate_indices(labels, 48, 12, np.random.RandomState(17), n_splits=3)

    for (train, test), (reference_train, reference_test) in zip(actual, expected.split(labels, labels)):
        np.testing.assert_array_equal(train, reference_train)
        np.testing.assert_array_equal(test, reference_test)


@pytest.mark.parametrize("train_size,expected_train", [(30, [6, 9, 15]), (48, [10, 14, 24])])
def test_dataset_stratified_split_keeps_expected_class_counts(train_size, expected_train):
    labels = np.repeat(np.arange(3), [12, 18, 30])
    dataset = Dataset.from_dict(
        {"id": np.arange(len(labels)), "label": labels},
        features=Features({"id": Value("int64"), "label": ClassLabel(names=["a", "b", "c"])}),
    )

    split = dataset.train_test_split(train_size=train_size, stratify_by_column="label", seed=17)

    np.testing.assert_array_equal(np.bincount(split["train"]["label"]), expected_train)
    np.testing.assert_array_equal(np.bincount(split["test"]["label"]), np.array([12, 18, 30]) - expected_train)
    train_ids, test_ids = set(split["train"]["id"]), set(split["test"]["id"])
    assert not train_ids & test_ids
    assert train_ids | test_ids == set(range(len(dataset)))
