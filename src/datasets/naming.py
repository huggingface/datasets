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
"""Utilities for file names."""
import glob
import itertools
import os
import re


_uppercase_uppercase_re = re.compile(r"([A-Z]+)([A-Z][a-z])")
_lowercase_uppercase_re = re.compile(r"([a-z\d])([A-Z])")

_single_underscore_re = re.compile(r"(?<!_)_(?!_)")
_multiple_underscores_re = re.compile(r"(_{2,})")

_split_re = r"^\w+(\.\w+)*$"

INVALID_WINDOWS_CHARACTERS_IN_PATH = r"<>:/\|?*"


def camelcase_to_snakecase(name):
    """Convert camel-case string to snake-case."""
    name = _uppercase_uppercase_re.sub(r"\1_\2", name)
    name = _lowercase_uppercase_re.sub(r"\1_\2", name)
    return name.lower()


def snakecase_to_camelcase(name):
    """Convert snake-case string to camel-case string."""
    name = _single_underscore_re.split(name)
    name = [_multiple_underscores_re.split(n) for n in name]
    return "".join(n.capitalize() for n in itertools.chain.from_iterable(name) if n != "")


def filename_prefix_for_name(name):
    if os.path.basename(name) != name:
        raise ValueError(f"Should be a dataset name, not a path: {name}")
    return camelcase_to_snakecase(name)


def filename_prefix_for_split(name, split):
    if os.path.basename(name) != name:
        raise ValueError(f"Should be a dataset name, not a path: {name}")
    if not re.match(_split_re, split):
        raise ValueError(f"Split name should match '{_split_re}'' but got '{split}'.")
    return f"{filename_prefix_for_name(name)}-{split}"


def filepattern_for_dataset_split(dataset_name, split, data_dir, filetype_suffix=None):
    prefix = filename_prefix_for_split(dataset_name, split)
    if filetype_suffix:
        prefix += f".{filetype_suffix}"
    filepath = os.path.join(data_dir, prefix)
    return f"{filepath}*"


def filename_for_dataset_split(dataset_name, split, filetype_suffix=None):
    prefix = filename_prefix_for_split(dataset_name, split)
    if filetype_suffix:
        prefix += f".{filetype_suffix}"
    return prefix


def filenames_for_dataset_split(path, dataset_name, split, filetype_suffix=None):

    NUM_DIGITS = 5
    counting_pattern = "[0-9]" * NUM_DIGITS

    prefix = filename_prefix_for_split(dataset_name, split)
    prefix = os.path.join(path, prefix)
    filetype_suffix = filetype_suffix if filetype_suffix is not None else ""

    single_file_path = f"{prefix}.{filetype_suffix}"
    if os.path.isfile(single_file_path):
        return [single_file_path]

    return sorted(glob.glob(f"{prefix}-{counting_pattern}-of-{counting_pattern}.{filetype_suffix}"))


def filepath_for_dataset_split(dataset_name, split, data_dir, filetype_suffix=None):
    filename = filename_for_dataset_split(
        dataset_name=dataset_name,
        split=split,
        filetype_suffix=filetype_suffix,
    )
    filepath = os.path.join(data_dir, filename)
    return filepath
