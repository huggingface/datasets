import csv
import json
import lzma
import shutil
import textwrap

import numpy as np
import pytest

from datasets.arrow_dataset import Dataset
from datasets.features import ClassLabel, Features, Sequence, Value, Array2D, Array3D

from .s3_fixtures import *  # noqa: load s3 fixtures


FILE_CONTENT = """\
    Text data.
    Second line of data."""


@pytest.fixture(scope="session")
def dataset():
    n = 10
    features = Features(
        {
            "tokens": Sequence(Value("string")),
            "labels": Sequence(ClassLabel(names=["negative", "positive"])),
            "answers": Sequence(
                {
                    "text": Value("string"),
                    "answer_start": Value("int32"),
                }
            ),
            "id": Value("int64"),
        }
    )
    dataset = Dataset.from_dict(
        {
            "tokens": [["foo"] * 5] * n,
            "labels": [[1] * 5] * n,
            "answers": [{"answer_start": [97], "text": ["1976"]}] * 10,
            "id": list(range(n)),
        },
        features=features,
    )
    return dataset


@pytest.fixture(scope="session")
def arrow_file(tmp_path_factory, dataset):
    filename = str(tmp_path_factory.mktemp("data") / "file.arrow")
    dataset.map(cache_file_name=filename)
    return filename


@pytest.fixture(scope="session")
def text_file(tmp_path_factory):
    filename = tmp_path_factory.mktemp("data") / "file.txt"
    data = FILE_CONTENT
    with open(filename, "w") as f:
        f.write(data)
    return filename


@pytest.fixture(scope="session")
def xz_file(tmp_path_factory):
    filename = tmp_path_factory.mktemp("data") / "file.xz"
    data = bytes(FILE_CONTENT, "utf-8")
    with lzma.open(filename, "wb") as f:
        f.write(data)
    return filename


@pytest.fixture(scope="session")
def xml_file(tmp_path_factory):
    filename = tmp_path_factory.mktemp("data") / "file.xml"
    data = textwrap.dedent(
        """\
    <?xml version="1.0" encoding="UTF-8" ?>
    <tmx version="1.4">
      <header segtype="sentence" srclang="ca" />
      <body>
        <tu>
          <tuv xml:lang="ca"><seg>Contingut 1</seg></tuv>
          <tuv xml:lang="en"><seg>Content 1</seg></tuv>
        </tu>
        <tu>
          <tuv xml:lang="ca"><seg>Contingut 2</seg></tuv>
          <tuv xml:lang="en"><seg>Content 2</seg></tuv>
        </tu>
        <tu>
          <tuv xml:lang="ca"><seg>Contingut 3</seg></tuv>
          <tuv xml:lang="en"><seg>Content 3</seg></tuv>
        </tu>
        <tu>
          <tuv xml:lang="ca"><seg>Contingut 4</seg></tuv>
          <tuv xml:lang="en"><seg>Content 4</seg></tuv>
        </tu>
        <tu>
          <tuv xml:lang="ca"><seg>Contingut 5</seg></tuv>
          <tuv xml:lang="en"><seg>Content 5</seg></tuv>
        </tu>
      </body>
    </tmx>"""
    )
    with open(filename, "w") as f:
        f.write(data)
    return filename


DATA = [
    {"col_1": "0", "col_2": 0, "col_3": 0.0},
    {"col_1": "1", "col_2": 1, "col_3": 1.0},
    {"col_1": "2", "col_2": 2, "col_3": 2.0},
    {"col_1": "3", "col_2": 3, "col_3": 3.0},
]
DATA_DICT_OF_LISTS = {
    "col_1": ["0", "1", "2", "3"],
    "col_2": [0, 1, 2, 3],
    "col_3": [0.0, 1.0, 2.0, 3.0],
}


@pytest.fixture(scope="session")
def csv_path(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("data") / "dataset.csv")
    with open(path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=["col_1", "col_2", "col_3"])
        writer.writeheader()
        for item in DATA:
            writer.writerow(item)
    return path


@pytest.fixture(scope="session")
def json_list_of_dicts_path(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("data") / "dataset.json")
    data = {"data": DATA}
    with open(path, "w") as f:
        json.dump(data, f)
    return path


@pytest.fixture(scope="session")
def json_dict_of_lists_path(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("data") / "dataset.json")
    data = {"data": DATA_DICT_OF_LISTS}
    with open(path, "w") as f:
        json.dump(data, f)
    return path


@pytest.fixture(scope="session")
def jsonl_path(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("data") / "dataset.jsonl")
    with open(path, "w") as f:
        for item in DATA:
            f.write(json.dumps(item))
    return path


@pytest.fixture(scope="session")
def text_path(tmp_path_factory):
    data = ["0", "1", "2", "3"]
    path = str(tmp_path_factory.mktemp("data") / "dataset.txt")
    with open(path, "w") as f:
        for item in data:
            f.write(item + "\n")
    return path


@pytest.fixture
def tmp_dir(tmp_path):
    yield str(tmp_path)
    shutil.rmtree(tmp_path)


@pytest.fixture
def create_dummy_dataset(tmp_dir):
    created_datasets = []

    def _create_dummy_dataset(in_memory: bool = None, multiple_columns=False, array_features=False):
        if multiple_columns:
            if array_features:
                data = {
                    "col_1": [[[True, False], [False, True]]] * 4,  # 2D
                    "col_2": [[[["a", "b"], ["c", "d"]], [["e", "f"], ["g", "h"]]]] * 4,  # 3D array
                    "col_3": [[3, 2, 1, 0]] * 4,  # Sequence
                }
                features = Features(
                    {
                        "col_1": Array2D(shape=(2, 2), dtype="bool"),
                        "col_2": Array3D(shape=(2, 2, 2), dtype="string"),
                        "col_3": Sequence(feature=Value("int64")),
                    }
                )
            else:
                data = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", "d"], "col_3": [False, True, False, True]}
                features = None
            dset = Dataset.from_dict(data, features=features)
        else:
            dset = Dataset.from_dict({"filename": ["my_name-train" + "_" + str(x) for x in np.arange(30).tolist()]})
        if in_memory:
            dset = dset.map(keep_in_memory=True)
        else:
            start = 0
            while os.path.isfile(os.path.join(tmp_dir, f"dataset{start}.arrow")):
                start += 1
            dset = dset.map(cache_file_name=os.path.join(tmp_dir, f"dataset{start}.arrow"))
        created_datasets.append(dset)
        return dset

    yield _create_dummy_dataset
    for dataset in created_datasets:
        dataset.__del__()
