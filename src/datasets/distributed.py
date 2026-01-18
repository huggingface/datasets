from typing import Literal, TypeVar

from .arrow_dataset import Dataset, _split_by_node_map_style_dataset
from .iterable_dataset import IterableDataset, _split_by_node_iterable_dataset


DatasetType = TypeVar("DatasetType", Dataset, IterableDataset)


def split_dataset_by_node(
    dataset: DatasetType,
    rank: int,
    world_size: int,
    stopping_strategy: Literal["first_exhausted", "all_exhausted"] = "first_exhausted",
) -> DatasetType:
    """
    Split a dataset for the node at rank `rank` in a pool of nodes of size `world_size`, with each
    rank having the same number of examples thanks to the `stopping_strategy`.

    The stopping strategy allows each node to have the same number of examples:

    - "first_exhausted": stop when the first node runs of of data, and discard the extra data in the other nodes
    - "all_exhausted": stop when the last node runs out of data, and other nodes may reuse their data to compensate

    For map-style datasets:

    Each node is assigned a chunk of data, e.g. rank 0 is given the first chunk of the dataset.
    To maximize data loading throughput, chunks are made of contiguous data on disk if possible.
    This doesn't need communication between nodes, since each node knows how many examples
    are available and can discard or reuse up to one example accordingly.

    For iterable datasets:

    The shards are evenly assigned across the nodes.
    To maximize data loading throughput, each nodes has its own data and there is no overlap between nodes.
    The stopping strategy has less impact at the end of training if the dataset has a number of shards that is
    a factor of `world_size` (e.g. if `dataset.num_shards % world_size == 0`), since each node has roughly
    the same amount of data available. Nodes communicate using torch distributed to decide when to stop.

    Args:
        dataset ([`Dataset`] or [`IterableDataset`]):
            The dataset to split by node.
        rank (`int`):
            Rank of the current node.
        world_size (`int`):
            Total number of nodes.

    Returns:
        [`Dataset`] or [`IterableDataset`]: The dataset to be used on the node at rank `rank`.
    """
    if isinstance(dataset, Dataset):
        return _split_by_node_map_style_dataset(
            dataset, rank=rank, world_size=world_size, stopping_strategy=stopping_strategy
        )
    else:
        return _split_by_node_iterable_dataset(
            dataset, rank=rank, world_size=world_size, stopping_strategy=stopping_strategy
        )
