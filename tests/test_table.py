import copy
import pickle
from decimal import Decimal
from functools import partial
from typing import List, Union
from unittest.mock import MagicMock

import numpy as np
import pyarrow as pa
import pytest

from datasets.features import Array2D, ClassLabel, Features, Image, LargeList, Sequence, Value
from datasets.features.features import Array2DExtensionType, get_nested_type
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
    array_cast,
    cast_array_to_feature,
    cast_table_to_schema,
    concat_tables,
    embed_array_storage,
    embed_table_storage,
    inject_arrow_table_documentation,
    table_cast,
    table_iter,
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


def assert_deepcopy_without_bringing_data_in_memory(table: MemoryMappedTable):
    with assert_arrow_memory_doesnt_increase():
        copied_table = copy.deepcopy(table)
    assert isinstance(copied_table, MemoryMappedTable)
    assert copied_table.table == table.table


def assert_deepcopy_does_bring_data_in_memory(table: MemoryMappedTable):
    with assert_arrow_memory_increases():
        copied_table = copy.deepcopy(table)
    assert isinstance(copied_table, MemoryMappedTable)
    assert copied_table.table == table.table


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


def assert_index_attributes_equal(table: Table, other: Table):
    assert table._batches == other._batches
    np.testing.assert_array_equal(table._offsets, other._offsets)
    assert table._schema == other._schema


def add_suffix_to_column_names(table, suffix):
    return table.rename_columns([f"{name}{suffix}" for name in table.column_names])


def test_inject_arrow_table_documentation(in_memory_pa_table):
    method = pa.Table.slice

    def function_to_wrap(*args):
        return method(*args)

    args = (0, 1)
    wrapped_method = inject_arrow_table_documentation(method)(function_to_wrap)
    assert method(in_memory_pa_table, *args) == wrapped_method(in_memory_pa_table, *args)
    assert "pyarrow.Table" not in wrapped_method.__doc__
    assert "Table" in wrapped_method.__doc__


def test_in_memory_arrow_table_from_file(arrow_file, in_memory_pa_table):
    with assert_arrow_memory_increases():
        pa_table = _in_memory_arrow_table_from_file(arrow_file)
        assert in_memory_pa_table == pa_table


def test_in_memory_arrow_table_from_buffer(in_memory_pa_table):
    with assert_arrow_memory_increases():
        buf_writer = pa.BufferOutputStream()
        writer = pa.RecordBatchStreamWriter(buf_writer, schema=in_memory_pa_table.schema)
        writer.write_table(in_memory_pa_table)
        writer.close()
        buf_writer.close()
        pa_table = _in_memory_arrow_table_from_buffer(buf_writer.getvalue())
        assert in_memory_pa_table == pa_table


def test_memory_mapped_arrow_table_from_file(arrow_file, in_memory_pa_table):
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
        # with no schema it might infer another order of the fields in the schema
        table = InMemoryTable.from_pandas(df)
        assert isinstance(table, InMemoryTable)
    # by specifying schema we get the same order of features, and so the exact same table
    table = InMemoryTable.from_pandas(df, schema=in_memory_pa_table.schema)
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


def test_in_memory_table_from_pylist(in_memory_pa_table):
    pylist = InMemoryTable(in_memory_pa_table).to_pylist()
    table = InMemoryTable.from_pylist(pylist)
    assert isinstance(table, InMemoryTable)
    assert pylist == table.to_pylist()


def test_in_memory_table_from_batches(in_memory_pa_table):
    batches = list(in_memory_pa_table.to_batches())
    table = InMemoryTable.from_batches(batches)
    assert table.table == in_memory_pa_table
    assert isinstance(table, InMemoryTable)


def test_in_memory_table_deepcopy(in_memory_pa_table):
    table = InMemoryTable(in_memory_pa_table)
    copied_table = copy.deepcopy(table)
    assert table.table == copied_table.table
    assert_index_attributes_equal(table, copied_table)
    # deepcopy must return the exact same arrow objects since they are immutable
    assert table.table is copied_table.table
    assert all(batch1 is batch2 for batch1, batch2 in zip(table._batches, copied_table._batches))


def test_in_memory_table_pickle(in_memory_pa_table):
    table = InMemoryTable(in_memory_pa_table)
    pickled_table = pickle.dumps(table)
    unpickled_table = pickle.loads(pickled_table)
    assert unpickled_table.table == table.table
    assert_index_attributes_equal(table, unpickled_table)


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


def test_in_memory_table_cast_reorder_struct():
    table = InMemoryTable(
        pa.Table.from_pydict(
            {
                "top": [
                    {
                        "foo": "a",
                        "bar": "b",
                    }
                ]
            }
        )
    )
    schema = pa.schema({"top": pa.struct({"bar": pa.string(), "foo": pa.string()})})
    assert table.cast(schema).schema == schema


