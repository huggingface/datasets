import pickle
from typing import List, Union

import numpy as np
import pyarrow as pa
import pytest

from datasets.table import (
    ConcatenationTable,
    InMemoryTable,
    MemoryMappedTable,
    Table,
    TableBlock,
    _in_memory_arrow_table_from_buffer,
    _in_memory_arrow_table_from_file,
    _interpolation_search,
    _memory_mapped_arrow_table_from_file,
    concat_tables,
    inject_arrow_table_documentation,
)

from .utils import assert_arrow_memory_doesnt_increase, assert_arrow_memory_increases, slow


@pytest.fixture(scope="session")
def in_memory_pa_table(arrow_file) -> pa.Table:
    return pa.ipc.open_stream(arrow_file).read_all()


def _to_testing_blocks(table: TableBlock) -> List[List[TableBlock]]:
    assert len(table) > 2
    blocks = [
        [table.slice(0, 2)],
        [table.slice(2).drop([c for c in table.column_names if c != "tokens"]), table.slice(2).drop(["tokens"])],
    ]
    return blocks


@pytest.fixture(scope="session")
def in_memory_blocks(in_memory_pa_table):
    table = InMemoryTable(in_memory_pa_table)
    return _to_testing_blocks(table)


@pytest.fixture(scope="session")
def memory_mapped_blocks(arrow_file):
    table = MemoryMappedTable.from_file(arrow_file)
    return _to_testing_blocks(table)


@pytest.fixture(scope="session")
def mixed_in_memory_and_memory_mapped_blocks(in_memory_blocks, memory_mapped_blocks):
    return in_memory_blocks[:1] + memory_mapped_blocks[1:]


def assert_pickle_without_bringing_data_in_memory(table: MemoryMappedTable):
    with assert_arrow_memory_doesnt_increase():
        pickled_table = pickle.dumps(table)
        unpickled_table = pickle.loads(pickled_table)
    assert isinstance(unpickled_table, MemoryMappedTable)
    assert unpickled_table.table == table.table


def assert_pickle_does_bring_data_in_memory(table: MemoryMappedTable):
    with assert_arrow_memory_increases():
        pickled_table = pickle.dumps(table)
        unpickled_table = pickle.loads(pickled_table)
    assert isinstance(unpickled_table, MemoryMappedTable)
    assert unpickled_table.table == table.table


def test_inject_arrow_table_documentation(in_memory_pa_table):
    method = pa.Table.slice

    def function_to_wrap(*args):
        return method(*args)

    args = (0, 1)
    wrapped_method = inject_arrow_table_documentation(method)(function_to_wrap)
    assert method(in_memory_pa_table, *args) == wrapped_method(in_memory_pa_table, *args)
    assert "pyarrow.Table" not in wrapped_method.__doc__
    assert "Table" in wrapped_method.__doc__


def test__in_memory_arrow_table_from_file(arrow_file, in_memory_pa_table):
    with assert_arrow_memory_increases():
        pa_table = _in_memory_arrow_table_from_file(arrow_file)
        assert in_memory_pa_table == pa_table


def test__in_memory_arrow_table_from_buffer(in_memory_pa_table):
    with assert_arrow_memory_increases():
        buf_writer = pa.BufferOutputStream()
        writer = pa.RecordBatchStreamWriter(buf_writer, schema=in_memory_pa_table.schema)
        writer.write_table(in_memory_pa_table)
        writer.close()
        buf_writer.close()
        pa_table = _in_memory_arrow_table_from_buffer(buf_writer.getvalue())
        assert in_memory_pa_table == pa_table


def test__memory_mapped_arrow_table_from_file(arrow_file, in_memory_pa_table):
    with assert_arrow_memory_doesnt_increase():
        pa_table = _memory_mapped_arrow_table_from_file(arrow_file)
        assert in_memory_pa_table == pa_table


def test_table_init(in_memory_pa_table):
    table = Table(in_memory_pa_table)
    assert table.table == in_memory_pa_table


def test_table_validate(in_memory_pa_table):
    table = Table(in_memory_pa_table)
    assert table.validate() == in_memory_pa_table.validate()


def test_table_equals(in_memory_pa_table):
    table = Table(in_memory_pa_table)
    assert table.equals(in_memory_pa_table)


def test_table_to_batches(in_memory_pa_table):
    table = Table(in_memory_pa_table)
    assert table.to_batches() == in_memory_pa_table.to_batches()


