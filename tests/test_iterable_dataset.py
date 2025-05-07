import asyncio
import pickle
import time
from copy import deepcopy
from dataclasses import dataclass
from itertools import chain, cycle, islice
from unittest.mock import patch

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pytest

from datasets import Dataset, load_dataset
from datasets.combine import concatenate_datasets, interleave_datasets
from datasets.distributed import split_dataset_by_node
from datasets.features import (
    ClassLabel,
    Features,
    Image,
    Value,
)
from datasets.formatting import Formatter, get_format_type_from_alias
from datasets.info import DatasetInfo
from datasets.iterable_dataset import (
    ArrowExamplesIterable,
    BufferShuffledExamplesIterable,
    CyclingMultiSourcesExamplesIterable,
    ExamplesIterable,
    FilteredExamplesIterable,
    FormattedExamplesIterable,
    FormattingConfig,
    HorizontallyConcatenatedMultiSourcesExamplesIterable,
    IterableDataset,
    MappedExamplesIterable,
    RandomlyCyclingMultiSourcesExamplesIterable,
    RebatchedArrowExamplesIterable,
    RepeatExamplesIterable,
    SelectColumnsIterable,
    ShuffledDataSourcesArrowExamplesIterable,
    ShuffledDataSourcesExamplesIterable,
    ShufflingConfig,
    SkipExamplesIterable,
    StepExamplesIterable,
    TakeExamplesIterable,
    VerticallyConcatenatedMultiSourcesExamplesIterable,
    _BaseExamplesIterable,
    _batch_to_examples,
    _convert_to_arrow,
    _examples_to_batch,
)

from .utils import (
    assert_arrow_memory_doesnt_increase,
    is_rng_equal,
    require_dill_gt_0_3_2,
    require_jax,
    require_not_windows,
    require_numpy1_on_windows,
    require_polars,
    require_pyspark,
    require_tf,
    require_torch,
    require_torchdata_stateful_dataloader,
)


DEFAULT_N_EXAMPLES = 20
DEFAULT_BATCH_SIZE = 4
DEFAULT_FILEPATH = "file.txt"

SAMPLE_DATASET_IDENTIFIER = "hf-internal-testing/dataset_with_script"  # has dataset script


def generate_examples_fn(**kwargs):
    kwargs = kwargs.copy()
    n = kwargs.pop("n", DEFAULT_N_EXAMPLES)
    filepaths = kwargs.pop("filepaths", None)
    for filepath in filepaths or [DEFAULT_FILEPATH]:
        if filepaths is not None:
            kwargs["filepath"] = filepath
        for i in range(n):
            yield f"{filepath}_{i}", {"id": i, **kwargs}


def generate_tables_fn(**kwargs):
    kwargs = kwargs.copy()
    n = kwargs.pop("n", DEFAULT_N_EXAMPLES)
    batch_size = kwargs.pop("batch_size", DEFAULT_BATCH_SIZE)
    filepaths = kwargs.pop("filepaths", None)
    for filepath in filepaths or [DEFAULT_FILEPATH]:
        buffer = []
        batch_idx = 0
        if filepaths is not None:
            kwargs["filepath"] = filepath
        for i in range(n):
            buffer.append({"id": i, **kwargs})
            if len(buffer) == batch_size:
                yield f"{filepath}_{batch_idx}", pa.Table.from_pylist(buffer)
                buffer = []
                batch_idx += 1
        yield batch_idx, pa.Table.from_pylist(buffer)


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


@pytest.fixture
def arrow_file(tmp_path_factory, dataset: IterableDataset):
    filename = str(tmp_path_factory.mktemp("data") / "file.arrow")
    Dataset.from_generator(dataset.__iter__).map(cache_file_name=filename)
    return filename


def assert_load_state_dict_resumes_iteration(ex_iterable: _BaseExamplesIterable):
    ex_iterable._init_state_dict()
    state_dicts = [ex_iterable.state_dict()]
    examples = []
    for _, example in ex_iterable:
        state_dicts.append(ex_iterable.state_dict())
        examples.append(example)
    for i, state_dict in enumerate(state_dicts):
        ex_iterable.load_state_dict(state_dict)
        examples_after_resuming = [example for _, example in ex_iterable]
        assert examples_after_resuming == examples[i:], f"resuming from idx {i} with {state_dict=}"


def assert_load_state_dict_resumes_arrow_iteration(ex_iterable: _BaseExamplesIterable):
    assert ex_iterable.iter_arrow is not None
    ex_iterable._init_state_dict()
    state_dicts = [ex_iterable.state_dict()]
    examples = []
    indices = [0]
    for _, pa_table in ex_iterable.iter_arrow():
        state_dicts.append(ex_iterable.state_dict())
        examples.extend(pa_table.to_pylist())
        indices.append(indices[-1] + len(pa_table))
    for i, state_dict in zip(indices, state_dicts):
        ex_iterable.load_state_dict(state_dict)
        examples_after_resuming = [
            example for _, pa_table in ex_iterable.iter_arrow() for example in pa_table.to_pylist()
        ]
        assert examples_after_resuming == examples[i:], f"resuming from idx {i} with {state_dict=}"


################################
#
#   Utilities tests
#
################################


@pytest.mark.parametrize("batch_size", [1, 2, 3, 9, 10, 11, 20])
@pytest.mark.parametrize("drop_last_batch", [False, True])
def test_convert_to_arrow(batch_size, drop_last_batch):
    examples = [{"foo": i} for i in range(10)]
    full_table = pa.Table.from_pylist(examples)
    num_rows = len(full_table) if not drop_last_batch else len(full_table) // batch_size * batch_size
    num_batches = (num_rows // batch_size) + 1 if num_rows % batch_size else num_rows // batch_size
    subtables = list(
        _convert_to_arrow(
            list(enumerate(examples)),
            batch_size=batch_size,
            drop_last_batch=drop_last_batch,
        )
    )
    assert len(subtables) == num_batches
    if drop_last_batch:
        assert all(len(subtable) == batch_size for _, subtable in subtables)
    else:
        assert all(len(subtable) == batch_size for _, subtable in subtables[:-1])
        assert len(subtables[-1][1]) <= batch_size
    if num_rows > 0:
        reloaded = pa.concat_tables([subtable for _, subtable in subtables])
        assert full_table.slice(0, num_rows).to_pydict() == reloaded.to_pydict()


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
    assert ex_iterable.iter_arrow is None
    assert_load_state_dict_resumes_iteration(ex_iterable)


def test_examples_iterable_with_kwargs():
    ex_iterable = ExamplesIterable(generate_examples_fn, {"filepaths": ["0.txt", "1.txt"], "split": "train"})
    expected = list(generate_examples_fn(filepaths=["0.txt", "1.txt"], split="train"))
    assert list(ex_iterable) == expected
    assert all("split" in ex for _, ex in ex_iterable)
    assert sorted({ex["filepath"] for _, ex in ex_iterable}) == ["0.txt", "1.txt"]
    assert_load_state_dict_resumes_iteration(ex_iterable)


def test_examples_iterable_shuffle_data_sources():
    ex_iterable = ExamplesIterable(generate_examples_fn, {"filepaths": ["0.txt", "1.txt"]})
    ex_iterable = ex_iterable.shuffle_data_sources(np.random.default_rng(40))
    expected = list(generate_examples_fn(filepaths=["1.txt", "0.txt"]))  # shuffle the filepaths
    assert list(ex_iterable) == expected
    assert_load_state_dict_resumes_iteration(ex_iterable)


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
    assert_load_state_dict_resumes_iteration(ex_iterable)


def test_arrow_examples_iterable():
    ex_iterable = ArrowExamplesIterable(generate_tables_fn, {})
    expected = sum([pa_table.to_pylist() for _, pa_table in generate_tables_fn()], [])
    assert next(iter(ex_iterable))[1] == expected[0]
    assert [example for _, example in ex_iterable] == expected
    expected = list(generate_tables_fn())
    assert list(ex_iterable.iter_arrow()) == expected
    assert_load_state_dict_resumes_iteration(ex_iterable)


def test_arrow_examples_iterable_with_kwargs():
    ex_iterable = ArrowExamplesIterable(generate_tables_fn, {"filepaths": ["0.txt", "1.txt"], "split": "train"})
    expected = sum(
        [pa_table.to_pylist() for _, pa_table in generate_tables_fn(filepaths=["0.txt", "1.txt"], split="train")], []
    )
    assert [example for _, example in ex_iterable] == expected
    assert all("split" in ex for _, ex in ex_iterable)
    assert sorted({ex["filepath"] for _, ex in ex_iterable}) == ["0.txt", "1.txt"]
    expected = list(generate_tables_fn(filepaths=["0.txt", "1.txt"], split="train"))
    assert list(ex_iterable.iter_arrow()) == expected
    assert_load_state_dict_resumes_iteration(ex_iterable)


def test_arrow_examples_iterable_shuffle_data_sources():
    ex_iterable = ArrowExamplesIterable(generate_tables_fn, {"filepaths": ["0.txt", "1.txt"]})
    ex_iterable = ex_iterable.shuffle_data_sources(np.random.default_rng(40))
    expected = sum(
        [pa_table.to_pylist() for _, pa_table in generate_tables_fn(filepaths=["1.txt", "0.txt"])], []
    )  # shuffle the filepaths
    assert [example for _, example in ex_iterable] == expected
    expected = list(generate_tables_fn(filepaths=["1.txt", "0.txt"]))
    assert list(ex_iterable.iter_arrow()) == expected
    assert_load_state_dict_resumes_iteration(ex_iterable)


@pytest.mark.parametrize(
    "tables",
    [
        [pa.table({"foo": range(10)})],
        [pa.table({"foo": range(5 * i, 5 * (i + 1))}) for i in range(2)],
        [pa.table({"foo": range(5 * i, 5 * (i + 1))}) for i in range(7)],
        [pa.table({"foo": [i]}) for i in range(10)],
    ],
)
@pytest.mark.parametrize("batch_size", [1, 2, 3, 7, 9, 10, 11, 13, 20])
@pytest.mark.parametrize("drop_last_batch", [False, True])
def test_rebatched_arrow_examples_iterable(tables, batch_size, drop_last_batch):
    full_table = pa.concat_tables(tables)
    num_rows = len(full_table) if not drop_last_batch else len(full_table) // batch_size * batch_size
    num_batches = (num_rows // batch_size) + 1 if num_rows % batch_size else num_rows // batch_size

    def gen(tables):
        for i, table in enumerate(tables):
            yield str(i), table

    ex_iterable = ArrowExamplesIterable(gen, {"tables": tables})
    ex_iterable = RebatchedArrowExamplesIterable(ex_iterable, batch_size=batch_size, drop_last_batch=drop_last_batch)
    subtables = list(ex_iterable.iter_arrow())
    assert len(subtables) == num_batches
    if drop_last_batch:
        assert all(len(subtable) == batch_size for _, subtable in subtables)
    else:
        assert all(len(subtable) == batch_size for _, subtable in subtables[:-1])
        assert len(subtables[-1][1]) <= batch_size
    if num_rows > 0:
        reloaded = pa.concat_tables([subtable for _, subtable in subtables])
        assert full_table.slice(0, num_rows).to_pydict() == reloaded.to_pydict()
    assert_load_state_dict_resumes_iteration(ex_iterable)
    assert_load_state_dict_resumes_arrow_iteration(ex_iterable)


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
    assert sorted(ex_iterable) == sorted(all_examples)


def test_cycling_multi_sources_examples_iterable():
    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"text": "foo"})
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {"text": "bar"})
    ex_iterable = CyclingMultiSourcesExamplesIterable([ex_iterable1, ex_iterable2])
    expected = list(chain(*zip(generate_examples_fn(text="foo"), generate_examples_fn(text="bar"))))

    # The cycling stops as soon as one iterable is out of examples (here ex_iterable1), so the last sample from ex_iterable2 is unecessary
    expected = expected[:-1]

    assert next(iter(ex_iterable)) == expected[0]
    assert list(ex_iterable) == expected
    assert all((x["id"], x["text"]) == (i // 2, "bar" if i % 2 else "foo") for i, (_, x) in enumerate(ex_iterable))
    assert_load_state_dict_resumes_iteration(ex_iterable)


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
    indices_iterator = cycle(rng.choice(len(iterators), size=1000, p=probabilities))
    expected = []
    lengths = [len(list(ex_iterable1)), len(list(ex_iterable2))]
    for i in indices_iterator:
        if lengths[0] == 0 or lengths[1] == 0:
            break
        for key, example in iterators[i]:
            expected.append((key, example))
            lengths[i] -= 1
            break
        else:
            break

    assert next(iter(ex_iterable)) == expected[0]
    assert list(ex_iterable) == expected
    assert_load_state_dict_resumes_iteration(ex_iterable)


@pytest.mark.parametrize("probabilities", [None, (0.5, 0.5), (0.9, 0.1)])
@pytest.mark.parametrize("stopping_strategy", ["first_exhausted", "all_exhausted"])
@pytest.mark.parametrize("step", [-1, 0, 5, 20, 30, 300])
def test_randomly_cycling_multi_sources_examples_iterable_state(probabilities, stopping_strategy, step):
    seed = 42
    generator = np.random.default_rng(seed)
    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"text": "foo"})
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {"text": "bar"})
    ex_iterable = RandomlyCyclingMultiSourcesExamplesIterable(
        [ex_iterable1, ex_iterable2],
        generator=generator,
        probabilities=probabilities,
        stopping_strategy=stopping_strategy,
    )
    step = min(step, len(list(ex_iterable)) - 1)
    ex_iterable._init_state_dict()
    state_dict = ex_iterable.state_dict()
    examples = []
    for i, x in enumerate(ex_iterable):
        examples.append(x)
        if i == step:
            state_dict = ex_iterable.state_dict()
    ex_iterable.load_state_dict(state_dict)
    assert examples[step + 1 :] == list(ex_iterable)


