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
import copy
import json
import os
import pickle
import shutil
import tempfile
from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import asdict
from functools import partial, wraps
from math import ceil, floor
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import pyarrow as pa
from multiprocess import Pool, RLock
from tqdm.auto import tqdm

from .arrow_reader import ArrowReader
from .arrow_writer import ArrowWriter, TypedSequence
from .features import Features, Value, cast_to_python_objects, pandas_types_mapper
from .fingerprint import fingerprint, generate_fingerprint, update_fingerprint
from .info import DatasetInfo
from .search import IndexableMixin
from .splits import NamedSplit
from .utils import map_nested
from .utils.logging import WARNING, get_logger, get_verbosity, set_verbosity_warning


if TYPE_CHECKING:
    from .dataset_dict import DatasetDict

logger = get_logger(__name__)

if int(pa.__version__.split(".")[0]) == 0:
    PYARROW_V0 = True
else:
    PYARROW_V0 = False


class DatasetInfoMixin(object):
    """This base class exposes some attributes of DatasetInfo
    at the base level of the Dataset for easy access.
    """

    def __init__(self, info: DatasetInfo, split: Optional[NamedSplit]):
        self._info = info
        self._split = split

    @property
    def info(self):
        """ :class:`datasets.DatasetInfo` object containing all the metadata in the dataset."""
        return self._info

    @property
    def split(self):
        """ :class:`datasets.DatasetInfo` object containing all the metadata in the dataset."""
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
    def features(self) -> Features:
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