def test_table_to_pydict(in_memory_pa_table):
    table = Table(in_memory_pa_table)
    assert table.to_pydict() == in_memory_pa_table.to_pydict()


def test_table_to_string(in_memory_pa_table):
    table = Table(in_memory_pa_table)
    assert table.to_string() == in_memory_pa_table.to_string()


def test_table_field(in_memory_pa_table):
    assert "tokens" in in_memory_pa_table.column_names
    table = Table(in_memory_pa_table)
    assert table.field("tokens") == in_memory_pa_table.field("tokens")


def test_table_column(in_memory_pa_table):
    assert "tokens" in in_memory_pa_table.column_names
    table = Table(in_memory_pa_table)
    assert table.column("tokens") == in_memory_pa_table.column("tokens")


def test_table_itercolumns(in_memory_pa_table):
    table = Table(in_memory_pa_table)
    assert isinstance(table.itercolumns(), type(in_memory_pa_table.itercolumns()))
    assert list(table.itercolumns()) == list(in_memory_pa_table.itercolumns())


def test_table_getitem(in_memory_pa_table):
    table = Table(in_memory_pa_table)
    assert table[0] == in_memory_pa_table[0]


def test_table_len(in_memory_pa_table):
    table = Table(in_memory_pa_table)
    assert len(table) == len(in_memory_pa_table)


def test_table_str(in_memory_pa_table):
    table = Table(in_memory_pa_table)
    assert str(table) == str(in_memory_pa_table).replace("pyarrow.Table", "Table")
    assert repr(table) == repr(in_memory_pa_table).replace("pyarrow.Table", "Table")


@pytest.mark.parametrize(
    "attribute", ["schema", "columns", "num_columns", "num_rows", "shape", "nbytes", "column_names"]
)
def test_table_attributes(in_memory_pa_table, attribute):
    table = Table(in_memory_pa_table)
    assert getattr(table, attribute) == getattr(in_memory_pa_table, attribute)


def test_in_memory_table_from_file(arrow_file, in_memory_pa_table):
    with assert_arrow_memory_increases():
        table = InMemoryTable.from_file(arrow_file)
        assert table.table == in_memory_pa_table
        assert isinstance(table, InMemoryTable)


def test_in_memory_table_from_buffer(in_memory_pa_table):
    with assert_arrow_memory_increases():
        buf_writer = pa.BufferOutputStream()
        writer = pa.RecordBatchStreamWriter(buf_writer, schema=in_memory_pa_table.schema)
        writer.write_table(in_memory_pa_table)
        writer.close()
        buf_writer.close()
        table = InMemoryTable.from_buffer(buf_writer.getvalue())
        assert table.table == in_memory_pa_table
        assert isinstance(table, InMemoryTable)


def test_in_memory_table_from_pandas(in_memory_pa_table):
    df = in_memory_pa_table.to_pandas()
    with assert_arrow_memory_increases():
        table = InMemoryTable.from_pandas(df)
        assert table.table == in_memory_pa_table
        assert isinstance(table, InMemoryTable)


def test_in_memory_table_from_arrays(in_memory_pa_table):
    arrays = list(in_memory_pa_table.columns)
    names = list(in_memory_pa_table.column_names)
    table = InMemoryTable.from_arrays(arrays, names=names)
    assert table.table == in_memory_pa_table
    assert isinstance(table, InMemoryTable)


def test_in_memory_table_from_pydict(in_memory_pa_table):
    pydict = in_memory_pa_table.to_pydict()
    with assert_arrow_memory_increases():
        table = InMemoryTable.from_pydict(pydict)
        assert isinstance(table, InMemoryTable)
        assert table.table == pa.Table.from_pydict(pydict)


def test_in_memory_table_from_batches(in_memory_pa_table):
    batches = list(in_memory_pa_table.to_batches())
    table = InMemoryTable.from_batches(batches)
    assert table.table == in_memory_pa_table
    assert isinstance(table, InMemoryTable)


