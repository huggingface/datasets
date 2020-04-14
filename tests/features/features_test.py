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
# coding=utf-8
"""Tests for tensorflow_datasets.core.features.feature.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import textwrap
import numpy as np
import tensorflow.compat.v2 as tf
from tensorflow_datasets import testing
from tensorflow_datasets.core import features as features_lib

tf.enable_v2_behavior()


class AnInputConnector(features_lib.FeatureConnector):
  """Simple FeatureConnector implementing the based methods used for test."""

  def get_tensor_info(self):
    # With this connector, the way the data is on disk ({'a', 'b'}) do not match
    # the way it is exposed to the user (int64), so we overwrite
    # FeaturesDict.get_tensor_info
    return features_lib.TensorInfo(shape=(), dtype=tf.int64)

  def get_serialized_info(self):
    return {
        'a': features_lib.TensorInfo(shape=(), dtype=tf.int64),
        'b': features_lib.TensorInfo(shape=(), dtype=tf.int64),
    }

  def encode_example(self, example_data):
    # Encode take the input data and wrap in in a dict
    return {
        'a': example_data + 1,
        'b': example_data * 10
    }

  def decode_example(self, tfexample_dict):
    # Merge the two values
    return tfexample_dict['a'] + tfexample_dict['b']


class AnOutputConnector(features_lib.FeatureConnector):
  """Simple FeatureConnector implementing the based methods used for test."""

  def get_tensor_info(self):
    return features_lib.TensorInfo(shape=(), dtype=tf.float32)

  def encode_example(self, example_data):
    return example_data * 10.0

  def decode_example(self, tfexample_data):
    return tfexample_data / 10.0


class FeatureDictTest(testing.FeatureExpectationsTestCase):

  def test_tensor_info(self):

    self.assertEqual(
        features_lib.TensorInfo(shape=(None, 3), dtype=tf.string),
        features_lib.TensorInfo(shape=(None, 3), dtype=tf.string),
    )

    self.assertNotEqual(
        features_lib.TensorInfo(shape=(None, 3), dtype=tf.string),
        features_lib.TensorInfo(shape=(None, 3), dtype=tf.int32),
    )

    self.assertNotEqual(
        features_lib.TensorInfo(shape=(2, 3), dtype=tf.string),
        features_lib.TensorInfo(shape=(5, 3), dtype=tf.string),
    )

    t = features_lib.TensorInfo(shape=(None, 3), dtype=tf.string)
    self.assertEqual(t, features_lib.TensorInfo.copy_from(t))

  def test_fdict(self):

    self.assertFeature(
        feature=features_lib.FeaturesDict({
            'input': AnInputConnector(),
            'output': AnOutputConnector(),
            'img': {
                'size': {
                    'height': tf.int64,
                    'width': tf.int64,
                },
                'metadata/path': tf.string,
            }
        }),
        serialized_info={
            'input': {
                'a': features_lib.TensorInfo(shape=(), dtype=tf.int64),
                'b': features_lib.TensorInfo(shape=(), dtype=tf.int64),
            },
            'output': features_lib.TensorInfo(shape=(), dtype=tf.float32),
            'img': {
                'size': {
                    'height': features_lib.TensorInfo(shape=(), dtype=tf.int64),
                    'width': features_lib.TensorInfo(shape=(), dtype=tf.int64),
                },
                'metadata/path':
                    features_lib.TensorInfo(shape=(), dtype=tf.string),
            }
        },
        dtype={
            'input': tf.int64,
            'output': tf.float32,
            'img': {
                'size': {
                    'height': tf.int64,
                    'width': tf.int64,
                },
                'metadata/path': tf.string,
            }
        },
        shape={
            'input': (),
            'output': (),
            'img': {
                'size': {
                    'height': (),
                    'width': (),
                },
                'metadata/path': (),
            },
        },
        tests=[
            # Np array
            testing.FeatureExpectationItem(
                value={
                    'input': 1,
                    'output': -1,
                    'img': {
                        'size': {
                            'height': 256,
                            'width': 128,
                        },
                        'metadata/path': 'path/to/xyz.jpg',
                    }
                },
                expected_serialized={
                    'input': {
                        'a': 2,  # 1 + 1
                        'b': 10,  # 1 * 10
                    },
                    'output': -10.0,  # -1 * 10.0
                    'img': {
                        'size': {
                            'height': 256,
                            'width': 128,
                        },
                        'metadata/path': 'path/to/xyz.jpg',
                    }
                },
                expected={
                    # a = 1 + 1, b = 1 * 10 => output = a + b = 2 + 10 = 12
                    'input': 12,  # 2 + 10
                    'output': -1.0,
                    'img': {
                        'size': {
                            'height': 256,
                            'width': 128,
                        },
                        'metadata/path':
                            tf.compat.as_bytes('path/to/xyz.jpg'),
                    },
                },
            ),
        ],
    )

  def test_feature_getitem(self):
    fdict = features_lib.FeaturesDict({
        'integer': tf.int32,
        'string': tf.string,
    })
    self.assertEqual(fdict['integer'].dtype, tf.int32)
    self.assertEqual(fdict['string'].dtype, tf.string)

  def test_feature__repr__(self):

    label = features_lib.ClassLabel(names=['m', 'f'])
    feature_dict = features_lib.FeaturesDict({
        'metadata': features_lib.Sequence({
            'frame': features_lib.Image(shape=(32, 32, 3)),
        }),
        'label': features_lib.Sequence(label),
    })

    self.assertEqual(
        repr(feature_dict),
        textwrap.dedent("""\
        FeaturesDict({
            'label': Sequence(ClassLabel(shape=(), dtype=tf.int64, num_classes=2)),
            'metadata': Sequence({
                'frame': Image(shape=(32, 32, 3), dtype=tf.uint8),
            }),
        })"""),
    )

  def test_feature_save_load_metadata_slashes(self):
    with testing.tmp_dir() as data_dir:
      fd = features_lib.FeaturesDict({
          'image/frame': features_lib.Image(shape=(32, 32, 3)),
          'image/label': features_lib.ClassLabel(num_classes=2),
      })
      fd.save_metadata(data_dir)
      fd.load_metadata(data_dir)


class FeatureTensorTest(testing.FeatureExpectationsTestCase):

  def test_shape_static(self):

    np_input = np.random.rand(2, 3).astype(np.float32)
    array_input = [
        [1, 2, 3],
        [4, 5, 6],
    ]

    self.assertFeature(
        feature=features_lib.Tensor(shape=(2, 3), dtype=tf.float32),
        dtype=tf.float32,
        shape=(2, 3),
        tests=[
            # Np array
            testing.FeatureExpectationItem(
                value=np_input,
                expected=np_input,
            ),
            # Python array
            testing.FeatureExpectationItem(
                value=array_input,
                expected=array_input,
            ),
            # Invalid dtype
            testing.FeatureExpectationItem(
                value=np.random.randint(256, size=(2, 3)),
                raise_cls=ValueError,
                raise_msg='int64 do not match',
            ),
            # Invalid shape
            testing.FeatureExpectationItem(
                value=np.random.rand(2, 4).astype(np.float32),
                raise_cls=ValueError,
                raise_msg='are incompatible',
            ),
        ],
    )

  def test_shape_dynamic(self):

    np_input_dynamic_1 = np.random.randint(256, size=(2, 3, 2), dtype=np.int32)
    np_input_dynamic_2 = np.random.randint(256, size=(5, 3, 2), dtype=np.int32)

    self.assertFeature(
        feature=features_lib.Tensor(shape=(None, 3, 2), dtype=tf.int32),
        dtype=tf.int32,
        shape=(None, 3, 2),
        tests=[
            testing.FeatureExpectationItem(
                value=np_input_dynamic_1,
                expected=np_input_dynamic_1,
            ),
            testing.FeatureExpectationItem(
                value=np_input_dynamic_2,
                expected=np_input_dynamic_2,
            ),
            # Invalid shape
            testing.FeatureExpectationItem(
                value=
                np.random.randint(256, size=(2, 3, 1), dtype=np.int32),
                raise_cls=ValueError,
                raise_msg='are incompatible',
            ),
        ]
    )

  def test_bool_flat(self):

    self.assertFeature(
        feature=features_lib.Tensor(shape=(), dtype=tf.bool),
        dtype=tf.bool,
        shape=(),
        tests=[
            testing.FeatureExpectationItem(
                value=np.array(True),
                expected=True,
            ),
            testing.FeatureExpectationItem(
                value=np.array(False),
                expected=False,
            ),
            testing.FeatureExpectationItem(
                value=True,
                expected=True,
            ),
            testing.FeatureExpectationItem(
                value=False,
                expected=False,
            ),
        ]
    )

  def test_bool_array(self):

    self.assertFeature(
        feature=features_lib.Tensor(shape=(3,), dtype=tf.bool),
        dtype=tf.bool,
        shape=(3,),
        tests=[
            testing.FeatureExpectationItem(
                value=np.array([True, True, False]),
                expected=[True, True, False],
            ),
            testing.FeatureExpectationItem(
                value=[True, False, True],
                expected=[True, False, True],
            ),
        ]
    )

  def test_string(self):
    nonunicode_text = 'hello world'
    unicode_text = u'你好'

    self.assertFeature(
        feature=features_lib.Tensor(shape=(), dtype=tf.string),
        shape=(),
        dtype=tf.string,
        tests=[
            # Non-unicode
            testing.FeatureExpectationItem(
                value=nonunicode_text,
                expected=tf.compat.as_bytes(nonunicode_text),
            ),
            # Unicode
            testing.FeatureExpectationItem(
                value=unicode_text,
                expected=tf.compat.as_bytes(unicode_text),
            ),
            # Empty string
            testing.FeatureExpectationItem(
                value='',
                expected=b'',
            ),
            # Trailing zeros
            testing.FeatureExpectationItem(
                value=b'abc\x00\x00',
                expected=b'abc\x00\x00',
            ),
        ],
    )

    self.assertFeature(
        feature=features_lib.Tensor(shape=(2, 1), dtype=tf.string),
        shape=(2, 1),
        dtype=tf.string,
        tests=[
            testing.FeatureExpectationItem(
                value=[[nonunicode_text], [unicode_text]],
                expected=[
                    [tf.compat.as_bytes(nonunicode_text)],
                    [tf.compat.as_bytes(unicode_text)],
                ],
            ),
            testing.FeatureExpectationItem(
                value=[nonunicode_text, unicode_text],  # Wrong shape
                raise_cls=ValueError,
                raise_msg='(2,) and (2, 1) must have the same rank',
            ),
            testing.FeatureExpectationItem(
                value=[['some text'], [123]],  # Wrong dtype
                raise_cls=TypeError,
                raise_msg='Expected binary or unicode string, got 123',
            ),
        ],
    )

  def test_repr_tensor(self):

    # Top level Tensor is printed expanded
    self.assertEqual(
        repr(features_lib.Tensor(shape=(), dtype=tf.int32)),
        'Tensor(shape=(), dtype=tf.int32)',
    )

    # Sequences colapse tensor repr
    self.assertEqual(
        repr(features_lib.Sequence(tf.int32)),
        'Sequence(tf.int32)',
    )

    class ChildTensor(features_lib.Tensor):
      pass

    self.assertEqual(
        repr(features_lib.FeaturesDict({
            'colapsed': features_lib.Tensor(shape=(), dtype=tf.int32),
            # Tensor with defined shape are printed expanded
            'noncolapsed': features_lib.Tensor(shape=(1,), dtype=tf.int32),
            # Tensor inherited are expanded
            'child': ChildTensor(shape=(), dtype=tf.int32),
        })),
        textwrap.dedent("""\
        FeaturesDict({
            'child': ChildTensor(shape=(), dtype=tf.int32),
            'colapsed': tf.int32,
            'noncolapsed': Tensor(shape=(1,), dtype=tf.int32),
        })"""),
    )


if __name__ == '__main__':
  testing.test_main()
