from copy import deepcopy
from itertools import chain, islice

import numpy as np
import pandas as pd
import pytest

from datasets import load_dataset
from datasets.combine import concatenate_datasets, interleave_datasets
from datasets.features import ClassLabel, Features, Value
from datasets.info import DatasetInfo
from datasets.iterable_dataset import (
    BufferShuffledExamplesIterable,
    CyclingMultiSourcesExamplesIterable,
    ExamplesIterable,
    FilteredExamplesIterable,
    HorizontallyConcatenatedMultiSourcesExamplesIterable,
    IterableDataset,
    MappedExamplesIterable,
    RandomlyCyclingMultiSourcesExamplesIterable,
    ShufflingConfig,
    SkipExamplesIterable,
    TakeExamplesIterable,
    TypedExamplesIterable,
    VerticallyConcatenatedMultiSourcesExamplesIterable,
    _batch_to_examples,
    _examples_to_batch,
    iterable_dataset,
)

from .utils import is_rng_equal, require_torch


DEFAULT_N_EXAMPLES = 20
DEFAULT_FILEPATH = "file.txt"

SAMPLE_DATASET_IDENTIFIER = "lhoestq/test"  # has dataset script


def generate_examples_fn(**kwargs):
    kwargs = kwargs.copy()
    n = kwargs.pop("n", DEFAULT_N_EXAMPLES)
    filepaths = kwargs.pop("filepaths", None)
    for filepath in filepaths or [DEFAULT_FILEPATH]:
        if filepaths is not None:
            kwargs["filepath"] = filepath
        for i in range(n):
            yield f"{filepath}_{i}", {"id": i, **kwargs}


@pytest.fixture
def dataset():
    ex_iterable = ExamplesIterable(generate_examples_fn, {})
    return IterableDataset(ex_iterable, info=DatasetInfo(description="dummy"), split="train")


@pytest.fixture
def dataset_with_several_columns():
    ex_iterable = ExamplesIterable(
        generate_examples_fn,
        {"filepath": ["data0.txt", "data1.txt", "data2.txt"], "metadata": {"sources": ["https://foo.bar"]}},
    )
    return IterableDataset(ex_iterable, info=DatasetInfo(description="dummy"), split="train")


################################
#
#   _BaseExampleIterable tests
#
################################


def test_examples_iterable():
    ex_iterable = ExamplesIterable(generate_examples_fn, {})
    expected = list(generate_examples_fn())
    assert next(iter(ex_iterable)) == expected[0]
    assert list(ex_iterable) == expected


def test_examples_iterable_with_kwargs():
    ex_iterable = ExamplesIterable(generate_examples_fn, {"filepaths": ["0.txt", "1.txt"], "split": "train"})
    expected = list(generate_examples_fn(filepaths=["0.txt", "1.txt"], split="train"))
    assert list(ex_iterable) == expected
    assert all("split" in ex for _, ex in ex_iterable)
    assert sorted({ex["filepath"] for _, ex in ex_iterable}) == ["0.txt", "1.txt"]


def test_examples_iterable_shuffle_data_sources():
    ex_iterable = ExamplesIterable(generate_examples_fn, {"filepaths": ["0.txt", "1.txt"]})
    ex_iterable = ex_iterable.shuffle_data_sources(np.random.default_rng(40))
    expected = list(generate_examples_fn(filepaths=["1.txt", "0.txt"]))  # shuffle the filepaths
    assert list(ex_iterable) == expected


def test_examples_iterable_shuffle_shards_and_metadata():
    def gen(filepaths, all_metadata):
        for i, (filepath, metadata) in enumerate(zip(filepaths, all_metadata)):
            yield i, {"filepath": filepath, "metadata": metadata}

    ex_iterable = ExamplesIterable(
        gen,
        {
            "filepaths": [f"{i}.txt" for i in range(100)],
            "all_metadata": [{"id": str(i)} for i in range(100)],
        },
    )
    ex_iterable = ex_iterable.shuffle_data_sources(np.random.default_rng(42))
    out = list(ex_iterable)
    filepaths_ids = [x["filepath"].split(".")[0] for _, x in out]
    metadata_ids = [x["metadata"]["id"] for _, x in out]
    assert filepaths_ids == metadata_ids, "entangled lists of shards/metadata should be shuffled the same way"


