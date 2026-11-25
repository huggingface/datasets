import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from datasets import (
    Dataset,
    DatasetDict,
    IterableDataset,
    IterableDatasetDict,
    concatenate_datasets,
    interleave_datasets,
    load_dataset,
    load_from_disk,
)

from .utils import push_parquet_shards_offline


def _dataset():
    return Dataset.from_dict({"a": [1, 2, 3], "b": ["x", "y", "z"], "c": [0.5, 1.5, 2.5]})


def test_with_column_metadata():
    ds = _dataset()
    new_ds = ds.with_column_metadata({"a": {"unit": "cm"}, "b": {"source": "manual"}})
    assert new_ds.info.column_metadata == {"a": {"unit": "cm"}, "b": {"source": "manual"}}
    assert ds.info.column_metadata is None
    assert new_ds["a"][:] == [1, 2, 3]
    # replaces the metadata of the given columns, and an empty dict removes it
    newer_ds = new_ds.with_column_metadata({"a": {"unit": "m"}, "b": {}})
    assert newer_ds.info.column_metadata == {"a": {"unit": "m"}}
    assert new_ds.info.column_metadata == {"a": {"unit": "cm"}, "b": {"source": "manual"}}


@pytest.mark.parametrize(
    "column_metadata, error",
    [
        ({"d": {"unit": "cm"}}, ValueError),
        ({"a": {"unit": 1}}, TypeError),
        ({"a": {1: "cm"}}, TypeError),
        ({"a": "cm"}, TypeError),
    ],
)
def test_with_column_metadata_rejects_invalid_metadata(column_metadata, error):
    with pytest.raises(error):
        _dataset().with_column_metadata(column_metadata)


def test_column_metadata_follows_column_operations():
    ds = _dataset().with_column_metadata({"a": {"unit": "cm"}, "b": {"source": "manual"}})
    assert ds.rename_column("a", "d").info.column_metadata == {"d": {"unit": "cm"}, "b": {"source": "manual"}}
    assert ds.rename_columns({"a": "d", "b": "e"}).info.column_metadata == {
        "d": {"unit": "cm"},
        "e": {"source": "manual"},
    }
    assert ds.remove_columns("a").info.column_metadata == {"b": {"source": "manual"}}
    assert ds.select_columns(["a", "c"]).info.column_metadata == {"a": {"unit": "cm"}}
    assert ds.map(lambda x: {"d": x["a"] * 2}).info.column_metadata == {"a": {"unit": "cm"}, "b": {"source": "manual"}}
    assert ds.map(lambda x: {"d": x["a"]}, remove_columns=["a"]).info.column_metadata == {"b": {"source": "manual"}}
    for transformed in [ds.filter(lambda x: x["a"] > 1), ds.select([2, 0]), ds.shuffle(seed=0), ds.sort("c")]:
        assert transformed.info.column_metadata == {"a": {"unit": "cm"}, "b": {"source": "manual"}}
    # a new column with the name of a removed one doesn't get the old metadata
    assert ds.remove_columns("a").add_column("a", [0, 0, 0]).info.column_metadata == {"b": {"source": "manual"}}


def test_column_metadata_concatenate_datasets():
    ds1 = _dataset().with_column_metadata({"a": {"unit": "cm"}, "b": {"source": "manual"}})
    ds2 = _dataset().with_column_metadata({"a": {"unit": "cm"}, "b": {"source": "scraped"}})
    # metadata that differs between the datasets is dropped
    assert concatenate_datasets([ds1, ds2]).info.column_metadata == {"a": {"unit": "cm"}}
    other = Dataset.from_dict({"d": [1, 2, 3]}).with_column_metadata({"d": {"unit": "kg"}})
    assert concatenate_datasets([ds1, other], axis=1).info.column_metadata == {
        "a": {"unit": "cm"},
        "b": {"source": "manual"},
        "d": {"unit": "kg"},
    }


def test_column_metadata_save_to_disk(tmp_path):
    ds = _dataset().with_column_metadata({"a": {"unit": "cm"}})
    ds.save_to_disk(str(tmp_path / "ds"))
    assert load_from_disk(str(tmp_path / "ds")).info.column_metadata == {"a": {"unit": "cm"}}


def test_column_metadata_to_parquet_and_back(tmp_path):
    ds = _dataset().with_column_metadata({"a": {"unit": "cm"}, "b": {"source": "manual"}})
    path = str(tmp_path / "data.parquet")
    ds.to_parquet(path)
    schema = pq.read_schema(path)
    assert schema.field("a").metadata == {b"unit": b"cm"}
    assert schema.field("b").metadata == {b"source": b"manual"}
    assert schema.field("c").metadata is None
    assert Dataset.from_parquet(path, cache_dir=str(tmp_path / "cache")).info.column_metadata == {
        "a": {"unit": "cm"},
        "b": {"source": "manual"},
    }
    streamed = load_dataset("parquet", data_files=path, split="train", streaming=True)
    assert streamed.info.column_metadata == {"a": {"unit": "cm"}, "b": {"source": "manual"}}


