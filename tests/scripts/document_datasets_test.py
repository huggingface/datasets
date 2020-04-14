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
"""Test of `document_datasets.py`."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow_datasets import testing
from tensorflow_datasets.core import builder
from tensorflow_datasets.core import utils
from tensorflow_datasets.scripts import document_datasets

DummyMnist = testing.DummyMnist


class DummyMnistConfigs(DummyMnist):
  """Builder with config and manual instructions."""
  MANUAL_DOWNLOAD_INSTRUCTIONS = """Some manual instructions."""
  BUILDER_CONFIGS = [
      builder.BuilderConfig(
          name="config_name",
          version=utils.Version("0.0.1"),
          description="Config description.",
      ),
  ]


class DocumentDatasetsTest(testing.TestCase):

  @classmethod
  def setUpClass(cls):
    super(DocumentDatasetsTest, cls).setUpClass()
    cls._tfds_tmp_dir = testing.make_tmp_dir()
    builder = DummyMnist(data_dir=cls._tfds_tmp_dir)
    builder.download_and_prepare()

  @classmethod
  def tearDownClass(cls):
    super(DocumentDatasetsTest, cls).tearDownClass()
    testing.rm_tmp_dir(cls._tfds_tmp_dir)

  def setUp(self):
    super(DocumentDatasetsTest, self).setUp()
    self.builder = DummyMnist(data_dir=self._tfds_tmp_dir)

  @testing.run_in_graph_and_eager_modes()
  def test_schema_org(self):
    schema_str = document_datasets.document_single_builder(self.builder)
    self.assertIn("http://schema.org/Dataset", schema_str)
    self.assertIn(
        '<meta itemprop="url" '
        'content="https://www.tensorflow.org'
        '/datasets/catalog/%s" />' % self.builder.name, schema_str)

  def test_with_config(self):
    """Test that builder with configs are correctly generated."""
    with testing.tmp_dir() as tmp_dir:
      builder = DummyMnistConfigs(data_dir=tmp_dir)
      builder.download_and_prepare()
    doc_str = document_datasets.document_single_builder(builder)

    self.assertIn("Some manual instructions.", doc_str)
    self.assertIn("Mnist description.", doc_str)  # Shared description.
    self.assertIn("Config description.", doc_str)  # Config-specific description

if __name__ == "__main__":
  testing.test_main()
