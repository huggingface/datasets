import copy
import importlib
import os
from dataclasses import dataclass
from functools import partial
from itertools import cycle, repeat
from typing import Any, Callable, Dict, Iterable, List, Optional, Union

import fsspec
import numpy as np
import pyarrow as pa

from .arrow_dataset import DatasetInfoMixin
from .builder import ArrowBasedBuilder, DatasetBuilder, GeneratorBasedBuilder
from .features import Features
from .formatting import PythonFormatter
from .info import DatasetInfo
from .load import import_main_class, prepare_module, url_or_path_parent
from .splits import NamedSplit, Split
from .utils import DownloadConfig, map_nested
from .utils.download_manager import GenerateMode
from .utils.file_utils import is_relative_path, url_or_path_join
from .utils.logging import get_logger
from .utils.version import Version


logger = get_logger(__name__)


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


def _shuffle_kwargs(rng: np.random.Generator, kwargs: dict) -> dict:
    shuffled_kwargs = {}
    for key, value in sorted(kwargs.items()):
        if isinstance(value, list):
            value = list(value)
            rng.shuffle(value)
            shuffled_kwargs[key] = value
        elif isinstance(value, dict):
            keys = list(value)
            rng.shuffle(keys)
            shuffled_kwargs[key] = {k: value[k] for k in keys}
        else:
            shuffled_kwargs[key] = value
    return shuffled_kwargs


class ExamplesIterable(_BaseExamplesIterable):
    def __init__(self, generate_examples_fn, kwargs):
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


class CyclingMultiSourcesExamplesIterable(_BaseExamplesIterable):
    def __init__(self, ex_iterables):
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


class RandomlyCyclingMultiSourcesExamplesIterable(CyclingMultiSourcesExamplesIterable):
    def __init__(self, ex_iterables, seed: Optional[int] = None, probabilities: Optional[List[float]] = None):
        super().__init__(ex_iterables)
        self.seed = seed
        self.probabilities = probabilities

    @staticmethod
    def _iter_random_indices(rng: np.random.Generator, num_generate_examples_fn_: int, random_batch_size=1000, p: Optional[List[float]] = None):
        if p is None:
            while True:
                yield from rng.integers(0, num_generate_examples_fn_, size=random_batch_size)
        else:
            while True:
                yield from rng.choice(num_generate_examples_fn_, size=random_batch_size, p=p)

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

    def __init__(self, ex_iterable: _BaseExamplesIterable, function: Callable, batch_size: Optional[int] = None):
        self.ex_iterable = ex_iterable
        self.function = function
        self.batch_size = batch_size

    def __iter__(self):
        iterator = iter(self.ex_iterable)
        for key, example in iterator:
            if self.batch_size is None:
                yield key, self.function(example)
            else:
                key_examples = [(key, example)] + [(key, example) for (key, example), _ in zip(iterator, range(self.batch_size - 1))]
                keys, examples = zip(*key_examples)
                batch = _examples_to_batch(examples)
                transformed_batch = self.function(batch)
                yield from zip(keys, _batch_to_examples(transformed_batch))

    def shuffle(self, seed: Optional[int]) -> "MappedExamplesIterable":
        """Shuffle the wrapped examples iterable."""
        return MappedExamplesIterable(self.ex_iterable.shuffle(seed), function=self.function, batch_size=self.batch_size)


