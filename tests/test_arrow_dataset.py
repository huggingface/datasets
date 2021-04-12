import os
import pickle
import shutil

import numpy as np
import pandas as pd
import pytest

import datasets.arrow_dataset
from datasets import NamedSplit, load_from_disk
from datasets.arrow_dataset import Dataset
from datasets.features import Array2D, Array3D, ClassLabel, Features, Sequence, Value
from datasets.info import DatasetInfo

from .utils import assert_arrow_memory_doesnt_increase, assert_arrow_memory_increases, require_tf, require_torch


def picklable_map_function(x):
    return {"id": int(x["filename"].split("_")[-1])}


def picklable_map_function_with_indices(x, i):
    return {"id": i}


@pytest.fixture
def tmp_dir(tmp_path):
    yield str(tmp_path)
    shutil.rmtree(tmp_path)


@pytest.fixture
def create_dummy_dataset(tmp_dir):
    created_datasets = []

    def _create_dummy_dataset(in_memory: bool, multiple_columns=False, array_features=False):
        if multiple_columns:
            if array_features:
                data = {
                    "col_1": [[[True, False], [False, True]]] * 4,  # 2D
                    "col_2": [[[["a", "b"], ["c", "d"]], [["e", "f"], ["g", "h"]]]] * 4,  # 3D array
                    "col_3": [[3, 2, 1, 0]] * 4,  # Sequence
                }
                features = Features(
                    {
                        "col_1": Array2D(shape=(2, 2), dtype="bool"),
                        "col_2": Array3D(shape=(2, 2, 2), dtype="string"),
                        "col_3": Sequence(feature=Value("int64")),
                    }
                )
            else:
                data = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", "d"], "col_3": [False, True, False, True]}
                features = None
            dset = Dataset.from_dict(data, features=features)
        else:
            dset = Dataset.from_dict({"filename": ["my_name-train" + "_" + str(x) for x in np.arange(30).tolist()]})
        if in_memory:
            dset = dset.map(keep_in_memory=True)
        else:
            start = 0
            while os.path.isfile(os.path.join(tmp_dir, f"dataset{start}.arrow")):
                start += 1
            dset = dset.map(cache_file_name=os.path.join(tmp_dir, f"dataset{start}.arrow"))
        created_datasets.append(dset)
        return dset

    yield _create_dummy_dataset
    for dataset in created_datasets:
        dataset.__del__()


@pytest.fixture
def map_to(tmp_dir):
    created_datasets = []

    def _map_to(in_memory, *datasets):
        if in_memory:
            datasets = [dataset.map(keep_in_memory=True) for dataset in datasets]
        else:
            start = 0
            while os.path.isfile(os.path.join(tmp_dir, f"dataset{start}.arrow")):
                start += 1
            datasets = [
                dataset.map(cache_file_name=os.path.join(tmp_dir, f"dataset{start + i}.arrow"))
                for i, dataset in enumerate(datasets)
            ]
        created_datasets.extend(datasets)
        return datasets if len(datasets) > 1 else datasets[0]

    yield _map_to
    for dataset in created_datasets:
        dataset.__del__()


@pytest.fixture
def mock_concatenate_datasets(tmp_dir):
    created_datasets = []
    unmocked_concatenate_datasets = datasets.concatenate_datasets

    def _mock_concatenate_datasets(*args, **kwargs):
        dset = unmocked_concatenate_datasets(*args, **kwargs)
        created_datasets.append(dset)
        return dset

    yield _mock_concatenate_datasets
    for dataset in created_datasets:
        dataset.__del__()


@pytest.fixture
def mock_dataset_cast(tmp_dir):
    created_datasets = []
    unmocked_dataset_cast = Dataset.cast

    def _mock_dataset_cast(*args, **kwargs):
        dset = unmocked_dataset_cast(*args, **kwargs)
        created_datasets.append(dset)
        return dset

    yield _mock_dataset_cast
    print("Delete casted_dataset", len(created_datasets))
    for dataset in created_datasets:
        dataset.__del__()


@pytest.fixture
def mock_dataset_flatten(tmp_dir):
    created_datasets = []
    unmocked_dataset_flatten = Dataset.flatten

    def _mock_dataset_flatten(*args, **kwargs):
        dset = unmocked_dataset_flatten(*args, **kwargs)
        created_datasets.append(dset)
        return dset

    yield _mock_dataset_flatten
    for dataset in created_datasets:
        dataset.__del__()


@pytest.fixture
def mock_dataset_load_from_disk(tmp_dir):
    created_datasets = []
    unmocked_dataset_load_from_disk = Dataset.load_from_disk

    def _mock_dataset_load_from_disk(*args, **kwargs):
        dset = unmocked_dataset_load_from_disk(*args, **kwargs)
        created_datasets.append(dset)
        return dset

    yield _mock_dataset_load_from_disk
    print("Delete loaded_from_disk_dataset", len(created_datasets))
    for dataset in created_datasets:
        dataset.__del__()


