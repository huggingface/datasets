# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the TensorFlow Datasets Authors.
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
import filecmp
import importlib
import inspect
import json
import os
import re
import shutil
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Type, Union
from urllib.parse import urlparse

import fsspec

from . import config
from .arrow_dataset import Dataset
from .builder import DatasetBuilder
from .dataset_dict import DatasetDict, IterableDatasetDict
from .features import Features
from .filesystems import extract_path_from_uri, is_remote_filesystem
from .iterable_dataset import IterableDataset
from .metric import Metric
from .packaged_modules import _PACKAGED_DATASETS_MODULES, hash_python_lines
from .splits import Split
from .tasks import TaskTemplate
from .utils.download_manager import GenerateMode
from .utils.file_utils import (
    DownloadConfig,
    cached_path,
    head_hf_s3,
    hf_bucket_url,
    hf_github_url,
    hf_hub_url,
    init_hf_modules,
    url_or_path_join,
    url_or_path_parent,
)
from .utils.filelock import FileLock
from .utils.info_utils import is_small_dataset
from .utils.logging import get_logger
from .utils.version import Version


if config.AIOHTTP_AVAILABLE:
    from .streaming import extend_module_for_streaming


logger = get_logger(__name__)


def init_dynamic_modules(
    name: str = config.MODULE_NAME_FOR_DYNAMIC_MODULES, hf_modules_cache: Optional[Union[Path, str]] = None
):
    """
    Create a module with name `name` in which you can add dynamic modules
    such as metrics or datasets. The module can be imported using its name.
    The module is created in the HF_MODULE_CACHE directory by default (~/.cache/huggingface/modules) but it can
    be overriden by specifying a path to another directory in `hf_modules_cache`.
    """
    hf_modules_cache = init_hf_modules(hf_modules_cache)
    dynamic_modules_path = os.path.join(hf_modules_cache, name)
    os.makedirs(dynamic_modules_path, exist_ok=True)
    if not os.path.exists(os.path.join(dynamic_modules_path, "__init__.py")):
        with open(os.path.join(dynamic_modules_path, "__init__.py"), "w"):
            pass
    return dynamic_modules_path


def import_main_class(module_path, dataset=True) -> Optional[Union[Type[DatasetBuilder], Type[Metric]]]:
    """Import a module at module_path and return its main class:
    - a DatasetBuilder if dataset is True
    - a Metric if dataset is False
    """
    module = importlib.import_module(module_path)

    if dataset:
        main_cls_type = DatasetBuilder
    else:
        main_cls_type = Metric

    # Find the main class in our imported module
    module_main_cls = None
    for name, obj in module.__dict__.items():
        if isinstance(obj, type) and issubclass(obj, main_cls_type):
            if inspect.isabstract(obj):
                continue
            module_main_cls = obj
            break

    return module_main_cls


def files_to_hash(file_paths: List[str]) -> str:
    """
    Convert a list of scripts or text files provided in file_paths into a hashed filename in a repeatable way.
    """
    # List all python files in directories if directories are supplied as part of external imports
    to_use_files: List[Union[Path, str]] = []
    for file_path in file_paths:
        if os.path.isdir(file_path):
            to_use_files.extend(list(Path(file_path).rglob("*.[pP][yY]")))
        else:
            to_use_files.append(file_path)

    # Get the code from all these files
    lines = []
    for file_path in to_use_files:
        with open(file_path, mode="r", encoding="utf-8") as f:
            lines.extend(f.readlines())
    return hash_python_lines(lines)


def convert_github_url(url_path: str) -> Tuple[str, Optional[str]]:
    """Convert a link to a file on a github repo in a link to the raw github object."""
    parsed = urlparse(url_path)
    sub_directory = None
    if parsed.scheme in ("http", "https", "s3") and parsed.netloc == "github.com":
        if "blob" in url_path:
            assert url_path.endswith(
                ".py"
            ), f"External import from github at {url_path} should point to a file ending with '.py'"
            url_path = url_path.replace("blob", "raw")  # Point to the raw file
        else:
            # Parse github url to point to zip
            github_path = parsed.path[1:]
            repo_info, branch = github_path.split("/tree/") if "/tree/" in github_path else (github_path, "master")
            repo_owner, repo_name = repo_info.split("/")
            url_path = "https://github.com/{}/{}/archive/{}.zip".format(repo_owner, repo_name, branch)
            sub_directory = f"{repo_name}-{branch}"
    return url_path, sub_directory


