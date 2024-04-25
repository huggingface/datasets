import fsspec
import pyarrow.parquet as pq
import pytest

from datasets import Audio, Dataset, DatasetDict, Features, IterableDatasetDict, NamedSplit, Sequence, Value, config
from datasets.features.image import Image
from datasets.info import DatasetInfo
from datasets.io.parquet import ParquetDatasetReader, ParquetDatasetWriter, get_writer_batch_size

from ..utils import assert_arrow_memory_doesnt_increase, assert_arrow_memory_increases


def _check_parquet_dataset(dataset, expected_features):
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 4
    assert dataset.num_columns == 3
    assert dataset.column_names == ["col_1", "col_2", "col_3"]
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_dataset_from_parquet_keep_in_memory(keep_in_memory, parquet_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = ParquetDatasetReader(parquet_path, cache_dir=cache_dir, keep_in_memory=keep_in_memory).read()
    _check_parquet_dataset(dataset, expected_features)


@pytest.mark.parametrize(
    "features",
    [
        None,
        {"col_1": "string", "col_2": "int64", "col_3": "float64"},
        {"col_1": "string", "col_2": "string", "col_3": "string"},
        {"col_1": "int32", "col_2": "int32", "col_3": "int32"},
        {"col_1": "float32", "col_2": "float32", "col_3": "float32"},
    ],
)
def test_dataset_from_parquet_features(features, parquet_path, tmp_path):
    cache_dir = tmp_path / "cache"
    default_expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = ParquetDatasetReader(parquet_path, features=features, cache_dir=cache_dir).read()
    _check_parquet_dataset(dataset, expected_features)


@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
def test_dataset_from_parquet_split(split, parquet_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    dataset = ParquetDatasetReader(parquet_path, cache_dir=cache_dir, split=split).read()
    _check_parquet_dataset(dataset, expected_features)
    assert dataset.split == split if split else "train"


@pytest.mark.parametrize("path_type", [str, list])
def test_dataset_from_parquet_path_type(path_type, parquet_path, tmp_path):
    if issubclass(path_type, str):
        path = parquet_path
    elif issubclass(path_type, list):
        path = [parquet_path]
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    dataset = ParquetDatasetReader(path, cache_dir=cache_dir).read()
    _check_parquet_dataset(dataset, expected_features)


def test_parquet_read_geoparquet(geoparquet_path, tmp_path):
    cache_dir = tmp_path / "cache"
    dataset = ParquetDatasetReader(path_or_paths=geoparquet_path, cache_dir=cache_dir).read()

    expected_features = {
        "pop_est": "float64",
        "continent": "string",
        "name": "string",
        "gdp_md_est": "int64",
        "geometry": "binary",
    }
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 5
    assert dataset.num_columns == 6
    assert dataset.column_names == ["pop_est", "continent", "name", "iso_a3", "gdp_md_est", "geometry"]
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


def _check_parquet_datasetdict(dataset_dict, expected_features, splits=("train",)):
    assert isinstance(dataset_dict, (DatasetDict, IterableDatasetDict))
    for split in splits:
        dataset = dataset_dict[split]
        assert len(list(dataset)) == 4
        assert dataset.features is not None
        assert set(dataset.features) == set(expected_features)
        for feature, expected_dtype in expected_features.items():
            assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_parquet_datasetdict_reader_keep_in_memory(keep_in_memory, parquet_path, tmp_path):
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = ParquetDatasetReader(
            {"train": parquet_path}, cache_dir=cache_dir, keep_in_memory=keep_in_memory
        ).read()
    _check_parquet_datasetdict(dataset, expected_features)


@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize(
    "features",
    [
        None,
        {"col_1": "string", "col_2": "int64", "col_3": "float64"},
        {"col_1": "string", "col_2": "string", "col_3": "string"},
        {"col_1": "int32", "col_2": "int32", "col_3": "int32"},
        {"col_1": "float32", "col_2": "float32", "col_3": "float32"},
    ],
)
def test_parquet_datasetdict_reader_features(streaming, features, parquet_path, tmp_path):
    cache_dir = tmp_path / "cache"
    default_expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = (
        Features({feature: Value(dtype) for feature, dtype in features.items()}) if features is not None else None
    )
    dataset = ParquetDatasetReader(
        {"train": parquet_path}, features=features, cache_dir=cache_dir, streaming=streaming
    ).read()
    _check_parquet_datasetdict(dataset, expected_features)


@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize("columns", [None, ["col_1"]])
@pytest.mark.parametrize("pass_features", [False, True])
@pytest.mark.parametrize("pass_info", [False, True])
def test_parquet_datasetdict_reader_columns(streaming, columns, pass_features, pass_info, parquet_path, tmp_path):
    cache_dir = tmp_path / "cache"

    default_expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    info = (
        DatasetInfo(features=Features({feature: Value(dtype) for feature, dtype in default_expected_features.items()}))
        if pass_info
        else None
    )

    expected_features = (
        {col: default_expected_features[col] for col in columns} if columns else default_expected_features
    )
    features = (
        Features({feature: Value(dtype) for feature, dtype in expected_features.items()}) if pass_features else None
    )

    dataset = ParquetDatasetReader(
        {"train": parquet_path},
        columns=columns,
        features=features,
        info=info,
        cache_dir=cache_dir,
        streaming=streaming,
    ).read()
    _check_parquet_datasetdict(dataset, expected_features)


@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
def test_parquet_datasetdict_reader_split(split, parquet_path, tmp_path):
    if split:
        path = {split: parquet_path}
    else:
        split = "train"
        path = {"train": parquet_path, "test": parquet_path}
    cache_dir = tmp_path / "cache"
    expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    dataset = ParquetDatasetReader(path, cache_dir=cache_dir).read()
    _check_parquet_datasetdict(dataset, expected_features, splits=list(path.keys()))
    assert all(dataset[split].split == split for split in path.keys())


def test_parquet_write(dataset, tmp_path):
    writer = ParquetDatasetWriter(dataset, tmp_path / "foo.parquet")
    assert writer.write() > 0
    pf = pq.ParquetFile(tmp_path / "foo.parquet")
    output_table = pf.read()
    assert dataset.data.table == output_table


def test_dataset_to_parquet_keeps_features(shared_datadir, tmp_path):
    image_path = str(shared_datadir / "test_image_rgb.jpg")
    data = {"image": [image_path]}
    features = Features({"image": Image()})
    dataset = Dataset.from_dict(data, features=features)
    writer = ParquetDatasetWriter(dataset, tmp_path / "foo.parquet")
    assert writer.write() > 0

    reloaded_dataset = Dataset.from_parquet(str(tmp_path / "foo.parquet"))
    assert dataset.features == reloaded_dataset.features

    reloaded_iterable_dataset = ParquetDatasetReader(str(tmp_path / "foo.parquet"), streaming=True).read()
    assert dataset.features == reloaded_iterable_dataset.features


@pytest.mark.parametrize(
    "feature, expected",
    [
        (Features({"foo": Value("int32")}), None),
        (Features({"image": Image(), "foo": Value("int32")}), config.PARQUET_ROW_GROUP_SIZE_FOR_IMAGE_DATASETS),
        (Features({"nested": Sequence(Audio())}), config.PARQUET_ROW_GROUP_SIZE_FOR_AUDIO_DATASETS),
    ],
)
def test_get_writer_batch_size(feature, expected):
    assert get_writer_batch_size(feature) == expected


def test_dataset_to_parquet_fsspec(dataset, mockfs):
    dataset_path = "mock://my_dataset.csv"
    writer = ParquetDatasetWriter(dataset, dataset_path, storage_options=mockfs.storage_options)
    assert writer.write() > 0
    assert mockfs.isfile(dataset_path)

    with fsspec.open(dataset_path, "rb", **mockfs.storage_options) as f:
        assert f.read()
