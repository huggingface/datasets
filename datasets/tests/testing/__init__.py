# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors.
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
"""Testing utilities."""

from tensorflow_datasets.testing.dataset_builder_testing import DatasetBuilderTestCase
from tensorflow_datasets.testing.mocking import mock_data
from tensorflow_datasets.testing.test_case import TestCase
from tensorflow_datasets.testing.test_utils import DummyDatasetSharedGenerator
from tensorflow_datasets.testing.test_utils import DummyMnist
from tensorflow_datasets.testing.test_utils import DummyParser
from tensorflow_datasets.testing.test_utils import DummySerializer
from tensorflow_datasets.testing.test_utils import fake_examples_dir
from tensorflow_datasets.testing.test_utils import FeatureExpectationItem
from tensorflow_datasets.testing.test_utils import FeatureExpectationsTestCase
from tensorflow_datasets.testing.test_utils import make_tmp_dir
from tensorflow_datasets.testing.test_utils import mock_kaggle_api
from tensorflow_datasets.testing.test_utils import RaggedConstant
from tensorflow_datasets.testing.test_utils import rm_tmp_dir
from tensorflow_datasets.testing.test_utils import run_in_graph_and_eager_modes
from tensorflow_datasets.testing.test_utils import SubTestCase
from tensorflow_datasets.testing.test_utils import test_main
from tensorflow_datasets.testing.test_utils import tmp_dir

__all__ = [
    "DatasetBuilderTestCase",
    "DummyDatasetSharedGenerator",
    "DummyMnist",
    "fake_examples_dir",
    "FeatureExpectationItem",
    "FeatureExpectationsTestCase",
    "SubTestCase",
    "TestCase",
    "RaggedConstant",
    "run_in_graph_and_eager_modes",
    "test_main",
    "tmp_dir",  # TODO(afrozm): rm from here and add as methods to TestCase
    "make_tmp_dir",  # TODO(afrozm): rm from here and add as methods to TestCase
    "mock_kaggle_api",
    "mock_data",
    "rm_tmp_dir",  # TODO(afrozm): rm from here and add as methods to TestCase
]
