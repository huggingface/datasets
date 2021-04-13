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
import shutil
import tempfile
from collections import defaultdict
from collections.abc import Iterable, Mapping
from copy import deepcopy
from dataclasses import asdict
from functools import partial, wraps
from math import ceil, floor
from pathlib import Path
from typing import TYPE_CHECKING, Any, BinaryIO, Callable, Dict, Iterator, List, Optional, Tuple, Union

import fsspec
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
from multiprocess import Pool, RLock
from tqdm.auto import tqdm

from . import config
from .arrow_reader import ArrowReader
from .arrow_writer import ArrowWriter, OptimizedTypedSequence
from .features import Features, cast_to_python_objects
from .filesystems import extract_path_from_uri, is_remote_filesystem
from .fingerprint import (
    fingerprint_transform,
    generate_fingerprint,
    generate_random_fingerprint,
    get_temporary_cache_files_directory,
    is_caching_enabled,
    update_fingerprint,
)
from .formatting import format_table, get_format_type_from_alias, get_formatter, query_table
from .info import DATASET_INFO_FILENAME, DatasetInfo
from .search import IndexableMixin
from .splits import NamedSplit
from .table import InMemoryTable, MemoryMappedTable, Table, concat_tables, list_table_cache_files
from .utils import map_nested
from .utils.deprecation_utils import deprecated
from .utils.logging import WARNING, get_logger, get_verbosity, set_verbosity_warning
from .utils.typing import PathLike


if TYPE_CHECKING:
    from .dataset_dict import DatasetDict

logger = get_logger(__name__)

if int(pa.__version__.split(".")[0]) == 0:
    PYARROW_V0 = True
else:
    PYARROW_V0 = False


class DatasetInfoMixin:
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
        """ :class:`datasets.NamedSplit` object corresponding to a named dataset split."""
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
    """Wrapper for dataset transforms that recreate a new Dataset to transmit the format of the original dataset to the new dataset"""

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
            new_format = self_format.copy()
            if new_format["columns"] is not None:  # new formatted columns = (columns - previously unformatted columns)
                # sort the columns to have a deterministic list of columns that we can compare with `out_format`
                new_format["columns"] = sorted(set(dataset.column_names) - unformatted_columns)
            out_format = {
                "type": dataset._format_type,
                "format_kwargs": dataset._format_kwargs,
                "columns": sorted(dataset._format_columns) if dataset._format_columns is not None else None,
                "output_all_columns": dataset._output_all_columns,
            }
            if out_format != new_format:  # only apply if there's a change not to update the fingerprint for nothing
                dataset.set_format(**new_format)
        return out

    wrapper._decorator_name_ = "transmit_format"
    return wrapper


def update_metadata_with_features(func):
    """Wrapper for dataset transforms that modify the features of the dataset, which makes it necessary to update the features stored in the metadata of its schema."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            self: "Dataset" = args[0]
            args = args[1:]
        else:
            self: "Dataset" = kwargs.pop("self")
        # apply actual function
        out: Optional["Dataset"] = func(self, *args, **kwargs)
        # get the dataset to update its metadata (to handle both in-place and not in-place transforms)
        dataset: "Dataset" = out if out is not None else self
        if dataset._data.schema.metadata is not None:
            metadata = json.loads(dataset._data.schema.metadata["huggingface".encode("utf-8")].decode())
            if "info" in metadata:
                metadata["info"]["features"] = asdict(dataset._info)["features"]
                new_schema = dataset._data.schema.with_metadata({"huggingface": json.dumps(metadata)})
                dataset._data = dataset._data.cast(new_schema)
        return out

    wrapper._decorator_name_ = "update_metadata_with_features"
    return wrapper


def _check_table(table) -> Table:
    """We check the table type to make sure it's an instance of :class:`datasets.table.Table`"""
    if isinstance(table, pa.Table):
        # for a pyarrow table, we can just consider it as a in-memory table
        # this is here for backward compatibility
        return InMemoryTable(table)
    elif isinstance(table, Table):
        return table
    else:
        raise TypeError(f"Expected a pyarrow.Table or a datasets.table.Table object, but got {table}.")


