import copy
from functools import wraps
from typing import List, TypeVar, Union

import pyarrow as pa


def wraps_arrow_table_method(arrow_table_method):
    def wrapper(method):
        out = wraps(arrow_table_method)(method)
        out.__doc__ = out.__doc__.replace("pyarrow.Table", "Table")
        return out

    return wrapper


def in_memory_arrow_table_from_file(filename: str) -> pa.Table:
    in_memory_stream = pa.input_stream(filename)
    opened_stream = pa.ipc.open_stream(in_memory_stream)
    pa_table = opened_stream.read_all()
    return pa_table


def in_memory_arrow_table_from_buffer(buffer: pa.Buffer) -> pa.Table:
    stream = pa.BufferReader(buffer)
    opened_stream = pa.ipc.open_stream(stream)
    table = opened_stream.read_all()
    return table


def memory_mapped_arrow_table_from_file(filename: str) -> pa.Table:
    memory_mapped_stream = pa.memory_map(filename)
    opened_stream = pa.ipc.open_stream(memory_mapped_stream)
    pa_table = opened_stream.read_all()
    return pa_table


class Table:
    """
    Wraps a pyarrow Table by using composition.
    This is the base class for InMemoryTable, MemoryMappedTable and ConcatenationTable.

    It implements all the basic attributes/methods of the pyarrow Table class except
    the Table transforms: slice, filter, flatten, combine_chunks, cast, add_column,
    append_column, remove_column, set_column, rename_columns and drop.

    The implementation of these methods differ for the subclasses.
    """

    def __init__(self, table: pa.Table):
        self.table = table

    @wraps_arrow_table_method(pa.Table.validate)
    def validate(self, *args, **kwargs):
        return self.table.validate(*args, **kwargs)

    @wraps_arrow_table_method(pa.Table.equals)
    def equals(self, *args, **kwargs):
        args = tuple(arg.table if isinstance(arg, Table) else arg for arg in args)
        kwargs = {k: v.table if isinstance(v, Table) else v for k, v in kwargs}
        return self.table.equals(*args, **kwargs)

    @wraps_arrow_table_method(pa.Table.to_batches)
    def to_batches(self, *args, **kwargs):
        return self.table.to_batches(*args, **kwargs)

    @wraps_arrow_table_method(pa.Table.to_pydict)
    def to_pydict(self, *args, **kwargs):
        return self.table.to_pydict(*args, **kwargs)

    @wraps_arrow_table_method(pa.Table.to_pandas)
    def to_pandas(self, *args, **kwargs):
        return self.table.to_pandas(*args, **kwargs)

    def to_string(self, *args, **kwargs):
        return self.table.to_string(*args, **kwargs)

    @wraps_arrow_table_method(pa.Table.field)
    def field(self, *args, **kwargs):
        return self.table.field(*args, **kwargs)

    @wraps_arrow_table_method(pa.Table.column)
    def column(self, *args, **kwargs):
        return self.table.column(*args, **kwargs)

    @wraps_arrow_table_method(pa.Table.itercolumns)
    def itercolumns(self, *args, **kwargs):
        return self.table.itercolumns(*args, **kwargs)

    @property
    def schema(self):
        return self.table.schema

    @property
    def columns(self):
        return self.table.columns

    @property
    def num_columns(self):
        return self.table.num_columns

    @property
    def num_rows(self):
        return self.table.num_rows

    @property
    def shape(self):
        return self.table.shape

    @property
    def nbytes(self):
        return self.table.nbytes

    @property
    def column_names(self):
        return self.table.column_names

    def __getitem__(self, i):
        return self.table[i]

    def __len__(self):
        return len(self.table)

    def __repr__(self):
        return self.table.__repr__().replace("pyarrow.Table", self.__class__.__name__)

    def __str__(self):
        return self.table.__str__().replace("pyarrow.Table", self.__class__.__name__)

    @wraps_arrow_table_method(pa.Table.slice)
    def slice(self, *args, **kwargs):
        raise NotImplementedError()

    @wraps_arrow_table_method(pa.Table.filter)
    def filter(self, *args, **kwargs):
        raise NotImplementedError()

    @wraps_arrow_table_method(pa.Table.flatten)
    def flatten(self, *args, **kwargs):
        raise NotImplementedError()

    @wraps_arrow_table_method(pa.Table.combine_chunks)
    def combine_chunks(self, *args, **kwargs):
        raise NotImplementedError()

    @wraps_arrow_table_method(pa.Table.cast)
    def cast(self, *args, **kwargs):
        raise NotImplementedError()

    @wraps_arrow_table_method(pa.Table.add_column)
    def add_column(self, *args, **kwargs):
        raise NotImplementedError()

    @wraps_arrow_table_method(pa.Table.append_column)
    def append_column(self, *args, **kwargs):
        raise NotImplementedError()

    @wraps_arrow_table_method(pa.Table.remove_column)
    def remove_column(self, *args, **kwargs):
        raise NotImplementedError()

    @wraps_arrow_table_method(pa.Table.set_column)
    def set_column(self, *args, **kwargs):
        raise NotImplementedError()

    @wraps_arrow_table_method(pa.Table.rename_columns)
    def rename_columns(self, *args, **kwargs):
        raise NotImplementedError()

    @wraps_arrow_table_method(pa.Table.drop)
    def drop(self, *args, **kwargs):
        raise NotImplementedError()


