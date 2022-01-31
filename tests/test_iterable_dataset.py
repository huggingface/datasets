from itertools import chain, islice

import numpy as np
import pytest

from datasets.combine import interleave_datasets
from datasets.features import ClassLabel, Features, Value
from datasets.info import DatasetInfo
from datasets.iterable_dataset import (
    BufferShuffledExamplesIterable,
    CyclingMultiSourcesExamplesIterable,
    ExamplesIterable,
    IterableDataset,
    MappedExamplesIterable,
    RandomlyCyclingMultiSourcesExamplesIterable,
    ShufflingConfig,
    SkipExamplesIterable,
    TakeExamplesIterable,
    TypedExamplesIterable,
    _batch_to_examples,
    _examples_to_batch,
    iterable_dataset,
)

from .utils import require_torch


DEFAULT_N_EXAMPLES = 20
DEFAULT_FILEPATH = "file.txt"


@pytest.fixture
def generate_examples_fn():
    def generate_examples_fn(**kwargs):
        n = kwargs.pop("n", DEFAULT_N_EXAMPLES)
        filepaths = kwargs.pop("filepaths", None)
        for filepath in filepaths or [DEFAULT_FILEPATH]:
            if filepaths is not None:
                kwargs["filepath"] = filepath
            for i in range(n):
                yield f"{filepath}_{i}", {"id": i, **kwargs}

    return generate_examples_fn


@pytest.fixture
def dataset(generate_examples_fn):
    ex_iterable = ExamplesIterable(generate_examples_fn, {})
    return IterableDataset(ex_iterable, info=DatasetInfo(description="dummy"), split="train")


################################
#
#   _BaseExampleIterable tests
#
################################


def test_examples_iterable(generate_examples_fn):
    ex_iterable = ExamplesIterable(generate_examples_fn, {})
    expected = list(generate_examples_fn())
    assert next(iter(ex_iterable)) == expected[0]
    assert list(ex_iterable) == expected


def test_examples_iterable_with_kwargs(generate_examples_fn):
    ex_iterable = ExamplesIterable(generate_examples_fn, {"filepaths": ["0.txt", "1.txt"], "split": "train"})
    expected = list(generate_examples_fn(filepaths=["0.txt", "1.txt"], split="train"))
    assert list(ex_iterable) == expected
    assert all("split" in ex for _, ex in ex_iterable)
    assert sorted({ex["filepath"] for _, ex in ex_iterable}) == ["0.txt", "1.txt"]


def test_examples_iterable_shuffle_data_sources(generate_examples_fn):
    ex_iterable = ExamplesIterable(generate_examples_fn, {"filepaths": ["0.txt", "1.txt"]})
    ex_iterable = ex_iterable.shuffle_data_sources(42)
    expected = list(generate_examples_fn(filepaths=["1.txt", "0.txt"]))  # shuffle the filepaths
    assert list(ex_iterable) == expected


@pytest.mark.parametrize("seed", [42, 1337, 101010, 123456])
def test_buffer_shuffled_examples_iterable(generate_examples_fn, seed):
    n, buffer_size = 100, 30
    rng = np.random.default_rng(seed)
    expected_indices_used_for_shuffling = list(
        islice(BufferShuffledExamplesIterable._iter_random_indices(rng, buffer_size=buffer_size), n - buffer_size)
    )
    # indices to pick in the shuffle buffer should all be in the right range
    assert all(0 <= index_to_pick < buffer_size for index_to_pick in expected_indices_used_for_shuffling)
    # it should be random indices
    assert expected_indices_used_for_shuffling != list(range(buffer_size))

    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    ex_iterable = BufferShuffledExamplesIterable(base_ex_iterable, buffer_size=buffer_size, seed=seed)

    # The final order of examples is the result of a shuffle buffer.
    all_examples = list(generate_examples_fn(n=n))
    # We create a buffer and we pick random examples from it.
    buffer, rest = all_examples[:buffer_size], all_examples[buffer_size:]
    expected = []
    for i, index_to_pick in enumerate(expected_indices_used_for_shuffling):
        expected.append(buffer[index_to_pick])
        # The picked examples are directly replaced by the next examples from the iterable.
        buffer[index_to_pick] = rest.pop(0)
    # Once we have reached the end of the iterable, we shuffle the buffer and return the remaining examples.
    rng.shuffle(buffer)
    expected += buffer

    assert next(iter(ex_iterable)) == expected[0]
    assert list(ex_iterable) == expected
    assert sorted(list(ex_iterable)) == sorted(all_examples)