@pytest.mark.parametrize(
    "n, func, batched, batch_size",
    [
        (3, lambda x: {"id+1": x["id"] + 1}, False, None),  # just add 1 to the id
        (3, lambda x: {"id+1": [x["id"][0] + 1]}, True, 1),  # same with bs=1
        (5, lambda x: {"id+1": [i + 1 for i in x["id"]]}, True, 10),  # same with bs=10
        (25, lambda x: {"id+1": [i + 1 for i in x["id"]]}, True, 10),  # same with bs=10
        (5, lambda x: {"id+1": [i + 1 for i in x["id"]]}, True, None),  # same with bs=None
        (5, lambda x: {"id+1": [i + 1 for i in x["id"]]}, True, -1),  # same with bs<=0
        (3, lambda x: {k: v * 2 for k, v in x.items()}, True, 1),  # make a duplicate of each example
    ],
)
def test_mapped_examples_iterable(n, func, batched, batch_size):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    ex_iterable = MappedExamplesIterable(base_ex_iterable, func, batched=batched, batch_size=batch_size)
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    if batched is False:
        expected = [{**x, **func(x)} for x in all_examples]
    else:
        # For batched map we have to format the examples as a batch (i.e. in one single dictionary) to pass the batch to the function
        all_transformed_examples = []
        # If batch_size is None or <=0, we use the whole dataset as a single batch
        if batch_size is None or batch_size <= 0:
            batch_size = len(all_examples)
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            batch = _examples_to_batch(examples)
            transformed_batch = func(batch)
            all_transformed_examples.extend(_batch_to_examples(transformed_batch))
        expected = _examples_to_batch(all_examples)
        expected.update(_examples_to_batch(all_transformed_examples))
        expected = list(_batch_to_examples(expected))
    assert next(iter(ex_iterable))[1] == expected[0]
    assert [x for _, x in ex_iterable] == expected
    assert_load_state_dict_resumes_iteration(ex_iterable)