@pytest.mark.parametrize("seed", [42, 1337, 101010, 123456])
def test_buffer_shuffled_examples_iterable(seed):
    n, buffer_size = 100, 30
    generator = np.random.default_rng(seed)
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    ex_iterable = BufferShuffledExamplesIterable(base_ex_iterable, buffer_size=buffer_size, generator=generator)

    rng = deepcopy(generator)
    expected_indices_used_for_shuffling = list(
        islice(BufferShuffledExamplesIterable._iter_random_indices(rng, buffer_size=buffer_size), n - buffer_size)
    )
    # indices to pick in the shuffle buffer should all be in the right range
    assert all(0 <= index_to_pick < buffer_size for index_to_pick in expected_indices_used_for_shuffling)
    # it should be random indices
    assert expected_indices_used_for_shuffling != list(range(buffer_size))

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


def test_cycling_multi_sources_examples_iterable():
    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"text": "foo"})
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {"text": "bar"})
    ex_iterable = CyclingMultiSourcesExamplesIterable([ex_iterable1, ex_iterable2])
    expected = list(chain(*zip(generate_examples_fn(text="foo"), generate_examples_fn(text="bar"))))

    assert next(iter(ex_iterable)) == expected[0]
    assert list(ex_iterable) == expected
    assert all((x["id"], x["text"]) == (i // 2, "bar" if i % 2 else "foo") for i, (_, x) in enumerate(ex_iterable))


@pytest.mark.parametrize("probabilities", [None, (0.5, 0.5), (0.9, 0.1)])
def test_randomly_cycling_multi_sources_examples_iterable(probabilities):
    seed = 42
    generator = np.random.default_rng(seed)
    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"text": "foo"})
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {"text": "bar"})
    ex_iterable = RandomlyCyclingMultiSourcesExamplesIterable(
        [ex_iterable1, ex_iterable2], generator=generator, probabilities=probabilities
    )

    # The source used randomly changes at each example. It stops when one of the iterators is empty.
    rng = deepcopy(generator)
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
    ],
)
def test_mapped_examples_iterable(n, func, batch_size):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    ex_iterable = MappedExamplesIterable(base_ex_iterable, func, batched=batch_size is not None, batch_size=batch_size)
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    if batch_size is None:
        expected = [{**x, **func(x)} for x in all_examples]
    else:
        # For batched map we have to format the examples as a batch (i.e. in one single dictionary) to pass the batch to the function
        all_transformed_examples = []
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            batch = _examples_to_batch(examples)
            transformed_batch = func(batch)
            all_transformed_examples.extend(_batch_to_examples(transformed_batch))
        expected = _examples_to_batch(all_examples)
        expected.update(_examples_to_batch(all_transformed_examples))
        expected = list(_batch_to_examples(expected))
    assert next(iter(ex_iterable))[1] == expected[0]
    assert list(x for _, x in ex_iterable) == expected