@slow
def test_in_memory_table_pickle_big_table():
    big_table_4GB = InMemoryTable.from_pydict({"col": [0] * ((4 * 8 << 30) // 64)})
    length = len(big_table_4GB)
    big_table_4GB = pickle.dumps(big_table_4GB)
    big_table_4GB = pickle.loads(big_table_4GB)
    assert len(big_table_4GB) == length


def test_in_memory_table_slice(in_memory_pa_table):
    table = InMemoryTable(in_memory_pa_table).slice(1, 2)
    assert table.table == in_memory_pa_table.slice(1, 2)
    assert isinstance(table, InMemoryTable)


def test_in_memory_table_filter(in_memory_pa_table):
    mask = pa.array([i % 2 == 0 for i in range(len(in_memory_pa_table))])
    table = InMemoryTable(in_memory_pa_table).filter(mask)
    assert table.table == in_memory_pa_table.filter(mask)
    assert isinstance(table, InMemoryTable)


def test_in_memory_table_flatten(in_memory_pa_table):
    table = InMemoryTable(in_memory_pa_table).flatten()
    assert table.table == in_memory_pa_table.flatten()
    assert isinstance(table, InMemoryTable)


def test_in_memory_table_combine_chunks(in_memory_pa_table):
    table = InMemoryTable(in_memory_pa_table).combine_chunks()
    assert table.table == in_memory_pa_table.combine_chunks()
    assert isinstance(table, InMemoryTable)


def test_in_memory_table_cast(in_memory_pa_table):
    assert pa.list_(pa.int64()) in in_memory_pa_table.schema.types
    schema = pa.schema(
        {
            k: v if v != pa.list_(pa.int64()) else pa.list_(pa.int32())
            for k, v in zip(in_memory_pa_table.schema.names, in_memory_pa_table.schema.types)
        }
    )
    table = InMemoryTable(in_memory_pa_table).cast(schema)
    assert table.table == in_memory_pa_table.cast(schema)
    assert isinstance(table, InMemoryTable)


def test_in_memory_table_add_column(in_memory_pa_table):
    i = len(in_memory_pa_table.column_names)
    field_ = "new_field"
    column = pa.array([i for i in range(len(in_memory_pa_table))])
    table = InMemoryTable(in_memory_pa_table).add_column(i, field_, column)
    assert table.table == in_memory_pa_table.add_column(i, field_, column)
    assert isinstance(table, InMemoryTable)


def test_in_memory_table_append_column(in_memory_pa_table):
    field_ = "new_field"
    column = pa.array([i for i in range(len(in_memory_pa_table))])
    table = InMemoryTable(in_memory_pa_table).append_column(field_, column)
    assert table.table == in_memory_pa_table.append_column(field_, column)
    assert isinstance(table, InMemoryTable)


def test_in_memory_table_remove_column(in_memory_pa_table):
    table = InMemoryTable(in_memory_pa_table).remove_column(0)
    assert table.table == in_memory_pa_table.remove_column(0)
    assert isinstance(table, InMemoryTable)


def test_in_memory_table_set_column(in_memory_pa_table):
    i = len(in_memory_pa_table.column_names)
    field_ = "new_field"
    column = pa.array([i for i in range(len(in_memory_pa_table))])
    table = InMemoryTable(in_memory_pa_table).set_column(i, field_, column)
    assert table.table == in_memory_pa_table.set_column(i, field_, column)
    assert isinstance(table, InMemoryTable)


def test_in_memory_table_rename_columns(in_memory_pa_table):
    assert "tokens" in in_memory_pa_table.column_names
    names = [name if name != "tokens" else "new_tokens" for name in in_memory_pa_table.column_names]
    table = InMemoryTable(in_memory_pa_table).rename_columns(names)
    assert table.table == in_memory_pa_table.rename_columns(names)
    assert isinstance(table, InMemoryTable)


def test_in_memory_table_drop(in_memory_pa_table):
    names = [in_memory_pa_table.column_names[0]]
    table = InMemoryTable(in_memory_pa_table).drop(names)
    assert table.table == in_memory_pa_table.drop(names)
    assert isinstance(table, InMemoryTable)


def test_memory_mapped_table_init(arrow_file, in_memory_pa_table):
    table = MemoryMappedTable(_memory_mapped_arrow_table_from_file(arrow_file), arrow_file)
    assert table.table == in_memory_pa_table
    assert isinstance(table, MemoryMappedTable)
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_from_file(arrow_file, in_memory_pa_table):
    with assert_arrow_memory_doesnt_increase():
        table = MemoryMappedTable.from_file(arrow_file)
    assert table.table == in_memory_pa_table
    assert isinstance(table, MemoryMappedTable)
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_from_file_with_replay(arrow_file, in_memory_pa_table):
    replays = [("slice", (0, 1), {}), ("flatten", tuple(), {})]
    with assert_arrow_memory_doesnt_increase():
        table = MemoryMappedTable.from_file(arrow_file, replays=replays)
    assert len(table) == 1
    for method, args, kwargs in replays:
        in_memory_pa_table = getattr(in_memory_pa_table, method)(*args, **kwargs)
    assert table.table == in_memory_pa_table
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_pickle_doesnt_fill_memory(arrow_file):
    with assert_arrow_memory_doesnt_increase():
        table = MemoryMappedTable.from_file(arrow_file)
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_pickle_applies_replay(arrow_file):
    replays = [("slice", (0, 1), {}), ("flatten", tuple(), {})]
    with assert_arrow_memory_doesnt_increase():
        table = MemoryMappedTable.from_file(arrow_file, replays=replays)
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == replays
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_slice(arrow_file, in_memory_pa_table):
    table = MemoryMappedTable.from_file(arrow_file).slice(1, 2)
    assert table.table == in_memory_pa_table.slice(1, 2)
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("slice", (1, 2), {})]
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_filter(arrow_file, in_memory_pa_table):
    mask = pa.array([i % 2 == 0 for i in range(len(in_memory_pa_table))])
    table = MemoryMappedTable.from_file(arrow_file).filter(mask)
    assert table.table == in_memory_pa_table.filter(mask)
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("filter", (mask,), {})]
    # filter DOES increase memory
    # assert_pickle_without_bringing_data_in_memory(table)
    assert_pickle_does_bring_data_in_memory(table)


def test_memory_mapped_table_flatten(arrow_file, in_memory_pa_table):
    table = MemoryMappedTable.from_file(arrow_file).flatten()
    assert table.table == in_memory_pa_table.flatten()
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("flatten", tuple(), {})]
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_combine_chunks(arrow_file, in_memory_pa_table):
    table = MemoryMappedTable.from_file(arrow_file).combine_chunks()
    assert table.table == in_memory_pa_table.combine_chunks()
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("combine_chunks", tuple(), {})]
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_cast(arrow_file, in_memory_pa_table):
    assert pa.list_(pa.int64()) in in_memory_pa_table.schema.types
    schema = pa.schema(
        {
            k: v if v != pa.list_(pa.int64()) else pa.list_(pa.int32())
            for k, v in zip(in_memory_pa_table.schema.names, in_memory_pa_table.schema.types)
        }
    )
    table = MemoryMappedTable.from_file(arrow_file).cast(schema)
    assert table.table == in_memory_pa_table.cast(schema)
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("cast", (schema,), {})]
    # cast DOES increase memory when converting integers precision for example
    # assert_pickle_without_bringing_data_in_memory(table)
    assert_pickle_does_bring_data_in_memory(table)


