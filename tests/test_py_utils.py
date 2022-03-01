from unittest import TestCase

import numpy as np
import pytest

from datasets.utils.py_utils import NestedDataStructure, map_nested, temp_seed, temporary_assignment, zip_dict

from .utils import require_tf, require_torch


def np_sum(x):  # picklable for multiprocessing
    return x.sum()


def add_one(i):  # picklable for multiprocessing
    return i + 1


class PyUtilsTest(TestCase):
    def test_map_nested(self):
        s1 = {}
        s2 = []
        s3 = 1
        s4 = [1, 2]
        s5 = {"a": 1, "b": 2}
        s6 = {"a": [1, 2], "b": [3, 4]}
        s7 = {"a": {"1": 1}, "b": 2}
        s8 = {"a": 1, "b": 2, "c": 3, "d": 4}
        expected_map_nested_s1 = {}
        expected_map_nested_s2 = []
        expected_map_nested_s3 = 2
        expected_map_nested_s4 = [2, 3]
        expected_map_nested_s5 = {"a": 2, "b": 3}
        expected_map_nested_s6 = {"a": [2, 3], "b": [4, 5]}
        expected_map_nested_s7 = {"a": {"1": 2}, "b": 3}
        expected_map_nested_s8 = {"a": 2, "b": 3, "c": 4, "d": 5}
        self.assertEqual(map_nested(add_one, s1), expected_map_nested_s1)
        self.assertEqual(map_nested(add_one, s2), expected_map_nested_s2)
        self.assertEqual(map_nested(add_one, s3), expected_map_nested_s3)
        self.assertEqual(map_nested(add_one, s4), expected_map_nested_s4)
        self.assertEqual(map_nested(add_one, s5), expected_map_nested_s5)
        self.assertEqual(map_nested(add_one, s6), expected_map_nested_s6)
        self.assertEqual(map_nested(add_one, s7), expected_map_nested_s7)
        self.assertEqual(map_nested(add_one, s8), expected_map_nested_s8)

        num_proc = 2
        self.assertEqual(map_nested(add_one, s1, num_proc=num_proc), expected_map_nested_s1)
        self.assertEqual(map_nested(add_one, s2, num_proc=num_proc), expected_map_nested_s2)
        self.assertEqual(map_nested(add_one, s3, num_proc=num_proc), expected_map_nested_s3)
        self.assertEqual(map_nested(add_one, s4, num_proc=num_proc), expected_map_nested_s4)
        self.assertEqual(map_nested(add_one, s5, num_proc=num_proc), expected_map_nested_s5)
        self.assertEqual(map_nested(add_one, s6, num_proc=num_proc), expected_map_nested_s6)
        self.assertEqual(map_nested(add_one, s7, num_proc=num_proc), expected_map_nested_s7)
        self.assertEqual(map_nested(add_one, s8, num_proc=num_proc), expected_map_nested_s8)

        sn1 = {"a": np.eye(2), "b": np.zeros(3), "c": np.ones(2)}
        expected_map_nested_sn1_sum = {"a": 2, "b": 0, "c": 2}
        expected_map_nested_sn1_int = {
            "a": np.eye(2).astype(int),
            "b": np.zeros(3).astype(int),
            "c": np.ones(2).astype(int),
        }
        self.assertEqual(map_nested(np_sum, sn1, map_numpy=False), expected_map_nested_sn1_sum)
        self.assertEqual(
            {k: v.tolist() for k, v in map_nested(int, sn1, map_numpy=True).items()},
            {k: v.tolist() for k, v in expected_map_nested_sn1_int.items()},
        )
        self.assertEqual(map_nested(np_sum, sn1, map_numpy=False, num_proc=num_proc), expected_map_nested_sn1_sum)
        self.assertEqual(
            {k: v.tolist() for k, v in map_nested(int, sn1, map_numpy=True, num_proc=num_proc).items()},
            {k: v.tolist() for k, v in expected_map_nested_sn1_int.items()},
        )
        with self.assertRaises(AttributeError):  # can't pickle a local lambda
            map_nested(lambda x: x + 1, sn1, num_proc=num_proc)

    def test_zip_dict(self):
        d1 = {"a": 1, "b": 2}
        d2 = {"a": 3, "b": 4}
        d3 = {"a": 5, "b": 6}
        expected_zip_dict_result = sorted([("a", (1, 3, 5)), ("b", (2, 4, 6))])
        self.assertEqual(sorted(list(zip_dict(d1, d2, d3))), expected_zip_dict_result)

    def test_temporary_assignment(self):
        class Foo:
            my_attr = "bar"

        foo = Foo()
        self.assertEqual(foo.my_attr, "bar")
        with temporary_assignment(foo, "my_attr", "BAR"):
            self.assertEqual(foo.my_attr, "BAR")
        self.assertEqual(foo.my_attr, "bar")


