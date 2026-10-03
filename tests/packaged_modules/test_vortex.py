import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from datasets import Features, List, Value, load_dataset, load_dataset_builder
from datasets.download import DownloadManager


vx = pytest.importorskip("vortex")


def _write_vortex_file(table: pa.Table, path) -> str:
    vx.io.write(vx.array(table), str(path))
    return str(path)


@pytest.fixture
def vortex_file(tmp_path) -> str:
    data = pa.table(
        {
            "id": pa.array([1, 2, 3, 4]),
            "value": pa.array([10.0, 20.0, 30.0, 40.0]),
            "text": pa.array(["a", "b", "c", "d"]),
        }
    )
    return _write_vortex_file(data, tmp_path / "data.vortex")


@pytest.fixture
def vortex_hf_dataset(tmp_path) -> str:
    data = pa.table(
        {
            "id": pa.array([1, 2, 3, 4]),
            "value": pa.array([10.0, 20.0, 30.0, 40.0]),
            "text": pa.array(["a", "b", "c", "d"]),
        }
    )
    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    _write_vortex_file(data, tmp_path / "data" / "train.vortex")
    _write_vortex_file(data[:2], tmp_path / "data" / "test.vortex")
    return str(tmp_path)


def test_load_vortex_file(vortex_file):
    dataset_dict = load_dataset("vortex", data_files=vortex_file)
    assert "train" in dataset_dict.keys()

    dataset = dataset_dict["train"]
    assert dataset.column_names == ["id", "value", "text"]
    assert dataset["id"] == [1, 2, 3, 4]
    assert dataset["text"] == ["a", "b", "c", "d"]


@pytest.mark.parametrize("streaming", [False, True])
def test_load_vortex_hf_dataset(vortex_hf_dataset, streaming):
    dataset_dict = load_dataset(vortex_hf_dataset, streaming=streaming)
    assert "train" in dataset_dict.keys()
    assert "test" in dataset_dict.keys()

    dataset = dataset_dict["train"]
    assert list(dataset["id"]) == [1, 2, 3, 4]
    dataset = dataset_dict["test"]
    assert list(dataset["id"]) == [1, 2]


@pytest.mark.parametrize("streaming", [False, True])
def test_load_vortex_dataset_with_columns(vortex_hf_dataset, streaming):
    dataset_dict = load_dataset(vortex_hf_dataset, columns=["id", "text"], streaming=streaming)
    dataset = dataset_dict["train"]

    assert set(dataset.column_names) == {"id", "text"}
    assert list(dataset["id"]) == [1, 2, 3, 4]
    assert list(dataset["text"]) == ["a", "b", "c", "d"]


@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize(
    "filters, expected_ids",
    [
        ([("id", ">", 2)], [3, 4]),
        ([("id", "in", [1, 4])], [1, 4]),
        ([("id", "not in", [1, 4])], [2, 3]),
        ([[("id", "<", 2)], [("text", "==", "d")]], [1, 4]),
        # a predicate may be a list rather than a tuple, like the Parquet loader accepts
        ([["id", ">", 2]], [3, 4]),
        ([[["id", "<", 2]], [["text", "==", "d"]]], [1, 4]),
    ],
)
def test_load_vortex_dataset_with_filters(vortex_hf_dataset, streaming, filters, expected_ids):
    dataset = load_dataset(vortex_hf_dataset, filters=filters, streaming=streaming, split="train")

    assert list(dataset["id"]) == expected_ids


