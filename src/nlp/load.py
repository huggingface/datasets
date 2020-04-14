# coding=utf-8
# Copyright 2020 The HuggingFace NLP Authors and the TensorFlow Datasets Authors.
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
"""Access datasets."""

import abc
import inspect
import re
import os
import json
import shutil
import logging
import importlib

from typing import Optional, Dict, Union

from . import naming
from .builder import DatasetBuilder
from .utils import py_utils
from .splits import Split
from .utils.file_utils import (HF_DATASETS_CACHE, is_remote_url, hf_bucket_url,
                         cached_path, url_to_filename)

logger = logging.getLogger(__name__)

__all__ = [
        "builder",
        "load",
]


CURRENT_FILE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DATASETS_PATH = os.path.join(CURRENT_FILE_DIRECTORY, 'datasets')
DATASETS_MODULE = "nlp.datasets"


def load_dataset(path: str,
                 name: Optional[str] = None,
                 force_reload: bool = False,
                 resume_download: bool = False,
                 proxies: Optional[Dict] = None,
                 local_files_only: bool = False,
                 data_dir: Optional[str] = None,
                 **kwargs):
    r"""
        Download/extract/cache a dataset to add to the lib from a path or url which can be:
            - a path to a local directory containing the dataset processing python script
            - an url to a S3 directory with a dataset processing python script

        Dataset codes are cached inside the lib to allow easy import (avoid ugly sys.path tweaks)
        and using cloudpickle (among other things).

        Return: tuple of
            the unique id associated to the dataset
            the local path to the dataset
    """
    if name is None:
        name = list(filter(lambda x: x, path.split('/')))[-1] + '.py'

    combined_path = os.path.join(path, name)
    if os.path.isfile(path) or is_remote_url(path):
        dataset_file = path
    elif os.path.isfile(combined_path) or is_remote_url(combined_path):
        dataset_file = combined_path
    else:
        dataset_file = hf_bucket_url(path, postfix=name)

    # Get the file on our local file system (either cache_dir or already local path)
    local_path = cached_path(
        dataset_file,
        cache_dir=data_dir,
        force_download=force_reload,
        extract_compressed_file=True,
        force_extract=force_reload,
        local_files_only=local_files_only,
    )

    # Define a directory with a unique name in our dataset folder
    dataset_id = url_to_filename(local_path)
    dataset_folder_path = os.path.join(DATASETS_PATH, dataset_id)
    dataset_file_path = os.path.join(dataset_folder_path, name)

    # Check if the dataset directory was already there
    if os.path.exists(dataset_file_path) and not force_reload:
        logger.info("Dataset script %s already found in datasets directory at %s, returning it. Use `force_reload=True` to override.",
                    local_path, dataset_file_path)
    else:
        # Create directory for dataset in DATASETS_PATH
        logger.info("Creating unique folder for dataset %s in datasets directory at %s", local_path, dataset_folder_path)
        shutil.rmtree(dataset_folder_path, ignore_errors=True)
        os.makedirs(dataset_folder_path)

        # Copy dataset.py file there
        shutil.copyfile(local_path, dataset_file_path)

        # Record metadata associating original dataset path with local unique folder
        logger.info("Creating metadata file for dataset %s at %s", local_path, dataset_file_path + ".json")
        meta = {"original path": local_path, "library path": dataset_file_path}
        meta_path = dataset_file_path + ".json"
        with open(meta_path, "w") as meta_file:
            json.dump(meta, meta_file)

        # Add an empty __init__ file to load the module
        init_file_path = os.path.join(dataset_folder_path, '__init__.py')
        with open(init_file_path, 'w'):
            pass

    importlib.invalidate_caches()
    module_name = name.replace('.py', '')
    module_path = '.'.join([DATASETS_MODULE, dataset_id, module_name])
    dataset_module = importlib.import_module(module_path)

    builder_cls = None
    for name, obj in dataset_module.__dict__.items():
        if isinstance(obj, type) and issubclass(obj, DatasetBuilder):
            builder_cls = obj
            builder_cls.name = naming.camelcase_to_snakecase(name)
            break

    return builder_cls


