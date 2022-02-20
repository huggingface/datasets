from dataclasses import asdict
from unittest import TestCase
from unittest.mock import patch

import numpy as np
import pandas as pd
import pyarrow as pa
import pytest

from datasets.arrow_dataset import Dataset
from datasets.features import (
    ClassLabel,
    Features,
    Sequence,
    Value,
    _arrow_to_datasets_dtype,
    _cast_to_python_objects,
    cast_to_python_objects,
    encode_nested_example,
    generate_from_dict,
    string_to_arrow,
)
from datasets.info import DatasetInfo

from ..utils import require_jax, require_tf, require_torch


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
            pa.time32("s"),
            pa.time64("us"),
            pa.timestamp("s"),
            pa.timestamp("ns", tz="America/New_York"),
            pa.date32(),
            pa.date64(),
            pa.duration("s"),
            pa.decimal128(10, 2),
            pa.decimal256(40, -3),
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

        supported_datasets_dtypes = [
            "time32[s]",
            "timestamp[ns]",
            "timestamp[ns, tz=+07:30]",
            "duration[us]",
            "decimal128(30, -4)",
            "int32",
            "float64",
        ]
        for sdt in supported_datasets_dtypes:
            self.assertEqual(sdt, _arrow_to_datasets_dtype(string_to_arrow(sdt)))

        unsupported_datasets_dtypes = [
            "time32[ns]",
            "timestamp[blob]",
            "timestamp[[ns]]",
            "timestamp[ns, tz=[ns]]",
            "duration[[us]]",
            "decimal20(30, -4)",
            "int",
        ]
        for sdt in unsupported_datasets_dtypes:
            with self.assertRaises(ValueError):
                string_to_arrow(sdt)

    def test_feature_named_type(self):
        """reference: issue #1110"""
        features = Features({"_type": Value("string")})
        ds_info = DatasetInfo(features=features)
        reloaded_features = Features.from_dict(asdict(ds_info)["features"])
        assert features == reloaded_features

    def test_reorder_fields_as(self):
        features = Features(
            {
                "id": Value("string"),
                "document": {
                    "title": Value("string"),
                    "url": Value("string"),
                    "html": Value("string"),
                    "tokens": Sequence({"token": Value("string"), "is_html": Value("bool")}),
                },
                "question": {
                    "text": Value("string"),
                    "tokens": Sequence(Value("string")),
                },
                "annotations": Sequence(
                    {
                        "id": Value("string"),
                        "long_answer": {
                            "start_token": Value("int64"),
                            "end_token": Value("int64"),
                            "start_byte": Value("int64"),
                            "end_byte": Value("int64"),
                        },
                        "short_answers": Sequence(
                            {
                                "start_token": Value("int64"),
                                "end_token": Value("int64"),
                                "start_byte": Value("int64"),
                                "end_byte": Value("int64"),
                                "text": Value("string"),
                            }
                        ),
                        "yes_no_answer": ClassLabel(names=["NO", "YES"]),
                    }
                ),
            }
        )

        other = Features(  # same but with [] instead of sequences, and with a shuffled fields order
            {
                "id": Value("string"),
                "document": {
                    "tokens": Sequence({"token": Value("string"), "is_html": Value("bool")}),
                    "title": Value("string"),
                    "url": Value("string"),
                    "html": Value("string"),
                },
                "question": {
                    "text": Value("string"),
                    "tokens": [Value("string")],
                },
                "annotations": {
                    "yes_no_answer": [ClassLabel(names=["NO", "YES"])],
                    "id": [Value("string")],
                    "long_answer": [
                        {
                            "end_byte": Value("int64"),
                            "start_token": Value("int64"),
                            "end_token": Value("int64"),
                            "start_byte": Value("int64"),
                        }
                    ],
                    "short_answers": [
                        Sequence(
                            {
                                "text": Value("string"),
                                "start_token": Value("int64"),
                                "end_token": Value("int64"),
                                "start_byte": Value("int64"),
                                "end_byte": Value("int64"),
                            }
                        )
                    ],
                },
            }
        )

        expected = Features(
            {
                "id": Value("string"),
                "document": {
                    "tokens": Sequence({"token": Value("string"), "is_html": Value("bool")}),
                    "title": Value("string"),
                    "url": Value("string"),
                    "html": Value("string"),
                },
                "question": {
                    "text": Value("string"),
                    "tokens": Sequence(Value("string")),
                },
                "annotations": Sequence(
                    {
                        "yes_no_answer": ClassLabel(names=["NO", "YES"]),
                        "id": Value("string"),
                        "long_answer": {
                            "end_byte": Value("int64"),
                            "start_token": Value("int64"),
                            "end_token": Value("int64"),
                            "start_byte": Value("int64"),
                        },
                        "short_answers": Sequence(
                            {
                                "text": Value("string"),
                                "start_token": Value("int64"),
                                "end_token": Value("int64"),
                                "start_byte": Value("int64"),
                                "end_byte": Value("int64"),
                            }
                        ),
                    }
                ),
            }
        )

        reordered_features = features.reorder_fields_as(other)
        self.assertDictEqual(reordered_features, expected)
        self.assertEqual(reordered_features.type, other.type)
        self.assertEqual(reordered_features.type, expected.type)
        self.assertNotEqual(reordered_features.type, features.type)

    def test_flatten(self):
        features = Features({"foo": {"bar1": Value("int32"), "bar2": {"foobar": Value("string")}}})
        _features = features.copy()
        flattened_features = features.flatten()
        assert flattened_features == {"foo.bar1": Value("int32"), "foo.bar2.foobar": Value("string")}
        assert features == _features, "calling flatten shouldn't alter the current features"


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
    with pytest.raises(ValueError):
        classlabel.str2int(1)