@pytest.mark.parametrize(
    "n, func, batch_size",
    [
        (3, lambda x: {"id+1": x["id"] + 1}, None),  # just add 1 to the id
        (3, lambda x: {"id+1": [x["id"][0] + 1]}, 1),  # same with bs=1
        (5, lambda x: {"id+1": [i + 1 for i in x["id"]]}, 10),  # same with bs=10
        (25, lambda x: {"id+1": [i + 1 for i in x["id"]]}, 10),  # same with bs=10
        (3, lambda x: {k: v * 2 for k, v in x.items()}, 1),  # make a duplicate of each example
    ],
)
def test_mapped_examples_iterable_drop_last_batch(n, func, batch_size):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    ex_iterable = MappedExamplesIterable(
        base_ex_iterable, func, batched=batch_size is not None, batch_size=batch_size, drop_last_batch=True
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    is_empty = False
    if batch_size is None:
        # `drop_last_batch` has no effect here
        expected = [{**x, **func(x)} for x in all_examples]
    else:
        # For batched map we have to format the examples as a batch (i.e. in one single dictionary) to pass the batch to the function
        all_transformed_examples = []
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            if len(examples) < batch_size:  # ignore last batch
                break
            batch = _examples_to_batch(examples)
            transformed_batch = func(batch)
            all_transformed_examples.extend(_batch_to_examples(transformed_batch))
        all_examples = all_examples if n % batch_size == 0 else all_examples[: n // batch_size * batch_size]
        if all_examples:
            expected = _examples_to_batch(all_examples)
            expected.update(_examples_to_batch(all_transformed_examples))
            expected = list(_batch_to_examples(expected))
        else:
            is_empty = True

    if not is_empty:
        assert next(iter(ex_iterable))[1] == expected[0]
        assert list(x for _, x in ex_iterable) == expected
    else:
        with pytest.raises(StopIteration):
            next(iter(ex_iterable))


@pytest.mark.parametrize(
    "n, func, batch_size",
    [
        (3, lambda x, index: {"id+idx": x["id"] + index}, None),  # add the index to the id
        (25, lambda x, indices: {"id+idx": [i + j for i, j in zip(x["id"], indices)]}, 10),  # add the index to the id
    ],
)
def test_mapped_examples_iterable_with_indices(n, func, batch_size):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    ex_iterable = MappedExamplesIterable(
        base_ex_iterable, func, batched=batch_size is not None, batch_size=batch_size, with_indices=True
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    if batch_size is None:
        expected = [{**x, **func(x, idx)} for idx, x in enumerate(all_examples)]
    else:
        # For batched map we have to format the examples as a batch (i.e. in one single dictionary) to pass the batch to the function
        all_transformed_examples = []
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            batch = _examples_to_batch(examples)
            indices = list(range(batch_offset, batch_offset + len(examples)))
            transformed_batch = func(batch, indices)
            all_transformed_examples.extend(_batch_to_examples(transformed_batch))
        expected = _examples_to_batch(all_examples)
        expected.update(_examples_to_batch(all_transformed_examples))
        expected = list(_batch_to_examples(expected))
    assert next(iter(ex_iterable))[1] == expected[0]
    assert list(x for _, x in ex_iterable) == expected


@pytest.mark.parametrize(
    "n, func, batch_size, remove_columns",
    [
        (3, lambda x: {"id+1": x["id"] + 1}, None, ["extra_column"]),  # just add 1 to the id
        (25, lambda x: {"id+1": [i + 1 for i in x["id"]]}, 10, ["extra_column"]),  # same with bs=10
        (
            50,
            lambda x: {"foo": ["bar"] * np.random.default_rng(x["id"][0]).integers(0, 10)},
            8,
            ["extra_column", "id"],
        ),  # make a duplicate of each example
    ],
)
def test_mapped_examples_iterable_remove_columns(n, func, batch_size, remove_columns):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n, "extra_column": "foo"})
    ex_iterable = MappedExamplesIterable(
        base_ex_iterable, func, batched=batch_size is not None, batch_size=batch_size, remove_columns=remove_columns
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    columns_to_remove = remove_columns if isinstance(remove_columns, list) else [remove_columns]
    if batch_size is None:
        expected = [{**{k: v for k, v in x.items() if k not in columns_to_remove}, **func(x)} for x in all_examples]
    else:
        # For batched map we have to format the examples as a batch (i.e. in one single dictionary) to pass the batch to the function
        all_transformed_examples = []
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            batch = _examples_to_batch(examples)
            transformed_batch = func(batch)
            all_transformed_examples.extend(_batch_to_examples(transformed_batch))
        expected = {k: v for k, v in _examples_to_batch(all_examples).items() if k not in columns_to_remove}
        expected.update(_examples_to_batch(all_transformed_examples))
        expected = list(_batch_to_examples(expected))
    assert next(iter(ex_iterable))[1] == expected[0]
    assert list(x for _, x in ex_iterable) == expected


@pytest.mark.parametrize(
    "n, func, batch_size, input_columns",
    [
        (3, lambda id_: {"id+1": id_ + 1}, None, ["id"]),  # just add 1 to the id
        (25, lambda ids_: {"id+1": [i + 1 for i in ids_]}, 10, ["id"]),  # same with bs=10
    ],
)
def test_mapped_examples_iterable_input_columns(n, func, batch_size, input_columns):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    ex_iterable = MappedExamplesIterable(
        base_ex_iterable, func, batched=batch_size is not None, batch_size=batch_size, input_columns=input_columns
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    columns_to_input = input_columns if isinstance(input_columns, list) else [input_columns]
    if batch_size is None:
        expected = [{**x, **func(*[x[col] for col in columns_to_input])} for x in all_examples]
    else:
        # For batched map we have to format the examples as a batch (i.e. in one single dictionary) to pass the batch to the function
        all_transformed_examples = []
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            batch = _examples_to_batch(examples)
            transformed_batch = func(*[batch[col] for col in columns_to_input])
            all_transformed_examples.extend(_batch_to_examples(transformed_batch))
        expected = _examples_to_batch(all_examples)
        expected.update(_examples_to_batch(all_transformed_examples))
        expected = list(_batch_to_examples(expected))
    assert next(iter(ex_iterable))[1] == expected[0]
    assert list(x for _, x in ex_iterable) == expected


@pytest.mark.parametrize(
    "n, func, batch_size",
    [
        (3, lambda x: x["id"] % 2 == 0, None),  # keep even number
        (3, lambda x: [x["id"][0] % 2 == 0], 1),  # same with bs=1
        (5, lambda x: [i % 2 == 0 for i in x["id"]], 10),  # same with bs=10
        (25, lambda x: [i % 2 == 0 for i in x["id"]], 10),  # same with bs=10
        (3, lambda x: False, None),  # return 0 examples
        (3, lambda x: [False] * len(x["id"]), 10),  # same with bs=10
    ],
)
def test_filtered_examples_iterable(n, func, batch_size):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    ex_iterable = FilteredExamplesIterable(
        base_ex_iterable, func, batched=batch_size is not None, batch_size=batch_size
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    if batch_size is None:
        expected = [x for x in all_examples if func(x)]
    else:
        # For batched filter we have to format the examples as a batch (i.e. in one single dictionary) to pass the batch to the function
        expected = []
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            batch = _examples_to_batch(examples)
            mask = func(batch)
            expected.extend([x for x, to_keep in zip(examples, mask) if to_keep])
    if expected:
        assert next(iter(ex_iterable))[1] == expected[0]
    assert list(x for _, x in ex_iterable) == expected


@pytest.mark.parametrize(
    "n, func, batch_size",
    [
        (3, lambda x, index: index % 2 == 0, None),  # keep even number
        (25, lambda x, indices: [idx % 2 == 0 for idx in indices], 10),  # same with bs=10
    ],
)
def test_filtered_examples_iterable_with_indices(n, func, batch_size):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    ex_iterable = FilteredExamplesIterable(
        base_ex_iterable, func, batched=batch_size is not None, batch_size=batch_size, with_indices=True
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    if batch_size is None:
        expected = [x for idx, x in enumerate(all_examples) if func(x, idx)]
    else:
        # For batched filter we have to format the examples as a batch (i.e. in one single dictionary) to pass the batch to the function
        expected = []
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            batch = _examples_to_batch(examples)
            indices = list(range(batch_offset, batch_offset + len(examples)))
            mask = func(batch, indices)
            expected.extend([x for x, to_keep in zip(examples, mask) if to_keep])
    assert next(iter(ex_iterable))[1] == expected[0]
    assert list(x for _, x in ex_iterable) == expected


@pytest.mark.parametrize(
    "n, func, batch_size, input_columns",
    [
        (3, lambda id_: id_ % 2 == 0, None, ["id"]),  # keep even number
        (25, lambda ids_: [i % 2 == 0 for i in ids_], 10, ["id"]),  # same with bs=10
    ],
)
def test_filtered_examples_iterable_input_columns(n, func, batch_size, input_columns):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    ex_iterable = FilteredExamplesIterable(
        base_ex_iterable, func, batched=batch_size is not None, batch_size=batch_size, input_columns=input_columns
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    columns_to_input = input_columns if isinstance(input_columns, list) else [input_columns]
    if batch_size is None:
        expected = [x for x in all_examples if func(*[x[col] for col in columns_to_input])]
    else:
        # For batched filter we have to format the examples as a batch (i.e. in one single dictionary) to pass the batch to the function
        expected = []
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            batch = _examples_to_batch(examples)
            mask = func(*[batch[col] for col in columns_to_input])
            expected.extend([x for x, to_keep in zip(examples, mask) if to_keep])
    assert next(iter(ex_iterable))[1] == expected[0]
    assert list(x for _, x in ex_iterable) == expected


def test_skip_examples_iterable():
    total, count = 10, 2
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": total})
    skip_ex_iterable = SkipExamplesIterable(base_ex_iterable, n=count)
    expected = list(generate_examples_fn(n=total))[count:]
    assert list(skip_ex_iterable) == expected
    assert (
        skip_ex_iterable.shuffle_data_sources(np.random.default_rng(42)) is skip_ex_iterable
    ), "skip examples makes the shards order fixed"


def test_take_examples_iterable():
    total, count = 10, 2
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": total})
    take_ex_iterable = TakeExamplesIterable(base_ex_iterable, n=count)
    expected = list(generate_examples_fn(n=total))[:count]
    assert list(take_ex_iterable) == expected
    assert (
        take_ex_iterable.shuffle_data_sources(np.random.default_rng(42)) is take_ex_iterable
    ), "skip examples makes the shards order fixed"


def test_vertically_concatenated_examples_iterable():
    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"label": 10})
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {"label": 5})
    concatenated_ex_iterable = VerticallyConcatenatedMultiSourcesExamplesIterable([ex_iterable1, ex_iterable2])
    expected = list(x for _, x in ex_iterable1) + list(x for _, x in ex_iterable2)
    assert list(x for _, x in concatenated_ex_iterable) == expected


def test_vertically_concatenated_examples_iterable_with_different_columns():
    # having different columns is supported
    # Though iterable datasets fill the missing data with nulls
    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"label": 10})
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {})
    concatenated_ex_iterable = VerticallyConcatenatedMultiSourcesExamplesIterable([ex_iterable1, ex_iterable2])
    expected = list(x for _, x in ex_iterable1) + list(x for _, x in ex_iterable2)
    assert list(x for _, x in concatenated_ex_iterable) == expected


