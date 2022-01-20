import os
import random
import tempfile
import unittest

import numpy as np
import pandas as pd
import pytest
from absl.testing import parameterized

import datasets
from datasets.arrow_writer import ArrowWriter
from datasets.features import Array2D, Array3D, Array3DExtensionType, Array4D, Array5D, Value, _ArrayXD
from datasets.formatting.formatting import NumpyArrowExtractor, SimpleArrowExtractor


SHAPE_TEST_1 = (30, 487)
SHAPE_TEST_2 = (36, 1024)
SHAPE_TEST_3 = (None, 100)
SPEED_TEST_SHAPE = (100, 100)
SPEED_TEST_N_EXAMPLES = 100

DEFAULT_FEATURES = datasets.Features(
    {
        "text": Array2D(SHAPE_TEST_1, dtype="float32"),
        "image": Array2D(SHAPE_TEST_2, dtype="float32"),
        "dynamic": Array2D(SHAPE_TEST_3, dtype="float32"),
    }
)


def generate_examples(features: dict, num_examples=100, seq_shapes=None):
    dummy_data = []
    seq_shapes = seq_shapes or {}
    for i in range(num_examples):
        example = {}
        for col_id, (k, v) in enumerate(features.items()):
            if isinstance(v, _ArrayXD):
                if k == "dynamic":
                    first_dim = random.randint(1, 3)
                    data = np.random.rand(first_dim, *v.shape[1:]).astype(v.dtype)
                else:
                    data = np.random.rand(*v.shape).astype(v.dtype)
            elif isinstance(v, datasets.Value):
                data = "foo"
            elif isinstance(v, datasets.Sequence):
                while isinstance(v, datasets.Sequence):
                    v = v.feature
                shape = seq_shapes[k]
                data = np.random.rand(*shape).astype(v.dtype)
            example[k] = data
            dummy_data.append((i, example))

    return dummy_data


class ExtensionTypeCompatibilityTest(unittest.TestCase):
    def test_array2d_nonspecific_shape(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            my_features = DEFAULT_FEATURES.copy()
            with ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow")) as writer:
                for key, record in generate_examples(
                    features=my_features,
                    num_examples=1,
                ):
                    example = my_features.encode_example(record)
                    writer.write(example)
                num_examples, num_bytes = writer.finalize()
            dataset = datasets.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))
            dataset.set_format("numpy")
            row = dataset[0]
            first_shape = row["image"].shape
            second_shape = row["text"].shape
            self.assertTrue(first_shape is not None and second_shape is not None, "need atleast 2 different shapes")
            self.assertEqual(len(first_shape), len(second_shape), "both shapes are supposed to be equal length")
            self.assertNotEqual(first_shape, second_shape, "shapes must not be the same")
            del dataset

    def test_multiple_extensions_same_row(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            my_features = DEFAULT_FEATURES.copy()
            with ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow")) as writer:
                for key, record in generate_examples(features=my_features, num_examples=1):
                    example = my_features.encode_example(record)
                    writer.write(example)
                num_examples, num_bytes = writer.finalize()
            dataset = datasets.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))
            dataset.set_format("numpy")
            row = dataset[0]
            first_len = len(row["image"].shape)
            second_len = len(row["text"].shape)
            third_len = len(row["dynamic"].shape)
            self.assertEqual(first_len, 2, "use a sequence type if dim is  < 2")
            self.assertEqual(second_len, 2, "use a sequence type if dim is  < 2")
            self.assertEqual(third_len, 2, "use a sequence type if dim is  < 2")
            del dataset

    def test_compatability_with_string_values(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            my_features = DEFAULT_FEATURES.copy()
            my_features["image_id"] = datasets.Value("string")
            with ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow")) as writer:
                for key, record in generate_examples(features=my_features, num_examples=1):
                    example = my_features.encode_example(record)
                    writer.write(example)
                num_examples, num_bytes = writer.finalize()
            dataset = datasets.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))
            self.assertIsInstance(dataset[0]["image_id"], str, "image id must be of type string")
            del dataset

    def test_extension_indexing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            my_features = DEFAULT_FEATURES.copy()
            my_features["explicit_ext"] = Array2D((3, 3), dtype="float32")
            with ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow")) as writer:
                for key, record in generate_examples(features=my_features, num_examples=1):
                    example = my_features.encode_example(record)
                    writer.write(example)
                num_examples, num_bytes = writer.finalize()
            dataset = datasets.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))
            dataset.set_format("numpy")
            data = dataset[0]["explicit_ext"]
            self.assertIsInstance(data, np.ndarray, "indexed extension must return numpy.ndarray")
            del dataset