def test_cycling_multi_sources_examples_iterable(generate_examples_fn):
    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"text": "foo"})
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {"text": "bar"})
    ex_iterable = CyclingMultiSourcesExamplesIterable([ex_iterable1, ex_iterable2])
    expected = list(chain(*zip(generate_examples_fn(text="foo"), generate_examples_fn(text="bar"))))

    assert next(iter(ex_iterable)) == expected[0]
    assert list(ex_iterable) == expected
    assert all((x["id"], x["text"]) == (i // 2, "bar" if i % 2 else "foo") for i, (_, x) in enumerate(ex_iterable))


@pytest.mark.parametrize("probabilities", [None, (0.5, 0.5), (0.9, 0.1)])
def test_randomly_cycling_multi_sources_examples_iterable(generate_examples_fn, probabilities):
    seed = 42
    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"text": "foo"})
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {"text": "bar"})
    ex_iterable = RandomlyCyclingMultiSourcesExamplesIterable(
        [ex_iterable1, ex_iterable2], seed=seed, probabilities=probabilities
    )

    # The source used randomly changes at each example. It stops when one of the iterators is empty.
    rng = np.random.default_rng(seed)
    iterators = (generate_examples_fn(text="foo"), generate_examples_fn(text="bar"))
    indices_iterator = RandomlyCyclingMultiSourcesExamplesIterable._iter_random_indices(
        rng, len(iterators), p=probabilities
    )
    expected = []
    for i in indices_iterator:
        for key, example in iterators[i]:
            expected.append((key, example))
            break
        else:
            break

    assert next(iter(ex_iterable)) == expected[0]
    assert list(ex_iterable) == expected


@pytest.mark.parametrize(
    "n, func, batch_size",
    [
        (3, lambda x: {"id+1": x["id"] + 1}, None),  # just add 1 to the id
        (3, lambda x: {"id+1": [x["id"][0] + 1]}, 1),  # same with bs=1
        (5, lambda x: {"id+1": [i + 1 for i in x["id"]]}, 10),  # same with bs=10
        (25, lambda x: {"id+1": [i + 1 for i in x["id"]]}, 10),  # same with bs=10
        (3, lambda x: {k: v * 2 for k, v in x.items()}, 1),  # make a duplicate of each example
        (
            50,
            lambda x: {"foo": ["bar"] * np.random.default_rng(x["id"][0]).integers(0, 10)},
            8,
        ),  # make a duplicate of each example
    ],
)
def test_mapped_examples_iterable(generate_examples_fn, n, func, batch_size):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    ex_iterable = MappedExamplesIterable(base_ex_iterable, func, batched=batch_size is not None, batch_size=batch_size)
    all_examples = list(generate_examples_fn(n=n))
    if batch_size is None:
        expected = [(key, func(x)) for key, x in all_examples]
    else:
        # For batched map we have to format the examples as a batch (i.e. in one single dictionary) to pass the batch to the function
        expected_examples_per_batch = [
            list(_batch_to_examples(func(_examples_to_batch([x for _, x in all_examples[i : i + batch_size]]))))
            for i in range(0, len(all_examples), batch_size)
        ]
        # The new key is the concatenation of the keys of each example in the batch
        expected_keys_per_batch = [
            ["_".join(key for key, _ in all_examples[i : i + batch_size])] * len(examples)
            for i, examples in zip(range(0, len(all_examples), batch_size), expected_examples_per_batch)
        ]
        # Combine keys and examples
        expected = [
            (key, example)
            for expected_keys, expected_examples in zip(expected_keys_per_batch, expected_examples_per_batch)
            for key, example in zip(expected_keys, expected_examples)
        ]
    assert next(iter(ex_iterable)) == expected[0]
    assert list(ex_iterable) == expected


