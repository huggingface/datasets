from unittest import TestCase
from unittest.mock import patch

import numpy as np
import pandas as pd

from datasets.arrow_dataset import Dataset
from datasets.features import Features, Sequence, Value, _cast_to_python_objects, cast_to_python_objects

from .utils import require_tf, require_torch


class FeaturesTest(TestCase):
    def test_from_arrow_schema_simple(self):
        data = {"a": [{"b": {"c": "text"}}] * 10, "foo": [1] * 10}
        original_features = Features({"a": {"b": {"c": Value("string")}}, "foo": Value("int64")})
        dset = Dataset.from_dict(data, features=original_features)
        new_features = dset.features
        new_dset = Dataset.from_dict(data, features=new_features)
        self.assertEqual(original_features.type, new_features.type)
        self.assertDictEqual(dset[0], new_dset[0])
        self.assertDictEqual(dset[:], new_dset[:])

    def test_from_arrow_schema_with_sequence(self):
        data = {"a": [{"b": {"c": ["text"]}}] * 10, "foo": [1] * 10}
        original_features = Features({"a": {"b": Sequence({"c": Value("string")})}, "foo": Value("int64")})
        dset = Dataset.from_dict(data, features=original_features)
        new_features = dset.features
        new_dset = Dataset.from_dict(data, features=new_features)
        self.assertEqual(original_features.type, new_features.type)
        self.assertDictEqual(dset[0], new_dset[0])
        self.assertDictEqual(dset[:], new_dset[:])

    def test_cast_to_python_objects_list(self):
        obj = {"col_1": [{"vec": [1, 2, 3], "txt": "foo"}] * 3, "col_2": [[1, 2], [3, 4], [5, 6]]}
        expected_obj = {"col_1": [{"vec": [1, 2, 3], "txt": "foo"}] * 3, "col_2": [[1, 2], [3, 4], [5, 6]]}
        casted_obj = cast_to_python_objects(obj)
        self.assertDictEqual(casted_obj, expected_obj)

    def test_cast_to_python_objects_tuple(self):
        obj = {"col_1": [{"vec": (1, 2, 3), "txt": "foo"}] * 3, "col_2": [(1, 2), (3, 4), (5, 6)]}
        expected_obj = {"col_1": [{"vec": [1, 2, 3], "txt": "foo"}] * 3, "col_2": [[1, 2], [3, 4], [5, 6]]}
        casted_obj = cast_to_python_objects(obj)
        self.assertDictEqual(casted_obj, expected_obj)

    def test_cast_to_python_objects_numpy(self):
        obj = {"col_1": [{"vec": np.arange(1, 4), "txt": "foo"}] * 3, "col_2": np.arange(1, 7).reshape(3, 2)}
        expected_obj = {"col_1": [{"vec": [1, 2, 3], "txt": "foo"}] * 3, "col_2": [[1, 2], [3, 4], [5, 6]]}
        casted_obj = cast_to_python_objects(obj)
        self.assertDictEqual(casted_obj, expected_obj)

    def test_cast_to_python_objects_series(self):
        obj = {
            "col_1": pd.Series([{"vec": [1, 2, 3], "txt": "foo"}] * 3),
            "col_2": pd.Series([[1, 2], [3, 4], [5, 6]]),
        }
        expected_obj = {"col_1": [{"vec": [1, 2, 3], "txt": "foo"}] * 3, "col_2": [[1, 2], [3, 4], [5, 6]]}
        casted_obj = cast_to_python_objects(obj)
        self.assertDictEqual(casted_obj, expected_obj)

    def test_cast_to_python_objects_dataframe(self):
        obj = pd.DataFrame({"col_1": [{"vec": [1, 2, 3], "txt": "foo"}] * 3, "col_2": [[1, 2], [3, 4], [5, 6]]})
        expected_obj = {"col_1": [{"vec": [1, 2, 3], "txt": "foo"}] * 3, "col_2": [[1, 2], [3, 4], [5, 6]]}
        casted_obj = cast_to_python_objects(obj)
        self.assertDictEqual(casted_obj, expected_obj)

    @require_torch
    def test_cast_to_python_objects_torch(self):
        import torch

        obj = {
            "col_1": [{"vec": torch.Tensor(np.arange(1, 4)), "txt": "foo"}] * 3,
            "col_2": torch.Tensor(np.arange(1, 7).reshape(3, 2)),
        }
        expected_obj = {"col_1": [{"vec": [1, 2, 3], "txt": "foo"}] * 3, "col_2": [[1, 2], [3, 4], [5, 6]]}
        casted_obj = cast_to_python_objects(obj)
        self.assertDictEqual(casted_obj, expected_obj)

    @require_tf
    def test_cast_to_python_objects_tf(self):
        import tensorflow as tf

        obj = {
            "col_1": [{"vec": tf.constant(np.arange(1, 4)), "txt": "foo"}] * 3,
            "col_2": tf.constant(np.arange(1, 7).reshape(3, 2)),
        }
        expected_obj = {"col_1": [{"vec": [1, 2, 3], "txt": "foo"}] * 3, "col_2": [[1, 2], [3, 4], [5, 6]]}
        casted_obj = cast_to_python_objects(obj)
        self.assertDictEqual(casted_obj, expected_obj)

    @patch("datasets.features._cast_to_python_objects", side_effect=_cast_to_python_objects)
    def test_dont_iterate_over_each_element_in_a_list(self, mocked_cast):
        obj = {"col_1": [[1, 2], [3, 4], [5, 6]]}
        cast_to_python_objects(obj)
        self.assertEqual(mocked_cast.call_count, 4)  # 4 = depth of obj
