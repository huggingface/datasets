import datetime
from typing import List, Tuple
from unittest import TestCase
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pyarrow as pa
import pytest

from datasets import Array2D
from datasets.arrow_dataset import Dataset
from datasets.features import Audio, ClassLabel, Features, Image, LargeList, Sequence, Value
from datasets.features.features import (
    _align_features,
    _arrow_to_datasets_dtype,
    _cast_to_python_objects,
    _check_if_features_can_be_aligned,
    _check_non_null_non_empty_recursive,
    _visit,
    cast_to_python_objects,
    decode_nested_example,
    encode_nested_example,
    generate_from_arrow_type,
    generate_from_dict,
    get_nested_type,
    require_decoding,
    require_storage_cast,
    require_storage_embed,
    string_to_arrow,
)
from datasets.features.translation import Translation, TranslationVariableLanguages
from datasets.info import DatasetInfo
from datasets.utils.py_utils import asdict

from ..utils import require_jax, require_numpy1_on_windows, require_tf, require_torch


def list_with(item):
    return [item]


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
            pa.array([datetime.time(1, 1, 1)]).type,  # arrow type: DataType(time64[us])
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

    def test_categorical_one_way(self):
        # Categorical types (aka dictionary types) need special handling as there isn't a bijection
        categorical_type = pa.dictionary(pa.int32(), pa.string())

        self.assertEqual("string", _arrow_to_datasets_dtype(categorical_type))

    def test_feature_named_type(self):
        """reference: issue #1110"""
        features = Features({"_type": Value("string")})
        ds_info = DatasetInfo(features=features)
        reloaded_features = Features.from_dict(asdict(ds_info)["features"])
        assert features == reloaded_features

    def test_feature_named_self_as_kwarg(self):
        """reference: issue #5641"""
        features = Features(self=Value("string"))
        ds_info = DatasetInfo(features=features)
        reloaded_features = Features.from_dict(asdict(ds_info)["features"])
        assert features == reloaded_features

    def test_class_label_feature_with_no_labels(self):
        """reference: issue #4681"""
        features = Features({"label": ClassLabel(names=[])})
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

    def test_flatten_with_sequence(self):
        features = Features({"foo": Sequence({"bar": {"my_value": Value("int32")}})})
        _features = features.copy()
        flattened_features = features.flatten()
        assert flattened_features == {"foo.bar": [{"my_value": Value("int32")}]}
        assert features == _features, "calling flatten shouldn't alter the current features"

    def test_features_dicts_are_synced(self):
        def assert_features_dicts_are_synced(features: Features):
            assert (
                hasattr(features, "_column_requires_decoding")
                and features.keys() == features._column_requires_decoding.keys()
            )

        features = Features({"foo": Sequence({"bar": {"my_value": Value("int32")}})})
        assert_features_dicts_are_synced(features)
        features["barfoo"] = Image()
        assert_features_dicts_are_synced(features)
        del features["barfoo"]
        assert_features_dicts_are_synced(features)
        features.update({"foobar": Value("string")})
        assert_features_dicts_are_synced(features)
        features.pop("foobar")
        assert_features_dicts_are_synced(features)
        features.popitem()
        assert_features_dicts_are_synced(features)
        features.setdefault("xyz", Value("bool"))
        assert_features_dicts_are_synced(features)
        features.clear()
        assert_features_dicts_are_synced(features)


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
    with pytest.raises(TypeError):
        classlabel = ClassLabel(names=np.array(names))


def test_classlabel_str2int():
    names = ["negative", "positive"]
    classlabel = ClassLabel(names=names)
    for label in names:
        assert classlabel.str2int(label) == names.index(label)
    with pytest.raises(ValueError):
        classlabel.str2int("__bad_label_name__")
    with pytest.raises(ValueError):
        classlabel.str2int(1)
    with pytest.raises(ValueError):
        classlabel.str2int(None)


def test_classlabel_int2str():
    names = ["negative", "positive"]
    classlabel = ClassLabel(names=names)
    for i in range(len(names)):
        assert classlabel.int2str(i) == names[i]
    with pytest.raises(ValueError):
        classlabel.int2str(len(names))
    with pytest.raises(ValueError):
        classlabel.int2str(-1)
    with pytest.raises(ValueError):
        classlabel.int2str(None)


