import struct

import pyarrow as pa
import pytest

from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.arrow.arrow import Arrow, ArrowConfig


@pytest.fixture
def arrow_file_streaming_format(tmp_path):
    filename = tmp_path / "stream.arrow"
    testdata = [[1, 1, 1], [0, 100, 6], [1, 90, 900]]

    schema = pa.schema([pa.field("input_ids", pa.list_(pa.int32()))])
    array = pa.array(testdata, type=pa.list_(pa.int32()))
    table = pa.Table.from_arrays([array], schema=schema)
    with open(filename, "wb") as f:
        with pa.ipc.new_stream(f, schema) as writer:
            writer.write_table(table)
    return str(filename)


@pytest.fixture
def arrow_file_file_format(tmp_path):
    filename = tmp_path / "file.arrow"
    testdata = [[1, 1, 1], [0, 100, 6], [1, 90, 900]]

    schema = pa.schema([pa.field("input_ids", pa.list_(pa.int32()))])
    array = pa.array(testdata, type=pa.list_(pa.int32()))
    table = pa.Table.from_arrays([array], schema=schema)
    with open(filename, "wb") as f:
        with pa.ipc.new_file(f, schema) as writer:
            writer.write_table(table)
    return str(filename)


@pytest.fixture
def arrow_file_with_invalid_offsets(tmp_path):
    filename = tmp_path / "invalid-offsets.arrow"
    table = pa.table({"col": pa.array([b"A", b"B"])})
    with open(filename, "wb") as f:
        with pa.ipc.new_stream(f, table.schema) as writer:
            writer.write_table(table)

    payload = bytearray(filename.read_bytes())
    schema_message_start = payload.index(b"\xff\xff\xff\xff")
    schema_metadata_length = struct.unpack_from("<I", payload, schema_message_start + 4)[0]
    record_batch_start = (schema_message_start + 8 + schema_metadata_length + 7) & ~7
    record_batch_metadata_length = struct.unpack_from("<I", payload, record_batch_start + 4)[0]
    record_batch_body_start = (record_batch_start + 8 + record_batch_metadata_length + 7) & ~7

    assert struct.unpack_from("<iii", payload, record_batch_body_start) == (0, 1, 2)
    struct.pack_into("<iii", payload, record_batch_body_start, 0, 2, 1)
    filename.write_bytes(payload)
    return str(filename)


@pytest.mark.parametrize(
    "file_fixture, config_kwargs",
    [
        ("arrow_file_streaming_format", {}),
        ("arrow_file_file_format", {}),
    ],
)
def test_arrow_generate_tables(file_fixture, config_kwargs, request):
    arrow = Arrow(**config_kwargs)
    generator = arrow._generate_tables([request.getfixturevalue(file_fixture)])
    pa_table = pa.concat_tables([table for _, table in generator])

    expected = {"input_ids": [[1, 1, 1], [0, 100, 6], [1, 90, 900]]}
    assert pa_table.to_pydict() == expected


def test_arrow_generate_tables_rejects_invalid_record_batch(arrow_file_with_invalid_offsets):
    with open(arrow_file_with_invalid_offsets, "rb") as f:
        record_batch = pa.ipc.open_stream(f).read_next_batch()

    record_batch.validate()
    with pytest.raises(pa.ArrowInvalid):
        record_batch.validate(full=True)

    arrow = Arrow()
    with pytest.raises(pa.ArrowInvalid):
        next(arrow._generate_tables([arrow_file_with_invalid_offsets]))


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = ArrowConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = ArrowConfig(name="name", data_files=data_files)
