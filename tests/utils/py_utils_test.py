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
"""Tests for py_utils."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import hashlib
import os
from tensorflow_datasets import testing
from tensorflow_datasets.core import constants
from tensorflow_datasets.core.utils import py_utils


class PyUtilsTest(testing.TestCase):

  def test_is_notebook(self):
    self.assertFalse(py_utils.is_notebook())

  def test_map_nested(self):
    """Test the mapping function."""
    def map_fn(x):
      return x * 10

    result = py_utils.map_nested(map_fn, {
        'a': 1,
        'b': {
            'c': 2,
            'e': [3, 4, 5],
        },
    })
    self.assertEqual(result, {
        'a': 10,
        'b': {
            'c': 20,
            'e': [30, 40, 50],
        },
    })

    result = py_utils.map_nested(map_fn, [1, 2, 3])
    self.assertEqual(result, [10, 20, 30])

    result = py_utils.map_nested(map_fn, 1)
    self.assertEqual(result, 10)

  def test_zip_nested(self):
    """Test the zip nested function."""

    arg0 = {
        'a': 1,
        'b': {
            'c': 2,
            'e': [3, 4, 5],
        },
    }
    arg1 = {
        'a': 10,
        'b': {
            'c': 20,
            'e': [30, 40, 50],
        },
    }

    result = py_utils.zip_nested(arg0, arg1)
    self.assertEqual(result, {
        'a': (1, 10),
        'b': {
            'c': (2, 20),
            'e': [(3, 30), (4, 40), (5, 50)],
        },
    })

    result = py_utils.zip_nested(1, 2)
    self.assertEqual(result, (1, 2))

  def test_dict_only(self):
    def map_fn(x):
      return x[0] + x[1]

    arg0 = {
        'a': (1, 2),
        'b': {
            'c': 2,
            'e': [3, 4, 5],
        },
    }
    arg1 = {
        'a': (10, 20),
        'b': {
            'c': 20,
            'e': [30, 40, 50],
        },
    }

    result = py_utils.zip_nested(arg0, arg1, dict_only=True)
    self.assertEqual(result, {
        'a': ((1, 2), (10, 20)),
        'b': {
            'c': (2, 20),
            'e': ([3, 4, 5], [30, 40, 50]),
        },
    })

    result = py_utils.map_nested(map_fn, result, dict_only=True)
    self.assertEqual(result, {
        'a': (1, 2, 10, 20),
        'b': {
            'c': 22,
            'e': [3, 4, 5, 30, 40, 50],
        },
    })

  def test_flatten_nest_dict(self):

    nest_d = {
        'a': 1,
        'b/c': 2,
        'b': {
            'e': 3,
            'f': {
                'g': 4
            },
        },
    }
    flat_d = {
        'a': 1,
        'b/c': 2,
        'b/e': 3,
        'b/f/g': 4,
    }

    self.assertEqual(py_utils.flatten_nest_dict(nest_d), flat_d)
    self.assertEqual(py_utils.pack_as_nest_dict(flat_d, nest_d), nest_d)

    with self.assertRaisesWithPredicateMatch(ValueError, 'Extra keys'):
      py_utils.pack_as_nest_dict({
          'a': 1,
          'b/c': 2,
          'b/e': 3,
          'b/f/g': 4,
          'b/h': 5,  # Extra key
      }, nest_d)

    with self.assertRaisesWithPredicateMatch(KeyError, 'b/e'):
      py_utils.pack_as_nest_dict(
          {
              'a': 1,
              'b/c': 2,
              'b/d': 3,
          },
          {
              'a': 1,
              'b': {
                  'c': 2,
                  'd': 3,
                  'e': 4,  # Extra key
              }
          },
      )

    with self.assertRaisesWithPredicateMatch(
        ValueError, 'overwrite existing key:'):
      py_utils.flatten_nest_dict({
          'a': {
              'b': 1,
          },
          'a/b': 2,  # Collision
      })

  def test_tfds_dir(self):
    """Test the proper suffix only, since the prefix can vary."""
    self.assertTrue(py_utils.tfds_dir().endswith('/tensorflow_datasets'))


class ReadChecksumDigestTest(testing.TestCase):

  def test_digest(self):
    digest, size = py_utils.read_checksum_digest(
        os.path.join(self.test_data, '6pixels.png'), hashlib.sha256)
    self.assertEqual(
        digest,
        '04f38ebed34d3b027d2683193766155912fba647158c583c3bdb4597ad8af34c')
    self.assertEqual(102, size)


class GetClassPathUrlTest(testing.TestCase):

  def test_get_class_path(self):
    cls_path = py_utils.get_class_path(py_utils.NonMutableDict)
    self.assertEqual(cls_path, 'tfds.core.utils.py_utils.NonMutableDict')
    cls_path = py_utils.get_class_path(
        py_utils.NonMutableDict(), use_tfds_prefix=False)
    self.assertEqual(cls_path,
                     'tensorflow_datasets.core.utils.py_utils.NonMutableDict')

  def test_get_class_url(self):
    cls_url = py_utils.get_class_url(py_utils.NonMutableDict)
    self.assertEqual(
        cls_url,
        (constants.SRC_BASE_URL + 'tensorflow_datasets/core/utils/py_utils.py'))


if __name__ == '__main__':
  testing.test_main()
