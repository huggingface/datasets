import os
import tempfile
import timeit
import unittest
from random import randint

import numpy as np

import nlp
import nlp.features as features
from nlp.arrow_writer import ArrowWriter


SHAPE_TEST_1 = (30, 487)
SHAPE_TEST_2 = (36, 1024)
SPEED_SHAPE_TEST = (100, 100)

DEFAULT_FEATURES = {
    "text": features.Array2D(dtype="float32"),
    "image": features.Array2D(dtype="float32"),
}


def log_duration(func):
    def wrapper(*arg, **kw):
        starttime = timeit.default_timer()
        r_vals = func(*arg, **kw)
        delta = timeit.default_timer() - starttime
        print(f"{func.__name__} took {delta} seconds to run")
        return r_vals

    return wrapper


def generate_examples(schema: dict, num_examples=10000, switch=False, fixed_extension_dim=True, speed_test=False):
    dummy_data = []
    for i in range(num_examples):
        example = {}
        extension_shape_bool = False
        for k, v in schema.items():
            if isinstance(v, features.Array2D):
                if speed_test:
                    shape = SPEED_SHAPE_TEST
                elif extension_shape_bool or (not extension_shape_bool and not switch):
                    shape = SHAPE_TEST_2
                    extension_shape_bool = False
                else:
                    shape = SHAPE_TEST_1
                    extension_shape_bool = True
                if fixed_extension_dim or speed_test:
                    data = np.random.rand(*shape).astype(v.inner_type)
                else:
                    data = []
                    for i in range(shape[0]):
                        data.append(np.random.rand(randint(1, shape[1])).astype(v.inner_type))
                    data = np.vstack(data)
            elif isinstance(v, nlp.Value):
                data = "".join([str(randint(0, i)) for i in range(randint(0, 9))])
            elif isinstance(v, nlp.Sequence) and str(v).count("Sequence") > 1:
                shape = SPEED_SHAPE_TEST
                data = np.random.rand(*shape).astype("float32").tolist()
            elif isinstance(v, nlp.Sequence):
                shape = SPEED_SHAPE_TEST
                data = np.random.rand(*(shape[0] ** 2,)).astype("float32").tolist()
            example[k] = data
            dummy_data.append((i, example))

    return dummy_data


@log_duration
def test_array2d_write_speed(feats, dummy_data, tmp_dir):
    my_features = nlp.Features(feats)
    writer = ArrowWriter(data_type=my_features.type, path=os.path.join(tmp_dir, "beta.arrow"))
    for key, record in dummy_data:
        example = my_features.encode_example(record)
        writer.write(example)
    num_examples, num_bytes = writer.finalize()


@log_duration
def test_nested_sequence(feats, dummy_data, tmp_dir):
    my_features = nlp.Features(feats)
    writer = ArrowWriter(data_type=my_features.type, path=os.path.join(tmp_dir, "beta.arrow"))
    for key, record in dummy_data:
        example = my_features.encode_example(record)
        writer.write(example)
    num_examples, num_bytes = writer.finalize()


@log_duration
def test_flattened_sequence(feats, dummy_data, tmp_dir):
    my_features = nlp.Features(feats)
    writer = ArrowWriter(data_type=my_features.type, path=os.path.join(tmp_dir, "beta.arrow"))
    for key, record in dummy_data:
        example = my_features.encode_example(record)
        writer.write(example)
    num_examples, num_bytes = writer.finalize()


