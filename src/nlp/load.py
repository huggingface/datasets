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

from .arrow_dataset import Dataset
from .builder import BuilderConfig, DatasetBuilder
from .splits import Split
from .utils.checksums_utils import CHECKSUMS_FILE_NAME, URLS_CHECKSUMS_FOLDER_NAME
from .utils.download_manager import GenerateMode
from .utils.file_utils import DownloadConfig, cached_path, hf_bucket_url


logger = logging.getLogger(__name__)

CURRENT_FILE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DATASETS_PATH = os.path.join(CURRENT_FILE_DIRECTORY, "datasets")
DATASETS_MODULE = "nlp.datasets"


def get_builder_cls_from_module(dataset_module):
    builder_cls = None
    for name, obj in dataset_module.__dict__.items():
        if isinstance(obj, type) and issubclass(obj, DatasetBuilder):
            builder_cls = obj
            break
    assert builder_cls is not None, f"Can't find a DatasetBuilder in module {dataset_module}"
    return builder_cls


def import_main_class(dataset_name, dataset_hash):
    """ Load the module """
    importlib.invalidate_caches()
    module_path = ".".join([DATASETS_MODULE, dataset_name, dataset_hash, dataset_name])
    dataset_module = importlib.import_module(module_path)

    builder_cls = get_builder_cls_from_module(dataset_module)
    builder_cls._DYNAMICALLY_IMPORTED_MODULE = dataset_module
    return builder_cls


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


def setup_module(file_path: str, download_config: Optional[DownloadConfig] = None, **download_kwargs,) -> DatasetBuilder:
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
    if download_config is None:
        download_config = DownloadConfig(**download_kwargs)
    download_config.extract_compressed_file = True
    download_config.force_extract = True

    name = list(filter(lambda x: x, file_path.split("/")))[-1] + ".py"

    if not name.endswith(".py"):
        raise ValueError("The provided name should be the filename of a python script (ends with '.py')")

    # We have three ways to find the dataset processing file:
    # - if os.path.join(path, name) is a file or a remote url
    # - if path is a file or a remote url
    # - otherwise we assume path/name is a path to our S3 bucket
    combined_path = os.path.join(file_path, name)
    if os.path.isfile(combined_path):
        dataset_file = combined_path
    elif os.path.isfile(file_path):
        dataset_file = file_path
    else:
        dataset_file = hf_bucket_url(file_path, filename=name)

    dataset_base_path = os.path.dirname(dataset_file)  # remove the filename
    dataset_checksums_file = os.path.join(dataset_base_path, URLS_CHECKSUMS_FOLDER_NAME, CHECKSUMS_FILE_NAME)

    # Load the module in two steps:
    # 1. get the dataset processing file on the local filesystem if it's not there (download to cache dir)
    # 2. copy from the local file system inside the library to import it
    local_path = cached_path(dataset_file, download_config=download_config)
    if local_path is None:
        raise ValueError("Couldn't find script file {}.".format(dataset_file))

    # Download the checksums file if available
    local_checksums_file_path = cached_path(dataset_checksums_file, download_config=download_config,)

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

        local_import_path = cached_path(url_or_filename, download_config=download_config,)
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

    return dataset_name, dataset_hash


def load(
    path: str,
    split: Optional[Union[str, Split]] = None,
    name: Optional[str] = None,
    version: Optional[str] = None,
    description: Optional[str] = None,
    data_dir: Optional[str] = None,
    data_files: Union[Dict, List] = None,
    dataset_config: Optional[BuilderConfig] = None,
    in_memory: bool = False,
    download_config: Optional[DownloadConfig] = None,
    download_mode: Optional[GenerateMode] = None,
    ignore_checksums: bool = False,
    save_checksums: bool = False,
    **config_kwargs,
) -> Dataset:
    """Loads the named dataset.

    If `split=None` (the default), returns all splits for the dataset. Otherwise,
    returns the specified split.

    `load` is a convenience method that fetches the `nlp.DatasetBuilder` by
    string name, optionally calls `DatasetBuilder.download_and_prepare`
    (if `download=True`), and then calls `DatasetBuilder.as_dataset`.
    This is roughly equivalent to:

    ```
    dataset_builder = nlp.get_dataset_builder(name, data_dir=data_dir, **builder_kwargs)
    dataset_builder.download_and_prepare(**download_and_prepare_kwargs)
    ds = builder.as_dataset(split=split)
    return ds
    ```

    If you'd like NumPy arrays instead of `tf.data.Dataset`s or `tf.Tensor`s,
    you can pass the return value to `nlp.as_numpy`.

    Callers must pass arguments as keyword arguments.

    **Warning**: calling this function might potentially trigger the download
    of hundreds of GiB to disk. Refer to the `download` argument.

    Args:
        name: `str`, the name of the `Dataset` (the snake case
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
        cache_dir: `str` (optional), directory to read/write data.
            Defaults to "~/nlp".
        in_memory: `bool`, if `True`, loads the dataset in memory which
            increases iteration speeds. Note that if `True` and the dataset has
            unknown dimensions, the features will be padded to the maximum
            size across the dataset.
        builder_kwargs: `dict` (optional), keyword arguments to be passed to the
            `nlp.DatasetBuilder` constructor. `data_dir` will be passed
            through by default.

    Returns:
        ds: `tf.data.Dataset`, the dataset requested, or if `split` is None, a
            `dict<key: nlp.Split, value: nlp.data.Dataset>`. If `batch_size=-1`,
            these will be full datasets as `tf.Tensor`s.
    """

    # Download/copy dataset script
    dataset_name, dataset_hash = setup_module(path, download_config=download_config)

    # Get dataset builder class
    builder_cls = import_main_class(dataset_name, dataset_hash)

    # Instantiate dataset builder
    builder_instance = builder_cls(
        config=dataset_config,
        name=name,
        version=version,
        description=description,
        data_dir=data_dir,
        data_files=data_files,
        **config_kwargs,
    )

    # Download and prepare data
    builder_instance.download_and_prepare(
        download_config=download_config,
        download_mode=download_mode,
        ignore_checksums=ignore_checksums,
        save_checksums=save_checksums,
    )

    # Build dataset for splits
    ds = builder_instance.as_dataset(split=split)

    return ds