def get_array_feature_types():
    shape_1 = [3] * 5
    shape_2 = [3, 4, 5, 6, 7]
    return [
        {
            "testcase_name": f"{d}d",
            "array_feature": array_feature,
            "shape_1": tuple(shape_1[:d]),
            "shape_2": tuple(shape_2[:d]),
        }
        for d, array_feature in zip(range(2, 6), [Array2D, Array3D, Array4D, Array5D])
    ]


@parameterized.named_parameters(get_array_feature_types())
class ArrayXDTest(unittest.TestCase):
    def get_features(self, array_feature, shape_1, shape_2):
        return datasets.Features(
            {
                "image": array_feature(shape_1, dtype="float32"),
                "source": Value("string"),
                "matrix": array_feature(shape_2, dtype="float32"),
            }
        )

    def get_dict_example_0(self, shape_1, shape_2):
        return {
            "image": np.random.rand(*shape_1).astype("float32"),
            "source": "foo",
            "matrix": np.random.rand(*shape_2).astype("float32"),
        }

    def get_dict_example_1(self, shape_1, shape_2):
        return {
            "image": np.random.rand(*shape_1).astype("float32"),
            "matrix": np.random.rand(*shape_2).astype("float32"),
            "source": "bar",
        }

    def get_dict_examples(self, shape_1, shape_2):
        return {
            "image": np.random.rand(2, *shape_1).astype("float32").tolist(),
            "source": ["foo", "bar"],
            "matrix": np.random.rand(2, *shape_2).astype("float32").tolist(),
        }

    def _check_getitem_output_type(self, dataset, shape_1, shape_2, first_matrix):
        matrix_column = dataset["matrix"]
        self.assertIsInstance(matrix_column, list)
        self.assertIsInstance(matrix_column[0], list)
        self.assertIsInstance(matrix_column[0][0], list)
        self.assertEqual(np.array(matrix_column).shape, (2, *shape_2))

        matrix_field_of_first_example = dataset[0]["matrix"]
        self.assertIsInstance(matrix_field_of_first_example, list)
        self.assertIsInstance(matrix_field_of_first_example, list)
        self.assertEqual(np.array(matrix_field_of_first_example).shape, shape_2)
        np.testing.assert_array_equal(np.array(matrix_field_of_first_example), np.array(first_matrix))

        matrix_field_of_first_two_examples = dataset[:2]["matrix"]
        self.assertIsInstance(matrix_field_of_first_two_examples, list)
        self.assertIsInstance(matrix_field_of_first_two_examples[0], list)
        self.assertIsInstance(matrix_field_of_first_two_examples[0][0], list)
        self.assertEqual(np.array(matrix_field_of_first_two_examples).shape, (2, *shape_2))

        with dataset.formatted_as("numpy"):
            self.assertEqual(dataset["matrix"].shape, (2, *shape_2))
            self.assertEqual(dataset[0]["matrix"].shape, shape_2)
            self.assertEqual(dataset[:2]["matrix"].shape, (2, *shape_2))

        with dataset.formatted_as("pandas"):
            self.assertIsInstance(dataset["matrix"], pd.Series)
            self.assertIsInstance(dataset[0]["matrix"], pd.Series)
            self.assertIsInstance(dataset[:2]["matrix"], pd.Series)
            self.assertEqual(dataset["matrix"].to_numpy().shape, (2, *shape_2))
            self.assertEqual(dataset[0]["matrix"].to_numpy().shape, (1, *shape_2))
            self.assertEqual(dataset[:2]["matrix"].to_numpy().shape, (2, *shape_2))

    def test_write(self, array_feature, shape_1, shape_2):
        with tempfile.TemporaryDirectory() as tmp_dir:
            my_features = self.get_features(array_feature, shape_1, shape_2)
            my_examples = [
                (0, self.get_dict_example_0(shape_1, shape_2)),
                (1, self.get_dict_example_1(shape_1, shape_2)),
            ]
            with ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow")) as writer:
                for key, record in my_examples:
                    example = my_features.encode_example(record)
                    writer.write(example)
                num_examples, num_bytes = writer.finalize()
            dataset = datasets.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))
            self._check_getitem_output_type(dataset, shape_1, shape_2, my_examples[0][1]["matrix"])
            del dataset

    def test_write_batch(self, array_feature, shape_1, shape_2):
        with tempfile.TemporaryDirectory() as tmp_dir:
            my_features = self.get_features(array_feature, shape_1, shape_2)
            dict_examples = self.get_dict_examples(shape_1, shape_2)
            dict_examples = my_features.encode_batch(dict_examples)
            with ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow")) as writer:
                writer.write_batch(dict_examples)
                num_examples, num_bytes = writer.finalize()
            dataset = datasets.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))
            self._check_getitem_output_type(dataset, shape_1, shape_2, dict_examples["matrix"][0])
            del dataset

    def test_from_dict(self, array_feature, shape_1, shape_2):
        dict_examples = self.get_dict_examples(shape_1, shape_2)
        dataset = datasets.Dataset.from_dict(
            dict_examples, features=self.get_features(array_feature, shape_1, shape_2)
        )
        self._check_getitem_output_type(dataset, shape_1, shape_2, dict_examples["matrix"][0])
        del dataset