def test_in_memory_table_cast_with_hf_features():
    table = InMemoryTable(pa.Table.from_pydict({"labels": [0, 1]}))
    features = Features({"labels": ClassLabel(names=["neg", "pos"])})
    schema = features.arrow_schema
    assert table.cast(schema).schema == schema
    assert Features.from_arrow_schema(table.cast(schema).schema) == features


def test_in_memory_table_replace_schema_metadata(in_memory_pa_table):
    metadata = {"huggingface": "{}"}
    table = InMemoryTable(in_memory_pa_table).replace_schema_metadata(metadata)
    assert table.table.schema.metadata == in_memory_pa_table.replace_schema_metadata(metadata).schema.metadata
    assert isinstance(table, InMemoryTable)


def test_in_memory_table_add_column(in_memory_pa_table):
    i = len(in_memory_pa_table.column_names)
    field_ = "new_field"
    column = pa.array(list(range(len(in_memory_pa_table))))
    table = InMemoryTable(in_memory_pa_table).add_column(i, field_, column)
    assert table.table == in_memory_pa_table.add_column(i, field_, column)
    assert isinstance(table, InMemoryTable)


def test_in_memory_table_append_column(in_memory_pa_table):
    field_ = "new_field"
    column = pa.array(list(range(len(in_memory_pa_table))))
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
    column = pa.array(list(range(len(in_memory_pa_table))))
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
    assert_deepcopy_without_bringing_data_in_memory(table)
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_from_file(arrow_file, in_memory_pa_table):
    with assert_arrow_memory_doesnt_increase():
        table = MemoryMappedTable.from_file(arrow_file)
    assert table.table == in_memory_pa_table
    assert isinstance(table, MemoryMappedTable)
    assert_deepcopy_without_bringing_data_in_memory(table)
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_from_file_with_replay(arrow_file, in_memory_pa_table):
    replays = [("slice", (0, 1), {}), ("flatten", (), {})]
    with assert_arrow_memory_doesnt_increase():
        table = MemoryMappedTable.from_file(arrow_file, replays=replays)
    assert len(table) == 1
    for method, args, kwargs in replays:
        in_memory_pa_table = getattr(in_memory_pa_table, method)(*args, **kwargs)
    assert table.table == in_memory_pa_table
    assert_deepcopy_without_bringing_data_in_memory(table)
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_deepcopy(arrow_file):
    table = MemoryMappedTable.from_file(arrow_file)
    copied_table = copy.deepcopy(table)
    assert table.table == copied_table.table
    assert table.path == copied_table.path
    assert_index_attributes_equal(table, copied_table)
    # deepcopy must return the exact same arrow objects since they are immutable
    assert table.table is copied_table.table
    assert all(batch1 is batch2 for batch1, batch2 in zip(table._batches, copied_table._batches))


def test_memory_mapped_table_pickle(arrow_file):
    table = MemoryMappedTable.from_file(arrow_file)
    pickled_table = pickle.dumps(table)
    unpickled_table = pickle.loads(pickled_table)
    assert unpickled_table.table == table.table
    assert unpickled_table.path == table.path
    assert_index_attributes_equal(table, unpickled_table)


def test_memory_mapped_table_pickle_doesnt_fill_memory(arrow_file):
    with assert_arrow_memory_doesnt_increase():
        table = MemoryMappedTable.from_file(arrow_file)
    assert_deepcopy_without_bringing_data_in_memory(table)
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_pickle_applies_replay(arrow_file):
    replays = [("slice", (0, 1), {}), ("flatten", (), {})]
    with assert_arrow_memory_doesnt_increase():
        table = MemoryMappedTable.from_file(arrow_file, replays=replays)
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == replays
    assert_deepcopy_without_bringing_data_in_memory(table)
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_slice(arrow_file, in_memory_pa_table):
    table = MemoryMappedTable.from_file(arrow_file).slice(1, 2)
    assert table.table == in_memory_pa_table.slice(1, 2)
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("slice", (1, 2), {})]
    assert_deepcopy_without_bringing_data_in_memory(table)
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_filter(arrow_file, in_memory_pa_table):
    mask = pa.array([i % 2 == 0 for i in range(len(in_memory_pa_table))])
    table = MemoryMappedTable.from_file(arrow_file).filter(mask)
    assert table.table == in_memory_pa_table.filter(mask)
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("filter", (mask,), {})]
    assert_deepcopy_without_bringing_data_in_memory(table)
    # filter DOES increase memory
    # assert_pickle_without_bringing_data_in_memory(table)
    assert_pickle_does_bring_data_in_memory(table)


