import os
import tempfile
import timeit
import unittest
from warnings import warn

import numpy as np
import pandas as pd
from absl.testing import parameterized

import nlp
from nlp.arrow_writer import ArrowWriter
from nlp.features import Array2D, Array3D, Array4D, Array5D, Value, _ArrayXD


SHAPE_TEST_1 = (30, 487)
SHAPE_TEST_2 = (36, 1024)
SPEED_TEST_SHAPE = (100, 100)
SPEED_TEST_N_EXAMPLES = 100

DEFAULT_FEATURES = nlp.Features(
    {"text": Array2D(SHAPE_TEST_1, dtype="float32"), "image": Array2D(SHAPE_TEST_2, dtype="float32")}
)


def get_duration(func):
    def wrapper(*args, **kwargs):
        starttime = timeit.default_timer()
        _ = func(*args, **kwargs)
        delta = timeit.default_timer() - starttime
        return delta

    wrapper.__name__ = func.__name__

    return wrapper


def generate_examples(features: dict, num_examples=100):
    dummy_data = []
    for i in range(num_examples):
        example = {}
        for col_id, (k, v) in enumerate(features.items()):
            if isinstance(v, _ArrayXD):
                data = np.random.rand(*v.shape).astype(v.dtype)
            elif isinstance(v, nlp.Value):
                data = "foo"
            elif isinstance(v, nlp.Sequence):
                shape = []
                while isinstance(v, nlp.Sequence):
                    shape.append(v.length)
                    v = v.feature
                data = np.random.rand(*shape).astype(v.dtype)
            example[k] = data
            dummy_data.append((i, example))

    return dummy_data


@get_duration
def write_array2d(feats, dummy_data, tmp_dir):
    my_features = nlp.Features(feats)
    writer = ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow"))
    for key, record in dummy_data:
        example = my_features.encode_example(record)
        writer.write(example)
    num_examples, num_bytes = writer.finalize()


@get_duration
def write_nested_sequence(feats, dummy_data, tmp_dir):
    my_features = nlp.Features(feats)
    writer = ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow"))
    for key, record in dummy_data:
        example = my_features.encode_example(record)
        writer.write(example)
    num_examples, num_bytes = writer.finalize()


@get_duration
def write_flattened_sequence(feats, dummy_data, tmp_dir):
    my_features = nlp.Features(feats)
    writer = ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow"))
    for key, record in dummy_data:
        example = my_features.encode_example(record)
        writer.write(example)
    num_examples, num_bytes = writer.finalize()


@get_duration
def read_unformated(feats, tmp_dir):
    dataset = nlp.Dataset.from_file(filename=os.path.join(tmp_dir, "beta.arrow"), info=nlp.DatasetInfo(features=feats))
    for _ in dataset:
        pass


@get_duration
def read_formatted_as_numpy(feats, tmp_dir):
    dataset = nlp.Dataset.from_file(filename=os.path.join(tmp_dir, "beta.arrow"), info=nlp.DatasetInfo(features=feats))
    dataset.set_format("numpy")
    for _ in dataset:
        pass


@get_duration
def read_batch_unformated(feats, tmp_dir):
    batch_size = 10
    dataset = nlp.Dataset.from_file(filename=os.path.join(tmp_dir, "beta.arrow"), info=nlp.DatasetInfo(features=feats))
    for i in range(0, len(dataset), batch_size):
        _ = dataset[i : i + batch_size]


@get_duration
def read_batch_formatted_as_numpy(feats, tmp_dir):
    batch_size = 10
    dataset = nlp.Dataset.from_file(filename=os.path.join(tmp_dir, "beta.arrow"), info=nlp.DatasetInfo(features=feats))
    dataset.set_format("numpy")
    for i in range(0, len(dataset), batch_size):
        _ = dataset[i : i + batch_size]


@get_duration
def read_col_unformated(feats, tmp_dir):
    dataset = nlp.Dataset.from_file(filename=os.path.join(tmp_dir, "beta.arrow"), info=nlp.DatasetInfo(features=feats))
    for col in feats:
        _ = dataset[col]


