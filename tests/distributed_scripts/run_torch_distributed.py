import os
from argparse import ArgumentParser
from typing import List

import torch.utils.data

from datasets import Dataset, IterableDataset
from datasets.distributed import split_dataset_by_node


NUM_SHARDS = 4
NUM_ITEMS_PER_SHARD = 3


class FailedTestError(RuntimeError):
    pass


def gen(shards: List[str]):
    for shard in shards:
        for i in range(NUM_ITEMS_PER_SHARD):
            yield {"i": i, "shard": shard}


def main():
    rank = int(os.environ["RANK"])
    world_size = int(os.environ["WORLD_SIZE"])

    parser = ArgumentParser()
    parser.add_argument("--streaming", type=bool)
    parser.add_argument("--local_rank", type=int)
    parser.add_argument("--num_workers", type=int, default=0)
    args = parser.parse_args()
    streaming = args.streaming
    num_workers = args.num_workers

    gen_kwargs = {"shards": [f"shard_{shard_idx}" for shard_idx in range(NUM_SHARDS)]}
    ds = IterableDataset.from_generator(gen, gen_kwargs=gen_kwargs)
    if not streaming:
        ds = Dataset.from_list(list(ds))

    ds = split_dataset_by_node(ds, rank=rank, world_size=world_size)
    dataloader = torch.utils.data.DataLoader(ds, num_workers=num_workers)

    full_size = NUM_SHARDS * NUM_ITEMS_PER_SHARD
    expected_local_size = full_size // world_size
    expected_local_size += int(rank < (full_size % world_size))

    local_size = sum(1 for _ in dataloader)
    if local_size != expected_local_size:
        raise FailedTestError(f"local_size {local_size} != expected_local_size {expected_local_size}")


if __name__ == "__main__":
    main()
