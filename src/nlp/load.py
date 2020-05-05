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

import importlib
import json
import logging
import os
import re
import shutil
from hashlib import sha256
from pathlib import Path
from typing import Dict, List, Optional, Union
from urllib.parse import urlparse

from filelock import FileLock

from .builder import DatasetBuilder
from .naming import camelcase_to_snakecase
from .splits import Split
from .utils.checksums_utils import CHECKSUMS_FILE_NAME, URLS_CHECKSUMS_FOLDER_NAME
from .utils.download_manager import DownloadConfig
from .utils.file_utils import HF_DATASETS_CACHE, cached_path, hf_bucket_url, is_remote_url


logger = logging.getLogger(__name__)

__all__ = [
    "builder",
    "load",
]


CURRENT_FILE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DATASETS_PATH = os.path.join(CURRENT_FILE_DIRECTORY, "datasets")
DATASETS_MODULE = "nlp.datasets"


def get_builder_cls_from_module(dataset_module):
    builder_cls = None
    for name, obj in dataset_module.__dict__.items():
        if isinstance(obj, type) and issubclass(obj, DatasetBuilder):
            builder_cls = obj
            builder_cls.name = camelcase_to_snakecase(name)
            break
    return builder_cls


def import_builder_class(dataset_name, dataset_hash):
    """ Load the module """
    importlib.invalidate_caches()
    module_path = ".".join([DATASETS_MODULE, dataset_name, dataset_hash, dataset_name])
    dataset_module = importlib.import_module(module_path)

    builder_cls = get_builder_cls_from_module(dataset_module)
    builder_cls._DYNAMICALLY_IMPORTED_MODULE = dataset_module
    return builder_cls, module_path


def files_to_hash(file_paths: List[str]):
    """
    Convert a list of scripts or text files provided in file_paths into a hashed filename in a repeatable way.
    """
    # List all python files in directories if directories are supplied as part of external imports
    to_use_files = []
    for file_path in file_paths:
        if os.path.isdir(file_path):
            to_use_files.extend(list(Path(file_path).rglob("*.[pP][yY]")))
        else:
            to_use_files.append(file_path)

    # Get the code from all these files
    lines = []
    for file_path in to_use_files:
        with open(file_path, mode="r") as f:
            lines.extend(f.readlines())
    filtered_lines = []
    for line in lines:
        line.replace("\n", "")  # remove line breaks, white space and comments
        line.replace(" ", "")
        line.replace("\t", "")
        line = re.sub(r"#.*", "", line)
        if line:
            filtered_lines.append(line)
    file_str = "\n".join(filtered_lines)

    # Make a hash from all this code
    file_bytes = file_str.encode("utf-8")
    file_hash = sha256(file_bytes)
    filename = file_hash.hexdigest()

    return filename


def _is_github_url(url_or_filename):
    """ Is this URL pointing to a github repository """
    parsed = urlparse(url_or_filename)
    return parsed.scheme in ("http", "https", "s3") and parsed.netloc == "github.com"


def get_imports(file_path: str):
    """ Find whether we should import or clone additional files for a given processing script.
        And list the import.

        We allow:
        - local dependencies and
        - external dependencies whose url is specified with a comment starting from "# From:' followed by an url to a file, an archive or a github repository.
            external dependencies will be downloaded (and extracted if needed in the dataset folder).
            We also add an `__init__.py` to each sub-folder of a downloaded folder so the user can import from them in the script.

        Note that only direct import in the dataset processing script will be handled
        We don't recursively explore the additional import to download further files.

        ```python
        import .c4_utils
        import .clicr.dataset-code.build_json_dataset  # From: https://github.com/clips/clicr
        ```
    """
    lines = []
    with open(file_path, mode="r") as f:
        lines.extend(f.readlines())

    logger.info("Checking %s for additional imports.", file_path)
    imports = []
    for line in lines:
        match = re.match(r"(?:from|import)\s+\.([^\s\.]+)[^#\r\n]*(?:#\s+From:\s+)?([^\r\n]*)", line)
        if match is None:
            continue
        if match.group(2):
            url_path = match.group(2)
            if _is_github_url(url_path):
                # Parse github url to point to zip
                repo_info, branch = url_path.split(":") if ":" in url_path else (url_path, "master")
                repo_owner, repo_name = repo_info.split("/")
                url_path = "https://github.com/{}/{}/archive/{}.zip".format(repo_owner, repo_name, branch)
            imports.append(("external", url_path))
        elif match.group(1):
            imports.append(("internal", match.group(1)))

    return imports


