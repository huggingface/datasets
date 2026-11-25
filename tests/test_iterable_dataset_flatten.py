import pandas as pd
import pyarrow as pa
import pytest

from datasets import Dataset, Features, Image, IterableDataset, IterableDatasetDict, Json, List, Value
from datasets.table import InMemoryTable


def _nested_data():
    return {
        "id": [0, 1, 2, 3],
        "meta": [
            {"score": 10, "nested": {"tag": "a", "flag": True}},
            {"score": 20, "nested": {"tag": "b", "flag": False}},
            {"score": 30, "nested": {"tag": "c", "flag": True}},
            {"score": 40, "nested": {"tag": "d", "flag": False}},
        ],
        "text": ["zero", "one", "two", "three"],
    }


def test_iterable_dataset_flatten_matches_dataset_arrow_backed():
    ds = Dataset.from_dict(_nested_data())
    expected = ds.flatten()
    iterable_ds = ds.to_iterable_dataset(num_shards=2).flatten()

    assert iterable_ds.column_names == expected.column_names
    assert iterable_ds.features == expected.features
    assert list(iterable_ds) == list(expected)


def test_iterable_dataset_flatten_parquet_roundtrip(tmp_path):
    ds = Dataset.from_dict(_nested_data())
    path = str(tmp_path / "nested.parquet")
    ds.to_parquet(path)

    streamed = IterableDataset.from_parquet(path).flatten()
    expected = ds.flatten()
    assert streamed.column_names == expected.column_names
    assert list(streamed) == list(expected)


@pytest.mark.parametrize("max_depth", [2, 3, 16])
def test_iterable_dataset_flatten_max_depth(max_depth):
    ds = Dataset.from_dict(_nested_data())
    expected = ds.flatten(max_depth=max_depth)
    iterable_ds = ds.to_iterable_dataset(num_shards=2).flatten(max_depth=max_depth)

    assert iterable_ds.column_names == expected.column_names
    assert iterable_ds.features == expected.features
    assert list(iterable_ds) == list(expected)


def test_iterable_dataset_flatten_max_depth_one_is_noop():
    ds = Dataset.from_dict(_nested_data())
    iterable_ds = ds.to_iterable_dataset(num_shards=2).flatten(max_depth=1)
    assert iterable_ds.column_names == ds.column_names
    assert iterable_ds.features == ds.features
    assert list(iterable_ds) == list(ds)


def test_iterable_dataset_flatten_from_generator_with_and_without_features():
    rows = [
        {"id": 0, "meta": {"score": 10, "nested": {"tag": "a"}}},
        {"id": 1, "meta": {"score": 20, "nested": {"tag": "b"}}},
    ]

    def gen():
        yield from rows

    # Without explicit features
    ds_no_feat = IterableDataset.from_generator(gen).flatten()
    assert ds_no_feat.features is None
    assert list(ds_no_feat) == [
        {"id": 0, "meta.score": 10, "meta.nested.tag": "a"},
        {"id": 1, "meta.score": 20, "meta.nested.tag": "b"},
    ]

    # Respects max_depth without features
    ds_depth2 = IterableDataset.from_generator(gen).flatten(max_depth=2)
    assert list(ds_depth2) == [
        {"id": 0, "meta.score": 10, "meta.nested": {"tag": "a"}},
        {"id": 1, "meta.score": 20, "meta.nested": {"tag": "b"}},
    ]

    # With explicit features
    features = Features({"id": Value("int64"), "meta": {"score": Value("int64"), "nested": {"tag": Value("string")}}})
    ds_with_feat = IterableDataset.from_generator(gen, features=features).flatten()
    assert ds_with_feat.column_names == ["id", "meta.score", "meta.nested.tag"]
    assert list(ds_with_feat) == [
        {"id": 0, "meta.score": 10, "meta.nested.tag": "a"},
        {"id": 1, "meta.score": 20, "meta.nested.tag": "b"},
    ]


def test_iterable_dataset_flatten_null_parent_struct():
    data = {
        "id": [0, 1, 2],
        "meta": [
            {"score": 10, "nested": {"tag": "a"}},
            None,
            {"score": 30, "nested": None},
        ],
    }
    ds = Dataset.from_dict(data)
    expected = ds.flatten()

    # Arrow-backed streaming path
    arrow_stream = ds.to_iterable_dataset().flatten()
    assert list(arrow_stream) == list(expected)

    # Python generator path with known features
    rows = [{"id": data["id"][i], "meta": data["meta"][i]} for i in range(3)]
    gen_stream = IterableDataset.from_generator(lambda: (r for r in rows), features=ds.features).flatten()
    assert list(gen_stream) == list(expected)


def test_iterable_dataset_flatten_preserves_json_and_list_columns():
    features = Features(
        {
            "id": Value("int64"),
            "payload": Json(),
            "items": List({"k": Value("string")}),
            "meta": {"x": Value("int64")},
        }
    )
    ds = Dataset.from_dict(
        {
            "id": [0, 1],
            "payload": [{"a": 1}, {"b": 2}],
            "items": [[{"k": "v1"}], [{"k": "v2"}]],
            "meta": [{"x": 10}, {"x": 20}],
        },
        features=features,
    )
    expected = ds.flatten()
    streamed = ds.to_iterable_dataset().flatten()
    assert streamed.column_names == expected.column_names
    assert streamed.features == expected.features
    assert list(streamed) == list(expected)