@pytest.mark.parametrize(
    "n, func, batched, batch_size",
    [
        (3, lambda x: {"id+1": x["id"] + 1}, False, None),  # just add 1 to the id
        (3, lambda x: {"id+1": [x["id"][0] + 1]}, True, 1),  # same with bs=1
        (5, lambda x: {"id+1": [i + 1 for i in x["id"]]}, True, 10),  # same with bs=10
        (25, lambda x: {"id+1": [i + 1 for i in x["id"]]}, True, 10),  # same with bs=10
        (5, lambda x: {"id+1": [i + 1 for i in x["id"]]}, True, None),  # same with bs=None
        (5, lambda x: {"id+1": [i + 1 for i in x["id"]]}, True, -1),  # same with bs<=0
        (3, lambda x: {k: v * 2 for k, v in x.items()}, True, 1),  # make a duplicate of each example
    ],
)
def test_mapped_examples_iterable_drop_last_batch(n, func, batched, batch_size):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    ex_iterable = MappedExamplesIterable(
        base_ex_iterable, func, batched=batched, batch_size=batch_size, drop_last_batch=True
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    is_empty = False
    if batched is False:
        # `drop_last_batch` has no effect here
        expected = [{**x, **func(x)} for x in all_examples]
    else:
        # For batched map we have to format the examples as a batch (i.e. in one single dictionary) to pass the batch to the function
        all_transformed_examples = []
        # If batch_size is None or <=0, we use the whole dataset as a single batch
        if batch_size is None or batch_size <= 0:
            batch_size = len(all_examples)
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
        assert [x for _, x in ex_iterable] == expected
    else:
        with pytest.raises(StopIteration):
            next(iter(ex_iterable))


def _wrap_async(func, *args, **kwargs):
    async def wrapped_func(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapped_func


@pytest.mark.parametrize(
    "n, func, batched, batch_size",
    [
        (3, lambda x, index: {"id+idx": x["id"] + index}, False, None),  # add the index to the id
        (
            25,
            lambda x, indices: {"id+idx": [i + j for i, j in zip(x["id"], indices)]},
            True,
            10,
        ),  # add the index to the id
        (5, lambda x, indices: {"id+idx": [i + j for i, j in zip(x["id"], indices)]}, True, None),  # same with bs=None
        (5, lambda x, indices: {"id+idx": [i + j for i, j in zip(x["id"], indices)]}, True, -1),  # same with bs<=0
    ],
)
@pytest.mark.parametrize("wrapper", [lambda x: x, _wrap_async])
def test_mapped_examples_iterable_with_indices(n, func, batched, batch_size, wrapper):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    ex_iterable = MappedExamplesIterable(
        base_ex_iterable, wrapper(func), batched=batched, batch_size=batch_size, with_indices=True
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    if batched is False:
        expected = [{**x, **func(x, idx)} for idx, x in enumerate(all_examples)]
    else:
        # For batched map we have to format the examples as a batch (i.e. in one single dictionary) to pass the batch to the function
        all_transformed_examples = []
        # If batch_size is None or <=0, we use the whole dataset as a single batch
        if batch_size is None or batch_size <= 0:
            batch_size = len(all_examples)
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
    assert [x for _, x in ex_iterable] == expected
    assert_load_state_dict_resumes_iteration(ex_iterable)


@pytest.mark.parametrize(
    "n, func, batched, batch_size, remove_columns",
    [
        (3, lambda x: {"id+1": x["id"] + 1}, False, None, ["extra_column"]),  # just add 1 to the id
        (25, lambda x: {"id+1": [i + 1 for i in x["id"]]}, True, 10, ["extra_column"]),  # same with bs=10
        (
            50,
            lambda x: {"foo": ["bar"] * np.random.default_rng(x["id"][0]).integers(0, 10)},
            True,
            8,
            ["extra_column", "id"],
        ),  # make a duplicate of each example
        (5, lambda x: {"id+1": [i + 1 for i in x["id"]]}, True, None, ["extra_column"]),  # same with bs=None
        (5, lambda x: {"id+1": [i + 1 for i in x["id"]]}, True, -1, ["extra_column"]),  # same with bs<=0
    ],
)
def test_mapped_examples_iterable_remove_columns(n, func, batched, batch_size, remove_columns):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n, "extra_column": "foo"})
    ex_iterable = MappedExamplesIterable(
        base_ex_iterable, func, batched=batched, batch_size=batch_size, remove_columns=remove_columns
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    columns_to_remove = remove_columns if isinstance(remove_columns, list) else [remove_columns]
    if batched is False:
        expected = [{**{k: v for k, v in x.items() if k not in columns_to_remove}, **func(x)} for x in all_examples]
    else:
        # For batched map we have to format the examples as a batch (i.e. in one single dictionary) to pass the batch to the function
        all_transformed_examples = []
        # If batch_size is None or <=0, we use the whole dataset as a single batch
        if batch_size is None or batch_size <= 0:
            batch_size = len(all_examples)
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            batch = _examples_to_batch(examples)
            transformed_batch = func(batch)
            all_transformed_examples.extend(_batch_to_examples(transformed_batch))
        expected = {k: v for k, v in _examples_to_batch(all_examples).items() if k not in columns_to_remove}
        expected.update(_examples_to_batch(all_transformed_examples))
        expected = list(_batch_to_examples(expected))
    assert next(iter(ex_iterable))[1] == expected[0]
    assert [x for _, x in ex_iterable] == expected
    assert_load_state_dict_resumes_iteration(ex_iterable)


# issue #7345 and PR #7353
@pytest.mark.parametrize("batched", [False, True])
@pytest.mark.parametrize("batch_size", [None, 2])
@pytest.mark.parametrize("input_columns", [None, ["i"]])
@pytest.mark.parametrize("remove_columns", [None, ["i"]])
@pytest.mark.parametrize("new_output", [False, True])
def test_iterable_dataset_vs_dataset_map(batched, batch_size, input_columns, remove_columns, new_output):
    if input_columns is not None and not new_output:
        return

    ds1 = Dataset.from_list([{"i": i} for i in range(4)])

    if batched:

        def f1(i):
            return {"i": [j + 1 for j in i]}
    else:

        def f1(i):
            return {"i": i + 1}

    if input_columns is None:

        def f2(x):
            return f1(x["i"])
    else:
        f2 = f1

    if new_output:
        f = f2
    else:

        def f(x):
            x["i"] = f2(x)["i"]
            return x

    r = [
        list(
            ds2.map(
                f,
                batch_size=batch_size,
                batched=batched,
                remove_columns=remove_columns,
                input_columns=input_columns,
            )
        )
        for ds2 in [ds1, ds1.to_iterable_dataset()]
    ]
    r[1] = [x for x in r[1] if len(x) > 0]
    assert len(r[0]) == len(r[1])
    assert all(x == y for x, y in zip(*r))


@pytest.mark.parametrize(
    "n, func, batched, batch_size, fn_kwargs",
    [
        (3, lambda x, y=0: {"id+y": x["id"] + y}, False, None, None),
        (3, lambda x, y=0: {"id+y": x["id"] + y}, False, None, {"y": 3}),
        (25, lambda x, y=0: {"id+y": [i + y for i in x["id"]]}, True, 10, {"y": 3}),
        (5, lambda x, y=0: {"id+y": [i + y for i in x["id"]]}, True, None, {"y": 3}),  # same with bs=None
        (5, lambda x, y=0: {"id+y": [i + y for i in x["id"]]}, True, -1, {"y": 3}),  # same with bs<=0
    ],
)
def test_mapped_examples_iterable_fn_kwargs(n, func, batched, batch_size, fn_kwargs):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    ex_iterable = MappedExamplesIterable(
        base_ex_iterable, func, batched=batched, batch_size=batch_size, fn_kwargs=fn_kwargs
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    if fn_kwargs is None:
        fn_kwargs = {}
    if batched is False:
        expected = [{**x, **func(x, **fn_kwargs)} for x in all_examples]
    else:
        # For batched map we have to format the examples as a batch (i.e. in one single dictionary) to pass the batch to the function
        all_transformed_examples = []
        # If batch_size is None or <=0, we use the whole dataset as a single batch
        if batch_size is None or batch_size <= 0:
            batch_size = len(all_examples)
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            batch = _examples_to_batch(examples)
            transformed_batch = func(batch, **fn_kwargs)
            all_transformed_examples.extend(_batch_to_examples(transformed_batch))
        expected = _examples_to_batch(all_examples)
        expected.update(_examples_to_batch(all_transformed_examples))
        expected = list(_batch_to_examples(expected))
    assert next(iter(ex_iterable))[1] == expected[0]
    assert [x for _, x in ex_iterable] == expected
    assert_load_state_dict_resumes_iteration(ex_iterable)


@pytest.mark.parametrize(
    "n, func, batched, batch_size, input_columns",
    [
        (3, lambda id_: {"id+1": id_ + 1}, False, None, ["id"]),  # just add 1 to the id
        (25, lambda ids_: {"id+1": [i + 1 for i in ids_]}, True, 10, ["id"]),  # same with bs=10
        (5, lambda ids_: {"id+1": [i + 1 for i in ids_]}, True, None, ["id"]),  # same with bs=None
        (5, lambda ids_: {"id+1": [i + 1 for i in ids_]}, True, -1, ["id"]),  # same with bs<=0
    ],
)
def test_mapped_examples_iterable_input_columns(n, func, batched, batch_size, input_columns):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    ex_iterable = MappedExamplesIterable(
        base_ex_iterable, func, batched=batched, batch_size=batch_size, input_columns=input_columns
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    columns_to_input = input_columns if isinstance(input_columns, list) else [input_columns]
    if batched is False:
        expected = [{**x, **func(*[x[col] for col in columns_to_input])} for x in all_examples]
    else:
        # For batched map we have to format the examples as a batch (i.e. in one single dictionary) to pass the batch to the function
        all_transformed_examples = []
        # If batch_size is None or <=0, we use the whole dataset as a single batch
        if batch_size is None or batch_size <= 0:
            batch_size = len(all_examples)
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            batch = _examples_to_batch(examples)
            transformed_batch = func(*[batch[col] for col in columns_to_input])
            all_transformed_examples.extend(_batch_to_examples(transformed_batch))
        expected = _examples_to_batch(all_examples)
        expected.update(_examples_to_batch(all_transformed_examples))
        expected = list(_batch_to_examples(expected))
    assert next(iter(ex_iterable))[1] == expected[0]
    assert [x for _, x in ex_iterable] == expected
    assert_load_state_dict_resumes_iteration(ex_iterable)


@pytest.mark.parametrize(
    "n, func, batched, batch_size",
    [
        (3, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), False, None),  # just add 1 to the id
        (3, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), True, 1),  # same with bs=1
        (5, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), True, 10),  # same with bs=10
        (25, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), True, 10),  # same with bs=10
        (5, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), True, None),  # same with bs=None
        (5, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), True, -1),  # same with bs<=0
        (3, lambda t: pa.concat_tables([t] * 2), True, 1),  # make a duplicate of each example
    ],
)
def test_mapped_examples_iterable_arrow_format(n, func, batched, batch_size):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    base_ex_iterable = RebatchedArrowExamplesIterable(base_ex_iterable, batch_size=batch_size if batched else 1)
    ex_iterable = MappedExamplesIterable(
        base_ex_iterable,
        func,
        batched=batched,
        batch_size=batch_size,
        formatting=FormattingConfig(format_type="arrow"),
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    if batched is False:
        expected = [func(pa.Table.from_pylist([x])).to_pylist()[0] for x in all_examples]
    else:
        expected = []
        # If batch_size is None or <=0, we use the whole dataset as a single batch
        if batch_size is None or batch_size <= 0:
            batch_size = len(all_examples)
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            batch = pa.Table.from_pylist(examples)
            expected.extend(func(batch).to_pylist())
    assert next(iter(ex_iterable))[1] == expected[0]
    assert [x for _, x in ex_iterable] == expected
    assert_load_state_dict_resumes_iteration(ex_iterable)
    assert_load_state_dict_resumes_arrow_iteration(ex_iterable)


@pytest.mark.parametrize(
    "n, func, batched, batch_size",
    [
        (3, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), False, None),  # just add 1 to the id
        (3, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), True, 1),  # same with bs=1
        (5, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), True, 10),  # same with bs=10
        (25, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), True, 10),  # same with bs=10
        (5, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), True, None),  # same with bs=None
        (5, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), True, -1),  # same with bs<=0
        (3, lambda t: pa.concat_tables([t] * 2), True, 1),  # make a duplicate of each example
    ],
)
def test_mapped_examples_iterable_arrow_format_from_arrow_examples_iterable(n, func, batched, batch_size):
    base_ex_iterable = ArrowExamplesIterable(generate_tables_fn, {"n": n})
    base_ex_iterable = RebatchedArrowExamplesIterable(base_ex_iterable, batch_size=batch_size if batched else 1)
    ex_iterable = MappedExamplesIterable(
        base_ex_iterable,
        func,
        batched=batched,
        batch_size=batch_size,
        formatting=FormattingConfig(format_type="arrow"),
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    if batched is False:
        expected = [func(pa.Table.from_pylist([x])).to_pylist()[0] for x in all_examples]
    else:
        expected = []
        # If batch_size is None or <=0, we use the whole dataset as a single batch
        if batch_size is None or batch_size <= 0:
            batch_size = len(all_examples)
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            batch = pa.Table.from_pylist(examples)
            expected.extend(func(batch).to_pylist())
    assert next(iter(ex_iterable))[1] == expected[0]
    assert [x for _, x in ex_iterable] == expected
    assert_load_state_dict_resumes_iteration(ex_iterable)
    assert_load_state_dict_resumes_arrow_iteration(ex_iterable)


@pytest.mark.parametrize(
    "n, func, batched, batch_size",
    [
        (3, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), False, None),  # just add 1 to the id
        (3, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), True, 1),  # same with bs=1
        (5, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), True, 10),  # same with bs=10
        (25, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), True, 10),  # same with bs=10
        (5, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), True, None),  # same with bs=None
        (5, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), True, -1),  # same with bs<=0
        (3, lambda t: pa.concat_tables([t] * 2), True, 1),  # make a duplicate of each example
    ],
)
def test_mapped_examples_iterable_drop_last_batch_and_arrow_format(n, func, batched, batch_size):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    base_ex_iterable = RebatchedArrowExamplesIterable(base_ex_iterable, batch_size=batch_size if batched else 1)
    ex_iterable = MappedExamplesIterable(
        base_ex_iterable,
        func,
        batched=batched,
        batch_size=batch_size,
        drop_last_batch=True,
        formatting=FormattingConfig(format_type="arrow"),
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    is_empty = False
    if batched is False:
        # `drop_last_batch` has no effect here
        expected = [func(pa.Table.from_pylist([x])).to_pylist()[0] for x in all_examples]
    else:
        all_transformed_examples = []
        # If batch_size is None or <=0, we use the whole dataset as a single batch
        if batch_size is None or batch_size <= 0:
            batch_size = len(all_examples)
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            if len(examples) < batch_size:  # ignore last batch
                break
            batch = pa.Table.from_pylist(examples)
            out = func(batch)
            all_transformed_examples.extend(
                out.to_pylist()
            )  # we don't merge with input since they're arrow tables and not dictionaries
        all_examples = all_examples if n % batch_size == 0 else all_examples[: n // batch_size * batch_size]
        if all_examples:
            expected = all_transformed_examples
        else:
            is_empty = True

    if not is_empty:
        assert next(iter(ex_iterable))[1] == expected[0]
        assert [x for _, x in ex_iterable] == expected
    else:
        with pytest.raises(StopIteration):
            next(iter(ex_iterable))


@pytest.mark.parametrize(
    "n, func, batched, batch_size",
    [
        (
            3,
            lambda t, index: t.append_column("id+idx", pc.add(t["id"], index)),
            False,
            None,
        ),  # add the index to the id
        (
            25,
            lambda t, indices: t.append_column("id+idx", pc.add(t["id"], indices)),
            True,
            10,
        ),  # add the index to the id
        (5, lambda t, indices: t.append_column("id+idx", pc.add(t["id"], indices)), True, None),  # same with bs=None
        (5, lambda t, indices: t.append_column("id+idx", pc.add(t["id"], indices)), True, -1),  # same with bs<=0
    ],
)
def test_mapped_examples_iterable_with_indices_and_arrow_format(n, func, batched, batch_size):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    base_ex_iterable = RebatchedArrowExamplesIterable(base_ex_iterable, batch_size=batch_size if batched else 1)
    ex_iterable = MappedExamplesIterable(
        base_ex_iterable,
        func,
        batched=batched,
        batch_size=batch_size,
        with_indices=True,
        formatting=FormattingConfig(format_type="arrow"),
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    if batched is False:
        expected = [func(pa.Table.from_pylist([x]), i).to_pylist()[0] for i, x in enumerate(all_examples)]
    else:
        expected = []
        # If batch_size is None or <=0, we use the whole dataset as a single batch
        if batch_size is None or batch_size <= 0:
            batch_size = len(all_examples)
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            batch = pa.Table.from_pylist(examples)
            expected.extend(func(batch, list(range(batch_offset, batch_offset + len(batch)))).to_pylist())
    assert next(iter(ex_iterable))[1] == expected[0]
    assert [x for _, x in ex_iterable] == expected
    assert_load_state_dict_resumes_iteration(ex_iterable)
    assert_load_state_dict_resumes_arrow_iteration(ex_iterable)


@pytest.mark.parametrize(
    "n, func, batched, batch_size, remove_columns",
    [
        (
            3,
            lambda t: t.append_column("id+1", pc.add(t["id"], 1)),
            False,
            None,
            ["extra_column"],
        ),  # just add 1 to the id
        (25, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), True, 10, ["extra_column"]),  # same with bs=10
        (
            50,
            lambda t: pa.table({"foo": ["bar"] * np.random.default_rng(t["id"][0].as_py()).integers(0, 10)}),
            True,
            8,
            ["extra_column", "id"],
        ),  # make a duplicate of each example
        (5, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), True, None, ["extra_column"]),  # same with bs=None
        (5, lambda t: t.append_column("id+1", pc.add(t["id"], 1)), True, -1, ["extra_column"]),  # same with bs<=0
    ],
)
def test_mapped_examples_iterable_remove_columns_arrow_format(n, func, batched, batch_size, remove_columns):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n, "extra_column": "foo"})
    base_ex_iterable = RebatchedArrowExamplesIterable(base_ex_iterable, batch_size=batch_size if batched else 1)
    ex_iterable = MappedExamplesIterable(
        base_ex_iterable,
        func,
        batched=batched,
        batch_size=batch_size,
        remove_columns=remove_columns,
        formatting=FormattingConfig(format_type="arrow"),
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    columns_to_remove = remove_columns if isinstance(remove_columns, list) else [remove_columns]
    if batched is False:
        expected = [
            {**{k: v for k, v in func(pa.Table.from_pylist([x])).to_pylist()[0].items() if k not in columns_to_remove}}
            for x in all_examples
        ]
    else:
        expected = []
        # If batch_size is None or <=0, we use the whole dataset as a single batch
        if batch_size is None or batch_size <= 0:
            batch_size = len(all_examples)
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            batch = pa.Table.from_pylist(examples)
            expected.extend(
                [{k: v for k, v in x.items() if k not in columns_to_remove} for x in func(batch).to_pylist()]
            )
    assert next(iter(ex_iterable))[1] == expected[0]
    assert [x for _, x in ex_iterable] == expected
    assert_load_state_dict_resumes_iteration(ex_iterable)
    assert_load_state_dict_resumes_arrow_iteration(ex_iterable)


@pytest.mark.parametrize(
    "n, func, batched, batch_size, fn_kwargs",
    [
        (3, lambda t, y=0: t.append_column("id+idx", pc.add(t["id"], y)), False, None, None),
        (3, lambda t, y=0: t.append_column("id+idx", pc.add(t["id"], y)), False, None, {"y": 3}),
        (25, lambda t, y=0: t.append_column("id+idx", pc.add(t["id"], y)), True, 10, {"y": 3}),
        (5, lambda t, y=0: t.append_column("id+idx", pc.add(t["id"], y)), True, None, {"y": 3}),  # same with bs=None
        (5, lambda t, y=0: t.append_column("id+idx", pc.add(t["id"], y)), True, -1, {"y": 3}),  # same with bs<=0
    ],
)
def test_mapped_examples_iterable_fn_kwargs_and_arrow_format(n, func, batched, batch_size, fn_kwargs):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    base_ex_iterable = RebatchedArrowExamplesIterable(base_ex_iterable, batch_size=batch_size if batched else 1)
    ex_iterable = MappedExamplesIterable(
        base_ex_iterable,
        func,
        batched=batched,
        batch_size=batch_size,
        fn_kwargs=fn_kwargs,
        formatting=FormattingConfig(format_type="arrow"),
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    if fn_kwargs is None:
        fn_kwargs = {}
    if batched is False:
        expected = [func(pa.Table.from_pylist([x]), **fn_kwargs).to_pylist()[0] for x in all_examples]
    else:
        expected = []
        # If batch_size is None or <=0, we use the whole dataset as a single batch
        if batch_size is None or batch_size <= 0:
            batch_size = len(all_examples)
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            batch = pa.Table.from_pylist(examples)
            expected.extend(func(batch, **fn_kwargs).to_pylist())
    assert next(iter(ex_iterable))[1] == expected[0]
    assert [x for _, x in ex_iterable] == expected
    assert_load_state_dict_resumes_iteration(ex_iterable)
    assert_load_state_dict_resumes_arrow_iteration(ex_iterable)


@pytest.mark.parametrize(
    "n, func, batched, batch_size, input_columns",
    [
        (3, lambda id_: pa.table({"id+1": pc.add(id_, 1)}), False, None, ["id"]),  # just add 1 to the id
        (25, lambda ids_: pa.table({"id+1": pc.add(ids_, 1)}), True, 10, ["id"]),  # same with bs=10
        (5, lambda ids_: pa.table({"id+1": pc.add(ids_, 1)}), True, None, ["id"]),  # same with bs=None
        (5, lambda ids_: pa.table({"id+1": pc.add(ids_, 1)}), True, -1, ["id"]),  # same with bs<=0
    ],
)
def test_mapped_examples_iterable_input_columns_and_arrow_format(n, func, batched, batch_size, input_columns):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    base_ex_iterable = RebatchedArrowExamplesIterable(base_ex_iterable, batch_size=batch_size if batched else 1)
    ex_iterable = MappedExamplesIterable(
        base_ex_iterable,
        func,
        batched=batched,
        batch_size=batch_size,
        input_columns=input_columns,
        formatting=FormattingConfig(format_type="arrow"),
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    columns_to_input = input_columns if isinstance(input_columns, list) else [input_columns]
    if batched is False:
        expected = [
            func(*[pa.Table.from_pylist([x])[col] for col in columns_to_input]).to_pylist()[0] for x in all_examples
        ]
    else:
        expected = []
        # If batch_size is None or <=0, we use the whole dataset as a single batch
        if batch_size is None or batch_size <= 0:
            batch_size = len(all_examples)
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            batch = pa.Table.from_pylist(examples)
            expected.extend(func(*[batch[col] for col in columns_to_input]).to_pylist())
    assert next(iter(ex_iterable))[1] == expected[0]
    assert [x for _, x in ex_iterable] == expected
    assert_load_state_dict_resumes_iteration(ex_iterable)
    assert_load_state_dict_resumes_arrow_iteration(ex_iterable)


@pytest.mark.parametrize(
    "n, func, batched, batch_size",
    [
        (3, lambda x: x["id"] % 2 == 0, False, None),  # keep even number
        (3, lambda x: [x["id"][0] % 2 == 0], True, 1),  # same with bs=1
        (25, lambda x: [i % 2 == 0 for i in x["id"]], True, 10),  # same with bs=10
        (5, lambda x: [i % 2 == 0 for i in x["id"]], True, None),  # same with bs=None
        (5, lambda x: [i % 2 == 0 for i in x["id"]], True, -1),  # same with bs<=0
        (3, lambda x: False, False, None),  # return 0 examples
        (3, lambda x: [False] * len(x["id"]), True, 10),  # same with bs=10
    ],
)
def test_filtered_examples_iterable(n, func, batched, batch_size):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    ex_iterable = FilteredExamplesIterable(base_ex_iterable, func, batched=batched, batch_size=batch_size)
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    if batched is False:
        expected = [x for x in all_examples if func(x)]
    else:
        # For batched filter we have to format the examples as a batch (i.e. in one single dictionary) to pass the batch to the function
        expected = []
        # If batch_size is None or <=0, we use the whole dataset as a single batch
        if batch_size is None or batch_size <= 0:
            batch_size = len(all_examples)
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            batch = _examples_to_batch(examples)
            mask = func(batch)
            expected.extend([x for x, to_keep in zip(examples, mask) if to_keep])
    if expected:
        assert next(iter(ex_iterable))[1] == expected[0]
    assert [x for _, x in ex_iterable] == expected
    assert_load_state_dict_resumes_iteration(ex_iterable)


@pytest.mark.parametrize(
    "n, func, batched, batch_size",
    [
        (3, lambda x, index: index % 2 == 0, False, None),  # keep even number
        (25, lambda x, indices: [idx % 2 == 0 for idx in indices], True, 10),  # same with bs=10
        (5, lambda x, indices: [idx % 2 == 0 for idx in indices], True, None),  # same with bs=None
        (5, lambda x, indices: [idx % 2 == 0 for idx in indices], True, -1),  # same with bs<=0
    ],
)
def test_filtered_examples_iterable_with_indices(n, func, batched, batch_size):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    ex_iterable = FilteredExamplesIterable(
        base_ex_iterable, func, batched=batched, batch_size=batch_size, with_indices=True
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    if batched is False:
        expected = [x for idx, x in enumerate(all_examples) if func(x, idx)]
    else:
        # For batched filter we have to format the examples as a batch (i.e. in one single dictionary) to pass the batch to the function
        expected = []
        # If batch_size is None or <=0, we use the whole dataset as a single batch
        if batch_size is None or batch_size <= 0:
            batch_size = len(all_examples)
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            batch = _examples_to_batch(examples)
            indices = list(range(batch_offset, batch_offset + len(examples)))
            mask = func(batch, indices)
            expected.extend([x for x, to_keep in zip(examples, mask) if to_keep])
    assert next(iter(ex_iterable))[1] == expected[0]
    assert [x for _, x in ex_iterable] == expected
    assert_load_state_dict_resumes_iteration(ex_iterable)


@pytest.mark.parametrize(
    "n, func, batched, batch_size, input_columns",
    [
        (3, lambda id_: id_ % 2 == 0, False, None, ["id"]),  # keep even number
        (25, lambda ids_: [i % 2 == 0 for i in ids_], True, 10, ["id"]),  # same with bs=10
        (3, lambda ids_: [i % 2 == 0 for i in ids_], True, None, ["id"]),  # same with bs=None
        (3, lambda ids_: [i % 2 == 0 for i in ids_], True, None, ["id"]),  # same with bs=None
    ],
)
def test_filtered_examples_iterable_input_columns(n, func, batched, batch_size, input_columns):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    ex_iterable = FilteredExamplesIterable(
        base_ex_iterable, func, batched=batched, batch_size=batch_size, input_columns=input_columns
    )
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    columns_to_input = input_columns if isinstance(input_columns, list) else [input_columns]
    if batched is False:
        expected = [x for x in all_examples if func(*[x[col] for col in columns_to_input])]
    else:
        # For batched filter we have to format the examples as a batch (i.e. in one single dictionary) to pass the batch to the function
        expected = []
        # If batch_size is None or <=0, we use the whole dataset as a single batch
        if batch_size is None or batch_size <= 0:
            batch_size = len(all_examples)
        for batch_offset in range(0, len(all_examples), batch_size):
            examples = all_examples[batch_offset : batch_offset + batch_size]
            batch = _examples_to_batch(examples)
            mask = func(*[batch[col] for col in columns_to_input])
            expected.extend([x for x, to_keep in zip(examples, mask) if to_keep])
    assert next(iter(ex_iterable))[1] == expected[0]
    assert [x for _, x in ex_iterable] == expected
    assert_load_state_dict_resumes_iteration(ex_iterable)


def test_map_async():
    dset = Dataset.from_dict({"x": range(100)}).to_iterable_dataset()

    async def f(example):
        await asyncio.sleep(0.1)
        return {"y": 1}

    _start = time.time()
    out = dset.map(f)
    assert time.time() - _start < 2.0
    assert next(iter(out))["y"] == 1

    async def f(batch):
        await asyncio.sleep(0.1)
        return {"y": [1] * len(batch["x"])}

    _start = time.time()
    out = dset.map(f, batched=True)
    assert time.time() - _start < 2.0
    assert next(iter(out))["y"] == 1


def test_filter_async():
    dset = Dataset.from_dict({"x": range(100)}).to_iterable_dataset()

    async def f(example):
        await asyncio.sleep(0.1)
        return example["x"] == 42

    _start = time.time()
    out = dset.filter(f)
    assert time.time() - _start < 2.0
    assert len(list(out)) == 1

    async def f(batch):
        await asyncio.sleep(0.1)
        return [x == 42 for x in batch["x"]]

    _start = time.time()
    out = dset.filter(f, batched=True)
    assert time.time() - _start < 2.0
    assert len(list(out)) == 1


def test_skip_examples_iterable():
    total, count = 10, 2
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": total})
    skip_ex_iterable = SkipExamplesIterable(base_ex_iterable, n=count)
    expected = list(generate_examples_fn(n=total))[count:]
    assert list(skip_ex_iterable) == expected
    assert skip_ex_iterable.shuffle_data_sources(np.random.default_rng(42)) is skip_ex_iterable, (
        "skip examples makes the shards order fixed"
    )
    assert_load_state_dict_resumes_iteration(skip_ex_iterable)


def test_take_examples_iterable():
    total, count = 10, 2
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": total})
    take_ex_iterable = TakeExamplesIterable(base_ex_iterable, n=count)
    expected = list(generate_examples_fn(n=total))[:count]
    assert list(take_ex_iterable) == expected
    assert take_ex_iterable.shuffle_data_sources(np.random.default_rng(42)) is take_ex_iterable, (
        "skip examples makes the shards order fixed"
    )
    assert_load_state_dict_resumes_iteration(take_ex_iterable)


@pytest.mark.parametrize(
    "n, num_times",
    [
        (3, None),
        (3, 3),
        (3, 0),
    ],
)
def test_repeat_examples_iterable(n, num_times):
    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    ex_iterable = RepeatExamplesIterable(base_ex_iterable, num_times=num_times)
    all_examples = [x for _, x in generate_examples_fn(n=n)]
    if num_times is not None:
        expected = all_examples * max(num_times, 0)
        assert [x for _, x in ex_iterable] == expected
    else:
        max_iters = 135
        iterator = iter(ex_iterable)
        for i in range(max_iters):
            assert next(iterator)[1] == all_examples[i % len(all_examples)], f"iteration {i} failed,"


def test_vertically_concatenated_examples_iterable():
    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"label": 10})
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {"label": 5})
    concatenated_ex_iterable = VerticallyConcatenatedMultiSourcesExamplesIterable([ex_iterable1, ex_iterable2])
    expected = [x for _, x in ex_iterable1] + [x for _, x in ex_iterable2]
    assert [x for _, x in concatenated_ex_iterable] == expected
    assert_load_state_dict_resumes_iteration(concatenated_ex_iterable)


def test_vertically_concatenated_examples_iterable_with_different_columns():
    # having different columns is supported
    # Though iterable datasets fill the missing data with nulls
    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"label": 10})
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {})
    concatenated_ex_iterable = VerticallyConcatenatedMultiSourcesExamplesIterable([ex_iterable1, ex_iterable2])
    expected = [x for _, x in ex_iterable1] + [x for _, x in ex_iterable2]
    assert [x for _, x in concatenated_ex_iterable] == expected
    assert_load_state_dict_resumes_iteration(concatenated_ex_iterable)