def test_classlabel_cast_storage():
    names = ["negative", "positive"]
    classlabel = ClassLabel(names=names)
    # from integers
    arr = pa.array([0, 1, -1, -100], type=pa.int64())
    result = classlabel.cast_storage(arr)
    assert result.type == pa.int64()
    assert result.to_pylist() == [0, 1, -1, -100]
    arr = pa.array([0, 1, -1, -100], type=pa.int32())
    result = classlabel.cast_storage(arr)
    assert result.type == pa.int64()
    assert result.to_pylist() == [0, 1, -1, -100]
    arr = pa.array([3])
    with pytest.raises(ValueError):
        classlabel.cast_storage(arr)
    # from strings
    arr = pa.array(["negative", "positive"])
    result = classlabel.cast_storage(arr)
    assert result.type == pa.int64()
    assert result.to_pylist() == [0, 1]
    arr = pa.array(["__label_that_doesnt_exist__"])
    with pytest.raises(ValueError):
        classlabel.cast_storage(arr)
    # from nulls
    arr = pa.array([None])
    result = classlabel.cast_storage(arr)
    assert result.type == pa.int64()
    assert result.to_pylist() == [None]
    # from empty
    arr = pa.array([], pa.int64())
    result = classlabel.cast_storage(arr)
    assert result.type == pa.int64()
    assert result.to_pylist() == []
    arr = pa.array([], pa.string())
    result = classlabel.cast_storage(arr)
    assert result.type == pa.int64()
    assert result.to_pylist() == []


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


@pytest.mark.parametrize(
    "schema",
    [[Audio()], LargeList(Audio()), Sequence(Audio())],
)
def test_decode_nested_example_with_list_types(schema, monkeypatch):
    mock_decode_example = MagicMock()
    monkeypatch.setattr(Audio, "decode_example", mock_decode_example)
    audio_example = {"path": "dummy_audio_path"}
    _ = decode_nested_example(schema, [audio_example])
    assert mock_decode_example.called
    assert mock_decode_example.call_args.args[0] == audio_example


@pytest.mark.parametrize(
    "schema",
    [[ClassLabel(names=["a", "b"])], LargeList(ClassLabel(names=["a", "b"])), Sequence(ClassLabel(names=["a", "b"]))],
)
def test_encode_nested_example_with_list_types(schema):
    result = encode_nested_example(schema, ["b"])
    assert result == [1]


@pytest.mark.parametrize("inner_type", [Value("int32"), {"subcolumn": Value("int32")}])
def test_encode_nested_example_sequence_with_none(inner_type):
    schema = Sequence(inner_type)
    obj = None
    result = encode_nested_example(schema, obj)
    assert result is None


@pytest.mark.parametrize(
    "features_dict, example, expected_encoded_example",
    [
        ({"col_1": ClassLabel(names=["a", "b"])}, {"col_1": "b"}, {"col_1": 1}),
        ({"col_1": [ClassLabel(names=["a", "b"])]}, {"col_1": ["b"]}, {"col_1": [1]}),
        ({"col_1": LargeList(ClassLabel(names=["a", "b"]))}, {"col_1": ["b"]}, {"col_1": [1]}),
        ({"col_1": Sequence(ClassLabel(names=["a", "b"]))}, {"col_1": ["b"]}, {"col_1": [1]}),
    ],
)
def test_encode_example(features_dict, example, expected_encoded_example):
    features = Features(features_dict)
    encoded_example = features.encode_example(example)
    assert encoded_example == expected_encoded_example


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


def test_encode_column_dict_with_none():
    features = Features(
        {
            "x": {"a": ClassLabel(names=["a", "b"]), "b": Value("int32")},
        }
    )
    encoded_column = features.encode_column([{"a": "a", "b": 1}, None], "x")
    assert encoded_column == [{"a": 0, "b": 1}, None]


