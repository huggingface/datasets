import os
import tempfile
import timeit
import unittest
from warnings import warn

import numpy as np
import pandas as pd

import nlp
import nlp.features as features
from nlp.arrow_writer import ArrowWriter


SHAPE_TEST_1 = (30, 487)
SHAPE_TEST_2 = (36, 1024)
SPEED_SHAPE_TEST = (100, 100)

DEFAULT_FEATURES = nlp.Features(
    {"text": features.Array2D(dtype="float32"), "image": features.Array2D(dtype="float32")}
)


def get_duration(func):
    def wrapper(*args, **kwargs):
        starttime = timeit.default_timer()
        _ = func(*args, **kwargs)
        delta = timeit.default_timer() - starttime
        return delta

    wrapper.__name__ = func.__name__

    return wrapper


def generate_examples(
    schema: dict, num_examples=100, columns_have_different_shapes=False, speed_test=False, ragged_array=False
):
    dummy_data = []
    shapes = [SPEED_SHAPE_TEST] if speed_test else [SHAPE_TEST_1, SHAPE_TEST_2]
    for i in range(num_examples):
        example = {}
        for col_id, (k, v) in enumerate(schema.items()):
            shape_index = col_id % len(shapes) if columns_have_different_shapes else 0  # alternate
            if isinstance(v, features.Array2D):
                shape = shapes[shape_index]
                if not ragged_array:  # matrix
                    data = np.random.rand(*shape).astype(v.dtype)
                else:  # ragged
                    data = []
                    for i in range(shape[0]):
                        data.append(np.arange(max(shape[1], i + 1)).astype(v.dtype))
                    data = np.array(data)
            elif isinstance(v, nlp.Value):
                data = "foo"
            elif isinstance(v, nlp.Sequence) and str(v).count("Sequence") > 1:  # nested sequence
                shape = SPEED_SHAPE_TEST
                data = np.random.rand(*shape).astype("float32")
            elif isinstance(v, nlp.Sequence):  # one sequence
                shape = SPEED_SHAPE_TEST
                data = np.random.rand(*shape).astype("float32").flatten()
            example[k] = data
            dummy_data.append((i, example))

    return dummy_data


@get_duration
def write_array2d(feats, dummy_data, tmp_dir):
    my_features = nlp.Features(feats)
    writer = ArrowWriter(data_type=my_features.type, path=os.path.join(tmp_dir, "beta.arrow"))
    for key, record in dummy_data:
        example = my_features.encode_example(record)
        writer.write(example)
    num_examples, num_bytes = writer.finalize()


@get_duration
def write_nested_sequence(feats, dummy_data, tmp_dir):
    my_features = nlp.Features(feats)
    writer = ArrowWriter(data_type=my_features.type, path=os.path.join(tmp_dir, "beta.arrow"))
    for key, record in dummy_data:
        example = my_features.encode_example(record)
        writer.write(example)
    num_examples, num_bytes = writer.finalize()


@get_duration
def write_flattened_sequence(feats, dummy_data, tmp_dir):
    my_features = nlp.Features(feats)
    writer = ArrowWriter(data_type=my_features.type, path=os.path.join(tmp_dir, "beta.arrow"))
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
def read_formated_as_numpy(feats, tmp_dir):
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
def read_batch_formated_as_numpy(feats, tmp_dir):
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
def read_col_formated_as_numpy(feats, tmp_dir):
    dataset = nlp.Dataset.from_file(filename=os.path.join(tmp_dir, "beta.arrow"), info=nlp.DatasetInfo(features=feats))
    dataset.set_format("numpy")
    for col in feats:
        _ = dataset[col]


