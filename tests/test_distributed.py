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


def test_split_dataset_by_node_iterable_force_sample_level_when_divisible():
    def gen(shards):
        for shard in shards:
            yield from ({"i": i, "shard": shard} for i in range(4))

    world_size = 2
    num_shards = 4  # divisible by world_size, so default behavior would be shard-level
    gen_kwargs = {"shards": [f"shard_{idx}.txt" for idx in range(num_shards)]}
    full_ds = IterableDataset.from_generator(gen, gen_kwargs=gen_kwargs)
    assert full_ds.num_shards == num_shards
    full_examples = list(full_ds)

    datasets_per_rank = [
        split_dataset_by_node(full_ds, rank=rank, world_size=world_size, force_sample_level=True)
        for rank in range(world_size)
    ]
    # When sample-level is forced, num_shards stays at the underlying value (StepExamplesIterable
    # does not collapse shards), and each rank receives the strided slice of examples.
    assert [ds.num_shards for ds in datasets_per_rank] == [num_shards] * world_size
    for rank, ds in enumerate(datasets_per_rank):
        expected = full_examples[rank::world_size]
        assert list(ds) == expected


def test_split_dataset_by_node_iterable_force_sample_level_before_map():
    world_size = 4
    num_examples = 24
    shards = [range(shard_idx * 6, (shard_idx + 1) * 6) for shard_idx in range(world_size)]

    for rank in range(world_size):
        counters = {"source": 0, "map": 0}

        def gen(shards):
            for shard in shards:
                for i in shard:
                    counters["source"] += 1
                    yield {"i": i}

        def counting_map(example):
            counters["map"] += 1
            return example

        ds = IterableDataset.from_generator(gen, gen_kwargs={"shards": shards})
        ds = split_dataset_by_node(ds, rank=rank, world_size=world_size, force_sample_level=True)
        ds = ds.map(counting_map)

        assert list(ds) == [{"i": i} for i in range(rank, num_examples, world_size)]
        # A sequential source must still be fully consumed, but transformations added after
        # split_dataset_by_node only run on this rank's examples.
        assert counters == {"source": num_examples, "map": num_examples // world_size}


def test_split_dataset_by_node_iterable_default_sample_level_remains_lazy():
    def gen():
        yield from ({"i": i} for i in range(10))

    world_size = 2
    full_ds = IterableDataset.from_generator(gen)

    taken = [split_dataset_by_node(full_ds, rank, world_size).take(3) for rank in range(world_size)]
    assert [list(ds) for ds in taken] == [[{"i": 0}, {"i": 2}], [{"i": 1}]]


def test_split_dataset_by_node_iterable_sample_level_before_filter():
    world_size = 4
    num_examples = 24
    shards = [range(shard_idx * 6, (shard_idx + 1) * 6) for shard_idx in range(world_size)]

    for rank in range(world_size):
        counters = {"source": 0, "filter": 0}

        def gen(shards):
            for shard in shards:
                for i in shard:
                    counters["source"] += 1
                    yield {"i": i}

        def counting_filter(example):
            counters["filter"] += 1
            return True

        ds = IterableDataset.from_generator(gen, gen_kwargs={"shards": shards})
        ds = split_dataset_by_node(ds, rank=rank, world_size=world_size, force_sample_level=True)
        ds = ds.filter(counting_filter)

        assert list(ds) == [{"i": i} for i in range(rank, num_examples, world_size)]
        assert counters == {"source": num_examples, "filter": num_examples // world_size}


def test_split_dataset_by_node_map_style_ignores_force_sample_level():
    full_ds = Dataset.from_dict({"i": range(17)})
    world_size = 3
    default = [split_dataset_by_node(full_ds, rank=rank, world_size=world_size) for rank in range(world_size)]
    with_flag = [
        split_dataset_by_node(full_ds, rank=rank, world_size=world_size, force_sample_level=True)
        for rank in range(world_size)
    ]
    for ds_default, ds_flag in zip(default, with_flag):
        assert list(ds_default) == list(ds_flag)


def test_split_dataset_by_node_iterable_force_sample_level_chaining():
    def gen():
        return ({"i": i} for i in range(60))

    world_size = 2
    num_workers = 3
    full_ds = IterableDataset.from_generator(gen)
    full_examples = list(full_ds)

    # Outer split sets the flag; inner split leaves it False and should inherit it.
    datasets_per_rank = [
        split_dataset_by_node(full_ds, rank=rank, world_size=world_size, force_sample_level=True)
        for rank in range(world_size)
    ]
    datasets_per_rank_per_worker = [
        split_dataset_by_node(ds, rank=worker, world_size=num_workers)
        for ds in datasets_per_rank
        for worker in range(num_workers)
    ]
    assert sum(len(list(ds)) for ds in datasets_per_rank_per_worker) == len(full_examples)
    assert len({tuple(x.values()) for ds in datasets_per_rank_per_worker for x in ds}) == len(full_examples)
    # Combined rank uses world_size * num_workers strides; verify rank 0/worker 0 sees indices 0, 6, 12, ...
    rank0_worker0 = list(datasets_per_rank_per_worker[0])
    assert rank0_worker0 == full_examples[0 :: world_size * num_workers]


def test_split_dataset_by_node_iterable_force_sample_level_after_shard_level_split():
    def gen(shards):
        for shard in shards:
            yield from ({"i": i, "shard": shard} for i in range(4))

    num_nodes = 2
    num_workers = 2
    shards = [f"shard_{idx}.txt" for idx in range(4)]
    full_ds = IterableDataset.from_generator(gen, gen_kwargs={"shards": shards})

    for node_rank in range(num_nodes):
        node_ds = split_dataset_by_node(full_ds, rank=node_rank, world_size=num_nodes)
        node_examples = [
            {"i": i, "shard": shard}
            for shard_idx, shard in enumerate(shards)
            if shard_idx % num_nodes == node_rank
            for i in range(4)
        ]
        for worker_rank in range(num_workers):
            worker_ds = split_dataset_by_node(
                node_ds, rank=worker_rank, world_size=num_workers, force_sample_level=True
            )
            assert list(worker_ds) == node_examples[worker_rank::num_workers]


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
