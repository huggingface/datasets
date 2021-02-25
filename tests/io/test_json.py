import json

import pytest

from datasets import DatasetInfo, Features, NamedSplit, Value
from datasets.io.json import JsonlDatasetReader


DATA = [
    {"col_1": "0", "col_2": 0, "col_3": 0.0},
    {"col_1": "1", "col_2": 1, "col_3": 1.0},
    {"col_1": "2", "col_2": 2, "col_3": 2.0},
    {"col_1": "3", "col_2": 3, "col_3": 3.0},
]


@pytest.fixture(scope="session")
def jsonl_path(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("data") / "dataset.jsonl")
    with open(path, "w") as f:
        for item in DATA:
            f.write(json.dumps(item))
    return path


@pytest.mark.parametrize(
    "features",
    [
        None,
        {"col_1": "string", "col_2": "int64", "col_3": "float64"},
        {"col_1": "string", "col_2": "string", "col_3": "string"},
        {"col_1": "int32", "col_2": "int32", "col_3": "int32"},
        {"col_1": "float32", "col_2": "float32", "col_3": "float32"},
    ],
)
@pytest.mark.parametrize("split, expected_split", [(None, None), (NamedSplit("train"), "train")])
def test_dataset_jsonl_reader(split, expected_split, features, jsonl_path):
    path = jsonl_path
    default_expected_features = {"col_1": "string", "col_2": "int64", "col_3": "float64"}
    expected_features = features.copy() if features else default_expected_features
    features = Features({feature: Value(dtype) for feature, dtype in features.items()}) if features else None
    info = DatasetInfo(features=features) if features else None

    ds = JsonlDatasetReader(path, split=split, info=info).read()
    assert ds.num_rows == 4
    assert ds.num_columns == 3
    assert ds.column_names == ["col_1", "col_2", "col_3"]
    for feature, expected_dtype in expected_features.items():
        assert ds.features[feature].dtype == expected_dtype
    assert ds.split == expected_split


# @pytest.mark.parametrize(
#     "features",
#     [
#         None,
#         {"col_1": "string", "col_2": "int64", "col_3": "float64"},
#         {"col_1": "string", "col_2": "string", "col_3": "string"},
#         {"col_1": "int32", "col_2": "int32", "col_3": "int32"},
#         {"col_1": "float32", "col_2": "float32", "col_3": "float32"},
#     ],
# )
# # @pytest.mark.parametrize("col_3_dtype", [None, "string", "int32", "int64", "float32", "float64"])
# # @pytest.mark.parametrize("col_2_dtype", [None, "string", "int32", "int64", "float32", "float64"])
# # @pytest.mark.parametrize("col_1_dtype", [None, "string", "int32", "int64", "float32", "float64"])
# @pytest.mark.parametrize("split, expected_split", [(None, None), (NamedSplit("train"), "train")])
# # def test_dataset_jsonl_reader(split, expected_split, col_1_dtype, col_2_dtype, col_3_dtype, jsonl_path):  # features,
# def test_dataset_jsonl_reader(split, expected_split, features, jsonl_path):  # features,
#     # feature_names = ["col_1", "col_2", "col_3"]
#     # feature_dtypes = [col_1_dtype, col_2_dtype, col_3_dtype]
#     # feature_default_dtypes = ["string", "int64", "float64"]
#     path = jsonl_path
#     expected_features = features.copy() if features else {"col_1": "string", "col_2": "int64", "col_3": "float64"}
#     features = Features({feature: Value(dtype) for feature, dtype in features.items()}) if features else None
#     info = DatasetInfo(features=features) if features else None
#
#     # expected_features = {
#     #     feature: dtype or default_dtype
#     #     for feature, dtype, default_dtype in zip(feature_names, feature_dtypes, feature_default_dtypes)
#     # }
#     # features = Features(
#     #     {
#     #         feature: Value(dtype or default_dtype)
#     #         for feature, dtype, default_dtype in zip(feature_names, feature_dtypes, feature_default_dtypes)
#     #     }
#     # ) if any(feature_dtypes) else None
#     # info = DatasetInfo(features=features) if features else None
#
#
#     # if info:
#     #     info = DatasetInfo(features=Features({"col_1": Value("string"), "col_2": Value("int64"), "col_3": Value("float32")}))
#     ds = JsonlDatasetReader(path, split=split, info=info).read()
#     assert ds.num_rows == 4
#     assert ds.num_columns == 3
#     assert ds.column_names == ["col_1", "col_2", "col_3"] # feature_names
#     # assert ds.features["col_1"].dtype == "string"
#     # assert ds.features["col_2"].dtype == "int64"
#     # assert ds.features["col_3"].dtype == "float64"
#     for feature, dtype in expected_features.items():
#         assert ds.features[feature].dtype == dtype
#     assert ds.split == expected_split
#     # assert ds.info == expected_info