def test_vertically_concatenated_examples_iterable_shuffle_data_sources():
    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"label": 10})
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {"label": 5})
    concatenated_ex_iterable = VerticallyConcatenatedMultiSourcesExamplesIterable([ex_iterable1, ex_iterable2])
    rng = np.random.default_rng(42)
    shuffled_ex_iterable = concatenated_ex_iterable.shuffle_data_sources(rng)
    # make sure the list of examples iterables is shuffled, and each examples iterable is shuffled
    expected = [x for _, x in ex_iterable2.shuffle_data_sources(rng)] + [
        x for _, x in ex_iterable1.shuffle_data_sources(rng)
    ]
    assert [x for _, x in shuffled_ex_iterable] == expected
    assert_load_state_dict_resumes_iteration(shuffled_ex_iterable)


def test_horizontally_concatenated_examples_iterable():
    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"label1": 10})
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {"label2": 5})
    concatenated_ex_iterable = HorizontallyConcatenatedMultiSourcesExamplesIterable([ex_iterable1, ex_iterable2])
    with pytest.raises(ValueError):  # column "id" is duplicated -> raise an error
        list(concatenated_ex_iterable)
    ex_iterable2 = MappedExamplesIterable(ex_iterable2, lambda x: x, remove_columns=["id"])
    concatenated_ex_iterable = HorizontallyConcatenatedMultiSourcesExamplesIterable([ex_iterable1, ex_iterable2])
    expected = [{**x, **y} for (_, x), (_, y) in zip(ex_iterable1, ex_iterable2)]
    assert [x for _, x in concatenated_ex_iterable] == expected
    assert concatenated_ex_iterable.shuffle_data_sources(np.random.default_rng(42)) is concatenated_ex_iterable, (
        "horizontally concatenated examples makes the shards order fixed"
    )
    assert_load_state_dict_resumes_iteration(concatenated_ex_iterable)


