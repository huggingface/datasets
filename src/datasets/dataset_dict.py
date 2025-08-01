import contextlib
import copy
import fnmatch
import itertools
import json
import math
import posixpath
import random
import re
import time
from collections.abc import Sequence
from functools import partial
from pathlib import Path
from typing import Callable, Optional, Union

import fsspec
import numpy as np
from fsspec.core import url_to_fs
from huggingface_hub import (
    CommitInfo,
    CommitOperationAdd,
    CommitOperationDelete,
    DatasetCard,
    DatasetCardData,
    HfApi,
)
from huggingface_hub.hf_api import RepoFile
from huggingface_hub.utils import HfHubHTTPError, RepositoryNotFoundError
from requests import HTTPError

from . import config
from .arrow_dataset import (
    PUSH_TO_HUB_WITHOUT_METADATA_CONFIGS_SPLIT_PATTERN_SHARDED,
    Dataset,
)
from .features import Features
from .features.features import FeatureType
from .info import DatasetInfo, DatasetInfosDict
from .iterable_dataset import IterableDataset
from .naming import _split_re
from .splits import NamedSplit, Split, SplitDict, SplitInfo
from .table import Table
from .utils import logging
from .utils.doc_utils import is_documented_by
from .utils.metadata import MetadataConfigs
from .utils.py_utils import asdict, glob_pattern_to_regex, string_to_dict
from .utils.typing import PathLike


logger = logging.get_logger(__name__)


class bind(partial):
    def __call__(self, *fn_args, **fn_kwargs):
        return self.func(*fn_args, *self.args, **fn_kwargs)


