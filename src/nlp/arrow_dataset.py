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

import contextlib
import hashlib
import logging
import os
from collections import defaultdict
from collections.abc import Iterable, Mapping
from functools import partial
from math import ceil, floor
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd
import pyarrow as pa
from tqdm.auto import tqdm

from nlp.utils.py_utils import dumps

from .arrow_writer import ArrowWriter
from .features import Features
from .search import IndexableMixin
from .utils import map_all_sequences_to_lists, map_nested


if TYPE_CHECKING:
    from .info import DatasetInfo  # noqa: F401
    from .splits import NamedSplit  # noqa: F401


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


class DatasetTransformationNotAllowedError(Exception):
    pass


class Dataset(DatasetInfoMixin, IndexableMixin):
    """ A Dataset backed by an Arrow table or Record Batch.
    """

    def __init__(
        self,
        arrow_table: Union[pa.Table, pa.RecordBatch],
        data_files: Optional[List[dict]] = None,
        info: Optional[Any] = None,
        split: Optional[Any] = None,
    ):
        DatasetInfoMixin.__init__(self, info=info, split=split)
        IndexableMixin.__init__(self)
        self._data: pa.Table = arrow_table
        self._data_files: List[dict] = data_files if data_files is not None else []
        self._format_type: Optional[str] = None
        self._format_kwargs: dict = {}
        self._format_columns: Optional[list] = None
        self._output_all_columns: bool = False

    @classmethod
    def from_file(cls, filename: str, info: Optional["DatasetInfo"] = None, split: Optional["NamedSplit"] = None):
        """ Instantiate a Dataset backed by an Arrow table at filename """
        mmap = pa.memory_map(filename)
        f = pa.ipc.open_stream(mmap)
        pa_table = f.read_all()
        return cls(arrow_table=pa_table, data_files=[{"filename": filename}], info=info, split=split)

    @classmethod
    def from_buffer(
        cls, buffer: pa.Buffer, info: Optional["DatasetInfo"] = None, split: Optional["NamedSplit"] = None
    ):
        """ Instantiate a Dataset backed by an Arrow buffer """
        mmap = pa.BufferReader(buffer)
        f = pa.ipc.open_stream(mmap)
        pa_table = f.read_all()
        return cls(pa_table, info=info, split=split)

    @classmethod
    def from_pandas(
        cls,
        df: pd.DataFrame,
        features: Optional[Features] = None,
        info: Optional["DatasetInfo"] = None,
        split: Optional["NamedSplit"] = None,
    ):
        """
        Convert :obj:``pandas.DataFrame`` to a "obj"``pyarrow.Table`` to create a :obj:``nlp.Dataset``.

        The column types in the resulting Arrow Table are inferred from the dtypes of the pandas.Series in the DataFrame. In the case of non-object
        Series, the NumPy dtype is translated to its Arrow equivalent. In the case of `object`, we need to guess the datatype by looking at the
        Python objects in this Series.

        Be aware that Series of the `object` dtype don't carry enough information to always lead to a meaningful Arrow type. In the case that
        we cannot infer a type, e.g. because the DataFrame is of length 0 or the Series only contains None/nan objects, the type is set to
        null. This behavior can be avoided by constructing an explicit schema and passing it to this function.

        Args:
            df (:obj:``pandas.DataFrame``): the dataframe that contains the dataset.
            features (:obj:``nlp.Features``, `optional`, defaults to :obj:``None``): If specified, the features types of the dataset
            info (:obj:``nlp.DatasetInfo``, `optional`, defaults to :obj:``None``): If specified, the dataset info containing info like
                description, citation, etc.
            split (:obj:``nlp.NamedSplit``, `optional`, defaults to :obj:``None``): If specified, the name of the dataset split.
        """
        pa_table = pa.Table.from_pandas(df=df, schema=pa.schema(features.type) if features is not None else None)
        return cls(pa_table, info=info, split=split)

    @classmethod
    def from_dict(
        cls,
        mapping: dict,
        features: Optional[Features] = None,
        info: Optional[Any] = None,
        split: Optional[Any] = None,
    ):
        """
        Convert :obj:``dict`` to a "obj"``pyarrow.Table`` to create a :obj:``nlp.Dataset``.

        Args:
            mapping (:obj:``mapping``): A mapping of strings to Arrays or Python lists.
            features (:obj:``nlp.Features``, `optional`, defaults to :obj:``None``): If specified, the features types of the dataset
            info (:obj:``nlp.DatasetInfo``, `optional`, defaults to :obj:``None``): If specified, the dataset info containing info like
                description, citation, etc.
            split (:obj:``nlp.NamedSplit``, `optional`, defaults to :obj:``None``): If specified, the name of the dataset split.
        """
        pa_table = pa.Table.from_pydict(
            mapping=mapping, schema=pa.schema(features.type) if features is not None else None
        )
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
        format_kwargs = self._format_kwargs
        format_columns = self._format_columns
        output_all_columns = self._output_all_columns
        for index in range(self._data.num_rows):
            yield self._getitem(
                index,
                format_type=format_type,
                format_columns=format_columns,
                output_all_columns=output_all_columns,
                format_kwargs=format_kwargs,
            )

    def __repr__(self):
        schema_str = dict((a, str(b)) for a, b in zip(self._data.schema.names, self._data.schema.types))
        return f"Dataset(schema: {schema_str}, num_rows: {self.num_rows})"

    @property
    def format(self):
        return {
            "type": "python" if self._format_type is None else self._format_type,
            "format_kwargs": self._format_kwargs,
            "columns": self.column_names if self._format_columns is None else self._format_columns,
            "output_all_columns": self._output_all_columns,
        }

    @contextlib.contextmanager
    def formated_as(
        self,
        type: Optional[str] = None,
        columns: Optional[List] = None,
        output_all_columns: bool = False,
        **format_kwargs,
    ):
        """ To be used in a `with` statement. Set __getitem__ return format (type and columns)

            Args:
                type (Optional ``str``): output type selected in [None, 'numpy', 'torch', 'tensorflow', 'pandas']
                    None means __getitem__ returns python objects (default)
                columns (Optional ``List[str]``): columns to format in the output
                    None means __getitem__ returns all columns (default)
                output_all_columns (``bool`` default to False): keep un-formated columns as well in the output (as python objects)
                format_kwargs: keywords arguments passed to the convert function like `np.array`, `torch.tensor` or `tensorflow.ragged.constant`.
        """
        old_format_type = self._format_type
        old_format_kwargs = self._format_kwargs
        old_format_columns = self._format_columns
        old_output_all_columns = self._output_all_columns
        try:
            self.set_format(type, columns, output_all_columns, **format_kwargs)
            yield
        finally:
            self.set_format(old_format_type, old_format_columns, old_output_all_columns, **old_format_kwargs)

    def set_format(
        self,
        type: Optional[str] = None,
        columns: Optional[List] = None,
        output_all_columns: bool = False,
        **format_kwargs,
    ):
        """ Set __getitem__ return format (type and columns)

            Args:
                type (Optional ``str``): output type selected in [None, 'numpy', 'torch', 'tensorflow', 'pandas']
                    None means __getitem__ returns python objects (default)
                columns (Optional ``List[str]``): columns to format in the output
                    None means __getitem__ returns all columns (default)
                output_all_columns (``bool`` default to False): keep un-formated columns as well in the output (as python objects)
                format_kwargs: keywords arguments passed to the convert function like `np.array`, `torch.tensor` or `tensorflow.ragged.constant`.
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
            assert not (
                type == "pandas" and format_kwargs is not None
            ), "Format type 'pandas' doesn't have any `**format_kwargs`."
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
        self._format_kwargs = format_kwargs
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

    def _convert_outputs(
        self, outputs, format_type=None, format_columns=None, output_all_columns=False, format_kwargs=None
    ):
        format_kwargs = format_kwargs if format_kwargs is not None else {}
        if format_type is None:
            if output_all_columns:
                return outputs
            if isinstance(outputs, dict) and format_columns is not None:
                return {k: v for k, v in outputs.items() if k in format_columns}
            return outputs

        map_nested_kwargs = {}
        if format_type == "numpy":
            import numpy as np

            if "copy" not in format_kwargs:
                format_kwargs["copy"] = False
            command = partial(np.array, **format_kwargs)
            map_nested_kwargs["map_list"] = False  # convert lists to array
        elif format_type == "torch":
            import torch

            command = partial(torch.tensor, **format_kwargs)
        elif format_type == "tensorflow":
            import tensorflow

            command = partial(tensorflow.ragged.constant, **format_kwargs)
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
                    v = map_nested(command, v, **map_nested_kwargs)
                output_dict[k] = v
        return output_dict

    @staticmethod
    def _unnest(py_dict):
        return dict((key, array[0]) for key, array in py_dict.items())

    @staticmethod
    def _nest(py_dict):
        return dict((key, [elem]) for key, elem in py_dict.items())

    def _getitem(
        self,
        key: Union[int, slice, str],
        format_type=None,
        format_columns=None,
        output_all_columns=False,
        format_kwargs=None,
    ) -> Union[Dict, List]:
        """ Can be used to index columns (by string names) or rows (by integer index or slices)
        """
        # In the following, to convert data from the arrow table to dicts or lists,
        # we use .to_pandas().to_dict() or .to_pandas().to_list() as they are
        # significantly faster than .to_pydict() thanks to zero-copy
        if isinstance(key, int):
            if key < 0:
                key = self._data.num_rows + key
            if key >= self._data.num_rows:
                raise IndexError(f"Index ({key}) outside of table length ({self._data.num_rows}).")
            if format_type is not None and format_type == "pandas":
                outputs = self._data.slice(key, 1).to_pandas()
            else:
                outputs = self._unnest(self._data.slice(key, 1).to_pandas().to_dict("list"))
        elif isinstance(key, slice):
            key_indices = key.indices(self._data.num_rows)
            if key_indices[2] != 1 or key_indices[1] < key_indices[0]:
                raise ValueError("Slicing can only take contiguous and ordered slices.")
            if format_type is not None and format_type == "pandas":
                outputs = self._data.slice(key_indices[0], key_indices[1] - key_indices[0]).to_pandas(
                    split_blocks=True
                )
            else:
                outputs = (
                    self._data.slice(key_indices[0], key_indices[1] - key_indices[0])
                    .to_pandas(split_blocks=True)
                    .to_dict("list")
                )
        elif isinstance(key, str):
            if key not in self._data.column_names:
                raise ValueError(f"Column ({key}) not in table columns ({self._data.column_names}).")
            if format_type is not None:
                if format_columns is None or key in format_columns:
                    if format_type == "pandas":
                        outputs = self._data[key].to_pandas(split_blocks=True)
                    else:
                        outputs = self._data[key].to_pandas(split_blocks=True).to_list()
                else:
                    outputs = self._data[key].to_pandas(split_blocks=True).to_list()
            else:
                outputs = self._data[key].to_pandas(split_blocks=True).to_list()
        elif isinstance(key, Iterable):
            data_subset = pa.concat_tables(self._data.slice(int(i), 1) for i in key)
            if format_type is not None and format_type == "pandas":
                outputs = data_subset.to_pandas(split_blocks=True)
            else:
                outputs = data_subset.to_pandas(split_blocks=True).to_dict("list")

        else:
            raise ValueError("Can only get row(s) (int or slice or list[int]) or columns (string).")

        if (
            (format_type is not None or format_columns is not None)
            and not isinstance(key, str)
            and format_type != "pandas"
        ):
            outputs = self._convert_outputs(
                outputs,
                format_type=format_type,
                format_columns=format_columns,
                output_all_columns=output_all_columns,
                format_kwargs=format_kwargs,
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
            format_kwargs=self._format_kwargs,
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
                allowed_batch_return_types = (list, np.ndarray)
                all_dict_values_are_lists = all(
                    isinstance(value, allowed_batch_return_types) for value in processed_inputs.values()
                )
                if all_dict_values_are_lists is False:
                    raise TypeError(
                        "Provided `function` which is applied to all elements of table returns a `dict` of types {}. When using `batched=True`, make sure provided `function` returns a `dict` of types like `{}`.".format(
                            [type(x) for x in processed_inputs.values()], allowed_batch_return_types
                        )
                    )

            return does_return_dict

        # We only update the data table (and use the cache) if the function returns a dict.
        # Test it on the first element or a small batch (0, 1) for batched inputs
        test_inputs = self[:2] if batched else self[0]
        test_indices = [0, 1] if batched else 0
        update_data = does_function_return_dict(test_inputs, test_indices)

        class NumExamplesMismatch(Exception):
            pass

        def apply_function_on_filtered_inputs(inputs, indices, check_same_num_examples=False):
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
                    format_kwargs=None,
                )
            if check_same_num_examples:
                input_num_examples = len(inputs[next(iter(inputs.keys()))])
                processed_inputs_num_examples = len(processed_inputs[next(iter(processed_inputs.keys()))])
                if input_num_examples != processed_inputs_num_examples:
                    raise NumExamplesMismatch()
            inputs.update(processed_inputs)
            return inputs

        # Find the output schema if none is given
        test_inputs = self[:2] if batched else self[0]
        test_indices = [0, 1] if batched else 0
        test_output = apply_function_on_filtered_inputs(test_inputs, test_indices)
        if arrow_schema is None and update_data:
            if not batched:
                test_output = self._nest(test_output)
            test_output = map_all_sequences_to_lists(test_output)
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
            for i, example in enumerate(tqdm(self)):
                example = apply_function_on_filtered_inputs(example, i)
                if update_data:
                    writer.write(example)
        else:
            for i in tqdm(range(0, len(self), batch_size)):
                batch = self[i : i + batch_size]
                indices = list(range(*(slice(i, i + batch_size).indices(self._data.num_rows))))  # Something simpler?
                try:
                    batch = apply_function_on_filtered_inputs(
                        batch, indices, check_same_num_examples=len(self.list_indexes()) > 0
                    )
                except NumExamplesMismatch:
                    raise DatasetTransformationNotAllowedError(
                        "Using `.map` in batched mode on a dataset with attached indexes is allowed only if it doesn't create or remove existing examples. You can first run `.drop_index() to remove your index and then re-add it."
                    )
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
        if len(self.list_indexes()) > 0:
            raise DatasetTransformationNotAllowedError(
                "Using `.filter` on a dataset with attached indexes is not allowed. You can first run `.drop_index() to remove your index and then re-add it.`"
            )

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
        test_inputs = map_all_sequences_to_lists(test_inputs)
        arrow_schema = pa.Table.from_pydict(test_inputs).schema

        # return map function
        return self.map(map_function, batched=True, with_indices=with_indices, arrow_schema=arrow_schema, **kwargs)

    def select(
        self,
        indices: Union[List[int], np.ndarray],
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
    ):
        """ Create a new dataset with rows selected following the list/array of indices.

            Args:
                `indices` (`Union[List[int], np.ndarray]`): List or 1D-NumPy array of integer indices for indexing.
                `keep_in_memory` (`bool`, default: `False`): Keep the dataset in memory instead of writing it to a cache file.
                `load_from_cache_file` (`bool`, default: `True`): If a cache file storing the current computation from `function`
                    can be identified, use it instead of recomputing.
                `cache_file_name` (`Optional[str]`, default: `None`): Provide the name of a cache file to use to store the
                    results of the computation instead of the automatically generated cache file name.
                `writer_batch_size` (`int`, default: `1000`): Number of rows per write operation for the cache file writer.
                    Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
        """
        if len(self.list_indexes()) > 0:
            raise DatasetTransformationNotAllowedError(
                "Using `.select` on a dataset with attached indexes is not allowed. You can first run `.drop_index() to remove your index and then re-add it."
            )
        # If the array is empty we do nothing
        if len(self) == 0:
            return self

        # Check if we've already cached this computation (indexed by a hash)
        if self._data_files:
            if cache_file_name is None:
                # we create a unique hash from the function, current dataset file and the mapping args
                cache_kwargs = {
                    "indices": indices,
                    "keep_in_memory": keep_in_memory,
                    "load_from_cache_file": load_from_cache_file,
                    "cache_file_name": cache_file_name,
                    "writer_batch_size": writer_batch_size,
                }
                cache_file_name = self._get_cache_file_path(self.select, cache_kwargs)
            if os.path.exists(cache_file_name) and load_from_cache_file:
                logger.info("Loading cached selected dataset at %s", cache_file_name)
                return Dataset.from_file(cache_file_name, info=self.info, split=self.split)

        # Prepare output buffer and batched writer in memory or on file if we update the table
        if keep_in_memory or not self._data_files:
            buf_writer = pa.BufferOutputStream()
            writer = ArrowWriter(schema=self.schema, stream=buf_writer, writer_batch_size=writer_batch_size)
        else:
            buf_writer = None
            logger.info("Caching processed dataset at %s", cache_file_name)
            writer = ArrowWriter(schema=self.schema, path=cache_file_name, writer_batch_size=writer_batch_size)

        # Loop over single examples or batches and write to buffer/file if examples are to be updated
        for i in tqdm(indices):
            example = self._getitem(key=int(i), format_type=None, format_columns=None, format_kwargs=None)
            writer.write(example)

        writer.finalize()  # close_stream=bool(buf_writer is None))  # We only close if we are writing in a file

        # Create new Dataset from buffer or file
        if buf_writer is None:
            return Dataset.from_file(cache_file_name, info=self.info, split=self.split)
        else:
            return Dataset.from_buffer(buf_writer.getvalue(), info=self.info, split=self.split)

    def sort(
        self,
        column: str,
        reverse: bool = False,
        kind: str = None,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
    ):
        """ Create a new dataset sorted according to a column.

            Currently sorting according to a column name uses numpy sorting algorithm under the hood.
            The column should thus be a numpy compatible type (in particular not a nested type).
            This also means that the column used for sorting is fully loaded in memory (which should be fine in most cases).

            Args:
                `column` (`str`): column name to sort by.
                `reverse`: (`bool`, default: `False`): If True, sort by descending order rather then ascending.
                `kind` (Optional `str`): Numpy algorithm for sorting selected in {‘quicksort’, ‘mergesort’, ‘heapsort’, ‘stable’},
                    The default is ‘quicksort’. Note that both ‘stable’ and ‘mergesort’ use timsort under the covers and, in general,
                    the actual implementation will vary with data type. The ‘mergesort’ option is retained for backwards compatibility.
                `keep_in_memory` (`bool`, default: `False`): Keep the dataset in memory instead of writing it to a cache file.
                `load_from_cache_file` (`bool`, default: `True`): If a cache file storing the current computation from `function`
                    can be identified, use it instead of recomputing.
                `cache_file_name` (`Optional[str]`, default: `None`): Provide the name of a cache file to use to store the
                    results of the computation instead of the automatically generated cache file name.
                `writer_batch_size` (`int`, default: `1000`): Number of rows per write operation for the cache file writer.
                    Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
        """
        if len(self.list_indexes()) > 0:
            raise DatasetTransformationNotAllowedError(
                "Using `.sort` on a dataset with attached indexes is not allowed. You can first run `.drop_index() to remove your index and then re-add it."
            )
        # If the array is empty we do nothing
        if len(self) == 0:
            return self

        # Check the column name
        if not isinstance(column, str) or column not in self._data.column_names:
            raise ValueError(
                "Column '{}' not found in the dataset. Please provide a column selected in: {}".format(
                    column, self._data.column_names,
                )
            )

        # Check if we've already cached this computation (indexed by a hash)
        if self._data_files:
            if cache_file_name is None:
                # we create a unique hash from the function, current dataset file and the mapping args
                cache_kwargs = {
                    "column": column,
                    "reverse": reverse,
                    "kind": kind,
                    "keep_in_memory": keep_in_memory,
                    "load_from_cache_file": load_from_cache_file,
                    "cache_file_name": cache_file_name,
                    "writer_batch_size": writer_batch_size,
                }
                cache_file_name = self._get_cache_file_path(self.sort, cache_kwargs)
            if os.path.exists(cache_file_name) and load_from_cache_file:
                logger.info("Loading cached sorted dataset at %s", cache_file_name)
                return Dataset.from_file(cache_file_name, info=self.info, split=self.split)

        indices = self._getitem(
            column, format_type="numpy", format_columns=None, output_all_columns=False, format_kwargs=None
        )
        indices = np.argsort(indices, kind=kind)
        if reverse:
            indices = indices[::-1]

        return self.select(
            indices=indices,
            keep_in_memory=keep_in_memory,
            load_from_cache_file=load_from_cache_file,
            cache_file_name=cache_file_name,
            writer_batch_size=writer_batch_size,
        )

    def shuffle(
        self,
        seed: Optional[int] = None,
        generator: Optional[np.random.Generator] = None,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
    ):
        """ Create a new Dataset where rows the rows are shuffled.

            Currently shuffling uses numpy random generators.
            You can either supply a NumPy BitGenerator to use, or a seed to initiate NumPy's default random generator (PCG64).

            Args:
                `seed` (Optional `int`): A seed to initialize the default BitGenerator if ``generator=None``.
                    If None, then fresh, unpredictable entropy will be pulled from the OS.
                    If an int or array_like[ints] is passed, then it will be passed to SeedSequence to derive the initial BitGenerator state.
                `generator` (Optional `np.random.Generator`): Numpy random Generator to use to compute the permutation of the dataset rows.
                    If ``generator=None`` (default), uses np.random.default_rng (the default BitGenerator (PCG64) of NumPy).
                `keep_in_memory` (`bool`, default: `False`): Keep the dataset in memory instead of writing it to a cache file.
                `load_from_cache_file` (`bool`, default: `True`): If a cache file storing the current computation from `function`
                    can be identified, use it instead of recomputing.
                `cache_file_name` (`Optional[str]`, default: `None`): Provide the name of a cache file to use to store the
                    results of the computation instead of the automatically generated cache file name.
                `writer_batch_size` (`int`, default: `1000`): Number of rows per write operation for the cache file writer.
                    Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
        """
        if len(self.list_indexes()) > 0:
            raise DatasetTransformationNotAllowedError(
                "Using `.shuffle` on a dataset with attached indexes is not allowed. You can first run `.drop_index() to remove your index and then re-add it."
            )
        # If the array is empty we do nothing
        if len(self) == 0:
            return self

        if seed is not None and generator is not None:
            raise ValueError("Both `seed` and `generator` were provided. Please specify just one of them.")

        assert generator is None or isinstance(
            generator, np.random.Generator
        ), "The provided generator must be an instance of numpy.random.Generator"

        # Check if we've already cached this computation (indexed by a hash)
        if self._data_files:
            if cache_file_name is None:
                # we create a unique hash from the function, current dataset file and the mapping args
                cache_kwargs = {
                    "generator": generator,
                    "seed": seed,
                    "keep_in_memory": keep_in_memory,
                    "load_from_cache_file": load_from_cache_file,
                    "cache_file_name": cache_file_name,
                    "writer_batch_size": writer_batch_size,
                }
                cache_file_name = self._get_cache_file_path(self.shuffle, cache_kwargs)
            if os.path.exists(cache_file_name) and load_from_cache_file:
                logger.info("Loading cached shuffled dataset at %s", cache_file_name)
                return Dataset.from_file(cache_file_name, info=self.info, split=self.split)

        if generator is None:
            generator = np.random.default_rng(seed)

        permutation = generator.permutation(len(self))

        return self.select(
            indices=permutation,
            keep_in_memory=keep_in_memory,
            load_from_cache_file=load_from_cache_file,
            cache_file_name=cache_file_name,
            writer_batch_size=writer_batch_size,
        )

    def train_test_split(
        self,
        test_size: Union[float, int, None] = None,
        train_size: Union[float, int, None] = None,
        shuffle: bool = True,
        seed: Optional[int] = None,
        generator: Optional[np.random.Generator] = None,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        train_cache_file_name: Optional[str] = None,
        test_cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
    ):
        """ Return a dictionary with two random train and test subsets (`train` and `test` ``Dataset`` splits).
            Splits are created from the dataset according to `test_size`, `train_size` and `shuffle`.

            This method is similar to scikit-learn `train_test_split` with the omission of the stratified options.

            Args:
                `test_size` (Optional `np.random.Generator`): Size of the test split
                    If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the test split.
                    If int, represents the absolute number of test samples.
                    If None, the value is set to the complement of the train size.
                    If train_size is also None, it will be set to 0.25.
                `train_size` (Optional `np.random.Generator`): Size of the train split
                    If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the train split.
                    If int, represents the absolute number of train samples.
                    If None, the value is automatically set to the complement of the test size.
                `shuffle` (Optional `bool`, default: `True`): Whether or not to shuffle the data before splitting.
                `seed` (Optional `int`): A seed to initialize the default BitGenerator if ``generator=None``.
                    If None, then fresh, unpredictable entropy will be pulled from the OS.
                    If an int or array_like[ints] is passed, then it will be passed to SeedSequence to derive the initial BitGenerator state.
                `generator` (Optional `np.random.Generator`): Numpy random Generator to use to compute the permutation of the dataset rows.
                    If ``generator=None`` (default), uses np.random.default_rng (the default BitGenerator (PCG64) of NumPy).
                `keep_in_memory` (`bool`, default: `False`): Keep the dataset in memory instead of writing it to a cache file.
                `load_from_cache_file` (`bool`, default: `True`): If a cache file storing the current computation from `function`
                    can be identified, use it instead of recomputing.
                `train_cache_file_name` (`Optional[str]`, default: `None`): Provide the name of a cache file to use to store the
                    train split calche file instead of the automatically generated cache file name.
                `test_cache_file_name` (`Optional[str]`, default: `None`): Provide the name of a cache file to use to store the
                    test split calche file instead of the automatically generated cache file name.
                `writer_batch_size` (`int`, default: `1000`): Number of rows per write operation for the cache file writer.
                    Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
        """
        if len(self.list_indexes()) > 0:
            raise DatasetTransformationNotAllowedError(
                "Using `.train_test_split` on a dataset with attached indexes is not allowed. You can first run `.drop_index() to remove your index and then re-add it."
            )
        # If the array is empty we do nothing
        if len(self) == 0:
            return self

        if test_size is None and train_size is None:
            test_size = 0.25

        # Safety checks similar to scikit-learn's ones.
        # (adapted from https://github.com/scikit-learn/scikit-learn/blob/fd237278e895b42abe8d8d09105cbb82dc2cbba7/sklearn/model_selection/_split.py#L1750)
        n_samples = len(self)
        if (
            isinstance(test_size, int)
            and (test_size >= n_samples or test_size <= 0)
            or isinstance(test_size, float)
            and (test_size <= 0 or test_size >= 1)
        ):
            raise ValueError(
                f"test_size={test_size} should be either positive and smaller "
                f"than the number of samples {n_samples} or a float in the (0, 1) range"
            )

        if (
            isinstance(train_size, int)
            and (train_size >= n_samples or train_size <= 0)
            or isinstance(train_size, float)
            and (train_size <= 0 or train_size >= 1)
        ):
            raise ValueError(
                f"train_size={train_size} should be either positive and smaller "
                f"than the number of samples {n_samples} or a float in the (0, 1) range"
            )

        if train_size is not None and not isinstance(train_size, (int, float)):
            raise ValueError(f"Invalid value for train_size: {train_size} of type {type(train_size)}")
        if test_size is not None and not isinstance(test_size, (int, float)):
            raise ValueError(f"Invalid value for test_size: {test_size} of type {type(test_size)}")

        if isinstance(train_size, float) and isinstance(test_size, float) and train_size + test_size > 1:
            raise ValueError(
                f"The sum of test_size and train_size = {train_size + test_size}, should be in the (0, 1)"
                " range. Reduce test_size and/or train_size."
            )

        if isinstance(test_size, float):
            n_test = ceil(test_size * n_samples)
        elif isinstance(test_size, int):
            n_test = float(test_size)

        if isinstance(train_size, float):
            n_train = floor(train_size * n_samples)
        elif isinstance(train_size, int):
            n_train = float(train_size)

        if train_size is None:
            n_train = n_samples - n_test
        elif test_size is None:
            n_test = n_samples - n_train

        if n_train + n_test > n_samples:
            raise ValueError(
                f"The sum of train_size and test_size = {n_train + n_test}, "
                "should be smaller than the number of "
                f"samples {n_samples}. Reduce test_size and/or "
                "train_size."
            )

        n_train, n_test = int(n_train), int(n_test)

        if n_train == 0:
            raise ValueError(
                f"With n_samples={n_samples}, test_size={test_size} and train_size={train_size}, the "
                "resulting train set will be empty. Adjust any of the "
                "aforementioned parameters."
            )

        # Check if we've already cached this computation (indexed by a hash)
        if self._data_files:
            if train_cache_file_name is None or test_cache_file_name is None:
                # we create a unique hash from the function, current dataset file and the mapping args
                cache_kwargs = {
                    "test_size": test_size,
                    "train_size": train_size,
                    "shuffle": shuffle,
                    "generator": generator,
                    "seed": seed,
                    "keep_in_memory": keep_in_memory,
                    "load_from_cache_file": load_from_cache_file,
                    "train_cache_file_name": train_cache_file_name,
                    "test_cache_file_name": test_cache_file_name,
                    "writer_batch_size": writer_batch_size,
                }
                train_kwargs = cache_kwargs.deepcopy()
                train_kwargs["split"] = "train"
                test_kwargs = cache_kwargs.deepcopy()
                test_kwargs["split"] = "test"

                if train_cache_file_name is None:
                    train_cache_file_name = self._get_cache_file_path(self.train_test_split, train_kwargs)
                if test_cache_file_name is None:
                    test_cache_file_name = self._get_cache_file_path(self.train_test_split, test_kwargs)
            if os.path.exists(train_cache_file_name) and os.path.exists(test_cache_file_name) and load_from_cache_file:
                logger.info("Loading cached split dataset at %s and %s", train_cache_file_name, test_cache_file_name)
                return {
                    "train": Dataset.from_file(train_cache_file_name, info=self.info, split=self.split),
                    "test": Dataset.from_file(test_cache_file_name, info=self.info, split=self.split),
                }

        if not shuffle:
            train_indices = np.arange(n_train)
            test_indices = np.arange(n_train, n_train + n_test)
        else:
            if generator is None:
                generator = np.random.default_rng(seed)

            # random partition
            permutation = generator.permutation(len(self))
            test_indices = permutation[:n_test]
            train_indices = permutation[n_test : (n_test + n_train)]

        train_split = self.select(
            indices=train_indices,
            keep_in_memory=keep_in_memory,
            load_from_cache_file=load_from_cache_file,
            cache_file_name=train_cache_file_name,
            writer_batch_size=writer_batch_size,
        )
        test_split = self.select(
            indices=test_indices,
            keep_in_memory=keep_in_memory,
            load_from_cache_file=load_from_cache_file,
            cache_file_name=test_cache_file_name,
            writer_batch_size=writer_batch_size,
        )

        return {"train": train_split, "test": test_split}

    def shard(
        self,
        num_shards: int,
        index: int,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
    ):
        """ Return the `index`-nth shard from dataset split into `num_shards` pieces.

            This shards deterministically, so ds.shard(n, i) will contain all elements of ds whose
            index mod n = i. Be sure to shard before using any randomizing operator (such as shuffle).
            It is best if the shard operator is used early in the dataset pipeline.

            Args:
                `num_shards` (`int`): How many shards to split the dataset into.
                `index` (`int`): Which shard to select and return.
                `keep_in_memory` (`bool`, default: `False`): Keep the dataset in memory instead of writing it to a cache file.
                `load_from_cache_file` (`bool`, default: `True`): If a cache file storing the current computation from `function`
                    can be identified, use it instead of recomputing.
                `cache_file_name` (`Optional[str]`, default: `None`): Provide the name of a cache file to use to store the
                    results of the computation instead of the automatically generated cache file name.
                `writer_batch_size` (`int`, default: `1000`): Number of rows per write operation for the cache file writer.
                    Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
        """
        indices = np.arange(index, len(self), num_shards)
        return self.select(
            indices=indices,
            keep_in_memory=keep_in_memory,
            load_from_cache_file=load_from_cache_file,
            cache_file_name=cache_file_name,
            writer_batch_size=writer_batch_size,
        )

    def add_faiss_index(
        self,
        column: str,
        index_name: Optional[str] = None,
        device: Optional[int] = None,
        string_factory: Optional[str] = None,
        metric_type: Optional[int] = None,
        custom_index: Optional["faiss.Index"] = None,  # noqa: F821
        train_size: Optional[int] = None,
        faiss_verbose: bool = False,
        dtype=np.float32,
    ):
        """ Add a dense index using Faiss for fast retrieval.
            By default the index is done over the vectors of the specified column.
            You can specify `device` if you want to run it on GPU (`device` must be the GPU index).
            You can find more information about Faiss here:
            - For `string factory`: https://github.com/facebookresearch/faiss/wiki/The-index-factory

            Examples of usage:

            ```
            ds = nlp.load_dataset('crime_and_punish', split='train')
            ds_with_embeddings = ds.map(lambda example: {'embeddings': embed(example['line']}))
            ds_with_embeddings.add_faiss_index(column='embeddings')
            # query
            scores, retrieved_examples = ds_with_embeddings.get_nearest_examples('embeddings', embed('my new query'), k=10)
            # save index
            ds_with_embeddings.save_faiss_index('embeddings', 'my_index.faiss')
            ```

            ```
            ds = nlp.load_dataset('crime_and_punish', split='train')
            # load index
            ds.load_faiss_index('embeddings', 'my_index.faiss')
            # query
            scores, retrieved_examples = ds.get_nearest_examples('embeddings', embed('my new query'), k=10)
            ```

            Args:
                `column` (`str`): The column of the vectors to add to the index.
                `index_name` (Optional `str`): The index_name/identifier of the index. This is the index_name that is used to call `.get_nearest` or `.search`.
                    By defaul it corresponds to `column`.
                `device` (Optional `int`): If not None, this is the index of the GPU to use. By default it uses the CPU.
                `string_factory` (Optional `str`): This is passed to the index factory of Faiss to create the index. Default index class is IndexFlatIP.
                `metric_type` (Optional `int`): Type of metric. Ex: faiss.faiss.METRIC_INNER_PRODUCT or faiss.METRIC_L2.
                `custom_index` (Optional `faiss.Index`): Custom Faiss index that you already have instantiated and configured for your needs.
                `train_size` (Optional `int`): If the index needs a training step, specifies how many vectors will be used to train the index.
                `faiss_verbose` (`bool`, defaults to False): Enable the verbosity of the Faiss index.
                `dtype` (data-type): The dtype of the numpy arrays that are indexed. Default is np.float32.
        """
        with self.formated_as(type="numpy", columns=[column], dtype=dtype):
            super().add_faiss_index(
                column=column,
                index_name=index_name,
                device=device,
                string_factory=string_factory,
                metric_type=metric_type,
                custom_index=custom_index,
                train_size=train_size,
                faiss_verbose=faiss_verbose,
            )
        return self

    def add_faiss_index_from_external_arrays(
        self,
        external_arrays: np.array,
        index_name: str,
        device: Optional[int] = None,
        string_factory: Optional[str] = None,
        metric_type: Optional[int] = None,
        custom_index: Optional["faiss.Index"] = None,  # noqa: F821
        train_size: Optional[int] = None,
        faiss_verbose: bool = False,
        dtype=np.float32,
    ):
        """ Add a dense index using Faiss for fast retrieval.
            The index is created using the vectors of `external_arrays`.
            You can specify `device` if you want to run it on GPU (`device` must be the GPU index).
            You can find more information about Faiss here:
            - For `string factory`: https://github.com/facebookresearch/faiss/wiki/The-index-factory

            Args:
                `external_arrays` (`np.array`): If you want to use arrays from outside the lib for the index, you can set `external_arrays`.
                    It will use `external_arrays` to create the Faiss index instead of the arrays in the given `column`.
                `index_name` (`str`): The index_name/identifier of the index. This is the index_name that is used to call `.get_nearest` or `.search`.
                `device` (Optional `int`): If not None, this is the index of the GPU to use. By default it uses the CPU.
                `string_factory` (Optional `str`): This is passed to the index factory of Faiss to create the index. Default index class is IndexFlatIP.
                `metric_type` (Optional `int`): Type of metric. Ex: faiss.faiss.METRIC_INNER_PRODUCT or faiss.METRIC_L2.
                `custom_index` (Optional `faiss.Index`): Custom Faiss index that you already have instantiated and configured for your needs.
                `train_size` (Optional `int`): If the index needs a training step, specifies how many vectors will be used to train the index.
                `faiss_verbose` (`bool`, defaults to False): Enable the verbosity of the Faiss index.
                `dtype` (data-type): The dtype of the numpy arrays that are indexed. Default is np.float32.
        """
        super().add_faiss_index_from_external_arrays(
            external_arrays=external_arrays.astype(dtype),
            index_name=index_name,
            device=device,
            string_factory=string_factory,
            metric_type=metric_type,
            custom_index=custom_index,
            train_size=train_size,
            faiss_verbose=faiss_verbose,
        )

    def add_elasticsearch_index(
        self,
        column: str,
        index_name: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        es_client: Optional["elasticsearch.Elasticsearch"] = None,  # noqa: F821
        es_index_name: Optional[str] = None,
        es_index_config: Optional[dict] = None,
    ):
        """ Add a text index using ElasticSearch for fast retrieval. This is done in-place.

            Examples of usage:

            ```
            es_client = elasticsearch.Elasticsearch()
            ds = nlp.load_dataset('crime_and_punish', split='train')
            ds.add_elasticsearch_index(column='line', es_client=es_client, es_index_name="my_es_index")
            scores, retrieved_examples = ds.get_nearest_examples('line', 'my new query', k=10)
            ```

            Args:
                `column` (`str`): The column of the documents to add to the index.
                `index_name` (Optional `str`): The index_name/identifier of the index. This is the index name that is used to call `.get_nearest` or `.search`.
                    By defaul it corresponds to `column`.
                `documents` (`Union[List[str], nlp.Dataset]`): The documents to index. It can be a `nlp.Dataset`.
                `es_client` (`elasticsearch.Elasticsearch`): The elasticsearch client used to create the index.
                `es_index_name` (Optional `str`): The elasticsearch index name used to create the index.
                `es_index_config` (Optional `dict`): The configuration of the elasticsearch index.
                    Default config is
                    {
                        "settings": {
                            "number_of_shards": 1,
                            "analysis": {"analyzer": {"stop_standard": {"type": "standard", " stopwords": "_english_"}}},
                        },
                        "mappings": {
                            "properties": {
                                "text": {"type": "text", "analyzer": "standard", "similarity": "BM25"},
                            }
                        },
                    }
        """
        with self.formated_as(type=None, columns=[column]):
            super().add_elasticsearch_index(
                column=column, host=host, port=port, es_client=es_client, index_name=index_name
            )
        return self