def builder(path: str,
            name: Optional[str] = None,
            **builder_init_kwargs):
    """Fetches a `nlp.DatasetBuilder` by string name.

    Args:
        name: `str`, the name of the `DatasetBuilder` (the snake case
            version of the class name). This can be either `"dataset_name"` or
            `"dataset_name/config_name"` for datasets with `BuilderConfig`s.
            As a convenience, this string may contain comma-separated keyword
            arguments for the builder. For example `"foo_bar/a=True,b=3"` would use
            the `FooBar` dataset passing the keyword arguments `a=True` and `b=3`
            (for builders with configs, it would be `"foo_bar/zoo/a=True,b=3"` to
            use the `"zoo"` config and pass to the builder keyword arguments `a=True`
            and `b=3`).
        **builder_init_kwargs: `dict` of keyword arguments passed to the
            `DatasetBuilder`. These will override keyword arguments passed in `name`,
            if any.

    Returns:
        A `nlp.DatasetBuilder`.

    Raises:
        DatasetNotFoundError: if `name` is unrecognized.
    """
    if name is not None:
        name, builder_kwargs = _dataset_name_and_kwargs_from_name_str(name)
        builder_kwargs.update(builder_init_kwargs)
    else:
        builder_kwargs = builder_init_kwargs
    builder_cls = load_dataset(path, name=name, **builder_kwargs)
    builder_instance = builder_cls(**builder_kwargs)
    return builder_instance


def load(path: str,
         name: Optional[str] = None,
         split: Optional[Union[str, Split]] = None,
         data_dir: Optional[str] = None,
                 batch_size=None,
                 in_memory=None,
                 download=True,
                 as_supervised=False,
                 with_info=False,
                 builder_kwargs=None,
                 download_and_prepare_kwargs=None,
                 as_dataset_kwargs=None):
    # pylint: disable=line-too-long
    """Loads the named dataset.

    If `split=None` (the default), returns all splits for the dataset. Otherwise,
    returns the specified split.

    `load` is a convenience method that fetches the `nlp.DatasetBuilder` by
    string name, optionally calls `DatasetBuilder.download_and_prepare`
    (if `download=True`), and then calls `DatasetBuilder.as_dataset`.
    This is roughly equivalent to:

    ```
    builder = nlp.builder(name, data_dir=data_dir, **builder_kwargs)
    if download:
        builder.download_and_prepare(**download_and_prepare_kwargs)
    ds = builder.as_dataset(
            split=split, as_supervised=as_supervised, **as_dataset_kwargs)
    if with_info:
        return ds, builder.info
    return ds
    ```

    If you'd like NumPy arrays instead of `tf.data.Dataset`s or `tf.Tensor`s,
    you can pass the return value to `nlp.as_numpy`.

    Callers must pass arguments as keyword arguments.

    **Warning**: calling this function might potentially trigger the download
    of hundreds of GiB to disk. Refer to the `download` argument.

    Args:
        name: `str`, the name of the `DatasetBuilder` (the snake case
            version of the class name). This can be either `"dataset_name"` or
            `"dataset_name/config_name"` for datasets with `BuilderConfig`s.
            As a convenience, this string may contain comma-separated keyword
            arguments for the builder. For example `"foo_bar/a=True,b=3"` would use
            the `FooBar` dataset passing the keyword arguments `a=True` and `b=3`
            (for builders with configs, it would be `"foo_bar/zoo/a=True,b=3"` to
            use the `"zoo"` config and pass to the builder keyword arguments `a=True`
            and `b=3`).
        split: `nlp.Split` or `str`, which split of the data to load. If None,
            will return a `dict` with all splits (typically `nlp.Split.TRAIN` and
            `nlp.Split.TEST`).
        data_dir: `str` (optional), directory to read/write data.
            Defaults to "~/nlp".
        batch_size: `int`, if set, add a batch dimension to examples. Note that
            variable length features will be 0-padded. If
            `batch_size=-1`, will return the full dataset as `tf.Tensor`s.
        in_memory: `bool`, if `True`, loads the dataset in memory which
            increases iteration speeds. Note that if `True` and the dataset has
            unknown dimensions, the features will be padded to the maximum
            size across the dataset.
        download: `bool` (optional), whether to call
            `nlp.DatasetBuilder.download_and_prepare`
            before calling `tf.DatasetBuilder.as_dataset`. If `False`, data is
            expected to be in `data_dir`. If `True` and the data is already in
            `data_dir`, `download_and_prepare` is a no-op.
        as_supervised: `bool`, if `True`, the returned `tf.data.Dataset`
            will have a 2-tuple structure `(input, label)` according to
            `builder.info.supervised_keys`. If `False`, the default,
            the returned `tf.data.Dataset` will have a dictionary with all the
            features.
        with_info: `bool`, if True, nlp.load will return the tuple
            (tf.data.Dataset, nlp.DatasetInfo) containing the info associated
            with the builder.
        builder_kwargs: `dict` (optional), keyword arguments to be passed to the
            `nlp.DatasetBuilder` constructor. `data_dir` will be passed
            through by default.
        download_and_prepare_kwargs: `dict` (optional) keyword arguments passed to
            `nlp.DatasetBuilder.download_and_prepare` if `download=True`. Allow
            to control where to download and extract the cached data. If not set,
            cache_dir and manual_dir will automatically be deduced from data_dir.
        as_dataset_kwargs: `dict` (optional), keyword arguments passed to
            `nlp.DatasetBuilder.as_dataset`.

    Returns:
        ds: `tf.data.Dataset`, the dataset requested, or if `split` is None, a
            `dict<key: nlp.Split, value: nlp.data.Dataset>`. If `batch_size=-1`,
            these will be full datasets as `tf.Tensor`s.
        ds_info: `nlp.DatasetInfo`, if `with_info` is True, then `nlp.load`
            will return a tuple `(ds, ds_info)` containing dataset information
            (version, features, splits, num_examples,...). Note that the `ds_info`
            object documents the entire dataset, regardless of the `split` requested.
            Split-specific information is available in `ds_info.splits`.
    """
    # if name is not None:
    #     _, name_builder_kwargs = _dataset_name_and_kwargs_from_name_str(name)
    #     name_builder_kwargs.update(builder_kwargs or {})
    #     builder_kwargs = name_builder_kwargs

    if builder_kwargs is None:
        builder_kwargs = {}

    # Set data_dir
    if data_dir is None:
        data_dir = HF_DATASETS_CACHE

    dbuilder: DatasetBuilder = builder(path, name, data_dir=data_dir, **builder_kwargs)
    if download:
        download_and_prepare_kwargs = download_and_prepare_kwargs or {}
        dbuilder.download_and_prepare(**download_and_prepare_kwargs)

    if as_dataset_kwargs is None:
        as_dataset_kwargs = {}
    as_dataset_kwargs = dict(as_dataset_kwargs)
    as_dataset_kwargs.setdefault("split", split)
    as_dataset_kwargs.setdefault("as_supervised", as_supervised)
    as_dataset_kwargs.setdefault("batch_size", batch_size)

    ds = dbuilder.as_dataset(**as_dataset_kwargs)
    if with_info:
        return ds, dbuilder.info
    return ds


