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
"""Tests for smallnorb.py."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
from absl.testing import absltest
from absl.testing import parameterized
import numpy as np
from tensorflow_datasets.image import smallnorb as smallnorb_tfds
from tensorflow_datasets.testing import smallnorb as smallnorb_builder
from tensorflow_datasets.testing import test_utils


class SmallnorbTest(parameterized.TestCase):

  @parameterized.named_parameters(
      ("uint8", np.array([[1, 2, 3], [1, 2, 3]], dtype=np.dtype("|u1"))),
      ("int32", np.array([-1, 0, 1], dtype=np.dtype("<i4"))),)
  def test_write_and_read(self, matrix):
    with test_utils.tmp_dir() as directory:
      path = os.path.join(directory, "matrix.mat")
      smallnorb_builder.write_binary_matrix(path, matrix)
      restored_matrix = smallnorb_tfds.read_binary_matrix(path)
      np.testing.assert_allclose(restored_matrix, matrix)


if __name__ == "__main__":
  absltest.main()
