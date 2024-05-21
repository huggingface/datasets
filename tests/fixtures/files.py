import contextlib
import csv
import json
import os
import sqlite3
import tarfile
import textwrap
import zipfile

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

import datasets
import datasets.config


# dataset + arrow_file


@pytest.fixture(scope="session")
def dataset():
    n = 10
    features = datasets.Features(
        {
            "tokens": datasets.Sequence(datasets.Value("string")),
            "labels": datasets.Sequence(datasets.ClassLabel(names=["negative", "positive"])),
            "answers": datasets.Sequence(
                {
                    "text": datasets.Value("string"),
                    "answer_start": datasets.Value("int32"),
                }
            ),
            "id": datasets.Value("int64"),
        }
    )
    dataset = datasets.Dataset.from_dict(
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


# FILE_CONTENT + files


FILE_CONTENT = """\
    Text data.
    Second line of data."""


@pytest.fixture(scope="session")
def text_file_content():
    return FILE_CONTENT


@pytest.fixture(scope="session")
def text_file(tmp_path_factory):
    filename = tmp_path_factory.mktemp("data") / "file.txt"
    data = FILE_CONTENT
    with open(filename, "w") as f:
        f.write(data)
    return filename


@pytest.fixture(scope="session")
def bz2_file(tmp_path_factory):
    import bz2

    path = tmp_path_factory.mktemp("data") / "file.txt.bz2"
    data = bytes(FILE_CONTENT, "utf-8")
    with bz2.open(path, "wb") as f:
        f.write(data)
    return path


@pytest.fixture(scope="session")
def gz_file(tmp_path_factory):
    import gzip

    path = str(tmp_path_factory.mktemp("data") / "file.txt.gz")
    data = bytes(FILE_CONTENT, "utf-8")
    with gzip.open(path, "wb") as f:
        f.write(data)
    return path


@pytest.fixture(scope="session")
def lz4_file(tmp_path_factory):
    if datasets.config.LZ4_AVAILABLE:
        import lz4.frame

        path = tmp_path_factory.mktemp("data") / "file.txt.lz4"
        data = bytes(FILE_CONTENT, "utf-8")
        with lz4.frame.open(path, "wb") as f:
            f.write(data)
        return path


@pytest.fixture(scope="session")
def seven_zip_file(tmp_path_factory, text_file):
    if datasets.config.PY7ZR_AVAILABLE:
        import py7zr

        path = tmp_path_factory.mktemp("data") / "file.txt.7z"
        with py7zr.SevenZipFile(path, "w") as archive:
            archive.write(text_file, arcname=os.path.basename(text_file))
        return path


@pytest.fixture(scope="session")
def tar_file(tmp_path_factory, text_file):
    import tarfile

    path = tmp_path_factory.mktemp("data") / "file.txt.tar"
    with tarfile.TarFile(path, "w") as f:
        f.add(text_file, arcname=os.path.basename(text_file))
    return path


@pytest.fixture(scope="session")
def xz_file(tmp_path_factory):
    import lzma

    path = tmp_path_factory.mktemp("data") / "file.txt.xz"
    data = bytes(FILE_CONTENT, "utf-8")
    with lzma.open(path, "wb") as f:
        f.write(data)
    return path


@pytest.fixture(scope="session")
def zip_file(tmp_path_factory, text_file):
    import zipfile

    path = tmp_path_factory.mktemp("data") / "file.txt.zip"
    with zipfile.ZipFile(path, "w") as f:
        f.write(text_file, arcname=os.path.basename(text_file))
    return path


@pytest.fixture(scope="session")
def zstd_file(tmp_path_factory):
    if datasets.config.ZSTANDARD_AVAILABLE:
        import zstandard as zstd

        path = tmp_path_factory.mktemp("data") / "file.txt.zst"
        data = bytes(FILE_CONTENT, "utf-8")
        with zstd.open(path, "wb") as f:
            f.write(data)
        return path


# xml_file


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
DATA2 = [
    {"col_1": "4", "col_2": 4, "col_3": 4.0},
    {"col_1": "5", "col_2": 5, "col_3": 5.0},
]
DATA_DICT_OF_LISTS = {
    "col_1": ["0", "1", "2", "3"],
    "col_2": [0, 1, 2, 3],
    "col_3": [0.0, 1.0, 2.0, 3.0],
}

DATA_312 = [
    {"col_3": 0.0, "col_1": "0", "col_2": 0},
    {"col_3": 1.0, "col_1": "1", "col_2": 1},
]

DATA_STR = [
    {"col_1": "s0", "col_2": 0, "col_3": 0.0},
    {"col_1": "s1", "col_2": 1, "col_3": 1.0},
    {"col_1": "s2", "col_2": 2, "col_3": 2.0},
    {"col_1": "s3", "col_2": 3, "col_3": 3.0},
]


@pytest.fixture(scope="session")
def dataset_dict():
    return DATA_DICT_OF_LISTS


@pytest.fixture(scope="session")
def arrow_path(tmp_path_factory):
    dataset = datasets.Dataset.from_dict(DATA_DICT_OF_LISTS)
    path = str(tmp_path_factory.mktemp("data") / "dataset.arrow")
    dataset.map(cache_file_name=path)
    return path


@pytest.fixture(scope="session")
def sqlite_path(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("data") / "dataset.sqlite")
    with contextlib.closing(sqlite3.connect(path)) as con:
        cur = con.cursor()
        cur.execute("CREATE TABLE dataset(col_1 text, col_2 int, col_3 real)")
        for item in DATA:
            cur.execute("INSERT INTO dataset(col_1, col_2, col_3) VALUES (?, ?, ?)", tuple(item.values()))
        con.commit()
    return path


@pytest.fixture(scope="session")
def csv_path(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("data") / "dataset.csv")
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["col_1", "col_2", "col_3"])
        writer.writeheader()
        for item in DATA:
            writer.writerow(item)
    return path


