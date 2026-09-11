import io
import json
import textwrap
from datetime import datetime
from unittest.mock import Mock, patch

import pandas as pd
import pyarrow as pa
import pyarrow.json as paj
import pytest

from datasets import Features, List, Value, load_dataset
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.json.json import AGENT_TRACES_FEATURES, Json, JsonConfig

from ..utils import require_teich


def _pyarrow_has_invalid_list_offsets():
    data = b'{"a":[1]}\n{"a":[null,2]}\n'
    table = paj.read_json(io.BytesIO(data), read_options=paj.ReadOptions(block_size=len(data.splitlines()[1])))
    try:
        table.validate(full=True)
    except pa.ArrowInvalid:
        return True
    return False


@pytest.fixture
def json_file(tmp_path):
    filename = tmp_path / "file.json"
    data = textwrap.dedent(
        """\
        {
            "col_1": 1,
            "col_2": 2
        }
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


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


# ndjson format is no longer maintained (see: https://github.com/ndjson/ndjson-spec/issues/35#issuecomment-1285673417)
@pytest.fixture
def ndjson_file(tmp_path):
    filename = tmp_path / "file.ndjson"
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


@pytest.fixture
def jsonl_file_with_mix_of_str_and_int(tmp_path):
    filename = tmp_path / "file.jsonl"
    data = textwrap.dedent(
        """\
        {"col_1": -1}
        {"col_1": 1}
        {"col_1": "foo"}
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def jsonl_file_with_dicts_of_varying_keys(tmp_path):
    filename = tmp_path / "file.jsonl"
    data = textwrap.dedent(
        """\
        {"col_1": {"a": 0}}
        {"col_1": {"b": 0}}
        {"col_1": {"c": 0}}
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def jsonl_file_with_lists_of_dicts_of_varying_keys(tmp_path):
    filename = tmp_path / "file.jsonl"
    data = textwrap.dedent(
        """\
        {"col_1": [{"a": 0}, {"b": 0}]}
        {"col_1": [{"c": 0}, {"d": 0}]}
        """
    )
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def jsonl_file_with_lists_of_dicts_of_varying_keys_and_bom(tmp_path):
    # Same content as jsonl_file_with_lists_of_dicts_of_varying_keys, but the file
    # starts with a UTF-8 BOM (written via the utf-8-sig codec).
    filename = tmp_path / "file_with_bom.jsonl"
    data = textwrap.dedent(
        """\
        {"col_1": [{"a": 0}, {"b": 0}]}
        {"col_1": [{"c": 0}, {"d": 0}]}
        """
    )
    with open(filename, "w", encoding="utf-8-sig") as f:
        f.write(data)
    return str(filename)


_messages = [
    {"role": "user", "content": "Turn on the living room lights and play my electronic music playlist."},
    {
        "role": "assistant",
        "tool_calls": [
            {
                "type": "function",
                "function": {"name": "control_light", "arguments": {"room": "living room", "state": "on"}},
            },
            {
                "type": "function",
                "function": {
                    "name": "play_music",
                    "arguments": {
                        "playlist": "electronic"
                    },  # mixed-type here since keys ["playlist"] and ["room", "state"] are different
                },
            },
        ],
    },
    {"role": "tool", "name": "control_light", "content": "The lights in the living room are now on."},
    {"role": "tool", "name": "play_music", "content": "The music is now playing."},
    {"role": "assistant", "content": "Done!"},
]

EXPECTED_ONE = {"col_1": [1], "col_2": [2]}
EXPECTED_THREE = {"col_1": [-1, 1, 10], "col_2": [None, 2, 20]}
EXPECTED_LIST_OF_STRINGS = {"text": ["First text.", "Second text.", "Third text."]}
EXPECTED_MIX = {"col_1": [-1, 1, "foo"]}
EXPECTED_DICTS_WITH_VARYING_KEYS = {"col_1": [{"a": 0}, {"b": 0}, {"c": 0}]}
EXPECTED_LISTS_OF_DICTS_WITH_VARYING_KEYS = {"col_1": [[{"a": 0}, {"b": 0}], [{"c": 0}, {"d": 0}]]}
EXPECTED_MESSAGES = {"messages": [_messages]}


@pytest.fixture
def jsonl_file_with_messages(tmp_path):
    filename = tmp_path / "file.jsonl"
    data = json.dumps({"messages": _messages})
    with open(filename, "w") as f:
        f.write(data)
    return str(filename)


def write_jsonl(path, rows):
    with open(path, "w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")
    return str(path)


def generate_agent_traces_output(trace_file):
    json_builder = Json(features=AGENT_TRACES_FEATURES)
    base_files = [trace_file]
    files_iterables = [[trace_file]]
    original_files = list(base_files)
    generator = json_builder._generate_tables(
        base_files=base_files, files_iterables=files_iterables, original_files=original_files
    )
    pa_table = pa.concat_tables([table for _, table in generator])
    return Features.from_arrow_schema(pa_table.schema).decode_batch(pa_table.to_pydict())


def assert_agent_traces_output(tmp_path, filename, rows, expected, num_sessions=1):
    trace_file = write_jsonl(tmp_path / filename, rows)
    out = generate_agent_traces_output(trace_file)
    for key, value in zip(AGENT_TRACE_FIELD_NAMES_TO_CHECK, expected):
        assert out[key] == [value] * num_sessions
    assert out["file_path"] == [trace_file] * num_sessions
    assert isinstance(out["messages"], list)
    assert out["messages"]
    assert all(
        isinstance(message["role"], str) and isinstance(message["content"], str)
        for messages in out["messages"]
        for message in messages
    )
    assert isinstance(out["tools"], list)
    assert isinstance(out["metadata"], (dict, list))
    assert isinstance(out["trace"], (dict, list))
    return trace_file, out


AGENT_TRACE_FIELD_NAMES_TO_CHECK = (
    "harness",
    "session_id",
    "prompt",
    "sent_at",
    "num_user_messages",
    "num_tool_calls",
)
CODEX_AGENT_TRACE_ROWS = [
    {"type": "session_meta", "payload": {"id": "codex-session"}},
    {
        "type": "response_item",
        "payload": {
            "type": "message",
            "role": "user",
            "content": [{"type": "input_text", "text": "context-wrapped codex prompt"}],
        },
    },
    {
        "type": "response_item",
        "payload": {
            "type": "message",
            "role": "user",
            "content": [{"type": "input_text", "text": "actual codex prompt"}],
        },
    },
    {
        "timestamp": "2026-04-01T10:01:00.000Z",
        "type": "event_msg",
        "payload": {"type": "user_message", "message": "actual codex prompt"},
    },
    {
        "type": "response_item",
        "payload": {"type": "function_call", "name": "exec_command", "call_id": "call_1"},
    },
    {
        "type": "response_item",
        "payload": {"type": "function_call_output", "call_id": "call_1", "output": "done"},
    },
]
CODEX_EXPECTED_AGENT_TRACE_FIELDS = (
    "codex",
    "codex-session",
    "actual codex prompt",
    "2026-04-01T10:01:00.000Z",
    1,
    1,
)

HERMES_SESSION = {
    "id": "20260605_092247_d018ec",
    "source": "cli",
    "model": "Qwen/Qwen3.5-35B-A3B",
    "system_prompt": "You are Hermes.",
    "started_at": 1_780_665_768.307,
    "message_count": 4,
    "tool_call_count": 1,
    "messages": [
        {
            "session_id": "20260605_092247_d018ec",
            "role": "user",
            "content": "Run pwd and date.",
            "timestamp": 1_780_665_767.307,
        },
        {
            "session_id": "20260605_092247_d018ec",
            "role": "assistant",
            "content": "",
            "reasoning_content": "The user asked for two shell commands.",
            "timestamp": 1_780_665_767.308,
            "tool_calls": [
                {
                    "id": "call_677f321e2b3047b4b8c7a1e1",
                    "type": "function",
                    "function": {
                        "name": "terminal",
                        "arguments": json.dumps({"command": "pwd && date -u +%Y-%m-%dT%H:%M:%SZ"}),
                    },
                },
            ],
        },
        {
            "session_id": "20260605_092247_d018ec",
            "role": "tool",
            "content": json.dumps({"output": "/tmp/work\n2026-06-05T13:22:47Z", "exit_code": 0, "error": None}),
            "tool_call_id": "call_677f321e2b3047b4b8c7a1e1",
            "timestamp": 1_780_665_767.309,
        },
        {
            "session_id": "20260605_092247_d018ec",
            "role": "assistant",
            "content": "Working directory: `/tmp/work`.",
            "reasoning": "The commands executed successfully.",
            "timestamp": 1_780_665_767.31,
        },
    ],
}


DROID_SESSION = [
    {
        "type": "session_start",
        "id": "droid-session",
        "title": "inspect the project",
        "sessionTitle": "Inspect project files",
        "owner": "caleb",
        "version": 2,
        "cwd": "/workspace/project",
    },
    {
        "type": "message",
        "id": "context-1",
        "timestamp": "2026-06-02T18:55:29.000Z",
        "message": {
            "role": "user",
            "visibility": "llm_only",
            "content": [{"type": "text", "text": "<system-reminder>injected context</system-reminder>"}],
        },
        "parentId": None,
    },
    {
        "type": "message",
        "id": "message-1",
        "timestamp": "2026-06-02T18:55:30.274Z",
        "message": {
            "role": "user",
            "content": [{"type": "text", "text": "Inspect the project"}],
        },
        "parentId": "context-1",
    },
    {
        "type": "message",
        "id": "message-2",
        "timestamp": "2026-06-02T18:55:35.000Z",
        "message": {
            "role": "assistant",
            "content": [
                {
                    "type": "thinking",
                    "thinking": "I should list the files first.",
                    "signature": "reasoning_content",
                    "signatureProvider": "generic-chat-completion-api",
                    "durationMs": 1200,
                },
                {"type": "text", "text": "I'll list the files."},
                {"type": "tool_use", "id": "LS_0", "name": "LS", "input": {"directory_path": "/workspace/project"}},
            ],
            "chatCompletionReasoningField": "reasoning_content",
            "chatCompletionReasoningContent": "I should list the files first.",
        },
        "parentId": "message-1",
    },
    {
        "type": "message",
        "id": "message-3",
        "timestamp": "2026-06-02T18:55:36.000Z",
        "message": {
            "role": "user",
            "content": [
                {"type": "tool_result", "tool_use_id": "LS_0", "is_error": False, "content": "README.md\nsrc"},
            ],
        },
        "parentId": "message-2",
    },
]


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = JsonConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = JsonConfig(name="name", data_files=data_files)


@pytest.mark.parametrize(
    "file_fixture, config_kwargs, expected",
    [
        ("json_file", {}, EXPECTED_ONE),
        ("jsonl_file", {}, EXPECTED_THREE),
        ("ndjson_file", {}, EXPECTED_THREE),
        ("jsonl_file_utf16_encoded", {"encoding": "utf-16"}, EXPECTED_THREE),
        ("json_file_with_list_of_dicts", {}, EXPECTED_THREE),
        ("json_file_with_list_of_dicts_field", {"field": "field3"}, EXPECTED_THREE),
        ("json_file_with_list_of_strings", {}, EXPECTED_LIST_OF_STRINGS),
        ("json_file_with_list_of_strings_field", {"field": "field3"}, EXPECTED_LIST_OF_STRINGS),
        ("json_file_with_dict_of_lists_field", {"field": "field3"}, EXPECTED_THREE),
        ("jsonl_file_with_mix_of_str_and_int", {}, EXPECTED_MIX),
        ("jsonl_file_with_dicts_of_varying_keys", {}, EXPECTED_DICTS_WITH_VARYING_KEYS),
        ("jsonl_file_with_lists_of_dicts_of_varying_keys", {}, EXPECTED_LISTS_OF_DICTS_WITH_VARYING_KEYS),
        (
            "jsonl_file_with_lists_of_dicts_of_varying_keys_and_bom",
            {},
            EXPECTED_LISTS_OF_DICTS_WITH_VARYING_KEYS,
        ),
        ("jsonl_file_with_messages", {}, EXPECTED_MESSAGES),
    ],
)
def test_json_generate_tables(file_fixture, config_kwargs, expected, request):
    json = Json(**config_kwargs)
    base_files = [request.getfixturevalue(file_fixture)]
    files_iterables = [[file] for file in base_files]
    original_files = list(base_files)
    generator = json._generate_tables(
        base_files=base_files, files_iterables=files_iterables, original_files=original_files
    )
    pa_table = pa.concat_tables([table for _, table in generator])
    out = Features.from_arrow_schema(pa_table.schema).decode_batch(pa_table.to_pydict())
    assert out == expected


@pytest.mark.parametrize("allow_full_read", [False, True])
@pytest.mark.parametrize("value", [[None, 1], [None, {"label": "en", "prob": 0.5}]])
def test_json_invalid_list_offsets(tmp_path, allow_full_read, value):
    rows = [{"a": value}]
    path = write_jsonl(tmp_path / "file.jsonl", rows)
    builder = Json()
    tables = []
    for _, table in builder._generate_tables([path], [[path]], [path], allow_full_read=allow_full_read):
        table.validate(full=True)
        tables.append(table)
    assert pa.concat_tables(tables).combine_chunks().to_pylist() == rows


@pytest.mark.parametrize("chunksize", [64 << 10, (16 << 10) - 1])
def test_json_invalid_list_offsets_multiple_blocks(tmp_path, chunksize):
    rows = [
        {"id": 0, "meta": {"line_identifications": [{"label": "en", "prob": 1.0}]}},
        {"id": 1, "meta": {"line_identifications": [None, {"label": "en", "prob": 0.5}]}},
    ]
    path = tmp_path / "file.jsonl"
    # Place each record in its own Arrow block. The second block infers the
    # list's value type after its leading null, even though the first is typed.
    path.write_text("".join(json.dumps(row).ljust((16 << 10) - 1) + "\n" for row in rows))
    path = str(path)
    builder = Json(chunksize=chunksize)
    tables = []
    for _, table in builder._generate_tables([path], [[path]], [path]):
        table.validate(full=True)
        tables.append(table)
    assert pa.concat_tables(tables).combine_chunks().to_pylist() == rows


@pytest.mark.skipif(not _pyarrow_has_invalid_list_offsets(), reason="PyArrow produces valid list offsets")
@pytest.mark.parametrize("retry", ["single_block", "explicit_schema", "pandas"])
@pytest.mark.parametrize("allow_full_read", [False, True])
def test_json_invalid_list_offsets_batch_retry(tmp_path, retry, allow_full_read):
    rows = [{"a": [i]} for i in range(6)]
    rows[3]["a"].insert(0, None)
    if retry != "single_block":
        # A leading null in the first record also breaks single-block inference.
        rows[2]["a"].insert(0, None)
    # Two Arrow blocks per batch: only the second batch has leading nulls.
    block_size = 16 << 10
    lines = [(json.dumps(row).ljust(block_size - 1) + "\n").encode() for row in rows]
    batches = [b"".join(lines[i : i + 2]) for i in range(0, len(lines), 2)]
    path = tmp_path / "file.jsonl"
    path.write_bytes(b"".join(batches))
    path = str(path)
    builder = Json(chunksize=len(batches[0]) - 1)
    if retry == "explicit_schema":
        # Features may have been inferred by _split_generators, not configured.
        builder.info.features = Features({"a": List(Value("int64"))})
    with open(path, "rb") as f:
        original_read = f.read

        def bounded_read(size=-1):
            assert size >= 0, "Unbounded file read after a valid first batch"
            return original_read(size)

        with (
            patch("datasets.packaged_modules.json.json.open", return_value=f) as open_file,
            patch.object(f, "read", side_effect=bounded_read) as read,
            patch.object(paj, "read_json", wraps=paj.read_json) as read_json,
            patch("datasets.packaged_modules.json.json.pd.DataFrame", wraps=pd.DataFrame) as dataframe,
        ):
            generator = builder._generate_tables([path], [[path]], [path], allow_full_read=allow_full_read)
            tables = []
            for _, table in generator:
                table.validate(full=True)
                tables.append(table)
    assert pa.concat_tables(tables).combine_chunks().to_pylist() == rows
    assert open_file.call_count == 1
    assert all(call.args == (builder.config.chunksize,) for call in read.call_args_list)
    assert [call.args[0].getvalue() for call in read_json.call_args_list] == [
        batches[0],
        batches[1],
        batches[1],
        batches[2],
    ]
    retry_options = read_json.call_args_list[2].kwargs
    assert retry_options["read_options"].block_size == len(batches[1])
    if retry == "explicit_schema":
        assert retry_options["parse_options"].explicit_schema == builder.info.features.arrow_schema
    if retry == "pandas":
        dataframe.assert_called_once()
    else:
        dataframe.assert_not_called()


def test_json_invalid_table_warning(tmp_path):
    rows = [{"a": [1]}]
    path = write_jsonl(tmp_path / "file.jsonl", rows)
    valid_table = pa.Table.from_pylist(rows)
    invalid_table = Mock(wraps=valid_table)
    error = pa.ArrowInvalid("synthetic validity bitmap error")
    invalid_table.validate.side_effect = error
    builder = Json()
    with (
        patch.object(paj, "read_json", side_effect=[invalid_table, valid_table]),
        patch("datasets.packaged_modules.json.json.logger.warning") as warning,
    ):
        tables = list(builder._generate_tables([path], [[path]], [path]))
    assert pa.concat_tables([table for _, table in tables]).to_pylist() == rows
    message = warning.call_args.args[0]
    assert "failed Arrow validation" in message
    assert str(error) in message
    assert "known cause of invalid list offsets" in message
    assert "#5531" in message


def test_json_valid_file_no_reread(jsonl_file):
    builder = Json()
    with patch.object(paj, "read_json", wraps=paj.read_json) as read_json:
        tables = list(builder._generate_tables([jsonl_file], [[jsonl_file]], [jsonl_file]))
    assert read_json.call_count == 1
    assert pa.concat_tables([table for _, table in tables]).to_pydict() == EXPECTED_THREE


@pytest.mark.parametrize("chunksize", [5, 64 << 10])
@pytest.mark.parametrize("dtype", ["int64", "float16"])
def test_json_invalid_list_offsets_with_features(tmp_path, chunksize, dtype):
    rows = [{"a": []}, {"a": [None, 1]}]
    path = write_jsonl(tmp_path / "file.jsonl", rows)
    builder = Json(chunksize=chunksize, features=Features({"a": List(Value(dtype))}))
    tables = []
    for _, table in builder._generate_tables([path], [[path]], [path]):
        table.validate(full=True)
        tables.append(table)
    assert pa.concat_tables(tables).combine_chunks().to_pylist() == rows


@pytest.mark.parametrize("encoding", ["utf-8-sig", "utf-16"])
def test_json_invalid_list_offsets_encoding(tmp_path, encoding):
    path = tmp_path / "file.jsonl"
    path.write_text('{"a":[null,1],"text":"caf\u00e9"}\n', encoding=encoding)
    path = str(path)
    tables = list(Json(encoding=encoding)._generate_tables([path], [[path]], [path]))
    table = pa.concat_tables([table for _, table in tables])
    table.validate(full=True)
    assert table.to_pylist() == [{"a": [None, 1], "text": "caf\u00e9"}]


@pytest.mark.parametrize("value", [1e-320, -1e-320, 5e-324, 0.12345678901234568])
def test_json_invalid_list_offsets_preserve_floats(tmp_path, value):
    rows = [{"a": [None, 1], "x": value}]
    path = write_jsonl(tmp_path / "file.jsonl", rows)
    tables = list(Json()._generate_tables([path], [[path]], [path], allow_full_read=False))
    table = pa.concat_tables([table for _, table in tables])
    table.validate(full=True)
    assert table.to_pylist() == rows


@pytest.mark.parametrize("encoding_errors, expected", [("replace", "caf\ufffd"), ("ignore", "caf")])
def test_json_invalid_list_offsets_encoding_errors(tmp_path, encoding_errors, expected):
    path = tmp_path / "file.jsonl"
    path.write_bytes(b'{"a":[null,1],"text":"caf\xff"}\n')
    path = str(path)
    builder = Json(encoding_errors=encoding_errors)
    tables = list(builder._generate_tables([path], [[path]], [path], allow_full_read=False))
    table = pa.concat_tables([table for _, table in tables])
    table.validate(full=True)
    assert table.to_pylist() == [{"a": [None, 1], "text": expected}]


@pytest.mark.parametrize("chunksize", [1, 64 << 10])
@pytest.mark.parametrize("offset, hour", [("", 12), ("Z", 12), ("+00:00", 12), ("+01:00", 11)])
def test_json_invalid_list_offsets_timestamp_schema(tmp_path, chunksize, offset, hour):
    rows = [
        {"a": [None, 1], "ts": f"2026-01-01T12:34:56{offset}"},
        {"a": [2], "ts": "2026-01-02T12:34:56"},
    ]
    path = write_jsonl(tmp_path / "file.jsonl", rows)
    dataset = load_dataset(
        "json", data_files=path, split="train", chunksize=chunksize, cache_dir=str(tmp_path / "cache")
    )
    assert dataset.to_list() == [
        {"a": [None, 1], "ts": datetime(2026, 1, 1, hour, 34, 56)},
        {"a": [2], "ts": datetime(2026, 1, 2, 12, 34, 56)},
    ]
    assert dataset.features["ts"] == Value("timestamp[s]")


@pytest.mark.parametrize("encoding_errors, expected", [("replace", "caf\ufffd"), ("ignore", "caf")])
def test_json_invalid_list_offsets_nested_timestamp_encoding_errors(tmp_path, encoding_errors, expected):
    path = tmp_path / "file.jsonl"
    path.write_bytes(b'{"a":[null,{"ts":"2026-01-01T12:34:56+01:00","caf\xff":1}],"text":"caf\xff"}\n')
    path = str(path)
    builder = Json(encoding_errors=encoding_errors)
    tables = list(builder._generate_tables([path], [[path]], [path], allow_full_read=False))
    table = pa.concat_tables([table for _, table in tables])
    table.validate(full=True)
    assert table.to_pylist() == [
        {"a": [None, {"ts": datetime(2026, 1, 1, 11, 34, 56), expected: 1}], "text": expected}
    ]


@pytest.mark.parametrize("chunksize", [1, 2, 3, 64 << 10])
def test_json_invalid_list_offsets_utf8_bom(tmp_path, chunksize):
    path = tmp_path / "file.jsonl"
    path.write_text('{"a":[null,1]}\n', encoding="utf-8-sig")
    dataset = load_dataset(
        "json", data_files=str(path), split="train", chunksize=chunksize, cache_dir=str(tmp_path / "cache")
    )
    assert dataset.to_list() == [{"a": [None, 1]}]


@pytest.mark.parametrize("encoding", ["utf-8", "utf-8-sig", "utf-16"])
def test_json_full_file_fallback_bom(tmp_path, encoding):
    path = tmp_path / "file.json"
    # Leading whitespace bypasses JSON array normalization, reaching the
    # pre-existing whole-file pandas fallback even with a complete BOM.
    path.write_text(' [{"a":[null,1]}]\n', encoding="utf-8-sig" if encoding == "utf-8" else encoding)
    path = str(path)
    builder = Json(encoding=encoding, on_mixed_types=None)
    tables = list(builder._generate_tables([path], [[path]], [path]))
    table = pa.concat_tables([table for _, table in tables])
    table.validate(full=True)
    assert table.to_pylist() == [{"a": [None, 1]}]


@pytest.mark.parametrize("chunksize", [5, 64 << 10])
@pytest.mark.parametrize("use_features", [False, True])
def test_json_invalid_list_offsets_preserve_values(tmp_path, chunksize, use_features):
    rows = [
        {"a": [], "id": None, "timestamp": 1690000000000},
        {"a": [None, 1], "id": 9007199254740993, "timestamp": 1690000000001},
    ]
    path = write_jsonl(tmp_path / "file.jsonl", rows)
    features = Features({"a": List(Value("int64")), "id": Value("int64"), "timestamp": Value("int64")})
    builder = Json(chunksize=chunksize, features=features if use_features else None)
    tables = list(builder._generate_tables([path], [[path]], [path]))
    table = pa.concat_tables([table for _, table in tables], promote_options="default")
    table.validate(full=True)
    assert table.to_pylist() == rows


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
    base_files = [request.getfixturevalue(file_fixture)]
    files_iterables = [[file] for file in base_files]
    original_files = list(base_files)
    generator = json._generate_tables(
        base_files=base_files, files_iterables=files_iterables, original_files=original_files
    )
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
    json = Json(**config_kwargs)
    base_files = [request.getfixturevalue(file_fixture)]
    files_iterables = [[file] for file in base_files]
    original_files = list(base_files)
    generator = json._generate_tables(
        base_files=base_files, files_iterables=files_iterables, original_files=original_files
    )
    pa_table = pa.concat_tables([table for _, table in generator])
    assert pa_table.column_names == ["ID", "Language", "Topic"]


@pytest.mark.parametrize(
    "filename, rows, expected",
    [
        pytest.param("codex.jsonl", CODEX_AGENT_TRACE_ROWS, CODEX_EXPECTED_AGENT_TRACE_FIELDS, id="codex"),
        pytest.param(
            "codex_response_item_only.jsonl",
            [
                {"type": "session_meta", "payload": {"id": "codex-session"}},
                {
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [{"text": "codex response item prompt"}],
                    },
                },
                {
                    "type": "response_item",
                    "payload": {"type": "function_call", "name": "exec_command", "call_id": "call_1"},
                },
            ],
            ("codex", "codex-session", None, None, 0, 1),
            id="codex-response-item-only",
        ),
        pytest.param(
            "claude.jsonl",
            [
                {
                    "timestamp": "2026-04-02T10:00:00.000Z",
                    "type": "user",
                    "sessionId": "claude-session",
                    "message": {"role": "user", "content": "claude prompt"},
                },
                {
                    "type": "assistant",
                    "sessionId": "claude-session",
                    "message": {
                        "role": "assistant",
                        "content": [{"type": "tool_use", "id": "toolu_1"}, {"type": "tool_use", "id": "toolu_2"}],
                    },
                },
                {
                    "type": "user",
                    "sessionId": "claude-session",
                    "message": {"role": "user", "content": [{"type": "tool_result", "content": "done"}]},
                },
            ],
            ("claude_code", "claude-session", "claude prompt", "2026-04-02T10:00:00.000Z", 1, 2),
            id="claude",
        ),
        pytest.param(
            "pi.jsonl",
            [
                {"type": "session", "id": "pi-session"},
                {
                    "timestamp": "2026-04-03T10:01:00.000Z",
                    "type": "message",
                    "message": {"role": "user", "content": "pi prompt"},
                },
                {
                    "type": "message",
                    "message": {
                        "role": "assistant",
                        "content": [{"type": "toolCall", "id": "call_1"}, {"type": "toolCall", "id": "call_2"}],
                    },
                },
                {
                    "type": "message",
                    "message": {"role": "toolResult", "content": [{"type": "text", "text": "done"}]},
                },
                {
                    "type": "message",
                    "message": {"role": "user", "content": [{"type": "text", "text": "second pi prompt"}]},
                },
            ],
            ("pi", "pi-session", "pi prompt", "2026-04-03T10:01:00.000Z", 2, 2),
            id="pi",
        ),
        pytest.param(
            "openclaw.jsonl",
            [
                {
                    "type": "session",
                    "id": "openclaw-session",
                    "cwd": "/Users/test/.openclaw/agents/main",
                },
                {
                    "timestamp": "2026-04-03T10:01:00.000Z",
                    "type": "message",
                    "message": {"role": "user", "content": "openclaw prompt"},
                },
            ],
            ("openclaw", "openclaw-session", "openclaw prompt", "2026-04-03T10:01:00.000Z", 1, 0),
            id="openclaw",
        ),
        pytest.param(
            "hermes.jsonl",
            [HERMES_SESSION],
            ("hermes", "20260605_092247_d018ec", "Run pwd and date.", "2026-06-05T13:22:48.307Z", 1, 1),
        ),
        pytest.param(
            "hermes_two_sessions.jsonl",
            [HERMES_SESSION] * 2,
            ("hermes", "20260605_092247_d018ec", "Run pwd and date.", "2026-06-05T13:22:48.307Z", 1, 1),
        ),
        pytest.param(
            "droid.jsonl",
            DROID_SESSION,
            ("droid", "droid-session", "Inspect the project", "2026-06-02T18:55:30.274Z", 1, 1),
            id="droid",
        ),
        pytest.param(
            "missing_prompt.jsonl",
            [
                {"type": "session_meta", "payload": {"id": "codex-session"}},
                {
                    "type": "response_item",
                    "payload": {"type": "message", "role": "assistant", "content": [{"text": "assistant response"}]},
                },
            ],
            ("codex", "codex-session", None, None, 0, 0),
            id="missing-prompt",
        ),
    ],
)
@require_teich
def test_json_generate_tables_with_agent_trace_metadata(tmp_path, filename, rows, expected):
    num_sessions = 2 if filename == "hermes_two_sessions.jsonl" else 1
    _, out = assert_agent_traces_output(tmp_path, filename, rows, expected, num_sessions=num_sessions)
    if filename == "droid.jsonl":
        assert out["metadata"][0]["trace_type"] == "droid"
    assert "models" not in out


@require_teich
@pytest.mark.parametrize(
    "filename, rows, expected",
    [
        pytest.param("codex.jsonl", CODEX_AGENT_TRACE_ROWS, CODEX_EXPECTED_AGENT_TRACE_FIELDS, id="codex"),
        pytest.param(
            "droid.jsonl",
            DROID_SESSION,
            ("droid", "droid-session", "Inspect the project", "2026-06-02T18:55:30.274Z", 1, 1),
            id="droid",
        ),
    ],
)
def test_json_load_dataset_with_agent_trace_metadata(tmp_path, filename, rows, expected):
    trace_file = write_jsonl(tmp_path / filename, rows)

    dataset = load_dataset("json", data_files=trace_file, split="train", cache_dir=str(tmp_path / "cache"))
    row = dataset[0]

    assert dataset.column_names == [
        "harness",
        "session_id",
        "prompt",
        "messages",
        "tools",
        "metadata",
        "sent_at",
        "num_user_messages",
        "num_tool_calls",
        "trace",
        "file_path",
    ]
    for key, value in zip(AGENT_TRACE_FIELD_NAMES_TO_CHECK, expected):
        assert row[key] == value, key
    if filename == "droid.jsonl":
        assert row["metadata"]["trace_type"] == "droid"
        assert json.loads(row["trace"].splitlines()[0])["type"] == "session_start"


def test_json_load_dataset_without_droid_marker_stays_ordinary_json(tmp_path):
    trace_file = write_jsonl(
        tmp_path / "droid_missing_marker.jsonl",
        [
            {"type": "session_start", "id": "droid-session", "version": 2},
            {
                "type": "message",
                "id": "message-1",
                "timestamp": "2026-06-02T18:55:30.274Z",
                "message": {"role": "user", "content": [{"type": "text", "text": "Inspect the project"}]},
            },
        ],
    )

    dataset = load_dataset("json", data_files=trace_file, split="train", cache_dir=str(tmp_path / "cache"))

    assert dataset.column_names == ["type", "id", "version", "timestamp", "message"]
    assert dataset[0]["type"] == "session_start"
