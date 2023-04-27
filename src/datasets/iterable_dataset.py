import copy
import itertools
import sys
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from itertools import cycle, islice
from typing import Any, Callable, Dict, Iterator, List, Optional, Union

import numpy as np
import pyarrow as pa

from . import config
from .arrow_dataset import DatasetInfoMixin
from .features import Features
from .features.features import FeatureType, _align_features, _check_if_features_can_be_aligned
from .filesystems import _reset_fsspec_lock
from .formatting import PythonFormatter, get_format_type_from_alias
from .info import DatasetInfo
from .splits import NamedSplit
from .table import table_cast
from .utils.logging import get_logger
from .utils.sharding import _merge_gen_kwargs, _number_of_shards_in_gen_kwargs, _shuffle_gen_kwargs, _split_gen_kwargs


logger = get_logger(__name__)


def _infer_features_from_batch(batch: Dict[str, list], try_features: Optional[Features] = None) -> Features:
    pa_table = pa.Table.from_pydict(batch)
    if try_features is not None:
        try:
            pa_table = table_cast(pa_table, pa.schema(try_features.type))
        except (TypeError, pa.ArrowInvalid, pa.ArrowNotImplementedError):
            pass
    return Features.from_arrow_schema(pa_table.schema)


def _examples_to_batch(examples: List[Dict[str, Any]]) -> Dict[str, list]:
    # we order the columns by order of appearance
    # to do so, we use a dict as an ordered set
    cols = {col: None for example in examples for col in example}
    # when an example is missing a column, we set the value to None with .get()
    arrays = [[example.get(col) for example in examples] for col in cols]
    return dict(zip(cols, arrays))


def _batch_to_examples(batch: Dict[str, list]) -> List[Dict[str, Any]]:
    """Convert a batch (dict of examples) to examples list"""
    n_examples = len(batch[next(iter(batch))])
    for i in range(n_examples):
        yield {col: array[i] for col, array in batch.items()}


class HasNextIterator(Iterator):
    """Iterator with an hasnext() function. Taken from https://stackoverflow.com/questions/1966591/has-next-in-python-iterators."""

    def __init__(self, it):
        self.it = iter(it)
        self._hasnext = None

    def __iter__(self):
        return self

    def __next__(self):
        if self._hasnext:
            result = self._thenext
        else:
            result = next(self.it)
        self._hasnext = None
        return result

    def hasnext(self):
        if self._hasnext is None:
            try:
                self._thenext = next(self.it)
            except StopIteration:
                self._hasnext = False
            else:
                self._hasnext = True
        return self._hasnext


class _BaseExamplesIterable:
    """Base class for the examples iterable used by an IterableDataset"""

    def __iter__(self):
        """An examples iterable should yield tuples (example_key, example) of type (int/str, dict)"""
        raise NotImplementedError(f"{type(self)} doesn't implement __iter__ yet")

    def shuffle_data_sources(self, generator: np.random.Generator) -> "_BaseExamplesIterable":
        """
        Either shuffle the shards/sources of the dataset, or propagate the shuffling to the underlying iterable.
        If the order of the shards must stay fixed (when using .skip or .take for example), then this method returns self.
        """
        raise NotImplementedError(f"{type(self)} doesn't implement shuffle_data_sources yet")

    def shard_data_sources(self, worker_id: int, num_workers: int) -> "_BaseExamplesIterable":
        """Either keep only the requested shard, or propagate the request to the underlying iterable."""
        raise NotImplementedError(f"{type(self)} doesn't implement shard_data_sources yet")

    def split_shard_indices_by_worker(self, worker_id: int, num_workers: int) -> List[int]:
        return list(range(worker_id, self.n_shards, num_workers))

    @property
    def n_shards(self) -> int:
        raise NotImplementedError(f"{type(self)} doesn't implement n_shards yet")


class ExamplesIterable(_BaseExamplesIterable):
    def __init__(self, generate_examples_fn: Callable, kwargs: dict):
        self.generate_examples_fn = generate_examples_fn
        self.kwargs = kwargs

    def __iter__(self):
        yield from self.generate_examples_fn(**self.kwargs)

    def shuffle_data_sources(self, generator: np.random.Generator) -> "ExamplesIterable":
        return ShuffledDataSourcesExamplesIterable(self.generate_examples_fn, self.kwargs, generator)

    def shard_data_sources(self, worker_id: int, num_workers: int) -> "ExamplesIterable":
        """Keep only the requested shard."""
        gen_kwargs_list = _split_gen_kwargs(self.kwargs, max_num_jobs=self.n_shards)
        shard_indices = self.split_shard_indices_by_worker(worker_id, num_workers)
        requested_gen_kwargs = _merge_gen_kwargs([gen_kwargs_list[i] for i in shard_indices])
        return ExamplesIterable(self.generate_examples_fn, requested_gen_kwargs)

    @property
    def n_shards(self) -> int:
        return _number_of_shards_in_gen_kwargs(self.kwargs)


class ShuffledDataSourcesExamplesIterable(ExamplesIterable):
    def __init__(self, generate_examples_fn: Callable, kwargs: dict, generator: np.random.Generator):
        super().__init__(generate_examples_fn, kwargs)
        self.generator = deepcopy(generator)

    def __iter__(self):
        """Shuffle the kwargs order to shuffle shards"""
        rng = deepcopy(self.generator)
        kwargs_with_shuffled_shards = _shuffle_gen_kwargs(rng, self.kwargs)
        yield from self.generate_examples_fn(**kwargs_with_shuffled_shards)

    def shard_data_sources(self, worker_id: int, num_workers: int) -> "ExamplesIterable":
        """Keep only the requested shard."""
        rng = deepcopy(self.generator)
        kwargs_with_shuffled_shards = _shuffle_gen_kwargs(rng, self.kwargs)
        return ExamplesIterable(self.generate_examples_fn, kwargs_with_shuffled_shards).shard_data_sources(
            worker_id, num_workers
        )


class SelectColumnsIterable(_BaseExamplesIterable):
    def __init__(self, ex_iterable: _BaseExamplesIterable, column_names: List[str]):
        self.ex_iterable = ex_iterable
        self.column_names = column_names

    def __iter__(self):
        for idx, row in self.ex_iterable:
            yield idx, {c: row[c] for c in self.column_names}

    def shuffle_data_sources(self, generator: np.random.Generator) -> "SelectColumnsIterable":
        return SelectColumnsIterable(self.ex_iterable.shuffle_data_sources(generator), self.column_names)

    def shard_data_sources(self, worker_id: int, num_workers: int) -> "SelectColumnsIterable":
        return SelectColumnsIterable(self.ex_iterable.shard_data_sources(worker_id, num_workers), self.column_names)

    @property
    def n_shards(self) -> int:
        return self.ex_iterable.n_shards


class StepExamplesIterable(_BaseExamplesIterable):
    def __init__(self, ex_iterable: _BaseExamplesIterable, step: int, offset: int):
        self.ex_iterable = ex_iterable
        self.step = step
        self.offset = offset

    def __iter__(self):
        ex_iterator = iter(self.ex_iterable)
        while True:
            batch = list(islice(ex_iterator, self.step))
            if len(batch) > self.offset:
                yield batch[self.offset]
            else:
                break

    def shuffle_data_sources(self, generator: np.random.Generator) -> "StepExamplesIterable":
        return StepExamplesIterable(
            self.ex_iterable.shuffle_data_sources(generator), step=self.step, offset=self.offset
        )

    def shard_data_sources(self, worker_id: int, num_workers: int) -> "StepExamplesIterable":
        return StepExamplesIterable(
            self.ex_iterable.shard_data_sources(worker_id, num_workers), step=self.step, offset=self.offset
        )

    @property
    def n_shards(self) -> int:
        return self.ex_iterable.n_shards


class CyclingMultiSourcesExamplesIterable(_BaseExamplesIterable):
    def __init__(
        self, ex_iterables: List[_BaseExamplesIterable], stopping_strategy: Optional[str] = "first_exhausted"
    ):
        self.ex_iterables = ex_iterables
        self.stopping_strategy = stopping_strategy

        # if undersampling ("first_exhausted"), we stop as soon as one dataset is exhausted
        # if oversampling ("all_exhausted"), we stop as soons as every dataset is exhausted, i.e as soon as every samples of every dataset has been visited at least once
        self.bool_strategy_func = np.all if (stopping_strategy == "all_exhausted") else np.any

    def _give_indice_iterator(self):
        # this is an infinite iterator to keep track of which iterator we want to pick examples from
        return cycle(range(len(self.ex_iterables)))

    def __iter__(self):
        iterators = [HasNextIterator(ex_iterable) for ex_iterable in self.ex_iterables]

        indices_iterator = self._give_indice_iterator()

        is_exhausted = np.full(len(self.ex_iterables), False)
        for i in indices_iterator:
            try:  # let's pick one example from the iterator at index i
                yield next(iterators[i])

                # it will resume from the yield at the next call so that we can directly test if the iterable is exhausted and if we need to break out of the loop
                if not iterators[i].hasnext():
                    is_exhausted[i] = True

                    if self.bool_strategy_func(is_exhausted):
                        # if the stopping criteria is met, break the main for loop
                        break
                    # otherwise reinitialise the iterator and yield the first example
                    iterators[i] = HasNextIterator(self.ex_iterables[i])

            except StopIteration:
                # here it means that the i-th iterabledataset is empty, i.e we never have the occasion to yield an element of the i-th dataset.
                # we still check if the stopping criteria is met and if we break out of the loop in case of an oversampling strategy
                is_exhausted[i] = True

                if self.bool_strategy_func(is_exhausted):
                    # if the stopping criteria is met, break the main for loop
                    break

    def shuffle_data_sources(self, generator: np.random.Generator) -> "CyclingMultiSourcesExamplesIterable":
        """Shuffle each underlying examples iterable."""
        ex_iterables = [ex_iterable.shuffle_data_sources(generator) for ex_iterable in self.ex_iterables]
        return CyclingMultiSourcesExamplesIterable(ex_iterables, self.stopping_strategy)

    @property
    def n_shards(self) -> int:
        return min(ex_iterable.n_shards for ex_iterable in self.ex_iterables)

    def shard_data_sources(self, worker_id: int, num_workers: int) -> "CyclingMultiSourcesExamplesIterable":
        """Either keep only the requested shard, or propagate the request to the underlying iterable."""
        return CyclingMultiSourcesExamplesIterable(
            [iterable.shard_data_sources(worker_id, num_workers) for iterable in self.ex_iterables],
            stopping_strategy=self.stopping_strategy,
        )


