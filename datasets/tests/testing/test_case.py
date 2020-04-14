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
"""Base TestCase to use test_data."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import contextlib
import os
import tempfile

from absl import logging
from absl.testing import absltest
import six
import tensorflow.compat.v2 as tf
from tensorflow_datasets.core.utils import gcs_utils



GCS_ACCESS_FNS = {
    "original_info": gcs_utils.gcs_dataset_info_files,
    "dummy_info": lambda _: [],
    "original_datasets": gcs_utils.is_dataset_on_gcs,
    "dummy_datasets": lambda _: False,
}


class TestCase(tf.test.TestCase):
  """Base TestCase to be used for all tests.

  `test_data` class attribute: path to the directory with test data.
  `tmp_dir` attribute: path to temp directory reset before every test.
  """

  @classmethod
  def setUpClass(cls):
    super(TestCase, cls).setUpClass()
    cls.test_data = os.path.join(os.path.dirname(__file__), "test_data")
    # Test must not communicate with GCS.
    gcs_utils.gcs_dataset_info_files = GCS_ACCESS_FNS["dummy_info"]
    gcs_utils.is_dataset_on_gcs = GCS_ACCESS_FNS["dummy_datasets"]

  @contextlib.contextmanager
  def gcs_access(self):
    # Restore GCS access
    gcs_utils.gcs_dataset_info_files = GCS_ACCESS_FNS["original_info"]
    gcs_utils.is_dataset_on_gcs = GCS_ACCESS_FNS["original_datasets"]
    yield
    # Revert access
    gcs_utils.gcs_dataset_info_files = GCS_ACCESS_FNS["dummy_info"]
    gcs_utils.is_dataset_on_gcs = GCS_ACCESS_FNS["dummy_datasets"]

  def setUp(self):
    super(TestCase, self).setUp()
    # get_temp_dir is actually the same for all tests, so create a temp sub-dir.
    self.tmp_dir = tempfile.mkdtemp(dir=tf.compat.v1.test.get_temp_dir())

  def assertRaisesWithPredicateMatch(self, err_type, predicate):
    if isinstance(predicate, six.string_types):
      predicate_fct = lambda err: predicate in str(err)
    else:
      predicate_fct = predicate
    return super(TestCase, self).assertRaisesWithPredicateMatch(
        err_type, predicate_fct)

  @contextlib.contextmanager
  def assertLogs(self, text, level="info"):
    with absltest.mock.patch.object(logging, level) as mock_log:
      yield
      concat_logs = ""
      for log_call in mock_log.call_args_list:
        args = log_call[0]
        base, args = args[0], args[1:]
        log_text = base % tuple(args)
        concat_logs += " " + log_text
      self.assertIn(text, concat_logs)