def test_vertically_concatenated_examples_iterable_shuffle_data_sources():
    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"label": 10})
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {"label": 5})
    concatenated_ex_iterable = VerticallyConcatenatedMultiSourcesExamplesIterable([ex_iterable1, ex_iterable2])
    rng = np.random.default_rng(42)
    shuffled_ex_iterable = concatenated_ex_iterable.shuffle_data_sources(rng)
    # make sure the list of examples iterables is shuffled, and each examples iterable is shuffled
    expected = list(x for _, x in ex_iterable2.shuffle_data_sources(rng)) + list(
        x for _, x in ex_iterable1.shuffle_data_sources(rng)
    )
    assert list(x for _, x in shuffled_ex_iterable) == expected


def test_horizontally_concatenated_examples_iterable():
    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"label1": 10})
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {"label2": 5})
    concatenated_ex_iterable = HorizontallyConcatenatedMultiSourcesExamplesIterable([ex_iterable1, ex_iterable2])
    with pytest.raises(ValueError):  # column "id" is duplicated -> raise an error
        list(concatenated_ex_iterable)
    ex_iterable2 = MappedExamplesIterable(ex_iterable2, lambda x: x, remove_columns=["id"])
    concatenated_ex_iterable = HorizontallyConcatenatedMultiSourcesExamplesIterable([ex_iterable1, ex_iterable2])
    expected = list({**x, **y} for (_, x), (_, y) in zip(ex_iterable1, ex_iterable2))
    assert list(x for _, x in concatenated_ex_iterable) == expected
    assert (
        concatenated_ex_iterable.shuffle_data_sources(np.random.default_rng(42)) is concatenated_ex_iterable
    ), "horizontally concatenated examples makes the shards order fixed"