class VerticallyConcatenatedMultiSourcesExamplesIterable(_BaseExamplesIterable):
    """
    VerticallyConcatenatedMultiSourcesExamplesIterable simply chains the input iterables.
    It doesn't require the examples iterables to always yield the same columns.
    Instead, this is handled by the `IterableDataset` class or `TypedExamplesIterable`.

    For information, `IterableDataset` merges the features of all the datasets to concatenate into one.
    We use `IterableDataset._resolve_features` to obtain the features of all the datasets to concatenate.

    Then for each example, `IterableDataset` and `TypedExamplesIterable` automatically fill missing columns with None.
    This is done with `_apply_feature_types_on_example`.
    """

    def __init__(self, ex_iterables: List[_BaseExamplesIterable]):
        self.ex_iterables = ex_iterables

    def __iter__(self):
        for ex_iterable in self.ex_iterables:
            yield from ex_iterable

    def shuffle_data_sources(
        self, generator: np.random.Generator
    ) -> "VerticallyConcatenatedMultiSourcesExamplesIterable":
        """Shuffle the list of examples iterable, as well as each underlying examples iterable."""
        rng = deepcopy(generator)
        ex_iterables = list(self.ex_iterables)
        rng.shuffle(ex_iterables)
        ex_iterables = [ex_iterable.shuffle_data_sources(generator) for ex_iterable in ex_iterables]
        return VerticallyConcatenatedMultiSourcesExamplesIterable(ex_iterables)

    @property
    def n_shards(self) -> int:
        return min(ex_iterable.n_shards for ex_iterable in self.ex_iterables)

    def shard_data_sources(
        self, worker_id: int, num_workers: int
    ) -> "VerticallyConcatenatedMultiSourcesExamplesIterable":
        """Either keep only the requested shard, or propagate the request to the underlying iterable."""
        return VerticallyConcatenatedMultiSourcesExamplesIterable(
            [iterable.shard_data_sources(worker_id, num_workers) for iterable in self.ex_iterables]
        )


def _check_column_names(column_names: List[str]):
    """Check the column names to make sure they don't contain duplicates."""
    counter = Counter(column_names)
    if not all(count == 1 for count in counter.values()):
        duplicated_columns = [col for col in counter if counter[col] > 1]
        raise ValueError(
            f"The examples iterables can't have duplicated columns but columns {duplicated_columns} are duplicated."
        )


class HorizontallyConcatenatedMultiSourcesExamplesIterable(_BaseExamplesIterable):
    """
    HorizontallyConcatenatedMultiSourcesExamplesIterable merges examples together for the input list of iterables.
    It also checks that there are no duplicate columns (otherwise we don't know which one to keep).
    This check is done once when yielding the first example.

    However it doesn't fill missing columns with None.
    Instead, this is handled by the `IterableDataset` class or `TypedExamplesIterable`.

    For information, `IterableDataset` merges the features of all the datasets to concatenate into one.
    We use `IterableDataset._resolve_features` to obtain the features of all the datasets to concatenate.

    Then for each example, `IterableDataset` and `TypedExamplesIterable` automatically fill missing columns with None.
    This is done with `_apply_feature_types_on_example`.
    """

    def __init__(self, ex_iterables: List[_BaseExamplesIterable]):
        self.ex_iterables = ex_iterables

    def __iter__(self):
        ex_iterators = [iter(ex_iterable) for ex_iterable in self.ex_iterables]
        for i in itertools.count():
            keys = []
            examples = []
            for ex_iterator in list(ex_iterators):
                try:
                    key, example = next(ex_iterator)
                    keys.append(key)
                    examples.append(example)
                except StopIteration:
                    ex_iterators.remove(ex_iterator)
            if ex_iterators:
                if i == 0:
                    _check_column_names([column_name for example in examples for column_name in example])
                new_example = {}
                for example in examples:
                    new_example.update(example)
                new_key = "_".join(str(key) for key in keys)
                yield new_key, new_example
            else:
                break

    def shuffle_data_sources(
        self, generator: np.random.Generator
    ) -> "HorizontallyConcatenatedMultiSourcesExamplesIterable":
        """Doesn't shuffle the wrapped examples iterable since it would break the alignment between them."""
        return self

    @property
    def n_shards(self) -> int:
        return 1

    def shard_data_sources(
        self, worker_id: int, num_workers: int
    ) -> "HorizontallyConcatenatedMultiSourcesExamplesIterable":
        """Either keep only the requested shard, or propagate the request to the underlying iterable."""
        return HorizontallyConcatenatedMultiSourcesExamplesIterable(
            [iterable.shard_data_sources(worker_id, num_workers) for iterable in self.ex_iterables]
        )


class RandomlyCyclingMultiSourcesExamplesIterable(CyclingMultiSourcesExamplesIterable):
    def __init__(
        self,
        ex_iterables,
        generator: np.random.Generator,
        probabilities: Optional[List[float]] = None,
        stopping_strategy: Optional[str] = "first_exhausted",
    ):
        super().__init__(ex_iterables, stopping_strategy)
        self.generator = deepcopy(generator)
        self.probabilities = probabilities

    @staticmethod
    def _iter_random_indices(
        rng: np.random.Generator,
        num_sources: int,
        random_batch_size=1000,
        p: Optional[List[float]] = None,
    ) -> Iterator[int]:
        """Get an infinite iterator that randomly samples the index of the source to pick examples from."""
        if p is None:
            while True:
                yield from (int(i) for i in rng.integers(0, num_sources, size=random_batch_size))
        else:
            while True:
                yield from (int(i) for i in rng.choice(num_sources, size=random_batch_size, p=p))

    def _give_indice_iterator(self):
        rng = deepcopy(self.generator)
        # this is an infinite iterator that randomly samples the index of the source to pick examples from
        return self._iter_random_indices(rng, len(self.ex_iterables), p=self.probabilities)

    def shuffle_data_sources(self, generator: np.random.Generator) -> "RandomlyCyclingMultiSourcesExamplesIterable":
        """Shuffle the data sources of each wrapped examples iterable."""
        ex_iterables = [ex_iterable.shuffle_data_sources(generator) for ex_iterable in self.ex_iterables]
        return RandomlyCyclingMultiSourcesExamplesIterable(
            ex_iterables, generator=generator, probabilities=self.probabilities
        )

    def shard_data_sources(self, worker_id: int, num_workers: int) -> "RandomlyCyclingMultiSourcesExamplesIterable":
        """Either keep only the requested shard, or propagate the request to the underlying iterable."""
        return RandomlyCyclingMultiSourcesExamplesIterable(
            [iterable.shard_data_sources(worker_id, num_workers) for iterable in self.ex_iterables],
            self.generator,
            self.probabilities,
            self.stopping_strategy,
        )


