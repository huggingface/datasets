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
import glob
import importlib
import inspect
import json
import os
import re
import shutil
import time
import warnings
from collections import Counter
from pathlib import Path, PurePath
from typing import Dict, List, Mapping, Optional, Sequence, Tuple, Type, Union
from urllib.parse import urlparse

import fsspec
import huggingface_hub
from huggingface_hub import HfApi

from . import config
from .arrow_dataset import Dataset
from .builder import DatasetBuilder
from .dataset_dict import DatasetDict, IterableDatasetDict
from .features import Features
from .filesystems import extract_path_from_uri, is_remote_filesystem
from .iterable_dataset import IterableDataset
from .metric import Metric
from .naming import camelcase_to_snakecase
from .packaged_modules import _EXTENSION_TO_MODULE, _PACKAGED_DATASETS_MODULES, hash_python_lines
from .splits import Split
from .streaming import extend_module_for_streaming
from .tasks import TaskTemplate
from .utils.download_manager import GenerateMode
from .utils.file_utils import (
    DownloadConfig,
    cached_path,
    head_hf_s3,
    hf_github_url,
    hf_hub_url,
    init_hf_modules,
    is_relative_path,
    is_remote_url,
    relative_to_absolute_path,
    url_or_path_join,
    url_or_path_parent,
)
from .utils.filelock import FileLock
from .utils.info_utils import is_small_dataset
from .utils.logging import get_logger
from .utils.py_utils import NestedDataStructure
from .utils.version import Version


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


def _resolve_data_files_locally_or_by_urls(
    base_path: str, patterns: Union[str, List[str], Dict], allowed_extensions: Optional[list] = None
) -> Union[List[Path], Dict]:
    """
    Return the absolute paths to all the files that match the given patterns.
    It also supports absolute paths in patterns.
    If an URL is passed, it is returned as is."""
    data_files_ignore = ["README.md", "config.json"]
    if isinstance(patterns, str):
        if is_remote_url(patterns):
            return [patterns]
        if is_relative_path(patterns):
            glob_iter = list(Path(base_path).rglob(patterns))
        else:
            glob_iter = [Path(filepath) for filepath in glob.glob(patterns)]

        matched_paths = [
            filepath.resolve()
            for filepath in glob_iter
            if filepath.name not in data_files_ignore and not filepath.name.startswith(".") and filepath.is_file()
        ]
        if allowed_extensions is not None:
            out = [
                filepath
                for filepath in matched_paths
                if any(suffix[1:] in allowed_extensions for suffix in filepath.suffixes)
            ]
            if len(out) < len(matched_paths):
                invalid_matched_files = list(set(matched_paths) - set(out))
                logger.info(
                    f"Some files matched the pattern '{patterns}' at {Path(base_path).resolve()} but don't have valid data file extensions: {invalid_matched_files}"
                )
        else:
            out = matched_paths
        if not out:
            error_msg = f"Unable to resolve any data file that matches '{patterns}' at {Path(base_path).resolve()}"
            if allowed_extensions is not None:
                error_msg += f" with any supported extension {list(allowed_extensions)}"
            raise FileNotFoundError(error_msg)
        return out
    elif isinstance(patterns, dict):
        return {
            k: _resolve_data_files_locally_or_by_urls(base_path, v, allowed_extensions=allowed_extensions)
            for k, v in patterns.items()
        }
    else:
        return sum(
            [
                _resolve_data_files_locally_or_by_urls(base_path, pattern, allowed_extensions=allowed_extensions)
                for pattern in patterns
            ],
            [],
        )


def _resolve_data_files_in_dataset_repository(
    dataset_info: huggingface_hub.hf_api.DatasetInfo,
    patterns: Union[str, List[str], Dict],
    allowed_extensions: Optional[list] = None,
) -> Union[List[PurePath], Dict]:
    data_files_ignore = ["README.md", "config.json"]
    if isinstance(patterns, str):
        all_data_files = [
            PurePath("/" + dataset_file.rfilename) for dataset_file in dataset_info.siblings
        ]  # add a / at the beginning to make the pattern **/* match files at the root
        matched_paths = [
            filepath.relative_to("/")
            for filepath in all_data_files
            if filepath.name not in data_files_ignore
            and not filepath.name.startswith(".")
            and filepath.match(patterns)
        ]
        if allowed_extensions is not None:
            out = [
                filepath
                for filepath in matched_paths
                if any(suffix[1:] in allowed_extensions for suffix in filepath.suffixes)
            ]
            if len(out) < len(matched_paths):
                invalid_matched_files = list(set(matched_paths) - set(out))
                logger.info(
                    f"Some files matched the pattern {patterns} in dataset repository {dataset_info.id} but don't have valid data file extensions: {invalid_matched_files}"
                )
        else:
            out = matched_paths
        if not out:
            error_msg = f"Unable to resolve data_file {patterns} in dataset repository {dataset_info.id}"
            if allowed_extensions is not None:
                error_msg += f" with any supported extension {list(allowed_extensions)}"
            raise FileNotFoundError(error_msg)
        return out
    elif isinstance(patterns, dict):
        return {
            k: _resolve_data_files_in_dataset_repository(dataset_info, v, allowed_extensions=allowed_extensions)
            for k, v in patterns.items()
        }
    else:
        return sum(
            [
                _resolve_data_files_in_dataset_repository(dataset_info, pattern, allowed_extensions=allowed_extensions)
                for pattern in patterns
            ],
            [],
        )