def test_iterable_dataset_flatten_idempotent_without_structs():
    ds = Dataset.from_dict({"a": [1, 2], "b": ["x", "y"]})
    streamed = ds.to_iterable_dataset().flatten()
    assert streamed.column_names == ["a", "b"]
    assert list(streamed) == [{"a": 1, "b": "x"}, {"a": 2, "b": "y"}]


def test_iterable_dataset_flatten_empty():
    features = Features({"id": Value("int64"), "meta": {"x": Value("string")}})
    # Python generator empty stream
    gen_empty = IterableDataset.from_generator(lambda: iter([]), features=features).flatten()
    assert gen_empty.column_names == ["id", "meta.x"]
    assert list(gen_empty) == []

    # Arrow-backed empty stream
    arrow_empty = Dataset.from_dict(_nested_data()).to_iterable_dataset().take(0).flatten()
    assert arrow_empty.column_names == ["id", "meta.score", "meta.nested.tag", "meta.nested.flag", "text"]
    assert list(arrow_empty) == []


def test_iterable_dataset_flatten_formats_and_batching():
    ds = Dataset.from_dict(_nested_data()).to_iterable_dataset(num_shards=2).flatten()

    arrow_tables = list(ds.with_format("arrow").iter(batch_size=2))
    assert len(arrow_tables) == 2
    assert all(isinstance(t, pa.Table) for t in arrow_tables)
    assert arrow_tables[0].column_names == ["id", "meta.score", "meta.nested.tag", "meta.nested.flag", "text"]

    dfs = list(ds.with_format("pandas").iter(batch_size=2))
    assert len(dfs) == 2
    assert all(isinstance(df, pd.DataFrame) for df in dfs)
    assert list(dfs[0].columns) == ["id", "meta.score", "meta.nested.tag", "meta.nested.flag", "text"]


def test_iterable_dataset_flatten_sharding_shuffling_and_checkpoint_resume():
    ds = Dataset.from_dict(_nested_data()).to_iterable_dataset(num_shards=2).flatten()
    assert ds.num_shards == 2

    # Sharding
    shard0 = list(ds.shard(num_shards=2, index=0))
    shard1 = list(ds.shard(num_shards=2, index=1))
    assert shard0 + shard1 == list(ds)

    # Shuffling preserves all flattened rows
    shuffled = list(ds.shuffle(seed=42, buffer_size=2))
    assert sorted(shuffled, key=lambda x: x["id"]) == list(ds)

    # Skip and take
    assert [x["id"] for x in ds.skip(1).take(2)] == [1, 2]

    # Checkpoint resume via state_dict / load_state_dict
    first_half = []
    state_dict = None
    for idx, example in enumerate(ds):
        first_half.append(example)
        if idx == 1:
            state_dict = ds.state_dict()
            break
    ds.load_state_dict(state_dict)
    second_half = list(ds)
    assert first_half + second_half == list(ds)


def test_iterable_dataset_flatten_updates_column_metadata():
    ds = Dataset.from_dict(_nested_data()).with_column_metadata(
        {"meta": {"desc": "nested"}, "text": {"language": "en"}}
    )
    streamed = ds.to_iterable_dataset()
    # Explicitly attach column_metadata on the iterable dataset info to verify flatten drops split struct metadata
    streamed._info.column_metadata = {"meta": {"desc": "nested"}, "text": {"language": "en"}}
    flattened = streamed.flatten()
    assert flattened.info.column_metadata == {"text": {"language": "en"}}


def test_iterable_dataset_dict_flatten():
    dsets = IterableDatasetDict(
        train=Dataset.from_dict(_nested_data()).to_iterable_dataset(num_shards=2),
        test=Dataset.from_dict(_nested_data()).to_iterable_dataset(num_shards=1),
    )
    flattened = dsets.flatten()
    expected = Dataset.from_dict(_nested_data()).flatten()
    assert isinstance(flattened, IterableDatasetDict)
    for split in ["train", "test"]:
        assert flattened[split].column_names == expected.column_names
        assert flattened[split].features == expected.features
        assert list(flattened[split]) == list(expected)


@pytest.mark.parametrize("decode", [True, False])
@pytest.mark.parametrize("nested", [True, False])
def test_flatten_image_feature_arrow_parity(decode, nested):
    image = {"path": "unused.png", "bytes": None}
    feature = Image(decode=decode)
    features = Features({"item": {"image": feature} if nested else feature})
    table = pa.Table.from_pydict(
        {"item": [{"image": image} if nested else image]},
        schema=features.arrow_schema,
    )
    ds = Dataset(InMemoryTable(table))
    expected = ds.flatten()
    streamed = ds.to_iterable_dataset().flatten().with_format("arrow")
    actual = pa.concat_tables(list(streamed))
    assert streamed.features == expected.features
    assert actual.equals(expected.data.table)
