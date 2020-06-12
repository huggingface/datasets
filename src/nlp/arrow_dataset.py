# coding=utf-8
# Copyright 2020 The HuggingFace Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
""" Simple Dataset wrapping an Arrow Table."""

import hashlib
import logging
import os
from collections import defaultdict
from collections.abc import Mapping
from typing import Any, Dict, List, Optional, Union

import numpy as np
import pyarrow as pa
from tqdm import tqdm

from nlp.utils.py_utils import dumps

from .arrow_writer import ArrowWriter
from .utils import convert_tuples_in_lists, map_nested


logger = logging.getLogger(__name__)


class DatasetInfoMixin(object):
    """ This base class exposes some attributes of DatasetInfo
        at the base level of the Dataset for easy access.
    """

    def __init__(self, info, split):
        self._info = info
        self._split = split

    @property
    def info(self):
        return self._info

    @property
    def split(self):
        return self._split

    @property
    def builder_name(self) -> str:
        return self._info.builder_name

    @property
    def citation(self) -> str:
        return self._info.citation

    @property
    def config_name(self) -> str:
        return self._info.config_name

    @property
    def dataset_size(self) -> Optional[int]:
        return self._info.dataset_size

    @property
    def description(self) -> str:
        return self._info.description

    @property
    def download_checksums(self) -> Optional[dict]:
        return self._info.download_checksums

    @property
    def download_size(self) -> Optional[int]:
        return self._info.download_size

    @property
    def features(self):
        return self._info.features

    @property
    def homepage(self) -> Optional[str]:
        return self._info.homepage

    @property
    def license(self) -> Optional[str]:
        return self._info.license

    @property
    def size_in_bytes(self) -> Optional[int]:
        return self._info.size_in_bytes

    @property
    def supervised_keys(self):
        return self._info.supervised_keys

    @property
    def version(self):
        return self._info.version