def get_imports(file_path: str):
    r"""Find whether we should import or clone additional files for a given processing script.
        And list the import.

    We allow:
    - library dependencies,
    - local dependencies and
    - external dependencies whose url is specified with a comment starting from "# From:' followed by the raw url to a file, an archive or a github repository.
        external dependencies will be downloaded (and extracted if needed in the dataset folder).
        We also add an `__init__.py` to each sub-folder of a downloaded folder so the user can import from them in the script.

    Note that only direct import in the dataset processing script will be handled
    We don't recursively explore the additional import to download further files.

    Examples::

        import tensorflow
        import .c4_utils
        import .clicr.dataset-code.build_json_dataset  # From: https://raw.githubusercontent.com/clips/clicr/master/dataset-code/build_json_dataset
    """
    lines = []
    with open(file_path, mode="r", encoding="utf-8") as f:
        lines.extend(f.readlines())

    logger.debug("Checking %s for additional imports.", file_path)
    imports: List[Tuple[str, str, str, Optional[str]]] = []
    is_in_docstring = False
    for line in lines:
        docstr_start_match = re.findall(r'[\s\S]*?"""[\s\S]*?', line)

        if len(docstr_start_match) == 1:
            # flip True <=> False only if doctstring
            # starts at line without finishing
            is_in_docstring = not is_in_docstring

        if is_in_docstring:
            # import statements in doctstrings should
            # not be added as required dependencies
            continue

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
            if any(imp[1] == match.group(2) for imp in imports):
                # We already have this import
                continue
            if match.group(3):
                # The import has a comment with 'From:', we'll retrieve it from the given url
                url_path = match.group(3)
                url_path, sub_directory = convert_github_url(url_path)
                imports.append(("external", match.group(2), url_path, sub_directory))
            elif match.group(2):
                # The import should be at the same place as the file
                imports.append(("internal", match.group(2), match.group(2), None))
        else:
            if match.group(3):
                # The import has a comment with `From: git+https:...`, asks user to pip install from git.
                url_path = match.group(3)
                imports.append(("library", match.group(2), url_path, None))
            else:
                imports.append(("library", match.group(2), match.group(2), None))

    return imports