@pytest.mark.parametrize(
    "op, value, expected_ids, parquet_ids",
    [
        ("==", 2, [2], [2]),
        ("!=", 2, [1, 3, 4], [1, 3, 4]),
        ("<", 3, [1, 2], [1, 2]),
        ("<=", 3, [1, 2, 3], [1, 2, 3]),
        (">", 3, [4], [4]),
        (">=", 3, [3, 4], [3, 4]),
        ("in", [1, 4], [1, 4], [1, 4]),
        # SQL semantics: a null satisfies no comparison, so `not in` drops it. The Parquet loader
        # keeps it, building `~field.isin(values)` where a null is not in the set.
        ("not in", [1, 4], [2, 3], [2, 3, None]),
    ],
)
def test_load_vortex_dataset_filters_nulls_following_sql(tmp_path, op, value, expected_ids, parquet_ids):
    data = pa.table({"id": pa.array([1, 2, 3, 4, None])})
    pq.write_table(data, tmp_path / "data.parquet")
    _write_vortex_file(data, tmp_path / "data.vortex")
    filters = [("id", op, value)]

    parquet_dataset = load_dataset(
        "parquet", data_files=str(tmp_path / "data.parquet"), split="train", filters=filters
    )
    vortex_dataset = load_dataset("vortex", data_files=str(tmp_path / "data.vortex"), split="train", filters=filters)

    assert vortex_dataset["id"] == expected_ids
    assert parquet_dataset["id"] == parquet_ids


@pytest.mark.parametrize("streaming", [False, True])
def test_load_vortex_dataset_with_filter_on_unprojected_column(vortex_hf_dataset, streaming):
    dataset = load_dataset(
        vortex_hf_dataset, columns=["text"], filters=[("id", ">", 2)], streaming=streaming, split="train"
    )

    assert list(dataset["text"]) == ["c", "d"]


@pytest.mark.parametrize("op", ["in", "not in"])
def test_vortex_filters_with_empty_values(op):
    from datasets.packaged_modules.vortex.vortex import _filters_to_expression

    with pytest.raises(ValueError, match=f"Empty set of values for '{op}' filter"):
        _filters_to_expression([("id", op, [])])


@pytest.mark.parametrize("filters", [[], [[]], [("id", "~=", 2)]])
def test_vortex_malformed_filters(filters):
    from datasets.packaged_modules.vortex.vortex import _filters_to_expression

    with pytest.raises(ValueError):
        _filters_to_expression(filters)


@pytest.mark.parametrize("streaming", [False, True])
def test_load_vortex_dataset_with_expr_filter(vortex_hf_dataset, streaming):
    import vortex.expr as ve

    dataset = load_dataset(vortex_hf_dataset, filters=ve.column("value") >= 30.0, streaming=streaming, split="train")

    assert list(dataset["id"]) == [3, 4]


@pytest.mark.parametrize("streaming", [False, True])
def test_load_vortex_dataset_with_batch_size(vortex_hf_dataset, streaming):
    dataset_dict = load_dataset(vortex_hf_dataset, batch_size=1, streaming=streaming)
    dataset = dataset_dict["train"]

    assert list(dataset["id"]) == [1, 2, 3, 4]


def _without_view_types(feature):
    """Replace the Arrow view types Vortex reports with their canonical equivalents."""
    if isinstance(feature, Value):
        return Value(feature.dtype.removesuffix("_view"))
    elif isinstance(feature, List):
        return List(_without_view_types(feature.feature), length=feature.length)
    elif isinstance(feature, dict):
        return type(feature)({name: _without_view_types(child) for name, child in feature.items()})
    return feature


def test_load_vortex_file_infers_view_typed_features(tmp_path):
    # Vortex reports its utf8 and binary as the Arrow view types, so the features hold the view
    # types too. Apart from those, the same data must load the same way as in any other format.
    data = pa.table(
        {
            "text": pa.array(["a", "b"]),
            "blob": pa.array([b"x", b"y"]),
            "nested": pa.array([{"text": "a", "blobs": [b"x"]}] * 2),
            "texts": pa.array([["a", "b"]] * 2),
        }
    )
    pq.write_table(data, tmp_path / "data.parquet")
    _write_vortex_file(data, tmp_path / "data.vortex")

    parquet_dataset = load_dataset("parquet", data_files=str(tmp_path / "data.parquet"), split="train")
    vortex_dataset = load_dataset("vortex", data_files=str(tmp_path / "data.vortex"), split="train")

    assert vortex_dataset.features["text"] == Value("string_view")
    assert vortex_dataset.features["blob"] == Value("binary_view")
    assert vortex_dataset.features["nested"] == {"text": Value("string_view"), "blobs": List(Value("binary_view"))}
    assert _without_view_types(vortex_dataset.features) == parquet_dataset.features
    assert vortex_dataset.to_dict() == parquet_dataset.to_dict()


