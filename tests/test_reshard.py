import csv
import json

import pytest

from datasets import load_dataset


@pytest.fixture(scope="session")
def csv_path_big(tmp_path_factory):
    """Create a CSV file with multiple lines for resharding testing"""
    path = str(tmp_path_factory.mktemp("data") / "dataset_reshard.csv")
    data = [{"id": i, "text": f"text {i}", "label": i % 2} for i in range(100)]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "text", "label"])
        writer.writeheader()
        for item in data:
            writer.writerow(item)
    return path


@pytest.fixture(scope="session")
def csv_path_small(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("data") / "dataset_small.csv")
    data = [{"id": i, "text": f"text {i}"} for i in range(5)]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "text"])
        writer.writeheader()
        for item in data:
            writer.writerow(item)
    return path


@pytest.fixture(scope="session")
def jsonl_path_big(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("data") / "dataset_reshard.jsonl")
    data = [{"id": i, "text": f"text {i}", "label": i % 2} for i in range(100)]
    with open(path, "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
    return path


@pytest.fixture(scope="session")
def jsonl_path_small(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("data") / "dataset_small.jsonl")
    data = [{"id": i, "text": f"text {i}"} for i in range(5)]
    with open(path, "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
    return path


@pytest.fixture(scope="session")
def parquet_path_multiple_rowgroups(tmp_path_factory):
    import pyarrow as pa
    import pyarrow.parquet as pq

    path = str(tmp_path_factory.mktemp("data") / "dataset_reshard.parquet")
    schema = pa.schema(
        {
            "id": pa.int64(),
            "text": pa.string(),
            "label": pa.int64(),
        }
    )

    data = {
        "id": list(range(100)),
        "text": [f"text {i}" for i in range(100)],
        "label": [i % 2 for i in range(100)],
    }

    with open(path, "wb") as f:
        writer = pq.ParquetWriter(f, schema=schema)
        # Write in multiple row groups to test resharding
        for i in range(0, 100, 10):
            table = pa.Table.from_pydict({k: v[i : i + 10] for k, v in data.items()}, schema=schema)
            writer.write_table(table)
        writer.close()
    return path


def test_reshard_jsonl_basic(jsonl_path_big):
    ds = load_dataset("json", data_files=jsonl_path_big, streaming=True)
    original_num_shards = ds["train"].num_shards
    print(f"Original num of shards: {original_num_shards}")
    # Reshard to maximum possible shards
    resharded_ds = ds["train"].reshard()
    assert resharded_ds.num_shards >= original_num_shards

    # Reshard to a specific number of shards
    target_shards = 10
    resharded_ds_specific = ds["train"].reshard(num_shards=target_shards)
    assert resharded_ds_specific.num_shards == target_shards

    origin_ids = [item["id"] for item in ds["train"]]
    resharded_ids = [item["id"] for item in resharded_ds]
    resharded_specific_ids = [item["id"] for item in resharded_ds_specific]
    assert origin_ids == resharded_ids
    assert resharded_ids == resharded_specific_ids


def test_reshard_parquet_basic(parquet_path_multiple_rowgroups):
    ds = load_dataset("parquet", data_files=parquet_path_multiple_rowgroups, streaming=True)
    original_num_shards = ds["train"].num_shards

    # Reshard to maximum possible shards (should split by row groups)
    resharded_ds = ds["train"].reshard()
    assert resharded_ds.num_shards >= original_num_shards

    # Reshard to a specific number of shards
    target_shards = 5
    resharded_ds_specific = ds["train"].reshard(num_shards=target_shards)
    assert resharded_ds_specific.num_shards == target_shards

    origin_ids = [item["id"] for item in ds["train"]]
    resharded_ids = [item["id"] for item in resharded_ds]
    resharded_specific_ids = [item["id"] for item in resharded_ds_specific]
    assert origin_ids == resharded_ids
    assert resharded_ids == resharded_specific_ids


def test_reshard_csv_basic(csv_path_big):
    ds = load_dataset("csv", data_files=csv_path_big, streaming=True)
    original_num_shards = ds["train"].num_shards

    # Reshard to maximum possible shards
    resharded_ds = ds["train"].reshard()
    assert resharded_ds.num_shards >= original_num_shards

    # Reshard to a specific number of shards
    target_shards = 10
    resharded_ds_specific = ds["train"].reshard(num_shards=target_shards)
    assert resharded_ds_specific.num_shards == target_shards

    origin_ids = [item["id"] for item in ds["train"]]
    resharded_ids = [item["id"] for item in resharded_ds]
    resharded_specific_ids = [item["id"] for item in resharded_ds_specific]
    assert origin_ids == resharded_ids
    assert resharded_ids == resharded_specific_ids


def test_reshard_csv_boundary_case(csv_path_small):
    """Test reshard with CSV dataset smaller than num_shards"""
    # Load the small dataset
    ds = load_dataset("csv", data_files=csv_path_small, streaming=True)
    # Try to reshard to more shards than data items
    target_shards = 10
    resharded_ds = ds["train"].reshard(num_shards=target_shards)
    origin_ids = [item["id"] for item in ds["train"]]
    resharded_ids = [item["id"] for item in resharded_ds]
    assert origin_ids == resharded_ids
    assert resharded_ds.num_shards == target_shards


def test_reshard_jsonl_boundary_case(jsonl_path_small):
    ds = load_dataset("json", data_files=jsonl_path_small, streaming=True)
    target_shards = 10
    resharded_ds = ds["train"].reshard(num_shards=target_shards)
    assert resharded_ds.num_shards == 10
    origin_ids = [item["id"] for item in ds["train"]]
    resharded_ids = [item["id"] for item in resharded_ds]
    assert origin_ids == resharded_ids
    assert resharded_ds.num_shards == target_shards


def test_reshard_pipeline(jsonl_path_big):
    ds = load_dataset("json", data_files=jsonl_path_big, streaming=True)
    resharded_ds = ds["train"].reshard(num_shards=10)
    filtered_ds = resharded_ds.filter(lambda x: x["label"] == 1)
    batched_ds = filtered_ds.batch(32)
    # Verify the dataset is still iterable
    batch = next(iter(batched_ds))
    assert "id" in batch
    assert "text" in batch
    assert "label" in batch