def prepare_module(
    path: str,
    script_version: Optional[Union[str, Version]] = None,
    download_config: Optional[DownloadConfig] = None,
    download_mode: Optional[GenerateMode] = None,
    dataset: bool = True,
    force_local_path: Optional[str] = None,
    dynamic_modules_path: Optional[str] = None,
    return_resolved_file_path: bool = False,
    **download_kwargs,
) -> Union[Tuple[str, str], Tuple[str, str, Optional[str]]]:
    r"""
        Download/extract/cache a dataset (if dataset==True) or a metric (if dataset==False)

    Dataset and metrics codes are cached inside the the dynamic modules cache to allow easy import (avoid ugly sys.path tweaks)
    and using cloudpickle (among other things).

    Args:

        path (str):
            path to the dataset or metric script, can be either:
                - a path to a local directory containing the dataset processing python script
                - an url to a github or S3 directory with a dataset processing python script
        script_version (Optional ``Union[str, datasets.Version]``):
            If specified, the module will be loaded from the datasets repository at this version.
            By default:
            - it is set to the local version fo the lib.
            - it will also try to load it from the master branch if it's not available at the local version fo the lib.
            Specifying a version that is different from your local version of the lib might cause compatibility issues.
        download_config (Optional ``datasets.DownloadConfig``: specific download configuration parameters.
        dataset (bool): True if the script to load is a dataset, False if the script is a metric.
        force_local_path (Optional str): Optional path to a local path to download and prepare the script to.
            Used to inspect or modify the script folder.
        dynamic_modules_path (Optional str, defaults to HF_MODULES_CACHE / "datasets_modules", i.e. ~/.cache/huggingface/modules/datasets_modules):
            Optional path to the directory in which the dynamic modules are saved. It must have been initialized with :obj:`init_dynamic_modules`.
            By default the datasets and metrics are stored inside the `datasets_modules` module.
        return_resolved_file_path (Optional bool, defaults to False):
            If True, the url or path to the resolved dataset or metric script is returned with the other ouputs
        download_kwargs: optional attributes for DownloadConfig() which will override the attributes in download_config if supplied.

    Return: Tuple[``str``, ``str``] with
        1. The module path being
            - the import path of the dataset/metric package if force_local_path is False: e.g. 'datasets.datasets.squad'
            - the local path to the dataset/metric file if force_local_path is True: e.g. '/User/huggingface/datasets/datasets/squad/squad.py'
        2. A hash string computed from the content of the dataset loading script.
    """
    if download_config is None:
        download_config = DownloadConfig(**download_kwargs)
    download_config.extract_compressed_file = True
    download_config.force_extract = True

    module_type = "dataset" if dataset else "metric"
    name = list(filter(lambda x: x, path.replace(os.sep, "/").split("/")))[-1]
    if not name.endswith(".py"):
        name = name + ".py"

    # Short name is name without the '.py' at the end (for the module)
    short_name = name[:-3]

    # first check if the module is packaged with the `datasets` package
    if dataset and path in _PACKAGED_DATASETS_MODULES:
        try:
            head_hf_s3(path, filename=name, dataset=dataset, max_retries=download_config.max_retries)
        except Exception:
            logger.debug(f"Couldn't head HF s3 for packaged dataset module '{path}'. Running in offline mode.")
        module_path, hash = _PACKAGED_DATASETS_MODULES[path]
        if return_resolved_file_path:
            return module_path, hash, None
        return module_path, hash

    # otherwise the module is added to the dynamic modules
    dynamic_modules_path = dynamic_modules_path if dynamic_modules_path else init_dynamic_modules()
    module_name_for_dynamic_modules = os.path.basename(dynamic_modules_path)
    datasets_modules_path = os.path.join(dynamic_modules_path, "datasets")
    datasets_modules_name = module_name_for_dynamic_modules + ".datasets"
    metrics_modules_path = os.path.join(dynamic_modules_path, "metrics")
    metrics_modules_name = module_name_for_dynamic_modules + ".metrics"

    if force_local_path is None:
        main_folder_path = os.path.join(datasets_modules_path if dataset else metrics_modules_path, short_name)
    else:
        main_folder_path = force_local_path

    # We have three ways to find the processing file:
    # - if os.path.join(path, name) is a file or a remote url
    # - if path is a file or a remote url
    # - otherwise we assume path/name is a path to our S3 bucket
    combined_path = os.path.join(path, name)
    if os.path.isfile(combined_path):
        file_path = combined_path
        local_path = file_path
    elif os.path.isfile(path):
        file_path = path
        local_path = path
    else:
        # Try github (canonical datasets/metrics) and then S3 (users datasets/metrics)
        try:
            head_hf_s3(path, filename=name, dataset=dataset, max_retries=download_config.max_retries)
            script_version = str(script_version) if script_version is not None else None
            if path.count("/") == 0:  # canonical datasets/metrics: github path
                file_path = hf_github_url(path=path, name=name, dataset=dataset, version=script_version)
                try:
                    local_path = cached_path(file_path, download_config=download_config)
                except FileNotFoundError:
                    if script_version is not None:
                        raise FileNotFoundError(
                            "Couldn't find remote file with version {} at {}. Please provide a valid version and a valid {} name".format(
                                script_version, file_path, "dataset" if dataset else "metric"
                            )
                        )
                    else:
                        github_file_path = file_path
                        file_path = hf_github_url(path=path, name=name, dataset=dataset, version="master")
                        try:
                            local_path = cached_path(file_path, download_config=download_config)
                            logger.warning(
                                "Couldn't find file locally at {}, or remotely at {}.\n"
                                "The file was picked from the master branch on github instead at {}.".format(
                                    combined_path, github_file_path, file_path
                                )
                            )
                        except FileNotFoundError:
                            raise FileNotFoundError(
                                "Couldn't find file locally at {}, or remotely at {}.\n"
                                "The file is also not present on the master branch on github.".format(
                                    combined_path, github_file_path
                                )
                            )
            elif path.count("/") == 1:  # users datasets/metrics: s3 path (hub for datasets and s3 for metrics)
                if dataset:
                    file_path = hf_hub_url(path=path, name=name, version=script_version)
                else:
                    file_path = hf_bucket_url(path, filename=name, dataset=False)
                try:
                    local_path = cached_path(file_path, download_config=download_config)
                except FileNotFoundError:
                    raise FileNotFoundError(
                        "Couldn't find file locally at {}, or remotely at {}. Please provide a valid {} name".format(
                            combined_path, file_path, "dataset" if dataset else "metric"
                        )
                    )
            else:
                raise FileNotFoundError(
                    "Couldn't find file locally at {}. Please provide a valid {} name".format(
                        combined_path, "dataset" if dataset else "metric"
                    )
                )
        except Exception as e:  # noqa: all the attempts failed, before raising the error we should check if the module already exists.
            if os.path.isdir(main_folder_path):
                hashes = [h for h in os.listdir(main_folder_path) if len(h) == 64]
                if hashes:
                    # get most recent
                    def _get_modification_time(module_hash):
                        return (Path(main_folder_path) / module_hash / name).stat().st_mtime

                    hash = sorted(hashes, key=_get_modification_time)[-1]
                    module_path = ".".join(
                        [datasets_modules_name if dataset else metrics_modules_name, short_name, hash, short_name]
                    )
                    logger.warning(
                        f"Using the latest cached version of the module from {os.path.join(main_folder_path, hash)} "
                        f"(last modified on {time.ctime(_get_modification_time(hash))}) since it "
                        f"couldn't be found locally at {combined_path} or remotely ({type(e).__name__})."
                    )
                    if return_resolved_file_path:
                        with open(os.path.join(main_folder_path, hash, short_name + ".json")) as cache_metadata:
                            file_path = json.load(cache_metadata)["original file path"]
                        return module_path, hash, file_path
                    return module_path, hash
            raise

    # Load the module in two steps:
    # 1. get the processing file on the local filesystem if it's not there (download to cache dir)
    # 2. copy from the local file system inside the modules cache to import it

    base_path = url_or_path_parent(file_path)  # remove the filename
    dataset_infos = url_or_path_join(base_path, config.DATASETDICT_INFOS_FILENAME)

    # Download the dataset infos file if available
    try:
        local_dataset_infos_path = cached_path(
            dataset_infos,
            download_config=download_config,
        )
    except (FileNotFoundError, ConnectionError):
        local_dataset_infos_path = None

    # Download external imports if needed
    imports = get_imports(local_path)
    local_imports = []
    library_imports = []
    for import_type, import_name, import_path, sub_directory in imports:
        if import_type == "library":
            library_imports.append((import_name, import_path))  # Import from a library
            continue

        if import_name == short_name:
            raise ValueError(
                f"Error in {module_type} script at {file_path}, importing relative {import_name} module "
                f"but {import_name} is the name of the {module_type} script. "
                f"Please change relative import {import_name} to another name and add a '# From: URL_OR_PATH' "
                f"comment pointing to the original realtive import file path."
            )
        if import_type == "internal":
            url_or_filename = url_or_path_join(base_path, import_path + ".py")
        elif import_type == "external":
            url_or_filename = import_path
        else:
            raise ValueError("Wrong import_type")

        local_import_path = cached_path(
            url_or_filename,
            download_config=download_config,
        )
        if sub_directory is not None:
            local_import_path = os.path.join(local_import_path, sub_directory)
        local_imports.append((import_name, local_import_path))

    # Check library imports
    needs_to_be_installed = []
    for library_import_name, library_import_path in library_imports:
        try:
            lib = importlib.import_module(library_import_name)  # noqa F841
        except ImportError:
            needs_to_be_installed.append((library_import_name, library_import_path))
    if needs_to_be_installed:
        raise ImportError(
            f"To be able to use this {module_type}, you need to install the following dependencies"
            f"{[lib_name for lib_name, lib_path in needs_to_be_installed]} using 'pip install "
            f"{' '.join([lib_path for lib_name, lib_path in needs_to_be_installed])}' for instance'"
        )

    # Define a directory with a unique name in our dataset or metric folder
    # path is: ./datasets|metrics/dataset|metric_name/hash_from_code/script.py
    # we use a hash to be able to have multiple versions of a dataset/metric processing file together
    hash = files_to_hash([local_path] + [loc[1] for loc in local_imports])

    if force_local_path is None:
        hash_folder_path = os.path.join(main_folder_path, hash)
    else:
        hash_folder_path = force_local_path

    local_file_path = os.path.join(hash_folder_path, name)
    dataset_infos_path = os.path.join(hash_folder_path, config.DATASETDICT_INFOS_FILENAME)

    # Prevent parallel disk operations
    lock_path = local_path + ".lock"
    with FileLock(lock_path):
        # Create main dataset/metrics folder if needed
        if download_mode == GenerateMode.FORCE_REDOWNLOAD and os.path.exists(main_folder_path):
            shutil.rmtree(main_folder_path)

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

        # Copy dataset infos file if needed
        if not os.path.exists(dataset_infos_path):
            if local_dataset_infos_path is not None:
                logger.info("Copying dataset infos file from %s to %s", dataset_infos, dataset_infos_path)
                shutil.copyfile(local_dataset_infos_path, dataset_infos_path)
            else:
                logger.info("Couldn't find dataset infos file at %s", dataset_infos)
        else:
            if local_dataset_infos_path is not None and not filecmp.cmp(local_dataset_infos_path, dataset_infos_path):
                logger.info("Updating dataset infos file from %s to %s", dataset_infos, dataset_infos_path)
                shutil.copyfile(local_dataset_infos_path, dataset_infos_path)
            else:
                logger.info("Found dataset infos file from %s to %s", dataset_infos, dataset_infos_path)

        # Record metadata associating original dataset path with local unique folder
        meta_path = local_file_path.split(".py")[0] + ".json"
        if not os.path.exists(meta_path):
            logger.info(f"Creating metadata file for {module_type} {file_path} at {meta_path}")
            meta = {"original file path": file_path, "local file path": local_file_path}
            # the filename is *.py in our case, so better rename to filenam.json instead of filename.py.json
            with open(meta_path, "w", encoding="utf-8") as meta_file:
                json.dump(meta, meta_file)
        else:
            logger.info(f"Found metadata file for {module_type} {file_path} at {meta_path}")

        # Copy all the additional imports
        for import_name, import_path in local_imports:
            if os.path.isfile(import_path):
                full_path_local_import = os.path.join(hash_folder_path, import_name + ".py")
                if not os.path.exists(full_path_local_import):
                    logger.info("Copying local import file from %s at %s", import_path, full_path_local_import)
                    shutil.copyfile(import_path, full_path_local_import)
                else:
                    logger.info("Found local import file from %s at %s", import_path, full_path_local_import)
            elif os.path.isdir(import_path):
                full_path_local_import = os.path.join(hash_folder_path, import_name)
                if not os.path.exists(full_path_local_import):
                    logger.info("Copying local import directory from %s at %s", import_path, full_path_local_import)
                    shutil.copytree(import_path, full_path_local_import)
                else:
                    logger.info("Found local import directory from %s at %s", import_path, full_path_local_import)
            else:
                raise OSError(f"Error with local import at {import_path}")

    if force_local_path is None:
        module_path = ".".join(
            [datasets_modules_name if dataset else metrics_modules_name, short_name, hash, short_name]
        )
    else:
        module_path = local_file_path

    # make the new module to be noticed by the import system
    importlib.invalidate_caches()

    if return_resolved_file_path:
        return module_path, hash, file_path
    return module_path, hash