def test_classlabel_int2str():
    names = ["negative", "positive"]
    classlabel = ClassLabel(names=names)
    for i in range(len(names)):
        assert classlabel.int2str(i) == names[i]
    with pytest.raises(ValueError):
        classlabel.int2str(len(names))


@pytest.mark.parametrize("class_label_arg", ["names", "names_file"])
def test_class_label_to_and_from_dict(class_label_arg, tmp_path_factory):
    names = ["negative", "positive"]
    names_file = str(tmp_path_factory.mktemp("features") / "labels.txt")
    with open(names_file, "w", encoding="utf-8") as f:
        f.write("\n".join(names))
    if class_label_arg == "names":
        class_label = ClassLabel(names=names)
    elif class_label_arg == "names_file":
        class_label = ClassLabel(names_file=names_file)
    generated_class_label = generate_from_dict(asdict(class_label))
    assert generated_class_label == class_label


def test_encode_nested_example_sequence_with_none():
    schema = Sequence(Value("int32"))
    obj = None
    result = encode_nested_example(schema, obj)
    assert result is None


def test_encode_batch_with_example_with_empty_first_elem():
    features = Features(
        {
            "x": Sequence(Sequence(ClassLabel(names=["a", "b"]))),
        }
    )
    encoded_batch = features.encode_batch(
        {
            "x": [
                [["a"], ["b"]],
                [[], ["b"]],
            ]
        }
    )
    assert encoded_batch == {"x": [[[0], [1]], [[], [1]]]}


def iternumpy(key1, value1, value2):
    if value1.dtype != value2.dtype:  # check only for dtype
        raise AssertionError(
            f"dtype of '{key1}' key for casted object: {value1.dtype} and expected object: {value2.dtype} not matching"
        )


def dict_diff(d1: dict, d2: dict):  # check if 2 dictionaries are equal

    np.testing.assert_equal(d1, d2)  # sanity check if dict values are equal or not

    for (k1, v1), (k2, v2) in zip(d1.items(), d2.items()):  # check if their values have same dtype or not
        if isinstance(v1, dict):  # nested dictionary case
            dict_diff(v1, v2)
        elif isinstance(v1, np.ndarray):  # checks if dtype and value of np.ndarray is equal
            iternumpy(k1, v1, v2)
        elif isinstance(v1, list):
            for (element1, element2) in zip(v1, v2):  # iterates over all elements of list
                if isinstance(element1, dict):
                    dict_diff(element1, element2)
                elif isinstance(element1, np.ndarray):
                    iternumpy(k1, element1, element2)


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

    def test_cast_to_python_or_numpy(self):
        obj = {"col_1": [{"vec": np.arange(1, 4), "txt": "foo"}] * 3, "col_2": np.arange(1, 7).reshape(3, 2)}
        expected_obj = {
            "col_1": [{"vec": np.array([1, 2, 3]), "txt": "foo"}] * 3,
            "col_2": np.array([[1, 2], [3, 4], [5, 6]]),
        }
        casted_obj = cast_to_python_objects(obj)
        dict_diff(casted_obj, expected_obj)

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
        expected_obj = {
            "col_1": [{"vec": np.array([1, 2, 3]), "txt": "foo"}] * 3,
            "col_2": np.array([[1, 2], [3, 4], [5, 6]]),
        }
        casted_obj = cast_to_python_objects(obj)
        dict_diff(casted_obj, expected_obj)

    @require_tf
    def test_cast_to_python_objects_tf(self):
        import tensorflow as tf

        obj = {
            "col_1": [{"vec": tf.constant(np.arange(1, 4)), "txt": "foo"}] * 3,
            "col_2": tf.constant(np.arange(1, 7).reshape(3, 2)),
        }
        expected_obj = {
            "col_1": [{"vec": np.array([1, 2, 3]), "txt": "foo"}] * 3,
            "col_2": np.array([[1, 2], [3, 4], [5, 6]]),
        }
        casted_obj = cast_to_python_objects(obj)
        dict_diff(casted_obj, expected_obj)

    @require_jax
    def test_cast_to_python_objects_jax(self):
        import jax.numpy as jnp

        obj = {
            "col_1": [{"vec": jnp.array(np.arange(1, 4)), "txt": "foo"}] * 3,
            "col_2": jnp.array(np.arange(1, 7).reshape(3, 2)),
        }
        assert obj["col_2"].dtype == jnp.int32
        expected_obj = {
            "col_1": [{"vec": np.array([1, 2, 3], dtype=np.int32), "txt": "foo"}] * 3,
            "col_2": np.array([[1, 2], [3, 4], [5, 6]], dtype=np.int32),
        }
        casted_obj = cast_to_python_objects(obj)
        dict_diff(casted_obj, expected_obj)

    @patch("datasets.features.features._cast_to_python_objects", side_effect=_cast_to_python_objects)
    def test_dont_iterate_over_each_element_in_a_list(self, mocked_cast):
        obj = {"col_1": [[1, 2], [3, 4], [5, 6]]}
        cast_to_python_objects(obj)
        self.assertEqual(mocked_cast.call_count, 4)  # 4 = depth of obj
