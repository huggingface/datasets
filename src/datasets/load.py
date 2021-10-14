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
import warnings
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Sequence, Tuple, Type, Union
from urllib.parse import urlparse

import fsspec
import requests
from huggingface_hub import HfApi, HfFolder

from . import config
from .arrow_dataset import Dataset
from .builder import DatasetBuilder
from .data_files import DataFilesDict, DataFilesList, _sanitize_patterns
from .dataset_dict import DatasetDict, IterableDatasetDict
from .features import Features
from .filesystems import extract_path_from_uri, is_remote_filesystem
from .iterable_dataset import IterableDataset
from .metric import Metric
from .packaged_modules import _EXTENSION_TO_MODULE, _PACKAGED_DATASETS_MODULES, hash_python_lines
from .splits import Split
from .streaming import extend_module_for_streaming
from .tasks import TaskTemplate
from .utils.download_manager import GenerateMode
from .utils.file_utils import (
    DownloadConfig,
    OfflineModeIsEnabled,
    _raise_if_offline_mode_is_enabled,
    cached_path,
    head_hf_s3,
    hf_github_url,
    hf_hub_url,
    init_hf_modules,
    is_relative_path,
    relative_to_absolute_path,
    url_or_path_join,
)
from .utils.filelock import FileLock
from .utils.info_utils import is_small_dataset
from .utils.logging import get_logger
from .utils.streaming_download_manager import StreamingDownloadManager, xglob, xjoin
from .utils.version import Version


logger = get_logger(__name__)

DEFAULT_SPLIT = str(Split.TRAIN)

ALL_ALLOWED_EXTENSIONS = list(_EXTENSION_TO_MODULE.keys()) + ["zip"]


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


def increase_load_count(name: str, resource_type: str):
    """Update the download count of a dataset or metric."""
    if not config.HF_DATASETS_OFFLINE and config.HF_UPDATE_DOWNLOAD_COUNTS:
        try:
            head_hf_s3(name, filename=name + ".py", dataset=(resource_type == "dataset"))
        except Exception:
            pass


def get_imports(file_path: str) -> Tuple[str, str, str, str]:
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


def _download_additional_modules(
    name: str, base_path: str, imports: Tuple[str, str, str, str], download_config: Optional[DownloadConfig]
) -> List[Tuple[str, str]]:
    """
    Download additional module for a module <name>.py at URL (or local path) <base_path>/<name>.py
    The imports must have been parsed first using ``get_imports``.

    If some modules need to be installed with pip, an error is raised showing how to install them.
    This function return the list of downloaded modules as tuples (import_name, module_file_path).

    The downloaded modules can then be moved into an importable directory with ``_copy_script_and_other_resources_in_importable_dir``.
    """
    local_imports = []
    library_imports = []
    for import_type, import_name, import_path, sub_directory in imports:
        if import_type == "library":
            library_imports.append((import_name, import_path))  # Import from a library
            continue

        if import_name == name:
            raise ValueError(
                f"Error in the {name} script, importing relative {import_name} module "
                f"but {import_name} is the name of the script. "
                f"Please change relative import {import_name} to another name and add a '# From: URL_OR_PATH' "
                f"comment pointing to the original relative import file path."
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
            f"To be able to use {name}, you need to install the following dependencies"
            f"{[lib_name for lib_name, lib_path in needs_to_be_installed]} using 'pip install "
            f"{' '.join([lib_path for lib_name, lib_path in needs_to_be_installed])}' for instance'"
        )
    return local_imports


def _copy_script_and_other_resources_in_importable_dir(
    name: str,
    importable_directory_path: str,
    subdirectory_name: str,
    original_local_path: str,
    local_imports: List[Tuple[str, str]],
    additional_files: List[Tuple[str, str]],
    download_mode: Optional[GenerateMode],
) -> str:
    """Copy a script and its required imports to an importable directory

    Args:
        name (str): name of the resource to load
        importable_directory_path (str): path to the loadable folder in the dynamic modules directory
        subdirectory_name (str): name of the subdirectory in importable_directory_path in which to place the script
        original_local_path (str): local path to the resource script
        local_imports (List[Tuple[str, str]]): list of (destination_filename, import_file_to_copy)
        additional_files (List[Tuple[str, str]]): list of (destination_filename, additional_file_to_copy)
        download_mode (Optional[GenerateMode]): download mode

    Return:
        importable_local_file: path to an importable module with importlib.import_module
    """

    # Define a directory with a unique name in our dataset or metric folder
    # path is: ./datasets|metrics/dataset|metric_name/hash_from_code/script.py
    # we use a hash as subdirectory_name to be able to have multiple versions of a dataset/metric processing file together
    importable_subdirectory = os.path.join(importable_directory_path, subdirectory_name)
    importable_local_file = os.path.join(importable_subdirectory, name + ".py")

    # Prevent parallel disk operations
    lock_path = importable_directory_path + ".lock"
    with FileLock(lock_path):
        # Create main dataset/metrics folder if needed
        if download_mode == GenerateMode.FORCE_REDOWNLOAD and os.path.exists(importable_directory_path):
            shutil.rmtree(importable_directory_path)
        os.makedirs(importable_directory_path, exist_ok=True)

        # add an __init__ file to the main dataset folder if needed
        init_file_path = os.path.join(importable_directory_path, "__init__.py")
        if not os.path.exists(init_file_path):
            with open(init_file_path, "w"):
                pass

        # Create hash dataset folder if needed
        os.makedirs(importable_subdirectory, exist_ok=True)
        # add an __init__ file to the hash dataset folder if needed
        init_file_path = os.path.join(importable_subdirectory, "__init__.py")
        if not os.path.exists(init_file_path):
            with open(init_file_path, "w"):
                pass

        # Copy dataset.py file in hash folder if needed
        if not os.path.exists(importable_local_file):
            shutil.copyfile(original_local_path, importable_local_file)

        # Record metadata associating original dataset path with local unique folder
        meta_path = importable_local_file.split(".py")[0] + ".json"
        if not os.path.exists(meta_path):
            meta = {"original file path": original_local_path, "local file path": importable_local_file}
            # the filename is *.py in our case, so better rename to filenam.json instead of filename.py.json
            with open(meta_path, "w", encoding="utf-8") as meta_file:
                json.dump(meta, meta_file)

        # Copy all the additional imports
        for import_name, import_path in local_imports:
            if os.path.isfile(import_path):
                full_path_local_import = os.path.join(importable_subdirectory, import_name + ".py")
                if not os.path.exists(full_path_local_import):
                    shutil.copyfile(import_path, full_path_local_import)
            elif os.path.isdir(import_path):
                full_path_local_import = os.path.join(importable_subdirectory, import_name)
                if not os.path.exists(full_path_local_import):
                    shutil.copytree(import_path, full_path_local_import)
            else:
                raise OSError(f"Error with local import at {import_path}")

        # Copy aditional files like dataset infos file if needed
        for file_name, original_path in additional_files:
            destination_additional_path = os.path.join(importable_subdirectory, file_name)
            if not os.path.exists(destination_additional_path) or not filecmp.cmp(
                original_path, destination_additional_path
            ):
                shutil.copyfile(original_path, destination_additional_path)
        return importable_local_file