def load_metric(
    path: str,
    config_name: Optional[str] = None,
    process_id: int = 0,
    num_process: int = 1,
    cache_dir: Optional[str] = None,
    experiment_id: Optional[str] = None,
    keep_in_memory: bool = False,
    download_config: Optional[DownloadConfig] = None,
    download_mode: Optional[GenerateMode] = None,
    script_version: Optional[Union[str, Version]] = None,
    **metric_init_kwargs,
) -> Metric:
    r"""Load a `datasets.Metric`.

    Args:

        path (``str``):
            path to the metric processing script with the metric builder. Can be either:
                - a local path to processing script or the directory containing the script (if the script has the same name as the directory),
                    e.g. ``'./metrics/rouge'`` or ``'./metrics/rogue/rouge.py'``
                - a metric identifier on the HuggingFace datasets repo (list all available metrics with ``datasets.list_metrics()``)
                    e.g. ``'rouge'`` or ``'bleu'``
        config_name (Optional ``str``): selecting a configuration for the metric (e.g. the GLUE metric has a configuration for each subset)
        process_id (Optional ``int``): for distributed evaluation: id of the process
        num_process (Optional ``int``): for distributed evaluation: total number of processes
        cache_dir (Optional str): path to store the temporary predictions and references (default to `~/.cache/metrics/`)
        experiment_id (``str``): A specific experiment id. This is used if several distributed evaluations share the same file system.
            This is useful to compute metrics in distributed setups (in particular non-additive metrics like F1).
        keep_in_memory (bool): Whether to store the temporary results in memory (defaults to False)
        download_config (Optional ``datasets.DownloadConfig``: specific download configuration parameters.
        download_mode (Optional `datasets.GenerateMode`): select the download/generate mode - Default to REUSE_DATASET_IF_EXISTS
        script_version (Optional ``Union[str, datasets.Version]``): if specified, the module will be loaded from the datasets repository
            at this version. By default it is set to the local version fo the lib. Specifying a version that is different from
            your local version of the lib might cause compatibility issues.

    Returns:
        `datasets.Metric`
    """
    module_path, _ = prepare_module(
        path,
        script_version=script_version,
        download_config=download_config,
        download_mode=download_mode,
        dataset=False,
    )
    metric_cls = import_main_class(module_path, dataset=False)
    metric = metric_cls(
        config_name=config_name,
        process_id=process_id,
        num_process=num_process,
        cache_dir=cache_dir,
        keep_in_memory=keep_in_memory,
        experiment_id=experiment_id,
        **metric_init_kwargs,
    )

    # Download and prepare resources for the metric
    metric.download_and_prepare(download_config=download_config)

    return metric


