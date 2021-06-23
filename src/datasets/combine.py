from typing import TYPE_CHECKING, List, Optional

from .info import DatasetInfo


if TYPE_CHECKING:
    from .iterable_dataset import IterableDataset


def interleave_datasets(
    datasets: List["IterableDataset"], probabilities: Optional[List[float]] = None, seed: Optional[int] = None
) -> "IterableDataset":
    """
    Interleave several iterable datasets (sources) into a single iterable dataset.
    The new iterable dataset alternates between the sources to yield examples.
    If `probabilities = None` (default) the iterable dataset will cycles through the sources
    in order for each next example in the iteration.
    If `probabilities` is not `None, the iterable dataset will sample a random source according
    to the provided probabilities for each next examples in the iteration.

    Args:
        datasets (:obj:`List[IterableDataset]`): list of datasets to merge
        probabilities (:obj:`List[float]`, optional, default None): If specified, the new iterable datasets will sample
            examples from one source at a time according to these probabilities.
        seed (:obj:`int`, optional, default None): The random seed used to choose a source for each example to yield.
    """
    from .iterable_dataset import (
        CyclingMultiSourcesExamplesIterable,
        MappedExamplesIterable,
        RandomlyCyclingMultiSourcesExamplesIterable,
        iterable_dataset,
    )

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