def _create_importable_file(
    local_path: str,
    local_imports: List[Tuple[str, str]],
    additional_files: List[Tuple[str, str]],
    dynamic_modules_path: str,
    module_namespace: str,
    name: str,
    download_mode: GenerateMode,
) -> Tuple[str, str]:
    importable_directory_path = os.path.join(dynamic_modules_path, module_namespace, name.replace("/", "___"))
    Path(importable_directory_path).mkdir(parents=True, exist_ok=True)
    (Path(importable_directory_path).parent / "__init__.py").touch(exist_ok=True)
    hash = files_to_hash([local_path] + [loc[1] for loc in local_imports])
    importable_local_file = _copy_script_and_other_resources_in_importable_dir(
        name=name.split("/")[-1],
        importable_directory_path=importable_directory_path,
        subdirectory_name=hash,
        original_local_path=local_path,
        local_imports=local_imports,
        additional_files=additional_files,
        download_mode=download_mode,
    )
    logger.debug(f"Created importable dataset file at {importable_local_file}")
    module_path = ".".join(
        [os.path.basename(dynamic_modules_path), module_namespace, name.replace("/", "___"), hash, name.split("/")[-1]]
    )
    return module_path, hash


def infer_module_for_data_files(
    data_files_list: DataFilesList, use_auth_token: Optional[Union[bool, str]] = None
) -> Optional[str]:
    extensions_counter = Counter(suffix[1:] for filepath in data_files_list for suffix in Path(filepath).suffixes)
    if extensions_counter:
        most_common = extensions_counter.most_common(1)[0][0]
        if most_common in _EXTENSION_TO_MODULE:
            return _EXTENSION_TO_MODULE[most_common]
        elif most_common == "zip":
            return infer_module_for_data_files_in_archives(data_files_list, use_auth_token=use_auth_token)


def infer_module_for_data_files_in_archives(
    data_files_list: DataFilesList, use_auth_token: Optional[Union[bool, str]]
) -> Optional[str]:
    archived_files = []
    for filepath in data_files_list:
        if str(filepath).endswith(".zip"):
            extracted = xjoin(StreamingDownloadManager().extract(filepath), "*")
            archived_files += [
                f.split("::")[0] for f in xglob(extracted, recursive=True, use_auth_token=use_auth_token)
            ]
    extensions_counter = Counter(suffix[1:] for filepath in archived_files for suffix in Path(filepath).suffixes)
    if extensions_counter:
        most_common = extensions_counter.most_common(1)[0][0]
        if most_common in _EXTENSION_TO_MODULE:
            return _EXTENSION_TO_MODULE[most_common]


@dataclass
class DatasetModule:
    module_path: str
    hash: str
    builder_kwargs: dict


@dataclass
class MetricModule:
    module_path: str
    hash: str


class _DatasetModuleFactory:
    def get_module(self) -> DatasetModule:
        raise NotImplementedError


class _MetricModuleFactory:
    def get_module(self) -> MetricModule:
        raise NotImplementedError


class CanonicalDatasetModuleFactory(_DatasetModuleFactory):
    """Get the module of a canonical dataset. The dataset script is downloaded from GitHub."""

    def __init__(
        self,
        name: str,
        revision: Optional[Union[str, Version]] = None,
        download_config: Optional[DownloadConfig] = None,
        download_mode: Optional[GenerateMode] = None,
        dynamic_modules_path: Optional[str] = None,
    ):
        self.name = name
        self.revision = revision
        self.download_config = download_config
        self.download_mode = download_mode
        self.dynamic_modules_path = dynamic_modules_path
        assert self.name.count("/") == 0
        increase_load_count(name, resource_type="dataset")

    def download_loading_script(self, revision: Optional[str]) -> str:
        file_path = hf_github_url(path=self.name, name=self.name + ".py", revision=revision)
        return cached_path(file_path, download_config=self.download_config)

    def download_dataset_infos_file(self, revision: Optional[str]) -> str:
        dataset_infos = hf_github_url(path=self.name, name=config.DATASETDICT_INFOS_FILENAME, revision=revision)
        # Download the dataset infos file if available
        try:
            return cached_path(
                dataset_infos,
                download_config=self.download_config,
            )
        except (FileNotFoundError, ConnectionError):
            return None

    def get_module(self) -> DatasetModule:
        # get script and other files
        revision = self.revision
        try:
            local_path = self.download_loading_script(revision)
        except FileNotFoundError:
            if revision is not None or os.getenv("HF_SCRIPTS_VERSION", None) is not None:
                raise
            else:
                revision = "master"
                local_path = self.download_loading_script(revision)
                logger.warning(
                    f"Couldn't find a directory or a dataset named '{self.name}' in this version. "
                    f"It was picked from the master branch on github instead."
                )
        dataset_infos_path = self.download_dataset_infos_file(revision)
        imports = get_imports(local_path)
        local_imports = _download_additional_modules(
            name=self.name,
            base_path=hf_github_url(path=self.name, name="", revision=revision),
            imports=imports,
            download_config=self.download_config,
        )
        additional_files = [(config.DATASETDICT_INFOS_FILENAME, dataset_infos_path)] if dataset_infos_path else []
        # copy the script and the files in an importable directory
        dynamic_modules_path = self.dynamic_modules_path if self.dynamic_modules_path else init_dynamic_modules()
        module_path, hash = _create_importable_file(
            local_path=local_path,
            local_imports=local_imports,
            additional_files=additional_files,
            dynamic_modules_path=dynamic_modules_path,
            module_namespace="datasets",
            name=self.name,
            download_mode=self.download_mode,
        )
        # make the new module to be noticed by the import system
        importlib.invalidate_caches()
        builder_kwargs = {"hash": hash, "base_path": hf_github_url(self.name, "", revision=revision)}
        return DatasetModule(module_path, hash, builder_kwargs)


class CanonicalMetricModuleFactory(_MetricModuleFactory):
    """Get the module of a metric. The metric script is downloaded from GitHub."""

    def __init__(
        self,
        name: str,
        revision: Optional[Union[str, Version]] = None,
        download_config: Optional[DownloadConfig] = None,
        download_mode: Optional[GenerateMode] = None,
        dynamic_modules_path: Optional[str] = None,
    ):
        self.name = name
        self.revision = revision
        self.download_config = download_config
        self.download_mode = download_mode
        self.dynamic_modules_path = dynamic_modules_path
        assert self.name.count("/") == 0
        increase_load_count(name, resource_type="metric")

    def download_loading_script(self, revision: Optional[str]) -> str:
        file_path = hf_github_url(path=self.name, name=self.name + ".py", revision=revision, dataset=False)
        return cached_path(file_path, download_config=self.download_config)

    def get_module(self) -> MetricModule:
        # get script and other files
        revision = self.revision
        try:
            local_path = self.download_loading_script(revision)
            revision = self.revision
        except FileNotFoundError:
            if revision is not None or os.getenv("HF_SCRIPTS_VERSION", None) is not None:
                raise
            else:
                revision = "master"
                local_path = self.download_loading_script(revision)
                logger.warning(
                    f"Couldn't find a directory or a metric named '{self.name}' in this version. "
                    f"It was picked from the master branch on github instead."
                )
        imports = get_imports(local_path)
        local_imports = _download_additional_modules(
            name=self.name,
            base_path=hf_github_url(path=self.name, name="", revision=revision, dataset=False),
            imports=imports,
            download_config=self.download_config,
        )
        # copy the script and the files in an importable directory
        dynamic_modules_path = self.dynamic_modules_path if self.dynamic_modules_path else init_dynamic_modules()
        module_path, hash = _create_importable_file(
            local_path=local_path,
            local_imports=local_imports,
            additional_files=[],
            dynamic_modules_path=dynamic_modules_path,
            module_namespace="metrics",
            name=self.name,
            download_mode=self.download_mode,
        )
        # make the new module to be noticed by the import system
        importlib.invalidate_caches()
        return MetricModule(module_path, hash)