def load_dataset_builder(
    path: str,
    name: Optional[str] = None,
    data_dir: Optional[str] = None,
    data_files: Union[Dict, List] = None,
    cache_dir: Optional[str] = None,
    features: Optional[Features] = None,
    download_config: Optional[DownloadConfig] = None,
    download_mode: Optional[GenerateMode] = None,
    script_version: Optional[Union[str, Version]] = None,
    use_auth_token: Optional[Union[bool, str]] = None,
    **config_kwargs,
) -> DatasetBuilder:
    """Load a builder for the dataset. A dataset builder can be used to inspect general information that is required to build a dataset (cache directory, config, dataset info, etc.)
    without downloading the dataset itself.

    This method will download and import the dataset loading script from ``path`` if it's not already cached inside the library.

    Args:

        path (:obj:`str`): Path to the dataset processing script with the dataset builder. Can be either:

            - a local path to processing script or the directory containing the script (if the script has the same name as the directory),
              e.g. ``'./dataset/squad'`` or ``'./dataset/squad/squad.py'``.
            - a dataset identifier in the HuggingFace Datasets Hub (list all available datasets and ids with ``datasets.list_datasets()``)
              e.g. ``'squad'``, ``'glue'`` or ``'openai/webtext'``.
        name (:obj:`str`, optional): Defining the name of the dataset configuration.
        data_dir (:obj:`str`, optional): Defining the data_dir of the dataset configuration.
        data_files (:obj:`str`, optional): Defining the data_files of the dataset configuration.
        cache_dir (:obj:`str`, optional): Directory to read/write data. Defaults to "~/datasets".
        features (:class:`Features`, optional): Set the features type to use for this dataset.
        download_config (:class:`~utils.DownloadConfig`, optional): Specific download configuration parameters.
        download_mode (:class:`GenerateMode`, optional): Select the download/generate mode - Default to REUSE_DATASET_IF_EXISTS
        script_version (:class:`~utils.Version` or :obj:`str`, optional): Version of the dataset script to load:

            - For canonical datasets in the `huggingface/datasets` library like "squad", the default version of the module is the local version fo the lib.
              You can specify a different version from your local version of the lib (e.g. "master" or "1.2.0") but it might cause compatibility issues.
            - For community provided datasets like "lhoestq/squad" that have their own git repository on the Datasets Hub, the default version "main" corresponds to the "main" branch.
              You can specify a different version that the default "main" by using a commit sha or a git tag of the dataset repository.
        use_auth_token (``str`` or ``bool``, optional): Optional string or boolean to use as Bearer token for remote files on the Datasets Hub.
            If True, will get token from `"~/.huggingface"`.

    Returns:
        :class:`DatasetBuilder`

    """
    # Download/copy dataset processing script
    module_path, hash, resolved_file_path = prepare_module(
        path,
        script_version=script_version,
        download_config=download_config,
        download_mode=download_mode,
        dataset=True,
        return_resolved_file_path=True,
        use_auth_token=use_auth_token,
    )

    # Get dataset builder class from the processing script
    builder_cls = import_main_class(module_path, dataset=True)

    # Set the base path for downloads as the parent of the script location
    if resolved_file_path is not None:
        base_path = url_or_path_parent(resolved_file_path)
    else:
        base_path = None

    # Instantiate the dataset builder
    builder_instance: DatasetBuilder = builder_cls(
        cache_dir=cache_dir,
        name=name,
        data_dir=data_dir,
        data_files=data_files,
        hash=hash,
        base_path=base_path,
        features=features,
        use_auth_token=use_auth_token,
        **config_kwargs,
    )

    return builder_instance


