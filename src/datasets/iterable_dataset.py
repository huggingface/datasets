import copy
from dataclasses import dataclass
from itertools import cycle, islice, repeat
from typing import Any, Callable, Dict, Iterable, Iterator, List, Optional

import numpy as np
import pyarrow as pa

from .arrow_dataset import DatasetInfoMixin
from .features import Features
from .formatting import PythonFormatter
from .info import DatasetInfo
from .splits import NamedSplit


def _infer_features_from_batch(batch: Dict[str, list], try_features: Optional[Features] = None) -> Features:
    pa_table = pa.Table.from_pydict(batch)
    if try_features is not None:
        try:
            pa_table = pa_table.cast(pa.schema(try_features.type))
        except (pa.ArrowInvalid, pa.ArrowNotImplementedError):
            pass
    return Features.from_arrow_schema(pa_table.schema)


def _examples_to_batch(examples: List[Dict[str, Any]]) -> Dict[str, list]:
    cols = sorted(examples[0].keys())
    arrays = []
    for col in cols:
        arrays.append([example[col] for example in examples])
    return dict(zip(cols, arrays))


def _batch_to_examples(batch: Dict[str, list]) -> List[Dict[str, Any]]:
    n_examples = len(batch[next(iter(batch))])
    for i in range(n_examples):
        yield {col: array[i] for col, array in batch.items()}


class _BaseExamplesIterable:
    def __iter__(self):
        raise NotImplementedError()

    def shuffle(self, seed: Optional[int]) -> "_BaseExamplesIterable":
        raise NotImplementedError()

    @property
    def n_shards(self) -> int:
        raise NotImplementedError()


def _shuffle_kwargs(rng: np.random.Generator, kwargs: dict) -> dict:
    shuffled_kwargs = {}
    for key, value in sorted(kwargs.items()):
        if isinstance(value, list):
            value = list(value)
            rng.shuffle(value)
            shuffled_kwargs[key] = value
        else:
            shuffled_kwargs[key] = value
    return shuffled_kwargs


class ExamplesIterable(_BaseExamplesIterable):
    def __init__(self, generate_examples_fn: Callable, kwargs: dict):
        self.generate_examples_fn = generate_examples_fn
        self.kwargs = kwargs

    def __iter__(self):
        for key, example in self.generate_examples_fn(**self.kwargs):
            yield key, example

    def shuffle(self, seed: Optional[int]) -> "ExamplesIterable":
        """Shuffle the kwargs order to shuffle shards for example"""
        rng = np.random.default_rng(seed)
        kwargs = _shuffle_kwargs(rng, self.kwargs)
        return ExamplesIterable(self.generate_examples_fn, kwargs)

    @property
    def n_shards(self) -> int:
        max_length = max([len(value) for value in self.kwargs.values() if isinstance(value, list)], default=0)
        return max(1, max_length)


class CyclingMultiSourcesExamplesIterable(_BaseExamplesIterable):
    def __init__(self, ex_iterables: List[_BaseExamplesIterable]):
        self.ex_iterables = ex_iterables

    def __iter__(self):
        iterators = [iter(ex_iterable) for ex_iterable in self.ex_iterables]
        indices_iterator = cycle(range(len(iterators)))
        for i in indices_iterator:
            for key, example in iterators[i]:
                yield key, example
                break
            else:
                break

    def shuffle(self, seed: Optional[int]) -> "CyclingMultiSourcesExamplesIterable":
        """Shuffle each underlying examples iterable."""
        ex_iterables = [ex_iterable.shuffle(seed) for ex_iterable in self.ex_iterables]
        return CyclingMultiSourcesExamplesIterable(ex_iterables)

    @property
    def n_shards(self) -> int:
        return sum(ex_iterable.n_shards for ex_iterable in self.ex_iterables)


class RandomlyCyclingMultiSourcesExamplesIterable(CyclingMultiSourcesExamplesIterable):
    def __init__(self, ex_iterables, seed: Optional[int] = None, probabilities: Optional[List[float]] = None):
        super().__init__(ex_iterables)
        self.seed = seed
        self.probabilities = probabilities

    @staticmethod
    def _iter_random_indices(
        rng: np.random.Generator,
        num_sources: int,
        random_batch_size=1000,
        p: Optional[List[float]] = None,
    ) -> Iterator[int]:
        if p is None:
            while True:
                yield from (int(i) for i in rng.integers(0, num_sources, size=random_batch_size))
        else:
            while True:
                yield from (int(i) for i in rng.choice(num_sources, size=random_batch_size, p=p))

    def __iter__(self):
        rng = np.random.default_rng(self.seed)
        iterators = [iter(ex_iterable) for ex_iterable in self.ex_iterables]
        indices_iterator = self._iter_random_indices(rng, len(iterators), p=self.probabilities)
        for i in indices_iterator:
            for key, example in iterators[i]:
                yield key, example
                break
            else:
                break

    def shuffle(self, seed: Optional[int]) -> "RandomlyCyclingMultiSourcesExamplesIterable":
        """Shuffle the sources order as well as the each wrapper examples iterable."""
        ex_iterables = [ex_iterable.shuffle(seed) for ex_iterable in self.ex_iterables]
        return RandomlyCyclingMultiSourcesExamplesIterable(ex_iterables, seed=seed, probabilities=self.probabilities)


