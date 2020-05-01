# coding=utf-8
# Copyright 2020 The HuggingFace NLP Authors and the TensorFlow DATASETS Authors.
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
"""Access METRICS."""

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


from nlp.utils.file_utils import HF_DATASETS_CACHE, cached_path, hf_bucket_url, is_remote_url


logger = logging.getLogger(__name__)



CURRENT_FILE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
METRICS_PATH = CURRENT_FILE_DIRECTORY 
METRICS_MODULE = "nlp.metrics"



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
    """ Find whether we should import or clone additional files for a given  script.
        And list the import.

        We allow:
        - local dependencies and
        - external dependencies whose url is specified with a comment starting from "# From:' followed by an url to a file, an archive or a github repository.
            external dependencies will be downloaded (and extracted if needed in the metric folder).
            We also add an `__init__.py` to each sub-folder of a downloaded folder so the user can import from them in the script.

        Note that only direct import in the metric  script will be handled
        We don't recursively explore the additional import to download further files.

        ```python
        import .c4_utils
        import .clicr.metric-code.build_json_dataset  # From: https://github.com/clips/clicr/{branch_name}
        ```
    """
    lines = []
    with open(file_path, mode="r") as f:
        lines.extend(f.readlines())

    logger.info("Checking %s for additional imports.", file_path)
    imports = []
    external_imports = []
    for line in lines:
        match = re.match(r"(?:from|import)\s+\.([^\s\.]+)[^#\r\n]*(?:#\s+From:\s+)?([^\r\n]*)", line)
        if match is None:
            continue
        if match.group(2):
            url_path = match.group(2)
            if _is_github_url(url_path):
                # Parse github url to point to zip
                repo_owner, repo_name, branch = url_path.split("/")[-3:]
                url_path_zip = "https://github.com/{}/{}/archive/{}.zip".format(repo_owner, repo_name, branch)
            imports.append(("external", url_path_zip))
            filename = line.split('#')[0].strip().split('.')[-2:]
            filename = os.path.join(filename[0], filename[1])
            external_imports.append((filename,url_path))
        elif match.group(1):
            imports.append(("internal", match.group(1)))

    return imports, external_imports


def load_metric_module(
    path: str,
    name: Optional[str] = None,
    force_reload: bool = False,
    resume_download: bool = False,
    proxies: Optional[Dict] = None,
    local_files_only: bool = False,
    data_dir: Optional[str] = None,
    **kwargs,
):
    r"""
        Download/extract/cache a metric to add to the lib from a path or url which can be:
            - a path to a local directory containing the metric  python script
            - an url to a S3 directory with a metric  python script

        metric codes are cached inside the lib to allow easy import (avoid ugly sys.path tweaks)
        and using cloudpickle (among other things).

        Return: tuple of
            the unique id associated to the metric
            the local path to the metric
    """
    global METRICS_PATH
    remote_files = []
    
    if name is None:
        name = list(filter(lambda x: x, path.split("/")))[-1] + ".py"

    if not name.endswith(".py") or "/" in name:
        raise ValueError("The provided name should be the filename of a python script (ends with '.py')")

    # We have three ways to find the metric  file:
    # - if os.path.join(path, name) is a file or a remote url
    # - if path is a file or a remote url
    # - otherwise we assume path/name is a path to our S3 bucket
    combined_path = os.path.join(path, name)
    if os.path.isfile(combined_path) or is_remote_url(combined_path):
        metric_file = combined_path
    elif os.path.isfile(path) or is_remote_url(path):
        metric_file = path
    else:
        metric_file = hf_bucket_url(path, filename=name)

    metric_base_path = os.path.dirname(metric_file)  # remove the filename
    # Load the module in two steps:
    # 1. get the metric  file on the local filesystem if it's not there (download to cache dir)
    # 2. copy from the local file system inside the library to import it
    local_path = cached_path(
        metric_file,
        cache_dir=data_dir,
        force_download=force_reload,
        extract_compressed_file=True,
        force_extract=force_reload,
        local_files_only=local_files_only,
    )

    # Download external imports if needed
    imports, external_imports = get_imports(local_path)
    local_imports = []
    for import_type, import_name_or_path in imports:
        if import_type == "internal":
            url_or_filename = metric_base_path + "/" + import_name_or_path + ".py"
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

    # Define a directory with a unique name in our metric folder
    # path is: ./METRICS/metric_name/hash_from_code/script.py
    metric_name = name[:-3]  # Removing the '.py' at the end
    metric_hash = files_to_hash([local_path] + local_imports)
    metric_main_folder_path = os.path.join(METRICS_PATH, metric_name)
    metric_hash_folder_path = os.path.join(metric_main_folder_path, metric_hash)
    metric_file_path = os.path.join(metric_hash_folder_path, name)
    # Prevent parallel disk operations
    lock_path = local_path + ".lock"
    with FileLock(lock_path):
        # Create main metric folder if needed
        if not os.path.exists(metric_main_folder_path):
            logger.info("Creating main folder for metric %s at %s", metric_file, metric_main_folder_path)
            os.makedirs(metric_main_folder_path, exist_ok=True)
        else:
            logger.info("Found main folder for metric %s at %s", metric_file, metric_main_folder_path)

        # add an __init__ file to the main metric folder if needed
        init_file_path = os.path.join(metric_main_folder_path, "__init__.py")
        if not os.path.exists(init_file_path):
            with open(init_file_path, "w"):
                pass

        # Create hash metric folder if needed
        if not os.path.exists(metric_hash_folder_path):
            logger.info(
                "Creating specific version folder for metric %s at %s", metric_file, metric_hash_folder_path
            )
            os.makedirs(metric_hash_folder_path)
        else:
            logger.info("Found specific version folder for metric %s at %s", metric_file, metric_hash_folder_path)
        ## get external import files and copy them
        metric_folder = os.path.join(METRICS_PATH, name.split('_')[0])  ## rouge_imports ==> rouge folder, bleu_imports ==> bleu folder
        if not os.path.exists(metric_folder):
            os.system('mkdir '+ metric_folder)
        for external_import in external_imports:
            filename, url = external_import
            external_import = url.split('/')
            file_path = os.path.join(local_import_path, external_import[-2]+'-'+external_import[-1], external_import[-2], filename+'.py')
            
            filename = filename.split('/')[-1]+'.py'
            ## copy the file in the local directory
            if not os.path.exists(os.path.join(metric_folder, filename)):
                shutil.copyfile(file_path, os.path.join(metric_folder, filename))
        shutil.rmtree(metric_main_folder_path)  ## remove the downloaded folder after copying the needed files
            
        #create an __init__.py file in the import folder
        init_file_path = os.path.join(metric_folder, "__init__.py")
        if not os.path.exists(init_file_path):
            with open(init_file_path, "w"):
                pass



