import os
import tempfile
import unittest

import numpy as np
import pandas as pd
from absl.testing import parameterized

import datasets
from datasets.arrow_writer import ArrowWriter
from datasets.features import Array2D, Array3D, Array4D, Array5D, Value, _ArrayXD


SHAPE_TEST_1 = (30, 487)
SHAPE_TEST_2 = (36, 1024)
SPEED_TEST_SHAPE = (100, 100)
SPEED_TEST_N_EXAMPLES = 100

DEFAULT_FEATURES = datasets.Features(
    {"text": Array2D(SHAPE_TEST_1, dtype="float32"), "image": Array2D(SHAPE_TEST_2, dtype="float32")}
)


def generate_examples(features: dict, num_examples=100, seq_shapes=None):
    dummy_data = []
    seq_shapes = seq_shapes or {}
    for i in range(num_examples):
        example = {}
        for col_id, (k, v) in enumerate(features.items()):
            if isinstance(v, _ArrayXD):
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
            writer = ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow"))
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
            writer = ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow"))
            for key, record in generate_examples(features=my_features, num_examples=1):
                example = my_features.encode_example(record)
                writer.write(example)
            num_examples, num_bytes = writer.finalize()
            dataset = datasets.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))
            dataset.set_format("numpy")
            row = dataset[0]
            first_len = len(row["image"].shape)
            second_len = len(row["text"].shape)
            self.assertEqual(first_len, 2, "use a sequence type if dim is  < 2")
            self.assertEqual(second_len, 2, "use a sequence type if dim is  < 2")
            del dataset

    def test_compatability_with_string_values(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            my_features = DEFAULT_FEATURES.copy()
            my_features["image_id"] = datasets.Value("string")
            writer = ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow"))
            for key, record in generate_examples(features=my_features, num_examples=1):
                example = my_features.encode_example(record)
                writer.write(example)
            num_examples, num_bytes = writer.finalize()
            dataset = datasets.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))
            self.assertTrue(isinstance(dataset[0]["image_id"], str), "image id must be of type string")
            del dataset

    def test_extension_indexing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            my_features = DEFAULT_FEATURES.copy()
            my_features["explicit_ext"] = Array2D((3, 3), dtype="float32")
            writer = ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow"))
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
            "testcase_name": "{}d".format(d),
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
            writer = ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow"))
            my_examples = [
                (0, self.get_dict_example_0(shape_1, shape_2)),
                (1, self.get_dict_example_1(shape_1, shape_2)),
            ]
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
            writer = ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow"))

            dict_examples = self.get_dict_examples(shape_1, shape_2)
            dict_examples = my_features.encode_batch(dict_examples)
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