def test_load_vortex_file_with_features(vortex_file):
    features = Features({"id": Value("int32"), "value": Value("float32"), "text": Value("large_string")})
    dataset = load_dataset("vortex", data_files=vortex_file, features=features, split="train")

    assert dataset.features == features
    assert dataset["id"] == [1, 2, 3, 4]


@pytest.mark.parametrize(
    "filters, expected", [(None, {"train": 4, "test": 2}), ([("id", ">", 2)], {"train": 2, "test": 0})]
)
def test_count_vortex_examples(vortex_hf_dataset, filters, expected):
    builder = load_dataset_builder(vortex_hf_dataset, filters=filters)

    assert builder.count_examples(DownloadManager()) == expected


@pytest.mark.parametrize("token", [None, True, False, "hf_token"])
def test_open_vortex_file_passes_hf_storage_options_to_the_store(monkeypatch, token):
    from datasets.packaged_modules.vortex import vortex as vortex_module

    stores, opened = [], []
    monkeypatch.setattr(
        vx.store,
        "HfStore",
        lambda repo_id, *, revision=None, token=None, endpoint=None: stores.append(
            (repo_id, revision, token, endpoint)
        ),
    )
    monkeypatch.setattr(vx, "open", lambda path, store=None: opened.append((path, store)))
    vortex_module._hf_store.cache_clear()

    storage_options = {"endpoint": "https://hub-ci.huggingface.co", "token": token}
    for shard in range(2):
        vortex_module._open_vortex_file(f"hf://datasets/org/name@abc123/data/{shard}.vortex", storage_options)

    # the token is passed on as it was given: `True` and `False` mean the saved login and no login
    assert stores == [("org/name", "abc123", token, "https://hub-ci.huggingface.co")]  # one store for both shards
    assert [path for path, _ in opened] == ["data/0.vortex", "data/1.vortex"]


def test_open_vortex_file_decodes_the_revision(monkeypatch):
    from datasets.packaged_modules.vortex import vortex as vortex_module

    stores = []
    monkeypatch.setattr(
        vx.store,
        "HfStore",
        lambda repo_id, *, revision=None, token=None, endpoint=None: stores.append(revision),
    )
    monkeypatch.setattr(vx, "open", lambda path, store=None: None)
    vortex_module._hf_store.cache_clear()

    vortex_module._open_vortex_file("hf://datasets/org/name@refs%2Fconvert%2Fparquet/data/train.vortex", {})

    assert stores == ["refs/convert/parquet"]  # `HfStore` percent-encodes it again itself


def test_open_vortex_file_refuses_hf_buckets():
    from datasets.packaged_modules.vortex import vortex as vortex_module

    with pytest.raises(NotImplementedError, match="HF Buckets"):
        vortex_module._open_vortex_file("hf://buckets/org/name/data/train.vortex", {})


@pytest.mark.parametrize("path", ["/local/data.vortex", "https://example.com/data.vortex"])
def test_open_vortex_file_leaves_non_hub_paths_to_vortex(monkeypatch, path):
    from datasets.packaged_modules.vortex import vortex as vortex_module

    opened = []
    monkeypatch.setattr(vx, "open", lambda path, store=None: opened.append((path, store)))

    vortex_module._open_vortex_file(path, {"token": "hf_token"})

    assert opened == [(path, None)]


@pytest.fixture
def vortex_multisplit_file(tmp_path) -> str:
    # Enough rows that the file's layout yields several splits (Vortex subdivides at about
    # 100k rows) to reshard on.
    path = str(tmp_path / "multisplit.vortex")
    vx.io.write(vx.array(pa.table({"id": pa.array(range(250_000))})), path)
    return path