@pytest.mark.parametrize(
    "ex_iterable",
    [
        ExamplesIterable(generate_examples_fn, {}),
        ShuffledDataSourcesExamplesIterable(generate_examples_fn, {}, np.random.default_rng(42)),
        SelectColumnsIterable(ExamplesIterable(generate_examples_fn, {}), ["id"]),
        StepExamplesIterable(ExamplesIterable(generate_examples_fn, {}), 2, 0),
        CyclingMultiSourcesExamplesIterable([ExamplesIterable(generate_examples_fn, {})]),
        VerticallyConcatenatedMultiSourcesExamplesIterable([ExamplesIterable(generate_examples_fn, {})]),
        HorizontallyConcatenatedMultiSourcesExamplesIterable([ExamplesIterable(generate_examples_fn, {})]),
        RandomlyCyclingMultiSourcesExamplesIterable(
            [ExamplesIterable(generate_examples_fn, {})], np.random.default_rng(42)
        ),
        MappedExamplesIterable(ExamplesIterable(generate_examples_fn, {}), lambda x: x),
        MappedExamplesIterable(ArrowExamplesIterable(generate_tables_fn, {}), lambda x: x),
        FilteredExamplesIterable(ExamplesIterable(generate_examples_fn, {}), lambda x: True),
        FilteredExamplesIterable(ArrowExamplesIterable(generate_tables_fn, {}), lambda x: True),
        BufferShuffledExamplesIterable(ExamplesIterable(generate_examples_fn, {}), 10, np.random.default_rng(42)),
        SkipExamplesIterable(ExamplesIterable(generate_examples_fn, {}), 10),
        TakeExamplesIterable(ExamplesIterable(generate_examples_fn, {}), 10),
        FormattedExamplesIterable(
            ExamplesIterable(generate_examples_fn, {}), None, Features({"id": Value("int32")}), token_per_repo_id={}
        ),
    ],
)
def test_no_iter_arrow(ex_iterable: _BaseExamplesIterable):
    assert ex_iterable.iter_arrow is None
    if not isinstance(ex_iterable, BufferShuffledExamplesIterable):
        assert_load_state_dict_resumes_iteration(ex_iterable)


@pytest.mark.parametrize(
    "ex_iterable",
    [
        ArrowExamplesIterable(generate_tables_fn, {}),
        ShuffledDataSourcesArrowExamplesIterable(generate_tables_fn, {}, np.random.default_rng(42)),
        SelectColumnsIterable(ArrowExamplesIterable(generate_tables_fn, {}), ["id"]),
        # StepExamplesIterable(ArrowExamplesIterable(generate_tables_fn, {}), 2, 0),  # not implemented
        # CyclingMultiSourcesExamplesIterable([ArrowExamplesIterable(generate_tables_fn, {})]),  # not implemented
        VerticallyConcatenatedMultiSourcesExamplesIterable([ArrowExamplesIterable(generate_tables_fn, {})]),
        # HorizontallyConcatenatedMultiSourcesExamplesIterable([ArrowExamplesIterable(generate_tables_fn, {})]),  # not implemented
        # RandomlyCyclingMultiSourcesExamplesIterable([ArrowExamplesIterable(generate_tables_fn, {})], np.random.default_rng(42)),  # not implemented
        MappedExamplesIterable(
            RebatchedArrowExamplesIterable(ExamplesIterable(generate_examples_fn, {}), batch_size=1),
            lambda t: t,
            formatting=FormattingConfig(format_type="arrow"),
        ),
        MappedExamplesIterable(
            RebatchedArrowExamplesIterable(ArrowExamplesIterable(generate_tables_fn, {}), batch_size=1),
            lambda t: t,
            formatting=FormattingConfig(format_type="arrow"),
        ),
        FilteredExamplesIterable(
            RebatchedArrowExamplesIterable(ExamplesIterable(generate_examples_fn, {}), batch_size=1),
            lambda t: True,
            formatting=FormattingConfig(format_type="arrow"),
        ),
        FilteredExamplesIterable(
            RebatchedArrowExamplesIterable(ArrowExamplesIterable(generate_tables_fn, {}), batch_size=1),
            lambda t: True,
            formatting=FormattingConfig(format_type="arrow"),
        ),
        # BufferShuffledExamplesIterable(ArrowExamplesIterable(generate_tables_fn, {}), 10, np.random.default_rng(42)),  # not implemented
        # SkipExamplesIterable(ArrowExamplesIterable(generate_tables_fn, {}), 10),  # not implemented
        # TakeExamplesIterable(ArrowExamplesIterable(generate_tables_fn, {}), 10),  # not implemented
        FormattedExamplesIterable(
            ArrowExamplesIterable(generate_tables_fn, {}), None, Features({"id": Value("int32")}), token_per_repo_id={}
        ),
    ],
)
def test_iter_arrow(ex_iterable: _BaseExamplesIterable):
    assert ex_iterable.iter_arrow is not None
    key, pa_table = next(ex_iterable.iter_arrow())
    assert isinstance(pa_table, pa.Table)
    assert_load_state_dict_resumes_arrow_iteration(ex_iterable)


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


def test_iterable_dataset_from_generator():
    data = [
        {"col_1": "0", "col_2": 0, "col_3": 0.0},
        {"col_1": "1", "col_2": 1, "col_3": 1.0},
        {"col_1": "2", "col_2": 2, "col_3": 2.0},
        {"col_1": "3", "col_2": 3, "col_3": 3.0},
    ]

    def gen():
        yield from data

    dataset = IterableDataset.from_generator(gen)
    assert isinstance(dataset, IterableDataset)
    assert list(dataset) == data


def test_iterable_dataset_from_generator_with_shards():
    def gen(shard_names):
        for shard_name in shard_names:
            for i in range(10):
                yield {"shard_name": shard_name, "i": i}

    shard_names = [f"data{shard_idx}.txt" for shard_idx in range(4)]
    dataset = IterableDataset.from_generator(gen, gen_kwargs={"shard_names": shard_names})
    assert isinstance(dataset, IterableDataset)
    assert dataset.num_shards == len(shard_names)


@require_numpy1_on_windows
def test_iterable_dataset_from_file(dataset: IterableDataset, arrow_file: str):
    with assert_arrow_memory_doesnt_increase():
        dataset_from_file = IterableDataset.from_file(arrow_file)
    expected_features = dataset._resolve_features().features
    assert dataset_from_file.features.type == expected_features.type
    assert dataset_from_file.features == expected_features
    assert isinstance(dataset_from_file, IterableDataset)
    assert list(dataset_from_file) == list(dataset)


@require_not_windows
@require_dill_gt_0_3_2
@require_pyspark
def test_from_spark_streaming():
    import pyspark

    spark = pyspark.sql.SparkSession.builder.master("local[*]").appName("pyspark").getOrCreate()
    data = [
        ("0", 0, 0.0),
        ("1", 1, 1.0),
        ("2", 2, 2.0),
        ("3", 3, 3.0),
    ]
    df = spark.createDataFrame(data, "col_1: string, col_2: int, col_3: float")
    dataset = IterableDataset.from_spark(df)
    assert isinstance(dataset, IterableDataset)
    results = []
    for ex in dataset:
        results.append(ex)
    assert results == [
        {"col_1": "0", "col_2": 0, "col_3": 0.0},
        {"col_1": "1", "col_2": 1, "col_3": 1.0},
        {"col_1": "2", "col_2": 2, "col_3": 2.0},
        {"col_1": "3", "col_2": 3, "col_3": 3.0},
    ]


@require_not_windows
@require_dill_gt_0_3_2
@require_pyspark
def test_from_spark_streaming_features():
    import PIL.Image
    import pyspark

    spark = pyspark.sql.SparkSession.builder.master("local[*]").appName("pyspark").getOrCreate()
    data = [(0, np.arange(4 * 4 * 3).reshape(4, 4, 3).tolist())]
    df = spark.createDataFrame(data, "idx: int, image: array<array<array<int>>>")
    features = Features({"idx": Value("int64"), "image": Image()})
    dataset = IterableDataset.from_spark(
        df,
        features=features,
    )
    assert isinstance(dataset, IterableDataset)
    results = []
    for ex in dataset:
        results.append(ex)
    assert len(results) == 1
    isinstance(results[0]["image"], PIL.Image.Image)