def test_memory_mapped_table_add_column(arrow_file, in_memory_pa_table):
    i = len(in_memory_pa_table.column_names)
    field_ = "new_field"
    column = pa.array([i for i in range(len(in_memory_pa_table))])
    table = MemoryMappedTable.from_file(arrow_file).add_column(i, field_, column)
    assert table.table == in_memory_pa_table.add_column(i, field_, column)
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("add_column", (i, field_, column), {})]
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_append_column(arrow_file, in_memory_pa_table):
    field_ = "new_field"
    column = pa.array([i for i in range(len(in_memory_pa_table))])
    table = MemoryMappedTable.from_file(arrow_file).append_column(field_, column)
    assert table.table == in_memory_pa_table.append_column(field_, column)
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("append_column", (field_, column), {})]
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_remove_column(arrow_file, in_memory_pa_table):
    table = MemoryMappedTable.from_file(arrow_file).remove_column(0)
    assert table.table == in_memory_pa_table.remove_column(0)
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("remove_column", (0,), {})]
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_set_column(arrow_file, in_memory_pa_table):
    i = len(in_memory_pa_table.column_names)
    field_ = "new_field"
    column = pa.array([i for i in range(len(in_memory_pa_table))])
    table = MemoryMappedTable.from_file(arrow_file).set_column(i, field_, column)
    assert table.table == in_memory_pa_table.set_column(i, field_, column)
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("set_column", (i, field_, column), {})]
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_rename_columns(arrow_file, in_memory_pa_table):
    assert "tokens" in in_memory_pa_table.column_names
    names = [name if name != "tokens" else "new_tokens" for name in in_memory_pa_table.column_names]
    table = MemoryMappedTable.from_file(arrow_file).rename_columns(names)
    assert table.table == in_memory_pa_table.rename_columns(names)
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("rename_columns", (names,), {})]
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_drop(arrow_file, in_memory_pa_table):
    names = [in_memory_pa_table.column_names[0]]
    table = MemoryMappedTable.from_file(arrow_file).drop(names)
    assert table.table == in_memory_pa_table.drop(names)
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("drop", (names,), {})]
    assert_pickle_without_bringing_data_in_memory(table)