class TableBlock(Table):
    """
    TableBlock is the allowed class inside a ConcanetationTable.
    Only MemoryMappedTable and InMemoryTable are TableBlock.
    This is because we don't want a ConcanetationTable made out of other ConcanetationTables.
    """

    pass


class InMemoryTable(TableBlock):
    """
    Wraps a pyarrow Table using composition.
    The table is said in-memory so pickling it does copy all the data using memory.
    Its implementation is simple and uses the underlying pyarrow Table methods directly.
    """

    @classmethod
    def from_file(cls, filename: str):
        table = in_memory_arrow_table_from_file(filename)
        return cls(table)

    @classmethod
    def from_buffer(cls, buffer: pa.Buffer):
        table = in_memory_arrow_table_from_buffer(buffer)
        return cls(table)

    @wraps_arrow_table_method(pa.Table.from_pandas)
    @staticmethod
    def from_pandas(*args, **kwargs):
        return InMemoryTable(pa.Table.from_pandas(*args, **kwargs))

    @wraps_arrow_table_method(pa.Table.from_arrays)
    @staticmethod
    def from_arrays(*args, **kwargs):
        return InMemoryTable(pa.Table.from_arrays(*args, **kwargs))

    @wraps_arrow_table_method(pa.Table.from_pydict)
    @staticmethod
    def from_pydict(*args, **kwargs):
        return InMemoryTable(pa.Table.from_pydict(*args, **kwargs))

    @wraps_arrow_table_method(pa.Table.from_batches)
    @staticmethod
    def from_batches(*args, **kwargs):
        return InMemoryTable(pa.Table.from_batches(*args, **kwargs))

    @wraps_arrow_table_method(pa.Table.slice)
    def slice(self, *args, **kwargs):
        return InMemoryTable(self.table.slice(*args, **kwargs))

    @wraps_arrow_table_method(pa.Table.filter)
    def filter(self, *args, **kwargs):
        return InMemoryTable(self.table.filter(*args, **kwargs))

    @wraps_arrow_table_method(pa.Table.flatten)
    def flatten(self, *args, **kwargs):
        return InMemoryTable(self.table.flatten(*args, **kwargs))

    @wraps_arrow_table_method(pa.Table.combine_chunks)
    def combine_chunks(self, *args, **kwargs):
        return InMemoryTable(self.table.combine_chunks(*args, **kwargs))

    @wraps_arrow_table_method(pa.Table.cast)
    def cast(self, *args, **kwargs):
        return InMemoryTable(self.table.cast(*args, **kwargs))

    @wraps_arrow_table_method(pa.Table.add_column)
    def add_column(self, *args, **kwargs):
        return InMemoryTable(self.table.add_column(*args, **kwargs))

    @wraps_arrow_table_method(pa.Table.append_column)
    def append_column(self, *args, **kwargs):
        return InMemoryTable(self.table.append_column(*args, **kwargs))

    @wraps_arrow_table_method(pa.Table.remove_column)
    def remove_column(self, *args, **kwargs):
        return InMemoryTable(self.table.remove_column(*args, **kwargs))

    @wraps_arrow_table_method(pa.Table.set_column)
    def set_column(self, *args, **kwargs):
        return InMemoryTable(self.table.set_column(*args, **kwargs))

    @wraps_arrow_table_method(pa.Table.rename_columns)
    def rename_columns(self, *args, **kwargs):
        return InMemoryTable(self.table.rename_columns(*args, **kwargs))

    @wraps_arrow_table_method(pa.Table.drop)
    def drop(self, *args, **kwargs):
        return InMemoryTable(self.table.drop(*args, **kwargs))