class MappedExamplesIterable(_BaseExamplesIterable):
    def __init__(
        self,
        ex_iterable: _BaseExamplesIterable,
        function: Callable,
        with_indices: bool = False,
        input_columns: Optional[List[str]] = None,
        batched: bool = False,
        batch_size: Optional[int] = 1000,
        drop_last_batch: bool = False,
        remove_columns: Optional[List[str]] = None,
        fn_kwargs: Optional[dict] = None,
    ):
        self.ex_iterable = ex_iterable
        self.function = function
        self.batched = batched
        self.batch_size = batch_size
        self.drop_last_batch = drop_last_batch
        self.remove_columns = remove_columns
        self.with_indices = with_indices
        self.input_columns = input_columns
        self.fn_kwargs = fn_kwargs or {}

    def __iter__(self):
        iterator = iter(self.ex_iterable)
        current_idx = 0
        if self.batched:
            for key, example in iterator:
                # If `batched`, first build the batch, if `batch_size` is None or <=0, then the batch is the whole dataset
                iterator_batch = (
                    iterator
                    if self.batch_size is None or self.batch_size <= 0
                    else islice(iterator, self.batch_size - 1)
                )
                key_examples_list = [(key, example)] + [(key, example) for key, example in iterator_batch]
                keys, examples = zip(*key_examples_list)
                if (
                    self.drop_last_batch
                    and self.batch_size is not None
                    and self.batch_size > 0
                    and len(examples) < self.batch_size
                ):  # ignore last batch
                    return
                batch = _examples_to_batch(examples)
                # then apply the transform
                inputs = batch
                function_args = [inputs] if self.input_columns is None else [inputs[col] for col in self.input_columns]
                if self.with_indices:
                    function_args.append([current_idx + i for i in range(len(key_examples_list))])
                transformed_batch = dict(batch)  # this will be updated with the function output
                transformed_batch.update(self.function(*function_args, **self.fn_kwargs))
                # then remove the unwanted columns
                if self.remove_columns:
                    for c in self.remove_columns:
                        del transformed_batch[c]
                if transformed_batch:
                    first_col = next(iter(transformed_batch))
                    bad_cols = [
                        col
                        for col in transformed_batch
                        if len(transformed_batch[col]) != len(transformed_batch[first_col])
                    ]
                    if bad_cols:
                        raise ValueError(
                            f"Column lengths mismatch: columns {bad_cols} have length {[len(transformed_batch[col]) for col in bad_cols]} while {first_col} has length {len(transformed_batch[first_col])}."
                        )
                # the new key is the concatenation of the examples keys from the batch
                new_key = "_".join(str(key) for key in keys)
                # yield one example at a time from the transformed batch
                for batch_idx, example in enumerate(_batch_to_examples(transformed_batch)):
                    yield new_key, example
                current_idx += batch_idx + 1
        else:
            for key, example in iterator:
                # If not batched, we can apply the transform and yield the example directly
                # first copy the example, since we might drop some keys
                example = dict(example)
                # then apply the transform
                inputs = example
                function_args = [inputs] if self.input_columns is None else [inputs[col] for col in self.input_columns]
                if self.with_indices:
                    function_args.append(current_idx)
                transformed_example = dict(example)  # this will be updated with the function output
                transformed_example.update(self.function(*function_args, **self.fn_kwargs))
                # then we remove the unwanted columns
                if self.remove_columns:
                    for c in self.remove_columns:
                        del transformed_example[c]
                yield key, transformed_example
                current_idx += 1

    def shuffle_data_sources(self, generator: np.random.Generator) -> "MappedExamplesIterable":
        """Shuffle the wrapped examples iterable."""
        return MappedExamplesIterable(
            self.ex_iterable.shuffle_data_sources(generator),
            function=self.function,
            with_indices=self.with_indices,
            input_columns=self.input_columns,
            batched=self.batched,
            batch_size=self.batch_size,
            remove_columns=self.remove_columns,
            fn_kwargs=self.fn_kwargs,
        )

    def shard_data_sources(self, worker_id: int, num_workers: int) -> "MappedExamplesIterable":
        """Keep only the requested shard."""
        return MappedExamplesIterable(
            self.ex_iterable.shard_data_sources(worker_id, num_workers),
            function=self.function,
            with_indices=self.with_indices,
            input_columns=self.input_columns,
            batched=self.batched,
            batch_size=self.batch_size,
            remove_columns=self.remove_columns,
            fn_kwargs=self.fn_kwargs,
        )

    @property
    def n_shards(self) -> int:
        return self.ex_iterable.n_shards


class FilteredExamplesIterable(_BaseExamplesIterable):
    def __init__(
        self,
        ex_iterable: _BaseExamplesIterable,
        function: Callable,
        with_indices: bool = False,
        input_columns: Optional[List[str]] = None,
        batched: bool = False,
        batch_size: Optional[int] = 1000,
    ):
        self.ex_iterable = ex_iterable
        self.function = function
        self.batched = batched
        self.batch_size = batch_size
        self.with_indices = with_indices
        self.input_columns = input_columns

    def __iter__(self):
        iterator = iter(self.ex_iterable)
        current_idx = 0
        if self.batched:
            for key, example in iterator:
                # If `batched`, first build the batch, if `batch_size` is None or <=0, then the batch is the whole dataset
                iterator_batch = (
                    iterator
                    if self.batch_size is None or self.batch_size <= 0
                    else islice(iterator, self.batch_size - 1)
                )
                key_examples_list = [(key, example)] + [(key, example) for key, example in iterator_batch]
                keys, examples = zip(*key_examples_list)
                batch = _examples_to_batch(examples)
                # then compute the mask for the batch
                inputs = batch
                function_args = [inputs] if self.input_columns is None else [inputs[col] for col in self.input_columns]
                if self.with_indices:
                    function_args.append([current_idx + i for i in range(len(key_examples_list))])
                mask = self.function(*function_args)
                # yield one example at a time from the batch
                for batch_idx, (key_example, to_keep) in enumerate(zip(key_examples_list, mask)):
                    if to_keep:
                        yield key_example
                current_idx += batch_idx + 1
        else:
            for key, example in iterator:
                # If not batched, we can apply the filtering function direcly
                inputs = dict(example)
                function_args = [inputs] if self.input_columns is None else [inputs[col] for col in self.input_columns]
                if self.with_indices:
                    function_args.append(current_idx)
                to_keep = self.function(*function_args)
                if to_keep:
                    yield key, example
                current_idx += 1

    def shuffle_data_sources(self, seed: Optional[int]) -> "FilteredExamplesIterable":
        """Shuffle the wrapped examples iterable."""
        return FilteredExamplesIterable(
            self.ex_iterable.shuffle_data_sources(seed),
            function=self.function,
            with_indices=self.with_indices,
            input_columns=self.input_columns,
            batched=self.batched,
            batch_size=self.batch_size,
        )

    def shard_data_sources(self, worker_id: int, num_workers: int) -> "FilteredExamplesIterable":
        """Keep only the requested shard."""
        return FilteredExamplesIterable(
            self.ex_iterable.shard_data_sources(worker_id, num_workers),
            function=self.function,
            with_indices=self.with_indices,
            input_columns=self.input_columns,
            batched=self.batched,
            batch_size=self.batch_size,
        )

    @property
    def n_shards(self) -> int:
        return self.ex_iterable.n_shards


class BufferShuffledExamplesIterable(_BaseExamplesIterable):
    def __init__(self, ex_iterable: _BaseExamplesIterable, buffer_size: int, generator: np.random.Generator):
        self.ex_iterable = ex_iterable
        self.buffer_size = buffer_size
        self.generator = generator

    @staticmethod
    def _iter_random_indices(rng: np.random.Generator, buffer_size: int, random_batch_size=1000) -> Iterator[int]:
        while True:
            yield from (int(i) for i in rng.integers(0, buffer_size, size=random_batch_size))

    def __iter__(self):
        buffer_size = self.buffer_size
        rng = deepcopy(self.generator)
        indices_iterator = self._iter_random_indices(rng, buffer_size)
        # this is the shuffle buffer that we keep in memory
        mem_buffer = []
        for x in self.ex_iterable:
            if len(mem_buffer) == buffer_size:  # if the buffer is full, pick and example from it
                i = next(indices_iterator)
                yield mem_buffer[i]
                mem_buffer[i] = x  # replace the picked example by a new one
            else:  # otherwise, keep filling the buffer
                mem_buffer.append(x)
        # when we run out of examples, we shuffle the remaining examples in the buffer and yield them
        rng.shuffle(mem_buffer)
        yield from mem_buffer

    def shuffle_data_sources(self, generator: np.random.Generator) -> "BufferShuffledExamplesIterable":
        """Shuffle the wrapped examples iterable as well as the shuffling buffer."""
        return BufferShuffledExamplesIterable(
            self.ex_iterable.shuffle_data_sources(generator), buffer_size=self.buffer_size, generator=generator
        )

    def shard_data_sources(self, worker_id: int, num_workers: int) -> "BufferShuffledExamplesIterable":
        """Keep only the requested shard."""
        return BufferShuffledExamplesIterable(
            self.ex_iterable.shard_data_sources(worker_id, num_workers),
            buffer_size=self.buffer_size,
            generator=self.generator,
        )

    @property
    def n_shards(self) -> int:
        return self.ex_iterable.n_shards


class SkipExamplesIterable(_BaseExamplesIterable):
    def __init__(self, ex_iterable: _BaseExamplesIterable, n: int):
        self.ex_iterable = ex_iterable
        self.n = n

    def __iter__(self):
        yield from islice(self.ex_iterable, self.n, None)

    def shuffle_data_sources(self, generator: np.random.Generator) -> "SkipExamplesIterable":
        """Doesn't shuffle the wrapped examples iterable since it would skip examples from other shards instead."""
        return self

    @property
    def n_shards(self) -> int:
        return self.ex_iterable.n_shards


class TakeExamplesIterable(_BaseExamplesIterable):
    def __init__(self, ex_iterable: _BaseExamplesIterable, n: int):
        self.ex_iterable = ex_iterable
        self.n = n

    def __iter__(self):
        yield from islice(self.ex_iterable, self.n)

    def shuffle_data_sources(self, generator: np.random.Generator) -> "TakeExamplesIterable":
        """Doesn't shuffle the wrapped examples iterable since it would take examples from other shards instead."""
        return self

    @staticmethod
    def split_number(num, n):
        quotient = num // n
        remainder = num % n
        result = [quotient] * n
        for i in range(remainder):
            result[i] += 1
        return result

    def shard_data_sources(self, worker_id: int, num_workers: int) -> "TakeExamplesIterable":
        """Keep only the requested shard."""
        return TakeExamplesIterable(
            self.ex_iterable.shard_data_sources(worker_id, num_workers),
            n=self.split_number(self.n, num_workers)[worker_id],
        )

    @property
    def n_shards(self) -> int:
        return self.ex_iterable.n_shards