class Array2DGeneralTests(unittest.TestCase):
    def test_array2d_nonspecific_shape(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            my_features = nlp.Features(DEFAULT_FEATURES)
            writer = ArrowWriter(data_type=my_features.type, path=os.path.join(tmp_dir, "beta.arrow"))
            for key, record in generate_examples(schema=DEFAULT_FEATURES, num_examples=1, switch=True):
                example = my_features.encode_example(record)
                writer.write(example)
            num_examples, num_bytes = writer.finalize()
            dataset = nlp.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))
            row = dataset[0]
            first_shape = row["image"].shape
            second_shape = row["text"].shape
            self.assertTrue(
                first_shape is not None and second_shape is not None, "need atleast 2 different shapes, only found 1"
            )
            self.assertTrue(len(first_shape) == len(second_shape), "both shapes are supposed to be equal length")
            self.assertNotEqual(first_shape, second_shape, "shapes must not be the same")

    def test_multiple_extensions_same_row(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            my_features = nlp.Features(DEFAULT_FEATURES)
            writer = ArrowWriter(data_type=my_features.type, path=os.path.join(tmp_dir, "beta.arrow"))
            for key, record in generate_examples(schema=DEFAULT_FEATURES, num_examples=1, fixed_extension_dim=True):
                example = my_features.encode_example(record)
                writer.write(example)
            num_examples, num_bytes = writer.finalize()
            dataset = nlp.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))
            row = dataset[0]
            first_len = len(row["image"].shape)
            second_len = len(row["text"].shape)
            self.assertNotEqual(first_len == 1, "use a sequence type if dim is  < 2")
            self.assertNotEqual(second_len == 1, "use a sequence type if dim is  < 2")

    # save this test for later if we ever want to have a non-fixed last dimension
    # def test_varying_last_dim(self):
    #     with tempfile.TemporaryDirectory() as tmp_dir:
    #         my_features = nlp.Features(DEFAULT_FEATURES)
    #         writer = ArrowWriter(data_type=my_features.type, path=os.path.join(tmp_dir, "beta.arrow"))
    #         for key, record in generate_examples(schema=DEFAULT_FEATURES, num_examples=1, fixed_extension_dim=False):
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
            DEFAULT_FEATURES["image_id"] = nlp.Value("string")
            my_features = nlp.Features(DEFAULT_FEATURES)
            writer = ArrowWriter(data_type=my_features.type, path=os.path.join(tmp_dir, "beta.arrow"))
            for key, record in generate_examples(schema=DEFAULT_FEATURES, num_examples=1):
                example = my_features.encode_example(record)
                writer.write(example)
            num_examples, num_bytes = writer.finalize()
            dataset = nlp.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))
            self.assertTrue(isinstance(dataset[0]["image_id"], str), "image id must be of type string")

    def test_extension_indexing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            DEFAULT_FEATURES["explicit_ext"] = features.Array2D(dtype="float32")
            my_features = nlp.Features(DEFAULT_FEATURES)
            writer = ArrowWriter(data_type=my_features.type, path=os.path.join(tmp_dir, "beta.arrow"))
            for key, record in generate_examples(schema=DEFAULT_FEATURES, num_examples=1):
                example = my_features.encode_example(record)
                writer.write(example)
            num_examples, num_bytes = writer.finalize()
            dataset = nlp.Dataset.from_file(os.path.join(tmp_dir, "beta.arrow"))
            try:
                data = dataset[0]["explicit_ext"]
            except Exception:
                self.assertTrue(1 == 2, "was unable to index the extension array")
            self.assertTrue(isinstance(data, np.ndarray), "idexed extenion must return numpy.ndarray")


if __name__ == "__main__":

    # formal unit tests
    unittest.main()

    # informal speed testing for multidim array
    ARRAY = False
    N_SEQ = False
    F_SEQ = False

    with tempfile.TemporaryDirectory() as tmp_dir:

        if ARRAY:
            feats = {"image": features.Array2D(dtype="float32")}
            data = generate_examples(schema=feats, speed_test=True)
            test_array2d_write_speed(feats, data, tmp_dir)

        if N_SEQ:
            feats = {"image": nlp.Sequence(nlp.Sequence(nlp.Value("float32")))}
            data = generate_examples(schema=feats, speed_test=True)
            test_nested_sequence(feats, data, tmp_dir)

        if F_SEQ:
            feats = {"image": nlp.Sequence(nlp.Value("float32"))}
            data = generate_examples(schema=feats, speed_test=True)
            test_flattened_sequence(feats, data, tmp_dir)