def load_dataset_module(
    path: str,
    name: Optional[str] = None,
    force_reload: bool = False,
    resume_download: bool = False,
    proxies: Optional[Dict] = None,
    local_files_only: bool = False,
    data_dir: Optional[str] = None,
    filenames: Optional[Dict] = None,
    **kwargs
):
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
    if name is None and path == "csv":
        raise ValueError("Generic CSV datasets needs a name")
    elif path == "csv":
        name += ".py"
        combined_path = os.path.join("datasets/nlp/csv", "csv.py")
    elif name is None:
        name = list(filter(lambda x: x, path.split("/")))[-1] + ".py"
        combined_path = os.path.join(path, name)

    if (not name.endswith(".py") or "/" in name) and path != "csv":
        raise ValueError("The provided name should be the filename of a python script (ends with '.py')")

    # We have three ways to find the dataset processing file:
    # - if os.path.join(path, name) is a file or a remote url
    # - if path is a file or a remote url
    # - otherwise we assume path/name is a path to our S3 bucket
    
    if os.path.isfile(combined_path) or is_remote_url(combined_path):
        dataset_file = combined_path
    elif os.path.isfile(path) or is_remote_url(path):
        dataset_file = path
    else:
        dataset_file = hf_bucket_url(path, filename=name)

    dataset_base_path = os.path.dirname(dataset_file)  # remove the filename
    dataset_checksums_file = os.path.join(dataset_base_path, URLS_CHECKSUMS_FOLDER_NAME, CHECKSUMS_FILE_NAME)

    # Load the module in two steps:
    # 1. get the dataset processing file on the local filesystem if it's not there (download to cache dir)
    # 2. copy from the local file system inside the library to import it
    local_path = cached_path(
        dataset_file,
        cache_dir=data_dir,
        force_download=force_reload,
        extract_compressed_file=True,
        force_extract=force_reload,
        local_files_only=local_files_only,
    )
    if local_path is None:
        raise ValueError("Couldn't find script file {}.".format(dataset_file))

    # Download the checksums file if available
    local_checksums_file_path = cached_path(
        dataset_checksums_file,
        cache_dir=data_dir,
        force_download=force_reload,
        extract_compressed_file=True,
        force_extract=force_reload,
        local_files_only=local_files_only,
    )

    # Download external imports if needed
    imports = get_imports(local_path)
    local_imports = []
    for import_type, import_name_or_path in imports:
        if import_type == "internal":
            url_or_filename = dataset_base_path + "/" + import_name_or_path + ".py"
        elif import_type == "external":
            url_or_filename = import_name_or_path
        else:
            raise ValueError("Script import should be external or internal.")

        local_import_path = cached_path(
            url_or_filename,
            cache_dir=data_dir,
            force_download=force_reload,
            extract_compressed_file=True,
            force_extract=force_reload,
            local_files_only=local_files_only,
        )
        local_imports.append(local_import_path)

    # Define a directory with a unique name in our dataset folder
    # path is: ./datasets/dataset_name/hash_from_code/script.py
    # we use a hash to be able to have multiple versions of a dataset processing file together
    dataset_name = name[:-3]  # Removing the '.py' at the end
    dataset_hash = files_to_hash([local_path] + local_imports)
    dataset_main_folder_path = os.path.join(DATASETS_PATH, dataset_name)
    dataset_hash_folder_path = os.path.join(dataset_main_folder_path, dataset_hash)
    dataset_file_path = os.path.join(dataset_hash_folder_path, name)
    dataset_urls_checksums_dir = os.path.join(dataset_hash_folder_path, URLS_CHECKSUMS_FOLDER_NAME)
    dataset_checksums_file_path = os.path.join(dataset_urls_checksums_dir, CHECKSUMS_FILE_NAME)

    # Prevent parallel disk operations
    lock_path = local_path + ".lock"
    with FileLock(lock_path):
        # Create main dataset folder if needed
        if not os.path.exists(dataset_main_folder_path):
            logger.info("Creating main folder for dataset %s at %s", dataset_file, dataset_main_folder_path)
            os.makedirs(dataset_main_folder_path, exist_ok=True)
        else:
            logger.info("Found main folder for dataset %s at %s", dataset_file, dataset_main_folder_path)

        # add an __init__ file to the main dataset folder if needed
        init_file_path = os.path.join(dataset_main_folder_path, "__init__.py")
        if not os.path.exists(init_file_path):
            with open(init_file_path, "w"):
                pass

        # Create hash dataset folder if needed
        if not os.path.exists(dataset_hash_folder_path):
            logger.info(
                "Creating specific version folder for dataset %s at %s", dataset_file, dataset_hash_folder_path
            )
            os.makedirs(dataset_hash_folder_path)
        else:
            logger.info("Found specific version folder for dataset %s at %s", dataset_file, dataset_hash_folder_path)

        # add an __init__ file to the hash dataset folder if needed
        init_file_path = os.path.join(dataset_hash_folder_path, "__init__.py")
        if not os.path.exists(init_file_path):
            with open(init_file_path, "w"):
                pass

        # Copy dataset.py file in hash folder if needed
        if not os.path.exists(dataset_file_path):
            logger.info("Copying script file from %s to %s", dataset_file, dataset_file_path)
            shutil.copyfile(local_path, dataset_file_path)
        else:
            logger.info("Found script file from %s to %s", dataset_file, dataset_file_path)

        # Copy checksums file if needed
        os.makedirs(dataset_urls_checksums_dir, exist_ok=True)
        if not os.path.exists(dataset_checksums_file_path):
            if local_checksums_file_path is not None:
                logger.info(
                    "Copying checksums file from %s to %s", dataset_checksums_file, dataset_checksums_file_path
                )
                shutil.copyfile(local_checksums_file_path, dataset_checksums_file_path)
            else:
                logger.info("Couldn't find checksums file at %s", dataset_checksums_file)
        else:
            logger.info("Found checksums file from %s to %s", dataset_checksums_file, dataset_checksums_file_path)

        # Record metadata associating original dataset path with local unique folder
        meta_path = dataset_file_path.split(".py")[0] + ".json"
        if not os.path.exists(meta_path):
            logger.info("Creating metadata file for dataset %s at %s", dataset_file, meta_path)
            meta = {"original file path": dataset_file, "local file path": dataset_file_path}
            # the filename is *.py in our case, so better rename to filenam.json instead of filename.py.json
            with open(meta_path, "w") as meta_file:
                json.dump(meta, meta_file)
        else:
            logger.info("Found metadata file for dataset %s at %s", dataset_file, meta_path)

        # Copy all the additional imports
        for local_import in local_imports:
            tail_name = os.path.basename(os.path.abspath(local_import))  # keep the last file or directory
            dataset_local_import = os.path.join(dataset_hash_folder_path, tail_name)
            if not os.path.exists(dataset_local_import):
                logger.info("Copying local import from %s to %s", local_import, dataset_local_import)
                if os.path.isdir(local_import):
                    shutil.copytree(local_import, dataset_local_import)
                    # add an __init__ file to the sub-directories in the copied folder if needed
                    # so people can relatively import from them
                    for root, _, files in os.walk(dataset_local_import, topdown=False):
                        if "__init__.py" not in files:
                            init_file_path = os.path.join(root, "__init__.py")
                            with open(init_file_path, "w"):
                                pass
                elif os.path.isfile(local_import):
                    shutil.copyfile(local_import, dataset_local_import)
                else:
                    raise ValueError(f"Error when copying {local_import} to {dataset_local_import}")
            else:
                logger.info("Found local import from %s to %s", local_import, dataset_local_import)

    builder_cls, _ = import_builder_class(dataset_name, dataset_hash)

    return builder_cls