@pytest.mark.parametrize(
    "feature",
    [
        Value("int32"),
        ClassLabel(num_classes=2),
        Translation(languages=["en", "fr"]),
        TranslationVariableLanguages(languages=["en", "fr"]),
    ],
)
def test_dataset_feature_with_none(feature):
    data = {"col": [None]}
    features = Features({"col": feature})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"col"}
    assert item["col"] is None
    batch = dset[:1]
    assert len(batch) == 1
    assert batch.keys() == {"col"}
    assert isinstance(batch["col"], list) and all(item is None for item in batch["col"])
    column = dset["col"]
    assert len(column) == 1
    assert isinstance(column, list) and all(item is None for item in column)

    # nested tests

    data = {"col": [[None]]}
    features = Features({"col": Sequence(feature)})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"col"}
    assert all(i is None for i in item["col"])

    data = {"nested": [{"col": None}]}
    features = Features({"nested": {"col": feature}})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"nested"}
    assert item["nested"].keys() == {"col"}
    assert item["nested"]["col"] is None


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
            for element1, element2 in zip(v1, v2):  # iterates over all elements of list
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
        expected_obj = {"col_1": [{"vec": (1, 2, 3), "txt": "foo"}] * 3, "col_2": [(1, 2), (3, 4), (5, 6)]}
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

    def test_cast_to_python_objects_pandas_timestamp(self):
        obj = pd.Timestamp(2020, 1, 1)
        expected_obj = obj.to_pydatetime()
        casted_obj = cast_to_python_objects(obj)
        self.assertEqual(casted_obj, expected_obj)
        casted_obj = cast_to_python_objects(pd.Series([obj]))
        self.assertListEqual(casted_obj, [expected_obj])
        casted_obj = cast_to_python_objects(pd.DataFrame({"a": [obj]}))
        self.assertDictEqual(casted_obj, {"a": [expected_obj]})

    def test_cast_to_python_objects_pandas_timedelta(self):
        obj = pd.Timedelta(seconds=1)
        expected_obj = obj.to_pytimedelta()
        casted_obj = cast_to_python_objects(obj)
        self.assertEqual(casted_obj, expected_obj)
        casted_obj = cast_to_python_objects(pd.Series([obj]))
        self.assertListEqual(casted_obj, [expected_obj])
        casted_obj = cast_to_python_objects(pd.DataFrame({"a": [obj]}))
        self.assertDictEqual(casted_obj, {"a": [expected_obj]})

    @require_numpy1_on_windows
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


SIMPLE_FEATURES = [
    Features(),
    Features({"a": Value("int32")}),
    Features({"a": Value("int32", id="my feature")}),
    Features({"a": Value("int32"), "b": Value("float64"), "c": Value("string")}),
]

CUSTOM_FEATURES = [
    Features({"label": ClassLabel(names=["negative", "positive"])}),
    Features({"array": Array2D(dtype="float32", shape=(4, 4))}),
    Features({"image": Image()}),
    Features({"audio": Audio()}),
    Features({"image": Image(decode=False)}),
    Features({"audio": Audio(decode=False)}),
    Features({"translation": Translation(["en", "fr"])}),
    Features({"translation": TranslationVariableLanguages(["en", "fr"])}),
]

NESTED_FEATURES = [
    Features({"foo": {}}),
    Features({"foo": {"bar": Value("int32")}}),
    Features({"foo": {"bar1": Value("int32"), "bar2": Value("float64")}}),
    Features({"foo": Sequence(Value("int32"))}),
    Features({"foo": Sequence({})}),
    Features({"foo": Sequence({"bar": Value("int32")})}),
    Features({"foo": [Value("int32")]}),
    Features({"foo": [{"bar": Value("int32")}]}),
    Features({"foo": LargeList(Value("int32"))}),
    Features({"foo": LargeList({"bar": Value("int32")})}),
]

NESTED_CUSTOM_FEATURES = [
    Features({"foo": {"bar": ClassLabel(names=["negative", "positive"])}}),
    Features({"foo": Sequence(ClassLabel(names=["negative", "positive"]))}),
    Features({"foo": Sequence({"bar": ClassLabel(names=["negative", "positive"])})}),
    Features({"foo": [ClassLabel(names=["negative", "positive"])]}),
    Features({"foo": [{"bar": ClassLabel(names=["negative", "positive"])}]}),
    Features({"foo": LargeList(ClassLabel(names=["negative", "positive"]))}),
    Features({"foo": LargeList({"bar": ClassLabel(names=["negative", "positive"])})}),
]


