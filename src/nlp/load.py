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
from .metric import Metric
from .splits import Split
from .utils.checksums_utils import CHECKSUMS_FILE_NAME, URLS_CHECKSUMS_FOLDER_NAME
from .utils.download_manager import GenerateMode
from .utils.file_utils import DownloadConfig, cached_path, hf_bucket_url


logger = logging.getLogger(__name__)

CURRENT_FILE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DATASETS_PATH = os.path.join(CURRENT_FILE_DIRECTORY, "datasets")
DATASETS_MODULE = "nlp.datasets"
METRICS_PATH = os.path.join(CURRENT_FILE_DIRECTORY, "metrics")
METRICS_MODULE = "nlp.metrics"


def import_main_class(module_path, dataset=True):
    """ Load the module """
    importlib.invalidate_caches()
    module = importlib.import_module(module_path)

    if dataset:
        main_cls_type = DatasetBuilder
    else:
        main_cls_type = Metric

    # Find the main class in our imported module
    module_main_cls = None
    for name, obj in module.__dict__.items():
        if isinstance(obj, type) and issubclass(obj, main_cls_type):
            module_main_cls = obj
            break

    return module_main_cls


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


def convert_github_url(url_path: str):
    parsed = urlparse(url_path)
    if parsed.scheme in ("http", "https", "s3") and parsed.netloc == "github.com":
        assert url_path.endswith(".py"), "External import from gitbhu should direcly point to a file ending with '.py'"
        assert "blob" in url_path, "External import from gitbhu should direcly point to a file"
        url_path = url_path.replace("blob", "raw")  # Point to the raw file
    return url_path


def get_imports(file_path: str):
    """ Find whether we should import or clone additional files for a given processing script.
        And list the import.

        We allow:
        - local dependencies and
        - external dependencies whose url is specified with a comment starting from "# From:' followed by the raw url to a file, an archive or a github repository.
            external dependencies will be downloaded (and extracted if needed in the dataset folder).
            We also add an `__init__.py` to each sub-folder of a downloaded folder so the user can import from them in the script.

        Note that only direct import in the dataset processing script will be handled
        We don't recursively explore the additional import to download further files.

        ```python
        import .c4_utils
        import .clicr.dataset-code.build_json_dataset  # From: https://raw.githubusercontent.com/clips/clicr/master/dataset-code/build_json_dataset
        ```
    """
    lines = []
    with open(file_path, mode="r") as f:
        lines.extend(f.readlines())

    logger.info("Checking %s for additional imports.", file_path)
    imports = []
    for line in lines:
        match = re.match(r"^import\s+(\.?)([^\s\.]+)[^#\r\n]*(?:#\s+From:\s+)?([^\r\n]*)", line, flags=re.MULTILINE)
        if match is None:
            match = re.match(
                r"^from\s+(\.?)([^\s\.]+)(?:[^\s]*)\s+import\s+[^#\r\n]*(?:#\s+From:\s+)?([^\r\n]*)",
                line,
                flags=re.MULTILINE,
            )
            if match is None:
                continue
        if match.group(1):
            # The import starts with a '.', we will download the relevant file
            if match.group(3):
                # The import has a comment with 'From:', we'll retreive it from the given url
                url_path = match.group(3)
                url_path = convert_github_url(url_path)
                imports.append(("external", match.group(2), url_path))
            elif match.group(2):
                # The import should be at the same place as the file
                imports.append(("internal", match.group(2), match.group(2)))
        else:
            imports.append(("library", match.group(2), match.group(2)))

    return imports