def test_skip_examples_iterable(generate_examples_fn):
    total, count = 10, 2
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": total})
    skip_ex_iterable = SkipExamplesIterable(base_ex_iterable, n=count)
    expected = list(generate_examples_fn(n=total))[count:]
    assert list(skip_ex_iterable) == expected
    assert skip_ex_iterable.shuffle_data_sources(42) is skip_ex_iterable, "skip examples makes the shards order fixed"


def test_take_examples_iterable(generate_examples_fn):
    total, count = 10, 2
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": total})
    take_ex_iterable = TakeExamplesIterable(base_ex_iterable, n=count)
    expected = list(generate_examples_fn(n=total))[:count]
    assert list(take_ex_iterable) == expected
    assert take_ex_iterable.shuffle_data_sources(42) is take_ex_iterable, "skip examples makes the shards order fixed"


############################
#
#   IterableDataset tests
#
############################


def test_iterable_dataset(generate_examples_fn):
    dataset = IterableDataset(ExamplesIterable(generate_examples_fn, {}))
    expected = [x for _, x in generate_examples_fn()]
    assert next(iter(dataset)) == expected[0]
    assert list(dataset) == expected


def test_iterable_dataset_factory(generate_examples_fn):
    ex_iterable = ExamplesIterable(generate_examples_fn, {})
    dataset = iterable_dataset(ex_iterable)
    assert isinstance(dataset, IterableDataset)
    assert dataset._ex_iterable is ex_iterable


@require_torch
def test_iterable_dataset_factory_torch_integration(generate_examples_fn):
    import torch

    ex_iterable = ExamplesIterable(generate_examples_fn, {})
    dataset = iterable_dataset(ex_iterable, format_type="torch")
    assert isinstance(dataset, IterableDataset)
    assert isinstance(dataset, torch.utils.data.IterableDataset)
    assert dataset._format_type == "torch"
    assert dataset._ex_iterable is ex_iterable


def test_iterable_dataset_info(generate_examples_fn):
    info = DatasetInfo(description="desc", citation="@article{}", size_in_bytes=42)
    ex_iterable = ExamplesIterable(generate_examples_fn, {})
    dataset = IterableDataset(ex_iterable, info=info)
    assert dataset.info == info
    assert dataset.description == info.description
    assert dataset.citation == info.citation
    assert dataset.size_in_bytes == info.size_in_bytes


def test_iterable_dataset_set_epoch(dataset: IterableDataset):
    assert dataset._epoch == 0
    dataset.set_epoch(42)
    assert dataset._epoch == 42


@pytest.mark.parametrize("seed", [None, 42, 1337])
@pytest.mark.parametrize("epoch", [None, 0, 1, 10])
def test_iterable_dataset_set_epoch_of_shuffled_dataset(dataset: IterableDataset, seed, epoch):
    buffer_size = 10
    shuffled_dataset = dataset.shuffle(buffer_size, seed=seed)
    if epoch is not None:
        shuffled_dataset.set_epoch(epoch)
    if seed is None:
        assert shuffled_dataset._effective_seed is None
    else:
        assert shuffled_dataset._effective_seed == seed + (epoch if epoch is not None else 0)


def test_iterable_dataset_map(dataset: IterableDataset, generate_examples_fn):
    func = lambda x: {"id+1": x["id"] + 1}  # noqa: E731
    dataset = dataset.map(func)
    assert isinstance(dataset._ex_iterable, MappedExamplesIterable)
    assert dataset._ex_iterable.function is func
    assert dataset._ex_iterable.batched is False
    assert next(iter(dataset)) == func(next(iter(generate_examples_fn()))[1])


def test_iterable_dataset_map_batched(dataset: IterableDataset, generate_examples_fn):
    func = lambda x: {"id+1": [i + 1 for i in x["id"]]}  # noqa: E731
    _func_unbatched = lambda x: {"id+1": x["id"] + 1}  # noqa: E731
    batch_size = 3
    dataset = dataset.map(func, batched=True, batch_size=batch_size)
    assert isinstance(dataset._ex_iterable, MappedExamplesIterable)
    assert dataset._ex_iterable.function is func
    assert dataset._ex_iterable.batch_size == batch_size
    assert next(iter(dataset)) == _func_unbatched(next(iter(generate_examples_fn()))[1])


