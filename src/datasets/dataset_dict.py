import contextlib
import copy
import json
import os
import re
from io import BytesIO
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import fsspec
import numpy as np
from huggingface_hub import HfApi

from . import config
from .arrow_dataset import Dataset
from .features import Features
from .filesystems import extract_path_from_uri, is_remote_filesystem
from .info import DatasetInfo
from .splits import NamedSplit, Split, SplitDict, SplitInfo
from .table import Table
from .tasks import TaskTemplate
from .utils import logging
from .utils.deprecation_utils import deprecated
from .utils.doc_utils import is_documented_by
from .utils.typing import PathLike


logger = logging.get_logger(__name__)


class DatasetDict(dict):
    """A dictionary (dict of str: datasets.Dataset) with dataset transforms methods (map, filter, etc.)"""

    def _check_values_type(self):
        for dataset in self.values():
            if not isinstance(dataset, Dataset):
                raise TypeError(f"Values in `DatasetDict` should of type `Dataset` but got type '{type(dataset)}'")

    def __getitem__(self, k) -> Dataset:
        if isinstance(k, (str, NamedSplit)) or len(self) == 0:
            return super().__getitem__(k)
        else:
            available_suggested_splits = [
                str(split) for split in (Split.TRAIN, Split.TEST, Split.VALIDATION) if split in self
            ]
            suggested_split = available_suggested_splits[0] if available_suggested_splits else list(self)[0]
            raise KeyError(
                f"Invalid key: {k}. Please first select a split. For example: "
                f"`my_dataset_dictionary['{suggested_split}'][{k}]`. "
                f"Available splits: {sorted(self)}"
            )

    @property
    def data(self) -> Dict[str, Table]:
        """The Apache Arrow tables backing each split."""
        self._check_values_type()
        return {k: dataset.data for k, dataset in self.items()}

    @property
    def cache_files(self) -> Dict[str, Dict]:
        """The cache files containing the Apache Arrow table backing each split."""
        self._check_values_type()
        return {k: dataset.cache_files for k, dataset in self.items()}

    @property
    def num_columns(self) -> Dict[str, int]:
        """Number of columns in each split of the dataset."""
        self._check_values_type()
        return {k: dataset.num_columns for k, dataset in self.items()}

    @property
    def num_rows(self) -> Dict[str, int]:
        """Number of rows in each split of the dataset (same as :func:`datasets.Dataset.__len__`)."""
        self._check_values_type()
        return {k: dataset.num_rows for k, dataset in self.items()}

    @property
    def column_names(self) -> Dict[str, List[str]]:
        """Names of the columns in each split of the dataset."""
        self._check_values_type()
        return {k: dataset.column_names for k, dataset in self.items()}

    @property
    def shape(self) -> Dict[str, Tuple[int]]:
        """Shape of each split of the dataset (number of columns, number of rows)."""
        self._check_values_type()
        return {k: dataset.shape for k, dataset in self.items()}

    @deprecated()
    def dictionary_encode_column_(self, column: str):
        """Dictionary encode a column in each split.

        Dictionary encode can reduce the size of a column with many repetitions (e.g. string labels columns)
        by storing a dictionary of the strings. This only affect the internal storage.

        .. deprecated:: 1.4.0

        Args:
            column (:obj:`str`):

        """
        self._check_values_type()
        for dataset in self.values():
            dataset.dictionary_encode_column_(column=column)

    @deprecated(help_message="Use DatasetDict.flatten instead.")
    def flatten_(self, max_depth=16):
        """In-place version of :meth:`DatasetDict.flatten`.

        .. deprecated:: 1.4.0
            Use :meth:`DatasetDict.flatten` instead.
        """
        self._check_values_type()
        for dataset in self.values():
            dataset.flatten_(max_depth=max_depth)

    def flatten(self, max_depth=16) -> "DatasetDict":
        """Flatten the Apache Arrow Table of each split (nested features are flatten).
        Each column with a struct type is flattened into one column per struct field.
        Other columns are left unchanged.
        """
        self._check_values_type()
        return DatasetDict({k: dataset.flatten(max_depth=max_depth) for k, dataset in self.items()})

    def unique(self, column: str) -> Dict[str, List[Any]]:
        """Return a list of the unique elements in a column for each split.

        This is implemented in the low-level backend and as such, very fast.

        Args:
            column (:obj:`str`):
                column name (list all the column names with :func:`datasets.Dataset.column_names`)

        Returns:
            Dict[:obj:`str`, :obj:`list`]: Dictionary of unique elements in the given column.

        """
        self._check_values_type()
        return {k: dataset.unique(column) for k, dataset in self.items()}

    def cleanup_cache_files(self) -> Dict[str, int]:
        """Clean up all cache files in the dataset cache directory, excepted the currently used cache file if there is one.
        Be carefull when running this command that no other process is currently using other cache files.

        Return:
            Dict with the number of removed files for each split
        """
        self._check_values_type()
        return {k: dataset.cleanup_cache_files() for k, dataset in self.items()}

    def __repr__(self):
        repr = "\n".join([f"{k}: {v}" for k, v in self.items()])
        repr = re.sub(r"^", " " * 4, repr, 0, re.M)
        return f"DatasetDict({{\n{repr}\n}})"

    @deprecated(help_message="Use DatasetDict.cast instead.")
    def cast_(self, features: Features):
        """In-place version of :meth:`DatasetDict.cast`.

        .. deprecated:: 1.4.0
            Use :meth:`DatasetDict.cast` instead.

        Args:
            features (:class:`datasets.Features`): New features to cast the dataset to.
                The name and order of the fields in the features must match the current column names.
                The type of the data must also be convertible from one type to the other.
                For non-trivial conversion, e.g. string <-> ClassLabel you should use :func:`map` to update the Dataset.
        """
        self._check_values_type()
        new_dataset_dict = {k: dataset.cast(features=features) for k, dataset in self.items()}
        self.update(new_dataset_dict)

    def cast(self, features: Features) -> "DatasetDict":
        """
        Cast the dataset to a new set of features.
        The transformation is applied to all the datasets of the dataset dictionary.

        You can also remove a column using :func:`Dataset.map` with `feature` but :func:`cast_`
        is in-place (doesn't copy the data to a new dataset) and is thus faster.

        Args:
            features (:class:`datasets.Features`): New features to cast the dataset to.
                The name and order of the fields in the features must match the current column names.
                The type of the data must also be convertible from one type to the other.
                For non-trivial conversion, e.g. string <-> ClassLabel you should use :func:`map` to update the Dataset.
        """
        self._check_values_type()
        return DatasetDict({k: dataset.cast(features=features) for k, dataset in self.items()})

    def cast_column(self, column: str, feature) -> "DatasetDict":
        """Cast column to feature for decoding.

        Args:
            column (:obj:`str`): Column name.
            feature (:class:`Feature`): Target feature.

        Returns:
            :class:`DatasetDict`
        """
        self._check_values_type()
        return DatasetDict({k: dataset.cast_column(column=column, feature=feature) for k, dataset in self.items()})

    @deprecated(help_message="Use DatasetDict.remove_columns instead.")
    def remove_columns_(self, column_names: Union[str, List[str]]):
        """In-place version of :meth:`DatasetDict.remove_columns`.

        .. deprecated:: 1.4.0
            Use :meth:`DatasetDict.remove_columns` instead.

        Args:
            column_names (:obj:`Union[str, List[str]]`): Name of the column(s) to remove.
        """
        self._check_values_type()
        new_dataset_dict = {k: dataset.remove_columns(column_names=column_names) for k, dataset in self.items()}
        self.update(new_dataset_dict)

    def remove_columns(self, column_names: Union[str, List[str]]) -> "DatasetDict":
        """
        Remove one or several column(s) from each split in the dataset
        and the features associated to the column(s).

        The transformation is applied to all the splits of the dataset dictionary.

        You can also remove a column using :func:`Dataset.map` with `remove_columns` but the present method
        is in-place (doesn't copy the data to a new dataset) and is thus faster.

        Args:
            column_names (:obj:`Union[str, List[str]]`): Name of the column(s) to remove.
        """
        self._check_values_type()
        return DatasetDict({k: dataset.remove_columns(column_names=column_names) for k, dataset in self.items()})

    @deprecated(help_message="Use DatasetDict.rename_column instead.")
    def rename_column_(self, original_column_name: str, new_column_name: str):
        """In-place version of :meth:`DatasetDict.rename_column`.

        .. deprecated:: 1.4.0
            Use :meth:`DatasetDict.rename_column` instead.

        Args:
            original_column_name (:obj:`str`): Name of the column to rename.
            new_column_name (:obj:`str`): New name for the column.
        """
        self._check_values_type()
        new_dataset_dict = {
            k: dataset.rename_column(original_column_name=original_column_name, new_column_name=new_column_name)
            for k, dataset in self.items()
        }
        self.update(new_dataset_dict)

    def rename_column(self, original_column_name: str, new_column_name: str) -> "DatasetDict":
        """
        Rename a column in the dataset and move the features associated to the original column under the new column name.
        The transformation is applied to all the datasets of the dataset dictionary.

        You can also rename a column using :func:`Dataset.map` with `remove_columns` but the present method:
            - takes care of moving the original features under the new column name.
            - doesn't copy the data to a new dataset and is thus much faster.

        Args:
            original_column_name (:obj:`str`): Name of the column to rename.
            new_column_name (:obj:`str`): New name for the column.
        """
        self._check_values_type()
        return DatasetDict(
            {
                k: dataset.rename_column(original_column_name=original_column_name, new_column_name=new_column_name)
                for k, dataset in self.items()
            }
        )

    def class_encode_column(self, column: str, include_nulls: bool = False) -> "DatasetDict":
        """Casts the given column as :obj:``datasets.features.ClassLabel`` and updates the tables.

        Args:
            column (`str`): The name of the column to cast
            include_nulls (`bool`, default `False`):
                Whether to include null values in the class labels. If True, the null values will be encoded as the `"None"` class label.

                .. versionadded:: 1.14.2
        """
        self._check_values_type()
        return DatasetDict(
            {k: dataset.class_encode_column(column=column, include_nulls=include_nulls) for k, dataset in self.items()}
        )

    @contextlib.contextmanager
    def formatted_as(
        self,
        type: Optional[str] = None,
        columns: Optional[List] = None,
        output_all_columns: bool = False,
        **format_kwargs,
    ):
        """To be used in a `with` statement. Set __getitem__ return format (type and columns)
        The transformation is applied to all the datasets of the dataset dictionary.

        Args:
            type (Optional ``str``): output type selected in [None, 'numpy', 'torch', 'tensorflow', 'pandas', 'arrow']
                None means __getitem__ returns python objects (default)
            columns (Optional ``List[str]``): columns to format in the output
                None means __getitem__ returns all columns (default)
            output_all_columns (``bool`` default to False): keep un-formatted columns as well in the output (as python objects)
            format_kwargs: keywords arguments passed to the convert function like `np.array`, `torch.tensor` or `tensorflow.ragged.constant`.
        """
        self._check_values_type()
        old_format_type = {k: dataset._format_type for k, dataset in self.items()}
        old_format_kwargs = {k: dataset._format_kwargs for k, dataset in self.items()}
        old_format_columns = {k: dataset._format_columns for k, dataset in self.items()}
        old_output_all_columns = {k: dataset._output_all_columns for k, dataset in self.items()}
        try:
            self.set_format(type, columns, output_all_columns, **format_kwargs)
            yield
        finally:
            for k, dataset in self.items():
                dataset.set_format(
                    old_format_type[k], old_format_columns[k], old_output_all_columns[k], **old_format_kwargs[k]
                )

    def set_format(
        self,
        type: Optional[str] = None,
        columns: Optional[List] = None,
        output_all_columns: bool = False,
        **format_kwargs,
    ):
        """Set __getitem__ return format (type and columns)
        The format is set for every dataset in the dataset dictionary

        Args:
            type (Optional ``str``): output type selected in [None, 'numpy', 'torch', 'tensorflow', 'pandas', 'arrow']
                None means __getitem__ returns python objects (default)
            columns (Optional ``List[str]``): columns to format in the output.
                None means __getitem__ returns all columns (default).
            output_all_columns (``bool`` default to False): keep un-formatted columns as well in the output (as python objects)
            format_kwargs: keywords arguments passed to the convert function like `np.array`, `torch.tensor` or `tensorflow.ragged.constant`.

        It is possible to call ``map`` after calling ``set_format``. Since ``map`` may add new columns, then the list of formatted columns
        gets updated. In this case, if you apply ``map`` on a dataset to add a new column, then this column will be formatted:

            new formatted columns = (all columns - previously unformatted columns)
        """
        self._check_values_type()
        for dataset in self.values():
            dataset.set_format(type=type, columns=columns, output_all_columns=output_all_columns, **format_kwargs)

    def reset_format(self):
        """Reset __getitem__ return format to python objects and all columns.
        The transformation is applied to all the datasets of the dataset dictionary.

        Same as ``self.set_format()``
        """
        self._check_values_type()
        for dataset in self.values():
            dataset.set_format()

    def set_transform(
        self,
        transform: Optional[Callable],
        columns: Optional[List] = None,
        output_all_columns: bool = False,
    ):
        """Set __getitem__ return format using this transform. The transform is applied on-the-fly on batches when __getitem__ is called.
        The transform is set for every dataset in the dataset dictionary
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
        self._check_values_type()
        for dataset in self.values():
            dataset.set_format("custom", columns=columns, output_all_columns=output_all_columns, transform=transform)

    def with_format(
        self,
        type: Optional[str] = None,
        columns: Optional[List] = None,
        output_all_columns: bool = False,
        **format_kwargs,
    ) -> "DatasetDict":
        """Set __getitem__ return format (type and columns). The data formatting is applied on-the-fly.
        The format ``type`` (for example "numpy") is used to format batches when using __getitem__.
        The format is set for every dataset in the dataset dictionary

        It's also possible to use custom transforms for formatting using :func:`datasets.Dataset.with_transform`.

        Contrary to :func:`datasets.DatasetDict.set_format`, ``with_format`` returns a new DatasetDict object with new Dataset objects.

        Args:
            type (Optional ``str``):
                Either output type selected in [None, 'numpy', 'torch', 'tensorflow', 'pandas', 'arrow'].
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
    ) -> "DatasetDict":
        """Set __getitem__ return format using this transform. The transform is applied on-the-fly on batches when __getitem__ is called.
        The transform is set for every dataset in the dataset dictionary

        As :func:`datasets.Dataset.set_format`, this can be reset using :func:`datasets.Dataset.reset_format`.

        Contrary to :func:`datasets.DatasetDict.set_transform`, ``with_transform`` returns a new DatasetDict object with new Dataset objects.

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

    def map(
        self,
        function,
        with_indices: bool = False,
        input_columns: Optional[Union[str, List[str]]] = None,
        batched: bool = False,
        batch_size: Optional[int] = 1000,
        remove_columns: Optional[Union[str, List[str]]] = None,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        cache_file_names: Optional[Dict[str, Optional[str]]] = None,
        writer_batch_size: Optional[int] = 1000,
        features: Optional[Features] = None,
        disable_nullable: bool = False,
        fn_kwargs: Optional[dict] = None,
        num_proc: Optional[int] = None,
        desc: Optional[str] = None,
    ) -> "DatasetDict":
        """Apply a function to all the elements in the table (individually or in batches)
        and update the table (if function does updated examples).
        The transformation is applied to all the datasets of the dataset dictionary.

        Args:
            function (`callable`): with one of the following signature:
                - `function(example: Dict) -> Union[Dict, Any]` if `batched=False` and `with_indices=False`
                - `function(example: Dict, indices: int) -> Union[Dict, Any]` if `batched=False` and `with_indices=True`
                - `function(batch: Dict[List]) -> Union[Dict, Any]` if `batched=True` and `with_indices=False`
                - `function(batch: Dict[List], indices: List[int]) -> Union[Dict, Any]` if `batched=True` and `with_indices=True`
            with_indices (`bool`, defaults to `False`): Provide example indices to `function`. Note that in this case the signature of `function` should be `def function(example, idx): ...`.
            input_columns (`Optional[Union[str, List[str]]]`, defaults to `None`): The columns to be passed into `function` as
                positional arguments. If `None`, a dict mapping to all formatted columns is passed as one argument.
            batched (`bool`, defaults to `False`): Provide batch of examples to `function`
            batch_size (`Optional[int]`, defaults to `1000`): Number of examples per batch provided to `function` if `batched=True`
                `batch_size <= 0` or `batch_size == None`: Provide the full dataset as a single batch to `function`
            remove_columns (`Optional[Union[str, List[str]]]`, defaults to `None`): Remove a selection of columns while doing the mapping.
                Columns will be removed before updating the examples with the output of `function`, i.e. if `function` is adding
                columns with names in `remove_columns`, these columns will be kept.
            keep_in_memory (`bool`, defaults to `False`): Keep the dataset in memory instead of writing it to a cache file.
            load_from_cache_file (`bool`, defaults to `True`): If a cache file storing the current computation from `function`
                can be identified, use it instead of recomputing.
            cache_file_names (`Optional[Dict[str, str]]`, defaults to `None`): Provide the name of a path for the cache file. It is used to store the
                results of the computation instead of the automatically generated cache file name.
                You have to provide one :obj:`cache_file_name` per dataset in the dataset dictionary.
            writer_batch_size (:obj:`int`, default `1000`): Number of rows per write operation for the cache file writer.
                This value is a good trade-off between memory usage during the processing, and processing speed.
                Higher value makes the processing do fewer lookups, lower value consume less temporary memory while running `.map()`.
            features (`Optional[datasets.Features]`, defaults to `None`): Use a specific Features to store the cache file
                instead of the automatically generated one.
            disable_nullable (`bool`, defaults to `False`): Disallow null values in the table.
            fn_kwargs (`Optional[Dict]`, defaults to `None`): Keyword arguments to be passed to `function`
            num_proc (`Optional[int]`, defaults to `None`): Number of processes for multiprocessing. By default it doesn't
                use multiprocessing.
            desc (`Optional[str]`, defaults to `None`): Meaningful description to be displayed alongside with the progress bar while mapping examples.
        """
        self._check_values_type()
        if cache_file_names is None:
            cache_file_names = {k: None for k in self}
        return DatasetDict(
            {
                k: dataset.map(
                    function=function,
                    with_indices=with_indices,
                    input_columns=input_columns,
                    batched=batched,
                    batch_size=batch_size,
                    remove_columns=remove_columns,
                    keep_in_memory=keep_in_memory,
                    load_from_cache_file=load_from_cache_file,
                    cache_file_name=cache_file_names[k],
                    writer_batch_size=writer_batch_size,
                    features=features,
                    disable_nullable=disable_nullable,
                    fn_kwargs=fn_kwargs,
                    num_proc=num_proc,
                    desc=desc,
                )
                for k, dataset in self.items()
            }
        )

    def filter(
        self,
        function,
        with_indices=False,
        input_columns: Optional[Union[str, List[str]]] = None,
        batched: bool = False,
        batch_size: Optional[int] = 1000,
        remove_columns: Optional[List[str]] = None,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        cache_file_names: Optional[Dict[str, Optional[str]]] = None,
        writer_batch_size: Optional[int] = 1000,
        fn_kwargs: Optional[dict] = None,
        num_proc: Optional[int] = None,
        desc: Optional[str] = None,
    ) -> "DatasetDict":
        """Apply a filter function to all the elements in the table in batches
        and update the table so that the dataset only includes examples according to the filter function.
        The transformation is applied to all the datasets of the dataset dictionary.

        Args:
            function (`callable`): with one of the following signature:
                - ``function(example: Union[Dict, Any]) -> bool`` if ``with_indices=False, batched=False``
                - ``function(example: Union[Dict, Any], indices: int) -> bool`` if ``with_indices=True, batched=False``
                - ``function(example: Union[Dict, Any]) -> List[bool]`` if ``with_indices=False, batched=True``
                - ``function(example: Union[Dict, Any], indices: int) -> List[bool]`` if ``with_indices=True, batched=True``
            with_indices (`bool`, defaults to `False`): Provide example indices to `function`. Note that in this case the signature of `function` should be `def function(example, idx): ...`.
            input_columns (`Optional[Union[str, List[str]]]`, defaults to `None`): The columns to be passed into `function` as
                positional arguments. If `None`, a dict mapping to all formatted columns is passed as one argument.
            batched (`bool`, defaults to `False`): Provide batch of examples to `function`
            batch_size (`Optional[int]`, defaults to `1000`): Number of examples per batch provided to `function` if `batched=True`
                `batch_size <= 0` or `batch_size == None`: Provide the full dataset as a single batch to `function`
            remove_columns (`Optional[List[str]]`, defaults to `None`): Remove a selection of columns while doing the mapping.
                Columns will be removed before updating the examples with the output of `function`, i.e. if `function` is adding
                columns with names in `remove_columns`, these columns will be kept.
            keep_in_memory (`bool`, defaults to `False`): Keep the dataset in memory instead of writing it to a cache file.
            load_from_cache_file (`bool`, defaults to `True`): If a cache file storing the current computation from `function`
                can be identified, use it instead of recomputing.
            cache_file_names (`Optional[Dict[str, str]]`, defaults to `None`): Provide the name of a path for the cache file. It is used to store the
                results of the computation instead of the automatically generated cache file name.
                You have to provide one :obj:`cache_file_name` per dataset in the dataset dictionary.
            writer_batch_size (:obj:`int`, default `1000`): Number of rows per write operation for the cache file writer.
                This value is a good trade-off between memory usage during the processing, and processing speed.
                Higher value makes the processing do fewer lookups, lower value consume less temporary memory while running `.map()`.
            fn_kwargs (`Optional[Dict]`, defaults to `None`): Keyword arguments to be passed to `function`
            num_proc (`Optional[int]`, defaults to `None`): Number of processes for multiprocessing. By default it doesn't
                use multiprocessing.
            desc (`Optional[str]`, defaults to `None`): Meaningful description to be displayed alongside with the progress bar while filtering examples.
        """
        self._check_values_type()
        if cache_file_names is None:
            cache_file_names = {k: None for k in self}
        return DatasetDict(
            {
                k: dataset.filter(
                    function=function,
                    with_indices=with_indices,
                    input_columns=input_columns,
                    batched=batched,
                    batch_size=batch_size,
                    remove_columns=remove_columns,
                    keep_in_memory=keep_in_memory,
                    load_from_cache_file=load_from_cache_file,
                    cache_file_name=cache_file_names[k],
                    writer_batch_size=writer_batch_size,
                    fn_kwargs=fn_kwargs,
                    num_proc=num_proc,
                    desc=desc,
                )
                for k, dataset in self.items()
            }
        )

    def sort(
        self,
        column: str,
        reverse: bool = False,
        kind: str = None,
        null_placement: str = "last",
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        indices_cache_file_names: Optional[Dict[str, Optional[str]]] = None,
        writer_batch_size: Optional[int] = 1000,
    ) -> "DatasetDict":
        """Create a new dataset sorted according to a column.
        The transformation is applied to all the datasets of the dataset dictionary.

        Currently sorting according to a column name uses pandas sorting algorithm under the hood.
        The column should thus be a pandas compatible type (in particular not a nested type).
        This also means that the column used for sorting is fully loaded in memory (which should be fine in most cases).

        Args:
            column (:obj:`str`): column name to sort by.
            reverse (:obj:`bool`, default `False`): If True, sort by descending order rather then ascending.
            kind (:obj:`str`, optional): Pandas algorithm for sorting selected in {‘quicksort’, ‘mergesort’, ‘heapsort’, ‘stable’},
                The default is ‘quicksort’. Note that both ‘stable’ and ‘mergesort’ use timsort under the covers and, in general,
                the actual implementation will vary with data type. The ‘mergesort’ option is retained for backwards compatibility.
            null_placement (:obj:`str`, default `last`):
                Put `None` values at the beginning if ‘first‘; ‘last‘ puts `None` values at the end.

                .. versionadded:: 1.14.2
            keep_in_memory (:obj:`bool`, default `False`): Keep the sorted indices in memory instead of writing it to a cache file.
            load_from_cache_file (:obj:`bool`, default `True`): If a cache file storing the sorted indices
                can be identified, use it instead of recomputing.
            indices_cache_file_names (`Optional[Dict[str, str]]`, defaults to `None`): Provide the name of a path for the cache file. It is used to store the
                indices mapping instead of the automatically generated cache file name.
                You have to provide one :obj:`cache_file_name` per dataset in the dataset dictionary.
            writer_batch_size (:obj:`int`, default `1000`): Number of rows per write operation for the cache file writer.
                Higher value gives smaller cache files, lower value consume less temporary memory.
        """
        self._check_values_type()
        if indices_cache_file_names is None:
            indices_cache_file_names = {k: None for k in self}
        return DatasetDict(
            {
                k: dataset.sort(
                    column=column,
                    reverse=reverse,
                    kind=kind,
                    null_placement=null_placement,
                    keep_in_memory=keep_in_memory,
                    load_from_cache_file=load_from_cache_file,
                    indices_cache_file_name=indices_cache_file_names[k],
                    writer_batch_size=writer_batch_size,
                )
                for k, dataset in self.items()
            }
        )

    def shuffle(
        self,
        seeds: Optional[Union[int, Dict[str, Optional[int]]]] = None,
        seed: Optional[int] = None,
        generators: Optional[Dict[str, np.random.Generator]] = None,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        indices_cache_file_names: Optional[Dict[str, Optional[str]]] = None,
        writer_batch_size: Optional[int] = 1000,
    ) -> "DatasetDict":
        """Create a new Dataset where the rows are shuffled.

        The transformation is applied to all the datasets of the dataset dictionary.

        Currently shuffling uses numpy random generators.
        You can either supply a NumPy BitGenerator to use, or a seed to initiate NumPy's default random generator (PCG64).

        Args:
            seeds (`Dict[str, int]` or `int`, optional): A seed to initialize the default BitGenerator if ``generator=None``.
                If None, then fresh, unpredictable entropy will be pulled from the OS.
                If an int or array_like[ints] is passed, then it will be passed to SeedSequence to derive the initial BitGenerator state.
                You can provide one :obj:`seed` per dataset in the dataset dictionary.
            seed (Optional `int`): A seed to initialize the default BitGenerator if ``generator=None``. Alias for seeds (the seed argument has priority over seeds if both arguments are provided).
            generators (Optional `Dict[str, np.random.Generator]`): Numpy random Generator to use to compute the permutation of the dataset rows.
                If ``generator=None`` (default), uses np.random.default_rng (the default BitGenerator (PCG64) of NumPy).
                You have to provide one :obj:`generator` per dataset in the dataset dictionary.
            keep_in_memory (`bool`, defaults to `False`): Keep the dataset in memory instead of writing it to a cache file.
            load_from_cache_file (`bool`, defaults to `True`): If a cache file storing the current computation from `function`
                can be identified, use it instead of recomputing.
            indices_cache_file_names (`Dict[str, str]`, optional): Provide the name of a path for the cache file. It is used to store the
                indices mappings instead of the automatically generated cache file name.
                You have to provide one :obj:`cache_file_name` per dataset in the dataset dictionary.
            writer_batch_size (:obj:`int`, default `1000`): Number of rows per write operation for the cache file writer.
                This value is a good trade-off between memory usage during the processing, and processing speed.
                Higher value makes the processing do fewer lookups, lower value consume less temporary memory while running `.map()`.
        """
        self._check_values_type()
        if seed is not None and seeds is not None:
            raise ValueError("Please specify seed or seeds, but not both")
        seeds = seed if seed is not None else seeds
        if seeds is None:
            seeds = {k: None for k in self}
        elif not isinstance(seeds, dict):
            seeds = {k: seeds for k in self}
        if generators is None:
            generators = {k: None for k in self}
        if indices_cache_file_names is None:
            indices_cache_file_names = {k: None for k in self}
        return DatasetDict(
            {
                k: dataset.shuffle(
                    seed=seeds[k],
                    generator=generators[k],
                    keep_in_memory=keep_in_memory,
                    load_from_cache_file=load_from_cache_file,
                    indices_cache_file_name=indices_cache_file_names[k],
                    writer_batch_size=writer_batch_size,
                )
                for k, dataset in self.items()
            }
        )

    def save_to_disk(self, dataset_dict_path: str, fs=None):
        """
        Saves a dataset dict to a filesystem using either :class:`~filesystems.S3FileSystem` or
        ``fsspec.spec.AbstractFileSystem``.

        Args:
            dataset_dict_path (``str``): Path (e.g. `dataset/train`) or remote URI
                (e.g. `s3://my-bucket/dataset/train`) of the dataset dict directory where the dataset dict will be
                saved to.
            fs (:class:`~filesystems.S3FileSystem`, ``fsspec.spec.AbstractFileSystem``, optional, defaults ``None``):
                Instance of the remote filesystem used to download the files from.
        """
        if is_remote_filesystem(fs):
            dest_dataset_dict_path = extract_path_from_uri(dataset_dict_path)
        else:
            fs = fsspec.filesystem("file")
            dest_dataset_dict_path = dataset_dict_path
            os.makedirs(dest_dataset_dict_path, exist_ok=True)

        json.dump(
            {"splits": list(self)},
            fs.open(Path(dest_dataset_dict_path, config.DATASETDICT_JSON_FILENAME).as_posix(), "w", encoding="utf-8"),
        )
        for k, dataset in self.items():
            dataset.save_to_disk(Path(dest_dataset_dict_path, k).as_posix(), fs)

    @staticmethod
    def load_from_disk(dataset_dict_path: str, fs=None, keep_in_memory: Optional[bool] = None) -> "DatasetDict":
        """
        Load a dataset that was previously saved using :meth:`save_to_disk` from a filesystem using either
        :class:`~filesystems.S3FileSystem` or ``fsspec.spec.AbstractFileSystem``.

        Args:
            dataset_dict_path (:obj:`str`): Path (e.g. ``"dataset/train"``) or remote URI (e.g.
                ``"s3//my-bucket/dataset/train"``) of the dataset dict directory where the dataset dict will be loaded
                from.
            fs (:class:`~filesystems.S3FileSystem` or ``fsspec.spec.AbstractFileSystem``, optional, default ``None``):
                Instance of the remote filesystem used to download the files from.
            keep_in_memory (:obj:`bool`, default ``None``): Whether to copy the dataset in-memory. If `None`, the
                dataset will not be copied in-memory unless explicitly enabled by setting
                `datasets.config.IN_MEMORY_MAX_SIZE` to nonzero. See more details in the
                :ref:`load_dataset_enhancing_performance` section.

        Returns:
            :class:`DatasetDict`
        """
        dataset_dict = DatasetDict()
        if is_remote_filesystem(fs):
            dest_dataset_dict_path = extract_path_from_uri(dataset_dict_path)
        else:
            fs = fsspec.filesystem("file")
            dest_dataset_dict_path = dataset_dict_path
        dataset_dict_json_path = Path(dest_dataset_dict_path, config.DATASETDICT_JSON_FILENAME).as_posix()
        dataset_info_path = Path(dest_dataset_dict_path, config.DATASET_INFO_FILENAME).as_posix()
        if fs.isfile(dataset_info_path) and not fs.isfile(dataset_dict_json_path):
            raise FileNotFoundError(
                f"No such file or directory: '{dataset_dict_json_path}'. Expected to load a DatasetDict object, but got a Dataset. Please use datasets.load_from_disk instead."
            )
        for k in json.load(fs.open(dataset_dict_json_path, "r", encoding="utf-8"))["splits"]:
            dataset_dict_split_path = (
                dataset_dict_path.split("://")[0] + "://" + Path(dest_dataset_dict_path, k).as_posix()
                if is_remote_filesystem(fs)
                else Path(dest_dataset_dict_path, k).as_posix()
            )
            dataset_dict[k] = Dataset.load_from_disk(dataset_dict_split_path, fs, keep_in_memory=keep_in_memory)
        return dataset_dict

    @staticmethod
    def from_csv(
        path_or_paths: Dict[str, PathLike],
        features: Optional[Features] = None,
        cache_dir: str = None,
        keep_in_memory: bool = False,
        **kwargs,
    ) -> "DatasetDict":
        """Create DatasetDict from CSV file(s).

        Args:
            path_or_paths (dict of path-like): Path(s) of the CSV file(s).
            features (:class:`Features`, optional): Dataset features.
            cache_dir (str, optional, default="~/.cache/huggingface/datasets"): Directory to cache data.
            keep_in_memory (bool, default=False): Whether to copy the data in-memory.
            **kwargs: Keyword arguments to be passed to :meth:`pandas.read_csv`.

        Returns:
            :class:`DatasetDict`
        """
        # Dynamic import to avoid circular dependency
        from .io.csv import CsvDatasetReader

        return CsvDatasetReader(
            path_or_paths, features=features, cache_dir=cache_dir, keep_in_memory=keep_in_memory, **kwargs
        ).read()

    @staticmethod
    def from_json(
        path_or_paths: Dict[str, PathLike],
        features: Optional[Features] = None,
        cache_dir: str = None,
        keep_in_memory: bool = False,
        **kwargs,
    ) -> "DatasetDict":
        """Create DatasetDict from JSON Lines file(s).

        Args:
            path_or_paths (path-like or list of path-like): Path(s) of the JSON Lines file(s).
            features (:class:`Features`, optional): Dataset features.
            cache_dir (str, optional, default="~/.cache/huggingface/datasets"): Directory to cache data.
            keep_in_memory (bool, default=False): Whether to copy the data in-memory.
            **kwargs: Keyword arguments to be passed to :class:`JsonConfig`.

        Returns:
            :class:`DatasetDict`
        """
        # Dynamic import to avoid circular dependency
        from .io.json import JsonDatasetReader

        return JsonDatasetReader(
            path_or_paths, features=features, cache_dir=cache_dir, keep_in_memory=keep_in_memory, **kwargs
        ).read()

    @staticmethod
    def from_parquet(
        path_or_paths: Dict[str, PathLike],
        features: Optional[Features] = None,
        cache_dir: str = None,
        keep_in_memory: bool = False,
        columns: Optional[List[str]] = None,
        **kwargs,
    ) -> "DatasetDict":
        """Create DatasetDict from Parquet file(s).

        Args:
            path_or_paths (dict of path-like): Path(s) of the CSV file(s).
            features (:class:`Features`, optional): Dataset features.
            cache_dir (str, optional, default="~/.cache/huggingface/datasets"): Directory to cache data.
            keep_in_memory (bool, default=False): Whether to copy the data in-memory.
            columns (:obj:`List[str]`, optional): If not None, only these columns will be read from the file.
                A column name may be a prefix of a nested field, e.g. 'a' will select
                'a.b', 'a.c', and 'a.d.e'.
            **kwargs: Keyword arguments to be passed to :class:`ParquetConfig`.

        Returns:
            :class:`DatasetDict`
        """
        # Dynamic import to avoid circular dependency
        from .io.parquet import ParquetDatasetReader

        return ParquetDatasetReader(
            path_or_paths,
            features=features,
            cache_dir=cache_dir,
            keep_in_memory=keep_in_memory,
            columns=columns,
            **kwargs,
        ).read()

    @staticmethod
    def from_text(
        path_or_paths: Dict[str, PathLike],
        features: Optional[Features] = None,
        cache_dir: str = None,
        keep_in_memory: bool = False,
        **kwargs,
    ) -> "DatasetDict":
        """Create DatasetDict from text file(s).

        Args:
            path_or_paths (dict of path-like): Path(s) of the text file(s).
            features (:class:`Features`, optional): Dataset features.
            cache_dir (str, optional, default="~/.cache/huggingface/datasets"): Directory to cache data.
            keep_in_memory (bool, default=False): Whether to copy the data in-memory.
            **kwargs: Keyword arguments to be passed to :class:`TextConfig`.

        Returns:
            :class:`DatasetDict`
        """
        # Dynamic import to avoid circular dependency
        from .io.text import TextDatasetReader

        return TextDatasetReader(
            path_or_paths, features=features, cache_dir=cache_dir, keep_in_memory=keep_in_memory, **kwargs
        ).read()

    @is_documented_by(Dataset.prepare_for_task)
    def prepare_for_task(self, task: Union[str, TaskTemplate], id: int = 0) -> "DatasetDict":
        self._check_values_type()
        return DatasetDict({k: dataset.prepare_for_task(task=task, id=id) for k, dataset in self.items()})

    @is_documented_by(Dataset.align_labels_with_mapping)
    def align_labels_with_mapping(self, label2id: Dict, label_column: str) -> "DatasetDict":
        self._check_values_type()
        return DatasetDict(
            {
                k: dataset.align_labels_with_mapping(label2id=label2id, label_column=label_column)
                for k, dataset in self.items()
            }
        )

    def push_to_hub(
        self,
        repo_id,
        private: Optional[bool] = False,
        token: Optional[str] = None,
        branch: Optional[None] = None,
        shard_size: Optional[int] = 500 << 20,
    ):
        """Pushes the ``DatasetDict`` to the hub.
        The ``DatasetDict`` is pushed using HTTP requests and does not need to have neither git or git-lfs installed.

        Each dataset split will be pushed independently. The pushed dataset will keep the original split names.

        Args:
            repo_id (:obj:`str`):
                The ID of the repository to push to in the following format: `<user>/<dataset_name>` or
                `<org>/<dataset_name>`. Also accepts `<dataset_name>`, which will default to the namespace
                of the logged-in user.
            private (Optional :obj:`bool`):
                Whether the dataset repository should be set to private or not. Only affects repository creation:
                a repository that already exists will not be affected by that parameter.
            token (Optional :obj:`str`):
                An optional authentication token for the Hugging Face Hub. If no token is passed, will default
                to the token saved locally when logging in with ``huggingface-cli login``. Will raise an error
                if no token is passed and the user is not logged-in.
            branch (Optional :obj:`str`):
                The git branch on which to push the dataset.
            shard_size (Optional :obj:`int`):
                The size of the dataset shards to be uploaded to the hub. The dataset will be pushed in files
                of the size specified here, in bytes.

        Example:
            .. code-block:: python

                >>> dataset_dict.push_to_hub("<organization>/<dataset_id>")
        """
        self._check_values_type()
        total_uploaded_size = 0
        total_dataset_nbytes = 0
        info_to_dump: DatasetInfo = next(iter(self.values())).info.copy()
        dataset_name = repo_id.split("/")[-1]
        info_to_dump.splits = SplitDict(dataset_name=dataset_name)
        for split in self.keys():
            logger.warning(f"Pushing split {split} to the Hub.")
            # The split=key needs to be removed before merging
            repo_id, split, uploaded_size, dataset_nbytes = self[split]._push_parquet_shards_to_hub(
                repo_id, split=split, private=private, token=token, branch=branch, shard_size=shard_size
            )
            total_uploaded_size += uploaded_size
            total_dataset_nbytes += dataset_nbytes
            info_to_dump.splits[split] = SplitInfo(
                str(split), num_bytes=dataset_nbytes, num_examples=len(self[split]), dataset_name=dataset_name
            )
        organization, dataset_name = repo_id.split("/")
        info_to_dump.download_checksums = None
        info_to_dump.download_size = total_uploaded_size
        info_to_dump.dataset_size = total_dataset_nbytes
        info_to_dump.size_in_bytes = total_uploaded_size + total_dataset_nbytes
        buffer = BytesIO()
        buffer.write(f'{{"{organization}--{dataset_name}": '.encode())
        info_to_dump._dump_info(buffer)
        buffer.write(b"}")
        HfApi(endpoint=config.HF_ENDPOINT).upload_file(
            path_or_fileobj=buffer.getvalue(),
            path_in_repo=config.DATASETDICT_INFOS_FILENAME,
            repo_id=repo_id,
            token=token,
            repo_type="dataset",
            revision=branch,
            identical_ok=True,
        )


class IterableDatasetDict(dict):
    pass