class LocalMetricModuleFactory(_MetricModuleFactory):
    """Get the module of a local metric. The metric script is loaded from a local script."""

    def __init__(
        self,
        path: str,
        download_config: Optional[DownloadConfig] = None,
        download_mode: Optional[GenerateMode] = None,
        dynamic_modules_path: Optional[str] = None,
    ):
        self.path = path
        self.name = Path(path).stem
        self.download_config = download_config
        self.download_mode = download_mode
        self.dynamic_modules_path = dynamic_modules_path

    def get_module(self) -> MetricModule:
        # get script and other files
        imports = get_imports(self.path)
        local_imports = _download_additional_modules(
            name=self.name,
            base_path=str(Path(self.path).parent),
            imports=imports,
            download_config=self.download_config,
        )
        # copy the script and the files in an importable directory
        dynamic_modules_path = self.dynamic_modules_path if self.dynamic_modules_path else init_dynamic_modules()
        module_path, hash = _create_importable_file(
            local_path=self.path,
            local_imports=local_imports,
            additional_files=[],
            dynamic_modules_path=dynamic_modules_path,
            module_namespace="metrics",
            name=self.name,
            download_mode=self.download_mode,
        )
        # make the new module to be noticed by the import system
        importlib.invalidate_caches()
        return MetricModule(module_path, hash)


class LocalDatasetModuleFactoryWithScript(_DatasetModuleFactory):
    """Get the module of a local dataset. The dataset script is loaded from a local script."""

    def __init__(
        self,
        path: str,
        download_config: Optional[DownloadConfig] = None,
        download_mode: Optional[GenerateMode] = None,
        dynamic_modules_path: Optional[str] = None,
    ):
        self.path = path
        self.name = Path(path).stem
        self.download_config = download_config
        self.download_mode = download_mode
        self.dynamic_modules_path = dynamic_modules_path

    def get_module(self) -> DatasetModule:
        # get script and other files
        dataset_infos_path = Path(self.path).parent / config.DATASETDICT_INFOS_FILENAME
        imports = get_imports(self.path)
        local_imports = _download_additional_modules(
            name=self.name,
            base_path=str(Path(self.path).parent),
            imports=imports,
            download_config=self.download_config,
        )
        additional_files = (
            [(config.DATASETDICT_INFOS_FILENAME, str(dataset_infos_path))] if dataset_infos_path.is_file() else []
        )
        # copy the script and the files in an importable directory
        dynamic_modules_path = self.dynamic_modules_path if self.dynamic_modules_path else init_dynamic_modules()
        module_path, hash = _create_importable_file(
            local_path=self.path,
            local_imports=local_imports,
            additional_files=additional_files,
            dynamic_modules_path=dynamic_modules_path,
            module_namespace="datasets",
            name=self.name,
            download_mode=self.download_mode,
        )
        # make the new module to be noticed by the import system
        importlib.invalidate_caches()
        builder_kwargs = {"hash": hash, "base_path": str(Path(self.path).parent)}
        return DatasetModule(module_path, hash, builder_kwargs)


class LocalDatasetModuleFactoryWithoutScript(_DatasetModuleFactory):
    """Get the module of a dataset loaded from the user's data files. The dataset builder module to use is infered from the data files extensions."""

    def __init__(
        self,
        path: str,
        data_files: Optional[Union[str, List, Dict]] = None,
        download_mode: Optional[GenerateMode] = None,
    ):
        self.path = path
        self.name = Path(path).stem
        self.data_files = data_files
        self.download_mode = download_mode

    def get_module(self) -> DatasetModule:
        data_files = DataFilesDict.from_local_or_remote(
            _sanitize_patterns(self.data_files), base_path=self.path, allowed_extensions=ALL_ALLOWED_EXTENSIONS
        )
        infered_module_names = {
            key: infer_module_for_data_files(data_files_list) for key, data_files_list in data_files.items()
        }
        if len(set(list(infered_module_names.values()))) > 1:
            raise ValueError(f"Couldn't infer the same data file format for all splits. Got {infered_module_names}")
        infered_module_name = next(iter(infered_module_names.values()))
        if not infered_module_name:
            raise FileNotFoundError(f"No data files or dataset script found in {self.path}")
        module_path, hash = _PACKAGED_DATASETS_MODULES[infered_module_name]
        builder_kwargs = {
            "hash": hash,
            "data_files": data_files,
            "name": os.path.basename(self.path),
            "base_path": self.path,
        }
        return DatasetModule(module_path, hash, builder_kwargs)


class PackagedDatasetModuleFactory(_DatasetModuleFactory):
    """Get the dataset builder module from the ones that are packaged with the library: csv, json, etc."""

    def __init__(
        self,
        name: str,
        data_files: Optional[Union[str, List, Dict]] = None,
        download_config: Optional[DownloadConfig] = None,
        download_mode: Optional[GenerateMode] = None,
    ):
        self.name = name
        self.data_files = data_files
        self.downnload_config = download_config
        self.download_mode = download_mode
        increase_load_count(name, resource_type="dataset")

    def get_module(self) -> DatasetModule:
        data_files = DataFilesDict.from_local_or_remote(
            _sanitize_patterns(self.data_files), use_auth_token=self.downnload_config.use_auth_token
        )
        module_path, hash = _PACKAGED_DATASETS_MODULES[self.name]
        builder_kwargs = {"hash": hash, "data_files": data_files}
        return DatasetModule(module_path, hash, builder_kwargs)