@pytest.mark.parametrize("blocks_type", ["in_memory", "memory_mapped", "mixed"])
def test_concatenation_table_init(
    blocks_type, in_memory_pa_table, in_memory_blocks, memory_mapped_blocks, mixed_in_memory_and_memory_mapped_blocks
):
    blocks = (
        in_memory_blocks
        if blocks_type == "in_memory"
        else memory_mapped_blocks
        if blocks_type == "memory_mapped"
        else mixed_in_memory_and_memory_mapped_blocks
    )
    table = ConcatenationTable(in_memory_pa_table, blocks)
    assert table.table == in_memory_pa_table
    assert table.blocks == blocks


def test_concatenation_table_from_blocks(in_memory_pa_table, in_memory_blocks):
    assert len(in_memory_pa_table) > 2
    in_memory_table = InMemoryTable(in_memory_pa_table)
    t1, t2 = in_memory_table.slice(0, 2), in_memory_table.slice(2)
    table = ConcatenationTable.from_blocks(in_memory_table)
    assert isinstance(table, ConcatenationTable)
    assert table.table == in_memory_pa_table
    assert table.blocks == [[in_memory_table]]
    table = ConcatenationTable.from_blocks([t1, t2])
    assert isinstance(table, ConcatenationTable)
    assert table.table == in_memory_pa_table
    assert table.blocks == [[in_memory_table]]
    table = ConcatenationTable.from_blocks([[t1], [t2]])
    assert isinstance(table, ConcatenationTable)
    assert table.table == in_memory_pa_table
    assert table.blocks == [[in_memory_table]]
    table = ConcatenationTable.from_blocks(in_memory_blocks)
    assert isinstance(table, ConcatenationTable)
    assert table.table == in_memory_pa_table
    assert table.blocks == [[in_memory_table]]


@pytest.mark.parametrize("blocks_type", ["in_memory", "memory_mapped", "mixed"])
def test_concatenation_table_from_blocks_doesnt_increase_memory(
    blocks_type, in_memory_pa_table, in_memory_blocks, memory_mapped_blocks, mixed_in_memory_and_memory_mapped_blocks
):
    blocks = {
        "in_memory": in_memory_blocks,
        "memory_mapped": memory_mapped_blocks,
        "mixed": mixed_in_memory_and_memory_mapped_blocks,
    }[blocks_type]
    with assert_arrow_memory_doesnt_increase():
        table = ConcatenationTable.from_blocks(blocks)
        assert isinstance(table, ConcatenationTable)
        assert table.table == in_memory_pa_table
        if blocks_type == "in_memory":
            assert table.blocks == [[InMemoryTable(in_memory_pa_table)]]
        else:
            assert table.blocks == blocks


@pytest.mark.parametrize("axis", [0, 1])
def test_concatenation_table_from_tables(axis, in_memory_pa_table, arrow_file):
    in_memory_table = InMemoryTable(in_memory_pa_table)
    concatenation_table = ConcatenationTable.from_blocks(in_memory_table)
    memory_mapped_table = MemoryMappedTable.from_file(arrow_file)
    tables = [in_memory_pa_table, in_memory_table, concatenation_table, memory_mapped_table]
    if axis == 0:
        expected_table = pa.concat_tables([in_memory_pa_table] * len(tables))
    else:
        expected_table = in_memory_pa_table
        for _ in range(1, len(tables)):
            for name, col in zip(in_memory_pa_table.column_names, in_memory_pa_table.columns):
                expected_table = expected_table.append_column(name, col)

    with assert_arrow_memory_doesnt_increase():
        table = ConcatenationTable.from_tables(tables, axis=axis)
    assert isinstance(table, ConcatenationTable)
    assert table.table == expected_table
    # because of consolidation, we end up with 1 InMemoryTable and 1 MemoryMappedTable
    assert len(table.blocks) == 1 if axis == 1 else 2
    assert len(table.blocks[0]) == 1 if axis == 0 else 2
    assert axis == 1 or len(table.blocks[1]) == 1
    assert isinstance(table.blocks[0][0], InMemoryTable)
    assert isinstance(table.blocks[1][0] if axis == 0 else table.blocks[0][1], MemoryMappedTable)


