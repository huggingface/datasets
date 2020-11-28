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
"""Utilities for file names."""

import os
import re


_first_cap_re = re.compile("(.)([A-Z][a-z0-9]+)")
_all_cap_re = re.compile("([a-z0-9])([A-Z])")

_split_re = r"^\w+$"


def camelcase_to_snakecase(name):
    """Convert camel-case string to snake-case."""
    s1 = _first_cap_re.sub(r"\1_\2", name)
    return _all_cap_re.sub(r"\1_\2", s1).lower()


def snake_to_camelcase(name):
    """Convert snake-case string to camel-case string."""
    return "".join(n.capitalize() for n in name.split("_"))


def filename_prefix_for_name(name):
    if os.path.basename(name) != name:
        raise ValueError("Should be a dataset name, not a path: %s" % name)
    return camelcase_to_snakecase(name)


def filename_prefix_for_split(name, split):
    if os.path.basename(name) != name:
        raise ValueError("Should be a dataset name, not a path: %s" % name)
    if not re.match(_split_re, split):
        raise ValueError(f"Split name should match '{_split_re}'' but got '{split}'.")
    return "%s-%s" % (filename_prefix_for_name(name), split)


def filepattern_for_dataset_split(dataset_name, split, data_dir, filetype_suffix=None):
    prefix = filename_prefix_for_split(dataset_name, split)
    if filetype_suffix:
        prefix += ".%s" % filetype_suffix
    filepath = os.path.join(data_dir, prefix)
    return "%s*" % filepath


def filename_for_dataset_split(dataset_name, split, filetype_suffix=None):
    prefix = filename_prefix_for_split(dataset_name, split)
    if filetype_suffix:
        prefix += ".%s" % filetype_suffix
    return prefix


def filepath_for_dataset_split(dataset_name, split, data_dir, filetype_suffix=None):
    filename = filename_for_dataset_split(
        dataset_name=dataset_name,
        split=split,
        filetype_suffix=filetype_suffix,
    )
    filepath = os.path.join(data_dir, filename)
    return filepath