@require_torch
def test_iterable_dataset_torch_integration():
    ex_iterable = ExamplesIterable(generate_examples_fn, {})
    dataset = IterableDataset(ex_iterable)
    import torch.utils.data

    assert isinstance(dataset, torch.utils.data.IterableDataset)
    assert isinstance(dataset, IterableDataset)


@require_torch
def test_iterable_dataset_torch_picklable():
    import pickle

    ex_iterable = ExamplesIterable(generate_examples_fn, {})
    dataset = IterableDataset(ex_iterable, formatting=FormattingConfig(format_type="torch"))
    reloaded_dataset = pickle.loads(pickle.dumps(dataset))

    import torch.utils.data

    assert isinstance(reloaded_dataset, IterableDataset)
    assert isinstance(reloaded_dataset, torch.utils.data.IterableDataset)
    assert reloaded_dataset._formatting.format_type == "torch"
    assert len(list(dataset)) == len(list(reloaded_dataset))


@require_torch
def test_iterable_dataset_with_format_torch():
    ex_iterable = ExamplesIterable(generate_examples_fn, {})
    dataset = IterableDataset(ex_iterable)
    from torch.utils.data import DataLoader

    dataloader = DataLoader(dataset)
    assert len(list(dataloader)) == len(list(ex_iterable))


@require_torch
def test_iterable_dataset_torch_dataloader_parallel():
    from torch.utils.data import DataLoader

    ex_iterable = ExamplesIterable(generate_examples_fn, {})
    dataset = IterableDataset(ex_iterable)
    dataloader = DataLoader(dataset, num_workers=2, batch_size=None)
    result = list(dataloader)
    expected = [example for _, example in ex_iterable]
    assert len(result) == len(expected)
    assert {str(x) for x in result} == {str(x) for x in expected}


@require_torch
@pytest.mark.filterwarnings("ignore:This DataLoader will create:UserWarning")
@pytest.mark.parametrize("num_shards, num_workers", [(2, 1), (2, 2), (3, 2), (2, 3)])
def test_sharded_iterable_dataset_torch_dataloader_parallel(num_shards, num_workers):
    from torch.utils.data import DataLoader

    ex_iterable = ExamplesIterable(generate_examples_fn, {"filepaths": [f"{i}.txt" for i in range(num_shards)]})
    dataset = IterableDataset(ex_iterable)
    dataloader = DataLoader(dataset, batch_size=None, num_workers=num_workers)
    result = list(dataloader)
    expected = [example for _, example in ex_iterable]
    assert len(result) == len(expected)
    assert {str(x) for x in result} == {str(x) for x in expected}


@require_torch
@pytest.mark.integration
@pytest.mark.parametrize("num_workers", [1, 2])
def test_iterable_dataset_from_hub_torch_dataloader_parallel(num_workers, tmp_path):
    from torch.utils.data import DataLoader

    dataset = load_dataset(SAMPLE_DATASET_IDENTIFIER, cache_dir=str(tmp_path), streaming=True, split="train")
    dataloader = DataLoader(dataset, batch_size=None, num_workers=num_workers)
    result = list(dataloader)
    assert len(result) == 2


@pytest.mark.parametrize("batch_size", [4, 5])
@pytest.mark.parametrize("drop_last_batch", [False, True])
def test_iterable_dataset_iter_batch(batch_size, drop_last_batch):
    n = 25
    dataset = IterableDataset(ExamplesIterable(generate_examples_fn, {"n": n}))
    all_examples = [ex for _, ex in generate_examples_fn(n=n)]
    expected = []
    for i in range(0, len(all_examples), batch_size):
        if len(all_examples[i : i + batch_size]) < batch_size and drop_last_batch:
            continue
        expected.append(_examples_to_batch(all_examples[i : i + batch_size]))
    assert next(iter(dataset.iter(batch_size, drop_last_batch=drop_last_batch))) == expected[0]
    assert list(dataset.iter(batch_size, drop_last_batch=drop_last_batch)) == expected


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


def test_iterable_dataset_set_epoch_resuming(dataset: IterableDataset):
    dataset_length = len(list(dataset))
    assert len(list(dataset)) == dataset_length > 0
    dataset.load_state_dict(dataset.state_dict())
    assert len(list(dataset)) == 0
    dataset.set_epoch(1)
    assert len(list(dataset)) == dataset_length > 0
    dataset.load_state_dict(dataset.state_dict())
    assert len(list(dataset)) == 0


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


def test_iterable_dataset_map_with_features(dataset: IterableDataset) -> None:
    # https://github.com/huggingface/datasets/issues/3888
    ex_iterable = ExamplesIterable(generate_examples_fn, {"label": "positive"})
    features_before_map = Features(
        {
            "id": Value("int64"),
            "label": Value("string"),
        }
    )
    dataset = IterableDataset(ex_iterable, info=DatasetInfo(features=features_before_map))
    assert dataset.info.features is not None
    assert dataset.info.features == features_before_map
    features_after_map = Features(
        {
            "id": Value("int64"),
            "label": Value("string"),
            "target": Value("string"),
        }
    )
    dataset = dataset.map(lambda x: {"target": x["label"]}, features=features_after_map)
    assert dataset.info.features is not None
    assert dataset.info.features == features_after_map


def test_iterable_dataset_map_with_fn_kwargs(dataset: IterableDataset) -> None:
    fn_kwargs = {"y": 1}
    mapped_dataset = dataset.map(lambda x, y: {"id+y": x["id"] + y}, fn_kwargs=fn_kwargs)
    assert mapped_dataset._ex_iterable.batched is False
    assert next(iter(mapped_dataset)) == {"id": 0, "id+y": 1}
    batch_size = 3
    mapped_dataset = dataset.map(
        lambda x, y: {"id+y": [i + y for i in x["id"]]}, batched=True, batch_size=batch_size, fn_kwargs=fn_kwargs
    )
    assert isinstance(mapped_dataset._ex_iterable, MappedExamplesIterable)
    assert mapped_dataset._ex_iterable.batch_size == batch_size
    assert next(iter(mapped_dataset)) == {"id": 0, "id+y": 1}


def test_iterable_dataset_filter(dataset: IterableDataset) -> None:
    fn_kwargs = {"y": 1}
    filtered_dataset = dataset.filter(lambda x, y: x["id"] == y, fn_kwargs=fn_kwargs)
    assert filtered_dataset._ex_iterable.batched is False
    assert next(iter(filtered_dataset)) == {"id": 1}


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
@require_tf
@require_jax
@pytest.mark.parametrize(
    "format_type", [None, "torch", "python", "tf", "tensorflow", "np", "numpy", "jax", "arrow", "pd", "pandas"]
)
def test_iterable_dataset_with_format(dataset: IterableDataset, format_type):
    formatted_dataset = dataset.with_format(format_type)
    assert formatted_dataset._formatting.format_type == get_format_type_from_alias(format_type)


@require_torch
def test_iterable_dataset_is_torch_iterable_dataset(dataset: IterableDataset):
    from torch.utils.data import DataLoader, _DatasetKind

    dataloader = DataLoader(dataset)
    assert dataloader._dataset_kind == _DatasetKind.Iterable
    out = list(dataloader)
    assert len(out) == DEFAULT_N_EXAMPLES


@require_torch
def test_iterable_dataset_persists_epoch_in_torch_workers(dataset: IterableDataset):
    from torch.utils.data import DataLoader

    dataset = dataset.shuffle(seed=42)
    dataloader = DataLoader(dataset, num_workers=1, persistent_workers=True)
    epoch0 = list(dataloader)
    assert list(dataloader) == epoch0
    dataset.set_epoch(1)
    assert list(dataloader) != epoch0

    # Make sure pickle works even with torch objects in shared memory
    dataset_copy: IterableDataset = pickle.loads(pickle.dumps(dataset))
    dataloader = DataLoader(dataset_copy, num_workers=1, persistent_workers=True)
    epoch1 = list(dataloader)
    assert list(dataloader) == epoch1
    dataset.set_epoch(2)  # this should not affect the copy
    assert list(dataloader) == epoch1
    dataset_copy.set_epoch(2)
    assert list(dataloader) != epoch1


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


@pytest.mark.parametrize("n", [0, 2])
def test_iterable_dataset_repeat(dataset: IterableDataset, n):
    repeat_dataset = dataset.repeat(n)
    assert isinstance(repeat_dataset._ex_iterable, RepeatExamplesIterable)
    assert repeat_dataset._ex_iterable.num_times == n
    assert list(repeat_dataset) == list(dataset) * n


def test_iterable_dataset_shard():
    num_examples = 20
    num_shards = 5
    dataset = Dataset.from_dict({"a": range(num_examples)}).to_iterable_dataset(num_shards=num_shards)
    assert sum(dataset.shard(num_shards, i).num_shards for i in range(num_shards)) == dataset.num_shards
    assert list(concatenate_datasets([dataset.shard(num_shards, i) for i in range(num_shards)])) == list(dataset)
    num_shards = 2
    assert sum(dataset.shard(num_shards, i).num_shards for i in range(num_shards)) == dataset.num_shards
    assert list(concatenate_datasets([dataset.shard(num_shards, i) for i in range(num_shards)])) == list(dataset)
    assert (
        sum(dataset.shard(num_shards, i, contiguous=False).num_shards for i in range(num_shards)) == dataset.num_shards
    )
    assert list(
        concatenate_datasets([dataset.shard(num_shards, i, contiguous=False) for i in range(num_shards)])
    ) != list(dataset)
    assert sorted(
        concatenate_datasets([dataset.shard(num_shards, i, contiguous=False) for i in range(num_shards)]),
        key=lambda x: x["a"],
    ) == list(dataset)


@pytest.mark.parametrize("method", ["skip", "take"])
@pytest.mark.parametrize("after_shuffle", [False, True])
@pytest.mark.parametrize("count", [2, 5, 11])
def test_iterable_dataset_skip_or_take_after_shuffle(method, after_shuffle, count):
    seed = 42
    n, num_shards = 3, 10
    ex_iterable = ExamplesIterable(
        generate_examples_fn, {"n": n, "filepaths": [f"{i}.txt" for i in range(num_shards)]}
    )
    dataset = IterableDataset(ex_iterable)
    shuffled_dataset = dataset
    if after_shuffle:
        shuffled_dataset = shuffled_dataset.shuffle(seed, buffer_size=DEFAULT_N_EXAMPLES)
        shuffled_dataset = shuffled_dataset.skip(count) if method == "skip" else shuffled_dataset.take(count)
        # skip/take a shuffled dataset should not keep the same examples and shuffle the shards
        key = lambda x: f"{x['filepath']}_{x['id']}"  # noqa: E731
        assert (len(list(dataset)) - count if method == "skip" else count) == len(list(shuffled_dataset))
        assert sorted(list(dataset)[count:] if method == "skip" else list(dataset)[:count], key=key) != sorted(
            shuffled_dataset, key=key
        )
    else:
        shuffled_dataset = shuffled_dataset.skip(count) if method == "skip" else shuffled_dataset.take(count)
        shuffled_dataset = shuffled_dataset.shuffle(seed, buffer_size=DEFAULT_N_EXAMPLES)
        # shuffling a skip/take dataset should keep the same examples and don't shuffle the shards
        key = lambda x: f"{x['filepath']}_{x['id']}"  # noqa: E731
        assert (len(list(dataset)) - count if method == "skip" else count) == len(list(shuffled_dataset))
        assert sorted(list(dataset)[count:] if method == "skip" else list(dataset)[:count], key=key) == sorted(
            shuffled_dataset, key=key
        )


