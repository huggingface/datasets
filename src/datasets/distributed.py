from typing import Literal, TypeVar

from .arrow_dataset import Dataset, _split_by_node_map_style_dataset
from .iterable_dataset import IterableDataset, _split_by_node_iterable_dataset


DatasetType = TypeVar("DatasetType", Dataset, IterableDataset)


def split_dataset_by_node(
    dataset: DatasetType, rank: int, world_size: int, strategy: Literal["auto", "shards", "examples"] = "auto"
) -> DatasetType:
    """
    Split a dataset for the node at rank `rank` in a pool of nodes of size `world_size`.

    For map-style datasets:

    Each node is assigned a chunk of data, e.g. rank 0 is given the first chunk of the dataset.
    To maximize data loading throughput, chunks are made of contiguous data on disk if possible.

    For iterable datasets:

    The splitting `strategy` can be `"auto"`, `"shards"`, or `"examples"`. The default `"auto"` assigns shards
    when the number of shards is divisible by `world_size` and otherwise assigns every `world_size`-th example.
    `"shards"` always assigns shards and requires divisibility, while `"examples"` always assigns examples.

    > [!WARNING]
    > If you shuffle your iterable dataset in a distributed setup, make sure to set a fixed `seed` in [`IterableDataset.shuffle`]
    so the same shuffled list of shards is used on every node to know which shards the node should skip.

    Args:
        dataset ([`Dataset`] or [`IterableDataset`]):
            The dataset to split by node.
        rank (`int`):
            Rank of the current node.
        world_size (`int`):
            Total number of nodes.
        strategy (`str`, defaults to `"auto"`):
            How to split an iterable dataset. Must be one of `"auto"`, `"shards"`, or `"examples"`.
            Map-style datasets only support `"auto"`.

    Returns:
        [`Dataset`] or [`IterableDataset`]: The dataset to be used on the node at rank `rank`.
    """
    if strategy not in {"auto", "shards", "examples"}:
        raise ValueError(f"Invalid strategy {strategy!r}. Expected one of 'auto', 'shards', or 'examples'.")
    if isinstance(dataset, Dataset):
        if strategy != "auto":
            raise ValueError(f"Map-style datasets only support strategy='auto', but got strategy={strategy!r}.")
        return _split_by_node_map_style_dataset(dataset, rank=rank, world_size=world_size)
    else:
        return _split_by_node_iterable_dataset(dataset, rank=rank, world_size=world_size, strategy=strategy)