def test_memory_mapped_table_flatten(arrow_file, in_memory_pa_table):
    table = MemoryMappedTable.from_file(arrow_file).flatten()
    assert table.table == in_memory_pa_table.flatten()
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("flatten", (), {})]
    assert_deepcopy_without_bringing_data_in_memory(table)
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_combine_chunks(arrow_file, in_memory_pa_table):
    table = MemoryMappedTable.from_file(arrow_file).combine_chunks()
    assert table.table == in_memory_pa_table.combine_chunks()
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("combine_chunks", (), {})]
    assert_deepcopy_without_bringing_data_in_memory(table)
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
    assert_deepcopy_without_bringing_data_in_memory(table)
    # cast DOES increase memory when converting integers precision for example
    # assert_pickle_without_bringing_data_in_memory(table)
    assert_pickle_does_bring_data_in_memory(table)


def test_memory_mapped_table_replace_schema_metadata(arrow_file, in_memory_pa_table):
    metadata = {"huggingface": "{}"}
    table = MemoryMappedTable.from_file(arrow_file).replace_schema_metadata(metadata)
    assert table.table.schema.metadata == in_memory_pa_table.replace_schema_metadata(metadata).schema.metadata
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("replace_schema_metadata", (metadata,), {})]
    assert_deepcopy_without_bringing_data_in_memory(table)
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_add_column(arrow_file, in_memory_pa_table):
    i = len(in_memory_pa_table.column_names)
    field_ = "new_field"
    column = pa.array(list(range(len(in_memory_pa_table))))
    table = MemoryMappedTable.from_file(arrow_file).add_column(i, field_, column)
    assert table.table == in_memory_pa_table.add_column(i, field_, column)
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("add_column", (i, field_, column), {})]
    assert_deepcopy_without_bringing_data_in_memory(table)
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_append_column(arrow_file, in_memory_pa_table):
    field_ = "new_field"
    column = pa.array(list(range(len(in_memory_pa_table))))
    table = MemoryMappedTable.from_file(arrow_file).append_column(field_, column)
    assert table.table == in_memory_pa_table.append_column(field_, column)
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("append_column", (field_, column), {})]
    assert_deepcopy_without_bringing_data_in_memory(table)
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_remove_column(arrow_file, in_memory_pa_table):
    table = MemoryMappedTable.from_file(arrow_file).remove_column(0)
    assert table.table == in_memory_pa_table.remove_column(0)
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("remove_column", (0,), {})]
    assert_deepcopy_without_bringing_data_in_memory(table)
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_set_column(arrow_file, in_memory_pa_table):
    i = len(in_memory_pa_table.column_names)
    field_ = "new_field"
    column = pa.array(list(range(len(in_memory_pa_table))))
    table = MemoryMappedTable.from_file(arrow_file).set_column(i, field_, column)
    assert table.table == in_memory_pa_table.set_column(i, field_, column)
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("set_column", (i, field_, column), {})]
    assert_deepcopy_without_bringing_data_in_memory(table)
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_rename_columns(arrow_file, in_memory_pa_table):
    assert "tokens" in in_memory_pa_table.column_names
    names = [name if name != "tokens" else "new_tokens" for name in in_memory_pa_table.column_names]
    table = MemoryMappedTable.from_file(arrow_file).rename_columns(names)
    assert table.table == in_memory_pa_table.rename_columns(names)
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("rename_columns", (names,), {})]
    assert_deepcopy_without_bringing_data_in_memory(table)
    assert_pickle_without_bringing_data_in_memory(table)


def test_memory_mapped_table_drop(arrow_file, in_memory_pa_table):
    names = [in_memory_pa_table.column_names[0]]
    table = MemoryMappedTable.from_file(arrow_file).drop(names)
    assert table.table == in_memory_pa_table.drop(names)
    assert isinstance(table, MemoryMappedTable)
    assert table.replays == [("drop", (names,), {})]
    assert_deepcopy_without_bringing_data_in_memory(table)
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
        # avoids error due to duplicate column names
        tables[1:] = [add_suffix_to_column_names(table, i) for i, table in enumerate(tables[1:], 1)]
        expected_table = in_memory_pa_table
        for table in tables[1:]:
            for name, col in zip(table.column_names, table.columns):
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


def test_concatenation_table_from_tables_axis1_misaligned_blocks(arrow_file):
    table = MemoryMappedTable.from_file(arrow_file)
    t1 = table.slice(0, 2)
    t2 = table.slice(0, 3).rename_columns([col + "_1" for col in table.column_names])
    concatenated = ConcatenationTable.from_tables(
        [
            ConcatenationTable.from_blocks([[t1], [t1], [t1]]),
            ConcatenationTable.from_blocks([[t2], [t2]]),
        ],
        axis=1,
    )
    assert len(concatenated) == 6
    assert [len(row_blocks[0]) for row_blocks in concatenated.blocks] == [2, 1, 1, 2]
    concatenated = ConcatenationTable.from_tables(
        [
            ConcatenationTable.from_blocks([[t2], [t2]]),
            ConcatenationTable.from_blocks([[t1], [t1], [t1]]),
        ],
        axis=1,
    )
    assert len(concatenated) == 6
    assert [len(row_blocks[0]) for row_blocks in concatenated.blocks] == [2, 1, 1, 2]


