from dataclasses import asdict
from unittest import TestCase
from unittest.mock import patch

import numpy as np
import pandas as pd
import pyarrow as pa
import pytest

from datasets import DatasetInfo
from datasets.arrow_dataset import Dataset
from datasets.features import (
    ClassLabel,
    Features,
    Sequence,
    Value,
    _arrow_to_datasets_dtype,
    _cast_to_python_objects,
    cast_to_python_objects,
    string_to_arrow,
)

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

    def test_string_to_arrow_bijection_for_primitive_types(self):
        supported_pyarrow_datatypes = [
            pa.timestamp("s"),
            pa.timestamp("ns", tz="America/New_York"),
            pa.string(),
            pa.int32(),
            pa.float64(),
        ]
        for dt in supported_pyarrow_datatypes:
            self.assertEqual(dt, string_to_arrow(_arrow_to_datasets_dtype(dt)))

        unsupported_pyarrow_datatypes = [pa.list_(pa.float64())]
        for dt in unsupported_pyarrow_datatypes:
            with self.assertRaises(ValueError):
                string_to_arrow(_arrow_to_datasets_dtype(dt))

        supported_datasets_dtypes = ["timestamp[ns]", "timestamp[ns, tz=+07:30]", "int32", "float64"]
        for sdt in supported_datasets_dtypes:
            self.assertEqual(sdt, _arrow_to_datasets_dtype(string_to_arrow(sdt)))

        unsupported_datasets_dtypes = ["timestamp[blob]", "timestamp[[ns]]", "timestamp[ns, tz=[ns]]", "int"]
        for sdt in unsupported_datasets_dtypes:
            with self.assertRaises(ValueError):
                string_to_arrow(sdt)

    def test_feature_named_type(self):
        """reference: issue #1110"""
        features = Features({"_type": Value("string")})
        ds_info = DatasetInfo(features=features)
        reloaded_features = Features.from_dict(asdict(ds_info)["features"])
        assert features == reloaded_features


def test_classlabel_init(tmp_path_factory):
    names = ["negative", "positive"]
    names_file = str(tmp_path_factory.mktemp("features") / "labels.txt")
    with open(names_file, "w", encoding="utf-8") as f:
        f.write("\n".join(names))
    classlabel = ClassLabel(names=names)
    assert classlabel.names == names and classlabel.num_classes == len(names)
    classlabel = ClassLabel(names_file=names_file)
    assert classlabel.names == names and classlabel.num_classes == len(names)
    classlabel = ClassLabel(num_classes=len(names), names=names)
    assert classlabel.names == names and classlabel.num_classes == len(names)
    classlabel = ClassLabel(num_classes=len(names))
    assert classlabel.names == [str(i) for i in range(len(names))] and classlabel.num_classes == len(names)
    with pytest.raises(ValueError):
        classlabel = ClassLabel(num_classes=len(names) + 1, names=names)
    with pytest.raises(ValueError):
        classlabel = ClassLabel(names=names, names_file=names_file)
    with pytest.raises(ValueError):
        classlabel = ClassLabel()


def test_classlabel_str2int():
    names = ["negative", "positive"]
    classlabel = ClassLabel(names=names)
    for label in names:
        assert classlabel.str2int(label) == names.index(label)
    with pytest.raises(KeyError):
        classlabel.str2int("__bad_label_name__")


def test_classlabel_int2str():
    names = ["negative", "positive"]
    classlabel = ClassLabel(names=names)
    for i in range(len(names)):
        assert classlabel.int2str(i) == names[i]
    with pytest.raises(ValueError):
        classlabel.int2str(len(names))


class CastToPythonObjectsTest(TestCase):
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
            "col_1": [{"vec": torch.tensor(np.arange(1, 4)), "txt": "foo"}] * 3,
            "col_2": torch.tensor(np.arange(1, 7).reshape(3, 2)),
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