def test_coalesced_row_ranges():
    from datasets.packaged_modules.vortex import vortex as vortex_module

    class SplitsOnly:
        def splits(self):
            return [(0, 10), (10, 20), (20, 100), (100, 105)]

    assert vortex_module._coalesced_row_ranges(SplitsOnly(), target_num_rows=50) == [(0, 20), (20, 100), (100, 105)]


def test_reshard_target_num_rows_follows_the_file_size(vortex_multisplit_file, monkeypatch):
    import os

    from datasets.packaged_modules.vortex import vortex as vortex_module

    vortex_file = vx.open(vortex_multisplit_file)
    file_num_bytes = os.path.getsize(vortex_multisplit_file)
    # a target of half the file must give a target of half the rows
    monkeypatch.setattr(vortex_module, "_RESHARD_TARGET_NUM_BYTES", file_num_bytes // 2)

    target = vortex_module._reshard_target_num_rows(vortex_file, vortex_multisplit_file)

    assert target == len(vortex_file) * (file_num_bytes // 2) // file_num_bytes


def test_reshard_target_num_rows_falls_back_without_a_file_size(vortex_multisplit_file, monkeypatch):
    from datasets.packaged_modules.vortex import vortex as vortex_module

    def unsized(file, download_config=None):
        raise OSError("no size for you")

    monkeypatch.setattr(vortex_module, "xgetsize", unsized)

    target = vortex_module._reshard_target_num_rows(vx.open(vortex_multisplit_file), vortex_multisplit_file)

    assert target == vortex_module._RESHARD_FALLBACK_NUM_ROWS


@pytest.mark.parametrize("filters", [None, [("id", ">=", 200_000)]])
def test_reshard_vortex_dataset(vortex_multisplit_file, monkeypatch, filters):
    from datasets.packaged_modules.vortex import vortex as vortex_module

    # a one-byte target keeps every natural split as its own shard
    monkeypatch.setattr(vortex_module, "_RESHARD_TARGET_NUM_BYTES", 1)
    dataset = load_dataset("vortex", data_files=vortex_multisplit_file, streaming=True, split="train", filters=filters)
    resharded = dataset.reshard()

    assert dataset.num_shards == 1
    assert resharded.num_shards > 1
    assert list(resharded) == list(dataset)
    # already-subdivided shards are kept as they are
    assert resharded.reshard().num_shards == resharded.num_shards


def test_generate_shards_with_row_ranges(vortex_multisplit_file):
    builder = load_dataset_builder("vortex", data_files=vortex_multisplit_file)
    shards = list(builder._generate_shards(files=["a", "b"], row_ranges=[None, (0, 5)]))

    assert shards == ["a", {"fragment_data_file": "b", "fragment_row_range": (0, 5)}]


@pytest.mark.parametrize("filters, expected", [(None, [2, 2]), ([("id", ">", 2)], [0, 2])])
def test_count_vortex_examples_per_row_range(vortex_file, filters, expected):
    builder = load_dataset_builder("vortex", data_files=vortex_file, filters=filters)
    counts = list(builder._generate_num_examples(files=[vortex_file] * 2, row_ranges=[(0, 2), (2, 4)]))

    assert counts == expected


@pytest.fixture
def bad_vortex_file(tmp_path) -> str:
    path = tmp_path / "bad.vortex"
    path.write_bytes(b"this is not a vortex file")
    return str(path)


def test_load_vortex_on_bad_files_error_by_default(vortex_file, bad_vortex_file):
    with pytest.raises(RuntimeError):
        load_dataset("vortex", data_files=[bad_vortex_file, vortex_file], split="train")


@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize("on_bad_files", ["warn", "skip"])
def test_load_vortex_on_bad_files_skip(vortex_file, bad_vortex_file, on_bad_files, streaming):
    # the bad file comes first, so both schema inference and generation have to skip it
    dataset = load_dataset(
        "vortex",
        data_files=[bad_vortex_file, vortex_file],
        split="train",
        on_bad_files=on_bad_files,
        streaming=streaming,
    )

    assert [example["id"] for example in dataset] == [1, 2, 3, 4]