class Dataset(DatasetInfoMixin):
    """ A Dataset backed by an Arrow table or Record Batch.
    """

    def __init__(
        self,
        arrow_table: Union[pa.Table, pa.RecordBatch],
        data_files: Optional[List[dict]] = None,
        info: Optional[Any] = None,
        split: Optional[Any] = None,
    ):
        super().__init__(info=info, split=split)
        self._data: pa.Table = arrow_table
        self._data_files: List[dict] = data_files if data_files is not None else []
        self._format_type = None
        self._format_columns = None
        self._output_all_columns = False

    @classmethod
    def from_file(cls, filename: str, info: Optional[Any] = None, split: Optional[Any] = None):
        """ Instantiate a Dataset backed by an Arrow table at filename """
        mmap = pa.memory_map(filename)
        f = pa.ipc.open_stream(mmap)
        pa_table = f.read_all()
        return cls(arrow_table=pa_table, data_files=[{"filename": filename}], info=info, split=split)

    @classmethod
    def from_buffer(cls, buffer: pa.Buffer, info: Optional[Any] = None, split: Optional[Any] = None):
        """ Instantiate a Dataset backed by an Arrow buffer """
        mmap = pa.BufferReader(buffer)
        f = pa.ipc.open_stream(mmap)
        pa_table = f.read_all()
        return cls(pa_table, info=info, split=split)

    @property
    def data(self):
        return self._data

    @property
    def cache_files(self):
        return self._data_files

    @property
    def columns(self):
        return self._data.columns

    @property
    def nbytes(self):
        return self._data.nbytes

    @property
    def num_columns(self):
        return self._data.num_columns

    @property
    def num_rows(self):
        return self._data.num_rows

    @property
    def column_names(self):
        return self._data.column_names

    @property
    def schema(self) -> pa.Schema:
        return self._data.schema

    @property
    def shape(self):
        return self._data.shape

    def drop(self, columns: Union[str, List[str]]):
        """ Drop one or more columns.

        Args:
            columns: list of str
        """
        if isinstance(columns, str):
            columns = [columns]
        if any(col not in self._data.column_names for col in columns):
            raise ValueError(
                "Columns {} not in the dataset. Current columns in the dataset: {}".format(
                    list(filter(lambda col: col not in self._data.column_names, columns)), self._data.column_names
                )
            )
        self._data = self._data.drop(columns)

    def unique(self, column: str):
        """ Return a list of the unque elements in a column.

        Args:
            columns: str
        """
        if column not in self._data.column_names:
            raise ValueError(f"Column ({column}) not in table columns ({self._data.column_names}).")
        return self._data.column(column).unique().to_pylist()

    def dictionary_encode_column(self, column: str):
        """ Dictionary encode a column.
            Dictionnary encode can reduce the size of a column with many repetitions (e.g. string labels columns)
            by storing a dictionnary of the strings. This only affect the internal storage.

        Args:
            columns: str
        """
        if column not in self._data.column_names:
            raise ValueError(f"Column ({column}) not in table columns ({self._data.column_names}).")
        casted_schema: pa.Schema = self._data.schema
        field_index = casted_schema.get_field_index(column)
        field: pa.Field = casted_schema.field(field_index)
        casted_field = pa.field(field.name, pa.dictionary(pa.int32(), field.type), nullable=False)
        casted_schema.set(field_index, casted_field)
        self._data = self._data.cast(casted_schema)

    def flatten(self):
        """ Flatten the Table.
            Each column with a struct type is flattened into one column per struct field.
            Other columns are left unchanged.
        """
        self._data = self._data.flatten()

    def __len__(self):
        return self._data.num_rows

    def __iter__(self):
        format_type = self._format_type
        format_columns = self._format_columns
        output_all_columns = self._output_all_columns
        for index in range(self._data.num_rows):
            yield self._getitem(
                index, format_type=format_type, format_columns=format_columns, output_all_columns=output_all_columns,
            )

    def __repr__(self):
        schema_str = dict((a, str(b)) for a, b in zip(self._data.schema.names, self._data.schema.types))
        return f"Dataset(schema: {schema_str}, num_rows: {self.num_rows})"

    @property
    def format(self):
        return {
            "type": "python" if self._format_type is None else self._format_type,
            "columns": self.column_names if self._format_columns is None else self._format_columns,
            "output_all_columns": self._output_all_columns,
        }

    def set_format(self, type: Optional[str] = None, columns: Optional[List] = None, output_all_columns: bool = False):
        """ Set __getitem__ return format (type and columns)

            Args:
                type (Optional ``str``): output type selected in [None, 'numpy', 'torch', 'tensorflow', 'pandas']
                    None means __getitem__ returns python objects (default)
                columns (Optional ``List[str]``): columns to format in the output
                    None means __getitem__ returns all columns (default)
                output_all_columns (``bool`` default to False): keep un-formated columns as well in the output (as python objects)
        """
        # Check return type
        if type == "torch":
            try:
                import torch  # noqa: F401
            except ImportError:
                logger.error("PyTorch needs to be installed to be able to return PyTorch tensors.")
        elif type == "tensorflow":
            try:
                import tensorflow  # noqa: F401
            except ImportError:
                logger.error("Tensorflow needs to be installed to be able to return Tensorflow tensors.")
        else:
            assert (
                type is None or type == "numpy" or type == "pandas"
            ), "Return type should be None or selected in ['numpy', 'torch', 'tensorflow', 'pandas']."

        # Check filter column
        if isinstance(columns, str):
            columns = [columns]
        if columns is not None and any(col not in self._data.column_names for col in columns):
            raise ValueError(
                "Columns {} not in the dataset. Current columns in the dataset: {}".format(
                    list(filter(lambda col: col not in self._data.column_names, columns)), self._data.column_names
                )
            )

        self._format_type = type
        self._format_columns = columns
        self._output_all_columns = output_all_columns
        logger.info(
            "Set __getitem__(key) output type to %s for %s columns "
            " (when key is int or slice) and %s output other (un-formated) columns.",
            "python objects" if type is None else type,
            "no" if columns is None else str(columns),
            "do" if output_all_columns else "don't",
        )

    def reset_format(self):
        """ Reset __getitem__ return format to python objects and all columns.

            Same as ``self.set_format()``
        """
        self.set_format()

    def _convert_outputs(self, outputs, format_type=None, format_columns=None, output_all_columns=False):
        if format_type is None:
            if output_all_columns:
                return outputs
            if isinstance(outputs, dict) and format_columns is not None:
                return {k: v for k, v in outputs.items() if k in format_columns}
            return outputs

        if format_type == "numpy":
            import numpy

            command = numpy.array
        elif format_type == "torch":
            import torch

            command = torch.tensor
        elif format_type == "tensorflow":
            import tensorflow

            command = tensorflow.ragged.constant
        else:

            def identity(x):
                return x

            command = identity

        if isinstance(outputs, (list, tuple)):
            return command(outputs)
        else:
            output_dict = {}
            for k, v in outputs.items():
                if format_columns is not None and k not in format_columns and not output_all_columns:
                    continue
                if format_columns is None or k in format_columns:
                    v = command(v)
                output_dict[k] = v
        return output_dict

    @staticmethod
    def _unnest(py_dict):
        return dict((key, array[0]) for key, array in py_dict.items())

    @staticmethod
    def _nest(py_dict):
        return dict((key, [elem]) for key, elem in py_dict.items())

    def _getitem(
        self, key: Union[int, slice, str], format_type=None, format_columns=None, output_all_columns=False
    ) -> Union[Dict, List]:
        """ Can be used to index columns (by string names) or rows (by integer index or slices)
        """
        if isinstance(key, int):
            if key < 0:
                key = self._data.num_rows + key
            if key >= self._data.num_rows:
                raise IndexError(f"Index ({key}) outside of table length ({self._data.num_rows}).")
            if format_type is not None and format_type == "pandas":
                outputs = self._data.slice(key, 1).to_pandas()
            else:
                outputs = self._unnest(self._data.slice(key, 1).to_pydict())
        elif isinstance(key, slice):
            key_indices = key.indices(self._data.num_rows)
            if key_indices[2] != 1 or key_indices[1] < key_indices[0]:
                raise ValueError("Slicing can only take contiguous and ordered slices.")
            if format_type is not None and format_type == "pandas":
                outputs = self._data.slice(key_indices[0], key_indices[1] - key_indices[0]).to_pandas()
            else:
                outputs = self._data.slice(key_indices[0], key_indices[1] - key_indices[0]).to_pydict()
        elif isinstance(key, str):
            if key not in self._data.column_names:
                raise ValueError(f"Column ({key}) not in table columns ({self._data.column_names}).")
            if format_type is not None:
                if format_columns is None or key in format_columns:
                    if format_type == "pandas":
                        outputs = self._data[key].to_pandas()
                    elif format_type == "numpy":
                        outputs = np.concatenate([arr.to_numpy() for arr in self._data[key].chunks])
                    else:
                        outputs = self._convert_outputs(self._data[key].to_pylist(), format_type=format_type)
                else:
                    outputs = self._data[key].to_pylist()
            else:
                outputs = self._data[key].to_pylist()
        else:
            raise ValueError("Can only get row(s) (int or slice) or columns (string).")

        if (
            (format_type is not None or format_columns is not None)
            and not isinstance(key, str)
            and format_type != "pandas"
        ):
            outputs = self._convert_outputs(
                outputs, format_type=format_type, format_columns=format_columns, output_all_columns=output_all_columns
            )
        return outputs

    def __getitem__(self, key: Union[int, slice, str]) -> Union[Dict, List]:
        """ Can be used to index columns (by string names) or rows (by integer index)
        """
        return self._getitem(
            key,
            format_type=self._format_type,
            format_columns=self._format_columns,
            output_all_columns=self._output_all_columns,
        )

    def cleanup_cache_files(self):
        """ Clean up all cache files in the dataset cache directory, excepted the currently used cache file if there is one.
            Be carefull when running this command that no other process is currently using other cache files.

            Return:
                Number of removed files
        """
        if not self._data_files or "filename" not in self._data_files[0]:
            return None
        current_cache_file = os.path.abspath(self._data_files[0]["filename"])
        cache_directory = os.path.dirname(current_cache_file)
        logger.info(f"Listing files in {cache_directory}")
        files: List[str] = os.listdir(cache_directory)
        files_to_remove = []
        for f_name in files:
            full_name = os.path.abspath(os.path.join(cache_directory, f_name))
            if f_name.startswith("cache-") and f_name.endswith(".arrow"):
                if full_name == current_cache_file:
                    logger.info(f"Keeping current cache file at {full_name}")
                    continue
                files_to_remove.append(full_name)
        for file_path in files_to_remove:
            logger.info(f"Removing {file_path}")
            os.remove(file_path)
        return len(files_to_remove)

    def _get_cache_file_path(self, function, cache_kwargs):
        """ Find a unique name from the filenames, kwargs and the function """
        if not self._data_files or "filename" not in self._data_files[0]:
            return None
        previous_files_string = "-".join(
            "-".join(str(k) + "-" + str(v) for k, v in f.items()) for f in self._data_files
        )
        cache_kwargs_string = "-".join(str(k) + "-" + str(v) for k, v in cache_kwargs.items())
        function_bytes = dumps(function)
        output_hash = hashlib.md5(
            previous_files_string.encode("utf-8") + cache_kwargs_string.encode("utf-8") + function_bytes
        ).hexdigest()
        cache_file_name = "cache-" + output_hash + ".arrow"
        cache_directory = os.path.dirname(self._data_files[0]["filename"])
        cache_file_path = os.path.join(cache_directory, cache_file_name)
        return cache_file_path

    def map(
        self,
        function,
        with_indices: bool = False,
        batched: bool = False,
        batch_size: Optional[int] = 1000,
        remove_columns: Optional[List[str]] = None,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
        arrow_schema: Optional[pa.Schema] = None,
        disable_nullable: bool = True,
    ):
        """ Apply a function to all the elements in the table (individually or in batches)
            and update the table (if function does updated examples).

            Args:
                `function` (`callable`): with one of the following signature:
                    - `function(example: Dict) -> Union[Dict, Any]` if `batched=False` and `with_indices=False`
                    - `function(example: Dict, indices: int) -> Union[Dict, Any]` if `batched=False` and `with_indices=True`
                    - `function(batch: Dict[List]) -> Union[Dict, Any]` if `batched=True` and `with_indices=False`
                    - `function(batch: Dict[List], indices: List[int]) -> Union[Dict, Any]` if `batched=True` and `with_indices=True`
                `with_indices` (`bool`, default: `False`): Provide example indices to `function`. Note that in this case the signature of `function` should be `def function(example, idx): ...`.
                `batched` (`bool`, default: `False`): Provide batch of examples to `function`
                `batch_size` (`Optional[int]`, default: `1000`): Number of examples per batch provided to `function` if `batched=True`
                    `batch_size <= 0` or `batch_size == None`: Provide the full dataset as a single batch to `function`
                `remove_columns` (`Optional[List[str]]`, default: `None`): Remove a selection of columns while doing the mapping.
                    Columns will be removed before updating the examples with the output of `function`, i.e. if `function` is adding
                    columns with names in `remove_columns`, these columns will be kept.
                `keep_in_memory` (`bool`, default: `False`): Keep the dataset in memory instead of writing it to a cache file.
                `load_from_cache_file` (`bool`, default: `True`): If a cache file storing the current computation from `function`
                    can be identified, use it instead of recomputing.
                `cache_file_name` (`Optional[str]`, default: `None`): Provide the name of a cache file to use to store the
                    results of the computation instead of the automatically generated cache file name.
                `writer_batch_size` (`int`, default: `1000`): Number of rows per write operation for the cache file writer.
                    Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
                `arrow_schema` (`Optional[pa.Schema]`, default: `None`): Use a specific Apache Arrow Schema to store the cache file
                    instead of the automatically generated one.
                `disable_nullable` (`bool`, default: `True`): Allow null values in the table.
        """
        # If the array is empty we do nothing
        if len(self) == 0:
            return self

        # Select the columns (arrow columns) to process
        if remove_columns is not None and any(col not in self._data.column_names for col in remove_columns):
            raise ValueError(
                "Column to remove {} not in the dataset. Current columns in the dataset: {}".format(
                    list(filter(lambda col: col not in self._data.column_names, remove_columns)),
                    self._data.column_names,
                )
            )

        # If we do batch computation but no batch sze is provided, default to the full dataset
        if batched and (batch_size is None or batch_size <= 0):
            batch_size = self._data.num_rows

        # Check if the function returns updated examples
        def does_function_return_dict(inputs, indices):
            """ Does the function returns a dict. """
            processed_inputs = function(inputs, indices) if with_indices else function(inputs)
            does_return_dict = isinstance(processed_inputs, Mapping)

            if does_return_dict is False and processed_inputs is not None:
                raise TypeError(
                    "Provided `function` which is applied to all elements of table returns a variable of type {}. Make sure provided `function` returns a variable of type `dict` to update the dataset or `None` if you are only interested in side effects.".format(
                        type(processed_inputs)
                    )
                )
            elif isinstance(test_indices, list) and does_return_dict is True:
                all_dict_values_are_lists = all(isinstance(value, list) for value in processed_inputs.values())
                if all_dict_values_are_lists is False:
                    raise TypeError(
                        "Provided `function` which is applied to all elements of table returns a `dict` of types {}. When using `batched=True`, make sure provided `function` returns a `dict` of types `list`.".format(
                            [type(x) for x in processed_inputs.values()]
                        )
                    )

            return does_return_dict

        # We only update the data table (and use the cache) if the function returns a dict.
        # Test it on the first element or a small batch (0, 1) for batched inputs
        test_inputs = self[:2] if batched else self[0]
        test_indices = [0, 1] if batched else 0
        update_data = does_function_return_dict(test_inputs, test_indices)

        def apply_function_on_filtered_inputs(inputs, indices):
            """ Utility to apply the function on a selection of columns. """
            processed_inputs = function(inputs, indices) if with_indices else function(inputs)
            if not update_data:
                return None  # Nothing to update, let's move on
            if remove_columns is not None:
                for column in remove_columns:
                    inputs.pop(column)
            if self._format_type is not None:
                inputs = self._getitem(
                    key=(indices if isinstance(indices, int) else slice(indices[0], indices[-1])),
                    format_type=None,
                    format_columns=None,
                )
            inputs.update(processed_inputs)
            return inputs

        # Find the output schema if none is given
        test_inputs = self[:2] if batched else self[0]
        test_indices = [0, 1] if batched else 0
        test_output = apply_function_on_filtered_inputs(test_inputs, test_indices)
        if arrow_schema is None and update_data:
            if not batched:
                test_output = self._nest(test_output)
            test_output = convert_tuples_in_lists(test_output)
            arrow_schema = pa.Table.from_pydict(test_output).schema
            if disable_nullable:
                arrow_schema = pa.schema(pa.field(field.name, field.type, nullable=False) for field in arrow_schema)

        # Check if we've already cached this computation (indexed by a hash)
        if self._data_files and update_data:
            if cache_file_name is None:
                # we create a unique hash from the function, current dataset file and the mapping args
                cache_kwargs = {
                    "with_indices": with_indices,
                    "batched": batched,
                    "batch_size": batch_size,
                    "remove_columns": remove_columns,
                    "keep_in_memory": keep_in_memory,
                    "load_from_cache_file": load_from_cache_file,
                    "cache_file_name": cache_file_name,
                    "writer_batch_size": writer_batch_size,
                    "arrow_schema": arrow_schema,
                    "disable_nullable": disable_nullable,
                }
                cache_file_name = self._get_cache_file_path(function, cache_kwargs)
            if os.path.exists(cache_file_name) and load_from_cache_file:
                logger.info("Loading cached processed dataset at %s", cache_file_name)
                return Dataset.from_file(cache_file_name, info=self.info, split=self.split)

        # Prepare output buffer and batched writer in memory or on file if we update the table
        if update_data:
            if keep_in_memory or not self._data_files:
                buf_writer = pa.BufferOutputStream()
                writer = ArrowWriter(schema=arrow_schema, stream=buf_writer, writer_batch_size=writer_batch_size)
            else:
                buf_writer = None
                logger.info("Caching processed dataset at %s", cache_file_name)
                writer = ArrowWriter(schema=arrow_schema, path=cache_file_name, writer_batch_size=writer_batch_size)

        # Loop over single examples or batches and write to buffer/file if examples are to be updated
        if not batched:
            for i, example in tqdm(enumerate(self)):
                example = apply_function_on_filtered_inputs(example, i)
                if update_data:
                    writer.write(example)
        else:
            for i in tqdm(range(0, len(self), batch_size)):
                batch = self[i : i + batch_size]
                indices = list(range(*(slice(i, i + batch_size).indices(self._data.num_rows))))  # Something simpler?
                batch = apply_function_on_filtered_inputs(batch, indices)
                if update_data:
                    writer.write_batch(batch)

        if update_data:
            writer.finalize()  # close_stream=bool(buf_writer is None))  # We only close if we are writing in a file

            # Create new Dataset from buffer or file
            if buf_writer is None:
                return Dataset.from_file(cache_file_name, info=self.info, split=self.split)
            else:
                return Dataset.from_buffer(buf_writer.getvalue(), info=self.info, split=self.split)
        else:
            return self

    def filter(self, function, with_indices=False, **kwargs):
        """ Apply a filter function to all the elements in the table in batches
            and update the table so that the dataset only includes examples according to the filter function.

            Args:
                `function` (`callable`): with one of the following signature:
                    - `function(example: Dict) -> bool` if `with_indices=False`
                    - `function(example: Dict, indices: int) -> bool` if `with_indices=True`
                `with_indices` (`bool`, default: `False`): Provide example indices to `function`. Note that in this case the signature of `function` should be `def function(example, idx): ...`.
                `batch_size` (`Optional[int]`, default: `1000`): Number of examples per batch provided to `function` if `batched=True`
                    `batch_size <= 0` or `batch_size == None`: Provide the full dataset as a single batch to `function`
                `remove_columns` (`Optional[List[str]]`, default: `None`): Remove a selection of columns while doing the mapping.
                    Columns will be removed before updating the examples with the output of `function`, i.e. if `function` is adding
                    columns with names in `remove_columns`, these columns will be kept.
                `keep_in_memory` (`bool`, default: `False`): Keep the dataset in memory instead of writing it to a cache file.
                `load_from_cache_file` (`bool`, default: `True`): If a cache file storing the current computation from `function`
                    can be identified, use it instead of recomputing.
                `cache_file_name` (`Optional[str]`, default: `None`): Provide the name of a cache file to use to store the
                    results of the computation instead of the automatically generated cache file name.
                `writer_batch_size` (`int`, default: `1000`): Number of rows per write operation for the cache file writer.
                    Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
                `disable_nullable` (`bool`, default: `True`): Allow null values in the table.
        """

        # transforme the filter function into the map function
        def map_function(batch, *args):
            result = defaultdict(list)
            num_examples = len(batch[next(iter(batch.keys()))])

            # create single examples
            for i in range(num_examples):
                example = map_nested(lambda x: x[i], batch, dict_only=True)

                # check if example should be fildered or not
                if with_indices:
                    keep_example = function(example, args[0][i])
                else:
                    keep_example = function(example)

                assert isinstance(
                    keep_example, bool
                ), f"The filter function returns a variable of type {type(keep_example)}, but should return a variable of type `bool`."
                # if example shall be kept add to result
                if keep_example:
                    for key in batch.keys():
                        result[key].append(example[key])

            # if no example shall be kept, init with empty list
            if bool(result) is False:
                for key in batch.keys():
                    result[key] = []

            return result

        # to avoid errors with the arrow_schema we define it here
        test_inputs = self[:2]
        if "remove_columns" in kwargs:
            test_inputs = {key: test_inputs[key] for key in (test_inputs.keys() - kwargs["remove_columns"])}
        arrow_schema = pa.Table.from_pydict(test_inputs).schema

        # return map function
        return self.map(map_function, batched=True, with_indices=with_indices, arrow_schema=arrow_schema, **kwargs)
