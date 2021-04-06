import copy
import os
import tempfile
from functools import wraps
from itertools import groupby
from typing import List, Optional, Tuple, TypeVar, Union

import pyarrow as pa

from . import config
from .utils.logging import get_logger


logger = get_logger(__name__)


def inject_arrow_table_documentation(arrow_table_method):
    def wrapper(method):
        out = wraps(arrow_table_method)(method)
        out.__doc__ = out.__doc__.replace("pyarrow.Table", "Table")
        return out

    return wrapper


def _in_memory_arrow_table_from_file(filename: str) -> pa.Table:
    in_memory_stream = pa.input_stream(filename)
    opened_stream = pa.ipc.open_stream(in_memory_stream)
    pa_table = opened_stream.read_all()
    return pa_table


def _in_memory_arrow_table_from_buffer(buffer: pa.Buffer) -> pa.Table:
    stream = pa.BufferReader(buffer)
    opened_stream = pa.ipc.open_stream(stream)
    table = opened_stream.read_all()
    return table


def _memory_mapped_arrow_table_from_file(filename: str) -> pa.Table:
    memory_mapped_stream = pa.memory_map(filename)
    opened_stream = pa.ipc.open_stream(memory_mapped_stream)
    pa_table = opened_stream.read_all()
    return pa_table


def _write_table_to_file(table: pa.Table, filename: str, writer_batch_size: Optional[int] = None) -> int:
    with open(filename, "wb") as sink:
        writer = pa.RecordBatchStreamWriter(sink=sink, schema=table.schema)
        batches: List[pa.RecordBatch] = table.to_batches()
        for batch in batches:
            writer.write_batch(batch)
        writer.close()
        return sum(batch.nbytes for batch in batches)


