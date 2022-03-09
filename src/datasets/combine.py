from typing import TYPE_CHECKING, Any, List, Optional, TypeVar

import numpy as np

from .info import DatasetInfo
from .utils import logging


logger = logging.get_logger(__name__)


if TYPE_CHECKING:
    from .arrow_dataset import Dataset
    from .iterable_dataset import IterableDataset


DatasetType = TypeVar("DatasetType", "Dataset", "IterableDataset")


def interleave_datasets(
    datasets: List[DatasetType], probabilities: Optional[List[float]] = None, seed: Optional[int] = None
) -> DatasetType:
    """
    Interleave several datasets (sources) into a single dataset.
    The new dataset is constructed by alternating between the sources to get the examples.

    You can use this function on a list of :class:`Dataset` objects, or on a list of :class:`IterableDataset` objects.

    If ``probabilities`` is ``None`` (default) the new dataset is constructed by cycling between each source to get the examples.
    If ``probabilities`` is not ``None``, the new dataset is constructed by getting examples from a random source at a time according to the provided probabilities.

    The resulting dataset ends when one of the source datasets runs out of examples.

    Args:
        datasets (:obj:`List[Dataset]` or :obj:`List[IterableDataset]`): list of datasets to interleave
        probabilities (:obj:`List[float]`, optional, default None): If specified, the new dataset is constructued by sampling
            examples from one source at a time according to these probabilities.
        seed (:obj:`int`, optional, default None): The random seed used to choose a source for each example.
        **kwargs: For map-style datasets:
            Keyword arguments to be passed to :meth:`Dataset.select` when selecting the indices used to interleave the datasets.

    Returns:
        :class:`Dataset` or :class:`IterableDataset`: Return type depends on the input `datasets`
        parameter. `Dataset` if the input is a list of `Dataset`, `IterableDataset` if the input is a list of
        `IterableDataset`.

    Example::

        For regular datasets (map-style):

        >>> from datasets import Dataset, interleave_datasets
        >>> d1 = Dataset.from_dict({"a": [0, 1, 2]})
        >>> d2 = Dataset.from_dict({"a": [10, 11, 12]})
        >>> d3 = Dataset.from_dict({"a": [20, 21, 22]})
        >>> dataset = interleave_datasets([d1, d2, d3])
        >>> dataset["a"]
        [0, 10, 20, 1, 11, 21, 2, 12, 22]
        >>> dataset = interleave_datasets([d1, d2, d3], probabilities=[0.7, 0.2, 0.1], seed=42)
        >>> dataset["a"]
        [10, 0, 11, 1, 2, 20, 12]

        For datasets in streaming mode (iterable):

        >>> from datasets import load_dataset, interleave_datasets
        >>> d1 = load_dataset("oscar", "unshuffled_deduplicated_en", split="train", streaming=True)
        >>> d2 = load_dataset("oscar", "unshuffled_deduplicated_fr", split="train", streaming=True)
        >>> dataset = interleave_datasets([d1, d2])
        >>> iterator = iter(dataset)
        >>> next(iterator)
        {'text': 'Mtendere Village was inspired by the vision...
        >>> next(iterator)
        {'text': "Média de débat d'idées, de culture...
    """
    from .arrow_dataset import Dataset
    from .iterable_dataset import IterableDataset

    if not datasets:
        raise ValueError("Unable to interleave an empty list of datasets.")
    iterable = isinstance(datasets[0], IterableDataset)
    map_style = isinstance(datasets[0], Dataset)
    if not (iterable ^ map_style):
        raise ValueError(
            f"Expected a list Dataset objects or a list of IterableDataset objects, but first element is a {type(datasets[0])}"
        )
    for dataset in datasets[1:]:
        if (map_style and not isinstance(dataset, Dataset)) or (iterable and not isinstance(dataset, IterableDataset)):
            raise ValueError(
                f"Unable to interleave a {type(datasets[0])} with a {type(dataset)}. Expected a list of Dataset objects or a list of IterableDataset objects."
            )
    if map_style:
        return _interleave_map_style_datasets(datasets, probabilities, seed)
    else:
        return _interleave_iterable_datasets(datasets, probabilities, seed)