def test_iterable_dataset_map_complex_features(dataset: IterableDataset, generate_examples_fn):
    # https://github.com/huggingface/datasets/issues/3505
    ex_iterable = ExamplesIterable(generate_examples_fn, {"label": "positive"})
    features = Features(
        {
            "id": Value("int64"),
            "label": Value("string"),
        }
    )
    dataset = IterableDataset(ex_iterable, info=DatasetInfo(features=features))
    dataset = dataset.cast_column("label", ClassLabel(names=["negative", "positive"]))
    dataset = dataset.map(lambda x: {"id+1": x["id"] + 1, **x})
    assert isinstance(dataset._ex_iterable, MappedExamplesIterable)
    features["label"] = ClassLabel(names=["negative", "positive"])
    assert [{k: v for k, v in ex.items() if k != "id+1"} for ex in dataset] == [
        features.encode_example(ex) for _, ex in ex_iterable
    ]


@pytest.mark.parametrize("seed", [42, 1337, 101010, 123456])
@pytest.mark.parametrize("epoch", [None, 0, 1])
def test_iterable_dataset_shuffle(dataset: IterableDataset, generate_examples_fn, seed, epoch):
    buffer_size = 3
    dataset._ex_iterable.kwargs["filepaths"] = ["0.txt", "1.txt"]
    dataset = dataset.shuffle(buffer_size, seed=seed)
    assert isinstance(dataset._shuffling, ShufflingConfig)
    assert dataset._shuffling.seed == seed
    # Effective seed is sum of seed and epoch
    if epoch is None:
        effective_seed = seed
    else:
        dataset.set_epoch(epoch)
        effective_seed = seed + epoch
    # Shuffling adds a shuffle buffer
    expected_first_example_index = next(
        iter(BufferShuffledExamplesIterable._iter_random_indices(np.random.default_rng(effective_seed), buffer_size))
    )
    assert isinstance(dataset._ex_iterable, BufferShuffledExamplesIterable)
    # It also shuffles the underlying examples iterable
    expected_ex_iterable = ExamplesIterable(
        generate_examples_fn, {"filepaths": ["0.txt", "1.txt"]}
    ).shuffle_data_sources(effective_seed)
    assert isinstance(dataset._ex_iterable.ex_iterable, ExamplesIterable)
    assert next(iter(dataset)) == list(islice(expected_ex_iterable, expected_first_example_index + 1))[-1][1]


@pytest.mark.parametrize(
    "features",
    [
        None,
        Features(
            {
                "id": Value("int64"),
                "label": Value("int64"),
            }
        ),
        Features(
            {
                "id": Value("int64"),
                "label": ClassLabel(names=["negative", "positive"]),
            }
        ),
    ],
)
def test_iterable_dataset_features(generate_examples_fn, features):
    ex_iterable = ExamplesIterable(generate_examples_fn, {"label": 0})
    dataset = IterableDataset(ex_iterable, info=DatasetInfo(features=features))
    if features:
        expected = [features.encode_example(x) for _, x in ex_iterable]
    else:
        expected = [x for _, x in ex_iterable]
    assert list(dataset) == expected


@require_torch
@pytest.mark.parametrize("format_type", [None, "torch", "python"])
def test_iterable_dataset_with_format(dataset: IterableDataset, format_type):
    formatted_dataset = dataset.with_format(format_type)
    assert formatted_dataset._format_type == format_type
    if format_type == "torch":
        import torch

        assert isinstance(formatted_dataset, torch.utils.data.IterableDataset)


@pytest.mark.parametrize("n", [0, 2, int(1e10)])
def test_iterable_dataset_skip(dataset: IterableDataset, n):
    skip_dataset = dataset.skip(n)
    assert isinstance(skip_dataset._ex_iterable, SkipExamplesIterable)
    assert skip_dataset._ex_iterable.n == n
    assert list(skip_dataset) == list(dataset)[n:]


@pytest.mark.parametrize("n", [0, 2, int(1e10)])
def test_iterable_dataset_take(dataset: IterableDataset, n):
    take_dataset = dataset.take(n)
    assert isinstance(take_dataset._ex_iterable, TakeExamplesIterable)
    assert take_dataset._ex_iterable.n == n
    assert list(take_dataset) == list(dataset)[:n]