class MemoryMappedTable(TableBlock):
    """
    Wraps a pyarrow Table using composition.
    The table is said memory mapped so pickling it doesn't copy the data into memory.
    Instead, only the path to the memory mapped arrow file is pickled, as well as the list
    of transforms to "replay" when reloading the table from the disk.

    Its implementation requires to store an history of all the transforms that were applied
    to the underlying pyarrow Table, so that they can be "replayed" when reloading the Table
    from the disk.
    """

    def __init__(self, table: pa.Table, path: str, replay=None):
        super().__init__(table)
        self.path = path
        self.replay = replay if replay is not None else []

    @classmethod
    def from_file(cls, filename: str, replay=None):
        table = memory_mapped_arrow_table_from_file(filename)
        table = cls._apply_replay(table, replay)
        return cls(table, filename, replay)

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("table")
        return state

    def __setstate__(self, state):
        state = state.copy()
        table = memory_mapped_arrow_table_from_file(state["path"])
        table = self._apply_replay(table, state["replay"])
        state["table"] = table
        self.__dict__ = state

    @staticmethod
    def _apply_replay(table: pa.Table, replay=None):
        if replay is not None:
            for name, args, kwargs in replay:
                table = getattr(table, name)(*args, **kwargs)
        return table

    def _merge_replay(self, new_replay):
        replay = copy.deepcopy(self.replay)
        replay.extend(new_replay)
        return replay

    @wraps_arrow_table_method(pa.Table.slice)
    def slice(self, *args, **kwargs):
        replay = [("slice", copy.deepcopy(args), copy.deepcopy(kwargs))]
        replay = self._merge_replay(replay)
        return MemoryMappedTable(self.table.slice(*args, **kwargs), self.path, replay)

    @wraps_arrow_table_method(pa.Table.filter)
    def filter(self, *args, **kwargs):
        replay = [("filter", copy.deepcopy(args), copy.deepcopy(kwargs))]
        replay = self._merge_replay(replay)
        return MemoryMappedTable(self.table.filter(*args, **kwargs), self.path, replay)

    @wraps_arrow_table_method(pa.Table.flatten)
    def flatten(self, *args, **kwargs):
        replay = [("flatten", copy.deepcopy(args), copy.deepcopy(kwargs))]
        replay = self._merge_replay(replay)
        return MemoryMappedTable(self.table.flatten(*args, **kwargs), self.path, replay)

    @wraps_arrow_table_method(pa.Table.combine_chunks)
    def combine_chunks(self, *args, **kwargs):
        replay = [("combine_chunks", copy.deepcopy(args), copy.deepcopy(kwargs))]
        replay = self._merge_replay(replay)
        return MemoryMappedTable(self.table.combine_chunks(*args, **kwargs), self.path, replay)

    @wraps_arrow_table_method(pa.Table.cast)
    def cast(self, *args, **kwargs):
        replay = [("cast", copy.deepcopy(args), copy.deepcopy(kwargs))]
        replay = self._merge_replay(replay)
        return MemoryMappedTable(self.table.cast(*args, **kwargs), self.path, replay)

    @wraps_arrow_table_method(pa.Table.add_column)
    def add_column(self, *args, **kwargs):
        replay = [("add_column", copy.deepcopy(args), copy.deepcopy(kwargs))]
        replay = self._merge_replay(replay)
        return MemoryMappedTable(self.table.add_column(*args, **kwargs), self.path, replay)

    @wraps_arrow_table_method(pa.Table.append_column)
    def append_column(self, *args, **kwargs):
        replay = [("append_column", copy.deepcopy(args), copy.deepcopy(kwargs))]
        replay = self._merge_replay(replay)
        return MemoryMappedTable(self.table.append_column(*args, **kwargs), self.path, replay)

    @wraps_arrow_table_method(pa.Table.remove_column)
    def remove_column(self, *args, **kwargs):
        replay = [("remove_column", copy.deepcopy(args), copy.deepcopy(kwargs))]
        replay = self._merge_replay(replay)
        return MemoryMappedTable(self.table.remove_column(*args, **kwargs), self.path, replay)

    @wraps_arrow_table_method(pa.Table.set_column)
    def set_column(self, *args, **kwargs):
        replay = [("set_column", copy.deepcopy(args), copy.deepcopy(kwargs))]
        replay = self._merge_replay(replay)
        return MemoryMappedTable(self.table.set_column(*args, **kwargs), self.path, replay)

    @wraps_arrow_table_method(pa.Table.rename_columns)
    def rename_columns(self, *args, **kwargs):
        replay = [("rename_columns", copy.deepcopy(args), copy.deepcopy(kwargs))]
        replay = self._merge_replay(replay)
        return MemoryMappedTable(self.table.rename_columns(*args, **kwargs), self.path, replay)

    @wraps_arrow_table_method(pa.Table.drop)
    def drop(self, *args, **kwargs):
        replay = [("drop", copy.deepcopy(args), copy.deepcopy(kwargs))]
        replay = self._merge_replay(replay)
        return MemoryMappedTable(self.table.drop(*args, **kwargs), self.path, replay)