@pytest.fixture
def mock_dataset_map(tmp_dir):
    created_datasets = []
    unmocked_dataset_map = Dataset.map

    def _mock_dataset_map(*args, **kwargs):
        dset = unmocked_dataset_map(*args, **kwargs)
        created_datasets.append(dset)
        return dset

    yield _mock_dataset_map
    for dataset in created_datasets:
        dataset.__del__()


@pytest.fixture
def mock_dataset_remove_columns(tmp_dir):
    created_datasets = []
    unmocked_dataset_remove_columns = Dataset.remove_columns

    def _mock_dataset_remove_columns(*args, **kwargs):
        dset = unmocked_dataset_remove_columns(*args, **kwargs)
        created_datasets.append(dset)
        return dset

    yield _mock_dataset_remove_columns
    for dataset in created_datasets:
        dataset.__del__()


@pytest.fixture
def mock_dataset_rename_column(tmp_dir):
    created_datasets = []
    unmocked_dataset_rename_column = Dataset.rename_column

    def _mock_dataset_rename_column(*args, **kwargs):
        dset = unmocked_dataset_rename_column(*args, **kwargs)
        created_datasets.append(dset)
        return dset

    yield _mock_dataset_rename_column
    for dataset in created_datasets:
        dataset.__del__()


@pytest.fixture
def mock_dataset_select(tmp_dir):
    created_datasets = []
    unmocked_dataset_select = Dataset.select

    def _mock_select(*args, **kwargs):
        dset = unmocked_dataset_select(*args, **kwargs)
        created_datasets.append(dset)
        return dset

    yield _mock_select
    for dataset in created_datasets:
        dataset.__del__()


@pytest.fixture(autouse=True)
def mock_dataset(
    monkeypatch,
    mock_concatenate_datasets,
    mock_dataset_cast,
    mock_dataset_flatten,
    mock_dataset_load_from_disk,
    mock_dataset_map,
    mock_dataset_remove_columns,
    mock_dataset_rename_column,
    mock_dataset_select,
):
    monkeypatch.setattr(datasets, "concatenate_datasets", mock_concatenate_datasets)
    monkeypatch.setattr(Dataset, "cast", mock_dataset_cast)
    monkeypatch.setattr(Dataset, "flatten", mock_dataset_flatten)
    monkeypatch.setattr(Dataset, "load_from_disk", mock_dataset_load_from_disk)
    monkeypatch.setattr(Dataset, "map", mock_dataset_map)
    monkeypatch.setattr(Dataset, "remove_columns", mock_dataset_remove_columns)
    monkeypatch.setattr(Dataset, "rename_column", mock_dataset_rename_column)
    monkeypatch.setattr(Dataset, "select", mock_dataset_select)


def pytest_generate_tests(metafunc):
    if hasattr(metafunc, "cls") and hasattr(metafunc.cls, "params"):
        func_args = metafunc.cls.params
        arg_names = list(func_args.keys())
        for arg_name in arg_names:
            if arg_name in metafunc.fixturenames:
                metafunc.parametrize(arg_name, func_args[arg_name])