def transmit_format(func):
    """Wrapper for dataset transforms that are not in-place to transmit the format of the original dataset to the new dataset"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            self: "Dataset" = args[0]
            args = args[1:]
        else:
            self: "Dataset" = kwargs.pop("self")
        # don't use self.format since it returns a list of columns for 'columns' even if self_format_columns is None
        unformatted_columns = set(self.column_names) - set(self._format_columns or [])
        self_format = {
            "type": self._format_type,
            "format_kwargs": self._format_kwargs,
            "columns": self._format_columns,
            "output_all_columns": self._output_all_columns,
        }
        # apply actual function
        out: Union["Dataset", "DatasetDict"] = func(self, *args, **kwargs)
        datasets: List["Dataset"] = list(out.values()) if isinstance(out, dict) else [out]
        # re-apply format to the output
        for dataset in datasets:
            new_format = dict(self_format)
            if new_format["columns"] is not None:  # new formatted columns = (columns - previously unformatted columns)
                new_format["columns"] = list(set(dataset.column_names) - unformatted_columns)
            out_format = {
                "type": dataset._format_type,
                "format_kwargs": dataset._format_kwargs,
                "columns": dataset._format_columns,
                "output_all_columns": dataset._output_all_columns,
            }
            if out_format != new_format:  # only apply if there's a change not to update the fingerprint for nothing
                dataset.set_format(**new_format)
        return out

    wrapper._decorator_name_ = "transmit_format"
    return wrapper


class Dataset(DatasetInfoMixin, IndexableMixin):
    """A Dataset backed by an Arrow table or Record Batch."""

    def __init__(
        self,
        arrow_table: pa.Table,
        data_files: Optional[List[dict]] = None,
        info: Optional[DatasetInfo] = None,
        split: Optional[NamedSplit] = None,
        indices_table: Optional[pa.Table] = None,
        indices_data_files: Optional[List[dict]] = None,
        fingerprint: Optional[str] = None,
        inplace_history: Optional[List[dict]] = None,
    ):
        info = info.copy() if info is not None else DatasetInfo()
        DatasetInfoMixin.__init__(self, info=info, split=split)
        IndexableMixin.__init__(self)
        self._data: pa.Table = arrow_table
        self._indices: Optional[pa.Table] = indices_table
        self._data_files: List[dict] = data_files if data_files is not None else []
        self._indices_data_files: List[dict] = indices_data_files if indices_data_files is not None else []
        self._inplace_history: List[dict] = (
            inplace_history
            if inplace_history is not None
            else [{"transforms": []} for _ in range(len(self._data_files))]
        )
        self._format_type: Optional[str] = None
        self._format_kwargs: dict = {}
        self._format_columns: Optional[list] = None
        self._output_all_columns: bool = False
        self._fingerprint: str = fingerprint

        # Read metadata

        if self._data.schema.metadata is not None and "huggingface".encode("utf-8") in self._data.schema.metadata:
            metadata = json.loads(self._data.schema.metadata["huggingface".encode("utf-8")].decode())
            if "info" in metadata and self.info.features is None:  # try to load features from the arrow file metadata
                self._info.features = DatasetInfo.from_dict(metadata["info"]).features
            if (
                "fingerprint" in metadata and self._fingerprint is None
            ):  # try to load fingerprint from the arrow file metadata
                self._fingerprint = metadata["fingerprint"]

        # Infer features if None

        inferred_features = Features.from_arrow_schema(arrow_table.schema)
        if self.info.features is None:
            self.info.features = inferred_features

        # Infer fingerprint if None

        if self._fingerprint is None:
            self._fingerprint = generate_fingerprint(self)

        # Sanity checks

        assert self.features is not None, "Features can't be None in a Dataset object"
        assert self._fingerprint is not None, "Fingerprint can't be None in a Dataset object"
        if self.info.features.type != inferred_features.type:
            raise ValueError(
                "External features info don't match the dataset:\nGot\n{}\nwith type\n{}\n\nbut expected something like\n{}\nwith type\n{}".format(
                    self.info.features, self.info.features.type, inferred_features, inferred_features.type
                )
            )

        if self._indices is not None:
            assert pa.types.is_unsigned_integer(
                self._indices.column(0)[0].type
            ), f"indices must be an Arrow table of unsigned integers, current type is {self._indices.column(0)[0].type}"

    @classmethod
    def from_file(
        cls,
        filename: str,
        info: Optional[DatasetInfo] = None,
        split: Optional[NamedSplit] = None,
        indices_filename: Optional[str] = None,
    ) -> "Dataset":
        """ Instantiate a Dataset backed by an Arrow table at filename """
        mmap = pa.memory_map(filename)
        f = pa.ipc.open_stream(mmap)
        pa_table = f.read_all()
        data_files = [{"filename": filename}]

        if indices_filename is not None:
            indices_mmap = pa.memory_map(indices_filename)
            indices_f = pa.ipc.open_stream(indices_mmap)
            indices_pa_table = indices_f.read_all()
            indices_data_files = [{"filename": indices_filename}]
        else:
            indices_pa_table = None
            indices_data_files = None

        return cls(
            arrow_table=pa_table,
            data_files=data_files,
            info=info,
            split=split,
            indices_table=indices_pa_table,
            indices_data_files=indices_data_files,
        )

    @classmethod
    def from_buffer(
        cls,
        buffer: pa.Buffer,
        info: Optional[DatasetInfo] = None,
        split: Optional[NamedSplit] = None,
        indices_buffer: Optional[pa.Buffer] = None,
    ) -> "Dataset":
        """ Instantiate a Dataset backed by an Arrow buffer """
        mmap = pa.BufferReader(buffer)
        f = pa.ipc.open_stream(mmap)
        pa_table = f.read_all()

        if indices_buffer is not None:
            indices_mmap = pa.BufferReader(indices_buffer)
            indices_f = pa.ipc.open_stream(indices_mmap)
            indices_pa_table = indices_f.read_all()
        else:
            indices_pa_table = None

        return cls(pa_table, info=info, split=split, indices_table=indices_pa_table)

    @classmethod
    def from_pandas(
        cls,
        df: pd.DataFrame,
        features: Optional[Features] = None,
        info: Optional[DatasetInfo] = None,
        split: Optional[NamedSplit] = None,
    ) -> "Dataset":
        """
        Convert :obj:``pandas.DataFrame`` to a "obj"``pyarrow.Table`` to create a :obj:``datasets.Dataset``.

        The column types in the resulting Arrow Table are inferred from the dtypes of the pandas.Series in the DataFrame. In the case of non-object
        Series, the NumPy dtype is translated to its Arrow equivalent. In the case of `object`, we need to guess the datatype by looking at the
        Python objects in this Series.

        Be aware that Series of the `object` dtype don't carry enough information to always lead to a meaningful Arrow type. In the case that
        we cannot infer a type, e.g. because the DataFrame is of length 0 or the Series only contains None/nan objects, the type is set to
        null. This behavior can be avoided by constructing explicit features and passing it to this function.

        Args:
            df (:obj:``pandas.DataFrame``): the dataframe that contains the dataset.
            features (:obj:``datasets.Features``, `optional`, defaults to :obj:``None``): If specified, the features types of the dataset
            info (:obj:``datasets.DatasetInfo``, `optional`, defaults to :obj:``None``): If specified, the dataset info containing info like
                description, citation, etc.
            split (:obj:``datasets.NamedSplit``, `optional`, defaults to :obj:``None``): If specified, the name of the dataset split.
        """
        if info is not None and features is not None and info.features != features:
            raise ValueError(
                "Features specified in `features` and `info.features` can't be different:\n{}\n{}".format(
                    features, info.features
                )
            )
        features = features if features is not None else info.features if info is not None else None
        if info is None:
            info = DatasetInfo()
        info.features = features
        pa_table: pa.Table = pa.Table.from_pandas(
            df=df, schema=pa.schema(features.type) if features is not None else None
        )
        return cls(pa_table, info=info, split=split)

    @classmethod
    def from_dict(
        cls,
        mapping: dict,
        features: Optional[Features] = None,
        info: Optional[Any] = None,
        split: Optional[Any] = None,
    ) -> "Dataset":
        """
        Convert :obj:``dict`` to a "obj"``pyarrow.Table`` to create a :obj:``datasets.Dataset``.

        Args:
            mapping (:obj:``mapping``): A mapping of strings to Arrays or Python lists.
            features (:obj:``datasets.Features``, `optional`, defaults to :obj:``None``): If specified, the features types of the dataset
            info (:obj:``datasets.DatasetInfo``, `optional`, defaults to :obj:``None``): If specified, the dataset info containing info like
                description, citation, etc.
            split (:obj:``datasets.NamedSplit``, `optional`, defaults to :obj:``None``): If specified, the name of the dataset split.
        """
        if info is not None and features is not None and info.features != features:
            raise ValueError(
                "Features specified in `features` and `info.features` can't be different:\n{}\n{}".format(
                    features, info.features
                )
            )
        features = features if features is not None else info.features if info is not None else None
        if info is None:
            info = DatasetInfo()
        info.features = features
        if features is not None:
            mapping = features.encode_batch(mapping)
        else:
            mapping = cast_to_python_objects(mapping)
        mapping = {
            col: TypedSequence(data, type=features.type[col].type if features is not None else None)
            for col, data in mapping.items()
        }
        pa_table: pa.Table = pa.Table.from_pydict(mapping=mapping)
        return cls(pa_table, info=info, split=split)

    def __del__(self):
        if hasattr(self, "_data"):
            del self._data
        if hasattr(self, "_indices"):
            del self._indices

    def __getstate__(self):
        state = dict(self.__dict__)
        state["_info"] = json.dumps(asdict(state["_info"]))
        state["_split"] = str(state["_split"]) if state["_split"] is not None else None
        if self._data_files:
            state["_data"] = None
        if self._indices_data_files:
            state["_indices"] = None
        logger.debug("Copying history")
        state["_inplace_history"] = [{"transforms": list(h["transforms"])} for h in state["_inplace_history"]]
        return state

    def __setstate__(self, state):
        assert (
            state.get("_data") is not None or state.get("_data_files") is not None
        ), "tried to unpickle a dataset without arrow_table or data_files"
        state = dict(state)
        state["_info"] = DatasetInfo.from_dict(json.loads(state["_info"]))
        state["_split"] = NamedSplit(state["_split"]) if state["_split"] is not None else None
        self.__dict__ = state
        reader = ArrowReader("", self.info)
        # Read arrow tables
        if self._data is None and self._data_files:
            tables = []
            for data_file, inplace_hist_per_file in zip(self._data_files, self._inplace_history):
                # Replay in-place history of transforms (cast_, rename_column_, etc.)
                pa_table = reader._read_files([data_file])
                sub_dataset = Dataset(pa_table, fingerprint="")
                for inplace_transform_name, args, kwargs in inplace_hist_per_file["transforms"]:
                    getattr(sub_dataset, inplace_transform_name)(*args, **kwargs)
                tables.append(sub_dataset._data)
            tables = [t for t in tables if len(t) > 0]
            # fix all-empty tables
            tables = tables or [pa.Table.from_batches([], schema=pa.schema(self.info.features.type))]
            self._data = pa.concat_tables(tables)
        reader = ArrowReader("", DatasetInfo(features=Features({"indices": Value("int64")})))
        if self._indices is None and self._indices_data_files:
            self._indices = reader._read_files(self._indices_data_files)

    def save_to_disk(self, dataset_path: str):
        """
        Save the dataset in a dataset directory

        Args:
            dataset_path (``str``): path of the dataset directory where the dataset will be saved to
        """
        assert (
            not self.list_indexes()
        ), "please remove all the indexes using `dataset.drop_index` before saving a dataset"
        self = pickle.loads(pickle.dumps(self))
        os.makedirs(dataset_path, exist_ok=True)
        # Write indices if needed
        if self._indices is not None:
            if not self._indices_data_files:
                cache_file_name = os.path.join(dataset_path, "indices.arrow")
                writer = ArrowWriter(path=cache_file_name)
                writer.write_table(self._indices)
                writer.finalize()
                self._indices_data_files = [{"filename": cache_file_name}]
        # Write dataset if needed
        if not self._data_files or any(len(h["transforms"]) > 0 for h in self._inplace_history):
            cache_file_name = os.path.join(dataset_path, "dataset.arrow")
            writer = ArrowWriter(path=cache_file_name)
            writer.write_table(self._data)
            writer.finalize()
            self._data_files = [{"filename": cache_file_name}]
            self._inplace_history = [{"transforms": []}]
        # Copy all files into the dataset directory
        for data_file in self._data_files + self._indices_data_files:
            # Copy file to destination directory
            src = data_file["filename"]
            filename = Path(src).name
            dest = os.path.join(dataset_path, filename)
            if src != dest:
                shutil.copy(src, dest)
            # Change path to relative path from inside the destination directory
            data_file["filename"] = filename
        # Get state
        state = self.__getstate__()
        dataset_info = json.loads(state.pop("_info"))
        assert state.get("_data") is None, "arrow table needs to be memory mapped"
        assert state.get("_indices") is None, "arrow table needs to be memory mapped"
        assert all(
            len(h["transforms"]) == 0 for h in state.get("_inplace_history", [])
        ), "in-place history needs to be empty"
        # Serialize state
        with open(os.path.join(dataset_path, "state.json"), "w", encoding="utf-8") as state_file:
            json.dump(state, state_file, indent=2, sort_keys=True)
        with open(os.path.join(dataset_path, "dataset_info.json"), "w", encoding="utf-8") as dataset_info_file:
            json.dump(dataset_info, dataset_info_file, indent=2, sort_keys=True)
        logger.info("Dataset saved in {}".format(dataset_path))

    @staticmethod
    def load_from_disk(dataset_path: str) -> "Dataset":
        """Load the dataset from a dataset directory

        Args:
            dataset_path (``str``): path of the dataset directory where the dataset will be loaded from
        """
        with open(os.path.join(dataset_path, "state.json"), "r", encoding="utf-8") as state_file:
            state = json.load(state_file)
        with open(os.path.join(dataset_path, "dataset_info.json"), "r", encoding="utf-8") as dataset_info_file:
            dataset_info = json.load(dataset_info_file)
        state["_info"] = json.dumps(dataset_info)
        dataset = Dataset.from_dict({})
        state = {k: state[k] for k in dataset.__dict__.keys()}  # in case we add new fields
        # Change path to absolute path
        for data_file in state.get("_data_files", []) + state.get("_indices_data_files", []):
            data_file["filename"] = os.path.join(dataset_path, data_file["filename"])
        dataset.__setstate__(state)
        return dataset

    @property
    def data(self) -> pa.Table:
        """The Apache Arrow table backing the dataset."""
        return self._data

    @property
    def cache_files(self):
        """The cache file containing the Apache Arrow table backing the dataset."""
        return self._data_files

    @property
    def num_columns(self) -> int:
        """Number of columns in the dataset."""
        return self._data.num_columns

    @property
    def num_rows(self) -> int:
        """Number of rows in the dataset (same as :func:`datasets.Dataset.__len__`)."""
        if self._indices is not None:
            return self._indices.num_rows
        return self._data.num_rows

    @property
    def column_names(self) -> List[str]:
        """Names of the columns in the dataset. """
        return self._data.column_names

    @property
    def shape(self) -> Tuple[int]:
        """Shape of the dataset (number of columns, number of rows)."""
        if self._indices is not None:
            return tuple(self._indices.num_rows, self._data.num_columns)
        return self._data.shape

    def unique(self, column: str) -> List[Any]:
        """Return a list of the unique elements in a column.

        This is implemented in the low-level backend and as such, very fast.

        Args:
            column (:obj:`str`):
                column name (list all the column names with :func:`datasets.Dataset.column_names`)

        Returns: :obj:`list` of unique elements in the given column.

        """
        if column not in self._data.column_names:
            raise ValueError(f"Column ({column}) not in table columns ({self._data.column_names}).")

        if self._indices is not None and self._indices.num_rows != self._data.num_rows:
            raise ValueError(
                f"This dataset is a shallow copy using an indices mapping of another Datset {self._data.num_rows}."
                f"The `Dataset.unique()` method is currently not handled on shallow copy. Please use `Dataset.flatten_indices()` "
                f"to create a deep copy of the dataset and be able to use `Dataset.unique()`."
            )

        return self._data.column(column).unique().to_pylist()

    @fingerprint(inplace=True)
    def dictionary_encode_column_(self, column: str):
        """Dictionary encode a column.

            Dictionary encode can reduce the size of a column with many repetitions (e.g. string labels columns)
            by storing a dictionary of the strings. This only affect the internal storage.

        Args:
            column (:obj:`str`):

        """
        if column not in self._data.column_names:
            raise ValueError(f"Column ({column}) not in table columns ({self._data.column_names}).")
        casted_schema: pa.Schema = self._data.schema
        field_index = casted_schema.get_field_index(column)
        field: pa.Field = casted_schema.field(field_index)
        casted_field = pa.field(field.name, pa.dictionary(pa.int32(), field.type), nullable=False)
        casted_schema.set(field_index, casted_field)
        self._data = self._data.cast(casted_schema)
        self.info.features = Features.from_arrow_schema(self._data.schema)

    @fingerprint(inplace=True)
    def flatten_(self, max_depth=16):
        """Flatten the Table.
        Each column with a struct type is flattened into one column per struct field.
        Other columns are left unchanged.
        """
        for depth in range(1, max_depth):
            if any(isinstance(field.type, pa.StructType) for field in self._data.schema):
                self._data = self._data.flatten()
            else:
                break
        if self.info is not None:
            self.info.features = Features.from_arrow_schema(self._data.schema)
        logger.info(
            "Flattened dataset from depth {} to depth {}.".format(depth, 1 if depth + 1 < max_depth else "unknown")
        )

    @fingerprint(inplace=True)
    def cast_(self, features: Features):
        """
        Cast the dataset to a new set of features.

        You can also remove a column using :func:`Dataset.map` with `feature` but :func:`cast_`
        is in-place (doesn't copy the data to a new dataset) and is thus faster.

        Args:
            features (:class:`datasets.Features`): New features to cast the dataset to.
                The name of the fields in the features must match the current column names.
                The type of the data must also be convertible from one type to the other.
                For non-trivial conversion, e.g. string <-> ClassLabel you should use :func:`map` to update the Dataset.
        """
        if sorted(features) != sorted(self._data.column_names):
            raise ValueError(
                f"The columns in features ({list(features)}) must be identical "
                f"as the columns in the dataset: {self._data.column_names}"
            )

        self._info.features = features
        type = features.type
        schema = pa.schema({col_name: type[col_name].type for col_name in self._data.column_names})
        self._data = self._data.cast(schema)

    @fingerprint(inplace=True)
    def remove_columns_(self, column_names: Union[str, List[str]]):
        """
        Remove one or several column(s) in the dataset and
        the features associated to them.

        You can also remove a column using :func:`Dataset.map` with `remove_columns` but the present method
        is in-place (doesn't copy the data to a new dataset) and is thus faster.

        Args:
            column_names (:obj:`Union[str, List[str]]`): Name of the column(s) to remove.
        """
        if isinstance(column_names, str):
            column_names = [column_names]

        for column_name in column_names:
            if column_name not in self._data.column_names:
                raise ValueError(
                    f"Column name {column_name} not in the dataset. "
                    f"Current columns in the dataset: {self._data.column_names}"
                )

        for column_name in column_names:
            del self._info.features[column_name]

        self._data = self._data.drop(column_names)

    @fingerprint(inplace=True)
    def rename_column_(self, original_column_name: str, new_column_name: str):
        """
        Rename a column in the dataset and move the features associated to the original column under the new column name.

        You can also rename a column using :func:`Dataset.map` with `remove_columns` but the present method:
            - takes care of moving the original features under the new column name.
            - doesn't copy the data to a new dataset and is thus much faster.

        Args:
            original_column_name (:obj:`str`): Name of the column to rename.
            new_column_name (:obj:`str`): New name for the column.
        """
        if original_column_name not in self._data.column_names:
            raise ValueError(
                f"Original column name {original_column_name} not in the dataset. "
                f"Current columns in the dataset: {self._data.column_names}"
            )
        if new_column_name in self._data.column_names:
            raise ValueError(
                f"New column name {original_column_name} already in the dataset. "
                f"Please choose a column name which is not already in the dataset. "
                f"Current columns in the dataset: {self._data.column_names}"
            )
        if not new_column_name:
            raise ValueError("New column name is empty.")

        new_column_names = [new_column_name if col == original_column_name else col for col in self._data.column_names]

        self._info.features[new_column_name] = self._info.features[original_column_name]
        del self._info.features[original_column_name]

        self._data = self._data.rename_columns(new_column_names)

    def __len__(self):
        """ Number of rows in the dataset """
        return self.num_rows

    def __iter__(self):
        """Iterate through the examples.
        If a formatting is set with :func:`datasets.Dataset.set_format` rows will be returned with the
        selected format.
        """
        format_type = self._format_type
        format_kwargs = self._format_kwargs
        format_columns = self._format_columns
        output_all_columns = self._output_all_columns
        for index in range(self.num_rows):
            yield self._getitem(
                index,
                format_type=format_type,
                format_columns=format_columns,
                output_all_columns=output_all_columns,
                format_kwargs=format_kwargs,
            )

    def __repr__(self):
        return f"Dataset({{\n    features: {list(self.features.keys())},\n    num_rows: {self.num_rows}\n}})"

    @property
    def format(self):
        return {
            "type": self._format_type,
            "format_kwargs": self._format_kwargs,
            "columns": self.column_names if self._format_columns is None else self._format_columns,
            "output_all_columns": self._output_all_columns,
        }

    @contextlib.contextmanager
    def formatted_as(
        self,
        type: Optional[str] = None,
        columns: Optional[List] = None,
        output_all_columns: bool = False,
        **format_kwargs,
    ):
        """To be used in a `with` statement. Set __getitem__ return format (type and columns)

        Args:
            type (Optional ``str``): output type selected in [None, 'numpy', 'torch', 'tensorflow', 'pandas']
                None means __getitem__ returns python objects (default)
            columns (Optional ``List[str]``): columns to format in the output
                None means __getitem__ returns all columns (default)
            output_all_columns (``bool`` default to False): keep un-formatted columns as well in the output (as python objects)
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

    @fingerprint(inplace=True)
    def set_format(
        self,
        type: Optional[str] = None,
        columns: Optional[List] = None,
        output_all_columns: bool = False,
        **format_kwargs,
    ):
        """Set __getitem__ return format (type and columns)

        Args:
            type (Optional ``str``): output type selected in [None, 'numpy', 'torch', 'tensorflow', 'pandas']
                None means __getitem__ returns python objects (default)
            columns (Optional ``List[str]``): columns to format in the output
                None means __getitem__ returns all columns (default)
            output_all_columns (``bool`` default to False): keep un-formatted columns as well in the output (as python objects)
            format_kwargs: keywords arguments passed to the convert function like `np.array`, `torch.tensor` or `tensorflow.ragged.constant`.
        """
        # Check return type
        if type in ["torch", "pytorch", "pt"]:
            try:
                import torch  # noqa: F401
            except ImportError:
                logger.error("PyTorch needs to be installed to be able to return PyTorch tensors.")
            type = "torch"
        elif type in ["tensorflow", "tf"]:
            try:
                import tensorflow  # noqa: F401
            except ImportError:
                logger.error("Tensorflow needs to be installed to be able to return Tensorflow tensors.")
            type = "tensorflow"
        elif type in ["numpy", "np"]:
            type = "numpy"
        elif type in ["pandas", "pd"]:
            type = "pandas"
        elif type in [None, "python"]:
            type = None
        else:
            assert not (
                type == "pandas" and (output_all_columns or format_kwargs)
            ), "Format type 'pandas' doesn't allow the use of `output_all_columns` or `**format_kwargs`."
            assert (
                type is None or type == "numpy" or type == "pandas"
            ), "Return type should be None or selected in ['numpy', 'torch', 'tensorflow', 'pandas'], but got '{}'".format(
                type
            )

        # Check filter column
        if isinstance(columns, str):
            columns = [columns]
        if columns is not None and any(col not in self._data.column_names for col in columns):
            raise ValueError(
                "Columns {} not in the dataset. Current columns in the dataset: {}".format(
                    list(filter(lambda col: col not in self._data.column_names, columns)), self._data.column_names
                )
            )

        format_kwargs.update(format_kwargs.pop("format_kwargs", {}))  # allow to use self.set_format(self.format)
        self._format_type = type
        self._format_kwargs = format_kwargs
        self._format_columns = columns
        self._output_all_columns = output_all_columns
        logger.info(
            "Set __getitem__(key) output type to %s for %s columns "
            " (when key is int or slice) and %s output other (un-formatted) columns.",
            "python objects" if type is None else type,
            "no" if columns is None else str(columns),
            "do" if output_all_columns else "don't",
        )

    def reset_format(self):
        """Reset __getitem__ return format to python objects and all columns.

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
            if "copy" not in format_kwargs:
                format_kwargs["copy"] = False
            command = partial(np.array, **format_kwargs)
            map_nested_kwargs["map_list"] = False  # convert lists to arrays
        elif format_type == "torch":
            import torch

            map_nested_kwargs["map_list"] = False  # convert lists to tensors

            def command(x):
                if isinstance(
                    x, (list, tuple, np.ndarray)
                ):  # add support for nested types like struct of list of struct
                    x = np.array(x, copy=False)
                    if x.dtype == np.object:  # pytorch tensors cannot be instantied from an array of objects
                        return [map_nested(command, i, **map_nested_kwargs) for i in x]
                return torch.tensor(x, **format_kwargs)

        elif format_type == "tensorflow":
            import tensorflow

            map_nested_kwargs["map_list"] = False  # convert lists to tensors

            def command(x):
                if isinstance(
                    x, (list, tuple, np.ndarray)
                ):  # add support for nested types like struct of list of struct
                    x = np.array(x, copy=False)
                    if x.dtype == np.object:  # tensorflow tensors can sometimes be instantied from an array of objects
                        try:
                            return tensorflow.ragged.constant(x, **format_kwargs)
                        except ValueError:
                            return [map_nested(command, i, **map_nested_kwargs) for i in x]
                return tensorflow.ragged.constant(x, **format_kwargs)

        else:

            def identity(x):
                return x

            command = identity
        if isinstance(outputs, (list, tuple, np.ndarray, pd.Series)):
            return command(outputs)
        elif isinstance(outputs, pd.DataFrame):
            if format_columns is not None and not output_all_columns:
                to_remove_columns = [col for col in self.column_names if col not in format_columns]
                output_dict = outputs.drop(to_remove_columns, axis=1)
            else:
                output_dict = outputs
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

    def _map_indices(self, indices: Union[int, slice, pa.Array, Iterable]):
        if self._indices is None:
            return indices

        if isinstance(indices, int):
            return self._indices.column(0)[indices].as_py()

        slice_indices = None
        array_indices = None
        if isinstance(indices, slice):
            slice_indices = indices.indices(self.num_rows)
            # Check if the slice is a contiguous slice - else build an indices array
            if slice_indices[2] != 1 or slice_indices[1] < slice_indices[0]:
                array_indices = pa.array(list(range(*slice_indices)), type=pa.uint64())
        elif isinstance(indices, pa.Array):
            array_indices = indices
        elif isinstance(indices, Iterable):
            array_indices = pa.array([int(i) for i in indices], type=pa.uint64())

        # We can do a slice
        if array_indices is None:
            return self._indices.column(0).slice(slice_indices[0], slice_indices[1] - slice_indices[0])

        # We cannot do a slice, we need to do a take or some concatenation on pyarrow < 1.0.0
        if PYARROW_V0:  # pre-1.0.0 backward compatibility
            data_array = pa.concat_tables(self._indices.slice(i.as_py(), 1) for i in array_indices).column(0)
        else:
            data_array = self._indices.column(0).take(array_indices)

        return data_array

    def _getitem(
        self,
        key: Union[int, slice, str],
        format_type=None,
        format_columns=None,
        output_all_columns=False,
        format_kwargs=None,
    ) -> Union[Dict, List]:
        """
        Can be used to index columns (by string names) or rows (by integer index, slices, or iter of indices or bools)
        """
        # In the following, to convert data from the arrow table to dicts or lists,
        # we use .to_pandas().to_dict() or .to_pandas().to_list() as they are
        # significantly faster than .to_pydict() thanks to zero-copy and because it doesn't
        # call `list()` on every object in sequences of sequences of objects for example
        if isinstance(key, int):
            if key < 0:
                key = self.num_rows + key
            if key >= self.num_rows or key < 0:
                raise IndexError(f"Index ({key}) outside of table length ({self.num_rows}).")

            # Check if we need to convert indices
            key = self._map_indices(key)

            if format_type is not None:
                if format_type == "pandas":
                    outputs = self._data.slice(key, 1).to_pandas(types_mapper=pandas_types_mapper)
                else:
                    outputs = self._unnest(
                        self._data.slice(key, 1).to_pandas(types_mapper=pandas_types_mapper).to_dict("list")
                    )
            else:
                outputs = self._unnest(self._data.slice(key, 1).to_pydict())

        elif isinstance(key, slice):
            indices_array = None
            key_indices = key.indices(self.num_rows)

            # Check if the slice is a contiguous slice - else build an indices array
            if key_indices[2] != 1 or key_indices[1] < key_indices[0]:
                indices_array = pa.array(list(range(*key)), type=pa.uint64())

            # Check if we need to convert indices
            if self._indices is not None:
                indices_array = self._map_indices(indices_array if indices_array else key)
                # TODO: here we could add a check that the resulting indices are a contiguous slice
                # to avoid using 'take' instead of 'slice'

            # Get the subset of the table
            if indices_array is not None:
                # if PYARROW_V0:  # don't use take (see https://issues.apache.org/jira/browse/ARROW-9773)
                data_subset = pa.concat_tables(
                    self._data.slice(indices_array[i].as_py(), 1) for i in range(len(indices_array))
                )
                # else:
                #     data_subset = self._data.take(indices_array)
            else:
                data_subset = self._data.slice(key_indices[0], key_indices[1] - key_indices[0])

            # Convert to the format
            if format_type is not None:
                if format_type == "pandas":
                    outputs = data_subset.to_pandas(types_mapper=pandas_types_mapper)
                else:
                    outputs = data_subset.to_pandas(types_mapper=pandas_types_mapper).to_dict("list")
            else:
                outputs = data_subset.to_pydict()

        elif isinstance(key, str):
            if key not in self._data.column_names:
                raise ValueError(f"Column ({key}) not in table columns ({self._data.column_names}).")

            # Check if we need to convert indices
            if self._indices is not None:
                indices_array = self._indices.column(0)
                # if PYARROW_V0:  # don't use take (see https://issues.apache.org/jira/browse/ARROW-9773)
                data_array = pa.concat_tables(self._data.slice(i.as_py(), 1) for i in indices_array).column(key)
                # else:
                #     data_array = self._data.column(key).take(indices_array)
            else:
                data_array = self._data.column(key)

            if format_type is not None:
                # We should use
                # outputs = self._data[key].to_pandas(types_mapper=pandas_types_mapper)
                # but there is a bug in pyarrow that makes ignores the types_mapper in that case
                # see https://issues.apache.org/jira/browse/ARROW-9664
                # We build a table with one column and call to_pandas on it instead
                one_column_table = pa.Table.from_arrays([data_array], schema=pa.schema([self._data.schema.field(key)]))
                if format_columns is None or key in format_columns:
                    if format_type == "pandas":
                        outputs = one_column_table.to_pandas(types_mapper=pandas_types_mapper)[key]
                    else:
                        outputs = one_column_table.to_pandas(types_mapper=pandas_types_mapper)[key].to_list()
                else:
                    outputs = one_column_table.to_pandas(types_mapper=pandas_types_mapper)[key].to_list()
            else:
                outputs = data_array.to_pylist()

        elif isinstance(key, Iterable):
            if len(key) > 0 and isinstance(key[0], (bool, np.bool_)):
                if len(key) != self.__len__():
                    raise ValueError(
                        f"Iterable with bool entries must be length of dataset ({self.__len__()}), " f"not {len(key)}"
                    )
                indices = [i for i, val in enumerate(key) if val]
            else:
                indices = key

            indices_array = pa.array([int(i) + len(self) if int(i) < 0 else int(i) for i in indices], type=pa.uint64())

            # Check if we need to convert indices
            indices_array = self._map_indices(indices_array)

            # TODO: here we could add a check that the resulting indices are a contiguous slice
            # to avoid using 'take' instead of 'slice'

            # if PYARROW_V0:  # don't use take (see https://issues.apache.org/jira/browse/ARROW-9773)
            data_subset = pa.concat_tables(
                self._data.slice(indices_array[i].as_py(), 1) for i in range(len(indices_array))
            )
            # else:
            #     data_subset = self._data.take(indices_array)

            if format_type is not None:
                if format_type == "pandas":
                    outputs = data_subset.to_pandas(types_mapper=pandas_types_mapper)
                else:
                    outputs = data_subset.to_pandas(types_mapper=pandas_types_mapper).to_dict("list")
            else:
                outputs = data_subset.to_pydict()

        else:
            raise ValueError("Can only get row(s) (int or slice or list[int]) or columns (string).")

        if format_type is not None or format_columns is not None:
            outputs = self._convert_outputs(
                outputs,
                format_type=format_type,
                format_columns=format_columns,
                output_all_columns=output_all_columns,
                format_kwargs=format_kwargs,
            )
        return outputs

    def __getitem__(self, key: Union[int, slice, str]) -> Union[Dict, List]:
        """
        Can be used to index columns (by string names) or rows (by integer index or iterable of indices or bools)
        """
        return self._getitem(
            key,
            format_type=self._format_type,
            format_columns=self._format_columns,
            output_all_columns=self._output_all_columns,
            format_kwargs=self._format_kwargs,
        )

    def cleanup_cache_files(self):
        """Clean up all cache files in the dataset cache directory, excepted the currently used cache file if there is one.
        Be carefull when running this command that no other process is currently using other cache files.

        Return:
            Number of removed files
        """
        if not self._data_files or "filename" not in self._data_files[0]:
            return None
        current_cache_files = [os.path.abspath(cache_file["filename"]) for cache_file in self._data_files]
        cache_directory = os.path.dirname(current_cache_files[0])
        logger.info(f"Listing files in {cache_directory}")
        files: List[str] = os.listdir(cache_directory)
        files_to_remove = []
        for f_name in files:
            full_name = os.path.abspath(os.path.join(cache_directory, f_name))
            if f_name.startswith("cache-") and f_name.endswith(".arrow"):
                if full_name in current_cache_files:
                    logger.info(f"Keeping currently used cache file at {full_name}")
                    continue
                files_to_remove.append(full_name)
        for file_path in files_to_remove:
            logger.info(f"Removing {file_path}")
            os.remove(file_path)
        return len(files_to_remove)

    def _get_cache_file_path(self, fingerprint):
        cache_file_name = "cache-" + fingerprint + ".arrow"
        cache_directory = os.path.dirname(self._data_files[0]["filename"])
        cache_file_path = os.path.join(cache_directory, cache_file_name)
        return cache_file_path

    def map(
        self,
        function: Optional[Callable] = None,
        with_indices: bool = False,
        input_columns: Optional[Union[str, List[str]]] = None,
        batched: bool = False,
        batch_size: Optional[int] = 1000,
        drop_last_batch: bool = False,
        remove_columns: Optional[List[str]] = None,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
        features: Optional[Features] = None,
        disable_nullable: bool = False,
        fn_kwargs: Optional[dict] = None,
        num_proc: Optional[int] = None,
        suffix_template: str = "_{rank:05d}_of_{num_proc:05d}",
        new_fingerprint: Optional[str] = None,
    ) -> "Dataset":
        """Apply a function to all the elements in the table (individually or in batches)
        and update the table (if function does updated examples).

        Args:
            function (`callable`): with one of the following signature:
                - `function(example: Union[Dict, Any]) -> Union[Dict, Any]` if `batched=False` and `with_indices=False`
                - `function(example: Union[Dict, Any], indices: int) -> Union[Dict, Any]` if `batched=False` and `with_indices=True`
                - `function(batch: Union[Dict[List], List[Any]]) -> Union[Dict, Any]` if `batched=True` and `with_indices=False`
                - `function(batch: Union[Dict[List], List[Any]], indices: List[int]) -> Union[Dict, Any]` if `batched=True` and `with_indices=True`
                If no function is provided, default to identity function: lambda x: x
            with_indices (`bool`, defaults to `False`): Provide example indices to `function`. Note that in this case the signature of `function` should be `def function(example, idx): ...`.
            input_columns (`Optional[Union[str, List[str]]]`, defaults to `None`): The columns to be passed into `function` as
                positional arguments. If `None`, a dict mapping to all formatted columns is passed as one argument.
            batched (`bool`, defaults to `False`): Provide batch of examples to `function`
            batch_size (`Optional[int]`, defaults to `1000`): Number of examples per batch provided to `function` if `batched=True`
                `batch_size <= 0` or `batch_size == None`: Provide the full dataset as a single batch to `function`
            drop_last_batch (`bool`, default: `False`): Whether a last batch smaller than the batch_size should be
                dropped instead of being processed by the function.
            remove_columns (`Optional[List[str]]`, defaults to `None`): Remove a selection of columns while doing the mapping.
                Columns will be removed before updating the examples with the output of `function`, i.e. if `function` is adding
                columns with names in `remove_columns`, these columns will be kept.
            keep_in_memory (`bool`, defaults to `False`): Keep the dataset in memory instead of writing it to a cache file.
            load_from_cache_file (`bool`, defaults to `True`): If a cache file storing the current computation from `function`
                can be identified, use it instead of recomputing.
            cache_file_name (`Optional[str]`, defaults to `None`): Provide the name of a cache file to use to store the
                results of the computation instead of the automatically generated cache file name.
            writer_batch_size (`int`, defaults to `1000`): Number of rows per write operation for the cache file writer.
                Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
            features (`Optional[datasets.Features]`, defaults to `None`): Use a specific Features to store the cache file
                instead of the automatically generated one.
            disable_nullable (`bool`, defaults to `True`): Disallow null values in the table.
            fn_kwargs (`Optional[Dict]`, defaults to `None`): Keyword arguments to be passed to `function`
            num_proc (`Optional[int]`, defaults to `None`): Number of processes for multiprocessing. By default it doesn't
                use multiprocessing.
            suffix_template (`str`, defaults to "_{rank:05d}_of_{num_proc:05d}"): If cache_file_name is specified, then this suffix
                will be added at the end of the base name of each. For example, if cache_file_name is "processed.arrow", then for
                rank=1 and num_proc=4, the resulting file would be "processed_00001_of_00004.arrow" for the default suffix.
            new_fingerprint (`Optional[str]`, defaults to `None`): the new fingerprint of the dataset after transform.
                If `None`, the new fingerprint is computed using a hash of the previous fingerprint, and the transform arguments
        """
        assert num_proc is None or num_proc > 0, "num_proc must be an integer > 0."

        # If the array is empty we do nothing
        if len(self) == 0:
            return self

        if function is None:
            function = lambda x: x  # noqa: E731

        if isinstance(input_columns, str):
            input_columns = [input_columns]

        if input_columns is not None:
            for input_column in input_columns:
                if input_column not in self._data.column_names:
                    raise ValueError(
                        "Input column {} not in the dataset. Current columns in the dataset: {}".format(
                            input_column, self._data.column_names
                        )
                    )

        if fn_kwargs is None:
            fn_kwargs = dict()

        # Check if the function returns updated examples
        def does_function_return_dict(inputs, indices):
            """ Does the function returns a dict. """
            fn_args = [inputs] if input_columns is None else [inputs[col] for col in input_columns]
            processed_inputs = (
                function(*fn_args, indices, **fn_kwargs) if with_indices else function(*fn_args, **fn_kwargs)
            )
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
        logger.info("Testing the mapped function outputs")
        test_inputs = self[:2] if batched else self[0]
        test_indices = [0, 1] if batched else 0
        update_data = does_function_return_dict(test_inputs, test_indices)
        logger.info("Testing finished, running the mapping function on the dataset")

        if num_proc is None or num_proc == 1:
            return self._map_single(
                function=function,
                with_indices=with_indices,
                input_columns=input_columns,
                batched=batched,
                batch_size=batch_size,
                drop_last_batch=drop_last_batch,
                remove_columns=remove_columns,
                keep_in_memory=keep_in_memory,
                load_from_cache_file=load_from_cache_file,
                cache_file_name=cache_file_name,
                writer_batch_size=writer_batch_size,
                features=features,
                disable_nullable=disable_nullable,
                fn_kwargs=fn_kwargs,
                new_fingerprint=new_fingerprint,
                update_data=update_data,
            )
        else:

            def format_cache_file_name(cache_file_name, rank):
                sep = cache_file_name.rindex(".")
                base_name, extension = cache_file_name[:sep], cache_file_name[sep:]
                cache_file_name = base_name + suffix_template.format(rank=rank, num_proc=num_proc) + extension
                logger.info("Process #{} will write at {}".format(rank, cache_file_name))
                return cache_file_name

            prev_env = dict(os.environ)
            # check if parallelism if off
            # from https://github.com/huggingface/tokenizers/blob/bb668bc439dc34389b71dbb8ce0c597f15707b53/tokenizers/src/utils/parallelism.rs#L22
            if prev_env.get("TOKENIZERS_PARALLELISM", "false").lower() not in (
                "",
                "off",
                "false",
                "f",
                "no",
                "n",
                "0",
            ):
                logger.warning("Setting TOKENIZERS_PARALLELISM=false for forked processes.")
            os.environ["TOKENIZERS_PARALLELISM"] = "false"
            with Pool(num_proc, initargs=(RLock(),), initializer=tqdm.set_lock) as pool:
                os.environ = prev_env
                shards = [
                    self.shard(num_shards=num_proc, index=rank, contiguous=True, keep_in_memory=keep_in_memory)
                    for rank in range(num_proc)
                ]
                kwds_per_shard = [
                    dict(
                        self=shards[rank],
                        function=function,
                        with_indices=with_indices,
                        input_columns=input_columns,
                        batched=batched,
                        batch_size=batch_size,
                        drop_last_batch=drop_last_batch,
                        remove_columns=remove_columns,
                        keep_in_memory=keep_in_memory,
                        load_from_cache_file=load_from_cache_file,
                        cache_file_name=format_cache_file_name(cache_file_name, rank)
                        if cache_file_name is not None
                        else None,
                        writer_batch_size=writer_batch_size,
                        features=features.copy() if features is not None else None,
                        disable_nullable=disable_nullable,
                        fn_kwargs=fn_kwargs,
                        rank=rank,
                        offset=sum(len(s) for s in shards[:rank]),
                        update_data=update_data,
                    )
                    for rank in range(num_proc)
                ]
                logger.info("Spawning {} processes".format(num_proc))
                results = [pool.apply_async(self.__class__._map_single, kwds=kwds) for kwds in kwds_per_shard]
                transformed_shards = [r.get() for r in results]
                logger.info("Concatenating {} shards from multiprocessing".format(num_proc))
                result = concatenate_datasets(transformed_shards)
                if new_fingerprint is not None:
                    result._fingerprint = new_fingerprint
                return result

    @transmit_format
    @fingerprint(inplace=False)
    def _map_single(
        self,
        function: Optional[Callable] = None,
        with_indices: bool = False,
        input_columns: Optional[Union[str, List[str]]] = None,
        batched: bool = False,
        batch_size: Optional[int] = 1000,
        drop_last_batch: bool = False,
        remove_columns: Optional[List[str]] = None,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
        features: Optional[Features] = None,
        disable_nullable: bool = False,
        fn_kwargs: Optional[dict] = None,
        new_fingerprint: Optional[str] = None,
        rank: Optional[int] = None,
        offset: int = 0,
        update_data=True,
    ) -> "Dataset":
        """Apply a function to all the elements in the table (individually or in batches)
        and update the table (if function does updated examples).

        Args:
            function (`callable`): with one of the following signature:
                - `function(example: Union[Dict, Any]) -> Union[Dict, Any]` if `batched=False` and `with_indices=False`
                - `function(example: Union[Dict, Any], indices: int) -> Union[Dict, Any]` if `batched=False` and `with_indices=True`
                - `function(batch: Union[Dict[List], List[Any]]) -> Union[Dict, Any]` if `batched=True` and `with_indices=False`
                - `function(batch: Union[Dict[List], List[Any]], indices: List[int]) -> Union[Dict, Any]` if `batched=True` and `with_indices=True`
                If no function is provided, default to identity function: lambda x: x
            with_indices (`bool`, defaults to `False`): Provide example indices to `function`. Note that in this case the signature of `function` should be `def function(example, idx): ...`.
            input_columns (`Optional[Union[str, List[str]]]`, defaults to `None`): The columns to be passed into `function` as
                positional arguments. If `None`, a dict mapping to all formatted columns is passed as one argument.
            batched (`bool`, defaults to `False`): Provide batch of examples to `function`
            batch_size (`Optional[int]`, defaults to `1000`): Number of examples per batch provided to `function` if `batched=True`
                `batch_size <= 0` or `batch_size == None`: Provide the full dataset as a single batch to `function`
            drop_last_batch (`bool`, default: `False`): Whether a last batch smaller than the batch_size should be
                dropped instead of being processed by the function.
            remove_columns (`Optional[List[str]]`, defaults to `None`): Remove a selection of columns while doing the mapping.
                Columns will be removed before updating the examples with the output of `function`, i.e. if `function` is adding
                columns with names in `remove_columns`, these columns will be kept.
            keep_in_memory (`bool`, defaults to `False`): Keep the dataset in memory instead of writing it to a cache file.
            load_from_cache_file (`bool`, defaults to `True`): If a cache file storing the current computation from `function`
                can be identified, use it instead of recomputing.
            cache_file_name (`Optional[str]`, defaults to `None`): Provide the name of a cache file to use to store the
                results of the computation instead of the automatically generated cache file name.
            writer_batch_size (`int`, defaults to `1000`): Number of rows per write operation for the cache file writer.
                Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
            features (`Optional[datasets.Features]`, defaults to `None`): Use a specific Features to store the cache file
                instead of the automatically generated one.
            disable_nullable (`bool`, defaults to `True`): Disallow null values in the table.
            fn_kwargs (`Optional[Dict]`, defaults to `None`): Keyword arguments to be passed to `function`
            new_fingerprint (`Optional[str]`, defaults to `None`): the new fingerprint of the dataset after transform.
                If `None`, the new fingerprint is computed using a hash of the previous fingerprint, and the transform arguments
            rank: (`Optional[int]`, defaults to `None`): If specified, this is the process rank when doing multiprocessing
            offset: (`int`, defaults to 0): If specified, this is an offset applied to the indices passed to `function` if `with_indices=True`
            update_data (`bool`, defaults to `True`): If False, no new arrow table will be created
        """
        assert (
            not keep_in_memory or cache_file_name is None
        ), "Please use either `keep_in_memory` or `cache_file_name` but not both."

        not_verbose = bool(logger.getEffectiveLevel() > WARNING)

        # Reduce logging to keep things readable in multiprocessing with tqdm
        if rank is not None and get_verbosity() < WARNING:
            set_verbosity_warning()
        # Print at least one thing to fix tqdm in notebooks in multiprocessing
        # see https://github.com/tqdm/tqdm/issues/485#issuecomment-473338308
        if rank is not None and "notebook" in tqdm.__name__:
            print(" ", end="", flush=True)

        # Select the columns (arrow columns) to process
        if remove_columns is not None and any(col not in self._data.column_names for col in remove_columns):
            raise ValueError(
                "Column to remove {} not in the dataset. Current columns in the dataset: {}".format(
                    list(filter(lambda col: col not in self._data.column_names, remove_columns)),
                    self._data.column_names,
                )
            )

        if isinstance(input_columns, str):
            input_columns = [input_columns]

        if input_columns is not None:
            for input_column in input_columns:
                if input_column not in self._data.column_names:
                    raise ValueError(
                        "Input column {} not in the dataset. Current columns in the dataset: {}".format(
                            input_column, self._data.column_names
                        )
                    )

        if fn_kwargs is None:
            fn_kwargs = dict()

        # If we do batch computation but no batch sze is provided, default to the full dataset
        if batched and (batch_size is None or batch_size <= 0):
            batch_size = self.num_rows

        class NumExamplesMismatch(Exception):
            pass

        def apply_function_on_filtered_inputs(inputs, indices, check_same_num_examples=False, offset=0):
            """ Utility to apply the function on a selection of columns. """
            fn_args = [inputs] if input_columns is None else [inputs[col] for col in input_columns]
            if offset == 0:
                effective_indices = indices
            else:
                effective_indices = [i + offset for i in indices] if isinstance(indices, list) else indices + offset
            processed_inputs = (
                function(*fn_args, effective_indices, **fn_kwargs) if with_indices else function(*fn_args, **fn_kwargs)
            )
            if not update_data:
                return None  # Nothing to update, let's move on
            if remove_columns is not None:
                for column in remove_columns:
                    inputs.pop(column)
            if self._format_type is not None:
                inputs = self._getitem(
                    key=(indices if isinstance(indices, int) else slice(indices[0], indices[-1] + 1)),
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

        # Check if we've already cached this computation (indexed by a hash)
        if update_data and self._data_files:
            if cache_file_name is None:
                # we create a unique hash from the function, current dataset file and the mapping args
                cache_file_name = self._get_cache_file_path(new_fingerprint)
            if os.path.exists(cache_file_name) and load_from_cache_file:
                logger.warning("Loading cached processed dataset at %s", cache_file_name)
                info = self.info.copy()
                info.features = features
                return Dataset.from_file(cache_file_name, info=info, split=self.split)

        # Prepare output buffer and batched writer in memory or on file if we update the table
        if update_data:
            if features is None:
                features = self.features
                update_features = True
            else:
                update_features = False
            if keep_in_memory or cache_file_name is None:
                buf_writer = pa.BufferOutputStream()
                tmp_file = None
                writer = ArrowWriter(
                    features=features,
                    stream=buf_writer,
                    writer_batch_size=writer_batch_size,
                    update_features=update_features,
                    fingerprint=new_fingerprint,
                )
            else:
                buf_writer = None
                logger.info("Caching processed dataset at %s", cache_file_name)
                tmp_file = tempfile.NamedTemporaryFile("wb", dir=os.path.dirname(cache_file_name), delete=False)
                writer = ArrowWriter(
                    features=features,
                    path=tmp_file.name,
                    writer_batch_size=writer_batch_size,
                    update_features=update_features,
                    fingerprint=new_fingerprint,
                )

        try:
            # Loop over single examples or batches and write to buffer/file if examples are to be updated
            pbar_iterable = self if not batched else range(0, len(self), batch_size)
            pbar_unit = "ex" if not batched else "ba"
            pbar_desc = "#" + str(rank) if rank is not None else None
            pbar = tqdm(pbar_iterable, disable=not_verbose, position=rank, unit=pbar_unit, desc=pbar_desc)
            if not batched:
                for i, example in enumerate(pbar):
                    example = apply_function_on_filtered_inputs(example, i, offset=offset)
                    if update_data:
                        example = cast_to_python_objects(example)
                        writer.write(example)
            else:
                for i in pbar:
                    if drop_last_batch and i + batch_size > self.num_rows:
                        continue
                    batch = self[i : i + batch_size]
                    indices = list(range(*(slice(i, i + batch_size).indices(self.num_rows))))  # Something simpler?
                    try:
                        batch = apply_function_on_filtered_inputs(
                            batch, indices, check_same_num_examples=len(self.list_indexes()) > 0, offset=offset
                        )
                    except NumExamplesMismatch:
                        raise DatasetTransformationNotAllowedError(
                            "Using `.map` in batched mode on a dataset with attached indexes is allowed only if it doesn't create or remove existing examples. You can first run `.drop_index() to remove your index and then re-add it."
                        )
                    if update_data:
                        batch = cast_to_python_objects(batch)
                        writer.write_batch(batch)
            if update_data:
                writer.finalize()  # close_stream=bool(buf_writer is None))  # We only close if we are writing in a file
        except (Exception, KeyboardInterrupt):
            if update_data:
                writer.finalize()
            if update_data and tmp_file is not None:
                tmp_file.close()
                if os.path.exists(tmp_file.name):
                    os.remove(tmp_file.name)
            raise

        if update_data and tmp_file is not None:
            tmp_file.close()
            shutil.move(tmp_file.name, cache_file_name)

        if update_data:
            # Create new Dataset from buffer or file
            info = self.info.copy()
            info.features = writer._features
            if buf_writer is None:
                return Dataset.from_file(cache_file_name, info=info, split=self.split)
            else:
                return Dataset.from_buffer(buf_writer.getvalue(), info=info, split=self.split)
        else:
            return self

    @transmit_format
    @fingerprint(inplace=False)
    def filter(
        self,
        function: Optional[Callable] = None,
        with_indices=False,
        input_columns: Optional[Union[str, List[str]]] = None,
        batch_size: Optional[int] = 1000,
        remove_columns: Optional[List[str]] = None,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
        fn_kwargs: Optional[dict] = None,
        num_proc: Optional[int] = None,
        suffix_template: str = "_{rank:05d}_of_{num_proc:05d}",
        new_fingerprint: Optional[str] = None,
    ) -> "Dataset":
        """Apply a filter function to all the elements in the table in batches
        and update the table so that the dataset only includes examples according to the filter function.

        Args:
            function (`callable`): with one of the following signature:
                - `function(example: Union[Dict, Any]) -> bool` if `with_indices=False`
                - `function(example: Union[Dict, Any], indices: int) -> bool` if `with_indices=True`
                If no function is provided, default to an always True function: lambda x: True
            with_indices (`bool`, defaults to `False`): Provide example indices to `function`. Note that in this case the signature of `function` should be `def function(example, idx): ...`.
            input_columns (`Optional[Union[str, List[str]]]`, defaults to `None`): The columns to be passed into `function` as
                positional arguments. If `None`, a dict mapping to all formatted columns is passed as one argument.
            batch_size (`Optional[int]`, defaults to `1000`): Number of examples per batch provided to `function` if `batched=True`
                `batch_size <= 0` or `batch_size == None`: Provide the full dataset as a single batch to `function`
            remove_columns (`Optional[List[str]]`, defaults to `None`): Remove a selection of columns while doing the mapping.
                Columns will be removed before updating the examples with the output of `function`, i.e. if `function` is adding
                columns with names in `remove_columns`, these columns will be kept.
            keep_in_memory (`bool`, defaults to `False`): Keep the dataset in memory instead of writing it to a cache file.
            load_from_cache_file (`bool`, defaults to `True`): If a cache file storing the current computation from `function`
                can be identified, use it instead of recomputing.
            cache_file_name (`Optional[str]`, defaults to `None`): Provide the name of a cache file to use to store the
                results of the computation instead of the automatically generated cache file name.
            writer_batch_size (`int`, defaults to `1000`): Number of rows per write operation for the cache file writer.
                Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
            fn_kwargs (`Optional[Dict]`, defaults to `None`): Keyword arguments to be passed to `function`
            num_proc (`Optional[int]`, defaults to `None`): Number of processes for multiprocessing. By default it doesn't
                use multiprocessing.
            suffix_template (`str`, defaults to "_{rank:05d}_of_{num_proc:05d}"): If cache_file_name is specified, then this suffix
                will be added at the end of the base name of each. For example, if cache_file_name is "processed.arrow", then for
                rank=1 and num_proc=4, the resulting file would be "processed_00001_of_00004.arrow" for the default suffix.
            new_fingerprint (`Optional[str]`, defaults to `None`): the new fingerprint of the dataset after transform.
                If `None`, the new fingerprint is computed using a hash of the previous fingerprint, and the transform arguments
        """
        if len(self.list_indexes()) > 0:
            raise DatasetTransformationNotAllowedError(
                "Using `.filter` on a dataset with attached indexes is not allowed. You can first run `.drop_index() to remove your index and then re-add it.`"
            )

        if function is None:
            function = lambda x: True  # noqa: E731

        if isinstance(input_columns, str):
            input_columns = [input_columns]

        if input_columns is not None:
            for input_column in input_columns:
                if input_column not in self._data.column_names:
                    raise ValueError(
                        "Input column {} not in the dataset. Current columns in the dataset: {}".format(
                            input_column, self._data.column_names
                        )
                    )

        if fn_kwargs is None:
            fn_kwargs = dict()
        fn_kwargs["input_columns"] = input_columns

        # return map function
        return self.map(
            partial(map_function, function=function, with_indices=with_indices),
            batched=True,
            with_indices=with_indices,
            features=self.features,
            batch_size=batch_size,
            remove_columns=remove_columns,
            keep_in_memory=keep_in_memory,
            load_from_cache_file=load_from_cache_file,
            cache_file_name=cache_file_name,
            writer_batch_size=writer_batch_size,
            fn_kwargs=fn_kwargs,
            num_proc=num_proc,
            suffix_template=suffix_template,
            new_fingerprint=new_fingerprint,
        )

    @transmit_format
    @fingerprint(inplace=False)
    def flatten_indices(
        self,
        keep_in_memory: bool = False,
        cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
        features: Optional[Features] = None,
        disable_nullable: bool = True,
        new_fingerprint: Optional[str] = None,
    ) -> "Dataset":
        """Create and cache a new Dataset by flattening the indices mapping.

        Args:
            keep_in_memory (`bool`, default: `False`): Keep the dataset in memory instead of writing it to a cache file.
            cache_file_name (`Optional[str]`, defaults to `None`): Provide the name of a cache file to use to store the
                results of the computation instead of the automatically generated cache file name.
            writer_batch_size (`int`, defaults to `1000`): Number of rows per write operation for the cache file writer.
                Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
            features (`Optional[datasets.Features]`, default: `None`): Use a specific Features to store the cache file
                instead of the automatically generated one.
            disable_nullable (`bool`, default: `True`): Allow null values in the table.
            new_fingerprint (`Optional[str]`, defaults to `None`): the new fingerprint of the dataset after transform.
                If `None`, the new fingerprint is computed using a hash of the previous fingerprint, and the transform arguments
        """

        return self.map(
            batched=True,  # for speed
            keep_in_memory=keep_in_memory,
            cache_file_name=cache_file_name,
            writer_batch_size=writer_batch_size,
            features=features,
            disable_nullable=disable_nullable,
            new_fingerprint=new_fingerprint,
        )

    def _new_dataset_with_indices(
        self,
        indices_cache_file_name: Optional[str] = None,
        indices_buffer: Optional[pa.Buffer] = None,
        fingerprint: Optional[str] = None,
    ) -> "Dataset":
        """ Return a new Dataset obtained by adding indices (provided in indices_cache_file_name or in a buffer) to the current Dataset. """

        assert (
            indices_cache_file_name is not None or indices_buffer is not None
        ), "At least one of indices_cache_file_name or indices_buffer must be provided."

        assert fingerprint is not None, "please specify a fingerprint for the dataset with indices"
        data_files = self._data_files
        if indices_cache_file_name is not None:
            indices_mmap = pa.memory_map(indices_cache_file_name)
            if data_files is None:
                data_files = []
            indices_data_files = [{"filename": indices_cache_file_name}]
        else:
            indices_mmap = pa.BufferReader(indices_buffer)
            indices_data_files = None
        indices_f = pa.ipc.open_stream(indices_mmap)
        indices_pa_table = indices_f.read_all()

        # Return new Dataset object
        # don't forget to copy the objects
        return Dataset(
            self._data,
            data_files=copy.deepcopy(data_files),
            info=self.info.copy(),
            split=self.split,
            indices_table=indices_pa_table,
            indices_data_files=copy.deepcopy(indices_data_files),
            fingerprint=fingerprint,
            inplace_history=copy.deepcopy(
                self._inplace_history
            ),  # in-place transforms have to be kept as we kept the same data_files
        )

    @transmit_format
    @fingerprint(inplace=False)
    def select(
        self,
        indices: Iterable,
        keep_in_memory: bool = False,
        indices_cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
        new_fingerprint: Optional[str] = None,
    ) -> "Dataset":
        """Create a new dataset with rows selected following the list/array of indices.

        Args:
            `indices` (sequence, iterable, ndarray or Series): List or 1D-array of integer indices for indexing.
            `keep_in_memory` (`bool`, default: `False`): Keep the indices mapping in memory instead of writing it to a cache file.
            `indices_cache_file_name` (`Optional[str]`, default: `None`): Provide the name of a cache file to use to store the
                indices mapping instead of the automatically generated cache file name.
            `writer_batch_size` (`int`, default: `1000`): Number of rows per write operation for the cache file writer.
                Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
            new_fingerprint (`Optional[str]`, defaults to `None`): the new fingerprint of the dataset after transform.
                If `None`, the new fingerprint is computed using a hash of the previous fingerprint, and the transform arguments
        """
        assert (
            not keep_in_memory or indices_cache_file_name is None
        ), "Please use either `keep_in_memory` or `indices_cache_file_name` but not both."
        if len(self.list_indexes()) > 0:
            raise DatasetTransformationNotAllowedError(
                "Using `.select` on a dataset with attached indexes is not allowed. You can first run `.drop_index() to remove your index and then re-add it."
            )

        # If the array is empty we do nothing
        if len(self) == 0:
            return self

        # Prepare the writer for our indices arrow table
        if keep_in_memory or indices_cache_file_name is None:
            buf_writer = pa.BufferOutputStream()
            tmp_file = None
            writer = ArrowWriter(
                stream=buf_writer, writer_batch_size=writer_batch_size, fingerprint=new_fingerprint, unit="indices"
            )
        else:
            buf_writer = None
            logger.info("Caching indices mapping at %s", indices_cache_file_name)
            tmp_file = tempfile.NamedTemporaryFile("wb", dir=os.path.dirname(indices_cache_file_name), delete=False)
            writer = ArrowWriter(
                path=tmp_file.name, writer_batch_size=writer_batch_size, fingerprint=new_fingerprint, unit="indices"
            )

        indices_array = pa.array(indices, type=pa.uint64())
        # Check if we need to convert indices
        if self._indices is not None:
            if PYARROW_V0:
                indices_array = pa.concat_tables(self._indices.slice(i.as_py(), 1) for i in indices_array).column(0)
            else:
                indices_array = self._indices.column(0).take(indices_array)

        indices_table = pa.Table.from_arrays([indices_array], names=["indices"])

        try:
            writer.write_table(indices_table)
            writer.finalize()  # close_stream=bool(buf_writer is None))  # We only close if we are writing in a file
        except (Exception, KeyboardInterrupt):
            if tmp_file is not None:
                tmp_file.close()
                if os.path.exists(tmp_file.name):
                    os.remove(tmp_file.name)
            raise

        if tmp_file is not None:
            tmp_file.close()
            shutil.move(tmp_file.name, indices_cache_file_name)

        # Return new Dataset object
        if buf_writer is None:
            return self._new_dataset_with_indices(
                indices_cache_file_name=indices_cache_file_name, fingerprint=new_fingerprint
            )
        else:
            return self._new_dataset_with_indices(indices_buffer=buf_writer.getvalue(), fingerprint=new_fingerprint)

    @transmit_format
    @fingerprint(inplace=False)
    def sort(
        self,
        column: str,
        reverse: bool = False,
        kind: str = None,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        indices_cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
        new_fingerprint: Optional[str] = None,
    ) -> "Dataset":
        """Create a new dataset sorted according to a column.

        Currently sorting according to a column name uses numpy sorting algorithm under the hood.
        The column should thus be a numpy compatible type (in particular not a nested type).
        This also means that the column used for sorting is fully loaded in memory (which should be fine in most cases).

        Args:
            column (`str`): column name to sort by.
            reverse: (`bool`, defaults to `False`): If True, sort by descending order rather then ascending.
            kind (Optional `str`): Numpy algorithm for sorting selected in {‘quicksort’, ‘mergesort’, ‘heapsort’, ‘stable’},
                The default is ‘quicksort’. Note that both ‘stable’ and ‘mergesort’ use timsort under the covers and, in general,
                the actual implementation will vary with data type. The ‘mergesort’ option is retained for backwards compatibility.
            keep_in_memory (`bool`, defaults to `False`): Keep the sorted indices in memory instead of writing it to a cache file.
            load_from_cache_file (`bool`, defaults to `True`): If a cache file storing the sorted indices
                can be identified, use it instead of recomputing.
            indices_cache_file_name (`Optional[str]`, defaults to `None`): Provide the name of a cache file to use to store the
                sorted indices instead of the automatically generated cache file name.
            writer_batch_size (`int`, defaults to `1000`): Number of rows per write operation for the cache file writer.
                Higher value gives smaller cache files, lower value consume less temporary memory.
            new_fingerprint (`Optional[str]`, defaults to `None`): the new fingerprint of the dataset after transform.
                If `None`, the new fingerprint is computed using a hash of the previous fingerprint, and the transform arguments
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
                    column,
                    self._data.column_names,
                )
            )

        # Check if we've already cached this computation (indexed by a hash)
        if self._data_files:
            if indices_cache_file_name is None:
                # we create a unique hash from the function, current dataset file and the mapping args
                indices_cache_file_name = self._get_cache_file_path(new_fingerprint)
            if os.path.exists(indices_cache_file_name) and load_from_cache_file:
                logger.warning("Loading cached sorted indices for dataset at %s", indices_cache_file_name)
                return self._new_dataset_with_indices(
                    fingerprint=new_fingerprint, indices_cache_file_name=indices_cache_file_name
                )

        column_data = self._getitem(
            column, format_type="numpy", format_columns=None, output_all_columns=False, format_kwargs=None
        )
        indices = np.argsort(column_data, kind=kind)
        if reverse:
            indices = indices[::-1]

        return self.select(
            indices=indices,
            keep_in_memory=keep_in_memory,
            indices_cache_file_name=indices_cache_file_name,
            writer_batch_size=writer_batch_size,
            new_fingerprint=new_fingerprint,
        )

    @transmit_format
    @fingerprint(inplace=False, randomized_function=True)
    def shuffle(
        self,
        seed: Optional[int] = None,
        generator: Optional[np.random.Generator] = None,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        indices_cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
        new_fingerprint: Optional[str] = None,
    ) -> "Dataset":
        """Create a new Dataset where the rows are shuffled.

        Currently shuffling uses numpy random generators.
        You can either supply a NumPy BitGenerator to use, or a seed to initiate NumPy's default random generator (PCG64).

        Args:
            seed (Optional `int`): A seed to initialize the default BitGenerator if ``generator=None``.
                If None, then fresh, unpredictable entropy will be pulled from the OS.
                If an int or array_like[ints] is passed, then it will be passed to SeedSequence to derive the initial BitGenerator state.
            generator (Optional `np.random.Generator`): Numpy random Generator to use to compute the permutation of the dataset rows.
                If ``generator=None`` (default), uses np.random.default_rng (the default BitGenerator (PCG64) of NumPy).
            keep_in_memory (`bool`, defaults to `False`): Keep the shuffled indices in memory instead of writing it to a cache file.
            load_from_cache_file (`bool`, defaults to `True`): If a cache file storing the shuffled indices
                can be identified, use it instead of recomputing.
            indices_cache_file_name (`Optional[str]`, defaults to `None`): Provide the name of a cache file to use to store the
                shuffled indices instead of the automatically generated cache file name.
            writer_batch_size (`int`, defaults to `1000`): Number of rows per write operation for the cache file writer.
                Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
            new_fingerprint (`Optional[str]`, defaults to `None`): the new fingerprint of the dataset after transform.
                If `None`, the new fingerprint is computed using a hash of the previous fingerprint, and the transform arguments
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

        if generator is None:
            if seed is None:
                seed = np.random.get_state()[1][0]
                _ = np.random.random()  # do 1 step of rng
            generator = np.random.default_rng(seed)

        # Check if we've already cached this computation (indexed by a hash)
        if self._data_files:
            if indices_cache_file_name is None:
                # we create a unique hash from the function, current dataset file and the mapping args
                indices_cache_file_name = self._get_cache_file_path(new_fingerprint)
            if os.path.exists(indices_cache_file_name) and load_from_cache_file:
                logger.warning("Loading cached shuffled indices for dataset at %s", indices_cache_file_name)
                return self._new_dataset_with_indices(
                    fingerprint=new_fingerprint, indices_cache_file_name=indices_cache_file_name
                )

        permutation = generator.permutation(len(self))

        return self.select(
            indices=permutation,
            keep_in_memory=keep_in_memory,
            indices_cache_file_name=indices_cache_file_name,
            writer_batch_size=writer_batch_size,
            new_fingerprint=new_fingerprint,
        )

    @transmit_format
    @fingerprint(
        inplace=False, randomized_function=True, fingerprint_names=["train_new_fingerprint", "test_new_fingerprint"]
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
        train_indices_cache_file_name: Optional[str] = None,
        test_indices_cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
        train_new_fingerprint: Optional[str] = None,
        test_new_fingerprint: Optional[str] = None,
    ) -> "DatasetDict":
        """Return a dictionary (:obj:`datasets.DatsetDict`) with two random train and test subsets (`train` and `test` ``Dataset`` splits).
        Splits are created from the dataset according to `test_size`, `train_size` and `shuffle`.

        This method is similar to scikit-learn `train_test_split` with the omission of the stratified options.

        Args:
            test_size (Optional `np.random.Generator`): Size of the test split
                If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the test split.
                If int, represents the absolute number of test samples.
                If None, the value is set to the complement of the train size.
                If train_size is also None, it will be set to 0.25.
            train_size (Optional `np.random.Generator`): Size of the train split
                If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the train split.
                If int, represents the absolute number of train samples.
                If None, the value is automatically set to the complement of the test size.
            shuffle (Optional `bool`, defaults to `True`): Whether or not to shuffle the data before splitting.
            seed (Optional `int`): A seed to initialize the default BitGenerator if ``generator=None``.
                If None, then fresh, unpredictable entropy will be pulled from the OS.
                If an int or array_like[ints] is passed, then it will be passed to SeedSequence to derive the initial BitGenerator state.
            generator (Optional `np.random.Generator`): Numpy random Generator to use to compute the permutation of the dataset rows.
                If ``generator=None`` (default), uses np.random.default_rng (the default BitGenerator (PCG64) of NumPy).
            keep_in_memory (`bool`, defaults to `False`): Keep the splits indices in memory instead of writing it to a cache file.
            load_from_cache_file (`bool`, defaults to `True`): If a cache file storing the splits indices
                can be identified, use it instead of recomputing.
            train_cache_file_name (`Optional[str]`, defaults to `None`): Provide the name of a cache file to use to store the
                train split indices instead of the automatically generated cache file name.
            test_cache_file_name (`Optional[str]`, defaults to `None`): Provide the name of a cache file to use to store the
                test split indices instead of the automatically generated cache file name.
            writer_batch_size (`int`, defaults to `1000`): Number of rows per write operation for the cache file writer.
                Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
            train_new_fingerprint (`Optional[str]`, defaults to `None`): the new fingerprint of the train set after transform.
                If `None`, the new fingerprint is computed using a hash of the previous fingerprint, and the transform arguments
            test_new_fingerprint (`Optional[str]`, defaults to `None`): the new fingerprint of the test set after transform.
                If `None`, the new fingerprint is computed using a hash of the previous fingerprint, and the transform arguments
        """
        from .dataset_dict import DatasetDict  # import here because of circular dependency

        if len(self.list_indexes()) > 0:
            raise DatasetTransformationNotAllowedError(
                "Using `.train_test_split` on a dataset with attached indexes is not allowed. You can first run `.drop_index() to remove your index and then re-add it."
            )
        # If the array is empty we do nothing
        if len(self) == 0:
            return DatasetDict({"train": self, "test": self})

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

        if generator is None and shuffle is True:
            if seed is None:
                seed = np.random.get_state()[1][0]
                _ = np.random.random()  # do 1 step of rng
            generator = np.random.default_rng(seed)

        # Check if we've already cached this computation (indexed by a hash)
        if self._data_files:
            if train_indices_cache_file_name is None or test_indices_cache_file_name is None:
                # we create a unique hash from the function, current dataset file and the mapping args

                if train_indices_cache_file_name is None:
                    train_indices_cache_file_name = self._get_cache_file_path(train_new_fingerprint)
                if test_indices_cache_file_name is None:
                    test_indices_cache_file_name = self._get_cache_file_path(test_new_fingerprint)
            if (
                os.path.exists(train_indices_cache_file_name)
                and os.path.exists(test_indices_cache_file_name)
                and load_from_cache_file
            ):
                logger.warning(
                    "Loading cached split indices for dataset at %s and %s",
                    train_indices_cache_file_name,
                    test_indices_cache_file_name,
                )
                return DatasetDict(
                    {
                        "train": self._new_dataset_with_indices(
                            fingerprint=train_new_fingerprint, indices_cache_file_name=train_indices_cache_file_name
                        ),
                        "test": self._new_dataset_with_indices(
                            fingerprint=test_new_fingerprint, indices_cache_file_name=test_indices_cache_file_name
                        ),
                    }
                )

        if not shuffle:
            train_indices = np.arange(n_train)
            test_indices = np.arange(n_train, n_train + n_test)
        else:
            # random partition
            permutation = generator.permutation(len(self))
            test_indices = permutation[:n_test]
            train_indices = permutation[n_test : (n_test + n_train)]

        train_split = self.select(
            indices=train_indices,
            keep_in_memory=keep_in_memory,
            indices_cache_file_name=train_indices_cache_file_name,
            writer_batch_size=writer_batch_size,
            new_fingerprint=train_new_fingerprint,
        )
        test_split = self.select(
            indices=test_indices,
            keep_in_memory=keep_in_memory,
            indices_cache_file_name=test_indices_cache_file_name,
            writer_batch_size=writer_batch_size,
            new_fingerprint=test_new_fingerprint,
        )

        return DatasetDict({"train": train_split, "test": test_split})

    def shard(
        self,
        num_shards: int,
        index: int,
        contiguous: bool = False,
        keep_in_memory: bool = False,
        indices_cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
    ) -> "Dataset":
        """Return the `index`-nth shard from dataset split into `num_shards` pieces.

        This shards deterministically. dset.shard(n, i) will contain all elements of dset whose
        index mod n = i.

        dset.shard(n, i, contiguous=True) will instead split dset into contiguous chunks,
        so it can be easily concatenated back together after processing. If n % i == l, then the
        first l shards will have length (n // i) + 1, and the remaining shards will have length (n // i).
        `datasets.concatenate([dset.shard(n, i, contiguous=True) for i in range(n)])` will return
        a dataset with the same order as the original.

        Be sure to shard before using any randomizing operator (such as shuffle).
        It is best if the shard operator is used early in the dataset pipeline.


        Args:
            num_shards (`int`): How many shards to split the dataset into.
            index (`int`): Which shard to select and return.
            contiguous: (`bool`, defaults to `False`): Whether to select contiguous blocks of indices for shards.
            keep_in_memory (`bool`, defaults to `False`): Keep the dataset in memory instead of writing it to a cache file.
            load_from_cache_file (`bool`, defaults to `True`): If a cache file storing the current computation from `function`
                can be identified, use it instead of recomputing.
            indices_cache_file_name (`Optional[str]`, defaults to `None`): Provide the name of a cache file to use to store the
                indices of each shard instead of the automatically generated cache file name.
            writer_batch_size (`int`, defaults to `1000`): Number of rows per write operation for the cache file writer.
                Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
        """
        assert 0 <= index < num_shards, "index should be in [0, num_shards-1]"
        if contiguous:
            div = len(self) // num_shards
            mod = len(self) % num_shards
            start = div * index + min(index, mod)
            end = start + div + (1 if index < mod else 0)
            indices = np.arange(start, end)
        else:
            indices = np.arange(index, len(self), num_shards)

        return self.select(
            indices=indices,
            keep_in_memory=keep_in_memory,
            indices_cache_file_name=indices_cache_file_name,
            writer_batch_size=writer_batch_size,
        )

    def export(
        self,
        filename: str,
        format: str = "tfrecord",
    ):
        """Writes the Arrow dataset to a TFRecord file.

        The dataset must already be in tensorflow format. The records will be written with
        keys from `dataset._format_columns`.

        Args:
            `filename` (`str`): The filename, including the .tfrecord extension, to write to.
            `format` (`Optional[str]`, default: `"tfrecord"`): The type of output file. Currently this is a no-op, as
                TFRecords are the only option. This enables a more flexible function signature
                later.
        """
        try:
            import tensorflow as tf  # noqa: F401
        except ImportError:
            logger.error("Tensorflow needs to be installed to be able to return Tensorflow tensors.")

        # From https://www.tensorflow.org/tutorials/load_data/tfrecord
        def _bytes_feature(values):
            """Returns a bytes_list from a list of string / byte."""
            return tf.train.Feature(bytes_list=tf.train.BytesList(value=values))

        def _float_feature(values):
            """Returns a float_list from a list of float / double."""
            return tf.train.Feature(float_list=tf.train.FloatList(value=values))

        def _int64_feature(values):
            """Returns an int64_list from a list of bool / enum / int / uint."""
            return tf.train.Feature(int64_list=tf.train.Int64List(value=values))

        def _feature(values: np.ndarray) -> "tf.train.Feature":
            """Typechecks `values` and returns the corresponding tf.train.Feature."""
            if values.ndim == 0:
                values = values.item()
            if isinstance(values, np.ndarray):
                if values.dtype == np.dtype(float):
                    return _float_feature(values)
                elif values.dtype == np.int64:
                    return _int64_feature(values)
                elif values.dtype == np.dtype(str) or (
                    values.dtype == np.dtype(object) and len(values) > 0 and isinstance(values[0], str)
                ):
                    return _bytes_feature([v.encode() for v in values])
                else:
                    raise ValueError(
                        f"values={values} is an np.ndarray with items of dtype {values[0].dtype}, which cannot be serialized"
                    )
            elif isinstance(values, float):
                return _float_feature([values])
            elif isinstance(values, int):
                return _int64_feature([values])
            elif isinstance(values, str):
                return _bytes_feature([values.encode()])
            else:
                raise ValueError(f"values={values} has dtype {values.dtype}, which cannot be serialized")

        def serialize_example(ex):
            feature = {key: _feature(value) for key, value in ex.items()}
            example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
            return example_proto.SerializeToString()

        def tf_serialize_example(ex):
            tf_string = tf.py_function(serialize_example, (ex,), tf.string)
            return tf.reshape(tf_string, ())

        def generator():
            for ex in self:
                yield serialize_example(ex)

        assert self._format_type == "numpy", "Dataset format must be numpy before exporting"
        assert filename.endswith(".tfrecord")
        tf_dataset = tf.data.Dataset.from_generator(generator, output_types=tf.string, output_shapes=())
        writer = tf.data.experimental.TFRecordWriter(filename)
        logger.info(f"Writing TFRecord to {filename}")
        writer.write(tf_dataset)
        logger.info(f"Finished writing TFRecord to {filename}")
        self = None  # delete the dataset reference used by tf_dataset

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
        """Add a dense index using Faiss for fast retrieval.
        By default the index is done over the vectors of the specified column.
        You can specify :obj:`device` if you want to run it on GPU (:obj:`device` must be the GPU index).
        You can find more information about Faiss here:

            - For `string factory <https://github.com/facebookresearch/faiss/wiki/The-index-factory>`__

        Args:
            column (:obj:`str`):
                The column of the vectors to add to the index.
            index_name (Optional :obj:`str`):
                The index_name/identifier of the index.
                This is the index_name that is used to call :func:`datasets.Dataset.get_nearest_examples` or :func:`datasets.Dataset.search`.
                By default it corresponds to `column`.
            device (Optional :obj:`int`):
                If not None, this is the index of the GPU to use.
                By default it uses the CPU.
            string_factory (Optional :obj:`str`):
                This is passed to the index factory of Faiss to create the index.
                Default index class is ``IndexFlat``.
            metric_type (Optional :obj:`int`):
                Type of metric. Ex: faiss.faiss.METRIC_INNER_PRODUCT or faiss.METRIC_L2.
            custom_index (Optional :obj:`faiss.Index`):
                Custom Faiss index that you already have instantiated and configured for your needs.
            train_size (Optional :obj:`int`):
                If the index needs a training step, specifies how many vectors will be used to train the index.
            faiss_verbose (:obj:`bool`, defaults to False):
                Enable the verbosity of the Faiss index.
            dtype (data-type): The dtype of the numpy arrays that are indexed.
                Default is ``np.float32``.

        Example::

            ds = datasets.load_dataset('crime_and_punish', split='train')
            ds_with_embeddings = ds.map(lambda example: {'embeddings': embed(example['line']}))
            ds_with_embeddings.add_faiss_index(column='embeddings')
            # query
            scores, retrieved_examples = ds_with_embeddings.get_nearest_examples('embeddings', embed('my new query'), k=10)
            # save index
            ds_with_embeddings.save_faiss_index('embeddings', 'my_index.faiss')

            ds = datasets.load_dataset('crime_and_punish', split='train')
            # load index
            ds.load_faiss_index('embeddings', 'my_index.faiss')
            # query
            scores, retrieved_examples = ds.get_nearest_examples('embeddings', embed('my new query'), k=10)
        """
        with self.formatted_as(type="numpy", columns=[column], dtype=dtype):
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
        """Add a dense index using Faiss for fast retrieval.
        The index is created using the vectors of `external_arrays`.
        You can specify `device` if you want to run it on GPU (`device` must be the GPU index).
        You can find more information about Faiss here:
        - For `string factory <https://github.com/facebookresearch/faiss/wiki/The-index-factory>`__

        Args:
            external_arrays (:obj:`np.array`):
                If you want to use arrays from outside the lib for the index, you can set :obj:`external_arrays`.
                It will use :obj:`external_arrays` to create the Faiss index instead of the arrays in the given :obj:`column`.
            index_name (:obj:`str`):
                The index_name/identifier of the index.
                This is the index_name that is used to call :func:`datasets.Dataset.get_nearest_examples` or :func:`datasets.Dataset.search`.
            device (Optional :obj:`int`):
                If not None, this is the index of the GPU to use.
                By default it uses the CPU.
            string_factory (Optional :obj:`str`):
                This is passed to the index factory of Faiss to create the index.
                Default index class is ``IndexFlat``.
            metric_type (Optional :obj:`int`):
                Type of metric. Ex: faiss.faiss.METRIC_INNER_PRODUCT or faiss.METRIC_L2.
            custom_index (Optional :obj:`faiss.Index`):
                Custom Faiss index that you already have instantiated and configured for your needs.
            train_size (Optional :obj:`int`):
                If the index needs a training step, specifies how many vectors will be used to train the index.
            faiss_verbose (:obj:`bool`, defaults to False):
                Enable the verbosity of the Faiss index.
            dtype (:obj:`numpy.dtype`): The dtype of the numpy arrays that are indexed. Default is np.float32.
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
        """Add a text index using ElasticSearch for fast retrieval. This is done in-place.

        Args:
            column (:obj:`str`):
                The column of the documents to add to the index.
            index_name (Optional :obj:`str`):
                The index_name/identifier of the index.
                This is the index name that is used to call :func:`datasets.Dataset.get_nearest_examples` or :func:`datasets.Dataset.search`.
                By default it corresponds to :obj:`column`.
            host (Optional :obj:`str`, defaults to localhost):
                host of where ElasticSearch is running
            port (Optional :obj:`str`, defaults to 9200):
                port of where ElasticSearch is running
            es_client (Optional :obj:`elasticsearch.Elasticsearch`):
                The elasticsearch client used to create the index if host and port are None.
            es_index_name (Optional :obj:`str`):
                The elasticsearch index name used to create the index.
            es_index_config (Optional :obj:`dict`):
                The configuration of the elasticsearch index.
                Default config is:

        Config::

            {
                "settings": {
                    "number_of_shards": 1,
                    "analysis": {"analyzer": {"stop_standard": {"type": "standard", " stopwords": "_english_"}}},
                },
                "mappings": {
                    "properties": {
                        "text": {
                            "type": "text",
                            "analyzer": "standard",
                            "similarity": "BM25"
                        },
                    }
                },
            }

        Example::

            es_client = elasticsearch.Elasticsearch()
            ds = datasets.load_dataset('crime_and_punish', split='train')
            ds.add_elasticsearch_index(column='line', es_client=es_client, es_index_name="my_es_index")
            scores, retrieved_examples = ds.get_nearest_examples('line', 'my new query', k=10)

        """
        with self.formatted_as(type=None, columns=[column]):
            super().add_elasticsearch_index(
                column=column,
                index_name=index_name,
                host=host,
                port=port,
                es_client=es_client,
                es_index_name=es_index_name,
                es_index_config=es_index_config,
            )
        return self


def concatenate_datasets(
    dsets: List[Dataset],
    info: Optional[Any] = None,
    split: Optional[Any] = None,
):
    """
    Converts a list of :obj:``datasets.Dataset`` with the same schema into a single :obj:``datasets.Dataset``.

    Args:
        dsets (:obj:``List[datasets.Dataset]``): A list of Datasets to concatenate
        info (:obj:``datasets.DatasetInfo``, `optional`, defaults to :obj:``None``): If specified, the dataset info containing info like
            description, citation, etc.
        split (:obj:``datasets.NamedSplit``, `optional`, defaults to :obj:``None``): If specified, the name of the dataset split.
    """
    if not all([dset.features.type == dsets[0].features.type for dset in dsets]):
        raise ValueError("Features must match for all datasets")

    # Datasets tables should all come from disk or memory, but not a mix

    dsets_in_memory = [not dset._data_files for dset in dsets]
    if any(dset_in_memory != dsets_in_memory[0] for dset_in_memory in dsets_in_memory):
        raise ValueError(
            "Datasets should ALL come from memory, or should ALL come from disk.\n"
            "However datasets {} come from memory and datasets {} come from disk.".format(
                [i for i in range(len(dsets)) if dsets_in_memory[i]],
                [i for i in range(len(dsets)) if not dsets_in_memory[i]],
            )
        )

    # Find common format or reset format

    format = dsets[0].format
    if any(dset.format != format for dset in dsets):
        format = {}
        logger.info("Some of the datasets have disparate format. Resetting the format of the concatenated dataset.")

    # Concatenate tables

    table = pa.concat_tables(dset._data for dset in dsets if len(dset._data) > 0)
    data_files = [copy.deepcopy(f) for dset in dsets for f in dset._data_files]
    inplace_history = [copy.deepcopy(h) for dset in dsets for h in dset._inplace_history]

    def apply_offset_to_indices_table(table, offset):
        if offset == 0:
            return table
        else:
            array = table["indices"]
            if isinstance(array, pa.ChunkedArray):
                new_array = pa.array(np.concatenate([c.to_numpy() for c in array.chunks]) + offset, pa.uint64())
            else:
                new_array = pa.array(array.to_numpy() + offset, pa.uint64())
            return pa.Table.from_arrays([new_array], names=["indices"])

    # Concatenate indices if they exist

    if any(dset._indices is not None for dset in dsets):

        # Datasets indices tables should all come from disk or memory, but not a mix
        # Datasets with no indices tables are replaced with a dataset with an indicies table in memory

        indices_mappings_in_memory = [not dset._indices_data_files for dset in dsets]
        if any(
            indices_mapping_in_memory != indices_mappings_in_memory[0]
            for indices_mapping_in_memory in indices_mappings_in_memory
        ):
            raise ValueError(
                "Datasets' indices should ALL come from memory, or should ALL come from disk.\n"
                "However datasets' indices {} come from memory and datasets' indices {} come from disk.".format(
                    [i for i in range(len(dsets)) if indices_mappings_in_memory[i]],
                    [i for i in range(len(dsets)) if not indices_mappings_in_memory[i]],
                )
            )
        indices_in_memory = indices_mappings_in_memory[0]

        # Create missing indices tables in memory

        if indices_in_memory:
            for i in range(len(dsets)):
                if dsets[i]._indices is None:
                    dsets[i] = dsets[i].select(range(len(dsets[i])))
        assert all(dset._indices is not None for dset in dsets), "each dataset should have an indices table"

        # An offset needs to be applied to the indices before concatenating

        indices_tables = []
        offset = 0
        for dset in dsets:
            indices_tables.append(apply_offset_to_indices_table(dset._indices, offset))
            offset += len(dset._data)

        # Concatenate indices

        indices_tables = [t for t in indices_tables if len(t) > 0]
        if indices_tables:
            indices_table = pa.concat_tables(indices_tables)
        else:
            indices_table = pa.Table.from_batches([], schema=pa.schema({"indices": pa.int64()}))
    else:
        indices_table = None
    if info is None:
        info = DatasetInfo.from_merge([dset.info for dset in dsets])
    fingerprint = update_fingerprint(
        "".join(dset._fingerprint for dset in dsets), concatenate_datasets, {"info": info, "split": split}
    )
    concatenated_dataset = Dataset(
        table,
        info=info,
        split=split,
        data_files=data_files,
        indices_table=indices_table,
        indices_data_files=None,  # can't reuse same files as an offset was applied
        fingerprint=fingerprint,
        inplace_history=inplace_history,
    )
    concatenated_dataset.set_format(**format)
    return concatenated_dataset


# This is outside Dataset.filter as it needs to be picklable for multiprocessing

# transform the filter function into the map function
def map_function(batch, *args, function=None, with_indices=None, **fn_kwargs):
    assert function is not None and with_indices is not None
    result = defaultdict(list)
    num_examples = len(batch[next(iter(batch.keys()))])
    input_columns = fn_kwargs.pop("input_columns", None)

    # create single examples
    for i in range(num_examples):
        example = map_nested(lambda x: x[i], batch, dict_only=True)
        fn_args = [example] if input_columns is None else [example[col] for col in input_columns]

        # check if example should be filtered or not
        if with_indices:
            keep_example = function(*fn_args, args[0][i], **fn_kwargs)
        else:
            keep_example = function(*fn_args, **fn_kwargs)

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