_VERSION_RE = r""

_NAME_REG = re.compile(
        r"^"
        r"(?P<dataset_name>\w+)"
        r"(/(?P<config>[\w\-\.]+))?"
        r"(:(?P<version>(\d+|\*)(\.(\d+|\*)){2}))?"
        r"(/(?P<kwargs>(\w+=\w+)(,\w+=[^,]+)*))?"
        r"$")


_NAME_STR_ERR = """\
Parsing builder name string {} failed.
The builder config string must be of the following format:
    dataset_name[/config_name][:version][/kwargs]

    Where:

        * dataset_name and config_name are string following python variable naming.
        * version is of the form x.y.z where {{x,y,z}} can be any digit or *.
        * kwargs is a comma list separated of arguments and values to pass to
            builder.

    Examples:
        my_dataset
        my_dataset:1.2.*
        my_dataset/config1
        my_dataset/config1:1.*.*
        my_dataset/config1/arg1=val1,arg2=val2
        my_dataset/config1:1.2.3/right=True,foo=bar,rate=1.2
"""

def _dataset_name_and_kwargs_from_name_str(name_str):
    """Extract kwargs from name str."""
    res = _NAME_REG.match(name_str)
    if not res:
        raise ValueError(_NAME_STR_ERR.format(name_str))
    name = res.group("dataset_name")
    kwargs = _kwargs_str_to_kwargs(res.group("kwargs"))
    try:
        for attr in ["config", "version"]:
            val = res.group(attr)
            if val is None:
                continue
            if attr in kwargs:
                raise ValueError("Dataset %s: cannot pass %s twice." % (name, attr))
            kwargs[attr] = val
        return name, kwargs
    except:
        logger.error(_NAME_STR_ERR.format(name_str))   # pylint: disable=logging-format-interpolation
        raise


def _kwargs_str_to_kwargs(kwargs_str):
    if not kwargs_str:
        return {}
    kwarg_strs = kwargs_str.split(",")
    kwargs = {}
    for kwarg_str in kwarg_strs:
        kwarg_name, kwarg_val = kwarg_str.split("=")
        kwargs[kwarg_name] = _cast_to_pod(kwarg_val)
    return kwargs


def _cast_to_pod(val):
    """Try cast to int, float, bool, str, in that order."""
    bools = {"True": True, "False": False}
    if val in bools:
        return bools[val]
    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except ValueError:
            return str(val)