############################
#
#   IterableDataset tests
#
############################


def test_iterable_dataset():
    dataset = IterableDataset(ExamplesIterable(generate_examples_fn, {}))
    expected = [x for _, x in generate_examples_fn()]
    assert next(iter(dataset)) == expected[0]
    assert list(dataset) == expected


def test_iterable_dataset_factory():
    ex_iterable = ExamplesIterable(generate_examples_fn, {})
    dataset = iterable_dataset(ex_iterable)
    assert isinstance(dataset, IterableDataset)
    assert dataset._ex_iterable is ex_iterable


@require_torch
def test_iterable_dataset_factory_torch_integration():
    import torch

    ex_iterable = ExamplesIterable(generate_examples_fn, {})
    dataset = iterable_dataset(ex_iterable, format_type="torch")
    assert isinstance(dataset, IterableDataset)
    assert isinstance(dataset, torch.utils.data.IterableDataset)
    assert dataset._format_type == "torch"
    assert dataset._ex_iterable is ex_iterable


@require_torch
def test_iterable_dataset_factory_torch_picklable():
    import pickle

    ex_iterable = ExamplesIterable(generate_examples_fn, {})
    dataset = iterable_dataset(ex_iterable, format_type="torch")
    reloaded_dataset = pickle.loads(pickle.dumps(dataset))

    import torch

    assert isinstance(reloaded_dataset, IterableDataset)
    assert isinstance(reloaded_dataset, torch.utils.data.IterableDataset)
    assert reloaded_dataset._format_type == "torch"
    assert len(list(dataset)) == len(list(reloaded_dataset))


