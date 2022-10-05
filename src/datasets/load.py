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
import shutil
import time
import warnings
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Sequence, Tuple, Type, Union

import fsspec
import requests
from huggingface_hub import HfApi

from . import config
from .arrow_dataset import Dataset
from .builder import DatasetBuilder
from .data_files import (
    DEFAULT_PATTERNS_ALL,
    DataFilesDict,
    DataFilesList,
    EmptyDatasetError,
    get_data_patterns_in_dataset_repository,
    get_data_patterns_locally,
    get_metadata_patterns_in_dataset_repository,
    get_metadata_patterns_locally,
    sanitize_patterns,
)
from .dataset_dict import DatasetDict, IterableDatasetDict
from .download.download_config import DownloadConfig
from .download.download_manager import DownloadMode
from .download.streaming_download_manager import StreamingDownloadManager, xglob, xjoin
from .features import Features
from .filesystems import extract_path_from_uri, is_remote_filesystem
from .info import DatasetInfo, DatasetInfosDict
from .iterable_dataset import IterableDataset
from .metric import Metric
from .packaged_modules import (
    _EXTENSION_TO_MODULE,
    _MODULE_SUPPORTS_METADATA,
    _PACKAGED_DATASETS_MODULES,
    _hash_python_lines,
)
from .splits import Split
from .tasks import TaskTemplate
from .utils._hf_hub_fixes import dataset_info as hf_api_dataset_info
from .utils.deprecation_utils import deprecated
from .utils.file_utils import (
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
from .utils.metadata import DatasetMetadata
from .utils.py_utils import get_imports
from .utils.version import Version


logger = get_logger(__name__)

ALL_ALLOWED_EXTENSIONS = list(_EXTENSION_TO_MODULE.keys()) + ["zip"]


def init_dynamic_modules(
    name: str = config.MODULE_NAME_FOR_DYNAMIC_MODULES, hf_modules_cache: Optional[Union[Path, str]] = None
):
    """
    Create a module with name `name` in which you can add dynamic modules
    such as metrics or datasets. The module can be imported using its name.
    The module is created in the HF_MODULE_CACHE directory by default (~/.cache/huggingface/modules) but it can
    be overridden by specifying a path to another directory in `hf_modules_cache`.
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
        if inspect.isclass(obj) and issubclass(obj, main_cls_type):
            if inspect.isabstract(obj):
                continue
            module_main_cls = obj
            obj_module = inspect.getmodule(obj)
            if obj_module is not None and module == obj_module:
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
        with open(file_path, encoding="utf-8") as f:
            lines.extend(f.readlines())
    return _hash_python_lines(lines)


def increase_load_count(name: str, resource_type: str):
    """Update the download count of a dataset or metric."""
    if not config.HF_DATASETS_OFFLINE and config.HF_UPDATE_DOWNLOAD_COUNTS:
        try:
            head_hf_s3(name, filename=name + ".py", dataset=(resource_type == "dataset"))
        except Exception:
            pass


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
    download_config = download_config.copy()
    if download_config.download_desc is None:
        download_config.download_desc = "Downloading extra modules"
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
    needs_to_be_installed = {}
    for library_import_name, library_import_path in library_imports:
        try:
            lib = importlib.import_module(library_import_name)  # noqa F841
        except ImportError:
            if library_import_name not in needs_to_be_installed or library_import_path != library_import_name:
                needs_to_be_installed[library_import_name] = library_import_path
    if needs_to_be_installed:
        _dependencies_str = "dependencies" if len(needs_to_be_installed) > 1 else "dependency"
        _them_str = "them" if len(needs_to_be_installed) > 1 else "it"
        raise ImportError(
            f"To be able to use {name}, you need to install the following {_dependencies_str}: "
            f"{', '.join(needs_to_be_installed)}.\nPlease install {_them_str} using 'pip install "
            f"{' '.join(needs_to_be_installed.values())}' for instance."
        )
    return local_imports


def _copy_script_and_other_resources_in_importable_dir(
    name: str,
    importable_directory_path: str,
    subdirectory_name: str,
    original_local_path: str,
    local_imports: List[Tuple[str, str]],
    additional_files: List[Tuple[str, str]],
    download_mode: Optional[DownloadMode],
) -> str:
    """Copy a script and its required imports to an importable directory

    Args:
        name (str): name of the resource to load
        importable_directory_path (str): path to the loadable folder in the dynamic modules directory
        subdirectory_name (str): name of the subdirectory in importable_directory_path in which to place the script
        original_local_path (str): local path to the resource script
        local_imports (List[Tuple[str, str]]): list of (destination_filename, import_file_to_copy)
        additional_files (List[Tuple[str, str]]): list of (destination_filename, additional_file_to_copy)
        download_mode (Optional[DownloadMode]): download mode

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
        if download_mode == DownloadMode.FORCE_REDOWNLOAD and os.path.exists(importable_directory_path):
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
        # Use os.path.splitext to split extension from importable_local_file
        meta_path = os.path.splitext(importable_local_file)[0] + ".json"
        if not os.path.exists(meta_path):
            meta = {"original file path": original_local_path, "local file path": importable_local_file}
            # the filename is *.py in our case, so better rename to filename.json instead of filename.py.json
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

        # Copy additional files like dataset_infos.json file if needed
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
    download_mode: DownloadMode,
) -> Tuple[str, str]:
    importable_directory_path = os.path.join(dynamic_modules_path, module_namespace, name.replace("/", "--"))
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
        [os.path.basename(dynamic_modules_path), module_namespace, name.replace("/", "--"), hash, name.split("/")[-1]]
    )
    return module_path, hash


def infer_module_for_data_files(
    data_files_list: DataFilesList, use_auth_token: Optional[Union[bool, str]] = None
) -> Optional[Tuple[str, str]]:
    """Infer module (and builder kwargs) from list of data files.

    Args:
        data_files_list (DataFilesList): List of data files.
        use_auth_token (bool or str, optional): Whether to use token or token to authenticate on the Hugging Face Hub
            for private remote files.

    Returns:
        tuple[str, str]: Tuple with
            - inferred module name
            - builder kwargs
    """
    extensions_counter = Counter(
        suffix[1:]
        for filepath in data_files_list[: config.DATA_FILES_MAX_NUMBER_FOR_MODULE_INFERENCE]
        for suffix in Path(filepath).suffixes
    )
    if extensions_counter:
        for ext, _ in extensions_counter.most_common():
            if ext in _EXTENSION_TO_MODULE:
                return _EXTENSION_TO_MODULE[ext]
            elif ext == "zip":
                return infer_module_for_data_files_in_archives(data_files_list, use_auth_token=use_auth_token)