def load_dataset(
    path: str,
    name: Optional[str] = None,
    data_dir: Optional[str] = None,
    data_files: Union[Dict, List] = None,
    split: Optional[Union[str, Split]] = None,
    cache_dir: Optional[str] = None,
    features: Optional[Features] = None,
    download_config: Optional[DownloadConfig] = None,
    download_mode: Optional[GenerateMode] = None,
    ignore_verifications: bool = False,
    keep_in_memory: Optional[bool] = None,
    save_infos: bool = False,
    script_version: Optional[Union[str, Version]] = None,
    use_auth_token: Optional[Union[bool, str]] = None,
    task: Optional[Union[str, TaskTemplate]] = None,
    streaming: bool = False,
    **config_kwargs,
) -> Union[DatasetDict, Dataset, IterableDatasetDict, IterableDataset]:
    """Load a dataset.

    This method does the following under the hood:

        1. Download and import in the library the dataset loading script from ``path`` if it's not already cached inside the library.

            Processing scripts are small python scripts that define the citation, info and format of the dataset,
            contain the URL to the original data files and the code to load examples from the original data files.

            You can find some of the scripts here: https://github.com/huggingface/datasets/datasets
            and easily upload yours to share them using the CLI ``huggingface-cli``.
            You can find the complete list of datasets in the Datasets Hub at https://huggingface.co/datasets

        2. Run the dataset loading script which will:

            * Download the dataset file from the original URL (see the script) if it's not already downloaded and cached.
            * Process and cache the dataset in typed Arrow tables for caching.

                Arrow table are arbitrarily long, typed tables which can store nested objects and be mapped to numpy/pandas/python standard types.
                They can be directly access from drive, loaded in RAM or even streamed over the web.

        3. Return a dataset built from the requested splits in ``split`` (default: all).

    Args:

        path (:obj:`str`): Path to the dataset processing script with the dataset builder. Can be either:

            - a local path to processing script or the directory containing the script (if the script has the same name as the directory),
              e.g. ``'./dataset/squad'`` or ``'./dataset/squad/squad.py'``.
            - a dataset identifier in the HuggingFace Datasets Hub (list all available datasets and ids with ``datasets.list_datasets()``)
              e.g. ``'squad'``, ``'glue'`` or ``'openai/webtext'``.
        name (:obj:`str`, optional): Defining the name of the dataset configuration.
        data_dir (:obj:`str`, optional): Defining the data_dir of the dataset configuration.
        data_files (:obj:`str`, optional): Defining the data_files of the dataset configuration.
        split (:class:`Split` or :obj:`str`): Which split of the data to load.
            If None, will return a `dict` with all splits (typically `datasets.Split.TRAIN` and `datasets.Split.TEST`).
            If given, will return a single Dataset.
            Splits can be combined and specified like in tensorflow-datasets.
        cache_dir (:obj:`str`, optional): Directory to read/write data. Defaults to "~/datasets".
        features (:class:`Features`, optional): Set the features type to use for this dataset.
        download_config (:class:`~utils.DownloadConfig`, optional): Specific download configuration parameters.
        download_mode (:class:`GenerateMode`, optional): Select the download/generate mode - Default to REUSE_DATASET_IF_EXISTS
        ignore_verifications (:obj:`bool`, default ``False``): Ignore the verifications of the downloaded/processed dataset information (checksums/size/splits/...).
        keep_in_memory (:obj:`bool`, default ``None``): Whether to copy the dataset in-memory. If `None`, the dataset
            will not be copied in-memory unless explicitly enabled by setting `datasets.config.IN_MEMORY_MAX_SIZE` to
            nonzero. See more details in the :ref:`load_dataset_enhancing_performance` section.
        save_infos (:obj:`bool`, default ``False``): Save the dataset information (checksums/size/splits/...).
        script_version (:class:`~utils.Version` or :obj:`str`, optional): Version of the dataset script to load:

            - For canonical datasets in the `huggingface/datasets` library like "squad", the default version of the module is the local version fo the lib.
              You can specify a different version from your local version of the lib (e.g. "master" or "1.2.0") but it might cause compatibility issues.
            - For community provided datasets like "lhoestq/squad" that have their own git repository on the Datasets Hub, the default version "main" corresponds to the "main" branch.
              You can specify a different version that the default "main" by using a commit sha or a git tag of the dataset repository.
        use_auth_token (``str`` or ``bool``, optional): Optional string or boolean to use as Bearer token for remote files on the Datasets Hub.
            If True, will get token from `"~/.huggingface"`.
        task (``str``): The task to prepare the dataset for during training and evaluation. Casts the dataset's :class:`Features` to standardized column names and types as detailed in :py:mod:`datasets.tasks`.
        streaming (``bool``, default ``False``): If set to True, don't download the data files. Instead, it streams the data progressively while
            iterating on the dataset. An IterableDataset or IterableDatasetDict is returned instead in this case.

            Note that streaming works for datasets that use data formats that support being iterated over like txt, csv, jsonl for example.
            Json files may be downloaded completely. Also streaming from remote zip or gzip files is supported but other compressed formats
            like rar and xz are not yet supported. The tgz format doesn't allow streaming.
        **config_kwargs: Keyword arguments to be passed to the :class:`BuilderConfig` and used in the :class:`DatasetBuilder`.

    Returns:
        :class:`Dataset` or :class:`DatasetDict`:
            if `split` is not None: the dataset requested,
            if `split` is None, a ``datasets.DatasetDict`` with each split.
        or :class:`IterableDataset` or :class:`IterableDatasetDict` if streaming=True:
            if `split` is not None: the dataset requested,
            if `split` is None, a ``datasets.streaming.IterableDatasetDict`` with each split.

    """
    ignore_verifications = ignore_verifications or save_infos
    # Check streaming
    if streaming:
        if not config.AIOHTTP_AVAILABLE:
            raise ImportError(
                f"To be able to use dataset streaming, you need to install dependencies like aiohttp "
                f"using 'pip install datasets[streaming]' or 'pip install aiohttp' for instance"
            )
    # Download/copy dataset processing script

    # Create a dataset builder
    builder_instance = load_dataset_builder(
        path,
        name,
        data_dir,
        data_files,
        cache_dir,
        features,
        download_config,
        download_mode,
        script_version,
        use_auth_token,
        **config_kwargs,
    )

    # Retturn iterable dataset in case of streaming
    if streaming:
        # this extends the open and os.path.join functions for data streaming
        extend_module_for_streaming(builder_instance.__module__, use_auth_token=use_auth_token)
        return builder_instance.as_streaming_dataset(
            split=split,
            use_auth_token=use_auth_token,
        )

    # Some datasets are already processed on the HF google storage
    # Don't try downloading from google storage for the packaged datasets as text, json, csv or pandas
    try_from_hf_gcs = path not in _PACKAGED_DATASETS_MODULES

    # Download and prepare data
    builder_instance.download_and_prepare(
        download_config=download_config,
        download_mode=download_mode,
        ignore_verifications=ignore_verifications,
        try_from_hf_gcs=try_from_hf_gcs,
        use_auth_token=use_auth_token,
    )

    # Build dataset for splits
    keep_in_memory = (
        keep_in_memory if keep_in_memory is not None else is_small_dataset(builder_instance.info.dataset_size)
    )
    ds = builder_instance.as_dataset(split=split, ignore_verifications=ignore_verifications, in_memory=keep_in_memory)
    # Rename and cast features to match task schema
    if task is not None:
        ds = ds.prepare_for_task(task)
    if save_infos:
        builder_instance._save_infos()

    return ds