class TestBaseDataset:
    params = {"in_memory": [False, True]}

    def test_dummy_dataset(self, in_memory, create_dummy_dataset):
        dset = create_dummy_dataset(in_memory)
        assert dset.features == Features({"filename": Value("string")})
        assert dset[0]["filename"] == "my_name-train_0"
        assert dset["filename"][0] == "my_name-train_0"

        dset = create_dummy_dataset(in_memory, multiple_columns=True)
        assert dset.features == Features({"col_1": Value("int64"), "col_2": Value("string"), "col_3": Value("bool")})
        assert dset[0]["col_1"] == 3
        assert dset["col_1"][0] == 3

        dset = create_dummy_dataset(in_memory, multiple_columns=True, array_features=True)
        assert dset.features == Features(
            {
                "col_1": Array2D(shape=(2, 2), dtype="bool"),
                "col_2": Array3D(shape=(2, 2, 2), dtype="string"),
                "col_3": Sequence(feature=Value("int64")),
            }
        )
        assert dset[0]["col_2"] == [[["a", "b"], ["c", "d"]], [["e", "f"], ["g", "h"]]]
        assert dset["col_2"][0] == [[["a", "b"], ["c", "d"]], [["e", "f"], ["g", "h"]]]

    def test_dataset_getitem(self, in_memory, create_dummy_dataset):
        dset = create_dummy_dataset(in_memory)
        assert dset[0]["filename"] == "my_name-train_0"
        assert dset["filename"][0] == "my_name-train_0"

        assert dset[-1]["filename"] == "my_name-train_29"
        assert dset["filename"][-1] == "my_name-train_29"

        assert dset[:2]["filename"] == ["my_name-train_0", "my_name-train_1"]
        assert dset["filename"][:2] == ["my_name-train_0", "my_name-train_1"]

        assert dset[:-1]["filename"][-1] == "my_name-train_28"
        assert dset["filename"][:-1][-1] == "my_name-train_28"

        assert dset[[0, -1]]["filename"] == ["my_name-train_0", "my_name-train_29"]
        assert dset[np.array([0, -1])]["filename"] == ["my_name-train_0", "my_name-train_29"]

    def test_dummy_dataset_serialize(self, in_memory, create_dummy_dataset, tmp_dir, monkeypatch):
        with monkeypatch.context() as m:
            m.chdir(tmp_dir)
            dset = create_dummy_dataset(in_memory).select(range(10))
            dataset_path = "my_dataset_0"  # rel path
            dset.save_to_disk(dataset_path)

            dset = Dataset.load_from_disk(dataset_path)
            assert len(dset) == 10
            assert dset.features == Features({"filename": Value("string")})
            assert dset[0]["filename"] == "my_name-train_0"
            assert dset["filename"][0] == "my_name-train_0"

        dset = create_dummy_dataset(in_memory).select(range(10))
        dataset_path = os.path.join(tmp_dir, "my_dataset_1")  # abs path
        dset.save_to_disk(dataset_path)

        dset = Dataset.load_from_disk(dataset_path)
        assert len(dset) == 10
        assert dset.features == Features({"filename": Value("string")})
        assert dset[0]["filename"] == "my_name-train_0"
        assert dset["filename"][0] == "my_name-train_0"

        dset = create_dummy_dataset(in_memory).select(
            range(10), indices_cache_file_name=os.path.join(tmp_dir, "ind.arrow")
        )
        dataset_path = os.path.join(tmp_dir, "my_dataset_2")  # abs path
        with assert_arrow_memory_doesnt_increase():
            dset.save_to_disk(dataset_path)

        dset = Dataset.load_from_disk(dataset_path)
        assert len(dset) == 10
        assert dset.features == Features({"filename": Value("string")})
        assert dset[0]["filename"] == "my_name-train_0"
        assert dset["filename"][0] == "my_name-train_0"

    def test_dummy_dataset_load_from_disk(self, in_memory, create_dummy_dataset, tmp_dir):
        dset = create_dummy_dataset(in_memory).select(range(10))
        dataset_path = os.path.join(tmp_dir, "my_dataset")
        dset.save_to_disk(dataset_path)

        dset = load_from_disk(dataset_path)
        assert len(dset) == 10
        assert dset.features == Features({"filename": Value("string")})
        assert dset[0]["filename"] == "my_name-train_0"
        assert dset["filename"][0] == "my_name-train_0"

    def test_set_format_numpy_multiple_columns(self, in_memory, create_dummy_dataset):
        dset = create_dummy_dataset(in_memory, multiple_columns=True)
        fingerprint = dset._fingerprint
        dset.set_format(type="numpy", columns=["col_1"])
        assert len(dset[0]) == 1
        assert isinstance(dset[0]["col_1"], np.int64)
        assert dset[0]["col_1"].item() == 3
        assert isinstance(dset["col_1"], np.ndarray)
        assert list(dset["col_1"].shape) == [4]
        np.testing.assert_array_equal(dset["col_1"], np.array([3, 2, 1, 0]))
        assert dset._fingerprint != fingerprint

        dset.reset_format()
        with dset.formatted_as(type="numpy", columns=["col_1"]):
            assert len(dset[0]) == 1
            assert isinstance(dset[0]["col_1"], np.int64)
            assert dset[0]["col_1"].item() == 3
            assert isinstance(dset["col_1"], np.ndarray)
            assert list(dset["col_1"].shape) == [4]
            np.testing.assert_array_equal(dset["col_1"], np.array([3, 2, 1, 0]))

        assert dset.format["type"] is None
        assert dset.format["format_kwargs"] == {}
        assert dset.format["columns"] == dset.column_names
        assert dset.format["output_all_columns"] is False

        dset.set_format(type="numpy", columns=["col_1"], output_all_columns=True)
        assert len(dset[0]) == 3
        assert isinstance(dset[0]["col_2"], str)
        assert dset[0]["col_2"] == "a"

        dset.set_format(type="numpy", columns=["col_1", "col_2"])
        assert len(dset[0]) == 2
        assert isinstance(dset[0]["col_2"], np.str_)
        assert dset[0]["col_2"].item() == "a"

    @require_torch
    def test_set_format_torch(self, in_memory, create_dummy_dataset):
        import torch

        dset = create_dummy_dataset(in_memory, multiple_columns=True)
        dset.set_format(type="torch", columns=["col_1"])
        assert len(dset[0]) == 1
        assert isinstance(dset[0]["col_1"], torch.Tensor)
        assert isinstance(dset["col_1"], torch.Tensor)
        assert list(dset[0]["col_1"].shape) == []
        assert dset[0]["col_1"].item() == 3

        dset.set_format(type="torch", columns=["col_1"], output_all_columns=True)
        assert len(dset[0]) == 3
        assert isinstance(dset[0]["col_2"], str)
        assert dset[0]["col_2"] == "a"

        dset.set_format(type="torch", columns=["col_1", "col_2"])
        with pytest.raises(TypeError):
            dset[0]

    @require_tf
    def test_set_format_tf(self, in_memory, create_dummy_dataset):
        import tensorflow as tf

        dset = create_dummy_dataset(in_memory, multiple_columns=True)
        dset.set_format(type="tensorflow", columns=["col_1"])
        assert len(dset[0]) == 1
        assert isinstance(dset[0]["col_1"], tf.Tensor)
        assert list(dset[0]["col_1"].shape) == []
        assert dset[0]["col_1"].numpy().item() == 3

        dset.set_format(type="tensorflow", columns=["col_1"], output_all_columns=True)
        assert len(dset[0]) == 3
        assert isinstance(dset[0]["col_2"], str)
        assert dset[0]["col_2"] == "a"

        dset.set_format(type="tensorflow", columns=["col_1", "col_2"])
        assert len(dset[0]) == 2
        assert dset[0]["col_2"].numpy().decode("utf-8") == "a"

    def test_set_format_pandas(self, in_memory, create_dummy_dataset):
        dset = create_dummy_dataset(in_memory, multiple_columns=True)
        dset.set_format(type="pandas", columns=["col_1"])
        assert len(dset[0].columns) == 1
        assert isinstance(dset[0], pd.DataFrame)
        assert list(dset[0].shape) == [1, 1]
        assert dset[0]["col_1"].item() == 3

        dset.set_format(type="pandas", columns=["col_1", "col_2"])
        assert len(dset[0].columns) == 2
        assert dset[0]["col_2"].item() == "a"

    def test_set_transform(self, in_memory, create_dummy_dataset):
        def transform(batch):
            return {k: [str(i).upper() for i in v] for k, v in batch.items()}

        dset = create_dummy_dataset(in_memory, multiple_columns=True)
        dset.set_transform(transform=transform, columns=["col_1"])
        assert dset.format["type"] == "custom"
        assert len(dset[0].keys()) == 1
        assert dset[0]["col_1"] == "3"
        assert dset[:2]["col_1"] == ["3", "2"]
        assert dset["col_1"][:2] == ["3", "2"]

        prev_format = dset.format
        dset.set_format(**dset.format)
        assert prev_format == dset.format

        dset.set_transform(transform=transform, columns=["col_1", "col_2"])
        assert len(dset[0].keys()) == 2
        assert dset[0]["col_2"] == "A"

    def test_transmit_format(self, in_memory, create_dummy_dataset):
        dset = create_dummy_dataset(in_memory, multiple_columns=True)
        transform = datasets.arrow_dataset.transmit_format(lambda x: x)
        # make sure identity transform doesn't apply unnecessary format
        assert dset._fingerprint == transform(dset)._fingerprint
        dset.set_format(**dset.format)
        assert dset._fingerprint == transform(dset)._fingerprint
        # check lists comparisons
        dset.set_format(columns=["col_1"])
        assert dset._fingerprint == transform(dset)._fingerprint
        dset.set_format(columns=["col_1", "col_2"])
        assert dset._fingerprint == transform(dset)._fingerprint
        dset.set_format("numpy", columns=["col_1", "col_2"])
        assert dset._fingerprint == transform(dset)._fingerprint

    def test_cast_in_place(self, in_memory, create_dummy_dataset):
        dset = create_dummy_dataset(in_memory, multiple_columns=True)
        features = dset.features
        features["col_1"] = Value("float64")
        features = Features({k: features[k] for k in list(features)[::-1]})
        fingerprint = dset._fingerprint
        dset.cast_(features)
        assert dset.num_columns == 3
        assert dset.features["col_1"] == Value("float64")
        assert isinstance(dset[0]["col_1"], float)
        assert dset._fingerprint != fingerprint

    def test_cast(self, in_memory, create_dummy_dataset):
        dset = create_dummy_dataset(in_memory, multiple_columns=True)
        features = dset.features
        features["col_1"] = Value("float64")
        features = Features({k: features[k] for k in list(features)[::-1]})
        fingerprint = dset._fingerprint
        casted_dset = dset.cast(features)
        assert casted_dset.num_columns == 3
        assert casted_dset.features["col_1"] == Value("float64")
        assert isinstance(casted_dset[0]["col_1"], float)
        assert casted_dset._fingerprint != fingerprint
        assert casted_dset != dset

    def test_remove_columns_in_place(self, in_memory, create_dummy_dataset):
        dset = create_dummy_dataset(in_memory, multiple_columns=True)
        fingerprint = dset._fingerprint
        dset.remove_columns_(column_names="col_1")
        assert dset.num_columns == 2
        assert list(dset.column_names) == ["col_2", "col_3"]

        dset = create_dummy_dataset(in_memory, multiple_columns=True)
        dset.remove_columns_(column_names=["col_1", "col_2", "col_3"])
        assert dset.num_columns == 0
        assert dset._fingerprint != fingerprint

    def test_remove_columns(self, in_memory, create_dummy_dataset):
        # TODO: no need to mock remove_columns?!
        dset = create_dummy_dataset(in_memory, multiple_columns=True)
        fingerprint = dset._fingerprint
        new_dset = dset.remove_columns(column_names="col_1")
        assert new_dset.num_columns == 2
        assert list(new_dset.column_names) == ["col_2", "col_3"]
        assert new_dset._fingerprint != fingerprint

        dset = create_dummy_dataset(in_memory, multiple_columns=True)
        new_dset = dset.remove_columns(column_names=["col_1", "col_2", "col_3"])
        assert new_dset.num_columns == 0
        assert new_dset._fingerprint != fingerprint

    def test_rename_column_in_place(self, in_memory, create_dummy_dataset):
        dset = create_dummy_dataset(in_memory, multiple_columns=True)
        fingerprint = dset._fingerprint
        dset.rename_column_(original_column_name="col_1", new_column_name="new_name")
        assert dset.num_columns == 3
        assert list(dset.column_names) == ["new_name", "col_2", "col_3"]
        assert dset._fingerprint != fingerprint

    def test_rename_column(self, in_memory, create_dummy_dataset):
        dset = create_dummy_dataset(in_memory, multiple_columns=True)
        fingerprint = dset._fingerprint
        new_dset = dset.rename_column(original_column_name="col_1", new_column_name="new_name")
        assert new_dset.num_columns == 3
        assert list(new_dset.column_names) == ["new_name", "col_2", "col_3"]
        assert list(dset.column_names) == ["col_1", "col_2", "col_3"]
        assert new_dset._fingerprint != fingerprint

    def test_concatenate(self, in_memory, map_to):
        data1, data2, data3 = {"id": [0, 1, 2]}, {"id": [3, 4, 5]}, {"id": [6, 7]}
        info1 = DatasetInfo(description="Dataset1")
        info2 = DatasetInfo(description="Dataset2")
        dset1, dset2, dset3 = (
            Dataset.from_dict(data1, info=info1),
            Dataset.from_dict(data2, info=info2),
            Dataset.from_dict(data3),
        )
        dset1, dset2, dset3 = map_to(in_memory, dset1, dset2, dset3)

        dset_concat = datasets.concatenate_datasets([dset1, dset2, dset3])
        assert (len(dset1), len(dset2), len(dset3)) == (3, 3, 2)
        assert len(dset_concat) == len(dset1) + len(dset2) + len(dset3)
        assert dset_concat["id"] == [0, 1, 2, 3, 4, 5, 6, 7]
        assert len(dset_concat.cache_files) == 0 if in_memory else 3
        assert dset_concat.info.description == "Dataset1\n\nDataset2\n\n"

    def test_concatenate_formatted(self, in_memory, map_to):
        data1, data2, data3 = {"id": [0, 1, 2]}, {"id": [3, 4, 5]}, {"id": [6, 7]}
        info1 = DatasetInfo(description="Dataset1")
        info2 = DatasetInfo(description="Dataset2")
        dset1, dset2, dset3 = (
            Dataset.from_dict(data1, info=info1),
            Dataset.from_dict(data2, info=info2),
            Dataset.from_dict(data3),
        )
        dset1, dset2, dset3 = map_to(in_memory, dset1, dset2, dset3)

        dset1.set_format("numpy")
        dset_concat = datasets.concatenate_datasets([dset1, dset2, dset3])
        assert dset_concat.format["type"] is None
        dset2.set_format("numpy")
        dset3.set_format("numpy")
        dset_concat = datasets.concatenate_datasets([dset1, dset2, dset3])
        assert dset_concat.format["type"] == "numpy"

    def test_concatenate_with_indices(self, in_memory, map_to):
        data1, data2, data3 = {"id": [0, 1, 2] * 2}, {"id": [3, 4, 5] * 2}, {"id": [6, 7]}
        info1 = DatasetInfo(description="Dataset1")
        info2 = DatasetInfo(description="Dataset2")
        dset1, dset2, dset3 = (
            Dataset.from_dict(data1, info=info1),
            Dataset.from_dict(data2, info=info2),
            Dataset.from_dict(data3),
        )
        dset1, dset2, dset3 = map_to(in_memory, dset1, dset2, dset3)
        dset1, dset2, dset3 = dset1.select([0, 1, 2]), dset2.select([0, 1, 2]), dset3

        dset_concat = datasets.concatenate_datasets([dset1, dset2, dset3])
        assert (len(dset1), len(dset2), len(dset3)) == (3, 3, 2)
        assert len(dset_concat) == len(dset1) + len(dset2) + len(dset3)
        assert dset_concat["id"] == [0, 1, 2, 3, 4, 5, 6, 7]
        # in_memory = False:
        # 3 cache files for the dset_concat._data table, and 1 for the dset_concat._indices_table
        # no cache file for the indices
        # in_memory = True:
        # no cache files since both dset_concat._data and dset_concat._indices are in memory
        assert len(dset_concat.cache_files) == 0 if in_memory else 3
        assert dset_concat.info.description == "Dataset1\n\nDataset2\n\n"

    def test_concatenate_with_indices_from_disk(self, in_memory, map_to, tmp_dir):
        data1, data2, data3 = {"id": [0, 1, 2] * 2}, {"id": [3, 4, 5] * 2}, {"id": [6, 7]}
        info1 = DatasetInfo(description="Dataset1")
        info2 = DatasetInfo(description="Dataset2")
        dset1, dset2, dset3 = (
            Dataset.from_dict(data1, info=info1),
            Dataset.from_dict(data2, info=info2),
            Dataset.from_dict(data3),
        )
        dset1, dset2, dset3 = map_to(in_memory, dset1, dset2, dset3)
        dset1, dset2, dset3 = (
            dset1.select([0, 1, 2], indices_cache_file_name=os.path.join(tmp_dir, "i1.arrow")),
            dset2.select([0, 1, 2], indices_cache_file_name=os.path.join(tmp_dir, "i2.arrow")),
            dset3.select([0, 1], indices_cache_file_name=os.path.join(tmp_dir, "i3.arrow")),
        )

        dset_concat = datasets.concatenate_datasets([dset1, dset2, dset3])
        assert (len(dset1), len(dset2), len(dset3)) == (3, 3, 2)
        assert len(dset_concat) == len(dset1) + len(dset2) + len(dset3)
        assert dset_concat["id"] == [0, 1, 2, 3, 4, 5, 6, 7]
        # in_memory = False:
        # 3 cache files for the dset_concat._data table, and 1 for the dset_concat._indices_table
        # There is only 1 for the indices tables (i1.arrow)
        # Indeed, the others are brought to memory since an offset is applied to them.
        # in_memory = True:
        # 1 cache file for i1.arrow since both dset_concat._data and dset_concat._indices are in memory
        assert len(dset_concat.cache_files) == 1 if in_memory else 3 + 1
        assert dset_concat.info.description == "Dataset1\n\nDataset2\n\n"

    def test_flatten_in_place(self, in_memory, map_to):
        dset = Dataset.from_dict(
            {"a": [{"b": {"c": ["text"]}}] * 10, "foo": [1] * 10},
            features=Features({"a": {"b": Sequence({"c": Value("string")})}, "foo": Value("int64")}),
        )
        dset = map_to(in_memory, dset)
        fingerprint = dset._fingerprint
        dset.flatten_()
        assert dset.column_names == ["a.b.c", "foo"]
        assert list(dset.features.keys()) == ["a.b.c", "foo"]
        assert dset.features == Features({"a.b.c": Sequence(Value("string")), "foo": Value("int64")})
        assert dset._fingerprint != fingerprint

    # TODO: there are no tests for Dataset.flatten

    def test_map(self, in_memory, create_dummy_dataset, tmp_dir):
        # standard
        dset = create_dummy_dataset(in_memory)

        assert dset.features == Features({"filename": Value("string")})
        fingerprint = dset._fingerprint
        dset_test = dset.map(lambda x: {"name": x["filename"][:-2], "id": int(x["filename"].split("_")[-1])})
        assert len(dset_test) == 30
        assert dset.features == Features({"filename": Value("string")})
        assert dset_test.features == Features(
            {"filename": Value("string"), "name": Value("string"), "id": Value("int64")}
        )
        assert dset_test["id"] == list(range(30))
        assert dset_test._fingerprint != fingerprint

        # no transform
        dset = create_dummy_dataset(in_memory)
        fingerprint = dset._fingerprint
        dset_test = dset.map(lambda x: None)
        assert len(dset_test) == 30
        assert dset_test._fingerprint == fingerprint

        # with indices
        dset = create_dummy_dataset(in_memory)
        dset_test_with_indices = dset.map(lambda x, i: {"name": x["filename"][:-2], "id": i}, with_indices=True)
        assert len(dset_test_with_indices) == 30
        assert dset.features == Features({"filename": Value("string")})
        assert dset_test_with_indices.features == Features(
            {"filename": Value("string"), "name": Value("string"), "id": Value("int64")}
        )
        assert dset_test_with_indices["id"] == list(range(30))

        # interrupted
        dset = create_dummy_dataset(in_memory)

        def func(x, i):
            if i == 4:
                raise KeyboardInterrupt()
            return {"name": x["filename"][:-2], "id": i}

        tmp_file = os.path.join(tmp_dir, "test.arrow")
        with pytest.raises(KeyboardInterrupt):
            dset.map(
                function=func,
                with_indices=True,
                cache_file_name=tmp_file,
                writer_batch_size=2,
            )
        assert not os.path.exists(tmp_file)
        dset_test_with_indices = dset.map(
            lambda x, i: {"name": x["filename"][:-2], "id": i},
            with_indices=True,
            cache_file_name=tmp_file,
            writer_batch_size=2,
        )
        assert os.path.exists(tmp_file)
        assert len(dset_test_with_indices) == 30
        assert dset.features == Features({"filename": Value("string")})
        assert dset_test_with_indices.features == Features(
            {"filename": Value("string"), "name": Value("string"), "id": Value("int64")}
        )
        assert dset_test_with_indices["id"] == list(range(30))

        # formatted
        dset = create_dummy_dataset(in_memory, multiple_columns=True)
        dset.set_format("numpy", columns=["col_1"])

        dset_test = dset.map(lambda x: {"col_1_plus_one": x["col_1"] + 1})
        assert len(dset_test) == 4
        assert dset_test.format["type"] == "numpy"
        assert isinstance(dset_test["col_1"], np.ndarray)
        assert isinstance(dset_test["col_1_plus_one"], np.ndarray)
        assert sorted(dset_test[0].keys()) == ["col_1", "col_1_plus_one"]
        assert sorted(dset_test.column_names) == ["col_1", "col_1_plus_one", "col_2", "col_3"]

    def test_map_multiprocessing(self, in_memory, create_dummy_dataset):
        # standard
        dset = create_dummy_dataset(in_memory)
        assert dset.features == Features({"filename": Value("string")})
        fingerprint = dset._fingerprint
        dset_test = dset.map(picklable_map_function, num_proc=2)
        assert len(dset_test) == 30
        assert dset.features == Features({"filename": Value("string")})
        assert dset_test.features == Features({"filename": Value("string"), "id": Value("int64")})
        assert len(dset_test.cache_files) == 0 if in_memory else 2
        assert dset_test["id"] == list(range(30))
        assert dset_test._fingerprint != fingerprint

        # with_indices
        dset = create_dummy_dataset(in_memory)
        fingerprint = dset._fingerprint
        dset_test = dset.map(picklable_map_function_with_indices, num_proc=3, with_indices=True)
        assert len(dset_test) == 30
        assert dset.features == Features({"filename": Value("string")})
        assert dset_test.features == Features({"filename": Value("string"), "id": Value("int64")})
        assert len(dset_test.cache_files) == 0 if in_memory else 3
        assert dset_test["id"] == list(range(30))
        assert dset_test._fingerprint != fingerprint

        # lambda (requires multiprocess from pathos)
        dset = create_dummy_dataset(in_memory)
        fingerprint = dset._fingerprint
        dset_test = dset.map(lambda x: {"id": int(x["filename"].split("_")[-1])}, num_proc=2)
        assert len(dset_test) == 30
        assert dset.features == Features({"filename": Value("string")})
        assert dset_test.features == Features({"filename": Value("string"), "id": Value("int64")})
        assert len(dset_test.cache_files) == 0 if in_memory else 2
        assert dset_test["id"] == list(range(30))
        assert dset_test._fingerprint != fingerprint

    def test_new_features(self, in_memory, create_dummy_dataset):
        dset = create_dummy_dataset(in_memory)
        features = Features({"filename": Value("string"), "label": ClassLabel(names=["positive", "negative"])})
        dset_test_with_indices = dset.map(lambda x, i: {"label": i % 2}, with_indices=True, features=features)
        assert len(dset_test_with_indices) == 30
        assert dset_test_with_indices.features == features

    def test_map_batched(self, in_memory, create_dummy_dataset):
        def map_batched(example):
            return {"filename_new": [x + "_extension" for x in example["filename"]]}

        dset = create_dummy_dataset(in_memory)
        dset_test_batched = dset.map(map_batched, batched=True)
        assert len(dset_test_batched) == 30
        assert dset.features == Features({"filename": Value("string")})
        assert dset_test_batched.features == Features({"filename": Value("string"), "filename_new": Value("string")})

        dset = create_dummy_dataset(in_memory)
        with dset.formatted_as("numpy", columns=["filename"]):
            dset_test_batched = dset.map(map_batched, batched=True)
            assert len(dset_test_batched) == 30
            assert dset.features == Features({"filename": Value("string")})
            assert dset_test_batched.features == Features(
                {"filename": Value("string"), "filename_new": Value("string")}
            )

        def map_batched_with_indices(example, idx):
            return {"filename_new": [x + "_extension_" + str(idx) for x in example["filename"]]}

        dset = create_dummy_dataset(in_memory)
        dset_test_with_indices_batched = dset.map(map_batched_with_indices, batched=True, with_indices=True)
        assert len(dset_test_with_indices_batched) == 30
        assert dset.features == Features({"filename": Value("string")})
        assert dset_test_with_indices_batched.features == Features(
            {"filename": Value("string"), "filename_new": Value("string")}
        )

    def test_map_nested(self, in_memory, map_to):
        dset = Dataset.from_dict({"field": ["a", "b"]})
        dset = map_to(in_memory, dset)
        dset = dset.map(lambda example: {"otherfield": {"capital": example["field"].capitalize()}})
        dset = dset.map(lambda example: {"otherfield": {"append_x": example["field"] + "x"}})
        assert dset[0] == {"field": "a", "otherfield": {"append_x": "ax"}}