def test_dataset_dict_with_column_metadata():
    dsets = DatasetDict(train=_dataset(), test=_dataset())
    dsets = dsets.with_column_metadata({"a": {"unit": "cm"}})
    assert {split: ds.info.column_metadata for split, ds in dsets.items()} == {
        "train": {"a": {"unit": "cm"}},
        "test": {"a": {"unit": "cm"}},
    }


def test_column_metadata_ignores_arrow_and_parquet_field_metadata(tmp_path):
    schema = pa.schema(
        [
            pa.field("a", pa.int64(), metadata={"PARQUET:field_id": "1", "unit": "cm"}),
            pa.field("b", pa.string(), metadata={"PARQUET:field_id": "2"}),
        ]
    )
    path = str(tmp_path / "data.parquet")
    pq.write_table(pa.table({"a": [1], "b": ["x"]}, schema=schema), path)
    ds = load_dataset("parquet", data_files=path, split="train", cache_dir=str(tmp_path / "cache"))
    assert ds.info.column_metadata == {"a": {"unit": "cm"}}


def test_column_metadata_push_to_hub_shards(offline_parquet_uploads):
    ds = _dataset().with_column_metadata({"a": {"unit": "cm"}})
    push_parquet_shards_offline(ds, num_shards=2)
    files = sorted(offline_parquet_uploads.glob("*.parquet"))
    assert len(files) == 2
    assert all(pq.read_schema(file).field("a").metadata == {b"unit": b"cm"} for file in files)


def _iterable_dataset(num_shards=1):
    return _dataset().to_iterable_dataset(num_shards=num_shards)


def test_iterable_dataset_with_column_metadata():
    ds = _iterable_dataset()
    new_ds = ds.with_column_metadata({"a": {"unit": "cm"}, "b": {"source": "manual"}})
    assert new_ds.info.column_metadata == {"a": {"unit": "cm"}, "b": {"source": "manual"}}
    assert ds.info.column_metadata is None
    assert [row["a"] for row in new_ds] == [1, 2, 3]
    # replaces the metadata of the given columns, and an empty dict removes it
    newer_ds = new_ds.with_column_metadata({"a": {"unit": "m"}, "b": {}})
    assert newer_ds.info.column_metadata == {"a": {"unit": "m"}}
    assert new_ds.info.column_metadata == {"a": {"unit": "cm"}, "b": {"source": "manual"}}

    # also works when features are unknown (e.g. from_generator without explicit features)
    gen_ds = IterableDataset.from_generator(lambda: ({"a": i} for i in range(3)))
    assert gen_ds.features is None
    gen_ds = gen_ds.with_column_metadata({"a": {"unit": "cm"}})
    assert gen_ds.info.column_metadata == {"a": {"unit": "cm"}}
    assert list(gen_ds) == [{"a": 0}, {"a": 1}, {"a": 2}]


@pytest.mark.parametrize(
    "column_metadata, error",
    [
        ({"d": {"unit": "cm"}}, ValueError),
        ({"a": {"unit": 1}}, TypeError),
        ({"a": {1: "cm"}}, TypeError),
        ({"a": "cm"}, TypeError),
    ],
)
def test_iterable_dataset_with_column_metadata_rejects_invalid_metadata(column_metadata, error):
    with pytest.raises(error):
        _iterable_dataset().with_column_metadata(column_metadata)


def test_iterable_dataset_column_metadata_follows_operations():
    ds = _iterable_dataset().with_column_metadata({"a": {"unit": "cm"}, "b": {"source": "manual"}})
    assert _dataset().with_column_metadata({"a": {"unit": "cm"}}).to_iterable_dataset().info.column_metadata == {
        "a": {"unit": "cm"}
    }
    assert ds.rename_column("a", "d").info.column_metadata == {"d": {"unit": "cm"}, "b": {"source": "manual"}}
    assert ds.rename_columns({"a": "d", "b": "e"}).info.column_metadata == {
        "d": {"unit": "cm"},
        "e": {"source": "manual"},
    }
    assert ds.with_format("arrow").rename_columns({"a": "d", "b": "e"}).info.column_metadata == {
        "d": {"unit": "cm"},
        "e": {"source": "manual"},
    }
    assert ds.remove_columns("a").info.column_metadata == {"b": {"source": "manual"}}
    assert ds.select_columns(["a", "c"]).info.column_metadata == {"a": {"unit": "cm"}}
    assert ds.map(lambda x: {"d": x["a"] * 2}).info.column_metadata == {
        "a": {"unit": "cm"},
        "b": {"source": "manual"},
    }
    assert ds.map(lambda x: {"d": x["a"]}, remove_columns=["a"]).info.column_metadata == {"b": {"source": "manual"}}
    for transformed in [
        ds.filter(lambda x: x["a"] > 1),
        ds.shuffle(seed=0, buffer_size=2),
        ds.skip(1),
        ds.take(2),
        ds.repeat(2),
    ]:
        assert transformed.info.column_metadata == {"a": {"unit": "cm"}, "b": {"source": "manual"}}
    # a new column with the name of a removed one doesn't get the old metadata
    assert ds.remove_columns("a").add_column("a", [0, 0, 0]).info.column_metadata == {"b": {"source": "manual"}}