@pytest.mark.parametrize("method", ["skip", "take"])
def test_iterable_dataset_shuffle_after_skip_or_take(generate_examples_fn, method):
    seed = 42
    n, n_shards = 3, 10
    count = 7
    ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n, "filepaths": [f"{i}.txt" for i in range(n_shards)]})
    dataset = IterableDataset(ex_iterable)
    dataset = dataset.skip(n) if method == "skip" else dataset.take(count)
    shuffled_dataset = dataset.shuffle(DEFAULT_N_EXAMPLES, seed=seed)
    # shuffling a skip/take dataset should keep the same examples and don't shuffle the shards
    key = lambda x: f"{x['filepath']}_{x['id']}"  # noqa: E731
    assert sorted(dataset, key=key) == sorted(shuffled_dataset, key=key)


def test_iterable_dataset_cast_column(generate_examples_fn):
    ex_iterable = ExamplesIterable(generate_examples_fn, {"label": 10})
    features = Features({"id": Value("int64"), "label": Value("int64")})
    dataset = IterableDataset(ex_iterable, info=DatasetInfo(features=features))
    casted_dataset = dataset.cast_column("label", Value("bool"))
    casted_features = features.copy()
    casted_features["label"] = Value("bool")
    assert list(casted_dataset) == [casted_features.encode_example(ex) for _, ex in ex_iterable]


@pytest.mark.parametrize(
    "probas, seed, expected_length",
    [
        (None, None, 3 * DEFAULT_N_EXAMPLES),
        ([1, 0, 0], None, DEFAULT_N_EXAMPLES),
        ([0, 1, 0], None, DEFAULT_N_EXAMPLES),
        ([0.2, 0.5, 0.3], 42, None),
        ([0.1, 0.1, 0.8], 1337, None),
        ([0.5, 0.2, 0.3], 101010, None),
    ],
)
def test_interleave_datasets(dataset: IterableDataset, probas, seed, expected_length):
    d1 = dataset
    d2 = dataset.map(lambda x: {"id+1": x["id"] + 1, **x})
    d3 = dataset.with_format("python")
    datasets = [d1, d2, d3]
    merged_dataset = interleave_datasets(datasets, probabilities=probas, seed=seed)
    # Check the examples iterable
    assert isinstance(
        merged_dataset._ex_iterable, (CyclingMultiSourcesExamplesIterable, RandomlyCyclingMultiSourcesExamplesIterable)
    )
    # Check that it is deterministic
    if seed is not None:
        merged_dataset2 = interleave_datasets([d1, d2, d3], probabilities=probas, seed=seed)
        assert list(merged_dataset) == list(merged_dataset2)
    # Check first example
    if seed is not None:
        rng = np.random.default_rng(seed)
        i = next(iter(RandomlyCyclingMultiSourcesExamplesIterable._iter_random_indices(rng, len(datasets), p=probas)))
        assert next(iter(merged_dataset)) == next(iter(datasets[i]))
    else:
        assert any(next(iter(merged_dataset)) == next(iter(dataset)) for dataset in datasets)
    # Compute length it case it's random
    if expected_length is None:
        expected_length = 0
        counts = [len(list(d)) for d in datasets]
        rng = np.random.default_rng(seed)
        for i in RandomlyCyclingMultiSourcesExamplesIterable._iter_random_indices(rng, len(datasets), p=probas):
            if counts[i] == 0:
                break
            counts[i] -= 1
            expected_length += 1
    # Check length
    assert len(list(merged_dataset)) == expected_length


def test_interleave_datasets_with_features(dataset: IterableDataset, generate_examples_fn):
    features = Features(
        {
            "id": Value("int64"),
            "label": ClassLabel(names=["negative", "positive"]),
        }
    )
    ex_iterable = ExamplesIterable(generate_examples_fn, {"label": 0})
    dataset_with_features = IterableDataset(ex_iterable, info=DatasetInfo(features=features))

    merged_dataset = interleave_datasets([dataset, dataset_with_features], probabilities=[0, 1])
    assert isinstance(merged_dataset._ex_iterable, CyclingMultiSourcesExamplesIterable)
    assert isinstance(merged_dataset._ex_iterable.ex_iterables[1], TypedExamplesIterable)
    assert merged_dataset._ex_iterable.ex_iterables[1].features == features
    assert next(iter(merged_dataset)) == next(iter(dataset_with_features))
