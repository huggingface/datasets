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
from typing import Optional

from .hf_api import HfApi
from .load import prepare_module
from .utils import DownloadConfig


logger = logging.getLogger(__name__)


def list_datasets(with_community_datasets=True):
    """ List all the datasets scripts available on HuggingFace AWS bucket """
    api = HfApi()
    return api.dataset_list(with_community_datasets=with_community_datasets)


def list_metrics(with_community_metrics=True):
    """ List all the metrics script available on HuggingFace AWS bucket """
    api = HfApi()
    return api.metric_list(with_community_metrics=with_community_metrics)


def inspect_dataset(path: str, local_path: str, download_config: Optional[DownloadConfig] = None, **download_kwargs):
    r"""
        Allow inspection/modification of a dataset script by copying on local drive at local_path.

        Args:
            path (``str``): path to the dataset processing script with the dataset builder. Can be either:
                - a local path to processing script or the directory containing the script (if the script has the same name as the directory),
                    e.g. ``'./dataset/squad'`` or ``'./dataset/squad/squad.py'``
                - a datatset identifier on HuggingFace AWS bucket (list all available datasets and ids with ``nlp.list_datasets()``)
                    e.g. ``'squad'``, ``'glue'`` or ``'openai/webtext'``
            local_path (``str``): path to the local folder to copy the datset script to.
            download_config (Optional ``nlp.DownloadConfig``: specific download configuration parameters.
            **download_kwargs: optional attributes for DownloadConfig() which will override the attributes in download_config if supplied.
    """
    module_path, _ = prepare_module(
        path, download_config=download_config, dataset=True, force_local_path=local_path, **download_kwargs
    )
    print(
        f"The processing script for dataset {path} can be inspected at {local_path}. "
        f"The main class is in {module_path}. "
        f"You can modify this processing script and use it with `nlp.load_dataset({local_path})`."
    )


def inspect_metric(path: str, local_path: str, download_config: Optional[DownloadConfig] = None, **download_kwargs):
    r"""
        Allow inspection/modification of a metric script by copying it on local drive at local_path.

        Args:
            path (``str``): path to the dataset processing script with the dataset builder. Can be either:
                - a local path to processing script or the directory containing the script (if the script has the same name as the directory),
                    e.g. ``'./dataset/squad'`` or ``'./dataset/squad/squad.py'``
                - a datatset identifier on HuggingFace AWS bucket (list all available datasets and ids with ``nlp.list_datasets()``)
                    e.g. ``'squad'``, ``'glue'`` or ``'openai/webtext'``
            local_path (``str``): path to the local folder to copy the datset script to.
            download_config (Optional ``nlp.DownloadConfig``: specific download configuration parameters.
            **download_kwargs: optional attributes for DownloadConfig() which will override the attributes in download_config if supplied.
    """
    module_path, _ = prepare_module(
        path, download_config=download_config, dataset=False, force_local_path=local_path, **download_kwargs
    )
    print(
        f"The processing scripts for metric {path} can be inspected at {local_path}. "
        f"The main class is in {module_path}. "
        f"You can modify this processing scripts and use it with `nlp.load_metric({local_path})`."
    )
