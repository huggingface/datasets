import os
import textwrap

import pyarrow as pa
import pytest
from packaging import version

import datasets.config
from datasets import ClassLabel, Features, Image, Value
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.csv.csv import Csv, CsvConfig

from ..utils import require_pil


@pytest.fixture
def csv_file(tmp_path):
    filename = tmp_path / "file.csv"
    data = textwrap.dedent(
        """\
        header1,header2
        1,2
        10,20
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def malformed_csv_file(tmp_path):
    filename = tmp_path / "malformed_file.csv"
    data = textwrap.dedent(
        """\
        header1,header2
        1,2
        10,20,
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def csv_file_with_image(tmp_path, image_file):
    filename = tmp_path / "csv_with_image.csv"
    data = textwrap.dedent(
        f"""\
        image
        {image_file}
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def csv_file_with_label(tmp_path):
    filename = tmp_path / "csv_with_label.csv"
    data = textwrap.dedent(
        """\
        label
        good
        bad
        good
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def csv_file_with_int_list(tmp_path):
    filename = tmp_path / "csv_with_int_list.csv"
    data = textwrap.dedent(
        """\
        int_list
        1 2 3
        4 5 6
        7 8 9
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = CsvConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = CsvConfig(name="name", data_files=data_files)


def test_csv_generate_tables_raises_error_with_malformed_csv(csv_file, malformed_csv_file, caplog):
    csv = Csv()
    base_files = [csv_file, malformed_csv_file]
    files_iterables = [[file] for file in base_files]
    generator = csv._generate_tables(base_files=base_files, files_iterables=files_iterables)
    with pytest.raises(ValueError, match="Error tokenizing data"):
        for _ in generator:
            pass
    assert any(
        record.levelname == "ERROR"
        and "Failed to read file" in record.message
        and os.path.basename(malformed_csv_file) in record.message
        for record in caplog.records
    )


@require_pil
def test_csv_cast_image(csv_file_with_image):
    with open(csv_file_with_image, encoding="utf-8") as f:
        image_file = f.read().splitlines()[1]
    csv = Csv(encoding="utf-8", features=Features({"image": Image()}))
    base_files = [csv_file_with_image]
    files_iterables = [[file] for file in base_files]
    generator = csv._generate_tables(base_files=base_files, files_iterables=files_iterables)
    pa_table = pa.concat_tables([table for _, table in generator])
    assert pa_table.schema.field("image").type == Image()()
    generated_content = pa_table.to_pydict()["image"]
    assert generated_content == [{"path": image_file, "bytes": None}]


def test_csv_cast_label(csv_file_with_label):
    with open(csv_file_with_label, encoding="utf-8") as f:
        labels = f.read().splitlines()[1:]
    csv = Csv(encoding="utf-8", features=Features({"label": ClassLabel(names=["good", "bad"])}))
    base_files = [csv_file_with_label]
    files_iterables = [[file] for file in base_files]
    generator = csv._generate_tables(base_files=base_files, files_iterables=files_iterables)
    pa_table = pa.concat_tables([table for _, table in generator])
    assert pa_table.schema.field("label").type == ClassLabel(names=["good", "bad"])()
    generated_content = pa_table.to_pydict()["label"]
    assert generated_content == [ClassLabel(names=["good", "bad"]).str2int(label) for label in labels]


def test_csv_convert_int_list(csv_file_with_int_list):
    csv = Csv(encoding="utf-8", sep=",", converters={"int_list": lambda x: [int(i) for i in x.split()]})
    base_files = [csv_file_with_int_list]
    files_iterables = [[file] for file in base_files]
    generator = csv._generate_tables(base_files=base_files, files_iterables=files_iterables)
    pa_table = pa.concat_tables([table for _, table in generator])
    assert pa.types.is_list(pa_table.schema.field("int_list").type)
    generated_content = pa_table.to_pydict()["int_list"]
    assert generated_content == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


@pytest.mark.parametrize(
    "dtype, values",
    [
        ("int8", [-128, 127]),
        ("int16", [-32768, 32767]),
        ("int32", [-2147483648, 2147483647]),
        ("int64", [-9223372036854775808, 9007199254740993, 9223372036854775807]),
        ("uint8", [0, 255]),
        ("uint16", [0, 65535]),
        ("uint32", [0, 4294967295]),
        ("uint64", [0, 9007199254740993, 18446744073709551615]),
        ("bool", [True, False]),
        ("string", ["001", "003"]),
    ],
)
@pytest.mark.parametrize("with_null", [False, True])
@pytest.mark.parametrize("chunksize", [1, 10])
def test_csv_generate_tables_nullable_scalars(tmp_path, dtype, values, with_null, chunksize):
    values = [values[0], None, *values[1:]] if with_null else values
    # Keep another column populated so a missing scalar is not an empty CSV row.
    path = tmp_path / "nullable.csv"
    path.write_text("value,text\n" + "".join(f"{'' if value is None else value},row\n" for value in values))
    # Feature order can differ from the order in the CSV header.
    features = Features({"text": Value("string"), "value": Value(dtype)})
    csv = Csv(features=features, chunksize=chunksize)
    tables = [table for _, table in csv._generate_tables(base_files=[str(path)], files_iterables=[[str(path)]])]
    table = pa.concat_tables(tables)
    assert table.schema == features.arrow_schema
    assert table.to_pydict() == {"text": ["row"] * len(values), "value": values}
    assert table["value"].null_count == int(with_null)
    if chunksize == 1:
        assert all(batch.num_rows == 1 for batch in tables)


@pytest.mark.parametrize("chunksize", [1, 10])
def test_csv_generate_tables_nullable_scalars_parser_options(tmp_path, chunksize):
    path = tmp_path / "nullable.csv"
    path.write_text('integer,boolean,text\n"1,234",yes,NA\nMISSING,MISSING,001\n5,no,003\n')
    features = Features({"integer": Value("int64"), "boolean": Value("bool"), "text": Value("string")})
    csv = Csv(
        features=features,
        chunksize=chunksize,
        thousands=",",
        true_values=["yes"],
        false_values=["no"],
        keep_default_na=False,
        na_values=["MISSING"],
    )
    table = pa.concat_tables(
        [table for _, table in csv._generate_tables(base_files=[str(path)], files_iterables=[[str(path)]])]
    )
    assert table.schema == features.arrow_schema
    assert table.to_pydict() == {
        "integer": [1234, None, 5],
        "boolean": [True, None, False],
        "text": ["NA", "001", "003"],
    }


def test_csv_generate_tables_scalars_na_filter_disabled(tmp_path):
    path = tmp_path / "no_null.csv"
    path.write_text("integer,boolean,text\n9007199254740993,True,NA\n5,False,\n")
    features = Features({"integer": Value("int64"), "boolean": Value("bool"), "text": Value("string")})
    csv = Csv(features=features, na_filter=False)
    table = pa.concat_tables(
        [table for _, table in csv._generate_tables(base_files=[str(path)], files_iterables=[[str(path)]])]
    )
    assert table.schema == features.arrow_schema
    assert table.to_pydict() == {
        "integer": [9007199254740993, 5],
        "boolean": [True, False],
        "text": ["NA", ""],
    }


@pytest.mark.parametrize("dtype", ["string", "large_string"])
@pytest.mark.parametrize("engine", ["c", "python"])
@pytest.mark.parametrize("chunksize", [1, 10])
@pytest.mark.parametrize(
    "content, values, options",
    [
        ('"001",row\n"003",row\n', ["001", "003"], {}),
        ("01.20,row\n003.00,row\n", ["01.20", "003.00"], {}),
        ("1e3,row\n2e-2,row\n", ["1e3", "2e-2"], {}),
        ("001,row\n,row\nNA,row\n003,row\n", ["001", None, None, "003"], {}),
        (
            '001,row\n"",row\nNA,row\n003,row\n',
            ["001", "", "NA", "003"],
            {"keep_default_na": False},
        ),
        ("001,row\n,row\nNULL,row\n003,row\n", ["001", "", "NULL", "003"], {"na_filter": False}),
        (
            "001,row\nMISSING,row\n003,row\n",
            ["001", None, "003"],
            {"keep_default_na": False, "na_values": ["MISSING"]},
        ),
        ('"001",row\n"00,3",row\n"say ""hi""",row\n', ["001", "00,3", 'say "hi"'], {}),
    ],
    ids=[
        "leading-zeros",
        "decimals",
        "scientific",
        "default-na",
        "keep-default-na",
        "na-filter",
        "custom-na",
        "quotes",
    ],
)
def test_csv_generate_tables_declared_strings(tmp_path, dtype, engine, chunksize, content, values, options):
    path = tmp_path / "strings.csv"
    path.write_text("value,tag\n" + content)
    features = Features({"tag": Value("string"), "value": Value(dtype)})
    csv = Csv(features=features, engine=engine, chunksize=chunksize, **options)
    table = pa.concat_tables(
        [table for _, table in csv._generate_tables(base_files=[str(path)], files_iterables=[[str(path)]])]
    )
    assert table.schema == features.arrow_schema
    assert table.to_pydict() == {"tag": ["row"] * len(values), "value": values}
    assert table["value"].is_null().to_pylist() == [value is None for value in values]


@pytest.mark.parametrize("pandas_version", ["2.0.3", "2.1.4", "2.2.3"])
def test_csv_pd_read_csv_kwargs_keeps_new_1_3_0_params_on_pandas_2x(monkeypatch, pandas_version):
    # pandas 2.x supports encoding_errors / on_bad_lines (added in 1.3.0), so they must be
    # forwarded to pd.read_csv. Regression for the ">= 1.3" guard that compared major and minor
    # independently, wrongly dropping them on pandas 2.0-2.2 (minor 0/1/2 fails minor >= 3).
    monkeypatch.setattr(datasets.config, "PANDAS_VERSION", version.parse(pandas_version))
    kwargs = CsvConfig(encoding_errors="replace", on_bad_lines="skip").pd_read_csv_kwargs
    assert kwargs["encoding_errors"] == "replace"
    assert kwargs["on_bad_lines"] == "skip"


@pytest.mark.parametrize("pandas_version", ["1.1.5", "1.2.5"])
def test_csv_pd_read_csv_kwargs_drops_new_1_3_0_params_below_pandas_1_3(monkeypatch, pandas_version):
    # The other half of the invariant: pandas < 1.3 lacks these params, so they must still be dropped.
    monkeypatch.setattr(datasets.config, "PANDAS_VERSION", version.parse(pandas_version))
    kwargs = CsvConfig(encoding_errors="replace", on_bad_lines="skip").pd_read_csv_kwargs
    assert "encoding_errors" not in kwargs
    assert "on_bad_lines" not in kwargs


@pytest.mark.skipif(
    datasets.config.PANDAS_VERSION.release < (1, 3),
    reason="on_bad_lines requires pandas >= 1.3",
)
def test_csv_generate_tables_skips_malformed_row_with_on_bad_lines_skip(csv_file, malformed_csv_file):
    # End-to-end on the installed pandas: on_bad_lines="skip" must reach pd.read_csv, so the
    # malformed row is skipped instead of raising. On pandas 2.0-2.2 the buggy guard dropped it
    # and this raised "Error tokenizing data".
    csv = Csv(on_bad_lines="skip")
    base_files = [malformed_csv_file]
    files_iterables = [[file] for file in base_files]
    generator = csv._generate_tables(base_files=base_files, files_iterables=files_iterables)
    pa_table = pa.concat_tables([table for _, table in generator])
    assert pa_table.num_rows == 1
    assert pa_table.to_pydict() == {"header1": [1], "header2": [2]}