class Dataset(DatasetInfoMixin, IndexableMixin):
    """A Dataset backed by an Arrow table."""

    def __init__(
        self,
        arrow_table: Table,
        info: Optional[DatasetInfo] = None,
        split: Optional[NamedSplit] = None,
        indices_table: Optional[Table] = None,
        fingerprint: Optional[str] = None,
    ):
        info = info.copy() if info is not None else DatasetInfo()
        DatasetInfoMixin.__init__(self, info=info, split=split)
        IndexableMixin.__init__(self)

        self._data: Table = _check_table(arrow_table)
        self._indices: Optional[Table] = _check_table(indices_table) if indices_table is not None else None

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
        in_memory: bool = False,
    ) -> "Dataset":
        """Instantiate a Dataset backed by an Arrow table at filename.

        Args:
            filename (:obj:`str`): File name of the dataset.
            info (:class:`DatasetInfo`, optional): Dataset information, like description, citation, etc.
            split (:class:`NamedSplit`, optional): Name of the dataset split.
            indices_filename (:obj:`str`, optional): File names of the indices.
            in_memory (:obj:`bool`, default ``False``): Whether to copy the data in-memory.

        Returns:
            :class:`Dataset`
        """
        table = ArrowReader.read_table(filename, in_memory=in_memory)

        if indices_filename is not None:
            indices_pa_table = ArrowReader.read_table(indices_filename, in_memory=in_memory)
        else:
            indices_pa_table = None

        return cls(
            arrow_table=table,
            info=info,
            split=split,
            indices_table=indices_pa_table,
        )

    @classmethod
    def from_buffer(
        cls,
        buffer: pa.Buffer,
        info: Optional[DatasetInfo] = None,
        split: Optional[NamedSplit] = None,
        indices_buffer: Optional[pa.Buffer] = None,
    ) -> "Dataset":
        """Instantiate a Dataset backed by an Arrow buffer.

        Args:
            buffer (:obj:`pyarrow.Buffer`): Arrow buffer.
            info (:class:`DatasetInfo`, optional): Dataset information, like description, citation, etc.
            split (:class:`NamedSplit`, optional): Name of the dataset split.
            indices_buffer (:obj:`pyarrow.Buffer`, optional): Indices Arrow buffer.

        Returns:
            :class:`Dataset`
        """
        table = InMemoryTable.from_buffer(buffer)

        if indices_buffer is not None:
            indices_table = InMemoryTable.from_buffer(buffer)
        else:
            indices_table = None

        return cls(table, info=info, split=split, indices_table=indices_table)

    @classmethod
    def from_pandas(
        cls,
        df: pd.DataFrame,
        features: Optional[Features] = None,
        info: Optional[DatasetInfo] = None,
        split: Optional[NamedSplit] = None,
    ) -> "Dataset":
        """
        Convert :obj:`pandas.DataFrame` to a :obj:`pyarrow.Table` to create a :class:`Dataset`.

        The column types in the resulting Arrow Table are inferred from the dtypes of the pandas.Series in the
        DataFrame. In the case of non-object Series, the NumPy dtype is translated to its Arrow equivalent. In the
        case of `object`, we need to guess the datatype by looking at the Python objects in this Series.

        Be aware that Series of the `object` dtype don't carry enough information to always lead to a meaningful Arrow
        type. In the case that we cannot infer a type, e.g. because the DataFrame is of length 0 or the Series only
        contains None/nan objects, the type is set to null. This behavior can be avoided by constructing explicit
        features and passing it to this function.

        Args:
            df (:obj:`pandas.DataFrame`): Dataframe that contains the dataset.
            features (:class:`Features`, optional): Dataset features.
            info (:class:`DatasetInfo`, optional): Dataset information, like description, citation, etc.
            split (:class:`NamedSplit`, optional): Name of the dataset split.

        Returns:
            :class:`Dataset`
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
        table = InMemoryTable.from_pandas(df=df, schema=pa.schema(features.type) if features is not None else None)
        return cls(table, info=info, split=split)

    @classmethod
    def from_dict(
        cls,
        mapping: dict,
        features: Optional[Features] = None,
        info: Optional[Any] = None,
        split: Optional[Any] = None,
    ) -> "Dataset":
        """
        Convert :obj:`dict` to a :obj:`pyarrow.Table` to create a :class:`Dataset`.

        Args:
            mapping (:obj:`Mapping`): Mapping of strings to Arrays or Python lists.
            features (:class:`Features`, optional): Dataset features.
            info (:class:`DatasetInfo`, optional): Dataset information, like description, citation, etc.
            split (:class:`NamedSplit`, optional): Name of the dataset split.

        Returns:
            :class:`Dataset`
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
            col: OptimizedTypedSequence(data, type=features.type[col].type if features is not None else None, col=col)
            for col, data in mapping.items()
        }
        pa_table = InMemoryTable.from_pydict(mapping=mapping)
        return cls(pa_table, info=info, split=split)

    @staticmethod
    def from_csv(
        path_or_paths: Union[PathLike, List[PathLike]],
        split: Optional[NamedSplit] = None,
        features: Optional[Features] = None,
        cache_dir: str = None,
        keep_in_memory: bool = False,
        **kwargs,
    ):
        """Create Dataset from CSV file(s).

        Args:
            path_or_paths (path-like or list of path-like): Path(s) of the CSV file(s).
            split (:class:`NamedSplit`, optional): Split name to be assigned to the dataset.
            features (:class:`Features`, optional): Dataset features.
            cache_dir (:obj:`str`, optional, default ``"~/datasets"``): Directory to cache data.
            keep_in_memory (:obj:`bool`, default ``False``): Whether to copy the data in-memory.
            **kwargs: Keyword arguments to be passed to :meth:`pandas.read_csv`.

        Returns:
            :class:`Dataset`
        """
        # Dynamic import to avoid circular dependency
        from .io.csv import CsvDatasetReader

        return CsvDatasetReader(
            path_or_paths, split=split, features=features, cache_dir=cache_dir, keep_in_memory=keep_in_memory, **kwargs
        ).read()

    @staticmethod
    def from_json(
        path_or_paths: Union[PathLike, List[PathLike]],
        split: Optional[NamedSplit] = None,
        features: Optional[Features] = None,
        cache_dir: str = None,
        keep_in_memory: bool = False,
        field: Optional[str] = None,
        **kwargs,
    ):
        """Create Dataset from JSON or JSON Lines file(s).

        Args:
            path_or_paths (path-like or list of path-like): Path(s) of the JSON or JSON Lines file(s).
            split (:class:`NamedSplit`, optional): Split name to be assigned to the dataset.
            features (:class:`Features`, optional): Dataset features.
            cache_dir (:obj:`str`, optional, default ``"~/datasets"``): Directory to cache data.
            keep_in_memory (:obj:`bool`, default ``False``): Whether to copy the data in-memory.
            field (:obj:`str`, optional): Field name of the JSON file where the dataset is contained in.
            **kwargs: Keyword arguments to be passed to :class:`JsonConfig`.

        Returns:
            :class:`Dataset`
        """
        # Dynamic import to avoid circular dependency
        from .io.json import JsonDatasetReader

        return JsonDatasetReader(
            path_or_paths,
            split=split,
            features=features,
            cache_dir=cache_dir,
            keep_in_memory=keep_in_memory,
            field=field,
            **kwargs,
        ).read()

    @staticmethod
    def from_text(
        path_or_paths: Union[PathLike, List[PathLike]],
        split: Optional[NamedSplit] = None,
        features: Optional[Features] = None,
        cache_dir: str = None,
        keep_in_memory: bool = False,
        **kwargs,
    ):
        """Create Dataset from text file(s).

        Args:
            path_or_paths (path-like or list of path-like): Path(s) of the text file(s).
            split (:class:`NamedSplit`, optional): Split name to be assigned to the dataset.
            features (:class:`Features`, optional): Dataset features.
            cache_dir (:obj:`str`, optional, default ``"~/datasets"``): Directory to cache data.
            keep_in_memory (:obj:`bool`, default ``False``): Whether to copy the data in-memory.
            **kwargs: Keyword arguments to be passed to :class:`TextConfig`.

        Returns:
            :class:`Dataset`
        """
        # Dynamic import to avoid circular dependency
        from .io.text import TextDatasetReader

        return TextDatasetReader(
            path_or_paths, split=split, features=features, cache_dir=cache_dir, keep_in_memory=keep_in_memory, **kwargs
        ).read()

    def __del__(self):
        if hasattr(self, "_data"):
            del self._data
        if hasattr(self, "_indices"):
            del self._indices

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Here `del` is used to del the pyarrow tables. This properly closes the files used for memory mapped tables
        self.__del__()

    def save_to_disk(self, dataset_path: str, fs=None):
        """
        Saves a dataset to a dataset directory, or in a filesystem using either :class:`~filesystems.S3FileSystem` or
        any implementation of ``fsspec.spec.AbstractFileSystem``.

        Args:
            dataset_path (:obj:`str`): Path (e.g. `dataset/train`) or remote URI (e.g. `s3://my-bucket/dataset/train`)
                of the dataset directory where the dataset will be saved to.
            fs (:class:`~filesystems.S3FileSystem`, ``fsspec.spec.AbstractFileSystem``, optional, defaults ``None``):
                Instance of the remote filesystem used to download the files from.
        """
        assert (
            not self.list_indexes()
        ), "please remove all the indexes using `dataset.drop_index` before saving a dataset"

        if is_remote_filesystem(fs):
            dataset_path = extract_path_from_uri(dataset_path)
        else:
            fs = fsspec.filesystem("file")
            cache_files_paths = [Path(cache_filename) for cache_filename in self.cache_files]
            # Check that the dataset doesn't overwrite iself. It can cause a permission error on Windows and a segfault on linux.
            if Path(dataset_path, config.DATASET_ARROW_FILENAME) in cache_files_paths:
                raise PermissionError(
                    f"Tried to overwrite {Path(dataset_path, config.DATASET_ARROW_FILENAME)} but a dataset can't overwrite itself."
                )
            if Path(dataset_path, config.DATASET_INDICES_FILENAME) in cache_files_paths:
                raise PermissionError(
                    f"Tried to overwrite {Path(dataset_path, config.DATASET_INDICES_FILENAME)} but a dataset can't overwrite itself."
                )

        # Get json serializable state
        state = {
            key: self.__dict__[key] if key != "_split" else str(self.__dict__[key])
            for key in [
                "_fingerprint",
                "_format_columns",
                "_format_kwargs",
                "_format_type",
                "_indexes",
                "_output_all_columns",
                "_split",
            ]
        }
        state["_data_files"] = [{"filename": config.DATASET_ARROW_FILENAME}]
        state["_indices_data_files"] = (
            [{"filename": config.DATASET_INDICES_FILENAME}] if self._indices is not None else None
        )
        for k in state["_format_kwargs"].keys():
            try:
                json.dumps(state["_format_kwargs"][k])
            except TypeError as e:
                raise TypeError(str(e) + f"\nThe format kwargs must be JSON serializable, but key '{k}' isn't.")

        # Get json serializable dataset info
        dataset_info = asdict(self._info)

        # Save dataset + indices + state + info
        fs.makedirs(dataset_path, exist_ok=True)
        with fs.open(Path(dataset_path, config.DATASET_ARROW_FILENAME).as_posix(), "wb") as dataset_file:
            with ArrowWriter(stream=dataset_file) as writer:
                writer.write_table(self._data)
                writer.finalize()
        if self._indices is not None:
            with fs.open(Path(dataset_path, config.DATASET_INDICES_FILENAME).as_posix(), "wb") as indices_file:
                with ArrowWriter(stream=indices_file) as writer:
                    writer.write_table(self._indices)
                    writer.finalize()
        with fs.open(
            Path(dataset_path, config.DATASET_STATE_JSON_FILENAME).as_posix(), "w", encoding="utf-8"
        ) as state_file:
            json.dump(state, state_file, indent=2, sort_keys=True)
        with fs.open(Path(dataset_path, DATASET_INFO_FILENAME).as_posix(), "w", encoding="utf-8") as dataset_info_file:
            json.dump(dataset_info, dataset_info_file, indent=2, sort_keys=True)
        logger.info("Dataset saved in {}".format(dataset_path))

    @staticmethod
    def load_from_disk(dataset_path: str, fs=None, keep_in_memory=False) -> "Dataset":
        """
        Loads a dataset that was previously saved using :meth:`save_to_disk` from a dataset directory, or from a
        filesystem using either :class:`~filesystems.S3FileSystem` or any implementation of ``fsspec.spec.AbstractFileSystem``.

        Args:
            dataset_path (:obj:`str`): Path (e.g. `dataset/train`) or remote URI (e.g. `s3//my-bucket/dataset/train`) of
                the dataset directory where the dataset will be loaded from.
            fs (:class:`~filesystems.S3FileSystem`, ``fsspec.spec.AbstractFileSystem``, optional, default ``None``):
                Instance of the remote filesystem used to download the files from.
            keep_in_memory (:obj:`bool`, default ``False``): Whether to copy the data in-memory.

        Returns:
            :class:`Dataset` or :class:`DatasetDict`.
                - if `dataset_path` is a path of a dataset directory: the :class:`Dataset` requested,
                - if `dataset_path` is a path of a dataset dict directory: a :class:`DatasetDict` with each split.
        """
        # copies file from filesystem if it is remote filesystem to local filesystem and modifies dataset_path to temp directory containing local copies
        if is_remote_filesystem(fs):
            src_dataset_path = extract_path_from_uri(dataset_path)
            tmp_dir = tempfile.TemporaryDirectory()
            dataset_path = Path(tmp_dir.name, src_dataset_path)
            fs.download(src_dataset_path, dataset_path.as_posix(), recursive=True)

        with open(
            Path(dataset_path, config.DATASET_STATE_JSON_FILENAME).as_posix(), "r", encoding="utf-8"
        ) as state_file:
            state = json.load(state_file)
        with open(Path(dataset_path, DATASET_INFO_FILENAME).as_posix(), "r", encoding="utf-8") as dataset_info_file:
            dataset_info = DatasetInfo.from_dict(json.load(dataset_info_file))

        table_cls = InMemoryTable if keep_in_memory else MemoryMappedTable
        arrow_table = concat_tables(
            table_cls.from_file(Path(dataset_path, data_file["filename"]).as_posix())
            for data_file in state["_data_files"]
        )
        if state.get("_indices_data_files"):
            indices_table = concat_tables(
                table_cls.from_file(Path(dataset_path, indices_file["filename"]).as_posix())
                for indices_file in state["_indices_data_files"]
            )
        else:
            indices_table = None

        return Dataset(
            arrow_table=arrow_table,
            indices_table=indices_table,
            info=dataset_info,
            split=state["_split"],
            fingerprint=state["_fingerprint"],
        )

    @property
    def data(self) -> Table:
        """The Apache Arrow table backing the dataset."""
        return self._data

    @property
    def cache_files(self):
        """The cache file containing the Apache Arrow table backing the dataset."""
        cache_files = list_table_cache_files(self._data)
        if self._indices is not None:
            cache_files += list_table_cache_files(self._indices)
        return cache_files

    @property
    def num_columns(self) -> int:
        """Number of columns in the dataset."""
        return self._data.num_columns

    @property
    def num_rows(self) -> int:
        """Number of rows in the dataset (same as :meth:`Dataset.__len__`)."""
        if self._indices is not None:
            return self._indices.num_rows
        return self._data.num_rows

    @property
    def column_names(self) -> List[str]:
        """Names of the columns in the dataset. """
        return self._data.column_names

    @property
    def shape(self) -> Tuple[int, int]:
        """Shape of the dataset (number of columns, number of rows)."""
        if self._indices is not None:
            return (self._indices.num_rows, self._data.num_columns)
        return self._data.shape

    def unique(self, column: str) -> List[Any]:
        """Return a list of the unique elements in a column.

        This is implemented in the low-level backend and as such, very fast.

        Args:
            column (:obj:`str`): Column name (list all the column names with :func:`datasets.Dataset.column_names`).

        Returns:
            :obj:`list`: List of unique elements in the given column.
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

    @deprecated()
    @update_metadata_with_features
    @fingerprint_transform(inplace=True)
    def dictionary_encode_column_(self, column: str):
        """Dictionary encode a column.

        Dictionary encode can reduce the size of a column with many repetitions (e.g. string labels columns)
        by storing a dictionary of the strings. This only affect the internal storage.

        .. deprecated:: 1.4.0

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

    @deprecated(help_message="Use Dataset.flatten instead.")
    @update_metadata_with_features
    @fingerprint_transform(inplace=True)
    def flatten_(self, max_depth=16):
        """In-place version of :meth:`Dataset.flatten`.

        .. deprecated:: 1.4.0
            Use :meth:`Dataset.flatten` instead.
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

    @update_metadata_with_features
    @fingerprint_transform(inplace=False)
    def flatten(self, new_fingerprint, max_depth=16) -> "Dataset":
        """Flatten the table.
        Each column with a struct type is flattened into one column per struct field.
        Other columns are left unchanged.

        Returns:
            :class:`Dataset`: A copy of the dataset with flattened columns.
        """
        dataset = copy.deepcopy(self)
        for depth in range(1, max_depth):
            if any(isinstance(field.type, pa.StructType) for field in dataset._data.schema):
                dataset._data = dataset._data.flatten()
            else:
                break
        if dataset.info is not None:
            dataset.info.features = Features.from_arrow_schema(dataset._data.schema)
        logger.info(
            "Flattened dataset from depth {} to depth {}.".format(depth, 1 if depth + 1 < max_depth else "unknown")
        )
        dataset._fingerprint = new_fingerprint
        return dataset

    @deprecated(help_message="Use Dataset.cast instead.")
    @fingerprint_transform(inplace=True)
    def cast_(self, features: Features):
        """In-place version of :meth:`Dataset.cast`.

        .. deprecated:: 1.4.0
            Use :meth:`Dataset.cast` instead.

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

    @fingerprint_transform(inplace=False)
    def cast(self, features: Features, new_fingerprint) -> "Dataset":
        """
        Cast the dataset to a new set of features.

        Args:
            features (:class:`datasets.Features`): New features to cast the dataset to.
                The name of the fields in the features must match the current column names.
                The type of the data must also be convertible from one type to the other.
                For non-trivial conversion, e.g. string <-> ClassLabel you should use :func:`map` to update the Dataset.

        Returns:
            :class:`Dataset`: A copy of the dataset with casted features.
        """
        dataset = copy.deepcopy(self)
        if sorted(features) != sorted(dataset._data.column_names):
            raise ValueError(
                f"The columns in features ({list(features)}) must be identical "
                f"as the columns in the dataset: {dataset._data.column_names}"
            )

        dataset._info.features = features
        type = features.type
        schema = pa.schema({col_name: type[col_name].type for col_name in dataset._data.column_names})
        dataset._data = dataset._data.cast(schema)
        dataset._fingerprint = new_fingerprint
        return dataset

    @deprecated(help_message="Use Dataset.remove_columns instead.")
    @update_metadata_with_features
    @fingerprint_transform(inplace=True)
    def remove_columns_(self, column_names: Union[str, List[str]]):
        """In-place version of :meth:`Dataset.remove_columns`.

        .. deprecated:: 1.4.0
            Use :meth:`Dataset.remove_columns` instead.

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

    @update_metadata_with_features
    @fingerprint_transform(inplace=False)
    def remove_columns(self, column_names: Union[str, List[str]], new_fingerprint) -> "Dataset":
        """
        Remove one or several column(s) in the dataset and the features associated to them.

        You can also remove a column using :func:`Dataset.map` with `remove_columns` but the present method
        is in-place (doesn't copy the data to a new dataset) and is thus faster.

        Args:
            column_names (:obj:`Union[str, List[str]]`): Name of the column(s) to remove.
            new_fingerprint

        Returns:
            :class:`Dataset`: A copy of the dataset object without the columns to remove.
        """
        dataset = copy.deepcopy(self)
        if isinstance(column_names, str):
            column_names = [column_names]

        for column_name in column_names:
            if column_name not in dataset._data.column_names:
                raise ValueError(
                    f"Column name {column_name} not in the dataset. "
                    f"Current columns in the dataset: {dataset._data.column_names}"
                )

        for column_name in column_names:
            del dataset._info.features[column_name]

        dataset._data = dataset._data.drop(column_names)
        dataset._fingerprint = new_fingerprint
        return dataset

    @deprecated(help_message="Use Dataset.rename_column instead.")
    @update_metadata_with_features
    @fingerprint_transform(inplace=True)
    def rename_column_(self, original_column_name: str, new_column_name: str):
        """In-place version of :meth:`Dataset.rename_column`.

        .. deprecated:: 1.4.0
            Use :meth:`Dataset.rename_column` instead.

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

        def rename(columns):
            return [new_column_name if col == original_column_name else col for col in columns]

        new_column_names = rename(self._data.column_names)
        if self._format_columns is not None:
            self._format_columns = rename(self._format_columns)

        self._info.features = Features(
            {
                new_column_name if col == original_column_name else col: feature
                for col, feature in self._info.features.items()
            }
        )

        self._data = self._data.rename_columns(new_column_names)

    @update_metadata_with_features
    @fingerprint_transform(inplace=False)
    def rename_column(self, original_column_name: str, new_column_name: str, new_fingerprint) -> "Dataset":
        """
        Rename a column in the dataset, and move the features associated to the original column under the new column
        name.

        Args:
            original_column_name (:obj:`str`): Name of the column to rename.
            new_column_name (:obj:`str`): New name for the column.
            new_fingerprint

        Returns:
            :class:`Dataset`: A copy of the dataset with a renamed column.
        """
        dataset = copy.deepcopy(self)
        if original_column_name not in dataset._data.column_names:
            raise ValueError(
                f"Original column name {original_column_name} not in the dataset. "
                f"Current columns in the dataset: {dataset._data.column_names}"
            )
        if new_column_name in dataset._data.column_names:
            raise ValueError(
                f"New column name {original_column_name} already in the dataset. "
                f"Please choose a column name which is not already in the dataset. "
                f"Current columns in the dataset: {dataset._data.column_names}"
            )
        if not new_column_name:
            raise ValueError("New column name is empty.")

        def rename(columns):
            return [new_column_name if col == original_column_name else col for col in columns]

        new_column_names = rename(self._data.column_names)
        if self._format_columns is not None:
            dataset._format_columns = rename(self._format_columns)

        dataset._info.features = Features(
            {
                new_column_name if col == original_column_name else col: feature
                for col, feature in self._info.features.items()
            }
        )

        dataset._data = dataset._data.rename_columns(new_column_names)
        dataset._fingerprint = new_fingerprint
        return dataset

    def __len__(self):
        """ Number of rows in the dataset."""
        return self.num_rows

    def __iter__(self):
        """Iterate through the examples.

        If a formatting is set with :meth:`Dataset.set_format` rows will be returned with the
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
        """To be used in a `with` statement. Set __getitem__ return format (type and columns).

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

    @fingerprint_transform(inplace=True)
    def set_format(
        self,
        type: Optional[str] = None,
        columns: Optional[List] = None,
        output_all_columns: bool = False,
        **format_kwargs,
    ):
        """Set __getitem__ return format (type and columns). The data formatting is applied on-the-fly.
        The format ``type`` (for example "numpy") is used to format batches when using __getitem__.
        It's also possible to use custom transforms for formatting using :func:`datasets.Dataset.set_transform`.

        Args:
            type (Optional ``str``):
                Either output type selected in [None, 'numpy', 'torch', 'tensorflow', 'pandas'].
                None means __getitem__ returns python objects (default)
            columns (Optional ``List[str]``): columns to format in the output.
                None means __getitem__ returns all columns (default).
            output_all_columns (``bool`` default to False): keep un-formatted columns as well in the output (as python objects)
            format_kwargs: keywords arguments passed to the convert function like `np.array`, `torch.tensor` or `tensorflow.ragged.constant`.

        It is possible to call ``map`` after calling ``set_format``. Since ``map`` may add new columns, then the list of formatted columns
        gets updated. In this case, if you apply ``map`` on a dataset to add a new column, then this column will be formatted:

            new formatted columns = (all columns - previously unformatted columns)

        """
        format_kwargs.update(format_kwargs.pop("format_kwargs", {}))  # allow to use self.set_format(self.format)

        # Check that the format_type and format_kwargs are valid and make it possible to have a Formatter
        type = get_format_type_from_alias(type)
        _ = get_formatter(type, **format_kwargs)

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

    def set_transform(
        self,
        transform: Optional[Callable],
        columns: Optional[List] = None,
        output_all_columns: bool = False,
    ):
        """Set __getitem__ return format using this transform. The transform is applied on-the-fly on batches when __getitem__ is called.
        As :func:`datasets.Dataset.set_format`, this can be reset using :func:`datasets.Dataset.reset_format`

        Args:
            transform (Optional ``Callable``): user-defined formatting transform, replaces the format defined by :func:`datasets.Dataset.set_format`
                A formatting function is a callable that takes a batch (as a dict) as input and returns a batch.
                This function is applied right before returning the objects in __getitem__.
            columns (Optional ``List[str]``): columns to format in the output
                If specified, then the input batch of the transform only contains those columns.
            output_all_columns (``bool`` default to False): keep un-formatted columns as well in the output (as python objects)
                If set to True, then the other un-formatted columns are kept with the output of the transform.

        """
        self.set_format("custom", columns=columns, output_all_columns=output_all_columns, transform=transform)

    def with_format(
        self,
        type: Optional[str] = None,
        columns: Optional[List] = None,
        output_all_columns: bool = False,
        **format_kwargs,
    ):
        """Set __getitem__ return format (type and columns). The data formatting is applied on-the-fly.
        The format ``type`` (for example "numpy") is used to format batches when using __getitem__.

        It's also possible to use custom transforms for formatting using :func:`datasets.Dataset.with_transform`.

        Contrary to :func:`datasets.Dataset.set_format`, ``with_format`` returns a new Dataset object.

        Args:
            type (Optional ``str``):
                Either output type selected in [None, 'numpy', 'torch', 'tensorflow', 'pandas'].
                None means __getitem__ returns python objects (default)
            columns (Optional ``List[str]``): columns to format in the output
                None means __getitem__ returns all columns (default)
            output_all_columns (``bool`` default to False): keep un-formatted columns as well in the output (as python objects)
            format_kwargs: keywords arguments passed to the convert function like `np.array`, `torch.tensor` or `tensorflow.ragged.constant`.
        """
        dataset = copy.deepcopy(self)
        dataset.set_format(type=type, columns=columns, output_all_columns=output_all_columns, **format_kwargs)
        return dataset

    def with_transform(
        self,
        transform: Optional[Callable],
        columns: Optional[List] = None,
        output_all_columns: bool = False,
    ):
        """Set __getitem__ return format using this transform. The transform is applied on-the-fly on batches when __getitem__ is called.

        As :func:`datasets.Dataset.set_format`, this can be reset using :func:`datasets.Dataset.reset_format`.

        Contrary to :func:`datasets.Dataset.set_transform`, ``with_transform`` returns a new Dataset object.

        Args:
            transform (Optional ``Callable``): user-defined formatting transform, replaces the format defined by :func:`datasets.Dataset.set_format`
                A formatting function is a callable that takes a batch (as a dict) as input and returns a batch.
                This function is applied right before returning the objects in __getitem__.
            columns (Optional ``List[str]``): columns to format in the output
                If specified, then the input batch of the transform only contains those columns.
            output_all_columns (``bool`` default to False): keep un-formatted columns as well in the output (as python objects)
                If set to True, then the other un-formatted columns are kept with the output of the transform.

        """
        dataset = copy.deepcopy(self)
        dataset.set_transform(transform=transform, columns=columns, output_all_columns=output_all_columns)
        return dataset

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
        format_kwargs = format_kwargs if format_kwargs is not None else {}
        formatter = get_formatter(format_type, **format_kwargs)
        pa_subtable = query_table(self._data, key, indices=self._indices if self._indices is not None else None)
        formatted_output = format_table(
            pa_subtable, key, formatter=formatter, format_columns=format_columns, output_all_columns=output_all_columns
        )
        return formatted_output

    def __getitem__(self, key: Union[int, slice, str]) -> Union[Dict, List]:
        """Can be used to index columns (by string names) or rows (by integer index or iterable of indices or bools)."""
        return self._getitem(
            key,
            format_type=self._format_type,
            format_columns=self._format_columns,
            output_all_columns=self._output_all_columns,
            format_kwargs=self._format_kwargs,
        )

    def cleanup_cache_files(self) -> int:
        """Clean up all cache files in the dataset cache directory, excepted the currently used cache file if there is
        one.

        Be careful when running this command that no other process is currently using other cache files.

        Returns:
            :obj:`int`: Number of removed files.
        """
        current_cache_files = [os.path.abspath(cache_file) for cache_file in self.cache_files]
        if not current_cache_files:
            return 0
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
        if is_caching_enabled() and self.cache_files:
            cache_file_name = "cache-" + fingerprint + ".arrow"
            cache_directory = os.path.dirname(self.cache_files[0])
        else:
            cache_file_name = "cache-" + generate_random_fingerprint() + ".arrow"
            cache_directory = get_temporary_cache_files_directory()
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
        load_from_cache_file: bool = None,
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
        and update the table (if function does update examples).

        Args:
            function (:obj:`Callable`): Function with one of the following signatures:

                - `function(example: Union[Dict, Any]) -> Union[Dict, Any]` if `batched=False` and `with_indices=False`
                - `function(example: Union[Dict, Any], indices: int) -> Union[Dict, Any]` if `batched=False` and `with_indices=True`
                - `function(batch: Union[Dict[List], List[Any]]) -> Union[Dict, Any]` if `batched=True` and `with_indices=False`
                - `function(batch: Union[Dict[List], List[Any]], indices: List[int]) -> Union[Dict, Any]` if `batched=True` and `with_indices=True`

                If no function is provided, default to identity function: ``lambda x: x``.
            with_indices (:obj:`bool`, default `False`): Provide example indices to `function`. Note that in this case the
                signature of `function` should be `def function(example, idx): ...`.
            input_columns (`Optional[Union[str, List[str]]]`, default `None`): The columns to be passed into `function`
                as positional arguments. If `None`, a dict mapping to all formatted columns is passed as one argument.
            batched (:obj:`bool`, default `False`): Provide batch of examples to `function`.
            batch_size (`Optional[int]`, default `1000`): Number of examples per batch provided to `function` if `batched=True`
                `batch_size <= 0` or `batch_size == None`: Provide the full dataset as a single batch to `function`.
            drop_last_batch (:obj:`bool`, default `False`): Whether a last batch smaller than the batch_size should be
                dropped instead of being processed by the function.
            remove_columns (`Optional[List[str]]`, default `None`): Remove a selection of columns while doing the mapping.
                Columns will be removed before updating the examples with the output of `function`, i.e. if `function` is adding
                columns with names in `remove_columns`, these columns will be kept.
            keep_in_memory (:obj:`bool`, default `False`): Keep the dataset in memory instead of writing it to a cache file.
            load_from_cache_file (:obj:`bool`, default `True` if caching is enabled): If a cache file storing the current computation from `function`
                can be identified, use it instead of recomputing.
            cache_file_name (`Optional[str]`, default `None`): Provide the name of a path for the cache file. It is used to store the
                results of the computation instead of the automatically generated cache file name.
            writer_batch_size (:obj:`int`, default `1000`): Number of rows per write operation for the cache file writer.
                Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
            features (`Optional[datasets.Features]`, default `None`): Use a specific Features to store the cache file
                instead of the automatically generated one.
            disable_nullable (:obj:`bool`, default `True`): Disallow null values in the table.
            fn_kwargs (`Optional[Dict]`, default `None`): Keyword arguments to be passed to `function`.
            num_proc (`Optional[int]`, default `None`): Number of processes for multiprocessing. By default it doesn't
                use multiprocessing.
            suffix_template (:obj:`str`):
                If cache_file_name is specified, then this suffix
                will be added at the end of the base name of each: defaults to "_{rank:05d}_of_{num_proc:05d}". For example, if cache_file_name is "processed.arrow", then for
                rank=1 and num_proc=4, the resulting file would be "processed_00001_of_00004.arrow" for the default suffix.
            new_fingerprint (`Optional[str]`, default `None`): the new fingerprint of the dataset after transform.
                If `None`, the new fingerprint is computed using a hash of the previous fingerprint, and the transform arguments.
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

        load_from_cache_file = load_from_cache_file if load_from_cache_file is not None else is_caching_enabled()

        if fn_kwargs is None:
            fn_kwargs = {}

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
            )
        else:

            def format_cache_file_name(cache_file_name, rank):
                sep = cache_file_name.rindex(".")
                base_name, extension = cache_file_name[:sep], cache_file_name[sep:]
                cache_file_name = base_name + suffix_template.format(rank=rank, num_proc=num_proc) + extension
                logger.info("Process #{} will write at {}".format(rank, cache_file_name))
                return cache_file_name

            prev_env = deepcopy(os.environ)
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
    @fingerprint_transform(inplace=False, ignore_kwargs=["load_from_cache_file", "cache_file_name"])
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
        load_from_cache_file: bool = None,
        cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
        features: Optional[Features] = None,
        disable_nullable: bool = False,
        fn_kwargs: Optional[dict] = None,
        new_fingerprint: Optional[str] = None,
        rank: Optional[int] = None,
        offset: int = 0,
    ) -> "Dataset":
        """Apply a function to all the elements in the table (individually or in batches)
        and update the table (if function does update examples).

        Args:
            function (:obj:`Callable`): with one of the following signature:
                - `function(example: Union[Dict, Any]) -> Union[Dict, Any]` if `batched=False` and `with_indices=False`
                - `function(example: Union[Dict, Any], indices: int) -> Union[Dict, Any]` if `batched=False` and `with_indices=True`
                - `function(batch: Union[Dict[List], List[Any]]) -> Union[Dict, Any]` if `batched=True` and `with_indices=False`
                - `function(batch: Union[Dict[List], List[Any]], indices: List[int]) -> Union[Dict, Any]` if `batched=True` and `with_indices=True`
                If no function is provided, default to identity function: lambda x: x
            with_indices (:obj:`bool`, defaults to `False`): Provide example indices to `function`. Note that in this case the signature of `function` should be `def function(example, idx): ...`.
            input_columns (`Optional[Union[str, List[str]]]`, defaults to `None`): The columns to be passed into `function` as
                positional arguments. If `None`, a dict mapping to all formatted columns is passed as one argument.
            batched (:obj:`bool`, defaults to `False`): Provide batch of examples to `function`
            batch_size (`Optional[int]`, defaults to `1000`): Number of examples per batch provided to `function` if `batched=True`
                `batch_size <= 0` or `batch_size == None`: Provide the full dataset as a single batch to `function`
            drop_last_batch (:obj:`bool`, default: `False`): Whether a last batch smaller than the batch_size should be
                dropped instead of being processed by the function.
            remove_columns (`Optional[List[str]]`, defaults to `None`): Remove a selection of columns while doing the mapping.
                Columns will be removed before updating the examples with the output of `function`, i.e. if `function` is adding
                columns with names in `remove_columns`, these columns will be kept.
            keep_in_memory (:obj:`bool`, defaults to `False`): Keep the dataset in memory instead of writing it to a cache file.
            load_from_cache_file (:obj:`bool`, defaults to `True` if caching is enabled): If a cache file storing the current computation from `function`
                can be identified, use it instead of recomputing.
            cache_file_name (`Optional[str]`, defaults to `None`): Provide the name of a path for the cache file. It is used to store the
                results of the computation instead of the automatically generated cache file name.
            writer_batch_size (:obj:`int`, defaults to `1000`): Number of rows per write operation for the cache file writer.
                Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
            features (`Optional[datasets.Features]`, defaults to `None`): Use a specific Features to store the cache file
                instead of the automatically generated one.
            disable_nullable (:obj:`bool`, defaults to `True`): Disallow null values in the table.
            fn_kwargs (`Optional[Dict]`, defaults to `None`): Keyword arguments to be passed to `function`
            new_fingerprint (`Optional[str]`, defaults to `None`): the new fingerprint of the dataset after transform.
                If `None`, the new fingerprint is computed using a hash of the previous fingerprint, and the transform arguments
            rank: (`Optional[int]`, defaults to `None`): If specified, this is the process rank when doing multiprocessing
            offset: (:obj:`int`, defaults to 0): If specified, this is an offset applied to the indices passed to `function` if `with_indices=True`
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

        load_from_cache_file = load_from_cache_file if load_from_cache_file is not None else is_caching_enabled()

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
            fn_kwargs = {}

        # If we do batch computation but no batch size is provided, default to the full dataset
        if batched and (batch_size is None or batch_size <= 0):
            batch_size = self.num_rows

        # Check if we've already cached this computation (indexed by a hash)
        if self.cache_files:
            if cache_file_name is None:
                # we create a unique hash from the function,
                # current dataset file and the mapping args
                cache_file_name = self._get_cache_file_path(new_fingerprint)
            if os.path.exists(cache_file_name) and load_from_cache_file:
                logger.warning("Loading cached processed dataset at %s", cache_file_name)
                info = self.info.copy()
                info.features = features
                return Dataset.from_file(cache_file_name, info=info, split=self.split)

        # We set this variable to True after processing the first example/batch in
        # `apply_function_on_filtered_inputs` if the map function returns a dict.
        # If set to False, no new arrow table will be created
        update_data = None

        class NumExamplesMismatch(Exception):
            pass

        def validate_function_output(does_return_dict, processed_inputs, indices):
            """ Validate output of the map function. """
            if does_return_dict is False and processed_inputs is not None:
                raise TypeError(
                    "Provided `function` which is applied to all elements of table returns a variable of type {}. Make sure provided `function` returns a variable of type `dict` to update the dataset or `None` if you are only interested in side effects.".format(
                        type(processed_inputs)
                    )
                )
            elif isinstance(indices, list) and does_return_dict is True:
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

        def apply_function_on_filtered_inputs(inputs, indices, check_same_num_examples=False, offset=0):
            """ Utility to apply the function on a selection of columns. """
            nonlocal update_data
            fn_args = [inputs] if input_columns is None else [inputs[col] for col in input_columns]
            if offset == 0:
                effective_indices = indices
            else:
                effective_indices = [i + offset for i in indices] if isinstance(indices, list) else indices + offset
            processed_inputs = (
                function(*fn_args, effective_indices, **fn_kwargs) if with_indices else function(*fn_args, **fn_kwargs)
            )
            if update_data is None:
                # Check if the function returns updated examples
                update_data = isinstance(processed_inputs, Mapping)
                validate_function_output(update_data, processed_inputs, indices)
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

        def init_buffer_and_writer():
            # Prepare output buffer and batched writer in memory or on file if we update the table
            writer_features = features
            if writer_features is None:
                writer_features = self.features
                update_features = True
            else:
                update_features = False
            if keep_in_memory or cache_file_name is None:
                buf_writer = pa.BufferOutputStream()
                tmp_file = None
                writer = ArrowWriter(
                    features=writer_features,
                    stream=buf_writer,
                    writer_batch_size=writer_batch_size,
                    update_features=update_features,
                    fingerprint=new_fingerprint,
                    disable_nullable=disable_nullable,
                )
            else:
                buf_writer = None
                logger.info("Caching processed dataset at %s", cache_file_name)
                tmp_file = tempfile.NamedTemporaryFile("wb", dir=os.path.dirname(cache_file_name), delete=False)
                writer = ArrowWriter(
                    features=writer_features,
                    path=tmp_file.name,
                    writer_batch_size=writer_batch_size,
                    update_features=update_features,
                    fingerprint=new_fingerprint,
                    disable_nullable=disable_nullable,
                )
            return buf_writer, writer, tmp_file

        # If `update_data` is True after processing the first example/batch, initalize these resources with `init_buffer_and_writer`
        buf_writer, writer, tmp_file = None, None, None

        # Optionally initialize the writer as a context manager
        with contextlib.ExitStack() as stack:
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
                            if i == 0:
                                buf_writer, writer, tmp_file = init_buffer_and_writer()
                                stack.enter_context(writer)
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
                            if i == 0:
                                buf_writer, writer, tmp_file = init_buffer_and_writer()
                                stack.enter_context(writer)
                            batch = cast_to_python_objects(batch)
                            writer.write_batch(batch)
                if update_data and writer is not None:
                    writer.finalize()  # close_stream=bool(buf_writer is None))  # We only close if we are writing in a file
            except (Exception, KeyboardInterrupt):
                if update_data:
                    if writer is not None:
                        writer.finalize()
                    if tmp_file is not None:
                        tmp_file.close()
                        if os.path.exists(tmp_file.name):
                            os.remove(tmp_file.name)
                raise

        if update_data and tmp_file is not None:
            tmp_file.close()
            shutil.move(tmp_file.name, cache_file_name)
            umask = os.umask(0o666)
            os.umask(umask)
            os.chmod(cache_file_name, 0o666 & ~umask)

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
    @fingerprint_transform(inplace=False, ignore_kwargs=["load_from_cache_file", "cache_file_name"])
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
            function (:obj:`Callable`): Callable with one of the following signatures:

                - ``function(example: Union[Dict, Any]) -> bool`` if ``with_indices=False``
                - ``function(example: Union[Dict, Any], indices: int) -> bool`` if ``with_indices=True``

                If no function is provided, defaults to an always True function: ``lambda x: True``.
            with_indices (:obj:`bool`, default `False`): Provide example indices to `function`. Note that in this case the signature of `function` should be `def function(example, idx): ...`.
            input_columns (:obj:`str` or `List[str]`, optional): The columns to be passed into `function` as
                positional arguments. If `None`, a dict mapping to all formatted columns is passed as one argument.
            batch_size (:obj:`int`, optional, default `1000`): Number of examples per batch provided to `function` if
                ``batched = True``. If ``batch_size <= 0`` or ``batch_size == None``: provide the full dataset as a
                single batch to `function`
            remove_columns (`List[str]`, optional): Remove a selection of columns while doing the mapping.
                Columns will be removed before updating the examples with the output of `function`, i.e. if `function` is adding
                columns with names in `remove_columns`, these columns will be kept.
            keep_in_memory (:obj:`bool`, default `False`): Keep the dataset in memory instead of writing it to a cache file.
            load_from_cache_file (:obj:`bool`, default `True`): If a cache file storing the current computation from `function`
                can be identified, use it instead of recomputing.
            cache_file_name (:obj:`str`, optional): Provide the name of a path for the cache file. It is used to store the
                results of the computation instead of the automatically generated cache file name.
            writer_batch_size (:obj:`int`, default `1000`): Number of rows per write operation for the cache file writer.
                Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
            fn_kwargs (:obj:`dict`, optional): Keyword arguments to be passed to `function`
            num_proc (:obj:`int`, optional): Number of processes for multiprocessing. By default it doesn't
                use multiprocessing.
            suffix_template (:obj:`str`):
                If `cache_file_name` is specified, then this suffix will be added at the end of the base name of each.
                For example, if `cache_file_name` is `"processed.arrow"`, then for ``rank = 1`` and ``num_proc = 4``,
                the resulting file would be `"processed_00001_of_00004.arrow"` for the default suffix (default
                `_{rank:05d}_of_{num_proc:05d}`)
            new_fingerprint (:obj:`str`, optional): The new fingerprint of the dataset after transform.
                If `None`, the new fingerprint is computed using a hash of the previous fingerprint, and the transform arguments.
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
            fn_kwargs = {}
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
    @fingerprint_transform(inplace=False, ignore_kwargs=["cache_file_name"])
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
            keep_in_memory (:obj:`bool`, default `False`): Keep the dataset in memory instead of writing it to a cache file.
            cache_file_name (`Optional[str]`, default `None`): Provide the name of a path for the cache file. It is used to store the
                results of the computation instead of the automatically generated cache file name.
            writer_batch_size (:obj:`int`, default `1000`): Number of rows per write operation for the cache file writer.
                Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
            features (`Optional[datasets.Features]`, default `None`): Use a specific Features to store the cache file
                instead of the automatically generated one.
            disable_nullable (:obj:`bool`, default `True`): Allow null values in the table.
            new_fingerprint (`Optional[str]`, default `None`): The new fingerprint of the dataset after transform.
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
        """Return a new Dataset obtained by adding indices (provided in indices_cache_file_name or in a buffer) to the
        current Dataset.
        """

        assert (
            indices_cache_file_name is not None or indices_buffer is not None
        ), "At least one of indices_cache_file_name or indices_buffer must be provided."

        assert fingerprint is not None, "please specify a fingerprint for the dataset with indices"
        if indices_cache_file_name is not None:
            indices_table = MemoryMappedTable.from_file(indices_cache_file_name)
        else:
            indices_table = InMemoryTable.from_buffer(indices_buffer)

        # Return new Dataset object
        # don't forget to copy the objects
        return Dataset(
            self._data,
            info=self.info.copy(),
            split=self.split,
            indices_table=indices_table,
            fingerprint=fingerprint,
        )

    @transmit_format
    @fingerprint_transform(inplace=False, ignore_kwargs=["indices_cache_file_name"])
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
            indices (sequence, iterable, ndarray or Series): List or 1D-array of integer indices for indexing.
            keep_in_memory (:obj:`bool`, default `False`): Keep the indices mapping in memory instead of writing it to a cache file.
            indices_cache_file_name (`Optional[str]`, default `None`): Provide the name of a path for the cache file. It is used to store the
                indices mapping instead of the automatically generated cache file name.
            writer_batch_size (:obj:`int`, default `1000`): Number of rows per write operation for the cache file writer.
                Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
            new_fingerprint (`Optional[str]`, default `None`): the new fingerprint of the dataset after transform.
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
            indices_array = self._indices.column(0).take(indices_array)

        indices_table = pa.Table.from_arrays([indices_array], names=["indices"])

        with writer:
            try:
                writer.write_table(indices_table)
                writer.finalize()  # close_stream=bool(buf_writer is None))  We only close if we are writing in a file
            except (Exception, KeyboardInterrupt):
                if tmp_file is not None:
                    tmp_file.close()
                    if os.path.exists(tmp_file.name):
                        os.remove(tmp_file.name)
                raise

        if tmp_file is not None:
            tmp_file.close()
            shutil.move(tmp_file.name, indices_cache_file_name)
            umask = os.umask(0o666)
            os.umask(umask)
            os.chmod(indices_cache_file_name, 0o666 & ~umask)

        # Return new Dataset object
        if buf_writer is None:
            return self._new_dataset_with_indices(
                indices_cache_file_name=indices_cache_file_name, fingerprint=new_fingerprint
            )
        else:
            return self._new_dataset_with_indices(indices_buffer=buf_writer.getvalue(), fingerprint=new_fingerprint)

    @transmit_format
    @fingerprint_transform(inplace=False, ignore_kwargs=["load_from_cache_file", "indices_cache_file_name"])
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
            column (:obj:`str`): column name to sort by.
            reverse (:obj:`bool`, default `False`): If True, sort by descending order rather then ascending.
            kind (:obj:`str`, optional): Numpy algorithm for sorting selected in {‘quicksort’, ‘mergesort’, ‘heapsort’, ‘stable’},
                The default is ‘quicksort’. Note that both ‘stable’ and ‘mergesort’ use timsort under the covers and, in general,
                the actual implementation will vary with data type. The ‘mergesort’ option is retained for backwards compatibility.
            keep_in_memory (:obj:`bool`, default `False`): Keep the sorted indices in memory instead of writing it to a cache file.
            load_from_cache_file (:obj:`bool`, default `True`): If a cache file storing the sorted indices
                can be identified, use it instead of recomputing.
            indices_cache_file_name (`Optional[str]`, default `None`): Provide the name of a path for the cache file. It is used to store the
                sorted indices instead of the automatically generated cache file name.
            writer_batch_size (:obj:`int`, default `1000`): Number of rows per write operation for the cache file writer.
                Higher value gives smaller cache files, lower value consume less temporary memory.
            new_fingerprint (`Optional[str]`, default `None`): the new fingerprint of the dataset after transform.
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
        if self.cache_files:
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
    @fingerprint_transform(
        inplace=False, randomized_function=True, ignore_kwargs=["load_from_cache_file", "indices_cache_file_name"]
    )
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
            seed (:obj:`int`, optional): A seed to initialize the default BitGenerator if ``generator=None``.
                If None, then fresh, unpredictable entropy will be pulled from the OS.
                If an int or array_like[ints] is passed, then it will be passed to SeedSequence to derive the initial BitGenerator state.
            generator (:obj:`numpy.random.Generator`, optional): Numpy random Generator to use to compute the permutation of the dataset rows.
                If ``generator=None`` (default), uses np.random.default_rng (the default BitGenerator (PCG64) of NumPy).
            keep_in_memory (:obj:`bool`, default `False`): Keep the shuffled indices in memory instead of writing it to a cache file.
            load_from_cache_file (:obj:`bool`, default `True`): If a cache file storing the shuffled indices
                can be identified, use it instead of recomputing.
            indices_cache_file_name (:obj:`str`, optional): Provide the name of a path for the cache file. It is used to store the
                shuffled indices instead of the automatically generated cache file name.
            writer_batch_size (:obj:`int`, default `1000`): Number of rows per write operation for the cache file writer.
                Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
            new_fingerprint (:obj:`str`, optional, default `None`): the new fingerprint of the dataset after transform.
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
        if self.cache_files:
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
    @fingerprint_transform(
        inplace=False,
        randomized_function=True,
        fingerprint_names=["train_new_fingerprint", "test_new_fingerprint"],
        ignore_kwargs=["load_from_cache_file", "train_indices_cache_file_name", "test_indices_cache_file_name"],
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
            test_size (:obj:`numpy.random.Generator`, optional): Size of the test split
                If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the test split.
                If int, represents the absolute number of test samples.
                If None, the value is set to the complement of the train size.
                If train_size is also None, it will be set to 0.25.
            train_size (:obj:`numpy.random.Generator`, optional): Size of the train split
                If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the train split.
                If int, represents the absolute number of train samples.
                If None, the value is automatically set to the complement of the test size.
            shuffle (:obj:`bool`, optional, default `True`): Whether or not to shuffle the data before splitting.
            seed (:obj:`int`, optional): A seed to initialize the default BitGenerator if ``generator=None``.
                If None, then fresh, unpredictable entropy will be pulled from the OS.
                If an int or array_like[ints] is passed, then it will be passed to SeedSequence to derive the initial BitGenerator state.
            generator (:obj:`numpy.random.Generator`, optional): Numpy random Generator to use to compute the permutation of the dataset rows.
                If ``generator=None`` (default), uses np.random.default_rng (the default BitGenerator (PCG64) of NumPy).
            keep_in_memory (:obj:`bool`, default `False`): Keep the splits indices in memory instead of writing it to a cache file.
            load_from_cache_file (:obj:`bool`, default `True`): If a cache file storing the splits indices
                can be identified, use it instead of recomputing.
            train_cache_file_name (:obj:`str`, optional): Provide the name of a path for the cache file. It is used to store the
                train split indices instead of the automatically generated cache file name.
            test_cache_file_name (:obj:`str`, optional): Provide the name of a path for the cache file. It is used to store the
                test split indices instead of the automatically generated cache file name.
            writer_batch_size (:obj:`int`, default `1000`): Number of rows per write operation for the cache file writer.
                Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
            train_new_fingerprint (:obj:`str`, optional, defaults to `None`): the new fingerprint of the train set after transform.
                If `None`, the new fingerprint is computed using a hash of the previous fingerprint, and the transform arguments
            test_new_fingerprint (:obj:`str`, optional, defaults to `None`): the new fingerprint of the test set after transform.
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
        if self.cache_files:
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
            num_shards (:obj:`int`): How many shards to split the dataset into.
            index (:obj:`int`): Which shard to select and return.
            contiguous: (:obj:`bool`, default `False`): Whether to select contiguous blocks of indices for shards.
            keep_in_memory (:obj:`bool`, default `False`): Keep the dataset in memory instead of writing it to a cache file.
            load_from_cache_file (:obj:`bool`, default `True`): If a cache file storing the current computation from `function`
                can be identified, use it instead of recomputing.
            indices_cache_file_name (:obj:`str`, optional): Provide the name of a path for the cache file. It is used to store the
                indices of each shard instead of the automatically generated cache file name.
            writer_batch_size (:obj:`int`, default `1000`): Number of rows per write operation for the cache file writer.
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
            filename (:obj:`str`): The filename, including the `.tfrecord` extension, to write to.
            format (`str`, optional, default `"tfrecord"`): The type of output file. Currently this is a no-op, as
                TFRecords are the only option. This enables a more flexible function signature later.
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

        def _feature(values: Union[float, int, str, np.ndarray]) -> "tf.train.Feature":
            """Typechecks `values` and returns the corresponding tf.train.Feature."""
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
            if hasattr(values, "dtype"):
                if np.issubdtype(values.dtype, np.floating):
                    return _float_feature([values.item()])
                elif np.issubdtype(values.dtype, np.integer):
                    return _int64_feature([values.item()])
                elif np.issubdtype(values.dtype, np.str):
                    return _bytes_feature([values.item().encode()])
                else:
                    raise ValueError(f"values={values} has dtype {values.dtype}, which cannot be serialized")
            else:
                raise ValueError(f"values={values} are not numpy objects, and so cannot be serialized")

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

    def to_csv(
        self,
        path_or_buf: Union[PathLike, BinaryIO],
        batch_size: Optional[int] = None,
        **to_csv_kwargs,
    ) -> int:
        """Exports the dataset to csv

        Args:
            path_or_buf (``PathLike`` or ``FileOrBuffer``): Either a path to a file or a BinaryIO.
            batch_size (Optional ``int``): Size of the batch to load in memory and write at once.
                Defaults to :obj:`datasets.config.DEFAULT_MAX_BATCH_SIZE`.
            to_csv_kwargs: Parameters to pass to pandas's :func:`pandas.DataFrame.to_csv`

        Returns:
            int: The number of characters or bytes written
        """
        # Dynamic import to avoid circular dependency
        from .io.csv import CsvDatasetWriter

        return CsvDatasetWriter(self, path_or_buf, batch_size=batch_size, **to_csv_kwargs).write()

    def to_dict(self, batch_size: Optional[int] = None, batched: bool = False) -> Union[dict, Iterator[dict]]:
        """Returns the dataset as a Python dict. Can also return a generator for large datasets.

        Args:
            batched (``bool``): Set to :obj:`True` to return a generator that yields the dataset as batches
                of ``batch_size`` rows. Defaults to :obj:`False` (returns the whole datasetas once)
            bacth_size (Optional ``int``): The size (number of rows) of the batches if ``batched`` is `True`.
                Defaults to :obj:`datasets.config.DEFAULT_MAX_BATCH_SIZE`.

        Returns:
            `dict` or `Iterator[dict]`
        """
        if not batched:
            return query_table(
                table=self._data,
                key=slice(0, len(self)),
                indices=self._indices if self._indices is not None else None,
            ).to_pydict()
        else:
            batch_size = batch_size if batch_size else config.DEFAULT_MAX_BATCH_SIZE
            return (
                query_table(
                    table=self._data,
                    key=slice(offset, offset + batch_size),
                    indices=self._indices if self._indices is not None else None,
                ).to_pydict()
                for offset in range(0, len(self), batch_size)
            )

    def to_pandas(
        self, batch_size: Optional[int] = None, batched: bool = False
    ) -> Union[pd.DataFrame, Iterator[pd.DataFrame]]:
        """Returns the dataset as a :class:`pandas.DataFrame`. Can also return a generator for large datasets.

        Args:
            batched (``bool``): Set to :obj:`True` to return a generator that yields the dataset as batches
                of ``batch_size`` rows. Defaults to :obj:`False` (returns the whole datasetas once)
            bacth_size (Optional ``int``): The size (number of rows) of the batches if ``batched`` is `True`.
                Defaults to :obj:`datasets.config.DEFAULT_MAX_BATCH_SIZE`.

        Returns:
            `pandas.DataFrame` or `Iterator[pandas.DataFrame]`
        """
        if not batched:
            return query_table(
                table=self._data,
                key=slice(0, len(self)),
                indices=self._indices if self._indices is not None else None,
            ).to_pandas()
        else:
            batch_size = batch_size if batch_size else config.DEFAULT_MAX_BATCH_SIZE
            return (
                query_table(
                    table=self._data,
                    key=slice(offset, offset + batch_size),
                    indices=self._indices if self._indices is not None else None,
                ).to_pandas()
                for offset in range(0, len(self), batch_size)
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

        Example:
            .. code-block:: python

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
                This is the index name that is used to call :meth:`Dataset.get_nearest_examples` or :meth:`Dataset.search`.
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
                Default config is::

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

        Example:
            .. code-block:: python

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
    Converts a list of :class:`Dataset` with the same schema into a single :class:`Dataset`.

    Args:
        dsets (:obj:`List[datasets.Dataset]`): List of Datasets to concatenate.
        info (:class:`DatasetInfo`, optional): Dataset information, like description, citation, etc.
        split (:class:`NamedSplit`, optional): Name of the dataset split.
    """
    if not all([dset.features.type == dsets[0].features.type for dset in dsets]):
        raise ValueError("Features must match for all datasets")

    # Find common format or reset format
    format = dsets[0].format
    if any(dset.format != format for dset in dsets):
        format = {}
        logger.info("Some of the datasets have disparate format. Resetting the format of the concatenated dataset.")

    # Concatenate tables
    table = concat_tables(dset._data for dset in dsets if len(dset._data) > 0)

    def apply_offset_to_indices_table(table, offset):
        if offset == 0:
            return table
        else:
            array = table["indices"]
            new_array = pc.add(array, pa.scalar(offset, type=pa.uint64()))
            return InMemoryTable.from_arrays([new_array], names=["indices"])

    # Concatenate indices if they exist
    if any(dset._indices is not None for dset in dsets):

        # Datasets with no indices tables are replaced with a dataset with an indices table in memory.
        # Applying an offset to an indices table also brings the table in memory.
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
            indices_table = concat_tables(indices_tables)
        else:
            indices_table = InMemoryTable.from_batches([], schema=pa.schema({"indices": pa.int64()}))
    else:
        indices_table = None

    # Concatenate infos
    if info is None:
        info = DatasetInfo.from_merge([dset.info for dset in dsets])
    fingerprint = update_fingerprint(
        "".join(dset._fingerprint for dset in dsets), concatenate_datasets, {"info": info, "split": split}
    )

    # Make final concatenated dataset
    concatenated_dataset = Dataset(
        table,
        info=info,
        split=split,
        indices_table=indices_table,
        fingerprint=fingerprint,
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