@require_torch
def test_iterable_dataset_with_format_torch():
    from torch.utils.data import DataLoader

    ex_iterable = ExamplesIterable(generate_examples_fn, {})
    dataset = iterable_dataset(ex_iterable).with_format("torch")
    dataloader = DataLoader(dataset)
    assert len(list(dataloader)) == len(list(ex_iterable))


@require_torch
def test_iterable_dataset_torch_dataloader_parallel():
    from torch.utils.data import DataLoader

    ex_iterable = ExamplesIterable(generate_examples_fn, {})
    dataset = iterable_dataset(ex_iterable).with_format("torch")
    dataloader = DataLoader(dataset, num_workers=2, batch_size=None)
    result = list(dataloader)
    expected = [example for _, example in ex_iterable]
    assert len(result) == len(expected)
    assert set(str(x) for x in result) == set(str(x) for x in expected)


@require_torch
@pytest.mark.parametrize("n_shards, num_workers", [(2, 1), (2, 2), (3, 2), (2, 3)])
def test_sharded_iterable_dataset_torch_dataloader_parallel(n_shards, num_workers):
    from torch.utils.data import DataLoader

    ex_iterable = ExamplesIterable(generate_examples_fn, {"filepaths": [f"{i}.txt" for i in range(n_shards)]})
    dataset = iterable_dataset(ex_iterable).with_format("torch")
    dataloader = DataLoader(dataset, batch_size=None, num_workers=num_workers)
    result = list(dataloader)
    expected = [example for _, example in ex_iterable]
    assert len(result) == len(expected)
    assert set(str(x) for x in result) == set(str(x) for x in expected)


@require_torch
@pytest.mark.parametrize("num_workers", [1, 2])
def test_iterable_dataset_from_hub_torch_dataloader_parallel(num_workers, tmp_path):
    from torch.utils.data import DataLoader

    dataset = load_dataset(
        SAMPLE_DATASET_IDENTIFIER, cache_dir=str(tmp_path), streaming=True, split="train"
    ).with_format("torch")
    dataloader = DataLoader(dataset, batch_size=None, num_workers=num_workers)
    result = list(dataloader)
    assert len(result) == 2


def test_iterable_dataset_info():
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
    shuffled_dataset = dataset.shuffle(seed, buffer_size=buffer_size)
    base_generator = shuffled_dataset._shuffling.generator
    if epoch is not None:
        shuffled_dataset.set_epoch(epoch)
    effective_generator = shuffled_dataset._effective_generator()
    assert effective_generator is not None
    if epoch is None or epoch == 0:
        assert is_rng_equal(base_generator, shuffled_dataset._effective_generator())
    else:
        assert not is_rng_equal(base_generator, shuffled_dataset._effective_generator())
        effective_seed = deepcopy(base_generator).integers(0, 1 << 63) - epoch
        assert is_rng_equal(np.random.default_rng(effective_seed), shuffled_dataset._effective_generator())


def test_iterable_dataset_map(
    dataset: IterableDataset,
):
    func = lambda x: {"id+1": x["id"] + 1}  # noqa: E731
    mapped_dataset = dataset.map(func)
    assert isinstance(mapped_dataset._ex_iterable, MappedExamplesIterable)
    assert mapped_dataset._ex_iterable.function is func
    assert mapped_dataset._ex_iterable.batched is False
    assert next(iter(mapped_dataset)) == {**next(iter(dataset)), **func(next(iter(generate_examples_fn()))[1])}


def test_iterable_dataset_map_batched(
    dataset: IterableDataset,
):
    func = lambda x: {"id+1": [i + 1 for i in x["id"]]}  # noqa: E731
    batch_size = 3
    dataset = dataset.map(func, batched=True, batch_size=batch_size)
    assert isinstance(dataset._ex_iterable, MappedExamplesIterable)
    assert dataset._ex_iterable.function is func
    assert dataset._ex_iterable.batch_size == batch_size
    assert next(iter(dataset)) == {"id": 0, "id+1": 1}