def _interleave_map_style_datasets(
    datasets: List["Dataset"],
    probabilities: Optional[List[float]] = None,
    seed: Optional[int] = None,
    info: Optional[Any] = None,
    split: Optional[Any] = None,
    **kwargs,
) -> "Dataset":
    """
    Interleave several map-style datasets (sources) into a single map-style dataset.
    The new dataset is constructed by alternating between the sources to get the examples.
    If `probabilities = None` (default) the new dataset is constructed by cycling between each source to get the examples.
    If `probabilities` is not `None, the new dataset is constructed by getting examples from a random source at a time according to the provided probabilities.

    Args:
        datasets (:obj:`List[Dataset]`): list of datasets to interleave
        probabilities (:obj:`List[float]`, optional, default None): If specified, the new dataset is constructued by sampling
            examples from one source at a time according to these probabilities.
        seed (:obj:`int`, optional, default None): The random seed used to choose a source for each example.
        **kwargs: Keyword arguments to be passed to :meth:`datasets.Datasets.select` when selecting the indices used to interleave the datasets.

    Output:
        :class:`datasets.Dataset`
    """
    from .arrow_dataset import concatenate_datasets

    # To interleave the datasets, we concatenate them and then we re-order the indices
    concatenated_datasets = concatenate_datasets(datasets, info=info, split=split)

    # Let's now build the indices to pass to .select()
    lengths = [len(dset) for dset in datasets]
    offsets = np.cumsum([0] + lengths[:-1])
    if probabilities is None:
        # Example:: If lengths of the datasets are [3, 4, 5]
        # Then the resulting indices should be [0, 3, 7, 1, 4, 8, 2, 6, 9]
        # Note that we only have 3 examples per dataset since the first dataset ran out of examples
        indices = (offsets.reshape(1, -1) + np.arange(min(lengths)).reshape(-1, 1)).flatten().tolist()
    else:

        def iter_random_indices():
            """Get an infinite iterator that randomly samples the index of the source to pick examples from."""
            rng = np.random.default_rng(seed)
            while True:
                yield from (int(i) for i in rng.choice(len(datasets), size=1000, p=probabilities))

        current_index = [0] * len(datasets)
        indices = []
        for source_idx in iter_random_indices():
            # we ran out of examples, let's stop
            if current_index[source_idx] >= lengths[source_idx]:
                break
            # let's add the example at the current index of the `source_idx`-th dataset
            indices.append(current_index[source_idx] + offsets[source_idx])
            current_index[source_idx] += 1
    return concatenated_datasets.select(indices, **kwargs)


def _interleave_iterable_datasets(
    datasets: List["IterableDataset"],
    probabilities: Optional[List[float]] = None,
    seed: Optional[int] = None,
    info: Optional[Any] = None,
    split: Optional[Any] = None,
) -> "IterableDataset":
    """
    Interleave several iterable datasets (sources) into a single iterable dataset.
    The new iterable dataset alternates between the sources to yield examples.
    If `probabilities = None` (default) the iterable dataset will cycles through the sources in order for each next example in the iteration.
    If `probabilities` is not `None, the iterable dataset will sample a random source according to the provided probabilities for each next examples in the iteration.

    Args:
        datasets (:obj:`List[IterableDataset]`): list of datasets to interleave
        probabilities (:obj:`List[float]`, optional, default None): If specified, the new iterable dataset samples
            examples from one source at a time according to these probabilities.
        seed (:obj:`int`, optional, default None): The random seed used to choose a source for each example.

    Output:
        :class:`datasets.IterableDataset`
    """
    from .iterable_dataset import (
        CyclingMultiSourcesExamplesIterable,
        RandomlyCyclingMultiSourcesExamplesIterable,
        TypedExamplesIterable,
        iterable_dataset,
    )

    ex_iterables = [
        TypedExamplesIterable(d._ex_iterable, d.features)
        if not isinstance(d._ex_iterable, TypedExamplesIterable) and d.features is not None
        else d._ex_iterable
        for d in datasets
    ]
    # Use cycling or random cycling or sources
    if probabilities is None:
        ex_iterable = CyclingMultiSourcesExamplesIterable(ex_iterables)
    else:
        generator = np.random.default_rng(seed)
        ex_iterable = RandomlyCyclingMultiSourcesExamplesIterable(
            ex_iterables, generator=generator, probabilities=probabilities
        )
    # Set new info - we reset the features
    if info is None:
        info = DatasetInfo.from_merge([d.info for d in datasets])
        info.features = None
    # Return new daset
    return iterable_dataset(ex_iterable=ex_iterable, info=info, split=split)