class ExtensionTypeCompatibilityTest(unittest.TestCase):
    def test_array2d_nonspecific_shape(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            my_features = DEFAULT_FEATURES.copy()
            writer = ArrowWriter(data_type=my_features.type, path=os.path.join(tmp_dir, "beta.arrow"))
            for key, record in generate_examples(
                schema=DEFAULT_FEATURES, num_examples=1, columns_have_different_shapes=True
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
            writer = ArrowWriter(data_type=my_features.type, path=os.path.join(tmp_dir, "beta.arrow"))
            for key, record in generate_examples(schema=my_features, num_examples=1):
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

    # save this test for later if we ever want to have a non-fixed last dimension
    # def test_varying_last_dim(self):
    #     with tempfile.TemporaryDirectory() as tmp_dir:
    #         my_features = DEFAULT_FEATURES
    #         writer = ArrowWriter(data_type=my_features.type, path=os.path.join(tmp_dir, "beta.arrow"))
    #         for key, record in generate_examples(schema=my_features, num_examples=1, ragged_array=True):
    #             example = my_features.encode_example(record)
    #             writer.write(example)
    #         num_examples, num_bytes = writer.finalize()
    #         dataset = nlp.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))
    #         row = dataset[0]
    #         inspect = None
    #         for col in row:
    #             if hasattr(col, "shape"):
    #                 self.assertNotEqual(len(col.shape) == 1, "use a sequence type if dim is  < 2")
    #                 inspect = col.tolist()
    #                 break
    #         self.assertTrue(inspect is not None, "could not find extension")
    #         match_this_dim = len(inspect[0])
    #         self.assertTrue(not all([len(i) == match_this_dim for i in inspect]), "dim -1 must not all be the same")

    def test_compatability_with_string_values(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            my_features = DEFAULT_FEATURES.copy()
            my_features["image_id"] = nlp.Value("string")
            writer = ArrowWriter(data_type=my_features.type, path=os.path.join(tmp_dir, "beta.arrow"))
            for key, record in generate_examples(schema=my_features, num_examples=1):
                example = my_features.encode_example(record)
                writer.write(example)
            num_examples, num_bytes = writer.finalize()
            dataset = nlp.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))
            self.assertTrue(isinstance(dataset[0]["image_id"], str), "image id must be of type string")

    def test_extension_indexing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            my_features = DEFAULT_FEATURES.copy()
            my_features["explicit_ext"] = features.Array2D(dtype="float32")
            writer = ArrowWriter(data_type=my_features.type, path=os.path.join(tmp_dir, "beta.arrow"))
            for key, record in generate_examples(schema=my_features, num_examples=1):
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
            read_formated_as_numpy,
            read_batch_unformated,
            read_batch_formated_as_numpy,
            read_col_unformated,
            read_col_formated_as_numpy,
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            feats = nlp.Features({"image": features.Array2D(dtype="float32")})
            data = generate_examples(schema=feats, speed_test=True)
            write_func = write_array2d
            times[write_func.__name__] = write_func(feats, data, tmp_dir)
            for read_func in read_functions:
                times[read_func.__name__ + " after " + write_func.__name__] = read_func(feats, tmp_dir)

        with tempfile.TemporaryDirectory() as tmp_dir:
            feats = nlp.Features({"image": nlp.Sequence(nlp.Sequence(nlp.Value("float32")))})
            data = generate_examples(schema=feats, speed_test=True)
            write_func = write_nested_sequence
            times[write_func.__name__] = write_func(feats, data, tmp_dir)
            for read_func in read_functions:
                times[read_func.__name__ + " after " + write_func.__name__] = read_func(feats, tmp_dir)

        with tempfile.TemporaryDirectory() as tmp_dir:
            feats = nlp.Features({"image": nlp.Sequence(nlp.Value("float32"))})
            data = generate_examples(schema=feats, speed_test=True)
            write_func = write_flattened_sequence
            times[write_func.__name__] = write_func(feats, data, tmp_dir)
            for read_func in read_functions:
                times[read_func.__name__ + " after " + write_func.__name__] = read_func(feats, tmp_dir)

        benchmark_df = pd.DataFrame.from_dict(times, orient="index", columns=["time"]).sort_index()
        warn("Speed benchmark:\n" + str(benchmark_df))
        self.assertGreater(
            times["write_nested_sequence"], times["write_array2d"] * 25
        )  # At leasr 25 times faster (it is supposed to be ~50 times faster)
        self.assertGreater(
            times["read_batch_formated_as_numpy after write_nested_sequence"],
            times["read_batch_formated_as_numpy after write_array2d"],
        )  # At least faster (it is supposed to be ~2 times faster)
        self.assertGreater(
            times["read_batch_unformated after write_nested_sequence"],
            times["read_batch_formated_as_numpy after write_array2d"] * 5,
        )  # At least 5 times faster (it is supposed to be ~10 times faster)


class Array2dTest(unittest.TestCase):
    def test_write(self):

        my_features = {
            "matrix": features.Array2D(dtype="float32"),
            "image": features.Array2D(dtype="float32"),
            "source": features.Value("string"),
        }

        dict_example_0 = {
            "image": np.random.rand(5, 5).astype("float32"),
            "source": "foo",
            "matrix": np.random.rand(16, 256).astype("float32"),
        }

        dict_example_1 = {
            "image": np.random.rand(5, 5).astype("float32"),
            "matrix": np.random.rand(16, 256).astype("float32"),
            "source": "bar",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:

            my_features = nlp.Features(my_features)
            writer = ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow"))
            my_examples = [(0, dict_example_0), (1, dict_example_1)]
            for key, record in my_examples:
                example = my_features.encode_example(record)
                writer.write(example)
            num_examples, num_bytes = writer.finalize()
            dataset = nlp.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))

            matrix_column = dataset["matrix"]
            self.assertIsInstance(matrix_column, list)
            self.assertIsInstance(matrix_column[0], list)
            self.assertIsInstance(matrix_column[0][0], list)
            self.assertEqual(np.array(matrix_column).shape, (2, 16, 256))

            matrix_field_of_first_example = dataset[0]["matrix"]
            self.assertIsInstance(matrix_field_of_first_example, list)
            self.assertIsInstance(matrix_field_of_first_example, list)
            self.assertEqual(np.array(matrix_field_of_first_example).shape, (16, 256))

            matrix_field_of_first_two_examples = dataset[:2]["matrix"]
            self.assertIsInstance(matrix_field_of_first_two_examples, list)
            self.assertIsInstance(matrix_field_of_first_two_examples[0], list)
            self.assertIsInstance(matrix_field_of_first_two_examples[0][0], list)
            self.assertEqual(np.array(matrix_field_of_first_two_examples).shape, (2, 16, 256))
            with dataset.formated_as("numpy"):
                self.assertEqual(dataset["matrix"].shape, (2, 16, 256))
                self.assertEqual(dataset[0]["matrix"].shape, (16, 256))
                self.assertEqual(dataset[:2]["matrix"].shape, (2, 16, 256))

    def test_write_batch(self):

        my_features = {
            "matrix": features.Array2D(dtype="float32"),
            "image": features.Array2D(dtype="float32"),
            "source": features.Value("string"),
        }

        dict_examples = {
            "image": np.random.rand(2, 5, 5).astype("float32").tolist(),
            "source": ["foo", "bar"],
            "matrix": np.random.rand(2, 16, 256).astype("float32").tolist(),
        }

        with tempfile.TemporaryDirectory() as tmp_dir:

            my_features = nlp.Features(my_features)
            writer = ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow"))

            # dict_examples = my_features.encode_batch(dict_examples)
            writer.write_batch(dict_examples)
            num_examples, num_bytes = writer.finalize()
            dataset = nlp.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))

            matrix_column = dataset["matrix"]
            self.assertIsInstance(matrix_column, list)
            self.assertIsInstance(matrix_column[0], list)
            self.assertIsInstance(matrix_column[0][0], list)
            self.assertEqual(np.array(matrix_column).shape, (2, 16, 256))

            matrix_field_of_first_example = dataset[0]["matrix"]
            self.assertIsInstance(matrix_field_of_first_example, list)
            self.assertIsInstance(matrix_field_of_first_example, list)
            self.assertEqual(np.array(matrix_field_of_first_example).shape, (16, 256))

            matrix_field_of_first_two_examples = dataset[:2]["matrix"]
            self.assertIsInstance(matrix_field_of_first_two_examples, list)
            self.assertIsInstance(matrix_field_of_first_two_examples[0], list)
            self.assertIsInstance(matrix_field_of_first_two_examples[0][0], list)
            self.assertEqual(np.array(matrix_field_of_first_two_examples).shape, (2, 16, 256))
            with dataset.formated_as("numpy"):
                self.assertEqual(dataset["matrix"].shape, (2, 16, 256))
                self.assertEqual(dataset[0]["matrix"].shape, (16, 256))
                self.assertEqual(dataset[:2]["matrix"].shape, (2, 16, 256))