@pytest.mark.parametrize("blocks_type", ["in_memory", "memory_mapped", "mixed"])
def test_concatenation_table_deepcopy(
    blocks_type, in_memory_blocks, memory_mapped_blocks, mixed_in_memory_and_memory_mapped_blocks
):
    blocks = {
        "in_memory": in_memory_blocks,
        "memory_mapped": memory_mapped_blocks,
        "mixed": mixed_in_memory_and_memory_mapped_blocks,
    }[blocks_type]
    table = ConcatenationTable.from_blocks(blocks)
    copied_table = copy.deepcopy(table)
    assert table.table == copied_table.table
    assert table.blocks == copied_table.blocks
    assert_index_attributes_equal(table, copied_table)
    # deepcopy must return the exact same arrow objects since they are immutable
    assert table.table is copied_table.table
    assert all(batch1 is batch2 for batch1, batch2 in zip(table._batches, copied_table._batches))


@pytest.mark.parametrize("blocks_type", ["in_memory", "memory_mapped", "mixed"])
def test_concatenation_table_pickle(
    blocks_type, in_memory_blocks, memory_mapped_blocks, mixed_in_memory_and_memory_mapped_blocks
):
    blocks = {
        "in_memory": in_memory_blocks,
        "memory_mapped": memory_mapped_blocks,
        "mixed": mixed_in_memory_and_memory_mapped_blocks,
    }[blocks_type]
    table = ConcatenationTable.from_blocks(blocks)
    pickled_table = pickle.dumps(table)
    unpickled_table = pickle.loads(pickled_table)
    assert unpickled_table.table == table.table
    assert unpickled_table.blocks == table.blocks
    assert_index_attributes_equal(table, unpickled_table)


def test_concat_tables_with_features_metadata(arrow_file, in_memory_pa_table):
    input_features = Features.from_arrow_schema(in_memory_pa_table.schema)
    input_features["id"] = Value("int64", id="my_id")
    intput_schema = input_features.arrow_schema
    t0 = in_memory_pa_table.replace_schema_metadata(intput_schema.metadata)
    t1 = MemoryMappedTable.from_file(arrow_file)
    tables = [t0, t1]
    concatenated_table = concat_tables(tables, axis=0)
    output_schema = concatenated_table.schema
    output_features = Features.from_arrow_schema(output_schema)
    assert output_schema == intput_schema
    assert output_schema.metadata == intput_schema.metadata
    assert output_features == input_features
    assert output_features["id"].id == "my_id"


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


def test_concatenation_table_slice_mixed_schemas_vertically(arrow_file):
    t1 = MemoryMappedTable.from_file(arrow_file)
    t2 = InMemoryTable.from_pydict({"additional_column": ["foo"]})
    expected = pa.table(
        {
            **{column: values + [None] for column, values in t1.to_pydict().items()},
            "additional_column": [None] * len(t1) + ["foo"],
        }
    )
    blocks = [[t1], [t2]]
    table = ConcatenationTable.from_blocks(blocks)
    assert table.to_pydict() == expected.to_pydict()
    assert isinstance(table, ConcatenationTable)
    reloaded = pickle.loads(pickle.dumps(table))
    assert reloaded.to_pydict() == expected.to_pydict()
    assert isinstance(reloaded, ConcatenationTable)
    reloaded = pickle.loads(pickle.dumps(table.slice(1, 2)))
    assert reloaded.to_pydict() == expected.slice(1, 2).to_pydict()
    assert isinstance(reloaded, ConcatenationTable)


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
    table = ConcatenationTable.from_blocks(blocks).cast(schema)
    assert table.table == in_memory_pa_table.cast(schema)
    assert isinstance(table, ConcatenationTable)
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
def test_concat_tables_cast_with_features_metadata(
    blocks_type, in_memory_pa_table, in_memory_blocks, memory_mapped_blocks, mixed_in_memory_and_memory_mapped_blocks
):
    blocks = {
        "in_memory": in_memory_blocks,
        "memory_mapped": memory_mapped_blocks,
        "mixed": mixed_in_memory_and_memory_mapped_blocks,
    }[blocks_type]
    input_features = Features.from_arrow_schema(in_memory_pa_table.schema)
    input_features["id"] = Value("int64", id="my_id")
    intput_schema = input_features.arrow_schema
    concatenated_table = ConcatenationTable.from_blocks(blocks).cast(intput_schema)
    output_schema = concatenated_table.schema
    output_features = Features.from_arrow_schema(output_schema)
    assert output_schema == intput_schema
    assert output_schema.metadata == intput_schema.metadata
    assert output_features == input_features
    assert output_features["id"].id == "my_id"