def test_iterable_dataset_map_complex_features(
    dataset: IterableDataset,
):
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
def test_iterable_dataset_shuffle(dataset: IterableDataset, seed, epoch):
    buffer_size = 3
    dataset = deepcopy(dataset)
    dataset._ex_iterable.kwargs["filepaths"] = ["0.txt", "1.txt"]
    dataset = dataset.shuffle(seed, buffer_size=buffer_size)
    assert isinstance(dataset._shuffling, ShufflingConfig)
    assert isinstance(dataset._shuffling.generator, np.random.Generator)
    assert is_rng_equal(dataset._shuffling.generator, np.random.default_rng(seed))
    # Effective seed is sum of seed and epoch
    if epoch is None or epoch == 0:
        effective_seed = seed
    else:
        dataset.set_epoch(epoch)
        effective_seed = np.random.default_rng(seed).integers(0, 1 << 63) - epoch
    # Shuffling adds a shuffle buffer
    expected_first_example_index = next(
        iter(BufferShuffledExamplesIterable._iter_random_indices(np.random.default_rng(effective_seed), buffer_size))
    )
    assert isinstance(dataset._ex_iterable, BufferShuffledExamplesIterable)
    # It also shuffles the underlying examples iterable
    expected_ex_iterable = ExamplesIterable(
        generate_examples_fn, {"filepaths": ["0.txt", "1.txt"]}
    ).shuffle_data_sources(np.random.default_rng(effective_seed))
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
def test_iterable_dataset_features(features):
    ex_iterable = ExamplesIterable(generate_examples_fn, {"label": 0})
    dataset = IterableDataset(ex_iterable, info=DatasetInfo(features=features))
    if features:
        expected = [features.encode_example(x) for _, x in ex_iterable]
    else:
        expected = [x for _, x in ex_iterable]
    assert list(dataset) == expected


def test_iterable_dataset_features_cast_to_python():
    ex_iterable = ExamplesIterable(
        generate_examples_fn, {"timestamp": pd.Timestamp(2020, 1, 1), "array": np.ones(5), "n": 1}
    )
    features = Features(
        {
            "id": Value("int64"),
            "timestamp": Value("timestamp[us]"),
            "array": [Value("int64")],
        }
    )
    dataset = IterableDataset(ex_iterable, info=DatasetInfo(features=features))
    assert list(dataset) == [{"timestamp": pd.Timestamp(2020, 1, 1).to_pydatetime(), "array": [1] * 5, "id": 0}]


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
def test_iterable_dataset_shuffle_after_skip_or_take(method):
    seed = 42
    n, n_shards = 3, 10
    count = 7
    ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n, "filepaths": [f"{i}.txt" for i in range(n_shards)]})
    dataset = IterableDataset(ex_iterable)
    dataset = dataset.skip(n) if method == "skip" else dataset.take(count)
    shuffled_dataset = dataset.shuffle(seed, buffer_size=DEFAULT_N_EXAMPLES)
    # shuffling a skip/take dataset should keep the same examples and don't shuffle the shards
    key = lambda x: f"{x['filepath']}_{x['id']}"  # noqa: E731
    assert sorted(dataset, key=key) == sorted(shuffled_dataset, key=key)


def test_iterable_dataset_add_column(dataset_with_several_columns):
    new_column = list(range(DEFAULT_N_EXAMPLES))
    new_dataset = dataset_with_several_columns.add_column("new_column", new_column)
    assert list(new_dataset) == [
        {**example, "new_column": idx} for idx, example in enumerate(dataset_with_several_columns)
    ]


def test_iterable_dataset_rename_column(dataset_with_several_columns):
    new_dataset = dataset_with_several_columns.rename_column("id", "new_id")
    assert list(new_dataset) == [
        {("new_id" if k == "id" else k): v for k, v in example.items()} for example in dataset_with_several_columns
    ]


def test_iterable_dataset_rename_columns(dataset_with_several_columns):
    column_mapping = {"id": "new_id", "filepath": "filename"}
    new_dataset = dataset_with_several_columns.rename_columns(column_mapping)
    assert list(new_dataset) == [
        {column_mapping.get(k, k): v for k, v in example.items()} for example in dataset_with_several_columns
    ]


def test_iterable_dataset_remove_columns(dataset_with_several_columns):
    new_dataset = dataset_with_several_columns.remove_columns("id")
    assert list(new_dataset) == [
        {k: v for k, v in example.items() if k != "id"} for example in dataset_with_several_columns
    ]
    new_dataset = dataset_with_several_columns.remove_columns(["id", "filepath"])
    assert list(new_dataset) == [
        {k: v for k, v in example.items() if k != "id" and k != "filepath"} for example in dataset_with_several_columns
    ]