class BufferShuffledExamplesIterable(_BaseExamplesIterable):

    def __init__(self, ex_iterable: _BaseExamplesIterable, buffer_size: int, seed: Optional[int]):
        self.ex_iterable = ex_iterable
        self.buffer_size = buffer_size
        self.seed = seed

    @staticmethod
    def _iter_random_indices(rng: np.random.Generator, buffer_size: int, random_batch_size=1000):
        while True:
            yield from rng.integers(0, buffer_size, size=random_batch_size)

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
        return _examples_to_batch([x for (key, x), _ in zip(self._iter(), range(n))])

    def _iter(
        self,
        epoch=0,
        shuffling: Optional[ShuffingConfig] = None,
    ):
        if shuffling:
            effective_seed = shuffling.seed + epoch if shuffling.seed is not None else None
            ex_iterable = self._ex_iterable.shuffle(effective_seed)
        else:
            ex_iterable = self._ex_iterable
        yield from ex_iterable

    def __iter__(self):
        for key, example in self._iter(
            epoch=self._epoch,
            shuffling=self._shuffling,
        ):
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

        Args:

            type (:obj:`str`, optional, default None): if set to "torch", the returned dataset
                will be a subclass of torch.utils.data.IterableDataset to be used in a DataLoader
        """
        return iterable_dataset(
            ex_iterable=self._ex_iterable,
            info=copy.deepcopy(self._info),
            split=self._split,
            format_type=type,
            shuffling=copy.deepcopy(self._shuffling),
        )

    def map(
        self,
        function: Callable,
        batch_size: Optional[int] = None
    ):
        """
        Return a dataset with the specified map function. The function is applied on-the-fly on the examples
        when iterating the dataset

        Args:
            function (:obj:`Callable`, optional, default None): if not None, this function is applied
                on-the-fly on the examples when you iterate on the dataset.
            batch_size (:obj:`int`, optional, default None): define the size of the batch passed
                to each call of the function:

                - if batch_size is None, then the function takes 1 example in and should return 1 example.
                    An example is a dictionary, e.g. {"text": "Hello there !"}
                - if batch_size is 1, then the function takes a batch of 1 example as input and can return
                    a batch with 1 or more examples.
                    A batch is a dictionary, e.g. a batch of 1 example is {"text": ["Hello there !"]}
                - if batch_size is ``n`` > 1, then the function takes a batch of ``n`` examples as input
                    and can return a batch with ``n`` examples, or with an arbitrary number of examples.
                    Note that the last batch may have less than ``n`` examples.
                    A batch is a dictionary, e.g. a batch of ``n`` examples is {"text": ["Hello there !"] * n}
        """
        info = copy.deepcopy(self._info)
        info.features = None
        ex_iterable = MappedExamplesIterable(self._ex_iterable, function=function, batch_size=batch_size)
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


def merge_datasets(datasets: List[IterableDataset], probabilities: Optional[List[float]] = None, seed: Optional[int] = None) -> IterableDataset:
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
    if probabilities is None:
        ex_iterable = CyclingMultiSourcesExamplesIterable([d._ex_iterable for d in datasets])
    else:
        ex_iterable = RandomlyCyclingMultiSourcesExamplesIterable([d._ex_iterable for d in datasets], seed=seed, probabilities=probabilities)
    info = DatasetInfo.from_merge([d.info for d in datasets])
    info.features = datasets[0].features
    return iterable_dataset(ex_iterable=ex_iterable, info=info)


class IterableDatasetDict(dict):
    pass


def load_dataset(
    path: str,
    name: Optional[str] = None,
    data_dir: Optional[str] = None,
    data_files: Union[Dict, List] = None,
    split: Optional[Union[str, Split]] = None,
    cache_dir: Optional[str] = None,
    features: Optional[Features] = None,
    download_config: Optional[DownloadConfig] = None,
    download_mode: Optional[GenerateMode] = None,
    script_version: Optional[Union[str, Version]] = None,
    use_auth_token: Optional[Union[bool, str]] = None,
    **config_kwargs,
):
    r"""Load a dataset in a streaming fashion to get iterable datasets.
    The data are loaded on-the-fly while iterating the dataset.

    This method does the following under the hood:

        1. Download and import in the library the dataset loading script from ``path`` if it's not already cached inside the library.

            Processing scripts are small python scripts that define the citation, info and format of the dataset,
            contain the URL to the original data files and the code to load examples from the original data files.

            You can find some of the scripts here: https://github.com/huggingface/datasets/datasets
            and easily upload yours to share them using the CLI ``huggingface-cli``.
            You can find the complete list of datasets in the Datasets Hub at https://huggingface.co/datasets

        2. Run the dataset loading script which will:

            * Prefetch the dataset file from the original URL (see the script) if it's not already downloaded and cached.
            * Iterate through the dataset file to generate examples.

                Usually data are loaded line by line from the dataset file in order to stream the data instead of downloading everything.
                However in some cases (for json data or compressed archives for example), the whole file needs to be loaded in memory.
                In this case, the dataset file is entirely downloaded before the examples are generated.

        3. Return a dataset built from the requested splits in ``split`` (default: all).

    Args:

        path (:obj:`str`): Path to the dataset processing script with the dataset builder. Can be either:

            - a local path to processing script or the directory containing the script (if the script has the same name as the directory),
              e.g. ``'./dataset/squad'`` or ``'./dataset/squad/squad.py'``.
            - a dataset identifier in the HuggingFace Datasets Hub (list all available datasets and ids with ``datasets.list_datasets()``)
              e.g. ``'squad'``, ``'glue'`` or ``'openai/webtext'``.
        name (:obj:`str`, optional): Defining the name of the dataset configuration.
        data_files (:obj:`str`, optional): Defining the data_files of the dataset configuration.
        data_dir (:obj:`str`, optional): Defining the data_dir of the dataset configuration.
        split (:class:`Split` or :obj:`str`): Which split of the data to load.
            If None, will return a `dict` with all splits (typically `datasets.Split.TRAIN` and `datasets.Split.TEST`).
            If given, will return a single Dataset.
            Splits can be combined and specified like in tensorflow-datasets.
        cache_dir (:obj:`str`, optional): Directory to read/write data. Defaults to "~/datasets".
        features (:class:`Features`, optional): Set the features type to use for this dataset.
        download_config (:class:`~utils.DownloadConfig`, optional): Specific download configuration parameters.
        download_mode (:class:`GenerateMode`, optional): Select the download/generate mode - Default to REUSE_DATASET_IF_EXISTS
        script_version (:class:`~utils.Version` or :obj:`str`, optional): Version of the dataset script to load:

            - For canonical datasets in the `huggingface/datasets` library like "squad", the default version of the module is the local version fo the lib.
              You can specify a different version from your local version of the lib (e.g. "master" or "1.2.0") but it might cause compatibility issues.
            - For community provided datasets like "lhoestq/squad" that have their own git repository on the Datasets Hub, the default version "main" corresponds to the "main" branch.
              You can specify a different version that the default "main" by using a commit sha or a git tag of the dataset repository.
        use_auth_token (Optional ``Union[str, bool]``): Optional string or boolean to use as Bearer token for remote files on the Datasets Hub.
            If True, will get token from `~/.huggingface`.
        **config_kwargs: Keyword arguments to be passed to the :class:`BuilderConfig` and used in the :class:`DatasetBuilder`.

    Returns:
        :class:`IterableDataset` or :class:`IterableDatasetDict`:
            if `split` is not None: the dataset requested,
            if `split` is None, a ``datasets.streaming.IterableDatasetDict`` with each split.

    """
    # Download/copy dataset processing script
    module_path, hash, resolved_file_path = prepare_module(
        path,
        script_version=script_version,
        download_config=download_config,
        download_mode=download_mode,
        dataset=True,
        return_resolved_file_path=True,
        use_auth_token=use_auth_token,
    )
    extend_module_for_streaming(module_path)

    # Set the base path for downloads as the parent of the script location
    if resolved_file_path is not None:
        base_path = url_or_path_parent(resolved_file_path)
    else:
        base_path = None

    # Get dataset builder class from the processing script
    builder_cls = import_main_class(module_path, dataset=True)

    # Instantiate the dataset builder
    builder_instance: DatasetBuilder = builder_cls(
        cache_dir=cache_dir,
        name=name,
        data_dir=data_dir,
        data_files=data_files,
        hash=hash,
        features=features,
        **config_kwargs,
    )

    # Build dataset for splits
    ds = as_streaming_dataset(
        builder_instance,
        split=split,
        base_path=base_path,
        use_auth_token=use_auth_token,
    )

    return ds


def extend_module_for_streaming(module_path):
    def xopen(file, mode="r", *args, **kwargs):
        return fsspec.open(file, mode=mode, *args, **kwargs).open()

    module = importlib.import_module(module_path)
    module.open = xopen


class StreamingDownloadManager(object):
    def __init__(
        self,
        dataset_name: Optional[str] = None,
        data_dir: Optional[str] = None,
        download_config: Optional[DownloadConfig] = None,
        base_path: Optional[str] = None,
    ):
        self._dataset_name = dataset_name
        self._data_dir = data_dir
        self._download_config = download_config or DownloadConfig()
        self._base_path = base_path or os.path.abspath(".")

    @property
    def manual_dir(self):
        return self._data_dir

    def download(self, url_or_urls):
        url_or_urls = map_nested(self._download, url_or_urls, map_tuple=True)
        return url_or_urls

    def _download(self, url_or_filename):
        if is_relative_path(url_or_filename):
            # append the relative path to the base_path
            url_or_filename = url_or_path_join(self._base_path, url_or_filename)
        return url_or_filename

    def extract(self, path_or_paths):
        return path_or_paths

    def download_and_extract(self, url_or_urls):
        return self.extract(self.download(url_or_urls))


def as_streaming_dataset(
    builder_instance: Union[GeneratorBasedBuilder, ArrowBasedBuilder],
    split: Optional[str] = None,
    base_path: Optional[str] = None,
    use_auth_token: Optional[str] = None,
) -> Union[Dict[str, IterableDataset], IterableDataset]:
    if not isinstance(builder_instance, (GeneratorBasedBuilder, ArrowBasedBuilder)):
        raise ValueError(f"Builder {builder_instance.name} is not streamable.")
    # By default, return all splits
    if split is None:
        split = {s: s for s in builder_instance.info.splits}

    # Create a dataset for each of the given splits
    datasets = map_nested(
        partial(
            _as_streaming_dataset_single,
            builder_instance=builder_instance,
            base_path=base_path,
            use_auth_token=use_auth_token,
        ),
        split,
        map_tuple=True,
    )
    if isinstance(datasets, dict):
        datasets = IterableDatasetDict(datasets)
    return datasets


def _as_streaming_dataset_single(
    split: str,
    builder_instance: Union[GeneratorBasedBuilder, ArrowBasedBuilder],
    base_path: Optional[str] = None,
    use_auth_token: Optional[str] = None,
) -> IterableDataset:
    dl_manager = StreamingDownloadManager(
        base_path=base_path,
        download_config=DownloadConfig(use_auth_token=use_auth_token),
        dataset_name=builder_instance.name,
        data_dir=builder_instance.config.data_dir,
    )
    splits_generators = {sg.name: sg for sg in builder_instance._split_generators(dl_manager)}
    if split not in splits_generators:
        raise ValueError(f"Bad split: {split}. Available splits: {list(splits_generators)}")
    gen_kwargs = splits_generators[split].gen_kwargs
    if isinstance(builder_instance, ArrowBasedBuilder):
        ex_iterable = ExamplesIterable(
            _generate_examples_from_tables_wrapper(builder_instance._generate_tables), kwargs=gen_kwargs
        )
    else:
        ex_iterable = ExamplesIterable(builder_instance._generate_examples, kwargs=gen_kwargs)
    return IterableDataset(ex_iterable, info=builder_instance.info, split=split)
