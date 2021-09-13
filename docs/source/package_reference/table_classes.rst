Table Classes
----------------------------------------------------

Each :obj:`datasets.Dataset` object is backed by a PyArrow Table.
A Table can be loaded from either the disk (memory mapped) or in memory.
Several Table types are available, and they all inherit from :class:`datasets.table.Table`.


.. autoclass:: datasets.table.Table
    :members: validate, equals,
        to_batches, to_pydict, to_pandas, to_string,
        field, column, itercolumns, schema, columns, num_columns, num_rows, shape, nbytes, column_names,

.. autoclass:: datasets.table.InMemoryTable
    :members: validate, equals,
        to_batches, to_pydict, to_pandas, to_string,
        field, column, itercolumns, schema, columns, num_columns, num_rows, shape, nbytes, column_names,
        slice, filter, flatten, combine_chunks, cast,
        add_column, append_column, remove_column, set_column, rename_columns, drop,
        from_file, from_buffer, from_pandas, from_arrays, from_pydict, from_batches

.. autoclass:: datasets.table.MemoryMappedTable
    :members: validate, equals,
        to_batches, to_pydict, to_pandas, to_string,
        field, column, itercolumns, schema, columns, num_columns, num_rows, shape, nbytes, column_names,
        slice, filter, flatten, combine_chunks, cast,
        add_column, append_column, remove_column, set_column, rename_columns, drop,
        from_file, 

.. autoclass:: datasets.table.ConcatenationTable
    :members: validate, equals,
        to_batches, to_pydict, to_pandas, to_string,
        field, column, itercolumns, schema, columns, num_columns, num_rows, shape, nbytes, column_names,
        slice, filter, flatten, combine_chunks, cast,
        add_column, append_column, remove_column, set_column, rename_columns, drop,
        from_blocks, from_tables

.. autofunction:: datasets.table.concat_tables

.. autofunction:: datasets.table.list_table_cache_files