class Table:
    """
    Wraps a pyarrow Table by using composition.
    This is the base class for InMemoryTable, MemoryMappedTable and ConcatenationTable.

    It implements all the basic attributes/methods of the pyarrow Table class except
    the Table transforms: slice, filter, flatten, combine_chunks, cast, add_column,
    append_column, remove_column, set_column, rename_columns and drop.

    The implementation of these methods differs for the subclasses.
    """

    def __init__(self, table: pa.Table):
        self.table = table

    def __getstate__(self):
        state = self.__dict__.copy()
        # We can't pickle objects that are bigger than 4GiB, or it causes OverflowError
        # So we write the table on disk instead
        if self.table.nbytes >= config.MAX_TABLE_NBYTES_FOR_PICKLING:
            table = state.pop("table")
            with tempfile.NamedTemporaryFile("wb", delete=False, suffix=".arrow") as tmp_file:
                filename = tmp_file.name
                logger.debug(
                    f"Attempting to pickle a table bigger than 4GiB. Writing it on the disk instead at {filename}"
                )
                _write_table_to_file(table=table, filename=filename)
                state["path"] = filename
                return state
        else:
            return state

    def __setstate__(self, state):
        state = state.copy()
        if "path" in state:
            filename = state.pop("path")
            logger.debug(f"Unpickling a big table from the disk at {filename}")
            state["table"] = _in_memory_arrow_table_from_file(filename)
            logger.debug(f"Removing temporary table file at {filename}")
            os.remove(filename)
        self.__dict__ = state

    @inject_arrow_table_documentation(pa.Table.validate)
    def validate(self, *args, **kwargs):
        return self.table.validate(*args, **kwargs)

    @inject_arrow_table_documentation(pa.Table.equals)
    def equals(self, *args, **kwargs):
        args = tuple(arg.table if isinstance(arg, Table) else arg for arg in args)
        kwargs = {k: v.table if isinstance(v, Table) else v for k, v in kwargs}
        return self.table.equals(*args, **kwargs)

    @inject_arrow_table_documentation(pa.Table.to_batches)
    def to_batches(self, *args, **kwargs):
        return self.table.to_batches(*args, **kwargs)

    @inject_arrow_table_documentation(pa.Table.to_pydict)
    def to_pydict(self, *args, **kwargs):
        return self.table.to_pydict(*args, **kwargs)

    @inject_arrow_table_documentation(pa.Table.to_pandas)
    def to_pandas(self, *args, **kwargs):
        return self.table.to_pandas(*args, **kwargs)

    def to_string(self, *args, **kwargs):
        return self.table.to_string(*args, **kwargs)

    @inject_arrow_table_documentation(pa.Table.field)
    def field(self, *args, **kwargs):
        return self.table.field(*args, **kwargs)

    @inject_arrow_table_documentation(pa.Table.column)
    def column(self, *args, **kwargs):
        return self.table.column(*args, **kwargs)

    @inject_arrow_table_documentation(pa.Table.itercolumns)
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

    def __eq__(self, other):
        return self.equals(other)

    def __getitem__(self, i):
        return self.table[i]

    def __len__(self):
        return len(self.table)

    def __repr__(self):
        return self.table.__repr__().replace("pyarrow.Table", self.__class__.__name__)

    def __str__(self):
        return self.table.__str__().replace("pyarrow.Table", self.__class__.__name__)

    @inject_arrow_table_documentation(pa.Table.slice)
    def slice(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.filter)
    def filter(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.flatten)
    def flatten(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.combine_chunks)
    def combine_chunks(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.cast)
    def cast(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.add_column)
    def add_column(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.append_column)
    def append_column(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.remove_column)
    def remove_column(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.set_column)
    def set_column(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.rename_columns)
    def rename_columns(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.drop)
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
    The table is said in-memory when it is loaded into the user's RAM.

    Pickling it does copy all the data using memory.
    Its implementation is simple and uses the underlying pyarrow Table methods directly.

    This is different from the MemoryMapped table, for which pickling doesn't copy all the
    data in memory. For a MemoryMapped, unpickling instead reloads the table from the disk.

    InMemoryTable must be used when data fit in memory, while MemoryMapped are reserved for
    data bigger than memory or when you want the memory footprint of your application to
    stay low.
    """

    @classmethod
    def from_file(cls, filename: str):
        table = _in_memory_arrow_table_from_file(filename)
        return cls(table)

    @classmethod
    def from_buffer(cls, buffer: pa.Buffer):
        table = _in_memory_arrow_table_from_buffer(buffer)
        return cls(table)

    @inject_arrow_table_documentation(pa.Table.from_pandas)
    @classmethod
    def from_pandas(cls, *args, **kwargs):
        return cls(pa.Table.from_pandas(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.from_arrays)
    @classmethod
    def from_arrays(cls, *args, **kwargs):
        return cls(pa.Table.from_arrays(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.from_pydict)
    @classmethod
    def from_pydict(cls, *args, **kwargs):
        return cls(pa.Table.from_pydict(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.from_batches)
    @classmethod
    def from_batches(cls, *args, **kwargs):
        return cls(pa.Table.from_batches(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.slice)
    def slice(self, *args, **kwargs):
        return InMemoryTable(self.table.slice(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.filter)
    def filter(self, *args, **kwargs):
        return InMemoryTable(self.table.filter(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.flatten)
    def flatten(self, *args, **kwargs):
        return InMemoryTable(self.table.flatten(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.combine_chunks)
    def combine_chunks(self, *args, **kwargs):
        return InMemoryTable(self.table.combine_chunks(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.cast)
    def cast(self, *args, **kwargs):
        return InMemoryTable(self.table.cast(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.add_column)
    def add_column(self, *args, **kwargs):
        return InMemoryTable(self.table.add_column(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.append_column)
    def append_column(self, *args, **kwargs):
        return InMemoryTable(self.table.append_column(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.remove_column)
    def remove_column(self, *args, **kwargs):
        return InMemoryTable(self.table.remove_column(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.set_column)
    def set_column(self, *args, **kwargs):
        return InMemoryTable(self.table.set_column(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.rename_columns)
    def rename_columns(self, *args, **kwargs):
        return InMemoryTable(self.table.rename_columns(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.drop)
    def drop(self, *args, **kwargs):
        return InMemoryTable(self.table.drop(*args, **kwargs))


# The MemoryMappedTable needs replays to properly reload tables from the disk
Replay = Tuple[str, tuple, dict]


class MemoryMappedTable(TableBlock):
    """
    The table is said memory mapped when it doesn't use the user's RAM but loads the data
    from the disk instead.

    Pickling it doesn't copy the data into memory.
    Instead, only the path to the memory mapped arrow file is pickled, as well as the list
    of transforms to "replay" when reloading the table from the disk.

    Its implementation requires to store an history of all the transforms that were applied
    to the underlying pyarrow Table, so that they can be "replayed" when reloading the Table
    from the disk.

    This is different from the InMemoryTable table, for which pickling does copy all the
    data in memory.

    InMemoryTable must be used when data fit in memory, while MemoryMapped are reserved for
    data bigger than memory or when you want the memory footprint of your application to
    stay low.
    """

    def __init__(self, table: pa.Table, path: str, replays: Optional[List[Replay]] = None):
        super().__init__(table)
        self.path = path
        self.replays: List[Replay] = replays if replays is not None else []

    @classmethod
    def from_file(cls, filename: str, replays=None):
        table = _memory_mapped_arrow_table_from_file(filename)
        table = cls._apply_replays(table, replays)
        return cls(table, filename, replays)

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("table")
        return state

    def __setstate__(self, state):
        state = state.copy()
        table = _memory_mapped_arrow_table_from_file(state["path"])
        table = self._apply_replays(table, state["replays"])
        state["table"] = table
        self.__dict__ = state

    @staticmethod
    def _apply_replays(table: pa.Table, replays: Optional[List[Replay]] = None) -> pa.Table:
        if replays is not None:
            for name, args, kwargs in replays:
                table = getattr(table, name)(*args, **kwargs)
        return table

    def _append_replay(self, replay: Replay) -> List[Replay]:
        replays = copy.deepcopy(self.replays)
        replays.append(replay)
        return replays

    @inject_arrow_table_documentation(pa.Table.slice)
    def slice(self, *args, **kwargs):
        replay = ("slice", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.slice(*args, **kwargs), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.filter)
    def filter(self, *args, **kwargs):
        replay = ("filter", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.filter(*args, **kwargs), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.flatten)
    def flatten(self, *args, **kwargs):
        replay = ("flatten", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.flatten(*args, **kwargs), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.combine_chunks)
    def combine_chunks(self, *args, **kwargs):
        replay = ("combine_chunks", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.combine_chunks(*args, **kwargs), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.cast)
    def cast(self, *args, **kwargs):
        replay = ("cast", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.cast(*args, **kwargs), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.add_column)
    def add_column(self, *args, **kwargs):
        replay = ("add_column", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.add_column(*args, **kwargs), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.append_column)
    def append_column(self, *args, **kwargs):
        replay = ("append_column", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.append_column(*args, **kwargs), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.remove_column)
    def remove_column(self, *args, **kwargs):
        replay = ("remove_column", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.remove_column(*args, **kwargs), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.set_column)
    def set_column(self, *args, **kwargs):
        replay = ("set_column", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.set_column(*args, **kwargs), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.rename_columns)
    def rename_columns(self, *args, **kwargs):
        replay = ("rename_columns", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.rename_columns(*args, **kwargs), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.drop)
    def drop(self, *args, **kwargs):
        replay = ("drop", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.drop(*args, **kwargs), self.path, replays)


# A ConcatenationTable is the concatenation of several tables.
# The ``blocks`` attributes stores a list of list of blocks.
# The first axis concatenates the tables along the axis 0 (it appends rows),
# while the second axis concatenates tables along the axis 1 (it appends columns).
TableBlockContainer = TypeVar("TableBlockContainer", TableBlock, List[TableBlock], List[List[TableBlock]])


class ConcatenationTable(Table):
    """
    The table comes from the concatenation of several tables called blocks.
    It enables concatenation on both axis 0 (append rows) and axis 1 (append columns).

    The underlying tables are called "blocks" and can be either InMemoryTable
    or MemoryMappedTable objects.
    This allows to combine tables that come from memory or that are memory mapped.
    When a ConcatenationTable is pickled, then each block is pickled:
    - the InMemoryTable objects are pickled by copying all the data in memory;
    - the MemoryMappedTable objects are pickled without copying the data into memory.
    Instead, only the path to the memory mapped arrow file is pickled, as well as the list
    of transforms to "replays" when reloading the table from the disk.

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
        # Check that all the blocks have the right type.
        # Only InMemoryTable and MemoryMappedTable are allowed.
        for subtables in blocks:
            for subtable in subtables:
                if not isinstance(subtable, TableBlock):
                    raise TypeError(
                        "The blocks of a ConcatenationTable must be InMemoryTable or MemoryMappedTable objects"
                        f", but got {subtable}."
                    )

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("table")
        return state

    def __setstate__(self, state):
        state = state.copy()
        state["table"] = self._concat_blocks_horizontally_and_vertically(state["blocks"])
        self.__dict__ = state

    @staticmethod
    def _concat_blocks(blocks: List[TableBlock], axis: int = 0) -> pa.Table:
        if axis == 0:
            return pa.concat_tables([t.table for t in blocks])
        elif axis == 1:
            for i, table in enumerate(blocks):
                if i == 0:
                    combined_table = table.table
                else:
                    for name, col in zip(table.column_names, table.columns):
                        combined_table = combined_table.append_column(name, col)
            return combined_table
        else:
            raise ValueError("'axis' must be either 0 or 1")

    @classmethod
    def _concat_blocks_horizontally_and_vertically(cls, blocks: List[List[TableBlock]]) -> pa.Table:
        tables_to_concat_vertically = []
        for i, tables in enumerate(blocks):
            if not tables:
                continue
            combined_table = cls._concat_blocks(tables, axis=1)
            if i > 0 and combined_table.schema != tables_to_concat_vertically[0].schema:
                # re-order the columns to make the schema match and concat the tables
                names = tables_to_concat_vertically[0].schema.names
                arrays = [combined_table[name] for name in names]
                combined_table = pa.Table.from_arrays(arrays, names=names)
            tables_to_concat_vertically.append(combined_table)
        return pa.concat_tables(tables_to_concat_vertically)

    @classmethod
    def _merge_blocks(cls, blocks: TableBlockContainer, axis: Optional[int] = None):
        if axis is not None:
            merged_blocks = []
            for is_in_memory, block_group in groupby(blocks, key=lambda x: isinstance(x, InMemoryTable)):
                if is_in_memory:
                    block_group = [InMemoryTable(cls._concat_blocks(block_group, axis=axis))]
                merged_blocks += list(block_group)
        else:  # both
            merged_blocks = [cls._merge_blocks(row_block, axis=1) for row_block in blocks]
            if all(len(row_block) == 1 for row_block in merged_blocks):
                merged_blocks = cls._merge_blocks(
                    [block for row_block in merged_blocks for block in row_block], axis=0
                )
        return merged_blocks

    @classmethod
    def _consolidate_blocks(cls, blocks: TableBlockContainer):
        if isinstance(blocks, TableBlock):
            return blocks
        elif isinstance(blocks[0], TableBlock):
            return cls._merge_blocks(blocks, axis=0)
        else:
            return cls._merge_blocks(blocks)

    @classmethod
    def from_blocks(cls, blocks: TableBlockContainer) -> "ConcatenationTable":
        if isinstance(blocks, TableBlock):
            table = blocks
            return cls(table.table, [[table]])
        elif isinstance(blocks[0], TableBlock):
            blocks = cls._consolidate_blocks(blocks, axis=0)
            table = cls._concat_blocks(blocks, axis=0)
            blocks = [[t] for t in blocks]
            return cls(table, blocks)
        else:
            # blocks = cls._consolidate_blocks(blocks)
            table = cls._concat_blocks_horizontally_and_vertically(blocks)
            return cls(table, blocks)

    @classmethod
    def from_tables(cls, tables: List[Union[pa.Table, Table]], axis: int = 0) -> "ConcatenationTable":
        blocks = []
        for table in tables:
            if isinstance(table, pa.Table):
                blocks.append([InMemoryTable(table)] if axis == 0 else InMemoryTable(table))
            elif isinstance(table, ConcatenationTable):
                blocks.extend(copy.deepcopy(table.blocks))
            else:
                blocks.append([table] if axis == 0 else table)
        return cls.from_blocks(blocks if axis == 0 else [blocks])

    @property
    def _slices(self):
        offset = 0
        for tables in self.blocks:
            length = len(tables[0])
            yield (offset, length)
            offset += length

    @inject_arrow_table_documentation(pa.Table.slice)
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

    @inject_arrow_table_documentation(pa.Table.filter)
    def filter(self, mask, *args, **kwargs):
        table = self.table.filter(mask, *args, **kwargs)
        blocks = []
        for (offset, length), tables in zip(self._slices, self.blocks):
            submask = mask.slice(offset, length)
            blocks.append([t.filter(submask, *args, **kwargs) for t in tables])
        return ConcatenationTable(table, blocks)

    @inject_arrow_table_documentation(pa.Table.flatten)
    def flatten(self, *args, **kwargs):
        table = self.table.flatten(*args, **kwargs)
        blocks = []
        for tables in self.blocks:
            blocks.append([t.flatten(*args, **kwargs) for t in tables])
        return ConcatenationTable(table, blocks)

    @inject_arrow_table_documentation(pa.Table.combine_chunks)
    def combine_chunks(self, *args, **kwargs):
        table = self.table.combine_chunks(*args, **kwargs)
        blocks = []
        for tables in self.blocks:
            blocks.append([t.combine_chunks(*args, **kwargs) for t in tables])
        return ConcatenationTable(table, blocks)

    @inject_arrow_table_documentation(pa.Table.cast)
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

    @inject_arrow_table_documentation(pa.Table.add_column)
    def add_column(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.append_column)
    def append_column(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.remove_column)
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

    @inject_arrow_table_documentation(pa.Table.set_column)
    def set_column(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.rename_columns)
    def rename_columns(self, names, *args, **kwargs):
        table = self.table.rename_columns(names, *args, **kwargs)
        names = dict(zip(self.table.column_names, names))
        blocks = []
        for tables in self.blocks:
            blocks.append(
                [t.rename_columns([names[name] for name in t.column_names], *args, **kwargs) for t in tables]
            )
        return ConcatenationTable(table, blocks)

    @inject_arrow_table_documentation(pa.Table.drop)
    def drop(self, columns, *args, **kwargs):
        table = self.table.drop(columns)
        blocks = []
        for tables in self.blocks:
            blocks.append([t.drop([c for c in columns if c in t.column_names], *args, **kwargs) for t in tables])
        return ConcatenationTable(table, blocks)


def concat_tables(tables: List[Table], axis: int = 0) -> Table:
    """
    Concatenate tables vertically.

    Returns:
        :obj:`datasets.table.Table` that is the concatenated table:
            If the number of input tables is > 1, then the returned table is a :obj:`datasets.table.ConcatenationTable`.
            Otherwise if there's only one table, it is returned as is.
    """
    tables = list(tables)
    if len(tables) == 1:
        return tables[0]
    return ConcatenationTable.from_tables(tables, axis=axis)


def list_table_cache_files(table: Table) -> List[str]:
    """
    Get the cache files that are loaded by the table.
    Cache file are used when parts of the table come from the disk via memory mapping.

    Returns:
        :obj:`List[str]`: a list of paths to the cache files loaded by the table
    """
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