def builder(path: str, name: Optional[str] = None, **builder_init_kwargs):
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
    builder_cls = load_dataset_module(path, name=name, **builder_kwargs)
    builder_instance = builder_cls(**builder_kwargs)
    return builder_instance


def csv_builder(path: str, name: str, dataset_files: Dict[Split, List], **csv_init_kwargs):
    """Fetches a CSV `nlp.DatasetBuilder` by string name.

    Args:
        path: `str`, the path where the script is located.
        name: `str`, the name of the `DatasetBuilder` (the snake case
            version of the class name). This can be either `"dataset_name"` or
            `"dataset_name/config_name"` for datasets with `BuilderConfig`s.
            As a convenience, this string may contain comma-separated keyword
            arguments for the builder. For example `"foo_bar/a=True,b=3"` would use
            the `FooBar` dataset passing the keyword arguments `a=True` and `b=3`
            (for builders with configs, it would be `"foo_bar/zoo/a=True,b=3"` to
            use the `"zoo"` config and pass to the builder keyword arguments `a=True`
            and `b=3`).
        dataset_files: `dict` of `Split` as keys and each value is a `list` of files
            location.
        **csv_init_kwargs: `dict` of keyword arguments passed to the CSV
            `DatasetBuilder`. These will override keyword arguments passed in `name`,
            if any.

    Returns:
        A `nlp.DatasetBuilder`.

    Raises:
        DatasetNotFoundError: if `name` is unrecognized.
    """
    if name is None:
        raise ValueError("The name parameter must be filled.")
    
    if dataset_files is None:
        raise ValueError("The dataset_files must be filled.")
    
    name, csv_kwargs = _dataset_name_and_kwargs_from_name_str(name)
    csv_kwargs.update(csv_init_kwargs)
    builder_cls = load_dataset_module(path, name=name)
    builder_instance = builder_cls(name, dataset_files, **csv_kwargs)

    return builder_instance