BlockPart = TypeVar("BlockPart", TableBlock, List[TableBlock], List[List[TableBlock]])


class ConcatenationTable(Table):
    """
    Wraps a pyarrow Table using composition.
    The table comes from the concatenation of several tables.

    The underlying tables are called "blocks" and can be either InMemoryTable
    or MemoryMappedTable objects.
    This allows to combine tables that come from memory or that are memory mapped.
    When a ConcatenationTable is pickled, then each block is pickled:
    - the InMemoryTable objects are pickled by copying all the data in memory;
    - the MemoryMappedTable objects are pickled without copying the data into memory.
    Instead, only the path to the memory mapped arrow file is pickled, as well as the list
    of transforms to "replay" when reloading the table from the disk.

    Its implementation requires to store each block separately.
    The ``blocks`` attributes stores a list of list of blocks.
    The first axis concatenates the tables along the axis 0 (it appends rows),
    while the second axis concatenates tables along the axis 1 (it appends columns).

    You can access the fully combined table by accessing the ConcatenationTable.table attribute,
    and the blocks by accessing the ConcatenationTable.blocks attribute.
    """

    def __init__(self, table: pa.Table, blocks: List[List[TableBlock]]):
        super().__init__(table)
        self.blocks = blocks
        assert all(isinstance(subtable, TableBlock) for subtables in blocks for subtable in subtables)

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("table")
        return state

    def __setstate__(self, state):
        state = state.copy()
        state["table"] = ConcatenationTable.from_blocks(state["blocks"]).table
        self.__dict__ = state

    @staticmethod
    def from_blocks(blocks_part: BlockPart):
        if isinstance(blocks_part, Table):
            table = blocks_part
            return ConcatenationTable(table.table, [[table]])
        elif isinstance(blocks_part[0], Table):
            table = pa.concat_tables([t.table for t in blocks_part])
            blocks = [[t] for t in blocks_part]
            return ConcatenationTable(table, blocks)
        else:
            tables_to_concat = []
            blocks = blocks_part
            for i, tables in enumerate(blocks):
                for j, table in enumerate(tables):
                    if j == 0:
                        combined_table = table.table
                    else:
                        for name, col in zip(table.column_names, table.columns):
                            combined_table = combined_table.append_column(name, col)
                if i > 0 and combined_table.schema != tables_to_concat[0].schema:
                    # re-order the columns to make the schema match and concat the tables
                    names = tables_to_concat[0].schema.names
                    arrays = [combined_table[name] for name in names]
                    combined_table = pa.Table.from_arrays(arrays, names=names)
                tables_to_concat.append(combined_table)
            table = pa.concat_tables(tables_to_concat)
            return ConcatenationTable(table, blocks)

    @staticmethod
    def from_tables(tables: List[Union[pa.Table, Table]]) -> "ConcatenationTable":
        blocks = []
        for table in tables:
            if isinstance(table, pa.Table):
                blocks.append([InMemoryTable(table)])
            elif isinstance(table, ConcatenationTable):
                blocks.extend(copy.deepcopy(table.blocks))
            else:
                blocks.append([table])
        return ConcatenationTable.from_blocks(blocks)

    @property
    def _slices(self):
        start = 0
        for tables in self.blocks:
            yield (start, start + len(tables[0]))
            start += len(tables[0])

    @wraps_arrow_table_method(pa.Table.slice)
    def slice(self, offset=0, length=None):
        table = self.table.slice(offset, length=length)
        length = length if length is not None else self.num_rows - offset
        blocks = []
        for tables in self.blocks:
            n_rows = len(tables[0])
            if length == 0:
                break
            elif n_rows <= offset:
                offset = offset - n_rows
            elif n_rows <= offset + length:
                blocks.append([t.slice(offset) for t in tables])
                length, offset = length + offset - n_rows, 0
            else:
                blocks.append([t.slice(offset, length) for t in tables])
                length, offset = 0, 0
        return ConcatenationTable(table, blocks)

    @wraps_arrow_table_method(pa.Table.filter)
    def filter(self, mask, *args, **kwargs):
        table = self.table.filter(mask, *args, **kwargs)
        blocks = []
        for (start, end), tables in zip(self._slices, self.blocks):
            submask = mask.slice(start, end)
            blocks.append([t.filter(submask, *args, **kwargs) for t in tables])
        return ConcatenationTable(table, blocks)

    @wraps_arrow_table_method(pa.Table.flatten)
    def flatten(self, *args, **kwargs):
        table = self.table.flatten(*args, **kwargs)
        blocks = []
        for tables in self.blocks:
            blocks.append([t.flatten(*args, **kwargs) for t in tables])
        return ConcatenationTable(table, blocks)

    @wraps_arrow_table_method(pa.Table.combine_chunks)
    def combine_chunks(self, *args, **kwargs):
        table = self.table.combine_chunks(*args, **kwargs)
        blocks = []
        for tables in self.blocks:
            blocks.append([t.combine_chunks(*args, **kwargs) for t in tables])
        return ConcatenationTable(table, blocks)

    @wraps_arrow_table_method(pa.Table.cast)
    def cast(self, target_schema, *args, **kwargs):
        table = self.table.cast(target_schema, *args, **kwargs)
        blocks = []
        for subtables in self.blocks:
            new_tables = []
            for subtable in subtables:
                subschema = pa.schema(
                    {
                        name: type
                        for (type, name) in zip(target_schema.types, target_schema.names)
                        if name in subtable.schema.names
                    }
                )
                new_tables.append(subtable.cast(subschema, *args, **kwargs))
            blocks.append(new_tables)
        return ConcatenationTable(table, blocks)

    @wraps_arrow_table_method(pa.Table.add_column)
    def add_column(self, *args, **kwargs):
        raise NotImplementedError()

    @wraps_arrow_table_method(pa.Table.append_column)
    def append_column(self, *args, **kwargs):
        raise NotImplementedError()

    @wraps_arrow_table_method(pa.Table.remove_column)
    def remove_column(self, i, *args, **kwargs):
        table = self.table.remove_column(i, *args, **kwargs)
        name = self.table.column_names[i]
        blocks = []
        for tables in self.blocks:
            blocks.append(
                [
                    t.remove_column(t.column_names.index(name), *args, **kwargs) if name in t.column_names else t
                    for t in tables
                ]
            )
        return ConcatenationTable(table, blocks)

    @wraps_arrow_table_method(pa.Table.set_column)
    def set_column(self, *args, **kwargs):
        raise NotImplementedError()

    @wraps_arrow_table_method(pa.Table.rename_columns)
    def rename_columns(self, names, *args, **kwargs):
        table = self.table.rename_columns(names, *args, **kwargs)
        names = dict(zip(self.table.column_names, names))
        blocks = []
        for tables in self.blocks:
            blocks.append(
                [t.rename_columns([names[name] for name in t.column_names], *args, **kwargs) for t in tables]
            )
        return ConcatenationTable(table, blocks)

    @wraps_arrow_table_method(pa.Table.drop)
    def drop(self, columns, *args, **kwargs):
        table = self.table.drop(columns)
        blocks = []
        for tables in self.blocks:
            blocks.append([t.drop([c for c in columns if c in t.column_names], *args, **kwargs) for t in tables])
        return ConcatenationTable(table, blocks)


def concat_tables(tables: List[Union[pa.Table, Table]]) -> ConcatenationTable:
    return ConcatenationTable.from_tables(tables)


def list_table_cache_files(table: Union[pa.Table, Table]) -> List[str]:
    if isinstance(table, ConcatenationTable):
        cache_files = []
        for subtables in table.blocks:
            for subtable in subtables:
                cache_files += list_table_cache_files(subtable)
        return cache_files
    elif isinstance(table, MemoryMappedTable):
        return [table.path]
    else:
        return []