@pytest.mark.parametrize("blocks_type", ["in_memory", "memory_mapped", "mixed"])
def test_concatenation_table_replace_schema_metadata(
    blocks_type, in_memory_pa_table, in_memory_blocks, memory_mapped_blocks, mixed_in_memory_and_memory_mapped_blocks
):
    blocks = {
        "in_memory": in_memory_blocks,
        "memory_mapped": memory_mapped_blocks,
        "mixed": mixed_in_memory_and_memory_mapped_blocks,
    }[blocks_type]
    metadata = {"huggingface": "{}"}
    table = ConcatenationTable.from_blocks(blocks).replace_schema_metadata(metadata)
    assert table.table.schema.metadata == in_memory_pa_table.replace_schema_metadata(metadata).schema.metadata
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
    column = pa.array(list(range(len(in_memory_pa_table))))
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
    column = pa.array(list(range(len(in_memory_pa_table))))
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
    column = pa.array(list(range(len(in_memory_pa_table))))
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
    # add suffix to avoid error due to duplicate column names
    concatenated_table = concat_tables(
        [add_suffix_to_column_names(table, i) for i, table in enumerate(tables)], axis=1
    )
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


def test_cast_integer_array_to_features():
    arr = pa.array([[0, 1]])
    assert cast_array_to_feature(arr, Sequence(Value("string"))).type == pa.list_(pa.string())
    assert cast_array_to_feature(arr, Sequence(Value("string")), allow_decimal_to_str=False).type == pa.list_(
        pa.string()
    )
    with pytest.raises(TypeError):
        cast_array_to_feature(arr, Sequence(Value("string")), allow_primitive_to_str=False)


def test_cast_float_array_to_features():
    arr = pa.array([[0.0, 1.0]])
    assert cast_array_to_feature(arr, Sequence(Value("string"))).type == pa.list_(pa.string())
    assert cast_array_to_feature(arr, Sequence(Value("string")), allow_decimal_to_str=False).type == pa.list_(
        pa.string()
    )
    with pytest.raises(TypeError):
        cast_array_to_feature(arr, Sequence(Value("string")), allow_primitive_to_str=False)


def test_cast_boolean_array_to_features():
    arr = pa.array([[False, True]])
    assert cast_array_to_feature(arr, Sequence(Value("string"))).type == pa.list_(pa.string())
    assert cast_array_to_feature(arr, Sequence(Value("string")), allow_decimal_to_str=False).type == pa.list_(
        pa.string()
    )
    with pytest.raises(TypeError):
        cast_array_to_feature(arr, Sequence(Value("string")), allow_primitive_to_str=False)


def test_cast_decimal_array_to_features():
    arr = pa.array([[Decimal(0), Decimal(1)]])
    assert cast_array_to_feature(arr, Sequence(Value("string"))).type == pa.list_(pa.string())
    assert cast_array_to_feature(arr, Sequence(Value("string")), allow_primitive_to_str=False).type == pa.list_(
        pa.string()
    )
    with pytest.raises(TypeError):
        cast_array_to_feature(arr, Sequence(Value("string")), allow_decimal_to_str=False)


@pytest.mark.parametrize(
    "array_list, expected_list",
    [
        ([{"age": 25}, {"age": 63}], [{"age": 25, "name": None}, {"age": 63, "name": None}]),
        ([{}, {}], [{"age": None, "name": None}, {"age": None, "name": None}]),  # completely empty struct
    ],
)
def test_cast_array_to_feature_with_struct_with_missing_fields(array_list, expected_list):
    arr = pa.array(array_list)
    feature = {"age": Value("int32"), "name": Value("string")}
    cast_array = cast_array_to_feature(arr, feature)
    assert cast_array.type == pa.struct({"age": pa.int32(), "name": pa.string()})
    assert cast_array.to_pylist() == expected_list


def test_cast_array_to_features_nested():
    arr = pa.array([[{"foo": [0]}]])
    assert cast_array_to_feature(arr, [{"foo": Sequence(Value("string"))}]).type == pa.list_(
        pa.struct({"foo": pa.list_(pa.string())})
    )


def test_cast_array_to_features_to_nested_with_no_fields():
    arr = pa.array([{}])
    assert cast_array_to_feature(arr, {}).type == pa.struct({})
    assert cast_array_to_feature(arr, {}).to_pylist() == arr.to_pylist()