@pytest.mark.parametrize("blocks_type", ["in_memory", "memory_mapped", "mixed"])
def test_concatenation_table_slice(
    blocks_type, in_memory_pa_table, in_memory_blocks, memory_mapped_blocks, mixed_in_memory_and_memory_mapped_blocks
):
    blocks = {
        "in_memory": in_memory_blocks,
        "memory_mapped": memory_mapped_blocks,
        "mixed": mixed_in_memory_and_memory_mapped_blocks,
    }[blocks_type]
    table = ConcatenationTable.from_blocks(blocks).slice(1, 2)
    assert table.table == in_memory_pa_table.slice(1, 2)
    assert isinstance(table, ConcatenationTable)


@pytest.mark.parametrize("blocks_type", ["in_memory", "memory_mapped", "mixed"])
def test_concatenation_table_filter(
    blocks_type, in_memory_pa_table, in_memory_blocks, memory_mapped_blocks, mixed_in_memory_and_memory_mapped_blocks
):
    blocks = {
        "in_memory": in_memory_blocks,
        "memory_mapped": memory_mapped_blocks,
        "mixed": mixed_in_memory_and_memory_mapped_blocks,
    }[blocks_type]
    mask = pa.array([i % 2 == 0 for i in range(len(in_memory_pa_table))])
    table = ConcatenationTable.from_blocks(blocks).filter(mask)
    assert table.table == in_memory_pa_table.filter(mask)
    assert isinstance(table, ConcatenationTable)


@pytest.mark.parametrize("blocks_type", ["in_memory", "memory_mapped", "mixed"])
def test_concatenation_table_flatten(
    blocks_type, in_memory_pa_table, in_memory_blocks, memory_mapped_blocks, mixed_in_memory_and_memory_mapped_blocks
):
    blocks = {
        "in_memory": in_memory_blocks,
        "memory_mapped": memory_mapped_blocks,
        "mixed": mixed_in_memory_and_memory_mapped_blocks,
    }[blocks_type]
    table = ConcatenationTable.from_blocks(blocks).flatten()
    assert table.table == in_memory_pa_table.flatten()
    assert isinstance(table, ConcatenationTable)


@pytest.mark.parametrize("blocks_type", ["in_memory", "memory_mapped", "mixed"])
def test_concatenation_table_combine_chunks(
    blocks_type, in_memory_pa_table, in_memory_blocks, memory_mapped_blocks, mixed_in_memory_and_memory_mapped_blocks
):
    blocks = {
        "in_memory": in_memory_blocks,
        "memory_mapped": memory_mapped_blocks,
        "mixed": mixed_in_memory_and_memory_mapped_blocks,
    }[blocks_type]
    table = ConcatenationTable.from_blocks(blocks).combine_chunks()
    assert table.table == in_memory_pa_table.combine_chunks()
    assert isinstance(table, ConcatenationTable)


@pytest.mark.parametrize("blocks_type", ["in_memory", "memory_mapped", "mixed"])
def test_concatenation_table_cast(
    blocks_type, in_memory_pa_table, in_memory_blocks, memory_mapped_blocks, mixed_in_memory_and_memory_mapped_blocks
):
    blocks = {
        "in_memory": in_memory_blocks,
        "memory_mapped": memory_mapped_blocks,
        "mixed": mixed_in_memory_and_memory_mapped_blocks,
    }[blocks_type]
    assert pa.list_(pa.int64()) in in_memory_pa_table.schema.types
    assert pa.int64() in in_memory_pa_table.schema.types
    schema = pa.schema(
        {
            k: v if v != pa.list_(pa.int64()) else pa.list_(pa.int32())
            for k, v in zip(in_memory_pa_table.schema.names, in_memory_pa_table.schema.types)
        }
    )
    with pytest.raises(pa.ArrowNotImplementedError):
        ConcatenationTable.from_blocks(blocks).cast(schema)
    schema = pa.schema(
        {
            k: v if v != pa.int64() else pa.int32()
            for k, v in zip(in_memory_pa_table.schema.names, in_memory_pa_table.schema.types)
        }
    )
    table = ConcatenationTable.from_blocks(blocks).cast(schema)
    assert table.table == in_memory_pa_table.cast(schema)
    assert isinstance(table, ConcatenationTable)


