import numpy as np
import pyarrow as pa
import pytest
from pyiceberg.catalog.sql import SqlCatalog
from pyiceberg.schema import Schema
from pyiceberg.types import DoubleType, FloatType, ListType, LongType, NestedField, StringType

from datasets import IterableDataset, load_dataset


@pytest.fixture
def catalog(tmp_path):
    cat = SqlCatalog(
        "test_catalog",
        **{
            "uri": f"sqlite:///{tmp_path}/catalog.db",
            "warehouse": str(tmp_path / "warehouse"),
        },
    )
    cat.create_namespace("test_db")
    return cat


@pytest.fixture
def sample_table(catalog):
    schema = Schema(
        NestedField(1, "id", LongType()),
        NestedField(2, "name", StringType()),
        NestedField(3, "value", DoubleType()),
        NestedField(4, "vector", ListType(element_id=5, element_type=FloatType(), element_required=False)),
    )
    table = catalog.create_table("test_db.sample", schema=schema)
    table.append(
        pa.table(
            {
                "id": pa.array([1, 2, 3], type=pa.int64()),
                "name": pa.array(["alice", "bob", "carol"], type=pa.large_string()),
                "value": pa.array([1.1, 2.2, 3.3], type=pa.float64()),
                "vector": pa.FixedSizeListArray.from_arrays(pa.array([0.1] * 12, pa.float32()), list_size=4),
            }
        )
    )
    return table


def test_load_iceberg_basic(catalog, sample_table):
    ds = load_dataset("iceberg", catalog=catalog, table="test_db.sample")
    assert "train" in ds
    dataset = ds["train"]
    assert dataset.num_rows == 3
    assert "id" in dataset.column_names
    assert "name" in dataset.column_names
    assert "value" in dataset.column_names
    assert "vector" in dataset.column_names
    assert list(dataset["id"]) == [1, 2, 3]
    assert list(dataset["name"]) == ["alice", "bob", "carol"]


def test_load_vectors(catalog, sample_table):
    ds = load_dataset("iceberg", catalog=catalog, table="test_db.sample", columns=["vector"])
    dataset = ds["train"]
    assert "vector" in dataset.column_names
    vectors = dataset.data["vector"].combine_chunks().values.to_numpy(zero_copy_only=False)
    assert np.allclose(vectors, np.full(12, 0.1), atol=1e-6)


def test_load_iceberg_columns(catalog, sample_table):
    ds = load_dataset("iceberg", catalog=catalog, table="test_db.sample", columns=["id", "name"])
    dataset = ds["train"]
    assert "id" in dataset.column_names
    assert "name" in dataset.column_names
    assert "value" not in dataset.column_names


def test_load_iceberg_filters(catalog, sample_table):
    ds = load_dataset("iceberg", catalog=catalog, table="test_db.sample", filters="value > 2.0")
    dataset = ds["train"]
    assert dataset.num_rows == 2
    assert list(dataset["name"]) == ["bob", "carol"]


def test_load_iceberg_multi_split(catalog):
    schema = Schema(
        NestedField(1, "x", LongType()),
    )
    train_table = catalog.create_table("test_db.train_split", schema=schema)
    train_table.append(pa.table({"x": pa.array([1, 2, 3], type=pa.int64())}))

    test_table = catalog.create_table("test_db.test_split", schema=schema)
    test_table.append(pa.table({"x": pa.array([10, 20], type=pa.int64())}))

    ds = load_dataset(
        "iceberg",
        catalog=catalog,
        table={"train": "test_db.train_split", "test": "test_db.test_split"},
    )
    assert "train" in ds
    assert "test" in ds
    assert ds["train"].num_rows == 3
    assert ds["test"].num_rows == 2


@pytest.mark.parametrize("streaming", [False, True])
def test_load_iceberg_streaming(catalog, sample_table, streaming):
    ds = load_dataset("iceberg", catalog=catalog, table="test_db.sample", split="train", streaming=streaming)
    if streaming:
        assert isinstance(ds, IterableDataset)
    items = list(ds)
    assert len(items) == 3
    assert all("id" in item for item in items)


def test_load_iceberg_snapshot(catalog):
    schema = Schema(
        NestedField(1, "id", LongType()),
    )
    table = catalog.create_table("test_db.versioned", schema=schema)
    table.append(pa.table({"id": pa.array([1, 2], type=pa.int64())}))

    # Capture snapshot after first append
    first_snapshot_id = table.current_snapshot().snapshot_id

    # Append more data
    table.append(pa.table({"id": pa.array([3, 4, 5], type=pa.int64())}))

    # Load at latest: should have 5 rows
    ds_latest = load_dataset("iceberg", catalog=catalog, table="test_db.versioned")
    assert ds_latest["train"].num_rows == 5

    # Load at first snapshot: should have 2 rows
    ds_old = load_dataset("iceberg", catalog=catalog, table="test_db.versioned", snapshot_id=first_snapshot_id)
    assert ds_old["train"].num_rows == 2


def test_load_iceberg_num_proc(catalog):
    """Test that num_proc > 1 works for parallel processing."""
    schema = Schema(
        NestedField(1, "id", LongType()),
    )
    table = catalog.create_table("test_db.parallel", schema=schema)
    table.append(pa.table({"id": pa.array([1, 2, 3], type=pa.int64())}))
    table.append(pa.table({"id": pa.array([4, 5, 6], type=pa.int64())}))

    ds = load_dataset("iceberg", catalog=catalog, table="test_db.parallel", num_proc=2)
    dataset = ds["train"]
    assert dataset.num_rows == 6
    assert sorted(dataset["id"]) == [1, 2, 3, 4, 5, 6]


def test_load_iceberg_missing_catalog_raises():
    with pytest.raises(ValueError, match="catalog"):
        load_dataset("iceberg", catalog=None, table="db.table")


def test_load_iceberg_missing_table_raises(catalog):
    with pytest.raises(ValueError, match="table"):
        load_dataset("iceberg", catalog=catalog, table=None)
