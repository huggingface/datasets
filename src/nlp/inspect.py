# coding=utf-8
# Copyright 2020 The HuggingFace NLP Authors.
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
""" List and inspect datasets and metrics."""

import logging

from .hf_api import HfApi
from .load import prepare_module


logger = logging.getLogger(__name__)


def list_datasets():
    api = HfApi()
    return api.dataset_list()


def list_metrics():
    api = HfApi()
    return api.metric_list()


def inspect_dataset(path, local_path, download_config=None, **download_kwargs):
    module_path = prepare_module(
        path, download_config=download_config, dataset=True, force_local_path=local_path, **download_kwargs
    )
    print(
        f"The processing script for dataset {path} can be inspected at {local_path}. "
        f"The main class is in {module_path}. "
        f"You can modify this processing script and use it with `nlp.load_dataset({local_path})`."
    )


def inspect_metric(path, local_path, download_config=None, **download_kwargs):
    module_path = prepare_module(
        path, download_config=download_config, dataset=False, force_local_path=local_path, **download_kwargs
    )
    print(
        f"The processing scripts for metric {path} can be inspected at {local_path}. "
        f"The main class is in {module_path}. "
        f"You can modify this processing scripts and use it with `nlp.load_metric({local_path})`."
    )