@pytest.fixture(scope="session")
def csv2_path(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("data") / "dataset2.csv")
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["col_1", "col_2", "col_3"])
        writer.writeheader()
        for item in DATA:
            writer.writerow(item)
    return path


@pytest.fixture(scope="session")
def bz2_csv_path(csv_path, tmp_path_factory):
    import bz2

    path = tmp_path_factory.mktemp("data") / "dataset.csv.bz2"
    with open(csv_path, "rb") as f:
        data = f.read()
    # data = bytes(FILE_CONTENT, "utf-8")
    with bz2.open(path, "wb") as f:
        f.write(data)
    return path


@pytest.fixture(scope="session")
def zip_csv_path(csv_path, csv2_path, tmp_path_factory):
    path = tmp_path_factory.mktemp("zip_csv_path") / "csv-dataset.zip"
    with zipfile.ZipFile(path, "w") as f:
        f.write(csv_path, arcname=os.path.basename(csv_path))
        f.write(csv2_path, arcname=os.path.basename(csv2_path))
    return path


@pytest.fixture(scope="session")
def zip_uppercase_csv_path(csv_path, csv2_path, tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / "dataset.csv.zip"
    with zipfile.ZipFile(path, "w") as f:
        f.write(csv_path, arcname=os.path.basename(csv_path.replace(".csv", ".CSV")))
        f.write(csv2_path, arcname=os.path.basename(csv2_path.replace(".csv", ".CSV")))
    return path


@pytest.fixture(scope="session")
def zip_csv_with_dir_path(csv_path, csv2_path, tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / "dataset_with_dir.csv.zip"
    with zipfile.ZipFile(path, "w") as f:
        f.write(csv_path, arcname=os.path.join("main_dir", os.path.basename(csv_path)))
        f.write(csv2_path, arcname=os.path.join("main_dir", os.path.basename(csv2_path)))
    return path


@pytest.fixture(scope="session")
def parquet_path(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("data") / "dataset.parquet")
    schema = pa.schema(
        {
            "col_1": pa.string(),
            "col_2": pa.int64(),
            "col_3": pa.float64(),
        }
    )
    with open(path, "wb") as f:
        writer = pq.ParquetWriter(f, schema=schema)
        pa_table = pa.Table.from_pydict({k: [DATA[i][k] for i in range(len(DATA))] for k in DATA[0]}, schema=schema)
        writer.write_table(pa_table)
        writer.close()
    return path


@pytest.fixture(scope="session")
def geoparquet_path(tmp_path_factory):
    df = pd.read_parquet(path="https://github.com/opengeospatial/geoparquet/raw/v1.0.0/examples/example.parquet")
    path = str(tmp_path_factory.mktemp("data") / "dataset.geoparquet")
    df.to_parquet(path=path)
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
            f.write(json.dumps(item) + "\n")
    return path


@pytest.fixture(scope="session")
def jsonl2_path(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("data") / "dataset2.jsonl")
    with open(path, "w") as f:
        for item in DATA:
            f.write(json.dumps(item) + "\n")
    return path


@pytest.fixture(scope="session")
def jsonl_312_path(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("data") / "dataset_312.jsonl")
    with open(path, "w") as f:
        for item in DATA_312:
            f.write(json.dumps(item) + "\n")
    return path


@pytest.fixture(scope="session")
def jsonl_str_path(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("data") / "dataset-str.jsonl")
    with open(path, "w") as f:
        for item in DATA_STR:
            f.write(json.dumps(item) + "\n")
    return path


@pytest.fixture(scope="session")
def text_gz_path(tmp_path_factory, text_path):
    import gzip

    path = str(tmp_path_factory.mktemp("data") / "dataset.txt.gz")
    with open(text_path, "rb") as orig_file:
        with gzip.open(path, "wb") as zipped_file:
            zipped_file.writelines(orig_file)
    return path


@pytest.fixture(scope="session")
def jsonl_gz_path(tmp_path_factory, jsonl_path):
    import gzip

    path = str(tmp_path_factory.mktemp("data") / "dataset.jsonl.gz")
    with open(jsonl_path, "rb") as orig_file:
        with gzip.open(path, "wb") as zipped_file:
            zipped_file.writelines(orig_file)
    return path


@pytest.fixture(scope="session")
def zip_jsonl_path(jsonl_path, jsonl2_path, tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / "dataset.jsonl.zip"
    with zipfile.ZipFile(path, "w") as f:
        f.write(jsonl_path, arcname=os.path.basename(jsonl_path))
        f.write(jsonl2_path, arcname=os.path.basename(jsonl2_path))
    return path


@pytest.fixture(scope="session")
def zip_nested_jsonl_path(zip_jsonl_path, jsonl_path, jsonl2_path, tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / "dataset_nested.jsonl.zip"
    with zipfile.ZipFile(path, "w") as f:
        f.write(zip_jsonl_path, arcname=os.path.join("nested", os.path.basename(zip_jsonl_path)))
    return path


@pytest.fixture(scope="session")
def zip_jsonl_with_dir_path(jsonl_path, jsonl2_path, tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / "dataset_with_dir.jsonl.zip"
    with zipfile.ZipFile(path, "w") as f:
        f.write(jsonl_path, arcname=os.path.join("main_dir", os.path.basename(jsonl_path)))
        f.write(jsonl2_path, arcname=os.path.join("main_dir", os.path.basename(jsonl2_path)))
    return path


@pytest.fixture(scope="session")
def tar_jsonl_path(jsonl_path, jsonl2_path, tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / "dataset.jsonl.tar"
    with tarfile.TarFile(path, "w") as f:
        f.add(jsonl_path, arcname=os.path.basename(jsonl_path))
        f.add(jsonl2_path, arcname=os.path.basename(jsonl2_path))
    return path


@pytest.fixture(scope="session")
def tar_nested_jsonl_path(tar_jsonl_path, jsonl_path, jsonl2_path, tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / "dataset_nested.jsonl.tar"
    with tarfile.TarFile(path, "w") as f:
        f.add(tar_jsonl_path, arcname=os.path.join("nested", os.path.basename(tar_jsonl_path)))
    return path


@pytest.fixture(scope="session")
def text_path(tmp_path_factory):
    data = ["0", "1", "2", "3"]
    path = str(tmp_path_factory.mktemp("data") / "dataset.txt")
    with open(path, "w") as f:
        for item in data:
            f.write(item + "\n")
    return path


@pytest.fixture(scope="session")
def text2_path(tmp_path_factory):
    data = ["0", "1", "2", "3"]
    path = str(tmp_path_factory.mktemp("data") / "dataset2.txt")
    with open(path, "w") as f:
        for item in data:
            f.write(item + "\n")
    return path


@pytest.fixture(scope="session")
def text_dir(tmp_path_factory):
    data = ["0", "1", "2", "3"]
    path = tmp_path_factory.mktemp("data_text_dir") / "dataset.txt"
    with open(path, "w") as f:
        for item in data:
            f.write(item + "\n")
    return path.parent


@pytest.fixture(scope="session")
def text_dir_with_unsupported_extension(tmp_path_factory):
    data = ["0", "1", "2", "3"]
    path = tmp_path_factory.mktemp("data") / "dataset.abc"
    with open(path, "w") as f:
        for item in data:
            f.write(item + "\n")
    return path


@pytest.fixture(scope="session")
def zip_text_path(text_path, text2_path, tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / "dataset.text.zip"
    with zipfile.ZipFile(path, "w") as f:
        f.write(text_path, arcname=os.path.basename(text_path))
        f.write(text2_path, arcname=os.path.basename(text2_path))
    return path


@pytest.fixture(scope="session")
def zip_text_with_dir_path(text_path, text2_path, tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / "dataset_with_dir.text.zip"
    with zipfile.ZipFile(path, "w") as f:
        f.write(text_path, arcname=os.path.join("main_dir", os.path.basename(text_path)))
        f.write(text2_path, arcname=os.path.join("main_dir", os.path.basename(text2_path)))
    return path


@pytest.fixture(scope="session")
def zip_unsupported_ext_path(text_path, text2_path, tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / "dataset.ext.zip"
    with zipfile.ZipFile(path, "w") as f:
        f.write(text_path, arcname=os.path.basename("unsupported.ext"))
        f.write(text2_path, arcname=os.path.basename("unsupported_2.ext"))
    return path


@pytest.fixture(scope="session")
def text_path_with_unicode_new_lines(tmp_path_factory):
    text = "\n".join(["First", "Second\u2029with Unicode new line", "Third"])
    path = str(tmp_path_factory.mktemp("data") / "dataset_with_unicode_new_lines.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


@pytest.fixture(scope="session")
def image_file():
    return os.path.join("tests", "features", "data", "test_image_rgb.jpg")


@pytest.fixture(scope="session")
def audio_file():
    return os.path.join("tests", "features", "data", "test_audio_44100.wav")


@pytest.fixture(scope="session")
def zip_image_path(image_file, tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / "dataset.img.zip"
    with zipfile.ZipFile(path, "w") as f:
        f.write(image_file, arcname=os.path.basename(image_file))
        f.write(image_file, arcname=os.path.basename(image_file).replace(".jpg", "2.jpg"))
    return path


@pytest.fixture(scope="session")
def data_dir_with_hidden_files(tmp_path_factory):
    data_dir = tmp_path_factory.mktemp("data_dir")

    (data_dir / "subdir").mkdir()
    with open(data_dir / "subdir" / "train.txt", "w") as f:
        f.write("foo\n" * 10)
    with open(data_dir / "subdir" / "test.txt", "w") as f:
        f.write("bar\n" * 10)
    # hidden file
    with open(data_dir / "subdir" / ".test.txt", "w") as f:
        f.write("bar\n" * 10)

    # hidden directory
    (data_dir / ".subdir").mkdir()
    with open(data_dir / ".subdir" / "train.txt", "w") as f:
        f.write("foo\n" * 10)
    with open(data_dir / ".subdir" / "test.txt", "w") as f:
        f.write("bar\n" * 10)

    return data_dir