class CommunityDatasetModuleFactoryWithoutScript(_DatasetModuleFactory):
    """
    Get the module of a dataset loaded from data files of a dataset repository.
    The dataset builder module to use is infered from the data files extensions.
    """

    def __init__(
        self,
        name: str,
        revision: Optional[Union[str, Version]] = None,
        data_files: Optional[Union[str, List, Dict]] = None,
        download_config: Optional[DownloadConfig] = None,
        download_mode: Optional[GenerateMode] = None,
    ):
        self.name = name
        self.revision = revision
        self.data_files = data_files
        self.download_config = download_config or DownloadConfig()
        self.download_mode = download_mode
        assert self.name.count("/") == 1
        increase_load_count(name, resource_type="dataset")

    def get_module(self) -> DatasetModule:
        if isinstance(self.download_config.use_auth_token, bool):
            token = HfFolder.get_token() if self.download_config.use_auth_token else None
        else:
            token = self.download_config.use_auth_token
        dataset_info = HfApi(config.HF_ENDPOINT).dataset_info(
            self.name,
            revision=self.revision,
            token=token,
            timeout=100.0,
        )
        data_files = DataFilesDict.from_hf_repo(
            _sanitize_patterns(self.data_files),
            dataset_info=dataset_info,
            allowed_extensions=ALL_ALLOWED_EXTENSIONS,
        )
        infered_module_names = {
            key: infer_module_for_data_files(data_files_list, use_auth_token=self.download_config.use_auth_token)
            for key, data_files_list in data_files.items()
        }
        if len(set(list(infered_module_names.values()))) > 1:
            raise ValueError(f"Couldn't infer the same data file format for all splits. Got {infered_module_names}")
        infered_module_name = next(iter(infered_module_names.values()))
        if not infered_module_name:
            raise FileNotFoundError(f"No data files or dataset script found in {self.path}")
        module_path, hash = _PACKAGED_DATASETS_MODULES[infered_module_name]
        builder_kwargs = {
            "hash": hash,
            "data_files": data_files,
            "name": self.name.replace("/", "___"),
            "base_path": hf_hub_url(self.name, "", revision=self.revision),
        }
        return DatasetModule(module_path, hash, builder_kwargs)


class CommunityDatasetModuleFactoryWithScript(_DatasetModuleFactory):
    """Get the module of a dataset from a dataset repository. The dataset script comes from the script inside the dataset repository."""

    def __init__(
        self,
        name: str,
        revision: Optional[Union[str, Version]] = None,
        download_config: Optional[DownloadConfig] = None,
        download_mode: Optional[GenerateMode] = None,
        dynamic_modules_path: Optional[str] = None,
    ):
        self.name = name
        self.revision = revision
        self.download_config = download_config
        self.download_mode = download_mode
        self.dynamic_modules_path = dynamic_modules_path
        assert self.name.count("/") == 1
        increase_load_count(name, resource_type="dataset")

    def download_loading_script(self) -> str:
        file_path = hf_hub_url(path=self.name, name=self.name.split("/")[1] + ".py", revision=self.revision)
        return cached_path(file_path, download_config=self.download_config)

    def download_dataset_infos_file(self) -> str:
        dataset_infos = hf_hub_url(path=self.name, name=config.DATASETDICT_INFOS_FILENAME, revision=self.revision)
        # Download the dataset infos file if available
        try:
            return cached_path(
                dataset_infos,
                download_config=self.download_config,
            )
        except (FileNotFoundError, ConnectionError):
            return None

    def get_module(self) -> DatasetModule:
        # get script and other files
        local_path = self.download_loading_script()
        dataset_infos_path = self.download_dataset_infos_file()
        imports = get_imports(local_path)
        local_imports = _download_additional_modules(
            name=self.name,
            base_path=hf_hub_url(path=self.name, name="", revision=self.revision),
            imports=imports,
            download_config=self.download_config,
        )
        additional_files = [(config.DATASETDICT_INFOS_FILENAME, dataset_infos_path)] if dataset_infos_path else []
        # copy the script and the files in an importable directory
        dynamic_modules_path = self.dynamic_modules_path if self.dynamic_modules_path else init_dynamic_modules()
        module_path, hash = _create_importable_file(
            local_path=local_path,
            local_imports=local_imports,
            additional_files=additional_files,
            dynamic_modules_path=dynamic_modules_path,
            module_namespace="datasets",
            name=self.name,
            download_mode=self.download_mode,
        )
        # make the new module to be noticed by the import system
        importlib.invalidate_caches()
        builder_kwargs = {
            "hash": hash,
            "base_path": hf_hub_url(self.name, "", revision=self.revision),
            "namespace": self.name.split("/")[0],
        }
        return DatasetModule(module_path, hash, builder_kwargs)


class CachedDatasetModuleFactory(_DatasetModuleFactory):
    """
    Get the module of a dataset that has been loaded once already and cached.
    The script that is loaded from the cache is the most recent one with a matching name.
    """

    def __init__(
        self,
        name: str,
        dynamic_modules_path: Optional[str] = None,
    ):
        self.name = name
        self.dynamic_modules_path = dynamic_modules_path
        assert self.name.count("/") <= 1

    def get_module(self) -> DatasetModule:
        dynamic_modules_path = self.dynamic_modules_path if self.dynamic_modules_path else init_dynamic_modules()
        importable_directory_path = os.path.join(dynamic_modules_path, "datasets", self.name.replace("/", "___"))
        hashes = (
            [h for h in os.listdir(importable_directory_path) if len(h) == 64]
            if os.path.isdir(importable_directory_path)
            else None
        )
        if not hashes:
            raise FileNotFoundError(f"Dataset {self.name} is not cached in {dynamic_modules_path}")
        # get most recent

        def _get_modification_time(module_hash):
            return (Path(importable_directory_path) / module_hash / (self.name.split("/")[-1] + ".py")).stat().st_mtime

        hash = sorted(hashes, key=_get_modification_time)[-1]
        logger.warning(
            f"Using the latest cached version of the module from {os.path.join(importable_directory_path, hash)} "
            f"(last modified on {time.ctime(_get_modification_time(hash))}) since it "
            f"couldn't be found locally at {self.name}, or remotely on the Hugging Face Hub."
        )
        # make the new module to be noticed by the import system
        module_path = ".".join(
            [
                os.path.basename(dynamic_modules_path),
                "datasets",
                self.name.replace("/", "___"),
                hash,
                self.name.split("/")[-1],
            ]
        )
        importlib.invalidate_caches()
        builder_kwargs = {"hash": hash, "namespace": self.name.split("/")[0]}
        return DatasetModule(module_path, hash, builder_kwargs)


class CachedMetricModuleFactory(_MetricModuleFactory):
    """
    Get the module of a metric that has been loaded once already and cached.
    The script that is loaded from the cache is the most recent one with a matching name.
    """

    def __init__(
        self,
        name: str,
        dynamic_modules_path: Optional[str] = None,
    ):
        self.name = name
        self.dynamic_modules_path = dynamic_modules_path
        assert self.name.count("/") == 0

    def get_module(self) -> MetricModule:
        dynamic_modules_path = self.dynamic_modules_path if self.dynamic_modules_path else init_dynamic_modules()
        importable_directory_path = os.path.join(dynamic_modules_path, "metrics", self.name)
        hashes = (
            [h for h in os.listdir(importable_directory_path) if len(h) == 64]
            if os.path.isdir(importable_directory_path)
            else None
        )
        if not hashes:
            raise FileNotFoundError(f"Metric {self.name} is not cached in {dynamic_modules_path}")
        # get most recent

        def _get_modification_time(module_hash):
            return (Path(importable_directory_path) / module_hash / (self.name + ".py")).stat().st_mtime

        hash = sorted(hashes, key=_get_modification_time)[-1]
        logger.warning(
            f"Using the latest cached version of the module from {os.path.join(importable_directory_path, hash)} "
            f"(last modified on {time.ctime(_get_modification_time(hash))}) since it "
            f"couldn't be found locally at {self.name}, or remotely on the Hugging Face Hub."
        )
        # make the new module to be noticed by the import system
        module_path = ".".join([os.path.basename(dynamic_modules_path), "metrics", self.name, hash, self.name])
        importlib.invalidate_caches()
        return MetricModule(module_path, hash)