@pytest.mark.parametrize("features", SIMPLE_FEATURES + CUSTOM_FEATURES + NESTED_FEATURES + NESTED_CUSTOM_FEATURES)
def test_features_to_dict_and_from_dict_round_trip(features: Features):
    features_dict = features.to_dict()
    assert isinstance(features_dict, dict)
    reloaded = Features.from_dict(features_dict)
    assert features == reloaded


@pytest.mark.parametrize("features", SIMPLE_FEATURES + CUSTOM_FEATURES + NESTED_FEATURES + NESTED_CUSTOM_FEATURES)
def test_features_to_yaml_list(features: Features):
    features_yaml_list = features._to_yaml_list()
    assert isinstance(features_yaml_list, list)
    reloaded = Features._from_yaml_list(features_yaml_list)
    assert features == reloaded


@pytest.mark.parametrize(
    "features_dict, expected_features_dict",
    [
        ({"col": [{"sub_col": Value("int32")}]}, {"col": [{"sub_col": Value("int32")}]}),
        ({"col": LargeList({"sub_col": Value("int32")})}, {"col": LargeList({"sub_col": Value("int32")})}),
        ({"col": Sequence({"sub_col": Value("int32")})}, {"col.sub_col": Sequence(Value("int32"))}),
    ],
)
def test_features_flatten_with_list_types(features_dict, expected_features_dict):
    features = Features(features_dict)
    flattened_features = features.flatten()
    assert flattened_features == Features(expected_features_dict)


@pytest.mark.parametrize(
    "deserialized_features_dict, expected_features_dict",
    [
        (
            {"col": [{"dtype": "int32", "_type": "Value"}]},
            {"col": [Value("int32")]},
        ),
        (
            {"col": {"feature": {"dtype": "int32", "_type": "Value"}, "_type": "LargeList"}},
            {"col": LargeList(Value("int32"))},
        ),
        (
            {"col": {"feature": {"dtype": "int32", "_type": "Value"}, "_type": "Sequence"}},
            {"col": Sequence(Value("int32"))},
        ),
        (
            {"col": [{"sub_col": {"dtype": "int32", "_type": "Value"}}]},
            {"col": [{"sub_col": Value("int32")}]},
        ),
        (
            {"col": {"feature": {"sub_col": {"dtype": "int32", "_type": "Value"}}, "_type": "LargeList"}},
            {"col": LargeList({"sub_col": Value("int32")})},
        ),
        (
            {"col": {"feature": {"sub_col": {"dtype": "int32", "_type": "Value"}}, "_type": "Sequence"}},
            {"col": Sequence({"sub_col": Value("int32")})},
        ),
    ],
)
def test_features_from_dict_with_list_types(deserialized_features_dict, expected_features_dict):
    features = Features.from_dict(deserialized_features_dict)
    assert features == Features(expected_features_dict)


@pytest.mark.parametrize(
    "deserialized_feature_dict, expected_feature",
    [
        (
            [{"dtype": "int32", "_type": "Value"}],
            [Value("int32")],
        ),
        (
            {"feature": {"dtype": "int32", "_type": "Value"}, "_type": "LargeList"},
            LargeList(Value("int32")),
        ),
        (
            {"feature": {"dtype": "int32", "_type": "Value"}, "_type": "Sequence"},
            Sequence(Value("int32")),
        ),
        (
            [{"sub_col": {"dtype": "int32", "_type": "Value"}}],
            [{"sub_col": Value("int32")}],
        ),
        (
            {"feature": {"sub_col": {"dtype": "int32", "_type": "Value"}}, "_type": "LargeList"},
            LargeList({"sub_col": Value("int32")}),
        ),
        (
            {"feature": {"sub_col": {"dtype": "int32", "_type": "Value"}}, "_type": "Sequence"},
            Sequence({"sub_col": Value("int32")}),
        ),
    ],
)
def test_generate_from_dict_with_list_types(deserialized_feature_dict, expected_feature):
    feature = generate_from_dict(deserialized_feature_dict)
    assert feature == expected_feature


@pytest.mark.parametrize(
    "features_dict, expected_features_yaml_list",
    [
        ({"col": LargeList(Value("int32"))}, [{"name": "col", "large_list": "int32"}]),
        (
            {"col": LargeList({"sub_col": Value("int32")})},
            [{"name": "col", "large_list": [{"dtype": "int32", "name": "sub_col"}]}],
        ),
    ],
)
def test_features_to_yaml_list_with_large_list(features_dict, expected_features_yaml_list):
    features = Features(features_dict)
    features_yaml_list = features._to_yaml_list()
    assert features_yaml_list == expected_features_yaml_list


