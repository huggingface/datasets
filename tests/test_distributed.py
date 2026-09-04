import os
import sys
from pathlib import Path

import pytest

from datasets import Dataset, IterableDataset
from datasets.distributed import split_dataset_by_node

from .utils import execute_subprocess_async, get_torch_dist_unique_port, require_torch


def test_split_dataset_by_node_map_style():
    full_ds = Dataset.from_dict({"i": range(17)})
    full_size = len(full_ds)
    world_size = 3
    datasets_per_rank = [
        split_dataset_by_node(full_ds, rank=rank, world_size=world_size) for rank in range(world_size)
    ]
    assert sum(len(ds) for ds in datasets_per_rank) == full_size
    assert len({tuple(x.values()) for ds in datasets_per_rank for x in ds}) == full_size


def test_split_dataset_by_node_map_style_with_examples_strategy():
    full_ds = Dataset.from_dict({"i": range(17)})

    with pytest.raises(ValueError, match="Map-style datasets only support strategy='auto'"):
        split_dataset_by_node(full_ds, rank=0, world_size=3, strategy="examples")


def test_split_dataset_by_node_invalid_strategy():
    full_ds = IterableDataset.from_generator(lambda: ({"i": i} for i in range(17)))

    with pytest.raises(ValueError, match="Invalid strategy"):
        split_dataset_by_node(full_ds, rank=0, world_size=3, strategy="invalid")


def test_split_dataset_by_node_iterable():
    def gen():
        return ({"i": i} for i in range(17))

    world_size = 3
    full_ds = IterableDataset.from_generator(gen)
    full_size = len(list(full_ds))
    datasets_per_rank = [
        split_dataset_by_node(full_ds, rank=rank, world_size=world_size) for rank in range(world_size)
    ]
    assert sum(len(list(ds)) for ds in datasets_per_rank) == full_size
    assert len({tuple(x.values()) for ds in datasets_per_rank for x in ds}) == full_size


@pytest.mark.parametrize("shards_per_node", [1, 2, 3])
def test_split_dataset_by_node_iterable_sharded(shards_per_node):
    def gen(shards):
        for shard in shards:
            yield from ({"i": i, "shard": shard} for i in range(17))

    world_size = 3
    num_shards = shards_per_node * world_size
    gen_kwargs = {"shards": [f"shard_{shard_idx}.txt" for shard_idx in range(num_shards)]}
    full_ds = IterableDataset.from_generator(gen, gen_kwargs=gen_kwargs)
    full_size = len(list(full_ds))
    assert full_ds.num_shards == world_size * shards_per_node
    datasets_per_rank = [
        split_dataset_by_node(full_ds, rank=rank, world_size=world_size) for rank in range(world_size)
    ]
    assert [ds.num_shards for ds in datasets_per_rank] == [shards_per_node] * world_size
    assert sum(len(list(ds)) for ds in datasets_per_rank) == full_size
    assert len({tuple(x.values()) for ds in datasets_per_rank for x in ds}) == full_size


def test_split_dataset_by_node_iterable_with_examples_strategy():
    def gen(shards):
        for shard in shards:
            yield from ({"i": 2 * shard + i} for i in range(2))

    world_size = 3
    full_ds = IterableDataset.from_generator(gen, gen_kwargs={"shards": list(range(6))})
    datasets_per_rank = [
        split_dataset_by_node(full_ds, rank=rank, world_size=world_size, strategy="examples")
        for rank in range(world_size)
    ]

    assert [ds.num_shards for ds in datasets_per_rank] == [full_ds.num_shards] * world_size
    assert [[example["i"] for example in ds] for ds in datasets_per_rank] == [
        list(range(rank, 12, world_size)) for rank in range(world_size)
    ]
    assert {example["i"] for ds in datasets_per_rank for example in ds} == set(range(12))


def test_split_dataset_by_node_iterable_with_shards_strategy():
    def gen(shards):
        yield from ({"shard": shard} for shard in shards)

    world_size = 3
    full_ds = IterableDataset.from_generator(gen, gen_kwargs={"shards": list(range(6))})
    datasets_per_rank = [
        split_dataset_by_node(full_ds, rank=rank, world_size=world_size, strategy="shards")
        for rank in range(world_size)
    ]
    shards_per_rank = [{example["shard"] for example in ds} for ds in datasets_per_rank]

    assert [ds.num_shards for ds in datasets_per_rank] == [2] * world_size
    assert all(shards_per_rank[rank].isdisjoint(shards_per_rank[other]) for rank in range(3) for other in range(rank))
    assert set.union(*shards_per_rank) == set(range(6))

    non_divisible_ds = IterableDataset.from_generator(gen, gen_kwargs={"shards": list(range(2))})
    with pytest.raises(ValueError, match="num_shards=2.*world_size=3"):
        split_dataset_by_node(non_divisible_ds, rank=0, world_size=world_size, strategy="shards")


