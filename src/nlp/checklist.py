# coding=utf-8
# Copyright 2020 The HuggingFace NLP Authors and the TensorFlow Datasets Authors.
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
"""CheckList helper class"""

import logging
import os

import numpy as np

from .arrow_dataset import Dataset
from .load import import_main_class, load_dataset, prepare_module
from .utils.download_manager import DownloadManager
from .utils.file_utils import DownloadConfig


logger = logging.getLogger(__name__)

try:
    from checklist.test_suite import TestSuite
except ImportError:
    logger.error(
        "ImportError: To be able to use this module, you need to install the following dependencies ['checklist'] using 'pip install checklist' for instance."
    )


def aggr_testcases(dataset):
    """Aggregates all test cases of a specific test in a dataset

    Args:
        dataset(``nlp.dataset``)

    Returns:
        nlp.dataset, where each row is a test, with test cases under key 'data'
    """
    nd = {"data": [], "test_name": [], "test_case": []}
    case_index = {}
    for e in dataset:
        key = (e["test_name"], e["test_case"])
        if key not in case_index:
            i = len(nd["data"])
            nd["data"].append([])
            nd["test_name"].append(e["test_name"])
            nd["test_case"].append(e["test_case"])
            case_index[key] = i
        i = case_index[key]
        cl_keys = set(["test_case", "test_name", "example_idx"])
        d = {x: v for x, v in e.items() if x not in cl_keys}
        nd["data"][i].append(d)
    return Dataset.from_dict(nd)


class CheckListSuite(object):
    """Interface between marcotcr/checklist and nlp/checklist"""

    def __init__(self, path: str, **load_dataset_kwargs):
        """Constructs a CheckListSuite.

        Users can use the CheckList functionality from marcotcr/checklist by using this object's .suite

        Args:
            path (``str``):
                path to the dataset processing script with the dataset builder. Can be either:
                    - a local path to processing script or the directory containing the script (if the script has the same name as the directory),
                        e.g. ``'./dataset/sentiment_checklist'`` or ``'./dataset/sentiment_checklist/sentiment_checklist.py'``
                    - a CheckList dataset identifier on HuggingFace AWS bucket (list all available datasets and ids with ``nlp.list_datasets()``)
                        e.g. ``'sentiment_checklist'``, ``'qqp_checklist'`` or ``'squad_checklist'``
        """
        self.dataset = load_dataset(path, **load_dataset_kwargs)["test"]
        download_config = load_dataset_kwargs.get("download_config")
        module_path, hash = prepare_module(path, download_config=download_config, dataset=True)
        builder_cls = import_main_class(module_path, dataset=True)
        builder_instance = builder_cls(
            hash=hash,
            **load_dataset_kwargs,
        )
        if download_config is None:
            download_config = DownloadConfig()
            download_config.cache_dir = os.path.join(builder_instance._cache_dir_root, "downloads")
        dl_manager = DownloadManager(
            dataset_name=builder_instance.name,
            download_config=download_config,
            data_dir=builder_instance.config.data_dir,
        )
        suite_file = os.path.join(
            dl_manager.download_and_extract(builder_instance.config.url), builder_instance.config.suite_name
        )
        self.suite = TestSuite.from_file(suite_file)
        self.fail_rate = {}

    def get_test(
        self,
        test_name: str,
        aggregate_testcases: bool = False,
    ) -> "Dataset":
        """Returns a dataset corresponding to one specific test

        Args:
            test_name (``str``):
                test name
            aggregate_testcases (``bool``):
                If True, will return a dataset with a single row, where test cases are aggregated
        Returns:
            ``nlp.Dataset``
        """
        d = self.dataset.filter(lambda x: x["test_name"] == test_name)
        if aggregate_testcases:
            d = aggr_testcases(d)
        return d

    def compute(
        self,
        prediction_key: str,
        confidence_key: str = None,
    ):
        """Runs the tests in the checklist for a specific set of predictions and confidences

        Failure rates are stored in self.fail_rate, and results for individual test examples are stored in self.dataset.

        Args:
            prediction_key (``str``):
                Key where predictions for each test example are stored in self.dataset
            confidence_key (``str``):
                Key where confidence scores for each test example are stored in self.dataset.
                Whether these confidences are required and what their format should be is detailed in
                self.dataset.info.
        """
        preds = self.dataset[prediction_key]
        confs = self.dataset[confidence_key] if confidence_key is not None else np.ones(len(preds))
        if type(confs[0]) == list:
            confs = [np.array(x) for x in confs]
        self.suite.run_from_preds_confs(preds, confs, overwrite=True)

        def update_fails(e):
            test_name = e["test_name"]
            if self.suite.tests[test_name].run_idxs is None:
                test_case = e["test_case"]
            else:
                test_case = np.where(self.suite.tests[test_name].run_idxs == e["test_case"])[0][0]
            d = self.suite.tests[test_name].results.expect_results[test_case]
            if d is None or d[e["example_idx"]] is None:
                fail = -1
            else:
                fail = d[e["example_idx"]] <= 0
            if "fail" not in e:
                e["fail"] = {}
            e["fail"][prediction_key] = int(fail)
            return e

        self.dataset = self.dataset.map(update_fails)
        self.fail_rate[prediction_key] = {}
        for t in self.suite.tests:
            try:
                self.fail_rate[prediction_key][t] = self.suite.tests[t].get_stats().fail_rate
            except (KeyError, AttributeError):
                self.fail_rate[prediction_key][t] = -1