@pytest.mark.parametrize(
    "features_yaml_list, expected_features_dict",
    [
        ([{"name": "col", "large_list": "int32"}], {"col": LargeList(Value("int32"))}),
        (
            [{"name": "col", "large_list": [{"dtype": "int32", "name": "sub_col"}]}],
            {"col": LargeList({"sub_col": Value("int32")})},
        ),
    ],
)
def test_features_from_yaml_list_with_large_list(features_yaml_list, expected_features_dict):
    features = Features._from_yaml_list(features_yaml_list)
    assert features == Features(expected_features_dict)


@pytest.mark.parametrize("features", SIMPLE_FEATURES + CUSTOM_FEATURES + NESTED_FEATURES + NESTED_CUSTOM_FEATURES)
def test_features_to_arrow_schema(features: Features):
    arrow_schema = features.arrow_schema
    assert isinstance(arrow_schema, pa.Schema)
    reloaded = Features.from_arrow_schema(arrow_schema)
    assert features == reloaded


NESTED_COMPARISON = [
    [
        [Features({"email": Value(dtype="string", id=None)}), Features({"email": Value(dtype="string", id=None)})],
        [Features({"email": Value(dtype="string", id=None)}), Features({"email": Value(dtype="string", id=None)})],
    ],
    [
        [Features({"email": Value(dtype="string", id=None)}), Features({"email": Value(dtype="null", id=None)})],
        [Features({"email": Value(dtype="string", id=None)}), Features({"email": Value(dtype="string", id=None)})],
    ],
    [
        [
            Features({"speaker": {"email": Value(dtype="string", id=None)}}),
            Features({"speaker": {"email": Value(dtype="string", id=None)}}),
        ],
        [
            Features({"speaker": {"email": Value(dtype="string", id=None)}}),
            Features({"speaker": {"email": Value(dtype="string", id=None)}}),
        ],
    ],
    [
        [
            Features({"speaker": {"email": Value(dtype="string", id=None)}}),
            Features({"speaker": {"email": Value(dtype="null", id=None)}}),
        ],
        [
            Features({"speaker": {"email": Value(dtype="string", id=None)}}),
            Features({"speaker": {"email": Value(dtype="string", id=None)}}),
        ],
    ],
]


@pytest.mark.parametrize("features", NESTED_COMPARISON)
def test_features_alignment(features: Tuple[List[Features], Features]):
    inputs, expected = features
    _check_if_features_can_be_aligned(inputs)  # Check that we can align, will raise otherwise.
    assert _align_features(inputs) == expected


@pytest.mark.parametrize("dtype", [pa.int32, pa.string])
def test_features_from_arrow_schema_primitive_data_type(dtype):
    schema = pa.schema([("column_name", dtype())])
    assert schema == Features.from_arrow_schema(schema).arrow_schema


@pytest.mark.parametrize("scalar_dtype", [pa.int32, pa.string])
@pytest.mark.parametrize("list_dtype", [pa.list_, pa.large_list])
def test_features_from_arrow_schema_list_data_type(list_dtype, scalar_dtype):
    schema = pa.schema([("column_name", list_dtype(scalar_dtype()))])
    assert schema == Features.from_arrow_schema(schema).arrow_schema


@pytest.mark.parametrize(
    "feature, other_feature",
    [
        ([Value("int64")], [Value("int64")]),
        (LargeList(Value("int64")), LargeList(Value("int64"))),
        (Sequence(Value("int64")), Sequence(Value("int64"))),
        (
            [{"sub_col_1": Value("int64"), "sub_col_2": Value("int64")}],
            [{"sub_col_2": Value("int64"), "sub_col_1": Value("int64")}],
        ),
        (
            LargeList({"sub_col_1": Value("int64"), "sub_col_2": Value("int64")}),
            LargeList({"sub_col_2": Value("int64"), "sub_col_1": Value("int64")}),
        ),
        (
            Sequence({"sub_col_1": Value("int64"), "sub_col_2": Value("int64")}),
            Sequence({"sub_col_2": Value("int64"), "sub_col_1": Value("int64")}),
        ),
    ],
)
def test_features_reorder_fields_as_with_list_types(feature, other_feature):
    features = Features({"col": feature})
    other_features = Features({"col": other_feature})
    new_features = features.reorder_fields_as(other_features)
    assert new_features.type == other_features.type