class ArrayXDDynamicTest(unittest.TestCase):
    def get_one_col_dataset(self, first_dim_list, fixed_shape):
        features = datasets.Features({"image": Array3D(shape=(None, *fixed_shape), dtype="float32")})
        dict_values = {"image": [np.random.rand(fdim, *fixed_shape).astype("float32") for fdim in first_dim_list]}
        dataset = datasets.Dataset.from_dict(dict_values, features=features)
        return dataset

    def get_two_col_datasset(self, first_dim_list, fixed_shape):
        features = datasets.Features(
            {"image": Array3D(shape=(None, *fixed_shape), dtype="float32"), "text": Value("string")}
        )
        dict_values = {
            "image": [np.random.rand(fdim, *fixed_shape).astype("float32") for fdim in first_dim_list],
            "text": ["text" for _ in first_dim_list],
        }
        dataset = datasets.Dataset.from_dict(dict_values, features=features)
        return dataset

    def test_to_pylist(self):
        fixed_shape = (2, 2)
        first_dim_list = [1, 3, 10]
        dataset = self.get_one_col_dataset(first_dim_list, fixed_shape)
        arr_xd = SimpleArrowExtractor().extract_column(dataset._data)
        self.assertIsInstance(arr_xd.type, Array3DExtensionType)
        pylist = arr_xd.to_pylist()

        for first_dim, single_arr in zip(first_dim_list, pylist):
            self.assertIsInstance(single_arr, np.ndarray)
            self.assertEqual(single_arr.shape, (first_dim, *fixed_shape))

    def test_iter_dataset(self):
        fixed_shape = (2, 2)
        first_dim_list = [1, 3, 10]
        dataset = self.get_one_col_dataset(first_dim_list, fixed_shape)

        for first_dim, ds_row in zip(first_dim_list, dataset):
            single_arr = ds_row["image"]
            self.assertIsInstance(single_arr, np.ndarray)
            self.assertEqual(single_arr.shape, (first_dim, *fixed_shape))

    def test_to_pandas_fail(self):
        fixed_shape = (2, 2)
        first_dim_list = [1, 3, 10]
        dataset = self.get_one_col_dataset(first_dim_list, fixed_shape)
        with self.assertRaises(NotImplementedError):
            dataset.to_pandas()

    def test_map_dataset(self):
        fixed_shape = (2, 2)
        first_dim_list = [1, 3, 10]
        dataset = self.get_one_col_dataset(first_dim_list, fixed_shape)

        dataset = dataset.map(lambda a: {"image": np.concatenate([a] * 2)}, input_columns="image")

        # check also if above function resulted with 2x bigger first dim
        for first_dim, ds_row in zip(first_dim_list, dataset):
            single_arr = ds_row["image"]
            self.assertIsInstance(single_arr, np.ndarray)
            self.assertEqual(single_arr.shape, (first_dim * 2, *fixed_shape))


