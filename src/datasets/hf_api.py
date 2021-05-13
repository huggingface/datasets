# coding=utf-8
# Copyright 2019-present, the HuggingFace Inc. team.
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


from typing import Dict, List, Optional, Union

import requests

from .utils.logging import get_logger


logger = get_logger(__name__)

ENDPOINT = "https://huggingface.co"


class ObjectInfo:
    """
    Info about a public dataset or Metric accessible from our S3.
    """

    def __init__(
        self,
        id: str,
        key: str,
        lastModified: Optional[str] = None,
        description: Optional[str] = None,
        citation: Optional[str] = None,
        size: Optional[int] = None,
        etag: Optional[str] = None,
        siblings: List[Dict] = None,
        author: str = None,
        **kwargs,
    ):
        self.id = id  # id of dataset
        self.key = key  # S3 object key of config.json
        self.lastModified = lastModified
        self.description = description
        self.citation = citation
        self.size = size
        self.etag = etag
        self.siblings = siblings  # list of files that constitute the dataset
        self.author = author
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        single_line_description = self.description.replace("\n", "") if self.description is not None else ""
        return f"datasets.ObjectInfo(\n\tid='{self.id}',\n\tdescription='{single_line_description}',\n\tfiles={self.siblings}\n)"


class HfApi:
    ALLOWED_FILE_TYPES = ["datasets", "metrics"]

    def __init__(self, endpoint=None):
        """Create Api using a specific endpoint and also the file types ('datasets' or 'metrics')"""
        self.endpoint = endpoint if endpoint is not None else ENDPOINT

    def dataset_list(self, with_community_datasets=True, id_only=False) -> Union[List[ObjectInfo], List[str]]:
        """
        Get the public list of all the datasets on huggingface, including the community datasets
        """
        path = "{}/api/datasets".format(self.endpoint)
        r = requests.get(path)
        r.raise_for_status()
        d = r.json()
        datasets = [ObjectInfo(**x) for x in d]
        if not with_community_datasets:
            datasets = [d for d in datasets if "/" not in d.id]
        if id_only:
            datasets = [d.id for d in datasets]
        return datasets

    def metric_list(self, with_community_metrics=True, id_only=False) -> Union[List[ObjectInfo], List[str]]:
        """
        Get the public list of all the metrics on huggingface, including the community metrics
        """
        path = "{}/api/metrics".format(self.endpoint)
        r = requests.get(path)
        r.raise_for_status()
        d = r.json()
        metrics = [ObjectInfo(**x) for x in d]
        if not with_community_metrics:
            metrics = [m for m in metrics if "/" not in m.id]
        if id_only:
            metrics = [m.id for m in metrics]
        return metrics