def _apply_feature_types_on_example(
    example: dict, features: Features, token_per_repo_id: Dict[str, Union[str, bool, None]]
) -> dict:
    example = dict(example)
    # add missing columns
    for column_name in features:
        if column_name not in example:
            example[column_name] = None
    # we encode the example for ClassLabel feature types for example
    encoded_example = features.encode_example(example)
    # Decode example for Audio feature, e.g.
    decoded_example = features.decode_example(encoded_example, token_per_repo_id=token_per_repo_id)
    return decoded_example


def _apply_feature_types_on_batch(
    batch: dict, features: Features, token_per_repo_id: Dict[str, Union[str, bool, None]]
) -> dict:
    batch = dict(batch)
    # add missing columns
    n_examples = len(batch[next(iter(batch))])
    for column_name in features:
        if column_name not in batch:
            batch[column_name] = [None] * n_examples
    # we encode the batch for ClassLabel feature types for example
    encoded_batch = features.encode_batch(batch)
    # Decode batch for Audio feature, e.g.
    decoded_batch = features.decode_batch(encoded_batch, token_per_repo_id=token_per_repo_id)
    return decoded_batch


class TypedExamplesIterable(_BaseExamplesIterable):
    def __init__(
        self,
        ex_iterable: _BaseExamplesIterable,
        features: Features,
        token_per_repo_id: Dict[str, Union[str, bool, None]],
    ):
        self.ex_iterable = ex_iterable
        self.features = features
        self.token_per_repo_id = token_per_repo_id

    def __iter__(self):
        # Then for each example, `TypedExamplesIterable` automatically fills missing columns with None.
        # This is done with `_apply_feature_types_on_example`.
        for key, example in self.ex_iterable:
            yield key, _apply_feature_types_on_example(
                example, self.features, token_per_repo_id=self.token_per_repo_id
            )

    def shuffle_data_sources(self, generator: np.random.Generator) -> "TypedExamplesIterable":
        """Shuffle the wrapped examples iterable."""
        return TypedExamplesIterable(
            self.ex_iterable.shuffle_data_sources(generator),
            features=self.features,
            token_per_repo_id=self.token_per_repo_id,
        )

    def shard_data_sources(self, worker_id: int, num_workers: int) -> "TypedExamplesIterable":
        """Keep only the requested shard."""
        return TypedExamplesIterable(
            self.ex_iterable.shard_data_sources(worker_id, num_workers),
            features=self.features,
            token_per_repo_id=self.token_per_repo_id,
        )

    @property
    def n_shards(self) -> int:
        return self.ex_iterable.n_shards


def _generate_examples_from_tables_wrapper(generate_tables_fn):
    def wrapper(**kwargs):
        python_formatter = PythonFormatter()
        for key, table in generate_tables_fn(**kwargs):
            batch = python_formatter.format_batch(table)
            for i, example in enumerate(_batch_to_examples(batch)):
                yield f"{key}_{i}", example

    return wrapper


@dataclass
class ShufflingConfig:
    generator: np.random.Generator
    _original_seed: Optional[int] = None


@dataclass
class DistributedConfig:
    rank: int
    world_size: int


def _maybe_add_torch_iterable_dataset_parent_class(cls):
    """Add torch.utils.data.IterableDataset as a parent class if 'torch' is available"""
    if config.TORCH_AVAILABLE:
        import torch.utils.data

        if torch.utils.data.IterableDataset not in cls.__bases__:
            cls.__bases__ += (torch.utils.data.IterableDataset,)