@pytest.mark.parametrize(
    "feature, expected_arrow_data_type", [(Value("int64"), pa.int64), (Value("string"), pa.string)]
)
def test_get_nested_type_with_scalar_feature(feature, expected_arrow_data_type):
    arrow_data_type = get_nested_type(feature)
    assert arrow_data_type == expected_arrow_data_type()


@pytest.mark.parametrize(
    "scalar_feature, expected_arrow_primitive_data_type", [(Value("int64"), pa.int64), (Value("string"), pa.string)]
)
@pytest.mark.parametrize(
    "list_feature, expected_arrow_nested_data_type",
    [(list_with, pa.list_), (LargeList, pa.large_list), (Sequence, pa.list_)],
)
def test_get_nested_type_with_list_feature(
    list_feature, expected_arrow_nested_data_type, scalar_feature, expected_arrow_primitive_data_type
):
    feature = list_feature(scalar_feature)
    arrow_data_type = get_nested_type(feature)
    assert arrow_data_type == expected_arrow_nested_data_type(expected_arrow_primitive_data_type())


@pytest.mark.parametrize(
    "arrow_primitive_data_type, expected_feature", [(pa.int32, Value("int32")), (pa.string, Value("string"))]
)
def test_generate_from_arrow_type_with_arrow_primitive_data_type(arrow_primitive_data_type, expected_feature):
    arrow_data_type = arrow_primitive_data_type()
    feature = generate_from_arrow_type(arrow_data_type)
    assert feature == expected_feature


@pytest.mark.parametrize(
    "arrow_primitive_data_type, expected_scalar_feature", [(pa.int32, Value("int32")), (pa.string, Value("string"))]
)
@pytest.mark.parametrize(
    "arrow_nested_data_type, expected_list_feature", [(pa.list_, Sequence), (pa.large_list, LargeList)]
)
def test_generate_from_arrow_type_with_arrow_nested_data_type(
    arrow_nested_data_type, expected_list_feature, arrow_primitive_data_type, expected_scalar_feature
):
    arrow_data_type = arrow_nested_data_type(arrow_primitive_data_type())
    feature = generate_from_arrow_type(arrow_data_type)
    expected_feature = expected_list_feature(expected_scalar_feature)
    assert feature == expected_feature


@pytest.mark.parametrize(
    "schema",
    [[ClassLabel(names=["a", "b"])], LargeList(ClassLabel(names=["a", "b"])), Sequence(ClassLabel(names=["a", "b"]))],
)
def test_check_non_null_non_empty_recursive_with_list_types(schema):
    assert _check_non_null_non_empty_recursive([], schema) is False


@pytest.mark.parametrize(
    "schema",
    [
        [[ClassLabel(names=["a", "b"])]],
        LargeList(LargeList(ClassLabel(names=["a", "b"]))),
        Sequence(Sequence(ClassLabel(names=["a", "b"]))),
    ],
)
def test_check_non_null_non_empty_recursive_with_nested_list_types(schema):
    assert _check_non_null_non_empty_recursive([[]], schema) is False


@pytest.mark.parametrize("feature", [[Audio()], LargeList(Audio()), Sequence(Audio())])
def test_require_decoding_with_list_types(feature):
    assert require_decoding(feature)


@pytest.mark.parametrize("feature", [[Audio()], LargeList(Audio()), Sequence(Audio())])
def test_require_storage_cast_with_list_types(feature):
    assert require_storage_cast(feature)


@pytest.mark.parametrize("feature", [[Audio()], LargeList(Audio()), Sequence(Audio())])
def test_require_storage_embed_with_list_types(feature):
    assert require_storage_embed(feature)


@pytest.mark.parametrize(
    "feature, expected",
    [([Value("int32")], [1]), (LargeList(Value("int32")), LargeList(1)), (Sequence(Value("int32")), Sequence(1))],
)
def test_visit_with_list_types(feature, expected):
    def func(x):
        return 1 if isinstance(x, Value) else x

    result = _visit(feature, func)
    assert result == expected