@pytest.mark.parametrize("blocks_type", ["in_memory", "memory_mapped", "mixed"])
def test_concatenation_table_add_column(
    blocks_type, in_memory_pa_table, in_memory_blocks, memory_mapped_blocks, mixed_in_memory_and_memory_mapped_blocks
):
    blocks = {
        "in_memory": in_memory_blocks,
        "memory_mapped": memory_mapped_blocks,
        "mixed": mixed_in_memory_and_memory_mapped_blocks,
    }[blocks_type]
    i = len(in_memory_pa_table.column_names)
    field_ = "new_field"
    column = pa.array([i for i in range(len(in_memory_pa_table))])
    with pytest.raises(NotImplementedError):
        ConcatenationTable.from_blocks(blocks).add_column(i, field_, column)
        # assert table.table == in_memory_pa_table.add_column(i, field_, column)
        # unpickled_table = pickle.loads(pickle.dumps(table))
        # assert unpickled_table.table == in_memory_pa_table.add_column(i, field_, column)


@pytest.mark.parametrize("blocks_type", ["in_memory", "memory_mapped", "mixed"])
def test_concatenation_table_append_column(
    blocks_type, in_memory_pa_table, in_memory_blocks, memory_mapped_blocks, mixed_in_memory_and_memory_mapped_blocks
):
    blocks = {
        "in_memory": in_memory_blocks,
        "memory_mapped": memory_mapped_blocks,
        "mixed": mixed_in_memory_and_memory_mapped_blocks,
    }[blocks_type]
    field_ = "new_field"
    column = pa.array([i for i in range(len(in_memory_pa_table))])
    with pytest.raises(NotImplementedError):
        ConcatenationTable.from_blocks(blocks).append_column(field_, column)
        # assert table.table == in_memory_pa_table.append_column(field_, column)
        # unpickled_table = pickle.loads(pickle.dumps(table))
        # assert unpickled_table.table == in_memory_pa_table.append_column(field_, column)


@pytest.mark.parametrize("blocks_type", ["in_memory", "memory_mapped", "mixed"])
def test_concatenation_table_remove_column(
    blocks_type, in_memory_pa_table, in_memory_blocks, memory_mapped_blocks, mixed_in_memory_and_memory_mapped_blocks
):
    blocks = {
        "in_memory": in_memory_blocks,
        "memory_mapped": memory_mapped_blocks,
        "mixed": mixed_in_memory_and_memory_mapped_blocks,
    }[blocks_type]
    table = ConcatenationTable.from_blocks(blocks).remove_column(0)
    assert table.table == in_memory_pa_table.remove_column(0)
    assert isinstance(table, ConcatenationTable)


@pytest.mark.parametrize("blocks_type", ["in_memory", "memory_mapped", "mixed"])
def test_concatenation_table_set_column(
    blocks_type, in_memory_pa_table, in_memory_blocks, memory_mapped_blocks, mixed_in_memory_and_memory_mapped_blocks
):
    blocks = {
        "in_memory": in_memory_blocks,
        "memory_mapped": memory_mapped_blocks,
        "mixed": mixed_in_memory_and_memory_mapped_blocks,
    }[blocks_type]
    i = len(in_memory_pa_table.column_names)
    field_ = "new_field"
    column = pa.array([i for i in range(len(in_memory_pa_table))])
    with pytest.raises(NotImplementedError):
        ConcatenationTable.from_blocks(blocks).set_column(i, field_, column)
        # assert table.table == in_memory_pa_table.set_column(i, field_, column)
        # unpickled_table = pickle.loads(pickle.dumps(table))
        # assert unpickled_table.table == in_memory_pa_table.set_column(i, field_, column)


@pytest.mark.parametrize("blocks_type", ["in_memory", "memory_mapped", "mixed"])
def test_concatenation_table_rename_columns(
    blocks_type, in_memory_pa_table, in_memory_blocks, memory_mapped_blocks, mixed_in_memory_and_memory_mapped_blocks
):
    blocks = {
        "in_memory": in_memory_blocks,
        "memory_mapped": memory_mapped_blocks,
        "mixed": mixed_in_memory_and_memory_mapped_blocks,
    }[blocks_type]
    assert "tokens" in in_memory_pa_table.column_names
    names = [name if name != "tokens" else "new_tokens" for name in in_memory_pa_table.column_names]
    table = ConcatenationTable.from_blocks(blocks).rename_columns(names)
    assert isinstance(table, ConcatenationTable)
    assert table.table == in_memory_pa_table.rename_columns(names)