def test_cast_array_to_features_nested_with_nulls():
    # same type
    arr = pa.array([{"foo": [None, [0]]}], pa.struct({"foo": pa.list_(pa.list_(pa.int64()))}))
    casted_array = cast_array_to_feature(arr, {"foo": [[Value("int64")]]})
    assert casted_array.type == pa.struct({"foo": pa.list_(pa.list_(pa.int64()))})
    assert casted_array.to_pylist() == arr.to_pylist()
    # different type
    arr = pa.array([{"foo": [None, [0]]}], pa.struct({"foo": pa.list_(pa.list_(pa.int64()))}))
    casted_array = cast_array_to_feature(arr, {"foo": [[Value("int32")]]})
    assert casted_array.type == pa.struct({"foo": pa.list_(pa.list_(pa.int32()))})
    assert casted_array.to_pylist() == [{"foo": [None, [0]]}]


def test_cast_array_to_features_to_null_type():
    # same type
    arr = pa.array([[None, None]])
    assert cast_array_to_feature(arr, Sequence(Value("null"))).type == pa.list_(pa.null())

    # different type
    arr = pa.array([[None, 1]])
    with pytest.raises(TypeError):
        cast_array_to_feature(arr, Sequence(Value("null")))


def test_cast_array_to_features_array_xd():
    # same storage type
    arr = pa.array([[[0, 1], [2, 3]], [[4, 5], [6, 7]]], pa.list_(pa.list_(pa.int32(), 2), 2))
    casted_array = cast_array_to_feature(arr, Array2D(shape=(2, 2), dtype="int32"))
    assert casted_array.type == Array2DExtensionType(shape=(2, 2), dtype="int32")
    # different storage type
    casted_array = cast_array_to_feature(arr, Array2D(shape=(2, 2), dtype="float32"))
    assert casted_array.type == Array2DExtensionType(shape=(2, 2), dtype="float32")


def test_cast_array_to_features_sequence_classlabel():
    arr = pa.array([[], [1], [0, 1]], pa.list_(pa.int64()))
    assert cast_array_to_feature(arr, Sequence(ClassLabel(names=["foo", "bar"]))).type == pa.list_(pa.int64())

    arr = pa.array([[], ["bar"], ["foo", "bar"]], pa.list_(pa.string()))
    assert cast_array_to_feature(arr, Sequence(ClassLabel(names=["foo", "bar"]))).type == pa.list_(pa.int64())

    # Test empty arrays
    arr = pa.array([[], []], pa.list_(pa.int64()))
    assert cast_array_to_feature(arr, Sequence(ClassLabel(names=["foo", "bar"]))).type == pa.list_(pa.int64())

    arr = pa.array([[], []], pa.list_(pa.string()))
    assert cast_array_to_feature(arr, Sequence(ClassLabel(names=["foo", "bar"]))).type == pa.list_(pa.int64())

    # Test invalid class labels
    arr = pa.array([[2]], pa.list_(pa.int64()))
    with pytest.raises(ValueError):
        assert cast_array_to_feature(arr, Sequence(ClassLabel(names=["foo", "bar"])))

    arr = pa.array([["baz"]], pa.list_(pa.string()))
    with pytest.raises(ValueError):
        assert cast_array_to_feature(arr, Sequence(ClassLabel(names=["foo", "bar"])))


@pytest.mark.parametrize(
    "arr",
    [
        pa.array([[0, 1, 2], [3, None, 5], None, [6, 7, 8], None], pa.list_(pa.int32(), 3)),
    ],
)
@pytest.mark.parametrize("slice", [None, slice(1, None), slice(-1), slice(1, 3), slice(2, 3), slice(1, 1)])
@pytest.mark.parametrize("target_value_feature", [Value("int64")])
def test_cast_fixed_size_list_array_to_features_sequence(arr, slice, target_value_feature):
    arr = arr if slice is None else arr[slice]
    # Fixed size list
    casted_array = cast_array_to_feature(arr, Sequence(target_value_feature, length=arr.type.list_size))
    assert casted_array.type == get_nested_type(Sequence(target_value_feature, length=arr.type.list_size))
    assert casted_array.to_pylist() == arr.to_pylist()
    with pytest.raises(TypeError):
        cast_array_to_feature(arr, Sequence(target_value_feature, length=arr.type.list_size + 1))
    # Variable size list
    casted_array = cast_array_to_feature(arr, Sequence(target_value_feature))
    assert casted_array.type == get_nested_type(Sequence(target_value_feature))
    assert casted_array.to_pylist() == arr.to_pylist()
    casted_array = cast_array_to_feature(arr, [target_value_feature])
    assert casted_array.type == get_nested_type([target_value_feature])
    assert casted_array.to_pylist() == arr.to_pylist()