@pytest.mark.parametrize("keep_in_memory", [False, True])
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
@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
@pytest.mark.parametrize("path_type", [str, list])
def test_dataset_from_csv(path_type, split, features, keep_in_memory, csv_path, tmp_path):
    if issubclass(path_type, str):
        path = csv_path
    elif issubclass(path_type, list):
        path = [csv_path]
    cache_dir = tmp_path / "cache"
    expected_split = str(split) if split else "train"
    # CSV file loses col_1 string dtype information: default now is "int64" instead of "string"
    default_expected_features = {"col_1": "int64", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = Features({feature: Value(dtype) for feature, dtype in features.items()}) if features else None
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = Dataset.from_csv(
            path, split=split, features=features, cache_dir=cache_dir, keep_in_memory=keep_in_memory
        )
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 4
    assert dataset.num_columns == 3
    assert dataset.column_names == ["col_1", "col_2", "col_3"]
    assert dataset.split == expected_split
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("in_memory", [False, True])
def test_dataset_from_file(in_memory, dataset, arrow_file):
    filename = arrow_file
    with assert_arrow_memory_increases() if in_memory else assert_arrow_memory_doesnt_increase():
        dataset_from_file = Dataset.from_file(filename, in_memory=in_memory)
    assert dataset_from_file.features.type == dataset.features.type
    assert dataset_from_file.features == dataset.features
    assert dataset_from_file.cache_files == ([filename] if not in_memory else [])


@pytest.mark.parametrize("keep_in_memory", [False, True])
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
@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
@pytest.mark.parametrize("path_type", [str, list])
def test_dataset_from_json(
    path_type,
    split,
    features,
    keep_in_memory,
    jsonl_path,
    tmp_path,
):
    file_path = jsonl_path
    field = None
    if issubclass(path_type, str):
        path = file_path
    elif issubclass(path_type, list):
        path = [file_path]
    cache_dir = tmp_path / "cache"
    expected_split = str(split) if split else "train"
    default_expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = Features({feature: Value(dtype) for feature, dtype in features.items()}) if features else None
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = Dataset.from_json(
            path, split=split, features=features, cache_dir=cache_dir, keep_in_memory=keep_in_memory, field=field
        )
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 4
    assert dataset.num_columns == 3
    assert dataset.column_names == ["col_1", "col_2", "col_3"]
    assert dataset.split == expected_split
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("keep_in_memory", [False, True])
@pytest.mark.parametrize(
    "features",
    [
        None,
        {"text": "string"},
        {"text": "int32"},
        {"text": "float32"},
    ],
)
@pytest.mark.parametrize("split", [None, NamedSplit("train"), "train", "test"])
@pytest.mark.parametrize("path_type", [str, list])
def test_dataset_from_text(path_type, split, features, keep_in_memory, text_path, tmp_path):
    if issubclass(path_type, str):
        path = text_path
    elif issubclass(path_type, list):
        path = [text_path]
    cache_dir = tmp_path / "cache"

    expected_split = str(split) if split else "train"

    default_expected_features = {"text": "string"}
    expected_features = features.copy() if features else default_expected_features
    features = Features({feature: Value(dtype) for feature, dtype in features.items()}) if features else None
    with assert_arrow_memory_increases() if keep_in_memory else assert_arrow_memory_doesnt_increase():
        dataset = Dataset.from_text(
            path, split=split, features=features, cache_dir=cache_dir, keep_in_memory=keep_in_memory
        )
    assert isinstance(dataset, Dataset)
    assert dataset.num_rows == 4
    assert dataset.num_columns == 1
    assert dataset.column_names == ["text"]
    assert dataset.split == expected_split
    for feature, expected_dtype in expected_features.items():
        assert dataset.features[feature].dtype == expected_dtype


@pytest.mark.parametrize("in_memory", [False, True])
@pytest.mark.parametrize(
    "method_and_params",
    [
        ("rename_column", tuple(), {"original_column_name": "labels", "new_column_name": "label"}),
        ("remove_columns", tuple(), {"column_names": "labels"}),
        (
            "cast",
            tuple(),
            {
                "features": Features(
                    {
                        "tokens": Sequence(Value("string")),
                        "labels": Sequence(Value("int16")),
                        "answers": Sequence(
                            {
                                "text": Value("string"),
                                "answer_start": Value("int32"),
                            }
                        ),
                        "id": Value("int32"),
                    }
                )
            },
        ),
        ("flatten", tuple(), {}),
        ("rename_column_", tuple(), {"original_column_name": "labels", "new_column_name": "label"}),
        ("remove_columns_", tuple(), {"column_names": "labels"}),
        (
            "cast_",
            tuple(),
            {
                "features": Features(
                    {
                        "tokens": Sequence(Value("string")),
                        "labels": Sequence(Value("int16")),
                        "answers": Sequence(
                            {
                                "text": Value("string"),
                                "answer_start": Value("int32"),
                            }
                        ),
                        "id": Value("int32"),
                    }
                )
            },
        ),
        ("flatten_", tuple(), {}),
    ],
)
def test_pickle_dataset_after_transforming_the_table(in_memory, method_and_params, arrow_file):
    method, args, kwargs = method_and_params
    dataset = Dataset.from_file(arrow_file, in_memory=in_memory)
    reference_dataset = Dataset.from_file(arrow_file, in_memory=in_memory)

    out = getattr(dataset, method)(*args, **kwargs)
    dataset = out if out is not None else dataset
    pickled_dataset = pickle.dumps(dataset)
    reloaded_dataset = pickle.loads(pickled_dataset)

    assert dataset._data != reference_dataset._data
    assert dataset._data.table == reloaded_dataset._data.table