class IterableDataset(DatasetInfoMixin):
    """A Dataset backed by an iterable."""

    def __init__(
        self,
        ex_iterable: _BaseExamplesIterable,
        info: Optional[DatasetInfo] = None,
        split: Optional[NamedSplit] = None,
        format_type: Optional[str] = None,
        shuffling: Optional[ShufflingConfig] = None,
        distributed: Optional[DistributedConfig] = None,
        token_per_repo_id: Optional[Dict[str, Union[str, bool, None]]] = None,
    ):
        if distributed and distributed.world_size > 1 and shuffling and shuffling._original_seed is None:
            raise RuntimeError(
                "The dataset doesn't have a fixed random seed across nodes to shuffle and split the list of dataset shards by node. "
                "Please pass e.g. `seed=42` in `.shuffle()` to make all the nodes use the same seed. "
            )

        info = info.copy() if info is not None else DatasetInfo()
        DatasetInfoMixin.__init__(self, info=info, split=split)

        self._ex_iterable = ex_iterable
        self._format_type = format_type
        self._shuffling = shuffling
        self._distributed = distributed
        self._epoch = 0
        self._token_per_repo_id: Dict[str, Union[str, bool, None]] = token_per_repo_id or {}
        _maybe_add_torch_iterable_dataset_parent_class(self.__class__)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d
        # Re-add torch iterable dataset as a parent class, since dynamically added parent classes are not kept when pickling
        _maybe_add_torch_iterable_dataset_parent_class(self.__class__)

    def _head(self, n=5):
        return _examples_to_batch(list(self.take(n)))

    def _effective_generator(self):
        if self._shuffling and self._epoch == 0:
            return self._shuffling.generator
        elif self._shuffling:
            # Create effective seed using self._epoch (we subtract in order to avoir overflow in long_scalars)
            effective_seed = deepcopy(self._shuffling.generator).integers(0, 1 << 63) - self._epoch
            effective_seed = (1 << 63) + effective_seed if effective_seed < 0 else effective_seed
            return np.random.default_rng(effective_seed)
        else:
            raise ValueError("This dataset is not shuffled")

    @property
    def n_shards(self) -> int:
        if self._distributed and self._ex_iterable.n_shards % self._distributed.world_size == 0:
            return self._ex_iterable.n_shards // self._distributed.world_size
        return self._ex_iterable.n_shards

    def _iter_pytorch(self, ex_iterable: _BaseExamplesIterable):
        # fix for fsspec when using multiprocess
        _reset_fsspec_lock()
        # check if there aren't too many workers
        import torch.utils.data

        worker_info = torch.utils.data.get_worker_info()
        if self._is_main_process() and ex_iterable.n_shards < worker_info.num_workers:
            logger.warning(
                f"Too many dataloader workers: {worker_info.num_workers} (max is dataset.n_shards={ex_iterable.n_shards}). "
                f"Stopping {worker_info.num_workers - ex_iterable.n_shards} dataloader workers."
            )
            logger.warning(
                f"To parallelize data loading, we give each process some shards (or data sources) to process. "
                f"Therefore it's unnecessary to have a number of workers greater than dataset.n_shards={ex_iterable.n_shards}. "
                f"To enable more parallelism, please split the dataset in more files than {ex_iterable.n_shards}."
            )
        # split workload
        _log_prefix = f"node#{self._distributed.rank} " if self._distributed else ""
        shards_indices = self._ex_iterable.split_shard_indices_by_worker(worker_info.id, worker_info.num_workers)
        if shards_indices:
            logger.debug(
                f"{_log_prefix}dataloader worker#{worker_info.id}, ': Starting to iterate over {len(shards_indices)}/{ex_iterable.n_shards} shards."
            )
            for key, example in ex_iterable.shard_data_sources(worker_info.id, worker_info.num_workers):
                if self.features:
                    yield _apply_feature_types_on_example(
                        example, self.features, token_per_repo_id=self._token_per_repo_id
                    )
                else:
                    yield example
            logger.debug(
                f"{_log_prefix}dataloader worker#{worker_info.id}, ': Finished iterating over {len(shards_indices)}/{ex_iterable.n_shards} shards."
            )
        else:
            logger.debug(
                f"{_log_prefix}dataloader worker#{worker_info.id}, ': Stopping... Number of dataset shards < num_workers ({ex_iterable.n_shards}<{worker_info.num_workers})."
            )

    def _is_main_process(self):
        if self._distributed and self._distributed.rank > 0:
            return False
        if "torch" in sys.modules:
            import torch.utils.data

            worker_info = torch.utils.data.get_worker_info()
            if worker_info is not None and worker_info.id > 0:
                return False
        return True

    def _prepare_ex_iterable_for_iteration(self) -> _BaseExamplesIterable:
        if self._shuffling:
            ex_iterable = self._ex_iterable.shuffle_data_sources(self._effective_generator())
        else:
            ex_iterable = self._ex_iterable

        if self._distributed:
            rank = self._distributed.rank
            world_size = self._distributed.world_size
            if ex_iterable.n_shards % world_size == 0:
                if self._is_main_process():
                    n_shards_per_node = ex_iterable.n_shards // world_size
                    plural = "s" if n_shards_per_node > 1 else ""
                    logger.warning(
                        f"Assigning {n_shards_per_node} shard{plural} (or data source{plural}) of the dataset to each node."
                    )
                ex_iterable = ex_iterable.shard_data_sources(rank, world_size)
            else:
                if self._is_main_process():
                    logger.warning(
                        f"Assigning 1 out of {world_size} examples of the dataset to each node. The others are skipped during the iteration."
                    )
                    logger.info(
                        f"It is more optimized to distribute the dataset shards (or data sources) across nodes. "
                        f"You can do that by using a dataset with number of shards that is a factor of world_size={world_size}. "
                        f"The current dataset has {ex_iterable.n_shards} which is not a factor of {world_size}"
                    )
                ex_iterable = StepExamplesIterable(ex_iterable, step=world_size, offset=rank)

        return ex_iterable

    def __iter__(self):
        ex_iterable = self._prepare_ex_iterable_for_iteration()

        if "torch" in sys.modules:
            import torch.utils.data

            worker_info = torch.utils.data.get_worker_info()
            if isinstance(self, torch.utils.data.IterableDataset) and worker_info is not None:
                # We're a torch.utils.data.IterableDataset in a PyTorch worker process
                yield from self._iter_pytorch(ex_iterable)
                return

        for key, example in ex_iterable:
            if self.features:
                # `IterableDataset` automatically fills missing columns with None.
                # This is done with `_apply_feature_types_on_example`.
                yield _apply_feature_types_on_example(
                    example, self.features, token_per_repo_id=self._token_per_repo_id
                )
            else:
                yield example

    def iter(self, batch_size: int, drop_last_batch: bool = False):
        """Iterate through the batches of size `batch_size`.

        Args:
            batch_size (:obj:`int`): size of each batch to yield.
            drop_last_batch (:obj:`bool`, default `False`): Whether a last batch smaller than the batch_size should be
                dropped
        """
        iterator = iter(self._prepare_ex_iterable_for_iteration())
        for key, example in iterator:
            # If batched, first build the batch
            examples = [example] + [example for key, example in islice(iterator, batch_size - 1)]
            if drop_last_batch and len(examples) < batch_size:  # ignore last batch
                return
            batch = _examples_to_batch(examples)
            if self.features:
                # `IterableDataset` automatically fills missing columns with None.
                # This is done with `_apply_feature_types_on_batch`.
                yield _apply_feature_types_on_batch(batch, self.features, token_per_repo_id=self._token_per_repo_id)
            else:
                yield batch

    @staticmethod
    def from_generator(
        generator: Callable,
        features: Optional[Features] = None,
        gen_kwargs: Optional[dict] = None,
    ) -> "IterableDataset":
        """Create an Iterable Dataset from a generator.

        Args:
            generator (`Callable`):
                A generator function that `yields` examples.
            features (`Features`, *optional*):
                Dataset features.
            gen_kwargs(`dict`, *optional*):
                Keyword arguments to be passed to the `generator` callable.
                You can define a sharded iterable dataset by passing the list of shards in `gen_kwargs`.
                This can be used to improve shuffling and when iterating over the dataset with multiple workers.

        Returns:
            `IterableDataset`

        Example:

        ```py
        >>> def gen():
        ...     yield {"text": "Good", "label": 0}
        ...     yield {"text": "Bad", "label": 1}
        ...
        >>> ds = IterableDataset.from_generator(gen)
        ```

        ```py
        >>> def gen(shards):
        ...     for shard in shards:
        ...         with open(shard) as f:
        ...             for line in f:
        ...                 yield {"line": line}
        ...
        >>> shards = [f"data{i}.txt" for i in range(32)]
        >>> ds = IterableDataset.from_generator(gen, gen_kwargs={"shards": shards})
        >>> ds = ds.shuffle(seed=42, buffer_size=10_000)  # shuffles the shards order + uses a shuffle buffer
        >>> from torch.utils.data import DataLoader
        >>> dataloader = DataLoader(ds.with_format("torch"), num_workers=4)  # give each worker a subset of 32/4=8 shards
        ```
        """
        from .io.generator import GeneratorDatasetInputStream

        return GeneratorDatasetInputStream(
            generator=generator,
            features=features,
            gen_kwargs=gen_kwargs,
            streaming=True,
        ).read()

    def with_format(
        self,
        type: Optional[str] = None,
    ) -> "IterableDataset":
        """
        Return a dataset with the specified format.
        This method only supports the "torch" format for now.

        Args:

            type (`str`, optional, default None): if set to "torch", the returned dataset
                will be a subclass of torch.utils.data.IterableDataset to be used in a DataLoader
        """
        type = get_format_type_from_alias(type)
        # TODO(QL): add examples formatting to get tensors when using the "torch" format
        # TODO(QL): add format_kwargs
        # TODO(QL): add format_columns and return_all_columns
        # TODO(QL): add pandas, numpy and tf formats
        return IterableDataset(
            ex_iterable=self._ex_iterable,
            info=self._info.copy(),
            split=self._split,
            format_type=type,
            shuffling=copy.deepcopy(self._shuffling),
            distributed=copy.deepcopy(self._distributed),
            token_per_repo_id=self._token_per_repo_id,
        )

    def map(
        self,
        function: Optional[Callable] = None,
        with_indices: bool = False,
        input_columns: Optional[Union[str, List[str]]] = None,
        batched: bool = False,
        batch_size: Optional[int] = 1000,
        drop_last_batch: bool = False,
        remove_columns: Optional[Union[str, List[str]]] = None,
        features: Optional[Features] = None,
        fn_kwargs: Optional[dict] = None,
    ) -> "IterableDataset":
        """
        Apply a function to all the examples in the iterable dataset (individually or in batches) and update them.
        If your function returns a column that already exists, then it overwrites it.
        The function is applied on-the-fly on the examples when iterating over the dataset.

        You can specify whether the function should be batched or not with the `batched` parameter:

        - If batched is `False`, then the function takes 1 example in and should return 1 example.
          An example is a dictionary, e.g. `{"text": "Hello there !"}`.
        - If batched is `True` and `batch_size` is 1, then the function takes a batch of 1 example as input and can return a batch with 1 or more examples.
          A batch is a dictionary, e.g. a batch of 1 example is {"text": ["Hello there !"]}.
        - If batched is `True` and `batch_size` is `n` > 1, then the function takes a batch of `n` examples as input and can return a batch with `n` examples, or with an arbitrary number of examples.
          Note that the last batch may have less than `n` examples.
          A batch is a dictionary, e.g. a batch of `n` examples is `{"text": ["Hello there !"] * n}`.

        Args:
            function (`Callable`, *optional*, defaults to `None`):
                Function applied on-the-fly on the examples when you iterate on the dataset.
                It must have one of the following signatures:

                - `function(example: Dict[str, Any]) -> Dict[str, Any]` if `batched=False` and `with_indices=False`
                - `function(example: Dict[str, Any], idx: int) -> Dict[str, Any]` if `batched=False` and `with_indices=True`
                - `function(batch: Dict[str, List]) -> Dict[str, List]` if `batched=True` and `with_indices=False`
                - `function(batch: Dict[str, List], indices: List[int]) -> Dict[str, List]` if `batched=True` and `with_indices=True`

                For advanced usage, the function can also return a `pyarrow.Table`.
                Moreover if your function returns nothing (`None`), then `map` will run your function and return the dataset unchanged.
                If no function is provided, default to identity function: `lambda x: x`.
            with_indices (`bool`, defaults to `False`):
                Provide example indices to `function`. Note that in this case the signature of `function` should be `def function(example, idx[, rank]): ...`.
            input_columns (`Optional[Union[str, List[str]]]`, defaults to `None`):
                The columns to be passed into `function`
                as positional arguments. If `None`, a dict mapping to all formatted columns is passed as one argument.
            batched (`bool`, defaults to `False`):
                Provide batch of examples to `function`.
            batch_size (`int`, *optional*, defaults to `1000`):
                Number of examples per batch provided to `function` if `batched=True`.
                `batch_size <= 0` or `batch_size == None` then provide the full dataset as a single batch to `function`.
            drop_last_batch (`bool`, defaults to `False`):
                Whether a last batch smaller than the batch_size should be
                dropped instead of being processed by the function.
            remove_columns (`[List[str]]`, *optional*, defaults to `None`):
                Remove a selection of columns while doing the mapping.
                Columns will be removed before updating the examples with the output of `function`, i.e. if `function` is adding
                columns with names in `remove_columns`, these columns will be kept.
            features (`[Features]`, *optional*, defaults to `None`):
                Feature types of the resulting dataset.
            fn_kwargs (`Dict`, *optional*, default `None`):
                Keyword arguments to be passed to `function`.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("rotten_tomatoes", split="train", streaming=True)
        >>> def add_prefix(example):
        ...     example["text"] = "Review: " + example["text"]
        ...     return example
        >>> ds = ds.map(add_prefix)
        >>> list(ds.take(3))
        [{'label': 1,
         'text': 'Review: the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .'},
         {'label': 1,
         'text': 'Review: the gorgeously elaborate continuation of " the lord of the rings " trilogy is so huge that a column of words cannot adequately describe co-writer/director peter jackson\'s expanded vision of j . r . r . tolkien\'s middle-earth .'},
         {'label': 1, 'text': 'Review: effective but too-tepid biopic'}]
        ```
        """
        if isinstance(input_columns, str):
            input_columns = [input_columns]
        if isinstance(remove_columns, str):
            remove_columns = [remove_columns]
        if function is None:
            function = lambda x: x  # noqa: E731
        if fn_kwargs is None:
            fn_kwargs = {}
        ex_iterable = MappedExamplesIterable(
            TypedExamplesIterable(self._ex_iterable, self._info.features, token_per_repo_id=self._token_per_repo_id)
            if self._info.features is not None
            else self._ex_iterable,
            function=function,
            with_indices=with_indices,
            input_columns=input_columns,
            batched=batched,
            batch_size=batch_size,
            drop_last_batch=drop_last_batch,
            remove_columns=remove_columns,
            fn_kwargs=fn_kwargs,
        )
        info = self.info.copy()
        info.features = features
        return IterableDataset(
            ex_iterable=ex_iterable,
            info=info,
            split=self._split,
            format_type=self._format_type,
            shuffling=copy.deepcopy(self._shuffling),
            distributed=copy.deepcopy(self._distributed),
            token_per_repo_id=self._token_per_repo_id,
        )

    def filter(
        self,
        function: Optional[Callable] = None,
        with_indices=False,
        input_columns: Optional[Union[str, List[str]]] = None,
        batched: bool = False,
        batch_size: Optional[int] = 1000,
    ) -> "IterableDataset":
        """Apply a filter function to all the elements so that the dataset only includes examples according to the filter function.
        The filtering is done on-the-fly when iterating over the dataset.

        Args:
            function (`Callable`):
                Callable with one of the following signatures:

                - `function(example: Dict[str, Any]) -> bool` if `with_indices=False, batched=False`
                - `function(example: Dict[str, Any], indices: int) -> bool` if `with_indices=True, batched=False`
                - `function(example: Dict[str, List]) -> List[bool]` if `with_indices=False, batched=True`
                - `function(example: Dict[str, List], indices: List[int]) -> List[bool]` if `with_indices=True, batched=True`

                If no function is provided, defaults to an always True function: `lambda x: True`.
            with_indices (`bool`, defaults to `False`):
                Provide example indices to `function`. Note that in this case the signature of `function` should be `def function(example, idx): ...`.
            input_columns (`str` or `List[str]`, *optional*):
                The columns to be passed into `function` as
                positional arguments. If `None`, a dict mapping to all formatted columns is passed as one argument.
            batched (`bool`, defaults to `False`):
                Provide batch of examples to `function`.
            batch_size (`int`, *optional*, default `1000`):
                Number of examples per batch provided to `function` if `batched=True`.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("rotten_tomatoes", split="train", streaming=True)
        >>> ds = ds.filter(lambda x: x["label"] == 0)
        >>> list(ds.take(3))
        [{'label': 0, 'movie_review': 'simplistic , silly and tedious .'},
         {'label': 0,
         'movie_review': "it's so laddish and juvenile , only teenage boys could possibly find it funny ."},
         {'label': 0,
         'movie_review': 'exploitative and largely devoid of the depth or sophistication that would make watching such a graphic treatment of the crimes bearable .'}]
        ```
        """
        if isinstance(input_columns, str):
            input_columns = [input_columns]

        # TODO(QL): keep the features (right now if we keep it it would call decode_example again on an already decoded example)
        info = copy.deepcopy(self._info)
        info.features = None

        # We need the examples to be decoded for certain feature types like Image or Audio, so we use TypedExamplesIterable here
        ex_iterable = FilteredExamplesIterable(
            TypedExamplesIterable(self._ex_iterable, self._info.features, token_per_repo_id=self._token_per_repo_id)
            if self._info.features is not None
            else self._ex_iterable,
            function=function,
            with_indices=with_indices,
            input_columns=input_columns,
            batched=batched,
            batch_size=batch_size,
        )
        return IterableDataset(
            ex_iterable=ex_iterable,
            info=info,
            split=self._split,
            format_type=self._format_type,
            shuffling=copy.deepcopy(self._shuffling),
            distributed=copy.deepcopy(self._distributed),
            token_per_repo_id=self._token_per_repo_id,
        )

    def shuffle(
        self, seed=None, generator: Optional[np.random.Generator] = None, buffer_size: int = 1000
    ) -> "IterableDataset":
        """
        Randomly shuffles the elements of this dataset.

        This dataset fills a buffer with `buffer_size` elements, then randomly samples elements from this buffer,
        replacing the selected elements with new elements. For perfect shuffling, a buffer size greater than or
        equal to the full size of the dataset is required.

        For instance, if your dataset contains 10,000 elements but `buffer_size` is set to 1000, then `shuffle` will
        initially select a random element from only the first 1000 elements in the buffer. Once an element is
        selected, its space in the buffer is replaced by the next (i.e. 1,001-st) element,
        maintaining the 1000 element buffer.

        If the dataset is made of several shards, it also does shuffle the order of the shards.
        However if the order has been fixed by using [`~datasets.IterableDataset.skip`] or [`~datasets.IterableDataset.take`]
        then the order of the shards is kept unchanged.

        Args:
            seed (`int`, *optional*, defaults to `None`):
                Random seed that will be used to shuffle the dataset.
                It is used to sample from the shuffle buffe and also to shuffle the data shards.
            generator (`numpy.random.Generator`, *optional*):
                Numpy random Generator to use to compute the permutation of the dataset rows.
                If `generator=None` (default), uses `np.random.default_rng` (the default BitGenerator (PCG64) of NumPy).
            buffer_size (`int`, defaults to `1000`):
                Size of the buffer.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("rotten_tomatoes", split="train", streaming=True)
        >>> list(ds.take(3))
        [{'label': 1,
         'text': 'the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .'},
         {'label': 1,
         'text': 'the gorgeously elaborate continuation of " the lord of the rings " trilogy is so huge that a column of words cannot adequately describe co-writer/director peter jackson\'s expanded vision of j . r . r . tolkien\'s middle-earth .'},
         {'label': 1, 'text': 'effective but too-tepid biopic'}]
        >>> shuffled_ds = ds.shuffle(seed=42)
        >>> list(shuffled_ds.take(3))
        [{'label': 1,
         'text': "a sports movie with action that's exciting on the field and a story you care about off it ."},
         {'label': 1,
         'text': 'at its best , the good girl is a refreshingly adult take on adultery . . .'},
         {'label': 1,
         'text': "sam jones became a very lucky filmmaker the day wilco got dropped from their record label , proving that one man's ruin may be another's fortune ."}]
        ```
        """
        if generator is None:
            generator = np.random.default_rng(seed)
        else:
            generator = deepcopy(generator)
        shuffling = ShufflingConfig(generator=generator, _original_seed=seed)
        return IterableDataset(
            ex_iterable=BufferShuffledExamplesIterable(
                self._ex_iterable, buffer_size=buffer_size, generator=generator
            ).shuffle_data_sources(generator),
            info=self._info.copy(),
            split=self._split,
            format_type=self._format_type,
            shuffling=shuffling,
            distributed=copy.deepcopy(self._distributed),
            token_per_repo_id=self._token_per_repo_id,
        )

    def set_epoch(self, epoch: int):
        self._epoch = epoch

    def skip(self, n) -> "IterableDataset":
        """
        Create a new [`IterableDataset`] that skips the first `n` elements.

        Args:
            n (`int`):
                Number of elements to skip.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("rotten_tomatoes", split="train", streaming=True)
        >>> list(ds.take(3))
        [{'label': 1,
         'text': 'the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .'},
         {'label': 1,
         'text': 'the gorgeously elaborate continuation of " the lord of the rings " trilogy is so huge that a column of words cannot adequately describe co-writer/director peter jackson\'s expanded vision of j . r . r . tolkien\'s middle-earth .'},
         {'label': 1, 'text': 'effective but too-tepid biopic'}]
        >>> ds = ds.skip(1)
        >>> list(ds.take(3))
        [{'label': 1,
         'text': 'the gorgeously elaborate continuation of " the lord of the rings " trilogy is so huge that a column of words cannot adequately describe co-writer/director peter jackson\'s expanded vision of j . r . r . tolkien\'s middle-earth .'},
         {'label': 1, 'text': 'effective but too-tepid biopic'},
         {'label': 1,
         'text': 'if you sometimes like to go to the movies to have fun , wasabi is a good place to start .'}]
        ```
        """
        ex_iterable = SkipExamplesIterable(self._ex_iterable, n)
        return IterableDataset(
            ex_iterable=ex_iterable,
            info=self._info.copy(),
            split=self._split,
            format_type=self._format_type,
            shuffling=copy.deepcopy(self._shuffling),
            distributed=copy.deepcopy(self._distributed),
            token_per_repo_id=self._token_per_repo_id,
        )

    def take(self, n) -> "IterableDataset":
        """
        Create a new [`IterableDataset`] with only the first `n` elements.

        Args:
            n (`int`):
                Number of elements to take.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("rotten_tomatoes", split="train", streaming=True)
        >>> small_ds = ds.take(2)
        >>> list(small_ds)
        [{'label': 1,
         'text': 'the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .'},
         {'label': 1,
         'text': 'the gorgeously elaborate continuation of " the lord of the rings " trilogy is so huge that a column of words cannot adequately describe co-writer/director peter jackson\'s expanded vision of j . r . r . tolkien\'s middle-earth .'}]
        ```
        """
        ex_iterable = TakeExamplesIterable(self._ex_iterable, n)
        return IterableDataset(
            ex_iterable=ex_iterable,
            info=self._info.copy(),
            split=self._split,
            format_type=self._format_type,
            shuffling=copy.deepcopy(self._shuffling),
            distributed=copy.deepcopy(self._distributed),
            token_per_repo_id=self._token_per_repo_id,
        )

    @property
    def column_names(self) -> Optional[List[str]]:
        """Names of the columns in the dataset.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("rotten_tomatoes", split="validation", streaming=True)
        >>> ds.column_names
        ['text', 'label']
        ```
        """
        return list(self._info.features.keys()) if self._info.features is not None else None

    def add_column(self, name: str, column: Union[list, np.array]) -> "IterableDataset":
        """Add column to Dataset.

        Args:
            name (str): Column name.
            column (list or np.array): Column data to be added.

        Returns:
            `IterableDataset`
        """

        def add_column_fn(example, idx):
            if name in example:
                raise ValueError(f"Error when adding {name}: column {name} is already in the dataset.")
            return {name: column[idx]}

        return self.map(add_column_fn, with_indices=True)

    def rename_column(self, original_column_name: str, new_column_name: str) -> "IterableDataset":
        """
        Rename a column in the dataset, and move the features associated to the original column under the new column
        name.

        Args:
            original_column_name (`str`):
                Name of the column to rename.
            new_column_name (`str`):
                New name for the column.

        Returns:
            `IterableDataset`: A copy of the dataset with a renamed column.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("rotten_tomatoes", split="train", streaming=True)
        >>> next(iter(ds))
        {'label': 1,
         'text': 'the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .'}
        >>> ds = ds.rename_column("text", "movie_review")
        >>> next(iter(ds))
        {'label': 1,
         'movie_review': 'the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .'}
        ```
        """

        def rename_column_fn(example):
            if original_column_name not in example:
                raise ValueError(
                    f"Error when renaming {original_column_name} to {new_column_name}: column {original_column_name} is not in the dataset."
                )
            if new_column_name in example:
                raise ValueError(
                    f"Error when renaming {original_column_name} to {new_column_name}: column {new_column_name} is already in the dataset."
                )
            return {new_column_name: example[original_column_name]}

        original_features = self._info.features.copy() if self._info.features else None
        ds_iterable = self.map(rename_column_fn, remove_columns=[original_column_name])
        if original_features is not None:
            ds_iterable._info.features = Features(
                {
                    new_column_name if col == original_column_name else col: feature
                    for col, feature in original_features.items()
                }
            )
        return ds_iterable

    def rename_columns(self, column_mapping: Dict[str, str]) -> "IterableDataset":
        """
        Rename several columns in the dataset, and move the features associated to the original columns under
        the new column names.

        Args:
            column_mapping (`Dict[str, str]`): A mapping of columns to rename to their new names

        Returns:
            `IterableDataset`: A copy of the dataset with renamed columns
        """

        def rename_columns_fn(example):
            if any(col not in example for col in column_mapping):
                raise ValueError(
                    f"Error when renaming {list(column_mapping)} to {list(column_mapping.values())}: columns {set(column_mapping) - set(example)} are not in the dataset."
                )
            if any(col in example for col in column_mapping.values()):
                raise ValueError(
                    f"Error when renaming {list(column_mapping)} to {list(column_mapping.values())}: columns {set(example) - set(column_mapping.values())} are already in the dataset."
                )
            return {
                new_column_name: example[original_column_name]
                for original_column_name, new_column_name in column_mapping.items()
            }

        original_features = self._info.features.copy() if self._info.features else None
        ds_iterable = self.map(rename_columns_fn, remove_columns=list(column_mapping))
        if original_features is not None:
            ds_iterable._info.features = Features(
                {
                    column_mapping[col] if col in column_mapping.keys() else col: feature
                    for col, feature in original_features.items()
                }
            )
        return ds_iterable

    def remove_columns(self, column_names: Union[str, List[str]]) -> "IterableDataset":
        """
        Remove one or several column(s) in the dataset and the features associated to them.
        The removal is done on-the-fly on the examples when iterating over the dataset.


        Args:
            column_names (`Union[str, List[str]]`):
                Name of the column(s) to remove.

        Returns:
            `IterableDataset`: A copy of the dataset object without the columns to remove.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("rotten_tomatoes", split="train", streaming=True)
        >>> next(iter(ds))
        {'text': 'the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .', 'label': 1}
        >>> ds = ds.remove_columns("label")
        >>> next(iter(ds))
        {'text': 'the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .'}
        ```
        """
        original_features = self._info.features.copy() if self._info.features else None
        ds_iterable = self.map(remove_columns=column_names)
        if original_features is not None:
            ds_iterable._info.features = original_features.copy()
            for col, _ in original_features.items():
                if col in column_names:
                    del ds_iterable._info.features[col]
        return ds_iterable

    def select_columns(self, column_names: Union[str, List[str]]) -> "IterableDataset":
        """Select one or several column(s) in the dataset and the features
        associated to them. The selection is done on-the-fly on the examples
        when iterating over the dataset.


        Args:
            column_names (`Union[str, List[str]]`):
                Name of the column(s) to select.

        Returns:
            `IterableDataset`: A copy of the dataset object with selected columns.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("rotten_tomatoes", split="train", streaming=True)
        >>> next(iter(ds))
        {'text': 'the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .', 'label': 1}
        >>> ds = ds.select_columns("text")
        >>> next(iter(ds))
        {'text': 'the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .'}
        ```
        """
        if isinstance(column_names, str):
            column_names = [column_names]

        if self._info:
            info = copy.deepcopy(self._info)
            if self._info.features is not None:
                for column_name in column_names:
                    if column_name not in self._info.features:
                        raise ValueError(
                            f"Column name {column_name} not in the "
                            "dataset. Columns in the dataset: "
                            f"{list(self._info.features.keys())}."
                        )
                info.features = Features({c: info.features[c] for c in column_names})

        ex_iterable = SelectColumnsIterable(self._ex_iterable, column_names)
        return IterableDataset(
            ex_iterable=ex_iterable,
            info=info,
            split=self._split,
            format_type=self._format_type,
            shuffling=self._shuffling,
            distributed=self._distributed,
            token_per_repo_id=self._token_per_repo_id,
        )

    def cast_column(self, column: str, feature: FeatureType) -> "IterableDataset":
        """Cast column to feature for decoding.

        Args:
            column (`str`):
                Column name.
            feature (`Feature`):
                Target feature.

        Returns:
            `IterableDataset`

        Example:

        ```py
        >>> from datasets import load_dataset, Audio
        >>> ds = load_dataset("PolyAI/minds14", name="en-US", split="train", streaming=True)
        >>> ds.features
        {'audio': Audio(sampling_rate=8000, mono=True, decode=True, id=None),
         'english_transcription': Value(dtype='string', id=None),
         'intent_class': ClassLabel(num_classes=14, names=['abroad', 'address', 'app_error', 'atm_limit', 'balance', 'business_loan',  'card_issues', 'cash_deposit', 'direct_debit', 'freeze', 'high_value_payment', 'joint_account', 'latest_transactions', 'pay_bill'], id=None),
         'lang_id': ClassLabel(num_classes=14, names=['cs-CZ', 'de-DE', 'en-AU', 'en-GB', 'en-US', 'es-ES', 'fr-FR', 'it-IT', 'ko-KR',  'nl-NL', 'pl-PL', 'pt-PT', 'ru-RU', 'zh-CN'], id=None),
         'path': Value(dtype='string', id=None),
         'transcription': Value(dtype='string', id=None)}
        >>> ds = ds.cast_column("audio", Audio(sampling_rate=16000))
        >>> ds.features
        {'audio': Audio(sampling_rate=16000, mono=True, decode=True, id=None),
         'english_transcription': Value(dtype='string', id=None),
         'intent_class': ClassLabel(num_classes=14, names=['abroad', 'address', 'app_error', 'atm_limit', 'balance', 'business_loan',  'card_issues', 'cash_deposit', 'direct_debit', 'freeze', 'high_value_payment', 'joint_account', 'latest_transactions', 'pay_bill'], id=None),
         'lang_id': ClassLabel(num_classes=14, names=['cs-CZ', 'de-DE', 'en-AU', 'en-GB', 'en-US', 'es-ES', 'fr-FR', 'it-IT', 'ko-KR',  'nl-NL', 'pl-PL', 'pt-PT', 'ru-RU', 'zh-CN'], id=None),
         'path': Value(dtype='string', id=None),
         'transcription': Value(dtype='string', id=None)}
        ```
        """
        info = self._info.copy()
        info.features[column] = feature
        # check that it's still valid, especially with regard to task templates
        try:
            info.copy()
        except ValueError:
            info.task_templates = None
        return IterableDataset(
            ex_iterable=self._ex_iterable,
            info=info,
            split=self._split,
            format_type=self._format_type,
            shuffling=copy.deepcopy(self._shuffling),
            distributed=copy.deepcopy(self._distributed),
            token_per_repo_id=self._token_per_repo_id,
        )

    def cast(
        self,
        features: Features,
    ) -> "IterableDataset":
        """
        Cast the dataset to a new set of features.

        Args:
            features ([`Features`]):
                New features to cast the dataset to.
                The name of the fields in the features must match the current column names.
                The type of the data must also be convertible from one type to the other.
                For non-trivial conversion, e.g. `string` <-> `ClassLabel` you should use [`~Dataset.map`] to update the Dataset.

        Returns:
            `IterableDataset`: A copy of the dataset with casted features.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("rotten_tomatoes", split="train", streaming=True)
        >>> ds.features
        {'label': ClassLabel(num_classes=2, names=['neg', 'pos'], id=None),
         'text': Value(dtype='string', id=None)}
        >>> new_features = ds.features.copy()
        >>> new_features["label"] = ClassLabel(names=["bad", "good"])
        >>> new_features["text"] = Value("large_string")
        >>> ds = ds.cast(new_features)
        >>> ds.features
        {'label': ClassLabel(num_classes=2, names=['bad', 'good'], id=None),
         'text': Value(dtype='large_string', id=None)}
        ```
        """
        info = self._info.copy()
        info.features = features
        # check that it's still valid, especially with regard to task templates
        try:
            info.copy()
        except ValueError:
            info.task_templates = None
        return IterableDataset(
            ex_iterable=self._ex_iterable,
            info=info,
            split=self._split,
            format_type=self._format_type,
            shuffling=copy.deepcopy(self._shuffling),
            distributed=copy.deepcopy(self._distributed),
            token_per_repo_id=self._token_per_repo_id,
        )

    def _step(self, step: int, offset: int) -> "IterableDataset":
        ex_iterable = StepExamplesIterable(self._ex_iterable, step=step, offset=offset)
        return IterableDataset(
            ex_iterable=ex_iterable,
            info=self._info.copy(),
            split=self._split,
            format_type=self._format_type,
            shuffling=copy.deepcopy(self._shuffling),
            distributed=copy.deepcopy(self._distributed),
            token_per_repo_id=self._token_per_repo_id,
        )

    def _resolve_features(self):
        if self.features is not None:
            return self
        elif isinstance(self._ex_iterable, TypedExamplesIterable):
            features = self._ex_iterable.features
        else:
            features = _infer_features_from_batch(self._head())
        info = self.info.copy()
        info.features = features
        return IterableDataset(
            ex_iterable=self._ex_iterable,
            info=info,
            split=self._split,
            format_type=self._format_type,
            shuffling=copy.deepcopy(self._shuffling),
            distributed=copy.deepcopy(self._distributed),
            token_per_repo_id=self._token_per_repo_id,
        )