@get_duration
def read_col_formatted_as_numpy(feats, tmp_dir):
    dataset = nlp.Dataset.from_file(filename=os.path.join(tmp_dir, "beta.arrow"), info=nlp.DatasetInfo(features=feats))
    dataset.set_format("numpy")
    for col in feats:
        _ = dataset[col]


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
            dataset = nlp.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))
            dataset.set_format("numpy")
            row = dataset[0]
            first_shape = row["image"].shape
            second_shape = row["text"].shape
            self.assertTrue(first_shape is not None and second_shape is not None, "need atleast 2 different shapes")
            self.assertEqual(len(first_shape), len(second_shape), "both shapes are supposed to be equal length")
            self.assertNotEqual(first_shape, second_shape, "shapes must not be the same")

    def test_multiple_extensions_same_row(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            my_features = DEFAULT_FEATURES.copy()
            writer = ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow"))
            for key, record in generate_examples(features=my_features, num_examples=1):
                example = my_features.encode_example(record)
                writer.write(example)
            num_examples, num_bytes = writer.finalize()
            dataset = nlp.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))
            dataset.set_format("numpy")
            row = dataset[0]
            first_len = len(row["image"].shape)
            second_len = len(row["text"].shape)
            self.assertEqual(first_len, 2, "use a sequence type if dim is  < 2")
            self.assertEqual(second_len, 2, "use a sequence type if dim is  < 2")

    def test_compatability_with_string_values(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            my_features = DEFAULT_FEATURES.copy()
            my_features["image_id"] = nlp.Value("string")
            writer = ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow"))
            for key, record in generate_examples(features=my_features, num_examples=1):
                example = my_features.encode_example(record)
                writer.write(example)
            num_examples, num_bytes = writer.finalize()
            dataset = nlp.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))
            self.assertTrue(isinstance(dataset[0]["image_id"], str), "image id must be of type string")

    def test_extension_indexing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            my_features = DEFAULT_FEATURES.copy()
            my_features["explicit_ext"] = Array2D((3, 3), dtype="float32")
            writer = ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow"))
            for key, record in generate_examples(features=my_features, num_examples=1):
                example = my_features.encode_example(record)
                writer.write(example)
            num_examples, num_bytes = writer.finalize()
            dataset = nlp.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))
            dataset.set_format("numpy")
            data = dataset[0]["explicit_ext"]
            self.assertIsInstance(data, np.ndarray, "indexed extension must return numpy.ndarray")


class SpeedBenchmarkTest(unittest.TestCase):
    def test_benchmark_speed(self):
        times = {}
        read_functions = (
            read_unformated,
            read_formatted_as_numpy,
            read_batch_unformated,
            read_batch_formatted_as_numpy,
            read_col_unformated,
            read_col_formatted_as_numpy,
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            feats = nlp.Features({"image": Array2D(SPEED_TEST_SHAPE, dtype="float32")})
            data = generate_examples(features=feats, num_examples=SPEED_TEST_N_EXAMPLES)
            write_func = write_array2d
            times[write_func.__name__] = write_func(feats, data, tmp_dir)
            for read_func in read_functions:
                times[read_func.__name__ + " after " + write_func.__name__] = read_func(feats, tmp_dir)

        with tempfile.TemporaryDirectory() as tmp_dir:
            feats = nlp.Features(
                {"image": nlp.Sequence(nlp.Sequence(nlp.Value("float32"), SPEED_TEST_SHAPE[1]), SPEED_TEST_SHAPE[0])}
            )
            data = generate_examples(features=feats, num_examples=SPEED_TEST_N_EXAMPLES)
            write_func = write_nested_sequence
            times[write_func.__name__] = write_func(feats, data, tmp_dir)
            for read_func in read_functions:
                times[read_func.__name__ + " after " + write_func.__name__] = read_func(feats, tmp_dir)

        with tempfile.TemporaryDirectory() as tmp_dir:
            feats = nlp.Features(
                {"image": nlp.Sequence(nlp.Value("float32"), SPEED_TEST_SHAPE[0] * SPEED_TEST_SHAPE[1])}
            )
            data = generate_examples(features=feats, num_examples=SPEED_TEST_N_EXAMPLES)
            write_func = write_flattened_sequence
            times[write_func.__name__] = write_func(feats, data, tmp_dir)
            for read_func in read_functions:
                times[read_func.__name__ + " after " + write_func.__name__] = read_func(feats, tmp_dir)

        benchmark_df = pd.DataFrame.from_dict(times, orient="index", columns=["time"]).sort_index()
        warn("Speed benchmark:\n" + str(benchmark_df))
        self.assertGreater(
            times["write_nested_sequence"], times["write_array2d"] * 10
        )  # At leasr 10 times faster (it is supposed to be ~25 times faster)
        self.assertGreater(
            times["read_batch_formatted_as_numpy after write_nested_sequence"],
            times["read_batch_formatted_as_numpy after write_array2d"],
        )  # At least faster (it is supposed to be ~2 times faster)
        self.assertGreater(
            times["read_batch_unformated after write_nested_sequence"],
            times["read_batch_formatted_as_numpy after write_array2d"] * 5,
        )  # At least 5 times faster (it is supposed to be ~10 times faster)


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
        return nlp.Features(
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
            dataset = nlp.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))
            self._check_getitem_output_type(dataset, shape_1, shape_2, my_examples[0][1]["matrix"])

    def test_write_batch(self, array_feature, shape_1, shape_2):

        with tempfile.TemporaryDirectory() as tmp_dir:

            my_features = self.get_features(array_feature, shape_1, shape_2)
            writer = ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow"))

            dict_examples = self.get_dict_examples(shape_1, shape_2)
            dict_examples = my_features.encode_batch(dict_examples)
            writer.write_batch(dict_examples)
            num_examples, num_bytes = writer.finalize()
            dataset = nlp.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))
            self._check_getitem_output_type(dataset, shape_1, shape_2, dict_examples["matrix"][0])

    def test_from_dict(self, array_feature, shape_1, shape_2):
        dict_examples = self.get_dict_examples(shape_1, shape_2)
        dataset = nlp.Dataset.from_dict(dict_examples, features=self.get_features(array_feature, shape_1, shape_2))
        self._check_getitem_output_type(dataset, shape_1, shape_2, dict_examples["matrix"][0])


if __name__ == "__main__":  # useful to run the profiler
    SpeedBenchmarkTest().test_benchmark_speed()
