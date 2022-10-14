from typing import List, Optional, TypeVar

from .arrow_dataset import Dataset, _concatenate_map_style_datasets, _interleave_map_style_datasets
from .info import DatasetInfo
from .iterable_dataset import IterableDataset, _concatenate_iterable_datasets, _interleave_iterable_datasets
from .splits import NamedSplit
from .utils import logging


logger = logging.get_logger(__name__)


DatasetType = TypeVar("DatasetType", "Dataset", "IterableDataset")


def interleave_datasets(
    datasets: List[DatasetType],
    probabilities: Optional[List[float]] = None,
    seed: Optional[int] = None,
    info: Optional[DatasetInfo] = None,
    split: Optional[NamedSplit] = None,
    stopping_strategy: Optional[str] = "first_exhausted",
) -> DatasetType:
    """
    Interleave several datasets (sources) into a single dataset.
    The new dataset is constructed by alternating between the sources to get the examples.

    You can use this function on a list of :class:`Dataset` objects, or on a list of :class:`IterableDataset` objects.

    If ``probabilities`` is ``None`` (default) the new dataset is constructed by cycling between each source to get the examples.
    If ``probabilities`` is not ``None``, the new dataset is constructed by getting examples from a random source at a time according to the provided probabilities.

    The resulting dataset ends when one of the source datasets runs out of examples except when ``oversampling`` is ``True``,
    in which case, the resulting dataset ends when all datasets have ran out of examples at least one time.

    Args:
        datasets (:obj:`List[Dataset]` or :obj:`List[IterableDataset]`): list of datasets to interleave
        probabilities (:obj:`List[float]`, optional, default None): If specified, the new dataset is constructed by sampling
            examples from one source at a time according to these probabilities.
        seed (:obj:`int`, optional, default None): The random seed used to choose a source for each example.
        info ([`DatasetInfo`], *optional*): Dataset information, like description, citation, etc.
            <Added version="2.4.0"/>
        split ([`NamedSplit`], *optional*): Name of the dataset split.
            <Added version="2.4.0"/>
        stopping_strategy (Optional :obj:`str`, defaults to `first_exhausted`):
            Two strategies are proposed right now, `first_exhausted` and `all_exhausted`.
            By default, `first_exhausted` is an undersampling strategy, i.e the dataset construction is stopped as soon as one dataset has ran out of samples.
            If the strategy is `all_exhausted`,  we use an oversampling strategy, i.e the dataset construction is stopped as soon as every samples of every dataset has been added at least once.
            Note that if the strategy is `all_exhausted`, the interleaved dataset size can get enormous:
            - with no probabilities, the resulting dataset will have max_length_datasets*nb_dataset samples.
            - with given probabilities, the resulting dataset will have more samples if some datasets have really low probability of visiting.
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
        >>> dataset = interleave_datasets([d1, d2, d3], probabilities=[0.7, 0.2, 0.1], seed=42, stopping_strategy="all_exhausted")
        >>> dataset["a"]
        [10, 0, 11, 1, 2, 20, 12, 10, 0, 1, 2, 21, 0, 11, 1, 2, 0, 1, 12, 2, 10, 0, 22]
        >>> dataset = interleave_datasets([d1, d2, d3], probabilities=[0.7, 0.2, 0.1], seed=42)
        >>> dataset["a"]
        [10, 0, 11, 1, 2]
        >>> dataset = interleave_datasets([d1, d2, d3])
        >>> dataset["a"]
        [0, 10, 20, 1, 11, 21, 2, 12, 22]
        >>> dataset = interleave_datasets([d1, d2, d3], stopping_strategy="all_exhausted")
        >>> dataset["a"]
        [0, 10, 20, 1, 11, 21, 2, 12, 22]
        >>> d1 = Dataset.from_dict({"a": [0, 1, 2]})
        >>> d2 = Dataset.from_dict({"a": [10, 11, 12, 13]})
        >>> d3 = Dataset.from_dict({"a": [20, 21, 22, 23, 24]})
        >>> dataset = interleave_datasets([d1, d2, d3])
        >>> dataset["a"]
        [0, 10, 20, 1, 11, 21, 2, 12, 22]
        >>> dataset = interleave_datasets([d1, d2, d3], stopping_strategy="all_exhausted")
        >>> dataset["a"]
        [0, 10, 20, 1, 11, 21, 2, 12, 22, 0, 13, 23, 1, 0, 24]
        >>> dataset = interleave_datasets([d1, d2, d3], probabilities=[0.7, 0.2, 0.1], seed=42)
        >>> dataset["a"]
        [10, 0, 11, 1, 2]
        >>> dataset = interleave_datasets([d1, d2, d3], probabilities=[0.7, 0.2, 0.1], seed=42, stopping_strategy="all_exhausted")
        >>> dataset["a"]
        [10, 0, 11, 1, 2, 20, 12, 13, ..., 0, 1, 2, 0, 24]
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
            f"Expected a list of Dataset objects or a list of IterableDataset objects, but first element is a {type(datasets[0])}"
        )
    for dataset in datasets[1:]:
        if (map_style and not isinstance(dataset, Dataset)) or (iterable and not isinstance(dataset, IterableDataset)):
            raise ValueError(
                f"Unable to interleave a {type(datasets[0])} with a {type(dataset)}. Expected a list of Dataset objects or a list of IterableDataset objects."
            )
    if stopping_strategy not in ["first_exhausted", "all_exhausted"]:
        raise ValueError(f"{stopping_strategy} is not supported. Please enter a valid stopping_strategy.")
    if map_style:
        return _interleave_map_style_datasets(
            datasets, probabilities, seed, info=info, split=split, stopping_strategy=stopping_strategy
        )
    else:
        return _interleave_iterable_datasets(
            datasets, probabilities, seed, info=info, split=split, stopping_strategy=stopping_strategy
        )


def concatenate_datasets(
    dsets: List[Dataset],
    info: Optional[DatasetInfo] = None,
    split: Optional[NamedSplit] = None,
    axis: int = 0,
):
    """
    Converts a list of :class:`Dataset` with the same schema into a single :class:`Dataset`.

    Args:
        dsets (:obj:`List[datasets.Dataset]`): List of Datasets to concatenate.
        info (:class:`DatasetInfo`, optional): Dataset information, like description, citation, etc.
        split (:class:`NamedSplit`, optional): Name of the dataset split.
        axis (``{0, 1}``, default ``0``, meaning over rows):
            Axis to concatenate over, where ``0`` means over rows (vertically) and ``1`` means over columns
            (horizontally).

            *New in version 1.6.0*

    Example:

    ```py
    >>> ds3 = concatenate_datasets([ds1, ds2])
    ```
    """

    if not dsets:
        raise ValueError("Unable to concatenate an empty list of datasets.")
    iterable = isinstance(dsets[0], IterableDataset)
    map_style = isinstance(dsets[0], Dataset)
    if not (iterable ^ map_style):
        raise ValueError(
            f"Expected a list of Dataset objects or a list of IterableDataset objects, but first element is a {type(dsets[0])}"
        )
    for dataset in dsets[1:]:
        if (map_style and not isinstance(dataset, Dataset)) or (iterable and not isinstance(dataset, IterableDataset)):
            raise ValueError(
                f"Unable to concatenate a {type(dsets[0])} with a {type(dataset)}. Expected a list of Dataset objects or a list of IterableDataset objects."
            )
    if map_style:
        return _concatenate_map_style_datasets(dsets, info=info, split=split, axis=axis)
    else:
        return _concatenate_iterable_datasets(dsets, info=info, split=split, axis=axis)