def dataset_module_factory(
    path: str,
    revision: Optional[Union[str, Version]] = None,
    download_config: Optional[DownloadConfig] = None,
    download_mode: Optional[GenerateMode] = None,
    force_local_path: Optional[str] = None,
    dynamic_modules_path: Optional[str] = None,
    data_files: Optional[Union[Dict, List, str, DataFilesDict]] = None,
    **download_kwargs,
) -> DatasetModule:
    r"""
    Download/extract/cache a dataset module.

    Dataset codes are cached inside the the dynamic modules cache to allow easy import (avoid ugly sys.path tweaks).

    Args:

        path (str): Path or name of the dataset.
            Depending on ``path``, the module that is returned is either generic module (csv, json, text etc.) or a module defined by dataset cript (a python file).

            For local datasets:

            - if ``path`` is a local directory containing data files (but doesn't contain a dataset script)
              -> load a generic module (csv, json, text etc.) based on the content of the directory
              e.g. ``'./path/to/directory/with/my/csv/data'``.
            - if ``path`` is a local dataset script or a directory containing a local dataset script (if the script has the same name as the directory):
              -> load the module from the dataset script
              e.g. ``'./dataset/squad'`` or ``'./dataset/squad/squad.py'``.

            For datasets on the Hugging Face Hub (list all available datasets and ids with ``datasets.list_datasets()``)

            - if ``path`` is a canonical dataset on the HF Hub (ex: `glue`, `squad`)
              -> load the module from the dataset script in the github repository at huggingface/datasets
              e.g. ``'squad'`` or ``'glue'``.
            - if ``path`` is a dataset repository on the HF hub containing data files (without a dataset script)
              -> load a generic module (csv, text etc.) based on the content of the repository
              e.g. ``'username/dataset_name'``, a dataset repository on the HF hub containing your data files.
            - if ``path`` is a dataset repository on the HF hub with a dataset script (if the script has the same name as the directory)
              -> load the module from the dataset script in the dataset repository
              e.g. ``'username/dataset_name'``, a dataset repository on the HF hub containing a dataset script `'dataset_name.py'`.

        revision (Optional ``Union[str, datasets.Version]``):
            Which revision of a dataset repository to use, or which revision of a canonical dataset to use.
            If specified, the module will be loaded at this version.
            By default for dataset repositories:
            - for dataset repositories, it is set to the "main" branch
            By default for canonical datasets:
            - it is set to the local version of the lib.
            - it will also try to load it from the master branch if it's not available at the local version of the lib.
            Specifying a version that is different from your local version of the lib might cause compatibility issues.
        download_config (:class:`DownloadConfig`, optional): Specific download configuration parameters.
        download_mode (:class:`GenerateMode`, default ``REUSE_DATASET_IF_EXISTS``): Download/generate mode.
        force_local_path (Optional str): Optional path to a local path to download and prepare the script to.
            Used to inspect or modify the script folder.
        dynamic_modules_path (Optional str, defaults to HF_MODULES_CACHE / "datasets_modules", i.e. ~/.cache/huggingface/modules/datasets_modules):
            Optional path to the directory in which the dynamic modules are saved. It must have been initialized with :obj:`init_dynamic_modules`.
            By default the datasets and metrics are stored inside the `datasets_modules` module.
        data_files (:obj:`Union[Dict, List, str]`, optional): Defining the data_files of the dataset configuration.
        script_version:
            .. deprecated:: 1.13
                'script_version' was renamed to 'revision' in version 1.13 and will be removed in 1.15.
        download_kwargs: optional attributes for DownloadConfig() which will override the attributes in download_config if supplied.

    Returns:
        DatasetModule
    """
    if download_config is None:
        download_config = DownloadConfig(**download_kwargs)
    download_config.extract_compressed_file = True
    download_config.force_extract = True

    filename = list(filter(lambda x: x, path.replace(os.sep, "/").split("/")))[-1]
    if not filename.endswith(".py"):
        filename = filename + ".py"
    combined_path = os.path.join(path, filename)

    # We have several ways to get a dataset builder:
    #
    # - if path is the name of a packaged dataset module
    #   -> use the packaged module (json, csv, etc.)
    #
    # - if os.path.join(path, name) is a local python file
    #   -> use the module from the python file
    # - if path is a local directory (but no python file)
    #   -> use a packaged module (csv, text etc.) based on content of the directory
    #
    # - if path has no "/" and is a module on github (in /datasets or in /metrics)
    #   -> use the module from the python file on github
    # - if path has one "/" and is dataset repository on the HF hub with a python file
    #   -> the module from the python file in the dataset repository
    # - if path has one "/" and is dataset repository on the HF hub without a python file
    #   -> use a packaged module (csv, text etc.) based on content of the repository

    # Try packaged
    if path in _PACKAGED_DATASETS_MODULES:
        return PackagedDatasetModuleFactory(
            path, data_files=data_files, download_config=download_config, download_mode=download_mode
        ).get_module()
    # Try locally
    elif path.endswith(filename):
        if os.path.isfile(path):
            return LocalDatasetModuleFactoryWithScript(
                path, download_mode=download_mode, dynamic_modules_path=dynamic_modules_path
            ).get_module()
        else:
            raise FileNotFoundError(f"Couldn't find a dataset script at {relative_to_absolute_path(path)}")
    elif os.path.isfile(combined_path):
        return LocalDatasetModuleFactoryWithScript(
            combined_path, download_mode=download_mode, dynamic_modules_path=dynamic_modules_path
        ).get_module()
    elif os.path.isdir(path):
        return LocalDatasetModuleFactoryWithoutScript(
            path, data_files=data_files, download_mode=download_mode
        ).get_module()
    # Try remotely
    elif is_relative_path(path) and path.count("/") <= 1 and not force_local_path:
        try:
            _raise_if_offline_mode_is_enabled()
            if path.count("/") == 0:  # canonical datasets/metrics: github path
                return CanonicalDatasetModuleFactory(
                    path,
                    revision=revision,
                    download_config=download_config,
                    download_mode=download_mode,
                    dynamic_modules_path=dynamic_modules_path,
                ).get_module()
            elif path.count("/") == 1:  # users datasets/metrics: s3 path (hub for datasets and s3 for metrics)
                hf_api = HfApi(config.HF_ENDPOINT)
                try:
                    if isinstance(download_config.use_auth_token, bool):
                        token = HfFolder.get_token() if download_config.use_auth_token else None
                    else:
                        token = download_config.use_auth_token
                    dataset_info = hf_api.dataset_info(
                        repo_id=path,
                        revision=revision,
                        token=token,
                        timeout=100.0,
                    )
                except Exception as e:  # noqa: catch any exception of hf_hub and consider that the dataset doesn't exist
                    if isinstance(
                        e,
                        (
                            OfflineModeIsEnabled,
                            requests.exceptions.ConnectTimeout,
                            requests.exceptions.ConnectionError,
                        ),
                    ):
                        raise ConnectionError(f"Couldn't reach '{path}' on the Hub ({type(e).__name__})")
                    elif "404" in str(e):
                        msg = f"Dataset '{path}' doesn't exist on the Hub"
                        raise FileNotFoundError(msg + f" at revision '{revision}'" if revision else msg)
                    else:
                        raise e
                if filename in [sibling.rfilename for sibling in dataset_info.siblings]:
                    return CommunityDatasetModuleFactoryWithScript(
                        path,
                        revision=revision,
                        download_config=download_config,
                        download_mode=download_mode,
                        dynamic_modules_path=dynamic_modules_path,
                    ).get_module()
                else:
                    return CommunityDatasetModuleFactoryWithoutScript(
                        path,
                        revision=revision,
                        data_files=data_files,
                        download_config=download_config,
                        download_mode=download_mode,
                    ).get_module()
        except Exception as e1:  # noqa: all the attempts failed, before raising the error we should check if the module is already cached.
            try:
                return CachedDatasetModuleFactory(path, dynamic_modules_path=dynamic_modules_path).get_module()
            except Exception as e2:  # noqa: if it's not in the cache, then it doesn't exist.
                if isinstance(e1, OfflineModeIsEnabled):
                    raise ConnectionError(f"Couln't reach the Hugging Face Hub for dataset '{path}': {e1}") from None
                if isinstance(e1, FileNotFoundError):
                    raise FileNotFoundError(
                        f"Couldn't find a dataset script at {relative_to_absolute_path(combined_path)} or any data file in the same directory. "
                        f"Couldn't find '{path}' on the Hugging Face Hub either: {type(e1).__name__}: {e1}"
                    ) from None
                raise e1 from None
    else:
        raise FileNotFoundError(
            f"Couldn't find a dataset script at {relative_to_absolute_path(combined_path)} or any data file in the same directory."
        )