def test_iterable_dataset_cast_column():
    ex_iterable = ExamplesIterable(generate_examples_fn, {"label": 10})
    features = Features({"id": Value("int64"), "label": Value("int64")})
    dataset = IterableDataset(ex_iterable, info=DatasetInfo(features=features))
    casted_dataset = dataset.cast_column("label", Value("bool"))
    casted_features = features.copy()
    casted_features["label"] = Value("bool")
    assert list(casted_dataset) == [casted_features.encode_example(ex) for _, ex in ex_iterable]


def test_iterable_dataset_cast():
    ex_iterable = ExamplesIterable(generate_examples_fn, {"label": 10})
    features = Features({"id": Value("int64"), "label": Value("int64")})
    dataset = IterableDataset(ex_iterable, info=DatasetInfo(features=features))
    new_features = Features({"id": Value("int64"), "label": Value("bool")})
    casted_dataset = dataset.cast(new_features)
    assert list(casted_dataset) == [new_features.encode_example(ex) for _, ex in ex_iterable]


def test_concatenate_datasets():
    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"label": 10})
    dataset1 = IterableDataset(ex_iterable1)
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {"label": 5})
    dataset2 = IterableDataset(ex_iterable2)
    concatenated_dataset = concatenate_datasets([dataset1, dataset2])
    assert list(concatenated_dataset) == list(dataset1) + list(dataset2)


def test_concatenate_datasets_resolves_features():
    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"label": 10})
    dataset1 = IterableDataset(ex_iterable1)
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {"label": 5})
    dataset2 = IterableDataset(ex_iterable2)
    concatenated_dataset = concatenate_datasets([dataset1, dataset2])
    assert concatenated_dataset.features is not None
    assert sorted(concatenated_dataset.features) == ["id", "label"]


def test_concatenate_datasets_with_different_columns():
    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"label": 10})
    dataset1 = IterableDataset(ex_iterable1)
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {})
    dataset2 = IterableDataset(ex_iterable2)
    # missing column "label" -> it should be replaced with nulls
    extended_dataset2_list = [{"label": None, **x} for x in dataset2]

    concatenated_dataset = concatenate_datasets([dataset1, dataset2])
    assert list(concatenated_dataset) == list(dataset1) + extended_dataset2_list
    # change order
    concatenated_dataset = concatenate_datasets([dataset2, dataset1])
    assert list(concatenated_dataset) == extended_dataset2_list + list(dataset1)


def test_concatenate_datasets_axis_1():
    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"label1": 10})
    dataset1 = IterableDataset(ex_iterable1)
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {"label2": 5})
    dataset2 = IterableDataset(ex_iterable2)
    with pytest.raises(ValueError):  # column "id" is duplicated -> raise an error
        concatenate_datasets([dataset1, dataset2], axis=1)
    concatenated_dataset = concatenate_datasets([dataset1, dataset2.remove_columns("id")], axis=1)
    assert list(concatenated_dataset) == [{**x, **y} for x, y in zip(dataset1, dataset2)]


def test_concatenate_datasets_axis_1_resolves_features():
    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"label1": 10})
    dataset1 = IterableDataset(ex_iterable1)
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {"label2": 5})
    dataset2 = IterableDataset(ex_iterable2).remove_columns("id")
    concatenated_dataset = concatenate_datasets([dataset1, dataset2], axis=1)
    assert concatenated_dataset.features is not None
    assert sorted(concatenated_dataset.features) == ["id", "label1", "label2"]


def test_concatenate_datasets_axis_1_with_different_lengths():
    n1 = 10
    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"label1": 10, "n": n1})
    dataset1 = IterableDataset(ex_iterable1)
    n2 = 5
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {"label2": 5, "n": n2})
    dataset2 = IterableDataset(ex_iterable2).remove_columns("id")
    # missing rows -> they should be replaced with nulls
    extended_dataset2_list = list(dataset2) + [{"label2": None}] * (n1 - n2)

    concatenated_dataset = concatenate_datasets([dataset1, dataset2], axis=1)
    assert list(concatenated_dataset) == [{**x, **y} for x, y in zip(dataset1, extended_dataset2_list)]
    # change order
    concatenated_dataset = concatenate_datasets([dataset2, dataset1], axis=1)
    assert list(concatenated_dataset) == [{**x, **y} for x, y in zip(extended_dataset2_list, dataset1)]


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


def test_interleave_datasets_with_features(
    dataset: IterableDataset,
):
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