@pytest.mark.parametrize("method", ["skip", "take"])
@pytest.mark.parametrize("after_split_by_node", [False, True])
@pytest.mark.parametrize("count", [2, 5, 11])
def test_iterable_dataset_skip_or_take_after_split_by_node(method, after_split_by_node, count):
    n, num_shards = 3, 10
    rank, world_size = 1, 2
    ex_iterable = ExamplesIterable(
        generate_examples_fn, {"n": n, "filepaths": [f"{i}.txt" for i in range(num_shards)]}
    )
    dataset = IterableDataset(ex_iterable)
    distributed_dataset = dataset
    true_distributed_dataset = split_dataset_by_node(dataset, rank=rank, world_size=world_size)
    if after_split_by_node:
        distributed_dataset = split_dataset_by_node(distributed_dataset, rank=rank, world_size=world_size)
        distributed_dataset = distributed_dataset.skip(count) if method == "skip" else distributed_dataset.take(count)
        assert (
            list(true_distributed_dataset)[count:]
            if method == "skip"
            else list(true_distributed_dataset)[:count] == list(distributed_dataset)
        )
    else:
        distributed_dataset = distributed_dataset.skip(count) if method == "skip" else distributed_dataset.take(count)
        distributed_dataset = split_dataset_by_node(distributed_dataset, rank=rank, world_size=world_size)
        assert len(
            list(true_distributed_dataset)[count // world_size :]
            if method == "skip"
            else list(true_distributed_dataset)[: count // world_size]
        ) == len(list(distributed_dataset))


def test_iterable_dataset_add_column(dataset_with_several_columns: IterableDataset):
    new_column = list(range(3 * DEFAULT_N_EXAMPLES))
    new_dataset = dataset_with_several_columns.add_column("new_column", new_column)
    assert list(new_dataset) == [
        {**example, "new_column": idx} for idx, example in enumerate(dataset_with_several_columns)
    ]
    new_dataset = new_dataset._resolve_features()
    assert "new_column" in new_dataset.column_names


def test_iterable_dataset_rename_column(dataset_with_several_columns: IterableDataset):
    new_dataset = dataset_with_several_columns.rename_column("id", "new_id")
    assert list(new_dataset) == [
        {("new_id" if k == "id" else k): v for k, v in example.items()} for example in dataset_with_several_columns
    ]
    assert new_dataset.features is None
    assert new_dataset.column_names is None
    # rename the column if ds.features was not None
    new_dataset = dataset_with_several_columns._resolve_features().rename_column("id", "new_id")
    assert new_dataset.features is not None
    assert new_dataset.column_names is not None
    assert "id" not in new_dataset.column_names
    assert "new_id" in new_dataset.column_names


def test_iterable_dataset_rename_columns(dataset_with_several_columns: IterableDataset):
    column_mapping = {"id": "new_id", "filepath": "filename"}
    new_dataset = dataset_with_several_columns.rename_columns(column_mapping)
    assert list(new_dataset) == [
        {column_mapping.get(k, k): v for k, v in example.items()} for example in dataset_with_several_columns
    ]
    assert new_dataset.features is None
    assert new_dataset.column_names is None
    # rename the columns if ds.features was not None
    new_dataset = dataset_with_several_columns._resolve_features().rename_columns(column_mapping)
    assert new_dataset.features is not None
    assert new_dataset.column_names is not None
    assert all(c not in new_dataset.column_names for c in ["id", "filepath"])
    assert all(c in new_dataset.column_names for c in ["new_id", "filename"])


def test_iterable_dataset_remove_columns(dataset_with_several_columns: IterableDataset):
    new_dataset = dataset_with_several_columns.remove_columns("id")
    assert list(new_dataset) == [
        {k: v for k, v in example.items() if k != "id"} for example in dataset_with_several_columns
    ]
    assert new_dataset.features is None
    new_dataset = dataset_with_several_columns.remove_columns(["id", "filepath"])
    assert list(new_dataset) == [
        {k: v for k, v in example.items() if k != "id" and k != "filepath"} for example in dataset_with_several_columns
    ]
    assert new_dataset.features is None
    assert new_dataset.column_names is None
    # remove the columns if ds.features was not None
    new_dataset = dataset_with_several_columns._resolve_features().remove_columns(["id", "filepath"])
    assert new_dataset.features is not None
    assert new_dataset.column_names is not None
    assert all(c not in new_dataset.features for c in ["id", "filepath"])
    assert all(c not in new_dataset.column_names for c in ["id", "filepath"])


def test_iterable_dataset_select_columns(dataset_with_several_columns: IterableDataset):
    new_dataset = dataset_with_several_columns.select_columns("id")
    assert list(new_dataset) == [
        {k: v for k, v in example.items() if k == "id"} for example in dataset_with_several_columns
    ]
    assert new_dataset.features is None
    new_dataset = dataset_with_several_columns.select_columns(["id", "filepath"])
    assert list(new_dataset) == [
        {k: v for k, v in example.items() if k in ("id", "filepath")} for example in dataset_with_several_columns
    ]
    assert new_dataset.features is None
    # select the columns if ds.features was not None
    new_dataset = dataset_with_several_columns._resolve_features().select_columns(["id", "filepath"])
    assert new_dataset.features is not None
    assert new_dataset.column_names is not None
    assert all(c in new_dataset.features for c in ["id", "filepath"])
    assert all(c in new_dataset.column_names for c in ["id", "filepath"])


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


def test_iterable_dataset_resolve_features():
    ex_iterable = ExamplesIterable(generate_examples_fn, {})
    dataset = IterableDataset(ex_iterable)
    assert dataset.features is None
    assert dataset.column_names is None
    dataset = dataset._resolve_features()
    assert dataset.features == Features(
        {
            "id": Value("int64"),
        }
    )
    assert dataset.column_names == ["id"]


def test_iterable_dataset_resolve_features_keep_order():
    def gen():
        yield from zip(range(3), [{"a": 1}, {"c": 1}, {"b": 1}])

    ex_iterable = ExamplesIterable(gen, {})
    dataset = IterableDataset(ex_iterable)._resolve_features()
    # columns appear in order of appearance in the dataset
    assert list(dataset.features) == ["a", "c", "b"]
    assert dataset.column_names == ["a", "c", "b"]


def test_iterable_dataset_with_features_fill_with_none():
    def gen():
        yield from zip(range(2), [{"a": 1}, {"b": 1}])

    ex_iterable = ExamplesIterable(gen, {})
    info = DatasetInfo(features=Features({"a": Value("int32"), "b": Value("int32")}))
    dataset = IterableDataset(ex_iterable, info=info)
    assert list(dataset) == [{"a": 1, "b": None}, {"b": 1, "a": None}]


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
    "probas, seed, expected_length, stopping_strategy",
    [
        (None, None, 3 * (DEFAULT_N_EXAMPLES - 1) + 1, "first_exhausted"),
        ([1, 0, 0], None, DEFAULT_N_EXAMPLES, "first_exhausted"),
        ([0, 1, 0], None, DEFAULT_N_EXAMPLES, "first_exhausted"),
        ([0.2, 0.5, 0.3], 42, None, "first_exhausted"),
        ([0.1, 0.1, 0.8], 1337, None, "first_exhausted"),
        ([0.5, 0.2, 0.3], 101010, None, "first_exhausted"),
        (None, None, 3 * DEFAULT_N_EXAMPLES, "all_exhausted"),
        ([0.2, 0.5, 0.3], 42, None, "all_exhausted"),
        ([0.1, 0.1, 0.8], 1337, None, "all_exhausted"),
        ([0.5, 0.2, 0.3], 101010, None, "all_exhausted"),
    ],
)
def test_interleave_datasets(dataset: IterableDataset, probas, seed, expected_length, stopping_strategy):
    d1 = dataset
    d2 = dataset.map(lambda x: {"id+1": x["id"] + 1, **x})
    d3 = dataset.with_format("python")
    datasets = [d1, d2, d3]

    merged_dataset = interleave_datasets(
        datasets, probabilities=probas, seed=seed, stopping_strategy=stopping_strategy
    )

    def fill_default(example):
        return {"id": None, "id+1": None, **example}

    # Check the examples iterable
    assert isinstance(
        merged_dataset._ex_iterable, (CyclingMultiSourcesExamplesIterable, RandomlyCyclingMultiSourcesExamplesIterable)
    )
    # Check that it is deterministic
    if seed is not None:
        merged_dataset2 = interleave_datasets(
            [d1, d2, d3], probabilities=probas, seed=seed, stopping_strategy=stopping_strategy
        )
        assert list(merged_dataset) == list(merged_dataset2)
    # Check features
    assert merged_dataset.features == Features({"id": Value("int64"), "id+1": Value("int64")})
    # Check first example
    if seed is not None:
        rng = np.random.default_rng(seed)
        i = next(iter(cycle(rng.choice(len(datasets), size=1000, p=probas))))
        assert next(iter(merged_dataset)) == fill_default(next(iter(datasets[i])))
    else:
        assert any(next(iter(merged_dataset)) == fill_default(next(iter(dataset))) for dataset in datasets)
    # Compute length it case it's random
    if expected_length is None:
        expected_length = 0
        counts = np.array([len(list(d)) for d in datasets])
        bool_strategy_func = np.all if stopping_strategy == "all_exhausted" else np.any
        rng = np.random.default_rng(seed)
        for i in cycle(rng.choice(len(datasets), size=1000, p=probas)):
            counts[i] -= 1
            expected_length += 1
            if bool_strategy_func(counts <= 0):
                break
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

    merged_dataset = interleave_datasets([dataset, dataset_with_features])
    assert merged_dataset.features == features


def test_interleave_datasets_with_oversampling():
    # Test hardcoded results
    d1 = IterableDataset(ExamplesIterable((lambda: (yield from [(i, {"a": i}) for i in [0, 1, 2]])), {}))
    d2 = IterableDataset(ExamplesIterable((lambda: (yield from [(i, {"a": i}) for i in [10, 11, 12, 13]])), {}))
    d3 = IterableDataset(ExamplesIterable((lambda: (yield from [(i, {"a": i}) for i in [20, 21, 22, 23, 24]])), {}))

    expected_values = [0, 10, 20, 1, 11, 21, 2, 12, 22, 0, 13, 23, 1, 10, 24]

    # Check oversampling strategy without probabilities
    assert [x["a"] for x in interleave_datasets([d1, d2, d3], stopping_strategy="all_exhausted")] == expected_values

    # Check oversampling strategy with probabilities
    expected_values = [20, 0, 21, 10, 1, 22, 23, 24, 2, 0, 1, 20, 11, 21, 2, 0, 12, 1, 22, 13]

    values = [
        x["a"]
        for x in interleave_datasets(
            [d1, d2, d3], probabilities=[0.5, 0.2, 0.3], seed=42, stopping_strategy="all_exhausted"
        )
    ]

    assert values == expected_values


@require_torch
def test_with_format_torch(dataset_with_several_columns: IterableDataset):
    import torch

    dset = dataset_with_several_columns.with_format(type="torch")
    example = next(iter(dset))
    batch = next(iter(dset.iter(batch_size=3)))
    assert len(example) == 3
    assert isinstance(example["id"], torch.Tensor)
    assert list(example["id"].shape) == []
    assert example["id"].item() == 0
    assert isinstance(batch["id"], torch.Tensor)
    assert isinstance(example["filepath"], list)
    assert isinstance(example["filepath"][0], str)
    assert example["filepath"][0] == "data0.txt"
    assert isinstance(batch["filepath"], list)
    assert isinstance(example["metadata"], dict)
    assert isinstance(example["metadata"]["sources"], list)
    assert isinstance(example["metadata"]["sources"][0], str)
    assert isinstance(batch["metadata"], list)


@require_tf
def test_with_format_tf(dataset_with_several_columns: IterableDataset):
    import tensorflow as tf

    dset = dataset_with_several_columns.with_format(type="tensorflow")
    example = next(iter(dset))
    batch = next(iter(dset.iter(batch_size=3)))
    assert isinstance(example["id"], tf.Tensor)
    assert list(example["id"].shape) == []
    assert example["id"].numpy().item() == 0
    assert isinstance(batch["id"], tf.Tensor)
    assert isinstance(example["filepath"], tf.Tensor)
    assert example["filepath"][0] == b"data0.txt"
    assert isinstance(batch["filepath"], tf.Tensor)
    assert isinstance(example["metadata"], dict)
    assert isinstance(example["metadata"]["sources"], tf.Tensor)
    assert isinstance(batch["metadata"], list)


def test_map_array_are_not_converted_back_to_lists(dataset: IterableDataset):
    def func(example):
        return {"array": np.array([1, 2, 3])}

    dset_test = dataset.map(func)
    example = next(iter(dset_test))
    # not aligned with Dataset.map because we don't convert back to lists after map()
    assert isinstance(example["array"], np.ndarray)


def test_formatted_map(dataset: IterableDataset):
    dataset = dataset.with_format("np")
    assert isinstance(next(dataset.iter(batch_size=3))["id"], np.ndarray)
    dataset = dataset.with_format(None)
    assert isinstance(next(dataset.iter(batch_size=3))["id"], list)

    def add_one_numpy(example):
        assert isinstance(example["id"], np.ndarray)
        return {"id": example["id"] + 1}

    dataset = dataset.with_format("np")
    dataset = dataset.map(add_one_numpy, batched=True)
    assert isinstance(next(dataset.iter(batch_size=3))["id"], np.ndarray)
    dataset = dataset.with_format(None)
    assert isinstance(next(dataset.iter(batch_size=3))["id"], list)


def test_format_from_arrow():
    python_arrow_extractor = Formatter.python_arrow_extractor
    numpy_arrow_extractor = Formatter.numpy_arrow_extractor

    with (
        patch.object(Formatter, "python_arrow_extractor") as mock_python_arrow_extractor,
        patch.object(Formatter, "numpy_arrow_extractor") as mock_numpy_arrow_extractor,
    ):
        mock_python_arrow_extractor.side_effect = python_arrow_extractor
        mock_numpy_arrow_extractor.side_effect = numpy_arrow_extractor

        def g():
            yield 0, pa.table({"a": range(10)})

        ds = IterableDataset(ArrowExamplesIterable(g, {}))
        ds = ds.with_format("np")
        ds = ds.map(lambda x: x, batched=True)
        next(iter(ds))

        # we do arrow -> numpy -> python
        mock_numpy_arrow_extractor.assert_called()
        # we don't do any arrow -> python
        mock_python_arrow_extractor.assert_not_called()


def test_format_arrow(dataset: IterableDataset):
    ds = dataset.with_format("arrow")
    assert isinstance(next(iter(ds)), pa.Table)
    assert isinstance(next(iter(ds.iter(batch_size=4))), pa.Table)
    assert len(next(iter(ds))) == 1
    assert len(next(iter(ds.iter(batch_size=4)))) == 4
    ds = ds.map(lambda t: t.append_column("new_col", pa.array([0] * len(t))))
    ds = ds.map(lambda t: t.append_column("new_col_batched", pa.array([1] * len(t))), batched=True)
    ds = ds.with_format(None)
    assert next(iter(ds)) == {**next(iter(dataset)), "new_col": 0, "new_col_batched": 1}


def test_format_pandas(dataset: IterableDataset):
    ds = dataset.with_format("pandas")
    assert isinstance(next(iter(ds)), pd.DataFrame)
    assert isinstance(next(iter(ds.iter(batch_size=4))), pd.DataFrame)
    assert len(next(iter(ds))) == 1
    assert len(next(iter(ds.iter(batch_size=4)))) == 4
    ds = ds.map(lambda df: df.assign(new_col=[0] * len(df)))
    ds = ds.map(lambda df: df.assign(new_col_batched=[1] * len(df)), batched=True)
    ds = ds.with_format(None)
    assert next(iter(ds)) == {**next(iter(dataset)), "new_col": 0, "new_col_batched": 1}


@require_polars
def test_format_polars(dataset: IterableDataset):
    import polars as pl

    ds = dataset.with_format("polars")
    assert isinstance(next(iter(ds)), pl.DataFrame)
    assert isinstance(next(iter(ds.iter(batch_size=4))), pl.DataFrame)
    assert len(next(iter(ds))) == 1
    assert len(next(iter(ds.iter(batch_size=4)))) == 4
    ds = ds.map(lambda df: df.with_columns(pl.Series([0] * len(df)).alias("new_col")))
    ds = ds.map(lambda df: df.with_columns(pl.Series([1] * len(df)).alias("new_col_batched")), batched=True)
    ds = ds.with_format(None)
    assert next(iter(ds)) == {**next(iter(dataset)), "new_col": 0, "new_col_batched": 1}


@pytest.mark.parametrize("num_shards1, num_shards2, num_workers", [(2, 1, 1), (2, 2, 2), (1, 3, 1), (4, 3, 3)])
def test_interleave_dataset_with_sharding(num_shards1, num_shards2, num_workers):
    from torch.utils.data import DataLoader

    ex_iterable1 = ExamplesIterable(generate_examples_fn, {"filepaths": [f"{i}-1.txt" for i in range(num_shards1)]})
    dataset1 = IterableDataset(ex_iterable1).with_format("torch")
    ex_iterable2 = ExamplesIterable(generate_examples_fn, {"filepaths": [f"{i}-2.txt" for i in range(num_shards2)]})
    dataset2 = IterableDataset(ex_iterable2).with_format("torch")

    dataset_merged = interleave_datasets([dataset1, dataset2], stopping_strategy="first_exhausted")
    assert dataset_merged.num_shards == min(num_shards1, num_shards2)
    dataloader = DataLoader(dataset_merged, batch_size=None, num_workers=num_workers)
    result = list(dataloader)
    expected_length = 2 * min(
        len([example for _, example in ex_iterable1]), len([example for _, example in ex_iterable2])
    )
    # some samples may be missing because the stopping strategy is applied per process
    assert expected_length - num_workers <= len(result) <= expected_length
    assert len(result) == len({str(x) for x in result})


def filter_func(batch):
    return batch["id"] == 4


def map_func(batch):
    batch["id"] *= 2
    return batch


def test_pickle_after_many_transforms(dataset_with_several_columns):
    dataset = dataset_with_several_columns
    dataset = dataset.remove_columns(["filepath"])
    dataset = dataset.take(5)
    dataset = dataset.map(map_func)
    dataset = dataset.shuffle()
    dataset = dataset.skip(1)
    dataset = dataset.filter(filter_func)
    dataset = dataset.add_column("additional_col", ["something"])
    dataset = dataset.rename_column("metadata", "metadata1")
    dataset = dataset.rename_columns({"id": "id1", "metadata1": "metadata2"})
    dataset = dataset.select_columns(["id1", "additional_col"])

    unpickled_dataset = pickle.loads(pickle.dumps(dataset))

    assert list(unpickled_dataset) == list(dataset)


@require_torchdata_stateful_dataloader
def test_resume_dataloader(dataset: IterableDataset):
    from torchdata.stateful_dataloader import StatefulDataLoader

    dl = StatefulDataLoader(dataset)
    remaining = []
    for i, x in enumerate(dl):
        if i == 2:
            state_dict = dl.state_dict()
        elif i > 2:
            remaining.append(x)
    dl = StatefulDataLoader(dataset)
    dl.load_state_dict(state_dict)
    assert remaining == list(dl)


def test_iterable_dataset_batch():
    # Create a simple IterableDataset
    data = [{"id": i, "text": f"Text {i}"} for i in range(10)]
    ds = IterableDataset.from_generator(lambda: (x for x in data))

    # Test with batch_size=3, drop_last_batch=False
    batched_ds = ds.batch(batch_size=3, drop_last_batch=False)
    batches = list(batched_ds)

    assert len(batches) == 4  # 3 full batches and 1 partial batch
    for i, batch in enumerate(batches[:3]):  # Check full batches
        assert len(batch["id"]) == 3
        assert len(batch["text"]) == 3
        assert batch["id"] == [3 * i, 3 * i + 1, 3 * i + 2]
        assert batch["text"] == [f"Text {3 * i}", f"Text {3 * i + 1}", f"Text {3 * i + 2}"]

    # Check last partial batch
    assert len(batches[3]["id"]) == 1
    assert len(batches[3]["text"]) == 1
    assert batches[3]["id"] == [9]
    assert batches[3]["text"] == ["Text 9"]

    # Test with batch_size=3, drop_last_batch=True
    batched_ds = ds.batch(batch_size=3, drop_last_batch=True)
    batches = list(batched_ds)

    assert len(batches) == 3  # Only full batches
    for i, batch in enumerate(batches):
        assert len(batch["id"]) == 3
        assert len(batch["text"]) == 3
        assert batch["id"] == [3 * i, 3 * i + 1, 3 * i + 2]
        assert batch["text"] == [f"Text {3 * i}", f"Text {3 * i + 1}", f"Text {3 * i + 2}"]

    # Test with batch_size=4 (doesn't evenly divide dataset size)
    batched_ds = ds.batch(batch_size=4, drop_last_batch=False)
    batches = list(batched_ds)

    assert len(batches) == 3  # 2 full batches and 1 partial batch
    for i, batch in enumerate(batches[:2]):  # Check full batches
        assert len(batch["id"]) == 4
        assert len(batch["text"]) == 4
        assert batch["id"] == [4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3]
        assert batch["text"] == [f"Text {4 * i}", f"Text {4 * i + 1}", f"Text {4 * i + 2}", f"Text {4 * i + 3}"]

    # Check last partial batch
    assert len(batches[2]["id"]) == 2
    assert len(batches[2]["text"]) == 2
    assert batches[2]["id"] == [8, 9]
    assert batches[2]["text"] == ["Text 8", "Text 9"]

    # Test with features
    batched_ds = ds._resolve_features().batch(batch_size=3)
    batches = list(batched_ds)

    assert batched_ds.features is not None
    assert len(batches) == 4  # 3 full batches and 1 partial batch
    for i, batch in enumerate(batches[:1]):
        assert len(batch["id"]) == 3
        assert len(batch["text"]) == 3
        assert batch["id"] == [3 * i, 3 * i + 1, 3 * i + 2]
        assert batch["text"] == [f"Text {3 * i}", f"Text {3 * i + 1}", f"Text {3 * i + 2}"]


@dataclass
class DecodableFeature:
    decode_example_num_calls = 0

    def __init__(self):
        self.decode = True

    def decode_example(self, example, token_per_repo_id=None):
        type(self).decode_example_num_calls += 1
        return "decoded" if self.decode else example

    def __call__(self):
        return pa.string()


def test_decode():
    data = [{"i": str(i)} for i in range(10)]
    features = Features({"i": DecodableFeature()})
    ds = IterableDataset.from_generator(lambda: (x for x in data), features=features)
    assert next(iter(ds)) == {"i": "decoded"}
    assert DecodableFeature.decode_example_num_calls == 1
    ds = ds.decode(False)
    assert next(iter(ds)) == {"i": "0"}
    assert DecodableFeature.decode_example_num_calls == 1
    ds = ds.decode(True)
    assert next(iter(ds)) == {"i": "decoded"}
    assert DecodableFeature.decode_example_num_calls == 2
    ds = ds.decode(num_threads=1)
    assert next(iter(ds)) == {"i": "decoded"}
    assert DecodableFeature.decode_example_num_calls == 4