def test_split_dataset_by_node_iterable_nested_strategy():
    full_ds = IterableDataset.from_generator(lambda: ({"i": i} for i in range(16)))
    ds = split_dataset_by_node(full_ds, rank=1, world_size=2, strategy="examples")
    nested_ds = split_dataset_by_node(ds, rank=0, world_size=2)

    assert [example["i"] for example in nested_ds] == list(range(2, 16, 4))
    same_ds = split_dataset_by_node(ds, rank=0, world_size=2, strategy="examples")
    assert [example["i"] for example in same_ds] == list(range(2, 16, 4))
    with pytest.raises(ValueError, match="Cannot change the strategy"):
        split_dataset_by_node(ds, rank=0, world_size=2, strategy="shards")


def test_split_dataset_by_node_iterable_shards_strategy_checked_at_iteration():
    """The shard count can change after the split; a forced "shards" split must fail clearly, not with IndexError."""

    def gen(shards):
        yield from ({"shard": shard} for shard in shards)

    full_ds = IterableDataset.from_generator(gen, gen_kwargs={"shards": list(range(6))})
    ds = split_dataset_by_node(full_ds, rank=1, world_size=3, strategy="shards")
    # shuffle() builds a dataset over a single shuffled source, which prepares the
    # iterable eagerly; the check fails there rather than mid-iteration.
    with pytest.raises(ValueError, match="num_shards=1.*world_size=3"):
        ds.shuffle(seed=0, buffer_size=4)


def test_split_dataset_by_node_iterable_distributed():
    def gen():
        return ({"i": i} for i in range(100))

    world_size = 3
    num_workers = 3
    full_ds = IterableDataset.from_generator(gen)
    full_size = len(list(full_ds))
    datasets_per_rank = [
        split_dataset_by_node(full_ds, rank=rank, world_size=world_size) for rank in range(world_size)
    ]
    datasets_per_rank_per_worker = [
        split_dataset_by_node(ds, rank=worker, world_size=num_workers)
        for ds in datasets_per_rank
        for worker in range(num_workers)
    ]
    assert sum(len(list(ds)) for ds in datasets_per_rank_per_worker) == full_size
    assert len({tuple(x.values()) for ds in datasets_per_rank_per_worker for x in ds}) == full_size


def test_distributed_shuffle_iterable():
    def gen():
        return ({"i": i} for i in range(17))

    world_size = 2
    full_ds = IterableDataset.from_generator(gen)
    full_size = len(list(full_ds))

    ds_rank0 = split_dataset_by_node(full_ds, rank=0, world_size=world_size).shuffle(seed=42)
    assert len(list(ds_rank0)) == 1 + full_size // world_size

    ds_rank0 = split_dataset_by_node(full_ds.shuffle(seed=42), rank=0, world_size=world_size)
    assert len(list(ds_rank0)) == 1 + full_size // world_size


@pytest.mark.parametrize("streaming", [False, True])
@require_torch
@pytest.mark.skipif(os.name == "nt", reason="execute_subprocess_async doesn't support windows")
@pytest.mark.integration
def test_torch_distributed_run(streaming):
    nproc_per_node = 2
    master_port = get_torch_dist_unique_port()
    test_script = Path(__file__).resolve().parent / "distributed_scripts" / "run_torch_distributed.py"
    distributed_args = f"""
        -m torch.distributed.run
        --nproc_per_node={nproc_per_node}
        --master_port={master_port}
        {test_script}
    """.split()
    args = f"""
        --streaming={streaming}
    """.split()
    cmd = [sys.executable] + distributed_args + args
    execute_subprocess_async(cmd, env=os.environ.copy())


@pytest.mark.parametrize(
    "nproc_per_node, num_workers",
    [
        (2, 2),  # each node has 2 shards and each worker has 1 shards
        (3, 2),  # each node uses all the shards but skips examples, and each worker has 2 shards
    ],
)
@require_torch
@pytest.mark.skipif(os.name == "nt", reason="execute_subprocess_async doesn't support windows")
@pytest.mark.integration
def test_torch_distributed_run_streaming_with_num_workers(nproc_per_node, num_workers):
    streaming = True
    master_port = get_torch_dist_unique_port()
    test_script = Path(__file__).resolve().parent / "distributed_scripts" / "run_torch_distributed.py"
    distributed_args = f"""
        -m torch.distributed.run
        --nproc_per_node={nproc_per_node}
        --master_port={master_port}
        {test_script}
    """.split()
    args = f"""
        --streaming={streaming}
        --num_workers={num_workers}
    """.split()
    cmd = [sys.executable] + distributed_args + args
    execute_subprocess_async(cmd, env=os.environ.copy())