def _concatenate_iterable_datasets(
    dsets: List[IterableDataset],
    info: Optional[DatasetInfo] = None,
    split: Optional[NamedSplit] = None,
    axis: int = 0,
) -> IterableDataset:
    """
    Converts a list of `IterableDataset` with the same schema into a single `IterableDataset`.
    Missing data are filled with None values.

    <Added version="2.4.0"/>

    Args:
        dsets (`List[datasets.IterableDataset]`): List of Datasets to concatenate.
        info (`DatasetInfo`, optional): Dataset information, like description, citation, etc.
        split (`NamedSplit`, optional): Name of the dataset split.
        axis (``{0, 1}``, default ``0``, meaning over rows):
            Axis to concatenate over, where ``0`` means over rows (vertically) and ``1`` means over columns
            (horizontally).

            *New in version 1.6.0*

    Example:

    ```py
    >>> ds3 = _concatenate_iterable_datasets([ds1, ds2])
    ```
    """
    dsets = [d._resolve_features() for d in dsets]

    # Perform checks (and a potentional cast if axis=0)
    if axis == 0:
        _check_if_features_can_be_aligned([dset.features for dset in dsets])
    else:
        _check_column_names([col_name for dset in dsets for col_name in dset.features])

    # TODO: improve this to account for a mix of ClassLabel and Value for example
    # right now it would keep the type of the first dataset in the list
    features = Features(
        {k: v for features in _align_features([dset.features for dset in dsets]) for k, v in features.items()}
    )

    ex_iterables = [d._ex_iterable for d in dsets]
    if axis == 0:
        ex_iterable = VerticallyConcatenatedMultiSourcesExamplesIterable(ex_iterables)
    else:
        ex_iterable = HorizontallyConcatenatedMultiSourcesExamplesIterable(ex_iterables)
    # Set new info - we update the features
    # setting the features also ensures to fill missing columns with None
    if info is None:
        info = DatasetInfo.from_merge([d.info for d in dsets])
    else:
        info = info.copy()
    info.features = features
    # Get all the auth tokens per repository - in case the datasets come from different private repositories
    token_per_repo_id = {repo_id: token for dataset in dsets for repo_id, token in dataset._token_per_repo_id.items()}
    # Return new daset
    return IterableDataset(ex_iterable=ex_iterable, info=info, split=split, token_per_repo_id=token_per_repo_id)