@pytest.mark.parametrize("blocks_type", ["in_memory", "memory_mapped", "mixed"])
def test_concatenation_table_drop(
    blocks_type, in_memory_pa_table, in_memory_blocks, memory_mapped_blocks, mixed_in_memory_and_memory_mapped_blocks
):
    blocks = {
        "in_memory": in_memory_blocks,
        "memory_mapped": memory_mapped_blocks,
        "mixed": mixed_in_memory_and_memory_mapped_blocks,
    }[blocks_type]
    names = [in_memory_pa_table.column_names[0]]
    table = ConcatenationTable.from_blocks(blocks).drop(names)
    assert table.table == in_memory_pa_table.drop(names)
    assert isinstance(table, ConcatenationTable)


def test_concat_tables(arrow_file, in_memory_pa_table):
    t0 = in_memory_pa_table
    t1 = InMemoryTable(t0)
    t2 = MemoryMappedTable.from_file(arrow_file)
    t3 = ConcatenationTable.from_blocks(t1)
    tables = [t0, t1, t2, t3]
    concatenated_table = concat_tables(tables, axis=0)
    assert concatenated_table.table == pa.concat_tables([t0] * 4)
    assert concatenated_table.table.shape == (40, 4)
    assert isinstance(concatenated_table, ConcatenationTable)
    assert len(concatenated_table.blocks) == 3  # t0 and t1 are consolidated as a single InMemoryTable
    assert isinstance(concatenated_table.blocks[0][0], InMemoryTable)
    assert isinstance(concatenated_table.blocks[1][0], MemoryMappedTable)
    assert isinstance(concatenated_table.blocks[2][0], InMemoryTable)
    concatenated_table = concat_tables(tables, axis=1)
    assert concatenated_table.table.shape == (10, 16)
    assert len(concatenated_table.blocks[0]) == 3  # t0 and t1 are consolidated as a single InMemoryTable
    assert isinstance(concatenated_table.blocks[0][0], InMemoryTable)
    assert isinstance(concatenated_table.blocks[0][1], MemoryMappedTable)
    assert isinstance(concatenated_table.blocks[0][2], InMemoryTable)


def _interpolation_search_ground_truth(arr: List[int], x: int) -> Union[int, IndexError]:
    for i in range(len(arr) - 1):
        if arr[i] <= x < arr[i + 1]:
            return i
    return IndexError


class _ListWithGetitemCounter(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unique_getitem_calls = set()

    def __getitem__(self, i):
        out = super().__getitem__(i)
        self.unique_getitem_calls.add(i)
        return out

    @property
    def getitem_unique_count(self):
        return len(self.unique_getitem_calls)


@pytest.mark.parametrize(
    "arr, x",
    [(np.arange(0, 14, 3), x) for x in range(-1, 22)]
    + [(list(np.arange(-5, 5)), x) for x in range(-6, 6)]
    + [([0, 1_000, 1_001, 1_003], x) for x in [-1, 0, 2, 100, 999, 1_000, 1_001, 1_002, 1_003, 1_004]]
    + [(list(range(1_000)), x) for x in [-1, 0, 1, 10, 666, 999, 1_000, 1_0001]],
)
def test_interpolation_search(arr, x):
    ground_truth = _interpolation_search_ground_truth(arr, x)
    if isinstance(ground_truth, int):
        arr = _ListWithGetitemCounter(arr)
        output = _interpolation_search(arr, x)
        assert ground_truth == output
        # 4 maximum unique getitem calls is expected for the cases of this test
        # but it can be bigger for large and messy arrays.
        assert arr.getitem_unique_count <= 4
    else:
        with pytest.raises(ground_truth):
            _interpolation_search(arr, x)


def test_indexed_table_mixin():
    n_rows_per_chunk = 10
    n_chunks = 4
    pa_table = pa.Table.from_pydict({"col": [0] * n_rows_per_chunk})
    pa_table = pa.concat_tables([pa_table] * n_chunks)
    table = Table(pa_table)
    assert all(table._offsets.tolist() == np.cumsum([0] + [n_rows_per_chunk] * n_chunks))
    assert table.fast_slice(5) == pa_table.slice(5)
    assert table.fast_slice(2, 13) == pa_table.slice(2, 13)
