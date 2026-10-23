from unittest.mock import patch

import pandas as pd
import pyarrow as pa
import pytest

import datasets
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.pandas.pandas import PANDAS_PICKLE_DISABLED_ERROR, Pandas, PandasConfig


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = PandasConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = PandasConfig(name="name", data_files=data_files)


@pytest.mark.parametrize("filename", ["input.pkl", "input.pickle", "input.csv", "input"])
@pytest.mark.parametrize("streaming", [False, True])
def test_fresh_load_rejects_without_unpickling(tmp_path, filename, streaming):
    path = tmp_path / filename
    path.write_bytes(b"unused: table generation must reject without unpickling")
    with patch("pandas.read_pickle") as read_pickle:
        with pytest.raises(ValueError) as caught:
            with pytest.warns(FutureWarning, match="Pandas builder is deprecated"):
                loaded = datasets.load_dataset(
                    "pandas",
                    data_files=str(path),
                    split="train",
                    streaming=streaming,
                    cache_dir=str(tmp_path / "c"),
                )
                if streaming:
                    # Streaming reaches table generation when the iterator is consumed.
                    list(loaded)
        assert str(caught.value) == PANDAS_PICKLE_DISABLED_ERROR
        read_pickle.assert_not_called()


@pytest.mark.parametrize("kwargs", [{}, {"info": datasets.DatasetInfo()}])
def test_direct_construction_allows_setup_but_rejects_table_generation(tmp_path, kwargs):
    with patch("pandas.read_pickle") as read_pickle:
        if "info" in kwargs:
            builder = Pandas(cache_dir=str(tmp_path / "c"), **kwargs)
        else:
            with pytest.warns(FutureWarning, match="Pandas builder is deprecated"):
                builder = Pandas(cache_dir=str(tmp_path / "c"), **kwargs)
        with pytest.raises(ValueError) as caught:
            builder._generate_tables(["input.pkl"])
        assert str(caught.value) == PANDAS_PICKLE_DISABLED_ERROR
        read_pickle.assert_not_called()


def test_generate_tables_rejects_before_opening_or_inspecting_files():
    builder = object.__new__(Pandas)
    with patch("builtins.open") as open_file, patch("pandas.read_pickle") as read_pickle:
        for files in (["input.pkl"], ["https://example.invalid/input.pkl"], [], None):
            with pytest.raises(ValueError) as caught:
                builder._generate_tables(files)
            assert str(caught.value) == PANDAS_PICKLE_DISABLED_ERROR
        open_file.assert_not_called()
        read_pickle.assert_not_called()


def test_load_dataset_builder_still_allows_setup(tmp_path):
    path = tmp_path / "input.pkl"
    path.write_bytes(b"unused: constructing a builder must not unpickle")
    with patch("pandas.read_pickle") as read_pickle:
        with pytest.warns(FutureWarning, match="Pandas builder is deprecated"):
            builder = datasets.load_dataset_builder("pandas", data_files=str(path), cache_dir=str(tmp_path / "c"))
        assert isinstance(builder, Pandas)
        with pytest.raises(ValueError) as caught:
            builder.download_and_prepare()
        assert str(caught.value) == PANDAS_PICKLE_DISABLED_ERROR
        read_pickle.assert_not_called()


def test_prepared_arrow_cache_can_be_reused_without_unpickling(tmp_path):
    path = tmp_path / "input.pkl"
    path.write_bytes(b"unused: seed the cache directly with an Arrow table")
    kwargs = {"data_files": str(path), "split": "train", "cache_dir": str(tmp_path / "c")}
    with patch("pandas.read_pickle") as read_pickle:
        # Simulate a prepared cache without ever deserializing a pickle.
        with patch.object(Pandas, "_generate_tables", return_value=iter([(0, pa.table({"value": ["cached"]}))])):
            with pytest.warns(FutureWarning, match="Pandas builder is deprecated"):
                prepared = datasets.load_dataset("pandas", **kwargs)
            assert prepared[0] == {"value": "cached"}
        with patch.object(
            Pandas, "_generate_tables", side_effect=ValueError(PANDAS_PICKLE_DISABLED_ERROR)
        ) as generate:
            with pytest.warns(FutureWarning, match="Pandas builder is deprecated"):
                cached = datasets.load_dataset("pandas", **kwargs)
            assert cached[0] == {"value": "cached"}
            generate.assert_not_called()
        read_pickle.assert_not_called()


@pytest.mark.parametrize("streaming", [False, True])
def test_safe_tabular_loading_still_works(tmp_path, streaming):
    frame = pd.DataFrame({"value": ["example"]})
    source = datasets.Dataset.from_pandas(frame, preserve_index=False)
    assert source[0] == {"value": "example"}
    path = tmp_path / "data.parquet"
    source.to_parquet(str(path))
    loaded = datasets.load_dataset(
        "parquet", data_files=str(path), split="train", streaming=streaming, cache_dir=str(tmp_path / "cache")
    )
    assert list(loaded) == [{"value": "example"}]