@pytest.mark.parametrize(
    "arr",
    [
        pa.array([[0, 1, 2], [3, None, 5], None, [6, 7, 8], None], pa.list_(pa.int32())),
    ],
)
@pytest.mark.parametrize("slice", [None, slice(1, None), slice(-1), slice(1, 3), slice(2, 3), slice(1, 1)])
@pytest.mark.parametrize("target_value_feature", [Value("int64")])
def test_cast_list_array_to_features_sequence(arr, slice, target_value_feature):
    arr = arr if slice is None else arr[slice]
    # Variable size list
    casted_array = cast_array_to_feature(arr, Sequence(target_value_feature))
    assert casted_array.type == get_nested_type(Sequence(target_value_feature))
    assert casted_array.to_pylist() == arr.to_pylist()
    casted_array = cast_array_to_feature(arr, [target_value_feature])
    assert casted_array.type == get_nested_type([target_value_feature])
    assert casted_array.to_pylist() == arr.to_pylist()
    # Fixed size list
    list_size = arr.value_lengths().drop_null()[0].as_py() if arr.value_lengths().drop_null() else 2
    casted_array = cast_array_to_feature(arr, Sequence(target_value_feature, length=list_size))
    assert casted_array.type == get_nested_type(Sequence(target_value_feature, length=list_size))
    assert casted_array.to_pylist() == arr.to_pylist()


@pytest.mark.parametrize("sequence_feature_dtype", ["string", "int64"])
@pytest.mark.parametrize("from_list_type", ["list", "fixed_size_list", "large_list"])
@pytest.mark.parametrize("list_within_struct", [False, True])
def test_cast_array_to_feature_with_list_array_and_sequence_feature(
    list_within_struct, from_list_type, sequence_feature_dtype
):
    list_type = {
        "list": pa.list_,
        "fixed_size_list": partial(pa.list_, list_size=2),
        "large_list": pa.large_list,
    }
    primitive_type = {
        "string": pa.string(),
        "int64": pa.int64(),
    }
    to_type = "list"
    array_data = [0, 1]
    array_type = list_type[from_list_type](pa.int64())
    sequence_feature = Value(sequence_feature_dtype)
    expected_array_type = list_type[to_type](primitive_type[sequence_feature_dtype])
    if list_within_struct:
        array_data = {"col_1": array_data}
        array_type = pa.struct({"col_1": array_type})
        sequence_feature = {"col_1": sequence_feature}
        expected_array_type = pa.struct({"col_1": expected_array_type})
    feature = Sequence(sequence_feature)
    array = pa.array([array_data], type=array_type)
    cast_array = cast_array_to_feature(array, feature)
    assert cast_array.type == expected_array_type


@pytest.mark.parametrize("large_list_feature_value_type", ["string", "int64"])
@pytest.mark.parametrize("from_list_type", ["list", "fixed_size_list", "large_list"])
def test_cast_array_to_feature_with_list_array_and_large_list_feature(from_list_type, large_list_feature_value_type):
    list_type = {
        "list": pa.list_,
        "fixed_size_list": partial(pa.list_, list_size=2),
        "large_list": pa.large_list,
    }
    primitive_type = {
        "string": pa.string(),
        "int64": pa.int64(),
    }
    to_type = "large_list"
    array_data = [0, 1]
    array_type = list_type[from_list_type](pa.int64())
    large_list_feature_value = Value(large_list_feature_value_type)
    expected_array_type = list_type[to_type](primitive_type[large_list_feature_value_type])
    feature = LargeList(large_list_feature_value)
    array = pa.array([array_data], type=array_type)
    cast_array = cast_array_to_feature(array, feature)
    assert cast_array.type == expected_array_type


def test_cast_array_xd_to_features_sequence():
    arr = np.random.randint(0, 10, size=(8, 2, 3)).tolist()
    arr = Array2DExtensionType(shape=(2, 3), dtype="int64").wrap_array(pa.array(arr, pa.list_(pa.list_(pa.int64()))))
    arr = pa.ListArray.from_arrays([0, None, 4, 8], arr)
    # Variable size list
    casted_array = cast_array_to_feature(arr, Sequence(Array2D(shape=(2, 3), dtype="int32")))
    assert casted_array.type == get_nested_type(Sequence(Array2D(shape=(2, 3), dtype="int32")))
    assert casted_array.to_pylist() == arr.to_pylist()
    # Fixed size list
    casted_array = cast_array_to_feature(arr, Sequence(Array2D(shape=(2, 3), dtype="int32"), length=4))
    assert casted_array.type == get_nested_type(Sequence(Array2D(shape=(2, 3), dtype="int32"), length=4))
    assert casted_array.to_pylist() == arr.to_pylist()


def test_embed_array_storage(image_file):
    array = pa.array([{"bytes": None, "path": image_file}], type=Image.pa_type)
    embedded_images_array = embed_array_storage(array, Image())
    assert isinstance(embedded_images_array.to_pylist()[0]["path"], str)
    assert embedded_images_array.to_pylist()[0]["path"] == "test_image_rgb.jpg"
    assert isinstance(embedded_images_array.to_pylist()[0]["bytes"], bytes)


