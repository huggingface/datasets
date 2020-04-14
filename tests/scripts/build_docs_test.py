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
"""Smoke Test for docs generation."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil
import tempfile

from absl.testing import absltest

from tensorflow_datasets.scripts import build_docs
from tensorflow_datasets.scripts import document_datasets


class BuildDocsTest(absltest.TestCase):

  def setUp(self):
    super(BuildDocsTest, self).setUp()
    self.workdir = tempfile.mkdtemp()
    if os.path.exists(self.workdir):
      shutil.rmtree(self.workdir)
    os.makedirs(self.workdir)

  def test_api_gen(self):
    build_docs.build_api_docs(
        output_dir=self.workdir,
        code_url_prefix="",
        search_hints=True,
        site_path="datasets/api_docs/python")

    # Check that the "defined in" section is working
    with open(os.path.join(self.workdir, "tfds.md")) as f:
      content = f.read()
    self.assertIn("__init__.py", content)

  def test_document_datasets(self):
    document_datasets.dataset_docs_str(datasets=["mnist", "cifar10"])


if __name__ == "__main__":
  absltest.main()