def _interleave_iterable_datasets(
    datasets: List[IterableDataset],
    probabilities: Optional[List[float]] = None,
    seed: Optional[int] = None,
    info: Optional[DatasetInfo] = None,
    split: Optional[NamedSplit] = None,
    stopping_strategy: Optional[str] = "first_exhausted",
) -> IterableDataset:
    """
    Interleave several iterable datasets (sources) into a single iterable dataset.
    The new iterable dataset alternates between the sources to yield examples.
    If `probabilities = None` (default) the iterable dataset will cycles through the sources in order for each next example in the iteration.
    If `probabilities` is not `None, the iterable dataset will sample a random source according to the provided probabilities for each next examples in the iteration.

    <Added version="2.4.0"/>

    Args:
        datasets (`List[IterableDataset]`): list of datasets to interleave
        probabilities (`List[float]`, optional, default None): If specified, the new iterable dataset samples
            examples from one source at a time according to these probabilities.
        seed (`int`, optional, default None): The random seed used to choose a source for each example.
        stopping_strategy (Optional `str`, defaults to `first_exhausted`):
            Two strategies are proposed right now.
            By default, `first_exhausted` is an undersampling strategy, i.e the dataset construction is stopped as soon as one dataset has ran out of samples.
            If the strategy is `all_exhausted`,  we use an oversampling strategy, i.e the dataset construction is stopped as soon as every samples of every dataset has been added at least once.
            Note that if the strategy is `all_exhausted`, the interleaved dataset size can get enormous:
            - with no probabilities, the resulting dataset will have max_length_datasets*nb_dataset samples.
            - with given probabilities, the resulting dataset will have more samples if some datasets have really low probability of visiting.

    Output:
        `datasets.IterableDataset`
    """
    datasets = [d._resolve_features() for d in datasets]

    # Perform checks
    _check_if_features_can_be_aligned([dset.features for dset in datasets])

    # TODO: improve this to account for a mix of ClassLabel and Value for example
    # right now it would keep the type of the first dataset in the list
    features = Features(
        {k: v for features in _align_features([dset.features for dset in datasets]) for k, v in features.items()}
    )

    ex_iterables = [d._ex_iterable for d in datasets]

    # Use cycling or random cycling or sources
    if probabilities is None:
        ex_iterable = CyclingMultiSourcesExamplesIterable(ex_iterables, stopping_strategy=stopping_strategy)
    else:
        generator = np.random.default_rng(seed)
        ex_iterable = RandomlyCyclingMultiSourcesExamplesIterable(
            ex_iterables, generator=generator, probabilities=probabilities, stopping_strategy=stopping_strategy
        )
    # Set new info - we update the features
    # setting the features also ensures to fill missing columns with None
    if info is None:
        info = DatasetInfo.from_merge([d.info for d in datasets])
    else:
        info = info.copy()
    info.features = features
    # Get all the auth tokens per repository - in case the datasets come from different private repositories
    token_per_repo_id = {
        repo_id: token for dataset in datasets for repo_id, token in dataset._token_per_repo_id.items()
    }
    # Return new daset
    return IterableDataset(ex_iterable=ex_iterable, info=info, split=split, token_per_repo_id=token_per_repo_id)