def prepare_module(path: str, download_config=None, dataset=True, **download_kwargs,) -> DatasetBuilder:
    r"""
        Download/extract/cache a dataset (if dataset==True) or a metric (if dataset==False)
        to add to the lib from a path or url which can be:
            - a path to a local directory containing the dataset processing python script
            - an url to a S3 directory with a dataset processing python script

        Dataset and metrics codes are cached inside the lib to allow easy import (avoid ugly sys.path tweaks)
        and using cloudpickle (among other things).

        Return: tuple of
            the unique id associated to the dataset/metric
            the local path to the dataset/metric
    """
    if download_config is None:
        download_config = DownloadConfig(**download_kwargs)
    download_config.extract_compressed_file = True
    download_config.force_extract = True

    module_type = "dataset" if dataset else "metric"
    name = list(filter(lambda x: x, path.split("/")))[-1]
    if not name.endswith(".py"):
        name = name + ".py"

    # Short name is name without the '.py' at the end (for the module)
    short_name = name[:-3]

    # We have three ways to find the processing file:
    # - if os.path.join(path, name) is a file or a remote url
    # - if path is a file or a remote url
    # - otherwise we assume path/name is a path to our S3 bucket
    combined_path = os.path.join(path, name)
    if os.path.isfile(combined_path):
        file_path = combined_path
    elif os.path.isfile(path):
        file_path = path
    else:
        file_path = hf_bucket_url(path, filename=name, dataset=dataset)

    base_path = os.path.dirname(file_path)  # remove the filename
    checksums_file = os.path.join(base_path, URLS_CHECKSUMS_FOLDER_NAME, CHECKSUMS_FILE_NAME)

    # Load the module in two steps:
    # 1. get the processing file on the local filesystem if it's not there (download to cache dir)
    # 2. copy from the local file system inside the library to import it
    local_path = cached_path(file_path, download_config=download_config)

    # Download the checksums file if available
    try:
        local_checksums_file_path = cached_path(checksums_file, download_config=download_config,)
    except (FileNotFoundError, ConnectionError):
        local_checksums_file_path = None

    # Download external imports if needed
    imports = get_imports(local_path)
    local_imports = []
    library_imports = []
    for import_type, import_name, import_path in imports:
        if import_type == "library":
            library_imports.append(import_name)  # Import from a library
            continue

        if import_name == short_name:
            raise ValueError(
                f"Error in {module_type} script at {file_path}, importing relative {import_name} module "
                f"but {import_name} is the name of the {module_type} script. "
                f"Please change relative import {import_name} to another name and add a '# From: URL_OR_PATH' "
                f"comment pointing to the original realtive import file path."
            )
        if import_type == "internal":
            url_or_filename = base_path + "/" + import_path + ".py"
        elif import_type == "external":
            url_or_filename = import_path
        else:
            raise ValueError("Wrong import_type")

        local_import_path = cached_path(url_or_filename, download_config=download_config,)
        local_imports.append((import_name, local_import_path))

    # Check library imports
    needs_to_be_installed = []
    for library_import in library_imports:
        try:
            lib = importlib.import_module(library_import)  # noqa F841
        except ImportError:
            needs_to_be_installed.append(library_import)
    if needs_to_be_installed:
        raise ImportError(
            f"To be able to use this {module_type}, you need to install the following dependencies {needs_to_be_installed} "
            f"using 'pip install {' '.join(needs_to_be_installed)}' for instance'"
        )

    # Define a directory with a unique name in our dataset or metric folder
    # path is: ./datasets|metrics/dataset|metric_name/hash_from_code/script.py
    # we use a hash to be able to have multiple versions of a dataset/metric processing file together
    hash = files_to_hash([local_path] + [loc[1] for loc in local_imports])
    main_folder_path = os.path.join(DATASETS_PATH if dataset else METRICS_PATH, short_name)
    hash_folder_path = os.path.join(main_folder_path, hash)
    local_file_path = os.path.join(hash_folder_path, name)
    urls_checksums_dir = os.path.join(hash_folder_path, URLS_CHECKSUMS_FOLDER_NAME)
    checksums_file_path = os.path.join(urls_checksums_dir, CHECKSUMS_FILE_NAME)

    # Prevent parallel disk operations
    lock_path = local_path + ".lock"
    with FileLock(lock_path):
        # Create main dataset/metrics folder if needed
        if not os.path.exists(main_folder_path):
            logger.info(f"Creating main folder for {module_type} {file_path} at {main_folder_path}")
            os.makedirs(main_folder_path, exist_ok=True)
        else:
            logger.info(f"Found main folder for {module_type} {file_path} at {main_folder_path}")

        # add an __init__ file to the main dataset folder if needed
        init_file_path = os.path.join(main_folder_path, "__init__.py")
        if not os.path.exists(init_file_path):
            with open(init_file_path, "w"):
                pass

        # Create hash dataset folder if needed
        if not os.path.exists(hash_folder_path):
            logger.info(f"Creating specific version folder for {module_type} {file_path} at {hash_folder_path}")
            os.makedirs(hash_folder_path)
        else:
            logger.info(f"Found specific version folder for {module_type} {file_path} at {hash_folder_path}")

        # add an __init__ file to the hash dataset folder if needed
        init_file_path = os.path.join(hash_folder_path, "__init__.py")
        if not os.path.exists(init_file_path):
            with open(init_file_path, "w"):
                pass

        # Copy dataset.py file in hash folder if needed
        if not os.path.exists(local_file_path):
            logger.info("Copying script file from %s to %s", file_path, local_file_path)
            shutil.copyfile(local_path, local_file_path)
        else:
            logger.info("Found script file from %s to %s", file_path, local_file_path)

        # Copy checksums file if needed
        os.makedirs(urls_checksums_dir, exist_ok=True)
        if not os.path.exists(checksums_file_path):
            if local_checksums_file_path is not None:
                logger.info("Copying checksums file from %s to %s", checksums_file, checksums_file_path)
                shutil.copyfile(local_checksums_file_path, checksums_file_path)
            else:
                logger.info("Couldn't find checksums file at %s", checksums_file)
        else:
            logger.info("Found checksums file from %s to %s", checksums_file, checksums_file_path)

        # Record metadata associating original dataset path with local unique folder
        meta_path = local_file_path.split(".py")[0] + ".json"
        if not os.path.exists(meta_path):
            logger.info(f"Creating metadata file for {module_type} {file_path} at {meta_path}")
            meta = {"original file path": file_path, "local file path": local_file_path}
            # the filename is *.py in our case, so better rename to filenam.json instead of filename.py.json
            with open(meta_path, "w") as meta_file:
                json.dump(meta, meta_file)
        else:
            logger.info(f"Found metadata file for {module_type} {file_path} at {meta_path}")

        # Copy all the additional imports
        for import_name, import_path in local_imports:
            full_path_local_import = os.path.join(hash_folder_path, import_name + ".py")
            if not os.path.exists(full_path_local_import):
                logger.info("Copying local import from %s at %s", import_path, full_path_local_import)
                shutil.copyfile(import_path, full_path_local_import)
            else:
                logger.info("Found local import from %s at %s", import_path, full_path_local_import)

    module_path = ".".join([DATASETS_MODULE if dataset else METRICS_MODULE, short_name, hash, short_name])
    return module_path