def metric_module_factory(
    path: str,
    revision: Optional[Union[str, Version]] = None,
    download_config: Optional[DownloadConfig] = None,
    download_mode: Optional[GenerateMode] = None,
    force_local_path: Optional[str] = None,
    dynamic_modules_path: Optional[str] = None,
    **download_kwargs,
) -> MetricModule:
    r"""
    Download/extract/cache a metric module.

    Metrics codes are cached inside the the dynamic modules cache to allow easy import (avoid ugly sys.path tweaks).

    Args:

        path (str): Path or name of the metric script.

            - if ``path`` is a local metric script or a directory containing a local metric script (if the script has the same name as the directory):
              -> load the module from the metric script
              e.g. ``'./metrics/accuracy'`` or ``'./metrics/accuracy/accuracy.py'``.
            - if ``path`` is a canonical metric (ex: `glue`, `squad`)
              -> load the module from the metric script in the github repository at huggingface/datasets
              e.g. ``'accuracy'`` or ``'rouge'``.

        revision (Optional ``Union[str, datasets.Version]``):
            If specified, the module will be loaded from the datasets repository at this version.
            By default:
            - it is set to the local version of the lib.
            - it will also try to load it from the master branch if it's not available at the local version of the lib.
            Specifying a version that is different from your local version of the lib might cause compatibility issues.
        download_config (:class:`DownloadConfig`, optional): Specific download configuration parameters.
        download_mode (:class:`GenerateMode`, default ``REUSE_DATASET_IF_EXISTS``): Download/generate mode.
        force_local_path (Optional str): Optional path to a local path to download and prepare the script to.
            Used to inspect or modify the script folder.
        dynamic_modules_path (Optional str, defaults to HF_MODULES_CACHE / "datasets_modules", i.e. ~/.cache/huggingface/modules/datasets_modules):
            Optional path to the directory in which the dynamic modules are saved. It must have been initialized with :obj:`init_dynamic_modules`.
            By default the datasets and metrics are stored inside the `datasets_modules` module.
        script_version:
            .. deprecated:: 1.13
                'script_version' was renamed to 'revision' in version 1.13 and will be removed in 1.15.
        download_kwargs: optional attributes for DownloadConfig() which will override the attributes in download_config if supplied.

    Returns:
        MetricModule
    """
    if download_config is None:
        download_config = DownloadConfig(**download_kwargs)
    download_config.extract_compressed_file = True
    download_config.force_extract = True

    filename = list(filter(lambda x: x, path.replace(os.sep, "/").split("/")))[-1]
    if not filename.endswith(".py"):
        filename = filename + ".py"
    combined_path = os.path.join(path, filename)
    # Try locally
    if path.endswith(filename):
        if os.path.isfile(path):
            return LocalMetricModuleFactory(
                path, download_mode=download_mode, dynamic_modules_path=dynamic_modules_path
            ).get_module()
        else:
            raise FileNotFoundError(f"Couldn't find a metric script at {relative_to_absolute_path(path)}")
    elif os.path.isfile(combined_path):
        return LocalMetricModuleFactory(
            combined_path, download_mode=download_mode, dynamic_modules_path=dynamic_modules_path
        ).get_module()
    elif is_relative_path(path) and path.count("/") == 0 and not force_local_path:
        try:
            return CanonicalMetricModuleFactory(
                path,
                revision=revision,
                download_config=download_config,
                download_mode=download_mode,
                dynamic_modules_path=dynamic_modules_path,
            ).get_module()
        except Exception as e1:  # noqa: all the attempts failed, before raising the error we should check if the module is already cached.
            try:
                return CachedMetricModuleFactory(path, dynamic_modules_path=dynamic_modules_path).get_module()
            except Exception as e2:  # noqa: if it's not in the cache, then it doesn't exist.
                if not isinstance(e1, FileNotFoundError):
                    raise e1 from None
                raise FileNotFoundError(
                    f"Couldn't find a metric script at {relative_to_absolute_path(combined_path)}. "
                    f"Metric '{path}' doesn't exist on the Hugging Face Hub either."
                ) from None
    else:
        raise FileNotFoundError(f"Couldn't find a metric script at {relative_to_absolute_path(combined_path)}.")