def load(
    path: str,
    name: Optional[str] = None,
    split: Optional[Union[str, Split]] = None,
    dataset_files: Dict[Split, List] = None,
    data_dir: Optional[str] = None,
    batch_size=None,
    in_memory=None,
    download=True,
    as_supervised=False,
    with_info=False,
    builder_kwargs=None,
    download_and_prepare_kwargs=None,
    as_dataset_kwargs=None,
    csv_kwargs=None,
    ignore_checksums=False,
):
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
        ignore_checksums: `bool`, if True, checksums test of downloaded files
            will be ignored. download_and_prepare_kwargs can overried this parameter.

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
    
    if csv_kwargs is None:
        csv_kwargs = {}

    # Set data_dir
    if data_dir is None:
        data_dir = HF_DATASETS_CACHE

    if path == "csv":
        csv_kwargs.update(builder_kwargs)
        dbuilder: DatasetBuilder = csv_builder(path, name, dataset_files, **csv_kwargs)
    else:   
        dbuilder: DatasetBuilder = builder(path, name, data_dir=data_dir, **builder_kwargs)
    
    if download:
        download_and_prepare_kwargs = download_and_prepare_kwargs or {
            "download_config": DownloadConfig(ignore_checksums=ignore_checksums)
        }
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
    r"$"
)


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
    except:  # noqa: E722
        logger.error(_NAME_STR_ERR.format(name_str))  # pylint: disable=logging-format-interpolation
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