def infer_module_for_data_files_in_archives(
    data_files_list: DataFilesList, use_auth_token: Optional[Union[bool, str]]
) -> Optional[Tuple[str, str]]:
    """Infer module (and builder kwargs) from list of archive data files.

    Args:
        data_files_list (DataFilesList): List of data files.
        use_auth_token (bool or str, optional): Whether to use token or token to authenticate on the Hugging Face Hub
            for private remote files.

    Returns:
        tuple[str, str]: Tuple with
            - inferred module name
            - builder kwargs
    """
    archived_files = []
    archive_files_counter = 0
    for filepath in data_files_list:
        if str(filepath).endswith(".zip"):
            archive_files_counter += 1
            if archive_files_counter > config.GLOBBED_DATA_FILES_MAX_NUMBER_FOR_MODULE_INFERENCE:
                break
            extracted = xjoin(StreamingDownloadManager().extract(filepath), "**")
            archived_files += [
                f.split("::")[0]
                for f in xglob(extracted, recursive=True, use_auth_token=use_auth_token)[
                    : config.ARCHIVED_DATA_FILES_MAX_NUMBER_FOR_MODULE_INFERENCE
                ]
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


class GithubMetricModuleFactory(_MetricModuleFactory):
    """Get the module of a metric. The metric script is downloaded from GitHub.

    <Deprecated version="2.5.0">

    Use the new library 🤗 Evaluate instead: https://huggingface.co/docs/evaluate

    </Deprecated>
    """

    @deprecated("Use the new library 🤗 Evaluate instead: https://huggingface.co/docs/evaluate")
    def __init__(
        self,
        name: str,
        revision: Optional[Union[str, Version]] = None,
        download_config: Optional[DownloadConfig] = None,
        download_mode: Optional[DownloadMode] = None,
        dynamic_modules_path: Optional[str] = None,
    ):
        self.name = name
        self.revision = revision
        self.download_config = download_config.copy() if download_config else DownloadConfig()
        if self.download_config.max_retries < 3:
            self.download_config.max_retries = 3
        self.download_mode = download_mode
        self.dynamic_modules_path = dynamic_modules_path
        assert self.name.count("/") == 0
        increase_load_count(name, resource_type="metric")

    def download_loading_script(self, revision: Optional[str]) -> str:
        file_path = hf_github_url(path=self.name, name=self.name + ".py", revision=revision, dataset=False)
        download_config = self.download_config.copy()
        if download_config.download_desc is None:
            download_config.download_desc = "Downloading builder script"
        return cached_path(file_path, download_config=download_config)

    def get_module(self) -> MetricModule:
        # get script and other files
        revision = self.revision
        try:
            local_path = self.download_loading_script(revision)
            revision = self.revision
        except FileNotFoundError:
            if revision is not None:
                raise
            else:
                revision = "main"
                local_path = self.download_loading_script(revision)
                logger.warning(
                    f"Couldn't find a directory or a metric named '{self.name}' in this version. "
                    f"It was picked from the main branch on github instead."
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
    """Get the module of a local metric. The metric script is loaded from a local script.

    <Deprecated version="2.5.0">

    Use the new library 🤗 Evaluate instead: https://huggingface.co/docs/evaluate

    </Deprecated>
    """

    @deprecated("Use the new library 🤗 Evaluate instead: https://huggingface.co/docs/evaluate")
    def __init__(
        self,
        path: str,
        download_config: Optional[DownloadConfig] = None,
        download_mode: Optional[DownloadMode] = None,
        dynamic_modules_path: Optional[str] = None,
    ):
        self.path = path
        self.name = Path(path).stem
        self.download_config = download_config or DownloadConfig()
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
        download_mode: Optional[DownloadMode] = None,
        dynamic_modules_path: Optional[str] = None,
    ):
        self.path = path
        self.name = Path(path).stem
        self.download_config = download_config or DownloadConfig()
        self.download_mode = download_mode
        self.dynamic_modules_path = dynamic_modules_path

    def get_module(self) -> DatasetModule:
        # get script and other files
        dataset_infos_path = Path(self.path).parent / config.DATASETDICT_INFOS_FILENAME
        dataset_readme_path = Path(self.path).parent / "README.md"
        imports = get_imports(self.path)
        local_imports = _download_additional_modules(
            name=self.name,
            base_path=str(Path(self.path).parent),
            imports=imports,
            download_config=self.download_config,
        )
        additional_files = []
        if dataset_infos_path.is_file():
            additional_files.append((config.DATASETDICT_INFOS_FILENAME, str(dataset_infos_path)))
        if dataset_readme_path.is_file():
            additional_files.append(("README.md", dataset_readme_path))
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
    """Get the module of a dataset loaded from the user's data files. The dataset builder module to use is inferred
    from the data files extensions."""

    def __init__(
        self,
        path: str,
        data_dir: Optional[str] = None,
        data_files: Optional[Union[str, List, Dict]] = None,
        download_mode: Optional[DownloadMode] = None,
    ):
        if data_dir and os.path.isabs(data_dir):
            raise ValueError(f"`data_dir` must be relative to a dataset directory's root: {path}")

        self.path = path
        self.name = Path(path).stem
        self.data_files = data_files
        self.data_dir = data_dir
        self.download_mode = download_mode

    def get_module(self) -> DatasetModule:
        base_path = os.path.join(self.path, self.data_dir) if self.data_dir else self.path
        patterns = (
            sanitize_patterns(self.data_files) if self.data_files is not None else get_data_patterns_locally(base_path)
        )
        data_files = DataFilesDict.from_local_or_remote(
            patterns,
            base_path=base_path,
            allowed_extensions=ALL_ALLOWED_EXTENSIONS,
        )
        module_names = {
            key: infer_module_for_data_files(data_files_list) for key, data_files_list in data_files.items()
        }
        if len(set(list(zip(*module_names.values()))[0])) > 1:
            raise ValueError(f"Couldn't infer the same data file format for all splits. Got {module_names}")
        module_name, builder_kwargs = next(iter(module_names.values()))
        if not module_name:
            raise FileNotFoundError(f"No data files or dataset script found in {self.path}")
        # Collect metadata files if the module supports them
        if self.data_files is None and module_name in _MODULE_SUPPORTS_METADATA and patterns != DEFAULT_PATTERNS_ALL:
            try:
                metadata_patterns = get_metadata_patterns_locally(base_path)
            except FileNotFoundError:
                metadata_patterns = None
            if metadata_patterns is not None:
                metadata_files = DataFilesList.from_local_or_remote(metadata_patterns, base_path=base_path)
                for key in data_files:
                    data_files[key] = DataFilesList(
                        data_files[key] + metadata_files,
                        data_files[key].origin_metadata + metadata_files.origin_metadata,
                    )
        module_path, hash = _PACKAGED_DATASETS_MODULES[module_name]
        builder_kwargs = {
            "hash": hash,
            "data_files": data_files,
            "config_name": os.path.basename(self.path.rstrip("/")),
            "base_path": self.path,
            **builder_kwargs,
        }
        if os.path.isfile(os.path.join(self.path, config.DATASETDICT_INFOS_FILENAME)):
            with open(os.path.join(self.path, config.DATASETDICT_INFOS_FILENAME), encoding="utf-8") as f:
                dataset_infos: DatasetInfosDict = json.load(f)
            if dataset_infos:
                builder_kwargs["config_name"] = next(iter(dataset_infos))
                builder_kwargs["info"] = DatasetInfo.from_dict(next(iter(dataset_infos.values())))
        if os.path.isfile(os.path.join(self.path, "README.md")):
            dataset_metadata = DatasetMetadata.from_readme(Path(self.path) / "README.md")
            if isinstance(dataset_metadata.get("dataset_info"), list) and dataset_metadata["dataset_info"]:
                dataset_info_dict = dataset_metadata["dataset_info"][0]
                builder_kwargs["info"] = DatasetInfo._from_yaml_dict(dataset_info_dict)
                if "config_name" in dataset_info_dict:
                    builder_kwargs["config_name"] = dataset_info_dict["config_name"]
            elif isinstance(dataset_metadata.get("dataset_info"), dict) and dataset_metadata["dataset_info"]:
                dataset_info_dict = dataset_metadata["dataset_info"]
                builder_kwargs["info"] = DatasetInfo._from_yaml_dict(dataset_info_dict)
                if "config_name" in dataset_info_dict:
                    builder_kwargs["config_name"] = dataset_info_dict["config_name"]
        return DatasetModule(module_path, hash, builder_kwargs)


class PackagedDatasetModuleFactory(_DatasetModuleFactory):
    """Get the dataset builder module from the ones that are packaged with the library: csv, json, etc."""

    def __init__(
        self,
        name: str,
        data_dir: Optional[str] = None,
        data_files: Optional[Union[str, List, Dict]] = None,
        download_config: Optional[DownloadConfig] = None,
        download_mode: Optional[DownloadMode] = None,
    ):

        self.name = name
        self.data_files = data_files
        self.data_dir = data_dir
        self.download_config = download_config
        self.download_mode = download_mode
        increase_load_count(name, resource_type="dataset")

    def get_module(self) -> DatasetModule:
        base_path = str(Path(self.data_dir).resolve()) if self.data_dir is not None else str(Path().resolve())
        patterns = (
            sanitize_patterns(self.data_files) if self.data_files is not None else get_data_patterns_locally(base_path)
        )
        data_files = DataFilesDict.from_local_or_remote(
            patterns,
            use_auth_token=self.download_config.use_auth_token,
            base_path=base_path,
        )
        if self.data_files is None and self.name in _MODULE_SUPPORTS_METADATA and patterns != DEFAULT_PATTERNS_ALL:
            try:
                metadata_patterns = get_metadata_patterns_locally(base_path)
            except FileNotFoundError:
                metadata_patterns = None
            if metadata_patterns is not None:
                metadata_files = DataFilesList.from_local_or_remote(
                    metadata_patterns, use_auth_token=self.download_config.use_auth_token, base_path=base_path
                )
                for key in data_files:
                    data_files[key] = DataFilesList(
                        data_files[key] + metadata_files,
                        data_files[key].origin_metadata + metadata_files.origin_metadata,
                    )
        module_path, hash = _PACKAGED_DATASETS_MODULES[self.name]
        builder_kwargs = {"hash": hash, "data_files": data_files}
        return DatasetModule(module_path, hash, builder_kwargs)


class HubDatasetModuleFactoryWithoutScript(_DatasetModuleFactory):
    """
    Get the module of a dataset loaded from data files of a dataset repository.
    The dataset builder module to use is inferred from the data files extensions.
    """

    def __init__(
        self,
        name: str,
        revision: Optional[Union[str, Version]] = None,
        data_dir: Optional[str] = None,
        data_files: Optional[Union[str, List, Dict]] = None,
        download_config: Optional[DownloadConfig] = None,
        download_mode: Optional[DownloadMode] = None,
    ):

        self.name = name
        self.revision = revision
        self.data_files = data_files
        self.data_dir = data_dir
        self.download_config = download_config or DownloadConfig()
        self.download_mode = download_mode
        increase_load_count(name, resource_type="dataset")

    def get_module(self) -> DatasetModule:
        hfh_dataset_info = hf_api_dataset_info(
            HfApi(config.HF_ENDPOINT),
            self.name,
            revision=self.revision,
            use_auth_token=self.download_config.use_auth_token,
            timeout=100.0,
        )
        patterns = (
            sanitize_patterns(self.data_files)
            if self.data_files is not None
            else get_data_patterns_in_dataset_repository(hfh_dataset_info, self.data_dir)
        )
        data_files = DataFilesDict.from_hf_repo(
            patterns,
            dataset_info=hfh_dataset_info,
            base_path=self.data_dir,
            allowed_extensions=ALL_ALLOWED_EXTENSIONS,
        )
        module_names = {
            key: infer_module_for_data_files(data_files_list, use_auth_token=self.download_config.use_auth_token)
            for key, data_files_list in data_files.items()
        }
        if len(set(list(zip(*module_names.values()))[0])) > 1:
            raise ValueError(f"Couldn't infer the same data file format for all splits. Got {module_names}")
        module_name, builder_kwargs = next(iter(module_names.values()))
        if not module_name:
            raise FileNotFoundError(f"No data files or dataset script found in {self.name}")
        # Collect metadata files if the module supports them
        if self.data_files is None and module_name in _MODULE_SUPPORTS_METADATA and patterns != DEFAULT_PATTERNS_ALL:
            try:
                metadata_patterns = get_metadata_patterns_in_dataset_repository(hfh_dataset_info, self.data_dir)
            except FileNotFoundError:
                metadata_patterns = None
            if metadata_patterns is not None:
                metadata_files = DataFilesList.from_hf_repo(
                    metadata_patterns, dataset_info=hfh_dataset_info, base_path=self.data_dir
                )
                for key in data_files:
                    data_files[key] = DataFilesList(
                        data_files[key] + metadata_files,
                        data_files[key].origin_metadata + metadata_files.origin_metadata,
                    )
        module_path, hash = _PACKAGED_DATASETS_MODULES[module_name]
        builder_kwargs = {
            "hash": hash,
            "data_files": data_files,
            "config_name": self.name.replace("/", "--"),
            "base_path": hf_hub_url(self.name, "", revision=self.revision),
            "repo_id": self.name,
            **builder_kwargs,
        }
        download_config = self.download_config.copy()
        if download_config.download_desc is None:
            download_config.download_desc = "Downloading metadata"
        try:
            dataset_infos_path = cached_path(
                hf_hub_url(self.name, config.DATASETDICT_INFOS_FILENAME, revision=self.revision),
                download_config=download_config,
            )
            with open(dataset_infos_path, encoding="utf-8") as f:
                dataset_infos: DatasetInfosDict = json.load(f)
            if dataset_infos:
                builder_kwargs["config_name"] = next(iter(dataset_infos))
                builder_kwargs["info"] = DatasetInfo.from_dict(next(iter(dataset_infos.values())))
        except FileNotFoundError:
            pass
        download_config = self.download_config.copy()
        if download_config.download_desc is None:
            download_config.download_desc = "Downloading readme"
        try:
            dataset_readme_path = cached_path(
                hf_hub_url(self.name, "README.md", revision=self.revision),
                download_config=download_config,
            )
            dataset_metadata = DatasetMetadata.from_readme(Path(dataset_readme_path))
            if isinstance(dataset_metadata.get("dataset_info"), list) and dataset_metadata["dataset_info"]:
                dataset_info_dict = dataset_metadata["dataset_info"][0]
                builder_kwargs["info"] = DatasetInfo._from_yaml_dict(dataset_info_dict)
                if "config_name" in dataset_info_dict:
                    builder_kwargs["config_name"] = dataset_info_dict["config_name"]
            elif isinstance(dataset_metadata.get("dataset_info"), dict) and dataset_metadata["dataset_info"]:
                dataset_info_dict = dataset_metadata["dataset_info"]
                builder_kwargs["info"] = DatasetInfo._from_yaml_dict(dataset_info_dict)
                if "config_name" in dataset_info_dict:
                    builder_kwargs["config_name"] = dataset_info_dict["config_name"]

        except FileNotFoundError:
            pass
        return DatasetModule(module_path, hash, builder_kwargs)


class HubDatasetModuleFactoryWithScript(_DatasetModuleFactory):
    """Get the module of a dataset from a dataset repository. The dataset script comes from the script inside the dataset repository."""

    def __init__(
        self,
        name: str,
        revision: Optional[Union[str, Version]] = None,
        download_config: Optional[DownloadConfig] = None,
        download_mode: Optional[DownloadMode] = None,
        dynamic_modules_path: Optional[str] = None,
    ):
        self.name = name
        self.revision = revision
        self.download_config = download_config or DownloadConfig()
        self.download_mode = download_mode
        self.dynamic_modules_path = dynamic_modules_path
        increase_load_count(name, resource_type="dataset")

    def download_loading_script(self) -> str:
        file_path = hf_hub_url(repo_id=self.name, path=self.name.split("/")[-1] + ".py", revision=self.revision)
        download_config = self.download_config.copy()
        if download_config.download_desc is None:
            download_config.download_desc = "Downloading builder script"
        return cached_path(file_path, download_config=download_config)

    def download_dataset_infos_file(self) -> str:
        dataset_infos = hf_hub_url(repo_id=self.name, path=config.DATASETDICT_INFOS_FILENAME, revision=self.revision)
        # Download the dataset infos file if available
        download_config = self.download_config.copy()
        if download_config.download_desc is None:
            download_config.download_desc = "Downloading metadata"
        try:
            return cached_path(
                dataset_infos,
                download_config=download_config,
            )
        except (FileNotFoundError, ConnectionError):
            return None

    def download_dataset_readme_file(self) -> str:
        readme_url = hf_hub_url(repo_id=self.name, path="README.md", revision=self.revision)
        # Download the dataset infos file if available
        download_config = self.download_config.copy()
        if download_config.download_desc is None:
            download_config.download_desc = "Downloading readme"
        try:
            return cached_path(
                readme_url,
                download_config=download_config,
            )
        except (FileNotFoundError, ConnectionError):
            return None

    def get_module(self) -> DatasetModule:
        # get script and other files
        local_path = self.download_loading_script()
        dataset_infos_path = self.download_dataset_infos_file()
        dataset_readme_path = self.download_dataset_readme_file()
        imports = get_imports(local_path)
        local_imports = _download_additional_modules(
            name=self.name,
            base_path=hf_hub_url(repo_id=self.name, path="", revision=self.revision),
            imports=imports,
            download_config=self.download_config,
        )
        additional_files = []
        if dataset_infos_path:
            additional_files.append((config.DATASETDICT_INFOS_FILENAME, dataset_infos_path))
        if dataset_readme_path:
            additional_files.append(("README.md", dataset_readme_path))
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
            "repo_id": self.name,
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
        importable_directory_path = os.path.join(dynamic_modules_path, "datasets", self.name.replace("/", "--"))
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
        warning_msg = (
            f"Using the latest cached version of the module from {os.path.join(importable_directory_path, hash)} "
            f"(last modified on {time.ctime(_get_modification_time(hash))}) since it "
            f"couldn't be found locally at {self.name}."
        )
        if not config.HF_DATASETS_OFFLINE:
            warning_msg += ", or remotely on the Hugging Face Hub."
        logger.warning(warning_msg)
        # make the new module to be noticed by the import system
        module_path = ".".join(
            [
                os.path.basename(dynamic_modules_path),
                "datasets",
                self.name.replace("/", "--"),
                hash,
                self.name.split("/")[-1],
            ]
        )
        importlib.invalidate_caches()
        builder_kwargs = {
            "hash": hash,
            "repo_id": self.name,
        }
        return DatasetModule(module_path, hash, builder_kwargs)


class CachedMetricModuleFactory(_MetricModuleFactory):
    """
    Get the module of a metric that has been loaded once already and cached.
    The script that is loaded from the cache is the most recent one with a matching name.

    <Deprecated version="2.5.0">

    Use the new library 🤗 Evaluate instead: https://huggingface.co/docs/evaluate

    </Deprecated>
    """

    @deprecated("Use the new library 🤗 Evaluate instead: https://huggingface.co/docs/evaluate")
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
    download_mode: Optional[DownloadMode] = None,
    dynamic_modules_path: Optional[str] = None,
    data_dir: Optional[str] = None,
    data_files: Optional[Union[Dict, List, str, DataFilesDict]] = None,
    **download_kwargs,
) -> DatasetModule:
    """
    Download/extract/cache a dataset module.

    Dataset codes are cached inside the dynamic modules cache to allow easy import (avoid ugly sys.path tweaks).

    Args:

        path (str): Path or name of the dataset.
            Depending on ``path``, the dataset builder that is used comes from a generic dataset script (JSON, CSV, Parquet, text etc.) or from the dataset script (a python file) inside the dataset directory.

            For local datasets:

            - if ``path`` is a local directory (containing data files only)
              -> load a generic dataset builder (csv, json, text etc.) based on the content of the directory
              e.g. ``'./path/to/directory/with/my/csv/data'``.
            - if ``path`` is a local dataset script or a directory containing a local dataset script (if the script has the same name as the directory):
              -> load the dataset builder from the dataset script
              e.g. ``'./dataset/squad'`` or ``'./dataset/squad/squad.py'``.

            For datasets on the Hugging Face Hub (list all available datasets and ids with ``datasets.list_datasets()``)

            - if ``path`` is a dataset repository on the HF hub (containing data files only)
              -> load a generic dataset builder (csv, text etc.) based on the content of the repository
              e.g. ``'username/dataset_name'``, a dataset repository on the HF hub containing your data files.
            - if ``path`` is a dataset repository on the HF hub with a dataset script (if the script has the same name as the directory)
              -> load the dataset builder from the dataset script in the dataset repository
              e.g. ``glue``, ``squad``, ``'username/dataset_name'``, a dataset repository on the HF hub containing a dataset script `'dataset_name.py'`.

        revision (:class:`~utils.Version` or :obj:`str`, optional): Version of the dataset script to load:

            - For datasets in the `huggingface/datasets` library on GitHub like "squad", the default version of the module is the local version of the lib.
              You can specify a different version from your local version of the lib (e.g. "main" or "1.2.0") but it might cause compatibility issues.
            - For community datasets like "lhoestq/squad" that have their own git repository on the Datasets Hub, the default version "main" corresponds to the "main" branch.
              You can specify a different version that the default "main" by using a commit sha or a git tag of the dataset repository.
        download_config (:class:`DownloadConfig`, optional): Specific download configuration parameters.
        download_mode (:class:`DownloadMode`, default ``REUSE_DATASET_IF_EXISTS``): Download/generate mode.
        dynamic_modules_path (Optional str, defaults to HF_MODULES_CACHE / "datasets_modules", i.e. ~/.cache/huggingface/modules/datasets_modules):
            Optional path to the directory in which the dynamic modules are saved. It must have been initialized with :obj:`init_dynamic_modules`.
            By default, the datasets and metrics are stored inside the `datasets_modules` module.
        data_dir (:obj:`str`, optional): Directory with the data files. Used only if `data_files` is not specified,
            in which case it's equal to pass `os.path.join(data_dir, "**")` as `data_files`.
        data_files (:obj:`Union[Dict, List, str]`, optional): Defining the data_files of the dataset configuration.
        **download_kwargs (additional keyword arguments): optional attributes for DownloadConfig() which will override
            the attributes in download_config if supplied.

    Returns:
        DatasetModule
    """
    if download_config is None:
        download_config = DownloadConfig(**download_kwargs)
    download_mode = DownloadMode(download_mode or DownloadMode.REUSE_DATASET_IF_EXISTS)
    download_config.extract_compressed_file = True
    download_config.force_extract = True
    download_config.force_download = download_mode == DownloadMode.FORCE_REDOWNLOAD

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
    # - if path has no "/" and is a module on GitHub (in /datasets)
    #   -> use the module from the python file on GitHub
    #   Note that this case will be removed in favor of loading from the HF Hub instead eventually
    # - if path has one "/" and is dataset repository on the HF hub with a python file
    #   -> the module from the python file in the dataset repository
    # - if path has one "/" and is dataset repository on the HF hub without a python file
    #   -> use a packaged module (csv, text etc.) based on content of the repository

    # Try packaged
    if path in _PACKAGED_DATASETS_MODULES:
        return PackagedDatasetModuleFactory(
            path,
            data_dir=data_dir,
            data_files=data_files,
            download_config=download_config,
            download_mode=download_mode,
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
            path, data_dir=data_dir, data_files=data_files, download_mode=download_mode
        ).get_module()
    # Try remotely
    elif is_relative_path(path) and path.count("/") <= 1:
        try:
            _raise_if_offline_mode_is_enabled()
            hf_api = HfApi(config.HF_ENDPOINT)
            try:
                dataset_info = hf_api_dataset_info(
                    hf_api,
                    repo_id=path,
                    revision=revision,
                    use_auth_token=download_config.use_auth_token,
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
                elif "401" in str(e):
                    msg = f"Dataset '{path}' doesn't exist on the Hub"
                    msg = msg + f" at revision '{revision}'" if revision else msg
                    raise FileNotFoundError(
                        msg
                        + ". If the repo is private, make sure you are authenticated with `use_auth_token=True` after logging in with `huggingface-cli login`."
                    )
                else:
                    raise e
            if filename in [sibling.rfilename for sibling in dataset_info.siblings]:
                return HubDatasetModuleFactoryWithScript(
                    path,
                    revision=revision,
                    download_config=download_config,
                    download_mode=download_mode,
                    dynamic_modules_path=dynamic_modules_path,
                ).get_module()
            else:
                return HubDatasetModuleFactoryWithoutScript(
                    path,
                    revision=revision,
                    data_dir=data_dir,
                    data_files=data_files,
                    download_config=download_config,
                    download_mode=download_mode,
                ).get_module()
        except Exception as e1:  # noqa: all the attempts failed, before raising the error we should check if the module is already cached.
            try:
                return CachedDatasetModuleFactory(path, dynamic_modules_path=dynamic_modules_path).get_module()
            except Exception as e2:  # noqa: if it's not in the cache, then it doesn't exist.
                if isinstance(e1, OfflineModeIsEnabled):
                    raise ConnectionError(f"Couldn't reach the Hugging Face Hub for dataset '{path}': {e1}") from None
                if isinstance(e1, EmptyDatasetError):
                    raise e1 from None
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


@deprecated("Use the new library 🤗 Evaluate instead: https://huggingface.co/docs/evaluate")
def metric_module_factory(
    path: str,
    revision: Optional[Union[str, Version]] = None,
    download_config: Optional[DownloadConfig] = None,
    download_mode: Optional[DownloadMode] = None,
    dynamic_modules_path: Optional[str] = None,
    **download_kwargs,
) -> MetricModule:
    """
    Download/extract/cache a metric module.

    <Deprecated version="2.5.0">

    Use the new library 🤗 Evaluate instead: https://huggingface.co/docs/evaluate

    </Deprecated>

    Metrics codes are cached inside the dynamic modules cache to allow easy import (avoid ugly sys.path tweaks).

    Args:

        path (str): Path or name of the metric script.

            - if ``path`` is a local metric script or a directory containing a local metric script (if the script has the same name as the directory):
              -> load the module from the metric script
              e.g. ``'./metrics/accuracy'`` or ``'./metrics/accuracy/accuracy.py'``.
            - if ``path`` is a metric on the Hugging Face Hub (ex: `glue`, `squad`)
              -> load the module from the metric script in the GitHub repository at huggingface/datasets
              e.g. ``'accuracy'`` or ``'rouge'``.

        revision (Optional ``Union[str, datasets.Version]``):
            If specified, the module will be loaded from the datasets repository at this version.
            By default:
            - it is set to the local version of the lib.
            - it will also try to load it from the main branch if it's not available at the local version of the lib.
            Specifying a version that is different from your local version of the lib might cause compatibility issues.
        download_config (:class:`DownloadConfig`, optional): Specific download configuration parameters.
        download_mode (:class:`DownloadMode`, default ``REUSE_DATASET_IF_EXISTS``): Download/generate mode.
        dynamic_modules_path (Optional str, defaults to HF_MODULES_CACHE / "datasets_modules", i.e. ~/.cache/huggingface/modules/datasets_modules):
            Optional path to the directory in which the dynamic modules are saved. It must have been initialized with :obj:`init_dynamic_modules`.
            By default, the datasets and metrics are stored inside the `datasets_modules` module.
        **download_kwargs (additional keyword arguments): optional attributes for DownloadConfig() which will override
            the attributes in download_config if supplied.

    Returns:
        MetricModule
    """
    with warnings.catch_warnings():
        # Ignore equivalent warnings to the one already issued
        warnings.filterwarnings("ignore", message=".*https://huggingface.co/docs/evaluate$", category=FutureWarning)

        if download_config is None:
            download_config = DownloadConfig(**download_kwargs)
        download_mode = DownloadMode(download_mode or DownloadMode.REUSE_DATASET_IF_EXISTS)
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
        elif is_relative_path(path) and path.count("/") == 0:
            try:
                return GithubMetricModuleFactory(
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


@deprecated("Use 'evaluate.load' instead, from the new library 🤗 Evaluate: https://huggingface.co/docs/evaluate")
def load_metric(
    path: str,
    config_name: Optional[str] = None,
    process_id: int = 0,
    num_process: int = 1,
    cache_dir: Optional[str] = None,
    experiment_id: Optional[str] = None,
    keep_in_memory: bool = False,
    download_config: Optional[DownloadConfig] = None,
    download_mode: Optional[DownloadMode] = None,
    revision: Optional[Union[str, Version]] = None,
    **metric_init_kwargs,
) -> Metric:
    """Load a `datasets.Metric`.

    <Deprecated version="2.5.0">

    Use `evaluate.load` instead, from the new library 🤗 Evaluate: https://huggingface.co/docs/evaluate

    </Deprecated>

    Args:

        path (``str``):
            path to the metric processing script with the metric builder. Can be either:
                - a local path to processing script or the directory containing the script (if the script has the same name as the directory),
                    e.g. ``'./metrics/rouge'`` or ``'./metrics/rogue/rouge.py'``
                - a metric identifier on the HuggingFace datasets repo (list all available metrics with ``datasets.list_metrics()``)
                    e.g. ``'rouge'`` or ``'bleu'``
        config_name (:obj:`str`, optional): selecting a configuration for the metric (e.g. the GLUE metric has a configuration for each subset)
        process_id (:obj:`int`, optional): for distributed evaluation: id of the process
        num_process (:obj:`int`, optional): for distributed evaluation: total number of processes
        cache_dir (Optional str): path to store the temporary predictions and references (default to `~/.cache/huggingface/metrics/`)
        experiment_id (``str``): A specific experiment id. This is used if several distributed evaluations share the same file system.
            This is useful to compute metrics in distributed setups (in particular non-additive metrics like F1).
        keep_in_memory (bool): Whether to store the temporary results in memory (defaults to False)
        download_config (Optional ``datasets.DownloadConfig``: specific download configuration parameters.
        download_mode (:class:`DownloadMode`, default ``REUSE_DATASET_IF_EXISTS``): Download/generate mode.
        revision (Optional ``Union[str, datasets.Version]``): if specified, the module will be loaded from the datasets repository
            at this version. By default, it is set to the local version of the lib. Specifying a version that is different from
            your local version of the lib might cause compatibility issues.

    Returns:
        `datasets.Metric`

    Example:

    ```py
    >>> from datasets import load_metric
    >>> accuracy = load_metric('accuracy')
    >>> accuracy.compute(references=[1, 0], predictions=[1, 1])
    {'accuracy': 0.5}
    ```
    """
    with warnings.catch_warnings():
        # Ignore equivalent warnings to the one already issued
        warnings.filterwarnings("ignore", message=".*https://huggingface.co/docs/evaluate$", category=FutureWarning)

        download_mode = DownloadMode(download_mode or DownloadMode.REUSE_DATASET_IF_EXISTS)
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
    download_mode: Optional[DownloadMode] = None,
    revision: Optional[Union[str, Version]] = None,
    use_auth_token: Optional[Union[bool, str]] = None,
    **config_kwargs,
) -> DatasetBuilder:
    """Load a dataset builder from the Hugging Face Hub, or a local dataset. A dataset builder can be used to inspect general information that is required to build a dataset (cache directory, config, dataset info, etc.)
    without downloading the dataset itself.

    You can find the list of datasets on the Hub at https://huggingface.co/datasets or with ``datasets.list_datasets()``.

    A dataset is a directory that contains:

    - some data files in generic formats (JSON, CSV, Parquet, text, etc.)
    - and optionally a dataset script, if it requires some code to read the data files. This is used to load any kind of formats or structures.

    Note that dataset scripts can also download and read data files from anywhere - in case your data files already exist online.

    Args:

        path (:obj:`str`): Path or name of the dataset.
            Depending on ``path``, the dataset builder that is used comes from a generic dataset script (JSON, CSV, Parquet, text etc.) or from the dataset script (a python file) inside the dataset directory.

            For local datasets:

            - if ``path`` is a local directory (containing data files only)
              -> load a generic dataset builder (csv, json, text etc.) based on the content of the directory
              e.g. ``'./path/to/directory/with/my/csv/data'``.
            - if ``path`` is a local dataset script or a directory containing a local dataset script (if the script has the same name as the directory):
              -> load the dataset builder from the dataset script
              e.g. ``'./dataset/squad'`` or ``'./dataset/squad/squad.py'``.

            For datasets on the Hugging Face Hub (list all available datasets and ids with ``datasets.list_datasets()``)

            - if ``path`` is a dataset repository on the HF hub (containing data files only)
              -> load a generic dataset builder (csv, text etc.) based on the content of the repository
              e.g. ``'username/dataset_name'``, a dataset repository on the HF hub containing your data files.
            - if ``path`` is a dataset repository on the HF hub with a dataset script (if the script has the same name as the directory)
              -> load the dataset builder from the dataset script in the dataset repository
              e.g. ``glue``, ``squad``, ``'username/dataset_name'``, a dataset repository on the HF hub containing a dataset script `'dataset_name.py'`.

        name (:obj:`str`, optional): Defining the name of the dataset configuration.
        data_dir (:obj:`str`, optional): Defining the data_dir of the dataset configuration. If specified for the generic builders (csv, text etc.) or the Hub datasets and `data_files` is None,
            the behavior is equal to passing `os.path.join(data_dir, **)` as `data_files` to reference all the files in a directory.
        data_files (:obj:`str` or :obj:`Sequence` or :obj:`Mapping`, optional): Path(s) to source data file(s).
        cache_dir (:obj:`str`, optional): Directory to read/write data. Defaults to "~/.cache/huggingface/datasets".
        features (:class:`Features`, optional): Set the features type to use for this dataset.
        download_config (:class:`~utils.DownloadConfig`, optional): Specific download configuration parameters.
        download_mode (:class:`DownloadMode`, default ``REUSE_DATASET_IF_EXISTS``): Download/generate mode.
        revision (:class:`~utils.Version` or :obj:`str`, optional): Version of the dataset script to load:

            - For datasets in the `huggingface/datasets` library on GitHub like "squad", the default version of the module is the local version of the lib.
              You can specify a different version from your local version of the lib (e.g. "main" or "1.2.0") but it might cause compatibility issues.
            - For community datasets like "lhoestq/squad" that have their own git repository on the Datasets Hub, the default version "main" corresponds to the "main" branch.
              You can specify a different version that the default "main" by using a commit sha or a git tag of the dataset repository.
        use_auth_token (``str`` or :obj:`bool`, optional): Optional string or boolean to use as Bearer token for remote files on the Datasets Hub.
            If True, will get token from `"~/.huggingface"`.
        **config_kwargs (additional keyword arguments): Keyword arguments to be passed to the :class:`BuilderConfig`
            and used in the :class:`DatasetBuilder`.

    Returns:
        :class:`DatasetBuilder`

    <Tip>

    Passing `use_auth_token=True` is required when you want to access a private dataset.

    </Tip>


    Example:

    ```py
    >>> from datasets import load_dataset_builder
    >>> ds_builder = load_dataset_builder('rotten_tomatoes')
    >>> ds_builder.info.features
    {'label': ClassLabel(num_classes=2, names=['neg', 'pos'], id=None),
     'text': Value(dtype='string', id=None)}
    ```
    """
    download_mode = DownloadMode(download_mode or DownloadMode.REUSE_DATASET_IF_EXISTS)
    if use_auth_token is not None:
        download_config = download_config.copy() if download_config else DownloadConfig()
        download_config.use_auth_token = use_auth_token
    dataset_module = dataset_module_factory(
        path,
        revision=revision,
        download_config=download_config,
        download_mode=download_mode,
        data_dir=data_dir,
        data_files=data_files,
    )

    # Get dataset builder class from the processing script
    builder_cls = import_main_class(dataset_module.module_path)
    builder_kwargs = dataset_module.builder_kwargs
    data_files = builder_kwargs.pop("data_files", data_files)
    config_name = builder_kwargs.pop("config_name", name)
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
        config_name=config_name,
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
    download_mode: Optional[DownloadMode] = None,
    ignore_verifications: bool = False,
    keep_in_memory: Optional[bool] = None,
    save_infos: bool = False,
    revision: Optional[Union[str, Version]] = None,
    use_auth_token: Optional[Union[bool, str]] = None,
    task: Optional[Union[str, TaskTemplate]] = None,
    streaming: bool = False,
    **config_kwargs,
) -> Union[DatasetDict, Dataset, IterableDatasetDict, IterableDataset]:
    """Load a dataset from the Hugging Face Hub, or a local dataset.

    You can find the list of datasets on the Hub at https://huggingface.co/datasets or with ``datasets.list_datasets()``.

    A dataset is a directory that contains:

    - some data files in generic formats (JSON, CSV, Parquet, text, etc.)
    - and optionally a dataset script, if it requires some code to read the data files. This is used to load any kind of formats or structures.

    Note that dataset scripts can also download and read data files from anywhere - in case your data files already exist online.

    This function does the following under the hood:

        1. Download and import in the library the dataset script from ``path`` if it's not already cached inside the library.

            If the dataset has no dataset script, then a generic dataset script is imported instead (JSON, CSV, Parquet, text, etc.)

            Dataset scripts are small python scripts that define dataset builders. They define the citation, info and format of the dataset,
            contain the path or URL to the original data files and the code to load examples from the original data files.

            You can find the complete list of datasets in the Datasets Hub at https://huggingface.co/datasets

        2. Run the dataset script which will:

            * Download the dataset file from the original URL (see the script) if it's not already available locally or cached.
            * Process and cache the dataset in typed Arrow tables for caching.

                Arrow table are arbitrarily long, typed tables which can store nested objects and be mapped to numpy/pandas/python generic types.
                They can be directly accessed from disk, loaded in RAM or even streamed over the web.

        3. Return a dataset built from the requested splits in ``split`` (default: all).

    It also allows to load a dataset from a local directory or a dataset repository on the Hugging Face Hub without dataset script.
    In this case, it automatically loads all the data files from the directory or the dataset repository.

    Args:

        path (:obj:`str`): Path or name of the dataset.
            Depending on ``path``, the dataset builder that is used comes from a generic dataset script (JSON, CSV, Parquet, text etc.) or from the dataset script (a python file) inside the dataset directory.

            For local datasets:

            - if ``path`` is a local directory (containing data files only)
              -> load a generic dataset builder (csv, json, text etc.) based on the content of the directory
              e.g. ``'./path/to/directory/with/my/csv/data'``.
            - if ``path`` is a local dataset script or a directory containing a local dataset script (if the script has the same name as the directory):
              -> load the dataset builder from the dataset script
              e.g. ``'./dataset/squad'`` or ``'./dataset/squad/squad.py'``.

            For datasets on the Hugging Face Hub (list all available datasets and ids with ``datasets.list_datasets()``)

            - if ``path`` is a dataset repository on the HF hub (containing data files only)
              -> load a generic dataset builder (csv, text etc.) based on the content of the repository
              e.g. ``'username/dataset_name'``, a dataset repository on the HF hub containing your data files.
            - if ``path`` is a dataset repository on the HF hub with a dataset script (if the script has the same name as the directory)
              -> load the dataset builder from the dataset script in the dataset repository
              e.g. ``glue``, ``squad``, ``'username/dataset_name'``, a dataset repository on the HF hub containing a dataset script `'dataset_name.py'`.

        name (:obj:`str`, optional): Defining the name of the dataset configuration.
        data_dir (:obj:`str`, optional): Defining the data_dir of the dataset configuration. If specified for the generic builders (csv, text etc.) or the Hub datasets and `data_files` is None,
            the behavior is equal to passing `os.path.join(data_dir, **)` as `data_files` to reference all the files in a directory.
        data_files (:obj:`str` or :obj:`Sequence` or :obj:`Mapping`, optional): Path(s) to source data file(s).
        split (:class:`Split` or :obj:`str`): Which split of the data to load.
            If None, will return a `dict` with all splits (typically `datasets.Split.TRAIN` and `datasets.Split.TEST`).
            If given, will return a single Dataset.
            Splits can be combined and specified like in tensorflow-datasets.
        cache_dir (:obj:`str`, optional): Directory to read/write data. Defaults to "~/.cache/huggingface/datasets".
        features (:class:`Features`, optional): Set the features type to use for this dataset.
        download_config (:class:`~utils.DownloadConfig`, optional): Specific download configuration parameters.
        download_mode (:class:`DownloadMode`, default ``REUSE_DATASET_IF_EXISTS``): Download/generate mode.
        ignore_verifications (:obj:`bool`, default ``False``): Ignore the verifications of the downloaded/processed dataset information (checksums/size/splits/...).
        keep_in_memory (:obj:`bool`, default ``None``): Whether to copy the dataset in-memory. If `None`, the dataset
            will not be copied in-memory unless explicitly enabled by setting `datasets.config.IN_MEMORY_MAX_SIZE` to
            nonzero. See more details in the :ref:`load_dataset_enhancing_performance` section.
        save_infos (:obj:`bool`, default ``False``): Save the dataset information (checksums/size/splits/...).
        revision (:class:`~utils.Version` or :obj:`str`, optional): Version of the dataset script to load:

            - For datasets in the `huggingface/datasets` library on GitHub like "squad", the default version of the module is the local version of the lib.
              You can specify a different version from your local version of the lib (e.g. "main" or "1.2.0") but it might cause compatibility issues.
            - For community datasets like "lhoestq/squad" that have their own git repository on the Datasets Hub, the default version "main" corresponds to the "main" branch.
              You can specify a different version that the default "main" by using a commit sha or a git tag of the dataset repository.
        use_auth_token (``str`` or :obj:`bool`, optional): Optional string or boolean to use as Bearer token for remote files on the Datasets Hub.
            If True, will get token from `"~/.huggingface"`.
        task (``str``): The task to prepare the dataset for during training and evaluation. Casts the dataset's :class:`Features` to standardized column names and types as detailed in :py:mod:`datasets.tasks`.
        streaming (:obj:`bool`, default ``False``): If set to True, don't download the data files. Instead, it streams the data progressively while
            iterating on the dataset. An IterableDataset or IterableDatasetDict is returned instead in this case.

            Note that streaming works for datasets that use data formats that support being iterated over like txt, csv, jsonl for example.
            Json files may be downloaded completely. Also streaming from remote zip or gzip files is supported but other compressed formats
            like rar and xz are not yet supported. The tgz format doesn't allow streaming.
        **config_kwargs (additional keyword arguments): Keyword arguments to be passed to the :class:`BuilderConfig`
            and used in the :class:`DatasetBuilder`.

    Returns:
        :class:`Dataset` or :class:`DatasetDict`:
        - if `split` is not None: the dataset requested,
        - if `split` is None, a ``datasets.DatasetDict`` with each split.

        or :class:`IterableDataset` or :class:`IterableDatasetDict`: if streaming=True

        - if `split` is not None: the dataset requested,
        - if `split` is None, a ``datasets.streaming.IterableDatasetDict`` with each split.

    <Tip>

    Passing `use_auth_token=True` is required when you want to access a private dataset.

    </Tip>

    Example:

    Load a dataset from the Hugging Face Hub:

    ```py
    >>> from datasets import load_dataset
    >>> ds = load_dataset('rotten_tomatoes', split='train')

    # Map data files to splits
    >>> data_files = {'train': 'train.csv', 'test': 'test.csv'}
    >>> ds = load_dataset('namespace/your_dataset_name', data_files=data_files)
    ```

    Load a local dataset:

    ```py
    # Load a CSV file
    >>> from datasets import load_dataset
    >>> ds = load_dataset('csv', data_files='path/to/local/my_dataset.csv')

    # Load a JSON file
    >>> from datasets import load_dataset
    >>> ds = load_dataset('json', data_files='path/to/local/my_dataset.json')

    # Load from a local loading script
    >>> from datasets import load_dataset
    >>> ds = load_dataset('path/to/local/loading_script/loading_script.py', split='train')
    ```

    Load an [`~datasets.IterableDataset`]:

    ```py
    >>> from datasets import load_dataset
    >>> ds = load_dataset('rotten_tomatoes', split='train', streaming=True)
    ```

    Load an image dataset with the `ImageFolder` dataset builder:

    ```py
    >>> from datasets import load_dataset
    >>> ds = load_dataset('imagefolder', data_dir='/path/to/images', split='train')
    ```
    """
    if Path(path, config.DATASET_STATE_JSON_FILENAME).exists():
        raise ValueError(
            "You are trying to load a dataset that was saved using `save_to_disk`. "
            "Please use `load_from_disk` instead."
        )

    download_mode = DownloadMode(download_mode or DownloadMode.REUSE_DATASET_IF_EXISTS)
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
        return builder_instance.as_streaming_dataset(split=split)

    # Some datasets are already processed on the HF google storage
    # Don't try downloading from Google storage for the packaged datasets as text, json, csv or pandas
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
            Instance of the remote filesystem used to download the files from.
        keep_in_memory (:obj:`bool`, default ``None``): Whether to copy the dataset in-memory. If `None`, the dataset
            will not be copied in-memory unless explicitly enabled by setting `datasets.config.IN_MEMORY_MAX_SIZE` to
            nonzero. See more details in the :ref:`load_dataset_enhancing_performance` section.

    Returns:
        :class:`Dataset` or :class:`DatasetDict`:
        - If `dataset_path` is a path of a dataset directory: the dataset requested.
        - If `dataset_path` is a path of a dataset dict directory: a ``datasets.DatasetDict`` with each split.

    Example:

    ```py
    >>> from datasets import load_from_disk
    >>> ds = load_from_disk('path/to/dataset/directory')
    ```
    """
    # gets filesystem from dataset, either s3:// or file:// and adjusted dataset_path
    if is_remote_filesystem(fs):
        dest_dataset_path = extract_path_from_uri(dataset_path)
    else:
        fs = fsspec.filesystem("file")
        dest_dataset_path = dataset_path

    if not fs.exists(dest_dataset_path):
        raise FileNotFoundError(f"Directory {dataset_path} not found")
    if fs.isfile(Path(dest_dataset_path, config.DATASET_INFO_FILENAME).as_posix()):
        return Dataset.load_from_disk(dataset_path, fs, keep_in_memory=keep_in_memory)
    elif fs.isfile(Path(dest_dataset_path, config.DATASETDICT_JSON_FILENAME).as_posix()):
        return DatasetDict.load_from_disk(dataset_path, fs, keep_in_memory=keep_in_memory)
    else:
        raise FileNotFoundError(
            f"Directory {dataset_path} is neither a dataset directory nor a dataset dict directory."
        )