def prepare_module(
    path: str,
    revision: Optional[Union[str, Version]] = None,
    download_config: Optional[DownloadConfig] = None,
    download_mode: Optional[GenerateMode] = None,
    dataset: bool = True,
    force_local_path: Optional[str] = None,
    dynamic_modules_path: Optional[str] = None,
    data_files: Optional[Union[Dict, List, str]] = None,
    script_version="deprecated",
    **download_kwargs,
) -> Union[Tuple[str, str], Tuple[str, str, Optional[str]]]:
    """For backward compatibility. Please use dataset_module_factory or metric_module_factory instead."""
    if script_version != "deprecated":
        warnings.warn(
            "'script_version' was renamed to 'revision' in version 1.13 and will be removed in 1.15.", FutureWarning
        )
        revision = script_version
    if dataset:
        results = dataset_module_factory(
            path,
            revision=revision,
            download_config=download_config,
            download_mode=download_mode,
            force_local_path=force_local_path,
            dynamic_modules_path=dynamic_modules_path,
            data_files=data_files,
            **download_kwargs,
        )
        return results.module_path, results.hash
    else:
        results = metric_module_factory(
            path,
            revision=revision,
            download_config=download_config,
            download_mode=download_mode,
            force_local_path=force_local_path,
            dynamic_modules_path=dynamic_modules_path,
            **download_kwargs,
        )
        return results.module_path, results.hash


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
    revision: Optional[Union[str, Version]] = None,
    script_version="deprecated",
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
        cache_dir (Optional str): path to store the temporary predictions and references (default to `~/.cache/huggingface/metrics/`)
        experiment_id (``str``): A specific experiment id. This is used if several distributed evaluations share the same file system.
            This is useful to compute metrics in distributed setups (in particular non-additive metrics like F1).
        keep_in_memory (bool): Whether to store the temporary results in memory (defaults to False)
        download_config (Optional ``datasets.DownloadConfig``: specific download configuration parameters.
        download_mode (:class:`GenerateMode`, default ``REUSE_DATASET_IF_EXISTS``): Download/generate mode.
        revision (Optional ``Union[str, datasets.Version]``): if specified, the module will be loaded from the datasets repository
            at this version. By default it is set to the local version of the lib. Specifying a version that is different from
            your local version of the lib might cause compatibility issues.
        script_version:
            .. deprecated:: 1.13
                'script_version' was renamed to 'revision' in version 1.13 and will be removed in 1.15.

    Returns:
        `datasets.Metric`
    """
    if script_version != "deprecated":
        warnings.warn(
            "'script_version' was renamed to 'revision' in version 1.13 and will be removed in 1.15.", FutureWarning
        )
        revision = script_version
    metric_module = metric_module_factory(
        path, revision=revision, download_config=download_config, download_mode=download_mode
    ).module_path
    metric_cls = import_main_class(metric_module, dataset=False)
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
    data_files: Optional[Union[str, Sequence[str], Mapping[str, Union[str, Sequence[str]]]]] = None,
    cache_dir: Optional[str] = None,
    features: Optional[Features] = None,
    download_config: Optional[DownloadConfig] = None,
    download_mode: Optional[GenerateMode] = None,
    revision: Optional[Union[str, Version]] = None,
    use_auth_token: Optional[Union[bool, str]] = None,
    script_version="deprecated",
    **config_kwargs,
) -> DatasetBuilder:
    """Load a builder for the dataset. A dataset builder can be used to inspect general information that is required to build a dataset (cache directory, config, dataset info, etc.)
    without downloading the dataset itself.

    This method will download and import the dataset loading script from ``path`` if it's not already cached inside the library.

    Args:

        path (:obj:`str`): Path or name of the dataset.
            Depending on ``path``, the dataset builder that is returned id either generic dataset builder (csv, json, text etc.) or a dataset builder defined defined a dataset script (a python file).

            For local datasets:

            - if ``path`` is a local directory (but doesn't contain a dataset script)
              -> load a generic dataset builder (csv, json, text etc.) based on the content of the directory
              e.g. ``'./path/to/directory/with/my/csv/data'``.
            - if ``path`` is a local dataset script or a directory containing a local dataset script (if the script has the same name as the directory):
              -> load the dataset builder from the dataset script
              e.g. ``'./dataset/squad'`` or ``'./dataset/squad/squad.py'``.

            For datasets on the Hugging Face Hub (list all available datasets and ids with ``datasets.list_datasets()``)

            - if ``path`` is a canonical dataset on the HF Hub (ex: `glue`, `squad`)
              -> load the dataset builder from the dataset script in the github repository at huggingface/datasets
              e.g. ``'squad'`` or ``'glue'``.
            - if ``path`` is a dataset repository on the HF hub (without a dataset script)
              -> load a generic dataset builder (csv, text etc.) based on the content of the repository
              e.g. ``'username/dataset_name'``, a dataset repository on the HF hub containing your data files.
            - if ``path`` is a dataset repository on the HF hub with a dataset script (if the script has the same name as the directory)
              -> load the dataset builder from the dataset script in the dataset repository
              e.g. ``'username/dataset_name'``, a dataset repository on the HF hub containing a dataset script `'dataset_name.py'`.


        name (:obj:`str`, optional): Defining the name of the dataset configuration.
        data_dir (:obj:`str`, optional): Defining the data_dir of the dataset configuration.
        data_files (:obj:`str` or :obj:`Sequence` or :obj:`Mapping`, optional): Path(s) to source data file(s).
        cache_dir (:obj:`str`, optional): Directory to read/write data. Defaults to "~/.cache/huggingface/datasets".
        features (:class:`Features`, optional): Set the features type to use for this dataset.
        download_config (:class:`~utils.DownloadConfig`, optional): Specific download configuration parameters.
        download_mode (:class:`GenerateMode`, default ``REUSE_DATASET_IF_EXISTS``): Download/generate mode.
        revision (:class:`~utils.Version` or :obj:`str`, optional): Version of the dataset script to load:

            - For canonical datasets in the `huggingface/datasets` library like "squad", the default version of the module is the local version of the lib.
              You can specify a different version from your local version of the lib (e.g. "master" or "1.2.0") but it might cause compatibility issues.
            - For community provided datasets like "lhoestq/squad" that have their own git repository on the Datasets Hub, the default version "main" corresponds to the "main" branch.
              You can specify a different version that the default "main" by using a commit sha or a git tag of the dataset repository.
        use_auth_token (``str`` or ``bool``, optional): Optional string or boolean to use as Bearer token for remote files on the Datasets Hub.
            If True, will get token from `"~/.huggingface"`.
        script_version:
            .. deprecated:: 1.13
                'script_version' was renamed to 'revision' in version 1.13 and will be removed in 1.15.

    Returns:
        :class:`DatasetBuilder`

    """
    if script_version != "deprecated":
        warnings.warn(
            "'script_version' was renamed to 'revision' in version 1.13 and will be removed in 1.15.", FutureWarning
        )
        revision = script_version
    if use_auth_token is not None:
        download_config = download_config.copy() if download_config else DownloadConfig()
        download_config.use_auth_token = use_auth_token
    dataset_module_factory_result = dataset_module_factory(
        path, revision=revision, download_config=download_config, download_mode=download_mode, data_files=data_files
    )

    # Get dataset builder class from the processing script
    dataset_module = dataset_module_factory_result.module_path
    builder_cls = import_main_class(dataset_module)
    builder_kwargs = dataset_module_factory_result.builder_kwargs
    data_files = builder_kwargs.pop("data_files", data_files)
    name = builder_kwargs.pop("name", name)
    hash = builder_kwargs.pop("hash")

    if path in _PACKAGED_DATASETS_MODULES and data_files is None:
        error_msg = f"Please specify the data files to load for the {path} dataset builder."
        example_extensions = [
            extension for extension in _EXTENSION_TO_MODULE if _EXTENSION_TO_MODULE[extension] == path
        ]
        if example_extensions:
            error_msg += f'\nFor example `data_files={{"train": "path/to/data/train/*.{example_extensions[0]}"}}`'
        raise ValueError(error_msg)

    # Instantiate the dataset builder
    builder_instance: DatasetBuilder = builder_cls(
        cache_dir=cache_dir,
        name=name,
        data_dir=data_dir,
        data_files=data_files,
        hash=hash,
        features=features,
        use_auth_token=use_auth_token,
        **builder_kwargs,
        **config_kwargs,
    )

    return builder_instance


def load_dataset(
    path: str,
    name: Optional[str] = None,
    data_dir: Optional[str] = None,
    data_files: Optional[Union[str, Sequence[str], Mapping[str, Union[str, Sequence[str]]]]] = None,
    split: Optional[Union[str, Split]] = None,
    cache_dir: Optional[str] = None,
    features: Optional[Features] = None,
    download_config: Optional[DownloadConfig] = None,
    download_mode: Optional[GenerateMode] = None,
    ignore_verifications: bool = False,
    keep_in_memory: Optional[bool] = None,
    save_infos: bool = False,
    revision: Optional[Union[str, Version]] = None,
    use_auth_token: Optional[Union[bool, str]] = None,
    task: Optional[Union[str, TaskTemplate]] = None,
    streaming: bool = False,
    script_version="deprecated",
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
                They can be directly accessed from drive, loaded in RAM or even streamed over the web.

        3. Return a dataset built from the requested splits in ``split`` (default: all).

    It also allows to load a dataset from a local directory or a dataset repository on the Hugging Face Hub without dataset script.
    In this case, it automatically loads all the data files from the directory or the dataset repository.

    Args:

        path (:obj:`str`): Path or name of the dataset.
            Depending on ``path``, the dataset builder that is returned id either generic dataset builder (csv, json, text etc.) or a dataset builder defined defined a dataset script (a python file).

            For local datasets:

            - if ``path`` is a local directory (but doesn't contain a dataset script)
              -> load a generic dataset builder (csv, json, text etc.) based on the content of the directory
              e.g. ``'./path/to/directory/with/my/csv/data'``.
            - if ``path`` is a local dataset script or a directory containing a local dataset script (if the script has the same name as the directory):
              -> load the dataset builder from the dataset script
              e.g. ``'./dataset/squad'`` or ``'./dataset/squad/squad.py'``.

            For datasets on the Hugging Face Hub (list all available datasets and ids with ``datasets.list_datasets()``)

            - if ``path`` is a canonical dataset on the HF Hub (ex: `glue`, `squad`)
              -> load the dataset builder from the dataset script in the github repository at huggingface/datasets
              e.g. ``'squad'`` or ``'glue'``.
            - if ``path`` is a dataset repository on the HF hub (without a dataset script)
              -> load a generic dataset builder (csv, text etc.) based on the content of the repository
              e.g. ``'username/dataset_name'``, a dataset repository on the HF hub containing your data files.
            - if ``path`` is a dataset repository on the HF hub with a dataset script (if the script has the same name as the directory)
              -> load the dataset builder from the dataset script in the dataset repository
              e.g. ``'username/dataset_name'``, a dataset repository on the HF hub containing a dataset script `'dataset_name.py'`.

        name (:obj:`str`, optional): Defining the name of the dataset configuration.
        data_dir (:obj:`str`, optional): Defining the data_dir of the dataset configuration.
        data_files (:obj:`str` or :obj:`Sequence` or :obj:`Mapping`, optional): Path(s) to source data file(s).
        split (:class:`Split` or :obj:`str`): Which split of the data to load.
            If None, will return a `dict` with all splits (typically `datasets.Split.TRAIN` and `datasets.Split.TEST`).
            If given, will return a single Dataset.
            Splits can be combined and specified like in tensorflow-datasets.
        cache_dir (:obj:`str`, optional): Directory to read/write data. Defaults to "~/.cache/huggingface/datasets".
        features (:class:`Features`, optional): Set the features type to use for this dataset.
        download_config (:class:`~utils.DownloadConfig`, optional): Specific download configuration parameters.
        download_mode (:class:`GenerateMode`, default ``REUSE_DATASET_IF_EXISTS``): Download/generate mode.
        ignore_verifications (:obj:`bool`, default ``False``): Ignore the verifications of the downloaded/processed dataset information (checksums/size/splits/...).
        keep_in_memory (:obj:`bool`, default ``None``): Whether to copy the dataset in-memory. If `None`, the dataset
            will not be copied in-memory unless explicitly enabled by setting `datasets.config.IN_MEMORY_MAX_SIZE` to
            nonzero. See more details in the :ref:`load_dataset_enhancing_performance` section.
        save_infos (:obj:`bool`, default ``False``): Save the dataset information (checksums/size/splits/...).
        revision (:class:`~utils.Version` or :obj:`str`, optional): Version of the dataset script to load:

            - For canonical datasets in the `huggingface/datasets` library like "squad", the default version of the module is the local version of the lib.
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
        script_version:
            .. deprecated:: 1.13
                'script_version' was renamed to 'revision' in version 1.13 and will be removed in 1.15.
        **config_kwargs: Keyword arguments to be passed to the :class:`BuilderConfig` and used in the :class:`DatasetBuilder`.

    Returns:
        :class:`Dataset` or :class:`DatasetDict`:
        - if `split` is not None: the dataset requested,
        - if `split` is None, a ``datasets.DatasetDict`` with each split.

        or :class:`IterableDataset` or :class:`IterableDatasetDict`: if streaming=True

        - if `split` is not None: the dataset requested,
        - if `split` is None, a ``datasets.streaming.IterableDatasetDict`` with each split.

    """
    if script_version != "deprecated":
        warnings.warn(
            "'script_version' was renamed to 'revision' in version 1.13 and will be removed in 1.15.", FutureWarning
        )
        revision = script_version
    ignore_verifications = ignore_verifications or save_infos

    # Create a dataset builder
    builder_instance = load_dataset_builder(
        path=path,
        name=name,
        data_dir=data_dir,
        data_files=data_files,
        cache_dir=cache_dir,
        features=features,
        download_config=download_config,
        download_mode=download_mode,
        revision=revision,
        use_auth_token=use_auth_token,
        **config_kwargs,
    )

    # Return iterable dataset in case of streaming
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
    Loads a dataset that was previously saved using :meth:`Dataset.save_to_disk` from a dataset directory, or
    from a filesystem using either :class:`datasets.filesystems.S3FileSystem` or any implementation of
    ``fsspec.spec.AbstractFileSystem``.

    Args:
        dataset_path (:obj:`str`): Path (e.g. `"dataset/train"`) or remote URI (e.g.
            `"s3://my-bucket/dataset/train"`) of the Dataset or DatasetDict directory where the dataset will be
            loaded from.
        fs (:class:`~filesystems.S3FileSystem` or ``fsspec.spec.AbstractFileSystem``, optional, default ``None``):
            Instance of of the remote filesystem used to download the files from.
        keep_in_memory (:obj:`bool`, default ``None``): Whether to copy the dataset in-memory. If `None`, the dataset
            will not be copied in-memory unless explicitly enabled by setting `datasets.config.IN_MEMORY_MAX_SIZE` to
            nonzero. See more details in the :ref:`load_dataset_enhancing_performance` section.

    Returns:
        :class:`Dataset` or :class:`DatasetDict`:
        - If `dataset_path` is a path of a dataset directory: the dataset requested.
        - If `dataset_path` is a path of a dataset dict directory: a ``datasets.DatasetDict`` with each split.
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