class TempSeedTest(TestCase):
    @require_tf
    def test_tensorflow(self):
        import tensorflow as tf
        from tensorflow.keras import layers

        def gen_random_output():
            model = layers.Dense(2)
            x = tf.random.uniform((1, 3))
            return model(x).numpy()

        with temp_seed(42, set_tensorflow=True):
            out1 = gen_random_output()
        with temp_seed(42, set_tensorflow=True):
            out2 = gen_random_output()
        out3 = gen_random_output()

        np.testing.assert_equal(out1, out2)
        self.assertGreater(np.abs(out1 - out3).sum(), 0)

    @require_torch
    def test_torch(self):
        import torch

        def gen_random_output():
            model = torch.nn.Linear(3, 2)
            x = torch.rand(1, 3)
            return model(x).detach().numpy()

        with temp_seed(42, set_pytorch=True):
            out1 = gen_random_output()
        with temp_seed(42, set_pytorch=True):
            out2 = gen_random_output()
        out3 = gen_random_output()

        np.testing.assert_equal(out1, out2)
        self.assertGreater(np.abs(out1 - out3).sum(), 0)

    def test_numpy(self):
        def gen_random_output():
            return np.random.rand(1, 3)

        with temp_seed(42):
            out1 = gen_random_output()
        with temp_seed(42):
            out2 = gen_random_output()
        out3 = gen_random_output()

        np.testing.assert_equal(out1, out2)
        self.assertGreater(np.abs(out1 - out3).sum(), 0)


@pytest.mark.parametrize("input_data", [{}])
def test_nested_data_structure_data(input_data):
    output_data = NestedDataStructure(input_data).data
    assert output_data == input_data


@pytest.mark.parametrize(
    "data, expected_output",
    [
        ({}, []),
        ([], []),
        ("foo", ["foo"]),
        (["foo", "bar"], ["foo", "bar"]),
        ([["foo", "bar"]], ["foo", "bar"]),
        ([[["foo"], ["bar"]]], ["foo", "bar"]),
        ([[["foo"], "bar"]], ["foo", "bar"]),
        ({"a": 1, "b": 2}, [1, 2]),
        ({"a": [1, 2], "b": [3, 4]}, [1, 2, 3, 4]),
        ({"a": [[1, 2]], "b": [[3, 4]]}, [1, 2, 3, 4]),
        ({"a": [[1, 2]], "b": [3, 4]}, [1, 2, 3, 4]),
        ({"a": [[[1], [2]]], "b": [[[3], [4]]]}, [1, 2, 3, 4]),
        ({"a": [[[1], [2]]], "b": [[3, 4]]}, [1, 2, 3, 4]),
        ({"a": [[[1], [2]]], "b": [3, 4]}, [1, 2, 3, 4]),
        ({"a": [[[1], [2]]], "b": [3, [4]]}, [1, 2, 3, 4]),
        ({"a": {"1": 1}, "b": 2}, [1, 2]),
        ({"a": {"1": [1]}, "b": 2}, [1, 2]),
        ({"a": {"1": [1]}, "b": [2]}, [1, 2]),
    ],
)
def test_flatten(data, expected_output):
    output = NestedDataStructure(data).flatten()
    assert output == expected_output