def _infer_module_for_data_files(data_files: Union[PurePath, List[PurePath], Dict]) -> Optional[str]:
    extensions_counter = Counter(
        suffix[1:] for filepath in NestedDataStructure(data_files).flatten() for suffix in filepath.suffixes
    )
    if extensions_counter:
        return _EXTENSION_TO_MODULE[extensions_counter.most_common(1)[0][0]]


def prepare_module(
    path: str,
    revision: Optional[Union[str, Version]] = None,
    download_config: Optional[DownloadConfig] = None,
    download_mode: Optional[GenerateMode] = None,
    dataset: bool = True,
    force_local_path: Optional[str] = None,
    dynamic_modules_path: Optional[str] = None,
    return_resolved_file_path: bool = False,
    return_associated_base_path: bool = False,
    data_files: Optional[Union[Dict, List, str]] = None,
    script_version="deprecated",
    **download_kwargs,
) -> Union[Tuple[str, str], Tuple[str, str, Optional[str]]]:
    r"""
        Download/extract/cache a dataset (if dataset==True) or a metric (if dataset==False)

    Dataset and metrics codes are cached inside the the dynamic modules cache to allow easy import (avoid ugly sys.path tweaks)
    and using cloudpickle (among other things).

    Args:

        path (str): Path or name of the dataset, or path to a metric script.
            Depending on ``path``, the module that is returned id either generic moduler (csv, json, text etc.) or a module defined defined a dataset or metric script (a python file).

            For local datasets:

            - if ``path`` is a local directory (but doesn't contain a dataset script)
              -> load a generic module (csv, json, text etc.) based on the content of the directory
              e.g. ``'./path/to/directory/with/my/csv/data'``.
            - if ``path`` is a local dataset or metric script or a directory containing a local dataset or metric script (if the script has the same name as the directory):
              -> load the module from the dataset or metric script
              e.g. ``'./dataset/squad'`` or ``'./dataset/squad/squad.py'``.

            For datasets on the Hugging Face Hub (list all available datasets and ids with ``datasets.list_datasets()``)

            - if ``path`` is a canonical dataset or metric on the HF Hub (ex: `glue`, `squad`)
              -> load the module from the dataset or metric script in the github repository at huggingface/datasets
              e.g. ``'squad'`` or ``'glue'`` or ``accuracy``.
            - if ``path`` is a dataset repository on the HF hub (without a dataset script)
              -> load a generic module (csv, text etc.) based on the content of the repository
              e.g. ``'username/dataset_name'``, a dataset repository on the HF hub containing your data files.
            - if ``path`` is a dataset repository on the HF hub with a dataset script (if the script has the same name as the directory)
              -> load the module from the dataset script in the dataset repository
              e.g. ``'username/dataset_name'``, a dataset repository on the HF hub containing a dataset script `'dataset_name.py'`.

        revision (Optional ``Union[str, datasets.Version]``):
            If specified, the module will be loaded from the datasets repository at this version.
            By default:
            - it is set to the local version of the lib.
            - it will also try to load it from the master branch if it's not available at the local version of the lib.
            Specifying a version that is different from your local version of the lib might cause compatibility issues.
        download_config (:class:`DownloadConfig`, optional): Specific download configuration parameters.
        download_mode (:class:`GenerateMode`, default ``REUSE_DATASET_IF_EXISTS``): Download/generate mode.
        dataset (bool): True if the script to load is a dataset, False if the script is a metric.
        force_local_path (Optional str): Optional path to a local path to download and prepare the script to.
            Used to inspect or modify the script folder.
        dynamic_modules_path (Optional str, defaults to HF_MODULES_CACHE / "datasets_modules", i.e. ~/.cache/huggingface/modules/datasets_modules):
            Optional path to the directory in which the dynamic modules are saved. It must have been initialized with :obj:`init_dynamic_modules`.
            By default the datasets and metrics are stored inside the `datasets_modules` module.
        return_resolved_file_path (Optional bool, defaults to False):
            If True, the url or path to the resolved dataset or metric script is returned with the other ouputs
        return_associated_base_path (Optional bool, defaults to False):
            If True, the base path associated to the dataset is returned with the other ouputs.
            It corresponds to the directory or base url where the dataset script/dataset repo is at.
        data_files (:obj:`Union[Dict, List, str]`, optional): Defining the data_files of the dataset configuration.
        script_version:
            .. deprecated:: 1.13
                'script_version' was renamed to 'revision' in version 1.13 and will be removed in 1.15.
        download_kwargs: optional attributes for DownloadConfig() which will override the attributes in download_config if supplied.

    Returns:
        Tuple[``str``, ``str``]:
        1. The module path being
            - the import path of the dataset/metric package if force_local_path is False: e.g. 'datasets.datasets.squad'
            - the local path to the dataset/metric file if force_local_path is True: e.g. '/User/huggingface/datasets/datasets/squad/squad.py'
        2. A hash string computed from the content of the dataset loading script.
    """
    if script_version != "deprecated":
        warnings.warn(
            "'script_version' was renamed to 'revision' in version 1.13 and will be removed in 1.15.", FutureWarning
        )
        revision = script_version
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
    def prepare_packaged_module(name):
        try:
            head_hf_s3(name, filename=name + ".py", dataset=dataset, max_retries=download_config.max_retries)
        except Exception:
            logger.debug(f"Couldn't head HF s3 for packaged dataset module '{name}'. Running in offline mode.")
        return _PACKAGED_DATASETS_MODULES[name]

    if dataset and path in _PACKAGED_DATASETS_MODULES:
        output = prepare_packaged_module(path)
        if return_resolved_file_path:
            output += (None,)
        if return_associated_base_path:
            output += (None,)
        return output

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

    # We have several ways to find the processing file:
    # - if os.path.join(path, name) is a local python file
    #   -> use the module from the python file
    # - if path is a local directory (but no python file)
    #   -> use a packaged module (csv, text etc.) based on content of the directory
    # - if path has no "/" and is a module on github (in /datasets or in /metrics)
    #   -> use the module from the python file on github
    # - if path has one "/" and is dataset repository on the HF hub with a python file
    #   -> the module from the python file in the dataset repository
    # - if path has one "/" and is dataset repository on the HF hub without a python file
    #   -> use a packaged module (csv, text etc.) based on content of the repository
    resource_type = "dataset" if dataset else "metric"
    combined_path = os.path.join(path, name)
    if path.endswith(name):
        if os.path.isfile(path):
            file_path = path
            local_path = path
            base_path = os.path.dirname(path)
        else:
            raise FileNotFoundError(f"Couldn't find a {resource_type} script at {relative_to_absolute_path(path)}")
    elif os.path.isfile(combined_path):
        file_path = combined_path
        local_path = combined_path
        base_path = path
    elif os.path.isfile(path):
        file_path = path
        local_path = path
        base_path = os.path.dirname(path)
    elif os.path.isdir(path):
        resolved_data_files = _resolve_data_files_locally_or_by_urls(
            path, data_files or "*", allowed_extensions=_EXTENSION_TO_MODULE.keys()
        )
        infered_module_name = _infer_module_for_data_files(resolved_data_files)
        if not infered_module_name:
            raise FileNotFoundError(f"No data files or {resource_type} script found in local directory {path}")
        output = prepare_packaged_module(infered_module_name)
        if return_resolved_file_path:
            output += (None,)
        if return_associated_base_path:
            output += (path,)
        return output
    else:
        # Try github (canonical datasets/metrics) and then HF Hub (community datasets)
        combined_path_abs = relative_to_absolute_path(combined_path)
        expected_dir_for_combined_path_abs = os.path.dirname(combined_path_abs)
        try:
            try:
                head_hf_s3(path, filename=name, dataset=dataset, max_retries=download_config.max_retries)
            except Exception:
                pass
            revision = str(revision) if revision is not None else None
            if path.count("/") == 0:  # canonical datasets/metrics: github path
                file_path = hf_github_url(path=path, name=name, dataset=dataset, revision=revision)
                try:
                    local_path = cached_path(file_path, download_config=download_config)
                except FileNotFoundError:
                    if revision is not None:
                        raise FileNotFoundError(
                            f"Couldn't find a directory or a {resource_type} named '{path}' using version {revision}. "
                            f"It doesn't exist locally at {expected_dir_for_combined_path_abs} or remotely at {file_path}"
                        ) from None
                    else:
                        github_file_path = file_path
                        file_path = hf_github_url(path=path, name=name, dataset=dataset, revision="master")
                        try:
                            local_path = cached_path(file_path, download_config=download_config)
                            logger.warning(
                                f"Couldn't find a directory or a {resource_type} named '{path}'. "
                                f"It was picked from the master branch on github instead at {file_path}"
                            )
                        except FileNotFoundError:
                            raise FileNotFoundError(
                                f"Couldn't find a directory or a {resource_type} named '{path}'. "
                                f"It doesn't exist locally at {expected_dir_for_combined_path_abs} or remotely at {github_file_path}"
                            ) from None
            elif path.count("/") == 1:  # users datasets/metrics: s3 path (hub for datasets and s3 for metrics)
                file_path = hf_hub_url(path=path, name=name, revision=revision)
                if not dataset:
                    # We don't have community metrics on the HF Hub
                    raise FileNotFoundError(
                        f"Couldn't find a {resource_type} in a directory at '{path}'. "
                        f"It doesn't exist locally at {combined_path_abs}"
                    )
                try:
                    local_path = cached_path(file_path, download_config=download_config)
                except FileNotFoundError:
                    hf_api = HfApi(config.HF_ENDPOINT)
                    try:
                        dataset_info = hf_api.dataset_info(
                            repo_id=path, revision=revision, token=download_config.use_auth_token
                        )
                    except Exception as exc:
                        raise FileNotFoundError(
                            f"Couldn't find a directory or a {resource_type} named '{path}'. "
                            f"It doesn't exist locally at {expected_dir_for_combined_path_abs} or remotely on {hf_api.endpoint}/datasets"
                        ) from exc
                    resolved_data_files = _resolve_data_files_in_dataset_repository(
                        dataset_info,
                        data_files if data_files is not None else "*",
                        allowed_extensions=_EXTENSION_TO_MODULE.keys(),
                    )
                    infered_module_name = _infer_module_for_data_files(resolved_data_files)
                    if not infered_module_name:
                        raise FileNotFoundError(
                            f"No data files found in dataset repository '{path}'. Local directory at {expected_dir_for_combined_path_abs} doesn't exist either."
                        ) from None
                    output = prepare_packaged_module(infered_module_name)
                    if return_resolved_file_path:
                        output += (None,)
                    if return_associated_base_path:
                        output += (url_or_path_parent(file_path),)
                    return output
            else:
                raise FileNotFoundError(
                    f"Couldn't find a {resource_type} directory at '{path}'. "
                    f"It doesn't exist locally at {expected_dir_for_combined_path_abs}"
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
                        f"couldn't be found locally at {combined_path_abs}, or remotely ({type(e).__name__})."
                    )
                    output = (module_path, hash)
                    if return_resolved_file_path:
                        with open(os.path.join(main_folder_path, hash, short_name + ".json")) as cache_metadata:
                            file_path = json.load(cache_metadata)["original file path"]
                        output += (file_path,)
                    if return_associated_base_path:
                        output += (url_or_path_parent(file_path),)
                    return output
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

    output = (module_path, hash)
    if return_resolved_file_path:
        output += (file_path,)
    if return_associated_base_path:
        output += (base_path,)
    return output


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
    module_path, _ = prepare_module(
        path,
        revision=revision,
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
    # Download/copy dataset processing script
    module_path, hash, base_path = prepare_module(
        path,
        revision=revision,
        download_config=download_config,
        download_mode=download_mode,
        dataset=True,
        return_associated_base_path=True,
        use_auth_token=use_auth_token,
        data_files=data_files,
    )

    # Get dataset builder class from the processing script
    builder_cls = import_main_class(module_path, dataset=True)

    # For packaged builder used to load data from a dataset repository or dataset directory (no dataset script)
    if module_path.startswith("datasets.") and path not in _PACKAGED_DATASETS_MODULES:
        # Add a nice name to the configuratiom
        if name is None:
            name = path.split("/")[-1].split(os.sep)[-1]
        # Resolve the data files
        allowed_extensions = [
            extension
            for extension in _EXTENSION_TO_MODULE
            if _EXTENSION_TO_MODULE[extension] == camelcase_to_snakecase(builder_cls.__name__)
        ]
        data_files = data_files if data_files is not None else "*"
        if base_path.startswith(config.HF_ENDPOINT):
            dataset_info = HfApi(config.HF_ENDPOINT).dataset_info(path, revision=revision, token=use_auth_token)
            data_files = _resolve_data_files_in_dataset_repository(
                dataset_info, data_files, allowed_extensions=allowed_extensions
            )
        else:  # local dir
            data_files = _resolve_data_files_locally_or_by_urls(
                path, data_files, allowed_extensions=allowed_extensions
            )
    elif path in _PACKAGED_DATASETS_MODULES:
        if data_files is None:
            error_msg = f"Please specify the data files to load for the {path} dataset builder."
            example_extensions = [
                extension for extension in _EXTENSION_TO_MODULE if _EXTENSION_TO_MODULE[extension] == path
            ]
            if example_extensions:
                error_msg += f'\nFor example `data_files={{"train": "path/to/data/train/*.{example_extensions[0]}"}}`'
            raise ValueError(error_msg)
        data_files = _resolve_data_files_locally_or_by_urls(".", data_files)

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