def load_metric(
    path: str,
    name: Optional[str] = None,
    process_id: int = 0,
    num_process: int = 1,
    data_dir: Optional[str] = None,
    experiment_id: Optional[str] = None,
    in_memory: bool = False,
    download_config: Optional[DownloadConfig] = None,
    **metric_init_kwargs,
) -> Metric:
    """Fetches a `nlp.Metric` by string name.

    Args:
        name: `str`, the name of the `Metric` (the snake case
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
        A `nlp.Metric`.

    Raises:
        MetricNotFoundError: if `name` is unrecognized.
    """
    # Download/copy metric script
    module_path = prepare_module(path, download_config=download_config, dataset=False)
    metric_cls = import_main_class(module_path, dataset=False)
    metric = metric_cls(
        name=name,
        process_id=process_id,
        num_process=num_process,
        data_dir=data_dir,
        experiment_id=experiment_id,
        in_memory=in_memory,
        **metric_init_kwargs,
    )
    return metric


def load_dataset(
    path: str,
    split: Optional[Union[str, Split]] = None,
    name: Optional[str] = None,
    version: Optional[str] = None,
    description: Optional[str] = None,
    data_dir: Optional[str] = None,
    data_files: Union[Dict, List] = None,
    dataset_config: Optional[BuilderConfig] = None,
    download_config: Optional[DownloadConfig] = None,
    download_mode: Optional[GenerateMode] = None,
    ignore_checksums: bool = False,
    save_checksums: bool = False,
    **config_kwargs,
) -> Dataset:
    """ Load a dataset.

    This method does the following under the hood:
        1. Download and import in the library the dataset loading script from ``path`` if it's not already cached inside the library.

            Processing scripts are small python scripts that define the citation, info and format of the dataset,
            contain the URL to the original data files and the code to load examples from the original data files.

            You can find some of the scripts here: https://github.com/huggingface/nlp/datasets
            and easily upload yours to share them using the CLI ``nlp-cli``.

        2. Run the dataset loading script which will:

            * Download the dataset file from the original URL (see the script) if it's not already downloaded and cached.
            * Process and cache the dataset in typed Arrow tables for caching.

                Arrow table are arbitrarly long, typed tables which can store nested objects and be mapped to numpy/pandas/python standard types.
                They can be directly access from drive, loaded in RAM or even streamed over the web.

        3. Return a dataset build from the requested splits in ``split`` (default: all).

    Args:
        path: `str`, the name of the `Dataset` (the snake case
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
    module_path = prepare_module(path, download_config=download_config, dataset=True)

    # Get dataset builder class
    builder_cls = import_main_class(module_path, dataset=True)

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