def load_from_disk(dataset_path: str, fs=None, keep_in_memory: Optional[bool] = None) -> Union[Dataset, DatasetDict]:
    """
    Loads a dataset that was previously saved using ``dataset.save_to_disk(dataset_path)`` from a dataset directory, or from a filesystem using either :class:`datasets.filesystems.S3FileSystem` or any implementation of ``fsspec.spec.AbstractFileSystem``.

    Args:
        dataset_path (:obj:`str`): Path (e.g. ``"dataset/train"``) or remote uri (e.g.
            ``"s3://my-bucket/dataset/train"``) of the Dataset or DatasetDict directory where the dataset will be
            loaded from.
        fs (:class:`~filesystems.S3FileSystem` or ``fsspec.spec.AbstractFileSystem``, optional, default ``None``):
            Instance of of the remote filesystem used to download the files from.
        keep_in_memory (:obj:`bool`, default ``None``): Whether to copy the dataset in-memory. If `None`, the dataset
            will not be copied in-memory unless explicitly enabled by setting `datasets.config.IN_MEMORY_MAX_SIZE` to
            nonzero. See more details in the :ref:`load_dataset_enhancing_performance` section.

    Returns:
        ``datasets.Dataset`` or ``datasets.DatasetDict``
            if `dataset_path` is a path of a dataset directory: the dataset requested,
            if `dataset_path` is a path of a dataset dict directory: a ``datasets.DatasetDict`` with each split.
            keep_in_memory (``bool``, default False): Whether to copy the data in-memory.
    """
    # gets filesystem from dataset, either s3:// or file:// and adjusted dataset_path
    if is_remote_filesystem(fs):
        dest_dataset_path = extract_path_from_uri(dataset_path)
    else:
        fs = fsspec.filesystem("file")
        dest_dataset_path = dataset_path

    if not fs.exists(dest_dataset_path):
        raise FileNotFoundError("Directory {} not found".format(dataset_path))
    if fs.isfile(Path(dest_dataset_path, config.DATASET_INFO_FILENAME).as_posix()):
        return Dataset.load_from_disk(dataset_path, fs, keep_in_memory=keep_in_memory)
    elif fs.isfile(Path(dest_dataset_path, config.DATASETDICT_JSON_FILENAME).as_posix()):
        return DatasetDict.load_from_disk(dataset_path, fs, keep_in_memory=keep_in_memory)
    else:
        raise FileNotFoundError(
            "Directory {} is neither a dataset directory nor a dataset dict directory.".format(dataset_path)
        )