@pytest.mark.parametrize("dtype, dummy_value", [("int32", 1), ("bool", True), ("float64", 1)])
def test_table_to_pandas(dtype, dummy_value):
    features = datasets.Features({"foo": datasets.Array2D(dtype=dtype, shape=(2, 2))})
    dataset = datasets.Dataset.from_dict({"foo": [[[dummy_value] * 2] * 2]}, features=features)
    df = dataset._data.to_pandas()
    assert type(df.foo.dtype) == datasets.features.PandasArrayExtensionDtype
    arr = df.foo.to_numpy()
    np.testing.assert_equal(arr, np.array([[[dummy_value] * 2] * 2], dtype=np.dtype(dtype)))


@pytest.mark.parametrize("dtype, dummy_value", [("int32", 1), ("bool", True), ("float64", 1)])
def test_array_xd_numpy_arrow_extractor(dtype, dummy_value):
    features = datasets.Features({"foo": datasets.Array2D(dtype=dtype, shape=(2, 2))})
    dataset = datasets.Dataset.from_dict({"foo": [[[dummy_value] * 2] * 2]}, features=features)
    arr = NumpyArrowExtractor().extract_column(dataset._data)
    assert isinstance(arr, np.ndarray)
    np.testing.assert_equal(arr, np.array([[[dummy_value] * 2] * 2], dtype=np.dtype(dtype)))


def test_array_xd_with_none():
    # Fixed shape
    features = datasets.Features({"foo": datasets.Array2D(dtype="int32", shape=(2, 2))})
    dummy_array = np.array([[1, 2], [3, 4]], dtype="int32")
    dataset = datasets.Dataset.from_dict({"foo": [dummy_array, None, dummy_array]}, features=features)
    arr = NumpyArrowExtractor().extract_column(dataset._data)
    assert isinstance(arr, np.ndarray) and arr.dtype == np.float64 and arr.shape == (3, 2, 2)
    assert np.allclose(arr[0], dummy_array) and np.allclose(arr[2], dummy_array)
    assert np.all(np.isnan(arr[1]))  # broadcasted np.nan - use np.all

    # Dynamic shape
    features = datasets.Features({"foo": datasets.Array2D(dtype="int32", shape=(None, 2))})
    dummy_array = np.array([[1, 2], [3, 4]], dtype="int32")
    dataset = datasets.Dataset.from_dict({"foo": [dummy_array, None, dummy_array]}, features=features)
    arr = NumpyArrowExtractor().extract_column(dataset._data)
    assert isinstance(arr, np.ndarray) and arr.dtype == np.object and arr.shape == (3,)
    np.testing.assert_equal(arr[0], dummy_array)
    np.testing.assert_equal(arr[2], dummy_array)
    assert np.isnan(arr[1])  # a single np.nan value - np.all not needed


@pytest.mark.parametrize("with_none", [False, True])
def test_dataset_map(with_none):
    ds = datasets.Dataset.from_dict({"path": ["path1", "path2"]})

    def process_data(batch):
        batch = {
            "image": [
                np.array(
                    [
                        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                        [[10, 20, 30], [40, 50, 60], [70, 80, 90]],
                        [[100, 200, 300], [400, 500, 600], [700, 800, 900]],
                    ]
                )
                for _ in batch["path"]
            ]
        }
        if with_none:
            batch["image"][0] = None
        return batch

    features = datasets.Features({"image": Array3D(dtype="int32", shape=(3, 3, 3))})
    processed_ds = ds.map(process_data, batched=True, remove_columns=ds.column_names, features=features)
    assert processed_ds.shape == (2, 1)
    with processed_ds.with_format("numpy") as pds:
        for i, example in enumerate(pds):
            assert "image" in example
            assert isinstance(example["image"], np.ndarray)
            assert example["image"].shape == (3, 3, 3)
            if with_none and i == 0:
                assert np.all(np.isnan(example["image"]))