def test_embed_array_storage_nested(image_file):
    array = pa.array([[{"bytes": None, "path": image_file}]], type=pa.list_(Image.pa_type))
    embedded_images_array = embed_array_storage(array, [Image()])
    assert isinstance(embedded_images_array.to_pylist()[0][0]["path"], str)
    assert isinstance(embedded_images_array.to_pylist()[0][0]["bytes"], bytes)
    array = pa.array([{"foo": {"bytes": None, "path": image_file}}], type=pa.struct({"foo": Image.pa_type}))
    embedded_images_array = embed_array_storage(array, {"foo": Image()})
    assert isinstance(embedded_images_array.to_pylist()[0]["foo"]["path"], str)
    assert isinstance(embedded_images_array.to_pylist()[0]["foo"]["bytes"], bytes)


@pytest.mark.parametrize(
    "array, feature, expected_embedded_array_type",
    [
        (
            pa.array([[{"path": "image_path"}]], type=pa.list_(Image.pa_type)),
            [Image()],
            pa.types.is_list,
        ),
        (
            pa.array([[{"path": "image_path"}]], type=pa.large_list(Image.pa_type)),
            LargeList(Image()),
            pa.types.is_large_list,
        ),
        (
            pa.array([[{"path": "image_path"}]], type=pa.list_(Image.pa_type)),
            Sequence(Image()),
            pa.types.is_list,
        ),
    ],
)
def test_embed_array_storage_with_list_types(array, feature, expected_embedded_array_type, monkeypatch):
    mock_embed_storage = MagicMock(
        return_value=pa.StructArray.from_arrays(
            [pa.array([b"image_bytes"], type=pa.binary()), pa.array(["image_path"], type=pa.string())],
            ["bytes", "path"],
        )
    )
    monkeypatch.setattr(Image, "embed_storage", mock_embed_storage)
    embedded_images_array = embed_array_storage(array, feature)
    assert expected_embedded_array_type(embedded_images_array.type)
    assert embedded_images_array.to_pylist() == [[{"bytes": b"image_bytes", "path": "image_path"}]]


def test_embed_table_storage(image_file):
    features = Features({"image": Image()})
    table = table_cast(pa.table({"image": [image_file]}), features.arrow_schema)
    embedded_images_table = embed_table_storage(table)
    assert isinstance(embedded_images_table.to_pydict()["image"][0]["path"], str)
    assert isinstance(embedded_images_table.to_pydict()["image"][0]["bytes"], bytes)


@pytest.mark.parametrize(
    "table",
    [
        InMemoryTable(pa.table({"foo": range(10)})),
        InMemoryTable(pa.concat_tables([pa.table({"foo": range(0, 5)}), pa.table({"foo": range(5, 10)})])),
        InMemoryTable(pa.concat_tables([pa.table({"foo": [i]}) for i in range(10)])),
    ],
)
@pytest.mark.parametrize("batch_size", [1, 2, 3, 9, 10, 11, 20])
@pytest.mark.parametrize("drop_last_batch", [False, True])
def test_table_iter(table, batch_size, drop_last_batch):
    num_rows = len(table) if not drop_last_batch else len(table) // batch_size * batch_size
    num_batches = (num_rows // batch_size) + 1 if num_rows % batch_size else num_rows // batch_size
    subtables = list(table_iter(table, batch_size=batch_size, drop_last_batch=drop_last_batch))
    assert len(subtables) == num_batches
    if drop_last_batch:
        assert all(len(subtable) == batch_size for subtable in subtables)
    else:
        assert all(len(subtable) == batch_size for subtable in subtables[:-1])
        assert len(subtables[-1]) <= batch_size
    if num_rows > 0:
        reloaded = pa.concat_tables(subtables)
        assert table.slice(0, num_rows).to_pydict() == reloaded.to_pydict()


@pytest.mark.parametrize("to_type", ["list", "fixed_size_list", "large_list"])
@pytest.mark.parametrize("from_type", ["list", "fixed_size_list", "large_list"])
def test_array_cast(from_type, to_type):
    array_type = {
        "list": pa.list_(pa.int64()),
        "fixed_size_list": pa.list_(pa.int64(), 2),
        "large_list": pa.large_list(pa.int64()),
    }
    arr = pa.array([[0, 1]], type=array_type[from_type])
    cast_arr = array_cast(arr, array_type[to_type])
    assert cast_arr.type == array_type[to_type]
    assert cast_arr.values == arr.values


def test_cast_table_to_schema_with_missing_fields():
    table = pa.table({"age": [25, 63]})
    schema = pa.schema({"age": pa.int32(), "name": pa.string()})
    cast_table = cast_table_to_schema(table, schema)
    assert cast_table.schema == pa.schema({"age": pa.int32(), "name": pa.string()})
    assert cast_table.to_pydict() == {"age": [25, 63], "name": [None, None]}