def _split_by_node_iterable_dataset(dataset: IterableDataset, rank: int, world_size: int) -> IterableDataset:
    """
    Split an iterable dataset for the node at rank `rank` in a pool of nodes of size `world_size`.

    If the dataset has a number of shards that is a factor of `world_size` (i.e. if `dataset.n_shards % world_size == 0`),
    then the shards are evenly assigned across the nodes, which is the most optimized.
    Otherwise, each node keeps 1 example out of `world_size`, skipping the other examples.

    Args:
        dataset ([`IterableDataset`]):
            The iterable dataset to split by node.
        rank (`int`):
            Rank of the current node.
        world_size (`int`):
            Total number of nodes.

    Returns:
        [`IterableDataset`]: The iterable dataset to be used on the node at rank `rank`.
    """
    if dataset._distributed:
        world_size = world_size * dataset._distributed.world_size
        rank = world_size * dataset._distributed.rank + rank
    distributed = DistributedConfig(rank=rank, world_size=world_size)
    return IterableDataset(
        ex_iterable=dataset._ex_iterable,
        info=dataset._info.copy(),
        split=dataset._split,
        format_type=dataset._format_type,
        shuffling=copy.deepcopy(dataset._shuffling),
        distributed=distributed,
        token_per_repo_id=dataset._token_per_repo_id,
    )