def test_iterable_dataset_column_metadata_combine():
    ds1 = _iterable_dataset().with_column_metadata({"a": {"unit": "cm"}, "b": {"source": "manual"}})
    ds2 = _iterable_dataset().with_column_metadata({"a": {"unit": "cm"}, "b": {"source": "scraped"}})
    # metadata that differs between the datasets is dropped
    assert concatenate_datasets([ds1, ds2]).info.column_metadata == {"a": {"unit": "cm"}}
    assert interleave_datasets([ds1, ds2]).info.column_metadata == {"a": {"unit": "cm"}}
    other = IterableDataset.from_dict({"d": [1, 2, 3]}).with_column_metadata({"d": {"unit": "kg"}})
    assert concatenate_datasets([ds1, other], axis=1).info.column_metadata == {
        "a": {"unit": "cm"},
        "b": {"source": "manual"},
        "d": {"unit": "kg"},
    }


def test_iterable_dataset_column_metadata_to_parquet_and_back(tmp_path):
    ds = _iterable_dataset().with_column_metadata({"a": {"unit": "cm"}, "b": {"source": "manual"}})
    path = str(tmp_path / "streamed.parquet")
    ds.to_parquet(path)
    schema = pq.read_schema(path)
    assert schema.field("a").metadata == {b"unit": b"cm"}
    assert schema.field("b").metadata == {b"source": b"manual"}
    assert schema.field("c").metadata is None
    assert IterableDataset.from_parquet(path).info.column_metadata == {
        "a": {"unit": "cm"},
        "b": {"source": "manual"},
    }
    assert Dataset.from_parquet(path, cache_dir=str(tmp_path / "cache")).info.column_metadata == {
        "a": {"unit": "cm"},
        "b": {"source": "manual"},
    }


@pytest.mark.parametrize("num_source_shards, num_shards", [(2, 2), (1, 3)])
def test_iterable_dataset_column_metadata_push_to_hub_shards(offline_parquet_uploads, num_source_shards, num_shards):
    ds = _iterable_dataset(num_shards=num_source_shards).with_column_metadata({"a": {"unit": "cm"}})
    push_parquet_shards_offline(ds, num_shards=num_shards)
    files = sorted(offline_parquet_uploads.glob("*.parquet"))
    assert len(files) == num_shards
    assert all(pq.read_schema(file).field("a").metadata == {b"unit": b"cm"} for file in files)


def test_iterable_dataset_dict_with_column_metadata():
    dsets = IterableDatasetDict(train=_iterable_dataset(), test=_iterable_dataset())
    dsets = dsets.with_column_metadata({"a": {"unit": "cm"}})
    assert {split: ds.info.column_metadata for split, ds in dsets.items()} == {
        "train": {"a": {"unit": "cm"}},
        "test": {"a": {"unit": "cm"}},
    }


@pytest.mark.parametrize("known_features", [False, True])
@pytest.mark.parametrize("operation", ["rename", "select", "remove", "map_remove"])
def test_streaming_column_metadata_transform_parquet(tmp_path, known_features, operation):
    rows = [{"distance": 1, "label": "x"}, {"distance": 2, "label": "y"}]
    features = Dataset.from_list(rows).features if known_features else None
    source = IterableDataset.from_generator(lambda: iter(rows), features=features).with_column_metadata(
        {"distance": {"unit": "cm"}, "label": {"source": "manual"}}
    )
    if operation == "rename":
        transformed = source.rename_column("distance", "position")
        expected = {"position": {"unit": "cm"}, "label": {"source": "manual"}}
    elif operation == "select":
        transformed = source.select_columns("distance")
        expected = {"distance": {"unit": "cm"}}
    elif operation == "remove":
        transformed = source.remove_columns("label")
        expected = {"distance": {"unit": "cm"}}
    else:
        transformed = source.map(lambda row: {"position": row["distance"]}, remove_columns="distance")
        expected = {"label": {"source": "manual"}}
    assert transformed.info.column_metadata == expected
    path = tmp_path / "transformed.parquet"
    transformed.to_parquet(path)
    schema = pq.read_schema(path)
    actual = {
        field.name: {key.decode(): value.decode() for key, value in field.metadata.items()}
        for field in schema
        if field.metadata
    }
    assert actual == expected
    assert source.info.column_metadata == {"distance": {"unit": "cm"}, "label": {"source": "manual"}}
    assert list(source) == rows