class DatasetDict(dict[Union[str, NamedSplit], "Dataset"]):
    """A dictionary (dict of str: datasets.Dataset) with dataset transforms methods (map, filter, etc.)"""

    def _check_values_type(self):
        for dataset in self.values():
            if not isinstance(dataset, Dataset):
                raise TypeError(f"Values in `DatasetDict` should be of type `Dataset` but got type '{type(dataset)}'")

    def _check_values_features(self):
        items = list(self.items())
        for item_a, item_b in zip(items[:-1], items[1:]):
            if item_a[1].features != item_b[1].features:
                raise ValueError(
                    f"All datasets in `DatasetDict` should have the same features but features for '{item_a[0]}' and '{item_b[0]}' don't match: {item_a[1].features} != {item_b[1].features}"
                )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Here `del` is used to del the pyarrow tables. This properly closes the files used for memory mapped tables
        for dataset in self.values():
            if hasattr(dataset, "_data"):
                del dataset._data
            if hasattr(dataset, "_indices"):
                del dataset._indices

    def __getitem__(self, k) -> Dataset:
        if isinstance(k, (str, NamedSplit)) or len(self) == 0:
            return super().__getitem__(k)
        else:
            available_suggested_splits = [
                split for split in (Split.TRAIN, Split.TEST, Split.VALIDATION) if split in self
            ]
            suggested_split = available_suggested_splits[0] if available_suggested_splits else list(self)[0]
            raise KeyError(
                f"Invalid key: {k}. Please first select a split. For example: "
                f"`my_dataset_dictionary['{suggested_split}'][{k}]`. "
                f"Available splits: {sorted(self)}"
            )

    @property
    def data(self) -> dict[str, Table]:
        """The Apache Arrow tables backing each split.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> ds.data
        ```
        """
        self._check_values_type()
        return {k: dataset.data for k, dataset in self.items()}

    @property
    def cache_files(self) -> dict[str, dict]:
        """The cache files containing the Apache Arrow table backing each split.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> ds.cache_files
        {'test': [{'filename': '/root/.cache/huggingface/datasets/rotten_tomatoes_movie_review/default/1.0.0/40d411e45a6ce3484deed7cc15b82a53dad9a72aafd9f86f8f227134bec5ca46/rotten_tomatoes_movie_review-test.arrow'}],
         'train': [{'filename': '/root/.cache/huggingface/datasets/rotten_tomatoes_movie_review/default/1.0.0/40d411e45a6ce3484deed7cc15b82a53dad9a72aafd9f86f8f227134bec5ca46/rotten_tomatoes_movie_review-train.arrow'}],
         'validation': [{'filename': '/root/.cache/huggingface/datasets/rotten_tomatoes_movie_review/default/1.0.0/40d411e45a6ce3484deed7cc15b82a53dad9a72aafd9f86f8f227134bec5ca46/rotten_tomatoes_movie_review-validation.arrow'}]}
        ```
        """
        self._check_values_type()
        return {k: dataset.cache_files for k, dataset in self.items()}

    @property
    def num_columns(self) -> dict[str, int]:
        """Number of columns in each split of the dataset.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> ds.num_columns
        {'test': 2, 'train': 2, 'validation': 2}
        ```
        """
        self._check_values_type()
        return {k: dataset.num_columns for k, dataset in self.items()}

    @property
    def num_rows(self) -> dict[str, int]:
        """Number of rows in each split of the dataset.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> ds.num_rows
        {'test': 1066, 'train': 8530, 'validation': 1066}
        ```
        """
        self._check_values_type()
        return {k: dataset.num_rows for k, dataset in self.items()}

    @property
    def column_names(self) -> dict[str, list[str]]:
        """Names of the columns in each split of the dataset.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> ds.column_names
        {'test': ['text', 'label'],
         'train': ['text', 'label'],
         'validation': ['text', 'label']}
        ```
        """
        self._check_values_type()
        return {k: dataset.column_names for k, dataset in self.items()}

    @property
    def shape(self) -> dict[str, tuple[int]]:
        """Shape of each split of the dataset (number of rows, number of columns).

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> ds.shape
        {'test': (1066, 2), 'train': (8530, 2), 'validation': (1066, 2)}
        ```
        """
        self._check_values_type()
        return {k: dataset.shape for k, dataset in self.items()}

    def flatten(self, max_depth=16) -> "DatasetDict":
        """Flatten the Apache Arrow Table of each split (nested features are flatten).
        Each column with a struct type is flattened into one column per struct field.
        Other columns are left unchanged.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("rajpurkar/squad")
        >>> ds["train"].features
        {'id': Value('string'),
         'title': Value('string'),
         'context': Value('string'),
         'question': Value('string'),
         'answers.text': List(Value('string')),
         'answers.answer_start': List(Value('int32'))}
        >>> ds.flatten()
        DatasetDict({
            train: Dataset({
                features: ['id', 'title', 'context', 'question', 'answers.text', 'answers.answer_start'],
                num_rows: 87599
            })
            validation: Dataset({
                features: ['id', 'title', 'context', 'question', 'answers.text', 'answers.answer_start'],
                num_rows: 10570
            })
        })
        ```
        """
        self._check_values_type()
        return DatasetDict({k: dataset.flatten(max_depth=max_depth) for k, dataset in self.items()})

    def unique(self, column: str) -> dict[str, list]:
        """Return a list of the unique elements in a column for each split.

        This is implemented in the low-level backend and as such, very fast.

        Args:
            column (`str`):
                column name (list all the column names with [`~datasets.DatasetDict.column_names`])

        Returns:
            Dict[`str`, `list`]: Dictionary of unique elements in the given column.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> ds.unique("label")
        {'test': [1, 0], 'train': [1, 0], 'validation': [1, 0]}
        ```
        """
        self._check_values_type()
        return {k: dataset.unique(column) for k, dataset in self.items()}

    def cleanup_cache_files(self) -> dict[str, int]:
        """Clean up all cache files in the dataset cache directory, excepted the currently used cache file if there is one.
        Be careful when running this command that no other process is currently using other cache files.

        Return:
            `Dict` with the number of removed files for each split

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> ds.cleanup_cache_files()
        {'test': 0, 'train': 0, 'validation': 0}
        ```
        """
        self._check_values_type()
        return {k: dataset.cleanup_cache_files() for k, dataset in self.items()}

    def __repr__(self):
        repr = "\n".join([f"{k}: {v}" for k, v in self.items()])
        repr = re.sub(r"^", " " * 4, repr, count=0, flags=re.M)
        return f"DatasetDict({{\n{repr}\n}})"

    def cast(self, features: Features) -> "DatasetDict":
        """
        Cast the dataset to a new set of features.
        The transformation is applied to all the datasets of the dataset dictionary.

        Args:
            features ([`Features`]):
                New features to cast the dataset to.
                The name and order of the fields in the features must match the current column names.
                The type of the data must also be convertible from one type to the other.
                For non-trivial conversion, e.g. `string` <-> `ClassLabel` you should use [`~DatasetDict.map`] to update the dataset.

        Example:

        ```py
        >>> from datasets import load_dataset, ClassLabel, Value
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> ds["train"].features
        {'label': ClassLabel(names=['neg', 'pos']),
         'text': Value('string')}
        >>> new_features = ds["train"].features.copy()
        >>> new_features['label'] = ClassLabel(names=['bad', 'good'])
        >>> new_features['text'] = Value('large_string')
        >>> ds = ds.cast(new_features)
        >>> ds["train"].features
        {'label': ClassLabel(names=['bad', 'good']),
         'text': Value('large_string')}
        ```
        """
        self._check_values_type()
        return DatasetDict({k: dataset.cast(features=features) for k, dataset in self.items()})

    def cast_column(self, column: str, feature) -> "DatasetDict":
        """Cast column to feature for decoding.

        Args:
            column (`str`):
                Column name.
            feature ([`Feature`]):
                Target feature.

        Returns:
            [`DatasetDict`]

        Example:

        ```py
        >>> from datasets import load_dataset, ClassLabel
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> ds["train"].features
        {'label': ClassLabel(names=['neg', 'pos']),
         'text': Value('string')}
        >>> ds = ds.cast_column('label', ClassLabel(names=['bad', 'good']))
        >>> ds["train"].features
        {'label': ClassLabel(names=['bad', 'good']),
         'text': Value('string')}
        ```
        """
        self._check_values_type()
        return DatasetDict({k: dataset.cast_column(column=column, feature=feature) for k, dataset in self.items()})

    def remove_columns(self, column_names: Union[str, list[str]]) -> "DatasetDict":
        """
        Remove one or several column(s) from each split in the dataset
        and the features associated to the column(s).

        The transformation is applied to all the splits of the dataset dictionary.

        You can also remove a column using [`~DatasetDict.map`] with `remove_columns` but the present method
        doesn't copy the data of the remaining columns and is thus faster.

        Args:
            column_names (`Union[str, list[str]]`):
                Name of the column(s) to remove.

        Returns:
            [`DatasetDict`]: A copy of the dataset object without the columns to remove.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> ds = ds.remove_columns("label")
        DatasetDict({
            train: Dataset({
                features: ['text'],
                num_rows: 8530
            })
            validation: Dataset({
                features: ['text'],
                num_rows: 1066
            })
            test: Dataset({
                features: ['text'],
                num_rows: 1066
            })
        })
        ```
        """
        self._check_values_type()
        return DatasetDict({k: dataset.remove_columns(column_names=column_names) for k, dataset in self.items()})

    def rename_column(self, original_column_name: str, new_column_name: str) -> "DatasetDict":
        """
        Rename a column in the dataset and move the features associated to the original column under the new column name.
        The transformation is applied to all the datasets of the dataset dictionary.

        You can also rename a column using [`~DatasetDict.map`] with `remove_columns` but the present method:
            - takes care of moving the original features under the new column name.
            - doesn't copy the data to a new dataset and is thus much faster.

        Args:
            original_column_name (`str`):
                Name of the column to rename.
            new_column_name (`str`):
                New name for the column.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> ds = ds.rename_column("label", "label_new")
        DatasetDict({
            train: Dataset({
                features: ['text', 'label_new'],
                num_rows: 8530
            })
            validation: Dataset({
                features: ['text', 'label_new'],
                num_rows: 1066
            })
            test: Dataset({
                features: ['text', 'label_new'],
                num_rows: 1066
            })
        })
        ```
        """
        self._check_values_type()
        return DatasetDict(
            {
                k: dataset.rename_column(
                    original_column_name=original_column_name,
                    new_column_name=new_column_name,
                )
                for k, dataset in self.items()
            }
        )

    def rename_columns(self, column_mapping: dict[str, str]) -> "DatasetDict":
        """
        Rename several columns in the dataset, and move the features associated to the original columns under
        the new column names.
        The transformation is applied to all the datasets of the dataset dictionary.

        Args:
            column_mapping (`Dict[str, str]`):
                A mapping of columns to rename to their new names.

        Returns:
            [`DatasetDict`]: A copy of the dataset with renamed columns.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> ds.rename_columns({'text': 'text_new', 'label': 'label_new'})
        DatasetDict({
            train: Dataset({
                features: ['text_new', 'label_new'],
                num_rows: 8530
            })
            validation: Dataset({
                features: ['text_new', 'label_new'],
                num_rows: 1066
            })
            test: Dataset({
                features: ['text_new', 'label_new'],
                num_rows: 1066
            })
        })
        ```
        """
        self._check_values_type()
        return DatasetDict({k: dataset.rename_columns(column_mapping=column_mapping) for k, dataset in self.items()})

    def select_columns(self, column_names: Union[str, list[str]]) -> "DatasetDict":
        """Select one or several column(s) from each split in the dataset and
        the features associated to the column(s).

        The transformation is applied to all the splits of the dataset
        dictionary.

        Args:
            column_names (`Union[str, list[str]]`):
                Name of the column(s) to keep.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> ds.select_columns("text")
        DatasetDict({
            train: Dataset({
                features: ['text'],
                num_rows: 8530
            })
            validation: Dataset({
                features: ['text'],
                num_rows: 1066
            })
            test: Dataset({
                features: ['text'],
                num_rows: 1066
            })
        })
        ```
        """
        self._check_values_type()
        return DatasetDict({k: dataset.select_columns(column_names=column_names) for k, dataset in self.items()})

    def class_encode_column(self, column: str, include_nulls: bool = False) -> "DatasetDict":
        """Casts the given column as [`~datasets.features.ClassLabel`] and updates the tables.

        Args:
            column (`str`):
                The name of the column to cast.
            include_nulls (`bool`, defaults to `False`):
                Whether to include null values in the class labels. If `True`, the null values will be encoded as the `"None"` class label.

                <Added version="1.14.2"/>

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("boolq")
        >>> ds["train"].features
        {'answer': Value('bool'),
         'passage': Value('string'),
         'question': Value('string')}
        >>> ds = ds.class_encode_column("answer")
        >>> ds["train"].features
        {'answer': ClassLabel(num_classes=2, names=['False', 'True']),
         'passage': Value('string'),
         'question': Value('string')}
        ```
        """
        self._check_values_type()
        return DatasetDict(
            {k: dataset.class_encode_column(column=column, include_nulls=include_nulls) for k, dataset in self.items()}
        )

    @contextlib.contextmanager
    def formatted_as(
        self,
        type: Optional[str] = None,
        columns: Optional[list] = None,
        output_all_columns: bool = False,
        **format_kwargs,
    ):
        """To be used in a `with` statement. Set `__getitem__` return format (type and columns).
        The transformation is applied to all the datasets of the dataset dictionary.

        Args:
            type (`str`, *optional*):
                Either output type selected in `[None, 'numpy', 'torch', 'tensorflow', 'jax', 'arrow', 'pandas', 'polars']`.
                `None` means `__getitem__` returns python objects (default).
            columns (`list[str]`, *optional*):
                Columns to format in the output.
                `None` means `__getitem__` returns all columns (default).
            output_all_columns (`bool`, defaults to False):
                Keep un-formatted columns as well in the output (as python objects).
            **format_kwargs (additional keyword arguments):
                Keywords arguments passed to the convert function like `np.array`, `torch.tensor` or `tensorflow.ragged.constant`.
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
                    old_format_type[k],
                    old_format_columns[k],
                    old_output_all_columns[k],
                    **old_format_kwargs[k],
                )

    def set_format(
        self,
        type: Optional[str] = None,
        columns: Optional[list] = None,
        output_all_columns: bool = False,
        **format_kwargs,
    ):
        """Set `__getitem__` return format (type and columns).
        The format is set for every dataset in the dataset dictionary.

        Args:
            type (`str`, *optional*):
                Either output type selected in `[None, 'numpy', 'torch', 'tensorflow', 'jax', 'arrow', 'pandas', 'polars']`.
                `None` means `__getitem__` returns python objects (default).
            columns (`list[str]`, *optional*):
                Columns to format in the output.
                `None` means `__getitem__` returns all columns (default).
            output_all_columns (`bool`, defaults to False):
                Keep un-formatted columns as well in the output (as python objects),
            **format_kwargs (additional keyword arguments):
                Keywords arguments passed to the convert function like `np.array`, `torch.tensor` or `tensorflow.ragged.constant`.

        It is possible to call `map` after calling `set_format`. Since `map` may add new columns, then the list of formatted columns
        gets updated. In this case, if you apply `map` on a dataset to add a new column, then this column will be formatted:

            `new formatted columns = (all columns - previously unformatted columns)`

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> from transformers import AutoTokenizer
        >>> tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        >>> ds = ds.map(lambda x: tokenizer(x["text"], truncation=True, padding=True), batched=True)
        >>> ds.set_format(type="numpy", columns=['input_ids', 'token_type_ids', 'attention_mask', 'label'])
        >>> ds["train"].format
        {'columns': ['input_ids', 'token_type_ids', 'attention_mask', 'label'],
         'format_kwargs': {},
         'output_all_columns': False,
         'type': 'numpy'}
        ```
        """
        self._check_values_type()
        for dataset in self.values():
            dataset.set_format(
                type=type,
                columns=columns,
                output_all_columns=output_all_columns,
                **format_kwargs,
            )

    def reset_format(self):
        """Reset `__getitem__` return format to python objects and all columns.
        The transformation is applied to all the datasets of the dataset dictionary.

        Same as `self.set_format()`

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> from transformers import AutoTokenizer
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        >>> ds = ds.map(lambda x: tokenizer(x["text"], truncation=True, padding=True), batched=True)
        >>> ds.set_format(type="numpy", columns=['input_ids', 'token_type_ids', 'attention_mask', 'label'])
        >>> ds["train"].format
        {'columns': ['input_ids', 'token_type_ids', 'attention_mask', 'label'],
         'format_kwargs': {},
         'output_all_columns': False,
         'type': 'numpy'}
        >>> ds.reset_format()
        >>> ds["train"].format
        {'columns': ['text', 'label', 'input_ids', 'token_type_ids', 'attention_mask'],
         'format_kwargs': {},
         'output_all_columns': False,
         'type': None}
        ```
        """
        self._check_values_type()
        for dataset in self.values():
            dataset.set_format()

    def set_transform(
        self,
        transform: Optional[Callable],
        columns: Optional[list] = None,
        output_all_columns: bool = False,
    ):
        """Set ``__getitem__`` return format using this transform. The transform is applied on-the-fly on batches when ``__getitem__`` is called.
        The transform is set for every dataset in the dataset dictionary
        As :func:`datasets.Dataset.set_format`, this can be reset using :func:`datasets.Dataset.reset_format`

        Args:
            transform (`Callable`, optional): user-defined formatting transform, replaces the format defined by :func:`datasets.Dataset.set_format`
                A formatting function is a callable that takes a batch (as a dict) as input and returns a batch.
                This function is applied right before returning the objects in ``__getitem__``.
            columns (`list[str]`, optional): columns to format in the output
                If specified, then the input batch of the transform only contains those columns.
            output_all_columns (`bool`, default to False): keep un-formatted columns as well in the output (as python objects)
                If set to True, then the other un-formatted columns are kept with the output of the transform.

        """
        self._check_values_type()
        for dataset in self.values():
            dataset.set_format(
                "custom",
                columns=columns,
                output_all_columns=output_all_columns,
                transform=transform,
            )

    def with_format(
        self,
        type: Optional[str] = None,
        columns: Optional[list] = None,
        output_all_columns: bool = False,
        **format_kwargs,
    ) -> "DatasetDict":
        """Set `__getitem__` return format (type and columns). The data formatting is applied on-the-fly.
        The format `type` (for example "numpy") is used to format batches when using `__getitem__`.
        The format is set for every dataset in the dataset dictionary.

        It's also possible to use custom transforms for formatting using [`~datasets.Dataset.with_transform`].

        Contrary to [`~datasets.DatasetDict.set_format`], `with_format` returns a new [`DatasetDict`] object with new [`Dataset`] objects.

        Args:
            type (`str`, *optional*):
                Either output type selected in `[None, 'numpy', 'torch', 'tensorflow', 'jax', 'arrow', 'pandas', 'polars']`.
                `None` means `__getitem__` returns python objects (default).
            columns (`list[str]`, *optional*):
                Columns to format in the output.
                `None` means `__getitem__` returns all columns (default).
            output_all_columns (`bool`, defaults to `False`):
                Keep un-formatted columns as well in the output (as python objects).
            **format_kwargs (additional keyword arguments):
                Keywords arguments passed to the convert function like `np.array`, `torch.tensor` or `tensorflow.ragged.constant`.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> from transformers import AutoTokenizer
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        >>> ds = ds.map(lambda x: tokenizer(x['text'], truncation=True, padding=True), batched=True)
        >>> ds["train"].format
        {'columns': ['text', 'label', 'input_ids', 'token_type_ids', 'attention_mask'],
         'format_kwargs': {},
         'output_all_columns': False,
         'type': None}
        >>> ds = ds.with_format("torch")
        >>> ds["train"].format
        {'columns': ['text', 'label', 'input_ids', 'token_type_ids', 'attention_mask'],
         'format_kwargs': {},
         'output_all_columns': False,
         'type': 'torch'}
        >>> ds["train"][0]
        {'text': 'compassionately explores the seemingly irreconcilable situation between conservative christian parents and their estranged gay and lesbian children .',
         'label': tensor(1),
         'input_ids': tensor([  101, 18027, 16310, 16001,  1103,  9321,   178, 11604,  7235,  6617,
                1742,  2165,  2820,  1206,  6588, 22572, 12937,  1811,  2153,  1105,
                1147, 12890, 19587,  6463,  1105, 15026,  1482,   119,   102,     0,
                    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                    0,     0,     0,     0]),
         'token_type_ids': tensor([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
         'attention_mask': tensor([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])}
        ```
        """
        dataset = copy.deepcopy(self)
        dataset.set_format(
            type=type,
            columns=columns,
            output_all_columns=output_all_columns,
            **format_kwargs,
        )
        return dataset

    def with_transform(
        self,
        transform: Optional[Callable],
        columns: Optional[list] = None,
        output_all_columns: bool = False,
    ) -> "DatasetDict":
        """Set `__getitem__` return format using this transform. The transform is applied on-the-fly on batches when `__getitem__` is called.
        The transform is set for every dataset in the dataset dictionary

        As [`~datasets.Dataset.set_format`], this can be reset using [`~datasets.Dataset.reset_format`].

        Contrary to [`~datasets.DatasetDict.set_transform`], `with_transform` returns a new [`DatasetDict`] object with new [`Dataset`] objects.

        Args:
            transform (`Callable`, *optional*):
                User-defined formatting transform, replaces the format defined by [`~datasets.Dataset.set_format`].
                A formatting function is a callable that takes a batch (as a dict) as input and returns a batch.
                This function is applied right before returning the objects in `__getitem__`.
            columns (`list[str]`, *optional*):
                Columns to format in the output.
                If specified, then the input batch of the transform only contains those columns.
            output_all_columns (`bool`, defaults to False):
                Keep un-formatted columns as well in the output (as python objects).
                If set to `True`, then the other un-formatted columns are kept with the output of the transform.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> from transformers import AutoTokenizer
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        >>> def encode(example):
        ...     return tokenizer(example['text'], truncation=True, padding=True, return_tensors="pt")
        >>> ds = ds.with_transform(encode)
        >>> ds["train"][0]
        {'attention_mask': tensor([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         1, 1, 1, 1, 1, 1, 1, 1, 1]),
         'input_ids': tensor([  101,  1103,  2067,  1110, 17348,  1106,  1129,  1103,  6880,  1432,
                112,   188,  1207,   107, 14255,  1389,   107,  1105,  1115,  1119,
                112,   188,  1280,  1106,  1294,   170, 24194,  1256,  3407,  1190,
                170, 11791,  5253,   188,  1732,  7200, 10947, 12606,  2895,   117,
                179,  7766,   118,   172, 15554,  1181,  3498,  6961,  3263,  1137,
                188,  1566,  7912, 14516,  6997,   119,   102]),
         'token_type_ids': tensor([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0])}
        ```
        """
        dataset = copy.deepcopy(self)
        dataset.set_transform(transform=transform, columns=columns, output_all_columns=output_all_columns)
        return dataset

    def map(
        self,
        function: Optional[Callable] = None,
        with_indices: bool = False,
        with_rank: bool = False,
        with_split: bool = False,
        input_columns: Optional[Union[str, list[str]]] = None,
        batched: bool = False,
        batch_size: Optional[int] = 1000,
        drop_last_batch: bool = False,
        remove_columns: Optional[Union[str, list[str]]] = None,
        keep_in_memory: bool = False,
        load_from_cache_file: Optional[bool] = None,
        cache_file_names: Optional[dict[str, Optional[str]]] = None,
        writer_batch_size: Optional[int] = 1000,
        features: Optional[Features] = None,
        disable_nullable: bool = False,
        fn_kwargs: Optional[dict] = None,
        num_proc: Optional[int] = None,
        desc: Optional[str] = None,
        try_original_type: Optional[bool] = True,
    ) -> "DatasetDict":
        """
        Apply a function to all the examples in the table (individually or in batches) and update the table.
        If your function returns a column that already exists, then it overwrites it.
        The transformation is applied to all the datasets of the dataset dictionary.

        You can specify whether the function should be batched or not with the `batched` parameter:

        - If batched is `False`, then the function takes 1 example in and should return 1 example.
          An example is a dictionary, e.g. `{"text": "Hello there !"}`.
        - If batched is `True` and `batch_size` is 1, then the function takes a batch of 1 example as input and can return a batch with 1 or more examples.
          A batch is a dictionary, e.g. a batch of 1 example is `{"text": ["Hello there !"]}`.
        - If batched is `True` and `batch_size` is `n > 1`, then the function takes a batch of `n` examples as input and can return a batch with `n` examples, or with an arbitrary number of examples.
          Note that the last batch may have less than `n` examples.
          A batch is a dictionary, e.g. a batch of `n` examples is `{"text": ["Hello there !"] * n}`.

        If the function is asynchronous, then `map` will run your function in parallel, with up to one thousand simultaneous calls.
        It is recommended to use a `asyncio.Semaphore` in your function if you want to set a maximum number of operations that can run at the same time.

        Args:
            function (`callable`): with one of the following signature:
                - `function(example: Dict[str, Any]) -> Dict[str, Any]` if `batched=False` and `with_indices=False`
                - `function(example: Dict[str, Any], indices: int) -> Dict[str, Any]` if `batched=False` and `with_indices=True`
                - `function(batch: Dict[str, list]) -> Dict[str, list]` if `batched=True` and `with_indices=False`
                - `function(batch: Dict[str, list], indices: list[int]) -> Dict[str, list]` if `batched=True` and `with_indices=True`

                For advanced usage, the function can also return a `pyarrow.Table`.
                If the function is asynchronous, then `map` will run your function in parallel.
                Moreover if your function returns nothing (`None`), then `map` will run your function and return the dataset unchanged.
                If no function is provided, default to identity function: `lambda x: x`.
            with_indices (`bool`, defaults to `False`):
                Provide example indices to `function`. Note that in this case the signature of `function` should be `def function(example, idx): ...`.
            with_rank (`bool`, defaults to `False`):
                Provide process rank to `function`. Note that in this case the
                signature of `function` should be `def function(example[, idx], rank): ...`.
            with_split (`bool`, defaults to `False`):
                Provide process split to `function`. Note that in this case the
                signature of `function` should be `def function(example[, idx], split): ...`.
            input_columns (`[Union[str, list[str]]]`, *optional*, defaults to `None`):
                The columns to be passed into `function` as
                positional arguments. If `None`, a dict mapping to all formatted columns is passed as one argument.
            batched (`bool`, defaults to `False`):
                Provide batch of examples to `function`.
            batch_size (`int`, *optional*, defaults to `1000`):
                Number of examples per batch provided to `function` if `batched=True`,
                `batch_size <= 0` or `batch_size == None` then provide the full dataset as a single batch to `function`.
            drop_last_batch (`bool`, defaults to `False`):
                Whether a last batch smaller than the batch_size should be
                dropped instead of being processed by the function.
            remove_columns (`[Union[str, list[str]]]`, *optional*, defaults to `None`):
                Remove a selection of columns while doing the mapping.
                Columns will be removed before updating the examples with the output of `function`, i.e. if `function` is adding
                columns with names in `remove_columns`, these columns will be kept.
            keep_in_memory (`bool`, defaults to `False`):
                Keep the dataset in memory instead of writing it to a cache file.
            load_from_cache_file (`Optional[bool]`, defaults to `True` if caching is enabled):
                If a cache file storing the current computation from `function`
                can be identified, use it instead of recomputing.
            cache_file_names (`[Dict[str, str]]`, *optional*, defaults to `None`):
                Provide the name of a path for the cache file. It is used to store the
                results of the computation instead of the automatically generated cache file name.
                You have to provide one `cache_file_name` per dataset in the dataset dictionary.
            writer_batch_size (`int`, default `1000`):
                Number of rows per write operation for the cache file writer.
                This value is a good trade-off between memory usage during the processing, and processing speed.
                Higher value makes the processing do fewer lookups, lower value consume less temporary memory while running `map`.
            features (`[datasets.Features]`, *optional*, defaults to `None`):
                Use a specific [`Features`] to store the cache file
                instead of the automatically generated one.
            disable_nullable (`bool`, defaults to `False`):
                Disallow null values in the table.
            fn_kwargs (`Dict`, *optional*, defaults to `None`):
                Keyword arguments to be passed to `function`
            num_proc (`int`, *optional*, defaults to `None`):
                 The number of processes to use for multiprocessing.
                - If `None` or `0`, no multiprocessing is used and the operation runs in the main process.
                - If greater than `1`, one or multiple worker processes are used to process data in parallel.
                 Note: The function passed to `map()` must be picklable for multiprocessing to work correctly
                 (i.e., prefer functions defined at the top level of a module, not inside another function or class).
            desc (`str`, *optional*, defaults to `None`):
                Meaningful description to be displayed alongside with the progress bar while mapping examples.
            try_original_type (`Optional[bool]`, defaults to `True`):
                Try to keep the types of the original columns (e.g. int32 -> int32).
                Set to False if you want to always infer new types.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> def add_prefix(example):
        ...     example["text"] = "Review: " + example["text"]
        ...     return example
        >>> ds = ds.map(add_prefix)
        >>> ds["train"][0:3]["text"]
        ['Review: the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .',
         'Review: the gorgeously elaborate continuation of " the lord of the rings " trilogy is so huge that a column of words cannot adequately describe co-writer/director peter jackson\'s expanded vision of j . r . r . tolkien\'s middle-earth .',
         'Review: effective but too-tepid biopic']

        # process a batch of examples
        >>> ds = ds.map(lambda example: tokenizer(example["text"]), batched=True)
        # set number of processors
        >>> ds = ds.map(add_prefix, num_proc=4)
        ```
        """
        self._check_values_type()
        if cache_file_names is None:
            cache_file_names = dict.fromkeys(self)

        dataset_dict = {}
        for split, dataset in self.items():
            if with_split:
                function = bind(function, split)

            dataset_dict[split] = dataset.map(
                function=function,
                with_indices=with_indices,
                with_rank=with_rank,
                input_columns=input_columns,
                batched=batched,
                batch_size=batch_size,
                drop_last_batch=drop_last_batch,
                remove_columns=remove_columns,
                keep_in_memory=keep_in_memory,
                load_from_cache_file=load_from_cache_file,
                cache_file_name=cache_file_names[split],
                writer_batch_size=writer_batch_size,
                features=features,
                disable_nullable=disable_nullable,
                fn_kwargs=fn_kwargs,
                num_proc=num_proc,
                desc=desc,
                try_original_type=try_original_type,
            )

            if with_split:
                function = function.func

        return DatasetDict(dataset_dict)

    def filter(
        self,
        function: Optional[Callable] = None,
        with_indices: bool = False,
        with_rank: bool = False,
        input_columns: Optional[Union[str, list[str]]] = None,
        batched: bool = False,
        batch_size: Optional[int] = 1000,
        keep_in_memory: bool = False,
        load_from_cache_file: Optional[bool] = None,
        cache_file_names: Optional[dict[str, Optional[str]]] = None,
        writer_batch_size: Optional[int] = 1000,
        fn_kwargs: Optional[dict] = None,
        num_proc: Optional[int] = None,
        desc: Optional[str] = None,
    ) -> "DatasetDict":
        """Apply a filter function to all the elements in the table in batches
        and update the table so that the dataset only includes examples according to the filter function.
        The transformation is applied to all the datasets of the dataset dictionary.

        Args:
            function (`Callable`): Callable with one of the following signatures:

                - `function(example: Dict[str, Any]) -> bool` if `batched=False` and `with_indices=False` and `with_rank=False`
                - `function(example: Dict[str, Any], *extra_args) -> bool` if `batched=False` and `with_indices=True` and/or `with_rank=True` (one extra arg for each)
                - `function(batch: Dict[str, list]) -> list[bool]` if `batched=True` and `with_indices=False` and `with_rank=False`
                - `function(batch: Dict[str, list], *extra_args) -> list[bool]` if `batched=True` and `with_indices=True` and/or `with_rank=True` (one extra arg for each)

                If no function is provided, defaults to an always `True` function: `lambda x: True`.
            with_indices (`bool`, defaults to `False`):
                Provide example indices to `function`. Note that in this case the
                signature of `function` should be `def function(example, idx[, rank]): ...`.
            with_rank (`bool`, defaults to `False`):
                Provide process rank to `function`. Note that in this case the
                signature of `function` should be `def function(example[, idx], rank): ...`.
            input_columns (`[Union[str, list[str]]]`, *optional*, defaults to `None`):
                The columns to be passed into `function` as
                positional arguments. If `None`, a dict mapping to all formatted columns is passed as one argument.
            batched (`bool`, defaults to `False`):
                Provide batch of examples to `function`.
            batch_size (`int`, *optional*, defaults to `1000`):
                Number of examples per batch provided to `function` if `batched=True`
                `batch_size <= 0` or `batch_size == None` then provide the full dataset as a single batch to `function`.
            keep_in_memory (`bool`, defaults to `False`):
                Keep the dataset in memory instead of writing it to a cache file.
            load_from_cache_file (`Optional[bool]`, defaults to `True` if caching is enabled):
                If a cache file storing the current computation from `function`
                can be identified, use it instead of recomputing.
            cache_file_names (`[Dict[str, str]]`, *optional*, defaults to `None`):
                Provide the name of a path for the cache file. It is used to store the
                results of the computation instead of the automatically generated cache file name.
                You have to provide one `cache_file_name` per dataset in the dataset dictionary.
            writer_batch_size (`int`, defaults to `1000`):
                Number of rows per write operation for the cache file writer.
                This value is a good trade-off between memory usage during the processing, and processing speed.
                Higher value makes the processing do fewer lookups, lower value consume less temporary memory while running `map`.
            fn_kwargs (`Dict`, *optional*, defaults to `None`):
                Keyword arguments to be passed to `function`
            num_proc (`int`, *optional*, defaults to `None`):
                 The number of processes to use for multiprocessing.
                - If `None` or `0`, no multiprocessing is used and the operation runs in the main process.
                - If greater than `1`, one or multiple worker processes are used to process data in parallel.
                 Note: The function passed to `map()` must be picklable for multiprocessing to work correctly
                 (i.e., prefer functions defined at the top level of a module, not inside another function or class).
            desc (`str`, *optional*, defaults to `None`):
                Meaningful description to be displayed alongside with the progress bar while filtering examples.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> ds.filter(lambda x: x["label"] == 1)
        DatasetDict({
            train: Dataset({
                features: ['text', 'label'],
                num_rows: 4265
            })
            validation: Dataset({
                features: ['text', 'label'],
                num_rows: 533
            })
            test: Dataset({
                features: ['text', 'label'],
                num_rows: 533
            })
        })
        ```
        """
        self._check_values_type()
        if cache_file_names is None:
            cache_file_names = dict.fromkeys(self)
        return DatasetDict(
            {
                k: dataset.filter(
                    function=function,
                    with_indices=with_indices,
                    with_rank=with_rank,
                    input_columns=input_columns,
                    batched=batched,
                    batch_size=batch_size,
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

    def flatten_indices(
        self,
        keep_in_memory: bool = False,
        cache_file_names: Optional[dict[str, Optional[str]]] = None,
        writer_batch_size: Optional[int] = 1000,
        features: Optional[Features] = None,
        disable_nullable: bool = False,
        num_proc: Optional[int] = None,
        new_fingerprint: Optional[str] = None,
    ) -> "DatasetDict":
        """Create and cache a new Dataset by flattening the indices mapping.

        Args:
            keep_in_memory (`bool`, defaults to `False`):
                Keep the dataset in memory instead of writing it to a cache file.
            cache_file_names (`Dict[str, str]`, *optional*, default `None`):
                Provide the name of a path for the cache file. It is used to store the
                results of the computation instead of the automatically generated cache file name.
                You have to provide one `cache_file_name` per dataset in the dataset dictionary.
            writer_batch_size (`int`, defaults to `1000`):
                Number of rows per write operation for the cache file writer.
                This value is a good trade-off between memory usage during the processing, and processing speed.
                Higher value makes the processing do fewer lookups, lower value consume less temporary memory while running `map`.
            features (`Optional[datasets.Features]`, defaults to `None`):
                Use a specific [`Features`] to store the cache file
                instead of the automatically generated one.
            disable_nullable (`bool`, defaults to `False`):
                Allow null values in the table.
            num_proc (`int`, optional, default `None`):
                Max number of processes when generating cache. Already cached shards are loaded sequentially
            new_fingerprint (`str`, *optional*, defaults to `None`):
                The new fingerprint of the dataset after transform.
                If `None`, the new fingerprint is computed using a hash of the previous fingerprint, and the transform arguments
        """
        self._check_values_type()
        if cache_file_names is None:
            cache_file_names = dict.fromkeys(self)
        return DatasetDict(
            {
                k: dataset.flatten_indices(
                    keep_in_memory=keep_in_memory,
                    cache_file_name=cache_file_names[k],
                    writer_batch_size=writer_batch_size,
                    features=features,
                    disable_nullable=disable_nullable,
                    num_proc=num_proc,
                    new_fingerprint=new_fingerprint,
                )
                for k, dataset in self.items()
            }
        )

    def sort(
        self,
        column_names: Union[str, Sequence[str]],
        reverse: Union[bool, Sequence[bool]] = False,
        null_placement: str = "at_end",
        keep_in_memory: bool = False,
        load_from_cache_file: Optional[bool] = None,
        indices_cache_file_names: Optional[dict[str, Optional[str]]] = None,
        writer_batch_size: Optional[int] = 1000,
    ) -> "DatasetDict":
        """Create a new dataset sorted according to a single or multiple columns.

        Args:
            column_names (`Union[str, Sequence[str]]`):
                Column name(s) to sort by.
            reverse (`Union[bool, Sequence[bool]]`, defaults to `False`):
                If `True`, sort by descending order rather than ascending. If a single bool is provided,
                the value is applied to the sorting of all column names. Otherwise a list of bools with the
                same length and order as column_names must be provided.
            null_placement (`str`, defaults to `at_end`):
                Put `None` values at the beginning if `at_start` or `first` or at the end if `at_end` or `last`
            keep_in_memory (`bool`, defaults to `False`):
                Keep the sorted indices in memory instead of writing it to a cache file.
            load_from_cache_file (`Optional[bool]`, defaults to `True` if caching is enabled):
                If a cache file storing the sorted indices
                can be identified, use it instead of recomputing.
            indices_cache_file_names (`[Dict[str, str]]`, *optional*, defaults to `None`):
                Provide the name of a path for the cache file. It is used to store the
                indices mapping instead of the automatically generated cache file name.
                You have to provide one `cache_file_name` per dataset in the dataset dictionary.
            writer_batch_size (`int`, defaults to `1000`):
                Number of rows per write operation for the cache file writer.
                Higher value gives smaller cache files, lower value consume less temporary memory.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset('cornell-movie-review-data/rotten_tomatoes')
        >>> ds['train']['label'][:10]
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        >>> sorted_ds = ds.sort('label')
        >>> sorted_ds['train']['label'][:10]
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        >>> another_sorted_ds = ds.sort(['label', 'text'], reverse=[True, False])
        >>> another_sorted_ds['train']['label'][:10]
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ```
        """
        self._check_values_type()
        if indices_cache_file_names is None:
            indices_cache_file_names = dict.fromkeys(self)
        return DatasetDict(
            {
                k: dataset.sort(
                    column_names=column_names,
                    reverse=reverse,
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
        seeds: Optional[Union[int, dict[str, Optional[int]]]] = None,
        seed: Optional[int] = None,
        generators: Optional[dict[str, np.random.Generator]] = None,
        keep_in_memory: bool = False,
        load_from_cache_file: Optional[bool] = None,
        indices_cache_file_names: Optional[dict[str, Optional[str]]] = None,
        writer_batch_size: Optional[int] = 1000,
    ) -> "DatasetDict":
        """Create a new Dataset where the rows are shuffled.

        The transformation is applied to all the datasets of the dataset dictionary.

        Currently shuffling uses numpy random generators.
        You can either supply a NumPy BitGenerator to use, or a seed to initiate NumPy's default random generator (PCG64).

        Args:
            seeds (`Dict[str, int]` or `int`, *optional*):
                A seed to initialize the default BitGenerator if `generator=None`.
                If `None`, then fresh, unpredictable entropy will be pulled from the OS.
                If an `int` or `array_like[ints]` is passed, then it will be passed to SeedSequence to derive the initial BitGenerator state.
                You can provide one `seed` per dataset in the dataset dictionary.
            seed (`int`, *optional*):
                A seed to initialize the default BitGenerator if `generator=None`. Alias for seeds (a `ValueError` is raised if both are provided).
            generators (`Dict[str, *optional*, np.random.Generator]`):
                Numpy random Generator to use to compute the permutation of the dataset rows.
                If `generator=None` (default), uses `np.random.default_rng` (the default BitGenerator (PCG64) of NumPy).
                You have to provide one `generator` per dataset in the dataset dictionary.
            keep_in_memory (`bool`, defaults to `False`):
                Keep the dataset in memory instead of writing it to a cache file.
            load_from_cache_file (`Optional[bool]`, defaults to `True` if caching is enabled):
                If a cache file storing the current computation from `function`
                can be identified, use it instead of recomputing.
            indices_cache_file_names (`Dict[str, str]`, *optional*):
                Provide the name of a path for the cache file. It is used to store the
                indices mappings instead of the automatically generated cache file name.
                You have to provide one `cache_file_name` per dataset in the dataset dictionary.
            writer_batch_size (`int`, defaults to `1000`):
                Number of rows per write operation for the cache file writer.
                This value is a good trade-off between memory usage during the processing, and processing speed.
                Higher value makes the processing do fewer lookups, lower value consume less temporary memory while running `map`.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> ds["train"]["label"][:10]
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        # set a seed
        >>> shuffled_ds = ds.shuffle(seed=42)
        >>> shuffled_ds["train"]["label"][:10]
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 0]
        ```
        """
        self._check_values_type()
        if seed is not None and seeds is not None:
            raise ValueError("Please specify seed or seeds, but not both")
        seeds = seed if seed is not None else seeds
        if seeds is None:
            seeds = dict.fromkeys(self)
        elif not isinstance(seeds, dict):
            seeds = dict.fromkeys(self, seeds)
        if generators is None:
            generators = dict.fromkeys(self)
        if indices_cache_file_names is None:
            indices_cache_file_names = dict.fromkeys(self)
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

    def save_to_disk(
        self,
        dataset_dict_path: PathLike,
        max_shard_size: Optional[Union[str, int]] = None,
        num_shards: Optional[dict[str, int]] = None,
        num_proc: Optional[int] = None,
        storage_options: Optional[dict] = None,
    ):
        """
        Saves a dataset dict to a filesystem using `fsspec.spec.AbstractFileSystem`.

        For [`Image`], [`Audio`] and [`Video`] data:

        All the Image(), Audio() and Video() data are stored in the arrow files.
        If you want to store paths or urls, please use the Value("string") type.

        Args:
            dataset_dict_path (`path-like`):
                Path (e.g. `dataset/train`) or remote URI (e.g. `s3://my-bucket/dataset/train`)
                of the dataset dict directory where the dataset dict will be saved to.
            max_shard_size (`int` or `str`, *optional*, defaults to `"500MB"`):
                The maximum size of the dataset shards to be saved to the filesystem. If expressed as a string, needs to be digits followed by a unit
                (like `"50MB"`).
            num_shards (`Dict[str, int]`, *optional*):
                Number of shards to write. By default the number of shards depends on `max_shard_size` and `num_proc`.
                You need to provide the number of shards for each dataset in the dataset dictionary.
                Use a dictionary to define a different num_shards for each split.

                <Added version="2.8.0"/>
            num_proc (`int`, *optional*, default `None`):
                Number of processes when downloading and generating the dataset locally.
                Multiprocessing is disabled by default.

                <Added version="2.8.0"/>
            storage_options (`dict`, *optional*):
                Key/value pairs to be passed on to the file-system backend, if any.

                <Added version="2.8.0"/>

        Example:

        ```python
        >>> dataset_dict.save_to_disk("path/to/dataset/directory")
        >>> dataset_dict.save_to_disk("path/to/dataset/directory", max_shard_size="1GB")
        >>> dataset_dict.save_to_disk("path/to/dataset/directory", num_shards={"train": 1024, "test": 8})
        ```
        """
        fs: fsspec.AbstractFileSystem
        fs, _ = url_to_fs(dataset_dict_path, **(storage_options or {}))

        if num_shards is None:
            num_shards = dict.fromkeys(self)
        elif not isinstance(num_shards, dict):
            raise ValueError(
                "Please provide one `num_shards` per dataset in the dataset dictionary, e.g. {{'train': 128, 'test': 4}}"
            )

        fs.makedirs(dataset_dict_path, exist_ok=True)

        with fs.open(
            posixpath.join(dataset_dict_path, config.DATASETDICT_JSON_FILENAME),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump({"splits": list(self)}, f)
        for k, dataset in self.items():
            dataset.save_to_disk(
                posixpath.join(dataset_dict_path, k),
                num_shards=num_shards.get(k),
                max_shard_size=max_shard_size,
                num_proc=num_proc,
                storage_options=storage_options,
            )

    @staticmethod
    def load_from_disk(
        dataset_dict_path: PathLike,
        keep_in_memory: Optional[bool] = None,
        storage_options: Optional[dict] = None,
    ) -> "DatasetDict":
        """
        Load a dataset that was previously saved using [`save_to_disk`] from a filesystem using `fsspec.spec.AbstractFileSystem`.

        Args:
            dataset_dict_path (`path-like`):
                Path (e.g. `"dataset/train"`) or remote URI (e.g. `"s3//my-bucket/dataset/train"`)
                of the dataset dict directory where the dataset dict will be loaded from.
            keep_in_memory (`bool`, defaults to `None`):
                Whether to copy the dataset in-memory. If `None`, the
                dataset will not be copied in-memory unless explicitly enabled by setting
                `datasets.config.IN_MEMORY_MAX_SIZE` to nonzero. See more details in the
                [improve performance](../cache#improve-performance) section.
            storage_options (`dict`, *optional*):
                Key/value pairs to be passed on to the file-system backend, if any.

                <Added version="2.8.0"/>

        Returns:
            [`DatasetDict`]

        Example:

        ```py
        >>> ds = load_from_disk('path/to/dataset/directory')
        ```
        """
        fs: fsspec.AbstractFileSystem
        fs, dataset_dict_path = url_to_fs(dataset_dict_path, **(storage_options or {}))

        dataset_dict_json_path = posixpath.join(dataset_dict_path, config.DATASETDICT_JSON_FILENAME)
        dataset_state_json_path = posixpath.join(dataset_dict_path, config.DATASET_STATE_JSON_FILENAME)
        dataset_info_path = posixpath.join(dataset_dict_path, config.DATASET_INFO_FILENAME)
        if not fs.isfile(dataset_dict_json_path):
            if fs.isfile(dataset_info_path) and fs.isfile(dataset_state_json_path):
                raise FileNotFoundError(
                    f"No such file: '{dataset_dict_json_path}'. Expected to load a `DatasetDict` object, but got a `Dataset`. Please use either `datasets.load_from_disk` or `Dataset.load_from_disk` instead."
                )
            raise FileNotFoundError(
                f"No such file: '{dataset_dict_json_path}'. Expected to load a `DatasetDict` object, but provided path is not a `DatasetDict`."
            )

        with fs.open(dataset_dict_json_path, "r", encoding="utf-8") as f:
            splits = json.load(f)["splits"]

        dataset_dict = DatasetDict()
        for k in splits:
            dataset_dict_split_path = posixpath.join(fs.unstrip_protocol(dataset_dict_path), k)
            dataset_dict[k] = Dataset.load_from_disk(
                dataset_dict_split_path,
                keep_in_memory=keep_in_memory,
                storage_options=storage_options,
            )
        return dataset_dict

    @staticmethod
    def from_csv(
        path_or_paths: dict[str, PathLike],
        features: Optional[Features] = None,
        cache_dir: str = None,
        keep_in_memory: bool = False,
        **kwargs,
    ) -> "DatasetDict":
        """Create [`DatasetDict`] from CSV file(s).

        Args:
            path_or_paths (`dict` of path-like):
                Path(s) of the CSV file(s).
            features ([`Features`], *optional*):
                Dataset features.
            cache_dir (str, *optional*, defaults to `"~/.cache/huggingface/datasets"`):
                Directory to cache data.
            keep_in_memory (`bool`, defaults to `False`):
                Whether to copy the data in-memory.
            **kwargs (additional keyword arguments):
                Keyword arguments to be passed to [`pandas.read_csv`].

        Returns:
            [`DatasetDict`]

        Example:

        ```py
        >>> from datasets import DatasetDict
        >>> ds = DatasetDict.from_csv({'train': 'path/to/dataset.csv'})
        ```
        """
        # Dynamic import to avoid circular dependency
        from .io.csv import CsvDatasetReader

        return CsvDatasetReader(
            path_or_paths,
            features=features,
            cache_dir=cache_dir,
            keep_in_memory=keep_in_memory,
            **kwargs,
        ).read()

    @staticmethod
    def from_json(
        path_or_paths: dict[str, PathLike],
        features: Optional[Features] = None,
        cache_dir: str = None,
        keep_in_memory: bool = False,
        **kwargs,
    ) -> "DatasetDict":
        """Create [`DatasetDict`] from JSON Lines file(s).

        Args:
            path_or_paths (`path-like` or list of `path-like`):
                Path(s) of the JSON Lines file(s).
            features ([`Features`], *optional*):
                Dataset features.
            cache_dir (str, *optional*, defaults to `"~/.cache/huggingface/datasets"`):
                Directory to cache data.
            keep_in_memory (`bool`, defaults to `False`):
                Whether to copy the data in-memory.
            **kwargs (additional keyword arguments):
                Keyword arguments to be passed to [`JsonConfig`].

        Returns:
            [`DatasetDict`]

        Example:

        ```py
        >>> from datasets import DatasetDict
        >>> ds = DatasetDict.from_json({'train': 'path/to/dataset.json'})
        ```
        """
        # Dynamic import to avoid circular dependency
        from .io.json import JsonDatasetReader

        return JsonDatasetReader(
            path_or_paths,
            features=features,
            cache_dir=cache_dir,
            keep_in_memory=keep_in_memory,
            **kwargs,
        ).read()

    @staticmethod
    def from_parquet(
        path_or_paths: dict[str, PathLike],
        features: Optional[Features] = None,
        cache_dir: str = None,
        keep_in_memory: bool = False,
        columns: Optional[list[str]] = None,
        **kwargs,
    ) -> "DatasetDict":
        """Create [`DatasetDict`] from Parquet file(s).

        Args:
            path_or_paths (`dict` of path-like):
                Path(s) of the CSV file(s).
            features ([`Features`], *optional*):
                Dataset features.
            cache_dir (`str`, *optional*, defaults to `"~/.cache/huggingface/datasets"`):
                Directory to cache data.
            keep_in_memory (`bool`, defaults to `False`):
                Whether to copy the data in-memory.
            columns (`list[str]`, *optional*):
                If not `None`, only these columns will be read from the file.
                A column name may be a prefix of a nested field, e.g. 'a' will select
                'a.b', 'a.c', and 'a.d.e'.
            **kwargs (additional keyword arguments):
                Keyword arguments to be passed to [`ParquetConfig`].

        Returns:
            [`DatasetDict`]

        Example:

        ```py
        >>> from datasets import DatasetDict
        >>> ds = DatasetDict.from_parquet({'train': 'path/to/dataset/parquet'})
        ```
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
        path_or_paths: dict[str, PathLike],
        features: Optional[Features] = None,
        cache_dir: str = None,
        keep_in_memory: bool = False,
        **kwargs,
    ) -> "DatasetDict":
        """Create [`DatasetDict`] from text file(s).

        Args:
            path_or_paths (`dict` of path-like):
                Path(s) of the text file(s).
            features ([`Features`], *optional*):
                Dataset features.
            cache_dir (`str`, *optional*, defaults to `"~/.cache/huggingface/datasets"`):
                Directory to cache data.
            keep_in_memory (`bool`, defaults to `False`):
                Whether to copy the data in-memory.
            **kwargs (additional keyword arguments):
                Keyword arguments to be passed to [`TextConfig`].

        Returns:
            [`DatasetDict`]

        Example:

        ```py
        >>> from datasets import DatasetDict
        >>> ds = DatasetDict.from_text({'train': 'path/to/dataset.txt'})
        ```
        """
        # Dynamic import to avoid circular dependency
        from .io.text import TextDatasetReader

        return TextDatasetReader(
            path_or_paths,
            features=features,
            cache_dir=cache_dir,
            keep_in_memory=keep_in_memory,
            **kwargs,
        ).read()

    @is_documented_by(Dataset.align_labels_with_mapping)
    def align_labels_with_mapping(self, label2id: dict, label_column: str) -> "DatasetDict":
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
        config_name: str = "default",
        set_default: Optional[bool] = None,
        data_dir: Optional[str] = None,
        commit_message: Optional[str] = None,
        commit_description: Optional[str] = None,
        private: Optional[bool] = None,
        token: Optional[str] = None,
        revision: Optional[str] = None,
        create_pr: Optional[bool] = False,
        max_shard_size: Optional[Union[int, str]] = None,
        num_shards: Optional[dict[str, int]] = None,
        embed_external_files: bool = True,
        num_proc: Optional[int] = None,
    ) -> CommitInfo:
        """Pushes the [`DatasetDict`] to the hub as a Parquet dataset.
        The [`DatasetDict`] is pushed using HTTP requests and does not need to have neither git or git-lfs installed.

        Each dataset split will be pushed independently. The pushed dataset will keep the original split names.

        The resulting Parquet files are self-contained by default: if your dataset contains [`Image`] or [`Audio`]
        data, the Parquet files will store the bytes of your images or audio files.
        You can disable this by setting `embed_external_files` to False.

        Args:
            repo_id (`str`):
                The ID of the repository to push to in the following format: `<user>/<dataset_name>` or
                `<org>/<dataset_name>`. Also accepts `<dataset_name>`, which will default to the namespace
                of the logged-in user.
            config_name (`str`):
                Configuration name of a dataset. Defaults to "default".
            set_default (`bool`, *optional*):
                Whether to set this configuration as the default one. Otherwise, the default configuration is the one
                named "default".
            data_dir (`str`, *optional*):
                Directory name that will contain the uploaded data files. Defaults to the `config_name` if different
                from "default", else "data".

                <Added version="2.17.0"/>
            commit_message (`str`, *optional*):
                Message to commit while pushing. Will default to `"Upload dataset"`.
            commit_description (`str`, *optional*):
                Description of the commit that will be created.
                Additionally, description of the PR if a PR is created (`create_pr` is True).

                <Added version="2.16.0"/>
            private (`bool`, *optional*):
                Whether to make the repo private. If `None` (default), the repo will be public unless the
                organization's default is private. This value is ignored if the repo already exists.
            token (`str`, *optional*):
                An optional authentication token for the Hugging Face Hub. If no token is passed, will default
                to the token saved locally when logging in with `huggingface-cli login`. Will raise an error
                if no token is passed and the user is not logged-in.
            revision (`str`, *optional*):
                Branch to push the uploaded files to. Defaults to the `"main"` branch.

                <Added version="2.15.0"/>
            create_pr (`bool`, *optional*, defaults to `False`):
                Whether to create a PR with the uploaded files or directly commit.

                <Added version="2.15.0"/>
            max_shard_size (`int` or `str`, *optional*, defaults to `"500MB"`):
                The maximum size of the dataset shards to be uploaded to the hub. If expressed as a string, needs to be digits followed by a unit
                (like `"500MB"` or `"1GB"`).
            num_shards (`Dict[str, int]`, *optional*):
                Number of shards to write. By default, the number of shards depends on `max_shard_size`.
                Use a dictionary to define a different num_shards for each split.

                <Added version="2.8.0"/>
            embed_external_files (`bool`, defaults to `True`):
                Whether to embed file bytes in the shards.
                In particular, this will do the following before the push for the fields of type:

                - [`Audio`] and [`Image`] removes local path information and embed file content in the Parquet files.
            num_proc (`int`, *optional*, defaults to `None`):
                Number of processes when preparing and uploading the dataset.
                This is helpful if the dataset is made of many samples or media files to embed.
                Multiprocessing is disabled by default.

                <Added version="4.0.0"/>

        Return:
            huggingface_hub.CommitInfo

        Example:

        ```python
        >>> dataset_dict.push_to_hub("<organization>/<dataset_id>")
        >>> dataset_dict.push_to_hub("<organization>/<dataset_id>", private=True)
        >>> dataset_dict.push_to_hub("<organization>/<dataset_id>", max_shard_size="1GB")
        >>> dataset_dict.push_to_hub("<organization>/<dataset_id>", num_shards={"train": 1024, "test": 8})
        ```

        If you want to add a new configuration (or subset) to a dataset (e.g. if the dataset has multiple tasks/versions/languages):

        ```python
        >>> english_dataset.push_to_hub("<organization>/<dataset_id>", "en")
        >>> french_dataset.push_to_hub("<organization>/<dataset_id>", "fr")
        >>> # later
        >>> english_dataset = load_dataset("<organization>/<dataset_id>", "en")
        >>> french_dataset = load_dataset("<organization>/<dataset_id>", "fr")
        ```
        """
        if num_shards is None:
            num_shards = dict.fromkeys(self)
        elif not isinstance(num_shards, dict):
            raise ValueError(
                "Please provide one `num_shards` per dataset in the dataset dictionary, e.g. {{'train': 128, 'test': 4}}"
            )

        self._check_values_type()
        self._check_values_features()
        total_uploaded_size = 0
        total_dataset_nbytes = 0
        info_to_dump: DatasetInfo = next(iter(self.values())).info.copy()
        info_to_dump.config_name = config_name
        info_to_dump.splits = SplitDict()

        for split in self.keys():
            if not re.match(_split_re, split):
                raise ValueError(f"Split name should match '{_split_re}' but got '{split}'.")

        api = HfApi(endpoint=config.HF_ENDPOINT, token=token)

        try:
            repo_id = api.repo_info(repo_id, repo_type="dataset").id
        except RepositoryNotFoundError:
            repo_url = api.create_repo(
                repo_id,
                repo_type="dataset",
                private=private,
                exist_ok=True,
            )
            repo_id = repo_url.repo_id

        if revision is not None and not revision.startswith("refs/pr/"):
            # We do not call create_branch for a PR reference: 400 Bad Request
            api.create_branch(
                repo_id,
                branch=revision,
                token=token,
                repo_type="dataset",
                exist_ok=True,
            )

        if not data_dir:
            data_dir = config_name if config_name != "default" else "data"  # for backward compatibility

        additions = []
        for split in self.keys():
            logger.info(f"Pushing split {split} to the Hub.")
            # The split=key needs to be removed before merging
            split_additions, uploaded_size, dataset_nbytes = self[split]._push_parquet_shards_to_hub(
                repo_id,
                data_dir=data_dir,
                split=split,
                token=token,
                revision=revision,
                create_pr=create_pr,
                max_shard_size=max_shard_size,
                num_shards=num_shards.get(split),
                embed_external_files=embed_external_files,
                num_proc=num_proc,
            )
            additions += split_additions
            total_uploaded_size += uploaded_size
            total_dataset_nbytes += dataset_nbytes
            info_to_dump.splits[split] = SplitInfo(str(split), num_bytes=dataset_nbytes, num_examples=len(self[split]))
        info_to_dump.download_checksums = None
        info_to_dump.download_size = total_uploaded_size
        info_to_dump.dataset_size = total_dataset_nbytes
        info_to_dump.size_in_bytes = total_uploaded_size + total_dataset_nbytes

        def get_deletions_and_dataset_card() -> tuple[str, list[CommitOperationDelete], str, Optional[str]]:
            parent_commit = api.repo_info(repo_id, repo_type="dataset", revision=revision).sha

            # Check if the repo already has a README.md and/or a dataset_infos.json to update them with the new split info (size and pattern)
            # and delete old split shards (if they exist)
            repo_with_dataset_card, repo_with_dataset_infos = False, False
            repo_splits: list[str] = []  # use a list to keep the order of the splits
            deletions: list[CommitOperationDelete] = []
            repo_files_to_add = [addition.path_in_repo for addition in additions]
            for repo_file in api.list_repo_tree(
                repo_id=repo_id,
                revision=parent_commit,
                repo_type="dataset",
                token=token,
                recursive=True,
            ):
                if not isinstance(repo_file, RepoFile):
                    continue
                if repo_file.rfilename == config.REPOCARD_FILENAME:
                    repo_with_dataset_card = True
                elif repo_file.rfilename == config.DATASETDICT_INFOS_FILENAME:
                    repo_with_dataset_infos = True
                elif (
                    repo_file.rfilename.startswith(tuple(f"{data_dir}/{split}-" for split in self.keys()))
                    and repo_file.rfilename not in repo_files_to_add
                ):
                    deletions.append(CommitOperationDelete(path_in_repo=repo_file.rfilename))
                elif fnmatch.fnmatch(
                    repo_file.rfilename,
                    PUSH_TO_HUB_WITHOUT_METADATA_CONFIGS_SPLIT_PATTERN_SHARDED.replace("{split}", "*"),
                ):
                    pattern = glob_pattern_to_regex(PUSH_TO_HUB_WITHOUT_METADATA_CONFIGS_SPLIT_PATTERN_SHARDED)
                    split_pattern_fields = string_to_dict(repo_file.rfilename, pattern)
                    assert split_pattern_fields is not None
                    repo_split = split_pattern_fields["split"]
                    if repo_split not in repo_splits:
                        repo_splits.append(repo_split)

            # get the info from the README to update them
            if repo_with_dataset_card:
                dataset_card_path = api.hf_hub_download(
                    repo_id,
                    config.REPOCARD_FILENAME,
                    repo_type="dataset",
                    revision=parent_commit,
                )
                dataset_card = DatasetCard.load(Path(dataset_card_path))
                dataset_card_data = dataset_card.data
                metadata_configs = MetadataConfigs.from_dataset_card_data(dataset_card_data)
            # get the deprecated dataset_infos.json to update them
            elif repo_with_dataset_infos:
                dataset_card = None
                dataset_card_data = DatasetCardData()
                metadata_configs = MetadataConfigs()
            else:
                dataset_card = None
                dataset_card_data = DatasetCardData()
                metadata_configs = MetadataConfigs()
            # create the metadata configs if it was uploaded with push_to_hub before metadata configs existed
            if not metadata_configs and repo_splits:
                default_metadata_configs_to_dump = {
                    "data_files": [{"split": split, "path": f"data/{split}-*"} for split in repo_splits]
                }
                MetadataConfigs({"default": default_metadata_configs_to_dump}).to_dataset_card_data(dataset_card_data)
            metadata_config_to_dump = {
                "data_files": [{"split": split, "path": f"{data_dir}/{split}-*"} for split in self.keys()],
            }
            configs_to_dump = {config_name: metadata_config_to_dump}
            if set_default and config_name != "default":
                if metadata_configs:
                    current_default_config_name = metadata_configs.get_default_config_name()
                    if current_default_config_name == "default":
                        raise ValueError(
                            "There exists a configuration named 'default'. To set a different configuration as default, "
                            "rename the 'default' one first."
                        )
                    if current_default_config_name:
                        _ = metadata_configs[current_default_config_name].pop("default")
                        configs_to_dump[current_default_config_name] = metadata_configs[current_default_config_name]
                metadata_config_to_dump["default"] = True
            # push to the deprecated dataset_infos.json
            if repo_with_dataset_infos:
                dataset_infos_path = api.hf_hub_download(
                    repo_id,
                    config.DATASETDICT_INFOS_FILENAME,
                    repo_type="dataset",
                    revision=parent_commit,
                )
                with open(dataset_infos_path, encoding="utf-8") as f:
                    dataset_infos: dict = json.load(f)
                dataset_infos[config_name] = asdict(info_to_dump)
                new_dataset_infos = json.dumps(dataset_infos, indent=4)
            else:
                new_dataset_infos = None
            # push to README
            DatasetInfosDict({config_name: info_to_dump}).to_dataset_card_data(dataset_card_data)
            MetadataConfigs(configs_to_dump).to_dataset_card_data(dataset_card_data)
            new_dataset_card = (
                DatasetCard(f"---\n{dataset_card_data}\n---\n") if dataset_card is None else dataset_card
            )
            return parent_commit, deletions, new_dataset_card, new_dataset_infos

        commit_message = commit_message if commit_message is not None else "Upload dataset"
        if len(additions) > config.UPLOADS_MAX_NUMBER_PER_COMMIT:
            logger.info(
                f"Number of files to upload is larger than {config.UPLOADS_MAX_NUMBER_PER_COMMIT}. Splitting the push into multiple commits."
            )
            num_commits = math.ceil(len(additions) / config.UPLOADS_MAX_NUMBER_PER_COMMIT)
            for i in range(0, num_commits):
                operations = additions[
                    i * config.UPLOADS_MAX_NUMBER_PER_COMMIT : (i + 1) * config.UPLOADS_MAX_NUMBER_PER_COMMIT
                ]
                for retry, sleep_time in enumerate(itertools.chain(range(10), itertools.repeat(30)), start=1):
                    # We need to retry if another commit happens at the same time
                    sleep_time *= 1 + random.random()
                    try:
                        commit_info = api.create_commit(
                            repo_id,
                            operations=operations,
                            commit_message=commit_message + f" (part {i:05d}-of-{num_commits:05d})",
                            commit_description=commit_description,
                            repo_type="dataset",
                            revision=revision,
                            create_pr=create_pr,
                        )
                    except HfHubHTTPError as err:
                        if (
                            err.__context__
                            and isinstance(err.__context__, HTTPError)
                            and err.__context__.response.status_code == 409
                        ):
                            # 409 is Conflict (another commit is in progress)
                            time.sleep(sleep_time)
                            logger.info(
                                f"Retrying intermediate commit for {repo_id}, {config_name} ({retry}/n with status_code {err.__context__.response.status_code})"
                            )
                            continue
                        else:
                            raise
                    break
                logger.info(
                    f"Commit #{i + 1} completed"
                    + (f" (still {num_commits - i - 1} to go)" if num_commits - i - 1 else "")
                    + "."
                )
            last_commit_additions = []
        else:
            last_commit_additions = additions

        for retry, sleep_time in enumerate(itertools.chain(range(10), itertools.repeat(30)), start=1):
            # We need to retry if there was a commit in between in case it touched the dataset card data
            sleep_time *= 1 + random.random()
            parent_commit, deletions, dataset_card, dataset_infos = get_deletions_and_dataset_card()
            dataset_card_additions = []
            if dataset_infos:
                dataset_card_additions.append(
                    CommitOperationAdd(
                        path_in_repo=config.DATASETDICT_INFOS_FILENAME,
                        path_or_fileobj=dataset_infos.encode("utf-8"),
                    )
                )
            dataset_card_additions.append(
                CommitOperationAdd(path_in_repo=config.REPOCARD_FILENAME, path_or_fileobj=str(dataset_card).encode())
            )
            try:
                commit_info = api.create_commit(
                    repo_id,
                    operations=last_commit_additions + dataset_card_additions + deletions,
                    commit_message=commit_message,
                    commit_description=commit_description,
                    repo_type="dataset",
                    revision=revision,
                    create_pr=create_pr,
                    parent_commit=parent_commit,
                )
            except HfHubHTTPError as err:
                if (
                    err.__context__
                    and isinstance(err.__context__, HTTPError)
                    and err.__context__.response.status_code in (412, 409)
                ):
                    # 412 is Precondition failed (parent_commit isn't satisfied)
                    # 409 is Conflict (another commit is in progress)
                    time.sleep(sleep_time)
                    logger.info(
                        f"Retrying commit for {repo_id}, {config_name} ({retry}/n with status_code {err.__context__.response.status_code})"
                    )
                    continue
                else:
                    raise
            break

        return commit_info


class IterableDatasetDict(dict[Union[str, NamedSplit], IterableDataset]):
    def _check_values_type(self):
        for dataset in self.values():
            if not isinstance(dataset, IterableDataset):
                raise TypeError(f"Values in `DatasetDict` should be of type `Dataset` but got type '{type(dataset)}'")

    def _check_values_features(self):
        items = [(key, dataset._resolve_features()) for key, dataset in self.items()]
        for item_a, item_b in zip(items[:-1], items[1:]):
            if item_a[1].features != item_b[1].features:
                raise ValueError(
                    f"All datasets in `DatasetDict` should have the same features but features for '{item_a[0]}' and '{item_b[0]}' don't match: {item_a[1].features} != {item_b[1].features}"
                )

    def __repr__(self):
        repr = "\n".join([f"{k}: {v}" for k, v in self.items()])
        repr = re.sub(r"^", " " * 4, repr, count=0, flags=re.M)
        return f"IterableDatasetDict({{\n{repr}\n}})"

    @property
    def num_columns(self) -> dict[str, Optional[int]]:
        """Number of columns in each split of the dataset.
        This can contain None valies if some splits have unknown features (e.g. after a map() operation).

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> ds.num_columns
        {'test': 2, 'train': 2, 'validation': 2}
        ```
        """
        self._check_values_type()
        return {k: dataset.num_columns for k, dataset in self.items()}

    @property
    def column_names(self) -> dict[str, Optional[list[str]]]:
        """Names of the columns in each split of the dataset.
        This can contain None valies if some splits have unknown features (e.g. after a map() operation).

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        >>> ds.column_names
        {'test': ['text', 'label'],
         'train': ['text', 'label'],
         'validation': ['text', 'label']}
        ```
        """
        self._check_values_type()
        return {k: dataset.column_names for k, dataset in self.items()}

    def with_format(
        self,
        type: Optional[str] = None,
    ) -> "IterableDatasetDict":
        """
        Return a dataset with the specified format.

        Args:

            type (`str`, *optional*):
                Either output type selected in `[None, 'numpy', 'torch', 'tensorflow', 'jax', 'arrow', 'pandas', 'polars']`.
                `None` means it returns python objects (default).

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> from transformers import AutoTokenizer
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes", split="validation", streaming=True)
        >>> tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        >>> ds = ds.map(lambda x: tokenizer(x['text'], truncation=True, padding=True), batched=True)
        >>> ds = ds.with_format("torch")
        >>> next(iter(ds))
        {'text': 'compassionately explores the seemingly irreconcilable situation between conservative christian parents and their estranged gay and lesbian children .',
         'label': tensor(1),
         'input_ids': tensor([  101, 18027, 16310, 16001,  1103,  9321,   178, 11604,  7235,  6617,
                1742,  2165,  2820,  1206,  6588, 22572, 12937,  1811,  2153,  1105,
                1147, 12890, 19587,  6463,  1105, 15026,  1482,   119,   102,     0,
                    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                    0,     0,     0,     0]),
         'token_type_ids': tensor([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
         'attention_mask': tensor([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])}
        ```
        """
        return IterableDatasetDict({k: dataset.with_format(type=type) for k, dataset in self.items()})

    def map(
        self,
        function: Optional[Callable] = None,
        with_indices: bool = False,
        with_split: bool = False,
        input_columns: Optional[Union[str, list[str]]] = None,
        batched: bool = False,
        batch_size: int = 1000,
        drop_last_batch: bool = False,
        remove_columns: Optional[Union[str, list[str]]] = None,
        fn_kwargs: Optional[dict] = None,
    ) -> "IterableDatasetDict":
        """
        Apply a function to all the examples in the iterable dataset (individually or in batches) and update them.
        If your function returns a column that already exists, then it overwrites it.
        The function is applied on-the-fly on the examples when iterating over the dataset.
        The transformation is applied to all the datasets of the dataset dictionary.

        You can specify whether the function should be batched or not with the `batched` parameter:

        - If batched is `False`, then the function takes 1 example in and should return 1 example.
          An example is a dictionary, e.g. `{"text": "Hello there !"}`.
        - If batched is `True` and `batch_size` is 1, then the function takes a batch of 1 example as input and can return a batch with 1 or more examples.
          A batch is a dictionary, e.g. a batch of 1 example is `{"text": ["Hello there !"]}`.
        - If batched is `True` and `batch_size` is `n` > 1, then the function takes a batch of `n` examples as input and can return a batch with `n` examples, or with an arbitrary number of examples.
          Note that the last batch may have less than `n` examples.
          A batch is a dictionary, e.g. a batch of `n` examples is `{"text": ["Hello there !"] * n}`.

        If the function is asynchronous, then `map` will run your function in parallel, with up to one thousand simultaneous calls.
        It is recommended to use a `asyncio.Semaphore` in your function if you want to set a maximum number of operations that can run at the same time.

        Args:
            function (`Callable`, *optional*, defaults to `None`):
                Function applied on-the-fly on the examples when you iterate on the dataset.
                It must have one of the following signatures:

                - `function(example: Dict[str, Any]) -> Dict[str, Any]` if `batched=False` and `with_indices=False`
                - `function(example: Dict[str, Any], idx: int) -> Dict[str, Any]` if `batched=False` and `with_indices=True`
                - `function(batch: Dict[str, list]) -> Dict[str, list]` if `batched=True` and `with_indices=False`
                - `function(batch: Dict[str, list], indices: list[int]) -> Dict[str, list]` if `batched=True` and `with_indices=True`

                For advanced usage, the function can also return a `pyarrow.Table`.
                If the function is asynchronous, then `map` will run your function in parallel.
                Moreover if your function returns nothing (`None`), then `map` will run your function and return the dataset unchanged.
                If no function is provided, default to identity function: `lambda x: x`.
            with_indices (`bool`, defaults to `False`):
                Provide example indices to `function`. Note that in this case the signature of `function` should be `def function(example, idx[, rank]): ...`.
            input_columns (`[Union[str, list[str]]]`, *optional*, defaults to `None`):
                The columns to be passed into `function`
                as positional arguments. If `None`, a dict mapping to all formatted columns is passed as one argument.
            batched (`bool`, defaults to `False`):
                Provide batch of examples to `function`.
            batch_size (`int`, *optional*, defaults to `1000`):
                Number of examples per batch provided to `function` if `batched=True`.
            drop_last_batch (`bool`, defaults to `False`):
                Whether a last batch smaller than the `batch_size` should be
                dropped instead of being processed by the function.
            remove_columns (`[list[str]]`, *optional*, defaults to `None`):
                Remove a selection of columns while doing the mapping.
                Columns will be removed before updating the examples with the output of `function`, i.e. if `function` is adding
                columns with names in `remove_columns`, these columns will be kept.
            fn_kwargs (`Dict`, *optional*, defaults to `None`):
                Keyword arguments to be passed to `function`

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes", streaming=True)
        >>> def add_prefix(example):
        ...     example["text"] = "Review: " + example["text"]
        ...     return example
        >>> ds = ds.map(add_prefix)
        >>> next(iter(ds["train"]))
        {'label': 1,
         'text': 'Review: the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .'}
        ```
        """

        dataset_dict = {}
        for split, dataset in self.items():
            if with_split:
                function = bind(function, split)

            dataset_dict[split] = dataset.map(
                function=function,
                with_indices=with_indices,
                input_columns=input_columns,
                batched=batched,
                batch_size=batch_size,
                drop_last_batch=drop_last_batch,
                remove_columns=remove_columns,
                fn_kwargs=fn_kwargs,
            )

            if with_split:
                function = function.func

        return IterableDatasetDict(dataset_dict)

    def filter(
        self,
        function: Optional[Callable] = None,
        with_indices=False,
        input_columns: Optional[Union[str, list[str]]] = None,
        batched: bool = False,
        batch_size: Optional[int] = 1000,
        fn_kwargs: Optional[dict] = None,
    ) -> "IterableDatasetDict":
        """Apply a filter function to all the elements so that the dataset only includes examples according to the filter function.
        The filtering is done on-the-fly when iterating over the dataset.
        The filtering is applied to all the datasets of the dataset dictionary.

        Args:
            function (`Callable`):
                Callable with one of the following signatures:

                - `function(example: Dict[str, Any]) -> bool` if `with_indices=False, batched=False`
                - `function(example: Dict[str, Any], indices: int) -> bool` if `with_indices=True, batched=False`
                - `function(example: Dict[str, list]) -> list[bool]` if `with_indices=False, batched=True`
                - `function(example: Dict[str, list], indices: list[int]) -> list[bool]` if `with_indices=True, batched=True`

                If no function is provided, defaults to an always True function: `lambda x: True`.
            with_indices (`bool`, defaults to `False`):
                Provide example indices to `function`. Note that in this case the signature of `function` should be `def function(example, idx): ...`.
            input_columns (`str` or `list[str]`, *optional*):
                The columns to be passed into `function` as
                positional arguments. If `None`, a dict mapping to all formatted columns is passed as one argument.
            batched (`bool`, defaults to `False`):
                Provide batch of examples to `function`
            batch_size (`int`, *optional*, defaults to `1000`):
                Number of examples per batch provided to `function` if `batched=True`.
            fn_kwargs (`Dict`, *optional*, defaults to `None`):
                Keyword arguments to be passed to `function`

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes", streaming=True)
        >>> ds = ds.filter(lambda x: x["label"] == 0)
        >>> list(ds["train"].take(3))
        [{'label': 0, 'text': 'Review: simplistic , silly and tedious .'},
         {'label': 0,
         'text': "Review: it's so laddish and juvenile , only teenage boys could possibly find it funny ."},
         {'label': 0,
         'text': 'Review: exploitative and largely devoid of the depth or sophistication that would make watching such a graphic treatment of the crimes bearable .'}]
        ```
        """
        return IterableDatasetDict(
            {
                k: dataset.filter(
                    function=function,
                    with_indices=with_indices,
                    input_columns=input_columns,
                    batched=batched,
                    batch_size=batch_size,
                    fn_kwargs=fn_kwargs,
                )
                for k, dataset in self.items()
            }
        )

    def shuffle(
        self,
        seed=None,
        generator: Optional[np.random.Generator] = None,
        buffer_size: int = 1000,
    ) -> "IterableDatasetDict":
        """
        Randomly shuffles the elements of this dataset.
        The shuffling is applied to all the datasets of the dataset dictionary.

        This dataset fills a buffer with buffer_size elements, then randomly samples elements from this buffer,
        replacing the selected elements with new elements. For perfect shuffling, a buffer size greater than or
        equal to the full size of the dataset is required.

        For instance, if your dataset contains 10,000 elements but `buffer_size` is set to 1000, then `shuffle` will
        initially select a random element from only the first 1000 elements in the buffer. Once an element is
        selected, its space in the buffer is replaced by the next (i.e. 1,001-st) element,
        maintaining the 1000 element buffer.

        If the dataset is made of several shards, it also does `shuffle` the order of the shards.
        However if the order has been fixed by using [`~datasets.IterableDataset.skip`] or [`~datasets.IterableDataset.take`]
        then the order of the shards is kept unchanged.

        Args:
            seed (`int`, *optional*, defaults to `None`):
                Random seed that will be used to shuffle the dataset.
                It is used to sample from the shuffle buffer and also to shuffle the data shards.
            generator (`numpy.random.Generator`, *optional*):
                Numpy random Generator to use to compute the permutation of the dataset rows.
                If `generator=None` (default), uses `np.random.default_rng` (the default BitGenerator (PCG64) of NumPy).
            buffer_size (`int`, defaults to `1000`):
                Size of the buffer.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes", streaming=True)
        >>> list(ds["train"].take(3))
        [{'label': 1,
         'text': 'the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .'},
         {'label': 1,
         'text': 'the gorgeously elaborate continuation of " the lord of the rings " trilogy is so huge that a column of words cannot adequately describe co-writer/director peter jackson\'s expanded vision of j . r . r . tolkien\'s middle-earth .'},
         {'label': 1, 'text': 'effective but too-tepid biopic'}]
        >>> ds = ds.shuffle(seed=42)
        >>> list(ds["train"].take(3))
        [{'label': 1,
         'text': "a sports movie with action that's exciting on the field and a story you care about off it ."},
         {'label': 1,
         'text': 'at its best , the good girl is a refreshingly adult take on adultery . . .'},
         {'label': 1,
         'text': "sam jones became a very lucky filmmaker the day wilco got dropped from their record label , proving that one man's ruin may be another's fortune ."}]
        ```
        """
        return IterableDatasetDict(
            {
                k: dataset.shuffle(seed=seed, generator=generator, buffer_size=buffer_size)
                for k, dataset in self.items()
            }
        )

    def rename_column(self, original_column_name: str, new_column_name: str) -> "IterableDatasetDict":
        """
        Rename a column in the dataset, and move the features associated to the original column under the new column
        name.
        The renaming is applied to all the datasets of the dataset dictionary.

        Args:
            original_column_name (`str`):
                Name of the column to rename.
            new_column_name (`str`):
                New name for the column.

        Returns:
            [`IterableDatasetDict`]: A copy of the dataset with a renamed column.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes", streaming=True)
        >>> ds = ds.rename_column("text", "movie_review")
        >>> next(iter(ds["train"]))
        {'label': 1,
         'movie_review': 'the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .'}
        ```
        """
        return IterableDatasetDict(
            {
                k: dataset.rename_column(
                    original_column_name=original_column_name,
                    new_column_name=new_column_name,
                )
                for k, dataset in self.items()
            }
        )

    def rename_columns(self, column_mapping: dict[str, str]) -> "IterableDatasetDict":
        """
        Rename several columns in the dataset, and move the features associated to the original columns under
        the new column names.
        The renaming is applied to all the datasets of the dataset dictionary.

        Args:
            column_mapping (`Dict[str, str]`):
                A mapping of columns to rename to their new names.

        Returns:
            [`IterableDatasetDict`]: A copy of the dataset with renamed columns

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes", streaming=True)
        >>> ds = ds.rename_columns({"text": "movie_review", "label": "rating"})
        >>> next(iter(ds["train"]))
        {'movie_review': 'the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .',
         'rating': 1}
        ```
        """
        return IterableDatasetDict(
            {k: dataset.rename_columns(column_mapping=column_mapping) for k, dataset in self.items()}
        )

    def remove_columns(self, column_names: Union[str, list[str]]) -> "IterableDatasetDict":
        """
        Remove one or several column(s) in the dataset and the features associated to them.
        The removal is done on-the-fly on the examples when iterating over the dataset.
        The removal is applied to all the datasets of the dataset dictionary.


        Args:
            column_names (`Union[str, list[str]]`):
                Name of the column(s) to remove.

        Returns:
            [`IterableDatasetDict`]: A copy of the dataset object without the columns to remove.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes", streaming=True)
        >>> ds = ds.remove_columns("label")
        >>> next(iter(ds["train"]))
        {'text': 'the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .'}
        ```
        """
        return IterableDatasetDict({k: dataset.remove_columns(column_names) for k, dataset in self.items()})

    def select_columns(self, column_names: Union[str, list[str]]) -> "IterableDatasetDict":
        """Select one or several column(s) in the dataset and the features
        associated to them. The selection is done on-the-fly on the examples
        when iterating over the dataset. The selection is applied to all the
        datasets of the dataset dictionary.


        Args:
            column_names (`Union[str, list[str]]`):
                Name of the column(s) to keep.

        Returns:
            [`IterableDatasetDict`]: A copy of the dataset object with only selected columns.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes", streaming=True)
        >>> ds = ds.select("text")
        >>> next(iter(ds["train"]))
        {'text': 'the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .'}
        ```
        """
        return IterableDatasetDict({k: dataset.select_columns(column_names) for k, dataset in self.items()})

    def cast_column(self, column: str, feature: FeatureType) -> "IterableDatasetDict":
        """Cast column to feature for decoding.
        The type casting is applied to all the datasets of the dataset dictionary.

        Args:
            column (`str`):
                Column name.
            feature ([`Feature`]):
                Target feature.

        Returns:
            [`IterableDatasetDict`]

        Example:

        ```py
        >>> from datasets import load_dataset, ClassLabel
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes", streaming=True)
        >>> ds["train"].features
        {'label': ClassLabel(names=['neg', 'pos']),
         'text': Value('string')}
        >>> ds = ds.cast_column('label', ClassLabel(names=['bad', 'good']))
        >>> ds["train"].features
        {'label': ClassLabel(names=['bad', 'good']),
         'text': Value('string')}
        ```
        """
        return IterableDatasetDict(
            {k: dataset.cast_column(column=column, feature=feature) for k, dataset in self.items()}
        )

    def cast(
        self,
        features: Features,
    ) -> "IterableDatasetDict":
        """
        Cast the dataset to a new set of features.
        The type casting is applied to all the datasets of the dataset dictionary.

        Args:
            features (`Features`):
                New features to cast the dataset to.
                The name of the fields in the features must match the current column names.
                The type of the data must also be convertible from one type to the other.
                For non-trivial conversion, e.g. `string` <-> `ClassLabel` you should use [`map`] to update the Dataset.

        Returns:
            [`IterableDatasetDict`]: A copy of the dataset with casted features.

        Example:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset("cornell-movie-review-data/rotten_tomatoes", streaming=True)
        >>> ds["train"].features
        {'label': ClassLabel(names=['neg', 'pos']),
         'text': Value('string')}
        >>> new_features = ds["train"].features.copy()
        >>> new_features['label'] = ClassLabel(names=['bad', 'good'])
        >>> new_features['text'] = Value('large_string')
        >>> ds = ds.cast(new_features)
        >>> ds["train"].features
        {'label': ClassLabel(names=['bad', 'good']),
         'text': Value('large_string')}
        ```
        """
        return IterableDatasetDict({k: dataset.cast(features=features) for k, dataset in self.items()})

    def push_to_hub(
        self,
        repo_id,
        config_name: str = "default",
        set_default: Optional[bool] = None,
        data_dir: Optional[str] = None,
        commit_message: Optional[str] = None,
        commit_description: Optional[str] = None,
        private: Optional[bool] = None,
        token: Optional[str] = None,
        revision: Optional[str] = None,
        create_pr: Optional[bool] = False,
        # max_shard_size: Optional[Union[int, str]] = None,  # TODO(QL): add arg
        num_shards: Optional[dict[str, int]] = None,
        embed_external_files: bool = True,
        num_proc: Optional[int] = None,
    ) -> CommitInfo:
        """Pushes the [`DatasetDict`] to the hub as a Parquet dataset.
        The [`DatasetDict`] is pushed using HTTP requests and does not need to have neither git or git-lfs installed.

        Each dataset split will be pushed independently. The pushed dataset will keep the original split names.

        The resulting Parquet files are self-contained by default: if your dataset contains [`Image`] or [`Audio`]
        data, the Parquet files will store the bytes of your images or audio files.
        You can disable this by setting `embed_external_files` to False.

        Args:
            repo_id (`str`):
                The ID of the repository to push to in the following format: `<user>/<dataset_name>` or
                `<org>/<dataset_name>`. Also accepts `<dataset_name>`, which will default to the namespace
                of the logged-in user.
            config_name (`str`):
                Configuration name of a dataset. Defaults to "default".
            set_default (`bool`, *optional*):
                Whether to set this configuration as the default one. Otherwise, the default configuration is the one
                named "default".
            data_dir (`str`, *optional*):
                Directory name that will contain the uploaded data files. Defaults to the `config_name` if different
                from "default", else "data".

                <Added version="2.17.0"/>
            commit_message (`str`, *optional*):
                Message to commit while pushing. Will default to `"Upload dataset"`.
            commit_description (`str`, *optional*):
                Description of the commit that will be created.
                Additionally, description of the PR if a PR is created (`create_pr` is True).

                <Added version="2.16.0"/>
            private (`bool`, *optional*):
                Whether to make the repo private. If `None` (default), the repo will be public unless the
                organization's default is private. This value is ignored if the repo already exists.
            token (`str`, *optional*):
                An optional authentication token for the Hugging Face Hub. If no token is passed, will default
                to the token saved locally when logging in with `huggingface-cli login`. Will raise an error
                if no token is passed and the user is not logged-in.
            revision (`str`, *optional*):
                Branch to push the uploaded files to. Defaults to the `"main"` branch.
            create_pr (`bool`, *optional*, defaults to `False`):
                Whether to create a PR with the uploaded files or directly commit.
            num_shards (`Dict[str, int]`, *optional*):
                Number of shards to write. Equals to this dataset's `.num_shards` by default.
                Use a dictionary to define a different num_shards for each split.
            embed_external_files (`bool`, defaults to `True`):
                Whether to embed file bytes in the shards.
                In particular, this will do the following before the push for the fields of type:

                - [`Audio`] and [`Image`] removes local path information and embed file content in the Parquet files.
            num_proc (`int`, *optional*, defaults to `None`):
                Number of processes when preparing and uploading the dataset.
                This is helpful if the dataset is made of many samples or media files to embed.
                Multiprocessing is disabled by default.

                <Added version="4.0.0"/>

        Return:
            huggingface_hub.CommitInfo

        Example:

        ```python
        >>> dataset_dict.push_to_hub("<organization>/<dataset_id>")
        >>> dataset_dict.push_to_hub("<organization>/<dataset_id>", private=True)
        >>> dataset_dict.push_to_hub("<organization>/<dataset_id>", num_shards={"train": 1024, "test": 8})
        ```

        If you want to add a new configuration (or subset) to a dataset (e.g. if the dataset has multiple tasks/versions/languages):

        ```python
        >>> english_dataset.push_to_hub("<organization>/<dataset_id>", "en")
        >>> french_dataset.push_to_hub("<organization>/<dataset_id>", "fr")
        >>> # later
        >>> english_dataset = load_dataset("<organization>/<dataset_id>", "en")
        >>> french_dataset = load_dataset("<organization>/<dataset_id>", "fr")
        ```
        """
        if num_shards is None:
            num_shards = dict.fromkeys(self)
        elif not isinstance(num_shards, dict):
            raise ValueError(
                "Please provide one `num_shards` per dataset in the dataset dictionary, e.g. {{'train': 128, 'test': 4}}"
            )

        self._check_values_type()
        self._check_values_features()
        total_uploaded_size = 0
        total_dataset_nbytes = 0
        info_to_dump: DatasetInfo = next(iter(self.values())).info.copy()
        info_to_dump.config_name = config_name
        info_to_dump.splits = SplitDict()

        for split in self.keys():
            if not re.match(_split_re, split):
                raise ValueError(f"Split name should match '{_split_re}' but got '{split}'.")

        api = HfApi(endpoint=config.HF_ENDPOINT, token=token)

        try:
            repo_id = api.repo_info(repo_id, repo_type="dataset").id
        except RepositoryNotFoundError:
            repo_url = api.create_repo(
                repo_id,
                repo_type="dataset",
                private=private,
                exist_ok=True,
            )
            repo_id = repo_url.repo_id

        if revision is not None and not revision.startswith("refs/pr/"):
            # We do not call create_branch for a PR reference: 400 Bad Request
            api.create_branch(
                repo_id,
                branch=revision,
                token=token,
                repo_type="dataset",
                exist_ok=True,
            )

        if not data_dir:
            data_dir = config_name if config_name != "default" else "data"  # for backward compatibility

        additions = []
        for split in self.keys():
            logger.info(f"Pushing split {split} to the Hub.")
            # The split=key needs to be removed before merging
            split_additions, uploaded_size, dataset_nbytes, num_examples = self[split]._push_parquet_shards_to_hub(
                repo_id,
                data_dir=data_dir,
                split=split,
                token=token,
                revision=revision,
                create_pr=create_pr,
                # max_shard_size=max_shard_size,  # TODO(QL): add arg
                num_shards=num_shards.get(split),
                embed_external_files=embed_external_files,
                num_proc=num_proc,
            )
            additions += split_additions
            total_uploaded_size += uploaded_size
            total_dataset_nbytes += dataset_nbytes
            info_to_dump.splits[split] = SplitInfo(str(split), num_bytes=dataset_nbytes, num_examples=num_examples)
        info_to_dump.download_checksums = None
        info_to_dump.download_size = total_uploaded_size
        info_to_dump.dataset_size = total_dataset_nbytes
        info_to_dump.size_in_bytes = total_uploaded_size + total_dataset_nbytes

        def get_deletions_and_dataset_card() -> tuple[str, list[CommitOperationDelete], str, Optional[str]]:
            parent_commit = api.repo_info(repo_id, repo_type="dataset", revision=revision).sha

            # Check if the repo already has a README.md and/or a dataset_infos.json to update them with the new split info (size and pattern)
            # and delete old split shards (if they exist)
            repo_with_dataset_card, repo_with_dataset_infos = False, False
            repo_splits: list[str] = []  # use a list to keep the order of the splits
            deletions: list[CommitOperationDelete] = []
            repo_files_to_add = [addition.path_in_repo for addition in additions]
            for repo_file in api.list_repo_tree(
                repo_id=repo_id,
                revision=parent_commit,
                repo_type="dataset",
                token=token,
                recursive=True,
            ):
                if not isinstance(repo_file, RepoFile):
                    continue
                if repo_file.rfilename == config.REPOCARD_FILENAME:
                    repo_with_dataset_card = True
                elif repo_file.rfilename == config.DATASETDICT_INFOS_FILENAME:
                    repo_with_dataset_infos = True
                elif (
                    repo_file.rfilename.startswith(tuple(f"{data_dir}/{split}-" for split in self.keys()))
                    and repo_file.rfilename not in repo_files_to_add
                ):
                    deletions.append(CommitOperationDelete(path_in_repo=repo_file.rfilename))
                elif fnmatch.fnmatch(
                    repo_file.rfilename,
                    PUSH_TO_HUB_WITHOUT_METADATA_CONFIGS_SPLIT_PATTERN_SHARDED.replace("{split}", "*"),
                ):
                    pattern = glob_pattern_to_regex(PUSH_TO_HUB_WITHOUT_METADATA_CONFIGS_SPLIT_PATTERN_SHARDED)
                    split_pattern_fields = string_to_dict(repo_file.rfilename, pattern)
                    assert split_pattern_fields is not None
                    repo_split = split_pattern_fields["split"]
                    if repo_split not in repo_splits:
                        repo_splits.append(repo_split)

            # get the info from the README to update them
            if repo_with_dataset_card:
                dataset_card_path = api.hf_hub_download(
                    repo_id,
                    config.REPOCARD_FILENAME,
                    repo_type="dataset",
                    revision=parent_commit,
                )
                dataset_card = DatasetCard.load(Path(dataset_card_path))
                dataset_card_data = dataset_card.data
                metadata_configs = MetadataConfigs.from_dataset_card_data(dataset_card_data)
            # get the deprecated dataset_infos.json to update them
            elif repo_with_dataset_infos:
                dataset_card = None
                dataset_card_data = DatasetCardData()
                metadata_configs = MetadataConfigs()
            else:
                dataset_card = None
                dataset_card_data = DatasetCardData()
                metadata_configs = MetadataConfigs()
            # create the metadata configs if it was uploaded with push_to_hub before metadata configs existed
            if not metadata_configs and repo_splits:
                default_metadata_configs_to_dump = {
                    "data_files": [{"split": split, "path": f"data/{split}-*"} for split in repo_splits]
                }
                MetadataConfigs({"default": default_metadata_configs_to_dump}).to_dataset_card_data(dataset_card_data)
            metadata_config_to_dump = {
                "data_files": [{"split": split, "path": f"{data_dir}/{split}-*"} for split in self.keys()],
            }
            configs_to_dump = {config_name: metadata_config_to_dump}
            if set_default and config_name != "default":
                if metadata_configs:
                    current_default_config_name = metadata_configs.get_default_config_name()
                    if current_default_config_name == "default":
                        raise ValueError(
                            "There exists a configuration named 'default'. To set a different configuration as default, "
                            "rename the 'default' one first."
                        )
                    if current_default_config_name:
                        _ = metadata_configs[current_default_config_name].pop("default")
                        configs_to_dump[current_default_config_name] = metadata_configs[current_default_config_name]
                metadata_config_to_dump["default"] = True
            # push to the deprecated dataset_infos.json
            if repo_with_dataset_infos:
                dataset_infos_path = api.hf_hub_download(
                    repo_id,
                    config.DATASETDICT_INFOS_FILENAME,
                    repo_type="dataset",
                    revision=parent_commit,
                )
                with open(dataset_infos_path, encoding="utf-8") as f:
                    dataset_infos: dict = json.load(f)
                dataset_infos[config_name] = asdict(info_to_dump)
                new_dataset_infos = json.dumps(dataset_infos, indent=4)
            else:
                new_dataset_infos = None
            # push to README
            DatasetInfosDict({config_name: info_to_dump}).to_dataset_card_data(dataset_card_data)
            MetadataConfigs(configs_to_dump).to_dataset_card_data(dataset_card_data)
            new_dataset_card = (
                DatasetCard(f"---\n{dataset_card_data}\n---\n") if dataset_card is None else dataset_card
            )
            return parent_commit, deletions, new_dataset_card, new_dataset_infos

        commit_message = commit_message if commit_message is not None else "Upload dataset"
        if len(additions) > config.UPLOADS_MAX_NUMBER_PER_COMMIT:
            logger.info(
                f"Number of files to upload is larger than {config.UPLOADS_MAX_NUMBER_PER_COMMIT}. Splitting the push into multiple commits."
            )
            num_commits = math.ceil(len(additions) / config.UPLOADS_MAX_NUMBER_PER_COMMIT)
            for i in range(0, num_commits):
                operations = additions[
                    i * config.UPLOADS_MAX_NUMBER_PER_COMMIT : (i + 1) * config.UPLOADS_MAX_NUMBER_PER_COMMIT
                ]
                for retry, sleep_time in enumerate(itertools.chain(range(10), itertools.repeat(30)), start=1):
                    # We need to retry if another commit happens at the same time
                    sleep_time *= 1 + random.random()
                    try:
                        commit_info = api.create_commit(
                            repo_id,
                            operations=operations,
                            commit_message=commit_message + f" (part {i:05d}-of-{num_commits:05d})",
                            commit_description=commit_description,
                            repo_type="dataset",
                            revision=revision,
                            create_pr=create_pr,
                        )
                    except HfHubHTTPError as err:
                        if (
                            err.__context__
                            and isinstance(err.__context__, HTTPError)
                            and err.__context__.response.status_code == 409
                        ):
                            # 409 is Conflict (another commit is in progress)
                            time.sleep(sleep_time)
                            logger.info(
                                f"Retrying intermediate commit for {repo_id}, {config_name} ({retry}/n with status_code {err.__context__.response.status_code})"
                            )
                            continue
                        else:
                            raise
                    break
                logger.info(
                    f"Commit #{i + 1} completed"
                    + (f" (still {num_commits - i - 1} to go)" if num_commits - i - 1 else "")
                    + "."
                )
            last_commit_additions = []
        else:
            last_commit_additions = additions

        for retry, sleep_time in enumerate(itertools.chain(range(10), itertools.repeat(30)), start=1):
            # We need to retry if there was a commit in between in case it touched the dataset card data
            sleep_time *= 1 + random.random()
            parent_commit, deletions, dataset_card, dataset_infos = get_deletions_and_dataset_card()
            dataset_card_additions = []
            if dataset_infos:
                dataset_card_additions.append(
                    CommitOperationAdd(
                        path_in_repo=config.DATASETDICT_INFOS_FILENAME,
                        path_or_fileobj=dataset_infos.encode("utf-8"),
                    )
                )
            dataset_card_additions.append(
                CommitOperationAdd(path_in_repo=config.REPOCARD_FILENAME, path_or_fileobj=str(dataset_card).encode())
            )
            try:
                commit_info = api.create_commit(
                    repo_id,
                    operations=last_commit_additions + dataset_card_additions + deletions,
                    commit_message=commit_message,
                    commit_description=commit_description,
                    repo_type="dataset",
                    revision=revision,
                    create_pr=create_pr,
                    parent_commit=parent_commit,
                )
            except HfHubHTTPError as err:
                if (
                    err.__context__
                    and isinstance(err.__context__, HTTPError)
                    and err.__context__.response.status_code in (412, 409)
                ):
                    # 412 is Precondition failed (parent_commit isn't satisfied)
                    # 409 is Conflict (another commit is in progress)
                    time.sleep(sleep_time)
                    logger.info(
                        f"Retrying commit for {repo_id}, {config_name} ({retry}/n with status_code {err.__context__.response.status_code})"
                    )
                    continue
                else:
                    raise
            break

        return commit_info
