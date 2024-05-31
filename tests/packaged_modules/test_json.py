import textwrap

import pyarrow as pa
import pytest

from datasets import Features, Value
from datasets.packaged_modules.json.json import Json


@pytest.fixture
def jsonl_file(tmp_path):
    filename = tmp_path / "file.jsonl"
    data = textwrap.dedent(
        """\
        {"col_1": -1}
        {"col_1": 1, "col_2": 2}
        {"col_1": 10, "col_2": 20}
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def jsonl_file_utf16_encoded(tmp_path):
    filename = tmp_path / "file_utf16_encoded.jsonl"
    data = textwrap.dedent(
        """\
        {"col_1": -1}
        {"col_1": 1, "col_2": 2}
        {"col_1": 10, "col_2": 20}
        """
    )
    with open(filename, "w", encoding="utf-16") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def json_file_with_list_of_dicts(tmp_path):
    filename = tmp_path / "file_with_list_of_dicts.json"
    data = textwrap.dedent(
        """\
        [
            {"col_1": -1},
            {"col_1": 1, "col_2": 2},
            {"col_1": 10, "col_2": 20}
        ]
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def json_file_with_list_of_strings(tmp_path):
    filename = tmp_path / "file_with_list_of_strings.json"
    data = textwrap.dedent(
        """\
        [
            "First text.",
            "Second text.",
            "Third text."
        ]
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def json_file_with_list_of_dicts_field(tmp_path):
    filename = tmp_path / "file_with_list_of_dicts_field.json"
    data = textwrap.dedent(
        """\
        {
            "field1": 1,
            "field2": "aabb",
            "field3": [
                {"col_1": -1},
                {"col_1": 1, "col_2": 2},
                {"col_1": 10, "col_2": 20}
            ]
        }
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def json_file_with_list_of_strings_field(tmp_path):
    path = tmp_path / "file.json"
    data = textwrap.dedent(
        """\
        {
            "field1": 1,
            "field2": "aabb",
            "field3": [
                "First text.",
                "Second text.",
                "Third text."
            ]
        }
        """
    )
    with open(path, "w") as f:
        f.write(data)
    return str(path)


@pytest.fixture
def json_file_with_dict_of_lists_field(tmp_path):
    path = tmp_path / "file.json"
    data = textwrap.dedent(
        """\
        {
            "field1": 1,
            "field2": "aabb",
            "field3": {
                "col_1": [-1, 1, 10],
                "col_2": [null, 2, 20]
            }
        }
        """
    )
    with open(path, "w") as f:
        f.write(data)
    return str(path)


@pytest.fixture
def json_file_with_list_of_dicts_with_sorted_columns(tmp_path):
    path = tmp_path / "file.json"
    data = textwrap.dedent(
        """\
        [
            {"ID": 0, "Language": "Language-0", "Topic": "Topic-0"},
            {"ID": 1, "Language": "Language-1", "Topic": "Topic-1"},
            {"ID": 2, "Language": "Language-2", "Topic": "Topic-2"}
        ]
        """
    )
    with open(path, "w") as f:
        f.write(data)
    return str(path)


@pytest.fixture
def json_file_with_list_of_dicts_with_sorted_columns_field(tmp_path):
    path = tmp_path / "file.json"
    data = textwrap.dedent(
        """\
        {
            "field1": 1,
            "field2": "aabb",
            "field3": [
                {"ID": 0, "Language": "Language-0", "Topic": "Topic-0"},
                {"ID": 1, "Language": "Language-1", "Topic": "Topic-1"},
                {"ID": 2, "Language": "Language-2", "Topic": "Topic-2"}
            ]
        }
        """
    )
    with open(path, "w") as f:
        f.write(data)
    return str(path)


@pytest.mark.parametrize(
    "file_fixture, config_kwargs",
    [
        ("jsonl_file", {}),
        ("jsonl_file_utf16_encoded", {"encoding": "utf-16"}),
        ("json_file_with_list_of_dicts", {}),
        ("json_file_with_list_of_dicts_field", {"field": "field3"}),
        ("json_file_with_list_of_strings", {}),
        ("json_file_with_list_of_strings_field", {"field": "field3"}),
        ("json_file_with_dict_of_lists_field", {"field": "field3"}),
    ],
)
def test_json_generate_tables(file_fixture, config_kwargs, request):
    json = Json(**config_kwargs)
    generator = json._generate_tables([[request.getfixturevalue(file_fixture)]])
    pa_table = pa.concat_tables([table for _, table in generator])
    if "list_of_strings" in file_fixture:
        expected = {"text": ["First text.", "Second text.", "Third text."]}
    else:
        expected = {"col_1": [-1, 1, 10], "col_2": [None, 2, 20]}
    assert pa_table.to_pydict() == expected


@pytest.mark.parametrize(
    "file_fixture, config_kwargs",
    [
        (
            "jsonl_file",
            {"features": Features({"col_1": Value("int64"), "col_2": Value("int64"), "missing_col": Value("string")})},
        ),
        (
            "json_file_with_list_of_dicts",
            {"features": Features({"col_1": Value("int64"), "col_2": Value("int64"), "missing_col": Value("string")})},
        ),
        (
            "json_file_with_list_of_dicts_field",
            {
                "field": "field3",
                "features": Features(
                    {"col_1": Value("int64"), "col_2": Value("int64"), "missing_col": Value("string")}
                ),
            },
        ),
    ],
)
def test_json_generate_tables_with_missing_features(file_fixture, config_kwargs, request):
    json = Json(**config_kwargs)
    generator = json._generate_tables([[request.getfixturevalue(file_fixture)]])
    pa_table = pa.concat_tables([table for _, table in generator])
    assert pa_table.to_pydict() == {"col_1": [-1, 1, 10], "col_2": [None, 2, 20], "missing_col": [None, None, None]}


@pytest.mark.parametrize(
    "file_fixture, config_kwargs",
    [
        ("json_file_with_list_of_dicts_with_sorted_columns", {}),
        ("json_file_with_list_of_dicts_with_sorted_columns_field", {"field": "field3"}),
    ],
)
def test_json_generate_tables_with_sorted_columns(file_fixture, config_kwargs, request):
    builder = Json(**config_kwargs)
    generator = builder._generate_tables([[request.getfixturevalue(file_fixture)]])
    pa_table = pa.concat_tables([table for _, table in generator])
    assert pa_table.column_names == ["ID", "Language", "Topic"]