class MappedExamplesIterable(_BaseExamplesIterable):
    def __init__(
        self, ex_iterable: _BaseExamplesIterable, function: Callable, batched: bool = False, batch_size: int = 1000
    ):
        self.ex_iterable = ex_iterable
        self.function = function
        self.batched = batched
        self.batch_size = batch_size

    def __iter__(self):
        iterator = iter(self.ex_iterable)
        for key, example in iterator:
            if self.batched:
                key_examples = [(key, example)] + [
                    (key, example) for key, example in islice(iterator, self.batch_size - 1)
                ]
                keys, examples = zip(*key_examples)
                batch = _examples_to_batch(examples)
                transformed_batch = self.function(batch)
                new_key = "_".join(str(key) for key in keys)
                yield from zip(repeat(new_key), _batch_to_examples(transformed_batch))
            else:
                yield key, self.function(example)

    def shuffle(self, seed: Optional[int]) -> "MappedExamplesIterable":
        """Shuffle the wrapped examples iterable."""
        return MappedExamplesIterable(
            self.ex_iterable.shuffle(seed), function=self.function, batch_size=self.batch_size
        )

    @property
    def n_shards(self) -> int:
        return self.ex_iterable.n_shards


class BufferShuffledExamplesIterable(_BaseExamplesIterable):
    def __init__(self, ex_iterable: _BaseExamplesIterable, buffer_size: int, seed: Optional[int]):
        self.ex_iterable = ex_iterable
        self.buffer_size = buffer_size
        self.seed = seed

    @staticmethod
    def _iter_random_indices(rng: np.random.Generator, buffer_size: int, random_batch_size=1000) -> Iterator[int]:
        while True:
            yield from (int(i) for i in rng.integers(0, buffer_size, size=random_batch_size))

    def __iter__(self):
        buffer_size = self.buffer_size
        rng = np.random.default_rng(self.seed)
        indices_iterator = self._iter_random_indices(rng, buffer_size)
        mem_buffer = []
        for x in self.ex_iterable:
            if len(mem_buffer) == buffer_size:
                i = next(indices_iterator)
                yield mem_buffer[i]
                mem_buffer[i] = x
            else:
                mem_buffer.append(x)
        rng.shuffle(mem_buffer)
        yield from mem_buffer

    def shuffle(self, seed: Optional[int]) -> "BufferShuffledExamplesIterable":
        """Shuffle the wrapped examples iterable as well as the shuffling buffer."""
        return BufferShuffledExamplesIterable(self.ex_iterable.shuffle(seed), buffer_size=self.buffer_size, seed=seed)

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
class ShuffingConfig:
    seed: Optional[int] = None


class IterableDataset(DatasetInfoMixin):
    """A Dataset backed by an iterable."""

    def __init__(
        self,
        ex_iterable: _BaseExamplesIterable,
        info: Optional[DatasetInfo] = None,
        split: Optional[NamedSplit] = None,
        format_type: Optional[str] = None,
        shuffling: Optional[ShuffingConfig] = None,
    ):
        info = info.copy() if info is not None else DatasetInfo()
        DatasetInfoMixin.__init__(self, info=info, split=split)

        self._ex_iterable = ex_iterable
        self._format_type = format_type
        self._shuffling = shuffling
        self._epoch = 0

    def _head(self, n=5):
        return _examples_to_batch([x for key, x in islice(self._iter(), n)])

    @property
    def _effective_seed(self):
        if self._shuffling:
            return self._shuffling.seed + self._epoch if self._shuffling.seed is not None else None
        else:
            return None

    @property
    def n_shards(self) -> int:
        return self._ex_iterable.n_shards

    def _iter(self):
        if self._shuffling:
            ex_iterable = self._ex_iterable.shuffle(self._effective_seed)
        else:
            ex_iterable = self._ex_iterable
        yield from ex_iterable

    def __iter__(self):
        for key, example in self._iter():
            if self.features:
                yield self.features.encode_example(example)
            else:
                yield example

    def with_format(
        self,
        type: Optional[str] = None,
    ) -> "IterableDataset":
        """
        Return a dataset with the specified format.
        This method only supports the "torch" format for now.

        Args:

            type (:obj:`str`, optional, default None): if set to "torch", the returned dataset
                will be a subclass of torch.utils.data.IterableDataset to be used in a DataLoader
        """
        # TODO(QL): add examples formatting to get tensors when using the "torch" format
        # TODO(QL): add format_kwargs
        # TODO(QL): add format_columns and return_all_columns
        # TODO(QL): add pandas, numpy and tf formats
        return iterable_dataset(
            ex_iterable=self._ex_iterable,
            info=copy.deepcopy(self._info),
            split=self._split,
            format_type=type,
            shuffling=copy.deepcopy(self._shuffling),
        )

    def map(self, function: Callable, batched: bool = False, batch_size: int = 1000):
        """
        Return a dataset with the specified map function. The function is applied on-the-fly on the examples when iterating over the dataset.

        You can specify whether the function should be batched or not with the ``batched`` parameter:

        - If batched is False, then the function takes 1 example in and should return 1 example.
          An example is a dictionary, e.g. {"text": "Hello there !"}
        - If batched is True and batch_size is 1, then the function takes a batch of 1 example as input and can return a batch with 1 or more examples.
          A batch is a dictionary, e.g. a batch of 1 example is {"text": ["Hello there !"]}
        - If batched is True and batch_size is ``n`` > 1, then the function takes a batch of ``n`` examples as input and can return a batch with ``n`` examples, or with an arbitrary number of examples.
          Note that the last batch may have less than ``n`` examples.
          A batch is a dictionary, e.g. a batch of ``n`` examples is {"text": ["Hello there !"] * n}

        Args:
            function (:obj:`Callable`, optional, default None): if not None, this function is applied
                on-the-fly on the examples when you iterate on the dataset.
            batched (:obj:`bool`, default `False`): Provide batch of examples to `function`.
            batch_size (:obj:`int`, optional, default ``1000``): Number of examples per batch provided to `function` if `batched=True`.

        """
        info = copy.deepcopy(self._info)
        info.features = None
        ex_iterable = MappedExamplesIterable(
            self._ex_iterable, function=function, batched=batched, batch_size=batch_size
        )
        return iterable_dataset(
            ex_iterable=ex_iterable,
            info=info,
            split=self._split,
            format_type=self._format_type,
            shuffling=copy.deepcopy(self._shuffling),
        )

    def shuffle(self, buffer_size, seed=None) -> "IterableDataset":
        """
        Randomly shuffles the elements of this dataset.

        This dataset fills a buffer with buffer_size elements, then randomly samples elements from this buffer,
        replacing the selected elements with new elements. For perfect shuffling, a buffer size greater than or
        equal to the full size of the dataset is required.

        For instance, if your dataset contains 10,000 elements but buffer_size is set to 1,000, then shuffle will
        initially select a random element from only the first 1,000 elements in the buffer. Once an element is
        selected, its space in the buffer is replaced by the next (i.e. 1,001-st) element,
        maintaining the 1,000 element buffer.

        Args:

            buffer_size (:obj:`int`): size of the buffer.
            seed (:obj:`int`, optional, default None): random seed that will be used to create the distribution.
        """
        shuffling = ShuffingConfig(seed=seed)
        return iterable_dataset(
            ex_iterable=BufferShuffledExamplesIterable(self._ex_iterable, buffer_size, seed=seed),
            info=copy.deepcopy(self._info),
            split=self._split,
            format_type=self._format_type,
            shuffling=shuffling,
        )

    def set_epoch(self, epoch: int):
        self._epoch = epoch


def iterable_dataset(
    ex_iterable: Iterable,
    info: Optional[DatasetInfo] = None,
    split: Optional[NamedSplit] = None,
    format_type: Optional[str] = None,
    shuffling: Optional[ShuffingConfig] = None,
):
    if format_type is not None and format_type == "torch":
        import torch

        class TorchIterableDataset(IterableDataset, torch.utils.data.IterableDataset):
            pass

        cls = TorchIterableDataset
    else:
        cls = IterableDataset
    return cls(
        ex_iterable=ex_iterable,
        info=info,
        split=split,
        format_type=format_type,
        shuffling=shuffling,
    )


def merge_datasets(
    datasets: List[IterableDataset], probabilities: Optional[List[float]] = None, seed: Optional[int] = None
) -> IterableDataset:
    """
    Merge several iterable datasets (sources) into one iterable dataset.
    The new iterable dataset alternates between the sources to yield the examples.
    By default it cycles through the sources in order, but you can also make the new
    iterable dataset sample examples from one random source at a time.

    Args:
        datasets (:obj:`List[IterableDataset]`): list of datasets to merge
        probabilities (:obj:`List[float]`, optional, default None): If specified, the new iterable datasets will sample
            examples from one source at a time according to these probabilities.
        seed (:obj:`int`, optional, default None): The random seed used to choose a source for each example to yield.
    """
    # Keep individual features formatting
    ex_iterables = [
        MappedExamplesIterable(d._ex_iterable, d.features.encode_example) if d.features is not None else d._ex_iterable
        for d in datasets
    ]
    # Use cycling or random cycling or sources
    if probabilities is None:
        ex_iterable = CyclingMultiSourcesExamplesIterable(ex_iterables)
    else:
        ex_iterable = RandomlyCyclingMultiSourcesExamplesIterable(ex_iterables, seed=seed, probabilities=probabilities)
    # Set new info - we reset the features
    info = DatasetInfo.from_merge([d.info for d in datasets])
    info.features = None
    # Return new daset
    return iterable_dataset(ex_iterable=ex_iterable, info=info)
